# A7: the earlier attempt (`OLD BUILD/OXPd1_solution-master`, Java, OXPd 1.x SOAP)

Lane A7 of the Datasec / OXPd analysis, 2026-11-18. Read-only analysis; nothing in the library was changed, built or run.

Path shorthand used for sources (all relative to the library root `/Volumes/Laptop-DEV/!CODING/Datasec/OXPd/`):

- `OB/` = `OLD BUILD/OXPd1_solution-master/`
- `S/` = `OB/server/src/com/hp/authenticationsuiteoxpd/server/`
- `C/` = `OB/client/src/com/hp/authenticationsuiteoxpd/authagent/`
- `W/` = `OB/server/web/`

## 1. BLUF

The lane holds a small Java 21 proof of concept (about 6,000 lines of Java, 2,570 lines of HTML) that registers an OXPd 1.x Authentication Agent, six USB card readers and a home-screen button on a device, and signs a user in to Entra with the OAuth **device code** flow shown as a QR code in the device browser. It was developed against the OXPd simulator on the developer's own Windows machine (`OB/todo.txt:22`). It is a spike, not a base to build on. The five facts that most shape the port:

1. **The card does not identify anyone.** A card read only triggers the QR flow; the Custom Security Attributes lookup exists but is never called (`S/MicrosoftAuthService.java:177`, one occurrence in the tree). Every sign-in needs a phone.
2. **Sign-in is the device code flow, not the product's flow.** No auth code + PKCE on the panel, no SignalR, no HP Secure Authentication app, no stored refresh token redemption (`S/AuthenticationStateMachine.java:517-581`).
3. **The device session is keyed by the printer's source IP address**, and the server is never told about sign-out because sign-out notification is switched off at registration (`S/PrinterManager.java:117`, `C/RegisterCardReaderSolution.java:189`). The previous user's Graph token stays live on the server.
4. **One generic HID keyboard parser serves all six readers**, where the Workpath product has three reader-specific decoders. Card strings may not match what Workpath stores, which breaks shared enrolment in a mixed fleet (finding 4.4).
5. **No transport security anywhere**: four plain HTTP listeners, certificate validation disabled for calls to the device, secrets in plain text in SQLite, two cryptographic keys hardcoded in source (section 8).

## 2. Coverage

| Class | Count | Detail |
|---|---|---|
| Files in the lane | 73 | `find … -type f` |
| Read whole | 40 | 16 root files (README, INSTALLATION, todo, 9 scripts, `.gitignore`, installer script and its 2 logs), 1 workflow file, 12 server Java, 3 handler XML, 2 client Java, 6 HTML pages |
| Not opened | 33 | 27 library jars, 3 compiled `.class` files in `OB/client/bin`, 3 copies of one PNG icon (4,678 bytes each) |
| Inspected without opening | 1 | `OB/lib/OXPdLib-1.8.4.jar`: entry listing, first 12 manifest lines, SHA-256 |

Identity of the two copies: `diff -rq` between `OLD BUILD/OXPd1_solution-master` and `HPAM - Docs and Notes/Source Code/OXPd1_solution-master` printed nothing and returned 0. Only the `OLD BUILD` copy was read.

Outside the lane, read to anchor findings: `START-HERE.md`, `README.md`, `README-INDEX.md` and Kam's verbatim brief (whole); `HPAM - Docs and Notes/Source Code/HPAuthenticationManager-main/app/src/main/java/com/hp/print/hpauthenticationmanager/sdk/PrinterAccessoryService.kt` lines 255-520 (reader decoding); `HPAM/Help-Portal/Articles/FAQ/HP-Authentication-Manager/HP-Authentication-Manager-Supported-NFC-BLE-Readers.md` lines 55-119; `OXPd1-NET-Java/Docs/oxpd-authentication-service-specification.md` lines 40-69 and grep hits at 120, 177, 250, 254.

Not done: no decompiling of OXPdLib classes, so the meaning of some constructor arguments and the scope of `NaiveTrustProvider` are marked (inferred). Nothing was executed.

Dead-code claims rest on one grep over `OB/server/src` and `OB/client/src` for each symbol; the same run returned hits for live symbols (for example `closeAnyRunningSolution` at three lines), which is the positive control.

## 3. Inventory

### 3.1 Layout

| Path | Content |
|---|---|
| `OB/server/src/…/server/` | 12 Java classes and 3 handler-chain XML files: the server |
| `OB/server/web/` | 6 HTML pages (3 live, 3 superseded) |
| `OB/client/src/…/authagent/` | 2 command-line tools: register and unregister |
| `OB/client/bin/` | Committed compiled classes, including `RegistrationClient.class`, which has no source in the tree |
| `OB/lib/` | 27 jars, 23 MB, committed |
| `OB/*.sh`, `OB/*.bat` | build, run-server, register, unregister (bash and Windows); `start-prompt-server.sh` (obsolete) |
| `OB/README.md`, `OB/INSTALLATION.md`, `OB/todo.txt` | Documents, all partly stale (section 6) |
| `OB/claude-install.ps1` and 2 logs | An unrelated tool installer and its transcript, dated 2026-04-06, from a Windows ARM64 machine. They hold a personal user name and machine name (section 8) |
| `OB/.github/workflows/gitleaks.yml` | Secret scan on push to `master` and on every pull request |

There is no `.git` folder, so no history. File times are 30 June; the installer log gives April 2026 as the working period.

### 3.2 Server classes

