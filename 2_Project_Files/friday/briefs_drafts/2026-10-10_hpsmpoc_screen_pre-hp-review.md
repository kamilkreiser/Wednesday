# HPSM-POC screen before HP's layout review (Tue 13 Oct): fixes only (Datasec)
Read-only screen, 2026-10-10 evening. Code: origin/main `5a93aa3` (= hosted, C-82). Analysis repo: origin/main `e4e8f1a`. No writes in the project, no servers, no hosted request.
Jira (read-only, token from the project's 4_Credentials/.env, values not printed): `project = HPSMPOC AND statusCategory != Done ORDER BY updated DESC`, POST /rest/api/3/search/jql, maxResults 100, nextPageToken followed until absent (2 pages): **TOTAL 111 open** (106 Backlog, 5 In Progress: 87, 88, 90, 91, 95). The open set is mostly epics, SOW deliverables, HP asks and SME/content work.

## BLUF
- **The context line "first read ~2.7 s" is out of date.** B194 (C-82, today 01:52Z) measured **6,197 ms**, and **4,496 ms of it is the `caller` stage** (B194_STATUS BLUF 6). The plan was quiet (24–48 % CPU). The highest-value fix work before Tuesday is finding and removing that cost. HPSMPOC-207 was clean on that start: 0 `fail:` lines, no 3211, 3213 or 3214. B193 M-1 is a test only.
- 15 items an agent can do now, for 2 seats: **Seat A = `api/`**, **Seat B = `web/` + e2e**, and records stay with Friday. 16 lines are not actionable before Tuesday. 12 records are stale.
- None of the actionable items needs an HP Restricted document, Kam, HP or an SME. Items 1 and 3 each need a pick from Friday on an open question (Q-B194-1 or Q-B194-2), not from Kam.

## 1. Agent-actionable now, fixes only (ranked by value to Tuesday)
| # | Key / id | What | Source | Files / area | Size | Spark? |
|---|---|---|---|---|---|---|
| 1 | HPSMPOC-232 / Q-B194-1 (a) | Split the `caller` stage into lookup vs create/refresh write. Then remove whichever part costs 4.5 s on the first read (ADR-A15 refresh-at-most-5-min applies) | B194_STATUS.md:150 (Q-B194-1); 232 Backlog | Seat A: `api/src/HpsmPoc.Modules.Assessment/Http/RequestStages.cs`, `Endpoints/Gate.cs`, `Identity/Caller.cs` | M | No (caller identity path, 3 files) |
| 2 | HPSMPOC-232 + 207 (records) | Add B194's numbers to Jira. 232's last comment (39299) says 2,698 ms; B194 measured 6,197 / caller 4,496. 207's last comment (39301) predates B194's clean start | 232/207 Backlog; B194_STATUS BLUF 4, 6 | Friday, Jira only | S | n/a |
| 3 | HPSMPOC-234 (+ Q-B194-2 data) | Web-side warm-up after a start: render the landing page once and open BFF→API connections with an unauthenticated GET. B194: Home settled in 10.7 s, BFF→API hop 1.2–2.2 s | 234 Backlog; B194_STATUS BLUF 6–7 | Seat B: `web/src/instrumentation.ts` + warm-up module | M | No (sits beside the sign-in warm-up) |
| 4 | HPSMPOC-243 M-1 | Test that EF entries below Error keep their level inside `HandledRace.ExpectAnyFailure()`. Make it red under B193's mutant; an Error in the same scope stays Debug | 243 Backlog, comment 39303; B193_STATUS lines 58–65 | Seat A: `api/tests/.../FirstVisitWarmupTests` or `HandledRaceLogTests` (product `HandledRace.cs:132–141` unchanged) | S | Yes (test only) |
| 5 | B193 N-3 (docs) | Bring ADR-A26 in line with the B192 whole-flow scope | B193_STATUS N-3; `api/src/HpsmPoc.Modules.Assessment/README.md:70` vs `HandledRace.cs:39–42` | Seat A (with #4) | S | Yes |
| 6 | HPSMPOC-207 / B193 N-1 | `FirstLoginTimedOut` also counts SingleAsync's "no / more than one element" IOE as a pool timeout. Narrow it, and add 18456, 229 and SingleAsync rows to the guard test | B193_STATUS N-1; `HostedDemoStartup.cs:179–180`; test `HostedDemoRobustnessTests.cs:513–544` | Seat A | S | Yes (one product file, not auth) |
| 7 | HPSMPOC-239 | `web-settings.test.ts` and `client-content.test.ts` time out under load. Give each an explicit timeout with a reason; do not raise the global default | 239 Backlog | Seat B: those 2 web test files | S | Yes (tests only) |
| 8 | HPSMPOC-238 | Flaky e2e F-22: replace `networkidle` after reload with a wait for the action plan's content | 238 Backlog | Seat B: `web/e2e/playbook-b17-clicks.spec.ts` (~:71) | S | Yes |
| 9 | HPSMPOC-227 | 3 opt-in live-API specs (6 tests) fail on main. CI never runs them | 227 Backlog | Seat B: `web/e2e/*-live-api.spec.ts` + local showcase API | M | No (3 files, live rig) |
| 10 | B189 m-1 (no ticket) | The blank-name rule refuses the assigned IVS U+E0100–E01EF. Upload was 201 at base, 422 at head: a B188 regression | B189_STATUS line 46; `FeedbackFiles.cs:141` (same range in `FeedbackEndpoints.cs:272`) | Seat A | S | Yes (validation, not auth). Gate left "keep or narrow" to Friday |
| 11 | HPSMPOC-228 N-6 | Report-store warm-up logs a failed round at Information; change it to Warning | 228 Backlog | Seat A: `api/src/HpsmPoc.Api/Timing/ReportStoreWarmup.cs` + `ReportStoreWarmupTests.cs` | S | Yes |
| 12 | B189 N-3 (no ticket) | The warm-up labels every 409 "not scored yet", including "no ruleset scores this set" | B189_STATUS line 49; `FirstVisitWarmup.cs:42, 177–179` | Seat A | S | Yes |
| 13 | HPSMPOC-228 N-2 / N-8 / N-3 | Remove the dead readiness POST regex (`bff.ts:149`); fix the TX cookie comment, which says 10 min where the value is 30 (`cookies.ts:5`); R11 guard blind to the dispatcher timer (infra/tests) | 228 Backlog | Seat B (bff/cookies); infra tests | S | No (bff/auth files) |
| 14 | HPSMPOC-225 | About 18 `GeneratedRegex` id shapes end in `$`, which accepts "id\n". Change them to `\z` and add one table test | 225 Backlog; e.g. `Requests.cs:105–123`, `ReportingEndpoints.cs:62–68`, `ActionPlanEndpoints.cs:57–60`, `ReadinessResultReader.cs:161–164` | Seat A (many files) | M | No (multi-file input validation) |
| 15 | Records | Open PRs for `records/b187`, `b188`, `b190`, `b192`, `b194`: all pushed, none on analysis main, which ends at C-81. Commit the B189 and B193 STATUS and evidence, which are untracked in the working tree and have no branch. Ticket B189 m-1/N-1..N-6 (Jira text "B189": 0 hits) and B193 N-2..N-7 | analysis `git ls-tree origin/main`, `git status` | Friday, analysis repo + Jira | S | n/a |
Low value for Tuesday (laptop only): HPSMPOC-159, where `client.ts:218` drops the reset 503 body. Size S, Spark yes. On hosted, `resetShowcase` gets a 404 and falls back to `resetDemo`. Rider for the next hosted deploy: HPSMPOC-196, measuring the forwarded-header shape (GETs only).

## 2. Look actionable but are NOT (before Tuesday)
- HPSMPOC-235 BFF keep-alive needs the new `undici` dependency (Q-B187-1 PROPOSAL), so Kam decides.
- HPSMPOC-237 is a decision about money (plan size), so Kam. HPSMPOC-224 (telemetry) means a new OpenTelemetry package plus hosted settings: a new dependency and infra, so Kam.
- Q-B194-2: the web's MI warm-up timed out. Changing the sign-in budgets is auth work; the web was unchanged, so treat it as a data point for Friday.
- Q-B192-1: Friday has ruled the 207 retry stays narrow until a socket reset is reproduced. Do not widen it.
- HPSMPOC-187 second half (the repeated action sentence) is not ruled by Kam (comment 38894) and the text is driven by content.
- HPSMPOC-203 (file name after a rename) is Kam's call under C-29. HPSMPOC-204 (PDF caption) and HPSMPOC-228 N-7 (alert titles) are wording for Kam.
- HPSMPOC-178 / 177 (hidden characters in the customer name / feedback comment) wait for Kam's word.
- HPSMPOC-193 (forwarded-address residual, live since C-59) is a security setting and needs Kam's ruling.
- HPSMPOC-180 (rules-schema version bump) changes every ruleset hash, so it needs a planned re-issue.
- HPSMPOC-60 (happy path on Demo) writes to the hosted demo: approval class.
- HPSMPOC-99 N-4 (Kam's Automation rule) and N-9 (scale-out); HPSMPOC-109 O-1 (delivery proof needs a credential or rule change).
- HPSMPOC-98 "filter by state" and HPSMPOC-94/162/165/168 are new features.
- HPSMPOC-154 and HPSMPOC-117 are decisions or platform limits; HPSMPOC-100 is privacy/retention for Kam.
- Waiting on HP: 82–86, 97, 166, 181, 241. SME or content: 31, 37, 44, 46, 61, 87, 88, 91, 95, 163, 167.
- SM integration (191, 220, 229, 240) needs an HP device, imports switched on, and HP SM material. Hold it: Restricted-document risk.
- SOW, governance and epics (1–21, 51, 57, 58, 62–64, 169–176) belong to Kam or HP.

## 3. Stale (open record vs main / evidence)
- **HPSMPOC-155** says "CI has no SQL Server". CI has had an `api on SQL Server` job since #112/#113 (`ci.yml:152–161`, "HPSMPOC-216 … extends HPSMPOC-155"), and B194's CI run 38013337823 was green on both SQL Server legs.
- **HPSMPOC-152** is open (Backlog), but the fix merged in PR #104 (`e787727`, an ancestor of 5a93aa3; comment 39001). A scan of `api/` on main finds 0 raw U+202A–202E / U+2066–2069.
- **HPSMPOC-127** is open, but #99 `04aae93` (templates 1.0.2, C-54) is an ancestor of the live 5a93aa3. Comment 38939, "hosted still runs 1.0.1", is no longer true. Closing it is Friday's call (Q-B127-2).
- **HPSMPOC-98** still says "no screen yet". `AdminFeedback.tsx` has been on main since #120 (`547d3ea`), with attempts added in #129 (`3a9288a`), and it rendered live in B194 BLUF 6. Only "filter by state" is unbuilt.
- **HPSMPOC-232** says "~2.4 s" (summary) and "2,698 ms" (39299). B194 measured 6,197 ms with caller 4,496. The brief's "~2.7 s" comes from B191.
- **HPSMPOC-207** "returns on some starts": its last data point is B191 (39301). The B194 start had 0 `fail:` lines, no 3211/3213/3214, and the retry was not exercised. None of this is on the ticket.
- **HPSMPOC-228 N-2** says "readiness PDF keeps 10 s", but `bff.ts:162` DOWNLOAD_READS has given it 30 s since B180 (#125). Only the dead `:149` regex remains.
- **HPSMPOC-87/88/90/95 are "In Progress"**, but they are built, merged (#51, #54, #52 + route A) and live. What remains is content approval, HP vetting or Kam's N-4. **HPSMPOC-148/149/134** have only residuals left after #104/#105.
- **HPSMPOC-60** comments say "no Demo environment"; the hosted demo has been live since C-74.
- **The project's `BACKLOG.md`** still shows "Blocking W1" (09-23). Its B06/B07 follow-ups are already done: the EF lost-insert `fail:` was fixed by ADR-A26 (B08), and the partner self subject by ADR-A25. **`CLAUDE.md` Status** says "Nothing built … no git repo yet", but main 5a93aa3 is live.
- **Analysis repo:** origin/main ends at C-81, and C-82 exists only on `records/b194`. The local `main` is ahead 2 / behind 108, with `history.md` modified. A records seat must start from origin/main, not the local checkout.
