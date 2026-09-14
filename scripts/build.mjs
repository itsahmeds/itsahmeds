// Regenerates assets/activity.svg from the GitHub contributions API plus scripts/profile.json.
// Zero dependencies. Run: GITHUB_TOKEN=... node scripts/build.mjs
import { readFileSync, writeFileSync, mkdirSync } from "node:fs";

const LOGIN = "itsahmeds";
const TOKEN = process.env.GITHUB_TOKEN;
if (!TOKEN) throw new Error("GITHUB_TOKEN missing");

const profile = JSON.parse(readFileSync(new URL("./profile.json", import.meta.url), "utf8"));
const rows = JSON.parse(readFileSync(new URL("./name.json", import.meta.url), "utf8"));

const query = `{
  user(login: "${LOGIN}") {
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
const weeks52 = cal.weeks.slice(-52);
const weeks = weeks52.map((w) => w.contributionDays.reduce((a, d) => a + d.contributionCount, 0));
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
const stamp = new Date().toISOString().slice(0, 16).replace("T", " ") + " utc";

// ---------- drawing ----------
const W = 900;
const GREEN = "#5CF27A", DIM = "#4E7A5A", INK = "#E9F5EC", OUT = "#B8D9C0", BG = "#0A0E0C", LINE = "#1C2A20";
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const mono = `font-family="JetBrains Mono, Cascadia Code, Fira Code, Menlo, Consolas, monospace"`;

// pixel name
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

// section 1: activity
const bx = 36, by = 150, bw = 12, gap = 4, bh = 110;
const max = Math.max(1, ...weeks);
let bars = "", ticks = "";
weeks.forEach((v, i) => {
  const h = v === 0 ? 2 : Math.max(3, Math.round((v / max) * bh));
  const x = bx + i * (bw + gap), y = by + bh - h;
  const last = i === weeks.length - 1;
  const op = v === 0 ? 0.22 : last ? 1 : 0.45 + 0.55 * (v / max);
  const t0 = (0.2 + i * 0.022).toFixed(3);
  const breathe = last ? `<animate attributeName="fill-opacity" values="1;0.55;1" dur="2.4s" begin="${(0.2 + i * 0.022 + 0.6).toFixed(2)}s" repeatCount="indefinite"/>` : "";
  bars += `<rect x="${x}" y="${by + bh}" width="${bw}" height="0" rx="1.5" fill="${GREEN}" fill-opacity="${op.toFixed(2)}">` +
    `<animate attributeName="height" from="0" to="${h}" dur="0.5s" begin="${t0}s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>` +
    `<animate attributeName="y" from="${by + bh}" to="${y}" dur="0.5s" begin="${t0}s" fill="freeze" calcMode="spline" keySplines="0.2 0.8 0.2 1"/>${breathe}</rect>`;
  const first = weeks52[i].contributionDays[0].date;
  const prev = i > 0 ? weeks52[i - 1].contributionDays[0].date : null;
  if (!prev || first.slice(5, 7) !== prev.slice(5, 7)) {
    const m = new Date(first + "T00:00:00Z").toLocaleString("en", { month: "short", timeZone: "UTC" }).toLowerCase();
    ticks += `<text x="${x}" y="${by + bh + 18}" fill="${DIM}" font-size="10">${m}</text>`;
  }
});
// gridlines at quarter steps of the peak, labelled with the value they mark
let grid = "";
[0.25, 0.5, 0.75, 1].forEach((f) => {
  const v = Math.round(max * f), y = by + bh - Math.round(f * bh) + 0.5;
  grid += `<line x1="${bx}" y1="${y}" x2="${bx + 52 * (bw + gap) - gap}" y2="${y}" stroke="${LINE}" stroke-dasharray="2 4"/>`;
  grid += `<text x="${bx + 52 * (bw + gap) + 6}" y="${y + 4}" fill="${DIM}" font-size="10">${v}</text>`;
});
const peakI = weeks.indexOf(max);
const peakDate = weeks52[peakI].contributionDays[0].date;
const peakLabel = `peak ${max} · week of ${new Date(peakDate + "T00:00:00Z").toLocaleString("en", { month: "short", day: "numeric", timeZone: "UTC" }).toLowerCase()}`;
const peakX = Math.min(bx + peakI * (bw + gap), bx + 52 * (bw + gap) - 220);
const peak = `<text x="${peakX}" y="${by - 12}" fill="${OUT}" font-size="11">${peakLabel}</text>`;
const statY = by + bh + 62;
let statI = 0;
const stat = (x, n, label) => {
  const b = (1.5 + statI++ * 0.12).toFixed(2);
  return `<g opacity="0"><animate attributeName="opacity" from="0" to="1" dur="0.5s" begin="${b}s" fill="freeze"/>` +
    `<text x="${x}" y="${statY}" fill="${INK}" font-size="24" font-weight="700">${n}</text>` +
    `<text x="${x}" y="${statY + 18}" fill="${DIM}" font-size="11">${label}</text></g>`;
};
const week = cal.weeks[cal.weeks.length - 1].contributionDays;
const dotsY = statY + 42;
let dots = "";
const wd = ["s", "m", "t", "w", "t", "f", "s"];
week.forEach((d, i) => {
  dots += `<rect x="${bx + i * 22}" y="${dotsY}" width="16" height="16" rx="3" fill="${GREEN}" fill-opacity="${d.contributionCount > 0 ? 0.9 : 0.15}"/>`;
  dots += `<text x="${bx + i * 22 + 8}" y="${dotsY + 30}" text-anchor="middle" fill="${DIM}" font-size="10">${wd[i]}</text>`;
});

