--- comment 5865708501 by linear[bot] at 2026-09-28T07:48:50Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1227/ks1072-posttier2s-anchor-store-witness-counts-every-stub-request-leaks">KS-1227 ks1072 postTier2's anchor-store witness counts every stub request, leaks its listener on a status red, and no cell pins a hit-only URL filter</a></summary>
<p>

## BLUF

**Test-only, a tidy-up of one helper.** The anchor-store witness that PR #1029 added to `postTier2` in `services/api-gateway/src/__tests__/ks1072-the-latest-anchor-selector-documents-a.test.ts` (merged as `27e53ec3a`) works: the tier-2 gate measured that it discriminates. It has three loose ends, all measured or read by that gate (records R-1029-2, R-1029-3, R-1029-4):

1. it counts EVERY request the stub anchor store receives, not only reads of this document;
2. a status red leaves its request listener attached;
3. a URL filter that kept only hits would red nothing, because no cell pins it.
   None affects a result today. **A candidate for the local model.**

## Recommendation

In `postTier2` (`:113-128` at `27e53ec3a`):

* **Detach in a** `try/finally` around the verify call and its status / body reads, as the KS-1180 control (`:133-140`) already does by detaching before it asserts.
* **Decide the counting rule on purpose.** Either keep "every stub request" (fails closed) and say so in the comment, or filter by this document's path. If you filter, pin the filter with a cell whose verify makes a second, non-hit request reach the stub, so a hit-only filter reds.
* Optional, tied to finding P-1029-1: the assertion message at `:128` says "tier 2 answered". The witness proves tier 2 was ASKED once. The open tier-1 half of KS-1180 (a stub originate that answers plus a 0-read cell) is what closes that gap; reword the message or leave it for that change.
  Regression proof: the gate's Q-D4-LEAK probe (a status red leaves `listenerCount('request')` at 2) must read 1 after the change.

## Detail

* **R-1029-2** (MEASURED, D-ENV-LIVE: 5 WITNESS reds while tier 2 answered): the listener pushes every URL, so a second call reaching this stub would red a correct tier-2 answer. Unreachable today: the ks1072 file never sets `ANCHORING_SERVICE_URL`, the two files that do (`ks864a…`, `ks1195…`) point elsewhere, and vitest isolates files. Fails closed.
* **R-1029-3** (MEASURED, Q-D4-LEAK / Q-D4-NOLEAK): on a status red, `anchorServer.off('request', …)` at `:125` is never reached, so one listener stays attached (count 2 at the last cell). It pushes into a dead array, and every later cell stays green. Harmless, but inconsistent with the control cell.
* **R-1029-4** (MEASURED for each listener, READ ONLY for the filter): Q-DEAF-HIT (5 WITNESS) and D-DEAF-MISS (1 CONTROL) show each listener is load-bearing. But every `postTier2` cell is a hit, so a filter keeping only `/api/anchors/document/doc-ks1072` would red nothing and would also mask R-1029-2.
* **Source:** the tier-2 gate report on #1029 at `cd3580e1f` (GO WITH FINDINGS, verdict 2026-09-17 12:42Z), §FINDINGS.
* **Searched before filing** (Linear, literal matches in titles, descriptions and comments, archived included):
  * `ks1072-the-latest-anchor-selector`: 3 hits. KS-1072 (the selector itself), KS-1199 (a tie-verdict gap in the same file, a different cell), and KS-1180 (this helper's parent).
  * `postTier2`, `anchorServer`, `listenerCount`: 0 hits each (the same search found the file name, so the instrument can match).
  * No ticket covers this tidy-up.
* Refs KS-1180 (stays In Progress: its tier-1 half and the P-1005 items remain open).
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1227-keep-the-count-every-stub-request-rule-and-say-so-beside-the-ba0b5f4e533f">Review in Linear</a></p>

