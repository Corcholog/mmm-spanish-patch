"""Lay out every screen of a script exactly as the build ships it, and report problems.

    python -I -X utf8 tools/screens.py [O0 ...] [--png]   ->  work/screens/<script>.txt

The script is rebuilt in memory (insert_script.rebuild, same wrapping as build.py), then
every text line is followed in play order (script_model) and read back from the rebuilt
file, so what is checked is the bytes the game will read, not a copy of the wrap logic.

Layout model of the engine (docs/KNOWLEDGE.md 4.7): codes have no width; a line-feed byte
starts a new row; \\k waits for a key and ends the page; half-width characters are 13 px,
full-width (Shift-JIS) 24 px; the engine wraps by itself past 47 columns (611 px), the
dialogue box shows 46 columns (598 px), narration pages 47. The card name the game draws
(Indian poker: "10 de corazones", "reina de diamantes") is counted as its longest, 18 columns.

Errors: a row wider than the visible width, an automatic engine wrap, more rows than the
box or page holds, a blank menu option or one with a line break, two words glued where two
text lines meet, Japanese or full-width characters on a screen with Spanish.
Warnings: a row that starts with a space or with , . ; : (or ends up empty).
"""
import argparse
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import charmap  # noqa: E402
import check  # noqa: E402
import insert_script as ins  # noqa: E402
import olm  # noqa: E402
import project  # noqa: E402
import script_model  # noqa: E402
import script_text as st  # noqa: E402

HALF, FULL = 13, 24
WRAP_PX = st.LINE_WIDTH * HALF                    # 611: the engine wraps beyond this
VISIBLE_PX = {'dialogue': st.DIALOGUE_CONTENT_WIDTH * HALF, 'narration': st.LINE_WIDTH * HALF}
ROWS = {'dialogue': st.DIALOGUE_PAGE_LINES, 'narration': st.NARRATION_PAGE_LINES}
NUMBER_COLS = st.NUMBER_COLS     # what the game draws there: the longest card name
CODE = re.compile(rb'\\(?:CG[0-9A-Fa-f]{8}|t\d+|FS|FE|LC|[A-Za-z])')
BACK = {stand: letter for letter, stand in charmap.SPANISH.items()}
SPANISH_OK = set(charmap.SPANISH)


def glyphs(raw):
    """Bytes as shown -> list of (char, px) and control codes ('\\k', '\\n', ...)."""
    out, i = [], 0
    while i < len(raw):
        m = CODE.match(raw, i)
        if m:
            out.append(('code', m.group().decode('ascii')))
            i = m.end()
            continue
        b = raw[i]
        if b == 0x0A:
            out.append(('code', '\n'))
            i += 1
        elif b < 0x80:
            ch = chr(b)
            out.append((BACK.get(ch, ch), HALF))
            i += 1
        else:
            out.append((raw[i:i + 2].decode('cp932', 'replace'), FULL))
            i += 2
    return out


class Screen:
    def __init__(self, kind):
        self.kind = kind
        self.rows = [[]]          # each row: list of (char, entry id)
        self.px = 0
        self.auto_wraps = []

    def newline(self):
        self.rows.append([])
        self.px = 0

    def put(self, ch, px, eid):
        if self.px + px > WRAP_PX:
            self.auto_wraps.append(eid)
            self.newline()
        self.rows[-1].append((ch, eid))
        self.px += px

    def text_rows(self):
        return [''.join(c for c, _ in r) for r in self.rows]


def kind_of(text):
    return 'narration' if text.startswith(b'\\FS') else 'dialogue'


def shown(new, line):
    """Bytes the text line prints in the rebuilt file (an executable string, or our Spanish
    replacement for it appended to the script file)."""
    ptr = olm.u32(new, line.site)
    if olm.BASE <= ptr < olm.BASE + len(new):
        return olm.text_at(new, ptr - olm.BASE)
    return line.exe_text


