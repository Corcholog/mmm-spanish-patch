"""What the game does with each text, read from the bytecode of a script file.

    python -I -X utf8 tools/script_model.py [O0 ...]     ->  counts and anomalies per file

The bytecode is the 4-byte words outside the text records (docs/KNOWLEDGE.md 4.3). We have
no full opcode table, so only the forms we understand are recognised and the rest is
skipped as opaque:

    <pointer>, 0, 0, <serial>        a text line (also into the executable's string pool)
    F0000000 <n> <pointer>           a menu option (consecutive options = one menu)
    F000000D <char> <clip>           voice clip for the next line (char: VOICES)
    F000005D 3 / 4                   narration window open / close
    F000006C ...                     scene start
    F0000006 / F0000048 ...          jump into another script file
    F0000008 <n> / F000000B <n>      label n / goto label n (labels are local to a scene)
    F0000054 2 <value>               a number drawn by the game between two text lines
                                     (OP54 with other first arguments draws card graphics)

`Script.events` lists them in file order (which is play order inside a scene); `chains()`
groups the text lines that are shown on one screen line, `pages()` the lines shown on one
screen before the player presses a key.
"""
import bisect
import functools
import os
import sys
from dataclasses import dataclass, field

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import exe_patch as xp  # noqa: E402
import olm  # noqa: E402
import project  # noqa: E402
import script_text as st  # noqa: E402

VOICES = {0: 'extra', 2: 'Kyosuke', 3: 'Reu', 4: 'Lease', 5: 'Hitoe', 6: 'Motomi', 7: 'Tae',
          8: 'Misao', 9: 'Ryo', 10: 'Kyohei'}
EXE_POOL = (0x30C800, 0x30CC00)     # RAM range of the short strings some text lines point at

OP_MENU, OP_VOICE, OP_WINDOW, OP_SCENE = 0xF0000000, 0xF000000D, 0xF000005D, 0xF000006C
OP_JUMPS = (0xF0000006, 0xF0000048)
OP_NUMBER = 0xF0000054
OP_LABEL, OP_GOTO = 0xF0000008, 0xF000000B     # OP08 <n> marks label n, OP0B <n> jumps to it


@dataclass
class TextLine:
    site: int                 # offset of the pointer word
    target: int               # file offset of the text (-1: a string of the executable's pool, in exe_text)
    serial: int
    kind: str                 # 'line', 'menu', 'exe', 'credits', 'title'
    record: int = -1          # start of the record that holds the text
    voice: str = ''
    exe_text: bytes = b''     # for kind 'exe': the string in the executable
    menu: int = -1            # for kind 'menu': index of the menu (options of one menu share it)
    number_before: bool = False   # the game draws a number right before this line


@dataclass
class Event:
    site: int
    kind: str                 # 'window_open', 'window_close', 'scene', 'jump', 'number', 'label', 'goto'
    label: int = -1           # for 'label' and 'goto': the label number (local to the scene)


@dataclass
class Script:
    name: str
    data: bytes
    events: list = field(default_factory=list)
    lines: list = field(default_factory=list)

    def text_of(self, line):
        """Original bytes the line prints."""
        if line.kind == 'exe' or line.target < 0:
            return line.exe_text
        return olm.text_at(self.data, line.target)

    def chains(self):
        """Lists of text lines shown on one screen line, in play order: a line whose text ends
        without a line break, wait or page end continues into the next line the game runs,
        unless a menu, a narration window, a scene start or a jump comes in between.

        Control flow is followed: a chain open at a goto continues after its label, and a
        line right after a label continues every chain that reaches it (by falling through
        or by a goto). So a line can belong to several chains (O0: "えーと、", "どれどれ、" and
        "ふむ。" each lead into "レゥの手は、")."""
        out, cur, pending = [], [], {}

        def close():
            out.extend(cur)
            cur.clear()

        for ev in self.events:
            if isinstance(ev, Event):
                if ev.kind == 'goto':
                    pending.setdefault(ev.label, []).extend(cur)
                    cur.clear()
                elif ev.kind == 'label':
                    cur.extend(pending.pop(ev.label, []))
                elif ev.kind != 'number':
                    close()
                    if ev.kind == 'scene':          # labels are local to a scene
                        for chs in pending.values():
                            out.extend(chs)
                        pending.clear()
                continue
            if ev.kind in ('menu', 'credits', 'title'):
                close()
                out.append([ev])
                continue
            if cur:
                for ch in cur:
                    ch.append(ev)
            else:
                cur.append([ev])
            if not st.continues_bytes(self.text_of(ev)):
                close()
        close()
        for chs in pending.values():
            out.extend(chs)
        return out

    def branch_joins(self):
        """[(line, next line)] for the pieces of a chain that the game joins across a goto,
        so the next piece is not simply the next entry in the file."""
        flow = sorted(e.site for e in self.events if isinstance(e, Event) and e.kind == 'goto')
        out = []
        for ch in self.chains():
            for a, b in zip(ch, ch[1:]):
                i = bisect.bisect_left(flow, a.site)
                if b.site < a.site or (i < len(flow) and flow[i] < b.site):
                    out.append((a, b))
        return out

    def pages(self):
        """Lists of chains shown together: a page ends at a wait for a key (\\k), when a
        narration window closes, and around every menu."""
        out, cur = [], []
        for ch in self.chains():
            if ch[0].kind == 'menu':
                if cur:
                    out.append(cur)
                    cur = []
                out.append([ch])
                continue
            cur.append(ch)
            if b'\\k' in self.text_of(ch[-1]):
                out.append(cur)
                cur = []
        if cur:
            out.append(cur)
        return out


