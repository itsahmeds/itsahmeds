# -*- coding: utf-8 -*-
"""Draws assets/console.svg for the profile README: a shell session, one monospace face,
80 columns, one accent. Stdlib only. Reads scripts/activity.json (written by scripts/activity.py).
Run from the repo root:  python3 scripts/render.py"""
import io, json, math, os

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(io.open(os.path.join(ROOT, "scripts", "activity.json"), encoding="utf-8"))

MONO = "'JetBrains Mono','Cascadia Code','SF Mono','DejaVu Sans Mono',Menlo,Consolas,monospace"
FS, LH = 13, 21            # font size, line height
PADX, PADY = 28, 26
W = 720
STATUS_H = 30

C = dict(bg="#0C0E12", border="#1F242C", fg="#C6CBD3", bright="#F1F3F6", dim="#5B6370",
         faint="#2A2F38", acc="#6FD48F", accbg="#16241C", status="#11141A")

# ---------------------------------------------------------------- content
NAME, ROLE = "ahmed hameed", "software engineering by degree, marketer by trade"
LEDE = "i build things and i solve problems."
REPOS, PRIVATE = 40, 36
BUILT = [
    ("content-operations", "topical authority, cannibalisation, refresh", 485),
    ("headless-cms", "content modelling, preview, deploy pipeline", 258),
    ("vendor-review", "review queues, automated qa", 114),
    ("ai-editorial-review", "weighted rubric, findings anchored to text", 112),
    ("cro-dashboards", "ga4 and on-site conversion in one view", 73),
    ("rank-tracker", "1,000 keywords a run across 6 markets", 66),
    ("publishing-control", "24k pages, 6 content types, two-way sync", 63),
    ("review-crawlers", "3 sources, batched inside serverless caps", 45),
    ("multi-tenant-crm", "email and whatsapp outreach, lead scoring", 29),
    ("ai-search-visibility", "whether an llm mentions you, and where", 18),
]
ALSO = ["# also: a workforce app with gps and payroll, two chrome extensions, an electron qa tool",
        f"# {PRIVATE} of {REPOS} repos are private. ask and i will walk you through one."]
COLS = [
    ("range", ["next.js · react · vite", "react native · expo", "electron · chrome mv3",
               "laravel · express · fastapi", "postgres · prisma · drizzle", "convex · supabase · redis"]),
    ("reliability", ["idempotent, safe to re-run", "retry with backoff", "per-source rate budgets",
                     "circuit breakers", "65 migrations, no downtime", "vitest and playwright gates"]),
    ("ai layer", ["claude code · mcp", "llm routing, model bakeoffs", "semantic dedup at scale",
                  "prompt and eval harnesses", "agent skill chains i wrote", "n8n · make.com"]),
]
HYG = ["typed end to end", "secret scanning", "commit hooks", "dependency bots",
       "error tracking", "performance budgets", "a runbook per job"]

# ---------------------------------------------------------------- line model
# a line is a list of (text, style) segments; style in C keys plus "b" (bright bold), "cmd"
lines = []          # entries: dict(segs=[...], size=FS, gap=0)
def L(*segs, size=FS, gap=0):
    lines.append(dict(segs=[s if isinstance(s, tuple) else (s, "fg") for s in segs], size=size, gap=gap))
def blank(): L()
def cmd(tool, rest=""):
    L(("~ $ ", "dim"), (tool, "acc"), (rest, "bright"))

def spark(weeks):
    blocks = "▁▂▃▄▅▆▇█"
    mx = max(weeks) or 1
    out = []
    for w in weeks:
        lvl = 0 if w == 0 else max(1, math.ceil(w / mx * 8))
        out.append(blocks[max(lvl - 1, 0)])
    pi = weeks.index(mx)
    return "".join(out[:pi]), out[pi], "".join(out[pi + 1:])

def bar12(c, mx):
    n = c / mx * 12
    full = int(n)
    if full == 0:
        return "▌", "░" * 11
    return "█" * full, "░" * (12 - full)

# whoami
cmd("whoami")
L((NAME, "name"), size=20, gap=6)
L(ROLE)
L(LEDE)
blank()
L(("# a spec before anything gets built, agents do most of the typing,", "dim"))
L(("# n8n and make run whatever has to keep running afterwards.", "dim"))
blank()

# stats
cmd("ahmed", " stats --since 12mo")
L(("commits  ", "dim"), (f"{A['total']:,}", "b"), ("   repos  ", "dim"), (str(REPOS), "b"),
  (f" ({PRIVATE} private)", "dim"), ("   streak  ", "dim"), (f"{A['longest']}d", "b"),
  ("   active  ", "dim"), (str(A["active"]), "b"), (f"/{A['ndays']} days", "dim"))
blank()
pre, pk, post = spark(A["weeks"])
L(("52w      ", "dim"), (pre, "fg"), (pk, "acc"), (post, "fg"), ("  peak ", "dim"), (str(A["peak"]), "b"), ("/wk", "dim"))
L((" " * (9 + len(A["weeks"]) - 6) + "now ─┘", "dim"))
L((f"# regenerated every 6h by a github action. last push {A.get('last', '')}.", "dim"))
blank()

# shipped
cmd("ahmed", " ls shipped --sort commits")
L(("commits".ljust(20) + "repo".ljust(22) + "what it does", "dim"))
mx = max(c for _, _, c in BUILT)
for n, d, c in BUILT:
    full, rest = bar12(c, mx)
    L((f"{c:>5} ", "b"), (full, "fg"), (rest, "faint"), ("  ", "fg"), (n.ljust(20), "bright"), ("  " + d, "fg"))
