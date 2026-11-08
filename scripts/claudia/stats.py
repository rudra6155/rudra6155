"""Live GitHub stats rendered as an `nvidia-smi` readout.

Runs in GitHub Actions (needs GITHUB_TOKEN). Without a token or on any API
failure it renders a placeholder with '--' — it never invents numbers.
"""
import datetime as dt
import json
import os
import sys
import urllib.request
from collections import Counter
from pathlib import Path

from common import DIM, FAINT, GREEN, GREY, ORANGE, TEXT, Scene, anim, vis

HERE = Path(__file__).parent
LOGIN = os.environ.get("PROFILE_LOGIN", "rudra6155")

QUERY = """query($login:String!){user(login:$login){
  followers{totalCount}
  repositories(ownerAffiliations:OWNER, privacy:PUBLIC, first:100, isFork:false){
    totalCount nodes{stargazerCount primaryLanguage{name}}}
  contributionsCollection{totalCommitContributions totalPullRequestContributions totalIssueContributions
    contributionCalendar{totalContributions weeks{contributionDays{date contributionCount}}}}}}"""


def fetch():
    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        return None
    req = urllib.request.Request("https://api.github.com/graphql",
                                 data=json.dumps({"query": QUERY, "variables": {"login": LOGIN}}).encode(),
                                 headers={"Authorization": f"bearer {token}", "Content-Type": "application/json"})
    try:
        with urllib.request.urlopen(req, timeout=30) as r:
            u = json.load(r)["data"]["user"]
    except Exception as e:  # noqa: BLE001
        print("stats: API failed:", e, file=sys.stderr)
        return None
    repos = u["repositories"]["nodes"]
    cc = u["contributionsCollection"]
    months = Counter()
    for w in cc["contributionCalendar"]["weeks"]:
        for d in w["contributionDays"]:
            months[d["date"][:7]] += d["contributionCount"]
    langs = Counter(r["primaryLanguage"]["name"] for r in repos if r["primaryLanguage"])
    return {
        "repos": u["repositories"]["totalCount"], "stars": sum(r["stargazerCount"] for r in repos),
        "followers": u["followers"]["totalCount"], "total": cc["contributionCalendar"]["totalContributions"],
        "commits": cc["totalCommitContributions"], "prs": cc["totalPullRequestContributions"],
        "issues": cc["totalIssueContributions"], "months": sorted(months.items())[-12:],
        "langs": langs.most_common(4), "updated": dt.datetime.now(dt.timezone.utc).strftime("%Y-%m-%d %H:%M UTC"),
    }


def build(out, t, data):
    sc = Scene(400, "rudra-smi — live GitHub stats")
    sc.frame(t)
    g = (lambda k: "--") if data is None else (lambda k: str(data[k]))
    X, CW, FS = 28, 7.8, 13
    widths = (37, 30, 33)
    full = sum(widths) + 2

    def row(*cells):
        return "|" + "|".join(c.ljust(w) for c, w in zip(cells, widths)) + "|"

    rule = "+" + "+".join("-" * w for w in widths) + "+"
    rows = [
        "+" + "-" * full + "+",
        "| " + "RUDRA-SMI 6155".ljust(26) + "Driver Version: curiosity".ljust(34) + "CUDA Version: built from scratch".ljust(full - 61) + "|",
        rule,
        row(" GPU  Name", " Public repos        Stars", " Followers"),
        row("  0   rudra6155", f" {g('repos'):>12}  {g('stars'):>11}", f" {g('followers'):>9}"),
        rule,
    ]
    for i, r in enumerate(rows):
        y = 34 + i * 18
        sc.add(f'<g {vis(t + .3 + i * .08)}>' + sc.text(X, y, r, GREY if i != 4 else TEXT, FS) + "</g>")
    y0 = 34 + len(rows) * 18 + 16
    sc.add(f'<g {vis(t + .9)}>' + sc.runs(X, y0, [("contributions, last 12 months: ", GREY, False), (g("total"), ORANGE, True),
                                                  ("   commits ", GREY, False), (g("commits"), TEXT, True),
                                                  ("   PRs ", GREY, False), (g("prs"), TEXT, True),
                                                  ("   issues ", GREY, False), (g("issues"), TEXT, True)], FS) + "</g>")
    # GPU-Util bars per month
    sc.add(f'<g {vis(t + 1.0)}>' + sc.text(X, y0 + 30, "GPU-Util (contributions / month)", DIM, 12) + "</g>")
    bx, by, bh = X + 4, y0 + 140, 92
    months = data["months"] if data else []
    peak = max([v for _, v in months] + [1])
    for i in range(12):
        x = bx + i * 74
        sc.add(f'<rect x="{x}" y="{by-bh}" width="52" height="{bh}" rx="3" fill="{FAINT}" {vis(t + 1.0)}/>')
        if i < len(months):
            m, v = months[i]
            h = max(2, v / peak * bh)
            sc.add(f'<rect class="gy" x="{x}" y="{by-h:.1f}" width="52" height="{h:.1f}" rx="3" fill="{ORANGE}" {anim("gy", .7, t + 1.1 + i * .06)}/>')
            sc.add(f'<g {vis(t + 1.6)}>' + sc.text(x + 26, by - h - 6, str(v), TEXT, 11, anchor="middle")
                   + sc.text(x + 26, by + 16, dt.date.fromisoformat(m + "-01").strftime("%b"), DIM, 11, anchor="middle") + "</g>")
    py = by + 46
    procs = "  ".join(f"{name} ({n})" for name, n in data["langs"]) if data else "--"
    sc.add(f'<g {vis(t + 1.8)}>' + sc.runs(X, py, [("Processes (top languages by repo): ", GREY, False), (procs, TEXT, False)], FS) + "</g>")
    note = f"auto-refreshed daily by GitHub Actions · last run {data['updated']}" if data else "waiting for the first GitHub Actions run"
    sc.add(f'<g {vis(t + 1.9)}>' + sc.text(X, py + 24, note, GREEN if data else DIM, 11) + "</g>")
    sc.save(out)


if __name__ == "__main__":
    sched = json.loads((HERE / "schedule.json").read_text())
    out = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE.parent.parent / "assets" / "stats.svg"
    data = fetch()
    if data is None and out.exists() and os.environ.get("GITHUB_TOKEN"):
        print("stats: keeping previous stats.svg")
        sys.exit(0)
    build(out, sched["stats"], data)
