# Gate verdict: Secuura Platform K PR #1531 (KS-1557 read side), Opus tier 1

**VERDICT: GO WITH NOTE. 0 Major, 3 Minor (m1, m2, m3), 9 observations.**
Report sha256/16: `64b8bfc92d36e2b6`. Recipe: `sha256` of this file with the 16 hex characters on this line replaced by `0000000000000000`, first 16 hex characters.

**Summary.** The read side does what the brief says it closes. I built every forgery shape I could through the unchanged develop write route, plus hand-planted rows for the shapes no route writes. On develop, verify presents forged evidence in 13 of them. On the head it presents none, in both tenancy modes, as `secuura_app`, and the result is the same across runs.

What still verifies CERTIFIED on the head is exactly what the PR body names as not closed:
- a parent that belongs to someone else (F11, F13);
- the same hash registered by two organisations, KS-1561 (F16, F17);
- the legacy-certify path, which is PR 1525's surface (F18);
- connector-to-connector citation, which is only reachable through the 32-bit suffix residual (P03).

The Minors are a merge-message hazard, a behaviour change that the body frames too narrowly, and the lookup cap's value, which no cell pins.

## Head under test
- **Code under test.**
  - Head `1ffc0d7a4ad740a91f2c04122fb55cd44477c928`, fetched by SSH from `refs/pull/1531/head` into a `git clone --shared` in my scratchpad.
  - Tree `c190292a793858fcf5baa7150740fc25c51fb687`, which equals the author's claimed landing tree. Instrument: `git rev-parse <head>^{tree}`.
  - It has one parent, develop `b28bfaecf24e4671440b9345289bfc368639bd11`, which equals the brief.
  - `git merge-tree --write-tree develop head` returns `c190292a7938…` with rc 0, the head's own tree. That follows trivially, because develop is the head's parent.
- **Diff.** `git diff --stat develop head` touches exactly six files, +778/-58:
  - `verification.ts` (the resolver lives here) and `verificationV2.ts`;
  - two new test files;
  - the two rewritten ks584 tests.
- **Database.** My own PG 15.14 on 127.0.0.1:55427, unix socket off.
  - Built with `initdb -U secuura --auth=trust`, then `docker/init/*` in order.
  - The `00-create-platform-db.sql` dblink step failed (role lookup), so I created `secuura_platform` by hand.
  - `run-migrations.sh` reported **applied=50 failed=0** (`evidence/migrations.txt`).
  - `documents` has `relrowsecurity=t` and `relforcerowsecurity=t`. `secuura_app` has `rolsuper=f` and `rolbypassrls=f`.
  - The cluster `timezone` is UTC. `packages/shared` was rebuilt and Prisma generated in both trees.
- **Pool mode.** It needs `platform_document_registry` FK'd to the same `tenants` table that the tests write. So `docker/init-platform/01-platform-schema.sql` was applied to the app DB and `PLATFORM_DATABASE_URL` pointed at it.
  - My first attempt used a separate platform DB. There the author's x-tenant cell went red in T mode with an FK violation. That red came from my setup, not the product, and it is disclosed under Self-correction.
- **Cleanup.** Postgres was stopped (`pg_ctl stop`, port closed). The app password was scanned for in the evidence folder: 0 hits.
- **Writes.** Nothing was written to the project. There were no pushes and no GitHub or Linear writes, and I contacted no remote box. Linear was read once, read-only, with the key sourced inside a script.

