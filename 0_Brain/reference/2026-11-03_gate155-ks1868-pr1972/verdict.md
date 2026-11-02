# QA GATE 155 (Tier 2, Sonnet, round 1) - Secuura PR 1972 (KS-1868 originate boot catches)

**Verdict: GO WITH NOTES.** fix-before-merge items: none. Notes N1-N3 below are optional follow-ups.

Head 8c255e05217fc8f0d43243d62b23351154d5bc12 (parent 7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6, one commit) fetched read-only into a `--shared` clone in this workdir. The local checkout lacked these objects, so I added a `gh` remote on the clone and fetched with the project's deploy key (fetch only). No write verbs ran in the Blockchain checkout.

## Boot-caller answer (Q2)
`initEventBus` has one caller, `index.ts:527` (`initEventBus();` in the app.listen callback, return ignored), and `initDb` has one caller, `index.ts:401` (`.then(log ok).catch(log failed)`, no exit). Head makes a hostile thrown value behave exactly as an ordinary Error already does at base (events: false, boot continues without events; initDb: resolves, logs "Database initialized" although the Prisma check failed, a pre-existing misleading line). Base DID differ for hostile values: the event-bus throw and the listener throw became an uncaughtException, which makes the service exit after 100 ms (index.ts:86), so head continues where base would have restarted. initDb never failed fast at base either, since its caller only logs. No outcome differs from the ordinary-Error outcome, so nothing is raised to tier 1.

## Findings
- **G155-F1 (info, positive)** - hostile-value behaviour at head equals the ordinary-Error row on all three arms.
  - FOUND: 0 of 13 kinds throw, reject, go uncaught or go unhandled at head, on every arm. Base: ctor THROWS for 3 (revoked proxy, getter throws, proxy-get-throws), the listener goes UNCAUGHT for 5 (those 3 plus null and undefined), initDb REJECTS for 5 (same 5).
  - TESTED: the real `events.ts`, `db.ts` and real winston logger (level debug, real formatters, a capture transport added), in a fresh node process per case with real uncaughtException and unhandledRejection handlers. Only ioredis (a mock EventEmitter for the listener, which emits via setImmediate), Prisma, the adapter and config were replaced. 13 kinds x 3 arms x base/head = 78 runs.
  - Kinds: ordinary, revoked Proxy, throwing message getter, Symbol message, frozen object with throwing toString (thrown directly), message = frozen throwing-toString object, message = null-prototype object, message with Symbol.toPrimitive returning an object, Proxy whose get trap throws, null, undefined, number, string.
  - HOW: the base rows fire (10 THROWS/UNCAUGHT/REJECTS across the three arms), which is the positive control. The head row has `unc=0 unh=0 logerr=0` everywhere. The logged value is a string for every hostile message. Raw: `logs/rec_base.txt`, `logs/rec_head.txt`; harness: `recorder/case.cjs`, `recorder/drive.sh`.
  - Detail: non-Error values (null, undefined, number, string, a frozen object without a message) log `undefined`, not a string. That is the same as base for those kinds, and the author's control C2 pins it.
- **G155-F2 (low)** - null/undefined thrown values have no test cell. The docs fragment says "(and, for the listener and initDb, a null or undefined value)", but none of the 15 cells throws or emits null or undefined. The mutant that removes `?.` (M4, below) survives, and the product behaviour for null/undefined is correct only by the recorder measurement above.
  - TESTED: the mutants. HOW: `logs/mutants.json`.
- **G155-F3 (low, test hygiene, not a defect)** - the author's tsc 0 -> 82 is real and reproduces exactly (82 = 49 in the 3 new files + 33 in the existing `ks1943-platform-scope-transaction-helper.test.ts`).
  - Cause: a scratch program holding every test. Two script-style (no import/export) files that both declare a top-level `mockH` collide.
  - MEASURED: each of the 4 files alone gives 0 errors; each new file paired with ks1943 gives 33-35; the 3 new files together give 48; base with no new files in the all-in-one program gives 0.
  - The service tsconfig excludes tests and gives 0 at base and head. Jest passes 205 of 205 suites (ts-jest compiles per file). `check:test-types` gates only auth, api-gateway, vc-issuer, security and m365-integration (package.json:44), so originate is not gated. Impact: an IDE or any future gating of originate would flag the files.
  - HOW: `logs/tsc_all_*.txt`, `logs/tsc_solo_*.txt`, `logs/tsc_service_*.txt`. The pairs that error are the positive control that the instrument fires.
  - Optional fix: add `export {};` to the new files.
