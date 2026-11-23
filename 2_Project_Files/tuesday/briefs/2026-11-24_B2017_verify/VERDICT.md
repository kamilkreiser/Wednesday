GATE B2017: GO WITH FINDINGS @ d3d10b7 on main e39396f

Gate G2 on Opus (claude-opus-5-5), round 1 of 2 of lane CT, one reader, in-session, read-only. OXPd 2 project, lane CT,
kit B2014 (seat X60; S4 Q1 IN and Q2 IN, Q3 to Q6 the defaults, each the coordinator's). Head
`d3d10b71cdcf90badca26a4f8ee91b7cee298b06` on `b2014/ct-oxpd1-contracts-steps-2-4`, ONE commit, one parent `e39396f9`
(BASE = main after PR 42), tree `ab8093c6920bf256c25383e2cb911efc59477181` (= the kit's staged tree). **Main did not move
during the gate** (`e39396f9` at 00:17 and at 00:29 by `gh api -X GET .../git/matching-refs/heads`; open pull requests 0),
so the merge with main of the moment is the head's own tree. Read and measured 2026-11-24 00:17 to about 00:35 AEDT in my
scratch `fleet/state/s319/g2017/`: `clone` (clone.py draft: push URL `invalid://no-push`, no identity; branch `gate-head`
at the head), `fetched/` (the gate's own fetch of the nine files), worktree `w2m` (lane W2's head `67c24d18` with this
head merged, tree `b2a09571`). Every dotnet job and test executable through the kit's `heavy.py` (sha256 `31adedc8...`)
and the wave lock, one at a time (released lock folders in `g2017/_quarantine/locks/`, all mine; another holder's lock
never touched). Origin by `gh api -X GET` under the project GH_CONFIG_DIR. No write to the project, GitHub, Jira or the
NAS; nothing of the NAS library but the jar, through `fetch_ct.py`; no push, no pull request, no re-run; no network call
to any device or tenant; nothing deleted (the gitleaks control moved to `g2017/_quarantine/`).

**BLUF.** The head is what the kit says and nothing else. The nine files, fetched again by the gate from the pinned jar
(jar sha256 equal to the README pin), are equal BYTE FOR BYTE to the branch's blobs (9 of 9; control: a changed byte is
not equal). `inputs.sha256` keeps BASE's 14 lines byte for byte and in order, 23 lines sorted by path, every listed hash
equal to its head blob, every file under `hp/` listed. The `.cs` diff is `ContractTests.cs` line 66 and `StubDevice.cs`
lines 180 and 182 only (every other line equal; 222 and 446 lines both sides). The nine are exactly the three services'
binding, port type and schema; their imports close over `common.xsd` (0 dangling over all 23 files); the callback pair is
not committed. All five HP quotes are in the files, his three quotes in `CLARIFICATIONS.md` at the dates given. Gate's
own runs: Oxpd1 40 / 0; whole solution 2054 / 0 / 2050 / 4; `REDPROOF: 9 of 9 MATCH, 9 of 9 undone equal` (independent
of the seat's); RULES 656; 111 unit tests; `CHECKS: 7 of 7 PASS`; hosted push run PASS on all four jobs, the windows
leg's Oxpd1 tests passing on HP's CRLF bytes. The merge with lane W2's head (if W2 lands first) is clean and measured:
see THE MERGE. Six Info findings; none blocks the landing.

## FOUND (round 1 of 2; grade Blocker / Major / Minor / Info)

1. **Info (the stub serves the new services with a generic answer; no cell calls them).** `StubDevice.Bindings()` and
   the POST route (`StubDevice.cs:205` on, `:242`) now load all seven bindings, and the stub answers any of the 78
   soapActions; for the 48 new ones the answer is the generic `<op>Response><op>Result><modelName>` envelope
   (`AnswerEnvelope`, `:400` on), not HP's response shape. MEASURED: the 26 stub-backed cells (C07, K01 to K16 less
   K07 and K14, W02 to W09) exercise only the Authorization, Authentication, DeviceInfo and Accessories routes
   (`git grep` of the seven service names over the Oxpd1 tests: the four only). So moving the pin from 4 to 7 hides no
   binding the stub cannot load (each new binding parses, 1 port, EndpointReference in the 2005 namespace, its
   soapActions distinct), but a stub green on a Test, CertificateManagement or UIConfiguration call would mean nothing
   until a write lane gives those operations their own answers and cells. For the step 2 to 4 kits.
2. **Info (the three new schemas are compiled by no cell).** C05's `Schemas()` (`ContractTests.cs:150` to `:162`)
   compiles `deviceinfo.xsd`, `authentication.xsd`, `accessories.xsd`, `authorization.xsd` only. MEASURED by the gate:
   all nine `.xsd` compile with `xmllint --nonet` (control: a broken schema fails to compile); every `wsdl:part` of the
   three new port-type files names a global element of its schema; every binding operation is a port-type operation
   and the reverse (Test 17 / 17, CertificateManagement 6 / 6, UIConfiguration 25 / 25). A write lane extends C05.
3. **Info (an unnamed "this method" in a quote).** `contracts/oxpd1/README.md:33` to `:34` quotes HP's "When disabled,
   only this method, the EnableService method, and the DisableService method will be functional." It is HP's text on
   `IsServiceEnabled` (`test.wsdl:497` operation, `:502` the sentence), which the README does not name, so "this
   method" can be misread as `GetScreenCapture` or the service. A round-2 wording: "HP, on `IsServiceEnabled`: ...".
4. **Info (the port pin counts ports, not files).** README `:21` to `:23`: "The number of listed files (contract cell
   C01) and the number of binding ports (`StubDevice.AddressingNamespace`) are pinned in the tests and move with this
   list." True for a new service; a new schema or port-type file alone moves C01 only, and a binding with two ports moves
   the port pin by two. The sentence is accurate as written; named so the next lane does not read "move with this list"
   as "move together".
