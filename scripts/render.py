# -*- coding: utf-8 -*-
"""Draws assets/hero.svg and assets/body.svg for the profile README.
Stdlib only. Reads scripts/activity.json (written by scripts/activity.py) and scripts/figlet.json.
Every animation is SMIL. Every sequence resolves to a complete resting frame.
Run from the repo root:  python3 scripts/render.py"""
import io, json, os, random

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
A = json.load(io.open(os.path.join(ROOT, "scripts", "activity.json"), encoding="utf-8"))
FIG = json.load(io.open(os.path.join(ROOT, "scripts", "figlet.json"), encoding="utf-8"))
W = 860
esc = lambda s: str(s).replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
MONO = "'JetBrains Mono','Cascadia Code','SF Mono','DejaVu Sans Mono',Menlo,Consolas,monospace"
CW = 0.60
wide = lambda s, sz: len(s) * sz * CW
random.seed(11)  # fixed, so the file only changes when the data does

NAME, ROLE = "Ahmed Hameed", "software engineering by degree, marketer by trade"
LEDE = "I build things and I solve problems."
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
ALSO = "also a workforce app with gps and payroll, two chrome extensions, an electron qa tool"
COLS = [
    ("range", ["next.js · react · vite", "react native · expo", "electron · chrome mv3",
               "laravel · express · fastapi", "postgres · prisma · drizzle", "convex · supabase · redis"]),
    ("reliability", ["idempotent, safe to re-run", "retry with backoff", "per-source rate budgets",
                     "circuit breakers", "65 migrations, no downtime", "vitest and playwright gates"]),
    ("ai layer", ["claude code · mcp", "llm routing, model bakeoffs", "semantic dedup at scale",
                  "prompt and eval harnesses", "agent skill chains i wrote", "n8n · make.com"]),
]
SDD_ROWS = [
    ("foundation", "runs once", ["init", "problem", "research", "requirements", "platform",
                                 "blueprint", "ux", "architecture", "structure", "roadmap"], False),
    ("delivery", "repeats", ["feature", "tasks", "build", "verify", "ship"], True),
    ("any time", "", ["status", "decide", "change", "defect", "adopt"], False),
]
HYG = ["typed end to end", "secret scanning", "commit hooks", "dependency bots",
       "error tracking", "performance budgets", "a runbook per job"]
MAIL, LI = "ahmedsheikh2654@gmail.com", "in/ahmed-hameed"
LOG = ["[ok] n8n  route lead -> crm workspace", "[ok] make  refresh rank sheet, 6 markets",
       "[ok] crawl 3 sources, batch 7 of 12", "[ok] spec  gate passed, task open",
       "[ok] build agents, 4 files touched", "[ok] ship  smoke check alive"]

P = dict(bg="#070B14", bg2="#0B1220", rule="#1B2536", ink="#E6F0FA", val="#94A6BD", key="#8FD3FF",
         mut="#7C8CA3", dim="#4F5D74", acc="#22D3EE", acc2="#A78BFA", ok="#34D399", num="#FBBF24",
         dot="#22324A")

LABEL_HERO = (f"{NAME}. {ROLE}. {LEDE} {A['total']} commits in the last twelve months across {REPOS} "
              f"repositories, {PRIVATE} private. Longest streak {A['longest']} days, peak week {A['peak']}. "
              "Spec-driven delivery loop: feature, tasks, build, verify, ship.")
LABEL_BODY = ("Shipped: " + "; ".join(f"{n}, {d}, {c} commits" for n, d, c in BUILT) + f". {ALSO}. "
              + ". ".join(f"{t}: {', '.join(i)}" for t, i in COLS)
              + ". SDD, spec-driven development, twenty skills: "
              + "; ".join(f"{g} {s}: {', '.join(k)}" for g, s, k, _ in SDD_ROWS)
              + ". In every repo: " + ", ".join(HYG) + f". Contact {MAIL}.")

UID = [0]
def uid(p="u"):
    UID[0] += 1
    return f"{p}{UID[0]}"

def T(x, y, s, fill, size=11.5, w=None, anchor=None, op=None, ls=None, extra=""):
    a = f'<text x="{x}" y="{y}" fill="{fill}" font-family="{MONO}" font-size="{size}"'
    if w: a += f' font-weight="{w}"'
    if anchor: a += f' text-anchor="{anchor}"'
    if op is not None: a += f' opacity="{op}"'
    if ls: a += f' letter-spacing="{ls}"'
    if extra: a += " " + extra
    return a + f">{esc(s)}</text>"

