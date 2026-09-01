# QA Agent Invocation Brief — Datasec / NexusAI — s12 Sustainability round 2, PASS 2 (fix round + SCIM commit) (2026-09-01)

**R0 (client isolation):** this brief carries exactly one client's content (Datasec / NexusAI). Never name or reference any other client. Read only the paths named here.

**Read FIRST, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`, then your own project's `CLAUDE.md` and the `human-emulation-testing` skill. **Then read pass 1's own output** — `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-01-s12-sustainability/SUMMARY.md` + `report-01/02/03` — that is the baseline this pass is measured against. **Driver note from pass 1: the Claude-in-Chrome MCP could not deliver events to this page (2.5× coordinate scaling; dispatched keys never arrived). Use the Playwright MCP from the start; do not re-spend time proving that.**

**Why this session exists (Kam, 2026-09-01 17:55, standing):** every change is reviewed by the testing agent — visually AND through code, in a real browser when browser-related — before Wednesday's completion check and any deploy. This is the SECOND pass of the gate's first live run: the builder has fixed the pass-1 findings, and one code-only commit (SCIM security fixes) has also landed on the branch since the pass-1 surface.

---

## 1. Target
- **Client / Project:** Datasec / NexusAI ("NexusAI Print Analytics" — Node/Express backend, vanilla JS front end, Bootstrap Icons).
- **Running target:** `http://127.0.0.1:3011/` — a LOCAL run of commit `9671040` (branch `rd-136-nga-defaults-s12`) stood up by the project's own agent from a fresh git worktree with a freshly seeded data directory (surface mail 2026-09-01T09:05:07Z). **Same commit as the branch under review, NOT the demo image.** Say exactly that in your report; never write that demo was tested.
- **Environment identity:** local, `NODE_ENV=development`, auth OPEN by design. **Fingerprint the browser** against this Mac before trusting "localhost" (pass 1 did: `navigator.hardwareConcurrency` 28 = `sysctl -n hw.ncpu`).
- **Production?:** NO. Nothing you touch reaches a deployed instance.

## 2. What changed since pass 1 (the builder's claims — inputs to falsify, not evidence)
- **Fix commits** for the pass-1 findings, by SUS-id: **SUS-01 · 02 · 03 · 04 · 05 · 06 · 07 · 08 · 09 · 11 · 12 · 13 · 14 · 15 · 16 · 18 + Q2 (commits 6587569 fix round, 9671040 SUS-03 follow-up)** — the builder's file-by-file claims and the test covering each are in `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/9671040/QA_CHANGES.md` (one row per SUS-id); the full diff vs main is `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/9671040/QA_DIFF.patch`.
- **Deliberately NOT fixed this round (do not re-flag as new; DO confirm they are unchanged and still tracked):** SUS-10 (tab-strip ARIA semantics — pre-existing, own ticket) · SUS-17 (vendor assets on cdn.jsdelivr — pre-existing, own ticket) · Q1 (the three paper factors feed no KPI — ruled the NEXT leg, not this round).
- **Q2 fix expected in-round:** KPI tile `factorRefs[]` now carry `unitBasis` (kpis.js `mediaAreaReference()` / `paperProfileReference()`), and the test at `__tests__/sustainability-period.test.js` either asserts on `/kpis` too or is retitled to what it checks. **Plus a new zero-row-period test** (the state the default view lands in).
- **SCIM commit `fb3b11e` (code-only; on the branch since pass 1):** closes two security-review findings — F-1 (token issuance dated on save, `entraProvisioningScimTokenIssuedAt`; a real `POST /api/setup/entra-provisioning/scim-token/revoke` that clears the token AND sets mode `off`, verifies the clear persisted, audits itself, idempotent) and F-4 (`audit('scim_auth_failed', {path, method, ip})` on the rejection branch with a payload IDENTICAL across failure modes — the shape must not become an oracle). Tests: `__tests__/scim-security-controls.test.js` (10 cases; 9 red-first, the 10th a deliberate positive control). Review doc: `docs/security/SCIM_PROVISIONING_SECURITY_REVIEW.md` v1.1 (F-2/F-3 dispositioned as open-by-decision). **The SCIM endpoint is INERT — mode untouched. Do not attempt to enable it, do not probe it for bypass beyond what the tests cover; this is the THROUGH-CODE half only.**

