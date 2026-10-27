# QA gate verdict - Secuura/Blockchain PRs #1729, #1730, #1731

- Tier 2, round 1 of 2. Gate model: Claude Sonnet 5.5 (claude-sonnet-5-5).
- Window: 2026-10-27 08:38 - 08:49 AEDT.
- Workspace: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/gate-b2-1027/` (clone in `repo/`, private TMPDIRs in `tmp/`, raw outputs beside them).
- Pushed / merged / commented / edited: nothing.

## Pins (start = end, equal to the briefed pins)
```
5c40e82cb53912a8a8b26b3545731e505bb6c4a1  refs/heads/develop
a5a5887b86bf57231ce9f6843dc0952f255f500c  refs/pull/1729/head
9295b0209d9b4e15baf68e531c04edffe15b2ec8  refs/pull/1730/head
cfd01099ef8d1b735e208e990705b2abcb4d82ee  refs/pull/1731/head
```
Saved as `lsremote_start.txt` and `lsremote_end.txt` in the workspace; `diff` of the two is empty. `gh pr view` also reported the same headRefOid for each PR. All three PRs share merge-base `ec3313a80440` (develop has since moved to 5c40e82; the files each PR touches are untouched on develop).

## BLUF
| PR | Verdict | Worst finding |
|---|---|---|
| #1729 KS-1563 | GO | INFO: the brief's "product hunk" does not exist. Both files are test files, so the red-proof is tampered hook copies, which is what the PR says. Every number reproduced. |
| #1730 KS-1523 | GO WITH NOTES | INFO: the diff has no executable change to `check.cjs` (header comments only, as the PR body says), and 3 baseline floors changed, not 5. The brief's description of a "regex fix" is not what the diff holds. LOW: CLAUDE.md:407 is now one very long line. |
| #1731 KS-1465 | GO | None above INFO. Leak, fix and cell-5 red-proof all reproduced exactly. |

Merge order: no conflicts, and the sequential orders give one tree for every pair and for all three (details at the end).

## #1729 KS-1563 (Seat S 3rd)

**FOUND**
- Diff is exactly 2 files, +55/-6 (`pre_push_hook_base.test.sh`, `pre_push_hook_base_fixture_guard.test.sh`), per `gh` and per `git diff dev...pr1729`. Both are test files. No product code is touched, so there is no product hunk to revert.
- Minor 1: the false "reversible if a cell aborts" claim is replaced by a comment naming the real mechanism (the `mktemp -d` `$WORK` tree plus the EXIT trap). Verified by reading the diff.
- Minor 2: "the only pinned tally in this directory" is replaced by a census claim. The directory holds 74 `.test.sh` files at head, matching "all 74".
- Minor 3: CASE 12 gains three cells (path line by shape, the rule sentence, `st/nogate` absent at the fixture's bare origin). The fixture guard pin moves 33 to 36.

**TESTED-HOW** (private `TMPDIR=tmp/r1`, `tmp/rm_*`; the suites need no node deps; deps were absent and were not needed)
- At head: `pre_push_hook_base` 36 passed / 0 failed, rc 0. `pre_push_hook_base_fixture_guard` 12/0, rc 0. `pre_push_hook_base_leg_comment` 4/0 of 4, rc 0. Comment is graded by exact string and passes.
- Tracked hook `.githooks/pre-push` sha256 `74e8d270...d3dba` at head, equal to the PR body's figure, and unchanged after all runs (`git status` clean).
- Red-proof via `HOOK_SH=<tampered copy>` (copies in `tmp/mut/`, line numbers asserted by diffing against the tracked hook):
  - control (untampered copy): 36/0
  - T1 delete path-line echo (line 316): 35/1, red = "the refusal names the PATH it looked for" only
  - T2 delete rule-sentence echo (line 317): 35/1, red = "the refusal states the rule" only
  - T3 `exit 1` to `:` (line 318): 36/0 (survives, as the PR says)
  - T3b `exit 1` to `exit 0`: 34/2, red = "REFUSES the push" and "st/nogate is ABSENT at the fixture's bare origin". Only the origin cell is new; the other is pre-existing.
  All tallies equal the PR body's table. The new cells discriminate.

**NOT TESTED**
- Full `run-shell-suites.sh` (95/0/1) was not re-run (about 9 minutes, and it is the same code path as the three suites above).
- Preflight legs, not re-run. The PR's own "13/16 legs ran, NOT a pass" statement is accurate in form.
- The fixture guard reds at 35 or 37 cells were not exercised.

**SEVERITIES**
- INFO: T3 surviving is disclosed by the PR. The origin cell stands on T3b, which I reproduced. The path-line assertion pins shape, not the exact path, also disclosed.
- INFO: the brief mentions reverting "ONLY the product hunk". There is none; the PR is test-only by design.
- No MAJOR, MINOR or LOW.

## #1730 KS-1523 (Seat V 3rd)

**FOUND**
- 6 files, +200/-11 as claimed. Three one-line floor diffs (auth 93 to 105, api-gateway 111 to 122, vc-issuer 17 to 19). `security` and `m365-integration` baselines are untouched (zero slack, per the PR). The brief said five; the PR body says three, and the diff says three.
- `check.cjs` diff is header comments only (+16/-2): no executable line changed, including line 267. The PR body states this ("header only"). The brief's "regex fix around line 267" is not in the diff; the mutants attack the existing regex.
- Code list: the old list `TS1192/TS2307/TS2305` is gone from all three places (`check.cjs` header, `CLAUDE.md:407`, the ks1000 header comment), and the new list (TS1192, TS2306, TS7016, `import("/abs")`; NOT TS2305 / TS2307) is in all three.

**TESTED-HOW** (deps ABSENT before: ran `npm ci --ignore-scripts` with a workspace-local npm cache, rc 0, then `npm run build --workspace=packages/shared`, rc 0; `TMPDIR=tmp/r3`)
- ks1000 suite at base `ec3313a80440`: 70 passed / 70. At head `9295b02`: 73 passed / 73 (same vitest invocation, `--root services/auth ks1000-auth-test-files`).
- Mutants applied to `check.cjs:267` by line number, content of the line asserted first, `git checkout --` after each, sha256 after each equal to head (`d406fab3...6585a2`, the PR's figure):
  - M1 lookahead removed: 72/73, red = LOOKAHEAD cell only
  - M2 class weakened (`-` dropped): 72/73, red = LOOKAHEAD cell only
  - M3 `g` removed: 72/73, red = `g` FLAG cell only
  - M4 escaping removed: 72/73, red = ESCAPING cell only
  All four mutants dead, each on its own cell; I did all four, not two.
- Leg 16 (`bash scripts/preflight/test-types-ratchet.sh`) at head: rc 0, "OK - 5 service(s)", examined counts 105 / 122 / 19 / 40 / 26. The raised floors equal the actual counts exactly.
- Tightening control: set the auth floor to 106 (scratch edit, restored by `git checkout --`, file is back at 105): leg 16 rc 1, "EXAMINED test files fell below the baseline's floor: 105 examined, floor 106". The gate bites.
- Code-list grep: old-list pattern across the whole repo at head (excluding `node_modules`, `.git`): 0 hits. Positive control: `TS2306` found in exactly the three expected files. Old list at base `ec3313a` is present in `CLAUDE.md:407` and the ks1000 test, confirming the grep finds what it should.

**NOT TESTED**
- `services/auth` full unit suite (1146/1146) and the shell runner (95/0/1) were not re-run. The PR itself reports an unrelated load flake in ks949 on the first auth run.
- `api-gateway` and `vc-issuer` unit suites not run (PR does not claim them).
- The claim that item (b)'s limit (`~`, `+`, space siblings) is bounded and cannot admit a new error is reasoning in the PR, not something I tested.
- Windows unsupported: documentation only, not testable.

**SEVERITIES**
- INFO: the brief's description (a regex fix, five floors) differs from the diff (comments-only `check.cjs`, three floors). The PR is internally consistent and honest; the brief was wrong.
- LOW: `CLAUDE.md:407` is now one very long line (about 400 chars).
- LOW: the PR body says 13/16 preflight legs ran; it states plainly that this is not a pass, so no overclaim.
- No MAJOR or MINOR.

## #1731 KS-1465 (Seat R 4th)

**FOUND**
- 2 files as claimed. `run-schemathesis.sh` change is comment-only (+9/-1: the removed line is the old one-line `FINDINGS_DIR (output dir)` comment; the non-comment `FINDINGS_DIR="${FINDINGS_DIR:-$(mktemp -d ...)}"` line is byte-unchanged, now at line 34). The test change is +19/-2: a `CASE_TMPDIR` for the default case, cell 5, and expected count 4 to 5.
- `orchestrate.sh:159` does pass `FINDINGS_DIR=` (the header's claim holds; the file is `Blockchain/Testing/ci/orchestrate.sh`).

**TESTED-HOW** (private TMPDIR per series; leaked directories = subdirectories of that TMPDIR after the runs)
- Control: planted `run-schemathesis.CONTROL`, count 1; removed, count 0.
- Base (develop `5c40e82`, test and wrapper identical to the PR's base), one shared TMPDIR, three runs: 4 passed / 0 failed each, cumulative leaked 1, 2, 3. All 3 leaked dirs hold `schemathesis.json`.
- Head `cfd0109`, one shared TMPDIR, three runs: 5/0 each, leaked 0, 0, 0 (and 0 in a separate per-run series).
- Red-proof: at head, replaced only `CASE_TMPDIR="$WORK/dflt-tmp" run_case dflt` with `run_case dflt` (asserted exactly one match), cell 5 present: 4 passed / 1 failed, the only FAIL is cell 5 ("findings dir is OUTSIDE $WORK"), 1 dir leaked. Restored by `git checkout --`; sha256 equals the head blob (`f4156de5...e9c`).

**NOT TESTED**
- Schemathesis itself never ran (stubs), as the PR says. `orchestrate.sh` not run. The 95/0/1 shell-suite run and push-gate legs not re-run.

**SEVERITIES**
- No MAJOR, MINOR or LOW. INFO: header says the default dir is "not cleaned up" and the caller owns it; that is accurate and matches behaviour.

## Merge order (clone-local, `git merge-tree --write-tree` and sequential `git merge`, my clone only)
- develop+#1729, develop+#1730, develop+#1731: all clean (rc 0).
- Pairs, both orders, each step rc 0:
  - #1729 then #1730 = #1730 then #1729, tree `dfd04b7e7a47`
  - #1729 / #1731, both orders, tree `0d56c4bf6766`
  - #1730 / #1731, both orders, tree `a199f1afdc9a`
- All three, orders 1-2-3 and 3-2-1: same tree `796f5bf6d25c`. No conflicts anywhere. No two PRs share a file.

## Instrument errors (mine)
1. First leg-16 probe ran `node check.cjs auth` from the wrong directory (rc 2, "no such directory: auth"). The checker wants `services/auth` from the Dev root. I re-ran through the repo's own `test-types-ratchet.sh`, whose output is the result above.
2. My clone's `origin` is the cache `src`, whose develop was stale (`c56dd7c`) and which holds no PR refs, so the first `ls-remote` through it was not the GitHub state. I took the pins from `ls-remote` run in the cache clone against GitHub (read-only), and fetched develop and the three PR heads into my clone through an added `gh` remote using the cache's configured deploy-key `core.sshCommand` passed with `-c` (fetch only). All fetched SHAs equal the pins.
3. In the merge script, the "mt pr1729 vs pr1730"-style lines printed `merge-tree dev <pr>` output, not a pairwise merge-tree. They are noise and I did not use them; the pair results above come from the sequential merges.
4. The hook layer mangled variable-path git writes in my first attempts; I re-issued them with literal paths. No effect on results.

## Files outside my workspace
None created. All writes (clone, `tmp/`, npm cache, scripts, outputs) are under the workspace above, plus this verdict folder `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-27_gate-b2-batch/`. No git command was run against the live Blockchain checkout or any worktree. `git status` in the cache `src` clone read empty. The cache clone and the Blockchain `3_Access_Keys` deploy key were used read-only for `ls-remote` and `fetch`.