def fade(body, begin, dur=0.4, dy=0):
    tr = (f'<animateTransform attributeName="transform" type="translate" values="0 {dy};0 0" dur="{dur}s" '
          f'begin="{begin:.2f}s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>') if dy else ""
    return (f'<g opacity="1"><animate attributeName="opacity" values="0;0;1" keyTimes="0;0.01;1" dur="{dur}s" '
            f'begin="{begin:.2f}s" fill="freeze"/>{tr}{body}</g>')

def count_up(x, y, final, fill, size, begin, dur=1.2, steps=26, **kw):
    vals = [round(final * (i + 1) / steps) for i in range(steps)]; vals[-1] = final
    step = dur / steps; out = []
    for i, v in enumerate(vals):
        s = f"{v:,}"; b0 = begin + i * step
        if i == steps - 1:
            out.append(f'<g opacity="1"><set attributeName="opacity" to="0" begin="0s"/>'
                       f'<set attributeName="opacity" to="1" begin="{b0:.3f}s"/>{T(x, y, s, fill, size, **kw)}</g>')
        else:
            out.append(f'<g opacity="0"><set attributeName="opacity" to="1" begin="{b0:.3f}s"/>'
                       f'<set attributeName="opacity" to="0" begin="{b0+step:.3f}s"/>{T(x, y, s, fill, size, **kw)}</g>')
    return "".join(out)

def figlet(word, x, y, cw, ch, fill, begin=None, per=0.008):
    out, rows = [], FIG[word]
    for r, row in enumerate(rows):
        c = 0
        while c < len(row):
            if row[c] == "#":
                s = c
                while c < len(row) and row[c] == "#": c += 1
                rect = f'<rect x="{x+s*cw:.1f}" y="{y+r*ch:.1f}" width="{(c-s)*cw:.1f}" height="{ch}" fill="{fill}"'
                if begin is not None:
                    rect += (f'><animate attributeName="opacity" values="0;0;1" keyTimes="0;0.01;1" dur="0.3s" '
                             f'begin="{begin + s*per:.3f}s" fill="freeze"/></rect>')
                else: rect += "/>"
                out.append(rect)
            else: c += 1
    return "".join(out), len(rows) * ch, max(len(r) for r in rows) * cw

def mini_bars(x0, y0, width, h, col, begin, ratio=0.6, stagger=0.012):
    n = len(A["weeks"]); mx = max(A["weeks"]) or 1
    pitch = width / n; bw = max(2, pitch * ratio); out = []
    for i, v in enumerate(A["weeks"]):
        f = v / mx; bh = max(1.5, round(f * h, 1)); x = x0 + i * pitch
        b = round(begin + i * stagger, 3)
        out.append(f'<rect x="{x:.1f}" y="{y0+h-bh:.1f}" width="{bw:.1f}" height="{bh}" fill="{col}" fill-opacity="{0.30+0.70*f:.2f}">'
                   f'<animate attributeName="height" values="0;{bh}" dur="0.5s" begin="{b}s" fill="freeze" calcMode="spline" keySplines="0.16 0.9 0.2 1"/>'
                   f'<animate attributeName="y" values="{y0+h};{y0+h-bh:.1f}" dur="0.5s" begin="{b}s" fill="freeze" calcMode="spline" keySplines="0.16 0.9 0.2 1"/></rect>')
    return "".join(out)

