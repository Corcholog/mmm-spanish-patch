"""Translation files -> script files OLM/O0..O7.

    python -I -X utf8 tools/insert_script.py [--src DIR] [--out DIR] [--identity]

For every record with Spanish text: re-attach its original start/end codes, convert
accents (tools/charmap.py), pre-wrap at 47 characters, then
  * write it back IN PLACE if it fits in the old slot (old text + its zero padding), or
  * append it at the end of the file (16-byte aligned) if it doesn't,
and rewrite every pointer to it (also pointers into the middle of a record). Records
without Spanish stay byte-for-byte as they were. Header size fields are updated.

--identity: the ES fields contain the original Japanese (round-trip test); encode as
Shift-JIS without wrapping.
"""
import argparse
import glob
import os
import re
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import olm  # noqa: E402
import project  # noqa: E402
import script_text as st  # noqa: E402

ENTRY_RE = re.compile(r'^== (O\d):(\d{4})(?:\.(\d+))?\s+@0x([0-9a-fA-F]+)')


def read_translations(folder, name):
    """{part start offset: Spanish text} for one script file (only non-empty ES)."""
    es = {}
    for path in sorted(glob.glob(os.path.join(folder, name, f'{name}_*.txt'))):
        cur = None
        with open(path, encoding='utf-8') as f:
            for lineno, line in enumerate(f, 1):
                line = line.rstrip('\n')
                m = ENTRY_RE.match(line)
                if m:
                    if m.group(1) != name:
                        raise SystemExit(f'{path}:{lineno}: entry for {m.group(1)} in a {name} file')
                    cur = int(m.group(4), 16)
                elif line.startswith('ES:') and cur is not None:
                    text = line[3:]
                    if text.startswith(' '):          # the single space after "ES:"
                        text = text[1:]
                    if text.strip(' '):               # only plain spaces count as empty (U+3000 is text)
                        es[cur] = text
    return es


EXE_ENTRY_RE = re.compile(r'^== (O\d):X\d{3}\s+@0x([0-9a-fA-F]+)')


