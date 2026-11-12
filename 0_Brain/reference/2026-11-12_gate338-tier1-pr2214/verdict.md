PR 2214: GO WITH NOTES (at head eb7315988de5; tier 1; round 1)

Gate 338, tier 1 (Opus), one session, 2026-11-12 09:03Z to 09:20Z (20:03 to 20:20 AEDT). Findings only: nothing fixed, posted, mailed, pushed, merged, or written to Linear, GitHub or a board.

Where things ran:
- Every write verb ran in my own clone `scratch/repo` (fresh `git clone --filter=blob:none`, sparse checkout as gate 334's `setup.sh`; `core.sshCommand` = the project deploy key). Fetch and merge-tree ran only there.
- `node_modules` and `packages/shared/dist`: read-only symlinks to gate 313's `r2` install (express 4.22.3, vitest 4.1.12, tsc 5.9.3), as gates 331/332/334 did. Control: r2's `packages/shared/src` blobs for `security/keyRevokePolicy.ts` (27ae85f6), `middleware/index.ts` (ccde0ce9), `crypto/jwks.ts` (28e3278f) and `index.ts` (d26ab548) are byte-equal to the PR head's.
- In the shared Secuura checkout I ran read verbs only (`git grep`, `rev-parse`, `GIT_OPTIONAL_LOCKS=0`), for the caller census (Q5).
- Every file I changed in the clone was restored and checked by blob: index.ts `9becd6065b3e` after every run (`scratch/whole.py` prints "restored … OK"), the ks2166 test `20c1364fa524`, the ks1931 test `6cff4e4ffd3e`. The two probe files were moved aside (`scratch/aside/zzprobe-gate338-{a,b}.test.ts.ran`). `git status` in the clone shows only the two symlinks.
- Vitest ran with `cwd` = the kyc package via python `subprocess` (`scratch/whole.py`). tsc ran by absolute path with `-p`. Nothing ran from the WEDNESDAY working directory.
- Machine: Node v26.8.1 (NOT the LTS line), macOS arm64. load1 was 12.5 at my start (09:03Z, before any run). I waited, and every suite run started with load1 between 3.1 and 5.1 (all under 8).
- No Spark row: the commission does not ask for one.

## Pins

| when | develop | refs/pull/2214/head |
|---|---|---|
| start, 09:03:55Z (`scratch/pins_start.txt`) | fa2d60ca8ceec35299bf934c9c8d2bf74a330c8d (= commission) | eb7315988de5c63cd6f9a1d96a89cb131b2643be (= commission) |
| end, 09:18:21Z (`scratch/pins_end.txt`) | **eab5ac6bff8ddb3f5e63264083ada73eb8405a4b (MOVED)** | unchanged |

**Develop moved during the gate.** The new commit is one squash, eab5ac6b "Refs KS-2182: tests/connectors moves from jest to Vitest". It touches 6 files: root `package.json` (the `test:connectors` script, and `vitest ^4.1.12` added as a root devDependency), `package-lock.json`, `tests/connectors/{jest.config.cjs → vitest.config.ts}` and two KS-2182 fragments. Nothing under `services/kyc` or `packages/shared` changed.
- `merge-tree --write-tree origin/develop(eab5ac6b) p2214`: rc 0, tree 05d734c3 (`out/merge_tree_end.txt`).
- develop to merged: exactly the PR's 10 files, +507 -9.
- head to merged: exactly develop's 6 files.
- This does not change any kyc measurement. I did not re-run the suite on the merged tree.

**Shape:** two commits on fa2d60ca:
- fe1587f5: the change, the ks849 repair, the four ks1868 repairs and the fragment pair;
- eb731598: the ks1931 repair, 3 lines added and 1 removed.

GraphQL: OPEN, not draft, base develop, headRefOid = pin, 2 commits, 10 files, +507 -9, closingIssuesReferences 0. Three-dot numstat equals the READY's list exactly.

## Summary

The owner rule is correct as ruled. I measured it against a wide range of hostile principals and identifiers, and every one either fails closed or is the subject's own id:
- the platform exception is admitted on the two reads only;
- a refusal costs no statement on list, DELETE and initiate, and exactly one lookup on GET /:id;
- a refused initiate writes no verification row and no consent row;
- the DELETE check runs before any delete.

I reproduced every READY figure:
- red-first 61/83;
- 83/83 for the new file at head;
- 177/177 for the whole suite;
- the ks1931 repair changes no assertion and is non-vacuous.

My 24 mutants: 21 killed and 2 survivors. M21 is equivalent.
- The survivors are an `x-user-id` fallback and a Unicode-folding role check. The code refuses both at head (probe), but no cell pins either (G338-2214-4).

A refresh token IS admitted as a bearer by kyc's `authenticate()`. It acts as its own subject only, so it does not get round this PR's check. It is pre-existing and outside this PR (G338-2214-2).

The PR body has the existence-oracle trade-off and is Refs-only. It is missing the tier-1 statement and the two named not-in-scope candidates (G338-2214-1).

No in-repo legitimate flow breaks.

No Major.

## Q1. Correctness, adversarially

Two probes. Raw rows: `out/probe_rows.json` and `out/probeB_rows.json`. Logs: `out/t_probeA.log` and `out/t_probeB.log`.
- **Probe A** (`scratch/probe/zzprobe-gate338-a.test.ts`) is the PR's own harness: an in-memory table, a real HTTP listener, and a stand-in `authenticate` that sets the principal named. It drives every principal against every route, and records status, statement count, DELETEs, consent rows and the table after.
- **Probe B** (`…-b.test.ts`) uses the same harness with the **real** shared `authenticate()`. `JWT_PUBLIC_KEY` is a fresh RSA key, JWKS is unset, and real RS256 tokens are signed.

**Role spellings** (caller = OTHER, subject = SUBJECT):

| caller's role | GET /:id | GET /user/:userId | DELETE | initiate |
|---|---|---|---|---|
| SYSTEM_ADMIN (control) | 200 | 200 | **403** | **403** |
| `system_admin`, `System_Admin` (ASCII fold) | 200 | 200 | 403 | 403 |
| ADMIN, ORG_ADMIN, ISSUER_ADMIN, OWNER, platform_admin | 403 | 403 | 403 | 403 |
| array `['SYSTEM_ADMIN']` or an object with `toString` | 403 | 403 | 403 | 403 |
| `SYSTEM_ADMıN` (U+0131) or `ſUPER_ADMIN` (U+017F) | 403 | 403 | 403 | 403 |
| fullwidth `ＳＹＳＴＥＭ_ＡＤＭＩＮ`, or `'SYSTEM_ADMIN '` with a trailing space | 403 | 403 | 403 | 403 |
| connector principal (`connector:api-key`) | 403 | 403 | 403 | 403 |

**Identity edges** (role OWNER, subject SUBJECT, on all four routes):
- **Admitted:** the claim is the subject in UPPER case. It is the same UUID, so this is the ruled ASCII fold.
- **Refused (403):**
  - a fullwidth `ａ` in the claim;
  - the subject with a trailing space;
  - the subject + `/`;
  - no `userId` but `sub` = subject;
  - no `userId` and an `x-user-id: <subject>` header;
  - a claim of OTHER plus an `x-user-id: <subject>` header;
  - `null`, an object with `toString`, or an empty principal `{}`.
- **Non-UUID subjects** on list and DELETE:
  - Kelvin `KYC-K-SUBJECT` (U+212A) against `kyc-k-subject`: refused in both directions.
  - fullwidth `ａbc` against `abc`: refused.
  - A `%2F` id `a/b` reaches the handler as `a/b`: the owner `a/b` is admitted, OTHER is refused.

**Paths** (caller OTHER):
- `%2D`-encoded dashes: 403, 0 statements.
- trailing slash on list, DELETE and /:id: 403.
- upper-case `/API/KYC/USER/…`: Express is case-insensitive, so it reaches the handler; 403, and the owner gets 200.
- `…/user/<OTHER>%2F..%2F<SUBJECT>`: 403.
- `//` doubled: 404 from kyc's catch-all.
- GET /:id with an upper-case record id: 404 (the stand-in keys `id` exactly; see the note under G338-2214-6).

**Record and body edges:**
- GET /:id record with `user_id` null: 403.
- Record stored upper case, owner's claim lower case: 200 (the owner).
- Missing record: 404.
- Initiate:
  - a fullwidth or array body userId, or no body userId: 400;
  - an extra `user_id: OTHER` key beside the body's `userId: SUBJECT`, with OTHER as caller: 403;
  - a non-subject with `consentGiven:false`: 403, not 400, as ruled;
  - an upper-case body userId from the lower-case owner: 201, and the row and the consent are stored UPPER (candidate b, G338-2214-3).

**Tokens, through the real `authenticate()`** (Probe B; list, GET /:id and DELETE each):

| token | result |
|---|---|
| access, `userId` = subject | 200 / 200 / 200 (3 DELETEs) |
| **REFRESH** (`type:'refresh'`, jti, 7d), `userId` = subject | **200 / 200 / 200 (3 DELETEs)**: admitted as a bearer |
| REFRESH, `userId` = OTHER | 403 / 403 / 403 |
| **REFRESH, role SYSTEM_ADMIN**, `userId` = OTHER | **200 / 200** / 403 |
| connector-type token (`connector:x`) | 403 ×3 |
| RS256, no `userId`, `sub` = subject | 403 ×3 |
| RS256, `userId` `""` or `42` | 403 ×3 |
| signed by another key, expired, `alg:none`, HS256 with the public key as secret, no header | 401 ×3 each |

**The refresh token, answered:** kyc's `authenticate()` admits it. `verifyJwtRs256` (`packages/shared/src/crypto/jwks.ts:243`) checks the signature, the algorithm and expiry, never `type`. auth signs both token types with the same key and the same `userId` (`services/auth/src/services/jwt.ts:186-235`), with lifetimes of 1h and 7d (`:43-44`).
- Reading only: the gateway's `authenticateToken` (`api-gateway/src/middleware/auth.ts:647-700`) refuses `type === 'connector'` but not `'refresh'`. It does run the session-active check on `sessionId`, which both types carry.
- For this PR: the refresh token is still keyed to its own user, so it gets through nothing the owner rule refuses. It is **not in scope** (a shared-verifier and gateway property). It is graded in G338-2214-2 because of what it lengthens: a 7-day bearer, and a 7-day platform read for a SYSTEM_ADMIN refresh token.

## Q2. Order

From the probe rows and the PR's own `expectRefusedAndInert`:
- **List, DELETE, initiate:** 0 statements on every refusal, across every row above.
- **GET /:id:** exactly 1 statement (`SELECT * FROM svc_kyc_verifications WHERE id = $1`), then 403.
- **Initiate:** a refusal writes neither a verification row (TABLE 0) nor a consent row (CONSENTS 0), including on `consentGiven:false`.
- **DELETE:**
  - every refusal: 0 DELETEs, and the seeded row survives.
  - The check is synchronous and sits before `await dbDeleteUserData`.
  - **M11** (check moved after the erase) is killed by 17 cells: status 403 still read, and the deletes assertion fails.
  - **M03** (check removed) is killed by 17.

## Q3. Reproduction

| run | load1 | files | tests | rc |
|---|---|---|---|---|
| head, whole kyc suite (`whole_head`) | 3.88 | 18 | **177 / 177** | 0 |
| red-first: head tests, develop's index.ts d08288dc (`redfirst_develop`) | 3.69 | 18 | 116 passed, **61 failed** | 1 |
| planted failing cell appended to ks2166 (`planted_cell`) | 3.59 | 1 | 83 passed, 1 failed (the planted cell) | 1 |

- **Red-first detail:**
  - The new file: 83 cells, 61 failed; every failing cell is RED-named; 0 RED-named cells passing; 0 non-RED cells failing.
  - Every other file: 94/94 (the 116 passes = 94 + 22).
  - This equals the READY.
- **The new file alone at head:** 83/83 (inside the 177; the file count in the JSON is 18).
- **tsc:**
  - `tsc --noEmit -p services/kyc/tsconfig.json`: rc 0, 0 lines.
  - With the tests (`scratch/tsc/tsconfig.tests.json`, gate 334's config with `declaration:false` for the symlinked install): rc 0, 0 lines, 18 test files listed.

**Mutants** (`scratch/mkmut.py`, `scratch/mut/*.ts`; whole kyc suite each, `out/mutants_summary.txt`, `out/mut_*.json`):

| mutant | failed | killed by |
|---|---|---|
| M01 GET /:id check removed | 14 | ks2166 |
| M02 list check removed | 14 | ks2166 |
| M03 DELETE check removed | 17 | ks2166 |
| M04 initiate check removed | 16 | ks2166 |
| **M05 platform exception widened to DELETE** (commission) | 3 | ks2166 A (the 3 platform spellings) |
| M06 exception widened to initiate | 3 | ks2166 A |
| M07 GET /:id exception off | 4 | ks2166 A + ks849 S3 |
| M08 list exception off | 3 | ks2166 A |
| **M09 `isPlatformOrOrgAdminRole` swap** (commission) | 2 | ks2166 ORG_ADMIN on the 2 reads |
| M10 `isPlatformOrOrgBoundedRole` swap | 4 | ks2166 ORG_ADMIN and ISSUER_ADMIN on the reads |
| M11 DELETE check after the erase | 17 | ks2166 |
| **M12 fold → `toLowerCase()`** (commission) | 3 | the 3 Kelvin cells |
| **M13 compare on the claim's `sub`** (commission) | 32 | ks2166, plus every repaired cell in ks849, ks1868 ×4 and ks1931 |
| M14 empty-id guard dropped | 1 | ks2166 I (empty against empty) |
| M15 no fold (strict compare) | 9 | the fold-admit cells |
| M16 `String()` coercion of non-strings | 4 | the array/numeric userId cells |
| M17 initiate check after the consent check | 1 | ks2166 R (403 not 400) |
| M18 list check after the read | 14 | ks2166 |
| **M19 caller falls back to the `x-user-id` header** | **0, SURVIVES** | none: no cell sends an `x-user-*` header |
| M20 GET /:id subject = the path id | 3 | ks2166 C/I |
| M21 initiate subject from the raw `req.body.userId` | 0, survives | **equivalent**: `.guid()` does not transform, so after a successful parse it is the same value |
| M22 403 message changed | 59 | ks2166 |
| **M23 platform check by `toUpperCase()` over the two names** | **0, SURVIVES** | none: no cell uses a U+0131 or U+017F role, though the code cites KS-1591 |
| M24 initiate 403 → 404 | 16 | ks2166 |

**On the READY's "18/18 killed":** the seat's 18 mutant files are not in the PR or in any gate-readable place, so I did not re-run them verbatim. My set covers every class the PR body lists, plus the commission's four (M05, M09, M12, M13, all killed). M19 and M23 are classes the seat's set did not include (G338-2214-4).

## Q4. The ks1931 repair

- **Assertions:**
  - The counted diff of lines beginning `expect(` over the 6 existing test files is **0**; on any `+`/`-` line anywhere it is also 0. The control on the new file is 34.
  - Per-file `expect(` totals are equal at develop and head: ks1868 ×4 12/12/17/12, ks1931 8, ks849 22.
  - The repair is exactly the stand-in `authenticate` now setting `req.user = { userId: USER_ID, role: 'OWNER' }`, plus a comment.
- **Non-vacuous:** I built `scratch/mut/M_no2211fix.ts` = the head index.ts with 2211's 3-hunk diff (cea1cdc2..c0e112d6) reverse-applied. It touches only `throwOnError` and the cascade's `true`.

| index.ts | ks1931 test | R1 | R2 | C1 | C2 |
|---|---|---|---|---|---|
| 2211 fix reverted | **repaired (head)** | **RED** | **RED** | pass | pass |
| 2211 fix reverted | unrepaired (develop's) | pass (**vacuous**) | pass (**vacuous**) | RED (403) | RED (403) |
| head | unrepaired | pass | pass | RED | RED |
| head | repaired | pass | pass | pass | pass |

The repair makes R1 and R2 fire again on a revert of 2211's fix. Without it they pass vacuously behind the 403. This matches the READY and body item 4.

## Q5. Callers (behaviour change: 200/201 → 403 for a non-subject, non-platform caller)

- **In-repo census** (`git grep` on develop as the shared checkout holds it, 0e6479d7, 2 days stale; every hit was re-read at p2214, blob-equal where checked). It covered the whole repository, not just `Blockchain/`. Patterns: `kyc/initiate`, `kyc/user`, `kyc/${`, `kyc/' +`, `kyc/" +`, `'/kyc'`, `kycApi`, `kycClient`, `KYC_SERVICE_URL`, `proxy('kyc'`.
  - **Positive control:** `kyc/microsoft/start` hits 11 files (the SDK, the issuer frontend, the e2e spec, the gateway).
  - The four routes have **no** caller in a frontend, service, SDK, connector, e2e spec or k6 script.
    - The SDK and the issuer UI call only `/api/kyc/microsoft/*` (untouched).
    - `KYC_SERVICE_URL` is used only by the gateway proxy and system-status.
    - The admin `kycApi` hit is a settings field `kycApiKey`.
  - **One caller outside `Blockchain/`, which the seat's census (scoped to `Blockchain/`) missed:** `systemTest/schemathesis/tests/test_workflows_lifecycle.py:185-218` (blob d292c712 at p2214).
    - It resolves its own id from `GET /users/me`, then `POST /kyc/initiate {userId: <own id>}` and `GET /kyc/{verificationId}`.
    - That is the subject acting for itself, so it is **still admitted**.
  - Akto and Schemathesis fuzzing: the spec already declares 403 on all four, so a 403 conforms.
- **Connector principals** (an `x-api-key` exchanged at the gateway, `userId` `connector:<id>`, role `connector`) now get 403 on all four. No in-repo connector calls them.
- **Platform reviewers** keep both reads.
- **Open-PR census** (`scratch/census_gql.py`: 101 open PRs, 449 file rows, every PR's files paged and asserted against totalCount):

| path | open PRs |
|---|---|
| kyc `index.ts` | [2214] |
| kyc `__tests__` | [2214] |
| `kyc.openapi.ts` | [] |
| anything under `services/kyc/` | [575, 649, 2214]; 575 and 649 touch `package.json` only |
| `keyRevokePolicy.ts` | [2066] |
| shared `middleware/index.ts` and `crypto/jwks.ts` | [] |

  - PR 2066's diff to `keyRevokePolicy.ts` (KS-2032, the live-ADMIN rule for tenant keys) does not touch `isPlatformRole` or `PLATFORM_ROLES`.
  - Controls: `services/auth/src/routes/users.ts` gives [2075, 2201]; an absent path gives [].
- **Verdict on breakage:** no legitimate in-repo flow breaks. Out-of-repo consumers are unknown: the extranet sibling, Kintsugi, demo clients, admin consoles (as the READY says).

## Q6. PR body

Read through GraphQL (`scratch/prbody2214.txt`, 8,590 chars).
- **Tier-1 statement: ABSENT.** "tier" occurs 0 times (case-insensitive). Gate 334's PR opened with a bold TIER 1 statement; this body has none (G338-2214-1).
- **Existence-oracle trade-off: present and accurate** (item 3). Measured: a non-subject gets 403 on an existing id and 404 on a missing one.
- **Refs only:** present.
  - The first line is `Refs KS-2166`, and closingIssuesReferences is 0.
  - The closing-word regex (close/fix/resolve forms followed by a key or #N) finds 0 hits; the control line `Fixes KS-1` gives 1.
  - The only hyphenated key is KS-2166 (×3).
  - The Linear URL is present.
- **Candidates listed as not-in-scope: INCOMPLETE.**
  - The body lists only the docs candidate (item 5).
  - The **refresh-token bearer** (0 hits for "refresh") and the **upper-case initiate id** are not in the body. The single "upper" hit is item 2's "admits upper case".
  - Both are in the READY (point 8 a and b) but not in the PR body (G338-2214-1).
- **Behaviour change:** stated plainly, in bold.
  - "No in-repo service or frontend calls these routes" is true.
  - Its grep was scoped to `Blockchain/`, so the systemTest caller (still admitted) is unmentioned. Info only.
- Items 1-4 and 6 are true as measured.
- **Item 7, mutants:** consistent with what I saw where the classes overlap. M11 fails first on the deletes assertion; the "killed only by the zero-DELETE assertion" wording is per-cell, which my 17-cell kill agrees with.

## Findings

- **G338-2214-1 (Minor, PR body): the tier-1 statement and the two named not-in-scope candidates are missing.**
  - The body has no tier-1 statement.
  - It does not list the refresh-token bearer or the upper-case initiate id as not in scope. The commission asks for both, and the READY carries them.
  - A body-only edit; no code or test change. Not a merge blocker if Wednesday accepts the READY as the record. Otherwise it is a body fix before merge.
- **G338-2214-2 (Minor, pre-existing, NOT in scope, measured): a refresh token works as a bearer.**
  - The shared `authenticate()` (via `verifyJwtRs256`) admits a refresh token as a bearer on kyc. Measured: a `type:'refresh'` token gets 200 on list, GET /:id and DELETE for its own subject.
  - Reading only: the gateway's `authenticateToken` checks `type === 'connector'` but not `'refresh'`.
  - It does **not** get round the owner rule: the token carries its own `userId`, and OTHER's refresh token gets 403.
  - What it does lengthen:
    - any bearer's life, from 1h to 7d (a stolen refresh token reads and **erases** its user's KYC data);
    - a SYSTEM_ADMIN's cross-user read on the two kyc reads, for the same 7 days. The role claim is not re-checked, the same stale-role class as KS-2032.
  - Candidate (a), now measured. Route to the board; a fix belongs in the shared verifier (reject `type !== 'access'` on the bearer path) and is out of this PR.
- **G338-2214-3 (Minor, pre-existing, NOT in scope): candidate (b) also causes an erasure gap.**
  - `svc_kyc_verifications.user_id` is `TEXT` (`migrations/002_verification-tiers.sql:476`, `docker/init/04-…:332`, `deployment/azure/migrate/init.sql:1251`).
  - Initiate stores an upper-case body userId verbatim (measured: row and consent both UPPER).
  - Every keyed read and delete is exact-text (`WHERE user_id = $1`). So those rows are not only missing from the owner's lower-case list (as the READY says), they are also **not erased** by:
    - the owner's lower-case DELETE;
    - the `user.erased` bus cascade, which carries the canonical id.
    This is from reading `dbDeleteUserData` plus the stand-in's exact matching; not measured on Postgres.
  - This PR narrows it: only the subject can now create such rows, where before anyone could. It does not cause it.
  - The router should see the GDPR consequence, not just the list symptom. Likely follow-up: canonicalise the body userId at initiate, or fold in the keyed queries.
- **G338-2214-4 (Note, test gap): two mutants survive.**
  - **M19:** the caller falls back to the `x-user-id` header when `userId` is missing. It survives because no cell sends an `x-user-*` header, though ruling D1 says they are rejected.
  - **M23:** the platform check uses `toUpperCase()`. It survives because no cell uses a U+0131 or U+017F role, though the code cites KS-1591.
  - The code is correct on both at head: probe A refuses the header in both shapes and refuses both Unicode roles.
  - Two cells would pin them. Not a blocker.
- **G338-2214-5 (Minor, pre-existing, NOT in scope): the same IDOR class remains on sibling routes.** Reading only:
  - `POST /api/kyc/:id/document`, `/:id/selfie`, `/:id/complete` and `GET /:id/result` (`index.ts:870, 993, 1061, 1235`) still act on any verification id without an owner check.
  - The `/api/kyc/microsoft/*` router (`routes/microsoft-verification.ts`) does the same:
    - `POST /start` and `/issue` take a body `userId`;
    - `GET /user/:userId/sessions` lists any user's sessions. The SDK and an e2e spec call it with another user's id (`TEST_USERS.holder.id`).
  - This PR makes verification ids harder to learn (initiate, list and GET /:id are now owner-scoped), but does not close these.
  - The ticket's scope is the four routes, so this is a candidate filing, not a defect here.
- **G338-2214-6 (Info): the existence oracle on GET /:id is confirmed and as ruled.**
  - A non-subject gets 403 on an existing id and 404 on a missing one.
  - `id` is `TEXT`, so an upper-case spelling of a minted lower-case id finds nothing (404) and gives nothing.
- **G338-2214-7 (Info): census scope and connectors.**
  - The seat's caller census was scoped to `Blockchain/` and missed `systemTest/schemathesis/tests/test_workflows_lifecycle.py`. That caller is self-acting and still admitted.
  - Connector (`x-api-key`) principals now get 403 on all four; no in-repo connector uses them.
- **G338-2214-8 (Info, gate conduct):**
  - node_modules were symlinked from gate 313's r2 (the shared sources are blob-equal).
  - Node 26 (not LTS).
  - load1 was 12.5 at session start, before any run; every run started under 8.
  - Develop moved during the gate (KS-2182, disjoint, merge-tree clean).
  - The census used the 2-day-stale shared checkout for breadth, with hits re-read at p2214.

No Major. The change is correct, fails closed on every hostile input I tried, and its tests are strong (21 of 24 mutants killed, 1 equivalent). G338-2214-1 is a body edit. G338-2214-2, -3 and -5 are pre-existing, out-of-scope filings for the board.

## NOT TESTED

- A running stack: a real token through the gateway proxy to kyc, and the gateway's session check on a refresh token (reading only).
- Postgres: the stand-in matches statements by text. The TEXT-column erasure gap (G338-2214-3) is from reading.
- The `user.erased` bus path.
- The seat's own 18 mutant files, verbatim (not available; my 24 cover the classes).
- The suite on the merged tree with develop eab5ac6b (merge-tree only; disjoint files).
- Node 24; a fresh `npm ci` at the head (symlinked installs); a container build.
- `docs-fragments.mjs check` (`Projects Documents/` is outside my sparse checkout).
- The pre-push hook and its legs; the four platform suites (Schemathesis, Akto, Playwright, k6); every other service's suite.
- Out-of-repo consumers: the extranet sibling, Kintsugi, demo clients, admin consoles.
- Linear: the KS-2166 ticket text and the seat's comment 595e26e4 were not read.
- The seat's worktree `worktrees/s-a29-ks2166`. My evidence is the pushed head.
