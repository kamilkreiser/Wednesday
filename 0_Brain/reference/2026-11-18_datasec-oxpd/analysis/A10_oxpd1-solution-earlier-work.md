# A10: the earlier OXPd 1 solution as sent on 2026-11-20 (`OXPd1_solution-master`)

Lane O of commission B1763, 2026-11-20. Read-only: nothing in the source tree was built or run, nothing was written outside this file, no network call was made.

STATUS OF THIS FILE: written in sections as the work went. A section that is missing below was not finished; the last section says what was not read.

Path shorthand (all relative to the extracted root `2_Project_Files/fleet/state/kam_attachments_1120b/extracted/`):

- `OX/` = `OXPd1_solution-master/OXPd1_solution-master/`
- `S/` = `OX/server/src/com/hp/authenticationsuiteoxpd/server/`
- `C/` = `OX/client/src/com/hp/authenticationsuiteoxpd/authagent/`
- `W/` = `OX/server/web/`
- Project documents are named by file (`02`, `03`, `05`, `A7`, `C1`, `C2`) with their own line numbers.

## 1. BLUF

1. **This is not new material. The archive sent at 11:50 is byte-for-byte the tree that report A7 already analysed on 2026-11-18.** `diff -rq` between the delivered tree and each of three copies already on this machine printed nothing and returned 0 (section 2). The commission's statement that "none of the twelve analysis reports, the architecture or the plan has seen" it is wrong: A7 (`analysis/A7_old-oxpd1-attempt.md`, 477 lines) is a report on exactly these 73 files, and `02` and `03` cite A7.
2. **What it is**: a Java 21 proof of concept of an OXPd 1.x server (12 server classes, 2 command-line registration tools, 6 HTML pages, 27 jars). It registers an Authentication Agent, six USB card readers and a home-screen button, and signs a user in with the Entra device code flow shown as a QR code. It does not talk to the HPAM back end at all (section 4).
3. **The "install logs" are not a record of the solution running on a printer.** They are the transcript of installing a developer tool (Claude Code 2.1.92) on a Windows ARM64 laptop on 2026-04-06. They record no printer, no registration and no sign-in (section 5).
4. **What this lane adds to A7**: the byte identity; a jar-by-jar library and licence table that A7 did not make (A7 left all 27 jars unopened); a check of A7's main claims against the delivered copy; the comparison with `02`, `03` and `05` as they stand today; proposed corrections.
5. **It answers no open question.** It is not the "OXPD1" repository (that one is empty, per C-40), it holds no printer evidence, and the questions A7 raised about it (was it ever run on hardware, is there a history, is the author available) are still open.

## 2. Identity of the delivery (measured)

| # | Fact | How measured |
|---|---|---|
| 2.1 | The archive `f-ed2f82f4f1fc_OXPd1_solution-master.zip` lists 192 entries: 73 real files, 96 `__MACOSX` resource-fork files, the rest directories. The commission's "169 files" is 73 + 96 | `unzip -Z1 … \| grep -v ^__MACOSX \| grep -v /$ \| wc -l` printed 73; `find …/__MACOSX -type f \| wc -l` printed 96 |
| 2.2 | The extracted real tree holds 73 files in 23 directories | `find OX -type f \| wc -l`, `find OX -type d \| wc -l` |
| 2.3 | Identical to `/Volumes/DEV-Working/Datasec/Friday/2026-11-19_oxpd-friday-work-and-library/OXPd/OLD BUILD/OXPd1_solution-master` (the copy A7 names as the one it read, `A7:5-10, 31`) | `diff -rq -x .DS_Store <that> OX`: no output, exit 0; 73 files there |
| 2.4 | Identical to `…/OXPd/HPAM - Docs and Notes/Source Code/OXPd1_solution-master` (the second copy A7 mentions, `A7:31`) | same command: no output, exit 0; 73 files |
| 2.5 | Identical to `/Volumes/Datasec_DEV/!CODING/Datasec/Security Review/Source_Code/OXPd1_solution-master` (a fourth copy, in another Datasec project; read only for this comparison) | same command: no output, exit 0; 73 files |
| 2.6 | Positive control for the comparison | `diff -rq OX/client OX/server` printed 5 difference lines, so the command does report differences when there are some |
| 2.7 | Digest of the delivered tree, for any later comparison: SHA-256 over the sorted list of per-file SHA-256 values and relative paths is `8f22d29e…478e2b` (full value: `8f22d29e5a3193bd116e32a182e1d50d9cfa64424ffa0e172fbc256264478e2b`) | `find OX -type f -exec shasum -a 256 {} + \| sed <strip root> \| sort -k2 \| shasum -a 256` |
| 2.8 | No `.git` folder: no history, no author, no dates beyond file times (all 30 June) and the installer log (6 April 2026) | `ls -la OX` |
| 2.9 | Line counts of the 12 server classes equal those in A7's table (`A7:59-72`): 703, 554, 425, 916, 595, 443, 804, 474, 223, 138, 59, 52 | `wc -l S/*.java` |

Consequence: every finding of A7 applies to this delivery unchanged, with `OB/` read as `OX/`. Sections 3 to 5 below re-check A7's main claims against the delivered copy and add what A7 did not cover; they do not repeat A7 in full.

## 3. Coverage of this pass

| Class | Count | Detail |
|---|---|---|
| Files in the delivered tree | 73 | `find OX -type f \| wc -l` |
| Read whole in this pass | 15 | `README.md`, `INSTALLATION.md`, `todo.txt`, `.gitignore`, `gitleaks.yml`, `build.sh`, `register.sh`, `unregister.sh`, `run-server.sh`, `start-prompt-server.sh`, `register.bat`, `claude-install.ps1`, both install logs, `S/PrinterManager.java` |
| Read in part, at the lines A7 cites | 7 | `S/MicrosoftAuthService.java` (1-12, 174-200, 318-348, 418-432), `S/AuthenticationStateMachine.java` (420-460), `S/CombinedServer.java` (86-100, 287-311), `S/CardReaderAuthenticationAgentService.java` (227-258, 404-424), `S/CardReaderAccessoriesCallbackHandler.java` (40-46, 282-330), `C/RegisterCardReaderSolution.java` (176-196), `W/onedrive.html` (674-679) |
| Searched by program, not read | all 39 text files | symbol counts, URL hosts, secret-keyword line numbers (sections 4, 7) |
| Jars: manifest and entry names only | 27 | section 6; nothing extracted to disk, nothing decompiled |
| Not opened | 6 | 3 compiled `.class` files (only bytes 4-7, the class-file version, were read: `00000041`, Java 21), 3 copies of one PNG (4,678 bytes each) |
| Compared whole by `diff`, not re-read line by line | 73 | section 2: because the tree is byte-identical to the one A7 read, A7's reading of the files this pass did not re-open stands as A7 wrote it, unverified by this pass |

