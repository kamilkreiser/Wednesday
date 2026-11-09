GATE B1402: GO WITH FINDINGS @ b768840 on main 94b24e8

Tier: G2 (tests only), per kit S8. Project MPS Calculator, repo datasecau/MPS-Commercial-Calculator.
Branch b1402/mps-dotnet-pins-template-carekey = b7688400c21e9f4d6784306127ec916f2fadcd0a (git ls-remote, 07:16:45 AEDT) = READY sha.
Main now 94b24e8b6da6f80857b09912d703fa778640ffe7 (moved from the S2 base 31234f5f by one docs-only commit, docs/IMPORTER.md; that commit is PR #167 and lane M8's path).
Verifier clone: session scratchpad v1402/clone, push URL no-push://invalid, never pushed. No gh API, no Jira, no az, no HTTP to any hosted host (git over SSH with the deploy key only, read: ls-remote and fetch).

## Results by step

| # | Check | Instrument | Control | Result |
|---|---|---|---|---|
| 1 | Branch = READY | git ls-remote origin | refs/heads/main read in the same call | b7688400 = READY; PASS |
| 1 | Paths in OWNS | git diff --name-only merge-base..head | - | 1 of 2 owned paths changed (TemplateIsolationTests.cs); 0 outside OWNS; CareKeyPatternApiTests.cs blob b1ac0180 unchanged; PASS |
| 1 | Overlap with sibling lanes | fnmatch over the 36 globs of the 9 other lanes in the kit's PARTITION; grep of the 9 sibling kits for my two paths | LaneM4x.cs matches LaneM4*.cs (True) | 0 overlaps; the only hit in each sibling kit is the M3 "NOT yours" line; PASS |
| 1 | Overlap with open PRs | fetched refs/pull/*/head (167); every PR head that touches TemplateIsolationTests.cs (#145, #148, #152, #156) is already squashed onto main (subject "(#n)" in main log, 1 each); #167 = branch b1406 (docs/IMPORTER.md), tree equal to main | - | 0 overlap. Open state itself NOT read (no API call allowed); see NOT RUN |
| 1 | Sibling pushed branches | origin b14xx/ refs | - | only b1406 (docs/IMPORTER.md, already landed); 0 overlap |
| 2 | Merge | git merge-tree --write-tree main head | stale PR #152 head vs main: rc 1 (conflict) | rc 0, tree d619e3d2; merge vs main differs only in TemplateIsolationTests.cs, whose blob = head blob d75ca28b; merge vs head differs only in docs/IMPORTER.md, whose blob = main blob e37fac25; clean; PASS |
| 3 | CI job dotnet at main / head / merge | project-local SDK 10.0.401 (global.json 10.0.100, latestFeature); restore from the local package cache, then dotnet build MpsCalc.slnx -c Release, dotnet test --no-build, counts parsed from trx | - | build rc 0, 0 Warning(s), 0 Error(s) at all three trees. trx: main Engine 743/743, Import 196/196, Api 3367/3367; head and merge Engine 743/743, Import 196/196, Api 3382/3382; 0 failed and 0 not executed everywhere. Names main to head and main to merge: lost 0, gained 15 (the lane's 15 rows), head and merge not-passed 0. --list-tests: 4306 / 4321 / 4321; comm -23 0, comm -13 15. PASS |
| 3 | Other CI jobs (web, python, package) | read ci.yml at head; git grep of tools/demo/test, infra/tests, scripts/tests, web scripts and tests for the changed path or a walk of tests/ | - | none reads the changed file; not run (see NOT RUN) |
| 3 | Repo-wide hidden-character walk (tracked text files) | own python walk, Unicode Cf category, main vs head | planted U+200B counts 1 | 680 files each; 21 Cf hits in 7 files at main and the identical 21 at head (pre-existing fixtures); delta 0; PASS |
| 4 | Red without the fix | throw-away tree: FormatGuardFires reverted to the pattern only; Api.Tests filtered to TemplateIsolationTests | - | build rc 0; 24 total, 4 failed, rc 1: exactly the 4 form rows, with the builder's reason lines word for word |
| 4 | New quiet rows and the files fact | mutant trees: (a) drop `depth == 0`; (b) drop `inHole` | - | (a) 1 red: the lambda clean row; (b) 2 red: the `ok ? 1 : 2` clean row and the template-files fact. The 10 quiet rows and the fact stay green with the fix removed, by design (they are over-fire controls on the new reader). Two of them are shown to kill a mutant; the other quiet rows guard the pattern's existing behaviour. Not vacuous |
| 5 | Closed lines at main 94b24e8 | grep -n; gitleaks 8.30.1 | pre-rename file (ed72606) rc 1; ghp_ canary rc 1 | MPSCALC-221 ALREADY-ON-MAIN holds: CareKeyPatternApiTests.cs:15 `SyntheticCarePack`, landed by #109 (93e1cab); gitleaks on that file at main rc 0. MPSCALC-381 item 3 holds at main: TemplateIsolationTests.cs:98 and :315 lines, from #156 (511e6c0, 1 file +9 -2) |
| 6 | Probes (throw-away tree, 15 extra rows) | probe Theory calling FormatGuardFires | - | Fires as expected (8/8): the four forms in verbatim $@/@$ strings, two literal holes before the format, a format inside a nested interpolated string, an escaped quote in an earlier hole's literal, a line break after the literal hole. Quiet as expected (4/7): colon in a string inside a hole, colon in a plain string, colon in a verbatim string, a goto label. Fired where quiet was expected (3/7): `$"{{a:b}}"`, `$"{F(':')}"`, `$"{a /* : */}"`. Python shows the UNCHANGED pattern FormatInHole (on main since before this lane) matches all three; the new reader skips doubled braces, char literals and comments. Pre-existing strictness, not introduced here; see finding F3 |
| 6 | Code-fact sentences in the changed comments | read of ScanCode/ScanString at head; ls of src/MpsCalc.Api/Templates | - | "four Templates files": 4 files (TemplateDtos, TemplateEndpoints, TemplateRules, TemplateStore); "the colons of the long refusal message in the store are text": TemplateStore.cs:188 `$"Start refused: {PathKey} ..."`, a text colon; the comment that the second reader goes through the scan's own hole logic matches the diff (ScanCode records `:` when inHole and depth 0). True |
| 7 | Name scan, added lines (80) and the commit message | python `(?<![A-Za-z])<name>(?![a-z])`, case-insensitive; ban list plus Friday, Tuesday, Wednesday | planted `x_by_Paul_y` fires | 0 and 0; PASS |
| 7 | Secrets, tenant/sub GUIDs, hosts, B-numbers/seat ids, Cf/non-ASCII in added lines and the message | regexes in the same scan; gitleaks git over 31234f5f..b7688400 | ghp_ canary dir rc 1; planted B1402, U+200B, ghp_ fire | 0 hits; gitleaks rc 0 "no leaks found"; PASS |
| 8 | Builder claims | below | | |
| 9 | Tier | S8: G2 tests only | | no security-shaped issue found |

