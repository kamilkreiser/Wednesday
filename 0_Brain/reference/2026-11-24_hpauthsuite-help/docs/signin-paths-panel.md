# Sign-in paths on the printer panel, screen by screen, as the gated guides show them

Read 2026-11-24 (Tuesday seat, s321). Source: the help-portal PDFs and one support video, copies read-only at `/Volumes/DEV-Working/Datasec/Friday/2026-11-19_oxpd-friday-work-and-library/OXPd/HPAM/Help-Portal/Documents/`. This file adds what the guides SHOW (screenshots, button labels, order) to the public-site account in `../signin-paths.md`. Every step names file and PDF page (`p<N>` = PDF page; printed footers match except where noted). Quotes are copied from the page or screenshot. **UNMEASURED** = no guide shows it.

Short names used below:
- **AM-UG** = `Manuals/Datasec-HP_Authentication_Manager_UG.pdf` (12 p, "Revised 10th November 2026")
- **SA-UG** = `Manuals/Datasec-HP_Secure_Authentication_UG.pdf` (18 p, "User Guide V1.5.12", "Released 7th October 2026")
- **SAI-UG** = `Manuals/Datasec-HP_Secure_Authentication_Intune_UG.pdf` (18 p, "Revised 7th October 2026")
- **SAI-SG** = `Manuals/HP_Secure_Authentication_Manager_Intune_Setup_Guide.pdf` (15 p, "Revised 7th October 2026")
- **HOSTED** = `Manuals/HP Authentication Manager Azure Hosted Deployment Instruction.pdf` (29 p, "Revised 10th November 2026")
- **PRINTER** = `Manuals/HP Authentication Manager Azure Printer Deployment Instruction.pdf` (8 p, "Revised 10th November 2026")
- **READERS** = `Manuals/Datasec - Reader_Configuration.pdf` (16 p, "Revised 24th September 2026")
- **CA-FIX** = `Support/Condition_access_policy_Fix.mp4` (479 s; frames `f_NNN` one per 5 s in `2_Project_Files/fleet/state/s321/docsread/frames/`, frame n is about (n-1)x5 s)
- App guides (OneDrive, SharePoint, Mailflow, Teams) for the start-from-an-app and sign-out lines.

## 0. Screens every path shares (the panel vocabulary)

| # | Screen | What is on it (verbatim) | Source |
|---|---|---|---|
| S0 | Home, signed out | top bar "Reset" "Sign In"; tiles incl. "HP Authentication Manager", "Onedrive", "SharePoint" (Mailflow, Teams, Universal Print on other screenshots); bottom "1" "Copy" | AM-UG p6, p8; CA-FIX f001 |
| S1 | HPAM QR main screen | header "HP Authentication Manager" · "Sign In" · (?) (i) · clock; body "Scan QR Code using HP Secure Authentication Mobile application" + QR; footer "Terms of use" "Privacy & Cookies" "About"; home icon, back arrow | AM-UG p6; SA-UG p5, p11; PRINTER p7 |
| S2 | Confirm ID | header "HP Authentication Manager" · "Sign In"; body "Please wait while we confirm your account ID" + spinner | AM-UG p7, p9, p10; SA-UG p12, p13; CA-FIX f041-f042 |
| S3 | Registration | header "HP Authentication Manager" · **"Registration"**; body "Please wait while we register your new Card/BLE/QRCode ID" + spinner | SA-UG p7; SAI-UG p8 |
| S4 | Microsoft number match (embedded in HPAM frame) | header "HP Authentication Manager" · "Sign In" (or "Registration" during enrolment, SAI-UG p9); Microsoft page "Approve sign in", "Open your Authenticator app, and enter the number shown to sign in.", two-digit number, "Didn't receive a sign-in request? Swipe down to refresh the content in your app.", link "Use your password instead" | AM-UG p7, p9, p11; SAI-UG p9; CA-FIX f007, f043 |
| S5 | Home, signed in | top bar "Sign Out" + user name (e.g. "John Doe", "Steve Molnar", "Steve Demo") | AM-UG p8, p9, p11; SA-UG p7; CA-FIX f008 |
| S6 | Signing out | blue top bar "Signing out" | CA-FIX f016, f082 |
| S7 | Short wait | header "HP Authentication Manager" · "Sign In"; body "Please wait." (seen once, then straight to S5 with no S4) | CA-FIX f089-f090 |

The user name on S5 comes from the HPCC setting "Console user name" (First Name + Last Name / Email / UPN / Display Name): PRINTER p5.

