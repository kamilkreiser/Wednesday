# A6 — Behavioural specification of the HP Authentication Suite, from its product documentation

Lane A6, Datasec / OXPd, 2026-11-18. Source: the documentation only (`HPAM/` and the non-source part of `HPAM - Docs and Notes/`). No source code was read in this lane; where another lane's code reading disagrees, the code wins (`START-HERE.md:42`).

## 1. BLUF

This lane holds the customer-facing description of the suite at V4.4: seven panel/phone apps, their journeys, the customer-side Azure back end, the Entra registration, network needs, readers, errors and known issues. Five facts shape the port:

1. **The sign-in is a browser journey on the panel plus a keyboard-wedge card read.** The Microsoft login runs in the printer's embedded browser (`COMMON:32`, `CA:53-55`); readers deliver the card ID as HID keystrokes, 32 characters at most (`RDR:58-67`). Both have direct OXPd counterparts to verify; neither needs app code on the device.
2. **Every credential and every stored refresh token lives in the customer's Entra tenant** (Custom Security Attributes on the user object), written by the "HP Authentication Manager" service principal with a client secret that today is pushed to every printer (`TOKENS:17`, `CSA:99`, `PD:111`). A server-side port can keep that secret off the devices, and a card enrolled on a Workpath printer can work on an OXPd printer if the port reads the same attributes in the same format.
3. **One session, many apps, and "exit is not sign out".** HPAM signs the user in once; Mailflow, OneDrive, SharePoint, Teams and Universal Print reuse the delegated Graph token until Sign Out, a second card tap, or the device inactivity timeout (`AMUG:241-250`, `S1 §2.4`).
4. **Universal Print is the most device-bound app.** Each printer registers itself up to three times (`_Secure`, `_Direct`, `_Pull`), holds a Microsoft-issued certificate with a 10-year life, serves Direct and Pull with nobody at the panel, and feeds the engine through IPPS (`UPDG:101-102`, `UPCERT:15`, `UPNET:9`). In the port the server must hold these identities and push jobs to the device.
5. **The documentation loses all screenshots and never states numeric limits, QR payload, SignalR messages, the Universal Print permissions or the HPCC configuration schema.** Those must come from the source lanes; the doc set alone cannot rebuild the product (§6, §7).

## 2. Coverage

Source keys used in citations (all paths relative to the library root; `HP/` = `HPAM/Help-Portal/`, `M/` = `HPAM/Help-Portal/Documents-Text/Manuals/`, `AR/` = `HPAM/Help-Portal/Articles/`):

| Key | File |
|---|---|
| ROOT | `HPAM/README.md` |
| G1…G7 | `HP/Apps/01-HP-Authentication-Manager.md` … `07-Network-Security-and-Conditional-Access.md` |
| HD | `M/HP Authentication Manager Azure Hosted Deployment Instruction.txt` |
| PD | `M/HP Authentication Manager Azure Printer Deployment Instruction.txt` |
| AMUG | `M/Datasec-HP_Authentication_Manager_UG.txt` |
| SEC | `M/HP Authentication Manager Azure App Registration Secret update Guide.txt` |
| DPF | `M/Disable-Public-Client-Flows.txt` |
| IDS | `M/Azure_Firewall_IDS_Info.txt` |
| RDR | `M/Datasec - Reader_Configuration.txt` |
| CA | `M/Conditional Access General Support Information.txt` |
| FWBP | `M/Firmware Update Best Practices v1.txt` |
| UPUG / UPDG | `M/Datasec-HP  Universal Print UG.txt` / `M/Datasec-HP Universal Print Deployment and Setup Guide.txt` |
| MFUG / ODUG / SPUG / TMUG | `M/Datasec - HP Mail Flow UG.txt` / `Datasec-HP OneDrive UG.txt` / `Datasec-HP_SharePoint-UG.txt` / `Datasec- HP Teams UG.txt` |
| SAUG / SAIUG / SAISG | `M/Datasec-HP_Secure_Authentication_UG.txt` / `…_Intune_UG.txt` / `M/HP_Secure_Authentication_Manager_Intune_Setup_Guide.txt` |
| LEGC / LEGB / LEGF | `M/Archive/V4 PDF/Customer HP Authentication Manager Deployment Instruction 1-2.txt` / `NFR BYO Azure Tenant Deployment Instructions 1-2.txt` / `NFR Free Azure Tenant Deployment Instructions.txt` |
| WP | `HP/Documents-Text/Portal-Attachments/HP Workpath - Security Whitepaper (September 2024).txt` |
| ERR | `AR/Error-Codes/HP-Authentication-Manager-Error-Codes/HP-Authentication-Manager-Error-Codes.md` |
| NEW | `AR/Error-Codes/HP-Authentication-Manager-Error-Codes/What-s-New.md` (8 other copies differ only in the category header line; checked with `diff`) |
| KNOWN | `AR/FAQ/Trouble-Shooting-Guides/Known-issues-Limitation-s.md` |
| in `AR/FAQ/HP-Authentication-Manager/`: READERS, PORTS, TOKENS, REGIONS, QR, SIGNALR, LA, LICENSE, FWVER, ADVANCE, UPCERT, FORGOT, USERPASS, HPAMFAQ, LANG | `HP-Authentication-Manager-Supported-NFC-BLE-Readers.md`, `What-ports-do-I-need-…md`, `Azure-Refresh-Tokens-…md`, `What-are-Printer-Regions.md`, `What-information-is-inside-the-QRCode.md`, `What-is-Azure-SignalR-Service-…md`, `What-is-Azure-Monitor-Log-Analytics-used-for.md`, `How-to-Order-and-or-Purchase-…md`, `What-Firmware-version-…md`, `HP-Authentication-Manager-and-HP-Advance.md`, `How-long-does-Universal-Print-Registration-certificate-s-live-for.md`, `What-happens-if-I-forgot-…md`, `Can-I-use-Username-and-Passwords-only-…md`, `HP-Authentication-Manager.md`, `What-Language-localization-do-you-support.md` |
| in `AR/FAQ/General-Information/`: COMMON, CSA, PREREQ, ROLES, PWLESS, CYPHER, ELATEC, UPNET | `Common-issues-when-setting-up-HP-Authentication-Manger.md`, `Custom-Security-Attributes-and-why-we-chose-this-pathway.md`, `Prerequisites-for-HP-Authentication-Manager.md`, `What-Permissions-Roles-Are-Required-…md`, `How-to-Setup-Azure-Passwordless-Authentication.md`, `How-do-I-add-my-Biometric-Finger-Prints-to-a-CypherCard.md`, `How-to-Program-Elatec-TWN4-Readers-…md`, `Which-Network-Services-do-I-need-for-Pull-and-Direct-Print.md` |
| in `AR/FAQ/Trouble-Shooting-Guides/`: CATIPS, E50199, SECUPD, DIAG, CARDFAIL, LOSTLA, TIPS, SYNC, HPCCISSUE | `Azure-Conditional-Access-and-Policy-Tips.md`, `Entra-ID-Sign-In-Failure-50199.md`, `How-do-I-update-my-App-Registration-Secret.md`, `How-to-produce-log-diagnostic-reports.md`, `I-cannot-sign-in-anymore-…md`, `I-lost-my-log-Analytics-…md`, `Printer-Trouble-shooting-Guide-Tips.md`, `Unable-to-Synchronise-Printer-…md`, `I-am-having-issues-with-HP-Command-centre.md` |
| UPGRADE / MANUALS | `AR/FAQ/HP-Authentication-office-365-Suite/Upgrading-Tips-Best-Practice-suggestions.md` / `User-Manuals-and-configuration-guides.md` |
| V05, V06, V07 | `HPAM/Videos/05-…`, `06-…`, `07-…` (auto-captions) |
| S1 §n, S2 §n, S3 §n | sub-reader extracts (see below); each carries its own `path:line` citations |

Three slices were read whole by sub-readers of this lane, who wrote line-cited extracts that I read whole and merged: S1 (Mailflow, OneDrive, SharePoint, Teams), S2 (Universal Print), S3 (mobile app, QR, BLE). The extracts sit in the session scratchpad at `/private/tmp/claude-501/-Volumes-Laptop-DEV-FRIDAY/d534540a-a4f0-44ac-a3a3-685bcd5abffc/scratchpad/oxpd_A6/` (`S1_m365_apps.md`, `S2_universal_print.md`, `S3_mobile_app.md`); that folder is temporary. Where this report cites `S1 §…` the underlying manual line is in the extract. I did not re-verify the sub-readers' line numbers against the manuals.

| Set | Count | Read whole | Sampled | Not opened |
|---|---|---|---|---|
| Library root briefs (`START-HERE.md`, `README.md`, `README-INDEX.md`) | 3 | 3 | 0 | 0 |
| `HPAM/README.md`, `HP/README.md`, `HP/INDEX.md` | 3 | 3 | 0 | 0 |
| `HP/Apps/` guides 01–07 | 7 | 7 | 0 | 0 |
| `HP/Documents-Text/` (text of the manuals) | 25 | 23 (14 by me, 9 by sub-readers) | 2: `EULA.txt` and `HP Privacy Statement.txt`, by keyword grep (licensor, data collection) plus the first lines | 0 |
| `HP/Articles/` files on disk | 91 (83 distinct + 8 extra copies of "What's New") | 86 (43 by me, 35 by sub-readers, 8 copies by `diff`) | 0 | 5: two EULA copies, two privacy-statement copies, one "Copyright Information" |
| `HPAM/Videos/` transcripts | 11 | 11 (3 by me, 8 by sub-readers); 01 and 02 have no speech | 0 | 0 |
| `HP/Documents/` binary originals (25 PDF, 4 ZIP, 2 MP4) | 31 | 0 | 0 | 31, by the lane brief (text versions read instead). The two videos, the reader tool archives and the HP Diagnostic Tool are therefore unread. |
| `HPAM - Docs and Notes/` outside `Source Code/` | 1 | — | — | only `.DS_Store`; there are no notes or documents there |

`INDEX.md` lists 91 links; the "83 articles" figure in the READMEs is the count of distinct articles. `HP/README.md:39` says "27 original files"; 31 are on disk.

One text file has no content: `HP/Documents-Text/Technical Resources/Cold Reset  Format Drive.txt` is the six-line placeholder of a rights-protected PDF.

## 3. Inventory

### 3.1 Apps, editions and versions as documented