# ------------------------------------------------------------------ scene parts
def defs_common(pre, floor_top=292, floor_bottom=470):
    return (
        f'<filter id="{pre}glow" x="-20%" y="-40%" width="140%" height="180%">'
        f'<feGaussianBlur stdDeviation="2.2" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        f'<filter id="{pre}bloom" x="-30%" y="-60%" width="160%" height="220%">'
        f'<feGaussianBlur stdDeviation="6" result="b"/><feMerge><feMergeNode in="b"/><feMergeNode in="b"/><feMergeNode in="SourceGraphic"/></feMerge></filter>'
        f'<pattern id="{pre}grain" width="3" height="3" patternUnits="userSpaceOnUse"><rect width="3" height="1" fill="#000" fill-opacity="0.18"/></pattern>'
        f'<pattern id="{pre}scan" width="4" height="4" patternUnits="userSpaceOnUse"><rect width="4" height="1" fill="{P["acc"]}" fill-opacity="0.08"/></pattern>'
        f'<radialGradient id="{pre}vig" cx="50%" cy="45%" r="70%"><stop offset="55%" stop-color="{P["bg"]}" stop-opacity="0"/><stop offset="100%" stop-color="{P["bg"]}" stop-opacity="0.85"/></radialGradient>'
        f'<radialGradient id="{pre}halo" cx="50%" cy="50%" r="50%"><stop offset="0%" stop-color="{P["acc"]}" stop-opacity="0.22"/><stop offset="100%" stop-color="{P["acc"]}" stop-opacity="0"/></radialGradient>'
        f'<linearGradient id="{pre}sweep" x1="0" y1="0" x2="1" y2="0"><stop offset="0%" stop-color="{P["acc"]}" stop-opacity="0"/><stop offset="50%" stop-color="{P["acc"]}" stop-opacity="0.10"/><stop offset="100%" stop-color="{P["acc"]}" stop-opacity="0"/></linearGradient>'
        f'<linearGradient id="{pre}floor" gradientUnits="userSpaceOnUse" x1="0" y1="{floor_top}" x2="0" y2="{floor_bottom}"><stop offset="0%" stop-color="{P["acc"]}" stop-opacity="0"/><stop offset="100%" stop-color="{P["acc"]}" stop-opacity="0.34"/></linearGradient>'
        f'<linearGradient id="{pre}sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0%" stop-color="#05070E"/><stop offset="100%" stop-color="{P["bg2"]}"/></linearGradient>'
    )

def particles(n, w, h, strength=1.0):
    out = []
    for _ in range(n):
        x, y = random.uniform(10, w - 10), random.uniform(10, h - 10)
        r = random.uniform(0.6, 1.5); rise = random.uniform(16, 40); d = random.uniform(14, 28)
        tw = random.uniform(2.2, 5.5); o0 = random.uniform(0.25, 0.8) * strength
        out.append(f'<circle cx="{x:.1f}" cy="{y:.1f}" r="{r:.1f}" fill="{P["acc"]}" opacity="{o0:.2f}">'
                   f'<animateTransform attributeName="transform" type="translate" values="0 0;0 {-rise:.0f}" dur="{d:.1f}s" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="{o0:.2f};{o0*0.3:.2f};{o0:.2f}" dur="{tw:.1f}s" repeatCount="indefinite"/></circle>')
    return "".join(out)

def floor_grid(pre, vpx=430, hy=292, bottom=470, cycle=6.0, nlines=10):
    out = [f'<line x1="{vpx}" y1="{hy}" x2="{xb}" y2="{bottom}" stroke="url(#{pre}floor)" stroke-width="1"/>'
           for xb in range(-260, W + 261, 86)]
    samples = 14
    ts = [i / (samples - 1) for i in range(samples)]
    ys = [hy + (bottom - hy) * (t ** 2.4) for t in ts]
    halfw = [((y - hy) / (bottom - hy)) * 700 for y in ys]
    ops = [0.38 * (t ** 1.4) for t in ts]
    kt = ";".join(f"{t:.3f}" for t in ts)
    for i in range(nlines):
        ph = i / nlines; idx = int(ph * (samples - 1)); b = f"{-ph*cycle:.2f}s"
        out.append(f'<line x1="{vpx-halfw[idx]:.0f}" y1="{ys[idx]:.1f}" x2="{vpx+halfw[idx]:.0f}" y2="{ys[idx]:.1f}" stroke="{P["acc"]}" stroke-width="1" opacity="{ops[idx]:.2f}">'
                   f'<animate attributeName="y1" values="{";".join(f"{y:.1f}" for y in ys)}" keyTimes="{kt}" dur="{cycle}s" begin="{b}" repeatCount="indefinite"/>'
                   f'<animate attributeName="y2" values="{";".join(f"{y:.1f}" for y in ys)}" keyTimes="{kt}" dur="{cycle}s" begin="{b}" repeatCount="indefinite"/>'
                   f'<animate attributeName="x1" values="{";".join(f"{vpx-h:.0f}" for h in halfw)}" keyTimes="{kt}" dur="{cycle}s" begin="{b}" repeatCount="indefinite"/>'
                   f'<animate attributeName="x2" values="{";".join(f"{vpx+h:.0f}" for h in halfw)}" keyTimes="{kt}" dur="{cycle}s" begin="{b}" repeatCount="indefinite"/>'
                   f'<animate attributeName="opacity" values="{";".join(f"{o:.2f}" for o in ops)}" keyTimes="{kt}" dur="{cycle}s" begin="{b}" repeatCount="indefinite"/></line>')
    out.append(f'<line x1="0" y1="{hy}" x2="{W}" y2="{hy}" stroke="{P["acc"]}" stroke-width="1" opacity="0.35"/>')
    return "".join(out)

