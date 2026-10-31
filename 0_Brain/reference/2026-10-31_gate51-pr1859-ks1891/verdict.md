# QA GATE 51: Secuura/Blockchain PR #1859 (KS-1891, Seat E 22nd), Tier 1, Round 1
**Head gated: 8f3181e35248715f7800a976cf8c0d30a159a2ac**, on develop **9e1eb55fde5338d0ad95848736cbd013d7b7f651**. Both were read with `ls-remote` (refs/pull/1859/head and refs/heads/develop) before the fetch and again from FETCH; neither had moved. merge-base equals the develop tip, so the PR sits directly on develop.

## VERDICT: GO WITH NOTES. Nothing needs fixing before merge.
The forced majors have exactly two production runtime consumers in shipped services. Both were exercised at head and both work. Every break caused by minimatch 11 is in dev tooling only (jest internals, babel-istanbul and ts-node-dev's rimraf). None of those breaks is reached by the configs or scripts the repo runs today (F2, F3).

| File(s) | Change | Gated |
|---|---|---|
| 106b1f4f3: 7 locks (admin, issuer, verifier, root, api-gateway, kyc, systemTest/akto) | follow-redirects 1.16.1 -> 1.16.2. Only the version, resolved and integrity lines change, 7 of each | yes, line-level diff |
| 8f3181e35: 17 package.json | `overrides.minimatch: ^11.0.1` in all 17. `"glob@>=9.0.0 <=14.0.1": "^14.0.2"` in root, anchoring and nft-certificate. Anchoring's old `minimatch ^5.1.6` override is replaced | yes, full diff read |
| 8f3181e35: 17 locks | regenerated | yes, every changed install path in all 19 changed locks |
| governance/jest.config.js, originate/jest.config.js, originate/jest.integration.config.js | `coverageProvider: 'v8'` and a one-line comment in each, +2 lines per file | yes |
| Total | 39 files, +389/-849. Matches E's mail. No docs or code files | yes |

### (1) Lock integrity
Instrument: `probes/lockdiff.py` (mine, independent of E's prover). It runs `git show` of base and head for every changed lock, compares (version, flags, integrity) per install path, and classifies each change by its parents. Output: `probes/lockdiff.txt`.
- All 19 changed locks were covered, not a sample. Every changed path is glob, minimatch or follow-redirects, or a package that hangs only under them:
  - brace-expansion and balanced-match;
  - @isaacs/nonrecursive-glob-match (a new dependency of minimatch 11.0.3);
  - path-scurry and lru-cache;
  - jackspeak, @isaacs/cliui and foreground-child;
  - cross-spawn, which, isexe, path-key, shebang-*, signal-exit and concat-map. These were removed with glob 11 or minimatch 3.
- The only entries the classifier flagged were in the root lock, and all are explained:
  - `foreground-child` 3.3.1 and its `signal-exit` 4.1.0 have **flag-only** changes (now devOptional): same version, same integrity. E disclosed this.
  - `lru-cache` moved: 11.5.1 was removed from under rimraf/ and node-pg-migrate/, and 11.5.3 was added under path-scurry/. path-scurry 3.0.0 declares `lru-cache ^11.0.0`, and path-scurry only comes in with glob 14.
- **No unrelated package changed version.** The dependency sections of the root lock entry are identical in base and head.
- Every new or changed head entry (54 in total) resolves from registry.npmjs.org and has a sha512 integrity.
- `npm ci --ignore-scripts` gave rc 0 on root, mcp-server, anchoring, nft-certificate, governance, originate and packages/shared.
- `npm ls glob minimatch follow-redirects --all` on root gave rc 0 with 0 invalid or UNMET lines. It shows glob 14.0.3 x3, minimatch 11.0.3 x16 and follow-redirects 1.16.2 x2.
- `npm ls --all` gave rc 0 on nft-certificate, governance and originate. The full root `npm ls` exits 1 only on UNMET OPTIONAL platform binaries (cbor-extract, dcspark).

### (2) Advisories
- **At head:**
  - `audit:gate`: rc 0, 10 advisories reported, all baselined. CLEANUP names the braces row, as expected.
  - `audit:locks`: rc 0, 44 standalone locks, 8 matched, all baselined.
  - None of the three GHSA ids appears in either output or in `audit-baseline.json`, so rc 0 is not coming from a baseline row.
- **Positive control on base** (worktree at 9e1eb55):
  - `audit:gate`: rc 1, 13 reported, with all three GHSAs listed as new.
  - `audit:locks`: rc 1, "FAIL — 3 advisories … NOT in the baseline", with all three listed. GHSA-mrwp is shown in 6 locks.
- **Independent check:** `npm audit --package-lock-only --json` on each changed lock, copied out to an isolated scratch directory so it is not hoisted (`probes/indep_audit.txt`).
  - Base: 19 of 19 locks report at least one of the three GHSAs.
  - Head: 0 of 19.
  - The count of all other advisories is identical base vs head in every lock, so the PR introduces no new advisory.

### (3) Runtime reach
Instrument: `probes/consumers.py` lists, for every lock entry that declares glob or minimatch, the version node actually resolves for it and whether the consumer is dev or prod (`consumers_{base,head}.txt`, `range_violations_head.txt`).

**Our own code.** `grep -rniE "(from|require\() *.(glob|minimatch|rimraf|archiver|readdir-glob)['\"]"` over Blockchain/Dev, excluding node_modules and dist, finds **one** import: `services/mcp-server/src/package-generator.ts:1 import { ZipArchive } from 'archiver'`. The same grep form for `express` finds 425 files, which shows the grep works. No service imports glob or minimatch directly.

**Production (non-dev) consumers at head**, which are all of them:

| Lock (image) | Path | Forced | How it uses the API | Exercised at head |
|---|---|---|---|---|
| services/mcp-server (and root) | archiver 8.0.0 -> readdir-glob 3.0.0 -> minimatch | ^10.2.2 -> **11.0.3** | `new minimatch.Minimatch(...)`, a named class. minimatch 11 CJS exports `Minimatch`, `minimatch`, `GLOBSTAR`, ... | **Yes, OK.** (a) `p_archiver.mjs`: ZipArchive append+finalize, plus `archive.glob('*.json', {ignore})`, which drives readdir-glob's Minimatch matchers. (b) `p_genpkg.mjs`: the **real compiled `generatePackage`** (`tsc` rc 0) for all 7 agent types. 7/7 return a valid ZIP (PK\x03\x04), 16–18 KB, 0 throws. (c) mcp-server vitest 30/30 (it mocks generatePackage, which is why (b) was needed). |
| services/anchoring, services/nft-certificate (and root) | @blockfrost/openapi -> rimraf 6.0.1 -> glob | ^11.0.0 -> **14.0.3** | rimraf 6 does `import { glob, globSync } from 'glob'`. glob 14 still exports both, plus `sync`. @blockfrost/openapi **never loads rimraf at runtime**: 0 references outside package.json; it is used only in its own build scripts. | **Yes, OK** in both services. rimraf ESM `{glob:true}` deleted `**/*.tmp` and kept `keep.txt`. rimraf CJS loads. `@blockfrost/blockfrost-js` loads (`BlockFrostAPI` is a function). |
| 7 locks | follow-redirects 1.16.2 (axios) | patch | no API change | module loads; `http.request`/`https.get` present. Not exercised through a live axios redirect |

- **Engines:** glob 14 and minimatch 11 need node `18 || 20 || >=22`, and brace-expansion 5 needs `20 || >=22`. Every Dockerfile uses `node:24-alpine` (75 FROM lines, no other base).
- **Base comparison:** anchoring on base resolved glob 11 against **minimatch 5.1.9**, because of the old `^5.1.6` override, an out-of-range pairing. The head removes that mismatch.

### (4) jest config
- `coverageProvider: 'v8'` appears in exactly governance/jest.config.js, originate/jest.config.js and originate/jest.integration.config.js. It is placed correctly at the top level of module.exports, with no other edits. tests/connectors/jest.config.cjs is untouched (E names this).
- governance, head:
  - plain run: 167/167;
  - `--coverage` (v8 by default now): 167/167, rc 0, All files 88.34%, 0 "minimatch is not a function";
  - **control** `--coverageProvider=babel`: rc 1, 5 of 6 suites failed, 11 "minimatch is not a function". The break is real and the config line is what avoids it.
- originate, head: `--coverage` gives 152/152 suites and 1860/1860 tests, rc 0, All files 78.94%, 0 minimatch errors. These match E's 88.3 and 78.9.

### (5) Scope
39 files, exactly as the commits claim. Commit 1 is lock-only and touches follow-redirects only. Commit 2 contains only the package.json overrides, the regenerated locks and the 3 jest files. There are no docs entries.

## FINDINGS
- **F1 Note (n). E's babel control count does not match mine.** E says explicit babel breaks "1 of 6" governance suites. I get **5 of 6** failed (11 tests ran, 7 failed). Either way it is a break, which is E's point; only the number is off. Correct the PR text if it repeats this.
- **F2 Minor, dev-only (n; worth a follow-up ticket).** glob 7.2.3 is still in 5 locks (root, governance, originate, referral, vc-issuer), under jest-config, jest-runtime, @jest/reporters, test-exclude and ts-node-dev's rimraf. It is **broken against the forced minimatch 11 on any glob pattern except a pure brace pattern**: `TypeError: Cannot read properties of undefined (reading 'charAt')` at glob/sync.js:148.
  - Control (`probes/p_glob7_control.txt`): the same glob 7.2.3 with minimatch 3.1.5 passes all 5 cases. With minimatch 11.0.3, 3 of 5 throw.
  - Current reach: none.
    - jest-runtime's call is inside `try {} catch {}`, a "did you mean" hint.
    - @jest/reporters only globs `coverageThreshold` glob keys, and no config sets coverageThreshold.
    - jest-config only globs `projects`, which is unset.
    - ts-node-dev's rimraf only globs paths with magic characters, and its cache path has none.
  - Risk: a future `coverageThreshold: {'src/**': …}`, a glob `projects` entry, or the babel provider will fail with a confusing TypeError. E's mail does not mention this mechanism.
- **F3 Note (n).** referral and vc-issuer also carry test-exclude 6 / babel-plugin-istanbul resolving to minimatch 11. They run vitest, so nothing exercises it, but `jest --coverage` there would hit the same break E fixed in governance and originate. referral's image copies the builder's node_modules, dev dependencies included (audit-locks.mjs header). That code ships but is never loaded.
- **F4 Info (n).** Applying `overrides.minimatch ^11` globally forces readdir-glob (declared ^10.2.2), eslint, @eslint/config-array, nodemon and @typescript-eslint (^10) one major up. Only readdir-glob is production code, and it was exercised (above). The eslint and nodemon cases are covered only by E's "eslint messages identical" claim, which I did not re-run.
- **F5 Note (instrument, mine).**
  - Running root `npm ci` after the mcp-server and anchoring installs wiped their service-local node_modules (npm workspace behaviour). Their probes had already run and been saved, so no result is affected. nft-certificate, governance and originate were installed afterwards.
  - Two probe fixes were needed before the probes ran correctly: the `package.json` subpath of readdir-glob is not exported, so I read the file directly; and the first PackageConfig was incomplete.
  - The base `audit:locks` first exited 1 for lack of `semver`, which made it invalid as a control. I re-ran it with node_modules linked, and the real FAIL output was printed.

## UNMEASURED
- Runtime of api-gateway and kyc through a real axios redirect (follow-redirects patch).
- The 4 frontend builds and eslint over 17 packages (E's claims, not re-run).
- vitest across the other services, including anchoring 568/569.
- originate's integration config (needs a DB).
- referral, vc-issuer, staking, shared, analytics, billing and api-gateway were not installed or exercised. They have no production glob or minimatch consumer at head (static, from the lock).
- `node-pg-migrate`: dev-only, and production migrations use `scripts/run-migrations.sh` (psql). The bundle loads at head with glob 14, but no `migrate` was run against a DB.
- Docker image builds, a running stack, Node 24. **All my runs used host Node v26.8.1**, as E's did.
- The 25 untouched locks (covered only by `audit:locks` rc 0).
- mobile/secuura-app (out of scope, KS-769).

## HOW
- **Spark gate:** `spark_gate.sh` needs PR test files to run red-first on base and head. This lock-only PR has none, so it cannot run meaningfully. Its deterministic parts (head-sha assertion, diff) were done by hand above.
- **Clone:** `git clone --shared --no-checkout` from gate 47's clone into the non-existent `repo/`, with the toplevel asserted before any fetch. Remote set to Secuura/Distributed_Secuura with the Blockchain deploy key; push URL `no_push_qa_gate`. Fetched refs/pull/1859/head and develop, then a detached checkout of 8f3181e35.
- **Base worktree:** at `repo/.git/gate_base`, moved there so it sits inside the gitignored `repo/`.
- **Scratch dirs** (isolated audits, glob7 control installs, rimraf targets) are in the session scratchpad.
- **Housekeeping:**
  - `git status` of the head checkout is clean (node_modules is ignored).
  - No git write verb was run in /Volumes/DevMASTER/!CODING.
  - No process I started is still running. Heavy installs and suites ran one at a time.
  - Nothing was fixed, pushed, commented on or touched in Linear.
