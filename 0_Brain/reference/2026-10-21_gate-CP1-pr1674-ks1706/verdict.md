VERDICT: GO WITH NOTE at head 827878479f87abc10cb31fd418c45da3eeff5ed3 (tier 1, round 1 of 2; landing tree 650837653068d267eba9eaabe62c5b04d3abc86a on develop 5671d5115921cae656c6c598741d9e9a87cbeeeb; 0 blockers, 5 notes)

## BLUF

PR #1674 does what it claims. Both repo gates go from rc 1 (the same ten GHSA ids) on develop to rc 0 on the head. A second instrument, `npm audit --package-lock-only`, agrees on the root lock and on two standalone vite-8 locks: none of the ten ids is left, and no new id shows up. The diff is exactly 34 M files: 31 locks plus 3 one-line vite pins. All 39 changed or added name@version entries match the registry's integrity and tarball URL. No new install scripts, no host other than the npm registry, no true major bumps. frontend/admin builds on both sides with 20 files each. auth, shared and billing vitest give identical results by test name. No blocker. The notes are follow-ups, not reasons to hold the merge.

## Heads (ls-remote, start 16:59 and end 17:08 AEDT)
- refs/pull/1674/head = branch head = 827878479f87abc10cb31fd418c45da3eeff5ed3 (both reads)
- develop = 5671d5115921cae656c6c598741d9e9a87cbeeeb (both reads; develop did not move, so no lock moved on develop since 5671d5115921)
- Landing tree: `git merge-tree --write-tree develop head` = 650837653068d267eba9eaabe62c5b04d3abc86a (rc 0, no conflict). This equals the head's own tree and the author's prediction.

## Findings by question

**Q1 Scope: HOLDS.** 1 commit, parent 5671d5115921, 0 merge commits. `diff --name-status` gives 34 M: 31 `package-lock.json` plus services/{analytics,auth,shared}/package.json. Each manifest diff is only `"vite": "7.3.6"` -> `"7.3.7"`. `git diff --quiet develop head -- Blockchain/Dev/scripts` rc 0, so the audit baseline and audit scripts are untouched. No path matching baseline|hook|husky|scripts/|.sh in the diff.

**Q2 The freeze clears, and for the right reason: HOLDS.**
- Instrument 1. `audit:gate` runs `npm audit --json` at Blockchain/Dev, which resolves the hoisted root tree from the root lock, and diffs the result against scripts/audit/audit-baseline.json. `audit:locks` reads every tracked standalone lock's `packages` map (44 = 46 tracked - root - mobile out of scope), POSTs exact versions to the registry bulk-advisory endpoint, and diffs against the same baseline.
  - develop: gate rc 1 (19 reported, 10 NEW). locks rc 1 (17 match, 10 NEW). Same ten ids in both: GHSA-22jm-h49p-29qw, -6prh-2h8m-c8cw, -46jr-4wx8-v453, -rvq5-wwqv-78pq (MCP SDK), -q3jh-wrc6-jgq8, -8r9p-f939-6h3c (follow-redirects), -5r4p-p66f-jhc7 (hono), -698v-4r3x-3vcv, -r825-w8mm-5pxw, -587h-7wmj-h5pm (vite/launch-editor).
  - head: gate rc 0 (9 reported, all baselined). locks rc 0 (7 match, 7 baselined).
- Instrument 2, a different family. `npm audit --package-lock-only --json` on the root lock in place. The standalone locks frontend/admin and services/billing were COPIED to isolated dirs, because in place npm audits the hoisted tree. Advisory id sets, develop -> head:
  - root 19 -> 9; admin 9 -> 4; billing 3 -> 0.
  - The ids found only on develop are exactly the ten (root 10/10, admin 5, billing 3). These develop counts are the positive control.
  - Ids only on the head (NEW): 0 in all three.
  - All 9 remaining root ids and all 4 remaining admin ids are in the baseline.

**Q3 What moved: HOLDS, no supply-chain flag.** Tool: my own node lock differ, keyed by package path.
- ROOT: 27 changed, 1 added, 0 removed.
  - vite 7.3.6->7.3.7.
  - Nested vite: frontend/{admin,issuer,verifier,website} 8.2.1->8.3.4 and {demo-overlay,outlook-addin} 6.4.3->6.4.4.
  - @modelcontextprotocol/sdk 1.31.0->1.32.1 (minor); follow-redirects 1.16.0->1.16.1; hono 4.13.8->4.13.13; picomatch 4.0.5->4.0.7.
  - rolldown and 14 @rolldown/binding-* 1.2.4->1.2.14 (patch); @oxc-project/types 0.144->0.154.
  - Added: @rolldown/binding-android-arm-eabi@1.2.14 (optional, dev).
  - One same-version entry, rolldown/node_modules/@rolldown/pluginutils@1.0.1, GAINED resolved+integrity that it lacked before. Both equal the registry.
