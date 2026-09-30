Six advisories published 2026-09-29T23:44:58Z–23:54:25Z began being reported by `npm audit`
between 02:54Z and 03:29Z on 2026-09-30, failing preflight legs 6 and 7 on `develop` and blocking
every push on this repo. None of them is our code: all six are transitive, and every affected range
has an in-range patch that this repo already resolves somewhere else today.

**Locks only.** No manifest, no baseline row, no gate file, nothing re-dated.

## The six, each against the lock entry that clears it

| advisory | sev | package | from → to | locks |
|---|---|---|---|---|
| GHSA-qhr7-859c-m2p7 | high | brace-expansion | 5.0.9 → 5.0.12, 1.1.18 → 1.1.21 | 17 |
| GHSA-6j4f-fj2g-mc7p | high | brace-expansion | 5.0.9 → 5.0.12, 1.1.18 → 1.1.21 | 17 |
| GHSA-q2hr-2g5m-vwhr | moderate | brace-expansion | 5.0.9 → 5.0.12, 1.1.18 → 1.1.21 | 17 |
| GHSA-hrr3-gc8f-f4qj | moderate | fast-uri | 3.1.7 → 3.1.8 | root, services/mcp-server, services/nft-certificate, systemTest/akto, systemTest/api-explorer |
| GHSA-j6r3-76f7-8jcv | moderate | ip-address | 10.7.0 → 10.7.2 | services/mcp-server |
| GHSA-h3mg-xc3c-68pw | moderate | ip-address | 10.7.0 → 10.7.2 | services/mcp-server |

Both ip-address advisories are `<= 10.7.0`, first patched 10.7.1 (GitHub advisory API). 10.7.2 is
what the root, `frontend/issuer`, `packages/shared` and `services/anchoring` locks already pin, so
`services/mcp-server` was the lone straggler.

**18 locks, 30 version moves, 0 entries added, 0 removed.** PROD entries moved: root
(brace-expansion, fast-uri), `services/mcp-server` (all three), `services/nft-certificate`
(brace-expansion, fast-uri). The rest are dev-flagged.

`Blockchain/Dev/mobile/secuura-app` is **untouched**: its brace-expansion pins (1.1.18 ×4, 2.1.4)
are out of scope under KS 769, which expires 2026-10-19. Leg 7 already declares that tree out of
scope, so no row survives because of it.

## How the locks were regenerated

Per lock, in `node:24-alpine`, **npm 11.19.0**:

    docker run --rm -v <dir>:/app -w /app node:24-alpine \
      npm update <pkgs> --package-lock-only --ignore-scripts

**The host npm was not used.** A lock-only `npm update` has been inert on this repo before under
host npm 11.5.1 — rc 0, nothing moved, a different lock written — where the container's npm moved
it. An rc-0 regen that moves nothing reads exactly like success, so **every move here is proved by
`cmp` plus a parse of both locks, never by the exit code.**

That instrument earned itself: **2 of 18 locks came back INERT and had to be fixed.**
- `systemTest/akto` and `systemTest/performance` failed `npm error EMISSINGTARGET … "../../observability"
  is referenced by "node_modules/secuura-observability" but does not exist`. Both declare
  `secuura-observability: file:../../observability`; only each lock's own directory had been mounted,
  so the sibling was invisible in the container. Fixed by mounting the repo root with `-w` at the
  package directory. Control for that diagnosis: `systemTest/playwright` has **0** `observability`
  references, which is why it alone succeeded first time.
- `systemTest/akto` then failed a second, different way — `Invalid tag name "brace-expansion fast-uri"` —
  because a scalar shell variable holding two package names does not word-split in zsh, so both went
  as one argument. Re-run with explicit arguments: moved.
- Collateral guard: `observability`'s own lock is sha256 `aa007277c89251be` **before and after** the
  root-mounted runs, so the wider mount did not let npm rewrite a lock that was not named.

## Test Evidence

**Touched:** 18 `package-lock.json` files. No source, no manifest, no test, no gate file, no
workflow.

**Ran — audit legs, at head `52dadb07f70d`, each rc captured on its own line:**
- `npm run audit:gate` (leg 6) — **rc 0**: "11 distinct advisories reported, 26 baselined" ·
  "OK — no advisories outside the triaged baseline". Was rc 1 with 4 unbaselined at `3e3a68260d0e`.
