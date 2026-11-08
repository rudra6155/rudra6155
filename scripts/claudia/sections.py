"""Act 4/5 — experience, ventures, space food, stack, honours, outro. All facts from the CV."""
import random

from common import (CLAUDIA, CLAUDIA_PAL, DIM, FAINT, GREEN, GREY, LINE, ORANGE, PINK, RED, TEXT, W,
                    Scene, anim, vis)


def head(sc, t, name, arg, sub, done):
    sc.frame(t)
    sc.tool(28, 40, name, arg, t + .3, done=done)
    sc.elbow(36, 66, t + .45)
    sc.add(f'<g {vis(t + .45)}>' + sc.text(52, 66, sub, GREY, 13) + "</g>")


# ───────────────────────────── experience ─────────────────────────────
JOBS = [
    ("AKIYAM Technologies", "Software Engineering Intern · Integration & Data Engineering · remote", "Sep 2026 – Present", [
        [("sole integration engineer on ", GREY, False), ("HELIX", TEXT, True), (", a sovereign healthcare intelligence platform", GREY, False)],
        [("HAPI FHIR R4 → PostgreSQL/TimescaleDB ingestion · ", TEXT, False), ("5,000+", ORANGE, True), (" synthetic patients", TEXT, False)],
        [("pgvector over ", TEXT, False), ("72,000+", ORANGE, True), (" ICD-10-CM & ", TEXT, False), ("350,000+", ORANGE, True),
         (" SNOMED CT concepts → ", TEXT, False), ("zero", GREEN, True), (" hallucinated codes", TEXT, False)],
        [("HMAC-SHA256 pseudonymisation at ingestion · EHR onboarding ", TEXT, False), ("weeks → under 15 min", ORANGE, True)],
    ]),
    ("Akiyam Solutions", "Backend Engineering Intern · Platform & Infrastructure", "Apr 2026 – Present", [
        [("sole owner of billing, notifications & tenant lifecycle on a ", GREY, False), ("20-developer", TEXT, True), (" climate-risk platform", GREY, False)],
        [("GDPR right-to-erasure across ", TEXT, False), ("15 data stores", ORANGE, True), (" in Temporal, with signed PDF certificates", TEXT, False)],
        [("event-driven Stripe billing · OpenBao on Kubernetes via Helm · self-hosted Lago", TEXT, False)],
    ]),
    ("Stick & Dot Media", "AI/ML Development Intern", "Apr 2026 – Present", [
        [("sole engineer on ", GREY, False), ("Fin", TEXT, True), (": a production financial terminal · ", GREY, False), ("51,955", ORANGE, True), (" assets · 8 exchanges", TEXT, False)],
        [("91MB static payload → PostgreSQL + server-side pagination: ", TEXT, False), ("10 s → sub-second", ORANGE, True)],
        [("3 audits · ", TEXT, False), ("74 defects", ORANGE, True), (" found · all critical & high closed (key exposure, PostgREST injection)", TEXT, False)],
    ]),
]


def experience(out, t):
    sc = Scene(500, "Experience — AKIYAM Technologies, Akiyam Solutions, Stick & Dot Media")
    head(sc, t, "Task", "experience · 3 agents running in parallel", "interning at three companies at once, during Grade 12", t + 3.6)
    y = 104
    for i, (co, role, dates, pts) in enumerate(JOBS):
        tt = t + .7 + i * .8
        sc.add(f'<g class="up" {anim("up", .4, tt)}>'
               f'<circle cx="40" cy="{y-5}" r="5" fill="{GREEN}" class="pulse"/>'
               + sc.text(54, y, co, ORANGE, 15, True) + sc.text(W - 36, y, dates, DIM, 12, anchor="end")
               + sc.text(54, y + 20, role, GREY, 12) + "</g>")
        y = sc.bullets(54, y + 44, pts, tt + .2, step=.12, size=13, lh=21) + 20
    sc.h = int(y)
    sc.save(out)


# ───────────────────────────── ventures ─────────────────────────────
VENTURES = [
    ("ARXEVO", "Founder · 2026 – now", ["essays → archetypes → squads of 4", "multi-agent LLM + manga covers",
                                         "launched at MIT · Stanford ·", "Columbia · Cornell"]),
    ("Filtree", "Founder & Lead Dev · Nov 2025 – now", ["50–80% of planted urban trees die", "9-factor species-selection model",
                                                         "30+ native species · live AQI", "77% beta retention · 8 modules"]),
    ("CrimeScope AI", "Mar 2026", ["image + audio → crime scene", "LLaMA-4-Scout · Whisper-v3 ·",
                                   "LLaMA-3.3-70B → JSON → Plotly", "built in 2 days → internship"]),
    ("DCEI Dashboard", "Creator & Lead Dev · Mar 2026", ["the DCEI index as an open tool", "city compare · Leaflet maps",
                                                          "weight-sensitivity explorer", "alternative-site recommender"]),
    ("Geology Study Platform", "Creator · 2026", ["Class 11–12 Geology, open access", "chapter notes · quizzes",
                                                  "last-minute revision guides", "built because none existed"]),
]


