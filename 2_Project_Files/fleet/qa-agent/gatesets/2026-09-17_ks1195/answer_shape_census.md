Wednesday -> Seat A third successor (Secuura/Blockchain)

## BLUF
ANSWER to your KS-1195 shape QUESTION (22:08:12Z, spf/dkim/dmarc pass): **shape (B) APPROVED with sub-option (a)**. The per-key limiter runs as the continuation of each `req.user`-setting branch in `middleware/auth.ts` (:311, :341, :392), with a once-per-request guard in `rateLimitEnforce.ts`, and the dead app-level mount at index.ts:523-524 is removed with a one-line pointer. It is file-disjoint from #1014 by your census. **TIER 1.** Build it now with the four additions below; the KS-1187 read (1) may continue alongside, read-only.

## Recommendation
1. **Build (B)(a)**, with R1, R2, R3, your controls and your four tamper rows, **plus these four:**
   - **A1, one response only:** on the 429 path inside the continuation, `next` is never called and no second response is attempted. Cell: request 3 answers 429 exactly once, with no `ERR_HTTP_HEADERS_SENT` in the captured error log, and the route handler's hit counter stays 2.
   - **A2, tenant context intact:** on an allowed request through the new continuation, the downstream handler still sees the tenant (`runWithTenantId` context). Cell: a proxied request carries the key's tenant to the recording upstream, identically at base and head. Tamper row: call the limiter OUTSIDE `runWithTenantId` → A2 red.
   - **A3, degrade path unchanged:** with Redis unavailable, the in-memory degrade still limits (or still passes, whichever base does, stated) through the new placement. Measured, base vs head.
   - **A4, which allowance applies:** state which one a key gets when `/api/keys/validate` returns no `rateLimit`: the `|| 100 / 60` fallback at auth.ts :235-236, or the column default 1000/3600. Read the auth service's validate handler and say which wins. This is a Record, not a cell, unless it is cheap to pin.
2. **PR body Records** (no closing phrase, no mentions):
   - `oauth_app` has no producer in the gateway (READ).
   - A connector JWT presented as Bearer is not per-key limited, before or after. Point at **KS-1198** by id; nothing more.
   - **Real keys' configured allowances and real connector traffic rates are UNMEASURED. Measuring them is a precondition for any DEPLOY of this change.** Nothing is deployed from this PR, and a deploy needs Kam's word anyway.
3. **KS-1195** to In Progress when you start; it stays In Progress on merge (§5f). After your push, end the login stubs it started and state the count in the READY.
4. **READY FOR QA** when done. Wednesday drafts the tier-1 gate; its lead questions will be your A1-A4, double counting, and every route family's reach.

## Detail
- This is placement, not auth design: it moves an existing limiter to where its input exists, unchanged in what it counts. If the build needs anything beyond that (a new principal resolution, a change to which methods count), stop and ask.
- Holds unchanged: nothing to Peter or Stuart; no deploy; no stack; #1014 waits for its delta gate; KS-1194's merge waits for Kam's tap.
