PR 2294: GO WITH NOTES (at head 604f8ff60f8c73be25c8a9bd941da026fcfddc3b; tier 1)

QA GATE 418, tier 1 (Opus, claude-opus-5-5). Findings only: nothing fixed, pushed, commented or mailed. Started 10:19:22 AEDT, verdict written 10:31 to 10:35 AEDT (times from `date`).
Re-read at start (gh as kksecura, read-only, 10:20:07, and again at 10:31:21): PR 2294 open, 1 commit, head 604f8ff60f8c, base develop e3e79b7317f1 (unmoved), 8 files +670 -7, the same 8 paths Wednesday listed.

## BLUF

- **No Blocker. No Major.** The change does what Kam ruled (option a).
  - A platform admin (SYSTEM_ADMIN or SUPER_ADMIN, any ASCII case) may act for any organisation.
  - ORG_ADMIN and ISSUER_ADMIN (any ASCII case) may act only where their users ROW organisation equals the target's.
  - Every other role, a Unicode spoof, an array role, an empty role and no role is refused before any lookup.
- **No bypass found.** I attacked:
  - the body organisation, the nominee, a stale token claim, an absent row, an org-less row and a non-UUID caller id;
  - another organisation's id, an absent id and a malformed id;
  - tenant headers and override;
  - path spellings: case, /api/v1, a trailing slash, trailing segments, an encoded slash, dot segments;
  - other methods and sub-paths;
  - chunked and oversize bodies.

  Each one either held or answered at the gateway with nothing forwarded.
- **The chain proof nobody had run now exists.** It is a socket proof of the REAL gateway app in front of the REAL originate signatoriesRouter, with originate's REAL authenticate (RS256), its real provenance middleware and its real tenant resolution.
  - Only originate's db and logger were replaced (a recorder).
  - 36 of 36 cells passed. Details under G418-1.
- **Every builder figure I re-derived matched.**
  - originate: 3610/3610 on develop, 3738/3738 on the head.
  - api-gateway: 2401/2401 on develop, 2531/2531 on the head.
  - packages/shared: 1746/1747 on both arms, the single failure KS-278 wallet-signature on both.
  - check:test-types: 15 baseline errors, 0 new, on both arms.
  - tsc: 0 errors in both services on both arms.
  - eslint on the 8 files: 0 errors; 4 warnings in proxy.ts on both arms (all no-unused-vars, pre-existing).
- **Mutants: 16 of 16 killed, each by a named cell.** 7 were the builder's, re-derived by me. 9 were my own, 4 of them aimed at the coupled test edits.
- **Notes for the follow-up list. None of them blocks the merge.**

## Findings

### G418-1 (Note): what the chain proof measured, and what it did not
- **FOUND:** No single run had reached gateway, then originate, then a database (the builder's READY says so).
- **TESTED:** `_work/tools/g418-probe.test.ts`, run from a separate worktree (`_work/chain`, at the head), then moved out of it; that tree's porcelain is 0. Log: `_work/out/probe1.log`, rc 0, 36/36.
- **HOW:** the vitest test boots the real gateway `index.ts` app over loopback. The upstream is an express app that mounts:
  - originate's `createGatewayProvenanceMiddleware`;
  - `resolveRequestTenantId`;
  - `express.json`;
  - the real `signatoriesRouter`, whose real `authenticate()` verifies the gateway-forwarded RS256 token.

  The db is a recorder holding USERS and SIGS tables, tenant-aware, and it applies the UPDATE's organisation scope. Results:
  - C1: SUPER_ADMIN nominate for B gives 201 with 1 INSERT, vouched, with the token's tenant.
  - C2: ORG_ADMIN(A) for B gives 403 ORG_REFUSAL, relayed, with 0 writes.
  - C3: ORG_ADMIN(A) for A gives 201.
  - C4: a token claiming B over a row saying A gives 403.
  - C5: revoke as ORG_ADMIN(A):
    - SIG_B: 403;
    - ABSENT: 403 with the same body;
    - not-a-uuid: 400 at the gateway, 0 forwards;
    - SIG_A: 200, and the UPDATE's scope is A.
  - C6: `Issuer_Admin` reinstates its own signatory (200), and B's is refused (403).
  - C7: an org-less ORG_ADMIN gets 403 on all three.
  - C8: a platform admin keeps 404 on an absent id, and system_admin revokes B's signatory with a NULL scope.
  - C9: these roles are refused at the gateway with 0 forwards and 0 writes:
    - 403: OWNER, VERIFIER, ISSUER_APPROVER, connector, admin, ADMIN, platform_admin, PLATFORM_ADMIN;
    - 401: `["SYSTEM_ADMIN"]`, the U+0131 and U+017F spoofs, and the empty role.
  - C10: a token with no role claim gets 401.
  - C11: an ORG_ADMIN that sends x-tenant-id or x-tenant-override is still forwarded with the token's tenant, and originate reads that tenant.
  - C12: a SUPER_ADMIN override reaches originate as the override tenant (built behaviour).
- **Controls:** C1, C3, C5, C6 and C8 prove the recorder and the router were reached and writes do happen, so the 0-write cells can fail.
- **NOT measured:** a real Postgres, Prisma's typed parameter binding (`${null}::uuid IS NULL`), RLS (the builder's `rls_probe_branch.txt` was not re-run by me), and multi-tenant mode. Prisma's client is not generated in any donor tree, so it was not cheap.

