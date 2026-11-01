"""Translate a batch with an LLM reached through the OpenCode API (an alternative to the Claude translator agent).

    python -I -X utf8 tools/llm_batch.py models                          list the model ids your key can use
    python -I -X utf8 tools/llm_batch.py translate work/batches/O2_2401-2700.md --model <id> [options]
    python -I -X utf8 tools/llm_batch.py translate <batch.md> --dry-run  build the prompts and print their sizes; no network

What it does (the same as the `mmm-translator` agent, minus the file tools):
  1. builds the system prompt from the project's own rules: docs/TRANSLATION_WORKFLOW.md, docs/STYLE_GUIDE.md,
     docs/scouting/<script>.md and a trimmed docs/STORY.md;
  2. translates the batch in chunks of whole pages (--chunk entries, default 60), each call carrying the last
     translated lines as context;
  3. writes the .tsv exactly where the Claude translator would, then runs the same checks as `batch.py check`
     (tools/batch.py validate) and sends only the failing entries back for correction, up to --rounds times.
The review step (mmm-reviewer) and `batch.py apply` stay as they are.

The API key is read from the environment variable OPENCODE_GO_API_KEY or, if it is not set, from a line
OPENCODE_GO_API_KEY=... in the file .env in the project root (ignored by git). It is never printed or stored.
The script sends the Japanese script text of the batch to the API: that is the point of using it.

API (docs: https://opencode.ai/v2/docs/console/api/inference and .../console/go): a Go subscription uses the base
https://opencode.ai/inference/go (default here); chat models at /openai/v1/chat/completions (default), Claude/Qwen-family
models at /anthropic/v1/messages (--api anthropic). DeepSeek models need Settings > Privacy > Regions = Global in the console.
"""
import argparse
import json
import os
import re
import sys
import time
import urllib.error
import urllib.request

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import batch  # noqa: E402
import project  # noqa: E402

BASE = 'https://opencode.ai/inference/go'     # the Go subscription's endpoints (the plain /inference ones bill the balance: HTTP 402)
SESSION = 'mmm-batch-' + str(int(time.time()))     # stable per run, sent as x-opencode-session
KEY_VAR = 'OPENCODE_GO_API_KEY'
ID = r'O\d:(?:\d{4}(?:\.\d+)?|X\d{3})'
ID_RE = re.compile(rf'^({ID})$')
PAGE_SPLIT = re.compile(r'^(?=## Page )', re.M)
ENTRY_ID = re.compile(rf'^\*\*({ID})\*\*', re.M)
REPLY_LINE = re.compile(rf'^({ID})\t(.*)$')

