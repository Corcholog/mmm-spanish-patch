"""Lint the Spanish in translation/ files.

    python -I -X utf8 tools/check.py [--pages] [files or folders ...]

Per entry (errors): characters the font can't draw, the stand-in symbols used literally,
\\codes inside the Japanese that are missing/changed in the Spanish, a different number of
line breaks, a word longer than a line, <PAGE> where it isn't allowed. Warnings: orphan
last lines.
Per screen: every screen is laid out as the build ships it (tools/screens.py): overflow,
engine wraps, too many rows, blank menu options, glued words, Japanese left on a Spanish
screen. Without the source ISO it falls back to line-count estimates (--pages prints them).
Also prints how much is translated.
"""
import argparse
import glob
import os
import re
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import charmap  # noqa: E402
import project  # noqa: E402
import script_text as st  # noqa: E402

ENTRY_RE = re.compile(r'^== (O\d:(?:\d{4}(?:\.\d+)?|X\d{3}))\s+@0x([0-9a-fA-F]+)\s*(.*)$')


def parse(path):
    """Yield dicts: id, off, info (codes shown on the == line), ja, en, es, line, file."""
    cur = None
    with open(path, encoding='utf-8') as f:
        for n, line in enumerate(f, 1):
            line = line.rstrip('\n')
            m = ENTRY_RE.match(line)
            if m:
                cur = dict(id=m.group(1), off=int(m.group(2), 16), info=m.group(3), ja='', en='',
                           es='', line=n, file=path)
            elif cur is not None and line.startswith('JA:'):
                cur['ja'] = line[4:] if line.startswith('JA: ') else line[3:]
            elif cur is not None and line.startswith('EN:'):
                cur['en'] = line[4:] if line.startswith('EN: ') else line[3:]
            elif cur is not None and line.startswith('ES:'):
                text = line[3:]
                cur['es'] = text[1:] if text.startswith(' ') else text
                cur['line'] = n
                yield cur
                cur = None


def check_entry(e):
    """Returns the list of errors for one entry with Spanish."""
    errors = []
    text, has_page = st.strip_page_token(e['es'])
    text = charmap.normalize(text)
    if has_page and not e['info'].rstrip().endswith('\\FE\\t60⏎'):
        errors.append(f'{st.PAGE_TOKEN} is only allowed on narration entries that end with \\FE\\t60⏎ '
                      f'(this one ends with: {e["info"].split("…")[-1] or "nothing"})')
    for ch in sorted(set(text)):
        if ch in charmap.STAND_INS:
            errors.append(f"'{ch}' is reserved (it stands in for an accented letter) and can't be typed")
        elif ch != st.LF and ord(ch) >= 0x80 and ch not in charmap.SPANISH:
            errors.append(f"'{ch}' is not in the font")
    ja_codes, es_codes = st.codes_in(e['ja']), st.codes_in(text)
    if ja_codes != es_codes:
        errors.append(f'codes inside the text differ: JA has {ja_codes or "none"}, ES has {es_codes or "none"}')
    if e['ja'].count(st.LF) != text.count(st.LF):
        errors.append(f'line breaks ({st.LF}): JA has {e["ja"].count(st.LF)}, ES has {text.count(st.LF)}')
    width = st.LINE_WIDTH if '\\FS' in e['info'] else st.DIALOGUE_CONTENT_WIDTH
    for w in re.split(r'[ \n]+', text.replace(st.LF, ' ')):
        if st.visible_len(w) > width:
            errors.append(f'a word is longer than {width} characters: {w[:20]}...')
    if not errors:
        try:
            charmap.encode(text.replace(st.LF, '\n'))
        except ValueError as ex:
            errors.append(str(ex))
    return errors


