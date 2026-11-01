# Translation style guide

Target: **neutral Latin American Spanish** that reads naturally across Mexico, Central America, South America and the Caribbean.

## 1. Workflow
1. Claude drafts from the **Japanese** text, using the English patch only to check meaning.
2. The user reviews the draft and fixes tone, naturalness and errors.
3. `tools/check.py` runs to catch technical problems (length, characters, control codes).
4. Status is updated in the table in `docs/PLAN.md`.

When Claude is unsure about a line (wordplay, cultural reference, ambiguous meaning), it leaves a `NOTE:` for the reviewer instead of guessing silently.

## 2. Language rules
- **ustedes** for second-person plural; never *vosotros*.
- **tú** between friends, family and peers. **usted** for strangers, elders and formal situations, following the Japanese politeness level (keigo → usted).
- Avoid strong regionalisms and words with different meanings across countries (e.g. *coger*, *concha*, *pico*, *chaqueta*, *pisto*). Prefer neutral options (*tomar*, *agarrar*).
- No voseo.
- Write ¿…? and ¡…! with opening marks, **if the font supports them** (that's a Phase 3 goal).
- Use accents correctly. If a glyph turns out to be impossible, we'll document a workaround here; we never just drop accents silently.

## 3. Formatting
- Dialogue quotes: decided: speaker name inline, `Name: "line"`; `「」` become `"`.
- Ellipsis: `...` (three dots; the font has no ellipsis character).
- Line length: 47 characters; narration pages max 10 lines; dialogue about 4 lines (unverified). The tool pre-wraps; see TRANSLATION_WORKFLOW.md.
- Keep control codes exactly as they appear in the source.

## 4. Open style decisions (settle in the Phase 4 pilot)
- [x] Honorifics (-san, -chan, -kun, -senpai): **keep** them (user decision 2026-10-25: they are part of the Japanese culture). Written with a hyphen, as in `Hitoe-san`, `Reu-chan`, `Watarase-kun`. Exceptions only where the Japanese plays with them. Applies to honorifics on names; common nouns (寮母さん, 店員さん) stay plain Spanish. Fixed O0:0154 to "Kyosuke-san".
- [x] おにいちゃん / お兄ちゃん: translate as **hermano** (user decision; "hermano mayor" where the age matters).
- [x] Names: given name first as in the English patch (Kyosuke, Hitoe Haruna), English romanization.
- [ ] Onomatopoeia and interjections (あ…, その…, えっと): translate or adapt
- [ ] Song lyrics and credits

## 5. Characters
_Filled in from the script. Name (JA) → Spanish spelling, who they are, how they speak, and how they address others._

| Japanese | Spanish | Role | Speech style / notes |
|---|---|---|---|
| 恭介 (渡良瀬恭介) | Kyosuke | Narrator, first person ("オレ"), a student living in the dorm | Casual, a bit sarcastic. Name kept as in the English patch |
| レゥ | Reu | A "Repliss", two days old, childlike | Speaks in a soft, drawn-out, innocent way ("Vaaale", "¿quééé?"); tú with Kyosuke |
| たえ | Tae | main character (1,834 lines) | _to describe when we read her scenes_ |
| ひとえ (榛名ひとえ) | Hitoe (Hitoe Haruna) | Kyosuke's childhood friend (1,809 lines) | tú with Kyosuke; teases him with mock formality ("señor Kyosuke"); calls herself ひとえ様 → "la gran Hitoe Haruna". Given name first, as in the English patch |
| みさお | Misao | main character (1,203 lines) | tú with Kyosuke (calls him "Kyosuke-san") and with Tae (user decision 2026-10-26: she is Tae's neighbour and cooking disciple); says "Da lo mejor de ti" |
| もとみ | Motomi | main character (956 lines) | _to describe_ |
| 恭平 | Kyohei | "Big brother Kyohei" (938 lines), not the narrator: **Kyosuke (恭介) ≠ Kyohei (恭平)** | _to describe_ |
| 亮 | Ryo | main character (888 lines) | _to describe_ |
| リース | Lease | a Repliss like Reu (360 lines), "Lease" in the English patch | Introduced in O2 as the second "β type" Reu brought by Kyohei; Kyosuke names her **Lease** at O2:4624. Speaker label: **"Beta"** (the font has no β) for the `β` lines; the early `レゥ` lines (O2:4086-4144) stay "Reu" with a NOTE; "Lease" from 4622. Speaks formal android Spanish with usted **to everyone, including the other Reu** (user, 2026-11-01); calls Kyosuke "Kyosuke-sama" (恭介様) and Kyohei "Amo" (マスター) (user decisions 2026-10-27) |
| きょうすけ | Kyosuke | the narrator again, written in hiragana (21 lines) | |
| ？？ | ??? | unknown speaker (161 lines) | keep as `???` |

Other speakers (all in `tools/speakers.py`'s output): 母/母親 Madre, 専門家 Experto, 店員 Empleado(a) (A/B/C…), キャスター Presentador(a), 生徒Ａ/Ｂ/Ｃ Estudiante A/B/C, 男子生徒 Estudiante, 友人/友達 Amigo(a), 先生/教師 Profesor(a), 寮生 Residente, 家政婦 Ama de llaves, 運ちゃん Taxista. The speaker's name is written inline (`Name: "line"`), so these labels need Spanish forms too.

## 6. Terms glossary
_Places, recurring terms, menu vocabulary. Keep it consistent across the whole game._

| Japanese | Spanish | Notes |
|---|---|---|
| セーブ | Guardar | menu |
| ロード | Cargar | menu |
| 阿見寮 / 寮 / 寄宿舎 | Residencia Ami / la residencia | 寮 = "residencia", not "dormitorio" (in Latin America that means bedroom) |
| 寮母さん | la encargada | the dorm's matron; joke in the opening ("ESE momento" for 『アノ』時) |
| 県立津久見高校 | Preparatoria Prefectural de Tsukumi | "preparatoria" is understood across Latin America |
| 個室 / 部屋 | cuarto | a room; "habitación" is fine too, keep "cuarto" for consistency |
| 布団 | futon | kept as "futon" (no accent, as in English) |
| ＧＷ | Golden Week | kept; the reader recognizes it |
| モノクロ | Monocromo | the trendy clothing shop on the shopping street (English patch: "Monochro") |
| 店員 / 店員さん | empleado(a) | shop staff; speaker labels `Empleado A/B/C` ("dependiente" sounds Spanish) |
| いらっ(しゃ)いませ said sloppily | ¡Bienvenío! / ¡Bienveníooo! | the clerks' slurred greeting; stretch when the Japanese has ～ |
| 幼なじみ | amigo / amiga de la infancia | |
| 並ぶ (in a queue) | hacer fila | neutral ("estar formado" is Mexican) |
| しょうがない / 仕方ない | qué se le va a hacer / ni modo ✗ | "ni modo" is regional; "qué remedio" also fine |
| times of day 午前１０時０３分 | `10:03 AM` | short form, fits better; `PM` for the afternoon |
| 〜様 used jokingly about oneself | "la gran …" | e.g. "la gran Hitoe Haruna" |
| 恭介「…」 | `Kyosuke: "..."` | speaker names are written inline in the text, as in the English patch; `「」` become `"` |
| ── (long dash) | `--` | the font has no long dash |
| … | `...` | the font has no ellipsis character |
| | | |
| 寮母 (Tae, substituting) | la encargada suplente (first time), then just "Tae" | her mother, the real matron, stays "la encargada" (user decision 2026-10-25) |
| かわいい (the lesson, O0 2849-2881) | lindo/a | keep "lindo/a" and leave a NOTE on the boys-vs-girls point |
| + and × (O1 math question) | + and × as they are | added to the font 2026-10-25 (user decision); Í and Ü can no longer be typed (write I, U) |
| ②, ③, ☆ in text | 2, 3, ! | written as plain digits and `!`; the user will check in the game whether circled digits exist |
| Chinese lines (O0 1746-1761) | pinyin without tones | as in the English patch |
| Repliss / Tyrell Bio Corporation | unchanged | probably story-related |
| ハリセンぼーん pinky-swear garble | "abanicos de papel" mistake translated | with a NOTE |
| 全寮制 (の高校) | preparatoria de internado / internado | 100% boarding: every student must live in the dorm; avoid "con internado" (sounds optional). User decision 2026-10-25 |
| 帰省 | volver a casa de la familia / ir de visita a casa | going back to the family home while living away; make it explicit when context isn't clear (帰宅 = going home after class, plain "volver a casa") |
| 幼稚園 | kínder | casual; "preescolar" is the alternative (User decision 2026-10-25) |
| 紫の上 (O0:1171, Genji Monogatari joke) | mi pequeña protegida | user decision 2026-10-25 |
| Reu's sobs しゃっく / ひっく | "Snif" when she is tearing up or sniffling (reads at once as crying); "Hip" (or "Snif... hip...") when the text describes catching her breath or hiccuping from crying | user decision |
| Reu's first sound ふぇ | "Fueh" (not "Fweh": "fue" is read as in fuego); sobs keep the final n: "Fueeen", "Buaaan", "Uaaan" | user decision |
| 悪友 | cómplice | friend who leads you into mischief; user decision 2026-10-25 (replaces "compinche"); worst-case line O0_022:510: e.g. "un pésimo cómplice" |
| Terms approved 2026-10-25 | tanque de vidrio, almacén, baño, doppelganger, Accesorio --, barra, conexión a tierra, enchufe, primera activación, Heeey, canasta, tienda de conveniencia, bento, por ahora/por lo pronto, pan de molde, canal público, dinero para mis gastos | accepted as listed in the LOG |
| いただきます (before eating) | Buen provecho | ごちそうさま (after eating) = "Gracias por la comida"; user decision 2026-10-25 |
| 高蛋白剤 | suplemento proteico | |
| 冷蔵庫 / 押入 | refrigerador / clóset | |
| そっちのおなか / こっちのお腹 | esa pancita / esta pancita | Reu's childlike words for her two kinds of hunger |
| numbers | 10 and up as digits, % for percentages, 0-9 as words | user decision 2026-10-26 ("30% restante", "hace 88 años", "5 minutos" when the JA has digits; spoken clock times as words) |
| セコンド | segundo/a | boxing second, offered by Hitoe and Motomi; user decision 2026-10-26 (keep despite the ambiguity with "un segundo" = a moment) |
| 三本勝負 / 行動範囲 / 呼び捨て | batalla de tres rondas / radio de acción / sin ningún honorífico | |
| Reu's mishearing of "policy" | Reu asks "¿Qué es una 'política'?" | no "polítika" (k reads as foreign) |
| 徹底抗戦 | resistir hasta el final | |
| 会議 (Tae's meeting) | reunión | not "junta" |
| 気持ちを切り替える | cambiar de actitud | not "cambiar el chip" (Spain) |
| がんばってね | ¡ánimo! | Hitoe's がんばりなさいよ = "¡esfuérzate!" |
| がんばってください (Misao) | Da lo mejor de ti | Misao's fixed phrase |
| スタート！ (race start) | ¡Ya! | |
| 泡 (Repliss healing) | espuma blanca | |
| 擬似的な対決 / ネイティブアメリカン | duelo simulado / nativos americanos | fake history No. 2 |
| 上着 (Kyosuke's leather coat) | abrigo | |
| リーチ (Indian poker) | me falta un punto / X está a un punto | |
| 百戦錬磨のギャンブラー | jugadora curtida en cien batallas | Kyosuke's mock title for Tae |
| 適当にやんなさい (Tae) | arréglatelas como puedas | |
| カギの束 | manojo de llaves | not "llavero" (Reu's keyring trinket in O0) |
| 敬語を使う | hablarle con formalidad | |
| ポーカーフェイス | cara de póker | |
| 手が悪かった | te tocaron malas cartas | |
| 戦術 | táctica | |
| ＴＰＯをわきまえない | no sabe distinguir el momento ni el lugar | |
| よいしょっ (lifting) | ¡Upa! | user decision 2026-10-26 |
| すきだよ (Reu to friends) | te quiero ("te quiero porque eres buena") | user decision 2026-10-26; not "me gustas" (romantic) |
| うふふ / えへへ (Reu) | Jijiji~ (longer laugh, more "ji") | O0_002 "Ehehe" aligned 2026-10-26 |
| 主役 (Reu) | la protagonista | |
| 義務 | deber | Reu: "¿qué es 'deber'?" |
| ぶっきらぼー | gruñón (Reu: "gruñóoon") | |
| 野次馬 / 観客 | curiosos / espectadores | |
| 大名行列 | el séquito de un señor feudal | |
| 仁王立ち | plantado/a como un guardián de templo | |
| だめったらだめ | No es no | |
| 自意識過剰 | creerse el centro de atención | |
| 複雑な顔 | cara de sentimientos encontrados | |
| オツム | el coco | |
| トトカルチョ | (estaban) apostando | not "quiniela" (regional) |
| ＩＱテスト | prueba de IQ | |
| 位置について / ヨーイ | En sus marcas... / Listos... | race start; quiz start: "¿Listos? ...Preparados... ¡Comiencen!" |
| ゴール！ | ¡Meta! | |
| 失笑 | no poder contener la risa | |
| やっちまった | metí la pata | not "la regué" (Mexican) |
| 泣いても笑っても | para bien o para mal | |
| 延長戦 | tiempo extra (a muerte súbita) | not "prórroga" (Spain) |
| 当事者の二人 | los dos implicados | |
| ココア | chocolate (caliente) | not "cocoa" |
| おのろけカップル | pareja de tortolitos | |
| 自業自得 | se lo buscó ella/él solo/a | keep identical when repeated |
| 悪あがき | patadas de ahogado | |
| 百歩譲って | hacer la enorme concesión de | |
| 〜様 (e.g. 萩本亮様) | el gran Ryo Hagimoto | |
| 大風呂敷を広げる | armar todo este escándalo | |
| ノートパソコン | laptop | |
| ご苦労様です (Kyosuke to an elder) | polite ("Se está esforzando mucho" / "Buen trabajo") | ironic only if the Japanese makes it explicit |
| 夜食 | algo de comer (a deshoras) | not "bocadillo" |
| 気分転換 | despejarse | |
| 男の料理 | cocina de hombre | |
| ボール (bowl) | bol | |
| 生クリーム / ベーコン / しょうゆ | crema / tocino / salsa de soya | |
| そういうことにしておきましょう (Kyosuke's muletilla) | dejémoslo así | keep identical |
| 恒例行事 | una tradición (de la Residencia Ami) | |
| N点 (grading) | un N de 100 | |
| 縁日めぐり (Hitoe's plan) | Tour por la feria | |
| 赤提灯 | faroles rojos | |
| メガネ | lentes | not gafas/anteojos (regional) |
| 下見 | ir a explorar | |
| ナンパ野郎 | mujeriego | |
| まいはに | mi cielo | |
| Hitoe's laughs ふふふ/むふふ/ぐふふ | Fufufu / Mufufu / Gufufu | ぷいっ "¡Hmph!", ぶう "Mmph", な～んてね "Naaah, es broma" |
| じぃ～ (stare) | *mirada fija* | |
| 鈍感 | despistado | |
| ひとえちゃん (Hitoe about herself) | Hitoe(-Haruna)-chan | "la gran Hitoe Haruna" only for ひとえ様 |
| にゃんこ (Reu) | gatito | |
| くんくん | *olfatea olfatea* | not "snif" (Reu crying) |
| ふぎゃー (cat) | ¡Fiaaau! | |
| ジ・エンド | fin de la historia | |
| 心配性 | aprensiva / se preocupa por todo | |
| 天然 (airhead) | distraída por naturaleza | |
| 一本気 / 義理に厚い | recto y leal | |
| オヤジ (stall man) | label "Vendedor" | |
| クジ / はずれ | sorteo, papelito / el papelito sin pareja | |
| えいやっ | ¡Allá voy! | |
| 浮気の虫 | el bicho de la infidelidad | |
| おつむがゆるゆる | el coco blando | |
| 夫婦喧嘩 | pelea de casados | not "pleito" (lawsuit in the Southern Cone) |
| 保護者 | tutor | |
| せーの | a la de tres / ¡Uno, dos, tres! | |
| Ryo's ふっふっふ | Ju, ju, ju | |
| ほえ？ (Reu) | ¿Eeeh? | |
| お代官様 | mi señor | period-drama plea |
| 表に出ろ | vamos a arreglar esto afuera | |
| 男 (Yasu's first lines) | label "Hombre" | then "Yasu" |
| ソノ筋の人 | gente del bajo mundo | |
| おんなじ (Reu) | iguales | returns at O1:5972 |
| 観察眼 | ojo observador | |
| ゴリラのお面 / お面屋 | máscara de gorila / puesto de máscaras | |
| わた菓子 | algodón de azúcar | |
| ダイビング・ハグ | abrazo en picada | |
| にらめっこ | duelo de miradas | |
| 甘いものは別腹 | Para lo dulce siempre hay un huequito aparte | as O0:3524 |
| 狐の嫁入り / お稲荷さんのお嫁入り | la boda de los zorros (de Inari) | not "del zorro" (El Zorro) |
| 狐に化かされる | embrujar (un zorro) | |
| 大名行列 (a literal procession) | cortejo | "séquito de un señor feudal" for a crowd following someone |
| りんご飴 | manzana acaramelada | |
| バーゲン / 荷物持ち | rebajas / cargar las bolsas | |
| 町内会 | junta de vecinos | |
| お囃子 | música de flautas y tambores | |
| 浴衣 | la yukata (feminine) | user decision 2026-10-26 |
| あんず飴 | albaricoques caramelizados | not chabacano/damasco (regional) |
| イカ焼き / じゃがバター / フランクフルト | calamar asado / papas con mantequilla / salchicha | |
| えっち (teasing) | Pervertido... | |
| お下がり | me la pasó (Tae-san) | |
| いらっしゃい (stall) | ¡Adelante, bienvenidos! | |
| 射的 / コルク弾 | tiro al blanco / balas de corcho | |
| お好み焼き | okonomiyaki | kept, like takoyaki |
| 屋台 / 出店 | puesto | |
| 店員 (stall) | label Empleado ("Vendedor" only for オヤジ/おっちゃん) | |
| 食う (Tae's joke) | atiborrarse | |
| 大判焼き | imagawayaki | kept (alt. "pastelito relleno") |
| みどりの (Reu's supplement) | lo verde | |
| 飛び道具 | armas de proyectil | |
| 前衛的 | de vanguardia | |
| 脂汗 | sudor frío | |
| 見守る | velar por (ellos) | |
| ゲームセンター | arcade | |
| 親友 (Hitoe) | mejor amiga | as "mejor amigo" for Ryo |
| 隙だらけ | descuidado / con la guardia baja | |
| 出動 | a la acción | |
| チョコモカバニラアイス | helado de chocolate moca con vainilla | |
| からかう | burlarse (de) | not "molestar" |
| "levels" of love (Hitoe) | nivel uno ... nivel 10 | numbers rule |
| つっこみ | réplica | |
| プリントシール | cabina de fotos (machine) / calcomanías (stickers) | |
| げんきん | interesada | |
| ナマイキ (child) | se puso insolente | |
| 夕寝 | siesta de atardecer | |
| 喧嘩両成敗 | Pelea de dos, castigo para los dos | |
| 美白機能 | función de piel luminosa | |
| 荷物持とうか | ¿te ayudo con las bolsas? | |
| アニキ (Kyohei) | mi hermano (narration) / ¡Hermano! (vocative) / hermano Kyohei (Hitoe's 恭平兄さん) | user decision 2026-10-27; context must tell Reu's "hermano" (Kyosuke) from it |
| えらーだえらーだ | Error, error. | developer placeholder, O2 (0404, 2583, 4657, 4710) |
| Ｐｍｆｈ－０００００とんで１/２ | Pmfh-00001 / Pmfh-00002 | android serials, with a NOTE |
| Misao's cold scene (O2 3360-3410) | tú, cold and sarcastic | not usted |
| Kazu-chan (Hitoe, O2 1342-1352) | keep "Kazu-chan" + NOTE (possible actor reference) | |
| 江口 / 江成 / 望月 (O2 1325-1360) | Eguchi / Enari / Mochizuki | Kyosuke's improvised surnames starting with E; plain romanization keeps the joke |
| ♪ in the birthday song (O2 4702-4707) | ~ (unless PCSX2 shows ♪ renders) | childlike lyrics |
| ストロー | pajita | RAE standard; not popote (Mexican), pitillo, sorbete |
| 応援団 | club de animación | |
| おばちゃん / 相撲部 / 群集 (labels) | Señora / Club de sumo / Multitud | |
| ごふっ / ごっくごっく | Gof. / Glup, glup… | |
| Hitoe's へへへ/えへへ | Jejeje / Jeje | |
| 5円 / 1円 | 5 yenes / 1 yen | |
| 修羅場 | campo de batalla | echoes 戦火/戦場 |
| mouth full (speech) | garble with "ahua" | |
| あう (Misao/Kyosuke whimper) | Uuu. | not "Au." (pain/dog) |
| 心変わり / 心移り | cambiar de sentimientos / fijarse en | |
| 魔力 / まほう (Reu repeats) | poder mágico / magia | |
| はい！ (magician's reveal) | ¡Tachán! | |
| エスパー仮面 | Enmascarado Telépata | |
| 墨汁 | tinta china | |
| フタマタ | andar con dos a la vez | |
| 正座 | sentada sobre los talones | |
| 尻に敷かれる | dejarse mandar | |
| グッモーニン、ミス | Buenos días, miss Tae-san | |
| すき (Reu defines it) | Querer a alguien es "querer estar juntos" | like/love ambiguity kept |
| 二日酔い | resaca | Tae's "entrañable vecina" gag (愛すべき隣人) |
| お粥 | gachas de arroz | |
| オートミール | oatmeal | kept: Reu asks what it is |
| むかい酒 | el pelo del perro (que te mordió) | |
| 満点 | Puntaje perfecto | |
| もしもし | ¿Hola? | not ¿Aló?/¿Bueno? (regional) |
| 目やに | lagañas | |
| 型 (karate) | kata | |
| 図書委員会 / 中学 / 洗面所 | comité de biblioteca / secundaria / baño | |
| おっけー | Ok | avoid "Va" (regional) |
| 勘 | instinto | |
| 本場の味 | el sabor auténtico | |
| パルミジャーノ | Parmigiano | |
| クレーンゲーム / ぬいぐるみ / 人形 | máquina de grúa / peluche / muñeco | |
| 財布 / 携帯電話 | billetera / celular | |
| 非通知 | número oculto | |
| ミシミシ | Cric, cric | |
| もこもこ | mullido | alternatives esponjoso / suavecito |
| Tae's drunk slur (せいじゃ) | "talonesh" only at O2:1787/1792 | the Japanese slurs only there; the earlier "sh" lines were removed |
| 遠慮しないの (an offer) | no te hagas del rogar | |
| 従兄妹 (Reu's cousin lie) | primo (the TV Chinese-lesson gag) / **prima** for Reu herself | clarified 2026-11-01 (O2:4026) |
| long silences (Misao/Tae, O2 1947-1958) | ~40 dots | 8 became 18, 16 became 36 earlier |
| 差し出がましい | Perdona que me meta | |
| 浮かない顔 | cara de funeral | |
| 後悔 quotes (O2 2145) | 'no debí hacer eso entonces' / 'debí hacer esto otro' | keep identical if it returns at O2:2590 |
| 布団 | futon | not "cobijas" |
| わたし (Reu) | yo (first person) | as in O0; Reu's third-person "Reu" only where the Japanese has レゥ |
| ぐう (stomach) | Grrr. | |
| カバン | mochila | not bolsa/bolso |
| 熱血小僧 | chico de sangre caliente | |
| 『』 around a single term | '...' (single quotes) | a full 『』 sentence stays in "..." |
| ellipses … / …… | "..." (3 dots); a run of 3+ gets 3 dots per character | in force since O0; checked in O2 2701-3000 |
| パシリ | mandadero/a | user approval 2026-10-25 |
| ヤレヤレ (narration) | Ay, ay, ay. | user approval 2026-10-25 |
| 女子棟 / 男子棟 | el edificio de las chicas / de los chicos | as in O0 |
| アニキ (yakuza boss, O1 festival) | Jefe (label); "el jefe" in narration | user decision 2026-10-25; not Kyosuke's brother (also アニキ). His sidekick Yasu: rough neutral Spanish, no regional slang |
| 縁日 | la feria (first time: "la feria del templo") | user decision 2026-10-25 |
| 金魚すくい | pesca de pececitos | user decision 2026-10-25 |
| ペア・おみくじ | Oráculo de parejas | user decision 2026-10-25 |
| プリクラ | cabina de fotos | user decision 2026-10-25 |
| 降りる / 勝負する (Indian poker) | Retirarme / Jugármela (menu); "me retiro" | |
| card names (drawn by the game) | "10 de corazones", "jota/reina/rey/as de picas"; suits tréboles, corazones, picas, diamantes | the line before is lowercase-safe: "la carta de Reu es" |
| 奥歯にものが挟まった | hablar con rodeos | never the literal "algo atorado entre los dientes" (2026-11-01) |
| 気味が悪い | me da escalofríos | not "mala espina" |
| まったく… (a sigh) | Increíble... | not "No puede ser" |
| 気合いが入っている (Tae dressed up) | muy animada | as in O2_009 |
| 時間がつぶせる | matar el tiempo | |
| 言ったもん勝ち | gana el que se queda con la última palabra | |
| わかんない (Reu, asked for an answer) | No sé... | |
| 大事な家族 | un miembro importante de mi familia | |
| ご苦労様 / お疲れさま (sarcastic) | Cuánto lo siento / Mis condolencias | non-ironic ご苦労様 = "Buen trabajo" |
| 十倍にして返す | devolver multiplicado por diez | |
| 純情少年 | chico inocente | |
| どうしようもない (of a face) | caso perdido | |
| 『何かいいことない？』 (Kyohei's mail) | ¿No pasa nada bueno? | O0 has 面白いこと = "¿No pasa nada interesante?"; different wording is fine (user, 2026-11-01) |
| 気にするな / 気になってる | No le des importancia / a mí me importa | the 矛盾 joke in the next line depends on it |
| オヤジ | mi viejo / el viejo | never "papá" |
| おにいちゃんのおにいちゃん (O2:4118) | el hermano del hermano | NOT "el hermano de mi hermano" (that would be Kyosuke) |
| 趣味 (of clothes) | gusto | |
| 『火の無い所に煙は立たず』 | no hay humo sin fuego | |
| 杵築たえさん (first full name) | Tae Kizuki... keep -san: "Kizuki-san" / Tae tells Kyohei "puede llamarme simplemente Tae" | Tae uses usted with Kyohei |
| 持病 | enfermedad crónica | |
| 了解 / わかった (giving in) | Entendido / Está bien | |
| 頼むよ / 頼むな (Kyohei asking Reu; 命令 = "órdenes") | Te lo pido | |
| 気取る | darse aires | |
| 秘蔵のお酒 | mi reserva personal | |
| はい、あ～ん (feeding) | Aquí tiene, diga 'aaah' | |
| 酒 / お酒 (Tae's gift from Kyohei) | whisky | also in dialogue, never "licor" (user, 2026-11-01) |
| 試作型レプリス / 甲種人型生命体 | Repliss prototipo / forma de vida humanoide de Clase A | |
| コードネーム | nombre en clave | |
| 新品交換 | cambio por una unidad nueva | |
| モニターテスト | prueba de monitoreo | |
| 回収 | recuperar | pending the user's call (O2:4557, 4565) |
| βタイプ | tipo Beta | speaker label stays "Beta" |
| 賃貸契約 | contrato de arrendamiento | not "alquiler" |
| 返却口 | ventanilla de devolución | |
| 一方的に | de forma unilateral | |
| おたんじょうかい | fiesta de cumpleaños | "cumple" only in the song |
| ―― (long dash) | `--` with nothing added beside it | no "..." or extra comma |
