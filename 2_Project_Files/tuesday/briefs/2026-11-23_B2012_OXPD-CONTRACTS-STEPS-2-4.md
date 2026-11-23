# B2012 -- OXPd CONTRACTS measurement: HP's service descriptions for first-run steps 2, 3 and 4

Drafter lane B2012 of commission `2026-11-23_B2010-B2012_OXPD-WAVE4-RECORDS-W2-CONTRACTS_DRAFTER_COMMISSION.md` (Tuesday s319). Read-only report, no kit, no seat. Written 2026-11-23 after 22:46 AEDT. Every number below was measured by this drafter's own commands tonight; nothing is RELAYED unless marked.

## BLUF

**ANSWERED: YES. All three are FOUND in HP's library, and NONE is under `contracts/oxpd1/` at main.**

- The descriptions live in the SAME jar the committed 14 files were taken from: `OXPdLib-1.8.4.jar` of SDK 1.8.4.1, SHA-256 `f2bb325f801cc2d6ef8e253abda54280129f5c9090bcc6342eb2a63109c3d341` (the exact hash `contracts/oxpd1/README.md` pins), entries `META-INF/wsdls/<folder>/<file>`.
- Step 2 -> **Test** service (`..._OXPd_service_test_2010_04_14`): `IsServiceEnabled`, `EnableService`, `DisableService`, `GetScreenCapture` (19 operations in the binding).
- Step 3 -> **CertificateManagement** service (`..._OXPd_service_certificatemanagement_2010_04_14`): `ExportCertificates`, `ImportCertificate`, `RemoveCertificate` (6 operations).
- Step 4 -> **UIConfiguration** service (`..._OXPd_service_uiconfiguration_2010_04_14`): `GetTopLevelButtonRecords`, `RegisterTopLevelButton`, `UnregisterTopLevelButton` (25 operations).
- Import closure: 3 files per service, plus `common.xsd`, which is already committed with an identical hash. **A CONTRACTS lane adds 9 files and changes no committed byte.**
- HP's own wording raises four hazards the write lanes must cover (see section 4). Two of them are the same kind as gate B2008 FOUND 2 (an undo that removes or overwrites something that was already on the device). The third is HP's warning that self-signed certificates are "not recommended/supported" in the OXPd CA store. That bears on step 3's "our development CA".
- Licence: the WSDL/XSD files themselves carry no copyright or licence text (0 hits). The library's README and HP's spec "Legal Notices" carry restrictive wording. It is quoted in section 5 and reported, not decided. Kam's 17:56 note (C-74) is the ruling on use of HP code.

## 1. Sources (re-measured tonight)

