GATE B1586: GO WITH FINDINGS @ 7868012 on main d607c8f

Tier G1 (kit S8 / GATE-ROUND slot: client-tester deliverable, round 1 of 2). Head 78680128ad0c0e5c4800f99077a4251a92a7382b (git ls-remote equals READY, read 21:32 and 22:18 AEDT). Main read 21:32 = f4e79a7a (PR 320 landed); re-read 22:16 and 22:18 = d607c8fb1f204042d0a7ada63610072970df8ab0 (PR 321, lane P, landed while I ran; open PRs now 0). Counts below are on the merge with f4e79a7 (tree 6f9bf12e); the merge with d607c8f (tree aa92d455, clean) differs from it ONLY in the 8 lane-P web files, and its `api/`, `infra/` and `.github/` subtrees are hash-identical (b4c968eb, 8dddb559, d9585f42), so every api, SQL and infra count carries over exactly; the hidden-characters scan (walks all tracked files, web included) was re-run on aa92d455: 14 OK.

The dead gate's files (landing.txt, pr-body.txt, pr-title.txt, squash-body.txt, squash-subject.txt, work/) were moved, not deleted, into `_dead_gate_2015/` (ls -la before and after printed 21:32). None of their content was used.

## Ruling asked of this gate: the sensitive-NAME hits on `BrandTokens.*`
**Name-only false hit. Not a CodeQL shape. No fix owed.** Reasons, at source:
1. The 5 added lines (`Layout.cs` 91, 95, 105, 106, 107) pass `BrandTokens.Primary/.Accent/.Fg/.Border` (static readonly `Rgb` colour structs, `Pdf/BrandTokens.cs`) into in-memory draw-op records. No file, log, console, network or response sink takes them; they become fill/stroke colours in the PDF.
2. CodeQL C# keys on the ACCESSED element's name, not the declaring type: `SensitiveVariableAccess` tests `this.getTarget().getName()` (`csharp-all/7.4.2/semmle/code/csharp/security/SensitiveActions.qll:134-135`, read in the CLI's own pack on this box). The targets are `Primary`, `Accent`, `Fg`, `Border`; `BrandTokens` is a type access, not a variable access.
3. Even the type name would not match: the C# `suspicious()` list (`SensitiveActions.qll:32-44`) is password, passwd, account*id, accnt*id, account*key, accnt*key, license/licence*key, voucher*code, trusted. "token", "secret" and "auth" are not in it for C#.
4. At base the same regex already hits 56 lines naming `BrandTokens` that landed through hosted CodeQL with no alert (builder's count; consistent with 2-3).
The hand row is the floor and fired correctly on the NAME; on reading, it is not the clear-text-sensitive-data shape. (The commit message's one hit is "Co-Authored-By", the trailer, and the squash body replaces it.)

## Findings
| # | Sev | Finding | Evidence |
|---|---|---|---|
| F1 | Minor | `api/src/HpsmPoc.Modules.Reporting/README.md` ADR-R13 row still says "The executive report's golden outlines are unchanged (asserted)"; at head the three executive outlines moved by one page. A code-fact sentence now false. The kit limited the README edit to ADR-R11, so the builder left it and flagged it. Fix in a later records/docs touch (one clause). | `git show origin/r:.../README.md` grep -c 'golden outlines are unchanged' = 1 |
| F2 | Minor (noise, not this lane) | `HpsmPoc.Api.Tests.Hosting.ForwardedProofTests.The_web_front_end_value_is_gone_from_the_request_once_the_pipeline_has_read_it` is intermittent at main: whole suite at main 1 red; at merge 0 red; alone 5x at main 2 red, 5x at merge 2 red (equal rate). It also made SQL part api-assessment at merge `bad = 1` (1463 passed, 1 failed, that test only). Lane R touches no Hosting file. Hosted CI may red on it: re-run, never a skip. | logs fwd-main-1..5, fwd-merge-1..5; sqlA trx |
| F3 | Note | Two rewritten/new tests are green with the fix removed by design: the HPSM-section slice (its rewrite only skips page 2) and the readiness guard. The guard is not vacuous: my mutant (readiness builder takes the default heading) turns it red (1 failed). | wt-mut run |
| F4 | Note | The dead gate left containers `g1586-azurite` (127.0.0.1:10070) and `g1586-mssql` (10071) running since 20:15 AEDT. Not mine, not touched (no delete without an owner). Tuesday may stop/remove them by name. Also: the five moved text files in `_dead_gate_2015/` carry mtime 21:46 (I moved them at 21:32 and never wrote them), so some other writer touched them after the move; `ps` at 22:20 shows no process naming this folder or g1586. Treat that folder as untrusted. | `docker ps -a` 22:17; `ls -la` 22:20 |
| F5 | Note | Kit Step 5 asked for the name-check control as an uncommitted scratch mutant; the builder committed it as a second test (`Control_without_the_heading_...`). Stronger, not a defect; it is red with the fix removed. | red run |

No Blocker, no Major.

## Checks (instrument, control)
- **Refs/partition.** 11 changed paths, 11 of 11 inside OWNS (5 product, 3 executive goldens, PdfReportGoldenTests.cs, 2 named new test files). 1 commit on base f32b209b. Overlap with main's moved paths (f32b209..f4e79a7, 41 paths; f4e79a7..d607c8f, 8 paths): 0 and 0; with PR 321 files: 0; with lane N kit OWNS: 0 (basenames grepped in the B1585 kit: 0 for each of our files except the generic README.md, all hits are `infra/README.md`, and the kit lists Reporting `Report/**` and `Pdf/**` as NOT its own; control `NarrativeReview.cs` = 9). No b1585 branch on origin (matching-refs length 0). 0 paths under Reporting moved on main.
- **Merge.** `git merge-tree --write-tree` clean (rc 0) against f4e79a7 and against d607c8f; tree equals main plus the head blobs by program (True; control with one altered blob False).
- **CI, api job** (Azurite pinned image on 127.0.0.1:10100):
  | tree | total | passed | failed | skipped | Azurite 10 by name |
  |---|---|---|---|---|---|
  | main f4e79a7 | 4129 | 4128 | 1 (F2) | 0 | 10/10 |
  | head 7868012 | 4131 | 4131 | 0 | 0 | 10/10 |
  | merge | 4145 | 4145 | 0 | 0 | 10/10 |
  By project at merge: Rules 164, Assessment 305, Reporting 864 (+14), Feedback 478, Api 2334 (+2). Build 0 warnings 0 errors at main, head, merge (TreatWarningsAsErrors). trx counter control: fixture of 3 known outcomes printed them.
- **CI, SQL Server** (pinned `2025-CU9` image, amd64 under emulation, 127.0.0.1:10101; Azurite 10102), merge only: api-assessment 1463 passed / 1 failed (F2) / 0 skipped, judge bad 1, 4 named Passed, databases 319 (floor 100), host retries 0; api-other-and-feedback 1348 passed (870 + 478) / 0 / 0, judge bad 0, 4 named Passed, databases 243 (floor 110), retries 0. Judge control: fixture trx gives bad 6. Not run at main (hosted CI ran it for PR 320).
- **CI, infra.** `validate.sh` (venv python 3.14.10, bicep drive-local): main 325 OK, merge 325 OK. `test_hidden_characters.py`: main 14 OK, merge 14 OK, newest merge 14 OK.
- **Web jobs not owed.** 0 JS/TS/Python files in the diff; needle scan of all 11 changed basenames over web/, infra/, scripts/: 0 files each (control `ReportModelBuilder.cs`: 2).
- **Red without the fix** (Layout.cs and PdfPigReportRenderer.cs reverted to main, rest of merge kept so it compiles): 19 failed: 13 of 14 ContentsPageTests cases, 2 of 2 ContentsHeadingNameCheckTests, 3 golden-outline cases, SOW order. Readiness guard: red under its own mutant (F3).
- **Goldens.** By program each executive outline differs from base only by PageCount + 1 and every Page + 1, headings identical (8->9, 9->10, 5->6); control altered = False. PdfPig pin unchanged (`csproj:17` 0.1.16); no csproj or Directory.Build change.
- **Silent class.** Heading-text locators in tests (`"[1-9]. <title>"`, `ReportSectionIds.Ordered`, title-in-IndexOf/Contains): only PdfReportGoldenTests (rewritten), ContentsPageTests (new), readiness tests (readiness PDF unchanged) and model-level asserts; the remaining Contains hits assert body text, which the contents page does not print.
- **Probes at source.** `ReportingEndpoints.ReportWords` (merge :799-825) reflects every public string property of Reporting-namespace objects, so `ContentsHeading` is an own word; `:496` builds `own` from the default model (heading included). ADR-R11 and commit-message sentences checked at source: true.
- **Scans** over 366 added lines in 11 files and the commit message: names (ban list + project people + git user) 0, control `_by_<name>_` fired for each; B-number/seat words 0; ticket key 0; non-ASCII 0; Cf 0; 40-hex 0; GUID 0; hosts 0; Process.Start 0; raw SQL 0; File/Console/log write 0; reflection 0; format-from-input 0; JS regex/innerHTML/child_process 0; Python chmod 0; sensitive-NAME 5 (ruled above). 27 of 27 planted controls fired.
- **CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof.** No other language changed.
- **Deploy on merge: NO.** `.github/workflows/` at head holds only `ci.yml` (push to main, pull_request, workflow_dispatch; permissions contents: read). Its header says "Build + test only. No deploy job, no cloud credentials"; a push to main keeps the deploy packages as build artifacts, deploying them is a separate runbook step. No `azure/login`, `environment:` or `secrets.` (0; control `runs-on` 10). `.github` unchanged by this branch.
- Ports 10100-10109: 0 listeners before (21:34) and after (22:17) (control unfiltered 21 / 19). My containers g1586b-* removed by name; no process of mine left.

## Builder STATUS claims
| Claim | Grade |
|---|---|
| Branch one commit 78680128 off f32b209b, 11 files +366 -37 | true |
| Whole suite at head 4131/4131, Azurite 10/10 | true (my head run identical) |
| Base 4115/4115 | not re-measured (my main is f4e79a7, 4129) |
| SQL parts 1455 and 1348 passed, 0 failed | 1348: true at my merge. 1455: not reproduced; my merge (newer main) gives 1463 passed + 1 known flaky red |
| Infra 325 OK, hidden chars 14 OK | true |
| 4 predicted reds before test edits | not re-measured (I measured red-with-fix-removed instead: 19) |
| Goldens move by exactly +1 | true |
| Null-heading PDF byte-identical to base; readiness byte-identical | not re-measured bytewise; the text-level property tests pass at merge |
| No web job owed | true |
| PdfPig 0.1.16 unchanged, Name unchanged | true |
| Sensitive-NAME 5 hits on BrandTokens | true; ruled false hit |
| ADR-R13 now inaccurate | true (F1) |
| Census 236 rows in 60 files | not re-measured |

## NOT RUN
- CodeQL csharp locally (arm64); hosted CodeQL is the proof.
- web-build, web-unit, web-e2e: not owed (evidence above). The live-API web specs (in no CI shard).
- SQL Server parts at main and at head alone (run at merge only).
- A screen reader; a paper print (zero border is counted from the raw PDF only by the committed test).
- Byte-level base-vs-head render comparison (text-level property covered by tests).

## Files
VERDICT.md, pr-title.txt, pr-body.txt, squash-subject.txt, squash-body.txt, landing.txt (this folder); `_dead_gate_2015/` holds the dead gate's moved files.
