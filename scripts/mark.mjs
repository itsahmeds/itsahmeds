// Draws assets/mark-light.svg and assets/mark-dark.svg: one quiet band, the year as a line.
// Transparent background on purpose, so it sits directly on GitHub's page with no card around it.
// Zero dependencies. Run: GITHUB_TOKEN=... node scripts/mark.mjs
import { writeFileSync, mkdirSync } from "node:fs";

const LOGIN = "itsahmeds";
const TOKEN = process.env.GITHUB_TOKEN;
if (!TOKEN) throw new Error("GITHUB_TOKEN missing");

const res = await fetch("https://api.github.com/graphql", {
  method: "POST",
  headers: { Authorization: `bearer ${TOKEN}`, "Content-Type": "application/json", "User-Agent": LOGIN },
  body: JSON.stringify({
    query: `{ user(login:"${LOGIN}"){ contributionsCollection { contributionCalendar {
      totalContributions weeks { contributionDays { contributionCount } } } } } }`,
  }),
});
const json = await res.json();
if (json.errors) throw new Error(JSON.stringify(json.errors));
const cal = json.data.user.contributionsCollection.contributionCalendar;

const weeks = cal.weeks.slice(-52).map((w) => w.contributionDays.reduce((a, d) => a + d.contributionCount, 0));
const total = cal.totalContributions;
const REPOS = 40, PRIVATE = 36;

const W = 860, H = 176, BASE = 150, AMP = 54;
const SANS = "-apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, Helvetica, Arial, sans-serif";
const MONO = "'JetBrains Mono', 'Cascadia Code', 'DejaVu Sans Mono', Menlo, Consolas, monospace";

const max = Math.max(1, ...weeks);
const step = W / (weeks.length - 1);
const pts = weeks.map((v, i) => [i * step, BASE - (v / max) * AMP]);
const line = pts.map(([x, y], i) => `${i ? "L" : "M"}${x.toFixed(1)} ${y.toFixed(1)}`).join(" ");
const area = `${line} L${W} ${BASE} L0 ${BASE} Z`;
const [lx, ly] = pts[pts.length - 1];

function build({ ink, muted, faint }) {
  return `<svg xmlns="http://www.w3.org/2000/svg" width="${W}" height="${H}" viewBox="0 0 ${W} ${H}" role="img"
  aria-label="Ahmed Hameed, software engineer by degree, marketer by trade. ${total} commits in the last twelve months across ${REPOS} repositories, ${PRIVATE} of them private.">
  <text x="0" y="46" fill="${ink}" font-family="${SANS}" font-size="38" font-weight="600" letter-spacing="-0.6">Ahmed Hameed</text>
  <text x="0" y="70" fill="${muted}" font-family="${SANS}" font-size="13.5">software engineer by degree, marketer by trade</text>
  <path d="${area}" fill="${ink}" fill-opacity="0.07"/>
  <path d="${line}" fill="none" stroke="${ink}" stroke-width="1.6" stroke-linejoin="round" stroke-linecap="round" opacity="0.85"/>
  <line x1="0" y1="${BASE}" x2="${W}" y2="${BASE}" stroke="${faint}" stroke-width="1"/>
  <circle cx="${lx.toFixed(1)}" cy="${ly.toFixed(1)}" r="3.2" fill="${ink}"/>
  <text x="0" y="170" fill="${muted}" font-family="${MONO}" font-size="11">${total.toLocaleString("en-US")} commits in the last 12 months  ·  ${REPOS} repositories, ${PRIVATE} private</text>
</svg>
`;
}

mkdirSync(new URL("../assets/", import.meta.url), { recursive: true });
writeFileSync(new URL("../assets/mark-light.svg", import.meta.url),
  build({ ink: "#12120F", muted: "#6B6B63", faint: "#DEDDD6" }));
writeFileSync(new URL("../assets/mark-dark.svg", import.meta.url),
  build({ ink: "#EDEDE8", muted: "#8C8C84", faint: "#2A2A26" }));
console.log(`mark written: ${total} commits, peak week ${max}`);