All text was displayed through a masking filter (long tokens, GUID tails and values beside secret keywords replaced by a length). One value slipped through before the filter was tightened: see section 7.

## 4. What it is and how far it got (inventory)

Every row was checked in the delivered copy in this pass unless marked "(A7, not re-opened)".

### 4.1 Architecture, language, build

| # | Fact | Source |
|---|---|---|
| 1 | One Java process. `CombinedServer` publishes two JAX-WS SOAP endpoints with `Endpoint.publish` and runs a hand-written HTTP server on a raw `ServerSocket` | `S/CombinedServer.java:98, 154, 238` |
| 2 | A second raw-socket HTTP server is the admin API | `S/AdminServer.java:68` |
| 3 | `client` is two command-line tools, register and unregister; `server` is 12 classes, 3 handler XML files and 6 HTML pages; `lib` is 27 jars and nothing else | `find OX/lib -type f -not -name "*.jar" \| wc -l` printed 0; file list in section 2 |
| 4 | Java 21, compiled by `javac -source 21 -target 21` against every jar in `lib/`; no Maven, Gradle or Ant file | `OX/build.sh:57-59, 64-66`; `OX/build.sh:34` |
| 5 | The JDK path is fixed to one Homebrew path on macOS and to `C:\Program Files\Java\jdk-21.0.2` on Windows | `OX/build.sh:14`, `OX/register.bat:4` |
| 6 | The committed client classes were compiled for Java 21 (class-file major version 0x41 = 65) | bytes 4-7 of each of the 3 files in `OX/client/bin/com/hp/authenticationsuiteoxpd/authagent/` |
| 7 | No compiled server, no `server.log`, no `data/` folder, no database file is in the tree | `find` for `server.log`, a `data` directory, `server/bin`, `*.db`: 0 each; control: `client/bin` found (1) |
| 8 | No test of any kind | grep `junit\|@Test` over `OX/server` and `OX/client/src`: 0 files; control `card` (whole word): 114 lines |

### 4.2 Which OXPd 1.x services it uses

Counted by program over `OX/server` and `OX/client/src` (case-insensitive). The same run found the used services, which is the positive control for the zeros.

| # | OXPd 1.x service | Used? | Calls and where |
|---|---|---|---|
| 9 | Service discovery | Yes | `DiscoveryTreeTranslator.GetOXPdDiscoveryTree` before every device call: `S/PrinterManager.java:45, 72, 204, 255, 310`; `C/RegisterCardReaderSolution.java:76` |
| 10 | Authentication (device side) | Yes | `GetAuthenticationAgentRecords`, `UnregisterAuthenticationAgent`, `GetSupportedAgentBindings`, `RegisterAuthenticationAgent`, `GetAuthenticationAgentRecord`: `S/PrinterManager.java:91, 94, 102, 120, 123`; `ReserveAuthenticationContext`: `S/AuthenticationStateMachine.java:341`; `ReleaseAuthenticationContext`: `S/CardReaderAuthenticationAgentService.java:160, 370` |
| 11 | Authentication Agent (server side, called by the device) | Yes | class implements `IAuthenticationAgentService`: `S/CardReaderAuthenticationAgentService.java:37`; pre-prompt always `CONTINUED` `:253`; post-prompt `SUCCEEDED` `:338` or `FAILED` `:350` |
| 12 | Accessories (card readers) | Yes | `RegisterOwnedAccessory` six times: `S/PrinterManager.java:134-143`; callback class implements `IAccessoriesServiceCallback`: `S/CardReaderAccessoriesCallbackHandler.java:38`; `HidOpen` `:302`, `HidStartReading` `:321` |
| 13 | UIConfiguration | Yes | `GetTopLevelButtonRecords`, `UnregisterTopLevelButton`, `GetUIProfile`, `RegisterTopLevelButton`: `S/PrinterManager.java:155, 160, 173, 192`; `EndUserSession`, `ReleaseUIContext`: `S/AuthenticationStateMachine.java:245, 250` |
| 14 | DeviceInfo | Written, dead | `GetManufacturerInfo` in one method: `S/CombinedServer.java:681-689`; A7 lists it as dead code (`A7:356`) (A7, not re-opened for callers) |
| 15 | Scan | **No** | `ScanProxy\|IScanProxy\|StartScanJob`: 0 files |
| 16 | Copy | **No** | `CopyProxy`: 0 files |
| 17 | Print (IPP extensions) | **No** | `IppProxy`: 0 files |
| 18 | Statistics, Statistics agent | **No** | `StatisticsProxy\|IStatisticsProxy`: 0 files |
| 19 | Authorization, Quota, CertificateManagement, SendFax | **No** | `AuthorizationProxy`, `QuotaProxy`, `CertificateManagementProxy`, `SendFaxProxy`: 0 files each |
| 20 | Accessory removal | **No** | `UnregisterOwnedAccessory`: 0 files; control `RegisterOwnedAccessory`: 2 files. The six reader records stay on the device after uninstall |
| 21 | Reader stop or close | **No** | `HidStopReading\|HidClose`: 0 files |
| 22 | `CONTEXT_RESENT` accessory event | **No** | 0 files |

So of the seven service areas the commission names, the build exercises three (authentication agent, UI, accessories and card readers). It has no device-management, scan, print or statistics code.

### 4.3 How it registers with a printer