## Builder STATUS claims graded

| Claim | Grade |
|---|---|
| Baseline Engine 743, Import 196, Api 3367, 0 failed | true (same counts at main 94b24e8, which differs only in a doc) |
| Head Api 3382 = 3367 + 15; lost 0, gained 15; list 4306 to 4321 | true |
| Build 0 Warning(s) at base and head | true |
| Red-first: 4 reds, the 4 form rows, with the quoted reason lines | true (reproduced by removing the fix) |
| P1 (colon hook removed): the 4 form rows red | true by an equivalent mutant (reader removed from FormatGuardFires): 4 red |
| P2 (`depth == 0` dropped): 1 red, the lambda clean row | true |
| P3 (`inHole` dropped): 2 red, `ok ? 1 : 2` and the files fact | true |
| P4 (planted format in src): new fact red, old fact green | not shown (not re-run) |
| gitleaks range rc 0 after a ghp_ canary rc 1 | true |
| MPSCALC-221: gitleaks file at base rc 0, pre-rename rc 1 | true |
| MPSCALC-381 item 3 at :98 and :315, from #156 (511e6c03, +9 -2) | true |
| Blobs: TemplateIsolationTests cbe2250b to d75ca28b; CareKey b1ac0180 unchanged | true |
| 80 added lines, non-ASCII 0; removed test lines 0 | true (my grep of the 10 removed lines: 0 Assert/Fact/Theory/InlineData/test-method lines; control 1) |
| Commit subject 113 ASCII characters, ending (MPSCALC-380) | true |
| Ahead 1, behind 1, merge base 31234f5f, files exactly one | true |
| SDK 10.0.401; global.json 10.0.100 latestFeature | true |
| Merged PRs run #1 to #166 | true at their read; #167 exists now (b1406 docs, landed as 94b24e8) |
| Jira states, comments and the ticket's "in place of the pattern" wording | not shown (Jira not read by this gate) |
| Main at Step 0 = S2; open PRs 0 | not shown (no API read by this gate); consistent with refs fetched |
| The heavy-lock load-gate deviation (one job held 3 s at load1 >= 7) | self-reported; not shown |

## Findings

| # | Severity | Finding |
|---|---|---|
| F1 | Minor | Shape departure, stated by the builder: the new reader is ORed with the pattern rather than replacing it ("in place of the pattern" in the ticket, as relayed). The reason given, that a replacement would mean changing existing assertions under the HOLDS, matches the code. The guard is strictly stronger. If the product owner wanted a true replacement, that is a new round. |
| F2 | Minor | GuardShapes() (the list fact at :401-406) still names the pattern alone as the third shape, so that fact does not exercise the second reader. The second reader is covered by the new rows and the new files fact. The builder lists this under RESIDUE. |
| F3 | Minor (pre-existing, not this lane) | The unchanged pattern FormatInHole fires on a doubled-brace literal `$"{{a:b}}"`, on a colon char literal in a hole `$"{F(':')}"` and on a colon inside a block comment in a hole. This is the over-strictness that MPSCALC-381 item 4 (guard strictness) leaves to the product owner. The template files hold none of these shapes, so nothing is red. |
| F4 | Minor | Unshown claims: P4, Jira text and states, and the builder's process deviation (see table). |
| F5 | Info | The branch commit's author/committer is the project's repo-local identity, the same as earlier seat branches. A squash on GitHub is authored by the merging account. Commit message itself: 0 names. |

No blocker, no major. No path outside the lane, no secret, no name, no red at head or merge, no hosted touch.
Deploy: ci.yml has no deploy job ("NO deploy job" header). A squash onto main runs ci on main, and its package job uploads a 7-day deploy-package artifact. That artifact is not a deploy: deploying is a manual runbook step. A merge triggers no deploy.

## NOT RUN
- Hosted CI (dotnet, web, python, package) and CodeQL: NOT RUN here; hosted CI and CodeQL on the PR are the proof.
- web, python and package jobs locally: NOT RUN. No test in them reads the changed file (git grep at head). The package job needs the web build. The python job needs `az bicep install`, which this gate may not run.
- Open-PR state through the GitHub API: NOT RUN (fence: no HTTP to hosted hosts). Overlap was proved from fetched refs/pull heads instead.
- Jira reads: NOT RUN (fence).
- Builder plant P4 (format planted in src): NOT RUN.
- Link checks: the repo has no link-check job; NOT RUN.
- Restore ran against the local package cache (--source ~/.nuget/packages), not nuget.org.
