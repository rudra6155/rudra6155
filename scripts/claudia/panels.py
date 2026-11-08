"""Act 3 — signature project panels. Every number comes from the CV.
Curves/waveforms that are not real data are labelled 'schematic' / 'illustration'."""
import heapq
import math
import random

from common import (DIM, FAINT, GREEN, GREY, LINE, ORANGE, ORANGE_D, PINK, RED, TEXT, W,
                    Scene, anim, vis)


def head(sc, t, name, arg, sub, done):
    sc.frame(t)
    sc.tool(28, 40, name, arg, t + .3, done=done)
    sc.elbow(36, 66, t + .45)
    sc.add(f'<g {vis(t + .45)}>' + sc.text(52, 66, sub, GREY, 13) + "</g>")


def big(sc, x, y, values, t, dur, unit="", label="", size=40):
    sc.counter(x, y, values, t, dur, ORANGE, size, True)
    w = len(values[-1]) * size * .6
    if unit:
        sc.add(f'<g {vis(t + dur)}>' + sc.text(x + w + 8, y, unit, GREY, 16) + "</g>")
    if label:
        sc.add(f'<g class="up" {anim("up", .4, t + dur)}>' + sc.text(x, y + 22, label, TEXT, 13) + "</g>")


def steps(a, b, n=12, fmt="{:.2f}"):
    return [fmt.format(a + (b - a) * (1 - (1 - i / (n - 1)) ** 2)) for i in range(n)]


# ───────────────────────────── 1. LLM inference engine ─────────────────────────────
def kernels(out, t):
    sc = Scene(330, "LLM Inference Engine — 74.14 tok/s, 1,630 kernels to one CUDA Graph")
    tc = t + 3.2
    head(sc, t, "Profile", "LLM Inference Engine · C++ · Triton · CUDA · PyTorch",
         "Qwen2.5-3B · 4-bit · RTX 4060 8GB · from scratch — no HuggingFace, no vLLM", tc + 1.6)
    X, Y, WD, HT, N = 40, 108, 560, 34, 120
    cw = WD / N
    sc.add(f'<g {vis(t + .7, tc)}>' + sc.text(X, 98, "decode step, before · 1,630 Triton kernel launches per token · ~45µs each", GREY, 12) + "</g>")
    cells = []
    for i in range(N):
        d = t + .8 + i * .012
        cells.append(f'<g {vis(d)}><rect x="{X + i*cw:.2f}" y="{Y}" width="{cw*.81:.2f}" height="{HT}" fill="#3A3A3A"/>'
                     f'<rect x="{X + i*cw + cw*.81:.2f}" y="{Y}" width="{cw*.19+.4:.2f}" height="{HT}" fill="{ORANGE}"/></g>')
    sc.add(f'<g {vis(None, tc)}>' + "".join(cells) + "</g>")
    sc.add(f'<g {vis(t + 2.4, tc)}>' + sc.runs(X, 162, [("81%", RED, True), (" of decode = Python launch overhead (grey)", GREY, False)], 13) + "</g>")
    # after: one graph replay
    sc.add(f'<g {vis(tc)}>' + sc.text(X, 98, "decode step, after · captured in a single CUDA Graph · device-side KV indexing", GREY, 12) + "</g>")
    sc.add(f'<rect class="gx" x="{X}" y="{Y}" width="{WD}" height="{HT}" rx="3" fill="{ORANGE}" {anim("gx", .6, tc)}/>')
    sc.add(f'<g {vis(tc + .5)}>' + sc.text(X + WD / 2, Y + 22, "1 × cudaGraphLaunch", "#1A0E08", 14, True, "middle") + "</g>")
    sc.add(f'<g {vis(tc + .3)}>' + sc.runs(X, 162, [("launch tax eliminated", GREEN, True), (" · 5.7× faster than baseline PyTorch", GREY, False)], 13) + "</g>")
    # right: tok/s
    big(sc, 640, 140, steps(0, 74.14), tc, 1.2, "tok/s", "decode throughput")
    # bottom metrics
    by = 206
    sc.add(f'<g {vis(t + 1.0)}>' + sc.text(X, by + 10, "p99 latency", GREY, 13) + "</g>")
    sc.add(f'<rect x="200" y="{by}" width="560" height="12" rx="2" fill="{FAINT}" {vis(t + 1.0)}/>')
    sc.add(f'<g {vis(None, tc + .3)}><rect class="gx" x="200" y="{by}" width="560" height="12" rx="2" fill="{RED}" {anim("gx", .7, t + 1.0)}/></g>')
    sc.add(f'<rect class="gx" x="200" y="{by}" width="{560*14.2/108:.1f}" height="12" rx="2" fill="{ORANGE}" {anim("gx", .4, tc + .3)}/>')
    sc.add(f'<g {vis(t + 1.6, tc + .3)}>' + sc.text(775, by + 11, "108 ms", RED, 13, True) + "</g>")
    sc.add(f'<g {vis(tc + .3)}>' + sc.runs(775, by + 11, [("108 → ", DIM, False), ("14.2 ms", ORANGE, True)], 13) + "</g>")
    by2 = by + 34
    sc.add(f'<g {vis(tc + .5)}>' + sc.text(X, by2 + 10, "memory BW", GREY, 13) + "</g>")
    sc.bar(200, by2, 560, 12, .623, tc + .5)
    sc.add(f'<g {vis(tc + 1.3)}>' + sc.text(775, by2 + 11, "62.3% of peak", ORANGE, 13, True) + "</g>")
    sc.bullets(X, by2 + 52, [[("BLOCK_N=128", ORANGE, True), (" memory-coalesced Triton kernels · custom C++/CUDA RMSNorm extension", TEXT, False)]], tc + 1.0, size=13)
    sc.save(out)