// section 2: stack + work (from profile.json)
const secY = dotsY + 72;
const lh = 22;
let stack = `<text x="${bx}" y="${secY}" fill="${DIM}" font-size="11">stack</text>`;
profile.stack.forEach(([k, v], i) => {
  const y = secY + 24 + i * lh;
  stack += `<text x="${bx}" y="${y}" fill="${GREEN}" font-size="13">${esc(k)}</text><text x="${bx + 130}" y="${y}" fill="${OUT}" font-size="13">${esc(v)}</text>`;
});
const workY = secY + 24 + profile.stack.length * lh + 26;
let work = `<text x="${bx}" y="${workY}" fill="${DIM}" font-size="11">work</text>`;
profile.work.forEach(([k, v], i) => {
  const y = workY + 24 + i * lh;
  work += `<text x="${bx}" y="${y}" fill="${INK}" font-size="13">${esc(k)}</text><text x="${bx + 200}" y="${y}" fill="${OUT}" font-size="13">${esc(v)}</text>`;
});
const moreY = workY + 24 + profile.work.length * lh;
work += `<text x="${bx + 200}" y="${moreY}" fill="${DIM}" font-size="12">${esc(profile.more)}</text>`;

const H = moreY + 84;

const svg = `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img"
  aria-label="itsahmeds. ${esc(profile.line)}. ${total} contributions in the last year, ${thisWeek} this week, current streak ${current} days, longest ${longest}. Stack: ${esc(profile.stack.map((s) => s[1]).join("; "))}. Work: ${esc(profile.work.map((w) => w[0]).join(", "))}. Regenerated ${stamp}.">
  <rect x="0.5" y="0.5" width="${W - 1}" height="${H - 1}" rx="10" fill="${BG}" stroke="${LINE}"/>
  <g ${mono}>
    <g fill="${GREEN}" shape-rendering="crispEdges">${name}</g>
    <text x="${bx}" y="112" fill="${OUT}" font-size="13">${esc(profile.line)}</text>
    <text x="${W - 36}" y="100" text-anchor="end" fill="${DIM}" font-size="11"><tspan fill="${GREEN}">●<animate attributeName="fill-opacity" values="1;0.2;1" dur="2.4s" repeatCount="indefinite"/></tspan> live · regenerated ${stamp} · every 6h</text>
    <text x="${W - 36}" y="115" text-anchor="end" fill="${DIM}" font-size="11">private work counted, not shown</text>

    <text x="${bx}" y="${by - 12}" fill="${DIM}" font-size="11">contributions per week · last 52 weeks</text>
    <line x1="${bx}" y1="${by + bh + 0.5}" x2="${bx + 52 * (bw + gap) - gap}" y2="${by + bh + 0.5}" stroke="${LINE}"/>
    ${grid}
    ${peak}
    ${bars}
    <rect x="${bx}" y="${by - 4}" width="2" height="${bh + 4}" fill="${GREEN}" fill-opacity="0.35">
      <animate attributeName="x" from="${bx}" to="${bx + 52 * (bw + gap) - 2}" dur="7s" begin="1.2s" repeatCount="indefinite"/>
    </rect>
    ${ticks}
    ${stat(bx, total, "last 365 days")}
    ${stat(bx + 190, last30, "last 30 days")}
    ${stat(bx + 380, current, "current streak, days")}
    ${stat(bx + 570, longest, "longest streak, days")}
    ${stat(bx + 760, busiest, "busiest day")}
    ${dots}
    <text x="${bx + 7 * 22 + 8}" y="${dotsY + 13}" fill="${DIM}" font-size="11">this week, sun to sat · ${thisWeek} so far · active ${activeDays} of ${days.length} days</text>

    <line x1="${bx}" y1="${secY - 30}" x2="${W - 36}" y2="${secY - 30}" stroke="${LINE}"/>
    ${stack}
    ${work}

    <text x="${bx}" y="${H - 48}" fill="${OUT}" font-size="13">ahmedsheikh2654@gmail.com</text>
    <text x="${W - 36}" y="${H - 48}" text-anchor="end" fill="${OUT}" font-size="13">linkedin.com/in/ahmed-hameed-037676253</text>
    <text x="${bx}" y="${H - 22}" fill="${DIM}" font-size="11">source: github contributions api + scripts/profile.json · built by .github/workflows/activity.yml</text>
    <text x="${W - 36}" y="${H - 22}" text-anchor="end" fill="${DIM}" font-size="11">github.com/${LOGIN}</text>
  </g>
</svg>
`;

mkdirSync(new URL("../assets/", import.meta.url), { recursive: true });
writeFileSync(new URL("../assets/activity.svg", import.meta.url), svg);
console.log(`activity.svg written: ${W}x${H} total=${total} thisWeek=${thisWeek} current=${current} longest=${longest} busiest=${busiest}`);
