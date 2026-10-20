VERDICT: GO WITH NOTE at head b5d65c8e0651... (tier 1, round 1 of 2; landing tree 7169421a85cb1b275c63d19531cf0217bc3549a8 on develop f01ba49da56d3d55204caa02ab3348f94d63b9c0; 0 blockers, 6 notes)

Gate CE1, PR #1666 (KS-758 F9, option (b)), Opus 5.5. Card state is as stated in the brief and claim (`secuura-ks758-erasure-log-subject-ref-1020` open, default (b)). I did not re-read the card myself; a GO from Wednesday names it.

## BLUF
The product change does what the claim says. The unresolvable branch writes exactly ONE `data_deletion_log` row. Its column list matches the retention writer's. I ran its exact bound values against a real Postgres 18 schema (migrations 001 + 036) and the row inserts, with positive controls that refuse. The reason is a bare category and the row carries no external_ref, tenant id or PII. The never-seen / already-erased branch logs with `cause` and writes no row. Fail-soft holds because every statement is its own transaction, so a failed INSERT cannot roll back the blanking. Suite by cell name: 135 suites, 1576 -> 1582, +6, 0 vanished, 0 failed. My 6 red-proof arms all red; 3 extra gap probes survive (notes N2, N3). No blocker. The notes are about what the tests do not pin and about the identifier in LOG LINES. The ruling covers the table, not the logs. Kam/Wednesday should say whether (b) reaches the logs.

## Heads
- Start 02:52:57Z, live ls-remote on github.com:Secuura/Distributed_Secuura: #1666 b5d65c8e0651a780fd594f4859d1f6282256d051, develop f01ba49da56d3d55204caa02ab3348f94d63b9c0. Both match the brief and the claim.
- End 03:00:04Z: the same two shas, unchanged.
- The local cache mirror (spark/cache/src) has a STALE develop c56dd7c32edf. I fetched from GitHub directly and did not use the cache's refs.
- Landing on live develop: `git merge-tree --write-tree gh/develop gh/pr1666` gave 7169421a85cb1b275c63d19531cf0217bc3549a8, rc 0, one line. That equals the claimed landing. A real `--no-ff` merge in the scratch clone has the same tree, `HEAD^{tree}` = 7169421a85cb.
- Merge-base is 3a6f1810981e. Develop moved by one file since then, an m365-integration test, so nothing in originate differs between merge-base and develop.

## Findings

### Q1 Scope and product diff
Three-dot shows 2 files, +197/-0: `Blockchain/Dev/services/originate/src/services/gdprService.ts` +52 and `.../__tests__/ks695-erasure-by-external-ref.test.ts` +145. The claim names the test file without `.test`, but the tree has `.test.ts`, a cosmetic difference. I read the whole product diff. It touches only the two unresolvable sub-branches of `executeErasureByExternalRef`:
- (a) never-seen / already-erased (gdprService.ts:1475-1491): adds a `logger.info` with `externalRef, connectorId, cause: provenanceRows === 0 ? 'ref-never-seen' : 'already-erased'`. It writes no row and still returns `{completed, alreadyErased:true}`.
- (b) blanking (1492-1541): after the UPDATE it adds one fail-soft INSERT and a `logger.error` in the catch. The return value is unchanged.
The resolvable path is untouched.