| What | Where | Measured |
|---|---|---|
| OXPd main | `datasecau/OXPd_2` by `gh api -X GET` (project GH_CONFIG_DIR) | `e39396f91dbfba3c46cc43d7790adb59581d2853`, tree `4af54a4bd6580ead93f629d705a728b0c487b17f`, subject "Lab tool hygiene before the first printer run ... (WP0.2) (#42)" |
| `contracts/oxpd1/` at main | git tree `ae7c32dfd75a232714c65e60756f8edb17931a69` | `.gitattributes`, `README.md`, `inputs.sha256`, 14 files under `hp/`. All 14 fetched by GET and hashed: **all 14 match `inputs.sha256`** |
| Pinned jar | `/Volumes/DEV-Working/Datasec/Friday/2026-11-19_oxpd-friday-work-and-library/OXPd/OXPd1-NET-Java/SDK/hp-ext-XX-oxpd-1.8.4.1/OXPdLib/Java/lib/OXPdLib-1.8.4.jar` | sha256 `f2bb325f...c3d341` = README's pin. 100 `.wsdl`/`.xsd` entries under `META-INF/wsdls/`. Its 4 committed bindings re-hash to the committed values (`910e541d...`, `e48bb98c...`, `ee8ed330...`, `0511705f...`), so provenance holds |
| Other jars (not the pin) | the same library: `.../hp-ext-XX-oxpd-1.8.4/OXPdLib/Java/lib/OXPdLib-1.8.4.jar` and two `OXPd1_solution-master/lib/` copies (`debf18cd...`); `.../1.8.2.1/.../OXPdLib-1.8.2.jar` (`4586c519...`); `.../OXPd1.7.3.2ProfessionalOnlybeta/.../OXPdLib-1.7.3.jar` (`4aa4f995...`) | not used. Note that the 1.8.4 package's jar has the same name and a different hash (README says so too) |
| .NET SDK classes | `.../hp-ext-XX-oxpd-1.8.4.1/OXPdLib/DotNet/` (`ITestProxy.cs`, `ICertificateManagementProxy.cs`, `IUIConfigurationProxy.cs`, `codegen/Test.cs`, `codegen/CertificateManagement.cs`, `codegen/UIConfiguration.cs`, `bin/Release/OXPdLib-1.8.4.dll` + `.XML`, `net8.0/OXPdLibCore-1.8.4.dll`) | every step-2/3/4 operation name appears in the matching interface (2 occurrences each). Control: `RegisterAuthenticationAgent` appears 2 times in `IAuthenticationProxy.cs` |
| HP specs (markdown) | `.../OXPd1-NET-Java/Docs/oxpd-test-service-specification.md`, `oxpd-certificate-management-service-specification.md`, `oxpd-browser-use-model-and-ui-configuration-service-specification.md`, `sdk-compatibility-guide.md` | quoted below |

The jar's `META-INF/wsdls` was extracted (read-only `unzip` into the session scratchpad, nothing written to the NAS) to read the files.

## 2. Per step

### Step 2: Test service on/off + one control-panel screenshot. **FOUND**

- Folder in jar: `META-INF/wsdls/http__www.hp.com_schemas_imaging_OXPd_service_test_2010_04_14/`
- Binding `TestSoap12Binding.wsdl`, 19 operations: AsyncEchoBinary AsyncEchoBinaryComplete AsyncEchoString AsyncEchoStringComplete **DisableService EnableService** ExecuteJavaScript GetBrowserState **GetScreenCapture** GetTestConfiguration GetTestStatistics **IsServiceEnabled** LaunchAppAccessPoint PressKey PressScreen SetCaret SetTestConfiguration SyncEchoBinary SyncEchoString.
- `test.wsdl` line 522, `EnableService`: "Enables the service. (The service is disabled by default at bootup.)". Line 527: "As of MinorRevision 1.1". Line 525: "it requires the caller to supply the device administrator credentials in the HTTP request header. Missing credentials will be challenged with a 401 response. Invalid credentials will result in a 403 response."
- `test.wsdl` line 545, `DisableService`: "Disables the service. (The service is disabled by default at bootup.)" (MinorRevision 1.1). Line 502, `IsServiceEnabled`: "When disabled, only this method, the EnableService method, and the DisableService method will be functional."
- `test.wsdl` line 363, `GetScreenCapture`: "Captures and returns the current content of the control panel display as a PNG, provided for test purposes." The same block requires admin credentials, and line 384 reads: "Subcode=&quot;IllegalOperation&quot; if the service is disabled." No MinorRevision tag, so it is in the base revision.
- Spec `oxpd-test-service-specification.md` line 23: "As of Minor Revision 1.1, the OXPd:Test service is disabled by default and must be explicitly enabled after every reboot before any of its functions can be used." Line 25: "These methods must not be used by a production solution." Line 35: "The service will remain enabled until disabled or until the device is rebooted." This matches step 2's undo ("reboot, or one disable call").
- Version: service namespace 2010-04-14; 12 operations are marked "As of MinorRevision 1.1" in `test.wsdl`.

### Step 3: development CA certificate upload + delete. **FOUND**

