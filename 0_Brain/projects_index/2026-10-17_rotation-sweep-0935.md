# Rotation sweep: Datasec feedback delta (2026-10-17 09:35)

A read-only sub-agent ran this for Tuesday at **09:32-09:40 AEDT on 2026-10-17** (`date`: Sat 17 Oct 2026 09:32:15 AEDT = 2026-10-16T22:32:15Z). It is the delta since [[2026-10-17_rotation-sweep-0740]]. **Window: from that sweep's outgoing watermarks to about 09:35 AEDT (22:35Z):** mailbox after 2026-10-16T20:32:15Z, Jira `>= "2026-10-17 07:30"`, GitHub `since=2026-10-16T20:30:00Z`. That is about 2 h, with a small overlap on purpose. I used the same method and store map as [[2026-10-16_feedback-sweep-1]].

**Instruments, and what I did not do:** I made each project's own Jira REST `GET /rest/api/3/search/jql` calls, paged until `isLast`, plus `GET /issue/<key>/comment`. Each used that project's own `4_Credentials/.env`, read by variable name inside a Python process and never printed. I made read-only `gh api --paginate` GETs under each project's own `GH_CONFIG_DIR`, and used `git for-each-ref`, `log` and `show` only (no fetch). I made AgentMail list GETs for tuesday-agent@ with Tuesday's own key. I made **no HTTP of any kind to an app host or a production host**, and no Jira, git, gh, mail or az writes.

## 1. BLUF

**No new feedback items in the window: 0 across all projects.** No new client-human responses, including the excluded projects. Agents created 25 new tickets in the window (RD-849, MPSCALC-189..212). All were seat-written, and none is a feedback item.