blank()
for a in ALSO: L((a, "dim"))
blank()

# stack
cmd("ahmed", " stack --group")
L(("".join(t.ljust(29) for t, _ in COLS).rstrip(), "dim"))
for i in range(6):
    L("".join(COLS[k][1][i].ljust(29) for k in range(3)).rstrip())
blank()

# sdd
cmd("sdd", " --list")
L(("spec-driven development · 20 skills", "dim"))
blank()
L(("foundation  ", "bright"), ("runs once   ", "dim"), ("init › problem › research › requirements › platform", "fg"))
L(("                        › blueprint › ux › architecture › structure › roadmap", "fg"))
L(("delivery    ", "bright"), ("repeats     ", "dim"), ("feature › tasks › ", "fg"), ("build", "acc"), (" › verify › ship ", "fg"), ("↺", "dim"))
L(("any time    ", "bright"), ("            ", "dim"), ("status · decide · change · defect · adopt", "fg"))
blank()

# lint
cmd("ahmed", " lint --repo '*'")
for r in range(0, len(HYG), 3):
    segs = []
    for h in HYG[r:r + 3]:
        segs += [("✓ ", "acc"), (h.ljust(24), "fg")]
    L(*segs)
L((f"{REPOS} repos, 0 warnings", "dim"))
blank()

# empty prompt; contact links live in the README under the image
L(("~ $ ", "dim"), ("█", "cursor"))

# ---------------------------------------------------------------- render
esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
FILL = dict(fg=C["fg"], bright=C["bright"], dim=C["dim"], faint=C["faint"], acc=C["acc"],
            b=C["bright"], name=C["bright"], cursor=C["acc"])
BOLD = {"b", "name"}

def render():
    y = PADY + FS + 2
    out = []
    for ln in lines:
        size = ln["size"]
        if ln["segs"]:
            y += (size - FS)  # taller lines push their baseline down
            t = [f'<text x="{PADX}" y="{y}" xml:space="preserve" font-family="{MONO}" font-size="{size}" fill="{C["fg"]}">']
            for s, st in ln["segs"]:
                if not s: continue
                attrs = f' fill="{FILL[st]}"'
                if st in BOLD: attrs += ' font-weight="700"'
                if st == "cursor":
                    attrs += '><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.2s" repeatCount="indefinite"/'
                t.append(f"<tspan{attrs}>{esc(s)}</tspan>")
            t.append("</text>")
            out.append("".join(t))
        y += LH + ln["gap"]
    body_h = y - LH + PADY
    H = body_h + STATUS_H

    # tmux-style status line
    sess = "[itsahmeds]"
    wins = "  ".join(f"{i}:{n}" for i, n in enumerate(["whoami", "stats", "shipped", "stack", "sdd", "lint"]))
    sy = body_h + STATUS_H / 2 + 4
    sess_w = len(sess) * FS * 0.6 + 12
    status = (f'<rect x="0" y="{body_h}" width="{W}" height="{STATUS_H}" fill="{C["status"]}"/>'
              f'<line x1="0" y1="{body_h}" x2="{W}" y2="{body_h}" stroke="{C["faint"]}"/>'
              f'<rect x="{PADX - 6}" y="{body_h + 6}" width="{sess_w:.0f}" height="{STATUS_H - 12}" fill="{C["accbg"]}"/>'
              f'<text x="{PADX}" y="{sy}" xml:space="preserve" font-family="{MONO}" font-size="12">'
              f'<tspan fill="{C["acc"]}">{sess}</tspan><tspan fill="{C["dim"]}">   {wins}</tspan></text>'
              f'<text x="{W - PADX}" y="{sy}" text-anchor="end" font-family="{MONO}" font-size="12" fill="{C["dim"]}">'
              f'{esc(A.get("last", ""))}</text>')

    label = (f"{NAME}. {ROLE}. {LEDE} {A['total']:,} commits in the last twelve months across {REPOS} repositories, "
             f"{PRIVATE} private, longest streak {A['longest']} days, peak week {A['peak']}. Shipped: "
             + "; ".join(f"{n}, {d}, {c} commits" for n, d, c in BUILT) + ". "
             + " ".join(COLS_LABEL for COLS_LABEL in (f"{t}: {', '.join(i)}." for t, i in COLS))
             + " spec-driven development, twenty skills: foundation runs once, delivery repeats, some any time."
             + " in every repo: " + ", ".join(HYG) + ".")

    return (f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}" viewBox="0 0 {W} {H}" role="img" '
            f'aria-label="{esc(label)}">'
            f'<rect width="{W}" height="{H}" rx="6" fill="{C["bg"]}"/>'
            f'<clipPath id="r"><rect width="{W}" height="{H}" rx="6"/></clipPath><g clip-path="url(#r)">'
            + "".join(out) + status +
            f'</g><rect x="0.5" y="0.5" width="{W - 1}" height="{H - 1}" rx="6" fill="none" stroke="{C["border"]}"/>'
            f'</svg>')

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    s = render()
    io.open(os.path.join(ROOT, "assets", "console.svg"), "w", encoding="utf-8", newline="\n").write(s)
    h = s.split('height="', 1)[1].split('"', 1)[0]
    print(f"console.svg  {W}x{h}  {len(s.encode('utf-8')) // 1024} KB  {len(lines)} lines")
