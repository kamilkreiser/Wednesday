GATE B1980: NO GO @ 1fca08c on main da8d64a

Gate G1 (security surface: TLS pin, the device admin password, network input), round 1 of 2 of lane X1, one Opus reader
(claude-opus-5-5), in-session, read-only. OXPd 1.x lane X1, kit B1976 (seat X49; Q1 = a in words at stamp S4, Q2 to Q6
the defaults, each the coordinator's, none the product owner's). Head `1fca08cf0edff8be961e8e7cc1aa065bff4eb96f` on
`b1976/x1-oxpd1-read-client`, ONE commit, one parent BASE `da8d64a8`. Read and measured 2026-11-23 12:18 to 12:45 AEDT
in my own scratch `fleet/state/s316/g1980/`: `clone` (the kit's `clone.py ... draft`: push URL `invalid://no-push`, no
identity; detached at the head), worktrees `red` (BASE + `1-red.diff` + the 14 HP files, then + `2-fix.diff`) and
`probe` (the head + my probe file, never committed). Every dotnet job through the kit's `heavy.py` (sha256
`31adedc8...`) and the wave lock `.tools/wave1-heavy.lock.d`, one at a time (lock waits 0 to 7 per job, load1 5.0 to
6.8); no other holder's lock touched. Origin by `gh api -X GET` under the project GH_CONFIG_DIR at 12:19: main
`da8d64a8` (unmoved since the seat's push); `matching-refs/heads/b1976` one row, `1fca08cf`; `compare main...1fca08cf`
ahead 1, behind 0, 30 files, every status `added`, +7742 -0, merge base `da8d64a8`; open pull requests 0 (newest 32,
closed, merged); open code-scanning alerts on main 0; repository private. No write to the project, GitHub or Jira; no
push, no pull request, no re-run; no `cd`; nothing deleted (the gitleaks control moved to `g1980/_quarantine/`).

**BLUF.** The head is BASE plus the two frozen patches, the 14 HP files and the two restore-written lock files, byte for
byte (tree `32057fba`, 30 `A` rows, nothing outside the three folders). The 14 HP files equal the jar's
`META-INF/wsdls/` entries by sha256 (14 of 14). Red first reproduces (18 / 13 failed, the kit's 13 cells, each an
assertion), the head is green (18 / 0), and all 14 mutants are red on exactly their cells and undone (my own
independent run). The whole solution is unchanged (1809 / 0, RULES 583, Ran 111), and the hosted run of the head and of
main both read PASS. The pin holds: the one certificate callback refuses a null certificate and a chain-only match
(measured). **But my probe found that the client breaks two of its own four properties on inputs no cell sends:**
(1) **a ~35 kB answer of nested elements crashes the whole process with a stack overflow** (uncatchable; on the
discovery-tree GET as well as a SOAP read), so "every call ends in one typed outcome" is false; (2) **the admin
password comes back in the returned answer** when the device's echo of it is split by a CDATA section, or when the
password is an element or attribute name (the record stays clean), so "never ... returned" is false. Also (3) the
WS-Addressing namespace the client sends (2004/08, with mustUnderstand) is NOT the one HP's committed descriptions use
(2005/08 and 2006/05): whether a device faults every call on it is UNMEASURED, but the kit's stated reason does not
hold. And (4) `Timeout = InfiniteTimeSpan` is accepted and turns every time bound off. **NO GO: a fix round (round 2 of
2).** Nothing here is a leak to the network or a trust bypass. The lane is HELD from landing anyway (kit Q3: after L1
and the slnx round), so the fix round costs no landing slot.

## FOUND

1. **Major (P4, the README's "Typed ends": a device answer crashes the host process).** `Oxpd1Soap.Mask`
   (`Oxpd1Soap.cs:138` to `:174`) copies the answer by recursion (`copy.Add(Mask(child, values));`, `:165`), and
   nothing bounds the nesting depth: `Parse` (`:60` to `:80`) sets no depth limit and `MaxAnswerBytes` bounds bytes
   only. MEASURED (probe, the stub on 127.0.0.1 with the right pin, `ForceBody`): a GetManufacturerInfo answer with 1000
   nested elements in its Result: `Answered`; with 5000 (35,283 bytes, 3.4% of the default 1 MiB bound): the test
   process died with `Stack overflow.` (rc -6), every repeated frame `Oxpd1Soap.Mask` (`logs/probe-deep-1.log` line 5
   on). The DISCOVERY TREE path (the unauthenticated GET, `Judge` with no row masks the whole document) died the same way
   at 5000 (35,031 bytes, `probe-deeptree-1.log`). A second recursion sits in the framework on the fault path: nesting
   inside `s:Code/s:Value` read by `.Value` (`Oxpd1Soap.cs:108`) survived 20,000 and died at 60,000 (420,147 bytes,
   under the bound) in `System.Xml.Linq.XContainer.AppendText` (`probe-deepfault-1.log`). A stack overflow cannot be
   caught in .NET: the whole host (the lab command, later the server) ends, not the call. Who can send it: only a
   device whose certificate is pinned (the pin is checked before any byte of an answer), so a broken or compromised
   printer; that is exactly the input this client exists to distrust (P4, H12 to H14). Not seen by the cells: no cell
   nests. The depth at which it dies depends on the thread's stack (macOS arm64 here; Linux and Windows UNMEASURED).
   **Fix (one direction; the coordinator's):** bound the depth while reading, before `XDocument.Load` (for example
   read with the `XmlReader` and refuse `reader.Depth` above a small fixed bound as `MalformedAnswer`), so neither
   recursion is reachable; a cell that nests past the bound in a result, in the tree and in a fault code (each
   `MalformedAnswer`, and the process alive) and one under it (`Answered`), and a mutant that removes the bound.

2. **Minor (P3, the README's "never logged, recorded or returned", `README.md:25` to `:29`): the returned answer can
   hold the admin password.** `Mask` scrubs each text node on its own (`:167` to `:169`, and a `CDATA` section is an
   `XText` there), and keeps element and attribute NAMES as they are (`:140`, `:149`). MEASURED (probe; the record
   file scanned by `LogScanner.Scan` with the password and `admin:<password>`; outcomes and booleans only, no value
   printed): the device's echo of the password split by a CDATA boundary inside a note (`synthetic-ad<![CDATA[...]]>`),
   in a SOAP answer (A1), in the tree (A2) and as two CDATA sections (A2b): `Answered`, and BOTH `Answer.ToString()` and
   `Answer.Value` hold the password (Mask writes the two parts as adjacent plain text, which serialise as one); the
   record scan is clean (the record scrubs the serialised string, `Oxpd1Client.cs:225`). The password as an element
   name (A3) or an attribute name (A4): `Answer.ToString()` holds it, record clean. K12 plants the echo as one text node
   only, so it cannot see this. The same probe shows the paths that DO hold: a character reference (A7), the Basic form
   (A9), an attribute value (A11), a comment (A12), a processing instruction (A13), a fault code that is, or is split
   around, the password (A5, A6, A6b): nothing in the answer, the fault code, `ToString()` or the record. Severity
   Minor: it needs a pinned device that echoes the password in a split or name form, and the value goes back to the
   caller that supplied it, not to a sink; but the README states "never" and the returned answer is what a caller logs.
   **Fix:** scrub the joined text of each run of adjacent text and CDATA nodes (or the element's whole `Value` before
   copying), and treat a secret inside an element or attribute name as `MalformedAnswer`; a K12 row for each shape.

3. **Major for function, UNMEASURED on a device (D3 / Q2, the coordinator's): the WS-Addressing namespace the client
   sends is not the one HP's committed descriptions use.** `Oxpd1Soap.cs:16` sends
   `http://schemas.xmlsoap.org/ws/2004/08/addressing` (August 2004), with `s:mustUnderstand="1"` on `Action` and `To`
   (`:31`, `:39`), and `ReplyTo` the 2004/08 anonymous role (`:17`). MEASURED over the 14 files at the head
   (`scratch/wsa.py`, prefix use counted beside each declaration): the 2004/08 `wsa` prefix is DECLARED in all 8 WSDL
   files and USED 0 times; the four bindings each USE `wsa10` = `http://www.w3.org/2005/08/addressing` (WS-Addressing
   1.0: `wsa10:EndpointReference`, 2 uses each); the four port-type files USE `wsaw` =
   `http://www.w3.org/2006/05/addressing/wsdl` (the WSDL binding of WS-Addressing 1.0) for every operation's Action (36,
   12, 8, 4 uses); the files also declare `msc` (`schemas.microsoft.com/ws/2005/12/wsdl/contract`). So kit D3's reason
   ("the binding files declare that namespace") is true of the declaration only; every addressing element the files
   contain is 1.0. Under SOAP 1.2 a header block with `mustUnderstand="1"` that the node does not understand ends in a
   `MustUnderstand` fault (the SOAP 1.2 processing rule; DERIVED, not from a file here); what a FutureSmart 5 device does
   is UNMEASURED. If it faults, every one of the five reads ends `Fault` at the first commissioned connection (fail
   closed: no write, no leak). The stub cannot see it: it reads `Action` in the same hard-coded 2004/08 namespace
   (`StubDevice.cs:203`). **Fix (the coordinator's choice, before the first connection):** send WS-Addressing 1.0
   (`http://www.w3.org/2005/08/addressing`, anonymous `http://www.w3.org/2005/08/addressing/anonymous`) as the
   descriptions do, and have the stub take the namespace from the binding files (so C03/K01 compare it); or keep 2004/08
   and record the evidence against it; or send no `mustUnderstand`.

4. **Minor (P4 and the options' "The time one call may take", `Oxpd1ClientOptions.cs:83` to `:84`): an infinite time-out
   is accepted and turns every bound off.** `Timeout` has no check of its own. MEASURED: `Timeout =
   Timeout.InfiniteTimeSpan` constructs (the handler's `ConnectTimeout` accepts infinite) and a read of a stub that
   waits 3 s ended `Answered` after 3016 ms (C3): no bound applies, so a device that never answers holds the call
   forever. Zero, -5 s and 30 days each throw `ArgumentOutOfRangeException` from the CONSTRUCTOR (C4, C5, C5b), the
   handler's own check, not the options'. **Fix:** the options refuse a time-out that is not positive and finite (and
   above a cap), with a K07 row.

## INFO

1. **The pin (the commission's question on `Pinned`).** `Oxpd1Client.cs:202` to `:215` (printed above by the seat and
   re-read at the head): a null certificate falls to the refusal; `chain` and `errors` are never read. MEASURED by calling
   the callback (reflection, probe B): null certificate with `RemoteCertificateNotAvailable`: false (B1); null with
   `None`: false (B1b); an UNPINNED leaf with a chain that builds to the pinned authority, errors `None`: false (B2);
   the pinned authority itself as the leaf: true (B3: it is the pinned certificate); the pinned certificate with
   chain-errors and name-mismatch both set: true (B4: the pin is the whole trust, kit D5; name and expiry are not
   consulted, by design). Over the 1814 added lines of `src/`, `tests/` and the contracts README, the only certificate
   callback is `Oxpd1Client.cs:49` (`RemoteCertificateValidationCallback = Pinned`) and its method `:202`; no
   `ServerCertificateCustomValidationCallback`, `DangerousAcceptAnyServerCertificateValidator`, `ClientCertificates`
   or second handler (pattern count 2, control: the callback line found). Nothing trusts a certificate the pin did not.
   TLS session resumption is not exercised by any cell (K04 closes each connection): UNMEASURED.
2. **Text paths for the password (the commission's question).** Exception messages: the library's five `throw` sites
   (`Oxpd1ClientOptions.cs:29`, `:34`, `:42`, `:76`; `Oxpd1Read.cs:86`) hold fixed text or the enum value; MEASURED,
   every exception the probe met (C1, C2, C2b, F1, F2, F3) has `ToString()` without the password. Fault code: scrubbed
   after `.Value` joins its parts (A5, A6, A6b: no password). `SettingName` in the record is `_options.AdminPasswordSetting`,
   the NAME (`Oxpd1Client.cs:228`); a caller who names the setting with the password itself would record it (the seat's
   H17: a named shape, no cell). The record: clean in all 14 A probes. FOUND 2 is the one path that carries it.
3. **Cancellation and time-outs, MEASURED.** A caller's token cancelled before the call or 300 ms into a 3 s call (a
   read, and the tree): `TaskCanceledException` (C1, C2, C2b), never an outcome (the seat's H18; `Oxpd1Client.cs:120`'s
   filter); true to the wording "never throws for a device answer or a transport fault", but the README does not say
   it. TCP accepted and TLS never answered, `Timeout` 1 s: `TimedOut` at 1002 ms (C6, and the tree C6b); headers then
   one body byte per 300 ms, 1.5 s: `TimedOut` at 1503 ms (C7); the response head trickled: `TimedOut` at 1503 ms (C8).
   The linked token covers the body read (`:117`), so no hang with a finite time-out. Two events, two orders: the
   time-out first and then the caller's cancel before the catch runs ends as the caller's exception (the filter reads
   the caller's token at catch time; DERIVED, not run).
4. **Bounds, MEASURED.** A 200 kB response header: `TransportFailed` (D1; the handler's default header limit). A body
   of exactly `MaxAnswerBytes`: `Answered`; one byte less: `TooLarge` (D6, D6b). `MaxAnswerBytes` 0 or -1 are accepted
   and every answer is then `TooLarge` (D4, D4b): harmless, unchecked. Depth: FOUND 1.
5. **Parsing, MEASURED** (the raw-TLS probe server for byte-exact bodies): an unknown declared encoding, utf-16 declared
   over UTF-8 bytes, a raw 0xFF byte, a NUL character reference, an external entity, an empty body, two Result
   elements: each `MalformedAnswer`; an answer in UTF-16 with a byte order mark: `Answered` (E3); a SOAP fault with
   status 200: `Fault` with status 200 (E10). No exception escaped `Parse` for any shape probed.
6. **Misuse, MEASURED (the seat's H20).** `(Oxpd1Read)99`: `ArgumentOutOfRangeException`, thrown synchronously by
   `ReadAsync` (not inside the task), before any send (F1); a call after `Dispose`: `ObjectDisposedException` (F2); a
   setting reader that throws: its exception, before any send (F3). A setting value of one space is not
   `NoCredential` (`IsNullOrEmpty`): it is sent, and the stub answered 403 (F4). None is a device answer.
7. **The stub's routes (the commission's question on `StubDevice.Bindings`).** Partly. `Bindings()`
   (`StubDevice.cs:148` to `:166`) reads every `*Soap12Binding.wsdl` under the committed folder at each start, and the
   SOAP route checks against it the `{service}` segment, the content type's `action` AND the `wsa:Action` (equal to each
   other), the request element's local name and namespace (`:288` to `:292`). But the route itself is a template,
   `/hp/device/webservices/OXPd/{service}` (`:184`): the prefix is a hand copy of the library's constant
   (`Oxpd1Read.cs:58`), so a wrong prefix cannot be caught (kit D2: DERIVED for three of the four services, and the
   bindings' own `soap12:address` is `http://localhost/Service`); the stub's WS-Addressing namespace is hard-coded too
   (FOUND 3); and the answers' `...Response` / `...Result` names are the library's convention mirrored. I checked those
   names against the committed schemas: all five `...Response` and `...Result` elements are declared, and each list
   type holds its record element (`OwnedAccessoryRecord`, `AuthenticationAgentRecord`, `SignInMethod`) (`xsdrec.py`).
   Whether those record elements are namespace-qualified (`elementFormDefault`) is NOT RUN (DEVIATIONS).
8. **The HP files against the jar, MEASURED.** A copy of the drafter's jar copy (`s315/d1976/jar/`, not the NAS) into
   `g1980/scratch/jar/`: sha256 `f2bb325f...3d341`, equal to plan 03's. Only `META-INF/wsdls/*` entries were read (144
   file entries; 844 class entries counted by name, none opened): the 14 listed entries equal `inputs.sha256` and the
   files at the head, 14 of 14; control: 5 other wsdls entries match no listed hash (0).
9. **The frame question (stamp checklist item 11).** See the section below.
10. **`words.py` over the whole commit's own added lines reads 4 hits, all false.** Over the 16 own non-HP files'
    added lines (1829): `seat ids 4`, every one `x64` in `net10.0/linux-x64` and `net10.0/win-x64` of the two
    restore-written lock files (BASE's 28 lock files hold 56 such); over the 14 non-lock files (1612 lines, = the
    patches' 1646 `+` lines less the 34 skeleton lines `2-fix.diff` replaces) and the message: `WORDS: clean (2 files)`.
11. **CodeQL:** the branch push ran no Analyze job (0 check runs beside the four); main's push run has the three
    Analyze rows, success. Whether the default setup's C# build analyses projects that are not in `Datasec.Suite.slnx`
    is UNMEASURED: a `csharp` results_count of 0 on a pull request of this head could be vacuous (landing.txt).

## THE FRAME QUESTION (README and kit sentences with "every", "never", "no path", "only"; three shapes not the tested one)

| Sentence | Shape handed that is NOT the tested one | Covered? |
|---|---|---|
| README:20 "No write ... five rows, each a Get operation" | a cast `(Oxpd1Read)99`; a row added; a public method added | F1 measured (throws before a send, no cell); C04 + `mReadOnlyOpen`; C04 reflection |
| README:14 "Every SOAP call goes to https://<host>:7627/..." | a public `SoapPort`/`TreePort` set by a caller; an IPv6 host; a service the stub's template accepts but HP serves elsewhere | init properties are public by design (stated); IPv6 accepted by `CheckHostName`, no cell, UNMEASURED; path prefix DERIVED (INFO 7, kit D2) |
| README:22 "accepted only when the SHA-256 ... on every handshake" | a null certificate; a chain to a pinned authority; a resumed TLS session | B1 measured, no cell; K05 and B2; UNMEASURED (INFO 1) |
| README:23 "A redirect is never followed" | 301/302/303/308; a redirect on the tree GET; a Location to http:// | K06 covers 307 on a read only; the others DERIVED from `AllowAutoRedirect = false` (one handler for both calls) |
| README:24 "only HTTP/1.1 is spoken" | the tree GET; a server that offers only h2; ALPN h2 first | K06 asserts the read only; the request sets `RequestVersionExact` 1.1 for both (DERIVED); h2-only server: no cell |
| README:25 "never logged, recorded or returned" | an echo split by CDATA; the password as a name; a case variant | FOUND 2 (A1, A2, A2b, A3, A4 return it); a case variant is kept in the answer (A10), and is not the password (README Limits) |
| README:28 "scrubbed from every text, the tree's included" | a char reference; the Basic form; a split fault code | A7, A9, A6/A6b measured clean; no cell for any |
| README:30 "Each call ends in one Oxpd1Outcome; a device's answer ... never throws" | deep nesting; a caller's cancel; misuse | FOUND 1 (process crash); C1/C2 throw, not a device answer (unstated in the README); F1 to F3 throw |
| README:31 "read strictly (no DTD, no external resolution)" | an external entity; a DTD with no entity; `MaxCharactersFromEntities` alone | E11 measured `MalformedAnswer`; K09 internal entity; `mDtd` the named survivor |
| README:31 "bounded (MaxAnswerBytes, refused, never truncated)" | nesting depth; header size; a declared length smaller than sent | FOUND 1; D1 measured; the handler refuses a body past its declared length (DERIVED) |
| Options:83 "The time one call may take" | `InfiniteTimeSpan`; zero; a slow TLS handshake | FOUND 4 (C3); C4 throws from the ctor; C6 measured `TimedOut` |
| README:48 "One call at a time is the tested shape" | two concurrent calls; one refused while one transports; a reused client after a refusal | named limit (H15); not run; K03 uses fresh clients (DERIVED) |

Two events, two orders where order matters: the caller's cancel and the time-out (INFO 3: whichever is seen at catch
time decides; the caller's wins when both are set); a certificate switch and a pooled connection (K04 closes each
connection: switch-then-handshake is refused; a pooled connection opened before the switch keeps its pinned session,
DERIVED); Mask then the record's Scrub (FOUND 2: scrubbing per node before serialising, and per string after, is why the
record is clean and the answer is not).

## WHAT I MEASURED

- **THE TOOLS:** `cp -Rc` of `fleet/state/s315/d1976/seat-tools/` to `g1980/gate/`: 10 of 10 sha256 equal to kit B1976's
  table; the seat's copy `<project>/.tools/b1976/gate/` also 10 of 10; the 14 HP files 14 of 14 against
  `gate/contracts-oxpd1/inputs.sha256`, 14 on disk. `words.py --control` `CONTROL FIRED: 13 of 13`.
- **THE COMMIT:** one parent `da8d64a8`; tree `32057fba19812273f46d68e8458ed884ad6bfc8d`; the stored message equal to
  `commit-message.txt` (280 bytes plus git's final LF); author and committer one address, ending `@datasec.com.au`
  (in-process, masked); `--name-status` 30 rows, not `A` or outside the three folders 0 (control: a planted `M
  Datasec.Suite.slnx` row counts 1); per folder 17 / 8 / 5; `diff --quiet` outside the three folders rc 0 (control
  inside `src/Datasec.Suite.Adapters.Oxpd1` rc 1); `ls-tree` 553 at BASE, 583 at the head; the 16 own non-HP files 0
  non-ASCII lines, 0 CR, a final LF on all but the two lock files (as BASE's) (control U+200B 1); `[Fact]` indented
  ClientTests 12, ContractTests 6, column 1 0, `[Theory]` 0.
- **THE PATCHES = THE HEAD:** worktree `red` at BASE, `git apply 1-red.diff` rc 0, the 14 HP files copied, `cmp` of the
  two lists rc 0, the three skeleton files equal the kit's red-step sha256, library README absent; after the restore
  and `git apply 2-fix.diff` rc 0, the three folders staged: `write-tree` = `32057fba`, equal to the head's tree;
  `diff --cached --stat 1fca08cf` empty.
- **RED FIRST** (`red`, BASE + `1-red.diff` + HP files): `red-restore` rc 0, both new lock files equal THE CODE's
  sha256; `red-build` `0 Warning(s)` `0 Error(s)`; `red-exe` `Total: 18, Errors: 0, Failed: 13, Skipped: 0`; the 13
  `[FAIL]` cells C05 K01 K02 K03 K04 K05 K06 K07 K08 K09 K10 K11 K12 (the kit's 13); next lines: `Assert.Equal() Failure:
  Values differ` x10, `Assert.Empty() Failure` (C05), `Assert.ThrowsAny() Failure: No exception was thrown` (K07), K01's
  `Assert.True` message `GetManufacturerInfo: TransportFailed`; the one `System.*Exception` word is K07's expected type.
- **GREEN, the head (`clone`):** `head-restore --locked-mode` rc 0, status clean; `head-build` 0/0; `head-exe` `Total:
  18, Errors: 0, Failed: 0, Skipped: 0`.
- **THE MUTANTS (independent of the seat's):** `mutants_x1.py <clone> g1980/scratch/mutants run g1980 'B1980 gate g1980'`
  as ONE call, rc 0: 14 rows, every row `Total 18`, `MATCH`, `undone equal True` (mPinAny K03 K04 K05; mRedirect K06;
  mProxy K01 K02 K03 K04 K05 K06 K09 K10 K11 K12; mNoCredential K08; mTreeUnscrubbed K12; mNoTimeout K11; m401 K09;
  mStreamBound K10; mNoMask K12; mNoScrub K12; mDtd NONE (the named survivor); mHostAny K07; mReadOnlyOpen C04;
  mWsaAction K01 K03 K04 K09 K10 K12); last line `MUTANTS: 14 of 14 MATCH, 14 of 14 undone equal`
  (`g1980/logs/mutants-run.log`). After it: status clean; `post-build` 0/0, the library dll (12:33:53) later than the
  newest source (`Oxpd1Soap.cs`, the last undo, 12:33:52); `post-exe` 18 / 0.
- **THE WHOLE SOLUTION at the head (= the merge with main of the moment):** `git merge-tree --write-tree origin/main
  1fca08cf` rc 0, tree `32057fba` (the head's: main is BASE, a fast-forward); `CI=true` `sln-restore --locked-mode` rc 0,
  30 tracked lock files unchanged by sha256; `sln-build` 0/0, 0 lines naming `Adapters.Oxpd1` (not in the solution, as
  the kit says); `sln-test` `total: 1809`, `failed: 0`, `succeeded: 1805`, `skipped: 4`, `Passed!`; `unittest discover
  build/tests` `Ran 111 tests`, `OK`; `repo_rules.py` (never `--source-documents`) `RULES-NOTE: R5 hash half NOT RUN (no
  supplied-source folder here)`, `RULES: clean (583 files)`.
- **MY PROBE** (`G1980Probe.cs`, one fact, 48 shapes, outcomes and booleans only, no value printed; a raw TLS server on
  127.0.0.1 for byte-exact and slow answers; sha256 `bd9a1b6d...` for the main run, `27378f42...` after one edit to the
deep mode only, kept as `scratch/G1980Probe.cs` and `scratch/G1980Probe-final.cs`): built 0/0 in `probe`; run whole
  `Total: 19, Errors: 0, Failed: 0` (the 18 cells and the probe; outcomes in `g1980/scratch/probe-out-main.txt`); three
  more runs with the deep shapes alone (`G1980_DEEP=1`; soap, tree, fault), each ended by the stack overflow (rc -6,
  `probe-out-deep.txt`, `probe-out-deeptree.txt`, `probe-out-deepfault.txt` and the three logs).
- **HOSTED (GET only, `hosted2.py`):** the head `1fca08cf... --total 1809 --rules 583 --skipped-linux 4 --skipped-windows
  21 --unit 111 --floor 111 --hardened-scan`: run 45091417542, attempt 1 on all four jobs, linux 1809 x2 / 1805 / 4,
  windows 1809 x2 / 1788 / 21, GUARD clean 10 / 11 files, every hardened secret-scan row OK (`NEUTRAL-SCAN: stored
  objects 1452 ...`, `91 commits scanned.`), RULES 583, Ran 111, floor 111; no Analyze rows; `HOSTED 1fca08cf...:
  PASS`. Main `da8d64a8... --rules 553`: run 45068273700, the four jobs and the three Analyze rows success; `HOSTED
  da8d64a8...: PASS`. Both equal the seat's STATUS lines.

## SCANS

- `words.py`: INFO 10 (`WORDS: clean (2 files)` over the 14 non-lock files' added lines and the message).
- gitleaks 8.30.1 `--no-banner --redact --ignore-gitleaks-allow --exit-code 1`: control FIRST (a token-shaped value built
  by program in a new scratch folder, never printed): rc 1, `leaks found: 1`, folder moved to `g1980/_quarantine/
  gl-control`; `dir` over the 30 head blobs and the message under neutral names (31 files): rc 0, `no leaks found`;
  `git --log-opts=da8d64a8..1fca08cf` over the clone: `1 commits scanned.`, `no leaks found`, rc 0.
- The texts of this folder: `words.py` over `pr-title.txt`, `squash-subject.txt`, `squash-body.txt`; gitleaks over the
  folder; `build/squash_scan.py` (from the clone's `build/`, equal to main's): see FOR-RECORDS.md SCANS.

## NOT RUN

Any run on Linux or Windows locally (the hosted legs do not run the 18 cells this round: BLUF 4 of the kit); the deep
shapes on Linux or Windows; CodeQL; `run_step.py`'s neutral scan locally (the hosted secret-scan of the head: every
hardened row OK); `repo_rules.py --source-documents` (never); any device, simulator or address but 127.0.0.1; the
`elementFormDefault` read of INFO 7 (DEVIATIONS); TLS session resumption; HTTP/2-only or renegotiating servers; two
concurrent calls; any re-run.

## DEVIATIONS

1. One hook refusal: a recursive `grep` for `elementFormDefault` over `clone/contracts/oxpd1/hp` was refused by
   `pretooluse_recursive_scope.sh` (it reads `fleet/state` as a big tree). Per the commission a refusal is a STOP for
   that action: I did not reach the same end another way; INFO 7's qualification question is NOT RUN.
2. My probe's deep runs end the test process on purpose (a stack overflow cannot be caught); each ran as its own
   heavy job, the 18 cells' green runs are the separate `head-exe` and `post-exe`.

## TREES LEFT

`g1980/clone` detached at `1fca08cf`, status clean (mutants undone, rebuilt, whole solution built); worktree
`g1980/red` at BASE with both patches, the HP files and the lock files staged (tree `32057fba`, never committed);
worktree `g1980/probe` at `1fca08cf` with `tests/Datasec.Suite.Adapters.Oxpd1.Tests/G1980Probe.cs` untracked (copy in
`g1980/scratch/`; the probe's build output under `bin/`); `g1980/scratch/jar/` (the jar copy); `g1980/scratch/**`
(helper scripts, `words/`, `gl-blobs/`, `mutants/`, probe outputs); `g1980/logs/**`; `g1980/_quarantine/{locks,
gl-control}`. No process left running; the wave lock not held by this reader.