# ───────────────────────────── 2. Kernel-Gen-LLM (reward hacking) ─────────────────────────────
def rewardhack(out, t):
    sc = Scene(380, "Kernel-Gen-LLM — 96% Pass@1, 2.39x geomean, caught reward hacking at 11.8x")
    t_draw = t + .9
    t_hack = t_draw + 2.0
    t_back = t_hack + 1.0
    head(sc, t, "Train", "Kernel-Gen-LLM · Qwen2.5-Coder-3B · 4-bit QLoRA · GRPO",
         "fine-tuned a 3B model to write high-performance Triton GPU kernels", t_back + 1.2)
    X0, Y0, CWd, CH = 70, 90, 470, 190

    def py(v):
        return Y0 + CH - v / 12 * CH

    for v in (0, 4, 8, 12):
        sc.add(f'<g {vis(t + .6)}><line x1="{X0}" y1="{py(v)}" x2="{X0+CWd}" y2="{py(v)}" stroke="{FAINT}"/>'
               + sc.text(X0 - 8, py(v) + 4, f"{v}×", DIM, 11, anchor="end") + "</g>")
    sc.add(f'<g {vis(t + .6)}>' + sc.text(X0, Y0 + CH + 20, "RL steps → (schematic curve · peak value is real)", DIM, 11)
           + sc.text(X0 - 40, Y0 - 10, "reward", DIM, 11) + "</g>")
    pts = [(0, .7), (.08, 1.0), (.16, 1.4), (.24, 1.7), (.32, 2.0), (.40, 2.2), (.48, 2.35),
           (.56, 2.9), (.62, 4.2), (.67, 6.6), (.71, 9.4), (.74, 11.8)]
    d = "M" + "L".join(f"{X0 + fx*CWd:.1f} {py(v):.1f}" for fx, v in pts)
    sc.add(f'<path class="draw" pathLength="1" d="{d}" fill="none" stroke="{ORANGE}" stroke-width="2.5" '
           f'stroke-linejoin="round" {anim("draw", 2.0, t_draw, timing="ease-in")}/>')
    # SFT checkpoint marker
    sx = X0 + .48 * CWd
    sc.add(f'<g {vis(t_draw + .8)}><line x1="{sx}" y1="{Y0}" x2="{sx}" y2="{Y0+CH}" stroke="{GREEN}" stroke-dasharray="3 4"/>'
           + sc.text(sx - 6, Y0 + CH - 6, "SFT ckpt", GREEN, 11, anchor="end") + "</g>")
    # hack
    hx, hy = X0 + .74 * CWd, py(11.8)
    sc.add(f'<g {vis(t_hack)}><circle cx="{hx}" cy="{hy}" r="7" fill="{RED}"/>'
           f'<circle cx="{hx}" cy="{hy}" r="14" fill="none" stroke="{RED}" class="pulse"/>'
           + sc.text(hx - 18, hy + 5, "too good to be true → 11.8×", RED, 13, True, "end") + "</g>")
    sc.add(f'<g class="up" {anim("up", .4, t_hack + .3)}>'
           f'<rect x="{hx - 290}" y="{hy + 22}" width="250" height="44" rx="6" fill="#2A1012" stroke="{RED}"/>'
           + sc.text(hx - 278, hy + 40, "REWARD HACKING DETECTED", RED, 12, True)
           + sc.text(hx - 278, hy + 57, "invalid kernels gamed the timer", "#F2A5A8", 12) + "</g>")
    # rollback arrow
    sc.add(f'<path class="draw" pathLength="1" d="M{hx+4} {hy+14}Q{hx+10} {py(.2)} {sx+6} {py(2.35)+6}" '
           f'fill="none" stroke="{GREEN}" stroke-width="2" stroke-dasharray="1" {anim("draw", .8, t_back)}/>')
    sc.add(f'<g {vis(t_back + .7)}>' + sc.text(sx + 70, py(.9) + 18, "rolled back to robust SFT checkpoint", GREEN, 12, True) + "</g>")
    # right stats
    RX = 640
    big(sc, RX, 128, [f"{v}%" for v in steps(0, 96, 10, "{:.0f}")], t_back, 1.0, "", "Pass@1 on 50 held-out tasks")
    big(sc, RX, 208, [f"{v}×" for v in steps(0, 2.39, 10)], t_back + .3, 1.0, "", "geomean kernel speedup")
    sc.bullets(36, 322, [
        [("anti-cheat harness: ", GREY, False), ("AST allowlists + ATen dispatcher interception", TEXT, False), (" · isolates GPU faults", GREY, False)],
        [("documented the RL instability", TEXT, False), (" for future alignment research", GREY, False)],
    ], t_back + .6, size=13)
    sc.save(out)


