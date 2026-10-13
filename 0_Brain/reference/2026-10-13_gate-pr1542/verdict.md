# Gate verdict: PR #1542 (KS-1119), Opus tier 1

Report sha256/16: dc6118785b29974c
(Recipe: delete the single line starting "Report sha256/16:" from this file, sha256 the remaining bytes, keep the first 16 hex characters.)

- **Head under test:** `9d23343a5ab7b63479feea8150674f631102f270`, tree `b01229fd1cd4297ffd6dc2f44436dfdc307ba4ed`, parent `a7cffc8d9831e67d91f6dd24d0047ffe3e26c97e` (live develop when I checked).
- **VERDICT: GO WITH NOTE.** Major findings: **0**. Minor findings: **2**.
- **What the verdict means:** the proven defect is fixed. A wrong hash no longer gets verified:true, and the stored hash is no longer handed back. I measured this from scratch against the real service: four aliases, four callers, both tenancy modes, both database layouts. verify-file's orphan / empty-external_id path is fixed too. Which registration a hash resolves to did not change, so the stop condition did not fire.
- **The note, which must be acted on before merge:** two behaviour changes are not named in the PR, and three sentences in the PR body are false:
  - "Single-tenant: no change."
  - "The only true→false flip anywhere is cell C."
  - M2 has "no reachable trigger".
- **What would require a delta gate:** correcting the PR body does not change the head. Changing (b) to the minimal fix under m-1 does change the head and needs a delta gate.
- I do not recommend deploying. Merge only on Wednesday's head-bound GO.

## Instruments and environment (all mine, in the scratchpad; nothing written inside !CODING)

- **Code:** a `git clone --shared` of the project into my scratchpad, with the push URL set to `DISABLED`. I fetched `refs/pull/1542/head` and `develop` with the project's `core.sshCommand`.
  - Asserted heads: `rev-parse` gave 9d23343a / a7cffc8d.
  - `ls-remote` immediately before writing: develop `a7cffc8d…` and pull/1542/head `9d23343a…`, matching both.
  - The project's own checkout stayed at `40ed3573`, untouched.
- **Runtime:** Node v24.7.0, a fresh `npm ci`, shared built, and the Prisma client generated in my scratch worktree.
- **Postgres:**
  - PostgreSQL 15.14 (Homebrew) on **port 55414**. lsof showed 55413, 55416 and 55418 held by others; 55436 and 55418 were never touched. TCP only, fsync off, UTC.
  - Three databases, built by `docker/init/*.sql` (00-create-platform-db skipped, it needs dblink) plus `docker/init-platform/*.sql`, then `scripts/run-migrations.sh`:
    - **L1 split:** `secuura` holds the tenant tables (112) and `secuura_platform` holds the platform tables (10).
    - **L2 single:** `secuura_one`, 120 tables.
  - Migrations: **applied=51 failed=0, rc 0 in both layouts.**
  - `secuura_app` is NOSUPERUSER NOBYPASSRLS (`false/false`), and documents RLS is enabled/forced `true/true`.
  - Evidence: `evidence/pg_setup.log`.
- **Develop variant:** `git diff --stat develop..head` shows exactly 2 files: verification.ts (+11/−3 lines, 14 changed) and the new test file (251 lines). So "develop" is the head tree with develop's `verification.ts` (sha256/16 `409083b94072b094`); head's is `17dcfa76577a107d`. Every run log records the sha of the file actually in place.
- **Tenant-manager assertion (with a control that fails):**
  - Every MT=true run logs `[DB] Multi-tenancy enabled — using TenantPoolManager`. The author's SETUP cell asserts `getTenantManager()!==null === MT`.
  - **Control:** MT=true with PLATFORM_DATABASE_URL unset (layout `L1fallback`) logs "falling back to single-tenant mode", and SETUP **reds** (plus B-outsider ×4 and F). Evidence: `evidence/runs/ctl_head_mttrue_fallback.log`.
