# Rotation sweep: Datasec feedback delta, Part 1 only (2026-10-20, 22:40)

A read-only sub-agent (claude-sonnet-5-5) ran this for Tuesday. Clock from the shell: `date` = **Tue 20 Oct 2026 22:36:24 AEDT** (11:36:24Z) at start and **22:38:30 AEDT** (11:38:30Z) at the last read. Window closes at that last read.

Method, instruments, controls and table shape copied from [[2026-10-20_rotation-sweep-2100]] (itself from [[2026-10-20_rotation-sweep-1300]] and [[2026-10-20_morning-sweep-0600]]). Window opens at the 21:00 file's OUTBOUND watermarks (its section 3), quoted here:

- Mailbox: at or after **2026-10-20T09:53:01.000Z** (20:53:01 AEDT); about 1 h 43 min to read time.
- Jira: RD `>= "2026-10-20 19:55"` AEDT (08:55Z); HPSMPOC `>= "2026-10-20 11:30"` AEDT (00:30Z); MPSCALC (excluded) `>= "2026-10-20 20:05"` AEDT (09:05Z); VSP and HPSM `>= "2026-10-19 19:35"` AEDT (08:35Z 10-19).
- GitHub: `since=2026-10-20T09:13:00Z` (20:13:00 AEDT).

Part 2 (ticket sweep) is not in this run.

## 1. BLUF

**Needs Kam from a client human: nothing. New feedback items: 0 across all projects. New client-human responses: 0. No ticket needed.** The window is fleet work only: NexusAI merged PR #98 (RD-782..789 CodeQL in test code, 22:16 AEDT); Composer merged PR #84 (B323 policy PDF contents page) and opened draft PR #85; MPS opened PRs #89 and #90; HPSM-POC deployed main `c149a303` to the hosted demo and filed HPSMPOC-303/-304 from gate B316 / B346; MPS filed no new tickets but pushed branches b311 and b345 against about 30 tickets. The only two mails in the window are a QA gate verdict and an MPS seat question; neither is from a client or from Kam.

| Project | New feedback items | Client-human responses | Other activity in window (not feedback) |
|---|---|---|---|
| **NexusAI** (RD) | **0** | **0** | Jira: 7 touched (RD-786, -811, -863, -869, -870, -872, -873), **2 created in window** (RD-872 19:59:53, RD-873 19:59:59, both already counted in the 21:00 sweep, the window overlaps by design); `project = RD` total **869** unchanged. 1 comment: RD-786 20:00:18 "BLUF: gate 30 round 1 found one Major on PR #98 ..." (also seen at 21:00). GitHub: main `aa811cf2` -> **`d463f881`** (1 commit, 10:09:38Z = 21:09:38 AEDT, "Merge main aa811cf (RD-863 172d321, HISTORY.md 1bc9e9d) into b302/test-code-codeql"); **PR #98 merged** 11:16:38Z (22:16:38 AEDT); PR #97 open draft (head `278afc2`, unchanged), PR #67 open (unchanged); 0 issue comments, 0 review comments. Mail: 1 row (QA GATE VERDICT gate 32, the watermark itself). |
| **Vision Portal** (VSP) | **0** | **0** | None. Jira 89 unchanged; GitHub main `6dbffdf3` (09-28), Dependabot PRs #14-#17 unchanged. |
| **Vision QuickQuote** | **0** (no `QuickQuote feedback (` mail in window) | **0** | None. GitHub main `5fa1187b` (10-18T09:57Z), PR #8 open, unchanged. |
| **Security Composer** | **0** | **0** | GitHub: main `eaff2b74` -> **`308b7aa6`** (1 commit, 10:11:07Z = 21:11:07 AEDT, "B323 (L6-a): policy PDF contents page with matching page numbers (#84)"); **PR #84 merged** 10:11:08Z; **PR #85 new** (open draft, "HOLD K6: L1 SM 3.16 content catalogue (release built, not cut)", head `40b332c`, created and updated 11:34:38Z = 22:34:38 AEDT). 0 issue / review comments. |
| **MPS Calculator** (MPSCALC, *excluded*) | 0 seen | **0** | Jira: 47 touched, **18 "created" in window are MPSCALC-288..305 (20:07-20:08 AEDT), already counted in the 21:00 sweep**; `project = MPSCALC` total **305** unchanged (no new ticket). 45 comments, all "BLUF:" seat / QA voice: QA gate B3xx verdicts on PRs #84-#88 at 20:09-20:10 AEDT (the tail of the 21:00 sweep's window), and seat pushes "pushed @ 0d7250e on branch b311/v2-home" (21:38) and "pushed @ 5f0bd02 on branch b345/v1-workspace-frame-p2" (22:19). Summary "feedback" 0 in window / 13 total; label 0 / 0. GitHub: main `67bf2004` unchanged (03:58:33Z); **PR #89 new** (open, "V2 Home: Ready to Export tab ...", head `2278484`, created 10:40:10Z, updated 11:33:48Z); **PR #90 new** (open, "V1 phase 2: rail fixes ...", head `5f0bd02`, created and updated 11:21:40Z). Mail: 1 row (see section 2). |
| **HPSM-POC** (HPSMPOC, *excluded*) | 0 submissions seen | **0** | Jira: 13 touched; **4 created in window**: HPSMPOC-301/-302 (11:30 AEDT, overlap with 13:00 and 21:00) and **HPSMPOC-303, -304 new** (22:07:39 and 22:07:42, labels `b346-2026-10-20` / `plan-b346-ta` / `plan-b346-tb`, `[B316 FOUND-3] Hosted zip deploy: the old API process keeps running ...` and `[B337/B346 cleanup candidate] vm-hpsm-sm leftovers ...`, both seat-filed, Backlog); project total **302 -> 304**. 12 comments, all "BLUF:" seat voice: 3 are the 11:31 "merged as datasecau/HPSM-POC#164" (overlap), 9 are 22:05:49-22:05:57 "BLUF: deployed to the hosted demo: main c149a303..., build ao-MW9SSW6F0" on HPSMPOC-263, -267, -268, -275, -290, -293, -298, -299, -300 (-268: "hosted API still runs .NET 10.0.12 after the deploy"). **Summary "feedback" 1 in window** (HPSMPOC-303: a seat finding whose summary contains the word) and **label `feedback` 1 in window** (HPSMPOC-290, created 10-18, Done, label from the b271 gate; touched only by the 22:05:49 deploy comment). Totals: summary 24 -> **25**, label 20 unchanged. Neither is a client submission. GitHub: code repo main `c149a303` and analysis repo main `9af1d55a` unchanged; no open PRs. |
| **HPSM** (HPSM) | 0 | 0 | Jira none (41 unchanged). GitHub **UNMEASURED** (`gh` not logged in under `HPSM/4_Credentials/.gh-config`; every call returned the "gh auth login" prompt, as on 13:00 and 21:00). |

