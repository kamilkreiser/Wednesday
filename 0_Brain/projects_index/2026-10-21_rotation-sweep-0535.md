# Rotation sweep: Datasec feedback delta (Part 1) + ticket sweep (Part 2), 2026-10-21, 05:35

A read-only sub-agent (claude-sonnet-5-5) ran this for Tuesday. Clock from the shell: `date` = **Wed 21 Oct 2026 05:31:40 AEDT** (Tue 20 Oct 18:31:40Z) at start and **05:34:24 AEDT (18:34:24Z)** at the last read. Window closes at that last read. Every time below is from a `date` I ran or from the API record.

Method, instruments, controls and table shape copied from [[2026-10-21_rotation-sweep-0115]]. Part 1 window opens at that file's "OUTBOUND watermarks for the next sweep", quoted here:

- Mailbox: at or after **2026-10-20T12:47:15.000Z**.
- Jira: RD `>= "2026-10-20 23:00"`; HPSMPOC `>= "2026-10-20 22:05"`; MPSCALC (excluded) `>= "2026-10-20 23:50"`; VSP and HPSM `>= "2026-10-19 19:35"` (all AEDT).
- GitHub: `since=2026-10-20T13:54:00Z`.

Facts are marked **MEASURED** (I ran it, instrument named), **RELAYED** (quoted from a file or ticket text) or **UNMEASURED**. Where a table row has no mark it is MEASURED by the instrument in section 2.

---

# PART 1: feedback delta

## 1. BLUF

**Needs Kam from a client human: nothing. New feedback items: 0 across all projects. New client-human responses: 0. No ticket needed.** The window (about 4 h 45 min on the mailbox, longer on Jira) is fleet work only: NexusAI PR #97 merged (04:12 AEDT), PR #101 (RD-874/-875) and #102 (records) opened, RD-876/-877/-878 filed from gate 29; HPSM-POC PR #165 merged (HPSMPOC-301/-302), PR #166 opened, HPSMPOC-305 filed from gate B357; MPS PRs #91 and #92 merged; Composer PR #85 pushed to `e969ad3`. The only mail is fleet traffic (an MPS seat question and a NexusAI QA gate 29 status thread), none from a client or Kam.