- Folder: `META-INF/wsdls/http__www.hp.com_schemas_imaging_OXPd_service_certificatemanagement_2010_04_14/`
- Binding `CertificateManagementSoap12Binding.wsdl`, 6 operations: **ExportCertificates ImportCertificate RemoveCertificate** ExportRemoteAppCertificates ImportRemoteAppCertificate RemoveRemoteAppCertificate. The three RemoteApp operations are "As of MinorRevision 1.1". `ImportRemoteAppCertificate` is "For Internal Use Only" (line 207), so it is not ours.
- `certificatemanagement.wsdl` line 100, `ImportCertificate`: "Adds a CA certificate to the device's certificate store (min size=1, max size=10240)."
  - Line 104: "If the certificate is already in the store, this operation will succeed (no exception thrown), but will have no effect (i.e. the certificate will not be duplicated)."
  - Line 105: "Imported certificates are stored in non-volatile memory on the device and are cleared by a disk init or partial clean (not by a restore factory settings)."
  - Lines 110 to 111: the admin-credential paragraph (401/403).
  - Line 135: "The use of self-signed certificates with the OXPd CA Certificate store is not recommended/supported. HP has discovered several cases of incompatible self-signed certificates, most notably those created using the IIS7 certificate generation tool. ... certificate validation on a particular codebase may become even more strict in future firmware releases".
- Line 169, `RemoveCertificate`: "Removes the supplied CA certificate from the certificate store". Line 171: "If the supplied certificate does not exist in the device's certificate store, this method will succeed (no exception thrown), but will have no effect."
- Line 64, `ExportCertificates`: "Returns the list of CA certificates in the device's certificate store (each certificate in PEM format)." It is admin-credentialed and serves as the read-before-write.
- Version: namespace 2010-04-14. The step-3 operations carry no MinorRevision tag, so they are in the base revision.

### Step 4: register / unregister one top-level test button. **FOUND**

- Folder: `META-INF/wsdls/http__www.hp.com_schemas_imaging_OXPd_service_uiconfiguration_2010_04_14/`
- Binding `UIConfigurationSoap12Binding.wsdl`, 25 operations, among them **GetTopLevelButtonRecord GetTopLevelButtonRecords RegisterTopLevelButton UnregisterTopLevelButton**, plus `SetApplicationFailureBehavior` / `GetApplicationFailureBehavior(s)`. Those last ones relate to B1968 needs-list step 4 ("Enable HP home screen if OXPd app fails to load"). That is a note only, not a proposal to call them.
- `uiconfiguration.wsdl` line 269, `RegisterTopLevelButton`: "Adds a top-level button record."
  - "all compliant devices will be tested to an arbitrary maximum of 20 buttons."
  - "**If the new button record's guid matches an existing record's, the new record overwrites the existing one.**"
  - "devices will handle UUIDs as case-sensitive strings"
  - "this method may return before the new button ... has become manifest on the device's control panel."
  - "The record is stored in non-volatile memory on the device and is cleared by a disk init or restore factory settings."
  - It requires admin credentials (401/403). A valid guest credential gets `SecurityAccessDeniedException`.
- Line 308, `UnregisterTopLevelButton`: "Removes the specified top-level button record." Then "If the button ID does not match an existing button record, this method will succeed (no exception thrown), but will have no effect."
- Line 343, `GetTopLevelButtonRecords`: "Returns the list of top-level button records configured on the device." This is the read-before-write.
- Version: namespace 2010-04-14. The file carries MinorRevision tags 1.1 (11), 1.2 (3), 1.3 (9) and 1.4 (6). The three button operations above carry no tag, so they are in the base revision.

### Which FutureSmart / OXPd 1.x level

- All three services are OXPd 1.x SOAP services with namespace date 2010-04-14, shipped in OXPdLib 1.8.4 (SDK 1.8.4.1, `Revision.txt`: "Build Date: Mon 06/23/2025").
- The only level gate in the operations used is the Test service's on/off trio, which needs **MinorRevision 1.1**. Before 1.1, the spec implies the service was not disabled by default.
- `sdk-compatibility-guide.md` line 133: "HP Color LaserJet M577 MFP | X | X |" (OXPd Java/.Net and OXPd JavaScript both supported). No file read maps an OXPd MinorRevision to a FutureSmart bundle number (search: "minor revision" within 80 characters of "futuresmart" in `OXPd1-NET-Java/Docs`, 0 hits). **The M577's actual Test-service MinorRevision is UNMEASURED.** First-run step 0 (DiscoveryTree) or step 1 (DeviceInfo) reads it on the device.

