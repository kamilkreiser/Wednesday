PR 2263: GO WITH NOTES (at head 2e8b9fffd91fa21b1a079b65d09aa014b9525544; tier 1)

# Gate 386, tier 1 (Opus), PR 2263 (KS-2280), 2026-11-20 ~07:51-08:05 AEDT

## Pins
- Pinned twice with gh api: at 07:51:16, before the first measurement, and at 08:04:11, before writing this.
  - Both times: open, not merged, not draft. Head 2e8b9fffd91f, base 718b15bbeb20, develop 718b15bbeb20, updated_at 2026-11-19T20:47:52Z.
  - 1 commit, 7 files, +378 -1, mergeable true (state unstable: the retired Actions runs).
- The head's only parent is 718b15bbeb20, which is develop's tip. So **the merged state is the PR head**: a merge onto develop would be a fast-forward. I measured on the head and labelled it as the merged state.
- `git diff --stat develop..head` shows exactly the 7 paths and the counts in the commission.
- Closing keywords on KS-2280: 0 in the PR body and 0 in the commit message. Control: the string "Closes KS-2280" matches 1, and "Refs KS-2280" appears once in the commit.

## How I measured
- **Clone.** My own clone at `_work/g`, made from the GitHub URL with `--reference-if-able <shared checkout> --dissociate`, so no alternates file is left. The shared checkout was only read.
  - I fetched develop and refs/pull/2263/head INTO MY CLONE ONLY, over https with the gh credential helper (read-only on GitHub).
- **Three worktrees:** `_work/h` (the head, which is also the merged state), `_work/d` (develop 718b15bbeb20) and `_work/x` (the head again, for mutants only).
- **node_modules.** APFS-cloned (`cp -c`) from s-w45-ks2280, which I only read: the root, packages/shared, services/api-gateway and services/shared. For h only, I also cloned the five other ratchet-gated services' trees.
  - The absolute self-link `node_modules/node_modules`, pointing into s-w45-ks2280, was moved to `_work/_quarantine/{h,d,x}/nm_selflink`.
  - 0 absolute links remain in any tree. Control: 112 relative links remain under each root node_modules.
- **dist.** packages/shared/dist was NOT copied; I built it myself with `tsc` (rc 0) in every tree. Control: 4 runtime-role files in h's dist, 0 in d's.
- **Run conditions:** Node v26.8.1, vitest 4.1.12, TMPDIR /private/tmp/g386t. load1 ran 4 to 11.
  - The whole suites ran while load1 was 9 to 11, briefly. Both arms ran under the same conditions and their results equal the builder's, so I do not count the load as a confound.
- **Scripts:** `_work/mutants_g386.py`, `_work/suites_g386.sh`, `_work/run_cwd_g386.py` (runs a command with a set cwd, so there is no `cd`), `_work/eslint_g386.mjs`.
- **Evidence:** `_work/evidence/`.
- **One slip of my own, fixed:** my first suite run used the wrong cwd, and 9 repo-wide guard files in packages/shared could not find the Dev root. I re-ran every suite with cwd set to the package. The wrong-cwd outputs are in `_work/_quarantine/evidence_cwd_wrong/`.
- **End state:**
  - After every mutant, the product bytes were restored and sha256-checked: runtime-role-guard.ts 0a7235a5ad37, index.ts 9bdc79a8ec6b. These equal the builder's stated hashes. db.ts was restored to eb7887ec9e39.
  - h, d and x each show 0 porcelain lines.
  - All planted files and probe files are in `_work/_quarantine/{planted,probes}/`.

## Q1. Does the PR meet every clause of THE SPEC? YES, all ten clauses (read at source, then measured)
| clause | where (head) | measured by |
|---|---|---|
| WARN by default | index.ts 1273 | G5, and my PGlite probe L1 (WARNING line with the flag unset) |
| REFUSE = `process.exit(1)` called by the guard itself, not a throw | index.ts 1269-1272 | M3a/M3b kill G1, G2, G6; probe L1 (`exitCalls [[1],[1]]`) |
| only on `DB_ROLE_GUARD=refuse` exactly; anything else warns | `=== 'refuse'`, index.ts 1269 | G5 (unset, `true`, `REFUSE`, ` refuse`, `warn`); see G386-2263-1 |
| FIRST in runDbBootTasks, BEFORE loadFromDb | index.ts 1288-1289 | Q7 (check after loadFromDb) killed by G1, G2 |
| therefore also on the KS-377 recovery path | db.ts 144 re-runs the same hook | Q16 (drop that re-run) killed by the existing db.retry cell "re-runs …" |
| unavailable or zero rows = warn and carry on | guard 41-50; index.ts 1262-1265 | G4, S4, S5; probe L2 (5 thrown shapes, refuse set, 0 exits) |
| rolsuper and rolbypassrls OR'd | guard 52 | M1, M2; P1 on real PGlite: SUPERUSER reads rolbypassrls false |
| logs = the two booleans + a fixed hint only | index.ts 1263, 1267-1273 | G6, and my own Q3 probes (below) |
| runDbBootTasks a named export | index.ts 1287 | the G-cells import it |
| startServer still does not run under vitest | require.main guard, index.ts 1358 | 0 "SECUURA API GATEWAY" banner lines in my probe output (control: 9 KS-2280 lines in the same file) |

