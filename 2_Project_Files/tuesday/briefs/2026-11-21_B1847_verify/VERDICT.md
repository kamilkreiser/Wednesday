GATE B1847: NO GO @ f2b237d on main 0804860

Gate G2 (Opus 5.5, in-session), round 1 of 2. This gate checks OXPd 2 lane A, WP3.8, the shared Graph HTTP layer
(kit B1832, seat X14). Head `f2b237d08565fbb07ad5a285c37b6b93d3cecc39` on `b1832/wp38-graph-layer`, one commit, one
parent `5e36d8dca42966395ea3dd014c7f788409eb585f`. Main is now `0804860b8993f6d7fd393cb64c44afcd2f9c8f05` (pull
request 7, one parent 5e36d8dc). Measured 2026-11-21 from 18:15:49 to 18:34:40 AEDT (clocks by `date`).

**BLUF.** NO GO, because of ONE Major. The tier stays **G2**: I found no kept token, no persistence and no forbidden
reach, so this is not G1.
- **The Major (F1).** A page or an upload answer can carry a JSON string that is not valid UTF-8, or that holds a
  lone surrogate escape (`\ud800`). Such a string in `@odata.nextLink`, `@odata.deltaLink` or `nextExpectedRanges`
  makes `JsonElement.GetString()` throw `InvalidOperationException`, and that exception leaves the library. This
  breaks the kit's closed list of failure kinds (C9). The exception's inner text also prints the offending body byte,
  for example `bytes [FF] at index 33`, which breaks C7's "no body byte".
- **Why the builder's tests miss it.** The builder's C9 random run only ever encodes ASCII text, so it cannot reach
  this. My own fuzz (seed 20261847) hit it 752 times in 20,000 paging conversations.
- **Everything else holds**, each checked by my own run:
  - Scope is exact.
  - The token goes only to the base origin: 34 hostile next links, 12 off-origin addresses, an upload on another host
    and 60,000 fuzz conversations, with 0 leaks.
  - The planted token, path, body and upload-credential words appear 0 times in a log with NO deny-list and in
    112,537 exception and result texts.
  - Retries, waits and the body read are bounded, and cancellation works at 6 wait points.
  - Build: 0 warnings, 0 errors. Suite: 1070, 0 failed.
  - The merge with main 0804860b is clean, and the merged tree builds and runs 1075, 0 failed.
  - The hosted run passes.
  - All 9 of my mutants go red by assertion.

**In plain words: the branch cannot be landed yet. One fix round must first make a malformed text in a network
answer end as the layer's own "malformed response" error. Main moved, but the branch merges with it cleanly. After
the fix, the pull request's checks must run against the current main, where the expected total is 1075 plus the fix
round's new tests.**

## How I worked

- **Read clone.** `/private/tmp/b1847-gate/clone`, made by the kit's `clone.py` in mode `draft` (push URL
  `invalid://no-push`, no identity). All eight tool hashes equal THE TOOLS (8 of 8).
- **Write verbs.** The workspace hook refuses git write verbs outside the session scratchpad. So every verb that
  writes objects, every build and the mutants ran in clones of the read clone inside the session scratchpad
  (`.../scratchpad/b1847/{head,merge,probe,mut}`, push URL `invalid://no-push`). The one scratch merge commit was
  made there with a throwaway identity and is never pushed.
- **One runner for every dotnet job.** All 25 jobs went through the kit's `heavy.py`, unchanged (sha256
  `31adedc8...`). It reads load first, takes the lock by `mkdir` of exactly `<project>/.tools/wave1-heavy.lock.d`
  with `owner.txt`, runs one command under a time bound, and MOVES the lock into
  `/private/tmp/b1847-gate/_quarantine/locks/` (25 folders there). Lock waits were at most 2 and load1 ran 1.6 to 7.0.
  After my last job, no lock folder is left in `.tools`.
- **Closed proxy.** Every job runs behind the runner's closed proxy (127.0.0.1:9). Restores carry
  `-p:NuGetAudit=false`, because the closed proxy refuses the SDK's audit request.
- **Where things are.** Logs in `/private/tmp/b1847-gate/logs/`. My probe is `/private/tmp/b1847-gate/probe/GateProbe.cs`
  (sha256 `c2a75237...`). Its report and texts are in `/private/tmp/b1847-gate/probe-out/`.
