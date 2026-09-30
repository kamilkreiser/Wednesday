## BLUF

`analytics`, `billing` and `governance` images fail `tsc` on `develop`. Each service image copies the
built `/shared` beside the service's own `node_modules`, so `tsc` sees two copies of the same
declarations resolved from two different locks — TS2742 on an inferred express type, TS2345 on pg's
`Pool`. `packages/shared` pins `@types/express-serve-static-core` 4.19.9 / `@types/pg` 8.23.1; these 15
locks pinned 4.19.8 / 8.20.0 (`vc-issuer` 8.21.0). This moves the 15 forward to agree.

**Locks only.** No manifest, no Dockerfile, no source, no baseline row, nothing re-dated.
**27 entries moved, 0 added, 0 removed.**

Refs KS-1380

## Why no manifest change was needed

Measured before running it, not after:

* `@types/express-serve-static-core` is declared in **no manifest in the repo**. It is transitive under
  `@types/express`, which requires it at `^4.17.33`; 4.19.9 is inside that range.
* `@types/pg` is a `devDependencies` entry at `^8.16.0` (`^8.11.0` in `tenant-provisioning` and
  `tokenisation`). 8.23.1 satisfies both. `packages/shared` declares the same `^8.16.0` — it sits at
  8.23.1 only because #1339 re-resolved it afresh.

So `npm update` of the two packages is an in-range lock move, and nothing else moved with them
(`ADDED=0` in all 15).

## How the locks were regenerated

Per lock, in a container. Host npm 11.5.1 is never used — it dies with `edgesOut` on this fleet
(KS 1379):

```
docker run --rm -v <lockdir>:/app -w /app node:24-alpine \
  npm update @types/express-serve-static-core @types/pg --package-lock-only --ignore-scripts
```

`node:24-alpine` carries npm **11.19.0**, printed in the same run. Per lock the record carries pre/post
sha256, `cmp` rc and parsed MOVED / ADDED / REMOVED counts — never npm's `up to date` banner, which is
not evidence that nothing moved.

**Control.** A pristine worktree at the same base, same container, same command **with no target**:
**0 of 15 files changed, `cmp` rc 0, MOVED=0 ADDED=0 REMOVED=0.** Every move in this PR is therefore
attributable to the change and not to the tool.

## Test Evidence

**Touched:** 15 `package-lock.json` — `Blockchain/Dev/package-lock.json`,
`connectors/whatsapp-bot`, and `services/` analytics, billing, governance, kyc, nft-certificate,
referral, shared, staking, tenant-provisioning, tokenisation, transfer, vc-issuer, wallet-connector.

**Ran, at this head (`6cf5c3629cd6268c3891f8aec01acfa7d7cae6cf`), base `377989cf3829`:**

| check | base | head |
| -- | -- | -- |
| `docker compose build analytics` | **rc 1**, TS2742 ×8 | **rc 0** |
| `docker compose build billing` | **rc 1**, TS2345 ×2 + TS2742 ×6 | **rc 0** |
| `docker compose build governance` | **rc 1**, TS2742 ×2 | **rc 0** |
| `docker compose build kyc` (already-green control) | rc 0 | **rc 0** |
| `npm run audit:gate` (leg 6) | rc 0 | **rc 0** |
| `npm run audit:locks` (leg 7) | rc 0 | **rc 0** |
| `npm run audit:contract` | rc 0, 59/59 | **rc 0, 59/59** |
| `packages/shared` suite (vitest) | 48 files / 945 tests / 0 failed | **48 / 945 / 0** |
| `services/analytics` (vitest) | 5 / 28 / 0 | **5 / 28 / 0** |
| `services/billing` (vitest) | 9 / 93 / 0 | **9 / 93 / 0** |
| `services/governance` (jest) | 4 suites / 115 / 0 | **4 / 115 / 0** |

Image builds ran one at a time in a **pristine** worktree — a guard asserted 0 `node_modules`
directories under `Blockchain/Dev` before each, with the dep-installed tree (33) as its control.
`packages/shared` was built before every suite run: its `dist` is absent in a fresh worktree and every
consumer suite then fails to *load*.

**Pre-push preflight, quoted as the hook printed it:**

```
PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.
  legs 3 4 8 — local stack not up; you can clear this by starting it.
  This is NOT a pass. Do not quote it as one — say which legs ran.
```

**NOT run:** legs 3, 4 and 8 (they need the local stack up). The four platform suites
(Schemathesis · Akto · Playwright · Performance/k6) were **not** run — this change touches no service
source, no route, no spec and no runtime dependency, only dev-only `@types` in lock files. The other 18
services with a `build:` entry were not rebuilt; the 13 that were cover every lock this PR touches that
maps to a buildable service. `services/queue` and `services/guardian` were not built by anything here
— see the note below.

**Migrations + config:** none. No migration, no environment variable, no compose change, no
`audit-baseline.json` row, no gate file.

## Tier

**T2.** Both `@types` are `"dev": true` in all 14 service and connector locks. In the workspace **root**
lock they are not — `esc` is `devOptional: true` and `@types/pg` carries no dev flag — but that lock
reaches no image: **0 of 31 Dockerfiles copy a root-level `package*.json`** (control: 31 of 31 copy
*some* `package*.json`, so the zero is measured). No shipped image's dependency set changes.

## Two measured notes that are NOT changed here

* **KS 1387** reports the same three failures and suggests a `tsc --noEmit` gate over every service.
  Measured at the base: `npx tsc --noEmit` in analytics, billing and governance is **rc 0 with zero
  `error TS` lines, all three** — because host workspace hoisting gives one copy of `@types/*` while the
  image has two. That cell would be green on this bug. The cell that works is KS-1380's own suggestion —
  assert every lock agrees with `packages/shared` — which is **red at this base (15 disagree) and green
  at this head (27/27 agree)**. It is deliberately **not** added in this PR: wiring the pre-push hook is
  gate code and wants its own review.
  KS 1387 also reports that `.dockerignore` does not exclude `packages/shared/node_modules`. It does —
  line 19 is `packages/*/node_modules`, present at every SHA in play and since the file was created.
* **KS 1379**'s lock drift and its runtime majors (`bullmq`/`msgpackr` 2, `@azure/msal-node` 6) are
  untouched, and its deploy hold stands. Restoring the pre-#1339 locks is **not** the fix: measured, it
  regresses `brace-expansion` in four locks and `fast-uri` in two, leaves 1,097 entries still differing
  from this base, and overshoots its own targets (`nodemailer@^10.0.12` resolves to 10.0.13).
* Also found while building: `services/queue` and `services/guardian` sit behind
  `profiles: [phase2]`, so `docker compose config --services` omits them and a default
  `docker compose build` never touches them (34 services resolved, 31 with a `build:` section).
  `services/queue` is the service whose runtime moved furthest under #1339.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
