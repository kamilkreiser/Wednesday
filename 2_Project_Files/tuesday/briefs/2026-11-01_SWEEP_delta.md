# SWEEP DELTA 2026-11-01 (read-only; re-check of the 2026-10-31 sweeps MPSCALC / PCOMP / HPSMPOC)

Measured Sun 1 Nov 2026 about 00:35 to 01:05 AEDT. Method: Jira GET only (`search/jql` by token, then issue GET for descriptions), credentials read in-process from each project's own env file, nothing printed. GitHub: `gh api -X GET` only, under each project's own `.gh-config`. No write anywhere except this file. Nothing under HP Reporting and Docs, Source_Documents, inbound or any SOW was opened.

Controls (each printed by the command that made the count):
- Board totals equal max key, 0 duplicates, 0 truncated comment sets, 0 foreign-project keys: MPSCALC 356 / max 356 / unique 356; PCOMP 115 / max 115 / unique 115; HPSMPOC 425 / max 425 / unique 425 (`fetch.py` output, `trunc 0`, `otherproj 0`).
- Status sums add up: MPSCALC 342 Backlog + 14 Done = 356; PCOMP 93 + 22 = 115; HPSMPOC 243 Done + 179 Backlog + 3 In Progress = 425 (printed, compared to the total).
- Cutoff 2026-10-31 12:00 AEDT = 01:00Z is asserted in code (`p('2026-10-31T12:00:00.000+1100')==CUT`, would abort if wrong). An earlier pass of mine compared the offset strings as plain text and mis-listed 19 HPSM keys as new; it was caught and redone with parsed timestamps. Figures below are the parsed ones.
- Landed-comment regex control: nonsense `zzqxnone` matches 0 comments; the real phrase matches 28 HPSM tickets.
- GitHub 404 control: `pulls/99999` on datasecau/HPSM-POC answers 404. Code-search control: `zzqxnonexist` total_count 0.
- PCOMP Done delta: yesterday 13 Done; today 22 = 13 + 9 moved since (PCOMP-14, -17, -22, -40, -43, -63, -95, -96, -97, all updated 2026-10-31 12:30 AEDT onward). Counts agree.

## BLUF: the lanes Tuesday should start next (3 firm, 1 held)

Live seats and what they own (OFF LIMITS): B987 = Jira comments/moves on 21 MPSCALC keys (109, 111, 138, 139, 143, 145, 146, 148, 156, 157, 162, 167, 171, 173, 175, 178, 179, 180, 184, 185, 186) plus the MPS ROOT records repo (CLARIFICATIONS.md, BACKLOG.md, JIRA.md, history.md, `.tools/.git-lock`); it writes NO code-repo file. B998 = HPSM-POC PR #266 (web/src/api/readRetry.ts, web/src/server/bff.ts and tests). B999 = HPSM-POC infra/ (sql.bicep, main.bicep, env/uat.bicepparam, infra/tests/test_security_baseline.py), Jira HPSMPOC-362.

1. **MPS V4 engine, next slice: MPSCALC-252 (T-V4-1, billable device groups), then -258 and -259 in the same chain. Size L** (-252), M each for -258/-259.
   - Why now: MPS PR #133 (squash 5d96a3dc, merged 2026-10-31 15:29 AEDT, 9 files +731 -22) built -254 and the rental half of -256, so the "first slice" of yesterday's lane is done. -252 gates -253, -255, -257, -269; D-05 a is ruled. -258 (D-03 a) and -259 (D-04 a) are labelled "wave 2, any, after the D card" in their own text, so they are startable now but share the same calculator files: one builder, in sequence, never two V4 builders at once.
   - Files (code repo datasecau/MPS-Commercial-Calculator, branch off main 5d96a3dc): src/MpsCalc.Engine/Input/QuoteInput.cs, PurchaseInput.cs, Calculation/PurchaseCalculator.cs, QuoteCalculator.cs, src/MpsCalc.Api Contracts/Dtos.cs, docs/api/openapi.json, docs/ENGINE.md, the calculation register (new rows R/X numbers after R-30 and X-34), plus the purchase-pair test of the version-diff route named in the -252 comment. Tier 1 gate (number-changing).
   - Collision-free: B987's 21 keys do not include 252, 258, 259 (checked against the kit table); B987 writes Jira and the root records repo only, never `2_Project_Files`. B998/B999 are another project. HOLD: do not commission any MPS records seat while B987 is live (see lane 4).
