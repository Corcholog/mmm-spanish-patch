"""Batches for the translation workflow (docs/TRANSLATION_WORKFLOW.md).

    python -I -X utf8 tools/batch.py next O0 [--size 80]   -> work/batches/O0_0083-0160.md + .tsv
    python -I -X utf8 tools/batch.py check FILE.tsv         -> validate a draft without applying it
    python -I -X utf8 tools/batch.py apply FILE.tsv [--force]  -> check, then write into translation/
    python -I -X utf8 tools/batch.py status                 -> progress per script

A batch is the next run of untranslated entries of one script, extended to the end of
its narration page, with a few already-translated entries before it as context. The
.md file is what the translator reads (pages, line budgets, JA, EN); the .tsv is the
draft it fills in: one line per entry, "ID<TAB>Spanish" with an optional third column
"NOTE: ..." for doubts (stored next to the entry as a NOTE: line).
"""
import argparse
import glob
import math
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import check  # noqa: E402
import project  # noqa: E402
import script_text as st  # noqa: E402

BATCHES = os.path.join(project.ROOT, 'work', 'batches')
CONTEXT = 6     # translated entries shown before a batch
ID_RE = re.compile(r'^(O\d):(\d{4}(?:\.\d+)?|X\d{3})$')   # X: a string from the executable (<script>_exe.txt)


def entries_of(script):
    out = []
    for path in sorted(glob.glob(os.path.join(project.TRANSLATION, script, '*.txt'))):
        out.extend(check.parse(path))
    return out


def needs_translation(e):
    return bool(e['ja'].strip()) and not e['es'].strip(' ')


def ja_lines(ja):
    """Rough screen lines of the Japanese (full-width characters take 2 columns)."""
    width = sum(1 if ord(c) < 0x80 else 2 for c in st.CODE_RE.sub('', ja).replace(st.LF, ''))
    return max(1, math.ceil(width / st.LINE_WIDTH))


def kind_of(e):
    return 'narration' if '\\FS' in e['info'] else 'dialogue'


def page_end(e):
    return '\\k' in e['info'] or st.strip_page_token(e['es'])[1]


def branch_join_flags(script, entries):
    """{entry ID: [flags]} for pieces the game joins across a goto (script_model.branch_joins):
    the sentence goes on in an entry that is not the next one in the file. Empty without the ISO."""
    try:
        import script_model
        model = script_model.build(script)
    except OSError:
        return {}
    ids = {('x' if ':X' in e['id'] else 'r', e['off']): e['id'] for e in entries}

    def eid(line):
        return ids.get(('x', line.site) if line.target < 0 else ('r', line.target))

    out = {}
    for a, b in model.branch_joins():
        ia, ib = eid(a), eid(b)
        if ia and ib:
            out.setdefault(ia, []).append(f'BRANCH: the sentence goes on in {ib}, not in the next entry')
            out.setdefault(ib, []).append(f'BRANCH: continues the sentence of {ia}')
    return out


