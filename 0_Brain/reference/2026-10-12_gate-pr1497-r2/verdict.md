# QA delta gate: Secuura Platform K PR #1497 (KS-695 ask 3 part ii), reworked head 6454dc9c

- **Head:** `6454dc9cb6a751b243d20e4c7a7c946791dd80a2`. It came from the full bundle `ks695b_pr1497_6454dc9c_full.bundle` (sha256/16 `14f40ac1c2e60371` confirmed; `git bundle verify` ok; it needs `1158045e52b8`). `d2a88a2c2b1e` is an ancestor (`merge-base --is-ancestor` rc 0). The control, develop as an ancestor, gave rc 1. There are four commits on `1158045e`: `c171b25f1`, `d2a88a2c2`, `4a79136ed` and `6454dc9cb`. The delta since the gated head is 7 files, +407/-18.
- **Base used:** the real `origin/develop` = `361537eed238e9886f4cc22d8a91607a96fb1508`, fetched just now. Develop is 2 commits past the PR's base, and neither commit touches any of the PR's 10 files. I gated the merge tree `b7f8af70` (a clean local merge in my scratch clone). Its originate source is identical to the PR head's.
- **Gate:** independent Opus, Tier 1 (destructive, GDPR path), full delta, Wednesday seat, 2026-10-12. I am neither the author nor the earlier gate.

## VERDICT: NO GO

**The m3 rework over-corrects. The new lineage guard drops every descendant whose `versionedById` is not NULL and not this connector, including a derivative made by the organisation's own human user. So A's erasure answers `completed` and leaves an A document's title (personal data) in place, although the spec now claims it blanks every lineage descendant except "one issued by another organisation or versioned by another connector".** I reproduced it through the real `/version` and erase routes in both tenancy modes (Finding M-A). A one-clause fix exists and I tested it: green on every file, both the author's and mine. Every earlier finding (M1, m1, m2, m3 as ruled) is otherwise fixed, and every should-catch mutation is killed.

## Earlier findings

| Finding | Status | Evidence line |
|---|---|---|
| **M1** (Major): seed arm (b) trusts `versionedById` | **FIXED** | Both copies (count at service lines 235-237, blanking at lines 260-262) read `issuer = org OR (vb = conn AND (issuer IS NULL OR issuer = org))`, and the parentheses bind correctly. The earlier gate's e2e (real create route, then B's erase) is green in MT=false, MT=true and as superuser. `GATE AX after B erase {"title":"A owned, versionedById planted as B.pdf",...}`. My R1: an A-issued child of a B document that carries B's `versionedById`, and that child's own unissued child, are both untouched. A row in two arms is counted once (`documentsBlanked:3` for BB, BBC and P1). |
| **m1** (Minor): `completed` with the key active | **FIXED** | `lower(btrim(organization_id))` plus a read-back of the named key inside the transaction. Bounds cell: an upper-case key with a trailing space gives 200 and the key is revoked. The trigger-skip cell gives 500 with name, title and key unchanged, and the retry completes. Earlier ATTACK 6: `GATE F erase 200 ... keyActive=false`. Whitespace that `btrim` does not strip (TAB, NBSP) now gives a 500 and never `completed` (Note N-B). |
| **m2** (Minor): 5 s Prisma timeout before the 150,000 guard | **FIXED in MODE F** | 140,000 flat documents: `ms:6212 completed documentsBlanked:140000` (it failed at 7,029 ms on d2a88a2c). 149,000 documents with 2 KB metadata: 6,972 ms in MODE F and 7,042 ms in MODE T. The pool branch, which `services.bicep` deploys (`MULTI_TENANCY_ENABLED=true`), has no budget at all (Note N-C). |
| **m3** (Minor, ruled conservative) | **Fixed for connectors, but over-broad** | WA (`vb = connector:A` under B's derivative) survives B's erasure (bounds cell and earlier ATTACK 2). But the guard also drops non-connector `versionedById` values. That is M-A. |

## By my runs

All runs used the merge tree `b7f8af70` after `npm ci --ignore-scripts`, a build of `packages/shared` and `npm run generate`. The database was my own throwaway PG 15 on port 55418, data dir in my scratchpad: init SQL applied with 0 failed, 49 migrations with 0 failed, platform tenancy applied, `secuura_app` with `rolsuper=f` and `rolbypassrls=f`. FORCE RLS was confirmed on `documents`, `organizations`, `svc_api_keys` and `action_provenance`. The DB is stopped (`listen rc=1`). Evidence is in `evidence_runs.txt`, `evidence_mutations.txt` and `evidence_suites.txt`.

1. **The author's files, as `secuura_app`:** `ks695-ask3-erase-connector.integration` 15/15 and `...-selector-bounds.integration` 7/7, with MT=false and again with MT=true. With no app URL (the title says superuser), bounds is 7/7.
2. **Superuser stand-in:** 1 failed per file in both modes, and it is the role probe each time (`connection is "postgres" (superuser=true, bypassrls=true) ... Refusing to pass`).
3. **The earlier gate's files, unchanged** (byte-identical to the author's copies, `diff` rc 0): attack 12/12 and e2e 1/1 in both modes, and e2e 1/1 as superuser. These were RED on d2a88a2c.
4. **Unit and static checks:** originate `npx jest` ran twice: 101 suites / 1185 tests, rc 0. `packages/shared` ran twice: 49 files / 954 tests. api-gateway ran twice: 112 files / 1076 tests (on develop `361537ee`). `tsc --noEmit` rc 0 in all three. eslint on the 9 changed TS files: rc 0, empty output. `check:openapi`: rc 0, `CHECK PASS`, 414 example blocks.
5. **The author's six mutations, re-run** (each landed with a changed sha and was restored byte-identical; `git diff` empty afterwards):
   - MA (guard dropped from the blanking): unit 1, bounds 2 and gate ATTACK 1 red.
   - MA2 (guard dropped from the count only): only the unit pin is red, as the author says.
   - MB (lineage guard dropped from the blanking): unit 1, bounds 2 and ATTACK 2 red.
   - MC1 (`btrim` reverted): unit 1 and bounds 1 red.
   - MC3 (read-back disabled): my first form did not compile (TS6133). That is a load failure, not a kill. In the compiling form `after.length < 0 && ...`: unit 1 and bounds 1 (trigger-skip) red.
   - MD (transaction options dropped): unit 1, bounds m2 (MODE F) and ATTACK 3+4 red. MODE T stays green, as it should.