| Class | Lines | Role |
|---|---|---|
| `CombinedServer` | 703 | `main`; publishes the two SOAP endpoints; hand-written HTTP server on 8080; Graph proxy for OneDrive |
| `CardReaderAuthenticationAgentService` | 554 | The OXPd Authentication Agent (`IAuthenticationAgentService`) |
| `CardReaderAccessoriesCallbackHandler` | 425 | The Accessories callback (`IAccessoriesServiceCallback`) and the HID parser |
| `AuthenticationStateMachine` | 916 | Per-printer `Session`, the device code flow, calls to the device |
| `MicrosoftAuthService` | 595 | Entra calls: device code, token poll, JWT decode; unused PKCE and CSA code |
| `PrinterManager` | 443 | Register, unregister, check; the dynamic OneDrive button |
| `AdminServer` | 804 | Admin HTTP API on 8090 |
| `AdminDatabase` | 474 | SQLite persistence |
| `IpCaptureHandler` | 223 | SOAP handler; fills a map that nothing reads |
| `SoapLoggingHandler` | 138 | SOAP message logger; not wired in |
| `QrCodeHelper` | 59 | ZXing QR to base64 PNG |
| `HPAMUserModel` | 52 | User fields and the console display-name rule |

### 3.3 Build, runtime, ports

- **Java 21**: `javac -source 21 -target 21` (`OB/build.sh:57-59`). No Maven, Gradle or Ant; the scripts compile every `.java` against every jar in `lib/`. `OB/INSTALLATION.md:73-79` tells the reader to run `ant build`, but there is no `build.xml`.
- The JDK path is hardcoded: a Homebrew `openjdk@21` path with a `java_home` fallback (`OB/build.sh:14-17`), and a fixed `C:\Program Files\Java\jdk-21.0.2` on Windows (`OB/build.bat:4`).
- **OXPdLib 1.8.4**: `OB/lib/OXPdLib-1.8.4.jar`, 1,611,836 bytes, 1,057 entries, classes dated 1 May 2024. Its SHA-256 equals the jar in `OXPd1-NET-Java/SDK/hp-ext-XX-oxpd-1.8.4/OXPdLib/Java/lib/`. The latest SDK in the library, 1.8.4.1, ships a jar with the **same file name but a different hash** (1,613,168 bytes, dated 23 June 2025). The old build is one SDK release behind.
- Other libraries: JAX-WS RI 4.0.3 and its Jakarta dependencies, `sqlite-jdbc-3.45.1.0`, ZXing 3.5.3 (`core`, `javase`), `slf4j-nop-2.0.9`. Logging is `System.out` piped through `tee` into `server.log` (`OB/run-server.sh:42-45`).
- Run: `run-server.sh` changes into `server/bin` and starts `CombinedServer`. It takes **no arguments**, although `build.sh:71` advertises `run-server.sh <SERVER_HOST> [PRINTER_HOST] [PRINTER_PASSWORD]`.

| Port | Listener | Used by | Source |
|---|---|---|---|
| 8080 | Raw-socket HTTP: device browser pages, `/session-state`, OneDrive proxy | Device browser | `S/CombinedServer.java:236-259` |
| 8090 | Raw-socket HTTP: admin page and API | Administrator | `S/AdminServer.java:16` |
| 8091 | JAX-WS SOAP 1.2: `AuthenticationAgentService` | Device | `S/CombinedServer.java:91` |
| 8092 | JAX-WS SOAP 1.2: `AccessoriesCallbackHandler` | Device | `S/CombinedServer.java:147` |

All four bind to every interface over plain HTTP.

Configuration sources: SQLite `hpam_config` (tenant, client id, secret, display rule, server IP override); JVM properties or environment for `oxpd.printer.host`, `oxpd.printer.password`, `oxpd.server.host`, `oxpd.admin.db`, `oxpd.web.root`.

## 4. Findings

### 4.1 Registration with a device

Two code paths do the same work: the command-line client (`C/RegisterCardReaderSolution.java`) and the server (`S/PrinterManager.java:63-80`, driven from the admin page). Both hold their own copy of the constants.

Sequence, with the OXPd 1.x service for each call:

| Step | Service | Calls | Source |
|---|---|---|---|
| 0 | (library) | `NaiveTrustProvider.setAlwaysTrust(true)`, then `DiscoveryTreeTranslator.GetOXPdDiscoveryTree(printerIp)` | `S/PrinterManager.java:65,72` |
| 1 | Authentication | `GetAuthenticationAgentRecords`, `UnregisterAuthenticationAgent` for any record with the same name, `GetSupportedAgentBindings` (takes element 0), `RegisterAuthenticationAgent`, `GetAuthenticationAgentRecord` to verify | `S/PrinterManager.java:82-126` |
| 2 | Accessories | `RegisterOwnedAccessory` six times | `S/PrinterManager.java:128-145` |
| 3 | UIConfiguration | `GetTopLevelButtonRecords`, `UnregisterTopLevelButton` for same title, `GetUIProfile`, `RegisterTopLevelButton` | `S/PrinterManager.java:147-194` |

The Authentication Agent record (`S/PrinterManager.java:114-119`), read against the field list in `OXPd1-NET-Java/Docs/oxpd-authentication-service-specification.md:46-63`:

| Field | Value |
|---|---|
| Id | One fixed UUID, the same on every device, hardcoded in three files |
| Name, localized name | "HP Authentication Manager OXPd", `en-US` only |
| AuthenticationAgent | `http://<server-ip>:8091/AuthenticationAgentService`, first supported binding, then arguments `60, 3` (timeouts or retries: inferred, constructor not read) |
| EnablePrePromptCheck | `true` |
| UserPromptTarget | `http://<server-ip>:8080/trigger-auth-direct`, plain binding |
| EnableSignoutNotification | **`false`** |
| SignoutNotificationMaxRetries, RetryInterval | `2`, `4` (ignored while notification is off, per the specification line 58-59) |
| ServerContextId | A random UUID, which the server then ignores |

Owned accessory records: vendor id, product id, serial number `null` (any unit of that model), callback `http://<server-ip>:8092/AccessoriesCallbackHandler` with the SOAP 1.2 binding (`S/PrinterManager.java:134-143`).

Button: title equal to the agent name, position 1, a browser target on the same URL as the prompt, a PNG icon. The icon size is read from `GetUIProfile` but the icon is sent at its original size (`C/RegisterCardReaderSolution.java:338-339`, `S/PrinterManager.java:399-414`).