- services/analytics and services/auth: 1 changed each (vite 7.3.6->7.3.7, patch), 0 added, 0 removed.
- frontend/admin: 33 changed, 1 added, 7 removed.
  - vite 8.1.4->8.3.4 and rolldown 1.1.5->1.2.14 (minor), with 14 bindings.
  - lightningcss 1.32.0->1.33.0 with 11 bindings; postcss 8.5.26->8.5.31; nanoid 3.3.18->3.3.20; picomatch 4.0.5->4.0.7; follow-redirects 1.16.1; @oxc-project/types 0.139->0.154.
  - Added: @rolldown/binding-android-arm-eabi@1.2.14.
  - Removed: @rolldown/binding-wasm32-wasi@1.1.5 and its wasm chain (@emnapi/core, @emnapi/runtime x2, @emnapi/wasi-threads, @napi-rs/wasm-runtime, @tybys/wasm-util).
  - Registry check: rolldown 1.1.5 lists wasm32-wasi and not android-arm-eabi; 1.2.14 is the reverse. Both list 15 optional bindings. The swap is upstream's.
- Across all 31 locks:
  - badHost 0 and newInstallScript 0.
  - lockfileVersion and name unchanged everywhere.
  - No MAJOR change anywhere. The only semver-breaking-class moves are @oxc-project/types 0.x (25 locks; see N3).
  - demo-overlay also drops yaml@2.9.0.
- Positive control: a mutant admin lock with one resolved URL set to evil.example.com and hasInstallScript planted on rolldown. The differ reported badHost 1 and newInstallScript 1.

**Q4 Installability: HOLDS.**
- `npm ci --ignore-scripts --dry-run` rc 0 on the head for:
  - the root, as a clean `git archive` of Blockchain/Dev ("added 1938 packages");
  - services/auth, services/analytics, services/shared and frontend/admin, each as its own package.json+lock in an isolated dir.
- Negative controls:
  - auth manifest put back to 7.3.6 against the 7.3.7 lock: rc 1, EUSAGE "lock file's vite@7.3.7 does not satisfy vite@7.3.6".
  - root with services/shared put back to 7.3.6: rc 1, EUSAGE "Missing: vite@7.3.6 from lock file".
  - Restore asserted by sha256: 006ec490df337cb2... equals the git blob at the head. The re-run after restore gave rc 0.

**Q5 Build and test where the author did not run: HOLDS.**
- (a) frontend/admin, built Dockerfile-shaped: its own lock, frontend/shared as vendor/shared, SHARED_DIR=./vendor/shared/src, `npm ci --ignore-scripts`, then `tsc && vite build`.
  - develop: vite 8.1.4, rc 0, 20 dist files. Head: vite 8.3.4, rc 0, 20 dist files.
  - The file NAMES are identical except two content hashes (auth-*.js, index-*.js), which a toolchain change is expected to produce.
  - The head prints one new vite warning (see N2).
  - --ignore-scripts was safe here: the only hasInstallScript entry in the lock is fsevents.
