PR 2224: GO WITH NOTES (at head a160347eab6655cccac7882bc6933372a475716e; tier 1)
PR 2225: GO WITH NOTES (at head 7d4a82f2706335456e882431bc10adc77241fb15; tier 1)

Gate 348 (tier 1, Opus), 2026-11-13 09:20 to 09:37 AEDT. Findings only: nothing was fixed, pushed, posted, commented, mailed, merged, or written to Linear or GitHub.

**Pins.** I re-read them with `git ls-remote` at 09:20:54 and again at 09:36:57 AEDT:
- develop 1ebc3eae6cf455d740df4c948963cceba9bab0a7
- refs/pull/2224/head a160347eab66…
- refs/pull/2225/head 7d4a82f27063…

None moved, and all three equal the commission's pins.
- Both PRs are ONE commit on ae5b615f4cc0.
- develop moved twice after that. The moves are `ae5b615f4cc0..1ebc3eae6cf4`, three paths: a packages/shared ks1973 test and two KS-2055 fragments under `Projects Documents/fragments`. None overlaps either PR. Instrument: `git diff --name-only`.
- At develop, all four touched files are blob-identical to ae5b615f4cc0: enforcement.ts f77932ee30, verification.ts c12c71c753, ks1628 a8e846931b, ks815 a6ec081c08. Instrument: `git rev-parse <ref>:<path>`.
- The builder's READY is copied in this folder as `r117_ready.txt` (16 lines, read whole).

## FOUND

### PR 2224 (KS-1197)

**G348-2224-1 (Low, behaviour delta, stated so it is ruled on knowingly).** "Admitted at none" is a refused-to-admitted change for exactly one class of principal:
- **Who:** a principal whose `verificationLevel` is a truthy non-string (number, array, object), on a document type whose `creatorVerificationLevel` is `none` (or empty).
- **Before:** `meetsVerificationLevel` threw on `.toLowerCase()`. The KS-529 wrapper at `routes/verification.ts:1024-1030` turned that into **500 INTERNAL_ERROR**: refused, by accident.
- **After:** **admitted** past the level check. MFA, providers, metadata schema and the workflow gate still apply after it.
- **Pinned:** cell K3 pins this, and my planted reverts redden it (TESTED, Q2).

It is not a widening of policy. Such a principal now gets exactly what the lowest authenticated principal already gets: the string `'none'`, an absent level, an unrecognised string such as `'api_key'` (KS-1176, cells C3 and C4), or the `__proto__` → `{}` account Peter documented on the ticket. It meets nothing above `none` (K1 → 403).

