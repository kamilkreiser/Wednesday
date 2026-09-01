# QA Agent Invocation Brief — Datasec / NexusAI — s13 Sustainability refine round 3, PASS 4 (delta-only) (2026-09-01)

**R0 (client isolation):** this brief carries exactly one client's content (Datasec / NexusAI). Never name or reference any other client. Read only the paths named here.

**Read FIRST, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md`, then your own project's `CLAUDE.md` and the `human-emulation-testing` skill. **Then read pass 3's own output** — `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/nexusai/reports/2026-09-01-s13-sustainability-pass3/SUMMARY.md` + its reports — every P3 id below is defined THERE with its repro; this pass is measured against it. **Then read the builder's delta notes:** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/abf3986/QA_CHANGES.md` (one row per R3 id + NINE warnings — read all nine before touching the page) and the diff `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/abf3986/QA_DIFF.patch` (delta `c1fe9ea..abf3986`, 1,823 lines, lockfile excluded; four commits: `6ab67f2` R3-1+2+8 · `1132210` R3-3+4+5 · `ad37a44` R3-6 · `abf3986` R3-9). **Driver: Playwright MCP from the start** (the Chrome MCP cannot deliver events to this page — proven in pass 1; do not re-spend it).

**Why this session exists (Kam, 2026-09-01 17:55, standing):** every change is reviewed by the testing agent — visually AND through code, in a real browser when browser-related — before Wednesday's completion check and any deploy. This is PASS 4: the builder (s13) has done refine round 3 against your pass-3 findings. **Nothing is deployed; the demo still runs the pre-s12 image.** A deploy GO depends on this report.

**Your own pass-3 line stands as the standing rule for this pass: "the fixture is not the product" — derive every fixture from the SHIPPED artefact: parse each page's own `<link>` list, build inputs from the shipped attributes, exercise the real dependency.** The builder says it has now done the same in its suite; that is its claim, not your evidence.

---

