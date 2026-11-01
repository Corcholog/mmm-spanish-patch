# My Merry May — Parche de traducción al español (work in progress)

A fan translation of **My Merry May** (PS2, KID, SLPS-25192) into **neutral Latin American Spanish**, translated from the Japanese script. It will be released only as a **BPS patch** that the user applies to their own copy of the game. This repository holds the tools, the documentation and the translation workflow. It contains **no game data** and, for now, **not the translation files** (see "What is not in this repository").

Inspired by the English patch: <https://github.com/pwnkyderedere/mmm-english-patch> (used only as a reference for meaning; the translation is made from the Japanese).

## Documentation

- [docs/PLAN.md](docs/PLAN.md): phases, tasks, progress and risks
- [docs/KNOWLEDGE.md](docs/KNOWLEDGE.md): what is known about the disc, formats, engine and tools, plus a ROM hacking glossary
- [docs/STYLE_GUIDE.md](docs/STYLE_GUIDE.md): translation rules, characters, terms glossary
- [docs/TRANSLATION_WORKFLOW.md](docs/TRANSLATION_WORKFLOW.md): how batches are translated and reviewed
- [docs/STORY.md](docs/STORY.md): story bible, updated after every batch (spoilers)
- [docs/LOG.md](docs/LOG.md): dated decisions and session history
- [docs/scouting/](docs/scouting): read-ahead notes per script file

## Status (2026-11-01)

| Script file | Entries | Translated |
|---|---|---|
| O0 (prologue and first days) | 5,939 | 100% |
| O1 (training, the contest, the festival routes) | 6,598 | 100% |
| O2 (Hitoe, Tae, the Repliss and Kyohei) | 4,713 | 100% |
| O3 – O7 | 11,885 | 0% |
| **Total** | **33,135** | **52.1%** |

Menus and system strings in the executable are still to do. In-game checks so far are done by the project owner in PCSX2; everything that was tested works (text, accents, own font, card names, menus, big-text screens).

## How the game and the patch work

- The disc image has one main executable (`SLPS_251.92`) and eight script files `OLM/O0`–`O7`. A script file is a short header, **bytecode** (a list of 32-bit instructions) and **text records** (Shift-JIS, NUL-terminated). Instructions point at text by RAM address (`0x4D3600 + file offset`).
- A translation moves text, never bytecode: Spanish text that fits stays in place, longer text is appended to the end of the file, and only the pointers that really point at text are rewritten. The pointer kind of every word is classified from the bytecode (`tools/olm.py`), because some words that look like pointers are really jumps or screen coordinates (this was a real bug: it broke every transition from O0 into O1).
- Spanish needs accented letters, which the engine cannot draw. The engine only draws half-width symbols that are in a list (`haff_opt`), so the build moves that list to a new memory segment, adds stand-in ASCII bytes for the accents (`tools/charmap.py`) and draws its own glyphs for them. The glyphs come from DejaVu Sans Mono (free licence, see `docs/fonts/`); only the rendered bitmaps go into the patch, never the font file.
- The text box is fixed-width: 13 px per half-width character, 46 visible columns and 4 rows for dialogue, 47 columns and 10 rows for narration. The build pre-wraps every line, because the engine's own wrap loses a character.
- Overlays share a heap; when a script grows past a limit, the heap start in the executable has to move (done: `0x5D0000`). The fully translated O1 ends at `0x589A00`, so there is room.
- Some texts are drawn by the executable itself (suit and card names in Indian poker, a few menu options, a few short strings). The build patches them in place or points the script at a Spanish copy.

Everything learned about the disc, the formats and the engine is in [`docs/KNOWLEDGE.md`](docs/KNOWLEDGE.md), the single source of truth for technical facts.

## Pipeline

```
original ISO (read-only, SHA-1 checked)
   │  tools/iso_extract.py, tools/dump_script.py
   ▼
translation/<script>/*.txt      one block per text: JA / EN reference / ES / NOTE   (local only)
   │  batch workflow: scout → translator → check → reviewer → check → apply
   ▼
tools/check.py + tools/screens.py     lint every entry and lay out every screen exactly as shipped
   │  tools/build.py
   ▼
build/*.iso (never published)  ──►  bps_create (planned)  ──►  patches/*.bps (the only thing released)
```

Main tools (`tools/`, run with `python -I -X utf8 tools/<name>.py` from the project root):

