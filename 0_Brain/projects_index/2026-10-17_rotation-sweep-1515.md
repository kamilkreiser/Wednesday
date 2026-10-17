# Rotation sweep: Datasec feedback delta (2026-10-17 15:15)

A read-only sub-agent ran this for Tuesday at **15:15-15:19 AEDT on 2026-10-17** (`date`: Sat 17 Oct 2026 15:15:43 AEDT = 2026-10-17T04:15:43Z). It is the delta since [[2026-10-17_rotation-sweep-0935]]. **Window: from that sweep's outgoing watermarks to about 15:15 AEDT (04:15Z):** mailbox after 2026-10-16T22:35:07Z, Jira `>= "2026-10-17 09:20"`, GitHub `since=2026-10-16T22:15:00Z`. That is about 6 h, with a small overlap on purpose. I used the same method and store map as [[2026-10-16_feedback-sweep-1]].

**Instruments, and what I did not do:** I made each project's own Jira REST `GET /rest/api/3/search/jql` calls, paged until `isLast`, plus `GET /issue/<key>/comment`. Each used that project's own `4_Credentials/.env`, read by variable name inside a Python process and never printed. I made read-only `gh api --paginate` GETs under each project's own `GH_CONFIG_DIR`, and used `git for-each-ref`, `log` and `show` only (no fetch). I made AgentMail list GETs for tuesday-agent@ with Tuesday's own key. I made **no HTTP of any kind to an app host or a production host**, and no Jira, git, gh, mail or az writes.

## 1. BLUF

**No new feedback items in the window: 0 across all projects.** No new client-human responses, including the excluded projects. Agents created 20 new tickets in the window (RD-850..854, MPSCALC-213..227). All were seat-written, and none is a feedback item.

