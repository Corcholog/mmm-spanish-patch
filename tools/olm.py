"""Read and relocate the text in KID "OLM" overlay script files (OLM/O0 ... O7).

File layout (see docs/KNOWLEDGE.md section 4.3):
  0x00-0xFF  header: magic "MWo3", load address 0x4D3600, size fields at 0x10/0x18/0x1C
  0x100-     bytecode (32-bit words: 0xF00000xx opcodes, 0x4D3600+offset pointers)
             interleaved with NUL-terminated text records on 16-byte boundaries

Usage:
    python -I -X utf8 tools/olm.py audit    <O file> [english O file]
    python -I -X utf8 tools/olm.py relocate <in> <out> [--max-size N] [--mark] [--old marker|zero]
    python -I -X utf8 tools/olm.py verify   <original> <relocated>

"relocate" moves text records to the end of the file and rewrites every pointer to
them. Without a translation it's a no-change round trip: the game should behave
identically.
"""
import bisect
import struct
import sys

BASE = 0x4D3600   # RAM address the overlay is loaded at
HDR = 0x100       # header size; the body starts here
ALIGN = 16        # text records start on 16-byte boundaries
FILE_ALIGN = 0x100
MARK = '◆'.encode('cp932')   # visible marker used by test builds
OLD_MARKER = b'[OLD]'        # written into abandoned slots by test builds


def u32(d, o):
    return struct.unpack_from('<I', d, o)[0]


