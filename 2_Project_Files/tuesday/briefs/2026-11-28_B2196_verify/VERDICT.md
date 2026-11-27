GATE B2196: GO WITH FINDINGS @ ef1eb24 on main e1802e2

Gate G1, ROUND 1 OF 2 of lane L3a (the host's composition, part A: Suite settings, the HTTPS certificate from the secret
store under the strict host-name rule, the landed libraries wired lazily), one Opus reader (claude-opus-5-5),
in-session, read-only, for Tuesday s337. Kit B2188 (seat X97; S4: Q1 "a" IN WORDS, Q2-Q8 the defaults; S8 the
canonical runner 31adedc8; every choice the coordinator's). Head `ef1eb24d29d207acedeb828f69bbdf13c5f0566f` on
`b2188/x97-l3a-host-composition`, ONE commit, one parent `cf224e1fa9050344a64d48913515654db6a80da7` (PR 61), tree
`1f7dd21124fd428962f8294cd433df138d81ea0f`, 750 files; `diff --name-status cf224e1f ef1eb24d`: 12 rows, 6 A, 6 M, all
under `src/Datasec.Suite.Server/` and `tests/Datasec.Suite.Server.Tests/` (re-measured by gh api GET 02:49:09: compare
ahead 1, behind 0, 12 files; `matching-refs/heads/b2188` one row = the head). **Main MOVED twice during the gate:** PR
62 (L2 Entra) -> `d9f89115`, then PR 63 (L1c contracts) -> `e1802e24d87bf8663f3f904ff478a833d483268f` (main at
03:43:38, open PRs 0); neither touches any owned or used path; the gate built the squash on each: on e1802e24 tree
`e9a3684d`, 780 files, whole solution 2564 / failed 0, RULES 780 (landing.txt). Measured 2026-11-28 02:48 to 03:50
AEDT in scratch `fleet/state/s337/g2196/` (`clone`: clone.py draft, push URL `invalid://no-push`, no identity, detached
at the head; worktrees `main-wt` (cf224e1f), `sq` (d9f89115 + head blobs), `sq2` (e1802e24 + head blobs); every mutant
and probe ran there and was undone or moved out: clone porcelain 0 rows at the end, sq/sq2 exactly the 12 overlaid
paths). Every heavy job through my copy of the kit's `heavy.py` (8 of 8 tool hashes equal THE TOOLS; heavy.py
`31adedc8...` = S8) under the OXPd wave lock, one holder at a time; 73 released lock folders of mine in
`g2196/_quarantine/locks/`; gate B2195's `owner.txt` read while it held the lock, never broken; lock free and no process
of mine left at the end (`ps` 0 rows naming g2196). Nothing to any printer, device, tenant, Azure, Microsoft host or HP
(every socket was 127.0.0.1 inside a test process); no Jira; no write to the project checkout, the seat's lane or GitHub.

## Grades (round 1 of 2): Blocker 0, Major 0, Minor 2, Info 9. Nothing blocks landing; no fix round.

