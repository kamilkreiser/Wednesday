BLUF: 0 new feedback, 0 client responses, 1 new ticket (MPSCALC-316, seat-filed, MPS excluded from feedback actions); briefable: none

# Rotation sweep 16:20: Datasec feedback + client-human delta, 2026-10-21

Read-only sub-agent (claude-sonnet-5-5) for Tuesday. Clock from `date`: **Wed 21 Oct 2026 16:19:48 AEDT** at start, **16:21:40 AEDT** at the last read (05:21:40Z). Method, instruments and scope copied from [[2026-10-21_rotation-sweep-1420]]: same sources, same scope (NexusAI, Vision Portal, QuickQuote, Composer, MPS, HPSM-POC, HPSM all read; MPS/HPSM-POC/HPSM read for activity, excluded from feedback actions). Feedback-store map: `0_Brain/reference/2026-10-12_datasec-feedback-stores/inventory.md`.

Windows opened at the 1420 OUTBOUND watermarks (inclusive, so the watermark rows return as controls): tuesday-agent@ >= 2026-10-21T00:09:45Z, coagent@ >= 2026-10-20T18:30:06Z; Jira RD >= 2026-10-21 10:38, HPSMPOC >= 14:08, MPSCALC >= 05:03, VSP/HPSM >= 2026-10-19 19:35 (AEDT); GitHub since=2026-10-21T03:14:28Z. All facts MEASURED (AgentMail list API; Jira Cloud `search/jql`, `/comment`, `search/approximate-count`, each project's own `4_Credentials/.env` parsed in-process, never printed; `gh api` GETs under each project's `GH_CONFIG_DIR`). No app host, production or hosted site contacted. `board_count.sh` not used (the 1420 sweep used `approximate-count`, and that script takes the token as an argument).

## BLUF

**New feedback items: 0 in every project. New client-human responses: 0. Nothing for Kam from a client.**

**New tickets: 1.**
- **MPSCALC-316** (Task, created 14:44:53 AEDT, "[B388-1] The API note and contract text say the body quoteRef is at most 100 cha...", labels lane-v0, needs-ruling, tier-2). Filed by the shared account (reporter = creator = the one account all seats use), seat-filed from QA gate B388. MPS is excluded from feedback actions. Board total **315 -> 316**, max key MPSCALC-316.
- **RD: 0 new** (875, max RD-879, both unchanged). **HPSMPOC: 0 new** (308, max 308). **VSP: 0** (89). **HPSM: 0** (41). QuickQuote and Composer have no Jira board; Composer BACKLOG.md not re-read, so a row added only on a branch is UNMEASURED.
- Control: the only non-zero delta in totals (MPSCALC 315 -> 316) equals the one new key.

**HPSMPOC open (statusCategory != Done): 111** paged, **approximate-count 111**, match (unchanged from 1420).

## Per project

