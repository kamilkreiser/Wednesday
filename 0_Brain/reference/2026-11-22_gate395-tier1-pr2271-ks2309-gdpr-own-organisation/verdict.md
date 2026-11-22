PR 2271: GO WITH NOTES (at head 4cec1424a1ccd47028667619240a5d3623bcacbc; tier 1)

# Gate 395, tier 1 (Opus), PR 2271 (KS-2309), 2026-11-22 ~15:52-16:07 AEDT

## Pins
- **Pinned twice, at 15:52:22 and 16:07:00**, by git ls-remote (through the Secuura project's gh credential helper, read-only) and gh pr view. Same values both times:
  - PR 2271 OPEN, MERGEABLE, head 4cec1424a1cc, ONE commit, parent = develop 44c312fd120b. 6 paths, +401 -20 (gdpr.ts +72 -16, ks2309 cells +263, adminConfig.ts +4 -3, ks2308 file +33 -1, two fragments +17 / +12). updatedAt 04:50:11Z.
  - develop = 44c312fd120bc943cefec36bd9f04b5410da5092.
- **Merged state = the head.** It fast-forwards onto develop; `git merge-tree --write-tree origin/develop pr/2271` gives rc 0 with tree e3bb487510e9 = the head's own tree. Every "head" figure below is the merged state.

## How I measured
- Own clone `_work/g` from GitHub (`--reference-if-able` gate 394's clone, `--dissociate`). Worktrees: `h` (head: suite, static, probe g), `x` (head: probes d/e/f, mutants), `d` (develop: suite, red-first, probe d).
- node_modules APFS-cloned from gate 394's `h` (root, packages/shared, services/{originate,auth,shared}); no package.json, lockfile or packages/ change between 387e824 (gate 394's head) and this head (diff empty). `packages/shared/dist` built with tsc in each worktree (rc 0).
- Node v26.8.1 (not LTS), jest, TMPDIR /private/tmp/g395t.
- Scripts in `_work/`: `run_cwd_g395.py`, `suites_g395.sh`, `static_g395.py`, `mutants_g395.py` (19 mutants over gdpr.ts and adminConfig.ts; 26 originate test files that import either router, 594 cells), `mt_g395.py`, `an_e.py` / `an_e2.py`, `lin_read_g395.py` / `lin_search_g395.py` (read-only GraphQL; the key is read into memory from the Secuura project's credentials file as gates 393/394 did, never printed).
- Probes (`_work/probes/`, each writes JSON/JSONL and asserts nothing; the copies run inside a worktree were moved to `_work/_quarantine/` after use):
  - **g395-probe-e**: the real gdprRouter, the REAL `db.ts` (single-tenant GUC proxy), the REAL `tenantGucContext` from @secuura/shared, real requireRole / requireSelfOrRole / hasAnyRole. Stand-ins: authenticate (caller from headers), `@prisma/client` (a fake that records every statement with the GUC set in its transaction and answers `users` under a simulated RLS: GUC tenant's rows only, all rows under the bypass, none with no scope), the gdpr service (records calls). 6 callers x 10 subject spellings x 9 routes = 540 requests, in three modes (normal; every query throws; the PrismaClient constructor throws).
  - **g394-probe-d** (gate 394's, copied unchanged) on develop and on the head.
  - **g395-probe-f**: the lazily imported `../db` throws at module load.
  - **g395-probe-g**: POST `/api/gdpr/dsr` for another user (Q4).
- End state: h, d, x each 0 porcelain lines; x's gdpr.ts sha256 20d4e28d… = h's (the head blob).
- Not touched: no seat tree, no !CODING write, no GitHub or Linear write, no database server, no container, no mail, no launch.

## Findings

No HIGH finding against this PR. The bound holds as ruled on all nine handlers, measured through the real db wrapper and the real tenant context.

### MEDIUM (pre-existing; not a defect of this PR; for Wednesday to route)
**G395-2271-1: POST `/api/gdpr/dsr` lets ANY authenticated caller file a data subject request, erasure included, in ANY user's name, in any tenant.**
- `gdpr.ts:375-401` (head): no `denyConsentIdor`, no `requireSelfOrRole`, no role check. It validates the body and the UUID shape, then `gdpr.createDSR(type, userId, email, notes)`.
- `gdprService.createDSR` (:309-327) writes `audit_trail` with `actor: userId`, the SUBJECT's id, not the caller's. The email and notes are the caller's. The row lands in GET `/dsr/pending` (every tenant, KS-2310) for an administrator to process; an `erasure` DSR is the `dsrId` POST `/erasure/:userId` takes.
- **Measured** (probe g, head): ORG_ADMIN, VERIFIER, OWNER and SYSTEM_ADMIN each get 201 with `createDSR` called for a foreign id, for both `erasure` and `access`.
- It is outside the closed nine and outside the ruled out-list (KS-2310, KS-1696, GET `/retention`). W 54th's census (M2) counted handlers that admit an ORG_ADMIN for another user; this one admits every role, so it fell outside that census. Linear (read-only searches "create DSR", "data subject request", "POST /dsr"): no ticket names it.
- No read follows from it (the creator cannot read the DSR back: GET `/dsr/:dsrId` refuses another user's for every non-platform caller at this head). The harm is a forged, mis-attributed, legally significant request in a platform-wide queue. Whether a user may file a DSR for someone else is a product question.

### LOW
**G395-2271-2: the tenant scope of the lookup is not pinned by any cell (one surviving mutant).**
- X1 (the users lookup wrapped in `runWithPlatformScope`, so it reads every tenant): **0 of 594 failed.** The cells mock `../db` whole, so no cell can see the scope. R4 in the PR says this is not established on a real Postgres.
- **Measured at the head (probe e):** every one of the 208 lookups ran inside one transaction with `app.current_tenant_id` = the request's tenant, never the bypass. A user of tenant T2 whose stored `organization_id` EQUALS the caller's was refused on all nine routes, and so was every request whose tenant was T2 for a T1 caller.
- Practical weight is low: the organisation equality still decides, so dropping the scope opens a door only if two tenants could share an organisation id. Fix shape, if wanted: one cell that runs the real `db.ts` with a recording client (probe e is the shape).

**G395-2271-3: for an ORG_ADMIN, an existing DSR id and an absent one cost different work (an existence signal by timing, not by answer).**
- The answers are byte-identical (Q2). But an existing other-organisation DSR costs `getDSR` plus the users lookup, while an absent one costs `getDSR` only (probe e: R8/R9 lookups 3 vs 0 across the refused spellings). If the db module cannot load (probe f), the existing DSR answers 500 and the absent one 403.
- Low: DSR ids are random UUIDs, so there is nothing to enumerate. Report only.

**G395-2271-4: words that do not hold exactly.**
1. "Anyone else gets the route's EXISTING refusal **before any service call**" (PR body; facts comment e9b1b36d; the gdpr.ts block comment). On GET and PATCH `/dsr/:dsrId` the bound needs the DSR's subject, so `gdpr.getDSR` (a read) runs first for a well-formed id. That is the ruled design ("the DSR pair bound on the loaded DSR's subject"); zero WRITE calls holds everywhere.
2. "the check first in nine handlers" (PR body). On POST `/consent`, POST `/consent/withdraw` and GET `/consent/check`, the existing 400 body checks run first, as `denyConsentIdor` did before. They do not depend on the subject, so they are no oracle.
3. "A top-level import broke six existing GDPR suites at load": not measured by me.

## The commission's questions
- **Q1 THE BOUND: holds.**
  - `refuseGdprSubject` (via `mayActForSubject`) is the first statement in the `try` of GET `/consent/:userId`, GET `/dsr/user/:userId`, GET `/export/:userId` and `/download`. It comes after the body checks on the three consent body routes (G395-2271-4.2), and after `getDSR` on the DSR pair (4.1). PATCH decides before `req.body` is read.
  - Platform roles and self pass with NO statement: probe e, SYSTEM_ADMIN and VERIFIER rows, 0 statements in 180 requests.
  - Probe e (normal mode), ORG_ADMIN of org B. **Admitted:** own-organisation subjects and DSRs, lower or upper case: 200/201, with the service called.
  - **Refused with 403** on all nine routes, with zero non-`getDSR` service calls:
    - another organisation, lower and upper case;
    - another tenant, even with the same organisation id;
    - absent;
    - malformed, braced, hyphenless, and with a trailing newline;
    - the token claim naming org A (A's subject is refused; its own B subject is still admitted, because the row decides);
    - the request's tenant set to T2;
    - a caller id with no users row.
  - **Gate 394's probe d re-run:**
    - Develop: ORG_ADMIN gets 200/201 with `getUserConsents`, `recordConsent`, `withdrawConsent`, `hasValidConsent` and `exportUserData` called for the foreign id (as gate 394 measured).
    - Head: ORG_ADMIN gets **500 with zero service calls** on all five. In that probe the real `db.ts` loads and the lookup throws, because this worktree has no generated Prisma client (KS-1305 message). So it fails closed (Q3).
    - Controls are unchanged: VERIFIER 403, SYSTEM_ADMIN 200.
  - **Scope:** the lazily loaded module runs the lookup under the REQUEST tenant. `index.ts:264-268` sets `req.tenantId = resolveRequestTenantId` (upstream, else the gateway-vouched `x-tenant-id`, else the default tenant), then `tenantGucContext()`, both before `/api/gdpr` is mounted (:299). `db.ts`'s proxy then bundles `set_config('app.current_tenant_id', …)` into the statement's transaction (measured in probe e). `users` is in migration 039's fail-closed list (:87).
  - No spelling, id shape or request shape got through.
- **Q2 NO ORACLE: holds** (status, body, content-type and content-length identical). For each of the nine routes, the ORG_ADMIN answers for 8 refused subject spellings (another organisation x2, another tenant, absent, malformed, braced, hyphenless, trailing newline) are one shape each:
  - GET `/consent/:userId`, the two exports and GET `/dsr/user/:userId`, GET `/dsr/:dsrId`: 403 "You may only access your own data".
  - The three consent routes: 403 "You may only act on your own consent records".
  - PATCH: 403 "Insufficient permissions" (requireRole's body).
  - The only difference is work done (G395-2271-3).
- **Q3 THE LAZY IMPORT: fails closed in every mode I could make.**
  - Every query throws (probe e throwQuery): ORG_ADMIN gets 500 or 403, with zero non-`getDSR` service calls in 360 requests.
  - The PrismaClient constructor throws (throwCtor): the same.
  - The real missing generated client (probe d on the head): 500, zero calls.
  - `../db` throws at module load (probe f): 500 on all nine, zero calls except `getDSR` on the DSR pair.
  - Every call to the bound sits inside its handler's `try`; the catch is `fail500`. The one other catch is POST `/consent`'s `mapGdprWriteDbError`, which can only map pg codes to 404/400, and the lookup's ids are UUID-checked before the cast.
  - Missing DATABASE_URL at runtime is not reachable past load: gdpr.ts imports `utils/logger` (top of file), whose graph reaches config.ts.
  - Platform and self never touch the db module.
  - **No fail-open found.**
- **Q4 OTHER DOORS:** I grepped services/, packages/ and scripts/ for the gdprService entry points and the two table names.
  - Outside the tests, only originate's gdpr.ts, adminConfig.ts (GET `/privacy`, guarded since KS-2308), retentionScheduler (the sweep) and the operator scripts reach them.
  - packages/shared `gdpr-compliance.ts` is an in-memory module that no service imports.
  - The api-gateway has no own route (it proxies `/api/gdpr`). Control: `gdprRouter` is found in 2 files.
  - Every router entry in gdpr.ts:
    - the nine are bound;
    - `/dsr/pending` (KS-2310) and `/deletion-log` (KS-1696) are ruled out;
    - `/retention` is report only;
    - `/erasure/:userId` and `/retention/enforce` are SYSTEM_ADMIN only;
    - `/erasures*` are connector-role only, tenant from the token;
    - **POST `/dsr` is open to every role: G395-2271-1.**
- **Q5 THE CELLS: reproduced.**
  - Head: ks2309 115/115, ks2308 57/57.
  - The head's two test files on develop's code (worktree d): ks2309 **66 failed, 49 passed**; ks2308 **1 failed (P3), 56 passed**. All 67 fail by assertion, none from the harness:
    - 53 `Expected 403, Received 200`;
    - 7 `403` vs `201`;
    - 5 `403` vs `404`;
    - 1 `403` vs `400` (the empty PATCH body);
    - 1 `toHaveBeenCalledTimes(1)` received 0.
  - N5/N6 are pins (green on develop), proven by their mutants (Q6).
- **Q6 MUTANTS** (on the merged state; 26 files, 594 cells; BASE 0 failed; both product files restored and sha256-checked after each; evidence/mutants.out, mutants_g395*.json, mut/):

  | mutant | failed | killed by |
  |---|---|---|
  | K3 export check removed | 8 | R1-R4 GET /export |
  | K5 denyConsentIdor admits any GDPR admin | 24 | the three consent body routes |
  | **K8 claim wins** | 14 | R4 x7 + R6 x7 |
  | K8b claim as fallback when the row has none | 7 | R4 |
  | **K9 null equals null** | 7 | R4 |
  | **K10 ORG_ADMIN as platform** | 66 | all red cells + C1 lookup pin |
  | **K11 bound after the service call** | 7 | GET /consent/:userId cells |
  | **K12 / K12b DSR decided on the DSR id (GET / PATCH)** | 1 / 1 | C1 own-organisation DSR |
  | K16 self removed | 7 | C2 |
  | **R1b refresh guard removed (void req)** | 1 | P3 |
  | **N5 / N6** | 1 / 1 | the N5 / N6 pins |
  | X2 subject UUID check removed | 7 | R3 malformed |
  | X3 refusal warning dropped | 9 | R9 warnings |
  | X4 malformed DSR id read for an ORG_ADMIN | 1 | R7 |
  | X5 subject org read from the caller's row | 40 | R/C cells |
  | X6 export/download check removed | 8 | R1-R4 /download |
  | **X1 lookup under platform scope** | **0** | **survivor: G395-2271-2** |

  My first X3 spelling did not compile (tsc 2; the run is in mutants_g395_run1.json); I re-spelled it and re-ran it (tsc 0, 9 killed).
- **Q7 WHOLE:**
  - Originate suite (default jest config, `--json`): develop **2965/2965 in 237 files**, head **3085/3085 in 238 files**. Failure sets are equal (both empty).
  - Per-test diff: 121 tests only on the head (115 ks2309 + 6 ks2308), 1 only on develop (the old P3 name), **0 changed status**.
  - tsc 0 (planted: rc 2, 1 error).
  - eslint `--max-warnings 0`: gdpr.ts, adminConfig.ts and both cell files rc 0; gdpr.ts and adminConfig.ts on develop rc 0 (planted: rc 1).
  - check.cjs originate: 332 examined, 271 under `__tests__`, 0/0/0 (planted: 1 new, rc 1).
  - Fragments OK (planted: FAIL). check:openapi CHECK PASS.
  - The spec declares 403 on all nine operations (js-yaml read of secuura-api.yaml).
  - Standalone ratchet: originate, auth, vc-issuer, security and m365 OK. **api-gateway 2 new (ks815, TS2345) in my clone, IDENTICAL on develop**: my clone has no install of api-gateway's own lockfile, and the PR touches no api-gateway file. So the api-gateway leg and the leg test (45/48, its 3 failures are that one result) are UNMEASURED here, not red against the PR.
  - Overlap: 19 open PRs (18 others + this one); none touches any of the 6 paths; no file list is truncated (control: package-lock.json in 11). **PR 2099 touches `gdprService.ts`, not `gdpr.ts`: confirmed.** Its diff changes no `getDSR` / `userId` line, and `merge-tree pr/2271 pr/2099` is rc 0.
  - merge-tree onto live develop: **rc 0** (tree = head tree). Planted control: a local commit a87a32c9fec1 rewriting develop's `denyConsentIdor` signature line, never pushed: **rc 1**, CONFLICT (content) in gdpr.ts. My first planted control (a comment on the export handler line) gave rc 0, a control that did not fire; I replaced it with the one above.
- **Q8 WORDS:**
  - PR body: summary, rule, census, figures (66/49, 1/56, 115/57, 2965/237, 3085/238, +120, 332/271, 6 paths +401 -20) and the mutant table rows I re-made all reproduce. Exceptions: G395-2271-4.1 and 4.2.
  - "consent_records and data_subject_requests have no tenant column and no RLS": holds (no policy on either; neither is in 039's list; users is).
  - "as documents.ts does at two sites": holds (:2239, :2931).
  - Callers: holds. Admin UI and smoke-test read only `/dsr/pending`; no product code calls `/pricing/refresh` (0 hits); the e2e GDPR specs use non-admin or `loginAsAdmin`.
  - Residuals:
    - R1 accurate (KS-2310 exists, Backlog);
    - R2 accurate (KS-1696 Backlog; `/retention` 200 for any role, probe d);
    - R3 accurate (probe e: VERIFIER absent DSR 404, another user's 403);
    - R4 honest (my probe e narrows it: the wrapper does scope; real RLS remains unrun);
    - R5 honest.
    - Missing from the residuals: POST `/dsr` (G395-2271-1).
  - NOT run is honest; Node 26 is disclosed.
  - KS-2309 (read-only): In Progress, priority 2, created 03:49:24Z. Its text holds, and it named only five routes, which the PR widened to nine as ruled.
  - Facts comment e9b1b36d (2,351 B; updatedAt .065Z is not after createdAt .085Z, so unedited): holds except G395-2271-4.1.

## Two-NO-GO cap
Not engaged.

## Faults, disclosed
- The first planted merge-tree control did not fire. The first X3 mutant did not compile. Both were replaced and re-run, as recorded above.
- A perl rename in probe e also renamed two JSON output keys (`svc`, `sql` became `mockSvc`, `mockSql`); cosmetic, the analysers read the renamed keys.
- I read no mail, used no `cut -c`, and used no `cd`.

## Not run
- The four platform suites, a booted originate or gateway, a real Postgres / RLS (probe e simulates RLS behind the real db.ts wrapper), any deployed environment, Node 24.
- The api-gateway ratchet leg on a proper install; the "six suites broke at top-level import" claim.