- (b) services/auth and services/shared vitest, run under the root workspace install (`npm ci --ignore-scripts`, then packages/shared `npm run build` because auth's vitest aliases packages/shared/dist). Hoisted vite: develop 7.3.6, head 7.3.7.
  - auth: 1137 tests on each side; 1135 pass / 2 fail on both. By name: 0 new reds, 0 vanished, 0 appeared.
  - shared: 11/11 pass on each side; 0 differences.
  - The 2 auth failures are the same on both sides and come from the isolation shape: ENOENT on the repo-root CLAUDE.md and a seed-site enumeration outside the archived subtree.
  - Comparator control: a mutant head JSON with one pass flipped to fail and one test deleted. It reported newRed 1 and vanished 1.
- (c) services/billing on vite 8.x via vitest, from its own lock in isolation (vite 8.3.0 -> 8.3.4, rolldown 1.2.9 -> 1.2.14, vitest 4.1.11).
  - 49 tests on each side; 42 pass / 7 fail on both; 0 differences by name.
  - All 7 failures are db.retry.test.ts with "Cannot find package '@secuura/shared'", an artefact of the isolation shape that is the same on both sides.

**Q6 Claim accuracy: the numbers I checked hold.**
- "31 locks": 31 package-lock.json in the diff. HOLDS.
- "+2258/-2360": `--shortstat` gives 34 files, 2258 insertions, 2360 deletions. HOLDS.
- "39 of 39 integrity": independent check, every changed or added name@version across the 31 locks against the registry's `dist.integrity` and `dist.tarball`. Result 39 distinct, 39 equal, 0 mismatch. Positive control: a mutant with one bad integrity and one bad resolved URL gave 2 MISMATCH. HOLDS.
- Also hold:
  - admin "20 dist files";
  - "cross TWO vite minors 8.1.4 -> 8.3.4" for admin, verifier and website (issuer is 8.3.1->8.3.4);
  - "lightningcss 1.33 with 11 bindings", MCP SDK 1.32.1, hono 4.13.13, follow-redirects 1.16.1;
  - "15 bindings" for both rolldown versions;
  - 20 service locks move rolldown (25 locks in total, counting the root and 4 frontends).
- The claim says "no baseline build to compare". I supplied one: develop gives 20 files, the same as the head.
- I found nothing the claim states as measured that the head does not support.
- PR body: NOT readable. There is no gh auth in my shell, and I did not borrow a token or write anything. Instead I read the commit message: "Refs KS-1706" present, 0 closing-keyword matches (keyword-scan control: "Closes KS-1706" matches).

## Notes (none blocking)
- N1: The head's 9 remaining root advisories are all baselined. But 6 of those baseline rows expire on 2026-10-31 (react-router x2 KS-528, deepmerge-ts KS-664, sprintf-js KS-1425, postcss-selector-parser KS-1425, braces KS-1403). If those tickets do not close, the gates will freeze again in about 10 days. This is outside this PR, but it is the next freeze.
- N2: The admin build on vite 8.3.4 prints a new warning: "config uses features unsupported by configLoader: 'native'" (`__dirname`, vite.config.ts:34). It is cosmetic now and becomes a future-major item.
- N3: @oxc-project/types moves 0.139/0.144/0.150/0.151 -> 0.154 in 25 locks. That is semver-breaking class (0.x minor). It is a types-only transitive of rolldown, and the builds and tests above are green.
- N4: The 15 CLEANUP baseline rows (undici x13, ip-address, @hono/node-server) print the same on develop and on the head. They predate this PR. Agree with the author: they need a ticket.
- N5: I could not read the PR body (see Q6). Wednesday should confirm "Refs, never Closes" on the body herself.

## FOUND / TESTED / HOW
- FOUND: 0 blockers. Scope exact. Freeze cleared by version moves, not by baseline edits. No new advisory ids, no install-script or registry-host drift. Build and tests show no regression.
- TESTED: Q1-Q6 as above. Every zero has a control from a different family: the develop-side advisory sets, the EUSAGE negative installs, and mutant locks and mutant test JSON fed to my own tools.
- HOW:
  - Scratch clone `git clone --shared` at .../scratchpad/gate_cp1/src. GitHub fetch via the cache's deploy-key sshCommand, used read-only.
  - Detached worktrees for develop and head. Isolated `git archive` copies for builds and tests.
  - npm 11.5.1, node v24.7.0, darwin. All npm runs used `--prefix` inside the scratch dir.

## NOT RUN
- Builds of frontend/verifier, website, issuer, demo-overlay and outlook-addin. The author built verifier and website; I did not rebuild them.
- Vitest for services/analytics and for any of the ~19 other vite-8 service suites besides billing.
- Any backend `tsc` build beyond packages/shared.
- Dry-runs for the remaining 26 locks. The author's Docker dry-runs cover them; not re-measured.
- akto, linux/musl installs, image builds, Docker (forbidden), deploy, preflight.
- The "29 optional edges with no lock entry" claim.

## Wall-clock
16:58:49 -> about 17:10 AEDT, roughly 12 minutes.

## Stray-file check
`git -C /Volumes/DevMASTER/WEDNESDAY status --short` shows untracked paths only under 0_Brain/reference/ (this folder) and 2_Project_Files/local-model/night/ (pre-existing). Nothing is outside the allowed prefixes, and I wrote nothing outside the scratchpad except this file.
sed '1d;$d' verdict.md | shasum -a 256 = 963d677382f7da8b04749e0dd994d519ae3e675a41a59e7cecb79c973d8bccb1