## 1. Ways to START a sign-in (all paths)

AM-UG p6, verbatim list "You have several choices on how to initiate a Sign-In and will depend on how your printer has been commissioned":
1. "Tap any HP Authentication Suite of Applications and this will detect if a Sign-in has already been initiated, if not it will start HP Authentication Manager Sign in Process and it will then open the application you had selected."
2. "Press **Sign in** and Scan QRCode using HP Secure Authentication mobile app, then choose your required application."
3. "Press **HP Authentication Manager** ICON and Scan QRCode ..."
4. "Tap Compatible NFC Card anytime, and then choose your required application."
5. "Use HP Secure Authentication Mobile app via BLE (Bluetooth Low Energy) option anytime, and then choose your required application."
The same five appear in the OneDrive, SharePoint, Mailflow and Teams guides (p5 of each).

Setup options that decide which screens appear:
- MFA switch: HPCC "Security Options" > "Enable Microsoft MFA/2FA/Passwordless Mode", "Default is Enabled" (PRINTER p5).
- QR needs SignalR: "you should see our Main Screen with its QRcode unless you have chosen not to configure SignalR" (PRINTER p7). HPCC field "SignalR Endpoint URL" (Optional) (PRINTER p5). SignalR not needed for card-only (HOSTED p5, p14).
- Card IDs stored in Entra custom security attributes: HPCC checkbox "Enable Microsoft Entra custom Security Attributes" (PRINTER p5).
- Registration needs time: set printer "Inactivity Timeout" to "300 Seconds" while users register, then lower (PRINTER p6-7).
- No HPCC switch for "card only", "QR on/off" or "BLE on/off" appears in any guide: UNMEASURED. On the PHONE, QR and BLE are per-user toggles (SA-UG p10, p15) or Intune keys `QRCode`, `BLE` 0/1/2 (SAI-SG p12-13).

## 2. QR, first use (self-registration) — fully shown

Source: SA-UG p4-p8 (non-Intune); SAI-UG p5-p10 (Intune variant).
1. Phone: open HPSA, "Tap **Get started**" (SA-UG p4; Welcome screen with "Get Started").
2. Phone: allow camera, "Select **While using the app**" (SA-UG p4). Phone shows "Account Validation": "Locate the Nearest HP Printer & Tap Sign-in or Tap the HP Authentication Manager Icon on the console." (SA-UG p4 screenshot).
3. Panel: "Tap **HP Authentication Manager** Icon on your HP Printers Console" (SA-UG p4, S0 with the tile boxed).
4. Panel: S1, "(Do not use your built-in Photo Camera App)" (SA-UG p5).
5. Phone: "Scan the QRcode that appears on the HP Printers Console using your Rear Camera." (SA-UG p5, phone "Scanning" screen).
6. Phone: "Sign into your Companies Microsoft Account on your Mobile Phone." (Microsoft "Sign in", SA-UG p5).
7. Phone: Microsoft "Approve sign in" with a number, user enters it in Authenticator ("Are you trying to sign in?", "No, it's not me" / "Yes") (SA-UG p6). Back in HPSA. "This has completed **Step one** of two" (SA-UG p6).
8. Panel: S3 "Please wait while we register your new Card/BLE/QRCode ID" (SA-UG p7).
9. Phone: "This will initiate a **Second** Microsoft 2 Digit Push Notification, so that it can register your QRcode Badge ID and assign it to your Azure 365 Office account." (SA-UG p7).
10. Panel: S5 signed in ("Step 3 - You will now be **signed into** the HP Device", SA-UG p7).
11. Result: "You Registered your HP Secure Authentication Mobile Phone Unique Generated Badge (QRCode) ID against your Microsoft 365 Account which will be the same ID used if you also decide to use the BLE Option." (SA-UG p8; same in SAI-UG p10). This settles the public site's open point: the BLE ID IS the QR badge ID.

Intune variant differences (SAI-UG):
- Phone: "Get Started" launches Microsoft Authenticator, "Pick an account to continue" (p6); Intune "Get Access" checks, CONTINUE (p7); set and confirm an app PIN (p7).
- Panel: S3 then **S4 inside a "Registration" header** on the PANEL ("Approve sign in", number 65, "Open your Authenticator app and approve the request. Enter the number if prompted.") (p9); the user enters the number "that appears on your Printers Console" (p9 step 12). So in this variant the second number-match is displayed on the panel.
- Prerequisite: HPAM "V4.2.1 or Greater" (p3); Android also needs Intune Company Portal installed (p4).
UNMEASURED: whether the non-Intune registration also shows S4 on the panel (SA-UG p7 shows only the phone push).

