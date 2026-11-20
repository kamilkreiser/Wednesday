# B1817 STAGE 1: the design change list for the product owner's rulings of the evening of 2026-11-20 (no design document edited)

Datasec / OXPd 2. Written 2026-11-21 by the stage-1 agent of commission B1817 (`TUESDAY/2_Project_Files/tuesday/briefs/2026-11-20_B1817_OXPD-DESIGN-REVISION_COMMISSION.md`), on Opus by the product owner's word of 2026-11-21 ("fable limit reached.  please continue with opus"). An earlier attempt of this stage (Fable, 2026-11-20 about 22:21) left a file at this path; it was copied byte for byte (sha1 equal) to `TUESDAY/2_Project_Files/fleet/state/s302/d1817/B1817_DESIGN-CHANGE-LIST_2026-11-20.md.partial` before this file replaced it, and was not used as a source. Every line number below was re-read from the design documents as they stand (`02_architecture.md` 1,126 lines, `03_plan-of-attack-and-build.md` 529, `05_readiness-to-build.md` 266, all dated 2026-11-20 14:01) and each quoted excerpt was checked by program to be a substring of the line it cites (section 7). Nothing here is a decision: class (c) rows are open questions with the default the build takes meanwhile.

## The product owner's words (the authority; verbatim as the commission prints them, its lines 6 to 11)