2. **Security Composer L3 structure: PCOMP-42 (remediation states "after validation" and "controlled/staged"), then PCOMP-44 (output kinds sm_policy_json and sm_policy_csv). Size L.** Replaces yesterday's "PCOMP-40..44": 40 and 43 are now Done and 41 is recorded-not-moved (see Composer table).
   - Files (repo datasecau/Datasec-Security-Composer, branch only): packages/db/migrations/0028_*.sql and packages/db/rollback/0028_*.down.sql (highest on main is 0027, tree read; both tickets still name 0022, stale: the number is the coordinator's call per the PCOMP-42 text), apps/api/src/**, packages/api-contract/src/** (document.ts OUTPUT_KINDS at :284 for -44; the file's own comment says the API checks the list against the renderers' OutputKind, so the builder may need one line in packages/renderers/src, measure first), DEPLOY.md rollback line, tests. Tier 1 gate (migration, contract). K5 is ruled (C-91); no screen words (L5 is separate). Branch only, no deploy; `sm_policy_json` matches 0 files on main (code search, control 0), so -44 is not already built.
   - Collision-free: different repo and different client-slot than B987/B998/B999. Within Composer, run -42 and -44 strictly one after the other (shared migration + contract files). Open Composer PR #95 (Guided setup target lock) is a different area; the builder rebases if it lands first.
3. **HPSM-POC small lane: HPSMPOC-422 (pin the not-applicable QuestionBlock anchor id, test-only) and HPSMPOC-423 (extend the blank-evidence list; default: add U+0085, U+FFF0-FFF8, U+1D173-1D17A, U+E0080-E0FFF, leave U+1BCA0-1BCA3 out because it draws a box), one test row per range. Size S (422) + S/M (423).**
   - Files: web/src/components/screens/QuestionBlock.tsx (read only), a new row in web/src/components/screens/AssessmentScreen.restyle.test.tsx or a new sibling test; web/src/components/customer/remediation-store.ts (the list at line 22) and remediation-store.test.ts. No visible words. 423 is product code: gate required; 422 is test-only (if the branch proves unreachable the lane reports that instead of a row, the ticket's own Done-when allows it).
   - Collision-free: none of these paths is in B998 (readRetry.ts, bff.ts, their tests) or B999 (infra/). Both files landed in merged PRs (#263, #265); no open PR touches them (open PRs: only #266). #266 changes only the BFF files, so a rebase is mechanical.
   - Honest flag: 423's text says "a scope call that is not made here" (the U+1BCA0 range). The default above is stated in the ticket itself; Tuesday may prefer to stamp it as the default in the kit.
4. **HELD, start only after B987 reaches READY: one MPS records seat** (shares the root repo, `.tools/.git-lock` and the project's Jira with B987). Content: MPS #133 records (MPSCALC-254 Done-eligible under the 2026-11-01 "Done = merged to main" ruling; MPSCALC-256 comment only, purchase half waits for -255; neither has a single Jira comment today, 0 and 0) and batch 2 of the 154 identity-landed tickets. Files: MPS root records files only.
   - Optional fifth, not collision-sensitive, needs Tuesday's call on reading a sibling product's catalogue: PCOMP-29 (L0-1 crosswalk, records only, 1_Project_Definition/Content/ in the Composer root). The ticket says the catalogue is "another project's files, the coordinator's call"; a names-only v0 from the Composer's own evidence is possible without it.

Reclassifications from yesterday (so no one is surprised): PCOMP-52 (PDF table of contents) was rank 3 ACTIONABLE; its own text says the word "Contents" goes on a words card before it ships (K9 ruled a), so it is NEEDS-RULING (words), not a lane. PCOMP-114 and PCOMP-115 are new and both say "NOT RULED, awaiting the product owner". HPSM-POC's Done rule is "merged, gated and deployed" (CLARIFICATIONS.md line 1904 in the analysis repo, quoted by the landing comments), so the 8 landed tickets below stay Backlog until a deploy of both hosted sites; the demo is held.

## 1. MPS Commercial Calculator (MPSCALC; repo datasecau/MPS-Commercial-Calculator; main 5d96a3dc)

Board: 356 issues, 342 Backlog + 14 Done, identical to yesterday (`fetch.py`). Issues created at or after the cutoff: 0 (control: cutoff assertion above). Issues updated at or after the cutoff: 0; comments created at or after the cutoff: 0. B987's STATUS file exists (first line `RECORDS B987: PENDING`, Step 0 done), so it has not yet written to Jira.

PRs: open #121 and #120 (dependabot, last updated 2026-10-26, unchanged). Merged since yesterday's sweep: **#133 (5d96a3dc, 2026-10-31T04:29:20Z)** "MPSCALC-254 MPSCALC-256: page basis per device or per line, and the rental recurring projection" (9 files, +731 -22, three commits, round-2 fix included). Branch b974 (30ea76d) is its source. Other branches: b94, b97, b98 (old).

| Yesterday rank, keys | Status now | Touched since? | Class today | Evidence |
|---|---|---|---|---|
| 1 MPSCALC-254 | Backlog, 0 comments | Built and merged by PR #133 (no Jira record yet) | DONE-PENDING-RECORD (blocked behind B987) | PR #133 body: "MPSCALC-254 (commit 790e224) ... register R-29 and X-34; the purchase group path waits for MPSCALC-252" |
| 1 MPSCALC-256 | Backlog, 0 comments | Rental half merged by #133; purchase projection not built | PARTLY DONE: stays open, comment only, behind -255 | PR #133 body: "The purchase projection is not built here ... until MPSCALC-255" |
| 3 MPSCALC-252 | Backlog, 1 comment (2026-10-20) | No | ACTIONABLE (lane 1) | Comment: purchase-pair test of version-diff route wanted with V4; no PR since |
| 4 MPSCALC-253 | Backlog | No | BLOCKED on -252 | ticket text "needs -252 first" (sweep) |
| 5 MPSCALC-258 | Backlog, 0 comments | No | ACTIONABLE (lane 1, after -252 or in sequence) | description: "Lane V4, tier 1, wave 2 (T-V4-7 to T-V4-12: any, after the D card)", D-03 a ruled |
| 6 MPSCALC-259 | Backlog, 0 comments | No | ACTIONABLE (same) | same wave 2 line, D-04 a ruled, "no default value is introduced" |
| 7 MPSCALC-261 | Backlog, label still needs-ruling, 1 comment (2026-10-24) | No | ACTIONABLE (ruling is in the comment; label stale) | comment: ruled 2026-10-24, "Not built". Touches the same Engine files; after -252 |
| 8 MPSCALC-255 / -257 / -315 | Backlog | No | BLOCKED on -252 (-315 on a -256 result field, which #133 has now partly supplied: re-measure) | sweep text; -315 not re-read |
| 9 MPSCALC-237 | Backlog, 0 comments | No | ACTIONABLE but serialise behind -252 (Dtos.cs, openapi.json overlap) | sweep |
| 10 MPSCALC-312 | Backlog | No | ACTIONABLE (S), same contract-sync pass as -237, after -252 | sweep |
| 11-13 MPSCALC-284/-285, -286/-287/-212, -269 | Backlog | No | ACTIONABLE; -284/-285 (importer, tools/MpsCalc.ImportCli, catalogue map) are the least likely to collide with lane 1, but "Engine software pricing" is shared; -269 after -252 | sweep; no new comments |
| 14 MPSCALC-161 | Backlog | No | ACTIONABLE with a new button word (use existing words) | sweep |
| 15 MPSCALC-343/-344/-349 | Backlog, 0 comments each | PRs #122 (panel tamper), #123 (Api csproj comment names the SDK tie), #124 (parity rows assert the refusal) merged 2026-10-26, before yesterday's sweep | UNVERIFIED: -349 very likely done by #123 (title matches the ticket); -343/-344 may be done by #122/#124. NOT read at the file level | PR titles only. A records seat should measure on main before closing |

Count of the 21 B987 keys still Backlog: all 21 (Done keys updated since the cutoff: 0).

Unchanged from yesterday: NEEDS-RULING and BLOCKED sets (MPSCALC-68..88, web screen lanes, etc.) have no new comment (0 comments at or after the cutoff on the whole board).

## 2. Security Composer (PCOMP; repo datasecau/Datasec-Security-Composer; main 075b2b23)

Board: 115 issues (was 113), 93 Backlog + 22 Done (was 100 + 13). New since the cutoff: PCOMP-114, PCOMP-115. Updated since the cutoff: 13 keys (114, 115, 97, 96, 95, 63, 62, 43, 41, 40, 22, 17, 14), all by the records pass of 2026-10-31 12:30 AEDT onward (comment timestamps 12:30 and 19:18 AEDT).

PRs: open #95 (Guided setup target lock, updated 2026-10-26), #91, #86 (dependabot), #85 (DRAFT, HOLD, L1 catalogue); all unchanged. Merged since: **#106 (075b2b23, 2026-10-31T07:52Z)** "Tests: pin a late digest verdict and a hash line after a closed string". Demo deploy at d70edf70 happened (pickup DELTA 855).

| Yesterday rank, keys | Status now | Touched since? | Class today | Evidence |
|---|---|---|---|---|
| 1 PCOMP-40 | **Done** | Moved 2026-10-31 12:30 AEDT | DONE | comment: PR #87 squash e019ac3a, migration 0025 |
| 1 PCOMP-43 | **Done** | Moved 12:30 AEDT | DONE | comment: migration 0023 |
| 1 PCOMP-41 | Backlog | Comment: recorded, not moved | BLOCKED (clause 2: approval-role list is content, content release held) | comment: "(2) ... NOT MET - the migration leaves the list out on purpose because it is content and the content release ... is held" |
| 1 PCOMP-42 (L3-4) | Backlog, 0 comments | No | ACTIONABLE (lane 2) | K5 ruled (C-91); description lines read |
| 1 PCOMP-44 (L3-6) | Backlog, 0 comments | No | ACTIONABLE (lane 2, after -42) | `sm_policy_json` code search 0 hits (control 0) |
| 2 PCOMP-36, -37, -38, -39 | Backlog, 2 comments each (2026-10-23) | No | ACTIONABLE as new data files under content/ (L2-3 -38 holds why-text: that is customer words, word pack first). Not chosen as a lane tonight: the L1 loader and the held draft #85 sit beside them and the value is lower than lane 2 | comments of 10-23 (C-100 approval; files disjoint from the loader) |
| 3 PCOMP-52 | Backlog, 0 comments | No | **NEEDS-RULING (words "Contents", K9 ruled a: goes on the lane's words card before it ships)** | description |
| 4 PCOMP-29 | Backlog, 0 comments | No | ACTIONABLE as records, but reads a sibling product's catalogue: Tuesday's call | description: "the coordinator's call" |
| 5 PCOMP-98 / -102 / -112 / -113 | Backlog | No (last updates 10-27 to 10-30) | ACTIONABLE (test-only, all in the Route B test file) | unchanged |
| 6 PCOMP-12, -83 | Backlog, 0 comments | No | ACTIONABLE (-83 is titled Blocker) | unchanged |
| 7 PCOMP-77, -82 | Backlog, 0 comments | No | ACTIONABLE; -82 needs a migration so after lane 2 | unchanged |
| 8 PCOMP-74, -75, -80, -81 | Backlog, 0 comments | No | ACTIONABLE (CSS only) | unchanged |
| 9 chores (-21, -23, -24, -15, -26..28, -66, -67, -93, -16, -13) | not re-read per key | no key in the updated list | unchanged | the 13 updated keys above contain none of them |
| (not ranked) PCOMP-62 | Backlog | Comment 2026-10-31 19:18 AEDT after PR #106: recorded, not moved; clause 2 NOT MET as written | BLOCKED/NEEDS-RULING (the regression as written was not run; PCOMP-114 is the reason) | comment text |

## 3. HPSM-POC (HPSMPOC; repo datasecau/HPSM-POC; main d0eff4ca)

Board: 425 issues (was 421 at yesterday's read), 243 Done + 179 Backlog + 3 In Progress (HPSMPOC-87, -90, -91, last updated 10-01 to 10-23, nothing to do with tonight's work). Updated since the cutoff: 43 keys.

PRs: open **#266 only** (b992/hpsmpoc-wake-tolerant-reads, head 7490fb36 = B998's subject). Merged since yesterday's sweep: **#262** (8ce48527, HPSMPOC-414), **#264** (68bf73cd, HPSMPOC-407 items 1+3), **#263** (c364caf0, HPSMPOC-413/416/418/419), **#265** (d0eff4ca, HPSMPOC-411/415/408). All three of yesterday's proposed lanes therefore landed in one day; every ticket got a landing comment ("BLUF: pull request N landed on main ...", each says "moves nothing and the ticket stays open").

| Yesterday rank | Status now | Touched since? | Class today | Evidence |
|---|---|---|---|---|
| 1 HPSMPOC-411 | Backlog, 1 comment | #265 merged | DONE-PENDING-RECORD (waits for a deploy of both hosted sites: product code) | comment 16:13 AEDT: "no deploy has happened" |
| 2 HPSMPOC-408 items 1+3 | Backlog, 1 comment | #265 merged | DONE-PENDING-RECORD for items 1+3; item 2 (limit sentences) remains NEEDS-WORDS | comment: "item 2 ... is words, stays open" |
| 3 HPSMPOC-413 | Backlog, 1 comment | #263 merged | DONE-PENDING-RECORD (test-only: moves "only on a records ruling, per ticket", precedent C-177..C-180, C-186) | comment of 407/413 style |
| 4 HPSMPOC-418 | Backlog, 1 comment | #263 merged | DONE-PENDING-RECORD (test-only) | comment |
| 5 HPSMPOC-415 | Backlog, 1 comment | #265 merged | DONE-PENDING-RECORD (product code, waits for deploy) | comment |
| 6 HPSMPOC-419 | Backlog, 1 comment | #263 merged | DONE-PENDING-RECORD (test-only) | comment |
| 7 HPSMPOC-416 | Backlog, 1 comment | #263 merged | DONE-PENDING-RECORD (test-only) | comment |
| 8 HPSMPOC-407 items 1+3 | Backlog, 1 comment | #264 merged | DONE-PENDING-RECORD for items 1+3; items 2 and 4 stay a ruling ("record as declined?") | comment |
| (ranked ASK) 405, 406, 409, 410, 412, 417, 420, 421 | Backlog, 0 comments each | No | unchanged: NEEDS-RULING / NEEDS-WORDS (Monday bundle) | 0 comments on each |
| 414 | Backlog, 1 comment (PR #262) | merged | DONE-PENDING-RECORD (test-only) | comment |

Deploy fact new since yesterday: a UAT review-copy deploy of main e8ac3f29 ran 2026-10-31 11:27 to 11:30 AEDT (B971). 28 HPSMPOC tickets carry its comment (keys 357, 363-368, 371-387, 398, 401, 403, 404; regex count with 0-hit control above); all 28 are still Backlog by design because "the Done rule is applied to a deploy of both hosted sites; the demo is held" (comment quoted on HPSMPOC-365). They are not a records lane tonight; they move with the demo release.

## 4. NEW tickets since 2026-10-31 12:00 AEDT

Parsed-timestamp result: MPSCALC none; PCOMP-114, PCOMP-115; HPSMPOC-421 (created just after 12:00 and already covered by yesterday's sweep), HPSMPOC-422, -423, -424, -425.

| Key | What | Class | Evidence |
|---|---|---|---|
| PCOMP-114 | Engine timing test (packages/engine/test/performance.test.ts) times out at 5000 ms under a CPU cap; test-only; fix shape: raise the row's timeout or budget | NEEDS-RULING ("State. Not started; NOT RULED, awaiting the product owner") | description, last paragraph |
| PCOMP-115 | CI typecheck reads nothing under packages/db/test (1110-line deploy-guide test never typechecked); test-config only | NEEDS-RULING (same sentence) | description |
| HPSMPOC-422 | QuestionBlock.tsx line 45 not-applicable anchor id pinned by no row (Minor, test-only) | ACTIONABLE (lane 3); reachability of the variant is unmeasured | description: Done-when allows a row, or "the branch shown unreachable" |
| HPSMPOC-423 | Blank-evidence list misses 3990 code points (remediation-store.ts:22) (Minor) | ACTIONABLE with a stated default (lane 3); note the ticket calls the U+1BCA0 range "a scope call that is not made here" | description |
| HPSMPOC-424 | One old Verified-complete entry with invisible-only evidence makes the whole saved register read as empty after reload, no message | NEEDS-RULING ("product question") | summary |
| HPSMPOC-425 | Invisible-only evidence still accepted for Evidence submitted / Not started / In progress | NEEDS-RULING ("product question") | summary |

## 5. UNMEASURED (could not or did not check)

- Hosted state of every site (no probe, as fenced). The e8ac3f29 UAT deploy and the Composer demo at d70edf70 are RELAYED (ticket comments and the pickup), not probed.
- CI state of MPS #120/#121 and Composer #86/#91 (not read).
- Whether MPSCALC-343, -344, -349 are already fixed by PRs #122-#124 (titles matched, files not read); likewise the other old MPSCALC residue of yesterday's ranks 16-21 (no key in them was updated; not measured on main).
- Whether `-315` is now unblocked by the result field #133 added (not read).
- Whether PCOMP-42 is partly built under another name: code search for `remediation_state` and `remediationState` found 0 files, `after_validation` found 3 test/route files for attribute overrides (a different feature), but `controlled_staged` found 0; the builder must measure on main first.
- Whether PCOMP-44's contract enum can change without a renderers change (document.ts:283 comment says the API checks the two lists agree).
- Whether the QuestionBlock not-applicable variant (HPSMPOC-422) can be drawn for the seeded customer: the ticket says nobody measured it.
- HPSMPOC tickets outside 405-425: 161 non-Done tickets were counted but only 356-367, 398-404 were skimmed by last comment; no classification of the rest (design-v12 parents 368-389 look landed, `gather` tickets 390-396 need input).
- Open B998 / B999 state beyond their STATUS first lines (`PROGRESS ... PENDING` on both; B999 started 00:28 AEDT with READY target 01:28). The HPSM-POC root repo's `core.sshCommand` names a missing key (pickup DELTA 859): any HPSM records lane must check it first.
- Jira "comment truncation": 0 issues returned fewer comments than their total on all three boards, but comment text was cut to 1500 characters in my working copy; classifications that rely on the tail of a long comment (PCOMP-62, PCOMP-41) were read for the quoted passages only.