# ───────────────────────────── 3. Redis-RS ─────────────────────────────
def redis(out, t):
    sc = Scene(330, "Redis-RS — wire-compatible RESP2 server in Rust, 199/199 oracle tests, 2.66x SET")
    t_end = t + 5.2
    head(sc, t, "Serve", "Redis-RS · Rust · Tokio · RESP2 over TCP", "wire-compatible Redis server, written from scratch", t_end)
    sc.add(f'<g class="up" {anim("up", .5, t + .5)}><rect x="28" y="84" width="440" height="222" rx="8" fill="#111" stroke="{LINE}"/></g>')
    lines = [("SET kernel triton", "OK"), ("GET kernel", '"triton"'), ("SET tok_s 74.14", "OK"),
             ("# kill -9 → restart → AOF replay", None), ("GET tok_s", '"74.14"')]
    y, tt = 112, t + .8
    for cmd, reply in lines:
        if reply is None:
            sc.add(f'<g {vis(tt)}>' + sc.text(44, y, cmd, ORANGE, 13) + "</g>")
            y += 26
            tt += .7
            continue
        sc.add(f'<g {vis(tt)}>' + sc.text(44, y, "redis-rs>", GREEN, 13, True) + "</g>")
        tt = sc.typed(44 + 10 * 7.8, y, cmd, tt + .1, 30, TEXT, 13)
        sc.add(f'<g {vis(tt + .2)}>' + sc.text(44, y + 20, reply, GREY, 13) + "</g>")
        y += 44
        tt += .35
    # right column
    RX = 500
    sc.add(f'<g {vis(t + .8)}>' + sc.text(RX, 100, "byte-for-byte diff vs redis:7.4.12", GREY, 13) + "</g>")
    sc.counter(RX, 132, [f"{v}/199" for v in steps(0, 199, 14, "{:.0f}")], t + .9, 1.6, GREEN, 24, True)
    sc.add(f'<g {vis(t + 2.5)}>' + sc.text(RX + 130, 132, "oracle cases pass", TEXT, 13) + "</g>")
    sc.add(f'<g {vis(t + 2.6)}>' + sc.text(RX, 172, "throughput vs native Redis @ 4 client threads", GREY, 13) + "</g>")
    for i, (lab, v) in enumerate([("native", 1.0), ("SET", 2.66), ("GET", 2.33)]):
        yy = 186 + i * 22
        col = DIM if lab == "native" else ORANGE
        sc.add(f'<g {vis(t + 2.7)}>' + sc.text(RX, yy + 11, lab, GREY, 12) + "</g>")
        sc.bar(RX + 60, yy, 300, 13, v / 2.8, t + 2.8 + i * .15, col)
        sc.add(f'<g {vis(t + 3.5)}>' + sc.text(RX + 372, yy + 11, f"{v:.2f}×", col if lab != "native" else GREY, 12, True) + "</g>")
    sc.add(f'<g {vis(t + 3.6)}>' + sc.text(RX, 272, "mutation testing", GREY, 13) + "</g>")
    for i in range(15):
        x = RX + 140 + i * 15
        sc.add(f'<rect x="{x}" y="261" width="11" height="13" rx="2" fill="{RED}" {vis(t + 3.6, t + 3.8 + i * .08)}/>')
        sc.add(f'<rect x="{x}" y="261" width="11" height="13" rx="2" fill="{GREEN}" {vis(t + 3.8 + i * .08)}/>')
    sc.add(f'<g {vis(t + 5.0)}>' + sc.text(RX, 296, "15/15 injected bugs caught · incl. deadlocks & missed fsync", TEXT, 12) + "</g>")
    sc.save(out)


