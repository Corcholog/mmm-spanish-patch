"""Build a Spanish ISO from the original disc and the translation/ files.

    python -I -X utf8 tools/build.py [--out build/MMM_es_pilot.iso] [--skip-hash] [--font own|english|none] [--wrap pad|newline]

Steps: verify the source ISO (SHA-1) -> lint the translations (tools/check.py) ->
patch the executable (font glyphs, half-width symbol list, heap start, advance) ->
insert the translations into OLM/O0..O7 (in place when a line fits, appended otherwise) ->
write the ISO (executable in place, scripts appended) -> check it.

Font: by default our own glyphs (tools/font_build.py, rendered from DejaVu Sans Mono: needs the
font file locally, see docs/fonts/README.md). `--font english` is the old pilot font made from
the English patch's glyphs (local only, an ISO built with it must never be published).
"""
import argparse
import os
import struct
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import charmap  # noqa: E402
import check  # noqa: E402
import exe_patch as xp  # noqa: E402
import font_build  # noqa: E402
import font_tool  # noqa: E402
import insert_script as ins  # noqa: E402
import olm  # noqa: E402
import project  # noqa: E402
import script_text as st  # noqa: E402
from iso_build import build_iso, check_iso  # noqa: E402

HEAP_START = 0x5D0000
ADVANCE = 13
# Indian-poker card names (exe_patch.set_card_formats): suits クラブ ハート スペード ダイヤ, then
# the formats for J, Q, K, A and a number (the number format gets the value first)
SUITS = ['tréboles', 'corazones', 'picas', 'diamantes']
CARD_FORMATS = ['jota de %s', 'reina de %s', 'rey de %s', 'as de %s', '%d de %s']
SEG9_SIZE = 256
CARD_FORMATS_AT = 0x40     # offset in segment 9 (the symbol list is at 0)


def patched_executable(font='own'):
    exe = bytearray(project.read_iso_file('SLPS_251.92'))
    if font == 'own':
        font_build.install_font(exe)
    elif font == 'english':
        eng = open(os.path.join(project.ENGLISH, 'SLPS_251.92'), 'rb').read()
        font_tool.install_pilot_font(exe, eng)
    seg9 = bytearray(SEG9_SIZE)
    lst = xp.set_haff_list(exe, charmap.HAFF_LIST)
    assert len(lst) <= CARD_FORMATS_AT
    seg9[:len(lst)] = lst
    cards = xp.set_card_formats(exe, [charmap.encode(f) for f in CARD_FORMATS], xp.SEG9_ADDR + CARD_FORMATS_AT)
    seg9[CARD_FORMATS_AT:CARD_FORMATS_AT + len(cards)] = cards
    assert len(seg9) == SEG9_SIZE
    xp.set_segment9(exe, bytes(seg9))
    xp.set_heap_start(exe, HEAP_START)
    xp.set_half_advance(exe, ADVANCE)
    xp.set_suits(exe, [charmap.encode(n) for n in SUITS])
    return bytes(exe)


def lint():
    return check.run([project.TRANSLATION])


GAME_START = 0x5D08     # O0: the first scene starts at 0x5D00 (F000006C 0); a debug jump goes right after it


def start_jump(spec):
    """Debug builds: where a new game should jump to. `spec` is an entry ID ("O0:2274",
    "O0:X004") or a scene ("O1:scene3", counted from 1 in file order). Returns
    (module number, offset of the instruction in that script file, description)."""
    import script_model
    name, what = spec.split(':', 1)
    module = project.SCRIPTS.index(name)
    model = script_model.build(name)
    if what.startswith('scene'):
        scenes = [e.site for e in model.events if isinstance(e, script_model.Event) and e.kind == 'scene']
        k = int(what[5:])
        return module, scenes[k - 1], f'{name} scene {k} of {len(scenes)}'
    entries = []
    for path in sorted(__import__('glob').glob(os.path.join(project.TRANSLATION, name, f'{name}_*.txt'))):
        entries.extend(check.parse(path))
    e = next((x for x in entries if x['id'] == spec), None)
    if e is None:
        raise SystemExit(f'--start: no entry {spec}')
    if ':X' in spec:
        return module, e['off'], f'{spec} (executable string)'
    lines = [l for l in model.lines if l.kind == 'line' and l.target == e['off']]
    if not lines:
        raise SystemExit(f'--start: {spec} is not a text line the game prints by itself (a menu option?)')
    return module, lines[0].site, f'{spec}: {e["ja"][:30]}'


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--out', default=os.path.join(project.BUILD, 'MMM_es_pilot.iso'))
    ap.add_argument('--skip-hash', action='store_true')
    ap.add_argument('--font', choices=['own', 'english', 'none'], default='own')
    ap.add_argument('--wrap', choices=['pad', 'newline'], default='newline',
                    help='how long lines are broken: pad = spaces up to column 47 (like the English patch), newline = real line feeds')
    ap.add_argument('--start', metavar='ID',
                    help='DEBUG build: a new game jumps straight to this line ("O0:2274") or scene ("O1:scene3"); '
                         'default output build/MMM_es_start_<ID>.iso. Never publish such an ISO')
    args = ap.parse_args()
    if args.start and args.out == ap.get_default('out'):
        args.out = os.path.join(project.BUILD, f'MMM_es_start_{args.start.replace(":", "_")}.iso')

    if not args.skip_hash:
        print('Verifying the source ISO...')
        project.verify_source_iso()
    print('Checking the translations...')
    if lint():
        raise SystemExit('Fix the errors above first (python tools/check.py shows them with file and line).')

    st.WRAP_NEWLINE = args.wrap == 'newline'
    repl = {'SLPS_251.92': patched_executable(args.font)}
    worst = 0
    for name in project.SCRIPTS:
        es = ins.read_translations(project.TRANSLATION, name)
        exe_es = ins.read_exe_translations(project.TRANSLATION, name)
        if not es and not exe_es:
            continue
        orig = project.read_iso_file('OLM/' + name)
        new, s = ins.rebuild(orig, es, st.encode_spanish, exe_es)
        repl['OLM/' + name] = new
        worst = max(worst, s['ends_at'])
        print(f"  {name}: {s['translated']} lines translated ({s['in_place']} in place, {s['moved']} appended), "
              f"{s['size']:,} bytes, ends at 0x{s['ends_at']:X}")
    if worst > HEAP_START:
        raise SystemExit(f'A script ends at 0x{worst:X}, above the heap start 0x{HEAP_START:X}')
    if args.start:
        module, site, what = start_jump(args.start)
        o0 = bytearray(repl.get('OLM/O0') or project.read_iso_file('OLM/O0'))
        assert olm.u32(o0, GAME_START - 8) == 0xF000006C, 'O0 does not start where expected'
        struct.pack_into('<4I', o0, GAME_START, 0xF0000006, module, olm.BASE + site, 0)   # OP06 jump
        repl['OLM/O0'] = bytes(o0)
        print(f'  DEBUG: a new game jumps to {what} (module {module}, 0x{site:x})')

    os.makedirs(os.path.dirname(args.out), exist_ok=True)
    build_iso(project.SRC_ISO, args.out, repl, in_place=['SLPS_251.92'])
    problems, s_total, d_total = check_iso(project.SRC_ISO, args.out, repl)
    if problems:
        raise SystemExit(f'ISO check FAILED: {problems}')
    print(f'Written: {args.out}  ({d_total} sectors, was {s_total}); changed: {", ".join(repl)}')


if __name__ == '__main__':
    main()
