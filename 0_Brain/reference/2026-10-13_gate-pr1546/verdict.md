# VERDICT: NO GO — PR 1546 (KS-1032) head ad366066e620037d753f9421bcd051ad09a9a7af · Major 1 / Minor 3 / Info 6
REPORT-HASH: sha256/16 34fb8ee6b4650ac6

Gate: independent OPUS QA gate, tier 1 (auth/tenant boundary), commissioned by Wednesday. Findings only; nothing fixed.
Head under test: **ad366066e620037d753f9421bcd051ad09a9a7af** (parent 405e33a1061310662b10245c5154c3d75c49f0f4, tree b371f9483256d83e07e73ad630a7de242b5149b3; all three asserted with `git rev-parse` after fetching `refs/pull/1546/head` in a `clone --shared` in the gate scratchpad).
Develop measured: **026c2d1614065c79fc8d96007ac0d80f19fb9363** (fetched `refs/heads/develop`, same clone). `gh pr view` (read-only) reports headRefOid = ad366066…, base develop, OPEN, MERGEABLE.

## Bottom line

The CODE does what Kam's ruling asks. With `GATEWAY_VOUCH_SECRET` unset, every forged identity/tenant header shape I tried is refused or ignored. That covers all 147 declared routes, compared bare against forged. On develop the same scan finds the hole. The NO GO is about the deploy condition, which the brief requires the body to state honestly. It does not. The body and `routes/metering.ts` both say Platform-S metering "answers **401**" on a box with no secret. Measured on the real app, Platform-S, called the way the gateway actually sends it, answers **200** and reads the **default tenant's** usage instead of its own. On an unset box the failure is a silent switch to the wrong tenant, not a refusal. A deploy check that only looks for "metering works" cannot detect a missing or mismatched secret. The fix is text: the body, one code comment, and how DEPLOY-BLOCKERS step (3) is checked. Do not recommend deploying in any case: this change deploys only after the secret is set (DEPLOY-BLOCKERS).

---

## MAJOR

