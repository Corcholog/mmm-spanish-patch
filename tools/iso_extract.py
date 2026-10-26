"""List and extract files from an ISO 9660 disc image (PS2 DVD, 2048-byte sectors).

Usage:
    python tools/iso_extract.py list    <iso> [table.tsv]
    python tools/iso_extract.py extract <iso> <outdir> [path-prefix ...]

The file table has: path, LBA (first sector), size in bytes.
"""
import os
import struct
import sys

SECTOR = 2048


def read_sector(f, lba, count=1):
    f.seek(lba * SECTOR)
    return f.read(SECTOR * count)


def walk(f, lba, size, prefix, out, recs=None):
    data = read_sector(f, lba, (size + SECTOR - 1) // SECTOR)[:size]
    pos = 0
    while pos < size:
        rec_len = data[pos]
        if rec_len == 0:  # records never straddle sectors; skip padding
            pos = (pos // SECTOR + 1) * SECTOR
            continue
        rec = data[pos:pos + rec_len]
        rec_pos = pos
        pos += rec_len
        extent = struct.unpack_from('<I', rec, 2)[0]
        length = struct.unpack_from('<I', rec, 10)[0]
        flags = rec[25]
        name_len = rec[32]
        raw = rec[33:33 + name_len]
        if raw in (b'\x00', b'\x01'):  # "." and ".."
            continue
        name = raw.decode('shift_jis', errors='replace')
        if ';' in name:
            name = name.rsplit(';', 1)[0]  # strip ISO version suffix ";1"
        path = prefix + name
        if flags & 2:
            walk(f, extent, length, path + '/', out, recs)
        else:
            out.append((path, extent, length))
            if recs is not None:  # absolute byte offset of this file's directory record
                recs[path] = lba * SECTOR + rec_pos


def list_files(iso_path, recs=None):
    with open(iso_path, 'rb') as f:
        pvd = read_sector(f, 16)
        if pvd[0] != 1 or pvd[1:6] != b'CD001':
            raise SystemExit('Not an ISO 9660 image (no primary volume descriptor at sector 16)')
        root = pvd[156:190]
        root_lba = struct.unpack_from('<I', root, 2)[0]
        root_size = struct.unpack_from('<I', root, 10)[0]
        total_sectors = struct.unpack_from('<I', pvd, 80)[0]
        volume_id = pvd[40:72].decode('ascii', errors='replace').strip()
        files = []
        walk(f, root_lba, root_size, '', files, recs)
    files.sort(key=lambda t: t[1])
    return volume_id, total_sectors, files


def main():
    if len(sys.argv) < 3 or sys.argv[1] not in ('list', 'extract'):
        raise SystemExit(__doc__)
    cmd, iso = sys.argv[1], sys.argv[2]
    volume_id, total, files = list_files(iso)
    if cmd == 'list':
        print(f'Volume: {volume_id}  sectors: {total}  files: {len(files)}')
        lines = ['path\tlba\tsize']
        for path, lba, size in files:
            lines.append(f'{path}\t{lba}\t{size}')
            print(f'{lba:>8}  {size:>12}  {path}')
        if len(sys.argv) > 3:
            with open(sys.argv[3], 'w', encoding='utf-8', newline='\n') as t:
                t.write('\n'.join(lines) + '\n')
    else:
        outdir = sys.argv[3]
        prefixes = sys.argv[4:]  # optional: only extract paths starting with one of these
        if prefixes:
            files = [t for t in files if t[0].startswith(tuple(prefixes))]
        with open(iso, 'rb') as f:
            for path, lba, size in files:
                dest = os.path.join(outdir, *path.split('/'))
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                f.seek(lba * SECTOR)
                remaining = size
                with open(dest, 'wb') as o:
                    while remaining:
                        chunk = f.read(min(remaining, 16 * 1024 * 1024))
                        if not chunk:
                            raise SystemExit(f'Unexpected end of image while reading {path}')
                        o.write(chunk)
                        remaining -= len(chunk)
        print(f'Extracted {len(files)} files to {outdir}')


if __name__ == '__main__':
    main()
