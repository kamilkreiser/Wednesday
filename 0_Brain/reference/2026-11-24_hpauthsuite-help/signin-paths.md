# Sign-in paths as the public HP AuthSuite help site describes them

Read 2026-11-24 from https://help.hpauthsuite.com (public pages only). Every quote is copied from the page named beside it. Where the site is silent the line says UNMEASURED. The site has no screen-by-screen walkthrough: those live in PDFs and videos that sit behind a Microsoft sign-in or on YouTube, none of which were read. So the steps below are the steps the ARTICLES state, not the full panel flow.

Product names on the site: HP Authentication Manager = HPAM (the printer app); HP Secure Authentication = HPSA (the phone app); Microsoft Authenticator is a third app the user must also have. Versions named on the site: HPAM V4.4 (released, notes dated 10 Nov 2026 on the page), V4.2.1, V4.2; mobile app V1.5 (error-code article asks for "1.5 >"), reader list written for "HP Authentication Manager v4.> and ... HP Secure Authentication Mobile Application v1.4.9 >".

Short source form used below: `A:<id>` means `https://help.hpauthsuite.com/support/solutions/articles/<id>`.

## 0. What every path shares

1. HPAM "instigates a Microsoft sign in process using Swipe Cards, BLE Devices Like HP Secure Authentication Mobile Application or via our custom generated QR Code." Source: A:47001240865 (https://help.hpauthsuite.com/support/solutions/articles/47001240865-hp-authentication-manager).
2. After the console sign-in the other apps need no second sign-in: "Users will have full access to HP office 365 Authentication suite of applications Like OneDrive, SharePoint, MailFlow, Teams and Universal Print, without the need to re-authenticate." Source: A:47001240865.
3. Only Microsoft identity is supported: "We currently support only Microsoft login and the Microsoft Authenticator mobile app configured for Passwordless Sign-in." Third-party sign-in (Okta, PingID, Cisco Duo) is not supported. Source: https://help.hpauthsuite.com/support/solutions/articles/47001285792-common-issues-when-setting-up-hp-authentication-manger
4. Printer prerequisites: "Printer Firmware 5.10.0.7", "Your HP MFD must be HP Workpath capable and enabled", "Your HP MFD must not have any other Login and Authentication application installed.", "We only support English Language / localization". Source: https://help.hpauthsuite.com/support/solutions/articles/47001245378-prerequisites-for-hp-authentication-manager
5. Installer: apps go onto printers "using HP's Command Centre Web Portal", which most customers cannot access. Source: A:47001245378 (same page as item 4).
6. User prerequisites for passwordless: "all users must be using Microsoft's Authenticator Mobile Application (Free), configured in Passwordless mode." For QR sign-in: "All users must be using the HP Secure Authentication Mobile App for Android and IOS (Free)". Source: A:47001245378.
7. Neither readers nor phones are mandatory in themselves: "NFC nor BLE Readers are required for our solution ... our solution will support a Reader-less flow by using our HP Secure Authentication Mobile app via the QRCode Option." Source: A:47001245378.
8. Licences: every user needs a Microsoft 365 licence; "If Universal Print Services are being deployed, each user must have a licence that includes Universal Print". Source: A:47001245378.
9. Setup test the site tells every user to run before touching a printer: open https://office.com, enter the username only, and expect "You will be prompted to use the Microsoft Authenticator app." or an option reading "Use the app instead." (the page's wording), with no password prompt. Source: A:47001285792 (URL in item 3).
10. Why a password prompt can appear: "the HP solution uses the printer's embedded web browser for user authentication", so Windows Hello passkey-style sign-in on a PC does not count; extra Azure AD and phone configuration is needed. Source: A:47001285792.

## 1. Card or badge (NFC / proximity reader), MFA enabled (the default)

Setup options and prerequisites
- Reader must output keystrokes: "The HP Authentication Manager application uses card readers that output keystrokes, essentially emulating a keyboard." Cards must be "ISO 14443A CSN" capable. Source: https://help.hpauthsuite.com/support/solutions/articles/47001217796-hp-authentication-manager-supported-nfc-ble-readers
- All readers should give the same ID: "it is essential that all Card/BLE readers are configured to output the exact same ID consistently across all devices." Otherwise "users needing to register their cards or BLE credentials multiple times". Source: A:47001217796.
- A card's ID is a static 32 or 56 bit number: "all cards should support the minimum of providing a Static 32/56bit ID". Source: A:47001217796.
- Microsoft Authenticator in passwordless mode is still required: "You are still required to use Microsoft Authenticator mobile app in Passwordless Mode to Register your card and perform MFA Sign-ins at the printers Console." Source: A:47001285792.
- Where the card ID is stored: Entra Custom Security Attributes (attribute "cardId"). "In HP Authentication Managers Case we store users Card/Badge identities". Source: https://help.hpauthsuite.com/support/solutions/articles/47001285099-custom-security-attributes-and-why-we-chose-this-pathway- ; attribute name from https://help.hpauthsuite.com/support/solutions/articles/47001309058-how-do-i-delete-a-users-card-id-from-custom-security-attributes
- Customer-hosted or Datasec-hosted Card IDs are both described: "If Datasec is Hosting your Card ID's then" versus "If Your Company is hosting your Card ID's Via Azure custom attributes". Source: https://help.hpauthsuite.com/support/solutions/articles/47001269321-i-cannot-sign-in-anymore-using-my-card-and-or-qrcode

Steps the site states
1. First use: the user taps the card, completes a Microsoft sign-in, and the card is registered to that account. Support for this reading: "first-time user registration or enrolment for Card, BLE, QR Code, or the HP Secure Authentication Mobile App, users are still required to complete a Microsoft login and authentication step." Source: https://help.hpauthsuite.com/support/solutions/articles/47001285412-can-i-use-username-and-passwords-only-to-register-and-perform-sign-in
2. The printer app writes the card ID after the user authenticates: "When a user adds or updates a card, the HP Authentication Manager Enterprise app performs the update on the user's behalf after the user successfully completes Azure AD authentication." Source: A:47001285099.
3. Later sign-ins: the card tap starts the Microsoft sign-in and Authenticator asks for the number match: the user must "enter the two-digit Microsoft number" and confirm with PIN, face or biometrics. Source: https://help.hpauthsuite.com/support/solutions/articles/47001246513-how-is-the-qrcode-and-ble-card-id-s-generated
4. Known quirk, fixed in V4.2.1: "it may not recognise the card and ask them to repeat the registration process." Workaround "Please Wait 30 Seconds and tap Card again". Source: https://help.hpauthsuite.com/support/solutions/articles/47001246572-known-issues-limitation-s
5. Reset: delete attribute cardId and Save; "it can take up to 5 Minutes before the changes are propagated". "The attribute cardId will be recreated automatically once a user registers a New Card." Source: https://help.hpauthsuite.com/support/solutions/articles/47001309058-how-do-i-delete-a-users-card-id-from-custom-security-attributes
6. Reader-only sites should avoid the QR attempt: the app "will try to generate a QRcode and will fail without indicating why" unless SignalR is set up; workaround "Tap your Card/Badge and Sign-in before you choose any of the Applications." Source: A:47001246572.

UNMEASURED on the site: the exact panel screens for tap, register and sign-in; which Microsoft screens appear; the timeout for the Authenticator number-match.

## 2. Card, No-MFA

- Introduced: "as of April 2025 we will support No MFA Sign-in for customers that do not wish to use Mobile Phones and currently use NFC/Proximity RFID Readers only." Source: A:47001240865.
- MFA is on by default and can be turned off by the customer: "When HP Authentication Manager is set for MFA Enabled!(Default)" and "Customers have the rights to disable the Passwordless MFA process for their Printers". Source: A:47001246513.
- What No-MFA does at sign-in: HPAM re-uses a stored refresh token: "HPAM also uses the previously stored refresh token in NO-MFA mode." and "we store refresh token to support our NO-MFA scenario only". Source: https://help.hpauthsuite.com/support/solutions/articles/47001285083-azure-refresh-tokens-how-are-they-used-by-hp-authentication-suite
- Registration is still interactive: "We support No MFA Authentication Challenge during standard sign-in. However , during first-time user registration or enrolment ... users are still required to complete a Microsoft login". Accepted registration methods: "Username + Password", "Username + Password + OTP", "Username + Microsoft Authenticator Push Notification". Source: A:47001285412.
- Refresh token life: "Refresh token lasts 90 days. Every time we obtain new access_token we receive new refresh_token which lasts another 90 days." If Entra rejects the silent refresh, "HPAM falls back to interactive login". Source: A:47001285083.
- Second-attempt quirk in No-MFA: "If you have configured not to use MFA, you may be asked to Validate your Microsoft Sign-in on the Second Attempt as well." Source: A:47001246572.
- Risk statement: with MFA off "any person can covertly use the person card to Sign-in"; the site points to CypherCard fingerprint cards or biometrics on the phone. Source: A:47001246513 and A:47001285412.
- Where the switch lives (HPCC configuration, MOC) : UNMEASURED. The site says only that the printer is configured through HP Command Centre ("review and re-apply via HP Command Centre", https://help.hpauthsuite.com/support/solutions/articles/47001230268-hp-authentication-manager-error-codes).

## 3. QR code (phone app scans the printer's QR)

Setup options
- SignalR: needed for QR sign-in on self-hosted sites. the page asks "Is it Optional?" and answers that SignalR and its related services are "not required" when only certified card readers and badges/smart cards are used. Source: https://help.hpauthsuite.com/support/solutions/articles/47001285413-what-is-azure-signalr-service-and-why-is-it-used-
- Datasec-hosted API vs customer-hosted: the SRS error "does not affect sites that are still using our Datasec Hosted API services." Source: https://help.hpauthsuite.com/support/solutions/articles/47001234721-hp-secure-authentication-error-codes-message
- Regions: the QR code carries the site settings, "which API and Keycloak Server your printer has been assigned to". Source: https://help.hpauthsuite.com/support/solutions/articles/47001246512-what-information-is-inside-the-qrcode . Region rules: https://help.hpauthsuite.com/support/solutions/articles/47001258067-what-are-printer-regions
- Keycloak is being retired: "All references to Keycloak is now Obsolete, we are deprecating our Keycloak Services in Mid 2027". Source: A:47001246512.
- Works on 4.3in screens: "Does the QRCode work on 4.3" Display Screens. A. Yes". Source: A:47001246512.

Steps the site states
1. The printer app generates the QR. Each code carries "a Random Hashed Keypair Name & Secret that provides a Onetime use for the mobile app", with "No Client or user information". Source: A:47001246512.
2. First registration: the user scans the printer's QR with the HPSA app (not the phone's camera): "You may have scanned the QRcode using your Built-in Camera App and not the HP Secure Authentication Mobile app". Source: A:47001234721.
3. The user signs in to Microsoft in the app; HPSA and HPAM use "the OAuth 2.1 Authorization Code flow with PKCE against Microsoft Entra", requesting the "offline_access scope". Source: A:47001285083.
4. HPAM "securely listens to SignalR and processes the user's first QR code scan. At that point, HPAM registers the mobile device and stores the user's Unique QR Code Badge ID." Source: A:47001285083.
5. Registration happens once: "Registration only happens once, and thereafter it enables you to effortlessly sign in to any of your company's printers using either the QR Code or Bluetooth (BLE)". Source: https://help.hpauthsuite.com/support/solutions/articles/47001243384-can-i-use-my-hp-secure-authentication-mobile-app-on-any-printer
6. Later sign-ins: scan the console QR; badge ID is "a unique set of 16 digits ... specific to the user's mobile phone and their Microsoft user name"; MFA then needs the Authenticator number match. Source: A:47001246513.
7. Failure cases: AI08 and AI09 (SignalR or QR missing), SRS (mobile side), "you may receive a success message yet you are not signed in" (fixed V4.2). Sources: A:47001230268, A:47001234721, A:47001246572.
8. First-time registration can time out on a slow printer: "default is 60 Seconds ... make it 120 Seconds". Source: https://help.hpauthsuite.com/support/solutions/articles/47001246315-trouble-shooting-tips-for-hp-secure-authentication-mobile-app

UNMEASURED on the site: the exact bytes or JSON in the QR (the site gives only the field idea: keypair name, secret, site settings); the SignalR message sequence beyond the sentences above.

## 4. BLE (Bluetooth Low Energy from the phone app to a reader on the printer)

Setup options and prerequisites
- Only certain readers: "If you choose to use HP Secure Authentication Mobile app via the Bluetooth Option, then we only support the Wave ID PcProx Plus BLE/ Wave ID Mobile - RDR-305x1BxU, Elatec TWN4 Slim Readers and HP35H11B Mobile credentials." Source: https://help.hpauthsuite.com/support/solutions/articles/47001217796-hp-authentication-manager-supported-nfc-ble-readers
- Inepro: "BLE Support only works when using the Inepro Mobile App (Spider ID) ... and therefore will not work with our HP Secure Authentication mobile app." Source: A:47001217796.
- No pairing: "The short answer is No!" Source: https://help.hpauthsuite.com/support/solutions/articles/47001245214-do-i-need-to-pair-my-mobile-phone-bluetooth-to-my-hp-printer
- The phone app must have BLE enabled: "Tap the Enable Bluetooth Reader Slider" under Settings. Source: https://help.hpauthsuite.com/support/solutions/articles/47001246312-my-bluetooth-button-is-missing-from-my-mobile-app
- Reader radio settings: Elatec TWN4 Slim only (not Nano), programmed with the supplied project files; the reader "BLE radio is active". Sources: https://help.hpauthsuite.com/support/solutions/articles/47001286017-how-to-program-elatec-twn4-readers-to-support-hp-authentication-suite and A:47001234721.

Steps the site states
1. Register first by QR (path 3). Then BLE: "If the user later enables Bluetooth Low Energy (BLE), their Unique BLE ID is also registered". Source: A:47001285083.
2. Sign in: press the BLE button in the app (or auto-launch) near the reader; the app sends the ID. Support: "It utilizes both a QR code and a BLE button that, when pressed, generates a unique set of 16 digits." (from A:47001246513); the BC01 error text "you should also hear a Beep indicating the reader received the Bluetooth commands" (A:47001234721).
3. Range: the app's Signal Strength setting; "the default is around 200-300mm (11") away from a Reader"; on the FAR setting a reader "up to 4-10 Meters" away can pick it up; "Please consider changing the Distance slider to Near". Source: https://help.hpauthsuite.com/support/solutions/articles/47001281263-why-does-my-ble-signal-starts-a-sign-in-on-another-printer-some-distance-away-from-me
4. Error BC01: "Unable to communicate with your BLE Reader". Fix: stand closer, check the reader's BLE radio, or use the QR. Source: A:47001234721.
5. iOS quirk (fixed September 2025): first BLE use "may receive a BC01 Error". Source: A:47001246572.

UNMEASURED: the BLE advertisement format and the identity of the 16 digits beyond "hashed"; whether the BLE ID is the same value as the QR badge ID (the site says "Unique BLE ID" and "Unique QR Code Badge ID", two names).

## 5. CypherCard / SentryCard (card with fingerprint) , a variant of the card path

- Biometric NFC card; "Each card supports the enrolment of up to two fingerprints". Enrolment is "exclusively by a mobile phone application" (SentryCard Enroll). Source: https://help.hpauthsuite.com/support/solutions/articles/47001300360-how-do-i-add-my-biometric-finger-prints-to-a-cyphercard
- Readers: "We now support the CypherCard Biometric SmartCard on Elatec TWN4 SLIM only readers and not TWN4 Nano. We also support Inepro Spider readers only". Source: A:47001217796.
- "the card's unique ID" is revealed to the reader "when a user authenticates via the built-in fingerprint sensor". Source: A:47001217796.
- Then it follows the card path (steps 1 to 6 of section 1). Source: A:47001300360 ("register the card's unique ID/number against the user's Azure login account on any of your HP Printers using HP Authentication Manager").
- A fixed enrol code is needed for visitor cards ("the customer's unique Enroll Code"); the code itself is not on the site.

## 6. Security key and passkey

- The words "passkey" and "security key" do not appear in any of the 84 articles (checked by search over the saved text, with a positive control on another word). UNMEASURED for a hardware security key (FIDO2 key) sign-in at the printer.
- The only nearby text: "security fobs like some of the YubiKeys" are listed as cards that give an ISO 14443A ID (so a YubiKey is treated as a card, not as a FIDO2 key). Source: A:47001217796.
- "Windows Hello FIDO2 support" is claimed for the CypherCard on a PC with FIDO2 readers, not for the printer. Source: A:47001217796.
- Windows Hello passwordless on a PC is called out as different from the printer sign-in: A:47001285792 (section 0 item 10).
- A "Passkey button" on the HPAM or HPSA screens is not mentioned anywhere on the site. UNMEASURED.

## 7. First-use self-registration (all methods)

1. Card: first tap leads to a Microsoft sign-in, then the card ID is written to the user's Entra attributes (section 1).
2. QR and BLE: install HPSA; scan the printer QR; sign in to Microsoft in the app; Authenticator must already be in passwordless mode (section 3).
3. "Create" step for the user account is not described: the user must already exist and be licensed (A:47001245378).
4. Each user can hold several IDs: "a total possibility of four unique IDs associated with your login user name". Source: A:47001246513.
5. Region effect: users who travel "will be required to re-register their HP Secure Authentication mobile application for the current Azure Region"; card users "register their Card Once only for the Region". Source: A:47001258067.
6. Reset the phone app: Hamburger menu, Settings, Reset App Defaults, Reset, then "Get Started". Source: https://help.hpauthsuite.com/support/solutions/articles/47001246313-how-do-i-reset-my-hp-secure-authentication-mobile-app
7. Test without hardware (V4.4): "Card Emulation allows administrators to simulate a card tap without requiring a physical card reader or QR code" with "a custom 4 to 6 character alphanumeric card ID" registered in Entra. Source: https://help.hpauthsuite.com/support/solutions/articles/47001250241-what-s-new-

## 8. Username and password, OTP, email, SMS

- Supported but discouraged: "We support authentication using a Microsoft username and password, including OTP (One-Time Passwords), email codes, or SMS verification. However, these methods are not recommended". Source: A:47001285412.
- These are also what the app falls back to when a silent refresh fails: "falls back to interactive login (user name/Password/OTP/MFA passwordless etc.)". Source: A:47001285083.

## 9. Conditional Access effects on every path (setup option that decides if sign-in works)

- The suite "relies on Microsoft Graph APIs and Graph Delegated User permissions. Despite having Admin consent, Microsoft Azure can still restrict access through conditional access policies." Source: https://help.hpauthsuite.com/support/solutions/articles/47001276480-azure-conditional-access-and-policy-tips
- Printers are not managed devices, and the printer browser can look like Android: "Azure AD/Entra ID does not recognize printers as Managed Devices" and "This embedded browser may present itself as an Android-based OS". "Our Latest Release V4.4 and has resolved this issue." Source: A:47001285792.
- A policy aimed only at HPAM is possible: "Under Enterprise applications > Conditional Access." Source: https://help.hpauthsuite.com/support/solutions/articles/47001242637-how-to-setup-azure-passwordless-authentication
- Silent-then-interactive error 50199 is described as normal: https://help.hpauthsuite.com/support/solutions/articles/47001305672-entra-id-sign-in-failure-50199

## 10. Error codes that belong to the sign-in paths (summary table)

| Code | Text on the site | Source |
|---|---|---|
| AI01 | "Please check network connections and base URL values." | A:47001230268 |
| AI02 | "Invalid credentials or server error." | A:47001230268 |
| AI03 | "Please check time and date settings." | A:47001230268 |
| AI04 | "Server error - failed to obtain token." | A:47001230268 |
| AI05 | "Server error - failed to obtain config." | A:47001230268 |
| AI06 | "Graph Org Check failed: HTTP 401" | A:47001230268 |
| AI07 | "Unable to Detect a Supported Card Reader" | A:47001230268 |
| AI08 | "No Card Reader and or SignalR Services Detected" | A:47001230268 |
| AI09 | "QRcode is missing, Please tap your Card / Badge to Sign-in" | A:47001230268 |
| BC01 | "Unable to communicate with your BLE Reader" | A:47001234721 |
| SRS | "Unable to complete a QRCode Sign-in" | A:47001234721 |

(A:47001230268 is https://help.hpauthsuite.com/support/solutions/articles/47001230268-hp-authentication-manager-error-codes ; A:47001234721 is https://help.hpauthsuite.com/support/solutions/articles/47001234721-hp-secure-authentication-error-codes-message)

## 11. What the site does NOT say about sign-in (all UNMEASURED)

- Any screen-by-screen panel flow (only in PDFs and videos not read).
- The security-key and passkey paths (not present).
- The wire format between printer, SignalR, Azure Functions and phone beyond the sentences quoted.
- How the printer app picks which of card, QR or BLE to offer on screen when more than one is on.
- The sign-out flow of the suite (no sign-out article exists).
- Whether HPAM can run without HP Command Centre configuration values (the AuthURL, ClientID, SignalR endpoint are named as printer configuration values in A:47001230268, but the full list is in the deployment PDF).
