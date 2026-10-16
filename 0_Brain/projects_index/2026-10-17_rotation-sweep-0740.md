# Rotation sweep: Datasec feedback delta (2026-10-17 07:40)

A read-only sub-agent ran this for Tuesday at **07:40-07:50 AEDT on 2026-10-17** (`date`: Sat 17 Oct 2026 07:39:54 AEDT = 20:39:54Z). It is the delta since [[2026-10-17_morning-sweep]]. **Window: 2026-10-17 06:00 AEDT (2026-10-16T19:00Z) to about 07:45 AEDT (20:45Z)**, roughly 1 h 45 min. I used the same method and store map as [[2026-10-16_feedback-sweep-1]].

**Instruments, and what I did not do:** I made each project's own Jira REST `GET /rest/api/3/search/jql` calls, paged until `isLast`, plus `GET /issue/<key>/comment`. Each used that project's own `4_Credentials/.env`, read by variable name inside a Python process and never printed. I made read-only `gh api --paginate` GETs under each project's own `GH_CONFIG_DIR`, and used `git for-each-ref`, `log`, `show` and `ls-remote` only. I made AgentMail list GETs for tuesday-agent@ with Tuesday's own key. I made **no HTTP of any kind to an app host or a production host**, and no Jira, git, gh, mail or az writes.

## 1. BLUF

**No new feedback items in the window: 0 across all projects.** No new client-human responses, including the excluded projects. No new tickets were created by agents in the window.

