VERDICT: GO WITH NOTE at head 04efb8107ab2f90e815f562ea3b169ea1a70d7eb (gated landing tree eaf0f260dbda94b00120959238ecb9503b2326d8, not the head tree d25458993d39). Both halves fix KS-1638 end to end in both directions, and half 1 is NOT a weakening. Two Minor findings, both in half 2's new code and tests, neither blocking: (1) the "refusal" does not hold back the suite run (it still fails the push); (2) no cell checks that the stripping actually happens.

# GATE S1: #1606 (KS-1638), tier 1, round 1 of 2

**Remote state.** `git ls-remote` at 14:17 AEDT, re-read at 14:58 AEDT, unchanged:
- develop `9512cc70d8c4ad8a1214b17a39d7c48456feb531`, tree `34ea098a022ca58aaff234a13c0603b21402fa14` (matches the brief).
- #1606 head `04efb8107ab2f90e815f562ea3b169ea1a70d7eb`: one commit, author Kam Kreiser <kamil.kreiser@secuura.ai>.
- #1597 head `8ec96bbac643dcb69ba90b2d81634f6cd40e85f1`.

**The head is not on current develop.** Its parent and merge base is `37834600a543` = develop~5 (KS-805). Develop then gained five merges: #1568 and the Q1 four. None of them touches a `.sh` file, the hook or the runner, and they share no file with this PR. Even so, the suites were run on the PREDICTED landing tree.

**Diff.** 3 files, +89/−2, exactly the files in the brief:
- `ks998_pre_push_judges_the_push.test.sh` +6/−2
- `preflight_deps.test.sh` +49/−1
- `preflight.sh` +33

`.githooks/pre-push` is unchanged.

## Named questions

### Q1. Is half 1 a weakening?
**NO.** Instrument: `s1/ks998.sh`. It ran ks998 standalone and fed planted hooks in through the suite's own `HOOK_SH` override, so no tree file was edited.

| run | ks998 | SC12 "without" | SC12 "ALLOW_FORCE=1" |
|---|---|---|---|
| develop file, real hook, flag unset | 80/80 | ok | ok |
| develop file, real hook, `ALLOW_FORCE=1` exported | **79/80** | **FAIL** | ok |
| head file, real hook, flag unset | 80/80 | ok | ok |
| head file, real hook, `ALLOW_FORCE=1` exported | 80/80 | ok | ok |
| **M1** hook never refuses a non-fast-forward (`.githooks/pre-push:80` `exit 1` → `:`), develop file, unset | 79/80 | **FAIL** | ok |
| **M1**, head file, unset | 79/80 | **FAIL** | ok |
| **M1**, head file, `ALLOW_FORCE=1` exported | 79/80 | **FAIL** | ok |
| **M2** hook ignores the flag, head file, unset / exported | 78/80 both | ok | **FAIL** (and "...remote now holds the rewritten tip" FAIL) |

- **M1 is killed by SC12 "without" on the head file whether or not the caller exports the flag.** `env -u ALLOW_FORCE` removes only the caller's leak. It does not remove the cell's ability to see the hook stop refusing.
- **M2 is killed by the SC12 flag cell.**
- R's red proof figures (79/80 → 80/80 → 80/80) are reproduced exactly.

### Q2. The derived strip list (half 2)
Instrument: `s1/derive.sh`. It extracts the PR's own block from `preflight.sh` (`hook_src=` through the closing `fi`, 19 lines) word for word and runs it against planted copies of the real hook.

- **(a) What the derivation finds on the real hook:** `ALLOW_FORCE` only, from `.githooks/pre-push:77`. That matches R. The hook's only other ALL-CAPS read is `ZERO`, which the hook assigns itself. `${1:-origin}` is positional, so it is correctly not matched.
- **(b) Can it strip something the suites NEED?** Not today. `ALLOW_FORCE` is read only by the hook, by ks998 (whose cells set it inline) and by the preflight_deps stub. No suite depends on inheriting it, and the full set is 91/0/0 with it stripped (Q4). It CAN in future:
  - V4: a hook line `${TMPDIR:-/tmp}` / `${HOME:-/}` makes it strip `HOME` and `TMPDIR` from all 91 suites, and nothing refuses that.
  - V5: a mention in a comment is also stripped.
  - V3, the reverse gap: an external control read as `$NAME`, `${NAME-x}`, `${NAME:+y}` or `${NAME:=z}` is NOT derived. The `ALLOW_FORCE`-named positive control cannot notice a second control that is missed.
  - These are design observations, not defects of this head.