# ───────────────────────────── 4. BCI + EEG-MOABB ─────────────────────────────
def bci(out, t):
    sc = Scene(420, "Real-Time BCI Pipeline — p99 7.4 ms, 64-channel EEG; EEG-MOABB kappa 0.633")
    head(sc, t, "Stream", "Real-Time BCI Pipeline · Python · LSL · CUDA · PyTorch",
         "64-channel EEG → GPU decoding → closed-loop cursor control on real hardware", t + 4.8)
    PX, PY, PW, PH = 28, 84, 520, 206
    sc.defs.append(f'<clipPath id="eeg"><rect x="{PX+46}" y="{PY}" width="{PW-50}" height="{PH}"/></clipPath>')
    sc.add(f'<g class="up" {anim("up", .5, t + .6)}><rect x="{PX}" y="{PY}" width="{PW}" height="{PH}" rx="8" fill="#111" stroke="{LINE}"/>')
    rng = random.Random(64)
    chans = ["Fp1", "C3", "Cz", "C4", "P3", "Pz", "P4", "O1"]
    span = PW - 50
    sc.css.append(f"@keyframes scroll{{to{{transform:translateX(-{span}px)}}}}")
    traces = []
    for i, ch in enumerate(chans):
        cy = PY + 20 + i * 23
        sc.add(sc.text(PX + 10, cy + 4, ch, DIM, 11))
        f1, f2, ph = rng.randint(2, 4), rng.randint(8, 13), rng.uniform(0, 6)
        pts = []
        n = 160
        for k in range(n + 1):
            x = k / n * span
            u = k / n * 2 * math.pi
            v = 4.5 * math.sin(f1 * u + ph) + 2.2 * math.sin(f2 * u + ph * 2) + 1.4 * math.sin(23 * u + ph)
            pts.append((x, cy + v))
        d1 = "M" + "L".join(f"{PX+48+x:.1f} {y:.1f}" for x, y in pts)
        d2 = "M" + "L".join(f"{PX+48+span+x:.1f} {y:.1f}" for x, y in pts)
        color = ORANGE if ch in ("C3", "Cz", "C4") else "#6B6B6B"
        traces.append(f'<path d="{d1}{d2.replace("M", "L", 1)}" fill="none" stroke="{color}" stroke-width="1.3"/>')
    sc.add(f'<g clip-path="url(#eeg)"><g style="animation:scroll 5s linear infinite">{"".join(traces)}</g></g>')
    sc.add(sc.text(PX + PW - 10, PY + PH - 8, "8 of 64 channels · synthetic illustration", DIM, 10, anchor="end") + "</g>")
    RX = 580
    big(sc, RX, 122, [f"{v}" for v in steps(30, 7.4, 10, "{:.1f}")], t + 1.0, 1.0, "ms", "p99 end-to-end latency (< 10 ms)")
    sc.label_value(RX, 186, "LSL sync jitter", "< 0.1 ms", t + 2.1)
    sc.label_value(RX, 210, "Cohen's κ      ", "0.587", t + 2.3)
    sc.add(f'<g class="up" {anim("up", .4, t + 2.5)}>' + sc.text(RX, 230, "= 2008 BCI Competition winner (BCICIV 2a),", GREY, 12)
           + sc.text(RX, 246, "  without EOG artifact removal", GREY, 12) + "</g>")
    sc.label_value(RX, 272, "buffers        ", "O(1) lock-free ring", t + 2.7, TEXT, 13)
    sc.label_value(RX, 290, "streams        ", "dual CUDA streams", t + 2.9, TEXT, 13)
    # EEG-MOABB
    y0 = 324
    sc.add(f'<g class="up" {anim("up", .4, t + 3.1)}>' + sc.runs(28, y0, [("EEG-MOABB", ORANGE, True), (" · Riemannian tangent space vs CSP+LDA on BCICIV 2a", GREY, False)], 13) + "</g>")
    for i, (lab, v, col) in enumerate([("tangent space", .633, ORANGE), ("CSP+LDA", .490, DIM)]):
        yy = y0 + 14 + i * 22
        sc.add(f'<g {vis(t + 3.2)}>' + sc.text(28, yy + 11, lab, GREY, 12) + "</g>")
        sc.bar(150, yy, 260, 13, v, t + 3.3 + i * .15, col)
        sc.add(f'<g {vis(t + 4.0)}>' + sc.text(420, yy + 11, f"κ {v:.3f}", col if col != DIM else GREY, 12, True) + "</g>")
    sc.bullets(500, y0 + 24, ["peak 88.9% on Subject 8 · Leave-One-Run-Out",
                              "label-shuffle control: 24.8–25.9% (chance 25.0%)",
                              "mutation-tested leakage audit: 8 deliberate leaks"], t + 3.6, size=12, lh=20)
    sc.save(out)