def simulate(name, es, data=None, exe_es=None):
    """[(screen, [entry offsets on it], [problems])] for the script with Spanish `es`
    (and `exe_es` for the executable strings)."""
    orig = data or project.read_iso_file('OLM/' + name)
    new, _ = ins.rebuild(orig, es, st.encode_spanish, exe_es) if (es or exe_es) else (orig, None)
    model = script_model.build(name)
    screens = []
    for page in model.pages():
        first = page[0][0]
        raw0 = shown(new, first)
        scr = Screen('menu' if first.kind == 'menu' else kind_of(raw0))
        if any(b'\\LC' in model.text_of(l) for ch in page for l in ch):
            scr.kind = 'poster'          # \LC: a centred full-screen title, laid out by its own rules
        offs, problems = [], []
        for chain in page:
            prev_last = None
            for line in chain:
                raw = shown(new, line)
                eid = line.target if line.target >= 0 else line.site    # exe entries are keyed by instruction
                if eid is not None:
                    offs.append(eid)
                if line.number_before:
                    before = scr.rows[-1][-1][0] if scr.rows[-1] else ' '
                    if before.isalnum():
                        problems.append(('error', eid, f'the number the game draws here is glued to the '
                                                       f'word before it ("{before}7"): add a space'))
                    for _ in range(NUMBER_COLS):
                        scr.put('#', HALF, eid)
                    prev_last = None
                gl = glyphs(raw)
                chars = [g for g in gl if g[0] != 'code']
                if prev_last is not None and chars and scr.rows[-1]:
                    a, b = prev_last, chars[0][0]
                    if a.isalnum() and b.isalnum():
                        problems.append(('error', eid, f'glued words where two text lines meet: "...{a}{b}..."'))
                    elif a in '.,;:!?' and b.isalpha():
                        problems.append(('error', eid, f'no space after "{a}" where two text lines meet: '
                                                       f'"...{a}{b}..."'))
                for g in gl:
                    if g[0] == 'code':
                        if g[1] == '\n':
                            scr.newline()
                        continue
                    scr.put(g[0], g[1], eid)
                if chars:
                    prev_last = chars[-1][0]
        screens.append((scr, offs, problems))
    return screens


def check_screen(scr, offs, problems, es, pending=frozenset()):
    """`pending`: offsets of entries not translated yet. A screen showing one of them is
    checked once it is all translated (pre-filled copies can sit next to Japanese)."""
    if pending.intersection(offs):
        return []
    out = list(problems)
    rows = scr.text_rows()
    while len(rows) > 1 and not rows[-1].strip():
        rows.pop()
    spanish = any(o in es for o in offs)
    if scr.kind == 'menu':
        if not ''.join(rows).strip():
            out.append(('error', offs[0] if offs else None, 'blank menu option'))
        if len(rows) > 1:
            out.append(('error', offs[0] if offs else None, 'menu option with a line break'))
        return out
    if not spanish or scr.kind == 'poster':
        return out
    limit_px, limit_rows = VISIBLE_PX[scr.kind], ROWS[scr.kind]
    for r, row in zip(rows, scr.rows):
        px = sum(FULL if len(c.encode('cp932', 'replace')) == 2 and c not in SPANISH_OK else HALF for c, _ in row)
        eid = row[-1][1] if row else None
        if px > limit_px:
            out.append(('error', eid, f'row is {px // HALF} columns wide, the {scr.kind} shows '
                                     f'{limit_px // HALF}: "{r.rstrip()[-30:]}"'))
        if r.strip() and (r[:1] in (' ', ',', ';', ':') or (r[:1] == '.' and r[1:2] != '.')):
            out.append(('warning', row[0][1], f'row starts with {r[:1]!r}: "{r[:30]}"'))
    for eid in scr.auto_wraps:
        out.append(('error', eid, 'the engine wraps this line by itself (a letter can get lost): '
                                  'the text has a row longer than 47 columns'))
    if len(rows) > limit_rows:
        out.append(('error', offs[-1] if offs else None,
                    f'{scr.kind} needs {len(rows)} rows, it holds {limit_rows}'))
    for row in scr.rows:
        for c, eid in row:
            if ord(c[0]) >= 0x80 and c not in SPANISH_OK and eid not in pending:
                out.append(('error', eid, f'Japanese or full-width character {c!r} on a Spanish screen'))
                break
    return out


def split_es(entries):
    """({part offset: Spanish}, {instruction offset: Spanish} for executable strings)."""
    es, exe_es = {}, {}
    for e in entries:
        if e['es'].strip(' '):
            (exe_es if ':X' in e['id'] else es)[e['off']] = e['es']
    return es, exe_es


