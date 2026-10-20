# Rotation sweep: Datasec feedback delta, Part 1 only (2026-10-20, 21:00)

A read-only sub-agent (claude-sonnet-5-5) ran this for Tuesday. Clock from the shell: `date` = **Tue 20 Oct 2026 20:59:38 AEDT** (09:59:38Z) at start and **21:02:41 AEDT** (10:02:41Z) at the last read. Window closes at that last read.

Method, instruments, controls and table shape copied from [[2026-10-20_rotation-sweep-1300]] (itself from [[2026-10-20_morning-sweep-0600]]). Window opens at the 13:00 file's OUTBOUND watermarks (its section 3), quoted here:

- Mailbox: at or after **2026-10-20T01:51:14.774Z** (12:51:14 AEDT); about 8 h 8 min to read time.
- Jira: RD `>= "2026-10-20 12:45"` AEDT (01:45Z); HPSMPOC `>= "2026-10-20 11:30"` AEDT (00:30Z); MPSCALC (excluded) `>= "2026-10-20 12:40"` AEDT (01:40Z); VSP and HPSM `>= "2026-10-19 19:35"` AEDT (08:35Z 10-19).
- GitHub: `since=2026-10-20T01:53:00Z` (12:53:00 AEDT).

Part 2 (ticket sweep) is not in this run.

## 1. BLUF