### Q2 The row can be inserted
- Schema read at 001_initial-schema.sql:473-483 plus 036_deletion_log_crypto_shred.sql. NOT NULL columns: `id` (PK, default uuid_generate_v4()) and `data_type`, VARCHAR(100), with NO CHECK. Everything else is nullable. The only CHECK is on `deletion_method`: hard / soft / anonymize / crypto-shred. The brief's premise needs one correction: `data_type` has no CHECK. Only NOT NULL constrains it.
- Same pair as the resolved path: gdprService.ts:616 `logDeletion(userId, dsrId, 'action_provenance', provenanceCount, 'anonymize', ...)` and new :1529 `'action_provenance' ... 'anonymize'`. The pair is identical.
- Column list: new `(data_type, records_affected, deletion_method, reason, performed_by)` is byte-identical to the retention writer at :470. That writer uses `$queryRaw ... RETURNING *`; the new code uses `$executeRaw` and no RETURNING, which is fine because nothing reads the row back. `user_id` and `dsr_id` are nullable FKs, so omitting them gives NULL. That is legal and verified below.
- REAL POSTGRES, no Docker: Homebrew `/opt/homebrew/opt/postgresql@18/bin` (18.3). I ran initdb into the scratch clone's folder and served on 127.0.0.1:54399; a unix socket would not work because the path is over 103 bytes. I applied 001 (rc 0) and 036 (rc 0). `\d data_deletion_log` confirms the shape above.
  - Prepared statement, the product's exact five-column INSERT. `('action_provenance', 3, 'anonymize', '<the exact category string, em dash included>', 'connector:conn-123')` gave INSERT 0 1. The same with records_affected 0 gave INSERT 0 1. Read back: user_id NULL, dsr_id NULL.
  - Positive control 1: deletion_method 'blank' was refused with `data_deletion_log_deletion_method_check`.
  - Positive control 2: data_type NULL was refused, NOT NULL.
  - Limit: this proves the row against the schema built FROM THE MIGRATIONS, not against the live database. Drift on the live CHECK stays unproven. There is also no RLS on this table: no migration after 001 mentions `deletion_log` (case-insensitive grep, positive control: 036 and 001 both hit).

### Q3 No subject identifier anywhere new
- The ROW carries data_type 'action_provenance', records_affected (an integer count), deletion_method 'anonymize', a reason that is a fixed literal category with no interpolation, and performed_by `connector:<connectorId>`. There is no external_ref, tenant id or PII in the row. CLEAN.
- The LOG LINES are not clean of the ref. NOTE N1, below.
- performed_by and KS-1696, a judgement as asked, no remedy. `connectorId` is the connector principal's `user.userId` minus its prefix (routes/gdpr.ts:475). That is an identifier of the calling integration, not of the data subject. It is NOT a new exposure: the resolvable path already writes `connector:<id>` into this same table on every connector erasure (`executeErasureImpl(userId, dsrId, performedBy)`, :1405, then `logDeletion(..., performedBy)`). Through KS-1696, other tenants' ORG_ADMINs could already read connector ids. This PR adds rows of the same kind. I judge that acceptable for this PR. The exposure belongs to KS-1696.

### Q4 Fail-soft
- Mechanism: `prisma` in originate (db.ts:176-205 single-tenant, :69-70 multi-tenant pool) runs EACH raw statement in its OWN transaction: BEGIN, set_config, statement, COMMIT. The blanking UPDATE has committed before the INSERT runs. A failed INSERT is caught at :1531 and the function still returns `{completed, alreadyErased:false}`. So the erasure stands and completes.
- Failure logged WITHOUT the identifier? NO. The `logger.error` at :1532 carries `externalRef` (see N1).
- Judgement on fail-soft: I think it is the right choice. Throwing would 5xx an erasure that is complete and irreversible, against an unbounded retrier. And a retry would NOT rewrite the row, because `remaining` would be 0 and the code would take the never-seen branch. So throwing buys nothing and costs the spin.
- What is lost if the INSERT fails: the only Art. 17 accountability record for that erasure. There is no retry path and no reconciliation. In PRODUCTION FILE logs, `utils/logger.ts:65-78` keeps only an allow-list (timestamp, level, service, message, requestId, method, path, statusCode, error). So the durable trace is the message plus the error text, without externalRef, connectorId or rows. The full context reaches only the Console stream. Losing it is quiet, not silent. NOTE N5.

