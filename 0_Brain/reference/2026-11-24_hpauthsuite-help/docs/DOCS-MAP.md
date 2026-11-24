# DOCS-MAP: what the gated help-portal documents say against our open questions

Read 2026-11-24 (Tuesday seat, s321). Questions: `2_Project_Files/tuesday/briefs/2026-11-24_B2027_answers/JIRA-DRAFTS.md` (T-01 to T-29, pack ids W1 to W48). Documents: `DOCS-INDEX.md` in this folder; public-site account: `../MAP.md`. Status words: **ANSWERED** = a document states it; **PARTLY** = part stated, missing part named; **NOT IN THE DOCUMENTS** = no document states it (searched page images and text). Page = PDF page. Quotes copied from the page or screenshot.

File short names: AM-UG (Datasec-HP_Authentication_Manager_UG.pdf), SA-UG (Datasec-HP_Secure_Authentication_UG.pdf), SAI-UG (…_Intune_UG.pdf), SAI-SG (HP_Secure_Authentication_Manager_Intune_Setup_Guide.pdf), HOSTED (HP Authentication Manager Azure Hosted Deployment Instruction.pdf), PRINTER (… Azure Printer Deployment Instruction.pdf), SECRET (… App Registration Secret update Guide.pdf), PUBLIC-FLOWS (Disable-Public-Client-Flows.pdf), CA-GUIDE (Conditional Access General Support Information.pdf), READERS (Datasec - Reader_Configuration.pdf), FW (Firmware Update Best Practices v1.pdf), OD (Datasec-HP OneDrive UG.pdf), SP (Datasec-HP_SharePoint-UG.pdf), MF (Datasec - HP Mail Flow UG.pdf), TM (Datasec- HP Teams UG.pdf), UPD (Datasec-HP Universal Print Deployment and Setup Guide.pdf), UPU (Datasec-HP  Universal Print UG.pdf), ARCH-CUST / ARCH-BYO / ARCH-NFR (the three Archive/V4 PDFs), CA-FIX (Support/Condition_access_policy_Fix.mp4, frame f_NNN ≈ (NNN-1)×5 s).

Trust caution: these are Datasec's own customer guides, mostly dated Sept to Nov 2026, describing the shipped V4.4 product. They are statements, not measurements. CA-GUIDE says of itself "This Article was produced by AI, and may not be 100% Accurate" (p2).

## 1. Answered by the documents (the Jira ticket may be unnecessary)

- **W11 / T-08, Graph permissions: ANSWERED (as documented to customers).** HOSTED p17: "There are 13 Permissions: Which covers all HP Authentication Suite of apps, excluding permissions required for Universal Print." All Delegated: ChannelMessage.Send, email, Mail.ReadWrite, Mail.Send, offline_access, openid, People.Read, profile, Sites.ReadWrite.All, User.Read, Team.ReadBasic.All, Channel.ReadBasic.All, Files.ReadWrite.All; the p20 screenshot "Microsoft Graph (13)" shows them "Granted". Mandatory: openid, offline_access, email, profile; offline_access: "We use this permission to allow for our NO-MFA Login Options" (p17). Per app (p18): SharePoint & OneDrive Sites.ReadWrite.All, User.Read; Teams ChannelMessage.Send, Channel.ReadBasic.All, Sites.ReadWrite.All, User.Read, Files.ReadWrite.All; Mailflow Mail.ReadWrite, Mail.Send, People.Read, User.Read. Extras: custom scope "SignalR.Access" (HOSTED p15); Intune app adds "DeviceManagementManagedApps.ReadWrite" (Microsoft Mobile Application Management, SAI-SG p4-p5); Universal Print by a separate "Consent to Universal Print" link (HOSTED p21), names not given; card IDs via Entra roles "Attribute Assignment Administrator" and "Attribute Definition Administrator" given to the HPAM service principal, not a Graph permission (HOSTED p24-p27). Caveats for the ticket, if kept: SAI-SG p5 shows "Microsoft Graph (14)" on the Datasec staging registration (one more than the 13; the 14th is not visible); the archive BYO guide lists a different "8 Permissions" set including Directory.Read.All (ARCH-BYO p14, p16). What a real customer tenant has consented to is still unmeasured.
- **W10 / T-07, the "Passwordless MFA" fix: ANSWERED (that half).** CA-FIX shows it end to end: policy "Require approved client apps or app protection policies", target "Office 365", device platforms Android + iOS, grant "Require app protection policy" (f017-f036) breaks the printer: OneDrive "Folder does not exist." (f009), Mailflow "Connection error MF03 Unable to communicate to Azure outlook services" (f012). Fix (f037): grant "Require authentication strength" = "Passwordless MFA", with "Require one of the selected controls"; afterwards OneDrive, Mailflow, SharePoint and Teams load (f041-f064). The TEMPLATES half stays PARTLY (below).
- **W30 / T-14, OneDrive "Shared with me": ANSWERED.** OD p26 limitation: "Unable to display Users Shared Links / Shared Folders / Files for Print and or Scan", workaround "Use SharePoint for Corporate Shared Files and Folders", resolution "TBA". Agrees with the public site.
- **W32 / T-16, Mailflow quick messages ever shown: ANSWERED (yes).** MF p15 (printed 13), "New Email" screenshot shows three bubbles "Here it is.", "Thanks, I have attached the files you requested.", "Please find the attached document." with an "X" close button; a chat-bubble icon appears on the compose/reply/draft screens (MF p11, p12, p17, p18, p20, p22, p23). The text never describes the feature.
- **W38 / T-22, error codes and their help article: ANSWERED (with the public site).** Meanings AI01-AI09 are on the public site (`../MAP.md`). The link target: ARCH-NFR p9 "click Error code on the console to link you to our support page", the link annotation pointing to help article 47001230268 "hp-authentication-manager-error-codes"; the current PRINTER p8 has the same sentence. Caveat: the link target is read from the archive (V3/V4-era) PDF; whether every code links to that same article in V4.4 is not stated.

