// Usage-gauge page checks (2026-09-22; Node, no browser): lift the pages' OWN `usageState` (index.html + chat.html) and run it on
// API-shaped rows: fresh -> "— 60%"; ageing (15..30 min) -> "— 60% (22m)" dimmed; absent / >= 30 min / unknown age -> "— no reading"
// dimmed with the last figure + age in the tooltip. Also: both pages fetch /api/usage, the "not synced" tooltips are gone, and the
// two pages carry the SAME function (one meaning on both surfaces — the 2026-09-09 lesson: enumerate every surface).
import fs from "node:fs"; import vm from "node:vm";
const HERE = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud"; let fails = 0;
const P = (ok, m) => { console.log((ok ? "PASS  " : "FAIL  ") + m); if (!ok) fails++; };
const pages = { "index.html": fs.readFileSync(`${HERE}/app/static/index.html`, "utf8"), "chat.html": fs.readFileSync(`${HERE}/app/static/chat.html`, "utf8") };
const lift = (html) => { const a = html.indexOf("const USE_STALE_S = 900, USE_DEAD_S = 1800;"), b = html.indexOf("function renderUsage(data)"); if (a < 0 || b < 0) throw new Error("usage block not found"); return html.slice(a, b); };
const blocks = Object.fromEntries(Object.entries(pages).map(([n, h]) => [n, lift(h)]));
P(blocks["index.html"] === blocks["chat.html"], "index.html and chat.html carry the SAME usageState/ageLabel block (one meaning on both surfaces)");
for (const [name, html] of Object.entries(pages)) {
  P(/WED\.getJSON\("\/api\/usage"\)/.test(html) && /setInterval\(pollUsage, 60000\)/.test(html), `${name}: polls GET /api/usage every 60 s through WED.getJSON`);
  P(!/weekly usage is not synced yet/.test(html), `${name}: the "not synced yet" tooltip is gone`);
  P(/id="use-wednesday"/.test(html) && /id="use-tuesday"/.test(html), `${name}: both chips keep their #use-<seat> spans`);
}
const ctx = {}; vm.createContext(ctx); vm.runInContext(blocks["index.html"], ctx);
const st = (d) => vm.runInContext("usageState(" + JSON.stringify(d) + ")", ctx);
let s = st({ seat: "wednesday", pct: 60, resets_in: "5d 2h", age_seconds: 120 });
P(s.text === " — 60%" && s.cls === "use" && /renews in 5d 2h/.test(s.title) && /reading 2m old/.test(s.title), `fresh (2m): ${JSON.stringify(s.text)} cls=${s.cls} title carries renewal + age`);
s = st({ seat: "tuesday", pct: 19, resets_in: "4d 19h", age_seconds: 1320 });
P(s.text === " — 19% (22m)" && s.cls === "use stale", `ageing (22m): ${JSON.stringify(s.text)} dimmed`);
s = st({ seat: "wednesday", pct: 60, resets_in: "5d", age_seconds: 1800 });
P(s.text === " — no reading" && s.cls === "use stale" && /last published 30m ago \(60%\)/.test(s.title), `stale (30m): ${JSON.stringify(s.text)} — tooltip: ${s.title}`);
s = st({ seat: "wednesday", pct: 60, age_seconds: 7200 });
P(s.text === " — no reading" && /2h ago \(60%\)/.test(s.title), `stale (2h): no reading, tooltip keeps the last figure`);
s = st(null);
P(s.text === " — no reading" && s.cls === "use stale" && /has not published/.test(s.title), `absent (null): ${JSON.stringify(s.text)} — ${s.title}`);
s = st({ seat: "wednesday", pct: 60, age_seconds: null });
P(s.text === " — no reading", `unknown age (null): no reading (never rendered as fresh)`);
s = st({ seat: "wednesday", pct: "60", age_seconds: 10 });
P(s.text === " — no reading", `pct not a number: no reading (claims nothing)`);
console.log(fails ? `### RESULT: ${fails} FAILED` : "### RESULT: ALL USAGE PAGE CHECKS PASS (the pages' own usageState in Node; not a browser)");
process.exit(fails ? 1 : 0);
