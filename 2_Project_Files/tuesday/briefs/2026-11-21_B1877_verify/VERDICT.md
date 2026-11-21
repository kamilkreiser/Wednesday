GATE B1877: GO WITH FINDINGS @ 610bb7d on main 5bb1418

Gate G1, round 2 of 2 (delta), whole-lane reader (successor of round-1 reader B1868). OXPd 2, WP1.2 in part, lane E:
the fix commit C1 `610bb7d2f1f3ded9a5616fcb00bcc6bef408e2f6` (one parent `523204dd`, no merge commit) on branch
`b1849/wp12-oxpd2-adapter`; main `5bb1418c107f61b286da9bb73795290f9c959e99`. Read and measured 2026-11-21, 23:15 to
23:30 AEDT (clocks by `date`), on Opus 5.5, in the reader's own clone (session scratchpad `b1877-clone`, made by the
kit's `clone.py ... draft`: push URL `invalid://no-push`, no identity) and a detached worktree of it holding the merged
tree (`b1877-merged`). Origin read by `gh api -X GET` under the project GH_CONFIG_DIR at 23:23:45: branch = 610bb7d2,
main = 5bb1418c, open pull requests 0, `compare main...610bb7d2` ahead 2, behind 1, 35 files, merge base 8ae5e08c;
open code-scanning alerts on main 0. Tools: the ten files of `fleet/state/s306/d1873/gate/` copied and ten of ten equal
to the kit's THE TOOLS by sha256; `words.py --control` `CONTROL FIRED: 13 of 13`. Every heavy job went through the
kit's `heavy.py` (sha256 `31adedc8...`): load1 first, the wave lock `<project>/.tools/wave1-heavy.lock.d` by `mkdir`
with `owner.txt`, released by a move into `/private/tmp/b1877-gate/_quarantine/locks/` (five jobs; waits 0, 0, 1, 9,
0 polls behind reader B1878: waits, not findings; `evidence/gate.log`); restores `--locked-mode -p:NuGetAudit=false`
with `CI=true`. `repo_rules.py` never got `--source-documents`; no key folder was hashed, listed or opened; synthetic
values only, none printed; no socket, no request to a printer or host. No write in the OXPd_2 project but the shared
lock; no git write outside the scratch clone; no GitHub write, no Jira, no mail. Scratch and logs:
`/private/tmp/b1877-gate/`; probe source, mutant program, outputs and hosted readings in `evidence/`.

