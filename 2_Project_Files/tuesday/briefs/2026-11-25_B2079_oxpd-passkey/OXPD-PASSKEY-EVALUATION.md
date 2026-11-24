# OXPd: adding a passkey sign-in option (evaluation for Kam)

Datasec / OXPd, 2026-11-25. Commission B2079 (Kam, live board 2026-11-25 10:00:48). Author: Fable 5.2 agent for Tuesday. Status: findings and a recommendation; nothing in the design documents is changed, nothing was run on a printer or a tenant, nothing was sent to anyone. Every statement about the project carries its record line (`02:` is `02_architecture.md`, `03:` is `03_plan-of-attack-and-build.md`, `05:` is `05_readiness-to-build.md`, `CLAR:` is `CLARIFICATIONS.md`); every statement about Microsoft carries its source key (M1 to M13, listed under Sources); the checking table is in `REVIEW.md` beside this file.

## BLUF

**Recommendation: build the passkey option as a phone-completed sign-in: the panel shows a QR code, the user opens it on their own phone and signs in to Microsoft there with their passkey (Authenticator or a synced passkey), and Microsoft returns the result to the OXPd server (the design's existing mechanism M2, the "phone link"). Fallback: the device-code button the Workpath app already ships as "Sign-in with Passkey" (mechanism M1), for tenants that still allow device code.**

- A passkey cannot be used ON the printer panel today, on either printer generation. The panel has no way to talk to a passkey: the OXPd 2 browser is a 2020 engine with no Bluetooth route to a phone, and HP's own reader guide says FIDO keys are not supported on HP printers. This is an HP question, not something Datasec can build around.
- A passkey CAN be used on the user's phone, in the phone's own browser, with nothing changed in Microsoft's sign-in. Both phone routes are already in the design (M1, M2); both are currently held unbuilt behind open question N-3. The recommendation needs Kam's word to build the Passkey button as a phone route now.
- The honest security statement: a phone route keeps the passkey itself un-phishable, but it does not prove the phone is standing at the printer. Only the on-panel Bluetooth route would prove that, and it is the one that is not feasible.
- Why it matters beyond a new feature: in a tenant that requires "phishing-resistant" sign-in by Conditional Access, the number-match sign-in on the panel (the baseline, W1) cannot satisfy the policy, because Authenticator number match is not a phishing-resistant method (M5). For those tenants a passkey route is the only interactive sign-in that works.
- Paul's specification (v0.2, sent by Kam at 10:09 as a high-level reference) reaches the same first conclusion by its own road: no passkey and no Microsoft sign-in on the printer; the phone does it. It then goes a different way from here on: through the HP Secure Authentication app and a new broker service, where this evaluation uses the phone's own browser and the server the design already has. Section 12 sets the two side by side.
- The page Kam linked records a small change: Microsoft moved the date of one Conditional Access helper for passkey REGISTRATION from end of November 2026 to January 2027. It affects a customer's rollout guidance, not the OXPd build.

## 1. What the linked page says

The page (daily.entra.news, 2026-11-23, "Enable Authenticator Passkey") reports a one-line change to a Microsoft Learn article: the note about the "Microsoft Authenticator Credential Registration" resource now says it "will be available in Jan 2027" where it said the end of November 2026. Checked against Microsoft's own article (M1, section "Workarounds for an authentication strength Conditional Access policy loop"; the article's metadata shows it updated 2026-11-23): the January 2027 wording is there. The earlier wording, the page's list of related changes, and a Message Center item it names (MC1450133, "Users can register a passkey or passwordless sign-in as their first multifactor authentication method") were read on the news page only: **unverified**. The news page says its own summary is AI-generated.

What the helper is for: a tenant whose Conditional Access policy demands a passkey for ALL resources locks users out of REGISTERING a passkey in Authenticator (a loop). Microsoft's workarounds are to scope the policy to named applications, to run two policies with a Temporary Access Pass, or to exclude this new registration resource, which arrives in January 2027 and needs an administrator to provision an enterprise application and opt users in through Graph (M1, same section). **Meaning for OXPd:** none for the build. It belongs in the customer set-up guide Datasec writes for a tenant that wants passkeys at its printers: until January 2027 such a tenant uses one of the other two workarounds.

## 2. Passkeys in Entra ID: the facts that bear on a printer

