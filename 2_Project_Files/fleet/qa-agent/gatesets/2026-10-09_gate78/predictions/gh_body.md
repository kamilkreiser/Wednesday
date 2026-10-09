Refs KS-1452 https://linear.app/secuura/issue/KS-1452

## What and why

`handlebars` 4.7.9 -> 4.7.10 in five `package-lock.json` files, nothing else. Three advisories published 2026-10-08T17:52Z make pre-push preflight legs 6 (npm-audit) and 7 (standalone-lock advisories) refuse **every** push on develop `1e7f90e26137`:

| Advisory | Severity | Vulnerable |
| -- | -- | -- |
| GHSA-8r5x-fm3f-whwj | critical | >=4.0.0 <=4.7.9 |
| GHSA-p8wg-vrv2-v86f | critical | >=4.0.0 <=4.7.9 |
| GHSA-xw65-4hp5-5hc7 | moderate | >=4.0.0 <=4.7.9 |

4.7.10 clears all three (npm bulk advisory endpoint: 4.7.9 returns the three, 4.7.10 returns `{}`), is `latest`, and is the only release above 4.7.9.

## The change: 5 locks, 5 entries, 18 field writes

| Lock | Fields written |
| -- | -- |
| `Blockchain/Dev/package-lock.json` (workspace root, leg 6) | `version`, `dependencies.minimist` (the root entry carries no `resolved`/`integrity`) |
| `services/governance` | `version`, `resolved`, `integrity`, `dependencies.minimist` |
| `services/originate` | `version`, `resolved`, `integrity`, `dependencies.minimist` |
| `services/referral` | `version`, `resolved`, `integrity`, `dependencies.minimist` |
| `services/vc-issuer` | `version`, `resolved`, `integrity`, `dependencies.minimist` |

* Not version-only: 4.7.10 itself moves `dependencies.minimist` from `^1.2.5` to `^1.2.8`. Every lock already resolves minimist 1.2.8, so no other entry moves.
* In range: all 7 declaring parents say `^4.7.9`. **0 manifests, 0 `overrides`, 0 baseline rows, 0 source.**
* `integrity` is the sha512 of the downloaded 4.7.10 tarball (712,317 B), equal to the registry's `dist.integrity`; the same pipeline reproduces the 4.7.9 value the locks carried.
* Built surgically from a plan derived from the files and the registry (not hand-listed); a host-npm regen of each standalone lock was the cross-check (below).

**WHY per changed line:** a JSON lock cannot carry a comment, so this description and the commit message are the WHY for every changed line (test-discipline §5d).

**No platform-doc change:** test-discipline §4 binds a test change (backend unit, integration or systemTest). This PR changes no test, so neither `Projects Documents/API_Security_Functional_Testing_Architecture_Flow_Diagrams.html` nor `QA_Tool_Cheat_Sheet_Secuura_API_Testing.html` moves.

## Runtime reach

| Service | handlebars at runtime? | Evidence |
| -- | -- | -- |
| originate | **yes**, 4.7.10 after this PR | direct prod dependency; runner `npm ci --ignore-scripts --omit=dev` from its own lock (`services/originate/Dockerfile:79`); isolated `npm ci --omit=dev` from the committed lock installs 4.7.10 |
| governance | no | `npm prune --omit=dev` before the runtime copy (`:54`); isolated `--omit=dev` install: absent |
| referral | no | `npm prune --omit=dev` (`:61`); isolated `--omit=dev` install: absent |
| vc-issuer | no | runner `npm ci --omit=dev` (`:86`); isolated `--omit=dev` install: absent |
| Dev root lock | no image | 0 Dockerfile references (control: `package-lock.json` 8) |

0 files in the repo import or require handlebars (controls: express 339, ts-jest 14). originate's unused direct declaration is filed separately as KS 1453 and is **not** touched here.

## Test Evidence

**Touched:** the five `package-lock.json` files above. Nothing else (path set asserted: exactly these 5).

**Ran (all local, on this head's tree):**

* Leg 6 `node scripts/audit/audit-gate.mjs`: develop rc 1 naming the three; this branch rc 0, the three named 0 times (control: the same output names 15 other GHSA ids). `audit-gate: 9 distinct advisories reported, 24 baselined.`
* Leg 7 `node scripts/audit/audit-locks.mjs`: develop rc 1, each `pinned: 4.7.9 … in 4 lock(s)`; this branch rc 0, 0 mentions.
* Leg 2 `scripts/preflight/lockfile-cleanroom.sh`: rc 0, "All 35 standalone lock(s) pass clean-room npm ci."
* `npm run audit:contract`: tests 59, pass 59, fail 0 (= `expected-case-count` 59).
* Semantic differ (independent of the editor's own check): exactly the 18 planned (entry, field) writes; key order and indent-2 round-trip equal; with the handlebars entry masked, every lock is byte-identical to develop.
* Negative controls, each on a scratch copy and restored sha-verified: the root entry back to 4.7.9 reddens leg 6 (leg 7 stays green); originate's standalone entry back to 4.7.9 reddens leg 7 (leg 6 stays green); a stale `minimist ^1.2.5` on one entry makes the differ fire.
* Parse census over all 45 tracked locks: 0 handlebars entries <= 4.7.9; exactly 5 at 4.7.10. `audit-baseline.json` blob `4af041e8d74a` and the `mobile/secuura-app` lock unchanged.
* Regen cross-check (host npm 11.5.1, node v24.7.0, isolated dir with no workspace root, handlebars entry removed and re-resolved): all four standalone entries moved to 4.7.10 and equal the committed entry on version/resolved/integrity/dependencies/dev/license/engines/bin. The regen also churned unrelated optional platform bindings (up to 10 entries), which is why it was a cross-check, not the build.
* Installs: `npm ci --ignore-scripts` rc 0 on the root and on each standalone lock in isolation (lock byte-unchanged, handlebars 4.7.10 installed).
* `services/originate` `npm run build`: rc 0.
* Unit suites: governance 115/115 (4 suites), originate 1,093/1,093 (96 suites), referral 34/34 (7 files), vc-issuer 159/159 (17 files).
* In-hook pre-push preflight on this push: `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` Legs 3, 4 and 8 skipped (local stack not up), so this is **not** a pass of all 15. Ran and passed, quoted from the push log: leg 2 `OK — all locks clean-room-installable`; leg 5 `OK — 59 audit-contract cases pass (expected 59)`; leg 6 `audit-gate: 9 distinct advisories reported, 24 baselined.` / `OK — no advisories outside the triaged baseline.`; leg 7 `OK — no standalone-lock advisories outside the triaged baseline.`; leg 14 `shell suites: 71 passed, 0 failed, 0 skipped (of 71)`; leg 15 `OK — 13 code guards passed.`

**NOT run:** the four platform suites (Schemathesis, Akto, Playwright, k6), image builds, any live or demo sweep — there is no local stack and Docker is down. No deploy.

**Migrations / config:** none.

## Not done here

* No baseline row. Leg 6's 15-entry CLEANUP advisory block stays out (disposition KS 767).
* The originate declaration (KS 1453): not built.
* This PR ends at READY FOR QA (tier 1, security); the merge is a later seat's, on a gate.

Precedent: the same in-range lock-refresh shape as KS 1437 (#1406) and KS 1425 (#1397).

🤖 Generated with [Claude Code](https://claude.com/claude-code)
