PR 2228: GO WITH NOTES (at head 4383051cafcf7c4535ab74eaa82a850be8efd780; tier 1)

Gate 351 (tier 1, Opus), 2026-11-13 13:58 to 14:10 AEDT. Findings only: nothing was fixed, pushed, posted, commented, mailed, merged, or written to Linear or GitHub.

**Pins.** I read them with `git ls-remote` at 13:58:14 (`scratch/pin1.out`) and again at 14:09:05 AEDT (`scratch/pin2.out`):
- develop 49e4d6a4d0074883dd76372abc54bf0bfb09e6d5
- refs/pull/2228/head 4383051cafcf7c4535ab74eaa82a850be8efd780
- refs/pull/2160/head b02bd2716cc2176cd6d2acd6b75885781f6c58d4

None moved, and all three equal the commission's `pins.out`.
- PR 2228 is ONE commit whose parent is develop 49e4d6a4d007. `merge-tree` develop × head gives the head's own tree da47396c1d08 in both orders, so "the merge" is the head tree.
- The product blob goes from 4257bdf3ba6e (develop) to 3bbdcd6f1c69 (head), as the READY says.
- The builder's READY (`r118_ready.txt`, read whole) is the claim under test. I did not open the R 118th HANDOVER.

## FOUND

**G351-2228-1 (Medium; needs Kam's ruling, which the PR already defers to him; not a NO GO).** The narrowing refuses NO live in-repo caller. It does refuse three classes of caller that are legitimate in principle, and the product's own vocabulary suggests some of them are intended.

Who is refused now:
- **A non-party user of the JS SDK.** `sdk/javascript/src/modules/certifications.ts:129` exposes `client.certifications.verify(id)` with no body, and the SDK README:58 documents it. Its natural user is a third-party verifier integration. Two kinds of principal are now refused:
  - a user JWT that is not the issuer, the holder or an admin;
  - a connector principal verifying a certification it did not issue. A connector is admitted only when its literal `connector:<platform>:<id>` equals `issuer.id`.
- **Same-tenant recipients of a `shareType: 'verify'` share.** `POST /:id/share` accepts `view | verify | reshare` (`certifications.ts:1343`). No code honours `shareType` on the verify route, before or after this PR, so the PR breaks no wiring. But a recipient handed a "verify" share is now refused by the verify route.
- **The "Verifier → Certifier" persona.** `POST /:id/recertify` (`:1436-1442`, "attesting that a Verifier has verified it") stays open to any same-tenant user. After this PR, a non-party may RE-CERTIFY a certification that it may no longer VERIFY. The PR leaves the two routes inconsistent. The body says so and leaves it to Kam (KS-1699's open question).
- Also refused: same-tenant `ORG_ADMIN` and `ISSUER_ADMIN` non-parties (cell C5). This matches `GET /:id` (KS-1695).

Callers that are NOT affected (Q2, below):
- **The public verifier portal.** It calls `/api/verification/verify`, not this route.
- **The issuer frontend helper.** `frontend/issuer/src/services/api.ts:481` `certificationApi.verify` has 0 call sites. Control: `certificationApi.getLineage` has 1.
- **Peter's e2e 8.1.3** (`verifier-exhaustive.prelaunch.spec.ts:298`). It sends no token, so it never reaches the guard.
- **Platform S.** It never calls this route (Stuart, KS-1699, 20 Oct).
- **Other services.** None calls this route: no service-to-service caller exists. nft-certificate calls only `GET /api/certifications/:id`.

Also: in a default stack TODAY, nothing reaches originate's verify through the gateway. The gateway stand-in (`api-gateway/src/routes/verification.ts:378` at develop, no flag gate until PR 2225) answers it. So the narrowing first bites when 2225 deploys. 2228 is the exact fix that gate 348 named for G348-2225-1.

**Exact action:** none is required for this PR. Wednesday should make sure Kam's ruling on KS-1699 (should verify, share and recertify be open to a non-party verifier?) is taken before PR 2225 deploys. If Kam rules "open to verifiers", this guard needs a deliberate verifier rule, for example share-recipient-by-email, added at the same site.

**G351-2228-2 (Low; body wording; the conclusion is unaffected).** The body's Consumers bullet says the e2e no-token call "reaches the originate router's `authenticate()` without credentials before and after this PR". That is not the path:
- **At develop:** the gateway stand-in answers it. Its lookup goes anonymously to originate's `GET /api/documents/:id`, which refuses it, and the stand-in returns 404.
- **After 2225:** the gateway's `requireScope` answers 401 and never contacts originate (G348, Q4).

Either way, the call never reaches the certifications router. The outcome the bullet draws (unaffected) is right.

**G351-2228-3 (Info; KS-1695 double attachment).** Linear (read-only) shows PR 2228 attached to BOTH tickets:
- KS-1699: In Progress, assignee kamil.kreiser, 2 comments. The PR comment is 2026-11-13T02:54:42Z.
- KS-1695: In Progress, attachments [2228, 1667].

The cause is the branch name `feature/ks-1699-certification-verify-needs-the-ks-1695-reader-check`. Is merge likely to move KS-1695's state? No. Control: PR 1667 (branch `kamilkreiser/ks-1695-certification-read-bound`, a `Refs` title) merged 2026-10-20T04:07Z, and KS-1695 is still In Progress. So the extra link is cosmetic. Leaving it or having the board seat unlink it are both fine; it changes nothing on KS-1695.

**G351-2228-4 (Info; cloak scope).** The refusal is byte-identical to this route's own unknown-id answer, `{"verified":false,"error":"Certification not found"}` with 404. I proved this by mutants that change one byte or the status, below. Existence can still be learned elsewhere:
- `POST /:id/revoke` answers 403 to a non-issuer (the builder already lists this);
- share and recertify are not yet bound.

Both are outside this PR's selection.

**G351-2228-5 (Info; test thinness, not a gap).** Every one of the 23 cells reddened under at least one plant (Q3). Two notes:
- The "empty principal" defence is pinned by ONE cell (R7). My `no_empty_guard` mutant reddened R7 only.
- C1, C2 and C6 are controls on pre-existing behaviour and stay green under every verify-guard mutant, by design. I showed they CAN go red with two control plants: a charge before the not-found check reddens C1 and C2, and a change to GET's refusal body reddens C6.

## TESTED

**Q1 The guard, read at the head (`certifications.ts:1247-1324`).**
- **Order of operations:** validationResult → `getCertification(id, tenant)` (a read) → unknown id gives 404 → **guard (`:1273`)** → status flags and hash → `createChargeEvent('verification', …)` (`:1291`) → 200. No write precedes the refusal.
- **The helper is reused exactly, not copied.** The call is `callerMayReadCertification(req, certification)`, defined once at `:159`. Its other call sites are GET `/:id` `:1102`, `/:id/lineage` `:1629` and `/:id/evidence-bundle` `:1722`. The exact call text occurs 4 times in total.
- **Who passes the helper:**
  - `isPlatformRole(role)`, which upper-cases, so `system_admin` and `SUPER_ADMIN` both pass;
  - otherwise a non-empty `req.user.userId` that equals `issuer.id` or `holder.id` exactly.
  - The issuing connector passes only through its literal `connector:…` id equalling `issuer.id`.
  - originate's `authenticate()` is JWT-only and sets `userId` from the token (`middleware/auth.ts`).
- **The builder's four principals are confirmed:** platform admin, issuer, holder, issuing connector.
- **The refusal body is a literal** that duplicates the not-found literal 9 lines above it. It does not share a helper with it. Byte equality is pinned by R4, R7 and R8, and my mutants prove that pin.

**Q2 Consumers** (`git grep` at the head, whole repo, tests and docs excluded where stated).
- **Search 1, the route string:** `certifications/…/verify` and `/:id/verify`. Non-test hits:
  - `frontend/issuer/src/services/api.ts:481`;
  - `sdk/javascript/src/modules/certifications.ts:129`;
  - the gateway stand-in `verification.ts:378`;
  - originate's own definition `:1248` and its index listing;
  - e2e `verifier-exhaustive.prelaunch.spec.ts:298`.
  - **Positive control:** the search finds both builder-named lines and the route definition.
- **Search 2, every `/verify` literal in `Blockchain/Dev` outside tests** (399 lines, deduplicated). No other caller of this route:
  - the verifier portal (`VerifyPage.tsx:81,124`, `ResultPage.tsx:106`), the python SDK (`client.py:102`) and the testing harness (v2.3 `p10_verify`) all use `/api/verification/verify`;
  - nft-certificate's `verify.secuura.io/<certId>` is a portal URL, not this API;
  - mcp-server `/verify` and the connectors call other routes.
- **Search 3, service-to-service:** only nft-certificate GETs `/api/certifications/:id`. Nothing POSTs verify.
- **Each caller, against the new guard:**

| Caller | Sends | Outcome |
|---|---|---|
| Issuer FE `certificationApi.verify` | user JWT | 0 call sites, dead code. A party would pass, a non-party would be refused. |
| JS SDK `certifications.verify` | whatever its HTTP client holds | Parties pass; non-party users and non-issuing connectors are refused (G351-2228-1). Never called in-repo; README example only. |
| e2e 8.1.3 :298 | no token | Never reaches originate (G351-2228-2). Unchanged. |
| Gateway stand-in (develop) | n/a | Answers itself today; after 2225 the proxy forwards to this handler. |

- **Legitimate callers now refused:** see G351-2228-1. In-repo live callers refused: none.

**Q3 Red-proof, reproduced by me** (jest JSON, file-stem pattern `ks1699-certification-verify-needs-issuer`, chosen because my folder path itself contains `ks1699`).

| Run | Result |
|---|---|
| Head | 23/23 |
| develop's product blob 4257bdf3 (= guard removed) | **12 failed / 11 passed**: R1-R7, R8×4, C5. Equals the READY. |
| Guard moved after `createChargeEvent` | 3 / 20: R2, R3, R5. Equals the READY. |
| My mutant: `req.user.id` instead of `userId` | 9 red: R2, R4, R6, R8-control, O1, O2, O4, C3, C4 |
| My mutant: holder-only check | 7 red: R2, R4, R6, R8-control, O1, C3, C4 |
| My mutant: issuer compared on `issuer.did`, not `issuer.id` | 7 red (same set) |
| My mutant: admin branch dropped | 3 red: R7, O3×2 |
| My mutant: empty-userId guard dropped | 1 red: R7 (G351-2228-5) |
| My mutant: case-insensitive, trimmed compare | 2 red: R8[upper], R8[spaces] |
| Cloak: extra field `certificationId` | 6 red: R4, R7, R8×4 |
| Cloak: GET body shape (`certificationNotFound`) | 6 red (same set) |
| Cloak: one byte (trailing `.`) | 6 red (same set) |
| Cloak: status 403, same body | 11 red |
| Control plant: charge before the lookup | 12 red, including C1, C2 |
| Control plant: GET refusal body changed | C6 red |

Every plant was restored with `git checkout HEAD --`, and `hash-object` read back 3bbdcd6f1c69 each time. The worktree ended with porcelain 0. Scripts: `scratch/plant.py`, `scratch/plants.sh`; outputs `scratch/out-plant-*.json`.

**Q4 Whole originate suite** (Node v26.8.1; own root `npm ci --ignore-scripts` per worktree; packages/shared built).

| Tree | Run 1 | Run 2 |
|---|---|---|
| develop 49e4d6a4d007 | 222 files / 2609 tests, 2609 pass, rc 0 | same |
| head = develop+2228 (tree da47396c) | 223 / 2632, 2632 pass, rc 0 | same |
| 2228 × 2160 merge probe (tree f997c8f5) | 224 / 2636, 2636 pass, rc 0 | not run |

- Runs were interleaved dev → head ×2; load1 ran from 9.5 to 24.
- 2609 + 23 = 2632, and 2632 + 4 (2160's ks2017 cells) = 2636.
- This is the first A/B at the NEW base. The builder's was at 49781230da49, and the counts are identical.
- **tsc as the repo runs it:** the service build is `tsc` on `services/originate/tsconfig.json`; originate is not in `check:test-types`. `tsc --noEmit -p` gives rc 0 at all three trees. Planted-error control: rc 2 (TS2322 at my plant), restored to 3bbdcd6f.
- **tsc with tests** (scratch config, types node+jest; the program holds 253 test files including ks1699): rc 2 at all three trees, on the same 4 lines in ks1937 and ks488. The develop and head diagnostics are identical.
- **eslint** (ESLint API, cwd `Blockchain/Dev`, root flat config): product and test file 0/0 at the head; develop product 0/0. Positive control: a planted `var`/`debugger` gives 2 errors (no-var, no-debugger), and the file was restored.

**Q5 The 2160 overlap** (`merge-tree --write-tree`, my clone).
- **Merges:**
  - head × 2160, both orders: rc 0, the same tree f997c8f5a4d3, matching the READY.
  - develop × 2160: rc 0.
- **The merged file keeps both changes' semantics:**
  - the KS-1699 guard comment appears 1 time;
  - the KS-2017 comment appears 1 time;
  - the guard call appears 4 times.
  - merged-vs-head on certifications.ts has the same `patch-id` as 2160's own certifications.ts diff (1c7ddb91d071), so 2160's `/issue` outer-catch hunk (`:935`) lands exactly. 2228's hunk (`:1264`) is untouched.
- **Planted-conflict control:** an edit on base line 935 committed on top of the head conflicts with 2160 in both orders (rc 1, `CONFLICT (content)` naming certifications.ts).
- **On the merged worktree:** the certification-related files (ks1699, ks1695, all ks1868, ks2017; 42 files, 403 tests) pass, and the whole suite is as in the table.

**Q6 Scope.**
- KS-1699's title and BLUF name three routes (verify, share, recertify). The PR selects `/:id/verify` ONLY.
- The body says so in the BLUF ("it selects `/:id/verify` ONLY, and KS-1699 stays open"), under "Audience change, in plain words (a NARROWING)", and under "Not claimed".
- The ticket comment of 2026-11-13T02:54:42Z says the same ("selects ONE of this ticket's three routes … this ticket stays open", "narrows the audience").
- Honest. Title `Refs KS-1699:`, body `Refs KS-1699`. Close-word regex: 0 hits; its control ("Closes KS-1") fires.
- KS-1695: see G351-2228-3. It changes nothing there.

**Q7 Body and docs.**
- Test Evidence section present (1).
- `PREFLIGHT INCOMPLETE — 13/16 legs ran, 3 SKIPPED. Nothing failed.` quoted (1), followed by "This is NOT a pass".
- Self-hold regex (do not merge / hold the merge / merge wait / not merged until / blocks the merge / hold the PR): 0 hits; its control fires.
- Both fragments are present and accurate against what I measured: +13 -0, 12 red, plants 12 / 3 / 20, suite 222/2609 → 223/2632.
- `docs-fragments.mjs check`: rc 0 at the head (cheat and flow 246 new each) against 245 at develop. The one cheat ADVISORY at line 6235 is identical at develop, so it predates this PR.

## HOW
- **Clone:** `scratch/clone`, `git clone --reference` to the Blockchain project's object store (read-only alternates). Fetched with that project's deploy key via a one-shot `GIT_SSH_COMMAND`; push URL `DISABLED` (re-checked at the end).
- **Worktrees** (sparse `Blockchain/Dev`; wt-head also had `Projects Documents` and `systemTest/__tests__/support` added for the fragment checker; wt-dev the same for its baseline):
  - `wt-dev` at 49e4d6a4d007;
  - `wt-head` at 4383051cafcf;
  - `wt-m2160` at a local merge-probe commit ec199424cf04 (tree f997c8f5), never pushed.
  - All three ended at their shas with porcelain 0.
- **GitHub:** PR JSON (2228, 1667) via `gh api` GET with the Blockchain gh config (`gh auth status` = kksecura).
- **Linear:** one GraphQL query per ticket (comments `first:50`, sorted client-side). The key was read inside python and never printed.
- **No writes outside this folder.**
- **Leftovers in `scratch/`:**
  - scripts: `setup.sh`, `plant.py`, `plants.sh`, `suites.sh`, `tsc.sh`, `mt.sh`, `mk_merge.sh`, `lintfrag.sh`, `frag-dev.sh`, `lint.mjs`, `linear.py`;
  - outputs: `out-*`, `tsc*`, `eslint-*`, `fragments*.out`, `KS-*.json`, `pr2228*`, `plant.idx`, `plant_conflict.ts`, `cert_*.ts`, `*.diff`.
  - In my clone only: one planted-conflict commit and one merge-probe commit.

## NOT TESTED
- Schemathesis, Akto, Playwright, k6, Docker/compose, a live database, and a real gateway + originate pair. The cells use an in-process server with a mocked repository and a mocked `authenticate()`.
- The 2225 + 2228 combination over HTTP. The gateway hand-off is taken from gate 348's probe and a source read.
- The JS SDK and any out-of-repo integrator against a running stack. Who uses `certifications.verify` outside this repo is unknown.
- Peter's e2e spec (read, not run).
- Node 24.
- Merge-probe suite: one run only. The R 118th HANDOVER was not opened.