def holo_frame(pre, x, y, w, h, tilt_deg, bob_dur, bob_phase, inner, bob=True):
    cx, cy = x + w / 2, y + h / 2
    tf = f'translate({cx:.1f} {cy:.1f}) skewY({tilt_deg}) translate({-cx:.1f} {-cy:.1f})' if tilt_deg else ""
    L = 12
    corners = "".join(
        f'<path d="{d}" fill="none" stroke="{P["acc"]}" stroke-width="1.6" stroke-linecap="round"/>'
        for d in (f"M{x} {y+L} V{y} H{x+L}", f"M{x+w-L} {y} H{x+w} V{y+L}",
                  f"M{x+w} {y+h-L} V{y+h} H{x+w-L}", f"M{x+L} {y+h} H{x} V{y+h-L}"))
    bobanim = (f'<animateTransform attributeName="transform" type="translate" additive="sum" values="0 0;0 -5;0 0" '
               f'dur="{bob_dur}s" begin="{-bob_phase}s" repeatCount="indefinite" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>') if bob else ""
    return (f'<g transform="{tf}">{bobanim}'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="{P["acc"]}" fill-opacity="0.045" stroke="{P["acc"]}" stroke-opacity="0.32" stroke-width="1"/>'
            f'<rect x="{x}" y="{y}" width="{w}" height="{h}" rx="3" fill="url(#{pre}scan)"/>'
            f'<g filter="url(#{pre}glow)">{corners}</g>{inner}</g>')

def connector(pre, x1, y1, x2, y2, begin, dur=2.6):
    pid = uid(pre + "p")
    return (f'<path id="{pid}" d="M{x1} {y1} L{x2} {y2}" fill="none" stroke="{P["acc"]}" stroke-opacity="0.22" stroke-width="1" stroke-dasharray="2 5"/>'
            f'<circle r="2.4" fill="{P["acc"]}" filter="url(#{pre}glow)" opacity="0">'
            f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.1;0.9;1" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/>'
            f'<animateMotion dur="{dur}s" begin="{begin}s" repeatCount="indefinite"><mpath xlink:href="#{pid}"/></animateMotion></circle>')

def light_sweep(pre, h, dur=7.5, begin=1.0):
    return (f'<g transform="rotate(-18 430 {h/2:.0f})"><rect x="-420" y="-300" width="260" height="{h+600}" fill="url(#{pre}sweep)">'
            f'<animateTransform attributeName="transform" type="translate" values="0 0;1500 0" dur="{dur}s" begin="{begin}s" repeatCount="indefinite"/></rect></g>')

def ticker(x, y, lines, size=9.5, each=1.7):
    cyc = each * len(lines); out = []
    for i, ln in enumerate(lines):
        t0 = i / len(lines); t1 = (i + 1) / len(lines)
        kt = f"0;{max(0,t0-0.001):.3f};{t0+0.02:.3f};{t1-0.02:.3f};{min(1,t1+0.001):.3f};1"
        out.append(f'<g opacity="{1 if i == 0 else 0}"><animate attributeName="opacity" values="0;0;1;1;0;0" keyTimes="{kt}" dur="{cyc}s" begin="0.8s" repeatCount="indefinite"/>'
                   f'{T(x, y, ln, P["ok"] if ln.startswith("[ok]") else P["val"], size)}</g>')
    return "".join(out)

