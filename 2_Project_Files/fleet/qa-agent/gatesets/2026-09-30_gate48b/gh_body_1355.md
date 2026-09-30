## What this changes

Adds an **unscoped** `"undici": "^7.29.1"` to the `overrides` of both `Blockchain/Dev/package.json`
and `Blockchain/Dev/frontend/issuer/package.json`, regenerates both locks, and carries the js-yaml
`5.2.3 → 5.4.2` fix in `systemTest/performance/package-lock.json`.

Both manifests already carried a **jsdom-scoped** `undici` override, which is why the top-level pin
stayed at `5.29.0` in both trees. The top-level pin comes from `@connectrpc/connect-node`, which
declares `undici ^5.28.3`.

**Five files, +14/−63.** No baseline row. No `GRANDFATHERED_NO_EXPIRY` entry touched.
`scripts/audit/audit-baseline.json` is byte-identical to develop's.

## Why, and what it replaces

`GHSA-r53p-7pc4-xj5r` (undici) and `GHSA-r3ph-w7gj-g6xm` (js-yaml) were published on 2026-09-29 and
between them refuse **every** push from `develop` at preflight legs 6 and 7. This PR removes both
advisories by bumping, so it needs **no security acceptance at all**.

That is the difference from PR #1354, which fixes js-yaml and *accepts* undici on a dated baseline
row. **This PR supersedes #1354's purpose on the merits. #1354 is untouched by this PR** — not
merged, amended, closed or pushed to. Its js-yaml half is the same bytes: the
`systemTest/performance/package-lock.json` blob here is `80c6752aab862bb6613cc014b1ebb0f2992967a6`,
identical to #1354's head.

Refs KS-1378 · context: KS 470, KS 559, KS 769, KS 1394

## How the locks were regenerated

Both in `node:24-alpine` (npm **11.19.0**, node **v24.21.0**, printed in the same run):

- **issuer lock** — issuer directory mounted, `npm install --package-lock-only --ignore-scripts`.
- **root lock** — `Blockchain/Dev` mounted (the root lock carries **32 `file:` link entries**, so a
  per-directory mount is the `EMISSINGTARGET` case recorded in KS 1394). This one needed
  `npm update undici --package-lock-only --ignore-scripts`; `npm install --package-lock-only` left
  the root lock's undici at `5.29.0`.

⚠ **npm printed `up to date` on every one of these runs, including the ones that rewrote a lock.**
The byte comparison is the instrument, not the banner.

**A pristine control tree at the same SHA, given the identical commands, did not move** — its
undici stayed `5.29.0`. So the override supplies the direction and the `update` verb the
re-resolution; neither alone moves it.

## The delta, per lock, measured against that control

Both locks change the **same three entries and nothing else**:

| | before | after |
|---|---|---|
| `node_modules/undici` | 5.29.0 | **7.30.0** |
| `node_modules/@fastify/busboy` | 2.1.1 | removed |
| `node_modules/jsdom/node_modules/undici` | 7.30.0 | removed (deduped) |

