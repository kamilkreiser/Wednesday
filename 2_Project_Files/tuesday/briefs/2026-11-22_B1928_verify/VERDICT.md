GATE B1928: GO WITH FINDINGS @ af26f80 on main 83683af

Gate G1 (sign-in and identity binding), round 1, READER 1 (the whole lane, the merge, the landing texts). OXPd 2, kit
B1914 (seat X28, lane A1, WP1.4 card part, component C5). Head `af26f801e23b4bc495acf34ee90f265d574ef290` on
`b1914/wp14-sign-in-state-machine` (one commit, parent `7b0f4f55`). Read and measured 2026-11-22 22:36 to about 22:55
AEDT, on Opus 5.5, in my own clones `fleet/state/s311/g1928/clone` (detached at the head) and `clone2` (the merge tree),
both by the kit's `clone.py ... draft` (push URL `invalid://no-push`, no identity). Origin by `gh api -X GET` under the
project GH_CONFIG_DIR: branch = af26f801 (one `b1914` ref); main was 0fc3344a at 22:36 and **83683af4 at 22:39 and
22:47** (pull request 22, lane U, as the coordinator relayed; one parent 0fc3344a; the eight Registration paths only);
open pull requests 0. No write to the project, GitHub or Jira; no push, no pull request; no `cd`; nothing deleted (my
probe file and scanner control moved to `g1928/_quarantine/`). The drafter's prototype was not needed for a
comparison: every D was probed directly on the head.

**BLUF.** The library does what THE CONTRACT and S4 say. D5 is built as S4 states it: the only `_broker.SignIn(` and
the only `_held =` assignment sit after both checks on one straight path, with the grant under `using`; every refusal
path I probed raises one audit, tells the printer and disposes the grant. D7 measures arrival to turn, `>=` the limit
and a future stamp refused, and extreme stamps are `StaleTap` without an exception. Measured on macOS arm64: the head
1638 / 0 failed; the merge with main 83683af4 **1646 / 0 failed**; the SignIn assembly 50 of 50; the kit's 22 mutants
plus B06's and B07's each red on their cells (mSupersedeLate equivalent, as the seat said); 16 probes, one or more per
D. Hosted push run 45017401495 PASS at 1638; main's PASS at 1589. One Minor finding (a throwing `Audit` subscriber
hides the event from the subscribers after it), the rest Info. Nothing blocks the landing.

## FOUND

1. **Minor: the `Audit` event reaches only the subscribers before a throwing one.** `RaiseAudit` calls the multicast
   delegate once inside one `try/catch` (`SignInActor.cs:411-427`). A delegate invocation stops at the first throwing
   handler, so a later subscriber never sees that refusal. Probe P15: a throwing first handler, then a counting
   second one, a token of another user: `BindingRefused`, **second subscriber saw 0 audits**. The kit's B07 adds the
   throwing handler AFTER the kit's own, so it cannot see this. The result, the printer report and the next tap are
   unaffected (B07, P15). D15 says only "an Audit handler's exception is dropped", and that holds; but "the audit event
   is raised once" is per delegate, not per subscriber, and a refused binding is the record the design asks for
   (`02:432` "refused and audited"). Not blocking: nothing subscribes yet (the host does not use the library). Fix
   sketch (backlog): one try/catch per entry of `GetInvocationList()`. Named in pr-body "Still open" and FOR-RECORDS 1.
2. **Info: Q11's cost, measured.** A `DeviceSignedOutAsync` queued while a switch's printer step runs is taken after
   it and ends the NEW broker session; the printer keeps the new user with no broker session (P11: `SignedIn
   (previous session ended)`, sign-out `True`, `sid-2` gone, no printer sign-out). This is exactly the default's
   stated cost (kit Q11) and is UNMEASURED on a printer; the README's Limits do not name it. Named in pr-body and
   FOR-RECORDS 2.
