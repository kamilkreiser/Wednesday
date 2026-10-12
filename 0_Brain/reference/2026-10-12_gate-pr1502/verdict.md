# QA gate: Secuura Platform K PR #1502 (KS-753)

- **Head:** `5daf8830dc46b465ec167985353b7c7ee552fd45` (bundle `ks753_b_5daf8830.bundle`, sha256/16 `4736169da01e7e43` matched, `git bundle verify` ok, prerequisite `06d33fb4b321c77270ff958f9db6accc5a622da8`), branch `feature/ks-753-timestamping-fail-closed-a-mock-tsa-fallback-must-not-report`, 1 commit on 06d33fb4.
- **Base gated against:** real current `origin/develop` = `8ea75e7cb60d257fc3b0244bb177ef2dd524312f` (fetched read-only 2026-10-12; KS-1359). Develop is 1 commit past the PR's parent and touches only `api-gateway` (platform.ts + its test). `git merge-tree --write-tree origin/develop 5daf8830` merged with no conflicts, rc 0, tree `0c1a0e99`. The timestamping tree is byte-identical between the head and the merge result: 0 diff lines, against 3 lines for api-gateway as the positive control. Every result below therefore also holds on the merged tree.
- Gate: OPUS tier, independent (not the author). Clone and runs were all in the scratchpad. Nothing was pushed and nothing was written to GitHub or the ticket.

## VERDICT: GO WITH NOTE

Both doors are closed. Creation no longer reports, persists or stamps `verified`/`verified_at` for a mock rfc3161 token, and `/verify` honours the stored column. I proved this on real Postgres rows as well as in unit tests. No consumer outside the timestamping service reads `verified`. The notes cover defence-in-depth and work to carry forward, not defects in this diff.

## By my runs

| Check | Result |
|---|---|
| Timestamping suite, head, run 1 | **8 files / 96 tests passed**, rc 0 |
| Timestamping suite, head, run 2 | **8 files / 96 tests passed**, rc 0 |
| `tsc --noEmit -p services/timestamping` | rc 0. Positive control: all 12 mutants also compiled (tsc_rc=0), and the mutants that changed types were checked by tsc |
| eslint, the 4 touched files (ESLint API, cwd = Blockchain/Dev) | 0 errors / 0 warnings. Positive control: a snippet with `var` and an unused var gives `no-var` and `no-unused-vars` errors with the same config |
| `npm run check:openapi` (generate-openapi --check + spec-examples) | rc 0, "CHECK PASS", 413 example blocks OK |
| **Red first:** new + flipped cells against the parent's `index.ts` + `qualified-tsa.ts` | **8 red / 11 green** across the ks753 file and the ks740 file: 6 ks753 cells plus the 2 flipped ks740 cells. The 4 real-token/row controls stay green on the parent. The author says 5 + 2 = 7; I count 8 because the "CONTROL - NULL row" cell is also red on the parent (see N4) |
| **Real Postgres 15** (throwaway, scratchpad, port 55417, stopped afterwards) | Head: create gives `verified:false` with no verifiedAt; the row is `verified=f, verified_at NULL`; `/verify` returns false with a reason; GET returns false; both batch rows are false; an OTS row stays true; a legacy NULL row verifies false. **Parent: the same test is red** (verified true everywhere). Evidence: `realpg-output.txt` |
| shared / gateway / originate suites | Not run. The diff touches only `services/timestamping`, and the gateway is a pure proxy for `/api/timestamps` (`proxy.ts:927`) |

**Mutations** (`mutations.txt`, runner `mutate.py.txt`). Each mutant had an exact single anchor and passed tsc, then ran through the full 96-test suite, and the file was restored after each one.

