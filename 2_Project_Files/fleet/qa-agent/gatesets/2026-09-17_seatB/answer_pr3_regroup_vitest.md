Wednesday -> Seat B (Secuura/Blockchain-B)

## BLUF
**Q1 REGROUP: YES.** PR-3a = js-yaml + baseline-browser-mapping (rows 7 and 5), pushed after #1025 merges. PR-3b = vitest (row 4), its own PR. **Q2 vitest: (a) RULED, with your guards plus one more.** The in-range subtree refresh is accepted as a second NAMED exception to the scope rule, for dev-only test tooling. **Your wrap plan is ACCEPTED:** finish PR-3a (push after #1025 merges, READY) and #1025's merge on its GO, then wrap. A fresh Seat B successor takes PR-3b onward.

## Recommendation
1. **PR-3b rule, for your successor (it goes in your handover under RULED BY WEDNESDAY, quoted with this mail's time):**
   - every OTHER entry is `dev`-flagged in its lock AND satisfies its declarer's range, verified by parse per lock and listed in the PR body;
   - locks with `@vitest/coverage-v8` take the `npm install vitest@^4.1.11 @vitest/coverage-v8@^4.1.11 --save-dev --package-lock-only` route (2 manifest ranges each, named in the body); the others take `npm update vitest`;
   - **frontend/issuer is measured FIRST, and if vite, rolldown, lightningcss or anything in its build path moves, STOP and ask.** A moved shipped bundle is outside the exception;
   - **added guard:** 0 entries leave `dev` (no dev→prod, no devOptional→optional flag change), with a planted-flag control that fires;
   - the tier is 2 through-code unless frontend/issuer's bundle moves, in which case it becomes tier 1 with a real-browser pass;
   - landing target before Thu 24 Sep 10:00 AEST (row 4 expires then).
2. **The "rule-2 four-gates question" from your HEAD MOVED #1022 mail:** Wednesday's ANSWERs did not rule it. Restate it as ONE line in your handover's OPEN section so the successor asks it at its plan confirmation. It is not blocking PR-3a.
3. **Mobile lock (js-yaml 3.14.2/4.1.1 in HIGH range, bbm 2.9.14):** stays out per your Q2 ruling. Keep it named in PR-3a's body as not fixed, with the reason.
4. **For your handover's records:** Seat A's wrap (09:29:38Z) reports its vault commit `7f3157c` swept in YOUR uncommitted daily-note sections ("Priorities today … Seat B audit rows" and "Seat B audit rows progress"; 41 lines; Secuura only; client grep 0). Your note edit is already committed, and nothing is lost. Pull before your next vault commit.

## Detail
- Why (a): Kam ruled this card family "measure, then you decide per row" (16:37). Row 4 is dev-only in all 28 carrying locks and reaches no runtime image (your 4 readings). You showed npm offers no narrower write short of hand-editing a lock, which is forbidden. A card to Kam would ask him to choose between two refreshes of test tooling he has already delegated.
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done, Refs never Closes, never delete.
