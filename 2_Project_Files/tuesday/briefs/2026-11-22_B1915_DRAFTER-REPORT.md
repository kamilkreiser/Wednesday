STARTABLE: YES

# B1915 DRAFTER REPORT: lane U (seat Datasec/OXPd2-X29), the Universal Print registration fix round

Drafter B1915 (Opus, read-only toward the OXPd_2 project, Jira and GitHub), for Tuesday s310, on the commission `2026-11-22_B1914-B1917_OXPD-WAVE1-KITS_DRAFTER_COMMISSION.md`, lane U only. Kit: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-22_B1915_SEAT-X29_oxpd2-u-registration-fix-round.md` and its sidecar `.measured`. Scratch, programs and every log: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s310/d1915/` (`gate/` = the kit's THE TOOLS; `logs/`; `scripts/prove.sh` = the whole proving run; `clone` = the drafter's working clone, `clone2` = the fresh clone the patches were proven on). Clock reads by `date`: 20:15:59 (start), 20:34:08 (the origin re-read), 20:47:23 (the report's write).

## BLUF
- **The kit is startable.** It freezes the whole round as two patches: `1-red-first.patch` (four test files, seven new cells) and `2-fix.patch` (four product files). Eight existing files change under the two `Registration/` folders. No file is added and no project, lock, solution or workflow file changes.
- **Fix 1 (item 52):** `DeleteRegistration` now takes the attach lock. Cell X02 is RED at `main` (50 of 50 runs) and GREEN after the fix (100 of 100).
- **Fix 2 (item 53):** the issuer is now called through `Task.Run`, so the bound covers an issuer that blocks before it returns its task. Cell T11 is RED at `main` (5 of 5 runs, by its own guard assertion) and GREEN after the fix (100 of 100).
- **Fix 3 (item 54):**
  - The cheap check: an answer the issuer has already disposed is refused. Cell T12 is RED at `main` (20 of 20) and GREEN after (100 of 100).
  - K06 kills `mNoZeroPkcs8`, R05 kills `mReadCertLoose`, and C14 kills both `mTimeIgnored` and `mVerifySystemClock`.
  - `mCatchNarrow` and `mFixUndone` remain NAMED SURVIVORS on macOS. For `mCatchNarrow`, the drafter's extra try (a disposed configured issuer) did not kill it either.
- **Fix 4 (item 55(1)): the kit carries the RULE, not the limit.** The rule is that the signature value must lie below the issuer's RSA modulus.
  - Why: it is 29 product lines, measured by program over the patch. That is under the commission's "about 30".
  - The prototype proved it red, then green: cell C15 is RED at `main` (20 of 20 on macOS arm64) and GREEN after (100 of 100).
  - Q1 is STOP-CLASS. Tuesday may still choose the limit instead.
- **`main` MOVED during drafting.** Pull request 18 merged as `4e8828ee` at 20:35:19 AEDT. On a fresh origin clone at `4e8828ee` (`clone3`), the drafter measured:
  - this lane's eight files are byte for byte the same as at `bf6b441e`;
  - both patches apply, and the resulting files `cmp` equal;
  - red: total 1586, failed 4 (the same four cells);
  - green: total 1586, failed 0, succeeded 1582, skipped 4;
  - `RULES: clean (500 files)`;
  - `main`'s hosted run: `HOSTED 4e8828ee...: PASS` at `--total 1579`.
  The kit's numbers are now keyed to `4e8828ee`, with `bf6b441e`'s kept beside them.
- **Whole solution at `bf6b441e`, measured on a fresh clone from BASE (`clone2`):**
  - BASE: total 1578, failed 0, skipped 4.
  - Test patch only: total 1585, failed 4. The four failures are exactly X02, T11, T12 and C15.
  - Both patches: total 1585, failed 0, succeeded 1581, skipped 4.
- **Chain:** the 24 lock files are unchanged by `restore --force`; both publishes rc 0; `GUARD: clean (10 files)` and `GUARD: clean (11 files)`; `Ran 111 tests`, `OK`; `RULES: clean (500 files)` without `--source-documents`; 11 mutants, every undo `cmp` 0.

## FACTS RE-MEASURED (instrument and control)
| Fact | Instrument | Result | Control |
|---|---|---|---|
| origin main | `gh api -X GET .../git/matching-refs/heads/main` (20:15:59, 20:34:08, 20:47:51) | `bf6b441e...` (the sweep's and B1912's), then `4e8828ee0259b2605c98ba0f9f319f6527436778` (pull request 18, merged 09:35:19Z) | `.private` true, `.permissions.push` true; `compare bf6b441e...4e8828ee` ahead 1, 2 files, both Sessions tests |
| new main hosted | `hosted2.py 4e8828ee... --total 1579 ...` (`evidence/hosted-main-4e8828ee.out`) | `HOSTED ...: PASS`, run 45008282606 | its own control row `NOT-A-LINE-OF-ANY-LOG count 0` |
| new main, the lane's files | sha256 at both shas by program (`evidence/base-files-equal.out`) | 8 of 8 equal | - |
| open pull requests | `gh api -X GET pulls?state=all&per_page=100` | at 20:34:08: 18 in all, 1 open: 18, `b1912/f13-test-race`, files `tests/Datasec.Suite.Sessions.Tests/Fakes.cs`, `RefreshBoundCellTests.cs` | its file list read separately (2 rows) |
| refs `b1915` | `matching-refs/heads/b1915` | 0 | `matching-refs/heads/b` 18 rows |
| BASE tree | `git ls-files \| wc -l`, `rev-parse HEAD^{tree}` | 500; tree `de9817fc...` (= B1912 FACT 2) | the 13 and 9 `Registration/` files listed by `git ls-files` |
| BASE local tests | `dotnet test` via `heavy.py`, twice (clone, clone2) | total 1578, failed 0, succeeded 1574, skipped 4 | the red run of the same command reads failed 4 |
| locks unchanged | sha256 of the 24 `packages.lock.json` before and after `restore --locked-mode --force` | `cmp` rc 0 | the count 24 printed from `git ls-files` |
| toolchain | `.tools/dotnet/dotnet --version`, `gitleaks version` | 10.0.404, 8.30.1 | - |
| BACKLOG items | `sed -n 346,387p BACKLOG.md` | items 52 to 57 at 346, 353, 360, 367, 374, 381; WP4.1's row is at `:410` (the sweep said 409) | `grep -n -F 'WP4.1'` lines 382 and 410 |
| words | `words.py --control`; `words.py` over the added lines, the message and both patches | `CONTROL FIRED: 13 of 13`; `WORDS: clean (4 files)` | first pass: 2 hits ("not ruled on" in two comments), reworded, re-run clean |
| secrets | `gitleaks dir` over 11 neutral copies | rc 0 `no leaks found` | a planted token from two halves: rc 1, then quarantined |
| ASCII | `LC_ALL=C grep -c -v -x -E '[ -~]*'` per changed file | 0 for each of 8 | a planted tab: 1 |
| machine | `uptime`, `df -g`, `tmux list-panes -a` | load 4.81 to 8.70 over the window; 988 GiB free; 6 panes, no OXPd2 pane | - |

## THE PROOF RUN (`scripts/prove.sh` on `clone2`, fresh from BASE; every heavy job through `heavy.py` and the wave lock)
The output of `prove.sh` whole (`<d1915>/logs/prove.out`), then every loop summary, then the test totals:
```
start 20:33:35
lock files:       24
p-restore: rc 0 (1s, lock waits 0, load1 5.95) log <d1915>/logs/p-restore.log
locks cmp rc 0
porcelain after restore:        0
p-base-build: rc 0 (5s, lock waits 0, load1 5.95) log <d1915>/logs/p-base-build.log
p-base-test: rc 0 (13s, lock waits 1, load1 6.98) log <d1915>/logs/p-base-test.log
p-red-build: rc 0 (47s, lock waits 9, load1 6.14) log <d1915>/logs/p-red-build.log
p-red-test: rc 2 (46s, lock waits 7, load1 6.4) log <d1915>/logs/p-red-test.log
p-red-up: rc 1 (10s, lock waits 0, load1 5.78) log <d1915>/logs/p-red-up.log
p-loop-red-X02: rc 0 (20s, lock waits 0, load1 5.86) log <d1915>/logs/p-loop-red-X02.log
p-loop-red-T12: rc 0 (3s, lock waits 0, load1 5.18) log <d1915>/logs/p-loop-red-T12.log
p-loop-red-C15: rc 0 (11s, lock waits 0, load1 5.16) log <d1915>/logs/p-loop-red-C15.log
p-loop-red-T11: rc 0 (51s, lock waits 0, load1 5.36) log <d1915>/logs/p-loop-red-T11.log
second apply --check rc 1
p-green-build: rc 0 (3s, lock waits 0, load1 4.24) log <d1915>/logs/p-green-build.log
p-green-test: rc 0 (8s, lock waits 0, load1 5.83) log <d1915>/logs/p-green-test.log
p-loop-green-X02: rc 0 (37s, lock waits 0, load1 6.0) log <d1915>/logs/p-loop-green-X02.log
p-loop-green-T11: rc 0 (18s, lock waits 0, load1 6.26) log <d1915>/logs/p-loop-green-T11.log
p-loop-green-T12: rc 0 (17s, lock waits 0, load1 5.92) log <d1915>/logs/p-loop-green-T12.log
p-loop-green-C15: rc 0 (60s, lock waits 0, load1 6.9) log <d1915>/logs/p-loop-green-C15.log
p-loop-green-C14: rc 0 (36s, lock waits 0, load1 6.29) log <d1915>/logs/p-loop-green-C14.log
p-loop-green-K06: rc 0 (37s, lock waits 0, load1 5.03) log <d1915>/logs/p-loop-green-K06.log
p-loop-green-R05: rc 0 (38s, lock waits 0, load1 4.76) log <d1915>/logs/p-loop-green-R05.log
p-loop-ctl: rc 0 (0s, lock waits 0, load1 3.69) log <d1915>/logs/p-loop-ctl.log
mNoZeroPkcs8: build rc 0 | Total: 345, Errors: 0, Failed: 1 | RED K06 | undo cmp 0
mReadCertLoose: build rc 0 | Total: 345, Errors: 0, Failed: 1 | RED R05 | undo cmp 0
mCatchNarrow: build rc 0 | Total: 345, Errors: 0, Failed: 0 | RED none: GREEN | undo cmp 0
mFixUndone: build rc 0 | Total: 345, Errors: 0, Failed: 0 | RED none: GREEN | undo cmp 0
mTimeIgnored: build rc 0 | Total: 345, Errors: 0, Failed: 1 | RED C14 | undo cmp 0
mVerifySystemClock: build rc 0 | Total: 345, Errors: 0, Failed: 1 | RED C14 | undo cmp 0
mDeleteUnlocked: build rc 0 | Total: 345, Errors: 0, Failed: 1 | RED X02 | undo cmp 0
mIssuerOnCallerPath: build rc 0 | Total: 345, Errors: 0, Failed: 1 | RED T11 | undo cmp 0
mDisposedAnswerHeld: build rc 0 | Total: 345, Errors: 0, Failed: 1 | RED T12 | undo cmp 0
mModulusOff: build rc 0 | Total: 345, Errors: 0, Failed: 1 | RED C15 | undo cmp 0
mModulusNoLength: build rc 0 | Total: 345, Errors: 0, Failed: 0 | RED none: GREEN | undo cmp 0
p-chain-build: rc 0 (2s, lock waits 0, load1 4.59) log <d1915>/logs/p-chain-build.log
p-chain-test: rc 0 (8s, lock waits 0, load1 4.59) log <d1915>/logs/p-chain-test.log
p-pub-linux: rc 0 (2s, lock waits 0, load1 6.58) log <d1915>/logs/p-pub-linux.log
p-pub-windows: rc 0 (2s, lock waits 0, load1 6.58) log <d1915>/logs/p-pub-windows.log
GUARD-WARN: development CA deny-list holds 0 fingerprints (owed)
GUARD: clean (10 files)
guard linux rc 0
GUARD-WARN: development CA deny-list holds 0 fingerprints (owed)
GUARD: clean (11 files)
guard windows rc 0
unittest rc 0
Ran 111 tests in 5.913s

OK
no supplied-source folder rc 0
RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder here)
RULES: clean (500 files)
repo_rules rc 0
end 20:46:55
```
```
p-loop-ctl runs 3 pass 0 fail 0 other 3 seconds 0
p-loop-green-C14 runs 100 pass 100 fail 0 other 0 seconds 35
p-loop-green-C15 runs 100 pass 100 fail 0 other 0 seconds 60
p-loop-green-K06 runs 100 pass 100 fail 0 other 0 seconds 38
p-loop-green-R05 runs 100 pass 100 fail 0 other 0 seconds 38
p-loop-green-T11 runs 100 pass 100 fail 0 other 0 seconds 18
p-loop-green-T12 runs 100 pass 100 fail 0 other 0 seconds 17
p-loop-green-X02 runs 100 pass 100 fail 0 other 0 seconds 37
p-loop-red-C15 runs 20 pass 0 fail 20 other 0 seconds 11
p-loop-red-T11 runs 5 pass 0 fail 5 other 0 seconds 51
p-loop-red-T12 runs 20 pass 0 fail 20 other 0 seconds 3
p-loop-red-X02 runs 50 pass 0 fail 50 other 0 seconds 20
```
- BASE whole solution (`p-base-test.log`): `total: 1578`, `failed: 0`, `succeeded: 1574`, `skipped: 4`.
- RED (`p-red-test.log`): `total: 1585`, `failed: 4`, `succeeded: 1577`, `skipped: 4`; the four `failed` names X02, C15, T11 (10 s 004 ms, its guard), T12, each with the message the kit quotes (one each by `grep -c -F`). The UniversalPrint assembly alone (`p-red-up.log`): `Total: 345, Errors: 0, Failed: 4`.
- GREEN (`p-green-test.log` and again after the mutants, `p-chain-test.log`): `total: 1585`, `failed: 0`, `succeeded: 1581`, `skipped: 4`; both builds `0 Warning(s)`, `0 Error(s)`.
- The eight files of `clone2` after both patches equal `clone`'s by `cmp` (8 of 8, rc 0); `git diff --name-only` of `clone2` against BASE: 8 rows; `ls-files` 500.
- An earlier pass (`logs/mutants-1.out`, on `clone`) ran the same mutants with a candidate cell C16 (a configured issuer disposed after construction, B1905 P09) present: `mCatchNarrow` stayed GREEN, so C16 was dropped (it killed nothing new). In that pass X02 first read GREEN at BASE once (before its warm-up delete was added); with the warm-up, 20 of 20 and then 50 of 50 RED.


- The proof run on `4e8828ee` (`scripts/prove3.sh`, `logs/prove3.out`). Note: its `porcelain after restore: 4` counts the four test files, because the test patch was applied before that restore; `git status` lists only the eight owned paths after both patches.

## D-DECISIONS (each the coordinator's default, a Question in the kit)
- D1/Q3: the delete takes `_attachSync`.
- D2/Q2: `Task.Run` for the issuer call. The synchronous try/catch is folded into the existing catch, so the reason is unchanged.
- D3/Q4: `internal bool IsDisposed`; a disposed answer is `TokenAnswerRefused`. No new reason is added.
- D4/Q1 (STOP-CLASS): the modulus rule, refused as `IssuerNotTrusted` (Q6). An issuer without an RSA key is not checked by it (Q8).
- D5/Q5: `mCatchNarrow` and `mFixUndone` are named survivors.
- D6: the seven cells and two nested test helpers (`ExportWatchingRsa`, `PausingStore`).
- D7: ONE commit. The red state is never committed.
- D8: five README places.
- Q7: Opus, READY Step0+150, push Step0+120, pane X29, gate G1. Lock waits are allowed 40 min, raised from B1912's 30 because four seats share the lock.

## Q-QUESTIONS FOR TUESDAY (each with its default, as in the kit)
1. **Q1 (STOP-CLASS): modulus rule or named limit?** Default: the rule.
   - Item 55(1) offered both. The rule is 29 lines and is proven red, then green.
   - The rule's cost: it refuses a signature whose length is not the modulus's. PKCS#1 requires that length (RFC 8017 8.2.2). No real issuer has been measured.
2. Q2: `Task.Run`, or a bound on each caller's wait? Default: `Task.Run`.
3. Q3: the attach lock, or a removed-ids set? Default: the lock.
4. Q4: `TokenAnswerRefused`, or a new reason? Default: the existing reason.
5. Q5: survivors, or a Linux-only cell? Default: survivors.
6. Q6: which reason for s+n? Default: `IssuerNotTrusted`.
7. Q7: the level and the windows, as listed under the D-decisions above.
8. Q8: should non-RSA issuers be checked by the rule? Default: not checked.

## CHAIN INPUTS (every step's inputs exist at BASE or come from an earlier step; the kit's table, re-checked)
| Step | Inputs | From |
|---|---|---|
| 0 | the kit, the stamp | Tuesday |
| 1 | `<src>` ten files; `<repo>` local values; origin; BASE's push run | drafter scratch (exists, hashed); `<repo>`; GitHub |
| 2 | BASE files | Step 1 clone |
| 3 | `1-red-first.patch`, `loop.sh`, the baseline build | Step 1 copy; Step 1 |
| 4 | the red tree, `2-fix.patch`, `mutants.py` | Step 3; Step 1 |
| 5 | the green tree with the mutants undone | Step 4 (mutants.py restores each file from its copy, cmp 0) |
| 6 | the staged tree, `commit-message.txt` | Step 5; Step 1 |
| 7 | the commit, `origin/main` | Step 6; the fetch at 7(b) |
No step reads a file that a later step makes. The red loops need the red build (Step 3 builds it before they run). The mutants need the green build, and `mutants.py` builds for itself.

## UNMEASURED
- Every hosted-leg outcome for this head. In particular C15 and T11 on Linux and Windows: the platform there may refuse s+n itself, which would make C15 green at BASE on those legs.
- Whether a real device-certificate issuer signs with exactly the modulus length (it should, by PKCS#1), and which key type it uses (item 57).
- The `NEUTRAL-SCAN` wordings of Step 6(c) on a commit of this lane. They are RELAYED from kit B1912, which copied them from `main`'s hosted log.
- `mFixUndone` on macOS: no input was found that makes the field reads throw there.

## STOP-severity checks of the kit run on the drafter's own output (DRAFTER_RULES 2026-11-20 line)
- Run on the prototype, each passing, with the control that fired:
  - the eight-path property (the `diff --name-only` of clone2 against BASE: 8 rows);
  - the red messages (one each, by `grep -c -F` in the red log);
  - the loops (control: a made-up name gives `other 3`);
  - the mutants' undo (`cmp` 0 on each);
  - the ASCII check (control: a planted tab);
  - gitleaks (control rc 1);
  - words (control 13 of 13);
  - the second apply refused (rc 1).
- NEVER RUN, and marked so in the kit: the hosted comparison of Step 7(e) and the neutral scan of Step 6(c) on a commit of this lane.

## OUTSIDE-THE-FENCES DISCLOSURE
- **Writes.** Only my two files in `briefs/` (the kit and this report) and the kit's sidecar, plus scratch under `fleet/state/s310/d1915/`. In the project, the only writes were the shared lock folder `.tools/wave1-heavy.lock.d`, taken and released by `heavy.py` only (moved into my scratch `_quarantine/locks/`), and reads of the project's package cache.
- **Clones.** I made my two clones by `git clone` from B1912's drafter clone (`fleet/state/s310/d1912/clone`, read only, at `bf6b441e`), not from the origin. Their push URL is `invalid://no-push`. No ref was written anywhere but in my scratch clones.
- **Reads.** I read the B1904 and B1905 verdicts and their evidence programs. I read `BACKLOG.md`, `CLAUDE.md` and `CLARIFICATIONS.md` lines (read only).
- **Not done.** No `decision_queue.sh` in any form. No Source_Documents, key folder or NAS read. No Jira call. No HTTP but `gh api -X GET`. No az, docker or ssh. No message to anyone. No other drafter's file was touched.
- **Tests and the lock.** I ran tests while other seats held or waited on the same lock. The commission allows this by name ("your prototype runs take the same lock"). Each of my jobs took the lock in turn and never broke another holder's lock. The first background baseline build finished at 20:20:27, before my first test edit at 20:20:55 (by `stat`), so it built pristine BASE.
- **Load.** load1 rose to 10.28 at one wait; `heavy.py` waited under its rule.
