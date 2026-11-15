GATE B1571: GO @ c6a7e7a on main 8766b25

Tier G2 (tests-only), round 1 of 2. Own clones under .tools/g1571 (head, mut=main blob), node 24.21.0, ports 9892-9895, CI=1 for the e2e shards. Findings: 0 Blocker, 0 Major, 0 Minor.

## Findings
| # | Sev | Finding |
|---|---|---|
| - | - | None. |

## Checks (instrument, result)
1. Refs: ls-remote of the branch = c6a7e7a8ae7cf1159f00a566aecb7e190eedca3c; main = 8766b253bb11e9ef23978abc6741e1c6146e74c4 (read at 15:33 AEDT); rev-list main..head = 1, HEAD^ = main. Changed paths: exactly web/e2e/a11y.spec.ts (1 of 1 owned). Diff: +2 lines (one comment line, `test.setTimeout(90_000);` as first statement of the journey test at :39). No other file touched. Open PR overlap: the brief names 0 open PRs (#318 landed as main); no other H-3 kit.
2. Merge: head is a direct child of main, so the merge result equals head (blob 7544071 vs main blob ded8f4f). `git merge-tree --write-tree` itself was NOT RUN: the session hook refuses that write verb in any clone outside the coordinator folder.
3. CI at head vs main (same machine, same build recipe): lint rc 0 (0 warnings); typecheck rc 0; `--check-shards` rc 0 ("every test in exactly one shard"); builds rc 0 at both; vitest 298 files, 4264 passed, 0 failed, 0 skipped at head and at main, names equal (4264 = 4264, lists identical); e2e with CI=1: `journey-and-prototype` head 2 + 182 + 14 passed, main the same; `prototype-tablet-1` head 181 passed 1 skipped, main the same; failed 0, flaky 0 (no flaky text in any of the four outputs). a11y rows at head in-shard: journey 20.0 s desktop, 18.1 s tablet; at main 19.7 s and 18.3 s (so the in-shard time is the same with or without the bound: the bound is headroom, not a speed change). The other six shards hold no id of this file (--check-shards) and are NOT RUN.
4. Repo-wide scan: infra/tests/test_hidden_characters.py at head, 14 tests OK (ResourceWarning as error).
5. Red without the fix, run by me, N = 5000 ms (below the journey's alone minimum, above the negative control's 0.8 s): main desktop journey RED timedOut 5753 ms "Test timeout of 5000ms exceeded."; main tablet RED 5835 ms same line; head desktop GREEN 11150 ms; head tablet GREEN 10746 ms; the other two tests (3.1-3.4 s, 0.8 s) green in all four, including the negative control. Second N = 8000 (desktop): main RED 9136 ms "Test timeout of 8000ms exceeded.", head GREEN 11803 ms. Control that the pair can fail: head with 90_000 replaced by 1_000 at N=5000 -> journey RED 1344 ms "Test timeout of 1000ms exceeded." (the in-file bound governs).
6. Claims in the builder's STATUS: "10 to 13 s alone" (comment): my 3 alone runs x 2 projects = 10642 to 12476 ms -> TRUE (builder 10374-13341). "sixteen screens": the test's own `expect(screens).toBe(16)` -> true. Red-first pair numbers: reproduced within noise -> true. Unit 298/4264 -> true. Shard counts and flaky 0 -> true. CodeQL 0 results -> true (mine below). The "ticket's 34.2 s under load" was not reproduced by me either (max in-shard 20.0 s at load1 up to 37).
7. Scans over added lines and the commit message: names (ban list + project first names, underscore-aware) 0, planted `_by_Kam_` fired; ticket/B-number/seat/day words 0 (planted 1); 40-hex 0 (planted 1); GUID 0; hosts 0 in added lines; sensitive-NAME row 0 in added lines (planted `authToken` fired; the message hits are the word "Co-Authored-By" only); non-ASCII 0 in diff and message (planted U+00A0 and U+202E fired); CodeQL hand rows (`new RegExp(`, `.replace(/[`, innerHTML, child_process) 0 (planted 1). Added string literals: none (a comment and a call with a number).
8. CodeQL javascript-security-extended.qls (v2.27.4, build-mode none, database in .tools/g1571/out): 0 results, 103 rules, 0 in web/e2e/a11y.spec.ts. csharp and python are not touched by this diff (no .py, no .cs).
9. Deploy: web/e2e only; ci.yml deploy rules do not apply (not NexusAI). No hosted touch, no push, no PR, no Jira, no mail.
10. Cleanup: ports 9890-9899 free (lsof 0 rows), no process of the gate left.

## NOT RUN
- `git merge-tree --write-tree` (hook refusal; merge equals head by construction, one-commit child of main).
- The other six e2e shards (playbook-desktop 1/2, playbook-mobile 1/2, prototype-desktop-2, prototype-tablet-2): no id of this file; hosted CI runs all eight.
- `bash infra/scripts/validate.sh` and the C#/API tests, SQL Server and any docker job: no bicep/dotnet-db here; hosted CI is the proof. The builder reported these red at main too; not part of this change.
- Python and C# CodeQL: no such file changed.
