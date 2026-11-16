// 09f — project-filter scope checks (Node, no browser). 2026-11-16, Friday seat.
// WHY: Kam, live board 2026-11-16 22:53: "I also cannot see any items on the fleet activity". His browser held a saved project
// filter whose chip the FRIDAY tab does not draw (agentOfProject() of that name is another seat), yet projOk still applied it,
// so every card was excluded and only "✕ clear" showed. RULE UNDER TEST: a saved project filter applies ONLY when its chip is
// drawn in the current view; whenever cards are excluded by a project filter, a lit chip for it is on screen.
// Usage: node 09f_filter_scope_checks.mjs [path/to/index.html]   (default: the index.html beside this script's app/static)
// RED ARM: run it against the pre-fix page (index.html.pre-1116-2305-hiddenfilter) — arms A and B must FAIL there.
// The code under test is LIFTED from the page text (the page's own statements), never re-typed here.
import fs from "node:fs"; import vm from "node:vm"; import path from "node:path"; import { fileURLToPath } from "node:url";
const HERE = path.dirname(fileURLToPath(import.meta.url));
const file = process.argv[2] || path.join(HERE, "..", "app", "static", "index.html");
const html = fs.readFileSync(file, "utf8"); let fails = 0;
const P = (ok, m) => { console.log((ok ? "PASS  " : "FAIL  ") + m); if (!ok) fails++; };
const line = (marker) => { const l = html.split("\n").find(x => x.includes(marker)); if (!l) throw new Error("page has no line containing: " + marker); return l; };
const between = (a, b) => { const i = html.indexOf(a), j = html.indexOf(b, i); if (i < 0 || j < 0) throw new Error("page has no block " + a + " .. " + b); return html.slice(i, j); };
// lifted: agentOfProject, the filter state helpers (present only after the fix), renderFilters, and renderFeed's filter statements
const helpers = html.includes("function activeProjectFilters") ? line("let drawnProjects") + "\n" + line("function activeProjectFilters") : "";
const projLines = html.split("\n").filter(l => /const (activeProj|projOk|typeOk) = /.test(l)).join("\n");
const code = [line("function agentOfProject(p)"), helpers, between("function renderFilters(decisions)", "function parseDecisions()"),
  "function visible(dp) { renderFilters(dp.open.concat(dp.ruledToday));\n" + projLines + "\n return dp.open.filter(d => typeOk('decision') && projOk(d)); }"].join("\n");
function run(view, saved, open) {
  const chips = [];
  const mk = () => ({ className: "", textContent: "", addEventListener() {}, appendChild() {} });
  const ctx = { activeAgent: view, filters: { types: [], projects: saved.slice() }, saveFilters() {}, renderFeed() {},
    filtersEl: { innerHTML: "", appendChild(b) { chips.push({ text: b.textContent, on: / on$| on /.test(" " + b.className + " ") && !/clear/.test(b.className), clear: /clear/.test(b.className) }); } },
    document: { createElement: mk } };
  vm.createContext(ctx); vm.runInContext(code, ctx);
  const vis = vm.runInContext("visible(dp)", Object.assign(ctx, { dp: { open, ruledToday: [] } }));
  return { vis, chips, lit: chips.filter(c => c.on).map(c => c.text), clear: chips.some(c => c.clear) };
}
const fri = (id, project) => ({ id, project, agent: "friday" }), tue = (id, project) => ({ id, project, agent: "tuesday" }), wed = (id, project) => ({ id, project, agent: "wednesday" });
const cards = [fri("f1", "General/Claude to Claude"), fri("f2", "General/Claude to Claude"), tue("t1", "Datasec/NexusAI"), wed("w1", "Secuura/Blockchain")];
// A — Kam's case: FRIDAY view, a saved filter for a project of another seat (no chip here). Every Friday card must show.
let r = run("friday", ["Datasec/HPSM-POC"], cards);
P(r.vis.length === 2 && r.lit.length === 0, `A  FRIDAY view + saved filter "Datasec/HPSM-POC" (not drawn here): ${r.vis.length} of 2 Friday cards visible, lit chips=[${r.lit}]`);
P(!r.clear, `A2 no "✕ clear" is drawn when no filter is in effect in this view (clear drawn: ${r.clear})`);
// B — a filter saved on the TUESDAY tab for a project that has cards there must not empty the FRIDAY tab.
r = run("friday", ["Datasec/NexusAI"], cards);
P(r.vis.length === 2, `B  FRIDAY view + filter saved on the Tuesday tab ("Datasec/NexusAI"): ${r.vis.length} of 2 Friday cards visible`);
// C — the filter still WORKS where its chip is drawn (clean arm: the legitimate use is not broken).
r = run("friday", ["General/Claude to Claude"], cards.concat([fri("f3", "General/Other")]));
P(r.vis.length === 2 && r.vis.every(d => d.project === "General/Claude to Claude") && r.lit.includes("General/Claude to Claude") && r.clear, `C  FRIDAY view + its own project filter: ${r.vis.length} shown (3 Friday cards, 1 other project excluded), chip lit, clear drawn`);
r = run("tuesday", ["Datasec/NexusAI"], cards.concat([tue("t2", "Datasec/HPSM-POC")]));
P(r.vis.length === 1 && r.vis[0].id === "t1" && r.lit.includes("Datasec/NexusAI"), `C2 TUESDAY view + "Datasec/NexusAI": ${r.vis.length} shown, chip lit`);
// D — a saved filter whose project has NO cards now but belongs to this view is still drawn lit (existing behaviour kept) and filters.
r = run("tuesday", ["Datasec/HPSM-POC"], cards);
P(r.vis.length === 0 && r.lit.includes("Datasec/HPSM-POC") && r.clear, `D  TUESDAY view + filter for a Datasec project with no cards: 0 shown, and its chip IS drawn lit with clear (the exclusion is visible)`);
// E — invariant over every view: cards excluded by a project filter => a lit chip is on screen.
let bad = 0;
for (const v of ["friday", "tuesday", "wednesday"]) for (const s of [["Datasec/HPSM-POC"], ["Datasec/NexusAI"], ["Secuura/Blockchain"], ["General/Claude to Claude"], ["friday"], ["No/Such"]]) {
  const x = run(v, s, cards), own = cards.filter(d => d.agent === v).length; if (x.vis.length < own && x.lit.length === 0) { bad++; console.log(`      hidden with no lit chip: view=${v} saved=${s}`); } }
P(bad === 0, `E  18 view x saved-filter combinations: ${bad} case(s) where cards are hidden with no lit chip (must be 0)`);
// no filter at all: everything of the view shows (positive control for the harness itself)
r = run("friday", [], cards); P(r.vis.length === 2 && !r.clear, `F  control, no saved filter: ${r.vis.length} of 2 visible`);
console.log(fails ? `\n${fails} FAIL` : "\nall PASS"); process.exit(fails ? 1 : 0);