| Fact | Source |
|---|---|
| Two kinds. Device-bound: the private key never leaves one device (Microsoft Authenticator on iOS or Android, or a FIDO2 security key). Synced: the key is kept by a cloud passkey provider (Apple iCloud Keychain, Google Password Manager) and usable on the user's other devices. Both kinds are generally available | M2 "Synced passkeys (FIDO2)"; M3 opening note |
| Licence: "Passkeys (FIDO2) are available in all Microsoft Entra ID editions, including Microsoft Entra ID Free. No extra licenses are required." Conditional Access (and so authentication strengths) needs Entra ID P1 | M2 opening note; M5 "Prerequisites" |
| Tenant set-up: the Passkey (FIDO2) method is switched on in the Authentication methods policy; passkey profiles (up to three) set, per group, whether attestation is enforced, which types are allowed (device-bound, synced) and which authenticator models (AAGUIDs) | M2 "Passkey profiles", "Enable passkey profiles" |
| Attestation: if enforced, only device-bound passkeys are allowed; synced passkeys do not support attestation. With attestation on, a passkey in Authenticator can only be registered inside the app, not cross-device | M4 "Types of passkeys"; M1 "Authenticator attestation" |
| Authenticator passkeys need iOS 17 or later, or Android 14 or later | M1 "Prerequisites"; M6 |
| Guest users cannot register passkeys (internal or external guests, B2B users in the resource tenant) | M2 "Known issues, Guest users" |
| A passkey is used through a browser or an authentication broker. Web: Chrome, Edge, Firefox and Safari on the listed operating systems. Native apps: through a broker (Authenticator, Company Portal) or MSAL with the system browser; "If you aren't using MSAL, you should still use the system web browser for authentication" | M3 both tabs; M7 "Android", "iOS and macOS" |
| Same-device sign-in: on the phone itself, in its browser, the user picks "Face, fingerprint, PIN or security key" on Microsoft's page and unlocks the passkey | M6 "Same-device authentication in a browser" |
| Cross-device sign-in: the OTHER device's browser shows a QR code; the phone scans it; "Bluetooth and an internet connection are required for this step and must both be enabled on your mobile and remote device"; the devices must reach Google's and Apple's relay addresses (`cable.ua5v.com`, `cable.auth.com`) | M6 "Cross-device authentication"; M1 "Prerequisites" |
| Why a passkey resists phishing: it is bound to the site it was made for ("origin-bound"), and "Every sign-in attempt requires that you're present to unlock the passkey on the device that you use for sign in" | M4 opening |
| Authentication strengths. The built-in "Phishing-resistant MFA strength" allows only FIDO2 security key (passkey), Windows Hello for Business or platform credential, and multifactor certificate sign-in. "Microsoft Authenticator (phone sign-in)" is in the MFA and Passwordless strengths only; a password plus a push notification is in the MFA strength only | M5 table "Built-in authentication strengths" |
| A custom authentication strength can require passkeys from named authenticator models only (for example Authenticator alone) | M2 "Enforce passkey (FIDO2) sign-in" |
| Device code flow: "allows users to sign in to input-constrained devices such as a smart TV, IoT device, or a printer"; the user signs in "via their mobile or PC browser". So the user may use a passkey in that browser. But: "Device code flow is a high-risk authentication method that can be part of a phishing attack"; "Microsoft recommends blocking device code flow wherever possible." A session started by device code stays marked and can be blocked later on refresh ("protocol tracking") | M8 opening, "Authenticating the user"; M9 "Device code flow", "Protocol tracking" |
| Password grant (ROPC): cannot use a passkey at all: "Accounts that don't have passwords can't sign in with ROPC, which means features like SMS sign-in, FIDO, and the Authenticator app won't work with that flow" | M10 "Important" box |

Flows that can carry a passkey: any interactive sign-in in a capable browser or broker, including the browser the user is sent to by a device code or a phone link. Flows that cannot: the password grant; any sign-in surface that is not a WebAuthn-capable browser or broker; cross-device sign-in where the screen showing the QR has no Bluetooth or no internet.

## 3. OXPd's sign-in paths today (from the project's records)

- **The product owner's rule (W1, C-60).** "we must mirror the flow set in extra. for Microsoft authenticator, that is initiate, display 2 digit in iframe, enter 2 digit in authenticator app. we cannot interfere with the login flow or the token management done by microsoft" (`CLAR:546`). The design therefore shows Microsoft's own page in the panel browser (mechanism M4, decision D10; `02:419`, `02:919`).
- **Five mechanisms** (`02:423-427`): M1 device code (QR and user code on the panel, sign-in on the phone); M2 phone link (QR with an authorize address built by the server, auth code with PKCE, the server a confidential client); M3 the HP Secure Authentication phone app over the customer's SignalR gateway; M4 Microsoft's page on the panel; M5 the stored refresh token of No-MFA mode.
- **Which mechanism serves which trigger** (`02:431-435`): on OXPd 2 a known card in MFA mode uses M4, in No-MFA mode M5, an unknown card (enrolment) M4, the phone app M3 (plus M4 when the MFA step is required), and the **Passkey button is "open (N-3)"**. On OXPd 1.x the row still reads M1 or M2 with the Passkey button on M1, and the document says that row contradicts D10 and waits for the M577 panel test (`02:437`; C-76 at `CLAR:796`; the test has not run).
- **A Passkey button already exists in the Workpath app.** Button "Sign-in with Passkey", Entra back end only: it runs Microsoft's device code flow, shows the verification address as a QR plus the user code, and on success signs the user in with "no card, no CSA lookup, no CSA write" (report A1 line 151). It is requirement F12, "Passkey / device-code sign-in (no card)" (`02:76`), built in work package WP3.3 (`03:305`). The second review found the word "passkey" 0 times in the manuals, help articles and video notes, so whether customers see this button on V4.4 is not known (report D1 lines 16 and 502).
- **The documented user paths** (report D1 section 2, lines 86-168): card tap already enrolled; card tap first time (self-enrolment, always with a Microsoft sign-in); phone app by QR; phone app by Bluetooth through the reader; and, on Microsoft's page, whatever the tenant requires. D1 line 464 records the documents' own limit: "no FIDO, FIDO2 or U2F at the printer".
- **Binding rule** (`02:439`): for a known card, the token obtained by M1, M2 or M4 must carry the object id of the user the card maps to, or the sign-in is refused and audited; the phone-side page shows the printer name and a short code so the user can check which printer they are signing in to.
- **The phone routes are on hold.** Open question N-3: if the first printer test of the panel page fails, what then; meanwhile "the phone routes and the relay stay unbuilt" (`05:210`; `03:585`). The relay for M2 (work package WP3.2) is a customer-side Azure release (`02:424`).
- **Phase and tenant (checked).** Everything is deployed in the client's own tenant (`CLAR:478`); "Phase 2 we will have a local server that allows for no internet. For now, internet is essential" (`CLAR:480`); "Phase 1 will be hosted through azure" (`CLAR:552`); "phase 1 needs to be a fully operational build" (`CLAR:849`); decision D1 (`02:910`). A passkey sign-in always needs Microsoft online, so it is a phase 1 feature by nature and has no meaning on a no-internet phase 2 server.
- **The panel hardware and browser.** OXPd 2: Chromium 87 (QtWebEngine 5.15); pop-ups, file input and downloads disabled; cookies and browser features "still under development" (`02:257`; report B1 lines 18, 299-310). B1 line 579: whether "passkey or FIDO flows work there is not answerable from the guides". OXPd 1.x: AppleWebKit 534 to 605, about 2-3 MB of memory for the whole solution (`02:257`). Card readers are USB HID readers owned by the solution; their reports go to the SERVER, not to the panel browser; low-level generic USB access is "not supported this release" (`02:256`; report B1 line 323). HP's reader guide: "Not supported: FIDO, FIDO2 HID, U2F on HP printers" (report A6 line 177).

