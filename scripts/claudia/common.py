"""Shared toolkit for the 'Claudia Code' profile scenes.

Every scene is a self-contained SVG: CSS keyframes (plus a little SMIL) only,
so it animates inside a GitHub README <img>. Glyphs are placed on a fixed
monospace grid and a subset of JetBrains Mono is embedded per file.
"""
from __future__ import annotations

import base64
import html
import io
import math
from pathlib import Path

from fontTools import subset
from fontTools.ttLib import TTFont

FONT_DIR = Path(__file__).parent / "fonts"

# palette — Claude-Code-ish terminal
BG, BAR, PANEL, LINE = "#0D0D0D", "#181818", "#141414", "#262626"
ORANGE, ORANGE_D, ORANGE_L = "#D97757", "#B5583A", "#EE9B7C"
TEXT, GREY, DIM, FAINT = "#E8E6E3", "#8C8C8C", "#5A5A5A", "#2E2E2E"
RED, GREEN, PINK = "#E5484D", "#4CC38A", "#FF6B81"

W = 960
FS = 15

BASE_CSS = (
    "text{white-space:pre}"
    "@keyframes s{to{opacity:1}}@keyframes h{to{opacity:0}}"
    "@keyframes up{from{opacity:0;transform:translateY(10px)}to{opacity:1;transform:none}}"
    ".up{opacity:0}"
    "@keyframes gx{from{transform:scaleX(0)}to{transform:scaleX(1)}}"
    "@keyframes gy{from{transform:scaleY(0)}to{transform:scaleY(1)}}"
    ".gx{transform-box:fill-box;transform-origin:left center;transform:scaleX(0)}"
    ".gy{transform-box:fill-box;transform-origin:center bottom;transform:scaleY(0)}"
    "@keyframes draw{to{stroke-dashoffset:0}}"
    ".draw{stroke-dasharray:1;stroke-dashoffset:1}"
    "@keyframes pop{0%{transform:scale(0)}60%{transform:scale(1.3)}100%{transform:scale(1)}}"
    ".pop{transform-box:fill-box;transform-origin:center;transform:scale(0)}"
    "@keyframes spin{to{transform:rotate(360deg)}}"
    ".spin{transform-box:fill-box;transform-origin:center;animation:spin 1s linear infinite}"
    "@keyframes blk{50%{opacity:0}}.blk{animation:blk 1.05s step-end infinite}"
    "@keyframes pulse{50%{opacity:.35}}.pulse{animation:pulse 1.6s ease-in-out infinite}"
    "@keyframes bob{50%{transform:translateY(-3px)}}"
)


def esc(s: str) -> str:
    return html.escape(s, quote=True)


def vis(show=None, hide=None) -> str:
    """Style attr: invisible until `show`, gone at `hide` (seconds from page load)."""
    anims = []
    if show is not None:
        anims.append(f"s .01s {show:.3f}s forwards")
    if hide is not None:
        anims.append(f"h .01s {hide:.3f}s forwards")
    if not anims:
        return ""
    return f'style="opacity:{0 if show is not None else 1};animation:{",".join(anims)}"'


def anim(name, dur, t, extra="forwards", timing="ease-out") -> str:
    return f'style="animation:{name} {dur}s {timing} {t:.3f}s {extra}"'


def font_b64(ttf: Path, chars: set[str]) -> str:
    f = TTFont(ttf)
    opts = subset.Options()
    opts.flavor = "woff2"
    opts.layout_features = []
    sub = subset.Subsetter(opts)
    sub.populate(text="".join(sorted(chars)) + " ")
    sub.subset(f)
    buf = io.BytesIO()
    f.flavor = "woff2"
    f.save(buf)
    return base64.b64encode(buf.getvalue()).decode()


