GATE B1630: GO WITH FINDINGS @ 8c64a89 on main d991547

Scope: B1627 (lane M-TP). Head 8c64a8959a467455ddfb51a7454c2fab092fb790 (2 commits on base efe6cdd5), re-read at origin 2026-11-16 18:2x: head and main d991547f unchanged, 0 open PRs. Gate tier G2.

W1 as it appears in a log line (hosted or local dev, once per start when the template path is blank):
`Warning: The template store is in memory: MpsCalc:Templates:Path is blank, so every template is lost at the next restart.`

## Findings
| # | Sev | Finding |
|---|-----|---------|
| 1 | Minor | `git merge-tree --write-tree` NOT RUN: the session hook refuses any write-verb git call (merge-tree included) on a clone outside the TUESDAY folder. Substitute, by read verbs only: main d991547f differs from base in `web/e2e/dashboard-390.spec.ts` alone; the four lane files that exist at base have blob ids equal at base and main (`git rev-parse`), and the fifth is new, so a merge is main plus the head blobs by construction. A rig built that way (git archive of main, the five head files overlaid) differs from the head rig only by the one e2e file (`diff -r`). The merge rig was built, tested and Release-built. Hosted CI at PR time is the final proof of a clean merge. |
| 2 | Minor | The builder's mutants mB1-mB3 (code mutants) were not re-run by this gate. The red-without-fix of the three blank rows (the property) was run independently and holds; the mutants stay builder claims (not shown). |
| 3 | Minor | Kit text says mA3 fires the distinct-directories assertion; it fires the first assertion (value equality). The second needs the overlay mutant (a3b, `2 != 3`), which this gate ran. Builder noted this itself; not a defect. |
No Blocker, no Major. No name, secret, tenant id, host, Cf character, or CodeQL pre-scan hit in 99 added lines or both commit messages.

## Checks run (own instruments)
- Refs: `git ls-remote` branch = READY sha; main d991547f. Diff base..head = 5 files (1/0, 7/0, 4/0, 3/0, 84/0), 0 removed lines; all five are the lane's files; open PRs 0 (gh GET). Kit blocks compared byte for byte from the kit text: A1 equal, B1 equal, B2 equal, B3 equal (84 lines, `cmp`), A2 equal (6 added non-blank lines plus the blank line seen in the diff). Both commit addresses equal the project repo's own.
- Infra (Bicep 0.48.1 from the project .tools): base `test_infra.py` Ran 28 OK; head and merge Ran 29 OK; `test_validate_script.py` Ran 6 OK; `validate.sh` on merge rc 0 last line `== validate: OK`; `scripts/tests/test_deploy_pre1.py` on merge Ran 44 OK (42.6 s).
- Red without the fix, A2: head test file against the base bicep: Ran 29, failures=1, `AssertionError: None != '/home/data/templates/'`. Mutants on copies: no trailing slash red (`'/home/data/templates' != '/home/data/templates/'`); line removed red (`None != ...`); value set to quotes path red (`'/home/data/quotes/' != ...`); overlay set to templates path red (`2 != 3`). Each Ran 29, failures=1, the new row only.
- Red without the fix, B: new test file on base source: Failed 3, Passed 1, Total 4; the three blank rows red with `Expected: ["Warning: The template store is in memory: MpsCalc:"...] Actual: []`; the set-path row green (filter control).
- Whole `MpsCalc.Api.Tests` in the proof rig (git archive, git init, one csproj pin 10.0.15 -> 10.0.13 in the rig only, restore from ~/.nuget/packages, no registry): base Total 3656 Passed 3654 Failed 2; merge Total 3660 Passed 3658 Failed 2. The two failures are the same names at base and merge: `PublishOutputTests.An_xml_publish_output_that_ships_the_assembly_without_its_deps_json_entry_fails_the_entry_count_first` and `PublishOutputTests.The_publish_output_carries_the_patched_xml_and_lists_it_in_deps_json` (the rig's lowered pin; not this lane's).
- Set-path behaviour unchanged: `TemplateStartWarningTests` + `TemplateStoreTests` + `TemplateIsolationTests` on merge: 58 passed, 0 failed (4 + 30 + 24); the two older classes are not in the diff (unedited).
- Release build of `MpsCalc.slnx` on the merge rig, --no-restore: 0 Warning(s), 0 Error(s).
- Scans over added lines and messages: non-ASCII 0 (control U+200B fires), names 0 (control `x_by_kam_y` fires), Cf/Cc 0, dynamic regex / eval / child_process / chmod / innerHTML / eslint-disable / sensitive-name / uuid / URL / .local / ids: 0 hits; gitleaks canary rc 1, range rc 0. Hand CodeQL rows (C#): the only variable-ish name is the log parameter `key` holding the setting name `MpsCalc:Templates:Path`, never a value.
- Heavy runs: load1 stayed 9-17 for the 15-minute wait (never under 7); ran anyway, one at a time, in own rigs under /private/tmp/b1630-gate (no project lock taken, no project folder writes).
- Claims graded (builder STATUS): Api tests 3656 -> 3660 true; same two failures true; infra 28 -> 29 true; validate.sh OK true; Release 0 warnings true; Part A red message true; B red 3/1 true; 54 store+isolation green true (58 with the new 4); mutants mA1-mA3b true (re-run), mB1-mB3 not shown.
- Deploy: a merge of this branch triggers no deploy by itself (no deploy workflow edited; nothing under .github changed); the infra apply and the site start are the later deploy card's. Hosted: until the infra apply, a deployed build with this code logs W1 once per start (the warning working).

## NOT RUN
CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof. `git merge-tree` (finding 1). Builder mutants mB1-mB3. Engine and Import test projects (nothing of the lane reaches them). `az`, apply or what-if, hosted HTTP, registry restore, `scripts/package.sh`, docker, web tests.
