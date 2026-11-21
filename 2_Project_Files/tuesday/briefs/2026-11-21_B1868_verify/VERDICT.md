GATE B1868: NO GO @ 523204d on main 8ae5e08

Gate G1, round 1 of 2, whole-lane reader. OXPd 2, WP1.2 in part, lane E: the OXPd 2 adapter beyond its generated
clients (per-device solution-token holder, callback credential check, five printer callbacks), kit B1849, seat X25,
head `523204dda0042eab2f2483257b7b0f29706c68fd` (one parent `8ae5e08c`) on branch `b1849/wp12-oxpd2-adapter`, main
`8ae5e08cadf6460f6f87fff091d3bafada2efe41`. Read and measured 2026-11-21, 21:58 to 22:16 AEDT (clocks by `date`), on
Opus 5.5, in the reader's own clone (session scratchpad `b1868-clone`, made by the kit's `clone.py ... draft`: push URL
`invalid://no-push`, no identity). Scratch and logs: `/private/tmp/b1868-gate/`; the probe source, the mutant program,
the scope program and their outputs, and the hosted reading are copied into `evidence/`. Every heavy job went through
the kit's runner (`heavy.py`; the seven tool files of `fleet/state/s305/d1849/gate/` seven of seven equal to the kit
by sha256; `words.py --control` `CONTROL FIRED: 13 of 13`): load1 first, the wave lock
`<project>/.tools/wave1-heavy.lock.d` by `mkdir` with `owner.txt`, released by a move into
`/private/tmp/b1868-gate/_quarantine/locks/` (the first job waited 3 polls behind reader B1866: a wait, not a finding);
restore `--locked-mode -p:NuGetAudit=false` with `CI=true`. `repo_rules.py` was never given `--source-documents`; no
key folder was hashed, listed or opened; every token, credential, card read and user is synthetic, made at run time,
none printed; no socket, no listener, no request to any printer or host (the device is a fake handler in the test
process). No git write in any project tree, no GitHub or Jira write, no message.