3. **Info: three survivors of my own mutants (test strength, not defects).** `rSubjectIgnoreCase` (D5 (2) compared
   case-insensitively) leaves 57 of 57 green: no cell's subject differs from the object id by case only. The head
   refuses that shape before any printer call (P06: `SessionRefused`, calls `report:SessionRefused`, store 0); under
   the mutant the broker would still refuse it after a printer sign-in (DERIVED from its README's exact subject rule),
   so the property holds either way, only the "before the printer" half is unpinned. `rSupersedeIgnoredAtPrinter`
   (the `Superseded` check at `:360` removed): its window is the synchronous code between the acquire's answer and
   the lock; no fake reaches it deterministically. `rBrokerUserFromToken` (`grant.Grant.Subject` as the session user):
   EQUIVALENT by reading (checked ordinally equal two lines above).
4. **Info: identifier forms (as S4 words it).** `Guid.TryParse` accepts padded, parenthesised, 32-digit and hex-struct
   forms (P05: each `SignedIn`, 0 audits); a different identifier, the all-zero one against a real user, `""` and
   `not-an-identifier` are `BindingRefused` with one audit (P05, B02). The all-zero identifier binds when lookup and
   token both state it (P07): the identity service's job, the named limit.
5. **Info: display names keep format characters.** U+202E and U+200B in name parts are kept (P08): `char.IsControl`
   does not count category Cf. D6's wording; a panel concern for later.
6. **Info, read and held:** the stop sets `_stopped` under the lock and cancels outside it (`:157-168`), so a queued
   tap could start a lookup in that gap and then be cancelled (DERIVED; outcome still `Stopped`, nothing kept). The
   attempt and stop `CancellationTokenSource`s are never disposed (no timers: no leak of note). The default
   `TimeProvider.System` is THE CONTRACT's `time = null`; the boundary scan holds (no `GetUtcNow`, `Task.Delay` or
   timer).

## THE CONTRACT, D1 TO D16 AND H1 TO H22 (read against the code; probes MEASURED)

- Contract: every type and member of THE CONTRACT present with its name and shape; masks on `CardUser`,
  `IdentityGrant`, `SignInDetails`, `SignInAuditEventArgs`; `TapResult` the outcome name (+ fixed suffix) (P14, L01).
- D1: references `Datasec.Suite.Sessions`, `System.Collections`, `System.Runtime`, `System.Threading`,
  `System.Threading.Channels` only (P01); T1/T2 byte-equal; lock rule PASS (my program, control `FAIL b,c` rc 1).
- D2: one unbounded channel, `SingleReader`, one loop; a tap and a printer sign-out interleave in arrival order (P02).
- D3: DEL and NUL `InvalidCard`; space-padded cards are taken as distinct cards (P03), as the rule says.
- D4: paths (a) to (f) at `:262-326`; the same user under a braces/upper-case object id signs out (P04).
- D5: `:300` card user's id parsed; `:343` `using`; `:346` identifiers; `:352` subject ordinal; `:374` first printer
  sign-in; `:390` the only broker `SignIn`; `:400` the only `_held` write. P05, P06, P07; B01 to B03, B06, B07.
- D6: `DisplayNames.cs` as D6; P08.
- D7: `:234-238`; long.MinValue, 0, long.MaxValue stamps `StaleTap`, 0 lookups, no exception (P09); S01 to S03.
- D8: `:123-131`, `:357-366`; S04, S05; mSupersedeLate equivalent (agreed, by reading).
- D9: `StepAsync` arms `WaitAsync(_stepTimeout, _time, callToken)` before the call starts; a null task or a
  synchronous throw is a failed step inside `Task.Run`.
- D10: capacity 1: the second waiting tap `QueueFull`; printer sign-outs never refused (P10).
- D11, D12: P02, P11; a session id with a space, or null: `SessionRefused`, one sign-out, grant disposed (P12).
- D13 to D15: B01, D03, Q04; a stop during a lookup: `Stopped`, 0 acquires, 0 printer calls (P13); L03.
- D16: boundary scan of the 13 `.cs` files at the head: 20 banned words 0 hits, both required present; controls 22 of
  22. No writable static but one compiler cache field (P16), which L02 rightly skips.
- H1 to H22: every cell of the seat's table exists, is named by its id and is green; the README's Limits hold every
  item the kit requires plus the seat's additions.

## TESTED (MEASURED, macOS arm64; every dotnet job and test executable through the kit's `heavy.py` unchanged, one at a
time; lock folders moved to `g1928/_quarantine/locks/`; waits only on other holders, never broken)

