# Knowledge base

Everything we've confirmed about the game, the disc, the formats, and the tools. Facts we haven't confirmed yet are marked **(unverified)**. Each section notes where its information came from.

Last updated: 2026-10-24 (end of Phase 1).

---

## 1. The game

| Field | Value | Source |
|---|---|---|
| Title | My Merry May (マイ・メリー・メイ) | EN patch README |
| Developer | KID | EN patch README |
| Platform | PlayStation 2 | EN patch README |
| Serial | SLPS-25192 | EN patch README, `SYSTEM.CNF` |
| Edition of our dump | 初回限定版 (Shokai Genteiban, "first-press limited edition") | ISO filename |
| Genre | Visual novel | — |
| Setting (from opening script text) | A run-down school dormitory ("Ami Dorm", 阿見寮) attached to a prefectural high school; first-person narrator. EN patch names characters "Kyosuke" and "Reu" | O0 script text |

## 2. Our disc image

File: `My Merry May (Japan) (Shokai Genteiban).iso` (project root, **read-only**)

| Property | Value | Verified by us? |
|---|---|---|
| Size | 1,738,833,920 bytes (= 849,040 sectors × 2048) | yes (2026-10-24) |
| SHA-1 | `2f3864821f2a88f86bb5e004f383d63add82bde2` | yes (2026-10-24) |
| CRC32 | `86616ECF` | The BPS applier checked the source CRC32 stored in the English patch and it matched, but we haven't compared it to this README value |
| MD5 | `8bae301ad49c4cea125d08578b16a2a5` | no (from EN README) |
| Filesystem | ISO 9660, volume ID `MY_MERRY_MAY`, 547 files | yes |
| `SYSTEM.CNF` | `BOOT2 = cdrom0:\SLPS_251.92;1`, `VER = 1.03`, `VMODE = NTSC` | yes |

This matches the base disc of the English patch exactly.

Note on names: files on this disc have no extensions, and some names end in a dot (`OLM/O0.`, `A000/A014.`). That's normal for ISO 9660. Our tools strip the `;1` version suffix and Windows drops the trailing dot when extracting (`OLM\O0`).

### 2.1 What is on the disc
The full list (path, LBA, size) is in [disc_file_table.tsv](disc_file_table.tsv). Summary:

| Path | Files | Size | What it is | Confidence |
|---|---|---|---|---|
| `SYSTEM.CNF` | 1 | 57 B | PS2 boot config | confirmed |
| `SLPS_251.92` | 1 | 7.2 MB | The game program: a PS2 **ELF** executable (entry point `0x100008`). Contains the engine code, menu strings and the **font** | confirmed (ELF); menu strings and font from the English diff |
| `MODULES/` | 13 | 0.6 MB | Sony IOP driver modules (`.IRX`, e.g. SIO2MAN, PADMAN, LIBSD, MCMAN) plus `IOPRP254.IMG`. Standard system libraries | likely; **unchanged** by the English patch |
| `OLM/O0`–`O7` | 8 | 2.8 MB | **The story script.** Eight overlay modules of Shift-JIS text and tables. See section 4.3 | confirmed |
| `A000/` | 32 | ~642 MB | Graphics and related data: many files hold **TIM2** images (the PS2 texture format), plus larger `ogdt` containers and data I haven't identified | partly identified; **unchanged** by the English patch |
| `A020/` | 3 | 24 MB | `ogdt` containers, same header as `A000/A01D` | likely graphics |
| `A040/` … `A220/` (16 folders) | 483 | ~21 MB | Groups of small `IECSsreV` headers (a Sony sound bank header, "SCEIVers" stored reversed) next to larger files that start with zeros. Looks like sound banks (header + data) | **(unverified)** probably voice/sound effects |
| `A240/` | 2 | 100 MB | MPEG program streams (`00 00 01 BA`): **video** (movies) | likely |
| `A980/` | 4 | 938 MB | Unidentified very large files. 91% of the disc | **(unverified)** unknown |

### 2.2 What the English patch changed (key finding)
Applying the English `.bps` to a copy of our ISO and comparing the two discs **file by file** (`tools/iso_diff.py`, full report in [diff_original_vs_english.tsv](diff_original_vs_english.tsv)) shows only **9 of 547 files differ**:

| File | Original size | English size | What happened |
|---|---|---|---|
| `OLM/O0` | 510,976 | 712,960 | Content changed, grew, **moved to the end of the disc** |
| `OLM/O1` | 579,328 | 749,312 | same |
| `OLM/O2` | 381,824 | 497,920 | same |
| `OLM/O3` | 353,152 | 466,304 | same |
| `OLM/O4` | 305,792 | 406,912 | same |
| `OLM/O5` | 315,776 | 422,528 | same |
| `OLM/O6` | 180,992 | 233,984 | same |
| `OLM/O7` | 152,576 | 204,032 | same |
| `SLPS_251.92` | 7,165,028 | 7,165,028 | Content changed, **same size, same position** |

Consequences:
- **All text is in two places: the script files (`OLM/`) and the executable.** The English team did not touch any of the images, sound, or video. So the title screen, menu graphics and so on, stay Japanese in the English release (to be checked in Phase 6).
- The English ISO is 3,702,784 bytes (1,808 sectors) larger than the original: the grown `O` files were **appended after the original end of the disc** (LBAs 849,040 and up). The old copies are left in place as dead data.
- The executable contains **no new disc positions** for the moved files (we searched for the new LBAs as 32-bit numbers and found none), so the game almost certainly **opens files by name** through the ISO filesystem. That means we're free to enlarge and relocate files as long as the directory entries are right. (Matches of the *old* LBA values in the original executable were found, but those locations were not modified by the English patch, so they're probably coincidences. **unverified**)

### 2.3 Rebuild strategy (how the English patch did it, and how we'll do it)
Same as theirs: write the modified file at the end of the image, update its directory record (LBA and size) in the ISO's directory table, update the total sector count in the volume descriptor, then produce a BPS of original → patched. We'll write that tool in Phase 3.

## 3. The English patch (reference)

- Repo: https://github.com/pwnkyderedere/mmm-english-patch
- Ships a single `MyMerryMay_EN.bps` plus `HASHES.txt`. **No game data and no tools** are published, so we can't reuse their extraction code.
- BPS file: 3,723,175 bytes. Downloaded to `work/english_patch/` (untracked).
- Our own `tools/bps_apply.py` applies it correctly: the output's SHA-1 equals the value in the English README (`6d697508ce87240dc8ab6cb2bcc71944beeadc00`), and the source, target and patch CRC32 checks all pass.
- Translated: full story, menus, save/load messages, options, chapter and scene titles, plus a new smaller English font with proper punctuation.
- Not translated: staff credits, song lyrics, and a few interjections ("a...", "sono,").
- Known issue: on a blank memory card the game says the system file is missing. Press ✕, then save from the System Data menu once.
- They haven't done a full playthrough, so layout problems in later scenes are possible.

