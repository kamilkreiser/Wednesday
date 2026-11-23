GATE B1979: GO WITH FINDINGS @ 4d4e933 on main da8d64a

Gate G1 (security surface: device credentials and device trust), round 1 of 2 of lane TA, one Opus reader. OXPd 2,
lane TA, kit B1973 (seat X47; Q1 = a in words at stamp S4, Q2 to Q7 the defaults, each the coordinator's, not the
product owner's): `DeviceAuth/`, the device token client and the holder's refresh endpoint. Head
`4d4e933ca6754ed388e3e7bca41ae595c798d87a` on `b1973/ta-device-token-client`, ONE commit, one parent `da8d64a8` (=
main). Read and measured 2026-11-23 12:19 to 12:44 AEDT on Opus 5.5 in my own scratch `fleet/state/s316/g1979/`:
`clone` (the kit's `clone.py ... draft`: push URL `invalid://no-push`, no identity; detached at the head) and worktrees
`red` (`da8d64a8` + `1-red.diff`, then + `2-fix.diff`) and `phead` (the head, for my probe). Every dotnet job through
the kit's `heavy.py` (sha256 `31adedc8...`) and the wave lock, one at a time (46 jobs, lock waits 0 to 2, load waits
behind other seats; no other holder's lock touched). Origin by `gh api -X GET` under the project GH_CONFIG_DIR, last
read 12:43: main `da8d64a8`; the branch `4d4e933c`; IP's branch `ea0df6c0`; `compare da8d64a8...4d4e933c` ahead 1,
behind 0, 11 files, +1515 -5; open pull requests 0 (newest 32, merged); open alerts on main 0. No write to the
project, GitHub or Jira; no push, no pull request, no re-run; nothing deleted (probe file and scanner control moved to
`g1979/_quarantine/`).

**BLUF.** The head is BASE plus the two frozen patches byte for byte (`red` after both patches: `write-tree`
`2a12a268` = the head's tree), nine `A` and two `M` rows, the eleven owned paths. Red first at `da8d64a8`: 1837 / 27
failed, all `DeviceAuthCellTests.DA` (15 methods, DA16 green), each by the skeleton's `NotImplementedException`; the
adapter executable `Total: 86, Failed: 27`. 17 of 17 mutants MATCH in one run, 17 undone, rebuilt (the dlls later than
the last undo), whole solution green again 1837 / 0 / 1833 / 4; adapter executable 86 / 0. Main has not moved, so the
merge with main of the moment IS the head (merge-tree = `2a12a268`): 1837, RULES 562, Ran 111 OK. Hosted: `HOSTED
4d4e933c...: PASS` (linux 1833, windows 1816, the adapter test assembly passed on both legs, 0 `failed Datasec.`
lines). The attack holds: `CheckPin` (`DeviceTokenClient.cs:177` to `:186`) ignores `SslPolicyErrors` by design and is
the ONLY certificate decision in the diff; null certificate false; pin required, 64 hex, compared as bytes in fixed
time; leaf only (DA05); no request before the https check (constructor) or the window check (before the form); no
redirect followed; no `System.Net.Sockets` or logging reference (L03 green); no text path carries a value (DA02; fixed
messages, no inner exception, fixed `ToString`s); Q3's table matches the code (`:294` to `:307`); timeout and caller
cancellation end without a hang. **One Minor finding (FOUND 1): a device root with a path is accepted and its path
silently dropped, against README Part 3's "the device root plus `TokenPath`".** Nothing blocks the landing; it may land
first (landing.txt MAIN MOVES (A)).

## FOUND

1. **Minor (behaviour against its own text; `<project>/CLAUDE.md:61-62`, no false sentence in repository text): a
   `DeviceRoot` with a path is accepted and the path is dropped.** `DeviceTokenClient.cs:43` refuses user info, query
   and fragment but not a path; `:62` builds `new Uri(root, path)` with an absolute `TokenPath`, which replaces the
   root's path. MEASURED (probe P16): root `https://127.0.0.1:<port>/base/` sends to `/cdm/oauth2/v1/token`, not
   `/base/cdm/oauth2/v1/token`. README Part 3 (`README.md:80` to `:81`) says "to the device root plus `TokenPath`" and
   `DeviceAuthOptions.DeviceRoot`'s doc names no path rule. Effect: a host that registers a device behind a path
   prefix talks to the wrong resource on the right (pinned) host; fail-closed at worst (a 404 is
   `UnexpectedStatus`), no value leaves the pinned connection. Fix (a later round of this lane, the coordinator's
   choice): refuse a root whose `AbsolutePath` is not `/` (`InvalidArgument`, one DA14 row) or state the rule in the
   README and the doc comment.

## INFO

1. **Certificate trust, read whole.** One `SocketsHttpHandler` (`:67`), one callback (`:75`), no
   `HttpClientHandler`, no `ServerCertificateCustomValidationCallback`, no `CertificateChainPolicy`, no
   `ConnectCallback` anywhere in `src/Datasec.Suite.Adapters.Oxpd2` (`git grep` at the head; positive control: the
   Contracts tests' own `SocketsHttpHandler` found). `CheckPin`: null certificate false (`:179`); hash of `certificate`
   (the leaf) only, `chain` unused, so a chain-only match cannot pass (DA05 MEASURED, mutant `mPinAny` red on DA04
   DA05); `ParsePin` (`:160`) requires 64 characters and decodes hex in either case to 32 bytes, so the comparison is
   byte-exact (probe P05: a lower-case pin works; `g`*64, 63 characters, empty, null refused, DA14). By design (D2):
   probe P06, a pinned certificate that is expired and for another name, is accepted (README Limits says so).
2. **AIA downloads during chain building are not switched off (UNMEASURED off macOS).** The handshake builds a chain
   before the callback; the client sets revocation `NoCheck` (`:76`) but not
   `X509ChainPolicy.DisableCertificateDownloads`, which .NET documents as false by default (DERIVED). Probe P07
   (macOS arm64): a leaf whose issuer is not sent, carrying AIA caIssuers and OCSP URLs on 127.0.0.1 listeners, drew
   0 connections to either, pinned to the leaf (`OK`) and to another certificate (`TlsFailed`, 0 requests). Linux
   (OpenSSL chain builder) and Windows (CAPI) UNMEASURED. If either fetches, a device or a man in the middle could
   make the host issue one HTTP GET to a URL of its choosing before the pin refuses. The README's "no revocation
   fetch" is true; the kit's D2 "so the handshake fetches nothing" is proven on macOS only. Cheap hardening for a later
   round: `CertificateChainPolicy = new X509ChainPolicy { DisableCertificateDownloads = true, RevocationMode =
   X509RevocationMode.NoCheck }`. FOR-RECORDS item 2.
3. **No send before the checks.** https and the root's shape: constructor (`:38` to `:46`), before any handler exists
   (DA03, 0 connections). Window: `:120`, before the code is copied or the form written (DA08, 0 connections; mutants
   `mWindowDoubled`, `mWindowInclusive`). Arguments refused synchronously (`:100`, `:142`, `:85`). The one send is
   `SendAndReadAsync` (`:280`); nothing else calls the invoker. Redirects: `AllowAutoRedirect = false` (`:70`) and every
   3xx is `Redirected` (`:294`); probe P11 300, 303, 304 `Redirected` too. Proxy: `UseProxy = false` (`:69`), by
   construction (H5, no cell).
4. **Q3's table against the code** (`:294` to `:307`): 3xx `Redirected`; 400, 401 refusal (`Refused`, or null on the
   refresh: DA11); every other non-200 `UnexpectedStatus` (probe P11: 201, 204, 402, 404, 407, 429, 502; DA11: 403,
   500, 503). Matches S4.
5. **Text paths.** `DeviceAuthException` carries a reason and a fixed message (`DeviceAuthException.cs:19` to `:32`),
   never an inner exception (every catch rethrows a new one; DA13 asserts `InnerException` null); `ToString` fixed on
   the client, options, access, code and endpoint; the parse's strings are not returned. DA02 scans messages, texts and
   fields with a positive control. The caller's cancellation leaves as `TaskCanceledException` (probe P14, mid-call
   and before the call, 0 connections before), whose message is .NET's own.
6. **Answers not of the tested shape (frame question, stamp checklist item 11).** The README's "the answer is read
   strictly ... Anything else is `AnswerInvalid`" and Part 3's "any other certificate ends the handshake ... before a
   request is sent". The commission's three examples are each COVERED by a DA13 row: 200 with a non-JSON body (`not
   json`), a body over the bound (`big` declared, `one-over-undeclared` undeclared), a duplicate or missing field
   (`{"access_token":"a","access_token":"b"}`, `{}`). Three shapes the client is handed that are NOT a tested shape,
   each MEASURED by my probe and each a stated limit or now named: (a) a declared length longer than the body sent
   (P10: `TransportFailed`; no cell; fail closed); (b) a body led by a UTF-8 BOM (P12: `AnswerInvalid`; no cell, no
   README line; fail closed; whether a device sends one UNMEASURED); (c) a presented certificate naming an AIA URL
   (P07; no cell; INFO 2). Also probed, all typed `AnswerInvalid`: depth 9, `null` value, `3600.0`, an `expires_in`
   beyond Int32, trailing text, `Access_Token`, an empty `refresh_token`, a lone-surrogate escape, `expires_in` -1; an
   extra nested member is read (`OK`). And on the request side: a root with a path (FOUND 1); `TokenPath "/\host/x"`
   passes the constructor's `//` check and sends the request line `//host/x` to the pinned device (P0x: no other
   host reached; `%2F%2F` and `/./x/../y` likewise stay on the device). FOR-RECORDS items 3 and 6.
7. **The install code** (probe P15): not consumed by an exchange (sent twice when exchanged twice; the device
   decides), and carries no client: a 20-minute-old code made by a client on one test clock was sent by a second
   client on another. With `TimeProvider.System` everywhere both share one timestamp base (DERIVED), so the window
   holds in the product; H11's limit stands.
8. **README and comments, at the head, each against the code.** Part 3 (`:78` to `:103`): true but FOUND 1's "root
   plus TokenPath". The Limits sentence (`:122` to `:126`) and the holder's `finally` limit (`:166` to `:168`): true
   (DA12, mutant `mLateRead`). `### Limits of the device token client` (`:170` to `:179`): true; its "Whether a device
   negotiates HTTP/2 is UNMEASURED" is narrower in fact: the client sends .NET's default HTTP/1.1 request version
   (no `Version` set, `:273`), so it offers no HTTP/2 (DERIVED). The `TryGet` doc comment matches README `:162` to
   `:164`. Kit pointers `:69`, `:70`, `:75`, `:120`, `:185`, `:299`, `:363` each true at the head.
9. **Windows timing.** The adapter assembly passed on the hosted Windows leg in 33.9 s at the head and 31.1 s at main
   (Linux 7.8 s and 8.0 s), so the 16 TLS cells add about 3 s, far from their 10 s guard.
10. **CodeQL:** a certificate callback that ignores policy errors, revocation off, and test certificates with private
    keys made in the test are the shapes a csharp reader may flag; read on the pull request (landing.txt step 3).

## WHAT I MEASURED

- **THE TOOLS:** `cp -Rc` of `fleet/state/s315/d1973/seat-tools/` to `g1979/gate/`; 9 of 9 sha256 equal to kit
  B1973's table and to the seat's copy `.tools/b1973/gate/`. `words.py --control` `CONTROL FIRED: 13 of 13`.
- **THE COMMIT:** one parent `da8d64a8`; the stored message equal to `commit-message.txt` (350 bytes plus git's final
  LF); author and committer the project's own address (masked here); `--name-status` nine `A`, two `M`, the owned
  paths; THE CODE's sha256: "After 1-red.diff" 14 of 14 (with the unchanged project and lock files and
  `TextCellTests.cs`), "After both" 16 of 16, at the head.
