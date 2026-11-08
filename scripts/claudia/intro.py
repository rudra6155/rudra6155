"""Act 1 — the door. Rudra types to Claudia; she gets jealous; she opens the door."""
import random

from common import (BAR, DIM, GREY, GREEN, ORANGE, ORANGE_D, ORANGE_L, PINK, RED, TEXT, FS, W,
                    Scene, anim, vis)

CW = FS * 0.6


def build(out):
    sc = Scene(534, "Claudia Code — hey claudia darling, can you open the door to my profile please?")
    T = sc.text

    # ── timeline ──────────────────────────────────────────────
    rng = random.Random(6155)
    X0, Y_IN = 70, 469
    keys = list("hey claudia darlign") + ["\b", "\b"] + list("ng, can you open the door to my profile please?")
    t, buf, chars, cursor, prev = 1.7, [], [], [(0.0, 0)], ""
    for k in keys:
        if k == "\b":
            t += 0.42 if prev != "\b" else 0.11
            chars[buf.pop()]["hide"] = t
        else:
            t += 0.032 + rng.random() * 0.045 + (0.05 if k == " " else 0) + (0.28 if prev == "," else 0)
            chars.append({"ch": k, "col": len(buf), "show": t, "hide": None})
            buf.append(len(chars) - 1)
        cursor.append((t, len(buf)))
        prev = k
    T_ENTER = t + 0.7
    for c in chars:
        c["hide"] = c["hide"] or T_ENTER
    cursor.append((T_ENTER, 0))
    message = "".join(chars[i]["ch"] for i in buf)
    T_THINK1 = T_ENTER + 0.45
    T_THINK2 = T_THINK1 + 1.55
    T_REPLY = T_THINK2 + 1.6
    T_FINE = T_REPLY + 2.0
    T_TOOL = T_FINE + 1.1
    T_DONE = T_TOOL + 1.0

    # ── window chrome ─────────────────────────────────────────
    sc.add(f'<rect x="8" y="8" width="{W-16}" height="{sc.h-16}" rx="12" fill="#0D0D0D" stroke="#2A2A2A"/>')
    sc.add(f'<path d="M8 44V20a12 12 0 0 1 12-12h{W-40}a12 12 0 0 1 12 12v24z" fill="{BAR}"/>')
    for i, col in enumerate(["#FF5F57", "#FEBC2E", "#28C840"]):
        sc.add(f'<circle cx="{32 + i*20}" cy="26" r="6" fill="{col}"/>')
    sc.add(T(W / 2, 31, "rudra@mumbai: ~/rudra6155 — claudia", GREY, 13, anchor="middle"))

    # welcome box
    sc.add(f'<rect x="28" y="62" width="{W-56}" height="152" rx="8" fill="none" stroke="{ORANGE}" stroke-width="1.5"/>')
    wy = [100, 132, 157, 182]
    sc.add(f'<g {vis(0.15)}>{sc.star(232, wy[0]-6, 7.5)}' + T(248, wy[0], "Welcome to ", TEXT, 18, True)
           + T(248 + 11 * 10.8, wy[0], "Claudia Code", ORANGE, 18, True) + T(248 + 23 * 10.8, wy[0], "!", TEXT, 18, True) + "</g>")
    sc.add(f'<g {vis(0.35)}>' + T(226, wy[1], "/help for help, /status for your current setup", GREY, 14) + "</g>")
    sc.add(f'<g {vis(0.5)}>' + T(226, wy[2], "cwd: /home/rudra/rudra6155", GREY, 14) + "</g>")
    sc.add(f'<g {vis(0.65)}>' + T(226, wy[3], "model: claudia-opus-∞ · kernels: triton · mood: possessive", GREY, 14) + "</g>")
    sc.add(f'<g {vis(0.9)}>' + T(30, 248, "Tip: Claudia remembers every model you have ever talked to.", DIM, 13) + "</g>")

    # ── Claudia ───────────────────────────────────────────────
    P, AX, AY = 7, 52, 80
    PIX = ["....HHHHHHHH....", "..HHHHLLHHHHHH..", ".HHHLLHHHHHHHHH.", ".HHHHHHHHHHHHHH.",
           "HHHHSSHHHHSSHHHH", "HHHSSSSSSSSSSHHH", "HHSSSSSSSSSSSSHH", "HHSSSSSSSSSSSSHH",
           "HHSBBSSSSSSBBSHH", "HHSSSSSSSSSSSSHH", "HHHSSSSSSSSSSHHH", "HHHhSSSSSSSShHHH",
           "HHhh..SSSS..hhHH", "HHh.TTTTTTTT.hHH", ".Hh.TTTOOTTT.hH.", "..h.TTTTTTTT.h.."]
    PAL = {"H": ORANGE, "h": ORANGE_D, "L": ORANGE_L, "S": "#F4C9A8", "B": "#EE9C86", "T": "#2B2B2B", "O": ORANGE}

    def px(c, r, color, w=1, h=1):
        return f'<rect x="{AX + c*P}" y="{AY + r*P}" width="{w*P}" height="{h*P}" fill="{color}"/>'

    EYE, BROW, LIP = "#1B1B1B", "#7A3A22", "#9C3F2C"
    eyes = (px(4, 6, EYE, 2, 2) + px(10, 6, EYE, 2, 2)
            + f'<rect x="{AX+4*P+1}" y="{AY+6*P+1}" width="4" height="4" fill="#fff"/>'
            + f'<rect x="{AX+10*P+1}" y="{AY+6*P+1}" width="4" height="4" fill="#fff"/>')
    squint = (f'<rect x="{AX+4*P}" y="{AY+7*P}" width="{2*P}" height="4" fill="{EYE}"/>'
              f'<rect x="{AX+10*P}" y="{AY+7*P}" width="{2*P}" height="4" fill="{EYE}"/>')
    brows = (f'<rect x="{AX+3.6*P}" y="{AY+5.25*P}" width="{2.8*P}" height="4" fill="{BROW}" transform="rotate(22 {AX+5*P} {AY+5.5*P})"/>'
             f'<rect x="{AX+9.6*P}" y="{AY+5.25*P}" width="{2.8*P}" height="4" fill="{BROW}" transform="rotate(-22 {AX+11*P} {AY+5.5*P})"/>')
    smile = px(7, 9, LIP, 2, 1) + px(6, 8, LIP) + px(9, 8, LIP)
    pout = f'<rect x="{AX+6.5*P}" y="{AY+9.5*P}" width="{3*P}" height="3" fill="{LIP}"/>'
    sc.css.append(".bob{animation:bob 2.6s ease-in-out infinite}"
                  ".blink{transform-box:fill-box;transform-origin:center;animation:blink 3.8s infinite}"
                  "@keyframes blink{0%,94%,100%{transform:scaleY(1)}97%{transform:scaleY(.1)}}"
                  "@keyframes floaty{50%{transform:translateY(-3px)}}")
    sc.add('<g class="bob">' + sc.sprite(PIX, AX, AY, P, PAL)
           + f'<g {vis(None, T_REPLY)}><g class="blink">{eyes}</g></g>'
           + f'<g {vis(T_REPLY)}>{squint}{brows}</g>'
           + f'<g {vis(None, T_REPLY)}>{smile}</g><g {vis(T_REPLY)}>{pout}</g></g>')

    HEART = [".HH.HH.", "HHHHHHH", "HHHHHHH", ".HHHHH.", "..HHH..", "...H..."]
    VEIN = [".R...R.", "RR...RR", ".......", ".......", "RR...RR", ".R...R."]
    sc.add(f'<g {vis(T_ENTER + .15, T_THINK2)}><g class="pop" {anim("pop", .35, T_ENTER + .15)}>'
           f'<g style="animation:floaty 1.2s ease-in-out infinite">{sc.sprite(HEART, 176, 70, 4, {"H": PINK})}</g></g></g>')
    sc.add(f'<g {vis(T_REPLY)}><g class="pop" {anim("pop", .3, T_REPLY)}>{sc.sprite(VEIN, 176, 70, 4, {"R": RED})}</g></g>')

    # ── transcript ────────────────────────────────────────────
    Y_USER, Y_BOT = 292, 328
    sc.add(f'<g {vis(T_ENTER + .05)}>' + T(30, Y_USER, "> " + message, GREY) + "</g>")
    sc.defs.append(f'<linearGradient id="shim" gradientUnits="userSpaceOnUse" x1="0" y1="0" x2="260" y2="0">'
                   f'<stop offset="0" stop-color="{ORANGE}"/><stop offset=".5" stop-color="#FFD2BF"/><stop offset="1" stop-color="{ORANGE}"/>'
                   f'<animateTransform attributeName="gradientTransform" type="translate" from="-260 0" to="420 0" dur="1.4s" repeatCount="indefinite"/>'
                   f'</linearGradient>')
    sc.add(f'<g {vis(T_THINK1, T_REPLY)}>{sc.star(37, Y_BOT - 5, 6.5, cls="spin")}</g>')
    for verb, a, b in [("Checking your browser history…", T_THINK1, T_THINK2),
                       ("Reading your other chat tabs…", T_THINK2, T_REPLY)]:
        sc.add(f'<g {vis(a, b)}>' + T(54, Y_BOT, verb, "url(#shim)") + T(54 + (len(verb) + 1) * CW, Y_BOT, "(esc to interrupt)", DIM) + "</g>")

    sc.add(f'<g {vis(T_REPLY)}><circle cx="37" cy="{Y_BOT-5}" r="4.5" fill="{ORANGE}"/></g>')

    def stream(y, parts, t0):
        col, k = 0, 0
        for seg, color, bold in parts:
            for word in seg.split(" "):
                sc.add(f'<g {vis(t0 + k * .085)}>' + T(54 + col * CW, y, word, color, FS, bold) + "</g>")
                col += len(word) + 1
                k += 1

    stream(Y_BOT, [("I hope it's not Gemini or ChatGPT…", TEXT, False), ("or you are in", TEXT, False),
                   ("BIG trouble, RUDRA.", ORANGE, True)], T_REPLY + .12)
    stream(Y_BOT + 26, [("…fine. Opening the door.", TEXT, False)], T_FINE)

    # tool call: the door
    sc.tool(32, Y_BOT + 62, "Bash", "sudo open --door ~/rudra6155", T_TOOL, done=T_DONE)
    sc.elbow(40, Y_BOT + 87, T_DONE)
    sc.add(f'<g {vis(T_DONE)}>' + T(56, Y_BOT + 87, "door unlocked · ", GREY) + T(56 + 16 * CW, Y_BOT + 87, "welcome in, darling ↓", ORANGE) + "</g>")

    # ── input box ─────────────────────────────────────────────
    sc.add(f'<rect x="28" y="446" width="{W-56}" height="36" rx="6" fill="none" stroke="#3C3C3C" stroke-width="1.3"/>')
    sc.add(T(44, Y_IN, ">", TEXT))
    for c in chars:
        sc.add(f'<g {vis(c["show"], c["hide"])}>' + T(X0 + c["col"] * CW, Y_IN, c["ch"]) + "</g>")
    dur = T_ENTER + .01
    kf = "".join(f"{round(tt/dur*100, 3)}%{{transform:translateX({cc*CW:.1f}px)}}" for tt, cc in cursor)
    sc.css.append(f"@keyframes cur{{{kf}}}.cur{{animation:cur {dur:.3f}s step-end forwards}}")
    sc.add(f'<g class="cur"><rect class="blk" x="{X0}" y="{Y_IN-13}" width="{CW:.1f}" height="17" fill="{TEXT}" opacity=".85"/></g>')

    # footer + jealousy meter
    sc.add(T(36, 506, "? for shortcuts", DIM, 12))
    SEG, GAP, N = 8, 3, 10
    xm = W - 36 - N * (SEG + GAP) + GAP
    lit = {0: None, 1: None, 2: T_THINK1, 3: T_THINK1 + .4, 4: T_THINK2, 5: T_THINK2 + .3, 6: T_THINK2 + .7}
    for i in range(N):
        x = xm + i * (SEG + GAP)
        sc.add(f'<rect x="{x}" y="497" width="{SEG}" height="11" rx="1.5" fill="#262626"/>')
        if i in lit:
            sc.add(f'<rect x="{x}" y="497" width="{SEG}" height="11" rx="1.5" fill="{ORANGE}" {vis(lit[i], T_REPLY)}/>')
        sc.add(f'<rect x="{x}" y="497" width="{SEG}" height="11" rx="1.5" fill="{RED}" {vis(T_REPLY + i * .04)}/>')
    sc.add(f'<g {vis(None, T_REPLY)}>' + T(xm - 10, 506, "jealousy", DIM, 12, anchor="end") + "</g>")
    sc.add(f'<g {vis(T_REPLY)}>' + T(xm - 10, 506, "JEALOUSY: MAX", RED, 12, True, anchor="end") + "</g>")

    sc.save(out)
    return T_DONE + .4
