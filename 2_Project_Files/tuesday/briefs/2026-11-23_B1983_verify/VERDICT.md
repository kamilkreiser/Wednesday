GATE B1983: GO WITH FINDINGS @ ea0df6c on main e193fb6

Gate G1 (security surface: network, TLS trust), round 1 of 2 of lane IP, one Opus reader (claude-opus-5-5),
in-session, read-only. OXPd 2, lane IP, kit B1972 (seat X46; Q1 = a in words at stamp S4, Q2 to Q7 the defaults, each
the coordinator's, not the product owner's): `HttpIppTransport` in the new assembly `Datasec.Suite.Jobs.Transport`.
Head `ea0df6c0399cedbaecc8ff385c2981f42383d9e6` on `b1972/ip-https-transport`, ONE commit, one parent `da8d64a8`.
Read and measured 2026-11-23 12:45 to 13:06 AEDT in my own scratch `fleet/state/s316/g1983/`: `clone` (clone.py
draft: push URL `invalid://no-push`, no identity; detached at the head), worktrees `red` (BASE + `1-red.diff`, then +
`2-fix.diff`), `phead` (head + my probe, quarantined after), `mta` (TA's head + IP), and `clone2`/`mmain` (a second
draft clone at 13:01, main `e193fb63` + IP, per ADDENDUM-1). Every dotnet job through the kit's `heavy.py` (sha256
`31adedc8...`) and the wave lock, one at a time (lock waits 0 to 16; no other holder's lock touched). Origin by `gh
api -X GET` under the project GH_CONFIG_DIR. No write to the project, GitHub or Jira; no push, no pull request, no
re-run; nothing deleted (probe file and scanner control moved to `g1983/_quarantine/`). No network beyond the origin
reads and the tests' 127.0.0.1.

**BLUF.** The head is BASE plus the two frozen patches byte for byte (`red` after both: `write-tree` `0dda2475` = the
head's tree; THE CODE 10 of 10 per column; patches and tools 10 of 10 by sha256, in my copy and the seat's). Red first
at BASE: 1839 / 18 failed, all `HttpIppTransportTests` N02 N03 N04 N05(2) N06(6) N07 N08 N09(3) N13 N14, each by an
xunit assertion; Jobs executable `Total: 152, Failed: 18`. 10 of 10 mutants MATCH, 10 undone, rebuilt (dll later than
the last undo), green again 1839 / 0 / 1835 / 4. The pin check holds: one callback in the diff, null certificate
false, 64-hex pin required, leaf DER hash in fixed time, chain unused; no request reaches the stub after a refused
handshake (N03, N04, my P01 across pins after three good sends). Three sends = three connections (P02). Hosted run
45092918591: linux 1835, windows 1818, 0 `failed Datasec.` lines (the first TLS listener on hosted legs: green); the
one hosted2.py FAIL is GitHub's stuck `rules` status field, and I agree it is GitHub's record, not the run (its log
counted by GET: every line as required). **Merge with main of the moment (`e193fb63`, after TA and L1): no conflict,
tree `97c8b349`, 1904 / 0 / 1900 / 4, RULES 587 = main's 1874 + 30 and 580 + 7, measured.** Two Minor findings;
nothing blocks the landing.

## FOUND

1. **Minor (a build the tests do not cover): the transport project is compiled as Debug by every Release build of the
   solution, locally and on both hosted legs.** It is not in `Datasec.Suite.slnx` (Q2), so the solution build reaches
   it only through the Jobs test project's `ProjectReference`, and MSBuild builds a project outside the solution with
   its default configuration. MEASURED: `red-build.log:27`, `head-build.log`, `mmain-build.log` (on e193fb63 too) and
   the head's hosted logs `job-linux.log` / `job-windows.log` all print `Datasec.Suite.Jobs.Transport -> .../bin/Debug/
   net10.0/...` while every other project (Jobs included) prints `bin/Release`; the Release test executable then loads
   the Debug transport. (The mutants run builds the test project directly and so built it Release: both configurations
   were exercised locally; CI exercises Debug only.) Effect: no security hole and no false test result found; the
   Release assembly of the transport is never built or tested by CI, and the kit's D1/Q2 premise ("the slnx line is
   hygiene only, an IDE's solution view") is false. Fix (the coordinator's order): the transport's solution line in the
   next lane that owns `Datasec.Suite.slnx` (L1 has landed, so it is free), with the hosted `Jobs.Transport ->` line
   then reading `bin/Release`.

2. **Minor (two sentences of repository text the code does not keep; `<project>/CLAUDE.md`, no false sentence in
   repository text).** (a) `IppTransportException.cs`, `ConnectFailed`'s comment: "the connect bound passed". MEASURED
   (probe P06): a peer that accepts TCP and never answers the TLS handshake, `ConnectTimeout` 1 s, ends in 1002 ms as
   `IppTransportException` **`Failed`**, not `ConnectFailed` (the bound itself holds, so the README's "the connect and
   the handshake within `ConnectTimeout`" is true). (b) README Behaviour: "Every failure is an `IppTransportException`
   ... never an inner exception". MEASURED (P07, P08): a caller's own cancellation, during a silent handshake and while
   the answer never comes, leaves as the platform's `TaskCanceledException` (P08 with the inner chain
   `IOException>SocketException`), in 1002 and 1003 ms; neither text held `127.0.0.1` or the port on macOS (other
   platforms UNMEASURED). This is the shape the sender expects (`PrintJobSender.cs` rethrows an OCE when its caller's
   token is cancelled; sender callers see `ResponseTimedOut` or the OCE, never the transport's text), so the code is
   right and the sentences are loose. Through the sender, (a) changes nothing (both reasons are `TransportFailed`).
   Fix: say "the connect bound passed during the handshake is `Failed`" (or map it to `ConnectFailed`, one cell) and
   "a cancellation by the caller's token leaves as `OperationCanceledException`".

## INFO (each the gate's own reading; DERIVED marks source reading, not run)

1. **The pin (`HttpIppTransport.cs:44`, `:171` to `:180`, printed above in the seat's STATUS and re-read at the
   head).** `IsPinned`: null certificate false (`:173`); `SHA256.HashData(certificate.GetRawCertData())` (the leaf
   presented; the chain argument is discarded `_`), `FixedTimeEquals` with a 32-byte pin (unequal lengths are false).
   `ParsePin` (`:160` to `:168`): null, wrong length, any non-hex (a leading space measured, P09) refused with an
   `ArgumentException` whose text holds no value; upper-case pin works (P10). `git grep` at the head for
   `ServerCertificateCustomValidationCallback|DangerousAccept|CertificateChainPolicy|ConnectCallback|=> true|HttpClient`
   over the transport and its test file: nothing; the only callback is `:44` (positive control: `RemoteCertificate
   ValidationCallback` found once in `src`). By design (D2, README "the chain, its errors and revocation are not
   consulted"): a pinned leaf under an untrusted issuer (P11) and a pinned certificate expired 5 days ago, another
   name, no SAN (P12) are accepted; `ipps://localhost:<port>` (two addresses, IPv4 and IPv6, certificate naming
   127.0.0.1 only) is accepted on the pinned leaf (P03).
