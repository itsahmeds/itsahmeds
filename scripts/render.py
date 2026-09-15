# -*- coding: utf-8 -*-
"""Draws assets/console.svg (and, with --light, assets/console-light.svg) for the profile README:
a shell session with one monospace face, one accent, each command on a rule with its output
indented beneath. Stdlib only. Reads scripts/activity.json (written by scripts/activity.py).
Run from the repo root:  python3 scripts/render.py [--light]"""
import io, json, math, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(io.open(os.path.join(ROOT, "scripts", "activity.json"), encoding="utf-8"))

MONO = "'JetBrains Mono','Cascadia Code','SF Mono','DejaVu Sans Mono',Menlo,Consolas,monospace"
FS, LH = 13, 21            # font size, line height
CW = FS * 0.6              # monospace advance, used to place rules, chips and the chart
PADX, PADY = 28, 26
W = 720
STATUS_H = 30
IND = 2                    # output indent, in columns
LBL = 13                   # shared label column, in columns

DARK = dict(bg="#0C0E12", border="#1F242C", fg="#C6CBD3", bright="#F1F3F6", dim="#5B6370",
            faint="#2A2F38", acc="#6FD48F", accbg="#16241C", status="#11141A", chip="#141920")
LIGHT = dict(bg="#FBFBF9", border="#DDDFDA", fg="#3A404A", bright="#111418", dim="#8B929C",
             faint="#E3E5E0", acc="#1E8A57", accbg="#E2F3E8", status="#F2F3EF", chip="#F1F2EE")
C = LIGHT if "--light" in sys.argv else DARK
OUT = "console-light.svg" if "--light" in sys.argv else "console.svg"

# ---------------------------------------------------------------- content
NAME, ROLE = "ahmed hameed", "software engineering by degree, marketer by trade"
LEDE = "i build things and i solve problems."
REPOS, PRIVATE = 40, 36
BUILT = [
    ("content-operations", "topical authority, cannibalisation, refresh"),
    ("headless-cms", "content modelling, preview, deploy pipeline"),
    ("vendor-review", "review queues, automated qa"),
    ("ai-editorial-review", "weighted rubric, findings anchored to text"),
    ("cro-dashboards", "ga4 and on-site conversion in one view"),
    ("rank-tracker", "1,000 keywords a run across 6 markets"),
    ("publishing-control", "24k pages, 6 content types, two-way sync"),
    ("review-crawlers", "3 sources, batched inside serverless caps"),
    ("multi-tenant-crm", "email and whatsapp outreach, lead scoring"),
    ("ai-search-visibility", "whether an llm mentions you, and where"),
]
ALSO = ["# also a workforce app with gps and payroll, two chrome",
        "# extensions, an electron qa tool. 36 of 40 repos are private.",
        "# ask and i will walk you through one."]
STACK = [
    ("range", ["next.js · react · vite · react native · expo",
               "electron · chrome mv3 · laravel · express · fastapi",
               "postgres · prisma · drizzle · convex · supabase · redis"]),
    ("reliability", ["idempotent, safe to re-run · retry with backoff",
                     "per-source rate budgets · circuit breakers",
                     "65 migrations, no downtime · vitest and playwright gates"]),
    ("ai layer", ["claude code · mcp · llm routing, model bakeoffs",
                  "semantic dedup at scale · prompt and eval harnesses",
                  "agent skill chains i wrote · n8n · make.com"]),
]
SDD = [   # (label, note, skills, animation): "once" fades in one by one, "loop" walks a highlight forever
    ("foundation", "runs once", ["init", "problem", "research", "requirements", "platform",
                                 "blueprint", "ux", "architecture", "structure", "roadmap"], "once"),
    ("delivery", "repeats", ["feature", "tasks", "build", "verify", "ship"], "loop"),
    ("any time", "", ["status", "decide", "change", "defect", "adopt"], None),
]
HYG = ["typed end to end", "secret scanning", "commit hooks", "dependency bots",
       "error tracking", "performance budgets", "a runbook per job"]