| Mutant | Red | Author's claim |
|---|---|---|
| A1 fallback does not set `mock:true` | 3 | 4 (the form of the mutant differs; still killed) |
| A2 verified derived from `!eidasQualified` | 2, incl. the **non-eIDAS control** | 3 (killed; the control fires) |
| A3 verified_at always stamped | 4 | 4 |
| A4 no-token clause dropped | 1 | 1 |
| A5 verify guard disabled | 2 | 2 |
| G1 createTimestamp reads a misspelled field (`as any).isMock`) | 4 | (mine) |
| G2 flag dropped across the module boundary (field-pick copy) | 4 | (mine) |
| G3 JSON round trip of the TSA reply | 0, **expected green**: the flag survives serialisation | (mine) |
| G4 verify guard `=== false` (lets NULL through) | 0. **Equivalent mutant:** `rowToTimestamp` already maps NULL to false (`verified: row.verified ?? false`), and G5 kills that line | (mine) |
| G5 `rowToTimestamp` reads NULL as true | 1 (the NULL cell) | (mine) |
| G6 INSERT stamps verified_at for a mock (`|| createdAt`) | 4 | (mine) |
| G7 response `verified` hard-coded true, INSERT honest | 5 | (mine) |

**Gate probes** (`gate1502-probes.test.ts.txt`, output in `probes-output.txt`; 10 cells, all ran):
- P1: a **mixed batch** (real, mock, no-token, real) gives per-item `[true, false, false, true]`. The INSERTs match, and verified_at is only on the real tokens. The batch path shares `createTimestamp`, and **there is no third caller** (`index.ts:226` single, `:310` batch).
- P5: a row with verified=NULL **and** a hash that matches the proof JSON is not verified. Nothing falls through to a JSON-hash match.
- P6: GET `/api/timestamps/:id` returns the stored column: false gives false, true gives true, NULL gives false.
- P2b: with the real module and `requireEidas:true`, the service still fails closed with 503.
- P2, P3, P4, P5b, P7, P8 are observations, listed under Findings.

## Findings

**Major:** none.

**Minor**
- **m1. `eidasQualified` / `requireEidas` are not gated on the mock flag (defence in depth).** `index.ts:469` reads `eidasQualified = tsaResult.token ? tsaResult.eidasQualified === true : false` and ignores `mock`. Evidence, P2: a TSA reply `{mock:true, eidasQualified:true}` gives `[201, verified false, eidasQualified **true**]`, and with `requireEidas:true` it gives **201 rather than 503**. The PR's own "FLAG decides" cell uses exactly this input and asserts only `verified`. **Not reachable today:** the real fallback hard-codes `eidasQualified:false` (`qualified-tsa.ts:333`). Suggested one-liner for a follow-up: `eidasQualified = tsaResult.token && tsaResult.mock !== true ? tsaResult.eidasQualified === true : false`.
- **m2. Mock-only types still verify (carried forward, stated in the PR, pre-existing).** P7: `opentimestamps`/`blockchain` creation answers `verified:true` and persists true. P8: a **forged** opentimestamps JSON proof (hash plus one attestation) with **no stored row** returns `verified:true` from `/verify` (`index.ts:616-621`). KS-1404 closed this forgery path for rfc3161 only. This is "a mock timestamp reported as verified" by the ticket's own wording, so it needs its own ticket. It does not block this PR: it is declared out of scope and is not a regression.

