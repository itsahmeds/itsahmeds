// Regenerates assets/activity.svg from the GitHub contributions API.
// Zero dependencies. Run: GITHUB_TOKEN=... node scripts/build.mjs
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";

const LOGIN = "itsahmeds";
const TOKEN = process.env.GITHUB_TOKEN;
if (!TOKEN) throw new Error("GITHUB_TOKEN missing");

const query = `{
  user(login: "${LOGIN}") {
    createdAt
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { contributionDays { date contributionCount weekday } }
      }
    }
  }
}`;

const res = await fetch("https://api.github.com/graphql", {
  method: "POST",
  headers: { Authorization: `bearer ${TOKEN}`, "Content-Type": "application/json", "User-Agent": LOGIN },
  body: JSON.stringify({ query }),
});
const json = await res.json();
if (json.errors) throw new Error(JSON.stringify(json.errors));
const cal = json.data.user.contributionsCollection.contributionCalendar;

// ---------- numbers ----------
const days = cal.weeks.flatMap((w) => w.contributionDays);
const total = cal.totalContributions;
const weeks = cal.weeks.slice(-52).map((w) => w.contributionDays.reduce((a, d) => a + d.contributionCount, 0));
const thisWeek = weeks[weeks.length - 1];
const last30 = days.slice(-30).reduce((a, d) => a + d.contributionCount, 0);

let current = 0;
for (let i = days.length - 1; i >= 0; i--) {
  if (days[i].contributionCount > 0) current++;
  else if (i === days.length - 1) continue; // today can still be empty
  else break;
}
let longest = 0, run = 0;
for (const d of days) { run = d.contributionCount > 0 ? run + 1 : 0; longest = Math.max(longest, run); }

const byWeekday = [0, 0, 0, 0, 0, 0, 0];
for (const d of days) byWeekday[d.weekday] += d.contributionCount;
const busiest = ["sun", "mon", "tue", "wed", "thu", "fri", "sat"][byWeekday.indexOf(Math.max(...byWeekday))];
const activeDays = days.filter((d) => d.contributionCount > 0).length;

const now = new Date();
const stamp = now.toISOString().slice(0, 16).replace("T", " ") + " utc";

// ---------- drawing ----------
const W = 900, H = 430;
const GREEN = "#5CF27A", DIM = "#4E7A5A", INK = "#E9F5EC", BG = "#0A0E0C", LINE = "#1C2A20";
const mono = `font-family="JetBrains Mono, Cascadia Code, Fira Code, Menlo, Consolas, monospace"`;

// pixel name
const rows = JSON.parse(readFileSync(new URL("./name.json", import.meta.url), "utf8"));
const cw = 5, ch = 11, nx = 36, ny = 34;
let name = "";
rows.forEach((row, r) => {
  let c = 0;
  while (c < row.length) {
    if (row[c] === "#") { const s = c; while (c < row.length && row[c] === "#") c++;
      name += `<rect x="${nx + s * cw}" y="${ny + r * ch}" width="${(c - s) * cw}" height="${ch}"/>`; }
    else c++;
  }
});

// weekly bars
const bx = 36, by = 130, bw = 12, gap = 4, bh = 120;
const max = Math.max(1, ...weeks);
let bars = "", ticks = "";
weeks.forEach((v, i) => {
  const h = v === 0 ? 2 : Math.max(3, Math.round((v / max) * bh));
  const x = bx + i * (bw + gap), y = by + bh - h;
  const last = i === weeks.length - 1;
  const op = v === 0 ? 0.22 : last ? 1 : 0.45 + 0.55 * (v / max);
  bars += `<rect x="${x}" y="${y}" width="${bw}" height="${h}" rx="1.5" fill="${GREEN}" fill-opacity="${op.toFixed(2)}"/>`;
  const firstDay = cal.weeks.slice(-52)[i].contributionDays[0].date;
  if (firstDay.endsWith("-01") || (i > 0 && firstDay.slice(5, 7) !== cal.weeks.slice(-52)[i - 1].contributionDays[0].date.slice(5, 7))) {
    const m = new Date(firstDay + "T00:00:00Z").toLocaleString("en", { month: "short", timeZone: "UTC" }).toLowerCase();
    ticks += `<text x="${x}" y="${by + bh + 18}" fill="${DIM}" font-size="10">${m}</text>`;
  }
});

// this week, day by day
const week = cal.weeks[cal.weeks.length - 1].contributionDays;
let dots = "";
week.forEach((d, i) => {
  const on = d.contributionCount > 0;
  dots += `<rect x="${bx + i * 22}" y="330" width="16" height="16" rx="3" fill="${GREEN}" fill-opacity="${on ? 0.9 : 0.15}"/>`;
});

const stat = (x, n, label) =>
  `<text x="${x}" y="300" fill="${INK}" font-size="26" font-weight="700">${n}</text>` +
  `<text x="${x}" y="318" fill="${DIM}" font-size="11">${label}</text>`;

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img"
  aria-label="itsahmeds activity. ${total} contributions in the last year, ${thisWeek} this week, current streak ${current} days, longest ${longest} days. Regenerated ${stamp}.">
  <rect x="0.5" y="0.5" width="${W - 1}" height="${H - 1}" rx="10" fill="${BG}" stroke="${LINE}"/>
  <g ${mono}>
    <g fill="${GREEN}" shape-rendering="crispEdges">${name}</g>
    <text x="${W - 36}" y="46" text-anchor="end" fill="${DIM}" font-size="11">activity · regenerated ${stamp}</text>
    <text x="${W - 36}" y="62" text-anchor="end" fill="${DIM}" font-size="11">refreshes every 6h · private work counted, not shown</text>

    <text x="${bx}" y="118" fill="${DIM}" font-size="11">contributions per week · last 52 weeks</text>
    <line x1="${bx}" y1="${by + bh + 0.5}" x2="${bx + 52 * (bw + gap) - gap}" y2="${by + bh + 0.5}" stroke="${LINE}"/>
    ${bars}
    ${ticks}

    ${stat(bx, total, "last 365 days")}
    ${stat(bx + 190, last30, "last 30 days")}
    ${stat(bx + 380, current, "current streak, days")}
    ${stat(bx + 570, longest, "longest streak, days")}
    ${stat(bx + 760, busiest, "busiest day")}

    ${dots}
    <text x="${bx + 7 * 22 + 8}" y="343" fill="${DIM}" font-size="11">this week, sun to sat · ${thisWeek} so far · active ${activeDays} of ${days.length} days</text>

    <text x="${bx}" y="${H - 22}" fill="${DIM}" font-size="11">source: github contributions api · built by .github/workflows/activity.yml</text>
    <text x="${W - 36}" y="${H - 22}" text-anchor="end" fill="${DIM}" font-size="11">github.com/${LOGIN}</text>
  </g>
</svg>
`;

mkdirSync(new URL("../assets/", import.meta.url), { recursive: true });
writeFileSync(new URL("../assets/activity.svg", import.meta.url), svg);
console.log(`activity.svg written: total=${total} thisWeek=${thisWeek} current=${current} longest=${longest} busiest=${busiest}`);
