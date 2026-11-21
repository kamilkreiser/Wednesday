STARTABLE: YES

# B1873 DRAFTER REPORT: lane E fix round (round 2 of 2), OXPd 2 adapter, kit `2026-11-21_B1873_SEAT-X25_oxpd2-wp12-adapter-fix-round.md`

Drafter: Opus 5.5, read-only, for Tuesday s306. Window 22:20:25 to 22:49:58 AEDT 2026-11-21 (clocks by `date`). Kit 93578 bytes, sha256 `b587e8a7853da1f5b9bd8d0a601bbf03149f4b8f6fd36a824d321f54a8a67c68` at the write of this report; sidecar 175 of 175 claims measured, `stamp_check.py <kit>` rc 0; 8 unfilled slots (S1 to S7 and the last line), as the kit says.

## BLUF
- **Startable once stamped.** ONE fix commit on `b1849/wp12-oxpd2-adapter` at `523204dd`, fast-forward, no rebase. Everything it applies was prototyped and run by me in my own scratch clone: the cells are red against `523204dd`, then green with the code, and the twelve mutants are each red on their cells.
- **F1 (B1868), the token holder:** `Flights` now counts COMPLETED flights. A request that waited for a refresh uses that refresh's result, its access value or its failure. Measured: B1868's G17 shapes went from 2 endpoint calls to 1 (after a start) and from 2 to 1 after the prime (after a 401). B1869's hang shape: the late caller now ends with the first flight at `RefreshTimeout`, where at HEAD1 it hung past the 10 s guard.
- **F1 (B1869), the credentials:** `Forget` deletes the vault record first. A per-serial generation that a cache fill must match stops a fill from undoing `Forget` or `Issue`. Measured: G25 and G26 are red at HEAD1 and green with the fix. The G28 race (1000 iterations) read 1000 and 40 accepted at HEAD1, and 0 and 0 with the fix.
- **F4 (B1869):** `Forget` during a refresh leaves nothing stored. A generation is checked under the entry's lock, and the vault call runs inside that lock.
- **Deviation 4:** the new outcome `BodyFailed` is appended, taking the count from 13 to 14.
- **The other Minors:** the grant copies its values; four test holes get builder cells; README line 37 is corrected.
- **Prototype numbers:** the whole solution reads `total: 1248` (1234 + 14), `failed: 0`, `skipped: 4`, and `RULES: clean (403 files)`.
- **Merges:** `merge-tree` was clean against `main` (`8ae5e08c`), and against `main` with lane G and lane B merged in, both as merges and as squashes.

## Facts re-measured (instrument; control)
- Origin at 22:20:25, by `gh api -X GET` under the project GH_CONFIG_DIR: branch `b1849/wp12-oxpd2-adapter` = `523204dd`; main = `8ae5e08c`; lane G = `8efae983`, lane B = `c5a6ff84`; open PRs 0; 15 refs. In my clone, `git log` shows 523204dd's parent is `8ae5e08c`.
- RED: the cells on HEAD1's product code (`logs/p-red4.log`, the lane's test project) read 57 total, 10 failed: the 10 non-pinning cases, each red by assertion. The four pinning cells (T13 renewal, B07, B08, B09) are green at HEAD1 and red under their mutants.
- GREEN:
  - With the code: 57 total, 0 failed, five times (927 ms to 1.024 s), plus six earlier runs at 55 cases before I split T13 and A06 into one method per row.
  - Whole solution: build `0 Warning(s)`/`0 Error(s)`; 1248/0/1244/4. The 4 skipped are the secret store's Windows tests. Contracts.Tests passed.
  - Locked restore with `CI=true`: rc 0, porcelain 0.
  - Both publishes rc 0; `GUARD: clean (10 files)` and `(11 files)`.
  - `repo_rules.py` without `--source-documents`: `R5 hash half NOT RUN`, `RULES: clean (403 files)`. `unittest`: `Ran 60`.
- Mutants (`tools/mutants.py`; texts in `gate/3-mutants.txt`; `--check` says 12 mutants, 0 pairs not standing exactly once). Each undo was proved by `cmp`. Twelve of twelve were red:

  | Mutant | Red cells |
  |---|---|
  | mCountAtStart | T12 x3, T13 first start |
  | mFailNoReuse | T12 hang, T13 x2 |
  | mForgetNoCheck | T14 |
  | mFillUnchecked | A06 forget |
  | mForgetCacheFirst | A07 |
  | mNoBodyFailed | B06 |
  | mGrantNoCopy | T15 |
  | mRefreshNoCopy | T15 |
  | mGrantNoCheck | T15 |
  | mOpNoMethod | B07 |
  | mOpFirst | B08 |
  | mPeekLength | B09 |

- Text checks:
  - Added lines: 847. Non-printable 0 and tabs 0 (a planted U+200B is caught). 64-hex 0 (a planted one is caught). 43-character base64url 0.
  - `=>` census: 31 at HEAD1 and 31 at the fix (a planted text with 2 counts 2).
  - Boundary words over the 118 added product lines: 0 hits; all 20 planted words fire.
  - `words.py` over the added lines and the commit message: `WORDS: clean (2 files)`; its own control fires 13 of 13.
  - gitleaks: control rc 1; clone rc 0; changed files under neutral names rc 0. Neutral scan: `25 of 25`, `objects of this commit not among them 0`, `no leaks found`.
