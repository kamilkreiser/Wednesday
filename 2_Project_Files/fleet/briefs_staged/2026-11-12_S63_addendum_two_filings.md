Seat S 63rd

ADDENDUM: two filings, queued AFTER your old-tenant SharePoint ticket (my ANSWER of 19:42Z). Each needs a board search first; a hit means a comment, not a new ticket.

FILING 1: the pre-push hook does not run the packages/shared vitest suite.
Source: Seat A 21st's wrap of 19:48Z. It is an INFERENCE from an outcome, not a read of the leg list. On clean develop, packages/shared carries two reds: ks1725-zod3-compat (KS-2170) and wallet-signature (the Node v26.8.1 class, KS-1727/KS-1739). A 21st's push hook still ended "13/16 legs ran, 3 SKIPPED. Nothing failed."
Your job:
1. Read the hook's leg list at develop c78c80bd5370 (Blockchain/Dev/.githooks/pre-push or what it calls; GraphQL or one tree read). Say which leg, if any, runs packages/shared tests, and whether a SKIPPED leg is the one.
2. If no leg covers it, file ONE Low (4) ticket: "Pre-push hook does not run the packages/shared vitest suite". Put the leg list in the body as you measured it, and the two reds that pass the hook as the evidence.
3. If a leg covers it but was skipped, say why it skips (its condition) and file the same ticket worded around the skip.

FILING 2: eight raw-email log sites outside KS-1873.
Source: Spark operator o157's census, measured by it with a paren-matched parse of 244 logger calls and a positive control. Report: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_spark-operator-o157/report.md, item 3. KS-1873's own site (users.ts:678) is being fixed in a separate lane; do not touch it.
The eight sites are: services/auth auth.ts:291 (a dev-only SMTP link), and userRepo.ts:1753, 1764, 1773, 1796, 1842, 1865 and 1867 (demo seeds).
Your job:
1. Re-read each line at c78c80bd5370 and say whether it can run outside dev or demo seeding (read the guard around it).
2. File ONE Low (4) ticket, "Raw email addresses in 8 auth log lines (demo seeds and a dev-only SMTP link)". Give each site's reach, and the fix shape the rest of the service already uses (maskEmail / hashEmail, or the user id). Write "Refs KS-1873" in the body, never a closing word. It is a CLAUDE-BUILD row.

Report both keys in your next STATUS. Add allow-list edits S63-D citing this ADDENDUM's subject. Grant: as your plan ANSWER. Not a signature class: two board filings with undos.

Wednesday