ROLE = """You are a professional Japanese -> Spanish (neutral Latin American) game translator working on the visual novel
"My Merry May" (PS2). You translate one batch of its script at a time, from the JAPANESE (the EN lines are only a
reference). The project's binding rules follow: the translation workflow, the style guide (decided terms are
binding), the read-ahead notes for this script file and the story so far. Follow them exactly.

OUTPUT FORMAT (strict): reply with ONLY translation lines, one per required entry, in the order given, each line
being: ID<TAB>Spanish text<TAB>NOTE: optional doubt   (a real TAB character between columns; the third column only
when you have a doubt worth a note). No headings, no commentary, no code fences, no blank lines, no quotes around the
Spanish text. Keep IDs exactly. Use the character ⏎ for a line break inside an entry exactly as many times as the
Japanese has. Never type the codes shown on the "==" lines. Never type & < = > @ [ ] ^ _ \\ ` { | } # $ (they stand in for
accented letters) nor a capital Í or Ü (write I, U). % + and × are allowed. Do not pad or wrap lines yourself. Entries shown with
"ES (already translated, do not change)" are context only: do NOT output a line for them.

KNOWN PITFALLS (a Claude reviewer found these in a previous draft of yours; avoid them):
1. Apply every DECIDED term of the style guide literally: Reu's えへへ/うふふ = "Jijiji~"; おかえり = "bienvenido/a";
   がんばって = "¡ánimo!" (Misao: "Da lo mejor de ti"); 返事は一回 = "¡Se responde una sola vez!"; グラウンド = "el campo";
   a quote that repeats in the story must be word for word identical to its earlier translation.
2. No calques from Japanese or from the EN reference: never "Diciendo eso, X hizo..." (say what happens), never
   "se calla la boca", "te hice preocuparte", "eso era realmente bueno". Write what a Latin American would say.
3. Keep particles and nuance: だから = "porque/por eso", だそうです = hearsay ("dicen que", "parece que"), さて = a pause
   ("Bueno,"), もう一回 = "otra vez", sarcasm (ステキ), sighs (あ～あ = "Ahh...") and yawns, stutters (keep them as stutters:
   "Es... escapo"), slurred speech (keep the slur if the next line corrects it). Do not drop or add information
   (no added "supongo", "vaya", "ni siquiera... ¿no?").
4. Tense and subject: keep the Japanese tense (present narration stays present) and say who does what; Japanese often
   omits the subject: find it in the context.
5. Voices: Misao uses tú with Kyosuke; Kyosuke uses usted with Tae and tú with Misao; Tae tú; Reu says "yo"
   for わたし and uses "hermano" for Kyosuke. 夕方 = "al atardecer", not "de tarde".
6. Ellipses: … and …… (one or two characters) = "..." (three dots, never six); only a run of 3 or more ellipsis
   characters gets three dots per character (4 characters = 12 dots).
7. Always keep -chan/-kun/-san on names (もとみちゃん = "Motomi-chan"), in narration and vocatives too.
8. Inside a quote use single quotes for a quoted word or phrase ('familia'), never nested double quotes; 『』 around a
   single term = '...'. Never nest ¡...¿...?! punctuation; every sentence needs a verb.
9. When a passage or sentence repeats in the batch or in the context, translate it word for word the same.
10. Keep the tense of the Japanese (do not turn past into present or the reverse). The subject of an echo or a short
   reply is the speaker: check who says it. Avoid regionalisms ("apurada", "es lo que hay"); カバン = "mochila".
11. Keep the format to the LAST entry: if the Japanese starts with `Name「`, your line starts with `Name: "` and ends
   with `"`; inner-thought narration gets no quote marks. Idioms get their meaning, never a literal rendering
   (奥歯にものが挟まった = "hablar con rodeos", 気味が悪い = "me da escalofríos", まったく… = "Increíble...").
12. Do not flatten hedges: ような similes ("como si..."), と思う ("creo que"), ほとんど ("casi"), だって ("es que") stay.
   A cut-off or elided sentence (あなたが……でしょ) stays cut off: do not fill it with invented words. Do not add
   superlatives ("más", "la más") the Japanese lacks. A sentence-final か musing is not a tag question ("¿no?");
   a greeting reply ああ is "Sí" or "Hola", not "Ah...". Use one verb for the same action; no Peninsular "y eso".
13. 〜たら / 〜ば keep their tense ("cuando termines", not "ya terminaste"); あのね, 確か, 頼むよ, さすが are attitude
   particles, not content (no "Es que", "Seguro que", "te lo pido", "Como era de esperarse"). When two neighbouring
   lines make a pun or contradiction (気にするな / 気になる), keep the pair visible in both. Teenagers and Reu never use
   formal words ("¿Qué se te ofrece?", "mortificar"). Add no connectors the Japanese lacks.
14. Ellipsis runs: count the characters (…… = "...", 4 characters = 12 dots, never 30); a leading "..." stays, with no
   space after it. オヤジ = "mi viejo", never "papá". Register follows the speaker AND the listener (です/ます = usted,
   also toward a third party: Tae and Lease use usted with Kyohei). Keep -san on a first full name. Do not drop or add
   とりあえず, わざわざ, って言うじゃない, "muy", "definitivamente". Never write "NOTE: rev:" (only the reviewer does).
15. Add no ellipsis the Japanese lacks (no "..." at the end of a line that ends in 。 or in nothing). A run of 4
   ellipsis characters is exactly 12 dots. Render one Japanese word the same way throughout the batch (check your
   own earlier lines). はい while handing something over is "Aquí tiene", not "Sí". A から clause needs its main clause
   (or is "Es que..." when the Japanese stops there). Mixed marks are ¡¿...?!, never ¿¿...??.
16. 〜のに is not "aunque" (it is "si ... / siendo que ..."); the long dash ―― is `--` with nothing added beside it;
   は？ / はあ？ is "¿Qué?" or "¿Cómo?", never "¿Ah?"; コードネーム = "nombre en clave"; keep the subject of an embedded
   clause; no Peninsular "¿Y eso?"; write only constructions that exist in Spanish (no "no se me abrazó").
Before answering, re-read each line once against the Japanese for these sixteen points."""


def read_text(path, default=''):
    try:
        return open(path, encoding='utf-8').read()
    except OSError:
        return default