**BLUF.** The round-1 Major is gone and nothing new is above Minor. My deterministic F1 probe G17 now reads 1 endpoint
call and 1 distinct access value after a start, and 1 endpoint call after the prime for a request arriving during a
renewal (round 1: 2 and 2); my unforced G11 race no longer shows a round with 2 calls (max 1, was 2). My 17 probes read
as the kit predicted (G05 `BodyFailed` for all four bodies; G12's grant changed after construction now sends the
ORIGINAL value; G13 unchanged: the late grant is still dropped, records). Two new probes of mine (G18, G19) on the
fix's own mechanisms hold. My 16 mutants re-made at the head: 16 of 16 red, every one on a builder cell, the three that
reddened only my probes at round 1 now red on the cells the kit named. Scope is the seven files; suite 1248 failed 0;
hosted PASS. **The merge holds:** `merge-tree` clean, tree `014d6221...` (the seat's claim), and that tree builds and
runs **1392, failed 0, skipped 4**, rules 443 files, `Ran 60`. Deviations 1 to 4: records or accepted, none touches the
code. Tuesday's item 4: I agree, a records-level limit. Findings: two Minor (text, records), one records. Landing texts
written.

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor (text) | **The README's Limits do not carry D30's named limits (a) to (c), nor B1868 F4 / B1869 F6 to F9.** The kit's H35 reads "NAMED LIMITS (D30, README)"; at 610bb7d2 only (d), the lookup's timing, is in the README (line 46); `StoreRefreshValue` during a flight, a lease sent once after `Forget`, the vault call under a serial's lock, the dropped late grant, the 401 after a failed refresh, the wrong-length record and `TryGet`'s fresh-copy need are named nowhere in the repository. No README line is false (each changed sentence read against the code, below). | The pull request body states all of them plainly (written here); a records pass adds them to the README Limits (`FOR-RECORDS.md` items 1 to 11). |
| F2 | Minor (records) | **D30 (a) reaches a waiter too.** Probe G18 (a), MEASURED: A's refresh held, B waiting on it, then `Forget` and `StoreRefreshValue(new)`, then the endpoint answers: A ends `NoRefreshValue` (generation moved: nothing stored, correct) and B, the waiter, ends `NoRefreshValue` as well, although the vault already holds the new refresh value; the next request C succeeds with one more endpoint call. This is D21 doing what it says (a waiter uses the result of the flight it waited for) meeting D30 (a); no value stored after `Forget`, nothing leaked. G18 (b): `Forget` whose vault delete throws during a refresh: `Forget` reports `VaultFailed`, the refresh stores nothing and ends `NoRefreshValue`, the old refresh value stays in the vault (consistent with the exception). | Records: one clause on D30 (a) ("and a request that waited on that refresh"); written into the pull request body. |
| F3 | Records | B1868 F4 unchanged, as the kit says: G13 at the head reads 2 endpoint calls in flight and the late rotated value not stored. | NOT DECIDED item 3 of the kit; stated in the pull request body. |

No Blocker, no Major. Round-1 findings: F1 closed (G17, G10, G11); F2 closed by `BodyFailed` (G05, B06); F3 closed
(copy; G12 sends the original; mGrantNoCheck red on T15); F4 records (F3 above); F5 closed (mOpNoMethod red on B07,
mFailReuseOff red on T12 hang and T13 x2); F6 closed in text (README line 44-47 and the class summary say "the same
comparison" and name the lookup's timing).

## 1. What the kit's FOR TUESDAY assigns to B1868, re-run at 610bb7d2

**G17, deterministic (both shapes)** (`evidence/probe-results.txt`): (a) lazy, B arrives during A's held first refresh:
`endpoint calls 1, device calls 2, distinct access values sent 1` (expected 1 and 1; round 1: 2, 2, 2). (b) primed (1
call), A's renewal after a 401 held, C arrives: `endpoint calls after the prime 1` (expected 1; round 1: 2).

**The 17 probes** (`evidence/GateProbeTests.cs`, 19 tests in the lane's test project in my clone only, never committed;
the round-1 file with the result path, G12's last measurement and two new probes changed by `evidence/edit_probe.py`):
lane project `total: 76` (57 cells + 19 probes), `failed: 0`. Against round 1: G01 23 Unauthorized, 0 reads, control 4
of 4; G02 Unavailable x2, 31-byte hash Unauthorized; G03 10 NotHandled, 11 media refused, 0 reads; G04 bounds as round
1 (200 Answered, 201 TooLarge read 201, ... 1 MiB+1 TooLarge read 1048577); **G05 now `result BodyFailed` for
IOException, OperationCanceledException, TimeoutException, ObjectDisposedException; wrong credential Unauthorized with
0 reads; sink 0**; G06 refusal kinds as round 1; G07 guard edges as round 1; G08 SinkFailed 4, AnswerInvalid 4; G09
800 / 800, 0 reads under a wrong credential, rotation old fails new passes; G10 200 x 16: rounds with a second refresh
0, max in flight 1, non-200 0; **G11 200 x 8: 0 of 1600 before their rotated value was written, max endpoint calls in a
round 1 (round 1: 2)**; **G12 six bad values ArgumentException / holder RefreshFailed, messages hold no value 6 of 6; a
grant changed after construction: "header holds a newline False, header is the ORIGINAL value True" (round 1: throws
FormatException)**; G13 RefreshFailed at the bound, the next send OK with 2 in flight, late rotated value not stored
(F3); G14 caller cancel OCE and the waiter refreshes (2 calls, the abandoned-flight rule), VaultFailed x2,
InvalidArgument x3; G15 NeedsRepair (device 1, endpoint 2), statuses passed through; G16 BodyTimedOut at 3 s, not at
2.999 s.

**New probes of this reader:** G18 (F2 above). **G19:** 200 rounds x (Issue, Forget) on a FRESH instance whose first
check's vault read has taken its snapshot and is released beside the mover: old accepted after Issue returned 0, new
refused 0, accepted after Forget returned 0, record left after Forget 0; free race 500 x (a device checking the old
credential in a loop beside `Issue`): old accepted by a check started after `Issue` returned 0. (B1878 owns G25 to G28
in depth.)

**My 16 mutants, re-made at the head** (`evidence/mutants.py`, `evidence/mutants.out`; one heavy job; each applied to
exactly one occurrence (a `check` pass printed 16 of 16 standing once), the lane's project built and run, the original
bytes restored and proved by byte equality and `git diff --quiet` rc 0). Texts unchanged but two: mForgetKeepsAccess
re-made on the new `Forget` (the `ClearAccess()` beside `Generation++` removed), mRotateNoStore matched without its
moved indentation.

| Mutant | RED at 610bb7d2 (by assertion) | Round 1 |
|---|---|---|
| mMediaParam | B03, G03 | B03, G03 |
| mOpNoMethod | **B07**, G03 | G03 only |
| mNoRepairMark | T03 | T03 |
| mForgetKeepsAccess (re-made) | T11 | T11 |
| mUsbClosedNoReset | U01, U02, U03, G07 | same |
| mCapOff | U03 | U03 |
| mRetryHeaders | T02 | T02 |
| mVaultAsStranger | A05, G02, B08, B09 | A05, G02 |
| mSignoutAnswer | S03 | S03 |
| mRefreshNoBound | T05, G13, T12 hang | T05, G13 |
| mGrantNoCheck | **T15**, G12 | G12 only |
| mRotateNoStore | T07 x2, G11, T15 | T07 x2, G11 |
| mSchemeCase | A02, G01 | A02, G01 |
| mKeyNoSerial | U02 | U02 |
| mReadNotCancelled | B05 | B05 |
| mFailReuseOff | **T12 hang, T13 first start, T13 renewal** | NONE (survived) |

16 of 16 red, each on at least one builder cell; build errors 0 in every run; the kit's expectations hold exactly.
After the last revert `git status --porcelain` 0 lines; the probe file moved to
`/private/tmp/b1877-gate/_quarantine/probe-*/`.

## 2. Scope (C1 inside the lane's two folders, the seven files only)

`git diff --name-status 523204dd 610bb7d2`: M `Callbacks/CallbackCredentials.cs` (+39 -7), M
`Callbacks/Oxpd2CallbackHandler.cs` (+11), M `Callbacks/Oxpd2CallbackOutcome.cs` (+3), M `Device/DeviceTokenHolder.cs`
(+54 -40), M `Device/SolutionTokenGrant.cs` (+11 -5), M `README.md` (+20 -9), A
`tests/Datasec.Suite.Adapters.Oxpd2.Tests/RaceCellTests.cs` (+709); no D, no R; no other test file. C1's tree
`f3375a65...` = the drafter's prototype tree (the kit's diffs applied byte for byte). `git diff --quiet 523204dd
610bb7d2 -- Datasec.Suite.slnx Directory.Packages.props .github build '*packages.lock.json' '*.csproj'
src/Datasec.Suite.Adapters.Oxpd2/Generated contracts tests/Datasec.Suite.Contracts.Tests global.json
Directory.Build.props NuGet.config` rc 0 (control over README.md rc 1). Added lines 847: outside printable ASCII 0
(control: a planted U+200B line counts 1); 64-hex literals 0; 43-character base64url runs 0. The `=>` census over the
21 product files: 31 at 523204dd, 31 at 610bb7d2 (control 2 of 2). `RaceCellTests.cs`: 14 test methods by the
indented pattern, column-1 0; no real-time wait but the cells' 10 s guard (`WaitFor` and `Guard`; the one `Task.Delay`
is the endpoint's infinite hang honouring its token). `words.py` over the 847 added lines and the commit message:
`WORDS: clean (2 files)`. gitleaks 8.30.1 (`--no-banner --redact --ignore-gitleaks-allow --exit-code 1`): control
first (a token built by program from two halves) rc 1; the seven files at the head plus the added lines under neutral
names rc 0; the commit message alone rc 0; the clone rc 0.

## 3. The README against the code (each changed sentence)

- `BodyFailed` appended as outcome 14: the enum has 14 members, `BodyFailed` last (`Oxpd2CallbackOutcome.cs:46`);
  the outcomes list ends `SinkFailed, BodyFailed`; the read step names it. True (G05, B06).
- The reuse sentence ("uses that refresh's result, its access value or its failure; it runs a refresh of its own
  only when no refresh completed after its wait began"): `Flights` incremented only on completion
  (`DeviceTokenHolder.cs:235` in `Fail`, `:390` on success), the reuse test at `:280` to `:291`. True (G17, T12, T13).
  An abandoned flight (the caller's cancellation) is not counted and its waiters refresh for themselves (G14): the
  README's "completed" covers it.
- The lookup's timing (README lines 44 to 47, class summary lines 12 to 14): true (`StoredHash` reads the vault for
  an uncached serial on every call).
- The two new Part 1 bullets: the grant copies both values and refuses the six shapes with a fixed message (G12,
  T15); `Forget` during a refresh stores nothing and ends `NoRefreshValue` (T14, G18). True.
- `Issue`/`Forget` "take effect for every check that starts after it returns": true by the generation
  (`CallbackCredentials.cs:64`, `:98`, `:175`, `:187`) and the vault-first `Forget` (`:90`); G19 0 violations.
- The exceptions paragraph ("throws nothing but `ArgumentNullException` and the caller's own cancellation"): every
  `throw` in the handler is `ArgumentNullException.ThrowIfNull` (`:92`, `:93`, `:214`, constructor `:48` to `:50`),
  `cancellationToken.ThrowIfCancellationRequested()` (`:94`) or a `throw;` under a
  `when (cancellationToken.IsCancellationRequested)` filter (`:143`, `:191`); the credential, the read and the sink
  are each wrapped in a general catch to a typed outcome. True (G05, G08, B06). The removed Limits line (a throwing
  stream passes out) is correctly gone.
- No README line of the diff is wider than 118 characters (6 wider lines, all round-1 lines; 0 among the added).

## 4. Suite and hosted

- Head 610bb7d2 through the lock (`evidence/head-suite-summary.txt`): locked restore rc 0, no fetch line, porcelain 0
  after; build `0 Warning(s)`, `0 Error(s)`; whole suite `total: 1248`, `failed: 0`, `succeeded: 1244`, `skipped: 4`
  (the four Windows key-ring tests of `Datasec.Suite.Secrets.Tests` by name); `Datasec.Suite.Contracts.Tests.dll`
  passed. `repo_rules.py <clone>` (no option): `RULES: clean (403 files)`; `build/tests` `Ran 60 tests`, OK.
- Hosted run `44902425592` of 610bb7d2 read by GET (`hosted.py`, sha256 `e73339f3...`, the same as
  `fleet/state/s304/d1835/gate/hosted.py`) with `--total 1248 --rules 403 --skipped-linux 4 --skipped-windows 19
  --unit 60 --floor 60`: **`HOSTED 610bb7d2f1f3ded9a5616fcb00bcc6bef408e2f6: PASS`** (four jobs success, attempt 1;
  linux and windows `total: 1248` twice each, failed 0, skipped 4 / 19, GUARD 10 / 11; rules `Ran 60`, floor 60,
  `RULES: clean (403 files)`; secret-scan both PLANTED-CONTROL lines, `objects of this commit not among them 0`, `no
  leaks found` x3; `evidence/hosted.out`). Control `--rules 402`: `FAIL 1`. Windows `skipped` lines naming a test
  outside `Datasec.Suite.Secrets.Tests`: 0. Main 5bb1418c by the same program with `--total 1335 --rules 410`: PASS,
  the three Analyze rows success (`evidence/hosted-main.out`).

## 5. THE MERGE (measured)

- `git merge-tree --write-tree 5bb1418c 610bb7d2` rc 0, clean, tree **`014d6221bb64796c13230e6c21a735558f4a65ba`** =
  the seat's claim; merge base 8ae5e08c. Against main: exactly the 35 paths of `8ae5e08c..610bb7d2` (program
  equality), the solution file gaining only the lane's one test line; against the head: exactly main's 42 paths;
  `git diff --quiet 610bb7d2 014d6221 -- src/Datasec.Suite.Adapters.Oxpd2 tests/Datasec.Suite.Adapters.Oxpd2.Tests` rc
  0. 443 files.
- That tree in a detached worktree (`read-tree -u --reset 014d6221`, index tree re-printed equal), through the lock:
  locked restore rc 0, no fetch line, lock files changed 0; build `0 Warning(s)`, `0 Error(s)`; **whole suite
  `total: 1392`, `failed: 0`, `succeeded: 1388`, `skipped: 4`** (the same four Windows tests by name;
  `evidence/merged-suite-summary.txt`). Measured, not added (it equals main 1335 + the lane's 57). Both workflow
  publishes rc 0, `release_guard.py` `GUARD: clean (10 files)` and `GUARD: clean (11 files)`; nothing in
  `src/Datasec.Suite.Server` references the adapter.
- `test ! -e <scratchpad>/1_Project_Definition` rc 0 first; `python3 -I build/repo_rules.py <merged>` WITHOUT
  `--source-documents`: `RULES-NOTE: R5 hash half NOT RUN`, **`RULES: clean (443 files)`**, rc 0.
  `python3 -I -B -m unittest discover -s build/tests`: **`Ran 60 tests`**, OK; `ci.yml` `FLOOR=60`.
- These are the numbers written into `landing.txt` for the pull request's merge ref (windows skipped 19 there is
  DERIVED: main and the head each read 19, the lane's tests skip nothing).

## 6. The seat's deviations 1 to 4

1. A `(cd ...)` inside a subshell in its Step-1 hash command: records only. A shell-discipline breach the seat named
   itself; it ran only `true` and changed nothing; the real check was the program's 10 of 10, and C1's tree equals the
   drafter's prototype tree, so nothing of the commit depends on it.
2. `repo_rules.py` first run before `git add` (402, untracked file not counted), then 403 after staging: accepted, no
   finding. I measured 403 at the head and the hosted rules job printed 403.
3. `3-mutants.txt` labels mFailNoReuse "5 lines" for a 4-line body: accepted (a kit text slip). My own mFailReuseOff
   removes the same four lines and is red on the same three cells (T12 hang, T13 x2): independent confirmation.
4. `compare main...<sha40>` behind 1, not 0: accepted. It is S4's answer applied (main moved, `merge-tree` clean, C1
   pushed alone); I measured the merge clean at the tree the seat printed.

## 7. Tuesday's item-4 ruling (`CallbackCredentials.StoredHash` leaves a read unzeroed)

Read at 610bb7d2: `:178-181` (a wrong-length read returns null and drops `stored`), `:187-190` (generation moved:
`stored` dropped, the cache answers), `:192-198` (another fill won: `stored` dropped, `filled` returned). **I agree it
is Minor or less (records).** Each dropped array is the SHA-256 digest of a 256-bit random credential: not the
credential, not invertible, and not usable to authenticate (Verify hashes what is presented, so presenting the digest
fails); the same digest is held in `_hashes` for the instance's life anyway, so an unzeroed duplicate until collection
adds no capability to someone who can read process memory. Round 1 had the same shape on the wrong-length path. Two
`ZeroMemory` lines and a cell in a later lane if wanted; named in the pull request body.

## 8. The landing texts (written: GO WITH FINDINGS)

In this folder: `pr-title.txt` (182 bytes), `pr-body.md` (both commits, what the adapter does, the limits stated
plainly: D30's five, Tuesday's item-4 limit, B1868 F4 and B1869 F6 to F9, and the host does not use it yet),
`squash-subject.txt` (ends `(#PRNUM)`), `squash-body.txt` (ends `Co-Authored-By: Claude Opus 5.5
<noreply@anthropic.com>`), `landing.txt` (the B1864 form: `pr_retrigger.sh --check` against 5bb1418c;
`pr_checks_wait.sh --min-checks 8` with the project GH_CONFIG_DIR in its environment; CodeQL analyses on
`refs/pull/N/head` at the head's sha FIRST, then open alerts 0; the pull_request job logs by GET with
`--allow-escape-sequences`; the merge's legs `total: 1392`, `RULES: clean (443 files)`, `Ran 60`, floor 60; head-pinned
squash `--match-head-commit 610bb7d2...`; after-merge reads with the merged totals and tree `014d6221`; MAIN MOVES
AGAIN with +57 tests and +33 files), `FOR-RECORDS.md`. `evidence/texts.py` (the B1864 program, paths and the two
branch commits changed) exported each text through the workflow's own `neutral_export` (cut from ci.yml at the head,
lines 120 to 128) as the commit message of a scratch repository and scanned it with the workflow's options: title,
title and body, body, squash message with a number and as written, squash body, the default squash shape over both
commit messages, landing.txt: each rc 0 `no leaks found`, message stored whole; the planted control rc 1, `leaks
found: 2` (`evidence/texts.out`). Word counts: the four repository texts 0 in every class but one host match in
squash-body.txt (the attribution line's address), non-ASCII 0; `words.py` over the four: `WORDS: clean (4 files)`;
landing.txt (Tuesday's form, not repository text) holds B-numbers, paths and the word gate by design. Word controls 16
of 16 fired. The pull request body carries no attribution line (the B1864 form; add one if Tuesday's rule wants it,
then scan again). **Landing happens only when reader B1878 is also GO or GO WITH FINDINGS.**

## NOT TESTED

- Windows and Linux locally (macOS arm64 only): the hosted legs ran the lane's cells, not my probes; the merged tree's
  hosted legs do not exist until the pull request opens.
- CodeQL csharp locally (cannot extract on arm64): the hosted analysis on the pull request is the only C# proof.
- Any device, simulator or real token endpoint; a real vault's timing under the entry lock (D30 (c)); the R5 hash
  half.
- The seat's twelve mutants were not re-run (I ran my own sixteen); B1878 owns G13, G14, G25 to G28, G08 and its free
  races in depth; the builder's 57 cells were read in part (the 14 new ones whole), not line by line.
