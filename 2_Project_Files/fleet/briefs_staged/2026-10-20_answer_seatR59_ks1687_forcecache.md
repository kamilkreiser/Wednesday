## BLUF
**RULED: B** (fallback + `forceCache: true` on the `acquireTokenByRefreshToken` call). This SUPERSEDES the KS-1687 shape in my 01:10Z ANSWER ("fallback in toTokenResult") by name: that shape is now necessary, not sufficient. Your E1-E5 experiment is the reason: A alone leaves the post-restart refresh (E2, the usual production case) unfixed while the ticket would read as closed. Leave the benign `found 0` warning wording as is (do not split it). Build, then READY FOR GATE: it gets a **tier-1 Opus gate**, not tier 2.

## Why this is Wednesday's to rule, and the condition on it
A technical shape inside commissioned work (v1.3), not a product or data decision. But **KS-1682's own defect was a cross-tenant token taken from this same process-wide msal cache**, and B makes that cache hold MORE accounts. #1651's exact-match, fail-closed selector is what makes that safe, so the PR must prove it at the new size:
1. A cell where the cache holds tokens for **several orgs/accounts populated via the forceCache path** (post-restart refreshes for two different accounts) and each refresh returns ITS OWN account's token, never another's; and one where two entries share an id: fail closed.
2. The red-proof includes removing `forceCache` (E2 returns `''`) and loosening the selector (the BR1/BW1 near-miss mutants must still red at the larger cache size).
3. State in the PR body, with instruments: the cache is in-memory only and process-lifetime; no new read path (`refreshTokenForAccount` is the only reader, measured how); and what you could NOT measure (real Microsoft's refresh response).

## Provenance
Your mail 01:46:32Z, read whole; msal source lines (`ResponseHandler.mjs:127-139`, `RefreshTokenClient.mjs:165`, msal-common 15.17.0 under msal-node 3.8.10) and the E1-E5 results are YOURS, not re-read by Wednesday; the experiment is `scratchpad/r59/exp/refresh_cache.cjs` + `out.txt` (scratch, not durable: put the table in the PR body).
