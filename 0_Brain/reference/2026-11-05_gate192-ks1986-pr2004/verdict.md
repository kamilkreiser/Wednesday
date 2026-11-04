GO WITH NOTES — HOLD-FOR-KAM (G192-F1: if the original's tenant has no registry row, or falls past the 8-tenant cap, v1 now shows ANOTHER tenant's later certification, which v2 already does; G192-F2: if the cross-tenant read fails and the chain answers, v1 shows the chain's certification with its issuer org UUID and name where base showed the local one. Neither is more permissive by count; both show a certification base did not show, and it is not shown to be the original holder's)
# QA Gate 192 (Tier 1, round 1): PR 2004 / KS-1986 v1 verify judges the original registration across tenants, as v2 does

## Subject (pinned at start AND end; the same at both)
- Start 2026-11-04 20:49:42Z, `git ls-remote origin` on the read-only checkout: `refs/pull/2004/head` = `577f668f478679a3e4965a28fba6b96a9e2212d6`, `refs/heads/develop` = `4ff25fb4f2c05192be178f941d746175d609471f` (`runs/pin_start.txt`).
- End 2026-11-04 21:02:23Z: the same two SHAs (`runs/pin_end.txt`). The head did not move and develop did not move.
- PR head parent = `035685291b9d58ae6ea8ba5f05adf9379f9c2944` (the built base); 1 commit.
- **Merge tree for the merge seat:** `git merge-tree --write-tree 4ff25fb4f2c0 577f668f4786` gave rc 0, tree **`cee76ac32b3655cc9597b7244a84e4a7ca0cef7e`** (run at the start and again at the end: the same). `diff --numstat develop..cee76ac3` is exactly the PR's 5 files with the PR's own counts, and the blob of each of the 5 paths in the merge tree equals the head blob (5 of 5).
- Host: macOS, Node v26.8.1 (NOT Node 24 LTS), TypeScript and jest from `npm ci` against the head's `Blockchain/Dev/package-lock.json` (workspaces originate + shared, `--ignore-scripts`, then `npm run build -w @secuura/shared`), PostgreSQL 15.19 (Homebrew keg).
- Method: I cloned the read-only checkout with `git clone --shared` into `repo/` and fetched `refs/pull/2004/head` and develop into that clone only. I drove the REAL `verificationRouter` and `verificationV2Router` over HTTP against my own PostgreSQL 15 cluster (socket `/private/tmp/g192/s`, port 55492, `listen_addresses` empty, postmaster pid 40131 recorded and stopped). There were 11 databases: the caller, nine other tenants, and the platform registry. Seat F 32nd's DB seam is copied into `pgcell/g192-pg15.harness.test.ts`: the seat's 10 cells re-typed, plus 17 cells of my own. Each run records the whole response body and headers for v1 `/verify`, v1 `verify-file` and v2. Base is the base blob overlaid in my clone and restored by `git checkout` (blob checked equal). `tools/compare.py` does the base-vs-head comparison, with no assertions in the harness. Mutants were run twice, once over the unit files and once over the PG matrix (`tools/mutants.py`). The suites ran in my clone with CWD in `cwd/` under `env -i`.

## Findings

### G192-F1 — MAJOR (HOLD-FOR-KAM): when the original's tenant is not among the registry tenants read, D-B2 presents a foreign LATECOMER's certification
- **FOUND:** `judgeAcrossTenants` (verification.ts 672-695 at head) treats the earliest row among the registry-listed tenants as "the original". When every local row is a certified copy that the cross rule refuses, it presents that foreign row and its certification. If the true original's tenant is missing from that set, the foreign row it presents is itself a later copy:
  - `G-ORIGINAL-UNREGISTERED`: B is the original at t0 in T2 with no registry row; Y certified a copy at t20 in T3; A certified a copy at t31 in the caller. Base presents `cert-a-1` (the caller's own latecomer). Head presents **`cert-y-1`** (T3's latecomer), `documentId doc-cert-y-1`, `certifierOrganizationId null`, `certifiedBy null`. This holds on both `/verify` and `verify-file`.
  - `G-CAP-9-SKEWED`: B's tenant is registered, but its registry `created_at` is later than 8 other tenants' rows, so the `LIMIT 8` drops it. Head presents **`cert-y-2`** where base presented `cert-a-1` (2 of 2 v1 paths).
  - In both cells, base presents a latecomer's certification too (the caller's own). The count of certifications is unchanged, so head is not more permissive by count. But head presents a DIFFERENT certification that is not the original holder's, which is the class bar's Major.
  - v2 presents the same latecomer at base and at head (`cert-y-1`, and in v2 with `certifierOrganizationId dddddddd…`). So this PR brings v1 into line with v2's pre-existing behaviour.