**F1 MINOR (the hang question's by-product; seat R18 (c) is wrong for the cells): a refused build leaks the half-built
host, and the rig cannot dispose it.** `ServerHost.Build` throws after `builder.Build()` for every `StoreCertificate`
refusal and before it for `SuiteHostOptions` refusals; nothing disposes the `WebApplication` (or the builder's
configuration) on the way out, and `CompositionRig._app` stays null because `Build` never returned, so the rig's
`DisposeAsync` has nothing to dispose. The seat's "in the cells the rig disposes what it built" does not hold for any
refusal. MEASURED (probe h2, macOS arm64, three rounds): each batch of 20 refusals after `builder.Build()` adds about
20 threads and 326 file descriptors that never come back (16/108 -> 39/535 -> 59/861 -> 78/1181), while 20 builds the
rig disposes add none (39/535 -> 39/535). The cells make about 24 such refusals per run (W02 4, W03 2, W04 6, W11 12).
Production: the process ends on a refusal, so no effect. Tests: a resource leak that grows with every refusal cell
(on Linux each leaked host also keeps its file watchers); not a hang (no wait), and the hosted legs pass. Fix shape: in
`ServerHost.Build`, dispose `app` when `StoreCertificate.Load` throws (a try/catch around the one call), and the rig
needs nothing. A follow-up, or L3b (same files).

**F2 MINOR (the kit's gate question "an exception swallowed into a pass, a refused certificate left undisposed"): a
malformed enhanced key usage extension leaves `Load` raw, with the certificate undisposed.** The EKU loop
(`StoreCertificate.cs:104-117`) is outside every try: MEASURED (probe p1j, an EKU extension whose value is an OCTET
STRING) -> `Build` throws `CryptographicException` "ASN1 corrupted data." (inner `AsnContentException`), not a
`SuiteHostException`; the re-imported certificate and its issuers are not disposed (the `finally` disposes only the
store values and zeroes the buffers, which it did: handed out 2, disposed 2). Fails CLOSED (the host does not build) and
the message carries no value, so P1 and P6 hold in substance; but README's "the host refuses to build, with one of
these kinds" is wider than the code. Also: the gate's mutant `gRefusedKept` (remove `certificate?.Dispose();` in
`Refused`) SURVIVES: no cell checks that a refused certificate is disposed. Fix shape: move the EKU read inside the
name-check style try (any exception -> `TlsNotServerAuth`).

**F3 INFO (Tuesday's point b, MEASURED, probe3 b1-b8): two certificates in the certificate secret: the FIRST one is
the certificate, always; nothing is searched or chosen.** The secret store holds one value per name, so "two
certificates matching the host name" can only be two PEM blocks in the one certificate secret. `CreateFromPem` takes
the first CERTIFICATE block; `ImportFromPem` puts the rest into the chain unchecked. [expired, valid] + valid's key ->
`TlsUnreadable` (key of another certificate); + expired's key -> `TlsNotValidNow`; [valid, expired] + valid's key ->
loads and serves the valid leaf (pinned client 200; a client pinned to the expired one refused) with the EXPIRED one
sent as an issuer; [short-lived, long-lived] + short's key -> serves the 0.5 h one; + long's key -> `TlsUnreadable`;
[long, short] + long's key -> serves the 48 h one. Two blocks with no line break between them (what
`ExportCertificatePem()` + another export gives when joined directly) -> `TlsUnreadable` (MEASURED: `CreateFromPem`
"do not contain a PEM with a CERTIFICATE label"; `ImportFromPem` count 0). Fail-closed in every shape; the rule "leaf
first, then its issuers, each block on its own lines" is the AZ lanes' contract (README states leaf first; the line
break is not stated). Kestrel's own OS-store selection (`Certificate:Subject`/`Store`, no `Suite:Tls`) is the
framework's, unchanged by this lane, UNMEASURED here (no store write on this Mac). Named limit (pr-body 2).

