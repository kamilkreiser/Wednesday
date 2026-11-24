# REVIEW: OXPD-PASSKEY-EVALUATION.md (B2079, 2026-11-25)

How to read this. Part 1: every claim about the project, with the record line it rests on. Part 2: every claim about Microsoft, with URL and section. Part 3: the claims of Paul's specification (v0.2) that were checked. Part 4: statements that rest on general knowledge and not on a source. Part 5: what could not be established. Part 6: method and limits.

Record paths are under `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/`. `02` = `Design/02_architecture.md` (364,736 bytes, dated 24 Nov 13:17); `03` = `Design/03_plan-of-attack-and-build.md` (240,583 bytes, 24 Nov 13:17); `05` = `Design/05_readiness-to-build.md`; `CLAR` = `CLARIFICATIONS.md` (144,221 bytes, 24 Nov 15:26); A1, A6, A12, B1, D1 = the reports in `Analysis/`.

**Program check:** 53 (file, line, quoted substring) triples were tested by a script on 2026-11-25; 53 matched at the stated line, 0 missed. Rows marked P in the last column were in that run.

## Part 1. Design and record claims

| # | Claim in the evaluation | Source line | Check |
|---|---|---|---|
| 1 | W1: Microsoft's page is shown on the panel; "we cannot interfere with the login flow or the token management done by microsoft" | `CLAR:546` (C-60); `02:419` | P |
| 2 | Five mechanisms M1 to M5 | `02:423-427` | P |
| 3 | M2: QR with authorize address built by the server, state and PKCE verifier kept on the server; redirect must be reachable from the phone; relay is a template change and a new offer version | `02:424` | P |
| 4 | M3: phone-app sign-in alone is not treated as the MFA step ("QR app is not counted as MFA") | `02:425`; `03:554` | P |
| 5 | Matrix: OXPd 2 Passkey button "open (N-3)"; OXPd 1.x Passkey button M1 | `02:433`, `02:434` | P |
| 6 | The OXPd 1.x row contradicts D10 and waits for the M577 panel test; the test has not run | `02:437`; `CLAR:796` (C-76) | P |
| 7 | Binding rule; phone-side page shows printer name and short code | `02:439` | P |
| 8 | F12 "Passkey / device-code sign-in (no card)" | `02:76` | P |
| 9 | F20: the server is a confidential client by design | `02:84` | P |
| 10 | F6, F8: card ids and the No-MFA refresh token live in custom security attributes | `02:70`, `02:72` | read |
| 11 | F1: custom Authentication Agent (akCustom) on OXPd 2 | `02:65` | read |
| 12 | Workpath "Sign-in with Passkey" is device code; "no card, no CSA lookup, no CSA write" | A1 line 151 | P |
| 13 | "No Bluetooth code exists in the app"; the reader emits keyboard input | A1 line 147 | P |
| 14 | The QR holds five encrypted fields | A1 line 149 | P |
| 15 | "a card number alone is a full credential" in No-MFA mode | A1 line 559; `02:653` | P |
| 16 | "passkey" occurs 0 times in manuals, articles, video notes; whether customers see the button is not known | D1 lines 16, 502 | P |
| 17 | Documented user paths A to E, fallbacks, what decides the paths | D1 lines 86-168, 197-210 | read |
| 18 | "no FIDO, FIDO2 or U2F at the printer" | D1 line 464 | P |
| 19 | "Not supported: FIDO, FIDO2 HID, U2F on HP printers"; static-ID fobs such as some YubiKeys | A6 line 177 | P |
| 20 | A Microsoft sign-in is always required at enrolment, also in No-MFA mode | D1 line 119 | P |
| 21 | "Disable public client flows" guide and its customers | A6 line 304 | P |
| 22 | OXPd 2 browser: Chromium 87 (QtWebEngine 5.15); pop-ups, file input, downloads disabled; cookies and features "under development" | `02:257`; B1 lines 18, 299-310, 519 | P |
| 23 | User agent "will be updated in future releases" | B1 line 300 | P |
| 24 | Whether "passkey or FIDO flows work there is not answerable from the guides" | B1 line 579 | P |
| 25 | Owned HID reader reports go to the server; generic USB "not supported this release" | `02:256`; B1 line 323 | P |
| 26 | The panel browser reaches only the solution's trusted sites | B1 line 356 | P |
| 27 | OXPd 1.x panels: AppleWebKit 534 to 605, 2-3 MB budget; a partner's attempt at Microsoft's page failed | `02:257`; `02:419` | P |
| 28 | OXPd 2: "no device client certificate"; static Basic or bearer credential | `02:251` | P |
| 29 | Tokens only on the server on OXPd | `02:427`; `02:642` (section 6.4 heading; body not re-read) | part |
| 30 | N-3: "the phone routes and the relay stay unbuilt" | `05:210`; `03:585` | P |
| 31 | WP3.3 carries passkey (F12), size M; WP3.2 relay "M-L" | `03:305`; `03:697` | P |
| 32 | Spike S7 aims at Conditional Access tenants; S4 is the first panel test | `03:185`; `03:182` | P (185) |
| 33 | OP-12 (relay path without a token) | `03:531` | P |
| 34 | Web redirect address on the registration; "allow public client flows" for M1 hangs on N-3 | `02:726` | P |
| 35 | Everything in the client's tenant | `CLAR:478` (C-58) | P |
| 36 | "Phase 2 we will have a local server that allows for no internet. For now, internet is essential" | `CLAR:480` (C-58) | P |
| 37 | "Phase 1 will be hosted through azure" | `CLAR:552` (C-60) | P |
| 38 | "phase 1 needs to be a fully operational build" | `CLAR:849` (C-80) | P |
| 39 | D1: client's Azure in phase 1, on-site no-internet in phase 2, network shape N-5 open | `02:910` | P |
| 40 | D10: on-panel page, ruled 2026-11-20 21:59:41 | `02:919` | P |
| 41 | R7: device code blocked by tenant policy; the no-fallback case | `02:959` | P |
| 42 | R24: the gateway does not authenticate the publisher | `02:976` | P |
| 43 | Phone app: auth code with PKCE "in a web view"; scope `api://<client id>/.default` | A12 rows 10, 11 (lines 65, 66) | P |
| 44 | Universal Print: the server "stands in for many printers" and fetches the user's jobs for release | `02:549-553` | P (549) |
| 45 | C-16 full parity in release 1; D34 | `02` decisions table, row D34 (line not pinned); CLARIFICATIONS C-16 heading at `CLAR:94` | read |
| 46 | No ruling of the product owner mentions passkey, FIDO, WebAuthn, device code or phishing | `CLAR`: `grep -o -i -c -E 'passkey|fido|webauthn|device.code|phish'` = 0; positive control in the same file: "authenticator" found at `CLAR:546` | counted |
| 47 | Registers: no open question on passkey, FIDO, WebAuthn or Bluetooth | `Registers/HP_QUESTIONS_DRAFT.md`, `QUESTIONS_BY_OWNER.md`, `DEVIATION-REGISTER_DRAFT.md`: grep hits were for "cookie" and "browser" only (lines 362, 382; 844, 860) | counted; the master list on Jira (OXPD2-1) was NOT read |

