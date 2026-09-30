## BLUF

**Thirteen advisories published 2026-09-30 between 15:03:21Z and 15:37:57Z made preflight legs 6 and 7 return rc 1 on `develop`'s own dependencies, so no push on this repo succeeded.** This is an in-range lockfile refresh that clears all thirteen. **No manifest change. No baseline row added, removed or changed.**

Twelve are axios (7 high, 5 moderate); one is dompurify (low). None is one of KS 1378's five, and none is one of the two KS 1395 names — this is a fourth, separate batch.

## What changed

Four lockfiles, nothing else:

| lock | package | from | to |
| -- | -- | -- | -- |
| `Blockchain/Dev/package-lock.json` (workspace root) | axios | 1.18.1 | 1.20.0 |
| `Blockchain/Dev/package-lock.json` (workspace root) | dompurify | 3.4.13 | 3.4.16 |
| `Blockchain/Dev/frontend/admin/package-lock.json` | axios | 1.18.1 | 1.20.0 |
| `Blockchain/Dev/frontend/verifier/package-lock.json` | axios | 1.18.1 | 1.20.0 |
| `Blockchain/Dev/services/kyc/package-lock.json` | axios | 1.18.1 | 1.20.0 |

**Four locks, not the three leg 7 names.** The workspace root lock pins both packages and is leg 6's, not leg 7's; refreshing only leg 7's three would have left leg 6 failing. `frontend/issuer` needs no change — its own standalone lock already pins axios 1.20.0 and dompurify 3.4.16, which is also why leg 7 never reported the dompurify advisory (its only standalone copy is already patched; the vulnerable copy is in the root lock). `mobile/secuura-app` is out of scope under KS 769 (expires 2026-10-19).

**Why in-range and not a manifest bump:** every affected manifest already admits the patched version — `frontend/admin` `axios ^1.6.5`, `frontend/verifier` `axios ^1.6.2`, `services/kyc` `axios ^1.8.2`, `frontend/issuer` `dompurify ^3.4.13`. Neither package is declared at the workspace root.

## Test Evidence

**Touched:** four `package-lock.json` files. `git diff --numstat` = 4/4, 4/4, 7/7, 4/4 lines. `package.json` files changed: **0**. Files changed that are not a lock: **0**.

**Ran:**

* `npm run audit:gate` (leg 6) — **rc 0** at head. BEFORE at develop `4f18c59a89db`: rc 1, `24 distinct advisories reported, 26 baselined` plus `FAIL — 13 NEW advisories not in the baseline`. AFTER: `11 distinct advisories reported, 26 baselined`, no FAIL block.
* `npm run audit:locks` (leg 7) — **rc 0** at head. BEFORE: rc 1, `18 advisories match, 6 already baselined` plus `FAIL — 12 advisories in standalone locks`. AFTER: `6 advisories match, 6 already baselined`.
* `npm run audit:contract` — **rc 0**, 59 tests pass, 0 fail, before and after.
* **All thirteen advisories shown absent from both legs, one by one**, each against the lock entry that cleared it. Positive control: leg 6 after the change still names 15 distinct ids (the grandfathered residue), three of them re-tested present by the same matcher — so the thirteen absences are real absences and not a matcher that stopped working.
* `services/kyc` suite (`vitest run`) — **rc 0, 6/6 files, 33/33 tests**, run in this tree AND in a pristine control tree at the same base carrying the OLD axios 1.18.1. Identical both sides: no regression from the bump.
* `packages/shared` `npm run build` — rc 0, `dist` 28 entries, in both trees.
* Images built: `docker compose -p b51probe build kyc admin-frontend verifier-frontend issuer-frontend` — **rc 0**, all four. `admin-frontend` and `verifier-frontend` genuinely re-ran `npm ci` (5.8s / 5.4s) because the changed lock busted their `COPY frontend/*/package*.json` layer; `kyc` re-ran both its stages; `issuer-frontend` was correctly CACHED because its own lock did not change. Build only — no `up`, `down`, `--rmi` or prune; 0 containers started.

**How the lock moves were proved:** regenerated containerised in `node:24-alpine` with **npm 11.19.0**, never host npm, because host npm has previously left an in-range `npm update --package-lock-only` INERT on this repo (rc 0, nothing moved). Every move verified by `cmp` plus a JSON lock parse against a **pristine control tree at the same base** — never by npm's `up to date` banner. All four locks moved, **0 INERT**, and **0 lock entries added or removed** in any of them (root 1968→1968 with 2 version moves; admin 329→329, verifier 308→308, kyc 262→262, 1 each). The control tree is still byte-identical at all four locks with `git status` 0 lines.

**Reachability (FOUND / TESTED / HOW):**

* `services/kyc` — **FOUND:** one source file imports `axios`; a real service path whose image ships `node_modules`. **TESTED:** its suite, before and after, 33/33 both. **HOW:** `vitest run` in this tree and in the pristine control.
* `frontend/admin`, `frontend/verifier` — **FOUND:** **zero** source files import `axios`; declared but unused, and their final images are nginx plus the built `dist/` with the builder stage discarded (a `find` for an axios directory in the final images returns nothing). **TESTED:** image build only. **HOW:** see NOT RUN.
* `frontend/issuer` — **FOUND:** `frontend/issuer/src/utils/sanitize.ts` imports `dompurify`. **TESTED:** nothing. **HOW:** see NOT RUN.

**NOT run:**

* **No suite for the three frontends — they declare no `test` script at all** (`frontend/admin`, `frontend/verifier`, `frontend/issuer`). That is KS 1391, open. So "suites before and after" is vacuous by construction for them and no pass is claimed.
* **No test covers `frontend/issuer/src/utils/sanitize.ts`**, the one dompurify consumer — searched `frontend/`, `services/` and `packages/` for a spec naming sanitize or dompurify; the five hits are api-gateway, originate and shared tests, none of them issuer's. The dompurify half of this PR is **untested**, and rests on the gate reading and the advisory's own patched range.
* No Schemathesis, Akto, Playwright or k6 run — none of them reads a lockfile version.
* No deploy anywhere: not kintsugi, not demo.
* `services/kyc`'s suite needs `packages/shared` built first, or one file fails to load with `Failed to resolve entry for package "@secuura/shared"`. **That red is pre-existing at develop, not caused by this change**: the pristine control tree with the OLD axios returns the identical `Test Files 1 failed | 5 passed (6)` and the identical single resolve error. Already recorded in `BACKLOG.md`.

**Migrations + config:** none. No migration file, no environment variable, no compose change, no CI change.

## Residue, unchanged by this PR

Leg 6's cleanup list still names the fourteen grandfathered dead rows on every run (thirteen undici plus `GHSA-v2v4-37r5-5v8g`): dead grandfathered rows; removal needs the contract floor `baseline-contract.test.mjs:217` revisited; Wednesday's to propose.

Refs KS-1378
