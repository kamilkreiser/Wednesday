GATE B1987: GO WITH FINDINGS @ 8f5813b on main cad65b8

Gate G1 (security surface: TLS pin, the device admin password, network input), **round 2 of 2 of lane X1, the LAST**,
one Opus reader (claude-opus-5-5), in-session, read-only. OXPd 1.x lane X1 fix round, kit B1984 (seat X50; stamp S4: Q1
= a in words, Q2 accept the limit, Q3 five minutes, Q4 64, Q5 the hold ends after a round-2 GO or GO WITH FINDINGS; each
the coordinator's, none the product owner's). Head `8f5813bf7825d989dac9c6681f930f66196192ef` on
`b1976/x1-oxpd1-read-client`: HEAD1 `1fca08cf`, then merge `ba15e0f9` of main `cad65b86`, then ONE fix commit. Read and
measured 2026-11-23 13:52 to 14:14 AEDT in my own scratch `fleet/state/s316/g1987/`: `clone` (the kit's `clone.py ...
draft`: push URL `invalid://no-push`, no identity; detached at the head), worktrees `red` (the merge + `3-red.diff`, then
+ `4-fix.diff` + `5-slnx.diff`), `probe` (the head + my probe file, never committed), `xh` (the head read-tree'd to the
merge with lane H's head), `cq` (the head, for CodeQL). Every dotnet job through the kit's `heavy.py` (sha256
`31adedc8...`) and the wave lock, one at a time (lock waits 0 to 2 per job; load1 1.9 to 6.5 at each job's start; the
mutant run waited out a load1 of 7.6 to 11.9 at 14:03 to 14:04); no other holder's lock touched (gate B1986 shares it).
Origin by `gh api -X GET` under the project GH_CONFIG_DIR at 13:52:42 and again at 14:10:38 (unchanged): main
`cad65b86`; `matching-refs/heads/b1976` one row, `8f5813bf`; `b1974/h-host-composition-v0` `0c65be47`; `b1984` 0 rows;
`compare main...8f5813bf` ahead 3, behind 0, 31 files (30 added, 1 modified: `Datasec.Suite.slnx` +2 -0), merge base
`cad65b86`; open pull requests 0 (newest 35, merged); pull requests from the branch 0; open code-scanning alerts on main
0; repository private, push true. No write to the project, GitHub or Jira; no push, no pull request, no re-run; nothing
deleted (the gitleaks control and two failed CodeQL databases moved to `g1987/_quarantine/`).

**BLUF.** The four round-1 findings are FIXED, and I re-measured each with gate B1980's own probe at the head: every deep
shape (5,000 and up to 140,000 levels in a SOAP result, in the tree, in a fault code) ends `MalformedAnswer` and the
process lives; A1 to A13 leave the password nowhere (answer, names, fault code, result text, record); the client sends
WS-Addressing 1.0 only (0 August 2004 strings in `src/`); `InfiniteTimeSpan`, zero, -5 s and 30 days are refused by the
OPTIONS. The merge commit's tree is `git merge-tree`'s exactly, and the fix commit is the three frozen patches byte for
byte (merge + patches = the head's tree `0dc0d950`). Red first reproduces (21 / 10, the kit's ten cells, each an
assertion); my own independent mutant run reads 24 of 24 MATCH and undone; the whole solution reads 1925 / 0 / 1921 / 4,
RULES 617, Ran 111; the hosted legs ran the lane's assembly on Linux and Windows for the first time, green (PASS).
**Three findings remain, each a Minor that can ship with a ticket; none is a Blocker:** (1) a password holding `&`, `<`,
`"`, a tab or a line feed, echoed by a pinned device inside a namespace URI, comes back in the returned answer's
namespace names (`Holds` compares serialised text, where those characters are escaped; the record stays clean); (2) the
work after the body is not under the time-out: 90,000 attributes on one element (889 kB) returned `Answered` after 7.4 s
with `Timeout` = 1 s, so the README's "A call is bounded in time" overstates; (3) the library README still says the
projects are not in the solution file. **X1 and H's slnx edits do NOT conflict** (MAIN MOVES below). CodeQL could not
run on this machine (its C# extractor is x86_64 only: "Bad CPU type"); it is first read on the pull request.

## FOUND (each Minor; for the product-owner card: Blocker none, Minor-ship-with-ticket three)

1. **Minor, ship with a ticket (P3, README:29 to :31 "Neither it nor its Basic form is in ... the returned `Answer`
   (... its element and attribute names and namespaces)"; also the class summary `Oxpd1Client.cs:19` "never logged,
   recorded or returned"): a password holding an XML-escaped character, echoed inside a namespace URI, is returned.**
   `Mask` copies every namespace declaration unchanged (`Oxpd1Soap.cs:196` to `:199`, `copy.Add(new XAttribute(a))`)
   and keeps every element's and attribute's `XName` (`:193`, `:202`); `Holds` (`:170` to `:184`) compares the copy's
   `ToString()` in two formattings and its `Value`. `ToString` escapes `&`, `<`, `"`, tab and line feed in a declaration's
   value (`&amp;`, `&lt;`, `&quot;`, `&#x9;`, `&#xA;`), so an ordinal search for the password misses it. MEASURED (probe
   N1 to N5, five passwords `synthetic-ad?min-0001` with `?` each of those five characters; the stub on 127.0.0.1 with
   the right pin; outcomes and booleans only, no value printed): an unused prefix declaration, an element in that
   namespace, a default namespace, an attribute in it, and the same in the TREE: every row `Answered`, and the returned
   `Answer` holds the password exactly in a declaration's `Value` (all 25 rows) and in `Name.NamespaceName` /
   `Name.ToString()` (the 20 rows that use the namespace); `ToString()`, `ToString(OmitDuplicateNamespaces)`, `Value` and
   `WriteTo` with `NewLineHandling.Entitize` do not show it; `WriteTo` with `NewLineHandling.None` DOES show the tab and
   line-feed forms (10 rows); the record scan is clean in every row; the fault code and the result's text are clean.
   Controls: the same five shapes with a password of plain characters end `MalformedAnswer` (5 of 5: `Holds` sees them,
   which is K12 A16's shape); the same passwords as a text node or an attribute value are scrubbed (10 of 10 clean). Who
   can send it: only a device whose certificate is pinned, echoing the admin password inside a namespace URI, and only
   when the password holds one of those characters; the value goes back to the caller that supplied it, not to a sink
   this library writes. That is the class of round-1 FOUND 2 (graded Minor there), on a narrower shape. **Why not a
   Blocker:** no network leak, no trust bypass, the record clean, fail-closed for every plain-character password.
   **Ticket (the coordinator's direction):** `Holds` also reads every element's and attribute's namespace name and every
   declaration's value as they are (or `Mask` refuses a declaration whose value holds a secret), and a K12 row whose
   password holds `&`.

2. **Minor, ship with a ticket (P4, README:42 to :43 "A call is bounded in time: `Timeout` is refused by the options
   unless it is positive, finite and at most five minutes"): the time-out does not bound the work after the body.**
   `timeout.Token` reaches the send and the body read only (`Oxpd1Client.cs:115`, `:117`); `Judge` (`:118`, parse, mask,
   `Holds`) and the record run after it with no token. MEASURED (probe K, macOS arm64, load1 2 to 5, record on): 90,000
   attributes on one element, 889,180 bytes (under the 1 MiB default): `Answered` after **7,432 ms with `Timeout` = 1 s**
   (K7) and 8,360 ms at 60 s (K2); 28,000 namespace declarations on one element with a child in each: 5,589 ms (K1),
   5,118 ms in the tree (K1t). Controls: a 1,000,000-character name 35 ms (K3), a 1,000,000-character text node 34 ms
   (K4), 200,000 siblings 108 ms (K5), a small answer 20 ms (K0). So the cost grows with attributes on ONE element; the
   exact framework cause is UNMEASURED (no profiler run). Bounded and finite by `MaxAnswerBytes` (150,000 short
   attributes needed 1.3 MB: `TooLarge`, K8), no crash, no leak, and only a pinned device can send it. Kit B1984's own
   frame table already says "parsing and masking after the body (bounded by size and depth, not time) ... stated here,
   not in the README". **Why not a Blocker:** finite, fail-closed, one host thread for seconds per answer, pinned devices
   only. **Ticket:** cap attributes per element (as `MaxElementDepth` caps depth) or check the time-out token inside the
   copy, or narrow the README sentence to "the connection and the body read".

3. **Minor, documentation, ship with a ticket: `src/Datasec.Suite.Adapters.Oxpd1/README.md:72` to `:73` is false at
   the head.** "**Not built by the solution yet.** The two projects are not in `Datasec.Suite.slnx`, so the hosted
   `dotnet test` does not run their cells until a later round adds the two lines" (printed by `cat -n` at the head; the
   seat's STATUS named it first). The head's `Datasec.Suite.slnx` holds both lines and the hosted legs ran the cells.
   **Ticket:** remove the bullet in the follow-up that fixes 1 or 2; landing it as is states one false sentence in a
   README, no code path.

## THE GATE LIST OF THE KIT (B1984 FOR TUESDAY, verbatim items; each MEASURED here)

- **`<merge>..<head>` read whole, and the merge's tree against `merge-tree`'s.** `git merge-tree --write-tree 1fca08cf
  cad65b86` = `d579d9d9b10782f92a0f117b261426a8b7baf9b4` = `ba15e0f9^{tree}`; parents `1fca08cf` then `cad65b86`;
  `diff --name-only cad65b86 ba15e0f9` 30 paths, outside the three lane folders 0; `diff --name-only 1fca08cf ba15e0f9`
  40 paths, inside the lane folders 0 (no hand edit). `diff --name-status ba15e0f9 8f5813bf` 8 rows, all `M`, each an
  owned path; `diff --numstat` 2/0 slnx, 12/2 Client, 20/2 Options, 77/11 Soap, 33/11 README, 140/0 ClientTests, 19/0
  ContractTests, 67/7 StubDevice (the 7 deleted test lines are the `SeenRequest` record, the two route lines, the
  `Answer` signature, the hard-coded 2004/08 namespace, the `Action` read and the `Enqueue` line, each replaced by its
  wider form; no assertion removed or weakened: ClientTests and ContractTests delete 0 lines). I read the whole diff and Oxpd1Client.cs and
  Oxpd1Soap.cs whole at the head.
- **The fix commit's paths against the three patches by sha256.** In `red` (the merge): `git apply` of `3-red.diff`,
  `4-fix.diff`, `5-slnx.diff` each rc 0, `add -u`, `write-tree` = `0dc0d9508e65d8f0553574d586b1b8ed3b11b650` = the
  head's tree. THE CODE's 10 files at the head: 10 of 10 sha256 and line feeds equal (the two lock files unchanged,
  HEAD1's). Stored messages equal `commit-message.txt` and `merge-message.txt`; author = committer on both commits, one
  address ending `@datasec.com.au` (in-process, masked).
- **`contracts/oxpd1/**` byte for byte HEAD1's:** `diff --quiet 1fca08cf 8f5813bf -- contracts/oxpd1` rc 0 (control on
  the src lane folder rc 1); the subtree is `ae7c32df` at both.
- **The red first of `3-red.diff` (10 of 21).** `red-restore` rc 0, `red-build` `0 Warning(s)` `0 Error(s)`,
  `red-exe` `Total: 21, Errors: 0, Failed: 10`: C07 `Strings differ`, K01 `GetManufacturerInfo: Fault 500 s:Sender`, K03
  K04 K09 K10 K12 `Values differ`, K07 and K14 `No exception was thrown`, K13 `soap 65: Answered` (= THE CONTROLS; the two
  `System.*Exception` words are expected types). `g1987/logs/red-exe.log`.
- **Each mutant red on its cells (an independent run).** `mutants_x2.py <g1987/clone> g1987/scratch/mutants run g1987
  'B1987 gate g1987'`, one call, exit 0, every row `Total 21`: `MUTANTS: 24 of 24 MATCH, 24 of 24 undone equal`
  (`g1987/logs/mutants-run.log`; mDtd the named survivor, NONE). After it: status 0 lines; `post-build` 0/0, the library
  dll 14:08:10 later than the newest source (`Oxpd1Read.cs`, 14:07:54); `post-exe` 21 / 0.
- **The gate's own deep shapes and A1 to A13 re-probed against the head.** `G1987Probe.cs` (gate B1980's
  `G1980Probe-final.cs` with its names changed, plus sections N, P, K; kept as `g1987/scratch/G1987Probe.cs`), built 0/0
  in `probe`, run whole `Total: 22, Errors: 0, Failed: 0` (the 21 cells and the probe). A1, A2, A2b, A7, A9 to A13
  `Answered` and A3, A4 `MalformedAnswer`, A5, A6, A6b `Fault`: in every row `ToString`, `Value`, names, fault code and
  result text without the password, record scan clean. Deep (each its own run, `G1987_DEEP=1`): soap, tree and fault at
  1,000, 5,000, 20,000, 60,000 and 140,000 levels (up to 980,283 bytes): every one `MalformedAnswer` in 10 to 53 ms, no
  `Stack overflow` in any log, each run `Total: 22, Failed: 0`. Round 1 died at 5,000 (soap, tree) and 60,000 (fault).
- **Whether any path but the 14 result constructions returns text from an answer.** `new Oxpd1ReadResult(` 14, all in
  `Oxpd1Client.cs`; only `:166` (the tree, after `Holds`) and `:182` (the answer after `Holds`, the fault code after
  `Scrub` then the cut) carry answer text. Other paths: the 7 `throw new` sites hold fixed text (`Oxpd1Read.cs:86` adds
  the enum value); every exception the probe met (C1, C2, C2b, C3 to C5b, F1 to F3) is without the password; `Parse`
  catches `XmlException`; `Mask`'s `ArgumentException` is unreachable through the client (the Result sits at depth 3, so
  `Mask` sees at most 61 below it); P1 to P5 (prefix redeclared, default undeclared, two prefixes, `xml:` attributes, a
  deny-listed element with a namespaced child) and K0 to K6 all ended in an outcome, none threw. The record: clean in
  every probe row. So the answer paths are the two above; FOUND 1 is the one shape that carries the password through them.
- **Whether `Holds` can miss a secret that `ToString()` with other options shows.** For a password of plain characters:
  no (every `SaveOptions`, `WriteTo` with either new-line handling: nothing, N plain rows). For a password with `&`, `<`,
  `"`, tab or line feed in a namespace: yes, FOUND 1 (`WriteTo` with `NewLineHandling.None` shows the tab and line-feed
  forms; the object model shows all five).
- **The hosted legs' 21 cells on Linux and Windows.** `hosted2.py 8f5813bf... --total 1925 --rules 617 --skipped-linux 4
  --skipped-windows 21 --unit 111 --floor 111 --hardened-scan` (GET only): run 45101945254, attempt 1 on all four jobs,
  every proof row OK, `HOSTED 8f5813bf...: PASS`. Job logs (ANSI stripped, `g1987/scratch/legs.py`):
  `Datasec.Suite.Adapters.Oxpd1.Tests` 5 lines on each leg, `total: 1925` 2 on each, `failed Datasec.` 0 on each
  (control: 32 `passed (` lines naming `Datasec.` on each); linux `succeeded: 1921`, `skipped: 4`, windows `succeeded:
  1904`, `skipped: 21`; each leg's `...Adapters.Oxpd1.Tests.dll (net10.0|x64) passed` (11 s 357 ms, 13 s 256 ms). The legs
  print no per-cell list: that the 21 ran is DERIVED from each total moving from main's 1904 (run 45099054678, read PASS
  here at 14:05) to 1925 with the skips unchanged. Tuesday's counts hold.
- **CodeQL on the lane now that it is in the solution.** NOT RUN on any head of this lane: the branch head's check runs
  are the four CI jobs only and `code-scanning/analyses?ref=refs/heads/b1976/x1-oxpd1-read-client` lists 0; main's latest
  csharp analysis (`cad65b86`, results 0) predates the lane. Locally: the toolchain's C# extractor
  (`tools/codeql/codeql/csharp/tools/osx64/Semmle.Autobuild.CSharp`, `file`: Mach-O x86_64; this machine arm64) fails
  "Bad CPU type in executable" with `--build-mode=none`, and the traced build exited 1; no Rosetta install (no tool
  installs). CodeQL is read FIRST on the pull request (landing.txt step 3).
- **`words.py` and gitleaks.** `words.py --control` `CONTROL FIRED: 13 of 13`; over the 370 `+` lines of `ba15e0f9..8f5813bf`
  (= the patches' 370), the stored fix message and the stored merge message: `WORDS: clean (3 files)`. gitleaks 8.30.1
  `--no-banner --redact --ignore-gitleaks-allow --exit-code 1`: control FIRST (a token built by program, never printed):
  rc 1, `leaks found: 1`, moved to `g1987/_quarantine/gl-control`; `dir` over 37 neutral files (the 31 head blobs of
  `cad65b86..8f5813bf`, the three patches, the added lines, both stored messages): rc 0, `no leaks found`; `git
  --log-opts=cad65b86..8f5813bf`: `2 commits scanned`, `no leaks found`, rc 0. The hosted secret-scan's hardened rows
  all OK.

## WIDER (commission item 2)

- **Certificate callbacks:** over the lane's `src/` and `tests/`, `/usr/bin/grep -i` for every callback and trust word
  finds ONE client callback, `Oxpd1Client.cs:49` (`RemoteCertificateValidationCallback = Pinned`), and the stub's
  SERVER `ServerCertificateSelector` (`StubDevice.cs:229`); no `ServerCertificateCustomValidationCallback`, no
  `DangerousAcceptAny...`, no `ClientCertificates`, no chain policy in `src/`. The probe called `Pinned` directly: a
  null certificate false (B1, B1b); an unpinned leaf whose chain builds to the pinned authority false (B2); the pinned
  certificate itself true (B3), with every policy error set true (B4: the pin is the whole trust, by design). Nothing
  trusts a certificate the pin did not.
- **The depth bound before any builder:** `XDocument.Load(` once (`Oxpd1Soap.cs:97`), after the reader pass `:83` to
  `:93`; `XDocument.Parse`, `XElement.Parse`, `XElement.Load`, `XmlDocument`, `ReadFrom` 0 in `src/` (the three in
  `tests/` read the committed bindings or the library's own envelope). Attribute count: FOUND 2. A long name and a
  huge text node: 35 ms and 34 ms at 1,000,000 characters (stated limit `MaxAnswerBytes` suffices). A wide answer: 108 ms
  at 200,000 siblings (the kit's H24 limit holds).
- **`Holds` against every serialisation path:** above, FOUND 1. The record path (`:235`, `Scrub` of `ToString`) is clean
  in every row, including FOUND 1's.
- **The time-out refusal from the options, not the handler:** `Oxpd1ClientOptions.cs:89` to `:99`, an `init` check;
  K07 builds options only; the probe's C3 to C5b now throw `ArgumentOutOfRangeException` from the options' `init`
  (round 1: C3 accepted, C4 to C5b from the handler's constructor).
- **WS-Addressing 1.0 everywhere the client writes a header:** `Envelope` (`Oxpd1Soap.cs:27` to `:64`) writes `Action`,
  `MessageID`, `ReplyTo/Address`, `To` all in `Wsa` = `http://www.w3.org/2005/08/addressing` (`:17`), `mustUnderstand`
  `1` on `Action` and `To`, anonymous `Wsa + "/anonymous"`. Over every file of `src/` at the head: `2004/08` 0,
  `schemas.xmlsoap.org/ws/` 0 (control: `2005/08/addressing` 2, `Oxpd1Soap.cs` and the README).

## THE FRAME QUESTION (each "never / every / only" sentence of the README at the head; three shapes outside the tested one)

| Sentence | Shapes not the tested one | Covered? |
|---|---|---|
| :14 "Every SOAP call goes to `https://<host>:7627/hp/device/webservices/OXPd/<service>`" | the prefix in another case; a caller's `SoapPort`; an IPv6 host | K01 ordinal + `mPathPrefix` (MATCH here); public init by design (stated); IPv6 no cell (DERIVED, `UriBuilder`) |
| :18 "Every addressing element the committed bindings contain is in that namespace" | the declared, unused 2004/08 prefix; the port types' `wsaw` attributes; a fifth binding file | C07 control (green); the `wsaw` vocabulary is WSDL, not a header (kit D3); `AddressingNamespace()` throws unless exactly 4 ports, one value |
| :24 "No write ... five rows, each a `Get`" | `(Oxpd1Read)99`; a sixth row; a public method added | F1 throws before a send (re-measured); C04 + `mReadOnlyOpen` (MATCH); C04 reflection |
| :26 "a certificate is accepted only when the SHA-256 ... on every handshake" | a null certificate; a chain to a pinned authority; a resumed TLS session | B1/B1b and B2 false (re-measured); K04 + `mPinAny`; resumption UNMEASURED (stated INFO) |
| :27 "A redirect is never followed ... only HTTP/1.1" | 301/302/303/308; the tree GET; an h2-only server | K06 (307, read); one handler for both calls (DERIVED); h2-only no cell (carried) |
| :29 "Neither it nor its Basic form is in ... the returned `Answer` (... names and namespaces)" | a password with `&` in a namespace; a case variant; a comment or PI | **FOUND 1**; A10 kept, a stated Limit; A12, A13 not copied (clean) |
| :37 "Exception texts of this library are fixed" | the caller's cancel; a throwing setting reader; misuse after Dispose | C1, C2 `TaskCanceledException` clean; F3 the reader's own text (the caller's); F2 clean |
| :39 "a device's answer or a transport fault never throws" | deep nesting; namespace prefix tricks; 90,000 attributes | deep 15 rows `MalformedAnswer`; P1 to P5 outcomes; K2 `Answered` (no throw) |
| :41 "an element deeper than 64 ... refused while the answer is READ, before any tree is built" | deep in a fault code; deep in the tree; an answer in UTF-16 | K13 + probe (fault, tree to 140,000); UTF-16 deep: no cell, DERIVED (the same reader; E3 UTF-16 `Answered` re-measured) |
| :42 "so no recursion over an answer can exhaust the stack" | `.Value` of a deep fault code; `ToString` in `Holds`; `Mask` handed a built element | after `Parse` each sees at most 64 (probe 60,000 and 140,000 fault rows alive); K14 + `mMaskDepth`; Linux and Windows stack at 64: the hosted legs ran K13 green |
| :42 "A call is bounded in time" | work after the body; a slow trickled body; a TLS handshake that never answers | **FOUND 2**; C7 `TimedOut` at 1,502 ms; C6, C6b at 1,002 ms |
| :43 "`Timeout` is refused by the options unless positive, finite and at most five minutes" | `InfiniteTimeSpan`; zero; `MaxValue` | K07 rows (green) + `mTimeoutOpen` (MATCH); probe C3 to C5b |
| :57 "a real tree deeper than 64 would end `MalformedAnswer` (closed, never a crash)" | 65; 5,000; 140,000 | K13 tree 65 and 5,000; probe tree to 140,000 |
| :72 "Not built by the solution yet" | - | **FOUND 3** (false at the head) |

Two events, two orders: the caller's cancel and the time-out (C1, C2: the caller's token wins at catch time, re-measured);
`Mask` then `Holds` then the record's `Scrub` (FOUND 1: the record scrubs a string that is already escaped, so it is clean
while the object is not).

## MAIN MOVES (X1 landing on main as it stands, and X1 landing after H)

- **(A) X1 NOW, main `cad65b86` (unmoved at 14:10:38):** the head IS the merge with main of the moment
  (`git merge-tree --write-tree cad65b86 8f5813bf` = `0dc0d950`, the head's tree). In `clone` at the head: `CI=true`
  `dotnet restore --locked-mode` rc 0; build 0 Warning(s) 0 Error(s), 33 ` -> ` lines, 2 naming `Adapters.Oxpd1`;
  `dotnet test` **`total: 1925`, `failed: 0`, `succeeded: 1921`, `skipped: 4`**, `Passed!`; in `red` (index = the head's
  tree) `repo_rules.py` (never `--source-documents`; `test ! -e g1987/1_Project_Definition` rc 0) `RULES-NOTE: R5 hash half
  NOT RUN (no supplied-source folder here)`, **`RULES: clean (617 files)`**; `unittest discover build/tests` `Ran 111
  tests`, `OK`. The squash's tree must equal `0dc0d950` (617 files).
- **(B) X1 AFTER H (H head `0c65be47` = its merge `4c415f9a` of `cad65b86` + one commit).** `git merge-tree --write-tree
  8f5813bf 0c65be47` rc 0, ONE line, tree **`7ad207efda2c152844f8391aa798172079be8b3d`, no conflict: the two slnx edits
  do NOT conflict** (`diff cad65b86 7ad207ef -- Datasec.Suite.slnx`: three separate hunks, X1's two lines, H's
  `Jobs.Transport` and `Server.Tests` lines). In worktree `xh` (`read-tree -m -u` to `7ad207ef`, `write-tree` equal,
  628 files): locked restore rc 0, lock files unchanged (`diff --stat` 0 lines); build 0/0, 34 ` -> ` lines (X1's two,
  Server, Server.Tests and `Jobs.Transport` now in `bin/Release`); **`total: 1940`, `failed: 0`, `succeeded: 1936`,
  `skipped: 4`** (= 1919 + 21, as the commission expected); **`RULES: clean (628 files)`** (= 598 + 30). H's own 1919
  and 598 are RELAYED from the commission, not measured here. H's head tree is `a17719c2`; a squash of H on `cad65b86`
  gives main that tree, and the merge of X1 into it has base `cad65b86` again, so it is `7ad207ef` (DERIVED from
  `merge-tree`'s inputs). If H lands first, ADDENDUM-2 has X1 merge main again: that new head's merge tree must equal
  `7ad207ef` with (B)'s numbers, and it is a NEW head, so it needs its own gate read (this verdict is pinned to
  `8f5813bf`), which can be short: the merge commit's tree equal to `7ad207ef` and the fix commit untouched. (A squash
  of `8f5813bf` itself over an H-moved main would also build `7ad207ef`, DERIVED; ADDENDUM-2 chose the merge, so
  landing.txt follows ADDENDUM-2.)
- **(C) Anything else landing first:** a new gate measure (landing.txt).

## NOT RUN

CodeQL (above: the extractor cannot run on arm64 here; none on the branch); any run on Linux or Windows locally (the
hosted legs ran the cells); the probe's N, P and K shapes on Linux or Windows; a profiler for FOUND 2's cause;
`run_step.py`'s neutral scan locally (the hosted secret-scan's hardened rows are OK, and the seat ran it); `repo_rules.py
--source-documents` (never); any device, simulator or address but 127.0.0.1; TLS session resumption; two concurrent
calls; HTTP/2-only servers; H's own head by `hosted2.py` (not mine to judge); any re-run.

## DEVIATIONS

1. One Bash call began with `cd` (to read the round-1 landing texts); the `pretooluse_no_cd.sh` hook REFUSED it before
   anything ran; I re-issued the same read with absolute paths and no `cd` (a read, not a way round a refused action).
2. `probe.py build` ran twice (the second after adding the K7 to K9 cost rows), so `logs/probe-build.log` holds the
   second build only (0 Warning(s), 0 Error(s) both times, printed by the program each time).
3. Two CodeQL `database create` attempts failed (traced: exit 1; `--build-mode=none`: Bad CPU type); both databases
   moved to `_quarantine/`; no third way tried.

## TREES LEFT

`g1987/clone` detached at `8f5813bf`, status clean, built (mutants undone and proved); worktrees `g1987/red` (the merge +
the three patches staged = tree `0dc0d950`, never committed), `g1987/probe` (the head + untracked
`tests/Datasec.Suite.Adapters.Oxpd1.Tests/G1987Probe.cs`; copy in `g1987/scratch/`), `g1987/xh` (index and files =
`7ad207ef`, never committed), `g1987/cq` (the head, restored only); `g1987/scratch/**` (helper scripts, probe outputs
`probe-out-{main,deep,deeptree,deepfault,cost}.txt`, `mutants/`, `gl-neutral/`, `added.txt`); `g1987/logs/**`;
`g1987/_quarantine/{locks,gl-control,cqdb-traced-failed,cqdb-none-failed}`. No process left running; the wave lock not
held by this reader.