5. **Info (the words tool's B-number class is `B1nnn` only).** `words.py` (kit B1813's, frozen; sha256 `6f932dc5...`)
   matches B-numbers by `B1[0-9]{3}`, so a `B2nnn` id would pass it. The gate's own count of `B2nnn` and `C-nnn` (one to
   three digits) over the 55 added lines, the commit message, and the PR title, squash subject and squash body: 0
   (control: the commission file counts 8). Nothing leaked here; the tool's gap is Tuesday's to carry to the next kit.
6. **Info (records only).** (a) The commit subject is 240 characters (the squash subject 250 with `#PRNUM`). (b) B2012
   line 128 says each port-type file imports `common.xsd`; MEASURED, each port-type file imports its schema and each
   schema imports `common.xsd` (the README's "import closure" is right). (c) H6 is now MEASURED, no longer RELAYED: 78
   soapActions over the seven bindings, 0 clashes within or across bindings, seven distinct service names (routes).

## THE KIT'S GATE LIST (FOR TUESDAY, "THE GATE")

- **Tools:** my copy `g2017/gate/` (from `d2014/seat-tools/`) and the seat's `.tools/b2014/gate/`: 24 of 24 sha256 equal
  to THE TOOLS (12 each).
- **The nine re-fetched:** `fetch_ct.py <jar> --control`: `JAR sha256 equals the pin: True`, `CONTROL common.xsd equal
  True`, `CONTROL changed byte equal False`. `fetch_ct.py <jar> g2017/fetched`: `FETCH: 9 of 9 equal` (8970, 63712,
  43972, 4582, 33807, 17627, 12717, 95446, 107300 bytes). Then `analyse.py`: each fetched file against `git show
  d3d10b71:<path>`: `A: 9 of 9 fetched equal the head blobs byte for byte` (control False).
- **BASE's 14 lines:** all present, in order, unchanged; 23 lines; sorted by path in byte order; distinct; the 9 added
  paths = the fetched set; files under `hp/` at the head 23 = the listed paths; listed hash differing from its blob: none;
  the list ends with LF and holds no CR.
- **The two pins and nothing else:** `git diff -U0` hunks: `ContractTests.cs` old line 66 only (1 / 1); `StubDevice.cs`
  old lines 180 and 182 only (2 / 2); every other line equal; `.cs` paths in the diff: those two. `checks_ct.py` check 7
  (and 1 to 6), my run on the head: `CHECKS: 7 of 7 PASS`, added lines 55, every control fired.
- **README sentences against the files (`quotes.py`):** 8 double-quoted strings in the README, 3 in the commit message.
  HP's five: "As of Minor Revision 1.1, ..." and "When disabled, only this method, ..." in `test.wsdl` (`:123`, `:502`);
  "If the certificate is already in the store, ..." (`certificatemanagement.wsdl:104`, inside `ImportCertificate`) and
  "The use of self-signed certificates with the OXPd CA Certificate store is not recommended/supported." (`:135`, the
  same operation; the README quotes the first sentence of a longer paragraph); "If the new button record's guid matches
  an existing record's, the new record overwrites the existing one." (`uiconfiguration.wsdl:273`, inside
  `RegisterTopLevelButton`). His three: `CLARIFICATIONS.md:394` (`2026-11-21T09:40:49`, "hp files have been provided to
  us.  we can store them where we want (and will try to do it safely)") and `:414` (the settlement); `:758` (his
  live-board note of 2026-11-23 17:56, "our license / commercial agreement allows us to use H[P code as part of our
  code]"). The README and the message give 2026-11-21 and 2026-11-23: equal. The README says the 2026-11-21 words were
  said of HP's OXPd 2 specification files (the C-56 subject, kit THE AUTHORITY): stated, not stretched. Control: an
  altered HP quote is found in no file. Every operation the README names (10) is an operation of the right binding.
  **The per-service READ-first rules against HP's text:** Test: disabled by default after every reboot (`test.wsdl:123`),
  so an undo `DisableService` is owed only if the lane enabled it: consistent. CertificateManagement: an import of a
  present certificate "will have no effect", and `RemoveCertificate` "Removes the supplied CA certificate" (`:169`), so
  a blind undo removes a certificate that was there: consistent. UIConfiguration: a register with a matching guid
  overwrites, and `UnregisterTopLevelButton` removes "the existing button" by ID (`uiconfiguration.wsdl:310`): the README's
  "removes a button that was there before" is consistent (the pre-existing record's content is already overwritten by
  the register; the README does not claim otherwise).
