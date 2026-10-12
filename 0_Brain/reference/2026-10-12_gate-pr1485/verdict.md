# Gate PR #1485 (KS-968): verdict GO WITH NOTE

**Head:** `ebdb123d5963e9c95d8bb223b08e58128cd38cb7`. The predicted merge over develop `6fa9bf7bd7863c6e0830f1a48d513cde8169d034` is `19a8877`, clean.
**Gate:** independent Opus gate, 2026-10-12. Everything was read-only on the Secuura repo. I used my own clone and my own throwaway Postgres 15 on port 56488 (init SQL with 0 failures, 49 migrations applied, 0 failed). The cluster was deleted afterwards.

## By my runs
- **Diff scope:** 6 files: userRepo.ts, the ks949 unit test, the integration suite, its config and README, and the root package.json.
- **Integration suite:** 6/6 on head (twice) and 6/6 on the merged tree. Running head's suite against develop's userRepo.ts gives 2/6 RED: the both-rows cell (`['active','LIVE-B']`) and the failure-named cell.
- **Harness controls:**
  - With the variable unset, the suite throws.
  - Host 10.1.2.3 is refused.
  - A database named `postgres` is refused.
- **Mutants:** 11 tried, 9 killed. The seat's three (m1 to m3) were all killed. Of my eight, six were killed. Two survived: **m5**, where the catch no longer rethrows, and m9, which is near-equivalent.
- **services/auth:**
  - Head: 89 files / 927 tests, green twice.
  - Merged: 90 files / 934 tests. Run 1 had 1 timeout, the ks949 "enumeration … planted" cell at 5003ms, a pre-existing cell under load. Run 2 was green, and that file ran alone 3 times on the merged tree, 31/31 each time.
- **Static checks:** tsc 0 errors and check:test-types 42/42 baseline with 0 new, on both trees. eslint shows 0 errors and 15 warnings, the same as the seat's.
- **State probes** (`logs/probe_*.json`; head vs develop):
  - Both rows, 3 boots in sequence: idempotent, the email row is suspended, the id row is untouched, 0 errors. Develop logs 3 errors and leaves the credential live.
  - Two concurrent boots: same result as the 3-boot run. Develop logs 2 errors.
  - An empty ADMIN_USER_PASSWORD is treated as unset.
  - The id row is never locked out in the both-rows state.

## Defects (all Minor, no Major)
1. **Minor: the harness's loopback guard can be bypassed.** See integration/ks968-…integration.ts:29-36. The guard checks `new URL(RAW).hostname`, but pg-connection-string lets `?host=`/`&port=` override it. Measured: a URL with host `127.0.0.1:1` plus `?host=<socket>&port=56488` ran 6/6 against another target, and `?host=192.0.2.1` dialled that address. Fix: validate the parsed config, or reject any query string.
2. **Minor: the rethrow is not pinned by any test.** See userRepo.ts:1654. Mutant m5 passes both suites (6/6 integration, 31/31 unit) while logging the false "SUSPENDED" warn.
3. **Minor: not every failed remediation gets the new error line.** The `getUserById`/`getUserByEmail` lookups at userRepo.ts:1589-1590 sit outside the named try. A database fault there still logs only the generic "Failed to seed demo user". This is from reading the code; I did not run it.
4. **Minor: the integration file has 4 tsc errors** (lines 114, 147, 163) under tsconfig.test.json. No typecheck, CI job or preflight covers the file, and the suite runs by hand only.
5. **Minor: "otherwise unchanged" is not exact.** When the email row is a legacy plaintext row with no lookup hash, develop suspended both rows (no collision occurred). Head leaves the id row ACTIVE.

## Notes (all of these behave the same on develop)
- If ADMIN_USER_PASSWORD is whitespace, head seeds that password and the account is ACTIVE.
- The recommended rescue of setting ADMIN_USER_PASSWORD first re-arms the **email row**, not the id row. That row is promoted to system_admin and ACTIVE, even when it was an OWNER.
- Two legacy plaintext duplicates of the address: only one is suspended (`LIMIT 1`).
- In the id-only state the id row is still suspended and renamed. So if the suspended email row is later deleted, the next boot locks out the operator's own id row.
- **Other places in the loop that swallow 23505:** the H5 rewrite at :1706 and createUser at :1758. Both can only hit it through a race, and both log only the generic line. The email arm writes no unique column, so it cannot raise 23505.
- **What the logs leak:** the address, the database error message and the error code. Neither the hash nor the detail text appears.
