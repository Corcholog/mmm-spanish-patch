"""Tests for dump_script.py + insert_script.py. Writes only under work/pipeline_test/.

    python -I -X utf8 tools/test_pipeline.py

1. Empty Spanish        -> insert must give byte-identical script files.
2. ES = the Japanese    -> full parse/encode/place path; must be byte-identical.
3. ES = the English     -> a realistic load: accents/wrap/in-place/move. Checks that
   every pointer leads to the expected text and every file fits in memory.
4. Pointer forms        -> every pointer-like word has a known kind (olm.site_kind); jumps
   land on a scene start (F000006C) in some script file.
5. Non-text words       -> after the English load and after the real translation, no word
   outside the text changes except real text references (a jump or a coordinate never moves).
"""
import bisect
import os
import re
import shutil
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import dump_script  # noqa: E402
import insert_script as ins  # noqa: E402
import olm  # noqa: E402
import project  # noqa: E402
import script_text as st  # noqa: E402

BASE = os.path.join(project.ROOT, 'work', 'pipeline_test')
EXPECTED_KINDS = {
    'O0': {'text': 5902, 'menu': 31, 'jump': 5},
    'O1': {'text': 6550, 'menu': 41, 'jump': 4},
    'O2': {'text': 4698, 'menu': 12, 'rect': 22, 'jump': 8},
    'O3': {'text': 4300, 'menu': 16, 'rect': 34, 'jump': 1},
    'O4': {'text': 3699, 'menu': 4, 'title': 1, 'jump': 3},
    'O5': {'text': 3722, 'menu': 6, 'rect': 25, 'title': 1},
    'O6': {'text': 2218, 'menu': 4, 'arg': 1, 'title': 1},
    'O7': {'text': 1259, 'credits': 709, 'jump': 3, 'data': 5},
}


def nontext_changes(orig, new):
    """Offsets of aligned words outside the text slots that differ, other than text references."""
    records, _ = olm.analyze(orig)
    starts = sorted(records)
    cap = {t: olm.slot_capacity(orig, t, records[t]) for t in starts}
    sites = {o for o, _ in olm.text_sites(orig)}
    out = []
    for o in range(olm.HDR, len(orig) - 3, 4):
        i = bisect.bisect_right(starts, o) - 1
        if o in sites or (i >= 0 and o < starts[i] + cap[starts[i]]):
            continue
        if olm.u32(orig, o) != olm.u32(new, o):
            out.append(o)
    return out


def fill(src, dst, field):
    """Copy translation files, setting ES to the JA or EN text."""
    for name in project.SCRIPTS:
        os.makedirs(os.path.join(dst, name), exist_ok=True)
        for fn in os.listdir(os.path.join(src, name)):
            lines = open(os.path.join(src, name, fn), encoding='utf-8').read().split('\n')
            out, keep = [], ''
            for line in lines:
                if line.startswith(field + ':'):
                    keep = line[len(field) + 2:]
                if line.startswith('ES:'):
                    line = 'ES: ' + keep
                out.append(line)
            open(os.path.join(dst, name, fn), 'w', encoding='utf-8', newline='\n').write('\n'.join(out))


def main():
    shutil.rmtree(BASE, ignore_errors=True)
    dumped = os.path.join(BASE, 'dump')
    for name in project.SCRIPTS:
        dump_script.dump(name, dumped, force=True)
    ok = True

    print('Test 1: empty Spanish')
    for name in project.SCRIPTS:
        orig = project.read_iso_file('OLM/' + name)
        new, s = ins.rebuild(orig, ins.read_translations(dumped, name), st.encode_spanish)
        same = new == orig
        ok &= same
        print(f'  {name}: {"identical" if same else "DIFFERENT"}')

    print('Test 2: ES = Japanese (identity encoding)')
    ja = os.path.join(BASE, 'ja')
    fill(dumped, ja, 'JA')
    for name in project.SCRIPTS:
        orig = project.read_iso_file('OLM/' + name)
        es = ins.read_translations(ja, name)
        new, s = ins.rebuild(orig, es, st.encode_identity)
        same = new == orig
        ok &= same
        print(f'  {name}: {len(es)} entries through the full path -> {"identical" if same else "DIFFERENT"}')

    print('Test 3: ES = English (realistic size and wrapping)')
    en = os.path.join(BASE, 'en')
    fill(dumped, en, 'EN')
    for name in project.SCRIPTS:
        orig = project.read_iso_file('OLM/' + name)
        es = ins.read_translations(en, name)
        bad = {}
        for p, text in es.items():          # drop entries the font can't show (reported)
            try:
                st.encode_spanish([text])
            except ValueError as e:
                bad[p] = str(e)
        for p in bad:
            del es[p]
        new, s = ins.rebuild(orig, es, st.encode_spanish)
        # every pointer must lead to text that is either unchanged or the encoded English
        recs, sites = olm.record_parts(orig)
        problems = 0
        for o, t in sites:
            nt = olm.u32(new, o) - olm.BASE
            got = olm.text_at(new, nt)
            if t in es:
                # wrapping padding differs when the parts of a record are wrapped together,
                # so compare with runs of spaces collapsed
                # (and when consecutive records are wrapped as one chain, spaces move between them)
                want = re.sub(rb'\s+', b'', st.encode_spanish([es[t]])[0])
                if want not in re.sub(rb'\s+', b'', got):
                    problems += 1
            elif got != olm.text_at(orig, t) and not any(p in es for r in recs if r[0] <= t < r[0] + r[1] + 1 for p in r[2]):
                problems += 1
        fits = s['ends_at'] <= project.OVERLAY_LIMIT
        ok &= problems == 0 and fits
        print(f"  {name}: {s['in_place']} in place, {s['moved']} moved, {len(bad)} skipped (unsupported chars), "
              f"{s['size']:,} bytes, {'fits' if fits else 'TOO BIG'}, pointer problems: {problems}")
        if bad:
            print('     e.g.', list(bad.values())[:2])
        moved = nontext_changes(orig, new)
        ok &= not moved
        if moved:
            print('     NON-TEXT WORDS CHANGED:', [hex(o) for o in moved[:8]])
        with open(os.path.join(BASE, name), 'wb') as f:
            f.write(new)

    print('Test 4: pointer forms')
    files = {name: project.read_iso_file('OLM/' + name) for name in project.SCRIPTS}
    for name, d in files.items():
        kinds = {}
        for o, t, k in olm.classify(d):
            kinds[k] = kinds.get(k, 0) + 1
            if k == 'jump' and not any(t + 4 <= len(x) and olm.u32(x, t) == 0xF000006C for x in files.values()):
                print(f'  {name}: jump at 0x{o:x} does not land on a scene start')
                ok = False
        good = kinds == EXPECTED_KINDS[name]
        ok &= good
        print(f'  {name}: {kinds}' + ('' if good else f'  EXPECTED {EXPECTED_KINDS[name]}'))

    print('Test 5: real translation leaves non-text words alone')
    for name in project.SCRIPTS:
        es = ins.read_translations(project.TRANSLATION, name)
        if not es:
            continue
        orig = files[name]
        new, _ = ins.rebuild(orig, es, st.encode_spanish)
        moved = nontext_changes(orig, new)
        ok &= not moved
        print(f'  {name}: {len(es)} translated, non-text words changed: {len(moved)}')
    print('ALL PASSED' if ok else 'FAILURES')


if __name__ == '__main__':
    main()