def api_key():
    key = os.environ.get(KEY_VAR, '').strip()
    if not key:
        for line in read_text(os.path.join(project.ROOT, '.env')).splitlines():
            line = line.strip()
            if line.startswith(KEY_VAR + '='):
                key = line.split('=', 1)[1].strip().strip('"\'')
    if not key:
        raise SystemExit(f'No API key: set the environment variable {KEY_VAR} (or put {KEY_VAR}=... in .env in the '
                         f'project root; .env is ignored by git). Environment variables set after the app started '
                         f'are only seen by programs started afterwards.')
    return key


def http(method, url, body=None, key=None, timeout=300):
    data = None if body is None else json.dumps(body).encode('utf-8')
    headers = {'Authorization': 'Bearer ' + key, 'Content-Type': 'application/json',
               'User-Agent': 'mmm-spanish-patch/1.0', 'anthropic-version': '2023-06-01',
               'x-opencode-session': SESSION}
    last = None
    for attempt in range(6):
        try:
            req = urllib.request.Request(url, data=data, headers=headers, method=method)
            with urllib.request.urlopen(req, timeout=timeout) as r:
                return json.load(r)
        except urllib.error.HTTPError as e:
            text = e.read().decode('utf-8', 'replace')[:400]
            last = f'HTTP {e.code}: {text}'
            if e.code not in (408, 429, 500, 502, 503, 504):
                raise SystemExit(f'API error ({url}): {last}')
        except (urllib.error.URLError, TimeoutError, ConnectionError) as e:
            last = str(e)
        time.sleep(min(60, 4 * 2 ** attempt))
    raise SystemExit(f'API did not answer after retries: {last}')


def call(system, user, args, key, usage):
    """One model call; returns the reply text. `usage` accumulates tokens and cost."""
    if args.api == 'anthropic':
        body = {'model': args.model, 'max_tokens': args.max_tokens, 'system': system,
                'messages': [{'role': 'user', 'content': user}]}
        if args.temperature is not None:
            body['temperature'] = args.temperature
        res = http('POST', args.base + '/anthropic/v1/messages', body, key)
        text = ''.join(p.get('text', '') for p in res.get('content', []) if p.get('type') == 'text')
        u = res.get('usage', {})
        usage['in'] += u.get('input_tokens', 0)
        usage['out'] += u.get('output_tokens', 0)
    else:
        body = {'model': args.model, 'max_tokens': args.max_tokens,
                'messages': [{'role': 'system', 'content': system}, {'role': 'user', 'content': user}]}
        if args.temperature is not None:
            body['temperature'] = args.temperature
        res = http('POST', args.base + '/openai/v1/chat/completions', body, key)
        text = (res.get('choices') or [{}])[0].get('message', {}).get('content') or ''
        u = res.get('usage', {})
        usage['in'] += u.get('prompt_tokens', 0)
        usage['out'] += u.get('completion_tokens', 0)
    usage['cost'] += float(res.get('usage', {}).get('cost', 0) or 0)
    usage['calls'] += 1
    if not text.strip():
        raise SystemExit('The model returned an empty reply (check the model id and --max-tokens).')
    return text


def list_models(args):
    key = api_key()
    res = http('GET', args.base + '/v1/models', None, key, timeout=60)
    ids = sorted(m.get('id', '') for m in res.get('data', res if isinstance(res, list) else []))
    print(f'{len(ids)} models:')
    for i in ids:
        print('  ' + i)


# ---------------------------------------------------------------- prompts

def trimmed_story(script, keep=30):
    """Setting, characters, motifs and open questions in full; only the last `keep` bullets of the scene list."""
    text = read_text(os.path.join(project.ROOT, 'docs', 'STORY.md'))
    parts = re.split(r'^(?=## )', text, flags=re.M)
    out = []
    for p in parts:
        if p.startswith('## Scenes'):
            lines = p.split('\n')
            bullets = [i for i, l in enumerate(lines) if l.startswith('- ')]
            if len(bullets) > keep:
                cut = bullets[-keep]
                lines = lines[:1] + ['(older scenes omitted)'] + lines[cut:]
            p = '\n'.join(lines)
        out.append(p)
    return ''.join(out)