- **Not touched.** I did not read, list or hash `Source_Documents/`.

## Findings

| # | Severity | Finding | Recommendation |
|---|---|---|---|
| F1 | **Major** (blocks the merge) | **An exception outside the failure kinds leaves the layer on malformed text in a network answer.** `GraphClient.cs:696` (`link.GetString()` for `@odata.nextLink`), `:699` (`delta.GetString()` for `@odata.deltaLink`) and `:352` (`range.GetString()` in `FirstExpectedStart`) catch only `JsonException`. A string holding invalid UTF-8 (`FF FE`, the overlong `C0 AF`) or a lone surrogate escape (`\ud800`, `\udfff`) makes `GetString` throw `InvalidOperationException` ("Cannot transcode invalid UTF-8 JSON text to UTF-16 string" / "Cannot read incomplete UTF-16 JSON text as string with missing low surrogate"). Stack: `GraphClient.ReadPage` <- `ReadPageLogged` <- `WalkAsync`. It reaches the caller of `GetPagesAsync` and of `UploadAsync`. Its inner `DecoderFallbackException` text holds a body byte (`Unable to translate bytes [FF] at index 33`), so C7 is broken too. No failure outcome is logged on that path. **The builder's C9 cannot see it**: `RandomConversationTests.Body` builds every body by `Encoding.UTF8.GetBytes` of ASCII text. So the STATUS claim "N9 pass: each ends in a result or GraphCallException" holds for that generator only, and my numbers contradict it as a property: 7 directed inputs, plus 752 of my 20,000 fuzz walks (381 surrogate, 371 UTF-8). | In the fix round: (1) treat `InvalidOperationException` from `GetString` (or decode with a strict check) as `MalformedResponse` in `ReadPage` and `FirstExpectedStart`. For a deltaLink, `MalformedResponse` is the safe default; returning null as reading 3(i) does for a non-string is the alternative. That is Tuesday's choice. (2) Add N4/N7 cells: invalid UTF-8, overlong UTF-8 and lone-surrogate escapes in nextLink, deltaLink and each `nextExpectedRanges` element. (3) Extend C9's body generator with raw non-UTF-8 bytes inside strings and `\ud800` escapes. (4) Red first against the head. |
| F2 | Minor (text) | Two code comments state Graph or cloud behaviour with no source and no UNMEASURED: the `UploadAsync` summary in `GraphClient.cs` ("the session address is pre-authorised"; the source is report A11 line 238, RELAYED), and `GraphCloud.cs` `Gcc` ("same Graph host as Commercial"; the source is report A1 line 363). The class summary of `GraphClient` does say that how Graph answers is not measured here. | Add the source or "assumed" to the two comments in the fix round. |
| R1 | Records | Reading 3(l): `MaxThrottleRetries` and `MaxNextLinkLength` have no upper limit, while `MaxPieceRetries` stops at 1000. I measured `MaxThrottleRetries = 20000` with `Retry-After: 0` forever: **20,001 sends** in one call. The bound is the option alone. Only a caller can set it, and the default is 3. | Optionally cap it like `MaxPieceRetries` in the fix round. Not a blocker. |
| R2 | Records | The layer gives the token source no time bound of its own. A source that never answers holds the call until the CALLER cancels (measured: it ends with a cancellation at the caller's 400 ms). Report A11 line 95 says the Workpath app waits at most 10 s for a new token (RELAYED). | For whoever writes the adapter over lane D's broker: bound the broker call there. |
| R3 | Records | Redirects and the caller's `HttpClient.DefaultRequestHeaders` are outside the layer (named limit N11). With my fake handler a 302 to another host ends as `HttpStatus`, and nothing is followed. Whether a real `HttpClientHandler` (which follows redirects by default) removes `Authorization` on a cross-host redirect is UNMEASURED here. | For the host wiring: build the Graph `HttpClient` with automatic redirects off, and with no default `Authorization`. |
| R4 | Records | The FOR TUESDAY 1 point, the token as a .NET `string` that cannot be wiped: **a records and design point, not a finding.** The G2 boundary is "no token kept after the call", and it holds (C8, my own walk). `HttpClient` takes a header value only as a `string`, so any bearer sent through it exists as a managed string for each request. A `GraphToken` over a byte buffer would move that copy; it would not remove it. Being able to wipe is in no rule of the kit. | Record it for the adapter's design, beside lane D's byte token. |
| R5 | Records | My mutant mNoTotalWait is caught by ONE test (`ThrottleTests.TheTotalWaitCapEndsTheCall`). The upload's total-wait cap (reading 3(f)) has no cell of its own. At the head it holds: with 1000 piece retries allowed and a 20 s `Retry-After` on every answer, 4 requests and a total wait of 60 s. | Add an upload total-wait cell when convenient. |
| R6 | Records | Builder's deviation 1: one `sed -i` on its own untracked lane scratch file. This is process only. | None beyond the record. |

## Item 1: scope (holds)

- **Refs** (by GET, 18:15:58). The branch is `f2b237d0...`, one parent `5e36d8dc`. Main is `0804860b...`. `compare
  main...head` reads diverged, ahead 1, behind 1, 40 files, merge base `5e36d8dc`. The head's four check runs
  (`linux`, `windows`, `rules`, `secret-scan`) are each completed success. The repository is `.private` true. There
  are 0 open pull requests.
- **Changed paths.** `git diff --name-status 5e36d8dc f2b237d0` has 40 rows: 39 `A` and 1 `M`. The one `M` is
  `Datasec.Suite.slnx`. Every `A` row is under `src/Datasec.Suite.Graph/` (17) or `tests/Datasec.Suite.Graph.Tests/`
  (22). There are 0 rows outside those two folders.
- **Solution file.** numstat 2 / 0. The two lines are Graph after Core and Graph.Tests after Core.Tests, so both
  folders stay in ordinal order.
- **Forbidden paths.** `git diff --quiet` over `Directory.Packages.props .github build README.md global.json
  Directory.Build.props NuGet.config .editorconfig .gitignore contracts src/Datasec.Suite.Logging` gives rc 0. The
  control (the same verb over `Datasec.Suite.slnx`) gives rc 1. The only lock files in the diff are the two new ones.
- **Project files.** The two csproj files are byte-equal to T2 (`dbad0118...`) and T3 (`d78f9f40...`), each
  extracted by program from the stamped kit. Block R extracted gives `7cbf0d4e...`, equal to FACT 7. The product
  project holds **one `ProjectReference`, `../Datasec.Suite.Logging/Datasec.Suite.Logging.csproj`**, and no
  `PackageReference`.
- **Binaries and keys.** 0 binary numstat rows, and 0 files with a key, certificate or binary extension.
- **Gitleaks** (8.30.1, the workflow's four options), over the 40 added files copied under neutral names: rc 0, `no
  leaks found`. The control (a provider-shaped value built from two halves) gives rc 1, `leaks found: 1`.
- **ASCII and words.** The 3364 added lines (lock files excluded) have 0 lines outside printable ASCII. `words.py`
  (control `CONTROL FIRED: 13 of 13`) over the added lines and the commit message gives `WORDS: clean (2 files)`.
  Each lock file alone gives `seat ids 2`, which equals its count of `linux-x64|win-x64` (2), and nothing else.
- **Authority.** `owner|decid|approv|ruled|ruling|instruct|coordinator` and the ban-list names count **0** in the
  added lines and the commit message (control: `token` counts 328). No text says the product owner decided anything.

## Item 2: the token boundary (holds; F1 is a different defect)

- **C8, my own reflection** over every type of the built assembly (`probe-report.txt` lines `G ...`):
  - Outside compiler-generated types, no field is of type `GraphToken` or assignable to `IGraphTokenSource`.
    `GraphToken`'s only field is its `string` backing field.
  - Every static field outside generated types is `readonly`: `GraphOptions.LongestWait`, `RetryAfterGrammar.Days`,
    `RetryAfterGrammar.Months`.
  - Inside generated types, the token-typed fields are instance fields of async state machines only (the kit's
    measured exclusion). None is static.
  - The referenced assemblies are `System.*`, `Serilog` and `Datasec.Suite.Logging`. None is `Microsoft.Identity*`,
    `Microsoft.Graph*`, `Azure.*` or `Datasec.Suite.Sessions`.
  - After a 401-then-200 call, the client instance's five fields hold no token and no source.
- **Authorization only to the base origin** (my handler records every request with its `Authorization`).
  - **SendAsync**: 12 off-origin addresses are refused with `ArgumentException` and 0 requests: another host, `http`,
    port 444, user info, `host@other`, `//other`, a suffix host, `file:`, a trailing dot, backslash forms and
    `#@`. `\\other.example.test\x` resolves to `https://graph.example.test//other.example.test/x`, on the base
    origin.
  - **Next links**: 34 hostile and edge links, among them another host, `http`, another port, user info,
    `graph@other`, a Cyrillic look-alike, punycode, IP literals, `%2e` and `%40` hosts, `file:`, `javascript:`,
    `ftp:`, relative, `//`, backslash, 8193+ characters and the 8192 bound. **0 requests carried a token off the
    base origin.** Each was followed exactly when it is an absolute https URL on the base host and port with no user
    info.
  - **Upload**: an upload on another host carrying `tempauth=<planted>` across 5 requests (PUT, PUT, GET, PUT, PUT)
    sent **0 Authorization headers**.
  - **Fuzz**: across all 60,000 conversations, 0.
- **No token in a log or an exception text.** A Serilog file logger with **no deny-list** at Verbose wrote 39 MB of
  events. All texts were kept: 112,537 exception messages, `ToString()`s and result texts. They hold **0** of: the
  token, the new token, the path word, the body word, the upload credential, a throwing source's message word and
  `Bearer`. The control is that the base host is found 161,120 times in the log. (F1's inner exception holds a body
  byte value, not a token.)
- **FOR TUESDAY 1** (the token as an unwipeable string): R4, a records and design point.
- **Tier.** No kept token, persistence or forbidden reach, so the lane stays G2.

## Item 3: network-answer parsing (fails on F1 only)

These are my own inputs, against my own oracle where a rule decides the outcome.

- **Retry-After**: 58 header cases, every one equal to my independently written oracle (58 of 58). They cover
  seconds, HTTP dates, negative, `+`, fractions, trimmed spaces and tabs, empty, 9 and 10 digits, `0000000030` (over
  cap by the digit rule), 20 digits, 100,000 nines and 100,000 letters, dates at exactly 30 s and at 31 s,
  lowercase, `UTC`, a double space, years 9999 and 0001, 29 February in a leap and a non-leap year, hour 24, minute
  60, second 60, Arabic-Indic and full-width digits, NBSP, CRLF, NUL, `Infinity`, `NaN`, `0x10`, `1e3`, an absent
  header, and two lines (`5 | 6`, `5 | ""`, `"" | 5`, date | 5).
  - The header on the content headers is refused by the framework, so the client used the fallback.
  - The total cap holds: waits of 30 and 30, then `Throttled`, with 3 sends.
- **Next links and delta links**: 34 links, 2 loops (A to A, 1 request; A to B to A, 2 requests), and an endless
  list of distinct links (`PagingTooManyPages` at 7 of 7). There were 28 page shapes:
  - **Escape (F1), 5 shapes**: invalid UTF-8, overlong UTF-8 and lone surrogate in nextLink; invalid UTF-8 and lone
    surrogate in deltaLink.
  - Failure kinds (`MalformedResponse` or `PagingForeignAddress`): nextLink a number, an object or an empty string;
    depth 65 and 100,000; a BOM; trailing data; two objects; a comment; a null value; an empty body; `null`;
    UTF-16.
  - Value: deltaLink a number, object, array or `true` (returned as null, reading 3(i)); an invalid UTF-8 item or
    property name; depth 64.
  - Duplicate nextLink keys: the last one is what is checked and followed, both orders safe.
- **Upload `nextExpectedRanges`**: 28 answers plus 3 sequences.
  - **Escape (F1)**: invalid UTF-8 and a lone surrogate.
  - `MalformedResponse`: empty, missing, null, a string, numbers, `abc-`, `-5-`, no dash, two dashes, a space, `+`,
    an Arabic digit, 19 digits (both forms), 40 digits, start equal to the length, start beyond the length, a bad
    second element, deep, not JSON, empty.
  - Proceeds: 18 digits; overlapping (the first is used); end before start; a second element beyond the length;
    backwards to 0.
  - Sequences: the same start forever gives `UploadNoProgress` at 6 requests. Two starts alternating forever give
    `UploadNoProgress` at **36 = the upload bound**. A final answer past the body bound gives `ResponseTooLarge`.
- **Body sizes** (`MaxResponseBytes = 1000`):
  - 1000 bytes gives a value, and 1001 gives `ResponseTooLarge`.
  - An endless body gives `ResponseTooLarge` after **1001 bytes read** from the stream.
  - `Content-Length: 10` over a 50,000-byte body: 1001 read.
  - An endless body on a 429 has **0 bytes read**: non-2xx bodies are never read.
  - Endless page and endless upload answer: 1001 read each.
- **Handler failures**: 11 cases x 3 entry points (33 runs), all inside the failure kinds:
  - `Transport`: `HttpRequestException`, `IOException`, `InvalidOperationException`, a null response, a faulted
    task, a body stream that throws.
  - `Timeout`: `TaskCanceledException` not from the caller.
  - `HttpStatus`: status 999, status 100, and a 302 to another host (not followed).
  - Value: a garbage `Location` with two `ETag` values.
- **Fuzz, seed 20261847**: 60,000 conversations, 20,000 per entry point, with 69,028 requests in all. The inputs are
  random statuses, Retry-After values, bodies, links, ranges, token-source failures and options.
  - **0 hangs, 0 over a request bound, 0 Authorization off the base origin or on an upload, 0 waits past
    `MaxTotalWait`.**
  - **Other exceptions: 752, all F1** (paging: 381 surrogate, 371 UTF-8). SendAsync and upload: 0. The upload's
    random bodies had no invalid-UTF-8 range string; the directed case above shows F1 there too.

## Item 4: retry and time bounds (holds)

- 429 forever with no header: 4 sends and waits of 1, 2 and 4 s, then `Throttled`.
- 503 with 30 s and 10 retries allowed: 3 sends and 60 s in all, then `Throttled`.
- 401 forever: 2 sends and 1 refresh, then `Unauthorized`. The sequence 401, 429, 401: 1 refresh, then
  `Unauthorized`. The sequence 429, 401, 429, 429, 200: a value after 5 sends and 1 refresh.
- Upload 503 forever: 6 requests (PUT, then 5 GETs), waits of 1, 2, 4, 8 and 15 s, then `Throttled`. With 1000
  piece retries allowed and a 20 s `Retry-After`: 4 requests and 60 s.
- **Cancellation, the caller's token cancelled at 150 ms** at six points: during a send's wait (the default delay
  over the system clock, `Retry-After: 30`), during a page-2 wait, during an upload-piece wait, inside an injected
  delay, inside `GetTokenAsync`, and inside the send. Each ends with `OperationCanceledException` in 150 to 160 ms.
  An attempt that never answers ends as `Timeout` at 202 ms (`AttemptTimeout` 200 ms).
- **Readings 3(a) to 3(l)**:

| Reading | Ruling | What shows it |
|---|---|---|
| (a) | accept | `Fallback(throttleRetries)`; E1 waits 1, 2, 4 |
| (b) | accept | `RetriesSpentKind`; upload 503 forever gives `Throttled` |
| (c) | accept | `GraphClient.cs:256-265` |
| (d) | accept | `pieceRetries = 0` on a 202 (`:244`); alternating starts are still bounded by the request bound (36) |
| (e) | accept | `:242` |
| (f) | accept (R5) | the upload's total wait is 60 s at 1000 retries |
| (g) | accept | `:236`; a Graph completed-session read is UNMEASURED |
| (h) | accept | `:520` |
| (i) | accept for non-strings; an invalid string escapes | F1 |
| (j) | accept | `CheckHeaders` |
| (k) | accept | `LogAttempt` and `LogOutcome` |
| (l) | accept | R1 |

## Item 5: build, suite, merge, hosted (holds)

- **Head**, with a `CI=true` locked restore and `-p:NuGetAudit=false`: rc 0. **Nothing was fetched**: the runner's
  closed proxy (127.0.0.1:9) would fail any fetch, locked mode refuses drift, the log holds 0 lines naming
  `http(s)://` or an `NU1xxx` code, and `git status --porcelain` shows 0 lines afterwards. Build: `0 Warning(s)`,
  `0 Error(s)`. `dotnet test -c Release --no-build`: **total 1070, failed 0, succeeded 1066, skipped 4** (the
  secret store's 4 Windows-only tests).
- **Merge with main 0804860b.** `git merge-tree --write-tree 0804860b f2b237d0` gives **rc 0, CLEAN**, tree
  `43208041...` (332 files).
  - Main's side changes 11 paths under `contracts/oxpd2/generator`, `Generated/` and `tests/Datasec.Suite.Contracts.Tests`.
    It does **not** touch `Datasec.Suite.slnx`: blob `2ca30a04` at both 5e36d8dc and 0804860b.
  - The merged `Datasec.Suite.slnx` is the head's blob `18c71925`: numstat against main is 2 added, 0 removed.
  - The merged tree, built in a scratch commit: locked restore rc 0, build `0 Warning(s)` `0 Error(s)`, **total 1075,
    failed 0, succeeded 1071, skipped 4**.
  - **The five extra** are what pull request 7 added over 894. Main's own push run, read by `hosted.py`, shows linux
    and windows `total: 899` and `HOSTED 0804860b...: PASS`. So 894 + 5 = 899, and 1070 + 5 = 1075.
  - Lanes in flight: merge-tree of the head with `b1831/wp15-token-broker` (70c1fad5) and with
    `b1836/r5-hp-inputs-exemption` (28d2852d) is clean both times (rc 0).
- **Hosted run of f2b237d0 by GET** (`hosted.py`, unchanged, `--total 1070 --rules 330 --skipped-linux 4
  --skipped-windows 19`): run 44878922385, attempt 1. Four jobs success, every step success.
  - linux: `total: 1070` x2, `succeeded: 1066`, `skipped: 4`, `failed: 0`, `0 Warning(s)`, `0 Error(s)`,
    `GUARD: clean (10 files)`.
  - windows: `total: 1070` x2, `succeeded: 1051`, `skipped: 19`, `GUARD: clean (11 files)`.
  - secret-scan: both PLANTED-CONTROL lines, `no leaks found` x3, `objects of this commit not among them 0`.
  - rules: `Ran 53 tests`, `UNIT-TEST FLOOR: ran 53, floor 53`, `RULES: clean (330 files)`.
  - Last line `HOSTED f2b237d0...: PASS`. Control: `--skipped-linux 5` gives `FAIL 2`.
- **Code scan.** It has NOT run on this branch: 0 analyses on the ref, and the push run carries the four ci jobs
  only. It runs on the pull request. Main reads 0 open code-scanning alerts (GET 18:33:50), and main's own
  `Analyze (csharp)` is now success. `CodeQL csharp: NOT RUN (cannot extract on arm64); hosted CodeQL is the only C#
  proof.` No JavaScript or Python is added.

## Item 6: mutants (independent; mine, in my mut clone)

Each mutant was applied by an exact one-place replacement (`/private/tmp/b1847-gate/scratch/mutate.py`), run as ONE
job of `dotnet test -c Release --no-restore` (build and the whole suite, through the runner), reverse-applied, and
proved by `git diff --quiet` with rc 0.

| Mutant | What | RED by assertion | Undo |
|---|---|---|---|
| mKeepTok | a field `GraphToken? _keptToken` on `GraphClient`, assigned each call | 1: `BoundaryTests.NoTypeOfTheLibraryKeepsATokenOrASource` (`Assert.Empty`) | rc 0 |
| mAuthGet | `Authorization` on the upload STATUS READ (GET) only | 1: `UploadTests.ARetryReadsTheStatusAndResumesFromTheNamedRange` (`Assert.All`/`Assert.Null`) | rc 0 |
| mAuthPutLast | `Authorization` on the LAST upload piece only | 2: the same test and `ThreePiecesWithExactRangesAndNoAuthorization` | rc 0 |
| mCrossOrigin | a next link followed when it is any https URL (host, port and user-info checks dropped) | 3: `ForeignLinksAreNeverRequested` (another host, port 8443, user info) (`Assert.Single`) | rc 0 |
| mNoTotalWait | the `MaxTotalWait` check removed from `TryPlanWait` | 1: `ThrottleTests.TheTotalWaitCapEndsTheCall` (`Assert.Equal`) (R5) | rc 0 |
| m401Twice | `refreshed = attempts >= 2`, so 2 refreshes per call | 3: `TheSameTokenAgainEndsAtTheSecond401`, `EveryAnswer401GivesOneRefreshAndTwoSends`, `FiftyConcurrentCalls...` | rc 0 |
| mNoThrottleCount (mine) | the `MaxThrottleRetries` check removed | 5: `TheFallbackDoublesUpToItsCap`, `ThrottleThatNeverClears503WithHeader`, `NoRetriesAllowedMeansOneSend`, `ThrottleThatNeverClears429`, and `AZeroWaitStillCountsAsARetry`, which ends on its 10 s guard by a type assertion | rc 0 |
| mLinkLength (mine) | the `MaxNextLinkLength` check removed | 1: `ForeignLinksAreNeverRequested` (the 8193-character link) | rc 0 |
| mCapWaited (mine) | `Retry-After` over `MaxRetryAfter` is waited | 5: `EachRow` R04, R11, R16; `AWaitOverTheCapIsNotWaited`; `EachRowThroughTheClient` R04 | rc 0 |

- **One slip, corrected.** The first undo of mNoThrottleCount failed (my pattern matched twice), so the next two
  jobs ran on top of it. I restored the file by an exact replacement, proved `git diff --quiet` rc 0, and re-ran all
  three. The table holds the clean re-runs.
- After the last undo the work tree is clean, and the suite reads 1070, failed 0, succeeded 1066, skipped 4.
- No mutant of mine reaches F1: the suite is green at the head WITH that defect.

## Item 7: the deviations

| # | Ruling | The line that proves it |
|---|---|---|
| 1 | ACCEPTED, records R6 | STATUS DEVIATIONS 1: an untracked file under `<lane>/scratch/`, outside the repository; the tree is unaffected (item 1) |
| 2 | ACCEPTED | my mutant jobs ran the same `--no-restore` form after a locked restore; the closed proxy refuses the audit (NU1900 without `-p:NuGetAudit=false`) |
| 3 | ACCEPTED as readings, each ruled in item 4; (i) is touched by F1 | `GraphClient.cs` lines cited in the table above |
| 4 | ACCEPTED | `NoSideDoorTests.cs`: "Every exception's text is kept for the scan, whatever its type (control C9 judges the type)." The kit's rule is to fix a TEST that does not fail by its own assertion |

## STATUS claims, graded

| Claim | Grade |
|---|---|
| local total 1070 (894 + 176), skipped 4 | true (mine) |
| hosted PASS, both legs 1070, RULES clean (330) | true (mine) |
| only shared file `Datasec.Suite.slnx`, 2 lines | true |
| no package, one ProjectReference | true |
| C8 / no token kept | true (my own walk) |
| nine mutants red | true in kind (mine: 9 of 9 red, different forms) |
| N9 "each ends in a result or GraphCallException" | **false as a property** (F1); true for the builder's generator only |
| restore fetched nothing | true (mine) |
| red-first counts (144 failed) | not shown (not re-run) |
| nocopy | not re-run by this gate (it reads `Source_Documents/`) |

## NOT RUN / NOT TESTED

- Anything on Windows: the hosted windows leg is the only proof.
- `dotnet publish` and the release guard locally (I read the hosted GUARD lines).
- CodeQL for C#: it cannot extract on arm64, and the pull request's scan has not run.
- A real `HttpClientHandler` with sockets: redirects, proxies, and real decompression (R3). No listener was started.
- Any real Graph answer or tenant.
- `nocopy.py` and `repo_rules.py --source-documents`: they would read `Source_Documents/`.
- The builder's own nine mutants in their exact form (mine are different forms of the same mutants).
- The red-first state against the stubs.
- Concurrency beyond what the builder's 50-call test and my fuzz exercise. My fuzz ran its conversations one after
  another.
- **Texts for the landing** (`pr-title.txt`, `pr-body.md`, `squash-*.txt`, `landing.txt`): not written, because the
  verdict is NO GO. Item 8 asks for them on GO or GO WITH FINDINGS only. They belong to the round-2 gate.