- **G155-F4 (info)** - 3 eslint warnings (unused `eslint-disable` for no-require-imports at lines 60, 42, 43 of the three new tests), 0 errors, as the author reports. They are harmless.
- **G155-F5 (info)** - the committed tests mock the logger and `console.error`, so they do not exercise the real winston logger. I did, and it did not throw at base for the Symbol or object values, so the real logger is not an extra failure source. Production-mode file transports were not tested (NOT TESTED below).

## Figures (re-measured; Node v26.8.1)
| Item | Author | Measured here |
|---|---|---|
| Originate suite before (base) | 202 / 2349, rc 0 | 202 suites / 2349 tests, rc 0 |
| Originate suite after (head) | 205 / 2364, rc 0 | 205 suites / 2364 tests, rc 0 |
| Red-first (3 new tests copied onto base, product at base) | 9 of 15 fail by assertion, 6 controls pass | 9 failed, 6 passed; all `expect` failures (e.g. Expected "Symbol(ks1868)", Received "<symbol>"); none by timeout |
| New tests at head | 15 of 15 | 15 of 15 |
| eslint on the 5 changed src/test files | 0 errors, 3 warnings | 0 errors, 3 warnings |
| docs-fragments check | n/a | rc 0, "lint clean, render passes html_docs_check"; the 2 ADVISORY "committed page differs from render" lines are identical at base, so they are pre-existing. Control: a deliberately bad fragment gives rc 1. |

Setup note: the first full run had 2 suites fail to compile because `@asteasolutions/zod-to-openapi` was missing from my install, identically at base and head (logs `full_*_run1_missing_dep.log`). After symlinking it from `packages/shared/node_modules`, both runs were fully green.

Mutants (27 run; M7 is a no-op on initDb because it has no `error:` field to blank). Applied one at a time to the head product code and killed by running the 3 new test files:
- Killed (26 of 27): constant to undefined, String(m) to m, drop the null/undefined passthrough, catch rethrows, constant text changed, logged field blanked, read hoisted out of try, try with no constant, and (ctor only) `return true` in the catch. They hold at all three sites.
- Survived (3, the same mutant at each site): M4 `err?.message` -> `err.message`. The read sits inside the try, so for null/undefined it only changes the logged text from `undefined` to the constant string. The recorder also did not kill it, because my judge accepted a string for null. It is a near-equivalent mutant, but it is exactly the null/undefined gap in F2.
- Source restored after the run (clone `git status` clean of src changes).

## merge-tree
`git merge-tree --write-tree develop(4deb2fc10b7d) pr1972` gives rc 0, a clean tree (fd2e7069da44095db94c3aa5a2bc7ea5146081e7). The merged tree differs from develop in exactly the PR's 7 paths (3 new tests, `db.ts`, `events.ts`, 2 new fragments).

## Install route
`npm ci --ignore-scripts` worked in `services/originate` (its own lockfile), in `packages/shared`, and at the Dev root with `--workspaces=false`. The G151-F8 failure did not reproduce for these installs. Side effect: the root `npm ci` emptied the workspace `node_modules` of originate and shared; I reinstalled both (`logs/npm_ci_*_2.log`). Shared was built with `npm run build`, and `node_modules/@secuura/shared` was symlinked to it as the Dockerfile does.

## NOT TESTED
- A real Redis, Postgres or Prisma, a booted service, the real `index.ts` boot path, and the uncaughtException handler on a hostile value (read, not run).
- The four platform suites, other services' `initDb` and `initEventBus` (separate copies), whole-suite CI, Node 24 (host is v26.8.1), and the multi-tenancy branch of `initDb` (unchanged).
- NODE_ENV=production logging (file transports with `keepFileFields`); Windows/Linux differences.
- Whether a real hostile thrown value occurs in practice.
- `docs-fragments` numbering at merge time (provisional).
- No process of mine is left running. Everything is under this workdir (`clone/`, `base/` worktree, `recorder/`, `mutants/`, `logs/`), and nothing was deleted.

## CORRECTION (appended by Wednesday 2026-11-03 09:5x AEDT; the gate's text above is left as written)
Line 3 says "Notes N1-N3 below are optional follow-ups"; the Findings section holds G155-F1..G155-F5 and no N1..N3. The findings are the record (F2 and F3 are the optional follow-ups). Caught by Seat W 21st while patching the notes into PR 1972 (NOTES PATCHED 22:58Z); verdict unaffected.