Two clauses deserve a remark:
- **Spec wording vs code.** The 'unavailable' line also prints the error's TYPE name (`err.constructor.name`, or `typeof` for a non-Error), for example `query failed: Error`. Kam's card (a) allows "Type and field names only", so I read this as compliant. See G386-2263-2.
- **The real driver.** The strict-boolean shape check is safe against the real driver. pg 8.20.0's pg-types parses OID 16 `'t'` to the JS boolean `true`. Control: int4 parses to a number. So the gateway will not read every real box as 'unexpected row shape'.

## Q2. Mutants, reproduced myself on x (`mut_x.json`): every named mutant dies; TWO flag-match mutants survive
| mutant | shared cells failing | gateway cells failing |
|---|---|---|
| BASE | 7/7 pass | 6/6 pass |
| M1 drop rolsuper | S1, P1 | G2 |
| M2 drop rolbypassrls | S2, P1 | G1, G5 |
| M3a throw instead of exit | – | G1, G2, G6 |
| M3b no exit | – | G1, G2, G6 |
| M4 refuse when unavailable | – | G4 |
| M5 refuse by default (`!== 'warn'`) | – | G5, G6 |
| M5c refuse always | – | G5, G6 |
| Q1 case-insensitive (`toLowerCase`) | – | G5 |
| **Q2 prefix (`startsWith('refuse')`)** | – | **none: SURVIVES 6/6** |
| **Q3 `trimEnd() === 'refuse'`** | – | **none: SURVIVES 6/6** |
| Q4 `trim()` | – | G5 |
| Q5 `includes('refuse')` | – | G5 |
| Q6 session_user for current_user | S6, P1 | – (the gateway stubs the db) |
| Q7 check after loadFromDb | – | G1, G2 |
| Q8 check not awaited | – | G1, G2, G6 |
| Q9 exit(0) | – | G1, G2 |
| Q10 check only once per process | – | G2, G4, G5, G6 |
| Q11 unavailable is silent | – | G4 |
| Q12 reason carries err.message | S4 | – |
| Q13 warning prints DATABASE_URL | – | G6 |
| Q14 FATAL prints DATABASE_URL | – | G6 |
| Q15 truthy, not strict boolean (tsc error, dist still emitted) | S5 | – |
| Q16 recovery path drops the hook re-run (db.ts 144) | – | db.retry "re-runs" (22/23) |
| Q17 failed query reads bypass (tsc TS6133 only, dist emitted) | S4 | G4 |
| Q18 no row reads ok | S5 | – |

Notes on the table:
- Shared-side mutants rebuilt dist before their gateway run, and dist was rebuilt again from the restored source.
- Q15 and Q17 failed type-check, but tsc still emitted (no `noEmitOnError`). Q17's G4 failure shows the mutant reached dist.
- The builder's "M5b loose flag match (trim, lower-case)" holds as named. Prefix and trailing-space matches are not covered: G386-2263-1.

## Q3. Can the URL, the role name or a thrown error reach the log through the new lines? NO (measured, with a control)
The markers were assembled at runtime, so no source line holds them. I captured vitest output with `--silent=false`.
- **Control first.** My first capture, under the default reporter, showed 0 lines even for my CONTROL line. That zero was blind, and I discarded it. The verbose capture shows the CONTROL line once in each file.
- **Probe L1, real PGlite.**
  - Setup: three roles created with the marker in the name (SUPERUSER, BYPASSRLS, plain), under `SET ROLE`, and a marked DATABASE_URL (user, password, host and db).
  - Each role ran through the warn path, then the refuse path.
  - Result: `["role:exit","byp:exit","plain:no-exit"]`, 4 KS-2280 lines.
