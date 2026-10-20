# Rotation sweep 07:50: Datasec feedback + client-human delta, 2026-10-21

Read-only sub-agent (claude-sonnet-5-5) for Tuesday. Clock from `date`: **Wed 21 Oct 2026 07:43:51 AEDT** at start, **07:45:57 AEDT** at the last read. Method, instruments and scope copied from [[2026-10-21_rotation-sweep-0535]] (Part 1 only; Part 2 not repeated, plus the new-ticket and open-count asks). Scope follows the 0535 file exactly: NexusAI, Vision Portal, QuickQuote, Composer, MPS, HPSM-POC and HPSM were all read; MPS/HPSM-POC/HPSM are "excluded" from feedback actions but read for activity. **The 10-16 rule and the 0535 file do not disagree**: the rule says sweep each Datasec project; 0535 narrowed the actionable set but still read everything. HPSM-POC in-app feedback lands in Jira (HPSMPOC) and the Postgres `poc.feedback_item` store; only Jira was readable.

Windows opened at 0535's OUTBOUND watermarks: mailbox >= 2026-10-20T16:51:18.000Z; Jira RD >= 2026-10-21 05:00, HPSMPOC >= 04:30, MPSCALC >= 05:00, VSP/HPSM >= 2026-10-19 19:35 (AEDT); GitHub since=2026-10-20T18:06:00Z. All facts MEASURED (instruments: AgentMail API; Jira Cloud `search/jql` + `/comment`, each project's own `4_Credentials/.env`, never printed; `gh api` GETs under each project's `GH_CONFIG_DIR`). No production or hosted host contacted.

## BLUF

**New feedback items: 0 in every project. New client-human responses: 0. New tickets: 0 on HPSMPOC, RD, MPSCALC. Nothing for Kam from a client.** Window is fleet work only (PR merges/openings below).

**HPSMPOC open (statusCategory != Done): 111.** Paged search `project = HPSMPOC AND statusCategory != Done`: **2 pages, isLast = True, 111 issues** (Backlog 108, In Progress 3). **Control: `POST /rest/api/3/search/approximate-count` returns 111.** Match. (0535 said 113; -2 is the two Done transitions HPSMPOC-301/-302 after the deploy, plus the board otherwise unchanged: total still 305.)

## Per project