def orphan(e):
    """Warning text if the entry wraps to several lines, ends with a line break, and its last
    line is only a few characters (a nearly empty screen line), else ''."""
    if not (e['es'].strip(' ') and e['info'].rstrip().endswith(st.LF) and not st.continues_info(e['info'])):
        return ''
    text = charmap.normalize(st.strip_page_token(e['es'])[0]).replace(st.LF, '\n')
    wrapped = st.chain_wrap([[text]], '\\FS' in e['info'])[0][0]
    for para in wrapped.split('\n'):
        n = st.visible_len(para)
        last = n - ((n - 1) // st.LINE_WIDTH) * st.LINE_WIDTH if n > st.LINE_WIDTH else 0
        if 0 < last <= st.ORPHAN_MAX:
            return (f'the last line has only {last} characters ({para.rstrip()[-last:]!r}) and the next entry '
                    f'starts a new line: shorten or rebalance to avoid a nearly empty line')
    return ''


_MENUS = {}


def menu_offsets(script):
    """Offsets of the choice-menu option records of a script (empty if the source ISO is not at hand)."""
    if script not in _MENUS:
        try:
            import olm
            _MENUS[script] = olm.menu_starts(project.read_iso_file('OLM/' + script))
        except Exception:
            _MENUS[script] = set()
    return _MENUS[script]


def screen_lint(script, entries, only=None):
    """Problems on the screens as the build lays them out (tools/screens.py), or None if that
    can't run here (no source ISO): then the line-count heuristics below are used instead."""
    if not any(e['es'].strip(' ') for e in entries):
        return []
    try:
        import screens
        return screens.lint(script, entries, only)
    except (OSError, FileNotFoundError) as ex:
        print(f'warning {script}: screens not simulated ({ex}); using line-count estimates')
        return None


def pages(entries):
    """Group the entries of one script into screen pages.

    A page ends at an entry whose ending codes include \\k (wait for a key), or whose
    Spanish ends with <PAGE>. Narration pages start with \\FS. Returns a list of
    (kind, [entries], lines needed); untranslated entries count by their English text.
    """
    out, cur = [], []
    for e in entries:
        cur.append(e)
        es_text, has_page = st.strip_page_token(e['es'])
        if '\\k' in e['info'] or has_page:
            out.append(cur)
            cur = []
    if cur:
        out.append(cur)
    result = []
    for page in out:
        kind = 'narration' if '\\FS' in page[0]['info'] else 'dialogue'
        lines, chain = 0, []
        menus = menu_offsets(page[0]['id'].split(':')[0])
        for e in page:
            if e['off'] in menus:                      # a menu option is its own box
                if chain:
                    lines += st.chain_lines(chain, kind == 'narration')
                    chain = []
                continue
            t = st.strip_page_token(e['es'])[0] if e['es'].strip(' ') else e['en']
            if t.strip():
                chain.append([t])
            if not st.continues_info(e['info']) and chain:      # a chain ends: it is laid out as one text
                lines += st.chain_lines(chain, kind == 'narration')
                chain = []
        if chain:
            lines += st.chain_lines(chain, kind == 'narration')
        result.append((kind, page, lines))
    return result


def run(paths, show_pages=False):
    """Check translation files, print the problems, return the number of errors."""
    args = argparse.Namespace(paths=paths, pages=show_pages)
    files = []
    for p in args.paths:
        files += sorted(glob.glob(os.path.join(p, '**', '*.txt'), recursive=True)) if os.path.isdir(p) else [p]
    by_script = {}
    for path in files:
        for e in parse(path):
            by_script.setdefault(e['id'].split(':')[0], []).append(e)
    total = done = n_err = n_warn = 0
    per_script = {}
    for script, entries in sorted(by_script.items()):
        for e in entries:
            total += 1
            s = per_script.setdefault(script, [0, 0])
            s[0] += 1
            if not e['es'].strip(' '):
                continue
            done += 1
            s[1] += 1
            for m in check_entry(e):
                n_err += 1
                print(f'ERROR   {os.path.relpath(e["file"], project.ROOT)}:{e["line"]} {e["id"]}: {m}')
        for e in entries:
            m = orphan(e)
            if m:
                n_warn += 1
                print(f'warning {os.path.relpath(e["file"], project.ROOT)}:{e["line"]} {e["id"]}: {m}')
        screen_msgs = screen_lint(script, entries)
        if screen_msgs is not None:              # the exact screens (tools/screens.py)
            for level, e, m in screen_msgs:
                where = f'{os.path.relpath(e["file"], project.ROOT)}:{e["line"]} {e["id"]}' if e else script
                if level == 'error':
                    n_err += 1
                    print(f'ERROR   {where}: {m}')
                else:
                    n_warn += 1
                    print(f'warning {where}: {m}')
            continue
        for kind, page, lines in pages(entries):  # fallback without the source ISO
            if not any(e['es'].strip(' ') for e in page):
                continue
            first, last = page[0], page[-1]
            where = f'{os.path.relpath(first["file"], project.ROOT)}:{first["line"]} {first["id"]}..{last["id"]}'
            if kind == 'narration':
                if args.pages:
                    print(f'page {first["id"]}..{last["id"]}: {lines} lines')
                if lines > st.NARRATION_PAGE_LINES:
                    n_err += 1
                    print(f'ERROR   {where}: this narration page needs {lines} lines, the limit is '
                          f'{st.NARRATION_PAGE_LINES}; end the page earlier with {st.PAGE_TOKEN} or shorten it')
            elif lines > st.DIALOGUE_PAGE_LINES:
                n_warn += 1
                print(f'warning {where}: this dialogue page needs {lines} lines (box fits about '
                      f'{st.DIALOGUE_PAGE_LINES}, unverified)')
    print(f'\n{done} of {total} entries translated ({100 * done / max(total, 1):.1f}%)  |  '
          + ', '.join(f'{k} {v[1]}/{v[0]}' for k, v in sorted(per_script.items()) if v[1])
          + f'\n{n_err} error(s), {n_warn} warning(s)')
    return n_err


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('paths', nargs='*', default=[project.TRANSLATION])
    ap.add_argument('--pages', action='store_true', help='print every narration page with its line count')
    args = ap.parse_args()
    sys.exit(1 if run(args.paths, args.pages) else 0)


if __name__ == '__main__':
    main()