- **(c) Planted reads:**
  - V1: adding `${FOO:-x}` makes the derivation give `ALLOW_FORCE FOO`, and both are stripped.
  - V2: adding a plain `BARPLAIN=1` assignment leaves the derivation at `ALLOW_FORCE`. Not stripped, as it should be.
  - Controls: V6 (ALLOW_FORCE renamed) and V7 (hook missing) both REFUSE with `fail=1`.
- **(d) Is a failure a FAIL, not a silent skip?** It is a FAIL: `fail=1`, the leg prints `FAIL - could not derive …`, rc 1, and the push is refused. **But it does NOT hold back the run.** The suite run at `preflight.sh:727-731` sits AFTER the `fi` at :726, outside the else branch. So on refusal the suites still run, with the hook's controls inherited, under a line that says "Refusing to run the shell suites" (:720). R's claim that the leg "withholds the run" is not true. Measured with `s1/withhold.sh`, which drives the PR's own `preflight_fixture_run` and reads the captured output:

  | case | verdict | did the suites run? |
  |---|---|---|
  | `nocontrol`, suite red | HOOKCTL-REFUSED/1 | **yes** ("shell suites: 0 passed, 1 failed") |
  | `nocontrol`, suite green | HOOKCTL-REFUSED/1 | **yes** ("1 passed") |
  | control: `noexport` (the de-slot refusal), suite red | DESLOT-REFUSED/1 | no (a real short-circuit) |

  This is Minor 1.

