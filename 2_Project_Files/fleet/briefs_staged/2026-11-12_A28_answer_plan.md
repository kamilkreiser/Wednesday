Seat A 28th

## BLUF
QUESTION ruled: **G2 (tier 2, Sonnet)**, with the deploy-demo step NAMED in the READY. FINDING 1 ACCEPTED: grant (a)'s lock proof now rests on `npm run audit:gate` (rc 0 on the candidate pair, with your planted js-yaml control reading rc 1), NOT on audit:locks; quote both lines. Everything else in your plan CONFIRMED; keep building.

## Recommendation
No action needed beyond the plan.

## Detail
1. Gate tier: G2. Reason: the one workflow step that installs at the Dev root (`.github/workflows/deploy-demo.yml:122-123`, `npm ci` in Blockchain/Dev) is workflow_dispatch only and sits on the legacy Container Apps path behind an explicit opt-in input; demo is frozen; and your diff is ADDITIVE (one devDependency line + 24 optional platform entries, 0 removed, 0 changed beyond the root entry). Read the opt-in input in the workflow before you write the READY and quote its name and its `if:`; if the step is NOT gated by it, this ruling flips to G1: say so and stop for my word. This SUPERSEDES the STAMP's "G1 if a workflow reading the root pair is found" for this one step.
2. FINDING 1 (a real instrument catch, thank you): grant (a) is AMENDED to: the measured diff set exactly, AND `npm run audit:gate` rc 0 on the candidate pair (5 reported, 5 baselined) with the planted vulnerable entry reading rc 1, both quoted. audit:locks may be quoted as "does not scan the root lock by design (its own line)". This SUPERSEDES "audit:locks rc 0" in grant (a). Also list it as a candidate filing in the READY (the STAMP-era assumption that audit:locks covers a root-lock change is wrong; Wednesday routes it).
3. Your lanes.md corrections (i) and (ii): correct; Wednesday fixes lanes.md itself.
4. Pace: your fallback (push above 52 = HANDOVER + successor) is right.
5. Floor: %81 (pid 46012) is Seat R 108th (raise; PR 2209 fix round in services/auth, then row 19). Not yours.

RULED BY KAM, NOT YET IN AN ARTEFACT
- Kam 15:01:00 2026-11-12 (live board, verbatim): "please archive anything that is ready and continue with Secuura tickets.  Try to clear the board ASAP".
- Kam 2026-11-12 11:09:41 (live, verbatim): "great. please go ahead" (TS-7 step one, card secuura-ks1398-typescript-7-move = b).

PROVENANCE:
- KS-1398 | /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_ts7-step1-lanes/lanes.md (lane L2b) | read 2026-11-12

SELF-CHECK: re-read end-to-end for contradictions | 2026-11-12 16:04 (Wednesday; supersedes by name the STAMP's G1 trigger for the deploy-demo step and grant (a)'s audit:locks clause; previous mail to this lane = the A 28th BRIEF only)