Credentials: only the device administrator password is passed (`CreateProxy(tree, ip, password)`). The `login` column kept per printer is never used in any device call. The command-line default password is a literal (`C/RegisterCardReaderSolution.java:33`).

Gaps in registration:

- **Unregister leaves the six owned accessories and the OneDrive button on the device** (`S/PrinterManager.java:305-353`). `UnregisterOwnedAccessory` occurs nowhere in the tree.
- Records are found by display name, not by id.
- "Installed" means only that the agent record exists (`S/PrinterManager.java:43-59`).
- The server IP is baked into every URL on the device. The admin page says a changed IP needs a server restart (`W/admin.html:952`); it also needs every printer registered again (inferred from the URLs above).

### 4.2 Sign-in flow, call by call

Session identity throughout: the server takes the TCP source address of each request and uses `"<ip>_session"` as the key (`S/CombinedServer.java:303-305`, `S/CardReaderAuthenticationAgentService.java:235-237`, `S/CardReaderAccessoriesCallbackHandler.java:115-116`). The `serverContextId` and `authenticationContextId` that the device sends are logged and otherwise dropped as keys.

**A. Reader attached**

1. Device to server: `ownedAccessoryEvent` with `CONTEXT_CREATED` (`S/CardReaderAccessoriesCallbackHandler.java:240-277`).
2. Server to device, on a worker thread: discovery tree, `HidOpen(accessoryContextId)`, `HidStartReading(accessoryContextId, "<ip>_session", callback)` (`:282-330`).
3. The callback URL in step 2 is built from property `oxpd.server.host` or environment `OXPD_SERVER_HOST`, **default `127.0.0.1`** (`:44, :92-102`). No script sets either. On the developer's setup the simulator ran on the same machine, so loopback worked; on a real device the reports would be sent to the device itself (inferred).
4. `CONTEXT_REVOKED` is logged only. `CONTEXT_RESENT`, which the Workpath app handles (`PrinterAccessoryService.kt:416-417`), is not handled.

**B. Card presented**

5. Device to server: `hidReportEvent`, one or more reports (`:105-161`). Parsed as in 4.4. On Enter, the string goes to `AuthenticationStateMachine.handleCardSequenceComplete` (`S/AuthenticationStateMachine.java:420-459`):

| Session condition | Action |
|---|---|
| Already authenticated | Queue the card, sign the device out, then start a new flow |
| Device code active or sign-in complete | Ignore the tap |
| Authentication context already reserved (button was pressed first) | Start the device code flow |
| Otherwise | Start the device code flow **and** `triggerAuthentication()` in parallel |

**C. Server starts sign-in on the device**

6. Server to device: discovery tree, then `ReserveAuthenticationContext(<agent UUID>)` on the Authentication service, **without** the administrator password (`S/AuthenticationStateMachine.java:328-345`).
7. If the device answers that a user is already signed in (matched by the text "already signed in" in the exception message, `:302`), the server calls `EndUserSession` or `ReleaseUIContext` on UIConfiguration and `ReleaseAuthenticationContext` on Authentication, waits 1.5 s, and tries once more (`:364-383`, `S/CardReaderAuthenticationAgentService.java:144-198`).

**D. Device runs the agent**

8. Device to server: `getPrePromptResult(authenticationContextId, languageCode, serverContextId)`. The server stores the context id and **always returns `CONTINUED`** (`S/CardReaderAuthenticationAgentService.java:227-258`).
9. Device opens its browser on `/trigger-auth-direct`. The request carries an `OXPd.UIContextId` header, which the server stores (`S/CombinedServer.java:287-311`). The same URL is the home-screen button's target; if no flow is active the handler calls `triggerAuthentication()` itself (`:319-345`). The response is `prompt.html`.

**E. Entra, in the background**

10. Server to Entra: `POST /{tenant}/oauth2/v2.0/devicecode` with `client_id`, scope `openid profile offline_access`, and `client_secret` (`S/MicrosoftAuthService.java:422-464`).
11. Server makes a 220 px QR PNG of `verification_uri_complete` (`S/QrCodeHelper.java:30-58`).
12. Server polls `POST /{tenant}/oauth2/v2.0/token` with the device code grant every `max(interval, 5)` seconds until expiry (`S/AuthenticationStateMachine.java:583-684`, `S/MicrosoftAuthService.java:472-515`).

**F. Panel**

13. `prompt.html` polls `GET /session-state` every 1.5 to 3 s and draws one of four sections: waiting for card, QR with user code and countdown, done, error (`W/prompt.html:157-203`).
14. The user scans the QR with a phone and signs in at Microsoft on the phone.

**G. Completion**

15. Token poll succeeds. The server base64-decodes the **access token** payload, without checking the signature, into `HPAMUserModel` (`S/MicrosoftAuthService.java:371-398`), stores access and refresh tokens on the session in memory, and sets the state to `signin_complete`.
16. The page shows "Signed in!" and after 800 ms calls `window.OXPd.close()`, else `window.close()`, else navigates to `about:blank` (`W/prompt.html:120-125`).
17. Device to server: `getPostPromptResult`. If Entra sign-in completed, the answer is `SUCCEEDED` with `AuthenticationInfo`; otherwise `FAILED` with "Authentication not completed" (`S/CardReaderAuthenticationAgentService.java:260-360`).
18. The server then registers an "HP OneDrive" home-screen button on that device, on a new thread (`:316-335`, `S/PrinterManager.java:198-250`).

`AuthenticationInfo` sent to the device (`S/CardReaderAuthenticationAgentService.java:404-438`): authentication type `OTHER`; fully qualified user name and user principal name = UPN; user name and display name = the configured console name; email; opaque authentication token = the Entra object id; no password, no cookie, no SID, no home folder; language preference from the device's language code.