def _exe():
    return project.read_iso_file('SLPS_251.92')


@functools.lru_cache(maxsize=None)
def build(name, data=None):
    d = data if data is not None else project.read_iso_file('OLM/' + name)
    exe = _exe()
    records, sites = olm.text_analyze(d)
    starts = sorted(records)
    kinds = {o: k for o, _, k in olm.classify(d)}
    targets = dict(sites)
    zone = sorted((t, t + olm.slot_capacity(d, t, ln)) for t, ln in records.items())
    zstarts = [z[0] for z in zone]

    def in_text(o):
        i = bisect.bisect_right(zstarts, o) - 1
        return i >= 0 and o < zone[i][1]

    s = Script(name, d)
    voice, number, menu_no, last_menu_end = '', False, -1, -1
    o = olm.HDR
    n = len(d)
    while o <= n - 4:
        if in_text(o):
            o += 4
            continue
        w = olm.u32(d, o)
        k = kinds.get(o)
        if k == 'text':
            t = targets[o]
            line = TextLine(o, t, olm.u32(d, o + 12), 'line',
                            starts[bisect.bisect_right(starts, t) - 1], voice, number_before=number)
            s.events.append(line)
            s.lines.append(line)
            voice, number = '', False
            o += 16
            continue
        if EXE_POOL[0] <= w < EXE_POOL[1] and o + 12 <= n and olm.u32(d, o + 4) == 0 and olm.u32(d, o + 8) == 0:
            off = xp.ram_to_off(w)
            line = TextLine(o, -1, olm.u32(d, o + 12), 'exe', voice=voice,
                            exe_text=bytes(exe[off:exe.index(b'\0', off)]), number_before=number)
            s.events.append(line)
            s.lines.append(line)
            voice, number = '', False
            o += 16
            continue
        if (w == OP_MENU and o + 12 <= n and EXE_POOL[0] <= olm.u32(d, o + 8) < EXE_POOL[1]):
            # a menu option whose text is a string of the executable (O0: "降りる")
            if o != last_menu_end:
                menu_no += 1
            off = xp.ram_to_off(olm.u32(d, o + 8))
            line = TextLine(o + 8, -1, olm.u32(d, o + 4), 'menu', menu=menu_no,
                            exe_text=bytes(exe[off:exe.index(b'\0', off)]))
            s.events.append(line)
            s.lines.append(line)
            last_menu_end = o + 12
            o += 12
            continue
        if w == OP_MENU and kinds.get(o + 8) == 'menu':
            if o != last_menu_end:
                menu_no += 1
            t = targets[o + 8]
            line = TextLine(o + 8, t, olm.u32(d, o + 4), 'menu', starts[bisect.bisect_right(starts, t) - 1],
                            menu=menu_no)
            s.events.append(line)
            s.lines.append(line)
            last_menu_end = o + 12
            o += 12
            continue
        if k in ('credits', 'title'):
            t = targets[o]
            line = TextLine(o, t, 0, k, starts[bisect.bisect_right(starts, t) - 1])
            s.events.append(line)
            s.lines.append(line)
        elif w == OP_VOICE:
            voice = VOICES.get(olm.u32(d, o + 4), str(olm.u32(d, o + 4)))
        elif w == OP_WINDOW and olm.u32(d, o + 4) in (3, 4):
            s.events.append(Event(o, 'window_open' if olm.u32(d, o + 4) == 3 else 'window_close'))
        elif w == OP_SCENE:
            s.events.append(Event(o, 'scene'))
        elif w in OP_JUMPS:
            s.events.append(Event(o, 'jump'))
        elif w in (OP_LABEL, OP_GOTO) and o + 8 <= n:
            s.events.append(Event(o, 'label' if w == OP_LABEL else 'goto', olm.u32(d, o + 4)))
        elif w == OP_NUMBER and olm.u32(d, o + 4) == 2:      # OP54 2, <value>: draws a number in the text
            number = True
            s.events.append(Event(o, 'number'))
        o += 4
    return s


def summary(name):
    s = build(name)
    from collections import Counter
    kinds = Counter(l.kind for l in s.lines)
    ev = Counter(e.kind for e in s.events if isinstance(e, Event))
    covered = {l.site for l in s.lines}
    missed = [o for o, _ in olm.text_sites(s.data) if o not in covered]
    chains = s.chains()
    multi = sum(1 for c in chains if len(c) > 1)
    shared = Counter(l.record for c in chains if len(c) > 1 for l in c if l.kind == 'line')
    print(f'{name}: lines {dict(kinds)}, events {dict(ev)}, chains of 2+: {multi}, '
          f'text sites not reached: {len(missed)}, records in 2+ chains: {sum(1 for v in shared.values() if v > 1)}')
    return missed


if __name__ == '__main__':
    for nm in sys.argv[1:] or project.SCRIPTS:
        summary(nm)
