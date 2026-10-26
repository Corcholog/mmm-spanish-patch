"""Patches to SLPS_251.92 (the executable). See docs/KNOWLEDGE.md 4.5 and 4.6.

Everything here is derived from the game's own symbol table (tools/elf_symbols.py)
and from comparing with the English patch.

Font: one big table of 24x24, 4-bit glyphs (288 bytes each) starting at RAM FONT_BASE.
Half-width (ASCII) characters use entries HALF_BASE + cell:
    cell 0-9 = '0'-'9', 10-35 = 'A'-'Z', 36-61 = 'a'-'z',
    cell 62+i = haff_opt[i]  (the list of allowed half-width symbols; anything else is dropped)
"""
import struct

SEG0_OFF, SEG0_ADDR = 0x180, 0x100000


def ram_to_off(ram):
    return ram - SEG0_ADDR + SEG0_OFF


FONT_BASE = 0x1AE3B0          # RAM address of font entry 0 (from kanjiRomAdrOriginal)
CELL = 288                    # bytes per glyph (24 x 24 pixels, 4 bits per pixel)
HALF_BASE = 3776              # font entry of half-width cell 0 (digit '0')
HAFF_FIRST_CELL = 62          # haff_opt[0] -> cell 62


def cell_off(cell):
    """File offset of half-width cell `cell` (0 = '0')."""
    return ram_to_off(FONT_BASE + (HALF_BASE + cell) * CELL)


# The two instructions in kanjiRomAdrOriginal that load the address of haff_opt
# ("addiu reg, $gp, -32728"). Replaced by "lui reg, hi" pointing at the new list.
HAFF_LOADS = {0x13BBF8: (0x27828028, 2), 0x13BC38: (0x27848028, 4)}   # RAM: (original word, register)
HAFF_ORIGINAL = b"?!'\"() "   # 7 symbols in the original game (haff_opt is only 8 bytes)

# Data word at RAM 0x1999DC = start of the heap (the ELF even has a section called "heap"
# at 0x560D00). Must be above every overlay end and above segment 9.
HEAP_WORD = 0x1999DC
HEAP_ORIGINAL = 0x560D00

# Half-width advance: "addiu $v0,$v0,12" in the layout routine; English uses 13.
ADVANCE_OFF = 0x2A794

# Program header 9 is an empty dummy in the original; we use it (like the English patch)
# to load extra data at SEG9_ADDR. Its file bytes go into the .line debug section, which
# is never loaded at runtime.
PH9 = 0x34 + 9 * 32
SEG9_FILE_OFF = 0x618EC0
SEG9_ADDR = 0x5C0000


def u32(d, o):
    return struct.unpack_from('<I', d, o)[0]


def set_segment9(exe, data):
    """Load `data` at RAM SEG9_ADDR. Returns nothing; modifies exe (bytearray)."""
    assert u32(exe, PH9) == 1, 'program header 9 is not a LOAD segment'
    exe[SEG9_FILE_OFF:SEG9_FILE_OFF + len(data)] = data
    struct.pack_into('<5I', exe, PH9 + 4, SEG9_FILE_OFF, SEG9_ADDR, SEG9_ADDR, len(data), len(data))


def set_haff_list(exe, chars, seg9_offset=0):
    """Point kanjiRomAdrOriginal at a new half-width symbol list placed in segment 9.

    The list must sit at a 64 KB-aligned RAM address, because each patched instruction
    is a single "lui". Returns the list bytes (to be placed in segment 9 at seg9_offset).
    """
    addr = SEG9_ADDR + seg9_offset
    assert addr & 0xFFFF == 0, 'the list must start at a 64 KB boundary'
    assert all(0x20 <= c < 0x7F for c in chars), 'list entries must be printable ASCII (lb is signed)'
    for ram, (orig, reg) in HAFF_LOADS.items():
        off = ram_to_off(ram)
        assert u32(exe, off) == orig, f'unexpected instruction at 0x{ram:x}'
        struct.pack_into('<I', exe, off, (0xF << 26) | (reg << 16) | (addr >> 16))   # lui reg, hi
    return bytes(chars) + b'\0'


def set_heap_start(exe, addr):
    off = ram_to_off(HEAP_WORD)
    assert u32(exe, off) in (HEAP_ORIGINAL, addr)
    struct.pack_into('<I', exe, off, addr)


def set_half_advance(exe, px=13):
    assert exe[ADVANCE_OFF] in (12, px)
    exe[ADVANCE_OFF] = px


# Card names drawn by the Indian-poker code (oscrRrnd, RAM 0x17F6CC-0x17F890): it copies
# the suit (16-byte slots: クラブの, ハートの, スペードの, ダイヤの) into a buffer, then
# sprintf(0x334010, fmt, suit, value) with fmt "%sＪ" / "%sＱ" / "%sＫ" / "%sＡ" for
# values 11-14 and "%s %d" otherwise. File offset of the first suit slot:
SUIT_OFF, SUIT_SLOT = 0x20A450, 16
# "lui a1, 0x31; addiu a1, a1, lo" pairs that load each format (RAM of the lui), in the order J Q K A number
CARD_FORMAT_LOADS = (0x17F7DC, 0x17F800, 0x17F824, 0x17F848, 0x17F86C)
# The number case passes (a2 = suit, a3 = value). To print the value first, a2 gets the value
# and a3 the suit (the second move goes into the delay slot of the jal, which was a nop).
CARD_SWAP = {0x17F874: (0x0260302D, 0x00E0302D),    # daddu a2, s3, zero -> daddu a2, a3, zero
             0x17F87C: (0x00000000, 0x0260382D)}    # nop                -> daddu a3, s3, zero


def set_card_formats(exe, formats, addr):
    """Point the five card-name formats at `formats` (J, Q, K, A, number; encoded bytes; the
    number one gets the value as its first argument, the suit as its second) stored from RAM
    `addr` on. Returns the bytes to place there."""
    blob = b''
    for ram, f in zip(CARD_FORMAT_LOADS, formats):
        a = addr + len(blob)
        off = ram_to_off(ram)
        assert u32(exe, off) >> 16 == 0x3C05 and u32(exe, off + 4) >> 16 == 0x24A5, f'unexpected code at 0x{ram:x}'
        lo = a & 0xFFFF
        hi = (a >> 16) + (1 if lo & 0x8000 else 0)
        struct.pack_into('<II', exe, off, 0x3C050000 | hi, 0x24A50000 | lo)
        blob += f + b'\0'
        blob += b'\0' * (-len(blob) % 4)
    for ram, (orig, new) in CARD_SWAP.items():
        off = ram_to_off(ram)
        assert u32(exe, off) in (orig, new), f'unexpected code at 0x{ram:x}'
        struct.pack_into('<I', exe, off, new)
    return blob


def set_suits(exe, names):
    """Replace the four suit strings (encoded bytes each, at most 15 long)."""
    for k, b in enumerate(names):
        assert len(b) < SUIT_SLOT
        o = SUIT_OFF + k * SUIT_SLOT
        exe[o:o + SUIT_SLOT] = b + b'\0' * (SUIT_SLOT - len(b))