## 3. `contracts/oxpd1/` at main: NOT present (positive control fired)

Over all 14 committed files under `hp/`, fetched by GET at `e39396f9` and hash-verified, case-insensitive `grep -o -i | wc -l`:

| term | count |
|---|---|
| EnableService, DisableService, IsServiceEnabled, GetScreenCapture | 0, 0, 0, 0 |
| ImportCertificate, RemoveCertificate, ExportCertificates | 0, 0, 0 |
| RegisterTopLevelButton, UnregisterTopLevelButton, TopLevelButton | 0, 0, 0 |
| `service/test`, `certificatemanagement` | 0, 0 |
| `uiconfiguration` | 3: prose only (`securitydomain.xsd:730` names `OXPd:UIConfiguration.GetApplicationAccessPoints`; `common.xsd:36,379` say BrowserTarget was "originally defined only in the uiconfiguration namespace"), no operation |
| **control** RegisterAuthenticationAgent / GetManufacturerInfo | **26 / 14** |

The committed bindings hold 30 operations (Accessories 18, Authentication 6, Authorization 4, DeviceInfo 2). This drafter re-counted that tonight, and it agrees with B2005's drafter's count.

## 4. Hazards in HP's own words that the write lanes must cover (for the kits, not decided here)

1. **Step 3: the undo can remove a certificate that was already there.** `ImportCertificate` of a certificate already in the store "will succeed ... but will have no effect". A blind `RemoveCertificate` undo would then delete a pre-existing certificate. This is the same class as gate B2008 FOUND 2. Default proposal: `ExportCertificates` READ first, and refuse to import (or record "no undo owed") when our CA is already present.
2. **Step 4: the register can overwrite an existing button.** A matching guid "overwrites the existing one", so the undo would then remove someone else's button. Default proposal: a `GetTopLevelButtonRecords` READ first, and refuse on a guid clash. Use a fresh, case-exact UUID.
3. **Step 2: the undo can change the prior state.** If the service is already enabled, a `DisableService` "undo" changes state we did not set. Default proposal: `IsServiceEnabled` READ first, and owe the disable only if we enabled it. `GetScreenCapture` faults with IllegalOperation while the service is disabled.
4. **Step 3: the development CA.** HP: "The use of self-signed certificates with the OXPd CA Certificate store is not recommended/supported". A development root CA is self-signed by construction. Whether HP's sentence targets self-signed server certificates (the IIS7 example) or any self-signed root is NOT settled by the text. It is a question for the step-3 kit, or for HP, and is not decided here.
5. All write and read operations above need the admin credential (401/403). L5's one-attempt password guard applies unchanged.

## 5. Licence and redistribution text found (QUOTED, REPORTED, NOT DECIDED)

The ruling on use: Kam's 17:56 note, recorded as **C-74** in the project's `CLARIFICATIONS.md` (line 758): "our license / commercial agreement allows us to use HP code as part of our code." The C-74 entry also cites C-11 and C-58 paragraph 10.

