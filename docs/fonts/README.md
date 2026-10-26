# Fonts used to draw the game text

The patch draws its own half-width glyphs (digits, letters, punctuation, Spanish accents, `%`).
They are rendered by `tools/font_build.py` from **DejaVu Sans Mono 2.37**
(<https://github.com/dejavu-fonts/dejavu-fonts/releases/tag/version_2_37>), whose licence
(Bitstream Vera + public-domain changes) allows this use; the licence text is in
`DEJAVU_LICENSE.txt` and the README of the release must credit it.

The font file is **not** committed. To rebuild the glyphs, download `dejavu-fonts-ttf-2.37.zip`,
extract `ttf/DejaVuSansMono.ttf` to `work/fontsrc/dejavu-fonts-ttf-2.37/ttf/` (or set the
environment variable `MMM_FONT` to its path), and `pip install Pillow`.