6. **Nine mutations of my own, all killed:**
   - X1, guard `AND`→`OR`: old file 3, bounds 3, attack 3 red.
   - X2, guard `IS NULL` dropped: old file 2, bounds 1 red.
   - **X3, the read-back reads the wrong key** (any inactive key in the tenant): the unit file stays GREEN. Only the bounds trigger-skip cell kills it.
   - X4, `lower` dropped but `btrim` kept: unit, bounds and ATTACK 5 red.
   - **X5, `db.ts` stops forwarding `opts`** (compiling form): the unit file stays GREEN, because it mocks `withTenant`. Bounds m2 and ATTACK 3+4 kill it.
   - X6, lineage guard inverted: unit, bounds 2 and ATTACK 2 red.
   - X7, `timeout` dropped but `maxWait` kept: unit, bounds m2 and ATTACK 3+4 red.
   - X8, guard mis-parenthesised so arm (b) binds alone (`a OR b AND c OR d OR b`): unit, bounds 2 and ATTACK 1 red.
   - No should-catch mutant survived.
7. **My attack file `gate1497r2-attack`, both modes, 6 passed / 1 slow cell run separately:**
   - **R1**: the two-arm rows and the A-issued child of a B document are bounded correctly.
   - **R2**: a key whose `organization_id` is stored with a trailing TAB, or with NBSP, gives `500` and `500` on retry, with `keyActive=true` and the name unchanged (N-B).
   - **R3**: a built-in CHECK violation inside the erasure gives 500, logged as `{"organizationId":..,"tenantId":..,"error":"... violates check constraint \"g97r2_chk\""}`. The org name and the title are absent from every log call (positive control: `logger.error` was called). Prisma's message (MODE F) and pg's message (MODE T) carry no row values.
   - **R4**: the retry completes.
   - **R5**: a statement trigger sleeping 27 s. MODE F answers **500 at 27,180 ms**, rolled back. MODE T answers **200 completed at 27,035 ms**, committed (N-C).
