"""Compare two ISO 9660 images file by file (by path, size, SHA-1).

Usage:
    python tools/iso_diff.py <iso_a> <iso_b> [report.tsv]

Reads straight from the images; nothing is extracted. Reports files that were
added, removed, resized, or changed, and files that stayed identical but moved
to a different LBA (sector).
"""
import hashlib
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iso_extract import SECTOR, list_files  # noqa: E402


def sha1_of(f, lba, size):
    h = hashlib.sha1()
    f.seek(lba * SECTOR)
    remaining = size
    while remaining:
        chunk = f.read(min(remaining, 16 * 1024 * 1024))
        h.update(chunk)
        remaining -= len(chunk)
    return h.hexdigest()


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    a_path, b_path = sys.argv[1:3]
    _, a_sectors, a_files = list_files(a_path)
    _, b_sectors, b_files = list_files(b_path)
    a = {p: (lba, size) for p, lba, size in a_files}
    b = {p: (lba, size) for p, lba, size in b_files}
    print(f'A: {len(a)} files, {a_sectors} sectors   B: {len(b)} files, {b_sectors} sectors')

    rows = []
    with open(a_path, 'rb') as fa, open(b_path, 'rb') as fb:
        for p in sorted(set(a) | set(b)):
            if p not in b:
                rows.append((p, 'REMOVED', a[p][1], '', a[p][0], ''))
            elif p not in a:
                rows.append((p, 'ADDED', '', b[p][1], '', b[p][0]))
            else:
                (la, sa), (lb, sb) = a[p], b[p]
                if sa != sb:
                    status = 'RESIZED'
                elif sha1_of(fa, la, sa) != sha1_of(fb, lb, sb):
                    status = 'CHANGED'
                elif la != lb:
                    status = 'MOVED'
                else:
                    continue
                rows.append((p, status, sa, sb, la, lb))

    counts = {}
    for r in rows:
        counts[r[1]] = counts.get(r[1], 0) + 1
    print('Summary:', counts or 'no differences')
    print(f'{"status":8} {"size A":>12} {"size B":>12} {"lba A":>8} {"lba B":>8}  path')
    for p, st, sa, sb, la, lb in rows:
        print(f'{st:8} {sa!s:>12} {sb!s:>12} {la!s:>8} {lb!s:>8}  {p}')
    if len(sys.argv) > 3:
        with open(sys.argv[3], 'w', encoding='utf-8', newline='\n') as t:
            t.write('path\tstatus\tsize_a\tsize_b\tlba_a\tlba_b\n')
            for p, st, sa, sb, la, lb in rows:
                t.write(f'{p}\t{st}\t{sa}\t{sb}\t{la}\t{lb}\n')


if __name__ == '__main__':
    main()