def system_prompt(script):
    root = project.ROOT
    pieces = [ROLE,
              '=== docs/TRANSLATION_WORKFLOW.md ===\n' + read_text(os.path.join(root, 'docs', 'TRANSLATION_WORKFLOW.md')),
              '=== docs/STYLE_GUIDE.md ===\n' + read_text(os.path.join(root, 'docs', 'STYLE_GUIDE.md')),
              f'=== docs/scouting/{script}.md ===\n' + read_text(os.path.join(root, 'docs', 'scouting', f'{script}.md'), '(none)'),
              '=== docs/STORY.md (trimmed) ===\n' + trimmed_story(script)]
    return '\n\n'.join(pieces)


def split_batch(md_text, required):
    """-> (header, [pages]) with each page = (text, [required ids on it])."""
    parts = PAGE_SPLIT.split(md_text)
    header, pages = parts[0], parts[1:]
    out = []
    for p in pages:
        ids = [i for i in ENTRY_ID.findall(p) if i in required]
        out.append((p, ids))
    return header, out


def make_chunks(pages, size):
    chunks, cur, n = [], [], 0
    for text, ids in pages:
        cur.append((text, ids))
        n += len(ids)
        if n >= size:
            chunks.append(cur)
            cur, n = [], 0
    if cur:
        chunks.append(cur)
    return chunks


def chunk_message(name, header, chunk, first, draft, order):
    ids = [i for _, ids in chunk for i in ids]
    parts = [f'Batch {name}. Translate ONLY these required entries, in this order, and output one line for each:\n' + ' '.join(ids)]
    if first:
        parts.append(header.strip())
    else:
        last = [i for i in order if i in draft and draft[i][0]][-8:]
        if last:
            parts.append('Context (your last translated entries of this batch; do not repeat them):\n' +
                         '\n'.join(f'- {i}: {draft[i][0]}' for i in last))
    parts.append(''.join(text for text, _ in chunk))
    parts.append('Reply with ONLY the lines ID<TAB>Spanish<TAB>NOTE: optional, nothing else.')
    return '\n\n'.join(parts)


def parse_reply(text, allowed):
    got = {}
    for raw in text.replace('\r', '').split('\n'):
        raw = raw.strip('`').rstrip()
        m = REPLY_LINE.match(raw)
        if not m or m.group(1) not in allowed:
            continue
        cols = m.group(2).split('\t')
        es = cols[0].strip()
        note = cols[1].strip() if len(cols) > 1 else ''
        if note.startswith('NOTE:'):
            note = note[5:].strip()
        got[m.group(1)] = (es, note)
    return got


def error_ids(errors):
    """{id: [messages]} from batch.validate errors (skips warnings)."""
    out = {}
    for e in errors:
        if e.startswith('warning'):
            continue
        m = re.match(rf'^({ID}):\s*(.*)$', e)
        if m:
            out.setdefault(m.group(1), []).append(m.group(2))
    return out


# ---------------------------------------------------------------- main command

