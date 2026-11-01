# Plan — My Merry May Spanish patch

Status legend: `[x]` done · `[~]` in progress · `[ ]` not started · `[-]` dropped / not needed

**Current phase:** 5 — Full translation (workflow running: O0 translated 100% on 2026-10-26, 5,935 of 33,133 entries; card names, executable strings and branch joins checked in game 2026-10-25; O1 scouted, scoreboard checked in game; O0, O1 and O2 translated 100% (17,250 of 33,135 = 52.1%, O2 finished 2026-11-01, drafted by DeepSeek V4 Pro with Claude review, not yet committed); next: scout O3; screens are checked by code with tools/screens.py). Open in parallel: menus/system strings, our own font, `bps_create.py`.

---

## Phase 0 — Setup ✅
- [x] Confirm the ISO matches the English patch's base disc (SHA-1 matches)
- [x] Study the English patch (BPS format, scope, known issues)
- [x] Decide translation source, translator, Spanish variety, versioning
- [x] Create git repo, folder layout, documentation

## Phase 1 — Disc extraction and mapping ✅
Goal: know every file on the disc and which ones hold text and fonts.
- [x] Write `tools/iso_extract.py`: list every file with its **LBA** (sector position), size, and path, then extract (file table in `docs/disc_file_table.tsv`)
- [x] Record the file table in `docs/KNOWLEDGE.md`
- [x] Identify the main executable (`SLPS_251.92`) and the data archives
- [x] Apply the English `.bps` to a **copy** of the ISO (`tools/bps_apply.py`; output hash matches the English README)
- [x] Diff the English-patched ISO against the original file by file (`tools/iso_diff.py`)

**Result:** only 9 of 547 files differ. Script text is in `OLM/O0`–`O7`; menu text and the font are in `SLPS_251.92`. Images, sound and video were not touched by the English team.