## Numbers (instrument and control)
| # | What | Head | Develop | Instrument | Control |
|---|---|---|---|---|---|
| 1 | Author's integration `ks1557-verify-trusts` | **17/17 in F mode, 17/17 in T mode, 3 of 3 runs each** | **14 red in F, 15 red in T, 3 of 3 runs** (head's test file copied into develop) | jest integration config, app role (`int_{head,dev}_{F,T}_{1..3}.txt`) | The SETUP cell asserts `secuura_app`, `su=f`, `bp=f` and tenant manager equal to the mode. On develop, only SETUP and the genuine control stay green (plus the x-tenant cell in F, where it is trivially green). So every RED-named cell goes red at develop in at least one mode, which supersedes the author's "4 of 17 never seen red". |
| 2 | Unit, the three suites | **3 suites / 64 tests** | ks584 rewrites 31/31 green on develop. The ks1557 unit suite cannot load there (the function is absent). | `npx jest` | Both ks584 rewrites pass on develop too, so they are regression fixtures, not pins of the new rule (see O7). |
| 3 | Whole originate unit suite | **103 suites / 1248 tests** | — | `npx jest` | — |
| 4 | tsc `--noEmit` (originate; it excludes tests) | rc 0 | — | `tsc_head.txt` | A planted `TS6133` returned rc 2 (`tsc_planted_control.txt`). Test files are type-checked by ts-jest: my harness's unused const failed to compile, so they cannot pass with type errors. |
| 5 | eslint on the six files | rc 0 | — | `eslint_head.txt` | A planted error returned rc 1 (`eslint_planted_control.txt`). |
| 6 | `check:openapi` | rc 0, "413 example blocks", OK | — | `check_openapi_head.txt` | A planted description change in `originate.openapi.ts` returned rc 1 "CHECK FAIL" (`check_openapi_planted_control.txt`). |
| 7 | Gate harness (forgery, tenancy, legit shapes) | 5/5 cells ran in each mode, 2 runs each. A diff of head run 1 against head run 2 on legit shapes: **0 differences** | 5/5 cells ran | `gate1531.integration.test.ts.txt`, `gate_*.json` | The differ catches 65 differences between develop and head, so it bites. |

## Forgery table (item 2): verify(victim hash), v1 `isCertified` / v2 matches carrying certification
Shapes F01 to F18 go through the real develop write route `POST /api/certifications/issue`, which is unchanged. Attacker A and victim B are different organisations in one tenant. Shapes P01 to P05 are planted by superuser SQL, because no route writes them. Each result held in both modes, and for the head across 2 runs (`gate_{head,dev}_{F,T}_*.json`, summarised by `ftable.py.txt`).

| Shape | Develop | Head |
|---|---|---|
| F01 own parent, victim hash, overrides `certificationId`/`certifiedAt`/`issuerName`/`issuerId`/`organizationId`/`certificationType` | **TRUE**: id `FORGED-CERT-ID`, at 2020-01-01, by "Org B Official Registrar", org = ORG_B, type FORGED | false, v2 0 |
| F02 `certificationId: null` | false (falsy) | false |
| F03 `certificationId: ''` | false (falsy) | false |
| F04 `certificationId: 'api-key'` | **TRUE**, id `api-key` | false |
| F05 another organisation's REAL certification id, same tenant | **TRUE**, B's id | false |
| F06 a certification id from ANOTHER tenant | **TRUE**, T2's id | false |
| F07 caller's own real certification for a DIFFERENT document | **TRUE** | false |
| F08 cites a document the caller legacy-certified | **TRUE** | false |
| F09 derived hash differs from parent (own parent, victim hash, no overrides) | **TRUE** (real id) | false |
| F10 no parent link (the route writes no derived row) | false | false |
| F11 **parent is the victim's document**, victim hash, `issuerName` chosen | TRUE | **TRUE**: the caller's real id, time and type, `certifiedBy` = caller string. NAMED NOT CLOSED in the body. |
| F12 victim parent plus an overridden `certificationId` | **TRUE** (forged id, 2020, ORG_B) | false |
| F13 victim parent plus overridden time, type and `issuerId` | **TRUE** with forged time, type and org | TRUE with the real time and type and a null org (same named path as F11) |
| F14 caller in T2 names T's document as parent | false | false |
| F15 `data.parentDocumentId` override (the column stays the real parent) | **TRUE** | false |
| F16 Probe B: A registers the same hash and lineage-certifies its own copy | TRUE | TRUE (KS-1561, not closed) |
| F17 Probe B, legacy path | TRUE | TRUE (KS-1561) |
| F18 A legacy-certifies B's document | TRUE | TRUE (PR 1525 surface, `certifications.ts` untouched) |
| P01 planted, no parent link, otherwise genuine | **TRUE** (2020, Planted Registrar) | false |
| P02 planted, parent hash differs | **TRUE** | false |
| P03 planted, a connector's NULL-owner row cites ANOTHER connector's certification (suffix matched by hand) | TRUE | **TRUE**: rule 5 is vacuous for connectors (NULL == NULL). Reachable only through the 32-bit suffix residual, which is named. |
| P04 same as P03 with a non-matching suffix | **TRUE** | false |
| P05 the cited certification row is REVOKED | TRUE | TRUE (disclosed: "revoked certifications are not examined") |