## 2. Priority questions in detail

### W8 / T-26, every sign-in path: PARTLY (much more than the site; full account in `signin-paths-panel.md`)
- QR first-use registration shown screen by screen, phone and panel: SA-UG p4-p8; Intune variant SAI-UG p5-p10. Panel screen: "Registration" header, "Please wait while we register your new Card/BLE/QRCode ID" (SA-UG p7). "This will initiate a Second Microsoft 2 Digit Push Notification" (SA-UG p7).
- QR, card, BLE later sign-ins: AM-UG p6-p11. MFA switch effect: "If MFA is enabled You will now need to acknowledge and enter the number that appears on the Screen into your Microsoft Authenticator app. Else if NO-MFA is Enabled, it will bypass the Mobile Authenticator 2 Digit request." (AM-UG p7, p9, p11).
- BLE ID = QR ID: "which will be the same ID used if you also decide to use the BLE Option" (SA-UG p8).
- Switch name: "Enable Microsoft MFA/2FA/Passwordless Mode", "Default is Enabled" (PRINTER p5).
- Missing: card first-use enrolment screens ("Just follow the Printers Console instructions to confirm your ID", AM-UG p8); passkey/security key (none); card-only/QR switch names; sign-out confirmation.

### W9 / T-06, Passkey button: PARTLY (the documents point to "no")
- READERS p3: "HP Printers do not support FIDO, FIDO2 HID,U2F protocols."
- HOSTED p4: "We only support Microsoft Authenticator Method policies for MFA Passwordless Sign-in" (its screenshot does show "Passkey (FIDO2)" enabled in the tenant's method list).
- No guide shows a Passkey button. Missing: a statement about a Passkey button on V4.4 screens.

### W10 / T-07, Conditional Access templates: PARTLY
- CA-GUIDE (9 pages, "13th April 2026") gives guidance, not templates. Recommended: "Use a dedicated HP Authentication enterprise app + exclude it from Conditional Access." (p9). Recipe: "Go to Microsoft Entra ID → Security → Conditional Access → Policies." … "Under "Exclude → Applications", add the HP Authentication Suite enterprise app." (p7). Other methods: exclude printer accounts (p7-p8), exclude platform Android (p8, "Not Preferred"), trusted printer subnet (p8-p9).
- PUBLIC-FLOWS: for stricter CA, disable "Allow public client flows" (p5), add Web redirect "http://Localhost" (p4), request a "Special Public Flow Enabled MOC file" (p3, p6); "only supported for deployments performed via the Manual Workpath Installation method" (p6).
- Missing: exported policy templates. The word "template" occurs in no document (CA-FIX shows the portal's own "New policy from template" button only).

### W16 / T-09, deployment tool customers get: PARTLY (both routes exist)
- HP Command Centre is the standard route: "Please use HP Command Centre to Install HP Authentication Manager to Customers fleet" (PRINTER p3); "As of September 2026, HP has provided several alternative tools for deploying HP Workpath applications" (PRINTER p4).
- HOSTED p3: "deployed by HP Command Centre or via the new Command Line Direct Installer"; p5 "HP Workpath New deployment options" with a "Workpath Essential Licence".
- A Datasec tool exists for manual installs: "Here is an Example of our HP Authsuite Manager Installer Tool and the New option called "Use confidential client authentication" enabled." (PUBLIC-FLOWS p6).
- "HPK Deployment Utility" occurs in no document. Missing: which customers get which tool today.

### W19 / T-10, the Manager walkthrough: PARTLY
- PUBLIC-FLOWS p6: the tool takes a MOC file ("Using the same tool originally used for your HP Authentication Manager deployment, replace your existing MOC file"); screenshot fields "App Registration Secret" (masked), "SignalR Endpoint URL", "Use confidential client authentication", "Microsoft Cloud Sovereignty".
- Missing: .cfg import, package kinds beyond the six, job database, password and TLS handling. Not in any document.

### W21-W24 / T-11, licensing: PARTLY overall
- W21 PARTLY: "we only require your Azure Entra Tenant ID which will be used by us to activate your licenses on our License Server located in Azure (Australia East Coast) region" (HOSTED p8). No customer-run licence server is mentioned.
- W22 NOT IN THE DOCUMENTS (portal source). Process only: "To request a HP Authentication Suite Printer Activation Licence, please send an Email to help@hpauthsuite.com" with tenant ID, order number, printer count, term (PRINTER p3).
- W23 PARTLY: HPAM "is also responsible for License Checks" (HOSTED p3); HPCC section "License Options" exists, contents not shown (PRINTER p4); greyed "Base URL" and "API Key" fields in the printer config (SECRET p8). Correction to the public-site reading: in the archive, "Auth URL" sits under "Microsoft Auth Options" next to "Token URL" and "Client ID" and is the Microsoft `/oauth2/v2.0/authorize` endpoint (ARCH-NFR p6-p8), so the site's "Printer License settings AuthURL" fix line is about Microsoft sign-in config, not the licence check.
- W24 NOT IN THE DOCUMENTS (behaviour at expiry). Only: "If this is a Proof of Concept (POC) installation, will provide a free 20 Day license." (PRINTER p3). The only expiry described is the client secret: "HP Authentication suite will stop working if the Secret expires" (ARCH-CUST p11).

### W36 / T-20, panel admin menu: PARTLY
- Per-app admin settings at the panel: sign in with "Administrator Access Code", open the app, "Settings": "Default Print Options", "Default Scan Options", "Send to Email" (OD p22-p25; SP p23-p26); Mailflow adds "Default Microsoft Options" incl. max attachment size (MF p31-p34); Teams print/scan only (TM p23-p26). Same presets in HPCC "Configure" (OD, SP, MF p30, TM p22).
- Missing: card emulation and the HPAM admin menu. No document shows either.

### W6 / T-05 and W37 / T-21, readers: W6 NOT IN THE DOCUMENTS; W37 PARTLY
- Certified list (READERS p16): RFIDEAS "Wave ID PcProx Plus BLE - RDR-30581BKU", "Wave ID Mobile - RDR-30581BKU", "Wave ID SP Plus Keyboard Black RDR-805H1AKU", "RFIdeas Model RDR-30Mx1CxU-MXS-HP"; HP "X3D03A/ X3D03B", "HP HIP2 Keystroke Reader Y7C05A / Y7C05B / 35H11A", "HP HIP2 Keystroke Reader 35H11B"; "Omnikey 5427 Reader ISO14443A Cards Only"; "Elatec TWN4 Slim Reader"; "Inepro Spider - ISO14443A Card Support, includes CypherCard Biometric smart Cards."
- No VID/PID in any document; OMNIKEY 5428 is not mentioned (5427 is). READERS contradicts itself on CypherCard + Spider (p3 "not Supported on TWN4 Nano, Inepro Spider readers" vs p13/p16).
- For the OXPd build: "You should not try and program the reader using OXPD unless you are programming the reader with No HP Authentication Manager installed, else use USB." (READERS p12); remote Elatec tool "will break HP Authentication Manager" if HPAM is installed (p10).

## 3. Full map: every pack id and ticket

| Pack id | Ticket | Topic | Status | File, page, quote |
|---|---|---|---|---|
| W1 | T-01 | card key in 4.4.1 source live? | NOT IN THE DOCUMENTS | Related only: readers "output keystrokes VIA HID, essentially emulating a keyboard" (READERS p3); IDs stored in custom security attributes (HOSTED p5). |
| W2 | T-02 | card-decoding family behind stored cards | NOT IN THE DOCUMENTS | Related: "supports Card Input values to a Maximum of 32 Characters output, in either Hexadecimal or Decimal format however we suggest you set your readers to output in Hexadecimal" (READERS p3). No firmware/Android family named. |
| W3 | T-03 | lab printer models and firmware | NOT IN THE DOCUMENTS | Screenshots name models only: EWS "HP Color LaserJet FlowMFP M577" (PRINTER p7); Universal Print list "HP LaserJet Flow E73130_HPE7313_Secure", "HP LaserJet MFP E72530_ARTUR_Direct" (UPD p4). Requirement: "HP MFD with Latest Firmware 5.10.7 or above" (HOSTED p5). |
| W4 | T-04 | FutureSmart 6 developer-mode printer | NOT IN THE DOCUMENTS | UPD p3 says the app is for "HP FutureSmart 5". |
| W6 | T-05 | readers the lab can lend | NOT IN THE DOCUMENTS | Certified list READERS p16 (section 2). |
| W8 | T-26 | every sign-in path | PARTLY | Section 2; `signin-paths-panel.md`. |
| W9 | T-06 | Passkey button / method | PARTLY | "HP Printers do not support FIDO, FIDO2 HID,U2F protocols." (READERS p3). |
| W10 | T-07 | CA templates; Passwordless MFA fix | PARTLY (fix ANSWERED, templates not) | CA-FIX f037 "Require authentication strength" "Passwordless MFA"; CA-GUIDE p9 "Use a dedicated HP Authentication enterprise app + exclude it from Conditional Access." |
| W11 | T-08 | Graph permissions | ANSWERED (as documented) | "There are 13 Permissions" (HOSTED p17); section 1. |
| W16 | T-09 | deployment tool | PARTLY | "our HP Authsuite Manager Installer Tool" (PUBLIC-FLOWS p6); "HP Command Centre or via the new Command Line Direct Installer" (HOSTED p3). |
| W19 | T-10 | Manager walkthrough | PARTLY | MOC file + four fields (PUBLIC-FLOWS p6); .cfg, packages, job DB, TLS absent. |
| W21 | T-11 | customers' own licence servers | PARTLY | "our License Server located in Azure (Australia East Coast) region" (HOSTED p8). |
| W22 | T-11 | licence portal source | NOT IN THE DOCUMENTS | Email process only (PRINTER p3). |
| W23 | T-11 | how a printer app checks its licence | PARTLY | "responsible for License Checks" (HOSTED p3); "License Options" (PRINTER p4); "Auth URL" is the Microsoft authorize URL (ARCH-NFR p6-p8). |
| W24 | T-11 | behaviour at licence expiry | NOT IN THE DOCUMENTS | Only "a free 20 Day license" for a POC (PRINTER p3). |
| W26 | T-12 | defect level for pilot | NOT IN THE DOCUMENTS | FW p3 generic HP advice: "transition to a pilot phase with limited devices or sites following successful device upgrade testing." No defect level. |
| W27 | T-13 | firmware tracking and re-test | PARTLY | "HP MFD with Latest Firmware 5.10.7 or above" (HOSTED p5; archive: "5.8.x > 5.9.2.3", ARCH-CUST p5). Generic HP: "Maintain tested and qualified firmware and solution versions by device model." (FW p2). Team process not stated. |
| W30 | T-14 | OneDrive Shared with me | ANSWERED | OD p26 (section 1). |
| W31 | T-15 | non-English panel | PARTLY | "We only support English Language / localization" (AM-UG p3; HOSTED p5). Behaviour of screens not shown. |
| W32 | T-16 | Mailflow quick messages shown | ANSWERED (yes) | MF p15 screenshot (section 1). |
| W33 | T-17 | which version | PARTLY | MF p15 is the photo; guide "Updated 10th November 2026"; Information screen "Version: 1.10.02" (MF p28). Not stated that both screenshots are the same build. |
| W34 | T-18 | SharePoint custom fields at scan | PARTLY | "Also enter any other metadata that your company has provisioned on your SharePoint site Document Library." (SP p8); screenshots show two fields "Description", "Total" (SP p8, p10, p11). No number in the guide: the word "four" is not in SP (the four-field limit is on the public site's known-issues list). |
| W35 | T-19 | OneDrive Back -> sign-out confirmation? | PARTLY | "If you Choose the Return Arrow or the Home Screen Icon, it will only exit and not sign you out." (OD p20; SP p21). No sign-out confirmation screen in any guide. |
| W36 | T-20 | panel admin menu | PARTLY | "Administrator Access Code" then app "Settings" (OD p22-p25); no card emulation. |
| W37 | T-21 | OMNIKEY 076B:5428, Inepro 1DA6:0110 | PARTLY | "Omnikey 5427 Reader ISO14443A Cards Only"; "Inepro Spider - ISO14443A Card Support" (READERS p16). No VID/PID. |
| W38 | T-22 | AI01-AI09 meanings and help article | ANSWERED (with the site) | "click Error code on the console to link you to our support page" -> article 47001230268 (ARCH-NFR p9; PRINTER p8). |
| W39 | T-23 | eight Universal Print "as coded" behaviours, UUID | PARTLY | Intended behaviours to compare against: "Pull – … as soon as you sign-in, all of your print jobs will be released, The user will not be challenged to perform any MFA Authentication" (UPD p4); "Please Select Pull Print Auto Sign-out setting. 10 > 30 Seconds Maximum" (UPD p6); "If you do not respond in a timely manner, the Pull Print service will automatically sign you out." (UPU p7). Our eight code points and the UUID question are not addressed. |
| W40 | T-24 | other IPP attribute groups | NOT IN THE DOCUMENTS | No IPP text in UPD or UPU. |
| W41 | T-27 | Log Analytics job record fields | PARTLY | Tables "HpamPrinterLogs_StatisticJobData_CL, contains all Printer Activities, Print, Scan, Copy, Fax, License etc." and "HpamPrinterLogs_Supply_CL" (HOSTED p23; screenshot spells "StatisticsJobData"); query fragments parse JSON columns `jobInfo` and `httpInfo` (p23). No field list. |
| W42 | T-28 | customers changed rule or tables | NOT IN THE DOCUMENTS | The connection string shows a DCE, stream `Custom-HpamPrinterLogs` and a `dcr-…` rule (HOSTED p22); nothing on customer changes. |
| W43 | T-29 | report / workbook queries | PARTLY | Named only: "HPAM_KQL_Report_Log_Analytics_Scripts.zip" with Print Activity, Scan Activity, Toner Supplies scripts (HOSTED p23). Contents not in the PDF. |
| W48 | T-25 | README password live? | NOT IN THE DOCUMENTS | Not a document topic. |

## 4. Counts

By pack item (32 W numbers, as in `../MAP.md`):
- ANSWERED: 4 (W11, W30, W32, W38); plus the fix half of W10.
- PARTLY: 17 (W8, W9, W10, W16, W19, W21, W23, W27, W31, W33, W34, W35, W36, W37, W39, W41, W43).
- NOT IN THE DOCUMENTS: 11 (W1, W2, W3, W4, W6, W22, W24, W26, W40, W42, W48).

Change against the public-site map: newly ANSWERED W11, W32, W38 (W30 was already); NOT -> PARTLY: W9, W16, W19, W33, W35, W39, W43; W10 fix half answered.

By ticket (29): ANSWERED 4 (T-08, T-14, T-16, T-22); PARTLY 16 (T-06, T-07, T-09, T-10, T-11, T-13, T-15, T-17, T-18, T-19, T-20, T-21, T-23, T-26, T-27, T-29); NOT 9 (T-01, T-02, T-03, T-04, T-05, T-12, T-24, T-25, T-28).

## 5. Worth a look (not asked)

- HPCC configuration fields, current (PRINTER p4-p6): "Tenant ID", "App Registration Client ID", "Enable Microsoft Entra custom Security Attributes", "App Registration Secret", "SignalR Endpoint URL", "Console user name", "Enable Microsoft MFA/2FA/Passwordless Mode", "Reporting Connection String", "Cloud Environment"; plus greyed "Base URL", "API Key" (SECRET p8). Archive adds "AppCenter Key (Logs)", "Token URL", "Auth URL", "Client ID" (ARCH-NFR p6-p8). Redirect URI `com.hp.hpauthenticationmanager://oauth2redirect`, public client (HOSTED p10).
- SignalR gateway Function App functions "healthcheck", "negotiate", "send"; app settings incl. MICROSOFT_PROVIDER_AUTHENTICATION_SECRET and SIGNALR_CONNECTION_STRING (SECRET p7-p8). Values not recorded.
- Intune phone-app keys (SAI-SG p12-p13): CloseAppOnInactivityTimeoutSeconds, QRCode, BLE, BleReaderType, BleConnectionDistance_Android, BleConnectionDistance_iOS, BleLockType.
- HPAM takes exclusive reader access: do not program readers over OXPd while HPAM is installed (READERS p10, p12).
- Teams PDF is missing printed pages 12-16 (TM p11 -> p12 jumps 11 -> 17).