**F4 INFO (seat R18 (a), MEASURED p6a): a local secret store that cannot open, with `Suite:Tls` set, refuses the build
with `SecretStoreException` "The key file of the secret store was refused." (fixed text, no folder or partition in the
message), not `TlsStoreFailed`**, because C5 resolves the store outside `Load` (the kit's call shape). A store that
throws on either READ is `TlsStoreFailed` (W04; probe p3e: a store that throws on the second read -> `TlsStoreFailed`,
the first value disposed).

**F5 INFO (P4 beyond the kit, MEASURED p4a/p4b/r1): the host's Graph client follows no redirect and sends no header of
its own, and it DOES use the machine's proxy settings.** `SuiteHttp.Handler`: `UseProxy` true, `Client.Timeout` 100 s,
`PooledConnectionLifetime` infinite, `Credentials` null, `PreAuthenticate` false, no decompression. A 307 to another
loopback port: status 307 returned, the second port never connected, `DefaultRequestHeaders` 0 after use (r1, with
NO_PROXY for loopback). Without NO_PROXY the request went to the runner's closed proxy `127.0.0.1:9` even for a
loopback address (p4b: "Connection refused (127.0.0.1:9)"): the environment's `HTTPS_PROXY`/`HTTP_PROXY` are honoured.
Graph addresses are https only (`GraphOptions` refuses an http base address, p5c), so a proxy sees a CONNECT tunnel,
not the token; for L3b and the AZ lanes: the VM's proxy variables steer Graph traffic.

**F6 INFO (P1/P2 shapes outside the cells, MEASURED, all fail-closed or harmless):** accepted: CN and SAN in upper
case (served, 200), a SAN with a trailing dot, a SAN list holding another name and a wildcard beside the host name
(served), CRLF line ends, a PKCS#1 `RSA PRIVATE KEY` and an ECDSA P-256 pair (both served; README says PKCS#8);
refused: CN only with no SAN (`TlsNameMismatch`), EKU anyExtendedKeyUsage only (`TlsNotServerAuth`), a UTF-8 BOM
before the PEM (`TlsUnreadable`), the two secrets swapped (`TlsUnreadable`), an encrypted PKCS#8 key (`TlsUnreadable`),
host names `PrintSuite.Example.Test`, `1.2.3`, `0x7f.1`, `127.0.0.1` (`InvalidOptions`, also with no `Suite:Tls`);
`999.999.999.999` passes the host-name rule (not an IP to `IPAddress.TryParse`; harmless). Two sources: every Kestrel
form refused `TlsTwoSources` (`Certificates:Default:Path`, endpoint `Certificate:Subject`+`Store`, lower-case
`kestrel:endpoints:https:certificate:path`, an SNI entry's `Certificate:Path`, and `Certificate:Password` alone, which
is over-broad but safe); `EndpointDefaults:ClientCertificateMode` alone is not a certificate (builds). `Suite:Tls` does
NOT make the host HTTPS-only: an HTTP endpoint beside it starts and `/health` answers 200 over plain HTTP (p2g; the
landed H05 keeps callbacks 403 there). Named limit (pr-body 5).

**F7 INFO (Tuesday's point a, THE HANG): not reproduced; not this lane's; the new cells hold no unbounded wait.**
Server.Tests ALONE through the runner (`-noColor -reporter verbose -longRunning 30`, TIMEOUT 900, the per-cell logger
the commission allows): head 5 of 5 green, `Total: 43`, Time 17.447, 17.124, 16.375, 15.606, 16.739 s, long-running
lines 0 in every run; main cf224e1f 3 of 3 green, `Total: 18`, 10.931, 10.351, 10.879 s; then 3 more head runs after
the probes 15.5, 15.2, 15.4 s. Whole solution on the head 2 of 2 green (`total: 2513`, 67 s each; Server.Tests dll 54 s
inside them), and on both squash trees (2564; Server.Tests dll 56 s and 54 s). The seat's hung log
`<lane>/logs/r-chain-test.log` shows the dll started and never reported, with no cell red (the runner prints no cell
line, so the cell is unknown). By reading: every new cell's start and stop go through the landed `BoundedAsync` (60 s),
every client has `Timeout` 60 s, `Assert.Throws(() => rig.Build(...))` is synchronous and local (CreateBuilder, the
store read, RSA key generation), `RefreshAsync` throws synchronously, and no cell binds a port but the host's own
127.0.0.1:0 or opens an OS certificate store (no `X509Store` in the diff; the PKCS#12 import is in memory). The only
unbounded steps are `ServerHost.Build` itself and RSA key generation, both CPU-bound and finite. The executable's time
rises (local 10.5 -> 16.5 s alone; hosted windows 12.454 s on cf224e1f -> 53.426 s on the head; about 60 RSA-2048 keys
per run) and each refusal leaks a host (F1); neither is a wait. The hang predates the lane (2026-11-25 and 2026-11-27,
owed 137). Not Major: no evidence this lane makes it more likely beyond a longer run.

**F8 INFO (mutants):** the kit's nine rows (seat's rows file, sha256 `a65964cf...` = the seat's), re-run by the gate on
ef1eb24d (the seat ran them only on its first, pre-rebase head): `MUTANTS: 9 of 9 MATCH, 9 of 9 undone equal`, the
same red cells as the seat's (W11 also red under five, inside the suite). The gate's own nine rows (sha256
`99aee3f5...`, suite W01-W11 + H01-H18): MATCH `gCertValueKept` (W01), `gStoreReadAlways` (W06, and H08), `gCookiesOn`
(W08), `gEagerSpool` (34 red, W09 among them: lazy wiring is guarded); SURVIVE (no cell): `gRefusedKept` (F2),
`gZeroDropped` (zeroing is not observable without reflection; by reading the `finally` zeroes both char arrays and the
export on every path), `gNameCatchPasses` (no shape makes the name read throw), `gKestrelCaseSensitive` (no lower-case
cell; probe p2c shows the code refuses it), `gHostUpperTaken` (no upper-case cell; probe p1f shows it refused). Every
row undone equal; clone porcelain 0 rows after.

**F9 INFO (README accuracy):** "every buffer filled with their text is zeroed ... (cell W01)": W01 proves the store
values disposed, not the buffers zeroed (F8). "The key text never becomes a string": true of this code; the framework's
PEM parsing inside `CreateFromPem` and the PKCS#12 export/import are not inspected (UNMEASURED). "one of these kinds":
see F2 and F4.

**F10 INFO (scope):** `MyDriveFiles` (L5 slice 2, landed after the kit was drafted) is not wired; L3b wires it with a
download client that carries no default Authorization header (its README's rule). The registry and `IAppModule` are
out by Q1 "a".

**F11 INFO (process):** the seat's DEVIATIONS are complete but for R18 (c) (F1); its mutants were not re-run after the
two rebases (the gate did: F8). My own: one shell call of mine held a `cd` and was REFUSED by the hook before it ran
(nothing executed); two copy attempts were refused by the path hook and redone by `cat >` from the seat's file (read
only); the first two-certificate probe joined PEM blocks with no line break and measured that shape (kept as F3's last
shape), then re-measured the documented shape (probe3).

## THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), whole
- **`<BASE>..<head>` read whole:** 12 files, 6 A, 6 M; `checks_l3a.py <clone> cf224e1f g2196/checks`: `CHECKS: 9 of 9
  PASS`, each control FIRED (1 rows 12 A 6 M 6; 3 references Adapters.Oxpd2 Core Graph Jobs OneDrive Secrets Sessions,
  package WindowsServices; 4 package entries 21, not in any BASE lock file 0; 6 BASE 18/0/0, head 24/5/19, W01-W11 once
  each; 7 one `new HttpClient(`, `AllowAutoRedirect = false`, `allowWildcards: false`, `allowCommonName: false`,
  `IPAddress.TryParse` once each, `DefaultRequestHeaders` 0; 8 HostCellTests.cs 2 removed 2 added, the H12 lines);
  `ADDED: 1141 lines, 108 lock-file lines`.
- **The pin run and each mutant's reds:** the seat's pin `Total: 43, Failed: 0` read in its log; the gate's runs of the
  head: Server.Tests 8 of 8 `Total: 43, Failed: 0`; mutants F8.
- **Can any path serve a certificate that fails D3 or D4?** No. Order: store read -> present -> readable (PEM +
  PKCS#12 re-import) -> valid now -> EKU -> CN and SAN; each check throws; the only swallowed exception is the name
  read's, mapped to `named = false` (a refusal, never a pass). The served object is the checked object (`certificate`,
  the re-imported one). With `Suite:Tls` a Kestrel certificate is refused (all forms, F6), so Kestrel's own certificate
  path cannot serve beside it; the HTTPS defaults delegate sets the store's certificate only when `served` is set
  (W01 serves it, pinned). A refused certificate IS disposed on every `Refused(...)` path; NOT on the malformed-EKU path
  (F2); no cell proves the disposal (gRefusedKept survives).
- **Key text as a `string` or in an unzeroed buffer?** No string in this code: `Encoding.ASCII.GetChars` into `char[]`,
  `CreateFromPem(ReadOnlySpan<char>, ReadOnlySpan<char>)`, the export `byte[]`; the `finally` zeroes both char arrays
  (`Array.Clear`) and the export (`ZeroMemory`) on every path, including the `AsciiChars` refusal; the two
  `SecretValue`s are disposed on every path (MEASURED: every refusal shape of p3a-p3e and p1-b: handed out = disposed;
  SecretValue.Dispose zeroes its bytes, `SecretValue.cs:39-43`). Framework-internal copies: UNMEASURED (F9).
- **Store read when `Suite:Tls` is absent?** No: `Load` runs only when `CertificateSecret` is set; W06 `HandedOut`
  empty; the gate's `gStoreReadAlways` turns W06 red; p2h (`Suite:HostName` only) reads nothing.
- **`TlsTwoSources` against every Kestrel certificate form?** Refused: `Certificates:Default:Path`, endpoint
  `Certificate:Path`/`KeyPath` (W05), `Certificate:Subject` + `Store`, lower-case keys, SNI `Certificate:Path`,
  `Certificate:Password` alone (F6). Environment variables map to the same configuration keys (the framework's
  `__` -> `:` rule; not separately run).
- **Messages carrying a name or value?** None found: W11 (22 messages) plus every probe message (F6, p5, p6): only
  `Host composition refused: <kind>[, setting <key>].`; raw exceptions met: F2 ("ASN1 corrupted data."), F4 (store's
  fixed text), `JobServiceException` "The disk refused a spool operation." for an absolute but unusable spool root
  (p5g); none holds a value.
- **The Graph client following a redirect or sending its own header?** No (W08; F5 r1: 307 returned, never followed,
  no default header; GraphClient sets no default header or base address by `grep -n -i` over `src/Datasec.Suite.Graph`).
- **Any library made at build or start?** No: every registration is a factory singleton; the host starts with no
  spool root, a `Mars` cloud or `Custom` without an address (W09, p5a-p5i), each refused at first resolve with its key
  (`GraphClient`, `MyDriveBrowser`, `JobSpool`, `ScanReceiver`); `gEagerSpool` (refusal at registration) turns 34 cells
  red. `ITokenBroker` resolves over an empty store (p5j); `custom` lower case accepted (p5d).
- **The two lock files and the locked restore on both legs:** check 4 PASS (21 entries, all in a BASE lock file); the
  lock diff adds the six Project entries and Serilog 4.4.0 / Serilog.Sinks.File 7.0.0 CentralTransitive in `net10.0`
  only; locked restore rc 0 locally (head, main, both squash trees) and on both hosted legs (`dotnet restore
  --locked-mode` steps success, `NU1004` 0 lines in either log).
- **The publish listing difference:** the gate published head and main cf224e1f (the workflow's two lines, CI=true):
  linux 28 vs 14, windows 29 vs 15; missing from head none; added exactly `Datasec.Suite.{Graph,Jobs,Logging,OneDrive,
  Sessions,UniversalPrint}.{dll,pdb}`, `Serilog.dll`, `Serilog.Sinks.File.dll` (14 each leg); `release_guard.py`
  `GUARD: clean (28 files)` / `(29 files)` on head, 14 / 15 on main.
- **The hosted run on both legs:** gate's `hosted3.py ef1eb24d... --total 2513 --rules 750 ... --guard-linux 28
  --guard-windows 29`: `HOSTED ef1eb24d...: PASS` (linux succeeded 2509, windows 2492, skipped 4 / 21; rules 750, floor
  117; secret-scan all controls); Server.Tests dll passed on linux (10.1 s) and windows (53.4 s).
- **The kit's mutants re-run through the canonical runner:** F8, 9 of 9 MATCH.
- **`words.py` and gitleaks:** `words.py --control` `CONTROL FIRED: 13 of 13`; over `added.txt` and the commit message
  `WORDS: clean (2 files)`; B-numbers `B2[0-9]{3}` 0 and 0 (control: the kit 28). gitleaks 8.30.1: control FIRST (a
  token built from halves and random characters, never printed) rc 1, moved to `_quarantine/`; the 12 head blobs,
  `added.txt`, `added-locks.txt` and the message under neutral names (15 files) rc 0; `gitleaks git` over
  `cf224e1f..ef1eb24d` rc 0; `src/Datasec.Suite.Server` and `tests/Datasec.Suite.Server.Tests` (bin and obj included)
  rc 0. The commit message equals the kit's `commit-message.txt` byte for byte (259 bytes).
- **CodeQL:** the pull request's own run (FACTS 6); main e1802e24's analyses csharp / python / actions 0, open alerts 0.

## TUESDAY'S POINTS
(a) The hang: F7. (b) Two certificates: F3.

## ADVERSARIAL: three shapes outside each property (each covered, measured or a named limit)
- P1 (certificate rules): upper-case CN/SAN served; CN-only refused; anyEKU refused; malformed EKU refused raw (F2);
  first-of-two-certificates rule (F3); PKCS#1 / ECDSA accepted (F6).
- P2 (one source, no store read): SNI, Default, Subject/Store, lower-case forms refused; HTTP endpoint beside `Suite:Tls`
  served (limit); no-Tls host-name refusal reads nothing.
- P3 (disposal and zeroing): store throws on the second read (first value disposed); key missing (1 of 1 disposed);
  expired / name / garbage refusals (2 of 2); zeroing by reading only (F8).
- P4 (Graph client): 307 not followed; proxy honoured (F5); 100 s timeout and infinite connection lifetime (F5).
- P5 (lazy): unknown cloud, relative or http custom address, whitespace or unusable spool root, ScanReceiver and
  MyDriveBrowser through their dependency: each refused at first use, host started (p5).
- P6 (messages): store-open failure (F4), malformed EKU (F2), unusable spool (p5g): fixed texts, no value.
- P7 (landed cells): H01-H18 green in every gate run; under the kit's mutants none red; `gStoreReadAlways` turns H08
  red (expected: it reads the store).

## NOT RUN
Local CodeQL (FACTS 6). The TLS chain a client receives (R13: no cell; the gate's probes pinned the leaf only). Kestrel's
OS-store certificate selection (no store write on this Mac). Windows behaviour of the leak (F1) and of PKCS#12 key
persistence for the served certificate (UNMEASURED). The seat's hung executable's cell (the log has none; not
reproduced).

## MAIN AT THE END
`e1802e24d87bf8663f3f904ff478a833d483268f` (PR 63), open pull requests 0, code scanning 0 open, 03:43:38 AEDT; push
run `HOSTED e1802e24...: PASS` at 2539 / 774 / 14 / 15. The squash of the head on it: tree `e9a3684d`, 780 files,
whole solution `total: 2564`, `failed: 0`, `succeeded: 2560`, `skipped: 4`, `RULES: clean (780 files)`.

## LANDING
`landing.txt` (steps, totals 2564 / 2560 / 2543 / 780 / 28 / 29 on e1802e24, MAIN MOVES), `pr-title.txt`,
`pr-body.md`, `squash-subject.txt` (210 characters with the placeholder; `SQUASH-SCAN: clean` with #64; words clean over
subject, body and title), `squash-body.txt`, `FOR-RECORDS.md`. Recommendation: land as GO WITH FINDINGS; F1 and F2 are a
small follow-up in the same two Server folders (or the first lines of L3b), never side by side with L3b.