## 2b. The builder's OWN warnings for this pass (from its 09:05:07Z STATUS — test these first)
- **SUS-03: the builder's first fix emitted a backwards period (`from 2027-01-01, to 2026-09-01`) that the same endpoint 400s when a caller sends it; its test asserted only `from !== to` and passed.** Fixed in `9671040` (`from <= to` + a past-window case). **Re-check by URL against the running server, not the suite:** `?from=2027-01-01`, `?to=2020-01-01`, `?from=2026-06-01`, and the inverted `?from=2026-04-29&to=2026-01-30` (must 400). State the FAIL condition first.
- **SUS-07 trap:** `POST /api/settings/costs` needs a real CSRF token — without it EVERY case returns 403 and reads like validation. The builder nearly recorded a false pass that way. Get the token first; expected codes: `-0.05` NEGATIVE_COST_VALUE · `"abc"` INVALID_COST_VALUE · `1e12` IMPLAUSIBLE_COST_VALUE · `true` INVALID_COST_VALUE (Number(true)===1 — the case a reviewer skips) · `0.012` → 200 and persisted.
- **Two surface traps:** the seeded feed is older than 30 days (default view correctly reports the window outside the data — choose All Time for figures); the dashboard PRE-FILLS From when you pick Custom Range — clear it AFTER selecting custom for the half-open case.
- **Contrast (the pass-1 gap the builder asks you to close):** measure the muted `.small.text-muted` basis line ("NOT per kilogram of wood") against 4.5:1. The builder will fix what you find.
- **New tickets filed, not fixed (do not re-flag; confirm unchanged):** RD-144 (SUS-10 ARIA tabs) · RD-145 (SUS-17 CDN vendoring) · RD-146 (NEW: no currency setting exists — `$` is hardcoded across every money renderer; SUS-06's fix makes the screen self-consistent and still wrong for a non-dollar customer).
- Old worktrees (697c933, 6587569) were removed by the builder; the pass-1 report paths are unchanged.

## 2c. LATE ADDENDUM (Wednesday, 19:1x AEST, from the builder's 09:08:56Z STATUS) — contrast: the arithmetic is done, ONE browser check settles the remaining hypothesis
The builder computed WCAG 1.4.3 ratios from the stylesheets: light `.text-muted` on white 6.78 / on the alert-light panel 6.69; dark `.text-muted #9090a0` on `.card #1e1e3f` **5.09 (the flagged "NOT per kilogram of wood" line — PASSES)**; on body `#1a1a2e` 5.43; **on a light alert background 3.06 — FAIL if it ever occurs.** Mechanism: `body.dark-mode .text-muted` is overridden to `#9090a0` (index-styles.css:1196, settings-styles.css:233) but dark mode overrides only `.alert-info` — `.alert-light/success/warning/danger` keep Bootstrap's light backgrounds. The builder believes no muted text sits inside those alerts but distrusts its own static walk.
**Your check (dark mode, computed styles, not stylesheet arithmetic):** for every `#sustainability [class*=text-muted]` and the registry-table equivalent, read the computed colour and the COMPOSITED background and compute the ratio; report any that lands on a light alert background as a 1.4.3 finding, and if none does, record the gap as LATENT (the next muted line inside an alert will hit it). State the FAIL condition first; include one element you know passes as the positive control.

## 3. Scope
- **Charter:** (a) VERIFY each claimed SUS fix against pass 1's own repro steps — state the FAIL condition, re-run the repro, and confirm the regression test named in the report exists and could fail; (b) hunt REGRESSIONS on the flows the fixes touched (period resolution, the cost POST, the 500 path, the live region) — the default "Last 30 Days" view and "All Time" both directions, the half-open and inverted ranges, the in-flight race with an injected delay, the costs round trip; (c) the through-code review of `fb3b11e` — read the diff and the ten tests against the two findings; look for the audit payload leaking token material or failure-mode distinctions, a revoke that reports success without persisting, an issued-at that moves on an unrelated save.
- **In scope:** the changed surfaces + the SCIM diff/tests. Console errors. Accessibility on the changed screens (the new live region: does it announce; is there a loading state).
- **Out of scope / do NOT touch:** the demo; enabling SCIM; Entra configuration screens beyond reading them; destructive settings changes you cannot revert (record any you make); no repository writes.

## 4. Credentials (POINTER ONLY)
- **None needed:** open mode. A login page on the surface = STOP and report.
- **Personas:** the sceptical finance reader again (Marcus — the period/units/costs oracle), then a short accessibility pass on the live region; a code-reviewer stance for the SCIM half.

## 5. State-mutation & cleanup
- Revert-what-you-change; exclude-and-report anything else. Pass 1 left one non-revertible residue (`cost_per_sheet_paper_updated_at`) — expect it, do not flag it as new; note any further residue you create.

## 6. Output boundary (fixed)
- Findings, reports and recommendations ONLY. No code, tests, fixtures, tickets or config changes. Fix-shape + regression test in prose.

## 7. Known-fragile / known-changed
- **Known-fragile after the fixes:** every SUS fix is a period-honesty or validation change — the risk is a fix that over-rejects (a legitimate range or cost now refused) or a message that names the wrong condition. Test the POSITIVE control on each: the valid range still loads, a valid cost still persists and renders with its currency symbol, a real 500 still surfaces `errorCode`.
- **Carry, do not rediscover:** ENERGY KWH / SCOPE2 / SECURE RELEASE unavailable by design; RD-139 row cap unexercisable at the seeded size (state it); RD-143 DATA_DIR trap (builder-filed).

## 8. Logistics
- **Time-box:** ~45–60 minutes + the two diff reads; stop when findings repeat.
- **Findings sink:** `projects/nexusai/reports/2026-09-01-s12-sustainability-pass2/` + `SUMMARY.md` ranked by severity with a per-SUS-id verdict table (FIXED / NOT FIXED / REGRESSED / NOT VERIFIABLE) and the verdict line "PASS for deploy / PASS with findings / FAIL". Wednesday reads the files; no tickets from you.
- **Signal when done:** end your turn with the summary path on its own last line.
- **Escalation:** `wednesday-agent@agentmail.to`, subject `[QA -> Wednesday] QUESTION: <topic>`, or the top of `SUMMARY.md` and continue on the safest reading. Approval-class ALWAYS pauses.

---

PROVENANCE:
- Pass-1 verdict PASS-with-findings, 18 findings SUS-01..18, Q1/Q2, the driver note | the pass-1 report files (path above), written 18:32–18:43 AEST | read 2026-09-01
- Wednesday's fix-round ruling (in/out lists; Q1 = next leg; Q2 in-round; zero-row test) | Wednesday ADDENDUM to s12, 2026-09-01T08:50:39Z, in datasec-nexusai@ | read 2026-09-01
- SCIM commit fb3b11e content (four files; F-1/F-4 mechanics; 10 tests, 9 red-first) | s12 STATUS mails 2026-09-01T08:23:28Z + 08:27:21Z; head verified by Wednesday's own ls-remote 18:27 AEST | read 2026-09-01
- 9671040 / /Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/9671040 / 3011 / the fixed SUS set | s12 "QA SURFACE UP (pass 2)" mail 2026-09-01T09:05:07Z | read 2026-09-01
- Kam's standing QA-gate process | dashboard chat 2026-09-01T17:55:18 + 17:55:45 AEST | read 2026-09-01