| Component | Kind | Version stated | Source |
|---|---|---|---|
| HP Authentication Manager (HPAM) | Workpath app on the printer: sign-in hub, licence check, printer activity logs, servicing of Universal Print Direct/Secure/Pull jobs | V4.4 (previous V4.2.1, V4.2, V4.1, V3) | `HD:87-90`, `NEW:9,55,97` |
| Mailflow for HP Authentication Suite | Workpath app (Outlook) | V4.4 | `NEW:106` |
| OneDrive for HP Authentication Suite | Workpath app (OneDrive for Business) | V4.4 | `NEW:123` |
| SharePoint for HP Authentication Suite | Workpath app | V4.4 | `NEW:145` |
| Teams for HP Authentication Suite | Workpath app | V4.4 | `NEW:161` |
| Universal Print for HP Authentication Suite | Workpath app (panel UI and registration); job servicing is attributed to HPAM | V4.4.1 | `NEW:177`, `HD:89-90` |
| HP Secure Authentication | iOS/Android mobile badge app (QR and BLE) | user guide "V1.5.12" (7 Oct 2026); readers article says app v1.4.9 or later | `S3 §1`, `READERS:11` |
| HP Secure Authentication for Intune | MDM edition, id `com.hp.secureauth.intune` | FAQ says "V1.3.3 has been released" | `S3 §1, §3` |
| "HP Authentication Suite Onboarding Azure Services" | Azure Marketplace deployment (SignalR, Function App, Storage, Log Analytics) | not versioned | `HD:635-637` |
| Datasec licence server | Azure Australia East | — | `HD:276-279`, `PORTS:70` |
| Legacy "API/Keycloak Hosted Services" | Datasec-hosted back end of V3 and of V4 sites that did not self-host | — | `LEGC:77-87`, `PD:38-47` |

The user's brief names "one or two more" apps beyond the five; the documentation names exactly five panel apps plus HPAM (`HD:76-80`). No sixth panel app is documented. HPAM is also offered as the authenticator for HP Advance and LRS VPSX Print Release (§4.9).

Languages: English only (`LANG:9`, `HD:159`). Copyright holder: Datasec Solutions Pty Ltd (`AR/FAQ/General-Information/Copyright.md:9`); the EULA text names Datasec as "the Company" (`HP/Documents-Text/Portal-Attachments/EULA.txt:177`, sampled).

### 3.2 Document dates

Hosted deployment, printer deployment, HPAM user guide, the four M365 user guides and both Universal Print guides: revised 10 Nov 2026 (`HD:3`, `PD:3`, `AMUG:3`, `S1 §1`, `S2 §1`). Disable public client flows: 13 Nov 2026 (`DPF:4`). Reader configuration: 24 Sep 2026 (`RDR:3`). Secret update: 17 Apr 2026 (`SEC:3`). Conditional Access guide: 13 Apr 2026 (`CA:4`). Mobile guides: 7 Oct 2026 (`S3 §1`). Workpath whitepaper: version 10.0, September 2024 (`WP:964`). Legacy NFR guide: April 2025 (`LEGF:4`); legacy BYO guide: copyright 2023 (`LEGB:20`).

## 4. Findings

### 4.1 HP Authentication Manager: the sign-in hub

**Role.** Primary sign-in application of the device; provides the Entra session to the five apps with no second sign-in; also does licence checks, produces printer activity logs and services Universal Print Direct, Secure and Pull jobs (`HD:87-90`). It does not support other HP or third-party apps, HP Single Sign-On or HP ID apps (`AMUG:71`), with one hedge: applications that can use "the HP Printer Signed in Device feature" may work (`HD:221-224`). (inferred) HPAM therefore establishes a device-level signed-in user, not only a private token.

**Entry points** (`AMUG:125-139`):

| # | What the user does | What happens |
|---|---|---|
| 1 | Taps any suite app tile | The app detects whether a sign-in exists; if not, HPAM's sign-in starts, then the chosen app opens |
| 2 | Presses **Sign in** on the console | QR screen; after sign-in the user picks an app |
| 3 | Taps the HPAM icon | Main screen with the QR code, or a login screen when SignalR is not configured (`PD:179-181,188`) |
| 4 | Taps an NFC card on the reader, at any time | Sign-in starts |
| 5 | Uses the phone over BLE, at any time | Sign-in starts |

Which of these exist depends on commissioning (`AMUG:125-126`). Card-only sites are told not to launch HPAM from the console, and to set the printer's default sign-in page (kiosk) so a card tap is required before any app can be launched (`KNOWN:80-82`).

**Sign-in journey, known credential** (`AMUG:142-171`, `176-201`, `207-235`):

1. Credential arrives: QR scan relayed from the phone, card ID from the reader, or BLE ID from the reader.
2. HPAM recognises the ID and starts the Microsoft sign-in for the associated user (`AMUG:159`; `S3 §6c`).
3. MFA mode (default): the console shows a two-digit number; the user enters it in Microsoft Authenticator (`AMUG:164-165`). No-MFA mode: the Authenticator step is skipped (`AMUG:165`).
4. The console shows the user as signed in (name format per configuration, §4.1 settings) and the suite apps are available (`AMUG:171`).

**First use, self-registration** (`AMUG:154-156`, `187-189`, `219-222`; `V05:17-22`, auto-captions):

1. Unknown ID is presented; the registration flow starts automatically.
2. The user is asked for a username; no password where the tenant is passwordless (`V05:18-19`, auto-caption).
3. The user completes the Authenticator number match (`V05:19-20`, auto-caption).
4. The console shows "Please wait while we register your new Card/BLE/QRCode ID" and, for the phone, a second Authenticator push confirms binding the ID (`S3 §4a`).
5. The ID is written to the user's Custom Security Attributes; the user is signed in (`CSA:99-101`).

A Microsoft sign-in is always required at enrolment, including in No-MFA mode, whatever the tenant's method: username + password, + OTP, or + Authenticator push (`HD:111-121`). Username/password, OTP, email code and SMS are supported but discouraged (`HD:106-110`). Third-party identity providers and MFA (Duo, PingID, Okta) are not supported (`HD:100-101`, `COMMON:23-26`).

**Sign out.** Tap **Sign Out** at the console, or tap the card on the reader again (`AMUG:250`); BLE again also signs out (`S2 §6.4`). Exiting an app does not sign out; the device's automatic timeout is the backstop (`AMUG:242-248`).

**Tokens** (`TOKENS:11-57`):

| Behaviour | Source |
|---|---|
| Interactive sign-in is the authorisation-code flow with PKCE against Entra (the article says "OAuth 2.1"), requesting `offline_access` | `TOKENS:11` |
| HPAM stores the user's refresh token in Custom Security Attributes (V4) or Keycloak (legacy) | `TOKENS:17` |
| Access token expiry during a session: silent refresh; the stored refresh token is replaced when Entra rotates it | `TOKENS:17` |
| No-MFA mode: the stored refresh token is redeemed for a new access token; no interactive step | `TOKENS:19` |
| Refresh tokens last 90 days, renewed on each use | `TOKENS:27` |
| Silent refresh rejected (expired, revoked, policy): fall back to interactive login | `TOKENS:32` |
| Admin can force re-authentication by removing or changing the stored ("encrypted") token, tightening Conditional Access, or resetting password/sessions; card IDs survive | `TOKENS:36-42` |
| Removing card IDs forces re-registration | `TOKENS:44` |
| Universal Print Pull does not use the user token; it has its own device tokens | `TOKENS:51` |
| Entra sign-in log shows error 50199 followed one second later by success: HPAM tries silent acquisition first, then interactive; documented as normal | `E50199:13-15,56-100` |

**Custom Security Attributes** (`CSA:17,99-121`, `HD:684-775`):

- The service principal of the "HP Authentication Manager" enterprise app is assigned two Entra roles: **Attribute Assignment Administrator** and **Attribute Definition Administrator** (`HD:698-726`, `745-762`). (inferred) The second lets the app create its own attribute set and definitions on first run; the docs give no attribute-set or attribute names.
- The app writes the card ID "on the user's behalf after the user successfully completes" authentication (`CSA:99`), re-creates a missing value at next login (`CSA:113`), and is "coded to interact only with the correct, designated attribute set" (`CSA:111`).
- Optionally a trusted person gets Attribute Assignment Administrator to view and delete card IDs for lost or reused cards (`HD:736-740`); the CSA article advises against giving it to a human (`CSA:107-111`). The two documents pull in opposite directions.
- Attribute sets can be deactivated but never deleted (`CSA:84`).

**Configuration settings** (HP Command Center > HP Authentication manager > Configure; `PD:89-159`):

| Group | Setting | Value, default | Source |
|---|---|---|---|
| Connection Options | Tenant ID | customer directory id | `PD:95` |
| | App Registration Client ID | | `PD:100` |
| | Enable Microsoft Entra Custom Security Attributes | on for V4 self-hosted | `PD:106` |
| | App Registration Secret | the secret *value* | `PD:111` |
| | SignalR Endpoint URL | optional; must end `.azurewebsites.net` | `PD:116`, `S3 §6b` |
| Device Options | Console user name | default First Name + Last Name; or Email, UPN, Display Name | `PD:121-124` |
| Security Options | Enable Microsoft MFA/2FA/Passwordless Mode | default enabled; unticking gives No-MFA | `PD:129-138` |
| Reporting | Reporting Connection String | optional | `PD:144-145` |
| Microsoft Cloud Sovereignty | Cloud environment | Commercial (default), GCC, GCC High, DoD, Custom; endpoints mapped automatically | `PD:150-154`, `HD:802-811` |
| Info / diagnostics (V4.4) | Extended debug logging; additional sign-in scopes; card emulation | off (inferred) | `NEW:65-91` |
| Special MOC only | "Use confidential client authentication" | for registrations with public client flows disabled | `DPF:112-113` |

Legacy (Datasec-hosted) configuration used different fields: Base URL, API Key, AppCentre Key (Logs), Token URL, Auth URL, Client ID, Device Options (`LEGF:116-128`). `ERR:104` still refers to a "Printer License settings AuthURL".

Configuration values with leading or trailing spaces produce error codes (`PD:181-183`). Reboot after all apps and configurations are applied (`PD:202`).

**Card emulation (V4.4).** An administrator creates a 4 to 6 character alphanumeric card ID, registers it in Entra and tests sign-in and registration with no reader (`NEW:79-91`).

**Panel size.** QR originally needed an 8-inch or larger panel (`QR:25`); 4.3-inch support was promised for the September 2025 release (`QR:27`) and "as of October 2025" 4.3-inch devices are supported for Universal Print, Pull and Direct only, not for Mailflow (`TIPS:23-25`).

### 4.2 Readers and credentials

