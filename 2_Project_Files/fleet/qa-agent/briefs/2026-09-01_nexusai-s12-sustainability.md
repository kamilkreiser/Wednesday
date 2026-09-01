# QA Agent Invocation Brief — Datasec / NexusAI — s12 Sustainability round 2 (2026-09-01)

**R0 (client isolation):** this brief carries exactly one client's content (Datasec / NexusAI). Never name or reference any other client. Read only the paths named here.

**Read FIRST, in full:** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/QA_AGENT_CHARTER.md` — mission, the two hard rules (state the FAIL condition before each test; untested areas are first-class output), method, boundaries, reporting standard. Then your own project's `CLAUDE.md` and the `human-emulation-testing` skill (persona-first; Claude-in-Chrome is the default driver).

**Why this session exists (Kam, 2026-09-01 17:55, standing from today):** every change is reviewed by the testing agent — visually AND through code, in a real browser when browser-related — BEFORE Wednesday's completion check and any deploy. You are the first live run of that gate.

---

## 1. Target
- **Client / Project:** Datasec / NexusAI (product: "NexusAI Print Analytics" dashboard — settings + reporting web app, Node/Express backend, vanilla JS front end with Bootstrap Icons).
- **Running target:** `http://127.0.0.1:3011/` — a LOCAL run of commit `697c933` (branch `rd-136-nga-defaults-s12`; = ef9859d + one further commit that adds a unitBasis label to the three paper factors) stood up by the project's own agent from a git worktree with a freshly seeded data directory. **Same commit as the branch under review, NOT the demo image.** Say exactly that in your report; never write that demo was tested.
- **Environment identity:** local, `NODE_ENV=development`, auth in OPEN mode by design (fresh data dir → `isAuthEnforced()` false; no shim). Confirmed by Wednesday from the agent's READY FOR QA + QA SURFACE UP mails.
- **Production?:** NO. Nothing you touch reaches any deployed instance. The demo (a Container App) is SSO-only and is not your surface.
- **Before trusting "localhost": fingerprint the browser** (`navigator.hardwareConcurrency`, `screen.width×height`) against this Mac (a Mac Studio M3 Ultra; compare with `sysctl -n hw.ncpu` in your shell). The Chrome extension can be attached to a different Mac; a refused loopback is the tell.

