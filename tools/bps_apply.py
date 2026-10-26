"""Apply a BPS patch (byuu/near's format) and verify all three checksums.

Usage:
    python tools/bps_apply.py <patch.bps> <source> <output>

The source file is never modified. The BPS format stores the source size,
target size, a list of actions, and CRC32 checksums of source, target and the
patch itself.
"""
import mmap
import sys
import zlib


class Reader:
    def __init__(self, data):
        self.data = data
        self.pos = 0

    def byte(self):
        b = self.data[self.pos]
        self.pos += 1
        return b

    def number(self):
        value, shift = 0, 1
        while True:
            x = self.byte()
            value += (x & 0x7F) * shift
            if x & 0x80:
                return value
            shift <<= 7
            value += shift


def apply_bps(patch_path, source_path, out_path):
    with open(patch_path, 'rb') as f:
        patch = f.read()
    if patch[:4] != b'BPS1':
        raise SystemExit('Not a BPS patch')
    src_crc, tgt_crc, patch_crc = (int.from_bytes(patch[-12:-8], 'little'),
                                   int.from_bytes(patch[-8:-4], 'little'),
                                   int.from_bytes(patch[-4:], 'little'))
    if zlib.crc32(patch[:-4]) != patch_crc:
        raise SystemExit('Patch file is corrupt (its own CRC32 does not match)')

    r = Reader(patch)
    r.pos = 4
    source_size, target_size, meta_size = r.number(), r.number(), r.number()
    r.pos += meta_size
    end = len(patch) - 12

    with open(source_path, 'rb') as sf:
        source = mmap.mmap(sf.fileno(), 0, access=mmap.ACCESS_READ)
        if len(source) != source_size:
            raise SystemExit(f'Source size {len(source)} != expected {source_size}')
        print('Checking source CRC32 ...')
        crc = 0
        for i in range(0, len(source), 64 * 1024 * 1024):
            crc = zlib.crc32(source[i:i + 64 * 1024 * 1024], crc)
        if crc != src_crc:
            raise SystemExit(f'Source CRC32 {crc:08X} != expected {src_crc:08X}')

        target = bytearray(target_size)
        out = 0
        src_rel = tgt_rel = 0
        while r.pos < end:
            data = r.number()
            cmd, length = data & 3, (data >> 2) + 1
            if cmd == 0:  # SourceRead: same offset in source
                target[out:out + length] = source[out:out + length]
            elif cmd == 1:  # TargetRead: literal bytes from the patch
                target[out:out + length] = patch[r.pos:r.pos + length]
                r.pos += length
            elif cmd == 2:  # SourceCopy: relative offset into source
                d = r.number()
                src_rel += -(d >> 1) if d & 1 else d >> 1
                target[out:out + length] = source[src_rel:src_rel + length]
                src_rel += length
            else:  # TargetCopy: relative offset into already-written output
                d = r.number()
                tgt_rel += -(d >> 1) if d & 1 else d >> 1
                if tgt_rel + length <= out:
                    target[out:out + length] = target[tgt_rel:tgt_rel + length]
                else:  # overlapping copy repeats bytes, so go one at a time
                    for i in range(length):
                        target[out + i] = target[tgt_rel + i]
                tgt_rel += length
            out += length
        source.close()

    if out != target_size:
        raise SystemExit(f'Wrote {out} bytes, expected {target_size}')
    crc = zlib.crc32(target)
    if crc != tgt_crc:
        raise SystemExit(f'Output CRC32 {crc:08X} != expected {tgt_crc:08X}')
    with open(out_path, 'wb') as f:
        f.write(target)
    print(f'OK: wrote {out_path} ({target_size} bytes, CRC32 {crc:08X})')


if __name__ == '__main__':
    if len(sys.argv) != 4:
        raise SystemExit(__doc__)
    apply_bps(*sys.argv[1:4])
