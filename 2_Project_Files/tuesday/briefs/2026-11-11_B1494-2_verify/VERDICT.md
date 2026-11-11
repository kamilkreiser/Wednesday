GATE B1494-2: GO WITH FINDINGS @ 3192a71 on main 54ed762

Tier G1 (Opus), round 2 of 2 (the cap). Subject: branch b1494/mps-api-stores @ 3192a71dfc4883c21d617c6e960df6e74ab541b2 (round 1 gated b225dbcf; one fix commit on top). Gate run 2026-11-11 16:42-16:59 AEDT. Own clone and worktrees under /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s267/gate1494r2/ (cloned from round 1's clone by copy, push URL INVALID-NO-PUSH, nothing pushed). The round-1 folder was read only.

## Why GO WITH FINDINGS (one line)
Round 1's Major is closed: the round-1 probe answers 500 at b225dbc and 503 FEEDBACK_STORE_UNAVAILABLE at 3192a71, with main's exact words, main's log line and nothing left in the store. Every new row is red without the fix, the seam is absent from the app, the diff stays in the lane, and the suite passes 4420/0. No new Major. What is left is two Minors: one behaviour change from main on a rare operator-fault shape, and round 1's deploy note.

## Findings

| # | Sev | Ticket | Finding | Evidence |
|---|---|---|---|---|
| 1 | Minor | MPSCALC-123 | **Removed store directory plus a file: main answers 201 (it re-creates the store and stores the item); head answers 503.** Measured with the same probe at all three trees: main `201`, store re-created with the item and its attachment; b225dbc `400 BAD_REQUEST "not well formed"`; head `503 FEEDBACK_STORE_UNAVAILABLE` with the exact words and log line, nothing created. The same shape WITHOUT a file answers 503 at all three trees (multipart and JSON alike), so head is now consistent with main's own no-file answer. The answer fails closed and says try again. The fix kit asked for exactly this ("removed directory" was listed as a write-failure shape). The builder disclosed it (STATUS FOR TUESDAY, reading 2). Not a refusal-words change, and no test at main pins the 201. It is a decision, not a defect: if Tuesday wants main's self-healing back, that is a follow-up ticket (the spool would re-create the store root). | `out/probe-final-{main,base,mut}-tree.txt` lines P2 |
| 2 | Minor (deploy note, carried) | MPSCALC-217 | Round 1's Minor 2, unchanged: suppose an Administrator staged and activated a reference store through the admin route before this change, and it holds a repeated (sheet, SKU) pair. After the deploy, that store answers 503 SOURCES_UNAVAILABLE the first time it is needed. Look at the active stored version before the deploy card. Written into pr-body.txt as a deploy note. | round 1 VERDICT row 2 |
| 3 | Minor | STATUS | Two STATUS figures cannot be reproduced exactly here, and neither one weakens the work. (a) The package zip sha256 `717e02eb...` is not reproducible by design, because entries are stamped with the run time. My run at the same head: rc 0, markers 0/57, B2 0 hits, zip sha256 `8052223c...`. (b) The two full-suite runs were taken at load 19.5 and 23.3, and STATUS says so itself. | `logs/package.log` |
| 4 | Info | MPSCALC-123 | The fix also closes a family of 500s that round 1 did not list: in an unwritable store, b225dbc answered a raw 500 for a bad-type file, a second file over the limit, an invalid message, a reused key and a replay. Head gives main's answer for every one of them: 415, 413, 400, 422, 200 (table below). | `out/probe-final-*.txt` lines P3 |

No Blocker: every path is in the lane, there is no secret, no name, no red at head, no hosted touch, and nothing is deployed.

## (1) Round 1's Major probe, re-run (`GateProbe123_a_store_directory_that_cannot_be_written_answers_503_store_unavailable`, round 1's file copied unchanged; the whole FeedbackGateProbe123 class, 15 rows, at each tree)
| Tree | Major probe | Whole class |
|---|---|---|
| main 54ed762 | 503 FEEDBACK_STORE_UNAVAILABLE (pass) | 15/15 pass (load 15.7-27.2) |
| b225dbc | `500 (not json); System.UnauthorizedAccessException: Access to the path '<store>/.upload-<id>.tmp' is denied` (fail) | 14/15 (load 16.6) |
| head 3192a71 | 503 FEEDBACK_STORE_UNAVAILABLE (pass) | 15/15 pass (load 15.7) |

My own probe (`FeedbackGateR2Probe`, same file at all three trees) adds the words, the log line and the leftovers:
| P1 unwritable store (0500), one 4 KiB PNG | main | b225dbc | head |
|---|---|---|---|
| answer | 503 FEEDBACK_STORE_UNAVAILABLE | 500 (not json) | 503 FEEDBACK_STORE_UNAVAILABLE |
| detail equals "The feedback could not be saved just now. No feedback item was stored; try again (the same key is safe to reuse)." | True | False | True |
| server path / "Exception" in body | False / False | True / True | False / False |
| log line | `Feedback was not stored: FEEDBACK_STORE_UNAVAILABLE (the write failed).` | none | same as main |
| .tmp left / store entries changed | 0 / no | 0 / no | 0 / no |
P1b (a PNG and a PDF, unwritable): main 503 with the words and the log line; base 500; head 503 with the words and the log line; nothing left. The words sentence and `"the write failed"` each appear once in FeedbackEndpoints.cs at all three trees. The `case SubmitOutcome.WriteFailed` block is byte-identical at main and head (`diff` of the extracted block).

## (2) The fix's own claims
| Shape | main | b225dbc | head |
|---|---|---|---|
| removed directory, PNG | 201 (store re-created; finding 1) | 400 BAD_REQUEST | 503 FSU, words exact, log line, dir not re-created |
| removed directory, multipart no file | 503 FSU | 503 FSU | 503 FSU |
| removed directory, JSON no file | 503 | 503 | 503 |
| unwritable: bad-type file only | 415 FEEDBACK_ATTACHMENT_TYPE | 500 | 415 |
| unwritable: PNG then bad-type | 415 | 500 | 415 |
| unwritable: PNG then over 5 MiB | 413 FEEDBACK_ATTACHMENT_TOO_LARGE | 500 | 413 |
| unwritable: empty message plus PNG | 400 BAD_REQUEST | 500 | 400 |
| unwritable: key reused plus PNG | 422 IDEMPOTENCY_KEY_REUSED | 500 | 422 |
| unwritable: replay of a stored PNG upload | 200 | 500 | 200 |
In every unwritable row: no "the write failed" log line, .tmp 0, store entries unchanged.
**Abort controls, unchanged at all three trees:**
- **P4: the client cancels mid-part**, using a non-buffering client taken from the rig's own factory. At all three trees the client sees `TaskCanceledException`, 0 items are stored, .tmp afterwards is 0, and no write-failed line is logged. The .tmp count mid-part is 0 at main (held in memory) and 1 at base and head (streamed).
- **P5: the request body throws an IOException after half a file**, sent through `ReadMultipart` by reflection (3 parameters at main, 4 at base and head). At all three trees the answer is `refused 400`, logged `BAD_REQUEST (part or file 2)`. `spool.Fault` is null at base and head, so the mapping did not swallow it. The half file is gone after the spool is disposed.
**Nothing created or left:** this holds for P1, P1b and P2, and for the builder's spool-fault rows ("store directory EMPTY"), which pass at head.

## (3) The test seam is test-only
- Static: `FeedbackSeams` is never registered in `src/`. Its only use is `app.Services.GetService<FeedbackSeams>()` at `FeedbackEndpoints.cs:53`, and `store.OpenSpoolFile` is set in one place, `:63`, from `seams?.OpenSpoolFile`, once at map time. No request path writes it. `FeedbackStore.OpenSpoolFile` is `internal`. `InternalsVisibleTo` names only `MpsCalc.Api.Tests` (`MpsCalc.Api.csproj:9`). The type is a `Func<...,FileStream>`, which no configuration binder can produce, and nothing in `src/` binds `FeedbackSeams` (no `Configure<`/`Bind(`/`Get<` on it). Registration is found in tests only (`FeedbackApiTests.cs:33`, `ConfigureTestServices(s => s.AddSingleton(Seams))`).
- Runtime: P6 builds the real app (ApiHost, without the rig's test services) with five configuration keys set (`OpenSpoolFile`, `FeedbackSeams:OpenSpoolFile`, `FeedbackSeams`, `MpsCalc:Feedback:OpenSpoolFile`, `MpsCalc:Feedback:Seams:OpenSpoolFile`). Result at head: upload 201, `GetService<FeedbackSeams>` null. It then walks the POST endpoint's delegate graph to the app's own FeedbackStore: `OpenSpoolFile` null. **Control P6b** (a rig whose test services set an opener): the same walk reads `SET Func`3`, so the walk can see a set seam.

## (4) Diff b225dbc..3192a71
6 paths, all under `src/MpsCalc.Api/Feedback/**` (4 modified) and `tests/MpsCalc.Api.Tests/**` (2 added). Outside: 0. Control: a planted `web/x.ts` makes it 1. **Removed lines under tests/: 0.** Control: the same count over main..b225dbc reads 14, which is round 1's figure. All removed lines: 14, all product lines in Feedback. No string literal is added in product code outside comments (0; control main..b225dbc: 4). The commit is a fast-forward (b225dbc is an ancestor). Whole branch: 15 paths vs main, 0 outside round 1's OWNS plus ANSWER-1's file. Ahead 5, behind 0. `git merge-tree --write-tree main head` rc 0, tree `17c1dcdd...` = head tree. `ls-remote` at 16:42 and 16:58: branch 3192a71dfc4883c21d617c6e960df6e74ab541b2, main 54ed76273cf5e7eb804315635c413034f28b3372 (unmoved).

## (5) Full suite at head and names
Job dotnet in a clean head worktree (porcelain 0): build `0 Warning(s)` `0 Error(s)`. Test rc 0, trx counters Engine 743/743, Import 196/196, Api 3481/3481, **4420 passed, 0 failed**. Run window 16:45-16:57, load 13.0 at the start and 25.3 at the end. Names (`--list-tests`, sorted) were compared with round 1's measured b225dbc list (4411): **lost 0**, gained 9, exactly the builder's 9 rows (5 WriteFailure, 4 SpoolFault). Control: `comm -23` of a two-line file against a one-line file prints 1.
**Red without the fix:**
- Head's `LaneL2FeedbackUploadWriteFailureTests.cs` on the b225dbc product: 3 RED (`unwritable`: 500 UnauthorizedAccessException; `removed`: 400 "not well formed"; bad-type: 500). The 2 abort controls are GREEN, as designed.
- Plants at head, each undone with `git diff --quiet` checked after:
  - **A, write/create mapping removed (`throw;`):** 16 red, including both WriteFailure 503 rows, the bad-type row, SpoolFault `write`, refusal-after-failed-write, key-reuse, GateProbe123 and my P1/P1b/P2/P3. Controls P4/P5 and both builder controls stay green.
  - **B, fault recorded but not raised in SubmitWith:** 4 red (`removed`, SpoolFault write and flush answering 201, P2). In that mutant the `unwritable` rows stay green: the later directory create fails on its own.
  - **C, flush mapping removed:** SpoolFault `flush` red (400). Every other row green.
  So each wrapper is pinned by at least one row.
Package job at head (Node v24.22.2, npm offline): rc 0, markers 0/57, B2 scan 0 hits (load 18.3-23.9). Python job: no python test names a changed path (0 hits for each of the 6 changed names; the positive control `CatalogueOverlayStore` gives 1). Not run this round.

## (6) Round 1's GREEN findings, light re-check at head (product files for 217/99/122 unchanged b225dbc..3192a71)
- **MPSCALC-217:** round 1's `GateProbe217` theory at head: adjacent, first-and-last, last-row, triple and other-price all 503. Same SKU on another sheet, same sheet with another SKU, case-variant and trailing-space all 200. Null vs "" sheet 503 (round 1's REPORT arm; it prints 503 x3). Identical to round 1's head reading. Load 20.0-24.5.
- **MPSCALC-99:** `GP99_a_short_body_with_the_store_held_answers_busy_at_the_bound_from_arrival` passes at head. Load 20.0-24.5, a pass-or-fail row with a margin, not a timing figure.
- **MPSCALC-98:** with the c1 mutant planted at head (`CatalogueOverlayStore.cs`, `before = Task.CompletedTask`), all 4 named tests are RED. Clean, they are 4/4 GREEN (load 22.8-25.4). The mutant was undone and the diff is empty.
- **MPSCALC-122:** the `Download` handler (FeedbackEndpoints.cs from `:413` to the end, 202 lines) is byte-identical at b225dbc and head. The hosted header rows pass in the head suite.

## (7) Scans over b225dbc..3192a71 (470 added lines, 1 commit message)
Ban-list names, underscore-aware (`(?<![A-Za-z])<name>(?![a-z])`; Kam, Kamil, Kreiser, Steve, Peter, Paul, Blanchard, Inch, Waite, Tuesday, Wednesday, Friday): 0. Control `x_by_kam_y` fired. B-numbers and seat ids: 0 (control `B1505`/`SEAT-` fired). Non-ASCII: 0 in the lines and 0 in the message (control U+200B gave 1). Cf characters: 0. GUIDs, hosts, ghp_/AKIA/PEM/JWT: 0. Emails: the attribution address only. gitleaks 8.30.1: canary rc 1, then range rc 0 ("1 commits scanned, no leaks found"). **CodeQL pre-scan:** `new RegExp(`, `new Regex(`, Regex calls, `.replace(/` hand-escape, `innerHTML`, `dangerouslySetInnerHTML`, `child_process`, `Process.Start`, `eval(`: all 0 (control fired). Bare `catch {`: 0. The 3 new catches are filtered (`when ex is IOException or UnauthorizedAccessException`). `Thread.Sleep`/Skip/`#pragma`: 0. `Task.Delay`: 2, both polls waiting for a state in a control row (allowed). Identity: author and committer both equal the project repo's configured email. Attribution trailer count 1. Subject 116 characters, ending `(MPSCALC-123)`.

## (8) B1505 STATUS claims
| Claim | Grade |
|---|---|
| One commit 3192a71, fast-forward of b225dbc, ls-remote = sha | TRUE |
| Ahead 5 / behind 0; 15 files vs main; 6 this round, all in Feedback/** and tests/** | TRUE |
| Unwritable store: 500 at b225dbc, 503 FSU with existing words and log line at head; partial file removed | TRUE |
| Removed directory: 400 at b225dbc (not 500 as round 1's text said), 503 at head | TRUE (round 1's "removed directory gives 500" was DERIVED, not measured; corrected) |
| At main a removed directory with a file answers 201 and re-creates the store | TRUE (finding 1) |
| Bad-type file in an unwritable store: 500 at base, 415 at head | TRUE |
| Abort and request-body faults keep their b225dbc and main answers | TRUE (P4, P5) |
| b225dbc 4411/0; head 4420/0 (= +9); names lost 0, gained exactly 9 | TRUE (head measured here; base list from round 1's measurement) |
| Build 0 warnings | TRUE |
| Removed test lines 0; removed product lines 14 | TRUE |
| Red-first: 3 red at base, controls green; plant 1 reds; plant 2 turns flush red | TRUE (reproduced as plants A and C; plant B added here) |
| Existing words count 1 each; no new string literal in product code | TRUE |
| Nothing created in the store on the failure path | TRUE |
| Seam is null in the app and set by tests only | TRUE (static, plus runtime with control) |
| Package rc 0, markers 0/57, B2 0 | TRUE (zip sha not reproducible by design; finding 3) |
| Scans clean; gitleaks canary 1 then 0; identity equal | TRUE |
| Full-suite load reads 19.5 / 23.3 | NOT SHOWN here (self-disclosed; no timing row depends on them) |
| `predictions.txt` written after the first red run | self-disclosed slip; no effect on the result |

## Is anything left that blocks landing?
No. Round 1's Major is closed by measurement, and so are round 1's rows 1 and 3. Rows 2 and 4 of this verdict are notes for Tuesday: a deploy check, and a decision on finding 1 if main's self-healing on a removed directory is wanted back. That would be a new ticket, not a gate item.

## NOT RUN
- Hosted CI and CodeQL: these are the landing proof.
- Open-PR overlap and sibling branches: they need the GitHub API, which the fence bars.
- The python job loop: it needs `az bicep`, which the fence bars, and no python test reads a changed path.
- Web and e2e jobs: no web path changed.
- RSS re-measurement for 123: the streaming path is unchanged by this round.
- The base full suite was not re-run. Round 1 measured it (4411/0), and its name list is reused.
- MPS heavy-lock directories: they are inside the project folder, which this gate may not write. Heavy jobs ran gated on load1 < 24, with load printed beside each result. Peaks of 25-27 occurred while my own full suite was running. Every result here is pass/fail, not timing.
- Kestrel real-socket abort: covered by the existing Kestrel suite, which passes in the head run.

## Trees (gitignored, under fleet/state/s267/gate1494r2/)
- `clone`: push URL INVALID-NO-PUSH.
- `main-tree`, `base-tree`, `head-tree` (porcelain 0), `mut-tree` (tracked diff empty after every plant), `pkg-tree`.
- Untracked probe copies in the main, base and mut trees.
- `scripts/` (FeedbackGateR2Probe.cs, probe.sh, batch.sh, plant.py, run_ci.sh, pkg.sh, scan.py).
- `logs/` (batch.txt, ci-head-tree.txt, gp123-*.log, b-test-*.log, package.log).
- `out/` (probe-final-*.txt, names-head-tree.txt, trx-head-tree, gitleaks-*.log, added.txt, msgs.txt).
- `pkgout/`; `pkgout-empty-unused*` (two empty dirs from a refused first run).
No process is left running and no port was used.
