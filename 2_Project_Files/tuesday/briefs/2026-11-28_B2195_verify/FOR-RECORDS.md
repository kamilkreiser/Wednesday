# FOR RECORDS: gate B2195 (lane L1c, OXPd 1.x contracts, round 1 of 2)

For the records pass after the landing (no text of the gate goes into a project file by the gate itself).

- **Lane L1c (plan r2 row C12, line 69) DONE when the squash lands:** HP's OXPd 1.x authentication-agent folder (3
  files), the accessories callback pair (2), the scan folder whole (5, its callback pair included) and the two schemas
  they import (`mediadomain.xsd`, `optionsdomain.xsd`) committed byte for byte from the pinned SDK 1.8.4.1 jar
  (`f2bb325f...d341`), listed with their SHA-256 (23 lines become 35); C01's count 35; the stub's binding-port pin 11.
  No code. **Lane L6's "commit the scan description" step is done here** (RELAYED from the kit's FOR RECORDS).
- **Provenance, MEASURED by the gate:** the jar is signed (`META-INF/JARSIGNK.RSA`, signer certificate subject `O=HP
  Inc., OU=HP Cybersecurity, CN=HP Inc.`, issued by `DigiCert Trusted G4 Code Signing RSA4096 SHA384 2021 CA1`); the
  signature verifies over `JARSIGNK.SF` (control: one byte added fails), the `.SF`'s manifest digest equals the
  manifest's SHA-256, and all 35 committed files equal their manifest `SHA-256-Digest`. The certificate chain was NOT
  checked against a trust store or for revocation.
- **Licence, MEASURED as far as it goes:** the SDK folder `hp-ext-XX-oxpd-1.8.4.1` holds no licence or readme of HP's
  (recursive name search for licen/readme/eula/notice/terms/copyright): the only legal files are the Java API
  documentation's (`OXPdLib/Java/docs/legal/`: `LICENSE` reads "Please see ..\java.base\LICENSE",
  `ADDITIONAL_LICENSE_INFO` and `ASSEMBLY_EXCEPTION` the same form, `jquery.md` and `jqueryUI.md` the MIT texts of
  those libraries), which are the documentation tool's, not HP's terms for the descriptions. `Revision.txt` names the
  release notes (`hp-ext-XX-oxpd1.8.4.1-ReleaseNotes.txt`, `1.8.4.1 Release Email.txt`), which are NOT in the SDK
  folder. The jar holds no licence-like entry; the 12 files hold no licence or copyright line. **HP's terms for
  committing these files to a private repository: UNMEASURED** (the authority stays the clarifications' words the
  README quotes, read by the coordinator as covering OXPd 1.x descriptions; HP's SDK agreement itself not read).
- **For lane X95 / L1x (stampable only after this lands):**
  1. Its base is the squash of this lane; the three paths it reads (`contracts/oxpd1`, `src/Datasec.Suite.Adapters.Oxpd1`,
     `tests/Datasec.Suite.Adapters.Oxpd1.Tests`) change only in `contracts/oxpd1/**`, `ContractTests.cs:66` and
     `StubDevice.cs:200` and `:202`.
  1a. Expected numbers at that base if nothing else lands first (MEASURED by the gate on the squash tree `58145d4f`
     over main `d9f89115`): whole solution `total: 2539`, succeeded 2535, skipped 4 (windows 21); Oxpd1 executable
     133; `RULES: clean (774 files)`. Read the landed main's push run first; never assume these.
  2. The port pin is now **11** and the list **35**: any further binding moves both (a new schema alone moves C01 only).
  3. `StubDevice.Bindings()` now holds 106 soapActions including the agent and callback ones; the callback bindings
     share `wsdl:service` names with their device-side siblings (`AccessoriesService`, `ScanService`). A lane that
     serves or calls a callback must not key on the service name alone.
  4. The authentication agent's binding: SOAP 1.2 (`soap12:binding`), document/literal, three operations
     (`GetPrePromptResult`, `GetPostPromptResult`, `SignOutNotification`), endpoint reference in the 2005/08 namespace;
     the port-type file's `wsaw:Action` attributes are in `http://www.w3.org/2006/05/addressing/wsdl`; the 2004/08
     prefix is declared and never used. The same holds in the jar's authorization-agent files (not committed). The
     analysis `C1_oxpd1-platform-specs-sdk.md:177` ("SOAP 1.2 with WS-Addressing 2004", from HP's specification
     document) is NOT what the description files say; which namespace a printer sends on the wire is UNMEASURED until
     lane L1d.
  5. No cell compiles `authenticationagent.xsd` or `scan.xsd` (C05's set is five device-side schemas); the gate
     compiled all 13 committed schemas with `xmllint --nonet` (control fails).
- **Hygiene for the next OX-A kit (outside this lane's paths):** "seven committed bindings" at
  `tests/Datasec.Suite.Adapters.Oxpd1.Tests/TestServiceTests.cs:28` (summary) and
  `src/Datasec.Suite.Adapters.Oxpd1/README.md:52` (now eleven).
- **Analysis correction (records seat):** C1:177's addressing claim vs the WSDL (item 4 above); the README pin is at
  `contracts/oxpd1/README.md:10` at the head (was `:9`); `inputs.sha256` does not name the jar's hash.
- Nothing here ran against a printer, a device or a tenant.