- **Two harnesses:**
  - **(i) The author's 18 cells**, run under jest as an independent re-run.
  - **(ii) My own probe**, `evidence/tools/probe.mjs`. It does not use the author's harness. It boots the **real `services/originate/src/index.ts`** with tsx, so the real middleware chain runs: gateway provenance, extractTenantContext and the KS-458 tenant block. It sends real HTTP. Callers are tenant A (the owner), B and C (outsiders) via `x-tenant-id`, and anonymous (no header). 444 cells per run, seeded with random hex per layout (`evidence/fixtures_*.json`).

## FOUND / TESTED / HOW

### Item 1. The author's 18 cells, the integration files and the unit suite

**18 cells, 3 runs each, both modes, both layouts.** Instrument: jest via `evidence/tools/run.sh`.

| variant | MT=true L1 | MT=true L2 | MT=false L1 | MT=false L2 |
|---|---|---|---|---|
| develop (3 runs) | 6 failed / 12 passed ×3 | 6/12 ×3 | 18/18 ×3 | 18/18 ×3 |
| head (3 runs) | 18/18 ×3 | 18/18 ×3 | 18/18 ×3 | 18/18 ×3 |

- **Develop's red set, by name:** A hash, A contentHash, A providedHash, A documentHash, C, E-probe. This matches the claim.
- **Controls:**
  - Develop reds, so the harness can fail.
  - The fallback-layout control reds SETUP.
- Evidence: `evidence/item1_summary.txt`, `evidence/runs/cells_*`.

**All 12 originate integration files, 141 tests, develop vs head, per-test diff.** Instrument: `evidence/tools/jcmp.py`.

| comparison | result |
|---|---|
| MT=true, L1 and L2 | exactly the 6 KS-1119 cells differ (✕→✓); every other test is identical |
| MT=false, L1 and L2 | 0 differing |

- **My environment's absolute numbers differ from the author's**, identically on develop and head:
  - L2: 6 `rightsHolders.tenant-scope` failures in all four runs. Cause: `new row violates row-level security policy for table "tenant_config"`, because I gave the suite the platform URL as `secuura_app`.
  - L1: about 80 failures, because the other suites assume the platform tables live in the tenant database.
- So **I did not reproduce "fix 141/141"**. I did reproduce "identical before and after except the 6".

**Unit suite** (`jest.config.js`): develop and head are both **105 suites / 1321 tests, 0 failed**, rc 0. The per-test diff is 0.

**tsc and eslint:**
- `tsc --noEmit` on originate at head: rc 0. Control: a planted type error gives rc 2.
- eslint on both touched files: rc 0. Control: a planted `var` gives rc 1.
- I did not run `check:openapi` (see NOT tested).

### Item 2. The defect, from scratch (real service)

Wrong hash, all four aliases, with a registered documentId. Two documents: one stored bare, one stored `sha256:`. Callers A, B, C and anonymous. Both modes, both layouts.

- **Develop, MT=true:**
  - Every one of the 32 alias cells, plus the `sha256:`-prefixed wrong hash and `"sha256:"` alone, answered `verified:true`, `hashValid:true`, `integrityVerified:true`, `documentExists:true`.
  - The body carried the **stored** `contentHash` (`storedHandedBack:true`).
  - Reproduced.
- **Head, MT=true:** all 52 wrong-hash cells claim nothing, except the 4 `other-docs-right-hash` cells explained below. The stored hash is handed back in **0** of the alias/prefixed wrong-hash cells.
- **MT=false:** develop and head are identical.
- **Is the anonymous path reachable?**
  - Non-production: yes. It resolves to the default tenant, and the defect reproduced for `anon`.
  - With `NODE_ENV=production` under MT, originate refuses a request with no `x-tenant-id` with **400 "Missing tenant context"**. With an outsider's `x-tenant-id`, head answers right hash → verified:true and wrong hash → not-registered.
  - So in production an anonymous caller reaches /verify only through the gateway, and the gateway is not tested here.
  - Evidence: `evidence/prod_anon_reachability.txt`.
- **Counts:** dev→head differences are **248 of 444 cells in each MT=true layout**, all of them true→false or claim→no-claim. MT=false differs in 3 cells (see m-1).
- Evidence: `evidence/probe_g1_dev_vs_head.txt`, `evidence/probe/` and `evidence/probe_r1/`.
- **Re-runs:** a second boot of develop and head in L1, both modes, gave 0 differing cells from the first.