| Project | New feedback items in window | New client-human responses | New tickets created in window | Other activity in window (not feedback) |
|---|---|---|---|---|
| **NexusAI** (RD) | **0** | **0** | **0** | RD-848 went to Testing at 07:22. It got 2 seat comments from S100O (06:33 start; 07:22 READY FOR GATE @ `065a0d8f`). Main is unchanged at `17fc6c51` |
| **Vision Portal** (VSP) | **0** | **0** | **0** | None (no Jira change, no commits, no issue or PR updates) |
| **Vision QuickQuote** | **0** (no `QuickQuote feedback (` mail) | **0** | n/a (BACKLOG tracker) | PR #10 round 2 pushed (updated 20:31:49Z; READY FOR QA @ `3a3399e` per mail 20:32Z) after the gate 20 NO GO (20:15Z). Main is unchanged at `437ab4bc` |
| **Security Composer** | **0** | **0** | n/a (BACKLOG tracker) | None. GitHub main is `230f9fab` (PR #79, 10-16 00:56Z). The newest records branch is still `records/b155` (10-16 13:11) |
| **MPS Calculator** (MPSCALC, *excluded*) | not swept (excluded) | **0** | **0** | 4 merges to main: #69 (MPSCALC-147 r2), #70 (Pkcs B156 F-1), #71 (MPSCALC-105), #72 (MPSCALC-183), 19:51-20:13Z. **Jira not updated for them** (see 3) |
| **HPSM-POC** (HPSMPOC, *excluded*) | not swept (excluded) | **0** | **0** | None. HPSM-POC and HPSM-POC-analysis: 0 commits, 0 issue or PR updates |
| **HPSM** (HPSM) | **0** | **0** | **0** | None. Open PRs **UNMEASURED** (`gh` is not logged in under HPSM's config, as in the morning sweep) |

There is no per-item section below, because the window holds no new feedback item. Section 2 gives the controls that prove each instrument could have seen one.

## 2. Evidence and controls

### Mailbox (tuesday-agent@agentmail.to)
- `GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`: 1 page, 100 fetched. The oldest fetched was 2026-10-13T12:08:40Z, so the window is fully covered. The newest was 2026-10-16T20:32:15Z.
- **11 messages ≥ 19:00Z.** All 11 are fleet mail: the NexusAI-O successor brief, plan Q/A, STATUS and READY FOR GATE; the Vision gate 20 Q/A, NO GO verdict, ROUND 2 and READY FOR QA; and an MPS B163 QUESTION. **0 feedback notices.** Across all 100 fetched, 1 subject contains "feedback": the MPS QUESTION about the MPSCALC-174 rate limit, 10-16 02:00Z, which is fleet mail and falls before the window.
- **Control 1 (continuity):** the newest message before the window is 2026-10-16T18:58:54Z (`[Datasec/MPS Commercial Calculator -> Tuesday] B104 lane E…`). That equals the morning sweep's outgoing mailbox watermark exactly.
- **Control 2 (the instrument sees a feedback notice):** I paged back 3 pages (300 messages, to 10-07T22:18Z) with the same call. It found `QuickQuote feedback (feature) from john.spears@datasec.com.au` at **2026-10-09T16:51:40Z**, the known CAD-currency item (C-14).

### Jira (JQL in AEDT; W = `"2026-10-17 06:00"`; every count paged to `isLast`)

| Project | JQL | Total | Control (a query known to hit) |
|---|---|---|---|
| RD | `project = RD AND (created >= W OR updated >= W)` | **1**: RD-848, updated 07:22 (seat comments; created 10-16 14:41) | This same query caught RD-848's 07:22 update, so it sees in-window changes |
| RD | `project = RD AND summary ~ "\"Feedback #\"" AND (created >= W OR updated >= W)` | **0** | `project = RD AND summary ~ "\"Feedback #\""` → **21** (same as the morning sweep); newest RD-842 (Feedback #10) |
| RD | `project = RD AND labels in (feedback, user-feedback)` | 5 (RD-400, 401, 840, 841, 842; no change) | n/a |
| RD | `project = RD AND created >= "2026-10-16 12:00"` | 1 (RD-848) | n/a |
| RD-848 comments | `GET /issue/RD-848/comment`, created ≥ 19:00Z | 2 of 2, both "Kamil Kreiser" (the shared account), both seat-written (S100O) | n/a |
| VSP | `project = VSP AND (created >= W OR updated >= W)` | **0** | `project = VSP AND statusCategory != Done` → **16** (same as the morning sweep); newest update 09-29 (VSP-80/86) |
| HPSMPOC | `project = HPSMPOC AND (created >= W OR updated >= W)` | **0** | `labels = hp-feedback` → **5** (newest HPSMPOC-230); `updated >= "2026-10-16 12:00"` → **27** (same as the morning sweep) |
| MPSCALC | `project = MPSCALC AND (created >= W OR updated >= W)` | **0** | `created >= "2026-10-16 12:00"` → **53** (same as the morning sweep) |
| MPSCALC | `… AND (summary ~ feedback OR labels in (feedback, user-feedback, in-app-feedback)) AND (created >= W OR updated >= W)` | **0** | as above |
| HPSM | `project = HPSM AND (created >= W OR updated >= W)` | **0** | `project = HPSM` → **41** (unchanged) |

**Client-human responses:** the only Jira comments in the window are the 2 on RD-848, and both come from seats. HPSMPOC-241 (the HP answers ticket) was not updated in the window. None of the 11 in-window mails comes from a client human; all are from `tuesday-agent@` or `coagent@`.

### GitHub (`gh api --paginate`, since 2026-10-16T19:00:00Z)

| Repo (gh config) | Commits on main since | Issues+PRs updated since | Open PRs | Open issues (non-PR) | Control: newest main commit |
|---|---|---|---|---|---|
| Reporting_Dashboard_Au (NexusAI) | 0 | 0 | #70 #67 #58 | 0 | `17fc6c51` 10-16T04:16Z |
| vision_datasec-sales-portal (Vision) | 0 | 0 | #16 #15 #14 | 0 | `6dbffdf3` 09-28 |
| vision_hpas-quickquote (Vision) | 0 | 1 (PR #10, 20:31:49Z) | #10 #8 | 0 | `437ab4bc` 10-16T04:07Z |
| Datasec-Security-Composer (Composer) | 0 | 0 | none | 0 | `230f9fab` 10-16T00:56Z |
| HPSM-POC (HPSM-POC) | 0 | 0 | none | 0 | `d916baf7` 10-13T21:25Z |
| HPSM-POC-analysis (HPSM-POC) | 0 | 0 | n/a | n/a | `6f5f0dc5` 10-16T01:52Z |
| MPS-Commercial-Calculator (MPS) | **4** | 4 (PRs #69-#72, all merged) | none | 0 | `798fe984` 10-16T20:13Z |

The MPS row shows that the "since" filter does see in-window activity. **No GitHub issue was opened on any repo**, so no feedback arrived as an issue.

### Composer carry-forward re-check
- I grepped `1061d219|d477d020` (case-insensitive) in `BACKLOG.md` on **all 78 local branches**: **0 hits**, the same as the morning sweep. Control: `C-62` on main's BACKLOG gives 3.
- The records repo has had 0 commits on any branch since 19:00Z.

## 3. Notes for Tuesday (not feedback)

1. **MPS: 4 merges, no Jira trace.** MPSCALC-147, -105 and -183 were merged by PRs #69, #71 and #72 (19:51-20:13Z), plus a Pkcs fix (#70, B156 F-1). Yet `project = MPSCALC AND updated >= W` → 0. Those tickets have no merge comment and no status move. This could be a records lag in the MPS seat's wrap, or the seat may not write to Jira by design (MPS-9). It is worth a check at the MPS wrap.
2. **Unticketed items carried forward** (unchanged from the morning sweep): Composer `d477d020` (editions lookup, needs Kam); Vision Portal #6 (Social Media Engagement tile; Portal paused); HPSMPOC-242 (an empty placeholder; HPSM-POC excluded).

## 4. Watermarks out
- Mailbox: **2026-10-16T20:32:15Z**.
- Jira: **2026-10-17 07:4x AEDT** (time of the last JQL). A safe value for the next `>=` is `"2026-10-17 07:30"`.
- GitHub: `since=2026-10-16T20:30:00Z` is safe.

## 5. UNMEASURED (same as the morning sweep)
- **Every live feedback store** (MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, the NexusAI share, Portal Postgres, the QuickQuote table). Each needs `az`, an app sign-in that writes, or HTTP to a hosted host. "0 new" means 0 reached the mailbox, Jira or GitHub.
- **Who wrote a Jira comment.** The shared "Kamil Kreiser" account cannot tell Kam from a seat. The 2 in-window comments read as seat-written (S100O).
- **HPSM open PRs:** `gh` is not logged in under `HPSM/4_Credentials/.gh-config`.
