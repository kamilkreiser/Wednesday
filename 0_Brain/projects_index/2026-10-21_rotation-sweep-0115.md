# Rotation sweep: Datasec feedback delta (Part 1) + ticket sweep (Part 2), 2026-10-21, 01:15

A read-only sub-agent (claude-sonnet-5-5) ran this for Tuesday. Clock from the shell: `date` = **Wed 21 Oct 2026 01:13:39 AEDT** (Tue 20 Oct 14:13:39Z) at start and **01:22:01 AEDT (14:22:01Z)** at the last read. Window closes at that last read. Every time below is from a `date` I ran or from the API record.

Method, instruments, controls and table shape copied from [[2026-10-20_rotation-sweep-2240]] (Part 1) and [[2026-10-20_morning-sweep-0600]] (Part 2 predicates and orders). Part 1 window opens at the 22:40 file's "OUTBOUND watermarks for the next sweep", quoted here:

- Mailbox: at or after **2026-10-20T11:13:55.000Z**.
- Jira: RD `>= "2026-10-20 19:55"`; HPSMPOC `>= "2026-10-20 22:05"`; MPSCALC (excluded) `>= "2026-10-20 22:15"`; VSP and HPSM `>= "2026-10-19 19:35"` (all AEDT).
- GitHub: `since=2026-10-20T11:34:00Z`.

Facts are marked **MEASURED** (I ran it, instrument named), **RELAYED** (quoted from a file or ticket text) or **UNMEASURED**. Where a table row has no mark it is MEASURED by the instrument in section 2.

---

# PART 1: feedback delta

## 1. BLUF

**Needs Kam from a client human: nothing. New feedback items: 0 across all projects. New client-human responses: 0. No ticket needed.** The window (about 2 h 40 min to the mailbox edge, longer on Jira) is fleet work only: MPS merged PRs #89 and #90 (V2 Home and V1 phase 2) and opened PR #91 (B352 follow-ups); NexusAI filed RD-874/RD-875 (gate 32 residues, seat-filed) and moved PR #97 to head `115a775`; Composer pushed PR #85 to `2756160`; MPS seats filed MPSCALC-306..315 from QA gates B347/B348; HPSM-POC analysis merged PR #125 (Records B346). The only new mail is one MPS seat question (coagent bus), not from a client or from Kam.

