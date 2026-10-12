# Gate brief: Secuura Platform K PR #1527 (ticket KS-1549, P1), OPUS tier 1 — concurrency on a credential path

Commissioned 2026-10-13 ~06:4x AEDT by the Wednesday seat.

## What you are gating
- Head `a430061c9d46d24498a5c83524889dba3dc009c7` (Wednesday's ls-remote), one commit on develop 69878dc5; develop is now `81ac1ea60ec684f1636a25832d9a7f3bf28470f5` (test files in governance/staking/transfer only; author says zero overlap; not merged in). Author V 5th. 6 files, +440/-52 per GitHub.
- The bug (measured by an earlier gate on develop): two concurrent key rotates on one connector leave 0 active keys (9 of 10 double-submits on real Postgres).
- Approved shape (Wednesday 18:56Z): rotate+connectorId path runs one transaction on ONE pooled client: runWithTenantId -> transaction(client) -> applyTenantGuc(client) -> pg_advisory_xact_lock(hashtext(tenant), hashtext(connector)) -> INSERT on the same client -> SAVEPOINT -> retire with RETURNING id (on failure ROLLBACK TO SAVEPOINT, priorKeysRevoked null: KS-577's contract) -> in-memory map updated for exactly the returned ids inside the lock, undone if COMMIT fails (KS-888's contract). Decision D (Wednesday): "the last rotate wins". Memory-only path unchanged.
- Author's numbers (NOT evidence): integration cells CONTROL (RLS binds), E3 (20 sequential -> 1 active), E1 (double-submit x10), E2 (N=20, memory agrees with DB), E4 (grace mode), E5 (two connectors), E6 (N=30 past pool max 10), E8 (forced retire failure -> 201, priorKeysRevoked null, new key saved, prior live): develop E1/E2/E4/E5/E6 red, head 8/8 over four runs; mutants killed (lock removed; INSERT on a second connection; GUC not applied; memory not told; handler reverted; savepoint removed -> E8 alone); survivor: lock keyed on tenant only (coarser, equivalent). "One transaction, no lock" gives TOO MANY active keys. Unit 30 files / 331; shared 949; tsc, eslint clean.

## How to get the code (READ-ONLY on the project)
- `git clone --shared` of `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files` into YOUR scratchpad; fetch `refs/pull/1527/head` with the project's `core.sshCommand`, or use `/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-10-12_seatV-5th/bundles/ks1549-a430061c9d46.bundle` (sha256/16 c82bc4e328fe8589, verified; needs 69878dc5). Assert the head.
- Build your OWN throwaway Postgres 15 (author's recipe: initdb -U secuura --auth=trust; start with unix_socket_directories='' listen_addresses=127.0.0.1 on a free port 55420-55429; CREATE DATABASE secuura; the repo's docker/init/* in order with a throwaway APP_DB_PASSWORD; create secuura_platform by hand if the dblink step fails; DATABASE_URL=... sh scripts/run-migrations.sh -> expect applied=50 failed=0; confirm svc_api_keys has FORCE RLS). Stop it when done. No pushes, no GitHub/Linear writes, no remote boxes.

## What to attack
1. Re-run E1-E8 at the head and at develop (red/green as claimed), as the app role, stable over repeated runs.
2. Your own concurrency shapes: N=2..50 mixed rotate and non-rotate mints on one connector; rotates on the SAME connector id across TWO tenants (the lock key includes tenant: confirm no cross-tenant serialisation or leak); hashtext collisions (two different connector ids whose hashes collide must still each end with one key: find or construct a collision, or argue it measurably); a client killed mid-transaction (the xact lock must release); the KS-757 trap (INSERT on another pooled client) re-measured.
3. The contracts: KS-577 (a failed retire keeps the mint, priorKeysRevoked null) and KS-888 (a failed COMMIT returns no key and leaves memory unchanged): force both failures yourself.
4. The in-memory map: after concurrent rotates, the map a validation reads agrees with the DB exactly (active ids, expiries in grace mode).
5. pgbouncer is NOT exercised by the author. If you can run pgbouncer locally in pool_mode=transaction in front of your Postgres, run E1/E6 through it; otherwise say UNMEASURED and why.
6. The test infrastructure: vitest.config.ts excludes *.integration.test.ts; vitest.integration.config.ts and test:integration exist; the integration file throws (never silently skips) without TEST_DATABASE_URL.
7. Suites at the head: services/security unit, shared 949.

## Output
- `0_Brain/reference/2026-10-13_gate-pr1527/verdict.md` (this folder only, plus your scratchpad; raw outputs under `evidence/`, never a directory named `out`). Head under test; numbers with instruments and controls; FOUND / TESTED / HOW; NOT tested.
- VERDICT: GO / GO WITH NOTE / NO GO; Majors and Minors with file:line and the reproducing shape.
