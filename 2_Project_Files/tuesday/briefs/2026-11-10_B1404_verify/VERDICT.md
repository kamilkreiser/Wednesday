GATE B1404: GO WITH FINDINGS @ f827f2d on main 089a639

Tier G1 (kit S8: product code, src/MpsCalc.Api/Sources/**). Gate run 2026-11-10 08:10-08:56 AEDT in a private clone under the
gate session scratchpad (fetch from origin by deploy key, push URL set to invalid://no-push, nothing pushed). No PR, no Jira,
no mail, no az, no gh API call.

## Summary
- Branch b1404/mps-source-lifecycle-validator = f827f2d7e5bc97e5a368c07c4cad8a477ccb83fd at origin (git ls-remote 08:10:31) = READY sha.
- Two commits on base 31234f5f: MPSCALC-99 (a step waiting for the source store locks holds no thread) and MPSCALC-189
  (only the canonical-singleton half: U+0340/U+0341/U+0343 read as U+0300/U+0301/U+0313 in source version ids).
  331, 90 and 92 are ALREADY-ON-MAIN (no commit); re-verified at current main by program (below).
- Main has moved to 089a63939c5b787168264862b35919e895b0211d (behind 2, ahead 2). Merge is clean and equals main plus the 5 head blobs.
- CI job dotnet, by program from trx, at main / head / merge: all green, build 0 warnings in all three; merge = main + exactly the 16 new rows.
- Red without the fix: 4/4 (99) and 6/6 (189) red-first rows go red with the fix removed.
- Adversarial probes (7 throw-away rows) all green at head. Two mutants of the 99 fix survive every test (findings F1, F3);
  one is caught by a single row by a thin margin (F2). None is a defect at head; they are guard gaps.
- No blocker: 5/5 paths in OWNS, 0 overlap with sibling lanes, the feedback lane or new PR heads, no secret, no name, no deploy trigger.

## Findings
| # | Severity | Finding | Evidence |
|---|---|---|---|
| F1 | Minor | The async lock-file poll half of MPSCALC-99 has no guard. A mutant that puts `Thread.Sleep(LockPoll)` back into `TakeFileLockAsync` (src/MpsCalc.Api/Sources/SourceLifecycle.cs, the `await Task.Delay(LockPoll)` line) passes every test. Cause: in-process steps queue on the turn chain first, so only one step per process polls the file lock at a time. A sync sleep there costs one thread, not 64. Impact at head: none, because the code is async. Gap: a revert of that line would pass CI. | Mutant M3: filter LaneM5, GateProbeM5, SourceLifecycle: 533/533 passed, rc 0. |
| F2 | Minor | The blocking-turn mutant is caught by 1 of 4 rows, by a thin margin. A mutant that waits for the turn with a blocking `before.Wait(...)` inside `StepAsync` turns only the `stage` row red: 3/64 late, max 2647 ms against a 2500 ms limit. The validate, activate and rollback rows stay green. The full revert (M1) is caught 4/4. On this 18-core machine the pool headroom absorbs most of the blocking, so the rows' power against this exact mutant is marginal. | Mutant M5: 532/533, 1 failed. Mutant M1: 529/533, the 4 LaneM5_99 rows failed (13-40/64 late, max 4.0-6.0 s). |
| F3 | Minor | The in-process hand-off order is not guarded. The builder disclosed this one. A mutant that completes a timed-out step's turn at once instead of handing it off passes every test, including my probe P3. The store lock file serialises the steps anyway (FileShare.None conflicts within the process too), so the mutant is observably equivalent today. The turn chain is defence in depth. | Mutant M4: 533/533 passed. Probe P3 at head: the order is correct (A 201, B 500 Busy at 1349 ms, C 201 at 1659 ms; log `seam1 releasing A-released seam2`). |
| F4 | Major (rubric: claim contradicted) | STATUS RESIDUE says "test files calling them 7" for the public sync step methods. Measured: 1 test file calls them (SourceLifecycleTests.Activate.cs:205, `lifecycle.Activate(...)`). The 7 match a loose grep that also counts `ReferenceDocumentValidator.Validate` calls in MpsCalc.Import.Tests (4 files) and `.Stage` property reads (GateB41). The companion claim "src callers 0" is true. This does not touch product code. | `grep -rn -E '\.(Stage|Validate|Activate|Rollback)\(' tests/` with validator and checks calls excluded: 1 line. |
| F5 | Minor | The 99 red counts are timing-dependent and do not reproduce exactly. STATUS reported 29-40/64 late at base. My revert copy measured 40/13/36/18 of 64 (stage/validate/activate/rollback). Red is reproduced; the counts are not. | trx of mutant M1. |
| I1 | Info | The commit author on both commits is the repo-local identity (the owner's name and corporate address). It is not in any commit message or added line, and the squash writes its own commit. Listed so Tuesday can see it. | `git log --format='%an <%ae>'`. |
| I2 | Info | Open residue stays open: MPSCALC-331's location clause for the 10 null-product shapes (coordinator ruling 2026-10-25, per STATUS), MPSCALC-189's docs sentence (docs/API.md, lane M11), and the declared Unicode classes (U+0344, compatibility forms). The PR must not say it closes 331, 90 or 92, or 189 as a whole. | STATUS RESIDUE; probe P7 confirms U+0344 is unchanged. |
| I3 | Info | Process notes the builder disclosed itself: one early `cd`, and one control file written outside its write set. No effect on the branch. | STATUS Step 0 process notes. |

## Steps and instruments
1. **Refs.**
   - `git ls-remote` (deploy key, read only): refs/heads/b1404/mps-source-lifecycle-validator = f827f2d7 = READY, and main = 089a6393.
   - Changed paths (main...head): 5. All 5 are in OWNS by fnmatch over the kit's three globs (control: web/x.ts is outside OWNS).
   - Sibling lane OWNS (M1-M4, M6, M8-M11): 0 hits (control: a Feedback path hits M6, so the check can fire).
   - Feedback lane branch b1405/mps-feedback-backend (2c7d5c28): 10 files, all in src/MpsCalc.Api/Feedback/** and tests/Feedback*; overlap with this lane: 0.
     Three-way merge main + this branch + the feedback branch by `git merge-tree`: clean (rc 0). The feedback branch does not reference SourceLifecycle or OverlayTimingGroup.
   - PR heads above #166: #167 (= the docs lane head, docs/IMPORTER.md) and #168 (= the template-pins lane head, TemplateIsolationTests.cs); overlap 0.
   - Over all 361 fetched refs not contained in main: 15 old refs touch these paths. All are branches or PR heads of landed
     work (PR #27, #29, #55, #56, #59, #100, and their source branches). Open/closed state was not read (no API).
2. **Merge.** `git merge-tree --write-tree origin/main f827f2d7` rc 0, tree 95096180.
   - `diff main merge` = exactly the 5 lane files.
   - `diff head merge` on those 5 = empty. The rest of `diff head merge` = main's 2 newer files.
3. **CI** (ci.yml at head; the jobs are dotnet, web, python and package; only dotnet reads the changed files). Project-local SDK
   10.0.401; global.json pins 10.0.100 with rollForward latestFeature. Restore used the local package cache only.
   Build and test were the CI commands, with `--no-restore` and a trx logger added.

   | tree | build | Engine | Import | Api | failed | rc |
   |---|---|---|---|---|---|---|
   | main 089a6393 | 0 Warning(s), 0 Error(s) | 743/743 | 196/196 | 3382/3382 | 0 | 0 |
   | head f827f2d7 | 0 Warning(s), 0 Error(s) | 743/743 | 196/196 | 3383/3383 | 0 | 0 |
   | merge (local) | 0 Warning(s), 0 Error(s) | 743/743 | 196/196 | 3398/3398 | 0 | 0 |

   - Names main vs merge: lost 0, gained 16, all `LaneM5*`.
   - Head vs main lost 15: these are main's newer TemplateIsolationTests rows (head is behind main), and the merge has all of them.
   - 99 rows at merge: late 0/64 on every step, max 2013-2029 ms against a 2000 ms bound, read 0.3-0.5 ms.
   - Repo-wide hidden-character scan (Unicode Cf, every tracked text file):
     - main: 17 in 6 files. head and merge: 17 in the same 6 files. Added by this lane: 0.
     - The 6 files are existing test fixtures and scripts/tests/test_deploy_pre1.py.
   - No link check applies: no docs changed, and CI has no link job.
4. **Red without the fix** (copies of head, only the fix reverted):
   - M1 (SourceLifecycle.cs and SourceAdminEndpoints.cs from main): the 4 LaneM5_99 rows fail, each for lateness.
   - M2 (SourceDocumentChecks.cs from main): the 6 LaneM5_189 red rows fail with exactly 36/18/52 of 52 letters
     (U+0340/U+0341/U+0343). Probe P7 fails too.
   - The 6 189 control rows stay green under M2, as designed: they are controls, not red-first rows.
5. **Closed lines at current main 089a6393:**
   - 331: guards at src/MpsCalc.Import/Validation/ReferenceDocumentValidator.cs:161, :166 and :203. 15/15
     `GovernedNull_a_staged_document...` rows pass at main. Mutant M7 removes the :166 and :203 guards: 77 SourceLifecycle rows
     go red with 500 (all 15 GovernedNull rows among them), so the rows hold the fix.
   - 90: SourceLifecycle.cs:917 (IOException/UnauthorizedAccessException leads to worded refusal) and :974 (versions not a real directory).
   - 92: SourceDocumentChecks.cs:326 (IsDocumentFault narrowed).
   - Store-hardening rows at main (`B53_` test-name prefix): 63 names, all passed.
   - 189 half 1 (fail-closed state words): SourceDocumentChecks.cs:252 on main, landed by e3624f0.
   - 331's PR #110 squash 8b046423 is an ancestor of main.
6. **Probes** (throw-away GateProbeM5Tests.cs at head; 7 rows, all green; never committed):
   - P1: 24 parallel stage requests on a free store: all 201, versions +24, event sequences unique.
   - P2: 8 route stages and 8 synchronous `Stage` calls mixed: all succeed, versions +16.
   - P3: hand-off. A holds the turn inside the registry write. B gives up (500 Busy at 1349 ms). C arrives after B and goes
     through once A finishes; C's write starts after A's.
   - P4: a step whose body throws (IOException at the write seam) frees the line. The next step is 201 in 9 ms.
   - P5: LockTimeout = 0 on a free store still succeeds, by the route and by the synchronous call.
   - P6: the synchronous Stage with another holder of store.lock throws Busy at 1024 ms against a 1 s bound.
   - P7: IdKey edges. Precomposed + U+0343 equals + U+0313. A leading U+0340 equals U+0300. Case folds. U+0340+U+0341 equals
     U+0300+U+0301. e+U+0341 equals U+00E9. U+0343 and U+0314 stay apart. U+0344 is unchanged (declared residue). Surrogates
     pass intact. Null gives "". ASCII is untouched.
   - The doc-comment fact "only U+0340, U+0341 and U+0343 in U+0300-U+036F decompose to one other mark" is confirmed by python
     unicodedata 13.0.0 (U+0344 decomposes to two marks).
   - The CA1001 fact for the ticket's SemaphoreSlim shape is confirmed: the builder's log holds
     `error CA1001: Type 'SourceLifecycle' owns disposable field(s) '_gate'`.
7. **Scans** (added lines: 428; commit messages: 2):
   - Name scan `(?<![A-Za-z])<name>(?![a-z])`, case-insensitive, over the ban list: 0 (planted `_by_<name>_` controls fire for the first and last names on the list).
   - B-numbers, seat ids and finding ids: 0 (control fires).
   - Secret regex: 0 (control fires).
   - gitleaks 8.30.1 on the range: rc 0, "no leaks found". The canary (a random ghp_ token) gives rc 1.
   - GUIDs and tenant/subscription ids: 0 (control fires). Hosts: 0 (control fires).
   - Non-ASCII lines: 0. Cf characters: 0 (control fires).
   - The commit subjects carry only the ticket keys.
8. **Claims** (builder STATUS):

   | claim | grade |
   |---|---|
   | READY sha read back at origin | true |
   | 2 commits, 5 files, all in the lane | true |
   | dotnet predicate at head: 0 warnings, 4322 tests, 0 failed | true (743+196+3383) |
   | lost 0, gained exactly 16 LaneM5 rows vs base | true by count at head; vs current main the merge is lost 0 / gained 16 |
   | base counts 743/196/3367 = 4306 at 31234f5f | not shown (I ran current main 089a6393: 3382 = 3367 + main's 15 new rows, consistent) |
   | 10 red / 6 green on unchanged product code | true (M1 and M2 reproduce 4 + 6 red; the 6 controls green) |
   | 189 counts 36/18/52 = 106 | true |
   | 99 base counts 29-40/64 late | true in kind, counts not reproduced exactly (F5) |
   | head 99 rows late 0/64, max about 2.02-2.03 s | true |
   | SemaphoreSlim shape fails CA1001 | true (log) |
   | ALREADY-ON-MAIN 331/90/92 at the cited lines | true at 089a6393 |
   | main moved to 089a6393 via docs/IMPORTER.md and TemplateIsolationTests.cs only | true |
   | sync step methods: src callers 0 | true |
   | sync step methods: test files 7 | false, measured 1 (F4) |
   | gitleaks rc 0 on the range | true (re-run) |
   | U+0344 the only other decomposing mark, left as is | true |
   | Seen outside scope: none | not contradicted |
9. **Tier.** G1 followed: the product code was probed adversarially (P1-P7, mutants M1-M7). No security-shaped issue found.
   The change narrows thread use and widens one duplicate rule. It adds no new refusal words and no contract change: the Busy
   text, SOURCE_STORE_WRITE_FAILED and DUPLICATE_SOURCE_VERSION_ID are unchanged.

## Deploy
None would trigger. ci.yml has no deploy job. On a main push its package job only keeps a build artifact for 7 days, and
deploying it is a manual runbook step. There is no other workflow in .github/workflows.

## NOT RUN
- Hosted CI (dotnet, web, python, package) and CodeQL. Hosted CI and CodeQL on the PR are the proof.
- The 99 timing rows have not been seen on the hosted ubuntu runner. They share the OverlayTimingGroup fixture with the overlay
  timing rows that already run there.
- web, python and package jobs, locally: no changed path is read by them. The python job needs az bicep and walks no source file.
- Open/closed state of old PRs: not read (no API by the fences). PR heads #167/#168 checked by ref.
- Mutant M7 was run at head, not at main. The validator file is identical at main and head, because the lane does not change it.
