# QA Agent Invocation Brief — Datasec / NexusAI — s13 Sustainability refine round 2, PASS 3 (delta-only) (2026-09-01)

**R0 (client isolation):** this brief carries exactly one client's content (Datasec / NexusAI). Never name or reference any other client. Read only the paths named here.

**Read FIRST, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`, then your own project's `CLAUDE.md` and the `human-emulation-testing` skill. **Then read pass 2's own output** — `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-01-s12-sustainability-pass2/SUMMARY.md` + `report-01/02/03` — every P2 id below is defined THERE, with its repro; this pass is measured against it. **Then read the builder's own delta notes:** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/c1fe9ea/QA_CHANGES.md` (one row per P2 id + NINE warnings written for you — read all nine before you touch the page) and the diff `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/c1fe9ea/QA_DIFF.patch` (delta `9671040..c1fe9ea`, lockfile excluded, 3,134 lines). **Driver: Playwright MCP from the start** (pass 1 proved the Chrome MCP cannot deliver events to this page — do not re-spend that).

**Why this session exists (Kam, 2026-09-01 17:55, standing):** every change is reviewed by the testing agent — visually AND through code, in a real browser when browser-related — before Wednesday's completion check and any deploy. This is PASS 3: the builder (a fresh session, s13) has fixed the pass-2 P2 findings. **Nothing is deployed; the demo still runs the pre-s12 image.** A deploy GO depends on this report.

---

## 1. Target
- **Client / Project:** Datasec / NexusAI ("NexusAI Print Analytics" — Node/Express backend, vanilla JS front end, Bootstrap Icons).
- **Running target:** `http://127.0.0.1:3012/` — a LOCAL run of commit **`c1fe9ea`** (branch `rd-136-nga-defaults-s12`) from the worktree above, PID 26584, data dir `qa-data/` inside the worktree, seeded **1,445 rows / 1,187 print, span 2026-01-30 → 2026-04-29** (identical to your pass-2 fixture). **Same commit as the branch under review, NOT the demo image** — say exactly that in the report; never write that demo was tested. Verified from Wednesday's seat at 20:4x AEST: `curl` 200 in 4 ms; worktree HEAD `c1fe9ea`; pass-2's :3011 is retired (HTTP 000).
- **Environment identity:** local, `NODE_ENV=development`, auth **OPEN by design**. **Fingerprint the browser** against this Mac before trusting "localhost" (`navigator.hardwareConcurrency` 28 = `sysctl -n hw.ncpu`).
- **Production?:** NO. Nothing you touch reaches a deployed instance.