**Note**
- **N1 (attack point a).** A row with `verified=false` that holds a **real DER** token returns false with the reason "locally generated mock token", and the crypto verifier is never consulted (P3). This cannot be produced by creation. The only writer, `index.ts:530`, always set the column, to true before this PR, so the column's DEFAULT FALSE never applied. A mis-targeted backfill is the only way to produce such a row. Any backfill must therefore target JSON-shaped proofs only (see Legacy rows), or genuine tokens will be refused with a false reason. An option for later is to fall through to `tsaVerifyTimestamp` when the stored proof is DER.
- **N2.** P5b: if the driver returned the **string** `'false'`, the `!ts.verified` guard would pass and verify true. Not reachable: the column is `BOOLEAN`, `pg` parses OID 16 to a JS boolean, and `db.ts` installs no `setTypeParser`. The real-Postgres run confirmed a boolean false and a NULL (`typeof` object).
- **N3.** My kill counts for A1 (3) and A2 (2) differ from the author's (4, 3). The cause is the form of the mutant. In my A1 the new creation cells stub the module and supply `mock:true` themselves, so only the cells that use the real module turn red. Every mutant is still killed.
- **N4.** "CONTROL - a row with verified NULL" is **red on the parent**, so it is a red-first cell, not a control. This is a labelling issue only.
- **N5.** The OpenAPI `Timestamp` schema (`timestamping.openapi.ts:120-145`) does not declare `verified` at all; it reaches responses through `.passthrough()`. The semantics this PR establishes ("a TSA signed it") are not published. The verify response does declare `verified` and `reason`.
- **N6 (pre-existing).** At creation, "verified" means "the configured `TSA_URL` returned a structurally valid TimeStampResp with status ≤ 1" (`rfc3161-client.ts:201ff`). It does not mean the signature or imprint was checked. `/verify` then trusts a `verified=true` row and skips `verifyRfc3161Token`. The comment the PR adds ("`verified` means a TSA actually signed this token") is therefore stronger than what the code checks for real tokens. This is outside KS-753 and worth a follow-up.
- **N7 (author attack c).** Only one place in the repo constructs a `TimestampResponse`: `qualified-tsa.ts createTimestamp`, with two return sites (the real token at `:293` without `mock`, and the fallback at `:317` with `mock:true`). `index.ts generateMockRFC3161Token` (`:649`) builds a proof string, not a `TimestampResponse`, and has **no `mock` field**. It is covered by the `!tsaResult.token` clause (cell + mutant A4), and it matters for the legacy count below.

## Consumers of verified/mock