def cmd_next(args):
    if not args.no_prefill:
        n = prefill(args.script)
        if n:
            print(f'{n} entries pre-filled from identical lines already translated (NOTE: copied from ...)')
    entries = entries_of(args.script)
    start = next((i for i, e in enumerate(entries) if needs_translation(e)), None)
    if start is None:
        print(f'{args.script}: nothing left to translate')
        return
    # extend the batch to the end of the page that contains entry start+size
    end = min(start + args.size, len(entries))
    while end < len(entries) and not page_end(entries[end - 1]):
        end += 1
    batch = entries[start:end]
    first, last = batch[0]['id'].split(':')[1], batch[-1]['id'].split(':')[1]
    os.makedirs(BATCHES, exist_ok=True)
    base = os.path.join(BATCHES, f'{args.script}_{first}-{last}')
    lines = [f'# Batch {args.script} {first}–{last} ({len(batch)} entries)\n',
             'Fill in the .tsv next to this file: one line per entry, `ID<TAB>Spanish`, optional 3rd column '
             '`NOTE: ...`. Rules: docs/TRANSLATION_WORKFLOW.md. Check with `python -I -X utf8 tools/batch.py check <tsv>`.\n']
    ctx = [e for e in entries[max(0, start - CONTEXT):start] if e['es'].strip(' ')]
    if ctx:
        lines.append('\n## Context (already translated, do not change)\n')
        for e in ctx:
            lines.append(f'- {e["id"]}: {e["es"]}\n')
    joins = branch_join_flags(args.script, entries)
    page, page_no = [], 0
    for e in batch:
        page.append(e)
        if page_end(e) or e is batch[-1]:
            page_no += 1
            kind = kind_of(page[0])
            if kind == 'narration':
                budget = st.NARRATION_PAGE_LINES
                jl = sum(ja_lines(x['ja']) for x in page if x['ja'])
                lines.append(f'\n## Page {page_no} · narration · {len(page)} entries · budget {budget} lines '
                             f'in total (the Japanese uses about {jl})\n')
            else:
                lines.append(f'\n## Page {page_no} · dialogue · budget {st.DIALOGUE_PAGE_LINES} lines\n')
            for x in page:
                flags = []
                if not x['ja'].strip():
                    flags.append('no text: leave empty')
                if '.' in x['id'].split(':')[1]:
                    flags.append('continues the previous entry (same sentence)')
                if x['info'].rstrip().endswith('\\FE\\t60⏎') and kind == 'narration':
                    flags.append('<PAGE> allowed')
                flags.extend(joins.get(x['id'], []))
                codes = st.codes_in(x['ja'])
                if codes:
                    flags.append('keep codes: ' + ' '.join(codes))
                lines.append(f'\n**{x["id"]}**' + (f'  _({"; ".join(flags)})_' if flags else '') + '\n')
                lines.append(f'- JA: {x["ja"]}\n')
                if x['en']:
                    lines.append(f'- EN: {x["en"]}\n')
                if x['es'].strip(' '):      # pre-filled from an identical line: context, not in the .tsv
                    lines.append(f'- ES (already translated, do not change): {x["es"]}\n')
            page = []
    with open(base + '.md', 'w', encoding='utf-8', newline='\n') as f:
        f.writelines(lines)
    with open(base + '.tsv', 'w', encoding='utf-8', newline='\n') as f:
        for e in batch:
            if needs_translation(e):
                f.write(f'{e["id"]}\t\n')
    print(f'{base}.md\n{base}.tsv\n{len(batch)} entries, {page_no} pages')


def read_tsv(path):
    rows = {}
    with open(path, encoding='utf-8') as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip('\n')
            if not line.strip() or line.startswith('#'):
                continue
            cols = line.split('\t')
            if not ID_RE.match(cols[0].strip()):
                raise SystemExit(f'{path}:{n}: first column must be an entry ID like O0:0083, got {cols[0]!r}')
            text = cols[1].strip() if len(cols) > 1 else ''
            note = cols[2].strip() if len(cols) > 2 else ''
            if note.startswith('NOTE:'):
                note = note[5:].strip()
            rows[cols[0].strip()] = (text, note)
    return rows


def validate(rows):
    """Errors for a draft: per entry, and for every page it touches. Returns (errors, entries)."""
    scripts = {r.split(':')[0] for r in rows}
    if len(scripts) != 1:
        raise SystemExit('a draft must cover one script')
    script = scripts.pop()
    entries = entries_of(script)
    by_id = {e['id']: e for e in entries}
    errors = []
    for rid, (text, _) in rows.items():
        if rid not in by_id:
            errors.append(f'{rid}: no such entry')
            continue
        if text:
            by_id[rid]['es'] = text
            found = check.check_entry(by_id[rid])
            errors += [f'{rid}: {m}' for m in found]
            if found:                    # a line the tools can't encode must not reach the screen simulation
                by_id[rid]['es'] = ''
                continue
            orphan = check.orphan(by_id[rid])
            if orphan:
                errors.append(f'warning {rid}: {orphan}')
        elif needs_translation(by_id[rid]):
            errors.append(f'{rid}: empty translation')
    msgs = check.screen_lint(script, entries, only=set(rows))
    if msgs is not None:                 # the screens exactly as the build lays them out
        for level, e, m in msgs:
            text = f'{e["id"] if e else script}: {m}'
            errors.append(text if level == 'error' else 'warning ' + text)
        return errors, script
    for kind, page, n in check.pages(entries):   # fallback without the source ISO
        if not any(e['id'] in rows for e in page):
            continue
        limit = st.NARRATION_PAGE_LINES if kind == 'narration' else st.DIALOGUE_PAGE_LINES
        if n > limit:
            msg = f'{page[0]["id"]}..{page[-1]["id"]}: {kind} page needs {n} lines, budget {limit}'
            errors.append(msg if kind == 'narration' else 'warning ' + msg)
    return errors, script


def cmd_check(args):
    rows = read_tsv(args.tsv)
    errors, _ = validate(rows)
    real = [e for e in errors if not e.startswith('warning')]
    for e in errors:
        print(('  ' if e.startswith('warning') else 'ERROR ') + e)
    print(f'{len(rows)} lines checked: {len(real)} error(s), {len(errors) - len(real)} warning(s)')
    sys.exit(1 if real else 0)