**Tenancy (item 3)** (`X*` keys in the JSONs).
- X1. The same certification id cannot exist in two tenants: the second insert fails with `documents_pkey`. The id is a global primary key.
- X2. An outsider in T2 verifies through the registry in pool mode.
  - On the head, the genuine certification counts (correct id) and the forged one does not. On develop the forged one presents as `FORGED`.
  - In single-tenant mode nothing is found on either tree.
- X3. A same-hash set spanning T and T2, verified as T2. v1 selects T2's local row (no certification) on both trees. v2 lists the T certification on both, so there is no change.
- X4. A T2-hosted derived row cites T's genuine certification (suffix matched). On develop it counts as T2 (v1) and as T and T2 (v2). On the head it counts nowhere, which shows the lookup is bound to the row's own tenant.
- X5. RLS on the exact lookup statement, run as `secuura_app`:
  - no GUC: **0 rows**;
  - correct GUC: 1 row;
  - wrong-tenant GUC: 0 rows.

## Writers (item 4), re-derived (`static_writers.md`, file:line per row)
- **Parent belonging to someone else.** This is the only deterministic writer that makes a forged row satisfy all five conditions: the certify derived row with `parentDocumentId` set to another document in the same tenant.
  - The parent resolves by `external_id` in the tenant with no access check (`documentRepo.ts:446,472`).
  - The hash is the caller's `data.contentHash` (`certifications.ts:532`).
  - Reproduced as F11. Named not closed.
- **The 32-bit residual.** `/version`+`/sign`, `/sign-cert` and `/sign-wallet` meet C1 and C2. They write a server-random 8-hex suffix, and the owner is the source's owner.
- **Nothing else can forge.**
  - `POST /api/documents` accepts a caller external id only as a UUID v4, which can never match `doc-\d+-hex`, and writes no parent.
  - `holderId` is written only by `saveCertification`.
  - GDPR, the admin backfill and transfer-custody can only remove evidence.

## Cost (item 5): `log_statement=all`, a separate `gatemark` client brackets each request, statements counted in between (`cost_*.counts.txt`, `qcount.py.txt`)
| Request shape | Develop F/T | Head F/T | Added | Lookups (head) |
|---|---|---|---|---|
| v1, plain hash (zero control) | 20 / 20 | 20 / 20 | **0** | 0 |
| v1, one genuine derived row | 24 / 24 | 28 / 28 | +4 | 1 |
| v1, nine claimed rows | 56 / 56 | 88 / 88 | **+32** | **8** |
| v1, thirty claimed rows | 140 / 140 | 172 / 172 | +32 | **8** (the cap holds) |
| v2, nine claimed rows | 4 / 9 | 36 / 41 | +32 | 8 |
| v2, thirty claimed rows | 4 / 9 | 36 / 41 | +32 | 8 |
| v2 by derived documentId (parent not in the set) | 4 / 4 | 12 / 12 | +8 | **2** (parent fetch + certification) |
| nine claimed rows whose parent is outside the set, v1 | 24 / 24 | 56 / 56 | +32 | 8 parent fetches |
| v1/v2 as a T2 outsider, nine rows (registry path) | 4/4 (F), 9/9 (T) | 4/4 (F), 41/41 (T) | +32 in T | 8 |

