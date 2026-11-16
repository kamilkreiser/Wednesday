GATE B1643: GO @ 4ac4540 on main 56bfe23

Gate tier G2 (tests-only lane). Main re-read by git ls-remote at 22:36 AEDT: 56bfe232cbf4c98a9752f949f1f279d755565750 (unchanged since the kit). Branch ref = 4ac454010fc09b1bc6950bc681562522aa922b8d, one commit ahead of main, parent = main. Gate took no lock in the MPS project folder (read-only to it; used only the deploy key for git ls-remote/fetch); all work in /private/tmp/b1643-gate/ (own clone, push URL invalid, nothing pushed). Load gate: load1 10.38 (22:23) and 7.13 (22:25), two reads about 120 s apart (not independent); heavy jobs one at a time.

## Findings
| # | Sev | Finding |
|---|---|---|
| 1 | Minor | The head commit's trailer reads `Co-Authored-By: Claude Sonnet 5.5`; the repo's recent squashes on main (56bfe23, 87dc262, d991547) carry `Claude Opus 5.5`. squash-body.txt uses the Opus 5.5 trailer (it replaces the commit message on a squash), so no action beyond landing with that file. |
| 2 | Minor | The builder's STATUS (c) second restore of the solution: its "no HTTP request" claim was not re-read from the builder's log (another seat's .tools is not read); my own equivalent local-only restore of MpsCalc.slnx (machine cache only, nuget-local.config with no nuget.org source) printed 0 `http(s)://` strings, so the form is sound. Tuesday accepted it. |

No Blocker, no Major.

## Rule rows
1. Diff at merge (merge-tree --write-tree origin/main head; merge tree e5e9bcc6 = head tree e5e9bcc6, clean): by my own program over `git diff -U0`, paths = {tests/MpsCalc.Api.Tests/FleetLineIdTests.cs}, 0 removed lines, 78 added; numstat 78 0. Planted control (a fake docs/API.md hunk with one removed line): program reported 2 paths, 1 removed, 79 added. No product, docs or openapi byte. PASS.
2. Mutants in my copy (Api.Tests only built per mutant, 0 warnings 0 errors each; filter `FullyQualifiedName~MpsCalc.Api.Tests.FleetLineId`, 16 tests at head; main = 13).
   - mA (`PriceAudit.cs:250` `Number(x)` -> `Number(o)`): 2 failed (R12 both cases, Actual names `fleet[3].colourClickOverride`), 14 passed (R13, R1 x2, R1_control, R2-R5, R6, R7, R8, R9, R10, R11). Undone with Edit; `git diff --quiet -- src` rc 0, porcelain 0.
   - mB (`QuoteEndpoints.cs:1672` `new[] { true, false }` -> `new[] { false }`): 1 failed (R13 at the final assertion; Expected [idB, idA], Actual [idA, idB]; its in-row controls before it passed), 15 passed (R12 x2 and all 13 existing rows of both files). Undone; `git diff --quiet` rc 0, porcelain 0.
   - Green without a mutant: main 13 passed 0 failed; head 16 passed 0 failed. PASS.
3. Non-vacuity, read in the file: R12 control sends the same edit through `WithoutIds` on a second quote and asserts the by-number list (`fleet[2].mono 0.0125->null`, `fleet[2].colour null->0.07`, `fleet[3].colour 0.065->null`); an `Assert.Equal(2, n)` positive control on the create entries. R13 asserts `SameFleetLine` false between the two stored lines and true between each sent line and its stored twin, and the stored-order control `[idA, idB]` before the swapped assertion `[idB, idA]`. All as the STATUS says. PASS.
4. Whole solution at the merge (merge tree = head tree): `dotnet build MpsCalc.slnx -c Release` 0 warnings 0 errors; `dotnet test MpsCalc.slnx -c Release --no-build` rc 0: Engine.Tests 743 passed, Import.Tests 196 passed, Api.Tests 3663 passed, 0 failed (Duration 9 m 45 s). Main's Api.Tests count by `--list-tests` at main: 3660, so +3 (R12 x2, R13). PASS.
   Restore requests (all api.nuget.org, the one id only): v3/index.json, v3-flatcontainer/system.security.cryptography.xml/index.json, the .nupkg at 10.0.15, 10.0.10 and 10.0.7, v3/vulnerabilities/index.json, v3-vulnerabilities/.../vulnerability.base.json and .../vulnerability.update.json (log: restore-registry.log; seat-local nuget.config with packageSourceMapping, `--packages` into /private/tmp/b1643-gate/nuget, never the global cache). Then local-only restores (0 http strings) of MpsCalc.slnx and of the main worktree's Api.Tests.
5. C# CodeQL: NOT RUN (the C# extractor cannot run on this arm64 box); hosted CodeQL is the only C# proof.
6. PR texts: written, ASCII, no B-numbers, seat ids, lane names or person names; squash body ends with the Opus 5.5 trailer the repo uses (read from three recent squashes). PASS.

## Other steps
- Refs: ls-remote of the branch = READY sha. Changed paths 1 of 1 in the lane's OWNS. Sibling branches read by `diff --name-only origin/main`: b1641 touches web/src/api/stub/purchaseQuotes.ts and web/src/api/stub/stubApi.test.ts; b1642 touches web/e2e/dashboard-390.spec.ts; shared paths with this lane: 0. (The fetch of b1642 succeeded; no open-PR list read: no `gh` call made.)
- CI jobs: only `dotnet` reads the changed file; `python` job tests do not read tests/MpsCalc.* (scripts/tests/test_sdk_pin.py, which walks the tree for global.json, run at head: 13 OK). `web` and `package` jobs read no changed path.
- Scans over the 78 added lines and the commit message (program scan.py): non-ASCII 0, Cf 0, tabs 0; ban-list names 0 (underscore-aware; planted `x_by_Kam_y` fired, planted U+200B, `new Regex(` and `secret=1` fired); `Process.Start`, `File.`, `Regex(`, `#pragma warning disable`, `SuppressMessage`, sensitive-name tokens, urls, GUID/tenant ids, B-numbers: 0 in added lines. Commit message: only "Co-Authored-By" (matches `auth` pattern) and the noreply address. gitleaks `git` over main..head rc 0; random ghp_ canary rc 1. Author and committer both kamil.kreiser@datasec.com.au (the repo's own).
- Claims graded: R12 red under mA, R13 red under mB, all existing rows green under each: TRUE. Whole solution 743/196/3663, 0 failed: TRUE. One file +78 -0: TRUE. R12 Theory both cases work: TRUE. Builder claim that existing same-number rows do not need the pass: TRUE (13 existing green under mB). Second restore without HTTP: not re-read, equivalent form reproduced (see finding 2).
- Deploy: the merge touches tests/** only; no deploy workflow exists in ci.yml; nothing triggers.

## NOT RUN
CodeQL C# (arm64, hosted is the proof); web checks (npm, Playwright), scripts/package.sh and the Python infra/demo tests needing Bicep (no web, infra, script or tool byte changed); hosted CI; any mail/PR/Jira.