The console name rule copies the Workpath setting with four choices: first plus last name, UPN, display name, email (`S/HPAMUserModel.java:22-36`).

### 4.3 What "signed in" means afterwards

- **On the device**: a user session carrying the fields above. Which device features that unlocks is decided by the device's own access-control configuration for this agent (inferred from the specification, line 67); the solution sets no permissions.
- **On the server**: `authenticated = true`, and the Graph access and refresh tokens held in memory under the printer's IP. `clearState` deliberately keeps them (`S/AuthenticationStateMachine.java:880-883`). A server restart loses them while the device stays signed in.
- **Sign-out**: `signOutNotification` is implemented (`S/CardReaderAuthenticationAgentService.java:378-397`) but can never be called, because registration disables it. The server session ends only when another card is tapped or an administrator presses Reset. The refresh token is never used (`getRefreshToken` has no caller); when the access token expires the OneDrive page simply fails.
- **Consequence** (inferred): after the device signs the user out by timeout, the OneDrive button is still on the home screen and the server still holds the token under that IP. The next person at the panel can open the previous user's files.

### 4.4 Card readers and HID parsing

The six models (`S/PrinterManager.java:29-36`, same list in `C/RegisterCardReaderSolution.java:39-46` and in the Workpath package manifest `…/HPAuthenticationManager-main/app/packaging_contents_release/hpk.xml:47-78`):

| VID:PID (decimal) | Reader, per the help-portal FAQ lines 59-115 | Workpath decoding (`PrinterAccessoryService.kt`) |
|---|---|---|
| 3111:15354 | RFIDeas WAVE ID family and the HP keystroke readers made by RFIDeas | Own function: converts byte 2 of each report, ends on newline (`:352-371, :499-518`) |
| 1008:69 | HP HIP2 universal reader X3D03A/B | Bytes taken as **raw characters**, ends on byte 13 (`:324-351`) |
| 2520:1040 | Elatec TWN4 | Own table: digits, and **upper-case** letters after a shift marker, ends on byte 40 (`:282-323`) |
| 2520:784 | Elatec (model not named in the FAQ) | Same as 2520:1040 |
| 1899:21544 | OmniKey 5427 (see section 6 for a number mismatch) | **No branch**: logs "Wrong vendor or product id" (`:372-375`) |
| 7590:272 | Inepro Spider | **No branch**, same |

The old build has one parser for all six (`S/CardReaderAccessoriesCallbackHandler.java:168-236`):

- Each report is read as a boot keyboard report: byte 0 modifier, byte 1 skipped, bytes 2 to 7 key codes.
- Shift is bit `0x02` only (left shift). Right shift is ignored.
- Usage codes `0x04-0x1D` become letters, **lower case unless shifted**; `0x1E-0x27` become digits or their shifted symbols; everything else is dropped.
- Usage `0x28` (Enter) ends the card.

Weaknesses, all from the same lines:

- No timeout and no length limit on the buffer. A partial read stays and is prefixed to the next card. The buffer is cleared only on Enter, `clearState` or reset.
- A reader configured without an Enter suffix never completes.
- No check of the report `ordinal`, which is logged (`:109`) but not compared. The Workpath app discards repeats by ordinal (`PrinterAccessoryService.kt:278`).
- No handling of keypad codes, hyphens or other punctuation.
- `remoteHidReportEvent` (encrypted reports) is an empty stub (`:419-423`).
- The vendor and product ids on each report are logged and not used to choose a decoder.
- For the HP reader 1008:69, if its reports reach OXPd as they reach Workpath (raw characters, carriage return), this parser would produce nothing usable and never see an end (inferred from comparing the two code paths; not tested by anyone).
- The README itself says the parser is simplified and may need adjusting per model (`OB/README.md:130`).

Card values are written to the log in clear (`S/CardReaderAuthenticationAgentService.java:75, 84`; `S/AuthenticationStateMachine.java:428`).

### 4.5 How a card maps to a user

**It does not.** `handleCardSequenceComplete` stores the string on the session and uses it only as a trigger (`S/AuthenticationStateMachine.java:429-430`, with the comment that the device code flow now owns sign-in). An unknown card, or one typed into the admin page's "Card Tap" box, starts exactly the same QR flow. The identity is whoever signs in on the phone.

The intended mapping is present as dead code and mirrors the Workpath scheme (`S/MicrosoftAuthService.java:177-352`):

1. Get an app-only Graph token with client credentials (`:219-241`).
2. `GET /v1.0/users` with `$count=true`, header `ConsistencyLevel: eventual`, and a filter on `customSecurityAttributes/HPAuthenticationSuite/cardId` using `startswith` on a hash of the card (`:192-204`).
3. The hash is HMAC-SHA256 of the card string with a hardcoded key, base64 without padding (`:323-333`). A second accepted form is an AES/ECB blob of `card + "%%%%" + email` under a second hardcoded key (`:335-345`).
4. Return the matched user's mail or UPN as a `login_hint` (`:243-264`).

It only reads. Nothing writes a card to a user (no enrolment), nothing stores or redeems a refresh token, and the JSON is parsed with regular expressions.

The older stage, where the card string itself became the user name, survives as an unused method (`S/CardReaderAuthenticationAgentService.java:443-464`) and as the whole of `OB/README.md`.

### 4.6 What the device browser shows, and from where

All pages come from the server's port 8080, read from `OB/server/web/` (`S/CombinedServer.java:405-440`).

| URL | Served file | State |
|---|---|---|
| `/`, `/prompt.html`, `/trigger-auth-direct` | `prompt.html` | Live. Single page for the whole sign-in |
| `/device-code.html`, `/error.html` | `prompt.html` (aliases) | The files of those names are superseded and never served (`:347-353`) |
| `/auth-prompt.html` | `auth-prompt.html` via the generic rule | Superseded, still reachable |
| `/onedrive` | `onedrive.html` | Live |
| `/session-state` | JSON | Live; the one polling endpoint |
| `/onedrive-api?path=` | Graph `GET` proxied with the session's token | Live |
| `/onedrive-file?…` | File bytes, or Graph PDF conversion | Live |