## Phase 2 — Reverse engineering the formats ✅
Goal: understand the formats well enough to read and write them. Details in KNOWLEDGE.md section 4.
- [x] Script container and compression: none (standalone `OLM/O*` files, plain Shift-JIS)
- [x] Script structure, enough to translate: NUL-terminated text records (4-byte aligned), bytecode of 32-bit words, pointers `0x4D3600 + offset`; full pointer audit against the English answer key (all 2,283 changed pointers found)
- [-] Account for every byte of the bytecode: not needed (we never move bytecode; the English patch doesn't either)
- [x] All eight script files share the format (same analysis on O0–O7; the English patch changes only their text, pointers and size fields)
- [x] Insertion method proven in PCSX2: text moved to the end of the file + pointers rewritten (round-trip tests A and B)
- [x] Speaker names: written inline in the text (`恭介「……ん？」`; English `Kyosuke: "…"`), no separate name field
- [x] Executable: every English change enumerated (strings, string pointers, `haff_opt`, font cells, advance, heap word, segment 9). Menu/system strings located
- [x] Font: 24×24, 4 bpp, font table at RAM `0x1AE3B0`, half-width cells at file `0x1B7D30`; char → glyph via `kanjiRomAdrOriginal` and the `haff_opt` list
- [x] **Spanish characters work** (proven in PCSX2): `haff_opt` moved to segment 9 with 16 stand-ins, accented glyphs in cells 77–92
- [x] Freeze cause: the heap-start word (RAM `0x1999DC`, ELF section `heap`) must be raised when overlays grow (confirmed)
- [x] The executable ships with a full symbol table and relocations (`tools/elf_symbols.py`)
- [x] Line width: 47 characters (the engine's own wrap drops a character, so we pre-wrap)
- [x] Space budget: in-place when a line fits; estimated O1 939 KB of 969 KB available (see Risks)
- [-] Double-byte (Shift-JIS) character → glyph mapping, kana cells: not needed, Spanish uses only half-width text
- Moved on: control-code meanings → Phase 3 (the checker only needs to preserve them); lines per page and dialogue window width → Phase 4 pilot; full playthrough of a large overlay → Phase 7

## Phase 3 — Tooling (Python, in `tools/`)
Already done: `iso_extract.py`, `iso_diff.py`, `bps_apply.py`, `iso_build.py` (append + in-place), `olm.py` (records, pointers, relocation), `exe_patch.py`, `charmap.py`, `elf_symbols.py`, `mips.py`.
- [x] Translation file format chosen and documented (KNOWLEDGE.md 4.10): one entry per block with `JA:` / `EN:` / `ES:`, only `ES:` is edited, codes re-attached automatically
- [x] `dump_script.py`: O0–O7 → 184 files / 33,000 entries in `translation/`
- [x] `insert_script.py`: charmap, pre-wrap at 47, **in place when the line fits, otherwise appended**, pointers rewritten (incl. mid-line and ending-code pointers), header sizes
- [x] **Round-trip tests** (`test_pipeline.py`): empty Spanish and ES = Japanese both give byte-identical files for all 8 scripts; an English-sized load fits (largest file 730 KB of 969 KB) with 0 pointer problems
- [x] `build.py`: source hash → lint → executable patches (heap `0x5D0000`, list, advance, pilot font) → scripts → ISO (executable in place) → check. Builds `build/MMM_es_pilot.iso`
- [x] `check.py`: lint translations (unsupported characters, stand-ins typed literally, codes, line breaks, long words, many-line warnings) and progress
- [x] `apply_translations.py`, `font_tool.py` (pilot font only); `check.py` is page-aware (narration page ≤ 10 lines) and `insert_script.py` supports `<PAGE>`
- [x] Experiment scripts removed from `tools/` (documented in LOG/KNOWLEDGE; in git history)
- [ ] Menu/system strings in the executable: dump and insert (including relocating long ones into segment 9, as the English patch does)
- [~] **Our own font** done in `tools/font_build.py` (DejaVu Sans Mono, 2026-10-26); waiting for the in-game test (`build/MMM_es_ownfont.iso`). Original item: `font_tool.py` **our own** glyphs for digits, letters, punctuation and accents (also add `%`, used for gauges at O0:0765/0775; check other symbols needed, e.g. `+ & # $`) (not the English patch's bitmaps). Needs an image library (Pillow) and a freely licensed font, or hand-drawn pixel art
- [ ] `bps_create.py`: make a BPS patch from original ISO → patched ISO
- [~] `build.py` builds the ISO in one command (done); still missing: writing the `.bps` into `patches/` and verifying it (needs `bps_create.py`)
- [x] Control codes documented (KNOWLEDGE.md and TRANSLATION_WORKFLOW.md)

## Phase 4 — Pilot
Goal: prove the whole pipeline end to end on a small slice before translating 100%.
- [x] Draft the **first scene**: O0 entries 1–82 (the whole opening narration + the morning scene with Reu), Spanish by Claude from the Japanese; **needs the user's review**
- [ ] Menus and system messages (executable strings) → still to do
- [x] Build, patch, and boot in PCSX2 (round 1, 2026-10-24): accents, commas, dots, `...`, `--`, 47-column wrapping, dialogue box and the Japanese scene change all work; **three narration pages (13, 13 and 11 lines) overflowed**: the game draws garbage from the 11th line
- [x] Measured: narration page = 10 lines; dialogue width 47
- [x] Round 2: accents and `ñ` confirmed on screen; the three overflowing pages were condensed instead of split (the user disliked half-empty pages)
- [ ] Check save/load screens and measure the dialogue box height (longest dialogue pages)
- [x] Honorifics decided (kept, 2026-10-25); names follow the English romanization (Haruna, Kyosuke…); onii-chan = "hermano"
- [ ] Still open: onomatopoeia/interjections, song lyrics and credits

## Phase 5 — Full translation
- [x] Workflow built (2026-10-24): `tools/batch.py`, agents `mmm-translator` + `mmm-reviewer`, skill `/translate`, rules in `docs/TRANSLATION_WORKFLOW.md`
- [x] First real batch with the workflow (O0 0083–0162): 17 of 80 lines corrected by the reviewer; user decisions applied (2026-10-25)
- [x] Story bible `docs/STORY.md` (seeded with O0 1–162) and read-ahead pass (`tools/scout.py` + `mmm-scout` agent + `/translate scout <script>`)
- [x] Scout O0 and settle its questions (2026-10-25). Next: continue batches in story order, a script file at a time
- [ ] Fill in the character and term glossary in `docs/STYLE_GUIDE.md` from the script
- [ ] Claude drafts Spanish script by script, in batches
- [ ] The user reviews each batch, and we track status per file in the table below
- [ ] Run `check.py` after every batch

| Script file | Lines | Drafted | Reviewed | Notes |
|---|---|---|---|---|
| _(filled in during Phase 3)_ | | | | |

## Phase 6 — Graphics with text (if any)
- [ ] Find images that contain Japanese text (title screen, menu labels, chapter cards)
- [ ] Decide which to translate, then edit and reinsert them

## Phase 7 — QA
- [ ] Full playthrough of every route (also confirms the big overlays fit in memory)
- [ ] Check for overflow, untranslated text, crashes, save compatibility
- [ ] Decide on credits and song lyrics (the English patch left both in Japanese)

## Phase 8 — Release
- [ ] Final `.bps` + hash list (input and output SHA-1, CRC32, MD5)
- [ ] Spanish README with patching instructions (Flips / MultiPatch / Rom Patcher JS)
- [ ] Credits: the translation team, and acknowledgement of the English patch as a reference
- [ ] Decide whether to publish (GitHub release with **patch only**, no game data or Japanese text)

---

## Open questions
- ~~Honorifics~~ Decided 2026-10-25: keep them; onii-chan = "hermano".
- ~~Name spellings~~ Follow the English patch's romanization (Haruna confirmed).
- Translate song lyrics and staff credits, or leave them like the English patch?
- Test on real PS2 hardware too, or PCSX2 only?
- ~~Is the font monospaced or proportional?~~ Answered: fixed width, 13 px per half-width character, 47 per line.

## Risks
| Risk | Impact | Mitigation | Status |
|---|---|---|---|
| ~~Unknown compression~~ | — | — | none exists |
| ~~No room in the font for accents~~ | — | `haff_opt` relocation + free cells | solved |
| O1 is close to its memory limit (939 / 969 KB estimated) | Spanish may not fit | pack moved lines into freed slots; or raise segment 9 / heap (check heap needs) | **checked 2026-10-26: fully translated O1 is 746,496 bytes and ends at 0x589A00, below the heap start 0x5D0000 (about 288 KB spare): fine** |
| Spanish runs longer than English; 47 characters per line | Overflow, more pages | pre-wrap + `check.py`; concise style | open |
| Shipping the English patch's glyphs | License/credit problem | draw our own font | planned |
| Large script volume (~33,000 records) | Long timeline | batch workflow + status table | open |