**How we use it:** the English-patched files (`work/english/`, untracked) are a map of where text lives and a second opinion on meaning.

## 4. File formats

### 4.1 Containers
- The script files (`OLM/O0`–`O7`) are **standalone**: no archive wrapper, no compression.
- The `A***` groups are not investigated yet (not needed for text, but needed if we translate images in Phase 6).

### 4.2 Compression
- `OLM/O*`: **none.** Byte entropy is about 4.8 bits per byte (compressed data sits near 8) and Japanese text is directly readable.
- The executable is a plain ELF; no compression seen.

### 4.3 Script files `OLM/O0`–`O7`

**Overlay modules.** They are loaded into the console's RAM at a fixed address, `0x4D3600`, one at a time (the executable's program headers list all 8 at the same address, see 4.5). They hold both script text and binary tables.

**Header (first 0x100 bytes)**, shown for O0 (little-endian 32-bit words):

| Offset | Original O0 | English O0 | Meaning |
|---|---|---|---|
| 0x00 | `MWo3` (`4D 57 6F 33`) | same | Magic |
| 0x04 | 1 | 1 | Module number (O1 = 2, …) |
| 0x08 | `0x4D3600` | same | RAM load address |
| 0x0C | `0xC0` | same | unknown **(unverified)** |
| 0x10 | `0x7CB00` | `0xAE000` | Size of body = **file size − 0x100** (checked on O0 and O1, both versions) |
| 0x18 | `0x550200` | `0x581700` | End address in RAM = load address + file size (checked) |
| 0x1C | `0x550200` | `0x581700` | same value again |
| 0x20 | `o0` | same | Module name tag (`o1`, `o2`, …) |
| rest | zeros | zeros | padding up to 0x100 |

So **when the file size changes, 0x10, 0x18 and 0x1C must be updated.** The English patch does it.

**Body (from 0x100): text records.**
- Text is **Shift-JIS** in the original and plain **ASCII** in the English patch (same record layout).
- Each text record starts on a **4-byte boundary**, directly after a NUL, and is padded with zeros to the next 4-byte boundary. Long records usually end up 16-byte aligned, but short ones (like `\k\p`) are packed one after another. Most records are a line of text followed by control codes. Example, original O0 at 0x100: `\FS` + 「学校の裏山の一部を切り開いたこの学生寮は…」+ `\FE\t60` + newline.
- Control codes are written as backslash sequences in the text. Counts in original O0:

| Code | Count | Probable meaning **(all unverified)** |
|---|---|---|
| `\k` | 5,726 | wait for button press |
| `\p` | 5,675 | new page / clear the text box |
| `\t60` | 40 | wait 60 ticks |
| `\FS` … `\FE` | 36 pairs | special text style (used for the opening narration) |
| `\O`, `\P`, `\S`, `\M`, `\R`, `\T`, `\LC`, `\CG…`, `\o` | few | scene commands (background/CG/music/...?) |

**Structure of the opening of `O0` (original), from the pointer table at `0x5D6C`:**
- The game opens with a long **narration** (the description of the dormitory): about 50 records, every one starting `\FS` and ending `\FE\t60` followed by a newline, **except the last record of each page, which ends `\FE\t60\k\O`**. The pages end at records `0x1D0`, `0x350`, `0x550`, `0x6C0`, `0x7F0`, `0x8A0`, `0xA40`, `0xBD0` (8 pages). So the reading is: `\FS … \FE` = narration text style; `\t60` = wait 60 ticks; `\k` = wait for a key; `\O` = end of narration page **(all unverified)**.
- Normal **dialogue** starts at record `0xC30`: plain text (no `\FS`) ending `\k\p`, e.g. `恭介「……ん？」\k\p`. `\k\p` = wait for a key, then clear the page.
- The bytecode groups records: `OP5D n` followed by `{pointer,0,0,index}` entries, then `OP5D 4` + `OP4B`. A group corresponds to one narration page (3–6 entries).
- **Retracted (2026-10-24):** I earlier blamed several freezes on text content (a bare `\k` at the end of a record; plain text inside the narration; a label like `S1` right after `\FS`). **None of these was proven**, and the real cause turned out to be memory (see 4.5, the word at RAM `0x1999DC`). Still good practice: keep each replaced record in the style of its section and end it like the original does.

- The English text puts the speaker's name inline: `Kyosuke: "…"\k\p`. How the original Japanese marks speakers is still to be checked.
- Each text record is a **NUL-terminated string**. Padding zeros follow up to the next 4-byte boundary. A record often ends with `\FE\t60\n` or `\k\p` (the `\n` seen before the NUL is a literal line-feed byte, 0x0A).
- Original `O0` has **5,932 text records** that something points at (found by `tools/olm.py audit`).

**What a "pointer" is, with a real example.** A script command that says "show this text" has to say *which* text. It does that with an address: the number of the memory location where the text sits. The game loads `O0` into RAM starting at address `0x4D3600`, so the text at position `0x100` of the file is at address `0x4D3600 + 0x100 = 0x4D3700` while the game runs. The script stores that address as a 4-byte number, `00 37 4D 00` (bytes are written backwards, "little-endian"). That number is a pointer. In original `O0` at file offset `0x5D6C` there is exactly this pointer, and the Japanese opening line (「学校の裏山の一部を…」) is what it points at. In the English `O0` the same 4 bytes at `0x5D6C` read `00 02 55 00` (= `0x550200` = `0x4D3600 + 0x7CC00`), pointing at the English line appended at the end of the file. If we move a line and forget to change the pointer, the game would read whatever is left at the old address (nothing, after we zero it). That is why every pointer to moved text must be rewritten, and why we audited that we found all of them.

**Binary regions inside the same file (the script bytecode).** Between blocks of text there are binary regions (the first ones in original O0 are at 0x5D00, 0x5E80, 0x6730, 0x7A80). They are made of **32-bit little-endian words**:
- Words with `0xF0` in the top byte, e.g. `0xF000006C`, `0xF0000012`: **opcodes** (the low byte is the command number). Seen so far: `0x08`, `0x0A`, `0x12`, `0x13`, `0x15`, `0x2F`, `0x31`, `0x32`, `0x33`, `0x34`, `0x37`, `0x3B`, `0x43`, `0x44`, `0x4B`, `0x5D`, `0x6C`. Meanings are **unknown**.
- Words in the range `0x4D3700` to `0x4D3600` + file size are **pointers** to somewhere inside the overlay (RAM address = `0x4D3600` + file offset). Text pointers appear in 16-byte entries `{ pointer, 0, 0, index }` with the index counting up (0, 1, 2, …) after an opcode `0xF000005D` (e.g. from 0x5D6C onward). One pointer also appears as an argument of opcode `0x37` (at 0x6824, pointing to 0x1E20).
- Original `O0` contains **5,938 pointer words that target text** (5,935 distinct targets: 5,932 record starts and 3 pointing into the middle of a record) and **72 that target bytecode** (all 72 inspected: opcode words such as `0xF000006C`, so jump or call targets). All 4-byte aligned. Checked against the English answer key: all 2,283 pointers the English patch changed are in our list, none missing.
- Pointer-like values also occur by coincidence at offsets that are **not** 4-aligned (opcode words end in `00 F0` and are followed by small arguments, so neighbouring words can spell an address). Those are not pointers.

