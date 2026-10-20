VERDICT: GO WITH NOTE at head d8e8e65b816a... (tier 1, round 2 of 2; landing tree fd2674434210e6590dd34975f8f756a06bf6fbc3 on develop 561a6c5b528289f4d7ecd19f9c069501e925e9ea; 0 blockers, 8 notes)

Gate CL1, PR #1666 round 2 (KS-758 F9 option (c), keyed hash of the external ref), Opus 5.5. I did not re-read the card. Kam's (c) ruling is as quoted in the brief and the claim.

## BLUF
The product does what the claim says. The reason becomes `...; ref_hmac=<64 hex>)` via the repo's real keyed `lookupHash`, which is HMAC-SHA256 over a separate 32-byte key and throws when the key is unregistered. The raw ref is hashed. The row and the new warn carry no raw ref, tenant id or PII, case-insensitively. I proved this with the REAL `lookupHash` and `registerLookupHmacKey`, not only with the author's stand-in. With the key never registered, the real helper throws, the erasure completes, the reason is the exact (b) string, and one warn carries only `connectorId` and the fixed error text. All three CE1 test gaps are closed and red by assertion. The suite by cell name is 1576 -> 1582 -> 1587, +5, 0 vanished, 0 failed.

There is no blocker. The main note is N1: the disclosure says a reader without the key learns "nothing about WHICH subject". That is not true for a reader who can anchor one hash to a ref they already know. Via KS-1696, that includes another tenant's admin. Wednesday should put this to Kam before merge. Three other notes are gaps the tests still leave (N3, N4, N5).

## Heads
- Start 03:38:48Z, ls-remote to GitHub (Blockchain deploy key, read-only remote `gh`, push URL disabled): develop `561a6c5b528289f4d7ecd19f9c069501e925e9ea`, `refs/pull/1666/head` `d8e8e65b816a6fe7a469d2955e33ce0c040d15f5` (equal to the claim and the brief).
- End 03:48:10Z: the same two shas.
- Head is a fast-forward over round 1: `merge-base --is-ancestor b5d65c8e0651 d8e8e65` rc 0. It adds one commit, `d8e8e65b8 Refs KS-758 F9 round 2`.
- Landing on LIVE develop: `git merge-tree --write-tree gh/develop gh/pr1666` gave rc 0, one line, `fd2674434210e6590dd34975f8f756a06bf6fbc3`.
- The claimed `7763738a7edb` reproduces exactly against the claim's develop `21e2ffd20795`.
- Develop moved by one commit since then (`561a6c5b5`, one vc-issuer test file, +6). So the landing differs only by that.
- `diff --name-only gh/develop <landing>` gives exactly the PR's 2 files. The landing's `services/originate` subtree is `1f5dd5600ecb` and `packages/shared` is `26b323dba1df`, identical to the head's. So the originate results at the head are the results at the landing.
- Merge-base is `3a6f1810981e`.

## Findings

### Q1 Delta and the helper
- `git diff b5d65c8e0651..d8e8e65` has 2 files, +160/-2. Three-dot against live develop has 2 files, +355/-0 (`gdprService.ts` +97, the test file +258). I read the whole product delta.
- The delta adds the `lookupHash` import (`gdprService.ts:20-30`) and a try/catch computing `refHmac` (`:1554-1566`). It then builds `unresolvedReason` (`:1567-1569`): with a hash, the (b) string plus `; ref_hmac=${refHmac}`; without one, the exact (b) string.
- The INSERT now binds `unresolvedReason` (`:1573-1575`). Nothing else changed in the product.
- The helper, read at `packages/shared/src/crypto/encryptedField.ts:576-603`:
  - Key: a module-level `lookupHmacKey`. `registerLookupHmacKey` requires exactly 32 bytes of hex (`:578-584`).
  - Hash: `lookupHash` throws `PII_LOOKUP_HMAC_KEY is not registered ...` when the key is unset (`:596-600`). Otherwise it returns `createHmac('sha256', key).update(value,'utf8').digest('hex')`.
  - The key is separate from the encryption KEK (`:573-574`). So this is a keyed HMAC, not a bare SHA-256.