# ───────────────────────────── 5. ROS2 navigation (A*) ─────────────────────────────
def astar_run(cols, rows, blocked, s, g):
    def hfun(a):
        dx, dy = abs(a[0] - g[0]), abs(a[1] - g[1])
        return max(dx, dy) + (math.sqrt(2) - 1) * min(dx, dy)
    openh = [(hfun(s), 0, s)]
    came, gs, order, seen = {}, {s: 0}, [], set()
    while openh:
        _, gc, cur = heapq.heappop(openh)
        if cur in seen:
            continue
        seen.add(cur)
        order.append(cur)
        if cur == g:
            break
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                if dx == dy == 0:
                    continue
                n = (cur[0] + dx, cur[1] + dy)
                if not (0 <= n[0] < cols and 0 <= n[1] < rows) or n in blocked:
                    continue
                if dx and dy and ((cur[0] + dx, cur[1]) in blocked or (cur[0], cur[1] + dy) in blocked):
                    continue
                ng = gc + (math.sqrt(2) if dx and dy else 1)
                if ng < gs.get(n, 1e9):
                    gs[n], came[n] = ng, cur
                    heapq.heappush(openh, (ng + hfun(n), ng, n))
    path, c = [g], g
    while c != s:
        c = came[c]
        path.append(c)
    return order, path[::-1]


