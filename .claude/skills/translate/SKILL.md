---
name: translate
description: Run the My Merry May translation workflow: "/translate scout O1" (read-ahead of a script file) or "/translate O0" / "/translate O1 120" (one batch: batch → mmm-translator → check → mmm-reviewer → apply → check → story bible). Use when the user asks to translate the next part of the script or to scout a script file.
---

# Translate

Follow `docs/TRANSLATION_WORKFLOW.md`. Two forms:

## `/translate scout <script>`: read-ahead (once per script file, before its first batch)
1. Launch the `mmm-scout` agent with the script name (O0…O7). Wait for it.
2. Check that `docs/scouting/<script>.md` exists and is under ~250 lines.
3. Report to the user: the 5 key findings, and the **questions** the scout raised, each with its recommendation. Wait for the user's answers; record decided terms in `docs/STYLE_GUIDE.md` (the user's decisions only), add a line to `docs/LOG.md`. Don't start batches until the user has answered or said to go ahead.

## `/translate <script> [size]`: one batch (default 300 entries; extended to the end of a page)
0. **Read-ahead present?** If `docs/scouting/<script>.md` doesn't exist, tell the user and run the scout form first (unless the user said to skip it).
1. **Batch:** `python -I -X utf8 tools/batch.py next <script> --size <size>`. Note the `.md` and `.tsv` paths. If nothing is left, tell the user and stop.
2. **Translate:** launch the `mmm-translator` agent with the batch `.md` and `.tsv` paths. Wait for it.
3. **Verify:** `python -I -X utf8 tools/batch.py check <tsv>`. If it has errors, send them back to the translator agent (continue the same agent) and repeat; don't fix them yourself unless trivial.
4. **Review:** launch the `mmm-reviewer` agent with the batch `.md` and `.tsv` paths. Wait for it. Then `python -I -X utf8 tools/batch.py check <batch>_reviewed.tsv` (0 errors required).
5. **Apply:** `python -I -X utf8 tools/batch.py apply <batch>_reviewed.tsv` (plain `apply`: fresh entries need no `--force`). Copy the review report to `translation/reviews/`. Then `python -I -X utf8 tools/check.py` (must be 0 errors) and `python -I -X utf8 tools/batch.py status`.
6. **Story bible:** append the reviewer's final **story notes** to `docs/STORY.md` ("Scenes so far", plus any new facts in the other sections); keep the file under ~300 lines (condense old scenes). Facts from the text only.
7. **Record:** add a line to `docs/LOG.md` (date, batch range, entries, notes left, notable review findings). Glossary proposals go to the user; edit `docs/STYLE_GUIDE.md` only with the user's OK.
8. **Report to the user:** batch range, entries translated, review summary (changes by category), the NOTE lines that need a human decision, glossary proposals, and where to read the result (`translation/<script>/...`). Ask whether to commit (commit only when the user says so) and whether to build an ISO to test.

Rules: one batch per run unless the user asks for more; never skip the review step; never apply a draft with errors; the user decides terms and style.
