# Project log

Dated record of decisions (with reasons) and what each session did. Newest first.

---

## 2026-11-01 — O2 batch 4503-X003: sixth DeepSeek V4 Pro batch; O2 is 100% (applied, not committed)

204 entries drafted (7 API calls, 184K in / 88K out; 7 pre-filled copies, all fine). Review: **26 of 204 rows changed (12.7%)**: 22 substantive (10.8%) + 4 format-only. Categories: naturalness 13, fidelity 5, addition 3, omission 1, format 4. Pro, six batches: 14.3%/6.6%, 9.9%/4.8%, 8.8%/8.4%, 12.5%/11.1%, 11.1%/7.1%, 12.7%/10.8% (Flash: 18%; 31%/24%). Errors concentrate in Kyohei's long technical speeches (4536-4605); narration and the birthday scene needed little. Reviewer ~160K tokens.
- Real meaning errors: 4605 (〜のに as "Aunque", inverted), 4549 and 4555 (lost "devices" / who causes the trouble). New patterns -> pitfall 16: concessives, the long dash ―― mishandled, constructions that do not exist in Spanish, transliterated interjections ("¿Ah?" for は？), ambiguous words (コードネーム, 意味って), lost embedded subject, Peninsular "¿Y eso?" again.
- **O2 summary (6 Pro batches, 3003-X003):** 1,645 entries drafted by DeepSeek V4 Pro, 188 rows changed (11.4%), 132 of them substantive (8.0%); about 150-180K Claude tokens per review. The Claude translator is no longer used for O2.
- Judgement calls for the user (left as drafted): 4604 帰国 read as the end of Kyohei's stay ("antes de que me vaya"); 4686 literal; 4699 "¡Ya te dije!" for だ～か～ら; 回収 = "recuperar"; 4651 "Lease-san" (Reu's honorific for her).

## 2026-11-01 — O2 batch 4203-4502: fifth DeepSeek V4 Pro batch (applied, not committed)

297 entries drafted (6 API calls, 162K in / 89K out, 0 errors on the first check). Review: **33 of 297 rows changed (11.1%)**: 21 substantive (7.1%) + 12 format-only (4.0%, ellipses and punctuation). Categories: naturalness 7, fidelity 5, glossary 5, addition 2, omission 1, register 1, format 12. Pro so far: 14.3%/6.6%, 9.9%/4.8%, 8.8%/8.4%, 12.5%/11.1%, 11.1%/7.1% (Flash: 18%; 31%/24%). Easier scene (little double-voice, plain gags). Only one real meaning error: 4211 (間柄 = their relationship, not "que le escriba"). Reviewer ~150K tokens.
- New patterns -> pitfall 15: ellipses ADDED where the Japanese has none (10 rows), 24 dots for 4 characters again (4288), one Japanese word with two renderings inside a batch (持病, 秘蔵, 頼む, 了解), はい when handing something over rendered "Sí", から clause with no main clause, ¿¿...?? instead of ¡¿...?!, usted between the two Reu.
- User decisions (2026-11-01): 酒 in 4356-4376 = "whisky" everywhere (was "licor" in the dialogue); Beta uses usted with everyone, including the other Reu (4239 now "no se preocupe"); Hitoe and Kyohei use tú both ways (the Japanese is casual on both sides).

## 2026-11-01 — O2 batch 3903-4202: fourth DeepSeek V4 Pro batch (applied, not committed)

296 entries drafted (5 API calls, 136K in / 77K out, 0 errors on the first check). Review: **37 of 296 rows changed (12.5%)**: 33 substantive (11.1%) + 4 format-only (dropped leading "..."). Categories: fidelity 12, naturalness 8, glossary 6, omission 3, register 3, addition 1, format 4. Pro so far: 14.3%/6.6%, 9.9%/4.8%, 8.8%/8.4%, 12.5%/11.1% (Flash: 18%; 31%/24%). Harder scene: 300 short Q&A pages, the Reu/Lease double voice, tenses alternating within a page. Reviewer ~182K tokens (the most so far).
- Meaning errors fixed: 4118 ("el hermano del hermano"; the scouting note was wrong), 4200 (Tae uses usted with Kyohei, invented "no hace falta que me llames Kizuki" removed), 4190 (Reu says "hermano"), 4026 (Reu is "prima"), 3949/3952 ("dijo", question restored), tense slips 4108/4189/4061, 3903/3906 "mi viejo".
- New patterns -> pitfall 14: ellipsis runs still unreliable (4 characters came out as 30 dots and as 3), dropped leading "...", オヤジ = "papá", register toward third parties (Tae/Kyohei, Lease), kinship vocabulary, first full name without -san, dropped/added とりあえず/わざわざ/って言うじゃない, added "muy"/"definitivamente", the translator tagging its own notes "NOTE: rev:".
- Decisions taken by default (shout if you disagree): 3940 "la gran Hitoe Haruna" (as in O1:6046-6048); Reu = "prima"; Lease's lines before 4233 keep the label "Reu" with notes (extends the 4086-4144 range to 3984-4034, 4086-4144, 4163-4182; 4191/4193 stay `???`); 3986 "Sí, bienvenido, señor." (the "señor" stands in for お帰りなさいませ).

## 2026-11-01 — O2 batch 3603-3902: third DeepSeek V4 Pro batch (applied, not committed)

296 entries drafted (11 API calls, 277K in / 126K out; one length error left after 6 rounds: 3818-3820, fixed by the reviewer). Review: **26 of 296 rows changed (8.8%)**: 25 substantive (8.4%; 22 = 7.4% without the 3 length-fix rows, of which about 7 were real meaning errors), 1 format-only. Categories: fidelity 11, naturalness 7, budget 3, omission 1, addition 1, register 1, glossary 1, format 1. Pro so far: 14.3%/6.6%, 9.9%/4.8%, 8.8%/8.4% (Flash: 18%; 31%/24%). Scene moderately hard (wordplay 気にするな/気になる -> 矛盾, loan joke, abstract self-analysis). Reviewer ~153K tokens.
- Real meaning errors fixed: 3644 ("Cuando termines de comer", Ryo is still eating), 3747 (the contradiction that the 矛盾 joke needs), 3616 (確か), 3659 (あのね), 3718 (発端 = "punto de partida"), 3898 (missing causal link to 3894).
- New patterns -> pitfall 13 in the prompt: 〜たら tense/aspect, attitude particles read as content, wordplay split over neighbouring lines, formal register in teenage speech ("mortificar"), set-phrase calques ("Como era de esperarse"), added connectors.
- User decision: the e-mail catchphrase in 3899 ("¿No pasa nada bueno?") may differ from O0's ("¿No pasa nada interesante?"). **Commit policy:** the user wants a single commit when O2 is finished (not per batch).

## 2026-11-01 — O2 batch 3303-3602: second DeepSeek V4 Pro batch

293 entries drafted (5 API calls, 132K in / 74K out), 0 errors on the first check; reviewed and applied (294 rows with one pre-filled copy fixed at 3310). Review: **29 of 293 rows changed (9.9%)**: 14 substantive (4.8%) + 15 stylistic (5.1%); no missing labels or format errors. Categories (30 rows): naturalness 13, fidelity 9, omission 5, addition 1, glossary 1, typo 1. Pro so far: 14.3% / 6.6% substantive, then 9.9% / 4.8%; Flash: 18%, 31% / 24%. The scene was easier in format (no codes, no wordplay) but harder in tone (icy confrontation with Misao, a monologue with a simile); the Misao scene needed only four small fixes, so the gain looks mostly due to the model. Reviewer used ~134K tokens.
- New patterns: dropped hedges (ような similes, と思う, ほとんど, だって), cut-off sentences filled with plausible empty text, added superlatives ("más preciada"), sentence-final か musing turned into "¿no?", a greeting reply ああ as "Ah...", verb drift comer/tomar, a Peninsular "y eso" -> pitfall 12 in the prompt.
- For the human review: 3462/3464 and 3488 (sarcastic ご苦労様 "Cuánto lo siento", お疲れさま "Mis condolencias"); 3565 Tae's セリフ……間違えてない? = "Esa frase... ¿no te equivocaste?" (hints at a role swap); 3374 continues 3373 in lowercase.

## 2026-11-01 — O2 batch 3003-3302: first batch drafted by DeepSeek V4 Pro

259 entries translated + reviewed (41 pre-filled copies, all checked in context, none needed fixing). Review: **37 of 259 rows changed (14.3%)**: 17 substantive (6.6%), 15 missing speaker labels/quotes (5.8%), 5 format-only (1.9%). By category: omission 15, naturalness 7, fidelity 5, addition 5, glossary 2, typo 2, register 1. Compared with V4.1 Flash (18% and 31%/24% substantive), Pro's substantive rate is about a quarter to a third of Flash's. Caveat: the scene is simple dialogue without wordplay or codes; a harder batch may look worse. API use: 7 calls, 179K tokens in, 71K out; the Claude reviewer used ~153K tokens.
- New pattern: **format drift at the end of the batch** (the last 19 rows lost every `Name: "` label and quote; the check cannot see it) -> pitfall 11 added to the llm_batch prompt. Other: idioms rendered literally (奥歯にものが挟まった, まったく, 気味が悪い), one invented detail ("hasta mañana"), quote marks around inner-thought narration. Not seen: wrong subject/negation/number, vosotros, regionalisms, forbidden characters.
- Glossary additions: see STYLE_GUIDE (3 rows). For the human review: 3245 "desde las sombras" (alt. "desde ultratumba"); 3171 "tu hermano Kyohei" vs 3178 "hermano Kyohei"; 3052/3069 `『』` in narration kept as single quotes (O2_011 single, O2_014 double: unify later).

## 2026-11-01 — O2 batch 2701-3000: second DeepSeek draft; the experiment's verdict so far

