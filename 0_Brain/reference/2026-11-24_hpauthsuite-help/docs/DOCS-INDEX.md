# DOCS-INDEX: help-portal documents read

Read 2026-11-24 (Tuesday seat, s321). Source copies (read-only): `/Volumes/DEV-Working/Datasec/Friday/2026-11-19_oxpd-friday-work-and-library/OXPd/HPAM/Help-Portal/Documents/`. Every page of every PDF below was read as a page image (screenshots included), 20 pages per call at most; text extracts were used only to search. Five readers split the work (the lead read the four sign-in documents and the video; four helpers read the rest to the same brief). Per-document page logs: `2_Project_Files/fleet/state/s321/docsread/notes/<file>.md`. Video stills: `2_Project_Files/fleet/state/s321/docsread/frames/`.

"Date printed" is copied from the document. Where none is printed, it says so (PDF metadata is not used as a date).

## Manuals/ (current), 18 documents, 283 pages

| File | Pages | Version / date printed | One-line summary |
|---|---|---|---|
| Datasec-HP_Authentication_Manager_UG.pdf | 12 | "Revised 10th November 2026" | End-user panel sign-in by QR, NFC card and BLE with MFA / No-MFA, and sign-out; panel screenshots. |
| Datasec-HP_Secure_Authentication_UG.pdf | 18 | "User Guide V1.5.12", "Released 7th October 2026" | Phone app: first-time QR registration (two Authenticator approvals), settings, QR and BLE badge-on, reset, app unlock. |
| Datasec-HP_Secure_Authentication_Intune_UG.pdf | 18 | "Revised 7th October 2026"; needs HPAM "V4.2.1 or Greater" | Intune-managed phone app: first use, registration screen on the panel, QR/BLE badge-on, locked settings, reset. |
| HP_Secure_Authentication_Manager_Intune_Setup_Guide.pdf | 15 | "Revised 7th October 2026"; HPAM "V4.2.1 or above" | Admin setup for the Intune phone app: extra delegated permission, iOS/Android redirect URIs, 7 Intune config keys. |
| HP Authentication Manager Azure Hosted Deployment Instruction.pdf | 29 | "Revised 10th November 2026"; text cites V4.4 | Customer Azure setup: app registration, secret, SignalR scope, the 13 Graph permissions, custom security attribute roles, Marketplace SignalR/Log Analytics, licensing by tenant ID. |
| HP Authentication Manager Azure Printer Deployment Instruction.pdf | 8 | "Revised 10th November 2026" | Installer guide: licence request by email (POC "free 20 Day license"), HP Command Centre configuration fields, 300 s timeout, panel test. |
| HP Authentication Manager Azure App Registration Secret update Guide.pdf | 8 | "Revised 17th April 2026"; for "V4 sites" | Rotate the app-registration secret in the SignalR Function App and on every printer via Command Centre. |
| Disable-Public-Client-Flows.pdf | 6 | "Revised 13th November 2026" | Disable "Allow public client flows" for stricter Conditional Access; needs a "Special Public Flow Enabled MOC file" and the "HP Authsuite Manager Installer Tool". |
| Conditional Access General Support Information.pdf | 9 | "13th April 2026"; p2 "This Article was produced by AI, and may not be 100% Accurate" | Why CA blocks printers (unmanaged, Android-like browser), four exemption methods, recommended: exclude the HP Authentication enterprise app. |
| Datasec - Reader_Configuration.pdf | 16 | "Revised 24th September 2026" | Supported readers (p16 list) and how to program rfIDEAS, Elatec, HP and Inepro readers to output hex keystroke IDs. |
| Azure_Firewall_IDS_Info.pdf | 2 | none printed | Informal note: firewall IDS/IPS signatures falsely flag Azure/Entra traffic; give vendors the endpoint lists. |
| Firmware Update Best Practices v1.pdf | 4 | footer "December 2021"; "© Copyright 2021 HP" | Generic HP FutureSmart firmware upgrade best practice (test per model, pilot, stagger). Not Datasec-specific. |
| Datasec-HP OneDrive UG.pdf | 26 | "Revised 10th November 2026"; app screen "Version: v1.14.00" (p18) | OneDrive app: scan/print/email, file management, sign-out, admin presets; limitation: no shared files (p26). |
| Datasec-HP_SharePoint-UG.pdf | 26 | "Revised 10th November 2026"; app screen "Version: 1.22.24" (p20). Footer page = PDF page + 2 | SharePoint app: sites, scan with library metadata, print, "Edit column values", sign-out, admin presets. |
| Datasec - HP Mail Flow UG.pdf | 34 | "Updated 10th November 2026"; app screen "Version: 1.10.02" (p28). Footer page = PDF page - 2 | Mailflow app: read, reply, compose with scan attachments (quick-message bubbles on p15), print, sign-out, presets. |
| Datasec- HP Teams UG.pdf | 26 | "Revised 10th November 2026"; no app version shown. Printed pages 12-16 are missing from the PDF | Teams app: scan to a channel's files with message, print from Teams files, sign-out, presets. |
| Datasec-HP Universal Print Deployment and Setup Guide.pdf | 14 | "Revised 10th November 2026"; text cites v4.4 | Register a printer as up to three Universal Print printers (_Secure/_Direct/_Pull), manually at the panel or via Command Centre. |
| Datasec-HP  Universal Print UG.pdf (two spaces) | 12 | "Updated 10th November 2026"; app screen "Universal Print Version: 2.3.12" (p10) | Universal Print app: Secure job list/preview, Direct, Pull auto-release dialog, exit vs sign-out. |

