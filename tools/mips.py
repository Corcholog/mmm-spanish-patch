"""Tiny MIPS (PS2 R5900) disassembler for reading small routines in SLPS_251.92.

Covers the common integer instructions only; anything else prints as .word.
RAM address of file offset `off` in the executable = 0x100000 + (off - 0x180)
(from the ELF program header: segment 0 maps file offset 0x180 to 0x100000).

Usage:
    python -I -X utf8 tools/mips.py <SLPS_251.92> <start RAM address, hex> [count words]
    python -I -X utf8 tools/mips.py <SLPS_251.92> --off <file offset, hex> [count words]
"""
import struct
import sys

SEG0_OFF, SEG0_ADDR = 0x180, 0x100000

REG = ['zero', 'at', 'v0', 'v1', 'a0', 'a1', 'a2', 'a3', 't0', 't1', 't2', 't3', 't4', 't5', 't6', 't7',
       's0', 's1', 's2', 's3', 's4', 's5', 's6', 's7', 't8', 't9', 'k0', 'k1', 'gp', 'sp', 'fp', 'ra']


def r(n):
    return '$' + REG[n]


def s16(x):
    return x - 0x10000 if x & 0x8000 else x


def disasm(w, pc):
    op = w >> 26
    rs, rt, rd = (w >> 21) & 31, (w >> 16) & 31, (w >> 11) & 31
    sh, fn, imm = (w >> 6) & 31, w & 63, w & 0xFFFF
    if w == 0:
        return 'nop'
    if op == 0:
        rtype = {0x21: 'addu', 0x23: 'subu', 0x24: 'and', 0x25: 'or', 0x26: 'xor', 0x27: 'nor',
                 0x2A: 'slt', 0x2B: 'sltu', 0x2D: 'daddu', 0x2F: 'dsubu', 0x0A: 'movz', 0x0B: 'movn',
                 0x04: 'sllv', 0x06: 'srlv', 0x07: 'srav'}
        if fn in rtype:
            if fn in (4, 6, 7):
                return f'{rtype[fn]} {r(rd)}, {r(rt)}, {r(rs)}'
            if fn == 0x25 and rt == 0:
                return f'move {r(rd)}, {r(rs)}'
            return f'{rtype[fn]} {r(rd)}, {r(rs)}, {r(rt)}'
        if fn == 0:
            return f'sll {r(rd)}, {r(rt)}, {sh}'
        if fn == 2:
            return f'srl {r(rd)}, {r(rt)}, {sh}'
        if fn == 3:
            return f'sra {r(rd)}, {r(rt)}, {sh}'
        if fn == 8:
            return f'jr {r(rs)}'
        if fn == 9:
            return f'jalr {r(rd)}, {r(rs)}'
        if fn == 0x10:
            return f'mfhi {r(rd)}'
        if fn == 0x12:
            return f'mflo {r(rd)}'
        if fn in (0x18, 0x19, 0x1A, 0x1B):
            return f'{["mult", "multu", "div", "divu"][fn - 0x18]} {r(rs)}, {r(rt)}'
        if fn == 0x0C:
            return 'syscall'
    tgt = pc + 4 + (s16(imm) << 2)
    if op == 1:
        return f'{["bltz", "bgez"][rt & 1]} {r(rs)}, 0x{tgt:x}' if rt in (0, 1) else f'.word 0x{w:08x}'
    if op == 2:
        return f'j 0x{((pc + 4) & 0xF0000000) | ((w & 0x3FFFFFF) << 2):x}'
    if op == 3:
        return f'jal 0x{((pc + 4) & 0xF0000000) | ((w & 0x3FFFFFF) << 2):x}'
    branch = {4: 'beq', 5: 'bne', 0x14: 'beql', 0x15: 'bnel'}
    if op in branch:
        return f'{branch[op]} {r(rs)}, {r(rt)}, 0x{tgt:x}'
    if op in (6, 7, 0x16, 0x17):
        return f'{ {6: "blez", 7: "bgtz", 0x16: "blezl", 0x17: "bgtzl"}[op] } {r(rs)}, 0x{tgt:x}'
    arith = {9: 'addiu', 0x19: 'daddiu', 0xA: 'slti', 0xB: 'sltiu'}
    if op in arith:
        return f'{arith[op]} {r(rt)}, {r(rs)}, {s16(imm)}'
    logic = {0xC: 'andi', 0xD: 'ori', 0xE: 'xori'}
    if op in logic:
        return f'{logic[op]} {r(rt)}, {r(rs)}, 0x{imm:x}'
    if op == 0xF:
        return f'lui {r(rt)}, 0x{imm:x}'
    mem = {0x20: 'lb', 0x21: 'lh', 0x23: 'lw', 0x24: 'lbu', 0x25: 'lhu', 0x27: 'lwu', 0x28: 'sb', 0x29: 'sh',
           0x2B: 'sw', 0x37: 'ld', 0x3F: 'sd', 0x1E: 'lq', 0x1F: 'sq'}
    if op in mem:
        return f'{mem[op]} {r(rt)}, {s16(imm)}({r(rs)})'
    return f'.word 0x{w:08x}'


def dump(data, addr, count):
    for i in range(count):
        a = addr + 4 * i
        off = a - SEG0_ADDR + SEG0_OFF
        w, = struct.unpack_from('<I', data, off)
        print(f'  {a:08x} ({off:06x}): {w:08x}  {disasm(w, a)}')


if __name__ == '__main__':
    if len(sys.argv) < 3:
        raise SystemExit(__doc__)
    data = open(sys.argv[1], 'rb').read()
    if sys.argv[2] == '--off':
        a = int(sys.argv[3], 16) - SEG0_OFF + SEG0_ADDR
        n = int(sys.argv[4]) if len(sys.argv) > 4 else 32
    else:
        a = int(sys.argv[2], 16)
        n = int(sys.argv[3]) if len(sys.argv) > 3 else 32
    dump(data, a, n)
