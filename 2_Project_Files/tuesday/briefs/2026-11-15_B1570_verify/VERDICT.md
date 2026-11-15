GO WITH FINDINGS
GATE B1570: GO WITH FINDINGS @ e5994b7 on main ee44790

BLUF: this is the tier G1 gate, round 1 of 2, run 2026-11-15 from 13:20 to 14:10 AEDT in my own clone at head. The branch is `b1570/mps-lane-mo-followups-400-403` @ `e5994b7cc4ab4a0afed8a3c95c45aab8d4b4107d` (3 commits, one per ticket). It builds MPSCALC-400 (order only), MPSCALC-401 and MPSCALC-403 as the kit says.
- Changed paths: only the three `scripts/` paths. The two swapped lines are byte-identical, no stop word changes, and the merge with current main is clean.
- Tests: every CI python file has the same rc at base, head and merge, both in a full clone and in a depth-1 copy (the hosted shape).
- Red without the fix: 11 of the 17 new rows fail against the old scripts. All 7 of my planted mutants are killed.
- CodeQL pre-scan: 0 results.
- Findings: Blocker 0, Major 0, Minor 1, Info 6.
- The one Minor is a wrong stated cause for a known environmental red, not a product issue: `test_run_demo.py` fails on this box with node present (its two Ctrl-C rows), not because node is missing. It is the same at base and head.

## Findings
| # | Grade | Where | Measurement |
|---|---|---|---|
| m1 | Minor | builder STATUS, BASELINE section ("test_run_demo.py rc 1 (23 tests; no node)"); the same cause is RELAYED in the kit, FACT 5 | `command -v node` prints `/opt/homebrew/bin/node`. The two reds are `test_ctrl_c_is_never_reported_as_an_unexpected_stop` and `test_ctrl_c_stops_api_and_web_and_leaves_a_bystander_in_the_same_dir` (class `C5StopsExactlyWhatItStarted`), with identical names at base, head and merge, full and depth-1. The equality bar holds, but the stated cause is wrong. `test_infra.py` is red for the reason given ("no Bicep compiler", `infra/tests/test_infra.py:66`). |
| i1 | Info | `scripts/deploy-from-ci.sh:233` with `:228` | Q-2, as accepted. In the shallow case the undecided line prints `(git answered 128)` although git answered 1. I checked whether it misleads beyond what the kit foresaw: it does not. The same line says the checkout "cannot say whether package ... includes" and asks for a full checkout, which is the right action. Only the number is literally untrue. It goes into the pending MPSCALC-402 word pack. |
| i2 | Info | `scripts/deploy-package.py:329` | The other `$`-ended patterns, listed by property. `:58` ENV_OR_DATA and `:165` `^reference.*\.json$` are REFUSE-lists over package leaf names: there `$` refuses MORE (a name with a trailing newline is still refused), so `\Z` would be the less safe side. Neither validates a whole outside value. `:329` `re.search(r"/actions/runs/(\d+)/attempts/\d+$", manifest source.run)` takes the run id out of a manifest value. It is unanchored at the front, so it is an extractor, not a whole-value check. A trailing newline after the attempt does not change the id it returns, and the id is then compared with the expected run. For later: if a whole-value check of `source.run` is wanted, that is a new ticket. Not a finding against this branch. The shell check at `scripts/deploy-from-ci.sh:213` (`=~ ...\.json$`) is POSIX ERE, where `$` is end of string, and it reads one line from `read -r`, so it is not in the class. |
| i3 | Info | kit Step 2(c) vs source | The kit expected "the overlay read count unchanged (2)" on the older-package stop. With the new order, a roll-forward stop never reaches the re-read, so the count is 1. The builder followed the source and pinned it: `test_the_reread_is_not_reached_when_the_roll_forward_stops` is red against the base script and green at head. That is correct. |
| i4 | Info | base `scripts/tests/test_deploy_rollforward.py:325` (`test_a_snapshot_alone_stops_an_older_package`) | The kit expected 3 hazard rows. My depth-1 control (BASE test file with the HEAD script, shallow copy) turns exactly 2 red: `test_count_above_0_and_an_older_package_stops_with_0_deploy_calls` and `test_one_new_type_row_in_the_overlay_alone_stops_an_older_package`. The third row asserts only `(overlay 0, quotes 0, snapshots 2)`, which both the older and the undecided lines carry, so it cannot tell them apart. This matches the builder's claim. The row is pre-existing and not edited. |
| i5 | Info | commits | All 3 are `kamil.kreiser@datasec.com.au | kamil.kreiser@datasec.com.au`, equal to the project repo's `config --local user.email`. They are unsigned (`verification.verified=false`), as before. Each ends with the builder's own attribution line (Sonnet 5.5). |
| i6 | Info | `scripts/deploy-from-ci.sh:226-227` | The new comment holds the word "older" in double quotes. It is a comment, not a string literal: no echo or stop was added, and the file with the 3 added lines removed equals base with the two lines swapped (program check, below). |