| # | Fact | Source |
|---|---|---|
| 23 | Two code paths do the same registration with their own copies of the constants: the command-line client and the server's `PrinterManager`, driven from the admin page | `C/RegisterCardReaderSolution.java:113-359`; `S/PrinterManager.java:63-80` |
| 24 | Scripts: `register.sh <PRINTER_HOST> <SERVER_HOST> [PRINTER_PASSWORD]` runs `RegisterCardReaderSolution`; `unregister.sh <PRINTER_HOST> [PRINTER_PASSWORD]` runs `UnregisterCardReaderSolution`. Both only set the classpath and start Java. The password argument falls back to a generic default | `OX/register.sh:2, 11-13, 49-51`; `OX/unregister.sh:2, 11-12, 47-49`; `OX/register.bat:22, 44` |
| 25 | Order of calls: accept-all certificate mode on, discovery tree, agent, six readers, home-screen button | `S/PrinterManager.java:65, 72, 75-77` |
| 26 | Agent record: one fixed id (the widely published example UUID that begins `550e8400`, the same on every device), name "HP Authentication Manager OXPd", `en-US` only, pre-prompt check `true`, sign-out notification **`false`**, retries 2 and 4, a random `serverContextId` | `S/PrinterManager.java:24-25, 109-119`; `C/RegisterCardReaderSolution.java:181-193` |
| 27 | Every URL written into the device is plain `http://` with the server's IP address: agent on 8091, accessories callback on 8092, prompt page on 8080 | `S/PrinterManager.java:67-69` |
| 28 | Reader records: vendor id, product id, serial number `null`, SOAP 1.2 callback, timeouts 60 and 3. The six id pairs are 3111:15354, 1008:69, 2520:1040, 2520:784, 1899:21544, 7590:272 | `S/PrinterManager.java:29-36, 134-143`; same list `OX/README.md:23-28` |
| 29 | Existing records are found and replaced by display name, not by id | `S/PrinterManager.java:91-97, 155-166` |
| 30 | "Installed" is decided by whether the agent record can be read, and "not installed" by matching words in an exception message | `S/PrinterManager.java:43-59` |
| 31 | The device administrator password is the only credential used toward the device | `S/PrinterManager.java:47, 86, 132, 151` |
| 32 | Uninstall removes the agent and the button, not the readers (row 20) and not the OneDrive button | `S/PrinterManager.java:305-353` |

### 4.4 How sign-in works in it

| # | Method | State | Source |
|---|---|---|---|
| 33 | **Card** | A card read is only a trigger. The decoded string is stored on the session and then the device code flow starts; nothing looks the card up | `S/AuthenticationStateMachine.java:420-459`, comment at `:430` |
| 34 | Card to user lookup in Custom Security Attributes | Written, **never called**: the method name occurs once in the tree (its own definition). Control: `requestDeviceCode` occurs in 2 files | `S/MicrosoftAuthService.java:177-204`; grep `resolveLoginHintFromCard` |
| 35 | **Microsoft** | Entra **device code** flow: `POST /{tenant}/oauth2/v2.0/devicecode`, scope `openid profile offline_access`, client secret sent when configured; shown as a QR code the user scans with a phone | `S/MicrosoftAuthService.java:422-429`; `devicecode`: 83 lines in 3 files |
| 36 | Auth code + PKCE on the panel | Helpers written, unused; the file header still calls the file "authorization-code + PKCE flow" | `S/MicrosoftAuthService.java:3`; `code_challenge\|code_verifier`: 3 lines in 1 file |
| 37 | **PIN** | **None.** The whole word "pin" does not occur in `OX/server`, `OX/client/src`, `OX/todo.txt` or `OX/README.md` | `grep -r -i -w -c pin`: 0; control `card`: 114 |
| 38 | **Phone** (the HP Secure Authentication app through SignalR) | **None.** SignalR appears only as a settings field and in the author's brief | `signalr`: 6 lines in 3 files: `OX/todo.txt:6`, `W/admin.html:401-402, 1017, 1044`, `S/AdminServer.java:439` |
| 39 | Passkey, FIDO | **None** | `passkey`: 0 files; `fido`: 0 files |
| 40 | Session identity | The printer's TCP source address plus `_session`; the context ids the device sends are logged and not used as keys | `S/CombinedServer.java:303-305`; `S/CardReaderAuthenticationAgentService.java:235-237` |
| 41 | Identity returned to the device | `AuthenticationType.OTHER`; fully qualified name and UPN from the token; user name and display name from the configured console-name rule; e-mail | `S/CardReaderAuthenticationAgentService.java:404-424` |
| 42 | Starting sign-in on an idle device | The server calls `ReserveAuthenticationContext` with the agent id, with no administrator password | `S/AuthenticationStateMachine.java:336-341` |
| 43 | Card reader start | On each reader event the server calls `HidOpen` then `HidStartReading`; the callback address defaults to `127.0.0.1` unless a property or environment variable sets it, and no script sets it | `S/CardReaderAccessoriesCallbackHandler.java:44, 93-95, 299-321` |

### 4.5 What it talks to

Every distinct `http(s)` host named in the 39 text files outside `lib/`, by program:

| # | Host | Count | First place | Meaning |
|---|---|---|---|---|
| 44 | `login.microsoftonline.com` | 5 | `S/MicrosoftAuthService.java:89` | Entra token and device code endpoints |
| 45 | `graph.microsoft.com` | 4 | `S/MicrosoftAuthService.java:195` | CSA query (dead) and the OneDrive proxy |
| 46 | `microsoft.com` | 1 | `S/MicrosoftAuthService.java:451` | the device-login address shown to the user |
| 47 | `license.hpauthsuite.com` | 2 | `W/admin.html:462, 1020` | a placeholder and default text in a settings field; nothing calls it |
| 48 | `cdn.tailwindcss.com`, `fonts.googleapis.com` | 1 each | `W/admin.html:7, 9` | the admin page loads scripts and fonts from the public internet |
| 49 | `localhost`, `127.0.0.1`, `0.0.0.0`, `192.168.1.100`, `your-server…` | | `W/admin.html:585`, `S/MicrosoftAuthService.java:37`, `OX/INSTALLATION.md:92` | local addresses and documentation examples |
| 50 | `storage.googleapis.com` | 1 | `OX/claude-install.ps1:32` | the unrelated tool installer (section 5) |

**It does not talk to the HPAM back end.** Counts over the same files: `azurewebsites` 0, `hpam-api` 0, `cc-api` 0, `negotiate` 0. Positive controls from the same run: `graph.microsoft.com` 4 lines in 2 files, `login.microsoftonline.com` 5 lines in 1 file. There is no call to a Function App, to SignalR, to the licence service or to Log Analytics. The licence, SignalR, MFA and reporting items exist only as names of stored settings (`S/AdminServer.java:439-440`).

### 4.6 Finished, stubbed, listed in `todo.txt`