- **THE PATCHES = THE HEAD:** `red` + `1-red.diff` + `2-fix.diff`, staged: `diff --cached --stat 4d4e933c` empty,
  `write-tree` `2a12a268` = the head's tree.
- **RED FIRST at `da8d64a8`** (`red`, `1-red.diff` alone): locked restore rc 0; build `0 Warning(s)` `0 Error(s)`;
  adapter executable `Total: 86, Errors: 0, Failed: 27`, 27 `[FAIL]` all `DeviceAuthCellTests.DA`, 0 holding DA16, 28
  `System.NotImplementedException` lines; whole solution `total: 1837`, `failed: 27`, `succeeded: 1806`, `skipped:
  4`, 27 `failed Datasec.` lines, all `DeviceAuthCellTests.DA`, 15 methods, 0 holding DA16.
- **THE MUTANTS:** `mutants_ta.py <clone> <keep> run g1979 'B1979 gate G1'` as ONE call: 17 rows, each `Total 86`,
  `MATCH`, `undone equal True` (mPinAny DA04 DA05; mFollowRedirect DA06; mHttpAllowed DA03; mWindowDoubled DA08;
  mWindowInclusive DA08; mNoExchangeClient DA07; mRefreshNotRequired DA09; mRefusalThrows DA11; mEveryErrorRefused
  DA11; mReadUnbounded DA13; mExpiresZero DA13; mDuplicatesAllowed DA13; mSpaceAllowed DA02 DA13; mPathIgnored DA14;
  mNoTimeout DA15; mTlsAsTransport DA04 DA05 DA15; mLateRead DA12); last line `MUTANTS: 17 of 17 MATCH, 17 of 17
  undone equal`, rc 0 (log `g1979/logs/mutants-run.out`). The first one-run 17 of 17 by a reader (the seat's was the
  builder's own). After it: status 0 lines; "After both" 16 of 16; build 0/0 with the adapter dll at 12:40:20 after
  the last undone source at 12:39:51.
- **GREEN, the head = the merge with main** (`clone`): `CI=true` locked restore `--force` rc 0; build 0/0; adapter
  executable `Total: 86, Errors: 0, Failed: 0`; whole solution `total: 1837`, `failed: 0`, `succeeded: 1833`,
  `skipped: 4`, `Passed!`. `git merge-tree --write-tree da8d64a8 4d4e933c` = `2a12a268`. `repo_rules.py` (never
  `--source-documents`; `test ! -e .../1_Project_Definition` rc 0): `RULES-NOTE: R5 hash half NOT RUN`, `RULES: clean
  (562 files)`. `unittest discover build/tests`: `Ran 111 tests`, `OK`. Expected after merge, as commissioned: 1837
  (1809 + 28), RULES 562: held. IP's tip: `git merge-tree --write-tree origin/b1972/ip-https-transport 4d4e933c` rc 0,
  no conflict; its ten paths share none with TA.
- **MY PROBE** (`G1979Probe.cs`, one fact, outcomes only, no value printed; sha256 `b239e3f4...`): `phead` built 0/0
  (a first build refused by the project's xUnit1051 analyzer on three `Task.Delay` calls without the test token; fixed
  in the probe, rebuilt) and run whole `Total: 87, Errors: 0, Failed: 0`; outcomes
  `g1979/scratch/probe-head.txt` (`4c45849c...`): INFO 1 to 7 and FOUND 1. The probe file then moved to
  `g1979/_quarantine/probes/`; `phead` status 0 lines.
- **HOSTED (GET only):** `hosted2.py 4d4e933c... --total 1837 --rules 562 --skipped-linux 4 --skipped-windows 21
  --unit 111 --floor 111 --hardened-scan`: run 45091850029, four jobs success, linux `succeeded: 1833`, windows
  `succeeded: 1816`, `RULES: clean (562 files)`, every hardened secret-scan row OK: `HOSTED 4d4e933c...: PASS`. Per
  leg (ANSI stripped): `failed Datasec.` 0 lines; `Datasec.Suite.Adapters.Oxpd2.Tests.dll (net10.0|x64) passed` on
  linux (7s 785ms) and windows (33s 902ms): the TLS cells green on both hosted legs (passing cells are not named in
  the log; the assembly's pass is the reading). `hosted2.py da8d64a8... --total 1809 --rules 553 ...`: run
  45068273700, four jobs and three Analyze rows success: `HOSTED da8d64a8...: PASS`.

## SCANS

- `words.py` over the 1515 added lines of `da8d64a8..4d4e933c` and the head's stored message: every count 0, `WORDS:
  clean (2 files)`.
- gitleaks 8.30.1 `dir --no-banner --redact --ignore-gitleaks-allow --exit-code 1`: control FIRST (a token-shaped
  value built by program from two halves and 36 random characters in a new scratch folder, never printed): rc 1,
  `leaks found: 1`, folder moved to `g1979/_quarantine/gl-control-*`; the eleven head blobs, the two words files and
  both patches as 15 neutral files in a new folder: rc 0, `no leaks found`. (The hosted secret-scan of the head ran the
  stored-object scan: OK.)
- `words.py` over `squash-subject.txt` (203 characters), `squash-body.txt` and `pr-title.txt` (168, under 256):
  `WORDS: clean (3 files)`.
- `build/squash_scan.py <subject with #33> squash-body.txt --scanner /opt/homebrew/bin/gitleaks` (from the head's
  `build/`, which equals main's: `build/**` is outside the diff): control `rc 1, found 2`, message `rc 0, found 0`,
  `SQUASH-SCAN: clean`.
- gitleaks over this verdict folder (seven files), run after this file was written whole: rc 0, `no leaks found`
  (printed in the reader's report); ASCII check of the folder: 0 lines outside printable ASCII but the attribution
  line of `pr-body.md`.

## CODEQL

Not run locally (the gate has no CodeQL step). Read on the pull request (landing.txt step 3); INFO 10.

## NOT RUN

Any local run on Linux or Windows (the hosted legs of the head only); the probe on Linux and Windows (INFO 2's AIA
question is the one that matters); the two publishes and `release_guard.py` locally (the head's push run: GUARD clean
10 and 11 files); `run_step.py`'s neutral scan locally (the hosted secret-scan ran it on the head, every hardened row
OK); `repo_rules.py --source-documents` (never); the merge with any main but `da8d64a8` (IP first: landing.txt MAIN
MOVES (B), first measured by the pull request); CodeQL; anything against a tenant or a device; any re-run.

## DEVIATIONS

None from the commission. Notes: (1) two Bash calls of mine were refused by the session's hooks before running (one
held a `cd`, one an unquoted `===`) and were re-issued without them; neither reached the same end by another route
that the hook meant to stop. (2) Heavy jobs ran in the Bash tool's background mode (each waited for before the next),
as the seat did, so a tool time bound could not leave the lock held. (3) My probe's first build failed on the
project's own analyzer (xUnit1051), not a result; fixed in the probe file and rebuilt.

## TREES LEFT

`g1979/clone` detached at `4d4e933c`, status clean (mutants undone, rebuilt); worktree `g1979/red` at `da8d64a8` with
both patches staged (index tree `2a12a268`, never committed); worktree `g1979/phead` at `4d4e933c`, clean (probe moved
out; its build output stays under `bin/`); `g1979/logs/**`, `g1979/scratch/**` (`probe-head.txt`, `G1979Probe.cs`,
`words/`, `gl-neutral-*`, `mutants/`, helper scripts), `g1979/_quarantine/{locks,gl-control-*,probes}`. No process left
running; the wave lock not held by this reader.
