GATE B1584: GO WITH FINDINGS @ 169a7bb on main f4e79a7

Tier G1 (kit S8 / GATE-ROUND: client-visible control on the live card, round 1 of 2). Gate run 21:10-21:30 AEDT 2026-11-15. All measurements are in this gate's own scratch clone (push URL set to INVALID_NO_PUSH, never pushed). The local merge commit 5c6100af is gate-only and was never pushed. The dead gate's files from ~20:15 were moved unread-as-evidence into `_dead_gate_2015/` (ls -la printed before and after). None of them counts here.

## Refs and partition
- `git ls-remote` branch b1584/hpsmpoc-answer-basis-chooser = 169a7bb02e198f74765fd92fd3cb05b6a726da77 = READY sha. One commit; parent f32b209b (the stamped BASE). Author and committer email are the configured noreply identity.
- Origin main = f4e79a7ae2f43dc7d50024570660c57d00eae3a4 (PR #320, 41 paths since BASE). Head paths against those 41: overlap 0 (control: registry.ts found 1).
- Changed paths 8 of 8 inside OWNS: the 4 product files, the 3 new test files, and 1 census REWRITE row (SnapshotRunner.provenance.test.tsx:85). That row is red at head without the rewrite and red at main with it. 0 api/, infra/, lib/, server/, .github/ paths.
- Open PRs: 0 (control: state=all lists 320, 319, 318 closed).
- Lane R branch 78680128 (11 paths): overlap 0 (control: self 11). Lane N's OWNS from its kit (11 named paths, migrations under api/): overlap 0 (control: ApiNarrative.tsx 1). Lane N has no branch on origin yet (matching-refs b158 lists none), so only its kit was compared.
- Deploy on merge: NO. The only workflow at head is .github/workflows/ci.yml ("Build + test only. No deploy job, no cloud credentials"). A push to main builds, tests and keeps deploy-package artifacts; deploying is a runbook step. No azure login or webapp deploy action is in any workflow file at head.

## Merge
`git merge-tree --write-tree f4e79a7 169a7bb` rc 0, tree b056b099. By program it equals main plus the head's 8 blobs (1548 paths, 8 differ from main; a perturbed control compares unequal).

## CI predicates (node v24.21.0 / npm 11.19.0 from the project's .tools/node24, ports 10092-10095)
| Job | main f4e79a7 | head 169a7bb | merge 5c6100af |
|---|---|---|---|
| lint (max-warnings 0) | - | - | rc 0 |
| typecheck | - | - | rc 0 |
| vitest whole | 299 files, 4275 passed, 0 failed | 300 files, 4291 passed, 0 failed | 301 files, 4302 passed, 0 failed |
| names main to merge | | | lost 0, added 27 (17 useSnapshot.basis, 10 QuestionCard.basis); control drop-one shows 1 |
| --check-shards | rc 0; playbook 68/67/68/67 | - | rc 0, "every test in exactly one shard"; playbook 69/68/69/68, others unchanged (198/181/182/181) |
| build (+postbuild bundle check) | rc 0 | - | rc 0, "none of 39 provenance markers" |
| e2e playbook-desktop-1 / -2 / mobile-1 / -2 | 64/54/63/52 passed; skipped 4/13/5/15; 0 failed | - | 65/55/64/53 passed; skipped 4/13/5/15; 0 failed, 0 flaky, 0 retry lines |
| e2e journey-and-prototype, prototype-desktop-2, tablet-1, tablet-2 | - | - | 198 / 177 (+4 skip) / 181 (+1) / 177 (+4) passed, 0 failed, 0 flaky |
| e2e total (8 shards, CI=1) | | | 970 passed, 0 failed, 0 flaky, 46 skipped |
| hidden characters (walks all 1548 tracked files) | | | Ran 14, OK. Control: a planted U+202E in QuestionCard.tsx makes it fail and name the file |
| infra unittest (python 3.14.10) | | | 189 ran, 0 failures, 4 errors: setUpClass of test_security_baseline, each "No such file or directory: 'bicep'" (4 of 4). bicep is not installed |

The new spec ran in both playbook projects at merge (4 rows passed). Merge minus main in the playbook shards: +4 passed, skips identical (37 = 37). Load1 during the runs was 18-38 (shared machine). No red.

## Red without the fix (at merge, the 4 product files put back to main's)
- The three snapshot test files: 13 failed, 21 passed. This matches the builder's 13/21.
- New browser spec, both projects, retries 0: 4 of 4 failed ("element(s) not found" on How do we know?).
- The 15 rows that stay green without the fix pin behaviour the change keeps. Each was tested by a targeted mutation of the fix, and every mutation turned rows red:
  - M1 basis over citation: 5 red.
  - M2 list on a cited answer: 1 red.
  - M3 prop on by default: 1 red.
  - M4 basis key on an asserted record: 1 red.
  - M5 basis key on a cited record: 1 red.
  - M6 disclosure always open: 5 red.
  - M7 delayed save: 1 red.
- No new test is vacuous.

## Probes
- Words: the new literals in the product files are only `How do we know?`, the basis ids and module or class tokens (control "Checked by us" flagged). The option texts come from evidenceText(). The five words were re-read at plain-words.ts:6-14, and the report's EvidenceText was re-read at ReportModelBuilder.cs:410-414.
- API side: ProvenanceTests.cs:552 still pins "without a citation every basis is accepted". AssessmentDbContext's ck_response_basis allows all five. So the real API accepts each choice on an uncited answer.
- Cited answer: no list (M2 proves the guard is tested). toWrite keeps the citation rule (M1).
- Follow-up and review: NotesField's prop defaults to false (M3), so there is no list without the prop.
- api/ and infra/ (and .github/) were grepped for questionnaire.ts, useSnapshot, QuestionCard, SnapshotRunner, playbook-answer-basis and web/src/components/snapshot: 0 files each (control web/src/content: 3). Lane P touches no api path, and at the merge api/ is byte-identical to main's.

## Scans (301 added lines + the commit message)
- Names, underscore-aware: 0. The list was the ban list, the project identity user name and the coordinator seat names; the planted underscore control fires.
- Work ids (work numbers, seat ids): 0 (control fires).
- HPSMPOC- keys: 0. Non-ASCII: 0 (controls U+00A0 and U+202E fire). GUID or 40-hex: 0 (control fires).
- Hosts: 1 hit, `http://mock.test` in QuestionCard.basis.test.tsx. That is an in-process fake fetch base on a reserved test TLD, already used by 3+ files on main. Not a hosted host.
- Secrets and .env: 0.
- CodeQL hand rows (new RegExp from a variable, the .replace hand-escape, innerHTML / dangerouslySetInnerHTML, child_process, the sensitive-NAME row): 0 each (controls fire). No Python or chmod lines were added.
- CodeQL CLI 2.27.4, javascript, javascript-security-extended.qls (2.5.0), on git-archive exports:
  - main: 0 results. Merge: 0 results.
  - The merge database holds the changed files (4 of 4 found in src.zip).
  - Planted control: 2 results (js/reflected-xss, js/regex-injection).
- CodeQL csharp: NOT RUN (cannot extract on arm64; no C# file changed). Hosted CodeQL is the only C# proof.

## Builder STATUS claims
| Claim | Grade |
|---|---|
| ls-remote = 169a7bb0, one commit off f32b209b, one ref named b1584 on origin | true |
| 8 paths, none of the 41 paths main gained since the base, none in an open PR | true |
| Census 184 rows / 49 files (BASIS 98, FN 36, NOTE 16, COMBO 34) over 357 test files | true (re-measured at f32b209b: identical) |
| 1 REWRITE row, SnapshotRunner.provenance.test.tsx:85 | true |
| Unit 4291 passed, 0 failed; lost 0, added 27 | true (head 4291; main-to-merge lost 0, added 27) |
| 13 red / 21 green of the three snapshot files at BASE; 15 are pins | true (13/21 at merge minus fix). The pins are shown non-vacuous by mutation |
| New e2e 4 red at BASE, 4 green at head | true (4 red without fix; 4 green at merge) |
| --check-shards playbook 69/68/69/68 | true (at merge) |
| 8 shards 970 passed, 0 failed, 0 flaky, 46 skipped | true at merge (not re-run at head itself) |
| API 4093 passed, 0 failed, 22 not executed | not shown (API not run by this gate; no api path changed) |
| CodeQL JS 0 at BASE and head, control 2 | true in substance (0 at main and merge, control 2) |
| Step 7 scans pass | true |
| Main never moved during the build | true for its window; main moved at 20:12 after READY. That is why this gate re-ran at the merge |

## Findings
| # | Severity | Finding |
|---|---|---|
| 1 | Minor | 15 of the 28 new or rewritten unit and component rows are green without the fix. They pin kept behaviour and are not red-first in the strict sense. Each is proven non-vacuous by a targeted mutation of the fix (M1-M7 above). Nothing to change. |
| 2 | Minor | Behaviour change to note in the release notes (the builder disclosed it): an uncited answer stored with a non-default basis (from seeds or other writers) used to be rewritten to "stated by the customer" on its next save from the live card. It now keeps the stored basis and shows it in the list. This is what the design intends (P1), and the PR body names it. |
| 3 | Minor | The builder's STATUS discloses a `sed -i.bak` on /dev/null, a verb on the kit's never list. It touched no file. It is a process slip only, with no effect on the branch. |
| 4 | Minor | The builder did not re-run the browser shards, the build or the API on its final tree. This gate's merge run covers the browser shards and the build. The API is unchanged. |
| 5 | Info | The commit's own trailer names the builder's model. The squash body here carries the landing attribution. |

No Blocker and no Major.

## NOT RUN
- API suite (dotnet build/test), the two SQL Server parts and the Azurite tests: no api/ path changed, no api or infra test reads a changed path (program above), and api/ at the merge equals main's. The known intermittent ForwardedProofTests was therefore not exercised. Hosted CI is the proof.
- `bash infra/scripts/validate.sh` and the 4 bicep-dependent infra classes: bicep is not installed here. Hosted CI is the proof.
- CodeQL csharp, python and actions: no such file changed, and the csharp extractor cannot run on arm64. Hosted CodeQL is the proof.
- Lint, typecheck and build at head alone, and the four prototype shards at main: not needed for a comparison (merge green; prototype shards do not depend on the changed card per the builder's head run and this merge run).
- Lane N branch comparison: the branch does not exist on origin yet. Only its kit's OWNS were compared.
- Jira, mail, board, PR, push, az, hosted hosts: none touched.

## Files
VERDICT.md, pr-title.txt, pr-body.txt, squash-subject.txt, squash-body.txt, landing.txt (this folder). The dead gate's files are in `_dead_gate_2015/`.
