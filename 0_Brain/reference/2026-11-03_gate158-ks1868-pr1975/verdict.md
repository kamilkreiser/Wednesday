# QA GATE 158 (Tier 2, Sonnet, round 1) - Secuura PR 1975 (KS-1868 transfer delegationService catches)

**Verdict: GO WITH NOTES.** Fix-before-merge items: none. Tier stays 2.

Head bd9dd971007322e6bf5de89e06a87536debe8dc8 (matches Wednesday's pin), develop 66cbe4e52d5afadc9d13ca141200026cc68d5095 (matches). Code from a `--shared` clone in `w/repo`; the local checkout lacked the PR objects, so (as gate 155) I added a `gh` remote on MY clone and fetched with the project deploy key (fetch only; no write verb ran in the Blockchain checkout). Host Node v26.8.1. Author's READY read whole.

## Caller answer (Q2)
verifyDbReady has one non-test caller, `index.ts` `runDbBootTasks` (last step), passed to `initDb` as its ready hook; `db.ts runDbReadyHook` (lines 97-112) already catches a rejecting hook and logs "DB ready boot work failed", so base turned a hostile value into that logged line and head logs its own warn instead (read, not booted). processExpiredDelegations has one non-test caller, `routes/delegations.ts:282` (admin route, platform roles only); through the REAL router over real HTTP the route returns 500 INTERNAL_ERROR at base for a revoked Proxy and a throwing message getter, and 200 "Processed 0 expired delegation(s)" at head, which is byte-identical to what an ordinary Error gives at base AND head. No outcome differs from the ordinary-Error outcome, so the tier is not raised; the 500 to 200 change for those two hostile kinds is the only behavioural move (author disclosed it).

## Findings
- **G158-F1 (info, positive)** - hostile values at head equal the ordinary-Error row at both catches.
  - FOUND: 0 of 15 hostile kinds reject, double-log, or go unhandled at head on either function; every row resolves (verify) / returns 0 (expire) and logs exactly once. Base REJECTS for 3 kinds per function (revoked Proxy, throwing message getter, Proxy whose get trap throws), 0 elsewhere.
  - TESTED: the real `delegationService.ts` with only `../db` replaced (query rejects with the value); console.warn/error replaced by recorders that also forward to the real console (forwarding never threw). Kinds: ordinary, revoked Proxy, message getter throws, Symbol message, thrown Symbol, null, undefined, BigInt message, throwing toJSON, throwing toString object (thrown and as message), null-prototype message, Proxy get-trap throws, toPrimitive returning object, number, string. 16 kinds x 2 functions x base/head = 64 runs, with a process unhandledRejection listener and a setImmediate wait.
  - HOW: positive control = the base rejects (6 rows) and base logs non-strings (symbol, bigint, object types) which the head turns into strings ("Symbol(s)", "10", "unreadable thrown value"). Raw: `logs/matrix.jsonl`; harness `harness/g158_matrix.test.ts.moved`.
  - Detail: for null, undefined, number, string and a message-less object the logged value is `undefined` at base AND head (no message to read), unchanged; this differs from the ordinary-Error row only in log text, not in outcome.
- **G158-F2 (info, positive)** - the admin route, real Express router, SYSTEM_ADMIN principal, `../db` replaced, real winston logger wrapped to record, 8 value kinds x base/head. Head: 200 "Processed 0 expired delegation(s)", 0 winston error lines, 0 unhandled, for every kind. Base: 500 for revoked Proxy and message getter (route logs "Process expired delegations failed" at error), 200 for the rest. Control: a non-admin role gets 403 (the route really ran); base 500 rows and their winston line are the positive control. Raw `logs/route.jsonl`.
- **G158-F3 (low, pre-existing, base = head)** - the expire route answers 200 "Processed 0 expired delegation(s)" when the UPDATE actually failed (an ordinary Error already did at base: row `ordinary` is 200 at base and head). Holds as the author said. The PR extends that same misleading success to two more value kinds. Not caused by this PR; a candidate follow-up ticket (service could return/throw a failure signal), not a merge blocker.
- **G158-F4 (low, test gap)** - two mutants survive the 6 committed cells, at both sites: M2 `String(m)` -> `m` (a Symbol, BigInt or hostile-object `message` is then logged raw, not as text) and M4 `err?.message` -> `err.message` (a null/undefined thrown value logs the constant instead of undefined; outcome unchanged because the inner try catches the TypeError). The committed cells use only a revoked Proxy and a getter, so no cell throws a Symbol/BigInt message or null/undefined. The product behaviour is correct (F1 measured it); only the pin is missing. Positive control: with M2 applied my matrix shows loggedType symbol/bigint/object for those rows (`logs/matrix_m2.jsonl`), so the instrument fires.
- **G158-F5 (info)** - gate-155 class check on this PR's own test file: tsc with tests included (`tsconfig.g158.json`, an untracked scratch config extending the service one) 0 errors at head and 0 with base product + new test; no script-style collision here (the file imports from vitest).
- **G158-F6 (info)** - docs-fragments check rc 0 "lint clean, render passes html_docs_check"; it prints 2 ADVISORY "committed page differs from the render" lines that appear identically on plain develop (`logs/docs_check_develop.log`), so pre-existing. Planted defect (unbalanced tags appended to the flow fragment) gives rc 1 with 2 findings; restored byte-for-byte, rc 0.

## Figures (Node v26.8.1; load average ~12-14, so `--maxWorkers=2` as the author)
| Item | Author | Measured here |
|---|---|---|
| Transfer suite base (new test excluded, base product) | 11 files / 139, rc 0 | 11 files / 139, rc 0 |
| Transfer suite head | 12 / 145, rc 0 | 12 files / 145, rc 0 |
| Red-first (new test, base product) | 4 of 6 fail, 2 controls pass, by assertion | 4 failed (R1-R4), 2 passed; all AssertionError `expected { threw: true } to deeply equal { threw: false }`, no timeout |
| tsc service | 0 | 0 (rc 0, empty) |
| tsc tests included | 0 | 0 at head, 0 at base product + new test |
| eslint, 2 changed ts files | clean | rc 0, no output; planted `debugger`/unused var gives rc 1 (2 errors, 1 warning), restored byte-equal |
| docs-fragments | rc 0, planted rc 1 | rc 0; planted rc 1; restored rc 0 |

Mutants (14 = 7 per site, applied to the head product file, run against the committed test file only; a run counts only if a vitest `Tests` summary printed, because my first pass was invalid: the root `npm ci` had emptied the service's node_modules, so every run "failed" and was falsely KILLED. I discarded it, reinstalled, and added that guard). Killed 12 of 14: constant to undefined, constant text changed, inner catch rethrows, log field blanked, read hoisted out of the try (each at both sites). Survived 2 per site as above: M2 and M4 (F4). Source restored (`cmp` equal to the head copy; clone status shows only my untracked scratch tsconfig).

## merge-tree
`git merge-tree --write-tree gh/develop FETCH_HEAD` rc 0, tree b06758cb3f929dcbcd1ecab4e4fe960a1def13c8; the tree differs from develop in exactly the PR's 4 paths (the new test, `delegationService.ts`, the cheat and flow fragments).

## Install route
Root `npm ci --workspaces=false --ignore-scripts` works and ESLint runs from `Blockchain/Dev`. Each install at one level empties the others' node_modules (workspace hoisting), so I re-installed the service with `--workspaces=false`, rebuilt `packages/shared` and symlinked `node_modules/@secuura/shared` as the Dockerfile does (`logs/npm_ci_*.log`).

## NOT TESTED
- A real Postgres/pg pool, a booted transfer service, the real `index.ts` boot path and `db.ts` `runDbReadyHook` with a hostile value (read, not run; the boot-hook claim rests on the code and on the base rejection I measured).
- Whether a real hostile thrown value occurs in practice; the `processExpiredDelegations` UPDATE against a real table.
- Other KS-1868 sites, the four platform suites, whole-suite CI, default-worker runs under load, Node 24, production logging (file transports).
- docs-fragments numbering at merge time (provisional).
- No background process of mine is running (ps checked). Nothing deleted; scratch left in the workdir: `w/repo` (with `tsconfig.g158.json`), `w/dev` (develop worktree of my clone), `harness/`, `logs/`.