## 4. The options at a glance

| # | Option | Verdict | At the printer | Phishing resistance | Needs from HP | Needs in Entra | Effort and phase |
|---|---|---|---|---|---|---|---|
| A | Passkey on Microsoft's page ON the panel, phone connected by QR and Bluetooth (true cross-device sign-in) | **Not feasible today** | Would be the best: scan the panel's QR, unlock the phone | Kept in full, with proof the phone is near | A current browser engine with WebAuthn, and a Bluetooth radio the browser can use: neither is in the records | Passkey method on | None possible now; HP roadmap |
| B | FIDO2 security key (USB or NFC) at the panel | **Not feasible** | Tap or insert a key | Kept in full | Firmware support HP's own guide says is absent | Passkey method on | None possible now; HP roadmap |
| C | Server relays a security key plugged into the reader port | **Not feasible, and not acceptable** | Tap a key | Broken by design | n/a | n/a | Rejected |
| D | **Phone link (M2): QR on the panel, passkey in the phone's own browser, result returned to the server** | **Feasible: RECOMMENDED** | Press Passkey, scan QR with the phone camera, unlock the passkey, panel signs in | Passkey kept; nearness NOT proven (QR can be relayed) | Nothing new | Passkey method on; a Web redirect address on the registration; works with public client flows off | Already designed (WP3.2, WP3.3), held by N-3; phase 1 |
| E | Device code (M1): today's "Sign-in with Passkey" button | **Feasible: FALLBACK** | Press Passkey, scan QR, type or confirm a code, sign in on the phone | Passkey kept; nearness NOT proven; Microsoft calls the flow high-risk | Nothing new | Passkey method on; "allow public client flows" on; device code not blocked by Conditional Access | Already designed (WP3.3), held by N-3; phase 1 |
| F | Passkey once, card afterwards: enrol with D or E, then daily card taps redeem the stored token (No-MFA mode, M5) | **Feasible: a companion to D, the customer's choice** | Daily: tap the card, nothing else | The card alone becomes the daily credential (as No-MFA mode today) | Nothing new | As D, plus the tenant's sign-in frequency decides how often the passkey is asked again | No new build beyond D; phase 1 |
| G | Passkey inside the HP Secure Authentication phone app (M3) | **Partly feasible; not a passkey sign-in of the panel** | As today's QR app | The app's own sign-in could use a passkey; the panel session is not derived from it | Nothing | Passkey method on | A phone-app release; value limited |
| H | Microsoft's page on the panel as it stands (M4), user has a passkey | **Not a passkey route; must be tested** | The page may offer a passkey the panel cannot perform | n/a | n/a | n/a | One added test row in the first panel test (S4) |

## 5. Each option in detail

### A. Passkey on the panel, phone connected by QR and Bluetooth

How it would work: Microsoft's page runs in the panel browser as in W1; the user picks "Face, fingerprint, PIN or security key"; the BROWSER draws a QR; the phone scans it; phone and panel find each other over Bluetooth; the user unlocks the passkey (M6 "Cross-device authentication").

Why it is not feasible today:

1. Microsoft states that Bluetooth and an internet connection are required on BOTH devices, the phone and the device showing the QR (M6; M1 "Prerequisites"). No project record shows a Bluetooth radio on an HP printer that the panel browser can use. The only Bluetooth in the product is inside the card reader, which presents itself to the printer as a keyboard (report A1 line 147: "No Bluetooth code exists in the app. The reader does the BLE exchange and emits the credential as keyboard input").
2. The QR in this flow is drawn by the browser itself, not by Microsoft's page and not by our server. The OXPd 2 browser is Chromium 87 from late 2020 with pop-ups disabled and its feature set "under development" (report B1 lines 299-310, 519). HP's guides do not say whether it exposes WebAuthn at all (report B1 line 579). From general knowledge, not verified: phone-as-passkey support entered Chromium well after version 87, and an embedded QtWebEngine 5.15 has no passkey dialog of its own.
3. OXPd 1.x panels are older WebKit engines with a 2-3 MB budget (`02:257`); a partner's attempt to show Microsoft's ordinary page there failed (`02:419`). A passkey ceremony there is not credible.
4. The panel would also have to reach Google's and Apple's relay hosts (M1), which means more entries in the solution's trusted-sites list (report B1 line 356).

