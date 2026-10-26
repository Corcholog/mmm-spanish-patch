"""Spanish text -> the bytes the game understands. (docs/KNOWLEDGE.md 4.6)

The engine only draws half-width characters that are digits, letters, or listed in the
half-width symbol list (haff_opt). Accented letters don't exist in ASCII, so each one is
stored as an ASCII symbol that Spanish text doesn't need; the font cell for that symbol
holds the accented glyph. Translators write normal Spanish; encode() does the swap.
"""

# symbols the English patch already uses (cells 62-76), kept as they are
BASE_SYMBOLS = "?!'\"() .,-:;/*~"

# Spanish letter (or symbol) -> stand-in ASCII byte (cells 77-91, in this order). Every
# printable ASCII byte is taken, so Í and Ü (never used so far) gave up their bytes on
# 2026-10-25: '+' now draws a real plus, '^' draws ×. Write I / U for them if ever needed.
SPANISH = {
    'á': '#', 'é': '&', 'í': '|', 'ó': '<', 'ú': '=', 'ñ': '>', 'ü': '@',
    'Á': '[', 'É': ']', 'Ó': '_', 'Ú': '`', 'Ñ': '{',
    '¿': '}', '¡': '$', '×': '^',
}

# extra symbols drawn by our own font (cells 92+), usable in text as they are
EXTRA_SYMBOLS = "%+"

HAFF_LIST = (BASE_SYMBOLS + ''.join(SPANISH.values()) + EXTRA_SYMBOLS).encode('ascii')
STAND_INS = set(SPANISH.values())

# typographic characters translators may type -> what the font has
NORMALIZE = {
    '＋': '+', '－': '-', '✕': '×',
    '…': '...', '“': '"', '”': '"', '«': '"', '»': '"', '‘': "'", '’': "'",
    '—': '--', '–': '-', '　': ' ', ' ': ' ',
}


def normalize(text):
    for a, b in NORMALIZE.items():
        text = text.replace(a, b)
    return text


def encode(text):
    """Encode Spanish text (control codes like \\k\\p pass through unchanged)."""
    out = []
    for ch in text:
        if ch in SPANISH:
            out.append(SPANISH[ch])
        elif ch in STAND_INS:
            raise ValueError(f'{ch!r} is used as a stand-in for an accented letter and cannot appear in text')
        elif ch.isalnum() and ord(ch) < 0x80 or ch in BASE_SYMBOLS or ch in EXTRA_SYMBOLS or ch == '\\' or ord(ch) < 0x20:
            out.append(ch)
        elif ord(ch) < 0x80:
            raise ValueError(f'{ch!r} has no glyph in the font (only letters, digits and "{BASE_SYMBOLS}" draw)')
        else:
            raise ValueError(f'character {ch!r} is not supported by the font')
    return ''.join(out).encode('ascii')


def cell_of(ch):
    """Font cell that draws `ch` (a Spanish letter or a base symbol)."""
    key = SPANISH.get(ch, ch).encode('ascii')
    return 62 + HAFF_LIST.index(key)