def sdd_loop(x, y, begin, size=10):
    keys = SDD_ROWS[1][2]; out = []; cx = x; cyc = len(keys) * 0.42
    for i, k in enumerate(keys):
        wg = wide(k, size) + 10
        t0, t1 = i * 0.42 / cyc, (i * 0.42 + 0.42) / cyc
        kt = f"0;{max(0,t0-0.001):.3f};{t0:.3f};{t1:.3f};{min(1,t1+0.001):.3f};1"
        out.append(f'<rect x="{cx:.0f}" y="{y-11}" width="{wg:.0f}" height="16" rx="2" fill="{P["acc"]}" fill-opacity="0.14">'
                   f'<animate attributeName="fill-opacity" values="0.14;0.14;0.6;0.6;0.14;0.14" keyTimes="{kt}" dur="{cyc:.2f}s" begin="{begin}s" repeatCount="indefinite"/></rect>')
        out.append(T(cx + 5, y, k, P["ink"], size)); cx += wg + 4
    out.append(T(cx + 3, y, "↺", P["acc"], 12))
    return "".join(out), cx + 16

def camera(inner, amp, dur=16.0, cx=430, cy=235):
    return (f'<g transform="translate({cx} {cy})"><g>'
            f'<animateTransform attributeName="transform" type="scale" values="1;{amp};1" dur="{dur}s" repeatCount="indefinite" calcMode="spline" keySplines="0.42 0 0.58 1;0.42 0 0.58 1"/>'
            f'<g transform="translate({-cx} {-cy})">{inner}</g></g></g>')

def wrap(h, body, label, pre, floor=(292, 470)):
    return (f'<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="{W}" height="{h}" '
            f'viewBox="0 0 {W} {h}" role="img" aria-label="{esc(label)}"><defs>{defs_common(pre, *floor)}</defs>'
            f'<rect width="{W}" height="{h}" fill="url(#{pre}sky)"/>{body}</svg>\n')

# =====================================================================
# HERO  ·  console
# =====================================================================
def hero():
    pre = "a"; H = 470
    back = particles(46, W, 300) + floor_grid(pre)
    fg = []
    fg.append(f'<ellipse cx="430" cy="150" rx="250" ry="86" fill="url(#{pre}halo)"><animate attributeName="opacity" values="0.8;1;0.8" dur="5s" repeatCount="indefinite"/></ellipse>')
    cw, ch = 7.6, 12.6
    aw = 42 * cw; ax = 430 - aw / 2; ay = 108
    art, ah, _ = figlet("AHMED", ax, ay, cw, ch, P["acc"], begin=0.4, per=0.012)
    fg.append(f'<g filter="url(#{pre}bloom)">{art}</g>')
    fg.append(f'<rect x="{ax-6:.0f}" y="{ay-6}" width="{aw+12:.0f}" height="{ah+12}" fill="{P["bg"]}" opacity="0">'
              f'<animate attributeName="opacity" values="0;0;0.35;0;0;0;0.2;0;0" keyTimes="0;0.31;0.32;0.33;0.6;0.79;0.80;0.81;1" dur="7s" begin="1.5s" repeatCount="indefinite"/></rect>')
    fg.append(fade(T(430, ay + ah + 32, "HAMEED", P["ink"], 22, "700", "middle", ls="6"), 1.1))
    fg.append(fade(T(430, ay + ah + 52, ROLE, P["mut"], 10.5, anchor="middle"), 1.3))
    # left: activity
    lp = (T(50, 168, "activity", P["key"], 10, "700", ls="1.5") + T(234, 168, "52w", P["dim"], 9, anchor="end")
          + mini_bars(50, 178, 184, 70, P["acc"], 1.4)
          + f'<line x1="50" y1="248" x2="234" y2="248" stroke="{P["acc"]}" stroke-opacity="0.35"/>'
          + T(50, 262, f"peak {A['peak']}", P["mut"], 9) + T(234, 262, A["busiest"], P["mut"], 9, anchor="end")
          + T(50, 278, f"active {A['active']} of {A['ndays']} days", P["dim"], 9))
    fg.append(holo_frame(pre, 36, 150, 212, 144, -5, 5.6, 0.0, lp))
    # right: metrics
    rp = (T(628, 168, "metrics", P["key"], 10, "700", ls="1.5")
          + count_up(628, 204, A["total"], P["num"], 30, 1.6, 1.3, 26, w="700")
          + T(628, 220, "commits, last 12 months", P["mut"], 9)
          + T(628, 246, str(REPOS), P["ink"], 16, "700") + T(654, 246, f"repositories, {PRIVATE} private", P["mut"], 9)
          + T(628, 268, str(A["longest"]), P["ink"], 16, "700") + T(654, 268, "day longest streak", P["mut"], 9)
          + T(628, 284, "●", P["ok"], 8) + T(640, 284, "building, always", P["ok"], 9))
    fg.append(holo_frame(pre, 612, 150, 212, 144, 5, 6.3, 2.1, rp))
    # bottom left: log
    bl = (T(50, 340, "log", P["key"], 10, "700", ls="1.5") + ticker(50, 360, LOG, 9.2)
          + T(50, 382, "// automation running", P["dim"], 8.5))
    fg.append(holo_frame(pre, 36, 322, 240, 74, -3, 7.1, 1.0, bl))
    # bottom right: stack
    br = (T(598, 340, "stack", P["key"], 10, "700", ls="1.5")
          + T(598, 358, "next.js · react · python · fastapi", P["val"], 9.2)
          + T(598, 372, "postgres · prisma · redis · supabase", P["val"], 9.2)
          + T(598, 386, "claude code · mcp · n8n · make.com", P["val"], 9.2))
    fg.append(holo_frame(pre, 584, 322, 240, 74, 3, 6.7, 3.4, br))
    # centre: the delivery loop
    fg.append(fade(T(430, 318, "spec-driven delivery loop", P["mut"], 9, anchor="middle", ls="1.5"), 1.8))
    loop, lw = sdd_loop(0, 0, 2.2, 10)
    fg.append(f'<g transform="translate({430 - lw/2:.0f} 344)">{loop}</g>')
    fg.append(fade(T(430, 380, LEDE, P["ink"], 12, anchor="middle"), 2.4))
    # connectors
    fg.append(connector(pre, 248, 200, ax + 8, ay + ah + 2, 1.9))
    fg.append(connector(pre, 612, 200, ax + aw - 8, ay + ah + 2, 3.1))
    fg.append(connector(pre, 276, 356, 430 - lw / 2 - 6, 341, 2.5))
    fg.append(connector(pre, 584, 356, 430 + lw / 2 + 2, 341, 3.8))
    body = (camera(back, 1.02) + camera("".join(fg), 1.05) + light_sweep(pre, H)
            + f'<rect width="{W}" height="{H}" fill="url(#{pre}vig)"/>'
            + f'<rect width="{W}" height="{H}" fill="url(#{pre}grain)" opacity="0.6"/>'
            + T(22, 20, "itsahmeds / README.md", P["dim"], 10) + T(W - 22, 20, "live", P["ok"], 10, anchor="end")
            + f'<circle cx="{W-52}" cy="16" r="3" fill="{P["ok"]}"><animate attributeName="opacity" values="1;0.2;1" dur="2.2s" repeatCount="indefinite"/></circle>')
    return wrap(H, body, LABEL_HERO, pre)

