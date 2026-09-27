--- comment 5854677097 by linear[bot] at 2026-09-27T09:33:02Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1212/ks1187-tests-no-cell-pins-that-the-erasure-door-reads-its-own-routers">KS-1212 ks1187 tests: no cell pins that the erasure door reads its own router's caseSensitive option (door vs factory router)</a></summary>
<p>

## BLUF

**No test pins that the gdpr erasure door reads its OWN router's** `caseSensitive` **option.** The door's case rule comes from the `erasureDoor` router's options, and the F-1019-2 cell added in #1019 checks that the rule is read from a router option. But both the door router and the proxy factory's router are default-constructed today (case-insensitive), so a change that read the WRONG router's option would still pass. The tier-1 round-2 gate on #1019 measured this: its tamper G-READOUTER, which reads the other router's option, left **0** failing cells at `82f09c8bd`. It is latent (both routers agree today) and test-only.

## Recommendation

Add one test-only cell pair. Mount the door on a **case-sensitive** router while the factory router stays default, and assert the door's case rule follows the door router. Then add the inverse: factory router case-sensitive, door router default. Both cells must go red under G-READOUTER. No product change. This is a local-model candidate; it is not being built by Seat A.

## Detail

* **The property:** `erasureDoorVerdict` compares the canonical path using the door router's own `caseSensitive` option. If the two routers ever differ, the door must follow its own router, not the factory's.
* **The gate's measurement:** report `/Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-17-ks1187-1019r2-82f09c8bd-tier1-r2/report.md`. Line 117 is the G-READOUTER row (0 reds: "cannot see WHICH router — both erasureDoor and the factory router are default-constructed"). Line 186 is the drafter's replicate (0). Line 194 lists G-READOUTER among the controls that cannot see.
* **Where:** the gdpr erasure door in the api-gateway proxy routes. The existing F-1019-2 cell is in `services/api-gateway/src/__tests__/ks1187-erasure-door-judges-the-canonical-path.test.ts`. It uses a bare app where every factory Router is case-sensitive at once, which is why it cannot separate the two routers.
* **Merged state:** #1019 squashed as `581c9db0d` on develop. The related ticket stays In Progress under §5f, so it cannot carry this record, and the local model's builder needs a ticket for it.
* **Searched first** (Linear, literal matches in titles, descriptions and comments, archived included):
  * `caseSensitive`: 0 fuzzy results to scan, 0 hits;
  * `erasureDoorVerdict`: 0 fuzzy results, 0 hits;
  * `F-1019-2`: 118 scanned, 1 hit (the related ticket's own comments);
  * `KS-1187`: 1 scanned (the ticket itself), 0 literal hits in text.
  * Linear's fuzzy search returned nothing to scan for the two code identifiers, so those zeros say little. No existing ticket was found for this record.
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1212-pin-that-the-erasure-door-reads-its-own-routers-casesensitive-ab4e56ea1f64">Review in Linear</a></p>