- **Red first, the pin's red, the red proof (from the seat's logs AND re-run):** seat `red-exe-oxpd1.log`: `Total: 40,
  Errors: 0, Failed: 2`, C02 `Actual:   11`, C01 `"missing: hp/...`; `exe-pinred.log`: `Total: 40, Errors: 0, Failed:
  26`, 26 `[FAIL]` lines (C07, K01 to K06, K08 to K13, K15, K16, W02 to W05, W06 x4, W08, W09 x2); `exe-green.log`
  and `exe-after-rp.log` `Failed: 0`; seat `redproof-run.out` 9 of 9. **The gate's own red proof** (`redproof_ct.py
  <g2017/clone> <g2017> 'G2017 gate' run`, the frozen tool, one heavy job per row): nine rows `Total 40 Failed 2 | red
  C01 C02 | ... MATCH | one file differs True | undone equal True`; `REDPROOF: 9 of 9 MATCH, 9 of 9 undone equal`; after
  it `status --porcelain --untracked-files=all` empty. The pin's red was NOT re-run by the gate (the seat's log is the
  proof; the gate's attack on what the pin could hide is FOUND 1).
- **The hosted run:** `hosted3.py d3d10b71... --total 2054 --rules 656 --skipped-linux 4 --skipped-windows 21 --unit 111
  --floor 111 --hardened-scan --guard-linux 14 --guard-windows 15` (the gate's read, 00:23): run 45181263021, four jobs
  success on attempt 1, every proof line OK, `HOSTED d3d10b71cdcf90badca26a4f8ee91b7cee298b06: PASS`. Windows job log:
  `Datasec.Suite.Adapters.Oxpd1.Tests.dll (net10.0|x64) passed` and `failed: 0`: C01 hashed HP's CRLF bytes green on
  the Windows checkout (`contracts/oxpd1/.gitattributes` = `* -text\n`, unchanged; no root `.gitattributes`).
- **`words.py` and gitleaks:** SCANS below.

## THE ATTACK (commission item 2)

- **Exactly the three services' binding, port type and schema:** the nine paths are three folders
  `..._service_{test,certificatemanagement,uiconfiguration}_2010_04_14/`, each `*Soap12Binding.wsdl`, `<svc>.wsdl`,
  `<svc>.xsd`. Imports, parsed (`xml.etree`, every `import`/`include`/`redefine` with its `location` or
  `schemaLocation`, resolved against the head tree): binding -> port type -> schema -> `../..._common_2010_04_14/
  common.xsd`; 0 dangling over all 23 files; `common.xsd` imports nothing and is unchanged (control entry of
  `fetch_ct.py`: equal).
- **The callback pair is NOT committed:** no path in the head tree holds `callback` but the OXPd 2 adapter's own C# and
  its test (12 paths, none under `contracts/`); `TestSoap12Binding.wsdl` names no callback (0); `test.wsdl` imports only
  `test.xsd`. `test.wsdl` documents the callback parameter of the live `AsyncEchoString` and `AsyncEchoBinary`
  operations (11 mentions outside comments) and `test.xsd` declares that parameter's type (7): text and types, not an
  import; nothing dangles. The two `Async*Complete` operations are inside XML comments (`operations inside comments 2`):
  the binding holds 17 live operations, as the kit corrects B2012.
- **`.gitattributes` keeps HP's bytes on both legs:** each of the nine is CRLF only (bare LF 0, bare CR 0), no BOM;
  `uiconfiguration.wsdl` 3 and `uiconfiguration.xsd` 9 bytes above 0x7E (as the kit). The windows leg's Oxpd1 tests
  passed (above), the linux leg likewise, and the gate's macOS run 40 / 0.
- **The port pin 4 to 7 hides no binding the stub cannot serve:** see FOUND 1. Seven `*Soap12Binding.wsdl`, one
  `wsdl:service` each with one `wsdl:port`, every EndpointReference in `http://www.w3.org/2005/08/addressing` (one
  value: `AddressingNamespace()` returns it); 0 uses of the August 2004 namespace over all 14 `.wsdl` files (14 declare
  it; C07's `>= 4` still holds); 78 soapActions, 0 duplicates (a duplicate would be overwritten silently in
  `Bindings()`); seven distinct `wsdl:service` names (the stub's routes). Which bindings the stub and cells exercise:
  the four the client and writer use, only.
- **Licence or redistribution text:** the nine files: 0 lines holding copyright, licence/license, redistribut,
  confidential, proprietary, rights reserved, consent, beta, trademark, warrant or `(c)`; `legal` matches only "Legal
  size" paper (`uiconfiguration.xsd:317`, `:318`); control: a planted "Copyright HP" matches. The jar: touched only by
  `fetch_ct.py` (its whole-file hash and ten named entries), so its other entries were NOT read by the gate (RELAYED,
  B2012 section 5: no LICENSE or NOTICE entry, `MANIFEST.MF` 0 hits). Nothing in the nine files contradicts committing
  them. What stays open, reported and not decided here: HP's spec "Legal Notices" ("No part of this documentation may
  be transformed, reproduced, or translated ... without prior consent", in HP's spec documents, not in these files),
  which bears on the `wsdl:documentation` prose these files carry (B2012 line 110); the "beta ... must not be
  redistributed to customers" line, which B2012 line 105 records as Friday's own README summary, "not HP's text", and
  SDK 1.8.4.1 is not labelled beta; R32. The authority for keeping them is the product owner's C-56 and C-74 as read by
  the coordinator; the gate decides nothing on it.

## THE FRAME (stamp checklist item 11: every "every / only / exactly" sentence, three shapes each)

- **"Nothing in this repository calls these three services yet."** (`contracts/oxpd1/README.md:27`) `frame.py`, over the
  whole head tree but `contracts/oxpd1/hp/`: (1) by operation name (the ten step 2 to 4 operations): hits only in
  `contracts/oxpd1/README.md` itself (`git grep -l`: 1 file); (2) by namespace or soapAction URI (`OXPd/service/test/2010`,
  `.../certificatemanagement/2010`, `.../uiconfiguration/2010`, `ITestService`, `ICertificateManagementService`,
  `IUIConfigurationService`): 0; (3) by route or service name (`TestService`, `CertificateManagementService`,
  `UIConfigurationService`): 0. The same three shapes at lane W2's head `67c24d18`: 0, 0, 0 (W2 writes the sign-in agent
  only). Control: `RegisterAuthenticationAgent` in `src` found (`Oxpd1Writer.cs` 3). Stated limit: the TEST stub
  routes and answers the three services (FOUND 1): it serves, it does not call.
