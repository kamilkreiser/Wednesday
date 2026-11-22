PR 2270: GO WITH NOTES (at head 387e824ee8880eb81297cc48781e2de49c93ac1a; tier 1)

# Gate 394, tier 1 (Opus), PR 2270 (KS-2308), 2026-11-22 ~14:31-14:45 AEDT

## Pins
- **Pinned twice, at 14:32:26 and 14:44:30**, by git ls-remote (through the Secuura project's gh credential helper) and gh pr view (read-only). Same values both times:
  - PR 2270 OPEN, MERGEABLE, head 387e824ee888, ONE commit, parent = develop ec3bee2ebbd8. 5 paths, +352 -4. updatedAt 03:29:47Z.
  - develop = ec3bee2ebbd847441cbf1990e6af9b3235494f3a (PR 2269's squash).
- **Merged state = the head.** It fast-forwards onto develop; `git merge-tree origin/develop pr/2270` gives rc 0 with tree abc36da16ada = the head's own tree. Every "head" figure below is the merged state.

## How I measured
- Own clone `_work/g` from GitHub (`--reference-if-able` gate 393's clone, `--dissociate`). Worktrees: `h` (head: suites, static), `x` (head: probes, mutants), `d` (develop: suite, red-first).
- node_modules copied (APFS clone) from gate 393's `h` (root, packages/shared, services/{auth,shared,originate}); the lockfiles, package.json files and packages/ are unchanged between gate 393's head 3423d65 and this head (diff empty). Workspace links are relative (checked). `packages/shared/dist` was not copied: I built it with tsc in each worktree (rc 0). My first cell run without it failed both suites with "Cannot find module '@secuura/shared'": a harness error, fixed and re-run, not a result.
- Node v26.8.1 (not LTS), jest, TMPDIR /private/tmp/g394t.
- Scripts in `_work/`: `run_cwd_g394.py`, `suites_g394.sh`, `static_g394.py`, `mutants_g394.py` (all 20 originate test files that import routes/adminConfig, 373 cells, per mutant), `mt_g394.py`, `lin_read_g394.py` / `lin_search_g394.py` (read-only GraphQL). Copied from gate 393 and re-pointed; never run in its folder.
- Probes (`_work/probes/`, each writes JSONL and asserts nothing; copies moved to `_work/_quarantine/` after use):
  - g394-probe-a: the PR's harness with a JSON role claim: 25 role shapes x 13 request shapes (the four routes, empty and malformed bodies, `?x=1`, `/PRICING`, `/privacy/`, an upper-case event type, and the two reloads).
  - g394-probe-c: gate 393's probe c re-run (PUT /privacy, ORG_ADMIN of another org vs SYSTEM_ADMIN).
  - g394-probe-d: the real gdpr router (real requireRole / requireSelfOrRole / hasAnyRole, a stand-in authenticate, gdprService mocked to record calls) for Q3.
- End state: h, d, x each 0 porcelain lines; x's adminConfig.ts sha256 55aea877… = h's (the head blob).
- Not touched: no seat tree, no !CODING write, no GitHub or Linear write, no database server, no container, no mail.

## Findings

No HIGH finding against this PR. The four guards hold as ruled: first statement, before the body, zero statements for every non-platform caller, requireRole's body, platform callers unchanged.

### MEDIUM (pre-existing; not a defect of this PR; for Wednesday to route)
**G394-2270-2: consent_records is still read and written cross-tenant by any ORG_ADMIN through `/api/gdpr/consent*`, one user at a time.** This is another door to one of the three tables, not in the ruled NOT-in list and not in W 53rd's M7.
- `routes/gdpr.ts:172` `GDPR_ADMIN_ROLES = ['SYSTEM_ADMIN', 'ORG_ADMIN']` (KS-228 / KS-235). `requireSelfOrRole` (`middleware/auth.ts:181-198`) and `denyConsentIdor` (`gdpr.ts:183-191`) admit any ORG_ADMIN for any subject id. Nothing binds the subject to the caller's tenant or organisation.
- `gdprService.getUserConsents` (:277-287) runs `SELECT * FROM consent_records WHERE user_id = $1` and decrypts `ip_address` via readPii. `consent_records` has no tenant column and no RLS (0 policy hits in migrations; `organizations` 17 as a control; not in 039).
- **Measured** (probe d, ORG_ADMIN of org B, a subject id it does not own): GET `/consent/:userId` 200 (service called with the foreign id, IP returned); POST `/consent` 201 (recordConsent for the foreign id); POST `/consent/withdraw` 200 (withdrawConsent); GET `/consent/check` 200; GET `/export/:userId` 200 (exportUserData). Controls: VERIFIER 403 on all five; SYSTEM_ADMIN 200.
- Reach: the gateway proxies `/api/gdpr` to originate behind `authenticateToken` only (`proxy.ts:897-899`).
- It needs the subject's user id. The bulk source of ids this PR removes (GET /admin/privacy's 100 newest rows) is closed, but KS-2235 (Backlog) still hands an ORG_ADMIN every tenant's users through GET /api/admin/users. So the cross-tenant consent read, forge and withdraw remain a two-step chain.
- No ticket found (searches "consent ORG_ADMIN", "gdpr consent another tenant", "GDPR_ADMIN_ROLES", "consent_records tenant": KS-228 and KS-235 are Done and made ORG_ADMIN a GDPR admin; KS-1696 is the deletion-log sibling). Whether an organisation admin is meant to be a GDPR admin for other tenants' users is a product question. The ticket's title wording "read every tenant's consent records" is fixed only for the bulk listing.
- Also seen (ruled NOT-in, report only): GET `/api/gdpr/retention` answers ANY authenticated role, VERIFIER included (probe d: 200), with every policy and its id. Harmless for writes now that PUT /privacy is guarded.

### LOW
**G394-2270-1: `POST /api/admin/pricing/refresh` is not "reload only": it answers any ORG_ADMIN with the whole price table, the payload GET /pricing now refuses.**
- `adminConfig.ts:244-251` (head): `await loadPricing(); res.json({ success: true, pricing: getPricingTable() })`. Probe a: ORG_ADMIN (with and without an org) got 200 with the full `pricing` object, after one `SELECT … FROM pricing_config`.
- So the Q2b guard on GET /pricing (cell R8 "no price table") closes no disclosure. The harm is low: the ANSWER already rated GET /pricing "low", and this is the price table.
- The premise "reload only" is in Wednesday's ANSWER (Q2b NOT-in), the PR body ("Not changed … (reload only)"), KS-2308's Fix paragraph, and the flow fragment. Cell P3 pins the ORG_ADMIN 200 but asserts only `mockExecuteRaw` not called, never the body.
- This is a ruling premise that does not hold, not a defect against the ruled list. If the GET guard is meant to close the read, the refresh needs the same guard or a body without `pricing`.

**G394-2270-3: two non-equivalent mutants of the new rule that all 373 cells miss (pinning gaps; no hole at this head).**
- N5: the GET /privacy guard skipped when a query string is present. 0 failed; every GET /privacy cell sends no query. Probe a shows the head refuses `?x=1`.
- N6: the PATCH guard applied only to lower-case event types (`/^[a-z_]+$/`). 0 failed; every PATCH cell uses `certification_sign`. Probe a shows the head refuses `/pricing/CERTIFICATION_SIGN`.
- Fix shape: one ORG_ADMIN cell on GET `/privacy?x=1` and one on PATCH with an upper-case or unknown event type.

**G394-2270-4: words that do not hold exactly.**
1. "`isPlatformRole`: SYSTEM_ADMIN or SUPER_ADMIN, any letter case" (PR body, facts comment 6b5618fb, adminConfig.ts:99): the router gate admits only `SYSTEM_ADMIN`, `SUPER_ADMIN`, `super_admin`. `System_Admin`, `system_admin` and `Super_Admin` get the gate's 403 (probe a). It fails closed. This is G393-2269-3.2 again; the test file's own comment (line 71) is correct.
2. "reload only" for POST /pricing/refresh: G394-2270-1.
3. The PR's mutant runs used "8 files, 222 tests"; mine used all 20 files that import the router (373). Not a contradiction, only a different set.

## The commission's questions
- **Q1 THE FOUR GUARDS: hold.**
  - `refuseUnlessPlatform(req, res, '<route>')` is the first statement inside `try` at :218 (GET /pricing), :229 (PATCH), :1398 (GET /privacy) and :1433 (PUT): before `req.body`, before `prisma`/`req.db`, before `getPricingTable`/`updatePricing`.
  - Probe a (325 requests, evidence/probe_a_x.jsonl):
    - ORG_ADMIN, and ORG_ADMIN with an org: 403 from the guard on all 11 shapes of the four routes (bodies valid, empty, malformed; `?x=1`; `/PRICING`; `/privacy/`; an upper-case event type). 0 statements, 0 platform scope; the warning names the route and the role.
    - Every other shape is refused 403 by requireRole first, with 0 statements: `admin`, VERIFIER, ISSUER_ADMIN, no role, null, `""`, `Super_Admin`, `System_Admin`, `system_admin`, `SYSTEM_ADMIN `, long-s, dotless-i, arrays `["SYSTEM_ADMIN"]` / `["super_admin"]` / `["ORG_ADMIN"]`, an object, 1, true, `platform_admin`, ORG_ADMIN+ZWSP.
    - All 282 403s carry one byte-identical body = requireRole's.
    - SYSTEM_ADMIN, SUPER_ADMIN and super_admin: today's statements (PUT 1 UPDATE per policy with an id; GET /privacy 2 SELECTs; PATCH UPDATE + reload SELECT; GET /pricing none; 400s unchanged).
  - **GET /privacy for ORG_ADMIN: no consent_records SELECT** (0 statements; the cell R7 and the probe agree).
  - The zero-statement assertions are real. The mocks record `$queryRaw` / `$executeRaw` and the platform-scope spy runs its callback. The P4 control sees both SELECTs, and on develop the same probe records 1/2/2 statements for ORG_ADMIN.
- **Q2 REACH: holds by code; the gateway forward was not run.**
  - The gateway has no own route for `/api/admin/privacy` or `/api/admin/pricing`. `admin.ts` answers `/api/privacy/settings` (a different path) and document-types, workflows, integrations and settings; there is no `/api/admin/:x` or `*` catch-all (control: `'/api/admin/document-types'` = 2 hits).
  - Both paths fall to `proxy.ts:1296-1300` (`authenticateToken(true)`, `enforceAdminProxy` = `isPlatformOrOrgAdminRole`, which admits ORG_ADMIN), so the originate guard is what refuses.
  - originate's `middleware/auth`, api-gateway and packages/shared are byte-unchanged since gate 393's head 3423d65 (diff empty), so gate 393's probe b (the real RS256 verifier: no header confers a role) still describes this head. I did not re-run probe b.
  - **Gate 393's probe c, re-run:** head: ORG_ADMIN 403, requireRole body, `sql: []`, scope 0; SYSTEM_ADMIN 200 with the UPDATE `(1, true, null, true, id)`. Develop: ORG_ADMIN 200 `updatedCount 1`, the same UPDATE.
- **Q3 ANY OTHER DOOR:** I grepped the whole repo for the three table names and Prisma-style model names (101 hits; services/ and packages/ outside tests: originate only; api-gateway, billing and other services 0, and they appear elsewhere only in init SQL and migrations).
  - `data_retention_policies`: adminConfig GET/PUT (guarded now); `index.ts:499` startup seed INSERT (no caller); `gdprService` :456 `getRetentionPolicies` (GET /api/gdpr/retention, ruled NOT-in: any authenticated role reads it), :479 and :538 inside `enforceRetention` (scheduler + SYSTEM_ADMIN-only POST /retention/enforce: probe d ORG_ADMIN 403).
  - `pricing_config`: `chargeEvents.ts` :67 `loadPricing` (startup; POST /pricing/refresh: G394-2270-1) and :103 `updatePricing` (PATCH only, guarded). No other caller of `getPricingTable`, `updatePricing` or `loadPricing`.
  - `consent_records`: adminConfig GET /privacy (guarded); `gdprService` :207 / :245 / :265 / :280 / :887 / :1069 via `/api/gdpr/consent*`, `/export`, `/erasure`. **The consent routes are open to any ORG_ADMIN for any user: G394-2270-2.** Erasure is SYSTEM_ADMIN-only (`gdpr.ts:594`).
  - `scripts/backfill-subject-deks.js` is an operator script, not a route.
- **Q4 THE CELLS: reproduced.**
  - Head: 52/52 + 31/31 (83 passed).
  - Head's two test files on develop's code (worktree d): **ks2308 52 cells, 18 failed, 34 passed; ks2302 31/31.** Every one of the 18 is an assertion failure, no harness error:
    - R1, R2 x4, R3 x3, R4: `Expected: 403 Received: 200`;
    - R5 x3: `403` vs `400`;
    - R6 x4: warning `undefined`;
    - R7, R8: `403` vs `200`.
  - The three KS-2302 pins (G1, G4/G5 x2) are green on develop and on the head: pins, not red-first. **Gate 393's G1, G4, G5 mutants each kill their pin** (Q6: M6 = G1 shape kills `G1 DELETE …` plus the four R2s; G4 and G5 each kill exactly their G4/G5 cell).
- **Q5 THE CAPABILITY PREMISE: holds.**
  - I grepped the whole repo (frontends, mobile, sdk, scripts, connectors, systemTest, tests, services, docs).
  - `admin/privacy`: 12 hits, all in the PR's own files or the static `/admin/privacy-policy` link.
  - `admin/pricing`: 20 hits; outside the PR only `originate/src/index.ts:195-197` (endpoint list) and three docs (Comprehensive-Test-Report:316 "Requires SYSTEM_ADMIN role (correct)", Development-Summary, the System-Administrator stakeholder guide). The guide is for a system administrator, so it is consistent with the rule.
  - Control: `admin/organizations` 79 (5 in `frontend/admin/src/services/api.ts`).
  - **No non-platform caller; the PR removes no working capability.**
- **Q6 MUTANTS** (on the merged state; 20 files, 373 cells; tsc 0 for every mutant; the product file restored and sha256-checked after each; evidence/mutants.out, mutants_g394.json, mut/):

  | mutant | failed | killed by |
  |---|---|---|
  | BASE | 0 / 373 | |
  | M1 PUT guard removed | 6 | R1, R2 PUT, R3 x3, R6 PUT |
  | M2 PATCH guard removed | 6 | R2 PATCH, R4, R5 x3, R6 PATCH |
  | M3 PUT guard after the policy loop | 2 | R1, R2 PUT |
  | M4 PATCH guard after the body checks | 3 | R5 x3 |
  | M5 / M11 wrong warning label (PUT / GET pricing) | 1 / 1 | R6 PUT / R6 GET /pricing |
  | M6 org-less ORG_ADMIN admitted (G1 shape) | 5 | R2 x4 + the G1 pin |
  | M7 PUT return dropped | 6 | R1, R2, R3 x3, R6 |
  | M7b PATCH return dropped | 6 | R2, R4, R5 x3, R6 |
  | M8 ORG_ADMIN admitted by the predicate | 30 | 18 ks2308 + 12 ks2302 |
  | M9 GET /privacy guard deleted (`void req`) | 3 | R2, R6, R7 |
  | M10 GET /pricing guard deleted (`void req`) | 3 | R2, R6, R8 |
  | G4 / G5 (gate 393's) | 1 / 1 | the G4 / G5 pin |
  | N1 GET /privacy guard after the SELECTs | 2 | R2, R7 |
  | N2 / N3 GET return dropped (pricing / privacy) | 3 / 3 | R2, R6, R8 / R2, R6, R7 |
  | N4 refusal message differs | 23 | 14 ks2308 + 9 ks2302 |
  | **N5 GET /privacy guard skipped with a query string** | **0** | **survivor: G394-2270-3** |
  | **N6 PATCH guard only for lower-case event types** | **0** | **survivor: G394-2270-3** |

  Every builder row I re-ran (M1-M11, M7b, G4, G5) is killed as the PR's table states, by the cells it names. My first M3 spelling had a non-unique anchor (the script asserted before writing and stopped); it was re-spelled, a dry pass checked all 20 anchors, and the whole set was re-run.
- **Q7 WHOLE:**
  - Originate suite (default jest config, `--json`): develop **2910/2910 in 236 files**, head **2965/2965 in 237 files** (+55 = 52 + 3). Failure-name sets equal (both empty); no failed suite on either arm.
  - tsc 0 (planted: rc 2, 1 error).
  - eslint `--max-warnings 0` on adminConfig.ts and both test files: rc 0; adminConfig.ts on develop: rc 0 (planted: rc 1).
  - check.cjs services/originate: 331 examined, 270 under `__tests__`, 0 baseline, 0 new, 0 stale (planted: 1 new, rc 1).
  - Fragments: OK (planted two-h2: FAIL).
  - check:openapi: CHECK PASS. I did not re-grep the openapi zero: gate 393 proved originate.openapi.ts has 0 `/api/admin` routes with its control, and this PR touches no spec or yaml.
  - Overlap: 19 open PRs (18 others + this one); none touches any of the 5 paths, none touches adminConfig.ts or the ks2302 file (control: package-lock.json in 11). No file list is truncated (changedFiles = listed for all 19).
  - merge-tree onto live develop: **rc 0** (tree = head tree). Planted control: local commit 1b65966b8e06 on develop rewriting the GET /pricing handler line, never pushed: **rc 1**, CONFLICT (content) in adminConfig.ts.
  - Not re-run: the standalone 6-service ratchet and its leg test.
- **Q8 WORDS:**
  - PR body: summary, rule, red 18/34, green 52/31, the mutant table, suite figures (2910/236, 2965/237), 331/270, the caller census and the overlap all reproduce. Exceptions: G394-2270-4.1 ("any letter case") and G394-2270-1 ("reload only").
  - "None of the three tables … is in migration 039's row-level-security list": holds (0 hits in 039; 001_initial-schema creates all three).
  - Residuals:
    - R1 is accurate as a routing note, but it omits the `/api/gdpr/consent` door (G394-2270-2).
    - R2 and R3 are honest (the sweep code read agrees: `enforceRetentionImpl` selects `auto_delete = true` only, and anonymises audit_logs/system_errors only when `deletion_method === 'anonymize'`, so 'hard' stops the stripping and `autoDelete:false` stops the deletion, as the ticket says).
    - R4 is accurate.
  - NOT run is honest, and Node 26 is disclosed. Push timings are the builder's and UNMEASURED beyond ls-remote.
  - KS-2308 (read-only): In Progress, priority 2, created 2026-11-20 06:49:51Z. Every measurable line holds except "(reload only)" (G394-2270-1); the title's consent-read clause is closed only for the bulk listing (G394-2270-2).
  - Facts comment 6b5618fb (2,775 B; updatedAt .367Z is not after createdAt .378Z, so it is unedited): holds except G394-2270-4.1.

## Two-NO-GO cap
Not engaged.

## Fault, disclosed
I printed my own probe-c JSONL (develop arm) through `cut -c1-220`, against the commission's "never read long lines through `cut -c`". It is gate-generated evidence, not mail; the values I rely on were re-read whole with python (status, sql, scope). Nothing else outside the limits.

## Not run
- The four platform suites, a booted originate or gateway (the `/api/admin/` forward is a code read; gate 393's probe b on the unchanged verifier is cited, not re-run), a real Postgres or RLS, the retention sweep, any deployed environment, Node 24.
- The standalone 6-service ratchet and its leg test; the openapi zero re-grep (no spec path touched).