def astar(out, t):
    sc = Scene(350, "ROS2 Navigation Stack — octile A*, 20 Hz pure pursuit, 40/40 episodes, 0 collisions")
    C, R, S = 26, 13, 17
    GX, GY = 30, 88
    rng = random.Random(2026)
    s, g = (1, 6), (24, 6)
    blocked = set()
    for x in (6, 13, 19):
        gap = rng.randrange(1, R - 1)
        for y in range(R):
            if abs(y - gap) > 1:
                blocked.add((x, y))
    for _ in range(28):
        b = (rng.randrange(C), rng.randrange(R))
        if b not in (s, g) and abs(b[0] - s[0]) + abs(b[1] - s[1]) > 2:
            blocked.add(b)
    order, path = astar_run(C, R, blocked, s, g)
    t_exp = t + .9
    k = 1.6 / len(order)
    t_path = t_exp + 1.7
    t_drive = t_path + .9
    head(sc, t, "Navigate", "ROS2 Navigation Stack · C++ · ROS2 · Gazebo · no Nav2",
         "autonomous navigation built from first principles", t_drive + 2.8)
    cells = [f'<rect x="{GX}" y="{GY}" width="{C*S}" height="{R*S}" fill="#111" stroke="{LINE}"/>']
    for (x, y) in blocked:
        cells.append(f'<rect x="{GX+x*S+1}" y="{GY+y*S+1}" width="{S-2}" height="{S-2}" rx="2" fill="#3A3A3A"/>')
    sc.add(f'<g class="up" {anim("up", .5, t + .5)}>{"".join(cells)}</g>')
    for i, (x, y) in enumerate(order):
        sc.add(f'<rect x="{GX+x*S+2}" y="{GY+y*S+2}" width="{S-4}" height="{S-4}" rx="2" fill="{ORANGE_D}" fill-opacity=".35" {vis(t_exp + i*k)}/>')
    pts = [(GX + x * S + S / 2, GY + y * S + S / 2) for x, y in path]
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    sc.add(f'<path class="draw" pathLength="1" d="{d}" fill="none" stroke="{ORANGE}" stroke-width="3" stroke-linejoin="round" {anim("draw", .8, t_path)}/>')
    for (x, y), col in ((s, GREEN), (g, PINK)):
        sc.add(f'<rect x="{GX+x*S+3}" y="{GY+y*S+3}" width="{S-6}" height="{S-6}" rx="3" fill="{col}" {vis(t + .7)}/>')
    # robot: drive along the path with a spinning lidar fan
    seg = [math.dist(pts[i], pts[i + 1]) for i in range(len(pts) - 1)]
    tot, acc, kf = sum(seg), 0, [f"0%{{transform:translate({pts[0][0]:.1f}px,{pts[0][1]:.1f}px)}}"]
    for i, L in enumerate(seg):
        acc += L
        kf.append(f"{acc/tot*100:.2f}%{{transform:translate({pts[i+1][0]:.1f}px,{pts[i+1][1]:.1f}px)}}")
    sc.css.append(f"@keyframes drive{{{''.join(kf)}}}")
    rays = "".join(f'<line x1="0" y1="0" x2="{30*math.cos(a):.1f}" y2="{30*math.sin(a):.1f}" stroke="{GREEN}" stroke-opacity=".5"/>'
                   for a in [i * math.pi / 8 for i in range(-3, 4)])
    sc.add(f'<g {vis(t_drive)}><g style="transform:translate({pts[0][0]:.1f}px,{pts[0][1]:.1f}px);animation:drive 2.6s ease-in-out {t_drive:.3f}s forwards">'
           f'<g class="spin" style="animation-duration:1.6s"><circle r="30" fill="none"/>{rays}</g>'
           f'<circle r="7" fill="{TEXT}" stroke="{ORANGE}" stroke-width="2.5"/></g></g>')
    sc.add(f'<g {vis(t + .6)}>' + sc.text(GX, GY + R * S + 18, "illustration: the planner idea replayed on a toy grid", DIM, 10) + "</g>")
    RX = 500
    big(sc, RX, 128, [f"{v}%" for v in steps(0, 100, 10, "{:.0f}")], t_drive + 2.6, .8, "", "success · 40 randomized Gazebo episodes · 0 collisions", 36)
    rows = [("planner   ", "8-connected octile A*"), ("control   ", "20 Hz pure-pursuit controller"),
            ("mapping   ", "TF2 log-odds occupancy grid"), ("lidar     ", "2° angular binning"),
            ("stress    ", "fault injection down to 0.27 RTF"), ("ci        ", "headless + reproducible in Docker")]
    for i, (a, b) in enumerate(rows):
        sc.label_value(RX, 186 + i * 22, a, b, t + 1.0 + i * .2, TEXT, 13)
    sc.save(out)