| Project | New feedback items | Client-human responses | Other activity in window (not feedback) |
|---|---|---|---|
| **NexusAI** (RD) | **0** | **0** | Jira: 11 touched; 5 "created in window" by my predicate, of which RD-874/-875 (23:03) are edge overlap with the 0115 file and **RD-876, RD-877, RD-878 are new** (05:01:42, 05:02:11, 05:02:17 AEDT; labels `b362-2026-10-21` / `gate-29`; all Low, To Do; filed by the B362 landing seat from gate 29 rows N29-6, N29-4, N29-2). `project = RD` total **871 -> 874**. 5 comments, all "BLUF:" seat voice (RD-873, -875, -874, -798 at 05:02; RD-873 23:02:46 is overlap). GitHub: main `115a775b` (commit date 12:45:48Z, before the `since` edge, so 0 commits by date; **PR #97 merged_at 2026-10-20T17:12:04Z**, 8 files); **new PR #101** (open, `rd-874-875-test-guards-uat-port-r11`, head `6e947f4`, 6 files, created 15:43:44Z, **mergeable_state dirty**); **new PR #102** (open, `records/b362`, head `6dcbedb`, 1 file `HISTORY.md`, created 18:06:15Z, state unstable); PR #67 open, unchanged. 0 issue comments, 0 review comments. Mail: QA gate 29 thread (see section 2). |
| **Vision Portal** (VSP) | **0** | **0** | None. Jira 89 unchanged (Done 73, Backlog 16); main `6dbffdf3` (09-28), Dependabot PRs #14-#17 unchanged. |
| **Vision QuickQuote** | **0** (no `QuickQuote feedback (` mail in window) | **0** | None. Main `5fa1187b` (10-18T09:57Z), PR #8 open, unchanged. |
| **Security Composer** | **0** | **0** | GitHub: main `308b7aa6` unchanged, 0 commits since the edge; **PR #85** (open draft) head `2756160` -> **`e969ad3`**, updated 15:23:58Z (02:23:58 AEDT), 57 files (was 56), mergeable clean. 0 issue / review comments. Decision store not re-read (UNMEASURED this run). |
| **MPS Calculator** (MPSCALC, *excluded*) | 0 seen | **0** | Jira: 26 touched; MPSCALC-306..315 listed by my predicate are edge overlap with the 0115 file (filed 23:51-23:53; window opened 23:50); newer: MPSCALC-304/-305 comments 05:03 (QA gate B365 on PR #92), -306..-311 and -245 comments 03:35 (QA gate B354 on PR #91). `project = MPSCALC` total **315** unchanged. 22 of the in-window comments are "BLUF:" seat / QA voice (list below counts all 26 touched). Summary "feedback" 0 / 13 total; label 0 / 0. GitHub: main `7bd7046a` -> **`1eccbc8b`** (2 commits by date: `f78c6408` 16:19:40Z, `1eccbc8b` 17:52:03Z); **PR #91 merged 16:19:41Z**, **PR #92 new and merged 17:52:04Z** ("MPSCALC-304 + MPSCALC-305 ..."). 0 open PRs. Mail: 1 seat QUESTION (the watermark row). |
| **HPSM-POC** (HPSMPOC, *excluded*) | 0 submissions seen | **0** | Jira: 16 touched; **HPSMPOC-305 created** (04:09:31, `b357-gate`, Backlog, Medium, B357-2 test gap on the merged FailOnceAsync guard); comments 02:14 (PR #165 pushed, -301/-302), 04:09-04:10 (QA gate B357, -301/-302), 04:30 (PR #166 pushed, -294/-295); the 22:05 deploy comments and -303/-304 are edge overlap. Total **304 -> 305**. Summary "feedback" 2 in window (HPSMPOC-303 overlap; HPSMPOC-294 "Feedback utf-7 tests", a seat test ticket) / **25** total; label 2 in window (HPSMPOC-290 overlap; -294) / **20** total. None is a submission. GitHub: code repo main `c149a303` -> **`6818896b`** (PR #165 merged 16:16:57Z, "HPSMPOC-301 + HPSMPOC-302 ..."); **PR #166 new** (open, `b364/feedback-pkcs-test-gaps-294-295`, head `4794bde`, 2 files, clean). **Analysis repo main `93ee2e0b` -> `e2a0d721`** (3 commits to 17:25:14Z, merge of PR #126 "Records B363: C-127 ..."). |
| **HPSM** (HPSM) | 0 | 0 | Jira none (41 unchanged; Backlog 25, Done 16). GitHub **UNMEASURED** (`gh` not logged in under `HPSM/4_Credentials/.gh-config`: the call returns the "gh auth login" prompt, as on earlier sweeps). |

**Actionable items: none.** There are no feedback items to categorise. RD-876/-877/-878 and HPSMPOC-305 are seat-filed from QA gate findings, not client submissions. (Note RD-876 states it is "a decision for the owner" in its summary: a Datasec product-owner call about a row cap, filed by a seat, not a client message.)

## 2. Method and controls

### Mailbox (tuesday-agent@agentmail.to), read 05:32 AEDT
- `GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`, paged by `page_token` to the end: **3,749 messages, 38 pages** (0115 read: 3,742, so +7); newest **2026-10-20T16:51:18.000Z** (03:51:18 AEDT), oldest 2026-09-08T21:47:13Z. Subjects, senders and timestamps only; no bodies read. No subject names Secuura or another client.
- **8 messages from the watermark on** (the watermark message plus 7), subjects: `[Datasec/MPS Commercial Calculator -> Tuesday] QUESTION: leave-flush vs the existing pin autosave.test:124` (12:47:15Z, the watermark; seat to Tuesday); `[QA/Datasec-NexusAI -> Tuesday] STATUS: flagged ...Opus 4.8 switch` (14:47:56Z); `[Wednesday -> QA/NexusAI-gate29] ANSWER: Opus 4.8 switch done, resume at r7 S4` (14:49:46Z, from the Tuesday seat); `GATE VERDICT — gate 29` (16:45:58Z); Tuesday seat ANSWER `verdict received, release your three servers` (16:47:23Z); `STATUS: servers released — gate 29` (16:49:05Z); Tuesday seat ANSWER `three qa-srvup29 helpers still running` (16:50:27Z); `STATUS: qa-srvup29 helpers released — gate 29` (16:51:18Z). All from `coagent@` (QA / MPS seats) or `tuesday-agent@` (the Tuesday seat itself). No row from a client, `datasec-vision@`, Kam forwards or `wednesday-agent@`.
- `coagent@agentmail.to` also listed (4,676 messages, 47 pages), filtered to subjects containing "Datasec/" or "-> Tuesday": the 2 inbound rows above are the only matches in the window (copies of the same two threads). The remaining rows in the window (5 rows, newest 18:30:06Z) matched neither filter and were skipped unread.
- **0 feedback notices, 0 client senders**; no subject in the window contains "feedback".
- **Control 1 (continuity):** the watermark message (12:47:15.000Z) comes back in the same call.
- **Control 2 (instrument fires):** the same read returns **50** subjects containing "feedback" (newest 2026-10-17T04:56:13.000Z, a Kam forward) and **1** subject starting `QuickQuote feedback (` (as at 0115).

### Jira (JQL in AEDT; every list paged to its end; read 05:32)
Instrument: each project's own `4_Credentials/.env` (RD from NexusAI, VSP from Vision_Sales_Portal, HPSMPOC from HPSM-POC, MPSCALC from the MPS project, HPSM from HPSM) parsed in-process in `python3 -I`, never printed; `GET /rest/api/3/search/jql` (`maxResults 100`, `nextPageToken`) and `/issue/<key>/comment`; Jira returns AEDT (+11:00) offsets.

| Project | W | Result | Control |
|---|---|---|---|
| RD | `2026-10-20 23:00` | **11 touched**: RD-873, -875, -874, -798, -878, -836, -774, -877, -876, -789, -786; **RD-876/-877/-878 new** (RD-874/-875 overlap); 5 comments in window | `project = RD ORDER BY key` = **874** (0115: 871; +3 = RD-876, -877, -878). The window query returns 11, so the query fires. |
| RD | | `summary ~ "feedback"` in window 0 / total 21; `labels in (feedback, user-feedback, hp-feedback)` in window 0 / total 5 | totals unchanged from 0115 (21, 5) |
| VSP | `2026-10-19 19:35` | **0** touched | total 89 unchanged; summary 0 in window / **1** total (instrument matches); label 0 / 0. As on earlier sweeps, the in-window zero has no in-window positive control (newest update 2026-09-29); it rests on the unchanged total and the 1 summary match. |
| HPSM | `2026-10-19 19:35` | **0** touched | total 41 unchanged; summary 0 / 0, label 0 / 0 (HPSM has never had a feedback hit: no project-specific control). |
| HPSMPOC | `2026-10-20 22:05` | **16 touched** (-295, -294, -302, -301, -305, -304, -303, -268, -300, -299, -298, -263, -275, -293, -267, -290); 24 comments in the listing, all "BLUF:" seat / QA voice; newest change 04:30:33 | total **305** (0115: 304; +1 = HPSMPOC-305). Summary 2 / **25**, label 2 / **20**. |
| MPSCALC (*excluded*) | `2026-10-20 23:50` | **26 touched**; comments all "BLUF:" seat / QA voice (newest 05:03:21) | total **315** unchanged. Summary 0 / **13**, label 0 / 0 (totals unchanged). |

**Positive control (same script):** the feedback-labelled rows exist and are matched: RD summary 21 / label 5 total, HPSMPOC summary 25 / label 20 (2 / 2 in window, both seat tickets), MPSCALC summary 13, VSP summary 1. The window queries fire on RD (11), HPSMPOC (16) and MPSCALC (26).

**Client-human responses in Jira: 0.** The opening (about 110 characters) of every in-window comment (RD 5, HPSMPOC 24, MPSCALC 26 by listing) reads as seat / QA voice. The shared "Kamil Kreiser" account cannot separate Kam from a seat.

### GitHub (`gh api` GETs, `since=2026-10-20T13:54:00Z`, read 05:33 AEDT; each under its own project's `GH_CONFIG_DIR`)

| Repo | Commits on main since | Issues/PRs updated since | Issue / review comments since | Open PRs | Control: main HEAD |
|---|---|---|---|---|---|
| Reporting_Dashboard_Au (NexusAI) | 0 by commit date (see caveat) | **3**: #102 (new, open), #101 (new, open, dirty), #97 (merged 17:12:04Z) | 0 / 0 | #102, #101, #67 | `115a775b` 10-20T12:45:48Z |
| vision_datasec-sales-portal | 0 | 0 | 0 / 0 | #14-#17 (Dependabot) | `6dbffdf3` 09-28 |
| vision_hpas-quickquote | 0 | 0 | 0 / 0 | #8 | `5fa1187b` 10-18T09:57Z |
| Datasec-Security-Composer | 0 | **1**: #85 (open draft, updated 15:23:58Z, head `e969ad3`) | 0 / 0 | #85(d) | `308b7aa6` 10-20T10:11:07Z |
| HPSM-POC (*excluded*) | **1** (`6818896b` 16:16:57Z) | **2**: #166 (new, open), #165 (merged) | 0 / 0 | #166 | `6818896b` |
| HPSM-POC-analysis (*excluded*) | **3** (to `e2a0d721` 17:25:14Z) | **1**: #126 (merged) | 0 / 0 | none | `e2a0d721` |
| MPS-Commercial-Calculator (*excluded*) | **2** (`f78c6408` 16:19:40Z, `1eccbc8b` 17:52:03Z) | **2**: #92 (new, merged 17:52:04Z), #91 (merged 16:19:41Z) | 0 / 0 | none | `1eccbc8b` |
| HPSM (*excluded*) | **UNMEASURED** | | | | `gh` not logged in under HPSM's config |

**Controls:** the `since` filter fires on NexusAI (3), Composer (1), HPSM-POC (2), analysis (1) and MPS (2); on each zero repo (Vision Portal, QuickQuote) the pre-window HEAD is visible under the same credentials. **Comment endpoints:** issue comments re-run with `since=2026-09-01T00:00:00Z` returns NexusAI 6, QuickQuote 4, Composer 3, HPSM-POC 3, analysis 1, MPS 2 (Vision Portal returns 0 total there, so its zero comment count has no positive control); none since the watermark. Review comments re-run on NexusAI with `since=2026-10-19T00:00:00Z` returns **2**, so that endpoint fires; none since the watermark on any repo. Merged flags read from `pulls/<n>`: NexusAI #97, HPSM-POC #165, MPS #91 and #92 `merged: true`; NexusAI #101, #102 `merged: false`. All authors `kamilDatasec` (the shared account; seat PRs). **Caveat (MEASURED):** the commits-since filter keys on commit date, and NexusAI #97 (head `115a775`, commit date 12:45:48Z) merged at 17:12:04Z by a fast-forward/rebase, so the "0 commits" for NexusAI is a date artefact; the merge is visible only via `pulls/97`. Same may apply to any repo whose seat merges an older-dated head. No non-PR GitHub issue opened anywhere.

## 3. Window edges and watermarks out (Part 1)

Window: opened per the quoted watermarks; closed at the last read **05:34:24 AEDT (18:34:24Z)**. Read span 05:31:40-05:34:24 AEDT. Edges, AEDT / UTC:
- **Mailbox (tuesday-agent@):** newest message read 2026-10-20T16:51:18.000Z (03:51:18 AEDT 10-21; QA gate 29 qa-srvup29 helpers released). `coagent@` newest 18:30:06Z (non-Datasec rows, skipped).
- **Jira:** newest processed change RD **2026-10-21 05:02:56 AEDT** (RD-873 comment); HPSMPOC **04:30:33**; MPSCALC (excluded) **05:03:21**; VSP 2026-09-29, HPSM 2026-10-02 (unchanged).
- **GitHub:** newest item read: NexusAI PR #102 created and updated **2026-10-20T18:06:15Z** (05:06:15 AEDT 10-21). Next run `since=2026-10-20T18:06:00Z`. HPSM not measured, no edge advanced for it.

---

# PART 2: ticket sweep (agent-actionable tickets per project, re-run against the boards at 05:32-05:34 AEDT; delta against the 0115 file)

Part 2 is the compact form: counts and status are MEASURED by paginated Jira reads; PR file lists MEASURED from `pulls/<n>/files`; ticket descriptions MEASURED (opening ~700 characters) only for RD-876/-877/-878 and HPSMPOC-305; everything else is carried from the 0115 file and marked RELAYED. Composer `BACKLOG.md` was **not re-read** this run (UNMEASURED); the 0115 figures stand as RELAYED.

## 4. BLUF table

| Project | Tracker | Open total | By status | Class A (agent-actionable) | Owned by a live seat |
|---|---|---|---|---|---|
| NexusAI | Jira RD, **874** issues | **382** in To Do + In Progress (372 + 10); 366 more are Testing/Release Ready (167 + 199) | To Do 372, In Progress 10, Testing 167, Release Ready 199, Put on Hold 7, Done 117, Declined 2 (sums to 874) | New: **RD-877** (test gap), **RD-878** (500 vs 400); RD-876 is an owner decision, not class A. RD-874/-875 are now on PR #101 (not candidates). To Do by priority: Highest 2, High 44, Medium 176, Low 148, Lowest 2; In Progress High 4, Medium 4, Low 2 | PR #101 = RD-874 + RD-875 (conflicts with main, needs a forward-merge); PR #102 = records B362 (HISTORY.md). RD-774 + RD-836 landed (PR #97 merged); both still show **In Progress** on the board (MEASURED) |
| HPSM-POC | Jira HPSMPOC, **305** issues | **113** (`statusCategory != Done`) | Backlog 110, In Progress 3 (-87, -90, -91), Done 192 | 0115 list less -301/-302 (landed, PR #165) and -294/-295 (PR #166 open); plus new **HPSMPOC-305** (Medium, test, `before-imports-on-hosted`) | PR #166 = HPSMPOC-294 + HPSMPOC-295 (2 test files); no other open PRs |
| Security Composer | `BACKLOG.md` (RELAYED, records main `348e5087` at 0115) | RELAYED 125 of 355 parsed rows | RELAYED | RELAYED carry: #363, #364, #57, #152, #178, #104 | **PR #85** (draft, now 57 files, head `e969ad3`) |
| MPS Calculator | Jira MPSCALC, **315** issues | **301** (all Backlog) | Backlog 301, Done 14. Tickets of merged PRs #91 and #92 are still Backlog (board does not move on merge, MPSCALC-304 text) | non-epic open 286; label-clean 243 (label-based upper bound, not comment-read) | none (0 open PRs) |
| Vision Portal | Jira VSP, **89** | **16** (all Backlog) | Done 73, Backlog 16; unchanged since 2026-09-29 | RELAYED carry: VSP-81, VSP-87 buildable; others have unmerged branches | none |
| Vision QuickQuote | no Jira; GitHub | not re-counted | PR #8 open (puppeteer 25), unchanged | nothing new that avoids the production gate | none |
| HPSM (excluded) | Jira HPSM, **41** | 25 (Backlog) | Done 16, Backlog 25; counted only | n/a | n/a |

**Changes since the 0115 sweep (all MEASURED):** RD 871 -> **874** (RD-876..878 created); NexusAI PR #97 merged, PR #101/#102 opened; HPSMPOC 304 -> **305** (-305 created; PR #165 merged, PR #166 opened); MPS PRs #91 and #92 merged, no open PR; Composer PR #85 56 -> 57 files; MPSCALC total unchanged at 315.

## 5. LANE CANDIDATES for Tuesday

Up to 4 per in-scope project. Selection: class A, no client-human input, not Kam's signature class. "Files" are RELAYED from ticket text unless marked MEASURED. **Live seats (MEASURED):** PR #101 (NexusAI: `__tests__/auth-gate-fail-closed.test.js`, `__tests__/rd395-ai-enabled-unreadable-store.test.js`, `__tests__/rd875-uat-run-target-and-port.test.js`, `__tests__/scim-security-controls.test.js`, `scripts/verify-expected-counts.json`, `tests/uat-run.js`); PR #102 (`HISTORY.md`); PR #166 (HPSM-POC: `api/tests/HpsmPoc.Api.Tests/PkcsInPackageTests.cs`, `api/tests/HpsmPoc.Modules.Feedback.Tests/Hpsmpoc290Tests.cs`); Composer PR #85 (57 files).

### NexusAI (Reporting_Dashboard_Au)
| Key | Summary | Status | Files it most likely touches | Collision |
|---|---|---|---|---|
| **RD-878** | PUT /api/risk-conditions/:id with a non-string `risk_level` answers 500 instead of 400 (`toLowerCase()` throws) (gate 29 N29-2) | To Do, Low (MEASURED) | `backend/server.js` risk-condition PUT handler and a test (RELAYED from the title; handler location not opened) | PR #101: none on the files. Touches the code PR #97 just landed; no live seat in that code. Same family as RD-877/RD-876. |
| **RD-877** | Two mutants survive the rd774 + security-fixes suite with 0 red: `page_count_above` `>` to `>=` (M10) and the validate-condition save gate weakened to `=== true` (M14b) (gate 29 N29-4) | To Do, Low (MEASURED) | the rd774 / security-fixes test files from PR #97 (8 files, MEASURED at 0115: `security-fixes.test.js`, `rd774-*`) plus possibly `scripts/verify-expected-counts.json` | PR #101 also edits `scripts/verify-expected-counts.json` (text-conflict risk only if a new test file is added). Order with RD-878. |
| **RD-814** | CodeQL baseline: `actions/missing-workflow-permissions` x3 | To Do, Medium | `.github/workflows/build.yml`, `deploy.yml`, `npm-audit.yml` (RELAYED, carried) | none with PR #101/#102. |
| **RD-780** | CodeQL baseline: `js/regex/missing-regexp-anchor` x2 in a developer script | To Do, High | `scripts/propose-dark-retheme.js` (RELAYED, carried) | none. |

Not candidates: **RD-876** (default risk template without a hard LIMIT 100; ticket text calls it "a decision for the owner": needs a Datasec product-owner ruling, so Kam-class); RD-874/-875 (PR #101, live); RD-873 (RD-786 remainder; its 05:02 comment says N30-2 is RD-875's now, so its scope shrank; seat unmeasured). **NexusAI open PRs (MEASURED):** #101 (6 files, **mergeable_state dirty**: needs a forward-merge against main), #102 (1 file, unstable), #67 (3 files, dirty, unchanged since 10-07).

### HPSM-POC (HPSM-POC repo; PR #166 open; no seat in the import code)
| Key | Summary | Status | Files | Collision |
|---|---|---|---|---|
| **HPSMPOC-305** | [B357-2] Import FailOnceAsync guard tests: two mutants (gd, gr) survive the committed suite; no row plants a swept run with rows or a non-null reason (MEASURED opening) | Backlog, Medium (`before-imports-on-hosted`, `test`) | tests of the merged guard in `api/tests/HpsmPoc.Api.Tests/Imports/*`, source `ImportEndpoints.cs` (FailOnceAsync) (RELAYED from the -301 carry) | none with PR #166 (different test files). Pin against a later change, not a defect (ticket text). |
| **HPSMPOC-288 / -289** | `web/src/server/formGate.ts` + tests (RELAYED, carried from 0115) | Backlog | `web/src/server/formGate.ts` and tests | none with PR #166. |
| **HPSMPOC-292** | SQLite migrations (RELAYED, carried) | Backlog | migrations | none. |
| **HPSMPOC-296 / -297** | web e2e (RELAYED, carried) | Backlog | web e2e | none. |
Landed or live (so no longer candidates): -301/-302 (PR #165 merged), -294/-295 (PR #166, gate next). Not candidates: -303 (hosted zip deploy script), -304 (Azure VM cleanup), `needs-kam` rows.

### Security Composer (B353 live on PR #85, now 57 files)
RELAYED from 0115, not re-verified this run: candidates #363 (`apps/web/src/screens/b116-s10-verify-dom.test.tsx`), #364 (`packages/engine/test/s47-crf2-linear-detector.test.ts`), #57 (`Discovery.tsx`), #152 (one new migration + rollback; migration-number clash risk with the L3-x lane). The collision picture against PR #85 (56 -> 57 files) was not re-measured; check the new 57th file before assigning any `packages/engine` lane.

### MPS Calculator (no open PR; no live seat)
The 0115 collision list is gone: PR #91 and #92 merged, 0 open PRs (MEASURED). RELAYED from 0115 (files from ticket text, unopened): **MPSCALC-289** (`QuoteEndpoints.cs:566-576` CopyRef surrogate split), **MPSCALC-292** (`tests/MpsCalc.Engine.Tests/ReconciliationTests.cs:457-476`), **MPSCALC-288 / -291 / -294 / -293**. MPSCALC-304 and -305 are landed (PR #92, QA gate B365 comments GO / GO WITH FINDINGS at 05:03) but the board still shows Backlog. MPSCALC-306..311 landed with PR #91 (gate B354). -310/-312..-315 stay open; collision with a live seat none now (UNMEASURED who, if anyone, is on them). MPS is outside the feedback actions but read for activity.

### Vision (Portal repo; no live seat; production work is Kam-gated)
RELAYED from 0115, unchanged (Jira and GitHub unchanged): VSP-81, VSP-87 (`server/dbRestore.js` etc.; unmerged branches `vsp-83-*`, `vsp-86-*` likely edit `dbRestore.js`), VSP-84 (`server/dbBackup.js`), VSP-72 (file not established). QuickQuote: no ticket store; PR #8 is Kam-ruled and unchanged; no candidate that avoids the production gate. HPSM: counts only.

## 6. Part 2 method, predicates and controls

- **Jira counts:** `project = <KEY> ORDER BY key` paged to its end, grouped by status in-process: RD 874 (To Do 372, In Progress 10, Testing 167, Release Ready 199, Put on Hold 7, Done 117, Declined 2; sums to 874); HPSMPOC 305 (Backlog 110, In Progress 3, Done 192); MPSCALC 315 (Backlog 301, Done 14; non-epic open 286, none of `needs-ruling` / `question-for-kam` / `phase-2` / `lane-later` 243); VSP 89 (Done 73, Backlog 16); HPSM 41 (Backlog 25, Done 16). Control: the RD, VSP, HPSM and MPS totals match the 0115 figures except the expected RD +3.
- **PR facts:** `pulls/<n>`, `pulls/<n>/files` via `gh api` under each project's own `GH_CONFIG_DIR`. Not run this run: `commits/<sha>/check-runs`.
- **Descriptions read:** RD-876, -877, -878 and HPSMPOC-305 (opening ~700 characters). No other ticket text read; all other fields are carried from 0115 (RELAYED).
- **Decision store, Composer BACKLOG.md, Portal branch list:** not re-read (UNMEASURED this run).
- **Live-seat exclusions:** PR #101, #102 (NexusAI), PR #166 (HPSM-POC), PR #85 (Composer).

## 7. UNMEASURED
- **Every live feedback store:** MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, the NexusAI share `feedbackItems`, Portal Postgres, the QuickQuote table. Each needs az, a writing sign-in or HTTP to a hosted host, all out of bounds. **"0 new" means only that nothing reached the mailbox, Jira or GitHub.**
- **Who wrote a Jira comment:** the shared account cannot tell Kam from a seat; only openings (about 110 characters) were read.
- **HPSM GitHub:** `gh` not logged in under HPSM's config.
- **Mail bodies** not read; the 5 `coagent@` rows that matched neither subject filter were skipped unread. The MPS QUESTION (12:47:15Z) and the gate 29 thread are listed by subject only.
- **Commits-since by commit date** can miss a merge of an older-dated head (see the caveat in section 2); merges were cross-checked through `pulls/<n>` only for PRs named above.
- **Vision Portal comment endpoint** has no positive control (0 comments total since 09-01).
- **Kam's card board and decision store** not read this run; any ruling after the last sweep is not reflected in the lanes. Composer `BACKLOG.md`, check-runs on the new PRs, who (if anyone) is on RD-873 / RD-877 / RD-878, and whether PR #101 conflicts only in `verify-expected-counts.json` are unmeasured.
- **File lists:** outside the PR file lists, candidate files are from ticket text (RELAYED), unopened.
- No HTTP to any app host, hosted site or production (only the AgentMail API, Jira Cloud search and comment reads, and `api.github.com`); no az, docker or ssh; no git commands in any project repo; no Jira, gh, mail or card writes. Temporary scripts lived in the session scratchpad.

## OUTBOUND watermarks for the next sweep

- Mailbox: at or after **2026-10-20T16:51:18.000Z** (tuesday-agent@; coagent@ newest seen 2026-10-20T18:30:06.000Z).
- Jira: RD `>= "2026-10-21 05:00"` (newest change 05:02:56); HPSMPOC `>= "2026-10-21 04:30"` (newest change 04:30:33); MPSCALC (excluded) `>= "2026-10-21 05:00"` (newest change 05:03:21); VSP and HPSM `>= "2026-10-19 19:35"` (all AEDT).
- GitHub: `since=2026-10-20T18:06:00Z`.
