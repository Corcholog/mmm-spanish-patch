"""Text of the script records: splitting off structural codes, the translation file
format, wrapping and encoding. (docs/KNOWLEDGE.md 4.3, 4.7, and "Translation files")
"""
import re

import charmap

LINE_WIDTH = 47          # half-width characters the engine puts on a line (KNOWLEDGE.md 4.7)
DIALOGUE_CONTENT_WIDTH = 46   # the dialogue box shows only 46 columns: a 47th character is cut in half
                              # (measured 2026-10-26 from the user's screenshots); narration uses all 47
LF = '⏎'                 # how a line-break byte (0x0A) is shown in translation files

# Codes that may sit at the very start / end of a record. They are kept automatically
# from the original record, so translators never touch them.
LEAD = b'\\FS'
TAIL_RE = re.compile(rb'(?:\\FE|\\t\d+|\\k|\\p|\\O|\\V|\n)+\Z')
# Any control code (zero width on screen)
CODE_RE = re.compile(r'\\(?:CG[0-9A-Fa-f]{8}|t\d+|FS|FE|LC|[A-Za-z])')

PART = '\x01'            # internal marker between the parts of a record (never in files)
CHAIN = '\x02'           # internal marker between consecutive records shown on the same line


def split(body):
    """Record bytes -> (lead codes, text, tail codes)."""
    lead = LEAD if body.startswith(LEAD) else b''
    rest = body[len(lead):]
    m = TAIL_RE.search(rest)
    tail = m.group() if m else b''
    return lead, rest[:len(rest) - len(tail)], tail


def layout(t, ln, parts, body):
    """Split a record into its codes and translatable parts.

    Returns (lead, tail, text_parts, tail_parts): text_parts are the pointer targets
    (record offsets) that start translatable text; tail_parts are pointers that land
    inside the ending codes (e.g. on the "\\p" of "\\k\\p"), which just follow the tail.
    """
    lead, _, tail = split(body)
    tail_start = t + ln - len(tail)
    text_parts = [p for p in parts if p < tail_start]
    tail_parts = [p for p in parts if p >= tail_start and p != t]
    if not text_parts:
        text_parts = [t]
    for p in text_parts[1:]:
        assert p >= t + len(lead), f'pointer into the leading code at 0x{p:x}'
    return lead, tail, text_parts, tail_parts


def show(raw):
    """Bytes (Shift-JIS/ASCII) -> text for a translation file."""
    return raw.decode('cp932').replace('\n', LF)


HEAD_RE = re.compile(rb'\A(?:\\FS|\\FE|\\k|\\p|\\O|\\V|\\t\d+|\n)+')


def show_english(raw):
    """English reference: drop the structural codes at both ends and the wrap padding
    (runs of spaces). The English patch sometimes starts a record with the previous
    record's ending codes, which would only confuse a reader."""
    raw = HEAD_RE.sub(b'', raw)
    raw = TAIL_RE.sub(b'', raw)
    return re.sub(r' {2,}', ' ', show(raw)).strip()


def codes_in(text):
    return CODE_RE.findall(text)


def visible_len(s):
    return len(CODE_RE.sub('', s).replace(PART, '').replace(CHAIN, ''))


WRAP_NEWLINE = True      # break lines with real line-feed bytes (confirmed in game 2026-10-26); False = pad with spaces to column 47 like the English patch (build.py --wrap pad)


def wrap(text, width=LINE_WIDTH, content=None):
    """Pre-wrap like the English patch: every line except the last of a paragraph is
    padded with spaces to exactly `width` (the engine's own wrap column), so the engine
    never cuts a word. Text lines hold at most `content` characters (default: `width`);
    the dialogue box needs content=46 because its 47th column is half hidden."""
    content = content or width
    out = []
    for para in text.split('\n'):
        words = [w for w in para.split(' ') if w != '']
        lines, line = [], ''
        for w in words:
            cand = w if not line else line + ' ' + w
            if visible_len(cand) <= content:
                line = cand
                continue
            if line:
                lines.append(line)
            while visible_len(w) > content:         # a single word longer than a line
                lines.append(w[:content])
                w = w[content:]
            line = w
        lines.append(line)
        if WRAP_NEWLINE:
            out.append('\n'.join(lines))
        else:
            out.append(''.join(l + ' ' * (width - visible_len(l)) for l in lines[:-1]) + lines[-1])
    return '\n'.join(out)