### Q3. R's census
**8 push suites and exactly one non-fast-forward suite: confirmed. "72 shell suites": NOT confirmed.**
- **Suite count.** The runner reaches 91 suites on both develop and the head: 71 under `Blockchain/Dev/scripts/__tests__` plus 20 under `systemTest/__tests__`. `git ls-files '*.test.sh'` also gives 91. R's own "91 passed" agrees with 91, not 72. Nit 1.
- **Push suites.** 8 suites run `git … push` outside a comment: check_no_demo_mutation_base, check_no_demo_mutation_missing_base, ks884, ks998 (44), ks998_stale_base_hint, pre_push_hook_base_fixture_guard, pre_push_hook_base (17, plus 1 in a comment = R's 18), pre_push_hook_current_develop. The grep's ninth hit, package_format_gate:688, is a string, not a push.
- **Non-fast-forward.** Only ks998 has a `--force` push (2, at :259 and :261). No `+refspec` anywhere.
- **Decisive instrument: the whole set under the real hook with the flag inherited, on develop.** Run e2e_dev (Q4): **90 passed, 1 failed**. The failure is ks998, cell `SC12 without ALLOW_FORCE…` only. So exactly one cell across all 91 suites was affected.

### Q4. The end-to-end case
**PASS in both directions.** Instrument: `s1/e2e.sh`.
- **Setup.**
  - A `--shared` clone of my clone, checked out at the predicted landing commit `15f10afce084` (tree eaf0f260).
  - `core.hooksPath .githooks`, so the REAL hook runs the REAL preflight.
  - Origin is a LOCAL bare repo. The push URL was printed as a receipt: `s1/e2e_land/origin.git`.
  - Branch `fx` was published, then rewritten with a Blockchain/Dev change. Control: the published tip is not an ancestor of the rewritten one.
- **Without the flag** (`env -u ALLOW_FORCE git push --force`): rc 1, the `REFUSED — non-fast-forward` line is present, the preflight never starts, and origin keeps the published tip.
- **With `ALLOW_FORCE=1`:** rc 0 and origin moves to the rewritten tip. The preflight output:
  - `ALLOW_FORCE=1 — proceeding`
  - `de-slotted 39 variable(s)`
  - `hook controls stripped for the suite run: ALLOW_FORCE (KS-1638)`
  - both SC12 cells ok
  - `shell suites: 91 passed, 0 failed, 0 skipped (of 91)`
  - `PREFLIGHT INCOMPLETE — 13/16 legs ran, 3 SKIPPED. Nothing failed.` (3/4/8 skip because no stack is running.) 535 s.
- **Red control: the same instrument on develop 9512cc70.** Without the flag: refused. With the flag: rc 1, leg 14 at 90/1 (ks998 SC12 "without"), `PREFLIGHT FAILED on leg(s) 14`, and origin is NOT moved. This is the ticket's defect, reproduced by the same instrument that shows it fixed.

### Q5. The fixture change
**Every existing cell still tests what it tested.** Some new cells do not test what their names say.
- **Red-first.** Running the head's `preflight_deps` against develop's `preflight.sh` (`s1/redfirst.sh`) gives 58 ok / 3 FAIL, the three stripping-dependent cells. That matches R.
- **Cells whose meaning changed:**
  - `leg 14: suites green -> preflight passes` (and the two leg-1 cells, which use the same fixture) now also requires the hook-control derivation to succeed. That is a stricter pass condition, not a weaker one. The hook stub is the minimal real shape (`${ALLOW_FORCE:-0}`).
  - The DESLOT cells are unchanged: the de-slot refusal happens before the derivation, and the classifier checks for it first.
  - The HEADER-MISMATCH cell is unchanged.
- **`KS-1638: that refusal SHORT-CIRCUITS — a red suite present, still not run`** (`preflight_deps.test.sh:518-519`) passes while the suites DO run (Q2d). The classifier picks the refusal text first and never looks at whether the run happened.
  - Mutant M4 makes the refusal genuinely hold back the run (it moves the run into the else branch). With M4 the suite still reads 61/61, so the cell cannot tell the claimed behaviour from the actual one.
  - The cell this one copies (:492, DESLOT) has the same blind classifier, but there the behaviour really is true. This is Minor 1's test half.
- **The inverted-want control `…NOT in that line`** (:508-509, `SOMETHING_ELSE`) is vacuous. No input in the fixture could ever produce that name. It does not test the assignment-vs-`:-` discrimination, and neither does the `nocontrol` stub: `ZERO=0` there would refuse even if it were wrongly derived, because ALLOW_FORCE is missing either way. V2 in Q2(c) is the only test of that discrimination. Nit 2.
- **No cell checks that the derived names actually leave the suites' environment.** Mutant M3 removes the `env_clear+=` loop at :724 but keeps the printed line, and it survives at 61/61. Because half 1 makes SC12 immune to an inherited flag, no in-hook cell would go red either, so half 2's stripping has no test with bite. This is Minor 2.
- M5 removes the positive control: killed by :516 and :519. Mutant runner: `s1/pfmut.sh`. The file was restored byte-identical by an EXIT trap.

### Q6. Test Evidence
**91 passed, 0 failed, 0 skipped on the predicted landing tree**, matching R's figure.
- **Landing tree.** Run `B_land_clean`, cwd = Blockchain/Dev, no slot variables and no ALLOW_FORCE in the environment, packages/shared built with tsc (rc 0, 29 dist entries). 488 s. The in-hook run of Q4 gives 91/0/0 a second time, with the flag present and stripped.
- **Head tree first run.** The first run on the head tree (wt-head) read 89/2:
  - ks949: "packages/shared is not built".
  - preflight_test_types_ratchet_leg: "no workspace install". My first link step had linked only the root and Blockchain/Dev node_modules.
  - Both are environmental. The same two suites pass on the landing tree once all per-package node_modules are linked and shared is built.
- **Suites I did not run:** none of the 91 was left out. I did not re-run the head-tree set after fixing the environment; the landing tree is the one that lands.
- Not run: jest/vitest service suites. This PR touches no service code.

### Q7. Predicted landing tree and overlap with #1597
`git merge-tree --write-tree` in my clone, all rc 0, no conflicts:

| step | tree |
|---|---|
| develop 9512cc70 | 34ea098a022ca58aaff234a13c0603b21402fa14 |
| + #1606 (solo) | **eaf0f260dbda94b00120959238ecb9503b2326d8** (≠ head tree d25458993d39, because the base is develop~5) |
| + #1597 (solo, on develop) | 9f0806065a68d0bcc0dd186abdbb51f2b8eaf5a4 |
| develop + #1606, then + #1597 | 4daaf4ff919da01c9c36b52c7f8fb66b08991b7c |
| develop + #1597, then + #1606 | 4daaf4ff919da01c9c36b52c7f8fb66b08991b7c (order-independent) |

- **Overlap with #1597: 0 shared files.** #1597 changes three originate files. Control: #1606 against itself gives 3.
- develop → eaf0f260 changes exactly the PR's 3 files, +89/−2.

## Severities (file:line, head 04efb8107ab2)
- **Minor 1: the refusal does not hold back the run, and its cell cannot see that.**
  - Where: `Blockchain/Dev/scripts/preflight/preflight.sh:727-731` runs the suites after the derivation's `fi` (:726). The refusal branch (:718-722) prints "Refusing to run the shell suites" and then they run anyway, with the hook's controls inherited.
  - It still fails closed: `fail=1`, rc 1, push refused. So this is not a bypass, but the output is false.
  - The test `Blockchain/Dev/scripts/__tests__/preflight_deps.test.sh:518-519` passes against both the actual behaviour and the claimed one (M4).
  - Fix shape (author's call): move :727-731 inside the else branch, and have the cell assert that `^shell suites:` is absent from `PREFLIGHT_FIXTURE_OUT`.
- **Minor 2: the stripping itself has no test with bite.** M3 (names printed, nothing stripped) survives the whole preflight_deps suite, and since half 1 hardened SC12 against the flag, ks998 would not catch it in-hook either. A cell whose fixture suite echoes `${ALLOW_FORCE-unset}`, run with `ALLOW_FORCE=1` exported, would close it.
- **Observation: the derivation's edges** (Q2b). It would strip HOME/TMPDIR if the hook ever read them with `:-`. It strips names that appear only in comments. It misses controls read in any form other than `:-`.
- **Nit 1:** R's census says "72 shell suites". The runner reaches 91 on develop and head, which is R's own Test Evidence denominator.
- **Nit 2:** the inverted-want control (`preflight_deps.test.sh:508-509`, `SOMETHING_ELSE`) is vacuous.
- **Nit 3:** `preflight.sh:700-701` cites `.githooks/pre-push:50` as the documented path. The documented `ALLOW_FORCE=1 git push` is at :45-46 and the code at :76-82, matching the brief. Line 50 is the "NOT closed by this" note.

## HOW
- **Clone.** `git clone --shared --no-checkout` of the project into `s1/repo`. Origin was set to git@github.com:Secuura/Distributed_Secuura.git with the push URL disabled. I fetched develop, pull/1606/head and pull/1597/head with the project checkout's `core.sshCommand` plus `-o ServerAliveInterval=30`.
- **Worktrees** inside s1/: `wt-head` (04efb810), `wt-dev` (9512cc70), `wt-mut` (04efb810, mutants only, restored), `wt-land` (prediction commit 15f10afce084 → tree eaf0f260).
- **node_modules.** Per-entry symlinks into the project checkout's installed modules, read-only (`nm.sh`, `nm2.sh`). `@secuura` was rebuilt as relative links inside each tree (`relink.sh`). The original links were moved, not deleted, to `s1/_q/`.
- **Commands.** cwd was set through `s1/incwd.py` (python subprocess); no `cd`.
- **Scripts:** `suites.sh`, `ks998.sh`, `derive.sh`, `withhold.sh`, `pfmut.sh`, `redfirst.sh`, `mt.sh`, `e2e.sh`. Logs are in `s1/logs/`.
- **Pushes.** The only pushes went to the local bare repos `s1/e2e_land/origin.git` and `s1/e2e_dev/origin.git`. Nothing was pushed to any real remote. There were no GitHub or Linear writes and no git write verb under !CODING (only ls-remote, rev-parse, status and config --get). At the end, the project checkout shows 0 tracked modifications and every scratch worktree shows 0 tracked modifications.
- **Self-report.**
  - A hook refused two of my `git -C $VAR` write verbs (worktree add, merge-tree) aimed at my scratch clone, because it cannot resolve a variable. I re-issued them with literal paths or from a script file.
  - It also refused an `unlink`; I used `mv` into `s1/_q/` instead.
  - It refused a `======` separator (zsh word-splitting).
  - Nothing was bypassed.

## NOT tested
- Linear (the KS-1638 ticket text), and R's logs in r51/ (I measured independently).
- R's live push line `hook controls stripped … ALLOW_FORCE`: not read from R's log. Reproduced in my own e2e instead.
- Behaviour on Linux/dash. The derivation is bash in preflight.sh, and the hook is unchanged.
- The stack-dependent legs 3/4/8 (skipped: no stack).
- A head-tree re-run of the full set after the environment fix (the landing tree was run instead).

MODEL: claude-opus-5-5
WALL-CLOCK: ~42 minutes (14:17 -> ~14:59 AEDT)
sha256: 287c2c8295bef8071f556c4e3a1e0936b81f08f255780b2ca4bef225209ec051
