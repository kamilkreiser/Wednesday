# Rotation sweep: Datasec feedback delta, Job A only (2026-10-19, 20:30)

A read-only sub-agent (claude-sonnet-5-5) ran this for Tuesday. Clock from the shell: `date` = **Mon 19 Oct 2026 20:32:40 AEDT** at first start; the successful run and the control reads finished 20:36 AEDT (= 09:36Z).

Method, instruments, controls and table shape copied from [[2026-10-19_rotation-sweep-1545]]. Window edges taken from that file's section 3 (its own stated watermarks), not assumed:

- Mailbox: after **2026-10-19T03:51:00.9Z** (about 5 h 45 min to read time).
- Jira: `>= "2026-10-19 15:30"` AEDT (about 5 h 05 min).
- GitHub: `since=2026-10-19T04:34:00Z` (about 5 h 00 min).

## 1. BLUF

**New feedback items: 0 across all projects. New client-human responses: 0. No ticket needed.** The window is fleet work: NexusAI-O readied PR #97 (RD-774 + RD-836, head 4c9b0d3), gate 28 went GO, PR #92 (RD-856) merged, and the seat filed RD-862 to RD-867; HPSM-POC PRs #161, #162, #163 merged; Composer opened draft PR #81; Tuesday and Wednesday exchanged ANSWER-24/25/26 and laptop-drive mail.

| Project | New feedback items | Client-human responses | Other activity in window (not feedback) |
|---|---|---|---|
| **NexusAI** (RD) | **0** | **0** | 11 issues touched, **6 created** (RD-862 16:27, RD-863/-864/-865/-866 16:56, RD-867 17:46; all seat-filed, labels hygiene/tech-debt, ai-assistant/test-gap/user-facing, flaky-test/test-infra; `project = RD` 857 -> **863**). RD-836, RD-774 touched 16:25-16:27 (READY FOR QA comments, both seat voice); RD-857 and RD-476 stay In Progress; RD-338 -> **Release Ready** (17:46). Comments in window: 2 (RD-836, RD-774, both 16:25). GitHub: main moved `7700cafd` -> **`ac0f4773`** (1 commit, 08:29Z, forward merge of main into the RD-856 branch); **PR #92 merged** 09:14:44Z (RD-856); PR #97 still open draft (updated 04:32:45Z, no change); 0 issue comments, 0 review comments. |
| **Vision Portal** (VSP) | **0** | **0** | Jira none. GitHub none (main `6dbffdf3`, 4 Dependabot PRs unchanged). |
| **Vision QuickQuote** | **0** (no `QuickQuote feedback (` mail) | **0** | None. GitHub main still `5fa1187b`, PR #8 open, nothing new. |
| **Security Composer** | **0** | **0** | GitHub: no commit on main (still `50d97508`); **PR #81 opened** (draft, "B281-1: timing tests reliable under load", `kamilDatasec`, updated 08:01:39Z). Not feedback. |
| **MPS Calculator** (MPSCALC, *excluded*) | 0 seen | **0** | None. Jira 231 unchanged; GitHub main `21c2aec7`. |
| **HPSM-POC** (HPSMPOC, *excluded*) | 0 submissions seen | **0** | Jira: 7 tickets touched 15:35-19:38 AEDT, **1 created** (HPSMPOC-293, 19:13, seat-filed B288, no labels; 292 -> **293**), 7 comments, all "BLUF: ..." seat voice. Label hits in window 2 (HPSMPOC-226, HPSMPOC-290) and summary hit 1 (HPSMPOC-226 "Feedback attachments follow-ups N-1..N-9"): these are seat follow-up work tickets on already-built feedback attachments, touched by seat BLUF comments, not new submissions. HPSMPOC-267 carries `needs-kam` (already existing, seat comment at 19:37). GitHub: **PRs #161, #162, #163 merged** (08:10Z, 06:47Z, 09:29Z); main `befd45e7` -> **`b3a7c275`** (3 commits); HPSM-POC-analysis `47a9896e` unchanged; no open PRs. |
| **HPSM** (HPSM) | **0** | **0** | Jira none (41 unchanged). GitHub **UNMEASURED** (`gh` not logged in under `HPSM/4_Credentials/.gh-config`). |

**Item needing a ticket: none.** There are no feedback items to categorise. (RD-862 to RD-867 and HPSMPOC-293 already exist and are seat-filed.)

## 2. Method and controls

