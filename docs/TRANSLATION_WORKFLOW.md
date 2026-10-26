# Translation workflow

How a batch of the script goes from Japanese to reviewed Spanish. Written for the translator and reviewer agents (`.claude/agents/`) and for the human reviewer. Ideas borrowed from [senshinji/claude-translation-skill](https://github.com/senshinji/claude-translation-skill) (MIT): separate translator and reviewer roles, a line-by-line anti-fabrication/omission check, structured review output. Everything else is specific to this game.

## Shared memory (what makes the translation consistent)
Translating the whole game at once is neither possible nor good (33,000 entries cannot be held, reviewed or corrected together). Consistency comes from files every batch reads, so each batch benefits from everything decided or learned before it:
- `docs/STYLE_GUIDE.md`: decided names, terms, voices, formats. **Binding.**
- `docs/STORY.md`: the **story bible**: setting, characters as shown by the text, scenes so far, running jokes. Updated after every batch (at most 6 lines per batch; kept under ~300 lines).
- `docs/scouting/<script>.md`: the **read-ahead** for a script file, written once before its first batch by the `mmm-scout` agent (scene map, recurring terms with proposed Spanish, wordplay, formatting hazards, questions). Proposals become binding only when the user approves them into the style guide.
- The batch's own **context lines** (the last translated entries before it).

## The loop (run with `/translate scout O1`, then `/translate O1`, or by hand)
0. **Once per script file:** `/translate scout <script>` → `tools/scout.py digest` + the `mmm-scout` agent → `docs/scouting/<script>.md`; the user answers its questions; decided terms go into the style guide.
1. `python -I -X utf8 tools/batch.py next O0 --size 80` → `work/batches/O0_<from>-<to>.md` (what to translate, by page, with budgets) and `.tsv` (the draft to fill).
2. **Translator agent** (`mmm-translator`) fills the `.tsv` and runs `tools/batch.py check` until it has 0 errors.
3. **Reviewer agent** (`mmm-reviewer`) checks every line against the Japanese and writes `…_reviewed.tsv` (the corrected full draft) and `…_review.md` (what changed and why).
4. `python -I -X utf8 tools/batch.py apply work/batches/…_reviewed.tsv` → into `translation/`, then `python -I -X utf8 tools/check.py`.
5. **Story bible:** the reviewer's story notes (at most 6 lines) are appended to `docs/STORY.md`.
6. **Human review** (the user): read the batch in `translation/`, especially the `NOTE:` lines and the review report; edit any `ES:` line directly. Decisions on terms go into the style guide.
7. From time to time: `python -I -X utf8 tools/build.py` and play the new part in PCSX2.

`python -I -X utf8 tools/batch.py status` shows progress and open notes.

## Hard limits (the tools reject a draft that breaks them)
- **Characters:** letters, digits, space, `? ! ' " ( ) . , - : ; / * ~ %` and `á é í ó ú ñ ü Á É Í Ó Ú Ñ Ü ¿ ¡`. Write `...` (not `…`), `--` for a long dash, `"` for quotes (`'` inside quotes). **Never** `% & + < = > @ [ ] ^ _ \` { | } # $` (they secretly stand in for the accented letters), no `♪ ○ ③`, no Japanese characters.
- **Codes:** never type the codes shown on the `==` line (`\FS`, `\FE\t60\k\O`, …): the tool adds them. Codes inside the Japanese text (`\LC`, `\CG…`, `\d`, `\o`, `\V`) must appear in the Spanish too, in the same order. `⏎` is a line break inside an entry: use exactly as many as the Japanese has.
- **Wrapping:** don't break or pad lines; the tool wraps for you: **47 characters** on narration pages (`\FS`), **46 characters** in the dialogue box (its 47th column is half hidden: measured 2026-10-26). Entries that continue on the same line (their ending codes have no `⏎`, `\k`, `\p` or `\O`, e.g. a quote split across two entries) are wrapped **together** with a space between them, so don't add or remove that space yourself.
- **Screen errors:** `batch.py check` and `check.py` lay out every screen your entries appear on exactly as the game will show it (`tools/screens.py`). An error names the entry and says what is wrong (a row wider than the box, a box needing more than 4 rows, two words glued where two entries meet, a number the game draws glued to the word before it, Japanese left on the screen). Fix the Spanish, never the tool. `python -I -X utf8 tools/screens.py O0 --png` writes the whole script as text screens (and pictures of flagged ones) for a human look.
- **Strings from the executable** (`<script>_exe.txt`, IDs `O0:X001`...): a few lines are short strings the game takes from SLPS_251.92 (`あ……`, `その、`, `ふむ。`, `。`). Translate them like any entry; they sit inside a sentence of the neighbouring entries, so read those first. They are handled after the other entries of the script.
- **No orphan lines:** an entry that ends with `⏎` and wraps to a last line of 10 characters or fewer (e.g. a lone `tiempos,`) wastes a whole screen line; `check.py` warns. Rewrite the entry so it fits on one line, or lengthen/shorten it so the last line is a real line.
- **Numbers:** write **10 and up as digits** (88 años, 150 centímetros, 20 minutos), percentages as `30%`, and minutes/measures with digits when the Japanese has digits; **0-9 stay words** (dos, tres, cinco), and spoken clock times stay words ("las cinco y media"). Displayed time stamps are `10:03 AM`; spoken times without 午前/午後 get no AM/PM.
- **Narration pages** (entries with `\FS`, grouped until an entry ending in `\k\O`): **10 lines in total**. Past that the game draws garbage. **Dialogue pages** (one entry each): **4 lines** (confirmed 2026-10-26: four full lines fit, that is the limit).
- **`<PAGE>`** at the end of a narration entry that ends with `\FE\t60⏎` ends the page there. Use it only when the page can't fit even after condensing, and only at a natural break (end of a sentence or paragraph).
- Entries marked "continues the previous entry" are the second half of the same sentence; translate both so they read as one.
- Entries shown with **ES (already translated, do not change)** were pre-filled from an identical line elsewhere (`NOTE: copied from ...`); they are context, not in the .tsv. The reviewer checks every copy in the batch: one that reads wrong in its new place (same Japanese, different context) gets a row in the reviewed .tsv with the corrected Spanish and `NOTE: rev: pre-filled copy fixed`; `batch.py apply` may overwrite such copies without --force.
- Entries marked **BRANCH** are joined by the game across a jump: the sentence goes on in the entry named in the flag, not in the next one in the file (several alternative lines can lead into the same entry). The entry after such a piece usually starts a new sentence; the shared entry must read well after each of its leads (e.g. lowercase after "Mmm,").
- Entries with empty Japanese stay empty.

## How to translate a page
1. **Read the whole page in Japanese first** (and the context lines before the batch). Translate from the **Japanese**. The English line is a reference to confirm meaning; if it disagrees with the Japanese, follow the Japanese and add a `NOTE:`.
2. **Budget:** Spanish runs ~40% longer than the Japanese layout. Aim for the Japanese line count shown in the page header; the narration limit is 10. Condense like a professional: shorter synonyms, no redundant connectors, merge clauses, drop filler words. **Never** drop information or invent any (see the checklist below).
3. **Voice and register** (details in `docs/STYLE_GUIDE.md`): neutral Latin American Spanish (ustedes, no vosotros, no voseo, no regional slang). `tú` between young characters and friends, `usted` for strangers/elders/formal speech (follow the Japanese politeness level). Kyosuke narrates in first person, casual and a bit sarcastic; keep the tense of the Japanese (present or past).
4. **Dialogue lines** keep the speaker inline: `Kyosuke: "..."`. `「」` become `"`. Speaker names: the character table in the style guide (`？？` → `???`).
5. **Interjections and sounds** (あ…, うぉ, ふあ～あ, むにゃむにゃ): adapt to natural Spanish (`Ah...`, `¡Uah!`, `Aaaahh`, `*murmullo*`); long vowels may be stretched (`Vaaale`). Use `¿...?` and `¡...!` with opening marks, also `¡¿...?!` for mixed (user decision 2026-10-25; never `¿¡...!?`).
6. **Numbers and units:** words in narration (`ochenta y ocho años`); times as `10:03 AM` / `3:30 PM` (decided 2026-10-25: short, fits better).
7. **When unsure** (wordplay, cultural reference, ambiguous subject): write your best translation and add `NOTE: …` in the third column explaining the doubt. Don't leave a line empty.
8. **New names or recurring terms:** use the style guide if listed; otherwise choose, and list it in your final summary as a glossary proposal.

## Anti-fabrication / omission checklist (translator self-check, reviewer line by line)
For every entry: (1) every piece of information in the Japanese is in the Spanish; (2) nothing in the Spanish is absent from the Japanese (no explanations, no added jokes); (3) who does what to whom is the same (Japanese often omits the subject: check it from context); (4) negations, numbers, names, and tense are right; (5) the tone matches (polite/rude, teasing, childlike for Reu); (6) the line still fits its page.

## Output formats
- **Draft** (`.tsv`): `O0:0083<TAB>Spanish text<TAB>NOTE: optional doubt`. One line per entry; keep the IDs exactly.
- **Reviewed draft** (`…_reviewed.tsv`): the full draft with corrections applied; for each changed line add/extend the note `NOTE: rev: <short reason>`.
- **Review report** (`…_review.md`): one bullet per change: ID, category (`fidelity` / `omission` / `addition` / `register` / `naturalness` / `glossary` / `typo` / `budget`), what was wrong, what it is now. Then a short overall assessment and glossary proposals.
