PR 2273: GO WITH NOTES (at head 8f7c7bd90167595af462a62b0ce8055d5ed0fff5; tier 1)

# Gate 397, tier 1 (Opus), PR 2273 (KS-2310 + KS-2311), 2026-11-22 ~18:10-18:23 AEDT

## Pins
- **Pinned twice, at 18:10:23 and 18:22:54**, by git ls-remote (through the Secuura project's gh credential helper, read-only) and gh pr view. Same values both times:
  - PR 2273 OPEN, not draft, MERGEABLE, head 8f7c7bd90167, ONE commit, parent = develop 302361a30209. 10 files, +591 -6, tree b91eb6fcb9d7. updatedAt 07:07:43Z (not changed since the READY).
  - develop = 302361a30209334ad6f6fbfbab3082984fde2342. PR 2272 head = fd178433fc4f (OPEN, one commit on the same develop).
- **Merged state = the head.** `git merge-tree --write-tree origin/develop pr/2273` gives rc 0, and the tree is the head's own tree b91eb6fcb9d7.

## How I measured
- My own clone `_work/g` from GitHub (`--reference-if-able` gate 395's clone, `--dissociate`). Worktrees:
  - `h` = head (suite, static);
  - `x` = head (probe h, mutants);
  - `d` = develop (suite, red-first, probe h baseline).
- node_modules and `packages/shared/dist` were APFS-cloned from gate 395's `h`. Develop's tree equals gate 395's head 4cec1424 (diff empty), and the PR changes no package.json, lockfile or `packages/` file (diff rc 0).
- Node v26.8.1 (not LTS), jest, TMPDIR /private/tmp/g397t.
- Scripts are in `_work/`:
  - `setup_g397.sh`, `run_cwd_g397.py`, `suites_g397.sh`, `redfirst_g397.py`, `probe_run_g397.py`, `an_h.py`;
  - `mutants_g397.py`: the builder's engine, read-only copy, re-pointed at my `x`, with six extra mutants E1-E6 of mine;
  - `pglite_g397.mjs` (my own; it reads the statement from the head's gdprService.ts and the policy from migration 039);
  - `static_g397.py`, `mt_g397.py`;
  - `lin_read_g397.py` (read-only GraphQL; the key is read into memory from the Secuura credentials file and never printed).
- **Probe h** (`_work/probes/g397-probe-h.test.ts`, findings-only, asserts nothing). It is gate 395's probe e shape, extended.
  - Real parts: gdprRouter, `db.ts` (single-tenant GUC wrapper), `tenantGucContext`, requireRole / hasAnyRole, and the real `createDSR` and `getPendingDSRs` (with a stand-in DEK store).
  - Stand-ins: authenticate (caller from headers), and `@prisma/client` (it records every statement with the GUC of its transaction).
  - Simulated RLS: `users` answers with the GUC tenant's rows only (all rows under the bypass). `data_subject_requests` has no RLS, so the list join is evaluated with the users rows visible under the scope.
  - 19 callers x 19 subject spellings x 2 body shapes = 722 POSTs, plus 19 list calls. Run on the head in normal and throw-every-query modes, and on develop.
  - Every probe copy run inside a worktree was moved to `_work/_quarantine/` after use.
- **End state:**
  - h, x and d have 0 porcelain lines.
  - x's gdpr.ts and gdprService.ts sha256 equal h's (c594072e…, abc5e6b4…).
  - Docker: no container or volume named g397 (0 of 106 container names; 0 volumes). I used no container.
  - Not touched: no seat tree, no `!CODING` write, no GitHub or Linear write, no database server, no mail, no launch, no `cd`, no `rm`.

## Findings

No HIGH and no MEDIUM finding. Both bounds hold as ruled. I measured them through the real db wrapper, the real tenant context and the real service statements.

### LOW
**G397-2273-1: "the CALLER is recorded" is not pinned against a body-supplied actor (one surviving mutant).**
- Mutant E1 lets a body `actorId` win over the caller. It survived all 433 cells (0 failed): no cell sends an extra body field.
- The head itself ignores such fields. In probe h, every one of the 361 caller x subject pairs gave an identical status, insert count, actor and subject with and without `{actorId, organizationId, tenantId}` in the body. So this is a coverage gap, not a defect.
- Fix shape, if wanted: one F6 row with `actorId` in the body.

**G397-2273-2: N4 (null equals null) is killed only by statement text; my PGlite run kills it on rows; one table row names an equivalent mutant.**
- **N4 (`IS NOT DISTINCT FROM`):** killed by S3's regex only (1 failed), as the PR says. My PGlite run gives the behavioural kill: a no-organisation ORG_ADMIN then gets `noorg-pending` and `noorg-admin-self`, under both no RLS and the 039 policy.
- **"`IS NOT NULL` dropped" (my E4)**, which the PR's N4 row also names, is SQL-equivalent. On PGlite it returns identical rows to the head's statement in every case, because `NULL = x` is never true. Only the text pin (S3) can kill it. It is harmless.
- These are words, not a gap.

**G397-2273-3: the list's tenant separation rests on `users` RLS. This is the stated residual, reproduced.**
- PGlite, no RLS: an organisation-B admin of T1 also gets T2's same-organisation-id request, under any scope.
- PGlite, migration 039's policy (ENABLE + FORCE) as a non-superuser, non-BYPASSRLS role:
  - T1 scope: only the three T1 rows;
  - T2 scope or no scope: nothing;
  - bypass: all four.
- PGlite, superuser control: all four. This shows the policy is what removes T2's row.
- Practical weight is low: organisation ids are UUIDs, and two tenants sharing one needs a shared organisation id. A deployed Postgres stays unrun (R4).

**G397-2273-4: words.**
1. PR body and the KS-2311 comment: "every real caller carries one [user id]". Not measured by me. It is the basis of the residual "a platform caller without a user id would record the subject", which I reproduced in probe h: SYSTEM_ADMIN with no userId gives actor = subject.
2. "Overlap: 18 open PRs". That held in the push run. Now there are 19 others: PR 2272 opened at 06:48:29Z, inside the push window. Its 5 paths are disjoint from these 10.
3. The stale-spec residual is accurate, and it is wider than stated. The `/dsr/pending` 403 response is still described as "Insufficient role (production only)" (originate.openapi.ts:3444), not only the description line. No status change is needed.

### Info (not findings)
- **The audit actor is the token's `userId` string, verbatim.** An upper-case caller id is recorded upper-case. Tokens carry canonical ids.
- **A caller filing for itself must spell its own id exactly as its token does.** An upper-case own id from a non-ORG_ADMIN gets the 403. This fails closed, and it is KS-2309's self rule unchanged.

## The commission's questions
- **Q1 THE BOUND on POST /dsr: holds.** (probe h head; develop baseline: every one of the 19 callers got 201 for other-organisation, other-tenant, absent and no-organisation subjects, with actor = the subject)
  - **Refused:** VERIFIER, OWNER, ISSUER_ADMIN and role-less callers get 201 only for self. Every other UUID-shaped subject gets 403 with no INSERT and no users lookup.
  - **ORG_ADMIN of org B is admitted** for self, own-organisation subjects (lower and upper case) and same-organisation colleagues. It is **refused (403, no INSERT)** in these cases:
    - another organisation (both cases);
    - no-organisation subject;
    - another tenant's user whose organisation id equals B;
    - absent subject.
  - **The claim never decides:** with claim = org A, the answers are identical to claim = org B.
  - **Other refused ORG_ADMIN shapes:**
    - caller row with no organisation, unknown caller row, non-UUID caller id, no userId: 403 for every non-self subject;
    - role spelt `org_admin`, or ORG_ADMIN only inside a `roles[]` array: treated as non-admin, 403 for others (fails closed).
  - **Platform:** SYSTEM_ADMIN, SUPER_ADMIN and super_admin get 201 for anyone.
  - **Shapes that do not slip through:**
    - array, object or number userId: 400 (zod `z.string()`);
    - braced, hyphenless, trailing newline, leading space, `urn:uuid:`, malformed: 404 for everyone;
    - extra body fields: no effect;
    - a userId that passes UUID_PATTERN but is not canonical: only the case varies, and the lookup lower-cases.
  - **Scope:** every users lookup ran in one transaction with `app.current_tenant_id` = the request tenant, never the bypass (0 exceptions). An ORG_ADMIN whose request tenant is T2 is refused for its own T1 colleagues.
- **Q2 ORDER and NO ORACLE: holds.**
  - Malformed ids give 404 for every caller with 0 lookups (C2 reproduced in the suite; probe h: 6 spellings x 19 callers).
  - For the ORG_ADMIN, every UUID-shaped refusal (other org x2, no org, other tenant, absent) is byte-identical: 403, content-length 92, the KS-2309 body. Each costs exactly ONE users lookup. Absent and present do the same work.
  - Non-admin refusals cost 0 lookups whatever the subject.
  - G395-2271-3's shape does not arise here, because there is no pre-read keyed on the subject. Confirmed.
  - Throw-every-query mode: the ORG_ADMIN gets 500 or 403, with no INSERT for any non-self subject. It fails closed.
- **Q3 THE ACTOR: holds.**
  - The INSERT's audit_trail actor is the caller for self, for the ORG_ADMIN on its own organisation and for platform callers on another user (probe h, real `createDSR`). On develop it was always the subject.
  - Connector erasure: `executeErasureByExternalRef` (gdprService.ts:1552) still calls `createDSR` with four arguments, so the default `actorId = userId` keeps the subject. M7 is killed by S2.
  - Encryption: the `writePii` lines (AAD `data_subject_requests.email|notes.${userId}.${type}`, key = the subject's DEK) are context lines in the diff, unchanged.
  - Readers of `audit_trail[0].actor`: none outside the service. The repo-wide grep for auditTrail / audit_trail found only gdprService's own writes and maps, the OpenAPI schema and thirdPartyVerifiers (a different table). The admin SystemHealth page reads no actor.
  - PR 2099's gdprService.ts hunk (+11, executeErasureImpl) touches no createDSR, actor or audit line (0 matches; control: 13 changed lines).
- **Q4 THE LIST: holds as ruled** (probe h through the real `getPendingDSRs` and the real db.ts, plus PGlite):
  - ORG_ADMIN of B in T1: own pending, own processing and its own self request. Never completed, organisation A, no-organisation or T2's same-organisation-id rows.
  - The claim does not change it. Upper-case caller id: same rows.
  - Request tenant T2: [] (the caller row is invisible). No-organisation row: []. Unknown row: [].
  - Non-UUID id or no userId: [] with 0 statements.
  - T2's own ORG_ADMIN of B gets only T2's row.
  - Platform spellings get all six open rows, with today's statement.
  - Every statement ran in-transaction under the request tenant, never the bypass. A DB error gives 200 [] (the catch is pre-existing; it fails closed).
  - Role gate: VERIFIER, OWNER, ISSUER_ADMIN and role-less get requireRole's 403.
  - PGlite is described under G397-2273-3. It covers the statement's rows and the 039 policy text on `users` as a non-superuser role. It does NOT cover the deployed database, its role's BYPASSRLS / ownership, or the MULTI_TENANCY pool path.
- **Q5 OTHER DOORS: none new.**
  - The `data_subject_requests` table is reached outside tests only by originate's gdpr.ts / gdprService.ts. Other mentions: index.ts (a comment), the OpenAPI spec, migrations and init SQL, the operator script backfill-subject-deks.js, and the context strings in packages/shared encryptedField.ts. The positive control is the 10 files listed.
  - `createDSR` / `getPendingDSRs` / `dsr/pending` callers: the route, the connector erasure, and the admin SystemHealth.tsx:99 (display). No frontend posts to `/api/gdpr/dsr`.
  - The api-gateway has no own route: its GDPR mentions are path normalisation, audit, and erasure-door tests.
  - e2e specs file only with `'self'`, a missing userId, `'test-user-id'` or `'ACCESS'`, so their outcomes are unchanged (404/400).
  - KS-1696 and KS-2230 were not re-filed.
- **Q6 THE CELLS: reproduced.**
  - Counts: router file 54, scope file 6, service file 6, plus 1 ks694 cell = 67.
  - Head suite: 3,152 of 3,152 in 241 files; develop: 3,085 of 3,085 in 238.
  - Per-test diff: 67 only on the head, 0 only on develop, 0 changed status.
  - **Red-first** (head's four files on develop's code, worktree d, then put back, porcelain 0): **100 run, 40 failed, 60 passed, 0 suites failed to run.**
    - Every failure is an assertion: 20 `403` vs `201`, 17 deep-equality on calls/args, 2 statement-regex, 1 call count.
    - The red set is exactly the designed one: F1-F7 = 30, L1-L4 = 4, P1b/P1d/P2a, S1/S3, and the ks694 cell.
  - **The scope cells are on the real module.** The scope file mocks only `@prisma/client`, `@prisma/adapter-pg`, events, subjectDeks, logger and authenticate. `../db` and `getPendingDSRs` are real. X1 and X1b are killed only by it (and by S3).
- **Q7 MUTANTS** (my run: x, 16 files, 433 cells; the no-mutant control has 0 failed and tsc 0; every file restored and sha256-checked):

  | mutant | failed | killed by |
  |---|---|---|
  | M1 POST check removed | 21 | F1-F5, F7, P1b |
  | M2 check after createDSR | 20 | F1-F5, P1b |
  | M3 ORG_ADMIN as platform on POST | 13 | F2-F5, F7, P1b |
  | M4 no actor passed | 11 | F6, P1d |
  | M5 subject as actor | 9 | F6, P1d |
  | M6 service ignores actor | 1 | S1 |
  | M7 connector default changed | 1 | S2 |
  | M8 check before the 404 | 2 | C2 |
  | N1 unfiltered list | 5 | L1-L3, P2a, ks694 |
  | N2 claim decides | 2 | L1, L2 |
  | N3 service ignores option | 2 | S3, P2a |
  | N4 IS NOT DISTINCT FROM | 1 | S3 (text only; PGlite kills it on rows) |
  | N5 platform filtered | 5+6 | P1 x3, P2b, ks694; ks1346b x6 |
  | N6 non-UUID caller queries | 1 | L4 |
  | X1 lookup under platform scope | 4 | P1a-P1d |
  | X1b list under platform scope | 2 | S3, P2a |
  | E2 caller joined on the subject row | 2 | S3, P2a |
  | E3 non-UUID caller gets the full list | 1 | L4 |
  | E4 IS NOT NULL dropped (equivalent) | 1 | S3 (text) |
  | E5 POST bound only for ORG_ADMIN | 8 | F1 |
  | E6 status filter dropped | 1 | S3 (text) |
  | **E1 body actorId wins** | **0** | **survivor: G397-2273-1** |

  21 of 22 compiling were killed; none failed to compile.
- **Q8 WHOLE:**
  - Suites as in Q6: failure sets equal, both empty.
  - tsc 0 (planted: rc 2, 1 error).
  - eslint `--max-warnings 0`: on the six files rc 0; on gdpr.ts and gdprService.ts at develop rc 0 (planted: rc 1).
  - check.cjs originate: 335 examined, 274 under `__tests__`, 0/0/0 (planted: 1 new, rc 1).
  - Fragments OK (planted: FAIL). check:openapi CHECK PASS.
  - Standalone ratchet: rc 1 on api-gateway ks815 TS2345 x2, **identical on develop** (a gap in this clone's install, as gate 395 recorded). The leg test is 45/48 for the same reason. The PR touches no api-gateway file. That leg is UNMEASURED here, not red against the PR.
  - **Overlap:** 20 open PRs (control: package-lock.json in 11; no file list near the cap). Only PR 2099 touches one of the 10 paths: gdprService.ts.
  - **merge-tree:**
    - vs PR 2099's head 8967de8b1755: rc 0, tree 2b2af1419fa0 (= the READY's);
    - vs develop + PR 2272 (fd178433fc4f): rc 0. PR 2272's 5 paths (adminConfig.ts, the ks2302 and ks2306 test files, two fragments) are disjoint from these 10;
    - planted controls (local commits, never pushed): getPendingDSRs' signature line rc 1, CONFLICT in gdprService.ts; the createDSR call line rc 1, CONFLICT in gdpr.ts.
- **Q9 WORDS:**
  - PR body: the summary, rule, census, figures (40/100, 60, 100/100, 3,085/238, 3,152/241, +67, 335/274, 10 paths +591 -6, mutant table) and the PGlite paragraph all reproduce. Exceptions: G397-2273-2 (the N4 row's second spelling is equivalent) and G397-2273-4.
  - ks445's four-argument claim holds (ks445 mocks hasAnyRole true with a user-less caller; line 168).
  - The waiver is stated honestly: "ignored (mine, named)" is explained as the tool's fixed label, and PR 2099 is named as KS-2060's.
  - Residuals are accurate (wider spec staleness: G397-2273-4.3).
  - NOT RUN is honest; Node 26 is disclosed.
  - KS-2310 / KS-2311 (read-only): both In Progress, priority 2, one comment each.
  - Facts comments 2e33d580 (2,656 B) and 1e6d2a5c (2,587 B): updatedAt is not after createdAt, so unedited. Every sentence I could check holds.

## Two-NO-GO cap
Not engaged.

## Faults, disclosed
- `an_h.py`'s first comparison of the plain vs extra-field bodies counted response bodies, which differ by timestamp, so it printed false mismatches. I re-compared on status, insert count, actor and subject: 0 mismatches.
- `mutants.out` captured only the last 90 lines in the task log. The full file is in `_work/evidence/mutants.out`.
- Two shell calls were refused by the fleet's hooks (a `cd` false positive on a variable path; a zsh `=` separator) and re-issued.
- I read no mail and used no `cut -c` on mail.

## Not run
- The four platform suites, a booted originate or gateway, a real Postgres with RLS (PGlite and simulated RLS only), the MULTI_TENANCY pool path, any deployed environment, Node 24.
- The api-gateway ratchet leg on a proper install.
- The suite on develop + PR 2272 (the paths are disjoint; merge-tree only).
