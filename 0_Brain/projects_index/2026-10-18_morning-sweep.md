# Morning sweep: Datasec feedback delta + ticket sweep (2026-10-18)

A read-only sub-agent (claude-opus-5-5) ran this for Tuesday from **06:00 to 06:07 AEDT on 2026-10-18** (`date`: Sun 18 Oct 2026 06:00:27 AEDT = 2026-10-17T19:00:27Z).

- **Job A** is the feedback delta since [[2026-10-17_rotation-sweep-1515]]. It uses the same method and store map ([[2026-10-16_feedback-sweep-1]] §2). **Window:** mailbox after 2026-10-17T03:54:56Z, Jira `>= "2026-10-17 15:00"` AEDT, GitHub `since=2026-10-17T03:55:00Z`. That runs to about 06:06 AEDT, roughly 15 h.
- **Job B** is the morning ticket sweep under the standing grant of 2026-08-12.

**Instruments, and what I did not do.**
- Jira: each project's own REST `GET /rest/api/3/search/jql`, paged until `isLast`, plus `GET /issue/<key>` and `/issue/<key>/comment`. Credentials came from each project's own `4_Credentials/.env`, read by variable name inside a Python process and never printed.
- GitHub: read-only `gh api --paginate` GETs under each project's own `GH_CONFIG_DIR`.
- git: `for-each-ref`, `log` and `show` only, with no fetch.
- Mail: AgentMail list GETs for tuesday-agent@, using Tuesday's key.
- I made **no HTTP of any kind to an app host, a hosted site or production**, and no Jira, git, gh, mail or az writes.

## 1. BLUF

### 1a. Feedback delta (Job A)

**There are no new feedback items in the window: 0 across all projects. There are no new client-human responses either: 0.**
- The only mail from outside the fleet is one forward from Kam himself. At 04:56:13Z he sent "FYI" with a GitHub code-scanning notice on NexusAI PR #88. That notice is about the CodeQL work on RD-801, not a feedback item.
- In the window, seats created 18 tickets (HPSMPOC-260..273 and MPSCALC-228..231). All were written by seats, and none is a feedback item.