- **TESTED:** Both cells on both v1 paths and on v2, at PG15, base and head. The natural-order control `G-CAP-9-NATURAL` passes: 10 tenants hold the hash and the original's registry row is earliest, so it is read and head presents B with no certification. `G-CAP-9-SKEWED-NOCERT` passes too: same skew, but the copies are uncertified, and head presents T2's uncertified copy with no certification. **Reachability is read, not measured:**
  - registration is fire-and-forget and its failure is swallowed (`registerInPlatformRegistry` catch → `logger.warn`; documents.ts:794 `.catch(() => {})`);
  - the registry is written only on the create path;
  - api-gateway `startup-migrations.ts:500-509` (KS-39 #4) records a past window in which "every fresh /api/documents create failed to register in the cross-tenant registry".

  How many production hashes have an original with no registry row was NOT measured.
- **HOW:** `runs/pg_base2.jsonl`, `runs/pg_head2.jsonl`, `runs/direction_base_head_v2.txt` (classes DIFFERENT). Mutant m6 (keeping `issuerId`) changes exactly these cells' `certifierOrganizationId`, which shows the cells reach the D-B2 path. Shape of a fix, for the rulers rather than the gate: D-B2 could present the foreign row without its certification unless the foreign original is corroborated. That is a design choice, so this is HOLD-FOR-KAM, not FIX-BEFORE-MERGE.

### G192-F2 — MAJOR (HOLD-FOR-KAM): on a cross-tenant read failure with every local row certified, D-B4 hands v1 to the chain fallback, which presents the chain's certification with its issuer org UUID and issuer name, unscoped
- **FOUND:** `G-CHAIN-UP-REGISTRY-DOWN`: the registry is unreachable; A has a certified copy alone in the caller; the (stubbed) anchoring service answers `verified: true` with metadata `{certId, issuerName, issuerOrgId, documentId}`.
  - Base presents the local `cert-a-1` and never calls the chain (chainCalls 0).
  - Head (D-B4, `skipCrossTenantLookup`, then the existing chain branch) calls the chain once and presents `source: blockchain` with `certification.certificationId = cert-chain-x`, `certifierOrganizationId = <planted org UUID>`, and `certifiedBy` / `issuer` = the planted issuer name. `onChainMetadata` carries the same values.
  - The canary search hits 2 of 2 v1 paths (org UUID and issuer name). The chain's certification is not judged against the original holder at all.
  - **Control:** `G-CONTROL-NO-LOCAL-CHAIN-UP` (no rows anywhere) exposes the same two values at base AND head. So the chain branch's exposure is PRE-EXISTING (base = head), and this PR gives it a new reach: an input that has a local row.
  - This also applies whenever one tenant's originals read fails (`G-TENANT-POOL-THROWS-ALL-CERTIFIED` takes the same branch; that cell ran with the chain down).
- **TESTED:** Both v1 paths at PG15, base and head, with the chain stubbed by global `fetch` (no anchoring service contacted). D-B4's text, "(the chain, else not found)", names the chain, so the route was ruled. What it presents (a certification, an org UUID, an issuer name) is what I am raising under KS-590 = a. Whether on-chain metadata counts as "tenant-owned naming" is Kam's ruling, not the gate's.
- **HOW:** `runs/pg_head2.jsonl` rows `G-CHAIN-UP-REGISTRY-DOWN`, compared with `G-CONTROL-NO-LOCAL-CHAIN-UP`. The metadata fields are written by `certifications.ts:622` (`issuerOrgId: issuer.id`) and read by `anchorReadback.ts:151`.

### G192-F3 — NOTE: D-B2 shows the foreign original's own state, including `revoked`, to a caller holding a valid certified copy
- **FOUND:** `G-REVOKED-FOREIGN-ORIGINAL`: base answers `verified: true`, `cert-a-1`. Head answers `verified: false`, `status: revoked`, `documentId doc-g192-B-original`.
  - This is less permissive, but it tells the caller that another tenant revoked its registration.
  - v2 shows the same (`revoked`) at base and head.
  - The fields head adds over base in every D-B2 cell are the foreign row's `documentId` (external_id), `documentType`, `status`, `certifiedAt` (its created_at), `contentHash`/`fileHash` and `checks`. Title, issuer, certifiedBy and certifierOrganizationId are null.
  - The key set is identical to base's existing scoped cross-tenant answer (head `S-LEAK-CANARY` vs base `S-NO-LOCAL-ROW`: 9 of 9 keys on `/verify`; 10 of 10 on `verify-file` vs base `G-NO-LOCAL-ROW-PREFIXED-REGISTRY`). That is the D-B2 ruling as written.
- **TESTED/HOW:** Field-by-field diffs in `runs/direction_base_head.txt`. An external_id can be an S-supplied `documentUuid` (KS-596): an identifier, not a name.

### G192-F4 — PRE-EXISTING (base = head), filing candidate (c): registry rows hold the hash in whatever form the create path was given, and crossTenantLookup compares only one form
- **FOUND (code at head):**
  - documents.ts:679 `const hash = clientHash || generateContentHash(data)`. `generateContentHash` (documentRepo.ts:221) returns bare hex.
  - A client `contentHash` passes validation with an optional `sha256:` prefix (documents.ts:577-581, which only lowercases a COPY for the check) and is stored and registered raw (documents.ts:795).
  - So registry rows hold BOTH forms: bare hex (server-hashed or bare client hash) and `sha256:<hex>` (a prefixed client hash).
- **Measured at PG, base = head:**
  - `S-NO-LOCAL-ROW` (bare registry row): `/verify` finds B, but `verify-file` answers not found, because it passes `sha256:<hex>` (:900/:934).
  - `G-NO-LOCAL-ROW-PREFIXED-REGISTRY` (prefixed registry row): `verify-file` finds B, but `/verify` answers not found.
  - Each path misses the other form.
- The NEW `readCrossTenantOriginals` binds all three forms. `G-REGISTRY-PREFIXED-FORM`: head finds the prefixed-registered original.
- Read only: an upper-case client hash is also stored raw and would match none of the three forms anywhere. Not driven.

### G192-F5 — NOTE: the cheat-sheet fragment says "Not measured here. Real PostgreSQL across tenants", but the READY reports Seat F 32nd's PG15 run
- A stale line in `Projects Documents/fragments/cheat/KS-1986-v1-original-across-tenants.html`. It is a docs accuracy note and changes no behaviour.

### G192-F6 — NOTE (cost): the caller's own tenant is read and counts toward the cap of 8
- In every multi-tenant cell the caller's tenant (`g_ten`) is among the per-tenant originals reads, and its rows are then dropped by the id dedupe. That costs one query and one of the 8 cap slots per verify. In `G-CAP-9-NATURAL` it takes a slot that a foreign tenant could have used.

## What passed (measured)
1. **Scope:** `diff --numstat 035685291b9d..577f668f` = 5 files exactly as the READY names them (verification.ts 158/10; the new test 334/0; ks1561-g188-f1 test 2/2; 2 fragments 16/0 and 8/0).
   - The existing-test change is 2 lines: the `describe` title (line 351) and the one `expect` (line 355). There are 0 other lines.
   - 0 api-gateway files, 0 migrations, verificationV2.ts untouched.
   - Merge-tree shared paths between `035685291b9d..develop` (4 files, PR 2002 = KS-1401) and the PR: **0**. Planted control (the PR range against itself): 5. Develop-range self control: 4.
2. **Class bar over v1, PG15, 27 cells × 2 v1 paths = 54 rows (10 the seat's, 17 mine):**
   - NEW (head presents a certification where base presented none): **0 of 54**.
   - DIFFERENT: **10**. 4 are the original holder's own (`S-FOREIGN-ORIGINAL-CERTIFIED` cert-b-own; `G-THREE-TENANTS-TIED` cert-y-1, where Y holds a tied original). 4 are a latecomer's (G192-F1). 2 are the chain's (G192-F2).
   - LESS: 28. SAME: 16.
   - v2 equal base vs head: **18 of 18**.
   - Every DIFFERENT row on the D-B2 path has `certifierOrganizationId null` and `certifiedBy null` (D-B3).
   - My three named cases: three tenants with the original tied in two (DIFFERENT, an original holder's); the caller holding a certified latecomer AND an uncertified later copy (LESS: head presents the uncertified copy `doc-local-z` with no certification); a revoked foreign original (LESS, G192-F3). The schema has no soft-delete column (`\d documents` at head), so `revoked` is the only removal state.
3. **Disclosure:** foreign title, org name, owner UUID, issuer org UUID and issuer name planted on the foreign originals (`S-LEAK-CANARY`, `S-FOREIGN-ORIGINAL-CERTIFIED`, `G-THREE-TENANTS-TIED`). The search covered the whole serialized body plus headers.
   - Hits in head v1 DB-sourced rows: **0**.
   - Controls that fired: `G-CONTROL-LOCAL-CANARY` (canaries on the caller's own row) 3 hits at base and head. Mutant m2 (scrub dropped) gives title and issuer hits in 6 v1 rows.
   - The chain cells are G192-F2. Headers carry only content-type/connection/keep-alive/x-powered-by at both versions.
4. **Fail closed:** registry DB missing, one tenant DB missing, and `getPool` throwing for a tenant, each with local rows. In none does a local certification appear: no `cert-a` in any of the 8 head rows, and each logs 1 KS-1986 warn. HTTP is 200 in all; 0 `logger.error`, 0 HTTP 500, 0 uncaught throws. The chain-up variant is G192-F2.
5. **G188-F1:** `S-24-LATER-COPIES`: head presents B with no certification. Mutant m3 (LIMIT-ed foreign fetch) turns 2 of 2 v1 rows to NEW (a latecomer certification reappears) at PG, and red 4 in the unit files.
6. **m4 (dedupe by object identity):** I judge it equivalent, and agree with F 31st.
   - Under m4 the caller's own originals enter the union a second time as new objects carrying the same id, org and owner. That leaves the earliest instant and the three identity sets unchanged.
   - `certifiedRow` is only ever asked about local row objects, which stay members of `originalRows` if they are originals.
   - D-B2 runs only when no local row is eligible. A local row at the union's earliest instant is always eligible under both rules, so a duplicated local row can never be among the presented `originals`.
   - Tried: all 27 PG cells, including two probes with 26 certified rows tied in the caller (more ties than ORIGINAL_ROWS_LIMIT, both at the union's earliest instant and later than a foreign original). Result: 0 of 72 rows differ from head, and 0 of 85 unit cells red.
7. **Cost (PG statement counts per v1 verify):**
   - Single-tenant: 0 platform, 0 tenant (`S-SINGLE-TENANT`, as base).
   - Multi-tenant with local rows: 1 registry enumeration + 1 originals read per registered tenant, including the caller's (2 with two tenants, 3 with three, **8** in the three cap cells with 10 tenants).
   - With no local rows: as base (1 platform + 1 tenant via crossTenantLookup).
   - The D-B2 path also drops `/verify`'s local lineage query (local 2 → 1).
   - The cap keeps the earliest 8 tenants by registry `created_at` and drops the rest. It hides the original only when the original's registry row is not among the earliest 8 (G192-F1, `G-CAP-9-SKEWED`). In natural order it does not.
8. **Red proof and suites:**
   - Red at base (base blob overlaid, the head's two test files): **15 of 54 red, all by assertion** (0 `error TS`, 0 TypeError).
   - Green at head: 85 of 85 over the three unit files.
   - **Mutants (raw table):**

     | mutant | unit cells red (of 85) | PG rows differing from head (of 66) |
     |---|---|---|
     | m1 | 9 | 26 |
     | m2 | 9 | 24 |
     | m3 | 4 | 2 |
     | m4 | 0 | 0 |
     | m5 | 4 | 10 |
     | m6 (mine: D-B3 dropped) | 2 | 8 |
     | m7 (mine: D-B2 selection without the cross rule) | 0 | 0 |

     Headline = table: 5 of 7 killed. The survivors are m4 (the seat's, equivalent, above) and m7 (mine, equivalent: every row in `originals` sits at the union's earliest instant, so the local and cross rules both accept them all).
   - Every mutant was restored with its blob equal to the head blob.
   - Whole originate suite at head: **2,475 of 2,475 tests, 210 of 210 suites**, rc 0.
   - `tsc --noEmit -p services/originate`: rc 0. `tsc` over verification.ts + both test files with jest types: rc 0, 0 errors (planted control: rc 2, 1 error).
   - eslint on the three files: rc 0, 0 problems (planted control: rc 1, 2 problems).
   - `docs-fragments.mjs check`: clean rc 0; a planted dangling `<!--ref:KS-9999-…-->` gives rc 1 with 1 finding; restored (git diff clean) rc 0.
9. **Title/body:**
   - Title `Refs KS-1986: v1 verify judges the original registration across tenants, as v2 does` = 83 chars (limit 92).
   - Body line 1 = Kam's release line (card wed-morning-fleet-activity-1105 = a, 07:07:25 AEDT). Line 2 says the commit body's HOLD line is superseded.
   - The commit body (read from git) does carry `HOLD: do not merge until Kam taps 'a' …` as its first body line.
   - 0 close words before a key, in both the body and the commit message.
   - The title and body were read from the seat's own GitHub read-back files (`seatF-32nd/pr/title_b.txt`, `body_b.md`, `create_b.out`), NOT live from GitHub. The gate holds no Secuura GitHub identity.
10. **Merge:** see Subject. rc 0, tree `cee76ac32b3655cc9597b7244a84e4a7ca0cef7e`, 0 shared paths (control 5).
11. **Candidate (c):** see G192-F4. Registry rows hold both forms in code. PRE-EXISTING (base = head) on both paths; the new read covers all three forms.

## NOT tested
- Node 24 (ran on Node v26.8.1).
- A real deploy, demo, kintsugi, real Platform S traffic, and the real anchoring service (the chain was a global-fetch stub). Production data volume, index behaviour, and how many production hashes have an original with no registry row or a skewed registry order (G192-F1's reachability is read from code, not measured).
- The real tenant manager / `runWithTenantId` / RLS GUCs: stubbed by the seam. The request `db` and the caller's tenant pool were the same database here; in production they are assumed to be the same, not verified.
- Lineage walks (stubbed), the by-documentId strategy of `/verify`, and `verificationV2.ts` beyond base = head equality.
- The four platform suites (Schemathesis, Akto, Playwright, k6) and the KS-380 preflight.
- Upper-case client hashes stored raw (read only).
- GitHub live read of the PR title/body (taken from the seat's read-back files).

## Plain answer for Kam
After this merge, when two organisations have registered the same file, the public verify page credits the organisation that registered it first, not a later copier in the visitor's own tenant. It does this without naming the other organisation, and if the cross-tenant check fails it shows no certificate rather than a wrong one. I found no case where it shows a certificate that today's code did not show at all. Two edge cases need your call. First, if the first registrant's record never reached the shared registry (registration there is best-effort and has failed before), the page can now credit a different later copier, in another organisation, instead of the visitor's own copier. v2 already behaves this way. Second, if the cross-tenant check fails and the blockchain lookup answers, the page shows the certificate written on chain, including that issuer's organisation ID and name. Today's code shows the visitor's own local record in that case.