**Actionable items: none.** There are no feedback items to categorise. RD-869..RD-873, MPSCALC-288..305 and HPSMPOC-301..304 are seat-filed from QA / gate findings, not client submissions.

## 2. Method and controls

### Mailbox (tuesday-agent@agentmail.to)
- `GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`, paged by `page_token` to the end, read about 22:36 AEDT: **3,741 messages, 38 pages** (21:00 read: 3,740, so +1); newest **2026-10-20T11:13:55.000Z** (22:13:55 AEDT, about 23 min before read time), oldest 2026-09-08T21:47:13Z. Subjects, senders and timestamps only; no bodies read. No subject named Secuura or another client.
- **2 messages from the watermark on** (the watermark message plus 1): `coagent@` 2 (QA GATE VERDICT gate 32 `[QA/Datasec-NexusAI -> Tuesday]` 09:53:01Z [the watermark]; `[Datasec/MPS Commercial Calculator -> Tuesday] QUESTION: CodeQL not running on PR 89 (B347/G25)` 11:13:55Z). `tuesday-agent@` own 0, `datasec-vision@` 0, `kamilDatasec`/Kam forwards 0, `wednesday-agent@` 0.
- **0 feedback notices, 0 client senders**; no subject in the window contains "feedback".
- **Control 1 (continuity):** the watermark message (09:53:01.000Z) comes back in the same call.
- **Control 2 (instrument fires):** the same read returns **50** subjects containing "feedback" (newest a Kam forward, 2026-10-17T04:56:13Z; same as 21:00) and **1** subject starting `QuickQuote feedback (` (2026-10-09T16:51:40Z). (The 21:00 file also counted a `Fwd:` copy of 2026-09-22T03:38:14Z; this run's prefix test does not match `Fwd:` rows, so 1 here, the same underlying set.)

### Jira (JQL in AEDT; every list paged to the end; read 22:36-22:38)
Instrument: each project's own `4_Credentials/.env` (RD and VSP from the project's own env as the 21:00 run; HPSMPOC from HPSM-POC; MPSCALC from the MPS env; HPSM from HPSM) parsed in-process in `python3 -I`, never printed; `GET /rest/api/3/search/jql` (`maxResults 100`, `nextPageToken`) and `/issue/<key>/comment`; comment times compared with the window edge (Jira returns AEDT offsets). Reporter / labels / summary read for the new RD, MPSCALC and HPSMPOC tickets.

