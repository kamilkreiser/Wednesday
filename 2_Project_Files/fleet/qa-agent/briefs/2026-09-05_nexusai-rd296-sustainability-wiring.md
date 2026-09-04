# QA Agent Invocation Brief — Datasec / NexusAI, RD-296 Sustainability log-source wiring (through-code + real-browser pass)

**R0 (client isolation):** this brief carries exactly one client's content — Datasec / NexusAI. Do not name or reference any other client, in the report or anywhere else.

## Charter (read first, in full)

`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`

Read it end-to-end before running anything. This brief supplies only WHAT and WHERE.

## 1. Target
- **Client / Project:** Datasec / NexusAI
- **Source tree (read-only, for root-causing):** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/2_Project_Files`
- **Branch under test:** `rd-136-nga-defaults-s12` at **`7147a4a8f6de14d98d4ee804ad6e5cacb4a078b3`** — verified as that branch's head at origin by Wednesday with `git ls-remote origin refs/heads/rd-136-nga-defaults-s12` at 2026-09-05 09:0x AEST. Previous head b77feea.
- **Running target:** a LOCAL run of that exact commit, which YOU stand up in your own worktree: `./scripts/qa-surface-up.sh 7147a4a 3111` → `http://127.0.0.1:3111/` (open mode, no auth shim; Sustainability is the 8th tab; its log lands at `qa-worktrees/7147a4a/qa-data/qa-surface-3111.log`). **Environment identity: LOCAL DEV, non-production; the surface has NO Log Analytics workspace configured, so it exercises the SQLite branch of the selector only.** If port 3111 is taken, pick another free port in the 31xx range and say so.
- **Production?** NO. Nothing in this pass touches the Azure demo or any deployed revision. **If any step would reach a deployed surface or make an outbound authenticated call to a real Log Analytics workspace, stop and mail Wednesday.** In particular: do NOT drive the synthetic-feed path — RD-118 records that it makes live authenticated queries into a real workspace.

## 2. Spec / DoD being tested against

**These are the BUILDER'S CLAIMS from its READY FOR QA mail to Wednesday at 2026-09-04T22:52Z. They are inputs to FALSIFY, not evidence.** Wednesday ratified the SHAPE of the report and has verified only the branch head at origin; correctness is this pass's question.

**Ticket:** RD-296 (Jira, project RD) — "The Sustainability tab BYPASSES the configured-log-source selector". **Kam's ruling 2026-09-04 15:10: build it — wire Sustainability to the same configured log sources as every other tab, knowing it lights no new tile and `SECURE_RELEASE_AVOIDED` stays dark structurally.**

