GATE B1852: GO WITH FINDINGS @ e909559 on main 61b17ec

Gate G1 round 2 of 2 (DELTA), reader B1852 (the whole lane; successor of round-1 reader B1838), OXPd 2 WP1.5, the session
and token broker fix round (kit B1845, seat X18): head `e9095598225e3ddbe7ff2ad942db44a41b815c81`, one parent
`70c1fad55128667e62fa5379719dfc6e0ba3ac1b` (the round-1 head); main `61b17ec01a563bbb67465cc799a170bbb7f1cf66`.
Read and measured 2026-11-21 18:53 to 19:45 AEDT (clocks by `date`) on Opus 5.5. Own clone from the origin with the
project deploy key (kit `clone.py`, mode `draft`, push URL `invalid://no-push`) in the session scratchpad
(`<scratchpad>/b1852/clone`; the workspace hook refuses git write verbs elsewhere); a second scratch clone
`<scratchpad>/b1852/merged` for the merge. Logs and programs: `/private/tmp/b1852-gate/` (`logs/`, `scratch/`, `out/`,
`chain.sh`, `mut.py`, `textscan.sh`). Every heavy job (3 at the head, 2 probe runs, 8 mutants, 3 on the merge) went
through the kit's `heavy.py` unchanged (sha256 of the six tool files equal to the kit's list): load first, the wave lock
by `mkdir` of exactly `<project>/.tools/wave1-heavy.lock.d` with `owner.txt`, closed local proxy, released by MOVE into
`/private/tmp/b1852-gate/_quarantine/locks/`; restores with `-p:NuGetAudit=false` (the closed proxy refuses the audit
request; the hosted legs run it). Waits behind B1853 and B1855 (up to 120 lock polls) were not findings. Never
`repo_rules.py --source-documents` with a source folder; no key folder opened; every value synthetic, none printed.

**BLUF.** The fix round does what its kit says. The round-1 points of this reader are closed or stated: F1 (a refresher
that blocks before returning its task) is CLOSED (measured by the reader's own probe and by mSyncBlock); F3 (grown record
buffer) is CLOSED (every retired buffer reported cleared; P04); F5 (b) is CLOSED (`RestartWindow` removed, V02) and F5 (a)
is closed in the code, README and R10; F4 is CLOSED (R08, R09; mWritten now reddens R08); F2 is KEPT as a README limit and
still measures as before (a token at true idle 49 min of a 30-min session), with E08 proving the bound. Scope, words,
gitleaks, no decode, suite 968/0, hosted PASS, and the merge with main 61b17ec0 (clean; 973/0; rules clean 329; Ran 60)
all hold. **No Blocker, no Major.** One Minor text finding (a comment still says "at most") and one records note.
Plain words: from this reader the branch can land when the second reader also passes; landing texts are in this folder.

## Findings

| # | Severity | Blocks? | Finding | Recommendation |
|---|---|---|---|---|
| G1 | Minor (text) | No | `src/Datasec.Suite.Sessions/TokenBrokerOptions.cs:14`, the XML comment of `RestartWindow`: "A record is restored only if its last activity is at most this long ago". The code (`TokenBroker.cs:760`, `idle >= _restartWindow` drops), the README and cell R10 say LESS than (a record idle exactly the window is dropped, measured by R10 and by mutant mRestore reddening R10). The seat named it itself (STATUS FOR RECORDS) and left it because the kit allowed no other product change. | One word, with the next change to the library (FOR-RECORDS 1). |
| G2 | Records | No | The README's D24 limit says the lengthening happens "only for a step smaller than the time since the record was last written": true when that time is read at the RESTART (E08 row 1: step 25 min one minute after the write, restart at true idle 29 min, restored; row 2: restart at true 10 min, dropped). Read as the time at the step, it would be false. | Optional clarity (FOR-RECORDS 2). |

## 1. What the kit's FOR TUESDAY section assigns to this reader

- **Read `70c1fad5..e9095598` whole** (one commit, 14 files, +643/-18) and the new README `## Limits`: five new limit
  lines (D21 overlap after a time-out; D20 pool thread held; D24 wall clock set back before a restart; D26 failing read at
  restart; D28 blocking handler), the refresh paragraph (D20, D23), "While the server runs" (D24), the four reasons (D27).
  The last line stays "The host does not use the broker yet."