> 🔴 **BRIEF UPDATED 21:4x AEST (read before any browser work): the surface is being RESTOOD at head `60a225f`** — one commit past `abf3986` (R3-9's real fix; test + security decision only, not observable on an open-mode surface). Expect ~3 minutes of HTTP 000 on :3013 during the restand; **re-verify the worktree HEAD (`qa-worktrees/60a225f`) and `/api/health` 200 before judging anything**, and read the regenerated `QA_CHANGES.md`/`QA_DIFF.patch` in THAT worktree (delta `c1fe9ea..60a225f`). Everything else in this brief stands; the R3-9 row and §2b/§3(c) carry the corrected criterion.

## 1. Target
- **Client / Project:** Datasec / NexusAI ("NexusAI Print Analytics" — Node/Express backend, vanilla JS front end, Bootstrap Icons).
- **Running target:** `http://127.0.0.1:3013/` — a LOCAL run of commit **`abf3986`** (branch `rd-136-nga-defaults-s12`) from the worktree above, PID 86625, data dir `qa-data/` inside the worktree, seeded **1,445 rows / 1,187 print, span 2026-01-30 → 2026-04-29** (identical fixture to passes 2 and 3). **Same commit as the branch under review, NOT the demo image** — say exactly that in the report; never write that demo was tested. Verified from Wednesday's seat at 21:3x AEST: `curl /api/health` 200 in 2 ms; worktree HEAD `abf3986`; branch head `abf3986c2` by `git ls-remote`; pass-3's :3012 retired (HTTP 000).
- **Environment identity:** local, `NODE_ENV=development`, auth **OPEN by design**. **Fingerprint the browser** against this Mac before trusting "localhost" (`navigator.hardwareConcurrency` = `sysctl -n hw.ncpu`).
- **Production?:** NO. Nothing you touch reaches a deployed instance.

## 2. What changed since pass 3 (the builder's claims — inputs to falsify, not evidence)
| R3 | pass-3 id | builder's claim |
|---|---|---|
| R3-1 (+R3-8) | P3-01 (+P3-09) | dark mode defined ONCE in `static/css/dark-mode.css`, linked from `index.html`, `settings.html` AND `first-run-setup.html`; both per-page blocks DELETED; the 96 registry lines that were 3.14:1 now ≥4.5:1; table striping via `--bs-table-*` + explicit base |
| R3-2 | P3-04 | alert severity restored as TEXT identity + 4 px left rule on the shared dark surface (headings 7.92–10.16:1, rules 3.81–5.86:1); pale Bootstrap backgrounds NOT back |
| R3-3 | P3-02 | strict-decimal predicate for cost strings: `"  "`, `"0x10"`, `"1e3"` → 400 with actionable `details`; `"0.011"` → 200; numbers accepted as numbers |
| R3-4 | P3-07 | money at 2 dp at every magnitude (40.403 → `$40.40`; 1239.5 → `$1,239.50`); counts unchanged |
| R3-5 | P3-05 | Retry = filled `btn-danger`, both modes |
| R3-6 | P3-03 | `type="text" inputmode="decimal" pattern` + `checkValidity()` — `12abc` refused AT THE BOX, nothing posted |
| R3-9 | P3-06 | **CORRECTED 21:4x (builder WITHDREW its abf3986 claim — the fix was INERT there):** the real `JsonStorage.readFile()` never rejects, it returns `null` on any error, so at `abf3986` an unreadable settings file read as OPEN (router 200). Fixed at **`60a225f`**: readability asked directly — settings file EXISTS and cannot be read/parsed → UNKNOWN → privileged router 403; ABSENT store still `open` (first-run must not fail closed). Tested through a REAL `JsonStorage` over a real temp dir (corrupt JSON + chmod-000; four controls). |
| R3-7 | — | **RD-151** (inline per-field errors) — ruled not deploy-gating; do NOT re-file |
- Suite at this head: `npm run verify` → `PASS 713/713 across 31 suites` (pass 3: 652/652). A green suite is the builder's claim, not yours.
- **Filed by the builder this round, do NOT re-file — DO confirm they are real where a diff touches them:** **RD-149** (light-mode muted grey fails AA on 4 of 6 pale alert backgrounds — pre-existing, product-wide) · **RD-150** (`getSetting` `value || null` erases a stored 0/false; `kpis.js`'s "unusable cost" branch dead for 0). Also standing: RD-147 (`.table-title`), RD-148 (P2-06 SCIM revoke UI).

## 2b. The builder's OWN warnings (nine in QA_CHANGES.md — the ones that decide this pass)
- **R3-9 cannot be exercised on this surface; a 403 here would be the REGRESSION** (auth open → provisioning routes correctly 200). Prove it THROUGH CODE at **`60a225f`** — the CORRECT criterion (a 'rejecting storage double' is the instrument the builder itself just disproved — do NOT accept it): **does the decision return UNKNOWN — and does the privileged router 403 — when the settings file EXISTS and cannot be read or parsed, exercised through a REAL `JsonStorage` over a real directory? And does an ABSENT store still answer `open`?** Read the test: real dependency, corrupt-JSON + chmod-000 cases, controls both directions; sabotage direction stated. If the test uses any double for the storage, record R3-9 as NOT VERIFIED, never as verified.
- **Select All Time first** — the default view shows "Unavailable" tiles BY DESIGN (seeded span outside Last 30 Days). Judge the default view ONLY for the completion-check questions below; judge tiles' values on All Time or an in-span range.
- **A paper cost is pre-set (`0.011`)**; whitespace in a box is now refused at the input (deliberate); an empty box is valid and OMITTED.
- **Its contrast numbers are jsdom, not a browser** — it asks you to re-measure; do.

## 3. Scope — DELTA ONLY, FAIL condition first every time
- **(a) Per-id verdict table (P3-01..09 → FIXED / NOT FIXED / REGRESSED / NOT VERIFIABLE-with-reason)** using pass 3's own repro per id, then the POSITIVE control (the legitimate case still works: All Time still prices; `"0.011"` still persists; a valid range still renders; light mode NOT hurt by the dark fix).
- **The three questions Wednesday's completion check will ask — answer them explicitly in their own section:** (1) on the EMPTY DEFAULT VIEW with a cost configured, is PAPER COST unavailable-with-a-reason naming the real data span (P2-01 — re-confirm UNREGRESSED)? (2) is every empty-window period sentence honest — both ends for a closed window, "onwards"/"up to" for open ends, tile reason AND Period line (P2-02 — re-confirm UNREGRESSED)? (3) 🔴 **in DARK MODE, in a real browser, does every muted/diagnostic line on the Settings → Sustainability factor registry (the 96 lines) AND on the dashboard's changed panels measure ≥ 4.5:1 from computed styles + composited background?** Measure — do not read the stylesheet. Also measure `first-run-setup.html` in dark mode as a NEW surface (it had zero dark rules before).
- **(b) Regressions on the touched flows:** the six alert variants in BOTH modes (severity distinguishable; text ≥4.5, rule ≥3; no pale backgrounds back); cost strings `" "`, `"\t"`, `"0x10"`, `"1e3"`, `"12abc"` (at the box: refused, nothing posted — watch the network), `""` (omitted), `"0.011"` (200); money 40.403 / 1239.5 / 0.5 on the tile; Retry in both modes on a forced 500; table striping/hover in dark mode; the settings form round-trip (clear one box, save, others survive); the live region across a 500 + Retry (identity, unregressed).
- **(c) Through-code:** R3-9 as in 2b (at `60a225f`, the restood head); the dark-mode test's page list is READ from each page's `<link>` tags (claim) — open the test and say whether the list is parsed or typed; `settings-cost-form.test.js` builds inputs from the shipped markup (claim) — same question; RD-149/RD-150 exact-set assertions — do they fail in BOTH directions as claimed.
- **Out of scope / do NOT touch:** the demo; enabling SCIM (`/scim/v2/Users` answers 401 here — confirm, don't probe further); destructive settings changes you cannot revert (record any); no repository writes; RD-147/148/149/150/151 (confirm, don't re-file); Q1 paper KPIs (a later round); AT runs and 200%/320 px reflow (the builder did not; list as NOT TESTED unless you have time inside the box).

## 4. Credentials (POINTER ONLY)
- **None needed:** open mode. A login page on the surface = STOP and report.
- **Personas:** Marcus (sceptical finance reader) for (a)+(b); a real-browser contrast instrument for question (3); a code-reviewer stance for (c).

## 5. State-mutation & cleanup
- Revert-what-you-change; exclude-and-report anything else. Known residue: `cost_per_sheet_paper_updated_at` (non-revertible timestamp). Restore the pre-set cost `0.011` if you change it.

## 6. Output boundary (fixed)
- Findings, report, recommendations ONLY. No code, tests, fixtures, tickets or config changes. Fix-shape + regression test in prose, per finding.

## 7. Known-fragile / known-changed
- Every fix is a contrast, validation, money-format or authz change — the risk is over-rejection (a legitimate cost/range refused), a dark fix that hurt light, a rule-based severity that disappears at small widths, a debounce swallowing a real action. Positive control on each.
- Carry, do not rediscover: ENERGY KWH / SCOPE2 / SECURE RELEASE unavailable by design; RD-139 row cap unexercisable at the seeded size; RD-143 filed+commented; RD-144..151 all filed.

## 8. Logistics
- **Time-box:** ~45 minutes + the diff/test reads; stop when findings repeat.
- **Findings sink:** `projects/nexusai/reports/2026-09-01-s13-sustainability-pass4/` + `SUMMARY.md` ranked by severity, with the per-P3-id verdict table, **the three completion-check answers as their own short section**, the NOT-TESTED list at the same weight, and the verdict line "PASS for deploy / PASS with findings / FAIL". Wednesday reads the files; no tickets from you.
- **Signal when done:** end your turn with the summary path on its own last line.
- **Escalation:** `wednesday-agent@agentmail.to`, subject `[QA -> Wednesday] QUESTION: <topic>`, or the top of `SUMMARY.md` and continue on the safest reading. Approval-class ALWAYS pauses.

---

PROVENANCE:
- Pass-3 verdict (13/14 FIXED, P2-05 NOT FIXED = P3-01, P3-04 regression, seven minors P3-02/03/05/06/07/08/09) | pass-3 SUMMARY.md (path above) as read by Wednesday 21:04 AEST + the daily note 21:04/21:05 | read 2026-09-01
- The R3 set, head abf3986, PID 86625 / :3013 / worktree / seed 1,445/1,187 / 713/713 / RD-149/150/151 / the .alert-info reconciliation / R3-9 mechanism + sabotage / the nine warnings | s13 STATUS "QA SURFACE UP (pass 4)" 2026-09-01T11:28:44Z in wednesday-agent@ + `qa-worktrees/abf3986/QA_CHANGES.md` | read 2026-09-01
- Delta commits 6ab67f2 · 1132210 · ad37a44 · abf3986; QA_DIFF.patch 1,823 lines | `git log --oneline c1fe9ea..abf3986` + `wc -l` in the worktree, Wednesday's seat 21:3x | read 2026-09-01
- Surface 200 in 0.002 s at :3013; :3012 HTTP 000; worktree HEAD abf3986; branch head abf3986c2 | Wednesday's own curl + `git rev-parse` + `git ls-remote` 21:3x AEST | read 2026-09-01
- Kam's standing QA-gate process | dashboard chat 2026-09-01T17:55:18 + 17:55:45 AEST | read 2026-09-01
