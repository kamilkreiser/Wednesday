# Gate 287, TIER 1 (Opus): PR 2131 (KS-625 option 2, Seat Y 10th). Commissioned 2026-11-09 17:1x by the 15:3x Wednesday seat (alone: its pair PR 2127 round 2 is still in the push queue and goes to gate 288).

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at FULL tier-1 depth.

Pins (Wednesday's ls-remote at 17:17:33 AEDT; RE-READ at start and end, and say whether each moved):
- develop 6beac8734a2f607200e3e71371b84268e1599029
- PR 2131 head 89081fae75e54e78e509d50a81cb0cd82c00eedd (6 paths: vc-issuer src/routes/presentations.ts, vc-issuer.openapi.ts, the regenerated docs/openapi/secuura-api.yaml, a new ks625 test, two fragments). READY: /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatY-10th/mail/out_05_ready_ks625.md (read whole).
- Overlap granted (OVL_IGNORE_PRS="2099 2073"): PR 2099 head 8967de8b1755 and PR 2073 head 2684a29d8f57 also change docs/openapi/secuura-api.yaml (hunks apart by the seat's read). Ruling: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-09_Y10_answer_ovl_ks625.md. Plan rulings D4 + (iii): /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-09_Y10_answer_plan.md.
- Kam's ruling: card secuura-backlog-31-decisions-1109 = a, row A7, option 2 NOW: "Make it honest now. Answer 'not verified' until the check exists." Option 1 (the real holder-signature check) is a LATER ticket and must NOT be in this PR.

Questions:
1. POST /api/presentations/verify (PUBLIC by the seat's read: gateway proxy.ts:1015-1022, spec security: []): does it now answer verified:false for EVERY presentation, including one with no proof, a garbage proofValue, and matching challenge/domain, with the existing field names only? Is anything else in the response or in the credential-verify path changed? Is no signature verifier written?
2. Consumers of a 'verified' answer in code (frontends, gateway, other services, tests, smoke scripts): what each does now that it always reads false; does any flow that worked on develop now break (name it; demo is frozen, so nothing deploys, but say it)?
3. The spec: the VpVerifyResponse example in vc-issuer.openapi.ts and the regenerated secuura-api.yaml: verified false and presentationProofValid false, one description sentence; check:openapi passes; is the yaml change ONLY what regeneration of this spec change produces (diff the regenerated yaml against develop's, no unrelated churn)?
4. The union with PRs 2073 and 2099 on secuura-api.yaml: merge-tree of 2131 with each and with both, in each order; then regenerate the yaml on the union and run check:openapi there (the later merge must pass it).
5. Red first as declared (4 FAIL / 3 PASS on develop, 7/7 after); the seat's mutants plus ONE of your own; the 842 existing vc-issuer cells identical; tsc, eslint, ratchet.
6. The PR body's correction that the route is public, and its sentence that option 1 remains open on KS-625: present and true?
Constraints: clone on the boot volume /private/tmp/g287 (no rm; size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; never push; never run the hook against the real remote; no real .env; no box, kintsugi or demo; keep load1 under 8; df DevMASTER at start and end.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate287-tier1-pr2131-ks625/verdict.md (if your Write is refused, put the WHOLE verdict in your final message). Line 1 exactly: 'PR 2131: <V>' with V one of GO | GO WITH NOTES | NO GO. Then FOUND / TESTED / HOW, NOT TESTED, findings with ids G287-<n> and severities. Findings only; post nothing; mail nothing.
