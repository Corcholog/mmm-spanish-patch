"""List the speakers in the script (NAME「...」 lines) with the English patch's name for each.

    python -I -X utf8 tools/speakers.py

Seeds the character table in docs/STYLE_GUIDE.md. Reads translation/ (JA + EN reference).
"""
import glob
import os
import re
import sys
from collections import Counter, defaultdict

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check  # noqa: E402
import project  # noqa: E402

JA_RE = re.compile(r'^([^「」\s]{1,12})「')
EN_RE = re.compile(r'^([A-Za-z][A-Za-z .\'?!-]{0,20}): ')


def main():
    count = Counter()
    english = defaultdict(Counter)
    first = {}
    for path in sorted(glob.glob(os.path.join(project.TRANSLATION, '*', '*.txt'))):
        for e in check.parse(path):
            m = JA_RE.match(e['ja'])
            if not m:
                continue
            name = m.group(1)
            count[name] += 1
            first.setdefault(name, e['id'])
            n = EN_RE.match(e['en'])
            if n:
                english[name][n.group(1)] += 1
    print(f'{sum(count.values())} spoken lines, {len(count)} different speaker labels\n')
    print(f'{"Japanese":14} {"lines":>6}  {"English patch name":24} first seen')
    for name, n in count.most_common(60):
        en = english[name].most_common(1)[0][0] if english[name] else '?'
        print(f'{name:14} {n:6}  {en:24} {first[name]}')


if __name__ == '__main__':
    main()