## Refs, scope, merge (measured)
- **Refs:** `git ls-remote` (13:22): the branch is `e5994b7cc4ab4a0afed8a3c95c45aab8d4b4107d` and main is `ee447909c2f3cda510e856608cf1aeaa62316d41`. `gh api -X GET .../git/ref/heads/main` gives the same main. Open PRs: 0.
- **Compare at source:** `gh api -X GET compare/ccc41367...e5994b7` gives ahead 3, behind 0, 3 files:
  - `scripts/deploy-from-ci.sh` +4 -1
  - `scripts/deploy-package.py` +3 -3
  - `scripts/tests/test_deploy_rollforward.py` +252 -4

  Against current main it is ahead 3, behind 1 (diverged). Main's one commit touches 9 `web/**` paths only (`git diff --name-only ccc41367 ee447909`).
- **Merge:** `git merge-tree --write-tree ee447909 e5994b7` in my clone gives rc 0 and tree `2bc54301`. `git diff --name-status main <tree>` lists exactly the 3 paths (M), and each blob in the merge tree equals the head blob (`990c709e`, `030ba280`, `f581f074`).
- **Byte check:** base `:237`/`:238` sha256 `f4fab4ca...`/`37717c1e...`. Head `:240`/`:241` are `37717c1e...`/`f4fab4ca...`, the same two lines in the new order. A program check shows the head file with its 3 added lines (`:226-228`) removed equals the base file with `:237`/`:238` swapped, byte for byte (`True`). So no other line moved and no stop word changed. The added lines hold no echo and no stop.
- **Deploy:** none can be triggered. There is no `.github/` change, and `ci.yml` has no merge-triggered deploy.

## 400 (order)
- The overlay re-read is now the LAST read before `az webapp deploy`. Deploy block at head:
  - `:239` pre1_hosted
  - `:240` rollforward_hosted
  - `:241` reread_overlay

  The next Kudu or curl read after that is `download_wwwroot` (`:284`, token at `:286`), which runs after the deploy call at `:267`. The runtime row `test_the_last_read_before_the_deploy_call_is_the_overlay_reread` checks the position in the calls log and is green at head.
- The count reads no overlay. `rollforward_hosted` (`:205-236`) uses `newtype_overlay` (set by PRE-1) and declares all its variables `local`. It never touches `overlay_copy`, `overlay_code` or `pre1_seen`, which are `reread_overlay`'s inputs (`:172-187`). So the move changes no input of either function.
- Token calls per deploy are unchanged. The two token rows (`5 + files` for 0, 1 and 3 files, and az calls equal to Kudu reads) are green with the head test file run against BOTH the base scripts (copy `mut/r0`) and the head scripts.
- The token is still printed 0 times. `test_scripts.py` `test_xtrace_never_prints_the_token` (`bash -x` plus `SHELLOPTS=xtrace`, probe and deploy with 0 and 1 care-pack rows, `assertNotIn(TOKEN, out+err)`) is unedited and green at base, head, merge and depth-1 head.

## 401 (shallow)
- Premise reproduced in my own synthetic repo (E, F, G, H; not a project repo). Full repo: shallow `false`, `is-ancestor F HEAD` rc 0, F against its parent rc 1. Depth-1 clone plus `fetch --depth 1 origin F E`: shallow `true`, `is-ancestor F HEAD` rc **1** although HEAD contains F.
- `:228`: `[[ "$older" == 1 && "$(git -C "$ROOT" rev-parse --is-shallow-repository 2> /dev/null)" != false ]] && older=128`.
  - The shallow question is asked only after an answer of 1. `&&` short-circuits, and the row `..._answers_0_goes_on_and_is_not_asked...` asserts that `shallow_calls()` is `[]`.
  - Any answer other than exactly `false` is undecided. Rows cover `true`, the empty answer, `no`, `True` and `False`.
  - An answer of 0 still goes on (rc 0, 1 deploy).
  - A full checkout answering 1 keeps the older stop.
