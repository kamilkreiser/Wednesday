# B1765 | Datasec / OXPd: apply reports A9 and A10 and today's answers (C-38 to C-44) to the architecture, the plan and the readiness statement. ONE WRITER.

From Tuesday (Datasec coordinator seat). Client: Datasec. Project: OXPd. Model: the newest Fable. Launched 2026-11-20 by Tuesday (s296). Tracked so a successor can RE-COMMISSION if `review/B1765_APPLIED.md` is absent (check the three documents against their `.pre-B1765` backups first: a half-applied pass is possible).

## Where you work
All under `/Volumes/Datasec_DEV/TUESDAY/0_Brain/reference/2026-11-18_datasec-oxpd/`: `02_architecture.md`, `03_plan-of-attack-and-build.md`, `05_readiness-to-build.md`, their PDFs, `CLARIFICATIONS.md` (C-1 to C-44; you do NOT edit it), `analysis/` (A1 to A10, B1 to B3, C1, C2), `review/`. The project folder `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2` holds COPIES of these: you never write there (Tuesday re-copies after you finish).

## Inputs to apply (read each WHOLE)
1. `analysis/A9_hpam-backend-gateway-and-infra.md`: its section PROPOSED CORRECTIONS (22) and its document comparisons. `hpam-api` is the sign-in gateway (three Azure Functions, SignalR hub `printerhub`); it does not check who sends an unlock message; `hpam-marketplace` is two offers (the customer-tenant deployment with its Log Analytics columns, and a deployable licence server); `infra_hpam` is the older Keycloak back end, out of scope under C-18.
2. `analysis/A10_oxpd1-solution-earlier-work.md`: its PROPOSED CORRECTIONS (8), including the sentence at `02` about the HP 1.8.4.1 library being "known to work" (the old build bundles 1.8.4), and the lines of report A7 it qualifies (A7 itself is NOT edited: record the qualification in the change log and in `review/B1765_APPLIED.md`).
3. The product owner's answers of 2026-11-20 in `CLARIFICATIONS.md`:
   - C-38: sensitivity labels are LEFT OUT of the rebuild ("Leave it out, as today"): replace the "not ruled" marks on them.
   - C-39: he has an HP MFP M577; firmware version and whether it may be wiped are NOT known: record it in the phase-0 kit list as stated, establish nothing about its OXPd generation.
   - C-40: the repositories received; `cc-api` not sent and (per A9, an inference) part of the older Keycloak back end; the repository `OXPD1` is empty.
   - C-41: questions and points to clarify live on ONE master list, Jira `OXPD2-1`; the kit checklist is Jira `OXPD2-2`. `05` should point to both.
   - C-42: the word to start the no-hardware work was GIVEN, with its limits (the option's detail) and his note that the kit is in hand and not configured. `05`'s BLUF ("Not yet"; "Your word to start building") must now say what is true: phase 0 has started on the no-hardware packages; what still waits (kit set-up, the tests on real printers and a tenant, HP's four undated items) is unchanged. The project folder is `OXPd_2`, the repository `datasecau/OXPd_2`.
   - C-43: deployment uses Datasec's existing HPK Deployment Utility, amended where OXPd needs it, not a new installer. Report A5 analysed it (the copy he sent has 0 files different). Find every place in `02` and `03` that designs or plans fleet deployment, onboarding or installation (search, with a control), say what the utility already does (from A5 and, where A5 is thin, from its source at `/Volumes/Datasec_DEV/!CODING/Datasec/OXPd_2/1_Project_Definition/Source_Documents/2026-11-20_from-product-owner/HPK-Deployment-Utility-main/`, read only, nothing run), which OXPd steps it could carry as it is, which need an amendment, and which it cannot carry; change the affected requirement rows and work packages accordingly, and mark as OPEN (for the master list) anything only the product owner can decide.
   - C-44: nothing to apply (a point for another team).
4. Question 10 of `05` (QR sign-in without MFA): its precondition is now answered by A9 (the gateway does not check the sender; two links in that reasoning are untested, say so). The DECISION stays the product owner's: do not decide it; update the question's text, its recommendation in the light of the evidence, and its default.
5. OQ-7 / question 7: the gateway half is now answered (A9). Update it in all three documents.

## Rules
- Backups first: `<file>.pre-B1765` for each of the six files (three `.md`, three `.pdf`), `cp -p` then `cmp`; never overwrite an existing backup of that name.
- Every change is a NEW change-log entry named `B1765 / <short id>` in `02` (its change-log section) and `03` (its change-log section); never rewrite an existing entry. In `05`, keep superseded text for the record where it was the product owner's reading matter (as B1760 did), and say what changed and when.
- A proposed correction you do NOT apply is listed in the APPLIED table with the reason. A correction that would change a product decision becomes an open point, not an edit.
- Every new sentence about behaviour carries its source (`analysis/A9...:line`, `analysis/A10...:line`, or a source path and line). Anything not established is written as unmeasured. No secret value anywhere (C-3): locations only.
- You write ONLY: the three documents, their PDFs, the six backups, `review/B1765_APPLIED.md` (one row per change: what, why, source line; counts by program; a list of the points to ADD to the master list `OXPD2-1` and of the items whose state changed on the kit list `OXPD2-2`, each as one ready sentence: Tuesday posts them, you do not call Jira).
- Re-render the three PDFs with `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/md2pdf/md2pdf.sh <file.md>`; say the page counts; if it fails, say what failed and leave the old PDF.
- No network call, no `gh`, no `az`, no git write, nothing to any person, nothing run from a source tree. No `cd` (a hook refuses it); absolute quoted paths; no unquoted word starting with `=`. Counts by program; an absence needs a search with a positive control.
- Make each document edit complete before the next and write to disk as you go: the machine lost power once today.

## Your reply to Tuesday
BLUF (what changed in the design and the plan, in five lines; does anything now change what the FIRST build seat should do: the repository layout, WP0.3, WP0.4 and the other no-hardware work packages; name each affected package); counts (corrections applied, not applied, new open points); the sentences for OXPD2-1 and OXPD2-2; page counts of the PDFs; what you did NOT read or verify.
