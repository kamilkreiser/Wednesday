GATE B1888: GO WITH FINDINGS @ edaa1b7 on main ca94ed9

Gate G1, lane G round 3 (the one extra test-only round), DELTA, whole-lane reader (successor of B1866). OXPd 2, the
job service: test-only commit C1 `2cfbd9dd45f2faedaa627c59984c3b2d3e1d8ef8` (one parent HEAD2 `8efae983`) and merge C2
`edaa1b7088baf50f182a01388b1778d645fc29a6` (parents C1 and main `ca94ed966ff476d31e2d35cb1ae0cc5c5d4b39b5`), branch
`b1841/wp17-scan-and-print-jobs`. Read and measured 2026-11-22, 10:27 to 10:55 AEDT (clocks by `date`), on Opus 5.5,
in the gate's own scratch clone (`clone.py ... draft`: push URL `invalid://no-push`, no identity) and a scratch
worktree, both in the session scratchpad. Kit tools copied from `fleet/state/s306/d1872/gate/` by `cp -Rc`: 16 of 16
sha256 equal to THE TOOLS of kit B1872; `hosted.py` of `s304/d1835` sha256 `e73339f3...` equal. Every dotnet job went
through the kit's `heavy.py` (230 jobs; the wave lock by `mkdir` with `owner.txt`, released by move into my
`_quarantine/locks/`; waits in 7 jobs, at most 14 polls: the other reader's jobs; the lock folder absent at the end);
restores with `-p:NuGetAudit=false`; `repo_rules.py` never got `--source-documents`; no key folder and nothing under
`Source_Documents/` opened, listed or hashed; synthetic values only, none printed. Evidence beside this file.