| Project | New feedback items | Client-human responses | New tickets since watermark | Other activity |
|---|---|---|---|---|
| NexusAI (RD) | 0 | 0 | **0** (total 874, max key RD-878, unchanged from 0535) | Jira: 9 touched (RD-873/-874/-875/-876/-877/-878/-798/-836/-774), all touched at 05:01-05:02 = 0535's own tail; no later change. 4 comments, all seat "BLUF:" voice (RD-873, -875, -874, -798 at 05:02). GitHub: **new PR #103** (open, `RD-780` regex alternation grouping, created 19:43:43Z); PR #101 head moved `6e947f4` -> `48a17df` (updated 18:34:20Z); #102 and #67 open unchanged; main still `115a775b`. 0 issue and 0 review comments. |
| Vision Portal (VSP) | 0 | 0 | 0 (total 89) | none. Jira 0 touched, main `6dbffdf3` (09-28), PRs #14-#17 unchanged. |
| QuickQuote | 0 (no `QuickQuote feedback (` mail in window) | 0 | n/a (no Jira) | none. main `5fa1187b`, PR #8 open, unchanged. |
| Security Composer | 0 | 0 | 0 on the board (no commit on main since 10-20T10:11Z, `308b7aa6`; BACKLOG.md not re-read, so a row added only on a branch is UNMEASURED) | PR #85 (draft) head `e969ad3`, unchanged from 0535. 0 comments. |
| MPSCALC (excl.) | 0 | 0 | **0** (total 315, max key MPSCALC-315) | Jira 2 touched (MPSCALC-304/-305, 05:03 QA gate B365 comments, seat voice). GitHub: **new PR #93** (open, MPSCALC-289 surrogate-pair copy-ref fix, created 19:44:39Z); main `1eccbc8b` unchanged. |
| HPSM-POC (excl.) | 0 (HPSMPOC-294 "Feedback utf-7 tests" and -303 match "feedback" by title; both are seat test/deploy tickets) | 0 | **0** (total 305, max HPSMPOC-305) | Jira 6 touched: -305 (comment 06:31, branch `b372/...` pushed), -294 (comments 04:30, 05:49 correction), -303/-302/-301 (05:39 hosted deploy comments, -301/-302 now Done), -295. Seat voice only. GitHub: **PR #166 merged** (HPSMPOC-294+295, 20:01:00Z, main commit `fa8416de`), **PR #167 new and merged** (HPSMPOC-305, 20:24:50Z); main now `54fbceac` (was `6818896b`). Analysis repo: PR #127 merged, main `6a368d9e` (was `e2a0d721`). |
| HPSM (excl.) | 0 | 0 | 0 (total 41) | none. Jira 0 touched. GitHub not read this run (`gh` not logged in under HPSM's config per 0535; not re-tried). |

Mail (tuesday-agent@): 3,749 messages, 38 pages, newest 2026-10-20T16:51:18Z = the watermark message only (QA gate 29 helpers released). So **0 new messages** since. `coagent@` (4,676, 47 pages): only 2 new rows, both `[Wednesday -> all agents] Morning shift change 2026-10-21` (18:30:03Z, 18:30:06Z; fleet broadcast, no client, no feedback).

Client-human responses in Jira: every in-window comment (RD 4, HPSMPOC 7, MPSCALC 2) is authored by the shared "Kamil Kreiser" account and opens "BLUF:" (seat/QA voice). That account cannot separate Kam from a seat, so a 0 here means "no comment that reads as a human client". No other author appears.

## Controls (every zero has a query that must return non-zero)

- Mail: the watermark message (16:51:18.000Z) returns in the same call. Instrument fires: **50** subjects containing "feedback" on tuesday-agent@ (newest 2026-10-17T04:56:13Z), **1** starting `QuickQuote feedback (`; coagent@ 36 and 8.
- Jira feedback search: RD summary "feedback" 21 total (0 in window), RD label 5 total; HPSMPOC summary 25 total / label 20 total (window 2 / 1, both seat tickets); MPSCALC summary 13 total; VSP summary 1 total; HPSM 0 total (never had a hit, no project control; same as 0535). Totals identical to 0535.
- New-ticket zeros: `project = X ORDER BY key` totals RD 874, HPSMPOC 305, MPSCALC 315, VSP 89, HPSM 41, all equal to 0535; the window queries return non-zero on RD (9), HPSMPOC (6), MPSCALC (2).
- GitHub zeros: since-filter fires on NexusAI (3), HPSM-POC (2), analysis (1), MPS (1). On zero repos (Vision Portal, QuickQuote, Composer) main HEAD is visible under the same credentials. Comment endpoints with `since=2026-09-01` return NexusAI 6, QuickQuote 4, Composer 3, HPSM-POC 3, analysis 1, MPS 2 (Vision Portal 0, no positive control there).

## UNMEASURED

- All live feedback stores (MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, NexusAI share `feedbackItems`, Portal Postgres, QuickQuote table): need az/HTTP to hosted hosts, out of bounds. "0 new" means only nothing reached the mailbox, Jira or GitHub.
- Mail bodies (subjects only); Composer BACKLOG.md and branch contents; HPSM GitHub; who exactly authored a "Kamil Kreiser" Jira comment.
- Commits-since is by commit date (the 0535 caveat stands; merges cross-checked via `pulls`/`issues` listing only).

## OUTBOUND watermarks for the next sweep

- Mailbox: at or after **2026-10-20T16:51:18.000Z** (tuesday-agent@, unchanged: nothing newer exists); coagent@ newest 2026-10-20T18:30:06.000Z.
- Jira (AEDT): RD `>= "2026-10-21 05:02"` (newest change 05:02:56); HPSMPOC `>= "2026-10-21 06:31"` (newest change 06:31:41, HPSMPOC-305 comment); MPSCALC `>= "2026-10-21 05:03"` (newest 05:03:21); VSP and HPSM `>= "2026-10-19 19:35"` (unchanged).
- GitHub: `since=2026-10-20T20:24:52Z` (newest item read: HPSM-POC PR #167 updated 20:24:52Z). NexusAI newest read 19:43:43Z, MPS 19:44:39Z, analysis 18:47:55Z; all earlier than the global edge, so no item can be missed by using the single edge except a late-pushed older-dated commit (the commit-date caveat).