# =====================================================================
# BODY  ·  the same world, in panels, on a spine
# =====================================================================
def leader_row(x, y, right, key, mid, val, begin, size=11, count=False):
    o = [T(x, y, key, P["ink"], size), T(x + wide(key, size) + 10, y, mid, P["val"], size)]
    cur = x + wide(key, size) + 10 + wide(mid, size)
    x1, x2 = cur + 9, right - wide(str(val), size) - 9
    if x2 > x1:
        o.append(f'<line x1="{x1:.0f}" y1="{y-3.5}" x2="{x2:.0f}" y2="{y-3.5}" stroke="{P["dot"]}" stroke-width="1.6" stroke-linecap="round" stroke-dasharray="0.1 5">'
                 f'<animate attributeName="x2" values="{x1:.0f};{x2:.0f}" dur="0.35s" begin="{begin:.2f}s" fill="freeze"/></line>')
    if count:
        o.append(count_up(right, y, int(val), P["num"], size, begin + 0.1, 0.7, 12, anchor="end"))
    else:
        o.append(T(right, y, str(val), P["num"], size, anchor="end"))
    return "".join(o)

def section_title(pre, x, y, right, label, tag, begin):
    o = [f'<g filter="url(#{pre}glow)">{T(x, y, label, P["ink"], 15, "700", ls="1")}</g>']
    x1 = x + wide(label, 15) + 14; x2 = right - (wide(tag, 9.5) + 12 if tag else 0)
    o.append(f'<line x1="{x1:.0f}" y1="{y-5}" x2="{x2:.0f}" y2="{y-5}" stroke="{P["acc"]}" stroke-opacity="0.3">'
             f'<animate attributeName="x2" values="{x1:.0f};{x2:.0f}" dur="0.6s" begin="{begin:.2f}s" fill="freeze"/></line>')
    if tag: o.append(T(right, y - 1, tag, P["dim"], 9.5, anchor="end"))
    return "".join(o)