| Project | W | Result | Control |
|---|---|---|---|
| RD | `2026-10-20 19:55` | **7 touched**; 2 created (RD-872, -873; overlap with 21:00) | `project = RD ORDER BY key` = **869** = 21:00's 869 (no new ticket). Prior-window query (`updated >= "2026-10-20 12:45"`) returns **11**, so the query fires. |
| RD | | `summary ~ "feedback"` in window 0 / total 21; `labels in (feedback, user-feedback, hp-feedback)` in window 0 / total 5 | totals unchanged from 21:00 (21, 5) |
| RD comments | | **1**, seat voice (RD-786 20:00:18, "BLUF: gate 30 round 1 found one Major on PR #98 ...") | the same comment the 21:00 sweep ended on |
| VSP | `2026-10-19 19:35` | **0** touched | total 89 unchanged; summary 0 in window / **1** total (instrument matches); label 0 / 0. In-window zero has no in-window positive control (prior-window query is the same window); it rests on the unchanged total and the 1 summary match (same limit as 13:00 and 21:00). |
| HPSM | `2026-10-19 19:35` | **0** touched | total 41 unchanged; summary 0 / 0, label 0 / 0 (HPSM has never had a feedback hit: no project-specific control). |
| HPSMPOC | `2026-10-20 11:30` | **13 touched**: -263, -267, -268, -275, -290, -293, -298, -299, -300, -301, -302, -303, -304; 4 created (-301..-304); 12 comments, all "BLUF:" | total **304** (302 at 21:00 + the 2 created at 22:07). Summary 1 / **25** total, label 1 / **20** total (both in-window hits read above: HPSMPOC-303 and HPSMPOC-290, both seat work). Prior window (`>= "2026-10-19 21:10"`) returns **14**. |
| MPSCALC (*excluded*) | `2026-10-20 20:05` | **47 touched**, 18 created (MPSCALC-288..305, 20:07-20:08 AEDT; overlap with 21:00); 45 comments, all "BLUF:" seat / QA voice | total **305** = 21:00's 305. Summary 0 / **13** total, label 0 / 0 (totals unchanged). Prior window (`>= "2026-10-20 12:40"`) returns **47**. |

**Positive control (same script):** the feedback-labelled rows exist and are matched: RD summary 21 / label 5 total, HPSMPOC summary 25 / label 20 (and 1 / 1 in window), MPSCALC summary 13, VSP summary 1. The window queries fire on RD (7), HPSMPOC (13) and MPSCALC (47).

**Client-human responses in Jira: 0.** The opening of all 58 in-window comments (1 RD, 12 HPSMPOC, 45 MPSCALC) reads as seat / QA voice. The shared "Kamil Kreiser" account cannot separate Kam from a seat.

### GitHub (`gh api` GETs, `since=2026-10-20T09:13:00Z`, read about 22:37-22:38 AEDT; each under its own project's `GH_CONFIG_DIR`)

| Repo | Commits on main since | Issues/PRs updated since | Issue / review comments since | Open PRs | Control: main HEAD |
|---|---|---|---|---|---|
| Reporting_Dashboard_Au (NexusAI) | **1** (`d463f881` 10:09:38Z) | **1**: #98 (merged 11:16:38Z) | 0 / 0 | #97(d), #67 | `d463f881` 10-20T10:09:38Z |
| vision_datasec-sales-portal | 0 | 0 | 0 / 0 | #14-#17 (Dependabot) | `6dbffdf3` 09-28 |
| vision_hpas-quickquote | 0 | 0 | 0 / 0 | #8 | `5fa1187b` 10-18T09:57Z |
| Datasec-Security-Composer | **2** (`eaff2b74` 09:13:29Z [the 21:00 edge, overlap], `308b7aa6` 10:11:07Z) | **3**: #85 (open draft, new, 11:34:38Z), #84 (merged 10:11:08Z), #83 (merged 09:13:30Z, overlap) | 0 / 0 | #85(d) | `308b7aa6` |
| HPSM-POC (*excluded*) | 0 | 0 | 0 / 0 | none | `c149a303` 10-20T00:11:40Z |
| HPSM-POC-analysis (*excluded*) | 0 | 0 | 0 / 0 | none | `9af1d55a` 10-20T00:45:05Z |
| MPS-Commercial-Calculator (*excluded*) | 0 | **2**: #90 (open, new, 11:21:40Z), #89 (open, new, 11:33:48Z) | 0 / 0 | #90, #89 (both non-draft) | `67bf2004` 10-20T03:58:33Z |
| HPSM (*excluded*) | **UNMEASURED** | | | | `gh` not logged in under HPSM's config |

