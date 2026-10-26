# My Merry May — Spanish translation patch

Fan translation of *My Merry May* (PS2, KID, SLPS-25192) into **neutral Latin American Spanish**, distributed as a patch file (BPS) applied to the user's own ISO. Inspired by the English patch at https://github.com/pwnkyderedere/mmm-english-patch.

## Read first
- `docs/PLAN.md` — phases, tasks, current status. Update checkboxes as work completes.
- `docs/KNOWLEDGE.md` — everything learned about the disc, file formats, engine, tools. **Source of truth for technical facts.**
- `docs/STYLE_GUIDE.md` — translation rules and character/term glossary.
- `docs/LOG.md` — dated decisions and session log.
- `docs/TRANSLATION_WORKFLOW.md` — how batches are translated and reviewed (rules for the `mmm-scout`, `mmm-translator` and `mmm-reviewer` agents in `.claude/agents/`; `/translate scout <script>` once per script file, then `/translate <script>` per batch).
- `docs/STORY.md` — story bible (what has happened, running motifs), updated after every batch; `docs/scouting/<script>.md` — read-ahead per script file.

## Documentation rule (user requirement)
The user wants everything documented, both as memory for Claude and as a learning resource for them.
- Every finding about a format, offset, encoding, or engine behavior goes into `docs/KNOWLEDGE.md` as soon as it is confirmed. Mark unconfirmed guesses as **(unverified)**.
- Every decision (and its reason) goes into `docs/LOG.md` with the date.
- Explain jargon the first time it appears; the user is learning ROM hacking through this project.
- Keep `docs/PLAN.md` status accurate at the end of each session.

## Hard rules
- **Never commit or publish game data**: no ISO, no extracted files, no rebuilt ISO. `.gitignore` covers `*.iso`, `work/`, `build/`.
- The original ISO in the project root is **read-only**. Never modify it in place; always write to `build/`.
- `translation/` contains Japanese source text next to the Spanish. That's fine for this local repo, but it must be stripped (or the repo kept private) before anything is pushed to a public remote.
- Verify the input ISO hash before building: SHA-1 `2f3864821f2a88f86bb5e004f383d63add82bde2`.

## Decisions so far
- Translate from the **Japanese** script, using the English patch only as a reference for meaning.
- **Claude drafts** the Spanish; the **user reviews**.
- Variety: **neutral Latin American Spanish** (see style guide).
- Local git repo; no remote yet.

## Layout
| Path | Contents | Tracked |
|---|---|---|
| `docs/` | Plan, knowledge base, style guide, log | yes |
| `tools/` | Python scripts (extract, dump, insert, build) | yes |
| `translation/` | Per-script translation files (JA + EN ref + ES) | yes (local only) |
| `patches/` | Released `.bps` patches | yes |
| `work/` | Extracted disc files, scratch | **no** |
| `build/` | Rebuilt ISOs | **no** |

## Environment
Windows 11, PowerShell + Git Bash. Python 3.14 (`python`), git 2.55, Node, .NET available. PCSX2 v2.4.0 is installed (`C:\Program Files\PCSX2\pcsx2-qt.exe`) with the user's BIOS; **the user runs all in-game tests and reports back with screenshots**. Run Python tools with `python -I -X utf8 tools/<script>.py` from the project root.

## Key facts for every build (details in KNOWLEDGE.md)
- Write `SLPS_251.92` **in place** in the ISO (`build_iso(..., in_place=['SLPS_251.92'])`).
- If any `OLM/O*` grows past RAM `0x560D00`, **raise the heap start** (`exe_patch.set_heap_start`), or the game freezes.
- Half-width symbols only draw if listed in `haff_opt` (relocated to segment 9 by `exe_patch.set_haff_list`); Spanish letters go through `tools/charmap.py`.
- Narration lines are 47 characters, dialogue-box lines 46; pre-wrap (the tool does it), never rely on the engine's wrap. Dialogue pages hold 4 lines, narration pages 10.
- The executable has a full symbol table: look things up with `tools/elf_symbols.py` before reverse-engineering by hand.