- The shim answers the shallow question itself (a new `case` arm, a second log). `git_calls` and its log are unchanged.
- Python loop run by me inside a depth-1 copy of my clone at head (`rev-parse --is-shallow-repository` printed `true`, `rev-list --count HEAD` printed 1): every file has the same rc and `Ran` as the full head, and as the depth-1 base except for rollforward going from 22 to 39.
- Hazard control: the BASE test file with the HEAD script in a depth-1 copy turns 2 rows red (see i4). That proves the shim edit closes a real hosted-CI hazard.

## 403 (anchors)
- `deploy-package.py:50` `SHA` and `:671-672` `NEWTYPE_FILES` end `\Z`. Nothing else on those lines changed.
- Each pattern has a newline row:
  - `test_the_commit_pattern_...`: newline, 39 and 41 hex, uppercase, and spaces are all refused.
  - `test_the_file_name_patterns_...`: quotes and snapshots, each with a newline.
- The commands refuse the newline too, not only the module:
  - `newtype-names`: a listing entry with a newline is dropped.
  - `newtype-count --store`: a file named with a newline is skipped (count 3, not 15).
  - `make --commit <sha>\n` and `verify --expect-commit <sha>\n`: exit 2 with the usage line. The same sha without the newline builds (rc 0).
- `package.sh` passes `$(git rev-parse HEAD)` (DERIVED: not run).
- Other `$`-ended patterns: see i2.

## Red without the fix, and my own mutants
- Head test file against the BASE scripts (`mut/r0`): **11 red** of the 17 new rows:
  - both 400 order rows and `..._reread_is_not_reached...`
  - the 401 rows `..._answers_1_is_undecided...`, `..._full_checkout..._keeps_the_older_stop` (red only on `shallow_calls()`, since base never asks) and `any_answer_..._but_false...`
  - all 5 of the 403 rows

  The 6 green ones are the unchanged stops, the 2 token rows, the answer-0 row and the count-0 row. That matches the kit's design (they are green at both).
- My mutants, each in its own scratch clone, test file `test_deploy_rollforward.py` (39 rows; unmutated head 39 of 39 green):

| Mutant | What it changes | Red rows |
|---|---|---|
| M1 | order swapped back | 3 |
| M2 | shallow test inverted (`== false`) | 6 |
| M3 | `SHA` back to `$` | 2 |
| M4 | quotes pattern back to `$` | 3 |
| M5 | `older == 1` guard removed (shallow asked always, so an answer of 0 turns into undecided) | 1 (`..._answers_0_goes_on...`) |
| M6 | only exactly `true` counts as shallow | 1 (`any_answer_..._but_false...`) |
| M7 | snapshots pattern back to `$` | 3 |

  **7 of 7 killed.**

## CI python predicate (ci.yml:84-107; every file, `python3 -I -B <file> -v`, cwd = the tree)
| Tree | Result |
|---|---|
| base `ccc41367` (full) | 13 files rc 0. Red: `test_run_demo.py` rc 1 (23 run, 2 fail, see m1) and `test_infra.py` rc 1 (0 run, no Bicep). |
| head `e5994b7` (full) | Identical rc per file. `test_deploy_rollforward.py` 22 to 39. |
| merge with main `ee447909` | Identical to head. |
| base depth-1 | Identical to base full. |
| head depth-1 | Identical to head full. |

- Test names (`... ok`): base 309, head 326. Lost (`comm -23`): **0** (control: one name dropped reads 1). Gained: 17.
- Real az never reached: a tripwire `az` sat on PATH ahead of `/opt/homebrew/bin` and behind the tests' own fakes, and logged 0 calls across all five loops and the mutant runs. Control: calling it directly logs 1 line, rc 99.
- `bash -n scripts/deploy-from-ci.sh` rc 0. `test_ci_workflow.py` rc 0. No `.github` change.

