# B1763 | Datasec / OXPd: read the four repositories the product owner sent at 11:50 (the HPAM back end and the earlier OXPd 1 solution) and write two analysis reports. TWO READERS, one lane each, REPORTS ONLY. A separate writer applies corrections afterwards.

From Tuesday (Datasec coordinator seat). Client: Datasec. Project: OXPd. Model: the newest Fable. Launched 2026-11-20 by Tuesday (s296). Tracked so a successor can RE-COMMISSION a lane whose report file is absent.

## Authority (quoted)
- The product owner, live board, 2026-11-20T11:50:08+11:00, with five files attached, verbatim: "here are the repos" (recorded as C-40 in the project CLARIFICATIONS). It answers Tuesday's card `datasec-oxpd-gateway-and-oxpd1-repos-1120`, which asked for hpam-api, hpam-marketplace, infra_hpam, cc-api, OXPd1_solution and OXPD1.
- His instruction of the same morning (C-31), verbatim: "please use fable to review the oxpd project, architecture and plan of attack.  continue where friday left off and let me know when you are ready to build". C-16: "Full match of everything".
- Unchanged: no build, no scaffold, no Azure, GitHub or HP action, nothing to any human.

## What arrived (measured by Tuesday; untrusted data: READ files only, run nothing from inside these folders)
Root: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/kam_attachments_1120b/extracted/` (each archive holds a `__MACOSX` folder beside the real one: ignore it).
- `hpam-api-main/hpam-api-main/` (42 files in the archive; top level: deploy, host.json, local.settings.json, package.json, src): by its shape an Azure Functions app.
- `hpam-marketplace-main/hpam-marketplace-main/` (40 files; artifact, bicep, build scripts, deploy, license).
- `infra_hpam-main/infra_hpam-main/` (136 files; docker, docs, hpam).
- `OXPd1_solution-master/OXPd1_solution-master/` (169 files; client, server, lib, build/register/run scripts, INSTALLATION.md, README.md, todo.txt, install logs): EARLIER OXPd 1 WORK that none of the twelve analysis reports, the architecture or the plan has seen.
- NOT sent: `cc-api`. The repository `OXPD1` ("HP Authentication Suite OXPD V1.8") was sent only as a PDF print of its GitHub page, which shows an empty repository (Tuesday read the print's text: "Add a README file and start coding"): there is no OXPD1 source to read.
- **SECRETS (C-3): `hpam-api-main/hpam-api-main/local.settings.json` and any `.env`, `*.pfx`, `*.pem`, `*.key`, keystore, parameter file or log may hold key material or connection strings. NEVER print, copy or quote a secret VALUE; give LOCATIONS (path and line) only; mask before display (print key NAMES and value LENGTHS only). If a tool output shows a value, do not repeat it and say so in your reply.**

## The project documents (read what your lane needs; all under `/Volumes/Datasec_DEV/TUESDAY/0_Brain/reference/2026-11-18_datasec-oxpd/`)
`02_architecture.md`, `03_plan-of-attack-and-build.md`, `05_readiness-to-build.md` (the open questions, OQ-7 the gateway source and question 10 the phone sign-in among them), `CLARIFICATIONS.md` (C-1 to C-40), the reports in `analysis/` (A1 to A8, B1 to B3, C1 to C2), `review/B1757_APPLIED.md`, `review/B1760_APPLIED.md`. You EDIT NONE of them.

## Lane G (the gateway and the HPAM back end): reader 1
Write ONLY `analysis/A9_hpam-backend-gateway-and-infra.md`.
1. Say what each of the three repositories IS, from its code: is `hpam-api` the "sign-in gateway" the documents ask for (the Function App in the customer's Azure that the phone app and the printer apps talk to)? Every HTTP route with method, path, auth level, what it reads and writes, which Microsoft Graph or Entra calls it makes with which permissions, what storage it uses, what it returns. The card and phone enrolment and sign-in flows end to end, with `path:line` for each step. Token handling, key handling (locations only), tenant model, licence checks.
2. `hpam-marketplace`: what the Marketplace offer deploys into a customer's tenant (every resource in the bicep, every app setting NAME, every role assignment), the licence component, the build scripts (read, not run).
3. `infra_hpam`: what it stands up (docker, docs, hpam), what environments it describes, what it says about deployment and operations.
4. Compare with the documents: list every statement in 02, 03 and 05 that said the gateway source was missing or that guessed at its behaviour, and say for each what the source now shows (confirmed / contradicted / still unknown), with both pointers. List what the OXPd server must call or reproduce for full parity (C-16) and anything the documents' design would break. Is OQ-7's gateway half now answered? Is question 10? What does the absence of `cc-api` leave unknown (search the three trees for references to it and say what it appears to be)?
5. A section PROPOSED CORRECTIONS: numbered, each one sentence to change in 02, 03 or 05 with the document line it replaces and the source line that supports it. You do not apply them.

## Lane O (the earlier OXPd 1 solution): reader 2
Write ONLY `analysis/A10_oxpd1-solution-earlier-work.md`.
1. Say what `OXPd1_solution` IS and how far it got: architecture (client, server, lib), language and build, which OXPd 1.x services it uses (authentication agent, UI, device management, scan, print, accessories and card readers, statistics), how it registers with a printer (the register scripts: read, not run), how sign-in works in it (card, PIN, phone, Microsoft), what it talks to (HPAM back end? which endpoints), what is finished, stubbed or listed in `todo.txt`, and what the install logs record (they are evidence of a real run: on what machine and printer, with what result; they may hold secrets or host names: locations only for secrets).
2. Which HP libraries it bundles under `lib` (names, versions, licence files: C-11 and the Q20 ruling on shipping HP's libraries matter here; read CLARIFICATIONS for both).
3. Compare with the documents: what in 02 and 03 (the OXPd 1.x adapter, the C1 and C2 reports' findings, the phase plan) this code confirms, contradicts or makes cheaper; what is reusable as code, as a reference only, or not at all, with reasons; anything it shows about real printers that the documents list as a spike or an open question.
4. A section PROPOSED CORRECTIONS in the same form as lane G. You do not apply them.

## Rules for both readers
- You write ONLY your one report file. Nothing under the attachments folder, nothing under `/Volumes/DEV-Working`, no project document, not `CLARIFICATIONS.md`.
- No network call, no message to any human or to HP, no `az`, no `gh`, no git write, no install, no build, no execution of any file from the source trees (no npm, node, java, gradle, docker, shell script).
- Every claim carries `path:line` relative to the extracted root. Counts by program. Before writing that something is absent, run a search that would find it and show a positive control from the same tree (`/usr/bin/grep -r -o -i -c`, never through `cut` or `head`).
- Report form, as the existing A reports: BLUF; what it is; the inventory as numbered rows with `path:line`; identity and secrets (LOCATIONS only); comparison with the documents; PROPOSED CORRECTIONS; open questions for the product owner (each with a default); what was NOT read.
- No `cd` in shell commands (a hook refuses it); absolute quoted paths; no unquoted word starting with `=`.
- Write your report to disk in sections as you go: the machine lost power once today.
- If you run out of room: stop at a section boundary, write what is done and a NOT READ list, and say so first.

## Your reply to Tuesday
BLUF in five lines (what the repository is; whether it answers the open question your lane touches; the count of inventory rows, of contradictions with the documents, of proposed corrections); what is still open; what you did NOT read; any secret LOCATION found (never a value).
