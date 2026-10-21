# Rotation sweep 14:20: Datasec feedback + client-human delta, 2026-10-21

Read-only sub-agent (claude-sonnet-5-5) for Tuesday. Clock from `date`: **Wed 21 Oct 2026 14:24:06 AEDT** at start, **14:34:13 AEDT** at the last read (03:34:13Z). Method, instruments and scope copied from [[2026-10-21_rotation-sweep-1100]] (which copied 0750 and 0535): same table, same sources, same scope (NexusAI, Vision Portal, QuickQuote, Composer, MPS, HPSM-POC, HPSM all read; MPS/HPSM-POC/HPSM read for activity, excluded from feedback actions).

Windows opened at the 1100 OUTBOUND watermarks: mailbox tuesday-agent@ >= 2026-10-20T16:51:18Z, coagent@ >= 18:30:06Z; Jira RD >= 2026-10-21 10:38, HPSMPOC >= 09:25, MPSCALC >= 05:03, VSP/HPSM >= 2026-10-19 19:35 (AEDT); GitHub since=2026-10-20T23:59:40Z. All facts MEASURED (AgentMail API list; Jira Cloud `search/jql`, `/comment`, `approximate-count`, each project's own `4_Credentials/.env` parsed in-process, never printed; `gh api` GETs under each project's `GH_CONFIG_DIR`). No app host, production or hosted site contacted.

## BLUF

**New feedback items: 0 in every project. New client-human responses: 0. Nothing for Kam from a client.** The window is fleet work only.

**New tickets (seat-filed, none from a client):**
- **RD (NexusAI): 0 new.** Total 875, max key RD-879 (both unchanged from 1100). The one touched issue is RD-879 itself, whose comment (10:38:31) is the 1100 watermark row. Control: wider query (updated >= 2026-10-21 00:00) returns 10.
- **HPSMPOC: 1 new, HPSMPOC-308** (created 13:58:52, "CI: the non-required SQL Server shard api on SQL Server (api-other-and-feedback) goes red", a seat CI ticket; the word "feedback" is a test-shard name, not a submission). Total **307 -> 308**, max key 308. Control: wider query returns 18.
- **MPSCALC: 0** (315, unchanged). **VSP: 0** (89). **HPSM: 0** (41). QuickQuote and Composer have no Jira board; Composer BACKLOG.md not re-read, so a row added only on a branch is UNMEASURED.
- **Control count:** board totals now RD 875, HPSMPOC 308, MPSCALC 315, VSP 89, HPSM 41; 1100 had 875 / 307 / 315 / 89 / 41. The one non-zero delta equals the one new key, so the count instrument fires.

**HPSMPOC open (statusCategory != Done): 111.** Paged search: 111 issues. **Control: `search/approximate-count` returns 111.** Match. (1100 said 113; +1 new -308, minus 3 moved to Done in window: HPSMPOC-232, -288, -289.)

## Per project

