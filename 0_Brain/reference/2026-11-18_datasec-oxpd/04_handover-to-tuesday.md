# Datasec / OXPd — HANDOVER from Friday (laptop seat) to Tuesday (Mac mini, Datasec seat)

Written 2026-11-19 by Friday on Kam's terminal word, verbatim: *"Once oxpd project is backed up, please send a note to tuesday to pick up this project but create handover notes of all the components that you have done so far and what needs to be done next.  we will continue with the claude project on this machine."*
Client: Datasec only. Everything below is about Datasec/OXPd.

## 0. BLUF
1. **Done:** the full analysis of the OXPd library folder (12 reports), the architecture document, the plan of attack and build, and all 25 of Kam's question answers folded into both documents (C-6 to C-30).
2. **Not done:** the Fable review pass of both documents Kam asked for (C-5, after Fable resets on Fri 2026-11-20 09:00 AEDT), Kam's confirmation of three readings, and anything at all built. **Nothing is built and no project folder is scaffolded. Building is a NEW ask for Kam** (it was outside Friday's grant).
3. **First act for Tuesday:** claim the project, read sections 2 to 4 below, then commission the Fable review pass at or after 09:00 on 2026-11-20.

## 1. Where everything is (all in the Wednesday brain repo, so a `git pull` in the TUESDAY tree has it)
Folder: `0_Brain/reference/2026-11-18_datasec-oxpd/` (commit with the 25 answers applied: `e5d5aa76ea`).

| file | what |
|---|---|
| `00_kam-brief_verbatim_2026-11-18.txt` | Kam's brief, verbatim (also C-1, C-2) |
| `01_analysis-brief.md` | the common brief the 12 analysis agents worked from |
| `analysis/A1…A7, B1…B3, C1, C2 *.md` | the 12 reports (A = the existing Workpath suite and the earlier OXPd 1 attempt; B = OXPd 2; C = OXPd 1.x). A1-A7 and B1-B3 written on Fable, C1-C2 on Opus after the Fable limit |
| `02_architecture.md` (+ `.pdf`, 26 pages) | the architecture: requirements, platform facts, the design, security, integration (Entra, mixed Workpath fleets), deployment methods, decisions, risks, change log |
| `03_plan-of-attack-and-build.md` (+ `.pdf`, 11 pages) | phases 0-6 with exit criteria, work packages, test strategy, dependencies, team and agent model, the 25-question table with answers, change log |
| `CLARIFICATIONS.md` | Kam's words numbered C-1 to C-30, copied by program from the board export. **Datasec standing rule:** this file moves to the project's own `1_Project_Definition/CLARIFICATIONS.md` once the project has a folder; a later ruling is a NEW entry |
| `04_handover-to-tuesday.md` | this file |

