GATE B2137: GO WITH FINDINGS @ 641935b on main 38a031e

Gate G1, ROUND 1 OF 2 of lane OX-C kit 1 (the other modules' hygiene: the Graph walk's loop key, owed 131; the device
token client's revocation line, 122; the Server README, 119; the Jobs transport's platform words, 120; the Identity
README's citations, 77; owed 84 not built), one Opus reader (claude-opus-5-5), in-session, read-only. OXPd 2, kit B2134
(seat X80; stamp S4: Q1 "a" one kit, Q3 "a" the edits and mutants frozen, the two cells the seat's, each in words; Q2,
Q4 to Q10 the defaults; S8 the canonical heavy runner 31adedc8; ANSWER-1 (a); every choice the coordinator's, none the
product owner's). Head `641935b53643de3246406aaa2005e34741288bcf` on `b2134/lane-c-kit1-hygiene`, ONE commit, one parent
= main `38a031e589c8d71049756752e39eafc91ad59055` (PR 56). Main and the branch did NOT move during the gate (gh api -X
GET 09:04:53 and 09:23:02 AEDT; open pull requests 0 both times; open code-scanning alerts 0 both times). Read and
measured 2026-11-27 09:04 to about 09:27 AEDT in my scratch `fleet/state/s332/g2137/`: `clone` (clone.py draft: push URL
`invalid://no-push`, no identity; detached at the head; the mutants ran here), worktrees `red` (BASE plus the head's
three test files, `git diff --quiet 38a031e5 -- src` rc 0) and `probe` (the head plus two probe files of mine,
`GateProbeB2137Tests.cs` in the Graph tests and `GateProbeB2137ServerTests.cs` in the Server tests, never committed,
never pushed). Every heavy job through the kit's `heavy.py` (sha256 31adedc8...; my copy of the eleven tools 11 of 11
equal to THE TOOLS by `cmp` and sha256) and the wave lock, taken per job and released, one at a time (36 jobs, lock
waits 0 each); the 36 released lock folders are mine, in `g2137/_quarantine/locks/`; no other holder's lock or file
touched; the lock absent at 09:25.

**AT THE HEAD (where a record or the kit disagrees with what I measured):**
1. **The Server README's held-hash sentence is true for one process, not for another process over the same vault**
   (FOUND 1): a credential re-issued elsewhere is refused while the older one still passes, and a device forgotten
   elsewhere still passes, until the host restarts. The kit's H9 named the first half as a records candidate; both
   halves are now MEASURED.
2. **The hang the seat met is owed 137's shape, not this lane's** (FOUND 2): its sample's fingerprint equals 137's
   (recorded at main baa32eae, before H16 existed), the `Broken` switch throws before any lock, the store is one per
   host, and my two whole runs at the head and six runs of the Server executable alone were green.
3. Kit D5 and H4 said "UNMEASURED" for what reaches the wire and for `GetLeftPart`'s canonical form: both MEASURED here
   (FOUND 3).

**BLUF.** The head does what its five items ask on every path the kit names. **No next link that names an address
already requested, by its text without the fragment, is still followed** (the kit's six rows plus my six walk shapes,
the first address included); **no next link that is a different address is now judged a loop**: across 34 address
pairs the ONLY change of judgment from BASE's `AbsoluteUri` key to the head's `GetLeftPart(UriPartial.Query)` key is the
fragment-only class (5 pairs); `%23` in a query or path stays another key, an empty `?` stays another key, and
`GetLeftPart` canonicalises no two addresses to one key that `AbsoluteUri` kept apart (MEASURED, macOS arm64); HTTP/1.1
puts no fragment on the wire (MEASURED). **The device token client's TLS options read the same before and after**: the
default is `NoCheck` (MEASURED, macOS arm64), and DA18 (which asserts the mode and the policy's mode) is green on the
hosted linux and windows legs of the head. **The Server README's new sentences are not wider than `CallbackCredentials`
on any single-process path** (a held hash by issue or by read, a hash never held, a record of the wrong length, a raced
read not reachable from any route), **but are wider for another process** (FOUND 1). **No landed cell changed** (removed
lines under `tests/` 0; every landed cell green locally and on both legs). Red first exactly the 3 rows (`Total: 203,
Errors: 0, Failed: 3`, each by assertion, my run) and H16 green on BASE (`Total: 16, Failed: 0`, my run); green Graph
`203 / 0`, Server `16 / 0`, adapter `88 / 0`, the whole solution `total: 2429`, `failed: 0`, `succeeded: 2425`,
`skipped: 4` (my runs h1 and h3); `MUTANTS: 7 of 7 MATCH, 7 of 7 undone equal` (my run of the frozen rows, every row's
red rows equal to the seat's); `HOSTED 641935b5...: PASS` (my read; control FAIL 4). **One Minor finding, six Info.
None blocks the landing.** Tuesday's points: (a) the hang: owed 137's pre-existing shape, neither H16 nor `Broken` can
plausibly cause it (FOUND 2, Info); (b) 122: the dropped line set the property to its own default and no platform reads
another value (MEASURED on macOS, and DA18 green on linux and windows): **Info, no finding**; (c) 120: "measured on
macOS arm64" is supported by its sources, arm64 DERIVED for the probe run itself (FOUND 5, Info).

## FOUND (graded; whether each blocks landing)

1. **Minor, does NOT block (the held-hash sentence and another process).** `logs/probe-server.tsv` S1: the host holds
   `SYNTH0101`'s hash from `rig.Issue`; a second `CallbackCredentials` over the host's own `IDeviceSecretVault`
   re-issues it; with the store answering, the older credential gets `200` and the new one `401`. S2: the host holds
   `SYNTH0102`'s hash; a second instance's `Forget` deletes the vault record (`ListNames` 1 to 0); the old credential
   still gets `200`. Why: `CallbackCredentials.StoredHash` returns a cached hash with no read
   (`CallbackCredentials.cs:170` to `:172`) and the cache is removed only by this instance's `Issue` or `Forget`
   (`:56` to `:65`, `:91` to `:99`). The README (`src/Datasec.Suite.Server/README.md:24` to `:29`) says "the issued one
   passes" and "until the process ends"; for a re-issue or a revocation by another process the issued one is refused
   and the revoked one passes, and the Limits section does not name it. Reach: a deployment whose credentials are issued
   or revoked by another process over the same vault (no route of this host issues or forgets: `.Issue(` and
   `.Forget(` on 0 lines of `src/` but the adapter README, `git grep` at the head). Pre-existing behaviour (the cache is
   BASE code, unchanged by this lane); the head's README is strictly more accurate than BASE's. Fix (records / a later
   round): a README Limits clause, and the design question of how a running host learns of a re-issue or a revocation.
   Proposed as an owed item (FOR-RECORDS.md PROPOSED 1).
2. **Info (Tuesday's point a: the Server.Tests hang is owed 137's shape).** The seat's `/usr/bin/sample` of pid 73596
   (`<project>/.tools/b2134/logs/orphan-server-tests-sample.txt`, 1221 lines, taken at 04:34:20, launch 04:03:33):
   main thread in `Monitor_Wait` (a managed wait from the runner's entry point), threads `Kestrel Timer` (a timed
   `Monitor.Wait`, one wake in 1564 samples), `Console logger queue processing thread`, `.NET File Watcher`, four
   `.NET TP Worker` idle, no running frame; the seat's `lsof`: no inet socket. This equals owed 137's Symptom word for
   word (main thread in a managed `Monitor.Wait`, the same three named threads, no inet socket, 21 threads), recorded on
   2026-11-25 at main baa32eae, before this lane's H16 or `Broken` existed. Neither can plausibly cause it: `Broken`
   throws in `TryGet` BEFORE `lock (_sync)` (`HostRig.cs:230` to `:235`), and `CallbackCredentials` reads the vault
   outside its own lock (`:168` to `:178`), so no lock is held across the exception; each `HostRig.StartAsync` makes its
   own `MemorySecretStore` (`HostRig.cs:93`) and no static store exists; the throw is caught and answered `503`
   (`NotificationEndpoint.cs:27` to `:35`), which H16 asserts. No open inet socket also rules out a cell waiting on
   `RawPostAsync`'s read. A live Kestrel timer and console logger mean a host that was not fully stopped, which is 137's
   own candidate (`HostRig.cs:108` and `:171`, no token, no bound). My runs: the whole solution twice at the head (h1:
   `rc 0 (57s)`, h3: `rc 0 (55s)`, Server.Tests `passed` in 16.6 s and 19.2 s) and the Server executable alone six
   times (`Total: 16, Failed: 0`, 4.1 to 4.6 s). Beside it (not this lane's, never touched): a second orphan test host
   on this machine, `Datasec.Suite.Sessions.Tests` of `/private/tmp/b1839-gate/clone` (pid 2177, parent 1, started
   2026-11-21 17:15, 14 threads, no inet socket), which fits owed 138 (the runner leaves an orphan at its bound).
3. **Info (kit D5 and H4 now MEASURED, macOS arm64).** `logs/probe-graph.tsv` K1 (34 pairs, BASE key `AbsoluteUri`
   against the head's key): changed by the fragment only 5, changed otherwise 0. Kept apart by both: `%23` in a query
   and a path, `items?` against `items`, parameters in another order, a trailing slash, `%2F`/`%3D`/`%26` against the
   reserved character, `+` against `%20`, `;p=1`, `%2523` against `%23`, `%3D%3D` in a skip token, `%00`. Joined by
   both (the same at BASE): `:443`, `%41` and `A` (path and query), the host's and the scheme's letter case, `%7e` and
   `~`, dot segments, `\` and `/`, a raw `ü` and `%C3%BC`, `%c3%bc` and `%C3%BC`, a lone `%` and `%25`, a raw tab
   and nothing. N1 (an in-process loopback listener, the request line as received): `items?page=2#f1`,
   `items?page=2#` and `items#f0` arrive as `GET /v1.0/items?page=2` and `GET /v1.0/items`; `items?page=2%23f1` arrives
   with `%23f1`. So a fragment-only loop at BASE re-sent the same request target to the server (the cell's red rows).
   W (walks through the client): an empty `?` after the start is followed once (a new key) and its repeat is a loop;
   no fragment after a fragment is a loop at 2 sends; a start address with a fragment then without is a loop at 1;
   `%23` then the real fragment is followed (two keys); `x/../items` naming the start is a loop at 1; control: two
   different pages then none ends with no error at 3. The kit's H4 limit stands (two texts are two keys); nothing in it
   is new at the head.
4. **Info (Tuesday's point b; the revocation line).** `logs/probe-graph.tsv` T1: `new SslClientAuthenticationOptions()`
   reads `CertificateRevocationCheckMode=NoCheck`, `new SocketsHttpHandler().SslOptions` the same, a policy set with no
   mode line reads mode `NoCheck` and policy `NoCheck` (`macOS 27.2.1|Arm64`). On the hosted legs DA18 asserts
   `Assert.Equal(X509RevocationMode.NoCheck, tls.CertificateRevocationCheckMode)` on the client's own handler options
   (`TlsOptions => _handler.SslOptions`, `DeviceTokenClient.cs:95`) and the head's linux and windows logs each hold
   `Datasec.Suite.Adapters.Oxpd2.Tests.dll ... passed` and 0 `failed Datasec.` lines: the value without the line is
   `NoCheck` on all three platforms (MEASURED). `mModeOnline` and `mPolicyOnline` each red DA18 at `:444` and `:448`
   (my run). Style only: the new comment (`DeviceTokenClient.cs:82` to `:83`) says "(measured on macOS arm64)" without
   the "other platforms UNMEASURED" the transport's two sentences carry; the claim it scopes (the mode is not read
   beside a policy) is owed 122's P02c/P02d, macOS arm64, and moot for this change. The same line stays in
   `HttpIppTransport.cs:43` with no policy (owed 121, not this lane's).
5. **Info (Tuesday's point c; 120's platform).** Gate B1983 `VERDICT.md:51` ends its P07/P08 sentence "neither text held
   `127.0.0.1` or the port on macOS (other platforms UNMEASURED)" (`sed -n 44,52p`); its P06 sentence (line 46, the
   `ConnectFailed` sentence E4 corrects) carries no platform word of its own; that session's `logs/head-test.log` prints
   `(net10.0|arm64)` on 46 lines and `(net10.0|x64)` on 0; its `probe-exe.log` (7 lines) prints no architecture, and
   its probe jobs ran in the same session on this machine, which runs no x86_64 program (kit FACTS 5). So "macOS" is
   MEASURED by the review's words and "arm64" is DERIVED for the probe run (from its own session's test log and the
   machine). Supported; the frozen words stand.
6. **Info (the mutant expectations; the kit's words only).** `mLoopKeyAdd` row 2 turned red by the `PagingLoop`
   assertion (`PagingTooManyPages`), not the sends assertion the kit named; `mLoopKeyCompare` row 2 (kit UNMEASURED)
   turned red, and K1 row 2 prints `AbsoluteUri` of `items?page=2#` as `items?page=2#` (the empty `#` kept). Equal to
   the seat's STATUS.
7. **Info (my own slip, and the tool's header).** My `h2-whole` ran `--no-build` straight after `mutants_c1.py run`
   and read `failed: 2`, exactly `mLoopKeyOriginal`'s row 6 and `mPolicyOnline`'s DA18: the tool undoes the source, not
   the build, so each suite's bin held its last mutant. After a build (`h3-build`, both dlls later than their sources by
   `stat`) `h3-whole` read `total: 2429`, `failed: 0`. The kit's Step 4 asks for that build and the seat did it
   (`post-mutants-build`), so the seat's numbers stand; the tool's header could say so (FOR-RECORDS.md PROPOSED 2).

## 1. THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), item by item

- **`<BASE>..<head>` read whole:** `diff --name-status` ten rows, all `M`; numstat 2/1, 14/6, 1/1, 3/3, 2/2, 5/5,
  11/6, 56/0, 45/0, 8/0, equal to `compare`'s ten modified files (GET 09:04); ONE commit, parent 38a031e5, tree
  7ec27cb9, author and committer the repo's `@datasec.com.au` address, equal (masked); `ls-files` 679. Every changed
  `src/` line and every added test line read. `apply_c1.py check`: `FROZEN` for each of the eight files (the eight
  frozen files equal to `edits_c1.json`); `checks_c1.py` on the head's index `CHECKS: 9 of 9 PASS` (check 3 frozen 8 of
  8, control False; check 4 removed lines under `tests/` 0, control added 109; check 9 citations 8 of 8, control BASE 6
  of 8). The commit message equals the frozen `commit-message.txt` byte for byte (290 bytes, `cmp` rc 0).
- **Red first** (`g2137/red`; `logs/r-*.log`): restore rc 0; build `0 Warning(s)`, `0 Error(s)`; Graph `Total: 203,
  Errors: 0, Failed: 3`, the `[FAIL]` lines exactly rows 1, 2, 3 of the new cell, each followed by an `Assert.Equal()
  Failure`: row 1 Expected `PagingLoop` Actual `PagingTooManyPages` (`:263`), row 2 Expected 2 Actual 3 (`:272`), row 3
  Expected 1 Actual 2 (`:272`); rows 4 to 6 and every landed cell passed. Server `Total: 16, Errors: 0, Failed: 0`
  (H16 green on BASE plus the support edits), `[FAIL]` 0. Equal to the kit's PREDICTED red and to the seat's run.
- **Head green** (`logs/h-*.log`): locked restore rc 0; build 0/0; Graph `Total: 203, Failed: 0`; Server `Total: 16,
  Failed: 0`; adapter `Total: 88, Failed: 0`; whole solution `total: 2429`, `failed: 0`, `succeeded: 2425`,
  `skipped: 4` (h1, and h3 after the rebuild of FOUND 7). Probe tree: build 0/0 (warnings not made errors for my
  probe), Graph `Total: 212, Failed: 0` (203 + my 9 probe cases), Server `Total: 20, Failed: 0` (16 + my 4), which
  record and assert nothing.
- **Mutants** (`logs/mutants-run.out`; the frozen `mutants_c1.json` sha256 7fd0cf1c..., `--list` `LIST: 7 mutants, 2
  suites, 2 cells`; my run, about 09:13 to 09:17): `MUTANTS: 7 of 7 MATCH, 7 of 7 undone equal`, every row's Total,
  Failed and applied sha256 equal to the seat's. By ROW (`logs/mt-*.log`): `mLoopKeyFragment` rows 1, 2, 3;
  `mLoopKeyAdd` rows 1, 2; `mLoopKeyCompare` rows 1, 2, 3; `mLoopKeyUnescaped` rows 4, 5 (`Assert.Null`: a
  `PagingLoop`); `mLoopKeyOriginal` row 6 (sends 2 not 1); `mModeOnline` DA18 `:444` (`Online`); `mPolicyOnline` DA18
  `:448` (`Online`). Nothing red outside the listed cells; the clone's status 0 lines after; `apply_c1.py check`
  `FROZEN` 8 of 8 after.
- **Whether ANY next link that names an address already requested, by its text without the fragment, is still
  followed:** NO (rows 1 to 3; FOUND 3's W shapes: no fragment after a fragment, the start address with a fragment then
  without, `x/../items`).
- **Whether ANY next link that is a different address is now judged a loop:** NO (FOUND 3: K1 0 pairs changed
  otherwise; `%23` in path and query, and a query that differs only after a `#`, which is a fragment and is a loop by
  design; `GetLeftPart` joins nothing `AbsoluteUri` kept apart).
- **Whether the device token client's TLS options read the same before and after on the hosted legs:** YES (FOUND 4;
  DA18 passed on linux and windows at the head; the default MEASURED here).
- **Whether the Server README's new sentences are wider than `CallbackCredentials` on any path:** a held hash (by
  issue: H16 and my S4; by read: H16): not wider; a hash never held, or a record of the wrong length (my S3: store
  answering `401`, throwing `503`; a serial with no record, throwing `503`): not wider; a raced read (`:185` to `:190`,
  not cached): unreachable from any route (no route issues or forgets), DERIVED; another process: WIDER (FOUND 1).
  My S4 also: a held serial with the store throwing gets `200` on the notification route with its credential, `401` with
  a malformed header and with its credential on two lines (the one-line rule, no read), and the same serial in lower
  case (within the rule, another name) `503`.
- **Whether ANY landed cell changed:** NO (check 4; every landed cell green in both whole runs and on both legs).
- **The README and comment sentences against the code** (head): Server README `:24` to `:29` against
  `CallbackCredentials.cs:56` to `:65` (issue caches), `:165` to `:199` (cached returned with no read; a read cached
  once; a raced read not kept), `ServerHost.cs:37` to `:38` (one vault and one `CallbackCredentials`, singletons),
  `NotificationEndpoint.cs:27` to `:35`; the notification bullet `:49` to `:50` against the same; the Services bullet on
  a store that cannot open stays true (nothing can be held before the store opens: `Issue` writes the vault first,
  `:55`). Transport README `:34` to `:35` and `IppTransportException.cs:13` to `:15`: FOUND 5. Identity README `:35`
  against `CsaStore.cs:294` (`catch (Exception)` in `PrefixOf`, `:287`) and `:311` (in `BlobOf`, `:304`): true (check
  9). GraphClient `:114` to `:118`, `GraphFailure.cs:15` and the `LoopKey` summary `:738` to `:742` against `:648`,
  `:735`, `:743`: true; the summary's "the request target of HTTP/1.1 carries no fragment: RFC 9112, section 3.2" is
  MEASURED for .NET's client here (FOUND 3, N1). `DeviceTokenClient.cs:82` to `:83`: FOUND 4. No `<file>.cs:<n>`
  citation anywhere in the repository names a file this change shifts (`git grep` for `GraphClient`, `GraphFailure`,
  `DeviceTokenClient`, `HostRig`, `HostCellTests`, `PagingTests`, `IppTransportException` with `.cs:<n>`: rc 1; control
  `CsaStore.cs:<n>` 4 lines).
- **The hosted run on both legs** (`logs/hosted.out`, my hosted3.py read, no `--wait`, about 09:21): run 45871265141,
  four jobs attempt 1 success, linux `total: 2429` twice, `succeeded: 2425`, `skipped: 4`, windows `succeeded: 2408`,
  `skipped: 21`, `RULES: clean (679 files)`, `UNIT-TEST FLOOR: ran 117, floor 117`, `GUARD: clean (14 files)` / `(15
  files)`, `failed Datasec.` 0 and 0 (control: 315 and 366 `Datasec.`); check runs beside the four: 0; last line
  `HOSTED 641935b53643de3246406aaa2005e34741288bcf: PASS`; the control at `--total 2430` printed `FAIL 4`.
- **CodeQL:** NOT RUN locally (kit FACTS 5); the pull request's own run is the read (landing.txt step 3). Main's
  analyses at 38a031e5: csharp, python, actions results 0.

## 2. TUESDAY'S OWN POINTS

- **(a) The Server.Tests hang:** owed 137's pre-existing shape; neither H16 nor the `Broken` switch can plausibly cause
  it (no shared static store, no lock held across the exception, the exception answered `503`); one-off at the head by
  ANSWER-1's rule, confirmed by my two green whole runs and six green runs alone. **Info** (FOUND 2). 137 stays owed and
  gains a second sighting.
- **(b) 122:** the dropped line set `SslClientAuthenticationOptions.CertificateRevocationCheckMode` to `NoCheck`, its
  own default (MEASURED here; .NET's managed default, the same object on every platform); DA18 reads `NoCheck` from the
  client's own handler on the hosted linux and windows legs; so no platform reads a different value. **Info, no
  finding** (FOUND 4).
- **(c) 120:** supported: "macOS" by the review's own words, "arm64" DERIVED for the probe run from its session's test
  log and this machine. **Info** (FOUND 5).

## 3. ADVERSARIAL BEYOND THE KIT (three shapes outside each property)

- **P1** (a fragment-only repeat is a loop; any other link on the origin is followed): an empty `?` after the start
  (followed once, a new key: covered); `%23` then the real fragment (two keys, followed: covered); `x/../items` naming
  the start (a loop at 1: covered, the same at BASE). Plus K1's 34 pairs (FOUND 3).
- **P2** (the TLS options hold `NoCheck` twice and downloads off): the default without the line (`NoCheck`, MEASURED);
  a policy with no mode line (both `NoCheck`, MEASURED); Linux and Windows (DA18 green on both legs: covered). Named
  limit: the other handlers (owed 121).
- **P3** (the README's credential sentences): a re-issue and a forget by another process (WIDER: FOUND 1); a record of
  the wrong length (never held, `503` while the store throws: covered); a held serial on the notification route, with a
  malformed header, on two lines, and in lower case (`200`, `401`, `401`, `503`: covered).
- **P4** (each measured sentence names its platform): the transport's Bounds bullet (`README.md:29`, "measured on macOS
  arm64": covered); the new comment in `DeviceTokenClient.cs:83` (names macOS arm64, not "other platforms": FOUND 4,
  style); the review's P06 sentence (no platform word of its own: FOUND 5).
- **P5** (citations true): the eight Identity citations (8 of 8: covered); any `<file>.cs:<n>` citation in the repository
  of a file this change shifts (none: covered); owed 137's `HostRig.cs:108` and `:171` in `BACKLOG.md` (both above the
  added lines at `:215`, still `await app.StartAsync();` and `await _app.StopAsync();` at the head: covered).
- **P6** (no landed cell changes): removed lines under `tests/` 0; `Broken` defaults false so H01 to H15 run the store
  unchanged (green); the whole solution green twice locally and on both legs (covered). `Broken` is a plain property
  read by the host's threads; its writes are ordered before each request by the socket round trip (DERIVED; H16 green
  in each of my 11 runs that held it, and the seat's).

## 4. SCANS

- **gitleaks 8.30.1:** control FIRST, a token built in-process from two halves and 36 random characters, never printed,
  outside the clone: rc 1, `leaks found: 1`, moved to `g2137/_quarantine/gl-control-1`; then `gitleaks git` over
  `38a031e5..641935b5` rc 0 (`1 commits scanned`, `no leaks found`); the ten head blobs, the commit's message and the
  whole diff as `1.txt` to `12.txt` in a new folder: rc 0, `no leaks found`.
- **words.py** (sha256 6f932dc5...): `--control` `CONTROL FIRED: 13 of 13`; over the 147 added lines (`checks_c1.py`'s
  `added.txt`; 147 equals the commit's insertions) and the commit message: `WORDS: clean (2 files)`; `B2[0-9]{3}` and
  `X[78][0-9]` 0 and 0.
- **SCANS-2** (this folder's texts): `words.py` over the squash subject with `#57`, `squash-body.txt` and
  `pr-title.txt`: `WORDS: clean (3 files)`; `pr-body.md`: `product owner` 1 and `coordinator` 2 (the "Who decides"
  section) and the attribution line's 4 emoji bytes, every other class 0; `B[12][0-9]{3}` and `X[78][0-9]` 0 in all
  four; `build/squash_scan.py` (the head's, equal to BASE's: `diff --quiet` over `build` and `.github` rc 0) with
  `#57`: control rc 1 found 2, message rc 0 found 0, `SQUASH-SCAN: clean`.
- **SCANS-3:** gitleaks over this folder's seven files and the `#57` subject under neutral names `1.txt` to `8.txt`,
  the control re-planted first (rc 1, moved to `g2137/_quarantine/gl-control-2`): rc 0, `no leaks found` (09:27).

## NOT RUN

CodeQL (kit FACTS 5; the pull request's own run). The chain's publish and release guard, `unittest`, `repo_rules.py` and
`run_step.py`'s neutral scan locally (RELAYED from the seat; equal on the hosted legs, my read: GUARD 14 and 15, `Ran 117
tests`, `RULES: clean (679 files)`, the hosted neutral scan). A managed stack of a hung Server.Tests host (no hang
occurred in my runs). Linux or Windows probes (macOS arm64 only; the hosted legs are the other platforms' read). Any
device.

## OUTSIDE THE FENCES

None written outside my two folders. Writes: this folder and `fleet/state/s332/g2137/` only (my clone, its two
worktrees, logs, scratch, tools, quarantine). No pull request, no push (the clone's push URL is `invalid://no-push`), no
re-run of a hosted job, no `cd` run, nothing deleted, no printer or device, no Azure, nothing to any person, no Jira.
Every gh call a GET under the project's GH_CONFIG_DIR. Reads of the project folder, by path only (no recursive read):
the seat's STATUS, `CLAUDE.md` (line 82 and its sha256), `BACKLOG.md` (items 119 to 123 and 137 to 138 by line, sha256
ba8ab83e unchanged), the seat's logs folder listing and three of its logs (`green-whole.log`, the sample, the
`mt-` names), and the lock folder's absence. Two other processes on the machine were read by `ps`/`lsof` only: none of
mine was left running. Two hook refusals, each a STOP for that action: a `git worktree add` whose path was a shell
variable (read as outside TUESDAY; re-issued with the literal scratch path), and an `echo` separator starting with `=`
(re-issued as `----`). One advisory from a hook on a pipeline's exit code
(re-issued with the command alone). No print of `kam_rulings_today.sh` or `kam_msgs.sh` was made or saved. No
background process of mine is left running; the wave lock is absent.