# ---------------------------------------------------------------- line model
lines = []
def L(*segs, size=FS, gap=0, indent=IND, **kw):
    """A text line: segments of (text, style). Styles: fg bright dim faint acc b name cursor."""
    d = dict(segs=[s if isinstance(s, tuple) else (s, "fg") for s in segs], size=size, gap=gap, indent=indent)
    d.update(kw); lines.append(d)
def blank(n=1):
    for _ in range(n): L()
def hdr(tool, rest=""):
    """Command line flush left, with a hairline running from the end of the text to the right edge."""
    L(("~ $ ", "dim"), (tool, "acc"), (rest, "bright"), indent=0, rule=True, gap=2)
def chips(label, note, items, anim=None):
    """Label in the shared column, then rounded chips; wraps onto more lines when the row is full."""
    full = W - 2 * PADX - (IND + LBL) * CW
    first = full - (len(note) * 11 * 0.6 + 24 if note else 0)   # the first row leaves room for the note
    rows, row, used = [], [], 0
    for it in items:
        w = len(it) * CW + 14
        avail = first if not rows else full
        if row and used + w > avail:
            rows.append(row); row, used = [], 0
        row.append(it); used += w + 8
    rows.append(row)
    k = 0
    for i, r in enumerate(rows):
        L((label if i == 0 else "", "bright"), chips=r, note=note if i == 0 else "", anim=anim, k0=k, n=len(items))
        k += len(r)

# whoami
hdr("whoami")
L((NAME, "name"), size=20, gap=6)
L(ROLE)
L(LEDE)
blank(2)

# stats: four cells, value over label
hdr("ahmed", " stats --since 12mo")
cells = [(f"{A['total']:,}", "commits"), (str(REPOS), f"repos · {PRIVATE} private"),
         (f"{A['longest']} days", "longest streak"), (f"{A['active']} / {A['ndays']}", "days active")]
CELL = 20
L(*[(v.ljust(CELL), "b") for v, _ in cells])
L(*[(l.ljust(CELL), "dim") for _, l in cells])
blank()
lines.append(dict(segs=[], size=FS, gap=0, indent=IND, chart=True))
L((f"# regenerated every 6h by a github action. last push {A.get('last', '')}.", "dim"))
blank(2)

# shipped: tree output
hdr("ahmed", " tree shipped")
L(("shipped/", "bright"))
for i, (n, d) in enumerate(BUILT):
    last = i == len(BUILT) - 1
    L(("└─ " if last else "├─ ", "dim"), (n.ljust(21), "bright"), (d, "fg"))
for a in ALSO: L(("   ", "fg"), (a, "dim"))
blank(2)

# stack: label rows on the shared label column
hdr("ahmed", " stack")
for i, (lab, rows) in enumerate(STACK):
    for j, r in enumerate(rows):
        L(((lab if j == 0 else "").ljust(LBL), "bright"), (r, "fg"))
    if i < len(STACK) - 1: blank()
blank(2)

# sdd: chips
hdr("sdd", " --list")
L(("spec-driven development · 20 skills", "dim"))
blank()
for lab, note, items, anim in SDD:
    chips(lab, note, items, anim)
blank(2)

# lint
hdr("ahmed", " lint --repo '*'")
for r in range(0, len(HYG), 3):
    segs = []
    for h in HYG[r:r + 3]:
        segs += [("✓ ", "acc"), (h.ljust(22), "fg")]
    L(*segs)
L((f"{REPOS} repos, 0 warnings", "dim"))
blank(2)

# empty prompt; contact links live in the README under the image
L(("~ $ ", "dim"), ("█", "cursor"), indent=0)

# ---------------------------------------------------------------- render
esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
FILL = dict(fg=C["fg"], bright=C["bright"], dim=C["dim"], faint=C["faint"], acc=C["acc"],
            b=C["bright"], name=C["bright"], cursor=C["acc"])
BOLD = {"b", "name"}
CHART_ROWS = 5

