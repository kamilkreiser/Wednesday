# STAGED — Datasec / NexusAI S24 — the Sustainability tab relayout (Kam's commission 13:1x, APPROVED 13:18, 2026-09-03 AEST) — not yet sent (after the 149e358 deploy + S23's wrap)

**Status:** APPROVED by Kam — panel 13:18:16 2026-09-03, verbatim: "That's fantastic. I agree with the approach. Please go ahead." (the approach + sequencing as mirrored 13:16). Commission section for the S24 brief. Sent only after the 149e358 deploy (Kam's 11:59 ask) and S23's wrap. The S24 brief proper adds the standing sections (protocol, provenance gate, holds, QA gate, CTX stop-line) from the S23 brief; this file is the WHAT.

## Kam's words (terminal, dictated, verbatim — the spec; read through dictation noise)
> The Nexus and the Sustainability page. Let's change the layout a little bit.
> Create one tile with the different metrics and add a little eye next to it. When clicked, shows where the calculation and where the data comes from. So displayed, we'll only have the actual stats.
> Then create a bigger pane which actually showcases the sustainability improvements. This will be calculated by printing double-sided versus single-sided, printing black and white versus color and anything else that you think would be useful?

> Paitilesns or stats that are unavailable, do not include.   ← "panels/tiles or stats that are unavailable, do not include"

## Wednesday's reading (proposed to Kam 13:1x with a DEFAULT; stands unless he amends)
1. **One metrics tile** replaces the nine-tile grid: the available KPIs only (impressions · sheets · A4-equivalent · duplex rate · paper mass · paper cost · water impact · wood use · tree-equivalent fibre avoided · water intensity — whichever are AVAILABLE for the selected window), each row = value + unit + a small **eye** control. **Unavailable KPIs are NOT rendered** (energy, Scope 2, secure-release today; any KPI that goes UNAVAILABLE for a window — e.g. paper cost with no cost set — disappears for that window rather than showing "unavailable"). Guard: the §17 rule "no KPI silently omitted — every declared code present in some state" stays TRUE in the API; the OMISSION is a rendering rule only, and a test asserts the API still declares every code while the tile renders only the available ones.
2. **The eye** opens that KPI's provenance from the record the API already carries (§17: evidence class MEASURED/CALCULATED/EQUIVALENT, method, source + factor + `unitBasis`, period, confidence, coverage) — a popover/drawer, keyboard-reachable, closes on Escape, one open at a time, both modes, brand tokens only. No new maths; the eye is a SURFACE over existing data. The registry table stays where it is (the eye links to its row).
3. **The Improvements pane** — larger, beside/below the tile — computed from the job rows for the selected window, every figure with its own eye, nothing invented:
   - **Avoided by duplex:** sheets avoided (= duplex sheets, each saving one sheet vs simplex), paper mass avoided (gsm-configured, CALCULATED), water / wood / tree-equivalent fibre avoided (the three paper factors, `unitBasis` asserted — the /1000 trap in S13_PAPER_KPI_DESIGN_NOTES.md), paper cost avoided (from the cost surface, consumed never redefined — RD-137).
   - **Avoided by mono:** cost avoided vs colour (colour and mono per-page cost from the cost settings); CO2e ONLY if a sourced factor exists in the registry — otherwise the row is NOT shown (Kam's addendum).
   - **Trend:** duplex rate and mono share, this window vs the previous window of the same length (the period discipline from RD-192/196 — honest sentences), with a small sparkline by month where the store span allows; no trend where there is no previous window (hidden, not "n/a").
   - **Remaining opportunity:** "if the remaining single-sided jobs had been duplex" → sheets / mass / water / cost — the what-if that drives action; same for colour→mono cost.
   - **Where to act:** the devices (and departments/users if the rows carry that dimension — measure first) with the highest single-sided and colour shares — a short ranked list. Only if the dimension exists in the data; otherwise omitted.
   - **Anything else the agent finds useful** is PROPOSED in the plan confirmation with the data it would rest on, not built unasked.
4. **Design first, for Kam's eye:** a rendered mock (both modes, brand tokens from `docs/STYLE_GUIDE.md` / BRAND.md only, no invented colour — style-guides-never-mixed) delivered as screenshots BEFORE the build proceeds past the mock; Kam's word or my ratification on the layout; then build → gate → the QA pass (browser) → completion → deploy on my GO.
5. **Integrity stand unchanged (Kam's s11 ruling):** provisional/not-reportable stays marked; no value laundered through provenance machinery; the eye is where "where does this number come from" is answered.

## Tickets
- The agent files the RD tickets at S24 start (one epic + sub-tasks: tile+eye · improvements pane · hide-unavailable rendering rule · mock) — Jira is the project's board; Wednesday never writes to it.

## Provenance for this file
- Kam's two messages: terminal, 13:1x AEST 2026-09-03, logged verbatim in 1_Project_Definition/Discovery/00_prompt-log.md (13:16 entries).
- KPI set + §17 evidence record: `git show 149e358:__tests__/sustainability-kpis.test.js` (test names), `docs/sustainability/S13_PAPER_KPI_DESIGN_NOTES.md` at 149e358 — read 13:1x.