### Item 3. Every producer of verified:true / hashValid:true in originate

Instrument: `git grep` at head, then reading each site.

- **`routes/verification.ts`:**
  - **:703 / :728** (verify-file chain-first): the chain said `verified`. Unchanged and out of scope.
  - **:791** (verify-file row path, `hashValid: true` hard-coded): rows come from the local by-hash query (hash-matched) or from `crossTenantLookup('', fileHash)`. With (a) that function can only return rows from the tenant by-hash query (:553-563). Measured: orphaned prefixed registration, deleted-document registration, and drift registration (document_id pointing at a real document with another hash), each with an `''`-external_id row and a NULL-external_id row present:
    - develop MT=true: verified:true with the unrelated `''` row (id 39c9dfe5…), all 4 callers;
    - head: not-registered in every case.
  - **:1125 / :1152 / :1176** (strategy-1 chain fallback): reached only when rows=0. Not changed.
  - **:1214** `buildResponse(docRow, hashMatch)`: rows come from the local by-hash query or crossTenantLookup. With (a), crossTenantLookup returns only by-hash rows. I found **no other path to :1214 for an uncompared row**.
  - **The chain fallback** returns early with its own body, or falls through with rows untouched. I confirmed this by reading :1037-1189: `rows` is never assigned there.
- **`routes/verificationV2.ts:269`** (chain-only match) and **`buildMatch(…, true)` :409:** rows come only from by-hash queries, local and cross-tenant (:315-372). There is no id fallback. Unaffected.
- **`routes/documents.ts:1546` and `certifications.ts:1030`:** these compare the hash themselves (`providedHash === document.contentHash`, `currentHash === certification.contentHash`). Unaffected.
- **Revoked:** wrong hash on a revoked document. Develop said verified:false but `hashValid:true` with the stored hash; head says not-registered. Right hash on a revoked document: unchanged.
- **The by-id strategy (documentId only):**
  - Under MT, from B, C and anonymous it still resolves across tenants: `documentExists:true`, `verified:false`, `hashValid:false`.
  - Single-tenant answers not-found outside the tenant.
  - Identical on develop and head: **0 `3.byid` cells differ, against 358 `4.right` lines in the same diff file as a positive control.**

### Item 4. The fix's own risk: callers, and the right-hash matrix

**Caller census** (a read-only sweep of the repo; table in the conversation record, summary here):

- **Gateway:** the api-gateway no longer handles `/api/verification/verify`. It proxies the path and body unchanged; it neither adds a documentId nor normalises the hash (static reading only).
- **No caller in the repo trims or lowercases a hash.**
- **Callers that send documentId plus a hash:**
  - e2e-v2 `api-client.ts:288` (providedHash, bare, server-returned);
  - USER_TESTING v2.3 :401/:429/:458 (server-returned) and :410 ("Wrong hash → verified=false", `'0'*64`);
  - systemTest schemathesis `test_workflows_lifecycle.py:121` and `platform_ops.verify_document` (server-returned);
  - `alternative-paths.spec.ts:230` (wrong hash);
  - mcp-server `http-server.ts:131` / `/verify-batch` (user-supplied raw contentHash passed through);
  - the OpenAPI VerifyRequest example.
- **What changes for them:**
  - Server-returned hashes are exact, so they are unchanged.
  - The wrong-hash cells now get the answer they assert (verified=false).
  - Only the mcp-server passthrough of a user-typed hash can reach the flips below.
- **frontend/verifier, connectors, SDK, outlook, gmail, m365:** contentHash only (`sha256:`+lowercase hex) or documentId only. Unchanged, except the orphan/empty-external_id case, which now answers not-registered as intended.

**Right-hash matrix:**
- 2 stored formats × 12 sent spellings × {own documentId, none, documentId of a tenant-B document} × 4 callers × 2 modes × 2 layouts.
- The 12 spellings: bare, `sha256:`, UPPER, `SHA256:`, `sha256:`+UPPER, mixed case, leading space, trailing space, trailing `\n`, `0x`, `00`-padded, `sha256:sha256:`.
- **The four format pairs the author measured are identical on develop and head**, for own documentId and for no documentId, from every caller, in both modes. This confirms the author's 16 readings.
- But the author's "only flip" claim is wrong, and a single-tenant flip exists. See m-1 and m-2.

