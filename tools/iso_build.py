"""Replace files inside an ISO 9660 image, the way the English patch does it.

Each replaced file is appended after the current end of the image, then its
directory record (LBA and size) and the volume size in the primary volume
descriptor are updated. The old copy of the file stays where it was as dead
data, and nothing else on the disc moves.

Usage (as a library):
    from iso_build import build_iso
    build_iso(src_iso, dst_iso, {'OLM/O0': new_bytes, ...})
"""
import os
import shutil
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from iso_extract import SECTOR, list_files  # noqa: E402


def resolve_names(files, replacements):
    """Map the names the caller used to the names on the disc.

    ISO 9660 names for extension-less files end in a dot ("OLM/O0."); accept both.
    """
    by_plain = {p.rstrip('.'): p for p, _, _ in files}
    out = {}
    for path, data in replacements.items():
        real = by_plain.get(path.rstrip('.'))
        if real is None:
            raise SystemExit(f'{path} is not on the disc (names look like OLM/O0 or SLPS_251.92)')
        out[real] = data
    return out


def build_iso(src, dst, replacements, in_place=()):
    """in_place: names of files to overwrite at their current position instead of appending.

    The executable must be written in place: the game hangs on "New Game" when
    SLPS_251.92 is moved (found in the font test, see docs/LOG.md). A file can go
    in place if it fits in the sectors it already occupies.
    """
    recs = {}
    _, total_sectors, files = list_files(src, recs)
    replacements = resolve_names(files, replacements)
    stay = set(resolve_names(files, {p: b'' for p in in_place}))
    where = {p: (lba, size) for p, lba, size in files}
    if os.path.getsize(src) != total_sectors * SECTOR:
        raise SystemExit('Image size does not match the volume size in its descriptor; refusing to edit')
    shutil.copyfile(src, dst)
    lba = total_sectors
    with open(dst, 'r+b') as f:
        for path, data in replacements.items():
            rec = recs[path]
            if path in stay:
                old_lba, old_size = where[path]
                slot = -(-old_size // SECTOR) * SECTOR
                if len(data) > slot:
                    raise SystemExit(f'{path} ({len(data)} bytes) does not fit in place ({slot} bytes)')
                f.seek(old_lba * SECTOR)
                f.write(data)
                f.write(b'\0' * (slot - len(data)))
                f.seek(rec + 10)  # only the length can change
                f.write(struct.pack('<I', len(data)) + struct.pack('>I', len(data)))
                continue
            f.seek(lba * SECTOR)
            f.write(data)
            f.write(b'\0' * (-len(data) % SECTOR))
            f.seek(rec + 2)   # extent LBA: little-endian then big-endian copy
            f.write(struct.pack('<I', lba) + struct.pack('>I', lba))
            f.seek(rec + 10)  # data length: little-endian then big-endian copy
            f.write(struct.pack('<I', len(data)) + struct.pack('>I', len(data)))
            lba += -(-len(data) // SECTOR)
        f.seek(16 * SECTOR + 80)  # primary volume descriptor: volume space size
        f.write(struct.pack('<I', lba) + struct.pack('>I', lba))
    return lba


def check_iso(src, dst, replacements):
    """Re-read dst and check the replaced files, and that nothing else moved."""
    _, s_total, s_files = list_files(src)
    _, d_total, d_files = list_files(dst)
    s = {p: (lba, size) for p, lba, size in s_files}
    d = {p: (lba, size) for p, lba, size in d_files}
    replacements = resolve_names(s_files, replacements)
    problems = []
    if os.path.getsize(dst) != d_total * SECTOR:
        problems.append('image size != volume size')
    if set(s) != set(d):
        problems.append('file list changed')
    with open(dst, 'rb') as f:
        for p in s:
            if p in replacements:
                lba, size = d[p]
                f.seek(lba * SECTOR)
                if size != len(replacements[p]) or f.read(size) != replacements[p]:
                    problems.append(f'{p}: contents differ from what we wrote')
            elif s[p] != d[p]:
                problems.append(f'{p}: moved or resized')
    return problems, s_total, d_total
