"""Copy translations from a tab-separated file into the translation/ files.

    python -I -X utf8 tools/apply_translations.py SCRIPT file.tsv [--force]

file.tsv: one translation per line, "0001<TAB>Spanish text" (the entry number of
SCRIPT, like O0:0001). Refuses to overwrite an existing translation unless --force.
Convenient for drafting a batch outside the translation files; the files stay the
source of truth.
"""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import project  # noqa: E402

ENTRY_RE = re.compile(r'^== (O\d:\d{4})\b')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('script')
    ap.add_argument('tsv')
    ap.add_argument('--force', action='store_true')
    args = ap.parse_args()
    todo = {}
    with open(args.tsv, encoding='utf-8') as f:
        for line in f:
            line = line.rstrip('\n')
            if line.strip():
                num, text = line.split('\t', 1)
                todo[f'{args.script}:{num.strip()}'] = text.strip()
    done = 0
    for path in sorted(glob.glob(os.path.join(project.TRANSLATION, args.script, '*.txt'))):
        lines = open(path, encoding='utf-8').read().split('\n')
        cur, changed = None, False
        for i, line in enumerate(lines):
            m = ENTRY_RE.match(line)
            if m:
                cur = m.group(1)
            elif line.startswith('ES:') and cur in todo:
                if line[3:].strip(' ') and not args.force:
                    raise SystemExit(f'{cur} already has Spanish; use --force to replace it')
                lines[i] = 'ES: ' + todo.pop(cur)
                changed = True
                done += 1
        if changed:
            open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(lines))
    if todo:
        print('not found:', ', '.join(sorted(todo)))
    print(f'{done} translations written')


if __name__ == '__main__':
    main()
