# ANSWER (Seat B 42nd): both design calls CONFIRMED as SHAPES; push ITEM 1, open the PR, READY FOR QA; ITEMS 2-3 handed over whole

## BLUF
**Push.** Both calls are confirmed as shapes that follow from Kam's own words, not new authority. Whether the code does them is the gate's question, not Wednesday's.
1. **Sticky revoke both ways ("revoked if EITHER the cache or the store says revoked"): CONFIRMED.** It is the intersection of two Kam rulings: KS-1370 (a) "A revoked key is never honoured" and `secuura-ks888-revoke-validate-on-failed-save` (a) "keep in-memory revoke". Refreshing blindly from the store would have undone the second; your R2 catch is exactly right, and fixing the code rather than the test was the right call.
2. **Vanished row → `Key not found`, cache entry evicted: CONFIRMED** as a defensive path (your grep: no live DELETE outside migration 019). Name it as defensive in the PR body.

## Then
- Open the PR (`Refs KS-1370`, no closing keyword) with your Test Evidence, **quoting both rulings and naming both calls as Wednesday-confirmed shapes**; post the facts-only KS-1370 comment (Kam's (a) on both cards, and the two confirmed calls) in the same turn.
- READY FOR QA for gate40. **Carry into your READY, for the gate:** RLS is NOT exercised by your drill (superuser, `rolbypassrls=t`), so the gate must drive the stored read as a NON-superuser app role. Also name the `usage_count` lost-update as a candidate.
- **ITEMS 2 and 3 are UNRAISED and handed over whole** to your successor, as you said. Write them into your handover by item number with the brief's path.
- Then hold for gate40, or wrap cold at your budget line with the handover current; the GO can go to a successor.
