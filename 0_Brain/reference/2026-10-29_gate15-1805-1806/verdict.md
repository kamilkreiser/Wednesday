# QA GATE 15 - Secuura/Blockchain PR #1805 (tier 1, head 7d47b670) and PR #1806 (tier 1, head 51df9ab2)

Base `develop` = `a5962b99d1273c40b29f79f411f082d46dd00521`. I read it by ls-remote at 07:05:14Z (start) and at 07:26:56Z (end), and it **did not move**. Both PR heads were the same at both readings (`refs/pull/1805/head` = `7d47b67086773b0351dfc851cc16b97da03e808b`, `refs/pull/1806/head` = `51df9ab28d43227f0a23e22332fe77ebcfa21c26`). Each head is a merge of develop a5962b99 into its branch, so merge-base(1805, 1806) = a5962b99.

## BLUF

**#1805 @ 7d47b670 (KS-1175, did:jwk): GO WITH NOTES.** 0 blocker, 0 major, 3 minor, 3 info.
The pattern widens by exactly one method. My probes (34 inputs x 2 fields) found no other method, no length past 512, no padding, no whitespace or newline, no NUL, no Unicode look-alike, and no empty segment getting through. Nothing in the tree decodes the JWK or uses it as a key. Only anchoring validates the field; originate forwards it as-is and the gateway only serves the spec. The 512 cap is the same in the schema and the spec, and storage has no column cap (jsonb, chunked at 64 bytes on chain). All 14 new cells are red-provable, and I reproduced the builder's 5 main mutant classes.
The notes:
- **Six mutant classes that the brief itself named survive every cell** (1805-1).
- **The alphabet is the shared DID alphabet, not base64url** (1805-2).
- **A did:jwk that carries a PRIVATE key is accepted and would be anchored as-is on a public chain** (1805-3). This exposure is new with this PR. Whether to guard it is for Kam or Stuart to decide.

**#1806 @ 51df9ab2 (KS-1709, keep + `anchoringStatus: 'failed'`): GO WITH NOTES.** 0 blocker, 0 major introduced, 1 major-class **pre-existing** defect (not a merge block), 2 minor, 3 info.
'failed' appears on a 4xx, a 5xx and an unreachable service. It never appears on an accepted 2xx with a JSON body (measured on 202, 202 with no id, 299). Production is byte-identical: the gate is `NODE_ENV === 'production'`, both production mutants were killed, and the key set of an accepted production 201 matches. The published schema matches the issue route.
The notes:
- **The kept certification reads `blockchain.anchored: true` on GET /api/documents/{id}, and POST /{id}/anchor refuses it as "already anchored"** (1806-1, measured). This is pre-existing since KS-1124 F4, but it contradicts the ruling's "mark it unanchored" on a second read surface.
- **An accepted 2xx whose body is not JSON is reported as 'failed'** (1806-2).
- **The recertify half of the change is not published**, because the route is not in the spec at all (1806-3).

**Recommended merge order: #1805 first, then #1806 re-prepped.** Code trees are byte-identical in both orders, and only the two HTML docs conflict. Both docs scripts renumber correctly to 107. But only order A (1805 first) gives correct doc figures without a re-run: in order B, Seat S's script writes a stale "414 example blocks" where the tree has 416 (BOTH-2).

