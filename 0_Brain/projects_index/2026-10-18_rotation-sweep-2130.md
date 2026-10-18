# Rotation sweep: Datasec feedback delta (2026-10-18, 21:30)

A read-only sub-agent (claude-sonnet-5-5) ran this for Tuesday from **21:36 to about 21:40 AEDT on 2026-10-18** (`date`: Sun 18 Oct 2026 21:36:37 AEDT = 2026-10-18T10:36:37Z).

- **Scope:** a feedback delta only, since [[2026-10-18_rotation-sweep-1930]] §4. I did not redo Job B (the ticket sweep).
- **Window:** mailbox after 2026-10-18T08:19:46Z; Jira `>= "2026-10-18 19:10"` AEDT; GitHub `since=2026-10-18T08:30:00Z`. That is roughly 2 h 5 min on Jira, 2 h on GitHub and 2 h 15 min on the mailbox.
- **Method:** the same as the 19:30 sweep (its header and §2). Jira used each project's own REST `search/jql`, paged to `isLast`, plus `/issue/<key>/comment` on every in-window issue. Credentials were read from each project's own `4_Credentials/.env` by variable name inside `python3 -I` and never printed. GitHub used `gh api --paginate` GETs under each project's own `GH_CONFIG_DIR`. git used `log`, `show`, `for-each-ref`, `rev-parse` and `config --get` only, with `--no-optional-locks`. Mail used AgentMail list GETs on tuesday-agent@ (subjects, senders and list previews only). Kam's cards were read with `bash 2_Project_Files/tools/decision_queue.sh list ruled` and `list`, filtered to Datasec lines on 2026-10-18.
- **What I did not do:** no HTTP of any kind to an app host, hosted site or production; no az or docker; no Jira, git, gh, mail or card writes; no git fetch, pull or worktree.
- **Exclusions:** as before. MPS Calculator and HPSM-POC were read under every instrument but are marked *excluded* (Kam's 2026-10-12 rule). **No feedback item from either project appeared in the window,** so the choice changes no count.

## 1. BLUF

**There are no new feedback items: 0 across all projects. There are no new client-human responses: 0.** Every mail in the window came from a seat, a gate, Wednesday or Tuesday. Every in-window Jira comment opens in a seat's voice ("S101O: …", "BLUF: …"). All GitHub activity was by `kamilDatasec`: one draft PR opened, one PR merged, one PR opened. The QuickQuote production publish attempt (21:14 to 21:24 AEDT, rolled back) left no trace in any of the three instruments I am allowed to use except the open retry card.

| Project | New feedback items | Client-human responses | Other activity in window (not feedback) |
|---|---|---|---|
| **NexusAI** (RD) | **0** | **0** | 2 issues updated, 0 created. **RD-778 is now READY FOR QA** (comment 21:18; draft **PR #94**, 10:18Z, branch `rd-778-xss-through-dom-s101o` @ `3047ae92`). RD-476 (19:12) is the 19:30 sweep's watermark row, seen again. `summary ~ "Feedback #"` in window 0. Main unchanged at `c7ca0ed7`. **Gate 25 verdict arrived** (RD-761 GO, RD-794 stacked GO WITH FINDINGS) and Tuesday released it (ANSWER-16, 10:35Z). Kam ruled RD-476 wording fixes (a) at 20:56 |
| **Vision Portal** (VSP) | **0** | **0** | None |
| **Vision QuickQuote** | **0** (no `QuickQuote feedback (` mail) | **0** | **PR #10 (v2.39, "email matches print") merged** to main as `5fa1187b` at 09:57:49Z (20:57 AEDT). PR #8 still open. The production publish attempt (21:14 to 21:24) was rolled back (expected); open retry card `quickquote-v239-retry-after-outage-1018`. Kam ruled the "five more sentences" card (a) at 20:56 |
| **Security Composer** | **0** | **0** | None. GitHub main still `230f9fab`. 0 local commits since 19:10 in all three local repos |
| **MPS Calculator** (MPSCALC, *excluded*) | 0 seen | **0** | **14 seat comments at 20:00:01 to 20:00:13** (deploy seat B268: "live on the hosted showcase since 2026-10-18", main `e6f92a5f`; plus MPSCALC-222/223/224/225/202/231 notes). No Jira creates. No GitHub activity. Seen as a seat bulk-comment, not feedback |
| **HPSM-POC** (HPSMPOC, *excluded*) | 0 seen (no new `hp-feedback`) | **0** | **PR #160** (round 3, BFF upload counter, HPSMPOC-281/-284/-285) open, updated 09:55:08Z (expected). Main unchanged at `dff40192`. Jira: no change since 16:54 (HPSMPOC-268 is still the newest). Kam ruled the 10.0.13 route card (a) at 20:56 |
| **HPSM** (HPSM) | **0** | **0** | None. GitHub is **UNMEASURED** (`gh` is not logged in) |

**Proposed tickets or categories:** none, because there are no new feedback items to categorise.

## 2. Evidence and controls

### Mailbox (tuesday-agent@agentmail.to)
- `GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`, paged 10 times (1,000 messages, newest **2026-10-18T10:35:43Z**, oldest 2026-10-04T09:20:40Z). The window is fully covered by page 0.
- **8 messages fall at or after 08:19:46Z** (7 after the watermark message, plus the watermark message itself):
  - 3 from `coagent@`: NexusAI-O READY FOR QA (RD-778, 10:18Z); NexusAI-O STATUS (RD-476 Q7/Q8 live re-run, money stated, 09:58Z); **QA/Datasec-NexusAI GATE VERDICT gate 25 (09:58Z)**.
  - 4 from `tuesday-agent@`: CORRECTION to NexusAI-O (08:19:46Z, the watermark), a shared-tooling note (08:40Z, `card_id_gate.sh` widened), ANSWER to NexusAI-O on Kam's RD-476 wording ruling (09:57Z), **ANSWER-16 RELEASE gate 25** (10:35Z).
  - 1 from `wednesday-agent@`: model routing v1.0 in force (coordination, 09:58Z).
- Fleet mail in window, as a count only: **8** (0 feedback).
- **0 feedback notices** (`QuickQuote feedback (` or `Vision feedback #`) and **0 senders outside the fleet** in the window. No mail from a QuickQuote seat is in this inbox for the 21:14 to 21:24 attempt, so its rollback is not visible here.
- **Control 1 (continuity):** the watermark message, Tuesday's CORRECTION to NexusAI-O at 2026-10-18T08:19:46Z, comes back in the same call. So the window edge is seen.
- **Control 2 (the instrument sees a feedback notice and an outside sender):** the same 10-page read returns `QuickQuote feedback (feature) from john.spears@datasec.com.au` from the HPAM Quoting Agent at **2026-10-09T16:51:40Z** (the known C-14 item), and Kam's forwards from `kamil.kreiser@datasec.com.au`, the newest at 2026-10-17T04:56:13Z. So the instrument fires on both.

### Jira (JQL in AEDT; W = `"2026-10-18 19:10"`; every query paged to `isLast`; read once at about 21:37)

| Project | JQL | Result | Control |
|---|---|---|---|
| RD | `project = RD AND (created >= W OR updated >= W)` | **2** updated, 0 created: RD-778 (21:18), RD-476 (19:12) | The query fires (2 rows) and re-sees the 19:12 watermark row. `project = RD` → 853 (unchanged) |
| RD | `summary ~ "\"Feedback #\""` in window / total | **0** / 21 | Total unchanged (21) |
| RD | `labels in (feedback, user-feedback)` in window / total | **0** / 5 | Total unchanged (5) |
| RD comments | `/issue/<key>/comment` on both, created ≥ 19:10 | **2**, both "Kamil Kreiser" (the shared account): RD-778 ("S101O: READY FOR QA mailed to Tuesday …"), RD-476 ("BLUF: the RD-476 live check ran on the existing dev deployment …") | n/a |
| VSP | same window query | **0** | `project = VSP` → 89 (unchanged). The newest updated is VSP-67 at 09-29 07:05, which the same instrument sees |
| VSP | `summary ~ feedback` in window / total | 0 / 1 | Total unchanged |
| HPSM | same window query | **0** | `project = HPSM` → 41 (unchanged). The newest updated is HPSM-21 at 10-02 10:14 |
| HPSMPOC | same window query | **0** | `project = HPSMPOC` → 287 (unchanged). Newest updated HPSMPOC-268 at 16:54, which the same instrument sees. Nothing changed after 16:54 |
| HPSMPOC | `labels in (feedback, user-feedback, hp-feedback)` in window / total | **0** / 16 (the 19:30 sweep's 5 `hp-feedback` + 11 `feedback`) | Total matches the prior sweep (5 + 11); `summary ~ "Feedback #"` total 22. The instrument sees the labels |
| MPSCALC | same window query | **14** updated, 0 created: -231, -225, -224, -223, -222, -214, -213, -203, -202, -194, -158, -155, -142, -140, all at 20:00 | `project = MPSCALC` → 231 (unchanged). Newest updated MPSCALC-224 at 20:00 |
| MPSCALC | feedback labels / `summary ~ "Feedback #"` in window | 0 / **1** (MPSCALC-194, total 13) | MPSCALC-194 is "Feedback dialog after a feedback-only 401 …", a seat-filed `plan-b164-r06` ticket about the dialog wording; it matched on the word, not on a submission. It was updated at 20:00 by the B268 deploy comment |
| MPSCALC comments | on all 14, created ≥ 19:10 | **14**, all at 20:00:01 to 20:00:13, all opening "BLUF: …" (10 x "live on the hosted showcase since 2026-10-18 (deploy seat B268) …" on -140, -142, -155, -158, -194, -203, -213, -214; -231 "merged to main in PR #83"; -222, -223, -224, -225 and -202 are B268 measurements) | n/a |

**Client-human responses in Jira:** 0. I read the opening (about 140 characters) of all 16 in-window comments. All read as written by a seat.

### GitHub (`gh api --paginate`, since 2026-10-18T08:30:00Z; read at about 10:37Z)

| Repo (gh config) | Commits on main since | Issues and PRs updated since | Issue / review comments since | Open PRs | Open issues (non-PR) | Control: main HEAD |
|---|---|---|---|---|---|---|
| Reporting_Dashboard_Au (NexusAI) | 0 | **1**: PR #94 (RD-778, draft, kamilDatasec, 10:18:33Z) | 0 / 0 | #94 (d) #93 (d) #92 (d) #91 (d) #70 #67 #58 | 0 | `c7ca0ed7` 10-17T08:56Z |
| vision_datasec-sales-portal (Vision) | 0 | 0 | 0 / 0 | #17 #16 #15 #14 | 0 | `6dbffdf3` 09-28 |
| vision_hpas-quickquote (Vision) | **1** (`5fa1187b`, 09:57:49Z, "Merge PR #10: QuickQuote v2.39, email matches print (C-20 fix 2 …") | 1 (PR #10, closed and merged by kamilDatasec, 09:57:50Z) | 0 / 0 | #8 | 0 | `5fa1187b` 10-18T09:57Z |
| Datasec-Security-Composer (Composer) | 0 | 0 | 0 / 0 | none | 0 | `230f9fab` 10-16T00:56Z |
| HPSM-POC (HPSM-POC) | 0 | **1**: PR #160 (open, not draft, kamilDatasec, 09:55:08Z) | 0 / 0 | #160 | 0 | `dff40192` 10-18T05:04Z |
| HPSM-POC-analysis (HPSM-POC) | 0 | 0 | 0 / 0 | none | 0 | `d479cb67` 10-18T06:09Z |
| MPS-Commercial-Calculator (MPS) | 0 | 0 | 0 / 0 | none | 0 | `21c2aec7` 10-17T20:06Z |

**Control:** the `since` filter returns in-window activity on three repos (NexusAI #94, QuickQuote #10 / `5fa1187b`, HPSM-POC #160), so it fires. On each zero repo, the pre-window HEAD is visible through the same credentials. **No GitHub issue was opened on any repo,** and there are no issue or review comments anywhere in the window.

### Composer carry-forward re-check
- I grepped `1061d219|d477d020` in `BACKLOG.md` on **all 78 local branches** of the records repo (the Composer project root, `Datasec Security Composer`): **0 hits**, the same as before. Control: `C-62` on main's BACKLOG gives 3.
- `git log --all --since=2026-10-18T19:10+11:00` gives **0** in all three local repos (records root, `2_Project_Files`, `_wt_b151code`). Controls: records `--since=2026-10-15` gives 1 (newest `3266142b`, 10-16 13:11); `2_Project_Files` newest commit `fa5a0b6a` 10-14 07:34; `_wt_b151code` newest `45591406` 10-13 20:50. GitHub shows no Composer activity, so nothing changes.

### Kam's cards (checked before calling anything new)
- `decision_queue.sh list ruled`, Datasec lines dated 2026-10-18 (live board):
  - **At 18:59** (already in the 19:30 sweep): NexusAI RD-476 prompt words (b), NexusAI C-170 shipped-docs words (a), QuickQuote 2.39 publish (a), HPSM-POC hosted runtime to 10.0.13 (a), MPS Calculator hosted deploy e6f92a5 (a).
  - **New at 20:56:** `nexusai-rd476-two-wording-fixes-1018` => a, `quickquote-v239-five-more-sentences-1018` => a, `hpsmpoc-runtime-10013-route-1018` => a (the third card is the "wait for Azure or pin Microsoft's image now" question). These are rulings, not feedback.
- `list` (open, Datasec): `composer-l05-setup-card-too-1014` (open since 10-14) and **`quickquote-v239-retry-after-outage-1018`** ("retry the publish after tonight's failed attempt?"; default: hold, no retry without Kam's tap, live stays on 2.36, Tuesday re-raises Monday 19 Oct). The retry card matches the expected rolled-back publish attempt. The store listing also prints other clients' cards; I used none of them.

## 3. Notes for Tuesday (not feedback)
1. **Gate 25 has mailed back and Tuesday has already answered:** `GATE VERDICT — gate 25` at 09:58:25Z, then ANSWER-16 at 10:35:43Z releasing RD-761 (GO) and RD-794 stacked (GO WITH FINDINGS) after the seat's RD-476. Nothing outstanding from gate 25 in subjects. (Gate 26 from the 19:30 sweep: no later subject names it; I cannot tell from subjects whether its findings were acknowledged, as before.)
2. **NexusAI-O's RD-778 is READY FOR QA** (mail 10:18Z, Jira comment 21:18, draft PR #94). The seat is waiting on a gate, not on Tuesday, unless Tuesday has not yet launched one. The RD-476 Q7/Q8 live re-run was reported at 09:58Z after Tuesday's 09:57Z ANSWER.
3. **QuickQuote v2.39 is merged to main (`5fa1187b`) but not live** (publish rolled back). The only open item is Kam's retry card. No QuickQuote seat mail sits in tuesday-agent@ for the failed attempt; the failure detail is not visible to this sweep.
4. **MPS Calculator is live on the hosted showcase** per 14 B268 comments at 20:00 (main `e6f92a5f`); the same comments say the host still reports DOTNETCORE-10.0.12 (MPSCALC-223/-224/-225). Excluded from counts.
5. **HPSM-POC PR #160 is open** (round 3). Kam ruled route (a) on the 10.0.13 card at 20:56.

## 4. Watermarks out
- **Mailbox:** **2026-10-18T10:35:43Z** (Tuesday's ANSWER-16 to NexusAI-O releasing gate 25, the newest message read).
- **Jira:** the newest processed change is **RD-778, updated 2026-10-18 21:18** (AEDT). Use `>= "2026-10-18 21:15"` for the next run, a small overlap, because NexusAI-O is active on RD-778 and RD-476.
- **GitHub:** `since=2026-10-18T10:18:00Z`. The newest activity seen was 2026-10-18T10:18:33Z (NexusAI PR #94); the reads ran at about 10:37Z, but the watermark goes no further than the newest item read.

## 5. UNMEASURED
- **Every live feedback store:** MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, the NexusAI share `feedbackItems`, Portal Postgres, and the QuickQuote table. Each needs az, a sign-in that writes, or HTTP to a hosted host, all of which are out of bounds. **"0 new" means only that nothing reached the mailbox, Jira or GitHub.**
- **Who wrote a Jira comment.** The shared "Kamil Kreiser" account cannot tell Kam from a seat. I read the opening of each in-window comment, not the full body.
- **HPSM GitHub:** `gh auth status` under `HPSM/4_Credentials/.gh-config` says "You are not logged into any GitHub hosts".
- **Mail bodies.** Only list previews and subjects were read, including the gate 25 verdict.
- **Mail sent to other inboxes.** I read only tuesday-agent@. The QuickQuote seat's account of the failed publish, if mailed, went elsewhere.
- **The Composer code repo's newest commits.** The local `2_Project_Files` stops at 10-14 because fetch is not allowed. GitHub was the instrument for Composer code instead.
- **Vision QuickQuote Jira.** As in earlier sweeps, QuickQuote has no Jira project of its own in this instrument set; its feedback path here is the `QuickQuote feedback (` mail plus GitHub.