### Mailbox (tuesday-agent@agentmail.to)
- `GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`, paged by `next_page_token` to the end (3,713 messages returned this run; newest **2026-10-19T07:42:56Z**, oldest 2026-09-08T21:47:13Z; the count is larger than the previous file's 1,400 because the pagination here ran to the end with no cut-off, the newest-edge behaviour is unchanged). Subjects, senders and timestamps only; no bodies read (the API `preview` field was not read either).
- **13 messages from the watermark on** (the watermark message itself plus 12 new):
  - `tuesday-agent@` x6 (to fleet or Wednesday): ANSWER-23 (03:51Z, the watermark), ANSWER-24 (05:26Z), ANSWER-25 (05:54Z), ANSWER-26 (06:00Z), and 3 laptop-drive mails to `wednesday-agent@` (07:24Z, 07:37Z, 07:41Z).
  - `coagent@` x3: NexusAI-O READY FOR QA PR #97 (05:25Z); NexusAI-O RD-862 filed (05:27Z); QA gate 28 GATE VERDICT (05:51Z).
  - `wednesday-agent@` x3: laptop-drive replies (07:35Z, 07:39Z, 07:42Z).
  - `datasec-vision@` x0; `kamil.kreiser@datasec.com.au` x0.
- **0 feedback notices, 0 client senders** in the window.
- **Control 1 (continuity):** the watermark message (ANSWER-23, 03:51:00.924Z) comes back in the same call, so the window edge is seen. Newest message is about 1 h 54 min before read time.
- **Control 2 (instrument fires on a feedback notice and an outside sender):** the same read returns `QuickQuote feedback (feature) from john.spears@datasec.com.au` (HPAM Quoting Agent, 2026-10-09T16:51:40Z, newest of its kind); 50 subjects overall contain "feedback", newest a Kam forward from `kamil.kreiser@datasec.com.au` at 2026-10-17T04:56:13Z.

### Jira (JQL in AEDT; W = `"2026-10-19 15:30"`; paged to `isLast`; read about 20:33)

| Project | JQL | Result | Control |
|---|---|---|---|
| RD | `project = RD AND (created >= W OR updated >= W)` | **11**: RD-836, RD-774, RD-862, RD-863, RD-857, RD-864, RD-865, RD-476, RD-866, RD-338, RD-867 | Query fires (11 rows). Total 857 -> 863; the +6 are exactly RD-862 to RD-867 created in window. |
| RD | `summary ~ "feedback"` in window / total | **0** / 21 | Total unchanged (21). |
| RD | `labels in (feedback, user-feedback, hp-feedback)` in window / total | **0** / 5 | Total unchanged (5). |
| RD comments | `/issue/<key>/comment`, created at or after W on the 11 issues (converted to AEDT) | 2: RD-836 16:25:48, RD-774 16:25:47 | Both seat voice ("READY FOR QA (S101O) ..."). |
| VSP | window query | **0** | `project = VSP` 89 unchanged. Feedback summary 0 / 1; label 0 / 0. |
| HPSM | window query | **0** | `project = HPSM` 41 unchanged. Feedback summary 0 / 0; label 0 / 0. |
| HPSMPOC | window query | **7** (-291, -226, -290, -267, -293, -275, -263) | Fires. Total 292 -> 293 (+1 = HPSMPOC-293 created 19:13). Summary "feedback" in window 1 / 23 (-226); label 2 / 19 (-226, -290). |
| HPSMPOC comments | same method | 7: -291 15:35:21, -226 16:42:33, -290 16:42:28, -267 19:37:58, -293 19:37:58, -275 19:37:59, -263 19:38:00 | All "BLUF: ..." seat voice. |
| MPSCALC | window query | **0** | `project = MPSCALC` 231 unchanged. Feedback summary 0 / 13; label 0 / 0. |

**Positive control (same script, prior window).** Re-running the identical query shapes with W = `"2026-10-18 21:15"` (the 06:00 sweep's window) returned HPSMPOC **31** updated, feedback-summary **5**, feedback-label **8** (the 1545 file's same control, run at that time, gave 26 / 5 / 7; the counts grew because seats edited more tickets since, including -290 and -226 today), and RD **21** updated. So the instrument sees feedback-labelled rows when any exist in a window. The two HPSMPOC label hits in the 15:30 window are accounted for above as seat-touched follow-up tickets, not submissions. VSP, MPSCALC and HPSM zeros rest on that same instrument plus unchanged totals; HPSM has never had a feedback-summary or label hit, so it has no project-specific positive control.

**Client-human responses in Jira:** 0. I read the opening (about 130 characters) of all 9 comments in window (2 RD, 7 HPSMPOC). All read as seat voice. The shared "Kamil Kreiser" account cannot separate Kam from a seat (see Not done).

### GitHub (`gh api` GETs, `since=2026-10-19T04:34:00Z`, read about 20:35 AEDT, each under its own `GH_CONFIG_DIR`)

| Repo | Commits on main since | Issues and PRs updated since | Issue / review comments since | Open PRs | Control: main HEAD |
|---|---|---|---|---|---|
| Reporting_Dashboard_Au (NexusAI) | **1** (`ac0f4773`, 08:29Z, merge of main 7700caf into the RD-856 branch) | **1**: #92 (merged 09:14:44Z, RD-856) | 0 / 0 | #97 (draft), #96, #93(d), #91(d), #67 | `ac0f4773` 10-19T08:29Z |
| vision_datasec-sales-portal | 0 | 0 | 0 / 0 | #17 #16 #15 #14 (Dependabot) | `6dbffdf3` 09-28 |
| vision_hpas-quickquote | 0 | 0 | 0 / 0 | #8 | `5fa1187b` 10-18T09:57Z |
| Datasec-Security-Composer | 0 | **1**: #81 (open draft, 08:01:39Z, B281-1) | 0 / 0 | #81 (draft) | `50d97508` 10-19T03:43Z |
| HPSM-POC (*excluded*) | **3** (`b3a7c275` 09:29Z, `2a0c5412` 08:10Z, `e4f270ea` 06:47Z) | **3**: #163, #162, #161 (all merged) | 0 / 0 | none | `b3a7c275` 10-19T09:29Z |
| HPSM-POC-analysis (*excluded*) | 0 | 0 | 0 / 0 | none | `47a9896e` 10-18T12:57Z |
| MPS-Commercial-Calculator (*excluded*) | 0 | 0 | 0 / 0 | none | `21c2aec7` 10-17 |
| HPSM (*excluded*) | **UNMEASURED** | **UNMEASURED** | **UNMEASURED** | **UNMEASURED** | `gh` not logged in under HPSM's config |

**Control:** the `since` filter fires on NexusAI, Composer and HPSM-POC, so it works under those configs; on each zero repo the pre-window HEAD is visible under the same credentials. **Comment zeros:** the window has no issue or review comments anywhere, so the same instrument was re-run on NexusAI with `since=2026-10-19T00:00:00Z`, and it returned the `github-advanced-security[bot]` review comment on PR #97 (01:42:56Z), proving the review-comment endpoint fires under that config. The merged flags for #92, #161, #162, #163 were read from `pulls/<n>` (all `merged: true`). No GitHub issue (non-PR) was opened anywhere. All PR authors are `kamilDatasec` (the shared account; seat PRs).

## 3. Watermarks out
- **Mailbox:** 2026-10-19T07:42:56Z (`wednesday-agent@` laptop-drive reply, the newest message read).
- **Jira:** newest processed change is **HPSMPOC-263 comment 2026-10-19 19:38:00** AEDT (RD: RD-338 / RD-867 at 17:46:43). Next run `>= "2026-10-19 19:35"` (small overlap, since seats are active on HPSMPOC b288 and NexusAI).
- **GitHub:** `since=2026-10-19T09:29:00Z` (newest item read: HPSM-POC #163 updated 09:29:57Z and commit `b3a7c275` 09:29:56Z; NexusAI #92 09:14:44Z, Composer #81 08:01:39Z are older and already counted here).

## 4. Not done
- **Every live feedback store is UNMEASURED:** MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, the NexusAI share `feedbackItems`, Portal Postgres, the QuickQuote table. Each needs az, a writing sign-in, or HTTP to a hosted host, all out of bounds. **"0 new" means only that nothing reached the mailbox, Jira or GitHub.**
- **Who wrote a Jira comment:** the shared "Kamil Kreiser" account cannot tell Kam from a seat. Openings only were read.
- **HPSM GitHub:** `gh` not logged in under HPSM's config.
- **Mail bodies** not read (subjects, senders, timestamps only). Mail to other inboxes not read; `coagent@` bus not read at all (the `coagent@` rows above are copies that reached `tuesday-agent@`). Between the mailbox watermark (07:42Z) and read time (09:36Z) nothing newer existed in the list.
- **Kam's card board** not re-read, so any ruling made after the 15:45 sweep is not reflected.
- **First run of this sweep** timed out in a GitHub history call (a script bug in the HEAD lookup, fixed by not paginating that one call) before writing results; the second, complete run is the one reported. No data was written anywhere by either.
- **Job B** (ticket sweep) not in scope for this run.
- No HTTP to any app host, hosted site or production (only the AgentMail API, Jira Cloud search, and `api.github.com`); no az or docker; no git write verbs; no Jira, gh, mail or card writes.