- **W1**, 21:59:41: "if my ruling moved it to the phone that is a mistake.  we must mirror the flow set in extra.  for Microsoft authenticator, that is initiate, display 2 digit in iframe, enter 2 digit in authenticator app.  we cannot interfere with the login flow or the token management done by microsoft" ("extra" is read as Entra, a dictation slip: the coordinator's reading, not his word.)
- **W2**, 22:00:26: "of the two tools, check that they do the same thing.  I do not think so, but whichever is newer."
- **W3**, 22:01:21: "p6.  yes.  clients deploy to their own tenant and our solution is subservient to the source of truth they use, currently entra"
- **W4**, 22:03:25: "one server per site on the customer's network is not inconsistent with them deploying through azure in their tenant.  Phase 1 will be hosted through azure and this offers different hosting options for the client"
- **W5**, 22:03:48: "OXPd runs in the clients azure subscription"
- **W6**, 22:04:02: "please go ahead and revise all docs and start building"
- His notes of 21:04, cited **N:line** (line of `TUESDAY/0_Brain/reference/2026-11-20_kam-oxpd-questions-notes/kam_notes_verbatim_2026-11-20_2104.txt`), each answer labelled by him (P2, P3, A2, A4 ...). The question each answers is the one of that label in `Registers/QUESTIONS_BY_OWNER_v2_2026-11-20.docx` (read by program); where a label alone does not fix the meaning, the row says so.
- Not granted by any of these words, and so not written as granted anywhere below: any Azure resource or spend; anything sent to HP or to any person (commission line 14; C-42's detail "Nothing goes to HP or any person, no Azure, no spend.").

---

## 4. Where two of his statements, or a statement and a ruled clarification, pull against each other (FIRST, for the product owner; none resolved here)

**P-1. C-29 against W1, and how far W1 reaches.** C-29 is the tap "Phone code or phone link"; the card's option detail reads "User finishes Microsoft sign-in on their phone; QR app is not counted as MFA." (board data file, card `datasec-oxpd-q02-phone-signin-step-1118`). W1 calls the phone move "a mistake". **What W1 reverses:** the first half of the option ("User finishes Microsoft sign-in on their phone"). **What W1 does not touch and so stands:** "QR app is not counted as MFA". **The pull that remains:** the option he did NOT tap, c "Must be on the printer screen", carried the detail "Only possible on newer (OXPd 2) printers, after a test." W1 names no printer generation, C-22 keeps OXPd 1.x printers (FutureSmart 4.7 and up) in scope, and the design records a partner's on-panel Microsoft sign-in failing on OXPd 1.x on memory and certificate trust (`02:414`, report C2 section 4.4). Whether the on-panel step is required on OXPd 1.x panels too, or on OXPd 2 only, is his to say (open question N-1).

**P-2. W1 "we cannot interfere with the login flow" against his note P3 "mirror how the current solutions work" (N:14).** The current product shows Microsoft's page inside the panel's embedded browser and the user types two digits into Authenticator (report D1 section 7 row 1, `AMUG p.7`; report D3 section 2.1, the video at 0:27 to 0:33). But the design records that today's Workpath path "depends on cookie wipe, script injection and a spoofed user agent that the server cannot reproduce in a device browser" (`02:414`, report A1 section 5.4), and the known-card sign-in passes a `login_hint` (`02:420`). Mirroring today's mechanics may itself be interference in the sense of W1; not interfering may mean a flow that differs from today's in those details. Not resolved (N-2, N-4).

**P-3. W1 "or the token management done by microsoft" against C-7 and the design's token custody.** C-7 ("As is, off by default") keeps No-MFA mode, in which a stored refresh token is redeemed by our side with no user present (`02:71`, F8); the design's server obtains, holds, refreshes and uses every user's tokens (`02:635`, D6 at `02:904`), on C-25 (one registration shared with Workpath, `02:902`). Whether that is "token management done by microsoft" (Microsoft issues and refreshes; we hold and present) or interference with it, his words do not say (N-4).

**P-4. C-26 against W4, W5 and his notes A4, A5.** C-26 is the tap "On each site's network" on a card titled "Where will the server run for the first customers: on each site's network, one per company, or hosted by Datasec?", option detail "Customer hosts one server per site.". W5: "OXPd runs in the clients azure subscription"; W4: "Phase 1 will be hosted through azure"; A5 (N:18): "Phase 2 we will have a local server that allows for no internet.  For now, internet is essential."; A4 (N:17): "everything including oxpd servers need to be in their tenant". He himself writes (W4) that one server per site on the customer's network "is not inconsistent" with deploying through Azure in their tenant, so he does not see a conflict; the documents still need to know which shape Phase 1 has: (i) a server in the client's Azure subscription for each site, joined to that site's network; (ii) a machine at each site deployed and governed through the client's Azure; (iii) Azure-hosted servers in Phase 1 and the on-site server in Phase 2 (A5 read plainly). Report D2 section 6.1 row 1 reads A4 and A5 as contradicting the ruled D1. Bearing on every option: the platform facts the design measured (`02:248`, `02:899`): both printer generations need two-way traffic, OXPd 1.x forbids address translation and fixes port 7627; the design's rejected option for D1 was "(c) customer Azure VM with VPN to sites". Not resolved (N-5).

**P-5. C-17 against W4 (and A7).** C-17 is the tap "Both equally", detail "Container, appliance and Windows all at release.". W4: Phase 1 "will be hosted through azure and this offers different hosting options for the client". If Phase 1 runs in the client's Azure subscription, whether all three packagings (Linux container, virtual appliance, Windows service) are still release-1 deliverables, and whether an Azure deployment (a template or Marketplace offer, as the current product's Azure pieces are delivered: report D2 section 6.1 row 2, reading A7 "Azure marketplace", N:20) is a fourth, is not said. Not resolved (N-6).

**P-6. C-43 against W2, and both against A15.** C-43: "also, Datasec has a deployment utility so you should use this or amend it so we can use it for this project" (the HPK Deployment Utility he attached). W2: "of the two tools, check that they do the same thing.  I do not think so, but whichever is newer." A15 (N:25), answering "Where should the OXPd changes to the HPK Deployment Utility be made: a branch of the utility's own repository, or somewhere else?": "separate app but with the intention of integration after MVP". **Measured (report D2 section 3, re-checked by program for this list):** the two tools do the same job (put Datasec's Workpath apps and their configurations on printers, in batches, with retries and per-printer results) by different means and not with the same steps: the Utility drives HP's `HPKTool-cli.exe` and carries an attestation step; HP AuthSuite Manager calls the printer's package-management service itself, has discovery, a Windows service with scheduled runs and one password per device, and has no attestation step (0 files name it). **"Newer" is not one answer:** by file dates the Manager is newer (338 of 344 files dated 2026-11-11, against 138 of 139 dated 2026-10-09); by version number the Utility's 3.0.0 is higher than the Manager's 1.1.0 (two separate version series). And A15's "separate app" may mean the OXPd deployment is a separate app from either tool until after the MVP, which pulls against "use this or amend it". Not resolved (N-9).

**P-7. A4 "Everything is deployed in the clients tennant" (N:17) against A6 "Yes, license server through Azure or Datasec.  2 deployment optiuons" (N:19), and against the question A4 answered.** A Datasec-hosted licence server is not in the client's tenant. And A4 was asked about the Universal Print app registration, which the documents and the manual give as Datasec's own multi-tenant registration (`02:725`; report D2 section 6.1 row 4). Whether "everything" excludes Datasec's print registration (each customer registers their own) is not said (N-14).

**P-8. W6 "start building" against C-42's limit, for a product whose Phase 1 is Azure-hosted (W4, W5).** C-42's detail binds "no Azure, no spend", and the coordinator told him on the board that Azure resources and spend stay his (commission line 14). The second test the rulings make urgent (a printer at a site reaching a server in Azure, part 3) cannot run without an Azure resource. Not resolved: the test is prepared and waits for his word (N-5).

**P-9. A18 "assume English for phase 1 but add to jira questions" (N:28) against C-16 "Full match of everything".** The OneDrive and SharePoint sources hold eight string sets (`02:102`); the manuals say English only (report D1 section 7 row 20). If the shipped apps show translations, English-only Phase 1 is less than a full match. Small, and he asked for the question to go on the master list: OP-21 stays open, as he said; no new open question is added for it.

---

## 1. The change table, one row per place a document must change

Columns: **Id**; **Where** (document:line, re-read); **As it stands** (an excerpt, checked to be a substring of that line); **By** (his word or answer, quoted); **Proposed** (new text for (a) and (b); the open question for (c)); **Class**. Report citations: D1, D2, D3, A12, B4 are `Analysis/` reports of 2026-11-20 evening, by section and row.

### 1A. The Microsoft step (W1)

| Id | Where | As it stands | By | Proposed | Class |
|---|---|---|---|---|---|
| R1-01 | 02:17 | "the interactive Microsoft step moves to the user's phone (device-code or a phone redirect)" | W1 “if my ruling moved it to the phone that is a mistake” | "What changes for users: not the Microsoft step. As Entra sets it today, the sign-in is started at the printer, Microsoft's page shows a two-digit number on the panel and the user enters it in the Authenticator app (W1, verbatim beside it); nothing of ours sits in Microsoft's login flow or token handling. The panel browsers' limits (section 5.5) make this the first test on a printer." The present product shows the number on the panel (D1 s7 row 1; D3 s2.1 0:27-0:33). | b |
| R1-02 | 02:70 | "now on the phone (changed by ruling, C-29)" | W1 | F7: replace with "shown on the printer panel, as today (W1, 2026-11-20 21:59:41, which reverses the phone half of C-29)"; OXPd 2 column: "Microsoft's page in the panel browser, number shown on the panel, entered in Authenticator; first printer test (S4)". | a |
| R1-03 | 02:70 | "Prompt page shows QR and code; Microsoft step on the phone only" | W1; P-1 | F7, OXPd 1.x column: OPEN N-1 (on-panel step on OXPd 1.x panels). Default meanwhile: the target is the same on-panel step; nothing of the phone route is built for 1.x before the 1.x panel test reports. | c |
| R1-04 | 02:72 | "Prompt page with QR and code; enrolment identity taken from the verified token" | W1 | F9: "Prompt page starts Microsoft's sign-in on the panel (as F7); enrolment identity taken from the verified token". | a |
| R1-05 | 02:184 | "the page is now on the phone: changed by ruling, C-29" | W1 | "the page stays Microsoft's and is shown on the panel (W1)". | a |
| R1-06 | 02:256 | "no Microsoft sign-in page on the 1.x panel; on OXPd 2 only after a spike" | W1 | "Microsoft's sign-in page on the panel is the design (W1); on OXPd 2 the Chromium 87 behaviour is the first printer test (S4); on OXPd 1.x see N-1". | a |
| R1-07 | 02:367 | "Entra: auth-code + PKCE (confidential client), device-code, refresh redemption" | W1 | C7: auth code + PKCE with Microsoft's page in the panel browser is the interactive route; whether device code (M1) is kept at all is N-3. Default: device code is not built before test 1 reports. | c |
| R1-08 | 02:369 | "sign-in prompt (QR, code, enrolment, errors)" | W1 | C9: "sign-in pages (the page that starts Microsoft's sign-in in the panel browser, enrolment, errors; the phone-app QR of F10)". | a |
| R1-09 | 02:414 | "The panel browser does not host Microsoft's sign-in page in the default design." | W1 | "The panel browser hosts Microsoft's sign-in page in the default design: the sign-in is initiated, the two-digit number is displayed on the panel, the user enters it in the Authenticator app (W1); nothing of ours sits in Microsoft's login flow or token handling. The risks this paragraph names do not go away and become the FIRST printer test (S4): on OXPd 2, Chromium 87 with undefined cookie behaviour between users and no pop-ups [B1 s5.3]; on OXPd 1.x, the partner's failures [C2 s4.4]. What the design does if that test fails is open (N-3)." Strike "So the interactive Microsoft step is moved off the panel". | a |
| R1-10 | 02:414 | "The panel browser does not host Microsoft's sign-in page in the default design." | W1 “display 2 digit in iframe” | OPEN N-2: inside a frame (his word) or as a full-page redirect within the panel browser. Whether Microsoft's sign-in page may be framed is UNMEASURED (no report mentions framing: section 7). Default: the panel page is written so that either works; test 1 tries the frame first, then the full-page redirect; the result goes to him. | c |
| R1-11 | 02:418 | "M1 Device code (baseline)" | W1 | M1 is no longer the baseline. Whether M1 stays as a fallback is N-3; default: not built before test 1 reports. | c |
| R1-12 | 02:419 | "M2 Phone redirect (auth code + PKCE, confidential)" | W1 | As R1-11: M2 and its gateway relay are kept, or not, by N-3; default: not built before test 1 reports. | c |
| R1-13 | 02:420 | "on OXPd that step becomes M1 or M2 (ruled, C-29" | W1; C-29 option detail “QR app is not counted as MFA” | "on OXPd that step is Microsoft's page on the panel (W1), as on Workpath; the phone-app sign-in alone is still not treated as the MFA step (C-29's option detail, not reversed by W1)". | a |
| R1-14 | 02:421 | "OXPd 2 only, and only if spike S4 passes on real firmware" | W1 | M4 becomes the baseline: "OXPd 2: the design; spike S4 is the first printer test. OXPd 1.x: N-1". Strike "Optional, per tenant; never on OXPd 1.x". | a |
| R1-15 | 02:428 | "M1 or M2 (M4 if enabled)" | W1 | Matrix, OXPd 2 row: "M4" for known card MFA and for enrolment; "M3 (+ M4 if the MFA step is required)"; Passkey button: N-3. Heading "(ruled, C-29)" becomes "(W1, 2026-11-20 21:59:41)". | a |
| R1-16 | 02:429 | "M3 (+ M1/M2)" | W1; P-1 | Matrix, OXPd 1.x row: OPEN N-1; default as R1-03. | c |
| R1-17 | 02:432 | "the phone-side sign-in shows the panel's printer name and a short code" | W1 | The oid binding check stays (it reads the token Microsoft returns; it does not change the flow); whether `login_hint` for a known card counts as interfering is N-4; the phone-side printer-name check applies only if N-3 keeps M1 or M2. Default: oid check kept, `login_hint` passed as Workpath does. | c |
| R1-18 | 02:463 | "Prompt page: QR + user code (device code) or QR (phone redirect)" | W1 | Sequence 5.5.1: "Prompt page: Microsoft's sign-in in the panel browser; the number is shown on the panel"; next line "U->>P: enter the number in Authenticator"; "S->>E: receive code" (auth code redemption). | a |
| R1-19 | 02:509 | "Lightweight ES5 page: QR + code, polls server by XHR" | W1; P-1 | Sequence 5.5.2 (OXPd 1.x): OPEN N-1; default as R1-03. | c |
| R1-20 | 02:717 | "(and the relay URL if M2b is chosen)" | W1 | Option A: "add a Web platform redirect URI on the server's FQDN for the panel sign-in (M4)"; the relay URL and "allow public client flows" clauses hang on N-3. | a |
| R1-21 | 02:720 | "sign-ins now come from the server's IP (printer-subnet location rules no longer match)" | W1 + D3 s5 row 1 | "the interactive sign-in comes from the printer's panel browser, as today; token redemption and refresh come from the server's address (in the client's Azure for Phase 1, W5). Today a policy keyed on device platform Android and iOS catches the printer and Datasec's fix adds 'Require authentication strength: Passwordless MFA' as a one-of alternative (D3 s2.1 3:00-3:08). Whether the OXPd panel browser is seen as the same platform is UNMEASURED: spike S7." | b |
| R1-22 | 02:908 | "(b) as baseline on both platforms; on-panel only on OXPd 2 after spike S4, per tenant" | W1 | D10: choice "(a) on-panel page, as Entra sets it (W1); first printer test S4; OXPd 1.x N-1; if S4 fails N-3"; status "Ruled 2026-11-20 21:59:41 (reverses the phone half of C-29)". | a |
| R1-23 | 02:946 | "D10 off-panel sign-in" | W1 | R5 mitigation: "D10 on-panel sign-in as Entra sets it (W1); the browser limits are the first printer test (S4); what follows a failure is N-3". | a |
| R1-24 | 02:948 | "M2 phone-redirect as a second mechanism" | W1 | R7 rests on device code as the baseline; with M4 as baseline its case changes. Whether R7 is kept, rewritten or closed follows N-3. Default: kept as written, marked "rests on N-3". | c |
| R1-25 | 02:973 | "A clause of HP's older SDK guide forbids reverse engineering" | W1 | New risk after R32: "R33 Microsoft's sign-in page in the panel browser: on OXPd 2 Chromium 87 cookie isolation between users is undefined and there are no pop-ups [B1 s5.3]; whether the page can be framed is unmeasured; on OXPd 1.x a partner's attempt failed [C2 s4.4]. Mitigation: first printer test (S4); outcome to the product owner (N-3)." | a |
| R1-26 | 03:57 | "else M4 is dropped" | W1 | S4 is the first printer test (Monday, see part 3). Pass: the number shows on the panel, entry in Authenticator completes, two users in sequence never share a Microsoft session, no pop-up is needed; recorded: frame or full page (N-2). Strike "else M4 is dropped". | a |
| R1-27 | 03:57 | "else M4 is dropped" | W1 | What a failed S4 leads to: OPEN N-3 (nobody decides it here). Default: the result goes to the product owner with options; M1, M2 and the relay stay unbuilt meanwhile. | c |
| R1-28 | 03:60 | "Device code and phone-redirect (server FQDN and Function App relay" | W1 + D3 s5 row 1 | S7 re-aimed: the panel sign-in (M4) and the server's refresh in a tenant with Conditional Access, including the D3 policy (Office 365, Android and iOS, "Require app protection policy") before and after Datasec's fix; device code and relay only if N-3 keeps them. | b |
| R1-29 | 03:76 | "(No-MFA and MFA via device code)" | W1 | "(No-MFA, and MFA through Microsoft's page on the panel)". | a |
| R1-30 | 03:82 | "device-code QR shown, phone sign-in completes" | W1 | E1.2: "Microsoft's page on the panel shows the number, the user enters it in Authenticator, sign-in completes; refused if a different user signs in (binding rule)". | a |
| R1-31 | 03:102 | "phone-redirect mechanism M2 with the gateway relay (C-29, C-27)" | W1 | Phase 3 order: strike from the list; M2 hangs on N-3. | c |
| R1-32 | 03:107 | "C-29 (Microsoft step on the phone, F7)" | W1 | Remove from deviation class (1): the Microsoft step on the panel is today's behaviour, not a deviation (W1). | a |
| R1-33 | 03:155 | "a minimal enrolment by device code" | W1 | WP1.4: "a minimal enrolment through Microsoft's page on the panel". | a |
| R1-34 | 03:157 | "prompt page, OneDrive pages" | W1 | WP1.6: "the page that starts Microsoft's sign-in on the panel (frame or full page, per S4 and N-2), OneDrive pages". | a |
| R1-35 | 03:178 | "Phone-redirect sign-in (M2)" | W1 | WP3.2: conditional, not planned until N-3 keeps M2. | c |
| R1-36 | 03:179 | "Enrolment completeness (phone redirect" | W1 | WP3.3: "Enrolment completeness (Microsoft's page on the panel, the 15-card limit, errors)". | a |
| R1-37 | 03:268 | "M2 falls back to the server FQDN for phones on the corporate network" | W1 | The gateway-relay blocker line rests on M1/M2 as baseline: kept only if N-3 keeps them; default: marked "rests on N-3". | c |
| R1-38 | 03:270 | "the baseline is phone code or phone link (C-29)" | W1 | "S4 is the first printer test; the on-panel page is the baseline (W1); a failure is N-3". | a |
| R1-39 | 03:307 | "Phone code or phone link" | W1 | Q2 row, Answer: add "; the phone half reversed by the product owner on 2026-11-20 21:59:41 (W1); 'QR app is not counted as MFA' stands". | a |
| R1-40 | 05:116 | "the second step you already ruled (phone code or phone link, C-29) bounds it" | W1 | "the second step (Microsoft's page on the panel with the Authenticator number, as you set it on 2026-11-20 at 21:59) bounds it". | a |
| R1-41 | 05:174 | "The phone-link relay needs one address" | W1 | OP-12: the relay serves M2 only; default changes from "Yes" to "not before S4 reports" (N-3). | c |
| R1-42 | 05:7 | "Phase 0 has started, on the work that needs no hardware." | W1 | Add a BLUF item: "The Microsoft sign-in step stays on the printer panel, as today (your words of 21:59); the phone move was a mistake and is reversed. The first printer test is whether the panel browsers carry Microsoft's page safely." | a |

### 1B. Token handling (W1, second sentence)

| Id | Where | As it stands | By | Proposed | Class |
|---|---|---|---|---|---|
| R1-43 | 02:18 | "live once, encrypted, on the customer's server" | W1 “we cannot interfere with the login flow or the token management done by microsoft”; P-3 | OPEN N-4. Default: unchanged; the server uses Microsoft's own library and the tokens Microsoft issues, holds them encrypted, never sends them to a device, and designs no new token handling. | c |
| R1-44 | 02:139 | "Microsoft tokens never leave the server" | W1; P-3 | N2: N-4; default as R1-43. | c |
| R1-45 | 02:366 | "holds the user's access + refresh tokens per device session" | W1; P-3 | C6: N-4; default as R1-43. | c |
| R1-46 | 02:618 | "C6 memory; persisted encrypted only for crash recovery" | W1; P-3 | 6.2 row: N-4; default as R1-43. | c |
| R1-47 | 02:635 | "Microsoft tokens are obtained, held, refreshed and used only by the server" | W1; P-3 | 6.4: N-4; default as R1-43. | c |
| R1-48 | 02:904 | "memory + encrypted persistence during the session" | W1; P-3 | D6: status "Firm" becomes "Firm in text; N-4 open". | c |
| R1-49 | 03:353 | "accepted with encryption and on-premises hosting" | W1; W5 “OXPd runs in the clients azure subscription” | 8.1 line: "on-premises hosting" becomes "hosting in the client's Azure subscription for Phase 1 (W5)" (a); the custody itself: N-4 (c). Class taken as the weaker. | c |

### 1C. Hosting (W3, W4, W5; notes A4 to A7)

| Id | Where | As it stands | By | Proposed | Class |
|---|---|---|---|---|---|
| R2-01 | 02:14 | "on the customer's own network, one server (or a two-node pair) per site" | W5; W4 “Phase 1 will be hosted through azure”; A5 “For now, internet is essential.” | "Where it runs: in Phase 1, in the client's own Azure subscription and tenant (W5, W4); one server per site (W4: 'not inconsistent' with deploying through Azure); a local server that works with no internet is Phase 2 (A5). Our solution is subservient to the client's source of truth, currently Entra (W3). How the printers of a site reach it is open (N-5) and is the second printer test." | a |
| R2-02 | 02:16 | "the design still assumes the Datasec-hosted service" | A6 “Yes, license server through Azure or Datasec.  2 deployment optiuons” | "the licence server has two deployment options, through Azure (the Marketplace licence-server offer) or Datasec (A6); the licence address is a setting of the server, as it is of the sign-in app today (D2 s6.1 row 3)". | b |
| R2-03 | 02:23 | "packaged both as a **Linux container/appliance and as a Windows service, equally supported**" | W4; P-5 | OPEN N-6. Default: the C-17 wording stands in the documents until he rules; CI keeps both build legs; no Azure-specific package is built. | c |
| R2-04 | 02:144 | "active/passive pair behind one name on a virtual IP" | W5; W4 | N7: OPEN N-7 (high availability in the client's Azure). Default: unchanged text, marked "rests on N-7"; nothing of it is built before phase 5. | c |
| R2-05 | 02:146 | "All user data stays on the customer's server and their Microsoft tenant" | W5; W3 | "All user data stays on the customer's server, in their own Azure subscription for Phase 1 (W5), and in their Microsoft tenant". | a |
| R2-06 | 02:248 | "a cloud-only server is not viable without a site relay" | W5; W4; P-4 | Keep the measured facts of the row; the consequence becomes: "how printers at a site reach a server in the client's Azure, and the server them, is OPEN (N-5) and is the second printer test". Default: the code stays hosting-neutral; no Azure resource is created. | c |
| R2-07 | 02:274 | "A single server product, deployed on the customer's network" | W5; W4 | "A single server product, deployed in the client's Azure subscription in Phase 1 (W5), one per site (W4); the path to the printers is N-5". | a |
| R2-08 | 02:280 | "Customer site network" | W5; P-4 | Component diagram: the server box sits inside the site subgraph. Redraw once N-5 is answered; default: kept with a note under it "Phase 1 hosting: client's Azure (W5); path: N-5". | c |
| R2-09 | 02:312 | "Datasec-hosted" | A6 | Diagram: the licence box reads "Licence service (Datasec-hosted or in the client's Azure, A6)". | a |
| R2-10 | 02:375 | "customer Azure Key Vault (keys non-exportable, sign remotely) when the customer allows" | W5; P-4 | C15: OPEN N-8 (whether the Key Vault provider becomes the default when the server runs in the client's Azure). Default: provider (a) stays the only built provider (B1789's own scope leaves Key Vault out); nothing changes in the built library. | c |
| R2-11 | 02:377 | "PostgreSQL 16 on the Linux container/appliance and SQL Server" | W4; P-5 | C17: N-6 (and whether a managed database in the client's Azure is a third option). Default: unchanged. | c |
| R2-12 | 02:378 | "Datasec Azure" | A6 | C18 "Runs where": "Datasec's Azure, or the client's Azure where the licence server is deployed there (A6)". | a |
| R2-13 | 02:555 | "both platforms need LAN reachability" | W3 “clients deploy to their own tenant”; W5 | 5.7 keeps its decision (one customer tenant per installation); reasons: "the client deploys into their own tenant and subscription (W3, W5)" replaces "Kam's 'localised server' (C-1)"; "both platforms need LAN reachability" becomes "both platforms need two-way reachability (N-5)". | a |
| R2-14 | 02:559 | "switch-over by a virtual IP that moves between the nodes" | W5; W4 | 5.8: N-7; default as R2-04. | c |
| R2-15 | 02:584 | "B3: Suite Server (customer LAN)" | W5; P-4 | Trust boundaries 6.1 (and B2 "customer LAN" at 02:593): redrawn when N-5 is answered (printers may reach the server across the internet or a private link). Default: kept, marked "rests on N-5". | c |
| R2-16 | 02:766 | "The design is unchanged: the server calls the Datasec-hosted licence service." | A6; D2 s6.1 row 3 | "Two deployment options (A6): Datasec's licence service or the Marketplace licence server in the client's Azure; the server's licence address is a setting, and a licence is bound to the licence server's host name (report A5 line 338)". OP-7 answered. | b |
| R2-17 | 02:780 | "The two server packagings below stand as ruled (C-17)" | W4; P-5 | 8.1: N-6; default as R2-03. | c |
| R2-18 | 02:784 | "Two packagings, equally supported" | W4; P-5 | Packaging row: N-6; default as R2-03. | c |
| R2-19 | 02:785 | "static IP on a network that reaches every printer" | W5; P-4 | Prerequisites: N-5; default: kept, marked "rests on N-5". | c |
| R2-20 | 02:786 | "An FQDN in the customer's DNS" | W5; P-4 | DNS row: the name must still resolve from printers; how (the client's DNS, a private zone in their Azure) is N-5. Default: kept. | c |
| R2-21 | 02:790 | "Two nodes behind one name on a virtual IP" | W5 | HA row: N-7; default as R2-04. | c |
| R2-22 | 02:833 | "blue/green on the appliance" | W4; P-5 | 8.4 server updates: N-6; default: kept. | c |
| R2-23 | 02:846 | "One server (or pair) per site whose printers it can reach on the LAN" | W4 “one server per site on the customer's network is not inconsistent with them deploying through azure in their tenant” | "One server (or pair) per site (W4), deployed through the client's Azure (W5); its path to the site's printers is N-5". The OQ-11 sentence stays: no central server (C-26, restated by W4). | a |
| R2-24 | 02:899 | "(a), one server or pair per site/LAN" | W5; W4; A5; P-4 | D1: choice "in the client's Azure subscription for Phase 1 (W5), one per site (W4); on-site, no-internet server in Phase 2 (A5)"; reason column keeps the measured platform facts; the network shape is N-5; status "Ruled by the product owner 2026-11-20 22:03 (W4, W5); C-26 restated in part; P-4 open". | a |
| R2-25 | 02:921 | "Linux container/appliance with PostgreSQL and Windows service with SQL Server" | W4; P-5 | D23: status "Ruled, C-17; N-6 open". | c |
| R2-26 | 02:925 | "active/passive pair, one name on a virtual IP" | W5 | D27: N-7. | c |
| R2-27 | 02:926 | "(c), local default" | W5 | D28: N-8. | c |
| R2-28 | 02:952 | "Server is a single point of failure" | W5 | R11 mitigation "Active/passive pair": N-7. | c |
| R2-29 | 02:961 | "Two packagings of equal standing" | W4; P-5 | R20: N-6. | c |
| R2-30 | 02:967 | "HA pair unproven" | W5 | R26: N-7. | c |
| R2-31 | 02:973 | "A clause of HP's older SDK guide forbids reverse engineering" | W5; W4 | New risk after R33: "R34 Printers at a site must reach a server in the client's Azure and be reached by it: two-way traffic, no address translation on OXPd 1.x, port 7627 fixed (`02:248`; [C1 s5.2]; [C2 s5.1 item 1]). Mitigation: the second printer test; N-5." | b |
| R2-32 | 03:9 | "then deployment tooling in both packagings" | W4; P-5 | BLUF 1: N-6. | c |
| R2-33 | 03:10 | "Release 1 is everything, on both platforms, in both packagings" | W4; P-5 | BLUF 2: "in both packagings" rests on N-6. | c |
| R2-34 | 03:16 | "no Azure, no spend" | W5; C-42 | BLUF 8 adds: "Phase 1 runs in the client's Azure subscription (W5). C-42's 'no Azure, no spend' still binds: no Azure resource is created, the second printer test's included, without the product owner's word." | a |
| R2-35 | 03:63 | "HA switch-over" | W5 | S10: N-7. | c |
| R2-36 | 03:117 | "installs the server in either packaging" | W4; P-5 | Phase 5 goal, packaging half: N-6. | c |
| R2-37 | 03:119 | "the Linux container, the appliance and the Windows installer each pass" | W4; P-5 | E5.1: N-6. | c |
| R2-38 | 03:125 | "E6.4 HA switch-over under 2 minutes" | W5 | E6.4: N-7. | c |
| R2-39 | 03:206 | "Packaging, both equally (C-17)" | W4; W5; A7 “Azure marketplace” | WP5.1: N-6; and whether an Azure deployment of the server (a template or Marketplace offer into the client's subscription) appears as new work. Default: not started. | c |
| R2-40 | 03:212 | "virtual-IP switch-over on Linux (keepalived)" | W5 | WP5.7: N-7. | c |
| R2-41 | 03:238 | "Both packagings equal (C-17): a release is not green until both are" | W4; P-5 | Test strategy packaging row: N-6. | c |
| R2-42 | 03:287 | "Two packagings (C-17)" | W4; P-5 | Team table: N-6. | c |
| R2-43 | 03:310 | "On each site's network" | W4; W5 | Q5 row, Answer: add "; Phase 1 hosted in the client's Azure subscription (W5, W4); one server per site restated (W4)". | a |
| R2-44 | 03:319 | "Both equally" | W4; P-5 | Q14 row: add "N-6 open (W4)". | c |
| R2-45 | 03:348 | "assumed the licence service stays Datasec-hosted" | A6; A5 | "Two deployment options, Datasec or the client's Azure (A6); the licence address is a server setting. A site with no internet is Phase 2 (A5)". | a |
| R2-46 | 03:382 | "No: one server per site (C-26)" | W4 | OQ-11: "No: one server per site (C-26; restated 2026-11-20 22:03:25, W4)"; mark answered. | a |
| R2-47 | 03:384 | "Must a site with no internet be supported" | A5 “Phase 2 we will have a local server that allows for no internet.  For now, internet is essential.” | OQ-13: ANSWERED: not in Phase 1; a local no-internet server is Phase 2 (A5). | a |
| R2-48 | 03:400 | "Who is meant to deploy the licence-server Marketplace offer" | A6 | OP-7: ANSWERED: two deployment options, through Azure or Datasec (A6). | a |
| R2-49 | 03:401 | "How many customers deployed the Azure side by the script" | A7 “Azure marketplace” | OP-8: his answer names the route, not the counts the question asked. OPEN N-17; default unchanged (every gateway change ships as an offer version and a script update). | c |
| R2-50 | 03:402 | "the gateway package live in the Marketplace today" | A8 “yes” (N:21; v2 A8 asks whether v1.3.0 is live) | OP-9: ANSWERED: yes. | a |
| R2-51 | 05:7 | "no Azure, no spend" | W5; C-42 | As R2-34, in the readiness BLUF. | a |
| R2-52 | 05:130 | "The option you did not choose was one per company account" | W4 | Q11: answered, one server per site (restated by W4). | a |
| R2-53 | 05:141 | "Must a site with no internet at all be supported?" | A5 | Q13: answered as R2-47. | a |
| R2-54 | 05:169 | "Who is meant to deploy the licence-server Azure offer" | A6 | OP-7: answered as R2-48. | a |
| R2-55 | 05:170 | "How many customers deployed the Azure side by the script" | A7 | OP-8: as R2-49 (N-17). | c |
| R2-56 | 05:171 | "the gateway package live in the Marketplace today" | A8 | OP-9: answered as R2-50. | a |
| R2-57 | 05:204 | "Two Linux and two Windows server hosts" | W5; P-5 | Kit item 16: N-18 (whether lab hosts or Azure hosts in a subscription he names). Default: unchanged; nothing in Azure without his word. | c |
| R2-58 | 05:185 | "## PHASE 0 NEEDS" | W1; W5; C-51 | Head the list with the two printer tests of part 3 (test 1 class a; test 2 waits for an Azure resource, N-5). | a |

### 1D. The deployment tool (W2; notes A15 to A17)

| Id | Where | As it stands | By | Proposed | Class |
|---|---|---|---|---|---|
| R3-01 | 02:42 | "So the utility itself is KEPT as the operator's deployment tool" | W2 “of the two tools, check that they do the same thing.  I do not think so, but whichever is newer.” | P9: "Changed by W2 (verbatim beside it): the two Datasec tools do the same job by different means and not the same steps (D2 s3.1 to s3.3); the newer by file dates is HP AuthSuite Manager 1.1.0 (338 of 344 files dated 2026-11-11, against 138 of 139 dated 2026-10-09), which becomes the deployment tool; the Utility is kept as reference. Version numbers point the other way (3.0.0 against 1.1.0, separate series), and A15 asks for a separate app: N-9." | b |
| R3-02 | 02:43 | "code NOT USED directly" | W2 | P10: "KEPT as the deployment tool, amended for OXPd (W2; D2 s3.2, s3.3); its TLS-off, TLS 1.0 and Basic-auth patterns are fixed, not carried (D2 s3.2 last paragraph)". | b |
| R3-03 | 02:124 | "with the OXPd amendment it can hand those files to the server's importer" | W2 | F60: "the deployment tool holds each app's configuration form and settings (the Manager's Applications Library: a .wdpkg with the .hpk and the app's .moc, D2 s3.2 step 1) and can hand them to the importer"; whether the Manager reads existing .cfg files is UNMEASURED. | b |
| R3-04 | 02:262 | "the operator's tool for it is Datasec's HPK Deployment Utility, amended" | W2 | "the operator's tool for it is Datasec's HP AuthSuite Manager, amended (W2; D2 s3)". | b |
| R3-05 | 02:274 | "from Datasec's existing HPK Deployment Utility, amended for OXPd" | W2 | "from Datasec's HP AuthSuite Manager, amended for OXPd (W2)". | b |
| R3-06 | 02:364 | "Batch onboarding, removal and their result lists are started and shown from the HPK Deployment Utility" | W2 | C4: "... from the deployment tool (the AuthSuite Manager, W2)". The engine keeps drift repair: the Manager has scheduled runs but no 15-minute drift check (D2 s3.3 row 12). | b |
| R3-07 | 02:376 | "batch onboarding is not a console page but a job in the HPK Deployment Utility" | W2 | C16: "a job in the deployment tool (W2)"; OP-4 unchanged. | b |
| R3-08 | 02:702 | "the utility that has this weakness is now the deployment tool" | W2; A16 “any improvement that is worth while is a good idea and will be done” | W22: "The Utility is no longer the deployment tool (W2). The Manager keeps one password per device under Windows data protection and sends it as HTTP Basic, with certificate checks off and TLS 1.0 allowed (D2 s3.2): those are the weaknesses to fix. OP-6 is answered by A16." | b |
| R3-09 | 02:780 | "installing the server itself is not something the HPK Deployment Utility can carry" | W2 | "Neither Datasec tool installs the server (D2 s3.3: rows 1 and 2 unchanged)". | b |
| R3-10 | 02:794 | "the operator starts them as a job in the HPK Deployment Utility, amended" | W2 | 8.2 lead: "... a job in the AuthSuite Manager, amended". | b |
| R3-11 | 02:816 | "the job is started and followed from the HPK Deployment Utility, amended" | W2 | 8.3 lead: as R3-10. | b |
| R3-12 | 02:842 | "The HPK Deployment Utility does that today, unchanged" | W2; D2 s6.2 row 8 | "The AuthSuite Manager does that today ('Uninstall Applications', D2 s3.2 step 4); Datasec's own advice for a change of sign-in solution is a format, and a printer claimed in Command Centre has a cloud record to remove (D2 s6.2 row 8)". | b |
| R3-13 | 02:850 | "Deployment for OXPd therefore uses Datasec's existing HPK Deployment Utility" | W2 | 8.7 ruling paragraph: add W2 after C-43 and the measured comparison; retitle the section "The deployment tool (C-43, W2)". | b |
| R3-14 | 02:887 | "The utility is the operator's deployment tool for the whole mixed fleet" | W2 | 8.7: the step table gains an AuthSuite Manager column: rows 6, 7, 10, 11, 12 read differently (D2 s3.3); rows 1, 2, 13, 15 unchanged; U1 to U10 kept as the record of the Utility. | b |
| R3-15 | 02:889 | "Whether HPKTool can do anything to an OXPd printer" | W2; D2 s6.2 row 4 | "HP's HPKTool guide describes no use on an OXPd printer (D2 s3.4: 'oxpd' 1 hit, about an application's launch data)". | b |
| R3-16 | 02:924 | "no new installer is built; the utility starts and follows the jobs" | W2 | D26: "(c) Datasec's deployment tool, the newer one (W2): the AuthSuite Manager, amended; the engine executes and repairs"; status "CHANGED by W2; N-9 open". | b |
| R3-17 | 02:972 | "The deployment tool is an existing Windows desktop utility" | W2 | R31: "The deployment tool is the AuthSuite Manager: a WinUI 3 app with a Windows service and scheduled runs (D2 s3.1); its import accepts only six fixed Workpath ids, so OXPd needs a package kind for solution.bdl (D2 s3.3)". | b |
| R3-18 | 03:17 | "Deployment uses Datasec's existing HPK Deployment Utility, amended" | W2 | BLUF 9: "Deployment uses Datasec's newer tool, HP AuthSuite Manager, amended (W2); N-9". | b |
| R3-19 | 03:23 | "the utility itself is the deployment tool, amended for OXPd" | W2 | "the AuthSuite Manager is the deployment tool (W2)". | b |
| R3-20 | 03:117 | "onboards the devices from Datasec's HPK Deployment Utility, amended for OXPd" | W2 | Phase 5 goal: "... from the AuthSuite Manager, amended". | b |
| R3-21 | 03:119 | "the job is started from the amended HPK Deployment Utility" | W2 | E5.2: "... from the amended AuthSuite Manager; the report is its per-run result (D2 s3.2 step 6)". | b |
| R3-22 | 03:139 | "where the amended utility lives is open (OP-5" | A15 “separate app but with the intention of integration after MVP” | WP0.3: "the OXPd deployment part is a separate app, integrated with the deployment tool after the MVP (A15, answering A15-1)"; it is not copied into `datasecau/OXPd_2` unless a brief says so. Which tool it later integrates into: N-9. | a |
| R3-23 | 03:146 | "HPK Deployment Utility: amendment design (added by B1765, C-43)" | W2; A15 | WP0.10 moves: the design note is written against the AuthSuite Manager and as a separate app (A15); the build check of the Utility is struck; a build check of the Manager replaces it. | b |
| R3-24 | 03:162 | "this admin API is the contract the HPK Deployment Utility is later built against" | W2 | WP1.11: "... the contract the deployment tool (or the separate app of A15) is built against". | b |
| R3-25 | 03:169 | "the operator's front end for batches is the amended HPK Deployment Utility" | W2 | WP2.2: as R3-24. | b |
| R3-26 | 03:207 | "the operator's tool is the amended utility (WP5.8)" | W2 | WP5.2: "the operator's tool is the deployment tool (WP5.8, W2)". | b |
| R3-27 | 03:208 | "whether the console keeps its own onboarding pages as well is OP-4" | W2 | WP5.3: wording follows R3-07. | b |
| R3-28 | 03:211 | "the amended utility can hand the" | W2 | WP5.6: as R3-03. | b |
| R3-29 | 03:213 | "HPK Deployment Utility amended for OXPd (added by B1765, C-43)" | W2; A15; A16 | WP5.8 moves: "OXPd deployment for the AuthSuite Manager, as a separate app integrated after the MVP (A15)"; scope from D2 s3.3 (a package kind for solution.bdl, OXPd job kinds, per-step results; discovery, per-device passwords and structured results exist already); the credential path fixed (A16). Size: not re-estimated. | b |
| R3-30 | 03:260 | "is fronted by the HPK Deployment Utility, amended" | W2 | Note (2): "... by the deployment tool (W2)". | b |
| R3-31 | 03:394 | "Is the amended HPK Deployment Utility the operator's tool" | W2 | OP-1: same point, of the AuthSuite Manager or the separate app; default unchanged (the server executes). | b |
| R3-32 | 03:395 | "also cover installing the server itself" | W2 | OP-2: same point; default unchanged; under N-6 the server may be deployed into Azure instead. | b |
| R3-33 | 03:396 | "The utility runs on Windows only" | A17 “yes for now” | OP-3: ANSWERED: a Windows PC for the tool is available at Workpath sites "for now" (A17). | a |
| R3-34 | 03:397 | "Does the server console also keep its own onboarding pages" | W2 | OP-4: of the deployment tool; default unchanged. | b |
| R3-35 | 03:398 | "Where does the amended utility live" | A15 | OP-5: ANSWERED: "separate app but with the intention of integration after MVP" (A15). | a |
| R3-36 | 03:399 | "May the amendment also change how the utility stores" | A16 | OP-6: ANSWERED: yes, worthwhile improvements are done (A16). | a |
| R3-37 | 05:16 | "Deployment uses Datasec's existing HPK Deployment Utility, amended" | W2 | BLUF 4: "Deployment uses Datasec's newer tool, the AuthSuite Manager (W2); the OXPd part is a separate app until after the MVP (A15); N-9". | b |
| R3-38 | 05:163 | "Is the amended HPK Deployment Utility the operator's tool" | W2 | OP-1: as R3-31. | b |
| R3-39 | 05:164 | "also cover installing the server itself" | W2 | OP-2: as R3-32. | b |
| R3-40 | 05:165 | "The utility runs on Windows only" | A17 | OP-3: answered as R3-33. | a |
| R3-41 | 05:166 | "Does the server's console also keep its own onboarding pages" | W2 | OP-4: as R3-34. | b |
| R3-42 | 05:167 | "Where does the amended utility live, and how is it released" | A15 | OP-5: answered as R3-35. | a |
| R3-43 | 05:168 | "May the amendment also change how the utility stores" | A16 | OP-6: answered as R3-36. | a |
| R3-44 | 05:222 | "so the deployment utility can be built against it" | W2 | WP0.3 row: "so the deployment tool (or the separate app) can be built against it". | b |
| R3-45 | 05:236 | "The design note for amending the HPK Deployment Utility" | W2; A15 | WP0.10 row: as R3-23. | b |
| R3-46 | 05:253 | "The HPK Deployment Utility was read in part and not built or run" | W2 | Add: "The AuthSuite Manager (344 files) was read by report D2 from its test catalogue and selected files; not built or run." | b |

### 1E. His other answers of 21:04, and the reports' corrections that touch a design line

| Id | Where | As it stands | By | Proposed | Class |
|---|---|---|---|---|---|
| R4-01 | 02:102 | "Six UI languages at parity" | A18 “assume English for phase 1 but add to jira questions” | F42: "Phase 1: English (A18). The string sets in the sources are kept for later; OP-21 stays on the master list as he asked." The manuals say English only (D1 s7 row 20). | b |
| R4-02 | 03:188 | "Default: the OneDrive and SharePoint pages carry eight" | A18 | WP3.12: default "English for Phase 1 (A18)"; size smaller, letter not re-estimated. | a |
| R4-03 | 03:414 | "Build all eight languages as the string files have them" | A18 | OP-21 default: "English for Phase 1 (A18); the question stays on the master list". | a |
| R4-04 | 05:183 | "Build all eight languages as the code has them" | A18 | OP-21: as R4-03. | a |
| R4-05 | 05:231 | "eight for the OneDrive and SharePoint pages" | A18 | WP3.12 row: as R4-02. | a |
| R4-06 | 03:383 | "Build on 1.8.4.1" | A22 “beta attached” + B4 s6 | OQ-12: "His answer 'beta attached' pointed at the OXPd 2 SDK Beta 10 folder, not an OXPd 1.x SDK (B4 s6: 0 of its files name OXPd 1.x); OQ-12 stays open as worded; default unchanged". | b |
| R4-07 | 05:135 | "Has HP given Datasec anything newer than OXPd 1.8.4.1?" | A22 + B4 s6 | Q12: as R4-06. | b |
| R4-08 | 03:385 | "None set; needed before the pilot" | A24 “as close to commercial ready as possible.” | OQ-14: his words record the aim and set no threshold (A24 asked the Workpath team's own pilot practice). OPEN N-13; default unchanged. | c |
| R4-09 | 05:147 | "What defect level ends the four-week pilot successfully?" | A24 | Q14: as R4-08 (N-13). | c |
| R4-10 | 03:403 | "Can the phone app's source (HP Secure Authentication) be supplied" | A9 “Attached should be the one for HPAM” + A12 s1, s8 item 3 | OP-10: ANSWERED: the source is in hand (HP Secure Authentication, standard edition 1.5.17, A12); the capture becomes a confirmation of a known message shape. | b |
| R4-11 | 05:172 | "Can the source of the phone app (HP Secure Authentication) be supplied" | A9 + A12 | OP-10: as R4-10. | b |
| R4-12 | 03:404 | "the API of the older Keycloak back end, and so out of scope under C-18" | A12 s8 item 2 (cc-api arrived with the 21:04 message) | OP-11: ANSWERED from source: yes, and not needed under C-18. | b |
| R4-13 | 05:173 | "which was not among the repositories" | A12 | OP-11: as R4-12. | b |
| R4-14 | 02:46 | "was not sent (C-40) and, by A9's inference" | A12 s8 item 1 | P13: "`cc-api` was received on 2026-11-20 with the product owner's 21:04 message and read (report A12): it is this back end's API". | b |
| R4-15 | 02:420 | "the phone app signs in itself and publishes" | A12 s8 item 4 | M3: seven fields (`id`, `realm`, `secret`, `email`, `userName`, `firstName`, `lastName`); `email` carries the sign-in name (`upn`). | b |
| R4-16 | 02:612 | "whether the library literal is that live key is an open question (OQ-8)" | A12 s8 item 6 | Add: the phone app's source holds the same literal (compared without printing it) and its release workflow injects no key; OQ-8 narrows to "is a store build made from this source unchanged?". | b |
| R4-17 | 05:103 | "every stored card and every installed phone app depends on it" | A12 s8 item 6 | Q8: as R4-16. | b |
| R4-18 | 02:367 | "15-card / 50-value limits" | A12 s8 item 7 | C7: "each phone a user signs in on is a separate card id, so the per-user limit is consumed per phone". | b |
| R4-19 | 03:143 | "capture the phone app's message body" | A12 s8 item 5 | WP0.7: strike the capture as an open input; of the two tenant tests, "is the per-user secret stable" is answered from source (stable per user and phone) and needs a confirming run only. | b |
| R4-20 | 03:177 | "what WP0.7 still owes this package is the phone app's message body" | A12 s8 item 5 | WP3.1: "the message body is known from source (A12); a confirming capture only". | b |
| R4-21 | 05:200 | "The source code of the customer gateway (the Function App)" | A12 s8 item 3 | Kit item 12: "Still wanted: the phone app's source" becomes "received with the 21:04 message (A12)". | b |
| R4-22 | 05:242 | "The phone app stays on this list" | A12 s8 item 3 | Strike: the phone app's source (standard edition) is in hand; the Intune edition is not (A12 s7.2 X6). | b |
| R4-23 | 05:252 | "The message the phone app sends is not in what you sent" | A12 s8 item 9 | Superseded by report A12 (the message is read from source). | b |
| R4-24 | 03:406 | "Is there more of the earlier OXPd 1 work than what was sent" | A11 “not much more than what has been provided” | OP-13: record his answer; the default ("what was sent is the last state") stands; not marked answered in full. | a |
| R4-25 | 05:175 | "Is there more of the earlier OXPd 1 work than what you sent" | A11 | OP-13: as R4-24. | a |
| R4-26 | 03:408 | "Was that code ever run against a physical printer" | A12 “I do not believe so but I will check” | OP-15: record his answer; default unchanged ("emulator only") pending his check. | a |
| R4-27 | 05:177 | "Was that code ever run against a physical printer" | A12 (his answer) | OP-15: as R4-26. | a |
| R4-28 | 02:80 | "Pull-print check at sign-in" | P3 “mirror how the current solutions work” + D1 s7 row 21 | F17 (and F53 at 02:112, the sequence at 02:454): "a Pull release precedes, and does not need, the Microsoft step, as today ('Pull-Print no MFA', D1 s7 row 21; report A1 line 132)". | b |
| R4-29 | 02:112 | "sign-in releases the user's jobs" | P3 + D1 s7 row 21 | F53: as R4-28. | b |
| R4-30 | 02:454 | "else Known card, No-MFA mode" | P3 + D1 s7 row 21 | Sequence 5.5.1: the pull-print check also runs before the Microsoft step in the MFA branch (as R4-28). | b |
| R4-31 | 02:97 | "OneDrive: four places (My Drive, Recent, Shared with me, Shared libraries)" | A2 “mirror existing operation of the apps”; D1 s7 row 3 | OPEN N-10: the V4.4 release notes say Shared with me was removed (D1 s7 row 3); the source has it live. Default: F37 keeps four places, marked "Shared with me rests on source alone; question to the Workpath team". | c |
| R4-32 | 02:211 | "The four places, as a consequence of C-16" | A2; D1 s7 row 3 | 3.9: N-10; default as R4-31. | c |
| R4-33 | 02:225 | "Shared with me by the Microsoft Search API" | A2; D1 s7 row 3 | F99: N-10; default as R4-31. | c |
| R4-34 | 02:535 | "OneDrive: four places (My Drive, Recent, Shared with me, Shared libraries); browse" | A2; D1 s7 row 3 | 5.6.3: N-10; default as R4-31. | c |
| R4-35 | 02:75 | "Passkey / device-code sign-in (no card)" | P3; D1 s7 row 2 | OPEN N-11: no document shows the Passkey button (D1 s7 row 2); with M1 no longer the baseline (R1-11) the button's method is also open. Default: F12 kept, not built before N-3 and N-11. | c |
| R4-36 | 02:118 | "default 10 s" | P3 + D1 s7 row 22 | F59: "the documents give a range of 10 to 30 seconds and example values 10 and 15 (D1 s7 row 22); 10 is the source's figure". | b |
| R4-37 | 02:84 | "Error vocabulary AI01-AI09 kept on the panel" | P3 + D1 s7 row 12 | F21: "the help article's texts for AI01, AI02, AI04 and AI05 are the legacy back end's; the current meanings come from report A1 lines 383-391". | b |
| R4-38 | 02:110 | "Registration by a Printer Administrator" | A4 “Mirror current deployment and look at deployment / support docs”; D1 s7 row 23; D2 s6.2 row 7 | OPEN N-12: today a fleet is also registered unattended from a stored account (D2 s6.2 row 7); whether OXPd offers that route (the server would hold that account's password). Default: interactive only, as designed. | c |
| R4-39 | 03:377 | "Approve the design choices that differ from Workpath" | P3 + D1 s9 item 12 | OQ-6: give the register's two rows their document and page (card emulation `NEW:65-91`; app settings `MFUG p.31-34`). | b |
| R4-40 | 02:725 | "not ruled: open question OQ-9" | A4 “Everything is deployed in the clients tennant”; P-7 | OPEN N-14: A4 answered the question whether Datasec owns the print registration; whether "everything" means each customer registers their own is not said. Default unchanged: nothing built on Datasec's registration before the answer. | c |
| R4-41 | 03:380 | "May the server register printers under Datasec's own Universal Print app registration?" | A4; P-7 | OQ-9: as R4-40 (N-14). | c |
| R4-42 | 05:108 | "May the server register printers under Datasec's own Universal Print app registration?" | A4; P-7 | Q9: as R4-40 (N-14). | c |
| R4-43 | 03:381 | "is QR sign-in in No-MFA mode offered on OXPd?" | P3 “The current product has MFA by default but different logon options depending on setup and right.” | OPEN N-15: his P3 words are recorded; they sit under the QR question and do not name QR (B1816 drafter fault 6), so they do not settle it. A12 settles one of the two untested links from source (the secret is stable per user and phone). Default unchanged: (a), as Workpath. | c |
| R4-44 | 05:119 | "Default until you rule: (a), as Workpath" | P3; A12 s1 item 5 | Q10: as R4-43 (N-15). | c |
| R4-45 | 05:192 | "One newer printer: FutureSmart 6" | A23 “anything we need”; N:10 | Kit items 4, 7, 8 (and 9, 10): "the Workpath product owner holds a lab with every device and reader needed; the HP Experience Centre is another option; the product owner has a printer at home (N:10, A23)". Names are left out of the document. | a |
| R4-46 | 05:209 | "Its firmware version is not known" | P2 “firmware version is irrelevant as we will need to wipe the device as testing requires developer mode on so we can deploy any firmware.”; C-47 | Printers: "the firmware version does not matter: the printer will be wiped and put in developer mode so any firmware can be deployed (P2, C-47)". Which OXPd generation an M577 belongs to is still not established (C-39). | a |
| R4-47 | 05:190 | "A Windows x86-64 PC on a wired network" | N:13 “Windows machine ready.”; C-49, C-52, C-53 | Kit item 2: "ready (N:13); his old PC (C-49, C-52); Virtual Machine Platform on and the VMware evaluation ended are still to settle (C-53)". | a |
| R4-48 | 05:193 | "An HP developer account with an" | N:8 “We will use my access during the dev process”; C-50 | Kit item 5: "the product owner's HP access is used during development (N:8, C-50)". | a |
| R4-49 | 05:202 | "From HP, in writing" | N:9 “Communication to the HP team is done through their portal for general questions” | Kit item 14: "HP is reached through its portal, with escalation by the product owner (N:9)". Nothing is sent by an agent. | a |
| R4-50 | 05:199 | "A test Microsoft tenant with" | A23 | Kit item 11: the team supplies what is needed (A23, answering A23-5). | a |
| R4-51 | 03:141 | "file HP's written confirmation (C-30); App Center/VNV enrolment" | N:8; N:9 | WP0.5: the product owner's access and HP's portal are the route (N:8, N:9); App Center enrolment (A21-2) is not answered by them. | a |
| R4-52 | 02:957 | "Licence rights over HP sources and redistribution of OXPd2Lib (beta)" | N:12 “We have the commercial agreement.” | OPEN N-16: the v2 questions document maps this paragraph to A21-6 and H6 point 2 (an agent's mapping); his words do not say they cover HP's library terms (R16) or the reverse-engineering clause (R32). Default unchanged for R16 and R32. | c |
| R4-53 | 03:374 | "Mailflow quick messages (F87) are dead" | A19 “I do not know and will ask workpath team.” | OQ-3 row: record that A19 goes to the Workpath team as a follow-up on the master list (his words); default unchanged. | a |
| R4-54 | 03:142 | "SharePoint 4.4.6, the manual's '4 custom fields'" | A20 “Ask as a follow up question for workpath team, add to jira questions” | WP0.6: items (a) and (c) go to the Workpath team as follow-ups on the master list (A20); defaults unchanged. | a |

---

## Open questions the class (c) rows write (each with the default the build takes meanwhile; for stage 2 to place in each document's open-questions section)

| N | Question for the product owner | Default meanwhile | Rows |
|---|---|---|---|
| N-1 | Does the on-panel Microsoft step apply to OXPd 1.x printers as well as OXPd 2 (P-1)? | Same target on both; built on the OXPd 2 page first; nothing of the phone route built for 1.x before the 1.x panel test reports | R1-03, R1-16, R1-19 |
| N-2 | Microsoft's page inside a frame (his word "iframe") or as a full page in the panel browser? | Page written for either; test 1 tries the frame first | R1-10 |
| N-3 | If the first printer test fails (cookies shared between users, page does not render, a pop-up needed): what then? Nobody decides it here | Result to him with options; M1, M2 and the relay stay unbuilt | R1-07, R1-11, R1-12, R1-17, R1-24, R1-27, R1-31, R1-35, R1-37, R1-41 |
| N-4 | Does "we cannot interfere with ... the token management done by microsoft" bear on the server holding, refreshing and redeeming users' tokens, on `login_hint`, and on No-MFA's stored token (P-3)? | Unchanged; Microsoft's library and tokens; nothing new designed | R1-43 to R1-49, R1-17 |
| N-5 | How do printers at a site reach a server in the client's Azure, and the server them (P-4, P-8)? | Code hosting-neutral; no Azure resource; the second test written and not run | R2-06, R2-08, R2-15, R2-19, R2-20 |
| N-6 | Which packagings ship in release 1 when Phase 1 is Azure-hosted; is an Azure deployment (template or Marketplace offer) one (P-5)? | C-17 wording stands; both CI legs; nothing Azure-specific built | R2-03, R2-11, R2-17, R2-18, R2-22, R2-25, R2-29, R2-32, R2-33, R2-36, R2-37, R2-39, R2-41, R2-42, R2-44 |
| N-7 | High availability in the client's Azure: the virtual-IP pair or Azure's own means? | Unchanged; phase-5 work, not started | R2-04, R2-14, R2-21, R2-26, R2-28, R2-30, R2-35, R2-38, R2-40 |
| N-8 | Does the Key Vault provider become the default when the server runs in the client's Azure? | Local provider (a) stays the only built one | R2-10, R2-27 |
| N-9 | Which tool, and in what form: the newer by date (AuthSuite Manager) per W2, the Utility per C-43, and A15's separate app (P-6)? | Design note against the Manager, OXPd part as a separate app; nothing pushed to either tool's repository | R3-01, R3-16, R3-18, R3-22, R3-37 |
| N-10 | Is "Shared with me" in the shipped OneDrive 4.4 (release notes say removed)? For the Workpath team | Kept, marked as resting on source | R4-31 to R4-34 |
| N-11 | Do customers see the Passkey button on V4.4, and by what method does it sign in now? | F12 kept, not built before N-3 and N-11 | R4-35 |
| N-12 | Does OXPd offer today's unattended Universal Print registration from a stored account? | Interactive only | R4-38 |
| N-13 | The pilot threshold (A24 gives an aim, no number) | None set; before the pilot | R4-08, R4-09 |
| N-14 | Does A4's "everything ... in their tenant" mean each customer registers their own print app (P-7)? | Nothing built on Datasec's registration | R4-40 to R4-42 |
| N-15 | QR sign-in without MFA on OXPd (OQ-10): P3's words do not settle it | (a), as Workpath | R4-43, R4-44 |
| N-16 | Does "We have the commercial agreement ..." cover HP's library terms (R16) or the reverse-engineering clause (R32)? | Unchanged | R4-52 |
| N-17 | OP-8: how many customers deployed by Marketplace and how many by script (A7 names the route) | Every gateway change ships both ways | R2-49, R2-55 |
| N-18 | Kit item 16 under Azure hosting: lab hosts, or hosts in a subscription he names? | Unchanged; nothing in Azure without his word | R2-57 |

---

## 2. The decisions table of 02 (lines 899 to 932), each marked

| D | Decision | Mark | How, and by what |
|---|---|---|---|
| D1 | Where the solution runs | **CHANGED; shape OPEN** | In the client's Azure subscription for Phase 1, one per site (W4, W5); on-site no-internet server Phase 2 (A5); network path N-5; P-4 |
| D2 | One core, two adapters | unchanged | |
| D3 | C#/.NET 10 | unchanged | |
| D4 | Reuse the HPAM registration | unchanged | W3 and A4 agree (the client's own registration) |
| D5 | CSA contract and key | unchanged | A12 adds evidence to OQ-8 (R4-16) |
| D6 | User token custody | **NOW OPEN** (text unchanged) | N-4, P-3 |
| D7 | Identity on the device session | unchanged | |
| D8 | Session end | unchanged | |
| D9 | Card decoding | unchanged | |
| D10 | Interactive Microsoft sign-in | **CHANGED** | On-panel, as Entra sets it (W1); 1.x N-1; failure N-3 |
| D11 | QR gateway | **CHANGED in part** | Subscriber unchanged; the M2 relay loses its baseline purpose and hangs on N-3 (OP-12) |
| D12 | Server-rendered panel UI | unchanged | The panel template must now carry Microsoft's page (R1-34) |
| D13 | Print delivery | unchanged | |
| D14 | Pull-print dialog | unchanged | Pull release needs no Microsoft step (R4-28, class b) |
| D15 to D20, D22 | | unchanged | |
| D21 | Single tenant per installation | unchanged | Reason changes (R2-13) |
| D23 | Packaging | **NOW OPEN** | N-6, P-5 |
| D24 | Fleet admin view | unchanged | |
| D25 | Licence validation | unchanged | Licence address becomes a setting (A6; R2-16) |
| D26 | Fleet deployment tool | **CHANGED** | The newer tool, AuthSuite Manager (W2, D2 s3); N-9 open |
| D27 | HA | **NOW OPEN** | N-7 |
| D28 | Secret store | **NOW OPEN** (priority only) | N-8 |
| D29 to D34 | | unchanged | D32's OXPd 1.x scope meets N-1 |

---

## 3. What the rulings do to work in flight and to the plan

**Work packages that move:** WP0.2 (S4 becomes the first printer test; a new spike for the second test; S7 re-aimed at the panel sign-in and the D3 policy; S10 hangs on N-7); WP0.7 and WP3.1 (the phone message is known from source: A12); WP0.10 and WP5.8 (re-aimed at the AuthSuite Manager and A15's separate app); WP1.4, WP1.6, WP3.3 (enrolment and prompt pages carry Microsoft's page on the panel); WP1.11, WP2.2, WP5.2, WP5.3, WP5.6 (their deployment-tool wording); WP3.12 (English for Phase 1: smaller); WP5.1 and WP5.7 (hang on N-6, N-7); WP5.4 (licence address as a setting; the customer-deployed licence server is a supported option, A6).
**Appear (proposed, not decided):** a spike S14 for the second printer test (needs an Azure resource: his word first); an Azure deployment of the server into the client's subscription (only if N-6 makes it one).
**Fall away as planned work, pending N-3:** WP3.2 (M2 phone redirect with the gateway relay) and the device-code baseline of WP1.4.

**The four wave-1 libraries (tested against the briefs in Tuesday's tree, not against the code repository, which was not opened):** card decoders B1786 (WP1.3), logging deny-list B1787 and B1798 (WP1.10), the print-protocol encoder B1788 (WP4.2 part), the local secret store B1789 (WP1.1 cut). None touches the sign-in screens or hosting: the words `azure` and `sign-in` in B1786 to B1788 occur only in their word-to-build lines and scope exclusions; B1789's header reads "NO KEY VAULT, NO TPM, NO HOST WIRING, ... NO AZURE" and lists the Key Vault provider as left for later. **Tuesday's reading holds**, with one qualification: N-8 could raise the Key Vault provider's priority, which is work B1789 did not do, not a change to what it built. The in-flight round-2 briefs B1810 (WP1.3) and B1811 (WP1.1) were not opened.

**Phase-0 list, with the two printer tests at its head:**
1. **Test 1 (Monday 2026-11-23, C-51), on the printer:** the Microsoft step on the panel as Entra sets it (W1): initiate, the number shown on the panel, entered in Authenticator; two users in sequence never share a Microsoft session; no pop-up; frame or full page recorded (N-2). Needs: the printer wiped into developer mode (P2, C-47), the product owner's HP access for the service key (N:8, C-50), a test tenant user with Authenticator. Caveat: the Chromium 87 case needs a FutureSmart 6 printer; which OXPd generation the M577 runs is not established (C-39); if it is OXPd 1.x the test exercises the WebKit panel (N-1) and the Chromium test waits for a FutureSmart 6 printer from the lab (A23).
2. **Test 2, waiting for his word:** a printer at a site reaches a server in the client's Azure, and the server reaches it (443 and 7627 to the printer, the server's HTTPS port from the printer; OXPd 1.x first, because it forbids address translation). Needs an Azure resource in a subscription he names (N-5, P-8). Written, not run.
3. Then the existing list (`05:189-205`), changed by rows R4-45 to R4-50 and R2-57: Windows PC ready (N:13; C-53 items to settle); printers and readers from the Workpath lab (A23, N:10); HP access (N:8, C-50); test tenant (A23); phone app source in hand (A12); HP route (N:9); kit item 16 under N-18.

---

## 5. What could not be established

- Which Phase-1 network shape his words mean (P-4); how printers reach Azure; whether OXPd 1.x is under W1 (P-1); whether framing works (no report mentions it; UNMEASURED); whether server token custody is "interfering" (P-3).
- "Newer" by date or by version (P-6); whether the AuthSuite Manager builds or runs (not built; D2 read it from files); whether it reads existing `.cfg` files.
- His "Phase 1" and the design's "phase 1" are different things (the design's is a thin OXPd 2 slice, `03:74`); whether his Phase 1 is release 1 (C-16, C-48) is not said. Stage 2 should not let the two names merge.
- What the notes' paragraph "We have the commercial agreement ..." answers (N-16); A7's meaning (route or count, N-17); A2's "it is their token" does not confirm D6 (B1816 drafter fault 2; no row written).
- Answers checked and found to change no design line: P4 (N:15) agrees with C-16 and C-48; A2 (N:16) changes nothing; A12 for OP-15 is recorded only.
- The code repository `datasecau/OXPd_2`, Jira, the board and mail were not read. B1810 and B1811 were not opened. Report sections read: D1 s7 and s9; D2 s3 and s6; D3 s0, s2.1 and s5; A12 s1 and s6 to s9; B4 s1, s5 and s6; the B1816 drafter's list of six faults (and its amendment). B1812's table was not used as a source.
- Nothing about HPSM-POC was opened (the board data file's card record lists other cards' names; none was read).

## 7. Controls and counts (by program)

Verifier: `TUESDAY/2_Project_Files/fleet/state/s302/d1817/opus_verify.py`, run 2026-11-21 08:25 AEDT (`date`), read-only on the design documents.

- **Rows: 207.** By class: **(a) 70, (b) 68, (c) 69.** By section: Microsoft step and token handling R1 49; hosting R2 58; deployment tool R3 46; other answers and report corrections R4 54. By document: `02` 97, `03` 69, `05` 41.
- Every row's excerpt is a substring of the line it cites: 207 of 207 (0 failures). Every curly-quoted word of his in the "By" column is a substring of the commission's lines 6 to 11, his notes file, `CLARIFICATIONS.md` or the board's card records: 0 failures. W1 to W6 at the top are byte-equal to the commission's quotations: 6 of 6. Every class (c) row names an open question: 69 of 69. Open questions defined 18, used 18, none used without a definition.
- Pull items (part 4): 9 (P-1 to P-9).

Absences, each with its positive control:

| Absent | Count | Positive control, same search | Count |
|---|---|---|---|
| `iframe`, `x-frame` or `frame-ancestors` in the 21 reports of `Analysis/` (case-insensitive) | 0 | `chromium 87` in the same files | 9 (B1 5, B2 3, C1 1) |
| `iframe` in `02`, `03`, `05` | 0 | `chromium 87` in the same files | 11 (02: 9, 03: 2, 05: 0) |
| `key vault` in the B1789 brief's scope as built work (header: "NO KEY VAULT") | header exclusion | `key vault` in that brief | 4 (all exclusions or "left") |
| The deployment tools' version and dates (re-measured on the library copy, `HPAM - Docs and Notes/Source Code/`) | | Manager `Directory.Build.props:6` VersionPrefix 1.1.0, 344 files, 338 dated 2026-11-11; Utility `Directory.Build.props:7` Version 3.0.0, 139 files, 138 dated 2026-10-09 | |

Paths: every relative path the commission names was found where expected under `1_Project_Definition/` (`Design/`, `Review/`, `Analysis/`, `Registers/`, `CLARIFICATIONS.md`). The output could not be written by a temp file and a rename: the coordinator tree's path guard refused `cp` and `mv` into this folder, so this file was written with the editor tool, verified in place, and this STATE line was added last, only after 0 failures.

STATE: COMPLETE