| File | How it reads | Correct |
|---|---|---|
| `services/timestamping/src/tsa/qualified-tsa.ts:317-335` (fallback) | Produces `mock:true`, `eidasQualified:false`, "(mock)" name | yes |
| `services/timestamping/src/tsa/qualified-tsa.ts:293-301` (real) | Produces a token with no `mock` | yes |
| `services/timestamping/src/index.ts:470` createTimestamp | `mock === true` or no token gives verified false | yes |
| `services/timestamping/src/index.ts:469` eidasQualified | Ignores `mock` | yes today. m1 is defence in depth |
| `services/timestamping/src/index.ts:520-521, 543-544` response + INSERT | `verified`, `verifiedAt` only when verified | yes (real PG) |
| `services/timestamping/src/index.ts:226 / :310` single + batch | Both go through `createTimestamp`; no third caller | yes (P1) |
| `services/timestamping/src/index.ts:740-753` rowToTimestamp | `row.verified ?? false` | yes |
| `services/timestamping/src/index.ts:574-593` POST /verify, DB-row branch | `!ts.verified` gives false + reason | yes. N1 covers the reason text |
| `services/timestamping/src/index.ts:600-608` POST /verify, rfc3161 no-row branch | DER only (KS-1404); a mock is refused | yes |
| `services/timestamping/src/index.ts:611-633` POST /verify, OTS/blockchain | JSON decode; a forged mock verifies true | **no, pre-existing and out of scope (m2)** |
| `services/timestamping/src/index.ts:342/357/384` GET by id / document / hash, via `formatTimestampResponse:799-819` | Returns the stored column | yes for new rows. Legacy rows still return true (stated) |
| `services/api-gateway/src/routes/proxy.ts:927-930` | Pure pass-through proxy | yes (does not interpret) |
| `services/api-gateway/src/routes/system-status.ts:113` | Health URL only | n/a |
| originate, anchoring, mcp-server, sdk, `MCP Deployment`, frontend/*, mobile | **0 hits** for `/timestamps` or `timestamping`. Positive control in the same loop: 215 / 86 / 21 / 19 / 13 / 160 / 21 `verified` hits | n/a: no consumer |
| `shared/types/svs-types.ts:324` QualifiedTimestamp | Type only, no `verified` | n/a |
| demo-service seed generators | Import a local `utils/timestamps` date helper; do not write `ts_timestamps` | n/a |
| systemTest schemathesis `tsa_predicates.py`, `test_tsa_mock_fallback.py` | Check the eidasQualified signal; no assertion on `verified` for a mock | n/a |

The only writer to `ts_timestamps` in the repo is `index.ts:530`. There are 0 other `INSERT`/`UPDATE ts_timestamps` statements outside tests.

## Legacy rows

Every rfc3161 row written before this PR holds `verified=true` and a `verified_at` date, whatever its token was. After the merge those rows still answer `verified:true` on `/verify` (P4, and on real Postgres) and on all three GET routes. That is data, not code, and the PR says so.

**Read-only count per environment** (file `legacy_count.sql.txt`; I proved it on the throwaway database only):

```sql
BEGIN TRANSACTION READ ONLY;
WITH c AS (
  SELECT timestamp_type, verified,
         (left(proof,3) = 'eyJ')        AS json_shaped,   -- base64 of '{"' = locally generated token
         (tsa_name LIKE '% (mock)')     AS mock_named,    -- post-migration-042 rows only
         (left(proof,2) = 'MI')         AS der_shaped     -- real RFC 3161 DER
  FROM ts_timestamps)
SELECT timestamp_type, count(*) AS total_rows,
  count(*) FILTER (WHERE verified IS TRUE  AND json_shaped) AS verified_true_json_mock,
  count(*) FILTER (WHERE verified IS TRUE  AND mock_named)  AS verified_true_mock_named,
  count(*) FILTER (WHERE verified IS TRUE  AND der_shaped)  AS verified_true_der,
  count(*) FILTER (WHERE verified IS FALSE AND der_shaped)  AS verified_false_der,
  count(*) FILTER (WHERE verified IS NULL)                  AS verified_null,
  count(*) FILTER (WHERE NOT json_shaped AND NOT der_shaped) AS unclassified_shape
FROM c GROUP BY timestamp_type ORDER BY timestamp_type;
ROLLBACK;
```

**Use the proof shape as the discriminator, not `tsa_name` and not the JSON `mock` field.** The `index.ts` generator writes no `mock` field, and rows written before migration 042 have no `tsa_name`. On the throwaway database the `(mock)` name found only 4 of the 5 legacy mocks (`realpg-output.txt`).

**What a backfill would involve (approval-class, not done):**
1. Run the read-only count above per environment (dev, staging, demo/Kintsugi, production), each against its own database and tenant.
2. If the count is above zero, Kam rules. The candidate statement is `UPDATE ts_timestamps SET verified = false, verified_at = NULL WHERE timestamp_type = 'rfc3161' AND verified IS TRUE AND left(proof,3) = 'eyJ'`, run in a transaction that first asserts the affected row count equals the count from step 1, with a before-image copy (`CREATE TABLE ts_timestamps_ks753_backup AS SELECT id, verified, verified_at FROM ... WHERE <same predicate>`) for rollback.
3. Leave DER-shaped rows alone (N1).
4. Decide the policy for opentimestamps/blockchain rows separately (m2); they are mock by design.
5. Warn relying parties: any proof a customer was told is "verified" will flip to false on `/verify`, so this needs comms.

## NOT tested

- No live TSA. Every "real token" path uses either a stub of `qualified-tsa.createTimestamp` or a 503 fetch. A genuine TimeStampResp through `rfc3161Request` to `index.ts` was not exercised end to end, and so neither was the "real token gives verified true" claim against a real TSA (N6).
- No run against any shared, demo, staging or production database. The legacy count SQL ran only on the throwaway Postgres.
- I did not run the shared, gateway or originate suites; the diff is confined to timestamping (see By my runs). Docker was down, so there was no service-to-service run through the gateway.
- I took `node_modules` from the project tree as a read-only symlink farm, built `packages/shared/dist` in the clone, and npm-installed `asn1js@3.0.10` and `pkijs@3.4.1` into the scratchpad. **The project tree's own `node_modules` lacks `asn1js`/`pkijs`**, so the suite cannot run there as-is. That is environment, not the PR.
- I did not read the PR body on GitHub (no GitHub reads). I took the claims from the brief.