## Scans
- **Names** (`(?<![A-Za-z])<name>(?![a-z])`, case-insensitive; ban list plus Friday, Tuesday, Wednesday, Thursday): 0 over the 259 added lines and 0 over the 3 commit messages. Control: `_by_Kam_` fires.
- **Ids:** B-number, seat, WED-, C-nn and session ids: 0. Control: `B1570` fires.
- **Characters and shapes:** non-ASCII 0, Cf 0. Secret, host, uuid, URL, `.local` and `Source_Documents` shapes: 0.
- **gitleaks:** `ccc41367..e5994b7` rc 0, 3 commits. Control: a random `ghp_` canary rc 1.
- **Removed lines:** 8, all allowed: the one swapped shell line, the 3 anchor lines, and 4 `git_shim` lines.
- **CodeQL pre-scan, the program itself:** CLI 2.27.4, suite `qlpacks/codeql/python-queries/1.9.0/codeql-suites/python-code-scanning.qls` (the org's default setup; there is no CodeQL workflow in the repo).
  - Database created from my clone at head, outside the clone: 24 `.py` files (24 of 24 tracked) plus 4 shebang fakes, so the builder's "28 files" is true.
  - Result: **0 results**, 43 rules.
  - Control (a scratch copy of `scripts/` plus a planted file): 1 result, `py/clear-text-storage-sensitive-data` at `scripts/tests/test_planted_gate.py:3`, a value named `api_secret` written with `open(...).write`. The planted `eval(sys.argv[1])` did not fire (no remote source), so the control proves the sensitive-data rule, not code injection.
  - Heavy lock `.tools/.heavy-lock-1` taken by atomic mkdir at 13:57:56 with a holder file, then released by MOVING the holder to `fleet/state/s277/g1570/locks/` and rmdir. Load1 9.60 at 13:53 and 9.20 at 13:56 (more than 120 s apart; the reads are not independent).
- **Hand rows** over added lines (controls `os.chmod(p, 0o755)`, `eval(x)`, `# noqa` and `0o750` all fire): `eval(`, `exec(`, `pickle`, `shell=True`, `os.system`, chmod or mode with a group or world digit, skip or suppress words: **0**. The two shim writes use `mode=stat.S_IRWXU` (owner only, the existing helper's form).
- **Sensitive-NAME row** (password|passwd|secret|token|credential|apikey|api_key|private_key|auth): 2 added lines contain one of the words:
  - `test_deploy_rollforward.py:566`, a comment ("access-token calls").
  - `:569`, the string `"get-access-token"` in an argv comparison.

  Neither is a variable, attribute, parameter or key NAME, and neither is written or printed. **0 hits.**

## Builder STATUS claims
| Claim | Grade |
|---|---|
| 3 commits, configured identity | true |
| 3 paths | true |
| swapped lines byte for byte | true |
| rollforward 22 to 39, others rc-equal (full and depth-1) | true |
| `comm -23` 0, 17 gained | true |
| red counts at base (400: 3; 401: 7 subtest failures; 403: 5) | true (my rerun: 11 distinct red rows = 3 + 3 + 5) |
| token table 5 + files, equal at base and head | true (by rows run against both scripts; the table itself is not re-printed) |
| 401 premise | true (reproduced) |
| depth-1 control red 2 of 3 | true |
| CodeQL 0 results, 28 files, 43 rules, control 1 sensitive-data result, eval alone did not fire | true |
| 8 removed lines | true |
| `:329` "may meet the property" | not shown by the builder; my reading in i2 |
| "test_run_demo.py ... no node" | false on the cause (m1) |
| behind 1, main moved on `web/**` only | true |

## NOT RUN
- Hosted CI on ubuntu-latest (Linux, bash 5, real az on PATH).
- Hosted CodeQL. Mine is a pre-scan.
- The `package` job (`scripts/package.sh`), and the `dotnet` and `web` jobs (they read no changed path).
- `test_infra.py` with a Bicep compiler, and the 2 Ctrl-C rows of `test_run_demo.py` in a passing environment.
- Any run of `deploy-from-ci.sh` against a host. Any real `az`, docker, or deploy.
- A separate xtrace probe of my own beyond the unedited existing row.

Hosted CI and CodeQL on the PR are the proof for these.

Scratch: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s277/g1570/` (clone with push URL `invalid://no-push-gate`; worktrees base-tree, main-tree, merge-tree; depth-1 copies; mut/; cq/ databases; prem/ synthetic repo). One stray file I made at `/tmp/x` (a file-name list) was moved into `work/stray-tmp-x.txt`. Nothing was pushed, and no PR, Jira, message or az was used.