def text_record_len(d, t):
    """Length of the text record starting at offset t, or None if t isn't one.

    A record starts on a 4-byte boundary, directly after a NUL, is valid
    Shift-JIS (CP932) up to the next NUL, and is followed by zero padding up to
    the next 4-byte boundary. (Long records usually end up 16-byte aligned, but
    short ones like "\\k\\p" are packed one after another.)
    """
    if t % 4 or t < HDR or t >= len(d) or d[t] == 0 or d[t - 1] != 0:
        return None
    end = d.find(b'\0', t)
    if end < 0:
        return None
    body = d[t:end]
    if any(c < 0x20 and c != 0x0A for c in body):
        return None
    # bytecode can look like a tiny text record; require something text-like
    if not (any(c >= 0x81 for c in body) or sum(1 for c in body if 0x20 <= c < 0x7F) >= 2):
        return None
    try:
        body.decode('cp932')
    except UnicodeDecodeError:
        return None
    pad_end = -(-(end + 1) // 4) * 4
    if any(d[end + 1:pad_end]):
        return None
    return end - t


def analyze(d):
    """Find text records and the pointer words that refer to them.

    Returns (records, sites):
      records: {start offset: text length} for every record that is pointed at
      sites:   [(offset of the pointer word, target offset)], only pointers whose
               target is inside a known text record (at its start or in the middle)
    """
    n = len(d)
    cand = [(o, u32(d, o) - BASE) for o in range(HDR, n - 3, 4)
            if BASE + HDR <= u32(d, o) < BASE + n]
    records = {}
    for t in sorted({t for _, t in cand}):
        ln = text_record_len(d, t)
        if ln is not None:
            records[t] = ln
    # zones where bytes are text, not pointers: referenced records, plus any long
    # unreferenced text record (short ones look like pointer-table entries)
    zones = {t: ln + 1 for t, ln in records.items()}
    for t in range(HDR, n, 4):
        if t not in zones:
            ln = text_record_len(d, t)
            if ln is not None and ln >= 8:
                zones[t] = ln + 1
    starts = sorted(zones)

    def in_text(o):
        i = bisect.bisect_right(starts, o) - 1
        return i >= 0 and o < starts[i] + zones[starts[i]]

    rec_starts = sorted(records)
    sites = []
    used = set()
    for o, t in cand:
        if in_text(o):
            continue
        i = bisect.bisect_right(rec_starts, t) - 1
        if i >= 0 and t < rec_starts[i] + records[rec_starts[i]] + 1:
            if t != rec_starts[i]:
                try:    # a real mid-line pointer lands on a character boundary
                    bytes(d[rec_starts[i]:t]).decode('cp932')
                except UnicodeDecodeError:
                    continue
            sites.append((o, t))
            used.add(rec_starts[i])
    # drop "records" whose only pointer was a coincidence inside other text
    records = {t: ln for t, ln in records.items() if t in used}
    return records, sites


# What a pointer-like word is, from the words around it (docs/KNOWLEDGE.md 4.3, "Instruction forms").
# Only TEXT_KINDS are references to text and may be rewritten when text moves; the others are
# arguments that merely look like pointers into this file (jumps into another script file,
# screen rectangles, a data table) and must never change.
TEXT_KINDS = ('text', 'menu', 'credits', 'title')
OPCODE = 0xF0000000


class UnknownPointer(Exception):
    pass


def site_kind(d, o):
    """Kind of the pointer-like word at offset o."""
    def w(k):
        p = o + 4 * k
        return u32(d, p) if HDR <= p <= len(d) - 4 else None
    if w(1) == 0 and w(2) == 0 and w(3) is not None and w(3) < 0x10000:
        return 'text'              # a text line: <pointer>, 0, 0, <serial>
    if w(-2) == OPCODE:
        return 'menu'              # OP00 <option number> <pointer>
    if w(-1) == 0xF0000065:
        return 'credits'           # OP65 <pointer>, 0, <size>, 0, 0x21 (O7 staff roll)
    if w(-3) == 0xF0000061:
        return 'title'             # OP61 a, b, <pointer> (chapter titles, O4-O6)
    if w(-2) == 0xF0000006:
        return 'jump'              # OP06 <module>, <address in that module>, ...
    if w(-4) == 0xF0000048:
        return 'jump'              # OP48 a, b, <module>, <address in that module>
    for k in (1, 2, 3):
        if w(-k) in (0xF000002E, 0xF0000031, 0xF000003C, 0xF0000045, 0xF000006E):
            return 'rect'          # screen coordinates such as 0x2CA64 that look like pointers
    if w(-2) == 0xF0000048:
        return 'arg'               # OP48 0, <value>, ...: a round number (0x4F0000 in O6), not text
    if all(w(k) is not None and (w(k) & 0xFFFF) == 0x1020 for k in (-1, 1)):
        return 'data'              # O7 table at 0x1c828..: (address, size) pairs, sizes end in 0x1020
    return 'unknown'


def classify(d):
    """[(pointer offset, target, kind)] for every pointer-like word that lands on text."""
    _, sites = analyze(d)
    return [(o, t, site_kind(d, o)) for o, t in sites]


def text_sites(d, strict=True):
    """The pointer sites that really refer to text (see TEXT_KINDS). With strict=True an
    unrecognised form raises UnknownPointer instead of being guessed."""
    out, unknown = [], []
    for o, t, k in classify(d):
        if k in TEXT_KINDS:
            out.append((o, t))
        elif k == 'unknown':
            unknown.append((o, t))
    if unknown and strict:
        raise UnknownPointer('pointer-like words of an unknown form (add the form to olm.site_kind): '
                             + ', '.join(f'0x{o:x}->0x{t:x}' for o, t in unknown[:8]))
    return out


def text_analyze(d, strict=True):
    """Like analyze(), but only real text references, and only the records they point at."""
    records, _ = analyze(d)
    sites = text_sites(d, strict)
    starts = sorted(records)
    used = {starts[bisect.bisect_right(starts, t) - 1] for _, t in sites}
    return {t: ln for t, ln in records.items() if t in used}, sites


def record_parts(d, strict=True):
    """Records with their parts: [(start, length, [part starts])], plus the pointer sites.

    A record is split into parts wherever a pointer points into its middle (the game
    can start reading there), so a translation can keep that pointer on the right word.
    Only real text references count (text_sites), so a jump or a coordinate that happens
    to look like a pointer neither splits a record nor gets rewritten.
    """
    records, sites = text_analyze(d, strict)
    starts = sorted(records)
    mids = {}
    for _, t in sites:
        if t not in records:
            st = starts[bisect.bisect_right(starts, t) - 1]
            mids.setdefault(st, set()).add(t)
    return [(t, records[t], [t] + sorted(mids.get(t, ()))) for t in starts], sites


def menu_starts(d):
    """Offsets of the records that are choice-menu options.

    A menu is a run of "0xF0000000, <option number>, <pointer>" word triples in the bytecode;
    the word two places before the pointer is that opcode (O0 has 31 options, in pairs such as
    O0:0166/0167 and 0407/0408). Options are separate boxes, never text that continues on the
    same screen line.
    """
    out = set()
    for o, t, k in classify(d):
        if k == 'menu':
            out.add(t)
    return out


def slot_capacity(d, t, ln):
    """Bytes available for a record written back in place: the old text, its NUL and the
    zero padding after it (which never runs past the record's 16-byte slot; checked on all
    33,113 records)."""
    end = t + ln + 1
    while end < len(d) and d[end] == 0 and end % 16:
        end += 1
    return end - t


def new_slot_size(body_len):
    return -(-(body_len + 1) // ALIGN) * ALIGN


def relocate(d, new_text=None, mark=False, old='zero', max_size=None):
    """Move text records to the end of the file and rewrite their pointers.

    new_text: optional {record start offset: replacement bytes} (translation).
    mark:     put a visible marker after a leading "\\FS" in each moved record (tests).
    old:      what to leave in abandoned slots: 'zero' or 'marker' ("[OLD]").
    max_size: stop relocating once the file would exceed this many bytes.
    Returns (new bytes, stats dict).
    """
    new_text = new_text or {}
    records, sites = text_analyze(d)
    out = bytearray(d)
    moved = {}    # old start -> (new start, insert_at, insert_len)
    for t in sorted(records):
        body = new_text.get(t, bytes(d[t:t + records[t]]))
        ins_at, ins = 0, b''
        if mark:
            ins_at = 3 if body.startswith(b'\\FS') else 0
            ins = MARK
            body = body[:ins_at] + ins + body[ins_at:]
        if max_size is not None and len(out) + new_slot_size(len(body)) > max_size:
            break
        # abandon the old slot
        old_len = records[t]
        for i in range(old_len + 1):
            out[t + i] = 0
        if old == 'marker':
            m = OLD_MARKER[:old_len]  # never write past the old text into a neighbouring record
            out[t:t + len(m)] = m
        moved[t] = (len(out), ins_at, len(ins))
        out += body + b'\0'
        out += b'\0' * (-len(out) % ALIGN)
    # rewrite pointers
    rewritten = 0
    rec_starts = sorted(records)
    for o, t in sites:
        i = bisect.bisect_right(rec_starts, t) - 1
        start = rec_starts[i]
        if start not in moved:
            continue
        new_start, ins_at, ins_len = moved[start]
        delta = t - start
        new_t = new_start + delta + (ins_len if delta >= ins_at and ins_len else 0)
        struct.pack_into('<I', out, o, BASE + new_t)
        rewritten += 1
    out += b'\0' * (-len(out) % FILE_ALIGN)
    struct.pack_into('<I', out, 0x10, len(out) - HDR)
    struct.pack_into('<I', out, 0x18, BASE + len(out))
    struct.pack_into('<I', out, 0x1C, BASE + len(out))
    stats = dict(records=len(records), pointer_sites=len(sites), moved=len(moved),
                 pointers_rewritten=rewritten, old_size=len(d), new_size=len(out))
    return bytes(out), stats


def text_at(d, t):
    end = d.find(b'\0', t)
    return bytes(d[t:end])


def verify(orig, new, mark=False):
    """Check that following every pointer in both files reads the same text."""
    records, sites = text_analyze(orig)
    problems = []
    for o, t in sites:
        a = text_at(orig, t)
        nt = u32(new, o) - BASE
        b = text_at(new, nt)
        if mark and b.startswith(b'\\FS' + MARK):
            b = b'\\FS' + b[3 + len(MARK):]
        elif mark and b.startswith(MARK):
            b = b[len(MARK):]
        if a != b:
            problems.append((o, t, nt, a[:30], b[:30]))
    # header consistency
    if u32(new, 0x10) != len(new) - HDR:
        problems.append(('header 0x10', u32(new, 0x10), len(new) - HDR))
    if u32(new, 0x18) != BASE + len(new) or u32(new, 0x1C) != BASE + len(new):
        problems.append(('header 0x18/0x1C',))
    return problems


def audit(d, english=None):
    n = len(d)
    records, sites = analyze(d)
    print(f'file size {n} (0x{n:x}); text records pointed at: {len(records)}; pointer sites: {len(sites)}')
    targets = {t for _, t in sites}
    print(f'distinct targets: {len(targets)}; mid-record targets: {sum(1 for t in targets if t not in records)}')
    # pointer-like words whose target is NOT a text record (bytecode jump targets etc.)
    other = [(o, u32(d, o) - BASE) for o in range(HDR, n - 3, 4)
             if BASE + HDR <= u32(d, o) < BASE + n]
    site_offs = {o for o, _ in sites}
    nontext = [(o, t) for o, t in other if o not in site_offs]
    print(f'other pointer-like words (not text pointers): {len(nontext)}')
    # unaligned hits: a 4-byte value equal to a record start at a non-4-aligned offset
    starts = set(records)
    unal = 0
    for o in range(HDR + 1, n - 3):
        if o % 4 and BASE + HDR <= u32(d, o) < BASE + n and (u32(d, o) - BASE) in starts:
            unal += 1
    print(f'unaligned words equal to a record start (likely coincidence in text/data): {unal}')
    if english is not None:
        changed = [o for o in range(HDR, n - 3, 4)
                   if o < len(english) and u32(d, o) != u32(english, o) and BASE <= u32(d, o) < BASE + n]
        changed_in_sites = [o for o in changed if o in site_offs]
        print(f'English answer key: {len(changed)} pointer-like words changed; '
              f'{len(changed_in_sites)} of them are in our site list')
        missing = [o for o in changed if o not in site_offs]
        print(f'  changed words NOT found by our analysis: {len(missing)}', [hex(o) for o in missing[:10]])


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ('audit', 'relocate', 'verify'):
        raise SystemExit(__doc__)
    cmd = sys.argv[1]
    d = open(sys.argv[2], 'rb').read()
    if cmd == 'audit':
        audit(d, open(sys.argv[3], 'rb').read() if len(sys.argv) > 3 else None)
    elif cmd == 'relocate':
        args = sys.argv[4:]
        kw = {}
        if '--mark' in args:
            kw['mark'] = True
        if '--old' in args:
            kw['old'] = args[args.index('--old') + 1]
        if '--max-size' in args:
            kw['max_size'] = int(args[args.index('--max-size') + 1], 0)
        new, stats = relocate(d, **kw)
        open(sys.argv[3], 'wb').write(new)
        print(stats)
    else:
        new = open(sys.argv[3], 'rb').read()
        problems = verify(d, new, mark='--mark' in sys.argv)
        print('OK: all pointers read the same text' if not problems else f'{len(problems)} PROBLEMS: {problems[:5]}')


if __name__ == '__main__':
    main()