- **"23 files, byte for byte, under `hp/`, each listed with its SHA-256"** (`:4`): (1) a file listed and missing: C01
  red (seat's red first); (2) a listed file one byte off: C01 and C02 red (red proof, 9 of 9, gate's run); (3) a file
  present and unlisted: C02's plant `not in the list: hp/extra.xsd`, green at the head.
- **"Each binding, its port-type file and its schema, plus `common.xsd` and `securitydomain.xsd`"** (`:12` to `:13`):
  7 x 3 + 2 = 23 = the listed set; (1) a dangling import: 0 (parsed); (2) a part naming no schema element: 0; (3) an
  unbound or extra binding operation: 0 / 0 per service. Limit: no cell parses imports (a later file with a dangling
  import would pass C01); FOUND 2.
- **"`.gitattributes` marks every file `-text`, so line ends ... stay as HP wrote them"** (`:19`): (1) Linux checkout:
  C01 green on the hosted linux leg; (2) Windows checkout: C01 green on the hosted windows leg; (3) macOS: the gate's
  clone, C01 green and the blobs equal to the jar's bytes.
- **"The number of listed files ... and the number of binding ports ... are pinned in the tests and move with this
  list"** (`:21` to `:23`): (1) a list change without the count: C01 red (seat's red first, `14` vs 23); (2) a binding
  change without the port pin: 26 red (seat's log); (3) a non-binding file: C01 only (FOUND 4, stated).
- **"The Test service's callback pair ... is not here"** (`:13` to `:14`): measured above (0 paths, 0 imports).
- **"this library makes none of them"** (`src/Datasec.Suite.Adapters.Oxpd1/README.md:76`): the same three shapes over
  `src/Datasec.Suite.Adapters.Oxpd1/`: 0, 0, 0 (README text aside); `checks_ct.py` check 6: no `src` path but the README.
- **"the undo is owed only when the lane turned it on"** (`:36`) and the two "removes a ... that was there before"
  sentences (`:42` to `:43`, `:49` to `:50`, printed by `grep -n`): rules for later lanes, DERIVED from HP's text (above); no code here, no cell
  owed by this lane.

## THE CHAIN AND THE MERGE (commission item 4)

- **Head (clone at `d3d10b71`, every heavy job through `heavy.py`):** `g-restore` (`CI=true`, `--locked-mode`,
  `-p:NuGetAudit=false`) rc 0 (22 s, lock waits 4); `status --porcelain --untracked-files=all` after it: 0 lines (no
  lock file changed); `g-build` rc 0, `0 Warning(s)`, `0 Error(s)`, 34 ` -> ` lines (a real build of a fresh clone);
  `g-exe-head` the Oxpd1 executable whole: `Total: 40, Errors: 0, Failed: 0, Skipped: 0`; the red proof (above);
  `g-test-head` `dotnet test -c Release --no-build`: `total: 2054`, `failed: 0`, `succeeded: 2050`, `skipped: 4`.
  Not heavy: `repo_rules.py <clone>`: `RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder here)`, `RULES: clean
  (656 files)`; `unittest discover -s build/tests`: `Ran 111 tests`, `OK`. Commit message = `commit-message.txt` byte
  for byte (575); tree = the kit's `ab8093c6`; 656 files.
- **The merge with main of the moment:** main = `e39396f9` = the head's parent: the merge IS the head (tree
  `ab8093c6`); the numbers above are its numbers.