2. **No request byte before the callback returns true.** DERIVED: `SocketsHttpHandler` completes `SslStream`'s client
   authentication (the callback runs inside it; false throws `AuthenticationException`, mapped by
   `HttpRequestError.SecureConnectionError` to `SecureConnectionRefused`) before it writes the first HTTP byte, and
   .NET's `SslStream` offers no client TLS 1.3 early data. MEASURED: the stub (Kestrel, above TLS) saw 0 requests on
   every refused handshake (N03, N04, P01). A raw-byte capture under TLS was NOT RUN.
3. **No reused connection.** MEASURED (P02): three sequential sends on one transport = 3 requests on 3 distinct
   Kestrel connection ids; a wrong-pin transport after them refused with 0 new requests (P01). DERIVED: with
   `PooledConnectionLifetime = TimeSpan.Zero` a connection returned to the pool is already expired and disposed, and
   `Connection: close` marks it not reusable; the handler's resend paths (a failed reused connection, a lower-version
   retry, an authentication retry: no credentials are set) need a reused connection, a version downgrade or
   credentials, none of which this handler has. Which of the two settings alone would suffice: UNMEASURED.
4. **The address check (`:115` to `:135`).** MEASURED (P04, `Target` directly): `IPP://` and `HTTP://` PlainRefused;
   `wss`, port 0, empty `?` and `#` AddressRefused; `IPPS://` normalised and accepted; `ipps://@host` (empty user
   information) accepted with the `@` dropped (harmless); `0x7f.1` normalised to 127.0.0.1 by `Uri`; `[::1]` kept;
   **a link-local `ipps://[fe80::1%25en0]:631/...` becomes `https://[fe80::1]:631/...`: the zone id is dropped**
   (`Uri.Host`); trust is unaffected (the pin still applies), reachability on such an address may fail: a named limit
   for the records (FOR-RECORDS.md item 3). A hostname with two addresses: the pin is per connection, so every
   address must present the pinned leaf (P03 measured the IPv4 one).