- Diffs:
  - `git apply --cached --check` with a scratch index: rc 0 for each diff.
  - HEAD1 tree + cells + code = the prototype tree (`f3375a65`) by `write-tree`.
  - In a worktree at HEAD1, `git apply` of the cells gives `?? tests/.../RaceCellTests.cs`, and with the code all seven sha256 equal the kit's.
- Hosted, by GET:
  - `523204dd` with `--total 1234 --rules 402 ... --unit 60 --floor 60`: PASS. The control `--total 1235` gives FAIL 4.
  - main `8ae5e08c` with 1191 and 370: PASS.

## D-decisions (all Tuesday's, as coordinator)
- **D21** (the F1 waiter rule): a waiter uses the result of a COMPLETED flight; a flight its caller abandoned is not counted.
- **D22** (holder `Forget`): a per-entry generation; the vault write and delete run under the entry's lock; the refresh ends `NoRefreshValue`.
- **D23** (credential cache): `Forget` deletes from the vault first; a per-serial generation; the first fill wins.
- **D24**: `BodyFailed` is appended after `SinkFailed`.
- **D25**: the grant copies BOTH values. The refresh copy goes one step past the ruling's words, so it is flagged.
- **D26**: the README and class-summary texts.
- **D27** (the cells): one new file, no round-1 test file edited.
- **D28**: the code is applied after the red run.
- **D29**: 12 mutants.
- **D30**: named limits:
  - `StoreRefreshValue` during a flight;
  - a lease already in hand is sent once after `Forget`;
  - a vault call under the lock;
  - the enrolled-serial timing;
  - the rotation row is held twice.
- **D31** (moved `main`): STOP-class.
- **D32**: hosted numbers.
- **D33**: 180/140, pane X25.

## Q-questions for Tuesday (default first)
- **Q31 (STOP-CLASS; S4 must answer it in words).**
  - Default: STOP if `main`'s changes since `8ae5e08c` touch the adapter folders, `Generated/`, `contracts/`, the contract tests or the lane's tests.
  - If `merge-tree` is clean, or `main` has not moved: push `C1` alone.
  - If the ONLY conflict is in `Datasec.Suite.slnx`: one merge commit resolving only the solution file with `place.py` (lane G's round-2 form).
  - Any other conflict: abort and STOP.
  - Alternative (a): push `C1` alone even when it conflicts.
- Q21 to Q30 and Q33: each default as above, with its alternative and cost in the kit.
- Q32: a NO GO in the delta review goes as a card to the product owner.

## UNMEASURED / PREDICTED
- The seat's whole-suite red total (1248, 10 failed). I measured red on the lane's project only.
- The hosted run of `C1` (`--total 1248 --rules 403`).
- The Windows leg of the new cells.
- A07 and the T12 synchronous-arrival assumption on a 2-core runner.
- The cost of holding a vault call under the entry's lock with a real store.
- B1869 G01's histogram after the fix.
- `gh .private` was not re-read this window.
- The B1868 and B1869 mutants other than those I adopted.

## Chain inputs
In the kit (CHAIN INPUTS): every input of each step exists at HEAD1 or comes from an earlier step.

## READ-WHOLE load (bytes, by program)
- **Mine: 406153 bytes.** That is DRAFTER_RULES, the commission, both verdicts, the round-1 kit, the gate commission, the round-1 STATUS and kit B1862 whole, the four HEAD1 product files and Fakes.cs, plus Oxpd2CallbackHandler.cs lines 1 to 200.
- I also read in part: Support.cs, DeviceCellTests.cs, CallbackCellTests.cs, TestClock.cs, the probe excerpts G17 and G25 to G28, and B1869's `mutant.py.txt`.
- **The seat: 271405 bytes plus the kit (93578).**

## Outside the fences (disclosure)
- Every git write verb ran only in my own scratch clone `fleet/state/s306/d1873/clone` (push URL `invalid://no-push`):
  - the branch `fix`;
  - the prototype commit `dff7f5e9`, made with a SCRATCH identity via `-c user.name/user.email` (`drafter@invalid.test`), never pushed, in a non-project clone;
  - scratch commits made by `commit-tree` for the merge simulations;
  - one worktree, `wt-head1`.
- One hook refusal: a `git -C $D/...` that the hook could not resolve. Nothing ran; I re-issued it with literal paths.
- My first two mutant batches failed with `NU1900`, because `dotnet test` without `--no-restore` hit the closed proxy. Those logs were moved to `d1873/_quarantine/`, not deleted. A fresh restore fixed it, and the kit now names the trap.
- Not read: the form kit **B1857**. I used B1862 as the fix-round form.
- No card was read. No Jira or GitHub write, no message, no `cd`, no delete.
- Heavy jobs ran through the round-1 `heavy.py` and the wave lock, with lock waits 0 and load1 between 1.30 and 3.41.