def cmd_apply(args):
    rows = read_tsv(args.tsv)
    errors, script = validate(rows)
    real = [e for e in errors if not e.startswith('warning')]
    if real:
        for e in real:
            print('ERROR ' + e)
        raise SystemExit('not applied: fix the errors first')
    done = write_rows(script, rows, args.force)
    print(f'{done} entries written to translation/{script}/')


def write_rows(script, rows, force=False):
    """Write {ID: (Spanish, note)} into translation/<script>/. Returns the number written."""
    done = 0
    for path in sorted(glob.glob(os.path.join(project.TRANSLATION, script, '*.txt'))):
        lines = open(path, encoding='utf-8').read().split('\n')
        out, cur, changed = [], None, False
        i = 0
        while i < len(lines):
            line = lines[i]
            m = check.ENTRY_RE.match(line)
            if m:
                cur = m.group(1)
            if line.startswith('ES:') and cur in rows:
                text, note = rows[cur]
                copied = i + 1 < len(lines) and lines[i + 1].startswith('NOTE: copied from ')
                if line[3:].strip(' ') and not force and not copied:   # a pre-filled copy may be corrected
                    raise SystemExit(f'{cur} already has Spanish; use --force to replace it')
                out.append('ES: ' + text)
                if i + 1 < len(lines) and lines[i + 1].startswith('NOTE:'):
                    i += 1                      # replace an old note
                if note:
                    out.append('NOTE: ' + note)
                changed = True
                done += 1
            else:
                out.append(line)
            i += 1
        if changed:
            open(path, 'w', encoding='utf-8', newline='\n').write('\n'.join(out))
    return done


SHORT_LINE = 4     # spoken text this short ("うん", "だから！") means different things in different places


def too_short_to_copy(ja):
    """True for lines like 恭介「うん」 whose meaning depends on the context (O1 2291, 2295)."""
    text = st.CODE_RE.sub('', ja).replace(st.LF, '')
    if '「' in text:
        text = text.split('「', 1)[1].rstrip('」')
    return len(text.strip('…。、！？!? 　')) <= SHORT_LINE


def prefill(script):
    """Copy existing Spanish into untranslated entries of `script` whose Japanese (and codes
    around it) are identical to an entry already translated, in any script (earlier scripts
    first, then file order). Each copy gets a NOTE naming its source. Copies that would break
    a screen are left for the translator. Returns the number written."""
    pool = {}
    for s in project.SCRIPTS:
        for e in entries_of(s):
            if e['es'].strip(' ') and e['ja'].strip():
                pool.setdefault((e['ja'], e['info']), e)
    rows = {}
    for e in entries_of(script):
        src = pool.get((e['ja'], e['info']))
        if needs_translation(e) and src and not too_short_to_copy(e['ja']):
            rows[e['id']] = (src['es'], f'copied from {src["id"]} (same Japanese)')
    for _ in range(5):                      # drop the copies that the checks reject
        if not rows:
            return 0
        errors, _ = validate(rows)
        bad = {m.split(':', 2)[0] + ':' + m.split(':', 2)[1] for m in errors if not m.startswith('warning')}
        if not bad & set(rows):
            break
        for rid in bad & set(rows):
            del rows[rid]
    return write_rows(script, rows)


def cmd_prefill(args):
    n = prefill(args.script)
    print(f'{args.script}: {n} entries pre-filled from identical Japanese lines already translated')


def cmd_status(args):
    total = done = 0
    for script in project.SCRIPTS:
        entries = [e for e in entries_of(script) if e['ja'].strip()]
        n = sum(1 for e in entries if e['es'].strip(' '))
        notes = 0
        for path in glob.glob(os.path.join(project.TRANSLATION, script, '*.txt')):
            notes += open(path, encoding='utf-8').read().count('\nNOTE:')
        total += len(entries)
        done += n
        print(f'{script}: {n:5}/{len(entries):5} ({100 * n / max(len(entries), 1):5.1f}%)  notes: {notes}')
    print(f'all: {done}/{total} ({100 * done / max(total, 1):.1f}%)')


def main():
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('next')
    p.add_argument('script')
    p.add_argument('--size', type=int, default=80)
    p.add_argument('--no-prefill', action='store_true', help="don't copy Spanish into identical lines first")
    p = sub.add_parser('prefill')
    p.add_argument('script')
    p = sub.add_parser('check')
    p.add_argument('tsv')
    p = sub.add_parser('apply')
    p.add_argument('tsv')
    p.add_argument('--force', action='store_true')
    sub.add_parser('status')
    args = ap.parse_args()
    {'next': cmd_next, 'prefill': cmd_prefill, 'check': cmd_check, 'apply': cmd_apply,
     'status': cmd_status}[args.cmd](args)


if __name__ == '__main__':
    main()