**How the English patch inserted its text (answer key).** Comparing the original and English `O0`:
- The bytecode regions are at the **same offsets** in both files (checked for all regions up to about 0x2C000). Only the text changed.
- Lines whose English fits the original record slot were written **in place**. Lines that didn't fit were **appended to the end of the file** (from offset `0x7CC00`, the original file size; **2,282 records** there) and their pointers were rewritten: exactly **2,283 pointer words differ** between the two files, and every one now points into the appended area. The first 0x500 bytes of English `O0` (the original text slots, all relocated) are zeroed.
- So the English files grew by simply appending text. Nothing else moved.

**Insertion method we can use** (implemented in `tools/olm.py`; being proven by the PCSX2 round-trip tests, see 4.8): leave all bytecode where it is, write every translated record at the end of the file (16-byte aligned, NUL-terminated), and rewrite every pointer that targets a text record (including the 3 that point into the middle of one). Then update the header size fields (0x10, 0x18, 0x1C) and round the file size up to a multiple of 0x100. Simplest is to always relocate all text, not just the lines that don't fit. The abandoned old slots are zeroed.

**Line wrapping.** English text is wrapped with **runs of spaces** (for example `...fills with the scent   of trees every morning...`), so the engine does not seem to wrap words itself; it wraps at a fixed width and the translators pad lines by hand. The original Japanese has no manual line breaks. **(unverified: the exact width and how the engine counts it; to be measured)**

**Instruction forms (2026-10-26, read from the bytecode of O0-O7; `olm.site_kind`, `tools/script_model.py`).** A text line is not printed by an opcode: it is its own 4-word instruction.

| Form | What it is | Count |
|---|---|---|
| `<pointer>, 0, 0, <serial>` | a text line; the serial counts up within a scene (restarts about 44 times in O0) | O0 5,902 |
| same, pointer into the executable (RAM `0x30C800`-`0x30CC00`) | a short string from SLPS_251.92 (`\k\p`, `⏎⏎⏎⏎`, `あ……`, `その、`, `ふむ。`, `。\k⏎`...) | O0 10 |
| `F0000000, <n>, <pointer>` | a menu option (consecutive ones = one menu). **The pointer can also go to the executable's string pool** (`0x30C800`-`0x30CC00`): the Indian-poker option 降りる (fold) is one; O0 1, O1 5, O2 3 (names), O4 2. Handled as `X` entries like the exe text lines | O0 31 (+1 exe) |
| `F000000D, <char>, <clip>` | voice clip for the next line; char 2 Kyosuke, 3 Reu, 4 Lease, 5 Hitoe, 6 Motomi, 7 Tae, 8 Misao, 9 Ryo, 10 Kyohei, 0 extras | O0 ~1,980 |
| `F000005D 3` / `F000005D 4` | narration (`\FS`) window open / close | O0 148 / 148 |
| `F000006C ...` | scene start (every jump target) | |
| `F0000008 <n>` / `F000000B <n>` | label n / goto label n, local to a scene (every goto has exactly one label in its scene: checked in O0-O7). Conditional branches (`F0000048 0 2 <n>`, `F0000055 0 2 <n>`...) also go to labels. **A sentence can continue across a goto**: O0 has three random reactions before the card reveal (5781+5782, 5783+5784, 5785+X004), each ending with an interjection that leads into 5786 "レゥの手は、". `script_model.chains()` follows gotos, so such a line is in several chains; `branch_joins()` lists them (O0 2, O1 12) | O0 260 labels, 104 gotos |
| `F0000006, <module>, <address>, x` and `F0000048 a, b, <module>, <address>` | **jump into another script file** (module 0 = O0); the address belongs to that file, so it only looks like a pointer into this one | 16 + 8 |
| `F000002E/31/3C/45/6E` arguments such as `0x4FFC64` | screen coordinates that look like pointers | 81 (O2, O3, O5) |
| `F0000054 2, <value>` | the game draws a card name into the text here (Indian poker; executable `oscrRrnd`: suit string + `%s %d` or `%sＪ/Ｑ/Ｋ/Ａ` for 11-14; our build: `%d de %s`, `jota/reina/rey/as de %s`, see `exe_patch.set_card_formats`); `F0000054` with other first arguments draws card graphics | O0 several |
| `F0000065 <pointer>, 0, size, 0, 0x21` / `F0000061 a, b, <pointer>` | O7 staff credits / O4-O6 chapter titles | 709 / 3 |

**Bug found and fixed 2026-10-26: the build rewrote jumps.** `olm.analyze` accepts every word that looks like a pointer into a text record. The 5 jumps from O0 into O1 (O0 `0x64bd4`, `0x64dd8`, `0x681f8`, `0x68338`, `0x6da44`) happen to land inside O0 text, so every Spanish build until then rewrote them, and each transition O0 -> O1 would have jumped to garbage. (The English patch has the same bug at `0x64dd8`.) Now only `olm.TEXT_KINDS` (text, menu, credits, title) are rewritten; jumps, coordinates and data stay as they are, and a pointer-like word of an unknown form stops the build (`olm.UnknownPointer`). Two O0 entries that existed only because of those false pointers (`0281.2`, `1556.2`) were merged back; `2728.2` is a real pointer into the middle of a record (the game prints that half on its own later). test_pipeline tests 4 and 5 pin this.

