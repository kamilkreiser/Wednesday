STARTABLE: YES once PR 231 has merged (the kit refuses itself until pulls/231 .merged prints true, REFUSE 4(b)); every measurement is at f06b080e because 231 was open at 15:01.

# B1737 drafter report (SEAT-N158, NexusAI lane N-F: RD-835 + RD-861)
Saved by Tuesday (s292) from the drafter's in-session reply (a subagent returns its report as text). Condensed by Tuesday; the kit is the authority.

## Files
Kit `2026-11-19_B1737_SEAT-N158_nexusai-lane-nf-browser-escapes.md` (272 lines, 85251 bytes, ASCII, sha256 prefix 2ca213e1c8950b5a; 5 slot lines); sidecar `.measured` 188 lines; stamp_check 188/188 rc 0. Scratch `2_Project_Files/fleet/state/s292/d1737/`.

## Shape
One lane, serial: A835 (index.js +23 -12: top-level csvCell, the eight esc closures pointed at it, plus the Printing and AI-reply writers), A861 (index.js +9 -3, settings.js +5 -5, first-run-setup.js +5 -5: escapeAttrValue, the user table and userNameWithInfo attributes, the dialog values via the files' own escapeHtml), T835, T861, at most two merges, K. No backend file, no inventory. Frozen patch apply1737.py: node --check 0 in all modes; blobs index.js A835 02893d5729f2, both 676a78625c63; settings.js f82ca22d8b27; first-run-setup.js 6e1992d07958. Predicted cells rd835 22, rd861 20; counts 6128/386. Slot 15 (band 29600-30239). Pane Datasec/NexusAI-N158, Sonnet C2.

## Gate tier
Recommend G1 Opus: XSS and formula-injection fixes on sinks fed by non-administrator data (user names break out of data-arg/title attributes in jsdom at base; ten of ten CSV writers emit a live leading '=' cell). CSP strict by default (server.js:846) but CSP_STRICT=false allows inline handlers; whether any deployment sets it: UNMEASURED.

## Old-answer census
Frame 468 .js under __tests__ and tests at f06b080e; readers 84 (76 .test.js, 5 helpers, 3 Playwright). No existing test pins a changed answer (rd778 controls use plain values). RD-131's drum cell lives only on stale branch rd-131-fleet-health-drum-csv-s87n (behind 596): STOP if it lands first. Heads census: 245 heads, 7 touch the three scripts, all stale.

## Corrections to the commission
Ten CSV writers, not eight (exportPrintingCSV :2100, exportResponseAsCSV :3046); RD-861 twin sinks settings.js:2102 and first-run-setup.js:2915; the user-table hole is userName in the attribute, not userClass; no RD-131 drum cell on main; no strictly free slot (15 appears only in a finished kit's control sentence); PR 231 touches no static/**.

## Q-questions (defaults)
Q-1 csvCell after escapeHtml; Q-2 prefix = + - @ tab CR inside quotes, exempt plain numbers and dash runs; Q-3 include the two extra writers; Q-4 fix the two identical-statement twins; Q-5 narrow escapeAttrValue (list :5769, :7437, :7459, :7375, :9285 for a follow-up); Q-6 escape userClass too; Q-7 DOM-fed raw numeric CSV columns left alone (listed); Q-8 G1 Opus; Q-9 CQ-1 and CQ-2 required; Q-10 slot 15, HARD STOP 18:00; Q-11 STOP if RD-131's branch or any head changes the exporters or userNameWithInfo; Q-12 ONE jest acquisition (judge/kept proved offline on .tools/b1733/raw/red-1.json; main move absorbed by conditional steps).

## UNMEASURED
jest colours of the new cells; CodeQL; CSP_STRICT=false deployments; DOM-fed numeric column provenance; OWASP's extra leading characters; a real browser and a spreadsheet opening a file; hosted CodeQL; retagging of the b1733 scripts.

## Disclosures
Wrote only the kit, sidecar and scratch; sed -i and .bak inside scratch only; node on scratch copies with the project's jsdom read-only; gh GET only; Jira GET only (RD-835, RD-861, RD-131, RD-778); no cd.
