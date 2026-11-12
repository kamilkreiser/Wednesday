GATE B1547: GO WITH FINDINGS @ b3d1a6f on main 9c8d2cd
Tier G2, class dependency-override, round 1 of 2. Clock from `date`: 20:58 to 21:06 AEDT 2026-11-12. Project Security Composer (datasecau/Datasec-Security-Composer), branch `b1547/composer-minimatch-alert-28` = b3d1a6f2c41ede22dfc9dbeb30593196973b47c1. Findings: Blocker 0, Major 0, Minor 3, Info 2. No security-shaped issue found. Work folder: /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s274/g1547/ (own clone, push URL set invalid, never pushed).

## Findings
| # | Class | Where | Finding |
|---|---|---|---|
| F1 | Minor | builder evidence squash-body.txt (last line), pr-body.txt (last line) | Neither carried the required closing line (`Co-Authored-By: Claude Opus 5.5 ...`, `Generated with [Claude Code]`). Corrected copies are in this folder. |
| F2 | Minor | builder evidence landing.txt lines 7 and 9 | Says "product owner's card" (a card word) and quotes CLARIFICATIONS.md:689 as the squash rule. Line 689 (project CLARIFICATIONS.md) says "merged head-pinned as Composer origin main" and "Not deployed"; it does not say squash. Squash is the recorded practice at lines 157, 182, 582, 855. Corrected landing.txt here states head-pinned squash without the card wording. |
| F3 | Minor | commit b3d1a6f message trailer | Trailer is `Co-Authored-By: Claude Sonnet 5.5`; the squash body replaces the commit message on merge and carries the standard Opus 5.5 line, so no action. |
| I1 | Info | package-lock.json, 3 added lines `"url": "https://github.com/sponsors/isaacs"` | Builder note (a): TRUE and HARMLESS. It is the `funding` metadata field of each new minimatch 11.0.1 entry; the removed 10.2.6 entry carried the identical field (diff lines `-"url": "https://github.com/sponsors/isaacs"`). It is not a `resolved` host; install never fetches it (only `npm fund` prints it). Every added `resolved` (4 lines) is registry.npmjs.org. |
| I2 | Info | npm 10.9.8 `npm ls minimatch --all` at head | Builder note (b): TRUE, measured. rc 1, `ELSPROBLEMS`, `invalid: minimatch@11.0.1 ... @eslint/config-array/node_modules/minimatch` against its declared `^10.2.4`; at base the same command is rc 0. Harmless to the project: the only `npm ci` users are docker/Dockerfile:26 and scripts/ci.sh:118 (the `docker build` of it); no `npm ls`/`npm list` in scripts/, docker/, compose.yaml, package.json, workspace manifests (recursive grep over the tree minus node_modules and docs: the only `npm ci` hits are those two lines, 0 `npm ls`; control: the same grep finds `npm ci` 2). There is no `.github` directory at head, so no hosted workflow runs it. |