- The author's 20→20, 24→28 and 56→88 reproduce exactly against the real base `b28bfaec`. The author measured against `5d5aea41`; `5d5aea41..b28bfaec` touches only two shell tests.
- Each logical lookup logs as four statements (BEGIN, `set_config`, SELECT, COMMIT).
- A request carries one `contentHash` or `documentId`. v1 and v2 have no batch verify (`/hash` and `/status` do no lookups), so a caller cannot multiply the cap across hashes.
- The body labels its timings scratch-local, and says "**Wall-clock on a real box is NOT measured**". Confirmed.
- I did not measure wall clock.

## Behaviour changes (item 6): full-response structural diff, develop vs head (`ldiff.py.txt`)
- **Identical, 0 differences in both modes:**
  - L1, genuine owner with the parent's hash: v1 hash, v2 hash, v2 by id and v1 by id;
  - L3, legacy-certified document;
  - L4, connector (S-style) genuine lineage certify with the parent's hash;
  - L5, an unknown hash;
  - L8, v1 verify-file of a genuine certification.
- **Changed:**
  - L6, holder erased (`{"anonymized":true}`): stops counting on v1 and v2. Named.
  - L7, custody transfer of the derived row: stops counting. Named in the body.
  - **L2, a genuine certify WITHOUT `data.contentHash`:** v2 by the derived row's hash and v2 by `derivedDocumentId` go from certified to not certified. See **m2**.
- **`certifierOrganizationId`.**
  - On develop the L1 derived evidence already carried `null`. It came from the caller's `data.issuerId`, which the server never writes, not from the certification row's user id. So **the brief's description of the old value is wrong**, and the PR body's description ("whatever the caller put in `data.issuerId`, or null") is right.
  - The legacy path (`verification.ts:146`) still emits the issuer's USER id under that name on both trees. That mislabel predates this PR.
  - Consumers (`static_consumers.txt`): the spec is `["string","null"]`, required (present); the frontend is `.nullable().optional()` with no reader; gateway, sdk and packages have 0 hits; Platform S documents have 0 hits.
  - Grep controls: `certificationId` gets 257 hits, while the British spelling and a nonsense token get 0.

## Mutants (item 7): `gmut.py.txt`
My runner loads only the author's mutant definitions and ignores the runner's dead constants. Each mutant must compile under tsc. I record every red cell name per layer, restore the files, and assert them byte-identical: `RESTORE OK 409083b94072b094 edc805ef398a64a5`. Raw results are in `mut_results.jsonl` and `mut_run1.log.txt`.
- **Comment-only control:** 0 red across 64+17+17 cells.
- **The author's seven: all killed.**
  - V01: unit 3 red.
  - V02: unit 2 red.
  - V03: unit 1 red, and only by "rows that fail the cheap checks do NOT consume the lookup cap" (see O3).
  - V04: unit 2 red; F and T 1 red each, by "only the external-id binding rejects this".
  - V09: unit 2 red; F and T by "cites a LEGACY-CERTIFIED document".
  - V10: unit 1 red ("cites ITSELF").
  - **W03: unit 0 red, integration 12 red in F and 12 in T.** Killed by the integration layers only, as the brief says.
- **Sampled 15 of the 24 the author did not re-run: all killed.**
  - V05: 13 / 5 / 6 red.
  - V06: 2 / 3 / 4 red.
  - V07, V08, V11, V17 and V18: unit only.
  - V13 and V14: unit and both integration modes.
  - V15: 2 / 5 / 5 red.
  - V16: unit, plus T 1 red.
  - **V22: T 1 red only.**
  - V25: unit + F + T.
  - **V26** (scored "unscorable" by the author): T 1 red, killed.
  - W02: F and T.
