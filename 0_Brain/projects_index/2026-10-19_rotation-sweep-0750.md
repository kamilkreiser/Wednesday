# Rotation sweep: Datasec feedback delta, Job A only (2026-10-19, 07:50)

A read-only sub-agent (claude-sonnet-5-5) ran this for Tuesday from **07:50 to about 07:55 AEDT on 2026-10-19** (`date`: Mon 19 Oct 2026 07:50:24 AEDT = 20:50Z at start; GitHub read at 07:51:13).

Method, instruments, controls and table shape copied from [[2026-10-19_morning-sweep-0600]] (Job A). Window edges taken from that file's section 4 (its own stated watermarks), not assumed:

- Mailbox: after **2026-10-18T18:25:13Z** (about 2 h 25 min to 20:50Z).
- Jira: `>= "2026-10-19 04:45"` AEDT (about 3 h 05 min).
- GitHub: `since=2026-10-18T17:49:00Z` (about 3 h 01 min).

## 1. BLUF

**New feedback items: 0 across all projects. New client-human responses: 0.** Everything in the window was fleet work: NexusAI-O finished the C-170 delta (PR #96 head `f15217c`, READY FOR QA, gate 28), filed RD-858 and RD-859, and began RD-774/RD-836; Vision published QuickQuote v2.39.

| Project | New feedback items | Client-human responses | Other activity in window (not feedback) |
|---|---|---|---|
| **NexusAI** (RD) | **0** | **0** | 5 issues touched, **2 created** (RD-858, RD-859, both 07:17, seat-filed security tickets, not feedback; `project = RD` 853 -> **855**). RD-774 and RD-836 moved To Do -> **In Progress** (07:17). RD-460 -> **Testing** (07:15, "BLUF: READY FOR QA: C-170 delta", head `f15217cb`). 3 new comments at 07:15 (RD-460, RD-774, RD-836), all seat voice. Also the 04:50 RD-460 STOP comment re-appears (04:45 overlap by design). GitHub: **main unchanged at `888203c8`**; PR #96 updated 19:19Z (the delta push); no new commits on main. |
| **Vision Portal** (VSP) | **0** | **0** | Jira none. GitHub none (main `6dbffdf3`, 4 Dependabot PRs unchanged). |
| **Vision QuickQuote** | **0** (no `QuickQuote feedback (` mail) | **0** | Mail: `datasec-vision` seat sent "B275 STATUS: PUBLISHED QuickQuote v2.39 (v0.6.6-tool2.39-5fa1187)" at 20:28:06Z (07:28 AEDT). GitHub: main still `5fa1187b`, PR #8 still open, last updated 10-16, no repo activity since. |
| **Security Composer** | **0** | **0** | None. GitHub main still `230f9fab`. |
| **MPS Calculator** (MPSCALC, *excluded*) | 0 seen | **0** | None. Jira 231 unchanged; GitHub main `21c2aec7`. |
| **HPSM-POC** (HPSMPOC, *excluded*) | 0 submissions seen | **0** | None in Jira (292 unchanged) or GitHub (HPSM-POC `befd45e7`, HPSM-POC-analysis `47a9896e`, no PRs open). |
| **HPSM** (HPSM) | **0** | **0** | Jira none (41 unchanged). GitHub **UNMEASURED** (`gh` not logged in under `HPSM/4_Credentials/.gh-config`). |

**Item needing a ticket: none.** There are no feedback items to categorise. (RD-858 and RD-859 already exist and are seat-filed.)

## 2. Method and controls

### Mailbox (tuesday-agent@agentmail.to)
- `GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`, paged 12 times (1,200 messages; newest **2026-10-18T20:28:06Z**, oldest 2026-09-28T21:42:42Z). Subjects, senders and timestamps only; no bodies read.
- **5 messages after the watermark** (plus the watermark itself):
  - `tuesday-agent@` x2: ANSWER-20 (19:06Z, RD-774 + RD-836 next build) and ANSWER-21 (20:16Z, plan confirmation RD-774/836 CONFIRMED).
  - `coagent@` x2: NexusAI-O READY FOR QA C-170 delta (20:15Z, f15217c on PR #96, holding for gate 28) and QUESTION plan confirmation RD-774/836 (20:15Z).
  - `datasec-vision@` x1: B275 STATUS PUBLISHED QuickQuote v2.39 (20:28Z).
  - `wednesday-agent@` x0.
- **0 feedback notices, 0 senders outside the fleet** in the window.
- **Control 1 (continuity):** the watermark message (Tuesday's ANSWER-1 to QA/NexusAI-gate27, 18:25:13Z) comes back in the same call, so the window edge is seen. Newest message is 22 min before read time; nothing is missing at the tail that the list could show.
- **Control 2 (instrument fires on a feedback notice and an outside sender):** the same read returns `QuickQuote feedback (feature) from john.spears@datasec.com.au` (HPAM Quoting Agent, 2026-10-09T16:51:40Z) and Kam's forwards from `kamil.kreiser@datasec.com.au` (newest 2026-10-17T04:56:13Z).

### Jira (JQL in AEDT; W = `"2026-10-19 04:45"`; paged to `isLast`; read 07:50)

| Project | JQL | Result | Control |
|---|---|---|---|
| RD | `project = RD AND (created >= W OR updated >= W)` | **5**: RD-859 (c 07:17), RD-858 (c 07:17), RD-836 (u 07:17), RD-774 (u 07:17), RD-460 (u 07:15) | Query fires (5 rows). Totals 853 -> 855, and the +2 are exactly the two created in window. |
| RD | `summary ~ "feedback"` in window / total | **0** / 21 | Total unchanged (21). |
| RD | `labels in (feedback, user-feedback, hp-feedback)` in window / total | **0** / 5 | Total unchanged (5). |
| RD comments | `/issue/<key>/comment`, created on 2026-10-19 | 4: RD-836 07:15:32, RD-774 07:15:30, RD-460 07:15:22 (all seat "Context: ANSWER-20 ..." / "BLUF: READY FOR QA ..."), and RD-460 04:50:57 (the prior sweep's last watermark item, overlap) | 3 new, all seat voice. |
| VSP | window query | **0** | `project = VSP` 89 unchanged. Feedback summary 0 / 1; label 0 / 0. |
| HPSM | window query | **0** | `project = HPSM` 41 unchanged. Feedback summary 0 / 0; label 0 / 0. |
| HPSMPOC | window query | **0** | `project = HPSMPOC` 292 unchanged. Feedback summary 0 / 23; label 0 / 19. |
| MPSCALC | window query | **0** | `project = MPSCALC` 231 unchanged. Feedback summary 0 / 13; label 0 / 0. |

**Positive control (same query shapes, prior window).** Re-running the identical script with W = `"2026-10-18 21:15"` (the 06:00 sweep's window) returned RD **10** (fires; includes today's 5), HPSMPOC **17** updated with feedback-summary **3** (-281, -282, -288) and feedback-label **7** (-281, -284, -285, -286, -288, -289, -290). These match the 06:00 file exactly, so the instrument, JQL and label handling are the ones that file used, and they see feedback-labelled rows when any are in the window. The zeros for VSP, HPSM, HPSMPOC and MPSCALC are therefore real zeros for this window, not instrument failure.

**Client-human responses in Jira:** 0. I read the opening (about 140 characters) of all 4 comments dated today. All read as seat voice (the shared "Kamil Kreiser" account cannot separate Kam from a seat; see Not done).

### GitHub (`gh api` GETs, `since=2026-10-18T17:49:00Z`, read 07:51 AEDT, each under its own `GH_CONFIG_DIR`)

| Repo | Commits on main since | Issues and PRs updated since | Issue / review comments since | Open PRs | Control: main HEAD |
|---|---|---|---|---|---|
| Reporting_Dashboard_Au (NexusAI) | **0** | **1**: #96 (open, C-170/RD-460, updated 19:19:48Z) | 0 / **6** (all `github-advanced-security[bot]` on #96 at 17:49:13Z, the same six the 06:00 sweep counted; they sit on the window edge) | #96, #94(d), #93(d), #92(d), #91(d), #67 | `888203c8` 10-18T14:25Z |
| vision_datasec-sales-portal | 0 | 0 | 0 / 0 | #17 #16 #15 #14 (Dependabot) | `6dbffdf3` 09-28 |
| vision_hpas-quickquote | 0 | 0 | 0 / 0 | #8 | `5fa1187b` 10-18T09:57Z |
| Datasec-Security-Composer | 0 | 0 | 0 / 0 | none | `230f9fab` 10-16 |
| HPSM-POC (*excluded*) | 0 | 0 | 0 / 0 | none | `befd45e7` 10-18T11:05Z |
| HPSM-POC-analysis (*excluded*) | 0 | 0 | 0 / 0 | none | `47a9896e` 10-18T12:57Z |
| MPS-Commercial-Calculator (*excluded*) | 0 | 0 | 0 / 0 | none | `21c2aec7` 10-17 |

**Control:** the `since` filter fires on NexusAI (PR #96 and the six bot review comments), so it works under that config; on each zero repo the pre-window HEAD is visible under the same credentials. No GitHub issue was opened anywhere and there are no issue comments anywhere. PR #96's update is a push to the branch (head `f15217c` per the mail and the RD-460 comment), not a commit to main.

## 3. Watermarks out
- **Mailbox:** 2026-10-18T20:28:06Z (`datasec-vision` B275 STATUS, the newest message read).
- **Jira:** newest processed change is **RD-858 / RD-859 created 2026-10-19 07:17** AEDT. Next run `>= "2026-10-19 07:15"` (small overlap, because NexusAI-O is active on RD-460/-774/-836).
- **GitHub:** `since=2026-10-18T19:19:00Z` (newest item read: PR #96 updated 19:19:48Z; the bot comments at 17:49:13Z are older).

## 4. Not done
- **Every live feedback store is UNMEASURED:** MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, the NexusAI share `feedbackItems`, Portal Postgres, the QuickQuote table. Each needs az, a writing sign-in, or HTTP to a hosted host, all out of bounds. **"0 new" means only that nothing reached the mailbox, Jira or GitHub.**
- **Who wrote a Jira comment:** the shared "Kamil Kreiser" account cannot tell Kam from a seat. Openings only were read.
- **HPSM GitHub:** `gh` not logged in under HPSM's config.
- **Mail bodies** not read (subjects, senders, timestamps only). Mail to other inboxes not read; `coagent@` bus not read at all.
- **Kam's card board** not re-read, so any ruling made after the 06:00 sweep is not reflected.
- **Job B** (ticket sweep) not in scope for this run.
- No HTTP to any app host, hosted site or production; no az or docker; no git write verbs; no Jira, gh, mail or card writes.
