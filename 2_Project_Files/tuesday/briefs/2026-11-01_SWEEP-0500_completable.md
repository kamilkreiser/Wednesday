# SWEEP 0500 2026-11-01: what can be finished next (read-only; MPSCALC / PCOMP / HPSMPOC, plus RD)

Measured Sun 1 Nov 2026, 04:50 to 05:05 AEDT. This sweep is a delta against `2026-11-01_SWEEP_delta.md`. The cutoff for "new since" is **2026-11-01 00:35 AEDT = 2026-10-31T13:35Z**, the time that sweep was measured.

How it was measured: Jira GET only, through a urllib reader that reads each project's own `4_Credentials/.env` inside the process (the previous sweep's `fetch.py`, copied to a private scratch folder; no token was printed). GitHub reads were `gh api -X GET`, each under that project's own `GH_CONFIG_DIR`. The repo trees come from `git/trees/<main sha>?recursive=1`. The only git read was one `cat-file` with `--no-optional-locks`. There was no HTTP to any hosted site and no read of the decision store. This file is the only thing written.

## Controls (each one printed by the command that produced the count)

- **Board totals equal the highest key**, with 0 duplicates, 0 truncated comment sets and 0 keys from another project:
  - MPSCALC 356, max 356, unique 356.
  - PCOMP 115, max 115, unique 115.
  - HPSMPOC 426, max 426, unique 426 (it was 425).
  - RD (NexusAI) 907, max 911, unique 907, with 2 truncated comment sets. The missing keys are RD-1, -2, -39 and -44. The same gap of 4 showed in the 10-27 sweep (889 issues against max 893). The RD reader uses `created >= -3650d`, because `key >= RD-1` returns 0 on RD. Controls for that switch: `key = RD-893` returns 1, and `text ~ "zzqxnonexist"` returns 0.
- **Status sums add up to the totals:**
  - MPSCALC: 319 Backlog + 37 Done = 356. At the delta sweep it was 342 + 14. The +23 Done are B987's 12 moves and B1004's 11, as listed in CLARIFICATIONS.md C-79 "Delivered" (line 1718).
  - PCOMP: 93 + 22 = 115 (no change).
  - HPSMPOC: 243 Done + 180 Backlog + 3 In Progress = 426.
  - RD: 364 To Do + 205 Testing + 199 Release Ready + 120 Done + 10 In Progress + 7 Put on Hold + 2 Declined = 907.
- **The cutoff is checked in code:** `p('2026-11-01T00:35:00.000+1100')==CUT`, and 00:34:59 sorts before it. Either check would stop the run if it were wrong. Timestamps are parsed, never compared as text.
- **Delta since the cutoff (parsed):**
  - MPSCALC: 0 new, 38 updated, 38 new comments. All are the records pass B1004 plus MPSCALC-254/-256 comments 40382/40383.
  - PCOMP: 0 new, 0 updated, 0 new comments. This zero is checked by the same code finding 38 on MPS, and by the cutoff assert.
  - HPSMPOC: 1 new (HPSMPOC-426), 3 updated (422, 423, 426), 2 new comments.
  - RD: 0 new, 0 updated. Last change 2026-10-30.
- **404 control:** `pulls/99999` returns 404 on MPS, Composer and HPSM-POC.
- **Open-PR zeros:** the same `gh` call lists 2 open PRs on MPS, and the closed list returns rows on HPSM-POC and NexusAI. So the HPSM-POC 0 and the NexusAI 0 are real.
- **Regex control:** `zzqxnone` matches 0 MPS comments, and `[B583]` matches 83.
- **"Not built" checks**, each paired with a positive control from the same file:
  - MPS per-group service fee: `ServiceFee|ManagedService` gives 0 in PurchaseInput.cs and PurchaseCalculator.cs at edac7431. Control: `FleetQuantity` gives 2 and 5 hits, and QuoteInput.cs gives 3 hits for the rental fee.
  - Composer `tail -n 6` check: still at DEPLOY.md:203 at 075b2b23. `\unrestrict` appears only in prose (line 257).
  - HPSM-POC part B views: `SECURITY_VIEWS` in views.ts lists only dashboard, fleet and assessments.
  - NexusAI RD-910: server.js:8093 still reads `(rosterLogs || []).map(log => log.User_Name)` at a4a227dc.