AM-UG p7 adds only: "If this is the First time you are using the QRCode Option to Sign-in, you will be asked to enroll you QR Code ID ... Just follow the Printer Console instructions to confirm your ID."

## 3. QR, later sign-ins

Source: SA-UG p11-p12; AM-UG p6-p8; SAI-UG p12-p13.
1. Panel: tap "Sign in", the HPAM tile, or any suite app (S0) (SA-UG p11 steps 1-3).
2. Phone: launch HPSA; it "will automatically start the to scan for a QRCODE" (SA-UG p11).
3. Panel: S1 (AM-UG p6).
4. Panel: S2 "HP Authentication Manager will now confirm your QRCode Account Badge ID and will Start a Microsoft Login by using your associated Microsoft User/Email account name." (SA-UG p12).
5. MFA on: S4 on the panel, user types the number into Authenticator (AM-UG p7 step 4). MFA off: "Else if NO-MFA is Enabled, it will bypass the Mobile Authenticator 2 Digit request." (AM-UG p7). SA-UG p12 step 7 is looser: "you will be prompted accordingly ... either using 2FA - MFA passwordless, PIN etc..".
6. Panel: S5 (AM-UG p8).

## 4. Card (NFC / proximity), MFA on and No-MFA

Source: AM-UG p8-p9; READERS p3-p16.
1. Panel: S0; "Tap your Compatible NFC Card on the Reader, this will initiate a Sign-in." (AM-UG p8). "Compatible card readers are required for NFC operations." (AM-UG p8).
2. First use: "If this is the First time you are using the NFC card to Sign-in, you will be asked to enroll you NFC Card unique ID, and will be assigned to your Microsoft Azure account. Just follow the Printers Console instructions to confirm your ID." (AM-UG p8). The enrolment screens themselves: UNMEASURED for card (only the shared S3 "register your new Card/BLE/QRCode ID", SA-UG p7, names cards). First registration always needs a Microsoft login even in No-MFA (HOSTED p4).
3. Panel: S2 "Please wait while we confirm your account ID" (AM-UG p9).
4. MFA on: S4 number match (AM-UG p9). No-MFA: S4 bypassed (AM-UG p9, same sentence as QR).
5. Panel: S5 (AM-UG p9).
6. Sign-out by card: "Tap **Sign Out** at the Console or **Tap your Card on your Reader** and this will perform a Sign out" (AM-UG p12).
Reader facts behind the tap (READERS): readers "output keystrokes VIA HID, essentially emulating a keyboard" (p3); up to "32 Characters" hex or decimal, hex recommended (p3); ISO14443A CSN 32/56-bit, MiFare Classic/DesFire CSN, CypherCard Biometric (56-bit UID, p8), BLE (128-bit, p9); every reader must output the same ID (p4).
Video evidence (CA-FIX f006-f008, f041-f045): S0 -> HPAM "Sign In" (blank, loading) -> S4 "Approve sign in" for steve.demo@... -> S5. What started it (card tap or button) is not visible in the frames, and the narration was not transcribed: UNMEASURED.
No-MFA observed? CA-FIX f089-f091: S0 -> S7 "Please wait." -> S5 with no S4. This fits the No-MFA / stored-refresh-token behaviour the site describes, but nothing on screen says which mode was set: UNMEASURED.

## 5. BLE