- Normalisation: `gdprService.ts` has exactly 4 `external_ref = ${externalRef}` comparisons (`:1197`, `:1449`, `:1503`, `:1594`), all raw equality. No `toLowerCase` or `trim` is applied to the ref anywhere in the file. So the raw hashing matches how the lookups compare.
- The ref IS trimmed upstream, though, by zod at both ends:
  - erasure ingress: `routes/gdpr.ts:514`, `z.string().trim().min(1).max(128)`
  - provenance write validator: `services/provenance.ts:44`, the same schema
  That is consistent: the value hashed equals the value stored. But the author's "normalised NOWHERE" is false in letter (N2).

### Q2 No raw ref, tenant id or PII in the row or any NEW log line
- The ROW binds five values: `'action_provenance'`, `blanked` (an integer), `'anonymize'`, the reason, and `connector:<connectorId>`. The reason is a fixed literal plus 64 lowercase hex characters.
- My cell CL1-R2 (real helper, real registrar, key `cd`x32) asserts:
  - the reason equals the (b) string plus `; ref_hmac=` plus HMAC(key, raw ref), exactly;
  - it does not contain the bare SHA-256 of the ref;
  - `JSON.stringify` of all five bound values, lowercased, does not contain the ref or TENANT;
  - zero warns;
  - the hash appears in no log line;
  - on this branch, the ONLY log line carrying the ref is the pre-existing `Connector erasure blanked provenance identity for an unresolved subject` info.
  The cell PASSES.
- The NEW warn (`:1563-1565`) carries `connectorId` and `error`. `error` is lookupHash's fixed message, which holds no input value. CL1-R1 asserts the payload keys are exactly `['connectorId','error']`, and that the lowercased payload contains neither the ref, `person-guid` nor TENANT. It PASSES.
- `connectorId` is the connector principal's id (`routes/gdpr.ts:475`), not a subject. CE1 judged it the same way.
- CE1 N1 still holds, deliberately, and the body says so (round 2 "Known residue"). The `externalRef` stays in three log lines:
  - the never-seen / already-erased `logger.info` at `gdprService.ts:1494-1497`;
  - the INSERT-failure `logger.error` at `:1577-1580`;
  - the pre-existing blanking `logger.info` at `:1583-1585`.

### Q3 Key unregistered (proved on the REAL helper)
- CL1-R1 runs the INSERT path in a copy of the author's file whose `lookupHash` override is replaced by `jest.requireActual('@secuura/shared').lookupHash`. The key is never registered in that module registry.
- Precondition asserted in the cell: `actual.lookupHash('x')` throws `/PII_LOOKUP_HMAC_KEY is not registered/`.
- Then:
  - the erasure returns `{completed, alreadyErased:false}`;
  - exactly one INSERT is written, and its reason is exactly the (b) string;
  - exactly one warn is logged, clean as in Q2.
  PASS.
- Positive controls: with the try/catch removed, R1 and H2 go red. With the warn removed, R1 and H2 go red (red-proof table below).
- Wiring, read:
  - `docker-compose.yml:601` (originate) is `PII_LOOKUP_HMAC_KEY=${PII_LOOKUP_HMAC_KEY:-}`, empty by default.
  - `deployment/azure/services.bicep:395` is `{ name: 'PII_LOOKUP_HMAC_KEY', secretRef: 'pii-lookup-hmac-key' }`. The secret value comes from `param piiLookupHmacKey string` (`:135`, `:305-306`), and nothing checks that it is non-empty.
  - `initFromEnv` registers only `if (hmacKey)` (`encryptedField.ts:635-636`).
  - originate calls `initFromEnv` only when `PII_ENCRYPTION_KEY` is set (`index.ts:370-384`). Nothing refuses to start without the HMAC key.
- JUDGEMENT: the degradation is visible in TWO places, not only through the warn.
  - The warn: its `message` survives the production file allow-list (`utils/logger.ts:69`, `FILE_LOG_FIELDS` = timestamp, level, service, message, requestId, method, path, statusCode). Its `connectorId` and `error` fields reach only the Console stream.
  - The row itself: a reader of `data_deletion_log` sees a reason without `ref_hmac=`.
  - There is NO boot-time signal. The warn fires only when an unresolvable connector erasure actually runs. A deployment without the key looks healthy until then, and every such row is silently (b).
  - The author's body says "(c) silently degrades to (b)". That is accurate about the system and slightly understates the row as a second signal.