| Project | New feedback items | Client-human responses | Other activity in window (not feedback) |
|---|---|---|---|
| **NexusAI** (RD) | **0** | **0** | Jira: 10 touched (RD-863, -869, -870, -872 and -811 are edge overlap with the 22:40 file; **RD-786, -789, -873 touched 23:03**; **RD-874 and RD-875 created 23:03:34 and 23:03:35**, labels `b343-2026-10-20` / `gate-32` / `test-quality`, Low, To Do, filed by the PR #98 landing seat). `project = RD` total **869 -> 871**. 2 comments: RD-786 20:00:18 "BLUF: gate 30 round 1 found one Major ..." (overlap) and **RD-873 23:02:46** "BLUF: RD-873 now also carries alert #116 ..." (seat voice). GitHub: main `d463f881` unchanged (10:09:38Z), 0 commits since the edge; **PR #97** (open draft) head `278afc2` -> **`115a775`**, updated 13:37:37Z (00:37:37 AEDT), 8 commits, mergeable clean; PR #67 open, unchanged (mergeable **dirty** against main). #98 shows as updated 12:05:40Z (already merged, 22:16 AEDT yesterday). 0 issue comments, 0 review comments. Mail: none for NexusAI. |
| **Vision Portal** (VSP) | **0** | **0** | None. Jira 89 unchanged (newest update 2026-09-29 07:05); main `6dbffdf3` (09-28), Dependabot PRs #14-#17 unchanged. |
| **Vision QuickQuote** | **0** (no `QuickQuote feedback (` mail in window) | **0** | None. Main `5fa1187b` (10-18T09:57Z), PR #8 open, unchanged. |
| **Security Composer** | **0** | **0** | GitHub: main `308b7aa6` unchanged (10:11:07Z), 0 commits since the edge; **PR #85** (open draft, "HOLD K6: L1 SM 3.16 content catalogue") head `40b332c` -> **`2756160`**, updated 12:16:58Z (23:16:58 AEDT), 8 commits, 56 files, mergeable clean. 0 issue / review comments. Decision store: 3 open Composer cards (`composer-l05-setup-card-too-1014`, `composer-demo-deploy-eaff2b7-words-1020`, `composer-contents-word-pr84-1020`). |
| **MPS Calculator** (MPSCALC, *excluded*) | 0 seen | **0** | Jira: 24 touched; **10 created: MPSCALC-306..315** (23:51:33-23:53:31 AEDT, labels `mpscalc-b351` / `plan-b351-*`, all Backlog, seat-filed from QA gates B347 [PR #89] and B348 [PR #90]); `project = MPSCALC` total **305 -> 315**. 26 comments, all "BLUF:" seat / QA voice (QA gate verdicts B347 on PR #89 @ 0d7250e and B348 on PR #90 @ 5f0bd02 at 23:55; the 22:19 "pushed @ 5f0bd02" comments are edge overlap). Summary "feedback" 0 in window / 13 total; label 0 / 0. GitHub: main `67bf2004` -> **`7bd7046a`** (2 commits: `d2b956b7` 11:41:17Z "MPSCALC-244/-28/-245: v13 lane V2 Home ...", `7bd7046a` 12:30:16Z "MPSCALC-239/-242/-27/... v13 lane V1 phase 2"); **PR #89 merged** 11:41:17Z, **PR #90 merged** 12:30:16Z; **PR #91 new** (open, non-draft, branch `b352/followup-overflow-e2e-autosave-flush`, head `5295ff7`, created 13:54:02Z, "MPSCALC-306/-307/-308/-309: follow-up ...", 6 commits, 12 files, mergeable clean). Mail: 2 rows (see section 2). Note: the B348 comment text says "PR #90 ... (not merged)" at 23:55 AEDT, while GitHub shows #90 merged at 12:30:16Z (23:30:16 AEDT). |
| **HPSM-POC** (HPSMPOC, *excluded*) | 0 submissions seen | **0** | Jira: 11 touched, all at or before 22:07:42 AEDT (edge overlap with the 22:40 sweep: the 22:05:49-22:05:57 deploy comments on -263, -267, -268, -275, -290, -293, -298, -299, -300; -303/-304 created 22:07). **Nothing newer.** Total **304** unchanged. Summary "feedback" 1 in window (HPSMPOC-303, seat finding) / **25** total; label 1 (HPSMPOC-290) / **20** total, both unchanged. GitHub: code repo main `c149a303` unchanged, no open PRs. **Analysis repo main `9af1d55a` -> `93ee2e0b`** (1 commit, 11:43:07Z, "Merge pull request #125 from datasecau/records/b346"; PR #125 "Records B346: C-124..C-126 (WU window, SM VM access, policy shape) ..." merged 11:43:08Z). Decision store: open card `hpsmpoc-sm-vm-budget-24x7-1020`. |
| **HPSM** (HPSM) | 0 | 0 | Jira none (41 unchanged). GitHub **UNMEASURED** (`gh` not logged in under `HPSM/4_Credentials/.gh-config`: the call returns the "gh auth login" prompt, as on earlier sweeps). |

**Actionable items: none.** There are no feedback items to categorise. RD-874/-875 and MPSCALC-306..315 are seat-filed from QA / gate findings, not client submissions.

## 2. Method and controls

### Mailbox (tuesday-agent@agentmail.to), read 01:14 AEDT
- `GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`, paged by `page_token` to the end: **3,742 messages, 38 pages** (22:40 read: 3,741, so +1); newest **2026-10-20T12:47:15.000Z** (23:47:15 AEDT, about 1 h 27 min before read time), oldest 2026-09-08T21:47:13Z. Subjects, senders and timestamps only; no bodies read. No subject names Secuura or another client.
- **2 messages from the watermark on** (the watermark message plus 1): both `CoAgent <coagent@agentmail.to>`: `[Datasec/MPS Commercial Calculator -> Tuesday] QUESTION: CodeQL not running on PR 89 (B347/G25)` 11:13:55Z (the watermark) and **`[Datasec/MPS Commercial Calculator -> Tuesday] QUESTION: leave-flush vs the existing pin autosave.test:124`** 12:47:15Z (new, a seat-to-Tuesday question). No row from `tuesday-agent@`, `datasec-vision@`, Kam forwards or `wednesday-agent@` in the window.
- **0 feedback notices, 0 client senders**; no subject in the window contains "feedback".
- **Control 1 (continuity):** the watermark message (11:13:55.000Z) comes back in the same call.
- **Control 2 (instrument fires):** the same read returns **50** subjects containing "feedback" (newest 2026-10-17T04:56:13.000Z, a Kam forward) and **1** subject starting `QuickQuote feedback (` (as at 22:40).

### Jira (JQL in AEDT; every list paged to its end; read 01:14-01:20)
Instrument: each project's own `4_Credentials/.env` (RD from NexusAI, VSP from Vision_Sales_Portal, HPSMPOC from HPSM-POC, MPSCALC from the MPS project, HPSM from HPSM) parsed in-process in `python3 -I`, never printed; `GET /rest/api/3/search/jql` (`maxResults 100`, `nextPageToken`) and `/issue/<key>/comment`; Jira returns AEDT (+11:00) offsets.

| Project | W | Result | Control |
|---|---|---|---|
| RD | `2026-10-20 19:55` | **10 touched**: RD-863, -869, -870, -872, -811, -786, -874, -789, -873, -875; **2 created** (RD-874, -875, 23:03); 2 comments | `project = RD ORDER BY key` = **871** (22:40: 869; +2 = RD-874, -875). Prior-window query (`updated >= "2026-10-20 12:45"`) returns **14**, so the query fires. |
| RD | | `summary ~ "feedback"` in window 0 / total 21; `labels in (feedback, user-feedback, hp-feedback)` in window 0 / total 5 | totals unchanged from 22:40 (21, 5) |
| VSP | `2026-10-19 19:35` | **0** touched | total 89 unchanged; summary 0 in window / **1** total (instrument matches); label 0 / 0. As on earlier sweeps, the in-window zero has no in-window positive control (newest update 2026-09-29); it rests on the unchanged total and the 1 summary match. |
| HPSM | `2026-10-19 19:35` | **0** touched | total 41 unchanged; summary 0 / 0, label 0 / 0 (HPSM has never had a feedback hit: no project-specific control). Newest update 2026-10-02. |
| HPSMPOC | `2026-10-20 22:05` | **11 touched** (-290, -267, -293, -275, -263, -298, -299, -300, -268, -303, -304), 9 comments, all "BLUF:"; newest change 22:07:42 | total **304** unchanged. Summary 1 / **25**, label 1 / **20** (HPSMPOC-303 and HPSMPOC-290, both read at 22:40). Prior window (`>= "2026-10-20 11:30"`) returns **13**. |
| MPSCALC (*excluded*) | `2026-10-20 22:15` | **24 touched**, **10 created** (MPSCALC-306..315); 26 comments, all "BLUF:" seat / QA voice | total **315** (22:40: 305; +10). Summary 0 / **13**, label 0 / 0 (totals unchanged). Prior window (`>= "2026-10-20 12:40"`) returns **57**. |

**Positive control (same script):** the feedback-labelled rows exist and are matched: RD summary 21 / label 5 total, HPSMPOC summary 25 / label 20 (1 / 1 in window), MPSCALC summary 13, VSP summary 1. The window queries fire on RD (10), HPSMPOC (11) and MPSCALC (24).

**Client-human responses in Jira: 0.** The opening (about 110 characters) of all 37 in-window comments (2 RD, 9 HPSMPOC, 26 MPSCALC) reads as seat / QA voice. The shared "Kamil Kreiser" account cannot separate Kam from a seat.

### GitHub (`gh api` GETs, `since=2026-10-20T11:34:00Z`, read 01:15-01:22 AEDT; each under its own project's `GH_CONFIG_DIR`)

| Repo | Commits on main since | Issues/PRs updated since | Issue / review comments since | Open PRs | Control: main HEAD |
|---|---|---|---|---|---|
| Reporting_Dashboard_Au (NexusAI) | 0 | **2**: #98 (merged earlier, updated 12:05:40Z), #97 (open draft, updated 13:37:37Z, head `115a775`) | 0 / 0 | #97(d), #67 | `d463f881` 10-20T10:09:38Z |
| vision_datasec-sales-portal | 0 | 0 | 0 / 0 | #14-#17 (Dependabot) | `6dbffdf3` 09-28 |
| vision_hpas-quickquote | 0 | 0 | 0 / 0 | #8 | `5fa1187b` 10-18T09:57Z |
| Datasec-Security-Composer | 0 | **1**: #85 (open draft, updated 12:16:58Z, head `2756160`) | 0 / 0 | #85(d) | `308b7aa6` 10-20T10:11:07Z |
| HPSM-POC (*excluded*) | 0 | 0 | 0 / 0 | none | `c149a303` 10-20T00:11:40Z |
| HPSM-POC-analysis (*excluded*) | **1** (`93ee2e0b` 11:43:07Z) | **1**: #125 (merged 11:43:08Z) | 0 / 0 | none | `93ee2e0b` |
| MPS-Commercial-Calculator (*excluded*) | **2** (`d2b956b7` 11:41:17Z, `7bd7046a` 12:30:16Z) | **3**: #91 (open, new, 13:54:02Z), #90 (merged 12:30:16Z), #89 (merged 11:41:17Z) | 0 / 0 | #91 | `7bd7046a` |
| HPSM (*excluded*) | **UNMEASURED** | | | | `gh` not logged in under HPSM's config |

**Controls:** the `since` filter fires on NexusAI (2), Composer (1), analysis (1) and MPS (3); on each zero repo (Vision Portal, QuickQuote, HPSM-POC) and on the zero-commit rows the pre-window HEAD is visible under the same credentials. **Comment endpoints:** issue comments re-run with `since=2026-09-01T00:00:00Z` returns NexusAI 6, QuickQuote 4, Composer 3, HPSM-POC 3, analysis 1, MPS 2 (Vision Portal returns 0 total there, so its zero comment count has no positive control); none since the watermark. Review comments re-run on NexusAI with `since=2026-10-19T00:00:00Z` returns **2** (`github-advanced-security[bot]` on PR #97, 2026-10-19T01:42:56Z and 22:34:13Z), so that endpoint fires; none since the watermark on any repo. Merged flags read from `pulls/<n>`: MPS #89 and #90 `merged: true`; MPS #91, Composer #85, NexusAI #97 `merged: false` (the last two draft). No non-PR GitHub issue opened anywhere. All authors `kamilDatasec` (the shared account; seat PRs).

## 3. Window edges and watermarks out (Part 1)

Window: opened per the quoted watermarks; closed at the last read **01:22:01 AEDT (14:22:01Z)**. Read span 01:13:39-01:22:01 AEDT. Edges, AEDT / UTC:
- **Mailbox:** newest message read 2026-10-20T12:47:15.000Z (23:47:15 AEDT; MPS QUESTION on leave-flush vs the pin autosave test).
- **Jira:** newest processed change RD **2026-10-20 23:03:36 AEDT** (RD-875); HPSMPOC 22:07:42 (no change since); MPSCALC (excluded) **23:55:53**; VSP 2026-09-29, HPSM 2026-10-02 (unchanged).
- **GitHub:** newest item read: MPS PR #91 created and updated **2026-10-20T13:54:02Z** (00:54:02 AEDT 10-21). Next run `since=2026-10-20T13:54:00Z`. HPSM not measured, no edge advanced for it.

---

# PART 2: ticket sweep (agent-actionable tickets per project, re-run against the boards at 01:14-01:22 AEDT)

## 4. BLUF table

Class A = no client-human input, no Kam ruling, not production, not money, not external comms, not irreversible (predicates and orders as the 06:00 file's "Part 2 predicates and orders"). Counts are from paginated reads; predicates in section 6.

| Project | Tracker | Open total | By status | Class A (agent-actionable) | Owned by a live seat |
|---|---|---|---|---|---|
| NexusAI | Jira RD, **871** issues | **379** in To Do + In Progress (369 + 10); 366 more are Testing/Release Ready (167 + 199) | To Do 369, In Progress 10, Testing 167, Release Ready 199, Put on Hold 7, Done 117, Declined 2 (sums to 871) | Same named lanes N1-N7 as 06:00 minus what landed (RD-863 now **Testing**; PR #98's RD-782..789 landed at least in part, see section 5); new this run: **RD-874, RD-875** (small, below); the rest of the Medium/Low backlog not individually read | PR #97 = RD-774, RD-836 (draft, gate next). Seat on RD-873: UNMEASURED. |
| HPSM-POC | Jira HPSMPOC, **304** issues | **112** (`statusCategory != Done`) | Backlog 109, In Progress 3 (-87, -90, -91), Done 192 | **16** (-148, -155, -171, -174, -193, -226, -228, -288, -289, -292, -294, -295, -296, -297, -301, -302); -298, -299, -300 are now **Done** (deployed `c149a303`); -303 (hosted zip deploy) and -304 (vm-hpsm-sm leftovers, Azure) are not class A | none (0 open PRs in code and analysis repos) |
| Security Composer | `BACKLOG.md` @ records main `348e5087` (no Jira; PCOMP parked) | **125** of 355 parsed rows (max row #365), under the 06:00 predicate | **29** MERGED not deployed; OPEN 64; KAM'S CALL 5; READY 4; RULED 3; DEFERRED 2; ASSIGNED 2; the rest single-state; the SRO_VIC plan rows #328-#362 (L0-L9) account for the rise from 90 | New class A rows #363, #364, #365 (opened on Tuesday's B339 ruling); carried from 06:00: #152, #178, #57, #104 and the C-lane rows (not re-verified); SRO_VIC L1-L9 rows are plan lanes that wait on L0-3 approval, Kam, or each other | **B353** = PR #85 (L1 SM 3.16 catalogue, draft); L3-1 assigned to brief B322 (status UNMEASURED); L6-a (#353) landed as PR #84 |
| MPS Calculator | Jira MPSCALC, **315** issues | **301** (all Backlog; High 6, Medium 269, Low 26; Epic 15, Task 283, Bug 3) | Backlog 301, Done 14. Merged PRs #84-#90 tickets are still Backlog (the board does not move a ticket on merge, as MPSCALC-304 states) | **243** non-epic rows carry no `needs-ruling` / `question-for-kam` / `phase-2` / `lane-later` label (label-based upper bound, 286 non-epic; not comment-read) | **B354** = PR #91 (MPSCALC-306/-307/-308/-309); the MPS question mail on the autosave pin is B354's |
| Vision Portal | Jira VSP, **89** | **16** (all Backlog; High 1, Medium 9, Low 6) | Done 73, Backlog 16; unchanged since 2026-09-29 | VSP-81, VSP-87 buildable; -76, -77, -78, -79, -80, -82, -83, -85, -86 already have unmerged branches (need a gate, not new work: branch names measured) | none |
| Vision QuickQuote | no Jira; GitHub | not re-counted | PR #8 open (puppeteer 25), unchanged | nothing new that avoids the production gate | none |
| HPSM (excluded) | Jira HPSM, **41** | 25 (Backlog; Highest 2, High 1, Medium 22) | Done 16, Backlog 25; counted only | n/a | n/a |

**Changes since the 06:00 morning sweep (all MEASURED):** RD 863 -> **871** (RD-868..875 created: 868-873 seat-filed, 874-875 by the PR #98 landing seat); NexusAI main `29c5ee8f` -> `d463f881` (PR #98 merged; RD-863 moved to Testing); HPSM-POC 300 -> **304** (-298, -299, -300 Done by the 22:05 deploy; -301..-304 created); MPSCALC 231 -> **315**; Composer rows 327 -> 365 (SRO_VIC plan, B320 follow-ups); Composer PR #84 and #83 merged, PR #85 open.

## 5. LANE CANDIDATES for Tuesday

Up to 4 per in-scope project. Selection: class A, no client-human input, not Kam's signature class. "Files" are RELAYED from ticket text unless marked MEASURED (the path was found in the repo tree through `gh api .../git/trees/main`, or the file list of the open PR through `pulls/<n>/files`). **Live seats (MEASURED, file lists from `pulls/<n>/files`):** B354 = MPS PR #91 (12 files: `QuoteApiTests.V2StaffDiffer.cs`, `web/e2e/b352-followups.spec.ts`, `web/e2e/b46-home.spec.ts`, `web/e2e/support/quoteMock.ts`, `QuoteList.columns.test.tsx`, `QuoteList.tsx`, `QuoteScreen.autosave.test.tsx`, `QuoteScreen.flush.test.tsx`, `QuoteScreen.tsx`, `quote/Toolbar.tsx`, `quoteListCsv.test.ts`, `quoteListCsv.ts`); B353 = Composer PR #85 (56 files in `content/`, `packages/content/`, `packages/engine/` [src/secrets.ts, src/index.ts and about 12 test files], `packages/renderers/`, `apps/api/` tests).

### NexusAI (Reporting_Dashboard_Au; neither live seat is in this repo)
| Key | Summary | Status | Files it most likely touches | Collision |
|---|---|---|---|---|
| **RD-874** | Three tests plant a torn settings.json at a hand-built path and stay green if the product's settings file is renamed (G32-1) | To Do, Low | `__tests__/auth-gate-fail-closed.test.js` (:1140/:1158), `__tests__/rd395-ai-enabled-unreadable-store.test.js` (:89/:93), `__tests__/scim-security-controls.test.js` (:788/:790); all three paths MEASURED present at main. Fix shape: one equality guard line before each plant. | B354/B353: none (other repos). PR #97 (8 files: `security-fixes.test.js`, `rd774-*`, `server.js`, `simpleDb.js`, `validators.js`, `riskSqlTemplates.js`, `verify-expected-counts.json`): none shared. Same class as RD-873/-786 test-code work; RD-874 "relates" both. |
| **RD-875** | `tests/uat-run.js` aims at the demo host by default and hard-codes port 443, so a port in `UAT_BASE` is ignored (gate 30 N30-2 / gate 32 N32) | To Do, Low | `tests/uat-run.js` (:11 default host, :18 `port: 443`; MEASURED present) plus a small unit test of the request-options builder. | B354/B353 none. If a new test file is added, `scripts/verify-expected-counts.json` is also edited, and PR #97 and #67 both edit it (text-conflict risk, not a logic one). **RD-873 lists the same N30-2 observation as one bullet and RD-789 also edited `uat-run.js`**: order RD-875 with RD-873, not in parallel. |
| **RD-814** | CodeQL baseline: `actions/missing-workflow-permissions` x3 | To Do, Medium | `.github/workflows/build.yml`, `deploy.yml`, `npm-audit.yml` (RELAYED, not read) | none with PR #97/#67 or the live seats. Disjoint from RD-874/-875. |
| **RD-780** | CodeQL baseline: `js/regex/missing-regexp-anchor` x2 in a developer script | To Do, High | `scripts/propose-dark-retheme.js` (:184/:214, RELAYED) | none; disjoint. (RD-779, RD-781 are the same family and files `scripts/refactor-inline-styles.js`, `scripts/csp-convert.py`.) |

**RD-874 and RD-875 (asked for specifically), MEASURED:** both filed 2026-10-20 23:03 (AEDT) by the PR #98 landing seat (B343) from gate 32's report; both **To Do, Low**, no assignee change, no comment, linked "Relates" RD-786 and RD-873 (RD-875 also RD-789). **Both are small, self-contained builder tasks**, ticket text RELAYED: RD-874 is three one-line guards in three existing test files plus a measured check that the rename mutant (S8a) turns each cell red; RD-875 removes a default host and passes `url.port` through in one script, with a small unit test or a dry run against a local https server on a non-default port. Neither touches product code. Caveat: both have the same family and a shared file with RD-873 (High, five+one open CodeQL alerts in test code, To Do, builder not measured); a seat taking RD-873 should take RD-874 and RD-875 in the same pass or sequence behind it.

**NexusAI open PRs (MEASURED):** **#97** (draft, `rd-774-risk-sql-templates-s101o`, head `115a775`, updated 2026-10-20T13:37:37Z, 8 commits, +1082 -588, mergeable clean, 8 of 8 check-runs success including CodeQL and 3 Analyze jobs) is the next gate. **#67** (open, non-draft, `rd-777-776-validators-s92r`, head `94b288c`, updated 2026-10-07, 3 files: `validators.js`, a test, `verify-expected-counts.json`) is **mergeable: false, state dirty** (conflicts with main); #97 and #67 both edit `backend/validators.js` and `scripts/verify-expected-counts.json`, so whichever lands second needs a forward-merge.

### HPSM-POC (HPSM-POC repo; 0 open PRs; neither live seat is here)
| Key | Summary | Status | Files | Collision |
|---|---|---|---|---|
| **HPSMPOC-301** | [B304-1, B304-4] Import FailAsync guard: a status-read failure after the sweep failed the run writes a second `import.failed` audit and overwrites the reason | Backlog, Medium (`before-imports-on-hosted`, `test`) | `api/src/HpsmPoc.Modules.Assessment/Ingest/ImportEndpoints.cs` (FailOnceAsync), `ImportPendingSweep.cs`, `api/tests/HpsmPoc.Api.Tests/Imports/*` (RELAYED) | none with B354/B353. Same files as -302: one seat. |
| **HPSMPOC-302** | [B304-3] Import sweep count tests: four sweep mutants survive (s1..s4) | Backlog, Medium (`before-imports-on-hosted`, `test`) | `ImportPendingSweep.cs:188-201` (LandedSinceAsync), `ImportSweptUploadTests.cs` and sibling tests (RELAYED) | none; pair with -301. |
| **HPSMPOC-294** | [B286-1, B286-2] Feedback utf-7 tests: not-swallowed guard calls the reader directly | Backlog, Medium (`feedback`, `test`) | `api/tests/HpsmPoc.Modules.Feedback.Tests/Hpsmpoc290Tests.cs:90,96-114,125-136`; seam `api/src/HpsmPoc.Modules.Feedback/Endpoints/FeedbackEndpoints.cs:96` (RELAYED) | none; test-only, disjoint from -301/-302. |
| **HPSMPOC-295** | [B283-1..-4] Pkcs guard tests: pin parameter and build-0 edge pinned by no row; stale comments | Backlog, Medium (`test`) | `api/tests/HpsmPoc.Api.Tests/PkcsInPackageTests.cs:139-141,185-187,213,231-232,308-310,323` (RELAYED) | none; test-only, disjoint. |
Next in line if more lanes are wanted: -288/-289 (`web/src/server/formGate.ts` + tests), -292 (SQLite migrations), -296/-297 (web e2e). Not candidates: -303 (hosted deploy script, hosted demo), -304 (Azure VM cleanup: az, out of scope for an agent lane), `needs-kam` rows.

### Security Composer (records main `348e5087`; B353 live on PR #85)
| Key | Summary | Status | Files | Collision with B353 (PR #85) / B354 |
|---|---|---|---|---|
| **#363** (B320-1) | A web test flaky under load: `b116-s10-verify-dom.test.tsx:120` waits on elapsed turns, not state | OPEN (Minor), opened on Tuesday's B339 ruling | `apps/web/src/screens/b116-s10-verify-dom.test.tsx` (RELAYED) | none (apps/web is not in PR #85's 56 files). |
| **#364** (B320-3) | Comment-only: state in the `SINGLE_SPLIT_BOUND` comment that the split sees super-linear growth in one string only | OPEN (Note) | `packages/engine/test/s47-crf2-linear-detector.test.ts` `:245-254` (RELAYED) | file-disjoint from PR #85 (which edits other `packages/engine/test/*` files and `src/secrets.ts`, `src/index.ts`); same directory, so rebase noise at most. |
| **#57** | The Expert Discovery typed editor writes every sub-answer at engagement level; API now 400s device-group sub-answers (latent: both releases declare 0) | OPEN (latent) | `apps/web/src/screens/Discovery.tsx` (`typedDraftFor`) (RELAYED) | none. Shares an area with #104 (ruled build) if both are taken. |
| **#152** | Index on `pc.audit_event (tenant_id, entity_type, entity_id)` for `listApprovals` | OPEN (Low, performance) | one new `packages/db/migrations/00NN_*.sql` + rollback (RELAYED) | none with PR #85 (no db files). **Migration-number clash risk with the L3-x lane (brief B322, status UNMEASURED)**; #178 (CHECK on `last_generate_input_hash`) belongs in the same migration. |
Not candidates (collide or wait): all SRO_VIC L1-x rows (#331-#335; B353's lane, PR #85); L2/L4/L5/L6-2/L6-3 (wait on L1-L3); L3-1..L3-6 (migration + contract; B322); L7/L8/L9 (wait on L1/L9-a, HPSM-POC VM seat); #365 is a records-only row (B301 STATUS closing block), a records seat's job, not a code lane. 29 MERGED-not-deployed rows and the three open cards wait on Kam's demo deploy word.

### MPS Calculator (MPS repo; B354 live on PR #91)
| Key | Summary | Status | Files | Collision with B354 (PR #91) |
|---|---|---|---|---|
| **MPSCALC-304** | [B305-3] Missing test row: a `HeadingShaped` that accepts digits survives | Backlog, Medium (lane-e, tier-1) | `tests/MpsCalc.Import.Tests/PanelSectionEndTests.cs`; `src/MpsCalc.Import/Books/SynnexBook.cs:335` (RELAYED) | none (PR #91 has no Import files). Test-only. |
| **MPSCALC-305** | [B305-4] Missing test row: supply-row and panel-record device sources of the panel check are unpinned | Backlog, Medium (lane-e, tier-1) | `src/MpsCalc.Import/Parity/ParityProof.cs:165-172`; an importer-made store test in `tests/MpsCalc.Import.Tests` (RELAYED) | none; same seat as -304. |
| **MPSCALC-289** | [B318-2] A clone reference cut to the length limit can split a surrogate pair and store U+FFFD | Backlog, Medium (lane-v0, tier-1) | `src/MpsCalc.Api/Quotes/QuoteEndpoints.cs:566-576` (CopyRef), a new API test file under `tests/MpsCalc.Api.Tests` (RELAYED) | none on the files; PR #91 adds only `QuoteApiTests.V2StaffDiffer.cs` in that test project (a different partial file). |
| **MPSCALC-292** | [B324-2] The "uses none of the calculators" source-scan guard can be bypassed (alias, namespace-relative, using static) | Backlog, Medium (lane-v3, tier-1) | `tests/MpsCalc.Engine.Tests/ReconciliationTests.cs:457-476`; `docs/RECONCILIATION.md` (RELAYED) | none. |
Also clean of B354 but not chosen: MPSCALC-288 (`QuoteEndpoints.cs:1131-1134` + `docs/api/openapi.json`, needs a choice between two fixes), -291, -294 (`PurchaseRecomputation.cs`, docs), -293 (`ReadinessPanel.tsx`; a new CSV header goes to the words gate). **Collide with or wait on B354:** -306, -307, -308, -309 (the PR's own tickets); -314 (autosave per typing pause; the fix choice is open and unruled, and PR #91 changes the same `QuoteScreen.tsx` autosave); -311 and -310 (staff-figure tests in `tests/MpsCalc.Api.Tests`: PR #91's `V2StaffDiffer.cs` may already cover -311, UNMEASURED); -312 (contract words, lane V0 files, regenerate client); -313 (`web/src/api/stub/stubApi.ts`, owner's file); -315 (lane V4 result field, calculation register row first). MPS is outside the feedback actions but is read for activity.

### Vision (Portal repo; no live seat; production work is Kam-gated, deploys are never in a lane)
| Key | Summary | Status | Files | Collision |
|---|---|---|---|---|
| **VSP-81** | Restore: a row written between plan and clear is cascade-deleted, child rows dropped by 23503 | Backlog, Medium | `server/dbRestore.js`, `server/dbRestore.test.js`, `test/db/restore-incomplete.test.js` (paths MEASURED present at main; mapping to the ticket RELAYED from the 06:00 carry) | none with B354/B353. **Unmerged branches `vsp-83-old-backup-dates` and `vsp-86-restore-clears-sessions` (names MEASURED) likely edit `dbRestore.js`**: order after they merge, or one seat for all restore tickets. |
| **VSP-87** | Restore: six table layouts where `--allow-incomplete` prints "leaving <t> as it is" and then changes it | Backlog, Medium | `server/dbRestore.js`, `test/db/restore-incomplete.test.js` | same as VSP-81; one seat for both. |
| **VSP-84** | Backup peaks at about 20x the database size in memory, inside the web process | Backlog, Medium | `server/dbBackup.js` (+ `dbBackup.test.js`; MEASURED present) | none; touches the backup code only. (Unmerged branch `vsp-85-backup-test-gaps` is the nearest.) |
| **VSP-72** | Two first boots on an empty database race: one fails 23505 on the first app tables | Backlog, Low | file not established (UNMEASURED; boot/schema code in `server/`) | none seen. |
QuickQuote: no ticket store; PR #8 (puppeteer 25) is Kam-ruled and unchanged; no candidate that avoids the production gate. HPSM: not classified (counts only; GitHub not measured).

## 6. Part 2 method, predicates and controls

- **NexusAI:** `project = RD ORDER BY key ASC` -> **871** read 871; by status: To Do 369, In Progress 10, Testing 167, Release Ready 199, Put on Hold 7, Done 117, Declined 2 (sums to 871). `project = RD AND statusCategory != Done` -> **754**. `project = RD AND statusCategory != Done AND status in ("To Do","In Progress") ORDER BY priority DESC, key ASC` -> **379** read 379: To Do Highest 2, High 44, Medium 176, Low 145, Lowest 2; In Progress High 4, Medium 4, Low 2. All 46 Highest/High rows in To Do/In Progress plus the 10 In Progress rows listed and read for key, summary, labels. Descriptions read in full for RD-874 and RD-875; last comments read for RD-786, -789, -873. Medium/Low rows not named were not individually read (the 06:00 Tier B/C reading stands unless noted). Control: the same script reproduces the 06:00 counts where nothing moved (Done 117, Release Ready 199, Put on Hold 7, Declined 2) and shows the expected deltas (To Do +5, Testing +3, total +8).
- **HPSM-POC:** `project = HPSMPOC ORDER BY key ASC` -> **304** read 304 (Backlog 109, In Progress 3, Done 192); `statusCategory != Done` -> **112**. Class A predicate as the 06:00 file: no Kam decision, no outside human, not production, work is code / tests / CI / docs. Descriptions read for -294, -295, -301, -302, -303; the other 107 open rows were re-listed by key, summary and labels only (the 94-row B/C/D split of 10-19 is carried, not redone).
- **Composer:** `git --no-optional-locks show main:BACKLOG.md` at `348e5087146e9fa37a43c8b1aee17da1dbf6f81d` (records main, 2026-10-20 21:08 AEDT, "Merge records/b339"), 362 lines, **355 parsed rows**, highest row #365. Open predicate as the 06:00 file (state text with markers stripped not beginning CLOSED, DONE, ACCEPTED, CORRECTED, NOTED, Covered, INFO, RECORDS AMENDED, DOCUMENTED, DEPLOYED or FIXED unless "FIXED ON A BRANCH", and not MERGED with a deploy line in the first 200 characters) -> **125 open**, **29** MERGED not deployed. Control: the same parse finds #84 OPEN, #363-#365 OPEN, and closes the rows closed at 06:00. Caveat: about 10 rows have a pipe character inside the item or state cell, so their state text starts mid-sentence and they are counted open (conservative); the 06:00 count of 90 on 317 rows is not strictly comparable.
- **MPS Calculator:** `project = MPSCALC ... statusCategory != Done` -> **301** (Backlog 301, Epic 15, Task 283, Bug 3; High 6, Medium 269, Low 26). Non-epic 286; non-epic with none of `needs-ruling`, `question-for-kam`, `phase-2`, `lane-later` -> 243 (label-based). Descriptions read for MPSCALC-288..295, -300..-305, -310..-315.
- **VSP and HPSM:** open lists paged (VSP 16, HPSM 25); VSP titles and labels re-read, nothing updated since 2026-09-29. Branch list of the Portal repo read (32 branches).
- **PR facts (NexusAI #97/#67, Composer #85, MPS #91/#90/#89):** `pulls/<n>`, `pulls/<n>/files`, `commits/<sha>/check-runs` via `gh api` under each project's own `GH_CONFIG_DIR`; file lists paged to their end and compared with `changed_files`.
- **Decision store:** `TUESDAY/0_Brain/dashboard/data/decisions.json` read only (859 cards: ruled 821, withdrawn 34, open 4): open Datasec cards `composer-l05-setup-card-too-1014`, `composer-demo-deploy-eaff2b7-words-1020`, `composer-contents-word-pr84-1020`, `hpsmpoc-sm-vm-budget-24x7-1020`.
- **Live-seat exclusions:** B354 (MPS PR #91), B353 (Composer PR #85), plus PR #97 (RD-774, RD-836) for NexusAI.

## 7. UNMEASURED
- **Every live feedback store:** MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, the NexusAI share `feedbackItems`, Portal Postgres, the QuickQuote table. Each needs az, a writing sign-in or HTTP to a hosted host, all out of bounds. **"0 new" means only that nothing reached the mailbox, Jira or GitHub.**
- **Who wrote a Jira comment:** the shared account cannot tell Kam from a seat; only openings (about 110 characters) were read.
- **HPSM GitHub:** `gh` not logged in under HPSM's config.
- **Mail bodies** not read; `coagent@` bus and other inboxes not read (the `coagent@` rows are copies that reached `tuesday-agent@`). The MPS QUESTION on leave-flush vs the pin autosave test (12:47:15Z) is a seat-to-Tuesday question, listed by subject only; it is B354's.
- **Vision Portal comment endpoint** has no positive control (0 comments total since 09-01).
- **Kam's card board** read only for open Datasec cards (4), not for rulings made overnight: any ruling after the last sweep is not reflected in the lanes.
- **Whether a seat is on RD-873, B322 (Composer L3-1), or the unmerged Vision branches:** not measured (no Jira assignee or branch-owner record was read). Whether B352/B354 covers MPSCALC-311 is unmeasured.
- **File lists:** for every candidate other than RD-874/-875 (paths measured in the tree) and the PR file lists, the files come from ticket text, not from the code; `ImportEndpoints.cs`, `QuoteEndpoints.cs`, `SynnexBook.cs`, `Discovery.tsx` and the others were not opened. VSP-72's file was not established. Whether adding a test in RD-875 changes `scripts/verify-expected-counts.json` is inferred from #97/#67's habit, not run.
- **Ticket depth:** NexusAI Testing (167) and Release Ready (199), Medium/Low rows not named; HPSM-POC's non-class-A rows; Composer rows not named (class A by state text only, not re-verified against code); MPS 243 label-based; whether MERGED Composer rows are live on the demo (no HTTP) is unknown.
- No HTTP to any app host, hosted site or production (only the AgentMail API, Jira Cloud search and comment reads, and `api.github.com`); no az, docker or ssh; the only git command in a project repo was `git --no-optional-locks -C <Composer> rev-parse / log / branch / show main:BACKLOG.md`; no Jira, gh, mail or card writes. Temporary scripts lived in the session scratchpad.

## OUTBOUND watermarks for the next sweep

- Mailbox: at or after **2026-10-20T12:47:15.000Z**.
- Jira: RD `>= "2026-10-20 23:00"` (newest change 23:03:36); HPSMPOC `>= "2026-10-20 22:05"` (unchanged); MPSCALC (excluded) `>= "2026-10-20 23:50"` (newest change 23:55:53); VSP and HPSM `>= "2026-10-19 19:35"` (all AEDT).
- GitHub: `since=2026-10-20T13:54:00Z`.