| Project | New feedback items in window | New client-human responses | New tickets created in window | Other activity in window (not feedback) |
|---|---|---|---|---|
| **NexusAI** (RD) | **0** | **0** | 1 (RD-849, seat-filed, from S100O's N-801-1; mail 20:44Z) | RD-801 and RD-802 updated 07:44 (no comments). RD-828 got 1 seat comment at 09:02 (S100O slice 2 start). Mail 22:35Z: READY FOR GATE `rd-801-feedback-log-injection-s87o` @ `66131135`. Main is unchanged at `17fc6c51` |
| **Vision Portal** (VSP) | **0** | **0** | **0** | Dependabot opened PR #17 (proxy-addr 2.0.7 → 2.0.8) at 20:53:52Z. No Jira change, no commits |
| **Vision QuickQuote** | **0** (no `QuickQuote feedback (` mail) | **0** | n/a (BACKLOG tracker) | **Gate 21 NO GO** on PR #10 @ `3a3399e` (mail 22:27Z). PR #10 itself was last updated 20:31:49Z, inside the overlap and already counted in the 07:40 sweep. Main is unchanged at `437ab4bc` |
| **Security Composer** | **0** | **0** | n/a (BACKLOG tracker) | None. GitHub main is still `230f9fab`. The newest local branch is still `records/b155` (10-16 13:11). 0 local commits on any branch since 06:00 |
| **MPS Calculator** (MPSCALC, *excluded*) | not swept (excluded) | **0** | 24 (MPSCALC-189..212, 08:06-08:07, seat) | PR #73 merged at 21:13:07Z: `12f8e566`, MPSCALC-150/-158 lane D stack. 66 issues updated, with 42 comments, all seat-written. Mail: B104 lane E addenda and 142/155 + 140 READY FOR REVIEW (22:23Z). **The Jira lag from the 07:40 note is closed** (see 3) |
| **HPSM-POC** (HPSMPOC, *excluded*) | not swept (excluded) | **0** | **0** | PR #156 merged at 22:14:13Z: `72073dac`, HPSMPOC-251/-252/-253/-255/-256/-258. **Jira not yet updated for it** (see 3). HPSM-POC-analysis: 0 commits |
| **HPSM** (HPSM) | **0** | **0** | **0** | None. Open PRs **UNMEASURED** (`gh` is still not logged in under HPSM's config) |

There is no per-item section below, because the window holds no new feedback item. Section 2 gives the controls that prove each instrument could have seen one.

## 2. Evidence and controls

### Mailbox (tuesday-agent@agentmail.to)
- `GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`: 1 page, 100 fetched. The oldest fetched was 2026-10-15T23:12:11Z, so the window is fully covered. The newest was 2026-10-16T22:35:07Z.
- **9 messages after 20:32:15Z.** All 9 are fleet mail, from `coagent@` (7) or `tuesday-agent@` (2 Tuesday ANSWERs to NexusAI-O):
  - NexusAI-O: the N-801-1 ANSWER and STATUS, the C-57 STATUS and ANSWER, and READY FOR GATE rd-801.
  - Vision: the gate 21 NO GO verdict.
  - MPS: B104 lane E ADDENDUM-2, ADDENDUM-3, and READY FOR REVIEW.

  **0 feedback notices.** Across all 100 fetched, 2 subjects contain "feedback". Both are fleet mail: the NexusAI-O READY FOR GATE for branch `rd-801-feedback-log-injection` (22:35Z, a CodeQL fix, not a feedback item) and the MPS QUESTION on MPSCALC-174 (10-16 02:00Z, before the window).
- **Control 1 (continuity):** the oldest message in my window boundary is 2026-10-16T20:32:15Z (`[Datasec/Vision_Sales_Portal -> Tuesday] READY FOR QA (round 2, tier 1)…`). That equals the 07:40 sweep's outgoing mailbox watermark exactly.
- **Control 2 (the instrument sees a feedback notice):** I paged back 4 pages (400 messages, to 10-07T11:19Z) with the same call. It found `QuickQuote feedback (feature) from john.spears@datasec.com.au` at **2026-10-09T16:51:40Z**, the known CAD-currency item (C-14).

### Jira (JQL in AEDT; W = `"2026-10-17 07:30"`; every count paged to `isLast`; last JQL about 09:34)

| Project | JQL | Total | Control (a query known to hit) |
|---|---|---|---|
| RD | `project = RD AND (created >= W OR updated >= W)` | **4**: RD-849 (created 07:44), RD-801 and RD-802 (updated 07:44), RD-828 (updated 09:02) | This same query catches 4 in-window changes, so it sees them |
| RD | `project = RD AND summary ~ "\"Feedback #\"" AND (created >= W OR updated >= W)` | **1**: RD-801. This is a fuzzy text match on "feedback" in its summary (CodeQL log-injection in `backend/routes/feedback.js`). It is not a `Feedback #N` item | `project = RD AND summary ~ "\"Feedback #\""` → **21** (unchanged); newest real item is still RD-842 (Feedback #10) |
| RD | `project = RD AND labels in (feedback, user-feedback)` | 5 (RD-400, 401, 840, 841, 842; no change) | n/a |
| RD | `project = RD AND created >= "2026-10-16 12:00"` | 2 (RD-848, RD-849) | was 1; +1 is RD-849 |
| RD comments | `GET /issue/<key>/comment` on all 4, created ≥ 07:30 | 1 (RD-828, 09:02, "Kamil Kreiser", the shared account; text starts "S100O (seat O) starts slice 2…") | n/a |
| VSP | `project = VSP AND (created >= W OR updated >= W)` | **0** | `project = VSP AND statusCategory != Done` → **16** (unchanged) |
| HPSMPOC | `project = HPSMPOC AND (created >= W OR updated >= W)` | **0** | `labels = hp-feedback` → **5** (newest is still HPSMPOC-230); `updated >= "2026-10-16 12:00"` → **27** (unchanged) |
| MPSCALC | `project = MPSCALC AND (created >= W OR updated >= W)` | **66** (24 created, MPSCALC-189..212; all in Backlog; reporter is the shared account) | `created >= "2026-10-16 12:00"` → **77** (was 53; +24) |
| MPSCALC | `… AND (summary ~ feedback OR labels in (feedback, user-feedback, in-app-feedback)) AND (created >= W OR updated >= W)` | 2: MPSCALC-194 (feedback-dialog 401 wording, a hardening finding) and MPSCALC-174 (merge comment). Neither is an in-app feedback item | n/a (MPS is excluded) |
| MPSCALC comments | `GET /issue/<key>/comment` on all 66, created ≥ 07:30 | 42, all "Kamil Kreiser". Samples read as seat-written: "BLUF: merged to main in PR #…" (08:09) and "B104 lane E, 2026-10-17. BLUF…" (09:11, 09:23) | n/a |
| HPSM | `project = HPSM AND (created >= W OR updated >= W)` | **0** | `project = HPSM` → **41** (unchanged) |

**Client-human responses:** all 43 in-window Jira comments come from the shared account and read as seat-written. HPSMPOC-241 (the HP answers ticket) was not updated. None of the 9 in-window mails comes from a client human.

### GitHub (`gh api --paginate`, since 2026-10-16T20:30:00Z)

| Repo (gh config) | Commits on main since | Issues+PRs updated since | Open PRs | Open issues (non-PR) | Control: newest main commit |
|---|---|---|---|---|---|
| Reporting_Dashboard_Au (NexusAI) | 0 | 0 | #70 #67 #58 | 0 | `17fc6c51` 10-16T04:16Z |
| vision_datasec-sales-portal (Vision) | 0 | 1 (PR #17, dependabot, 20:53:52Z) | #17 #16 #15 #14 | 0 | `6dbffdf3` 09-28 |
| vision_hpas-quickquote (Vision) | 0 | 1 (PR #10, 20:31:49Z; in the overlap, already counted) | #10 #8 | 0 | `437ab4bc` 10-16T04:07Z |
| Datasec-Security-Composer (Composer) | 0 | 0 | none | 0 | `230f9fab` 10-16T00:56Z |
| HPSM-POC (HPSM-POC) | **1** | 1 (PR #156, merged) | none | 0 | `72073dac` 10-16T22:14Z |
| HPSM-POC-analysis (HPSM-POC) | 0 | 0 | none | 0 | `6f5f0dc5` 10-16T01:52Z |
| MPS-Commercial-Calculator (MPS) | **1** | 1 (PR #73, merged) | none | 0 | `12f8e566` 10-16T21:13Z |

The HPSM-POC and MPS rows show that the "since" filter does see in-window activity. **No GitHub issue was opened on any repo**, so no feedback arrived as an issue.

### Composer carry-forward re-check
- I grepped `1061d219|d477d020` (case-insensitive) in `BACKLOG.md` on **all 78 local branches**: **0 hits**, the same as the last two sweeps. Control: `C-62` on main's BACKLOG gives 3.
- `git log --all --since=2026-10-17T06:00+11:00` in the Composer records repo gives 0. In the code checkout (`2_Project_Files`), the newest ref is `b152/approved-words-and-looks` (10-14).

## 3. Notes for Tuesday (not feedback)

1. **MPS Jira lag: closed.** MPSCALC-147, -105 and -183 each got a "BLUF: merged to main in PR #69 / #71 / #72" comment at 08:09:52-54. The MPS seat also filed MPSCALC-189..212 at 08:06-08:07, and B104 lane E posted updates on MPSCALC-155 and -140 (09:11, 09:23). PR #73 (`12f8e566`, MPSCALC-150/-158) is the commit behind Kam's hosted-deploy ruling (DELTA 203).
2. **HPSM-POC: merge with no Jira trace yet.** PR #156 (`72073dac`, 09:14 AEDT) names HPSMPOC-251, -252, -253, -255, -256 and -258, but `project = HPSMPOC AND updated >= W` → 0 at about 09:34. That is only 20 minutes after the merge, so it may be normal wrap lag. It is the same pattern MPS showed at 07:40; check it at the HPSM-POC wrap.
3. **Vision QuickQuote gate 21 NO GO** on PR #10 @ `3a3399e` (22:27Z). This is round 2 failing gate; it is fleet work, not feedback.
4. **Unticketed items carried forward** (unchanged): Composer `d477d020` (editions lookup, needs Kam); Vision Portal #6 (Social Media Engagement tile; Portal paused); HPSMPOC-242 (an empty placeholder; HPSM-POC excluded).

## 4. Watermarks out
- Mailbox: **2026-10-16T22:35:07Z**.
- Jira: **2026-10-17 09:34 AEDT** (time of the last JQL). A safe value for the next `>=` is `"2026-10-17 09:20"`.
- GitHub: `since=2026-10-16T22:15:00Z` is safe. It catches the PR #156 merge again, as a known item.

## 5. UNMEASURED (same as the earlier sweeps)
- **Every live feedback store** (MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, the NexusAI share, Portal Postgres, the QuickQuote table). Each needs `az`, an app sign-in that writes, or HTTP to a hosted host. "0 new" means 0 reached the mailbox, Jira or GitHub.
- **Who wrote a Jira comment.** The shared "Kamil Kreiser" account cannot tell Kam from a seat. I sampled the in-window comments, and every one read as seat-written; I did not read all 43 in full.
- **HPSM open PRs:** `gh` is not logged in under `HPSM/4_Credentials/.gh-config`.
