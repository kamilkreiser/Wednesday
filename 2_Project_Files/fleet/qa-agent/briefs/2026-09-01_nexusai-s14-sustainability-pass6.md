# QA Agent Invocation Brief — Datasec / NexusAI — s14 Sustainability refine round 5, PASS 6 (delta-only + the real-engine sweep as acceptance) (2026-09-01)

**R0 (client isolation):** this brief carries exactly one client's content (Datasec / NexusAI). Never name or reference any other client. Read only the paths named here.

**Read FIRST, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`, then your own project's `CLAUDE.md` and the `human-emulation-testing` skill. **Then read pass 5's own output** — `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-01-s14-sustainability-pass5/SUMMARY.md` + its three reports — every P5 id below is defined THERE with its repro; this pass is measured against it. **Then read the builder's delta notes:** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/ca98a55/QA_CHANGES.md` — the TOP section "pass 6 (round 5 delta)" with warnings A–D; the pass-5 table beneath it still stands — and the diff `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/ca98a55/QA_DIFF.patch` (delta `1f41edc..ca98a55`, 714 lines, 8 files; two commits: `b1cafaf` R5-1..R5-4 · `ca98a55` notes). **Driver: Playwright MCP from the start** (the Chrome MCP cannot deliver events to this page — proven in pass 1).

**Why this session exists (Kam, 2026-09-01 17:55, standing):** every change is reviewed by the testing agent — visually AND through code, in a real browser when browser-related — before Wednesday's completion check and any deploy. This is PASS 6: the builder (s14) has done round 5 against your pass-5 Majors. **Nothing is deployed; the demo still runs the pre-s12 image.** A deploy GO depends on this report — **this pass is the acceptance pass if it passes.**

**Your own counter-move from pass 5 is now the standing acceptance, and this pass runs it:** ONE real-engine sweep — set `body.dark-mode`, walk EVERY visible text node on all three pages, assert ≥ 4.5:1 from computed styles + composited background; assert `checkValidity() === false` for a known-bad cost string; light mode unhurt. The builder states plainly (warnings A–C) that R5-2 cannot be measured by jsdom (it does not honour `!important` — it measured that), R5-3 is arithmetic not a render, and R5-1 was checked in Node's `v`-mode only. **Those three sentences are the whole reason you exist tonight.**

---

## 1. Target
- **Client / Project:** Datasec / NexusAI ("NexusAI Print Analytics" — Node/Express backend, vanilla JS front end, Bootstrap 5.3.0 + Icons).
- **Running target:** `http://127.0.0.1:3015/` — a LOCAL run of commit **`ca98a55`** (branch `rd-136-nga-defaults-s12`) from the worktree above, **PID 24637**, data dir `qa-data/` inside the worktree, seeded 1,445 rows / 1,187 print, span 2026-01-30 → 2026-04-29 (the same fixture as passes 4 and 5), paper cost `0.011`, money tile 136.345. **Same commit as the branch under review, NOT the demo image** — say exactly that in the report; never write that demo was tested. Verified from Wednesday's seat at 23:3x AEST: `git ls-remote` branch head `ca98a55f4`; worktree HEAD `ca98a55f4`; `lsof` PID 24637 cwd = that worktree; `curl /api/health` 200 (`version 2.0.1`) in 2 ms; `GET /api/settings/costs` → `costPerSheetPaper 0.011`; the served `settings.html` carries `pattern="[+\-]?([0-9]+(\.[0-9]+)?|\.[0-9]+)"` ×6. **`:3013` and `:3014` are RETIRED (HTTP 000) — every measurement is at :3015.**
- **Isolation:** re-verify yourself as in pass 5 (cwd + `GET /api/settings/costs` = 0.011 + `/api/setup/status` storageStatus.dataDir + `$HOME/data/settings.json` sha before/after). The builder says the script verified it; that is its claim.
- **Environment identity:** local, `NODE_ENV=development`, auth **OPEN by design**. **Fingerprint the browser** against this Mac before trusting "localhost" (`navigator.hardwareConcurrency` = `sysctl -n hw.ncpu`, 28).
- **Production?:** NO. Nothing you touch reaches a deployed instance.