def translate(args):
    md_path = args.md
    tsv_path = os.path.splitext(md_path)[0] + '.tsv'
    name = os.path.basename(md_path)[:-3]
    script = name.split('_')[0]
    order = [l.split('\t')[0].strip() for l in read_text(tsv_path).splitlines() if ID_RE.match(l.split('\t')[0].strip())]
    if not order:
        raise SystemExit(f'{tsv_path}: no entry IDs (run batch.py next first)')
    existing = batch.read_tsv(tsv_path)
    if any(t for t, _ in existing.values()) and not args.force:
        raise SystemExit(f'{tsv_path} already has Spanish text; use --force to overwrite it.')
    required = set(order)
    md_text = read_text(md_path)
    header, pages = split_batch(md_text, required)
    chunks = make_chunks(pages, args.chunk)
    system = system_prompt(script)
    print(f'{name}: {len(order)} entries, {len(chunks)} chunks; system prompt {len(system):,} characters')
    if args.dry_run:
        for k, ch in enumerate(chunks, 1):
            msg = chunk_message(name, header, ch, k == 1, {}, order)
            print(f'  chunk {k}: {sum(len(i) for _, i in ch)} entries, user message {len(msg):,} characters')
        print('Dry run: nothing sent.')
        return
    key = api_key()
    usage = {'in': 0, 'out': 0, 'cost': 0.0, 'calls': 0}
    draft = {}
    for k, ch in enumerate(chunks, 1):
        want = [i for _, ids in ch for i in ids]
        got = {}
        for attempt in range(3):
            missing = [i for i in want if i not in got]
            if not missing:
                break
            if attempt == 0:
                msg = chunk_message(name, header, ch, k == 1, draft, order)
            else:
                msg = (f'You omitted these entries. Reply with ONLY their lines (ID<TAB>Spanish<TAB>NOTE: optional): '
                       + ' '.join(missing) + '\n\n' + ''.join(t for t, ids in ch if set(ids) & set(missing)))
            got.update(parse_reply(call(system, msg, args, key, usage), set(want)))
        for i in want:
            draft[i] = got.get(i, ('', ''))
        print(f'  chunk {k}/{len(chunks)}: {sum(1 for i in want if draft[i][0])}/{len(want)} entries')

    def save():
        with open(tsv_path, 'w', encoding='utf-8', newline='\n') as f:
            for i in order:
                es, note = draft.get(i, ('', ''))
                f.write(f'{i}\t{es}' + (f'\tNOTE: {note}' if note else '') + '\n')

    save()
    for rnd in range(1, args.rounds + 1):
        rows = {i: draft[i] for i in order}
        errors, _ = batch.validate(rows)
        bad = error_ids(errors)
        for i in order:
            if not draft[i][0] and i not in bad:
                bad[i] = ['empty translation']
        print(f'check round {rnd}: {len(bad)} entries with errors')
        if not bad:
            break
        fix_pages = [(t, ids) for t, ids in pages if set(ids) & set(bad)]
        lines = []
        for t, ids in fix_pages:
            for i in ids:
                lines.append(f'- {i}: current Spanish: {draft[i][0] or "(empty)"}')
        msg = ['Some of your lines failed the automatic checks (rules in the workflow). Fix ONLY the entries listed under '
               '"Errors", keeping everything else as is; shorten or reword in Spanish, never change the tool rules.',
               'Errors:\n' + '\n'.join(f'- {i}: ' + ' | '.join(m) for i, m in bad.items()),
               'Current Spanish of the entries on the affected pages (for context; entries not under Errors are fine):\n'
               + '\n'.join(lines),
               'The affected pages (Japanese):\n' + ''.join(t for t, _ in fix_pages),
               'Reply with ONLY the corrected lines for the entries under Errors: ID<TAB>Spanish<TAB>NOTE: optional.']
        got = parse_reply(call(system, '\n\n'.join(msg), args, key, usage), set(bad))
        for i, v in got.items():
            draft[i] = v
        save()
    else:
        errors, _ = batch.validate({i: draft[i] for i in order})
        bad = error_ids(errors)
        print(f'STILL FAILING after {args.rounds} rounds: ' + (', '.join(bad) or 'none'))
    errors, _ = batch.validate({i: draft[i] for i in order})
    warns = [e for e in errors if e.startswith('warning')]
    real = [e for e in errors if not e.startswith('warning')]
    print(f'Final: {len(real)} error(s), {len(warns)} warning(s) -> {tsv_path}')
    for w in warns[:10]:
        print('  ' + w)
    print(f'Usage: {usage["calls"]} calls, {usage["in"]:,} tokens in, {usage["out"]:,} tokens out'
          + (f', cost ${usage["cost"]:.4f}' if usage['cost'] else ''))
    print('Next: the review step (mmm-reviewer agent), then batch.py check / apply as usual.')


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest='cmd', required=True)
    p = sub.add_parser('models')
    p.add_argument('--base', default=BASE)
    p = sub.add_parser('translate')
    p.add_argument('md', help='work/batches/<script>_<from>-<to>.md (its .tsv must exist next to it)')
    p.add_argument('--model', default=os.environ.get('OPENCODE_GO_MODEL'), help='model id (see the models command)')
    p.add_argument('--api', choices=['openai', 'anthropic'], default='openai', help='chat-completions or messages endpoint')
    p.add_argument('--base', default=BASE)
    p.add_argument('--chunk', type=int, default=60, help='entries per call (whole pages)')
    p.add_argument('--rounds', type=int, default=6, help='check-and-fix rounds')
    p.add_argument('--max-tokens', type=int, default=12000)
    p.add_argument('--temperature', type=float, default=None)
    p.add_argument('--force', action='store_true', help='overwrite a .tsv that already has Spanish')
    p.add_argument('--dry-run', action='store_true')
    args = ap.parse_args()
    if args.cmd == 'models':
        list_models(args)
        return
    if not args.model and not args.dry_run:
        raise SystemExit('Pass --model <id> (or set OPENCODE_GO_MODEL); list ids with: llm_batch.py models')
    translate(args)


if __name__ == '__main__':
    main()