Source: AM-UG p10-p11; SA-UG p9-p10, p13-p15; SAI-UG p11, p14-p15; SAI-SG p10-p14.
Setup on the phone (BLE is off by default): Menu > "Settings" > "Bluetooth Reader" on; optionally "QRCode Scanner" off; pick reader in "Supported (BLE) Readers" (e.g. "Elatec TWN4"); "(BLE) Connection distance" slider Far..Near (e.g. "-40 dBm"), default "approximately 7-8 Inches/ 200mm" (SA-UG p15). Intune keys: `BLE`, `BleReaderType` (Elatec / Rfideas), `BleConnectionDistance_Android`, `BleConnectionDistance_iOS` (20-100), `BleLockType` (SAI-SG p12-p13).
Sign-in:
1. Phone: "Tap your **Bluetooth** button on your **HP Secure Authentication Mobile** app when you are near your printer, do not place your Phone on the reader or Tap the Reader as it may open up your Wallet." (AM-UG p10; phone shows "Welcome John Doe", "Select how you would like to log in", buttons "Bluetooth" "QR Code"). SA-UG p13: launching the app near the reader "will automatically initiate a BLE Signal"; phone shows "Bluetooth communication is successful", button "Bluetooth Reader".
2. Panel: S2 "HP Authentication Manager will confirm your BLE Badge ID and will Start a Microsoft Login" (SA-UG p13; AM-UG p10).
3. First use: "you will be asked to enroll you Bluetooth unique ID ... Just follow the Printers Console instructions" (AM-UG p10). But SA-UG p8 says the BLE ID is the same as the QR badge ID already registered, and the panel S3 names "Card/BLE/QRCode" (SAI-UG p8: "The first time you Scan the QRCode and or Use BLE, you will be asked to register your Mobile Phone Badge ID"). Whether a QR-registered phone is asked again on first BLE use: UNMEASURED (the guides say both).
4. MFA on: S4 (AM-UG p11). No-MFA: bypassed (AM-UG p11).
5. Panel: S5 (AM-UG p11).
6. If nothing happens: "get a Little closer to the reader and tap the Bluetooth Reader Button to try again." (SA-UG p13).
Readers that do BLE (READERS p16): RFIDEAS Wave ID PcProx Plus BLE / Wave ID Mobile (RDR-30581BKU), HP HIP2 Keystroke Reader 35H11B, Elatec TWN4 Slim.

## 6. Security key / passkey

- No guide shows a passkey or security-key button, screen or step. The words "passkey" and "security key" do not occur in any guide text; positive control: "Passkey (FIDO2)" appears in a screenshot (below), and "FIDO" in READERS.
- READERS p3: "HP Printers do not support FIDO, FIDO2 HID,U2F protocols." YubiKeys only as card fobs giving an ISO 14443A ID: "This could also include security fobs like some of the YubiKeys." (READERS p3).
- HOSTED p4 screenshot shows the Entra "Authentication method policies" with "Passkey (FIDO2)" enabled for all users, but the text says: "We only support Microsoft Authenticator Method policies for MFA Passwordless Sign-in" (HOSTED p4).
- S4 shows only "Use your password instead" as an alternative link (AM-UG p7; CA-FIX f007). A Microsoft "Sign in with a passkey / security key" option on the embedded page: UNMEASURED.

## 7. Sign-out

- Console: "Tap **Sign Out** at the Console or **Tap your Card on your Reader**" (AM-UG p12). Panel then shows S6 "Signing out" (CA-FIX f016).
- Leaving an app does not sign out: "If you Choose the Return Arrow or the Home Screen Icon, it will only exit and not sign you out." (OneDrive UG p20; SharePoint UG p21; Mailflow and Teams guides same sense). Each app has its own "Sign Out" button in its title bar (CA-FIX f009, f045).
- No sign-out confirmation screen is shown in any guide: UNMEASURED.
- Timeout: "review the printers Auto Timeout settings" (AM-UG p12); EWS "Inactivity Timeout" 10-300 s (PRINTER p7).

## 8. Conditional Access effect on the paths (what the fix video shows)

CA-FIX: with a policy "Require approved client apps or app protection policies" (target "Office 365", device platforms Android + iOS, grant "Require app protection policy") the user signs in (S4, S5) but OneDrive shows "Folder does not exist." and Mailflow "Connection error MF03 Unable to communicate to Azure outlook services" (f009-f012, f017-f036). After adding grant "Require authentication strength" = "Passwordless MFA" with "Require one of the selected controls", the same sign-in reaches OneDrive folders, Mailflow inbox, SharePoint sites and Teams (f037-f064). Sign-in screens themselves are unchanged.

## 9. Still UNMEASURED after the documents

1. Card first-use enrolment screens (only "follow the Printers Console instructions" and the shared S3 text).
2. What happens on the panel when MFA is off at first registration (HOSTED p4 says a Microsoft login is still needed; no screen).
3. Whether non-Intune QR registration shows the second number-match on the panel (Intune guide shows it on the panel; non-Intune guide shows only the phone).
4. Which HPCC setting makes a printer "card only" or hides the QR (AI07 "Card Readers ONLY" exists per the public site; no switch name in the guides).
5. Passkey / security key: no path at all in the guides.
6. Sign-out confirmation screen: none shown.
7. CA-FIX narration (audio present, not transcribed) and what triggered each sign-in in the video.
8. Error screens AI01-AI09 on the panel: no guide shows them; PRINTER p8 says only "click Error code on the console to link you to our support page".
