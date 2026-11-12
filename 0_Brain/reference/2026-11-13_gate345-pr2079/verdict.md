PR 2079: GO WITH NOTES (at head 0fffdfba0f9578f23d48112068d1451ea947cd29; tier 1)

Gate 345 (tier 1, Opus relaunch), 2026-11-13 06:08-06:21 AEDT. Findings only: nothing merged, pushed, commented, mailed or written to Linear/GitHub.
Pins: re-read by git ls-remote at 06:08:50 and again at 06:20:43 AEDT: develop 410feda1a85e54b82a65464607f4761c2da3bb1b, refs/pull/2079/head 0fffdfba0f9578f23d48112068d1451ea947cd29. Neither moved; both equal the commission's pins.
PR merge-base with develop: c5c26b2835df (develop is 98 commits ahead of it). PR = ONE commit, 18 paths (+123 / -2567).

## FOUND

G345-2079-1 (Medium, process; a merge condition, not a code defect). The two pre-merge acknowledgement boxes (Schemathesis, Akto) are unticked and say "NOT run". `!CODING/Secuura/Blockchain/2_Project_Files/CLAUDE.md:266-270` reads: "Before merging a PR, the pre-merge suites MUST be run and pass, and the author acknowledges it in the PR description." By the letter of the project's rules this blocks the merge until they are run, or until Wednesday/Kam waives them for this PR. The case for a waiver: no running service loads `@secuura/service-utils` (G345-2079-Q3 below), so neither suite can reach the deleted code. The waiver is a ruling for Wednesday; the gate does not make it. The `PREFLIGHT INCOMPLETE (13/16, legs 3 4 8 skipped, nothing failed)` line is quoted correctly as not a pass. On its own it is not a separate blocking rule: TESTED = QA GO + Test Evidence + own suites (CLAUDE.md:296-299).

G345-2079-2 (Low). Every GitHub check on the PR is red, but no job ever ran. All 13 failures finished in 2-3 s on 2026-11-06 18:16Z. The annotation on "Linear ticket present" and "Code Security Gates" reads: "The job was not started because recent account payments have failed or your spending limit needs to be increased." Actions is retired for this repo (CLAUDE.md:288-290, 492-498). The red is billing, not content, and it carries no testing claim either way. `mergeStateStatus` is UNSTABLE for that reason only.

G345-2079-3 (Low). The floor move (500 -> 494) is justified, but the PR's numbers are stale against current develop. The walker's own count, read by planting an impossible floor: develop 410feda1a85e = 507, PR head = 500, merge result = 501 (the PR body measured 506 -> 500 at its base c5c26b2835df). At the merge, the old floor `>500` would still pass (501). The move is strictly needed only at the stale head. The drop develop -> merge is exactly 6, the six deleted product files, so nothing else went blind. The slack after merge is 7, not the 6 the comment states. The in-code comment ("reads 500 after") describes the head, not the post-merge tree. Cosmetic.

G345-2079-4 (Low). The PR's own consumer guard (new test G4) scans only `services/shared/src` and only `from '...'` forms. It would miss a `require(...)`, a dynamic `import(...)`, or an importer elsewhere in the repo. My repo-wide census (Q3 below) covers that gap at this head. The test stays narrower than the claim "nothing imports it".

G345-2079-5 (Info). Docs left stale after merge:
- `.planning/codebase/CONCERNS.md:26,165-166` still recommends wiring `redis-security-store.ts` into all services as the production store, and that file is now deleted.
- `BACKLOG.md:264-295` (the KS-657 row) still says the dead half is "UNCHANGED". Ticket acceptance 3 asks for that row to be removed.
- `Blockchain/Dev/docs/archive/PHASE4_*` and the two `KS-1868-services-shared-redis-stores-cache.html` fragments describe deleted code. These are historical.
- `ioredis` stays declared and is now unused (the body says so).
- `services/shared/services/redis.ts` stays (the body says so). It imports `@secuura/shared/cache/redis`, not the deleted code.