# ───────────────────────────── 6. PM2.5 acoustic agglomeration ─────────────────────────────
def pm25(out, t):
    sc = Scene(426, "Acoustic Agglomeration for PM2.5 — 88.2% reduction at 1.421 kHz")
    t_sw = t + .9
    head(sc, t, "Experiment", "Acoustic Agglomeration for PM2.5 Mitigation · Lead Author",
         "built the rig, swept the frequencies, found the resonance", t_sw + 4.0)
    X0, Y0, CWd, CH = 70, 96, 420, 180
    f0, f1 = .5, 2.5

    def px(f):
        return X0 + (f - f0) / (f1 - f0) * CWd

    def py(v):
        return Y0 + CH - v / 100 * CH

    for v in (0, 25, 50, 75, 100):
        sc.add(f'<g {vis(t + .6)}><line x1="{X0}" y1="{py(v)}" x2="{X0+CWd}" y2="{py(v)}" stroke="{FAINT}"/>'
               + sc.text(X0 - 8, py(v) + 4, f"{v}%", DIM, 11, anchor="end") + "</g>")
    sc.add(f'<g {vis(t + .6)}>' + sc.text(X0, Y0 + CH + 18, "frequency sweep 0.5 → 2.5 kHz (schematic curve · peak is real)", DIM, 11)
           + sc.text(X0 - 50, Y0 - 12, "PM2.5 reduction", DIM, 11) + "</g>")
    sc.add(f'<g {vis(t + .7)}><line x1="{X0}" y1="{py(15)}" x2="{X0+CWd}" y2="{py(15)}" stroke="{RED}" stroke-dasharray="5 4"/>'
           + sc.text(X0 + 6, py(15) - 7, "conventional filtration < 15%", RED, 11) + "</g>")
    pts = []
    for i in range(121):
        f = f0 + (f1 - f0) * i / 120
        v = 8 + 80.2 * math.exp(-((f - 1.421) / .16) ** 2) + 6 * math.exp(-((f - 2.1) / .25) ** 2)
        pts.append((px(f), py(v)))
    d = "M" + "L".join(f"{x:.1f} {y:.1f}" for x, y in pts)
    sc.add(f'<path class="draw" pathLength="1" d="{d}" fill="none" stroke="{ORANGE}" stroke-width="2.5" {anim("draw", 2.2, t_sw, timing="linear")}/>')
    pkx, pky = px(1.421), py(88.2)
    sc.add(f'<g {vis(t_sw + 1.1)}><circle cx="{pkx}" cy="{pky}" r="6" fill="{ORANGE}"/>'
           f'<circle cx="{pkx}" cy="{pky}" r="13" fill="none" stroke="{ORANGE}" class="pulse"/>'
           + sc.text(pkx + 18, pky + 4, "88.2% @ 1.421 kHz", ORANGE, 14, True) + "</g>")
    # particle box
    BX, BY, BW, BH = 540, 84, 390, 170
    sc.add(f'<g class="up" {anim("up", .5, t + .6)}><rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="8" fill="#111" stroke="{LINE}"/>'
           f'<path d="M{BX+16} {BY+70}h14l18-16v52l-18-16h-14z" fill="{GREY}"/></g>')
    t_on = t_sw + 1.1
    for i in range(3):
        sc.add(f'<g {vis(t_on)}><path d="M{BX+58+i*14} {BY+60}q10 25 0 50" fill="none" stroke="{ORANGE}" stroke-width="2" '
               f'style="animation:pulse 1s ease-in-out {i*.2:.1f}s infinite"/></g>')
    rng = random.Random(25)
    clusters = [(BX + 170, BY + 55), (BX + 260, BY + 110), (BX + 330, BY + 50), (BX + 200, BY + 128)]
    for i in range(44):
        x, y = rng.uniform(BX + 110, BX + BW - 20), rng.uniform(BY + 18, BY + BH - 18)
        cx, cy = clusters[i % 4]
        cx += rng.uniform(-7, 7)
        cy += rng.uniform(-7, 7)
        sc.css.append(f"@keyframes p{i}{{to{{transform:translate({cx-x:.1f}px,{cy-y:.1f}px)}}}}")
        sc.add(f'<g {vis(t + .7)}><circle cx="{x:.1f}" cy="{y:.1f}" r="2.6" fill="#9A9A9A" '
               f'style="animation:p{i} 1.8s cubic-bezier(.5,0,.2,1) {t_on + rng.uniform(0, .6):.3f}s forwards"/></g>')
    sc.add(f'<g {vis(t_on + 2.2)}>' + sc.text(BX + BW - 12, BY + BH - 10, "particles agglomerate → filterable", ORANGE, 11, anchor="end") + "</g>")
    sc.add(f'<g {vis(t + .7)}>' + sc.text(BX + BW - 12, BY + 18, "illustration", DIM, 10, anchor="end") + "</g>")
    sc.bullets(BX, BY + BH + 26, ["rig: Arduino Uno · Plantower PMS5003 ·",
                                  "  Scientech ST4062 function generator",
                                  "reproduced across independent trials",
                                  "open data + analysis code released"], t + 1.2, size=12, lh=19)
    sc.bullets(28, 374, [[("theory preprint: ", GREY, False), ("Stokes number · Sutherland's Law · acoustic radiation force", TEXT, False)],
                         [("predicted the capture-efficiency gains ", GREY, False), ("later confirmed by the experiment", ORANGE, True)]],
               t_sw + 2.4, size=13)
    sc.save(out)


# ───────────────────────────── DCEI ─────────────────────────────
def dcei(out, t):
    sc = Scene(262, "DCEI — Data Center Environmental Impact Index for India")
    head(sc, t, "Analyze", "DCEI · Data Center Environmental Impact Index for India · Lead Author",
         "where should India build its data centres? 50 cities scored on public data", t + 3.2)
    rows = [("Delhi", 66.0, RED), ("Chennai", 64.8, RED), ("Mumbai", 59.2, ORANGE), ("Kochi", 27.0, GREEN)]
    for i, (city, v, col) in enumerate(rows):
        y = 96 + i * 30
        sc.add(f'<g {vis(t + .7)}>' + sc.text(36, y + 12, city, TEXT, 13) + "</g>")
        sc.bar(120, y, 300, 16, v / 100, t + .8 + i * .15, col)
        sc.add(f'<g {vis(t + 1.6)}>' + sc.text(430, y + 13, f"{v:.1f}", col, 13, True) + "</g>")
    sc.add(f'<g {vis(t + 1.8)}>' + sc.text(36, 230, "highest-risk siting vs a low-risk alternative (Kochi)", DIM, 11) + "</g>")
    sc.bullets(500, 100, [
        [("sub-indices: ", GREY, False), ("water stress · carbon intensity", TEXT, False)],
        "               community impact · thermal load",
        [("sources: ", GREY, False), ("CGWB · CEA · IMD · Census 2011", TEXT, False)],
        [("robustness: ", GREY, False), ("Spearman ρ 0.87–0.95", ORANGE, True), (" (5 weightings)", GREY, False)],
        [("context: ", GREY, False), ("$32B+ committed since 2023", TEXT, False)],
        [("live dashboard: ", GREY, False), ("dcei.filtree.in", ORANGE, True)],
    ], t + 1.0, size=13, lh=24)
    sc.save(out)


