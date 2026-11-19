# B1757 | Datasec / OXPd: apply the Fable review (B1753) to the architecture and the plan, and write the readiness statement. ONE WRITER.

From Tuesday (Datasec coordinator seat). Client: Datasec. Project: OXPd. Model: the newest Fable. Drafted and launched 2026-11-20 by Tuesday (s295).

## Authority (quoted)
- The product owner, Tuesday terminal, 2026-11-20, verbatim: "please use fable to review the oxpd project, architecture and plan of attack.  continue where friday left off and let me know when you are ready to build".
- CLARIFICATIONS C-5: the Fable review run of documents synthesised on Opus. Handover section 3 item 1: apply corrections as NEW change-log entries, re-render the PDFs.

## Inputs (all under `/Volumes/Datasec_DEV/TUESDAY/0_Brain/reference/2026-11-18_datasec-oxpd/`)
- The two documents you EDIT: `02_architecture.md`, `03_plan-of-attack-and-build.md`.
- The four review files, read each WHOLE first: `review/R1_parity.md` (20 findings), `review/R2_platforms.md` (23), `review/R3_security-and-integration.md`, `review/R4_consistency-and-coverage.md` (29; 1 Blocker R4-02).
- Sources: `CLARIFICATIONS.md` (C-1 to C-30), `analysis/` (twelve reports), the library READ-ONLY at `/Volumes/DEV-Working/Datasec/Friday/2026-11-19_oxpd-friday-work-and-library/OXPd` (never write, move or delete anything under `/Volumes/DEV-Working`; a recursive grep over the whole library is slow: target a subfolder).
- The card texts (option labels AND details) for the 25 OXPd cards: `/Volumes/Datasec_DEV/TUESDAY/0_Brain/dashboard/data/decisions.json` (ids `datasec-oxpd-q..-1118`; fields `options[].detail`, `ruled_choice`).

## What Tuesday already checked at source (four findings, all held)
- R4-02 (Blocker): 02 line 274 names HP `OXPd2Lib` as the C2 adapter technology; 02 R16 line 792 says OXPd2Lib only after the production SDK; card q20 option a detail reads "Rewrite logic; ship older library unchanged; newer library after beta."
- R1-03: `CypherOneDrive-main/.github/workflows/release.yml:129` builds `assembleOnedriveforbusinessRelease` only; `OneDriveConstants.java:13-18` has the personal and business endpoint constants commented out.
- R3 F1: the string literal at `CardValidator.kt:10` and at `Encryptor.kt:12` is the same value (compared by hash; NEVER print it).
- Every other finding is the reviewer's claim, unverified by Tuesday. Before you apply a correction that changes a design decision, a phase, an exit criterion or a requirement row, open the source line the finding cites and confirm it. If a finding does not hold at source, do NOT apply it: record it under REJECTED with what you read.

## The job
1. Make backup copies first: `02_architecture.md.pre-B1757` and `03_plan-of-attack-and-build.md.pre-B1757` (cp, then cmp).
2. Work every finding in all four files (all severities). For each, one disposition:
   - APPLIED: the document text is corrected. Use the reviewer's proposed text as a proposal, not gospel: it must agree with the source you opened. Each applied correction gets a NEW change-log entry (02 section 11, 03 section 9) naming the finding id (for example "B1757 / R4-02"), what changed and the source line. Never rewrite or delete existing change-log entries.
   - OPEN FOR THE PRODUCT OWNER: the finding turns on something only he can decide (the three open readings Q1, Q7, Q15; a ruling applied wider than the card option he tapped; a scope choice; anything that needs HP or a human). Then: make the document conform to the NARROWEST reading the card text supports, mark the wider thing clearly as "not ruled: open question OQ-n", and never write "(ruled, C-n)" for something the card option does not say. Do not resolve it, do not invent his answer.
   - SPIKE: the finding is settled only by a measurement on hardware or a tenant. Add or correct the phase-0 spike (what it must measure, pass and fail) in 03, and the matching risk in 02.
   - REJECTED: does not hold at source (say what you read), or already recorded in the document as a decision or risk (cite it).
   - Where two lanes found the same thing (for example the 18 uncited A6 rows, R1-01 and R4-04; the non-exportable key against the HA pair, R2 F6 and R3 F8; section 8.2 step order), apply once and name both ids.
3. Parity (C-16, "Full match of everything"): every A6 checklist row and every Workpath feature the reviewers found without a requirement row gets a requirement row in 02 section 3 and a work package and test in 03, OR is listed under OPEN FOR THE PRODUCT OWNER with the reason (for example SharePoint: shipped as its own package, source not in the library). The parity gate text (E3.1, E6.8) must be passable as written: say exactly which deviations are allowed and by which C-entry.
4. Phase order: no exit criterion may depend on a component built in a later phase (R4-07). Fix the order or the criterion, and say which.
5. Keep both documents internally consistent after the edits: section numbers, cross-references, the question table in 03 section 8 against CLARIFICATIONS.
6. Re-render both PDFs beside the markdown, replacing `02_architecture.pdf` and `03_plan-of-attack-and-build.pdf` (keep the old ones as `.pre-B1757` copies). The renderer is `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/md2pdf` (read its files or README for the invocation; if it will not run, say exactly what failed and leave the old PDFs in place: do not install anything).
7. Write `review/B1757_APPLIED.md`: a table with one row per finding (id, severity, disposition, where applied or why not, source line you opened), then the counts by disposition (they must sum to the number of findings in the four files: count them by program), then REJECTED with reasons.
8. Write `05_readiness-to-build.md` (for the product owner; plain words, BLUF first, no internal seat names, no lane ids in the BLUF):
   - BLUF: is the project ready to start building, and if not, exactly what stands between here and a start.
   - What the review changed, in ten lines at most.
   - OPEN QUESTIONS FOR THE PRODUCT OWNER: each as one decision with options, a recommendation and the default the design takes meanwhile; say which phase each one blocks (many block nothing in phase 0).
   - PHASE 0 NEEDS: the hardware, tenants, accounts, firmware, keys and HP items phase 0 requires (include what R2 F5 found missing), each with who must supply it.
   - WHAT CAN START WITHOUT ANY OF THE ABOVE: the work packages that need no hardware, no tenant and no answer.
   - WHAT WAS NOT VERIFIED: claims still resting on a report line only, sources not in the library.

## Rules
- You write ONLY: the two documents, their two PDFs, the four `.pre-B1757` backups, `review/B1757_APPLIED.md`, `05_readiness-to-build.md`. Nothing else anywhere. The four review files and CLARIFICATIONS are not edited.
- No network call, no message to any human or to HP, no `az`, no `gh`, no git write, no install, no build, no project scaffold.
- SECRETS (C-3): never print, copy or quote a secret VALUE (key, client secret, password, card key, keystore content); locations only. If a tool output shows one, do not repeat it and say so in your reply. R3 reports that the library copy on the NAS contains key material: do not open keystores, `config.properties`, `.cfg`, `.pem` or `.key` files.
- Every count you write is counted by program. Before writing that something is absent, run a search that would find it and show a positive control (`/usr/bin/grep -o -i -c`, never through `cut` or `head`).
- No `cd` in shell commands; absolute quoted paths.
- If you run out of room: stop at a finding boundary, write B1757_APPLIED.md with what is done and a NOT DONE list of finding ids, and say so first in your reply. A partial pass that says so is useful.

## Your reply to Tuesday
The BLUF of `05_readiness-to-build.md`; the disposition counts; the list of OPEN FOR THE PRODUCT OWNER items by title; whether both PDFs were re-rendered; anything NOT DONE.