- **D20 as built:** `TokenBroker.cs:400` `call = Task.Run(() => _refresher.RefreshAsync(key, renewal, user, token));`,
  locals at `:397-399`, bound unchanged at `:401`. `Task.Run` occurs once in the library (search over every `.cs`).
  A null inner task makes `Task.Run`'s proxy cancelled, which the existing `catch (Exception)` maps to `RefreshFailed`
  (F14 green, reader's H7-H10 null-task and throwing shapes green).
- **D23 as built:** `TokenBroker.cs:350-355`, after the still-current branch, before the hand-out; both clocks via
  `IdlePassed`. It also applies after a refused refresh (the caller then gets `SessionExpired`): as the seat says, accepted.
- **The reader's probe file, 37 cases, at the new head** (`reader-probes-r2.cs.txt`, output
  `reader-probes-r2-output.txt`, both in this folder; run in the scratch clone only, never pushed): first run
  (`logs/probes-1.log`) 111 total, 20 failed = all 20 seeds of the seeded fuzz, each on its 10 s guard. Cause read in the
  probe: the fuzz moved the test clock only `if (... kit.Refresher.Calls > callsBefore)` right after starting a call,
  which with D20 is no longer synchronous, so the hanging refresher's bound was never passed. This is the timing change
  the kit predicted for cells (D20's "existing cells that this changes"), not a product fault: after the same wait the
  lane's cells use (call entered and bound armed, then the clock moved; a refresh that never arms its bound still fails
  the 10 s guard, so nothing is masked), run 2 (`logs/probes-2.log`): **111 of 111 green** (lane 74 + probes 37).
  The fuzz's 20 seeds printed exactly the round-1 numbers (tokens handed out, refusals, restarts), seed for seed.
  - **SYNC-BLOCK (F1): CLOSED.** "caller still waiting 3 s (real) after the test clock passed the 30 s bound: False";
    after release the caller got `RefreshTimedOut` (round 1: True, then `SessionNotFound`); another session and
    `SignOut` answered in 0 ms; 1 record left (the other session's).
  - **D12 record writer (F3): CLOSED.** The probe now also reads the writer's report: `+` x40, `+` x60, accented x40:
    growths 1, every retired buffer cleared True; ASCII x1 and x64: growths 0. The allocation still shows the growth
    (4,941 to 5,061 B beyond estimate plus record), as the kit said; the proof is the cleared report and P04.
  - **D7 across a restart (F2): KEPT as a limit.** "restored 1; at true idle 49 min (idle timeout 30 min) a read gives A
    TOKEN", unchanged. The README sentence bounds it at the step (here 25 min; the session lives at most until wall idle
    30 min = true 55 min), which E08 asserts (restored; `Sweep` 0 at wall idle 29:59, 1 at 30:00, reason `Expired`).
    The fuzz's "idle start moved later" maxima are unchanged (seed 19: 32 min 35 s), each under its step.
  - **`RestartWindow` gone (F5 b):** the probe file names no `SignOutReason.RestartWindow` (it compiled unchanged but for
    the two lines above); V02 asserts the four names and values 1 to 4.
  - Every other probe as in round 1: H1-H4 (3,730 handles, 11,198 calls, 1 distinct message), H5/H11 (42 near subjects),
    H7-H10 (20 shapes), H8 bound, H12/H13 (1,000 callers -> 1 call; 1,000 waiters + sign-out -> 1,000
    `SessionNotFound`), H14 (16 clock rows), H15 (50 crafted records: restored 4, expired 5, unreadable 45, deleted 50),
    R03 (776 of 776 bit flips `StoreFailed`, files byte-equal), H17 store failures, raw files and disposal clean.
- **D20 waits did not weaken F08/F09 (or F05 x2, L01):** in the diff each hunk ADDS one `await Expect.Eventually(() =>
  kit.Refresher.Calls == N && kit.Clock.LiveTimers == 1, ...)` line before the first listed line; no assertion line is
  removed or changed (F05 hang keeps `Assert.Equal(1, kit.Clock.LiveTimers)`, F08 and F09 keep
  `Assert.Equal(1, kit.Refresher.Calls)`). `Expect.Eventually` fails on its 10 s guard, so a mutant that never reaches the
  condition still reddens the cell (mTimeout below reddens F05 x2, F08 x2, F09, L01).

## 2. Scope (measured in the reader's clone)

