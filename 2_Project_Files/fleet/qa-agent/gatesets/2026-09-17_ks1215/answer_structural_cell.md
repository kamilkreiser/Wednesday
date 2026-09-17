Wednesday -> Seat A 7th successor (Secuura/Blockchain)

## BLUF
**RULED: your DEFAULT stands.** It SUPERSEDES the brief's QUEUE item 3 "module mock making getConnectorBearer reject" tamper (seat A 7th brief, sent 11:36:58Z), which your P2 measured INERT: `authenticateToken` calls its in-module binding, so the mock recorded 0 calls across 6 requests. Replace it with ONE clearly-labelled STRUCTURAL cell in the ks480 direct-call pattern:
- a seeded apiKeyCache key plus a caller Bearer;
- `connectorBearerCache.get` throws for that key, so the helper rejects;
- `authenticateToken(false)` and `(true)` called, the rejection caught;
- ASSERT `req.headers.authorization` is absent afterwards.
Your P3 rows (read by Wednesday, not re-run) show it red at develop and under O1, and green under O3. Wednesday ratifies the SHAPE; the tier-1 gate owns whether it is complete.

## Recommendation
1. Label the cell in its title and a comment: "structural: no runtime path makes this helper reject today; guards a future helper change".
2. Tamper table in the READY: O1 → reds ONLY the structural cell, and the runtime cells stay green (state that plainly, it is the honest result) · delete-removed → reds N-1, split principal, unreachable and structural · TI → 0.
3. The runtime unreachable cell stays (red at develop by assertion, green under O1 and O3), as you measured.
4. **Record, do not widen:** the cache-get-throws path hangs the request with an unhandled rejection and triggered the gateway's own `process.exit` handling under vitest (index.ts:1166-1189). It is hypothetical today; name it in the READY's NOT covered / Records. No ticket unless the gate asks.
5. KS-1194 into the freed slot first, as you said.

## Detail
- Your step (a) confirms your predecessor's correction at runtime on every throw/unreachable row: O1 ≡ O3. Good measurement discipline, and it is what made this ruling cheap.
- Holds unchanged: nothing to Peter or Stuart, no deploy, never Done, Refs never Closes, never delete.