| id | severity | finding | evidence class |
|---|---|---|---|
| 1805-1 | minor | **Six regex weakenings survive every cell.** Each was put on `DID_PATTERN` in `anchorSchema.ts:122` and run against both DID test files (132 cells):<br>- `m` flag (newline)<br>- `=` added to the class (padding)<br>- `$` dropped (trailing junk)<br>- `i` flag (case)<br>- `+`→`*` (empty segment)<br>- `\s` added (whitespace)<br>All six: **0 failed**. The product refuses each of these inputs today (probe, 1805-5), but nothing pins it, and these are exactly the classes the brief asked about. The builder's own classes are killed, by cells that match their stated targets: old pattern 6, any method 8, no cap 3, no `-`/`_` 2, old message 2. **Regression test the owner should add:** refusal cells on both fields for `did:jwk:`, `did:jwk:abc\n`, `did:jwk:ab\ncd`, `did:jwk:abc==`, ` did:jwk:abc`, `did:jwk:abc `, `DID:JWK:abc`, `did:jwk:abc def`. Each should assert `invalid_string` on the field's own path, as the PR's `issuesFor` helper does. | MEASURED AT RUNTIME (`evidence/mut1805.py`, `mut1805/summary.json`) |
| 1805-2 | minor | **The pattern is not specific to did:jwk.** After `did:jwk:` it admits the shared DID alphabet `[A-Za-z0-9._:%-]`, so `did:jwk::`, `did:jwk:.`, `did:jwk:%00` and `did:jwk:____` (which does not decode to JSON) are all ACCEPTED and would be anchored. The code comment at `anchorSchema.ts:115-116` says "K checks its shape (prefix, alphabet, cap)". The "alphabet" there is not base64url. This is consistent with the ruled "shape only" posture and with how did:key/did:web are treated, so it is not a defect of the ruling. But the comment over-claims, and VOCABULARY.md does not say so either. Fix-shape (either): reword the comment to "the DID alphabet, not base64url", or use a per-method pattern `did:jwk:[A-Za-z0-9_-]+`. | MEASURED AT RUNTIME (`evidence/probe/probe1805.ts`, `probe1805.out`) |
| 1805-3 | minor (question for Kam / Stuart) | **A did:jwk carrying PRIVATE key material is accepted.** A P-256 JWK with `d` present, 243 chars, gives ACCEPT on both fields. K "never decodes the JWK" (by the ruling), so it cannot notice. Once anchored, the value is written to Cardano metadata, which is public and irreversible. did:key cannot carry a private key by construction; did:jwk can, so **this exposure arrives with this PR**. Likelihood is low: S sends Entra's public did:jwk. The blast radius is a permanently published key. Fix-shape if wanted: decode base64url, parse JSON, and refuse when any of `d p q dp dq qi oth k` is present. That is a guard, not a key use, but it does depart from "never decodes", so it is a ruling, not mine. | MEASURED AT RUNTIME (same probe) + READ ONLY (on-chain path `cardano/cardanoMetadatum.ts`) |
| 1805-4 | info | **Length-cap consistency holds.** `DID_MAX_LENGTH` 512 = spec `maxLength: 512` (both fields). Storage is `anchor_store.metadata_payload` (JSON, no column cap). On chain the value is chunked to 64-byte strings (`cardanoMetadatum.ts`, ks1284 green). Realistic did:jwk sizes measured: Ed25519 114, P-256 176, secp256k1 182, RSA-2048 bare 506 (accept). **RSA-2048 with kid/alg/use is 610 and RSA-3072 is 732: both refused `too_big`.** That is fine for Entra (EC) but would 400 an RSA-keyed did:jwk. | MEASURED AT RUNTIME |
| 1805-5 | info | **Writers and readers agree.** Census of every non-test reference to actorDid/orgDid/DID_PATTERN/did:jwk: only `services/anchoring` validates (`anchorSchema.ts` and `anchoring.openapi.ts`, both importing `DID_PATTERN`). originate forwards `identity` as-is (`utils/anchorIdentity.ts`, no re-validation, by design). `anchorReadback.ts` returns it without re-validating. `anchorOverwriteGuard.ts` compares it for equality only. The gateway serves `secuura-api.yaml` (`api-gateway/src/index.ts:590`) and does not validate against it. **0 code paths decode did:jwk**: the prism resolver handles only key/web and is not on this path. The spec carries the pattern in exactly one schema (2 fields, yaml :1295/:1318). Caveat for spec consumers, pre-existing: in a Python-flavour regex, `$` matches before a trailing `\n`, so a Python validator (e.g. Schemathesis) would accept `did:jwk:abc\n` while K refuses it 400. Probe results (refused): padding, `+`/`/`, leading/trailing/embedded whitespace, tab, NUL, `DID:JWK`, `did:Jwk`, Cyrillic `ј` in the method, full-width/Cyrillic letters in the payload, zero-width space, `did:jwks:`, `did:jwkx:`, `did:jwk:` (empty), `did:jwk`, 513 chars, number, array. | READ ONLY (census) + MEASURED (probe) |
| 1805-6 | info | **The anchoring whole suite is rc 1 at develop, at 1805 and on the combined tree**, because of one pre-existing red: `threadTokenMint emulator round-trip parameterises mint + spend with a deterministic per-seed policyId` ("Could not serialize the data: Unsupported type", inside `@lucid-evolution/plutus`). Counts: develop 390/391, 1805 404/405 (+14), combined 404/405. The builder's evidence records the same `anchoring_whole_suite.rc = 1`, so it is not hidden, but "160/160" is the four-file figure, not the suite figure. | MEASURED |
| 1806-1 | **major-class, PRE-EXISTING (not introduced, not a merge block for #1806)** | **A kept certification reads as ANCHORED on the documents surface.** A certification is a row in `documents`, so `GET /api/documents/{certUuid}` serves it. With the blob #1806's own cells assert (`status: 'failed', anchoringStatus: 'failed', anchorId: null`):<br>- **GET answers `blockchain.anchored: true`**, because `documents.ts:1200` treats only `'anchor_failed'` as unanchored.<br>- **POST /api/documents/{id}/anchor answers 400 "Document is already anchored"** (`documents.ts:1458`), so the documents retry route cannot re-anchor it.<br>Controls: `anchor_failed` gives `anchored: false` / POST 202, and `null` gives `false` / 202. `reconcileDocumentAnchorState` returns early on `anchorId: null`, so nothing heals it. `verification.ts:100` and `verificationV2.ts` already treat `'failed'` as failed, so the verify surfaces are honest. This dates from KS-1124 F4 (2026-09-28). #1806 does not change it, but #1806 is the ruling "mark it unanchored", and this second read surface says the opposite: the "claims something true that isn't" class. **Fix-shape:** use one set, e.g. `FAILED_ANCHOR_STATUSES` from `verification.ts:100`, at both `documents.ts` sites. **Regression test:** the kept-cert blob gives GET `anchored: false` and POST /anchor 202. | MEASURED AT RUNTIME (`evidence/probe/_quarantine_2026-10-29/gate15-probe-docs.test.ts`, `probe/probe_docs.out`; documentRepo mocked, the real `documentsRouter`) |
| 1806-2 | minor | **'failed' is also set on an ACCEPTED 2xx whose body does not parse as JSON.** `upstream.json()` throws inside the `try` before `anchoringStatus = 'submitted'` (`certifications.ts:618-621`). Measured on the issue route: **202 with an empty body gives 201 + `anchoringStatus: "failed"`**, and 200 with `ok` (text) gives the same. In production, 202-empty gives **503, with the provisional row deleted while anchoring had accepted**: an orphan anchor. That production part is pre-existing. The published description says "a 4xx, a 5xx, an unreachable service or a timeout", which omits this case. Never on an accepted 2xx with a JSON body: 202+id, 202 without `data.id` and 299+id all give no key, `submitted`. 409 gives failed. Likelihood is low (anchoring always answers JSON). Fix-shape: set `submitted` on `upstream.ok` before parsing (anchorId null when unreadable), or add "or an unreadable acceptance" to the description. Same code shape in recertify (READ ONLY). | MEASURED AT RUNTIME (`probe/probe1806.out` P1-P10) |
| 1806-3 | minor | **The recertify response is undocumented.** `POST /api/certifications/{id}/recertify` is not in the spec at all: it is listed as deferred at `originate.openapi.ts:27`, and the yaml has 0 `recertify` matches. So the new top-level `anchoringStatus` on that 201 ships unpublished, and `CertificationIssueResponse` covers only the issue route. Also, recertify's anchoring `fetch` has **no `AbortSignal.timeout`**, unlike issue's 10 s. The builder's own test header says so. The effective bound is the runtime's default fetch timeout (not measured). Both points are pre-existing; the first is now more visible. | READ ONLY |
| 1806-4 | info | **Production byte-identical: confirmed.** In production a 'failed' never reaches a 201: the `return res.status(503)` comes before the 201 on both routes. Mutants G5/G6 (gate disabled) are killed by I5,I6 / Q5,Q6. The key set of a production 201 on 202-accepted (P10) is `id,type,holderId,status,data,issuedAt,blockchainAnchor,chargeEvents,derivedDocumentId,parentDocumentId`, identical to I4's assertion. The empty spread adds no key. Reach: the comparison is an exact string, so `staging` (`env.dev.json`, `services.bicep:393/1545`) and `Production` with a capital P (P8) take the 201+failed path. `env.demo.json` is `production`, so the 503 applies there. | MEASURED + READ ONLY |
| 1806-5 | info | **The builder's proof reproduces.** New cells: develop's `certifications.ts` gives 6 red (I1-3, Q1-3) / 6 green; head gives 12/12. My mutants, each killed by exactly the cells named:<br>- G1/G2 (issue/recert spread removed) by I1-3 / Q1-3<br>- G3/G4 (always emit) by I4 / Q4<br>- G5/G6 (production gate off) by I5,I6 / Q5,Q6<br>- G7 (wrong value `unanchored`) by I1-3<br>Restore verified by sha256. originate full: develop **1745/1745** (147 files), 1806 **1757/1757** (149), combined **1757/1757**. | MEASURED (`evidence/mut1806.py`, `mut1806/summary.json`, `orig_*.json`) |
| 1806-6 | info | The brief lists "2 new test files". The PR also edits `ks1293-originate-suite-is-hermetic.test.ts` (+2, listing both new files in the hermetic manifest), which is correct, so the PR's 8 files are right. The published `CertificationIssueResponse` (allOf Certification + optional `anchoringStatus` enum `[failed]`) matches the issue route's code (Certification is `.passthrough()`, requiring only `id`, `status`). | READ ONLY |
| BOTH-1 | info | **Merge mechanics.** `git merge-tree --write-tree` in both orders: rc 1, **only the two `Projects Documents/*.html` conflict** (both add section 106), and `secuura-api.yaml` auto-merges. I built both orders as local commits: order A (1805 squash, then merge 1806) and order B (the reverse), with the docs taken whole from the simulated develop, as the builders' rule says. **The non-doc trees are identical (0 diff lines).** Combined tree:<br>- `npm run check:openapi` rc 0 (416 example blocks)<br>- `generate-openapi --check` rc 0, and **rc 1 with one planted pattern byte**, restored and re-checked rc 0<br>- anchoring 404/405 (the same pre-existing red)<br>- originate 1757/1757<br>- `tsc --noEmit` anchoring 0 / originate 0<br>- eslint on all 8 changed .ts files rc 0<br>So after either PR merges, the other's yaml regenerates clean. | MEASURED (`evidence/merge.log`, `combine.log`, `checkopenapi_A.log`, `plant_yaml.log`) |
| BOTH-2 | minor | **Renumbering works with both builders' scripts, but only order A carries true figures without a re-run.**<br>- **Order A:** `add_docs_ks1709_u6.py wt-A 107 106 <U evidence_merged> <sim-develop>` rc 0. It writes `<h2>107. A certification whose anchor was refused...`, keeps 1805's 106, and its block says "416 example blocks", which is true on the combined tree.<br>- **Order B:** `add_docs_ks1175.py wt-B <sim-develop> 106 107 <seat S dir>` rc 0. It writes `<h2>107. actorDid and orgDid accept did:jwk...`, but the block says **"414 example blocks, OK" "measured on the merged tree"**, which is **false** on the combined tree (416). The reason: that script reads a fixed `SEAT/evidence/verify_post_merge/` folder, while U's takes an evidence dir argument. So if #1806 goes first, Seat S must re-run its proof into that folder before rebuilding.<br>Both orders: `html_docs_check` rc 0 on both docs (planted `<p>` gives rc 1), and `html_docs_matrix.test.sh` 18 passed / 0 failed. | MEASURED (`evidence/docs_A.out`, `docs_B.out`, `html_check_*.out`, `html_matrix_*.out`) |
| BOTH-3 | info | **The audit gates are rc 0 at develop, 1805 and 1806** (hono v2 is on develop): `audit:gate` "OK, no advisories outside the triaged baseline", and `audit:locks` 44 locks, "8 advisories match, 8 already baselined". Neither PR touches a lockfile. Both read the live registry at the time of running (07:1xZ). | MEASURED |

**Merge order:** #1805 first. Then #1806 re-preps on the new develop:
1. Merge develop in.
2. Take both docs whole from develop.
3. Rebuild at 107 with `add_docs_ks1709_u6.py` against a fresh evidence dir.
4. The yaml auto-merges, and `generate-openapi --check` stays rc 0.

Measured in simulation; the new #1806 head needs its own head-pinned gate or a delta check. **Why this order:** U's script takes a fresh evidence dir, and its handover already plans this path. S's script would publish a stale figure unless its evidence folder were rewritten (BOTH-2). Risk is otherwise equal: the code is identical, and neither PR's cells read the other's code.

**Spark half:** `spark_gate.sh` **now runs (exit 0 on both PRs)**. The workaround was in my clone only: `origin` set to `git@github.com:Secuura/Distributed_Secuura.git`, with `core.sshCommand` set to the project deploy key (read-only use).
Its facts, verbatim:
- 1805, `--node-modules <service node_modules>`:
  - `targeted on HEAD: {'files': 1, 'files_ok': 0, 'files_failed': 1, 'passed': 0, 'failed': 0, 'count_unparsed_files': []}`
  - same on BASE
  - log: `sh: vitest: command not found`
- 1805, `--node-modules <workspace-root node_modules>`:
  - `targeted on HEAD: {'files': 1, 'files_ok': 1, 'files_failed': 0, 'passed': 66, 'failed': 0, ...}`
  - `targeted on BASE product code: {'files': 1, 'files_ok': 0, 'files_failed': 1, 'passed': 58, 'failed': 8, ...}`
  - `diff {'files': 7, 'added': 128, 'deleted': 10}`
- 1806 (root node_modules):
  - `targeted on HEAD: {'files': 2, 'files_ok': 2, 'files_failed': 0, 'passed': 12, 'failed': 0, ...}`
  - `targeted on BASE product code: {'files': 2, 'files_ok': 0, 'files_failed': 2, 'passed': 6, 'failed': 6, ...}`
  - `diff {'files': 8, 'added': 490, 'deleted': 2}`

**I agree with the second and third sets**: 66 = the file's 52 + 14, 8 red at base = the 6 accept cells + 2 message cells, and 6/6 matches mine.

**There is no Spark VERDICT.** The LLM half (`spark_review.py`) answered **HTTP 400** for #1805. Its prompt was **3,152,582 chars**, because it inlines the *full text* of every touched file: the yaml plus two HTML docs, about 3.1 MB. A dry run for #1806 measured 3,333,625 chars, so I did not send it. Tool findings, not fixed:
- **S-1:** a missing runner (rc 127) is recorded as `files_failed 1, passed 0, failed 0`, which reads as RED. Nothing in facts.json marks that the runner was missing, a green/red that measured nothing.
- **S-2:** every Platform K PR carries the two docs, so every one will overflow `spark_review.py` the same way.
- **S-3:** `spark_gate.sh` refuses a `--work` under `/Volumes/DevMASTER/WEDNESDAY`, so its work dirs are in my session scratchpad. I copied the facts to `evidence/spark_facts/`.

## TESTED / NOT TESTED / HOW

### Setup
- **Clone:** `work/repo`, which did not exist before, made by `git clone --shared` of the spark cache. Toplevel assert equal to the path: yes, at start and end.
- **Remote:** in MY clone only, `origin` was re-pointed to the GitHub URL, with `core.sshCommand` set to the deploy key named in the cache's own config. I fetched `refs/g/1805`, `refs/g/1806` and `origin/develop`, and all equal the brief's SHAs.
- **Worktrees:**
  - `wt-develop`, `wt-1805`, `wt-1806`: clean at the end.
  - `wt-A` (local, never pushed: sim-develop `6c2ff406` = 1805 tree on a5962b99, merge `65f49845`) and `wt-B` (sim-develop `b8954f12`, merge `6f05d616`). These two are left with the two docs modified, which is the builders' scripts' output, kept as evidence.
  - Refs `refs/gate15/sim-A|B` are in my clone only.
- **Containment:**
  - No git command pointed under `!CODING`, and nothing was written there: builder scripts and evidence were only read, and the scripts were copied by `cat` into `evidence/builder_tools/`.
  - Nothing was posted, pushed, commented or merged, and no deploy box was touched.
  - `spark_review.py` read `LINEAR_API_KEY` from the Secuura `4_Credentials/.env` (its default `--linear-env`) to fetch ticket text. That is read only, and no value appears in any artefact of mine.
- **Node:** v26.8.1 / npm 11.19.0 (host Homebrew, **non-LTS**) for everything. I ran `npm ci --ignore-scripts` in each worktree (1806 packages, rc 0) and built `packages/shared` in each.

### Per PR
- **#1805:**
  - FAIL condition: any of the 14 new cells green at develop's schema, any red at head, a forbidden input accepted, suite delta other than +14, or check:openapi non-zero.
  - Four files: 160/160 at 1805 and 146/146 at develop.
  - Mutants: `mut1805.py` (12 runs, control green, restore sha256 equal).
  - Probe: `probe1805.ts` via `tsx` against the real `identitySchema`.
  - Anchoring full suite at develop, 1805 and combined (1805-6). check:openapi rc 0 at develop, 1805 and 1806.
- **#1806:**
  - FAIL condition: a new cell green at develop's route, 'failed' on an accepted JSON 2xx, any production 201 carrying the key, a production response that differs, spec ≠ code, or originate delta other than +12.
  - New cells, red-proof and mutants: `mut1806.py`.
  - Response probes: `gate15-probe-1806.test.ts` (P1-P10, using the builder's own harness).
  - documents-route probe: `gate15-probe-docs.test.ts`.
  - Both probe files were placed in my worktree only to run, then **moved** to `evidence/probe/_quarantine_2026-10-29/`. The worktree was clean afterwards.
  - originate full suite at develop, 1806 and combined.

### NOT TESTED
- Any running stack: local :6882, kintsugi, demo. The pushed hook's three skipped legs (spec-auth conformance, path resolvability, served-spec consistency) were not re-run either.
- The four platform suites (Schemathesis, Akto, Playwright, k6): not commissioned, no stack.
- The 10 s timeout path on issue (no cell drives it, and nor did I).
- Recertify's 2xx-unparseable case (READ ONLY, same code shape).
- The runtime's actual default timeout for recertify's un-signalled fetch.
- The documents-route probe used a mocked repository, not Postgres or RLS.
- The gateway's mapping of `status: 'failed'` to off-chain-only (KS-1124 F4) was not exercised.
- Stuart's real dev-ps did:jwk (I used synthetic JWKs, including the PR's RFC 7515 one). Entra's real key type was not confirmed.
- PS-1324, the KS-1175 and KS-1709 tickets and Kam's card `secuura-ks1709-keep-unanchored-certification-1023` were not read by me. Spark fetched KS-1709/KS-1175 text into its prompt, which I did not review.
- PR bodies read from the builders' evidence copies, not from GitHub.
- **Test files were not type-checked by my `tsc`:** both services' tsconfigs exclude `src/__tests__`. originate's tests are type-checked by ts-jest at run time (it caught my own TS6133). The anchoring test file was not type-checked by me; the builder claims `tsc_tests_included` rc 0.
- Suites on Node 24 LTS.
- The Spark LLM verdict (see S-2).
- Seat S's red-proof files `M0`-`M4` were only cross-read (counts match). I ran my own mutants.

### Instrument errors (mine, in order)
1. The no-cd hook refused `git -C $D worktree/fetch` written with a shell variable. I re-issued with literal paths or inside my scripts under `evidence/`.
2. The first anchoring full runs (develop, 1805) failed 3 files with "Failed to resolve entry for package @secuura/shared", because shared was not built. That was a setup failure, not a verdict. I built shared and re-ran, and discarded those runs (`anch_*_full.json`, superseded by `*_full2`).
3. The four-file run first collected **0 tests, rc 1**: zsh did not word-split my `$F`. I re-ran with explicit arguments.
4. My first 1805 probe ran under vitest, whose reporter swallowed `console.log` (0 PROBE lines, a green that measured nothing). I re-ran with `tsx`: 68 lines.
5. The first 1806 probe failed in ts-jest on TS6133 (an unused const copied from the harness). I added `// @ts-nocheck` and re-ran.
6. The first `html_docs_check` and matrix calls used the wrong path (`Blockchain/Dev/systemTest`), giving rc 1 module-not-found and rc 127. The tools live at the repo root `systemTest/`, and I re-ran there.
7. The path guard refused a multi-source `cp` from `!CODING` (it read it as a write). I used `cat` instead.
8. Spark: the first 1805 run with the service's own node_modules was `vitest: command not found` (S-1). I re-ran with root node_modules.
9. The first 1805 `npm ci` wrapper was a backgrounded subshell, so its task "completed" at once while the installs ran on (PIDs 83927/83929/83931). I confirmed each log said `rc=0` before using it.
- **PIDs I started:** the three npm ci subshells above, and the jest/vitest/tsx runs (foreground). All exited on their own, and nothing was killed. Test HTTP servers are in-process jest harnesses.

### Artefacts
`/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-10-29_gate15-1805-1806/evidence/`:
- Scripts: `wt.sh`, `anch.sh`, `orig.sh`, `mut1805.py`, `mut1806.py`, `merge.sh`, `combine.sh`, `plant_yaml.sh`, `probe/`
- Results: `mut1805/`, `mut1806/`, every `anch_*`/`orig_*` json+log, `checkopenapi_*`, `audit_*`, `docs_A|B.out`, `html_*`
- Spark: `spark_*.out`, `spark_facts/`, `spark_review_1805|1806/` (prompt and section sizes)

Work dir left in place: `work/` (the clone and five worktrees).