ORPHAN_MAX = 10              # a last line this short (or less) wastes a screen line: check.py warns
NUMBER_COLS = 18             # room for a card name the game draws (longest: "reina de diamantes", build.CARD_FORMATS)
NARRATION_PAGE_LINES = 10    # more lines are drawn as garbage (measured in the pilot, KNOWLEDGE.md 4.7)
DIALOGUE_PAGE_LINES = 4      # dialogue box height (estimate from a screenshot, unverified)
PAGE_TOKEN = '<PAGE>'        # end of a translation entry: end the narration page here
PAGE_TAIL = b'\\FE\\t60\\k\\O'  # the ending the game itself uses at the end of a narration page


def continues_info(info):
    """Does the next entry continue on the same screen line? `info` is what the == line shows."""
    tail = info.split('…')[-1]
    return not any(c in tail for c in ('\\k', '\\p', '\\O', LF))


def continues_bytes(tail):
    return not any(c in tail for c in (b'\n', b'\\k', b'\\p', b'\\O'))


def join_marked(texts, marker):
    """Join pieces of text that are printed one right after the other (the parts of a record, or
    consecutive records on one line) with an invisible `marker` and, when Spanish needs one, a
    space: none before , . ; : ? ! ) or after an opening mark or at an existing space. The
    Japanese has no spaces, so without this "haces" + "ESO" would be printed as "hacesESO"."""
    out = texts[0]
    for prev, nxt in zip(texts, texts[1:]):
        glue = (not prev.strip(' ')) or (not nxt) or prev.endswith((' ', '¿', '¡', '(')) or nxt[0] in ',.;:?!) '
        # the space goes at the END of the first piece: a piece the game also prints on its
        # own (a pointer into the middle of a record, O0:2728.2) must not start with a space
        out += ('' if glue else ' ') + marker + nxt
    return out


def chain_wrap(records, narration=False):
    """Wrap consecutive records that are shown on one line as a single text.

    `records`: list of records, each a list of Spanish parts (already normalized, newline =
    '\\n'). The records are joined with a space (none before , . ; : ? ! ) or after an opening
    mark), wrapped together and split again, so the pad spaces and the wrap fall on word
    boundaries across records. Returns the same structure with the wrapped parts.
    """
    content = LINE_WIDTH if narration else DIALOGUE_CONTENT_WIDTH
    out = join_marked([join_marked(r, PART) for r in records], CHAIN)
    wrapped = wrap(out, LINE_WIDTH, content)
    return [r.split(PART) for r in wrapped.split(CHAIN)]


def chain_lines(records, narration=False):
    """Screen lines the chain of records needs (records as in chain_wrap, not yet normalized)."""
    texts = [[charmap.normalize(p).replace(LF, '\n') for p in r] for r in records]
    flat = CHAIN.join(PART.join(r) for r in chain_wrap(texts, narration))
    return sum(-(-max(visible_len(l.rstrip(' ')), 1) // LINE_WIDTH) for l in flat.split('\n'))


def count_lines(text, narration=True):
    """Screen lines `text` needs after wrapping (a blank entry needs one)."""
    return chain_lines([[text]], narration)


def strip_page_token(text):
    """(text without the trailing <PAGE>, whether it had one)"""
    t = text.rstrip(' ')
    if t.endswith(PAGE_TOKEN):
        return t[:-len(PAGE_TOKEN)].rstrip(' '), True
    return text, False


def encode_spanish(text_parts, narration=False):
    """List of parts (str = Spanish from the ES: field, bytes = keep as is) -> list of bytes.

    Spanish parts of one record are wrapped together (they are shown as one line on
    screen), then split again, so pointers into the middle of a record stay on the
    right word. If some parts are kept as bytes, each Spanish part is wrapped on its own.
    Dialogue boxes (narration=False) hold 46 columns, narration pages 47.
    """
    content = LINE_WIDTH if narration else DIALOGUE_CONTENT_WIDTH
    if any(isinstance(p, bytes) for p in text_parts):
        return [p if isinstance(p, bytes)
                else charmap.encode(wrap(charmap.normalize(p).replace(LF, '\n'), LINE_WIDTH, content))
                for p in text_parts]
    joined = join_marked([charmap.normalize(p).replace(LF, '\n') for p in text_parts], PART)
    wrapped = wrap(joined, LINE_WIDTH, content)
    return [charmap.encode(p) for p in wrapped.split(PART)]


def encode_identity(text_parts, narration=False):
    """For round-trip tests: the ES field holds the original Japanese."""
    return [p if isinstance(p, bytes) else p.replace(LF, '\n').encode('cp932') for p in text_parts]
