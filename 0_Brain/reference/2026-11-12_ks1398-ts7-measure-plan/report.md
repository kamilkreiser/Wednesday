# KS-1398 measure-and-plan: TypeScript 7.0.2 for platform-k (outside systemTest + observability)

Filed by Wednesday from the measuring agent's returned text (its Write was refused), 2026-11-12 ~11:0x AEDT. Executes Kam's ruling 'b' of 2026-10-01 on card secuura-ks1398-typescript-7-move. Measured in an isolated clone only; nothing pushed, merged or written to any project checkout, Linear, GitHub, mail or board. Scratch clone (gitignored): this folder's scratch/, 6.7 GB.

**WEDNESDAY'S CAVEAT (read first):** the agent's clone base was 0e6479d7b, the shared checkout's stale LOCAL origin/develop ref, not the live develop (697f422f1a39 at Wednesday's ls-remote 10:4x; about 19 commits newer). The tool failures do not depend on those commits; counts of files and errors may differ slightly on the live tip. Re-measure counts at the build.

## BLUF
1. All five tools named in the ticket break on TS 7.0.2, reproduced in our repo: typescript-eslint, ts-jest, ts-node, ts-node-dev, tsup. Each is a hard crash or refusal. No tool has a TS 7 release (registry read).
2. A sixth breaker not in the ticket: 14 of our own files load the TypeScript compiler library (source-reading guard tests + 2 codemod scripts). TS 7 ships no such library, so they fail (auth 2 of 149 test files, shared 6 of 81). None fail on TS 5.9.3.
3. tsc 7 itself is cheap: production source type-checks with 0 errors on auth and originate unchanged; shared fails on one removed option (moduleResolution: node), 0 after deleting it. About 5x faster (0.5-1.0 s vs 4.2-4.7 s).
4. Cost (counts): 38 package.json on TS 5.x to bump; 5 moduleResolution:node removals; 5 baseUrl removals; 14 compiler-library files to rewrite; 5 ts-node + 1 ts-node-dev packages to tsx; 2 jest packages to Vitest (originate: 248 test files, 212 jest-API files, 1,067 jest.mock calls; governance 20/18); ESLint to oxlint at the Blockchain/Dev root; 1 SDK d.ts fix; tests/connectors (26 files) on ts-jest.
5. Recommended order: everything that also works on TS 5 first (tools, Vitest, oxlint, tsconfig cleanup, the 14 files), then flip the version in small batches (shared first).
6. Ticket corrections: referral and vc-issuer are already on Vitest (dead ts-jest devDependencies: a deletion); sdk/javascript has no lockfile/tsconfig and its d.ts step is already red on TS 5.9.3; tests/connectors is a further ts-jest user.

## TESTED (TS 5.9.3 control vs 7.0.2, same clone, same commands)
| Tool | Where | TS 5.9.3 | TS 7.0.2 |
|---|---|---|---|
| ts-jest + jest | services/originate (220 suites) | 218 pass, 2 fail (KS-1051, pre-existing) | 220/220 suites fail, 0 tests run: "does not expose the JavaScript compiler API required by ts-jest" |
| ts-node | services/staking | probe-ok | TypeError ts.sys.fileExists in ts-node configuration.js:91 |
| ts-node-dev | services/governance | runs | same crash |
| tsup --dts | sdk/javascript | d.ts written (with a minimal tsconfig) | TypeError reading useCaseSensitiveFileNames, no d.ts |
| tsup 9.0.0 --dts | sdk/javascript | not run | asks for the @typescript/typescript6 fallback |
| typescript-eslint 8.x | Dev root config over packages/shared/src | lints | crash, exit 2 (typescript-estree shared.js:59) |

tsc --noEmit: auth prod 0 -> 0, tests-incl 41 -> 80 (all +39 in the 2 compiler-library files); shared prod 0 -> 1 (TS5108; 0 after the line is deleted), tests-incl 25 -> 459 (compiler-library files); originate prod 0 -> 0, tests-incl 4 -> 17 with types:["node","jest"] (13,276 without: TS 7's default types is empty). Runtime on TS 7 without tool upgrades: auth 147/149 files (only the 2 compiler-library files fail); shared 74/81 (6 compiler-library + the pre-existing wallet-signature); originate 0/220 (ts-jest). Vitest 4.1 works on TS 7.

Removed options (each measured): moduleResolution node (5 files: packages/shared, services/billing, nft-certificate, shared, wallet-connector); baseUrl (5: frontend admin, issuer, verifier, mobile/secuura-app, services/vc-issuer; all use paths). Lock churn from the bump alone, per package: shared +368/-57, auth +371/-10, originate +497/-169 (keep lock changes scoped per package).

The 14 compiler-library files: packages/shared/src/__tests__/ entrypoint-corpus, ks1564-admin-api-keys-page-sends-no-default-org.test, ks1724-bounded-json-structural-caps.test, ks1725-zod3-compat.test, ks781-p3-3-body-parser-order.test; scripts/__tests__/ks1231_settings_save_payload.cells.mts; scripts/spec-examples/codemod/locate.ts and strip.ts; services/api-gateway/src/__tests__/ ks1240b-every-hand-built-gateway-fetch-is-bounded.test, ks1480-no-allowance-warning-fields-are-escaped.test; services/auth/src/__tests__/ ks1000-auth-test-files-are-type-checked-against-a-shrinking-baseline.test, ks1240b-social-provider-fetches-are-bounded-and-classified.test; services/mcp-server/src/__tests__/ks1767-api-client-types-the-gateway-error-body.test; services/originate/src/__tests__/ks1293-originate-suite-is-hermetic.test.

## ORDER (develop green throughout)
1. Tools that also work on TS 5: delete dead ts-jest (referral, vc-issuer); ts-node/ts-node-dev to tsx (6 packages); governance, tests/connectors, then originate (largest) to Vitest; oxlint beside ESLint, then remove ESLint.
2. Decide the 14 compiler-library files before the flip: rewrite on a non-TypeScript parser (clean; works on TS 5, can land early) or alias @typescript/typescript6 for them only (unproven).
3. tsconfig cleanup TS 5 also accepts: moduleResolution node16/bundler, drop baseUrl, add types; per package.
4. sdk/javascript d.ts: tsconfig + lock, then tsup 9 or another emitter.
5. Flip 5 -> 7.0.2 in batches: shared first (24 images depend on it), then services, then frontends and mobile; each batch passes start-secuura.sh --rebuild, its tests and audit:locks.
6. Playwright and currency items last, as in the ticket.
Smallest first move: steps 1-4 remove every TS 7 blocker with no version change.

## NOT MEASURED
tsc on the other 35 TS packages (frontends, mobile, Vite packages); oxlint rule parity on this tree; whether tsup 9 + @typescript/typescript6 produces a d.ts (attempt confounded); runtime tests for the other 35 packages; Docker --rebuild and image-size effects of TS 7's native binary; Vitest 4 -> 5 and Playwright; originate's two failing jest suites (KS-1051); drift between the ticket's base and the clone base; the live develop tip (see caveat).

## HOW
git clone --no-hardlinks of the project checkout into scratch/repo (push URL disabled), a cp -R copy for the TS 7 runs with typescript@7.0.2 --save-exact --legacy-peer-deps --ignore-scripts per package; npm ci --ignore-scripts per package; TS 5.9.3 control on every measurement; a planted type error confirmed tsc 7 checks; registry reads by npm view (read-only); census by a read-only parser over git ls-files; Linear read-only, key in-process. One cd, in a subshell, for tsup's package-local runner. Logs in scratch/ as tsc5-*, tsc7-*, test5-*, test7-*.