`git diff --name-status 70c1fad5 e9095598`: 14 rows (2 `A` `.cs`: `ClearingBufferWriter.cs`,
`RefreshBoundCellTests.cs`; 12 `M`), all under `src/Datasec.Suite.Sessions/` or `tests/Datasec.Suite.Sessions.Tests/`,
no `D`, no project file, lock file or solution line (the property checked by program; control with a planted
`M Datasec.Suite.slnx` and a `D` row: both named). `git diff --quiet` over the solution file, `Directory.*.props`,
`global.json`, `.github`, `build`, `README.md`, `NuGet.config`, `*.csproj`, `*packages.lock.json`, the secret store and
its tests, `packaging`: rc 0 (control over the lane's src: rc 1). Added lines 643: 0 outside printable ASCII (control 1).
`words.py --control` 13 of 13; over the added lines and the commit message: `WORDS: clean (2 files)`. gitleaks 8.30.1 with
the workflow's options over the 14 changed files under neutral names plus the added lines and the message (16 files):
rc 0, `no leaks found`; planted control (a token built at run time, never printed) rc 1. **No token decode:** the round-1
search repeated over the library (`FromBase64`, `Base64Url.Decode`, `JsonDocument`, `JsonSerializer`, `Split(`,
`IndexOf(`, `Jwt`, `claim`, `unique_name`, `preferred_username`, `upn`, `GetString`, `Parse(`, plus `Thread`, `Timer`,
`Task.Delay`, `DateTime.Now`, `Stopwatch`, `Environment.`, `System.Net`, `ArrayPool`, `File.`, `Directory.`,
`Console.`): the only hits are the record reader's own `GetString`/`GetBytesFromBase64` of record fields
(`SessionRecord.cs:190-227`, as round 1) and the one `Task.Run` (`TokenBroker.cs:400`). `ClearingBufferWriter` holds no
pool and no static state.

## 3. Suite and hosted

Through the lock at e9095598: restore `--locked-mode -p:NuGetAudit=false` `CI=true` rc 0 (closed proxy; `git status
--porcelain` 0 lines after), build Release `0 Warning(s)` `0 Error(s)`, whole suite **`total: 968`, `failed: 0`,
`succeeded: 964`, `skipped: 4`** (894 + 74). Hosted push run 44881807696 of e9095598 read by GET with the kit's
`hosted.py` (`--total 968 --rules 327 --skipped-linux 4 --skipped-windows 19`): **`HOSTED e9095598...: PASS`**; four jobs
success, attempt 1; linux and windows `total: 968` twice each, `failed: 0`, skipped 4 / 19, `0 Warning(s)`,
`0 Error(s)`, `GUARD: clean (10 files)` / `(11 files)` (unchanged from main: the host references nothing of the broker);
rules `Ran 53 tests`, `floor 53`, `RULES: clean (327 files)` (the branch's own tree, cut before pull request 8);
secret-scan both PLANTED-CONTROL lines (neutral 25 of 25), `objects of this commit not among them 0`, `no leaks found`
x3. Control with `--skipped-linux 5`: `FAIL 2`. Windows log: 20 lines holding `skipped`, 0 name a Sessions test.

## 4. The merge with main 61b17ec0

`git merge-tree --write-tree 61b17ec0 e9095598`: rc 0, **clean**, tree `e1489d23d5e2631b9f8c26420afb1dd66251c2ec`, merge
base 5e36d8dc. Main's side since the base touches `.github/workflows` (1), `build` (2), `contracts/oxpd2/generator` (2),
`src/Datasec.Suite.Adapters.Oxpd2/Generated` (5), `tests/Datasec.Suite.Contracts.Tests` (4): 0 paths under the lane or
the solution file. The tree checked out by `read-tree -u -m` in the second scratch clone (`git diff --quiet e1489d23`
rc 0, 329 files) and run through the lock: restore rc 0 (0 lines naming http, fetch or download; no lock file changed),
build `0 Warning(s)` `0 Error(s)`, whole suite **`total: 973`, `failed: 0`, `succeeded: 969`, `skipped: 4`** (899 + 74,
the expected). `python3 -I build/repo_rules.py <tree>` (no `--source-documents`; the default folder does not exist next
to the scratch clone, so `R5 hash half NOT RUN`): **`RULES: clean (329 files)`** rc 0; the same with an empty folder:
clean (329); control (a planted tracked `.gitleaksignore`): `RULES: R1 .gitleaksignore:0`, then unstaged and moved to
quarantine, index back to e1489d23. `python3 -I -m unittest discover -s build/tests`: **`Ran 60 tests`, `OK`**; the
merged `ci.yml` holds `FLOOR=60`. Main 61b17ec0's own push run (the d1844 `hosted.py`, sha256 `f929194e...`,
`--total 899 --rules 293 --ran 60`): PASS, with the three Analyze rows success. Open code-scanning alerts on main: 0.

## 5. Mutants (the reader's own, on the NEW head; each applied by `mut.py`, build and test of the Sessions test project under one hold of the lock, total 111 = lane 74 + probes 37, then the original bytes restored and `git diff --quiet -- src` rc 0, 8 of 8)

| Mutant | Edit | Red (lane cells; reader probes) |
|---|---|---|
| mWritten | `\|\| record.Written > nowWall` removed (`:760`) | **R08** (round 1: no lane cell; F4 a closed); probe H15 restart |
| mPsid | key lookup compares the serial only (`:592`) | **B07**, B04 |
| mAnswerMono | answer acceptance ignores the monotonic clock (`:476`) | F06 "later by the wall clock, earlier by the monotonic" |
| mWall | monotonic halves of `IdlePassed` and `RemainingLife` inert | E04, E06, **E07 (monotonic alone)**, F02 monotonic; probes H14 and all 20 fuzz seeds |
| mRestore | idle and window tests at restore never true | R01, R02, **R10**; probe H15 |
| mZero | `TokenGrant.Dispose` does not clear | F11, F13, F15, F05 late, F06 x3, F09, L02; probes H8, 1,000 waiters, raw files and disposal |
| mSyncBlock | the D20 fix inverted (inline call restored) | **F11, F12** (only these; the reader's SYNC-BLOCK probe records rather than asserts) |
| mTimeout | bound -> infinite | F05 x2, F08 x2, F09, L01 (by the D20 wait's guard), F11, F12, F13, F15, E07 x3; probes H8 and 20 fuzz seeds |

Every mutant red by assertion; every build `0 Error(s)`; after the last restore `git diff --quiet -- src` rc 0, so the
product source equals the head whose whole-suite run is item 3. The lane's mutants of this round named for B1853
(mStaleWaiter, mSubjAnswer, mRace, mLate) are the second reader's.

## 6. The seat's deviations 1 to 8

1 predictions written after the first test edits, before any build or run: **accepted** (records; nothing could have
shaped them). 2 one `sed -i ''` on one class-summary comment line of `ExpiryCellTests.cs` in its own clone: **accepted**
(records; the line "Cells E01 to E08 ..." is in the reviewed diff, nothing deleted). 3 eleven mutants, not "twelve": **accepted**
(the kit's own list holds eleven; the seat ran them plus three). 4 mTimeout and mRace redden D20-changed cells through the
wait's guard: **accepted** (reproduced for mTimeout above; F11 and F12 redden by their own assertions; the assertions are
unchanged). 5 L01 got a D20 wait (`Calls == 3`): **accepted** (only a line added; it is the cell's third call). 6 E07's
"which" printed through the test output helper: **accepted**. 7 R09 builds both brokers by hand over one `StoreRoot`:
**accepted** (read: the restarting broker is over `FakeRecordStore { FailLoad = true }` set before its constructor;
asserts `RestoreResult(0,0,2,2)`, store empty, 0 refresher calls). 8 a gitleaks rc first read through a pipe, rerun alone:
**accepted** (this reader's own scans are item 2).

## 7. Texts for the landing (GO WITH FINDINGS)

`pr-title.txt`, `pr-body.md` (both commits; what the broker does and does not do; the limits D21, D24, D28 stated plainly
with the others; the host does not use it yet; nothing says anyone outside the engineering work decided anything),
`squash-subject.txt` (ends `(#PRNUM)`), `squash-body.txt` (ends `Co-Authored-By: Claude Opus 5.5
<noreply@anthropic.com>`), `landing.txt` (the B1850 form: main moved, `pr_retrigger.sh --check` against 61b17ec0,
`pr_checks_wait.sh --min-checks 8`, CodeQL analyses on `refs/pull/N/head` at the head's sha FIRST then alerts 0, the
merge's rules job `Ran 60` and `floor 60`, PR legs 973, head-pinned squash, after-merge reads with tree e1489d23), and
`FOR-RECORDS.md` (with the seat's open text point at `TokenBrokerOptions.cs:14`). Each exported through the workflow's own
`neutral_export` (cut by program from the merged `ci.yml` from line 120; identical at e9095598) as the message of a
commit object in a scratch repository and scanned with `--no-banner --redact --ignore-gitleaks-allow --exit-code 1`:
title, title + body, body, the squash message with a number, squash body, squash subject, landing.txt, FOR-RECORDS.md:
export rc 0, message stored whole, scan rc 0, `no leaks found`, 8 of 8; control (the squash message plus a planted token
built at run time) rc 1, `leaks found: 2`. `words.py` over the title, squash subject, squash body without its attribution
line and the body without its footer: `WORDS: clean (4 files)`; the squash body whole: `WORDS: clean (1 files)`. All
ASCII except the body's footer line. The merge numbers in the texts (973, 329, Ran 60) are this reader's measurements.

## NOT RUN / NOT TESTED

The Windows leg of any probe (the hosted Windows leg ran the lane's 74). C# CodeQL (cannot extract on this arm64
machine; the pull request's csharp analysis is the only C# proof: landing step 3). The second reader's scope (races by held
fakes, its 13 adversarial facts, mStaleWaiter, mSubjAnswer, mRace, mLate, mIdleAfter, mGrowNoClear, mLateKeep) was not
re-run here. The real WP1.4 refresher (none exists). Two records of one device at restore; a second process over one
partition. A whole-solution run after the mutants (the source was proved equal to the head instead). `repo_rules.py`
with a real supplied-source folder (never, by rule).