**PCSX2 save states (.p2s, checked on v2.4.0, 2026-10-26).** A zip whose members are compressed with zstd (method 93; Python 3.14's `zipfile` reads and writes it): `eeMemory.bin` (32 MB main RAM), `iopMemory.bin`, `GS.bin`, `SPU2.bin`, register files and `Screenshot.png`. The script file being run is in RAM at `0x4D3600` (header `MWo3`); a state from O0 matched all 7,169 O0 opcode words. The text of the box on screen also sits in other buffers (`0x314F05`, `0x4CDA69`: the current box and the message history), which a refresh does not change. The interpreter's position was not found in plain RAM (`scr_execPoint` at `0x30CDBC` was 0; it is probably kept in the script thread's registers), so states cannot yet be created at an arbitrary line: use `build.py --start` for that.

**Not yet known:** what each opcode does; how choices and branching work; how speaker names are shown in the Japanese script; whether pointers can also live at unaligned offsets. The other seven files (O1–O7) are assumed to use the same format (same header magic) but haven't been analysed.

### 4.4 Text encoding
Shift-JIS for Japanese (we decode with Python's `shift_jis` codec and get clean text). The English patch uses ASCII for English text.

### 4.5 The executable `SLPS_251.92`

ELF32, little-endian MIPS, entry point `0x100008`. It has 10 program headers (segments = chunks of the file copied into RAM at start):

| Seg | File offset | RAM address | In-file size | In-RAM size | Notes |
|---|---|---|---|---|---|
| 0 | 0x180 | 0x100000 | 0x20CB00 | 0x3D3600 | Main program: code and data. RAM size ends exactly at `0x4D3600` where overlays start |
| 1–8 | 0x20CC80 (dummy) | 0x4D3600 | 0 | 0x7CC00, 0x8D700, 0x5D380, 0x56380, 0x4AA80, 0x4D180, 0x2C300, 0x25400 | Reserve RAM for overlays O0–O7. In-RAM size = exact size of the original O file (0x7CC00 = 510,976 bytes = O0 ✓) |
| 9 | 0x20CC80 (dummy) | 0x560D00 | 0 | 0 | **Empty** in the original (placed right after the biggest overlay) |

What the English patch did to this:
- **Segments 1–8 were left alone**, even though the overlay files grew. So the in-RAM size values there are *not* limits the engine enforces (or at least it works with larger files). **(unverified in emulator)**
- **Segment 9 was repurposed** as a new data segment: file offset `0x618EC0`, RAM address `0x5C0000`, size `0x1240` (4,672 bytes), holding **English menu/system strings that don't fit in the original string slots**.
- A **table of string pointers** around file offsets `0x09D164`–`0x09D69E` was edited: many pointers that originally pointed to Japanese strings near RAM `0x307B30` now point into the new segment at `0x5C0xxx`. This is the technique for longer system text: add a segment, redirect pointers.
- The other small edits are now understood (disassembled with `tools/mips.py`):
  - `0x4ACEC`, `0x4AD28`, `0x7F8F0`, `0x9610C`: each is a `lui`/`addiu` pair loading the address of a menu string into a register before calling the string-draw function (`jal 0x121FE0` and similar). The English patch changed the address from the Japanese string (`0x31xxxx`) to the English one in the new segment (`0x5C0xxx`). This is how one menu string gets redirected.
  - `0x99B5D` (2 bytes): a data word at RAM `0x1999DC` changes from **`0x560D00`** (exactly the end of the largest overlay, O1) to **`0x5D0000`** (just above the new segment, which ends at `0x5C1240`). Most likely the "start of free memory / heap" address (the code that reads it was not found; it is probably reached through a base register). **CONFIRMED NECESSARY by testing (2026-10-24):** builds with a relocated `O0` ending at ~`0x5A1F00` froze hard (FPS 0) on New Game in most cases; the same builds with only this word raised to `0x5D0000` run normally (bisect C → C2, D → D2). Without it, our larger overlay overwrites live memory above `0x560D00`, and whether it freezes depends on exactly which bytes land where. (The round-trip test B worked by luck.) **Rule: whenever any overlay ends above `0x560D00`, raise this word above the largest overlay end (the English value `0x5D0000` covers overlays up to `0x5D0000`).**
  - Complete list of the English patch's executable changes (enumerated 2026-10-24): program header for segment 9; the advance byte; this word; string-pointer redirects (`lui`/`addiu` pairs and several pointer tables: chapter/scene titles at `0x9D164`–`0x9D69E`, menus at `0xA84F4`, `0x1D2C54`, `0x1FBD58`–`0x1FC4B6`, `0x205130`–`0x2051D6`, `0x20CA10`); strings translated in place (`0x1D1560`…, ending texts `0x1D23C0`…, memory-card and system messages `0x208E10`–`0x2098AB`, options `0x20C1A0`); the new strings at file `0x618EC0`; and font cells 0–67, 69–76. **There is no character-mapping table among them.**
  - `0xA84F4`, `0xA8508`: more entries of the string-pointer table (a table of RAM addresses of strings, in the data area at about RAM `0x1A836C`).
  - `0x2A794` (1 byte): `addiu $v0,$v0,12` becomes `addiu $v0,$v0,13`: the half-width character advance, see 4.6.

The executable has 15,652 changed bytes in total: about 1,400 in the edits above and the rest in the font (cells 0–76).

### 4.6 Font

> **Current understanding (2026-10-24, from the game's own symbol table, see 4.9). This box supersedes the older notes below where they disagree.**
> - **One big font table** of 24×24 4-bit glyphs (288 bytes each) starts at RAM **`0x1AE3B0`** (file `0xAE530`). The function **`kanjiRomAdrOriginal`** (RAM `0x13B590`) returns the address of a character's glyph.
> - **Half-width (ASCII) glyphs** are font entries **3776 + cell**: cell 0–9 = `0`–`9`, 10–35 = `A`–`Z`, 36–61 = `a`–`z` (computed: `a` → entry `c + 3715`), and **cell 62+i = the i-th character of `haff_opt`**. So "cell 0" is at file **`0x1B7D30`**. (My earlier origin `0x1B7D44` was 20 bytes off; copies between files with the same grid were unaffected.)
> - **`haff_opt`** (RAM `0x30C798`, file `0x20C918`) is the **list of allowed half-width symbols**: `?!'"() ` in the original (declared 8 bytes). The English patch writes 15: `?!'"() .,-:;/*~`, overflowing into the variables `A982_VHC`/`A983_VHC`. The lookup loops `i < strlen(haff_opt)`, compares the byte with `haff_opt[i]` (signed `lb`, so list entries must be ASCII), and returns entry `3838 + i`. **Any other half-width character returns 0 and is dropped by the parser** (it doesn't appear on screen or in Message History). This is why `#$%&…`, and in our early builds `. , - :` etc., vanished: we had copied the English glyphs but not the English list.
> - The two instructions that load the list address are `addiu $v0,$gp,-32728` at RAM `0x13BBF8` and `addiu $a0,$gp,-32728` at `0x13BC38` (`$gp` = `0x314770`).
> - **`isHankaku`** (RAM `0x1293C0`): every byte 0x20–0x7E is a one-byte half-width character; bytes ≥ 0x80 start a two-byte Shift-JIS character (so half-width katakana bytes are swallowed in pairs).
> - **✅ CONFIRMED IN PCSX2 (2026-10-24, `MMM_accent_test.iso`):** all 16 Spanish characters (`á é í ó ú ñ ü Á É Í Ó Ú Ñ Ü ¿ ¡`) and the punctuation `. , - : " ( )` display on screen and in Message History. Spanish is technically possible with no engine code changes beyond the list relocation.
> - **Method (proven):** move the list into segment 9 at RAM `0x5C0000` (64 KB-aligned so each load becomes one `lui reg, 0x5C`), extend it with 16 stand-in ASCII symbols for `á é í ó ú ñ ü Á É Í Ó Ú Ñ Ü ¿ ¡` (`tools/charmap.py`), and draw those letters in cells 77–92 (free in both fonts). Translators write normal Spanish; the build converts it.
> **Our own font (2026-10-26).** `tools/font_build.py` renders every half-width cell from **DejaVu Sans Mono** (Bitstream Vera licence + public-domain changes; licence text in `docs/fonts/DEJAVU_LICENSE.txt`; the font file itself is local-only, see `docs/fonts/README.md`; only the rendered bitmaps end up in the patch). Size 20 px (advance 12.04 px, game advance byte 13), baseline on cell row 19 like the English font, glyphs start at column 1, pixel levels 0-5 from the anti-aliasing (`round(alpha*5/255)`). It draws cells 0-61 (digits, letters), 62-76 (the 15 base symbols), 77-92 (the 16 Spanish letters, drawn directly from the font instead of composed) and **93 = `%`** (`charmap.EXTRA_SYMBOLS`, so `haff_opt` has 32 entries). Space is cell 68 (blank). `build.py` uses it by default (`--font english` is the old pilot). Preview: `python -I -X utf8 tools/font_build.py preview` -> `work/font_preview.png`. **Verified only in the preview image, not yet in game (unverified).**

**Format (decoded 2026-10-24).** The glyph images are in the executable. Each glyph ("cell") is **24 × 24 pixels at 4 bits per pixel, 12 bytes per row, 288 bytes per cell**; the low nibble is the left pixel of each pair. Pixel values are **0–5** (0 transparent, 5 full: an anti-aliased font with 6 levels). My first renders failed because I started the cell grid a few bytes too early; the grid origin that gives clean glyphs is **file offset `0x1B7D44`** (RAM about `0x2B7BC4`), cell *k* at `0x1B7D44 + 288·k`. The exact origin is only known to within a few bytes (anything from `0x1B7D42` to `0x1B7D47` gives the same compact glyphs, because glyphs have blank margins); copying whole cells between files with the same origin is safe regardless.

**Cell order is not ASCII order.** In the English font: cells 0–9 = `0 1 2 3 4 5 6 7 8 9`, 10–35 = `A–Z`, 36–61 = `a–z`, then punctuation. In the original Japanese font the same cells hold the **full-width** (24 px wide) versions of those characters.

**Occupancy map (cell numbers relative to `0x1B7D44`):**

| Cells | Original | English patch | Notes |
|---|---|---|---|
| −120 … −23 | glyph data | unchanged | what these are is not yet identified |
| −22 … −1 | empty | unchanged | |
| 0 … 67 | full-width digits, letters, a few symbols | replaced with narrow Latin glyphs | |
| 68 … 94 | empty | cells 69–76 filled; **68 and 77–94 empty** | 27 cells, 18 of them still free in the English font |
| 95 … 180 | glyph data | unchanged | probably kana; not yet identified |
| 181 … 190 | empty | unchanged | |
| 191 … | not font-like data | unchanged | other data |

**English punctuation in cells 62–76 (identified by looking at the glyphs):** `?`(62) `!`(63) `'`(64) `"`(65) `(`(66) `)`(67) space(68, blank) `.`(69) `,`(70) `-`(71) `:`(72) `;`(73) `/`(74) `*`(75) `~`(76).

**Hypothesis (historical: disproved, the real mechanism is the `haff_opt` list in the box above; the test script was removed, see LOG):** the engine's built-in ASCII path maps the **95 printable ASCII characters onto cells 0–94**: 62 alphanumerics, then the 33 symbols onto cells 62–94 in an engine-defined order. The 15 symbols above sit in cells 62–76; the remaining 18 symbols (`# $ % & + < = > @ [ \ ] ^ _ ` { | }`) would map to the blank cells 77–94. If true, those 18 cells can be filled with accented letters (á é í ó ú ü ñ Á É Í Ó Ú Ñ ¿ ¡ …) and Spanish text can use those 18 ASCII bytes as stand-ins, with no engine code change and the correct half-width spacing.

**Advance width (how far the cursor moves after a character).** The layout routine at RAM `0x12A5F0`–`0x12A62C` (file `0x02A770`) reads a flag byte from the character record: for **half-width** characters (ASCII) the advance is `size·11 + 12` pixels, for **full-width** it is `size·11 + 24` (`size` = low 4 bits). The English patch changes the `12` to `13` (file offset `0x2A794`, one byte). So ASCII text is **fixed width** (12–13 px per character), not proportional, and full-width kana/kanji take 24 px. This matches the English files being hand-wrapped with runs of spaces.

**What the English patch did *not* do:** it changed no text-decoding code. The engine already draws ASCII; the English team only replaced glyph pictures (cells 0–76), redirected menu string pointers, and changed the one advance constant.

**Still unknown:** which ASCII symbol maps to which of cells 77–94 (test pending); how double-byte (Shift-JIS) characters map to cells (probably via the segments at −120 and 95–180 and further data); whether single-byte half-width katakana (`0xA1`–`0xDF`) are drawn; where the 24 px height sits relative to the text line.

### 4.9 The executable ships with debug information
`SLPS_251.92` was built with Metrowerks CodeWarrior and still contains its section headers, a **symbol table of 37,133 names** (`.symtab`/`.strtab`), **relocation tables** (`.relmain`, `.relo0`–`.relo7`: every place the code refers to a symbol), DWARF debug info (`.debug`, `.line`) and a section literally called **`heap` at `0x560D00`**. `tools/elf_symbols.py` lists symbols (`find`, `at`) and finds references (`refs`); a full dump goes to `work/symbols.tsv` (untracked, derived from the game). Examples: `kanjiRomAdrOriginal` 0x13B590, `isHankaku` 0x1293C0, `haff_opt` 0x30C798, `_gp` 0x314770. Small variables are reached through `$gp`, which is why searching for `lui`/`addiu` address pairs missed them. **Use the symbols first** next time something needs finding in the code.

### 4.10 Translation files (format and pipeline)
**Where:** `translation/O0/O0_001.txt` … `translation/O7/…`: 184 files of 200 entries each, 33,000 entries in total. Generated by `tools/dump_script.py`, read by `tools/insert_script.py`. Plain UTF-8 text, one entry per block:

```
== O0:0003  @0x0001d0  \FS …\FE\t60\k\O
JA: ここは県立津久見（つくみ）高校付属施設、学生寄宿舎、通称『阿見（あみ）寮』──
EN: This is a facility attached to Tsukumi Prefectural High School: the student boarding house commonly known as "Ami Dorm"--
ES: 
```
- `O0:0003` = the entry's ID (script file : record number); `@0x0001d0` = where the line sits in the file (the insertion tool finds each entry by this offset, so **never edit the `==` line**).
- `JA:` the original Japanese (Shift-JIS, shown as Unicode). `EN:` the English patch's text as a reference, with its wrap padding and structural codes removed (empty if unknown). Neither is read by the tools.
- **`ES:` is the only thing translators edit.** Empty = keep the original line untouched. The text goes on one line; `⏎` stands for a line-break byte (36 records have one; copy it where the JA has it).
- The codes in the `==` line (`\FS` at the start, `\FE\t60\k\O` at the end) are re-attached automatically from the original. **Don't type them.** Codes that appear *inside* the JA text (`\LC`, `\CG00000000`, `\d`, `\o`, `\V`) must be copied into the ES in the same place.
- **Narration pages: at most 10 lines in total** (see 4.7). A narration page is a run of entries whose `==` line starts with `\FS`, ending at the entry whose codes end in `\k\O`. If a page is too long, write **`<PAGE>`** at the end of an entry that ends with `\FE\t60⏎`: the tool then ends the page there (it swaps the entry's ending for `\FE\t60\k\O`, the ending the game itself uses). Example: `ES: por alguna razón que sonaba convincente, todos terminaron con un cuarto para ellos solos. <PAGE>`. `check.py --pages` lists every page with its line count and errors on pages over 10 lines.
- **Don't wrap or pad lines.** The tool wraps at 47 characters like the English patch (every line but the last is padded with spaces to 47; see 4.7).
- Entries ending in `.2`, `.3` (e.g. `O0:0281.2`) are the second part of a line that the game can also start reading in the middle. They are shown as separate entries; translate them so the two parts read as one sentence.
- **Allowed characters:** space, `A–Z a–z 0–9`, `? ! ' " ( ) . , - : ; / * ~ %`, and `á é í ó ú ñ ü Á É Í Ó Ú Ñ Ü ¿ ¡`. Typographic `… “ ” ‘ ’ — –` are converted automatically (`...`, `"`, `'`, `--`, `-`). **Not available:** `% & + < = > @ [ ] ^ _ \` { | } # $ ♪ ○ ③` and kana/kanji (the symbols in the first list are the stand-ins for the accents; `check.py` will flag them).

**How `insert_script.py` works**, for each entry with Spanish: re-attach the original start/end codes → `charmap` (accents → stand-in symbols) → pre-wrap at 47 → if the bytes fit in the old slot (the old text, its NUL and the zero padding after it, which never extends past 16 bytes: measured on all 33,113 records), **write in place**; otherwise **append at the end of the file** and rewrite every pointer to the line (including pointers into its middle, and pointers that land inside its ending codes) → update the file's header sizes. Entries without Spanish are left as they were.

**What `dump_script.py` found about the data (2026-10-24):**
- 33,113 text records pointed at by the scripts (O0 5,932, O1 6,589, O2 4,710, O3 4,314, O4 3,704, O5 3,729, O6 2,223, O7 1,911) and 54 more mid-line entry points.
- Control codes in the originals (counts over all eight files): `\k` 31,659 · `\p` 31,076 · `\FS` 304 · `\FE` 300 · `\t` 288 (`\t60`) · `\O` 187 · `\LC` 52 · `\CG` 38 (`\CG00000000`, `\CGF00FFFF8`: colour/graphics, seen in the ending screens) · `\V` 23 · `\d` 4 · `\o` 3.
- 110 pointers land mid-record; only those on a character boundary are real entry points (one in O2 pointed at the second byte of `を` and was a false positive, now ignored).
- Some pointers land on the ending codes themselves (the `\p` of `\k\p`): they follow the ending wherever it ends up.
- A few records end with a Japanese full-width space (`81 40`); `.strip()` removes those in Python, which silently broke the first round-trip. Readers must strip only plain spaces.
- The English reference is not a strict map: the English patch sometimes starts a line with the previous line's ending codes; those are removed for display.

**Tests (`tools/test_pipeline.py`, all passing 2026-10-24):** (1) empty Spanish → all eight script files byte-identical; (2) ES = the Japanese text → byte-identical (exercises parse, encode and in-place placement of ~33,000 entries); (3) ES = the English text (a realistic length and wrap load) → every pointer leads to the right text and every file fits in memory: O0 694 KB, O1 730 KB, O2 484 KB, O3 455 KB, O4 394 KB, O5 408 KB, O6 227 KB, O7 199 KB (limit 969 KB), about 65% of lines in place and 35% appended. English text needs the same room as Spanish minus ~25%, so Spanish should still fit (earlier estimate: O1 ≈ 939 KB).

### 4.7 Text box limits
- **47 half-width characters per line** is the engine's wrap column (observed in the accent test; the English script also wraps at 47, padding with spaces). **The dialogue box shows only 46 columns**: a 47th character is cut in half, and when the engine wraps a 47-character line in the middle of a word ("ju" + "ntos") the 47th is half outside the box. So the tool wraps dialogue text at 46 and pads to 47 (narration pages use all 47). Measured 2026-10-26 from the user's screenshots of the own-font ISO.
- **Dialogue box height: 4 lines** (confirmed 2026-10-26: four full lines render correctly).
- **Choice-menu options are never chained.** A menu is a run of `0xF0000000, <option number>, <pointer>` word triples in the bytecode (31 options in O0, 41 in O1, 12 in O2, 16 in O3, 4 in O4, 6 in O5, 4 in O6): `olm.menu_starts` finds them (the word two places before the pointer is `0xF0000000`). Their records have no ending code, so a naive chain rule joined them with the next dialogue line (found 2026-10-26: option 2 came out blank or the following line broke after two words). Chains skip menu options, and `check.py` counts menu options outside the page's lines.
- **Parts and entries printed one after the other get an automatic space** (`script_text.join_marked`): the Japanese has no spaces, so a sentence split into two entries/parts (`0281.1` "...no haces" + `0281.2` "ESO como...") was printed as "hacesESO" until 2026-10-26. A space is added except before `, . ; : ? ! )` or after `¿ ¡ (` or an existing space.
- **Two ways to break lines (2026-10-26, the second is (unverified) in game):** `pad` (default; the English patch's way: pad each line with spaces to 47 columns so the engine wraps) and `newline` (`build.py --wrap newline`: real line-feed bytes, 0x0A, which the Japanese script already uses inside 36 records; saves about 24 KB in O0). The user reported lost letters at some line breaks in `pad` builds ("despacio" shown as "espacio", "la tienda" as "latienda"), so `newline` is the candidate to become the default if the in-game test confirms it.
- **Consecutive entries on one line** (an entry whose ending codes have no `⏎ \k \p \O`, such as O0:0158 -> 0159) are continuous text on screen. Wrapping each independently overflowed the line (the second entry did not know the column where the first ended). `script_text.chain_wrap` now wraps the whole chain as one text (joined with a space, except before `, . ; : ? ! )`) and splits it back by entry; `check.py` counts page lines the same way and warns about orphan last lines of 10 characters or fewer in entries ending with `⏎`.
- **The engine's automatic wrap loses a character:** a 48-character line `… - fin.` displayed as `… - f` / `n.`. So text must be **pre-wrapped** at word boundaries by our tool (padding each line to 47 with spaces, as the English patch does), never left to the engine. Exact behaviour at the boundary (dropped vs drawn off-screen) unverified.
- **Narration pages hold 10 lines** (measured 2026-10-24 in the pilot: pages of 9 and 10 lines were fine; pages of 11 to 13 drew the first 10 lines normally and the rest as squashed glyphs and vertical "barcodes"). A narration page is the run of entries up to one that ends with `\k\O`; all its entries' wrapped lines count together. Pages that are too long must be split with `<PAGE>` (see 4.10) or shortened. `check.py` enforces the limit.
- **Dialogue box**: the normal message window (starts at entry 37 of O0) showed 2-line messages comfortably; its height looks like about 4 lines (estimate from a screenshot, **unverified**); its width took 47 characters per line. `check.py` warns above 4 lines.

### 4.8 O0 round-trip tests (no translation)
Purpose: prove the insertion method (4.3) before translating. The Japanese text is not changed, only moved. Built by a script that was removed after the test (it is in git history; `olm.relocate` still implements the method).

| ISO | What it does | O0 size | O0 ends at RAM | Static checks |
|---|---|---|---|---|
| `MMM_rt_A_partial_marked.iso` | Relocates the first 1,118 of 5,932 records (the opening of the game), sized to fit exactly the 0x8D700 bytes of RAM the original reserves for the largest overlay. Relocated lines start with a diamond (◆). Old slots hold the text `[OLD]` so a missed pointer would be visible. | 579,328 | `0x560D00` | pass |
| `MMM_rt_B_all.iso` | Relocates **all** 5,932 records. No marker. Old slots zeroed. | 846,080 | `0x5A1F00` (past the English patch's biggest overlay end, `0x589600`) | pass |

Static checks that passed for both: following every text pointer in the new file reads exactly the same text as in the original; header size fields consistent; the ISO re-parses with the same 547 files; `iso_diff.py` shows `OLM/O0` is the only file that differs; no 4-byte-aligned word anywhere still points at an emptied slot (the 25 and 5 unaligned look-alikes are bytecode argument pairs).

**Expected in PCSX2:** A: lines in the first scenes begin with ◆ and the rest of the game is unchanged; no `[OLD]` anywhere. B: looks identical to the original. If A works but B crashes or shows garbage, the cause is the larger overlay (RAM), not the pointers: see the memory question in PLAN.md.

**PCSX2 results (user, 2026-10-24): both pass.**
- A: the diamond glyph displays on relocated lines, and the game looks identical to the original otherwise.
- B: identical to the original.

What this proves:
- **The insertion method works on the real engine**: moving text to the end of the file and rewriting the pointers gives the same game. Our pointer list is complete for the part of the game that was played.
- **The diamond (◆, SJIS `81 9F`) exists in the font**, so double-byte symbols from the standard Shift-JIS set can be displayed.
- **An `O0` of 846,080 bytes (ending at RAM `0x5A1F00`) works**, beyond the 0x560D00 the original executable reserves, and beyond the English patch's largest overlay end (`0x589600`). This was only exercised for the stretch of the game the user played (not every scene), so treat it as "works at least for normal play", not as a proven hard limit. The larger overlays (O1 is the biggest at 579,328 bytes originally) have not been tested.

## 5. Tools and environment

### 5.1 Our tools (`tools/`)
| Tool | What it does | Usage |
|---|---|---|
| `iso_extract.py` | Reads an ISO 9660 image: `list` prints/saves the file table (path, LBA, size); `extract` copies files out (optionally only paths starting with given prefixes) | `python -I tools/iso_extract.py list <iso> [table.tsv]`<br>`python -I tools/iso_extract.py extract <iso> <outdir> [prefix …]` |
| `bps_apply.py` | Applies a BPS patch to a file and checks all three CRC32 checksums | `python -I tools/bps_apply.py <patch.bps> <source> <output>` |
| `iso_diff.py` | Compares two ISOs file by file (path, size, SHA-1) and reports resized, changed, moved, added and removed files | `python -I tools/iso_diff.py <iso_a> <iso_b> [report.tsv]` |
| `olm.py` | Script-file library and CLI: `audit` (find text records and pointers, compare with the English file), `relocate` (move text to the end and rewrite pointers; also the future insertion path for translations), `verify` (check pointers still read the same text) | `python -I -X utf8 tools/olm.py audit <O file> [english O file]` |
| `iso_build.py` | Replaces files inside an ISO the way the English patch does: appends the new file after the end of the image, updates the directory record (LBA and size, both byte orders) and the volume size | library: `build_iso(src, dst, {'OLM/O0': bytes})`, `check_iso(...)` |
| `mips.py` | Small MIPS (R5900) disassembler for reading routines in `SLPS_251.92`. RAM address of file offset `off` = `0x100000 + (off − 0x180)` | `python -I -X utf8 tools/mips.py <exe> <RAM addr> [words]` or `--off <file offset>` |
| `elf_symbols.py` | Symbols and code references from the executable's own symbol/relocation tables (4.9) | `python -I -X utf8 tools/elf_symbols.py <exe> find|refs|at|dump …` |
| `exe_patch.py` | Library of executable patches: font cell offsets, segment 9, the half-width list, heap start, advance | library |
| `project.py` | Paths, source ISO hash, reading files from the original disc | library |
| `script_text.py` | Record parts (start/end codes vs text), translation-file text helpers, 47-column wrap, encoding | library |
| `dump_script.py` | Script files → `translation/` files (JA + EN reference + empty ES) (4.10) | `python -I -X utf8 tools/dump_script.py [--force]` |
| `insert_script.py` | `translation/` files → script files: in place when it fits, appended otherwise, pointers rewritten (4.10) | `python -I -X utf8 tools/insert_script.py [--identity]` |
| `test_pipeline.py` | Round-trip and realistic-load tests for the two above (writes under `work/pipeline_test/`) | `python -I -X utf8 tools/test_pipeline.py` |
| `charmap.py` | Spanish text → game bytes (accented letters → stand-in ASCII symbols) | `charmap.encode('¿Qué?')` |
| `check.py` | Lints the `ES:` fields: unsupported characters, stand-in symbols typed literally, codes inside the text, line breaks, over-long words, many-line warnings; prints translation progress | `python -I -X utf8 tools/check.py [--max-lines N] [paths]` |
| `build.py` | **One command: source hash → lint → patch executable → insert scripts → ISO in `build/`.** Pilot builds use the English glyphs (local only, never publish) | `python -I -X utf8 tools/build.py [--out FILE] [--skip-hash]` |
| `font_tool.py` | Reads/writes font cells, composes the Spanish accents from existing letters, installs the pilot font | library |
| `apply_translations.py` | Copies a batch of translations from a tab-separated draft file into the `translation/` files | `python -I -X utf8 tools/apply_translations.py O0 file.tsv` |
| `speakers.py` | Lists speaker labels with line counts and the English patch's names (seeds the character table) | `python -I -X utf8 tools/speakers.py` |
| `script_model.py` | Reads the bytecode: every text line in play order with its kind (line, menu, exe string, credits, title), voice, serial, number inserts; `chains()` (lines shown on one screen line) and `pages()` | `python -I -X utf8 tools/script_model.py [O0]` |
| `screens.py` | **Screen simulator:** rebuilds a script in memory and lays out every screen from the bytes the build ships (46/47 columns, 4/10 rows, real line feeds, numbers drawn by the game); errors for overflow, engine wraps, blank menus, glued words, Japanese left on Spanish screens. `check.py`, `batch.py check` and `build.py` use it | `python -I -X utf8 tools/screens.py O0 [--png]` -> `work/screens/O0.txt` (+ PNG previews of flagged screens) |
| `build.py --start O0:2274` | **Debug ISO:** a new game jumps straight to that line (or `O1:scene3`, a scene start) with an `F0000006` jump written right after O0's first scene start (`0x5D08`). Confirmed in game 2026-10-26 (O0:5780): it works, without a background; it may not work for every line. Never publish | `python -I -X utf8 tools/build.py --start O0:5780` -> `build/MMM_es_start_O0_5780.iso` |
| `savestate.py` | **Refresh a PCSX2 save state** with the current translation: replaces the script file in RAM (0x4D3600; its bytecode is identical in every build, so the game's position stays valid), our font cells and the symbol list. Advance one line to see the new text | `python -I -X utf8 tools/savestate.py refresh <state.p2s>` -> `build/<name>_refreshed.p2s`; `info <state.p2s>` |
| `batch.py` | Translation workflow batches: `next` (next untranslated pages → `work/batches/*.md` + `.tsv`), `check` (validate a draft), `apply` (write into `translation/`, with `NOTE:` lines), `status` (progress, open notes). See docs/TRANSLATION_WORKFLOW.md | `python -I -X utf8 tools/batch.py next O0` |
| `scout.py` | Read-ahead digest of a whole script file (flow per 200 entries, speakers, time marks, frequent katakana words, quoted terms, honorific names) for the `mmm-scout` agent | `python -I -X utf8 tools/scout.py digest O0` |

Notes: `-I` runs Python in isolated mode (it ignores the current folder and environment variables), which is the safe way to run scripts that read untrusted files. To print Japanese in the Windows console, add `-X utf8` (the default console encoding can't show it).

### 5.2 Working files (untracked, in `work/` and `build/`)
- `work/original/`: `SLPS_251.92`, `SYSTEM.CNF`, `OLM/O0`–`O7` from the original ISO
- `work/english/`: the same files from the English-patched ISO
- `work/english_patch/MyMerryMay_EN.bps`: the English patch
- `build/MyMerryMay_EN_test.iso`: original ISO + English patch (1,742,536,704 bytes)

### 5.3 Environment
| Tool | Status | Notes |
|---|---|---|
| Python | 3.14.6 installed | Main language for our tools |
| git | 2.55 installed | Local repo |
| Node.js, .NET | installed | Not planned for use |
| 7-Zip | not found | Not needed; our Python tools read ISOs |
| PCSX2 | v2.4.0 at `C:\Program Files\PCSX2\pcsx2-qt.exe`, configured with the user's own BIOS (a US BIOS is fine for this NTSC-J game) | **Works**: the user confirmed the original ISO reaches the title screen and `build\MyMerryMay_EN_test.iso` (English-patched) runs too |
| MultiPatch | `MultiPatch.app` is an **empty macOS app bundle** | Can't run on Windows. Use Flips or Rom Patcher JS (web) to apply patches |

---

## 6. Glossary (ROM hacking terms)
Quick reference for terms that come up in this project.

- **ISO**: a byte-for-byte image of a disc. PS2 DVDs use the ISO 9660 filesystem.
- **Sector**: the disc's basic unit, 2048 bytes of data on a DVD.
- **LBA (Logical Block Address)**: a sector's number. A file's LBA tells you where on the disc it starts.
- **Directory record**: the entry in the ISO's directory table holding a file's name, LBA and size. Changing a file's LBA/size means editing its record.
- **ELF**: the executable file format PS2 programs use. It has a list of **program headers (segments)** saying which part of the file goes to which RAM address.
- **Executable (`SLPS_251.92`)**: the program the PS2 boots. It contains the engine, menu strings, and here the font.
- **IOP module (`.IRX`)**: a driver for the PS2's secondary processor (sound, memory card, controller). Standard Sony code, not game-specific.
- **Overlay**: a chunk of program or data loaded into RAM on demand at a fixed address, replacing the previous one. The `OLM/O*` script files are overlays.
- **Shift-JIS**: the standard Japanese text encoding. ASCII characters take 1 byte and Japanese characters take 2.
- **Control code**: a special sequence inside the text that does something instead of printing a character (here written like `\k`, `\p`, `\t60`).
- **Pointer / pointer table**: an address that tells the engine where something is. If you make a text line longer, every pointer to things after it has to be updated.
- **Opcode**: a number that tells a script engine which command to run.
- **Entropy**: a measure of how random bytes look. Compressed or encrypted data is close to 8 bits per byte; text and code are lower. Used to detect compression.
- **TIM2**: the PS2's standard image/texture format.
- **Font / glyph**: a glyph is the picture of one character. The font is a table of glyphs plus a mapping from character codes to glyphs.
- **Monospaced vs proportional**: monospaced gives every character the same width, while proportional fonts use narrow and wide widths (i vs m). Proportional fonts fit more text per line.
- **Round-trip test**: extract data, then reinsert it unchanged, and check the output is byte-identical. It proves the tools don't damage anything.
- **BPS**: a patch format that stores only the differences between the original and modified file, plus checksums of both. It's what the English patch uses. Apply it with Flips, MultiPatch, or Rom Patcher JS.
- **xdelta**: another patch format that's common for large disc images.
