VERDICT: GO WITH NOTE at head b697e5b63ede... (tier 2, round 1 of 2; landing tree e128f13c9d55abcef758778146417949fe9a0259 on develop f75b52721dadd9539b64de17575e57823b8a936a; 0 blockers, 3 notes)

## BLUF
- Tier 2 holds: no shipped (non-dev) dependency crosses a minor, no major anywhere, no install script newly added, every resolved host is registry.npmjs.org (root-lock workspace links aside). Non-dev moves are only dompurify 3.4.16 -> 3.4.17 and ip-address 10.7.2 -> 10.7.4 (patch).
- The freeze clears for the right reason: develop is rc 1 / rc 1 with exactly the six GHSA ids; head is rc 0 / rc 0; a second instrument (`npm audit`) agrees (root 15 -> 9 ids, the six gone, nothing new; guardian and kyc 2 -> 0).
- Standalone-lock suites (security, guardian, kyc): 0 new reds, 0 vanished by test name, identical on develop and head. Notes are about reach (see Notes), not defects.

## Findings (notes, none blocking)
- N1 (reach, Q5): security standalone gave 354 tests / 4 red on BOTH sides vs the claim's 361/0. The 4 red files read repo-level files outside the service directory (ENOENT; `ks742`, `ks869`, `ks952`, `ks1434`), so they cannot pass in an isolated copy. They are identical red on develop and head, so they are environmental, not caused by the PR. The claim's 361/0 comes from the hoisted full-repo install and I did not reproduce it.
- N2 (control quality, Q4): the negative control (guardian manifest wanting vitest ^5.0.0 against the 4.1.12 lock) fails rc 1, but with an ERESOLVE peer conflict (vitest 4.1.12 vs @vitest/coverage-v8 peer), not the clean "lock does not satisfy" message the author got in Docker on npm 11.19.0. Host npm is 11.5.1. A second mismatch I tried (develop lock + head manifest) made npm 11.5.1 crash rc 2 with "Cannot read properties of null (reading 'edgesOut')". Both fail, as required. Just don't quote my control as the "Invalid: lock file" form.
- N3 (wording, Q1/Q6): "22 manifest lines" is 22 insertions plus 22 deletions (44 changed lines; 11 files x 2 lines each). True as 22 changed lines per side; say so if the PR body states it otherwise.
- Observation (not a defect): 4 dev-only minors ride along (@oxc-project/types 0.154 -> 0.155, chai 6.2.2 -> 6.3.0, std-env 4.2 -> 4.3, tinyrainbow 3.1.1 -> 3.2.0), all in vitest's closure, all dev=true, listed in the claim.

## FOUND / TESTED / HOW

Q1 Scope (holds). `git diff --name-status` develop..head: 37 M, 26 package-lock.json + 11 package.json, nothing else (no audit-baseline, hook or script). Each of 11 package.json: only `vitest` and `@vitest/coverage-v8` `^4.1.11` -> `^4.1.12` (aggregated: 11 x 4 distinct line shapes, 22 ins / 22 del). One commit; `rev-list --merges` = 0; parent = f75b52721dad. Head tree e128f13c9d55 equals the predicted landing tree because merge-base(develop, head) = develop tip and live ls-remote at start and end both read develop f75b52721dad, PR head b697e5b63ede (read via the cache clone's origin; my scratch clone's own origin is the local cache and its develop ref is stale, so I ignored it).

Q2 Freeze clears (holds). Read first: `audit-gate.mjs` runs `npm audit --json` at the workspace root and diffs against `scripts/audit/audit-baseline.json`; `audit-locks.mjs` enumerates `git ls-files '*package-lock.json'` and asks the registry bulk-advisory endpoint about each lock's exact pinned versions (38 standalone locks, 1481 distinct packages). Results (exported archives of each tree with a throwaway git index, root `npm ci --ignore-scripts` for the semver import):
- develop: audit:gate rc 1, 6 NEW; audit:locks rc 1, 6 NEW (13 matches, 7 baselined). Ids: GHSA-cg2g-xh64-v4q7 (critical, dompurify), GHSA-mrv2-3pqr-j5jr (high, dompurify), GHSA-c6gr-qvv4-5v3f (low, dompurify), GHSA-qxg6-89mg-rqv8 and GHSA-xp26-3454-mjgp (moderate, @vitest/mocker, 24 locks), GHSA-rxp7-6hxx-x8q5 (moderate, ip-address, 4 locks). Exactly the claim's six.
- head: audit:gate rc 0 ("9 distinct advisories reported, 24 baselined", the same 15 lapsing-row cleanup list as on develop, so not blind); audit:locks rc 0 (7 matches, 7 baselined).
- Second instrument `npm audit --package-lock-only --json` (id sets from `via[].url`): root develop 15 ids -> head 9 ids (the six removed, 0 new; 9 subset of 15); guardian develop {qxg6, xp26} -> head empty; kyc same. Controls for the zeros: the develop locks themselves show the ids in both instruments (different families: registry bulk endpoint vs npm audit tree walk).