8. **The human-user e2e `gate1497r2-human`** (real `documentsRouter` `/version`, then the real erase route), both modes, **RED**: `after {"src":"[erased]","human":"A contract with Jane Citizen.pdf (watermarked)","connector":"[erased]"}` with `200 completed documentsBlanked:2`. Under mutant MB (the d2a88a2c lineage arm) and under FIX2 (below), the human derivative is blanked (`documentsBlanked:3`).
9. **The NULL-issuer e2e `gate1497r2-e2e`:** an unissued document that A's connector creates with `data.versionedById = B`, and A's `/version` of A's own document with `metadata.versionedById = B`, are both blanked by B's erasure (`documentsBlanked:2`). A's ordinary derivative is untouched. `action_provenance` has no row for any of them (N-A).
10. **Scale (`gate1497r2-scale`, `secuura_app`):**
    - 140k flat, MODE F: 6.2 s.
    - 149k with 2 KB metadata: 7.0 s in MODE F and 7.0 s in MODE T.
    - 20,001-deep lineage: 0.96 s.
    - A 10-document org in a tenant holding 2M **issued** bystander documents: 24 ms (index plan).
    - The same org in a tenant holding 2M **NULL-issuer** documents: 2.36 s. The bystanders were untouched each time.

## Findings

### M-A (MAJOR): the reworked lineage guard leaves the organisation's own descendants unblanked and still answers `completed`

Lines 244 and 269: `AND (c.metadata->>'versionedById' IS NULL OR c.metadata->>'versionedById' = ${connectorUser})`. `/version`, `/sign-cert` and `/sign-wallet` write `versionedById: user.id`. For a human user (`DOCUMENT_WRITE_ROLES`: ISSUER_ADMIN, ORG_ADMIN, and so on) that value is a bare user id, not `connector:...`. Such a derivative is therefore no longer followed. Evidence (runs item 8, both modes): A's ISSUER_ADMIN versions A's issued document; A's erasure answers `200 completed documentsBlanked:2`; the derivative keeps `A contract with Jane Citizen.pdf (watermarked)`. On d2a88a2c it was blanked (mutant MB, `documentsBlanked:3`).

This is a regression introduced by the rework, and it contradicts:
- the published description: "their lineage descendants; never one issued by another organisation or versioned by another connector". A user is not a connector.
- Wednesday's ruling as the code comment words it: "the selector does not follow what it would itself attribute to someone else". The selector attributes only `connector:<id>` values.

By the brief's rule this is leaving data the PR claims to blank. The same guard lets any writer hide a descendant from its own organisation's erasure with any non-connector value (for example `metadata.versionedById: "x"` on `/version`).

**Fix (tested as FIX2, green on unit 26/26, old 15/15, bounds 7/7, gate attack 12/12 and human 1/1):** in both copies, `AND (c.metadata->>'versionedById' IS NULL OR c.metadata->>'versionedById' = ${connectorUser} OR c.metadata->>'versionedById' NOT LIKE 'connector:%')`. Add the human-derivative cell as a red-first pin. If Wednesday or Kam instead want human derivatives excluded, the spec and the LIMITATION must say so. Today they say the opposite.

### Minor

- **N-A → m-1 (Minor): the forgeable `versionedById` still selects UNISSUED documents.** M1 is closed for issued documents. A NULL-issuer document can still be claimed for B by any writer:
  - by a create without `organizationUuid`;
  - or by **any** `/version` (derivatives are always NULL-issuer, and `metadata` is spread after `versionedById`). `/version` also has no organisation check on the source, so any `documents:write` caller in the tenant can version any document.

  Evidence (runs item 9): A's `/version` of A's own payroll document, with `metadata.versionedById = B`, is blanked by **B's** erasure, and it would not be reached by **A's**, because the m3 guard excludes it. K has no provenance row to tell the truth. The same lever can inflate B's reach to force a permanent `ORGANISATION_TOO_LARGE`. This is the residue of KS-1508 (server-set `versionedById`), not of this diff. It leaves an issued document alone, and planting needs a writer in the tenant. **Recommend KS-1508 lands before KS-695 deploys.**
- **N-C → m-2 (Minor): the transaction budget exists only in the branch that is not deployed, and its comment overstates it.**
  - `services.bicep` sets `MULTI_TENANCY_ENABLED=true`, so production takes the pg-pool branch, which has no transaction or statement timeout. R5: committed at 27 s. A transaction past 30 s would commit after the proxy has already answered S with a 5xx. S then retries with a revoked key, which is open question Q1.
  - In MODE F, Prisma's timeout does not interrupt a running statement: the 500 arrived at 27.2 s, not 25 s. So the comment's "fails first, in the process" is not literally true. What is true is that anything past 25 s is rolled back.
  - The margin under the guard is honest on a laptop (149k ≈ 7 s in both modes, about 4× headroom). But the cost also grows with the tenant's NULL-issuer population: arm (b) scans it twice, 2M rows ≈ 2.4 s. The guard does not count that.
  - Fix or state it: `SET LOCAL statement_timeout` in the erasure (both branches), or a sentence in the comment and the PR.

