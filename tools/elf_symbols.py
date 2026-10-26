"""Symbols and references in SLPS_251.92 (it ships with a full symbol table and
relocation sections from the Metrowerks CodeWarrior build).

Usage:
    python -I -X utf8 tools/elf_symbols.py <exe> dump <out.tsv>       all symbols (address, size, name)
    python -I -X utf8 tools/elf_symbols.py <exe> find <text>          symbols whose name contains text
    python -I -X utf8 tools/elf_symbols.py <exe> refs <name>          code locations that reference a symbol
    python -I -X utf8 tools/elf_symbols.py <exe> at <hex address>     which symbol contains an address

The symbol table and relocations describe the original layout; the dump goes in
work/ (untracked), since it's derived from the game binary.
"""
import bisect
import struct
import sys

REL_TYPES = {2: 'R_MIPS_32', 4: 'R_MIPS_26', 5: 'R_MIPS_HI16', 6: 'R_MIPS_LO16', 7: 'R_MIPS_GPREL16'}


class Elf:
    def __init__(self, path):
        self.d = d = open(path, 'rb').read()
        shoff, = struct.unpack_from('<I', d, 0x20)
        shentsize, shnum, shstrndx = struct.unpack_from('<HHH', d, 0x2E)
        self.secs = [struct.unpack_from('<10I', d, shoff + i * shentsize) for i in range(shnum)]
        names_off = self.secs[shstrndx][4]
        self.secnames = [self.cstr(names_off + s[0]) for s in self.secs]
        sym = next(i for i, s in enumerate(self.secs) if s[1] == 2)
        _, _, _, _, off, size, link, *_ = self.secs[sym]
        stroff = self.secs[link][4]
        self.syms = []
        for j in range(size // 16):
            st_name, value, ssize, info, other, shndx = struct.unpack_from('<IIIBBH', d, off + 16 * j)
            self.syms.append((value, ssize, self.cstr(stroff + st_name), shndx, info & 15))
        self.by_addr = sorted((v, s, n) for v, s, n, sh, t in self.syms if v and n)
        self.addrs = [x[0] for x in self.by_addr]

    def cstr(self, off):
        return self.d[off:self.d.find(b'\0', off)].decode('latin1')

    def find(self, text):
        return [(v, s, n) for v, s, n, *_ in self.syms if text in n]

    def at(self, addr):
        """The named symbol that contains addr (functions have sizes)."""
        i = bisect.bisect_right(self.addrs, addr) - 1
        while i >= 0:
            v, s, n = self.by_addr[i]
            if v <= addr < v + max(s, 1):
                return v, s, n
            if s and v + s <= addr:
                break
            i -= 1
        return None

    def refs(self, name):
        """Relocation entries that point at symbol `name`: (patched address, type)."""
        idx = [j for j, s in enumerate(self.syms) if s[2] == name]
        out = []
        for i, s in enumerate(self.secs):
            if s[1] != 9:  # SHT_REL
                continue
            target = self.secs[s[7]]  # sh_info = section the relocations apply to
            tname = self.secnames[s[7]]
            for k in range(s[5] // 8):
                r_offset, r_info = struct.unpack_from('<II', self.d, s[4] + 8 * k)
                if (r_info >> 8) in idx:
                    out.append((tname, r_offset, REL_TYPES.get(r_info & 0xFF, r_info & 0xFF)))
        return out


def main():
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    elf = Elf(sys.argv[1])
    cmd = sys.argv[2]
    if cmd == 'dump':
        with open(sys.argv[3], 'w', encoding='utf-8', newline='\n') as f:
            f.write('address\tsize\tname\n')
            for v, s, n in elf.by_addr:
                f.write(f'{v:08x}\t{s}\t{n}\n')
        print(f'{len(elf.by_addr)} symbols written')
    elif cmd == 'find':
        for v, s, n in sorted(elf.find(sys.argv[3])):
            print(f'0x{v:08x} {s:6} {n}')
    elif cmd == 'refs':
        for sec, off, typ in elf.refs(sys.argv[3]):
            where = elf.at(off) if sec == 'main' else None
            print(f'{sec:6} 0x{off:08x} {typ:15} in {where[2] if where else "?"}')
    elif cmd == 'at':
        print(elf.at(int(sys.argv[3], 16)))


if __name__ == '__main__':
    main()