| Tool | What it does |
|---|---|
| `olm.py` | Reads script files: text records, pointer classification, relocation |
| `script_model.py` | Reads the bytecode: every text line in play order (voices, menus, windows, jumps, labels, gotos); groups lines that appear on one screen line, **following jumps** |
| `screens.py` | **Screen simulator**: rebuilds a script in memory and lays out every screen as the game will show it; reports overflows, glued words, blank menu options, Japanese left on screen |
| `insert_script.py`, `script_text.py`, `charmap.py` | Insert Spanish: wrapping, joins, stand-in bytes |
| `exe_patch.py`, `font_build.py` | Executable patches (heap, symbol list, font cells, card names) and the own font |
| `build.py` | Builds the ISO; `--start O1:2990` makes a **debug ISO** that starts a new game at any line |
| `savestate.py` | Refreshes a PCSX2 save state with the current text (debug) |
| `llm_batch.py` | Optional translator step through an LLM API (OpenCode: DeepSeek etc.), same checks and loop; the key comes from `OPENCODE_GO_API_KEY`, never from the repo |
| `check.py`, `batch.py` | Lint and the batch tool (`next`, `prefill`, `check`, `apply`, `status`) |
| `test_pipeline.py` | Round-trip tests: rebuilding with no translation gives byte-identical files; no non-text word ever changes |
| `export_public.py` | Builds and publishes this public copy: only tracked files, minus `translation/`, with safety checks and a no-reply author |
| `elf_symbols.py`, `mips.py` | The executable ships with a full symbol table; these look things up and disassemble small routines |

## Translation workflow and agents

Translation is drafted by Claude and reviewed by the project owner (the owner decides terms and style). Work goes in batches of about 300 entries, driven by three agents defined in [`.claude/agents/`](.claude/agents) and one skill, [`.claude/skills/translate`](.claude/skills/translate/SKILL.md):

1. **`mmm-scout`** reads a whole script file once and writes a read-ahead (`docs/scouting/<script>.md`): scene map, recurring terms, wordplay, formatting hazards and questions for the owner.
2. **`mmm-translator`** translates one batch from the Japanese within the line and page limits.
3. `batch.py check` runs the same checks the build uses (character set, codes, every screen).
4. **`mmm-reviewer`** reviews the batch line by line against the Japanese (fidelity, omissions, register, naturalness, glossary) and writes a corrected draft plus a report.
5. `batch.py apply`, then `check.py`; story notes go to [`docs/STORY.md`](docs/STORY.md) (story bible), decisions to [`docs/LOG.md`](docs/LOG.md), terms to [`docs/STYLE_GUIDE.md`](docs/STYLE_GUIDE.md).

Lessons built into the tools: identical Japanese lines are pre-filled with the existing Spanish (reviewers still check each copy in context, and very short lines are never copied); a sentence can continue across a jump in the script (a line can follow several different lines), so batches flag such joins; every text screen is checked by code before anybody plays it.

Details: [`docs/TRANSLATION_WORKFLOW.md`](docs/TRANSLATION_WORKFLOW.md).

## Key decisions

(Full list with dates and reasons in [`docs/LOG.md`](docs/LOG.md); style rules and the glossary in [`docs/STYLE_GUIDE.md`](docs/STYLE_GUIDE.md).)

- Translate from the **Japanese**; the English patch is reference only. Neutral Latin American Spanish (no regional slang: "papas", "lentes", "laptop", "salsa de soya"; "tú" between friends, "usted" where the Japanese is polite).
- Honorifics are kept (-san, -chan, -kun); onii-chan = "hermano"; names follow the English patch's romanization.
- Numbers: 0–9 as words, 10 and up as digits (except when the Japanese has digits).
- Mixed marks are written `¡¿...?!`.
- Narration and dialogue are pre-wrapped with real line feeds; every screen must pass `screens.py` with 0 errors.
- Own font, own build: nothing from the English patch's binary changes is reused.
- Never publish game data, the original or rebuilt ISOs, debug ISOs or save states.

## Repository layout

| Path | Contents |
|---|---|
| `docs/` | Plan, knowledge base, style guide, log, workflow, story bible, scouting notes, font licence |
| `tools/` | Python tools (above) |
| `.claude/agents/`, `.claude/skills/` | The agents and the `/translate` skill |
| `patches/` | Released `.bps` patches (none yet) |
| `translation/`, `work/`, `build/` | **Local only, not published** |

Requirements to run the tools: Python 3.12+, Pillow (for the font), your own legal copy of the disc image (SHA-1 `2f3864821f2a88f86bb5e004f383d63add82bde2`, the Japanese first-press limited edition), and a copy of DejaVu Sans Mono (see `docs/fonts/README.md`).

## What is not in this repository

- **Game data**: no ISO, no extracted files, no rebuilt or debug ISOs, no save states.
- **The translation files** (`translation/`): each entry stores the Japanese original next to the Spanish, so they stay local. The Spanish will reach players only through the BPS patch.
- Working files (`work/`) and build output (`build/`).

## Next steps

1. Scout and translate O3 – O7 (about 11,900 entries), then the menus and system strings in the executable.
2. Decide the songs and staff credits (translate or leave).
3. `bps_create.py` and the first release of a `.bps` with a README and credits.
4. Full playthrough QA in PCSX2.

## Legal

This repository contains **no game data**. You need your own copy of the game; only tools, documentation and (later) patch files are distributed. Not affiliated with KID or the original developers.

## Acknowledgements

The [English patch](https://github.com/pwnkyderedere/mmm-english-patch) by pwnkyderedere inspired this project and is used as a translation reference. Glyphs are rendered from DejaVu Sans Mono (see `docs/fonts/DEJAVU_LICENSE.txt`).