## 2. Spec / DoD being tested against
- **Spec source (read-only):** the Sustainability Analytics dev spec v1.0 in the project tree — `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/697c933/docs/sustainability/` (17 sections; §6.1 KPI definitions, §7.1 factor sourcing rule "never infer water/fibre from a carbon factor", §7.2 tree-equivalent display rule, §16 MVP scope, §17 "a metric must state its period").
- **What was changed in this round (the agent's claims — inputs to falsify, not evidence):**
  1. Settings → Sustainability nav entry AND section heading now show a TREE icon (`bi-tree`); previously the class `bi-leaf` rendered a blank (it does not exist in bootstrap-icons 1.10.0).
  2. Dashboard → Sustainability tab LOADS (previously "Could not load sustainability KPIs" on every deployment: the page called `/api/sustainability/kpis` with no period; the §17 guard refused; 500). Now: an unbounded request resolves its period against the data actually read; the tab FOLLOWS the dashboard's date controls (`#dateRange`, `#fromDate`, `#toDate`), reloads on change, and STATES its period on the tab.
  3. Factor registry (Settings → Sustainability): 27 sourced default factor records — NGA 2025 electricity Scope-2/Scope-3 by state/territory (Table 1) + three paper factors (water 665 L/kg; wood 3.51 m3/tonne paper; 24 tree-equivalents/tonne paper) — each with publication · table · row · version · effective-from · retrieved date · licence · link · alternatives considered. A **Reference column** was added. The "Not for reporting" banner is now CONDITIONAL: with nothing provisional it is replaced by a green summary of the three publications; the provisional machinery still exists and has a direct test.
  4. Settings → Costs: POST now returns a `deprecations` entry for `costPerSheetSimplex` (dormant setting retired; RD-140).
  5. (commit 697c933) every paper factor record carries a `unitBasis` ("per tonne of finished paper (NOT per kilogram of wood)" on wood and tree-equivalents; "per kilogram of finished paper" on water) shown in the API, under the value in the registry table, and on the KPI tile reference line — check all three places; a per-tonne figure read as per-kilogram is wrong by 1000× and looks plausible.
  6. Every user-visible number on the tab carries its evidence class (Measured / Calculated / Unavailable) and "Where this number comes from" references.
- **Code-review half (through code):** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/697c933/QA_DIFF.patch` (the full `git diff main...697c933`) and `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/697c933/QA_CHANGES.md` (the agent's file-by-file claims + the tests covering each). Read the diff against each claim above; read the tests, don't only trust that they ran; note any claim with no test that could fail.
- **Source tree (read-only, for root-causing):** `/Volumes/DevMASTER/!CODING/Datasec/NexusAI/qa-worktrees/697c933` (the worktree at 697c933). Do not edit anything in it.

## 3. Scope
- **Charter:** explore the Settings → Sustainability surfaces and the Dashboard → Sustainability tab as a demanding admin user who will put these numbers in front of a customer, looking for figures that are wrong, unlabelled, unsourced, or that change meaning when the date range changes; and review the diff for claims the tests cannot falsify.
- **In scope:** the four changed surfaces above; the date-range interaction (default "Last 30 Days" vs "All Time" vs a custom range that partially overlaps the seeded data span 2026-01-30 → 2026-04-29); the factor registry's Reference column and links; the conditional banner; the deprecation response on the Costs POST; console errors; keyboard/accessibility on the changed screens; navigation chaos (refresh mid-load, back, deep link straight to the tab).
- **Out of scope / do NOT touch:** anything outside the local instance; the demo/Container App; Entra/SCIM/provisioning screens (a separate review); no destructive settings changes beyond what you can revert in-session (record any you make); no repository writes.

## 4. Credentials (POINTER ONLY)
- **None needed:** the local run is in open mode. If you meet a login page on 127.0.0.1:3011, STOP and report it — that is a finding about the surface, not a door to force.
- **Roles/personas:** an admin configuring sustainability for a customer (power user); a sceptical finance reader who will challenge every number (novice-to-the-domain persona); an accessibility user on the changed screens.
- **Disposable account for state-mutating fuzz:** none — settings you change in-session, revert; anything you cannot revert, report as coverage gap.

## 5. State-mutation & cleanup
- **Sanctioned pattern:** revert-what-you-change; exclude-and-report anything else.
- **Reachable-on-demand product states:** empty period (a custom range with no data) · full span ("All Time") · partial overlap · factor registry with all-sourced records (current) · provisional state (NOT reachable in-session without editing the seed — report as a gap, do not construct it).
- **Two traps the builder recorded, so you do not rediscover them as bugs:** (a) the seeded data spans 2026-01-30 → 2026-04-29, so "Last 30 Days" correctly shows zeros — choose "All Time" to see figures (test BOTH directions: zeros with the reason stated is the correct behaviour on the default range); (b) `DATA_DIR` is silently ignored if the directory has no `settings.json` yet — already filed by the builder as RD-143 (High); do not re-file, but DO note if the running instance shows any sign of having used the wrong data dir.

## 6. Output boundary (fixed)
- Findings, reports and recommendations ONLY. No code, tests, fixtures, tickets or config changes. Describe the fix-shape and the regression test the owner should add, in prose.

## 7. Known-fragile / known-changed areas
- **Known-fragile:** the period plumbing (the defect that hid the tab for its whole life was a missing period; hunt its siblings — the tab's own "Refresh" button, a range change while a load is in flight, deep-linking to the tab before the date controls initialise); the unit labels on tiles (one tile is known to read "148.74 currency" — the unit label, not the value — confirm and classify); factor units (two paper records are deliberately held in per-tonne-of-paper units with a note — check the SLOT label matches the value's unit everywhere it is displayed and in the API JSON).
- **Recent changes — do NOT flag as new:** the tree icon replacing a blank; the conditional banner replacing the always-on "Not for reporting"; the `deprecations` entry on the Costs POST; the tab reading the dashboard date controls (it used to ignore them).
- **Known open gaps (carry, do not rediscover):** ENERGY KWH and SCOPE2 tiles are deliberately "Unavailable" (no energy column in the store; RD-61) — the correct behaviour is that the tile NAMES the missing input; SECURE RELEASE AVOIDED likewise unavailable by design (§6.2). RD-139 (SQL date filter + 10k-row cap) was addressed in this round — a large "All Time" period must not silently under-report; the seeded set is small (1,445 rows) so state that the cap could not be exercised.

## 8. Logistics
- **Session time-box:** ~60–75 minutes of driving + the diff read; one persona per session, up to three sessions; stop when findings repeat.
- **Findings sink:** your report under your own project: `projects/nexusai/reports/<session>/` per your template, plus a one-page BLUF summary (`SUMMARY.md`) ranked by severity with: what you tested, what you did not, coverage map, and a verdict line "PASS for deploy / PASS with findings / FAIL" — Wednesday reads the files; no tickets from you.
- **Signal when done:** end your turn with the summary path on its own last line. Wednesday's watcher sees an idle pane; there is no inbox for you yet.
- **Escalation path:** anything the brief does not answer → Wednesday (`wednesday-agent@agentmail.to`, subject `[QA -> Wednesday] QUESTION: <topic>`) if your project has mail configured; otherwise write the question at the top of `SUMMARY.md` and continue on the safest reading. Approval-class items ALWAYS pause. Priority on findings is the humans' call.

---

PROVENANCE:
- Local run at 127.0.0.1:3011 = commit ef9859d in a worktree with a seeded data dir, open-mode auth by design, NOT the demo image | NexusAI agent mails READY FOR QA 2026-09-01T08:11:57Z + QA SURFACE UP (2026-09-01T08:17:42Z) in wednesday-agent@agentmail.to | read 2026-09-01
- The five change claims, the icon root cause (bi-leaf width 0 / bi-tree 16px), the tab root cause (missing period → §17 refusal → 500, demo logs 07:48:44Z) | READY FOR QA mail 2026-09-01T08:11:57Z + Kam's live screenshots 17:5x AEST | read 2026-09-01
- Seeded span 2026-01-30 → 2026-04-29; DATA_DIR trap (RD-143) | READY FOR QA mail | read 2026-09-01
- Spec location docs/sustainability in the project tree | ls of the NexusAI repo | read 2026-09-01
- Known gaps ENERGY/SCOPE2/SECURE RELEASE unavailable by design; RD-139 addressed | READY FOR QA mail + the tab screenshot read by Wednesday | read 2026-09-01
- Kam's standing QA-gate process | dashboard chat 2026-09-01T17:55:18 and 17:55:45 AEST | read 2026-09-01
