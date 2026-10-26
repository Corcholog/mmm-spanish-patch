"""Project paths and access to the original disc. Shared by the build tools."""
import hashlib
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
SRC_ISO = os.path.join(ROOT, 'My Merry May (Japan) (Shokai Genteiban).iso')
SRC_SHA1 = '2f3864821f2a88f86bb5e004f383d63add82bde2'
TRANSLATION = os.path.join(ROOT, 'translation')
ENGLISH = os.path.join(ROOT, 'work', 'english')   # English-patched files, local reference only
BUILD = os.path.join(ROOT, 'build')
SCRIPTS = [f'O{i}' for i in range(8)]
OVERLAY_BASE = 0x4D3600
OVERLAY_LIMIT = 0x5C0000          # overlays must end below segment 9

sys.path.insert(0, HERE)
from iso_extract import SECTOR, list_files  # noqa: E402

_files = None


def read_iso_file(path, iso=SRC_ISO):
    """Bytes of a file on the original disc, e.g. 'OLM/O0' or 'SLPS_251.92'."""
    global _files
    if _files is None or iso != SRC_ISO:
        _, _, files = list_files(iso)
        if iso != SRC_ISO:
            return _read(iso, files, path)
        _files = files
    return _read(iso, _files, path)


def _read(iso, files, path):
    for p, lba, size in files:
        if p.rstrip('.') == path:
            with open(iso, 'rb') as f:
                f.seek(lba * SECTOR)
                return f.read(size)
    raise SystemExit(f'{path} not found on the disc')


def english_script(name):
    """English-patched OLM file, or None if work/english isn't there."""
    p = os.path.join(ENGLISH, 'OLM', name)
    return open(p, 'rb').read() if os.path.exists(p) else None


def verify_source_iso():
    h = hashlib.sha1()
    with open(SRC_ISO, 'rb') as f:
        for chunk in iter(lambda: f.read(64 * 1024 * 1024), b''):
            h.update(chunk)
    if h.hexdigest() != SRC_SHA1:
        raise SystemExit(f'Source ISO SHA-1 {h.hexdigest()} does not match {SRC_SHA1}')