| Project | New feedback items in window | New client-human responses | New tickets created in window | Other activity in window (not feedback) |
|---|---|---|---|---|
| **NexusAI** (RD) | **0** | **0** | 5 (RD-850..854, 13:03, gate 24 findings, seat) | **Main moved `17fc6c51` → `065a0d8f`** (PR #87, RD-848, merged 02:07:42Z). 10 issues updated, 8 comments, all seat-written. Mail: gate 24 GO WITH FINDINGS, the TURN, the RD-837 / RD-802 / RD-828 s2 ANSWERs, and a T9-unmounted QUESTION (03:34Z) |
| **Vision Portal** (VSP) | **0** | **0** | **0** | None. No Jira change, no commits, no issue or PR updated |
| **Vision QuickQuote** | **0** (no `QuickQuote feedback (` mail) | **0** | n/a (BACKLOG tracker) | PR #10 round 3 READY FOR QA @ `f31720e` (v2.39, 00:31Z), then **gate 22 GO WITH FINDINGS** (03:51Z). Main is unchanged at `437ab4bc` |
| **Security Composer** | **0** | **0** | n/a (BACKLOG tracker) | None. GitHub main is still `230f9fab`. Newest local branch is still `records/b155` (10-16 13:11). 0 local commits since 09:20 |
| **MPS Calculator** (MPSCALC, *excluded*) | not swept (excluded) | **0** | 15 (MPSCALC-213..227, 14:40-14:42, seat) | 6 PRs merged (#74 #75 #76 #77 #78 #79); main now `1e8a738f`. 26 issues updated, 16 comments, all seat-written. Kam card rulings were recorded by the seat on -194, -203, -144 |
| **HPSM-POC** (HPSMPOC, *excluded*) | not swept (excluded) | **0** | **0** | PR #157 merged 04:03:43Z: `787d1590`, HPSMPOC-254. **Jira still not updated for PR #156 or #157** (see 3). HPSM-POC-analysis: 0 commits |
| **HPSM** (HPSM) | **0** | **0** | **0** | None. GitHub **UNMEASURED** (`gh` is still not logged in under HPSM's config) |

There is no per-item section below, because the window holds no new feedback item and no client-human response. Section 2 gives the controls that prove each instrument could have seen one.

## 2. Evidence and controls

### Mailbox (tuesday-agent@agentmail.to)
- `GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`: 1 page, 100 fetched. The oldest fetched was 2026-10-16T02:26:02Z, so the window is fully covered. The newest was 2026-10-17T03:54:56Z.
- **26 messages after 22:35:07Z.** All 26 are fleet mail, from `coagent@` (17) or `tuesday-agent@` (9, Tuesday's own TURN / ANSWER / ROUND 3 mails):
  - NexusAI-O (and QA/NexusAI): READY FOR GATE rd-802, READY FOR QA RD-837 and RD-828 s2, READY RD-837 r2, gate 24 verdict, STATUS TURN step 1, MERGED RD-848, QUESTION T9 unmounted.
  - Vision (and QA/Vision): READY FOR QA QQEP round 3, gate 22 verdict.
  - MPS: B104 lane E READY FOR GATE (x2), QUESTION B167 store-compat, ADDENDUM-7 (x2), QUESTION B169 main moved, ADDENDUM-8.

  **0 feedback notices.** Across all 100 fetched, 1 subject contains "feedback": the NexusAI-O READY FOR GATE for branch `rd-801-feedback-log-injection` at 22:35:07Z, which is the watermark message itself (excluded by `>`), and a CodeQL fix, not a feedback item. **0 senders outside `coagent@` / `tuesday-agent@` in the window.**
- **Control 1 (continuity):** the window boundary is exactly the 09:35 sweep's outgoing watermark (22:35:07Z, the rd-801 READY FOR GATE). The first message after it is 22:36:35Z (Tuesday ANSWER on RD-801 + RD-822).
- **Control 2 (the instrument sees a feedback notice):** I paged back 6 pages (600 messages, to 10-06T11:11Z) with the same call. It found `QuickQuote feedback (feature)` from the HPAM Quoting Agent sender at **2026-10-09T16:51:40Z**, the known CAD-currency item (C-14).

### Jira (JQL in AEDT; W = `"2026-10-17 09:20"`; every count paged to `isLast`; last JQL about 15:18)

| Project | JQL | Total | Control (a query known to hit) |
|---|---|---|---|
| RD | `project = RD AND (created >= W OR updated >= W)` | **10**: RD-850..854 (created 13:03), RD-848 (13:58), RD-828 (12:31), RD-837 (11:39), RD-802 (11:31), RD-801 (09:35) | This same query catches 10 in-window changes, so it sees them |
| RD | `project = RD AND summary ~ "\"Feedback #\"" AND (created >= W OR updated >= W)` | **1**: RD-801. A fuzzy text match on "feedback" (CodeQL log-injection in `backend/routes/feedback.js`). Not a `Feedback #N` item | `project = RD AND summary ~ "\"Feedback #\""` → **21** (unchanged) |
| RD | `project = RD AND labels in (feedback, user-feedback)` | 5 (no change) | n/a |
| RD | `project = RD AND created >= "2026-10-16 12:00"` | 7 (RD-848..854) | was 2; +5 is RD-850..854 |
| RD comments | `GET /issue/<key>/comment` on all 10, created ≥ 09:20 | **8** (RD-801, -802, -828, -837 x3, -848, -853), all "Kamil Kreiser" (shared account). **I read the opening of all 8; every one reads as seat-written** ("S100O re-check…", "READY FOR QA (tier 2…", "MERGED (S100O…", "Review CLOSED and accepted by Tuesday…", "Closed: the correction was posted…") | n/a |
| VSP | `project = VSP AND (created >= W OR updated >= W)` | **0** | `project = VSP AND statusCategory != Done` → **16** (unchanged) |
| HPSMPOC | `project = HPSMPOC AND (created >= W OR updated >= W)` | **0** | `labels = hp-feedback` → **5** (newest still HPSMPOC-230); `updated >= "2026-10-16 12:00"` → **27** (unchanged); `project = HPSMPOC` → 259 |
| MPSCALC | `project = MPSCALC AND (created >= W OR updated >= W)` | **26** (15 created, MPSCALC-213..227; all in Backlog; reporter the shared account) | `created >= "2026-10-16 12:00"` → **92** (was 77; +15) |
| MPSCALC | `… AND (summary ~ feedback OR labels in (feedback, user-feedback, in-app-feedback)) AND (created >= W OR updated >= W)` | 1: MPSCALC-194 (feedback-dialog 401 wording, a hardening finding, now ruled and merged in PR #79). Not an in-app feedback item. `labels in (feedback, …)` alone → 0 | n/a (MPS is excluded) |
| MPSCALC comments | `GET /issue/<key>/comment` on all 26, created ≥ 09:20 | **16**, all "Kamil Kreiser". **I read the opening of all 16; every one reads as seat-written** ("BLUF: merged to main in PR #…", "B104 lane E…", "BLUF: the product owner ruled card … = a/b", "BLUF: gate B167-… widens this ticket") | n/a |
| HPSM | `project = HPSM AND (created >= W OR updated >= W)` | **0** | `project = HPSM` → **41** (unchanged) |

**Client-human responses:** all 24 in-window Jira comments come from the shared account and read as seat-written (I read the opening of each, not every full body). HPSMPOC-241 (the HP answers ticket) was not updated (last 10-16 12:34). None of the 26 in-window mails comes from a client human.

### GitHub (`gh api --paginate`, since 2026-10-16T22:15:00Z)

| Repo (gh config) | Commits on main since | Issues+PRs updated since | Open PRs | Open issues (non-PR) | Control: newest main commit |
|---|---|---|---|---|---|
| Reporting_Dashboard_Au (NexusAI) | 0 (see note) | 1 (PR #87, merged 02:07Z) | #70 #67 #58 | 0 | `065a0d8f`, committer date 10-16T20:21Z |
| vision_datasec-sales-portal (Vision) | 0 | 0 | #17 #16 #15 #14 | 0 | `6dbffdf3` 09-28 |
| vision_hpas-quickquote (Vision) | 0 | 1 (PR #10, open, 00:30:24Z) | #10 #8 | 0 | `437ab4bc` 10-16T04:07Z |
| Datasec-Security-Composer (Composer) | 0 | 0 | none | 0 | `230f9fab` 10-16T00:56Z |
| HPSM-POC (HPSM-POC) | **1** (`787d1590`) | 1 (PR #157, merged) | none | 0 | `787d1590` 10-17T04:03Z |
| HPSM-POC-analysis (HPSM-POC) | 0 | 0 | none | 0 | `6f5f0dc5` 10-16T01:52Z |
| MPS-Commercial-Calculator (MPS) | **6** (`ed726068` `0217044e` `422b87b2` `725b4ef5` `f1d5641a` `1e8a738f`) | 6 (PRs #74-#79, all merged) | none | 0 | `1e8a738f` 10-17T04:02Z |

The HPSM-POC, MPS and QuickQuote rows show that the "since" filter does see in-window activity. **No GitHub issue was opened on any repo**, so no feedback arrived as an issue.

**Frame notes:** (a) The NexusAI commits-since count is 0 even though main moved, because `commits?since=` filters on committer date and PR #87 was a fast-forward of a commit dated 10-16T20:21Z; the move is seen through PR #87 in the issues list and the changed main SHA. (b) The 09:35 file said `since=22:15:00Z` would re-catch HPSM-POC PR #156; it does not, because that merge was at 22:14:13Z. Nothing was missed: #156 was already counted at 09:35.

### Composer carry-forward re-check
- I grepped `1061d219|d477d020` (case-insensitive) in `BACKLOG.md` on **all 78 local branches**: **0 hits**, the same as the last three sweeps. Control: `C-62` on main's BACKLOG gives 3.
- `git log --all --since=2026-10-17T09:20+11:00` in the Composer records repo gives 0; in the code checkout (`2_Project_Files`) also 0. Newest refs: `records/b155` (10-16 13:11) and `b152/approved-words-and-looks` (10-14).

## 3. Notes for Tuesday (not feedback)

1. **HPSM-POC Jira lag: still open, now about 6 h.** PR #156 (`72073dac`, 09:14 AEDT) names HPSMPOC-251/-252/-253/-255/-256/-258, and PR #157 (`787d1590`, 15:03 AEDT) names HPSMPOC-254. All seven are still in **Backlog**, last updated 10-16 12:26-12:28, and `project = HPSMPOC AND updated >= W` → 0 at about 15:18. At 09:35 this looked like normal wrap lag; at 6 h it is a pattern to raise with the HPSM-POC seat (the same thing MPS showed at 07:40 and then closed).
2. **NexusAI main moved** to `065a0d8f` (RD-848, PR #87), under Tuesday's TURN at 02:02:12Z after gate 24 GO WITH FINDINGS. RD-850..854 are the gate 24 findings (RD-853 already Done). The NexusAI-O QUESTION at 03:34Z (T9 unmounted, jest lock unreachable) got two Tuesday ANSWERs at 03:35Z, the second marked SUPERSEDES.
3. **MPS:** 6 merges to main in the window (#74-#79). Kam card rulings were recorded by the seat as Jira comments on MPSCALC-194 (= a), -203 (= b) and -144 (= b); these are Kam's rulings relayed by the seat, not client-human responses. The seat filed MPSCALC-213..227 from B169 (several labelled `needs-ruling`: -222, -224, -226). Open mail: QUESTION "B169 main moved to #78 during merge comments" (03:46Z) and ADDENDUM-8 READY FOR GATE (03:54Z).
4. **Vision QuickQuote:** gate 22 GO WITH FINDINGS on QQEP @ `f31720e` (03:51Z). PR #10 is still open.
5. **Unticketed items carried forward** (unchanged): Composer `d477d020` (editions lookup, needs Kam); Vision Portal #6 (Social Media Engagement tile; Portal paused); HPSMPOC-242 (an empty placeholder; HPSM-POC excluded).

## 4. Watermarks out
- Mailbox: **2026-10-17T03:54:56Z**.
- Jira: **2026-10-17 15:18 AEDT** (time of the last JQL). A safe value for the next `>=` is `"2026-10-17 15:00"`.
- GitHub: `since=2026-10-17T03:55:00Z` is safe. It re-catches the HPSM-POC PR #157 and MPS PR #79 merges (04:02-04:03Z) as known items.

## 5. UNMEASURED (same as the earlier sweeps)
- **Every live feedback store** (MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, the NexusAI share, Portal Postgres, the QuickQuote table). Each needs `az`, an app sign-in that writes, or HTTP to a hosted host. "0 new" means 0 reached the mailbox, Jira or GitHub.
- **Who wrote a Jira comment.** The shared "Kamil Kreiser" account cannot tell Kam from a seat. I read the opening (up to about 400 characters) of all 24 in-window comments, and every one reads as seat-written; I did not read every full body.
- **HPSM GitHub** (commits, PRs, issues): `gh` is not logged in under `HPSM/4_Credentials/.gh-config`.