**BLUF.** The delta is exactly the one helper change, byte-equal to the kit's `1-a03.diff`; the merge of main holds
and changes no lane byte; no product byte changed. The flake is gone at the head: **0 of 160** Jobs-project runs
failed (a loop of 60 and one of 100), while the same loop at HEAD2 **failed 1 of 40** here (A03, `Collection was
modified`, `ReceiverTests.cs:621` from `:144`), and the forcing probe is red 3 of 3 at HEAD2 and green 3 of 3 at the
head. The secret-text property is still caught (mUnknownEarly, mKeepField, mKeepInSpool red on A03; mKeepTask the named
survivor). Suite 1524 / 0 failed; hosted PASS. Merge ready on main ca94ed96 and on ca94ed96 plus lane I. One Minor
(text): the named limit of the skip list is wider than "inside a Task" (B1889's F1, re-measured here); written into
the landing texts.

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | Minor (text) | **The named limit is wider than the kit, STATUS and C1's message state.** The walk does not see text kept as the state of ANY skipped object, not only inside a `Task`. MEASURED here: B1889's mutant mKeepInGone (`_ = _spool.GoneToken(job).Register(static _ => { }, text);` added in `OpenScan`) survives at the head (Jobs project total 120, failed 0; the library dll newer than the edit; undone, `cmp` equal, `git diff --quiet -- src` rc 0). Red at HEAD2: RELAYED from B1889 (not re-run here). The product registers no callback: `git grep 'Register('` over `src/Datasec.Suite.Jobs` at edaa1b70 rc 1 (control: `GoneToken` 2 lines, `CreateLinkedTokenSource` 3 lines; a linked source's callbacks carry the source, not text, DERIVED). No secret is kept there today, so this is a limit to state, not a hole. | Stated in `pr-body.md` and `squash-body.txt` (Limits) and `FOR-RECORDS.md` item 1, in the coordinator's words. No code change. |
| F2 | Records | The new comment above `NotOwnState` reads "Never the receiver's or its spool's storage"; `SpoolJob.Gone` is a `CancellationTokenSource` the spool's job holds (no secret text: census). | FOR-RECORDS.md; a later wording edit if wanted. |
| F3 | Records | The HEAD2 loop rate varies by machine state (drafter 0/145, B1866 12/40, seat 5/40, here 1/40); the forcing probe is the timing-free instrument. | FOR-RECORDS.md. |

No Blocker, no Major.

## 1. Scope (item 2)

- `git diff --name-status 8efae983 2cfbd9dd`: exactly `M tests/Datasec.Suite.Jobs.Tests/ReceiverTests.cs`, +19 -2.
  `git diff 8efae983 2cfbd9dd` is **byte-equal** (`cmp`) to `1-a03.diff`; `1-a03.diff` applied to HEAD2's tree in a
  scratch index gives `d7417f4e9128237d1a8fc79bf4622242611fe071` = `2cfbd9dd^{tree}`. The file at C1 and at the head:
  sha256 `7528a5c5...` (= THE CODE).
- `git diff 2cfbd9dd edaa1b70 -- src/Datasec.Suite.Jobs tests/Datasec.Suite.Jobs.Tests`: 0 bytes;
  `git diff 8efae983 edaa1b70 -- src/Datasec.Suite.Jobs`: 0 bytes (control: against 5dd0f859, 13071 bytes). No product
  byte changed since round 2.
- C2 against C1 changes 91 paths, exactly main's 91 since 8ae5e08c (`comm -3`: 0). The head against main: 32 `A`,
  1 `M` (`Datasec.Suite.slnx` +2 -0); no path outside the two job folders and the solution file.
  `slnx_order.py` on the head: `SLNX: ordinal, job lines 1 and 1` (control `CONTROL FIRED: 2 of 2`). No change to
  `Directory.Packages.props`, `.github`, `build`.
- Both commit messages equal the kit's `commit-message-a03-only.txt` and `merge-message.txt` (but git's trailing
  blank line), each ending in the attribution line.
- Added lines: 19, 0 outside printable ASCII (planted U+200B counts 1); `NotOwnState`/`B1872` count 3 (all
  `NotOwnState`; control `B1872` 3 in `force-probe.cs.txt`). `words.py` over the 19 added lines and both messages:
  `WORDS: clean (3 files)` (`CONTROL FIRED: 13 of 13`). gitleaks 8.30.1 (`--no-banner --redact
  --ignore-gitleaks-allow --exit-code 1`): planted control (built by program from two halves, never printed, then
  quarantined) rc 1; added lines, both messages and the head's `ReceiverTests.cs` under neutral names rc 0; the
  head's `src/Datasec.Suite.Jobs` and `tests/Datasec.Suite.Jobs.Tests` rc 0 each.
- Read whole: the helper at the head (`:597-:666`), A03 (`:101-:146`); the helper is used by A03 only (`git grep`).

## 2. Determinism (item 3; the loop of 40 at the head, as B1866's successor)

- **HEAD2** (8efae983, restored, built 0/0): `LOOP red: runs 40, failed runs 1, A03 failures 1, other failures 0,
  totals ['120']`; run 35's log holds `Collection was modified` once and `ReceiverTests.cs:621` and `:144` once each
  (control run 1: 0). The loop can fail on this machine.
- **Forcing probe at HEAD2** (kit's `force-probe.cs.txt`, scratch, then quarantined): 3 of 3 runs `total: 121`,
  `failed: 1`, the one red `B1872Force.F1_...`; FORCE lines: faults 8, 11, 5 of 300, every completed walk reached the
  other spool's root (292, 289, 295) (evidence/force-red-head2.txt).
- **The head** (restored, built 0/0, binary holds `IsNotOwnState`): `LOOP green: runs 60, failed runs 0, ...` (its
  first 40 included: 40 of 40 green) and `LOOP green2: runs 100, failed runs 0, ...`, totals 120. Whole solution
  `LOOP sln: runs 3, failed runs 0, ... totals ['1524']`.
- **Probes at the head** (force + census, scratch, then quarantined): 3 of 3 `total: 123`, `failed: 0`; FORCE faults
  0, other spool's root 0, own root 300 of 300; `CENSUS CONTROL ... 6 of 6`; 52 types, 22 skipped-type fields (4
  non-generated: `ScanReceiver._time`, `JobSpool._time`, `PrintJobSender._time`, `SpoolJob.Gone`); exactly the
  three SKIP paths (receiver `_time`, spool `_time`, a job's `Gone`); `OWN OBJECTS ... fixed walk: 5; old walk: 5`;
  own objects lost 0. In the run whose old walk met no pending timer the two walks agree (seen 39/51, strings 6/6).
  (B1889 rules the census and own-object count as its item; recorded here as corroboration.)

## 3. The property still caught (item 4; on `ScanReceiver.cs` at the head, Edit tool, one heavy job each, undone and proved by `cmp` against the pre-mutant copy and `git diff --quiet -- src` rc 0 every time)

| Mutant | Result |
|---|---|
| mUnknownEarly | **red**: A03 only, `Assert.Equal() Failure: Values differ`, `Expected: 3`, `Actual: 2`, `:135` |
| mKeepField | **red**: A03 only, `A03: the receiver keeps the secret's text`, `:144` |
| mKeepInSpool | **red**: A03 only, same message, `:144` |
| mKeepTask | **survives** (total 120, failed 0; the mutant is in the test's copy of the library: `KeptTask` 1) |
| mKeepInGone (B1889's, on Tuesday's request) | **survives** at the head (F1) |

**Ruling on mKeepTask as a named limit: acceptable**, widened per F1: the walk cannot follow the six types without
reaching state all tests share (the measured cause of the round-2 red), and the library keeps no text in any of
them today (no Task field outside an async method's own state, by the census; no `Register(` call; 0 static fields;
0 AsyncLocal/ThreadLocal/ThreadStatic). The limit is a test's blind spot, stated in the landing texts. After the last
undo: whole solution rebuilt 0/0, `total: 1524`, `failed: 0`.

## 4. Suite and hosted (item 5)

- Head, through the lock: restore rc 0, 0 lines naming `http`, `status --porcelain` 0; build `0 Warning(s)`,
  `0 Error(s)`; `dotnet test -c Release --no-build`: **`total: 1524`, `failed: 0`**, `succeeded: 1520`, `skipped: 4`
  (three times more after mutants, plus the 3-run loop). `repo_rules.py <clone>` (no option, no sibling
  `1_Project_Definition`): `R5 hash half NOT RUN`, `RULES: clean (476 files)`; `unittest discover -s build/tests`
  `Ran 60 tests`, `OK`.
- Hosted run 44961278314 of edaa1b70 by GET: `hosted.py edaa1b70... --total 1524 --rules 476 --skipped-linux 4
  --skipped-windows 19 --unit 60 --floor 60`: four jobs success, attempt 1, nothing beside them; linux 1524 x2,
  succeeded 1520, skipped 4, GUARD 10; windows 1524 x2, succeeded 1505, skipped 19, GUARD 11; secret-scan both
  PLANTED-CONTROL lines, `objects of this commit not among them 0`, `no leaks found` x3; rules `Ran 60`, floor 60,
  `RULES: clean (476 files)`. **`HOSTED edaa1b70...: PASS`**; control `--total 1525`: `FAIL 4`. Windows log: 0 skipped
  lines naming a Jobs test (control 9 name KeyRing); 0 `Collection was modified` in either leg.
- CodeQL: NOT RUN (Tuesday's, on the pull request; not available on this machine).

## 5. Merge readiness (item 6)

- **Main ca94ed96:** `merge-tree --write-tree ca94ed96 edaa1b70` rc 0, tree `83d583a5...` = the head's tree; main is
  in the head. Numbers: 1524 / 476 / `Ran 60` (= the seat's). Origin by GET 10:47:42: branch = edaa1b70, main =
  ca94ed96, open pull requests 0, none with this head, open alerts on main 0, `compare main...edaa1b70` 5 / 0 / 33.
- **Main ca94ed96 plus lane I (ff1defac, based on 5bb1418c):** `merge-tree ca94ed96 ff1defac` rc 0, tree `9a1e42a2`
  (446 files); with edaa1b70 over base ca94ed96 rc 0, tree `f82bc894` in both orders and by the natural
  `merge-tree ff1defac edaa1b70`; 478 files; slnx ordinal, job lines 1 and 1. In a scratch worktree through the lock:
  restore rc 0 with no lock file changed; build 0/0; **`total: 1524`, `failed: 0`, `skipped: 4`**; both publishes rc
  0, GUARD 10 and 11 files; `RULES: clean (478 files)`; **`Ran 108 tests`**, OK (lane I's FLOOR=108).
- Both sets are in `landing.txt`, labelled case A and case B, with the form of the B1877 landing:
  `pr_retrigger.sh --check`, `pr_checks_wait.sh --min-checks 8`, CodeQL analyses at the head's sha first then open
  alerts 0, the merge-ref job logs by `--allow-escape-sequences`, the head-pinned squash, after-merge reads.

## 6. The seat's deviations (STATUS DEVIATIONS 1 to 6)

1. The loop at HEAD2 read 5 of 40, not the kit's 0: **accepted** (a stronger red; recorded under Q37; this gate read 1
   of 40 at HEAD2 with the same message and frame).
2. `unittest` run through a `subprocess.run(..., cwd=<clone>)` wrapper (no `cd`): **accepted** (this gate did the
   same; `Ran 60`).
3. The two gitleaks control files moved to quarantine: **accepted** (never delete).
4. The pane check counted titles; no pane titled `Datasec/OXPd2-X23`: **accepted as records** (the REFUSE is "more
   than one"; not met).
5. `3-mutants.txt` header says Q39 where the kit says Q38: **accepted as records** (kit text; mReasonDisposed not run
   under Q38 NO either way; FOR-RECORDS).
6. STATUS drafted in scratch and written by `os.replace`: **accepted** (the kit's HOLDS form).

The seat's other claims re-checked and true: C1/C2 shas, parents and tree; 19 / 2; 1311 at C1 (not re-run here: the
head was measured instead); 1524 / 476 at the merge; mutant results; `HOSTED edaa1b70: PASS`.

## 7. Landing texts

Written in this folder: `pr-title.txt`, `pr-body.md` (all three rounds; limits stated plainly incl. F1; the host does
not use it yet), `squash-subject.txt` (ends `(#PRNUM)`), `squash-body.txt` (ends with the attribution line),
`landing.txt`, `FOR-RECORDS.md`. Each claim in them re-read against the head (18 reasons in `JobServiceError`; no
server reference to the library, `git grep 'Suite.Jobs' src/Datasec.Suite.Server` rc 1; no package, workflow or
build file change). Scanned by `evidence/texts.py` (B1877's program, paths, the five branch commits and a planted
value built at run time changed): each text exported through the workflow's own `neutral_export` (ci.yml lines 120
to 128 at the head) as a commit message and scanned with the workflow's options: title, title and body, body, squash
message with a number and as written, squash body, the default squash shape over all five branch commits, landing.txt:
each rc 0 `no leaks found`, stored whole; the planted control rc 1 `leaks found: 2`. Word counts: the four
repository texts 0 in every class but one host match in `squash-body.txt` (the attribution address), non-ASCII 0;
`words.py` over the four: `WORDS: clean (4 files)`; landing.txt (not repository text) holds B-numbers and paths by
design. Word controls 16 of 16. **Land only when B1889 is also GO or GO WITH FINDINGS** (RELAYED: it is).

## 8. What was NOT tested

- The W02 body cell and mReasonDisposed (not in this round: Stamp S4, Q38 NO; their absence is not a finding).
- mKeepInGone at HEAD2 (RELAYED red from B1889); kit B1862's eleven earlier mutants (product unchanged since round 2).
- Linux and Windows locally (macOS arm64 only; hosted legs read by GET); CodeQL; the R5 hash half; the publishes and
  release guard at the head itself (read in the hosted legs; run locally on the three-way tree only).
- Lane I's own correctness (only its merge with this lane); the pull_request merge-ref runs (none exist yet).
- A real transport, a device, what HP's devices send.