| Project | New feedback items | Client-human responses | New tickets since watermark | Other activity |
|---|---|---|---|---|
| NexusAI (RD) | 0 | 0 | **0** (total 875, max RD-879) | Jira 1 touched: RD-879 (the watermark comment 10:38:31, "BLUF:" seat voice). GitHub: **PR #103 merged 05:14:43Z** (head `940dac4`); main `c139e4a8` -> **`940dac40`** (03:36:23Z; 1 commit, a forward-merge into the PR branch); open #102 head `6dcbedb` -> `b52b46f`, #101 `48a17df` -> `5cc0629`, #67 `94b288c` unchanged. 0 issue and 0 review comments. |
| Vision Portal (VSP) | 0 | 0 | 0 (total 89) | none. Jira 0 touched; main `6dbffdf3` (09-28); open PRs #14-#17 (Dependabot) unchanged. |
| QuickQuote | 0 (no `QuickQuote feedback (` mail in window) | 0 | n/a (no Jira) | none. main `5fa1187b` (10-18), PR #8 open, unchanged. |
| Security Composer | 0 | 0 | 0 on the board (see caveat) | none. main `308b7aa6` unchanged; open #86 (Dependabot), #85 (draft) unchanged; 0 comments. |
| MPSCALC (excl.) | 0 | 0 | **1: MPSCALC-316** (total 316) | Jira 4 touched: MPSCALC-304/-305 (05:03, B365 QA gate, the watermark rows), MPSCALC-316 (new), MPSCALC-289 (14:45:13 comment, "BLUF: QA gate B388 (round 2 of 2) on PR #93 ... merged as main", seat voice). GitHub: main `f5b6f5a7` (10-20 23:20Z) unchanged; 0 open PRs; nothing since the 03:14:28Z watermark. |
| HPSM-POC (excl.) | 0 (summary "feedback" 27 total, same as 1420; label 15; 0 in window) | 0 | 0 (total 308) | Jira 1 touched: HPSMPOC-235 (the 14:08:28 watermark comment, "BLUF: deployed to the hosted demo", seat voice). GitHub code repo: **PRs #171 (04:08:38Z) and #176 (04:54:52Z) merged**; main `ec0a62a1` -> **`db179494`** (04:54:51Z; 2 commits); **#177 open** (head `549e838`, 05:17:58Z, UAT start page without sign-in). Analysis repo: only PR #129 (the 03:14:28Z watermark row, merged earlier); main `1212e9e5` unchanged; 0 open. All authors the shared seat account. |
| HPSM (excl.) | 0 | 0 | 0 (total 41) | none. Jira 0 touched. GitHub UNMEASURED (`gh` not logged in under HPSM's config, same as 1420). |

Mail (tuesday-agent@): 3,750 messages, 38 pages, newest 2026-10-21T00:09:45.896Z, **unchanged from 1420**; the only row in window is that watermark row (the seat's own outbound mail). `coagent@` 4,676 messages, 47 pages, newest 2026-10-20T18:30:06Z = the watermark row (untagged, not read); no newer row. Subjects of untagged coagent@ rows were not read.

Client-human responses in Jira: every in-window comment (RD 1, HPSMPOC 1, MPSCALC 3) is posted from the one shared account and opens "BLUF:" (seat/QA voice). That account cannot separate Kam from a seat, so a 0 means "no comment that reads as a human client". GitHub: only the shared seat account authored anything in window; 0 issue comments and 0 review comments in any repo read.

## Controls (every zero has a query that must return non-zero)

- Mail: the watermark rows return in the same calls (tuesday-agent@ 00:09:45Z, coagent@ 18:30:06Z), so the window query can return a row. Instrument fires: **50** subjects containing "feedback" on tuesday-agent@, **1** starting `QuickQuote feedback (`; coagent@ 36 and 8 (identical to 1420, so no new feedback subject).
- Jira feedback search: RD summary 21 / label 5; HPSMPOC summary 27 / label 15; MPSCALC summary 13 / label 0; VSP summary 1 / label 0; HPSM 0 / 0 (never had a hit, no positive control). Counts match 1420, so no new feedback-named ticket. In window: no feedback-named ticket in any project.
- New-ticket zeros: totals from `approximate-count` and max key from `ORDER BY key DESC`; the window `updated` query returns non-zero on RD (1), HPSMPOC (1), MPSCALC (4). Wide controls `updated >= 2026-10-21 00:00` return RD 10, HPSMPOC 18, MPSCALC 10; `created >= 2026-10-21 00:00` returns RD 4, HPSMPOC 4, MPSCALC 1 (VSP and HPSM return 0 even wide, no positive control; their totals match 1420).
- HPSMPOC open: paged 111 = approximate-count 111.
- GitHub zeros: the `since` filter fires on NexusAI (1 commit, 3 PRs), HPSM-POC (2 commits, 3 PRs) and analysis (1 PR). On the zero repos (Vision Portal, QuickQuote, Composer, MPS) main HEAD is visible under the same credentials. Comment endpoints with `since=2026-09-01` return NexusAI issue comments 6 and review comments 26, HPSM-POC issue comments 4, so both comment endpoints fire; in window both are 0.

## FOUND

No feedback item and no client-human response anywhere. One seat-filed ticket (MPSCALC-316, an API-note vs contract-text length mismatch from a QA gate, labelled needs-ruling; MPS is excluded). Fleet merges: NexusAI #103, HPSM-POC #171 and #176; new open HPSM-POC #177. Nothing for Tuesday to brief.

## TESTED

Mailbox (both inboxes, full paging, subjects/senders/timestamps only; coagent@ rows filtered on Datasec/Tuesday tags before anything was printed); Jira per project (touched list, new keys, totals, max key, feedback summary/label counts, comments on every touched issue, reporter of the new key, HPSMPOC open count paged plus approximate-count); GitHub per repo (main HEAD, commits since, issues/PRs updated since, open PRs, issue and review comments since; merged flags re-checked on the `pulls` endpoint for #101, #102, #103, #171, #176, #177).

## HOW

`python3 -I` scripts in the session scratchpad parsing each project's own `.env` in-process (nothing printed or written), Basic-auth GETs to the Jira site plus the read-only `search/approximate-count` POST, AgentMail list GETs, `gh api` GETs under each project's own `GH_CONFIG_DIR`. QuickQuote read under the Vision Portal gh config. Local git, az, docker, ssh and every app host untouched.

## NOT TESTED

- Live feedback stores (MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, NexusAI share `feedbackItems`, Portal Postgres, QuickQuote table): need az or HTTP to app hosts, out of bounds. "0 new" means only that nothing reached the mailbox, Jira or GitHub.
- Mail bodies (subjects only); Composer BACKLOG.md and branch contents; HPSM GitHub; who exactly authored a shared-account Jira comment; comment text beyond the leading 70 characters.
- Commits-since is by commit date; merges cross-checked through the `pulls` endpoint.

## OUTBOUND watermarks for the next sweep

- Mailbox: tuesday-agent@ at or after **2026-10-21T00:09:45.896Z** (unchanged); coagent@ 2026-10-20T18:30:06.000Z (unchanged).
- Jira (AEDT): RD `>= "2026-10-21 10:38"` (unchanged); HPSMPOC `>= "2026-10-21 14:08"` (unchanged); MPSCALC `>= "2026-10-21 14:45"` (newest change 14:45:13, MPSCALC-289 comment); VSP and HPSM `>= "2026-10-19 19:35"` (unchanged). Board totals out: RD 875 (max 879), HPSMPOC 308 (max 308), MPSCALC 316 (max 316), VSP 89, HPSM 41; HPSMPOC open 111.
- GitHub: `since=2026-10-21T05:17:58Z` (newest item read: HPSM-POC #177 updated 05:17:58Z). Per-repo main: NexusAI `940dac40` 03:36:23Z, HPSM-POC `db179494` 04:54:51Z, analysis `1212e9e5` 03:14:27Z, MPS `f5b6f5a7` 10-20T23:20:47Z, Composer `308b7aa6` 10-20T10:11:07Z, Vision `6dbffdf3`, QuickQuote `5fa1187b`. Open PRs to re-check: HPSM-POC #177 `549e838`; NexusAI #101 `5cc0629`, #102 `b52b46f`, #67 `94b288c`; Composer #85, #86; QuickQuote #8; Vision #14-#17.