`todo.txt` is not a task list. It is the author's 22-line brief to a coding assistant: what the Workpath suite is (`OX/todo.txt:2-12`), the instruction "This must be ported to the older. OXPd platform" (`:15`), how OXPd devices work (`:17`), "There is already basic implementation of the server in solution folder. There are scripts to install and uninstall solution on MFP" (`:20`), and "Also emulator is running on this windows machine so I could check the server behavior" (`:22`).

| # | Item of that brief | State in the code | Evidence |
|---|---|---|---|
| 51 | Authentication agent on the device | Written | rows 10, 11 |
| 52 | Listens to the card reader | Written, as a trigger only, one generic keyboard parser | rows 12, 33 |
| 53 | Card to user e-mail in Custom Security Attributes | Read path written and never called; no write path (no enrolment) | row 34 |
| 54 | Sign-in against Microsoft, token handed to the other apps | Device code only; the token stays in the server's memory under the printer's IP | rows 35, 40 |
| 55 | SignalR socket for the phone app's QR | Absent | row 38 |
| 56 | Mailflow, Teams, SharePoint | Absent: no file | file list, section 2 |
| 57 | OneDrive | Browse and preview page written; **print is a placeholder** (`alert('Print coming in next version.')`); no scan | `W/onedrive.html:676-678` |
| 58 | Universal Print (three virtual printers) | Absent | file list; row 17 |
| 59 | Scan and print through SOAP | Absent | rows 15, 17 |
| 60 | Shared look (the common library) | Absent | (A7, not re-opened) `A7:299` |

Stale documents inside the tree: `README.md` describes an older stage where any card is authorised and the card string becomes the user name (`OX/README.md:16-18, 97, 132`) and names a package path that does not exist (`:79, 117-123`); `INSTALLATION.md` describes a `RegistrationClient.java` with four arguments and an Ant build, neither of which exists in source (`OX/INSTALLATION.md:34, 73-79, 105-135`); `build.sh:71` advertises arguments that `run-server.sh` does not take (`OX/run-server.sh:42-45`).

## 5. What the install logs record

The commission treats the two logs as evidence of a real run of the solution. They are not.