- **The merge with lane W2's head, for MAIN MOVES (W2 first):** `git merge-base --is-ancestor e39396f9 67c24d18` rc 0
  (W2 is one commit on the same BASE); `git diff --stat e39396f9 67c24d18`: six paths, all `src/Datasec.Suite.Lab/**`
  or `tests/Datasec.Suite.Lab.Tests/**`; W2's push checks 4 of 4 success (GET). `git merge-tree --write-tree 67c24d18
  d3d10b71` rc 0, tree `b2a09571fab930b15751568a27222e1a7d03686c`; worktree `w2m` (W2's head + `read-tree -m -u` to that
  tree; `write-tree` = `b2a09571`): `g-w2m-restore` rc 0, no unstaged change after it; `g-w2m-build` rc 0, `0
  Warning(s)`, `0 Error(s)`; `g-w2m-test` rc 0: `total: 2093`, `failed: 0`, `succeeded: 2089`, `skipped: 4` (= 2054 + 39); `repo_rules.py <w2m>`: `RULES: clean (657 files)` (648 + 9).
  W2's own stub (`tests/Datasec.Suite.Lab.Tests/Oxpd1/Oxpd1Stub.cs`) reads no binding file: the port pin does not
  touch it.

## SCANS

- **gitleaks 8.30.1:** control FIRST (`gl.py control`: a token-shaped value built by a program from two halves and 36
  random characters, never printed, alone in a new folder): rc 1, `leaks found: 1`, folder and report moved to
  `g2017/_quarantine/`. `gitleaks dir <clone>` (`--no-banner --redact --ignore-gitleaks-allow --exit-code 1`): rc 0, `no
  leaks found`. Neutral copies (`gl.py neutral`): the 14 head blobs of the diff, the commit message as committed and the
  three patches as `1.txt` to `18.txt`: rc 0, `no leaks found`. Hosted secret-scan of the head: clean (both
  PLANTED-CONTROL lines, `objects of this commit not among them 0`, NEUTRAL-SCAN-REACH `not among the stored objects 0`).
- **words.py:** `--control` `CONTROL FIRED: 13 of 13`; the 55 added lines (`checks_ct.py`'s `added.txt`), the commit
  message, `pr-title.txt`, `squash-subject.txt`, `squash-body.txt`: `WORDS: clean (5 files)`. **HP's nine files**
  (commission: "HP's files included"), REPORTED not judged (their bytes are HP's): every word class 0 but `decided,
  ruled, approved, instructed` 2 (`uiconfiguration.wsdl:855` and `:921`, "This method instructs the device ...") and
  bytes outside printable ASCII (each file's CR bytes, plus the 3 and 9 high bytes): none is a name, a C-number, a
  B-number or a card id. Gate's own count of `B2nnn` / `C-nnn` over the repository texts and landing texts: 0 (control 8;
  FOUND 5).
- **squash_scan.py** (the clone's `build/`, equal to main `e39396f9`'s: `build/**` is in no diff of this lane): subject
  with `#43` + `squash-body.txt`: control rc 1 found 2; message rc 0 found 0; `SQUASH-SCAN: clean`.
- **Code scanning (GET):** main `e39396f9` csharp, python, actions `results_count` 0; open alerts 0. The branch push ran
  no Analyze (CodeQL runs at the pull request): landing.txt step 3.

## NOT RUN

The pin's red (seat's log only). Any CodeQL analysis of the head (none exists yet). The hosted legs of the W2 merge
(local macOS only). `fetch_ct.py`'s two refusals (H7, H8: no wrong jar made, no second fetch into an existing folder).
Any read of the jar's other entries or of HP's spec documents (commission bound; RELAYED from B2012). `repo_rules.py
--source-documents` (R5 hash half). Any device, tenant or HP contact.

## LANDING TEXTS (this folder)

`landing.txt` (head-pinned SQUASH by `<project>/CLAUDE.md:82`, the 8 check names, merge-ref numbers linux and windows
2054, RULES 656, csharp analysis 0, alerts 0, squash_scan, MAIN MOVES with W2 first: +39 tests, +1 rules file, the
measured merge tree `b2a09571`), `pr-title.txt`, `pr-body.md`, `squash-subject.txt` (`#PRNUM`), `squash-body.txt`,
`FOR-RECORDS.md` (with the kit's FOR RECORDS). No C-number or card id in any repository text (the PR body, the squash
subject and body, the commit and the README: 0). Who decided: the coordinator for the lane; the product owner's words
only as quoted with their dates.
