GATE B1624: GO WITH FINDINGS @ 962e937 on main b946691

Gate tier G2, independent. Head 962e93714ed27adc77378687ed42e0d07743d4c0 on branch b1620/hpsmpoc-owner-cut-whole-characters; main read again at the end by git ls-remote: b946691111f290d61bfde34969c464c16a162a93 (equal to the base the branch was cut from). Nothing pushed, no PR, no hosted HTTP, no az, no Jira, no mail. All work in /private/tmp/b1624-gate/ (own clone, push URL set invalid; archives of main, head and merge trees; a copy with the product file reverted).

## Findings

| # | Sev | Finding |
|---|---|---|
| 1 | Minor | Mutant that survives: in startingOwner, `break` replaced by `continue` (a later small cluster is then added after a cluster that did not fit, so the result is no longer a prefix). All 135 rows pass (evidence/mut_H_skipfirstbreak.txt). No new row, and no older row, feeds an input where a short cluster follows one that does not fit. The property is "longest prefix"; the walk's `break` is the only thing that holds it, and it is the base's own line, unchanged. Not a regression and the kit asked for no such row; a one-row addition (letters(99) + FAMILY + "b" expecting letters(99)) would kill it. |
| 2 | Minor | Gate did not meet the heavy-load rule: load1 never read under 7 in the 15 minutes waited (reads in evidence/loadwait.log: 8.94 at 16:09:17, then 9.6 to 20.5 until 16:24:34, 10.74). Jobs then ran one at a time, load1 10 to 33 (evidence/runs.txt). Every result was a clean pass or a stable count; no red was ever load-shaped. |
| 3 | Minor | The head-versus-merge comparison is by tree identity, not three separate runs: main equals the branch base, so `git merge-tree --write-tree` gives tree 6cd35f505572592e8750d10f01d046c619b94450, which is the head commit's own tree (compared by git diff --stat, empty). Head and merge are the same bytes; one set of runs stands for both. |
| 4 | Minor | Open-PR overlap was read from branches (the PR API is fenced): of 341 remote branches not merged into main, 9 touch the two owned files; the newest other than this one is dated 2026-11-11 (the already-landed first point's pre-squash branch); all others are 2026-11-04 or older. No branch dated after that touches either file. The PR list itself was not read. |
| 5 | Minor | A lone-surrogate input stays lone in the result when the lone surrogate is the 100th unit (letters(99) + U+D83D + "b" gives 100 units ending in U+D83D). The base returns the same; no change in behaviour, no row pins it. Listed because the commission named a lone surrogate input. |
| 6 | Minor | The run script I used (run_all.sh in the scratch folder) contains `cd` inside its subshells; no `cd` was typed in any Bash tool call. Disclosed, not a fence write. |

No Blocker. No Major. No path outside the lane, no secret, no name, no deploy trigger.

## Evidence by commission item

- Refs: ls-remote of the branch = 962e93714ed27adc77378687ed42e0d07743d4c0; main = b946691111f290d61bfde34969c464c16a162a93. git diff --numstat main head: exactly 2 paths, both OWNS (remediation-store.test.ts +71 -0; remediation-store.ts +10 -4); 2 of 2 inside the lane. One commit, author and committer the same noreply identity.
- Merge: `git merge-tree --write-tree main head` exit 0, clean, tree 6cd35f50... equal to the head tree.
- The property, by my own probe (evidence/probe.mjs, probe-out.txt): an independent oracle (every prefix length 0..100 tested against segmenter boundaries, longest taken, end-trimmed) against the head function: 32 named cases, 0 mismatches, and 200000 seeded random strings over a joiner/mark/flag/surrogate/space alphabet, 0 mismatches, 0 fitting owners changed (byte for byte). Control: the base function differs from the oracle on the family case (true). Old versus new, named: family after 97 letters, base ends U+61,U+1F468,U+200D (100 units), head 97 letters; family after 95, base ends a shorter family, head 95; skin tone, flag, keycap, accent: base ends bare or half, head ends on the letters (97, 97, 98, 99); exactly 100 units (92 letters + family): kept whole at 100 in both; first cluster over 100 (e + 150 marks): head gives "" (base 100 units); ASCII 101 gives 100 in both; ASCII 100 returned unchanged; leading and trailing spaces: the cut counts after trimming, a fitting owner returned with its spaces; undefined gives "". Fallback (Intl.Segmenter undefined): head equals base on 8 of 8 inputs, and with the segmenter back head differs from base on 4 (control). Result identical with LC_ALL=tr_TR.UTF-8.
- Red without the fix (copy: head tests, main's product file): owner test file, 3 runs, 3 of 3: 8 failed, 127 passed, of 135. The 8: joiner, shorter family, skin tone, flag, keycap, accent, first cluster over limit, property row. Six are `expected 'aaa...' to be 'aaa...'`, one `expected 'e...' to be ''`, the property row `boundary 0: expected false to be true`. The two green-at-base rows (exact limit, fallback) are killed by my mutants B (off by one: exact-limit and fallback rows red, plus 101-letter row and 5-spaces row) and D (no fallback guard: fallback row red).
- Mutants (my own, evidence/mut_*.txt; fixed product file mutated in the copy): A code-point walk 8 red, killed; B `>=` 4 red, killed; C no end-trim 1 red, killed; D no guard 1 red, killed; E word granularity 4 red, killed; F fitting owner trimmed 1 red, killed; G locale undefined 0 red (equivalent for every tested input, the kit says the choice is for determinism); H `continue` for `break` 0 red, survived (finding 1).
- The two departures keep the kit's intent: (1) the property row adds a fifth assertion (cut on a grapheme boundary), strictly stronger than the four the kit named; it is the assertion that fails at base. (2) The fallback row sits before the joiner row, so the `typeof Intl.Segmenter` assertion in the joiner row really runs after the restore; the restore is a `finally`; with the order the kit wrote it would have been vacuous. Neither weakens a kit assertion.
- CI by program (jobs that read the files), main versus head (= merge), node v24.21.0, bicep from the project's .tools/bicep on PATH:

| Job | main | head and merge |
|---|---|---|
| web lint (--max-warnings=0) | rc 0 | rc 0 |
| web typecheck | rc 0 | rc 0 |
| whole vitest | 304 files, 4327 passed, 0 failed, 0 skipped | 304 files, 4337 passed, 0 failed, 0 skipped |
| compare by test name and outcome | | lost 0, added 10 (all in remediation-store.test.ts), changed 0; control: one row dropped gives lost 1 |
| owner test file | 125 | 135 passed, 0 failed |
| npm run build | rc 0, check-client-bundle: none of 39 provenance markers | rc 0, none of 39 |
| test_hidden_characters.py | Ran 14 OK | Ran 14 OK |
| infra discover (all test_*.py) | Ran 325 OK | Ran 325 OK |
| infra/scripts/validate.sh | rc 0 | rc 0 |

- Scans over the 81 added lines and the commit message: names (Kam, Kamil, Kreiser, Steve, Peter, Pete, Paul, Blanchard, Inch, Waite, the configured login) underscore-aware, 0 hits (control `_by_Kam_` fires); non-ASCII or control characters 0 (so no Cf); B-number, seat id, SEAT, Tuesday, Wednesday, Friday, ticket key: 0; new RegExp, innerHTML, dangerouslySetInnerHTML, child_process, eval, sensitive-name words, uuid-shaped ids, hosts: 0; skip, only, eslint-disable, ts-ignore, ts-expect-error, as any, added import: 0. Mode and file-permission rows: none (no Python added).
- CodeQL CLI 2.27.4, javascript-typescript, javascript-code-scanning.qls (87 rules), database in /private/tmp/b1624-gate/cqdb over the head tree (= merge) source root web/: 718 of 718 files scanned, 0 results (evidence/codeql.sarif). No planted-positive control was run.
- Does the merge trigger a deploy: the pre-existing rule in this standard names NexusAI only; HPSM-POC's ci.yml builds deploy packages as artifacts on main and nothing here deploys (no az, no environment step read as a deploy). Standing line: this phase builds no integration with HP tools; nothing deploys.
- Claims graded (builder STATUS): 8 of 10 new rows red at base by assertion: TRUE (8 of 135 failed, 3 of 3 runs, my copy; the two others are green by construction and killed by mutants B and D). Owner file 135/135: TRUE. Whole web 4327 -> 4337: TRUE. Lost 0: TRUE. Five mutants killed: TRUE (my runs A to E killed; the builder's list did not include H, finding 1). Lint, typecheck, build rc 0: TRUE. Infra 325 and validate.sh rc 0 with bicep on PATH: TRUE. Base red without bicep (4 errors, rc 127): NOT SHOWN by me (I ran only with bicep on PATH). FOR TUESDAY 1 and 2 (kit imprecisions): TRUE as stated.

## NOT RUN

- Hosted CI jobs: api, api on SQL Server shards, e2e shards (browser), gitleaks, dependency review, npm audit, shellcheck (no .sh file changed), the web deploy package. Hosted CI is the proof for those.
- `Intl.Segmenter` on a real browser other than node's ICU (Safari and Firefox engines): not run; the fallback row covers a browser without it, but not one whose segmenter segments differently.
- The infra tests without bicep on PATH.
- CodeQL planted-positive control.
- The PR list through the API (fenced); open-PR overlap read from branches.
