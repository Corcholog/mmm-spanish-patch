"""Put the current translation into a PCSX2 save state (.p2s), so an old state can be
reused to test new text without replaying the game.

    python -I -X utf8 tools/savestate.py info    <state.p2s>
    python -I -X utf8 tools/savestate.py refresh <state.p2s> [--out <new.p2s>] [--wrap pad|newline]

A .p2s file is a zip (zstd-compressed members) holding the PS2's memory: eeMemory.bin is
the 32 MB main RAM. The script file the game is running sits in RAM at 0x4D3600, and its
bytecode is at the same offsets in every build (only text moves), so replacing that copy
with the freshly built script keeps the game's position valid: the next lines read the new
text. (The box on screen when the state was saved still shows the old text until you
advance.) "refresh" also writes our font cells and the half-width symbol list into RAM.

Limits: the state must be from a Spanish build of ours (same executable patches); route
flags and everything else stay as saved. Never share states: they contain the game.
"""
import argparse
import os
import struct
import sys
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exe_patch as xp  # noqa: E402
import insert_script as ins  # noqa: E402
import olm  # noqa: E402
import project  # noqa: E402
import script_text as st  # noqa: E402

RAM = 'eeMemory.bin'
OVERLAY = olm.BASE                   # 0x4D3600
OVERLAY_END = project.OVERLAY_LIMIT  # 0x5C0000: segment 9 starts here
FONT_CELLS = 95                      # half-width cells 0-94


def loaded_script(ee):
    """Name of the script file in RAM (the one whose bytecode opcodes all match), or None."""
    best = (0, None)
    for name in project.SCRIPTS:
        d = project.read_iso_file('OLM/' + name)
        ops = [o for o in range(olm.HDR, len(d) - 3, 4) if olm.u32(d, o) >> 8 == 0xF00000]
        same = sum(1 for o in ops if ee[OVERLAY + o:OVERLAY + o + 4] == d[o:o + 4])
        best = max(best, (same / max(len(ops), 1), name))
    return best[1] if best[0] > 0.99 else None


def read_state(path):
    with zipfile.ZipFile(path) as z:
        return [(i, z.read(i.filename)) for i in z.infolist()]


def write_state(path, members):
    with zipfile.ZipFile(path, 'w') as z:
        for info, data in members:
            z.writestr(info, data, compress_type=info.compress_type)


def refresh(src, out):
    members = read_state(src)
    ee = bytearray(next(data for info, data in members if info.filename == RAM))
    name = loaded_script(ee)
    if name is None:
        raise SystemExit('no known script file in RAM at 0x4D3600 (is this a My Merry May state?)')
    orig = project.read_iso_file('OLM/' + name)
    new, s = ins.rebuild(orig, ins.read_translations(project.TRANSLATION, name), st.encode_spanish,
                         ins.read_exe_translations(project.TRANSLATION, name))
    old_end = OVERLAY + olm.u32(ee, OVERLAY + 0x10) + olm.HDR
    ee[OVERLAY:max(old_end, OVERLAY + len(new))] = b'\0' * (max(old_end, OVERLAY + len(new)) - OVERLAY)
    ee[OVERLAY:OVERLAY + len(new)] = new
    # our font and symbol list, from the executable the build makes
    import build
    exe = build.patched_executable('own')
    lo = xp.cell_off(0)
    hi = xp.cell_off(FONT_CELLS)
    ram_lo = xp.FONT_BASE + xp.HALF_BASE * xp.CELL
    ee[ram_lo:ram_lo + (hi - lo)] = exe[lo:hi]
    seg9 = exe[xp.SEG9_FILE_OFF:xp.SEG9_FILE_OFF + build.SEG9_SIZE]
    ee[xp.SEG9_ADDR:xp.SEG9_ADDR + len(seg9)] = seg9
    struct.pack_into('<I', ee, xp.HEAP_WORD, build.HEAP_START)
    # card names: the suit slots and the patched code of oscrRrnd
    suit_ram = xp.SUIT_OFF - xp.SEG0_OFF + xp.SEG0_ADDR
    ee[suit_ram:suit_ram + 4 * xp.SUIT_SLOT] = exe[xp.SUIT_OFF:xp.SUIT_OFF + 4 * xp.SUIT_SLOT]
    for ram in list(xp.CARD_FORMAT_LOADS) + [r + 4 for r in xp.CARD_FORMAT_LOADS] + list(xp.CARD_SWAP):
        ee[ram:ram + 4] = exe[xp.ram_to_off(ram):xp.ram_to_off(ram) + 4]
    members = [(info, bytes(ee) if info.filename == RAM else data) for info, data in members]
    write_state(out, members)
    print(f'{out}: {name} refreshed ({s["translated"]} translated lines, {len(new):,} bytes); '
          f'advance one line to see the new text')


def info(path):
    members = read_state(path)
    ee = next(data for i, data in members if i.filename == RAM)
    version = next(data for i, data in members if i.filename.endswith('Version.id'))
    print(f'{path}: PCSX2 {version[4:10].decode("ascii", "replace")}, script in RAM: {loaded_script(ee)}')


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('cmd', choices=['info', 'refresh'])
    ap.add_argument('state')
    ap.add_argument('--out')
    ap.add_argument('--wrap', choices=['pad', 'newline'], default='newline')
    args = ap.parse_args()
    st.WRAP_NEWLINE = args.wrap == 'newline'
    if args.cmd == 'info':
        info(args.state)
    else:
        base = os.path.splitext(os.path.basename(args.state))[0]
        refresh(args.state, args.out or os.path.join(project.BUILD, f'{base}_refreshed.p2s'))


if __name__ == '__main__':
    main()