- **Probe L2.** The role query rejects 5 ways:
  - an Error whose message quotes the marked URL and user;
  - a custom `PgLikeError` naming the marked role;
  - an Error with a marked message;
  - a thrown string;
  - a plain object.
  - Result: 5 warnings, reasons `Error`, `PgLikeError`, `Error`, `string` and `object`.
- **Probe R1, the REAL db.ts → queryWithTenantGuc → pg Pool path.** No mock, with a marked URL on an unresolvable `.invalid` host and no server. Result: 1 warning, `query failed: Error`.
- **Grep over both captures** (`leak_pglite_v.out`, `leak_realdb_v.out`, `/usr/bin/grep -i`):
  - The marker appears in 1 line per file, the CONTROL line, and in 0 KS-2280 lines (control: 9 KS-2280 lines and 1 KS-2280 line).
  - 0 KS-2280 lines contain `postgres`.

## Q4. Suites, static checks, ratchet and fragments: CLEAN; the figures equal the builder's
- **api-gateway, whole suite:** d 2,071/2,071 in 181 files; merged (= h) 2,077/2,077 in 182. Failure-name sets equal (both empty).
- **packages/shared, whole suite:** d 1,718/1,723 in 86 files; h 1,725/1,730 in 87. Failure-name sets EQUAL. The 5 reds are exactly:
  - KS-1725 F and J;
  - KS-727 corpus 2 (two cells);
  - wallet-signature KS-278.
  - These are the commission's KS-1727 + KS-2281 four. Nothing else is red.
  - Positive control: the same JSON-reporter pipeline counted those 5.
- **tsc --noEmit:**
  - api-gateway rc 0; packages/shared rc 0.
  - The new shared test file, through a temp config in `_work/tsc_shared_test`, rc 0 (shared excludes `src/__tests__`).
  - Planted controls fired: gateway src TS2322 (rc 2), shared test TS2322 (rc 2).
- **Test-types ratchet (check.cjs), merged state, all six gated services:** 0 new and 0 stale each.
  - auth: 41 errors, all baselined.
  - api-gateway: 220 files, 15 errors, all baselined (develop: 219 files, 15).
  - vc-issuer, security, m365-integration and originate: 0 errors.
  - Planted gateway test: rc 1, new errors named.
- **eslint (API, cwd Dev):** 0 errors and 0 warnings on runtime-role-guard.ts, shared index.ts and both new test files.
  - Gateway index.ts has 2 warnings (no-namespace, an unused disable directive). Develop's index.ts has the same 2, so 0 are new.
  - Planted file: no-debugger error and no-unused-vars warning.