## Claims checked
1. Diff = exactly two paths (package.json, package-lock.json): TRUE (`diff --stat`: 2 files, +66 -16; 1 commit, 0 behind). Manifest change = only the `overrides` block, 8 added 0 removed: TRUE (numstat 8 0). Lock +58 -16: TRUE.
2. Lock written by npm, reproduced: with drive-local node v24.22.2 / npm 11.19.1, `npm install --package-lock-only --ignore-scripts`. No-change control on main's files: rc 0, lock blob 39a36218569c8fc535a5e4eb24b3024de9ac878e = main's blob (control passes, so the tool is stable). On main's files plus head's package.json: rc 0, lock blob **0fabc670e1b9aadf275a51e9c5044c32cd2d19a4 = head's blob**, package.json blob ccfb0bf0... = head's. TRUE.
3. Exactly the five predicted entries (by key, parsed JSON): ADD eslint/node_modules/minimatch 11.0.1, ADD @eslint/config-array/node_modules/minimatch 11.0.1, ADD @typescript-eslint/typescript-estree/node_modules/minimatch 11.0.1, ADD @isaacs/nonrecursive-glob-match 1.1.0 (dev), DEL node_modules/minimatch 10.2.6; no other key differs; 348 -> 351: TRUE.
4. Every minimatch entry at head outside `>= 7.0.0, < 11.0.1`: 4 entries (5.1.9 under @redocly/openapi-core unchanged, three 11.0.1), 0 in range; control: base has 1 in range (10.2.6): TRUE.
5. `resolved` on added entries: 4 of 4 registry.npmjs.org, non-registry 0. Integrity: `npm view minimatch@11.0.1 dist.integrity` = sha512-t+Vn6DX4...RZoLQ== and `@isaacs/nonrecursive-glob-match@1.1.0` = sha512-GPm/Dbvk...PfDfw== both EQUAL the lock; tarball URLs equal; licenses BlueOak-1.0.0 equal; minimatch 11.0.1's registry dependencies (brace-expansion ^5.0.12, @isaacs/nonrecursive-glob-match ^1.0.1) equal the lock entry and are satisfied by hoisted brace-expansion 5.0.12: TRUE.
6. In the pinned image (node v22.23.2, npm 10.9.8): `docker build --target ci` (npm ci from the lock) rc 0 at head and base. Installed copies on disk, measured: head has minimatch 11.0.1 at eslint/, @eslint/config-array/ and @typescript-eslint/typescript-estree/ node_modules and 5.1.9 under @redocly/openapi-core (resolution from eslint and typescript-estree directories prints 11.0.1; config-array's package.json is not exported so its resolution was checked by directory listing only); base has hoisted 10.2.6 only. minimatch 11.0.1 matches (`**/*.ts` true on a.ts, false on a.js). TRUE.
7. Evidence: no names (ban list 0 in added lines, commit message and all six evidence files; control `x_by_Kam_y` fires 1), no B-numbers/seat ids/card ids in pr-title, pr-body, squash-*, ticket-text (the only B-like token is the branch ref `b1547/...` in landing.txt, the real ref name), 0 non-ASCII bytes, 0 UUIDs. Alert coverage statements true: alert 28 open now, 15 others open (fast-uri 8, fastify 1, ip-address 1, undici 5; read via `gh api -X GET`), advisory GHSA-g3hv-75wg-m249, range `>= 7.0.0, < 11.0.1`, patched 11.0.1, scope development: TRUE. Builder's "registry read, 0 stable versions declare 11.x" and audit 14 -> 4: not re-run by me (NOT TESTED below).

## What I ran (my own clone/archives; the builder's trees/scripts unused; `--network none` for all test containers; heavy lock taken and released)
Images built from the base and head trees by me: `pc-g1547-node:base|head` (ci target, rc 0 both), `pc-g1547-web:head` (rc 0).
| Check | base 9c8d2cd | head b3d1a6f |
|---|---|---|
| `npm run lint` | rc 0 | rc 0 (non-vacuous: a planted unused-var file fails rc 1 at head) |
| `format:check` | rc 0 | rc 0 |
| `typecheck` | rc 0 | rc 0 |
| `build` | rc 0 | rc 0 |
| whole vitest (JSON) | 315 files, 3177 tests: 3174 passed, 2 failed, 1 skipped | identical |
| compare by (file, test, status) | - | lost 0, changed 0, added 0 (control: flipped+dropped row gives changed 1, lost 1) |
| the 2 failed | packages/content/src/citations.test.ts, both at base and head (needs the withheld source text) | same |
| `scripts/test-db.sh` (packages/db) | 39 files, 674 passed | 39 files, 674 passed |
| `scripts/test-db.sh` (apps/api db) | 83 files, 1563 passed | 83 files, 1563 passed |
The DB runs were compared by counts from the runner text (all passed, rc 0), not by test name. Merge: `git merge-tree --write-tree 9c8d2cd b3d1a6f` rc 0, tree de561f6a... = head's tree; main unmoved (ls-remote 9c8d2cd), so merge = head and no separate merge run. Open PRs: only #85 (draft, 57 files, 0 files named package.json or package-lock.json; control regex matches `apps/x/package.json`): overlap 0. No `.github` at head (no hosted test workflow, no deploy-demo-style trigger); check-runs on the head: 0 (no PR yet). Scans over the 66 added diff lines: hosts only registry.npmjs.org (4) and github.com/sponsors (3); `new RegExp`, innerHTML, child_process, chmod, secret-like words 0; JSON only, no code, so no new CodeQL query input.

## NOT TESTED
- Hosted CodeQL on the PR head (no PR yet; Tuesday reads it after opening).
- The compose-stack, .NET bridge and egress parts of scripts/ci.sh, and ci.sh as a whole (it reads withheld source text); this change touches nothing they read.
- Registry-side claim "0 of 381/20/415 stable versions declare 11.x" and `npm audit` 14 -> 4 (builder claims; not re-measured by me). Secret-scan script (I ran regex scans instead, 0 hits).
- DB suites compared by count, not by name. A future in-image `npm install` with npm 10.9.8 (builder says it rewrites 27 optional entries; I did not run it). Playwright/browser tests.

## FOR TUESDAY
- Open the PR from `pr-title.txt` and `pr-body.txt` in /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-12_B1547_verify/; read hosted code scanning on the head; land with `landing.txt` (head-pinned squash; replace N; paths absolute). Land only if main is still 9c8d2cd.
- After landing, read open Dependabot alerts: 28 should be gone, 15 remain by design.
- Use my corrected `squash-body.txt` and `pr-body.txt` (the builder's lacked the closing lines).
- Known quirk to expect: `npm ls minimatch --all` under npm 10.9.8 reports ELSPROBLEMS at head; nothing in CI runs it. Override removal condition is in pr-body.txt.
- Resources: images `pc-g1547-node:base`, `pc-g1547-node:head`, `pc-g1547-web:head` removed by exact name (containers 0, images 0 after; control: 3 untagged lines printed on removal). `scripts/test-db.sh` creates its own `pc-dbtest-*` network/containers/volumes and removed them (0 left). Heavy lock was mine (holder file shows g1547) and is released to /Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s274/g1547/quarantine/composer-heavy.lock.released; `.tools/` has 0 heavy entries now. Scratch HOME for npm view: /private/tmp/g1547home. Ports used: none. Outside-the-fences: git clone/fetch/ls-remote with the project deploy key (no push), `gh api -X GET` reads, `npm view` (registry.npmjs.org) and registry installs from the containers' image build; no az, Jira, mail, PR action.