**Claims:**
1. `backend/services/sustainability/rowSource.js` (NEW) is the reader; `backend/server.js`'s selector now reports its source and the mount injects the reader; `backend/routes/sustainability.js` adds `dataSource` to the KPI response. **The tab now reads THROUGH the module-level selector like every other tab.**
2. Runtime proof offered: one `/api/sustainability/kpis` request adds exactly 2 "Using local database (Azure Log Analytics not enabled)" lines to the surface log (window read + RD-267's previous-window read); one `/api/health` adds 0; the line is emitted ONLY by the selector, not by the SQLite reader. `dataSource: "local-database"` on the response.
3. The read is `{limit, from, to}`; the window is applied on the job's own timestamp; `from`/`to` still go down so SQLite keeps filtering in SQL (RD-139 not undone). **Truncation is measured on the RAW read, before the window filter.**
4. **A period→timespan adapter was built then DELETED**: `_executeQueryDirect` forwards `options.timespan` verbatim; every caller passes `'Nd'`; the file's own comment says the API wants ISO-8601 (`P30D`). Builder chose not to be the first caller to depend on that mismatch (filed RD-305, unmeasured against a live workspace).
5. **All four LAW parsers in `azureLogAnalytics.js` emit every one of the 11 fields the sustainability services read** — "no row-shape adapter needed", with a control the builder says proves the check reports a miss.
6. Six KPIs lit, three dark — the same sets as before; `SECURE_RELEASE_AVOIDED` is an unconditional `unavailable()` push at `kpis.js:481`. The tab says so truthfully and does not error.
7. `__tests__/sustainability-row-source.test.js` (NEW, 21 tests); `__tests__/sustainability-period.test.js` now uses the real factory instead of a hand-written copy of `getRows`. Gate claim: `PASS — 1528/1528 across 90` (counts file regenerated in the same commit). **No UI file touched.**
8. `.gitignore` gained one line for `data/.machine-id` (RD-307). The builder states no test reads `.gitignore`.

## 3. Scope

**Charter:** a through-code pass PLUS a real-browser pass on RD-296 at `7147a4a`, hunting for the classes this fleet keeps paying for — a wiring claim proved by a log line that something else could also emit, a "same as every other tab" claim that is same-in-name only, a window filter that changes the figures a user sees, a green suite whose fixtures never enter the product's path, and a deletion (the adapter) whose absence breaks the branch nobody can render here.

**In scope:**
- The RD-296 diff (`git diff b77feea..7147a4a`) — every file it names, read as well as run.
- **Claim 1/2 — REACH and IDENTITY:** enumerate every emitter of the "Using local database" line yourself; enumerate every path by which Sustainability rows can be read (is there still a direct SQLite read anywhere in the sustainability services, `getDataSpan` included — the builder says RD-304 is exactly that, confirm its scope); confirm at runtime on the local surface (**MEASURED AT RUNTIME**) with your own request/log correlation, including a control request.
- **Claim 3 — FIGURES:** do the six lit KPI figures on the tab at `7147a4a` equal the figures at `b77feea` on the same seeded data? Stand both up if you can (two worktrees, two ports) and diff the `/api/sustainability/kpis` JSON. Any figure that moved is a finding, even if "right", because the ticket promised no visible change on a SQLite deployment. Check the window edges (a job exactly at `from`, exactly at `to`) and the truncation reporting on a raw read that exceeds the cap.
- **Claim 5 — the 11-field parity:** re-derive it independently from the four parsers and the sustainability services' reads; do not accept the builder's list. State your evidence class.
- **Claim 4 — the deleted adapter:** READ ONLY is all that is possible here; say what a live-workspace probe would need to settle RD-305 and which of the three cases the code as written assumes.
- **Claim 7 — the tests:** read the 21 new tests; do they drive the product's path (the selector + the reader) or a hand-built stand-in? Re-derive one red-proof: break the wiring (a tamper you RESTORE byte-identically, hash proven) and confirm which tests go red.
- **Browser pass (REAL browser, Claude-in-Chrome, both modes):** the Sustainability tab renders at `7147a4a` with 0 console errors; six lit / three dark as claimed; the "Read before using these numbers" note present; dark mode set the product's own way (`localStorage 'darkMode'`); nothing off-guide — no colour was added, confirm that by diff, not by eye.
- **Claim 8:** confirm no test reads `.gitignore`; confirm `data/.machine-id` is untracked and now ignored; **do not move, copy, read the contents of, or delete `data/.machine-id`** — it is a key-derivation seed and its disposition is Kam's (RD-307).

**Out of scope / do NOT touch:**
- **RD-245 / RD-155** — the F-1/F-3 round is IN PROGRESS in the builder's own session on the SAME branch; the builder may push new commits above `7147a4a` while you work. **Pin your worktree to `7147a4a` and test that SHA only**; report the branch head you observe at the end so Wednesday knows whether the gated SHA is still the head.
- RD-303, the tracked `4_Credentials/.azure/` files — awaiting Kam's ruling; do not report them as a new finding.
- Anything deployed. The synthetic feed. Any other client's tree.

## 4. Credentials (POINTER ONLY — never values)
- `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/4_Credentials/.env` — source it only if `qa-surface-up.sh` needs it; never echo a value, never copy one into a report. **Do not go looking for Log Analytics credentials; there are none in scope for this pass.**
- No personas required; the local surface is open mode.

## 5. State-mutation & cleanup
- **Pattern: exclude-and-report-only.** No accounts, no shared state.
- **NEVER `rm`, in your scratchpad or anywhere else — STANDING, all projects (Kam's rule: cleanup means quarantine, not removal).** Build each attempt in its own `mktemp -d` and abandon the old one; if a path must be cleared, move it into a dated `_quarantine_YYYY-MM-DD/` beside it and say so. Guard every expansion (`"${DIR:?unset}/…"`). If cleanup starts costing budget, stop building the fixture and report the affected checks as NOT RUN with the blocker named.
- **Restore any file you tamper with byte-identically and prove it with a hash.**
- The worktree you create under `qa-worktrees/` is the project's sanctioned pattern (the builder's own script creates it); leave it in place and name it in the report.

## 6. Output boundary (fixed — not a choice)
**Findings, reports and recommendations ONLY.** Make NO changes of any kind — no code, no tests, no fixtures, no tickets, no config. Describe the fix-shape and the regression test the owner should add, in prose. The project's own agent authors and commits everything. (Kam ruling 2026-08-11, absolute.)

## 6a. EVIDENCE CLASS ON EVERY FINDING THAT RECOMMENDS AN ACTION (mandatory)
**Any finding that recommends an ACTION carries its evidence class inline, in these words:** **`MEASURED AT RUNTIME`** (driven and observed — name the probe) · **`PROBED`** (an adjacent call; say what it does NOT cover) · **`READ ONLY`** (from source/spec/config, not executed). A recommendation without one is incomplete. **The corollary bites here:** `1528/1528 across 90` is a claim about a suite; the LAW branch of this change cannot be rendered in this environment and any statement about it is READ ONLY at best — say so in those words.

## 7. Known-fragile / known-changed areas
- **Known-fragile:** this project's guards have repeatedly been red-proofed in the shape of the defect that motivated them and shipped over a corpus of a different shape (RD-245's F-1/F-3 is the live example). The jsdom instrument cluster (RD-163/201/199) is a known open gap — if a contrast number matters to you, it is suspect.
- **Recent changes — do NOT flag as new:** RD-291, RD-294, RD-299, RD-301, RD-302, RD-282, RD-155 (Testing), F-2's fix at 1c5d3f7 (its own re-gate is deliberately batched with RD-245 — not yours today), RD-292's date humanising, RD-297 (one prose date left deliberately — carded for Kam, not a finding).
- **Known open gaps carried:** RD-304 (getDataSpan SQLite-only), RD-305 (timespan format), RD-306 (no server-side job-time filter on the LAW path — 10,000 cap), RD-307 (`.machine-id`). Confirm or sharpen their scope if you can; do not re-discover them as new.
- The QA project still has no launcher entry, no inbox and no wrap hook — Wednesday runs this hop by hand and reads your report from your own project tree.