- `npm run audit:locks` (leg 7) — **rc 0**: "OK — no standalone-lock advisories outside the triaged
  baseline". Was rc 1 with 6 unbaselined.
- `npm run audit:contract` — **rc 0, 59/59.**
- Each of the six advisory ids greps to **0 occurrences** in both legs' output, checked one at a time.
- `npm ci --ignore-scripts` — **rc 0, 1935 packages**: the refreshed root lock installs.

**Ran — images, build only (no `up`, no `down`, no `--rmi`, no prune):**
- `docker compose -p b49probe build mcp-server nft-certificate` — **rc 0**, both images built.
  These are the two services whose own locks moved and whose Dockerfiles copy that lock and run
  `npm ci`. **0 Dockerfiles copy the workspace-root lock**, so the root lock's 4 moves reach no image.
- Resolved versions read inside each built image (`--rm --network none --read-only` probe):
  `app/node_modules/brace-expansion` **5.0.12**, `app/node_modules/fast-uri` **3.1.8**,
  `app/node_modules/ip-address` **10.7.2** (mcp-server). Control: `develop`'s locks pinned
  5.0.9 / 3.1.7 / 10.7.0, so the probe discriminates.
- `docker system df` before → after: images 111 → 113, build cache 799 → 833 entries. Nothing pruned
  or removed.

**Ran — suites for the two services whose images ship these locks, before and after:**
- Before (pristine `develop`, `s-b49-ctrl`): mcp-server `1 failed | 2 passed (3)` files, `3 passed |
  2 skipped (5)` tests; nft-certificate `2 failed | 4 passed (6)` files, `29 passed (29)` tests.
- After (this head): **byte-identical counts and the identical failing-file set** (`diff` rc 0 on the
  failing-file lists). Root cause both sides: `Failed to resolve entry for package "@secuura/shared"` —
  `packages/shared/dist` is absent in both worktrees. **Pre-existing at `develop`, not caused by this
  change**; `packages/shared` is not among the 18 files here.
- With `packages/shared` built (`npm run build`, rc 0), on this head: mcp-server **3/3 files, 5/5
  tests, rc 0**; nft-certificate **6/6 files, 38/38 tests, rc 0**. The 38-vs-29 difference is the two
  files that previously could not load.

**Pristine control (root-lock drift):** in a second `--detach` worktree at the same SHA, given the
same container and flags but **no package arguments**, `npm install --package-lock-only
--ignore-scripts` returned rc 0 and **`cmp` rc 0 — it moved nothing at all** (0 added, 0 removed, 0
version-moved, 0 dev-flag-moved). Entries the control churns that this change does not: **0**.
Entries this change moves that the control does not: exactly its **4** root entries. A previously
recorded 12-entry root-lock drift (eleven `lightningcss-*` plus `magicast`) did **not** reproduce
here; that finding came from a regen whose **manifest had changed**, which invalidates resolution.
This change alters no manifest.

**NOT run / NOT covered:**
- No Schemathesis run, no Akto scan, no k6 run, no Playwright run.
- No deploy anywhere — not the VM demo, not Azure. **Merged is not deployed.**
- The other 16 locks' images were not built and their suites were not run; only the two PROD services
  whose own locks moved were built and exercised.
- 🔴 **Residue this change cannot fix, found by the image probe:** the `node:24-alpine` base image
  carries npm's **own** bundled `brace-expansion 5.0.7` and `ip-address 10.2.0` at
  `usr/local/lib/node_modules/npm/node_modules/…`. Both sit in the vulnerable ranges. They are not in
  our dependency tree, no lock of ours pins them, and **neither leg 6 nor leg 7 audits them** — both
  read our lockfiles. Out of scope here; reported rather than left silent.
- Whether any consumer behaviour changes between brace-expansion 5.0.9 → 5.0.12, fast-uri 3.1.7 →
  3.1.8 or ip-address 10.7.0 → 10.7.2 was not traced beyond the suites above; these are patch
  releases inside already-declared ranges.

**Migrations + config:** none. No migration, no environment variable, no config file, no secret.

Refs KS-1378