def chart(top, x0):
    """52 weekly bars on a square-root scale. Grows in once, then the current week pulses."""
    weeks = A["weeks"]; n = len(weeks); mx = max(weeks) or 1
    pitch = CW; bw = pitch - 2
    xb = x0 + 9 * CW                        # bars start after the "52w" gutter
    base = top + 4 * LH - 6
    hmax = 4 * LH - 14
    pi = weeks.index(mx)
    g = [f'<text x="{x0}" y="{top + FS}" font-family="{MONO}" font-size="{FS}" fill="{C["dim"]}">52w</text>',
         f'<circle cx="{x0 + 4.5 * CW:.1f}" cy="{top + FS - 4}" r="2.4" fill="{C["acc"]}">'
         f'<animate attributeName="opacity" values="1;1;0.15;0.15;1" keyTimes="0;0.45;0.5;0.95;1" dur="2s" repeatCount="indefinite"/></circle>',
         f'<text x="{x0 + 5.5 * CW:.1f}" y="{top + FS}" font-family="{MONO}" font-size="11" fill="{C["acc"]}">live</text>',
         f'<line x1="{xb:.1f}" y1="{base + 0.5}" x2="{xb + n * pitch:.1f}" y2="{base + 0.5}" stroke="{C["faint"]}"/>',
         f'<line x1="{xb:.1f}" y1="{base - hmax + 0.5}" x2="{xb + n * pitch:.1f}" y2="{base - hmax + 0.5}" stroke="{C["faint"]}" stroke-dasharray="2 4"/>',
         f'<text x="{xb + n * pitch + 2 * CW:.1f}" y="{base - hmax + 4}" xml:space="preserve" font-family="{MONO}" font-size="{FS}">'
         f'<tspan fill="{C["dim"]}">peak </tspan><tspan fill="{C["bright"]}" font-weight="700">{mx}</tspan><tspan fill="{C["dim"]}">/wk</tspan></text>',
         f'<text x="{xb + n * pitch + 2 * CW:.1f}" y="{base}" font-family="{MONO}" font-size="11" fill="{C["dim"]}">√ scale</text>']
    for i, w in enumerate(weeks):
        h = 0 if w == 0 else max(2, hmax * math.sqrt(w / mx))
        x = xb + i * pitch
        fill = C["acc"] if i == pi else (C["bright"] if i == n - 1 else C["fg"])
        op = "1" if i >= n - 1 or i == pi else "0.75"
        if h == 0:
            g.append(f'<rect x="{x:.1f}" y="{base - 1}" width="{bw:.1f}" height="1" fill="{C["faint"]}"/>')
            continue
        b = 0.15 + i * 0.018
        r = (f'<rect x="{x:.1f}" y="{base - h:.1f}" width="{bw:.1f}" height="{h:.1f}" fill="{fill}" opacity="{op}">'
             f'<animate attributeName="height" from="0" to="{h:.1f}" dur="0.45s" begin="{b:.2f}s" fill="freeze" calcMode="spline" keySplines="0.2 0.7 0.2 1"/>'
             f'<animate attributeName="y" from="{base}" to="{base - h:.1f}" dur="0.45s" begin="{b:.2f}s" fill="freeze" calcMode="spline" keySplines="0.2 0.7 0.2 1"/>')
        if i == n - 1:
            r += f'<animate attributeName="opacity" values="1;0.35;1" dur="1.6s" begin="{b + 0.5:.2f}s" repeatCount="indefinite"/>'
        g.append(r + '</rect>')
    for idx, name in A["months"]:
        if idx == 0 and len(A["months"]) > 1 and A["months"][1][0] < 3: continue
        g.append(f'<text x="{xb + idx * pitch:.1f}" y="{base + 15}" font-family="{MONO}" font-size="10" fill="{C["dim"]}">{name}</text>')
    return "".join(g)

