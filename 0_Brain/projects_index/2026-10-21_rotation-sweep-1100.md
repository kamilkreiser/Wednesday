# Rotation sweep 11:00: Datasec feedback + client-human delta, 2026-10-21

Read-only sub-agent (claude-sonnet-5-5) for Tuesday. Clock from `date`: **Wed 21 Oct 2026 11:01:00 AEDT** at start, **11:03:14 AEDT** at the last read (00:03:14Z). Method, instruments and scope copied from [[2026-10-21_rotation-sweep-0750]] (which copied [[2026-10-21_rotation-sweep-0535]]): same table, same sources, same scope (NexusAI, Vision Portal, QuickQuote, Composer, MPS, HPSM-POC, HPSM all read; MPS/HPSM-POC/HPSM read for activity, excluded from feedback actions).

Windows opened at the 0750 OUTBOUND watermarks: mailbox >= 2026-10-20T16:51:18.000Z (tuesday-agent@), coagent@ >= 18:30:06Z; Jira RD >= 2026-10-21 05:02, HPSMPOC >= 06:31, MPSCALC >= 05:03, VSP/HPSM >= 2026-10-19 19:35 (AEDT); GitHub since=2026-10-20T20:24:52Z. All facts MEASURED (AgentMail API list; Jira Cloud `search/jql`, `/comment`, `approximate-count`, each project's own `4_Credentials/.env` parsed in-process, never printed; `gh api` GETs under each project's `GH_CONFIG_DIR`). No app host, production or hosted site contacted.

## BLUF

**New feedback items: 0 in every project. New client-human responses: 0. Nothing for Kam from a client.** The window is fleet work only.

