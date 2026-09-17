Wednesday -> Seat A (Secuura/Blockchain)

## BLUF
**RULED: O3, "the connector branch never carries the caller's Bearer".** It is one `delete req.headers.authorization;` at the top of the connector branch in `services/api-gateway/src/middleware/auth.ts`, before any await. Wednesday ratifies the SHAPE on your measured table (read, not re-run): it closes N-1 and the split principal, and it leaves a legitimate connector's rows unchanged. O2 turns an exchange blip into an outage. O4 demotes a legitimate connector to anonymous/401 during an exchange failure. That is a partner-facing behaviour change, the same reason KS-1207's option A was declined. **Whether O3 is complete and correct at runtime is the tier-1 gate's question, not Wednesday's.** Build it locally now; it pushes when a slot frees (the cap is full: #1028, #1029, #1031).

## Recommendation
1. Build O3 with these cells, each red at develop 75ad0e55c BY ASSERTION, on BOTH an optional mount (`/api/credentials`) and a required one (`/api/documents`):
   - N-1 regression: valid key + REVOKED JWT + exchange 401 → no upstream receives the revoked user's Bearer.
   - split principal: valid key + LIVE JWT + exchange 401 → the forwarded Authorization is not the user's.
   - **exchange THROWS / unreachable** (your table did not measure this; your case for O3 over O1 rests on it): no upstream receives the caller's Bearer.
   - controls: exchange OK (key alone and key + live JWT) → connector-jwt forwarded, unchanged; live JWT alone → unchanged.
2. Tampers: O1 (delete only on failure) must RED the throws cell (that is what makes O3 distinguishable); the delete removed must RED N-1; TI inert.
3. One row in production mode on `/api/v1`, stated as such. `/api/batch/*`: list under NOT covered, as you said.
4. READY tier 1, `Refs KS-1215`; name this ruling (this mail) and the residual you already stated (a revoked-JWT holder with a VALID key acts as the connector, which the key alone already grants).

## Detail
- The order in the queue is unchanged: this build waits locally; KS-1194 merges only on Kam's tap.
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done, Refs never Closes, never delete.
