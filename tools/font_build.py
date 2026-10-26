"""Our own game font: renders the half-width glyphs from DejaVu Sans Mono (free licence)
into the engine's 24x24 4-bit cells. (docs/KNOWLEDGE.md 4.6, 4.11)

    python -I -X utf8 tools/font_build.py preview      ->  work/font_preview.png (zoomed sheet)

The font file is NOT part of the repository or of the patch: only the rendered bitmaps
end up in the patch. Put DejaVuSansMono.ttf where FONT_PATH points (see docs/fonts/README.md);
the licence text is kept in docs/fonts/DEJAVU_LICENSE.txt.

Cell layout (same as the English patch): 0-9 digits, 10-35 A-Z, 36-61 a-z, 62+ the symbols of
charmap.HAFF_LIST (15 base symbols, the Spanish stand-ins, then extra symbols such as % and +).
Geometry: baseline on row 19 (like the English font), glyphs start at x = X0, advance 12-13 px.
"""
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import charmap  # noqa: E402
import exe_patch as xp  # noqa: E402
import font_tool as ft  # noqa: E402
import project  # noqa: E402

FONT_PATH = os.environ.get('MMM_FONT') or os.path.join(
    project.ROOT, 'work', 'fontsrc', 'dejavu-fonts-ttf-2.37', 'ttf', 'DejaVuSansMono.ttf')
SIZE = 20            # em size in pixels: DejaVu Sans Mono is 0.602 em wide -> 12 px advance
BASELINE = 19        # row of the baseline (the English font also sits on row 19)
X0 = 1               # first column of the glyphs
LEVELS = 5           # pixel values are 0..5


def _font():
    from PIL import ImageFont
    return ImageFont.truetype(FONT_PATH, SIZE)


def render(ch, font=None):
    """24x24 grid (rows of 0..5) for one character."""
    from PIL import Image, ImageDraw
    font = font or _font()
    img = Image.new('L', (ft.W, ft.H), 0)
    ImageDraw.Draw(img).text((X0, BASELINE), ch, font=font, fill=255, anchor='ls')
    px = img.load()
    return [[round(px[x, y] * LEVELS / 255) for x in range(ft.W)] for y in range(ft.H)]


def cell_chars():
    """{cell: character} for every half-width cell we draw."""
    cells = {}
    for i, c in enumerate('0123456789'):
        cells[i] = c
    for i in range(26):
        cells[10 + i] = chr(65 + i)
        cells[36 + i] = chr(97 + i)
    back = {stand: letter for letter, stand in charmap.SPANISH.items()}
    for i, b in enumerate(charmap.HAFF_LIST.decode('ascii')):
        # the list holds stand-ins: the cell draws the Spanish letter they stand for
        cells[xp.HAFF_FIRST_CELL + i] = back.get(b, b)
    return dict(sorted(cells.items()))


def install_font(exe):
    """Write all our glyphs into the executable image (bytearray)."""
    font = _font()
    for cell, ch in cell_chars().items():
        ft.put(exe, cell, render(ch, font))


def preview_png(path):
    from PIL import Image
    font = _font()
    cells = cell_chars()
    zoom, cols = 6, 16
    rows = (len(cells) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (ft.W * zoom // 2 + 6), rows * (ft.H * zoom + 6)), (30, 30, 40))
    for n, (cell, ch) in enumerate(cells.items()):
        g = render(ch, font)
        ox = (n % cols) * (ft.W * zoom // 2 + 6)
        oy = (n // cols) * (ft.H * zoom + 6)
        for y in range(ft.H):
            for x in range(ft.W // 2):
                v = g[y][x]
                c = 40 + v * 43
                for dy in range(zoom):
                    for dx in range(zoom):
                        sheet.putpixel((ox + x * zoom + dx, oy + y * zoom + dy), (c, c, c))
    sheet.save(path)
    print(path, f'{len(cells)} glyphs')


if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == 'preview':
        preview_png(os.path.join(project.ROOT, 'work', 'font_preview.png'))
    else:
        print(__doc__)