def pending_of(entries):
    return frozenset(e['off'] for e in entries if e['ja'].strip() and not e['es'].strip(' '))


def lint(name, entries, only=None, data=None):
    """[(level, entry dict or None, message)] for a script, from check.parse-style entries.
    `only`: set of entry IDs; report only screens that show one of them."""
    by_off = {e['off']: e for e in entries}
    es, exe_es = split_es(entries)
    out = []
    for scr, offs, problems in simulate(name, es, data, exe_es):
        if only is not None and not any(by_off.get(o, {}).get('id') in only for o in offs):
            continue
        for level, eid, msg in check_screen(scr, offs, problems, es, pending_of(entries)):
            out.append((level, by_off.get(eid) or (by_off.get(offs[0]) if offs else None), msg))
    return out


def report(name, entries, png=False):
    by_off = {e['off']: e for e in entries}
    es, exe_es = split_es(entries)
    os.makedirs(os.path.join(project.ROOT, 'work', 'screens'), exist_ok=True)
    path = os.path.join(project.ROOT, 'work', 'screens', f'{name}.txt')
    n_err = n_warn = 0
    flagged = []
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        for i, (scr, offs, problems) in enumerate(simulate(name, es, None, exe_es)):
            ids = [by_off[o]['id'] for o in offs if o in by_off]
            found = check_screen(scr, offs, problems, es, pending_of(entries))
            f.write(f'--- screen {i + 1} {scr.kind} {ids[0] if ids else ""}..{ids[-1] if ids else ""}\n')
            width = VISIBLE_PX.get(scr.kind, VISIBLE_PX['dialogue']) // HALF
            for r in scr.text_rows():
                f.write(f'  |{r:<{width}}|\n')
            for level, eid, msg in found:
                f.write(f'  {level.upper()}: {by_off.get(eid, {}).get("id", "?")}: {msg}\n')
                n_err += level == 'error'
                n_warn += level == 'warning'
            if found:
                flagged.append((i + 1, scr, ids))
    print(f'{path}: {n_err} error(s), {n_warn} warning(s)')
    if png and flagged:
        render_png(name, flagged)
    return n_err


def render_png(name, flagged):
    import font_build
    from PIL import Image, ImageDraw
    font = font_build._font()
    folder = os.path.join(project.ROOT, 'work', 'screens', name)
    os.makedirs(folder, exist_ok=True)
    for no, scr, ids in flagged[:200]:
        rows = scr.text_rows()
        width = VISIBLE_PX.get(scr.kind, VISIBLE_PX['dialogue'])
        img = Image.new('RGB', (WRAP_PX + 20, 26 * max(len(rows), 1) + 20), (20, 60, 70))
        dr = ImageDraw.Draw(img)
        dr.rectangle([8, 8, 10 + width, 12 + 26 * max(len(rows), 1)], outline=(80, 220, 220))
        for y, r in enumerate(rows):
            x = 10
            for c in r:
                if ord(c[0]) >= 0x80 and c not in SPANISH_OK:
                    dr.rectangle([x, 10 + 26 * y, x + FULL, 34 + 26 * y], outline=(255, 60, 60))
                    x += FULL
                    continue
                g = font_build.render(c, font)
                for yy in range(24):
                    for xx in range(HALF):
                        v = g[yy][xx]
                        if v:
                            img.putpixel((x + xx, 10 + 26 * y + yy), (40 + v * 43,) * 3)
                x += HALF
        img.save(os.path.join(folder, f'{no:05d}_{ids[0].replace(":", "_") if ids else "x"}.png'))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('scripts', nargs='*')
    ap.add_argument('--png', action='store_true', help='also draw the flagged screens with our font')
    args = ap.parse_args()
    for name in args.scripts or project.SCRIPTS:
        entries = []
        for path in sorted(__import__('glob').glob(os.path.join(project.TRANSLATION, name, f'{name}_*.txt'))):
            entries.extend(check.parse(path))
        if any(e['es'].strip(' ') for e in entries):
            report(name, entries, args.png)


if __name__ == '__main__':
    main()