**Mechanism.** Readers output keystrokes over HID, emulating a keyboard (`RDR:66-67`). Card value: up to 32 characters, hexadecimal or decimal, hexadecimal recommended (`RDR:58-59`). Every reader in a fleet must output the identical ID or users register once per reader type (`RDR:91-93`). The developers key on USB VID and PID (`READERS:13`).

**Card technologies.** ISO 14443A CSN 32/56-bit, MIFARE Classic CSN, MIFARE DESFire CSN (`RDR:43-47`); static-ID fobs such as some YubiKeys (`RDR:69`); CypherCard biometric card, which reveals its ID only after the on-card fingerprint match (`READERS:23`). Not supported: FIDO, FIDO2 HID, U2F on HP printers (`RDR:71`); BLE protocols of other vendors (`RDR:56`).

**Certified readers** (`READERS:59-115`, `RDR:247-287`):

| Reader | VID:PID (hex) | ISO 14443A | BLE (HP Secure Authentication) | CypherCard |
|---|---|---|---|---|
| RFIDeas WAVE ID PcProx Plus BLE / WAVE ID Mobile, RDR-30581BKU | 0C27:3BFA | yes | yes | no |
| RFIDeas WAVE ID SP Plus Keyboard RDR-805H1AKU; RDR-30Mx1CxU-MXS-HP | 0C27:3BFA | yes | no | no |
| HP MFP24 Universal Card Reader X3D03A / X3D03B | 03F0:0045 | yes, as a keystroke reader after factory reset (`RDR:61-63`) | untested on X3D03B (`RDR:204`) | no |
| HP HIP2 Keystroke Reader Y7C05A / Y7C05B / 35H11A | 0C27:3BFA | yes | no | no |
| HP HIP2 Keystroke Reader 35H11B | 0C27:3BFA | yes | yes | no |
| Elatec TWN4 Slim (not Nano) | 09D8:0410 | yes | yes | yes |
| Inepro Spider | 1DA6:0110 | yes | no (only with Inepro's own app) | yes |
| HID Omnikey 5427 | 076B:0428 as hex; the decimal PID printed beside it does not match (`READERS:115`) | yes | no | no |

Four different products share 0C27:3BFA, so VID/PID does not tell a BLE-capable reader from a card-only one.

**Reader programming** (administrator, off the printer): RFIDeas Configuration Utility 6.0.9+, only "Send ID as hexadecimal number" active, "Disable Keystroke for SDK" off (`RDR:108-134`, `READERS:119-121`); Elatec AppBlaster 5.x, CypherCard = ISO 14443A UID 56 bits hex auto, BLE = Mobile Badge BLE transponder hex auto length, wallet-waking options disabled (`RDR:142-160`); older TWN4 without "/B" in the version string need DevPack 490 and Datasec's four project files (`ELATEC:11-37`); Inepro Spider tool 2.14.24 with Datasec's configuration file (`RDR:219-240`); HP Card Reader Configuration Utility for 35H11A and X3D03 (`RDR:178-199`).

Two interference warnings matter to an OXPd port: the HP-Elatec Reader Management tool reconfigures a reader over TCP/IP through the printer only when HPAM is not installed, otherwise it breaks HPAM (`RDR:168-170`); and the X3D03 reader should not be programmed "using OXPD" while HPAM is installed (`RDR:201-202`). (inferred) HPAM claims the reader exclusively on the device.

**CypherCard.** Up to two fingerprints per card, enrolled with the third-party SentryCard Enroll phone app (`CYPHER:11-16`); production cards are single-owner, visitor cards can be erased with special Elatec firmware and need a customer enrol code (`CYPHER:28-36`).

**Lifecycle.** Enrol by first tap (§4.1). Revoke by deleting the ID from the user's attributes (`HD:736-740`); in the legacy hosted mode Datasec clears all of a user's IDs on request because it cannot tell them apart (`CARDFAIL:23`).

### 4.3 HP Secure Authentication (mobile app) and its Intune edition

Full detail in `S3`; the behaviour a rebuild needs:

**What it is.** A mobile badge: it gives the phone a unique ID bound to the user's Microsoft account, usable by QR scan or over BLE (`S3 §2`). Free; iOS and Android; no supported OS versions are documented (`S3 §1`). (inferred, S3) Built with Flutter.

**Badge ID.** "A unique set of 16 digits" specific to phone and Microsoft user name, hashed; QR and BLE use the same ID; a second phone creates a second set (`S3 §5`). The hashing scheme is not documented.

**First-run registration, standard edition** (`S3 §4a`): Get started → allow camera "while using the app" → at the printer tap the HPAM icon → scan the QR with the app (never the phone's camera app) → sign in to Microsoft on the phone → number match → console shows the registering message → second Authenticator push binds the ID → signed in at the printer. **Intune edition** (`S3 §4b`): Get started launches Microsoft Authenticator as broker first; the user picks the work account, grants camera, may set an Intune app PIN, then scans.

**QR sign-in, both sides** (`S3 §6`, `QR:13-21`, `SIGNALR:9,19`):

| Step | Printer | Phone |
|---|---|---|
| 1 | On Sign in, HPAM icon or a suite app tile, generates a QR holding a random hashed key-pair name and "secret", one-time, valid only while displayed; also site/region settings | — |
| 2 | Has obtained a token from the Function App gateway and holds a SignalR connection | Opens the app; rear camera scans automatically |
| 3 | Receives the badge ID through SignalR, confirms it, starts the Microsoft login for that user | Has obtained its own token from the gateway and sent the scan result |
| 4 | Shows the number-match digits | User approves in Authenticator (biometric + digits) |
| 5 | Signed in | — |

The message names, payloads and QR lifetime in seconds are not documented.

**BLE sign-in** (`S3 §7`): no pairing; the app transmits the badge ID to a certified BLE reader; the reader beeps and the printer treats the value as a card read (inferred: via the same HID path). Opening the app near the reader can start it automatically; a **Bluetooth Reader** button retries. BLE is off by default and after a reset. Range is a slider from very close to far, default about 200 mm; far can reach 10 m and sign the user in at, or another user out of, a neighbouring printer.

**Settings** (`S3 §8`): QR scanner on/off; Bluetooth Reader on/off; reader type Elatec or RFIDeas; connection distance; app unlock by biometric or PIN; Site Settings (read-only); Reset App Defaults.

**Intune edition** (`S3 §9`): prerequisites HPAM V4.2.1+, SignalR, Authenticator, Company Portal on Android, Intune licences. App registration gains one delegated permission and two platform redirect entries (§4.8). Seven case-sensitive app-configuration keys, one policy per platform: `CloseAppOnInactivityTimeoutSeconds`, `QRCode` (0 user choice / 1 on and locked / 2 off and locked), `BLE` (same; if 2 then `QRCode` must be 0 or 1), `BleReaderType`, `BleConnectionDistance_Android`, `BleConnectionDistance_iOS` (20 to 100), `BleLockType` (0/1). No tenant id or secret is carried in these keys.

**Region binding (legacy mode).** The app stores the API and Keycloak server of the printer it registered at; moving between regions means reset and re-register (`REGIONS:23-25`, `QR:21`).

**Errors** (`S3 §12`): `BC01` (cannot reach the BLE reader), `SRS` (self-hosted SignalR offline, secret expired or endpoint wrong), "We are sorry - Invalid request" and "Unexpected error when authenticating" (legacy Keycloak redirect or secret problems), `DioException` host lookup failure (phone network blocks the back end).

### 4.4 The four Microsoft 365 apps

Full detail in `S1`. Common rules: Workpath apps that depend on HPAM; launching one while signed out triggers the HPAM sign-in then opens the app; exit keeps the session (`S1 §2.3, §2.4`).

**Scan** (`S1 §2.5-2.7`). Options: file type and resolution (75 to 600 DPI), original sides, colour/grey/black, original size (default Letter), orientation, image adjustment (sharpness, darkness, contrast, background clean-up), optimise text/picture, crop (default do not crop), blank page suppression (default off), multi-feed detection (default off), document separation by page count (not in the Teams manual). Formats: JPEG, PDF, PDF/A, TIFF, MTIFF, XPS; OCR outputs on supporting printers: searchable PDF and PDF/A, CSV, HTML, RTF, Text, Unicode Text; PDF encryption and compression are model-dependent. Default file type is JPEG, one file per page; administrators normally preset PDF. File name: typed, or automatic `Scan_<date>_<time>` (the manuals print `MMDDYYY`); V4.4 shows the default extension in the name field (`NEW:128`). Preview is optional in the storage apps and always shown in Mailflow; pages can be removed, rescanned or added before **Start**.

**Print** (`S1 §3.3, §4.3, §5.3, §6.3`, `NEW:112,129`). Options differ per manual: Mailflow has sides, colour, paper size/tray, copies; OneDrive and SharePoint have sides, paper, collate and page range; Teams has sides, colour, paper. Page-range printing is listed as new in V4.4 for all four apps and Universal Print (`NEW:112,129,152,168,181`). Staples must be chosen at the console (`KNOWN:299`); no fold options (`KNOWN:298`).

| App | Journeys documented | App-specific limits |
|---|---|---|
| Mailflow | new mail with scans (To/CC/BCC with directory auto-complete, subject, message, attach, **SEND EMAIL** or **SAVE DRAFT**); **ATTACH SCANS AND REPLY** on a selected mail; scan to a new or existing draft; print a mail and its attachments from the attachments panel; refresh; type-ahead search | Printable: mail body, DOC, DOCX, PPT, PPTX, XLS, XLSX, PDF, TXT. Admin preset "Max File Attachment Size" (no number given). Not supported on 4.3-inch or smaller panels (`S1 §3`) |
| OneDrive | browse folders; scan to folder; optional "Send to Email" through the printer's own SMTP scan-to-email (default disabled); print (tap, multi-select by long press, swipe to print); rename; delete; create folder; search; tile/list view; refresh; sort ascending/descending in V4.4 (`NEW:127`) | RTF/CSV/HTML OCR zip files and XPS do not print. Shared links and folders are not shown; "Shared with me" removed in V4.4 because Microsoft deprecated the Graph call (`NEW:135`, `KNOWN:143-151`) |
| SharePoint | pick site → library → folder; scan with entry of the library's metadata fields; optional Send to Email; print; multi-select print/delete; create/rename/delete files and folders; sort by name, modified, size; search; view; refresh | At most 4 custom index fields; mandatory fields not made obvious; fix "scheduled for next release 2027" (`KNOWN:153-160`) |
| Teams | pick Teams folder destination; scan with optional "Send a message to a channel in Teams" and message text; print; multi-select; rename/delete documents and folders; create folder; search; view | Manual pages 12 to 16 carry no text (`S1 §0`) |

**Rendering and size limits found outside the manuals.** DOCX is converted to PDF by Microsoft Graph for printing, with a hard timeout of about 45 seconds; complex documents fail (`KNOWN:200-210`). TIFF/MTIFF print since V4.2 but large MTIFF may exceed printer memory and has no preview (`KNOWN:186-198`). Password-protected PDFs print since V4.2.1; Purview-labelled documents are "still under review" (`KNOWN:131-139`).

**Administrator presets** (`S1 §2.8`): pushed fleet-wide from HP Command Center, or set per printer by signing in with the device's Administrator Access Code and opening the app, which then shows Default Scan Options, Default Print Options, and (Mailflow) Default Microsoft Options or (OneDrive, SharePoint) Default Send to Email Options. The contents of these pages are screenshots only.

**Errors** (`S1 §9`): Mailflow `MF01` (cannot load printer features), `MF02` (cannot obtain the HP Workpath attestation token), `MF03` (cannot reach Outlook services; usually Conditional Access); "You do not have permissions to perform this operation" in all four (consent missing or Conditional Access); OneDrive "Folder does not exist" (Conditional Access); `AADSTS530021` (approved-client-app policy rejecting the refresh token).

### 4.5 Universal Print

Full detail in `S2`.

**Registration model.** One device registers up to three Universal Print printers, named `<registration name>_Secure`, `_Direct`, `_Pull` (`S2 §4.1`). At registration the printer obtains a certificate from Azure; lifetime 10 years; no renewal process published by Microsoft; reinstalling yields a new one (`UPCERT:9-19`).

**Three ways to register** (`S2 §4.2-4.4`):

1. At the panel (Commercial cloud only): sign in with the Administrator Access Code → open Universal Print → tick services → **Proceed** → a code appears → complete the Microsoft device-code sign-in with an account that is Global Admin, or Application Administrator plus Printer Administrator, with a Universal Print licence → Approve → wait → share the printers in Azure.
2. Automatically from HP Command Center: configuration carries a dedicated account with a Universal Print licence, Printer Administrator role, MFA off and no MFA-enforcing Conditional Access; the printer registers itself within about 10 minutes; the account can be disabled afterwards. A Microsoft change to the device-code flow in October broke this until V4.4.1 (`KNOWN:15-21`, `NEW:199`).
3. Automatically through HP's "Workpath New deployment options" (Essential licence).

Tenant-wide admin consent to the enterprise app "Universal Print for HP Authentication Manager" is needed once in the Commercial cloud (`HD:606-616`); GCC, GCC High and DoD need the customer's own app registration (`HD:618-622`; the referenced "Universal Print App Registration for GCC.pdf" is not in the library). Sovereign-cloud settings cannot be made at the console (`NEW:188`). Since V4.2 a configuration push no longer re-registers printers (`KNOWN:272-284`).

**Queue behaviour** (`S2 §5`):

| Queue | At the device | Notes |
|---|---|---|
| `_Secure` | Sign in → open app → list of the user's jobs → tick one, several or All → preview → per job or for all selected: output sides, paper, colour mode, staples, booklet, hole punch, copies, page range (V4.4.1) → Print | Options shown depend on the device (mono, no finisher). Since V4.4.1 the list shows date/time and file size (`NEW:182`), except that file size is not available for `_Secure` and neither for Print Anywhere members (`KNOWN:288-289`) |
| `_Direct` | Nothing; prints "within a few minutes" | PIN-protected Direct jobs are released from the device's own Print from Storage menu |
| `_Pull` | Sign-in alone releases all pending jobs; no MFA challenge, no selection, no preview | With "Pull-Print Auto Release" on (per-user default): screen shows the job count, **Cancel Print Jobs** (also deletes them from the queue), **Remain Signed In**; no response → automatic sign-out while printing continues. With it off: a prompt at each sign-in |
| Print Anywhere | As Secure or Pull, at any member printer | Members are `_Secure` or `_Pull` registrations, kept in separate virtual queues and not shared themselves |

**Data path.** IPP on TCP 631 and "IPPS Printing" enabled in the embedded web server are required (`PORTS:68`, `UPNET:9`). A previewed-but-not-printed Print Anywhere Secure job used to be deleted on leaving the preview, explained as a limit of the IPP/Mopria standards (`KNOWN:290-296`). (inferred) The printer fetches the document from Universal Print as an IPP infrastructure printer, and a fetched job cannot be put back. `START-HERE.md:29` (from the old build's notes) says `_Secure` prints through the Workpath SDK and the other two through the printer's IPP port; the documentation neither confirms nor contradicts that.

**Limits and history** (`KNOWN:222-325`): jobs up to 1 GB since V4.2 (28 MB before); held jobs expire in Universal Print after 3 days (`S2 §11`, from an article that declares itself AI-generated); several large Pull jobs could exhaust printer memory before V4.2; mixed duplex settings in a multi-job release all took the console default before V4.2; "Black & White" as default prints colour on LaserJets, use Greyscale; no fold finishing; HP's built-in firmware Universal Print connector must not be registered alongside, except as a disaster-recovery direct printer (`S2 §2`).

**Reporting change in V4.4.1.** Toner colour values are now upper case (`BLACK`), which breaks older KQL scripts (`NEW:192-193`).

### 4.6 Administrator journeys

**A. Azure hosted deployment (V4, current)**, by a Global Administrator or equivalent (`HD:284-306`, `317-775`):

1. Create app registration "HP Authentication Manager": single tenant; redirect URI of type Public client/native, `com.hp.hpauthenticationmanager://oauth2redirect` (`HD:344-350`).
2. Add a client secret; record the value (not the secret ID) and the expiry; at most 2 years suggested (`HD:379-402`). Record client ID and tenant ID (`HD:408-411`).
3. Optional, for QR/BLE: set the Application ID URI to the default `api://…` value and add scope `SignalR.Access`, admins-only consent, display name "Access SignalR" (`HD:417-451`).
4. Add delegated Graph permissions (§4.8) and grant admin consent (`HD:563-601`).
5. Consent to the Universal Print enterprise app through Datasec's link (`HD:606-616`).
6. Optional: deploy "HP Authentication Suite Onboarding Azure Services" from Azure Marketplace; note its outputs: Reporting Connection String, SignalR Endpoint URL, Tenant ID (`HD:628-646`). PowerShell or Bash scripts are an alternative (`PREREQ:21`).
7. Assign the enterprise app to Attribute Assignment Administrator and Attribute Definition Administrator (`HD:684-768`).
8. Hand five values to the installer: tenant ID, client ID, secret value, SignalR endpoint, reporting connection string (`HD:651-661`, `790-794`).
9. Send Datasec the tenant ID and a purchase order (device count, term of 1 to 5 years) for licence activation (`HD:276-279`).

Roles for step 6: subscription Owner or Contributor; resource providers Microsoft.Web, Storage, Monitor, Insights, SignalRService, ContainerInstance, Authorization must be registered (`ROLES:19,67-81`).

**B. Printer deployment**, normally by the HP reseller (`PD:68-203`): install HPAM from HP Command Center (policy recommended) or with HP's newer command-line/"Workpath New deployment options" tools, which need an HP Workpath Essential licence (`HD:155`, `PD:77-78`); push the configuration (§4.1); set the device inactivity timeout to 300 seconds for the enrolment period, then back to about 60 (`PD:166-172`); test by tapping the HPAM icon; install and configure the other apps; reboot. Pre-checks for installers: date, time and time zone; printer claimed and synchronised in Command Center within 2 days; Workpath enabled (some models need an extra DIMM); no other sign-in application (`COMMON:116-132`).

**C. Secret rotation** (`SEC:23-114`): create a new secret → in the resource group, open the Function App → Settings → Environment variables → set `MICROSOFT_PROVIDER_AUTHENTICATION_SECRET` → Apply → Restart → push the new secret to every printer through HP Command Center. Symptoms of an expired secret: AI08/AI09 and no QR (`ERR:82,94`). Legacy sites email the new secret to Datasec instead and change nothing on printers (`FORGOT:13-25`, `SECUPD:23-35`).

**D. Disable public client flows** (`DPF:38-113`): add a Web redirect URI `http://localhost` → switch off "Allow public client flows" → request a special MOC file from Datasec → redeploy HPAM with "Use confidential client authentication" enabled. Supported only for manual Workpath installs, not for HP Command Center installs (`DPF:83-85`). Purpose: allow stricter Conditional Access on the app (`DPF:22-27`).

**E. Conditional Access.** The Conditional Access guide states on its first page that it was produced by AI and may not be fully accurate (`CA:6`); treat everything cited from `CA` as unverified. Claims: printers cannot enrol in Intune, so "require compliant device", "require approved client app" and "require app protection policy" always fail (`CA:35-49,145-160`); the embedded browser often identifies as Android (`CA:53-55`); blocks surface as OneDrive "Folder does not exist", SharePoint "You do not have permissions", Mailflow MF03 (`CA:121-129`). Remedies in its order: exclude the HP Authentication enterprise app from the restrictive policies; exclude accounts; exclude the platform; exclude trusted printer subnets (`CA:275-385`). The human-written articles support the device-compliance and Android points (`COMMON:103-108`) and the symptom list (`CATIPS:11`). The guide's second remedy speaks of printer "service accounts" (`CA:313-315`), which do not exist in this product: sign-in is by the end user.

**F. Passwordless setup** is the customer's job; test at `office.com` with username only, expecting the Authenticator prompt (`COMMON:44-58`, `PWLESS:13-19`).

**G. Legacy "API/Keycloak Hosted Services" deployment** (`LEGC`, `LEGB`, `LEGF`; pre-V4 and still offered to customers content to have a third party hold card and login data, `LEGC:84-87`):

1. Customer creates the same app registration and secret (`LEGC:263-304`).
2. Customer fills an encrypted PDF form with secret expiry, registration name, client ID, secret value and the OpenID Connect metadata URL, and emails it to Datasec (`LEGC:205-212,319-338`).
3. Customer applies the same Graph permissions and Universal Print consent (`LEGC:344-489`).
4. Datasec returns, within 1 to 2 working days, further values to finish the registration (a Web redirect to the regional Keycloak realm, per `S3 §10`) and the printer configuration values (`LEGC:496-500`). "Set 2 of 2" of these instructions is not in the library.
5. Datasec hosts API, databases and Keycloak in one chosen Azure region per customer: Australia East, USA East, EU West (`LEGC:219-229`), plus Singapore in the NFR guide (`LEGB:217-220`). Printer Regions let a customer split a fleet by region, at the cost of re-registering phones when users travel (`REGIONS:11-27`). Datasec's API is used only to start a sign-in (`REGIONS:11`).
6. NFR/demo variant: a Datasec-owned demo tenant with issued accounts and fixed configuration values (`LEGF:18-34,116-128`).

Migration from legacy to self-hosted is mentioned ("decided to Migrate and or install New HP Authsuite V4", `FORGOT:33`) but no migration procedure is documented.

**H. Upgrades** (`UPGRADE:18-64`): read release notes and known issues, agree a statement of work and rollback plan, check the printer synchronised with Command Center within 2 days, upgrade one printer, test with one or two users for one to two days, then the rest; in policies choose "App Only" or "App and Configuration" with care for Universal Print.

**I. Diagnostics.** Application data logs exported through the embedded web server (how-to is a video not in the library); wait about 15 minutes after a crash before producing a JDP log (`DIAG:11-15`, `COMMON:172`); extended debug logging in HPAM V4.4 (`NEW:71-73`); HP's network test tools (`PORTS:24`, `SYNC:37`).

### 4.7 Customer-side Azure architecture

| Resource | Hosted by | Purpose | Data at rest | Source |
|---|---|---|---|---|
| Entra tenant: app registration + enterprise app "HP Authentication Manager" | customer | OAuth client for panel and phone; service principal that writes attributes | client secret | `HD:344-411` |
| Entra user objects: Custom Security Attributes | customer | card, BLE and QR IDs; the user's refresh token; "other user specific custom values" | credential IDs, refresh tokens | `CSA:17`, `TOKENS:17` |
| Azure SignalR Service | customer (optional) | real-time channel between console and phone for QR sign-in and phone registration | none documented | `HD:244-246`, `SIGNALR:9` |
| Azure Function App (Flex Consumption) | customer (optional) | "authentication gateway": HPAM and the phone app get a token from it before connecting to SignalR; holds the app secret in an environment variable | app secret | `HD:248-251`, `SEC:94` |
| Storage account (Blob) | customer | Function code; Log Analytics query history; under 100 MB | code, saved queries | `HD:261-267`, `LA:22` |
| Log Analytics workspace with data collection endpoint and rule | customer (optional) | printer activity logs: tables `HpamPrinterLogs_StatisticJobData_CL` (print, scan, copy, fax, licence events) and `HpamPrinterLogs_Supply_CL` (toner percentage per device); three free KQL scripts | usage logs | `HD:663-678`, `LOSTLA:13-25` |
| Microsoft Graph, Universal Print | Microsoft | mail, files, Teams, print queues | — | `HD:466-470` |
| Datasec licence server, Australia East | Datasec | licence activation keyed on tenant ID | tenant ID, device count, term | `HD:276-279` |
| HP Command Center, App Center, attestation/token, Web Services | HP (AWS US, Frankfurt for Command Center) | app distribution, configuration, app whitelist renewal, attestation | device identifiers | `WP:152,522-534` |

The Reporting Connection String is a composite: the data collection endpoint's log-ingestion URL, a fixed stream name, and the data collection rule's immutable ID, joined with `@` (`LOSTLA:21-25`). The printers therefore post logs straight to the Azure Monitor ingestion API (inferred).

Data flows: panel browser → Entra sign-in; HPAM → Graph (attributes, organisation check, `ERR:37`); HPAM → Function App → SignalR; phone → Function App → SignalR; apps → Graph with the user's delegated token; Universal Print service ↔ printer; printer → Log Analytics; HPAM → licence server; device → HP cloud. All printer traffic is outbound (`WP:345-346`). Datasec states it needs only the tenant ID (`HD:276-281`).

### 4.8 Entra app registrations and permissions

**"HP Authentication Manager"** (single tenant). Redirects: public client/native custom scheme (`HD:347-350`); optional Web `http://localhost` for confidential-client mode (`DPF:56-61`); for the Intune phone app an iOS/macOS and an Android platform entry for `com.hp.secureauth.intune` (a signature hash is printed in the setup guide, `S3 §9b`); legacy mode adds a Web redirect to the regional Keycloak broker endpoint (`S3 §10`). Exposed scope: `SignalR.Access` (`HD:445-450`).

| Permission (delegated, Microsoft Graph unless noted) | Needed by | Reason as documented | Source |
|---|---|---|---|
| `openid` | all, mandatory | sign in with work account, basic profile | `HD:497-498` |
| `offline_access` | all, mandatory | keep access; "to allow for our NO-MFA Login Options" | `HD:500-502` |
| `email` | all, mandatory | read primary email address | `HD:504-505` |
| `profile` | all, mandatory | basic profile | `HD:507-508` |
| `User.Read` | SharePoint, OneDrive, Teams, Mailflow | read signed-in user's profile | `HD:519-521` |
| `Sites.ReadWrite.All` | SharePoint, OneDrive, Teams | edit or delete documents and list items in all site collections on behalf of the user | `HD:516-517,533-534` |
| `Files.ReadWrite.All` | Teams (listed there only) | read, create, update, delete files the user can access | `HD:540-541` |
| `ChannelMessage.Send` | Teams | send channel messages as the user | `HD:527-528` |
| `Channel.ReadBasic.All` | Teams | read channel names and descriptions | `HD:530-531` |
| `Team.ReadBasic.All` | Teams (in the 13-item list; no description block) | — | `HD:485` |
| `Mail.ReadWrite` | Mailflow | create, read, update, delete mail | `HD:545-546` |
| `Mail.Send` | Mailflow | send mail as the user | `HD:548-549` |
| `People.Read` | Mailflow | ranked list of relevant people (recipient auto-complete) | `HD:551-553` |
| `DeviceManagementManagedApps.ReadWrite` (Microsoft Mobile Application Management) | Intune phone app only | Intune app management | `S3 §9b` |

Thirteen Graph permissions cover the suite "excluding permissions required for Universal Print" (`HD:472-473`); only those for installed apps need be granted (`HD:492-494`). No document names the permission by which the service principal reads and writes Custom Security Attributes; the two directory roles are the only grant shown (inferred: the app authenticates as itself with the secret and relies on the roles).

**"Universal Print for HP Authentication Manager/Suite"** enterprise app: a Datasec-published multi-tenant application consented per tenant in the Commercial cloud (`HD:610-616`); its permissions are not listed anywhere in the documentation. Sovereign clouds: customer's own registration (`HD:618-622`).

Entra sign-in logs name the application "HP Authentication Manager – Azure Only" in one article (`E50199:49`), and another article says the usual registration name is "HP Authentication Suite" (`SECUPD:13`).

### 4.9 Network requirements

| Destination | Protocol / port | Who needs it | Source |
|---|---|---|---|
| Microsoft sign-in and Graph endpoints (Commercial, or sovereign set chosen in configuration) | HTTPS 443 | printer | `ERR:138`, `WP:822-844` |
| Customer Function App `*.azurewebsites.net` and SignalR `*.service.signalr.net` (or the AzureSignalR service tag, or regional ranges) | HTTPS 443 | printer and phone | `PORTS:74-92`, `S3 §13` |
| Azure Monitor ingestion endpoint of the customer's region | HTTPS 443 | printer | `LOSTLA:13-25` (inferred) |
| Datasec licence server (host name and address at `PORTS:70`) | HTTPS | printer | `PORTS:70` |
| `*.api.hp.com` (app attestation and token), `*.smartcloudprint.com` and `lookupsvc.smartcloudprint.com` (App Center, Command Center), `*.avatar.ext.hp.com` (HP Web Services), `*.id.hp.com` (HP Connect) | HTTPS 443; HTTP 80; UDP 9930 for signalling | printer, Workpath platform only | `PORTS:28-48,18`, `WP:657-693` |
| Universal Print | IPP, TCP 631; IPPS printing enabled on the device | printer | `PORTS:68`, `UPNET:9` |
| Legacy: Datasec regional API and Keycloak hosts | HTTPS 443 | printer and phone | `S3 §13` |

Signalling uses UDP 9930 first and HTTP 80 second, reversed when a web proxy is configured on the printer (`WP:165-167`); that is the only statement about proxies in the whole set. With V4.4 installed through the new deployment options, HP Web Services and the `*.hp.com` allow-list are no longer needed (`PORTS:20`). Certificates: nothing is documented about TLS trust or customer CA certificates for the suite; the whitepaper mentions a per-app private certificate store used by HP's Secure Access app only (`WP:506-515`). Firewall intrusion-detection rules can misclassify Azure traffic (`IDS:1-27`; the note reads as pasted AI chat output and carries no product facts). The printer clock matters: more than an hour of drift breaks HP cloud calls (`KNOWN:125`), and AI03 is a time/date error (`ERR:31`). DNS loss on firmware before 5.10.7 produced "Web Page Not Available / ERR NAME NOT RESOLVED" until reboot (`ERR:136-143`, `KNOWN:11`).

### 4.10 Security claims and the Workpath security model

**Suite claims.** Default sign-in is Entra passwordless with Authenticator number matching, described as phishing-resistant (`HPAMFAQ:17`). All Graph access is delegated to the signed-in user (`HD:469-470`). The QR code carries no user or client data (`QR:13`). Credential IDs are under the customer's control in their own tenant (`PD:33-36,45-47`). No-MFA mode is at the customer's risk: a lost unprotected card gives full access to the owner's mail and files, so biometric cards or app unlock are recommended (`HD:123-138`). Users must sign out (`AMUG:242-244`).

**What Workpath gives the existing apps** (`WP`), and so what a server-driven port does not inherit:

| Workpath mechanism | Statement | Source |
|---|---|---|
| Distribution | Apps are submitted to HP App Center, vetted, signed by HP (SHA-256) and whitelisted before they appear in the Command Center catalogue | `WP:132-135,316-319` |
| Whitelist renewal | Printer must stay connected to HP's cloud; unrenewed for 14 days → warning; 30 days → app disabled | `WP:200-210` |
| Platform off by default | Enabled per printer by an authorised administrator | `WP:596-598` |
| Settings | Changeable only by authenticated administrators | `WP:193` |
| Web view sign-in | Apps show a third-party authentication page in a web view | `WP:401-402` |
| Client secrets | Never in the app; held by App Center and used through an attestation and token proxy | `WP:404-419` |
| Data at rest | RSA + AES-256 hybrid or AES-256, for example cloud service tokens | `WP:337-341` |
| Network | All connections initiated by the printer, HTTPS/TLS 443; apps cannot use loopback; no executable download after install | `WP:345-346,567-568,592-593` |
| Device protections | SureStart, run-time intrusion detection, firmware whitelisting, secure boot, connection inspector | `WP:543-627` |
| Developer mode | Link Debug Bridge for unsigned apps, audited; disabling it removes all installed apps | `WP:576-588` |
| Hosting regions | App Center, HP ID, Web Services in AWS US; Command Center in AWS Frankfurt | `WP:522-534` |

The whitepaper lists HP's own apps ("HP for OneDrive Business", "HP Mail Flow", "HP for Universal Print", "HP for Microsoft Teams" and others) with their OAuth client IDs (`WP:756-804`) and required URLs (`WP:807-864`); it describes the platform and HP's apps, not Datasec's suite. The suite still depends on the HP attestation service: MF02 is "Unable to obtain HP Workpath Attestation token" (`S1 §9`) and "Unable to retrieve data from HP cloud services" comes from "a very small HP Service" the apps still rely on (`KNOWN:119`).

### 4.11 Supported devices, firmware, coexistence

- HP MFPs that are Workpath-capable and enabled; list on HP's developer site, not in the library (`FWVER:9`). Some models need an extra DIMM (`PREREQ:58`). Genuine HP consumables or no Workpath app installs (`FWVER:12`).
- Firmware statements, in conflict (see §6): 5.8.x to 5.10.0.7 (`FWVER:11`, `PREREQ:30`); 5.10.7 or above (`HD:153`); 5.10.0.7 or above for HP Advance integration (`ADVANCE:32`).
- No other login or authentication application may be installed: named examples EveryonePrint, HP Secure Access, HP ID; the printer must not be set to "Sign in Once" in Command Center (`PREREQ:60`, `TIPS:11`).
- HPAM can act as the authenticator, with MFA, for **HP Advance** and **LRS VPSX Print Release** once their own authentication modules are removed; integration requirements come from HP (`PREREQ:62`, `ADVANCE:9-39`). How those products consume the HPAM session is not documented.
- Tap-and-go from sleep was fixed in V4.2.1 (`NEW:104`): a card tap must wake the device.

### 4.12 Licensing and ordering

Sold and installed through HP Direct or an HP reseller using Command Center; also orderable on Azure Marketplace (apps alone, or bundled with a printer), still installed by an authorised installer (`LICENSE:11-33`). Activation: email customer name, tenant ID, HP order number, number of printers, term of 1 to 5 years; matched to the purchase order (`PD:51-62`). Proof of concept: free 20-day licence (`PD:64`). The licence is per printer and per term, keyed to the tenant (inferred from those fields). HPAM performs the licence check (`HD:89`); licence events appear in the reporting table (`HD:670`). No edition tiers within the suite are documented: customers install the apps they want. Microsoft-side: every user needs a Microsoft 365 licence, and a Universal Print licence for printing (`PREREQ:42-46`). Help-portal access for resellers is gated by an allow-list of company domains (`AR/FAQ/Trouble-Shooting-Guides/You-are-not-allowed-to-access-this-page-Help-Portal.md:13-15`).

### 4.13 Error and troubleshooting catalogue

| Code / message | Shown on | Meaning | Remedy | Source |
|---|---|---|---|---|
| AI01 | panel | check network connections and base URL values | re-check configuration; firewall and Conditional Access; reboot | `ERR:27,43-53` |
| AI02 | panel | invalid credentials or server error | as above; check the secret | `ERR:29,47` |
| AI03 | panel | check time and date | fix clock | `ERR:31` |
| AI04 | panel | server error, failed to obtain token | as AI01 | `ERR:33` |
| AI05 | panel | server error, failed to obtain config | as AI01 | `ERR:35` |
| AI06 | panel | "Graph Org Check failed: HTTP 401" | complete onboarding, notably attribute roles | `ERR:37,49` |
| AI07 | panel | no supported card reader detected (card-only printer) | fix or add a reader; consider QR as fallback | `ERR:57-66` |
| AI08 | panel | no card reader and/or SignalR unavailable | check SignalR, endpoint value, secret expiry | `ERR:68-82` |
| AI09 | panel | QR missing; tap card instead | as AI08 | `ERR:84-94` |
| AADSTS900023 | panel browser | tenant identifier invalid | check tenant/AuthURL setting | `ERR:100-104` |
| AADSTS700016 | panel browser | application not found | check client ID | `ERR:108-112` |
| AADSTS500113 | panel browser | no reply address registered | fix the redirect URI | `ERR:116-120` |
| HP Server / HP Token errors | panel | first launch, or HP cloud unreachable | retry, reboot, check ports | `ERR:124-134` |
| "Web Page Not Available" | panel browser | firmware DNS loss | reboot; firmware 5.10.7 | `ERR:136-143` |
| "This app will be disabled in X days" / "has been disabled" | panel | Workpath whitelist not renewed | reconnect to HP cloud | `WP:206-210` |
| Icons without app names after install | panel | — | reboot | `AR/FAQ/Trouble-Shooting-Guides/My-console-icons-do-not-have-the-application-name.md:9-11` |
| MF01, MF02, MF03; permission and folder messages; AADSTS530021 | panel | see §4.4 | | `S1 §9` |
| "Device registration required" | panel, Universal Print | printer not registered | register | `S2 §14` |
| BC01, SRS, Keycloak pages, DioException | phone | see §4.3 | | `S3 §12` |
| Sign-in log 50199 then success | Entra | normal silent-then-interactive pattern | none | `E50199:13-15` |

Older spellings AL01–AL09, A01–A06 and A101–A109 appear as search keywords for the same codes (`ERR:153-199`). Error screens carry a link to the help portal; before V4.2 such links let users browse the open internet from the panel (`KNOWN:367-373`, `NEW:95`).

### 4.14 Known issues (current) and what is new in V4.4

New in V4.4 / V4.4.1 (`NEW:55-199`): sovereign cloud setting (HPAM and Universal Print); extended debug logging; additional sign-in scopes for richer Entra logs; card emulation; page-range printing in all apps; OneDrive sort; default file extension shown in scan name; "Shared with me" removed; Universal Print list shows date/time and file size; toner values upper-case in reporting; automatic Universal Print registration fixed; error links can no longer browse the internet.

Still open as documented (`KNOWN`): DOCX conversion timeout (`:200-210`); Purview-labelled documents (`:139`); OneDrive shared content (`:143-151`); SharePoint index-field limits (`:153-160`); no fold options and console-only stapling (`:298-307`); monochrome default prints colour (`:319-325`); first-launch "Failed to get device token / Please enable HP Web Services / Unable to retrieve data from HP cloud services", "still under investigation" (`:438-446`); colour matching (`:427-433`). Firmware DNS loss is tied to firmware 5.10.7 (`:11`).

### 4.15 The HPAM-to-OXPd2 mappings in `HPAM/README.md`: SUGGESTIONS TO VERIFY, not facts

`ROOT:50` itself heads them "suggestions for the agent to verify against the specs", and `START-HERE.md:101` repeats the warning. None is established by any document in this lane.

| Existing behaviour | Suggested OXPd2 touchpoint | Source | What must be verified |
|---|---|---|---|
| Sign-in flows | `authentication` service; `authenticationServiceOverview.md`, `securityModel.md` | `ROOT:51` | whether an agent can run a browser-hosted Microsoft login, set the signed-in user and name, and end the session on a second card tap |
| Card and BLE readers | `usbAccessories` service (HID readers); forum thread on Y7C05 | `ROOT:52` | whether keystroke readers by VID/PID (§4.2) can be claimed, whether a tap wakes the device and arrives with no app open |
| On-device app UI | `application` service: access points, browser use model, runtime chrome, home screen | `ROOT:53` | tiles per app, launch while signed out, panel sizes, scan preview and page editing in a browser |
| Secure and pull release | `printJob` service; `pullPrintAuth` demo | `ROOT:54` | job submission with finishing attributes, capacity for 1 GB jobs, status back to Universal Print |
| Packaging and signing | `solutionManager`; Solution Packaging Utility | `ROOT:55` | — |

Not covered by the README's list, and needing a mapping: scanning with the full option set of §4.4; device capability discovery; device administrator sign-in detection; job statistics and supply levels for the reporting tables; PIN jobs in device storage; inactivity timeout control; delivery of configuration to a fleet.

## 5. What this means for the port

1. **Keep the Entra contract unchanged.** Same registration name, redirect, scopes and attribute storage (§4.7, §4.8) let a mixed fleet share one enrolment: a card registered at a Workpath printer signs in at an OXPd printer. This needs the attribute set, names and value encoding from the source lanes; the documentation gives none (§4.1).
2. **Move the secret to the server.** Today the client secret, which carries two directory roles over every user's attributes and stored refresh tokens, is typed into Command Center and stored on every printer (`PD:111`). In a server design the printers need not hold it (§8).
3. **The server becomes the Universal Print device.** Certificates, three registrations per printer, polling and Direct/Pull servicing all move server-side, then jobs go to the engine over the network (§4.5). Existing Workpath registrations of the same printer are separate objects; replacing Workpath with OXPd on a device means new registrations and re-pointing shares and Print Anywhere membership, since reinstalling yields a new certificate (`UPCERT:19`).
4. **The QR channel can be simplified but must stay compatible.** The phone app is shipped software: it expects the QR format, the Function App token endpoint and the SignalR conversation it has today (§4.3). Either the port's server joins the customer's existing SignalR as the "printer" party, or the phone app changes. The documented payload is too thin to choose (§7).
5. **Conditional Access will look different.** Today Entra sees an Android-like embedded browser on the printer's IP (`COMMON:106`). With a server making Graph calls, token redemption comes from the server's address, and location-based exemptions written for printer subnets (`CA:367-385`, AI-produced) will no longer match. The "exclude the enterprise app" remedy carries over.
6. **Dependencies that disappear:** HP Command Center, App Center whitelisting, attestation tokens (MF02, HP Server/Token errors), HP Web Services allow-lists, the 30-day whitelist expiry (§4.10). **Dependencies that appear:** a deployment and configuration channel replacing Command Center policies, per-app presets storage, a licence check on the server, and a log shipper that keeps the two Log Analytics tables and their column formats so customers' KQL reports survive (§4.5 reporting note).
7. **Device-bound behaviours to re-prove on OXPd** (checklist §9): card tap at any time including from sleep; second tap signs out; scan with preview and page editing; capability-dependent print options; PIN jobs from device storage; administrator access code opening an app's settings pages; 4.3-inch panels.
8. **Reusable as is:** the whole Azure back end, the mobile apps, the reader programming profiles, the help-portal error vocabulary (AI01–AI09, MF01–MF03), the deployment guide for the tenant side, the licensing process.
9. **Traps:** Graph DOCX conversion timeout; Universal Print job deleted after preview; mixed reader ID formats; BLE range crossing printers; reader tools that talk to the reader through the printer conflict with whoever owns the reader (`RDR:168-170,201-202`), which on OXPd will be the solution.

## 6. Contradictions and doubts

| # | Topic | Statements | Reading |
|---|---|---|---|
| 1 | Firmware range | 5.8.x–5.10.0.7 (`FWVER:11`); "5.10.7 or above" (`HD:153`); "5.8.x > 5..0.2" (`COMMON:128`, garbled); legacy 5.8.x–5.9.2.3 (`LEGC:137`); 5.10.7 "by approximately October 2026" (`KNOWN:11`) vs "due by Mid August 2026" (`KNOWN:101`) | "5.10.0.7" and "5.10.7" are probably the same build written two ways; unverified |
| 2 | Where the refresh token is used | used for silent refresh during a session and for No-MFA (`TOKENS:17-19`); "to support our NO-MFA scenario only" (`TOKENS:51`) | both in one article; code must settle |
| 3 | Who should hold the attribute role | assign a trusted person (`HD:736-740`); do not assign any human (`CSA:107-111`) | CSA article is newer advice |
| 4 | Workpath apps and client secrets | apps never have their client secrets (`WP:404-406`); HPAM is configured with the customer's secret value (`PD:111`) | the whitepaper describes HP's token-proxy apps; Datasec's V4 does not follow that model |
| 5 | Number of Graph permissions | 13 (`HD:472`); 8 (`LEGB:328`) | older count |
| 6 | Registration name | "HP Authentication Manager" (`HD:344`); "HP Authentication Suite" (`SECUPD:13`); log shows "HP Authentication Manager – Azure Only" (`E50199:49`) | customer-chosen; do not match on the name |
| 7 | Universal Print app name | "…for HP Authentication Manager" (`HD:611`) and "…for HP Authentication Suite" (`S2 §1`) | same app |
| 8 | Direct print latency | "immediately" (`G3:19`, videos) vs "within a few minutes" (`S2 §5.2`) | polling interval unknown |
| 9 | Where a Secure job waits | cloud (manuals) vs "at the printer" (auto-caption video) (`S2 §5.1`) | manuals win |
| 10 | 4.3-inch panels | not supported (`QR:25`); supported from Sept/Oct 2025 for print apps (`QR:27`, `TIPS:23`) | current V4.4: yes for Universal Print, no for Mailflow |
| 11 | Badge IDs per phone | QR and BLE share one ID; yet "four unique IDs" for two phones (`S3 §5`) | unresolved |
| 12 | Enrolment timeout | 300 s (`PD:166`); "Sleep Mode Set to 300" (`COMMON:120`); 120 s (`S3 §12`) | inactivity timeout is meant; value is advice, not enforced |
| 13 | Legacy regions | three (`LEGC:222-226`) vs four with Singapore (`LEGB:217-220`) | list grew |
| 14 | Print options per app | summary guide gives one common list (`G4:30-34`); manuals differ per app (`S1 §11`) | manuals may lag the apps; code decides |
| 15 | SignalR "required" for the phone app (`G2:11`) | required for QR; BLE goes through the reader (`S3 §15`); but first registration of a phone is by QR scan | BLE-only sites still need SignalR to enrol phones (inferred) |
| 16 | Omnikey PID | hex 428 vs decimal 21455 (`READERS:115`) | one is wrong |

Sources that declare or show unreliability: the Conditional Access guide (AI-produced, `CA:6`); the Universal Print retention article (AI-generated, per `S2 §11`); `IDS` (pasted chat answer); the video transcripts (auto-captions: "Enra", "fishing", "props card", `ROOT:10`); the `Apps/01–07` guides (second-hand summaries written at collection time, `HP/README.md:8`; `S1 §11`, `S2 §16` and `S3 §15` list where they overreach). Dates printed in the documents run to November 2026 and the articles carry no year in most "Modified" lines.

## 7. Questions for Kam or his team

| # | Question | Why it matters | Assumption if unanswered |
|---|---|---|---|
| 1 | Must credentials enrolled on Workpath printers work unchanged on OXPd printers in the same tenant (same attribute set, same ID encoding, same stored refresh token)? | Decides whether the port is bound to the existing attribute schema and token handling | Yes: one enrolment for a mixed fleet |
| 2 | Is the HP Secure Authentication phone app frozen for this project, so the OXPd server must speak today's QR, Function App and SignalR conversation, or may the app and the Marketplace back end change? | Sets the QR design and whether customers must redeploy Azure resources | Frozen: the server impersonates the printer side |
| 3 | Where does the OXPd server run for a customer: on their LAN, in their Azure subscription, or Datasec-hosted, and one per site or per tenant? | Changes Conditional Access exposure, Universal Print reachability to printers (IPPS on the LAN), licensing and the "customer hosts everything" claim | Customer-hosted, on a network that reaches the printers |
| 4 | Which of the five apps, and which Universal Print modes, are in scope for the first OXPd release, and is there really a sixth or seventh app? | The documentation shows five plus HPAM | All five; no others |
| 5 | Are legacy Keycloak-hosted customers in scope for OXPd, or V4 self-hosted only? | Doubles the sign-in back ends | V4 self-hosted only |
| 6 | Which Graph or Universal Print permissions does the Datasec multi-tenant Universal Print app hold, and can a server register printers under it? | Not documented anywhere | Reuse the same enterprise app |
| 7 | Which OXPd device families and panel sizes are targeted, and do the same certified readers attach to them? | Reader list and 4.3-inch limits are Workpath findings | Same readers; 8-inch panels first |
| 8 | Do HP Advance and LRS VPSX integrations have to work with the OXPd edition? | They consume the device sign-in, mechanism undocumented | Out of scope for release one |
| 9 | Is No-MFA mode to be carried over as is? | It stores long-lived refresh tokens for every user | Yes, same option, default off |
| 10 | How is the OXPd edition licensed: same per-printer licence and licence server, one licence across both platforms? | Licence check moves to the server | Same licence, checked by the server |
| 11 | Is "Set 2 of 2" of the legacy instructions, the GCC Universal Print registration guide, and the KQL script pack available? | Missing from the library; needed for the reporting schema and sovereign clouds | Take schemas from source code |

## 8. Secrets and sensitive items seen (locations only), and weaknesses not to carry over

Locations of sensitive values in the documentation (none reproduced here):

| Location | What is there |
|---|---|
| `M/Archive/V4 PDF/NFR Free Azure Tenant Deployment Instructions.txt:116-127` | a demo back-end base URL, an API key, an "AppCentre Key (Logs)", token and authorise URLs containing a tenant id, and a client id, all in clear |
| same file `:23-24,46,71,84` | the demo tenant's domain name |
| `M/Archive/V4 PDF/Customer HP Authentication Manager Deployment Instruction 1-2.txt:211` and `…/NFR BYO Azure Tenant Deployment Instructions 1-2.txt:208` | the password that unlocks the "secure" PDF form customers used to send their client secret to Datasec; the same password in both documents |
| `AR/FAQ/Trouble-Shooting-Guides/Entra-ID-Sign-In-Failure-50199.md:47-48` | a correlation id and session id from a real sign-in log |
| `AR/FAQ/Trouble-Shooting-Guides/I-lost-my-log-Analytics-report-connection-string-URL.md:29` | a full example reporting connection string (ingestion endpoint and rule id) |
| `HP/Apps/02-HP-Secure-Authentication-Mobile-App.md:43` and the Intune setup guide (`S3 §9b`) | Android signature hash of the Intune app (public platform value) |
| `WP:756-804` | OAuth client ids of HP's own Workpath apps (published by HP) |
| many articles | SharePoint share links with access tokens to Datasec's document library (for example `ERR:45,82`) |
| `HD:739` | a named example administrator account; S2 notes a presenter's name in a video transcript |
| `PORTS:70` | licence server address |

Weaknesses in the existing product, as the documentation shows them, that the port should not reproduce:

1. **Tenant secret on every device.** The app registration secret is entered in HP Command Center and delivered to each printer (`PD:111`); the same secret authenticates a service principal holding Attribute Assignment and Attribute Definition Administrator over the whole tenant (`HD:698-762`). Those roles are not scoped to the product's attribute set in the instructions; the CSA article itself warns that the role lets a holder alter other vendors' attributes (`CSA:109`). Anyone extracting the secret from a printer or from Command Center can read every user's stored credential IDs and refresh tokens (inferred from `TOKENS:17`; the article calls the stored token "encrypted", `TOKENS:38`, without saying with what key).
2. **Refresh tokens for all enrolled users stored in the directory**, for No-MFA and silent refresh (`TOKENS:17-19`), valid 90 days rolling (`TOKENS:27`).
3. **No-MFA mode turns a static card serial into the only factor** (`HD:131-135`); ISO 14443A serial numbers are readable and clonable, and the keystroke interface accepts any USB keyboard-like device typing the same characters (inferred from `RDR:66-67`).
4. **Card emulation** lets an administrator invent a 4 to 6 character credential on a production printer (`NEW:79-91`); nothing documents who may enable it or how it is audited.
5. **Auto-registration account for Universal Print**: a Printer Administrator account with MFA disabled and exempt from Conditional Access, with its password held in the Command Center configuration (`S2 §3`, `COMMON:140-158`).
6. **Secrets by email.** Legacy onboarding sends client secrets in a PDF whose password is printed in the instructions (rows 2 and 3 above), and secret rotation by email continues for hosted sites (`SECUPD:25-35`).
7. **Session left open.** Exit does not sign out, and the timeout is raised to 300 s during enrolment (`AMUG:242-248`, `PD:166-172`).
8. **Kiosk escape, fixed in V4.2**: error links opened the general internet in the panel browser (`KNOWN:367-373`). A browser-based OXPd UI must confine navigation from the start.
9. **Function App secret in a plain environment variable** (`SEC:94-100`), not a key vault reference.

## 9. Requirements checklist for the port

One line per behaviour. "Device" = needs something from the printer (panel UI, reader input, scan, print engine, identity, storage, timeout); "Server" = can live wholly off the device.

| # | Behaviour to reproduce | Bound to | Source |
|---|---|---|---|
| 1 | Tile per app on the home screen; launch while signed out starts sign-in, then opens the chosen app | Device (panel) | `AMUG:128-129` |
| 2 | Sign in button and HPAM tile show a QR sign-in screen | Device (panel) | `AMUG:131-134` |
| 3 | Card tap at any time starts sign-in, with no app open | Device (reader) | `AMUG:136` |
| 4 | Card tap wakes a sleeping device and signs in | Device (reader, power) | `NEW:104` |
| 5 | BLE reader input treated as a card read | Device (reader) | `S3 §7a` |
| 6 | Reader accepted as HID keystroke source; value up to 32 characters, hex or decimal | Device (reader) | `RDR:58-67` |
| 7 | Reader recognised by VID/PID for the certified list | Device (reader) | `READERS:13,59-115` |
| 8 | Missing reader detected and reported (AI07, AI08) | Device (reader) | `ERR:57-76` |
| 9 | Look up credential ID against the user's Custom Security Attributes | Server | `CSA:17,99` |
| 10 | Unknown ID starts self-registration with Microsoft sign-in, then writes the ID | Device (panel browser) + Server | `AMUG:187-189`, `CSA:99` |
| 11 | Console message while registering a new ID | Device (panel) | `S3 §4a` |
| 12 | Microsoft sign-in page shown on the panel; number-match digits displayed | Device (panel browser) | `AMUG:164`, `COMMON:32` |
| 13 | Authorisation-code flow with PKCE, `offline_access` | Server | `TOKENS:11` |
| 14 | Store and rotate the user's refresh token in Custom Security Attributes | Server | `TOKENS:17` |
| 15 | No-MFA mode: redeem stored refresh token, no interactive step; enrolment still interactive | Server | `TOKENS:19`, `HD:111-113` |
| 16 | Silent refresh during session; fall back to interactive when rejected | Server + Device (panel) | `TOKENS:17,32` |
| 17 | Username/password, OTP, SMS, email code sign-in work because the page is Microsoft's | Device (panel browser) | `HD:106-110` |
| 18 | Signed-in user's name shown on the console in the configured format | Device (panel) | `PD:121-124` |
| 19 | One session shared by all suite apps | Server (+ device session) | `HD:61-64` |
| 20 | Sign Out on console and in each app's ribbon ends access for all apps | Device (panel) | `AMUG:250`, `V05:23` (auto-caption) |
| 21 | Second card or BLE tap signs out | Device (reader) | `AMUG:250` |
| 22 | Exit from an app keeps the session | Device (panel) | `S1 §2.4` |
| 23 | Device inactivity timeout ends the session; configurable (60, 120, 300 s advice) | Device (timeout) | `PD:166-172` |
| 24 | Device-level signed-in state usable by other solutions (HP Advance, LRS VPSX) | Device (auth agent) | `HD:223`, `PREREQ:62` |
| 25 | No other authentication solution on the device | Device | `PREREQ:60` |
| 26 | QR generated per display: one-time random key-pair name and secret, plus site settings | Server (rendered on panel) | `QR:13-21` |
| 27 | Token from the Function App gateway, then SignalR connection awaiting the phone | Server | `SIGNALR:9,19` |
| 28 | QR missing or SignalR down reported (AI08, AI09) with card fallback | Server + Device (panel) | `ERR:68-94` |
| 29 | Phone registration by QR with second Authenticator confirmation | Server + phone | `S3 §4a` |
| 30 | QR usable on 8-inch panels; 4.3-inch for print apps | Device (panel size) | `QR:25-27`, `TIPS:23` |
| 31 | Card emulation for administrators (4–6 characters) | Server (admin UI) | `NEW:79-91` |
| 32 | Extended debug logging switch | Server | `NEW:71-73` |
| 33 | Additional sign-in scopes switch for Entra logs | Server | `NEW:75-77` |
| 34 | Sovereign cloud selection (Commercial, GCC, GCC High, DoD, Custom) | Server (config) | `PD:150-154` |
| 35 | Confidential-client mode when public flows are disabled | Server (config) | `DPF:38-113` |
| 36 | Configuration: tenant ID, client ID, secret, attribute switch, SignalR URL, name format, MFA switch, reporting string | Server (config) | `PD:89-159` |
| 37 | Fleet-wide configuration push and per-app presets | Server (deployment) | `PD:68-72`, `S1 §2.8` |
| 38 | Licence check keyed on tenant ID against Datasec's server; 20-day POC | Server | `PD:51-64`, `HD:89` |
| 39 | Printer activity logs to Log Analytics: jobs (print, scan, copy, fax, licence) | Device (job statistics) + Server | `HD:670` |
| 40 | Toner percentage per device to Log Analytics; upper-case colour names | Device (supplies) + Server | `HD:671`, `NEW:192` |
| 41 | Error screens link to the help portal without open browsing | Device (panel browser) | `PD:190`, `NEW:95` |
| 42 | English only | — | `LANG:9` |
| 43 | Device administrator access code sign-in opens an app's settings pages | Device (admin sign-in state) | `S1 §2.8` |
| 44 | Scan from glass or feeder with: sides, colour, size, orientation, resolution 75–600, image adjustment, optimise, crop, blank-page suppression, multi-feed detection | Device (scanner) | `S1 §2.5` |
| 45 | Scan formats JPEG, PDF, PDF/A, TIFF, MTIFF, XPS; OCR formats; PDF encryption; compression (model-dependent) | Device (scanner/OCR) | `S1 §2.5` |
| 46 | Document separation by page count | Device or Server | `S1 §2.5` |
| 47 | Scan preview with remove, rescan, add page, cancel job | Device (scanner + panel) | `S1 §2.7` |
| 48 | Automatic and typed file names; default extension shown | Server (panel UI) | `S1 §2.6`, `NEW:128` |
| 49 | Admin default scan and print options | Server (config) | `S1 §2.8` |
| 50 | Print stored documents with sides, colour, paper size/tray, collate, copies, page range | Device (print engine) | `S1 §3.3-6.3`, `NEW:112` |
| 51 | Print options limited to what the device supports | Device (capabilities) | `S2 §6.3` |
| 52 | Print preview of documents on the panel | Device (panel) + Server | `S1 §3.2` |
| 53 | Office documents converted to PDF through Graph before printing | Server | `KNOWN:202` |
| 54 | Password-protected PDF, TIFF and MTIFF printing | Device (print engine) | `KNOWN:131-137,186-198` |
| 55 | Mailflow: list mail and folders, search, refresh | Server (panel UI) | `S1 §3.3` |
| 56 | Mailflow: compose with To/CC/BCC auto-complete, subject, message, scanned attachments; send; save draft | Server + Device (scanner, keyboard) | `S1 §3.3` |
| 57 | Mailflow: reply with scans keeping the thread; edit existing draft | Server + Device (scanner) | `S1 §3.3` |
| 58 | Mailflow: print message and attachments; multi-select | Server + Device (print) | `S1 §3.3` |
| 59 | Mailflow: admin maximum attachment size | Server (config) | `S1 §2.8` |
| 60 | Mailflow: unsupported on 4.3-inch or smaller | Device (panel size) | `S1 §3.1` |
| 61 | OneDrive: browse, scan to folder, print, rename, delete, create folder, search, sort, tile/list | Server + Device (scan/print) | `S1 §4.3`, `NEW:127` |
| 62 | OneDrive/SharePoint: optional Send to Email through the device's SMTP scan-to-email, default off | Device (scan-to-email) | `S1 §4.3` |
| 63 | SharePoint: sites → libraries → folders; metadata entry at scan (4 custom fields) | Server (panel UI) | `S1 §5.3`, `KNOWN:155` |
| 64 | SharePoint: sort by name, modified, size; multi-select print and delete | Server (panel UI) | `S1 §5.3` |
| 65 | Teams: scan to a Teams folder with optional channel message; print; manage files and folders | Server + Device (scan/print) | `S1 §6.3` |
| 66 | App Guide tutorial at first launch; Information page with version and licences | Server (panel UI) | `S1 §2.9` |
| 67 | Permission and Conditional Access failures shown with the documented messages (MF03 and others) | Server (panel UI) | `S1 §9` |
| 68 | Universal Print: register a device as up to three printers with name suffixes | Server (holds identity) | `S2 §4.1` |
| 69 | Universal Print: registration at the panel with device-code display under device admin sign-in | Device (panel, admin state) + Server | `S2 §4.3` |
| 70 | Universal Print: unattended registration from configuration with a service account | Server | `S2 §4.4` |
| 71 | Universal Print: hold the Microsoft-issued certificate(s), 10-year life | Server (secure storage) | `UPCERT:9-15` |
| 72 | Universal Print: enable, disable and rename services; changes flow to Azure without re-registration | Server | `KNOWN:284`, `NEW:188` |
| 73 | `_Direct`: print with nobody at the panel within minutes | Device (print engine reachable) + Server | `S2 §5.2` |
| 74 | `_Direct` with PIN: job lands in device job storage, released from the device's own menu | Device (job storage) | `S2 §8` |
| 75 | `_Secure`: list the user's jobs with date/time and size; refresh | Server (panel UI) | `S2 §6`, `NEW:182` |
| 76 | `_Secure`: preview; select one, several or all; override sides, paper, colour, staples, booklet, hole punch, copies, page range; release | Server + Device (print engine, finisher) | `S2 §6.3` |
| 77 | `_Pull`: sign-in alone releases all jobs, with no MFA challenge | Device (reader event) + Server | `S2 §5.3` |
| 78 | `_Pull`: prompt with job count, Cancel Print Jobs (deletes from queue), Remain Signed In, timed auto sign-out | Device (panel, session end) + Server | `S2 §5.3` |
| 79 | `_Pull`: per-user "Auto Release" setting | Server | `S2 §9` |
| 80 | Print Anywhere: serve jobs of a virtual queue at any member printer; job status reported back as completed | Server + Device (job status) | `S2 §5.4`, `KNOWN:224-232` |
| 81 | Universal Print jobs up to 1 GB; engine memory limits respected | Device (print engine) | `KNOWN:234-244,260-270` |
| 82 | IPP 631 / IPPS enabled on the device for Universal Print output | Device (network service) | `PORTS:68`, `UPNET:9` |
| 83 | "Device registration required" message when unregistered | Server (panel UI) | `S2 §14` |
| 84 | Finishing: 5 staple positions, booklet, hole punch; no fold | Device (finisher) | `S2 §12` |
| 85 | Phone app: unchanged QR and BLE behaviour, settings, Intune keys | Phone (+ Server contract) | `S3 §6-9` |
| 86 | Secret rotation without touching printers (improvement over today) | Server | `SEC:23-28` |
| 87 | Outbound-only connectivity to Microsoft, customer Azure, licence server | Server (and device ↔ server on the LAN) | `WP:345-346`, `PORTS:68-92` |
| 88 | Clock accuracy checked and reported (AI03) | Server | `ERR:31` |
| 89 | Diagnostic log export for support | Server | `DIAG:11-15` |
| 90 | Coexistence with Workpath printers in the same tenant: same registration, same enrolments, same queues naming, same reporting tables | Server | §5 items 1, 3, 6 (inferred requirement from the brief) |