5. **Bounds and hangs.** `ConnectTimeout` must be above 0 and at most 10 minutes (`:28`): `InfiniteTimeSpan` (-1 ms)
   is refused with `ArgumentOutOfRangeException` (P09, no value in the text; the sibling-lane shape does not occur
   here); exactly 10 minutes accepted. The handshake is bounded by it (P06, 1002 ms). There is no response bound in
   the transport (an `HttpMessageInvoker` has no `HttpClient.Timeout`): the sender's `SendTimeout` and
   `ResponseTimeout` (both checked by `Bounds.IsTimeBound` in the landed sender) cancel it (N11 green), as the README
   says. A direct caller with no token has no response bound: stated by the README ("every other bound is the
   sender's").
6. **Bodies and recursion.** The transport reads no body: it hands back the answer stream unread; the bounded read is
   the landed sender's (`IppReader` with `maxHeaderBytes`, `ResponseTimeout`). Answer headers are bounded by the
   handler's default `MaxResponseHeadersLength` (DERIVED). No recursion in the diff can be driven by the peer: the one
   loop (`FindReplay`, `:147` to `:158`) walks a locally built exception chain iteratively; the stub's `IppReader` call
   is test-only.
7. **Text and values.** `IppTransportException` messages are fixed per reason, no inner exception (N14, and every
   probe row `inner=null`); both `ToString()`s print the type name; `ObjectDisposedException.ThrowIf(..., this)` names
   the type only. A 401 is refused like any non-200 with 1 request (N09). An HTTP/1.0 answer is refused (`:89`,
   DERIVED; whether a printer answers IPP over 1.0 is UNMEASURED: FOR-RECORDS item 4).
8. **D-GH, the stuck `rules` status.** Read again at 12:55 to 12:57: check run 137426289705 `in_progress`, conclusion
   `success`, `completed_at 01:09:32Z`; workflow run 45092918591 `completed success` attempt 1; job steps six of six
   `success`; log 36553 bytes, echo lines left out 42, `Ran 111 tests in` 1, `UNIT-TEST FLOOR: ran 111, floor 111` 1,
   `RULES: clean (560 files)` 1, `OK` 2, control 0 (`scratch/rules.py`, `logs/job-rules-by-get.log`). I agree with
   ANSWER-2: GitHub's record, not the run. Landing step 3 says how to read it.

## WHAT I RAN (MEASURED; logs in `g1983/logs/`)
- Tools: 10 of 10 sha256 equal to THE TOOLS in my copy `g1983/gate` and in the seat's `<project>/.tools/b1972/gate`.
- Origin at 12:46: main `da8d64a8`, branch `ea0df6c0`, compare ahead 1 behind 0, 10 files +827 -3 (seven A, three M:
  the ten owned paths), open pull requests 0, open alerts on main 0, head parents [`da8d64a8`], message = the kit's
  `commit-message.txt` plus git's final line feed (the file is a byte prefix, `cmp` EOF on the file). At 13:01 (fresh
  clone, ADDENDUM-1): main `e193fb63` (parents 126c95e8 <- da8d64a8), branch still `ea0df6c0`.
