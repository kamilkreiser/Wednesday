# Gate 207 commission — Secuura / Blockchain, PR 2016 (KS-1407 N-1382-2: e2e case 12.5.3 calls the real change-password route on its own throwaway account), TIER 2 (test-only), ROUND 1 of 2

Written by Wednesday 2026-11-05 ~21:12 AEDT. Model: Sonnet. Tier 2: the PR changes one Playwright e2e spec and docs fragments only (no product file). If you find a product-file change, line 1 is NO GO (scope: product file changed). QA GATE: findings only; fix nothing; write nothing outside this folder; no box; no stack; post nothing to Linear or GitHub; no external network.
`verdict.md` holds the INCOMPLETE stub; overwrite at the end. Final line 1 is exactly `GO`, `GO WITH NOTES` or `NO GO (<reason>)`.
Read first, whole: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/qa-agent/BRIEF_TEMPLATE.md, then `ready_2016.txt` here (Seat J 16th's READY, verbatim). Clone read-only: `git clone --shared /Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files <subfolder here>`; if the head object is missing there, try gate 206's clone under /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate206-ks1804-pr2015/ as a second --shared source; if neither has it: NO GO (subject unreadable). Never `cd`; never a recursive grep/find over 0_Brain/reference, local-model/ or 5_Project_History.

## Subject (Wednesday's `git ls-remote origin`, 21:11:51 AEDT)
refs/pull/2016/head = `d91821a99dbbdadf83854b78dc5cebaeec1cbc99`; seat-stated base `5fc5569ed96a` (one commit; verify); develop NOW = `1e4bdcb899c44023404bcd33c511de6f7dde2f6e`. Seat-stated 3 files +65/-43: Blockchain/Dev/tests/e2e/tests/security-bad-actor.prelaunch.spec.ts and a fragment pair.

## Wednesday's rulings it implements (binding; to Seat J 16th, 06:05:32Z then 06:11:19Z which SUPERSEDES the first on the account)
Case 12.5.3 calls the REAL route POST /api/users/me/change-password (not the dead /api/auth/change-password); its assertions are unconditional (a non-200 fails the case); it uses its OWN throwaway account (never the shared seeded account, because the real route's 12-character strength check would refuse the old 7-9 character restore and leave the shared account changed for the ~130 later references); no restore step.

## Questions
1. Scope: exactly the 3 paths; no product file; read every changed line of the spec.
2. Ruling conformance, by reading: real route; no remaining 200-conditional around the assertions; own account created in the case (unique per run), strong random passwords, no reference to the shared seeded account's credentials in this case; session A probed after the change expects 401; no restore of any shared state. Name any other case in the file that the edit could affect (shared variables, ordering, fixtures).
3. Static checks: the seat's type check reproduced (0 errors in the spec on base and head; plant a type error and see it reported); grep controls for the dead route and the real route on base vs head.
4. The test is NOT RUN (no stack): state what that leaves unproven; do not try to stand a stack up.
5. Docs-fragments check with a planted defect.
6. Merge tree onto develop 1e4bdcb899c4: rc and tree; shared paths with everything merged since 5fc5569ed96a = 0 (planted control).

## Output
`verdict.md` (verdict line, BLUF, findings with severity, file:line, evidence path). Final message: verdict line + one line per finding.
