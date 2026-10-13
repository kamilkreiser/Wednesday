# Gate brief: pull request 1547 (KS-1594) fix round 1, DELTA, Opus tier 1

Commissioned by the Wednesday seat. 0_Brain paths are relative to /Volumes/DevMASTER/WEDNESDAY/; project paths under /Volumes/DevMASTER/!CODING/Secuura/Blockchain/.

## What you are gating
- Head 0f97a0157635690ee41d51bf620586e05fff65c2 (Wednesday's own ls-remote of refs/pull/1547/head = the author's). One commit on top of the round-1 gated head a897f57eba3d39afd8fd19e2895cb0e83188ab58. develop 026c2d1614065c79fc8d96007ac0d80f19fb9363.
- Round-1 verdict: 0_Brain/reference/2026-10-13_gate-pr1547/verdict.md (GO WITH NOTE, m1-m3, hash c7a359227342f0b6); its evidence is in evidence.tgz beside it (the 6158-request matrix test, classify.js, mutants).
- THE RULE THIS ROUND MUST IMPLEMENT (Kam's card secuura-provisioning-scope-escapes-the-org-bound, ruled b at 12:55:49 AEDT, verbatim option text: "Allow it, but bound the provisioning key to the minting admin's own scope"; Wednesday's ruling to the author at 09:59Z): `isProvisioningCapable(requested) && !callerIsPlatform && requestedOrg === null` -> 403, where requestedOrg is the BODY organizationId after normalisation, NO fall-back to the caller's claim. This is meant to equal the security route's condition (author's read: services/security/src/index.ts :1239-1247 on develop). A non-platform caller naming a FOREIGN org is refused by (c). A non-string organizationId -> 400 before normalisation, with no row written.
- Author's claims (NOT evidence): c1-c5 unchanged at 403; new c16 (ORG_ADMIN(A1) + register + org A1 -> 201 bound to A1); c17 (four non-string shapes -> 400, no row); c18 (super_admin and SUPER_ADMIN -> 201, coverage). 23/23 cells in both modes; red-first 5 failed. Ten mutants killed (T1-T6, G7a deleted clause, G7b inverted clause, G8 SYSTEM_ADMIN-only, M2m guard removed). The author's first G8 was a load failure caught late, so check every kill carries a real assertion message.

## Gate
1. Diff a897f57e..0f97a015: every hunk named; nothing outside the two files.
2. Re-read the security route's condition YOURSELF at develop 026c2d16 and state whether the two doors now give the same verdict for every (role, permission, organizationId) shape. Re-run your round-1 matrix (from evidence.tgz) on the new head in both tenancy modes, with the classifier updated to the rule above: zero false passes (non-platform provisioning-capable key stored org-less or foreign), zero false refusals (ORG_ADMIN naming its own org, any case or whitespace, -> 201 bound to own), zero rows on refusals, zero 5xx. Develop as the control.
3. m2: every non-string shape -> 400 and row count unchanged, for platform AND non-platform callers; null and absent still behave as absent.
4. Mutants: re-run the author's ten and add at least three of your own (e.g. the 400 guard after normalisation; requestedOrg compared raw; the platform check reading the wrong field). Report by cell name, with a comment-only control; reject any kill whose failures carry an empty message.
5. Merge prediction on the live develop tip: overlap with a planted control, merge-tree with a conflicting negative control.

## Rules
Read-only on the project: clone --shared into YOUR scratchpad and fetch there. No git write verb in !CODING, no push, no GitHub/Linear writes, no Docker, no remote box. Never cd; never delete; never rm inside bash -c. Your own Postgres on a free port (lsof first); avoid 55413, 55414, 55418, 55419, 55436, 55440, 55463. Write only here and in your scratchpad (raw outputs under evidence/, never a directory named out); npm and tar outputs need explicit absolute destinations in your scratchpad.

## Output
0_Brain/reference/2026-10-13_gate-pr1547-r2/verdict.md: VERDICT on line 1, sha256/16 of the report on LINE 2 (delete line 2, sha256 the rest, first 16 hex), FOUND / TESTED / HOW, NOT tested, severities with file:line. Round 2 of 2 under the cap. Deploys only in the KS-1570 round.