### M1. The deploy condition names the wrong failure signature (body "⚠ Deploy condition"; `services/originate/src/routes/metering.ts:55-59`)
- **FOUND.** The body says: "Until the secret is set on a box: that box's Platform-S metering answers **401** … On a single-tenant deployment … the answers are unchanged." The comment at metering.ts:55-59 says the same. DEPLOY-BLOCKERS step (3) relies on it ("the refusal would otherwise cut them … Seat J 8th's inference, not measured").
- **What the code does.** For an `sk_` key, api-gateway's `authenticateToken` (`services/api-gateway/src/middleware/auth.ts:419-427`) attaches BOTH a connector Bearer JWT, minted by auth `/internal/connector-token` with the key's `tenantId` claim, AND the trust headers. On an unset box originate strips the headers, so the shim does not fire. `authenticate()` then accepts the Bearer and sets `req.user` (role connector). The handler scopes by `req.tenantId`, not `req.user.tenantId` (`metering.ts:72-74,108`). `req.tenantId` was set by the KS-458 block to `DEFAULT_TENANT_ID` because the header is gone. Result: **200, default tenant's usage**.
- **TESTED / HOW** (instrument: jest on the real `index.ts`, the listen spy as in the author's harness, `getUsageSummary` mocked to record its tenant argument, `verifyJwtRs256` mocked to accept a named connector token carrying tenant T_CONN):
  - GA1, unset: Platform-S shape (Bearer + `x-user-role: connector` + `x-tenant-id: T_CONN`, no vouch) gave **200, tenantArg = a0000000-…-000000000001 (DEFAULT)**. On develop the same cell gave 200 with tenantArg = T_CONN (the cell is red on develop, `evidence/gateA_wt_dev.json`).
  - GA2, unset: the same request without the Bearer (the gateway's token exchange failed) gave **401** and the handler never ran. **This is the only shape that matches the body's "401".**
  - GC5, secret SET but the vouch WRONG, with the Bearer: 200 on DEFAULT. A mismatched secret looks exactly like an unset one.
  - Control GC1, secret set and correct vouch: 200 on T_CONN. GC2, same without a Bearer: 200 on T_CONN.
- **Why Major.** The ruling makes the deploy safe by "check Platform S metering end to end". With this code, a status-code check passes even when the secret is missing or mismatched. The real consequence is a partner reading another tenant's usage totals whenever S's key tenant differs from DEFAULT. Whether that is true on Kintsugi or demo is UNMEASURED. "Answers unchanged on single-tenant" holds only if S's key tenant equals DEFAULT.
- **Also imprecise.** "A multi-tenant deployment loses its tenant" depends on NODE_ENV. With `MULTI_TENANCY_ENABLED=true` and `NODE_ENV=production`, `extractTenantContext` (`packages/shared/src/db/tenant-context.ts:70`, "Missing tenant context") answers **400 on every request** once the headers are stripped. In non-production it falls to DEFAULT. Read statically; not run.
- **Minimal fix (no logic change needed):**
  - (a) Rewrite the body's deploy-condition paragraph and metering.ts:55-59 to say this: unset or mismatched gives 200 on the default tenant when the gateway's token exchange worked, and 401 only when it failed. Multi-tenant production gives 400.
  - (b) Wednesday re-words DEPLOY-BLOCKERS step (3): the end-to-end check must assert that the response's `data.tenantId` equals S's key tenant, not merely that it is 200.
  - (c) Optional hardening for a follow-up ticket, not required by the ruling: have `reqTenantId` in metering prefer a verified `req.user.tenantId` when `authenticate()` set the user.
  - (a) changes the head (comment only); a delta re-gate of a comment-only commit is cheap.

## MINOR

### m1. The author's cells do not pin either "second line" as wired into the real app (author's point 2: yes, under-pinned)
- **FOUND.** Mutant g2 removes the verdict read from the metering shim (`metering.ts:62`, leaving only `void isGatewayVouched`). Mutant g5 reverts the KS-458 block (`index.ts:250-252`) to the old ungated inline header read. **Both SURVIVE all 36 author cells** (author_red = 0 for each; `evidence/mutation_gate_r2_g2_g7.log`, `evidence/mutation_gate.log`). C1-C3 test `resolveRequestTenantId` directly, which kills m5 and m6, but not the call site in `index.ts`.
- **Gate cells built** (`evidence/gate1546-b-nostrip.test.ts`). The real app runs with the strip REMOVED by a mock that keeps the real verdict and puts back every header the middleware deleted. Control GB0 proves a forged header really survives.
  - GB1 (forged connector headers, no Bearer → 401, handler not called) kills g2.
  - GB2 (human JWT + forged `x-tenant-id` → tenant DEFAULT) kills g5.
- **Fix:** add GB0-GB2 (or equivalents) to the PR's cells.

### m2. Part (c)'s "upstream-attached tenant is verified, never a raw header" is false in multi-tenant mode
- **FOUND.**
  - `utils/requestTenant.ts:11-13` says `req.tenantId` attached upstream comes from a verified context. So does the C2 comment (`ks1032-unconfigured-vouch-fails-closed.test.ts:250-252`).
  - The body says: "never from a caller's raw header".
  - In fact the ONLY upstream writer is `extractTenantContext` (`packages/shared/src/db/tenant-context.ts`, `req.tenantId = tenantId` from `req.headers['x-tenant-id']`). I enumerated every `.tenantId =` writer in originate and shared: three, namely `index.ts:251`, `metering.ts:65` and `tenant-context.ts:91`.
- **Consequence.** With `MULTI_TENANCY_ENABLED=true` the attached arm wins and is not gated, so part (c) gives no defence there if the strip is ever removed. The strip remains the only line. Not exploitable while the strip works: GA5, GB3 and GC7 found 0 forged-versus-bare differences. MULTI_TENANCY is `${MULTI_TENANCY_ENABLED:-false}` in docker-compose.yml. Whether it is on for any live box is not measured by me.
- **Fix:** correct the three texts. Optionally gate `extractTenantContext`'s header read on `isGatewayVouched` in the `index.ts` multi-tenant block.

### m3. Operator-facing docs still say unset is fail-OPEN (the docs the deploy seat reads)
- **FOUND (head, grep -n -i "fail-open").**
  - `Blockchain/Dev/.env.example:329`: "UNSET is valid and fail-OPEN by design".
  - `Blockchain/Dev/env.example:465`: the same.
  - `docs/ENVIRONMENT-VARIABLES.md:74`: "No (fail-open, see below)".
  - `docs/ENVIRONMENT-VARIABLES.md:106`: "Unset is valid and fail-OPEN by design".
  - `services/originate/src/index.ts:210`: "why an unset secret is fail-open but loud".
- None was touched. The body says "no config file changed", which is true but leaves these contradicting the shipped behaviour.
- **Fix:** update all five in this PR, or as a follow-up that lands before the deploy.

## INFO

- **i1 (by design, KS-1041, not this diff).** The vouch is a static bearer secret, not a per-request MAC. Replay attacks and "vouch computed over a subset of headers" do not apply: there is nothing request-bound to replay against, and anyone holding the secret is the gateway. GC6 shows it: the correct secret plus forged headers gives 200 on the forged tenant. The secret's storage scope is the control (docs/ENVIRONMENT-VARIABLES.md).
- **i2.** Mutant g7 (`presented === secret` instead of `timingSafeEqual`) SURVIVES all 67 cells, as expected. It is an equivalent mutant, timing only, and cannot be caught by a functional test. The code (pre-existing) uses a length check plus `timingSafeEqual`.
- **i3.** On an unset box, `documents.ts:1018-1021` treats every admin whose JWT tenant is not DEFAULT as "using override", which disables the admin cross-tenant registry fallback. This errs on the safe side. Read statically.
- **i4.** A vouch with trailing whitespace is accepted (GC4b, 200). This is HTTP optional-whitespace trimming by the parser, so the received value IS the secret. Not a defect.
- **i5.** A duplicated `x-user-role` header was already refused on develop: node joins it to "connector, connector". The other forged variants were 200 on develop and are 401 on head (GA4, 8 variants).
- **i6.** The Linear attachment on KS-1032 is `linkKind = contributes`, 1 attachment (read-only GraphQL query, `evidence/linear_ks1032_attachments.json`). There is no closing keyword in the body: 0 hits from the regex `(close[sd]?|fix(e[sd])?|resolve[sd]?) (#|KS-|https)`; a planted "Closes KS-1" gives 1 hit.

---

## FOUND / TESTED / HOW — by brief item

**1. Author's cells, red/green, suites, tsc**
- **Head**, jest JSON reporter (`evidence/head_ks1032_ks1041.json`): ks1032 12/12; ks1041-gateway-provenance 21/21; ks1041-provenance-mount-wiring 3/3. Total **36/36**.
- **Develop**, the head's two test files copied in (`evidence/dev_headcells.json`):
  - The ks1032 file does not compile (TS2339, the new exports are absent). This confirms "a straight revert is a compile break".
  - The head's ks1041-gateway-provenance file gives **2 red / 19 green**. The red cells are exactly the two inverted ones; the green cells are the controls.
  - Develop's own ks1041 pair: 24/24 (`evidence/dev_ks1041_own.json`).
- **Red variant (author's point 1), INDEPENDENT of the author's tool.** I built it from DEVELOP, not from the head: develop plus only the plumbing (an `isGatewayVouched` export that nothing ever records, and a `requestTenant.ts` holding develop's ungated logic). Result **6 red / 6 green**:
  - red: A1, A2, A3, A5, B1, C1;
  - green: both CONTROLs, A4, B2, C2, C3;
  - A1 received **200**.
  - The variant reproduces develop's trust of forged headers; it is not too kind. `evidence/red_variant_gate.json`.
- **Full originate unit suite** (jest, default config, integration files excluded):
  - head **106/106 suites, 1333/1333**;
  - develop 105/105, 1321/1321;
  - scratch merge of develop + head 106/106, 1333/1333.
  - Files: `evidence/unit_wt_*.json`.
- **tsc `--noEmit -p services/originate/tsconfig.json`:** head rc 0 / 0 errors; develop rc 0 / 0; merge rc 0 / 0. The control, a planted type error, gave rc 2 / 2 errors. Files: `evidence/tsc_*.log`.

**2. The boundary**
- **Header reads, enumerated by grep over originate src** (`evidence/head_header_reads.txt`, 47 lines). After the PR the only trust-header reads are:
  - `requestTenant.ts:36` (gated);
  - `metering.ts:62-65` (gated);
  - `adminConfig.ts:561` `x-tenant-override` (inside an authenticated admin route; stripped unless vouched).
  - Every other route takes identity from `authenticate()` (a verified JWT) and tenant from `req.tenantId`.
  - `extractTenantContext` is the multi-tenant reader (m2).
- **All declared routes, not sampled.** GA5, GB3 and GC7 walk every route in all 17 mount stacks, 147 (method, path) pairs. Each is sent bare, with a forged connector set, and with a forged admin set (`x-user-role`, `x-user-id`, `x-tenant-id`, `x-tenant-override`, `x-roles`, `x-auth-user`, `x-org-id`, `x-organization-id`, `x-user-email`). Status and normalised bodies are compared.
  - **Head: 0 differences** in each of three states: unset; strip removed; set with no vouch.
  - **Develop, the CONTROL that the scan can register a hit: exactly 1 difference**, `GET /api/metering/usage [connector] bare=401 forged=200`.
- **Variants, secret unset** (GA4, 8 cells): upper-case header names, duplicate role, duplicate tenant, whitespace vouch, empty vouch, duplicate vouch, padded role, header present with no vouch. **Head 8/8 give 401** with the handler not run; **develop 7/8 give 200**.
- **Variants, secret set** (GC4, 6 cells): wrong vouch of the same length, prefix, upper-cased, duplicated, empty, superset. All give 401.
- **Legitimate calls are not refused** (false-refusal check):
  - GC1-GC3: vouched Platform-S with and without a Bearer, and a vouched human. All 200 on the right tenant.
  - A4 (author): the direct callers m365 and nft are unaffected.
- **False pass found:** none in the code. The one false statement is M1.

**3. Platform-S metering:** see M1. Exact answer: 401 only when no Bearer arrives; otherwise 200 on DEFAULT.

**4. Mutants** (instrument: `evidence/mut_gate.py`; each mutant is run against 67 cells, the 36 author cells plus 31 gate cells; the mutated file is restored from the pristine head copy and checked byte-identical; baseline 67/0 and restored 67/0):

| id | mutant | result | author cells red | gate cells red |
|---|---|---|---|---|
| c0 | CONTROL comment-only | survived (correct) | 0 | 0 |
| m1 | vouched-reader trusts 'unconfigured' | killed | 3 (B1,B2,C1) | 3 (GB1-3) |
| m2 | NOT-unvouched test | killed | 3 | 3 |
| m3 | unconfigured records, no strip | killed | 2 (B1, KS-1041 inverted) | 0 |
| m4 | unconfigured strips, no record | killed | 1 | 1 |
| m5 | attached tenant gated | killed | 1 (C2) | 0 |
| m6 | absent verdict = vouched | killed | 1 (C1) | 0 |
| m7 | vouch left on request | killed | 2 | 0 |
| g1 | unset branch fail-open (develop exactly) | killed | 2 | 1 |
| g2 | metering verdict read REMOVED | killed **by gate only** | **0** | 2 (GB1, GB3) |
| g3 | metering verdict read INVERTED | killed | 1 | 5 |
| g4 | isGatewayVouched INVERTED | killed | 5 | 8 |
| g5 | index.ts wiring reverted to the ungated inline read | killed **by gate only** | **0** | 1 (GB2) |
| g6 | strip removed (both branches) | killed | 7 | 0 |
| g7 | `===` instead of timingSafeEqual | survived (equivalent, i2) | 0 | 0 |
| g8 | tenant fallback changed | killed | 0 | 4 |
| g9 | strip pattern loses `tenant` | killed | 1 | 0 |
| g10 | vouchMatches drops the empty guards | killed | 1 | 0 |

- **First-run caveat.** In the first run, g2 and g7 failed to compile (TS6133). They were re-run with `void` guards and the table shows the re-runs (`mutation_gate_r2_g2_g7.log`, `mutation_gate_r3_g7.log`). The first-run g2 "kill" was a compile break, not a behavioural kill. Recorded so nobody quotes it.
- **Tally:** the author's 7 are re-derived and 7/7 killed. Gate mutants: 10 (g1-g10). 9 behavioural kills; g7 is equivalent. 2 kills (g2, g5) come only from gate cells, which is m1.

**5. Scope and hygiene**
- `git diff --stat 405e33a1..ad366066`: **6 files, +464/-43**. These are exactly the six declared, and they match `gh pr view` files.
- **Overlap with develop's movement** (`git diff --name-only 405e33a1..026c2d16` = 2 files: `routes/verification.ts` and the ks1119 integration test; `comm -12` against the PR's 6) = **0**. Planted control (`index.ts` appended to develop's list) = 1.
- **`git merge-tree --write-tree 026c2d16 ad366066` → rc 0, tree ae6367a2d680d0bbdb7a37163fa4f4065dc10bef.** Negative control: a scratch commit (develop plus an edit to the line the PR changes at metering.ts:42) merged with the head gives **rc 1, CONFLICT (content) in metering.ts** (`evidence/overlap_mergetree.txt`).
- All 67 author and gate cells pass on that merged tree, and the full suite is 1333/1333 (`evidence/merge_gate_and_author.json`).
- The body's statements match the code everywhere except M1 (401) and m2 ("never a raw header").
- **Author's point 4 (the inversion is honest).** Only the two cells in the "unconfigured" describe block changed, and the ruling and card are cited. A grep for `import('../index')` / `require('../index')` across originate tests finds 2 files, both in this PR's scope (control: the ks1032 file counts 1). So no other unit test loads the real app relying on fail-open. `rightsHolders.tenant-scope.integration.test.ts` sends `x-tenant-id`, but it builds its own express app (adminConfigRouter + extractTenantContext) with no provenance middleware, so it is unaffected.
- **Author's point 3.** Part (c) is real behaviour at the function level (C1-C3; m5 and m6 killed). Its wiring was decoration until GB2 (m1), and it does not exist in multi-tenant mode (m2).

## NOT tested, and whether it could hide a Major
- No live stack, no Docker, no remote box. I measured nothing on Kintsugi or demo: not the effective secret, not MULTI_TENANCY, not S's key tenant. **This could hide a Major.** If S's key tenant is not DEFAULT, M1's tenant switch is a real cross-tenant usage disclosure on any unset or mismatched box. The deploy blocker must measure it.
- The JWT signature was mocked (`verifyJwtRs256`), with token shapes taken from auth's `generateConnectorToken`. The real RS256/JWKS path was not exercised. It is pre-existing and unchanged.
- I did not run the gateway itself. That the Bearer and the trust headers travel together on `/api/metering` is read from `api-gateway/src/middleware/auth.ts:419-427` and `routes/proxy.ts:298,653-656`.
- Multi-tenant mode (`MULTI_TENANCY_ENABLED=true`) was not run. `getTenantManager()` is null before `initDb`, so the block is a pass-through in this harness. m2 and i3 are static reads.
- `POST /api/verification/verify-file` and `POST /api/v2/verification/verify-file` (multipart) time out bare and forged alike. Those 2 of 147 routes are effectively not covered by the enumeration. They are public verify routes that read no trust header (grep), so they are unlikely to hide a Major.
- I did not run the DB-backed integration suites, Schemathesis, Akto, Playwright, k6, or preflight. I used no Postgres at all, so I touched none of the reserved ports.
- No GitHub or Linear writes were made. The PR body was read via `gh pr view` with the project token, and Linear via a read-only GraphQL query.

## Evidence index (this folder, `evidence/`)
- Gate cells: `gate1546-a-unset.test.ts`, `gate1546-b-nostrip.test.ts`, `gate1546-c-set.test.ts`, `gate_cells_gatekit/`.
- Runs: `gateA_wt_gate.json` (head), `gateA_wt_dev.json` (develop), `gateBC_head.json`, `head_ks1032_ks1041.json`, `dev_headcells.json`, `red_variant_gate.json`, `unit_wt_*.json`, `tsc_*.log`, `merge_gate_and_author.json`.
- Mutation: `mut_gate.py`, `mutation_gate*.log`, `mut_*.json`.
- Overlap and merge: `overlap_mergetree.txt`.
- PR and Linear: `pr1546.json`, `pr1546_body.md`, `linear_ks1032_attachments.json`.
- Census: `head_header_reads.txt`.

Hash recipe: delete line 2, take sha256 of the rest, keep the first 16 hex characters.