# ───────────────────────────── core ML ─────────────────────────────
def coreml(out, t):
    sc = Scene(384, "GPT-From-Scratch (163k tok/s) and CIFAR-10 ResNet-18 reproduction (95.39%)")
    head(sc, t, "Train", "GPT-From-Scratch · CIFAR-10 Reproduction · PyTorch",
         "the fundamentals, rebuilt by hand and audited", t + 3.6)
    L, Rx = 36, 500
    sc.add(f'<g {vis(t + .6)}>' + sc.text(L, 100, "GPT-From-Scratch", ORANGE, 15, True) + sc.text(Rx, 100, "CIFAR-10 Reproduction", ORANGE, 15, True) + "</g>")
    sc.counter(L, 140, [f"{int(v):,}" for v in steps(0, 163000, 12, "{:.0f}")], t + .8, 1.1, TEXT, 30, True)
    sc.add(f'<g {vis(t + 1.9)}>' + sc.text(L + 7 * 18 + 8, 140, "tok/s", GREY, 15) + "</g>")
    sc.counter(Rx, 140, [f"{v}%" for v in steps(0, 95.39, 12)], t + .8, 1.1, TEXT, 30, True)
    sc.add(f'<g {vis(t + 1.9)}>' + sc.text(Rx + 6 * 18 + 8, 140, "± 0.21% · ResNet-18 · 3 seeds", GREY, 13) + "</g>")
    sc.bullets(L, 172, ["decoder-only GPT in pure PyTorch (no HF)", "lazy max-heap byte-level BPE tokenizer",
                        "fp32 softmax upcast under bfloat16", "Jacobian check: zero future-gradient flow",
                        "bit-exact PRNG checkpoint resumption"], t + 1.2, size=12, lh=20)
    sc.bullets(Rx, 172, ["600 epochs across 3 seeds, bit-exact determinism", "removed non-deterministic CUDA atomic backward",
                         "all 150MB of CIFAR-10 in VRAM as uint8", "on-device augmentations"], t + 1.4, size=12, lh=20)
    y = 290
    sc.add(f'<g {vis(t + 2.3)}>' + sc.text(L, y, "positional-embedding ablation · loss (lower is better)", GREY, 12) + "</g>")
    for i, (lab, v, col) in enumerate([("learned", 3.153, ORANGE), ("sinusoidal", 3.186, DIM)]):
        yy = y + 12 + i * 20
        sc.add(f'<g {vis(t + 2.3)}>' + sc.text(L, yy + 10, lab, GREY, 12) + "</g>")
        sc.bar(L + 96, yy, 260, 12, (v - 3.0) / .25, t + 2.4 + i * .1, col)
        sc.add(f'<g {vis(t + 3.0)}>' + sc.text(L + 364, yy + 10, f"{v:.3f}", col if col != DIM else GREY, 12, True) + "</g>")
    sc.add(f'<g {vis(t + 2.4)}>' + sc.text(L + 96, y + 62, "axis from 3.00 · 3 seeds", DIM, 10) + "</g>")
    sc.add(f'<g class="up" {anim("up", .4, t + 2.6)}>' + sc.runs(Rx, y + 2, [("citation archaeology", ORANGE, True)], 13)
           + sc.text(Rx, y + 22, "the widely cited 93.02% baseline came from a", TEXT, 12)
           + sc.text(Rx, y + 40, "community GitHub repo, not the ResNet paper →", TEXT, 12)
           + sc.runs(Rx, y + 58, [("modern recipes add ", TEXT, False), ("+2.37pp", ORANGE, True)], 12) + "</g>")
    sc.save(out)