### Item 5. Stop condition: same-hash registrations

- **Setup:** one hash H5 registered in tenant A (a certified document, older) and in tenant B (a certified document, newer). Tenant A also holds a draft row of H5 stored `sha256:`.
- **Probes:** sent bare and `sha256:`, with no documentId and with documentId dupA / dupA2 / dupB, from A, B, C and anonymous, in both modes and both layouts.
- **Result:** **0 of 32 `5.*` cells differ between develop and head in any of the 4 comparisons.** The same row wins every time:
  - A sees dupA;
  - B sees dupB;
  - C and anonymous see dupA with no documentId and dupB with documentId dupB.
- **The stop condition did not fire.**
- **Instrument sensitivity:** mutants M8 and M9 change the 5.* readings, so these cells can detect a change.

### Item 6. Mutants

12 mutants, generated by `evidence/tools/mutants.py`; each sha256/16 is in `evidence/mutant_shas.json`. Each was run two ways:
- the author's 18 cells, MT true and false, L1;
- my 444-cell probe against the real service, MT true and false, L1, compared cell by cell against head.

| mutant | author's 18 cells, MT=true | author's 18 cells, MT=false | my probe, MT=true | my probe, MT=false |
|---|---|---|---|---|
| M1 drop the gate | KILLED by A×4 and E-probe | survives | KILLED (242 cells: 2.wrong.*, 3.file/verify orphan/drift/deleted) | survives |
| M2 `hashMatch = true` | **survives** | **survives** | **KILLED** (6: `4.right.storedPref.double_pref.*`) | **KILLED** (3: same) |
| M1+M2 (≈ develop) | KILLED by A×4, C, E | survives | KILLED (248) | KILLED (3) |
| M3 row side not normalised | KILLED by B×4 | KILLED by B×2 | KILLED (25) | KILLED (10) |
| M4 gate inverted | KILLED by A×4, E, F | survives | KILLED (251, incl. 3.byid) | survives |
| M5 comment-only control | survives | survives | survives (0) | survives (0) |
| M6 gate on `!documentId` | KILLED by E-probe and F | survives | KILLED (37: verify-file orphan, 3.byid) | survives |
| M7 `!docRows` guard removed | KILLED, **compile-time only** (TS18048 "docRows is possibly undefined", 18/18 load-fail) | same | survives (0); behaviourally equivalent under tsx | survives |
| M8 sent side not normalised | KILLED by B (4) | KILLED by B (2) | KILLED (27) | KILLED (14) |
| M9 flag from documentId | **survives** | **survives** | KILLED (24: other-docs-right-hash, tenantB-hash, 5.dup) | KILLED (16) |
| M10 fallback restored for documentId `''` only | KILLED by E-probe only | survives | KILLED (28: verify-file and /verify hash-only orphan) | survives |
| M11 tenant hash query drops the `sha256:` form | KILLED by B outsider (1) | survives | KILLED (6) | survives |

Cell-level detail: `evidence/mutants_cells_byname.txt` and `evidence/mutants_probe_summary.txt`.

**Judging M2:**
- (b) is **not** dead code, and it **does** have a reachable trigger once (a) is in place, in **both** modes.
- The trigger is a hash sent as `sha256:sha256:<hex>` for a row stored `sha256:<hex>`.
- The lookup matches that row through its `hashNorm` term (`content_hash = 'sha256:<hex>'`), but (b) compares `normaliseHash(row) = '<hex>'` against `hashNorm = 'sha256:<hex>'`. The result is false.
- So (b) **can and does produce a false not-verified for a row the lookup itself matched** (m-1).
- (b) also gives real defence in depth. Under M10 (the fallback re-opened for documentId `''`) it is what keeps /verify hash-only from claiming verified:true, though the unrelated document is still named.
- **Recommendation:** keep (b), but make it the same predicate as the lookup (minimal fix under m-1). It is then unreachable as a false negative and still catches any future uncompared row.

