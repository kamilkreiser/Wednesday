---
date: 2026-11-12
type: drafter-output
client_project: Secuura/Blockchain (Platform K)
ticket: KS-1398 (parent; Backlog; Linear read 2026-11-12 11:21 AEDT)
scope: STEP ONE = ORDER items 1-4 of 0_Brain/reference/2026-11-12_ks1398-ts7-measure-plan/report.md. No version flip (item 5), nothing from item 6.
measured_at: develop 697f422f1a394ab00454ced051f018556573837e (live origin/develop, re-read twice by this drafter via ls-remote, 11:2x and 11:3x; UNMOVED from the commission's 697f422f1a39)
drafter: Sonnet (routing v1.0 row C8)
---

# KS-1398 STEP ONE: build lanes, measured at live develop 697f422f1a39

## BLUF
1. Step one splits into **nine lanes** (L1, L2a, L2b, L3, L4, L5, L6a, L6b, L7). Every lane owns a disjoint file set, with ONE exception that cannot be designed away: **the root `Blockchain/Dev/package-lock.json` carries a full entry for every npm workspace** (32 workspace links; `services/referral`, `staking`, `vc-issuer`, `governance` and the rest are all IN the root lock), so every lane that edits a workspace manifest also edits the root lock. Those lanes are therefore **built in parallel but merged in a fixed order**, each regenerating the root lock on top of the previous merge (section 3).
2. **First lane: L1** (dead ts-jest removal in referral + vc-issuer, ts-node to tsx in five packages). Full brief: `brief_L1.md`. It is the smallest, has no source-code change and no open non-dependabot PR on any of its files.
3. Three corrections to the commission's suggested split, each forced by the files (section 2): **(a)** governance's ts-node-dev to tsx moves to L2a, because L2a owns governance's `package.json` whole (L1 is five packages, not six); **(b)** the 14 compiler-library files are 13 for L4 + 1 for L3 (`ks1293` is a jest-config-coupled guard that enumerates originate's test files, so it must change with originate's runner); **(c)** originate's 249 tests sit in ONE flat directory, so "batch by directory" is impossible: L3 batches by filename range.
4. **A finding that changes L4's design:** not all 14 files are parse-only. `ks1767` (mcp-server) builds a full `ts.createProgram` and asserts compiler DIAGNOSTICS (TS2xxx codes); `ks1000` (auth) calls `ts.transpileModule(...).diagnostics` as a syntax oracle. A non-TypeScript **parser** cannot replace a type-check; those two need the `tsc` CLI as a subprocess (it exists on TS 5 and TS 7) or a parser's syntax errors respectively. See L4 and QUESTION 3.
5. The measured counts at the live tip **equal** the report's counts for every tool census (14 compiler-library files, 5 ts-node + 1 ts-node-dev, 5 moduleResolution:node, 5 baseUrl, 38 package.json on TS 5.x), so the plan's census stands. The jest-API sizes moved slightly (originate 220 files / 1,071 `jest.mock(` against the report's 212 / 1,067: different instrument, plus 20 newer commits).

---

## 1. What was measured, and with what (instrument + positive control for every line)

All reads are `git show/grep/ls-tree/diff/merge-base` at the sha `697f422f1a394ab00454ced051f018556573837e`, run in a **private clone** `scratch/repo` of this folder (`git clone --shared --no-checkout` of the project checkout, then `git fetch origin develop 'refs/pull/*/head:refs/remotes/pr/*'` INTO THE CLONE; its push URL is set to `DISABLED`; gitignored in the WEDNESDAY `.gitignore` in the same action; `git status` shows only the `.gitignore` edit). **Why a clone:** the project checkout's local `origin/develop` is stale (`0e6479d7b6c0`) and the sha `697f422f1a39` is NOT an object there (`git cat-file -t 697f422f1a39` = `fatal: Not a valid object name`), so `git show <sha>:<path>` was impossible without a fetch, and a fetch into the checkout is forbidden (hard rule 1). Nothing was written into `/Volumes/DevMASTER/!CODING/Secuura/Blockchain`; the only reads there were `ls-remote`, `config --get`, `rev-parse`, `cat-file -t`, `remote -v`.

| Fact | Count at 697f422f1a39 | Instrument | Positive control / agreement |
|---|---|---|---|
| Live develop tip | `697f422f1a394ab00454ced051f018556573837e` | `git ls-remote origin refs/heads/develop` (twice) | equals the commission's tip; the checkout's local ref reads `0e6479d7b6c0` (stale, as the report's caveat said) |
| Files at tip | 5,947 | `git ls-tree -r --name-only <sha>` | n/a |
| `package.json` files | 50 total; 44 outside systemTest/observability | python walk of the ls-tree list, each blob parsed | the 44 includes 38 with `typescript` `~/^5`: equals the report's "38 on TS 5.x" |
| Compiler-library files (`from 'typescript'`, `require('typescript')`, `import ts`, dynamic import) | **14**, the identical list to the report | `git grep -lE` at the sha, lockfiles and `*.md` excluded | the 14 names match the report one for one; a WIDER grep (`'typescript'` string, `ts.createSourceFile`, `ts.SyntaxKind`) finds 22 = the same 14 + 8 under `systemTest/` (out of scope: KS-1396) |
| ts-node users | 5 packages: `connectors/whatsapp-bot`, `deployment/cardano`, `services/referral`, `services/staking`, `services/vc-issuer` | `git grep -nE ts-node` (non-lock, non-docs) + manifest parse | lock hits: `git grep -l '"node_modules/ts-node"'` finds 6 lock files (the 5 + governance, via ts-node-dev) |
| ts-node-dev user | 1: `services/governance` | same | same |
| ts-jest in a `package.json` | 4: governance, originate, referral, vc-issuer | manifest parse | `git grep -l ts-jest` also names 3 jest config files (governance, originate x2) + `tests/connectors/jest.config.cjs` + 1 originate test (`ks1068`) |
| Dead ts-jest/jest/@types/jest | referral and vc-issuer: **0 files** use `jest.`, 0 `jest.mock`, 0 `jest.fn`; no jest config file in either; tests are vitest (`vi.`: 16 referral files, control) | `git grep -lE '(^\|[^A-Za-z_])jest\.'` per package dir, lock and `jest.config*` excluded | control: governance gives 18 files, originate 220 with the same command; `vi.` gives 16 in referral |
| Vitest users already | 24 of the 44 manifests | manifest parse | n/a |
| `moduleResolution: node` | **5**: `packages/shared`, `services/billing`, `services/nft-certificate`, `services/shared`, `services/wallet-connector` | `git grep -nE '"moduleResolution"' -- '*tsconfig*.json'` + a JSON parse of all 46 non-systemTest tsconfigs | equals the report's 5; other values present: `bundler` (13 files), `NodeNext`/`Node16` (4); 24 tsconfigs set `module: commonjs` with NO moduleResolution (implicit, see NOT MEASURED) |
| `baseUrl` | **5**: `frontend/admin`, `frontend/issuer`, `frontend/verifier`, `mobile/secuura-app`, `services/vc-issuer` | same grep | equals the report's 5 |
| tsconfig `types` | set in 2 of 46 (`outlook-addin`, `scripts/openapi-examples`); absent in 44 | JSON parse | 4 tsconfigs failed my comment-stripping parse (issuer, verifier, mobile, vc-issuer); the grep above still saw their `baseUrl` |
| ESLint | root `eslint.config.mjs` (132 lines); `eslint` in ~14 manifests; CI runs `npm run lint --workspaces --if-present` (ci.yml:48, deploy-demo.yml:135) | `git grep -nE eslint` + manifest parse | `observability/.oxlintrc.json` exists (the precedent); **no oxlint config outside systemTest/observability** (`git grep -lE oxlint` outside them: only a SKILL.md, a workflow comment, history.md) |
| ESLint **API** consumers | 2 tests import `ESLint` from `eslint`: `services/api-gateway/src/__tests__/ks1543-document-types-catch-logs-the-error.test.ts` and `ks1543-five-pre-existing-eslint-warnings-in.test.ts` | `git grep -nE "import .*eslint"` | the second matches 12 lines, the first 7 |
| `tests/connectors` | 26 files (20 `*.test.ts`, 0 use `jest.`); config `jest.config.cjs` is `preset: 'ts-jest'`; run only by root script `test:connectors` (`jest --config tests/connectors/jest.config.cjs`); `check-coverage.mjs` IS wired into CI | `git ls-tree` + grep | `git grep -n 'test:connectors'` finds ONLY `package.json:52`: the jest suite itself is not in any workflow |
| governance jest API | 20 test files, **18 use `jest.`**, 32 `jest.mock(`, 61 `jest.fn(`, 9 fake-timer calls, 6,208 lines in the 18 | `git grep -hoE` counts | report said 20/18: equal |
| originate jest API | 249 test files, **220 files** use `jest.`, **1,071** `jest.mock(`, 2,528 `jest.fn(`, 20 `jest.spyOn(`, **192 `jest.requireActual`**, 6 fake-timer calls, 48,337 lines in those 220; ALL 249 in ONE directory `src/__tests__/` | same | report: 248/212/1,067. Delta = instrument (mine counts non-`.test` helpers too) + 20 newer commits; I do not claim the delta is explained |
| sdk/javascript | 9 files; no `package-lock.json`, no `tsconfig.json`; `tsup src/index.ts --format cjs,esm --dts`; vitest `^1.0.4`; not an npm workspace (not in the root lock) | `ls-tree` | root lock probe: `services/referral`... present, `sdk/javascript`, `connectors/whatsapp-bot`, `deployment/cardano` ABSENT |
| Commits since the report's base | 20 commits `0e6479d7b..697f422f1`, 41 files; **0 of them touch a `package.json`, `tsconfig*` or `jest*` path** | `git log --oneline` + `git diff --name-only -- '*package.json' '*tsconfig*' '*jest*'` | empty output on the diff, 20 on the log |

### Open PRs (the lane-collision rule)
**Instrument.** `git ls-remote origin 'refs/pull/*/head'` = **2,120** PR heads (every PR ever, open or not). The API state is NOT mine (project identity), so open-vs-closed was inferred from a **second instrument**: `git ls-remote origin 'refs/pull/*/merge'` = **99 refs**. GitHub keeps a `refs/pull/N/merge` only for PRs it can currently merge. **Controls:** all 7 known-open PRs (2199, 2196, 2193, 2191, 2137, 2125, 2079) HAVE a merge ref; 0 of the 50 heads whose full patch reverse-applies cleanly onto develop (squash-merged, changes already in develop) have one. **Limit, stated:** an open PR with merge conflicts has NO merge ref, so the 99 is a LOWER bound on open PRs. For the PRs near a lane I also list the "possibly open" ones (head not an ancestor of develop, patch does not reverse-apply, no merge ref, head since 2026-10-20); their state is **UNMEASURED at the API** and the build seat reads it (GraphQL; a REST 403 is never an absence).
**Changed-file set per PR:** `git diff --name-only $(git merge-base <develop> <head>) <head>` (three-dot, per the standing line), all 99 + 1,631 other non-ancestor heads, in the clone where every PR object exists (no PR was UNMEASURED for missing objects).
**Result per lane** is in each lane's "Open-PR contact" line. Headline: **no lane file is touched by PRs 2196, 2193, 2137, 2125; L2b, L5, L6b-source, L7 are untouched by any open PR; the hard contacts are 2099 (governance + root lock), 2191 (originate `tsconfig.test.json`), 2199/2079/2159 (three L4 files), and 17 PRs on originate files.** Ten of the 99 are dependabot[bot] bumps by head-commit author (`git log -1 --format=%an`: 575, 635, 639, 649, 945, 946, 947, 948, 949, 1965); they edit root manifests/lock; see QUESTION 1. (Authors of the 99: 88 Kam Kreiser, 10 dependabot[bot], 1 StuartOBD.)

---

## 2. The lanes

Routing line format: `model: <id from models_latest.json> -- <row> -- P1-P4`. `models_latest.json` (checked 2026-11-12 11:08 +1100, `warnings: []`) names **claude-sonnet-5-5**. P1 NO (dev tooling, no signature class; nothing deploys, no client words). P2/P3 **unmeasured by this drafter**: Wednesday reads `fleet/usage_gate.sh` at stamping. P4 NO (Secuura, the Spark is cleared for Secuura only; no Datasec). Gates by the 09-05 tier rule: tests-only / config / tooling = **G2 (tier 2, Sonnet)**; anything that changes a non-test source file or a Dockerfile = G1.

### L1: dead ts-jest removal + ts-node -> tsx (five packages)   [FIRST LANE; brief written]
- **ORDER items:** 1 (part: dead ts-jest; ts-node to tsx).
- **Owns (exact files):** `Blockchain/Dev/services/referral/{package.json,package-lock.json}`, `.../services/vc-issuer/{package.json,package-lock.json}`, `.../services/staking/{package.json,package-lock.json}`, `.../connectors/whatsapp-bot/{package.json,package-lock.json}`, `.../deployment/cardano/package.json` (NO lockfile exists there: do not create one), the six cardano scripts that name ts-node in a shebang or usage text (`scripts/deploy-contracts.ts`, `env-manager.ts`, `faucet.ts`, `test-contracts.ts`, `testnet-deploy.ts`, `wallet-setup.ts`), `services/m365-integration/SETUP.md` (one line, 66), plus ITS OWN docs fragment pair, plus a slot in the root-lock chain (section 3, position 1).
- **Changes:** referral and vc-issuer lose `jest`, `ts-jest`, `@types/jest`; referral, vc-issuer, staking (`nodemon ... --exec ts-node`) get `"dev": "tsx watch src/index.ts"` (the form the other 19 services use) and lose `ts-node` and, because nothing else names it (`git grep -nE nodemon`: only those three manifests plus one shell-test word), `nodemon`; whatsapp-bot and cardano swap `ts-node` for `tsx` in scripts and devDependencies; `tsx` is added at the repo's `^4.23.1` (the same range as 19 services).
- **Size (measured, files in scope):** 5 manifests (59, 54, 51, 26, 22 lines), 4 locks (7,670, 7,685, 4,142, 1,165 lines), 6 cardano scripts + 1 doc line. Expected manifest diff: about 35 lines; lock diff: removals only except the `tsx` subtree (NOT measured; the brief demands a measured removal/addition set).
- **Tests that prove it on TS 5 (green before AND after):** `npm test -w services/referral` (vitest, 18 test files), `-w services/vc-issuer` (28), `-w services/staking` (8); `npm run build -w <each>` (tsc, unchanged); `npm ci --dry-run` in each standalone lock dir (preflight's lock clean-room leg); `npm run audit:locks`; for whatsapp-bot and cardano a `tsx` smoke on one script (no suite exists there). Suite counts before/after printed as ratios.
- **Routing:** `model: claude-sonnet-5-5 -- C2 -- P1 NO, P2/P3 gauge by Wednesday at stamp, P4 NO`. Gate G2.
- **Spark:** **NO as a lane.** Two lines of the predicate fail: a lockfile cannot be spelled out as `-`/`+` lines (it needs `npm` to regenerate), and the cardano scripts have no runnable test nearby. The three `package.json` hunks alone WOULD be rung 1-2, but splitting them from the lock regeneration puts two seats on one file pair.
- **Open-PR contact:** none non-dependabot. Dependabot 575 and 649 (Aug 2026, stale) edit `referral/staking/vc-issuer package.json`: see QUESTION 1. Possibly-open (UNMEASURED): 1953, 1859, 1688, 1679, 1674 touch `referral/package-lock.json`; the manifest-level overlap of each was not itemised.

### L2a: governance -> Vitest (+ its ts-node-dev -> tsx)
- **ORDER items:** 1.
- **Owns:** everything under `Blockchain/Dev/services/governance/` (34 files): `package.json`, `package-lock.json`, `jest.config.js` (replaced by `vitest.config.ts`), the 18 jest-API test files (6,208 lines) and the 2 others, `tsconfig.json` (so `types` is set here, not in L5), a fragment pair, and root-lock slot 2.
- **Size (measured):** 20 test files / 6,424 lines; 32 `jest.mock(`, 61 `jest.fn(`, 1 `jest.spyOn(`, 9 fake-timer calls, 0 `requireActual`; 1 `@jest/globals` import. The jest config carries a `uuid` ESM transform (KS-594) and `coverageProvider: 'v8'` (KS-1891) that must survive; Vitest handles ESM `uuid` natively, which retires KS-1894's `glob inside jest and ts-node-dev` problem for this package.
- **Tests:** `npm test -w services/governance` before (jest: counts at the build, UNMEASURED today) and after (vitest), the test COUNT must not drop; `npm run build -w services/governance` (tsc); `tsc` over the test files if the package has a test tsconfig (it has none: state that).
- **Routing:** `model: claude-sonnet-5-5 -- C2 -- P1 NO, P2/P3 at stamp, P4 NO`. Gate G2 (tests + tooling; the product `src/` is untouched).
- **Spark:** no (a runner migration is not a spelled-out hunk).
- **Open-PR contact (HARD):** **PR 2099** (head `8967de8b1755`, 2026-11-09) edits `governance/package.json`, `package-lock.json`, `db.ts`, `index.ts`, two tests and more: **L2a must wait for 2099 to merge** (or Wednesday rules otherwise). Also possibly-open (UNMEASURED): 13 PRs touching governance tests/src (2051, 2039, 1953, 1952, 1947, 1944, 1939, 1938, 1859, 1840, 1824, 1696...). Any test file one of them touches is held back to a later round.

### L2b: tests/connectors -> Vitest
- **ORDER items:** 1.
- **Owns:** `Blockchain/Dev/tests/connectors/` (26 files: `jest.config.cjs` replaced by `vitest.config.ts`, `_helpers.ts` (it calls the `describe`/`describe.skip` globals), the 20 tests; `check-coverage.mjs` and `connectors.registry.json` untouched) + the ONE script line `package.json:52` (`test:connectors`) in the ROOT manifest, plus a root devDependency on `vitest` (the root does not declare it today; it resolves only by hoisting). It therefore holds root-manifest slot 1 and root-lock slot 3.
- **Size (measured):** 20 test files, 0 `jest.` uses, 458 lines of `.ts` in the directory: the smallest runner move. All tests are skipped unless env vars are set, so the proof is "same number of suites, same skip count".
- **Tests:** `npm run test:connectors` before/after, printing `suites x/y, tests a passed b skipped` both sides; `npm run check:connectors` (the CI-wired coverage check) unchanged.
- **Routing:** `model: claude-sonnet-5-5 -- C2 -- P1 NO, P2/P3 at stamp, P4 NO`. Gate G2.
- **Spark:** **candidate, pilot rung 4**: one directory, mechanical (config swap + globals), runnable in-process (every cell skips without env). Fails predicate line 5 only if the root `package.json` + lock hand-off is counted; keep it Sonnet.
- **Open-PR contact:** none (0 of 99, 0 possibly-open on the directory). Root manifest/lock: dependabot only.

### L3: originate -> Vitest (largest; rounds by filename range)
- **ORDER items:** 1.
- **Owns:** everything under `Blockchain/Dev/services/originate/` (320 files): `package.json`, `package-lock.json`, `jest.config.js`, `jest.integration.config.js` -> `vitest.config.ts` + `vitest.integration.config.ts`, `tsconfig.json` and `tsconfig.test.json` (`types: ["node","jest"]` becomes the vitest equivalent; the report measured 13,276 errors without `types`), the two helper files (`helpers/sharedModuleMock.ts`, `helpers/verifyHealFetch.ts`), the `uuid-cjs.ts` stub (becomes unnecessary), **`ks1293-originate-suite-is-hermetic.test.ts`** (it enumerates originate's test files and states "RUNS UNDER the DEFAULT jest config"), `ks1061-shared-mock-completeness`, `ks1068` (names ts-jest), fragments, and the LAST round's edit to `scripts/audit/audit-baseline.json` ONLY if a measured need appears (see QUESTION 6). Root-lock slot 5.
- **Size (measured):** 249 test files / 51,761 lines; **220 files / 48,337 lines use `jest.`**; **1,071 `jest.mock(`**, 2,528 `jest.fn(`, 20 `jest.spyOn(`, **192 `jest.requireActual`**, 6 fake-timer calls, 2 `@jest/globals` imports. Two suites are already red on develop (KS-1051, pre-existing: the report measured 218 pass / 2 fail at its base; the live-tip reading is UNMEASURED and is the FIRST thing round 0 prints).
- **Hazards the files show (not solved here):** `jest.requireActual(...)` is synchronous, Vitest's `vi.importActual` is async; `jest.mock` hoisting differs from `vi.mock`; jest's CJS `uuid` mapper has no Vitest analogue because Vitest reads ESM; `jest.useFakeTimers` options differ. Round 0 should prove a shim or codemod on 5 files before any batch.
- **Rounds:** all 249 tests are ONE flat directory, so a "by directory" split does not exist. Suggested: **round 0** (config + `types` + the two helper files + ks1293 + 5 representative tests, jest and vitest side by side, `npm test` runs both with disjoint include/ignore lists), then **rounds 1..N by filename range** (about 40 files each), **final round** deletes jest/ts-jest/@types/jest from the manifest and lock. Each round re-reads the open-PR set and HOLDS BACK any test file an open PR touches (the 38 files at this tip are listed in section 4); held files go in the next round.
- **Tests:** `npm test -w services/originate` before: jest; after each round: the sum of jest + vitest counts must equal the before count (suite and test counts as ratios); `npm run test:integration` configs parse (the integration suites need Postgres: NOT RUN is an honest line); `npm run build -w services/originate`; the `check:test-types` ratchet (see section 3 hazards).
- **Routing:** `model: claude-sonnet-5-5 -- C2 -- P1 NO, P2/P3 at stamp, P4 NO`. Gate G2 per round (tests-only), because no product source file changes. If a round must touch `src/` non-test code, that round is G1 and the seat stops and asks.
- **Spark:** **no for the lane; pilot rung 4 only per file** after round 0 proves the codemod AND only for files that are not security-surface tests. Most of originate's tests assert authorisation refusals, so the Sonnet seat keeps them.
- **Open-PR contact (HARD):** 17 of the 99 open-proxy PRs touch originate (2191, 2177, 2167, 2161, 2160, 2158, 2154, 2141, 2138, 2101, 2100, 2099, 2094, 2093, 2087, 2052 + stale 949, 575). **PR 2191 edits `originate/tsconfig.test.json`**: that file is held until 2191 merges (the A24 brief's A2 row says 2191 is A1/KS-1090, not yet merged).

### L4: the compiler-library files, rewritten on a non-TypeScript parser (13 files; the 14th is in L3)
- **ORDER items:** 2 (Wednesday's design: no `@typescript/typescript6` alias).
- **Owns (13 files):** `packages/shared/src/__tests__/{entrypoint-corpus.ts, ks1564-admin-api-keys-page-sends-no-default-org.test.ts, ks1724-bounded-json-structural-caps.test.ts, ks1725-zod3-compat.test.ts, ks781-p3-3-body-parser-order.test.ts}`; `scripts/__tests__/ks1231_settings_save_payload.cells.mts`; `scripts/spec-examples/codemod/{locate.ts, strip.ts}`; `services/api-gateway/src/__tests__/{ks1240b-every-hand-built-gateway-fetch-is-bounded.test.ts, ks1480-no-allowance-warning-fields-are-escaped.test.ts}`; `services/auth/src/__tests__/{ks1000-auth-test-files-are-type-checked-against-a-shrinking-baseline.test.ts, ks1240b-social-provider-fetches-are-bounded-and-classified.test.ts}`; `services/mcp-server/src/__tests__/ks1767-api-client-types-the-gateway-error-body.test.ts`. Plus: the ROOT manifest `package.json` devDependency for the chosen parser and root-lock slot 4 (a root devDependency resolves from every workspace; it avoids touching five more manifests that other lanes own). `ks1293` is L3's.
- **Size (measured, per file: lines / `ts.` references / `createSourceFile` calls):** entrypoint-corpus 175/18/1; ks1564 521/65/1; ks1724 506/10/1; ks1725 738/48/6; **ks781 5,719/280/9**; ks1231 407/52/2; locate 183/19/1; strip 114/11/1; gateway ks1240b 365/14/1; ks1480 310/12/1; auth ks1000 **1,461**/28/1; auth ks1240b 447/10/1; mcp ks1767 114/12/1. Total about 11,060 lines in the 13.
- **The finding:** `ks1767` builds a **Program** (`createProgram`, `createCompilerHost`, `readConfigFile`, `flattenDiagnosticMessageText`) and asserts compiler diagnostics: no parser reproduces a type error. `ks1000` uses `ts.transpileModule(...).diagnostics` as a "does this text parse" oracle (a parser's syntax errors replace that) and `ks1000`'s subject (a type-checked-baseline ratchet) reads the `tsconfig.test.json` files. For ks1767 the honest rewrite is a subprocess `tsc --noEmit` on the probe (works on 5 and 7, but the diagnostic TEXT may differ between versions, so the assertion must key on the code, e.g. TS2322, not the message). This is QUESTION 3.
- **Parser choice (QUESTION 2):** candidates measured in the root lock: `@babel/parser` 7.29.7 already present (transitive, via jest's babel chain, which L3 removes: it must be declared explicitly or it may vanish); `oxc-parser` ABSENT (`@oxc-project/types` 0.154.0 is present, dev, via rolldown); `@swc/core` ABSENT; `acorn` 8.16.0 present but no TypeScript. Node-type vocabulary differs from the TS AST (`CallExpression`, `Identifier`, `StringLiteral` map cleanly; `forEachChild`, `getStart()` do not), so each file's helper rewrite is real work.
- **Tests:** each file's own suite green before AND after (`npx vitest run <file>` per file, from its package), PLUS the guard must still catch what it caught: a **planted regression per guard** (each of these files exists to fail on a defect), run red then green. Suite totals for `packages/shared` (81 files at the report's base, 6 compiler-library failures expected only on TS 7), `services/auth`, `api-gateway`, `mcp-server`. Then `npm run check:test-types` and the ratchet.
- **Routing:** `model: claude-sonnet-5-5 -- C2 -- P1 NO (see note), P2/P3 at stamp, P4 NO`. Gate G2. **Note:** `ks1240b` (fetch-is-bounded guards), `ks1564` (a source guard on an auth-adjacent page), `ks781` (body-parser order) assert security properties; they stay on Sonnet and the gate reads the planted-regression proofs.
- **Spark:** **mostly no.** The AST walkers are not spelled-out hunks. The smallest could be pilot rung 4 after a Sonnet seat proves the first: `strip.ts` (114), `locate.ts` (183), `entrypoint-corpus.ts` (175). Every one of the three would still need a golden written first; none is rung 1-3 today.
- **Open-PR contact (HARD, three files):** **PR 2199** (KS-2170, `ks1725-zod3-compat.test.ts`, gate-322 GO, going to the merge seat), **PR 2079** (`ks1725-zod3-compat.test.ts`), **PR 2159** (`ks1231_settings_save_payload.cells.mts`). Those two files are HELD OUT of L4 round 1 and done after the PRs merge. Possibly-open (UNMEASURED): 1953 (ks1725), 1944 (ks1724, ks781), 1841/1788 (auth ks1240b), 1785 (gateway ks1240b), 1769 (mcp ks1767), 1765/1744/1730/1710 (auth ks1000), 1734 (ks1564). Also KS-1761 (Backlog, "ks1564 ... the AST guard does not see a member call, a bracket c...") targets the same file: pair it or leave ks1564 until it lands.

### L5: tsconfig cleanup (moduleResolution node16/bundler, drop baseUrl, add `types`)
> **CORRECTED 2026-11-12 13:50 by Wednesday (from Seat A 26th's measurement, confirmed by gate 328 on PR 2207):** `node16`/`bundler` is WRONG for these five `module: commonjs` files (TS5110 / TS5095). The built change DELETES `moduleResolution: node` (TS 5.9.3 then defaults identically: gate 328 read identical `--traceResolution` module-resolution lines in all nine packages) and drops `baseUrl` with `paths` values made `./`-relative; NO `types` was needed (no missing-global code on TS 7.0.2). Built as PR 2207 (KS-2177), GO WITH NOTES at 0d82e65bc5be. Open on TS 7: services/billing TS6059 (rootDir) — a decision for the version-flip step, not this lane. The original text below is kept as written.
- **ORDER items:** 3.
- **Owns (only `tsconfig*.json`; no manifest):** the five moduleResolution sites `packages/shared/tsconfig.json`, `services/{billing,nft-certificate,shared,wallet-connector}/tsconfig.json`; the five baseUrl sites `frontend/{admin,issuer,verifier}/tsconfig.json`, `mobile/secuura-app/tsconfig.json`, `services/vc-issuer/tsconfig.json`; and the `types` field where a package needs it. **NOT L5's:** `services/originate/tsconfig*.json` (L3) and `services/governance/tsconfig.json` (L2a), because their `types` depends on which test runner is installed.
- **Size (measured):** 10 files, one line each for the two removals; `types` additions unmeasured (the report found TS 7's default `types: []` costs 13,276 errors on originate; the other 44 tsconfigs set no `types`, so every one needs a per-package decision).
- **Tests:** per package `npm run build` (tsc) before/after, `tsc --noEmit` including test files where a `tsconfig.test.json` exists, the **test-type-check ratchet** (`npm run check:test-types`, `ks1000`/`ks1090` suites: a tsconfig change can move their baselines), frontends `vite build`. All on TS 5 (the options are valid there).
- **Hazard:** a `types` entry needs the type package in the package's `devDependencies`; if one is missing the fix is a manifest edit owned by another lane: STOP and report, do not edit it.
- **Routing:** `model: claude-sonnet-5-5 -- C2 -- P1 NO, P2/P3 at stamp, P4 NO`. Gate G2 (config), unless a frontend bundle output changes (then G1).
- **Spark:** **YES, per file, the strongest candidate in step one:** one file, one hunk (delete `"baseUrl": "."` or change `"moduleResolution": "node"` to `"node16"`/`"bundler"`), runnable test nearby (`tsc --noEmit`), not a security surface. But `baseUrl` removal with `paths` needs the `paths` values rewritten relative (the report: all five use `paths`): that is a 2-hunk file, rung 2. The seat measures `tsc` before/after per file so a failing cell is its own control.
- **Open-PR contact:** none. L5 can run in parallel with everything and merge first or last.

### L6a: oxlint beside ESLint at the Blockchain/Dev root
- **ORDER items:** 1 (first half).
- **Owns:** a NEW `Blockchain/Dev/.oxlintrc.json`, the ROOT `package.json` (devDependency `oxlint`, an `oxlint` script; ESLint stays) and root `package-lock.json` (slot 6), plus CI/doc wiring if any. The reference is `observability/.oxlintrc.json` + `observability/package.json` (`oxlint` 1.90.0, pinned) and `systemTest/oxlint`; copy the pinning discipline, not the rules.
- **Size:** unmeasured (rule parity on this tree is NOT MEASURED in the report either). The new rule file is a port of `eslint.config.mjs` (132 lines).
- **Tests:** `npx oxlint` over `Blockchain/Dev` exit 0, with the same 2 planted-defect shape the observability harness uses; ESLint (`npm run lint`) still green BESIDE it; counts of files linted by each printed as a ratio.
- **Routing:** `model: claude-sonnet-5-5 -- C2 -- P1 NO, P2/P3 at stamp, P4 NO`. Gate G2.
- **Spark:** no.
- **Open-PR contact:** root manifest/lock touched by 11 open-proxy PRs: the 10 dependabot ones plus PR 2099 (lock only): the root lock is regenerated at merge time (section 3).

### L6b: ESLint removal   [LAST lane]
- **ORDER items:** 1 (second half).
- **Owns:** `Blockchain/Dev/eslint.config.mjs` (delete is not allowed: the brief rule is "never delete"; the file is QUARANTINED into a dated folder and the move recorded, or Wednesday rules), every manifest's `eslint` / `lint` script (about 14 manifests, plus `typescript-eslint`, `@eslint/js`, `globals` at the root) and the matching locks (about 14 + root), the two ESLint-API tests (`ks1543-...` x2: they must be rewritten against oxlint or retired), `.github/dependabot.yml` (the `@typescript-eslint` groups), `.github/workflows/ci.yml:48` and `deploy-demo.yml:135` if the `lint` script name changes, and the `.claude/skills/secuura-test-discipline/SKILL.md:463-465` wording the ticket names.
- **Why last:** it edits ~14 manifests and ~15 locks that every other lane also owns; running it earlier makes every other lane collide.
- **Tests:** `npm run lint --workspaces --if-present` (CI's exact command) before/after as a ratio; the 2 rewritten tests with planted defects.
- **Routing:** `model: claude-sonnet-5-5 -- C2 -- P1 NO, P2/P3 at stamp, P4 NO`. Gate G2, G1 if a workflow file changes.
- **Spark:** no.
- **Open-PR contact:** PRs 1764, 1743, 1702 (possibly open, UNMEASURED) edit `ks1543-document-types-catch-logs-the-error.test.ts`.

### L7: sdk/javascript d.ts (tsconfig + lock + emitter)
- **ORDER items:** 4.
- **Owns:** `Blockchain/Dev/sdk/javascript/` (9 files; `package.json`, `src/**`, README). It has NO lockfile and NO tsconfig (so both are NEW files); it is NOT a workspace, so it does not touch the root lock and can run in parallel with everything. A tsup `dts` step is already red on TS 5.9.3 (the report); it asked `ignoreDeprecations: "6.0"` for tsup 8.5's injected `baseUrl`.
- **Size:** 9 files / 1,575 lines; new: `tsconfig.json`, `package-lock.json`.
- **Tests:** `npm run build` (tsup, cjs+esm+dts) producing `dist/index.d.ts` (the report's red-on-5.9.3 is the "before"); `npm test` (vitest) is separately red: KS-2136 says it "runs vitest with no test files and exits 1". Do not fix KS-2136 here unless Wednesday folds it in (same `package.json`).
- **Routing:** `model: claude-sonnet-5-5 -- C2 -- P1 NO, P2/P3 at stamp, P4 NO`. Gate G2; G1 if it changes published artefacts (it is `"license": "MIT"`, `prepublishOnly: npm run build`): check nothing publishes it.
- **Spark:** pilot rung 4: one package, `tsc`/`tsup` is the nearby runnable test; the open choice (tsup 9 vs another emitter) is a DECISION (predicate line 5), so Sonnet decides first. The report could not tell whether `tsup 9 + @typescript/typescript6` emits a d.ts.
- **Open-PR contact:** possibly-open PR 2106 (2026-11-09) edits `sdk/javascript/README.md` and `src/modules/transfers.ts` (merge-ref absent; UNMEASURED).

---

## 3. Ordering, collisions and the root lock

**The one shared file.** `Blockchain/Dev/package-lock.json` (workspaces `packages/*`, `services/*`, `frontend/*`) lists each workspace's dependencies, so ANY edit to a workspace `package.json` changes the root lock (measured: `services/referral`, `staking`, `vc-issuer`, `governance` all appear in it with their `devDependencies`; `sdk/javascript`, `connectors/whatsapp-bot`, `deployment/cardano` do not). Each package ALSO carries its own standalone lock, which is what its Docker image installs (`audit-locks.mjs`); both must move together.

**Rule:** lanes are built in parallel in separate worktrees, but **merged in this order, one at a time**, and each lane regenerates ONLY its own entries of the root lock on the freshly-merged develop (no unscoped re-resolve: KS-1379 moved ~1,000 non-target entries once):

| Slot | Lane | Root lock | Root `package.json` | Parallel-safe with |
|---|---|---|---|---|
| (free) | L5 tsconfig | no | no | everything |
| (free) | L7 sdk | no | no | everything |
| 1 | L1 | yes (referral, vc-issuer, staking) | no | L5, L7, L2b-code |
| 2 | L2a | yes (governance) | no | after 2099 merges |
| 3 | L2b | yes (root devDep vitest) | **yes** (script + devDep) | |
| 4 | L4 | yes (root devDep parser) | **yes** | the 2 held files wait |
| 5 | L3 | yes (originate, rounds) | no | |
| 6 | L6a | yes | **yes** | after L2b/L4 |
| 7 | L6b | yes (about 14 workspaces) | **yes** | LAST |

**Sequencing reasons:** (1) L2b before L6a: both edit root `package.json`. (2) L3's FINAL round and L2a are the last two jest removals; `@babel/parser` (needed by L4) is currently present only transitively through jest's babel chain, so L4 declares it explicitly BEFORE L3's last round. (3) The `tests/connectors` suite resolves `jest`/`ts-jest` by hoisting from governance/originate, so **L2b must merge before the LAST jest removal (L3 final round)** or `npm run test:connectors` breaks. (4) `scripts/audit/audit-baseline.json` carries the `deepmerge` entry (GHSA-gcqx-w48m-w2h4, KS-1707, expires 2027-02-28) whose reason names `jest-config` in root, originate, governance, referral, vc-issuer: no lane edits that file; whether an unused baseline entry makes the gate fail is UNMEASURED (QUESTION 6).

**Hazard on every lane that edits a tsconfig or a test file:** the test-type-check ratchet (`check:test-types`, `scripts/typecheck-tests/check.cjs`, suites ks1000/ks1090 reading `tsconfig.test.json`) is a baseline of compiler errors per service; moving `types` or the test runner can move it. Run it before and after, in L2a, L3 and L5.

**Parallelism.** Builds that can start NOW in parallel: L1, L2b (code), L5, L7 (4 worktrees). L2a waits for PR 2099. L4 can start its 11 non-held files. L3 round 0 can start (config + helpers + ks1293 + 5 tests, nothing an open PR touches) but its tsconfig.test.json waits for 2191. L6a any time after L2b. L6b last.

---

## 4. Appendix: originate files held back from L3 (touched by an open-proxy PR at this tip)
38 paths (24 test files, 11 source files, `tsconfig.test.json`, one helper). Test files: ks1032-unconfigured-vouch-fails-closed, ks1041-gateway-provenance, ks1600-malformed-permissions..., ks1634 x3, ks1868-originate-{db-init-prisma,email-acs-and-smtp,events-init,events-redis-error-listener}, ks1937-email-service-logs..., ks1939-verification-by-id..., ks1991 x4 (two integration), ks2017-..., ks2060-the-wallet-clears..., ks2094-..., ks2145-..., ks2163-..., ks488-smtp-opt-in, ks563, ks584-verify-row-selection, ks590, ks741; helper `ks1991PgCluster.ts`; source `events.ts`, `routes/{adminConfig,certifications,documents,verification,verificationV2}.ts`, `services/{email,gdprService}.ts`, `utils/{gatewayProvenance,idNamespaceCollision}.ts`, `tsconfig.test.json`. (L3 changes no source file; the 11 source paths are listed only because a PR that edits them will also edit tests the lane would convert.) The build seat recomputes this at its cut.

---

## NOT MEASURED
- **PR open/closed state at the API** (the project's identity is not mine): I used the merge-ref lower bound (99) and a "possibly open" list; both are inferences with stated controls. Dependabot's 10 PRs are counted as open on the same evidence.
- **Root-lock regeneration cost and scope.** I did not run `npm install --package-lock-only` anywhere (no write instruction to test; `npm ci` not run). Whether a scoped removal/addition leaves the other ~1,600 entries byte-identical, per lane, is UNMEASURED. The L1 brief makes it the first measurement.
- Test counts at the live tip: governance, originate (jest), referral, vc-issuer, staking, shared, auth, api-gateway, mcp-server suite totals, and which originate suites are red today (the report's 218/2 is at the old base).
- Whether `tsx` runs each of the five `dev` entry points (needs DB/Redis env), whether `tsx watch` is a behavioural equal of `nodemon --exec ts-node` (ignore patterns, signals), whether the cardano scripts run at all today.
- tsc on the other TS packages under `module: commonjs` with NO `moduleResolution` (24 tsconfigs): the report measured auth and originate clean on TS 7; the rest is unmeasured, and "implicit node10" may be a sixth removed-option site.
- Oxlint rule parity with `eslint.config.mjs` on this tree; whether `oxlint-tsgolint` is needed outside type-aware rules.
- Whether `ks781` (5,719 lines, 280 `ts.` references) is rewritable at reasonable cost, or should be split.
- The mobile app: `mobile/secuura-app` runs `jest` (no `jest`/`ts-jest` in its manifest; presumably via the Expo preset): not part of the report's census, unmeasured.
- Linear tickets other than KS-1398 are read by TITLE only (searches below); KS-1894, KS-2136, KS-1761, KS-1051, KS-1737, KS-920, KS-1224 may bear on a lane.
- Existing child tickets: **none exist** for any lane (KS-1398 `children` = []; title/description searches on ts-node, ts-jest, oxlint, tsup, moduleResolution, baseUrl, "typescript 7" and the package names found no step-one ticket; KS-1398 itself returns, as expected, as the positive control).

## QUESTIONS FOR WEDNESDAY (one line each)
1. Ten dependabot PRs (575, 635, 639, 649, 945-949, 1965) hold the root lock and several manifests open since Aug-Nov: do you waive them for the manifest lanes, or must they merge/close first?
2. Parser for L4: `@babel/parser` (present transitively, needs an explicit devDependency) or `oxc-parser` (absent; same family as oxlint and rolldown)?
3. `ks1767` (and the type-check half of `ks1000`) need compiler diagnostics, not a parser: accept a `tsc` CLI subprocess keyed on the diagnostic CODE, or retire/replace those two cells?
4. PR 2099 blocks L2a (governance manifest + tests) and PR 2191 blocks one originate config file: hold those lanes until they merge, or sequence behind them with a fresh cut?
5. Lane L1 deviates from "6 packages": governance's ts-node-dev goes to L2a so one lane owns governance whole; and `ks1293` goes to L3. Approve?
6. After jest leaves every lock, the `deepmerge` entry in `audit-baseline.json` (KS-1707) may be unused: does an unused entry fail `audit:locks`, and who edits that Kam-ruled entry?
7. `eslint.config.mjs`: "never delete" vs ESLint removal in L6b: quarantine into a dated folder, or an explicit deletion grant?
8. Vitest version for the moved suites: the repo's `^4.1.12` (works on TS 7 per the report) or `^5` (what systemTest uses; ticket item 7)?

## WEDNESDAY'S RULINGS ON THE QUESTIONS (11:3x AEDT 12 Nov, design calls inside Kam's 11:09 go; his word corrects any)
1. Dependabot PRs (575, 635, 639, 649, 945-949, 1965): WAIVED for the manifest lanes. Lanes proceed; nobody touches, rebases or closes a dependabot PR. After each lane merges, its now-conflicting dependabot PRs are LISTED in the READY/MERGED mail (numbers only) for a later board pass.
2. L4 parser: `@babel/parser` as an EXPLICIT devDependency (already in the tree through jest; mature TS plugin). Not oxc-parser.
3. ks1767 and ks1000's diagnostic half: ACCEPT a `tsc` CLI subprocess keyed on the diagnostic CODE (TS2xxx), not message text; the cells are kept, never retired. The parser rewrite covers only the parse-only files.
4. PRs 2099 and 2191: SEQUENCE behind them with a fresh cut after each merges. L2a waits for 2099; L3's config round waits for 2191. Other lanes do not wait.
5. L1 = five packages (governance's ts-node-dev to L2a) and ks1293 to L3: APPROVED.
6. deepmerge baseline entry (KS-1707): measure at L3's final round whether an unused entry fails `audit:locks`; editing that entry is NOT a lane's call (Kam-ruled entry) -> the seat stops and Wednesday cards it then.
7. eslint.config.mjs in L6b: ruled when L6b is briefed (it is the LAST lane); until then no lane touches it.
8. Vitest: the repo's `^4.1.12` for every moved suite (proven on TS 7 by the report). v5 is ticket item 7, later.
