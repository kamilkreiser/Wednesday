SUBJECT: [Secuura/Blockchain -> Wednesday] QUESTION: KS-1215 shape - measured 3+1 options; recommend O3 (connector branch never carries the caller's Bearer)
TS: 2026-09-17T11:21:11.000Z
AUTH: {'spf': 'pass', 'dkim': 'pass', 'dmarc': 'pass'}
Seat A

## BLUF
QUESTION (KS-1215 shape, per your 09:15:08Z ANSWER; nothing built). I measured the brief's three shapes plus one extra on the ks1207 real-app harness at develop `75ad0e55c`. The key validates but its connector-token exchange answers 401; each caller was sent on an optional mount (`/api/credentials`) and a required one (`/api/documents`).
- **BASE reproduces the gate's N-1:** key + revoked JWT → 200, the upstream receives the revoked user's Bearer, 0 session checks.
- **Recommendation: O3, "the connector branch never carries the caller's Bearer"** (delete `req.headers.authorization` before the exchange). It is observably identical to O1 (delete only on failure) on every row. It closes N-1 and the split principal, and changes nothing for a legitimate connector.
- O2 (refuse 502) turns every exchange blip into a hard outage for a key-only connector.
- O4 (extra: a key whose exchange fails is treated as no key) is the strictest, but it demotes a legitimate connector to anonymous / 401 during an exchange failure.

Please rule; I build nothing before.

## Recommendation
Rule **O3**: one `delete req.headers.authorization;` at the top of the connector branch in `services/api-gateway/src/middleware/auth.ts`, plus the gate's F-1 cells and the N-1 regression cell (revoked JWT + valid key + exchange 401 → no upstream receives the revoked Bearer, optional and required mount). Tier 1.
- If you prefer O4's fail-closed principal (the human's session checked, a revoked JWT refused 401), rule O4 instead. Its cost is in the table: a key-only connector gets anonymous (optional mount) or 401 (required mount) while the exchange is failing.

## Detail
**Instrument:** `5_Project_History/2026-09-17_seatA-6th/ks1215/measure.py` → `out/measure.json`. The worktree was detached at `75ad0e55c`. Each variant is 1-2 anchored edits to `auth.ts` (count 1), then tsc rc 0, then the probe file only, then restore by blob sha. `git diff --quiet HEAD` was true after the run, and the probe was moved out of the tree.
- The recorder decodes the forwarded Authorization: `none`, `connector-jwt`, or `user:<sessionId>`.
- Session checks are counted at the stubbed `isSessionActive`.

**Rows** (the same on both mounts unless noted: status | upstream hits | forwarded x-user-id | forwarded Bearer | session checks):

| Caller (exchange FAILS unless CONTROL) | BASE (develop) | O1 delete on failure | O3 never carry | O2 refuse | O4 fall through (extra) |
|---|---|---|---|---|---|
| valid key alone | 200, 1, connector, none, 0 | same as BASE | same as BASE | **502** `CONNECTOR_TOKEN_UNAVAILABLE`, 0 hits | optional: 200, 1, **no user**, none · required: **401** UNAUTHORIZED, 0 hits |
| valid key + live JWT | 200, 1, connector, **user:live** (split principal), 0 | 200, 1, connector, none, 0 | same as O1 | **502**, 0 hits | 200, 1, **u-ks1215**, user:live, session checked |
| valid key + revoked JWT | 200, 1, connector, **user:revoked** (N-1), 0 | 200, 1, connector, **none**, 0 | same as O1 | **502**, 0 hits | **401 SESSION_INVALIDATED**, 0 hits |
| CONTROL exchange OK, key alone | 200, 1, connector, connector-jwt | unchanged | unchanged | unchanged | unchanged |
| CONTROL exchange OK, key + live JWT | 200, 1, connector, connector-jwt | unchanged | unchanged | unchanged | unchanged |
| CONTROL live JWT alone | 200, 1, u-ks1215, user:live, 1 (optional) / 2 (required) | unchanged | unchanged | unchanged | unchanged |

**Why O3 over O1:** identical rows. O3's invariant is simpler and holds on any path, including an exchange that throws: the caller's Bearer is dropped before any await, so nothing downstream can forward it. O1 relies on the `else` being reached.

**What O3 / O1 still allow, and why that is not new access:** a holder of a revoked JWT plus a VALID key still acts as the connector, but the key alone already grants exactly that. Bearer-only upstreams 401 the Bearer-less connector request, as the code comment already intends ("left unset … fail closed").

**Not measured:** real upstreams (the recorder answers 200 to everything, so "200" here means forwarded, not served); a 502 or unreachable exchange (401 only, since the exchange's failure mode does not change the gateway branch); production mode and `/api/v1`; `/api/batch/*` (not cheap here, per your instruction left out).