def read_exe_translations(folder, name):
    """{instruction offset: Spanish} from <name>_exe.txt (strings the game takes from the
    executable; see dump_script.dump_exe)."""
    path = os.path.join(folder, name, f'{name}_exe.txt')
    out, cur = {}, None
    if not os.path.exists(path):
        return out
    with open(path, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            m = EXE_ENTRY_RE.match(line)
            if m:
                cur = int(m.group(2), 16)
            elif line.startswith('ES:') and cur is not None:
                text = line[4:] if line.startswith('ES: ') else line[3:]
                if text.strip(' '):
                    out[cur] = text
    return out


def exe_strings(orig, exe_es, out, laid_out=None):
    """Append the Spanish for executable strings to `out` and point their instructions at it.
    `laid_out`: {site: encoded text} from chains() (with the space or line break it needs
    next to the text around it)."""
    laid_out = laid_out or {}
    import script_model
    model = script_model.build('', bytes(orig))
    by_site = {l.site: l for l in model.lines if l.target < 0}
    for site, text in sorted(exe_es.items()):
        if site not in by_site:
            raise SystemExit(f'executable-string entry @0x{site:x} is not an executable text line')
        lead, _, tail = st.split(by_site[site].exe_text)
        body = lead + laid_out.get(site, st.encode_spanish([text])[0]) + tail
        out += b'\0' * (-len(out) % olm.ALIGN)
        struct.pack_into('<I', out, site, olm.BASE + len(out))
        out += body + b'\0'
    return len(exe_es)


def chains(orig, recs, es, exe_es=None):
    """Wrap the text lines that the game shows on one screen line as one text.

    The groups come from the bytecode (script_model: consecutive text lines with no line
    break, wait, page end, menu, window, scene or jump between them). Returns
    {record start: [encoded parts]} for the records of every group with two or more pieces.
    A group is skipped (each record wrapped on its own) if one of its records is not fully
    translated, is read from the middle, or already belongs to another group. Short strings
    the game takes from the executable (script_model kind 'exe') count with their own width.
    """
    import script_model
    items = {}
    for t, ln, all_parts in recs:
        if not any(p in es for p in all_parts):
            continue
        lead, tail, parts, _ = st.layout(t, ln, all_parts, orig[t:t + ln])
        texts = [es.get(p) for p in parts]
        if any(x is None for x in texts):
            continue
        texts[-1], _ = st.strip_page_token(texts[-1])
        items[t] = dict(lead=lead, texts=[st.charmap.normalize(p).replace(st.LF, '\n') for p in texts])
    out, used = {}, set()
    for ch in script_model.build('', bytes(orig)).chains():
        group, ok, number = [], True, False
        for line in ch:
            if line.number_before and group:
                # the game draws a number here (Indian poker cards): the text before it needs
                # a trailing space, or "es" + 7 shows as "es7"
                t0, texts0 = group[-1]
                group[-1] = (t0, texts0[:-1] + [texts0[-1].rstrip(' ') + ' '])
                # and the card name takes room on the line: wrap as if it were there
                group.append((None, ['#' * st.NUMBER_COLS]))
                number = True
            if line.kind == 'exe':
                if line.site in exe_es:          # its Spanish replacement is what will be shown
                    group.append((('exe', line.site), [st.charmap.normalize(exe_es[line.site])]))
                    continue
                visible = st.CODE_RE.sub('', line.exe_text.decode('cp932')).strip('\n')
                if visible:
                    group.append((None, [visible]))
            elif line.kind == 'line' and line.target == line.record and line.record in items:
                # a record reached from several branches is in several chains: it is wrapped
                # with the first one, and tools/screens.py checks every branch as shipped
                group.append((line.record, items[line.record]['texts']))
            else:
                ok = False
        records = [t for t, _ in group if isinstance(t, int)]
        if not ok or (len(group) < 2 and not number) or not records:
            continue
        wrapped = st.chain_wrap([texts for _, texts in group], items[records[0]]['lead'] == st.LEAD)
        for (t, _), parts in zip(group, wrapped):
            if t in used:                    # already laid out by an earlier branch
                continue
            if isinstance(t, int):
                out[t] = [st.charmap.encode(p) for p in parts]
            elif t is not None:              # ('exe', site): keeps its join space / line break
                out[t] = st.charmap.encode(''.join(parts))
            used.add(t)
    return out


def rebuild(orig, es, encode, exe_es=None):
    """Return (new file bytes, stats). es: {part start: text}; encode: list[str] -> list[bytes];
    exe_es: {instruction offset: text} for strings the game takes from the executable."""
    recs, sites = olm.record_parts(orig)
    known = {p for _, _, parts in recs for p in parts}
    stray = sorted(p for p in es if p not in known)
    if stray:      # Spanish that no pointer reads would be dropped silently
        raise SystemExit('translations at offsets that are not text entries: '
                         + ', '.join(f'0x{p:x}' for p in stray[:8]) + ' (re-dump or merge them)')
    out = bytearray(orig)
    new_addr = {}      # record start -> new start
    new_part = {}      # part start -> offset of that part inside the new record
    stats = dict(records=len(recs), translated=0, in_place=0, moved=0)
    chain_enc = chains(orig, recs, es, exe_es or {}) if encode is st.encode_spanish else {}
    for t, ln, all_parts in recs:
        if not any(p in es for p in all_parts):
            continue
        body = orig[t:t + ln]
        lead, tail, parts, tail_parts = st.layout(t, ln, all_parts, body)
        tail_start = t + ln - len(tail)
        bounds = parts + [tail_start]
        pieces = []
        for k, p in enumerate(parts):
            piece = orig[bounds[k]:bounds[k + 1]]
            if k == 0:
                piece = piece[len(lead):]
            pieces.append(piece)
        texts = [es.get(p) for p in parts]
        new_tail = tail
        if texts[-1] is not None:
            texts[-1], page_end = st.strip_page_token(texts[-1])
            if page_end:                      # <PAGE>: end the narration page after this entry
                assert not tail_parts, f'<PAGE> on an entry with a pointer into its ending (0x{t:x})'
                new_tail = st.PAGE_TAIL
        if t in chain_enc:
            enc = chain_enc[t]
        else:
            enc = encode([x if x is not None else pieces[k] for k, x in enumerate(texts)], lead == st.LEAD)
        new = bytearray(lead)
        offs = []
        for k, b in enumerate(enc):
            offs.append(len(new) if k else 0)
            new += b
        before_tail = len(new)
        new += new_tail
        stats['translated'] += 1
        for k, p in enumerate(parts):
            new_part[p] = offs[k]
        for p in tail_parts:
            new_part[p] = before_tail + (p - tail_start)
        cap = olm.slot_capacity(orig, t, ln)
        if len(new) + 1 <= cap:
            out[t:t + cap] = bytes(new) + b'\0' * (cap - len(new))
            new_addr[t] = t
            stats['in_place'] += 1
        else:
            out[t:t + ln + 1] = b'\0' * (ln + 1)
            new_addr[t] = len(out)
            out += bytes(new) + b'\0'
            out += b'\0' * (-len(out) % olm.ALIGN)
            stats['moved'] += 1
    # pointers
    starts = [r[0] for r in recs]
    rewritten = 0
    import bisect
    for o, target in sites:
        rs = starts[bisect.bisect_right(starts, target) - 1]
        if rs not in new_addr:
            continue
        nt = new_addr[rs] + new_part.get(target, 0)
        if nt != target:
            struct.pack_into('<I', out, o, olm.BASE + nt)
            rewritten += 1
    laid_out = {k[1]: v for k, v in chain_enc.items() if isinstance(k, tuple)}
    stats['exe_strings'] = exe_strings(orig, exe_es, out, laid_out) if exe_es else 0
    if len(out) != len(orig):
        out += b'\0' * (-len(out) % olm.FILE_ALIGN)
        struct.pack_into('<I', out, 0x10, len(out) - olm.HDR)
        struct.pack_into('<I', out, 0x18, olm.BASE + len(out))
        struct.pack_into('<I', out, 0x1C, olm.BASE + len(out))
    stats.update(pointers_rewritten=rewritten, size=len(out), ends_at=olm.BASE + len(out))
    return bytes(out), stats


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--src', default=project.TRANSLATION)
    ap.add_argument('--out', default=os.path.join(project.ROOT, 'work', 'inserted'))
    ap.add_argument('--identity', action='store_true')
    args = ap.parse_args()
    encode = st.encode_identity if args.identity else st.encode_spanish
    os.makedirs(args.out, exist_ok=True)
    limit = project.OVERLAY_LIMIT
    for name in project.SCRIPTS:
        orig = project.read_iso_file('OLM/' + name)
        new, s = rebuild(orig, read_translations(args.src, name), encode,
                         None if args.identity else read_exe_translations(args.src, name))
        with open(os.path.join(args.out, name), 'wb') as f:
            f.write(new)
        flag = '  <-- TOO BIG' if s['ends_at'] > limit else ''
        print(f"{name}: {s['translated']}/{s['records']} translated, {s['in_place']} in place, {s['moved']} moved, "
              f"{s['pointers_rewritten']} pointers, {s['size']:,} bytes (ends 0x{s['ends_at']:X}){flag}")


if __name__ == '__main__':
    main()