- **The gate's own ten.**
  - G1, parent-hash check removed, made compile-valid on the second try: unit 2 + F 3 + T 3 red, killed.
  - G2, certification lookup drops its tenant clause: unit 3 red (the bound-value cell), killed. With FORCE RLS the clause is belt-and-braces.
  - G3, parent fetch drops its tenant clause: unit 1 red, killed.
  - G4, resolves-to-nothing accepted: unit + F 2 + T 2, killed.
  - G5, time taken from the derived row's `created_at`: F 3 + T 3, killed.
  - **G6, cap raised from 8 to 1000: SURVIVED all 98 cells.** See **m3**.
  - G7, suffix binding replaced by any `doc-*`: unit 5 + F + T, killed.
  - G8, cross-tenant rows not tagged with `_tenantId`: T 1 red only, killed.
  - G9, `readForRow` ignores the row's tenant pool: unit + T, killed.
  - G10, owner binding treats NULL as a wildcard: unit 1 red (the connector cell), killed.

## Existing cells and unpinned guards (item 8)
- **The ks584 rewrites.**
  - The fixtures are now genuine-shaped: a parent in the set with the same hash, an external id carrying the certification prefix, a UUID certification id and a tenant id.
  - Their mock answers the certification lookup with one fixed certification row for ANY id and tenant. The parent fetch is not mocked separately; it returns the row set. Neither side has an owner or issuer, so rule 5 passes vacuously.
  - They pass on develop as well (31/31), so they pin nothing about the new rule. That is acceptable for KS-584 regression fixtures. The rule is pinned by the ks1557 suites, as the mutants show.
- **Guards no cell pins:**
  - the cap's numeric value (m3);
  - rule 3 for connectors, which is the only binding left once rule 5 is vacuous (P03 is TRUE on the head by design).
- **What the PR body says is not closed.** The body states under "Not closed here":
  - the 32-bit external-id prefix residual;
  - a parent that belongs to someone else;
  - KS-1561.

  The top of the body says KS-1557 and KS-1561 stay open. The PR does not claim to close either.

## Scope and hygiene (item 9)
- **Overlap.** `certifications.ts` and both PR 1525 test files are untouched (`static_overlap.txt`). The overlap scan covered all 1452 `refs/pull/*/head` fetched by SSH.
  - The six files overlap no OPEN PR; the only hits are merged PRs 1223, 1280 and 1500.
  - The planted control `certifications.ts` **fired on PR 1525**.
  - Open or merged state was taken from Linear's projection, because `gh` auth was unavailable (hosts.yml empty, rc 4).
- **Pre-push claims.** Re-read from the author's hook log (`push_1ffc0d7a_hook_output.log`): "PREFLIGHT INCOMPLETE — 13/16 legs ran, 3 SKIPPED. Nothing failed." Legs 3, 4 and 8 were skipped because the local stack was down. Shell suites ran 86/86. I did not re-run these; that would need a push.
- **Link kind.** Linear's live KS-1557 attachment for PR 1531 reads `linkKind: "contributes"`, status open (`static_linear.json`). The body check used the author's posted copy (`static_pr_body.md`, sha256/16 `9f4fd7b8860442b6`), because the live GitHub body could not be read (gh auth).
  - Scanning for a close-family word within 40 characters of a ticket key gives one hit: "`Refs KS-1557`. No close-family keyword …". The word FOLLOWS the key, so it is not a closing pattern.
  - The planted control "fixes KS-9999" fired.

## Findings
### m1 (Minor): the head's commit message carries the closing pattern the body was rewritten to remove
- **Where.** The final paragraph of commit `1ffc0d7a`'s message: "Refs KS-1557. This does NOT close KS-1557 (the write side is open) and does not close KS-1561."
- **Measurement.** It gives three close-keyword-then-key hits in my scanner (`static_closekw_commitmsg.txt`); the planted control fired.
- **Why it matters.** Linear parses magic words in commit messages as well as PR bodies. The author's own account says Linear already misread a negation sentence in the body as `closes`. A squash that reuses this message could close KS-1557 and KS-1561 on merge.
- **Trailer.** The message also carries `Co-Authored-By: Claude Opus 5`. The repo squashes with zero trailers (both develop commits I read have none).
- **Fix shape.** At merge, use a squash message with `Refs KS-1557`, no "close" next to a key, and no trailer. Then re-check the Linear `linkKind` after the merge.