def chip_row(y, x0, ln):
    """Label text, then rounded chips from x0 + LBL columns, then an optional dim note after them."""
    out = []
    label = ln["segs"][0][0] if ln["segs"] else ""
    if label:
        out.append(f'<text x="{x0}" y="{y}" font-family="{MONO}" font-size="{FS}" fill="{C["bright"]}">{esc(label)}</text>')
    x = x0 + LBL * CW
    anim, k, n = ln.get("anim"), ln.get("k0", 0), ln.get("n", 1)
    CYCLE = 1.3 * n                          # seconds for one walk of the loop
    for it in ln["chips"]:
        w = len(it) * CW + 14
        rect = f'<rect x="{x:.1f}" y="{y - FS - 1}" width="{w:.1f}" height="{FS + 7}" rx="3" fill="{C["chip"]}" stroke="{C["faint"]}"'
        text = f'<text x="{x + 7:.1f}" y="{y}" font-family="{MONO}" font-size="{FS - 1}" fill="{C["fg"]}"'
        if anim == "loop":
            a, b = k / n, (k + 1) / n
            kt = f'keyTimes="0;{a:.3f};{b:.3f};1" dur="{CYCLE}s" begin="1s" calcMode="discrete" repeatCount="indefinite"'
            rect += (f'><animate attributeName="stroke" values="{C["faint"]};{C["acc"]};{C["faint"]};{C["faint"]}" {kt}/>'
                     f'<animate attributeName="fill" values="{C["chip"]};{C["accbg"]};{C["chip"]};{C["chip"]}" {kt}/></rect>')
            text += f'><animate attributeName="fill" values="{C["fg"]};{C["acc"]};{C["fg"]};{C["fg"]}" {kt}/>{esc(it)}</text>'
            out.append(rect + text)
        elif anim == "once":
            rect += "/>"; text += f">{esc(it)}</text>"
            out.append(f'<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.35s" begin="{0.4 + k * 0.14:.2f}s" fill="freeze"/>{rect}{text}</g>')
        else:
            out.append(rect + "/>" + text + f">{esc(it)}</text>")
        x += w + 8; k += 1
    if ln.get("note"):
        out.append(f'<text x="{W - PADX}" y="{y}" text-anchor="end" font-family="{MONO}" font-size="11" fill="{C["dim"]}">{esc(ln["note"])}</text>')
    return "".join(out)

def render():
    y = PADY + FS + 2
    out = []
    for ln in lines:
        size = ln["size"]; x0 = PADX + ln["indent"] * CW
        if ln.get("chart"):
            out.append(chart(y - FS, x0)); y += CHART_ROWS * LH; continue
        if ln.get("chips"):
            out.append(chip_row(y, x0, ln)); y += LH + 4; continue
        if ln["segs"]:
            y += (size - FS)
            t = [f'<text x="{x0:.1f}" y="{y}" xml:space="preserve" font-family="{MONO}" font-size="{size}" fill="{C["fg"]}">']
            ncols = 0
            for s, st in ln["segs"]:
                if not s: continue
                ncols += len(s)
                attrs = f' fill="{FILL[st]}"'
                if st in BOLD: attrs += ' font-weight="700"'
                if st == "cursor":
                    attrs += '><animate attributeName="opacity" values="1;1;0;0" keyTimes="0;0.5;0.5;1" dur="1.2s" repeatCount="indefinite"/'
                t.append(f"<tspan{attrs}>{esc(s)}</tspan>")
            t.append("</text>")
            out.append("".join(t))
            if ln.get("rule"):
                rx = x0 + ncols * CW + 10
                out.append(f'<line x1="{rx:.1f}" y1="{y - 4.5}" x2="{W - PADX}" y2="{y - 4.5}" stroke="{C["faint"]}"/>')
        y += LH + ln["gap"]
    body_h = y - LH + PADY
    H = body_h + STATUS_H

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
             f"{PRIVATE} private, longest streak {A['longest']} days, peak week {A['peak']}. shipped: "
             + "; ".join(f"{n}, {d}" for n, d in BUILT) + ". "
             + " ".join(f"{t}: {' '.join(r)}." for t, r in STACK)
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
    io.open(os.path.join(ROOT, "assets", OUT), "w", encoding="utf-8", newline="\n").write(s)
    h = s.split('height="', 1)[1].split('"', 1)[0]
    print(f"{OUT}  {W}x{h}  {len(s.encode('utf-8')) // 1024} KB  {len(lines)} lines")