## TESTED (answers to the commission's questions)

Q1 KS-657 scope (Linear, read-only, project key). Title: "services/shared (@secuura/service-utils) cannot build ... its src/ half is dead but types/ is live in billing". Acceptance 2 is the retire-or-repair decision. The ticket comment of 2026-11-06T09:28:49Z records Kam's ruling: card secuura-ks-657-dead-shared-cache-code-1106 = a, "Delete the cache section; keep the types". The PR does exactly that: it deletes `src/cache/` (5 files), the store that imports `../cache/redis-client`, the two re-exports and the six KS-1868 tests that pinned them, and keeps `types/`, `security/{audit,headers,rate-limiter,validation}.ts` and `utils/logger.ts`. `Refs KS-657` with no close word is right, because the ticket stays open (state at read: In Progress).

Q3 Consumer enumeration (THE question). Instrument: `git grep` at the merge-result tree 09404e649ab8 and at the head, over the whole repo (not only services/shared). The scratch clone borrowed the project checkout's object store as a read-only alternate, plus a batched fetch of the 153 missing blobs, so each grep took about 3 s. Patterns: all 25 exported symbols of the six deleted modules, plus the module paths `redis-security-store|redis-client|cache-middleware|connection-pool|security:bruteforce` and `service-utils`.
- Results: 37 files at each tree. Every code hit is an unrelated same-name symbol: `packages/shared/src/cache/redis.ts` CACHE_TTL, api-gateway's own `services/redis.ts` brute-force/rate-limit store, `packages/shared/src/middleware` redisClient, local TTL constants, a local `certificationCache` Map, and comments.
- No importer, constructor, dynamic import or require of the deleted code anywhere.
- `@secuura/service-utils` appears in no package.json other than its own, and in no code.
- No relative import resolves into `services/shared/src`. The frontends' `../shared/src` is `frontend/shared`.
- Dockerfile/compose/scripts: the only reference is `services/billing/Dockerfile:47 COPY services/shared/types/` (kept) and a comment at `scripts/build-docker.sh:7`.
- Census walkers: `entrypoint-corpus.test.ts:69` lists the `services/shared` package dir (kept). The zod census names `security/validation.ts` and `audit.ts` (kept).
- Env: the deleted code read only REDIS_HOST/PORT/PASSWORD/DB/PREFIX, which other services read too, so no config is orphaned.
- Positive controls: the same grep finds billing's live `../../shared/types/svs-types` import (chargeable-events.ts:23 and its test) and the COPY line. At the merge-base it finds `getSecurityStores` in the store and in security/index.ts.
- Runtime: no service's brute-force lockout, CSRF or rate limiting changes, because no running process loads this package. Api-gateway's lockout and rate limit use their own `services/api-gateway/src/services/redis.ts` and `middleware/rateLimitEnforce.ts`, untouched.
- Open-PR overlap: 92 open PRs. Only #2079 touches the 18 paths (positive control: #2079 lists 18). #948 (a dependabot vite bump) touches `services/shared/package.json`, which is not in this PR. No other open PR's patch names a deleted symbol, the path or `service-utils`.

Q2 Floor red-proof (packages/shared ks1725-zod3-compat.test.ts, F2 cell):
- At head: the planted old floor `>500` gives RED, "AssertionError: expected 500 to be greater than 500" (267/268). The restored 494 passes 268/268. The file was restored by `git checkout` and its sha256 matched before and after.
- Counts via a planted `>9999`: develop 507, merge 501.
- Not hiding a regression: the drop is exactly the six deleted files (see G345-2079-3).

Q4 Suites (vitest JSON counts; Node v26.8.1, not the LTS 24; load1 2.2-3.6). All three trees use identical package.json and lock blobs for the three packages.