| Project | New feedback items | Client-human responses | New tickets since watermark | Other activity |
|---|---|---|---|---|
| NexusAI (RD) | 0 | 0 | **0** (total 875, max RD-879) | Jira 1 touched: RD-879 (the watermark comment, 10:38:31, "BLUF:" seat voice). GitHub: main `c139e4a8` unchanged (21:37:53Z); 0 commits, 0 issue/PR updated since; open #103 `138b78e`, #102 `6dcbedb`, #101 `48a17df`, #67 `94b288c`, all unchanged. 0 issue and 0 review comments. |
| Vision Portal (VSP) | 0 | 0 | 0 (total 89) | none. Jira 0 touched; main `6dbffdf3` (09-28); open PRs #14-#17 unchanged (heads `61c43d7`, `72e3b17`, `65d2635`, `44e1b0a`). |
| QuickQuote | 0 (no `QuickQuote feedback (` mail in window) | 0 | n/a (no Jira) | none. main `5fa1187b` (10-18), PR #8 open `4d6ed6e`, unchanged. |
| Security Composer | 0 | 0 | 0 on the board (see BLUF caveat) | none. main `308b7aa6` unchanged; open #86 `fd24426` (Dependabot) and #85 `e969ad3` (draft) unchanged; 0 comments. |
| MPSCALC (excl.) | 0 | 0 | **0** (total 315) | Jira 2 touched (MPSCALC-304/-305, 05:03, QA gate B365, same as 1100). GitHub: main `f5b6f5a7` unchanged (23:20:47Z); 0 open PRs; nothing since. |
| HPSM-POC (excl.) | 0 (summary "feedback" now 27 total, 1 in window = HPSMPOC-308 by its shard name; label 15 total, 0 in window; none a submission) | 0 | **1: HPSMPOC-308** (total 308) | Jira 10 touched; all 9 in-window comments open "BLUF:" (deployed-to-hosted-demo or merged/gated seat voice: HPSMPOC-235, -232, -288, -289, -307, -99, -226, -234, -148). GitHub code repo: **PRs #173 and #170 merged** (both 2026-10-21T01:17:17Z / 01:18:05Z); main `f06d2a69` -> **`ec0a62a1`** (01:18:04Z; 2 commits by date, `d563a5a1`, `ec0a62a1`); open **#171** `cc3eae4` only. Analysis repo: **PR #129 merged** (03:14:28Z, records B403), main `2bb78382` -> **`1212e9e5`** (03:14:27Z, 4 commits by date); 0 open. All PR authors the shared seat account. |
| HPSM (excl.) | 0 | 0 | 0 (total 41) | none. Jira 0 touched. GitHub UNMEASURED (`gh` not logged in under HPSM's config: "gh auth login" prompt, same as 1100). |

Mail (tuesday-agent@): 3,750 messages, 38 pages, newest 2026-10-21T00:09:45.896Z. **1 new message since 1100**: it is the Tuesday seat's own outbound mail (`decision_queue prior-ruling gate is now client-scoped`), not a client or an inbound. Nothing else beyond the 16:51:18Z watermark row (QA gate 29 helpers released). `coagent@` (4,676, 47 pages): newest 18:30:06Z = the 1100 watermark row (untagged, not read); no newer row. Subjects of untagged coagent@ rows were not read.

Client-human responses in Jira: every in-window comment (RD 1, HPSMPOC 9, MPSCALC 2) is posted from the one shared account and opens "BLUF:" (seat/QA voice). That account cannot separate Kam from a seat, so a 0 means "no comment that reads as a human client". GitHub: the only authors in window are the shared seat account; no bot activity this window.

## Controls (every zero has a query that must return non-zero)

- Mail: the watermark message (16:51:18.000Z) returns in the same call on tuesday-agent@ and 18:30:06Z on coagent@, and the 00:09:45Z row proves the window query can return a newer row. Instrument fires: **50** subjects containing "feedback" on tuesday-agent@, **1** starting `QuickQuote feedback (`; coagent@ 36 and 8 (identical to 1100, so no new feedback subject).
- Jira feedback search: RD summary 21 total (0 in window), RD label 5; HPSMPOC summary **27** (26 at 1100; +1 = HPSMPOC-308) / label 15 (the 1100 note said 20; the label query here is `labels in (feedback)` and counts 15, a method difference to flag, not a change in data; UNRECONCILED); MPSCALC summary 13 / label 0; VSP summary 1; HPSM 0 / 0 (never had a hit, no positive control).
- New-ticket zeros: `project = X` approximate-count totals above; max key from `ORDER BY key DESC`; the window `updated` query returns non-zero on RD (1), HPSMPOC (10), MPSCALC (2), and the wide `updated >= 2026-10-21 00:00` control returns RD 10, HPSMPOC 18, MPSCALC 8 (VSP and HPSM return 0 even wide, no positive control; their board totals match 1100).
- HPSMPOC open: paged 111 = approximate-count 111.
- GitHub zeros: `since` filter fires on HPSM-POC (2 commits, 2 PRs) and analysis (4 commits, 1 PR). On the zero repos (NexusAI, Vision Portal, QuickQuote, Composer, MPS) main HEAD is visible under the same credentials. Comment endpoints with `since=2026-09-01` return issue comments NexusAI 6, QuickQuote 4, Composer 3, HPSM-POC 4, analysis 1, MPS 2 (Vision Portal 0, no positive control); review comments NexusAI 26, Composer 5, MPS 11, HPSM-POC 10, analysis 20, so both comment endpoints fire. Review comments with `since=2026-10-19` return NexusAI 2 (fires). In window: 0 issue comments and 0 review comments everywhere read.

## FOUND

No feedback item and no client-human response anywhere. One seat-filed ticket (HPSMPOC-308, CI shard flake). Fleet merges listed in the table (HPSM-POC #170, #173; analysis #129). Nothing for each project's own agent to ticket from this sweep, so nothing for Tuesday to brief.

## TESTED

Mailbox (both inboxes, full paging, subjects/senders/timestamps only; coagent@ rows filtered on Datasec tags before anything else, none beyond the watermark row existed); Jira per project (touched list, new keys, totals, max key, feedback summary/label counts, comments on every touched issue, HPSMPOC open count paged plus approximate-count); GitHub per repo (main HEAD, commits since, PRs updated since with merged flags, open PRs, issue and review comments since, issues updated since).

## HOW

`python3 -I` scripts in the session scratchpad parsing each project's own `.env` in-process (nothing printed or written), Basic-auth GETs to the Jira site plus the read-only `search/approximate-count` POST, AgentMail list calls, `gh api` GETs under each project's own `GH_CONFIG_DIR`. QuickQuote read under the Vision Portal gh config. Local git, az, docker, ssh and every app host untouched.

## NOT TESTED

- Live feedback stores (MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, NexusAI share `feedbackItems`, Portal Postgres, QuickQuote table): need az or HTTP to app hosts, out of bounds. "0 new" means only that nothing reached the mailbox, Jira or GitHub.
- Mail bodies (subjects only); Composer BACKLOG.md and branch contents; HPSM GitHub; who exactly authored a shared-account Jira comment; the full comment text beyond the leading "BLUF:" (first 70 characters read).
- Commits-since is by commit date (the 0535 caveat stands; merges cross-checked through the `pulls` endpoint, as above).

## OUTBOUND watermarks for the next sweep

- Mailbox: tuesday-agent@ at or after **2026-10-21T00:09:45.896Z** (newest, the seat's own outbound); coagent@ newest 2026-10-20T18:30:06.000Z (unchanged).
- Jira (AEDT): RD `>= "2026-10-21 10:38"` (newest 10:38:31, unchanged); HPSMPOC `>= "2026-10-21 14:08"` (newest change 14:08:28, HPSMPOC-235 comment); MPSCALC `>= "2026-10-21 05:03"` (unchanged); VSP and HPSM `>= "2026-10-19 19:35"` (unchanged). Board totals out: RD 875 (max 879), HPSMPOC 308 (max 308), MPSCALC 315, VSP 89, HPSM 41; HPSMPOC open 111.
- GitHub: `since=2026-10-21T03:14:28Z` (newest item read: analysis PR #129 updated 03:14:28Z). Per-repo newest read: HPSM-POC main `ec0a62a1` 01:18:04Z (PR #170 merged 01:18:05Z), analysis main `1212e9e5` 03:14:27Z, MPS main `f5b6f5a7` 23:20:47Z, NexusAI main `c139e4a8` 21:37:53Z, Composer main `308b7aa6` 10-20T10:11:07Z. Open PRs to re-check: HPSM-POC #171 `cc3eae4`; NexusAI #101 `48a17df`, #102 `6dcbedb`, #103 `138b78e`, #67 `94b288c`; Composer #85 `e969ad3`, #86 `fd24426`; QuickQuote #8 `4d6ed6e`; Vision #14 `61c43d7`, #15 `72e3b17`, #16 `65d2635`, #17 `44e1b0a`.
