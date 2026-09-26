--- comment 5838941476 by linear[bot] at 2026-09-25T20:15:54Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1319/walktimeouts-guard-the-wiring-pin-passes-on-a-commented-out-line-and">KS-1319 walkTimeouts guard: the wiring pin passes on a commented-out line, and the derivation misses nested and async tree-walkers</a></summary>
<p>

## BLUF

Three non-blocking findings from the tier-2 gate on PR #1254 (KS-1155, merged `ac38dc21dba4`). All three are in the `walkTimeouts` pair added by that PR — one file family, one test pass, one ticket.

**The first two matter more than their Polish severity suggests: they are limits of the thing that keeps the walker list honest**, which is the part of that change doing the real work. The budget itself is cheap; the guard that stops the list going stale is the point.

## The three items

1. **WIRING-PIN-SCRAPE.** The cell that proves `vitest.config.ts` wires the setup file is a **source scrape** — `expect(config).toContain('setupFiles')`. It would pass on a **commented-out** `setupFiles` line. That cell exists precisely because removing the wiring reddened nothing otherwise, so a scrape that a comment satisfies is a thin guard on the one thing nothing else covers.
2. **NESTED / DERIVE-MARKERS.** The derivation reads `src/__tests__/*.test.ts` one level deep and looks for `readdirSync`, `DEV_ROOT` or `WALK_ROOTS`. It therefore does **not** see a tree-walking guard in a **sub-directory**, nor one that walks via **async** `readdir` (or `fs/promises`, or `glob`). Either would get the 5 s default and start flaking under load — the exact state KS-1155 exists to end — while the drift guard stays green.
3. **TS1343** (Polish).

## Done when

- ☐ the wiring check cannot be satisfied by a commented-out line (parse the config, or assert the setup file is actually loaded at runtime)
- ☐ the derivation covers sub-directories and async tree-reading spellings, or names the spellings it deliberately does not cover so the blind spot is stated rather than latent
- ☐ TS1343 resolved or recorded as accepted

## Not in scope here

KS-1155's own `load >= 30` bar stays open on that ticket and is not addressed by any of the above.

## Board search before filing

Literal match over **1,307 issues (includeArchived) and 3,684 comments**: `WIRING-PIN-SCRAPE` -> 1 (KS-1155, this finding's own record) · `DERIVE-MARKERS` -> 1 (same) · `walkTimeouts` -> 1 (same). **Searched those three terms, 0 open hits outside KS-1155 itself.** Controls: `readYaml` -> 10 hits, fires; `qqx7-fresh-control-never-written-anywhere` -> 0.

## Provenance

Tier-2 gate `QA/Secuura-batch1249`, non-blocking (N-1254-a, N-1254-b, N-1254-d), recorded at the merge of #1254.

Refs KS-1155
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1319-the-wiring-check-survives-a-comment-out-the-derivation-misses-c3f692da595a">Review in Linear</a></p>

