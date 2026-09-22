// Phase 3 page checks (Node, no browser): (1) DOM ORDER of the cockpit mirror — #needs precedes #feed inside ONE #feedscroll and
// no pinned #needscroll region exists; the local cockpit.html still HAS its pinned region (untouched). (2) SYNTHETIC FILTER — a row
// with synthetic=true present in an API-shaped response is absent from what the pages keep, using common.js's own isSynthetic and
// the exact ingestion statements lifted from index.html / chat.html.
import fs from "node:fs"; import vm from "node:vm";
const HERE = "/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard-cloud"; let fails = 0;
const P = (ok, m) => { console.log((ok ? "PASS  " : "FAIL  ") + m); if (!ok) fails++; };
const idx = fs.readFileSync(`${HERE}/app/static/index.html`, "utf8"), chat = fs.readFileSync(`${HERE}/app/static/chat.html`, "utf8");
const local = fs.readFileSync("/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/dashboard/cockpit.html", "utf8");
const fs_i = idx.indexOf('id="feedscroll"'), needs_i = idx.indexOf('id="needs"'), feed_i = idx.indexOf('id="feed"'), close_i = idx.indexOf("</div></div>", feed_i);
P(fs_i > 0 && fs_i < needs_i && needs_i < feed_i && feed_i < close_i && !/id="needscroll"/.test(idx), `live index.html: #feedscroll[${fs_i}] > #needs[${needs_i}] > #feed[${feed_i}] in ONE scroller; no #needscroll (pinned region) in the live page`);
P(/id="needscroll"/.test(local) && /#needscroll\s*\{\s*flex:none/.test(local), "local cockpit.html UNTOUCHED: still has its pinned #needscroll region");
P(!/#needscroll\s*\{\s*flex:none/.test(idx), "live index.html CSS: the pinned #needscroll rule is gone");
const rf = idx.slice(idx.indexOf("function renderFeed"), idx.indexOf("async function pollDecisions"));
P(rf.indexOf("needsEl.appendChild(decisionCard(d))") < rf.indexOf('uh.textContent = "Updates"'), "renderFeed: Needs-you cards are appended before the Updates head (Updates renders BELOW)");
// (2) synthetic filter
const src = fs.readFileSync(`${HERE}/app/static/common.js`, "utf8");
const sb = { window: {}, crypto: globalThis.crypto, TextEncoder, TextDecoder, atob, btoa, console, localStorage: undefined, indexedDB: undefined, fetch: async () => { throw new Error("no fetch"); } };
sb.globalThis = sb; vm.createContext(sb); vm.runInContext(src, sb); const WED = sb.window.WED;
const api = { messages: [{ row_key: "2026-09-21T01:00:00.000Z_real", id: "real", synthetic: false }, { row_key: "2026-09-21T01:00:01.000Z_syn", id: "live-syn", synthetic: true }, { row_key: "2026-09-21T01:00:02.000Z_real2", id: "real2" }],
              cards: [{ id: "card-real" }, { id: "live-card-syn", synthetic: true }] };
const pick = (html, marker) => { const line = html.split("\n").find(l => l.includes(marker)); if (!line) throw new Error("no line " + marker); return line.trim(); };
// index.html poll() ingestion, verbatim
const pollLine = pick(idx, "if (WED.isSynthetic(r) || WED.isHidden(r)) { WED.hidden.messages++; continue; }   // synthetic: skipped, never rendered") + "\n" + pick(idx, "if (!rows.has(r.row_key)) fresh.push(r); rows.set(r.row_key, r); }");
const run = (code) => { const ctx = { WED, d: api, rows: new Map(), fresh: [], sinceM: "", cardRows: new Map() }; vm.createContext(ctx); vm.runInContext(code, ctx); return ctx; };
let c = run(pollLine); P(c.rows.size === 2 && !c.rows.has("2026-09-21T01:00:01.000Z_syn") && c.sinceM === "2026-09-21T01:00:02.000Z_real2" && WED.hidden.messages === 1, `index.html poll(): 3 rows from the API -> ${c.rows.size} kept, the synthetic one absent, sinceM still advanced past it, hidden.messages=${WED.hidden.messages}`);
c = run(pick(idx, "for (const r of d.cards || []) { if (WED.isSynthetic(r)) { WED.hidden.cards++; continue; } cardRows.set(r.id, r); }"));
P(c.cardRows.size === 1 && !c.cardRows.has("live-card-syn") && WED.hidden.cards === 1, `index.html pollDecisions(): 2 cards -> ${c.cardRows.size} kept, synthetic card absent, hidden.cards=${WED.hidden.cards}`);
c = run(pick(chat, "if (WED.isSynthetic(r) || WED.isHidden(r)) { WED.hidden.messages++; continue; } rows.set(r.row_key, r); }   // synthetic hidden"));
P(c.rows.size === 2 && !c.rows.has("2026-09-21T01:00:01.000Z_syn"), `chat.html poll(): synthetic row absent from the kept rows (${c.rows.size} of 3)`);
// (3) hidden rows (2026-09-22): a row with hidden=true is skipped by both pages' ingestion (defence in depth behind the API's own filter);
//     WED.hiddenQ is empty when the page URL has no ?hidden=1 (the sandbox has no location), so the API call carries no reveal.
const apiH = { messages: [{ row_key: "2026-09-22T04:00:00.000Z_keep", id: "keep" }, { row_key: "2026-09-22T04:00:01.000Z_hid", id: "hid", hidden: true, hidden_by: "x", hidden_at: "2026-09-22T04:30:00Z" }] };
const runH = (code) => { const ctx = { WED, d: apiH, rows: new Map(), fresh: [], sinceM: "", cardRows: new Map() }; vm.createContext(ctx); vm.runInContext(code, ctx); return ctx; };
const h0 = WED.hidden.messages; let h = runH(pollLine);
P(h.rows.size === 1 && !h.rows.has("2026-09-22T04:00:01.000Z_hid") && h.sinceM === "2026-09-22T04:00:01.000Z_hid" && WED.hidden.messages === h0 + 1, `index.html poll(): hidden=true row absent (${h.rows.size} of 2 kept), sinceM advanced past it, counted as hidden`);
h = runH(pick(chat, "if (WED.isSynthetic(r) || WED.isHidden(r)) { WED.hidden.messages++; continue; } rows.set(r.row_key, r); }   // synthetic hidden"));
P(h.rows.size === 1 && !h.rows.has("2026-09-22T04:00:01.000Z_hid"), `chat.html poll(): hidden=true row absent (${h.rows.size} of 2 kept)`);
P(WED.hiddenQ === "" && WED.revealHidden === false && typeof WED.isHidden === "function", "common.js: no ?hidden=1 -> hiddenQ empty, revealHidden false (the API is not asked for hidden rows)");
P(/WED\.hiddenQ/.test(idx.split("async function poll(")[1].split("\n")[3]) && /WED\.hiddenQ/.test(chat.split("async function poll(")[1].split("\n")[3]), "both pages pass WED.hiddenQ on the poll() API call (the ?hidden=1 reveal reaches the API)");
console.log(fails ? `### RESULT: ${fails} FAILED` : "### RESULT: ALL PAGE CHECKS PASS (static DOM order + the pages' own ingestion statements in Node; not a browser)");
process.exit(fails ? 1 : 0);
