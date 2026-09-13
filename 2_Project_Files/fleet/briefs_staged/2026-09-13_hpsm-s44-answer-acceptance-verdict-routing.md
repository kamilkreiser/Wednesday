BLUF. **The acceptance+security gate on caf63fd returned DELIVERABLES: NO GO · SECURITY: GO WITH FINDINGS** (verdict mail 09:58:13Z, DKIM pass). Tuesday read the report whole: `/Volumes/KK_T9_External_HDD/!CODING/Testing Agent MAIN/projects/hpsm/reports/2026-09-13-composer-caf63fd-brief-acceptance-security-tier1/report.md`, 538 lines.
- **This is a NEW class (acceptance against the original brief), so this is fix round 1 of 2 under the cap.**
- **Your merge order 1–6 and the confirmed plan are unchanged.** Put the two Majors in your queue AFTER step 6 (the rolling upgrade) and name their lanes in a STATUS.

## Routing
1. **D-B1 (Blocker, the live gate):** already in hand. Gate fix b-tight waits for Kam's word. Nothing changes.
2. **D-M1 (Major): required discovery is never required.**
   - The measurement: a policy releases with 0 of 26 answers while §14.1 T3 `all_required_discovery_complete` reads true. Both content releases define 0 typed sub-answers and 0 show_when/required_when, so `MISSING_REQUIRED_INPUT` (`packages/engine/src/resolve.ts:694-706`) can never fire.
   - Fix-shape (the gate's): a Required question with no answer, and no sub-answer definition, makes the term false (or the release declares the term unmeasurable). Load the seed-contract C9 breakdown for the §9.1 trigger questions. Regression: 0 answers on the shipped bundle gives release 409 naming the term; E8 with D-006 unanswered gives MISSING_REQUIRED_INPUT.
   - **Paths overlap C11 and the credential round (packages/engine, packages/content).** Partition it by exact file, or sequence it.
   - **DEMO IMPACT: STOP for Tuesday before this reaches live.** It changes what Kam's release walk-through needs (discovery answers, and possibly a content hash change that strands tonight's A and B engagements). Merging to local main on GREEN is fine; the upgrade carrying it waits for Tuesday.
3. **D-M2 (Major): an exception with no compensating control and no evidence gets 201, is approved, and releases.**
   - Fix-shape: required fields per trigger kind in the contract (422 naming the field), plus a validate stage that refuses an incomplete exception. Regression: every trigger × every missing field gives 422; a legacy incomplete exception makes release 409.
   - **Paths:** `packages/api-contract` (`ExceptionCreate`) + `apps/api` exception routes + the validate stage. The contract is shared with F-API/F-WEB, so sequence it against the feedback merge.
   - **DEMO IMPACT:** tonight's engagements may carry incomplete exceptions. **Measure whether release or validate on A and B changes before the upgrade that carries it, and STOP for Tuesday if it does.**
4. **S-m3 (Minor): a ~2,000-deep JSON body makes the recursive credential scanner (`apps/api/src/secrets.ts` `stringsIn`) answer 500.** Goes into the credential-detector round (same file family). Iterative traversal with a depth cap → 422 `PAYLOAD_TOO_DEEP`.
5. **S-m1 (headers) and S-m2 (Mailpit, MinIO S3 and worker routed onto the public edge):** both live in `docker/edge.nginx.conf`, a SEAT root file. **BACKLOG now, with priority.** Propose them as one small edge commit after the fix round, with a measurement that the app does not use `/objects/`, `/mail/` or `/worker/` from the browser. Not before Monday unless that is measured safe.
6. **D-m1…D-m10, D-p1, D-p3, D-p4, S-p1:** into the BACKLOG fold, each with its report ID and path. **Two to flag in the fold:**
   - D-m5 (S9's register overflows at 1440) is a sibling of W5-M3. If FX-S7's scoped rules make it cheap, say so.
   - D-m6 (S5 re-asks D-001…D-006 against ruling A-17) needs Kam's ruling on A-17 before anyone changes it. Record it as that.
7. **D-p2 (the "intentional switch-ON failure" ruling versus the build) is already settled.** D1 is retired (S43, analysis f88bb73), and your chain uses a zero-failure verdict.

## What does not change
- The next rolling upgrade still carries only merge steps 1–5. The public-URL browser check stays in the post-check.
- After the gate fix is applied, Tuesday commissions a re-run of the LIVE half of this gate (the walk-through and probes 2, 3, 5, 7, 9, 11–13). **Do not create anything on live for it.**
- Findings are yours to fix through the partition. No Jira. No push.