### Q4 What a reader can and cannot learn (judgement; no remedy proposed)
The author's disclosure is accurate as far as it goes: with the key, prove a named subject was erased; without it, equal hashes mean the same subject. It is INCOMPLETE on three points (N1):
1. **Anchoring defeats "nothing about WHICH subject".** A keyless reader who knows ONE ref and can find that ref's row learns that every other row with the same hash is that subject. Today that reader includes any ORG_ADMIN, via KS-1696. They can find their row because `performed_by` names their own connector and `createdAt` is returned (`mapDeletionLogRow`, `gdprService.ts:513-524`). The hash is not tenant-scoped: the HMAC input is the ref alone. So a matching row under ANOTHER connector tells that admin that another organisation's connector erased the same subject, and when. That is a cross-tenant membership disclosure without the key. It holds whenever the same PersonGuid can reach K through two connectors. Whether Platform S issues one PersonGuid per person across organisations is NOT established by me.
2. **Same key, no domain separation.** `ref_hmac` uses the same `PII_LOOKUP_HMAC_KEY` and the same unprefixed construction as the email lookup hashes, e.g. `users.email_lookup_hash` in auth's `userRepo.ts` and `action_provenance.email_hash` in `provenance.ts:110,203,305`. A ref that ever equalled a normalised email string would produce the same value as that email's lookup hash. With a GUID ref this cannot happen. The schema accepts any 1-128 character string.
3. "A Platform-S PersonGuid is exactly that kind of small search space" (body and in-code comment) is wrong about a GUID. The key's real value here is against confirming a guessed candidate, not against enumeration. The conclusion (keyed, not bare) is right. The stated reason is not.

### Q5 CE1's gaps and the red-proof
Harness: `scratchpad/gate_cl1/harness/mutants.py`.
- For each arm it makes an anchored edit, asserting exactly 1 occurrence.
- It runs the product `tsc --noEmit -p originate/tsconfig.json`, and requires rc 0 before the arm counts.
- It runs jest on the author's file (51 cells) and my copy, counting only my 2 GATECL1 cells, 53 in all.
- It classifies each red as ASSERT (an `expect(` failure) or OTHER (a thrown error).
- It restores with `git checkout` and asserts sha256 equality. The product sha256 was `50ae93fd9045...2eab2` before and after every arm, and restored-equal was true on all 11.

| arm | tsc | red cells (kind) |
|---|---|---|
| A0 none | 0 | none, 53/53 |
| CE1 G-a: `records_affected` hard-coded `${1}` | 0 | **G-a** (ASSERT), now red (CE1 M3 survived) |
| CE1 H3: `${externalRef.toUpperCase()}` inside the reason | 0 | **H3** (ASSERT, at the lowercased `not.toContain`), H1 (ASSERT, prefix), CL1-R2 (ASSERT); now red (CE1 M4 survived) |
| CE1 G-c: the two `cause` labels swapped | 0 | **G-c** (ASSERT), now red (CE1 M5 survived) |
| author: option (a), `refHmac = externalRef` | 0 | F2 H1 H2 H3 FC1 CL1-R1 CL1-R2 (all ASSERT) |
| author: try/catch removed | 0 | H2, CL1-R1, both by a THROWN `PII_LOOKUP_HMAC_KEY is not registered` rejection, NOT an expect (N5) |
| author: warn removed | 0 | H2, CL1-R1 (ASSERT) |
| mine M1: bare SHA-256 instead of the keyed HMAC | 0 | H1 H2 CL1-R1 CL1-R2 (ASSERT) |
| mine M2: the warn also carries `tenantId` | 0 | CL1-R1 only (ASSERT); **H2 survives** (N4) |
| probe P1: `lookupHash(externalRef.toLowerCase().trim())` | 0 | **NONE, survives all 53** (N3) |
| probe P2: the warn carries `externalRef.toUpperCase()` | 0 | CL1-R1 only; **H2 survives** (N4) |

- The author's option (a) arm reproduces as a superset of the claim. My shape bypasses `lookupHash`, so H2 also reds. I did not run the author's "hash removed" arm, since 3 of the 4 were asked.
- No arm reddened any cell outside the KS-758 block or my two, so there was no collateral on the other 40 cells of the file.

### Q6 Counts by cell name, type-check, merge-tree
- I ran the whole originate jest with `--json` at three points, `npm test --prefix <clone>/services/originate`, with jest cwd inside the clone:
  - live develop `561a6c5`: 135 suites, 1576 passed
  - round 1 `b5d65c8`: 135 suites, 1582 passed
  - head `d8e8e65`: 135 suites, 1587 passed, 0 failed, rc 0