Text found:
- **The WSDL/XSD files themselves:** `grep -i -E "copyright|licen[cs]e|redistribut|confidential|proprietary"` over the jar's `META-INF/wsdls/` (100 files) found only 3 unrelated lines: an enumeration `Confidential` (a stamp option) and "may provide customer confidential data" in `statistics.wsdl`. There is **no copyright or licence header** in any description file. The jar's `META-INF/MANIFEST.MF`: 0 hits for licen/copyright/vendor. The jar holds no LICENSE or NOTICE entry.
- **Library README** (`/Volumes/DEV-Working/Datasec/Friday/2026-11-19_oxpd-friday-work-and-library/OXPd/README.md` line 3, Friday's summary, not HP's text): "HP material — partner/beta licence terms apply; beta firmware/SDKs must not be redistributed to customers." SDK 1.8.4.1 is not labelled beta in its folder name, `Manifest.txt` or `Revision.txt` (grep "beta": 0). The `OXPd1.7.3.2ProfessionalOnlybeta` package is labelled beta, and this proposal uses nothing from it.
- **HP spec "Legal Notices"**, for example `OXPd1-NET-Java/Docs/oxpd-accessories-service-specification.md` lines 258 to 260: "This document contains proprietary information that is protected by copyright. All rights are reserved. No part of this documentation may be transformed, reproduced, or translated to another language without prior." `Knowledge-Base/Certificate-Management--115009494648-OXPd-CertificateManagement-Fleet-Specification.md` line 261 has the same text, ending "without prior consent." "© Copyright 2015 HP Development Company, L.P." The same paragraph is in 10 files under `OXPd1-NET-Java/` (Knowledge-Base fleet specs and the SDK user guide). The three markdown specs for the step-2/3/4 services (`oxpd-test-...`, `oxpd-certificate-management-...`, `oxpd-browser-use-model-and-ui-configuration-...`) hold 0 copyright/licence lines.
- `OXPd2/SDK/OXPd2-SDK-Beta-10/LICENSE.txt` (1,376 lines) is third-party npm notices (Apache 2.0 for `indefinite-observable@2.0.1`, and so on). It does not bear on OXPd 1.x.
- `HPAM/Help-Portal/.../EULA.*` is the HPAM product's end-user licence and does not bear on the SDK.

**What may seem to conflict (reported, never decided):** the WSDL files carry HP's `<wsdl:documentation>` prose (the very sentences quoted in section 2). HP's spec Legal Notice says "No part of this documentation may be ... reproduced ... without prior consent". Committing the WSDL files reproduces that prose in a private repository. C-74 says HP code may be used as part of our code, and 14 such files are already committed at main under the same pattern. Whether C-74 also covers HP's embedded documentation prose is Kam's to say if Tuesday thinks it needs saying. This drafter does not rule on it.

## 6. Proposed CONTRACTS lane (Tuesday's to commission; defaults are this drafter's)

- **What:** commit 9 files byte for byte from the pinned jar (`f2bb325f...`), at the jar's own folder names, under `contracts/oxpd1/hp/`:

```
ebc2ef86afe137577aeef308b243e47a698fc4a2a11513098bbf825a68a3947a  hp/http__www.hp.com_schemas_imaging_OXPd_service_test_2010_04_14/TestSoap12Binding.wsdl
2b0af19d05850ef155e6c8ca2272457771f346e715c37756b49ab9dcc947f177  hp/http__www.hp.com_schemas_imaging_OXPd_service_test_2010_04_14/test.wsdl
f3c88dbf639b5f5ea06d103c9c60a347dd07984efa4a87e45c1fd197d283bfe2  hp/http__www.hp.com_schemas_imaging_OXPd_service_test_2010_04_14/test.xsd
8a04ab7403a75aed164a1f38a44ed10c2697bdf03cf32a526b5f51b2d544cf31  hp/http__www.hp.com_schemas_imaging_OXPd_service_certificatemanagement_2010_04_14/CertificateManagementSoap12Binding.wsdl
2a4f37ec940af0d291693f1f33be58fb7a55ed3f9813a729790b6820d9836b61  hp/http__www.hp.com_schemas_imaging_OXPd_service_certificatemanagement_2010_04_14/certificatemanagement.wsdl
e52fd5bd6da13b10bb77ed265bd2e292713a70f9ff731243729aded15e26fd0d  hp/http__www.hp.com_schemas_imaging_OXPd_service_certificatemanagement_2010_04_14/certificatemanagement.xsd
1e0d17b9f3f7279e2e7903772662717c5a42f68a16fa10c11670521f954d06c5  hp/http__www.hp.com_schemas_imaging_OXPd_service_uiconfiguration_2010_04_14/UIConfigurationSoap12Binding.wsdl
cd0467900521b7be0f65bf5ee7443385f73dd36f416e8c0bc5b4f5d33ef618ab  hp/http__www.hp.com_schemas_imaging_OXPd_service_uiconfiguration_2010_04_14/uiconfiguration.wsdl
ebb28d8b58873c8c298052240387895401bb525b3e3d8071e51f5afc25478a77  hp/http__www.hp.com_schemas_imaging_OXPd_service_uiconfiguration_2010_04_14/uiconfiguration.xsd
```

  Import closure, measured from every `wsdl:import`/`xs:import`/`xsd:import` in the three folders: each binding imports its port-type file. Each port-type file imports its schema and `../http__www.hp.com_schemas_imaging_OXPd_common_2010_04_14/common.xsd`. The jar's `common.xsd` hashes to `e373777e...102b`, the committed value, so it needs no change. `TestSoap12Binding.wsdl` does not import `testCallback.wsdl`; only `TestCallbackSoap12Binding.wsdl` does. Leave the callback pair out: the device calls it, so we would serve it, and step 2 does not need it.