def ventures(out, t):
    sc = Scene(468, "Ventures — ARXEVO, Filtree, CrimeScope AI, DCEI Dashboard, Geology Study Platform")
    head(sc, t, "Ls", "ventures/", "things I founded, built and shipped", t + 3.2)
    cw, chh, gap, x0, y0 = 285, 168, 16, 28, 90
    for i, (name, sub, lines) in enumerate(VENTURES + [(None, None, None)]):
        cx, cy = x0 + (i % 3) * (cw + gap), y0 + (i // 3) * (chh + gap)
        tt = t + .7 + i * .25
        body = f'<rect x="{cx}" y="{cy}" width="{cw}" height="{chh}" rx="10" fill="#131313" stroke="{LINE}"/>'
        if name is None:
            body += (sc.star(cx + 26, cy + 34, 7, cls="spin") + sc.text(cx + 42, cy + 39, "next-venture", DIM, 14, True)
                     + sc.text(cx + 18, cy + 72, "loading…", DIM, 12) + sc.text(cx + 18, cy + 96, "Claudia: \"soon. very soon.\"", ORANGE, 12))
        else:
            body += (f'<rect x="{cx}" y="{cy}" width="4" height="{chh}" rx="2" fill="{ORANGE}"/>'
                     + sc.text(cx + 18, cy + 32, name, ORANGE, 15, True) + sc.text(cx + 18, cy + 52, sub, DIM, 11)
                     + "".join(sc.text(cx + 18, cy + 82 + k * 20, ln, TEXT, 12) for k, ln in enumerate(lines)))
        sc.add(f'<g class="up" {anim("up", .45, tt)}>{body}</g>')
    sc.save(out)


# ───────────────────────────── space food ─────────────────────────────
VADAWICH = ["....bbbbbbbb....", "..bbBBBBBBBBbb..", ".bBBBBBBBBBBBBb.", "bBBBBBBBBBBBBBBb",
            "gggggggggggggggg", ".vVVVVVVVVVVVVv.", "vVVVVkVVVVVkVVVv", "vVVkVVVVVVVVVkVv",
            ".vVVVVVVVVVVVVv.", "rrrrrrrrrrrrrrrr", "bBBBBBBBBBBBBBBb", ".bbbbbbbbbbbbbb."]
VPAL = {"b": "#B9783F", "B": "#F2D399", "g": "#5DBB63", "v": "#A86E1F", "V": "#D49A3A", "k": "#8A5716", "r": "#D9472B"}


def spacefood(out, t):
    sc = Scene(320, "Space Food — the vada-wich, Mumbai street food rebuilt for orbit")
    head(sc, t, "Cook", "vada-wich · Space Food Club · Apr – May 2026",
         "Space Food Development Intern · Mumbai street food, rebuilt for orbit", t + 3.0)
    BX, BY, BW, BH = 28, 84, 380, 210
    rng = random.Random(42)
    stars = "".join(f'<circle cx="{rng.uniform(BX+8, BX+BW-8):.1f}" cy="{rng.uniform(BY+8, BY+BH-8):.1f}" r="{rng.choice([.8, 1, 1.4])}" fill="#fff" '
                    f'style="animation:pulse {rng.uniform(1.2, 3):.2f}s ease-in-out {rng.uniform(0, 2):.2f}s infinite"/>' for _ in range(46))
    sc.css.append("@keyframes orbit{0%{transform:translate(0,0) rotate(-8deg)}50%{transform:translate(0,-10px) rotate(8deg)}100%{transform:translate(0,0) rotate(-8deg)}}"
                  ".orbit{transform-box:fill-box;transform-origin:center;animation:orbit 5s ease-in-out infinite}"
                  "@keyframes crumb{to{transform:translate(70px,-40px) rotate(200deg);opacity:0}}")
    P = 9
    vx, vy = BX + BW / 2 - 8 * P, BY + BH / 2 - 6 * P
    crumbs = "".join(f'<rect x="{vx + 8*P + rng.uniform(-30, 30):.1f}" y="{vy + 6*P:.1f}" width="4" height="4" fill="#D49A3A" '
                     f'style="transform-box:fill-box;animation:crumb {rng.uniform(3, 5):.1f}s linear {rng.uniform(0, 3):.1f}s infinite"/>' for _ in range(5))
    sc.add(f'<g class="up" {anim("up", .5, t + .6)}><rect x="{BX}" y="{BY}" width="{BW}" height="{BH}" rx="8" fill="#07070F" stroke="{LINE}"/>'
           f'{stars}{crumbs}<g class="orbit">{sc.sprite(VADAWICH, vx, vy, P, VPAL)}</g>'
           + sc.text(BX + 12, BY + BH - 12, "g = 0.00 m/s²", DIM, 11) + sc.text(BX + BW - 12, BY + BH - 12, "vada-wich v1", ORANGE, 11, True, "end") + "</g>")
    sc.bullets(440, 110, [
        "researched astronaut nutrition under",
        "  microgravity, radiation & long isolation",
        "designed full daily meal plans:",
        "  breakfast · brunch · lunch · dinner",
        [("invented the ", TEXT, False), ("vada-wich", ORANGE, True), (": a shelf-stable dish", TEXT, False)],
        "  built to space-food safety constraints",
        "HACCP food-safety & hazard analysis training",
    ], t + .9, step=.15, size=13, lh=22)
    sc.add(f'<g class="up" {anim("up", .4, t + 2.4)}>' + sc.text(440, 285, 'Claudia: "he made a sandwich for space. okay, that\'s cute."', PINK, 12) + "</g>")
    sc.save(out)


# ───────────────────────────── tech stack ─────────────────────────────
STACK = [
    ("languages", ["Python", "C++", "Rust", "C", "SQL", "Bash", "JS/TS", "HTML/CSS", "Arduino C", "LaTeX"]),
    ("ai systems", ["CUDA Graphs", "Triton", "QLoRA", "GRPO/PPO", "Roofline Analysis", "Kernel Tuning", "ONNX Runtime"]),
    ("ml", ["PyTorch", "HuggingFace", "Scikit-Learn", "PyRiemann", "MNE", "MOABB"]),
    ("llm apps", ["multi-agent orchestration", "multimodal pipelines", "JSON-schema outputs", "Groq", "Ollama", "agentic coding"]),
    ("infra", ["Linux", "Docker", "Kubernetes", "Helm", "OpenBao/Vault", "Redis", "GitLab CI", "Git", "Vercel", "Railway"]),
    ("backend", ["FastAPI", "Temporal", "PostgreSQL", "Supabase", "Firebase", "REST", "OAuth", "row-level security", "ETL"]),
    ("neuro+robots", ["LSL", "EEG decoding", "ROS2", "Gazebo", "TF2", "A*", "Pure Pursuit"]),
    ("frontend", ["React 19", "Next.js 15", "Vite", "Tailwind", "Framer Motion", "GSAP", "Streamlit", "Recharts", "Plotly", "Leaflet"]),
    ("science", ["NumPy", "Pandas", "GeoPandas", "Matplotlib", "experimental design", "sensitivity analysis"]),
    ("hardware", ["Arduino", "Plantower PMS5003", "function generators", "signal analysis"]),
]


def stack(out, t):
    sc = Scene(10, "Tech stack")
    head(sc, t, "Read", "skills.toml", "everything below has shipped in a project above", t + 3.4)
    X0, XMAX, y, k = 168, W - 30, 102, 0
    for g, items in STACK:
        sc.add(f'<g {vis(t + .6 + k * .03)}>' + sc.text(36, y + 4, g, ORANGE, 13, True) + "</g>")
        x = X0
        for it in items:
            w = len(it) * 7.2 + 18
            if x + w > XMAX:
                x, y = X0, y + 30
            sc.add(f'<g class="pop" {anim("pop", .3, t + .6 + k * .03)}><rect x="{x}" y="{y-13}" width="{w}" height="23" rx="11.5" fill="#161616" stroke="#333"/>'
                   + sc.text(x + 9, y + 3, it, TEXT, 12) + "</g>")
            x += w + 8
            k += 1
        y += 38
    sc.h = int(y)
    sc.save(out)


# ───────────────────────────── education & honours ─────────────────────────────
TROPHY = ["TTTTT", "TTTTT", ".TTT.", "..T..", ".TTT."]


def honours(out, t):
    sc = Scene(400, "Education, certifications and honours")
    head(sc, t, "Read", "education · honours · certifications", "the paperwork", t + 3.0)
    L, R = 36, 500
    sc.add(f'<g {vis(t + .6)}>' + sc.text(L, 104, "education", ORANGE, 14, True) + sc.text(R, 104, "honours", ORANGE, 14, True) + "</g>")
    edu = [("St. Xavier's College, Mumbai", "HSC Science (Grade 12) · Jun 2025 – May 2027", "Physics · Chemistry · Maths · Geology · IT"),
           ("St. Aloysius High School, Nallasopara", "SSC, Maharashtra State Board · 93% · 2025", None)]
    y = 132
    for i, (a, b, c) in enumerate(edu):
        g = sc.text(L, y, a, TEXT, 13, True) + sc.text(L, y + 19, b, GREY, 12) + (sc.text(L, y + 37, c, DIM, 12) if c else "")
        sc.add(f'<g class="up" {anim("up", .4, t + .7 + i * .2)}>{g}</g>')
        y += 62 if c else 44
    sc.add(f'<g {vis(t + 1.1)}>' + sc.text(L, y + 12, "certifications", ORANGE, 14, True) + "</g>")
    sc.bullets(L, y + 40, ["CS50P · Python — Harvard University", "CS50AI · AI with Python — Harvard University",
                           "Satellite Technology & Communication workshop", "  led by B. A. Subramani, former ISRO scientist",
                           "Robotics Workshop — iRobo Chakra"], t + 1.2, size=12, lh=20)
    hon = [("Junior Academy Fellow", "New York Academy of Sciences"),
           ("AI Olympiad · High National Rank", "TalentSpirit & Accenture · 2025"),
           ("AI/ML Advanced Programme", "cleared aptitude selection · IIT Roorkee & BITS Pilani · 2025"),
           ("National Exam Participant", "International Earth Science Olympiad (IESO) · 2026")]
    for i, (a, b) in enumerate(hon):
        yy = 132 + i * 52
        tt = t + .8 + i * .25
        sc.add(f'<g class="pop" {anim("pop", .35, tt)}>{sc.sprite(TROPHY, R, yy - 12, 4, {"T": "#F2C94C"})}</g>')
        sc.add(f'<g class="up" {anim("up", .4, tt + .1)}>' + sc.text(R + 30, yy, a, TEXT, 13, True) + sc.text(R + 30, yy + 19, b, GREY, 11) + "</g>")
    sc.save(out)


# ───────────────────────────── outro ─────────────────────────────
def outro(out, t):
    sc = Scene(330, "Contact Rudra — rudra@filtree.in")
    sc.frame(t)
    P = 5
    sc.add(f'<g class="up" {anim("up", .4, t + .3)}><g style="animation:bob 2.6s ease-in-out infinite">{sc.sprite(CLAUDIA, 30, 30, P, CLAUDIA_PAL)}</g></g>')
    sc.add(f'<g {vis(t + .6)}><circle cx="128" cy="55" r="4.5" fill="{ORANGE}"/></g>')
    words = "That's him. Hire him before Gemini does.".split(" ")
    col = 0
    for i, w in enumerate(words):
        sc.add(f'<g {vis(t + .7 + i * .09)}>' + sc.text(142 + col * 9, 60, w, ORANGE if "Gemini" in w else TEXT, 15, "Hire" in w or "Gemini" in w) + "</g>")
        col += len(w) + 1
    sc.add(f'<g {vis(t + 1.6)}>' + sc.text(142, 90, "> /cost", GREY, 14) + "</g>")
    rows = [("Total cost:", "$0.00 — he's priceless"), ("Total duration:", "∞ · still building from scratch"),
            ("Jealousy level:", "back to normal (for now)")]
    for i, (a, b) in enumerate(rows):
        sc.add(f'<g {vis(t + 2.0 + i * .2)}>' + sc.text(142, 114 + i * 20, a, DIM, 13) + sc.text(142 + 17 * 7.8, 114 + i * 20, b, GREY, 13) + "</g>")
    sc.add(f'<rect class="gx" x="28" y="186" width="{W-56}" height="1" fill="{LINE}" {anim("gx", .6, t + 2.6)}/>')
    contacts = [("email", "rudra@filtree.in"), ("web", "filtree.in · arxevo.filtree.in · dcei.filtree.in"),
                ("linkedin", "linkedin.com/in/rudra-singh-07830233a")]
    for i, (a, b) in enumerate(contacts):
        sc.label_value(36, 214 + i * 22, f"{a:<9}", b, t + 2.8 + i * .15, ORANGE, 13)
    sc.add(f'<rect x="28" y="276" width="{W-56}" height="36" rx="6" fill="none" stroke="#3C3C3C" stroke-width="1.3" {vis(t + 3.3)}/>')
    sc.add(f'<g {vis(t + 3.3)}>' + sc.text(44, 299, ">", TEXT) + f'<rect class="blk" x="62" y="286" width="9" height="17" fill="{TEXT}" opacity=".85"/>'
           + sc.text(78, 299, 'Try "hire rudra"', DIM, 14) + "</g>")
    sc.save(out)