- Set difference by (file, fullName):
  - develop -> round 1: 0 vanished, +6 (F1-F5, FC1).
  - round 1 -> head: 0 vanished, +5 (H1 H2 H3 G-a G-c), 0 duplicate names.
  - Comparator positive control: dropping one name from the head set is detected as 1 vanished.
- The brief's base sha `7e3b9362e08b` exists. I measured on live develop instead, which has the same 1576.
- Own-program type-check of the test file (originate is outside leg 16, KS-1090):
  - Scratch tsconfig in `harness/` extends originate's (strict, noUnusedLocals), with `files: [the test file]`, `types: [jest, node]` and an absolute `typeRoots`. Result: rc 0, 0 errors.
  - `--listFilesOnly` shows the test file, `gdprService.ts` and `@types/jest/index.d.ts` (3 of 3).
  - Positive control: appending `export const __gatePc: number = "not-a-number";` gave rc 2 with TS2322 at (995,14). Restored by `git checkout`, sha256 `498a4c9f...9dfc` equal before and after.
- Product `tsc --noEmit` at the head is rc 0.
- merge-tree: see Heads.
- `@electric-sql/pglite` was not needed: nothing in this PR touches m365.

### Q7 The PR body
- `gh` is unauthenticated in this seat. The project's `.gh-config` gave "gh auth login", and the REST API gave 404 for the private repo. So I could NOT read the LIVE body.
- I read the author's own read-back file instead: `/private/tmp/claude-501/-Volumes-DevMASTER--CODING-Secuura-Blockchain/d77e5e6f-.../scratchpad/pr1666_rb3.md`, 14:35:22 AEDT, read only.
  - It is 19,101 characters (`wc -m`), equal to the claim's "19,101 bytes", which is really a character count: it is 19,239 bytes.
  - It is the author's sent `pr1666_final.md` byte for byte, plus a trailing newline.
- Treat what follows as the body AS SENT AND READ BACK BY THE AUTHOR, not as independently read live. Against the code:
  - No sentence describes a guard that does not exist. The fail-soft, the warn, the fallback, the key wiring, "nothing refuses to start", the four raw comparisons, CE1 N1 left on purpose, and the KS-1696 read all match the code.
  - Inaccurate sentences, none of them a phantom guard (N2):
    - "external_ref is normalised **nowhere**": zod `.trim()` runs at both ends (Q1).
    - "A Platform-S PersonGuid is exactly that kind of small search space" (Q4.3).
    - "`performed_by` (the connector organisation id)": it is the connector principal's `user.userId` (`routes/gdpr.ts:475`).
    - "Without the key: nothing about which subject" (N1).
    - Round 1's "Known residue" still says "The card can still move. If (a) or (c) is ruled...". This is stale. The banner at the top covers only "bare category" passages.
  - The in-code comment at `gdprService.ts:1516-1525` still says "`reason` carries a bare CATEGORY and no subject reference (... option (b))". It is now contradicted eleven lines further down by the (c) block.

## Notes (none blocks)
- **N1 (the main item for Wednesday/Kam: disclosure incomplete).** The disclosure omits:
  - anchoring: a keyless reader who knows one ref identifies all of its rows;
  - that the hash is tenant-unscoped, so the correlator links the same subject ACROSS tenants and connectors. Through KS-1696, an ORG_ADMIN can learn that another organisation's connector erased a subject the admin can name;
  - that the key and construction are shared with the email lookup hashes, with no domain separation.
  Whether one PersonGuid can reach K under two connectors is unestablished. No remedy proposed.