### Q5 records_affected
- It is `blanked`, the rowCount the blanking `$executeRaw` returned (:1492), bound directly at :1529. It is read at source.
- There is no `> 0` guard, unlike every `logDeletion` call on the resolved path, so a 0 would be written. In practice 0 is unreachable: the branch is entered only when `remaining > 0`, and the UPDATE has no identity-not-null filter, so it matches at least those rows.
- Consequence of that missing filter: the count is "provenance rows for this ref in this tenant", which includes rows already blanked earlier. It is not "rows whose identity was removed by this run". It can over-count on a second partial erasure. This comes from the pre-existing UPDATE, not from the new code.
- The test does not pin the count (N2).

### Q6 Red-proof
Harness: `harness/mutants.py` in the scratchpad. For each arm it applies an anchored edit (anchor asserted to occur exactly once), runs the product `tsc --noEmit -p originate/tsconfig.json`, runs jest on the test file only (46 cells), and classifies each red as ASSERT (an expect matcher) or OTHER (a thrown error). It then restores with `git checkout` and asserts sha256 equality. Product sha256 fa920dd0ebb3...e5d2 before and after: restored-equal True on every arm. Every arm had tsc rc 0 BEFORE its run counted.
| arm | red cells | by |
|---|---|---|
| A0 none (control) | 0/46 | n/a |
| A1 INSERT removed (author) | F1 F4 | ASSERT; F2 F3 FC1 also red but by TypeError (`deletionLogWrites()[0]` undefined) |
| A2 option (a) reason (author) | F2 FC1 | ASSERT |
| A3 fail-soft removed (author) | F4 | thrown rejection propagating out of `await`, NOT an expect (N4) |
| A4 row on never-seen branch (author) | F5, plus 2 pre-existing cells ("already blanked writes NOTHING", "NEVER SEEN ... must never 404") | ASSERT |
| M1 mine: deletion_method 'crypto-shred' (passes the CHECK, wrong meaning) | F1 | ASSERT |
| M2 mine: reason + ' ref=' + externalRef | F2 FC1 | ASSERT |
| M3 probe: records_affected hardcoded 1 | NONE, survives (N2) | n/a |
| M4 probe: reason + externalRef.toUpperCase() | NONE, survives (N3) | n/a |
| M5 probe: `cause` labels swapped | NONE, survives (N3) | n/a |
| M6 probe: performed_by `connector:${connectorId}:${tenantId}` | F1 | ASSERT |
The 4 author arms reproduce the claim's cell sets exactly. The claim's "cell red by assertion" holds for A1 (via F1/F4), A2 and A4. For A3 it holds only loosely (N4).

Suite by cell NAME. Whole originate jest, `--json`, on live develop f01ba49 and on the PR head; originate is identical at the landing:
- develop: 135 suites, 1576 tests, 0 failed.
- head: 135 suites, 1582 tests, 1582 passed, 0 failed, 0 pending.
- Set difference by (file, fullName): 0 vanished, 6 added (F1 F2 F3 F4 F5 FC1, all in the KS-758 F9 describe), 0 duplicate names. The 6 additions are the comparator's own positive control.

Test file type-checked in its OWN program, outside the push gate (KS-1090):
- Scratch tsconfig extends originate's (strict, noUnusedLocals) with `files: [the test file]` and `types: [jest, node]`.
- rc 0, 0 `error TS` lines. `--listFiles` shows the test file, gdprService.ts and @types/jest in the program.
- Positive control: I appended `export const __gatePc: number = "not-a-number";` and got rc 2 with `TS2322` at the test file (882,14). Restored by `git checkout`, sha256 711c46e7...28a8 equal before and after.
- The product `tsc --noEmit` at the landing is rc 0.