- RED (`red`, BASE + `1-red.diff`; CODE red 10 of 10, unchanged 5 of 5): `red-restore` (CI=true, locked) rc 0;
  `red-build` 0/0; `red-exe` `Total: 152, Errors: 0, Failed: 18`, kinds `Assert.Throws` 11, `Assert.Null` 1,
  `Assert.Equal` 6, not an assertion 0, 18 of 18 in `HttpIppTransportTests`; `red-test` (no filter) `total: 1839`,
  `failed: 18`, `succeeded: 1817`, `skipped: 4`; `^ *failed Datasec\.` 18 and `...HttpIppTransportTests\.N` 18.
- Both patches in `red`: `git apply` rc 0; `add -A`; `write-tree` `0dda24750134b44fa4ff02faeb03e28a868fe68d` = the
  head's tree. `checks_ip.py` on that staged tree: `CHECKS: 6 of 6 PASS` (10 rows A 7 M 3, shared 42 paths rc 0 /
  control rc 1, ASCII clean, added 797 / with locks 827, public 6/4/3/28 = 41, no Jobs source; each control fired).
- HEAD (`clone`, CODE both 10 of 10, unchanged 5 of 5): `head-restore` rc 0; `head-build` 0/0; `head-test` 1839 / 0 /
  1835 / 4. `mutants_ip.py ... run` (one call, 20 heavy jobs): every row `Total 152`, `MUTANTS: 10 of 10 MATCH, 10 of
  10 undone equal` (rows as the kit's list: mPinIgnored N03 N04 N14; mRedirectFollowed N07; mPlainTaken N05;
  mHttp2Offered N08; mLengthKnown N01 N02 N07 N09 N11 N12; mStatusIgnored N09; mTypeIgnored N09; mReplayTaken N13;
  mAddressLoose N06; mTextLeaks N14). After: `status --porcelain` 0 rows; `after-mutants-build` 0/0; test-bin
  `Datasec.Suite.Jobs.Transport.dll` 12:52:51 later than the last undo of `HttpIppTransport.cs` 12:52:29;
  `after-mutants-test` 1839 / 0 / 1835 / 4. `repo_rules.py` (no `--source-documents`) `RULES: clean (560 files)`;
  `unittest` `Ran 111 tests`, `OK`.
- Probe (`phead`, `G1983Probe.cs`, 6 facts, never committed, moved to `_quarantine/G1983Probe-phead.cs`; the Jobs
  executable whole `Total: 158, Errors: 0, Failed: 0`): output `scratch/probe-out.txt` (P01 to P12 quoted above).
- Merges: `merge-tree --write-tree e193fb63 ea0df6c0` rc 0, `97c8b349f5a399711b747e372801b8c06a3770d6`, no conflict;
  `git diff --stat da8d64a8 e193fb63` over slnx, `Directory.*`, `global.json`, `NuGet.config`, `.github`, `build` and
  every Jobs path: `Datasec.Suite.slnx | 2 ++` only (L1's two Lab lines). `mmain` (e193fb63 + IP's diff, index tree =
  97c8b349): restore --force (CI=true, locked) rc 0, build 0/0, **1904 / 0 / 1900 / 4**, **RULES 587**. Main's push
  run 45097688311 by hosted2.py `--total 1874 --rules 580`: `HOSTED e193fb63...: PASS` (linux 1870, windows 1853).
  Before ADDENDUM-1: `merge-tree da8d64a8 ea0df6c0` = `0dda2475` (the head); TA + IP (`mta`, tree `5538ce57`) 1867 / 0
  / 1863 / 4, RULES 569: superseded, kept in landing.txt (A0).
- Hosted (head): `hosted2.py ea0df6c0... --total 1839 --rules 560 ...`: linux/windows/secret-scan every row OK,
  `FAIL 1 (check run rules not completed success)` only (INFO 8); `failed Datasec.` lines 0 and 0; the Jobs test
  assembly `passed` on both legs.

