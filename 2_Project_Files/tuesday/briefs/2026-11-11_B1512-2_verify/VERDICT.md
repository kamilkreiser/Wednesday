GATE B1512-2: GO @ fa713a5 on main aae420f
Round 2 of 2 (the cap) on branch `b1512/mps-lane-l5-ops-tooling`. Tier G1 (Opus). Round 1 read GO WITH FINDINGS @ 2eba09d (Major 1, Minor 5); the fix round added 3 forward commits. Gate run 2026-11-11 20:23-20:45 AEDT.

Why: the Major is closed. The new row goes red with az's own code (1, 7, 130) when the pass-through line is removed, while its rc-0 control and every other row stay green. The `-o json` Minor is closed: its row goes red when `-o json` is dropped. The `:21` change is comment-only, proven byte for byte. The seed fix adds exactly the existing dry-run line on the all-exist path, and a real run is byte-identical to round 1. No existing test line changed. All 11 python-job files pass at head and on the merge with current main, with 241 tests each: lost 0 against round 1, gained exactly the 5 fix-round rows. The three operator-word Minors (3b, 4, 5) are held for the product owner, as the fix kit set out. Their absence is not a finding.

Own clone and worktrees: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s269/gate1512r2/` (`repo`, `wt-head`, `wt-merged`, `wt-r1`, `wt-mut`). Nothing pushed, no PR, no Jira, nothing deployed, real az never run or read.

## Pins
- Branch = `fa713a5bdf4b020d8754780c9b3bd269acb9de56`. I read it with `gh api -X GET repos/datasecau/MPS-Commercial-Calculator/git/ref/heads/b1512/mps-lane-l5-ops-tooling --jq .object.sha` under the project GH_CONFIG_DIR at 20:23:40, and again at 20:31:43 and 20:43:11. Round 1 head `2eba09d8efe7e199691eee9706c62e6aa7da35df` exists at source (`gh api -X GET .../git/commits/2eba09d8...` returned that sha). `git merge-base --is-ancestor 2eba09d8 fa713a5b` rc 0, so it is a plain fast-forward: 3 commits, each author and committer `kamil.kreiser@datasec.com.au`, each naming one ticket.
- Main = `aae420ff8a9e3f8a34be0aff22f8934e1708911a` (same reads; unmoved at 20:43). Open PRs: 0.
- `merge-base origin/main fa713a5b` = `5cd6002f` (the lane base). Main's only change since that base under `scripts/`, `infra/`, `tools/` or `.github/` is `.github/workflows/ci.yml` (PR #178).
- `git merge-tree --write-tree origin/main fa713a5b` rc 0 (clean), tree `b885a136`. I committed it locally as `50b48cf0` (never pushed). In the merged tree, `scripts infra tools` are identical to head and `.github src tests web docs` are identical to main (`git diff --quiet` rc 0 both).
- Fix-round diff `2eba09d8..fa713a5b`: 4 files, +122 -2, and the 4 files are exactly the kit's: `scripts/deploy-from-ci.sh`, `scripts/tests/test_deploy_pre1.py`, `tools/demo/seed.py`, `tools/demo/test/test_seed.py`.

## Findings

| # | Sev | Ticket | Finding | Evidence |
|---|---|---|---|---|
| 1 | Closed (was Major) | MPSCALC-126 | **The az exit-code pass-through is now pinned.** The line is `scripts/deploy-from-ci.sh:206` at head (`if [[ "$deploy_rc" != 0 ]]; then exit "$deploy_rc"; fi`); it was :205 at 2eba09d, and the comment commit moved it +1. P1 replaced it with `:`. Row `test_126_viii_a_...` went red for all three subtests: `AssertionError: 0 != 1`, `0 != 7`, `0 != 130`. Control row `test_126_viii_b_...` (rc 0) stayed ok, and so did `test_126_ix`. 39 of the 40 rows in test_deploy_pre1 were ok and test_scripts was 51/51 ok, so only the new row catches it. P2 (`exit 1`) gave row A red for 7 (`1 != 7`) and 130 (`1 != 130`), green for 1: the value is pinned, not just a non-zero code. My extra plant P6 (exit before the answer is printed) made row A red on the answer-unchanged assertion while B stayed ok. | `out/mutants.txt`; `out/loop-mut-P1-pass-through-removed/`, `-P2-exit-1/`, `-P6-exit-before-printing-answer/`; `probes/mutants.py` |
| 2 | Closed (was Minor) | MPSCALC-126 | **`-o json` is now pinned.** P3 changed `--clean true -o json ` to `--clean true ` at `:202`. Row `test_126_ix_az_webapp_deploy_is_called_with_o_json` went red with `AssertionError: 0 != 1 : ['webapp', 'deploy', ...` (a count assertion, not an index error). Rows A and B stayed ok. | `out/loop-mut-P3-no-o-json/` |
| 3 | Closed (3a, was Minor) | MPSCALC-126 | **The `:21` header change is comment-only.** The diff over the script is `-` one `#` line and `+` two `#` lines. I removed every `#` line from the script at 2eba09d and at head (`/usr/bin/grep -v -E '^[[:space:]]*#'`), and `cmp` gave rc 0 (211 code lines each). Control: one character planted in a code line gave `cmp` rc 1. The only `$0` reader is `:25` (`dirname "$0"`), so nothing prints the header. `/bin/bash -n` rc 0 under bash 3.2.57. | `out/dep-r1.code`, `out/dep-head.code`, `out/dep-ctrl.code` |
| 4 | Closed (was Minor 6) | MPSCALC-173 | **A dry run in which every chosen scenario exists now ends with the existing dry-run line, and a real run is unchanged.** The change is one condition at `tools/demo/seed.py:709`, `if not todo and not args.dry_run:`. With `todo` empty, `:711-757` makes no catalogue GET and `shapes` is `{}`. The run then reaches the existing print at `:755-757`. My probe ran at 2eba09d and at head: a real run, then a second real run, then a dry run, for `--only S1,S2,S3` and `S1,S2,S3,S4`. The only output difference between the two trees is one added line, `seed: dry run: 0 would be created, 3 would be skipped, 0 failed. Nothing was created.` The second real run is byte-identical, and the requests are identical: `GET /api/v1/quotes` only, plus `GET /api/v1/inventory` with S4. P4 (restore `if not todo:`) made `_173_f` red: `'DEMO-S3 exists, skipped ...' != 'seed: dry run: 0 would be created, 3 woul...'`, while `_173_g` stayed ok. My extra plant P5 (fall-through also on a real run) made `_173_g` red: `['seed: 0 created, 3 skipped, 0 failed. Re...'] != []`. | `out/allexist-wt-r1.txt`, `out/allexist-wt-head.txt` (`diff`: 1 added line); `out/loop-mut-P4-*`, `-P5-*` |
| 5 | Held (not a finding) | MPSCALC-126/203/173 | Items 3b (line at the final exit 3, now `deploy-from-ci.sh:260`), 4 (stop wording at `:167`/`:176` and the `PRE-1:` prefix at `:164`) and 5 (dry run and `--out-dir`, `seed.py:36-38,661-663,679`) are unbuilt, as the fix kit held them for the product owner. Lines are +1 in the script versus the kit because of the comment commit. | fix kit "HELD FOR TUESDAY"; fix-round STATUS "HELD" |
| 6 | Info | - | **The fix round built every round-1 Minor that it did not hold:** #2 (row C), #3a (comment) and #6 (seed fix and rows). #3b, #4 and #5 are held. None is left unbuilt and unheld. Round 1's Info rows 7-11 needed no action. | round-1 VERDICT table vs this table |
| 7 | Info | - | The PR body's last line (the required attribution line) carries one non-ASCII glyph. The rest of the PR and squash text is ASCII (`LC_ALL=C grep -c -v -x -E '[ -~]*'`: pr-body 1, the other four files 0). | this folder |

**Counts: Blocker 0, Major 0 (round 1's Major closed), Minor 0 open (2 closed, 3 held for the product owner), Info 2.**

## What I checked, by the brief's eight points
1. **Major:** see row 1. Plants P1, P2 and P6 ran in `wt-mut`. Each was restored, then `git diff --quiet` rc 0 and porcelain empty were checked. Porcelain was 0 lines at the end.
2. **`-o json`:** see row 2 (P3).
3. **`:21` comment-only:** see row 3.
4. **`seed.py:709`:** see row 4 (P4, plus extra plant P5).
5. **No existing test line changed:** `git diff -U0 2eba09d8 fa713a5b -- scripts/tests tools/demo/test infra/tests` has 0 removed lines and 119 added lines. Control: the same count over round 1's own diff (`5cd6002f..2eba09d8`) gives 3, the three lines allowed by ANSWER-1/2. Added `skipTest(`, `unittest.skip`, `xfail` or `sleep(`: 0. Non-ASCII added lines: 0 (control with a planted U+200B: 1). Name, id and secret scan over added lines plus the 3 commit messages: 0 hits beyond the `Co-Authored-By: Claude Sonnet 5.5` trailers, which matched the digit-dot-digit pattern. The control, planted `test_by_kam_thing`, `B1512`, `ghp_` and `1.5`, fired 4 times (`probes/scan.py`).
6. **Python-job loop:** loop of `ci.yml` (head `:86`, main `:102`), `python3 -I -B <file> -v`, BICEP = the project's standalone 0.48.1.

| Tree | Files | Tests | Result | vs round 1 (`gate1512/out/loop-*/names.txt`) |
|---|---|---|---|---|
| head `fa713a5b` | 11 | 241 | 11/11 rc 0 | lost 0, gained 5 |
| merged with main `aae420ff` (local `50b48cf0`) | 11 | 241 | 11/11 rc 0 | lost 0, gained 5 |

   - Per file at head: test_demo_doc 10, test_run_demo 23, test_seed 29, test_seed_hosted 15, test_seed_purchase 12, test_infra 28, test_validate_script 6, test_ci_workflow 8, test_deploy_pre1 40, test_entra_all_roles 19, test_scripts 51.
   - The 5 gained rows: `Pre1DeployCallPlumbing.test_126_viii_a_...`, `test_126_viii_b_...`, `test_126_ix_...`, and `DryRunWhenEverythingExists.test_173_f_...`, `test_173_g_...`. Head and merged name lists are identical (`cmp` rc 0).
   - Control: one head name removed shows lost 1.
   - On the merged tree, `test_ci_workflow` read main's new `ci.yml` and passed 8/8.
   - Both loops ran under project heavy slot 1 (20:35:03-20:39:09 and 20:39:09-20:43:02). The holders were moved to `logs/` and the directory was removed; `.heavy-lock-1` was absent afterwards.
7. **Tripwire:**
   - `tripwire/az` came first, after the tests' own fakes. The runner builds its PATH with nothing inherited: `tripwire:nodebin:/usr/bin:/bin:/usr/sbin:/sbin`. `AZURE_CONFIG_DIR` was the empty `azure-null`.
   - Every run printed `PROOF OK`: exactly 1 folder holds an `az` (the tripwire); `command -v az` names the tripwire; `nodebin` holds exactly `['node']`; `azure-null` is empty. Control: `/opt/homebrew/bin` added to a copy of the list, checked by existence only and never run, reports 2 folders.
   - `TRIPWIRE-HIT.log` was absent after every run: 2 loops, 7 mutant runs, 1 light run, 2 probe runs.
   - The control fired once, a direct call by its own path at 20:24:55 (rc 1). The log was moved to `_quarantine/tripwire-control.log`.
8. **Round-1 Minors not built and not held:** none (row 6).

## What I ran (counts)
- 2 heavy loops (head, merged): 22 file runs, 482 tests, 0 red.
- 1 light run at head: test_seed 29, test_deploy_pre1 40, test_scripts 51, all ok.
- 6 plants (P1-P6), each restored and proved clean. Every plant went red on the intended row, and every control row stayed ok.
- 1 seed probe (`probes/allexist.py`) at 2eba09d and at head, run with the strict PATH and the tripwire. It used the loopback stub only.
- Static checks: comment-only `cmp` with control, `bash -n`, ASCII scan, name/id/secret scan, removed-test-lines count with control.

## NOT RUN
- Hosted CI and CodeQL on the PR.
- Any real deploy, or any run of `deploy-from-ci.sh` outside the tests and their fakes.
- Any real `az`: not executed, and not read by path.
- Any Entra run or hosted seed.
- The dotnet, web and package jobs: no path they read changed in the fix round.
- shellcheck.
- No Jira read.

## Corrections
- My brief says "`scripts/deploy-from-ci.sh:205` (re-print the line at head)". At head the pass-through line is `:206`; the comment commit added one line, and it is unchanged. The `-o json` call is `:202`.
- Round 1's runner appended the inherited PATH after the tripwire. Mine builds a strict PATH plus a node-only folder, as the fix round recommended for `test_run_demo.py`. My runner also restores default SIGINT for each child, so a background-started loop matches CI. `test_run_demo` was 23/23 on both trees.
- Fix-round STATUS: checked against its claims, no correction needed. Red-first reasons, counts (241, lost 0, gained 5), the comment-only proof and the held-item text all match what I measured. It said it did not build the merge with new main; this gate did, and it is clean and green.