class Scene:
    def __init__(self, h: int, title: str, w: int = W):
        self.w, self.h, self.title = w, h, title
        self.els: list[str] = []
        self.defs: list[str] = []
        self.css: list[str] = []
        self.chars: set[str] = set()

    # ── primitives ──────────────────────────────────────────────
    def add(self, s: str):
        self.els.append(s)
        return s

    def text(self, x, y, s, color=TEXT, size=FS, bold=False, anchor=None, attrs="") -> str:
        self.chars.update(s)
        b = ' font-weight="700"' if bold else ""
        a = f' text-anchor="{anchor}"' if anchor else ""
        return f'<text x="{x:.1f}" y="{y:.1f}" fill="{color}" font-size="{size}"{b}{a} {attrs}>{esc(s)}</text>'

    def runs(self, x, y, parts, size=FS) -> str:
        """Several colored runs on one monospace line. parts = [(text, color, bold), ...]."""
        out, col = [], 0
        for s, color, bold in parts:
            out.append(self.text(x + col * size * 0.6, y, s, color, size, bold))
            col += len(s)
        return "".join(out)

    def frame(self, t: float, title: str | None = None):
        """Dark rounded terminal card that slides in at t (sized at render time)."""
        self.frame_t = t

    def tool(self, x, y, name, arg, t, done=None):
        """Claude-Code tool call line:  ● Name(arg)  — dot blinks until `done`, then turns green."""
        dot = (f'<circle cx="{x+4}" cy="{y-5}" r="4.5" fill="{DIM}" class="pulse"/>'
               f'<circle cx="{x+4}" cy="{y-5}" r="4.5" fill="{GREEN}" {vis(done)}/>') if done else \
            f'<circle cx="{x+4}" cy="{y-5}" r="4.5" fill="{ORANGE}"/>'
        self.add(f'<g {vis(t)}>{dot}' + self.text(x + 16, y, name, TEXT, FS, True)
                 + self.text(x + 16 + len(name) * FS * .6, y, f"({arg})", GREY) + "</g>")

    def elbow(self, x, y, t, color=DIM):
        """the '⎿' connector drawn as a path."""
        self.add(f'<path d="M{x} {y-13}v8h9" fill="none" stroke="{color}" stroke-width="1.4" {vis(t)}/>')

    def typed(self, x, y, s, t0, cps=55, color=TEXT, size=FS, bold=False) -> float:
        """Reveal a string one glyph at a time. Returns end time."""
        cw = size * 0.6
        for i, ch in enumerate(s):
            if ch != " ":
                self.add(f'<g {vis(t0 + i / cps)}>' + self.text(x + i * cw, y, ch, color, size, bold) + "</g>")
        return t0 + len(s) / cps

    def counter(self, x, y, values, t0, dur, color=ORANGE, size=FS, bold=True, anchor=None):
        """Count-up by swapping pre-rendered labels."""
        n = len(values)
        for i, v in enumerate(values):
            a = t0 + dur * i / (n - 1) if n > 1 else t0
            b = t0 + dur * (i + 1) / (n - 1) if i < n - 1 else None
            self.add(f'<g {vis(a, b)}>' + self.text(x, y, v, color, size, bold, anchor) + "</g>")

    def bar(self, x, y, w, h, frac, t, color=ORANGE, dur=.9, track=FAINT, rx=2):
        self.add(f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="{rx}" fill="{track}" {vis(t)}/>')
        if frac > 0:
            self.add(f'<rect class="gx" x="{x}" y="{y}" width="{w*frac:.1f}" height="{h}" rx="{rx}" fill="{color}" '
                     f'{anim("gx", dur, t, timing="cubic-bezier(.2,.8,.2,1)")}/>')

    def label_value(self, x, y, label, value, t, vcolor=ORANGE, size=14):
        self.add(f'<g class="up" {anim("up", .4, t)}>' + self.text(x, y, label, GREY, size)
                 + self.text(x + (len(label) + 1) * size * .6, y, value, vcolor, size, True) + "</g>")

    def bullets(self, x, y, lines, t0, step=.18, size=14, lh=22, color=TEXT, mark="›") -> float:
        """Lines may be str or list of runs. Returns y after the block."""
        for i, ln in enumerate(lines):
            yy = y + i * lh
            cont = isinstance(ln, str) and ln.startswith("  ")
            body = self.runs(x + 18, yy, ln, size) if isinstance(ln, list) else self.text(x + 18, yy, ln[2:] if cont else ln, color, size)
            m = "" if cont else self.text(x, yy, mark, ORANGE, size, True)
            self.add(f'<g class="up" {anim("up", .4, t0 + i * step)}>' + m + body + "</g>")
        return y + len(lines) * lh

    def star(self, cx, cy, r, color=ORANGE, rays=6, sw=2.4, cls="", attrs=""):
        d = "".join(f"M{cx - r*math.cos(math.pi*i/rays):.2f} {cy - r*math.sin(math.pi*i/rays):.2f}"
                    f"L{cx + r*math.cos(math.pi*i/rays):.2f} {cy + r*math.sin(math.pi*i/rays):.2f}" for i in range(rays))
        c = f' class="{cls}"' if cls else ""
        return f'<path{c} d="{d}" stroke="{color}" stroke-width="{sw}" stroke-linecap="round" {attrs}/>'

    def sprite(self, grid, x, y, s, pal) -> str:
        return "".join(f'<rect x="{x + c*s}" y="{y + r*s}" width="{s}" height="{s}" fill="{pal[ch]}"/>'
                       for r, row in enumerate(grid) for c, ch in enumerate(row) if ch in pal)

    # ── output ──────────────────────────────────────────────────
    def svg(self) -> str:
        reg = font_b64(FONT_DIR / "JetBrainsMono-Regular.ttf", self.chars)
        bold = font_b64(FONT_DIR / "JetBrainsMono-Bold.ttf", self.chars)
        fonts = (f"@font-face{{font-family:J;font-weight:400;src:url(data:font/woff2;base64,{reg}) format('woff2')}}"
                 f"@font-face{{font-family:J;font-weight:700;src:url(data:font/woff2;base64,{bold}) format('woff2')}}")
        return (f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {self.w} {self.h}" width="{self.w}" height="{self.h}" '
                f'font-family="J, ui-monospace, SFMono-Regular, Menlo, Consolas, monospace" xml:space="preserve">'
                f'<title>{esc(self.title)}</title>'
                f'<style>{fonts}{BASE_CSS}{"".join(self.css)}</style>'
                f'<defs>{"".join(self.defs)}</defs>' + self._frame() + "".join(self.els) + "</svg>")

    def _frame(self) -> str:
        t = getattr(self, "frame_t", None)
        if t is None:
            return ""
        return (f'<g class="up" {anim("up", .5, t)}>'
                f'<rect x="6" y="4" width="{self.w-12}" height="{self.h-8}" rx="12" fill="{BG}" stroke="{LINE}"/></g>')

    def save(self, path: Path):
        s = self.svg()
        path.write_text(s)
        print(f"  {path.name:<22} {len(s)/1024:6.1f} KB")


# Claudia, pixel sprite (16×16)
CLAUDIA = ["....HHHHHHHH....", "..HHHHLLHHHHHH..", ".HHHLLHHHHHHHHH.", ".HHHHHHHHHHHHHH.",
           "HHHHSSHHHHSSHHHH", "HHHSSSSSSSSSSHHH", "HHSSEESSSSEESSHH", "HHSSEESSSSEESSHH",
           "HHSBBSSSSSSBBSHH", "HHSSSSSMMSSSSSHH", "HHHSSSSSSSSSSHHH", "HHHhSSSSSSSShHHH",
           "HHhh..SSSS..hhHH", "HHh.TTTTTTTT.hHH", ".Hh.TTTOOTTT.hH.", "..h.TTTTTTTT.h.."]
CLAUDIA_PAL = {"H": ORANGE, "h": ORANGE_D, "L": ORANGE_L, "S": "#F4C9A8", "B": "#EE9C86",
               "T": "#2B2B2B", "O": ORANGE, "E": "#1B1B1B", "M": "#9C3F2C"}