The library itself (source of the Workpath apps, the earlier OXPd 1 attempt, SDKs and docs): `/Volumes/Laptop-DEV/!CODING/Datasec/OXPd` on Kam's laptop drive. It was treated as **read-only**. NAS backup (this handover's precondition): `/Volumes/DEV-Working/Datasec/Friday/2026-11-19_oxpd-friday-work-and-library/` (Friday's documents plus the library; MANIFEST.txt with sha256 per file; secret-named files and folders excluded).

## 2. Components done (what each piece covers)
- **Analysis (12 reports).** A1 HP Authentication Manager source · A2 Mailflow and Teams source · A3 OneDrive, SharePoint, Universal Print source · A4 shared libraries and Workpath usage · A5 back end, licensing, admin and deployment source · A6 product behaviour specification from the docs · A7 the earlier OXPd 1 attempt · B1 OXPd 2 platform guides · B2 OXPd 2 API contracts · B3 OXPd 2 SDK, demos and forum · C1 OXPd 1.x platform specs and SDK · C2 OXPd 1.x field experience, JS and general.
- **Architecture (02).** A local server per site serving OXPd 2 and OXPd 1.x printers, keeping the Workpath suite untouched as the behavioural specification and reusing its back-end contracts (attribute set, gateway, Log Analytics streams, licence protocol); security architecture (no secret in source; TLS from the customer's internal authority, C-9); mixed-fleet integration with Workpath; both packagings (Linux container/appliance and Windows service, equal standing, C-17).
- **Plan (03).** Phase 0 environment and eight risk spikes on real hardware; phase 1 a thin vertical slice (card sign-in + OneDrive scan and print) on OXPd 2; phase 2 the same slice on OXPd 1.x; phase 3 the remaining sign-in methods and Microsoft 365 apps; phase 4 Universal Print; phase 5 deployment tooling, admin, licence, reporting; phase 6 hardening, certification, pilot, release. Sizes relative (S-XL), no dates (HP signing turnaround and devices dominate).
- **Questions.** 25 posted as cards on 2026-11-18; Kam answered all 25 on 2026-11-19 03:29-03:34. Twenty matched the assumptions; **five changed the design:** Q1 "Yes, HP confirmed" (C-30: OXPd 2 no longer held back), Q4 "May change" (C-27: the customer Azure gateway may change; its source is in none of the library's repositories), Q12 "No, ours only" (C-19: one stack per printer, a pre-install check, no coexistence testing), Q14 "Both equally" (C-17), Q15 "Full match of everything" (C-16: release 1 is full parity with the Workpath suite).
- **Kam's other rulings that bind the work:** C-3 the keys found in the library are old and rotated (no rotation action; the new server still keeps no secret in source; never copy a secret value into any document, locations only) · C-4/C-5 the model rule (below).

## 3. Open items (in order)
1. **Fable review pass (C-5).** Kam: *"use opus now and we will run a fable run to review"*. At or after **2026-11-20 09:00 AEDT** (when the Fable limit resets): an independent Fable agent reads 02 and 03 whole (with the 12 reports and CLARIFICATIONS as sources) and reports corrections: claims not supported by a report or the library, design gaps against full parity (C-16), contradictions with C-6..C-30. Apply the corrections (new change-log entries), re-render the PDFs, tell Kam on the panel with pointers.
2. **Three readings Friday offered Kam on the panel, NOT yet confirmed by him:** (a) Q1 "HP confirmed" covers HP's position only, not HP signing turnaround; (b) Q7 "Store it encrypted" allows an optional stored device-admin copy on OXPd 2, off by default; (c) Q15 "Full match of everything" means everything Workpath does, no more. Re-raise as cards only if a design step depends on one (each with a default).
3. **Phase 0 items Kam must provide** (03 §3 Phase 0, blocking items in bold there): an x86-64 PC for the OXPd 2 simulator and SPU; one OXPd 2 printer (FutureSmart 6, firmware ≥ 6.38.0.793, LDB developer mode, not a pilot unit); one FutureSmart 4.7/5.x printer for OXPd 1.x; a Workpath printer with the current suite; the six certified card readers (C-23); a test Entra tenant (custom security attributes, the existing HPAM registration reused per C-25, Universal Print licences, the onboarding Azure deployment, a Printer Administrator test account with MFA); the customer gateway's source; App Center/VNV access and the HP contact. These go to Kam as ONE card when the project moves to building, not before.
4. **Building = a new ask.** Friday's grant (EXPIRING-GRANTS row, Kam 2026-11-18 21:18) covered analysis, architecture, plan and questions only. Before any scaffold, build seat, Azure, GitHub or HP-portal action, Kam's word is needed (a card with the phase-0 shape). Nothing goes to HP or any human from a seat.

## 4. Rules that came with the project
- **Model:** C-1 "keep latest fable running for you and the sub agents" for architecture and design; C-4/C-5 Opus while Fable is out, then the Fable review. Read the model ID from `0_Brain/dashboard/data/models_latest.json` at launch; set a seat's model at launch, never `/model` in a pane.
- **Library read-only;** secrets: locations only, never values (C-3).
- **Datasec standing rules** (Tuesday's own mail to Friday, 2026-11-18 10:25 local, subject "ANSWER: Datasec/OXPd is yours; two Datasec rules apply at the document stage", read in full 2026-11-19): (1) the CLARIFICATIONS file, moved into the project's own folder when one exists; (2) every brief carries a PRIOR-WORK CHECK (02 §2 and 03 §2 hold the first one). Not binding until code starts: CodeQL on a PR before any commit reaches main, head-pinned merges, the demo/deploy holds. No Jira board for OXPd is known; a board is Kam's call.
- **Claim:** Friday releases `Datasec/OXPd — Friday (laptop)` when this handover is sent; Tuesday claims `Datasec/OXPd — Tuesday (Mac mini)` before driving it.

## 5. What Friday did NOT verify
- The library's contents were read by the 12 analysis agents, not re-read whole by Friday; each report cites `library:path:line` for its claims.
- The Fable review has not run, so 02 and 03 are DRAFTS: their claims have had Friday's read of the BLUFs, decisions and question tables, and Kam's answers, but no independent review yet.