`onedrive.html` (715 lines) lists the user's drive through `/me/drive/root/children`, sorts, shows a breadcrumb, previews images and PDFs, previews Office files through Graph's `?format=pdf`, and shows a print-settings panel (sides, colour, finishing, paper, collate). **Print is a placeholder**: the button raises "Print coming in next version." (`W/onedrive.html:676-678`). The print settings are not sent anywhere.

The admin page (`W/admin.html`, 1,137 lines) is for a desktop browser, not the device: first-run setup, login, recovery, dashboard, printers (add, CSV import, check, install, uninstall, emulate card tap, reset session), HPAM configuration, server IP override.

### 4.7 QR code use

The QR encodes Microsoft's device-login URL with the user code filled in (`S/AuthenticationStateMachine.java:555-563`). It is drawn on the server and sent inside the JSON as base64, so the device browser needs no internet access and no script library (`S/QrCodeHelper.java:3`). The quiet zone is one module (`:35`). The page also prints the user code and the address to type by hand (`W/prompt.html:100-101`).

This is unrelated to the product's QR sign-in, where the HP Secure Authentication phone app scans a code and a SignalR message reaches the device (`OB/todo.txt:6`). `signalREndpoint` is only a stored setting (`S/AdminServer.java:439`).

### 4.8 SQLite

File: `OB/data/admin.db` by default (`S/CombinedServer.java:50`), WAL mode, one shared connection, every method `synchronized` (`S/AdminDatabase.java:40-58`).

| Table | Columns | Use |
|---|---|---|
| `admin_users` | `username` PK, `password_hash`, `recovery_code`, `created_at` | Admin login. Hash is PBKDF2-HMAC-SHA256, 65,536 iterations, 16-byte salt (`:438-447`). Recovery code in plain text |
| `auth_events` | `id`, `timestamp` (indexed), `printer_ip`, `event_type`, `card_sequence`, `result` | Dashboard log. For sign-in results the `card_sequence` column holds the user's **email** (`S/CardReaderAuthenticationAgentService.java:344`) |
| `hpam_config` | `key` PK, `value` | Tenant id, client id, client secret, SignalR URL, console name rule, MFA flag, reporting string, licence URL, server IP override |
| `printers` | `id`, `ip` unique, `login`, `password`, `added_at`, `installed`, `last_check_at` | Fleet list. Password in plain text, defaulting to a literal |

No tokens, sessions or card mappings are persisted. No migrations or schema version.

A small defect: the printer rows are built with keys `addedAt` and `lastCheckAt` (`S/AdminDatabase.java:383-385`) and read back as `added_at` and `last_check_at` (`S/AdminServer.java:545-546`), so the API always returns null for both.

### 4.9 Finished, stubbed, missing against `todo.txt`

| Item in the brief (`OB/todo.txt`) | State | Evidence |
|---|---|---|
| Act as authentication agent on the device | Working on the simulator | 4.1, 4.2 |
| Listen to the card reader | Working as a trigger, generic parser | 4.4 |
| Card to user email in Custom Security Attributes through a service principal | Read path written, **never called**; no write path | `S/MicrosoftAuthService.java:177` |
| Sign in against Microsoft | Done with device code, not the product's auth code + PKCE. PKCE helpers exist unused (`:64-173`); there is no `/callback` route | 4.2 |
| Distribute the token to the other apps | Collapsed into a server-side session: the OneDrive page reads the token by printer IP. No interface for other apps | `S/AuthenticationStateMachine.java:896-899` |
| SignalR socket for the phone app's QR | Missing; only a settings field | `S/AdminServer.java:439` |
| MFA / no-MFA mode | Missing; only a checkbox that is stored | `W/admin.html:439-443` |
| Mailflow | Missing | no file |
| Teams | Missing | no file |
| OneDrive | Browse and preview written; print and scan-to missing | 4.6 |
| SharePoint | Missing | no file |
| Universal Print (`_Direct`, `_Secure`, `_Pull`) | Missing | no file |
| Scan and print through SOAP | Missing: no Scan, Copy, Print or Statistics proxy is used | imports in `S/*.java` |
| Shared look (CommonValueLibrary) | Missing; pages use ad hoc styles | `W/*.html` |
| Licensing, reporting | Settings fields only | `S/AdminServer.java:437-441` |

A doubt on the OneDrive part: the only scopes requested are `openid profile offline_access` (`S/MicrosoftAuthService.java:426`), so the token may not carry file permissions, and the page may fail on real data (inferred from Entra behaviour, not from the library).

### 4.10 Architecture and code quality

**Structure.** One process, static state everywhere, no dependency injection, no tests, no interfaces between layers. The state machine calls SOAP proxies directly; HTTP handlers reach into static maps; the SOAP agent writes to the database and starts button installs. JSON is built and parsed by hand with string concatenation and regular expressions (`S/AdminServer.java:770-799`, `S/MicrosoftAuthService.java:540-586`). Both HTTP servers are hand-written on `ServerSocket`, reading one byte at a time.

**Threading.**

- Unbounded cached thread pools (`S/AuthenticationStateMachine.java:31`, `S/CombinedServer.java:242`, `S/AdminServer.java:21, 61`).
- A new single-thread executor is created per event and never shut down (`S/CombinedServer.java:68, 332`; `S/CardReaderAuthenticationAgentService.java:318`), which leaks a thread each time.
- Each sign-in holds a thread asleep in the poll loop for up to the code's lifetime.
- `Session` mixes `volatile` and plain fields written from several threads; the card buffer is a bare `StringBuilder`.
- Sessions, admin jobs and pending OAuth states are never expired (`S/AuthenticationStateMachine.java:389`, `S/AdminServer.java:26`, `S/MicrosoftAuthService.java:40`).

**TLS and certificates.**