What would change the verdict: HP ships a current browser engine on OXPd 2 with WebAuthn and a usable Bluetooth radio. Two HP questions (section 9). Security if it existed: the strongest option; the Bluetooth step proves the phone is beside the printer, so a QR photographed and sent elsewhere is useless.

### B. FIDO2 security key at the panel (USB or NFC)

Not feasible. HP's reader guide says FIDO, FIDO2 HID and U2F are not supported on HP printers (report A6 line 177; report D1 line 464). On OXPd 2 a USB accessory owned by the solution delivers its reports to the solution SERVER; the panel browser never sees the key, and generic USB access is not supported (report B1 line 323; `02:256`). Some fobs work at the printer today only as static-ID cards ("static-ID fobs such as some YubiKeys", report A6 line 177): that is a card number, not a passkey, and gives none of a passkey's protection.

### C. The server relays a security key plugged into the printer

In theory the server could read and write the key's USB reports through the accessories interface and perform the passkey exchange with Microsoft itself. Rejected, for three reasons. It makes our server impersonate a browser on Microsoft's sign-in origin, which is exactly the relay a passkey exists to prevent. It breaks Kam's rule, "we cannot interfere with the login flow or the token management done by microsoft" (`CLAR:546`). And HP states the key class is unsupported (option B).

### D. Phone link (M2): the recommended route