### G418-2 (Note): the org-scope race is closed by the UPDATE's WHERE, but only a SQL-text cell pins it
- **FOUND:** revoke and reinstate check the signatory row's organisation, then UPDATE with `AND (${gate.orgScope}::uuid IS NULL OR organization_id = ${gate.orgScope}::uuid)` (signatories.ts:520 and :586). That closes the window between the SELECT and the UPDATE: a row moved out of the caller's organisation updates 0 rows and gets the built 404.
- **TESTED:** I reproduced mutant B-M12a. With the clause removed, exactly 2 cells fail, and both are the structural ones ("UPDATE carries its own organisation in the WHERE", a regex on the SQL text).
- **HOW:** No behavioural cell can see the race: the mock never moves a row between the two statements.
- **Severity:** Note. The SQL is correct by reading, and the builder's RLS replay measured 0 rows for another organisation and 1 for its own. Not re-run by me.

### G418-3 (Note): the nominee is not bound to the organisation (LISTED, ruled not built)
- **FOUND:** nominate judges only the BODY's organizationId (signatories.ts:157). An ORG_ADMIN of A can name any userId, a user of B or of another tenant, as A's signatory.
- **Severity:** It does not let A act for B: the row is A's. It is the "nominee's organisation" item Wednesday ruled LISTED. Cell "RED nominate: an ORG_ADMIN naming ANOTHER organisation for ITSELF" pins the body organisation as the thing judged, and B-M4 (judge the nominee instead) is killed by 10 cells.
- **Disposition:** Follow-up only.

### G418-4 (Note): refusal shape: no existence oracle for a bound admin; three answers differ by design
- **FOUND:** For a bound caller, another organisation's id, an absent id and a malformed id all get the same 403 ORG_REFUSAL at originate (measured directly and through the chain, C5). G-d, a mutant that let an absent id through to the UPDATE (so 404), is killed.
- **Three differences, none of which reveals existence outside the caller's organisation:**
  1. At the gateway a malformed :id is a 400 before originate (a syntactic answer).
  2. Its own organisation's signatory in the wrong state gets the built 404 ("not found or already revoked"); that state is its own organisation's.
  3. The gateway's role 403 body (`Admin access required`) differs from originate's ROLE_REFUSAL. Both are fixed strings.
- **Leaks:** No error text carries an organisation or user id. The ids appear only in logger lines (warn: role and route; info: ids), never in a response.
- **Platform 404:** kept (C8, and twin cells on both arms).

### G418-5 (Note): the 1mb raw-stream cap drains the whole body before the 413
- **FOUND:** `readSignatoryBody` (proxy.ts:767) stops keeping chunks past 1mb but keeps reading until 'end', then answers 413. It does not reject early on a declared Content-Length.
- **TESTED:**
  - B5: an 8mb body gets 413 in 17 ms on loopback, 0 forwards.
  - B2: a chunked body of cap+1 gets 413, not forwarded.
  - B1: a chunked body under the cap is forwarded once.
  - B3: a declared 2mb body held open after 1mb+100 bytes gets no answer for 3 s.
  - Control B4: the same held-open body on the gateway-PARSED path /api/workflows behaves the same (no answer in 3 s).
- **Severity:** This is parity with the existing parser path, not a regression. Low exposure; Note.
- **Other body checks:**
  - B6: text/plain gets 415 at the gateway, 0 forwards.
  - The gateway's boundedJson structural caps do not run on this raw path. Originate's own `boundedJson` (10mb) and `rejectNulBytes()` do, as for every proxied path.