- **N2 (wording).** The five body sentences and the stale in-code comment listed under Q7. Cell F2's name ("the reason is a bare CATEGORY") is also now false on the happy path, though its assertions still hold.
- **N3 (raw hashing unpinned).** Probe P1 (`toLowerCase().trim()` before hashing) survives all 53 cells, because `EXTERNAL_REF = 'person-guid-from-platform-s'` is already lowercase with no whitespace. H1's comment "not lowercased, not trimmed" is not enforced by any assertion. I verified raw hashing by reading the code, not through the tests.
- **N4 (H2's warn check is weaker than it reads).** It is case-sensitive and checks only the ref. An uppercased ref (P2) or a `tenantId` (M2) added to the warn survives H2. Only my CL1-R1 catches them. This is the same shape CE1 found on the row, now on the warn.
- **N5 (red by assertion, strictly).** The try/catch-removed arm reds H2 by a thrown rejection escaping `await`, not through an expect. CE1 N4 was the same pattern on F4. The claim's "each arm ... red" holds; "by assertion" does not for this arm.
- **N6 (Q3 judgement).** A missing key has no boot-time signal. It shows only per erasure: the warn's message (in prod files; its fields only on Console) and the row's missing `ref_hmac`. A key of the wrong length makes `initFromEnv` throw. Originate catches that as `PII encryption init failed`, which also leaves the HMAC key unregistered. That behaviour is pre-existing.
- **N7 (CE1 N1 unchanged, on purpose).** The ref is still in the never-seen info at `:1494-1497`, the INSERT-failure error at `:1577-1580`, and the pre-existing info at `:1583-1585`.
- **N8 (carried, unmeasured).** Two concurrent POSTs could still write two rows (CE1 N6). With (c), the two rows would now carry equal hashes, which is a correlator for a single subject.

## FOUND / TESTED / HOW
- FOUND (read):
  - the whole product delta and the whole unresolvable branch (`gdprService.ts:1480-1588`);
  - `encryptedField.ts:560-640`;
  - originate `index.ts` keyring init;
  - the compose and bicep wiring;
  - the logger redaction and file allow-list;
  - `mapDeletionLogRow` and `getDeletionLog`, and the `/deletion-log` route;
  - `connectorContext`;
  - the zod ref schemas;
  - every `lookupHash(` caller outside tests;
  - the test file's KS-758 block and its `@secuura/shared` mock;
  - the author's sent body.
- TESTED:
  - ls-remote at start and end;
  - merge-tree on live develop and on the claim's develop;
  - landing subtree equality;
  - the whole originate suite at 3 points, by cell name;
  - an own-program tsc of the test file with a positive control;
  - product tsc;
  - 11 mutant arms (A0 + 3 CE1 + 3 author + 2 mine + 2 probes);
  - 2 own cells against the REAL lookupHash/registrar.
- HOW:
  - `git clone --shared` of the spark cache into `scratchpad/gate_cl1/src`, plus a `gh` remote (read-only fetch of develop and `refs/pull/1666/head`).
  - `npm ci --ignore-scripts --prefix <clone>/Blockchain/Dev`, then `npm run build --prefix packages/shared`, then `npm run generate --prefix services/originate`.
  - My cells live in `<clone>/.../__tests__/zz-gatecl1-real.test.ts`. It is a generated copy of the author's file with the real `lookupHash` passed through and a `GATECL1` describe appended. It exists in the scratch clone only.
  - No cd, no rm, no Docker, no push, no GitHub/Linear writes, nothing under !CODING (the author's scratchpad was read only).

## NOT RUN
- The LIVE PR body (gh unauthenticated). I read the author's read-back copy (Q7).
- The author's "hash removed" arm (3 of 4 chosen).
- Real Postgres. CE1 proved the five-column INSERT. The new reason is 157 characters, measured. `reason` is `TEXT` (`migrations/001_initial-schema.sql:480`), and only two migrations name `data_deletion_log`: 001 and 036. The only `ALTER TABLE data_deletion_log` lines are 036:11-12, which touch the `deletion_method` CHECK. The same grep also finds 001, which is its positive control. So the length cannot be refused by the migration-built schema. The live database is unproven.
- The four platform suites (no stack).
- Whether the live vault's `pii-lookup-hmac-key` is non-empty (no Azure).
- Whether Platform S's PersonGuid is shared across organisations (N1).
- Concurrency (N8).

## Wall-clock
14:38:34 AEDT (03:38:34Z) to about 03:51Z, roughly 13 minutes.
`git -C /Volumes/DevMASTER/WEDNESDAY status --short` before writing: 24 untracked paths, 0 outside `0_Brain/`, `5_Project_History/`, `2_Project_Files/local-model/` or `2_Project_Files/fleet/briefs_staged/`.
sha256 (sed '1d;$d' verdict.md | shasum -a 256): 1f76bec4d389ffffb8a930138e52b1928b0f50a2aaaf7760d0b16751043c7df1