| package | develop 410feda1a85e | PR head 0fffdfba0f95 | merge probe (09404e649ab8) |
|---|---|---|---|
| services/shared | 9 files / 45 tests, 45 pass | 4 / 20, 20 pass | 4 / 20, 20 pass |
| packages/shared | 82 files / 1631: 1563 pass, 9 fail, 59 skip | 75 / 1495: 1427 pass, 9 fail, 59 skip | 82 / 1631: 1563 pass, 9 fail, 59 skip |
| services/billing | 20 files / 347 pass, 2 files fail to load | not run | same as develop |
| builds (tsc) | packages/shared 0, services/shared 0, billing 0 | packages/shared 0 | packages/shared 0, services/shared 0 (dist has no cache/), billing 0 |

- services/shared: 45 -> 20 = minus the 32 deleted KS-1868 cells, plus the 7 new cells.
- packages/shared: the 9 failures are identical on all three trees and environmental (my scratch install, not the workspace root): ks256 spec-example guard 8 (JSON parse of a child script), wallet-signature 1, plus a ks781 file-level error. The PR's head is on the old base, so its file count differs from develop's.
- ks1725-zod3-compat: 268/268 on all three trees.
- Billing's 2 load failures are `jsonwebtoken` not hoisted in my per-package install. They are identical on develop and the merge.
- Red-first for the new KS-657 test: run against develop it gives 4 RED by AssertionError (G1-G4), and the 3 controls pass. At the head and the merge it passes 7/7.

Q5 Merge: `git merge-tree --write-tree` develop 410feda1a85e x head 0fffdfba0f95 gives rc 0 in both orders, with the same tree 09404e649ab83a76219183db7386fc96f9c9dbf2.
- One path is changed on both sides: `ks1725-zod3-compat.test.ts`. Develop changed the 113 -> 114 wrapped-count pin; the PR changed the F2 floor. In the merged file both hunks are present.
- Survival control: merged vs develop differs in exactly the PR's 18 paths. Merged vs head differs in exactly develop's 392 changed paths. So every develop line survives, and the PR's changes survive.

Body checks: Linear URL present; `Refs KS-657` (no close word); PII review stated N/A; Test Evidence block present with honest NOT-run lines; fragment pair present (flow + cheat).

## HOW
- Scratch only: `scratch/clone` (blobless, push URL DISABLED). Its `objects/info/alternates` now points read-only at the Blockchain project's `.git/objects`; that is a file inside my clone, and the project repo was not written to.
- `scratch/wt`: a worktree on a local merge-probe commit 4620a8b9b1d2 (parents develop + head, tree 09404e649ab8). It was never pushed.
- Installs: `npm ci --ignore-scripts` per package, plus vitest 4.1.12 / vite 7.3.7 `--no-save` into packages/shared, plus a scratch symlink `node_modules/@secuura/shared -> ../../packages/shared` to emulate the workspace root.
- Reads: Linear (KS-657 plus 9 comments, read-only) and GitHub (PR body, check runs, annotations, open-PR files) via the Blockchain project's own `.env` key and gh config. No secret printed.

## NOT TESTED
- Schemathesis, Akto, Playwright, k6: no stack (G345-2079-1).
- No Docker image build.
- No full workspace-root `npm ci`, so the 9 packages/shared and 2 billing environmental failures are not cleared. They are equal on develop and the merge, so they are not attributed to the PR.
- Node 24.
- Consumers outside this repository and untracked files.
- Other services' unit suites: the enumeration names no service consumer, so none were run.

Leftovers (deletion is refused by hook, so they stay): `scratch/wt` (checked out at develop, with an untracked copy of the ks657 test from the red-first run), `scratch/*.json|*.log`, `scratch/missing.txt`, `scratch/hits-*.txt`, `scratch/open-pr*.txt`, `scratch/ks657.json`, `scratch/pr2079.json`, and the alternates file in the clone. A stray `/tmp/x` was also created by a mis-typed redirect: 392 lines, the path names develop changed since c5c26b2835df. It holds no secrets.