## 2. What changed since pass 5 (the builder's claims — inputs to falsify, not evidence)
| R5 | pass-5 id | builder's claim |
|---|---|---|
| R5-1 | **P5-03 Major** | dash escaped in `DECIMAL_PATTERN_SOURCE`; served attribute `[+\-]?([0-9]+(\.[0-9]+)?|\.[0-9]+)`; the test now compiles the source with the `v` flag and asserts it compiles |
| R5-2 | **P5-02 Major** | `!important` on all six `body.dark-mode .text-*-emphasis` rules; guard is SOURCE-LEVEL (declarations carry `!important`) + a test that PINS jsdom's `!important` blindness — **the cascade result is unmeasured by the builder** |
| R5-3 | **P5-01 Major** | 78 dark rules for first-run-setup's own surfaces (page, tab strip, cards, component rows, steps, icons, badges, the four semantic tints, code, controls); worst computed text pair 7.21:1; tint borders ≥ 3:1 — **arithmetic + static analysis, not a render** |
| R5-4 | P5-05 Minor | the R4-6 cache test drives the REAL `JsonStorage` over a real directory; both call-count controls spy on that instance; also asserts JsonStorage resolved to the directory it was handed |
| P5-04 | Minor | **NOT fixed — RD-156 filed (Medium)**; do not re-file. Consequence: R4-8's "clear the cost" step cannot be performed from the UI |
- Suite at this head: `npm run verify` → `PASS 837/837 across 36 suites` (pass 5: 815). A green suite is the builder's claim, not yours — and every one of the last three passes found Majors above a green suite.
- New guards the builder says it proved to fail: the `v`-compile check, the `!important` declaration check, a malformed-hex check (it wrote `#665river` by hand into a shipped stylesheet once this round — a browser drops the whole declaration silently; check the shipped stylesheets carry no such value NOW).
- Carried, do not re-file: RD-147, RD-148, RD-150, RD-151, RD-152, RD-154, RD-155, RD-156.