### G418-6 (Note): an unchanged nominate body organisation reaches a `::uuid` cast for a platform admin
- **FOUND:** a platform admin's non-UUID `organizationId` reaches `${organizationId}::uuid` (signatories.ts:174) and gets the generic 500. That is the develop behaviour, and it is the LISTED "nominate's UUID validation".
- **Unchanged but cleared:** a bound admin's comparison folds with the shared `normaliseOrgId` (trim plus lowercase). I checked that no folded string can equal a canonical uuid while casting to a different one: a brace or unhyphenated spelling does not normalise to the canonical form, so it is refused.

### G418-7 (Note): the coupled test edits still test what their names say
- **ks1868 x2:** the edit adds `role: 'SYSTEM_ADMIN'` so the cell passes the new gate with no users read and still reaches the database throw.
  - G-e1 (the revoke catch reads `String(error)` unguarded) is killed: 2 of 12 cells fail in ks1868-signatories-write-routes-p2.
  - G-e2 (the same in the nominate catch) is killed: 2 of 5 cells fail in the o77p2 file.
  - So the added gate did not disarm them (the 2026-09-20 early-return lesson: checked).
- **ks955:** G-h (drop the vouch on the signatory forward) is killed by ks955 alone: 3 of 13 cells fail.
- **ks1240b:** G-f (drop the forward's AbortSignal) is killed by ks1240b alone: 5 of 37 fail, the census and the three "stalled body" forwards.

### G418-8 (Note): ASCII case variants of the two organisation roles are admitted (as ruled)
- **What is admitted:** `org_admin` and `Issuer_Admin` pass both layers: through `isPlatformOrOrgBoundedRole`, then bounded by membership (C6 measured `Issuer_Admin`).
- **Ruled:** Wednesday's ANSWER item 3.
- **Unmeasured:** whether any real token carries such a spelling.

## Guards, before and after (each passes on both arms; files and counts identical)

| Guard | develop | head |
|---|---|---|
| packages/shared ks1536-one-role-vocabulary | 99/99 | 99/99 |
| packages/shared ks1701-no-hand-written-platform-comparisons (G1/G2) | 4/4 | 4/4 |
| packages/shared ks781-p3-3-body-parser-order (LEG F: proxy.ts `{ routes: 1, guarded: 'none' }`, line 2343, unchanged) | 244/244 | 244/244 |
| api-gateway ks1536-gateway-role-checks-are-the-shared-predicates | 103/103 | 103/103 |
| api-gateway ks1701-workflow-approval-override | 25/25 | 25/25 |
| api-gateway ks570-proxy-mount-auth | 18/18 | 18/18 |
| originate ks1701 / ks1536 x2 | 168, 34, 5 | 168, 34, 5 |

- **ks570 sees the new routes:** it walks `layer.route.stack`, and G-g (revoke route without `authenticateToken(true)`) is killed by ks570 ALONE ("every /api mount either requires auth or is public by design").
- **No new inline role list in product code:** the diff adds no role literal outside comments; both layers call the shared `isPlatformRole` and `isPlatformOrOrgBoundedRole`.
- **Unchanged files:** the ks1536 baseline json is not in the diff.

## Mutants (own runner `_work/tools/mutants.py`, each plant matched exactly once, restored by bytes and sha256, probe tree porcelain 0 after)

| Id | Plant | Result |
|---|---|---|
| B-M1 | membership check deleted | KILLED 28/128 |
| B-M3 | caller organisation from the token claim | KILLED 35/128 (the builder's v1 died of compile; v2 and this run both killed) |
| B-M4 | judge the nominee's organisation | KILLED 10/128 |
| B-M12a | revoke UPDATE without the organisation scope | KILLED 2/128 (structural only, G418-2) |
| B-M13 | allow when both organisations are absent | KILLED 10/128 |
| B-M14b | gateway UUID check and encoding removed | KILLED 12/115 |
| B-M15 | gateway cap removed | KILLED 2/115 |
| G-a | comparison without the shared fold | KILLED 2/128 |
| G-b | gateway gate drops ISSUER_ADMIN (`isPlatformOrOrgAdminRole`) | KILLED 3/115 |
| G-c | cap off by one (exactly 1mb refused) | KILLED 1/115 |
| G-d | absent id let through to the UPDATE (the oracle) | KILLED 2/128 |
| G-e1 / G-e2 | ks1868 catch disarm | KILLED 2/12, 2/5 |
| G-f | ks1240b loses the signal | KILLED 5/37 |
| G-g | ks570 alone, no auth on revoke | KILLED 1/18 |
| G-h | ks955 alone, no vouch | KILLED 3/13 |

Survivors: none.

**Static-leg planted controls** (`_work/tools/controls.py`). Each leg went red with its plant and green after the restore:

| Leg | Before | Planted | After |
|---|---|---|---|
| tsc originate | 0 | 2 | 0 |
| tsc api-gateway | 0 | 2 | 0 |
| eslint originate | 0 errors | 2 errors | 0 errors |
| eslint api-gateway | 0 errors | 2 errors | 0 errors |
| ratchet api-gateway | rc 0 | rc 1 | rc 0 |

## Conformance table (derived from the code at the head, signatories.ts:78-127, proxy.ts:755-811; confirmed by cells or the chain)

Gateway column: F = forwarded, 403/401 = answered at the gateway. The originate column applies to nominate, revoke and reinstate alike: the target is the body organisation for nominate and the signatory row's organisation for revoke and reinstate.

| Caller | Gateway | Originate (all three) |
|---|---|---|
| SYSTEM_ADMIN, SUPER_ADMIN, system_admin, Super_Admin | F | allow, any organisation; NULL scope; absent id 404 |
| ORG_ADMIN, own organisation (row) | F | allow; UPDATE scoped to its organisation |
| ORG_ADMIN, other organisation / absent id / malformed id | F (a malformed :id gets 400 at the gateway) | 403 ORG_REFUSAL, 0 writes |
| ORG_ADMIN, no organisation on its row | F | 403 ORG_REFUSAL, no signatory read |
| ORG_ADMIN, no users row / non-UUID userId | F | 403 ORG_REFUSAL |
| ORG_ADMIN, token says B, row says A | F | the row decides (A only) |
| ISSUER_ADMIN, Issuer_Admin, org_admin: own / other | F | allow / 403 ORG_REFUSAL |
| ISSUER_APPROVER, OWNER, VERIFIER, connector (API key or token), admin, ADMIN, platform_admin, PLATFORM_ADMIN | 403 | 403 ROLE_REFUSAL, 0 lookups |
| U+0131 / U+017F spoofs, array role, empty role, no role | 401 (authenticateToken) | 403 ROLE_REFUSAL, 0 lookups |
| unauthenticated | 401 | 401 |

- **No admin acts outside its own organisation, and no non-admin acts at all.** Blocker count: 0.

Reachability through the gateway (SYSTEM_ADMIN, 0 forwards each):
- **404, nothing forwarded:**
  - PATCH, PUT, DELETE and GET on /:id;
  - GET /:id/history and GET /check;
  - POST /:id, /:id/approve, /:id/revoke/extra and /check;
  - PATCH /:id/revoke;
  - /%2e%2e/revoke.
- **400:** /:id%2Frevoke/revoke.
- **Spellings of the ruled routes (trailing slash, upper case, /api/v1, /API/V1):** forwarded to the canonical originate path, and each is gated (anon 401, OWNER 403, 0 forwards).
- **The list GET:** forwarded as before.

## Not tested (by anyone)

- **No real database behind the chain:** a real Postgres, RLS policy 039 and Prisma's typed binding were not run; the builder's PREPARE replay was not re-run by me.
- **Multi-tenant mode** (`MULTI_TENANCY_ENABLED`, a `req.db` tenant pool, whether `users` lives in that pool).
- **Real tokens:** whether any real token carries a case-variant organisation role.
- **No live stack:** no Schemathesis, Akto, Playwright or k6.
- **The connector principal:** the API-key path at the gateway was read in code (`role: 'connector'`, refused by the coarse gate), not driven with a validated key.
- **The PR body and the KS-2339 facts comment** were not audited sentence by sentence (not asked by this commission).
- **LISTED by the builder, outside this gate:** ApprovalQueue, PATCH /:id and the reads at originate (authenticated only; the gateway does not route them), the nominee's organisation, the platform tenant write, revoked_by, nominate UUID validation, issuer page T7, admin/create's uncapped read, and the yaml.

## Housekeeping

- **Trees:** under `_work/`: repo (clone), head, dev, probe, chain (worktrees, porcelain 0 each; node_modules cloned by `cp -c` from s-w75-base after a blob-equal check of the 8 package manifests and locks).
- **Containers:** none started; s-w75-rls untouched.
- **Outputs:** `_work/out/`.