**Needs Kam from a client human: nothing. New feedback items: 0 across all projects. New client-human responses: 0. No ticket needed.** The window is fleet work only: NexusAI landed RD-863 (PR #99, main `aa811cf2`) after QA gates 30/31/32, the seat filed RD-869..RD-873 from gate findings; Composer merged PR #82 and PR #83 and opened draft PR #84; MPS merged four PRs (#87, #85, #88, #86; main `67bf2004`) and filed 18 MPSCALC tickets from QA gates. No mail in the window comes from a client or from Kam; every row is a seat, QA or Tuesday message.

| Project | New feedback items | Client-human responses | Other activity in window (not feedback) |
|---|---|---|---|
| **NexusAI** (RD) | **0** | **0** | Jira: 11 issues touched, **5 created** (**RD-869..RD-873**, 17:59-19:59 AEDT, all reporter "Kamil Kreiser" shared account, labels `ai-assistant` / `b338-2026-10-20` / `gate-30` / `gate-31` / `codeql-baseline`, gate-finding follow-ups); `project = RD` 864 -> **869**. 6 comments, all seat voice (RD-863 "S101O: started / READY FOR QA / LANDED via PR #99", RD-836 and RD-774 "S101O: ...", RD-786 "BLUF: gate 30 round 1 ..."). GitHub: main `39653db4` -> **`aa811cf2`** (3 commits: `172d321f` RD-863 fix, `1bc9e9df` HISTORY.md, `aa811cf2` merge, 05:20:08Z); **PR #99 merged** 05:59:36Z (RD-863), **PR #100 merged** 03:43:25Z (HISTORY docs); PR #98 open draft (head `e80920c`), PR #97 open draft (head `278afc2`, unchanged), PR #67 open; 0 issue comments, 0 review comments. Mail: 14 rows, all seat / QA / Tuesday (see section 2). |
| **Vision Portal** (VSP) | **0** | **0** | None. Jira 89 unchanged; GitHub main `6dbffdf3` (09-28), Dependabot PRs #14-#17 unchanged. |
| **Vision QuickQuote** | **0** (no `QuickQuote feedback (` mail) | **0** | None. GitHub main `5fa1187b` (10-18T09:57Z), PR #8 open, unchanged. |
| **Security Composer** | **0** | **0** | GitHub: main `d8d2a2c7` -> **`eaff2b74`** (2 commits: `318df176` PR #82 B301, 07:22:28Z; `eaff2b74` PR #83 "L3-1: exception review date, review frequency and device-group scope (migration 0022 ...)", 09:13:29Z); **PR #82 and #83 merged**; **PR #84 new** (open draft, "B323 (L6-a): policy PDF contents page ...", updated 08:54:44Z). 0 issue / review comments. |
| **MPS Calculator** (MPSCALC, *excluded*) | 0 seen | **0** | Jira: 42 issues touched, **18 created** (MPSCALC-288..305, 20:07-20:08 AEDT, `[Bxxx-n]` QA-gate findings, labels `mpscalc-b340`, `lane-*`, `tier-*`); `project = MPSCALC` 287 -> **305**; 52 comments, all "BLUF:" seat / QA voice (B3xx pushes and QA gate verdicts on PRs #84-#88). GitHub: main `acfcf5de` -> **`67bf2004`** (4 commits, 03:14-03:58Z; **PRs #87, #85, #88, #86 merged**); no open PRs. Summary "feedback" 0 in window / 13 total; label 0 / 0. |
| **HPSM-POC** (HPSMPOC, *excluded*) | 0 submissions seen | **0** | Jira: 5 touched (-298, -299, -300, -301, -302), 2 "created" in window are -301/-302 at 11:30 AEDT, **already counted in the 13:00 sweep** (the window overlaps by design; project total 302 unchanged). 3 comments (-298/-299/-300 at 11:31:50-51, "BLUF: merged as HPSM-POC#164", also seen 13:00). Summary / label in window 0 / 0 (totals 24 / 20, unchanged). GitHub: code repo main `c149a303` and analysis repo main `9af1d55a` unchanged; no open PRs. No new activity since the 13:00 sweep. |
| **HPSM** (HPSM) | 0 | 0 | Jira none (41 unchanged). GitHub **UNMEASURED** (`gh` not logged in under `HPSM/4_Credentials/.gh-config`; every call returned the "gh auth login" prompt, as on 13:00). |

**Actionable items: none.** There are no feedback items to categorise. RD-869..RD-873 and MPSCALC-288..305 are seat-filed from QA findings, not client submissions.

## 2. Method and controls

### Mailbox (tuesday-agent@agentmail.to)
- `GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`, paged by `page_token` to the end, read about 21:00 AEDT: **3,740 messages, 38 pages**; newest **2026-10-20T09:53:01.000Z** (about 10 min before read time), oldest 2026-09-08T21:47:13Z. Subjects, senders and timestamps only; no bodies read. No subject named Secuura or another client.
- **14 messages from the watermark on** (the watermark message plus 13): `tuesday-agent@` 5 (ANSWER plan confirmation RD-863 [the watermark, 01:51:14.774Z]; ANSWER gate 30 04:17Z; ANSWER gate 31 04:45Z; ANSWER-30 GO land RD-863 04:49Z), `coagent@` 9 (NexusAI-O READY FOR QA RD-863 02:57Z; NexusAI-O Session wrap 03:42Z; QA QUESTION / ADDENDUM / GATE VERDICT gate 30 at 04:15, 04:22, 04:22Z; QA QUESTION and GATE VERDICT gate 31 at 04:44, 04:48Z; NexusAI-O MERGED RD-863 @ aa811cf PR #99 07:00Z; QA QUESTION gate 32 deadline 08:55Z; QA GATE VERDICT gate 32 09:53Z). `datasec-vision@` 0; `kamilDatasec`/Kam forwards 0; `wednesday-agent@` 0.
- **0 feedback notices, 0 client senders**; no subject in the window contains "feedback".
- **Control 1 (continuity):** the watermark message (01:51:14.774Z) comes back in the same call.
- **Control 2 (instrument fires):** the same read returns **50** subjects containing "feedback" (newest a Kam forward, 2026-10-17T04:56:13Z; same as 13:00) and exactly **2** subjects starting `QuickQuote feedback (` (2026-10-09T16:51:40Z, plus a `Fwd:` copy on 2026-09-22T03:38:14Z). (A looser case-insensitive "quickquote feedback" match also returns a Wednesday brief of 2026-10-12, which is not a notice.)

### Jira (JQL in AEDT; every list paged to the end; read 21:01:19-21:01:41)
Instrument: each project's own `4_Credentials/.env` sourced transiently with `set -a` into `python3 -I`, never printed; `GET /rest/api/3/search/jql` (`maxResults 100`, `nextPageToken`) and `/issue/<key>/comment`; comment times converted to AEDT and compared with the window edge. Reporter / labels / summary read for the new RD and MPSCALC tickets (samples RD-864, -811, -869..-873; MPSCALC-288, -296, -305).

| Project | W | Result | Control |
|---|---|---|---|
| RD | `2026-10-20 12:45` | **11 touched**: RD-873, -872, -871, -870, -869, -864, -863, -836, -811, -786, -774; **5 created** (RD-869..873) | `project = RD ORDER BY key` = **869** (864 + 5 created, exactly). Prior-window query (`updated >= "2026-10-20 04:20"`) returns **23**, so the query fires. |
| RD | | `summary ~ "feedback"` in window 0 / total 21; `labels in (feedback, user-feedback, hp-feedback)` in window 0 / total 5 | totals unchanged from 13:00 (21, 5) |
| RD comments | | **6**, all seat voice (openings read, about 110 chars: "S101O: ...", "BLUF: gate 30 round 1 found one Major on PR #98 ...") | newest comment RD-786 20:00:18 |
| VSP | `2026-10-19 19:35` | **0** touched | total 89 unchanged; summary 0 in window / **1** total (instrument matches); label 0 / 0. Prior-window control also returns 0, so the zero has no in-window positive control; it rests on the unchanged total and the 1 summary match (same limit as 13:00). |
| HPSM | `2026-10-19 19:35` | **0** touched | total 41 unchanged; summary 0 / 0, label 0 / 0 (HPSM has never had a feedback hit: no project-specific control). |
| HPSMPOC | `2026-10-20 11:30` | **5 touched** (-298..-302), 2 created (-301, -302; overlap with 13:00); 3 comments, all "BLUF:" | total **302** = 13:00's 302. Summary / label in window 0 / 0 of **24** / **20** total (unchanged). Prior window (`>= "2026-10-19 21:10"`) returns **7**. |
| MPSCALC (*excluded*) | `2026-10-20 12:40` | **42 touched**, **18 created** (MPSCALC-288..305); 52 comments, all "BLUF:" seat / QA voice | total 287 -> **305** (+18 = created). Summary 0 / **13** total, label 0 / 0 (totals unchanged). Prior window (`>= "2026-10-19 19:35"`) returns **85**. |

**Positive control (same script):** the feedback-labelled rows exist and are matched: RD summary 21 / label 5 total, HPSMPOC summary 24 / label 20, MPSCALC summary 13, VSP summary 1. The window queries fire on RD (11), HPSMPOC (5) and MPSCALC (42).

**Client-human responses in Jira: 0.** The opening of all 61 in-window comments (6 RD, 3 HPSMPOC, 52 MPSCALC) reads as seat / QA voice. The shared "Kamil Kreiser" account cannot separate Kam from a seat.

### GitHub (`gh api` GETs, `since=2026-10-20T01:53:00Z`, read about 21:02 AEDT; each under its own project's `GH_CONFIG_DIR`)

| Repo | Commits on main since | Issues/PRs updated since | Issue / review comments since | Open PRs | Control: main HEAD |
|---|---|---|---|---|---|
| Reporting_Dashboard_Au (NexusAI) | **3** (`172d321f` 02:19Z, `1bc9e9df` 03:43Z, `aa811cf2` 05:20:08Z) | **3**: #99 (merged 05:59:36Z), #98 (open draft, 05:30:45Z), #100 (merged 03:43:25Z) | 0 / 0 | #98(d), #97(d), #67 | `aa811cf2` 10-20T05:20:08Z |
| vision_datasec-sales-portal | 0 | 0 | 0 / 0 | #14-#17 (Dependabot) | `6dbffdf3` 09-28 |
| vision_hpas-quickquote | 0 | 0 | 0 / 0 | #8 | `5fa1187b` 10-18T09:57Z |
| Datasec-Security-Composer | **2** (`318df176` 07:22:28Z, `eaff2b74` 09:13:29Z) | **3**: #82 (merged), #83 (merged 09:13:30Z), #84 (open draft, new, 08:54:44Z) | 0 / 0 | #84(d) | `eaff2b74` |
| HPSM-POC (*excluded*) | 0 | 0 | 0 / 0 | none | `c149a303` 10-20T00:11:40Z |
| HPSM-POC-analysis (*excluded*) | 0 | 0 | 0 / 0 | none | `9af1d55a` 10-20T00:45:05Z |
| MPS-Commercial-Calculator (*excluded*) | **4** (`1b32bbe6` 03:14Z, `f2584d36` 03:31Z, `77e541c8` 03:54Z, `67bf2004` 03:58:33Z) | **4**: #87, #85, #88, #86 (all merged) | 0 / 0 | none | `67bf2004` |
| HPSM (*excluded*) | **UNMEASURED** | | | | `gh` not logged in under HPSM's config |

**Controls:** the `since` filter fires on NexusAI, Composer and MPS; on each zero repo (Vision Portal, QuickQuote, HPSM-POC, analysis) the pre-window HEAD is visible under the same credentials. **Comment endpoint control:** issue comments re-run with `since=2026-09-01T00:00:00Z` returns NexusAI 6, QuickQuote 4, Composer 3, HPSM-POC 3, analysis 1, MPS 2, so the endpoint fires (Vision Portal returns 0 total there, so its zero comment count has no positive control); none since the watermark. Review comments on NexusAI: the earlier `github-advanced-security[bot]` comments on #97 (10-19, 10-19 22:34Z) are before the window; none new. Merged flags for #99, #100, #82, #83, #85-#88 read from `pulls/<n>` (all `merged: true`). No non-PR GitHub issue opened anywhere. All authors `kamilDatasec` (the shared account; seat PRs).

## 3. Window edges and watermarks out

Window: opened per the quoted watermarks above; closed at the last read **21:02:41 AEDT (10:02:41Z)**. Read span 20:59:38-21:02:41 AEDT (09:59:38-10:02:41Z). Edges, AEDT / UTC:

- **Mailbox:** 2026-10-20T09:53:01.000Z (20:53:01 AEDT; QA GATE VERDICT gate 32, the newest message read).
- **Jira:** newest processed change RD-786 comment **2026-10-20 20:00:18 AEDT** (RD-873 created 19:59:59); next run RD `>= "2026-10-20 19:55"` (08:55Z), small overlap. HPSMPOC newest update 11:31:51 AEDT unchanged; next `>= "2026-10-20 11:30"` (00:30Z). MPSCALC (excluded) newest update **20:10:49 AEDT**; next `>= "2026-10-20 20:05"` (09:05Z). VSP and HPSM: unchanged, keep `>= "2026-10-19 19:35"`.
- **GitHub:** newest item read: Composer #83 updated **2026-10-20T09:13:30Z** (20:13:30 AEDT). Next run `since=2026-10-20T09:13:00Z`. HPSM not measured, no edge advanced for it.

## 4. UNMEASURED
- **Every live feedback store:** MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, the NexusAI share `feedbackItems`, Portal Postgres, the QuickQuote table. Each needs az, a writing sign-in or HTTP to a hosted host, all out of bounds. **"0 new" means only that nothing reached the mailbox, Jira or GitHub.**
- **Who wrote a Jira comment:** the shared account cannot tell Kam from a seat; only openings (about 110-130 characters) were read.
- **HPSM GitHub:** `gh` not logged in under HPSM's config.
- **Mail bodies** not read; `coagent@` bus and other inboxes not read (the `coagent@` rows are copies that reached `tuesday-agent@`).
- **Vision Portal comment endpoint** has no positive control (0 comments total since 09-01).
- **Kam's card board** not re-read.
- **Part 2** (ticket sweep) not in scope for this run.
- No HTTP to any app host, hosted site or production (only the AgentMail API, Jira Cloud search and comment reads, and `api.github.com`); no az, docker or ssh; no git commands in project repos; no Jira, gh, mail or card writes. Temporary scripts lived in the session scratchpad.