## Notes (none blocks)
- N1 (identifier in new LOG LINES, the main item for Wednesday/Kam). Both new log lines carry `externalRef`: the never-seen/already-erased `logger.info` at :1486 and the INSERT-failure `logger.error` at :1532.
  - Before this PR the never-seen branch logged nothing. It now writes a Platform-S subject ref that K never held into the Console stream.
  - Console redaction (`SENSITIVE_LOG_KEY`, logger.ts:45) does not match `externalRef`. The production FILE allow-list drops it.
  - This matches house convention: 20 `externalRef,` log sites in gdprService.ts, including the pre-existing blanking-branch info line at :1538. The author's comment says so openly.
  - Option (b) as worded governs the deletion-log row and the API surface, and the row is clean. Whether (b) should reach logs is a ruling for Kam. I am not proposing a remedy.
- N2 (records_affected unpinned). F1's `expect(vals[1]).toBe(1)` equals the value the mock returns for EVERY `$executeRaw`, so a hardcoded `${1}` survives (M3). Q5 is verified by reading the source, not by the test.
- N3 (two assertions weaker than they read). F2's containment is case-sensitive, so an uppercased ref in the reason survives (M4). The `cause` field is asserted by no cell, so swapped labels survive (M5). Both pass today.
- N4 (red by assertion, strictly). A3 reds F4 only because the rejection escapes `await executeErasureByExternalRef(...)`, not through an expect such as `resolves.toEqual`. A1's F2/F3/FC1 reds are TypeErrors. The claim's "cell red by assertion" is loose for those cells. Each arm still has at least one genuine red.
- N5 (fail-soft trace in prod files, judgement). A failed log INSERT leaves only the message and the DB error text in the production log files: no connector, count or ref. Reconstructing which erasure lacks its accountability row would need the Console stream.
- N6 (unmeasured, minor). Two concurrent POSTs for the same unresolvable ref can both see `remaining > 0`. Both would blank and both would write a row, giving duplicate accountability rows. Not exercised.

## FOUND / TESTED / HOW
- FOUND: product diff read whole; the function read whole (:1326-1543); db.ts transaction model; tenant-guc.ts; logger redaction and file allow-list; migrations 001 and 036; retention writer :470 and logDeletion :916; route caller and connectorContext.
- TESTED:
  - Real-Postgres INSERT with 2 positive controls.
  - Whole originate suite at both ends by cell name.
  - Test-file own-program tsc with a positive control.
  - Product tsc.
  - 11 mutant arms: 4 author arms, 2 of mine, 4 gap probes, plus A0.
  - merge-tree and a real merge on live develop.
  - ls-remote at start and end.
- HOW: `git clone --shared` of the cache into the scratchpad `gate_ce1/src`, with an added `gh` remote to GitHub using the Blockchain deploy key for read-only ls-remote and fetch only. `npm ci --ignore-scripts --prefix <clone>/Blockchain/Dev`, then `npm run build --prefix packages/shared`, then `npm run generate --prefix services/originate`. No cd, no rm, no Docker, no push, no GitHub/Linear writes, nothing under !CODING.

## NOT RUN
- The product function end-to-end against Postgres. The INSERT was proven with psql using the product's SQL and values, not through prisma or adapter-pg.
- The live database's actual CHECK.
- The 4 platform/integration suites (no stack).
- Prisma's error-message shape for a real 23514 (whether DETAIL "Failing row contains" reaches `err.message`). The failing row holds no ref either way.
- Concurrency (N6).
- The KS-758 F6 half and KS-1696, both out of scope by brief.

## Wall-clock
02:52:42Z to 03:01Z (about 9 min). Postgres stopped cleanly at the end.
`git -C /Volumes/DevMASTER/WEDNESDAY status --short` before writing: every untracked path is under 0_Brain/ or 2_Project_Files/local-model/ or 2_Project_Files/fleet/briefs_staged/. None is outside the allowed set.
sha256 (sed '1d;$d' verdict.md | shasum -a 256): 2809a664f07cfc920efb781332a4e7a451bbd817af93a2af1dde16f7d390bfa3
