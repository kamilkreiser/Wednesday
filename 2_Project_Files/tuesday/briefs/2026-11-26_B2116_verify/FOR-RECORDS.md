# FOR RECORDS: lane L2 round 1 of 2 of the MPS Commercial Calculator (kit B2111, seat M177), MPSCALC-135 and 297, head 184eff58 (gate B2116: GO WITH FINDINGS)

For the records lane only, AFTER a landing of this gated head (its squash on main); nothing here is written into a
project file by the gate. Who decided every choice of this lane: the coordinator (Tuesday), as coordinator. The product
owner's words are only the 2026-11-11 records notes the kit quotes (RELAYED from the kit's THE AUTHORITY; the gate did
not re-read the tickets or CLARIFICATIONS.md).

## MPSCALC-135 (Done-when of comment 40941, read with comment 41135)
1. Measure why the dialog stays and the picker times out: MET before this lane (41135).
2. Fix those reds: MET on the stub leg (heldRentalFlow.ts; the gate re-ran leg B: 3 of 3 default, 1 of 1 at 390). On the
   no-API leg NOT fixed to green: nothing can answer the journey, so the spec skips itself with its reason
   (`smoke.spec.ts:25-28`). The picker timeout did not reproduce at base (the seat); leg A's red was the 5 versus 4 row
   count from the short proposal's cap (MPSCALC-110).
3. Press Short-form before the Proposal checks: MET (`smoke.spec.ts:79`, from the landing of #178).
4. Green in all four legs, **read as the coordinator's Q3 reads it: green where an API or the stub answers the
   journey (A default, A at 390, B; A at 1440 is the builder's, RELAYED; the gate re-ran A default x3, A 390 x1, B default x3, B 390 x1), and
   skipped with its reason where neither does (C; the gate re-ran it: 1 skipped, the reason line printed).** The
   ticket's Linux legs are UNMEASURED until the pull request's hosted run (the web job's two Playwright steps). The
   ticket stays open for the product owner's reading of its own wording (Q3 is the coordinator's, not his).

## MPSCALC-297
1. Exact-nav spec green at 1440 and 390 px: MET with no edit (the seat: `b46-home.spec.ts` 15 passed in stub mode, 15
   skipped with the stub off, by its own rule; RELAYED, the gate did not re-run it).
2. smoke.spec.ts green at desktop and phone width: MET by hand on A (default, 1440, 390) and B (default, 390); the gate
   re-ran A default, A 390, B default and B 390. In CI the stub step runs it once, at the config's default viewport; no
   CI run at phone width, and C skips.

## Owed lines (the kit's FACT 7)
- (1) The smoke journey on an API was red at `smoke.spec.ts:78` from 2026-11-12 (the short proposal's cap of MPS #189,
  `RENTAL_SHORT_LINE_CAP = 3`) and nobody saw it, because CI left the spec out; the fix is the spec's literal.
- (2) After the landing and merge, MPSCALC-135 clause 4 reads as Q3 says and MPSCALC-297 clause 2 reads MET on legs A and B.
- (3) The two stub fidelity follow-ups of the landing of MPS #193 stay owed (BACKLOG rows `[B1574-OWED-1]` and
  `[B1574-OWED-2]`); the half-stale smoke reason in the config is corrected by this lane.
- (4) Leg A (an API on a synthetic store) has no CI step: a hand-run leg (the recipe is the kit's).

## The gate's findings for the records (none edited by this lane)
- **'reject' (the seat's finding, CONFIRMED by the gate, Minor):** in stub mode a Submitted held rental quote offers an
  Approver `['approve', 'reject']` (`heldRentalFlow.ts` `heldRentalPermissions`), but the stub answers no `reject`; the
  call goes to the real API (the gate's probe: `real.reject` called once; with no API the proxy answers 502).
  `newVersion` and `getSnapshot` likewise have no stub answer (DERIVED from `client.ts:76-80`, not run); after Approved
  the permissions are empty, so no button offers them. Dev stub only.
- **Stub role gap (Minor, gate finding F2):** the stub's calculate and submit check no role (the gate's probe: an
  Approver persona's calculate answered `Succeeded`; an analyst persona's submit answered `Submitted`); approve does.
- **Skip scope (Minor, F1):** the stub-off skip covers any 502, 503 or 504 from `/api/v1/quotes`, including a live API
  that fails that way (the gate's probe: a loopback server answering 503 gave `1 skipped`, rc 0; one answering 500 gave
  `1 failed`); a hand-run leg A against such an API reads as a skip, not red.
- **Console allowance (Minor, F4):** one `Bad Gateway` console message from any resource is allowed in stub mode, not only
  the stub create's.
- **MPSCALC-195's drop** (the product owner's 2026-11-26 09:14 ruling, 'Decision datasec-mps-195-engine-sentence-1126: b
  - Drop it') is also owed to this records pass (Tuesday's records kit): this lane does not touch it.
- UNMEASURED: hosted Linux legs; `npm audit`; whether the builder's `npm ci` or dotnet restore contacted a registry.
