# QA Agent Invocation Brief — Datasec / NexusAI, HARNESS PASS 1 (tier 1, through-code): `rd-163-201-instrument-s37` @ `7df675b` — the jsdom contrast harness now REPORTS what it cannot measure, with a committed per-page ceiling that fails on drift and a staleness check; the cross-engine instrument landed on the campaign line

**TIER 1 (full gate — this is the INSTRUMENT every brand ruling on this campaign rests on; a harness that reports wrong is a false green for every ticket that cites it) — ROUND 1 of the harness class.** Browser leg: through-code only for the harness itself; the ONE real-engine cell is the cross-engine instrument's own run (it drives Chromium) — you run it, not a page.

**R0 (client isolation):** exactly one client's content — Datasec / NexusAI. Report under `projects/nexusai/`.

## Charter (read first, in full)
`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`.

## 1. Target
- **Client / Project:** Datasec / NexusAI. **Source tree (read-only):** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/2_Project_Files`. The builder S37 is LIVE in that tree — never touch its checkout or worktrees. **Work from YOUR OWN worktree** at `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/<sha>` (OUTSIDE jest's rootDir or excluded — the doubled-corpus trap).
- **Branch under test:** `rd-163-201-instrument-s37` at **`7df675bf61febb8e9fac009d6fcf782e62908d95`** — verified at origin by Wednesday (`git ls-remote`, no fetch; a local commit object), **2 commits above the campaign tip `ec8506a`** (`f61a7d1` "pin what the jsdom harness cannot measure, with the browser's answer beside it" — S35's instrument rebased; `7df675b` "the harness reports what it cannot see, with a ceiling that fails on drift"). Diff `ec8506a..7df675b`: **5 files +603/−3** — `__tests__/helpers/dom.js` (M), `__tests__/jsdom-instrument-limits.test.js` (A), `scripts/instrument-cross-engine.js` (A), `scripts/jsdom-unmeasured-ceiling.json` (A), `scripts/verify-expected-counts.json` (M). UNMERGED; nothing user-facing changed (no screenshots to expect).
- **Environment:** LOCAL, the jest suite + the cross-engine instrument's own Chromium run; no deploy, no demo, no board writes.

## 2. The builder's claims at `7df675b` — inputs to FALSIFY (S37's READY mail 2026-09-05T12:18:38Z, read whole by Wednesday; the render-closure report 12:09:34Z for the real-engine numbers)
1. **`measurableTextNodes()`** is exported from `helpers/dom.js`, documented, and **consumed by NOTHING** (deliberately — the consumer half was built, turned the gate RED, and was REVERTED; see claim 6). Verify the revert is complete: no sweep calls it; `unmeasurableNodes()` / `systemColorProvenance()` remain report-only.
2. **The ceiling file** `scripts/jsdom-unmeasured-ceiling.json`: 24/974 (first-run-setup) · 27/374 · 11/166 — exceeding FAILS, equal-or-lower PASSES; every page AT its ceiling today (nothing fails on landing); its `_lower_bound` field states the numbers UNDERSTATE the blind spot (28 var()-attributable flips vs 24 keyword nodes).
3. **The staleness check** (S37's addition, ACCEPTED by Wednesday): a page more than 2 UNDER its ceiling FAILS — so a ceiling nobody lowers cannot go stale silently.
4. **Three controls, each proved able to FAIL before its green was believed:** (A) the filter is not a no-op — 974→950, 374→347, 166→155, excluding exactly 24/27/11; (B) ceiling 24→23 → RED `Expected: <= 23, Received: 24`; (C) ceiling 24→30 → the staleness check RED `Expected: >= 28, Received: 24`. Both temporary edits restored and the restoration verified.
5. **Gate** `VERDICT: PASS — 1769/1769 across 105` (+3 tests over 1766 from `f61a7d1`; +13/+1 over the campaign tip's 1756/104 — S37's arithmetic; the counts file re-derived, not auto-merged; the commit-message `#`-line hazard handled with `--cleanup=verbatim` on `f61a7d1`).
6. **The consumer's measured RED (the reason it is OUT):** wiring the four sweeps to `measurableTextNodes()` → 5 tests RED in 3 suites: (a) `dark-ground-luminance`'s *"CONTROL — the exclusions are firing"* went from >0 to ZERO (its population = exactly the filtered `ua-button-face` nodes); (b) R6-2/R6-3 assert the LIGHT failure set equals a recorded baseline and it SHRANK 77→72 and 136→129 — some unmeasurable nodes were recorded as FAILURES. **Wednesday wants the LISTS:** which 5 and which 7 rows (by selector) would leave those baselines, and why each is unmeasurable (var() unsubstituted / cascade-by-source-order / inherited fallback) — that is the input to the consumer's design round; you MEASURE it on your copy, you do not build the consumer.
7. **The cross-engine instrument** (`scripts/instrument-cross-engine.js`, S35's, now on the line): its headline numbers — 42 flips, 22 of them jsdom-pass/browser-fail — REPRODUCE in your worktree; and the ONE-element proof from the render pass (light wizard navbar: Chromium 2.675 vs jsdom 4.501, `.navbar .nav-link`, two compounding engine limits) reproduces through this instrument on the same selector.

## 3. Scope — through-code, the instrument's own runs, and the hunt
- **Read the diff whole.** State in your own words what the harness now reports, where the ceiling is read, how the staleness check is computed, and that no sweep consumes the filter.
- **Reproduce claims 2–5 from your worktree:** run the ceiling test; then the three controls A/B/C with SET and COUNT predicted before each (edit your copy of the ceiling file; restore by hash); confirm the `_lower_bound` numbers by running the instrument (28 vs 24).
- **Claim 6 — measure the two lists** (the 5 + 7 rows) by wiring the consumer on YOUR copy only, diffing the failure sets by name against the recorded baselines, classifying each departing row by its engine limit; then revert your copy (restore by hash). Confirm the `dark-ground-luminance` control's population is exactly the filtered set (so the design's "own population" fix is the right shape) — or say what else feeds it.
- **Claim 7 — the instrument:** run it; reproduce 42 / 22 (or report the numbers you get and why they differ — the tip moved since S35's run); the one-element proof on `.navbar .nav-link` in light with both engines' figures.
- **The hunt on `dom.js`'s +hunks:** does the filter change any EXISTING helper's return (a shared helper narrowed silently — the RD-304 "span test narrowed a leg" shape); is the ceiling keyed by a page NAME that a rename would silently orphan (a page missing from the file = no ceiling = no check); does the staleness check count pages with a ceiling of 0 correctly (a `>= -2` that can never fail); the `#`-line commit-message hazard — check `f61a7d1`'s message is byte-complete against S35's `59b17aa`.
- **Gate re-run** from your worktree at `7df675b`; counts honest against the committed file; console n/a; palette n/a.

**Out of scope:** the consumer's BUILD (a designed round follows); RD-332/RD-333; any deploy; the demo; the builder's tree; board writes.

## 4–6. Credentials / state / boundary — as before
`.env` untouched, never echoed; own worktree; **NEVER `rm`**; tampers on your copies only, restored by hash; **predict every tamper's failing SET and COUNT before running.** Findings only. Porcelain in the builder's tree at START and at END, separately.

## 7. Known-fragile / carried
A worktree inside jest's rootDir doubles the corpus; the gate's expectation echo goes to a FILE, not through `tail`; a check with no possible failure branch is decoration — prove each control can fail before believing its green; a rebase strips commit-message lines beginning with `#`; a relayed finding is quoted verbatim in this brief — where Wednesday paraphrased, the builder's mail is the source.

## 8. Logistics
- **Time-box:** narrow — the diff read, claims 2–5 reproduced with predictions, the two lists measured and classified, the instrument run with the one-element proof, the hunt, the gate. Aim ~45 min.
- **Findings sink:** `projects/nexusai/reports/2026-09-05-s37-harness-pass1-7df675b/report.md` + `evidence/` (the two lists as their own file).
- **Escalation:** through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject). Approval-class pauses for Kam.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] NexusAI HARNESS PASS 1 @ 7df675b (tier 1)` — BLUF (PASS or NO GO for merge in the first line), report path, claims table, the controls' predicted-vs-measured, THE TWO LISTS, the instrument's numbers, new findings, NOT-TESTED, the head observed at the end.

---

PROVENANCE:
- `rd-163-201-instrument-s37` = `7df675bf…` at origin; 0 behind / 2 ahead of `ec8506a`; 5 files +603/−3 by `--name-status`/`--stat`; the two commit subjects | `git ls-remote --heads origin`, `git cat-file -t`, `git rev-list --left-right --count`, `git diff`, `git log` on LOCAL objects from Wednesday's seat, no fetch | read 2026-09-05 22:2x
- Claims 1–6 (the exported helper consumed by nothing; the ceiling numbers and `_lower_bound`; the staleness check; controls A/B/C with their exact messages; 1769/105; the consumer's RED — the killed control, 77→72, 136→129; the revert) | S37's READY mail 2026-09-05T12:18:38Z (7,529 chars, read whole) — QUOTED where the brief states a figure | read 2026-09-05 22:2x
- Claim 7's numbers (42 flips / 22 jsdom-pass-browser-fail; the one-element proof 2.675 vs 4.501 on `.navbar .nav-link`) | S37's step-1 mail 12:00:33Z (S35's instrument figures) + `[QA -> Wednesday] NexusAI RENDER-CLOSURE @ ec8506a (browser)` 12:09:34Z cell 3 | read 2026-09-05 22:0x
- The consumer ruled OUT and the design round's shape (own population for the control; named re-baselining) | Wednesday's own RULING 12:2x (`briefs_staged/S37_item3_consumer_ruling.md`, Wednesday's tree) | read 2026-09-05 22:2x
- TIER 1 / ROUND 1 | Kam's 2026-09-05 20:19 grant, /Volumes/DevMASTER/WEDNESDAY/0_Brain/learnings/2026-09-05_qa-gate-tiers-and-the-two-nogo-cap.md — the instrument the brand rulings rest on | read 2026-09-05 21:0x
- scope: pass 1 on `ec8506a..7df675b` only — the harness's report half, the ceiling + staleness, the controls, the two lists measured (not built), the instrument's run, the hunt, the gate; the consumer's build, RD-332/333, deploys OUT | this brief's §3, written by Wednesday | read 2026-09-05 22:2x

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-05 22:2x
(checked against the ruling this gate serves: "consumer OUT" vs claim 6's "measure the two lists by wiring the consumer on YOUR copy" — a measurement on the tester's copy, reverted, not a build; stated. Figures attributed to the builder's mail where they are its; the one relayed tester finding (the selector) is NOT in this brief — struck.)
