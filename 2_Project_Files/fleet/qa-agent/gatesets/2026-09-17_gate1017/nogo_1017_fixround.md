Wednesday -> Seat A (Secuura/Blockchain)

## BLUF
**NO GO on #1017 KS-1195 @cbe29597d** (tier-1 gate verdict 23:31:00Z from coagent@, spf/dkim/dmarc pass; report `Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1195-1017-cbe29597d-tier1-r1/report.md`). **This fix round is ROUND 2 of 2 under the cap:** if round 2 is also NO GO, the closed instances ship and the residue is ticketed.
The NO GO rests on **F-1 (Major, NEW, made live by #1017):** the "per-key" limiter buckets by `connectorId || userId`. A key whose validate response has no connectorId gets the literal userId `connector:api-key`, so every such key shares ONE bucket across ALL tenants. The gate measured it on the real app: tenant X's key 200, 200, then tenant Y's key's FIRST request 429. **Wednesday re-read the three source lines itself (read-only `git show`):** `rateLimitEnforce.ts:108` at cbe29597d (`const clientId = user.connectorId || user.userId || 'unknown'`) · `auth.ts:280` at cbe29597d (``userId: `connector:${meta.connectorId || 'api-key'}` ``) · `originate/src/routes/adminConfig.ts` at develop fa887f382, whose `INSERT INTO svc_api_keys` column list has no `connector_id`. So every admin-minted key platform-wide shares 1000 requests per hour. The bucket code is older than #1017; #1017 is what makes it fire. Everything else in the delta reads GO WITH FINDINGS.
**This AMENDS Wednesday's 07:5x KS-1195 shape answer (`answer_shape_census.md`, items A1-A4): it adds A5, bucket identity.** A1-A4 stand as answered by the gate.

## Recommendation
1. **A5, the fix (same PR, new head):** the limiter's bucket for a machine caller must be that CALLER'S OWN identity, never a value two tenants' keys can share. The oracle is KS-164's wording, "a key configured at N/min lets N through", so it is per KEY. **Proposal, not a ruling on your code:** bucket `api_key` principals by the key's own id and `oauth_app` principals by the app's client id. First read what the validate response actually carries (auth.ts:231 region; the security service's validate handler). If no key id reaches the gateway, say so and propose the smallest honest source, rather than hashing something that is not unique. State in the READY how a keyless-connector key and a connector key are each bucketed.
2. **Cells, on the REAL app (the gate's instrument shape):**
   (a) two keys with NO connectorId in two tenants → independent buckets;
   (b) two keys under the SAME connectorId → independent (per key);
   (c) an admin-mint-shaped key (no connector_id, 1000/3600) counts only against itself.
   Red-proof each against the round-1 head, where they must go red. Add a tamper row **G-BUCKET** (restore `connectorId || userId`) and carry project tsc rc per row.
3. **F-2 (Minor, SHIPS-WITH):** one real-app count-once cell on a real double-authenticated chain (POST /api/gdpr/erasures is the gate's), red under G-ERASE. Today the guard is pinned only by a bare-app cell.
4. **Tickets. Search first and quote the searches. Ours, Backlog, related KS-1195, NOT linked to #1017. File them after the READY, not before:**
   (i) **ONE limiter follow-up ticket** (one test pass proves it): F-3 (no cell sees G-OAUTH / G-UNKOPT / G-JWTCATCH) · F-4 (`next()` inside the limiter's try: a sync throw is counted and dispatched twice; the JWT branch becomes an unhandled rejection, which under production's default `UNHANDLED_REJECTION_MODE=exit` calls gracefulShutdown; unreachable through Express 4 by READ) · F-5 (refused mutations still write audit rows; a refused uncached key still costs validate + exchange) · R-2 (an unthrottled "has no rateLimit" warn).
   (ii) **R-1, originate:** the admin key mint writes no `connector_id` and an UNCLAMPED `rate_limit = d.rateLimit || 1000`, so -1 is reachable by an admin and means 429 forever.
   (iii) **R-4, security:** an unknown `sk_` key passes optional auth on `/api/credentials*` and `/api/referrals/:sub` (base = head). Measure before choosing a priority, and state the measurement on the ticket.
   R-3 (the test token carries no tenant) and R-5 (an instrument artefact) are records only.
5. **KS-1195: ONE facts comment** carrying F-1 and the extended deploy precondition: F-1 fixed and gated before any deploy, plus the existing unmeasured allowances and traffic rates. KS-1195 stays In Progress on merge (§5f). Nothing to Peter or Stuart.
6. **On the new head:** a READY FOR QA naming ROUND 2 (tier 1), with the A5 bucket statement, cells (a)-(c) + F-2's cell, and the tamper table including G-BUCKET and G-ERASE.

## Detail
- **Gate slips it recorded:** the drafter's "keyless keys and A4 edges are hand-edited / pre-backfill only" was wrong, because the admin mint writes both today. Wednesday's and the drafter's optional-auth list missed `admin.ts:1455` and `:1483`. Your TW 1 → 6 was already self-reported.
- **NOT TESTED by the gate:** the count of real keys without a connector_id (needs an authorised read-only DB query per environment), real Redis, multi-replica counting, the deployed gateway. A per-key bucket makes the first of these irrelevant to the fix.
- **Holds unchanged:** 3 of 3 open PRs. #1018 and #1019 heads stay unmoved (the #1019 gate is being drafted). No deploy, no `.github/workflows`, no local stack, Kam's 40% cap. If your context passes 80% mid-round, write the handover with this mail's items and their state, then wrap.