Mains, read with `git/ref/heads/main`:
- MPS `edac7431` (#134, 2026-10-31T17:37:43Z).
- Composer `075b2b23` (unchanged).
- HPSM-POC `77c3132e` (#268, 16:12:31Z).
- NexusAI `a4a227dc` (unchanged since #146).
- HPSM-POC-analysis `0a33f395`.

Live panes (`tmux list-panes -a`, 05:01): `tuesday`, `Datasec/MPS-R102` (B1013) and `fleet-monitor`. B1014 is a drafter, not a pane.

## BLUF: the lanes Tuesday should start next (4 firm, 1 held)

OFF LIMITS, as relayed:
- **B1013** owns the MPS root records repo and Jira comments on MPSCALC-252/-258/-259. Its own kit fences also forbid comments on -253 to -256.
- **B1014** owns the HPSM-POC-analysis records repo and the keep-awake tickets.

None of the four lanes below writes to either repo or to those Jira keys. Every lane writes only to a code repo branch. Tuesday lands each one through CodeQL.

**1. MPS: MPSCALC-255, the per-group managed-service fee, engine half. Then MPSCALC-256's purchase projection, in sequence. Size L.**
- Why now: -255's only code dependency was -252 (T-V4-1). Its engine half is on main as #134 (`edac7431`): X-35 `PurchaseSection.FleetQuantity` is at ENGINE.md:161. -256's purchase half waits for -255, per B1004's item 6(b).
- Files at main edac7431 (from the tree read):
  - `src/MpsCalc.Engine/Input/PurchaseInput.cs` (138 lines)
  - `src/MpsCalc.Engine/Calculation/PurchaseCalculator.cs` (927)
  - `src/MpsCalc.Engine/Results/PurchaseResult.cs`
  - `src/MpsCalc.Engine/Reconciliation/PurchaseRecomputation.cs`
  - `docs/ENGINE.md` (the register lives here: new X row after X-37)
  - new `tests/MpsCalc.Engine.Tests/*` rows
  - The ticket also names `PurchaseCatalogue.cs`, which is **not in the tree** (stale name).
- Collision check: B1013 writes only records and Jira, never `2_Project_Files`. Open PRs #120 and #121 change only `web/package-lock.json`. No other MPS builder is live. Keep the Api/DTO half held (lane 5).
- Model: `model-routing.md` line 93 (C3 money design surface, Opus 1st), as B1000 used. `claude-opus-5-5` (models_latest 04:48). Gate on line 108 (G1, tier 1).

**2. HPSM-POC: HPSMPOC-388, customer security workspace part B (findings, remediation roadmap, reports and evidence, continuous assurance). Read-only. Size L.**
- Why now: both dependencies are merged. HPSMPOC-387 is `32fc1750`, 2026-10-30. HPSMPOC-377 is in the e8ac3f29 UAT deploy (C-250). Part B is not built: `views.ts` lists 3 views, and `app/(app)/security/[customerId]/` holds only assessments, dashboard and fleet.
- Files at main 77c3132e:
  - new `web/src/components/security/{findings,roadmap,reports,assurance}*`
  - new `web/src/app/(app)/security/[customerId]/<view>/page.tsx`
  - edits to `components/security/views.ts`, `labels.ts`, `components/shell/customer-nav.ts`
  - the walk harnesses `security.no-write.test.tsx`, `security.no-price.test.tsx`, `security.alias.test.tsx` and `security.routes.test.ts`
- Collision check: B1014 is the analysis repo plus keep-awake (infra and readRetry/bff). This lane is `web/src/components/security` and app routes only, with 0 open PRs on HPSM-POC.
- Fences:
  - "Continuous assurance" is "Not connected" placeholders only, as FleetDevices does (1 hit). C-163 (analysis CLARIFICATIONS:2672): build only what this phase needs, no HP-tool integration.
  - Framework alignment stays held.
  - Any label that is not in the product owner's v1.2 design is NEEDS-WORDS and stops the lane.
- Model: line 92 (C2, Sonnet 1st), `claude-sonnet-5-5`. Gate on line 108 (G1: UAT reviewers are client testers).

**3. Composer: PCOMP-102, the Route B completeness check that accepts a cut script ending in a planted footer line. Size M. Optional ride-along: PCOMP-112, test-only, S, a different file.**
- Why now:
  - It is a Minor with a measured data-loss shape: 3 of 5 cut prefixes applied with exit 0 and lost data.
  - The product owner's 2026-10-27 ruling landed PR #96 and asked for this residue to be ticketed.
  - The Done-when is concrete: the 5 planted cuts are refused; the complete script, with or without one trailing blank, is accepted; the check stays in one fenced block under the b616 scanner.
- Files at main 075b2b23:
  - `DEPLOY.md:203` (the `tail -n 6` line), plus the pin paragraph at :218-259 that pins its words
  - `packages/db/test/b778-route-b-script-complete.db.test.ts`
  - `packages/db/test/b616-deploy-commands.db.test.ts`, which scans DEPLOY.md and must stay green
  - For -112: `apps/api/test/b626-date-rule-rows.db.test.ts`
- Collision check: different repo from both off-limits seats. Open Composer PRs touch other files: #95 `apps/api/src/routes/engagements.ts` + b712 test; #91 and #86 package files; #85 draft content. PCOMP-113 (NEEDS-RULING) also edits the DEPLOY.md pin paragraph, so hold it until this lands. PCOMP-42/-44 are blocked, with no seat.
- Coordinator's design call (not the product owner's): fix shape (i), match the `\restrict`/`\unrestrict` key and refuse a script without the pair (the ticket calls this "the safe direction"), or fix shape (ii), the three-line footer block.
- Model: line 92 (Sonnet). If Tuesday reads a restore path as C4, use line 94 (Opus). Gate: line 108 for -102, line 109 for -112.

**4. NexusAI: RD-910, a roster list holding a null entry makes every name-bearing chat question answer 500. Size S. Plus RD-911 as a separate small lane (S, test-only).**
- Why now:
  - RD-910: the product owner's 2026-10-30 ruling landed #143 and asked for this edge case to be ticketed. The fix shape and the Done-when are in the ticket. server.js:8093 is unchanged at a4a227dc.
  - RD-911: the Done-when's first branch needs no decision: each bound is either left with a reason, or replaced by a count with a red-first plant.
- Files:
  - RD-910: `backend/server.js` (:8086-8093), plus one cell beside F1 in `__tests__/rd869-roster-before-skip-list.test.js`.
  - RD-911: `__tests__/rd407-concurrent-settings-writers.test.js`, `__tests__/rd407-r2-missing-mid-swap.test.js`.
- Collision check: no NexusAI seat is live and there are 0 open PRs. RD-909 (NEEDS-RULING) is in the same function `checkForCurrentUserQuery`, so it is not paired with RD-910.
- Landing and status: NexusAI lands by merge commit (RD-899/-900 comments: "as merge commit"). Status goes to Testing (NexusAI CLAUDE.md:302). Nothing is deployed: deploy goes through Partner Center behind the testing-agent gate (CLAUDE.md:315-326).
- Model: line 92 or line 85 (L6 test-only) for RD-911, Sonnet. Gate line 109.

**5. HELD (not startable while B1013 is live): MPS records batch 3, C-79 Done checks on merged-but-open tickets.**
- **80 open MPSCALC tickets carry a `[B583]` "merged work names this ticket" comment.** Count by regex over all 356 issues; control `zzqxnone` 0. Examples: -232 to -236 (lane V0, PR #85, squash f2584d36).
- The C-79 Done rule is MPS CLARIFICATIONS.md:1712-1722: "Done means merged to main, the same as Composer", plus every Done-when clause MET.
- This lane shares the root repo, `.tools/.git-lock` and Jira with B1013. The HPSM-POC equivalent (HPSMPOC-369/-370/-397, apparently built by `9659148c` "Shell: a left sidebar ...", 0 comments) is HELD behind B1014, and the HPSM Done rule (below) needs a deploy anyway.

**Done rules, checked at source:**
- **MPS:** C-79 (CLARIFICATIONS.md:1712, the product owner's 2026-11-01 ruling 00:18:56 AEDT): merged to main AND every Done-when clause met.
- **Composer:** its own file holds **no product-owner Done ruling**. C-111 (3), quoted at :2049, reads: "The project still records no standing rule for when a merged, not deployed ticket moves (C-105 (3)); these moves rest on the coordinator's instruction ... Done here means merged to main, not deployed." Instrument: `grep -i 'done means merged'` gives 0 lines; `standing rule` finds :2049; control `PR #88` gives 22. The MPS ruling's words "the same as Composer" therefore point at a coordinator practice, not a Composer C-entry.
- **HPSM-POC:** "Done means merged, gated and deployed" (analysis CLARIFICATIONS.md:1904, R-R10-1, as read from origin main 0a33f395).

## 1. MPS Commercial Calculator (MPSCALC; datasecau/MPS-Commercial-Calculator; main edac7431)

Since the cutoff, PR **#134** merged at 2026-10-31T17:37:43Z: "ENGINE HALF", 9 files, +701 -17. Its body says: "The three tickets stay open; the Api, DTO, openapi, web, audit reason and permission are held and not built here." Open PRs: #120 and #121 (dependabot, `web/package-lock.json`). The local checkout is stale: its `origin/main` is 5d96a3dc and `cat-file edac7431` fails. Everything here was read from origin.

| Key(s) | Status / comments | Class | Evidence |
|---|---|---|---|
| 252, 258, 259 | Backlog; 1/0/0 comments, B1013 writing now | HELD (off limits). Engine half partly done; Api/DTO/openapi/web half not built; -258 also open on permission, reason and audit | PR #134 body; B1013 kit lines 26-28 |
| 255 | Backlog, 0 comments | **ACTIONABLE (lane 1)** | depends on T-V4-1 only; 0 fee hits on purchase files |
| 256 (purchase half) | Backlog, comment 40383 "not moved" | BLOCKED on -255; follows lane 1 | B1004 item 6(b) |
| 253 | Backlog | ACTIONABLE for perDevice / fixedPerGroup / manual after lane 1 (same files). usageOnly is a coordinator reading ("to confirm with the coordinator"); perSite waits for -257 | description |
| 257 | Backlog | ACTIONABLE engine, same files; serialise after 255/253. The reconcile issue's message text may need words: measure | description |
| 269 | Backlog | ACTIONABLE (new `src/MpsCalc.Api/Templates/**`, contract via V0). Collides with the held Api half on Dtos.cs/openapi.json | description |
| 237 | Backlog, 0 comments | ACTIONABLE (its dependency -236 is merged in PR #85). Server side; "new words go to the words gate before any deploy". Shares Dtos.cs/openapi.json/QuoteEndpoints.cs with the held Api half: one contract builder at a time | description; -236 `[B583]` comment |
| 312 | Backlog | ACTIONABLE (S, contract words sync); same files as -237: pair them | description |
| 261 | Backlog | Visible-credit part ACTIONABLE at the coordinator's call; the authorisation rule is NEEDS-RULING ("waits for a ruling", no D card) | description |
| 232-236 and 75 more (80 in all) | Backlog, `[B583]` record | DONE-ELIGIBLE candidates under C-79, HELD behind B1013 (records) | regex count above |
| 147, 153, 163, 170, 254, 256 | Backlog, recorded by B1004 | Each held on one named clause (C-79 section, item 6(b)) | CLARIFICATIONS.md:1745 |

## 2. Security Composer (PCOMP; datasecau/Datasec-Security-Composer; main 075b2b23)

Board unchanged since the cutoff: 0 created, 0 updated, 0 comments. No PR merged since #106. Open PRs: #95, #91, #86, #85 (draft, HOLD).

| Key | Class | Evidence |
|---|---|---|
| 42, 44 | BLOCKED / NEEDS-RULING: the open product-owner card on refusal words (relayed). B1001's report: -42 needs new words and an unbuilt dependency; -44 needs a status/code sentence | B1001_DRAFTER-REPORT lines 1-10 |
| 102 | **ACTIONABLE (lane 3)** | Done-when and ruling quoted above |
| 112 | ACTIONABLE (S, test-only: a row, or correct the record) | Done-when: "Either a row ... or the record is corrected" |
| 98 | ACTIONABLE (L, test-only, `b616-deploy-commands.db.test.ts` only). Whether it counts as round 1 of 2 "is not ruled": the coordinator's call. Serialise with lane 3 (b616 file) | description |
| 113 | NEEDS-RULING: "which of the three is wanted is not decided ... awaiting the product owner" | description |
| 114, 115 | NEEDS-RULING ("NOT RULED, awaiting the product owner") | previous sweep; 0 updates since |
| 52 | NEEDS-WORDS ("Contents" goes on a words card) | previous sweep |
| 41, 62 | BLOCKED (content release held / clause 2 as written) | previous sweep |
| 36-39, 12, 83, 77, 82, 74/75/80/81, 29 | Unchanged from the delta sweep (0 updates). -83 half 2 is NOT ruled; -74 white token needs the product owner's token approval | descriptions |

## 3. HPSM-POC (HPSMPOC; datasecau/HPSM-POC; main 77c3132e)

Merged since the cutoff:
- **#266** `de6f83fb` (14:44:17Z)
- **#267** `e0b93957` (15:00:30Z)
- **#268** `77c3132e` (16:12:31Z, "UAT database stays awake")

None is deployed, as relayed by the HPSMPOC-426 / -422 / -423 comments. There are 0 open PRs.

| Key | Class | Evidence |
|---|---|---|
| 422, 423 | DONE-PENDING-DEPLOY (merged #267, gated B1005; the Done rule needs a deploy) | comments 2026-11-01 02:22 |
| 426 (new) | HELD (keep-awake / B1014). Done-when needs an approved deploy | description |
| 388 | **ACTIONABLE (lane 2)** | above |
| 405 | ACTIONABLE (Minor, shell; fix shape = bottom safe area or chip line). Files: the shell, `components/feedback/FeedbackPill.module.css`; a measured cell is needed | description |
| 402 | PARTLY DONE: hand-off 1 is on main (NarrativeScreen:165 `showNext={approved}` via a026cb30 HPSMPOC-378; ApiNarrative:216 `approvedNow`; AssessmentScreen:126 `locked`). Hand-off 2 (an e2e row in `web/e2e/step-previous.spec.ts`) is ACTIONABLE (S, test-only); hand-off 3 is a page-lane note | file reads at 77c3132e |
| 369, 370, 397 | Probably built (CustomerPicker.tsx, customer-nav.ts, AppShell.sidebar.test.tsx from 9659148c; no burger spec in the tree), 0 comments: records, HELD behind B1014. UNVERIFIED clause by clause | `commits?path=` reads |
| 409 | Item 1 NEEDS-WORDS (the name is words, the product owner's); item 2 (region landmark) unmeasured | description |
| 417 | NEEDS-RULING ("which links are built is a scope call that is not made here") | description |
| 424, 425 | NEEDS-RULING (product question) | previous sweep |
| 389, 390-396 | 389 BLOCKED (after all lanes); 390-396 NEEDS input ("needs input" in the title) | titles |
| 405-421 others, 357-404 deployed-to-UAT set | Unchanged from the delta sweep (0 updates since the cutoff) | delta |

## 4. NexusAI (RD; datasecau/Reporting_Dashboard_Au; main a4a227dc)

This board is swept because the seat works it: 114 brief filenames dated 10-26 to 10-30 match `nexus|cypher|mypki|attio|vision`. The content census finds 0 CypherKey, CPKEY, myPKI, ATTIO and Vision_Sales_Portal hits, so all 114 are NexusAI, the last being B927 R92. 0 changes since 2026-10-30. 0 open PRs.

| Key | Class | Evidence |
|---|---|---|
| 910 | **ACTIONABLE (lane 4)** | description; server.js:8093 |
| 911 | ACTIONABLE (test-only, S) | Done-when branch 1 |
| 901, 902, 903, 904, 905, 906, 907, 908, 909 | NEEDS-RULING: each says "The product owner decides" (retire or leave; gate the read sync; move the kql write; logSafe; pin cell J; the name-capture fix) | descriptions |
| 896 | NEEDS input: data directories from the product owner, then a repair choice | Done-when |
| 894, 895, 897-900 | Testing (landed) | comments |

## 5. Other Datasec folders under `!CODING/Datasec/` (listed; which were swept)

- **Swept:** MPS, Composer, HPSM-POC (board HPSMPOC), and NexusAI (board RD).
- **Skipped, with a Jira env but no Tuesday kit since 10-25** (filename and `grep -F` census of `tuesday/briefs` for 10-25..11-01: 0 each): ATTIO, CypherKey (CPKEY), myPKI, Vision_Sales_Portal (its RG is production), and HPSM (the older analysis project; HPSM-POC is the live one).
- **Skipped, no Jira keys in env:** b118, Commercial Readiness, Datasec-Sales-Tools, `Datasec%20MPS%20Commercial%20Calculator` (a stray copy), Feedback_System, HPAM, Lead_Bot, Marketing_Collateral, RESEARCH, Security Review, Task_Dispatcher, Websites, `_archive`, `_quarantine_*`.

## 6. UNMEASURED

- Hosted state of everything (fenced). "Not deployed" is RELAYED from ticket comments.
- CI and CodeQL on the new mains: #134 says "NOT TESTED: hosted CI and CodeQL".
- Whether the open product-owner card on Composer refusal words has been answered (decision store not read, by fence).
- Clause-level Done-when for the 80 `[B583]` MPS tickets and for HPSMPOC-369/-370/-397.
- Whether -253's usageOnly reading or -257's reconcile-issue text needs words.
- The RD board's 2 truncated comment sets (keys not read).
- PCOMP-102 behaviour under pg_dump before 16.10 (the ticket names the fallback question).
- HPSMPOC-405's current overlap at main 77c3132e (not re-measured).
