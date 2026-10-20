# Rotation sweep: Datasec feedback delta, Part 1 only (2026-10-20, 13:00)

A read-only sub-agent (claude-sonnet-5-5) ran this for Tuesday. Clock from the shell: `date` = **Tue 20 Oct 2026 12:57:36 AEDT** (01:57:36Z) at start and **12:59:53 AEDT** (01:59:53Z) at the last read. (The shell clock runs about 1 h earlier than the "06:00" label of the previous file would imply; every edge below is stated in both zones, so the window is unambiguous.)

Method, instruments, controls and table shape copied from [[2026-10-20_morning-sweep-0600]] (itself from [[2026-10-19_rotation-sweep-2030]]). Window edges are the 06:00 file's section 3, not assumed:

- Mailbox: at or after **2026-10-19T17:22:34Z** (about 8 h 35 min to read time).
- Jira: RD `>= "2026-10-20 04:20"` AEDT; HPSMPOC `>= "2026-10-19 21:10"` AEDT; VSP, HPSM, MPSCALC `>= "2026-10-19 19:35"` AEDT (their last watermark, the 06:00 file's W).
- GitHub: `since=2026-10-19T18:58:00Z`.

Part 2 (ticket sweep) is not in this run.

## 1. BLUF

**New feedback items: 0 across all projects. New client-human responses: 0. No ticket needed.** The window is fleet work only: NexusAI landed C-170 (PR #96, main `39653db`), the NexusAI seat filed RD-868 and is on RD-863 and the PR #97 / PR #98 branches; HPSM-POC merged PR #164 (main `c149a303`) with records PR #124 and the seat filed HPSMPOC-301/-302; MPS merged PR #84 and the seats opened PRs #85/#86 and filed 56 MPSCALC tickets; Composer opened draft PR #82. The one human-sender mail in the window is Kam forwarding a GitHub notification (the CodeQL bot comment on NexusAI PR #97), not a client submission.

| Project | New feedback items | Client-human responses | Other activity in window (not feedback) |
|---|---|---|---|
| **NexusAI** (RD) | **0** | **0** | Jira: 16 issues touched, **1 created** (**RD-868**, 07:33 AEDT, "Risk-condition store: writers outside RD-836 ...", seat-filed; `project = RD` 863 -> **864**). 16 comments, all seat voice ("S101O: LANDED / started / READY ..." on RD-476, RD-460, RD-505, RD-506, RD-836, RD-774, RD-863; "Correction (S101O)" on RD-868; "BLUF: pushed @ 8bb6c33 / 49ba21e on b302/test-code-codeql" on RD-782..789). GitHub: main `29c5ee8f` -> **`39653db4`** (1 commit, 18:58:25Z, merge of main into the C-170 branch); **PR #96 merged** 19:48:38Z (C-170 / RD-460); PR #97 open draft, head **`278afc2`** (updated 00:54Z); **PR #98 new** (open draft, RD-782..789 CodeQL in test code, head `49ba21e`); open PRs #98(d), #97(d), #67. 0 issue comments; 1 review comment (`github-advanced-security[bot]` on #97, 22:34:13Z, "File data in outbound network request"). Mail: 9 `coagent@` / `tuesday-agent@` seat messages (READY TO LAND / MERGED C-170, ANSWER-27, ANSWER-28, ticket keys RD-863..868, PR #97 new head 278afc2, plan confirmation RD-863 and its ANSWER) plus 1 Kam forward of the GitHub notification for PR #97 (23:54:21Z). |
| **Vision Portal** (VSP) | **0** | **0** | None. Jira 89 unchanged; GitHub main `6dbffdf3` (09-28), 4 Dependabot PRs (#14-#17) unchanged. |
| **Vision QuickQuote** | **0** (no `QuickQuote feedback (` mail) | **0** | None. GitHub main `5fa1187b` (10-18T09:57Z), PR #8 open, unchanged. |
| **Security Composer** | **0** | **0** | GitHub: **PR #82 opened** (draft, "B301: CI timing-test truth (BACKLOG #326 split bound, #327 Node comment labels)", `kamilDatasec`, updated 01:42:26Z). Main still `d8d2a2c7`. 0 commits, 0 comments. |
| **MPS Calculator** (MPSCALC, *excluded*) | 0 seen | **0** | Jira: 67 issues touched, **56 created** (MPSCALC-232..287, 10:33-10:35 AEDT, T-V0..T-V11 build-plan tickets; `project = MPSCALC` 231 -> **287**), 21 comments, all "BLUF:" seat voice (b303 push, "planned as T-V..." plan comments, b309 / b313 pushes). GitHub: **PR #84 merged** (main `acfcf5de`, 23:42:02Z); **PRs #85 and #86 new** (open, V0 quote contract and V5 starters, updated 01:52-01:53Z). Summary "feedback" 0 in window / 13 total; label 0 / 0. (The brief counted 66 tickets; the project total grew by 56, which is what is visible here.) |
| **HPSM-POC** (HPSMPOC, *excluded*) | 0 submissions seen | **0** | Jira: 7 issues touched, **2 created** (**HPSMPOC-301, -302**, 11:30 AEDT, B304 follow-ups, seat-filed; 300 -> **302**), 8 comments, all "BLUF:" seat voice (-226, -267, -298, -299, -300 incl. "merged as HPSM-POC#164"). Label hit in window 1 and summary hit 1: both HPSMPOC-226 ("Feedback attachments follow-ups", an existing seat follow-up ticket touched by a BLUF comment), not a submission. GitHub: **PR #164 merged** (main `c149a303`, 00:11:40Z); analysis repo main `9af1d55a` (3 commits, **records PR #124** merged 00:45Z); no open PRs. |
| **HPSM** (HPSM) | 0 | 0 | Jira none (41 unchanged). GitHub **UNMEASURED** (`gh` not logged in under `HPSM/4_Credentials/.gh-config`; every call returned the "gh auth login" prompt). |

**Actionable items: none.** There are no feedback items to categorise. (RD-868, HPSMPOC-301/-302 and MPSCALC-232..287 already exist and are seat-filed.)

## 2. Method and controls

### Mailbox (tuesday-agent@agentmail.to)
- `GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`, paged by `page_token` to the end: **3,727 messages, 38 pages**; newest **2026-10-20T01:51:14.774Z** (about 6 min before read time), oldest 2026-09-08T21:47:13Z. Subjects, senders, timestamps only; no bodies read.
- **13 messages from the watermark on** (the watermark message plus 12): `coagent@` 6 (NexusAI-O MERGED RD-476 @ 29c5ee8 [the watermark, 17:22:34Z]; READY TO LAND C-170 @ 39653db; MERGED C-170 @ 39653db PR #96 (20:48Z); Ticket keys RD-863..868 / N28-11 lock evidence (20:53Z); MPS QUESTION T-V0-1 allow-list (23:51Z); PR #97 new head 278afc2 (01:47Z); QUESTION plan confirmation RD-863 (01:49Z)); `tuesday-agent@` 3 (ANSWER-27 19:47Z, ANSWER-28 23:57Z, ANSWER plan confirmation RD-863 01:51Z); `wednesday-agent@` 1 (ATTIO digest retarget, 21:02Z); `kamil.kreiser@datasec.com.au` 1 (23:54:21Z, `FW: [datasecau/Reporting_Dashboard_Au] RD-774 + RD-836 ... (PR #97)`, the same forwarded-GitHub-notification pattern as the 10-19T03:49Z forwards). `datasec-vision@` 0.
- **0 feedback notices, 0 client senders** in the window; no subject in the window contains "feedback".
- **Control 1 (continuity):** the watermark message (17:22:34.000Z, MERGED RD-476) comes back in the same call.
- **Control 2 (instrument fires):** the same read returns 50 subjects containing "feedback" (newest a Kam forward, 2026-10-17T04:56:13Z) and exactly 2 `QuickQuote feedback (` notices (newest 2026-10-09T16:51:40Z, then 2026-09-22T03:38:14Z).

### Jira (JQL in AEDT; every list paged to the end; read about 12:58-12:59)
Instrument: each project's own `4_Credentials/.env` read by variable name inside `python3 -I`, never printed; `GET /rest/api/3/search/jql` (`maxResults 100`, `nextPageToken`) and `/issue/<key>/comment`; comment times converted to UTC and compared to the window edge.

| Project | W | JQL | Result | Control |
|---|---|---|---|---|
| RD | `2026-10-20 04:20` | `project = RD AND (created >= W OR updated >= W)` | **16**: RD-476, RD-460, RD-505, RD-506, RD-868, RD-789, -784, -785, -788, -782, -783, -786, -787, RD-836, RD-774, RD-863; **1 created** (RD-868) | `project = RD ORDER BY key` = **864** (863 + RD-868, exactly the one created). Prior window (`updated >= "2026-10-18 21:15"`) returns **33**, so the query fires. |
| RD | | `summary ~ "feedback"`, in window / total | 0 / 21 | total unchanged (21) |
| RD | | `labels in (feedback, user-feedback, hp-feedback)`, in window / total | 0 / 5 | total unchanged (5) |
| RD comments | | created at or after W on the 16 issues | **16**, all seat voice (opening about 130 chars read: "S101O: ...", "Correction (S101O)", "BLUF: pushed @ ...") | |
| VSP | `2026-10-19 19:35` | window query | **0** | total 89 unchanged; feedback summary 0 in window / **1** total (instrument matches); label 0 / 0. Prior window also returns 0 updated, so the zero has no in-window positive control; it rests on the unchanged total and the 1 summary match. |
| HPSM | `2026-10-19 19:35` | window query | **0** | total 41 unchanged; summary 0 / 0, label 0 / 0 (HPSM has never had a feedback hit: no project-specific control). |
| HPSMPOC | `2026-10-19 21:10` | window query | **7**: -226, -267, -301, -302, -298, -299, -300; **2 created** (-301, -302) | total 300 -> **302** (+2 = exactly -301, -302). Prior window returns **40** updated, 6 summary, 9 label. |
| HPSMPOC | | feedback summary / label, in window | summary 1 (-226) of **24** total; label 1 (-226) of **20** total | totals unchanged. Seat follow-up ticket touched by a BLUF comment at 21:11, not a submission. |
| HPSMPOC comments | | same method | **8** (-226, -267 at 21:11; -298, -299, -300 at 08:56 and 11:31) | every one opens "BLUF:" (seat voice) |
| MPSCALC (*excluded*) | `2026-10-19 19:35` | window query | **67** touched, **56 created** (MPSCALC-232..287); 21 comments all "BLUF:" seat voice | total 231 -> **287** (+56 = created). Summary "feedback" 0 / **13** total (instrument matches), label 0 / 0. Prior window returns 67 updated. |

**Positive control (same script, prior window `2026-10-18 21:15`):** RD 33 updated, 0 summary, 0 label; HPSMPOC 40 / 6 / 9; VSP 0; HPSM 0; MPSCALC 67. The instrument sees feedback-labelled rows when they exist (HPSMPOC 6 and 9).

**Client-human responses in Jira: 0.** The opening of all 45 in-window comments (16 RD, 8 HPSMPOC, 21 MPSCALC) reads as seat voice. The shared "Kamil Kreiser" account cannot separate Kam from a seat.

### GitHub (`gh api` GETs, `since=2026-10-19T18:58:00Z`, read about 12:58 AEDT; each under its own project's `GH_CONFIG_DIR`)

| Repo | Commits on main since | Issues/PRs updated since | Issue / review comments since | Open PRs | Control: main HEAD |
|---|---|---|---|---|---|
| Reporting_Dashboard_Au (NexusAI) | **1** (`39653db4` 18:58:25Z, merge of main 29c5ee8 into the C-170 branch) | **3**: #97 (open draft, 00:54:31Z), #98 (open draft, new, 00:28:08Z), #96 (merged 19:48:38Z) | 0 / **1** (bot, #97, 22:34:13Z) | #98(d), #97(d), #67 | `39653db4` 10-19T18:58:25Z |
| vision_datasec-sales-portal | 0 | 0 | 0 / 0 | #14-#17 (Dependabot) | `6dbffdf3` 09-28 |
| vision_hpas-quickquote | 0 | 0 | 0 / 0 | #8 | `5fa1187b` 10-18T09:57Z |
| Datasec-Security-Composer | 0 | **1**: #82 (open draft, new, 01:42:26Z) | 0 / 0 | #82(d) | `d8d2a2c7` 10-19T18:13:47Z |
| HPSM-POC (*excluded*) | **1** (`c149a303` 00:11:40Z, PR #164) | **1**: #164 (merged 00:11:41Z) | 0 / 0 | none | `c149a303` |
| HPSM-POC-analysis (*excluded*) | **3** (`374b5b24`, `41c68cd2`, merge `9af1d55a` 00:45:05Z; Records B315) | **1**: #124 (merged 00:45:06Z) | 0 / 0 | none | `9af1d55a` |
| MPS-Commercial-Calculator (*excluded*) | **1** (`acfcf5de` 23:42:02Z, PR #84) | **3**: #84 (merged), #85, #86 (open, 01:52-01:53Z) | 0 / 0 | #86, #85 | `acfcf5de` |
| HPSM (*excluded*) | **UNMEASURED** | | | | `gh` not logged in under HPSM's config |

**Controls:** the `since` filter fires on NexusAI, Composer, HPSM-POC, analysis and MPS; on each zero repo (Vision Portal, QuickQuote) the pre-window HEAD is visible under the same credentials. **Comment endpoints:** review comments fire on NexusAI (the in-window #97 bot comment, plus the earlier 10-19T01:42:56Z one on the same PR); issue comments re-run with `since=2026-09-01T00:00:00Z` returns 6, so the endpoint fires; none since the watermark. Merged flags for #96, #164, #84 read from `pulls/<n>` (`merged: true`); #97, #98 `merged: false`. No non-PR GitHub issue opened anywhere. All authors `kamilDatasec` (the shared account; seat PRs) or the code-scanning bot.

## 3. Watermarks out
- **Mailbox:** 2026-10-20T01:51:14.774Z (`tuesday-agent@` ANSWER plan confirmation RD-863, the newest message read).
- **Jira:** newest processed change **RD-863 comment 2026-10-20 12:49:08** AEDT (RD) and **HPSMPOC-300 comment 2026-10-20 11:31:51** AEDT (newest HPSMPOC update). Next run RD `>= "2026-10-20 12:45"`, HPSMPOC `>= "2026-10-20 11:30"` (small overlap; seats are active). VSP and HPSM: unchanged, keep `>= "2026-10-19 19:35"`. MPSCALC (excluded): newest update 12:44:24 AEDT, next `>= "2026-10-20 12:40"`.
- **GitHub:** `since=2026-10-20T01:53:00Z` (newest item read: MPS #86 updated 01:53:07Z; Composer #82 01:42:26Z, NexusAI #97 00:54:31Z are older and counted here). HPSM not measured, no edge advanced for it.

## 4. Not done
- **Every live feedback store is UNMEASURED:** MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, the NexusAI share `feedbackItems`, Portal Postgres, the QuickQuote table. Each needs az, a writing sign-in or HTTP to a hosted host, all out of bounds. **"0 new" means only that nothing reached the mailbox, Jira or GitHub.**
- **Who wrote a Jira comment:** the shared account cannot tell Kam from a seat; only openings (about 130 characters) were read.
- **HPSM GitHub:** `gh` not logged in under HPSM's config.
- **Mail bodies** not read (including the Kam forward of the PR #97 notification, classified by subject and sender only); `coagent@` bus and other inboxes not read (the `coagent@` rows are copies that reached `tuesday-agent@`).
- **Kam's card board** not re-read.
- **MPS ticket count:** the brief said 66 tickets filed by B308; the Jira project total moved 231 -> 287 (+56) and 56 carry a created time in the window. The other 10 are not visible in Jira from this instrument (not investigated).
- **Part 2** (ticket sweep) not in scope for this run.
- No HTTP to any app host, hosted site or production (only the AgentMail API, Jira Cloud search and comment reads, and `api.github.com`); no az, docker or ssh; no Jira, gh, mail or card writes. Temporary scripts lived in the session scratchpad.