294 entries translated + reviewed. Review: **90 of 294 lines changed (31%)**: 70 substantive (24%: naturalness 27, fidelity 25, typo 10, glossary 6, omission 1, addition 1) + 20 ellipsis normalisations. The first batch needed 18%; this range (inner monologue, quoted memories) is harder, and **my own prompt rule 6 was wrong** (it asked for 6 dots per two-character ellipsis; the project uses "..."): fixed. The "known pitfalls" fixed several surface errors (decided terms, "Diciendo eso", だから/さて) but new patterns appeared: -chan dropped, repeated passages translated differently, nested double quotes, tense flips, wrong subject in echoes, regionalisms. The prompt now has 10 points. Tokens: 131,084 in / 35,195 out. Reviewer workload was ~1.5-2x a Claude draft, so the net Claude-usage saving is modest. To align: O2_011.txt line 754 (Tae's lecture drops 可能な限り). Story notes added to STORY.

## 2026-11-01 — O2 batch 2401-2700: first batch drafted by DeepSeek V4.1 Flash (llm_batch.py)

Key finding of the first run: the Go subscription needs its own endpoint (`https://opencode.ai/inference/go/...`); the plain `/inference/...` bills the balance and returned HTTP 402. With the Go endpoint the whole batch (295 entries, 5 calls, 127,203 tokens in / 32,235 out) passed `batch.py check` with 0 errors in the first round. Claude review: **54 of 295 lines changed (18%)**: fidelity 20, naturalness 16, glossary 7, typo 5, omission 3, addition 2, register 1 — about 1.5-2x the usual Claude-translator draft. Typical flash-model errors: decided glossary terms not applied (Reu's えへへ "Jijiji", おかえり "bienvenido", がんばって "¡ánimo!", repeated quotes), English calques ("Diciendo eso, X hizo..."), flattened particles (だから, だそうです, さて), tense/subject slips, invented hedges; ellipsis counts (3 dots per ellipsis character). 295 entries translated + reviewed. Story: Reu's bento at the gate, Speed and Concentration with Misao, Motomi in the corridor. Prompt improvements added to llm_batch.py (a "known pitfalls" section).

## 2026-11-01 — Cheaper translator step: tools/llm_batch.py (OpenCode API); small fixes

The agents consume a lot of the user's Claude usage, so `tools/llm_batch.py` can do the translator step with a model from the user's OpenCode Go subscription (API docs https://opencode.ai/v2/docs/console/api/inference: base `https://opencode.ai/inference`, chat models at `/openai/v1/chat/completions`, ids from `GET /inference/v1/models`; the docs do not list a DeepSeek id, so the first step is `llm_batch.py models`). It sends the Japanese batch text to a third party (the user's call). The key is read from the environment variable `OPENCODE_GO_API_KEY` or a git-ignored `.env`; export_public.py refuses any `.env*` file. Tested offline with a fake model (chunking, parsing, an injected forbidden character, an injected omission: both recovered). Also: (1) `batch.py check` now shows orphan-line warnings; (2) a draft line with a forbidden character used to crash the screen simulation instead of being reported: such a line is now blanked for the simulation and reported by the entry check; (3) TRANSLATION_WORKFLOW and the translator agent no longer list `+` as forbidden or Í/Ü as allowed (stale since 2026-10-25). Review (Claude) and apply are unchanged: the reviewer still checks every line and `apply` re-checks.

## 2026-11-01 — O2 batch 2101-2400 (Tae at the rainy entrance, Motomi's return, Reu at the gate)

293 entries translated + reviewed (review resumed after a usage-limit stop). Review: 34 rows (fidelity ~12, omission ~5, naturalness ~10, typo ~7, glossary 1 "futon" for cobijas, register 1, addition 1); three over-long pages fixed. Menu 2122/2123 verified (label 1: 2124-2153, label 2: 2154-2161, shared from 2162). Reu's わたし lines (2338, 2352) are first person ("hice algo"), as in O0, not third person. Session paused here because the user hit the weekly usage limit; next: O2 from 2401.

## 2026-10-27 — O2 batch 1801-2100 (Tae on his lap, Misao asleep, the rainy entrance)

295 entries translated + reviewed. Review: 17 rows + 1 note fix (fidelity 11, naturalness 6, typo 1, addition 1). Both menus verified in the bytecode flow (1846-1847: option 1 jumps to 1902; option 2 shows 1866-1901; 1941-1942 both join at 1968). Fixes: 2070 "fui... me topé" (he went alone), 1917 "no te hagas del rogar", 2088 "Es verdad...".

## 2026-10-27 — O2 batch 1501-1800 (shopping, arcade, Tae drunk at 2 AM)

296 entries translated + reviewed. Review: 14 rows (fidelity 4, naturalness 4, addition 4 = the invented "sh" slur removed from 1755/1760/1764/1772, pre-filled 1661 "No es para tanto."). Tae's slur is kept only at 1787/1792 ("talonesh"), where the Japanese has it (せいじゃ). 1721 turned to preterite (this morning's meeting). Glossary added: sabor auténtico, Parmigiano, máquina de grúa/peluche/muñeco, billetera, celular, número oculto, Cric cric, mullido.

## 2026-10-27 — O2 batch 1201-1500 (the improvised-surname menu, the date at the park)

295 entries + 3 menu rows translated + reviewed. The three executable strings are a real 3-option menu after O2:1326 (verified in the bytecode): X001 Eguchi, X002 Enari, X003 Mochizuki (bare names). Review: 16 rows (fidelity 6, naturalness 8, register 2: "Va" avoided). 1220 reversed in the English reference (Misao was the one taught the pasta). Glossary added: lagañas, kata, comité de biblioteca, secundaria, baño, Ok, instinto. To check in PCSX2 when convenient: the surname menu.

## 2026-10-27 — O2 batch 0901-1200 (Tae's hangover, call to Misao)

293 entries translated + reviewed. Review: 5 rows (fidelity 2, omission 1, naturalness 3). No pre-filled copy needed fixing. Glossary added: resaca, gachas de arroz, oatmeal, el pelo del perro, entrañable vecina, Puntaje perfecto, ¿Hola?.

## 2026-10-27 — O2 batch 0601-0900 (the day after: Reu's "querer", Ryo's cheer)

297 entries translated + reviewed. Review: 9 rows (naturalness 5, fidelity 1, omission 1, addition 1). Source day-order inconsistency at 0662-0666 kept. Glossary added: tinta china, andar con dos a la vez, sentada sobre los talones, dejarse mandar, "Querer a alguien es..." definition. For the user: Kyosuke's own 0879/0882 "querer o no querer" could read as "want or not want" (alternative "que me quieras o no").

## 2026-10-27 — O2 batch 0301-0600 (Ryo's breakup confession, Hitoe's unfinished sentence, coin tricks)

299 entries translated + reviewed. Review: 28 rows (naturalness 15, fidelity 8, omission 1, register 1, typo 2, glossary 1). **0404 "Error, error."** is kept as decided: the next line has no break, so the row after "Error, error. " (14 columns) must stay within 46; the reviewer made 0405's first row short with an added adverb ("sorprendentemente", not in the Japanese). Open for the user: keep it, or use "Error." with the original 0405. Glossary added: Tachán, poder mágico, Enmascarado Telépata.

## 2026-10-27 — O2 batch 0001-0300 (lunch at the tienda escolar, Ryo on Monday)

298 entries translated + reviewed. Review: 20 rows (fidelity 6, naturalness 9, register 1, addition 1, omission 1, typo 1, glossary 2). "popote" replaced by "pajita"; 0234 no longer uses usted with Ryo; 0109/0111 garbled with a full mouth. Glossary added: pajita, club de animación, labels, sound effects, yenes, campo de batalla, "Uuu." for あう.

## 2026-10-27 — O2 scouted; the user accepted all recommendations

`docs/scouting/O2.md`. Decisions recorded in STYLE_GUIDE: Lease's label "Beta" (written in letters, the font has no β), early レゥ lines stay "Reu" with a NOTE, Lease from 4622; Lease addresses Kyosuke "Kyosuke-sama" and Kyohei "Amo" with usted; アニキ (Kyohei) = "mi hermano"/"¡Hermano!"/"hermano Kyohei"; えらーだえらーだ = "Error, error."; Misao's cold scene keeps tú; android serials "Pmfh-00001/2"; "Kazu-chan" kept with a NOTE; birthday song with "~" for ♪; surnames Eguchi/Enari/Mochizuki; pre-fill runs (about 296 lines). To check in PCSX2: whether the three surnames are menu options or displayed names, and whether ♪ renders.

## 2026-10-26 — Public repository

The user asked for the repo to be pushed (public) so their Claude chat can read the project. Because `translation/` holds the Japanese original next to the Spanish (hard rule: never published), the working repo is not pushed. `tools/export_public.py` builds a snapshot of the tracked files minus `translation/`, `work/`, `build/` (47 files, 0.46 MB; checks: no ISO/patch/archive extensions, no file over 1 MB, no file with more than 2,000 Japanese characters), commits it to a separate clone (`work/public_repo`) with the GitHub no-reply author, and pushes it. New `README.md` is the unified overview (how it works, pipeline, agents, decisions, status). The user created https://github.com/Corcholog/mmm-spanish-patch and pushed the first snapshot (cb35bdf) themselves, because creating a public repository was blocked by the permission system. Update with the same command whenever the user asks.

## 2026-10-26 — O1 COMPLETE (last batch 6318-X007: photo booth, dream of Kyohei, Monday)

272 entries translated + reviewed; the 7 executable strings (X001-X007) were already filled by the pre-fill ("." x3, "Retirarme" x4) and checked. Review: 25 rows (fidelity 5, omission 5, addition 2, register 2, naturalness 8, glossary 1, typo 2). O1 is 6,598 of 6,598; total 12,537 of 33,135 (37.8%). Open for the user: the dream brother (???) and child Hitoe use tú with each other although the JA is polite (reviewer changed one usted slip at 6542). Next: build a full ISO to verify O1's memory budget (PLAN risk: O1 close to its RAM limit), then scout O2. **Memory check done (full build, 2026-10-26): O1 fully translated is 746,496 bytes, ends at 0x589A00, under the heap start 0x5D0000 (about 288 KB spare); O0 ends at 0x57B700. No heap change needed.**

## 2026-10-26 — O1 batch 6018-6317 (Sunday with Hitoe: rebajas, ice cream, levels, arcade)

296 entries translated + reviewed. Review: 17 rows (fidelity 6, naturalness 4, omission 1, addition 2, numbers 4). Hitoe's love levels follow the numbers rule ("nivel uno", "nivel seis", "nivel 10"). Glossary added: arcade, mejor amiga, a la acción, helado de chocolate moca con vainilla, burlarse de.

## 2026-10-26 — O1 batch 5718-6017 (end of Route Tae+Misao, Reu's drawing, Sunday)

293 entries translated + reviewed. Review: 16 rows (naturalness 7, fidelity 4, omission 1: 5991 義務 restored, typo 1, addition 2, pre-filled 5869 "Es verdad."). Glossary added: imagawayaki, lo verde, armas de proyectil, de vanguardia, sudor frío, velar por.

## 2026-10-26 — O1 batch 5418-5717 (Route Tae + Misao: papas, okonomiyaki, shooting gallery)

290 entries translated + reviewed. Review: 29 rows (fidelity 14, addition 2, naturalness 8, glossary 3, pre-filled 5518 "Perdón por la espera~"). 5702 "¡Hermano!" verified in the script flow (both branches end with Reu's arrival, 5772). Stall label unified to "Empleado". Glossary added: tiro al blanco, okonomiyaki, puesto, Empleado, atiborrarse.

## 2026-10-26 — O1 batch 5118-5417 (end of Route Motomi, start of Route Tae + Misao)

297 entries translated + reviewed. Review: 16 changes (fidelity 4, naturalness 5, omission 2, addition 1, register 2 incl. pre-filled 5299 "...Perdón.", typo 2). Route boundary confirmed in the bytecode: 5241-5242 close Route Motomi. Glossary added: albaricoques caramelizados, calamar asado / papas con mantequilla / salchicha, Pervertido, me la pasó, stall greeting. Open for the user: **Misao uses tú with Tae** (5280 set to tú: she is Tae's neighbour and cooking disciple; no earlier Spanish line showed it). **User decision: yes, tú.**

## 2026-10-26 — O1 batch 4818-5117 (Route Hitoe with the fox wedding, start of Route Motomi)

293 entries translated + reviewed. Review: 7 changes (fidelity 5 incl. pre-filled 5091 "No pasa nada", 5030 "Nosotras"; naturalness 2). Glossary added: la boda de los zorros, embrujar, cortejo, manzana acaramelada, rebajas, cargar las bolsas, junta de vecinos, música de flautas y tambores. Open for the user: "la yukata" or "el yukata". **User decision: "la yukata".**

## 2026-10-26 — O1 batch 4518-4817 (Route Reu with the yakuza, start of Route Hitoe)

294 entries translated + reviewed. Review: 9 changes (naturalness 7, fidelity 1, register 1). Jefe (calm, old-fashioned) and Yasu (rough, neutral) checked for regional slang. 別腹 reuses O0:3524 "un huequito aparte" (docs said "otro estómago" by mistake; STORY and scouting corrected). Glossary added: Hombre, bajo mundo, iguales, ojo observador, máscara de gorila, algodón de azúcar, abrazo en picada, duelo de miradas.

## 2026-10-26 — O1 batch 4218-4517 (feria, Oráculo de parejas, route menu)

295 entries translated + reviewed (review resumed after a usage-limit stop). Review: 9 changes (naturalness 7: route menu 4389-4391 now bare names "Reu..." / "Hitoe..." / "Motomi-chan..." as in the JA; glossary 1: "pelea de casados"; fidelity 1). Glossary added: Vendedor, sorteo/papelito, ¡Allá voy!, bicho de la infidelidad, coco blando, pelea de casados, tutor, a la de tres, Ju ju ju, ¿Eeeh?, mi señor, vamos a arreglar esto afuera.

## 2026-10-26 — O1 batch 3918-4217 (Motomi's worry, Reu and the cat, feria begins)

298 entries translated + reviewed. Review: 9 changes (fidelity 2, register 1, naturalness 6). The 4099/4100 seam is a menu branch (3902 apologise -> 3904-4099 -> 4166; 3903 hurry on -> 4100-4165 -> 4166), confirmed in the bytecode. Glossary added: gatito, *olfatea olfatea*, ¡Fiaaau!, fin de la historia, aprensiva, distraída por naturaleza, recto y leal.

## 2026-10-26 — O1 batch 3618-3917 (Friday: Hitoe plans the festival outing)

297 entries translated + reviewed. Review: 11 changes (naturalness 9, fidelity 1: 3906, register 1: 3847 Hitoe's self-praise uses "-chan" as in the JA ひとえちゃん, "la gran" kept for 様). Pre-filled copies fine. Glossary added: Tour por la feria, faroles rojos, lentes, ir a explorar, mujeriego, mi cielo, Hitoe's laughs, *mirada fija*, despistado, ひとえちゃん rule.

## 2026-10-26 — O1 batch 3318-3617 (2 AM with Tae, pasta with Misao, Friday morning)

298 entries translated + reviewed. Review: 8 changes (fidelity 3, naturalness 5). Pre-filled copies fine. Glossary added: algo de comer, despejarse, cocina de hombre, bol, crema/tocino/salsa de soya, muletilla "dejémoslo así", tradición, "un N de 100".

## 2026-10-26 — O1 batch 3018-3317 (contest ends in a draw; 2 AM with Tae)

294 entries translated + reviewed. Review: 7 changes (naturalness 5, tone 1: 3267 ご苦労様です kept polite, typo 1) incl. pre-filled 3298 "Así es.". Glossary added: chocolate, tortolitos, se lo buscó, patadas de ahogado, enorme concesión, el gran ~, armar todo este escándalo, laptop, ご苦労様です rule.

## 2026-10-26 — O1 batch 2718-3017 (quiz result, Tae's break, round 3 begins)

286 entries translated + reviewed. Review: 5 changes (fidelity 1, naturalness 4: 2957 "Para bien o para mal" instead of a calque). Pre-filled copies and the in-game-checked scoreboard all fine. Glossary added: no poder contener la risa, metí la pata, para bien o para mal, tiempo extra, los dos implicados.

## 2026-10-26 — O1 batch 2418-2717 (round 1 lost by a hair, quiz)

299 entries translated + reviewed. Review: 9 changes (fidelity 2 incl. pre-filled 2614 "¿Entonces qué es?", naturalness 6 — 2546 avoids "fresco" = cheeky —, typo 1). Glossary added: el coco, apostando, prueba de IQ, race/quiz start calls, ¡Meta!. Open for the user: Ryo's proverb mix-up (2657-2658) as "agua que no has de beber, déjala correr" corrected to "del agua mansa líbreme Dios" (alternative: "de tal palo, tal astilla", closer to トンビがタカを生む but loses the echo). **User decision 2026-10-26: keep the water pair.**

## 2026-10-26 — O1 batch 2118-2417 (contest day: mornings, arrival, round 1 starts)

289 entries translated + reviewed. Review: 15 changes (naturalness 11, fidelity 3, omission 1), incl. 2 pre-filled copies of very short lines (2291 恭介「うん」 "No." -> "Ajá."; 2295 「だから！」 "¡Que no!" -> "¡¿Y entonces?!"). **Pre-fill no longer copies lines with 4 or fewer spoken characters** (`batch.too_short_to_copy`): their meaning depends on the scene; 149 such copies ahead in O1 were cleared. Glossary added (consistent, approved by the reviewer): Jijiji~, la protagonista, deber, gruñón, curiosos/espectadores, séquito de un señor feudal, guardián de templo, No es no, creerse el centro de atención, cara de sentimientos encontrados; O0_002 "Ehehe" aligned to "Jijiji".

## 2026-10-26 — O1 batch 1813-2112 (block C: poker with Misao, honorifics scene)

152 entries translated + reviewed. Review: 5 changes (fidelity 4 incl. pre-filled 1896 "y la carta de Reu es"; naturalness 1). Glossary added (consistent): hablarle con formalidad, cara de póker, te tocaron malas cartas, táctica, no sabe distinguir el momento ni el lugar. For the user: 2022 Reu's すきだよ to Misao = "te quiero porque eres buena" (alternative "me caes bien").

## 2026-10-25 — O1 batch 1507-1806 (end of block B, start of block C)

48 entries translated + reviewed. Review: 4 changes (1753 pre-filled copy "¿Qué es bonito?" as 0707; 1726 "¿Reu está bien?" to avoid an usted reading; 1646 "las llaves"; 1647 "manojo de llaves"). カギの束 = "manojo de llaves" also applied to 0583/1159 for consistency (added to the glossary). Note: 1662 keeps the source's "dentro de tres días" (the contest is two days away; source slip).

## 2026-10-25 — O1 batch 1202-1500 (block B: river, poker by phone)

45 entries translated + reviewed (most of block B pre-filled from block A). Review: 5 changes (fidelity 2, naturalness 1, 2 pre-filled copies fixed: 1386 "les explico" as in 0846, 1368 Misao answering the phone "¿Sí?"). No glossary proposals.

## 2026-10-25 — O1 batch 0900-1199 (block A poker, TV special, start of block B)

133 entries translated + reviewed (review resumed after a usage-limit stop). Review: 2 fidelity changes (1040, 1047); no pre-filled copy needed fixing (block B copies checked for two people). Card lines: "la carta de Reu es <carta> y la carta de Tae-san es <carta>... Ya veo...". Glossary added: リーチ, 百戦錬磨のギャンブラー, 適当にやんなさい. Open for the user: mixed marks order (¡¿...?! used 70 times, ¿¡...!? 26 times; the workflow says ¿¡...!?). **User decision: ¡¿...?! everywhere**; the 26 others converted, workflow updated.

## 2026-10-25 — O1 batch 0600-0899 (block A: river, Reu heals, fake history No. 2)

264 entries translated + reviewed; review: 10 changes (naturalness 7, fidelity 1, omission 1, register 1), 3 of them **pre-filled copies that didn't fit their new place** (0653, 0707, 0846: same Japanese, different context), applied with --force. Lesson: reviewers check the copies in each batch. Glossary added (consistent): Misao's がんばってください "Da lo mejor de ti", スタート "¡Ya!", 泡 "espuma blanca", duelo simulado, nativos americanos, abrigo. For the user: よいしょっ = "¡Upa!" (alternative "¡Arriba!").

## 2026-10-25 — O1 batch 0301-0599 (end of Hitoe variant, Motomi variant, start of block A)

119 entries translated + reviewed (the rest pre-filled from O0). Review: 3 changes (fidelity 2: 0305 Reu's ううん = "No...", 0336 "di un paso" since Hitoe is absent; naturalness 1: 0406). Glossary (consistent with existing choices, added): 徹底抗戦, 会議, 気持ちを切り替える, がんばってね. Open for the user: clock times in one scene mix words (0323-0324 "las cinco y media") and digits (pre-filled 0429-0433 "4:30", also O0:5310-5311 "5:30"). **User decision: leave the mix.**

## 2026-10-25 — O1 batch 0001-0300 (Hitoe's training)

280 entries translated + reviewed (20 pre-filled copies; the run's own prefill added 4). Review: 11 changes (naturalness 7, fidelity 2, register 1, grammar 1); 0176 keeps Kyosuke's comic polite slip ("se lo aseguro"). Translator wrongly avoided lowercase í (only Í/Ü are out); fixed in review (0272 "¡Increííble!"). Glossary proposals for the user: パシリ = "mandadero/a"; ヤレヤレ (narration) = "Ay, ay, ay."; 女子棟/男子棟 = "el edificio de las chicas/de los chicos" (as in O0). NOTE left: 0263 little Kyosuke (きょうすけ) labelled "Kyosuke".

## 2026-10-25 — O1 scouted; decisions; pre-fill of identical lines; + and × in the font

Scout: `docs/scouting/O1.md`. User decisions: (1) copy existing Spanish into identical Japanese lines; (2) add + and × to the font; (3) the user checks the scoreboard/GAME OVER widths in PCSX2; (4) yakuza boss アニキ = "Jefe"; (5) festival terms as proposed (la feria / pesca de pececitos / Oráculo de parejas / cabina de fotos); (6) O0:5856 is Kyosuke folding: "M-me retiro...". Recorded in STYLE_GUIDE.
- **Font:** every printable ASCII byte was already taken, so the stand-ins of Í and Ü (never used) were given up: '+' now draws a plus (í moved to '|'), '^' draws ×. Í/Ü can't be typed (write I/U).
- **Pre-fill:** `batch.py prefill <script>` (also run automatically by `batch.py next`) copies Spanish into untranslated entries whose Japanese and codes match an already-translated entry, with `NOTE: copied from <ID>`; copies the checks reject are dropped. O1: 720 entries. Batches list the copies as context only. Screens that still show a Japanese line are checked once fully translated (`screens.check_screen(pending=...)`).
- O1 scoreboard and GAME OVER translated (2995-3001, 3057) for the PCSX2 check: `build/MMM_es_start_O1_2990.iso`, `build/MMM_es_start_O1_3056.iso` (GAME OVER only shows if Kyosuke loses). **Checked in game by the user: the big-text scoreboard lines fit;** the rest of O1 is still Japanese, with the pre-filled copies showing in Spanish in between (expected).

## 2026-10-25 — Sentences that continue across a goto

Screenshot: "Mmm, La carta de Reu es trébol 0." The scene picks one of three reactions (5781+5782, 5783+5784, 5785+X004) and each ends with an interjection (えーと、 / どれどれ、 / ふむ。) that the game joins with 5786. The tools had chained by file order, so the Spanish had "Mmm, para alguien..." and "A ver, creo que..." (wrong) and a capital "La". Found that `F0000008 n` is a label and `F000000B n` a goto (all 104 O0 gotos match a unique label in their scene). `script_model.chains()` now follows gotos (a line can be in several chains; the build lays a shared record out with the first, `screens.py` checks every branch), `branch_joins()` lists the joins, and `batch.py next` flags both ends with "BRANCH: ..." for the translator. Fixed O0 5783, 5785 (now start sentences), 5786 (lowercase), X004 "Bueno,". O1 has 12 such joins. The card text "trébol 0" against a 6 of spades is a debug-ISO effect: the start jump skips the deal, so the suit index and value are still 0 (unverified until a normal playthrough).

## 2026-10-25 — Card names: "10 de corazones", "reina de diamantes"

Starting at 5779 (so the deal runs) the text matched the cards (corazón 10, trébol 3), confirming the suit strings. The user asked for "(number) de (suit)" and words for the face cards; the K was full-width (the J/Q/K/A formats are `%sＪ` etc.). The card code is `oscrRrnd` (RAM 0x17F6CC-0x17F890): strcpy(buf, suit) then sprintf(0x334010, fmt, buf, value), fmt by value 11-14 or `%s %d`. `exe_patch.set_card_formats` points the five format loads at new strings in segment 9 (offset 0x40; segment 9 is now 256 bytes): `jota de %s`, `reina de %s`, `rey de %s`, `as de %s`, `%d de %s`; for the number case it swaps the two arguments (a2 = value, a3 = suit; the second move fills the jal's delay slot, a nop). Suits are now plural: tréboles, corazones, picas, diamantes. Layout reserves 18 columns for the card name (`st.NUMBER_COLS`, longest "reina de diamantes") both in the build's wrapping and in screens.py, so 5788 and 5804 now break the line before the overflow. 1 = A? unverified (value 14 is the ace in the code; 1 may never occur). **Confirmed in game by the user (start-at-5779 ISO).**

## 2026-10-25 — Card suit names live in the executable

Screenshot: "La carta de Reu es クラブの 0." The Indian-poker code draws the card text itself with the format `"%s %d"` (executable file offset `0x20A4B0`) and four 16-byte suit strings at `0x20A450` (クラブの, ハートの, スペードの, ダイヤの). `exe_patch.set_suits` / `build.SUITS` now write `trébol`, `corazón`, `pica`, `diamante`, giving "La carta de Reu es trébol 7." (the game adds the space before the number; the 0 seen in a start-at-line ISO is only because the jump skipped the card setup). Other card strings may remain in the executable (the `%s（` / `%sＰ` / `%s）` / `%sＡ` formats at `0x20A490`: unverified use). A save-state refresh does not patch these yet.

## 2026-10-25 — Bug: a menu option taken from the executable stayed Japanese

The user tested the start-at-5780 ISO and saw Japanese in the choice box. The second option of the Indian-poker choice (降りる) is `F0000000 2 0x30C910`: a menu option whose pointer goes to the executable's string pool, a form the model only knew for text lines. `script_model` now recognises it (kind menu, `target -1`, text in `exe_text`), `dump_exe`/`exe_strings`/`screens` handle it, and `O0:X006` was added ("Retirarme"). The same form exists in O1 (5), O2 (3 names), O4 (2): they will appear as `X` entries when those files are dumped. The user also saw Japanese in the dialogue box; a scan of every text reference in the rebuilt O0 finds none left, so this needs a screenshot if it persists.

## 2026-10-26 — Debug tools: start a new game at any line, refresh save states

The user asked for save files at chosen points, so testing doesn't need a full playthrough. Their PCSX2 state (`test_playtru_1.p2s`) showed the old pinky-swear overflow: a state keeps the script text that was in RAM when it was saved, so it shows old text after a rebuild. Two tools: `build.py --start <ID>` makes a debug ISO whose new game jumps straight to a line or scene (an OP06 jump after O0's first scene start; the user confirmed it at O0:5780, with no background), and `tools/savestate.py refresh` writes the current translation, font and symbol list into an existing state (the bytecode never moves, so the position stays valid). Creating a state from nothing needs the interpreter's position, which isn't in plain RAM (probably in the script thread's registers): not pursued.

## 2026-10-26 — Control every text by code: script model, screen simulator, jump bug

The user asked for a way to catch layout bugs by code instead of by playing. A read-only look at the bytecode showed how text is really used (instruction-form table in KNOWLEDGE 4.3) and found a **live bug: every Spanish build rewrote the 5 jumps from O0 into O1** (they look like pointers into O0 text); the English patch has the same bug at one site. Done:
- `olm.site_kind`/`text_sites`: only real text references are rewritten; unknown forms stop the build. Translation files re-dumped (2 false O0 parts merged: 0281, 1556; O1-O7 had no Spanish). Tests 4 (pointer forms pinned per file) and 5 (no non-text word changes after a rebuild) added; all pass.
- `tools/script_model.py`: text lines in play order from the bytecode; the build groups lines shown on one screen line from it (fixes 6 O0 groups that the file-order rule got wrong, e.g. a line followed by a page end stored in the executable).
- `tools/screens.py`: lays out every screen from the rebuilt bytes; used by `check.py`, `batch.py check` (so translator/reviewer agents see screen errors) and `build.py` (refuses to build with errors). It found the 5 Japanese pieces O0 takes from the executable, a missing space after each of them, and the card number glued to the word before it ("es7"); all fixed.
- Executable strings: `<script>_exe.txt` (O0 5, O1 3, O5 1); the build appends the Spanish to the script file and points that one instruction at it. O0's translated: Ah... / o sea, / eh... / Mmm. / . ; a space is added automatically before a number the game draws.
- **Real line breaks are now the default** (`build.py --wrap newline`; the user confirmed them in game); `--wrap pad` remains.
- O0 result: 0 errors, 0 warnings on every screen. To confirm in game: the O0 -> O1 transition, the card numbers (5786, 5787, 5803), the Spanish executable strings (2274, 2488, 2491, 5786).

## 2026-10-26 — Bug: menu options were chained with the next text

The user's screenshots after the chain-wrapping change: a menu option showed blank and the line after the menu broke after "...Es verdad". Cause: menu option records (O0:0166/0167, 0407/0408 ...) have no ending code, so `continues` joined them with the following dialogue entry. Fix: menu options are recognised from the bytecode (`olm.menu_starts`: `0xF0000000, n, pointer`) and never chained; `check.py` excludes them from page line counts. Regression risk to watch: any other record type that has no ending code but is not a continuation (none seen in O0 beyond menus). New test ISOs: `MMM_es_newline2.iso` (real line breaks) and `MMM_es_pad4.iso` (padding).

## 2026-10-26 — Second round of in-game feedback

The user sent a screenshot with a 47-character dialogue line overflowing the box (it matches the old ISOs; `ownfont2` already breaks that line) and a list of typos. Causes: (1) entries split inside a sentence were glued without a space ("hacesESO"): fixed in the tool (`join_marked`); (2) two lines could lose a letter or space at a line break ("espacio" for "despacio", "latienda") although the files and built bytes are right: suspected engine behaviour with padded lines; built an experimental ISO that breaks lines with real line feeds instead (`build.py --wrap newline`, `build/MMM_es_newline.iso`); (3) "jajajaja" -> "jajaja" fixed. A full proofreading pass over all 5,935 O0 lines by three independent agents found only 5 more real errors (O0:1022 "del comedor", 3311 and 3405 punctuation, 4856 word order, 5261 comma), all fixed. Spell-check approach: read-only agents write a correction TSV, applied with `batch.py apply --force`.

## 2026-10-26 — First in-game test of the own font: fixes

The user tested `build/MMM_es_ownfont.iso` and found: (1) numbers spelled out where digits read better ("treinta por ciento", "ochenta y ocho años"): rule set (10+ digits, % for percentages, 0-9 words); (2) an entry wrapping to a last line of 8 characters ("tiempos,") wasted a screen line: `check.py` now warns about orphan last lines (<= 10 characters) in entries ending with a line break (10 found in O0, all rewritten); (3) **dialogue lines of 47 characters overflow the box by half a character**, and a word was cut in the middle ("ju|ntos") where two entries continue on the same line: the box shows 46 columns, so dialogue is wrapped at 46 (pad 47), and **consecutive entries on one line are now wrapped as one chain** (`script_text.chain_wrap`, `insert_script.chains`); (4) confirmed: four full dialogue lines fit, which is the limit. 6 dialogue pages that became 5 lines at width 46 were condensed. O0 checked: 0 errors, 0 warnings. All 16 rewrites and 10 number edits are in translation/O0.

## 2026-10-26 — Our own font

With the user's OK I downloaded DejaVu Sans Mono 2.37 (official release zip, 5.5 MB; licence in docs/fonts/) and installed Pillow 13 (pip). `tools/font_build.py` renders the 94 half-width cells (24x24, levels 0-5, 20 px em, baseline row 19); `build.py` now uses it by default and no longer needs work/english (`--font english` keeps the old pilot). **`%` now has a glyph (cell 93, `charmap.EXTRA_SYMBOLS`)**, so the gauge lines at O0:0765, 0775 and 0820s are back to `%`. Mono font, 12 px advance, DejaVu's zero has a dot inside (accepted). Not yet seen in game: the user needs to test `build/MMM_es_ownfont.iso` (the file MMM_es_pilot.iso was locked by PCSX2).

## 2026-10-26 — Batch O0 5700–5932: script file O0 COMPLETE

233 entries (+3 trailing), 19 lines changed by review (~8%: 6 fidelity, 8 naturalness, 3 omission, 1 addition, 1 typo). O0 is 100% translated and reviewed (5,935 entries, 589 NOTE lines to look at). Terms: póker indio (Reu: 'el pólker indio'), 駆け引き = juego mental, 降りる = retirarse, menu 5800/5801 = "Jugármela" / "¡Me la juego!", 黒板 = pizarra, トランプ aside 'toranpu' kept (5746), Presentador/Experto. **Needs in-game check:** card values inserted by the engine at 5786-5787 and 5803-5804 (digits may glue to the text: fallback is a trailing ":"); ③③③ as "333" at 5820 and ② as "2" at 5794. Total 5,935/33,133 (17.9%).

## 2026-10-26 — Batch O0 3900–4199 (300-entry batch #10)

300 entries, 13 lines changed by review (~4%: 4 fidelity, 9 naturalness). The first attempt (2026-10-25) was lost when the translator agent was stopped by a tooling failure; redone. Terms: 購買 = tienda escolar, 幻のパン = el pan fantasma (焼きそばパン = pan de yakisoba), 詰襟 = uniforme escolar de cuello alto, カバン = mochila ("bolso" is a handbag in Mexico), 心配性 = preocupón, 浮気者 = infiel, ホームルーム = hora de tutoría, 小学校 = primaria. Spoken times without 午前/午後 in the Japanese go without AM/PM ("¿Las 8:32?"). 3955: "30 caracteres" (JA says 30; the EN patch changed it to 80). 4073 idiom kept literal on purpose (the next line refers to the pigeon). "¡Pero cómo cree!" -> "¡Claro que no!". Total 4,201/33,133.

## 2026-10-26 — Batch O0 4200–4499 (300-entry batch #11)

300 entries, only 8 lines changed by review (~3%: 4 glossary, 2 naturalness, 2 typo). Terms: 楽したいホルモン = "hormonas de la pereza" ("flojera" is regional; scouting file corrected), bench = "banco" (not "banca"), 手数料 = comisión, 出世払い = "pagarla cuando triunfe en la vida", 下駄箱 = casilleros de zapatos, 保健室 = enfermería, 勲章 = medalla, 一目惚れ = amor a primera vista, 自習 = Estudio libre. Total 4,501/33,133.

## 2026-10-26 — Batch O0 4500–4799 (300-entry batch #12)

300 entries, 32 lines changed by review (~11%: 10 fidelity, 17 naturalness, 2 omission, 1 typo, 1 glossary, 1 register). Key fixes: 4711 reversed meaning, 4766 "tu segunda" spoiled a misunderstanding, 4755 garbled JA clarified. Reu's mishearing of policy: "polítika" dropped (k reads as foreign): Reu asks "¿Qué es una 'política'?". Terms: 三本勝負 = batalla de tres rondas, 行動範囲 = radio de acción, 呼び捨て = sin ningún honorífico, セコンド = segundo/a (ambiguous with 'un segundo' = a moment; alt. esquinero), bug (not error) for the activation fault. User decision: keep segundo/a (not esquinero). Total 4,801/33,133.

## 2026-10-26 — Batch O0 4800–5099 (300-entry batch #13)

300 entries, 20 lines changed by review (~7%: 7 fidelity, 8 naturalness, 2 omission, 2 addition, 1 typo). The menu 4941-4944 is a different format from the earlier ones (4942 ends \k⏎ and 4943 ends \k\p): the labels "A, muchas gracias" / "B, esta vez tendré que declinar" are literal. Fixed: 5051 subject (Hitoe spreads the rumour), 5060 "te enciende" (sexual reading) -> "dan ganas de darlo todo", 4862 silence length. Terms: お見通し = "te leo como un libro abierto", 鬼教官 = instructora implacable, 代返, ギャラリー = multitud, 女装騒ぎ = "el alboroto de vestirme de mujer". Open for the user: contest vocabulary mixes competencia / contienda / batalla de tres rondas (could be unified). Total 5,101/33,133.

## 2026-10-26 — Batch O0 5100–5399 (300-entry batch #14)

300 entries, 14 lines changed by review (~5%: 7 naturalness, 3 fidelity, 2 glossary, 1 omission, 1 register). Terms: 懸垂 = dominadas, 鬼軍曹 = sargento implacable, 特訓 = entrenamiento especial (menú de entrenamiento), ジョギング = trotar, ダッシュ = carreras rápidas, むにゃむにゃ = *murmullo*, あつい (fever) = estás ardiendo ("muy caliente" has a sexual reading), 色目を使う = hacerles ojitos. Total 5,401/33,133.

## 2026-10-26 — Batch O0 5400–5699 (300-entry batch #15)

300 entries, 20 lines changed by review (~7%: 6 fidelity, 8 naturalness, 2 addition, 3 glossary). Fixes: 5484 added subject removed, 5692 "querido" removed (mock-formal usted carries the ojou parody), 5655 全寮制 = "preparatoria de internado". Terms: 返事は一回 = "¡Se responde una sola vez!" (recurs in O1/O2/O4), ぷにぷに = "toc, toc", うりうり = "piqui, piqui" (judgment call, avoids hitting reading), 夕方 = "de la tarde". 5658 poster: codes kept exactly, ☆ = "!". Total 5,701/33,133.

## 2026-10-25 — Batch O0 3600–3899 (300-entry batch #9)

300 entries, 15 lines changed by review (5%). The 5-line dialogue page 3637-3640 was reduced to 4 by moving a clause across the entry boundary (NOTE on both lines; dialogue box height still unverified in game). Terms/open for the user: その道の先輩 = "veterana en la materia" (alt. senpai), サラダオイル = "aderezo" (alt. aceite), 3626 object of 置いておく read as Reu, 一番弟子 = discípula número uno, 心の友 = amigo del alma, にひひ = Jejeje, えへへ = Jijiji, ぶぅ = Buu. Total 3,901/33,133.

## 2026-10-25 — Batch O0 3300–3599 (300-entry batch #8)

300 entries, 16 lines changed by review (~5%: 5 fidelity, 9 naturalness, 1 omission, 1 addition). Terms: 別腹 = "un huequito aparte", 神経過敏 = "estar muy nervioso", 危ない橋 = "algo arriesgado", 皮の上着 = "abrigo de cuero" (chaqueta/chamarra are regional), 悩みの種 = "semilla de mis preocupaciones", お・に・い・さ・ま = "her-ma-no ma-yor~", "coraje" avoided (Mexican) -> "rabia". The 微妙/Delicao callback works (Kyosuke says 'delicado' at 3440 first). Total 3,601/33,133.

## 2026-10-25 — Batch O0 3000–3299 (300-entry batch #7)

300 entries, only 5 lines changed by review (~2%: 2 fidelity, 3 naturalness). Lead's spot audit of 10 random lines: all faithful. The scene is plain prose and the drafts have been good since the checks per 60 entries. Terms: 管理人室 = el cuarto de la encargada, 受付 = Recepcionista, 駄目 = "se puede / no se puede" (matches 2995), father Kyoichi vs older brother Kyohei (恭平). Total 3,301/33,133.

## 2026-10-25 — Batch O0 2701–2999 (300-entry batch #6)

299 entries (+ split 2728.1/.2), 17 lines changed by review (~6%: 12 naturalness, 3 fidelity, 1 addition, 1 omission). Translator ~95k tokens, reviewer ~100k. The lindo/delicado lesson (2822-2881): lindo/a kept (user decision), 微妙 = "delicado", Reu's mishearing 'Delicao' (reviewer: best allowed option; caveat: 'delicao' is a colloquial Caribbean form). Terms: お兄様 = hermano mayor (stilted verb), 言葉のあや = forma de hablar, むさい = desaliñado, 従兄妹 = prima. Open for the user: 'Delicao' wording; 2990 'prima' vs 'primo/a'; 親友 / とも reading gag rendered literally. Total 3,001/33,133.

## 2026-10-25 — Batch O0 2401–2700 (300-entry batch #5)

300 entries, 11 lines changed by review (~4%: 6 naturalness, 3 fidelity, 1 register; 2604-2605 count as one). Translator ~85k tokens, reviewer ~85k. Spot audit by the lead of 8 random lines: good quality (one slightly loose: 2603). Terms: ジャージ = ropa deportiva, お払い = purificación, 寮生A-D = Residente A-D, lone ！ = "¡!", ひゃっく (hiccup) = Hip. Open: 2509/2607 usted for comic effect; 2624 stray-dog idiom literal (alt. "tómalo como un mal rato"). Total 2,701/33,133.

## 2026-10-25 — Batch O0 2101–2400 (300-entry batch #4)

300 entries, 14 lines changed by review (~5%: 3 fidelity, 3 omission, 6 naturalness, 1 register, 1 typo). Translator ~95k tokens, reviewer ~90k. New characters: Motomi Azuma (吾妻もとみ), Misao Yuki (結城みさお). Terms: 神経衰弱 = juego de memoria, ちゃらんぽらん/いい加減 = irresponsable, 面倒臭い = pereza, おふだ = amuleto. Open for the user: 2323 "Misao Yuki-chan" vs "Misao Yuki, Misao-chan"; 2368 who Kyosuke addresses (usted/tú). Review rate is lowest so far: watch it (could mean a good draft or a lenient reviewer). Total 2,401/33,133.

## 2026-10-25 — Batch O0 1801–2100 (300-entry batch #3)

300 entries, 38 lines changed by review (~13%: 25 naturalness, 6 fidelity, 5 register, 1 omission, 1 glossary). Translator ~88k tokens, reviewer ~100k. Terms/pending the user: 合コン = "cita grupal", cat cry フギャッ = "¡Fiau!", ぜ (Ryo) = "amigo.", Tae's ただいま gag = "ya llegué / bienvenida a casa", どういたしまして (sarcastic) = "Gracias por el cumplido", きゅうすけ (slip) = "Kyusuke", Ryo/Kyosuke mock-polite exchange in usted (2081-2083). Menu 1926-1927 format as 0407-0408. Total 2,101/33,133.

## 2026-10-25 — Batch O0 1502–1800 (300-entry batch #2)

299 entries, 28 lines changed by review (~9%: 11 naturalness, 9 fidelity, 6 register, 1 omission, 1 addition). Translator ~93k tokens, reviewer ~105k. Regionalisms removed: antier -> anteayer, echar ganas -> dar lo mejor de mí, ¿Cómo crees? -> ¡Claro que no!. Terms pending the user: 鬼ごっこ = "las atrapadas", かくれんぼ = "las escondidas" (no fully neutral names exist), 鶯張り = "piso de ruiseñor", ファミレス = restaurante familiar, お子さまランチ = menú infantil, ウェイトレス = mesera, セーフティーゾーン = zona segura, 一昨日 = anteayer, 1752 bare "!?" written "¡¿...?!". All Chinese pinyin checked. Total 1,801/33,133.

## 2026-10-25 — Batch O0 1202–1501 (first 300-entry batch)

300 entries, 29 lines changed by review (~10%; earlier 80-entry batches: 8-31%), so the larger size did not hurt quality. Cost: translator ~93k tokens, reviewer ~103k tokens (vs ~45k for 80 entries: about 2.3x for 3.75x the entries). NOTE lines: 1209, 1242, 1252 (pancita), 1260/1339 splits, 1278, 1316, 1403, 1436 (lindo/linda), 1471. Terms pending user OK: いただきます = "Buen provecho" (reviewer; translator had "Gracias por la comida", which is kept for ごちそうさま at O0_019:865-875), 高蛋白剤 = suplemento proteico, 冷蔵庫 = refrigerador, 押入 = clóset, そっちのおなか = "esa pancita". Total 1,502/33,133.

## 2026-10-25 — Terms approved, 悪友 = cómplice, batches of 300

The user approved the whole pending-terms table (tanque de vidrio, almacén, baño, doppelganger, Accesorio, barra, conexión a tierra, enchufe, primera activación, Heeey, canasta, tienda de conveniencia, bento, por ahora/por lo pronto, pan de molde, canal público, dinero para mis gastos). 悪友 changed from "compinche" to **"cómplice"** (applied at O0:0574 and 0577). Batch size raised from 80 to 300 for the next batch (compare review corrections per line with the 80-entry batches). 

## 2026-10-25 — User decisions: Murasaki, Reu's sobs

紫の上 = "mi pequeña protegida" (applied at O0:1171). Sobs: "Snif" for tearing up/sniffling, "Hip" or "Snif... hip..." for catching breath/hiccuping. "Fueh" confirmed. The user is open to larger batches.

## 2026-10-25 — Batch O0 1122–1201

80 entries, 15 changed by review (7 fidelity, 6 naturalness, 2 glossary, 1 omission). NOTE: 1171 紫の上 = "mi Dama Murasaki" (Genji Monogatari reference, user may prefer another solution). Terms: 食堂 = comedor (also fixed O0:1042 area line 117 'cafetería' -> 'comedor'), 小遣い = "dinero para mis gastos", 仕送り = "el dinero que me envían", 食パン = pan de molde, 国営放送 = canal público, おいしい (perk) = "no está nada mal". Total 1,202/33,133.

## 2026-10-25 — Batch O0 1042–1121

80 entries, 16 changed by review (10 fidelity, 1 omission, 1 addition, 3 naturalness, 1 typo). NOTE lines: 1065 ('Hermano'), 1121 (pinyin). Terms: アルビノ = "albino", カラーコンタクト = "lentes de contacto", もこもこ = "Peludito", "déjà vu" avoided (à not in the font; use a paraphrase). Total 1,122/33,133.

## 2026-10-25 — Batch O0 0962–1041

80 entries, 6 changed by review (3 fidelity, 2 glossary, 1 addition): the screen messages now match the earlier wording ("Accidente en la primera activación", "La configuración finalizó con éxito -- Disfrute de su vida con Reu."); STORY.md corrected. Reu's sounds: Hic, Buaaan, Uaaan, Fuaaan, Bueh, Fueh; しゃっく = "Snif" (alt. "Hip", pending user). 男子棟 = "edificio de los chicos". First words ...bre / Hambre / Tengo hambre. Total 1,042/33,133.

## 2026-10-25 — Batch O0 0882–0961

80 entries, 20 changed by review (12 fidelity incl. tense fixes, 1 omission, 5 naturalness, 1 typo). Reu's first sounds: ふぇ = "Fueh", crying "Fueeen"/"Uaaan" (keep the final n); 不可抗力 = "fuerza mayor"; 年甲斐もなく = "como un niño a mi edad"; "pena" avoided (embarrassment in Mexico) -> "lástima". Pending user OK: the sound spellings (alt. "Fweh"). Total 962/33,133.

## 2026-10-25 — Batch O0 0802–0881

80 entries, 25 changed by review (11 fidelity, 8 naturalness, 3 glossary, 2 addition, 1 omission, 1 typo). Terms pending user OK: ゲージ = "barra" (not indicador), アース = "conexión a tierra", おーい = "Heeey", 初回起動 = "primera activación", コンセント = "enchufe". No % used. Total 882/33,133.

## 2026-10-25 — Batch O0 0722–0801 and a checker gap

80 entries, 12 changed by review (6 fidelity, 4 naturalness). **Found:** `%` is ASCII, so the checker accepted it, but it has no glyph in `haff_opt` and would not draw. `charmap.encode` now rejects any ASCII symbol outside letters, digits, `? ! ' \" ( ) . , - : ; / * ~` and Spanish accents (also `+ = < > & @ # $ [ ] ^ _ { | } ` backtick). 0765 became "-- 1 -- 2 -- 3 -- 4 --" and 0775 "32 por ciento"; restore `%` when our own font adds the glyph (PLAN: own font). Terms: Ingrese (not Introduzca: Spain), computer UI: botón Inicio/Finalizar/Confirmar, hacer clic, barra/indicador, nanorrobots; personality options Alegre/Intelectual/Serena/Amable. Total 802/33,133.

## 2026-10-25 — Batch O0 0642–0721

80 entries, 10 changed by review (8 fidelity, 1 omission, naturalness/glossary). Terms: 洗面所 = "baño" ("lavabo" is a sink in Latin America; alt. lavamanos), 付属 = "Accesorio --" (alt. Extra/Adicional), レプリス plural = "los Repliss", 起動 = activación, パソコン = computadora. Total 722/33,133.

## 2026-10-25 — Batch O0 0562–0641

80 entries, 18 changed by review (7 fidelity, 3 omission, 2 addition, 5 naturalness, 2 register). 0641 time written "Son las 3:13 AM." (JA has no AM/PM; inferred from the sleepless night in 0636; the user may confirm). Removed regionalisms ("ruidero", "Va"→"Okey"). Terms: 悪友 = compinche; Ryo Hagimoto; Ryo-kun/Kyosuke-kun/Tae-san kept. Total 642/33,133.

## 2026-10-25 — Batch O0 0482–0561

80 entries, 24 changed by review (8 fidelity, 4 omission, 3 addition, 5 glossary, 7 naturalness). Terms pending user OK: 水槽 = "tanque de vidrio" (translator had "pecera"), 物置 = "almacén" (alt. cobertizo: would change 0480, 0492, 0509), ワレモノ = FRÁGIL, 天地無用 = ESTE LADO ARRIBA, とりあえず = "por ahora"/"por lo pronto". Total 562/33,133.

## 2026-10-25 — Batch O0 0402–0481

80 entries, 17 changed by review (6 fidelity, 1 omission, 5 glossary = "Tae-san" restored where the translator had dropped it, 4 naturalness, 1 register, 2 typo). First menu (0407-0408 Recordar/No recordar) and \LC poster (0413) handled. Names: Tae Kizuki, Kyoichi Watarase; アニキ = "mi hermano mayor"; オヤジ = "mi viejo"; リヤカー = carretilla (alt. carrito de mano). Total 482/33,133.

## 2026-10-25 — Batch O0 0322–0401

80 entries, 13 lines changed by review (4 fidelity, 8 naturalness, 1 typo); no NOTEs. Reu's えらい = "¿Lo hice bien?" (not "buena"). Total 402/33,133.

## 2026-10-25 — Batch O0 0243–0321

80 entries, 11 changed by review (6 fidelity, 2 omission, 2 naturalness, 1 glossary). NOTEs left: 0252 bento, 0253/0312 idiom, 0283 pinky-swear, 0285 Hitoe-san. Pending user OK: ドッペルゲンガー = "doppelganger" (reviewer; translator had "doble"), 買い物カゴ = canasta, コンビニ = tienda de conveniencia (alt. tienda 24 horas), 弁当 = bento. Total 322/33,133.

## 2026-10-25 — Batch O0 0163–0242

80 entries translated and reviewed (11 changed: 6 fidelity, 3 naturalness, 1 glossary, 1 register); no NOTE lines. Also fixed O0:0154 to "Kyosuke-san" (honorifics decision). Glossary decided by the user (with refinements): 全寮制 = "preparatoria de internado", 帰省 = "volver a casa de la familia", 幼稚園 = "kínder"; applied to O0:0170, 0174, 0192. Total 242/33,133. Review: `translation/reviews/O0_0163-0242_review.md`.

## 2026-10-25 — User decisions after the O0 scout

Scout output: `docs/scouting/O0.md`. Decisions: (1) Tae = "la encargada suplente" then "Tae"; her mother stays "la encargada". (2) かわいい lesson: "lindo/a" + NOTE. (3) ②/③/☆ as 2/3/! (the user will check in-game whether circled digits show). (4) おにいちゃん = "hermano". (5) **Honorifics are kept** (-san/-chan/-kun/-senpai), overriding the scout's proposal to drop them, because they are Japanese culture. (6) Chinese lines in pinyin without tones. (7) Repliss and Tyrell Bio Corporation unchanged. (8) Pinky-swear gag translated with a NOTE. Style guide updated.

## 2026-10-25 — Story bible and read-ahead pass

**Question from the user:** should everything be translated at once for consistency and wider context? **Answer:** no (33,000 entries can't be held in one context, nor reviewed, and a wrong approach would be wrong everywhere); consistency comes from shared memory read by every batch.

**Built:** `docs/STORY.md` (setting, characters, scenes so far, running motifs; seeded from O0 1–162; ≤6 lines added per batch; ≤~300 lines); `tools/scout.py` (digest of a whole script: 6 KB for O0) and the `mmm-scout` agent that reads it plus samples and writes `docs/scouting/<script>.md` (scene map, term proposals, wordplay, hazards, questions); translator and reviewer now read STORY.md and the scouting file and report story notes; `/translate scout <script>` and the updated `/translate <script>` skill; workflow doc has a "Shared memory" section. Not yet run: the first real scout (O0).


## 2026-10-25 — User decisions on batch O0 0083–0162

| Question | Decision |
|---|---|
| Time format | `10:03 AM` (short, fits better) |
| Shop モノクロ | "Monocromo" |
| Slurred greeting いらっさいませ | "¡Bienvenío!" ("¡Bienveníooo!" when stretched with ～; the alternative "¡'Veníooo!" dropped) |
| Hitoe's ひとえ様 | "la gran Hitoe Haruna" |
| Vocabulary | "hacer fila", "qué se le va a hacer" OK |
| Clerks 店員 | "Empleado A/B/C", "los empleados" (they're shop staff; "dependiente" sounds Spanish) |
| Surname | Haruna, given name first as in the English patch |
| 幼なじみ | "amigo/amiga de la infancia" |

Applied to O0:0083, 0107–0109, 0112; resolved notes removed from 0083, 0088, 0107, 0109, 0114, 0156. Added to STYLE_GUIDE.md (characters and terms) and TRANSLATION_WORKFLOW.md (time format), so the agents use them from the next batch.


## 2026-10-25 — First workflow batch: O0 0083–0162

`/translate O0`: 80 entries (the shopping-street scene from "10:03" to Hitoe's first lines). Translator: 0 errors after one self-correction (O0:0156 shortened to the 4-line dialogue budget), 8 notes. Reviewer: 17 of 80 lines changed: naturalness 9 (regionalisms "ni modo", "formada", "anda" removed; calque "más importante aún"), fidelity 5 (the ダメ→ダメ過ぎる joke, 0100, 0143, 0145), omission 3 (0088, 0101, 0161); no additions, register or budget problems. Applied with 0 errors; review report copied to `translation/reviews/O0_0083-0162_review.md`. Open for the user: 20 notes in O0 (8 from this batch plus review notes) and glossary proposals (shop モノクロ = "Monocromo", time format "10:03 de la mañana", Hitoe Haruna, Dependiente A/B/C, "amiga de la infancia", "hacer fila").


## 2026-10-24 — Translation workflow

**Looked at** https://github.com/senshinji/claude-translation-skill (MIT, one commit, not updated in 7 months): a document-translation skill (docx/pdf) using Claude Code's experimental Agent Teams with translator, term researcher, reviewer, revision and typesetting roles. **Not used as is** (no support for our line/page limits, character set, codes or file format; needs an experimental setting). **Borrowed ideas:** separate translator and independent reviewer, line-by-line anti-fabrication/omission checklist, structured review output.

**Built:** `tools/batch.py` (next / check / apply / status, with `NOTE:` support), `docs/TRANSLATION_WORKFLOW.md` (the rules both agents follow: limits, page-by-page method with a line budget, condensing, voice, the checklist, output formats), `.claude/agents/mmm-translator.md`, `.claude/agents/mmm-reviewer.md`, `.claude/skills/translate/SKILL.md` (`/translate O0`). Self-test: a draft with a reserved symbol, a typed code, an empty line, an unknown ID and an over-long dialogue was rejected with exactly those messages and not applied; a valid draft with a note applied, and re-applying without the note restored the file byte for byte.

**Decisions**
| Decision | Choice | Why |
|---|---|---|
| Unit of work | batch of ~80 entries, extended to a page end | fits an agent's context with Japanese + English + rules; pages are never split across batches |
| Translate by | page, with a line budget | the pilot showed entry-by-entry translation overflows or wastes pages |
| Review | independent agent + human | the human keeps final say; notes and the review report make that fast |
| Applying | only through `batch.py apply` after `check` | a bad draft can't reach `translation/` |


## 2026-10-24 (pilot round 1) — first Spanish screens; the 10-line page limit

**Round 2 (user):** the `<PAGE>` splits worked (page 4–5 showed 6 lines, `ñ` renders), but the user judged a 6-line page with a lot of empty space "wrong". Cause: Spanish is ~40% longer than the Japanese layout (entries 4–7: 9 Japanese lines, 13 Spanish), and I translated entry by entry without a page budget. **Decision: translate page by page with a line budget and condense the wording so pages fit in ≤10 lines; use `<PAGE>` only where a natural break is unavoidable.** Re-did the three long pages condensed (now 10, 10 and 10 lines, no `<PAGE>` used), rebuilt the pilot. Also added `speakers.py` and seeded the character table: 19,186 spoken lines, 9 main speakers.

**User test of `MMM_es_pilot.iso` (10 screenshots):** accents, `, . ... --`, the 47-column wrap, the dialogue box and the Japanese resuming at "10:03 AM" all worked. **Bug:** narration pages of 13, 13 and 11 lines (entries 4–7, 8–13, 28–31) showed 10 normal lines, then squashed glyphs and vertical bars on lines 11+. Pages of 9 and 10 lines were fine.

**Why my tools missed it:** `check.py` only looked at single entries, and my earlier "page report" compared Spanish with the English patch, assuming English fits (it doesn't always: the English patch's own README admits layout problems). Lesson: **measure the real limit, don't infer it from the reference.**

**Fix:** `check.py` now groups entries into pages (narration = `\FS` run up to `\k\O`) and errors above 10 lines; `<PAGE>` (KNOWLEDGE.md 4.10) lets a translator end a page early; the three long pages were split (after entries 5, 10 and 29: pages are now 6+7, 7+6, 6+5 lines). `build.py` runs the checker, so an overflowing page can't be built any more. Removed `page_report.py` (folded into `check.py --pages`).

**Also noted:** I see no accent glyph bugs in the screenshots, but `¿ ¡ ñ ü Á Ñ` haven't appeared in the screens sent so far; round 2 should show them (entries 47 `¿¡`, 4 `ñ`, 3 `Á`...).


## 2026-10-24 (Phase 3/4) — checker, build script, first Spanish pilot ISO

**Done:** `check.py`, `build.py`, `font_tool.py`, `apply_translations.py`, `page_report.py`; drafted Spanish for **O0 entries 1–82** (opening narration + morning scene, up to the scene change at "10:03 AM"); built `build/MMM_es_pilot.iso` (O0: 38 lines in place, 44 appended; O0 ends at `0x551400`, within the original memory; executable in place; heap start `0x5D0000`). Read-back through the ISO's own pointers confirmed the text, the stand-in accents, the 47-column padding and the untouched Japanese from entry 83 on.

**Translation choices** (STYLE_GUIDE.md): names as in the English patch (Kyosuke, Reu); "residencia" for 寮; "la encargada" for 寮母; "futon" and "Golden Week" kept; tú between the young characters; speaker names inline (`Kyosuke: "..."`); `...` and `--` instead of `…` and `──`. Spanish pages need about as many screen lines as the English ones (`page_report.py`: equal or ±1).

**Pilot caveats:** the pilot ISO uses the English patch's glyphs (plus accents composed from them), so it's for local testing only and must never be published; menus and system text are still Japanese; the Japanese title screen etc. are untouched. Unknown until tested: whether a Spanish narration page overflows the text box, and the dialogue window width.

**Housekeeping:** removed the experiment scripts (`make_font_test*`, `make_bisect`, `make_accent_test`, `make_roundtrip`) since their results are documented.


## 2026-10-24 (Phase 3 start) — dump/insert pipeline and tests

**Done:** `dump_script.py`, `insert_script.py`, `script_text.py`, `project.py`, `test_pipeline.py`; generated `translation/` (184 files, 33,000 entries, 5.4 MB). Format and workings: KNOWLEDGE.md 4.10. Round-trip tests all pass.

**Bugs found by the tests (each would have corrupted the game, so they were worth writing):**
1. A mid-line pointer that landed on the second byte of a Japanese character (a false positive in O2). Now ignored.
2. `str.strip()` also strips the Japanese full-width space, which some records end with, so a round-trip silently changed a few bytes. Now only plain spaces are stripped.
3. Pointers that land on the ending codes of a record (e.g. the `\p` of `\k\p`) were treated as text parts and duplicated the ending. They now follow the ending.
4. Records with only some parts translated were pushed through the Spanish encoder; untranslated parts now keep their original bytes.
5. My checker was too strict about the padding of two-part records (false alarms). Fixed the checker, not the tool.

**Decisions**
| Decision | Choice | Why |
|---|---|---|
| Who edits what | Only the `ES:` line; start/end codes re-attached automatically | Fewer ways to break a line; codes are the same for the same record |
| Wrapping | The tool wraps and pads to 47 | The engine's own wrap loses a character (4.7) |
| Placement | In place when it fits, else appended | Keeps O1 within memory (Test 3: 730 KB of 969 KB with English-length text) |
| Typographic characters | Converted automatically (`… “ ” ‘ ’ — –`) | Translators and editors insert them by habit; the font has none of them |
| Tooling/environment | Shell heredocs mangle `\n` in edits here | Use the Edit/Write tools for code with backslashes |

**Next:** `check.py` (lint), the executable's menu/system strings, our own font, `build.py` + `.bps`, then the Phase 4 pilot.


## 2026-10-24 (end of day) — Spanish characters proven in PCSX2

**Result of `MMM_accent_test.iso` (user screenshot, Message History):** `¿Qué tal, niño? ¡Sí, señor! Canción, pingüino.` / `ÁÉÍÓÚ ÑÜ áéíóú ñü: "comillas", (paréntesis) - f` / `n.` / `¡Hola, Paqui!` All 16 Spanish characters and the punctuation display. **The biggest technical risk of the project is resolved.**

**New observation:** line width is 47 characters; the 48-character line lost its `i` at the engine's automatic wrap. So the insertion tool must pre-wrap at 47 (like the English patch's space padding).

**Decisions**
| Decision | Choice | Why |
|---|---|---|
| Spanish characters | Stand-in ASCII symbols + relocated `haff_opt` (`tools/charmap.py`, `tools/exe_patch.py`) | Proven to work; no engine code changes beyond two `lui` instructions |
| Release font | Draw our own glyphs | The test used the English patch's bitmaps, which aren't ours to redistribute |
| Line wrapping | Our tool pre-wraps at 47 | The engine's wrap drops a character |


## 2026-10-24 (late night) — Font test 1 result: the hypothesis failed

**Result of `MMM_font_test1.iso` (user, as three *screens*):** screen 1 showed `Hello! 0123456789 ABC xyz ?!'"()`, screen 2 showed `END`, screen 3 showed `hola paqui`.
- The symbols screen (`#$%&+<=>@[]^_` …) never appeared (a screen with nothing drawable is skipped).
- The English line was cut after `)`: the 8 symbols `. , - : ; / * ~` that followed drew nothing.
- The five half-width katakana bytes drew nothing, but ` END` after them did.
- So letters, digits, space and `? ! ' " ( )` draw; everything else I tried is silently skipped. **My hypothesis (all 33 ASCII symbols map onto cells 62–94) is wrong, or incomplete.** Cells 77–94 are NOT reached by those symbols, and even `. , - : ; / * ~` (cells 69–76 in the English font) did not draw in our build, although the English patch shows them.
- **Good news:** the font injection works (English glyphs appear), the in-place executable is fine, and the `\k\p` ending fixed the hang.

**Things checked while investigating:**
- The "other data" at font cells 362–383 that the English patch also changed is **menu text** (Japanese `セーブ`/`ロード` → `Save`/`Load`), not glyphs. So the only glyph cells the English patch changed are 0–67 and 69–76.
- In all eight script files, the English patch changed **only text records, their pointers, and the size fields**; nothing else (re-checked properly after a first, sloppier check). So no engine data hides in the script files.

**Open question:** why do `. , - : ; / * ~` draw in the English build but not in ours? Candidates: they need something else the English patch changed (an executable table I haven't identified), or the `\FS` narration style uses a different glyph source than normal text, or the characters need a different mapping.

**Built `MMM_font_test2.iso`** (7 screens, symbols placed between letters so an invisible symbol is obvious; with and without `\FS`; full-width punctuation; half-width katakana; "hola paqui" last). User to screenshot or describe each screen.

**Result: test 2 hung.** Differences from the working test 1: (a) plain text (no `\FS`) in the first three opening screens, (b) the third opening record lost its original ending `\k\O`, (c) two-byte Shift-JIS and high bytes (0xA1, 0xA5, 0xDF) in S5/S6.

**Hypothesis:** the first three opening records are the narration screen (`\FS … \FE`), and `\O` at the end of the third one opens the normal message window. Plain text before `\O` has no window to draw into and the game waits forever. **(unverified)** Test 1 kept the `\O` and worked.

**Second result: both rebuilt test 2 ISOs (including the ASCII-only 2b) hung.** So the `\O`/window idea was wrong, or at least not the cause. Looking at the whole opening in the original script (see KNOWLEDGE.md 4.3, "Structure of the opening"):
- The opening is a long **narration** of records that all start with `\FS` and end `\FE\t60`; narration **pages** end with `\k\O` (records `0x1D0`, `0x350`, `0x550`, `0x6C0`, `0x7F0`, `0x8A0`, `0xA40`, `0xBD0`: 8 pages). Normal dialogue (plain text, `\k\p`) only begins at record `0xC30`.
- Test 1 (works) replaced only records that kept the narration style. Tests 2/2b (hang) put plain text at `0x230`/`0x2A0`, still inside the narration.
- **Revised hypothesis: plain text (no `\FS`) inside the narration section hangs the game.** (unverified; consistent with all four results so far.)

**Built test 3** (`tools/make_font_test3.py`, replaces the test 2 script): narration screens S1/S3 stay `\FS`; plain-text screens S2/S4 and "hola paqui" go in the dialogue (`0xC30`+), which means about 8 confirm presses through the narration first. `test3` is ASCII only; `test3b` adds the full-width screen S5 (narration, `0x1D0`); `test3c` adds the katakana screen S6 (dialogue, `0xCE0`). Obsolete test ISOs deleted from `build/` (regenerable).

**Result: all three test 3 ISOs hung too.** So "plain text in narration" was not the (only) cause either. Re-comparing every result: the only content present in all hanging tests (2, 2b, 3, 3b, 3c) and absent from the working test 1 is **symbols directly next to digits** (`1#2$3%4&5+6<7=8>9@0[1]2^3_4`5{6|7}8`), always on the first page. New hypothesis: some symbol+digit sequences are engine codes (format/variable markers like `%4`, `@0`, `[1]`, `{6|7}`) and a malformed one hangs the page layout. **(unverified)** The earlier "plain text in narration" conclusion is withdrawn: it was never isolated.

**Built test 4** (`tools/make_font_test4.py`): `test4` = punctuation between letters only; `test4b` = the symbols between `K`s, no digits, no `%`; `test4c` = `1#2$3%4&5`. Each also has plain dialogue screens (S2, "hola paqui") after the narration.

**Result: all three test 4 ISOs hang, with FPS 0 / Speed 28% (EE stuck, a hard freeze), even `test4` whose only first-page change is plain punctuation between letters.** Since every build after test 1 hangs regardless of content, the content theories for tests 2–4 are unproven. **Mistake: no control test was run.** Next: user boots the original ISO and `MMM_rt_B_all.iso` (known good earlier) to rule out an emulator/save-state/memory-card change before any more theories.

**Control test (user): the original ISO and `MMM_rt_B_all.iso` both still work.** So the emulator is fine and my builds are at fault. Checked: the executable in the frozen builds differs from the original only in font cells 0–94 and the advance byte (same as the working test1b); the 3 mid-record pointers are not in any replaced record. The screenshot shows the "continue" arrow on an empty page, so the freeze happens while processing the first page.

**New hypothesis:** every frozen build begins record 0x100 with my label right after `\FS`: `\FSS1`, `\FSS3`, `\FSS5`. `S` + digit there probably parses as a code with a numeric argument (like `\t60`). Test 1 and the English script never have that. Built test 5: `test5` = same tests without labels; `test5b` = only `\FSS1 abc` (should freeze if right). Lesson: **test labels must not touch control codes.**

**Result: test 5 (no labels) and 5b both freeze.** The label theory is wrong too. Third wrong guess in a row, so I switched method: **one-change-at-a-time bisect from the last build that worked** (`tools/make_bisect.py`). Core tools are unchanged since that build (`git diff 567e286` touches only test scripts). `MMM_bisect_A` = font test 1 exactly (control); `B` = A + visible text "Hello" in the first record (0x100); `C` = A + `A.B,C-D:E;F/G*H~I` in record 0x180; `D` = A + `S1 abc` in record 0x180.

One thing I noticed: in the working test 1, the user never saw the first record's screen (it contained only symbols that don't draw). Every frozen build has **visible** text in record 0x100. B tests exactly that.

**Bisect round 1 (user): A works, B works, C freezes, D freezes.** Visible text in the first record is fine (B). Replacing record 0x180 with `A.B,C-D:E;F/G*H~I` (C) or `S1 abc` (D) freezes. The "uppercase + non-lowercase at the start" idea was killed by the English script (it has narration lines starting `I ` and `A `). The English text also has lines like `I.` and `A-` and draws `.` and `-`, while our build doesn't: **our build is missing something the English executable has.**
- Checked the English-changed table at `0x9D164`: it's chapter/scene titles ("Prologue", "Opening", …), not a character table.
- **Prime suspect now:** the word at RAM `0x1999DC` (file `0x99B5C`), which the English patch raises from `0x560D00` (= end of the largest original overlay) to `0x5D0000`, and which **none of my builds changed**. If it is the heap start (unverified: I could not find the code that reads it), loading our ~846 KB `O0` (ends `0x5A1F00`) overwrites live heap data, and what breaks would depend on exact byte contents. That fits the seemingly random, content-dependent freezes, and rt_B working by luck.
- Built `MMM_bisect_C2` and `MMM_bisect_D2`: C and D plus only that word raised to `0x5D0000`.

**Bisect round 2 (user): C2 and D2 both run normally (FPS 60).** **Root cause of every freeze since font test 1 found: the memory-limit word at RAM `0x1999DC` must be raised (to `0x5D0000`, like the English patch) when `O0` grows past `0x560D00`.** All my text-content explanations (bare `\k`, plain text in narration, `\FSS1`) are retracted; they were coincidences of which bytes overwrote memory. KNOWLEDGE.md 4.3 and 4.5 corrected.

**Still open:** C2's second screen read `ABCDEFGHI`: `. , - : ; / * ~` not seen. But the English patch's own screenshot of this scene shows `, . : " --` drawing, and a full enumeration of the English executable changes found no character table: everything is strings, pointers, the font cells, the advance byte and the memory word. So in our C2 they should draw. Either they are there but too small to notice, or something is still different. Asked the user for a close screenshot of that screen.

**Screenshot of C2's second screen:** `ABCDEFGHI`, evenly spaced: the symbols are **skipped entirely** (no space taken), not drawn invisibly. The Message History (backlog) also shows `ABCDEFGHI`, so the symbols are dropped when the text is **parsed and stored**, not at drawing time. The English script uses the very same bytes (`,` = 0x2C, `.` = 0x2E, checked in hex), but there they always follow a lowercase letter (`dorm,`, `awakening.`). Built `MMM_bisect_E.iso` (memory fix included) with one line testing contexts: `dorm, A.B a.b 1.2 x-y A-B test. ok`.

**Bisect E (user screenshots):** `dorm AB ab 12 xy AB test ok`: every symbol dropped regardless of context, also in Message History. So something the English executable has was still missing.

**Found it.** Listing *all* 110 changed regions of the English executable (my earlier listing hid small text-looking ones) showed 8 bytes at file `0x20C91F`: zeros → `.,-:;/*~`. Then the executable turned out to contain its **full symbol table and relocations** (KNOWLEDGE.md 4.9). The bytes are the variable **`haff_opt`**, the list of allowed half-width symbols, used by `kanjiRomAdrOriginal`: list position i → glyph cell 62+i; not in the list → dropped. The `heap` section at `0x560D00` confirms the memory word. Also corrected the font grid origin to file `0x1B7D30`.

**Built `MMM_accent_test.iso`:** list moved to segment 9 at `0x5C0000` with 16 stand-ins for Spanish characters, accented test glyphs in cells 77–92, heap `0x5D0000`, advance 13, three Spanish screens. New tools: `elf_symbols.py`, `exe_patch.py`, `charmap.py`, `make_accent_test.py`.

**Lessons:** (1) when diffing against a reference patch, list *every* change, not just the ones that look interesting; (2) check for symbols/debug info in a binary before reverse engineering it by hand; (3) always run a control test before trusting a new failure.

**Superseded rebuild note:** `MMM_font_test2.iso` now keeps the opening structure (three `\FS` screens, the third ending `\k\O`, then plain screens after it), and `MMM_font_test2b.iso` is the same structure with ASCII only (no two-byte, no high bytes) to bisect. Rule for future tests: **keep the original opening structure; put plain-text test screens only after the `\O`.**


## 2026-10-24 (night) — Font decoded; mapping test built

**Done**
- Explained pointers to the user and added a worked example to KNOWLEDGE.md 4.3.
- Decoded the font format: 24×24 px, 4 bpp, 288-byte cells, grid origin `0x1B7D44`, six gray levels. The key was a bounding-box search over cell alignments: the glyphs only look clean once the grid origin is right (my earlier renders were a few bytes off).
- Identified cell order (digits, A–Z, a–z, punctuation) and the occupancy map (4.6). Original cells 0–61 are full-width Latin; English replaced them with narrow glyphs.
- Wrote `tools/mips.py` (small MIPS disassembler; we didn't want to download one without asking) and used it to understand every code edit in the English patch (4.5). Biggest surprise: **the English patch changed no text-decoding code**, only glyph pictures, string pointers, the half-width advance (12→13) and a probable free-memory constant (`0x560D00`→`0x5D0000`).
- Searched the code for the char→cell mapping (arithmetic constants, lookup tables, Shift-JIS range checks): all false leads (script opcode dispatcher, `strtol`-style parser, GS register setup). No table exists; the mapping is computed some other way.
- Built `build/MMM_font_test1.iso` to test the hypothesis that the 33 ASCII symbols map onto cells 62–94, leaving 18 blank cells (77–94) free for accented letters.

**Decisions**
| Decision | Choice | Why |
|---|---|---|
| Find the mapping by experiment, not by reading more code | Test ISO with recognizable letters in the blank cells | Several code searches came up empty; a screen test answers it directly and also tests our font injection |
| Don't download a disassembler | Wrote `tools/mips.py` | Downloading needs the user's OK, and ours is small and reusable |

**Result of the first font test ISO: it hung on "New Game" (stuck loading).** It differed from the working round-trip test B in two ways: the executable had been **moved** (appended at the end of the disc, because my builder only appended) and the font/text content had changed. Leading suspect: the moved executable, since the English patch never moves it and our earlier tests only moved `OLM/O0`. **Cause not confirmed.**

**Response:** `iso_build.py` can now overwrite a file in place (same LBA). Rebuilt the test with the executable in place (`MMM_font_test1.iso`, font + test lines) plus `MMM_font_test1b.iso` (executable in place, font changes only, original text) so a second failure can be pinned on the text or on the font. Rule from now on: **write `SLPS_251.92` in place.**

**Second round (user): test1 hangs, test1b does not.** So the font injection and the in-place executable are fine, and the hang comes from my test text lines. (The "moved executable" suspicion is therefore not what hung test1; whether moving it is harmful is still untested, but keep it in place anyway, like the English patch.)

**Hypothesis for the hang:** my first two test lines ended with a bare `\k`. Counting the real script (all eight files, original and English): `\k` is followed by another code (`\p` or `\O`) in about 31,200 of about 31,400 cases and by a newline in most of the rest. Never by nothing except once. So the script reader probably expects something after `\k`. Fix: end lines with `\k\p`.

**Third round built:** `MMM_font_test1.iso` (lines 1-3 with `\k\p`, plus a 4th line "hola paqui" as a shout-out to the user's friend, test ISO only), and three single-line ISOs `test1c` (line 1 only), `test1d` (line 2 only), `test1e` (line 3 only) to bisect if the full one still hangs.

**Next:** user boots test1, then test1b if test1 still hangs. If test1 works, read the three test lines to get the symbol→cell mapping. If the hypothesis holds, accented letters go into cells 77–94 and Spanish text uses those ASCII symbols as stand-ins. If not, plan B is to patch the engine's character mapping.


## 2026-10-24 (evening) — Round-trip tools and test ISOs built

**Done**
- `tools/olm.py`, `tools/iso_build.py`, `tools/make_roundtrip.py` (see KNOWLEDGE.md 5.1 and 4.8).
- Built `build/MMM_rt_A_partial_marked.iso` and `build/MMM_rt_B_all.iso`; both passed the static checks. Not yet booted.

**What went wrong first, and the fix (worth remembering)**
- My first record detector assumed every text record is 16-byte aligned and padded to 16. The audit against the English answer key showed 24 pointers missed. Cause: short records (`\k\p` etc.) are packed with only 4-byte alignment. Fixed; the audit now finds all 2,283 changed English pointers, with none missing. Lesson: always audit a parser against the English files before trusting it.
- The disc names extension-less files with a trailing dot (`OLM/O0.`); `iso_build` accepts both spellings.

**Decisions**
| Decision | Choice | Why |
|---|---|---|
| Two test ISOs instead of one | A = partial and marked, B = all text | B's O0 ends at RAM `0x5A1F00`, beyond anything the English patch uses. If B breaks we need to know whether pointers or RAM size is to blame; A isolates the pointer question inside the original RAM budget |
| Marker in test A | `◆` before each relocated line, `[OLD]` in abandoned slots | Makes both "new copy is being read" and "a pointer was missed" visible on screen |
| Zero the old slots in real builds | `old='zero'` | Same as the English patch; a missed pointer then shows up as blank text instead of silently working |

**Result (user tested in PCSX2): A and B both pass.** The ◆ shows on A's relocated lines and B looks identical to the original. The insertion method is proven, and an O0 ending at RAM `0x5A1F00` runs fine in normal play.

**Still open:** what is in RAM after the overlay area, since the larger overlays (O1…) haven't been tested at large sizes. The original executable reserves up to `0x560D00`; the English patch moved a dummy segment there to `0x5C0000`, possibly to protect memory above it. Revisit when we build big overlays, or if a crash appears.

**Next:** the font. It decides whether Spanish accents are possible, and it's now the biggest remaining risk.


## 2026-10-24 (later) — Phase 2 started: script layout understood, font not yet

**Done**
- PCSX2 v2.4.0 installed and set up with the user's own BIOS (US BIOS is fine). The user confirmed that **both** the original ISO and the English-patched copy (`build/MyMerryMay_EN_test.iso`) boot.
- Mapped `OLM/O0`: text records (NUL-terminated, 16-byte aligned) versus bytecode regions (32-bit words: `0xF000_00xx` opcodes and `0x4D3600+offset` pointers).
- Used the English `O0` as an answer key: its bytecode is byte-identical in position, 2,283 pointers were redirected to text appended at the end of the file.
- Tried to decode the font bitmaps (4 bpp 24×24, 4 bpp 12×24, 2 bpp 24×24): none gave clean glyphs, so the layout is still unknown.

**Decisions**
| Decision | Choice | Why |
|---|---|---|
| Text insertion method | Always append all translated text at the end of each `O*` file and rewrite every text pointer | It's what the English patch does, and it avoids the problem of Spanish lines not fitting the Japanese slots |
| Prove it before translating | Do a no-change relocation round-trip and boot it in PCSX2 first | Catches missing pointers cheaply; translation is the expensive part |

**Next**
- Round-trip tool for O0 (dump, relocate, repoint) and a PCSX2 boot test.
- Font: figure out the real bitmap layout (likely swizzled) and the code-to-glyph mapping. Ideas: look at how the engine code indexes the font; compare against known 4bpp swizzle layouts; try rendering with the PCSX2 texture/VRAM viewer.

## 2026-10-24 — Phase 1 complete: disc mapped, English patch diffed

**Done**
- Wrote `tools/iso_extract.py`, `tools/bps_apply.py`, `tools/iso_diff.py` (see KNOWLEDGE.md 5.1).
- Listed the disc: 547 files, saved as `docs/disc_file_table.tsv`.
- Downloaded the English patch and applied it to a copy of the ISO. Output SHA-1 matches the English README, so our BPS applier is correct.
- Diffed original vs English: only 9 files differ (`OLM/O0`–`O7` and `SLPS_251.92`). Saved as `docs/diff_original_vs_english.tsv`.
- Looked inside those files (analysis scripts were throwaway, in the scratchpad; the results are in KNOWLEDGE.md 4.3–4.6).

**Findings that matter most**
1. Script = `OLM/O0`–`O7`: uncompressed Shift-JIS with readable control codes. Much easier than expected.
2. But those files also contain pointer tables with RAM addresses, so longer text means fixing pointers. This is now the main Phase 2 task.
3. The English patch relocated the grown script files to the end of the disc and changed no disc addresses in the executable, so the game opens files by name and we can enlarge files freely.
4. For longer menu text the English team added a new memory segment (`0x5C0000`) to the executable and redirected string pointers into it.
5. The font lives in the executable (about `0x1B7D40`, 288-byte glyph cells). Images, sound and video were untouched by the English patch.

**Decisions**
| Decision | Choice | Why |
|---|---|---|
| Compare discs by file, not raw bytes | `iso_diff.py` reads files straight from the images | No need to extract 3.5 GB; the result is easy to read |
| Own BPS applier instead of downloading Flips | `tools/bps_apply.py` | No extra downloads, and it verifies all checksums. Also the base for our own BPS creator later |
| Keep disc metadata tables in the repo | `docs/*.tsv` (paths, LBAs, sizes, no game data) | Useful reference; no copyright content |

**Next**
- Phase 2: map the script structure byte by byte, using the English files as the answer key for pointers.
- The user should install PCSX2 before Phase 4 (earlier is better; it also lets us test the memory-size question).


## 2026-10-24 — Project kickoff

**Done**
- Verified the ISO's SHA-1 matches the base disc of the English patch (`2f3864821f2a88f86bb5e004f383d63add82bde2`).
- Read the English patch repo: one BPS file, no tools or game data published.
- Found that `MultiPatch.app` is an empty macOS app bundle, so it's useless on Windows.
- Checked the environment: Python 3.14.6 and git 2.55 are present. 7-Zip and PCSX2 weren't found.
- Created the git repo, folder layout, `.gitignore`, `CLAUDE.md`, and the docs (plan, knowledge base, style guide, this log).

**Decisions**
| Decision | Choice | Why |
|---|---|---|
| Translation source | Japanese, with the English patch as reference | Best quality. Translating from the English text would copy its errors and liberties |
| Who translates | Claude drafts, user reviews | Fastest way to cover a full visual novel while keeping human quality control |
| Spanish variety | Neutral Latin American | Widest audience |
| Version control | Local git, no remote | History and rollback. Can publish later (patch only) |
| Docs location | Markdown files in `docs/` + `CLAUDE.md` | Claude reads them automatically each session, and the user can read them in any editor |
| Tool language | Python | Already installed, and good for binary parsing |
| Patch format | BPS (planned) | Same as the English patch. Works with Flips, MultiPatch, Rom Patcher JS |

**Next**
- Phase 1: write the ISO extractor, build the file table, apply the English patch to a copy and diff it to find the text and font files.