- **docs-fragments check:** OK on h ("301 new" flow and cheat, against develop's 300).
  - The 2 ADVISORY page-lag lines are on both arms.
  - Each new fragment holds 1 `<h2>`.
  - Planted two-heading fragment: rc 1, "must hold exactly one entry".

## Q5. What would boot differently TODAY with this merged and no flag? Nothing stops
- `DB_ROLE_GUARD` appears in no compose file, workflow, bicep or env file: 5 tracked hits, all in the PR's own files. Control: APP_DB_USER is in 14 tracked files.
- Unset, the code path can only `return` or `console.warn`. Every other value except the exact `refuse` warns too (G5, my Q1/Q4/Q5).
- What does change on each successful DB hook run (boot, and each KS-377 recovery):
  - one extra `pg_roles` query on the pool, outside any tenant scope;
  - then either nothing (a plain role), a WARNING with the two booleans (a superuser or BYPASSRLS role), or a WARNING "could not read …" (the query failed, no row, an odd shape).
- A box whose DB is down never reaches the hook, so degraded mode is unchanged.
- Only the gateway calls the check. Five other services keep their own module-private runDbBootTasks, untouched.
- **The PGlite cell:** it uses only the existing hoist.
  - No package.json declares `@electric-sql/pglite`. Control: 27 package.json files declare vitest.
  - The lockfile's dependents are @prisma/dev, pglite-socket and pglite-tools; the version is 0.4.1.
  - The PR touches 0 package.json or lockfile paths (control: 7 paths in the diff).
  - Tracked importers are now 4: ks1256, ks1673, ks1677 and ks2280. That makes it the "fourth KS-1694 importer", as claimed.

## Q6. The PR body and the KS-2280 facts comment (e11e8f2c): every factual sentence I could check holds
I read the PR body (gh api, 9,844 bytes) and the issue via Linear GraphQL (a read-only query).
- The issue is In Progress. Its one attachment is PR 2263, and it has one comment, e11e8f2c (3,167 chars).
- Verified at source:
  - **Dev-default password check:** develop index.ts 101-105 (102-106 at the head).
  - **docker-compose.yml:** line 427 `NODE_ENV=${NODE_ENV:-development}` and line 473 `${APP_DB_USER:-secuura_app}` both sit in the `api-gateway:` service (line 411). Every other NODE_ENV in that file is the literal `development`.
  - **DEPLOYMENT-ARCHITECTURE.md line 32:** the demo VM runs `Blockchain/Dev/docker-compose.yml`.
  - **deploy-demo.yml:**
    - line 35 is the `i_know_this_is_the_legacy_container_apps_path` guard input;
    - lines 60-61 refuse runs without it ("targets the DELETED Container Apps demo");
    - line 407 holds the one `secuuraadmin` hit, in job `deploy-services` (line 363).
  - **The demo correction stands:** demo's gateway role and NODE_ENV are UNMEASURED. It is worded that way in the PR body, the comment and the flow fragment.
  - **docker-compose.production.yml:** 18 DATABASE_URL lines, 18 on `${POSTGRES_USER}`, 0 on APP_DB_USER, over 18 services.
  - **Migration 039:** 25 tables in its array, FORCE at line 111.
  - **Migration 027:** "No FORCE ROW LEVEL SECURITY" (line 19). rights_holders is in neither 038 nor 039.
  - The PGlite facts (Q5); "no package.json or lockfile edit"; shared excludes `src/__tests__`.
  - All suite, ratchet, eslint and docs-fragments figures.
  - The mutant table, row by row, for the 10 rows I re-ran under the same names.
- Builder-only, NOT re-measured by me:
  - Kintsugi's gateway measured as secuura_app, false/false (no box allowed);
  - the pre-push hook's 13/16 legs, its timings and leg 14/15 figures;
  - the red-first run;
  - the standalone `preflight_test_types_ratchet_leg.test.sh` 48/0.
- One sentence is incomplete, though not false: G386-2263-3.

## Findings
- **G386-2263-1 (LOW, test coverage; not merge-blocking).** Two weakenings of the exact flag match survive all 13 cells, at the head and on the merged state.
  - `startsWith('refuse')` (a prefix match) and `trimEnd() === 'refuse'` both leave 6/6 gateway cells green.
  - G5 tries only `true`, `REFUSE`, ` refuse` (a leading space) and `warn`.
  - Either mutant would REFUSE (stop a box) on a value the spec says must warn, such as `refused`, `refuse-later` or `refuse ` (a trailing space, a common .env slip).
  - The product is correct today: it uses `=== 'refuse'`.
  - Suggested follow-up, Wednesday's call: add `'refuse '` and `'refusex'` to G5's value list.
- **G386-2263-2 (INFO, spec wording).** The 'unavailable' warning carries a fixed phrase plus the thrown value's TYPE name, for example `query failed: Error` or `PgLikeError`.
  - That is within card ks1346 = a ("Type and field names only"). It is slightly wider than the spec's literal "two booleans and a fixed hint ONLY".
  - No value reached the log in any probe (Q3).
- **G386-2263-3 (INFO, PR body).** "Unset, the gateway behaves as before plus one warning line on a superuser or BYPASSRLS role" leaves out two things:
  - the extra `pg_roles` query on each hook run;
  - the "could not read the database role's attributes" warning when the query fails, returns no row or returns an odd shape.
  - Both are harmless and are stated elsewhere in the body ("unavailable never refuses"). This is not a false fact.
- **G386-2263-4 (INFO, coverage shape).** The gateway cells all stub `../db`, so no committed cell drives the real query → queryWithTenantGuc → pg path.
  - I measured that path by probe: pg parses bool to a JS boolean, and the real-pool failure path gives the warning, with no leak.
  - It is not pinned by a test. Not blocking.
- **Not this PR (pre-existing, for routing only).** `Blockchain/Dev/docker-compose.yml` line 473 carries a literal default `APP_DB_PASSWORD` fallback inside the gateway's DATABASE_URL (not quoted here). This PR did not add it.

## Not run / not measured
- Node 24 (not installed); any live stack, container, database server or box (in-process PGlite only); the pre-push hook and its 16 legs; the four platform suites; Kintsugi or demo.
- Other services' suites: the PR touches only packages/shared, api-gateway and fragments. Shared consumers were covered by the whole shared suite and by the six-service ratchet, not by their own suites.
- I did not read the builder's evidence files as results.

Nothing was written to GitHub, Linear or any !CODING path. No mail was sent, nothing was launched, no process was killed, and no sub-agents were used.