## 3. Scope — DELTA ONLY, FAIL condition first every time
- **(a) Per-id verdict table (P5-01..P5-05 → FIXED / NOT FIXED / REGRESSED / NOT VERIFIABLE-with-reason)** using pass 5's own repro per id, then the POSITIVE control (the legitimate case still works: `0.011` and `-0.05` still pass `checkValidity()`; `-0.05` still reaches the server and returns the NEGATIVES message; light mode still 296 lines / 0 failures on the Sustainability tab; All Time still prices 136.345 / $136.35).
- **(b) THE ACCEPTANCE SWEEP — in a real browser, its own section, every number verbatim:** (i) `body.dark-mode` on `index.html`, `settings.html` (Settings → Sustainability tab open, All Time selected) and `first-run-setup.html` — walk EVERY visible text node, computed colour vs composited background, list every line < 4.5:1 with its selector; state the count of lines measured per page (pass 5: 296 / 69 / 67). **R5-3's bar: first-run-setup dark = ZERO failures across all 67+ visible lines** (light: unchanged — its 17 pre-existing failures are off-delta; if the count moved, say so). (ii) **R5-2: the six `.text-*-emphasis` classes in dark — computed colour on the factor registry's source caveats and, since five were latent, on a synthetic element of each class injected into the page — do they now win the cascade?** Report the six measured ratios. (iii) **R5-1: on the six cost boxes, `checkValidity() === false` for `zzz`, `12abc`, `0x10`, `"  "`, `"0."` and `=== true` for `0.011`, `-0.05`, `.5`; NO SyntaxError in the console on settings load (pass 5 saw one on every load); P4-07's `title` now reachable (type `abc`, read the tooltip).** Run your pass-5 negative control again (`willValidate`, `disabled`, and one string that cannot match by construction) so an all-true or all-false matrix is a measurement, not an inert probe. (iv) the three completion-check questions re-confirmed UNREGRESSED in their own short section: (1) empty default view PAPER COST unavailable-with-reason naming the span; (2) period sentences honest across the four windows; (3) the smoke assertion `getComputedStyle(document.body).color === rgb(232, 232, 232)` on all three pages.
- **(c) Regressions on the touched flows:** the six alert variants distinct in both modes (pass 5: zero twins); Retry both modes on a forced 500; the settings form round-trip; money 40.403 / 1239.5 / 0.5; the dashboard's changed panels dark (RD-147 `.table-title` 1.55 is carried — confirm, don't re-file).
- **(d) Through-code:** R5-4 — open `__tests__/auth-enforced-cache.test.js`: is the storage the real `JsonStorage` (import + construction over a real temp dir) with NO stub `getSetting` anywhere in the file; do the controls spy on that instance; does the resolved-dir assertion exist. R5-1 — open the decimal test: does it compile with the `v` flag and assert compilation; is the served `pattern` genuinely the exported constant (one source). R5-2 — the `!important` guard and the jsdom-limitation pin: can each fail (sabotage in a scratch copy, never the repo). The malformed-hex check: scope and a sabotage. **R5-3's 78 rules: is the scope derivation (stylesheet ∩ classes in the HTML) complete — pick five classes the page renders and confirm each has a dark counterpart; name any it missed.**
- **Out of scope / do NOT touch:** the demo; enabling SCIM (`/scim/v2/Users` → 401 here — confirm once, read-only); destructive settings changes you cannot revert (record any; restore `0.011`); no repository writes; RD-147/148/150/151/152/154/155/156 (confirm, don't re-file); Q1 paper KPIs; AT runs and 200%/320 px reflow (list as NOT TESTED unless time inside the box); cross-browser spread of R5-1 (Chrome 152 only — state it; one Safari/Firefox check is welcome if trivially available, not required).

## 4. Credentials (POINTER ONLY)
- **None needed:** open mode. A login page on the surface = STOP and report.
- **Personas:** a real-browser contrast instrument for (b)(i)–(ii); Marcus (sceptical finance reader) for (b)(iii) + (c); a code-reviewer stance for (d).

## 5. State-mutation & cleanup
- Revert-what-you-change; exclude-and-report anything else. Known residue: `*_updated_at` timestamps. Restore the pre-set cost `0.011`; remove `localStorage.darkMode` at session end; the same three capture-layer interventions you disclosed in pass 5 are acceptable if disclosed again.

## 6. Output boundary (fixed)
- Findings, report, recommendations ONLY. No code, tests, fixtures, tickets or config changes. Fix-shape + regression test in prose, per finding.

## 7. Known-fragile / known-changed
- Every fix is a contrast, cascade-precedence, regex-dialect or test-instrument change — the risk is a dark rule that hurt light, an `!important` that now overrides a legitimately coloured element elsewhere, a pattern that now over-refuses a legitimate cost (`.5`? `+0.02`? `1e3` should still be refused), a first-run page whose dark rules break its light layout. Positive control on each.
- Carry, do not rediscover: ENERGY KWH / SCOPE2 / SECURE RELEASE unavailable by design; RD-139 row cap unexercisable at the seeded size; RD-143..156 all filed.

## 8. Logistics
- **Time-box:** ~45 minutes + the diff/test reads; stop when findings repeat.
- **Findings sink:** `projects/nexusai/reports/2026-09-01-s14-sustainability-pass6/` + `SUMMARY.md` ranked by severity, with the per-P5-id verdict table, **the acceptance sweep as its own section with per-page line counts and every failing line**, the three completion-check answers, the NOT-TESTED list at the same weight, and the verdict line "PASS for deploy / PASS with findings / FAIL". Wednesday reads the files; no tickets from you.
- **Signal when done:** end your turn with the summary path on its own last line.
- **Escalation:** `wednesday-agent@agentmail.to`, subject `[QA -> Wednesday] QUESTION: <topic>`, or the top of `SUMMARY.md` and continue on the safest reading. Approval-class ALWAYS pauses.

---

PROVENANCE:
- Pass-5 verdict (PASS with findings; P5-01/02/03 Major, P5-04/05 Minor; the three completion answers; the counter-move) | pass-5 SUMMARY.md (path above) as read by Wednesday 23:2x AEST | read 2026-09-01
- The R5 set, head ca98a55, PID 24637 / :3015 / worktree / 837/837 / RD-156 / warnings A–D / :3013 + :3014 retired | s14 STATUS "QA SURFACE UP (pass 6)" 2026-09-01T13:35:04Z in wednesday-agent@ + `qa-worktrees/ca98a55/QA_CHANGES.md` top section | read 2026-09-01
- Delta commits b1cafaf · ca98a55; QA_DIFF.patch 714 lines | `git -C <worktree> log --oneline 1f41edc..ca98a55` + `wc -l`, Wednesday's seat 23:3x | read 2026-09-01
- Surface 200 (`version 2.0.1`) at :3015 in 2 ms; :3013/:3014 HTTP 000; PID 24637 cwd = the ca98a55 worktree (`lsof`); worktree HEAD ca98a55f4; branch head ca98a55f4 on origin; costs → 0.011; served pattern escaped ×6 | Wednesday's own curl + `lsof` + `git rev-parse` + `git ls-remote` + `grep` 23:3x AEST | read 2026-09-01
- Kam's standing QA-gate process + "completion, not the same test" | dashboard chat 2026-09-01T17:55:18 + 17:55:45 AEST | read 2026-09-01