## Part 2. Microsoft claims (all pages fetched 2026-11-25)

| Key | Claim | URL | Section | Page metadata |
|---|---|---|---|---|
| M1 | The registration resource "will be available in Jan 2027"; it must be provisioned (app id given on the page) and users opted in through Graph before it can be excluded | https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-enable-authenticator-passkey | "Workarounds for an authentication strength Conditional Access policy loop" | updated 2026-11-23T18:50Z; commit 8e09d5b1 (the same commit id the news page links as the head of its diff) |
| M1 | Authenticator passkeys: Android 14 or iOS 17 and later; cross-device needs Bluetooth and internet on both devices and the relay hosts; no cross-device registration with attestation | same | "Prerequisites for passkeys in Authenticator"; "Authenticator attestation" | same |
| M1 | Authenticator AAGUIDs | same | "Authenticator AAGUIDs" | same |
| M2 | "available in all Microsoft Entra ID editions, including Microsoft Entra ID Free. No extra licenses are required" | https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-authentication-passkeys-fido2 | opening note | updated 2026-06-15 |
| M2 | Passkey profiles, up to three; types device-bound and synced; attestation; AAGUID restrictions | same | "Passkey profiles"; "Enable passkey profiles" | same |
| M2 | Device-bound and synced defined; synced passkeys do not support attestation | same | "Synced passkeys (FIDO2)" | same |
| M2 | Custom authentication strength restricted by AAGUID | same | "Enforce passkey (FIDO2) sign-in" | same |
| M2 | Guests cannot register passkeys | same | "Known issues, Guest users" | same |
| M3 | Both passkey kinds are generally available; browser matrix; brokers; native apps | https://learn.microsoft.com/en-us/entra/identity/authentication/concept-fido2-compatibility | opening note; "Web browsers" tab; "Native apps" tab | updated 2026-09-10 |
| M4 | Origin-bound keys; "Every sign-in attempt requires that you're present to unlock the passkey on the device that you use for sign in"; attestation excludes synced passkeys | https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-passkeys-fido2 | opening; "What are passkeys?"; "Types of passkeys" | updated 2026-11-17 |
| M5 | Conditional Access needs Entra ID P1 | https://learn.microsoft.com/en-us/entra/identity/authentication/concept-authentication-strengths | "Prerequisites" | updated 2026-06-26 |
| M5 | Phishing-resistant strength = FIDO2 security key, Windows Hello for Business or platform credential, multifactor certificate; Authenticator phone sign-in is in MFA and Passwordless only; password plus push in MFA only | same | "Built-in authentication strengths", table | same |
| M5 | An authentication strength satisfied by a passkey sign-in 24 hours earlier (Microsoft's own example) | same | "Known issues" | same |
| M6 | Same-device and cross-device sign-in steps; "Bluetooth and an internet connection are required for this step and must both be enabled on your mobile and remote device" | https://learn.microsoft.com/en-us/entra/identity/authentication/how-to-sign-in-passkey-authenticator | "Same-device authentication in a browser"; "Cross-device authentication" (iOS and Android tabs) | updated 2026-07-06 |
| M7 | Apps: MSAL with system browser or broker; "If you aren't using MSAL, you should still use the system web browser for authentication" | https://learn.microsoft.com/en-us/entra/identity-platform/support-fido2-authentication | "Android"; "iOS and macOS" | updated 2026-06-15 (article dated 2021) |
| M8 | Device code: for "a smart TV, IoT device, or a printer"; the user signs in "via their mobile or PC browser" | https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-device-code | opening; "Authenticating the user" | updated 2026-06-15 |
| M9 | "Device code flow is a high-risk authentication method that can be part of a phishing attack"; "Microsoft recommends blocking device code flow wherever possible"; protocol tracking | https://learn.microsoft.com/en-us/entra/identity/conditional-access/concept-authentication-flows | "Device code flow"; "Protocol tracking" | updated 2026-03-25 |
| M10 | ROPC: "Accounts that don't have passwords can't sign in with ROPC, which means features like SMS sign-in, FIDO, and the Authenticator app won't work with that flow"; incompatible with MFA | https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth-ropc | "Warning" and "Important" boxes | updated 2026-06-15 |
| M12 | On-behalf-of: the assertion "must have an audience (aud) claim of the app making this OBO request"; a Conditional Access demand returns "interaction_required" to be surfaced to the client | https://learn.microsoft.com/en-us/entra/identity-platform/v2-oauth2-on-behalf-of-flow | "Middle-tier access token request"; "Error response example" | updated 2026-06-15 |
| M13 | OEM badge release: the printer declares `owner-authorized-badge` and calls Get-Jobs, Fetch-Job, Acknowledge-Job with `requesting-user-uri` | https://learn.microsoft.com/en-us/universal-print/hardware/universal-print-oem-badge-release | "Expected Behavior of Printer" | updated 2025-11-12 |
| M11 | News page (not Microsoft): the change of 2026-11-23, +1 / -1 lines | https://daily.entra.news/changes/2026-11-23/enable-authenticator-passkey-09/ | whole page | read 2026-11-25 |

**Read on the news page only, marked unverified in the evaluation:** the earlier wording ("at the end of November 2026"); the list of related changes (28 October, 17 November, 23 November, 26 October); Message Center item MC1450133 and its title. The news page states its summary is AI-generated.

## Part 3. Paul's specification (v0.2): claims checked

| Claim in the specification | Checked against | Result |
|---|---|---|
| No WebAuthn or Entra sign-in on the MFP is the right direction | B1 lines 299-310, 579; A6 line 177 | Agrees with the records |
| Mobile: system browser or broker; avoid embedded WebView | M3, M7 | Agrees with Microsoft |
| On-behalf-of needs a token for the broker's own audience; never an ID token | M12 | Agrees (audience rule confirmed; the ID-token sentence was not looked for) |
| Claims challenges must go back to the phone | M12 "Error response example" | Agrees |
| "HP publicly describes OXPd2 custom walk-up authentication" | `02:65` (F1) | Agrees with the records; HP's page not opened |
| Device identity by mTLS or per-device certificate | `02:251` | Not available on OXPd 2 as the records describe it |
| CSA is "not an authentication claim or key store" | `02:70`, `02:72` | Contradicts the shipped product's use |
| "Connector-managed printers are not supported for the documented OEM badge path" | M13 | Not found on the cited page as read; unverified |
| QR static or dynamic is to be discovered; tokens on MFP to be confirmed | A1 line 149; `02:427` | Already known from the records |
| First release = sign-in and pull release only | C-16 (`CLAR:94`), D34 | Narrower than the product owner's parity ruling |
| Guests, cross-tenant, national clouds out of the first release | M2 (guests) | Guests agree; national clouds are requirement F19 in the design (`02` section 3.2), so "out" differs from the records |
| Intune wipe does not delete a passkey held in another provider | none | Not checked |
| Its nine reference links | two Microsoft links opened (M12, M13) and three overlap M2, M3, M7; the two HP links and two Microsoft links (claims challenge, partner cloud integration) were not opened | Part checked |

The specification is marked internal confidential. It was read in place (`fleet/state/kam_attachments_1125/`), quoted in short phrases only, and not copied anywhere.

## Part 4. Statements that rest on general knowledge (flagged as such in the evaluation)

- Phone-as-passkey ("hybrid") support entered Chromium well after version 87; an embedded QtWebEngine 5.15 has no passkey dialog. Not verified against any source in this pass. The verdict on option A does not depend on it alone: Microsoft's Bluetooth requirement (M6, M1) and the absence of any record of a panel Bluetooth radio stand without it.
- The description of how a QR could be photographed and relayed to a victim (options D and E) is reasoning, not a cited attack report. Microsoft's own page calls device code "part of a phishing attack" (M9); the same reasoning is applied to the phone link.
- That a phone-link sign-in with a passkey satisfies a phishing-resistant authentication strength is inferred from the strength's definition (M5: the method is in the strength) and Microsoft's 24-hour example; it is listed as to be measured in spike S7.
- That option C (server-relayed security key) would "impersonate a browser on Microsoft's origin" is reasoning from how WebAuthn binds a passkey to a site (M4).

## Part 5. What could not be established

1. Whether the OXPd 2 panel browser exposes WebAuthn; whether any HP printer has a Bluetooth radio the browser can use. (HP questions 1 to 3.)
2. What Microsoft's page does on the panel for a passkey user or under a phishing-resistant policy. UNMEASURED.
3. Whether device code completed with a passkey satisfies an authentication strength. Not stated on the pages read.
4. Whether Conditional Access accepts the server's later refreshes after a passkey sign-in on the phone. UNMEASURED.
5. Whether the phase 1 server is reachable from a phone on the internet (N-5 open).
6. Whether the phone app's "web view" is embedded or the system browser (A12 row 10 says "web view" only; the app source was not opened in this pass).
7. Whether customers see the Passkey button on V4.4.
8. MC1450133's content; the earlier wording of the changed note.
9. The fit of Universal Print OEM badge release to printers a server stands in for.
10. The Jira master list OXPD2-1 was not read (Jira is outside what this pass opened), so a passkey question already on it would not have been seen. The three register files in `Registers/` hold none.
11. `02` sections 6.4 and 7.1 and the whole of `03` were read by heading and by grep hits, not end to end; `02` section 5.5 (lines 417-530) and sections 3.1-3.2 and 4 were read whole.

## Part 6. Method and limits

- Microsoft pages were read through a fetch tool that converts a page to text. Quotations are as returned on 2026-11-25 and were not compared with the page source by eye.
- Nothing was run on a printer, a simulator, a tenant or Azure. No `az` command. Nothing was sent to anyone. Nothing was written outside `tuesday/briefs/2026-11-25_B2079_oxpd-passkey/` and the scratch folder `fleet/state/s326/b2079/`. No file of the OXPd project was changed.
- Requests to outside services carried only the public URLs listed in Part 2.
- Render: the `.docx` by the hand-written WordprocessingML script the design documents use (`fleet/state/s320/A/docx02.py`, a copy in the scratch folder with one line changed, the document title property); the `.pdf` by `2_Project_Files/tools/md2pdf/md2pdf.sh` (pandoc to HTML, headless Chrome), which is what the design PDFs' metadata shows (Creator HeadlessChrome, Title the file name).
