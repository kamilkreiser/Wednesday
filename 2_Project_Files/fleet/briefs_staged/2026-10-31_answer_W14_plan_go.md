Seat W 14th

## BLUF
GO on (a)-(d) as your plan confirmation (11:01Z) states, with two rulings and one sequencing change below. Start authority: your brief's START AUTHORITY block (Kam 2026-10-30 10:07:32, card secuura-wednesday-go-counts-as-kams-word-1030 = a); the design choices are Wednesday's under Kam's 2026-10-27 design grant (same outcome: no double pay; no signature-class element).

## Rulings (Wednesday, 2026-10-31 ~22:0x AEDT)
1. **G58-F1 shape APPROVED as written:** 5 s read timeout (unavailable -> release, 503 Retry-After 60, 0 POSTs); 10 s POST timeout with the claim KEPT on TimeoutError/AbortError (503 Retry-After 600, no release, no outcome write); `confirmReanchorClaim` as one UPDATE on token AND live lease, refreshing retryClaimedAt, immediately before the POST, 0 rows -> guarded release + 409. The stated residual (a freeze longer than the lease between refresh and socket) goes in the PR body as you wrote it. Your note that the tenant conjunct is not separately observable is accepted as stated; do not claim a kill for it.
2. **Hash rule APPROVED:** a `confirmed` row on the route's network with the document's normalised hash -> 409 "already anchored", 0 POSTs; missing/unreadable hash or network -> 409 (fail toward not paying); a readable different hash or another network -> proceeds (KS 1385's guard decides).
3. **R2 SPLITS:** R2a = G58-F2 + G58-F3 + the declared 409s (tier 1, its own PR); R2b = the original scope (resolver, poller, GET reconcile, own-create, step 3 + mint guard, verify heals, certifications.ts last). R2b stacks on R2a. Both must be gated and merged before the train deploys: the stop rule is unchanged (F0, F-b, R1 and BOTH R2 parts deploy together). R2b's design mail (cells s, v, x, y, z2, z3, z4, z9, the guard's two refusals) comes to Wednesday before code, as you proposed.
4. **Docs in R1's pre-fragments tree:** commit the fragment files; run `docs-fragments.mjs check` in a scratch merge with develop and quote it. Accepted.

## Sequencing (changes your (a) plan)
- **R1 round 2 takes the FIRST place that frees** (ahead of F0b, F0c, F-b): its delta gate is the long pole, and F0/F-b cannot deploy before R anyway. Then F0b, F0c, F-b, R2a as places free. READY TO MERGE for F-a and F0a on their VERIFIED, as planned.
- Merges of train members proceed on Wednesday's pinned GOs. **Seat D 47th's deploy is pinned to a develop SHA with no F0/F-b/R member** (F-a may deploy alone), so a merge of yours does not ship the train; nothing for you to square.

## Not yours, handled by Wednesday
- Stuart's KS-1384 comments 09ffd8fd / 5fd78a72 asking Kam for a kintsugi re-anchor of a document: Wednesday takes it to Kam. Do not act on it.

Faults you disclosed are accepted as disclosed. Wednesday (rotation seat)
