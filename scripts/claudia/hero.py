"""Act 2 — the doors open: pixel name reveal + boot log."""
import random

from common import (DIM, GREEN, GREY, LINE, ORANGE, ORANGE_D, TEXT, W, Scene, anim, vis)

GLYPHS = {
    "R": ["####.", "#...#", "#...#", "####.", "#.#..", "#..#.", "#...#"],
    "U": ["#...#", "#...#", "#...#", "#...#", "#...#", "#...#", ".###."],
    "D": ["####.", "#...#", "#...#", "#...#", "#...#", "#...#", "####."],
    "A": [".###.", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
    "S": [".####", "#....", "#....", ".###.", "....#", "....#", "####."],
    "I": ["#####", "..#..", "..#..", "..#..", "..#..", "..#..", "#####"],
    "N": ["#...#", "##..#", "#.#.#", "#..##", "#...#", "#...#", "#...#"],
    "G": [".###.", "#...#", "#....", "#.###", "#...#", "#...#", ".###."],
    "H": ["#...#", "#...#", "#...#", "#####", "#...#", "#...#", "#...#"],
}


def build(out, t0):
    sc = Scene(440, "Rudra Kumar Sudhir Singh — AI systems & GPU optimization")
    T = sc.text
    H = sc.h
    sc.defs.append(f'<clipPath id="card"><rect x="6" y="4" width="{W-12}" height="{H-8}" rx="12"/></clipPath>')
    sc.add(f'<rect x="6" y="4" width="{W-12}" height="{H-8}" rx="12" fill="#0D0D0D" stroke="{LINE}"/>')

    # glow behind the doors
    sc.defs.append(f'<radialGradient id="glow"><stop offset="0" stop-color="{ORANGE}" stop-opacity=".35"/>'
                   f'<stop offset="1" stop-color="{ORANGE}" stop-opacity="0"/></radialGradient>')
    sc.add(f'<ellipse cx="{W/2}" cy="100" rx="420" ry="140" fill="url(#glow)" {vis(t0 + .4, t0 + 2.6)}/>')

    # pixel name
    P, GAP = 10, 10
    word = "RUDRA SINGH"
    width = sum(30 if ch == " " else 5 * P + GAP for ch in word) - GAP
    x, y0 = (W - width) / 2, 58
    rng = random.Random(7)
    col_global = 0
    for ch in word:
        if ch == " ":
            x += 30
            col_global += 3
            continue
        for r, row in enumerate(GLYPHS[ch]):
            for c, v in enumerate(row):
                if v != "#":
                    continue
                d = t0 + 1.0 + (col_global + c) * .018 + rng.random() * .12
                px, py = x + c * P, y0 + r * P
                sc.add(f'<g class="pop" {anim("pop", .28, d)}>'
                       f'<rect x="{px+4}" y="{py+4}" width="{P}" height="{P}" fill="{ORANGE_D}" opacity=".55"/>'
                       f'<rect x="{px}" y="{py}" width="{P-1}" height="{P-1}" fill="{ORANGE}"/></g>')
        x += 5 * P + GAP
        col_global += 6

    t1 = t0 + 2.0
    sc.add(f'<g class="up" {anim("up", .5, t1)}>' + T(W / 2, 172, "RUDRA KUMAR SUDHIR SINGH", GREY, 14, True, "middle", 'letter-spacing="5"') + "</g>")
    sc.add(f'<g class="up" {anim("up", .5, t1 + .35)}>' + T(W / 2, 202, "High school engineer · AI systems & GPU optimization · Mumbai, India", ORANGE, 15, False, "middle") + "</g>")
    sc.add(f'<g class="up" {anim("up", .5, t1 + .7)}>' + T(W / 2, 236, "I build from scratch, bypassing high-level frameworks to profile hardware bottlenecks.", TEXT, 14, False, "middle") + "</g>")
    sc.add(f'<g class="up" {anim("up", .5, t1 + .85)}>' + T(W / 2, 258, "My work spans custom Triton kernels, Rust systems programming, and real-time BCI decoding.", TEXT, 14, False, "middle") + "</g>")
    sc.add(f'<rect class="gx" x="40" y="282" width="{W-80}" height="1" fill="{LINE}" {anim("gx", .8, t1 + 1.0)}/>')

    logs = [
        "Mounted /brain — Grade 12 Science @ St. Xavier's College, Mumbai",
        "Loaded kernels: triton · cuda · c++ · rust · ros2 · pytorch",
        "Started 3 internships: AKIYAM Technologies · Akiyam Solutions · Stick & Dot Media",
        "Linked 3 preprints on Zenodo (lead author)",
    ]
    tb = t1 + 1.3
    for i, ln in enumerate(logs + ["Reached target profile.target — scroll, darling."]):
        y = 312 + i * 24
        t = tb + i * .3
        last = i == len(logs)
        sc.add(f'<g {vis(t)}>' + T(40, y, "[", DIM, 13) + T(40 + 7.8, y, "  OK  ", GREEN, 13, True) + T(40 + 7 * 7.8, y, "]", DIM, 13)
               + T(40 + 9 * 7.8, y, ln, ORANGE if last else GREY, 13, last) + "</g>")

    # the doors (closed from page load, swing open at t0)
    sc.css.append(f"@keyframes dl{{to{{transform:translateX(-{W/2+10}px)}}}}@keyframes dr{{to{{transform:translateX({W/2+10}px)}}}}")
    half = W / 2

    def door(x0, side):
        inset = "".join(f'<rect x="{x0 + 40}" y="{y}" width="{half - 80}" height="{h}" rx="6" fill="none" stroke="{ORANGE_D}" stroke-width="3"/>'
                        for y, h in [(36, 160), (226, 180)])
        kx = x0 + half - 26 if side == "l" else x0 + 26
        knob = f'<circle cx="{kx}" cy="220" r="9" fill="#F0B39B" stroke="{ORANGE_D}" stroke-width="3"/>'
        return (f'<g style="animation:d{side} 1.3s cubic-bezier(.7,0,.3,1) {t0 + .2:.3f}s forwards">'
                f'<rect x="{x0}" y="0" width="{half}" height="{H}" fill="{ORANGE}"/>{inset}{knob}</g>')

    sc.add(f'<g clip-path="url(#card)">{door(0, "l")}{door(half, "r")}'
           f'<rect x="{half-1}" y="0" width="2" height="{H}" fill="{ORANGE_D}" {vis(None, t0 + .25)}/>'
           f'<g {vis(None, t0 + .2)}>' + T(half, 330, "PRIVATE · ask Claudia ↑", "#7A3A22", 14, True, "middle") + "</g></g>")

    sc.save(out)
    return tb + len(logs) * .3 + .5