**At the printer.** The user presses "Sign-in with Passkey" (or, by Kam's ruling, any trigger that needs an interactive step in a passkey tenant). The panel shows a QR and a two-digit or short code and the printer's name. The user scans the QR with the phone's camera. The phone's own browser opens a page of the OXPd server that names the printer and shows the same code, then goes to Microsoft's ordinary sign-in page, where the user picks their passkey and unlocks it with face, fingerprint or PIN (same-device sign-in, M6). Microsoft redirects the phone back to the server with a one-time code; the server redeems it with its own credential and the PKCE verifier it kept; the panel, which has been polling, completes the sign-in (`02:424`).

**Why it fits the rules already made.** Microsoft's page is untouched and runs in a real browser; the server is an ordinary confidential web client, as the design already makes it (`02:84`, F20). It is not device code, so a tenant that blocks device code, or has public client flows switched off, can still use it. It works with device-bound Authenticator passkeys and with synced passkeys alike, because the passkey is used on the phone that holds it. It serves both printer generations, because the panel only shows a QR and polls.

**Security.** Kept: the passkey cannot be handed to a fake Microsoft page; the user's password is never typed anywhere; the one-time code is useless without the verifier and credential held by the server (`02:424`). Lost: proof of nearness. A person standing at a printer can photograph its QR and send it to a victim; if the victim opens it and signs in, the session opens on the attacker's printer. Mitigations, most already in the design: the server's page on the phone names the printer and shows the code before Microsoft's page opens (`02:439`); the QR lives for a short time and is used once; for a known card the token must match the card's user or the sign-in is refused and audited (`02:439`); every passkey sign-in is audited with printer and time. A site may also restrict the route to phones on its own network (variant a below). This residual risk is the same class as the device-code route and as today's Workpath Passkey button; it should be said plainly to customers and not described as "phishing-resistant sign-in at the printer".

**What it needs.**

- The phone must reach an https address that ends at the server. Variant (a): the server's own address, for phones on the corporate network. Variant (b): a relay on the customer's existing Function App, which the gateway read showed is a template change and a new offer version (`02:424`; `03:394`). With phase 1 hosted in the client's Azure subscription (`CLAR:552`), the server itself may be reachable from a phone on the internet: that depends on the network shape, open question N-5 (`02:910`). Not established here.
- A Web redirect address on the app registration (already listed for M4 at `02:726`).
- In Entra: the Passkey (FIDO2) method enabled for the users (M2). No licence beyond the tenant's own. If the customer enforces passkeys by Conditional Access: Entra ID P1 and an authentication strength (M5).
- From HP: nothing new.

**Effort and phase.** Phase 1. No new work package: it is WP3.2 (relay, sized "M-L") and WP3.3 (passkey, F12, sized M) as already planned (`03:305`, `03:697`), both held behind N-3. Tests fall inside spike S7, which already aims at Conditional Access tenants (`03:185`).

### E. Device code (M1): the fallback, and today's behaviour

This is what "Sign-in with Passkey" does in the Workpath app today (report A1 line 151): Microsoft's own device code flow, which Microsoft describes for "a printer" by name (M8). The user signs in on their phone at Microsoft's address and may use a passkey there. Building it is parity with Workpath (C-16) and needs no reachable address on the server.

Why it is the fallback and not the recommendation: Microsoft calls the flow "high-risk" and "recommends blocking device code flow wherever possible" (M9). The tenants most likely to want passkeys are the tenants most likely to have blocked it. It also needs "allow public client flows" kept on (`02:423`, `02:726`), which the customers of the "disable public client flows" guide have switched off (report A6 line 304). The design already carries this as risk R7 (`02:959`). Security: as option D, with less control, because the page that asks for the code is Microsoft's generic one and cannot name the printer.

Not established: whether a sign-in completed by device code with a passkey satisfies a Conditional Access authentication strength. The pages read do not say. It should be measured in spike S7 before anything is promised to a customer.

### F. Passkey once, card afterwards

No-MFA mode already works this way with other methods: one Microsoft sign-in at enrolment, the refresh token stored in the user's custom security attributes, then the card alone signs in (report D1 line 119; `02:427`). If the enrolment sign-in is done with a passkey through D or E, daily use is a card tap. This is the least friction a passkey tenant can have at a printer. Its limits are today's: in No-MFA mode "a card number alone is a full credential" (report A1 line 559; `02:653`); and the tenant's Conditional Access decides how long the stored token lives. Microsoft's own example shows an authentication strength satisfied by a passkey sign-in made 24 hours earlier (M5 "Known issues"); whether a stored token redeemed by the server keeps satisfying a customer's policy is UNMEASURED and belongs in S7. This is the customer's setting (default MFA mode on, C-7), not a design change.

### G. Passkey inside the HP Secure Authentication phone app

The app signs the user in to Entra itself, "authorization code with PKCE (S256) in a web view" (report A12 row 10), then sends the printer a per-user secret that the printer treats as a card id (`02:425`). Two limits. First, Microsoft supports passkeys in apps through a broker or the system browser (M3 native apps tab; M7); if the app's web view is an embedded one, passkeys will not work in it until the app is changed. Which kind it is was not established from A12. Second, even with a passkey in the app, the panel's Microsoft session is not created by that sign-in: the ruling stands that the "QR app is not counted as MFA" (`02:425`; `03:554`), and the gateway does not authenticate the publisher (`02:976`). So this improves the phone app's own sign-in and is not a passkey sign-in of the panel. Worth a line in the phone app's backlog, not a route for this feature as the app and gateway stand today. Paul's specification proposes the rebuilt form of this option, in which the server itself checks the phone's token; that changes the verdict from "not a passkey sign-in of the panel" to "a second feasible route, larger to build": section 12.

### H. Microsoft's page on the panel as it stands

Not an option to choose, but a hole to close. If a user who owns a passkey, or a tenant that demands one, reaches Microsoft's page in the panel browser, the page may offer the passkey as the way in. What Chromium 87 on the panel then does is UNMEASURED (report B1 line 579). And in a tenant whose Conditional Access requires the phishing-resistant strength for this application, number match cannot satisfy it (M5 table), so the baseline panel sign-in cannot complete for any user. The first panel test (S4) should record both cases; it costs one more test user with a passkey and one policy.

## 6. Passkey by sign-in path

| Sign-in path (records) | Passkey today (Workpath) | With the recommendation |
|---|---|---|
| Passkey button, no card (F12) | Device code; the user may use a passkey on the phone (A1 line 151) | Phone link first; device code where the tenant allows it and the phone link has no reachable address |
| Known card, MFA mode (F7) | Number match on the panel (W1). No passkey | Unchanged by default. Kam's question K3: in a tenant that requires a passkey, the card tap leads to the phone link, with the binding rule on the card's user |
| Unknown card, enrolment (F9) | Microsoft's page on the panel. No passkey | Unchanged by default; same question K3. Enrolment by phone link binds the card to whoever signed in, as today |
| Known card, No-MFA mode (F8) | Stored token, no interaction | Unchanged. Option F: the stored token may come from a passkey sign-in |
| Phone app QR and Bluetooth (F10, F11) | The app's own sign-in, then number match in MFA mode | Unchanged; option G is a phone-app matter |
| Pull release at sign-in (F17) | Needs no Microsoft step | Unchanged |
| Card emulation, administrator (F18) | Server console | Unchanged |

## 7. Recommendation, fallback, and what would have to be true

**Recommend option D (phone link, M2), with option E (device code, M1) as the fallback, option F offered as the customer's setting, and option A put to HP as a roadmap question.** For the phone link to be the right answer, these must hold:

1. Kam agrees that the Passkey button is a phone route. W1 put the Authenticator step back on the panel; it did not rule on the Passkey button, which is a phone route in the Workpath app today. This needs his word because N-3 currently holds every phone route unbuilt (question K1).
2. A phone can reach the server's redirect address in phase 1, directly or through the relay (N-5; OP-12 at `03:531`).
3. Spike S7 shows, in a tenant with a passkey-only authentication strength: the phone link completes; the server's later refreshes are accepted; and what device code does under the same policy.
4. Customers accept the plain statement of what is and is not protected (section 5, option D, Security).
5. The customer's users are members, not guests, and have iOS 17 or Android 14 or later for Authenticator passkeys (M1; M2 "Known issues").

If 2 fails for a customer and device code is blocked in their tenant, that customer has no passkey route at the printer; this is risk R7's "no fallback" case in a new form (`02:959`), and the answer is then the relay as a requirement.

## 8. What a customer configures in Entra (for the set-up guide)

- Enable Passkey (FIDO2) in Authentication methods; choose passkey profiles: device-bound only (Authenticator, security keys) or also synced; attestation on or off (M2). For Authenticator passkeys, the Authenticator AAGUIDs are listed in M1 "Authenticator AAGUIDs".
- No licence is needed for passkeys themselves (M2). Entra ID P1 only if the customer enforces them with Conditional Access (M5).
- If enforcing: prefer a policy scoped to named applications over "All resources", to avoid the registration loop; from January 2027 the new registration resource is a third way out (M1; section 1).
- On the HP Authentication Manager registration: a Web redirect address for the server (`02:726`). For the device-code fallback only: "allow public client flows" on and no Conditional Access block on device code flow (M9).
- Cross-device Bluetooth settings and the relay hosts (M1 "Prerequisites") do NOT apply to the recommended route: the passkey is used on the phone that holds it.

## 9. Risks

| Risk | Where it bites | Handling |
|---|---|---|
| QR relayed to a victim away from the printer | D and E | Printer name and code on the phone page; short life, single use; binding rule for known cards; audit; optional corporate-network-only setting |
| Customers hear "passkey" as "phishing-resistant at the printer" | Sales and guides | One agreed sentence in the guide; do not use the phrase for D or E |
| Tenant blocks device code, and the phone cannot reach the server | E fails, D fails | Relay (WP3.2) becomes a requirement for that tenant (`02:959`) |
| Conditional Access rejects the server's refresh after a passkey sign-in (location, sign-in frequency) | D, F | UNMEASURED; spike S7 |
| Baseline panel sign-in cannot satisfy a phishing-resistant policy | M4 in passkey tenants | Test in S4; the passkey route is the answer for those tenants |
| The Passkey button is undocumented for customers | Parity scope | Question K2 |
| Microsoft's passkey features are moving monthly (two changes to the linked article in November alone, per the news page: unverified) | Guides age quickly | Date every Microsoft statement in the guide; re-read at release |

## 10. Questions this raises

**For HP (each one question):**

1. Does the OXPd 2 panel browser (QtWebEngine 5.15, Chromium 87) expose the WebAuthn interface to a page, and if so with which authenticator transports?
2. Is a newer browser engine planned for OXPd 2 before production release, and for which firmware version? (The guide says the user agent "will be updated in future releases", report B1 line 300.)
3. Does any FutureSmart 6 device have a Bluetooth radio that the panel browser can use for cross-device passkey sign-in?
4. Is FIDO2 security-key support at the panel (USB or NFC) on HP's roadmap, given the reader guide's "Not supported: FIDO, FIDO2 HID, U2F on HP printers"?

**For Kam (each one question):**

1. K1. May the Passkey button be built as a phone route on both printer generations now (phone link first, device code as fallback), apart from open question N-3?
2. K2. Do customers see "Sign-in with Passkey" on the shipped V4.4 app today? (No manual shows it; report D1 line 502.)
3. K3. In a tenant that requires a passkey, should a card tap in MFA mode, and card enrolment, also lead to the phone link, or is passkey sign-in the card-less button only, as today?
4. K4. Is there a named customer or tender behind this request whose Conditional Access policy we should test against?
5. K5. May the HP Secure Authentication phone app's own sign-in be moved to the system browser so that passkeys work inside it (option G)?
6. K6. Is the passkey option to work with nothing installed on the phone (this evaluation's phone link), or is the HP Secure Authentication app as the user's badge the product you want (Paul's specification), or the first now and the second after?

## 11. Proposed change-log entry (text only; nothing is edited)

For `02_architecture.md`, section 11, and the same entry by reference in `03_plan-of-attack-and-build.md`:

**B2079 (passkey evaluation, 2026-11-25; the product owner's request of 2026-11-25 10:00:48: "evaluate how we can incorporate a passkey auth option into OXPd"):** PROPOSED, not ruled. (1) Section 5.5, matrix, column "Passkey button": OXPd 2 "open (N-3)" and OXPd 1.x "M1" both become "M2 phone link; M1 device code where the tenant allows it and no redirect address is reachable", subject to his answer to K1. (2) Section 5.5, new paragraph after the binding rule: a passkey cannot be performed on the panel of either generation (no WebAuthn-capable browser with a Bluetooth route on OXPd 2: report B1 lines 299-310, 579; FIDO not supported on HP printers: report A6 line 177); the user's passkey is used on the user's own phone through M1 or M2; this keeps the passkey's protection of the credential and does not prove the phone is at the printer. (3) F12 (`02:76`): OXPd 2 and OXPd 1.x cells read "Prompt page with QR: M2, else M1". (4) New risk row: a tenant whose Conditional Access requires the phishing-resistant strength cannot complete the panel number-match sign-in (Microsoft, authentication strengths table, read 2026-11-25); the passkey route is the interactive sign-in for such tenants. (5) Document 03: spike S4 gains two recorded cases (a passkey user on the panel page; a phishing-resistant policy); spike S7 gains three (phone link under a passkey-only strength; the server's refresh after it; device code under the same policy); WP3.2 and WP3.3 no longer hang on N-3 for the Passkey button if K1 is answered yes. (6) Four questions to HP and six to the product owner are added to the master list (OXPD2-1). Source document: `OXPD-PASSKEY-EVALUATION.md`.

## 12. Paul's specification (v0.2): where this evaluation agrees, differs or goes further

The document Kam attached at 10:09 is "Digital Passkey Badge, HP Workpath + OXPd 2.0", v0.2, 24 November 2026; it gives its owner as "Datasec Engineering" and its status as "draft for technical review". Kam's words: "consider it but it does not have the same level of tech approach so take it as a high level reference only". It was read whole. It says of itself that "No SDK or production source was supplied for verification" and that its interfaces "are not HP SDK signatures"; so it was written without the project's records, and the comparison below is between its intent and what those records and Microsoft's pages show. Its technical claims were checked before being relied on; the result of each check is in `REVIEW.md`.

**In one paragraph, what it proposes.** The phone is the badge. The printer shows a QR. The user scans it with the HP Secure Authentication app, which shows the printer's name, signs the user in to Entra with a passkey through the system browser or broker, and confirms to a new "session broker" in the customer's Azure. The broker checks the app's token, issues a one-time grant, and the printer side redeems it and opens a native walk-up session. The broker then gets Microsoft Graph tokens by the on-behalf-of flow. First release: walk-up sign-in and Universal Print pull release only.

**Where the two agree.**

| Point | The specification | This evaluation |
|---|---|---|
| No passkey on the printer | "No WebAuthn or Entra sign-in browser dependency on MFP" | Options A, B, C: not feasible, with the records' reasons |
| The phone holds and uses the passkey | Phone app with system browser or broker; "Avoid embedded WebView" | Option D; Microsoft's own guidance says the same (M7) |
| Customer's own tenant and Azure, no shared Datasec service | Stated as non-negotiable | The product owner's ruling (`CLAR:478`) |
| QR is short-lived, single use, carries no token | 60 second QR, one-time grant | Option D, Security |
| The user confirms the named printer before signing in | "confirm printer name, location and action" | The design's phone-side page (`02:439`) |
| A forwarded QR remains a risk; Bluetooth signal strength is not proof of presence | Test T11, "residual relay risk" | Section 5 option D and section 9, stated the same way |
| A passkey sign-in may reuse an existing Microsoft session; do not promise a fresh passkey at every tap | "Freshness limitation" | Option F and the sign-in frequency risk |
| No tokens on the printer | "No reusable user token" on the device | The design already holds tokens on the server only (`02:427`; `02:642`) |
| Guests out of the first release | Risk table | Microsoft: guests cannot register passkeys (M2) |

**Where they differ.**

| Point | The specification | This evaluation, and why |
|---|---|---|
| What the user needs on the phone | The HP Secure Authentication app (a browser-only path is "optional") | Nothing but the phone's camera and browser. Fewer things to install and release; works for a user who has never set up the app |
| How the server gets the user's tokens | On-behalf-of: the app's token is exchanged by the broker | Auth code with PKCE, redeemed directly by the server (M2 as already designed). Both are standard Microsoft flows. Microsoft's on-behalf-of page (M12) confirms the specification's rule that the token must be issued for the broker's own audience, and that a Conditional Access demand comes back as an "interaction_required" error the phone must then satisfy: one more round trip to build and test |
| New parts | A broker, a new delegated scope and app role, a device registry with certificates, a new API of eight routes | None new: the suite server already is the broker; the registration gains one redirect address |
| Printer identity | "mTLS" or a per-device certificate | Not available on OXPd 2: the records say "no device client certificate"; the device presents a static credential (`02:251`). On OXPd nothing runs on the printer at all, so the specification's "device polls the broker" becomes "the server's own page polls the server" |
| Printer generations | Workpath and OXPd 2.0 | OXPd 2 and OXPd 1.x (the project's scope), and Workpath unchanged |
| Scope of the first release | Sign-in and pull release only; other Microsoft 365 work "gated" | The product owner's ruling is full parity in release 1 (C-16; `02` decision D34). A passkey sign-in that opened only printing would not meet it |
| Custom security attributes | "not an authentication claim or key store" | In the shipped product they are exactly that: card ids and the No-MFA refresh token live there (`02:70` F6, `02:72` F8). The specification's rule would be a change to the product, not a description of it |
| Fallback to device code | Not mentioned | Kept as the fallback, because the Workpath app ships it today (report A1 line 151) |

**Where the specification goes further, and what is worth taking from it now.**

- It makes the phone app's sign-in COUNT. Today the gateway does not check who published an unlock message (`02:976`), which is why "QR app is not counted as MFA". A server that validates the app's token (issuer, tenant, audience, user id) closes that gap. The records show the app already asks for a token for the HP Authentication Manager registration itself (`api://<client id>/.default`, report A12 row 11), so the first step toward this design exists in the shipped app. This is the right long-term shape for the phone app (question K6).
- Protocol hygiene that applies equally to option D and costs nothing to adopt: at least 128 bits of randomness in the QR reference with only its hash stored; states with atomic single redemption; two users confirming one QR, only one wins; its tests T08 to T12.
- A second, independent key in the app for signing individual transactions (its "Phase 2"). Outside this evaluation; it is not a passkey, as the specification itself says.
- Recovery and offboarding rules for the badge; an acceptance test matrix. Useful when the feature is planned in detail.

**Where this evaluation goes further.** It answers whether the printer could do it at all, from HP's guides and the reader guide. It places the feature in the existing design (mechanisms M1 and M2, requirement F12, work packages WP3.2 and WP3.3, open question N-3) so that no new component is needed for a first version. It covers OXPd 1.x. It finds that a phishing-resistant Conditional Access policy breaks the baseline panel sign-in. And it reads the linked Microsoft change.

**Claims in the specification that did not check out, or could not be checked.**

- "Connector-managed printers are not supported for the documented OEM badge path": the Microsoft page it cites (M13, updated 2025-11-12) does not say this as read today. Unverified. The page describes how a PRINTER declares badge release to Universal Print; in the OXPd design the server registers and stands in for the printers and already fetches a user's jobs for release (`02:549-553`), so the fit of that Microsoft path to OXPd is its own question and was not evaluated here.
- "Determine whether QR is static or dynamic" and "confirm whether tokens currently reside on MFP": both are already known from the records. The QR is per printer with five encrypted fields (report A1 line 149); on Workpath the tokens are on the printer, on OXPd they are on the server only.
- "HP publicly describes OXPd2 custom walk-up authentication": agrees with the records (requirement F1, `02:65`). Its HP links were not opened (HP's portal is outside this commission's permitted fetches).
- "Intune wipe alone does not delete a passkey held in another provider": plausible, not checked.

**Net effect on the recommendation: none on the first step, one addition.** Option D stays the recommendation because it is already designed, needs no app and serves both generations. The specification's app-and-broker route is recorded as the candidate second step, with question K6 asking which Kam wants. The two share their server side (QR reference, session states, printer confirmation, single redemption), so building D first does not waste work if the app route follows.

## 13. What could not be established

- Whether the OXPd 2 panel browser exposes WebAuthn at all, and whether any HP printer has a Bluetooth radio usable by it (HP's guides are silent; nothing was run).
- What Microsoft's page shows on the panel to a user who has a passkey, or under a phishing-resistant policy (UNMEASURED; no tenant or printer was used).
- Whether a device-code sign-in completed with a passkey satisfies an authentication strength (not stated in the pages read).
- Whether the phase 1 server will be reachable from a phone on the internet (N-5 is open).
- Whether the phone app's "web view" is an embedded view or the system browser (A12 says "web view" only).
- Whether customers see the Passkey button today (D1).
- The content of Message Center item MC1450133 and the earlier wording of the changed note (news page only).
- Whether the Universal Print OEM badge release path can serve printers that a server stands in for, and the specification's statement about connector-managed printers (section 12).
- HP's public OXPd 2 and Workpath pages cited by the specification (not opened).
- Microsoft pages were read through a fetch tool that converts pages to text; quotations are as that tool returned them on 2026-11-25 and were not compared with the page source by eye.

## Sources

Microsoft (all read 2026-11-25; "updated" is the page's own metadata as returned):

- M1. Enable and support passkeys in Authenticator for Microsoft Entra ID. https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-enable-authenticator-passkey (updated 2026-11-23)
- M2. How to enable passkeys (FIDO2) in Microsoft Entra ID. https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-authentication-passkeys-fido2 (updated 2026-06-15)
- M3. Passkey (FIDO2) authentication matrix with Microsoft Entra ID. https://learn.microsoft.com/en-us/entra/identity/authentication/concept-fido2-compatibility (updated 2026-09-10)
- M4. Passkeys (FIDO2) authentication method in Microsoft Entra ID. https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-passkeys-fido2 (updated 2026-11-17)
- M5. Overview of Conditional Access authentication strengths. https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-strengths (updated 2026-06-26)
- M6. Sign in with passkeys in Authenticator for Android and iOS devices. https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-sign-in-passkey-authenticator (updated 2026-07-06)
- M7. Support passwordless authentication with FIDO2 keys in apps you develop. https://learn.microsoft.com/en-us/entra/identity-platform/support-fido2-authentication (updated 2026-06-15)
- M8. OAuth 2.0 device authorization grant. https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code (updated 2026-06-15)
- M9. Authentication flows as a condition in Conditional Access policy. https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-authentication-flows (updated 2026-03-25)
- M10. Microsoft identity platform and OAuth 2.0 Resource Owner Password Credentials. https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth-ropc (updated 2026-06-15)
- M12. Microsoft identity platform and OAuth 2.0 On-Behalf-Of flow. https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-on-behalf-of-flow (updated 2026-06-15)
- M13. Universal Print Anywhere OEM Badge Release Integration. https://learn.microsoft.com/en-us/universal-print/hardware/universal-print-oem-badge-release (updated 2025-11-12)
- M11. The news page Kam linked (not Microsoft; a community change tracker). https://daily.entra.news/changes/2026-11-23/enable-authenticator-passkey-09/

Project records (read-only, under the OXPd_2 project's `1_Project_Definition/`): `Design/02_architecture.md`, `Design/03_plan-of-attack-and-build.md`, `Design/05_readiness-to-build.md`, `CLARIFICATIONS.md`, `Analysis/A1_auth-manager-source.md`, `Analysis/A6_product-behaviour-spec-from-docs.md`, `Analysis/A12_phone-app-and-legacy-keycloak-api-source.md`, `Analysis/B1_oxpd2-platform-guides.md`, `Analysis/D1_current-solution-operation-second-review.md`, `Registers/HP_QUESTIONS_DRAFT.md`, `Registers/QUESTIONS_BY_OWNER.md`. The line-by-line table is in `REVIEW.md`.

Kam's attachment of 2026-11-25 10:09:04 (internal confidential; read in place, not copied): "Digital Passkey Badge, HP Workpath + OXPd 2.0", v0.2, 24 November 2026, in Tuesday's attachments folder `fleet/state/kam_attachments_1125/`.