**BLUF.** One Major, so NO GO for round 1. The token holder's single flight does not cover a request that ARRIVES
while a refresh is running: that request waits for the running refresh, then runs a SECOND refresh although a fresh
access value is held by then (measured deterministically, both after a start and after a 401; finding F1). Concurrent
401s still cause exactly one refresh (200 rounds x 16, max 1 endpoint call in flight), the rotation order holds (1600
sends, 0 before their rotated refresh value was written), and everything else of the callback side holds under my own
inputs: no body byte is read before the credential passes (every refusal, 0 read calls), the five operations only,
the bounds, the landed parser only, the stale-read guard, the sink under its deadline, the answer re-parsed, and no
value in any text. Scope is the 34 paths of the property; no landed contract test changed and all are green; the
merge onto main is the head's own tree; suite 1234 failed 0; hosted PASS. Both seat deviations Tuesday put to the
readers grade Minor. Five more findings are Minor or records. The fix is small (count completed flights, or use a held
value after taking the flight lock) plus one cell; a fix round follows.

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | **Major** | **A request that arrives while a refresh is running causes a second refresh.** `DeviceTokenHolder.FlightAsync` (`Device/DeviceTokenHolder.cs:265-300`) increments `Flights` at the START of a flight (`:290`), and the lazy path (`AcquireAsync`, `:172-192`) records `observed = entry.Flights` when it finds no access value (`:188`). A caller that looks during a running flight records the in-progress count; after the flight it finds `Flights == observed` (`:277`), skips the reuse branch and runs its own refresh (`:290-294`), though `entry.Access` now holds a fresh value. Measured (probe G17, deterministic, the endpoint held by a gate): (a) A starts the first refresh, B arrives during it: **2 endpoint calls, 2 distinct access values sent**; (b) primed, A gets a 401 and its renewal is held, C (a new request) arrives during it: **2 endpoint calls after the prime**. Also seen unforced in G11 (200 rounds x 8 concurrent first sends: max 2 endpoint calls in a round). This contradicts the kit's D4 (2) ("if no access value is held, refresh first": at the second refresh one IS held), the class summary (`:9-10`, "a caller that waited for another caller's refresh reuses its result") and the STATUS (BLUF "single flight per serial"; FOR TUESDAY 5 "a caller that waited for another caller's refresh gets that refresh's result"). Under the verifier standard a claim the numbers contradict is Major. Harm (DERIVED, UNMEASURED on a device): one extra token-endpoint call per burst of requests that meets a refresh; if a device keeps one active access value per solution, the extra refresh can invalidate the value a 401-retry is carrying, and that retry's second 401 marks the device `NeedsRepair` (out of service until an operator stores a new refresh value). No value is leaked and the rotation order is kept (the second refresh re-reads the vault after the first `Put`). | Count COMPLETED flights (increment when a flight ends, so `observed` is a value that was handed out), or, on the lazy path, after taking `entry.Flight` use `entry.Access` when it is not null. Add a cell: a request that arrives while a held refresh runs causes no second endpoint call, after a start and after a 401 (G17's shape). Keep G10/T04. |
| F2 | Minor (records) | **Deviation 4, graded** (Tuesday's ruling 2 put to the readers). Measured (G05): a body stream that throws after the credential passed gives `HandleAsync` the stream's OWN exception object, unchanged, for `IOException`, `OperationCanceledException` (not the caller's token), `TimeoutException` and `ObjectDisposedException`, no inner exception added. The same throwing bodies under a wrong credential are never read (Unauthorized, 0 read calls). No credential, token or body byte can leak by this path: the exception is the host stream's, the library adds no text, and `BoundedReader` zeroes its buffer in `finally` (`Device/BoundedReader.cs:50-53`); the sink is not called. The `OperationCanceledException` case means a host cannot tell the caller's cancellation from the stream's by type alone (D20 says OCE only for the caller's own token); that is the host's mapping. The README's limit names "an I/O error" only. | Minor: keep for round 1 as Tuesday ruled. Records: widen the README limit line to "any exception the body stream throws (an I/O error, its own cancellation or timeout) passes out unchanged". If the fix round touches it, Tuesday's default (`BodyFailed`) is fine. |
| F3 | Minor | **Deviation 3 accepted, with two notes.** The check is typed and texted as D18 requires (G12: empty, space, CR LF, 0x7F, non-ASCII, NUL each `ArgumentException` with a fixed message holding no value, 6 of 6; the holder reports each as `RefreshFailed`, no inner exception, state `Ready`, 0 device calls). But (a) `SolutionTokenGrant` keeps the caller's memory (`Device/SolutionTokenGrant.cs:25`, no copy): a grant whose bytes change after construction passes the check, and the held value then makes every send throw `FormatException` (G12, measured), not `DeviceTokenException`, with no refresh; (b) no cell of the lane tests the check: the mutant mGrantNoCheck (the byte check removed) leaves the lane's 43 tests green and only my G12 red. | Copy the bytes in the constructor (`accessValue.ToArray()`) and validate the copy; add a cell for the check. Needs an endpoint implementation that misbehaves, so Minor. |
| F4 | Minor (records) | **A timed-out refresh overlaps the next and its late grant is dropped.** G13: an endpoint that ignores its token and hangs: the first send ends `RefreshFailed` at `RefreshTimeout` (as D5 says), the next send starts a second endpoint call while the first is still running (2 in flight), and when the first finally answers with a rotated refresh value, that value is never stored. If a device invalidates the old refresh value on rotation (UNMEASURED, H22), the device then ends `NeedsRepair`. This is D5's design (cancel at the bound), not a code fault. | Records: name it in the README's Limits ("a refresh answered after `RefreshTimeout` is discarded, a rotated refresh value with it") and in NOT DECIDED item 5. |
| F5 | Minor (test gap) | Two of my mutants show gaps in the lane's cells: mOpNoMethod (the method check of `FindOperation` reduced to non-null) leaves the 43 green (only my G03, `GET /prePromptResult` and `post`, goes red); mFailReuseOff (a waiter no longer reuses a failed flight's error) leaves every test green, so FOR TUESDAY 5's "a failure included" is unpinned. | Add a B02 row for a handled path under another method; pin the failure reuse or drop the claim. |
| F6 | Minor (text) | README line 37 ("so the same work is done") and the class summary of `CallbackCredentials` are true of the COMPARISON only: an unknown serial reads the vault on every call while a known one is served from the cache (`Callbacks/CallbackCredentials.cs:147-167`), so whether a serial is enrolled may be told by timing. The serial is not a secret (the host names it) and the credential comparison itself is fixed-time; the second reader owns D9 in depth. | Records: say "the same comparison is done"; consider caching a negative result, or leave as a named limit. |

No Blocker. Every finding but F1 is Minor, records or text.

## 1. Scope, landed constraints, merge (my scope program, `evidence/scope.py`, output `evidence/scope.out`)

- `git diff --name-status 8ae5e08c 523204dd`: 34 rows, A 32, M 2, outside the property 0; control (a planted
  `M src/Datasec.Suite.Adapters.Oxpd2/Generated/Runtime/Oxpd2Json.cs`) outside 1. Added only under `Device/`,
  `Callbacks/`, the one `README.md` and `tests/Datasec.Suite.Adapters.Oxpd2.Tests/`; the two M rows are
  `Datasec.Suite.slnx` and the adapter's project file, each `1 0` by numstat.
- Unchanged against main: `Generated/`, the adapter's `packages.lock.json`, `contracts/`,
  `tests/Datasec.Suite.Contracts.Tests/`, `Directory.Packages.props`, `.github/`, `build/`, `global.json`,
  `Directory.Build.props`, `NuGet.config` (each `yes`; control over `Datasec.Suite.slnx` fires). One lock file in the
  diff, the new test project's. Adapter project file: `ProjectReference` 0, `PackageReference` 0,
  `InternalsVisibleTo` 2 (sha256 `0bf22003...` = T1). Test project: one `ProjectReference` (the adapter), one
  `PackageReference` (`xunit.v3`, central) = T2.
- The solution line: `place.py --dry` over main's own `Datasec.Suite.slnx` placed it at tests 14 (ordinal True), and
  `--write` on that copy gives a file byte-equal (`cmp`) to the head's; `--dry` over the head's file refuses
  `already present` (the control).
- Every landed contract test green and unedited: `tests/Datasec.Suite.Contracts.Tests/` has no diff; at the head
  `Datasec.Suite.Contracts.Tests.dll passed`; the suite total 1234 = main 1191 + the lane's 43 (the lane's project
  alone ran 43 + my 17 = 60), so no contract test count moved.
- **The merge (B1868):** `git merge-tree --write-tree 8ae5e08c 523204dd` rc 0, clean, tree
  `bcef7003d7931044508fefef98e9c2465acb16dc` = `523204dd^{tree}` (merge base 8ae5e08c; 402 files against main's 370).
  `python3 -I build/repo_rules.py <clone>` WITHOUT `--source-documents`: `RULES-NOTE: R5 hash half NOT RUN`,
  `RULES: clean (402 files)`, rc 0 (= `git ls-files` 402). `python3 -I -B -m unittest discover -s build/tests`:
  `Ran 60 tests`, `OK`; `ci.yml` `FLOOR=60`.
- Text: the 33 added or changed files but the lock file: bytes outside printable ASCII and LF 0, CR 0, tabs 0, no file
  without a final newline. `words.py` over the 4219 added lines (lock file excluded) and the commit message:
  `WORDS: clean (2 files)`. Ban-list names 0 (control 1), "product owner" 0, decided/ruled/approved 0, B-numbers 0,
  ticket keys 0, C-ids 0, 64-hex literals 0, 43-character base64url runs 0. No text says the product owner decided
  anything about the adapter. gitleaks 8.30.1 with the workflow's options over the clone: `no leaks found`, rc 0
  (control: a planted token built from two halves, rc 1).

## 2. THE CONTRACT and THE REQUIRED SECTION, with my own inputs

The product code (21 files) read whole. The public surface is THE CONTRACT's: 18 public types, the names, members and
defaults of D1 to D20 (the STATUS's list re-read in the source). **The `=>` census (N02):** 31 occurrences in the 21
product files, every one named in `evidence/scope.out`: 17 expression-bodied members, 14 switch-expression arms
(`DeviceTokenException.MessageOf`, `Oxpd2CallbackHandler.CheckAnswer` and `Reparse`), 0 lambdas, 0 method-group
conversions; N02 and the landed `No_static_field_of_the_adapter_is_writable` are green at the head.

My probes (`evidence/GateProbeTests.cs`, 17 tests in the lane's test project in my clone only, never committed; own
fakes for vault, endpoint, device, sink and stream; the builder's test clock reused; all 17 green at the head except
where a finding is named; result lines in `evidence/probe-results-clean-run.txt`):

| H | My inputs | Result |
|---|---|---|
| H1, H2, D10 | G01: 23 wrong headers or serials (null, empty, `Bearer` alone, `Bearer ` alone, a tab, a no-break space, a leading space, trailing CR LF, 44 with `=`, 42, a full-width last letter, a `+` inside, `Token`, `Bearerx`, `Basic` with the value, another device's value, mine for another serial, the lower-case twin serial, a serial with a newline, 65 characters, a `/`, never issued, one flipped character) | each `Unauthorized`, empty body, no refusal fields, 0 read calls, sink 0; control `Bearer`, `bearer`, `BEARER`, `beARer` Answered 4 of 4 |
| H3 | G02: a vault whose read throws, with a well-formed header and with none; a stored hash of 31 bytes | `Unavailable` both, 0 read calls; 31 bytes `Unauthorized` (control: a 32-byte hash of the value verifies) |
| H4 | G03: `post`, `authentication`, a trailing `/`, `/PrePromptResult`, `GET` and `PUT` on handled paths, no leading `/`, a path under the other target, empty strings | `NotHandled` 10 of 10, 0 read calls |
| H5 | G03: `charset=utf8`, a quoted charset, a trailing `;`, a bare `;`, `application/json,text/plain`, a NUL, `application/problem+json`, `utf-16`, `foo=utf-8`, a space, `application / json` | `UnsupportedMediaType` 11 of 11, 0 read calls; `application/json;charset=utf-8`, ` APPLICATION/JSON ; CHARSET = UTF-8 `, `application/json` accepted |
| H6 | G04: bound 200: exactly 200 bytes in 1-byte reads with declared length 0; 201 in 7-byte reads with declared 10; declared `long.MaxValue`; declared -5; 5 MB with no declared length; an empty body; the default bound at 1048576 and 1048577 | Answered (read 200); `TooLarge` read 201; `TooLarge` 0 read calls; Answered; `TooLarge` read 201; `Refused Malformed`; Answered and `TooLarge` (read 1048577) |
| H7 | G16: a body that never ends, `BodyReadTimeout` 3 s on the test clock | not done at 2.999 s, `BodyTimedOut` at 3 s, sink 0 |
| H8 | G06: missing required, wrong type, duplicate key, 100000 `[`, trailing data, an escaped lone surrogate, a BOM, invalid UTF-8, a null required value, a body naming an unknown property after the synthetic value; `hidRead` and `usbClosed` in one envelope | each `Refused` with the parser's kind (`MissingRequired`, `WrongType`, `DuplicateKey`, `Malformed`); no result text or refusal path holds a body byte; the unknown property is ACCEPTED by the landed parser and reaches the sink (the parser's behaviour, not this lane's); both payloads together `Refused OutOfRange`, so a `usbClosed` cannot reset the guard inside a card read |
| H9 | G07 (cap 3): `long.MinValue` (the parser refuses it), 0 twice, `long.MaxValue` twice, a null context then an empty one, another serial on the same context, `ForgetDevice`, a read whose sink fails then the same sequence again | Stale on every repeat; null and empty contexts share one entry (as D15 says); serials independent; ForgetDevice resets; the cap drops one entry; a sequence handed to a failing sink stays consumed (the builder's named limit) |
| H10 | G08: a null task, a synchronous throw, the sink's own cancellation, a faulted `TimeoutException`, a plain object, the request echoed back, an answer missing a required property, an answer over `MaxAnswerBytes` 64 | `SinkFailed` 4, `AnswerInvalid` 4, no body returned |
| H11 | G14 and the cells: the caller's cancellation | `OperationCanceledException` (a `TaskCanceledException`) |
| H12 to H14, H18 | G15: a 401 then a refused refresh; statuses 403, 500, 407, 200, 400 | `NeedsRepair` (device 1, endpoint 2), the next send `NeedsRepair` with 0 device calls; statuses passed through with only the lazy refresh |
| H15 | **G10: 200 rounds x 16 concurrent sends that all meet a 401 (stated iteration count)** | rounds with more than one refresh after the lazy one 0; endpoint calls in flight at once max 1; every send ended 200 |
| H15 (beyond) | **G17 (deterministic): a request that ARRIVES during a refresh** | **2 endpoint calls (F1)** |
| H16 | G13, G14: an endpoint that ignores its token and hangs; a vault read failure; the caller cancelling during a refresh | `RefreshFailed` at the bound (F4 on what follows); `VaultFailed`; OCE for the caller and the waiter refreshes for itself (2 calls, the abandoned flight's rule) |
| H17 | **G11: 200 rounds x 8 concurrent first sends, a distinct access value and rotated refresh value per endpoint call**; a throwing `Put` | sends that saw a value before its rotated refresh value was written 0 of 1600; throwing `Put`: `VaultFailed`, 0 device calls, the old refresh value kept |
| H19 | G14: a lower-case `authorization` header added without validation; a 17-byte stream of unknown length over a bound of 16 | `InvalidArgument` both, 0 device and endpoint calls |
| H20, H21 | the builder's T10 and T11 (read; T10 shows `DeviceTokenException` unwrapped through a real `HttpClient` and a generated client) | green |
| H22 | the named limits, README `## Limits` read line by line | true at the head, F2, F4 and F6 to add |
| Callbacks race | G09: 50 rounds x 32 concurrent callbacks, half with a wrong credential; a rotation after them | Answered 800, Unauthorized 800, reads under a wrong credential 0; after `Issue` the old value fails and the new passes |

## 3. Mutants of my own on PRODUCT code (`evidence/mutants.py`; outputs `mutants.out`, `mutants2.out`)

Sixteen, none of them on the kit's list, each applied to exactly one occurrence, the lane's test project built and run
(the builder's 43 cells plus my 17 probes), reverted to the original bytes and proved by `git diff --quiet` rc 0:

| Mutant | Edit | RED (by assertion) |
|---|---|---|
| mMediaParam | the charset value no longer checked | B03, G03 |
| mOpNoMethod | the method check reduced to non-null | G03 only (F5) |
| mNoRepairMark | the second 401 no longer marks the device | T03 |
| mForgetKeepsAccess | `Forget` keeps the held bytes | T11 |
| mUsbClosedNoReset | `usbClosed` no longer resets its context | U01, U02, U03, G07 |
| mCapOff | no eviction at the cap | U03 |
| mRetryHeaders | the retry drops the request's headers | T02 |
| mVaultAsStranger | a throwing vault read reported `Unauthorized` | A05, G02 |
| mSignoutAnswer | any answer to `signoutNotification` accepted | S03 |
| mRefreshNoBound | the refresh's time bound removed | T05 (by its guard), G13 |
| mGrantNoCheck | the grant's byte check removed | G12 only (F3) |
| mRotateNoStore | a rotated refresh value not written | T07 x2, G11 |
| mSchemeCase | the scheme compared case-sensitively | A02, G01 |
| mKeyNoSerial | the guard's key without the serial | U02 |
| mReadNotCancelled | the read not cancelled at its bound | B05 (the stream's cancellation wait) |
| mFailReuseOff | a waiter no longer reuses a failed flight's error | NONE: survives (F5; a behaviour no cell pins) |

15 of 16 red by assertion; the survivor is a gap of claim, not of safety. (My first mMediaParam edit did not compile
and is not counted; it was re-made as above.) After the last revert the lane's project ran 60 of 60 green and the
whole suite 1234 failed 0; `git status --porcelain` 0 lines; the probe file moved to
`/private/tmp/b1868-gate/_quarantine/probe-final/`.

## 4. Suite and hosted

- Head, through the lock (`evidence/suite-summary.txt`): locked restore rc 0 (nothing fetched: no fetch line, closed
  proxy; porcelain 0 after), build `0 Warning(s)` `0 Error(s)`, whole suite `total: 1234`, `failed: 0`,
  `succeeded: 1230`, `skipped: 4` (the four Windows tests of the secret store by name, none of this lane). After the
  probes and mutants: again 1234 / 0 / 1230 / 4.
- Hosted run `44896274969` of 523204dd read by GET (`hosted.py`, sha256 `e73339f3...`, the same as
  `fleet/state/s304/d1835/gate/hosted.py`) with `--total 1234 --rules 402 --skipped-linux 4 --skipped-windows 19
  --unit 60 --floor 60`: `HOSTED 523204dda0042eab2f2483257b7b0f29706c68fd: PASS` (four jobs success, attempt 1, every
  step success or skipped; linux and windows `total: 1234` twice each, `failed: 0`, skipped 4 / 19, guards 10 and 11;
  rules `Ran 60 tests`, `UNIT-TEST FLOOR: ran 60, floor 60`, `RULES: clean (402 files)`; secret-scan both
  PLANTED-CONTROL lines, `NEUTRAL-SCAN: ... objects of this commit not among them 0`, `no leaks found` x3). Control:
  the same with `--rules 401`: `FAIL 1`. Windows skipped lines naming a test outside `Datasec.Suite.Secrets.Tests`: 0.
- By GET at 22:14: main = 8ae5e08c, the branch = 523204dd, `compare main...head` ahead 1 behind 0, 34 files; open pull
  requests 0; open code-scanning alerts on main 0.

## 5. The seat's deviations

1. N03's first version as an XML comment: accepted (the lock file untouched; the reds were by text, which is what N03
   and the landed project-file test read; the file is T1 byte for byte at the head).
2. The stray `rm` aimed at `/dev/null`: records only (no effect the STATUS could show; nothing of the lane changed;
   I cannot measure the seat's machine at that time).
3. The grant's byte check: accepted, as Tuesday ruled, with F3.
4. A throwing body stream passes out: Minor (records), F2. No harm path found.
5. A01 and A03 red by the throwing stubs and by the mutants mStoreClear and mEquals: accepted (both cells assert what
   the kit says; my mVaultAsStranger and mSchemeCase show the credential cells bite).

## 6. CodeQL

CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C# proof, and no analysis has run on this
branch (`check runs beside the four: 0`). Hand rows: the product writes no file, log, console or exception text with
a value; the test code writes nothing to a file or console; no regular expression is built from input. No likely
alert seen; UNMEASURED.

## NOT TESTED

- Timing of the credential check (fixed-time comparison read in the source and pinned by A03's seam, not timed): the
  second reader's D9.
- Windows locally (the hosted `windows` leg is its only proof); any device, simulator or real token endpoint; the host
  binding of the vault and the endpoint; the R5 hash half.
- The builder's 43 cells were read in part (their asserts listed by program; T02, T03, T04, one B05 and one T05 read whole), not
  line by line; the generated code and the landed contract tests were not re-read beyond the lines D2 names (they have
  no diff).
- No landing texts are written: this reader's verdict is NO GO.
