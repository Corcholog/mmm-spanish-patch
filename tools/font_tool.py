"""Font glyphs: reading/writing the 24x24 4-bit cells and building the Spanish accents.
(docs/KNOWLEDGE.md 4.6)

PILOT FONT: for local pilot builds only, the digits, letters and punctuation come from the
English patch's glyphs (work/english, never published) and the accented letters are made
from them by adding marks. The release needs our own glyphs: see docs/PLAN.md.
"""
import charmap
import exe_patch as xp

W = H = 24
SHADES = ' .:+*#'     # levels 0-5 for the previews


def get(exe, cell):
    o = xp.cell_off(cell)
    rows = []
    for y in range(H):
        r = []
        for b in exe[o + y * 12:o + y * 12 + 12]:
            r += [b & 15, b >> 4]
        rows.append(r)
    return rows


def put(exe, cell, g):
    o = xp.cell_off(cell)
    for y in range(H):
        for x in range(0, W, 2):
            exe[o + y * 12 + x // 2] = (g[y][x] & 15) | ((g[y][x + 1] & 15) << 4)


def bbox(g):
    pts = [(x, y) for y in range(H) for x in range(W) if g[y][x]]
    xs, ys = [p[0] for p in pts], [p[1] for p in pts]
    return min(xs), min(ys), max(xs), max(ys)


ACUTE = [[0, 0, 3, 5], [0, 3, 5, 3], [3, 5, 3, 0]]
TILDE = [[0, 5, 5, 0, 0, 5], [5, 0, 0, 5, 5, 0]]
DIAER = [[5, 5, 0, 0, 5, 5], [5, 5, 0, 0, 5, 5]]


def with_mark(base, mark, top_limit):
    g = [row[:] for row in base]
    x0, y0, x1, _ = bbox(g)
    mh, mw = len(mark), len(mark[0])
    cx = (x0 + x1) // 2 - mw // 2 + (1 if mark is ACUTE else 0)
    bottom = min(y0, top_limit) - 2
    for dy in range(mh):
        for dx in range(mw):
            y = bottom - (mh - 1) + dy
            if 0 <= y < H and mark[dy][dx]:
                g[y][cx + dx] = max(g[y][cx + dx], mark[dy][dx])
    return g


def dotless(g, xheight_top):
    out = [row[:] for row in g]
    for y in range(0, xheight_top):
        out[y] = [0] * W
    return out


def rotated(g, top_target):
    r = [[g[H - 1 - y][W - 1 - x] for x in range(W)] for y in range(H)]
    ox0, _, ox1, _ = bbox(g)
    rx0, ry0, rx1, _ = bbox(r)
    sx = (ox0 + ox1) // 2 - (rx0 + rx1) // 2
    sy = top_target - ry0
    out = [[0] * W for _ in range(H)]
    for y in range(H):
        for x in range(W):
            ny, nx = y + sy, x + sx
            if r[y][x] and 0 <= ny < H and 0 <= nx < W:
                out[ny][nx] = r[y][x]
    return out


def spanish_glyphs(exe):
    """The 16 Spanish characters, made from the letters already in `exe` (cells 0-62)."""
    letter = {c: get(exe, 36 + ord(c) - 97) for c in 'abcdefghijklmnopqrstuvwxyz'}
    letter.update({c: get(exe, 10 + ord(c) - 65) for c in 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'})
    xh = bbox(letter['x'])[1]
    cap = bbox(letter['H'])[1]
    q, ex = get(exe, 62), get(exe, 63)
    return {
        'á': with_mark(letter['a'], ACUTE, xh), 'é': with_mark(letter['e'], ACUTE, xh),
        'í': with_mark(dotless(letter['i'], xh), ACUTE, xh), 'ó': with_mark(letter['o'], ACUTE, xh),
        'ú': with_mark(letter['u'], ACUTE, xh), 'ñ': with_mark(letter['n'], TILDE, xh),
        'ü': with_mark(letter['u'], DIAER, xh),
        'Á': with_mark(letter['A'], ACUTE, cap), 'É': with_mark(letter['E'], ACUTE, cap),
        'Í': with_mark(letter['I'], ACUTE, cap), 'Ó': with_mark(letter['O'], ACUTE, cap),
        'Ú': with_mark(letter['U'], ACUTE, cap), 'Ñ': with_mark(letter['N'], TILDE, cap),
        'Ü': with_mark(letter['U'], DIAER, cap),
        '¿': rotated(q, xh), '¡': rotated(ex, xh),
    }


def install_pilot_font(exe, english_exe):
    """Pilot only: English glyphs in cells 0-76, then the Spanish letters in cells 77+."""
    lo, hi = xp.cell_off(0), xp.cell_off(77)
    exe[lo:hi] = english_exe[lo:hi]
    for ch, g in spanish_glyphs(exe).items():
        cell = charmap.cell_of(ch)
        assert 77 <= cell <= 94 and not any(exe[xp.cell_off(cell):xp.cell_off(cell) + xp.CELL]), cell
        put(exe, cell, g)


def preview(glyphs):
    names = list(glyphs)
    for i in range(0, len(names), 8):
        group = names[i:i + 8]
        print('  ' + '  '.join(f'{n:^16}' for n in group))
        for y in range(H):
            line = '  '.join(''.join(SHADES[v] for v in glyphs[n][y][4:20]) for n in group)
            if line.strip():
                print('  ' + line)
