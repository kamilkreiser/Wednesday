GATE B1943: GO WITH FINDINGS @ 93ea278 on main 0c3900b

Gate G1 (security surface: the device-token holder; and round 1's binding rule), round 2 of 2 of lane F1, reader
B1943, on Opus 5.5. Commission `2026-11-23_B1943_GATE_COMMISSION.md` read whole. Read whole as well: gate B1938's
VERDICT.md; kit B1940 (lines 1 to 211, two pages; its Stamp S4 holds Q1 to Q3 in words, the coordinator's; Q1 scoped
to T14 and probes A, C, D on purpose); the drafter's report; the seat's STATUS (ends `READY B1940: 93ea278e...`; its
two DEVIATIONS, a no-op `cd` subshell and one rc read through a pipe then repeated alone, change nothing measured
here). Kit B1935 parts (a) to (c) as gate B1938 quoted them. Head `93ea278eecb7c42378bd01f6bcabdc42eda3863e` on
`b1935/f1-sign-in-and-token-follow-ups`: one fast-forward on round 1's `c15e13f5`, which sits on `c480a0c8`. Measured
2026-11-23 02:19 to 02:40 AEDT in my own clones under `fleet/state/s312/g1943/`: `clone` (detached at the head),
`red` (`c15e13f5` plus `3-cells-red.diff`, then `4-fix.diff`), `merge` (main `0c3900b7` with the merged tree read
in), each by the kit's `clone.py ... draft` (push URL `invalid://no-push`, no identity). Origin by `gh api -X GET`
under the project GH_CONFIG_DIR at 02:31:58: main `0c3900b7`; the branch `93ea278e`; `b1940` refs 0; open pull
requests 0; from this branch, any state, 0. No write to the project, GitHub or Jira; no push, no pull request; no
`cd`; nothing deleted (probe files and scanner controls moved to `g1943/_quarantine/`).

**BLUF.** Round 2 does what round 1's verdict asked, and each of gate B1938's four findings is CLOSED or NAMED at the
head, measured: the late same-object answer is kept (T14 red first at `c15e13f5`, and B1938's own G1 form 500 of 500
kept), the `Invalidate` race no longer serves an all-zero token in my race probes (0 at the head, 6 and 4 with the
re-check removed, 7 and 2970 at `c15e13f5`), one object for two registrations is named, and the wording is "does not
check". Parts (a) to (c) are byte for byte round 1's. The lock the late clean-up now takes nests with nothing and
blocks an issuer's completing thread only for one of the holder's short sections; 600 runs of everything at once
ended within their bounds. Everything the commission asked to run is green, and the merge with main `0c3900b7` is
clean (1759 / 0, as predicted). **One Minor shape is open and not named, and it is not this lane's regression:** one
token object answered to two calls for ONE id across a `Remove`, which clears what the id holds again (FOUND 1). It
makes the rewritten late-answer sentence false if "registration" is read as the id. I judge it a README line for a
later lane, not a third build round: it needs an issuer that answers one object twice, the family the README
already names, and it is the same at `c15e13f5`. If the coordinator reads the lane's property strictly ("every other
way ... is refused or named"), this is the one item that fails it.

## ROUND 1's FINDINGS, AT THE HEAD

1. **B1938 FOUND 1, the held object answered after the bound: CLOSED.** `DisposeLate(Entry entry, ...)`
   (`CloudDeviceTokenHolder.cs:230`) takes `entry.Sync` (`:236`) and disposes only `if (!ReferenceEquals(done.Result,
   entry.Held))` (`:238` to `:241`); both call sites pass the entry (`:275`, `:282`). T14 (`CloudDeviceTokenHolderTests.cs:447`)
   is red at `c15e13f5` by its own assertion (`T14: the late answer's clean-up disposed the held token`, `:478`) and
   green at the head; `mLateDisposesHeld` reddens T14 only. Beyond the cell, probe L1 in B1938 G1's own form (the late
   answer completed on the test thread, `RunContinuationsAsynchronously`), 500 runs: head `disposed False | third
   served bytes 1 = 500`; `c15e13f5` `disposed True | third served len 27 all zero = 500`. The two-calls variant
   (H10 forward) is closed by the same line: probe R2's head rows serve X or the held bytes, never zero.
