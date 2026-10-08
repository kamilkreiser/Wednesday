Refs KS-1410
https://linear.app/secuura/issue/KS-1410

Raised from a Wednesday-held Spark pass, re-proved by Seat R 19th on develop `0a6177ea5482`.

## What this changes

Ten catch blocks across three api-gateway routers built their 500 response body from
`err.message` with **no `NODE_ENV` guard**, so whatever the thrown error said reached the client in
every environment, production included. Each router now has a local `fail500` helper matching the
shape originate already uses (KS 1334, KS 730): log the thrown text server-side with the route
named, answer a constant `INTERNAL_ERROR` body.

| file | sites |
|---|---|
| `Blockchain/Dev/services/api-gateway/src/routes/notifications.ts` | 6 |
| `Blockchain/Dev/services/api-gateway/src/routes/batch.ts` | 3 |
| `Blockchain/Dev/services/api-gateway/src/routes/audit-export.ts` | 1 |

**Scope: 10 of the ticket's 28 sites. The other 18 stay OPEN**, including
`transfer/delegations.ts`. This PR does not close the ticket.

## Test Evidence

**Touched:** the three routers above, two new suites under
`Blockchain/Dev/services/api-gateway/src/__tests__/`, and both platform-k HTML docs
(flow block `36.`, cheat section `KS-1410`) in the same commit, per SKILL §4.

**Ran, on this branch, by the author:**

- **Red-first, SKILL §5b.** With the three routers reverted to the base and the new suites kept:
  `2 failed (2)`, **`Tests 21 failed | 6 passed (27)`, rc 1**. The six survivors are the 200-path
  controls — that the same 27 cells executed in both states is what distinguishes a real red from a
  suite that failed to import. With the fix: `2 passed (2)`, **`Tests 27 passed (27)`, rc 0**.
  The product files were then restored and re-verified `cmp`-identical (with a 1-byte tamper proving
  `cmp` can fail), and the green re-run reproduced 27/27.
- **Whole touched-service unit suite:** `@secuura/api-gateway` — **`Tests 845 passed (845)`, rc 0**,
  no failures.
- **S-1:** `npm ci --ignore-scripts` in `Blockchain/Dev` (1937 packages, rc 0);
  `npm run build --workspace=packages/shared` rc 0 with `dist/index.js` asserted present
  (17,746 B, and a phantom path read absent through the same test); `npm ci` in all four of
  `systemTest/{akto,api-explorer,performance,playwright}`, rc 0 each. 0 unrelated tracked files
  modified afterwards.
- **Doc blocks:** appended by tool with a byte-for-byte read-back — **0 failed**, including
  "THE ONLY difference from the blob at the base IS this fragment, byte for byte" for both documents,
  both 1-byte-altered-fragment controls correctly failing the same comparison, and all 30 / 19
  pre-existing blocks re-read byte-identical. Flow tail `26.` -> `36.`; cheat tail `KS 1164` ->
  `KS-1410`.

**Versions, read from `node_modules` rather than memory:** node `v24.7.0`, npm `11.5.1`,
vitest `4.1.11`, typescript `5.9.3`, `/bin/bash` `3.2.57`.

**Engines gap, measured:** `systemTest/akto`, `systemTest/performance` and `systemTest/playwright`
each declare `engines.node >= 24.11.0`; this host runs **v24.7.0**, so all three installed below
their declared floor — **105 `EBADENGINE` warnings**. `systemTest/api-explorer` declares none.

**NOT run, and not claimed:**

- **The four platform suites (Schemathesis, Akto, Playwright, Performance/k6) did not run** — no
  local stack on this host. No pass is claimed for any of them.
- **A live run is OWED.** Every cell above dispatched the router objects offline through a fake
  req/res pair; no gateway process served a request, so the runtime 500 path is unmeasured.
  **The ticket does not move to Done** (SKILL §5f).
- The 18 remaining KS-1410 sites are untouched and unmeasured.
- Harness note: the batch / audit-export suite grades only the first product's sites in its A3b
  arm, so that arm is weaker than its name suggests.

**Migrations + config:** none. No dependency, lockfile, manifest, baseline or spec-version edit.
No file under `systemTest/` is touched, so SKILL §5c does not apply.
