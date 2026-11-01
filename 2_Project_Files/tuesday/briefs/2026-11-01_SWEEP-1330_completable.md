# SWEEP 1330 2026-11-01: what can be finished next (read-only; MPSCALC / PCOMP / HPSMPOC / RD, plus ATTIO)

## BLUF
- All four of SWEEP-0500's firm lanes are **confirmed landed at source**: MPS #135 (`5c64a442`, MPSCALC-255 Done), HPSM-POC #269 + #270 (`a3a06b9a`), Composer #107 + #108 (`6e69886d`), NexusAI #147 + records #148 (`89375808`). MPS records moved 61 tickets to Done since 05:05 (37 to 98).
- **5 firm lanes, ranked:** (1) MPS **MPSCALC-256 purchase half** (M, Opus); (2) NexusAI **RD-913** high-advisory lock fix (S, Sonnet; closing it fully needs a ruling on the moderates); (3) NexusAI **RD-912** clean the remaining roster reads (S, Sonnet); (4) MPS **MPSCALC-355** walk-cap test rows, measure first (M, test-only); (5) Composer **PCOMP-98** cross-line scanner context (L, test-only, needs the CI image's bash 5.2).
- **HPSM-POC has no firm lane.** Its Done rule needs a deploy, and the open HPSM work is waiting on rulings: deploy `a3a06b9a` (#269/#270) to UAT, whether a UAT-only deploy counts as Done (13 deployed keys sit in Backlog), and which fix HPSMPOC-428 gets. HPSMPOC-405 is first alternate.
- **ATTIO has a Jira board** (30 issues, max key 31). It has no completable lane: every open item is a [KAM] item, a human pilot, a product mapping (ATTIO-31), or off-limits (ATTIO-29, B1042). Its GitHub could not be read from this machine (see UNMEASURED).

Measured Sun 1 Nov 2026, 13:30 to 13:36 AEDT. This sweep is a delta against `2026-11-01_SWEEP-0500_completable.md`. The cutoff for "new since" is **2026-11-01 05:05 AEDT = 2026-10-31T18:05Z**, the time that sweep finished measuring.

How it was measured:
- Jira was read with GET only, through the urllib reader that reads each project's own `4_Credentials/.env` inside the process. That reader is SWEEP-0500's `fetch2.py`, copied to `/private/tmp/claude-501/-Volumes-Laptop-DEV-TUESDAY/f8947a38-04ac-46b8-96f3-ceebf0948b77/scratchpad/sweep1330/fetch.py`. Its JQL is `project = <KEY> AND ( created >= -3650d )`, with the parentheses. No token was printed.
- GitHub was read with `gh api -X GET`, each call under that project's own `GH_CONFIG_DIR`. Repo trees come from `git/trees/<main sha>?recursive=1`, with `truncated` false.
- Local git use was read verbs with `--no-optional-locks` only (log, config, one ls-remote).
- There was no HTTP to any hosted site and no read of the decision store. This file is the only thing written.

## Controls (each one printed by the command that produced the count)

- **Board totals equal the highest key**, with 0 duplicates, 0 truncated comment sets and 0 keys from another project:
  - MPSCALC 356, max 356, unique 356.
  - PCOMP 115, max 115, unique 115.
  - HPSMPOC 428, max 428, unique 428 (it was 426).
  - RD 909, max 913, unique 909, with 2 truncated comment sets. The gap of 4 is the same as at 05:00 (RD-1, -2, -39, -44).
  - ATTIO 30, max 31, unique 30, with ATTIO-1 missing. The probe `project = ATTIO AND ( text ~ "zzqxnonexist" )` returns 0, and the full JQL returns rows.
- **Status sums add up to the totals:**
  - MPSCALC: 258 Backlog + 98 Done = 356. At 05:00 it was 319 + 37, so +61 Done. The 61 are records B1019 (28), B1021 (30), B1024 (1, MPSCALC-255) and B1026 (2, MPSCALC-252/-259). They are listed in root git log `89522e1`, `a9d53a0`, `a36f4bf` and `76f1806`.
  - PCOMP: 93 + 22 = 115. No change, because B1041 had not yet written.
  - HPSMPOC: 243 Done + 182 Backlog + 3 In Progress = 428.
  - RD: 365 To Do + 206 Testing + 199 Release Ready + 120 Done + 10 In Progress + 7 Put on Hold + 2 Declined = 909. RD-910 moved to Testing; RD-912 and RD-913 are new.
  - ATTIO: 14 To Do + 13 Done + 2 In Review + 1 In Progress = 30.
- **The cutoff is checked in code:** `p('2026-11-01T05:05:00.000+1100')==CUT`, and `05:04:59` sorts before it. Either assert would stop the run if it were wrong. Timestamps are parsed, never compared as text.
- **Delta since the cutoff (parsed):**
  - MPSCALC: 0 new, 80 updated, 80 new comments. Regex over the 80: `Recorded; not moved` 19, `moved to Done` 61, control `zzqxnone` 0. The 19 held keys are 27, 28, 34, 150, 160, 189, 196, 198, 215, 217, 233, 236, 244, 245, 297, 306, 316, 324 and 325.
  - PCOMP: 0 new, 0 updated, 0 comments. This zero is checked by the same code finding 80 on MPS, and by the cutoff assert.
  - HPSMPOC: 2 new (HPSMPOC-427, -428), 16 updated, 16 new comments. 13 of them are the "UAT now runs 77c3132e" deploy comment at 12:57.
  - RD: 2 new (RD-912, -913), 3 updated, 1 new comment (RD-910 landing).
  - ATTIO: 0 new, 0 updated.
- **404 control:** `pulls/99999` returns 404 on MPS, Composer, HPSM-POC, HPSM-POC-analysis and NexusAI.
- **Open-PR zeros:** the same `gh` call lists 2 open PRs on MPS and 4 on Composer. The closed list returns 5 rows on HPSM-POC, the analysis repo and NexusAI. So their 0 open PRs are real.
- **Model ids:** `models_latest.json` checked 2026-11-01 13:27:30: opus `claude-opus-5-5`, sonnet `claude-sonnet-5-5`.

Mains, read with `git/ref/heads/main`:
- MPS `5c64a442` (#135, 2026-10-31T19:57:38Z).
- Composer `6e69886d` (#108, 2026-11-01T01:14:43Z; #107 `c8eba7f6` before it).
- HPSM-POC `a3a06b9a` (#270, 00:59:14Z; #269 `1f4bf7bc`).
- HPSM-POC-analysis `e0c9bb87` (#163, B1040: C-260, C-261).
- NexusAI `89375808` (#148 records; #147 `88144175`).
- attio: UNMEASURED (see section 7).

Live panes: `tmux list-panes -a -F '#{session_name} ...'` at 13:35 printed three `fleet main zsh` lines and nothing else. That is not the frame SWEEP-0500 printed (named panes), so which seats are live is UNMEASURED here. The in-flight seats below are RELAYED from the task and the briefs folder: B1041 kit and report present, and no B1042 kit filed yet.

## Done rules, checked at source (unchanged since 05:00 unless said)
- **MPS:** C-79 (`CLARIFICATIONS.md:1712`): merged to main AND every Done-when clause MET. The root repo has no remote, so it was read locally. Its log since the cutoff shows 5 records commits and 0 C-entries ("0 C-entries" in each subject).
- **Composer:** C-111 (3), coordinator practice: merged to main, not deployed. The highest heading in the local root file is C-114 (line 2105). C-115 and C-116 belong to B1041 (in flight).
- **HPSM-POC:** "Done means merged, gated and deployed" (analysis `CLARIFICATIONS.md:1904`, quoted again in C-260/C-261 at origin `e0c9bb87`). C-260 leaves "whether Done applies to a UAT-only deploy" **open**.

## The lanes, ranked (5 firm)

OFF LIMITS (relayed, not proposed):
- B1041: Composer records, PCOMP-102/-112 moves, C-115/C-116, the B1037-1/-2/-3 tickets and row B1038-1.
- B1042: ATTIO-29 records.
- HPSMPOC-428: wake-time 500 (assessed in section 3 only).
- PCOMP-44: HELD by the product owner's 2026-11-01 ruling until renderers exist.

None of the five firm lanes writes to the Composer root records repo, to Jira PCOMP, or to ATTIO.

### 1. MPS: MPSCALC-256, purchase half (annual figures and projection breakdown on the purchase result). Size M.
- **Done-when (ticket's own):** "The result carries monthly, annual and contract projections for pages, click cost, managed-service cost, click revenue, service revenue and recurring GP; annual equals monthly times twelve exactly; register row and red-first test; existing totals unchanged." Clause 1a (the rental half) was MET by MPS #133. Clause **1b (purchase) is NOT MET** (B1004 record, comment 40383: "the purchase half waits behind MPSCALC-255").
- **Why now:** MPSCALC-255 is Done (comment at 07:29: "MPS #135, squash 5c64a442 ... equal to code main"). B1015's kit line 14 names this as the lane that "follows this lane and is OUT".
- **Not built yet:** at `5c64a442`, `annual` gives 0 hits in PurchaseResult.cs (276 lines) and PurchaseCalculator.cs (961). `projection` / `RecurringProjection` also gives 0 in both. Positive controls from the same files: `monthly` gives 12 in PurchaseResult.cs, `ManagedService` gives 9 and 12, and `FleetQuantity` gives 1 and 6. The rental model to mirror is ENGINE.md:41 (R-30, `PortfolioResult.Projection`, six measures, Monthly/Annual/Contract), with `tests/MpsCalc.Engine.Tests/RecurringProjectionTests.cs` in the tree.
- **Files it touches (from the tree read):**
  - `src/MpsCalc.Engine/Results/PurchaseResult.cs`
  - `src/MpsCalc.Engine/Calculation/PurchaseCalculator.cs`
  - possibly `src/MpsCalc.Engine/Reconciliation/PurchaseRecomputation.cs`
  - `docs/ENGINE.md`: a new register row after X-38 at line 164
  - new `tests/MpsCalc.Engine.Tests/*` rows
  - The ticket's `PurchaseCatalogue.cs` is still **not in the tree**, a stale name: 0 lines in `mps_tree.txt` (747 paths). Control: `PurchaseResult.cs` is found.
- **Words:** "New words go to the product owner's words gate before any deploy." This is engine only, with no deploy, so no words are needed now.
- **Model:** `model-routing.md` line 93 (C3, money design surface, O55 1st), the same row B1015 used for -255. `claude-opus-5-5`. Gate: line 108 (G1, tier 1).
- **Open PRs:** #120 and #121 (dependabot, `/web`, RELAYED from 05:00 as `web/package-lock.json`). No overlap.
- **Serialise after this lane** (same files): MPSCALC-253 (perDevice / fixedPerGroup / manual), MPSCALC-257, and MPSCALC-196's X-33 row (ENGINE.md).

### 2. NexusAI: RD-913, npm-audit red on main: fix the two high advisories in the lock. Size S, plus a measurement.
- **Done-when (ticket's own):** "the npm-audit push run on main reads success, or the product owner has accepted the remaining rows and this ticket records that decision."
- **What the lane can finish:** the lock-only raises follow-redirects 1.16.1 to 1.16.2 and joi 18.2.9 to 18.3.1 (the ticket's recommendation, the RD-879/-881 shape, no package.json change). It can also **measure** whether the 12 moderate rows clear with a parent upgrade (archiver / sqlite3). If they do not clear lock-only, the ticket's own second branch is a product-owner decision: **needs a ruling** (section 6).
- **Why now:** the check is red on every new NexusAI branch, including the branches of lanes 3 and any later lane (ticket: "it does show red on every new branch until the lock changes").
- **Not built yet:** `package-lock.json` at `89375808`, parsed: `node_modules/follow-redirects` 1.16.1 and `node_modules/joi` 18.2.9. Positive controls from the same parse: axios 1.20.0, express 5.2.1, and the nested glob 10.5.0, all non-null.
- **Files:** `package-lock.json` only (in the tree at line 786 of `rd_tree.txt`). Workflow `.github/workflows/npm-audit.yml`: no change ("no audit exception, no baseline and no workflow change").
- **Model:** line 92 (C2, S55 1st). `claude-sonnet-5-5`. Gate: line 109 (G2, config). Landing: merge commit (RELAYED from SWEEP-0500: RD-899/-900 comments). Status goes to Testing. Nothing is deployed (Partner Center, behind the testing-agent gate).
- **Open PRs:** 0 (control above). It does not overlap lane 3 (different file).

### 3. NexusAI: RD-912, clean the chat route's remaining roster reads (null entry gives 500 at :7315, a handled error at :9862). Size S.
- **Done-when:** the ticket gives no separate Done-when line. Its Recommendation is the closable test: "Clean every roster-shaped read the same way, ideally with one shared helper that keeps only object rows, used at lines 7314 and 7334 and in the sibling generateUserActivityAnalysis (line 10138) ... Add one cell beside cell F2 of `__tests__/rd869-roster-before-skip-list.test.js` (line 663) ... red at main 88144175 ... red before #147 ... It moves scripts/verify-expected-counts.json ... by one test. A code change with its own review gate." Tuesday should treat that as the Done-when, or ask the builder to quote it as such.
- **Not built yet:** at `89375808` (server.js 22411 lines, the same server.js as `88144175`):
  - :7314 `const allLogs = await getAllPrinterLogs({ limit: 1000 });`, and :7315 `allLogs.some(log => log.User_Name?.toLowerCase() ...` with no entry guard.
  - :7334 `await getAllPrinterLogs({ limit: 1000 })` is passed raw.
  - :9862 `const logUser = log.User_Name?.toLowerCase();`
  - :10186 `rosterLogs.map(log => log.User_Name)`, unguarded.
  - Positive control, same file: :8089 holds RD-910's guard `rosterLogs.filter((log) => log !== null && typeof log === 'object')`.
- **Files:** `backend/server.js`, `__tests__/rd869-roster-before-skip-list.test.js`, `scripts/verify-expected-counts.json`.
- **Collision:** RD-909 (NEEDS-RULING) is the name-capture fix inside `checkForCurrentUserQuery`. RD-912's pointers are the route (:7314/:7334) and the two activity functions (:9862, :10186), not that function. Keep the lane fenced to those lines. 0 open PRs. Run it after lane 2, or in parallel and expect the red npm-audit check.
- **Model:** line 92 (C2, Sonnet). Gate: line 109 (G2), as B1023 gated RD-910 ("gate-tier2").

### 4. MPS: MPSCALC-355, the walk-cap test gaps of gate B678 (B678-1 to -5). Measure first, then add rows. Test-only. Size M.
- **Done-when (B678-1, the shape of all five):** "g01_sharedBomCc and g02_sharedBomRn are each red under a committed row (a new row, or a row already at main that the measurement shows red) and that row is green at the unedited product; the existing rows stay green; no product byte changes." It is the same for g04 (B678-2) and the other three sections.
- **Why now:** it also unblocks MPSCALC-325. B1021 held -325 at 07:07 on exactly this: "the committed rows do not pin the cap for lines numbered 0 (B678-2 ... filed as MPSCALC-355)". Under C-79 a merged test-only row closes the clause.
- **Not built yet (RELAYED plus partial MEASURED):** B1021's record at code main `5c64a442` (CLARIFICATIONS.md:1877) says the cap for line 0 is unpinned. `tests/MpsCalc.Api.Tests/QuoteWalkCaps.cs` (749 lines) was last changed by `960141b3` (#129, 2026-10-27T05:03Z, "two fleet lines with one number and a control character each list that entry twice"). That commit lands after the ticket was filed (00:29Z) and may cover part of B678-1, which is why the ticket says "measure first". `g01|sharedBom` gives 0 hits. Rows for lines numbered 0 exist by comment (:431, :475, :611). Whether they kill g04 is UNMEASURED. Control: `[Fact` gives 40.
- **Files:** `tests/MpsCalc.Api.Tests/QuoteWalkCaps.cs` (or one new test file beside it). The measurement reads `src/MpsCalc.Api/Quotes/PurchaseValidation.cs` and `QuoteEndpoints.cs` and changes no product byte.
- **Collision:** none with lane 1 (Engine versus Api tests). Open PRs #120/#121 are web only.
- **Model:** line 85 (L6 test-only pin; S55 is the "1st fallback"), Sonnet. Gate: line 109 (G2). Note that G2 says O55 is 1st "if the follow-up's mechanism sits on a G1 surface". The walk caps are input-hardening, so Tuesday's call is whether the gate is G1 (line 108) instead.

### 5. Composer: PCOMP-98, cross-line context in the DEPLOY.md command-guard scanner (16 known lost cells, 187 sweep instances). Test-only. Size L.
- **Done-when (ticket's own, 5 clauses):**
  1. "Each of the 16 ids has a regression row that is red on main at the squash above and green after the fix, with the pty (bash 5.2) transcript naming the failing line."
  2. "No existing row is loosened and no closed case ... is lost."
  3. "The edit stays inside `packages/db/test/b616-deploy-commands.db.test.ts` (or one new test file beside it): no product byte, no DEPLOY.md byte."
  4. "A fresh-seed sweep reports 0 class instances outside a list the fix names."
  5. "A gate of its own."
- **Why now:** SWEEP-0500 serialised it behind PCOMP-102 because both touch the b616 file. PCOMP-102 landed as #108, which changed DEPLOY.md and `b778-...test.ts` only (PR files read: `DEPLOY.md +10 -6`, `b778 +174 -2`). The b616 file is free.
- **Not built yet:** the last commit on the b616 path at `6e69886d` is `075b2b23` (#106, "pin a late digest verdict and a hash line after a closed string"), and before it `4a2911f1` (#94, the squash the ticket names). No commit after the ticket names this class. 0 of the cell ids Q01563, Q02784, Q00288, F8-Z2538, P-exec-open-A and Q02893 appear in the file (1110 lines). That is a weak proof by itself, because rows need not carry ids. Control: `heredoc|here-doc|<<` gives 118 hits.
- **Bash 5.2:** this machine has only `/bin/bash` 3.2.57. The B1037 gate ran "under the CI image's bash" in a container (B1041 kit line 86). The seat needs that container route for clause 1. This is fenced for this drafter, not for a builder seat.
- **Collision:** open PRs #95 (`apps/api/src/routes/engagements.ts`, b712 test), #91 and #86 (package files), #85 (draft, content). None touches b616. B1041 writes the root records repo and Jira only (kit line 54: "A Composer builder or gate seat writes under its own `.tools/b<NNN>`: quote it and continue"). **Serialise with any future DEPLOY.md lane**, for example the B1041 NEW-VERSION-WORDS ticket from B1037-2 (`DEPLOY.md:263`), because b616 scans DEPLOY.md.
- **Coordinator's call:** "whether it counts as round 1 of 2 is not ruled" (ticket). This is a counter call, not a product decision.
- **Model:** line 85 (L6 test-only, S55 fallback), Sonnet. Gate: line 109 (G2). Landing: squash.

### Alternates (agent-completable, not in the five)
| Key | Size | Done-when / state | Not-built proof (control) | Files | Model / gate |
|---|---|---|---|---|---|
| HPSMPOC-405 | S-M | "no fixed shell element sits over a row button or a last entry at the sizes named, or the item is recorded as declined". Fix shape is the coordinator's design call (the gate's "safe area for fixed elements" is the clean one). It reaches DONE-PENDING-DEPLOY only | `FeedbackPill.module.css` last commit `c2dd4037` (2026-10-03, #86), before the finding (gate B959, 10-30). Control: the file's footer rule `padding-bottom: 6rem` is present, and the overlap was measured with it | `web/src/components/feedback/FeedbackPill.module.css`, `web/src/components/shell/AppShell.tsx`, list pages; 0 open PRs | 92 Sonnet / 108 (G1: client testers) |
| MPSCALC-196 | S, docs | held only on "register row X-33 is not in docs/ENGINE.md" (B1021) | ENGINE.md register at `5c64a442`: X-32 at :159, then X-34 at :160. `x-33` gives 0 hits, control `x-32` gives 1. X-20 is explained at :178, X-33 is not | `docs/ENGINE.md`; serialise after lane 1 | 92 / 109 |
| MPSCALC-215 | S | "Each prefix + 24 hex + a trailing newline gives 400 on quote create, PATCH and the inventory PATCH". Held: the inventory PATCH answers 404 | `InventoryEndpoints.cs:157-160` returns `NotFound()` for a non-key. Control: `PurchaseValidation.cs:38` already ends `\\z` | `src/MpsCalc.Api/Inventory/InventoryEndpoints.cs` + an Api test | 93 (price-edit admin surface) or 92 / 108 |
| MPSCALC-253 | L | per rule: register row and red-first test; fixedPerGroup is not multiplied by the fleet quantity; manual is taken as typed; an unknown rule is refused | not re-measured (ticket "Depends on MPSCALC-252", now Done) | same engine files as lane 1, so after it. usageOnly is a coordinator reading; perSite waits for -257 | 93 / 108 |
| RD-911 | S, test-only | Done-when branch 1: each bound is left with a reason, or replaced by a count with a red-first plant | `rd407-r2-missing-mid-swap.test.js:138` still `Date.now() - startedAt` and `:45 PAST_BUDGET_MS = BUDGET + 400`; concurrent `:68 STORM_DEADLINE_MS = 60000`. Last commits `ae8748cb` (10-29) and `1e9a2c03` (10-29) predate the ticket. Control: `retry` gives 18 | the two rd407 test files | 85 / 109 |

## 6. Needs a ruling (one-line question each; not completable by an agent)

- **HPSM-POC, deploy:** May main `a3a06b9a` (#269 part B, #270 test-only) go to UAT? C-260: "PR #269 and PR #270 NOT deployed", "compare a3a06b9a...77c3132e reads behind 2". This is approval-class (deploy).
- **HPSM-POC, Done on UAT:** Does a UAT-only deploy satisfy "merged, gated and deployed"? (C-260: "the slot read COMMENT-ONLY; every key stays Backlog".) 13 keys carry the 12:57 "UAT now runs 77c3132e" comment and stay Backlog: 399, 407, 408, 411, 413, 414, 415, 416, 418, 419, 422, 423, 426.
- **HPSMPOC-428 (new):** Which fix: the API's transient-retry and connect budget, or keep the database awake (and the demo's too, which is money)? The ticket says: "Which fix is built is a scope call that is not made here." **Agent-completable once ruled** (the API EF retry and connect timeout is a code change). **Its Done-when needs a deploy decision:** "a database wake no longer loses a read to an API 500 in a measured visit on an environment that pauses". UAT no longer pauses, so the measurement needs a pausing environment.
- **HPSMPOC-427:** Apply the test-only precedent (move at merge) or wait for a deploy? (C-261: "a later records step if the product owner wants the test-only precedent applied".)
- **HPSMPOC-388:** the 12 px hint (B1022-10, no ruling). Done also waits on the deploy above.
- **HPSMPOC-402:** possibly all three hand-offs are built. Hand-off 1 is `a026cb30`. Hand-off 2: `step-previous.spec.ts:26-31` `NO_FORWARD` (from `c364caf0`, #263) exercises showNext false. Hand-off 3: RevenueResults.tsx:9 imports `ui/Table`; EngagementsList.tsx:10-11 and CustomerManagement.tsx:13-15 import `ui/Progress` and `ui/Table`. This is a records candidate behind the UAT-Done ruling above, UNVERIFIED clause by clause (for example "page score bars" on RevenueResults).
- **HPSM carried from 05:00:** -409 item 1 (words), -417 (scope), -424 and -425 (product), -390 to -396 (input).
- **MPS:**
  - The Api / DTO / openapi / web half of -252/-258/-259: which ticket owns it (CLARIFICATIONS:1774 7(a)).
  - -258: the permission, reason and audit of the manual tier (7(b)).
  - -316: maxLength says characters (comment 40096).
  - -306: owner question B354-5.
  - -150: tile placement.
  - -233, -236, -244, -245: coordinator defaults the product owner has not ruled.
  - -261: the authorisation rule.
  - A hosted deploy of code main `5c64a442` (not ruled; the showcase runs `e027ebd0`, relayed).
- **Composer:** -113, -114 and -115 ("NOT RULED"); -52 (words); -42 (refusal words plus an unbuilt dependency); -83 half 2; -74 (token approval). -44 is HELD.
- **NexusAI:**
  - RD-913 moderates: accept the 12 rows, or approve an archiver / sqlite3 parent upgrade? (Ticket branch 2.)
  - RD-901 to -909: each says "The product owner decides".
  - RD-896: data directories from the product owner.
- **ATTIO:**
  - ATTIO-31: how three Vision values (incumbent / competition / no) map to a two-state checkbox, or whether the attribute type changes. This is a product mapping.
  - ATTIO-8 and -10 are [KAM] items.
  - ATTIO-15 needs the Pro tier (money).
  - ATTIO-19 and ATTIO-24 to -27 are real quotes, a pilot with people, and cutover.
  - ATTIO-30 is In Review (the product owner's commission).
  - ATTIO-16 is In Progress since 08-22, with 5 comments, and was not opened here.

## 1. MPS Commercial Calculator (MPSCALC; datasecau/MPS-Commercial-Calculator; main 5c64a442)
Since the cutoff, #135 merged at 19:57:38Z. Open PRs are #120 and #121 (dependabot). Records B1019, B1021, B1024 and B1026 moved 61 keys and held 19, all with "0 C-entries".

| Key(s) | Status | Class | Evidence |
|---|---|---|---|
| 255 | **Done** (07:29) | landed (SWEEP-0500 lane 1) | comment: "MPS #135, squash 5c64a442 ... Done-when met" |
| 252, 259 | **Done** (08:01/08:02) | re-judged under C-79 | B1026, `76f1806` |
| 258 | Backlog | NEEDS-RULING (reason / permission / audit) | CLARIFICATIONS:1923 |
| 256 purchase half | Backlog | **ACTIONABLE (lane 1)** | above |
| 355 | Backlog | **ACTIONABLE (lane 4)** | above |
| 325 | Backlog, held | closes with -355 (B678-2) plus its red-run reading | B1021 :1877 |
| 196, 215 | Backlog, held | alternates (S) | table above |
| 253, 257 | Backlog | ACTIONABLE after lane 1 (same files) | descriptions |
| 237, 312, 269 | Backlog, 0 comments | ACTIONABLE (05:00 reading unchanged, 0 updates). Contract files collide with the unowned Api half | 05:00 table |
| 27, 28, 34, 150, 160, 189, 198, 217, 233, 236, 244, 245, 297, 306, 316, 324 | Backlog, held 11-01 | each held on a named clause (CLARIFICATIONS :1831, :1887). Build gaps (27, 28, 34, 160, 217) are larger lanes; 297 and 198 need an e2e run (the repo CI has no Playwright step); others need rulings | records |

## 2. Security Composer (PCOMP; datasecau/Datasec-Security-Composer; main 6e69886d)
Board: 0 created, 0 updated, 0 comments since the cutoff (B1041 had not yet written at 13:30). #107 (`c8eba7f6`) and #108 (`6e69886d`) merged at 00:57:39Z and 01:14:43Z. Open PRs: #95, #91, #86, #85 (draft, HOLD).

| Key | Class | Evidence |
|---|---|---|
| 102, 112 | landed. OFF LIMITS (B1041 records) | PR files above |
| 98 | **ACTIONABLE (lane 5)** | above |
| 113, 114, 115, 52, 42, 83, 74 | needs a ruling | section 6 |
| 44 | HELD (product owner, 2026-11-01) | relayed |
| 36-39, 12, 77, 82, 41, 62, 29 | unchanged from 05:00 (0 updates) | 05:00 table |

## 3. HPSM-POC (HPSMPOC; datasecau/HPSM-POC; main a3a06b9a)
Merged since the cutoff: #269 `1f4bf7bc` (23:24:35Z) and #270 `a3a06b9a` (00:59:14Z). UAT runs `77c3132e` (C-260, deployed 11:09-11:11 AEDT). The demo runs `c00e2828`. 0 open PRs.

| Key | Class | Evidence |
|---|---|---|
| 388 | landed (part B, #269 at the cap on the product owner's ruling). DONE-PENDING-DEPLOY | C-259 |
| 427 (new) | built and merged (#270, gate B1036 GO WITH FINDINGS). Needs a ruling (test-only precedent or deploy) | C-261; comment 12:56 |
| 428 (new) | **agent-completable code half once the fix is ruled. Flag: its Done-when needs a deploy decision** on a pausing environment | description |
| 399, 407, 408, 411, 413-416, 418, 419, 422, 423, 426 | deployed to UAT, Backlog. Needs the UAT-Done ruling | 12:57 comments; C-260 |
| 405 | alternate (Sonnet, G1) | table above |
| 402 | records candidate, all three hand-offs appear built | section 6 |
| 409, 417, 424, 425, 389-396 | unchanged | 05:00 |

## 4. NexusAI (RD; datasecau/Reporting_Dashboard_Au; main 89375808)
#147 (merge `88144175`, 23:00:59Z) and #148 (records B1029) landed. RD-910 is in Testing. 0 open PRs.

| Key | Class | Evidence |
|---|---|---|
| 910 | landed (Testing) | comment 11:00 |
| 913 (new) | **ACTIONABLE (lane 2)**, with a ruling for the moderates | above |
| 912 (new) | **ACTIONABLE (lane 3)** | above |
| 911 | alternate (test-only) | table above |
| 901-909, 896 | needs a ruling | section 6 |

## 5. ATTIO (board ATTIO, measured; datasecau/attio)
The board exists: 30 issues, max 31, last update 2026-09-07 (ATTIO-31), and 0 changes since the cutoff. Local root log head is `fae239b` (2026-09-07). There is no firm lane; see section 6. ATTIO-29 is OFF LIMITS (B1042).

## Other Datasec folders
Unchanged from SWEEP-0500 section 5, except that ATTIO is now swept (above). CypherKey, myPKI, Vision_Sales_Portal (its RG is production) and HPSM were not swept.

## 7. UNMEASURED
- **ATTIO GitHub:** `gh` under `ATTIO/4_Credentials/.gh-config` answers "To get started with GitHub CLI, please run: gh auth login". `git ls-remote origin` fails with "Identity file /Volumes/DevMASTER/!CODING/Datasec/ATTIO/3_Access_Keys/github_deploy_rw not accessible" and then "Permission denied (publickey)". Its open PRs and main are unknown. This was reported, not worked around.
- Which seats are live: the pane list format differed from 05:00 (see above).
- Hosted state of everything (fenced). "Deployed to UAT" is RELAYED from C-260 and the ticket comments.
- Whether 960141b3 or the line-0 rows already kill g01/g02/g04 (lane 4 measures first).
- PCOMP-98: where the seat gets bash 5.2 (the CI image route is relayed from B1037/B1041).
- RD-913: whether the moderate rows clear without an archiver or sqlite3 upgrade (not run).
- HPSMPOC-402 clause by clause, and HPSMPOC-405's overlap at `a3a06b9a` (not re-measured).
- MPS open PRs #120/#121 file lists (relayed from 05:00, not re-read).
- The RD board's 2 truncated comment sets.
