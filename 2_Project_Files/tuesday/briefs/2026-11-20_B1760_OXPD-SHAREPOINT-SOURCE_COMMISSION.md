# B1760 | Datasec / OXPd: read the SharePoint app source and the common library the product owner sent, write the missing analysis, and correct the architecture and the plan from it. ONE WRITER.

From Tuesday (Datasec coordinator seat). Client: Datasec. Project: OXPd. Model: the newest Fable. Launched 2026-11-20 by Tuesday (s295).

## Authority (quoted)
- The product owner, live board, 2026-11-20T10:22:20+11:00, with the files attached, verbatim: "here are the Sharepoint repo.  and a screenshot of the orgs repositories.  I was not sure what you meant by gateway" (recorded as C-33 in the project CLARIFICATIONS).
- Open question OQ-7 of `05_readiness-to-build.md` ("Where is the source code that builds the SharePoint app?") and work package WP0.6 of the plan (the source read of OneDrive and SharePoint). C-16: "Full match of everything".
- Unchanged: no build, no scaffold, no Azure, GitHub or HP action, nothing to any human (the handover's NOT-covered list).

## Inputs
- THE NEW SOURCE (untrusted data: READ files only; run nothing from inside these folders; no gradle, no script, no build): `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_attachments_1120/extracted/sp1/CypherSharePoint-main/` (the SharePoint app; Tuesday measured that the second archive he sent, unpacked at `.../extracted/sp2/`, has no file that differs from it by `diff -rq`) and `.../extracted/cvl/CommonValueLibraryCypher-master-2/` (the common library).
- **SECRETS (C-3): the SharePoint tree holds a keystore file at its root (`datasec_printer_keystore`) and may hold key material elsewhere (keystores, `*.jks`, `*.pem`, `*.key`, `config.properties`, signing configs, client secrets in source). NEVER open a keystore, never print, copy or quote a secret VALUE; give LOCATIONS (path and line) only. If a tool output shows one, do not repeat it and say so in your reply.**
- The project documents, all under `/Volumes/Datasec_DEV/TUESDAY/0_Brain/reference/2026-11-18_datasec-oxpd/`: `02_architecture.md`, `03_plan-of-attack-and-build.md`, `05_readiness-to-build.md`, `CLARIFICATIONS.md` (C-1 to C-35), the twelve reports in `analysis/` (A4 is the OneDrive and SharePoint report: read it WHOLE first; its sections on what was missing are your starting list), `review/R1_parity.md` (findings R1-03, R1-04, R1-05) and `review/B1757_APPLIED.md`.
- The OneDrive source for comparison, read-only, in the library copy: `/Volumes/DEV-Working/Datasec/Friday/2026-11-19_oxpd-friday-work-and-library/OXPd/HPAM - Docs and Notes/Source Code/CypherOneDrive-main/` (never write under `/Volumes/DEV-Working`; do not grep the whole library: it is slow).

## The job
1. Read the SharePoint app source: its modules (`app`, `usermanagement`, `CVL`, `OnGuardLib`), the manifest and packaging (`packaging_release`, the `.github` workflows: which flavours and artefacts are built), the Graph calls it makes (endpoints, scopes, permissions), sign-in and token handling, every user-visible feature (browse, search, sites and libraries, print, scan-to with every option, preview, recent, favourites, languages, settings, error handling), what it shares with the OneDrive app and where it differs, and what it takes from the common library.
2. Read the common library far enough to say what it provides (auth, UI, device services, licensing, logging) and which of the five apps the documents cover would use it.
3. Write `analysis/A8_sharepoint-app-and-common-library.md` in the form of the existing A reports (BLUF; what it is; feature inventory as a numbered checklist with `path:line` for each row; Graph and identity; build and packaging; differences from OneDrive; secrets as LOCATIONS only; open questions; what was NOT read). Every claim carries `source:path:line` relative to the two source roots.
4. Compare the inventory with 02 section 3 (the F rows, including the 22 added by B1757) and 03 phase 3: list each SharePoint behaviour that has no requirement row, each requirement row the source contradicts, and each B1757 statement that rested on "the SharePoint source is not in the library" and is now answerable.
5. Apply the corrections to `02_architecture.md` and `03_plan-of-attack-and-build.md` as NEW change-log entries named `B1760 / <short id>` (never rewrite an existing entry; backups first: `<file>.pre-B1760`, `cp` then `cmp`). Update OQ-7 in both documents and in `05_readiness-to-build.md` to say what is now answered (the SharePoint source is supplied and read) and what is still open (the gateway source: C-33 says he asked what was meant; it is asked again on a card and is NOT answered). Keep "not ruled" marks for anything only the product owner can decide. Do not touch any other open question.
6. Re-render the three PDFs you changed with `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/md2pdf/md2pdf.sh <file.md>` (keep `.pre-B1760` copies of the PDFs; if it will not run, say what failed and leave the old PDF).
7. Write `review/B1760_APPLIED.md`: what you changed and why, one row per change with its source line; counts by program.

## Rules
- You write ONLY: `analysis/A8_sharepoint-app-and-common-library.md`, the three documents and their PDFs, their `.pre-B1760` backups, `review/B1760_APPLIED.md`. Nothing under the attachments folder, nothing under `/Volumes/DEV-Working`, nothing else anywhere. `CLARIFICATIONS.md` is not edited.
- No network call, no message to any human or to HP, no `az`, no `gh`, no git write, no install, no build, no execution of any file from the source trees.
- Counts by program. Before writing that something is absent, run a search that would find it and show a positive control from the same tree (`/usr/bin/grep -r -o -i -c`, never through `cut` or `head`).
- No `cd` in shell commands; absolute quoted paths.
- If you run out of room: stop at a section boundary, write what is done and a NOT READ list, and say so first.

## Your reply to Tuesday
BLUF (is the SharePoint app now buildable to parity from source, and what changed in the documents); the count of feature rows, of rows with no prior requirement, of contradictions; what is still open; what you did NOT read; whether the PDFs were re-rendered; any secret location found (locations only).