## SCANS
- gitleaks 8.30.1: control FIRST (a token built by program from two halves and 36 random characters, never printed,
  outside any clone): rc 1, `leaks found: 1`, moved to `_quarantine/gl-control`. Then the ten blobs at the head, both
  patches, the added lines (797) and the head's commit message as `1.txt` to `14.txt` (`scratch/gl-neutral`): rc 0, `no
  leaks found`; `gitleaks git` over `da8d64a8..ea0df6c0`: 1 commit, rc 0, `no leaks found`.
- `words.py --control` `CONTROL FIRED: 13 of 13`; over `added.txt` (797) and the head's message: `WORDS: clean (2
  files)`; over the 827 lines with the lock files: `seat ids 2` (the `linux-x64` / `win-x64` lock lines, as the kit
  says). My landing texts: `squash-subject.txt` (with #35), `squash-body.txt`, `pr-title.txt`: `WORDS: clean (3 files)`;
  `build/squash_scan.py` from main e193fb63's build/, subject with #35: control rc 1 found 2, message rc 0 found 0,
  `SQUASH-SCAN: clean`. `pr-body.md` names the coordinator and the product owner on purpose (who decides) and is not a
  repository text.

## FRAME QUESTION (stamp item 11): for each every/never/only sentence, three shapes NOT the tested one
| Sentence (README / kit) | Shape 1 | Shape 2 | Shape 3 |
|---|---|---|---|
| "accepted only when the certificate ... hashes to the pin" | issuer's pin, leaf presented: cell N04 | a resumed or second handshake with another pin: P01 MEASURED refused; renegotiation: stated limit (H15) | pinned but expired / other name / untrusted issuer: P11, P12 accepted, by design (README) |
| "plain ipp or http ... refused before any connection" | upper-case `IPP://`, `HTTP://`: P04 PlainRefused, no cell | `wss`, `ftp`, `file`: N06 (ftp, file), P04 (wss) | a 3xx to an `http:` Location: not followed (`AllowAutoRedirect = false`, N07 for an https Location; http Location DERIVED, no cell) |
| "every request runs on a new connection and new handshake" | three sends on one transport: P02 3 of 3 distinct, no cell | two transports, one host: P01 | concurrent sends: no cell, DERIVED (no pool kept) |
| "never written twice" | the content asked twice: N13 | the handler's resend on a reused connection: unreachable (INFO 3), stated limit H11 | a 401 retry with credentials: no credentials set, N09 401 case 1 request |
| "Every failure is an IppTransportException ... never an inner exception" | refused / wrong pin / connect: N03, N10, N14 | handshake never completes: P06 `Failed` (FOUND 2a) | caller cancellation: P07, P08 `TaskCanceledException` with an inner chain (FOUND 2b) |
| "no request reaches the printer" (refused handshake) | wrong pin: N03 | issuer pin: N04 | other pin after good sends: P01; pre-TLS bytes: DERIVED (INFO 2) |
| "never user information, a query or a fragment" | `user@`: N06 | empty `?`, `#`: P04 refused | empty `@`: P04 accepted, dropped (harmless); zone id dropped (INFO 4) |
| kit: "nothing in src/Datasec.Suite.Jobs/ but its README changes" | checks_ip check 6 | compare file list (10 rows) | the Jobs csproj and lock file unchanged: CODE unchanged 5 of 5 |

## NOT RUN
CodeQL (read on the pull request: landing.txt step 3); a raw byte capture below TLS; any printer, device or host but
127.0.0.1 and the origin; the hosted legs of the merge with e193fb63 (windows 1883 is PREDICTED); a renegotiation;
the merge with any main after e193fb63; `repo_rules.py --source-documents`.

## WHO DECIDED
Every choice of this lane and of the landing order is the coordinator's (Tuesday's), as coordinator; none is the
product owner's. The two findings are for the coordinator to order into a later round of this lane (round 2 of 2) or
into the slnx-owning lane; neither blocks this landing.