| # | Fact | Source |
|---|---|---|
| 61 | `claude-install.ps1` is the Windows installer script of a developer tool (Claude Code): it resolves the latest version, downloads a binary, checks its SHA-256 and runs its installer. It contains nothing about OXPd, printers or this solution | `OX/claude-install.ps1:24-105` |
| 62 | `claude-install.log` is the PowerShell transcript of one run of that script: started 2026-04-06 15:22:01, finished 15:22:52, version 2.1.92, platform `win32-arm64`, result "successfully installed" | `OX/claude-install.log:3, 20, 27-28, 44-46, 74, 78` |
| 63 | `claude-install-console.log` is the console copy of the same run (UTF-16), same times and result | `OX/claude-install-console.log:2, 9-10, 26-28, 57` |
| 64 | Machine: Windows NT 10.0.26200, PowerShell 5.1, ARM64. The transcript header holds a Windows user name and a machine name (a real person's name: location only) | `OX/claude-install.log:4-7`; `OX/claude-install-console.log:4` |
| 65 | Working folder at the time: a path ending `\datasec\oxpd\solution\` on drive `E:` of that machine | `OX/claude-install.log:19` |
| 66 | Printer, firmware, registration, sign-in, card read: **none recorded.** Model and firmware words (`futuresmart`, `laserjet`, `pagewide`, `firmware`, `jedi`, a model number pattern) occur 0 times in the 39 text files; control `printer`: 451 lines | grep counts, this pass |
| 67 | `.gitignore` lists both logs and `*.log`, yet both are in the archive: they were committed before the rule or added by force | `OX/.gitignore:9, 25-26` |
| 68 | The only statement about where the solution ran is the author's: an emulator on "this windows machine" | `OX/todo.txt:22` |
| 69 | `README.md` tells the reader the printer is at a private lab address and gives a "default" administrator password for it (value not repeated here). Whether that address was a printer or the emulator is not stated anywhere | `OX/README.md:34, 72, 80-81` |

What the logs do establish: the working period (April 2026), that the work was done on a Windows ARM64 laptop, and that the code was written with a coding assistant. An ARM64 Windows machine is worth one line to the product owner: HP's OXPd 1.x simulator needs Windows with IIS (`C1:340`), and whether "emulator" at `todo.txt:22` means that simulator, and on what machine it ran, is not in the tree.

## 6. Libraries bundled under `lib` (A7 left all 27 jars unopened)

Method: for each jar, `unzip -Z1` (entry names), `unzip -p … META-INF/MANIFEST.MF` (manifest), `shasum -a 256`. Nothing was extracted to disk and no class was decompiled. 27 jars, 22,953,421 bytes in total, no other file in `lib/`, and no licence file anywhere in the tree outside the jars (`find OX -iname "*licen*"`: 0; control `*readme*`: 1).

### 6.1 The HP library

| # | Fact | How measured |
|---|---|---|
| L1 | `OX/lib/OXPdLib-1.8.4.jar`, 1,611,836 bytes, 1,057 entries, every entry dated 2024-05-01. SHA-256 `debf18cd…19fe8a` | `unzip -Z1 \| wc -l`; `unzip -l` date column; `shasum` |
| L2 | It is the **unchanged jar of HP's SDK 1.8.4**: same SHA-256 as `OXPd1-NET-Java/SDK/hp-ext-XX-oxpd-1.8.4/OXPdLib/Java/lib/OXPdLib-1.8.4.jar` in the library copy on this machine | `shasum` of both: equal |
| L3 | It is **not** the jar of SDK 1.8.4.1, the version the architecture builds on. That jar has the same file name and a different hash (`f2bb325f…c3d341`) | `shasum` of `…/hp-ext-XX-oxpd-1.8.4.1/OXPdLib/Java/lib/OXPdLib-1.8.4.jar` |
| L4 | The jar is **signed**: `META-INF/JARSIGNK.SF` and `META-INF/JARSIGNK.RSA`, with 990 per-entry SHA-256 digests in the manifest. A modified copy would fail signature verification, which is a practical check on the "unchanged" condition | `unzip -Z1 \| grep ^META-INF/ \| grep -v wsdls`; `grep -c SHA-256-Digest` on the manifest |
| L5 | The manifest states no name, vendor, version or licence (its main section is `Manifest-Version: 1.0` only) | first lines of the manifest |
| L6 | **No licence, notice or copyright file is inside the jar.** Entry names matching `licen\|notice\|eula\|copyright`: 0. Control: entries matching `wsdl`: 173 | `unzip -Z1 \| grep -i -c` |
| L7 | Content: 843 classes (752 under `com/hp/www/schemas/…`, 91 under `com/hp/www/oxpd/helpers`), 64 WSDL and 36 XSD files, 17 binding files. It also carries 4 development leftovers: one `.classpath`, one `.project`, one `.properties`, one `.xpr` | extension histogram of the entry names |
| L8 | Service packages in the jar (class counts): accessories 59, authentication 18, authenticationagent 15, authorization 19, authorizationagent 12, certificatemanagement 17, copy 43, deviceinfo 10, quota 9, quotaagent 31, scan 136, sendfax 43, statistics 23, statisticsagent 10, test 43, uiconfiguration 70 | package histogram |
| L9 | There is no print service package. Print is through the IPP helper classes (`IppProxy`, `IppRequest`, …) and an undocumented `pushprintcontrol` pair that exists as WSDL and XSD (entries naming `print`: 19; control `scan`: 160). This agrees with `C1:366` | `unzip -Z1 \| grep -i -c print` |
| L10 | The accept-all certificate helper the build calls ten times lives in this jar: `NaiveTrustProvider`, `NaiveTrustManager` | helper class list; grep `NaiveTrustProvider`: 10 lines in 5 files |

Bearing on C-11 and the Q20 ruling. C-11 is the tap "As assumed" on card q20; the assumption as the plan records it is "Reimplement logic; redistribute OXPdLib 1.x unchanged; OXPd2Lib only after production SDK" (`03:318`). The terms themselves are in HP's SDK user guide as report C1 read it: licensed SDK users may distribute the pre-built libraries unchanged as part of a solution, and may not distribute the source or a modified library (`C1:316`, `C1:485`). Against that:

- The earlier build is consistent with the ruling as far as the jar goes: it carries the pre-built library, unmodified (L2, L4), and no HP library source.
- The terms are not in the jar and not in this repository (L5, L6). Whoever ships the library must take the terms from the SDK guide; nothing in the artefact carries them.
- The jar is committed to a source repository. `.gitignore` has a heading for third-party jars with **no pattern under it** (`OX/.gitignore:11-12`), so all 27 jars are in git. Whether keeping HP's library in a GitHub repository counts as "distribution as part of a solution" is a question for HP's terms, not for this tree (not established here).
- A product build must use the 1.8.4.1 jar and identify it by hash, since the file name is the same (L3; `C1:498` says the same).
- All of this matters only if the Java sidecar fallback is taken. The chosen stack is .NET (`02:815`), which uses HP's .NET library, not this jar.

### 6.2 Third-party libraries (all open source; licences as each jar's own manifest declares)

| # | Jar | Version (manifest) | Declared licence (`Bundle-License`) | Licence file inside |
|---|---|---|---|---|
| L11 | `jaxws-rt-4.0.3.jar` | 4.0.3, Eclipse Foundation | EDL 1.0 | `META-INF/LICENSE.md`, `NOTICE.md` |
| L12 | `jakarta.xml.ws-api-4.0.2.jar` | 4.0.2 | EDL 1.0 | yes |
| L13 | `jakarta.xml.bind-api-4.0.2.jar` | 4.0.2 | EDL 1.0 | yes |
| L14 | `jakarta.xml.soap-api-3.0.2.jar` | 3.0.2 | EDL 1.0 | yes |
| L15 | `jakarta.activation-api-2.1.3.jar` | 2.1.3 | EDL 1.0 | yes |
| L16 | `jakarta.annotation-api-2.1.1.jar` | 2.1.1 | EPL 2.0, with a second (GNU) licence URL the manifest line truncates | yes |
| L17 | `jaxb-core-4.0.5.jar`, `jaxb-runtime-4.0.5.jar`, `txw2-4.0.5.jar` | 4.0.5 | EDL 1.0 (`txw2` states none in the lines read) | yes |
| L18 | `saaj-impl-3.0.4.jar` | 3.0.4 | EDL 1.0 | yes |
| L19 | `angus-activation-2.0.2.jar` | 2.0.2 | EDL 1.0 | yes |
| L20 | `istack-commons-runtime-4.1.2.jar` | 4.1.2 | EDL 1.0 | **none** |
| L21 | `mimepull-1.10.0.jar`, `stax-ex-2.1.0.jar`, `streambuffer-2.1.0.jar` | 1.10.0, 2.1.0, 2.1.0 | EDL 1.0 | yes |
| L22 | `gmbal-api-only.jar` | 4.0.3 | EDL 1.0 | yes |
| L23 | `management-api.jar` | 3.2.3 | EDL 1.0 | yes |
| L24 | `ha-api.jar` | 3.1.13 | EPL 2.0, with a second (GNU) licence URL the manifest line truncates | yes |
| L25 | `FastInfoset.jar` | 2.1.1 | Apache 2.0, with a second URL truncated | `META-INF/LICENSE`, `NOTICE.md` |
| L26 | `woodstox-core.jar` | 7.0.0, FasterXML | Apache 2.0 | `META-INF/LICENSE` |
| L27 | `stax2-api.jar` | 4.2.2 | BSD | `META-INF/LICENSE` |
| L28 | `slf4j-api-2.0.9.jar`, `slf4j-nop-2.0.9.jar` | 2.0.9 | MIT | `META-INF/LICENSE.txt` |
| L29 | `sqlite-jdbc-3.45.1.0.jar` (13,501,708 bytes, the largest: it carries native libraries) | 3.45.1.0 | Apache 2.0 | two licence files under `META-INF/maven/org.xerial/sqlite-jdbc/` |
| L30 | `zxing-core-3.5.3.jar`, `zxing-javase-3.5.3.jar` | 3.5.3 | Apache 2.0 (`core`; `javase` states none) | **none** |

Six jars have no version in their file name (`FastInfoset`, `gmbal-api-only`, `ha-api`, `management-api`, `stax2-api`, `woodstox-core`); the versions above are from their manifests. Licence names are read from manifest URLs; the licence texts themselves were not opened. No jar in the set declares a licence that forbids redistribution; the two EPL 2.0 jars and the dual-licensed ones would need their notices carried if a Java sidecar ever shipped (general knowledge of those licences, not from the tree).

## 7. Identity and secrets (LOCATIONS only)

No value is written in this report.

| # | Location | What |
|---|---|---|
| I1 | `S/MicrosoftAuthService.java:33` | A hardcoded key used for HMAC-SHA256 of the card string (use at `:323-329`). Literal length 20 |
| I2 | `S/MicrosoftAuthService.java:34` | A hardcoded key used for AES/ECB of the card blob (use at `:335-341`). Literal length 16 |
| I3 | `OX/README.md:81` | A printer administrator password given as the "default", beside a lab address at `:34, 72, 80`. Length 8. It occurs nowhere else in the 39 text files (searched by program without display) |
| I4 | `OX/register.sh:13`, `OX/unregister.sh:12`, `OX/register.bat:22`; and per A7 `C/RegisterCardReaderSolution.java:33`, `C/UnregisterCardReaderSolution.java:21`, `S/CardReaderAuthenticationAgentService.java:56`, `S/AdminDatabase.java:94`, `S/AdminServer.java:558-559` | A generic default device administrator password (a different literal from I3) (the Java lines: A7, not re-opened) |
| I5 | `OX/claude-install.log:4-7, 19, 22, 30, 40, 48` and repeats; `OX/claude-install-console.log:1, 4, 12, 22, 30` and repeats | A real person's Windows user name, a machine name and local paths |
| I6 | `OX/.github/workflows/gitleaks.yml:25-26` | Names of two GitHub secrets (references only, no value) |
| I7 | Run-time only, not in the tree: `data/admin.db` | Would hold the Entra client secret, printer passwords and the admin recovery code in plain text (`A7:458`). No such file is present (section 4, row 7) |

Tenant id, client id, client secret, token, certificate, private key: none found in the tree. How that was checked, by program:

- PEM blocks (`BEGIN … PRIVATE KEY` or `CERTIFICATE`): 0 lines in the 39 text files; control, lines starting `import`: 160.
- 388 lines carry a secret keyword (`passw`, `pwd`, `secret`, `token`, `bearer`, `credential`, `client id`, `tenant`, and others). On those lines, 9 quoted literals are long or mixed enough to be a value; all 9 are setting names or algorithm names (`tenantId`, `serviceEndpointClientId`, `serviceEndpointSecret`, `OXPD_PRINTER_PASSWORD`, `PBKDF2WithHmacSHA256`, `HmacSHA256`): `S/AdminDatabase.java:443, 455`, `S/AdminServer.java:438, 472, 493`, `S/AuthenticationStateMachine.java:528-529`, `S/CardReaderAuthenticationAgentService.java:222`, `S/MicrosoftAuthService.java:327`. The tenant, client id and client secret are read from the database at run time, not written in source.
- GUID-shaped literals: 5 in the 39 text files, 3 distinct: the agent id (3 places: `S/PrinterManager.java:24`, `S/AuthenticationStateMachine.java:341`, `C/RegisterCardReaderSolution.java`), an example id in `OX/INSTALLATION.md:145`, and part of a download address in `OX/claude-install.ps1:32`. None is a tenant or client id.
- Files with secret-shaped extensions (`.env`, `.pfx`, `.pem`, `.key`, keystore): none among the 73 files (file list, section 2).
- Limit of the scan: it keys on those words, so it does not flag a constant named only `…_KEY`. I1 and I2 are known from A7 and were confirmed at their lines; a third constant of that kind in a file this pass did not read would be missed by the scan, though A7, which read every source file whole, lists none.

**Two findings that are new against A7:**

1. **The two hardcoded keys (I1, I2) are not the Workpath card key.** Compared by SHA-256 of the literals, without display: both differ from the literal at `HPAuthenticationManager-main/app/src/main/java/com/hp/print/hpauthenticationmanager/util/CardValidator.kt:10` and `…/util/Encryptor.kt:12` (those two are equal to each other, length 43). A search of 4,118 text files under the library's `HPAM - Docs and Notes/Source Code/` for the two literals found them only in the library's own copy of this same file (2 hits, which is also the positive control). Limits: text files only (`.kt`, `.java`, `.xml`, `.gradle`, `.kts`, `.properties`, `.json`, `.cs`, `.ts`, `.js`, `.md`, `.txt`), build folders skipped, compiled binaries not searched; a key built at run time would not be found.
2. **The algorithm is not the Workpath algorithm either.** Here: a plain HMAC-SHA256 of the card string, base64 without padding (43 characters), used as a `startswith` prefix, and an AES/ECB blob of `card + "%%%%" + email` (`S/MicrosoftAuthService.java:323-345`). Workpath 4.4.1, as report A1 read it: a 64-character blob of which 62 characters are a nonce, an AES-GCM ciphertext and a tag (`A1:189`, `A1:200`). So A7's statements that the dead lookup "mirrors the Workpath scheme" (`A7:232`) and that the scheme is "inherited from the Workpath product" (`A7:474`) hold for the query shape only. **Even if the lookup were wired in, it could not find a card enrolled by today's Workpath app.** It may mirror an older Workpath version; the tree does not say.

A value that reached a tool output: the first display of `OX/README.md` in this pass showed line 81 in full, before the masking filter covered that pattern. The value was not copied into this report, into any file, or into the reply.

## 8. Comparison with the documents

### 8.1 Where the documents already stand on this tree

`02` cites A7 on 24 lines and `03` on 9 (`grep -i -c A7`). The tree is row P14 of the architecture: "NOT USED as code; KEPT as knowledge" (`02:47`), and the plan says "the earlier Java OXPd 1.x attempt is knowledge only, not code" (`03:21`). Nothing in the delivery changes that position.

### 8.2 Confirmed (re-checked in the delivered copy)

| # | Document statement | What the code shows |
|---|---|---|
| D1 | `02:47`: card never looked up, device-code only, session by source IP, no TLS, sign-out notification off | rows 33, 34, 35, 40, 27, 26 |
| D2 | `02:780`: the new design registers with sign-out notification ON and a `serverContextId` that carries the device record id, citing A7 | the old build passes `false` and a random id: `S/PrinterManager.java:117-118` |
| D3 | `02:798`: uninstall must remove every record, citing A7 | the old build leaves the six readers: row 20 |
| D4 | `02:821` (D9): per-reader decoders, not a generic parser | one parser for all six ids (A7 4.4, not re-opened); the six id pairs equal the six of the Workpath package as the plan lists them in hexadecimal (`03:40`): row 28 |
| D5 | `02:332`: a Java 21 sidecar on JAX-WS RI 4.0.3 is a possible fallback | `jaxws-rt-4.0.3.jar` and its 20 companion jars are present with exact versions (L11 to L27); Java 21 class files exist (row 6) |
| D6 | `03:52` (spike S2) asks whether a device can call an agent over HTTPS with a pinned device certificate | the old build never tried: every registered URL is `http://` and certificate checks are switched off (rows 25, 27, L10). The spike is still needed |
| D7 | `03:53` (spike S3) asks whether reader reports decode to the Workpath string | no reader output is recorded anywhere in the tree (row 66). The spike is still needed |
| D8 | `C1:362`: HP's Java agent example publishes with `Endpoint.publish` over plain HTTP on port 8091 | the build does the same, on the same port: `S/CombinedServer.java:89-98` |
| D9 | `C1:140`: `ReserveAuthenticationContext` starts sign-in from the server on an idle panel | used exactly so, without the administrator password: row 42 |
| D10 | `03:345`: "this is the last state" of the old build (an assumed default) | now supported for the default branch: what the product owner sent from the repository on 2026-11-20 is byte-identical to the library copy (section 2). History and other branches were not sent |

### 8.3 Contradicted

| # | Statement | What is measured | Weight |
|---|---|---|---|
| X1 | Commission B1763, "What arrived": the tree is "EARLIER OXPd 1 WORK that none of the twelve analysis reports, the architecture or the plan has seen" | It is the tree report A7 read, byte for byte (rows 2.3 to 2.5), and `02` and `03` cite A7 | High for planning: no new input arrived on the OXPd 1 side |
| X2 | Commission B1763, lane O item 1: the install logs "are evidence of a real run: on what machine and printer, with what result" | They are a transcript of installing a developer tool; no printer appears (section 5) | Medium: there is still no evidence of this code on hardware |
| X3 | `02:332`: the fallback is "JAX-WS RI 4.0.3 + OXPdLib 1.8.4.1 jar, known to work [A7 §5.1]" | The build carries the SDK **1.8.4** jar (L2, L3); A7 §5.1 itself says 1.8.4 (`A7:375`). And "known to work" rests on one sentence of the author (`OX/todo.txt:22`): no run log, no compiled server (row 7) | Low to medium: the pair that was tried is not the pair the fallback would ship |
| X4 | `02:648` (W3) cites `[A7 §8.2 item 11]` as evidence for "one global hardcoded key for card blob and QR payload"; `A7:232, 474` call the old build's card scheme the Workpath scheme | The old build's two keys are different values, of different lengths, used by a different algorithm, and occur nowhere in the Workpath sources searched (section 7) | Medium: it removes a second supposed location of the live card key; it also means the old lookup code is no model for parity |

### 8.4 Weaker than stated (not contradicted)

| # | Statement | What the tree supports |
|---|---|---|
| Y1 | `02:47`: "Spike against the simulator"; `A7:286`: "Working on the simulator" | Only `OX/todo.txt:22` says an emulator ran on the author's Windows machine. The README points at a lab address as "the printer" (`OX/README.md:34`). Which it was is not recorded |
| Y2 | `03:345`: the two keys are "treated as sensitive, covered by C-3" on A7's assumption that they are the Workpath production keys (`A7:440`) | They are not the key at the Workpath lines the documents name (section 7). Treating them as sensitive is still right; the reason changes |

### 8.5 Cheaper, reusable, or not

| Item | Class | Reason |
|---|---|---|
| Any Java source file as product code | **Not at all** | The stack is .NET (`02:815`); the code is static state, hand-written HTTP and JSON, no tests (row 8), plain HTTP, accept-all certificates (rows 27, L10) |
| Registration call order and record fields | Reference only | Already taken into the design (`02:780`); A7 §4.1 |
| Reserve, pre-prompt, browser, close, post-prompt sequence | Reference only | Already taken (A7 §4.2) |
| The dead Custom Security Attributes lookup | **Not at all, and not as a reference** | Wrong key and wrong algorithm for today's Workpath data (X4). The reference is the Workpath source (`A1:189-200`) |
| The device code flow code | Reference only | Matches the design's baseline mechanism M1 (`02:387`) in outline; it trusts an unverified token and requests no Graph scopes (`S/MicrosoftAuthService.java:426`) |
| The jar set for a Java sidecar | Makes the fallback cheaper | Exact names, versions and hashes of a set that compiles on Java 21 are known (section 6). Swap the HP jar for the 1.8.4.1 one |
| `register` and `unregister` tools | Possible lab probe only | They are the one part that could be pointed at a real OXPd 1.x device to see whether records register at all. They switch certificate checks off and write `http://` callbacks, so never beyond a lab; using them at all is a decision for the product owner (question 5 below), and the plan's spikes are written fresh (`03:47`) |
| Admin page feature list | Reference only | A7 §5.1 |
| Install logs, `README.md`, `INSTALLATION.md`, `start-prompt-server.sh` | Not at all | Unrelated or stale (sections 4.6, 5) |

### 8.6 What it shows about real printers

Nothing. No model, firmware, serial number, device response or reader output is in the tree (row 66). Every spike and open question the documents hold about device behaviour stays as it is: S2 (agents over HTTPS), S3 (reader parity), and question 12 of `05` (anything newer than 1.8.4.1). It says nothing about the printer of C-39.

It also does not touch OQ-7 (the gateway source) or question 10 (the phone sign-in): the build has no gateway call and no phone-app path (rows 38, 47 and section 4.5).

## 9. PROPOSED CORRECTIONS (not applied)

Each is one sentence to change, the document line it replaces, and the source that supports it.

1. **`02:47` (row P14, third column).** Replace "Spike against the simulator" with: "Spike; by the author's note it was checked against an emulator on his own Windows machine, the tree holds no run log, and the copy the product owner sent on 2026-11-20 (C-40) is byte-identical to the library copy [A10 §2, §5]". Support: `OX/todo.txt:22`; section 2 rows 2.3 to 2.5; section 4 row 7.
2. **`02:332` (row C3).** Replace "(JAX-WS RI 4.0.3 + OXPdLib 1.8.4.1 jar, known to work [A7 §5.1])" with: "(JAX-WS RI 4.0.3 + the OXPdLib jar; the earlier build compiled against the SDK 1.8.4 jar, not the 1.8.4.1 one, and that it ran is the author's note only [A7 §5.1] [A10 §6])". Support: `OX/lib/OXPdLib-1.8.4.jar` SHA-256 equal to the SDK 1.8.4 jar and different from the 1.8.4.1 jar (L2, L3); `OX/build.sh:29`; `OX/todo.txt:22`.
3. **`02:648` (row W3, evidence column).** After "[A7 §8.2 item 11]" add: "(the earlier OXPd 1 build's two keys are different values under a different algorithm and are not this key [A10 §7])". Support: `S/MicrosoftAuthService.java:33-34, 323-345`; hash comparison with `CardValidator.kt:10` and `Encryptor.kt:12`; `A1:189`.
4. **`02:626` (secret locations, old build keys).** Replace the description "Hardcoded HMAC and AES keys" with: "Hardcoded HMAC and AES keys of the earlier build's own card scheme, not the Workpath card key; the same two lines are also in the copy under `2_Project_Files/fleet/state/kam_attachments_1120b/extracted/` and in `!CODING/Datasec/Security Review/Source_Code/` [A10 §2, §7]". Support: section 2 rows 2.3 to 2.5; section 7.
5. **`02:49` (row P16, fourth column).** After "redistributable unchanged [C1 §5.3]" add: "; the jar is signed by HP and carries no licence text, so the product takes the 1.8.4.1 build identified by hash and carries the terms from the SDK guide [A10 §6]". Support: L3 to L6; `C1:316, 498`.
6. **`03:345`.** Replace "this is the last state [A7 §7 Q7]; **its two hardcoded keys**: treated as sensitive, covered by C-3 [A7 §7 Q4]" with: "the repository's default branch as sent on 2026-11-20 is byte-identical to the library copy, and no history or other branch was sent [A10 §2]; **its two hardcoded keys** are not the Workpath card key and are still treated as sensitive [A10 §7]". Support: section 2; section 7.
7. **`05:172` (the bullet "Sources that are not in the library").** Add the sentence: "The repository `OXPd1_solution` sent on 2026-11-20 is the earlier OXPd 1 attempt already analysed (report A7), byte for byte, and the repository `OXPD1` is empty, so neither adds source [A10 §2]". Support: section 2; C-40.
8. **`05:180` (the bullet on the backup copy).** Add the sentence: "For the earlier OXPd 1 attempt the comparison has now been made against what the product owner sent from the repository: identical, 73 files [A10 §2]". Support: section 2 rows 2.3 to 2.5.

Not a correction to `02`, `03` or `05`, and so outside the numbered list, for Tuesday to route: (a) the commission's own "What arrived" line and any card or note that tells the product owner the OXPd 1 repository was new material (X1); (b) report A7 lines 232 and 474 and its question 4, which this report qualifies (X4). A7 is a dated analysis report and is not edited; this report is the qualification.

## 10. Open questions for the product owner (each with a default)

1. **Is there more of the earlier OXPd 1 work than this: another branch, a later working copy on the developer's machine, or the repository's history?** What arrived is the default branch and equals what the library already held. Default: no; this is the last state.
2. **Was this code ever run against a physical printer, and if so which model and firmware?** The README names a lab address as the printer; the author's note names an emulator. Default: emulator only; nothing is treated as proven on hardware.
3. **Is the printer administrator password written in the README (`OX/README.md:81`) a live password of a lab printer?** Default: treated as live; it is never copied, and the printer's password should be changed by whoever owns that printer.
4. **Where did the two hardcoded card keys in the earlier build come from: an older Workpath version, or made up for the spike?** They are not today's Workpath card key. Default: made up or outdated; never carried into the new product, never printed.
5. **May the earlier build's register and unregister tools be used once as a lab probe against the test printer, to see whether an OXPd 1.x device accepts the records?** They turn certificate checks off and register plain-HTTP addresses. Default: no; the phase-0 spikes are written fresh, as the plan says.
6. **The repository `OXPD1` ("HP Authentication Suite OXPD V1.8") is empty. Is it meant to receive anything?** Default: ignored; the new work goes to the repository named in C-37.

## 11. What was NOT read

- **13 of the 14 Java source files were not read whole in this pass.** `S/PrinterManager.java` was read whole; six others were read only at the lines listed in section 3; the remaining seven, `S/AdminDatabase.java`, `S/AdminServer.java`, `S/IpCaptureHandler.java`, `S/SoapLoggingHandler.java`, `S/QrCodeHelper.java`, `S/HPAMUserModel.java`, `C/UnregisterCardReaderSolution.java`, and the three handler XML files were searched by program only. Their content is covered by A7's reading of the identical files, which this pass did not repeat.
- **5 of the 6 HTML pages were not read**: `admin.html`, `auth-prompt.html`, `device-code.html`, `error.html`, `prompt.html`; `onedrive.html` at lines 674-679 only.
- `build.bat`, `run-server.bat`, `unregister.bat`: not read (their `.sh` twins and `register.bat` were).
- The 3 `.class` files (version bytes only) and the 3 PNG copies: not opened. `RegistrationClient.class` has no source in the tree; what it does is unknown.
- The 27 jars: entry names and manifests only. No class was decompiled, so what `NaiveTrustProvider.setAlwaysTrust` switches off for the rest of the JVM (A7's open doubt, `A7:320`) is still not established. The licence texts inside the jars were not opened.
- HP's SDK user guide itself (the licence terms at lines 462-468): not opened in this pass; quoted through report C1.
- The PDF print of the `OXPD1` repository page: not opened; its content is taken from the commission and C-40.
- The other three delivered repositories (`hpam-api`, `hpam-marketplace`, `infra_hpam`): not opened; they are lane G.
- Reports A2 to A6, A8, B1 to B3, C2 and the review files R1 to R4: not read. `02` and `03` were read at the lines found by search (about 40 lines of `02`, about 60 of `03`), not whole; `05`, `CLARIFICATIONS.md` and A7 were read whole; A1 and C1 at the lines found by search.
- The Workpath sources in the library: only the two key lines, by hash, and a literal search over text files; nothing else.
- Nothing was built or run, so every statement about behaviour is from reading.
