# Spark operator commission o159 (Secuura/Blockchain): SCREEN for the next Spark task, then run it. Wednesday, 06:37 rotation-successor seat, 2026-11-12 ~07:0x AEDT. Operator model: claude-sonnet-5-5.

WHY: the Spark is idle again (o158 delivered KS-1873 PASS 7/7). The rule: never keep it idle (learnings 2026-10-28). A thin pool is normal; an empty one needs a WRITTEN, MEASURED reason.

Method: as o156/o157/o158 (read ../2026-11-12_spark-operator-o158/commission.md, ../2026-11-12_spark-operator-o157/commission.md and its report.md whole; the four STOP pre-checks and the brief shape stand).

STEP 1, SCREEN (one GraphQL pass, paginated, never a per-issue REST loop): KS Backlog + Todo, easy to hard. Take the FIRST ticket that meets the Spark predicate:
- ONE product file (or test-only);
- the ticket NAMES the fix (anything shaped "decide whether" is a card, so skip it and say so);
- a runnable in-process test nearby to copy;
- not on Peter or Stuart;
- no held READY already names it (grep the key over 2_Project_Files/local-model/night/READY_*);
- its file is NOT a live lane's file.
The live lanes' files, so none of these: issuerCerts.ts, services/issuerCert.ts, tokenisation src/index.ts, auth password.ts, kyc src/index.ts, shared audit-logger.ts, auth routes/users.ts (Seat R 103rd); packages/shared ks1725-zod3-compat.test.ts and Blockchain/Dev/scripts/__tests__/* (Seat A 22nd); any file of an open PR (census, control PR 2125 api-gateway/src/index.ts must fire). Auth/security files are ALLOWED for a fully spelled-out edit (routing v1.0 rule 4: the PR then gets a tier-1 gate). Print every ticket you skipped and the clause it failed, so the screen is a list, not a feeling.

STEP 2: run the four pre-checks on the chosen ticket, then a Wednesday-style brief (≤ 3 edit points, current text and replacement, red-first test, control), then ONE round. Original + ONE rebrief. Read every PASS's +/- lines at source and hold it with hold_ready. Move the spent brief out of night/briefs/ into this folder's brief_spent/ (never delete). If a pre-check STOPs, return to step 1 and take the NEXT candidate, up to THREE candidates in this session; then report.

All constraints as o158 (no cd, no rm, read-only git in the Secuura checkout with GIT_OPTIONAL_LOCKS=0, writes only under 2_Project_Files/local-model/ and this folder, no secrets printed, no push/PR/board/Linear write/mail). If DevMASTER drops mid-run (it did during o158), re-check every file you wrote in the minutes before and say so.

OUTPUT: report.md in THIS folder, under 50 lines (the screen list, the chosen ticket(s), pre-check evidence, round result, held READY path). If your Write is refused, return the text in full.