- issuer lock **723 → 721** entries · root lock **1970 → 1968** entries.
- `integrity` and `resolved` of the new entry equal the registry's `dist` values for 7.30.0
  (control: the same comparison against 7.29.1's integrity returns false).
- ⚠ **The root lock also carries 12 unrelated entry changes** — eleven `lightningcss-<platform>`
  binaries and `magicast`, all `dev: true → null`. **These are npm's own bookkeeping, not this
  change:** a pristine control tree given the identical commands produces the **same 12**, set-equal,
  `only in mine: NONE`. Any future root-lock regeneration (KS 1380's fix included) will carry them.

## Scope: who actually consumes undici

Derived from the lock graph, not assumed:

- **24 of 32 workspace members reach undici** — but **23 of them only via `vitest → jsdom`**, and
  **`jsdom` resolves undici to `7.30.0` both before and after** (before: its nested copy; after: the
  hoisted one). Their test tooling loads the same version either way.
- **Exactly one member reaches undici through runtime `dependencies`: `frontend/issuer`**, via
  `@meshsdk/core → @meshsdk/provider → @utxorpc/sdk → @connectrpc/connect-node → undici`.
  (Control: the same runtime walker finds `express` reachable from 26 of 32, so it is not blind.)

So the real blast radius is the issuer frontend, which is the tree gate48a flagged.

**NOT COVERED:** `Blockchain/Dev/mobile/secuura-app` is out of the audit corpus (KS 769, expires
2026-10-19) and its undici 6.28.0 via `@expo/cli` is **unmeasured** — this PR does not touch it.

## Leg 6's CLEANUP line, verbatim — and nothing is removed here

With this change, `audit:gate` drops from 24 reported advisories to 11 and prints:

```
CLEANUP (advisory): 14 baseline entries are no longer reported — remove:
  - GHSA-2mjp-6q6p-2qxm (undici, KS-470)
  - GHSA-35p6-xmwp-9g52 (undici, KS-470)
  - GHSA-4992-7rv2-5pvq (undici, KS-470)
  - GHSA-g8m3-5g58-fq7m (undici, KS-470)
  - GHSA-g9mf-h72j-4rw9 (undici, KS-470)
  - GHSA-p88m-4jfj-68fv (undici, KS-470)
  - GHSA-v9p9-hfj2-hcw8 (undici, KS-470)
  - GHSA-vrm6-8vpv-qv8q (undici, KS-470)
  - GHSA-vxpw-j846-p89q (undici, KS-470)
  - GHSA-v2v4-37r5-5v8g (ip-address, KS-470)
  - GHSA-mwp4-54f8-5fhr (ip-address, KS-729)
  - GHSA-8xcm-r25x-g524 (undici, KS-559)
  - GHSA-m8rv-5g2x-5cg5 (undici, KS-559)
  - GHSA-v3r7-h72x-cjcm (undici, KS-559)
OK — no advisories outside the triaged baseline.
```

**Twelve undici rows and two ip-address rows. This PR removes NONE of them** — the baseline cleanup
is a separate change, and note this is now *advisory* output on a **passing** leg.

## Test Evidence

**Touched:** `Blockchain/Dev/package.json`, `Blockchain/Dev/package-lock.json`,
`Blockchain/Dev/frontend/issuer/package.json`, `Blockchain/Dev/frontend/issuer/package-lock.json`,
`systemTest/performance/package-lock.json`.

**Ran** (all on this branch's head unless stated):

- `audit:contract` **rc 0** · `audit:gate` (leg 6) **rc 0** · `audit:locks` (leg 7) **rc 0**.
  Each rc read on its own line, never through a pipe.
  Measured across three configurations so the result is attributable:
  | configuration | contract | leg 6 | leg 7 |
  |---|---|---|---|
  | develop | 0 | 1 (r53p) | 1 (r3ph + r53p) |
  | + override only | 0 | **0** | 1 (r3ph only) |
  | + override + js-yaml (this PR) | **0** | **0** | **0** |
  Leg 7's denominator moves across the three — `20 advisories match, 18 baselined` → `7/6` → `6/6` —
  so the pass is not vacuous. Corpus as the tool states it: **43 standalone lockfiles**
  (45 tracked − the Dev root − 1 out of scope).
- **Issuer image build** under undici 7.30.0: `docker compose -p b48probe build issuer-frontend`,
  **rc 0**. `npm ci` genuinely re-ran — **666 packages** (develop: 671). Build only; nothing started,
  pruned or removed.
- **Served tree byte-identical to develop's.** The build exported the *same* image digest
  (`sha256:061307f7b133…`) as the develop build, and BuildKit reported
  `COPY --from=builder /app/dist/` as `CACHED` — its cache key is the content digest, so the built
  `dist/` hashed identical despite a different install. Served tree: **58 files, 7,388 KiB** —
  matching gate48a's develop measurement exactly. **0** served files mention undici
  (controls: `react` 12, `secuura` 7; and the same extractor on the bare `nginx:1.30-alpine` base
  returns 6 files, so it discriminates).

**NOT run:**

- **The 23 service suites** whose only path to undici is `vitest → jsdom`. Not skipped for
  convenience: `jsdom` resolves undici to **7.30.0 on both sides**, measured from both locks, so
  their behaviour through undici cannot change. Running them would add no information about *this*
  change. Say if you want them run anyway.
- No Schemathesis, no Akto, no k6, no Playwright. No deploy of any kind.
- No `npm audit fix`, no lock hand-edit, no baseline edit.

**Migrations + config:** none. No migration, no schema change, no environment variable, no
compose/service definition touched. `frontend/issuer/Dockerfile` copies only
`frontend/issuer/package*.json` before `npm ci`, so the **root** manifest/lock change does not reach
the issuer image; the image result above is attributable to the **issuer** lock alone.

### The pre-push preflight on this exact head

**`12/15 legs ran, 3 SKIPPED, nothing failed.`** The hook prints, in its own words:
*"This is NOT a pass. Do not quote it as one — say which legs ran."* So: **it is not a pass, and the
three that did not run are legs 3, 4 and 8** — all `SKIP — local stack not up on
http://localhost:6882`. Shell suites: **61 passed, 0 failed, 0 skipped (of 61)**.

Inside that run:

- **Leg 6** (npm-audit gate): `audit-gate: 11 distinct advisories reported, 25 baselined.` →
  `OK — no advisories outside the triaged baseline.`
- **Leg 7** (standalone-lock advisories): `43 standalone lockfiles … 1611 distinct packages pinned —
  6 advisories match, 6 already baselined.` → `OK — no standalone-lock advisories outside the
  triaged baseline.`
- **Leg 2** (lockfile clean-room): `All 35 standalone lock(s) pass clean-room npm ci`, and its
  `covered:` list names `frontend/issuer` — so the regenerated issuer lock is clean-room installable
  by the repo's own guard, measured in the hook rather than by me.

⚠ **Disclosure on the first push attempt:** it was refused, `push rc=1`, on **leg 14** (one shell
suite aborted: `packages/shared is not built … dist/index.js missing`, **0 of its 27 cells ran**) and
**leg 1** (`DEPS MISSING — this working tree's workspace install is absent or incomplete. This is NOT
spec drift.`). Both were the same environment condition — a fresh worktree with no workspace install
— and neither reads any of the five files in this diff. Fixed with the remedy the hook itself
prescribes (`npm ci` in `Blockchain/Dev`, then `npm run build -w packages/shared`), **not** with the
`--no-verify` bypass the hook also offers. The commit SHA did not change between the two attempts, so
the files legs 6 and 7 passed are byte-identical. That first run counted **11/15**, not 12/15,
because leg 1 did not run either.