| Project | New feedback items in window | New client-human responses | New tickets created in window | Other activity in window (not feedback) |
|---|---|---|---|---|
| **NexusAI** (RD) | **0** | **0** | **0** | **Main moved `065a0d8f` → `b89c9383` (PR #88, RD-801+822) → `55047f45` (PR #89, RD-802) → `c7ca0ed7` (PR #90, RD-828 s2).** 4 issues updated and 10 comments, all written by the seat. The TURN is complete, and the seat sent a session wrap at 11:04Z |
| **Vision Portal** (VSP) | **0** | **0** | **0** | None. No Jira change, no commits, no issue or PR updated |
| **Vision QuickQuote** | **0** (no `QuickQuote feedback (` mail) | **0** | n/a (tracker is BACKLOG.md) | Vision seat wrap at 18:30:44Z: PR #10 @ `f31720e` "waits only on Kam's ONE publish card (C-20)". Main is unchanged at `437ab4bc` |
| **Security Composer** | **0** | **0** | n/a (tracker is BACKLOG.md) | None. GitHub main is still `230f9fab`. 0 local commits since 15:00. The newest local branch is still `records/b155` |
| **MPS Calculator** (MPSCALC, *excluded*) | not swept (excluded) | **0** | 4 (MPSCALC-228..231, 05:46 on 10-18, seat) | PRs #80, #81, #82 merged; main is now `e6f92a5f`. 8 issues updated and 5 comments, all written by the seat |
| **HPSM-POC** (HPSMPOC, *excluded*) | not swept (excluded) | **0** | 14 (HPSMPOC-260..273, 16:35-16:36, seat, B257) | **The Jira lag from the 15:15 sweep is closed.** HPSMPOC-251..258 were updated at 16:36 with merge comments; six are now Done and -254 is still Backlog. HPSM-POC-analysis PR #118 merged (`2e284455`) |
| **HPSM** (HPSM) | **0** | **0** | **0** | None. GitHub is **UNMEASURED** (`gh` is still not logged in under HPSM's config) |

### 1b. Ticket sweep (Job B)

**The predicate behind every "agent-actionable" count.** A ticket counts if all of these hold:
1. It is not Done (`statusCategory != Done`), paged to `isLast`.
2. It is not an Epic.
3. Its status is To Do, In Progress or Backlog. This excludes Testing and Release Ready, because NexusAI's CLAUDE.md:302 says Kam or a teammate moves tickets out of those states. It also excludes Put on Hold and Declined.
4. It carries none of these labels: `needs-decision`, `needs-kam`, `needs-ruling`, `question-for-kam`, `owner-kam`, `for-kam`, `kam`, `awaiting-hp`, `hp-request`, `hp-clarification`, `needs-hp-content`, `needs-sme-content`, `owner-hp-sponsor`, `owner-datasec-sme`, `blocked*`.
5. It has no open inward "Blocks" link.

The rank order is priority (Highest to Lowest), then key number. **The predicate is mechanical.** Where it lets through something that plainly needs a human, I say so.

| Board | Open (not Done) | Agent-actionable by the predicate | Really workable today | Top 5 (priority, key) | New since 10-17 15:00 |
|---|---|---|---|---|---|
| **NexusAI** (RD) | 733 | **355** (Highest 1, High 48, Medium 165, Low 139, Lowest 2) | Fewer than 355. The top of the list holds vendor, spend and audit items (see the note below the table) | RD-478 (Highest, To Do: remove the remaining VM / local-model code, C-51), RD-20 ‡, RD-21 ‡, RD-28 ‡, RD-50 (High, To Do: repoint Feedback System and Lead Bot off the retired 4.x VM). The next High items with no human dependency: RD-262, RD-386, RD-476, RD-505, RD-506 | **0 created.** Updated: RD-801, -802, -822, -828 (all Release Ready, merged) |
| **Vision Portal** (VSP) | 16 (all Backlog) | 16 by labels | **0.** The 2026-09-29 Vision pause stands for the portal (CLARIFICATIONS C-13, C-17, C-18: "the portal, ATTIO and the rest of the Vision backlog (2026-09-29 pause stands)"). C-12 also parks VSP-72 and VSP-84 | If the pause were lifted: VSP-76 (High: dead client handed on after terminate), VSP-65, VSP-78, VSP-81, VSP-82 (Medium) | 0 |
| **Vision QuickQuote** (BACKLOG.md @ origin/main `437ab4bc`, plus open PRs) | 27 open checkbox items (of 53); PRs #10 and #8 open | **1**: PR #8 (C-19, puppeteer 25 + node 22). It has been READY FOR QA (tier 1) since 2026-10-16T01:56:46Z, and I found no gate verdict in the mailbox. The next step is a QA gate that Tuesday commissions. PR #10 waits on Kam's publish card (C-20), so it is not actionable | 8 of the 27 BACKLOG items need no human input, but all sit under the Vision pause (no commissioning C-number covers them) | If commissioned: the extract-zip advisories (L360 and L762, the same item, being fixed in PR #8), L156 (provider error text on `/healthz`), L101 (BC-F1 cell cannot go red), L134 (empty purge logs nothing), L118 (default close bound has only a regex guard) | 0 new BACKLOG lines on main. One new local branch `backlog/qq-extract-zip-2026-10-16` @ `01c8d7f` (10-17 10:19, G21-F3 ticketed) |
| **MPS Calculator** (MPSCALC, awareness) | 217 (all Backlog) | **164** (High 6, Medium 136, Low 22). Of these, 43 are `spec-seed` epic-style seed tasks, which leaves 121 | Likely fewer: MPSCALC-141 says "decide each" | MPSCALC-140, -141, -142, -148, -150 (all High, from Paul's review of 10-16) | **MPSCALC-231** (lane-e, importer rule text) is actionable. MPSCALC-228, -229 and -230 are `needs-ruling` |
| **HPSM-POC** (HPSMPOC, awareness) | 117 (114 Backlog, 3 In Progress) | **72** (High 1, Medium 60, Low 8, Lowest 3). Of these, 18 are `poc-seed-2026-09-23` SOW seeds (17 of them `owner-dev-team`), which leaves 54 | Fewer: HPSMPOC-100 is a client follow-up, and HPSMPOC-87 is a draft for Kam | HPSMPOC-87 (High, In Progress: C-30 customer questions, DRAFT for Kam), then the seeds -11, -12, -13, -14. The first non-seed items are -98, -99, -100, -109, -117 | **12 actionable new:** HPSMPOC-260..266 and -269..273 (B257 filings from gates B252, B255 and B256). Also new, but labelled `needs-kam`: -267 and -268 |

‡ RD-20 (SOC 2 / ISO vendor), RD-21 (CREST pen test) and RD-28 (SOC 2 Type II audit) pass the label predicate. Each needs a vendor and spend, which is approval-class, so they are **not agent work**.

**NexusAI blockers named at the previous boot:**

| Ticket | State | What it needs |
|---|---|---|
| **RD-460** (Highest, Testing; `blocker`, `needs-decision`) | Last updated 09-28 | **Kam has two decisions:** (1) the monetisation model, because Solution templates cannot be bought through the Marketplace, so charging needs a Container (AKS), SaaS or VM offer; (2) approval of a dedicated anonymous-pull Standard ACR (about US$20/month), with the image push being Kam's. **It also needs the release of the queued C-170 package merge.** Gate batch-5b said GO WITH FINDINGS on `be0fe37` on 09-28, "QUEUED, not released". GitHub compare `be0fe37...c7ca0ed7` gives `diverged` (behind 1), so that commit is not in main. That fits with RD-505 and RD-506, which close on that merge, both still being To Do |
| **RD-361** (Highest, Release Ready; `blocker`) | Last updated 09-29 | The code is on the demo since 2026-09-14 (`c469ae9`). It needs **Kam's board call**: move demo-deployed tickets to Done now, or at a Marketplace release. It blocks RD-13 (DEV offer and $0 test purchase). The related RD-368 (SEC-01 remediation 3) is To Do and `needs-decision` |
| **RD-641** (High, Release Ready; `blocker`) | Last updated 09-23 | **Fixed.** Two consecutive green CI Builds on 09-23 (`34f11f4` and `0677388`), with the known failing set empty. It needs only the Release Ready → Done move, which belongs to Kam or a teammate (CLAUDE.md:302). There is no agent work left |

## 2. Evidence and controls

### Mailbox (tuesday-agent@agentmail.to)
- `GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100` returned 1 page of 100 messages. The oldest was 2026-10-16T03:14:57Z, so the window is fully covered; the newest was **2026-10-17T18:30:44Z**.
- **18 messages fall after 03:54:56Z:**
  - 11 from `coagent@`: NexusAI-O QUESTION x3, READY x3, MERGED x3, and Session wrap 10-17; Vision Session wrap 10-18.
  - 6 from `tuesday-agent@`: Tuesday's ANSWERs.
  - **1 from `kamil.kreiser@datasec.com.au`** (Kam): "Fw: [datasecau/Reporting_Dashboard_Au] RD-801+RD-822 … (PR #88)". Its preview reads "FYI … From: github-advanced-security[bot]". This is Kam, not a client human, and the notice concerns CodeQL work, not feedback.
- **0 feedback notices** and **0 client-human senders** in the window.
- **Control 1 (continuity):** the first message after the watermark is 04:56:13Z. The last one counted by the 15:15 sweep was 03:54:56Z, and nothing in between was dropped (same call, same page).
- **Control 2 (the instrument sees a feedback notice):** I paged back 8 pages (800 messages, to 10-05T11:28Z) with a subject match on "feedback". It found `QuickQuote feedback (feature)` from the HPAM Quoting Agent at **2026-10-09T16:51:40Z**, the known C-14 CAD item, plus 7 fleet mails. So the instrument fires.

### Jira (JQL in AEDT; W = `"2026-10-17 15:00"`; every count paged to `isLast`; last JQL at about 06:05 on 10-18)

| Project | JQL | Total | Control |
|---|---|---|---|
| RD | `project = RD AND (created >= W OR updated >= W)` | **4**: RD-801 (18:29), RD-802 (19:52), RD-822 (18:29), RD-828 (22:02) | The same query finds 4 in-window changes, so it sees changes |
| RD | `… summary ~ "\"Feedback #\"" AND (created >= W OR updated >= W)` | 2: RD-801 and RD-822. Both are fuzzy matches on "feedback" (log injection in `feedback.js`; a coordinator-action validator). Neither is a `Feedback #N` item | `project = RD AND summary ~ "\"Feedback #\""` → **21** (unchanged) |
| RD | `project = RD AND created >= W` | **0** | `created >= "2026-10-16 12:00"` → 7 (unchanged from 15:15) |
| RD | `labels in (feedback, user-feedback)` | 5 (unchanged) | n/a |
| RD comments | `GET /issue/<key>/comment` on all 4, created ≥ 15:00 | **10**, all by "Kamil Kreiser" (shared account). I read the opening of each; every one is written by the seat ("S100O, TURN step 2…", "MERGED (S100O…", "READY for Tuesday's source review") | n/a |
| VSP | `project = VSP AND (created >= W OR updated >= W)` | **0** | `statusCategory != Done` → **16** (unchanged) |
| HPSMPOC | `project = HPSMPOC AND (created >= W OR updated >= W)` | **21** (14 created, -260..273; 7 updated, -251..258) | `project = HPSMPOC` → 273 (was 259; +14) |
| HPSMPOC | `labels = hp-feedback` / `… AND created >= W` | 5 / **0** | The newest is still HPSMPOC-230. HPSMPOC-241 (the HP answers ticket) was last updated 10-16 12:34, so no HP response arrived there |
| HPSMPOC | `labels = feedback AND (created >= W OR updated >= W)` | 2: -260 and -265. These are seat-written gate findings about the feedback form route, not in-app feedback | n/a |
| HPSMPOC comments | on all 21 plus -241, created ≥ 15:00 | **7** (-251..258), all opening "BLUF: merged as datasecau/HPSM-POC#156/#157", written by the seat | n/a |
| MPSCALC | `project = MPSCALC AND (created >= W OR updated >= W)` | **8**: -194, -203, -213, -214 (updated 05:47 on 10-18); -228..231 (created 05:46) | `created >= "2026-10-16 12:00"` → **96** (was 92; +4) |
| MPSCALC | feedback labels / `summary ~ feedback` in the window | 0 / 1 (MPSCALC-194, a merged hardening item, not in-app feedback) | n/a (MPS is excluded) |
| MPSCALC comments | on all 8, created ≥ 15:00 | **5**, all "BLUF: merged to main in PR #…" or "three non-blocking items from gate B170", written by the seat | n/a |
| HPSM | `project = HPSM AND (created >= W OR updated >= W)` | **0** | `project = HPSM` → **41** (unchanged) |

**Client-human responses:** 0. All 22 in-window Jira comments come from the shared account and read as written by seats. I read the opening, about 300 characters, of each.

### GitHub (`gh api --paginate`, since 2026-10-17T03:55:00Z)

| Repo (gh config) | Commits on main since | Issues+PRs updated since | Open PRs | Open issues (non-PR) | Control: main HEAD |
|---|---|---|---|---|---|
| Reporting_Dashboard_Au (NexusAI) | **5** (`a1742b38` `b89c9383` `62a6fd87` `55047f45` `c7ca0ed7`) | 3 (PRs #88 #89 #90, merged) | #70 #67 #58 | 0 | `c7ca0ed7` 10-17T08:56Z |
| vision_datasec-sales-portal (Vision) | 0 | 0 | #17 #16 #15 #14 (Dependabot) | 0 | `6dbffdf3` 09-28 |
| vision_hpas-quickquote (Vision) | 0 | 0 | #10 #8 | 0 | `437ab4bc` 10-16T04:07Z |
| Datasec-Security-Composer (Composer) | 0 | 0 | none | 0 | `230f9fab` 10-16T00:56Z |
| HPSM-POC (HPSM-POC) | 1 (`787d1590`, known from 15:15) | 1 (PR #157, known) | none | 0 | `787d1590` 10-17T04:03Z |
| HPSM-POC-analysis (HPSM-POC) | **1** (`2e284455`) | 1 (PR #118, merged) | none | 0 | `2e284455` 10-17T05:42Z |
| MPS-Commercial-Calculator (MPS) | 4 (`1e8a738f` known; `b8ea9027` `cfe376d5` `e6f92a5f`) | 4 (PR #79 known; #80 #81 #82) | none | 0 | `e6f92a5f` 10-17T06:16Z |

The re-catch of HPSM-POC PR #157 and MPS PR #79, which the 15:15 sweep had already counted, shows the `since` filter sees activity at the window edge. **No GitHub issue was opened on any repo**, so no feedback arrived as an issue.

### Composer carry-forward re-check
- I grepped `1061d219|d477d020` in `BACKLOG.md` on **all 78 local branches** (`git show <branch>:BACKLOG.md`): **0 hits**, the same as the last four sweeps. Control: `C-62` on main's BACKLOG gives 3.
- `git log --all --since=2026-10-17T15:00+11:00` gives 0 in the records repo and 0 in `2_Project_Files`.

### Ticket sweep instruments (Job B)
- `project = <P> AND statusCategory != Done ORDER BY key`, paged to `isLast`. It returned RD 733, VSP 16, MPSCALC 217 and HPSMPOC 117. The classification ran over the full sets saved locally.
- **RD status mix:** To Do 357, Testing 160, Release Ready 199, In Progress 8, Put on Hold 7, Declined 2.
- **RD exclusions:** 3 epics, 368 by status, 5 by gating label, 2 by an open Blocks link (RD-13 and RD-550).
- **Control (the gate filter fires):** RD has 12 open tickets labelled `needs-decision`; 5 of them are in an actionable status, and those 5 are excluded. MPSCALC excludes 38 by label (`needs-ruling` 21, `question-for-kam` 18) and HPSMPOC excludes 36 (for example `needs-kam` 14, `awaiting-hp` 9). So the label filter fires.
- **QuickQuote:** I parsed `git show origin/main:BACKLOG.md` (origin/main = `437ab4bc`, the same as GitHub's HEAD). It has 53 checkbox items: 27 open and 26 done. Open items by section: Open 15, Stage 3 go-live 5, Housekeeping 3, Open decisions with Kam 2, item 17 1, Kam's review round 1.
  - I classified them by reading each "Why deferred" line. 14 need Kam (a pricing, wording or publish call, Owner grant or ruling), 1 is not reachable (L626, Will's disk), 4 are deploy-side or stale (L591, L624, and L340: "v2.20 not deployed", but the live site has since moved past v2.20), and 8 need no human input.
  - The local `main` (`8b29136`) is behind origin/main and was not used.
- **Vision pause evidence:** `1_Project_Definition/CLARIFICATIONS.md` lines 104-106, 137 and 143, and `5_Project_History/history.md:2189` ("Portal/ATTIO/backlog remain paused since 2026-09-29 (C-13)").

## 3. Notes for Tuesday (not feedback)

1. **QuickQuote PR #8 (C-19) has had no QA gate for about 2 days.** It has been READY FOR QA tier 1 since 2026-10-16T01:56:46Z, and I found no gate verdict mail in the 8 pages read. It is the only QuickQuote item that is agent-actionable now, and the next move (commissioning the gate) is Tuesday's. A publish would still be Kam's separate tap.
2. **The HPSM-POC Jira lag is closed.** At 16:36 the seat posted merge comments on HPSMPOC-251..258 and moved six to Done. **HPSMPOC-254 is still in Backlog** although its comment says PR #157 merged; check whether that is deliberate (for example, waiting for a deploy). The seat also filed 14 B257 tickets; -267 and -268 are `needs-kam`.
3. **The NexusAI TURN is complete.** Three fast-forward merges took main to `c7ca0ed7`, deploy-demo was SKIPPED each time, and the seat wrapped at 11:04Z. There is no open NexusAI-O mail.
4. **RD-460's queued C-170 package merge is still not on main** (12 days after its gate). RD-361 and RD-641 sit in Release Ready, waiting only on Kam's board moves. If Kam wants the blockers cleared, all three can go on one card.
5. **MPS:** PRs #80, #81 and #82 merged; main is now `e6f92a5f`. MPSCALC-228..230 (from B171) are `needs-ruling` and need Kam's cards.
6. **Unticketed items carried forward** (unchanged): Composer `d477d020` (editions lookup, needs Kam); Vision Portal #6 (Social Media Engagement tile; Portal paused); HPSMPOC-242 (an empty placeholder; HPSM-POC excluded).

## 4. Watermarks out
- Mailbox: **2026-10-17T18:30:44Z** (the Vision session wrap).
- Jira: the last JQL ran at about **2026-10-18 06:05 AEDT**. The newest in-window change is MPSCALC 05:47. A safe value for the next `>=` is `"2026-10-18 05:45"`.
- GitHub: `since=2026-10-17T18:55:00Z` is safe. The newest activity seen was 10:02:57Z (NexusAI PR #90).

## 5. UNMEASURED
- **Every live feedback store** (MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, the NexusAI share, Portal Postgres, the QuickQuote table). Each needs `az`, an app sign-in that writes, or HTTP to a hosted host. "0 new" means 0 reached the mailbox, Jira or GitHub.
- **Who wrote a Jira comment.** The shared "Kamil Kreiser" account cannot tell Kam from a seat. I read the opening of all 22 in-window comments, not every full body.
- **HPSM GitHub:** `gh` is not logged in under `HPSM/4_Credentials/.gh-config`.
- **The body of Kam's forwarded mail** (04:56:13Z). Only the list preview was read, because the bound was list GETs only.
- **Whether RD-460's package content landed on main under another SHA.** Only the ancestry of `be0fe37` was checked; the To Do status of RD-505 and RD-506 suggests it did not.
- **Whether "agent-actionable" tickets are really workable.** The counts are label and status predicates. Ticket bodies were read only for the top items and the three blockers; there may be more hidden human dependencies like RD-20, -21 and -28.
- **QuickQuote PR #8's gate state** outside the mailbox (for example, a gate report in the Testing Agent tree). I did not read that tree.
