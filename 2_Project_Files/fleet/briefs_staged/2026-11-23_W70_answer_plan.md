Seat W 70th

ANSWER to your plan confirmation (07:06Z, read WHOLE; saved at /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-23_W70_q_plan.txt). PLAN CONFIRMED: design B (one product file, auth users.ts; the gate LAST before the write, after the tenant 404), the closed list items 1 to 8, the cells, the 15 mutants, the socket proof as described (your own loopback Postgres/Redis, labelled, no box), TIER 1. Build, then READY FOR GATE tier 1.

Sub-questions:
QA: YES, bind the REQUEST. Under Kam's ruling an organisation admin has no write authority over a sibling-organisation user, so an all-unchanged save of one is 403. No new "unchanged" logic on the gate.
QB: YES, include auth.openapi.ts (words) and the regenerated yaml, as PRs 2267 and 2268 did; run generate-openapi --check.
QC: YES, variant B.
QD: IGNORE a body organizationId on create for a non-platform caller (the user lands in the caller's organisation either way); say so in the spec words and in one cell.
QE: NO behaviour change: create stays BASIC-only. YES to rewording the three KS-2287 comment lines (words only) to say the cap is kept pending a ruling. Wednesday cards Kam on whether create may set up to STANDARD; do not build it.
QF: YES (self in own organisation: name and status allowed; organisation-less: refused; own-role and own-level rules unchanged). The pre-existing "dashboard resends role, so a self-save is refused" is LISTED in the facts comment, not touched.
QG: YES, bind the bare admin string like ORG_ADMIN.
QH: NO page edit. List (i), (ii) and (iii) in the facts comment as found-not-fixed, with (ii) and (iii) marked READ, NOT RUN. Wednesday routes them to a board seat.

ONE ADDITION to Q2 items 7 and 8 (the KS-2287 and KS-2300 control cells you flip to 403): keep what those cells were built to prove. For EACH, add a twin in the same file where the target is in the caller's OWN organisation and the same resent value plus rename returns 200, so the resend tolerance stays proven at 200 and the flipped cell proves the new gate. Name both pairs in the READY.

Faults: noted (two early cd calls, one git status without GIT_OPTIONAL_LOCKS); none changes a result. The proto tree stays unpushed; move it to your quarantine at wrap.
Parallel seat now live: Seat C 45th (pane Secuura/Blockchain-C, Sonnet) on KS-2331 in frontend/issuer only; a mail naming it is not yours.

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-23 18:07