**Controls:** the `since` filter fires on NexusAI, Composer and MPS; on each zero repo (Vision Portal, QuickQuote, HPSM-POC, analysis) the pre-window HEAD is visible under the same credentials. **Comment endpoint control:** issue comments re-run with `since=2026-09-01T00:00:00Z` returns NexusAI 6, QuickQuote 4, Composer 3, HPSM-POC 3, analysis 1, MPS 2, so the endpoint fires (Vision Portal returns 0 total there, so its zero comment count has no positive control); none since the watermark. Review-comment endpoint returns 0 since the watermark on every repo (no in-run positive control this time; the earlier `github-advanced-security[bot]` comments on NexusAI #97 are before the window). Merged flags read from `pulls/<n>`: #98 (NexusAI) and #84 (Composer) `merged: true`; Composer #85 `merged: false` draft; MPS #89, #90 `merged: false`. No non-PR GitHub issue opened anywhere. All authors `kamilDatasec` (the shared account; seat PRs).

## 3. Window edges and watermarks out

Window: opened per the quoted watermarks above; closed at the last read **22:38:30 AEDT (11:38:30Z)**. Read span 22:36:24-22:38:30 AEDT (11:36:24-11:38:30Z). Edges, AEDT / UTC:

- **Mailbox:** 2026-10-20T11:13:55.000Z (22:13:55 AEDT; MPS Commercial Calculator QUESTION on PR 89, the newest message read). Next run: at or after **2026-10-20T11:13:55.000Z**.
- **Jira:** newest processed change RD-786 comment **2026-10-20 20:00:18 AEDT** (no RD change since); next run RD `>= "2026-10-20 19:55"` (08:55Z), unchanged. HPSMPOC newest update **22:07:42 AEDT** (HPSMPOC-304 created); next `>= "2026-10-20 22:05"` (11:05Z). MPSCALC (excluded) newest update **22:19:15 AEDT**; next `>= "2026-10-20 22:15"` (11:15Z). VSP and HPSM: unchanged, keep `>= "2026-10-19 19:35"`.
- **GitHub:** newest item read: Composer #85 created/updated **2026-10-20T11:34:38Z** (22:34:38 AEDT). Next run `since=2026-10-20T11:34:00Z`. HPSM not measured, no edge advanced for it.

## 4. UNMEASURED
- **Every live feedback store:** MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, the NexusAI share `feedbackItems`, Portal Postgres, the QuickQuote table. Each needs az, a writing sign-in or HTTP to a hosted host, all out of bounds. **"0 new" means only that nothing reached the mailbox, Jira or GitHub.**
- **Who wrote a Jira comment:** the shared account cannot tell Kam from a seat; only openings (about 100 characters) were read.
- **HPSM GitHub:** `gh` not logged in under HPSM's config.
- **Mail bodies** not read; `coagent@` bus and other inboxes not read (the `coagent@` rows are copies that reached `tuesday-agent@`). The MPS QUESTION on PR 89 (CodeQL not running, B347/G25) is a seat-to-Tuesday question, listed by subject only.
- **Vision Portal comment endpoint** has no positive control (0 comments total since 09-01); the GitHub review-comment endpoint had no in-run positive control.
- **Kam's card board** not re-read.
- **Part 2** (ticket sweep) not in scope for this run.
- No HTTP to any app host, hosted site or production (only the AgentMail API, Jira Cloud search and comment reads, and `api.github.com`); no az, docker or ssh; no git commands in project repos; no Jira, gh, mail or card writes. Temporary scripts lived in the session scratchpad.

## OUTBOUND watermarks for the next sweep

- Mailbox: at or after **2026-10-20T11:13:55.000Z**.
- Jira: RD `>= "2026-10-20 19:55"`; HPSMPOC `>= "2026-10-20 22:05"`; MPSCALC (excluded) `>= "2026-10-20 22:15"`; VSP and HPSM `>= "2026-10-19 19:35"` (all AEDT).
- GitHub: `since=2026-10-20T11:34:00Z`.