Who can carry such a claim:
- an auth-minted RS256 JWT built from a bad stored level (the ticket's 2026-10-12 `__proto__` path);
- a dev/test-only test token. Its holder can already claim any string level, including `government`, so nothing is gained there.

Instruments: source read of `enforcement.ts:54-66, 98-170` at the head and `middleware/auth.ts:122-163, 523-716`; vitest K-cells and planted reverts.

**G348-2224-2 (Low, scope honesty: correct as stated).**
- **Body:** BLUF "A PARTIAL DEFENCE, not the ticket's fix … the ticket stays open". `Refs KS-1197` only. 0 close words (regex control fires on "Closes KS-1").
- **Ticket scope:** the ticket's recommendation is to validate where the principal is built (`middleware/auth.ts`) and to make the verify handler's rejection reach the error handler. Neither is done, and the body says so.
- **Linear read-only:** state In Progress; the PR is attached.
- **The verify-handler half:** it concerned the `POST /api/documents/:id/verify` mock that KS-1628 retired. The step-approval code at `verification.ts:544-566` calls neither function. The role `.toLowerCase()` there (line 552) is the seat's side observation; I agree it is outside this PR.

**G348-2224-3 (Info).** eslint reports 1 warning: `no-useless-assignment` at line 62:9 of the new test. There are 0 errors. Product file: 0 / 0. This matches the READY.

### PR 2225 (KS-1855 half two)

**G348-2225-1 (Medium, needs Wednesday's ruling before the demo redeploy; not a NO GO, because the behaviour change is Kam's ruling c).** In a default stack, an authenticated, in-scope caller who is NOT the owner of a certification was previously refused (404) and is now admitted (200). Each call also writes a charge event.
- **Before:** the stand-in's "exists" check was originate `GET /api/documents/:id`, forwarded with the caller's bearer. That route 404-cloaks a same-tenant non-owner (`originate/src/routes/documents.ts:1177-1187`), so the stand-in answered **404 "Certification not found"**.
- **After:** the request reaches originate `POST /api/certifications/:id/verify` (`certifications.ts:1247-1310`). That route does a tenant-scoped `getCertification` and then answers **200** with `status`, `checks`, `issuer {id, did}` and the raw `blockchain` object. It has **no `callerMayReadCertification` bind**: the KS-1695 rule that `GET /:id` applies, whose doc comment says "Callers must apply this BEFORE any side effect".
- **Side effect:** the route **writes a `verification` charge event on every call** (`createChargeEvent('verification', …)`, line 1273). The public `/api/verification` verify writes none: `git grep -c createChargeEvent` gives 0 in originate `verification.ts`, against 9 in `certifications.ts` as the control.
- **Mitigation, read from source and not measured:** the anonymous public `POST /api/verification/verify` by documentId already discloses status and issuer name. So the information delta is mainly the DID and the raw blockchain object. The new thing is the billable write per call, by any same-tenant principal with the scope.
- **Exact fix, if Wednesday wants it before deploy:** in originate's verify handler, apply `callerMayReadCertification` (or a deliberate verifier rule) before `createChargeEvent`. This is a separate originate change, not in this PR's file. The alternative is to record that verify is meant to be open to any same-tenant principal.
- **Instruments:** source reads at the 2225 head. My in-process probe (Q4) shows the path reaches originate with the caller's bearer. Originate's own non-owner answer is read, not run.

**G348-2225-2 (Low, docs).**
- `api-gateway/src/index.ts:426-433` still says "The certifications route is still answered here". With the flag unset (the default) that is no longer true.
- `verification.ts:453-454` ("originate doesn't expose") is stale, as the body itself says it left it.

**G348-2225-3 (Info).** KS-815's NUL-in-body guard cells on this route now run only with the flag stubbed on. With the flag off (default), the body streams raw to originate, which ignores it in verify. My probe saw `{"purpose":"gate348"}` arrive intact, so the "gate before mockBodyParser" claim holds. The gateway-side body guard for this path is now flag-only. That is the intended consequence, recorded.

**G348-2225-4 (Info).** H1 stubs the flag to `''`, not unset. My probe used a real `delete process.env.ENABLE_MOCK_ENDPOINTS` and got the same fall-through, so the cell's claim holds for "unset".

### Both

**G348-BOTH-1 (Info, body wording).** Both bodies say "The pre-merge acknowledgement boxes for Schemathesis and Akto are therefore NOT ticked". In fact neither body contains the boxes at all:
- `[ ]` occurs 0 times and `ack:` 0 times in each body.
- Positive control: `.github/pull_request_template.md:14-15` at develop carries `- [ ] <!--ack:schemathesis-->` and `<!--ack:akto-->`.
- The seat's PRs 2219 and 2223 also have 0, so this is the seat's normal practice, not a regression.

Per Kam's card `secuura-premerge-block-nine-prs-1113` = c, a merge does not wait on those suites. So this changes nothing. It is just not literally "unticked".

**G348-BOTH-2 (Info).** Neither body has a self-hold sentence. A hold regex (do not merge / hold the merge / merge wait / not merged until / blocks the merge) gives 0 hits in each, and its control fires. There are 0 close words. Each body carries `PREFLIGHT INCOMPLETE — 13/16 legs ran, 3 SKIPPED. Nothing failed.` followed by "This is NOT a pass". It is quoted correctly as not a pass.

## TESTED

**Q1 Scope (Linear GraphQL, read-only).**
- **KS-1197**, "A non-string verificationLevel claim: POST /api/documents answers 500 and a verifier-gated verify never answers (async throw)". In Progress, PR 2224 attached. PR 2224 is presented as a partial defence and says the ticket stays open (G348-2224-2).
- **KS-1855**, "The gateway answers four admin and verify routes from stand-ins … and certification verify that always says verified:false". In Progress, PR 2225 attached. The ticket comment of 2026-11-09T19:50Z records ruling c verbatim. The PR title and BLUF say "HALF TWO", and "Half one (routes/admin.ts) is NOT in this PR, and the ticket stays open". `Refs KS-1855` only.

**Q2 Red-first, reproduced by me** with the package's own runner (`npm --prefix …/services/api-gateway test -- run <file>`, vitest JSON counts):

| Run | Result |
|---|---|
| KS-1197, head | 13/13 |
| KS-1197, product reverted to develop's blob f77932ee | **9 failed / 4 passed** (K1×3, K2, K3×3, K4, K5 red, all by AssertionError on `THREW …toLowerCase…`; C1-C4 green) |
| KS-1197, planted revert of hunk 2 only | 4 red (K1×3, K2: `userLevel.toUpperCase is not a function`) |
| KS-1197, planted revert of hunk 1 only | 2 red (K4, K5) |
| KS-1855, ks1628 + ks815, head | 22/22 |
| KS-1855, product reverted to c12c71c7 | **2 failed / 20 passed** (H1, H2: `[404, true]` vs `[404, false]`; G2 control green) |
| KS-1855, planted gate without the flag half | H1 red only |
| KS-1855, planted gate without the NODE_ENV half | H2 red only |

So each product hunk and each half of the gate is pinned by named cells. Every plant was restored with `git checkout HEAD -- <file>`, and `hash-object` read back the head blobs be841d50 and 9928be09.

**Q3 Callers of `meetsVerificationLevel` / `enforceDocumentTypeRules`.** Instrument: `git grep` at the 2224 head and at develop over the whole repo, excluding tests.
- **Product call chain:** `enforcement.ts:155` (`meetsVerificationLevel`, inside `enforceDocumentTypeRules`) ← `routes/verification.ts:932` (deps-injected: `index.ts:54` import, `:940` deps, `verification.ts:108` type, `:324` destructure) ← `router.post('/api/documents', authenticateToken(true), …)` at `:739`.
- **Other hits:** `docs/VOCABULARY.md`, an `admin.ts:317` comment, a `verification.ts:756` comment, the KS-1466 fragment. Test files: 27 at the head, 26 at develop (+1 = the new file).
- **Positive control:** `resolveDocumentType` is found in enforcement.ts (2), enforcement.test.ts (7) and ks501 (5).
- **Result: ONE product caller, as the seat says.** It is reachable only with auth required. Refused-before / admitted-now: see G348-2224-1.

**Q4 Unauthenticated (and other) callers, before and after.** Instrument: an IN-PROCESS test, not a reading.
- **Setup:** `scratch/gate348-probe.test.ts`, the REAL gateway app (`index.ts` default export, shaped like ks1084), with every `*_SERVICE_URL` pointed at a recording stub. The stub emulates originate's `authenticate()`: no Authorization → 401, else 200.
- **Runs:** the same file was run at develop (`wt-dev`) and at the 2225 head, with `ENABLE_MOCK_ENDPOINTS` deleted, under NODE_ENV=test (so CSRF is off; CSRF is global and mounted before both answerers, so it cannot separate them).
- **Results:** `scratch/probe-dev.json` and `scratch/probe-2225.json`.

| Caller (flag unset) | develop (stand-in) | 2225 head |
|---|---|---|
| **A. No credentials** | **404** `Certification not found`. The gateway made an anonymous upstream `GET /api/documents/:id`. | **401 UNAUTHORIZED "Authentication required"** from `requireScope` (no user after `authenticateToken(false)`, `scopes.ts:28-31`). **0 upstream calls.** |
| B. Garbage bearer | 200 stand-in body. This is my stub's artefact: the stub 200s any bearer, while real originate would 401 it, so the stand-in would answer 404. | 401 |
| C/D. User JWT (authMethod email or absent) | 200 stand-in (`verified:false`, `test-issuer`) | 200 from originate. The body arrived intact and the bearer was forwarded. |
| E. OAuth JWT, scopes `documents:read` only | 200 stand-in. There was no scope check. | **403 Insufficient scope** |
| F. OAuth JWT, `certifications:read` | 200 stand-in | 200 from originate |
| G. Unvalidated `sk_` key, no bearer | 404 | 401 (the key was checked at the security stub first) |

- **Control:** flag `true` at the head reproduces develop's row for every caller.
- **Control:** flag `true` + NODE_ENV production at the head falls through, as the flag-unset row does. Here the proxy sent `/api/v1/certifications/…` upstream, a production-mode proxy rewrite that is not this PR's code.
- **(a) Unauthenticated caller:** before, 404 from the stand-in. After, 401 at the gateway, and originate is never contacted.
- **(b) Authenticated caller with the scope:** originate's real verdict, and a charge event per call.
- **(c) What changed direction:** refused-to-admitted only for an authenticated in-scope same-tenant non-owner (G348-2225-1, read at originate). Admitted-to-refused only for an OAuth or API-key principal lacking a certifications scope (now 403; before, the stand-in's 200 for an existing record it may read). No credentials and garbage bearers were refused before as well (404 from the stand-in, after an anonymous upstream lookup) and are refused now (401 at the gateway, never reaching originate): refused both times, with a different code and no upstream call.

**Q5 Consumers.**
- **Peter's `tests/e2e/tests/verifier-exhaustive.prelaunch.spec.ts:298`** (read, not run, not edited) is test 8.1.3. It is the FOURTH fallback in a chain (`/api/verify`, `/api/documents/verify`, `/api/documents/:id/verify`, then this route). It is called with **no token**: `apiRequest` adds Authorization only when `options.token` is set (`fixtures/test-helpers.ts:537-553`).
  - Before (flag false by default, `docker-compose.yml:523`; no `ENABLE_MOCK_ENDPOINTS` anywhere under `tests/e2e` or in `docker-compose.e2e.override.yml`): the stand-in's lookup goes unauthenticated → originate 401 → **404**.
  - After: **401**.
  - Both are ≥400 and <500, so the cell falls through to hash verification or its `toBeLessThan(500)` exactly as before. **Outcome unchanged in a default stack.** If his env sets the flag true, nothing changes either. Not run against a stack.
- **`frontend/issuer/src/services/api.ts:481`** (`certificationApi.verify`, JWT via interceptor, sends `{providedHash}`): **0 callers** in `frontend/`. Control: `certificationApi.` has 2 hits in LineageViewer.tsx. It is dead code today. If it is called, an issuer user now gets originate's real verdict, which ignores `providedHash`.
- **`sdk/javascript/src/modules/certifications.ts:129`** (README example): with `X-Api-Key`, before → always 404 (the stand-in never forwarded the key). After → 403 without a certifications scope, or originate's verdict under the connector bearer with the scope. With an accessToken, same as C/F above.
- **Prod-like flag:** `docker-compose.production.yml:85` `ENABLE_MOCK_ENDPOINTS=false` with `NODE_ENV=production`, so the demo/prod change happens on redeploy, as the body says.

**Q6 Suites, tsc, eslint** (Node v26.8.1; own root-workspace `npm ci --ignore-scripts` per worktree; packages/shared built):

| Tree | Run 1 | Run 2 | Run 3 |
|---|---|---|---|
| develop 1ebc3eae6cf4 | 170 files / 1904 tests, 1904 pass, rc 0 | same | same |
| 2224 head | 171 / 1917, 1917 pass, rc 0 | same | not run |
| 2225 head | 170 / 1906, 1906 pass, rc 0 | same | not run |
| develop + 2224 + 2225 (merge probe tree 4c2acdbef3e1) | 171 / 1919, 1919 pass, rc 0 | not run | not run |

- Runs were interleaved dev → 2224 → 2225 ×2, then the merge probe and a third develop run. load1 ran from 2.4 to 12.3 (other seats' jobs).
- The counts equal the READY's. 1904 + 13 + 2 = 1919.
- `tsc --noEmit -p services/api-gateway/tsconfig.json`: rc 0 at all three trees. The planted-error control gave rc 2 (TS2322 in my plant), and the file was restored to blob be841d50.
- `tsc -p tsconfig.test.json`: rc 2 at all three trees, on an identical set of 25 lines (sorted `diff -q` equal) in csrf 10, ks1165 5, rateLimitEnforce 6, ks1464 2, ks1374 1, ks695 1. None of them is in a changed file.
- eslint, ESLint API with cwd = `Blockchain/Dev` and the root flat config: 2224 product 0/0, test 0 errors / 1 warning (G348-2224-3); 2225 all three files 0/0; develop baseline for the same files 0/0. The rule firing on line 62 is the positive control that the config applies.

**Q7 merge-tree** (`--write-tree`, each side's own merge-base, in my clone):

| Merge | rc | Tree |
|---|---|---|
| develop × 2224, both orders | 0 | 17a269f4da70 |
| develop × 2225, both orders | 0 | 2e6261be6ee0 |
| 2224 × 2225, both orders | 0 | 14c0707cf4b8 |
| develop + 2224 + 2225 (merge probe) | 0 | 4c2acdbef3e1, differing from develop in exactly the 5 PR paths |

- Planted conflicting edit on the 2224 line → rc 1. Twin (an identical edit) → rc 0. Planted conflicting edit on the 2225 line → rc 1.
- Survival: merged-vs-head differs in exactly develop's 3 moved paths for each PR, and those 3 are blob-identical in the merge probe tree. All 5 PR blobs in that tree equal the head blobs.

**Q8 Bodies:** see G348-BOTH-1 and G348-BOTH-2. Tier statements are first in the BLUF. The 2224 body has "PARTIAL DEFENCE"; the 2225 body has "HALF TWO".

## HOW
- **Clone:** `scratch/clone`, `git clone --reference` (read-only alternates) to the Blockchain project's object store, push URL `DISABLED` (re-checked at the end). The PR refs were fetched into the clone only.
- **Worktrees:** sparse (`Blockchain/Dev`): `scratch/wt-dev`, `wt-2224`, `wt-2225`, and `wt-triple`, which is checked out at a local merge-probe commit with tree 4c2acdbef3e1 that was never pushed. All three subject worktrees ended clean, at their pinned shas.
- **GitHub:** PR JSON via `gh api` GET with the Blockchain gh config. **Linear:** one GraphQL query, key read inside python and never printed.
- **No writes outside this folder.**
- **Leftovers (in `scratch/`):**
  - the probe file and its two used copies, moved to `scratch/_quarantine_probe/`;
  - the `out-*.json/log` files, `probe-*.json`, `tsc*`, `pr*_body.md`, `KS-*.json`, `plant.idx`;
  - in my clone only: three unreferenced plant commits, two merge-probe commits and their blobs.

## NOT TESTED
- Schemathesis, Akto, Playwright, k6, Docker/compose, and a real gateway + originate pair. In Q4, originate is a stub. The stub's 200 to any bearer makes develop's "garbage bearer" row optimistic: real originate would make it 404.
- Originate's real answer to a same-tenant non-owner on `POST /:id/verify` (G348-2225-1) is read from source, not run.
- CSRF behaviour under NODE_ENV≠test. It is global and mounted before both answerers.
- `POST /api/documents` over HTTP for KS-1197. The cells call the functions directly.
- Peter's e2e spec (not run, by commission), sdk/python and the connectors, and the demo stack's live flag value.
- Node 24.
- Merge-probe suite: one run only.