## Manuals/Archive/V4 PDF/, 3 documents, 47 pages (read whole; used only where the current guides are silent)

| File | Pages | Version / date printed | One-line summary |
|---|---|---|---|
| Customer HP Authentication Manager Deployment Instruction 1-2.pdf | 18 | none printed; cover "Set 1 of 2" | Older customer setup against Datasec-hosted API/Keycloak; same 13 Graph permissions; firmware "5.8.x > 5.9.2.3". |
| NFR BYO Azure Tenant Deployment Instructions 1-2.pdf | 18 | none printed; "Copyright © 2023 Datasec Solutions"; "set 1of 2" | Older NFR setup in a partner's own tenant; a different 8-permission set incl. Directory.Read.All. |
| NFR Free Azure Tenant Deployment Instructions.pdf | 11 | "Update April 2025"; refers to "the latest V3 release (March)" | NFR demo on Datasec's shared demo tenant; Command Centre fields Base URL, API Key, AppCenter Key, Token URL, Auth URL, Client ID. |

## Support/, 1 video

| File | Length | Date | Summary |
|---|---|---|---|
| Condition_access_policy_Fix.mp4 | 479 s (96 stills, one per 5 s) | none shown; panel clock 11:57 AM - 12:07 PM | The "Passwordless MFA" fix: a CA policy requiring app protection for Android/iOS breaks OneDrive ("Folder does not exist.") and Mailflow (MF03); adding grant "Require authentication strength: Passwordless MFA" (one of the selected controls) makes all apps work. Narration audio exists and was not transcribed (no speech-to-text tool). |

## Not read (outside the brief)

`Technical Resources/` (Cold Reset PDF, Elatec tutorial video, DevPack zip), `Portal-Attachments/` (EULA, Privacy Statement, Security Whitepaper, Diagnostic Tool zip), `Utilities/` (zips).

## Counts by program

- Documents read: 21 PDFs (18 current + 3 archive) + 1 video = 22.
- Pages read: 330 PDF pages (283 current + 47 archive); video 96 stills.
- By product: HP Authentication Manager / deployment and Azure 8 (AM UG, Hosted, Printer, Secret update, Public client flows, CA guide, Firewall note, Firmware paper) + 3 archive; HP Secure Authentication (phone app) 3 (UG, Intune UG, Intune setup); readers 1; OneDrive 1; SharePoint 1; Mailflow 1; Teams 1; Universal Print 2; support video 1.
- Secrets: several pages show a partial client secret, tenant/client IDs, an Android signature hash, a demo API key and an AppCenter key (Hosted p11, p13-16, p22, p25, p27; Secret update p3-p4, p5-p6 subscription ID; Intune setup p8; archive Customer and NFR guides, NFR Free p6-p7; archive PDF form password). Recorded as existing only; no value was copied anywhere.