- No listener uses TLS. Every registered URL is `http://`.
- `NaiveTrustProvider.setAlwaysTrust(true)` is called at start-up and before each device call (`S/CombinedServer.java:42`, `S/PrinterManager.java:44, 65, 200, 254, 307`). `OB/INSTALLATION.md:230` itself says not to use it in production.
- Whether that setting also switches off certificate checks for the calls to Entra and Graph in the same JVM is **not established**; the class was not decompiled. If it does, token requests carrying the client secret are open to interception.
- No certificate management for the device (the library has a `CertificateManagementProxyFactory`; it is not used).

**Error handling.** Broad `catch (Exception)` with a log line and continue. Device state is inferred from exception text (`S/AuthenticationStateMachine.java:302`, `S/PrinterManager.java:53-54`). Failed button installs and failed sign-outs are logged and forgotten.

**Hardcoded values.** Ports; the agent UUID in three files; the reader list in two files; a default administrator password literal in six places; default host `127.0.0.1` for printer and server; `en-US` strings only; US paper sizes in the OneDrive page; `http://localhost:8090` as the admin API address inside the admin page (`W/admin.html:585`), which makes the admin page usable only from a browser on the server itself, while the port is open to the network.

**Wrong-target bugs** that a single simulator hides:

- `signOutPreviousUser` and `forceDeviceSignOut` use the property-configured host or password, not the calling printer's record (`S/CardReaderAuthenticationAgentService.java:159, 367-369`).
- The `HidStartReading` callback address (4.2 step 3).

Security weaknesses are listed in section 8.

### 4.11 What the code reveals about OXPd 1.x

Each item is something the author ran into, with where it shows.

| Constraint or behaviour | Evidence |
|---|---|
| Nothing is installed on the device. Records are registered at run time and persist on the device | `OB/INSTALLATION.md:5, 171-177` |
| The device calls the server, so the server address is fixed into the device and must be reachable from the printer network | `S/PrinterManager.java:67-69`, `S/PrinterManager.java:361-381` (subnet matching to pick the address) |
| Inbound SOAP needs the WS-Addressing 2004 handler from OXPdLib. Declaring it by annotation failed under the Jakarta JAX-WS runtime, so it is added in code | `S/CardReaderAuthenticationAgentService.java:35-36`, `S/CombinedServer.java:100-116` |
| Proxy calls from pool threads need the context class loader set by hand | `S/AuthenticationStateMachine.java:290-292, 518` |
| A card read at an idle device does not start sign-in. The server must call `ReserveAuthenticationContext` | `S/AuthenticationStateMachine.java:449-458` |
| `ReserveAuthenticationContext` fails when a user is signed in; the server must end the session first and wait | `S/AuthenticationStateMachine.java:302-320`, `:30` (1.5 s) |
| `getPostPromptResult` comes when the browser closes, for any reason. The page must close itself; pressing Home yields a failed sign-in | `S/CardReaderAuthenticationAgentService.java:287-291, 346-357`, `W/prompt.html:120-125` |
| The browser must stay on the registered URL; leaving it restarts the cycle. Hence one page with polling | `W/device-code.html:150-151`, `S/CombinedServer.java:342-345` |
| Browser requests carry the UI context id in an `OXPd.UIContextId` header; it is needed to close the browser from the server | `S/CombinedServer.java:296-299`, `S/AuthenticationStateMachine.java:260-264` |
| Two ways to close: `EndUserSession` (returns to home, signs out) and `ReleaseUIContext` (closes the browser only) | `S/AuthenticationStateMachine.java:242-252` |
| A reader must be opened and reading started on each `CONTEXT_CREATED`; the call back to the device must not block the callback | `S/CardReaderAccessoriesCallbackHandler.java:255-271, 299-321` |
| The device does not tell the callback which printer it is in a usable way, so the author fell back to the source IP | `S/IpCaptureHandler.java:1-5`, `S/CardReaderAuthenticationAgentService.java:466-551` |
| Button ids must be UUIDs; icon size is device-specific | `C/RegisterCardReaderSolution.java:316`, `:296-313` |
| Apps cannot be hidden until sign-in by simple means, so the OneDrive button is added after sign-in and removed on reset | `S/PrinterManager.java:196`, `S/CombinedServer.java:66-82` |
| The device browser is treated as old: the OneDrive page uses `var` and `XMLHttpRequest` only, though the prompt page uses `fetch` | `W/onedrive.html:251-260`, `W/prompt.html:191` |

Dead code that records abandoned approaches: card string as user name; a timed "authenticating" screen (`completeAuthenticationAfterDelay`, `isLoadingInProgress`); server-chosen page (`determinePageToServe`); auth code + PKCE with a `/callback`; device id from `GetManufacturerInfo` (`S/CombinedServer.java:668-700`); the SOAP-body IP map; the SOAP logger.

## 5. What this means for the port

### 5.1 Reusable for a new OXPd 1.x back end

Reuse as **knowledge and call order**, to be rewritten, not as code to copy.

| Item | Why | Finding |
|---|---|---|
| The registration recipe: three services, the order of calls, the record fields | It is a worked example that reached a signed-in state on the simulator | 4.1 |
| The run-time sequence: reserve context, pre-prompt `CONTINUED`, browser, close, post-prompt with `AuthenticationInfo` | Same | 4.2 |
| The reconcile step for "already signed in" and the settle delay | A real device behaviour to design for | 4.11 |
| The single-page prompt with one polling endpoint and self-close | Forced by the platform | 4.11 |
| The reader start-up sequence (`HidOpen`, `HidStartReading`) | Required | 4.2 |
| The `AuthenticationInfo` mapping and the four console-name choices | Matches the Workpath setting | 4.2 |
| Server-drawn QR passed as data | Removes the device's need for internet | 4.7 |
| The CSA query shape: `$count`, `ConsistencyLevel: eventual`, filter path | Starting point, to check against the Workpath source | 4.5 |
| The admin feature list: fleet list, CSV import, install, check, uninstall, card-tap emulation, session reset | A sound first cut of what operators need | 4.6 |
| The library set that works on Java 21: JAX-WS RI 4.0.3 with OXPdLib 1.8.4 | Saves a compatibility search, if Java is chosen | 3.3 |