### Notes

- **N-B.** The read-back turns TAB or NBSP whitespace, which JS `trim()` strips and `btrim()` does not, into a permanent 500 (R2: 500 then 500, key active). That is safe (never `completed`), but S retries without bound. Only an admin-minted key can carry such an id. Using `regexp_replace` or the shared normaliser on both sides would close it. The same applies to a NULL `is_active` row: `null !== false` throws.
- **N-D.** Test-strength gaps (not blocking): X3 (the read-back reads the wrong row) and X5 (`db.ts` stops forwarding `opts`) survive the unit file. Each is killed only by one real-Postgres cell, and the integration suites are not run by any CI gate (KS-1474). MA2 (guard dropped from the count) is killed only by a text pin.
- **N-E.** Logging is clean. Ids, counts and the DB error message only; the name and titles never appeared (R3, both modes). The 503 is logged at warn with the counts. Prisma's message embeds the invocation text but not row values.
- **N-F.** `withTenant`'s third parameter is additive and optional. All 16 other originate callers pass two arguments, and `$transaction(fn, undefined)` behaves as before. The suites are unchanged (1185/1185).
- **N-G.** The earlier gate's N2 to N6 stand as written (`withTenant` returns success when a callback swallows an error; the 60 s gateway key cache; `[erased]` as a real organisation name; `register-connector` restoring the name; the scope still in grace). None of them is a Major for this PR.

## Answers to the author's five attack points

1. **Selector bounds.**
   - Parentheses: correct in both copies, `A OR (B AND (C OR D))`. X8 (mis-bound) is killed.
   - A row in two arms: counted once (R1, BB and BBC).
   - NULL issuer: reached by design, and forgeable (m-1).
   - Another tenant reusing the connector id and GUID: untouched (author's cell, re-run green).
   - An A-attributed document with B's `versionedById`: untouched (AX, AX2, and the e2e).
   - B's own issued, versioned-unissued, derivative and unattributed-child documents: blanked, count 4 (bounds).
   - **But** the lineage guard drops the organisation's own human-versioned descendants (M-A).
2. **The read-back.** The named key is read by id and tenant after a row lock taken at step 1b.
   - A repeat: the key reads inactive, the call passes and answers `alreadyErased`.
   - A second key of the same organisation, or a connector with two keys: only the named key is read back, so the other stays active (by design, N1).
   - A concurrent re-activation: it blocks on the `FOR UPDATE` lock until commit, so it cannot fool the read-back. A re-activation after commit is outside the erasure.
   - I found no path where the named key is legitimately active at the read-back. The only false 500s are N-B.
3. **`withTenant` options.** Additive and safe (N-F). The 25 s budget is honest for MODE F. It does nothing in the deployed MODE T, and an organisation under 150,000 documents can still run long in a tenant with millions of NULL-issuer rows, or on slower production hardware (m-2).
4. **Logging.** No personal data in any log line I could provoke (N-E).
5. **Spec.** "The named key" and the selector bounds are stated, and `check:openapi` passes. The selector sentence is now **false** for human-versioned descendants (M-A). On the GDPR "not reached" list (`metadata.issuerName`, recipient email, `sIdentity`, `certification_metadata`, lifecycle, shares, versions, audit, chain): the PR does not claim to blank any of them, and it states them first, for Kam, in the PR body. So none is a Major under the rule. They are a **Minor-level disclosure gap** in the *published spec*, whose LIMITATION still names only unattributable documents. `metadata.issuerName` (the erased name, still served on verify) is the one I would put to Kam before deploy. The m3 policy also means A's derivative of B's document keeps B's title after B's erasure; that is Wednesday's ruling, and it should be listed among the "not reached" items.

## NOT tested

- Any live, Kintsugi, demo or production stack; the real gateway, security and auth chain (the 60 s validate cache); `register-connector` end to end.
- Production-scale timing (Azure Postgres, pgbouncer, WAL and TOAST on real metadata). My timings are from a laptop.
- `/sign-cert` and `/sign-wallet` derivatives. I read from code that they set `versionedById: user.id` the same way `/version` does, but did not run them.
- The human-user path in a Platform-S-only deployment: whether S organisations have K portal users at all. The spec's claim is general, so I rated it on the claim.
- Schemathesis, Akto, Playwright and k6; the pre-push preflight hook; the earlier gate's scale file at 140k in MODE T (my own probe covered 149k there).
- The author's statement that the bounds file was red first on the unfixed code (not re-run; it is consistent with every mutant above being killed).
