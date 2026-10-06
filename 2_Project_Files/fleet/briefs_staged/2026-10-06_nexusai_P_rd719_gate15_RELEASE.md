# STAGED RELEASE for the next NexusAI-P seat (P is CLOSED; relaunch P's lane to land it). Written by Tuesday s99, 2026-10-06 ~16:2x AEDT.

## BLUF
RELEASE: gate 15 — RD-719 @ 7861a06 (Chart.js 3.9.1 vendored, tier 1) is GO WITH FINDINGS, no Blocker. Report: Testing Agent MAIN/projects/nexusai/reports/2026-10-05-gate-batch15/report.md (read WHOLE by Tuesday). Land it in P's merge turn; RD-721 (filed by S86P, waits on RD-719's GO per C-182) is then unblocked.

## Measured by the gate (§1)
sha384 = the root commit 8eb94ce's pin; byte-identical to the official chart.js-3.9.1.tgz package/dist/chart.min.js (R-NET, cmp rc 0); CSP unchanged; image leg (manifest): added exactly static/vendor/chart-3.9.1.min.js, changed exactly static/index.html; browser leg (local, offline, NOT the demo): painted 4 open / 4 signed in, base 0, SRI tamper refused; full verify 4240/257; onto END main 9938876: counts only. Recommended merge order RD-719 -> RD-424 (order-independent).

## Findings -> ONE ticket (Kam's one-ticket rule), linked to RD-719, filed by P
- A-F1 MAJOR (C-40): the vendored file's identity is guarded by the provenance RECORD alone; a consistent swap of file + record + page attribute (M-swap) leaves 747/747 green. Fix-shape: a cell pinning the sha384 (or upstream sha256 fbc4…e710) to a CONSTANT independent of the record; M-swap must turn it red.
- A-F2 Minor: V3 misses protocol-relative //cdn tags, CDN URLs inside shipped .js, and pages under a static/ subdirectory. Fix-shape: scheme-optional matcher over the shipped set (.html + .js).
- A-F4 Minor (Tuesday's MINOR): the MIT notice TEXT ships for neither Chart.js nor @kurkle/color; a shipped third-party notices file (RD-721 can carry it).
- A-F3 (READY said 10 `new Chart(` sites; 16) and A-P1 (15:55:13Z vs 15:55:14Z) go in the MERGED mail. A-N1 (/vendor/ is outside STATIC_ASSET_PREFIXES; signed-in requests stamp session activity) is a deployment note for RD-721.
## DECISION OWED BY TUESDAY before P lands it: A-F1 is a Major on a COVERAGE gap (the product bytes are proven identical to upstream). Tuesday s99's reading: land RD-719 now, A-F1 fixed in the follow-up ticket's first round (tier 2, through code), because RD-721 is blocked on it and the shipped bytes are proven; re-confirm at the relaunch.
## Open, not P's: Y-F1 (rd490 timeouts in one MT1 plain verify, unreproduced): watch rd490 in CI on the PR.