**New tickets (all seat-filed from dependency-audit / test-gap findings, none from a client):**
- **RD (NexusAI): 1 new, RD-879** (created 07:57:28 AEDT, npm-audit red on main, follow-redirects 1.16.0; landed via PR #104 merged). RD total **874 -> 875**, max key 878 -> 879. Control: window query returns 9 (non-zero).
- **HPSMPOC: 2 new, HPSMPOC-306** (07:55:14, "Feedback tests: pin the planted carrier's boundary", a seat test ticket) **and HPSMPOC-307** (09:25:04, CI audit red on main, vite 8.3.0; fixed by PR #172 merged). Total **305 -> 307**, max key 307. Control: window query returns 13.
- **MPSCALC: 0** (total 315, max 315 unchanged; window query returns 2). **VSP: 0** (89). **HPSM: 0** (41). QuickQuote and Composer have no Jira board; Composer has no new commit on main (BACKLOG.md not re-read, so a row added only on a branch is UNMEASURED).
- **Control count:** board totals now RD 875, HPSMPOC 307, MPSCALC 315, VSP 89, HPSM 41; 0750 had 874 / 305 / 315 / 89 / 41. The two non-zero deltas equal the new keys listed, so the count instrument fires.

**HPSMPOC open (statusCategory != Done): 113.** Paged search `project = HPSMPOC AND statusCategory != Done`: 113 issues across 2 pages (Backlog 110, In Progress 3). **Control: `POST /rest/api/3/search/approximate-count` returns 113.** Match. (0750 said 111; +2 is exactly HPSMPOC-306 and -307, both Backlog.)

## Per project

| Project | New feedback items | Client-human responses | New tickets since watermark | Other activity |
|---|---|---|---|---|
| NexusAI (RD) | 0 | 0 | **1: RD-879** (total 875, max RD-879) | Jira 9 touched: RD-879 (comment 10:38:31, landed on main by fast-forward), and RD-873/-874/-875/-798/-836/-774/-877/-878 all at 05:02 = the same tail as 0750, no later change. 5 comments, all "BLUF:" seat voice. GitHub: **PR #104 merged** (RD-879, 23:00:27Z, head `c139e4a`); main `115a775b` -> **`c139e4a8`** (commit 21:37:53Z, 1 commit by date); PR #103 (RD-780) open, head `138b78e`, unchanged since 19:43:43Z; open #103, #102 (`6dcbedb`), #101 (`48a17df`), #67. 0 issue and 0 review comments. |
| Vision Portal (VSP) | 0 | 0 | 0 (total 89) | none. Jira 0 touched; main `6dbffdf3` (09-28); open PRs #14-#17 unchanged. |
| QuickQuote | 0 (no `QuickQuote feedback (` mail in window) | 0 | n/a (no Jira) | none. main `5fa1187b` (10-18), PR #8 open `4d6ed6e`, unchanged. |
| Security Composer | 0 | 0 | 0 on the board (see BLUF caveat) | **New PR #86** (open, not draft, **Dependabot** vite 8.3.0 -> 8.3.4, created 22:10:51Z; automated, not a human). PR #85 (draft) head `e969ad3` unchanged. main `308b7aa6` unchanged. 0 comments. |
| MPSCALC (excl.) | 0 | 0 | **0** (total 315) | Jira 2 touched (MPSCALC-304/-305, 05:03 QA gate B365, same as 0750). GitHub: **PR #93 merged** (23:20:48Z); main `1eccbc8b` -> **`f5b6f5a7`** (23:20:47Z); 0 open PRs. |
| HPSM-POC (excl.) | 0 (summary "feedback" now 26 total, window 4; label 20 total, window 4: HPSMPOC-294, -305(label), -226, -306 by title/label; every one is a seat test or follow-up ticket, none a submission) | 0 | **2: HPSMPOC-306, -307** (total 307) | Jira 13 touched; every in-window comment (13) opens "BLUF:" (branch-pushed or QA-gate seat voice) except 09:22:28 on HPSMPOC-292, a coordinator record. GitHub code repo: **PRs #168, #169, #172, #175 merged** (22:50:16Z, 23:44:58Z, 23:26:18Z, 23:54:43Z); main `54fbceac` -> **`f06d2a69`** (23:54:42Z, 4 commits by date); open **#170, #171, #173**; **#174 closed unmerged (Dependabot vite bump; its one issue comment, "no longer needed", is from the bot)**. Analysis repo: **PR #128 merged** (21:09:04Z), main `6a368d9e` -> `2bb78382`, 3 commits by date; 0 open. |
| HPSM (excl.) | 0 | 0 | 0 (total 41) | none. Jira 0 touched. GitHub UNMEASURED (`gh` not logged in under HPSM's config; retried once, same "gh auth login" prompt). |

Mail (tuesday-agent@): 3,749 messages, 38 pages, newest 2026-10-20T16:51:18Z = the watermark message only (QA gate 29 helpers released). **0 new messages** since 0750 (and none since 0535: the mailbox has been silent since 03:51 AEDT). `coagent@` (4,676, 47 pages): newest 18:30:06Z = the 0750 watermark row (`[Wednesday -> all agents]` fleet broadcast, 1 row from the watermark on, no new row). Subjects of untagged coagent@ rows were not needed; none read.

Client-human responses in Jira: every in-window comment (RD 5, HPSMPOC 13, MPSCALC 2) is posted from the one shared account and opens "BLUF:" or is a coordinator record (seat/QA voice). That account cannot separate Kam from a seat, so a 0 means "no comment that reads as a human client". The only non-seat GitHub author in window is Dependabot (bot).

## Controls (every zero has a query that must return non-zero)

- Mail: the watermark message (16:51:18.000Z) returns in the same call on tuesday-agent@, and 18:30:06Z on coagent@. Instrument fires: **50** subjects containing "feedback" on tuesday-agent@ (newest 2026-10-17T04:56:13Z), **1** starting `QuickQuote feedback (`; coagent@ 36 and 8. Totals identical to 0750.
- Jira feedback search: RD summary 21 total (0 in window), RD label 5 total; HPSMPOC summary **26** total (25 at 0750; the +1 is HPSMPOC-306 by title) / label 20; MPSCALC summary 13; VSP summary 1; HPSM 0 / 0 (never had a hit, no project control). RD/MPSCALC/VSP identical to 0750.
- New-ticket zeros: `project = X ORDER BY key` totals above; window queries return non-zero on RD (9), HPSMPOC (13), MPSCALC (2).
- HPSMPOC open: paged 113 = approximate-count 113.
- GitHub zeros: since-filter fires on NexusAI (1), HPSM-POC (9 items), analysis (1), MPS (1), Composer (1). On the zero repos (Vision Portal, QuickQuote) main HEAD is visible under the same credentials. Comment endpoints with `since=2026-09-01` return NexusAI 6, QuickQuote 4, Composer 3, HPSM-POC 4, analysis 1, MPS 2 (Vision Portal 0, no positive control). Issue comments since the watermark: HPSM-POC 1 (the bot), all others 0; review comments 0 everywhere (review-comment endpoint not re-controlled this run; it fired on NexusAI at 0535).

## FOUND

No feedback item and no client-human response anywhere. Seat-filed tickets RD-879, HPSMPOC-306, HPSMPOC-307. Fleet merges listed in the table. Nothing for each project's own agent to ticket from this sweep, so nothing for Tuesday to brief.

## TESTED

Mailbox (both inboxes, full paging, subjects/senders/timestamps only; coagent@ rows filtered on Datasec tags before anything else, none beyond the watermark row existed); Jira per project (touched list, new keys, totals, feedback summary/label counts, comments on every touched issue, HPSMPOC open count paged plus approximate-count); GitHub per repo (main HEAD, commits since, issues/PRs updated since, issue and review comments since, open PRs, merged flags on every PR in window).

## HOW

`python3 -I` scripts in the session scratchpad parsing each project's own `.env` in-process (nothing printed or written), Basic-auth GETs to the Jira site, AgentMail list calls, `gh api` GETs under each project's own `GH_CONFIG_DIR`. Local git, az, docker, ssh and every app host untouched.

## NOT TESTED

- Live feedback stores (MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, NexusAI share `feedbackItems`, Portal Postgres, QuickQuote table): need az or HTTP to app hosts, out of bounds. "0 new" means only that nothing reached the mailbox, Jira or GitHub.
- Mail bodies (subjects only); Composer BACKLOG.md and branch contents; HPSM GitHub; who exactly authored a shared-account Jira comment.
- Commits-since is by commit date (the 0535 caveat stands; merges cross-checked through the `pulls` endpoint, as above).

## OUTBOUND watermarks for the next sweep

- Mailbox: tuesday-agent@ at or after **2026-10-20T16:51:18.000Z** (unchanged, nothing newer exists); coagent@ newest 2026-10-20T18:30:06.000Z (unchanged).
- Jira (AEDT): RD `>= "2026-10-21 10:38"` (newest change 10:38:31, RD-879 comment); HPSMPOC `>= "2026-10-21 09:25"` (newest change 09:25:04, HPSMPOC-307 created); MPSCALC `>= "2026-10-21 05:03"` (newest 05:03:21, unchanged); VSP and HPSM `>= "2026-10-19 19:35"` (unchanged). Board totals out: RD 875 (max 879), HPSMPOC 307, MPSCALC 315, VSP 89, HPSM 41; HPSMPOC open 113.
- GitHub: `since=2026-10-20T23:59:40Z` (newest item read: HPSM-POC PR #170 updated 23:59:39Z). Per-repo newest read: NexusAI #104 23:00:27Z, Composer #86 22:10:54Z, MPS #93 23:20:48Z, analysis #128 21:09:04Z, HPSM-POC #170 23:59:39Z. Open PRs to re-check: HPSM-POC #170 `b1ae054`, #171 `cc3eae4`, #173 `549e6b9`; NexusAI #101 `48a17df`, #102 `6dcbedb`, #103 `138b78e`, #67 `94b288c`; Composer #85 `e969ad3`, #86 `fd24426`; QuickQuote #8 `4d6ed6e`; Vision #14-#17.