def spine_node(pre, y, begin):
    return (f'<g filter="url(#{pre}glow)"><circle cx="22" cy="{y}" r="4" fill="{P["bg"]}" stroke="{P["acc"]}" stroke-width="1.5">'
            f'<animate attributeName="r" values="0;4" dur="0.3s" begin="{begin:.2f}s" fill="freeze"/></circle></g>')

def sdd_rows(x, y, begin):
    o = []
    for r, (g, note, keys, loops) in enumerate(SDD_ROWS):
        ry = y + r * 30
        o.append(T(x, ry, g, P["key"], 11) + (T(x + 72, ry, note, P["dim"], 9.5) if note else ""))
        cx = x + 134; cyc = len(keys) * 0.42
        for i, k in enumerate(keys):
            wg = wide(k, 10.5) + 11
            rect = f'<rect x="{cx:.0f}" y="{ry-12}" width="{wg:.0f}" height="18" rx="2" fill="{P["acc"] if loops else P["acc2"]}" fill-opacity="0.14"'
            if loops:
                t0, t1 = i * 0.42 / cyc, (i * 0.42 + 0.42) / cyc
                kt = f"0;{max(0,t0-0.001):.3f};{t0:.3f};{t1:.3f};{min(1,t1+0.001):.3f};1"
                rect += f'><animate attributeName="fill-opacity" values="0.14;0.14;0.55;0.55;0.14;0.14" keyTimes="{kt}" dur="{cyc:.2f}s" begin="{begin+1:.2f}s" repeatCount="indefinite"/></rect>'
            else:
                rect += f'><animate attributeName="fill-opacity" values="0;0.14" dur="0.26s" begin="{begin + r*0.18 + i*0.07:.2f}s" fill="freeze"/></rect>'
            o.append(rect); o.append(T(cx + 5.5, ry, k, P["ink"], 10.5)); cx += wg + 4
        if loops: o.append(T(cx + 4, ry, "↺", P["acc"], 13))
    return "".join(o), y + len(SDD_ROWS) * 30

