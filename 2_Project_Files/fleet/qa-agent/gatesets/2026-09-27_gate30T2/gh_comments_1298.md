--- comment 5846743687 by linear[bot] at 2026-09-26T13:42:10Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1347/the-urlpathname-percent-encoding-class-also-exists-in-2-blockchaindev">KS-1347 The URL.pathname percent-encoding class also exists in 2 Blockchain/Dev files, outside KS-1337's scope</a></summary>
<p>

## BLUF

The `new URL(..., import.meta.url).pathname` class that KS-1337 fixes in `systemTest/performance` **also exists outside** `systemTest/`**, in two files under** `Blockchain/Dev` — out of KS-1337's stated scope, so it is filed separately. A URL pathname is percent-encoded, so any of these resolving a path from a directory whose name contains a space yields `%20` and an `ERR_MODULE_NOT_FOUND`-class failure. **This fleet has such a directory.**

## The sites (gate29 sweep D, `git grep` over the clone at develop)

* `Blockchain/Dev/scripts/openapi-examples/proxy/server.ts:31`
* `Blockchain/Dev/services/auth/src/__tests__/ks732-mfa-disable-proof.test.ts:293, :296, :316`

**4 lines in 2 files.** KS-1337 fixed 1 of the 3 occurrences inside `systemTest/` (`performance/runner/cli.ts:162`, merged `3f70224a069b`); its other two — `systemTest/akto/tests/preSuiteSetup.ts:36` and `systemTest/playwright/global-setup.ts:42` — stay on that ticket. **These two are not on it.**

**Fix shape:** `fileURLToPath(new URL(...))`, as merged in `runner/cli.ts`. Red-proof shape: resolve from a temp directory whose name contains a space and assert the resolved path equals the real file, as the KS-1337 cell does — that shape reds even from a checkout without a space, which matters because most checkouts do not have one.

## A second, related gap, recorded here rather than split (the GO capped this at one ticket)

**Neither** `ks860` **nor** `ks879` **walks** `systemTest/` — `ks879`'s `DEV_ROOT` is `Blockchain/Dev` and `ks860`'s `WALK_ROOTS` are `services/` and `packages/` (gate29 N-1291-4, read at source). So that whole tree has **no raw-control-byte and no loopback-bind guard**, and nothing structural would have caught this class there either. That is arguably a separate workload from the four lines above; it is named here so it is not lost, and it can be split out.

## Done when

- ☐ the 4 lines in the 2 `Blockchain/Dev` files take their path through `fileURLToPath`
- ☐ at least one cell pins the spaced-directory case for them
- ☐ a decision is recorded on whether `ks860`/`ks879` should walk `systemTest/` (or a separate ticket exists for it)

## Provenance

Gate29 report `2026-09-26-batch1290-g29/report.md` (sha256 `c3a273b3a582c088d3d088a3ac21a954c562ac8735cc679ec7979c12553f1e52`, measured by this seat), notes **N-1291-2** (its sweep-D half) and **N-1291-4**.

## Board search before filing

Literal match over **1335 issues (includeArchived) and 3780 comments**. Control token `b31nonce-9wq4tx-never-written` -> 0, while known terms returned hits, so the search discriminates in both directions. `import.meta.url).pathname` -> 2 (KS-1337, scoped to `systemTest/`; KS-847 Done, a NUL-byte/grep issue) · `WALK_ROOTS` -> 3 (KS-1319 and KS-1155, both about walk TIMEOUTS, not coverage; KS-876 Done). **Neither half of this is filed.**

Refs KS-1337
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1347-take-the-ks732-spec-and-handler-paths-with-fileurltopath-not-8183d3494b6e">Review in Linear</a></p>