2. **B1938 FOUND 2, the race with `Invalidate`: CLOSED.** `Finish` re-checks `answer.IsDisposed` under `entry.Sync`
   after the same-object check (`:318` to `:324`). My probe R1 (the G4 shape, 3000 runs, a barrier and a random spin
   of 0 to 399): head `served all-zero 0, served the held bytes 2829, refused 171`; with `mNoDisposedRecheck`
   applied, `6 / 2872 / 122`; at `c15e13f5`, `7 / 2815 / 178`. My second race R2 (the late clean-up of call 2 and the
   in-time answer of call 3 both one new object X, 3000 runs): head `served the held bytes = 30; served X = 2970`, no
   zero; with the re-check removed `zero | next all zero = 4`; at `c15e13f5` 2970 runs end serving zeros (202 at
   once, 2768 on the next call). So the re-check is what closes both windows, and the probes fire without it. Counts
   of races on one machine, never rates. `mNoDisposedRecheck` survives every cell (348 / 0): the named survivor.
3. **B1938 FOUND 3, one object for two registrations: NAMED.** `README.md:146` to `:149` ("an issuer that answers one
   token object for two registrations has it held by both, so the holder's own `Remove`, `Invalidate`, renewal or
   clean-up of a late answer for one clears the bytes the other holds"), true by `:217`, `:159`, `:334`, `:240`. Not
   refused, as kit B1940 Q2 = a says. Its sibling across a `Remove` is NOT covered: FOUND 1 below.
4. **B1938 FOUND 4, "cannot tell": CLOSED.** `README.md:146`: "a copy carries the registration it came from, and the
   holder does not check that", true by `CloudDeviceToken.cs:33` to `:37` (`Origin`, `Generation`) and `:309` (the only
   compare is with `entry.Held`).

## FOUND (this gate)

