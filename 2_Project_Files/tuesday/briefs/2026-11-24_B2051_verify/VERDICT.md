GATE B2051: GO WITH FINDINGS @ 77641b0 on main e2a20ae

Gate G1 (owed 79 changes the device token client's TLS chain policy and its device-root rule), round 1 of 2 of lane L2,
one Opus reader (claude-opus-5-5), in-session, read-only. OXPd 2, lane L2, kit B2049 (seat X64; Q1 and Q2 "a" in words at
stamp S4, Q3 to Q9 the defaults; each the coordinator's, not the product owner's). Head
`77641b0ea391e6ad192bfde849d1c66ea5816f8f` on `b2049/l2-device-root-chain-policy-text`, ONE commit, one parent `e2a20aef`
(BASE = main = PR 45's squash). Main did NOT move during the gate (e2a20aef by gh api -X GET at 16:31 and 16:48 and by a
fresh clone at 16:33). Read and measured 2026-11-24 16:30 to 16:50 AEDT in my scratch `fleet/state/s323/g2051/`: `clone`
(clone.py draft: push URL `invalid://no-push`, no identity; the head checked out detached), worktrees `red` (BASE +
`1-red.diff`) and `pat` (the head + a gate probe file, now `_quarantine/G2051Probe.cs.txt`). Every dotnet job and test
executable through the kit's `heavy.py` (sha256 `31adedc8...`) and the wave lock, one at a time (20 released lock folders,
all mine, in `g2051/_quarantine/locks/`; lock waits 0 to 3; no other holder's lock touched; the lock absent at the end).
Origin by `gh api -X GET` under the project GH_CONFIG_DIR. No write to the project, GitHub or Jira; no push, no pull
request, no re-run; no printer, no device, no tenant, no Azure; nothing deleted (moved to `_quarantine`).

**BLUF.** The head is BASE plus the two frozen patches byte for byte (temporary-index `write-tree`: red tree `7a6b8239`,
both-patches tree `41cad605` = `77641b0e^{tree}`, both equal the kit's; `2-fix.diff` alone refused, rc 1); the ten tools
equal THE TOOLS' sha256 in my copy, the seat's `.tools/b2049/gate` and the drafter's source (10 of 10 each); the commit
message equals `commit-message.txt`. Seven paths, all M, numstat equal to the kit; `checks_l2.py` 8 of 8 with every
control. Red first: the OXPd 2 executable `Total: 88, Failed: 2`, DA17 (`accepted /base/`) and DA18 (`policy set False`),
each by `Assert.Equal() Failure`. Green 2114 / 0 / 2110 / 4. `MUTANTS: 4 of 4 MATCH, 4 of 4 undone equal` (my run of the
frozen tool). **The G1 questions, MEASURED by a probe on macOS arm64:** 40 root spellings, 0 taken whose `AbsolutePath`
is not `/`; the seam IS the handler's own `SslOptions` (a callback set through it before the first send ran in the
handshake); the chain built in that handshake carries revocation `NoCheck` and downloads disabled; a wrong pin is still
`TlsFailed` with 0 requests and the issuer-never-sent leaf still taken; one constructor, one handler, one invoker: no
other path of the client sends. Hosted push run 45332864758 PASS on both legs (my own hosted3.py read: linux 2110,
windows 2093, RULES 657). Two Minor findings (text) and nine Info; none sends a byte, none blocks the landing.

## FOUND

1. **Minor (server README: the new `503` sentence is false for a cached serial).** `Server/README.md:23` to `:25` (owed
   84 (1)): "The check reads the stored hash of a serial within the serial rule whatever the header holds, so a vault that
   throws makes it `503` with none, one or two lines." `CallbackCredentials.StoredHash` returns the in-memory hash first
   (`CallbackCredentials.cs:170`) and reads the vault only when nothing is cached (`:178`). MEASURED (probe P04, macOS):
   a serial issued in this instance, then the vault broken: `Verify` returns false (401) for no header, one wrong header
   and a malformed one, 0 vault reads; a fresh instance (uncached): throws (503); a serial outside the rule: false, no
   read. The host issues through its own singleton (owed 86, RELAYED), so after an issue in the running host a vault
   outage gives 401, not 503, on that serial. The clause "401 while the vault answers" stays true (a sufficient
   condition). The HTTP status mapping (throw to 503) is DERIVED from `NotificationEndpoint.cs:31` to `:33` and
   `CallbackEndpoint.cs:47`; the route was not run. Fail closed either way. Fix (round 2 or a text pass): "a vault that
   throws makes it `503` for a serial whose stored hash is not cached in the process".
2. **Minor (two measured sentences without their platform).** The commission asks every platform word marked. Transport
   `README.md:34` to `:35` "(measured: a `TaskCanceledException`, with its inner exceptions)" names no platform, and
   `IppTransportException.cs:13` to `:15` states "A connect bound that passes during the TLS handshake is `Failed`, not
   this" with no mark at all; owed 83 records both measurements (probes P06 to P08) on macOS, other platforms
   UNMEASURED (`BACKLOG.md:601`, read by the gate). The README's own Bounds bullet (`:29`) does carry "measured on macOS
   arm64": the doc comment and the cancellation sentence do not. Fix: add "on macOS arm64" to both.
3. **Info (the landed revocation mode is dead beside the policy; a survivor).** MEASURED (P02c, P02d, macOS): mode
   `Online` with policy `NoCheck` built a `NoCheck` chain; mode `NoCheck` with policy `Online` built an `Online` chain:
   when `CertificateChainPolicy` is set, `CertificateRevocationCheckMode` is not read. A gate mutant removing
   `DeviceTokenClient.cs:82` survived every cell (`Total: 92, Failed: 0` with my probe; DA18's `Assert.Equal(NoCheck,
   tls.CertificateRevocationCheckMode)` reads the type's default). Harmless (both say off). The kit's D2 "both say off"
   is true; the README's Part 3 and the doc comments are not wrong. Q2 alternative c (drop the line) is the coordinator's.
4. **Info (the seam after the first send).** `TlsOptions` returns the same object twice and is the one the first
   handshake used (MEASURED P02a). After the first send, a callback set through it did NOT run on the next connection,
   but a change to its `X509ChainPolicy` object (revocation `Offline`, downloads on) DID reach the next chain (MEASURED
   P02e): the handler works from a shallow copy of its options. Reach: `internal`, granted to two test assemblies only
   (`Datasec.Suite.Adapters.Oxpd2.csproj:3` and `:4`); no `src/` reader (`TlsOptions` on 1 line of `src/`, its
   definition). The seat's H17 (a) and (b), now measured. Its doc "The TLS settings the client's own handler connects
   with" holds before the first send.
5. **Info (H8 on macOS with the policy: 0, and the policy changes nothing measurable there).** A leaf with AIA (issuer
   and OCSP) and CRL addresses on a 127.0.0.1 listener, issuer never sent: 0 connections in each of 5 variants (as built
   twice, main's settings, no policy with mode `Online`, policy with downloads ON and revocation `Online`); control 1
   (MEASURED P03). The adapter README's Limits "(with the policy ...) it is UNMEASURED" is now measured for macOS;
   Linux and Windows stay UNMEASURED (no probe there; heavy.py's closed proxy would also hide .NET's own Linux fetcher:
   DERIVED). So DA18 is a configuration proof plus one pinned handshake, as D3 says; it can never show a fetch stopped.
6. **Info (root spellings; the kit's H3 corrected).** MEASURED (P01, 40 spellings): `//`, `///`, `/%2F`, `/%5C`, `/%20`,
   `/;x`, `/%00`, `/~`, `/base?x`, `/BASE`, `/%2fbase`, empty query `/?`, empty fragment `/#`, `user@`: refused; `/./`,
   `/../`, `/a/..`, `/a/../`, `/a/b/../../`, `/%2e/`, `/%2E%2E/`, `/.%2E/`, `/.`, `/..`, `/./.`, trailing space or tab:
   `Uri` normalises them to `/` and they are taken (6 called: 6 requests, every one to `/cdm/oauth2/v1/token`). Those
   are RFC 3986 dot segments, not a prefix: the README's "a path prefix is never dropped in silence" holds. **The kit's
   H3 DERIVED "a backslash is turned into `/` by `Uri` and then refused" is wrong for `https://host:port\` and
   `https://host:port\base\`: `new Uri` throws `UriFormatException`** (fail closed, before the client). H4 confirmed
   (IPv6, a default port, `localhost.`, `HTTPS`, `hTTps`: taken). `https://@host/` (empty user information, the B2008
   FOUND 1 shape) is taken; the `@` is not in the request line or the Host header (DERIVED), so harmless here.
7. **Info (DA17's "before any connection" cannot fail).** The constructor makes no connection on main either; DA17's red
   is the exception alone (seat H17 (c)). The "0 connections" line is a guard, not a discriminator.
8. **Info (the hardening covers one of four device-facing handlers).** No chain policy in `Oxpd1Client.cs:44`,
   `HttpIppTransport.cs:33` or the lab's `DeviceChannel.cs:52` (each a `new SocketsHttpHandler` with a pin callback).
   Owed 79's Linux/Windows fetch concern applies to each (UNMEASURED). The transport README's "the chain, its errors and
   revocation are not consulted" is silent on downloads. Not this lane's (H10); an owed-list candidate.
9. **Info (one more exit of the transport the README does not name).** "Every failure is an `IppTransportException` ...
   Not so ..." lists the caller's cancellation, a call after `Dispose` and a null argument. An exception from
   `ReadAsStreamAsync` inside `SendAsync` (`HttpIppTransport.cs:94`) is rethrown as it is (`:96` to `:100`), and the
   constructor throws `ArgumentException` / `ArgumentOutOfRangeException` for a bad pin or bound (`:26` to `:31`,
   `ParsePin`). DERIVED; whether `ReadAsStreamAsync` can throw there for `SocketsHttpHandler` is UNMEASURED. H12's
   neighbour.
10. **Info (owed 87's bullet: "Measured on macOS arm64" covers two source-read clauses).** The caller's own cancellation
    and `ResponseHeadersRead` are read at source (`Oxpd2ClientCore.cs:44`, `:53`), not in the reader's measured list
    (`BACKLOG.md:628`); the other clauses are. True as written; the mark is slightly wide.
11. **Info (timing).** The OXPd 2 test assembly took 38.5 s on the hosted Windows leg of this head (owed 86 recorded
    33.9 s at an earlier head); each cell's guard is 10 s. No risk read.

## THE KIT'S GATE LIST (FOR TUESDAY, "THE GATE")

- `BASE..head` read whole: `DeviceTokenClient.cs` whole at the head (527 lines), `DeviceAuthOptions.cs` diff,
  `DeviceAuthCellTests.cs` diff and its helpers (`Clients`, `Certs`, `TlsStub`, `StubAnswer`), the three README diffs and
  each README whole where a sentence leans on a neighbour; the sources each sentence names (`HttpIppTransport.cs` whole,
  `Oxpd2ClientCore.cs` whole, `ApplicationClient.cs:6` to `:11`, `CallbackCredentials.cs` whole, `IDeviceSecretVault.cs`,
  `NotificationEndpoint.cs` and `CallbackEndpoint.cs` by grep), `BACKLOG.md:567` to `:632`.
- Patches and tools: 10 of 10 sha256 equal in three copies. Head tree = BASE + both patches (above).
- Red first: `Total: 88, Errors: 0, Failed: 2`; the two `[FAIL]` lines DA17 and DA18, each `Assert.Equal() Failure:
  Strings differ` (`Expected: "InvalidArgument /base/"`, `Actual: "accepted /base/"`; `Expected: "policy set True"`,
  `Actual: "policy set False"`). The red worktree's `src/` diff against BASE is the `_handler` field, the field
  assignment and the `TlsOptions` property only: main's TLS settings byte for byte.
- Does the seam return the handler the client SENDS with? Yes: `_handler` is the object passed to
  `new HttpMessageInvoker(_handler, disposeHandler: true)` (`:90`), the only invoker, and `TlsOptions => _handler.SslOptions`
  (`:94`); MEASURED P02a (a callback set through it ran in the client's own handshake). After the first send: FOUND 4.
- Mutants: every row `Total 88 Failed 1`, each red on exactly its listed cell, `undone equal True`; clone status empty
  after. Gate's own extra mutant (remove the landed mode line): survived (FOUND 3).
- Does ANY root with a non-`/` path reach a connection? No: the rule is in the one constructor (`:48` to `:49`), before
  `_tokenUri`, the handler and the invoker exist; MEASURED 40 spellings, 0 taken with a non-`/` `AbsolutePath` (FOUND 6).
- Can the chain policy be bypassed by another constructor, handler or code path? No path found: one public constructor
  (no other, no factory), the class `sealed`, `DeviceAuthOptions` `sealed`, the handler made once and held `readonly`,
  every call through `PostAsync` -> `SendAndReadAsync` -> `_invoker.SendAsync` (`:294`), `Dispose` disposes the
  invoker. `new DeviceTokenClient(` on 0 lines of `src/` (no production caller yet); `TlsOptions` reachable only from
  the two test assemblies (FOUND 4).
- README and doc-comment sentences against the source (the kit's table, every row): adapter `:82` to `:86` (rule, policy)
  TRUE at `:48` to `:49`, `:83` to `:87`; adapter `:178` to `:180` TRUE as of what it cites (FOUND 5 adds macOS);
  adapter `:213` to `:219` TRUE (`Oxpd2ClientCore.cs:44`, `:53`, `:55` to `:58`, `:79`, `:94`; FOUND 10);
  `DeviceAuthOptions.cs:6` to `:9` and the client's summary and constructor doc TRUE; `IppTransportException.cs:13` to
  `:15` TRUE at `HttpIppTransport.cs:140` to `:145` but unmarked (FOUND 2); transport `:28` to `:31` TRUE and marked;
  transport `:32` to `:38` TRUE at `:53` to `:55`, `:70` to `:73`, cancellation unmarked (FOUND 2), one more exit
  unnamed (FOUND 9); server `:21` to `:25` the `401` clause TRUE, the `503` sentence FALSE for a cached serial (FOUND 1).
- Platform words in the added lines (`grep -i 'measur|macos|linux|windows|platform'` over the diff, 9 lines): each
  "measured" names macOS arm64 or is UNMEASURED except the two of FOUND 2; "the platform builds the chain ... with
  revocation off and certificate downloads off" (adapter `:84` to `:86`) is a statement of configuration, MEASURED by the
  gate on macOS (P02a), DERIVED on the other legs.
- The server README rewrap word for word: BASE lines 24 to 26 (116, 209, 65 characters) and head lines 26 to 29 (116,
  113, 114, 48): 63 words and 63, equal in order (my program; control: the changed `401` paragraph's words differ).
- The hosted run on both legs: my `hosted3.py 77641b0e... --total 2114 --rules 657 --skipped-linux 4 --skipped-windows 21
  --unit 111 --floor 111 --hardened-scan --guard-linux 14 --guard-windows 15` (16:44): run 45332864758, attempt 1, every
  step success; linux `total: 2114` x2, `succeeded: 2110`, `skipped: 4`, GUARD 14; windows `succeeded: 2093`, `skipped:
  21`, GUARD 15; secret-scan both PLANTED-CONTROL lines, `no leaks found` x3, `wrong 0` x2, `not among ... 0`; rules
  `RULES: clean (657 files)`, floor 111; `HOSTED 77641b0e...: PASS`; `failed Datasec.` (case-insensitive) 0 and 0
  (control: 36 `passed` lines per leg); `Adapters.Oxpd2.Tests.dll` ran on both legs (passed, 8.6 s and 38.5 s). BASE's
  run 45284683760 re-read by me: PASS at 2112 / 657 (linux 2108, windows 2091): the head adds exactly 2 on each leg, and
  skipped did not move, so DA17 and DA18 succeeded on both legs (DERIVED arithmetic).
- **What the hosted legs DID prove for DA18 (linux-x64, windows-x64):** the handler's options read back with the
  policy set; one TLS handshake with the policy in place against a leaf whose issuer is never sent completes under the
  pin (1 request). **What they did NOT prove:** that the platform's chain on those legs carries the policy (no callback
  read there), and any fetch behaviour (the cells' leaf carries no AIA, OCSP or CRL address, so there is nothing to fetch).
- Code scanning: no CodeQL on a branch push (`check runs beside the four: 0`); the pull request's own analysis is the
  authority (landing.txt step 3). words and gitleaks: SCANS.

## WIDER (G1 attack): a test-only probe (`_quarantine/G2051Probe.cs.txt`, never committed; results
`g2051/scratch/probe-results.txt`, shapes and counts only, no value; the OXPd 2 executable whole `Total: 92, Errors: 0,
Failed: 0`)

- P01 roots: FOUND 6.
- P02 the chain in the client's own handshake (the pin callback wrapped through the seam, then the original called):
  as built `NoCheck`, downloads disabled `True`, 1 chain element, errors `RemoteCertificateChainErrors`, pin verdict
  `True`, 1 request; a wrong pin `TlsFailed`, 0 requests; mode/policy disagreement FOUND 3; after-start FOUND 4; main's
  settings (policy null) built a `NoCheck`, downloads-enabled chain and the call answered.
- P03 issuer, OCSP and CRL fetch: FOUND 5.
- P04 the vault that throws: FOUND 1.
- Gate mutant `xNoMode` (one line removed in `pat`, the adapter dll 16:43:43 later than the source 16:43:39): `Total: 92,
  Failed: 0`; undone, sha256 `2f8af23d...` equal to the head's.

## FRAME (stamp checklist item 11: three shapes outside the tested one per every/never/only sentence the change adds)

| Sentence | Shapes outside the tested one | Cell, probe or stated limit |
|---|---|---|
| P1 every root whose path is not `/` is refused, no connection | `//`; percent-encoded `/` and `\`; dot segments; backslash; empty query/fragment; IPv6; default port; trailing-dot host; case of scheme | P01 40 spellings: 0 non-`/` taken; dot segments normalised and taken (RFC, not a prefix); backslash throws in `Uri` (H3 corrected, FOUND 6) |
| P1b "a path prefix is never dropped in silence" (README) | `/a/..`; `/%2E%2E/`; `/base/` | the first two are not prefixes (RFC 3986 removal); `/base/` DA17 |
| P2 every chain built with no download and no revocation check | mode and policy disagree; options changed after the first send; a leaf with AIA/OCSP/CRL; another handler of the adapter | P02c/d (policy wins, FOUND 3); P02e (FOUND 4, tests only); P03 macOS 0 (FOUND 5); other handlers not covered (FOUND 8) |
| P2b the client sends only through `_invoker` over `_handler` | another constructor; a subclass; a second invoker | none exists (sealed, one constructor, `readonly` fields; source) |
| P2c trust is still the pin alone | wrong pin with the policy; issuer never sent; downloads on | P02b `TlsFailed` 0 requests; DA18 and P02a taken; P03 variant 4 taken |
| P3 every transport failure is an `IppTransportException` except cancellation, after-`Dispose`, null | `ReadAsStreamAsync` failing inside `SendAsync`; the constructor's argument checks; a concurrent `Dispose` | FOUND 9 (DERIVED); a concurrent `Dispose` after the check is `Failed` via the catch-all (`:82` to `:84`, DERIVED) |
| P4 `401` only while the vault answers; `503` when it throws | cached serial; uncached serial; serial outside the rule | P04: cached 401 (FOUND 1), uncached 503, outside the rule 401 without a read |
| P5 the body read is bounded by the caller's token only | `HttpClient.Timeout` in the read; the size bound; `SendRawAsync`'s body | source: the size bound also stops it (`MaxBodyBytes`); `SendRawAsync` hands the body to the caller (not the client's read); the reader's macOS measurement RELAYED |

## SCANS

- gitleaks 8.30.1: control FIRST (a GitHub-token-shaped value of 40 characters built by a program from two halves and 36
  random characters, never printed, alone in a new folder): rc 1, `leaks found: 1`, folder moved to
  `g2051/_quarantine/gl-control`. Then the head's 7 changed blobs, the added lines (109), the commit message as committed
  and both patches under neutral names `1.txt` to `11.txt`: rc 0, `no leaks found`.
- words.py: `--control` `CONTROL FIRED: 13 of 13`; the added lines + `commit-message.txt` (equal to the commit's message)
  `WORDS: clean (2 files)`; the squash subject (with #46), squash body and PR title `WORDS: clean (3 files)`. The PR body
  holds `coordinator` 2 and `product owner` 1 by design (its "Who decides" section, as the form). `B2[0-9]{3}` 0 and 0
  over the added lines and the message (control: the kit 22).
- squash_scan.py (the head's `build/`, equal to main's): subject with #46 + `squash-body.txt`: control rc 1 found 2,
  message rc 0 found 0, `SQUASH-SCAN: clean`.

## THE CHAIN AND THE MERGE

- Head (`clone`): locked restore (`CI=true`) rc 0; build `0 Warning(s)`, `0 Error(s)`; `dotnet test`: `total: 2114`,
  `failed: 0`, `succeeded: 2110`, `skipped: 4`. `repo_rules.py` (no `--source-documents`) `RULES-NOTE: R5 hash half NOT
  RUN`, `RULES: clean (657 files)`; `unittest` `Ran 111 tests` OK; `checks_l2.py` 8 of 8 (other paths 650 rc 0, control
  rc 1; added 109, removed 20; public lines 2).
- Merge with main of the moment: main IS BASE (e2a20aef at 16:48), so the merge is the head (tree `41cad605`), measured
  above. Open PRs 0; open code-scanning alerts 0; main's analyses results 0 (csharp, python, actions).
- Lane L1 (kit B2048): no branch on the origin at 16:31 or 16:48 (its lane folder `.tools/b2048` exists): the merge with
  L1 is NOT measured; landing.txt MAIN MOVES (B) carries the path rule.

## NOT RUN

- The probe on Linux and Windows (every P01 to P04 result is macOS arm64 only); a behavioural fetch measure on any leg
  with the policy other than macOS.
- The two `dotnet publish` lines and `release_guard.py` locally (the hosted legs' GUARD 14 and 15 read instead; the seat
  ran both locally).
- CodeQL locally (no Rosetta, as the kit measured; not re-tried); the PR's merge-ref run (does not exist yet).
- The server routes over HTTP with a throwing vault (FOUND 1 is measured at `CallbackCredentials`; the status mapping
  is DERIVED).
- An independent build of the kit's four mutants (my run is of the frozen tool, same as the seat's); one independent
  extra mutant was run (FOUND 3).
- The merge with lane L1 (not pushed).
- Any device, simulator or tenant.

## DISCLOSURE

- My first probe build failed on the xunit analyser rule xUnit1051 (a `Task.Run` without the test's token); I passed the
  token and rebuilt. The failed build changed nothing else.
- A pretooluse advisory on a case-sensitive `grep -c 'failed Datasec\.'`: I re-ran it with `-i` and a positive control
  (both 0; control 36 per leg); the numbers above are the re-run's.
- The probe and the extra mutant ran in the `pat` worktree only; the mutated file was restored by copy and its sha256
  printed equal to the head's; the probe file was moved to `_quarantine`; `pat`'s status is clean of tracked changes.
- The PR number in the scanned squash subject is #46 (the next number after 45, a guess): a different number changes
  characters, scan again (landing.txt step 5).

## LANDING

`landing.txt`, `pr-title.txt`, `pr-body.md`, `squash-subject.txt`, `squash-body.txt`, `FOR-RECORDS.md` in this folder.
Who decides to land: the coordinator (Tuesday), never the product owner. FOUND 1 and 2 are text, for round 2 of 2 of
lane L2 or a text pass, not a hold on this landing: nothing in either changes a byte on the wire, the device token client
has no production caller yet, and the code of owed 79 is correct as measured.