- **Also:** append the 9 lines to `contracts/oxpd1/inputs.sha256`. Update `contracts/oxpd1/README.md`: "14 files" becomes 23, "the four bindings ... (DeviceInfo, Authentication, Accessories, Authorization)" becomes seven, and the same jar pin stays. `.gitattributes` already marks every file `-text`, so no change there.
- **Owned paths:** `contracts/oxpd1/hp/**` (9 new files only), `contracts/oxpd1/inputs.sha256`, `contracts/oxpd1/README.md`. Possibly `tests/Datasec.Suite.Adapters.Oxpd1.Tests/ContractTests.cs`, **UNMEASURED**: this drafter did not read whether a contract cell pins the file count at 14 or hashes the folder against `inputs.sha256`. The kit drafter must read `ContractTests.cs` and `Repo.Contracts` at BASE and STOP if a cell needs changing outside the owned paths. No `src/`, no `slnx`, no package, no lock file.
- **Partition:** it touches `contracts/**`, which B2010 and B2011 are forbidden to touch, so there is no clash with tonight's lanes. It must not run in parallel with any other lane that owns `contracts/oxpd1/**`.
- **Gate tier (proposal):** the lightest tier the project has for a data-only change. Checks: hash conservation (the 14 old lines unchanged; the 9 new ones re-hashed by the gate from the pinned jar), the four hosted checks green, and gitleaks clean. If the project's ladder has no tier below G1, then G1. That is Tuesday's choice.
- **Then:** one write lane per step (2, 3, 4), each a pair with its undo, each with the READ-before-write of section 4. The Test-service lane also carries `GetScreenCapture` as a read.

## 7. Search record

- Folders searched: the whole library `/Volumes/DEV-Working/Datasec/Friday/2026-11-19_oxpd-friday-work-and-library/OXPd/`, 31,481 files.
  - `find -iname "*.wsdl" -o -iname "*.xsd"` found loose descriptions only in Demos, Tools (oxpm 1.7.0.0, Jedi profiler) and `OXPdUI/SIPS`. None of them is a step-2/3/4 service.
  - Then `OXPd1-NET-Java/SDK/` (all four packages), the 1.8.4.1 jar's `META-INF/wsdls/` (100 description files), `OXPdLib/DotNet/` of 1.8.4.1, and `OXPd1-NET-Java/Docs/`.
  - Licence search: `-iname "*licen*|*eula*|*copying*|*notice*|*terms*"` over the library; content grep `redistribut|licen[cs]e agreement|confidential|proprietary|developer agreement|terms of use` over `OXPd1-NET-Java/Docs`, `OXPd1-NET-Java/SDK`, the three top-level READMEs, `General/Portal-Pages` and `General/Partner-Resources`.
- Terms: the operation names in section 3; `service_test`, `certificatemanagement`, `uiconfiguration` (folder names); `MinorRevision`; `M577`.
- Nothing was written on the NAS. No secret was opened. No device or host was contacted except GitHub GETs.
