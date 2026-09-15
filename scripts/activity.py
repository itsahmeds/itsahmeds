# -*- coding: utf-8 -*-
"""Turns the raw GraphQL contributions response into scripts/activity.json.
Stdlib only. Usage:  python3 scripts/activity.py scripts/raw.json"""
import io, json, os, sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
src = sys.argv[1] if len(sys.argv) > 1 else os.path.join(ROOT, "scripts", "raw.json")
d = json.load(io.open(src, encoding="utf-8"))
cal = d["data"]["user"]["contributionsCollection"]["contributionCalendar"]

days = [x for w in cal["weeks"] for x in w["contributionDays"]]
w52 = cal["weeks"][-52:]
weeks = [sum(x["contributionCount"] for x in w["contributionDays"]) for w in w52]
MN = ["jan", "feb", "mar", "apr", "may", "jun", "jul", "aug", "sep", "oct", "nov", "dec"]
months, prev = [], None
for i, w in enumerate(w52):
    m = w["contributionDays"][0]["date"][5:7]
    if m != prev:
        months.append([i, MN[int(m) - 1]]); prev = m
longest = run = 0
for x in days:
    run = run + 1 if x["contributionCount"] > 0 else 0
    longest = max(longest, run)
bywd = [0] * 7
for x in days:
    bywd[x["weekday"]] += x["contributionCount"]
pi = weeks.index(max(weeks))
out = {
    "total": cal["totalContributions"], "weeks": weeks, "months": months,
    "last30": sum(x["contributionCount"] for x in days[-30:]),
    "longest": longest,
    "busiest": ["sun", "mon", "tue", "wed", "thu", "fri", "sat"][bywd.index(max(bywd))],
    "active": sum(1 for x in days if x["contributionCount"] > 0), "ndays": len(days),
    "peak": max(weeks), "peakIdx": pi,
    "peakMonth": MN[int(w52[pi]["contributionDays"][0]["date"][5:7]) - 1],
}
json.dump(out, io.open(os.path.join(ROOT, "scripts", "activity.json"), "w", encoding="utf-8"), indent=0)
print(f"activity.json: total={out['total']} last30={out['last30']} longest={out['longest']} peak={out['peak']}")