**Gap in the author's cells:**
- M9 survives all 18 of the author's cells. No cell sends a documentId that names a different document from the one the hash matches.
- M2 survives because no cell sends a double prefix.

### Item 7. Scope and hygiene

- **Diff stat vs develop:** 2 files, +262/−3.
  - `Blockchain/Dev/services/originate/src/routes/verification.ts`: +11/−3.
  - The new test file: +251.
- **merge-tree:** `git merge-tree --write-tree develop head` gives `b01229fd…`, rc 0, so it merges cleanly and the result equals the head tree.
- **Commit:** author and committer are Kam Kreiser; one commit; parent a7cffc8d. The message ends `Refs KS-1119` with a Co-Authored-By trailer. **No closing keyword** in the message (grep for close/fix/resolve finds nothing).
- **Amend claim:** the pre-amend sha `f2fef256` is **not present** in my clone ("Not a valid object name"). So I **could not verify the tree equality across the amend**. The pushed head's tree is the one gated.
- **PR body:** I read the author's local copy `5_Project_History/2026-10-13_seatJ-7th/evidence/ks1119/pr_body_final.md`. `gh pr view` failed: no gh auth in that project's config, and I did not look further for credentials. So **the live PR body was not read**.
  - The local body has `Refs KS-1119` and no closing keyword.
  - Three of its claims are false; see the note at the top and m-1 / m-2.
  - I made no Linear read or write.

## Findings

### m-1 (Minor): (b) disagrees with the lookup it guards. Unnamed true→false flip in single-tenant mode, the live configuration

**Where:**
- `services/originate/src/routes/verification.ts:1212` (head):
  ```ts
  const hashMatch = typeof docRow.content_hash === 'string' && normaliseHash(docRow.content_hash) === hashNorm;
  ```
- versus the lookup at :1015-1026 (`content_hash = computedHash OR = hashNorm OR = 'sha256:'+hashNorm`, with `hashNorm = computedHash.replace(/^sha256:/,'')`, :1003/:1008);
- and crossTenantLookup :553-563 (same three terms).

**Reproducing shape:**
- MULTI_TENANCY_ENABLED=false, caller in the owning tenant, document stored `content_hash='sha256:<hex>'`, `POST /api/verification/verify {"contentHash":"sha256:sha256:<hex>"}`.
- Develop: `verified:true, hashValid:true, integrityVerified:true`.
- Head: `verified:false, documentExists:true, hashValid:false, integrityVerified:false`, with `contentHash` = the stored `sha256:<hex>`.
- Controls from the same boot: `sha256:<hex>` and `<hex>` stay verified:true on head.
- Also with own documentId, and with documentId of a tenant-B document. Under MT: own documentId from all 4 callers, no documentId from tenant A.
- Evidence: `evidence/raw_double_prefix_mtfalse.txt` and the MT=false section of `evidence/probe_g1_dev_vs_head.txt` (3 cells per layout).

**Why Minor and not Major:**
- It fails closed, on a malformed input.
- No caller in the repo sends a double prefix.

**Why it is a finding:**
- It contradicts "Single-tenant: no change" and "M2 … no reachable trigger".
- It gives a self-contradictory answer: "document exists, hash invalid" for the row matched *by* that hash.
- Wednesday's ruling makes every true→false flip a named behaviour change.

**Minimal fix:** compute the flag with exactly the lookup's predicate:
```ts
const hashMatch = [computedHash, hashNorm, 'sha256:' + hashNorm].includes(docRow.content_hash);
```
This changes the head, so it needs a delta gate.

**Alternative (no head change):** name the flip in the PR body and correct the three false sentences.

### m-2 (Minor): unnamed multi-tenancy flips beyond "whole hash upper case"

The PR's "only true→false flip anywhere is cell C" is false. Under MULTI_TENANCY_ENABLED=true, from all four callers including the owner A, the head turns develop's verified:true into **"This document hash is not registered"** for:

- **(a) Other spellings of the right hex with the document's own documentId:** mixed case, `SHA256:` prefix, `sha256:`+UPPER, leading space, trailing space, trailing newline, `0x` prefix, `00`-padded, double prefix. Both stored formats.
  - Develop "verified" these only because the id fallback answers true for **any** string. So the flip is the defect being removed. It is correct, but undercounted: the author's attack point 2 asked exactly this question, and the answer is "no, every non-exact spelling flips".
