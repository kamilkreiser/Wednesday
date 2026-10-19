# Rotation sweep: Datasec feedback delta, Job A only (2026-10-19, 15:45)

A read-only sub-agent (claude-sonnet-5-5) ran this for Tuesday. Clock from the shell: `date` = **Mon 19 Oct 2026 15:43:08 AEDT** at start; mailbox, Jira and GitHub reads ran 15:43 to 15:44 AEDT (= 04:43Z to 04:44Z).

Method, instruments, controls and table shape copied from [[2026-10-19_rotation-sweep-0750]]. Window edges taken from that file's section 3 (its own stated watermarks), not assumed:

- Mailbox: after **2026-10-18T20:28:06Z** (about 8 h 15 min to read time).
- Jira: `>= "2026-10-19 07:15"` AEDT (about 8 h 30 min).
- GitHub: `since=2026-10-18T19:19:00Z` (about 9 h 25 min).

(That file calls its watermarks "section 3"; the task's "section 4" is this file's section 3 below.)

## 1. BLUF

**New feedback items: 0 across all projects. New client-human responses: 0.** The window is fleet work: NexusAI merged RD-778 (PR #94, main `7700caf`), filed RD-860 and RD-861, opened PR #97 (RD-774 + RD-836); Composer merged PR #80; HPSM-POC opened PR #161 and the seat closed or commented 10 HPSMPOC tickets; Tuesday answered ANSWER-22 and ANSWER-23.

| Project | New feedback items | Client-human responses | Other activity in window (not feedback) |
|---|---|---|---|
| **NexusAI** (RD) | **0** | **0** | 9 issues touched, **2 created** (RD-860, RD-861, both 11:58, seat-filed RD-778 residue, labels security/xss/codeql-baseline/test-gap; `project = RD` 855 -> **857**). RD-778 -> **Testing** (11:59, "MERGED to main", PR #94). RD-771 re-pinned (11:58). RD-774/RD-836/RD-460 touched 07:15-07:17 (the prior window's tail, overlap). 5 comments in window, all seat voice (RD-836, RD-774, RD-460 at 07:15; RD-778 11:58; RD-771 11:58). GitHub: main moved `888203c8` -> **`7700cafd`** (1 commit, the RD-778 forward-merge, 10-18T23:00Z); PR #94 merged; **PR #97 opened** 01:39Z (RD-774 + RD-836, by `kamilDatasec`, open); PR #96 unchanged since 19:19Z; 1 new review comment, `github-advanced-security[bot]` 01:42Z. |
| **Vision Portal** (VSP) | **0** | **0** | Jira none. GitHub none (main `6dbffdf3`, 4 Dependabot PRs unchanged). |
| **Vision QuickQuote** | **0** (no `QuickQuote feedback (` mail) | **0** | Mail: `datasec-vision` B275 STATUS PUBLISHED QuickQuote v2.39, 20:28:06Z (the previous watermark, re-seen). GitHub: main still `5fa1187b`, PR #8 open, nothing new. |
| **Security Composer** | **0** | **0** | GitHub: 1 commit on main, **`50d97508`** 03:43Z ("Composer: objects image as a compose variable; CI uses Chainguard MinIO by digest (B280, #80)"); PR #80 merged by `kamilDatasec`. Main `230f9fab` -> `50d97508`. Not feedback. |
| **MPS Calculator** (MPSCALC, *excluded*) | 0 seen | **0** | None. Jira 231 unchanged; GitHub main `21c2aec7`. |
| **HPSM-POC** (HPSMPOC, *excluded*) | 0 submissions seen | **0** | Jira: 10 tickets touched 12:22-15:35 AEDT, none created (292 unchanged), 11 seat comments, all "BLUF: ..." seat voice. One summary hit for "feedback": HPSMPOC-98 "Admin screen for the feedback list" (a feature ticket, now Done, seat-closed 12:27; not a feedback item). Label hits 0. GitHub: **PR #161 opened** 01:44Z ("HPSMPOC-291, HPSMPOC-227: test-only fixes (B276)", `kamilDatasec`); HPSM-POC main `befd45e7` and HPSM-POC-analysis `47a9896e` unchanged. |
| **HPSM** (HPSM) | **0** | **0** | Jira none (41 unchanged). GitHub **UNMEASURED** (`gh` not logged in under `HPSM/4_Credentials/.gh-config`). |

**Item needing a ticket: none.** There are no feedback items to categorise. (Not a ticket matter, for Tuesday's awareness only: PR #97 carries the CodeQL alert #272 that ANSWER-23 already names.)

## 2. Method and controls

### Mailbox (tuesday-agent@agentmail.to)
- `GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`, paged to the end (1,400 messages; newest **2026-10-19T03:51:00.9Z**, oldest 2026-09-27T12:16:36Z). Subjects, senders and timestamps only; no bodies read.
- **7 messages from the watermark on** (the watermark message itself plus 6 new):
  - `datasec-vision@` B275 STATUS PUBLISHED QuickQuote v2.39 (20:28:06Z, the watermark).
  - `coagent@` x2: QA gate 27 GATE VERDICT (21:15Z); NexusAI-O MERGED RD-778 PR #94 (00:59Z).
  - `tuesday-agent@` x2: ANSWER-22 (21:17Z, RD-778 release) and ANSWER-23 (03:51Z, PR #97 CodeQL alert #272).
  - `kamil.kreiser@datasec.com.au` x2: two GitHub notification forwards (03:49Z, PRs #97 and #96). Kam's forwards of repo notifications, not client feedback.
  - `wednesday-agent@` x0.
- **0 feedback notices, 0 client senders** in the window.
- **Control 1 (continuity):** the watermark message (`datasec-vision` B275 STATUS, 20:28:06Z) comes back in the same call, so the window edge is seen. Newest message is 53 min before read time.
- **Control 2 (instrument fires on a feedback notice and an outside sender):** the same read returns `QuickQuote feedback (feature) from john.spears@datasec.com.au` (HPAM Quoting Agent, 2026-10-09T16:51:40Z); 9 subjects overall contain "feedback". Kam's `@datasec.com.au` forwards are seen as the outside-fleet sender class.

### Jira (JQL in AEDT; W = `"2026-10-19 07:15"`; paged to `isLast`; read 15:43)

| Project | JQL | Result | Control |
|---|---|---|---|
| RD | `project = RD AND (created >= W OR updated >= W)` | **9**: RD-861, RD-860 (c 11:58), RD-859, RD-858 (c 07:17), RD-836, RD-778, RD-774, RD-771, RD-460 | Query fires (9 rows). Totals 855 -> 857; the +2 are exactly the two created in window. |
| RD | `summary ~ "feedback"` in window / total | **0** / 21 | Total unchanged (21). |
| RD | `labels in (feedback, user-feedback, hp-feedback)` in window / total | **0** / 5 | Total unchanged (5). |
| RD comments | `/issue/<key>/comment`, created at or after W on the 9 issues | 5: RD-836 07:15, RD-774 07:15, RD-460 07:15, RD-778 11:58, RD-771 11:58 | 2 new beyond the 07:50 sweep's four; all read as seat voice. |
| VSP | window query | **0** | `project = VSP` 89 unchanged. Feedback summary 0 / 1; label 0 / 0. |
| HPSM | window query | **0** | `project = HPSM` 41 unchanged. Feedback summary 0 / 0; label 0 / 0. |
| HPSMPOC | window query | **10** (-291, -271, -246, -245, -227, -174, -171, -148, -98, -13) | Fires. Total 292 unchanged. Summary "feedback" 1 / 23 (-98, a feature ticket); label 0 / 19. |
| MPSCALC | window query | **0** | `project = MPSCALC` 231 unchanged. Feedback summary 0 / 13; label 0 / 0. |

**Positive control (same script, prior window).** Re-running the identical query shapes on HPSMPOC with W = `"2026-10-18 21:15"` (the 06:00 sweep's window) returned **26** updated, with feedback-summary **5** (-290, -288, -282, -281, -98) and feedback-label **7** (-281, -284, -285, -286, -288, -289, -290). The label set matches the 06:00 file exactly; the summary set is the 06:00 file's three plus -290 and -98 (the window now runs to 15:43, so it catches later seat edits). So the instrument sees feedback-labelled rows when any exist in a window, and the zero label count for 07:15 onward is a real zero. RD fires with 9 rows. VSP, MPSCALC and HPSM zeros rest on that same instrument plus unchanged totals; HPSM has never had a feedback-summary or label hit, so it has no project-specific positive control.

**Client-human responses in Jira:** 0. I read the opening (about 110-140 characters) of the 16 comments in window (5 RD, 11 HPSMPOC). All read as seat voice ("BLUF: ...", "Context: ...", "MERGED ..."). The shared "Kamil Kreiser" account cannot separate Kam from a seat (see Not done).

### GitHub (`gh api` GETs, `since=2026-10-18T19:19:00Z`, read 15:44 AEDT, each under its own `GH_CONFIG_DIR`)

| Repo | Commits on main since | Issues and PRs updated since | Issue / review comments since | Open PRs | Control: main HEAD |
|---|---|---|---|---|---|
| Reporting_Dashboard_Au (NexusAI) | **1** (`7700cafd`, RD-778 forward-merge) | **3**: #97 (open, 04:32Z), #96 (open, 19:19:48Z), #94 (merged, 23:58Z) | 0 / **1** (`github-advanced-security[bot]`, 01:42Z) | #97, #96, #93(d), #92(d), #91(d), #67 | `7700cafd` 10-18T23:00Z |
| vision_datasec-sales-portal | 0 | 0 | 0 / 0 | #17 #16 #15 #14 (Dependabot) | `6dbffdf3` 09-28 |
| vision_hpas-quickquote | 0 | 0 | 0 / 0 | #8 | `5fa1187b` 10-18T09:57Z |
| Datasec-Security-Composer | **1** (`50d97508`, B280) | **1**: #80 (merged 03:43Z) | 0 / 0 | none | `50d97508` 10-19T03:43Z |
| HPSM-POC (*excluded*) | 0 | **1**: #161 (open, 04:34Z, B276 test-only) | 0 / 0 | #161 | `befd45e7` 10-18T11:05Z |
| HPSM-POC-analysis (*excluded*) | 0 | 0 | 0 / 0 | none | `47a9896e` 10-18T12:57Z |
| MPS-Commercial-Calculator (*excluded*) | 0 | 0 | 0 / 0 | none | `21c2aec7` 10-17 |

**Control:** the `since` filter fires on NexusAI, Composer and HPSM-POC, so it works under those configs; on each zero repo the pre-window HEAD is visible under the same credentials. No GitHub issue (non-PR) was opened anywhere, and there are no issue comments anywhere. All PR authors are `kamilDatasec` (the shared account; seat PRs). The only commenter in window is the code-scanning bot.

## 3. Watermarks out
- **Mailbox:** 2026-10-19T03:51:00.9Z (`tuesday-agent@` ANSWER-23, the newest message read).
- **Jira:** newest processed change is **HPSMPOC-291 comment 2026-10-19 15:35** AEDT (RD: RD-778/-771/-860/-861 at 11:58-11:59). Next run `>= "2026-10-19 15:30"` (overlap, since seats are active on HPSMPOC-291 and NexusAI).
- **GitHub:** `since=2026-10-19T04:34:00Z` (newest item read: HPSM-POC #161 updated 04:34:13Z; PR #97 04:32:45Z). Composer #80 (03:43Z) and the bot comment (01:42Z) are older and already counted here.

## 4. Not done
- **Every live feedback store is UNMEASURED:** MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, the NexusAI share `feedbackItems`, Portal Postgres, the QuickQuote table. Each needs az, a writing sign-in, or HTTP to a hosted host, all out of bounds. **"0 new" means only that nothing reached the mailbox, Jira or GitHub.**
- **Who wrote a Jira comment:** the shared "Kamil Kreiser" account cannot tell Kam from a seat. Openings only were read.
- **HPSM GitHub:** `gh` not logged in under HPSM's config.
- **Mail bodies** not read (subjects, senders, timestamps only). Mail to other inboxes not read; `coagent@` bus not read at all (the `coagent@` rows above are copies that reached `tuesday-agent@`).
- **Kam's card board** not re-read, so any ruling made after the 07:50 sweep is not reflected.
- **Job B** (ticket sweep) not in scope for this run.
- No HTTP to any app host, hosted site or production; no az or docker; no git write verbs; no Jira, gh, mail or card writes.