def body():
    pre = "c"; M, R = 44, W - 30; IN = 16   # panel inner padding
    fg, y, t = [], 40, 0.2
    nodes = []

    # shipped
    ph = 40 + len(BUILT) * 20 + 40
    inner = [section_title(pre, M + IN, y + 26, R - IN, "shipped", f"{PRIVATE} of {REPOS} repositories private", t)]
    ry = y + 52; tt = t + 0.2
    for n, d, c in BUILT:
        inner.append(fade(leader_row(M + IN, ry, R - IN, n, d, c, tt, 11, count=True), tt)); ry += 20; tt += 0.07
    inner.append(fade(T(M + IN, ry + 6, "// " + ALSO, P["dim"], 9.5), tt))
    fg.append(fade(holo_frame(pre, M, y, R - M, ph, 0, 0, 0, "".join(inner), bob=False), t, dy=8))
    nodes.append((y + 22, t)); y += ph + 22; t = tt + 0.2

    # stack: three panels
    cw3 = (R - M - 24) / 3; ph = 40 + 6 * 17 + 22
    for i, (ti, items) in enumerate(COLS):
        px = M + i * (cw3 + 12)
        inner = [f'<g filter="url(#{pre}glow)">{T(px + IN, y + 26, ti, P["key"], 12, "700", ls="1.5")}</g>']
        for k, it in enumerate(items): inner.append(T(px + IN, y + 50 + k * 17, it, P["val"], 10.3))
        fg.append(fade(holo_frame(pre, px, y, cw3, ph, 0, 0, 0, "".join(inner), bob=False), t + i * 0.12, dy=8))
    nodes.append((y + 22, t)); y += ph + 22; t += 0.5

    # sdd
    ph = 40 + 3 * 30 + 26
    blk, _ = sdd_rows(M + IN, y + 58, t + 0.2)
    inner = section_title(pre, M + IN, y + 26, R - IN, "sdd", "spec-driven development · 20 skills", t) + blk
    fg.append(fade(holo_frame(pre, M, y, R - M, ph, 0, 0, 0, inner, bob=False), t, dy=8))
    nodes.append((y + 22, t)); y += ph + 22; t += 1.2

    # every repo: bracket chips
    chips = []; cx = M; cy = y + 8
    for h_ in HYG:
        wg = wide(h_, 10) + 18
        if cx + wg > R: cx = M; cy += 30
        chips.append(f'<rect x="{cx:.0f}" y="{cy}" width="{wg:.0f}" height="22" rx="2" fill="{P["acc"]}" fill-opacity="0.05" stroke="{P["acc"]}" stroke-opacity="0.35"/>'
                     f'<path d="M{cx:.0f} {cy+6} V{cy} H{cx+6:.0f} M{cx+wg-6:.0f} {cy+22} H{cx+wg:.0f} V{cy+16}" fill="none" stroke="{P["acc"]}" stroke-width="1.4"/>'
                     + T(cx + 9, cy + 15, h_, P["val"], 10))
        cx += wg + 8
    fg.append(fade(T(M, y - 2, "in every repo", P["dim"], 9.5, ls="1.5") + "".join(chips), t))
    nodes.append((y - 6, t)); y = cy + 22 + 26; t += 0.25

    # contact
    fg.append(f'<line x1="{M}" y1="{y}" x2="{R}" y2="{y}" stroke="{P["rule"]}"/>'); y += 26
    fg.append(fade(T(M, y, "email", P["key"], 11.5) + T(R, y, MAIL, P["ink"], 11.5, anchor="end")
                   + f'<line x1="{M+44}" y1="{y-3.5}" x2="{R-wide(MAIL,11.5)-9:.0f}" y2="{y-3.5}" stroke="{P["dot"]}" stroke-width="1.6" stroke-linecap="round" stroke-dasharray="0.1 5"/>', t)); y += 19
    fg.append(fade(T(M, y, "linkedin", P["key"], 11.5) + T(R, y, LI, P["ink"], 11.5, anchor="end")
                   + f'<line x1="{M+66}" y1="{y-3.5}" x2="{R-wide(LI,11.5)-9:.0f}" y2="{y-3.5}" stroke="{P["dot"]}" stroke-width="1.6" stroke-linecap="round" stroke-dasharray="0.1 5"/>', t + 0.1)); y += 28
    fg.append(fade(T(M, y, "// a spec before anything gets built, agents do most of the typing,", P["dim"], 10)
                   + T(M, y + 15, "// n8n and make run whatever has to keep running afterwards.", P["dim"], 10), t + 0.2)); y += 22
    fg.append(f'<rect x="{M}" y="{y-1}" width="8" height="13" fill="{P["acc"]}"><animate attributeName="opacity" values="1;1;0;0" dur="1.1s" repeatCount="indefinite"/></rect>')
    H = y + 30

    # spine with travelling pulses, drawn under the panels
    spine = [f'<line x1="22" y1="30" x2="22" y2="{H-30}" stroke="{P["acc"]}" stroke-opacity="0.22" stroke-width="1" stroke-dasharray="2 5"/>']
    for k in range(2):
        spine.append(f'<circle cx="22" r="2.6" fill="{P["acc"]}" filter="url(#{pre}glow)" opacity="0">'
                     f'<animate attributeName="opacity" values="0;1;1;0" keyTimes="0;0.06;0.94;1" dur="6s" begin="{1+k*3}s" repeatCount="indefinite"/>'
                     f'<animate attributeName="cy" values="30;{H-30}" dur="6s" begin="{1+k*3}s" repeatCount="indefinite"/></circle>')
    for ny, nb in nodes: spine.append(spine_node(pre, ny, nb))

    out = (particles(30, W, H, 0.6) + "".join(spine) + "".join(fg) + light_sweep(pre, H, 11, 2)
           + f'<rect width="{W}" height="{H}" fill="url(#{pre}grain)" opacity="0.5"/>')
    return wrap(H, out, LABEL_BODY, pre, floor=(H, H + 1))

if __name__ == "__main__":
    os.makedirs(os.path.join(ROOT, "assets"), exist_ok=True)
    for name, fn in (("hero", hero), ("body", body)):
        s = fn()
        io.open(os.path.join(ROOT, "assets", f"{name}.svg"), "w", encoding="utf-8", newline="\n").write(s)
        h = s.split('height="', 1)[1].split('"', 1)[0]
        print(f"{name}.svg  860x{h}  {len(s)//1024} KB")