- **(b) The exact right hash with the documentId of a document in another tenant:**
  - Shape: A's hash plus B's documentId from callers B, C and anonymous; B's hash plus A's documentId from A, C and anonymous; all spellings.
  - Develop: verified:true naming the **wrong** document (the documentId's own row and its stored hash). That is the defect.
  - Head: "not registered", although the same hash with no documentId verifies.
  - Cause, pre-existing: `crossTenantLookup` looks up the registry by documentId first (:526-531) and never falls back to the by-hash registry search (:532) when that tenant has no hash match.
  - The new answer fails closed, but the text "This document hash is not registered" is false.
- Evidence: `evidence/probe_g1_dev_vs_head.txt`, the `4.right.*` lines for L1 and L2 MT=true.

**Minimal fix:**
- In the PR body: replace "only flip … C" with these classes.
- In a follow-up ticket, not this PR: in `crossTenantLookup`, when the documentId-resolved tenant has no by-hash row and a hash was supplied, retry the registry by hash. This needs its own KS-584/590 review because it touches which registration answers.

### Observations (pre-existing, unchanged by this PR, identical on develop and head; listed so nobody reads them as covered)

1. **The documentId-only answer hands any caller the stored `contentHash`** (verification.ts:1344), across tenants under MT. The wrong-hash path no longer leaks it, but anyone holding a documentId gets it anyway.
2. **`{documentId: X, hash: <document Y's hash>}` answers verified:true naming Y.** The documentId is ignored when the hash matches; all callers, both modes. A relying party that reads only `verified` would accept the hash as document X.
3. **KS-1590 is wider than verify-file.** The registry by-hash search (`content_hash = $1`, exact, :533-535) also makes /verify hash-only cross-tenant answers depend on the sent spelling. Example: a bare-registered hash sent with `sha256:` and no documentId answers not-registered for outsiders. The function is shared, so KS-1590 should name /verify too.
4. **Registry by-hash `LIMIT 1` has no ORDER BY** (:533-535). Which tenant's registration answers an outsider is arbitrary. That is KS-584/590 territory, and the same on both versions.

## NOT tested (and whether it could hide a Major)

- **The api-gateway in front:**
  - Not run. I only read it: the census says the path and body are proxied unchanged.
  - A gateway that injected a documentId, or normalised hashes, would change which m-2 flips are reachable. It cannot re-open the fixed defect, because (a) is in originate.
  - Unlikely to hide a Major.
- **Any deployed environment, and whether MULTI_TENANCY_ENABLED is on anywhere:** UNMEASURED.
  - m-1 matters there regardless, because it is single-tenant.
  - The original defect's live severity depends on that census, not on this PR.
- **Per-tenant-DB mode (`PROVISION_PER_TENANT_DB=true`):**
  - Not run.
  - (a) and (b) do not depend on which pool `getPool` returns, so I see no mechanism for a Major. That is an argument, not a measurement.
- **Akto BOLA on /verify, Schemathesis, Playwright, k6:** not run.
  - BOLA-shaped cross-tenant reads were exercised by my B/C/anonymous callers at originate level only.
- **Not run by me:**
  - `check:openapi` (the PR claims no spec change, and the diff touches no spec or openapi file);
  - the push-hook preflight;
  - the e2e-v2 / USER_TESTING / schemathesis suites named in the census.
- **Not reproduced:**
  - "fix 141/141": my environment has 6 (L2) or about 80 (L1) unrelated failures, identical before and after.
  - The amend's tree equality: pre-amend object f2fef256 not available.
  - The live PR body: not read.
- **NODE_ENV=production:** tested only for the anonymous-reachability question above.

## Clean-up

- My PostgreSQL on 55414 is stopped (`pg_ctl stop`). lsof shows no listener on 55414 or on the service ports 47100-47140.
- No originate, tsx or jest processes of mine are running.
- The scratch clone, worktree and data stay in my session scratchpad.
- Nothing was written in `!CODING`. No git write verb ran in the project folder. No push, and no GitHub or Linear write.