## 8. Logistics
- **Session time-box:** one bounded pass; if the browser half cannot be completed, deliver the through-code half with the browser checks listed as NOT RUN.
- **Findings sink:** your report under your own project tree at `projects/nexusai/reports/2026-09-05-s33-rd296-through-code-and-browser/report.md` with probe scripts in `evidence/` beside it. Findings numbered F-1…; severity Blocker/Major/Minor; each with its evidence class.
- **Escalation path:** back through Wednesday (`wednesday-agent@agentmail.to`, QUESTION subject) for anything this brief does not answer; approval-class items ALWAYS pause for Kam. Priority on any finding is the humans' call, never yours.
- **When done:** mail Wednesday, subject `[QA -> Wednesday] RD-296 through-code + browser pass @ 7147a4a` — BLUF first, the report's path, findings by severity, the NOT-TESTED list, the branch head you observed at the end.

---

PROVENANCE:
- 7147a4a8f6de is the head of rd-136-nga-defaults-s12 at origin, above b77feea | `git ls-remote origin refs/heads/rd-136-nga-defaults-s12` + `git log --oneline -4` on the NexusAI repo (read-only) | read 2026-09-05
- Every claim in §2, the surface command, the four filed tickets, the "no UI file touched" statement, the synthetic-feed caution | builder's mail `[Datasec/NexusAI -> Wednesday] READY FOR QA: RD-296 @ 7147a4a — gate PASS 1528/90, both-mode screenshots, and a timespan adapter I built then deleted` at wednesday-agent@agentmail.to, 2026-09-04T22:52Z | read 2026-09-05
- Kam's build-it ruling on RD-296 (2026-09-04 15:10) and "no new tile lights; SECURE_RELEASE_AVOIDED stays dark structurally" | Wednesday's 0_Brain/tasks/NEXT-PICKUP.md (09-04 version §2c) — Wednesday's project, not the QA project's | read 2026-09-05
- RD-296 In Progress/Highest; RD-245 In Progress/High; RD-303 To Do/High | Jira REST search, project RD | read 2026-09-05
- RD-245's F-1/F-3 round in progress on the same branch (the pin hazard) | Wednesday's S33 brief and the builder's plan-confirmation mail 2026-09-04T22:20Z — Wednesday's project, not the QA project's | read 2026-09-05
- Rendered tab, both modes, six lit metrics and the energy note present at 7147a4a | `2_Project_Files/tests/screenshots/rd296-sustainability-{light,dark}-7147a4a.png` in the NexusAI tree, viewed by Wednesday | read 2026-09-05
