# Morning sweep: Datasec projects (2026-10-17)

Run by a read-only sub-agent for Tuesday, about 06:0x-06:3x AEDT on 2026-10-17. "Since yesterday" means since **2026-10-16 12:00 AEDT** (01:00Z). Human responses are counted since 2026-10-15. Follows [[2026-10-16_feedback-sweep-1]] and [[2026-10-16_feedback-sweep-2]].

**What this sweep did not do:** no Jira writes, no git writes, no `az`, no mail sends, no `gh` writes, and **no HTTP of any kind to an app host**. The only network reads were: each project's Jira REST `GET /rest/api/3/search/jql` (paged until `isLast`) and `GET /issue/<key>/comment`, using that project's own `4_Credentials/.env`; read-only `gh api` GETs under each project's own `GH_CONFIG_DIR`; and one AgentMail list call for tuesday-agent@. Git use was `ls-remote`, `log` and `show` only.

## 1. BLUF

| Project | Open total (query → API total) | Agent-actionable | New or changed since 10-16 12:00 | Client-human responses since 10-15 | Open PRs |
|---|---|---|---|---|---|
| **NexusAI** (RD) | **728** (`project = RD AND statusCategory != Done`) | **6 in the seat's queue** (RD-848, RD-801+822 → RD-802, RD-828 s2, RD-837); 309 To Do rows pass a label filter (a heuristic, see 2) | 6 (1 created: RD-848; 5 updated by the RD-846 merge and deploy comments) | **0** | 3 (#58, #67, #70): stale since 10-07/08, CI green |
| **Vision Portal** (VSP) + **QuickQuote** | VSP **16** (`project = VSP AND statusCategory != Done`) | **2** on QuickQuote (PR #10 to gate 20; PR #8 puppeteer 25). Portal 0 (paused, sweep 1) | VSP 0. QuickQuote: v2.36 merged and published (6 commits on main since 01:00Z); PR #10 READY 18:46Z | **0** | Portal 3 Dependabot PRs (gitleaks red on all 3); QuickQuote 2 (#10, #8, all checks green) |
| **HPSM-POC** (HPSMPOC) | **109** (`project = HPSMPOC AND statusCategory != Done`) | **about 33** by label filter (37 rows, less 4 that need a person or a deploy). Top: 251, 252, 256 | 27 updated (26 by the 12:26-12:34 records pass, 9 new tickets 251-259) | **1, relayed:** HP (Terry Dumont) answered 5 of the 9 questions in a mail of 10-16 06:56 AEDT. Kam forwarded it; it is on HPSMPOC-241 | 0 (`HPSM-POC` repo; last PR #155 closed 10-13) |
| **Security Composer** (BACKLOG.md) | **about 98 open rows** of 308 (a classification by the start of each State cell; see 2) | **about 8** candidates, not yet checked against the C-71 "hold" rulings | 0 code commits on GitHub main since 01:00Z. Records: `records/b155` 13:11 AEDT (site gate removed, C-75) | **0** seen (no Jira; no mail) | 0 (last PR #79 merged 10-16 00:56Z) |
| **MPS Calculator** (MPSCALC) | **174 open** (Backlog 174) of 188 (Done 14) | Tuesday manages this one: counts only | 61 changed, of which **53 created** (12:28-12:34 AEDT, the feedback-sweep batch); 0 created after 16:18 | **0** | 0 open; 28 commits on main since 01:00Z (#57-#68) |
| **HPSM** (HPSM) | **25** (Backlog 25) of 41 | **0**: dormant, no app | 0 | 0 | **UNMEASURED**: the project's `gh` config is not logged in |

**Feedback since the sweep 2 watermarks: 0 new items.** Mailbox: 21 messages after 05:14:29Z, all fleet mail, none a feedback notice. Jira: 0 new feedback tickets. RD-840 and RD-841 (Feedback #8 and #9) were touched at 16:19, one minute after the watermark, by the demo-deploy comment. That is not a new item. Composer `1061d219` and `d477d020` still have **no BACKLOG row by id** (78 local branches checked). `1061d219` is covered in substance by row #275 and C-62 ("Policy Designer" rename, deployed). `d477d020` (editions lookup) has no row anywhere.

## 2. Detail per project

### NexusAI (Jira RD, repo `datasecau/Reporting_Dashboard_Au`)

**Open, by status** (`project = RD AND statusCategory != Done`, total 728): To Do 354 · Release Ready 194 · Testing 163 · In Progress 8 · Put on Hold 7 · Declined 2 (Declined sits outside the Done category on this board, so it is counted here). **By priority:** Medium 311 · High 204 · Low 194 · Highest 18 · Lowest 1.

**Main** = `17fc6c51` (ls-remote): PR #86 (RD-846), deployed to the demo as revision 0000100 (from the S99O wrap mail, not re-measured: no app HTTP).

**The seat's next-work queue**, one line each:

| Key | State now | Acceptance (from the ticket) |
|---|---|---|
| RD-848 (Low, To Do, created 10-16 14:41) | No branch on origin (`ls-remote refs/heads/rd-848*` → none) | Drop Dockerfile:74's build-stage `COPY package.json package-lock.json` (already inherited via deps), and add a static guard on every stage: no COPY may copy only files the stage already holds byte-identical. Glob-resolving, so it catches 8de8e5c. Also F-846-2: cite the stage by name, not "(line 22)" |
| RD-801 (Medium, Testing) | READY FOR QA since 10-07 05:10 on `rd-801-feedback-log-injection-s87o` @ `66131135` (ls-remote equal); **no PR open** | CodeQL alerts #155-#158 (js/log-injection, feedback.js) close on merge, with a per-call helper and red-first. Never dismiss (C-190) |
| RD-822 (Medium, Testing) | Same branch, its own commit `686bf53` | Validator `/[ -]/`. Spaced reasons are accepted; LF, CR, TAB, NUL, DEL and ESC are refused. Verify PASS 4317/266 |
| RD-802 (Medium, Testing) | READY FOR QA 10-07 17:20 on `rd-802-provisioning-log-injection-s87o` @ `a103c8e8` (ls-remote equal), stacked on RD-801 (C-199). Gate range `6613113..a103c8e`. No PR | Alerts #154, #159 and #160 close. It merges **after** RD-801, never alone; on an RD-801 fix round it forward-merges |
| RD-828 (Low, Release Ready) | Slice 1 (A-F1 and F-F1) merged in PR #82 → `b2eecdf` on 10-13. **Slice 2 not started** (no branch beyond `rd-828-gate14-cells-s93o` @ `b2eecdf`) | Slice 2 = B-F1 (pin the census to the 16 literal rule strings), C-F1 (an ARM that strips only server.js IP lines), C-P1 (the "count changed" wording), plus the D-F1 and E-F1 cells from the gate 14 report |
| RD-837 (Medium, To Do) | No branch. The ticket says "Do NOT build yet: lane O's tooling queue, after F-821-1" | c57-id-superset.sh links each runner tree to its own install, or prints the resolved proxy-addr path and version beside the failed count. Install per C-63 |

Also new on 10-16: **RD-847** (Low, To Do, 11:47, before the window): the lock tool's BASE is hard-coded to the T9 drive.

**Agent-actionable, up to 10:** RD-848 (Low; filed by Tuesday's TURN, fix shape given); RD-801 + RD-822 → RD-802 (Medium; built, waiting for a QA gate, so the next actor is Tuesday or QA, not Kam); RD-828 slice 2 (Low; cells already specified by gate 14); RD-847 (Low; tooling on the new machine); RD-837 (Medium; queued after F-821-1); RD-836 (High, To Do; risk-conditions POST has no role check; not labelled for a decision); RD-774 (High; CodeQL js/sql-injection simpleDb.js:859); RD-793 (High; data-source mutators have no role check). **Heuristic:** 309 of the 354 To Do rows carry none of `needs-decision`, `kam`, `fleet-activity`, `horizon-2/3`, `blocked` or `marketplace`. That is an upper bound, not a measured count.

**Changed since 10-16 12:00** (`project = RD AND (created >= "2026-10-16 12:00" OR updated >= "2026-10-16 12:00")` → 6): RD-848 created; RD-846, RD-838, RD-839, RD-840 and RD-841 updated 16:14-16:19 by the S99O merge and demo-deploy comments.

**Human responses since 10-15:** 7 RD issues updated since 10-15 00:00, carrying 8 comments. All 8 are by the shared account "Kamil Kreiser", and every one reads as a seat's (S99O) comment. No client-human comment.

**Open PRs** (`gh api repos/.../pulls?state=open`, paginated → 3): #70 `rd-775-readiness-key-s92r` @ `537741ce`; #67 `rd-777-776-validators-s92r` @ `94b288cc`; #58 `rd-761-law-endpoint-policy-s89r` @ `7f1881ea`. On all three the 5 check runs (CodeQL ×4, audit-production-deps) succeeded, and none has a commit status. Last updated 10-07/08, so they are **stale**.

### Vision Sales Portal (Jira VSP, repos `vision_datasec-sales-portal` and `vision_hpas-quickquote`)

**VSP open** (`project = VSP AND statusCategory != Done` → 16): Backlog 16 · High 1 (VSP-76) · Medium 9 · Low 6. Newest update 09-29. **0** created or updated since 10-16 12:00. **0** comments since 10-15. Sweep 1 recorded the portal as paused; that was not re-checked.

**QuickQuote** (its tracker is `Quoting Tool/hpas-quoting-tool/BACKLOG.md`, not Jira): origin/main = `437ab4bc` (10-16 15:07 AEDT, PR #11, v2.36). There have been 6 commits on main since 01:00Z (PRs #7, #9, #11). Open items in BACKLOG were not counted (its "Open" section is narrative, lines 79-449).

**Agent-actionable:** (1) **PR #10** `fix/qq-email-matches-print-2026-10-16` @ `7b952f6e`, READY FOR QA tier 1 (18:46Z mail). The next actor is the QA gate: the gate 20 brief is already in Tuesday's tree, untracked. (2) **PR #8** `fix/qq-puppeteer-25-2026-09-22` @ `4d6ed6ef` (Kam ruled "build now" at 12:41 on 10-16; the amd64 run is timing-bound under emulation). The next step needs Tuesday's call on what proves it. Portal: 0 (paused).

**Open PRs:** Portal (→ 3, all Dependabot): #16 brace-expansion @ `65d26358` (gitleaks **failure**, tests ok); #15 ip-address @ `72e3b171` (gitleaks **failure**, tests ok); #14 qs+express @ `61c43d7f` (gitleaks, test 20 and test 22 all **failure**). QuickQuote (→ 2): #10 @ `7b952f6e` and #8 @ `4d6ed6ef`, 13 of 13 check runs green on each. **No open GitHub issues** on any of the three repos (NexusAI, Portal, QuickQuote).

### HPSM-POC (Jira HPSMPOC, repo `datasecau/HPSM-POC`)

**Open** (`project = HPSMPOC AND statusCategory != Done` → 109): Backlog 106 · In Progress 3. Medium 93 · Low 9 · High 4 · Lowest 3.

**Agent-actionable:** I took the 109 open rows and dropped every row labelled `needs-kam`, `owner-kam`, `awaiting-hp`, `hp-request`, `needs-sme*`, `owner-datasec-sme`, `needs-hp*`, `next-phase`, `sow-deliverable`, `owner-dev-team` or `poc-seed`. That leaves **37**. Four of those still need a person or a deploy: HPSMPOC-204 (`for-kam` wording), HPSMPOC-240 (needs a support contract), HPSMPOC-126 and HPSMPOC-196 (measured at the next hosted deploy). That gives **about 33**. The top 10, newest gate output first:
- HPSMPOC-251 (Medium): imports. An upload's later batches land on a run the pending sweep already failed (B247 T-1/T-0).
- HPSMPOC-252 (Medium): the pending-import sweep ends Faulted on a routine host stop (B247 T-2).
- HPSMPOC-256 (Medium): the BFF form route. A crafted Content-Type boundary bypass (B243 N-3..N-5).
- HPSMPOC-258 (Medium): two Feedback regexes still end in `$` (the HPSMPOC-225 remainder).
- HPSMPOC-254 (Medium): Pkcs advisories. The copy that runs is the .NET shared one (B248).
- HPSMPOC-255 (Medium): deploy-package.py live-check verdict (B243 N-1/N-2/N-7).
- HPSMPOC-253 (Medium): a stale comment at AssessmentModule.cs:122 (B247 N-4).
- HPSMPOC-148 (Medium): mock parity, the lone-surrogate case (B87).
- HPSMPOC-224 (Medium): the hosted demo sends no telemetry (B170 O-1).
- HPSMPOC-98 (Medium): an admin screen for the feedback list.

Kam ruled on 10-16 at 11:4x that HPSM-POC is "NOT frozen, keep working on it now" (Tuesday's daily note 10-16, line 44).

**Changed since 10-16 12:00** (→ 27, all between 12:26 and 12:34 AEDT): new HPSMPOC-251 through 259; 12 closed in the records pass (-88, -95, -127, -134, -159, -225, -229, -238, -239, -243, -244, -247, -250 and others); HPSMPOC-241 (the HP answers); HPSMPOC-91 commented "not closed". **0 after 16:18.**

**Human responses since 10-15:** 21 comments, all by the shared account, all seat-written. **One client response, relayed:** HPSMPOC-241's comment of 10-16 12:28 records that HP answered 5 of the 9 questions (G1-1 export file names are an enhancement request; G1-2 missed scheduled runs are not caught up; …), in Terry Dumont's mail of 10-16 06:56 AEDT, forwarded by Kam at 01:06:25Z. Kam's ruling on it: integration is next-phase, so it is stored and architected but not built (HPSMPOC-259).

**Open PRs:** 0 (→ empty; repo `open_issues_count` 0; the last closed PR is #155, 10-13T21:25Z; pushed_at 10-13). 0 commits on main since 01:00Z. The B250 records work went to `datasecau/HPSM-POC-analysis` (PR #117 per the daily note); I did not query that repo.

### Datasec Security Composer (tracker BACKLOG.md, repo `datasecau/Datasec-Security-Composer`)

The records repo at the project root is **local only (it has no origin)**. Main is `06124b9e` (10-13 09:29). The newest branch is `records/b155` @ `3266142b` (10-16 13:11 AEDT, B155: site gate removed, C-75). Its BACKLOG.md is identical to main's (`git diff --stat main records/b155 -- BACKLOG.md` → empty).

**Open rows:** the BACKLOG has 308 numbered rows (max #318). I classified each row by the first word of its State cell. Rows starting DONE, CLOSED, DEPLOYED, MERGED, FIXED, RULED, SUPERSEDED or COVERED count as closed: **210**. The rest count as open: **98** (58 start "OPEN"; the others are KAM'S CALL ×5, READY FOR REVIEW ×3, DEFERRED ×3 and mixed partial states). This is a text heuristic: some "open" rows are half-deployed, and many open rows carry a C-71 ruling of "(a) Hold". **Count UNVERIFIED.**

**Agent-actionable (candidates, about 8, none cross-checked against C-71):** #273 and #271 (the `problems.ts:13` words, "next rounds per C-64"); #272 (S5 "HPSM" from content; needs a content release, so probably Kam-gated); #315 (Gate B136-F1 Minor, "a ticket for later per Kam's card a"); #291 (DEPLOY.md Route B two-step not built); #178 (an additive CHECK on `last_generate_input_hash`); #152 (an audit_event index); #140 (the token checker's `//` comments, tooling); #84 (an up.sh health race). The large "next round" family (#280-#288, #300-#309) is ruled under C-71 COMP-12/18/19. Read those rulings before calling any of them actionable.

**Changed since 10-16 12:00:** 0 commits on GitHub main since 01:00Z (`gh api commits?since=2026-10-16T01:00:00Z` → 0). The last merge was PR #79 at 00:56Z, just before the window. Records: `records/b155` (13:11 AEDT). **Human responses:** none reachable (no Jira, and no Composer feedback mail in tuesday-agent@).

**Open PRs:** 0 (→ empty; `open_issues_count` 0).

### MPS Commercial Calculator (Jira MPSCALC): counts only

- `project = MPSCALC` → 188: **Backlog 174 · Done 14**. Open by priority: Medium 142 · Low 26 · High 6.
- `… AND (created >= "2026-10-16 12:00" OR updated >= "2026-10-16 12:00")` → 61. `… AND created >= "2026-10-16 12:00"` → 53 (38 at 12:28, 14 at 12:29, 1 at 12:34). `… AND created >= "2026-10-16 16:18"` → 0.
- Comments since 10-15: 53, all by the shared account; 0 client-human.
- Open PRs → 0. Main has 28 commits since 01:00Z, the newest `ec29d51a` (#68, 18:46Z).

### HPSM (Jira HPSM)

`project = HPSM` → 41; open (`statusCategory != Done`) → 25, all Backlog (Medium 22 · Highest 2 · High 1). 0 created or updated since 10-16 12:00, and 0 updated since 10-15. Dormant (SOW-01 built no app). **Open PRs UNMEASURED:** `gh` under `HPSM/4_Credentials/.gh-config` answered "To get started with GitHub CLI, please run: gh auth login".

## 3. Feedback sweep 3

**Watermarks in:** mailbox 2026-10-16T05:14:29Z; Jira 2026-10-16 16:18 AEDT.

### Mailbox (tuesday-agent@agentmail.to)
`GET /v0/inboxes/tuesday-agent@agentmail.to/messages?limit=100`, 1 page, 100 fetched. The oldest fetched was 2026-10-13T07:14Z, so the window is fully covered. **21 messages after 05:14:29Z** (22 counting the watermark message itself), newest **18:58:54Z**. All 21 are fleet mail (`[Datasec/... -> Tuesday]` or `[Wednesday -> ...]`). **0 feedback notices** (no `QuickQuote feedback (`, Portal feedback, MPS or Composer feedback subject). The nearest thing to feedback is Vision's PR #10 (email matches print), which is build work.

### Jira (all JQL in AEDT; W = `"2026-10-16 16:18"`)

| JQL | Total |
|---|---|
| `project = HPSMPOC AND labels = hp-feedback` | 5 (unchanged; newest HPSMPOC-230) |
| `project = HPSMPOC AND (created >= W OR updated >= W)` | 0 |
| `project = RD AND summary ~ "\"Feedback #\""` (control) | 21 |
| `project = RD AND (summary ~ "\"Feedback #\"" OR labels in (feedback, user-feedback)) AND (created >= W OR updated >= W)` | 2: RD-840 and RD-841, updated 16:19 by the demo-deploy comment. **Not new items** (Feedback #8 and #9, now on the demo) |
| `project = RD AND (created >= W OR updated >= W)` | 5 (the same deploy comments; RD-848 was created 14:41, before W) |
| `project = MPSCALC AND (summary ~ feedback OR labels in (feedback, user-feedback, in-app-feedback)) AND (created >= W OR updated >= W)` | 0 |
| `project = MPSCALC AND labels in (feedback, user-feedback, in-app-feedback)` | 0 (MPS uses `feedback-sweep`, per sweep 1) |
| `project = MPSCALC AND created >= W` | 0 |
| `project = HPSM` | 41 (unchanged) |
| `project = VSP AND (summary ~ feedback OR labels in (feedback)) AND created >= -2d` | 0 |

### Composer re-check (sweep 1's two items)
I grepped `1061d219|d477d020` (case-insensitive) in `BACKLOG.md` on **all 78 local branches** of the Composer records repo: **0 hits**. The root file (314 lines) and `_wt_b155rec/BACKLOG.md` also give 0. Positive control: the same file has 31 lines matching `feedback` and 3 matching `C-62`.
- **`1061d219`** ("Policy Designer" rename): no row by id. Its substance is **row #275** ("C-62, the rename to 'Policy Designer' in everything users see", built in PRs #58 and #60), and `CLARIFICATIONS.md:994` cites the id under C-62. In effect it is tracked; only the id is missing from the BACKLOG.
- **`d477d020`** (editions lookup): **no row, no C-number.** It is found only in `Briefs/2026-10-09_B104_SEAT-C_home-width-and-css-feedback.md`, which says it waits for Kam. **Still unticketed.**

### New items
**0.** Unticketed carried forward: Composer `d477d020`; Vision Portal #6 (sweep 1); HPSMPOC-242 (an empty placeholder).

### Watermarks out
- Mailbox: **2026-10-16T18:58:54Z**.
- Jira: **2026-10-17 06:2x AEDT**, the time of this sweep's last JQL. A safe value for the next `>=` is `"2026-10-17 06:00"`.
- Stores: unchanged (nothing was read from any store).

## 4. UNMEASURED

- **Every live feedback store** (MPS Kudu, Composer `pc.feedback_item`, HPSM-POC `poc.feedback_item`, NexusAI share, Portal Postgres, QuickQuote table). Each needs `az`, an app sign-in that writes, or HTTP to a hosted host, and all three are out of bounds. "0 new" means 0 reached the mailbox or Jira.
- **Client-human comments in Jira:** every comment across RD, HPSMPOC and MPSCALC since 10-15 (82 in all) is posted by the one shared "Kamil Kreiser" account, which the seats also use. Kam-as-human and a seat cannot be told apart by author. I read the bodies of the RD and HPSMPOC comments, and all read as seat comments; the MPS bodies were only grepped (2 lines mention Paul, Steve or HP).
- **HPSM open PRs:** `gh` is not logged in under HPSM's config.
- **`datasecau/HPSM-POC-analysis`** (B250 records repo): not queried.
- **Composer open-row count and actionable list:** a text heuristic; not checked against the C-71 rulings.
- **NexusAI agent-actionable beyond the named queue:** 309 is a label-filter upper bound, not a judgement per ticket.
- **QuickQuote BACKLOG open items:** not counted (narrative format).
- **Demo and live state** (NexusAI revision 0000100, QuickQuote v2.36 live): taken from mail and git only, never fetched.