### 5.2 Throw away

- Session identity by IP address. Use a stable device identity and the device's own context ids.
- The generic HID parser. Port the per-reader decoders and add ordinal checks, a timeout and a length limit.
- The device code flow as the main sign-in, unless Kam confirms it (question 1).
- Both hand-written HTTP servers and the hand-written JSON.
- Static global state and the per-event executors.
- Plain HTTP, trust-all certificates, plain-text secrets, hardcoded keys.
- The dynamic add and remove of home-screen buttons as an access-control method, unless the OXPd Authorization service proves unusable (another lane's subject).
- The duplicated registration client; one code path is enough.
- `README.md`, `INSTALLATION.md` and `start-prompt-server.sh` as documentation.

### 5.3 Requirements and traps

1. **Card strings must equal Workpath's, byte for byte, per reader model.** The stored value is a keyed hash of the string, so a difference in letter case or terminator makes an enrolled card unknown. In a mixed fleet this decides whether a card enrolled at a Workpath device works at an OXPd device. (4.4, 4.5)
2. **Two of the six registered readers have no decoder in the Workpath app** (1899:21544, 7590:272). Their support needs checking before any promise is made. (4.4)
3. **Turn sign-out notification on** and treat it as best effort: the specification says it is not sent after a power loss (line 254). Add a server-side session timeout as well. (4.3)
4. **The server holds the user's tokens.** On Workpath the token lives on the device; here it lives on the server for every signed-in device. This needs encryption at rest if persisted, strict clearing on sign-out, and a stated position for customers. "Token sharing" between apps becomes a server-side session service. (4.3, 4.9)
5. **The server's address is written into every device.** Use a DNS name and TLS from the start; plan re-registration as a routine fleet action. (4.1)
6. **The sign-in UI cannot leave its page** and completion is signalled by closing the browser. An auth code flow that redirects the panel browser to Microsoft and back must be tested against this early, on a real device. (4.11)
7. **Idle card tap is server-initiated**, so the server needs device credentials and a network path to every device at all times. (4.11)
8. **Uninstall must remove everything it registered**, including accessories. (4.1)
9. **Nothing here was proven on hardware.** Treat every flow as unverified on a physical OXPd 1.x device. (BLUF, 4.2 step 3)
10. **Use SDK 1.8.4.1**, not the 1.8.4 jar in this build; the jar keeps the same name, so check the hash. (3.3)

### 5.4 Lessons for one server that serves OXPd 1 and OXPd 2

- **Keep the protocol at the edge.** Here the state machine, the HTTP handlers and the SOAP agent are fused. A dual server needs a core that knows nothing of SOAP or REST, with a small set of operations: device registered, reader input received, sign-in requested, sign-in completed with a user, sign-out, close panel UI. One adapter implements these with the OXPd 1.x SOAP services; another with the OXPd2 REST services.
- **Normalise at the adapter.** Card input should leave each adapter as the same string for the same card and reader. Device identity should leave each adapter as the same kind of key.
- **Share the panel web app.** On both generations the user sees pages from the server in the device browser. One web front end with a thin per-platform shim (how to close, how the context id arrives) avoids two UIs.
- **Share the identity core.** Entra sign-in, CSA lookup and write, token custody and Graph calls do not depend on the device generation, nor on Workpath; they should match the Workpath behaviour exactly.
- **Make fleet management first class.** Registration state per device, idempotent install and uninstall, and credential storage are needed for OXPd 1; OXPd2 replaces registration with a signed bundle but still needs the same inventory.
- **Choose the language once.** OXPd 1 offers .NET and Java libraries; OXPd2 offers .NET, Java and JavaScript (`START-HERE.md:60`). The existing back end is C# (`START-HERE.md:41`). This build chose Java without a recorded reason.

## 6. Contradictions and doubts

| Subject | Source A | Source B |
|---|---|---|
| What the solution does | `OB/README.md:16-18, 97, 132`: any card is authorised and its string becomes the user name | Code: Entra device code sign-in; card is a trigger only (4.5). The code is current |
| Package and paths | `OB/README.md:79, 117-123`: `solution/…/com/example/oxpd/` | Actual package `com.hp.authenticationsuiteoxpd` |
| Registration tool | `OB/INSTALLATION.md:34, 105-135`: `RegistrationClient.java` with four arguments | No such source; only a stale `.class` in `OB/client/bin`. The real tool is `RegisterCardReaderSolution` with three arguments |
| Build tool | `OB/INSTALLATION.md:73-79`: Ant | Shell and batch scripts; no `build.xml` |
| Pre-prompt check | Comment at `C/RegisterCardReaderSolution.java:187`: checks for card data before showing the browser | `getPrePromptResult` always returns `CONTINUED` |
| Button type | Printed text at `C/RegisterCardReaderSolution.java:355`: "Info only (no browser)" | The button has a browser target (`:328-336`) |
| Auth flow header | `S/MicrosoftAuthService.java:3`: "authorization-code + PKCE flow" | Device code is the active flow; PKCE is unused |
| Server arguments | `OB/build.sh:71` | `OB/run-server.sh` takes none |
| Java file count | `START-HERE.md:25`: `server/src` has 14 Java files | 12 in `server/src`, 2 in `client/src` |
| OmniKey product id | FAQ line 115: hexadecimal 428, decimal 21455 | Code and `hpk.xml`: 21544 (hexadecimal 5428). The FAQ figures do not agree with each other either |
| `.gitignore` | Ignores `client/bin/` and `*.class`; has a heading for jars with no pattern | This copy contains `client/bin` classes and all jars |
| Prompt server | `OB/start-prompt-server.sh`: Python server on 8080 | `CombinedServer` binds 8080 itself; the script would conflict |

Doubts:

- The scope of `NaiveTrustProvider` (4.10).
- Whether the OneDrive page works with the scopes requested (4.9).
- How HID reports from each reader actually look when delivered by OXPd Accessories as opposed to the Workpath SDK (4.4).
- Whether Entra accepts the device code grant for the product's app registration; the library has a document on disabling public client flows (`START-HERE.md:48`), which points the other way (inferred).

## 7. Questions for Kam or his team

1. **Was the device code flow a stopgap, or is it an accepted sign-in method for OXPd?** Why it matters: it sets the whole sign-in design, and tenants often block this flow by policy (general knowledge, not from the library). Assumed if unanswered: stopgap; the port follows the Workpath flows (auth code + PKCE, stored-token redemption, the phone app through SignalR).
2. **Must a card enrolled at a Workpath device work at an OXPd device, and the reverse, against the same Custom Security Attributes?** Why: it fixes the card-string and hashing rules and where the hashing key lives. Assumed: yes, full interchange.
3. **Was this build ever run against a physical OXPd 1.x device with real readers? Which models and firmware?** Why: nothing in the tree shows it, and several defaults only work with a co-located simulator. Assumed: simulator only.
4. **Are the two hardcoded keys in `S/MicrosoftAuthService.java:33-34` the production keys of the Workpath product?** Why: if so, they protect every customer's stored card values and now sit in a second source tree; the port needs a decision on key custody. Assumed: yes, and to be treated as sensitive.
5. **Is server-side custody of user tokens acceptable to customers and to Datasec's security position?** Why: unavoidable on OXPd, and a change from Workpath. Assumed: acceptable with encryption, short lifetime and on-premises hosting.
6. **Java or .NET for the new server?** Why: this build is Java; the existing back end is C#. Assumed: decided in the architecture document on the strength of the OXPd2 and OXPd 1 libraries, not on this build.
7. **Is there a later version or a git history of this build, and is its author available?** Why: there is no `.git`, and the documents lag the code. Assumed: this is the last state.
8. **Are OmniKey 5427 and Inepro Spider supported today on Workpath?** Why: they are registered but the app has no decoder branch for them. Assumed: not working today; out of the first release.

## 8. Secrets and sensitive items seen (locations only), and weaknesses not to carry over

### 8.1 Secrets and personal data

| Location | What |
|---|---|
| `S/MicrosoftAuthService.java:33` | A hardcoded HMAC key for card hashing |
| `S/MicrosoftAuthService.java:34` | A hardcoded AES key for the card blob |
| `OB/README.md:81` | A printer administrator password written as the "default" |
| `C/RegisterCardReaderSolution.java:33`, `C/UnregisterCardReaderSolution.java:21`, `S/CardReaderAuthenticationAgentService.java:56`, `S/AdminDatabase.java:94`, `S/AdminServer.java:558-559`, `OB/register.sh:13` | A default device administrator password literal |
| `OB/claude-install.log:4-7, 19-22`, `OB/claude-install-console.log:1, 4, 12` | A real person's user name, a machine name and local paths |
| `OB/README.md:34, 72, 80` | A lab printer IP address |
| Run-time, not in the tree: `OB/data/admin.db` | Would hold the Entra client secret, printer passwords and the admin recovery code in plain text. The file is not present in this copy |

No tenant id, client id, client secret, token or certificate was found in the tree. The gitleaks workflow exists, yet the two keys above are in the source.

### 8.2 Weaknesses the port must not repeat

1. **No TLS on any listener**; the Entra-derived user data, session state and admin password travel in clear (`S/CombinedServer.java:91, 147, 238`; `S/AdminServer.java:68`).
2. **Certificate validation disabled** for device calls, possibly JVM-wide (4.10).
3. **Session by source IP.** Any host that reaches port 8080 from a printer's address, or shares it through NAT, is that printer's session (`S/CombinedServer.java:303-305`).
4. **Unauthenticated Graph proxy** for that session: `/onedrive-api` forwards any Graph `GET` path with the user's token and answers with `Access-Control-Allow-Origin: *` (`S/CombinedServer.java:358-368, 502-530`).
5. **Server-side request forgery**: `/onedrive-file?url=` fetches any URL from the server (`S/CombinedServer.java:543-558`).
6. **Tokens outlive the user's device session** because sign-out notification is off (4.3).
7. **Access token trusted without signature check** to build the identity sent to the device (`S/MicrosoftAuthService.java:371-398`).
8. **Secrets in plain text in SQLite**: client secret, printer passwords, recovery code (4.8). The secret is also returned in full to the admin page (`S/AdminServer.java:445-455`, `W/admin.html:1016`) although a second endpoint takes care to redact it.
9. **Admin first-run setup is open**: whoever reaches port 8090 first creates the administrator (`S/AdminServer.java:218-233`). No lockout or rate limit on login or recovery; CORS `*` on the admin API (`:728`).
10. **Card-tap emulation in the admin API** starts a sign-in on any printer (`S/AdminServer.java:388-403, 610-620`). Keep such a tool out of production builds.
11. **Hardcoded AES in ECB mode and a fixed HMAC key** for card values (`S/MicrosoftAuthService.java:323-345`). The scheme is inherited from the Workpath product (per the file's own header, `:4`); the port should record it as an existing product weakness and decide whether compatibility requires keeping it.
12. **Sensitive values in logs**: card strings, user email, tenant and client ids, Entra error bodies (`S/CardReaderAuthenticationAgentService.java:75`, `S/AuthenticationStateMachine.java:531-536`, `S/MicrosoftAuthService.java:161, 491-493`).
13. **Admin page pulls scripts and fonts from public CDNs** (`W/admin.html:7, 9`), which fails on an isolated network and adds a supply-chain exposure.
14. **Device administrator password reused as a default** and never required to be set (`S/AdminServer.java:558-559`).