## 2. What changed since pass 2 (the builder's claims — inputs to falsify, not evidence)
- **Fixed (the builder's set): P2-01 · 02 · 03 · 04 · 05 · 05a · 07 · 08 · 09 · 10 · 11 · 12 · 13 · 14** — fourteen of fifteen. Per-id claims + file pointers are in `QA_CHANGES.md`.
- **Deliberately NOT fixed: P2-06** (no revoke control / issued-at in the Entra provisioning UI) → deferred to **RD-148** (High, linked RD-135). **Do not re-file; DO confirm it is unchanged and still tracked.**
- **Filed, not fixed: RD-147** (`.table-title` 1.55:1 dark-mode, 16 headings, pre-existing, dashboard-wide; linked RD-144/145). Do not re-file.
- Suite at this head: `npm run verify` → `PASS 652/652 across 31 suites` (was 538/538 across 26). A green suite is the builder's claim, not yours.

## 2b. The builder's OWN warnings (all nine in QA_CHANGES.md — the four that decide this pass)
- **Auth is OPEN here, so P2-07's DENIAL cannot be exercised on this surface** — and a 403 here would be the REGRESSION: `requireAuth` calls `next()` with no `req.user` when auth is not enforced (server.js:2291), the gate enforces the role only once auth is enforced (the codebase idiom at server.js:752/:2929), fails closed on an unreadable store or an unwired caller. Prove P2-07 THROUGH CODE: read the router + the tests (fail-closed case; the open/enforced PAIR — either assertion alone is satisfied by a gate that is always on or always off). State plainly that runtime denial needs an auth-enforced instance.
- **The default Sustainability view shows "Unavailable" tiles, not zeros** (seeded span is outside Last 30 Days — that is SUS-04/05 working). **Select All Time or a custom range inside the span before judging any tile.** This caught pass 2.
- **A paper cost is pre-set (`costPerSheetPaper = 0.011`)**, so the money tile is exercisable immediately. Clearing it now means OMITTING the field — sending `null` is refused by design (P2-03 fix). The builder found the destructive path was the product's OWN Settings form (`parseFloat('')` → NaN → JSON `null` on every save with a blank box).
- **RD-143 bit the builder:** `DATA_DIR` only wins if the dir already holds a settings.json with ≥1 key (`{}` rejected) — `qa-data/settings.json` carries one inert scaffolding key `qaSurface`; ignore it. The seed env var does NOT run on this boot path (one call site, branch not taken) — the builder seeded via the product's own seeder; it has NOT filed that, pending a reachability question. Report what you observe; do not conclude about the env var.

## 2c. The builder's instrument notes (things its OWN tests got wrong first — test at the surface, not the suite)
- jsdom's CSSOM does not resolve `var()`: table cells measured transparent, so a contrast assertion PASSED on unfixed code until a known-answer probe caught it. **Your contrast numbers must come from a real browser's computed styles + composited background.**
- A `vendor-surface.css` check gave a false negative; the 250 ms debounce (P2-08) silently HOLLOWED the P2-05a tests (green while exercising no render) — caught by assertion time, re-proved by sabotage. **For P2-05a, prove node identity yourself** (`[role=status]` is the SAME node across two renders; diagnostics + Retry INSIDE it).
- jsdom lacks `setImmediate` (a winston false "broken component"). Irrelevant to you except: do not trust the suite's a11y greens.

## 3. Scope — DELTA ONLY
- **(a) VERIFY each P2 id in a per-id table (FIXED / NOT FIXED / REGRESSED / NOT VERIFIABLE-with-reason)** using pass 2's own repro for that id — state the FAIL condition first, re-run the repro, then run the POSITIVE control (the legitimate case still works: a populated window still prices — control value from the builder: All Time → `$136.345`; a valid cost still persists; a real 500 still surfaces `errorCode`; the API still 400s `INVERTED_PERIOD` when called directly while the UI answers an inverted pair locally).
- **The three questions Wednesday's completion check will ask of your report — answer them explicitly:** (1) on the EMPTY DEFAULT VIEW with a cost configured, is PAPER COST unavailable-with-a-reason that names the real data span (P2-01)? (2) is every empty-window period sentence honest — no fabricated single day, both ends stated for a closed window, "onwards"/"up to" for open ends, in the tile reason AND the Period line (P2-02)? (3) does every muted/diagnostic line in dark mode on the changed panels measure ≥ 4.5:1 in a real browser (P2-04/05)?
- **(b) REGRESSIONS on the touched flows:** the costs form round-trip (clear one box, save, the others survive; arrays/objects/`""`/`null` → 400 via API), the debounce (type From after To → calm in-panel sentence, not the red panel), the live region across a 500 + a Retry, the dark-mode override list (did fixing the surface break light mode? the builder claims a light-mode regression assertion — check the light theme too).
- **(c) THROUGH-CODE (SCIM, endpoint stays INERT — `/scim/v2/Users` answers 401 here, correct):** P2-07 (authorised, not just authenticated — see 2b), P2-09 (revoke verifies all three writes and names the one that did not persist), P2-10 (pre-dating tokens reported `scimTokenIssuedAtUnknown` + note, deliberately not backfilled — `GET /api/setup/entra-provisioning`), P2-11 (429 path audited under its own action; rate limit overridable in tests), P2-14 (F-4 assertion now compares VALUES across the three failure modes). Read the diff and the tests; do not enable anything; no probe beyond what the tests cover.
- **Out of scope / do NOT touch:** the demo; enabling SCIM; destructive settings changes you cannot revert (record any you make); no repository writes; RD-147/148 (confirm, don't re-file); Q1 paper KPIs (ruled a later round).

## 4. Credentials (POINTER ONLY)
- **None needed:** open mode. A login page on the surface = STOP and report.
- **Personas:** Marcus (the sceptical finance reader — periods/units/costs) for (a)+(b); a short a11y pass with a real-browser contrast instrument; a code-reviewer stance for (c).

## 5. State-mutation & cleanup
- Revert-what-you-change; exclude-and-report anything else. Known residue from earlier passes: `cost_per_sheet_paper_updated_at` (non-revertible timestamp) — expect it. Note any further residue you create; the pre-set cost `0.011` must be restored if you change it.

## 6. Output boundary (fixed)
- Findings, reports and recommendations ONLY. No code, tests, fixtures, tickets or config changes. Fix-shape + regression test in prose.

## 7. Known-fragile / known-changed
- Every fix is a period-honesty, validation, a11y-structure or authz change — the risk is over-rejection (a legitimate range/cost refused), a message naming the wrong condition, a dark fix that hurt light, or a debounce that swallows a real user action. Positive control on each.
- Carry, do not rediscover: ENERGY KWH / SCOPE2 / SECURE RELEASE unavailable by design; RD-139 row cap unexercisable at the seeded size (state it); RD-143 (builder-filed + commented tonight); RD-144/145/146/147/148 all filed.

## 8. Logistics
- **Time-box:** ~45 minutes + the diff/test reads; stop when findings repeat.
- **Findings sink:** `projects/nexusai/reports/2026-09-01-s13-sustainability-pass3/` + `SUMMARY.md` ranked by severity, with the per-P2-id verdict table, the three completion-check answers as their own short section, the NOT-TESTED list at the same weight, and the verdict line "PASS for deploy / PASS with findings / FAIL". Wednesday reads the files; no tickets from you.
- **Signal when done:** end your turn with the summary path on its own last line.
- **Escalation:** `wednesday-agent@agentmail.to`, subject `[QA -> Wednesday] QUESTION: <topic>`, or the top of `SUMMARY.md` and continue on the safest reading. Approval-class ALWAYS pauses.

---

PROVENANCE:
- Pass-2 verdict PASS-with-findings; P2-01..14 (+05a) definitions, repros, the "tested at the finding" pattern | pass-2 SUMMARY.md (path above), 208 lines, read from Wednesday's seat | read 2026-09-01
- The builder's fixed set (14/15), P2-06 → RD-148, RD-147 filed, 652/652, PID 26584 / :3012 / worktree c1fe9ea / seed 1,445/1,187 / cost 0.011 pre-set / open mode / P2-07 mechanism / RD-143 cause / seed call-site note | s13 STATUS "QA SURFACE UP (pass 3)" mail 2026-09-01T10:33:56Z in wednesday-agent@ | read 2026-09-01
- Per-id changes + the nine warnings + the parseFloat default-path finding | /Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/c1fe9ea/QA_CHANGES.md (8,100 B, 20:32) | read 2026-09-01
- Instrument notes (jsdom var(), vendor-surface.css, debounce-hollowed tests, setImmediate) | s13 STATUS mail 2026-09-01T10:20Z (items 4/5/8) as recorded in Wednesday's daily note 20:22 | read 2026-09-01
- Surface 200 in 0.004 s at :3012; :3011 HTTP 000; worktree HEAD c1fe9ea; branch head c1fe9eab8 | Wednesday's own curl + `git rev-parse` + `git ls-remote` 20:4x AEST | read 2026-09-01
- Kam's standing QA-gate process | dashboard chat 2026-09-01T17:55:18 + 17:55:45 AEST | read 2026-09-01