### m2 (Minor): "Legitimate rows keep counting" is not true for a spec-conformant certify without `data.contentHash`
- **Shape (L2).**
  1. The owner registers document P.
  2. `POST /api/certifications/issue {type, parentDocumentId: P, data: {title}}`, with no `data.contentHash`. The published spec (`secuura-api.yaml` CertificationIssueRequest) never asks for one.
  3. The derived row's hash becomes `generateDocumentContentHash(data)`, which is not P's hash.
- **Measured (`gate_{dev,head}_{F,T}_1.json` LEGIT.L2).** v2 by the derived hash and v2 by `derivedDocumentId` return `isCertified: true` with the real certification id on develop. On the head they return `isCertified: false`, no certification. Both modes.
  - v1 by P's hash is false on both trees, so it is unchanged.
- **Assessment.** This is inherent to a read-side-only fix. Such a row is indistinguishable from the F09 forgery (own parent, foreign hash), so failing closed is the right default.
- **What the body says.** It mentions this only as "Historic derived rows … whose hash is not their parent's stop counting", next to "Legitimate rows keep counting".
  - It is not historic-only: every new genuine certification issued without `data.contentHash` is affected.
  - Platform S's certify payload shape is not confirmed in any document I could read. The KS-584 UAT fixture suggests S sends the parent's hash, so S may be unaffected.
- **Fix shape.** No code change. State it in the body or ticket as a client-visible change, and confirm S's payload on KS-1557. The write-side hash bind is the real fix.

### m3 (Minor): the lookup cap's VALUE is pinned by no cell
- **Measured.** Mutant G6, `MAX_EVIDENCE_LOOKUPS = 1000`, survives all 64 unit and 2 × 17 integration cells.
  - The cap cell (`ks1557-trusted-certification-evidence.test.ts:228-231`) asserts `toHaveLength(MAX_EVIDENCE_LOOKUPS)`, so it follows the constant.
  - The cap is real at the head: 8 lookups at both 9 and 30 claimed rows (`cost_head_{F,T}.counts.txt`).
- **Fix shape.** One assertion `expect(MAX_EVIDENCE_LOOKUPS).toBe(8)`, or a literal 8 in the cell.

### Observations (not findings)
- **O1. Lookups per row.** The cap limits EXAMINED rows to 8, but an examined row can cost two lookups: a parent fetch when the parent is outside the same-hash set, plus the certification lookup. Measured:
  - 2 lookups for v2 by `derivedDocumentId`;
  - 8 parent fetches when the parents are outside the set.

  By code, the worst case is 16 logical lookups (64 statements) when 8 same-hash rows have same-hash parents pushed out by `VERIFY_ROWSET_LIMIT` = 24. I did not construct that case. v1's registry path can also re-resolve one row after `crossTenantLookup` (≤1 extra). The body's "one lookup per examined row" holds for parents inside the set.
