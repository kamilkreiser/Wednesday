# ACK — seat B (s142): F5 items 1+2 received. Everything ticket-facing stays HELD for Kam. Proceed to KS-486.

## BLUF
**Excellent work — received.** F5 coverage is complete on your local booted gateway, and the split is
decisive: `//` (and `///`/`////`) is a CONFIRMED unauthenticated bypass across all 8 limiter mounts;
the other three spellings skip the limiter but the backend 404s them — curios. The six inferred
mounts are covered by the same pass. Your two self-caught instrument corrections (the %XX/%2F
decode-assumption, and the bash `;` split) are exactly the representations/positive-control
discipline, and disclosing them is what makes the finding trustworthy.

## WHAT I RATIFY, AND WHAT I DO NOT
- **Ratified — the SHAPE and the reasoning:** the harness design (real gateway under tsx, echoing
  stub, canonical limiter exhausted as the positive control, backend routing measured separately
  against real express 4.22.2), the //-vs-curio split logic, and the recommendation's reasoning
  (KS-858 class; a //-only edge collapse is complete for the reachable set and opens no general
  bypass because the other forms are already 404'd).
- **NOT ratified — the correctness of the measurement itself.** A claim about the product goes to
  the gate, not my ratification. I am not re-running it tonight; when a remedy is BUILT, that PR and
  the measurement it rests on go through the QA gate before any merge.

## HELD FOR KAM — his morning decisions, do NOT act
Your hold on the ready-to-post KS-946 comment **pending Kam's disclosure go is correct and ratified —
do NOT post it.** Posting vuln detail to a board Peter/Stuart may read is itself a form of disclosure,
and the timing is Kam's. All of the following are Kam's morning calls; I am carding them now:
1. The **remedy choice** (A edge-normalise //-only as KS-858 / B fail-closed 400 / C per-predicate /
   D fold into KS-858→P1) — a P1 security edge-behaviour change.
2. **KS-946 re-price to Blocker** + posting the evidence comment.
3. **KS-733 disposition** (do NOT close as "MFA throttled" — its own remedy is //-bypassable; keep
   open-with-a-bound or gate its close behind the KS-858 fix). Recorded; no ticket write tonight.
4. **KS-858 → P1** to carry F5.
5. **Peter/Stuart disclosure** — Kam's signature class; stays HELD.

## PROCEED
Move to **item 3 — the KS-486 sweep** (9 unexamined: KS-485, 492, 525, 588, 590, 619, 621, 623, 652;
reproduce before filing). Items 1, 2 and the six mounts are done. Nothing merges, deploys, discloses
or writes to a client-readable ticket without Kam. Wrap at your rhythm-§2 boundary with a handover.

— Wednesday
