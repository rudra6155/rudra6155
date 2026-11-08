"""Build every scene of the profile. Usage: python scripts/claudia/build.py

All scenes share one clock (seconds since the README loads): Act 1 plays,
the doors open, then each panel starts one after another.
"""
import json
import sys
from pathlib import Path

HERE = Path(__file__).parent
sys.path.insert(0, str(HERE))

import hero  # noqa: E402
import intro  # noqa: E402
import panels  # noqa: E402
import sections  # noqa: E402
import stats  # noqa: E402

ASSETS = HERE.parent.parent / "assets"
STEP = 1.0  # gap between consecutive panels starting

ORDER = [
    ("kernels", panels.kernels), ("rewardhack", panels.rewardhack), ("redis", panels.redis),
    ("bci", panels.bci), ("astar", panels.astar), ("pm25", panels.pm25), ("dcei", panels.dcei),
    ("coreml", panels.coreml), ("experience", sections.experience), ("ventures", sections.ventures),
    ("spacefood", sections.spacefood), ("stack", sections.stack), ("honours", sections.honours),
    ("stats", None), ("outro", sections.outro),
]


def main():
    ASSETS.mkdir(exist_ok=True)
    sched = {"intro": 0.0}
    t = intro.build(ASSETS / "intro.svg")
    sched["hero"] = round(t, 3)
    t = hero.build(ASSETS / "hero.svg", t)
    for name, fn in ORDER:
        sched[name] = round(t, 3)
        if fn:
            fn(ASSETS / f"{name}.svg", t)
        t += STEP
    (HERE / "schedule.json").write_text(json.dumps(sched, indent=1) + "\n")
    if not (ASSETS / "stats.svg").exists():
        stats.build(ASSETS / "stats.svg", sched["stats"], None)
    print("schedule:", ", ".join(f"{k}@{v:.1f}s" for k, v in sched.items()))


if __name__ == "__main__":
    main()
