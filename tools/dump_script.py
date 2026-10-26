"""Script files -> translation files (translation/O0/O0_001.txt, ...).

    python -I -X utf8 tools/dump_script.py [--out DIR] [--force]

Reads OLM/O0..O7 from the original disc; the English reference comes from
work/english (local only). Refuses to overwrite a file that already has Spanish in it
unless --force. Format: docs/KNOWLEDGE.md, "Translation files".
"""
import argparse
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import olm  # noqa: E402
import project  # noqa: E402
import script_text as st  # noqa: E402

PER_FILE = 200   # records per translation file

HEADER = """\
# My Merry May — traducción | OLM/{name}, parte {part:03d} (registros {first}–{last} de {total})
# Edit only the "ES:" lines. An empty ES keeps the original line.
# The codes in the "==" line are added back automatically. Keep any \\codes that appear
# inside JA (\\LC, \\CG…, \\d, \\o). "⏎" = line break. Don't wrap or pad lines yourself.
# Narration pages (entries whose "==" line starts with \\FS) fit at most 10 screen lines in
# total; to end a page early write <PAGE> at the end of an entry that ends with \\FE\\t60⏎.
# Run tools/check.py (add --pages to see every page) before building.

"""

HEADER_END = '== '


def english_parts(eng, sites_by_target, parts):
    """English reference text for each part of one record (or '' if unknown)."""
    if eng is None:
        return [''] * len(parts)
    out = []
    targets = []
    for p in parts:
        s = sites_by_target.get(p)
        targets.append(olm.u32(eng, s) - olm.BASE if s is not None else None)
    for k, t in enumerate(targets):
        if t is None:
            out.append('')
            continue
        raw = olm.text_at(eng, t)
        nxt = targets[k + 1] if k + 1 < len(targets) else None
        if nxt is not None and t < nxt <= t + len(raw):   # English kept the parts together
            raw = raw[:nxt - t]
        out.append(st.show_english(raw))
    return out


def dump(name, out_dir, force):
    d = project.read_iso_file('OLM/' + name)
    eng = project.english_script(name)
    recs, sites = olm.record_parts(d)
    by_target = {}
    for s, t in sorted(sites):
        by_target.setdefault(t, s)
    folder = os.path.join(out_dir, name)
    os.makedirs(folder, exist_ok=True)
    total = len(recs)
    written = 0
    for part_no, i0 in enumerate(range(0, total, PER_FILE), 1):
        path = os.path.join(folder, f'{name}_{part_no:03d}.txt')
        if os.path.exists(path) and not force and has_spanish(path):
            raise SystemExit(f'{path} already contains Spanish; not overwriting (use --force)')
        chunk = recs[i0:i0 + PER_FILE]
        lines = [HEADER.format(name=name, part=part_no, first=i0 + 1, last=i0 + len(chunk), total=total)]
        for n, (t, ln, all_parts) in enumerate(chunk, i0 + 1):
            body = d[t:t + ln]
            lead, tail, parts, _ = st.layout(t, ln, all_parts, body)
            ens = english_parts(eng, by_target, parts)
            bounds = parts + [t + ln - len(tail)]
            for k, p in enumerate(parts):
                piece = d[bounds[k]:bounds[k + 1]]
                if k == 0:
                    piece = piece[len(lead):]
                pid = f'{name}:{n:04d}' + (f'.{k + 1}' if len(parts) > 1 else '')
                info = []
                if k == 0 and lead:
                    info.append(st.show(lead))
                if k == len(parts) - 1:
                    info.append('…' + st.show(tail) if tail else '…')
                if k > 0:
                    info.insert(0, '(continues the previous entry)')
                lines.append(f'== {pid}  @0x{p:06x}  {" ".join(info)}\n')
                lines.append(f'JA: {st.show(piece)}\n')
                lines.append(f'EN: {ens[k]}\n')
                lines.append('ES: \n\n')
        with open(path, 'w', encoding='utf-8', newline='\n') as f:
            f.writelines(lines)
        written += 1
    return total, written


EXE_HEADER = """\
# My Merry May — traducción | OLM/{name}: textos cortos que el juego toma del ejecutable
# These lines are printed from strings in SLPS_251.92 (the same string can be used by
# several scripts). The build appends each Spanish text to the script file and points that
# one text instruction at it, so the executable is not changed. Edit only "ES:".

"""


def dump_exe(name, out_dir, force):
    """translation/<name>/<name>_exe.txt: the executable strings with visible text that this
    script prints (script_model kind 'exe'). IDs are <name>:X001..; @ is the instruction."""
    import script_model
    lines = [l for l in script_model.build(name).lines
             if l.target < 0 and st.CODE_RE.sub('', l.exe_text.decode('cp932')).replace('\n', '')]
    path = os.path.join(out_dir, name, f'{name}_exe.txt')
    if not lines:
        return 0
    if os.path.exists(path) and not force and has_spanish(path):
        return len(lines)
    out = [EXE_HEADER.format(name=name)]
    for i, l in enumerate(lines, 1):
        lead, text, tail = st.split(l.exe_text)
        info = ' '.join(x for x in (st.show(lead), '…' + st.show(tail) if tail else '…') if x)
        out.append(f'== {name}:X{i:03d}  @0x{l.site:06x}  (executable string) {info}\n')
        out.append(f'JA: {st.show(text)}\nEN: \nES: \n\n')
    with open(path, 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(out)
    return len(lines)


def has_spanish(path):
    with open(path, encoding='utf-8') as f:
        return any(line.startswith('ES:') and line[3:].strip(' \n') for line in f)


def refresh_headers(folder):
    """Rewrite the comment header of existing files (keeps every entry, so Spanish is safe)."""
    import glob
    import re
    n = 0
    for path in sorted(glob.glob(os.path.join(folder, '*', '*.txt'))):
        text = open(path, encoding='utf-8').read()
        m = re.match(r'# My Merry May — traducción \| OLM/(O\d), parte (\d+) \(registros (\d+)–(\d+) de (\d+)\)', text)
        if not m:
            continue
        name, part, first, last, total = m.group(1), *map(int, m.groups()[1:])
        body = text[text.index('\n' + HEADER_END) + 1:]
        new = HEADER.format(name=name, part=part, first=first, last=last, total=total) + body
        if new != text:
            open(path, 'w', encoding='utf-8', newline='\n').write(new)
            n += 1
    print(f'{n} headers refreshed')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=project.TRANSLATION)
    ap.add_argument('--force', action='store_true')
    ap.add_argument('--refresh-headers', action='store_true',
                    help='only rewrite the comment header of the existing files')
    args = ap.parse_args()
    if args.refresh_headers:
        refresh_headers(args.out)
        return
    for name in project.SCRIPTS:
        total, files = dump(name, args.out, args.force)
        exe = dump_exe(name, args.out, args.force)
        print(f'{name}: {total} records -> {files} files' + (f', {exe} executable strings' if exe else ''))


if __name__ == '__main__':
    main()