- Tools: the seven of `<src>` copied, sha256 7 of 7 equal to the kit. `words.py --control` `CONTROL FIRED: 13 of 13`.
- Head: `CI=true dotnet restore --locked-mode --force` rc 0, porcelain 0 lines (no lock file changed); build
  `0 Warning(s)` `0 Error(s)`; whole solution `total: 1638`, `failed: 0`, `succeeded: 1634`, `skipped: 4`,
  `failed Datasec.` 0. Loop: `LOOP: 50 of 50 passed`, each `Total: 57, Errors: 0, Failed: 0`.
- Mutants (my program, one replacement each, one heavy job each: build of the SignIn tests 0/0, the assembly
  `Total: 57`; undo by copy, `cmp` equal every time; `git diff --quiet af26f801` rc 0 after): mBindingOff B01 B02 B07
  L01; mSameCardLookup A02 A06; mNoStale S01 S02 S03; mStaleStrict S01 S03; mFutureTaken S02; mNoSupersede S04;
  mSwitchKeeps A04 Q01 S05; mUnknownKeeps A05; mSubjectLate B03; mGrantKept A01 B01 B02 B03 D01 D02 D03; mLateKept
  B05 S04; mDeviceFailKeeps D01 D02; mBrokerFailKeeps D03; mUnbounded A07 B05 D02; mNoQueueCap Q02; mFormIgnored F01;
  mNoFallback F02; mControlTaken F02; mUpperCardTaken C01; mGuidOrdinal B02; mPrinterSignOutIgnored Q03; mNullGrantTaken
  B06; mAuditThrowsThrough B07; mSupersedeLate NONE (equivalent). Mine: rSameUserByText A03; rSubjectIgnoreCase,
  rSupersedeIgnoredAtPrinter, rBrokerUserFromToken NONE (FOUND 3). (mNullGrantTaken's first form did not compile under
  the nullable errors; re-made as `acquire.Value!` with only `End != Answered` refused. Table `g1928/logs/mutants-table.txt`.)
- Probes: a scratch class `G1928Probes` (24 cases, each reports by `Assert.Fail("PROBE ...")`; source
  `g1928/scratch/G1928Probes.cs`, in no patch), build 0/0, run by `-class`: Total 24, every one reporting (log
  `g1928/logs/probes2.log`). Then moved to `_quarantine/probe-file/`; porcelain 0.
