GATE B1938: NO GO @ c15e13f on main c480a0c

Gate G1 (security surfaces: the binding rule and the device-token holder), round 1 of 2, reader B1938, lane F1 only.
Kit B1935 (seat X37), ANSWER-1, STATUS read whole (it ends `READY B1935`). Q1 = a and Q2 = a by stamp S4: the
coordinator's calls as coordinator, not the product owner's. Head `c15e13f5fb89bc33b0f7c8ab9bcd1cc56d2b222d` on
`b1935/f1-sign-in-and-token-follow-ups`, ONE commit, parent `c480a0c8` (= main). Read and measured 2026-11-23 00:58 to
01:15 AEDT on Opus 5.5, in my own clones under `fleet/state/s312/g1938/`: `clone` (main, then the red cells, then the
fix, then lane F2's diff) and `head` (detached at the head), each by the kit's `clone.py ... draft` (push URL
`invalid://no-push`, no identity). Origin by `gh api -X GET` under the project GH_CONFIG_DIR at 01:01: main = c480a0c8;
the branch = c15e13f5; lane F2's branch = b74f0f0c; `compare c480a0c8...c15e13f5` ahead 1, behind 0, 7 files; newest
pull request 25 (closed, merged); no open one. No write to the project, GitHub or Jira; no push, no pull request; no
`cd`; nothing deleted (probe files and scanner controls moved to `g1938/_quarantine/`).

**BLUF.** Parts (a), (b) and (c) are right and proved: the audit fan-out, the empty identifier and the two README
Limits lines each hold, also outside the cells (below). Part (d), the same-object renewal, closes the shape it was
built for (T13, and fifty concurrent callers now get the held bytes where main disposed them), **but the lane's own
required property, "the token holder never disposes the token it holds because an issuer answered with that same
object, and never hands out cleared bytes for that reason", fails on two paths the drafter did not probe, and a third
path the property names ("every other way an issuer's answer can share an object with the holder is refused or named
in the README") is neither refused nor named.** Each is MEASURED on the head and hands out a 27-byte all-zero token
with no error. None is a regression (each is the same or worse at main), but one makes the commit's new README sentence
false, and each has a small fix inside the owned paths. Round 1 of 2: this goes back as a fix round (FOUND 1 to 3, and
FOUND 4's wording). Everything else measured here is green.

## FOUND

1. **Minor, the new README sentence is false in this shape: the held object answered AFTER the bound is disposed by
   the late-answer path, and the next failed renewal hands out its cleared bytes.** `RunFlightAsync` hands a timed-out
   call to `DisposeLate` (`CloudDeviceTokenHolder.cs:263` to `:268`), which disposes whatever the call later answers
   (`:227` to `:242`), outside `entry.Sync` and with no look at `entry.Held`. If that late answer IS the held object,
   the holder disposes its own held token. The held entry is untouched otherwise, so the next renewal that fails
   inside the lifetime serves `CopyOf(entry)` from the zeroed buffer (`:121` to `:122`, `:249` to `:250`). MEASURED
   (probe G1, `IssueTimeout` 2 s, lifetime 100 s): `second copy bytes 1 True; held disposed by the late answer True;
   third (issuer throws) served len 27 all zero True; calls 3`, the same at main. The Registration README now says
   "An answer that is the very token object already held is `TokenAnswerRefused` too, and that object is kept as it
   is (not disposed)" (`README.md:108` to `:109`), next to "an answer that arrives later is disposed" (`:103` to
   `:104`): for a late same-object answer the second wins and the first is false. Fix sketch (DERIVED, not built): in
   the late-answer path take `entry.Sync` and skip the dispose when `ReferenceEquals(late, entry.Held)`, or name the
   shape among the Limits; a limit or a cell of G1's shape either way.
2. **Minor, a race: a same-object answer and a concurrent `Invalidate` with a current copy.** The disposed check runs
   outside the entry's lock (`:278` to `:286`); `Finish` takes the lock and compares with `entry.Held` (`:300`). An
   `Invalidate(id, copy)` between the two disposes the held object and sets `Held = null` (`:155` to `:161`), so the
   compare fails and the disposed object is held as `Accepted` with a fresh age (`:317` to `:320`). MEASURED (probe
   G4, 3000 runs, the answer and the `Invalidate` released together by a barrier, a random spin of 0 to 399 before the
   `Invalidate`): head `served all-zero 14, served the held bytes 2719, refused 267 (TokenAnswerRefused 267)`; main
   `served all-zero 2973, served the held bytes 0, refused 27`. So the fix narrows it about 200-fold and does not close
   it; one run each, the counts are a race's and will vary. Fix sketch (DERIVED): check `answer.IsDisposed` again
   inside `Finish` under `entry.Sync`, beside the same-object check; the race then has no window.
3. **Minor, unchanged from main and not named: one issuer object answered to two registrations.** The same-object
   check compares with the entry's own held token only, so an issuer that answers one object for two ids has it held
   by both. Then the holder's own `Remove`, `Invalidate` or renewal of the first disposes what the second still serves.
   MEASURED: G2 `both answers held without refusal, calls 2; after Remove(id1): id2 served len 27 all zero True`; G3
   (the first renewed with a new token at 91 s) `calls 3; id2 (age 41 s) served len 27 all zero True`; the same at main.
   The new Limits line (`README.md:140` to `:142`) names an issuer that keeps and later clears its own answer, and a
   holder copy answered back; it does not name this, where the holder clears it itself. Fix sketch: name it in that
   line, or refuse an answer that another entry holds (a scan under `_sync`, DERIVED), or Q1's alternative c.
4. **Info (wording): "the holder cannot tell either"** (`README.md:142`). For the copy answered back, it can: the copy
   carries `Origin` and `Generation` (`CloudDeviceToken.cs`, internal), and the kit's own Q5 alternative is the one
   line that refuses it. "does not check" is what the code does. G6 re-measured the shape: `renewal served bytes 1
   True; original disposed True; after the caller disposed its copy: served all zero True calls 2` (as the drafter's Q2).

## THE ATTACKS THE COMMISSION NAMED

- **Q1 a, a cleared or disposed token by a path not probed:** an issuer that answers a held object after an
  `Invalidate`: sequential, refused by the disposed check (drafter's Q3, RELAYED); concurrent, FOUND 2. A concurrent
  renewal: one flight, so fifty callers get one call and the held bytes, the object not disposed (G5 head `calls 2;
  50 callers all the held bytes True; held disposed False`; main `... False; held disposed True`). A caller holding a
  copy: FOUND 4 / G6, the named limit. Beyond the list: the late answer (FOUND 1) and two registrations (FOUND 3).
- **`GetInvocationList()` per handler, order and cost:** order is subscription order, as the multicast call gave.
  The snapshot is taken at the raise: a handler that removes a later one and adds another during the raise does not
  change this raise (S2 head `order h1,h2,h3 ... second raise order h2,h4`; at main the first throw stopped the list:
  `order h1`, then `h2`). One arguments object for every handler (`True (4 seen)`); the sender is the actor. The same
  handler subscribed twice is called twice, and the recorder after it is reached (S3 head `thrower called 2 kit
  recorder 1 handler after 1`; main `1 / 0 / 0`). Cost: one array per raise, raised only on a binding refusal
  (DERIVED). Nothing a caller could rely on changes but the fix itself.
- **The empty identifier in ANY form `Guid.TryParse` accepts:** the check is on the parsed value (`SignInActor.cs:304`),
  and the only acquire is behind it (`:334`, called from `:329` only). MEASURED S1 on the head, each form asserted to
  parse to `Guid.Empty` first: `P`, `X`, `D` space-padded, `N` tab and line-feed padded, `B` space-padded each
  `LookupFailed acquires 0 calls 0 audits 0 store 0`; control (a real id in the `X` form) `SignedIn acquires 1`. At
  main every form was `SignedIn acquires 1 ... store 1`. The README's "in any form `Guid` reads" is true.

## THE README, SENTENCE BY SENTENCE (the added lines, against the head)

- SignIn `:21` to `:24` (the empty identifier, "nothing is acquired"): true (B09, B10, S1).
- SignIn `:33` to `:34` and `:68` ("raised once to each handler, each in its own try"; "the handlers after it still
  run"): true (B08, S2, S3). The doc comment `:91` to `:94` says the same.
- SignIn `:87` to `:90` (`MaxTapAge` plus four `StepTimeout`): true by the code: the age is read once in `TurnAsync`;
  then the lookup (`:277`), the switch's printer sign-out (`EndSessionAsync` -> `DeviceSignOutAsync`), the acquire
  (`:334`) and `CompleteSignInAsync` are each one bounded `StepAsync`, and the broker's calls are synchronous. "about
  125 seconds" is 5 + 4 x 30 (DERIVED); the drafter's P1 (121 s at 29 s a step) RELAYED.
- SignIn `:91` to `:93` (a late printer sign-out ends the NEW broker session): true by the code: `SignedOutItem` (`:222`) runs
  `EndBrokerSession()` only (no printer call), on whatever `_held` is at its turn. P2 RELAYED. "Whether a printer
  sends such a late sign-out is UNMEASURED": correctly marked.
- Registration `:108` to `:109`: false for a late same-object answer (FOUND 1); true otherwise (T13, G5).
- Registration `:140` to `:142`: true for the two shapes it names; does not name FOUND 3; "cannot tell" (FOUND 4).

## TESTED (MEASURED, macOS arm64; every dotnet job and test executable through the kit's `heavy.py` unchanged, one at
a time, the wave lock shared with reader B1939; load1 3.2 to 6.8; lock waits 0 or 1)

- Tools: the ten files of kit B1935's THE TOOLS copied from `d1935/gate`, sha256 10 of 10 equal to the kit's table.
- The commit is the two patches: in `clone` at main, `1-cells-red.diff` applied, the three test files then equal the
  head's (`git diff --stat c15e13f5 -- tests` empty); then `2-fix.diff`; then `git diff --quiet c15e13f5` rc 0 and
  porcelain the seven `M` rows. The stored message equals `commit-message.txt`. Numstat 14/5, 17/8, 9/0, 5/1, 59/0,
  6/1, 37/1 (the kit's).
- RED FIRST at main (the cells alone; locked restore rc 0; build `0 Warning(s)` `0 Error(s)`): SignIn `Total: 62,
  Errors: 0, Failed: 5`: B08 `Assert.Single() Failure: The collection was empty`; B09 `D`, `N`, `B` and B10 each
  `Expected: LookupFailed` / `Actual:   SignedIn`. Universal Print `Total: 347, Errors: 0, Failed: 1`: T13 `T13 the
  held bytes: the bytes differ`. Each red is its own assertion.
- GREEN at the head (`head`, porcelain 0 after the locked restore): build 0/0; the whole solution `total: 1668`,
  `failed: 0`, `succeeded: 1664`, `skipped: 4`, no `failed Datasec.` line (control `Test run summary` 1).
- Mutants (`mutants_f1.py` unchanged, driven by `g1938/scratch/mutants_drive.py`: apply, build 0/0, the library's
  executable whole, undo `equal True`, `git diff --quiet HEAD` rc 0, then a REBUILD before anything else ran):
  `mAuditOneTry` SignIn 62 / 1 (B08); `mEmptyTaken` 62 / 4 (B09 x3, B10); `mSameObjectHeld` Universal Print 347 / 1
  (T13, `the held bytes`); `mSameObjectDisposed` 347 / 1 (T13, `the held bytes`); `mSameObjectAccepted` 347 / 1 (T13,
  `past the lifetime: expected TokenAnswerRefused, nothing was thrown`). Each exactly its cells. After all five: 62 / 0
  and 347 / 0.
- Surface: `surface_f1.py head c480a0c8...` rc 0: SignIn 46 lines / 13 files, Registration 48 / 12, Secrets 74 / 19,
  `SURFACE: equal (3 folders)`; `--control` `CONTROL FIRED: 3 of 3`.
- Probes: scratch classes `ZG1938Probes` (S1 to S3) and `ZG1938UpProbes` (G1 to G6), each fact reporting by
  `Assert.Fail("PROBE ...")`, in no patch, source `g1938/scratch/`. Built and run (`-class`) once at main (in `clone`,
  over the red cells) and once at the head; both times moved out after (`_quarantine/probe-main/`, `probe-head/`);
  then porcelain 0, rebuild 0/0, whole solution 1668 / 0 again.
- Paths: `diff --name-status c480a0c8 c15e13f5` seven `M` rows, the owned paths. The seven files at the head are
  printable ASCII with no tab, 0 CR, a final LF. `unittest` `Ran 111 tests`, `OK`; `repo_rules.py` (no
  `--source-documents`) `RULES: clean (530 files)`.
- Merge with main: main is still c480a0c8, so the merge is the head's own tree (`merge-tree --write-tree c480a0c8
  c15e13f5` = `13bbc6a1`, the head's tree). With lane F2 as well (`merge-tree c15e13f5 b74f0f0c` rc 0, tree
  `39f04ba2`, the 14 paths of the two lanes, no conflict; F2's head has parent c480a0c8 too): that tree in `clone`
  (`git diff --quiet 39f04ba2` rc 0): locked restore rc 0; build 0/0; `total: 1670`, `failed: 0`, `succeeded: 1666`,
  `skipped: 4`; `RULES: clean (530 files)`.
- HOSTED head: `hosted2.py c15e13f5... --total 1668 --rules 530 --skipped-linux 4 --skipped-windows 21 --unit 111
  --floor 111 --hardened-scan`: run 45029555551, four jobs success, attempt 1; linux 1668 x2 / 1664 / 4, GUARD 10;
  windows 1668 x2 / 1647 / 21, GUARD 11; rules 530, floor 111; every hardened secret-scan row OK; `HOSTED
  c15e13f5fb89bc33b0f7c8ab9bcd1cc56d2b222d: PASS`. HOSTED main c480a0c8 (1662): `PASS`, Analyze rows success.
- WORDS: `--control` `CONTROL FIRED: 13 of 13`; over the 147 added lines and the stored message: `WORDS: clean (2
  files)`.
- GITLEAKS 8.30.1: control FIRST (a token shape built by a program from two halves and 36 random characters, never
  printed) rc 1 `leaks found: 1`, moved to `_quarantine/gl-control-commit`; the added lines and the message as
  neutral `1.txt`, `2.txt`: rc 0, `no leaks found`.

## NOT TESTED

- Nothing on Linux or Windows locally (the hosted legs are those runs); the probes there: UNMEASURED.
- No publish, release guard, `run_step.py` neutral scan or locked restore with `--force` locally: the hosted run and
  the seat's chain cover them (RELAYED from STATUS).
- The seat's loops (50 and 10 runs) not repeated; my runs of each executable were green every time.
- The drafter's probes P1 to P4 and Q1 to Q3 not re-run (RELAYED); S2, S3, S1 and G6 cover P4's, P3's and Q2's shapes.
- No CodeQL locally; the head's push run has no Analyze rows, so code scanning is read on a pull request.
- FOUND 2's counts are one run of a race on one machine.

## FOR THE FIX ROUND (round 2; the coordinator's to commission)

Inside the owned paths only, no public change: (1) the late-answer path does not dispose an answer that is the held
object (FOUND 1), with a cell of G1's shape, red first; (2) `answer.IsDisposed` checked again in `Finish` under
`entry.Sync` (FOUND 2); a deterministic cell may not exist for the window, so the mutant that removes the re-check and
a scratch race probe like G4 are the control; (3) FOUND 3 named in the Limits line, or refused with a cell; (4)
"cannot tell" -> "does not check" (FOUND 4). Parts (a) to (c) need nothing. The landing texts in this folder are for
the form only: do not land on this verdict.

## SCANS (of the texts of this folder, after the last edit)

- `words.py` per file: `pr-title.txt` (180 bytes), `squash-subject.txt` (189), `squash-body.txt` (1476, 26 lines):
  every class 0. `pr-body.md`: `coordinator` 2 (the required who-decides line) and 4 non-ASCII bytes (the required
  robot line); every other class 0.
- `build/squash_scan.py` (main c480a0c8's, from the `head` clone, whose `build/` equals main's), with `#PRNUM` replaced
  by `#26`: control `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.
- gitleaks 8.30.1: a fresh firing control, then the texts of this folder as neutral `<n>.txt`: the last line below.
- gitleaks result: fresh control rc 1, `leaks found: 1` (moved to `g1938/_quarantine/gl-control-texts`); the seven texts of this folder (this file before this line) as neutral `1.txt` to `7.txt`: rc 0, `no leaks found`.
