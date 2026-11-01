"""Build and publish the PUBLIC copy of this repository (tools, docs, agents; no translation, no game data).

    python -I -X utf8 tools/export_public.py                       dry run: build the snapshot, run the safety checks, list it
    python -I -X utf8 tools/export_public.py --push --remote <url> commit the snapshot to the public clone and push it

The working repository keeps everything locally (translation/ holds the Japanese original next to the
Spanish, which must never be published). This tool takes the files that git tracks, drops what must
stay private, checks the rest, and copies them into a separate clone (work/public_repo, untracked)
with its own history: one commit per export. The author is the GitHub no-reply address, so no private
e-mail address ends up in a public commit.

Safety checks (a failure stops the export): no path under a denied prefix, no file bigger than 1 MB,
no disc/archive/patch extension, and no file with a large amount of Japanese text.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CLONE = os.path.join(ROOT, 'work', 'public_repo')

DENY_PREFIXES = ('translation/', 'work/', 'build/')        # never published
DENY_EXT = ('.iso', '.bin', '.img', '.mdf', '.cue', '.bps', '.ips', '.ppf', '.p2s', '.elf', '.zip', '.7z', '.rar', '.ttf')
MAX_BYTES = 1_000_000
MAX_CJK = 2000                                              # Japanese characters allowed in one file (glossary terms, short quotes)
CJK = re.compile('[぀-ヿ一-鿿＀-￯]')
NOREPLY = '{id}+{login}@users.noreply.github.com'


def git(*args, cwd=ROOT, check=True):
    r = subprocess.run(['git', *args], cwd=cwd, capture_output=True, text=True, encoding='utf-8')
    if check and r.returncode:
        raise SystemExit(f'git {" ".join(args)} failed:\n{r.stderr}')
    return r.stdout


def public_files():
    files = [f for f in git('ls-files').split('\n') if f]
    return [f for f in files if not f.startswith(DENY_PREFIXES)]


def safety(files):
    problems = []
    for f in files:
        path = os.path.join(ROOT, f)
        if os.path.basename(f).startswith('.env'):
            problems.append(f'{f}: secrets file')
        if f.lower().endswith(DENY_EXT):
            problems.append(f'{f}: extension not allowed')
        if os.path.getsize(path) > MAX_BYTES:
            problems.append(f'{f}: bigger than {MAX_BYTES:,} bytes')
        try:
            text = open(path, encoding='utf-8').read()
        except (UnicodeDecodeError, OSError):
            continue
        n = len(CJK.findall(text))
        if n > MAX_CJK:
            problems.append(f'{f}: {n} Japanese characters (limit {MAX_CJK}): game text?')
    return problems


def snapshot(files):
    """Replace the clone's working tree with `files` (keeps .git)."""
    os.makedirs(CLONE, exist_ok=True)
    for name in os.listdir(CLONE):
        if name != '.git':
            p = os.path.join(CLONE, name)
            shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    for f in files:
        dst = os.path.join(CLONE, f)
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(os.path.join(ROOT, f), dst)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--push', action='store_true', help='commit the snapshot and push it')
    ap.add_argument('--remote', help='URL of the public repository (needed the first time)')
    ap.add_argument('--email', help='author e-mail (default: the GitHub no-reply address, see --gh-id)')
    ap.add_argument('--gh-id', help='numeric GitHub user id, for the no-reply address')
    ap.add_argument('--login', default='Corcholog')
    ap.add_argument('-m', '--message', default='Update from the working repository')
    args = ap.parse_args()

    files = public_files()
    problems = safety(files)
    total = sum(os.path.getsize(os.path.join(ROOT, f)) for f in files)
    print(f'{len(files)} files, {total / 1e6:.2f} MB (denied: {", ".join(DENY_PREFIXES)})')
    if problems:
        raise SystemExit('Safety check failed:\n  ' + '\n  '.join(problems))
    print('Safety checks passed.')

    snapshot(files)
    if not os.path.isdir(os.path.join(CLONE, '.git')):
        git('init', '-b', 'main', cwd=CLONE)
    if args.remote:
        have = git('remote', cwd=CLONE).split()
        git('remote', 'set-url' if 'origin' in have else 'add', 'origin', args.remote, cwd=CLONE)
    email = args.email or (NOREPLY.format(id=args.gh_id, login=args.login) if args.gh_id else None)
    if email:
        git('config', 'user.email', email, cwd=CLONE)
        git('config', 'user.name', args.login, cwd=CLONE)
    git('add', '-A', cwd=CLONE)
    status = git('status', '--short', cwd=CLONE)
    print(status.rstrip() or 'No changes since the last export.')
    if not args.push:
        print(f'Dry run: snapshot written to {CLONE}. Add --push to commit and push.')
        return
    if not git('config', 'user.email', cwd=CLONE, check=False).strip():
        raise SystemExit('Set the author with --gh-id (no-reply address) or --email first.')
    if status.strip():
        git('commit', '-m', args.message, cwd=CLONE)
    git('push', '-u', 'origin', 'main', cwd=CLONE)
    print('Pushed.')


if __name__ == '__main__':
    main()