- Merge: `git merge-tree --write-tree 83683af4 af26f801` rc 0, tree `06b275b05d96f847063e195093d2da39811bcb33`, 530
  files; against main exactly the 31 owned paths (30 A, 1 M, other 0); against the head exactly the nine files main
  gained. The slnx at main is blob 027a240f, unchanged since BASE, so the two lines still place by the ordinal rule
  (`Sessions` < `SignIn` < `UniversalPrint` in both folders; the merge's diff shows exactly the two lines). In
  `clone2` (that tree via `read-tree -u --reset`, `git diff --quiet 06b275b0` rc 0 before and after): locked restore rc
  0; build 0/0; whole solution `total: 1646`, `failed: 0`, `succeeded: 1642`, `skipped: 4`, `failed Datasec.` 0;
  `repo_rules.py` (no `--source-documents`; `test ! -e g1928/1_Project_Definition` rc 0) `RULES: clean (530 files)`;
  `unittest` `Ran 111 tests`, `OK`. Expected hosted on the merge ref: 1589 + 57 = 1646 both legs, succeeded 1642 /
  1627, skipped 4 / 19, RULES 530.
- HOSTED head: `hosted2.py af26f801... --total 1638 --rules 530 --skipped-linux 4 --skipped-windows 19 --unit 111
  --floor 111 --hardened-scan` rc 0: run 45017401495, attempt 1, four jobs success, `check runs beside the four: 0`;
  linux and windows `total: 1638` twice each; `failed Datasec.` 0 and 0 (control `Datasec.Suite.SignIn` 7 and 7); last
  line `HOSTED af26f801e23b4bc495acf34ee90f265d574ef290: PASS`.
- HOSTED main: `hosted2.py 83683af4... --wait --total 1589 --rules 500 ...` rc 0: four jobs success, Analyze actions,
  csharp, python beside them; `HOSTED 83683af4be3fb39612153c103f922fc2febf7acc: PASS`. Open code-scanning alerts on
  main 0.
- WORDS: over the 2556 added lines (7b0f4f55..af26f801, lock files left out) and the stored commit message (`cmp`
  equal to the kit's `commit-message.txt`): `WORDS: clean (2 files)`.
- ASCII: every added file but the two lock files, 0 lines outside printable ASCII.
- GITLEAKS 8.30.1: control FIRST (a token shape built by program, never printed): rc 1, moved to
  `_quarantine/gl-control`; then the 31 files at the head, the message and the added lines as neutral `<n>.txt` (33
  files): rc 0, `no leaks found`.
- Lock files: the two new ones' sha256 equal the kit's prediction (`1a1957a6...`, `7df6497a...`); no existing lock
  file in the diff.

## CODEQL (read on the pull request; landing step 3)

No CodeQL locally; the branch push had no Analyze rows. A reader of the Analyze (csharp) rows checks a
`/language:csharp` row AT af26f801 with results_count 0 and open alerts 0, and reads any alert against the shapes
landing.txt step 3 lists (the generic catches, the fire-and-forget `ContinueWith`, the undisposed token sources,
`complete.Value!`). An alert is fixed by a new commit and a new gate, never dismissed.

## NOT TESTED

- Nothing on Linux or Windows locally (the hosted legs are those runs). No publish or release guard locally (hosted:
  GUARD clean 10 and 11). No `run_step.py` neutral scan locally (the hosted secret-scan ran it on this head).
- The red-first state not re-made here (the seat's run and the 24 mutants on the head carry it).
- D5 and D7 adversarially: the second reader's (B1929). My D5 and D7 probes (P05 to P07, P09) are a first pass only.
- Nothing against a printer, a simulator, a tenant or the real identity service.

## THE LANDING TEXTS (this folder)

- `pr-title.txt` 236 bytes (under 256; not the commit subject, 249 bytes). `squash-subject.txt` 245 bytes, the title
  plus ` (#PRNUM)`. `squash-body.txt`: what and why in three paragraphs, ending
  `Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>`. `pr-body.md`: why, what changed, what proves it, still
  open (no printer, the placeholders, re-delivery, the sign-out without a session id, the multicast audit, the named
  limits), who decides: the coordinator, as coordinator; no line says the product owner decided anything; ends with
  the Claude Code line. `landing.txt` in B1924's form with this pull request's numbers: main 83683af4, merge tree
  06b275b0, merge-ref totals 1646 both legs, succeeded 1642 / 1627, skipped 4 / 19, RULES 530, Ran 111, floor 111;
  step 6 main's push run PASS at 1646; MAIN MOVES for lanes S (+5) and D (+6), with any csproj, lock, props, slnx or
  Sessions change a STOP.

## SCANS (of the landing texts, after the last edit)

- `words.py`: `pr-title.txt`, `squash-subject.txt`, `squash-body.txt` every class 0 (`WORDS: clean (3 files)`).
  `pr-body.md`: `coordinator` 2 (the required "who decides" lines) and 4 non-ASCII bytes (the required robot line),
  every other class 0 (`WORDS: 6 hits`, as B1924's pr-body read).
- gitleaks 8.30.1: a fresh firing control (rc 1, moved to `_quarantine/gl-control2`), then the seven texts of this
  folder as neutral `<n>.txt`: rc 0, `no leaks found`.
- `build/squash_scan.py` (main 83683af4's, from `clone2`) with `#PRNUM` replaced by `#23` and `squash-body.txt`:
  control `rc 1, found 2`, message `rc 0, found 0`, `SQUASH-SCAN: clean`.
- Only this SCANS section was edited after those scans (no landing text changed).

Can it land? Yes, by `landing.txt`, once the second reader's VERDICT (B1929, D5 and D7) reads GO or GO WITH FINDINGS
and the pull request's merge-ref checks (1646 on both legs) and CodeQL read as its step 3 requires. The Minor finding
(FOUND 1) goes to the backlog; it is not a condition of this landing.