Q3 What moved (holds). Parsed every package entry in all 26 locks: 463 version changes: 412 patch dev, 44 minor dev (the 4 above, repeated across locks), 7 patch non-dev (dompurify and ip-address in frontend/issuer and the root; ip-address in packages/shared, services/anchoring, services/mcp-server). Zero major, zero non-dev minor. No newly added hasInstallScript on any changed or added package. Non-registry resolved hosts: only the root lock's `@secuura/*` workspace links (resolved = local path, as before). Floor lock (guardian): 31 changed = 9 vitest family + 22 side effects (vite 8.3.4 -> 8.3.5, rolldown 1.2.14 -> 1.2.15 + 15 bindings, @oxc-project/types, chai, std-env, tinyrainbow, nanoid 3.3.19 -> 3.3.20), all dev, 0 added, 0 removed. Lock-only lock (staking): 9 changed (8 vitest-family + `vitest/node_modules/picomatch` 4.0.5 -> 4.0.7, dev, vitest declares `^4.0.3`), none added/removed, no rolldown/vite change. frontend/issuer: 10 changed, vite NOT moved. Referral: 30 changed = 9 + 21 side effects (matches claim). Root: 2 added (hoisted `@vitest/coverage-v8` 4.1.12, its nested `@bcoe/v8-coverage` 1.0.2) and 30 removed (15 nested per-workspace `@vitest/coverage-v8` 4.1.11 + 15 nested `@bcoe/v8-coverage`), matching the "15 copies collapse into one" oddity; the surviving entry is dev, no install script, peer vitest 4.1.12.

Q4 Installability (holds). Clean exports of the head, `npm ci --ignore-scripts --dry-run`, host npm 11.5.1: root rc 0 (1910 packages), services/guardian rc 0 (244), services/security rc 0 (260), services/referral rc 0 (576), frontend/issuer rc 0 (720); stderr empty on all. Negative control: see N2 (rc 1 and rc 2, both fail). A real `npm ci --ignore-scripts` of the root (1910) and of three standalone locks also succeeded on each side (below).

Q5 Standalone suites (partial, holds on what ran). Each service copied from `git archive` of each side to an isolated directory outside the monorepo (no hoisting), own `npm ci --ignore-scripts`, `@secuura/shared` built from that side's own packages/shared (own `npm ci` + `tsc`) and symlinked in. Installed vitest asserted: head 4.1.12, develop 4.1.11. vitest JSON reporter, keyed (file, fullName):
- services/security: develop 354 total / 350 pass / 4 fail; head 354 / 350 / 4; distinct 354 = 354, vanished 0, new 0, status changes 0 (the same 4 red, see N1).
- services/guardian: 1/1/0 both sides, 0 vanished, 0 new.
- services/kyc: 34/34/0 both sides, 0 vanished, 0 new.
Comparator control: planted removal of one key is detected (vanished = 1). My first comparator run reported false "34 vanished" because file keys embedded the side's directory name; I fixed the key and reran before relying on it.

Q6 Claim accuracy. (a) "26 locks moved, 20 byte-identical": holds. 46 tracked package-lock.json in the tree; 26 differ, 20 have identical blob shas on both sides (`ls-tree` comparison). (b) "22 manifest lines": holds as 22 insertions / 22 deletions (N3). (c) Suite table rows: guardian 1/0 holds, kyc 34/0 holds (standalone), security 361/0 does not reproduce standalone (354 total, 4 environmental red, identical both sides; N1). Also verified: "referral and vc-issuer carry 21 side-effect packages" (referral 30 - 9 = 21), "22 in the floor locks" (guardian 31 - 9 = 22), staking picomatch, root collapse of 15.

Q7 Not covered. See NOT RUN.

## NOT RUN
- The other 22 standalone suites, and the full hoisted-install suites (author's 5359-test comparison not re-run; only security, guardian, kyc standalone).
- security's 7 tests only reachable in the hoisted repo layout (4 files that read repo-level paths).
- frontend builds, image builds, deploy, jest, integration, schemathesis, k6, Playwright, Akto, and the three pre-push legs needing a local stack (3, 4, 8) which the author also reports skipped.
- Docker (forbidden); I could not use node:24-alpine / npm 11.19.0 so my installs are on host npm 11.5.1. The author's 26/26 Docker dry-runs were not repeated (only 5 of 26 locks dry-run here).
- PR check state (GitHub Actions) and the KS-1707 comment: read nothing from GitHub/Linear.
- No lock was regenerated; I did not test determinism of the author's regen method.

## Wall-clock
About 10 minutes by the shell clock (07:24:50 to 07:31), end-of-run ls-remote: develop f75b52721dad, PR head b697e5b63ede, both unchanged from the start. `git -C /Volumes/DevMASTER/WEDNESDAY status --short` shows no untracked path outside 0_Brain/, 5_Project_History/, 2_Project_Files/local-model/, 2_Project_Files/fleet/briefs_staged/. All scratch lives under the session scratchpad `gate_da1/`.
sha256 of `sed '1d;$d' verdict.md | shasum -a 256`: 7413f6543f0c4ef06b468e71050dfb2a93ff07d1fd1df9b84f1380d6781234c1
