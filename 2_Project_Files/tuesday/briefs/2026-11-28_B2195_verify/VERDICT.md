GATE B2195: GO WITH FINDINGS @ f4aacb5 on main d9f8911

Gate G2 on Opus (claude-opus-5-5), round 1 of 2 of lane L1c, one reader, in-session, read-only. OXPd 2 project, lane
L1c (HP's OXPd 1.x authentication-agent, accessories-callback and scan descriptions), kit B2185, seat X94 (S4: Q1 "a"
the seat measures the jar, Q2 "IN" the stub pin, Q3-Q8 the defaults; every choice the coordinator's). Head
`f4aacb5e090fc27004ab1ca608779c48820ba361` on `b2185/x94-oxpd1-contracts-l1c`, ONE commit, one parent `cf224e1f`
(PR 61), tree `aececb52...` (gh api and the gate's clone agree). **MAIN MOVED during the gate:** PR 62 (lane L2 Entra)
merged 2026-11-27T15:49:38Z (02:49:38 AEDT); main is now `d9f89115333bbed2ade723e4c11d523b2a9cd079` (one parent
`cf224e1f`, tree `aa53e949...` = gate B2194's measured squash tree, 762 files, its push run `HOSTED ... PASS` at 2539 /
762 read by the gate). compare `cf224e1f...d9f89115`: 21 files, all under `src/Datasec.Suite.Identity.Entra/` and
`tests/Datasec.Suite.Identity.Entra.Tests/`: none of this lane's 16 paths. compare `main...f4aacb5e`: diverged, ahead 1,
behind 1, 16 files. Open pull requests 0.

Read and measured 2026-11-28 02:47 to about 03:20 AEDT in scratch `fleet/state/s337/g2195/` (clone of the seat's clone
by `git clone --no-hardlinks`, push URL `invalid://no-push`, branch `gate-head` at the head; `fetched/` the gate's own
extraction of the 12 files from the jar; `merged/repo` the new main's tarball by `gh api -X GET`, indexed, with the
head's 16 blobs over it). Every dotnet job and test executable through the canonical `heavy.py` (sha256 `31adedc8...`,
equal to S8) and the OXPd wave lock, one at a time, owner `G2195 gate reader (Tuesday s337)`; released lock folders in
`g2195/_quarantine/locks/`, another holder's lock never touched. Origin by `gh api -X GET` under the project
GH_CONFIG_DIR. No write to the project, GitHub, Jira or the NAS; the jar and the SDK folder read only; no push, no pull
request, no re-run; nothing to any printer, device, tenant, Azure, Microsoft host or HP; nothing deleted (the gitleaks
control moved to `g2195/_quarantine/`).

**BLUF.** The head is what the kit says and nothing else. The jar hashes to the pin (`f2bb325f...d341`); the gate's own
selection by property over the jar's entry names gives exactly the 12 added paths (A 3, B 5, C 2, D 2: `mediadomain.xsd`,
`optionsdomain.xsd`), and the gate's own extraction equals the branch's blobs byte for byte, 12 of 12 (control: one
changed byte is not equal). Beyond the kit: the jar is SIGNED by HP Inc. (CMS signature verifies over its `.SF`; control
fails), and all 35 committed files equal the signed manifest's SHA-256 digests. The head's tree is main `cf224e1f` plus
the 16 paths (12 A, 4 M, 0 D, 0 renames); the `.cs` diff is `ContractTests.cs:66` (23 to 35) and `StubDevice.cs:200`,
`:202` (7 to 11, "seven" to "eleven") only, and 11 is both the inventory's and the gate's own port count. Envelope
re-measured from the files: one EndpointReference namespace (2005/08), the 2004 namespace used 0 times (declared in 22
files), one `wsdl:service` and a soapAction on every operation of all 11 bindings, 106 soapActions with no collision
(also ignoring case), every `Single()` target unique ignoring case, `IsServiceEnabled` the only non-Get name admitted.
Gate's own runs: Oxpd1 133 / 0 at the head; four red-proof arms of the gate's own at the PUSHED head (`4 of 4 MATCH`,
C01 and C02 the only reds, `Actual: 3`, each undone and re-hashed equal); the squash onto the moved main (tree
`58145d4f...`, 774 files) locked restore rc 0, build 0 / 0, Oxpd1 133 / 0, whole solution `total: 2539`, `failed: 0`,
`succeeded: 2535`, `skipped: 4`, `RULES: clean (774 files)`, `Ran 117 tests` OK. gitleaks (control rc 1) clean over `main..head`, its 17 blobs and the
message; `words.py` clean over the added lines and the message. The hosted push run of the head reads PASS at 2488 /
756. Nine Info findings; none blocks the landing.

## FOUND (round 1 of 2; grade Blocker / Major / Minor / Info)

1. **Info (the commission's pin pointer).** The commission says the jar's pin is "the hash `contracts/oxpd1/inputs.sha256`
   names"; `inputs.sha256` does not name it (0 hits). The pin is `contracts/oxpd1/README.md:10` at the head (`:9` at
   BASE: this commit added a README line above it) and `l1c.py`'s `JAR_SHA256`; the jar's sha256 equals both
   (`f2bb325f801cc2d6ef8e253abda54280129f5c9090bcc6342eb2a63109c3d341`, 1,613,168 bytes; control: one changed character
   is not in the README).
2. **Info (Tuesday's point d: the agent shape; the analysis is wrong about the description files).** The committed
   `AuthenticationAgentSoap12Binding.wsdl` is SOAP 1.2 (`soap12:binding`), document/literal, three operations
   (`GetPrePromptResult`, `GetPostPromptResult`, `SignOutNotification`); its one port's `EndpointReference` is in
   `http://www.w3.org/2005/08/addressing` (prefix `wsa10`); it DECLARES `wsa` and `wsap` in the 2004/08 namespace and
   uses neither (0 elements, 0 attributes); its port-type file's `Action` attributes are in
   `http://www.w3.org/2006/05/addressing/wsdl`. So the envelope PASS stands on the files. **The authorization agent in
   the same jar (`authorizationagent_2013_03_01`, not committed) has the SAME shape** (soap12, EPR 2005/08, 2004 declared
   and used 0 times, `wsaw:Action`), so a later lane that commits it will NOT meet the 2004 namespace in the description
   files, and the stub's one-namespace rule will hold (all five agent bindings in the jar: EPR 2005/08). The analysis
   `C1_oxpd1-platform-specs-sdk.md:177` ("SOAP 1.2 with WS-Addressing 2004") cites HP's specification document, not the
   WSDL; **which addressing namespace a printer SENDS on the wire to an agent is UNMEASURED** (R9, lane L1d). A records
   correction for the analysis, and a line lane L1's drafter must read: the WSDL is not evidence of the wire.
3. **Info (licence and provenance, Tuesday's point e).** Provenance MEASURED: `META-INF/JARSIGNK.RSA` names signer
   `C=US, ST=California, L=Palo Alto, O=HP Inc., OU=HP Cybersecurity, CN=HP Inc.`, issuer `DigiCert Trusted G4 Code
   Signing RSA4096 SHA384 2021 CA1`; `openssl cms -verify -noverify` over `JARSIGNK.SF` rc 0 (control, one byte added:
   rc 4, bad signature); the `.SF`'s `SHA-256-Digest-Manifest` equals the manifest's SHA-256
   (`KuWIlhRx...BLcg=`); 35 of 35 committed files equal their manifest `SHA-256-Digest`. The chain was not checked
   against a trust store or for revocation. **Licence: UNMEASURED.** The SDK folder (`hp-ext-XX-oxpd-1.8.4.1`, name
   search for licen / readme / eula / notice / terms / copyright, recursive) holds no licence or readme of HP's. The only
   legal files are the Java API documentation's, `OXPdLib/Java/docs/legal/`: `LICENSE` (33 bytes) "Please see
   ..\java.base\LICENSE"; `ADDITIONAL_LICENSE_INFO` "Please see ..\java.base\ADDITIONAL_LICENSE_INFO";
   `ASSEMBLY_EXCEPTION` "Please see ..\java.base\ASSEMBLY_EXCEPTION"; `jquery.md` and `jqueryUI.md` (the MIT texts of
   jQuery 3.7.1 and jQuery UI): the documentation tool's notices, not HP's terms. `Revision.txt` names
   `hp-ext-XX-oxpd1.8.4.1-ReleaseNotes.txt` and `1.8.4.1 Release Email.txt`, which are NOT in the SDK folder. The jar
   holds no licence-like entry (its `META-INF` holds only the manifest and the signature pair); the 12 files hold no
   licence or copyright line (one `Confidential` hit is an enumeration value for a stamp, `optionsdomain.xsd:2553`).
   Nothing read restricts committing these files to a private repository, and nothing read permits it: the authority
   stays the clarifications' words the README quotes (C-56, read by the coordinator as covering the OXPd 1.x files;
   C-74), as for the 23 already committed. HP's SDK agreement itself: not read.
4. **Info (stale "seven" outside the lane's paths).** `TestServiceTests.cs:28` ("the seven committed bindings", the
   seat named it) AND `src/Datasec.Suite.Adapters.Oxpd1/README.md:52` ("Over every operation of the seven committed
   bindings, no other name without `Get` passes"): both now eleven. The README line is still TRUE of the property (T01
   runs over all 11; measured: 66 non-Get names, only `IsServiceEnabled` admitted), only the count is stale. OX-A's
   folder; a hygiene line for its next kit.
5. **Info (a README count that can be misread).** `contracts/oxpd1/README.md:12`: "the import closure of seven bindings
   the device serves". The device also serves `ScanService` (`ScanSoap12Binding.wsdl`, 20 operations), now committed,
   so eight committed bindings are device-served. The sentence describes the original seven's closure and the next bullet
   names the scan folder; a reader could still count seven. Wording for the next touch of this README.
6. **Info (no cell compiles the new schemas or calls the new operations).** C05's `Schemas()` compiles five schemas
   (`ContractTests.cs:153`: deviceinfo, authentication, accessories, authorization, test). MEASURED by the gate:
   all 13 committed `.xsd` compile with `xmllint --nonet` (control: a broken schema does not); every import of the 35
   files resolves inside `hp/` (37 imports, 0 dangling); each new binding's operations equal its port type's (3/3, 3/3,
   2/2, 20/20). A lane that reads these files extends C05.
7. **Info (the stub serves callback and agent actions; a service name shared).** The seat's R6 extension, confirmed:
   `AccessoriesCallbackSoap12Binding.wsdl` names `wsdl:service` `AccessoriesService` and `ScanCallbackSoap12Binding.wsdl`
   names `ScanService`, the same as their device-side siblings. `StubDevice.Bindings()` keys by soapAction
   (`map[action] = ...`, Ordinal, last writer wins, so a future collision would be SILENT in the stub; the envelope
   check is what catches it) and compares the service name only with the request path, so the stub would answer
   `ScanJobEvent` posted to `/ScanService`. The read form admits the agent's `GetPrePromptResult` and
   `GetPostPromptResult` by their `Get` prefix; no exposure (the read catalogue is the closed seven-row enum; T02 holds).
8. **Info (the seat's deviations, read).** DEVIATIONS 2 (one build job re-run after `BLOCKED: lock held`, a lock wait,
   not a red) is a reading of the kit's "about 90 in all" line that the gate accepts: no test or red was retried.
   DEVIATIONS 3 (red first, pin red and red proof at BASE `7d652c5f` only): the three paths were byte-equal at all three
   mains (seat's `diff --quiet` rc 0, and the gate's M-path check below), and the gate's own four arms ran at the PUSHED
   head `f4aacb5e`: covered.
9. **Info (records only).** (a) The commit subject is 275 characters (284 with ` (#PRNUM)`). (b) The commit message
   quotes the clarifications without the README's caveat that the first was said of OXPd 2 files; the squash body in this
   folder points to the README's quotes instead of repeating them (the README and the PR body carry the caveat). (c) The README's "as the first 14 were" (`:23`) predates
   this lane (`:18` at main), now 23 before this commit: unchanged by this lane, left. (d) `optionsdomain.xsd` starts
   with a UTF-8 BOM and three new files hold bytes above 0x7E (mediadomain 24, optionsdomain 3, scan.xsd 76): kept by
   `* -text`; the windows leg's Oxpd1 tests passed on them.

## THE KIT'S GATE LIST (its FOR TUESDAY, "THE GATE"), each measured

- **Re-hash from the pinned jar (`verify1.out`).** Jar sha256 = the README pin = `l1c.py` `JAR_SHA256`. The jar's
  `META-INF/wsdls/` holds 144 entries in 29 folders; ONE `_service_authenticationagent_` folder (3 entries), ONE
  `_service_scan_` folder (5), ONE `_service_accessories_` folder (callback-named: 2). Import closure from those 10 over
  the jar: 15 files, 0 dangling; not committed at main and outside A/B/C: exactly `mediadomain.xsd` and
  `optionsdomain.xsd` (2, under 8). **Selection by property (12) == the paths added at the head (12): True.** Byte compare
  of the gate's extraction (`zipfile`, into `g2195/fetched/`) with `git show <head>:<path>`: **12 of 12 EQUAL** (sha256
  and sizes as the seat's FOR TUESDAY list, every file CRLF). The 23 files already on main: 23 of 23 equal to the jar.
  The Test callback pair is in the jar (`TestCallbackSoap12Binding.wsdl`, `testCallback.wsdl`) and NOT committed.
- **The list.** `inputs.sha256`: 23 lines at main, 35 at the head; main's 23 kept byte for byte and in order (a
  subsequence); sorted by path in byte order; unique; LF only; every listed hash equals its head blob; the listed set ==
  the files under `hp/`. No line holds `..`, a backslash or CR.
- **The README's new lines against the files.** "35 files" (35 listed); "every file of the jar's `authenticationagent`
  folder" (3 of 3), "the accessories files whose name holds `callback`" (2 of 2), "every file of the jar's `scan`
  folder" (5 of 5), "with the files they import (12 files; the bindings here now hold 11 ports in all)" (12; 11 ports);
  "The Test service's callback pair ... is still not here" (true); "The stub reads every binding here, the solution-side
  ones included" (true: `Bindings()` and `AddressingNamespace()` glob `*Soap12Binding.wsdl`). All true; F5 is a wording
  note on an older sentence.
- **The pin's red and the red proof.** The seat's logs, read by the gate: red first `Total: 133, Errors: 0, Failed: 2`
  (`[FAIL]` 2); pin red `Failed: 82`, `[FAIL]` 82, "over seven ports" 82, C01 or C02 among them 0; green `Failed: 0`.
  The seat's `REDPROOF: 12 of 12 MATCH, 12 of 12 undone equal` (at BASE). **The gate's own arms** (`runs.py redproof`,
  each the first CR of the file to a space, the Oxpd1 executable whole through `heavy.py`, undone, re-hashed), at the
  pushed head, after a gate build (`0 Warning(s)`, `0 Error(s)`) and green `Total: 133, Errors: 0, Failed: 0`:
  ```
  GATE-REDPROOF 1 AuthenticationAgentSoap12Binding.wsdl | rc 1 Total 133 Failed 2 | red C01 C02 | Actual 3 | MATCH | undone equal True
  GATE-REDPROOF 2 scan.xsd                              | rc 1 Total 133 Failed 2 | red C01 C02 | Actual 3 | MATCH | undone equal True
  GATE-REDPROOF 3 mediadomain.xsd                       | rc 1 Total 133 Failed 2 | red C01 C02 | Actual 3 | MATCH | undone equal True
  GATE-REDPROOF 4 accessoriesCallback.wsdl              | rc 1 Total 133 Failed 2 | red C01 C02 | Actual 3 | MATCH | undone equal True
  ```
  One per family (A, B, D, C). After: `status --porcelain --untracked-files=all` 0 rows; the executable `Total: 133,
  Errors: 0, Failed: 0`.
- **The envelope (`verify2.out`, ElementTree over the head's files, case-insensitive glob as on Windows).** 11 binding
  files, 11 ports, EPR namespaces `['http://www.w3.org/2005/08/addressing']`; the 2004/08 namespace: 0 uses, 22 files
  declare it; every binding: 1 `wsdl:service`, soap12 binding, soapAction on every operation (missing 0); 106 soapActions,
  106 distinct, collisions 0 (ignoring case 0); `Single()` targets (`deviceinfo.xsd`, `authentication.xsd`,
  `accessories.xsd`, `authorization.xsd`, `test.xsd`, `uiconfiguration.xsd`, `certificatemanagement.xsd`,
  `TestSoap12Binding.wsdl`) 1 each ignoring case; no basename or path held twice ignoring case; non-Get names 66, the read
  form admits `['IsServiceEnabled']` only.
- **`BASE..head`** (base = the head's parent `cf224e1f`): 12 `A` + 4 `M`, 0 `D`, 0 renames; added files mode 100644, all
  under `contracts/oxpd1/hp/`.

## TUESDAY'S OWN POINTS

- **(a) The rebase.** `ls-tree -r` of `cf224e1f` (744 paths) and of the head (756): differing paths exactly 16 (12
  absent at main, 4 with another blob), every other path the same mode and blob. True.
- **(b) `StubDevice.cs`.** `git diff cf224e1f HEAD`: one hunk, lines 200 (`ports != 7` to `ports != 11`) and 202
  ("over seven ports" to "over eleven ports"); 11 = the inventory's `STUB-PREDICT ports 11` = the gate's own port count.
- **(c) `ContractTests.cs`.** One line, 66: `Assert.Equal(23, ...` to `Assert.Equal(35, ...`. True.
- **(d) The agent's addressing.** F2.
- **(e) Licence and provenance.** F3.

## ADVERSARIAL BEYOND THE KIT (three shapes outside each property; each covered or a named limit)

| Property | Shape outside the tested one | Covered by / limit |
|---|---|---|
| P1 list | a list line `hp/../x` | C01 checks only the `hp/` prefix, so it would accept and hash a file outside `hp/`: named limit; MEASURED 0 such lines (and 0 with a backslash or CR) |
| P1 list | a hidden file under `hp/` (e.g. `.DS_Store`) | C01 names it (`GetFiles "*"` includes hidden files); 0 present |
| P1 list | two paths equal ignoring case (Windows) | 0 (measured); the windows leg's C01 green on the head's push run |
| P2 stub | a callback binding sharing a device-side `wsdl:service` name | named limit R6 (F7), MEASURED twice |
| P2 stub | soapActions equal ignoring case; a silent overwrite in `Bindings()` | 0 of 106 (measured); the envelope, not the stub, is what catches a collision (F7) |
| P2 stub | a binding whose operations differ from its port type; two services in one file | 4 of 4 equal; 1 service per file (measured) |
| P3 bytes | the jar not HP's | signed by HP Inc., signature verifies, 35 of 35 manifest digests (F3) |
| P3 bytes | a BOM or bytes above 0x7E altered by a checkout | byte compare 12 of 12; `* -text`; windows leg green (F9d) |
| P3 bytes | a committed file of main drifted from the jar | 23 of 23 equal |
| P4 selection | other callback families in the jar (copy, sendfax, test) | outside the property (C is the accessories folder only; B is the scan folder only); not committed (measured) |
| P4 selection | the jar's `Bindings/*Callback-jaxws-bindings.xml` (JAX-WS build customisation files for accessories and scan callbacks) | outside the `wsdls/<service>` folders; not descriptions; not committed; named limit |
| P4 selection | an import beyond depth one, or a dangling one | the gate's transitive closure over the jar: 0 dangling; over the committed tree: 37 imports, 0 dangling |

## SCANS

- gitleaks 8.30.1: control FIRST (a token built from two halves and 36 random characters, never printed): `dir` rc 1,
  `leaks found: 1` (moved to `g2195/_quarantine/leakctl-2026-11-28`); `git` over `cf224e1f..f4aacb5e` rc 0 (`1 commits
  scanned`, `no leaks found`); the 16 head blobs and the commit message under neutral names (`g2195/blobs/1.txt` to
  `17.txt`) `dir --ignore-gitleaks-allow` rc 0, `no leaks found`. The squash texts: `build/squash_scan.py` (from the
  clone) over `squash-subject.txt` with `#63` and `squash-body.txt`: control found 2, message found 0, `SQUASH-SCAN:
  clean`.
- `words.py` (sha256 `6f932dc5...`, the kit's): `--control` `CONTROL FIRED: 13 of 13`; over the gate's `added.txt` (29
  lines of the four changed files; `cmp` equal to the seat's `checks3/added.txt`) and the commit message: `WORDS: clean
  (2 files)`; over the squash subject (`#63`), the squash body and the PR title: clean. `pr-body.md`: 1 `coordinator`
  (the commission asks the body to say the choices are the coordinator's) and 4 bytes of the attribution line's emoji;
  it is not a commit text. `B2nnn`, `C-nnn`, `X9n` over `added.txt` and the message: 0 and 0 (control: this commission
  counts 8 lines).
- CodeQL: not run by the gate; main `d9f89115`'s analyses read: csharp, python, actions results 0; open alerts 0.

## HOSTED

- The head's push run (gate's `hosted3.py`, sha256 `969fe376...`): `HOSTED f4aacb5e090fc27004ab1ca608779c48820ba361:
  PASS` at `--total 2488 --rules 756` (linux succeeded 2484, skipped 4, GUARD 14; windows 2467, 21, GUARD 15; the
  Oxpd1 test dll `passed` on windows on HP's CRLF bytes).
- The new main's push run: `HOSTED d9f89115333bbed2ade723e4c11d523b2a9cd079: PASS` at `--total 2539 --rules 762`
  (`--wait`; the first read, while windows was in progress, printed `FAIL 1 (check run windows not completed success)`).

## THE MERGE WITH THE MOVED MAIN (the commission's moved-main rule)

- New main `d9f89115` (PR 62), read at 02:53 and again at 03:12:56 (unchanged; branch still `f4aacb5e`; open pull
  requests 0; open code-scanning alerts 0). Its tarball (`gh api -X GET .../tarball/d9f89115...`) indexed in
  `g2195/merged/repo` writes tree `aa53e9491d93cdde65be94dca7b4297fb96fe66f` = main's own tree (762 files).
- Overlay rule (`overlay.py`): every M path at the new main equal to `cf224e1f`'s bytes (4 of 4 True), every A path
  absent (12 of 12 True): no conflict is possible. The head's 16 blobs over it write **tree
  `58145d4fbf174b95b8af3f3c4ae8d3901fc53f79`, 774 files** (= 762 + 12).
- On that tree, through the canonical runner (owner `G2195`): `m-restore` (`CI=true`, `--locked-mode`) rc 0;
  `m-build` rc 0, `0 Warning(s)`, `0 Error(s)`; `m-exe-oxpd1` `Total: 133, Errors: 0, Failed: 0`; `m-test-solution`
  (`TIMEOUT=1800`) rc 0, **`total: 2539`, `failed: 0`, `succeeded: 2535`, `skipped: 4`**, `[FAIL]` 0 (2539 = the new
  main's 2539 + 0: this lane adds no cell). Not heavy: `repo_rules.py` (no `--source-documents`; the merged folder has
  no `1_Project_Definition`) `RULES-NOTE: R5 hash half NOT RUN (no supplied-source folder here)`, **`RULES: clean (774
  files)`**; `unittest discover -s build/tests` `Ran 117 tests`, `OK`. At the head alone: `RULES: clean (756 files)`.
- Expected on the PR's merge ref with main `d9f89115`: linux and windows `total: 2539`; linux `succeeded: 2535`,
  `skipped: 4`; windows `succeeded: 2518`, `skipped: 21` (DERIVED: the windows skip count as on both mains' push runs);
  GUARD 14 and 15 (unchanged: no contract file is published); `RULES: clean (774 files)`.

## NOT RUN

- The gate's own pin red (a `.cs` revert and a rebuild): the seat's log read instead (82 of 82). Arms 5 to 12 of the
  red proof (the seat's 12 of 12 at BASE; the gate's 4 at the head).
- The whole solution at the head alone (the seat's three rounds and the head's hosted run at 2488; the gate ran the
  MERGED tree instead, which is what lands).
- CodeQL locally; the certificate chain against a trust store; HP's SDK agreement (not in the SDK folder).
- Nothing against a printer, device, tenant, Azure, a Microsoft host or HP.
