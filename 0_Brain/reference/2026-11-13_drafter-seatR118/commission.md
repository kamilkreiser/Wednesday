# Commission: DRAFTER for Seat R 118th (Secuura/Blockchain RAISE/FIX seat, lane -R), 2026-11-13 09:4x AEDT

Commissioned by Wednesday (the 08:0x seat). Read-only drafter: write ONLY the brief path below and files in THIS folder (a clone here is allowed). Nothing raised, pushed, posted, mailed or written to Linear or GitHub.

## Produce
1. `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-13_seatR118_fix.md`
2. `notes.md` here: everything Wednesday must rule or check before stamping.

## Copy-and-change
- Template brief: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-13_seatR117_raise.md` (STAMPED; read WHOLE) and its predecessor chain by pointer. R 117th's record: `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-13_seatR-117th/HANDOVER.md` (FINAL block whole).
- THE DEFECT: gate 348's verdict `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-13_gate348-tier1-pr2224-2225/verdict.md` (read WHOLE; G348-2225-1 at line 45 is the subject).

## Wednesday's ruling (the work)
- **This is a CLAUDE BUILD row (no held Spark patch), TIER 1:** in services/originate, the POST /api/certifications/:id/verify handler (`src/routes/certifications.ts` ~1247-1310 at develop 1ebc3eae6cf4) must apply the KS-1695 reader check (`callerMayReadCertification`, the one `GET /:id` applies) BEFORE `createChargeEvent('verification', …)`, so a same-tenant non-owner is refused (cloaked as GET /:id does) and no charge event is written for a refused call. Red-first cells: non-owner refused + NO charge event written; owner admitted + one charge event; controls. Read how GET /:id applies the check and copy its shape; do not invent a new rule.
- PR 2225 (KS-1855 half two) is HELD until this fix merges first; PR 2224 is not this seat's. The ticket: a board search FIRST (symbol callerMayReadCertification, path certifications.ts, 'charge event' + verify); if none tracks it, the brief has the seat file ONE ticket (Refs KS-1855, KS-1695; assigned to the board account, never Peter/Stuart) before its branch.
- G348-2225-2 (two stale comments: api-gateway index.ts:426-433 and routes/verification.ts:453) are NOT in this PR (they are on 2225's side); list them for the board seat.
- Also measure for the brief: every other originate route in certifications.ts that writes a charge event or returns a certification without callerMayReadCertification (a census with a positive control); list them as findings, do NOT widen the row.

## Must-checks for notes.md
- Floor: %189 Seat B 170th (MERGE, queue 2141 first; its 46 paths are listed in its brief `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-13_seatB170_merge.md` BLUF 5): confirm no queued path is services/originate/src/routes/certifications.ts (PR files API).
- The exact develop sha at your read; the lines of the handler and of GET /:id's check, quoted.

Model: Sonnet. Return a 10-line summary.