- **O2. The brief's description of the old field is wrong.** It said `certifierOrganizationId` "used to be the certification row's USER id" on derived evidence. Measured: develop presented the caller's `data.issuerId`, or `null`. The PR body describes it correctly.
- **O3. Parent-link check.** Rule 2's "parent link is set" duplicates the hash check: a null parent fails `fetchParentHash`'s UUID test. So V03 is caught only by the unit cell for cheap checks not consuming the cap. The integration cell "has NO parent link" passes under V03 because of the hash check.
- **O4. Single-cell dependence.** V22, V26 and G8 (the registry and pool path) are each killed by one cell only, the T-mode x-tenant cell. A cell that leans on its environment for that path deserves a second pin.
- **O5. The author's runner was edited after run 1.** The needles for V03 (F/T) and W03 (unit) were removed after run 1 (fork finding, `static_mutant_list.md`). My independent run matches the edited picture: W03 is integration-only and V03 is unit-only. V26 is killable (T mode), although the author marked it unscorable.
- **O6. Connector principals.** For connectors, rule 5 (owner equals issuer) adds nothing (P03). The body says so implicitly ("both NULL for a connector principal"). The only remaining binding is the 32-bit suffix.
- **O7. The ks584 rewrites pass on develop.** They are non-red fixtures (see item 8).
- **O8. Pool-mode environment.** The author's pool-mode integration needs the platform registry to share the app DB's `tenants` table. Otherwise registry inserts fail their FK silently (a logged warn) and the x-tenant cell reds. This is not documented in the test header.
- **O9.** Revoked certifications still count (P05). The body discloses this.

## Self-correction
- **Separate platform DB.** My first pool-mode runs used a separate platform DB with the platform schema. The author's x-tenant cell went red there, 1 of 17, because of an FK violation on `platform_document_registry`.
  - Cause: my environment, not the product. The cell's tenants live in the app DB.
  - I re-ran with the registry in the app DB: 17/17 green, 3 of 3. The red logs were overwritten by the re-runs. The FK warning text is quoted in O8.
- **G1 did not compile.** My first G1 replacement (`if (false) continue;`) failed tsc with rc 2, because of unused locals. A mutant that does not compile is discarded, not counted as a kill. I re-ran G1 in a compile-valid form and it was killed.
- **Runs that never reached the tests.**
  - The first integration run failed 17/17 because the Prisma client was not generated (`npm ci` uses ignore-scripts). That was an environment fault; I ran `npm run generate` in both trees.
  - The first harness run failed to compile on an unused const; I fixed it.

## NOT tested
- **pgbouncer, and a real gateway with JWT/JWKS.** UNMEASURED. All calls went straight to the routers, with the principal injected by a header shim (the same as the author's). pgbouncer is not installed and the Docker daemon is not used.
- **Wall-clock latency.** Not measured, on any box.
- **The 16-lookup worst case (O1).** Not constructed.
- **The live GitHub PR body.** Not read (gh auth unavailable). The posted copy and Linear's live `linkKind` stand in for it.
- **Pre-push hook.** Not re-run; that would need a push.
- **Schemathesis, Akto, Playwright, k6, deployed checks.** Not run.
- **Mutants.** Nine of the author's 24 other mutants were not sampled: V12, V19, V20, V21, V23, V24, V27, W01 and W04.
- **Erasure and custody transfer.** Not driven through the real routes. Their shapes were applied by SQL (L6, L7).
- **Postgres versions other than 15.**

## Evidence index (`evidence/`)
- Author's cells: `int_head_{F,T}_{1..3}.txt`, `int_dev_{F,T}_{1..3}.txt`.
- Unit: `unit3_head.txt`, `unit_all_head.txt`, `unit2_dev_own.txt`, `unit3_dev_headtests.txt`.
- Gate harness and its outputs: `gate1531.integration.test.ts.txt`; `gate_{head,dev}_{F,T}_*.{txt,json}`.
- Cost: `cost_{head,dev}_{F,T}.{txt,json,counts.txt}`.
- Mutants: `mut_results.jsonl`, `mut_run1.log.txt`, `gmut.py.txt`.
- Static: `static_*` (writers, consumers, overlap, PR body, close-keyword scans, Linear, author's runner and mutant list).
- Tools: `tsc_*`, `eslint_*`, `check_openapi_*`, `pg_setup.sh.txt`, `migrations.txt`, `runint.sh.txt`, `runcost.sh.txt`, `qcount.py.txt`, `ftable.py.txt`, `ldiff.py.txt`.