1. **Minor, not named, the same at `c15e13f5`: one token object answered to two calls for ONE id across a `Remove`.**
   `Remove(id)` retires the entry (`:177`, `:211` to `:224`: `Held = null`, `Removed = true`); the next `GetAsync(id)`
   makes a NEW entry (`:71` to `:75`) whose call can be answered with object X. If the OLD entry's call then answers
   X too, X is disposed: late, by `DisposeLate`, which compares with the OLD entry's `Held` (null, `:238`); in time, by
   `Finish`'s removed path (`:328` to `:331`). The id then serves X's cleared bytes until a renewal succeeds or X's
   lifetime passes. MEASURED (macOS arm64, head and `c15e13f5` alike): H15a `at the bound bytes1; removed True; new
   registration served bytes 5; X disposed by the old entry's late answer True; the new registration then served len
   27 all zero; calls 3`; H15b `removed True; the old waiter refused NotFound; new registration served bytes 5; X
   disposed by the old entry's answer True; the new registration then served len 27 all zero; calls 3`. Against the
   README: `:104` to `:106` ("an answer that arrives later is disposed, under the registration's lock, unless it is
   the very token object the registration holds at that moment: that object is kept as it is") is false in H15a if
   "registration" is the id; the Remove bullet (`:115` to `:116`, "an answer that arrives later is disposed") is true;
   the Limits line names "two registrations", which one id across a `Remove` is not plainly. The seat met this shape
   and disclosed it as H15 (STATUS, DERIVED, "for the gate"). Why not a NO GO: it needs an issuer that answers one
   object to two calls (H3's family, already named as misbehaviour the holder does not check), it is not changed by
   this lane, and the host does not use the library (`README.md:150`). Fix sketch (DERIVED, not built): one Limits
   clause, "or to two calls for one id across a `Remove`", and "registration" read as the id in `:105`; no code.
2. **Info: T14's comment overstates its wait.** `CloudDeviceTokenHolderTests.cs:474` to `:475` say the clean-up "has
   run when this task ends", and `:477` waits for `issuer.Issued.Count == 2`; but `FakeIssuer.RunAsync` adds to
   `Issued` before its task completes (`FakeIssuer.cs:155` to `:164`), so that wait does not prove the clean-up ran.
   The red at `c15e13f5` rests on the continuation running inline on the completing thread (`ExecuteSynchronously`,
   `:250`): red 1 of 1 here, 20000 of 20000 by the drafter (RELAYED). At the head the cell cannot read red for timing
   (DERIVED: a later clean-up also keeps the held object). For the next cell author: wait on the object's state.
3. **Info: a late answer that is a caller's copy clears that copy** (probe L2, head and `c15e13f5`: `the caller's copy
   disposed by the late clean-up True; the holder then served bytes 1; calls 3`). As the README says (a late answer
   that is not the held object is disposed); that caller's `AsSpan` then throws (`CloudDeviceToken.cs:48`), never
   hands out cleared bytes. No change needed.

## THE ATTACKS THE COMMISSION NAMED (every shape: closed, named limit, or open)

- **In time, the held object:** closed (`:309` to `:316`; T13; mutants c to e).
- **Late, the held object:** closed (`:238`; T14; L1).
- **After an `Invalidate`, sequential:** closed: the answer is disposed, refused at `:288` (and `:318`); kit B1935
  FACT 4 RELAYED. **Concurrent:** closed (`:318`; R1 head 0). **After an `Invalidate` and late:** nothing held is
  cleared (the `Invalidate` dropped it, `:159` to `:160`); the drafter's probe D RELAYED; consistent with D1 below.
- **After the whole lifetime, in time and late:** the same-object compare does not look at age; in time it is refused
  and kept, and `GetAsync` throws the reason because the age passed the lifetime (`:121` to `:124`): never served;
  late it is kept (`:238`). Closed; drafter's probe D RELAYED, consistent with the code.
- **Two calls in flight (one timed out, one current) answering one object:** closed in both orders (R2; `:238` for
  forward, `:318` for the concurrent reverse).
- **A copy answered back:** in time, named (`README.md:145` to `:146`); late, disposed as any late answer (Info 3).
- **Two registrations:** named (`:146` to `:149`). **One id across a `Remove`:** OPEN, not named (FOUND 1).
- **Every other dispose site, read:** `:159` (`Invalidate`, only with a current copy), `:217` (`Retire`), `:240`
  (late), `:292` (an invalid answer outside the lock: the held object is never invalid by length or lifetime, and if
  it was already disposed it is cleared already), `:330` (an answer for a removed entry: FOUND 1's in-time form),
  `:334` (a renewal with a different object: the old held one). No other path disposes a token because of an
  issuer's answer.
- **Deadlock or inversion of D1's lock against `_sync`:** none. No path holds `_sync` and an entry's lock together:
  `GetAsync` `:68` to `:78` then `:82`; `Invalidate` `:144` to `:148` then `:155`; `Remove` `:174` to `:181` then
  `Retire` `:214`; `Dispose` `:191` to `:201` then `:214`. The continuation takes the entry's lock alone and calls only
  `CloudDeviceToken.Dispose` (`CloudDeviceToken.cs:60` to `:64`: `ZeroMemory` and a flag). Nothing completes a task
  under an entry's lock (`Finish` `:342`, `Retire` `:223`, after the lock; `Flight.Done` runs its continuations
  asynchronously, `:350`). **Blocking the issuer's completing thread:** yes, by design of `ExecuteSynchronously`
  (`:250`), for at most one of the holder's sections, which (as before this lane) call the handed-in `TimeProvider`
  (`:89`, `:121`, `:337`). MEASURED, probe D1: 600 runs of a late answer (the held object or a new one), the next
  renewal (sometimes the same object), two callers and an `Invalidate`, released together: `every task ended within
  its bound; all-zero 0, served 1605, refused 195` at the head (3 all-zero with the re-check removed, 29 at
  `c15e13f5`). DERIVED, unchanged: an answer completing at the very instant of the bound fails the filter at `:272`
  and is reported `TokenUnavailable` (and disposed unless held).
- **Parts (a) to (c), byte for byte:** `diff c15e13f5 93ea278e` names three files, none under SignIn (numstat
  23/6, 16/9, 41/1); `mAuditOneTry` SignIn `62 / 1` (B08); `mEmptyTaken` `62 / 4` (B10, B09 `D`, `N`, `B`). Hold.

## THE README, SENTENCE BY SENTENCE (the round-2 lines, at the head)

- `:103` to `:106` "an answer that arrives later is disposed, under the registration's lock, unless it is the very
  token object the registration holds at that moment: that object is kept as it is": true per entry (`:230` to
  `:243`); false across a `Remove` if "registration" is the id (FOUND 1).
- `:108` to `:109` "not already disposed (checked when it arrives and again under the registration's lock just before
  it would be held)": true (`:288`; `:318` under `:302`).
- `:109` to `:110` the length and lifetime rule, "else `TokenAnswerRefused`, and it is disposed": true (`:289` to
  `:292`; the re-check refuses an answer already disposed).
- `:110` to `:112` "An answer within the bound that is the very token object already held is `TokenAnswerRefused`
  too, and that object is kept as it is (not disposed): the renewal has failed, so the rule below applies": true
  (`:309` to `:316`; `:121` to `:124`).
- `:143` "compares an answer with that registration's own held token only": true (`:238`, `:309`).
- `:144` to `:146` the kept-and-changed issuer token and the copy answered back, "does not check that": true (as
  B1938 measured; `CloudDeviceToken.cs:33` to `:37`).
- `:146` to `:149` one object for two registrations, cleared by the holder's own `Remove`, `Invalidate`, renewal or
  late clean-up for one; "hands out such cleared bytes until a renewal succeeds or the token's whole lifetime has
  passed": true (`:217`, `:159`, `:334`, `:240`; `:89`, `:121`), and FOUND 1's shape behaves the same, unnamed.

## TESTED (MEASURED, macOS arm64; every dotnet job and test executable through the kit's `heavy.py` unchanged, one at
a time, the wave lock; lock waits 0 every job; load1 2.65 to 6.57)

- Tools: the eleven files of kit B1940's THE TOOLS copied from `d1940/gate`, sha256 11 of 11 equal to its table.
- The commit is the two patches: in `red` at `c15e13f5`, `3-cells-red.diff` applied, then `git diff --stat
  93ea278e -- tests` empty; then `4-fix.diff`, then `git diff --quiet 93ea278e` rc 0 (porcelain the three `M` rows).
  Both stored messages equal their kits' files (`commit-message-2.txt`, 394 bytes; round 1's `commit-message.txt`,
  447 bytes). `diff --name-status c480a0c8 93ea278e`: the seven `M` rows; `c15e13f5`: three.
- RED FIRST at `c15e13f5` (cells alone; locked restore rc 0; build `0 Warning(s)` `0 Error(s)`): Universal Print
  `Total: 348, Errors: 0, Failed: 1`, the one `[FAIL]` T14, `T14: the late answer's clean-up disposed the held token`,
  stack `CloudDeviceTokenHolderTests.cs(478,0)`.
- GREEN at the head (`clone`): locked restore rc 0; build 0/0; whole solution `total: 1669`, `failed: 0`,
  `succeeded: 1665`, `skipped: 4` (`Test run summary: Passed!`); Universal Print `Total: 348, Errors: 0, Failed: 0`;
  SignIn `Total: 62, Errors: 0, Failed: 0`.
- Mutants (`mutants_f1r2.py` unchanged, driven by `g1943/scratch/mutants_drive.py`: apply, build 0/0, the library's
  executable whole, undo `equal True`, `git diff --quiet HEAD` rc 0, then a REBUILD 0/0 before anything else ran):
  `mAuditOneTry` SignIn 62 / 1 (B08); `mEmptyTaken` 62 / 4 (B10, B09 `D`, `N`, `B`); `mSameObjectHeld`,
  `mSameObjectDisposed`, `mSameObjectAccepted` Universal Print 348 / 1 each (T13); `mLateDisposesHeld` 348 / 1 (T14);
  `mNoDisposedRecheck` 348 / 0 (the named survivor). Each exactly its cells. The sha256 before and after each apply
  equal the seat's table.
- Surface: `surface_f1.py clone c15e13f5...` and `... c480a0c8...` each `SURFACE: equal (3 folders)` (SignIn 46 lines
  / 13 files, Registration 48 / 12, Secrets 74 / 19); `--control` against each `CONTROL FIRED: 3 of 3`.
- Probes: scratch class `ZG1943UpProbes` (R1, R2, H15a, H15b, L1, L2, D1; each reports by `Assert.Fail("PROBE ...")`;
  run with `-class`, a probe selector, never a cell run), source `g1943/scratch/ZG1943UpProbes.cs`, in no patch. Built
  and run at the head, at the head under `mNoDisposedRecheck` (then undone `equal True`), and at `c15e13f5`; then
  moved out (`_quarantine/probe-head/`, `probe-red/`); `clone` porcelain 0, then a rebuild 0/0 and Universal Print
  `Total: 348, Errors: 0, Failed: 0` again (the probe class gone from the binary). Every number above is from those three runs. The head was run once before as well, with H15a
  mis-shaped (an extra call took the issuer's third answer), so H15a was rewritten; that run's other rows: R1 0
  all-zero (2863 held, 137 refused), R2 0 (9 / 2991), D1 0 (1567 / 233), L1, L2 and H15b as above.
- Files: the seven lane files at the head, each printable ASCII with no tab, 0 CR, last byte `0a` (control: a planted
  U+200B line counts 1). `repo_rules.py` (no `--source-documents`) on the head `RULES: clean (530 files)`.
- Merge with main `0c3900b7` (parent `39f57d6a`, parent `c480a0c8`): merge base `c480a0c8`; main changed 29 paths
  since it, none of the lane's seven and none under SignIn or UniversalPrint (control: the lane's own 7 in those
  folders). `merge-tree --write-tree 0c3900b7 93ea278e` rc 0, tree `b06d8049f745591ecd0ddbea7f6e8403cf9250bf`, 551
  files; against main exactly the seven `M` rows; the lane files equal the head's. In `merge` (`read-tree -m -u HEAD
  b06d8049`, `diff --quiet b06d8049` rc 0): locked restore rc 0; build 0/0; `total: 1759`, `failed: 0`, `succeeded:
  1755`, `skipped: 4` (PREDICTED 1752 + 7 = 1759: HELD); `RULES: clean (551 files)`; `unittest` `Ran 111 tests`, `OK`.
- HOSTED head: `hosted2.py 93ea278e... --total 1669 --rules 530 --skipped-linux 4 --skipped-windows 21 --unit 111
  --floor 111 --hardened-scan`: run 45036798637, four jobs success, attempt 1; linux 1669 x2 / 1665 / 4, GUARD 10;
  windows 1669 x2 / 1648 / 21, GUARD 11; rules 530, floor 111; every hardened secret-scan row OK; `HOSTED
  93ea278eecb7c42378bd01f6bcabdc42eda3863e: PASS`. HOSTED main `0c3900b7` (`--total 1752 --rules 551`): run
  45035239506, `PASS`, Analyze (actions), (csharp), (python) success.
- WORDS: `--control` `CONTROL FIRED: 13 of 13`; over the lane's 221 added lines (`c480a0c8..93ea278e`) and both stored
  messages: every class 0, `WORDS: clean (3 files)`.
- GITLEAKS 8.30.1: control FIRST (a token shape built by a program from two halves and 36 random characters, never
  printed) rc 1 `leaks found: 1`, moved to `_quarantine/gl-control-commit`; the added lines and the two messages as
  neutral `1.txt` to `3.txt`: rc 0, `no leaks found`.

## NOT TESTED

- Nothing on Linux or Windows locally (the hosted legs are those runs); the probes there: UNMEASURED.
- No publish, release guard, `run_step.py` neutral scan or locked restore with `--force` locally (the head's hosted
  run and the seat's chain cover them, RELAYED from STATUS); the seat's 10-run loop not repeated.
- The drafter's probes A to G not re-run (RELAYED); R1, R2, L1, L2 and D1 cover A, B, C and G's shapes.
- No CodeQL locally; the head's push run has no Analyze rows, so code scanning is read on a pull request.
- The hosted legs on the merged tree: not run (no pull request); windows `succeeded: 1738` is PREDICTED.

## LANDING (the coordinator's)

landing.txt (one squash of both commits, head-pinned, MAIN MOVES from `0c3900b7`), pr-title.txt, pr-body.md (both
rounds, round 1's premature ratification and its retraction), squash-subject.txt, squash-body.txt, FOR-RECORDS.md.
Who decides to land: the coordinator. FOUND 1 is for the backlog (FOR-RECORDS item 1); it is not a reason to hold
this landing, in this gate's reading.

## SCANS (of the texts of this folder, after the last edit; `g1943/scratch/texts_scan.py`)

- Sizes: `pr-title.txt` 184 bytes (183 characters); `squash-subject.txt` 218 bytes, 214 characters with `#28` in
  place of `#PRNUM` (under 256 with any two- or three-digit number); `squash-body.txt` 2019 bytes, 34 lines;
  `pr-body.md` 5130 bytes.
- `words.py` per file: `pr-title.txt`, `squash-subject.txt`, `squash-body.txt`: every class 0. `pr-body.md`: `product
  owner` 1 and `coordinator` 3 (the required who-decides lines), round numbers 9 (the required naming of both rounds
  and round 1's ratification), 4 non-ASCII bytes (the required robot line); every other class 0. The four texts not
  meant for the repository (landing, FOR-RECORDS, this file) carry B-numbers, seat and gate words by design.
- `build/squash_scan.py` (main `0c3900b7`'s, from the `merge` clone, whose `build/` and `.github/` equal main's: `diff
  --quiet` rc 0), subject with `#28`: control `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.
- gitleaks 8.30.1: a fresh firing control, then the texts of this folder as neutral `<n>.txt`: the last line below.
- gitleaks result (02:39): fresh control rc 1, `leaks found: 1` (moved to `g1943/_quarantine/gl-control-final`); the seven texts of this folder (this file before this line) as neutral `1.txt` to `7.txt`: rc 0, `no leaks found`.
