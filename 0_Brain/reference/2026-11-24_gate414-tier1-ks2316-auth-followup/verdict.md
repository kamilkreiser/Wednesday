PR 2290: GO WITH NOTES (at head 341185aab5a704992c64a4b944745142378c48a5; tier 1)

# Gate 414, tier 1 (Opus), PR 2290 (KS-2316 follow-up plus KS-1701's deferred auth sites), 2026-11-23 13:07:54Z to 13:29:19Z (00:07 to 00:29 AEDT 24 Nov, both from `date`)

**Authority (each read through `decision_queue.sh show`):**
- `secuura-users-stub-org-scope-ks2316-1123` = b, "Cover it too" (ruled 20:57:44 +11:00).
- `secuura-org-admin-create-level-cap-ks2316-1123` = b, "Allow up to STANDARD on create" (20:57:47).
- `secuura-platform-role-spellings-ks1701-1123` = a, "Everything asks the shared check" (10:11:59). Its delivered artefact is now PR 2289's squash 7af256b71a3b.
- Context: `secuura-org-admin-user-writes-scope-ks2316-1122` = a, delivered by PR 2288 as 8c2c24d37074.

**How rulings:** Wednesday's W72 plan ANSWER, read WHOLE (S7 moves with S1; the stub binds by ROLE; ISSUER_ADMIN is not bound; resolve first, refuse only the INSERT; NONE is admitted; S10 and S11 are untouched; the 2099 waiver; the json and ks2125 ride here). Also read: the seat's BRIEF, its plan QUESTION and its READY.

**Scope:** findings only. Nothing was fixed, pushed, posted, mailed, merged or deployed. No ticket or PR was written to. No `!CODING` path was written, fetched into or run under a git write verb.

## Pins
- **Pin 1, 13:08:08Z** (ls-remote over https, Blockchain's GH_CONFIG_DIR):
  - develop 7af256b71a3bbd1c31193df4b62487c6ddcd2020;
  - refs/pull/2290/head and the branch: 341185aab5a7;
  - PR 2099: 8967de8b1755;
  - PR 2289's last head: c8468d288024.
- **Pin 2, 13:28:52Z:** all unchanged. PR 2290 is OPEN, MERGEABLE, updatedAt 13:04:37Z, with 1 comment (the Linear linkback) and 0 reviews.
- **The PR:** 1 commit, whose one parent is 8c2c24d37074. 16 files = closed list v1, +924 −58.
- **Develop moved:** 7af256b's one parent is 8c2c24d37074 and its tree is 789505563da2. Of its 35 paths, ONE is shared with this PR: the ks1536 baseline json.
- **Subtrees:**
  - `services/auth` is identical on 8c2c24d and 7af256b (f440c964). It is also identical on the head and on the merge (e6461b78). So the auth arms are develop and head.
  - `packages/shared` differs on all four commits, so it was run on all four.

## How I measured
- **Clone:** my own clone `_work/g` (`--reference-if-able` gate 413's clone, `--dissociate`). Git write verbs ran only through `_work/gitx.sh` (my clone).
- **Worktrees:**
  - `d`: 8c2c24d
  - `n`: 7af256b
  - `h`: the head
  - `m`: a LOCAL merge commit 11afb1d8, tree 71b319a0, never pushed
  - `x`: a copy of m, for plants and mutants
  - `r`: d plus the PR's 8 auth test files, for red-first
- **node_modules:** APFS clones from gate 412 (root, auth, shared) and gate 413 (gateway, m only). Every lockfile used is sha-equal to develop's, and the PR changes no manifest. Shared `dist` was built with tsc in every tree.
- **Environment:** Node 26.8.1. TMPDIR `/private/tmp/g414`, which is now moved to `_work/_quarantine/private_tmp_g414`.
- **Tools** (all in `_work/`): `suites.sh`, `guards.py`, `guardsL.py`, `mutants.py`, `static.sh`, `plant_merge.py`, `lin_read.py`, `probes/g414-noloss.probe.test.ts` and `proof/`. Evidence is in `_work/evidence/`.
- **End state:**
  - Worktrees d, n, h, m and x have 0 porcelain lines. r holds only the 8 copied test files.
  - Containers `g414-ks2316-pg` and `g414-ks2316-redis` (labels `secuura.seat=g414`, published on 127.0.0.1 only) are STOPPED and kept.
  - Both auth processes were stopped by PID (tsx parents 16175 and 16286), and both ports were confirmed free afterwards.

## Findings
There is no HIGH and no MEDIUM finding.
- S1 to S9 ask the shared `isPlatformRole`, and nobody loses access at any of them (6,510-role census, Q2).
- The stub, the cap and the platform gain behave as ruled over a real socket on a real Postgres, with every write read back (Q7).
- I reproduced red-first (88) and every whole-suite figure.
- 25 of 25 mutants were killed and 0 survived (12 of the 25 are my own), plus 3 ks2125/ks1536 guard plants.
- The merge onto 7af256b is clean, and packages/shared is green on the merged tree apart from the one KS-278 name develop also fails.

### LOW
**G414-2290-1: the deferred ks1701 lowering is not needed for the merge, but until it lands, five shapes of returning platform check in auth pass every shared guard.**
- **FOUND:** on the merged tree, develop's ks1701 guard still carries:
  - the G1 allowance `authenticate.ts: 1` and `users.ts: 1`, though both files now hold 0 comparisons;
  - the FROZEN_BASELINE entries `users.ts: 9`, `oauth.ts: 1` and `authenticate.ts: 1`, though the merged json holds 3, absent and absent.
- **TESTED** (`guards.py`; tree x = the merge; one plant at a time; the three shared guard files were run, 107 cells; each file was sha-restored; x was clean at the end):
  - C0 (no plant): green.
  - **RED, as they should be:**
    - GA (a list back in oauth.ts): ks1536 G2 and ks2125 R1.
    - GB (users.ts baseline 3 → 4): ks2125 R2.
    - GC (a list in users.ts): ks1536 G2 and ks2125 R2.
    - GH (a hand-written comparison in oauth.ts): ks1701 G1.
  - **GREEN, so no guard sees them:**
    - GD: a list plus a `oauth.ts: 1` baseline entry;
    - GE: a list plus users.ts 3 → 4;
    - GF: `r === 'Super_Admin'` in users.ts;
    - GG: the same in authenticate.ts;
    - GI: a list plus an `authenticate.ts: 1` entry.
  - **With the seat's described lowering simulated** (`guardsL.py`: ALLOWED loses authenticate.ts and users.ts; FROZEN users.ts 9 → 3, with oauth.ts and authenticate.ts removed):
    - C0 stays green.
    - GD, GE, GF, GG and GI all go RED (ks1701 G1 or G2).
- **HOW:** the code that ships is right, and nothing here blocks the merge. What is lost is the ratchet's grip on the three auth files until the deferred lowering lands. The lowering is measured green on the real merge, so it can ride as a one-file follow-up (or a fix round) whenever Wednesday routes it. This matches the PR body's "passes as it stands", which is true but does not say that the slack is open.

**G414-2290-2: for an organisation admin with no organisation, the stub now answers three ways without writing anything.**
- **FOUND:** on the head, the org-less ORG_ADMIN gets:
  - 200 for an address in its own tenant;
  - 404 for an address held in ANOTHER tenant;
  - 403 for an address that exists nowhere.
- **Compared with develop and /lookup:**
  - Develop's stub already split these three cases for the same caller (200 / 404 / 201), but each "exists nowhere" probe minted an INVITED row, which left a trace and turned the next probe into a 200.
  - `/lookup` answers only 200 or 404 for the same caller: a nonexistent address and another tenant's address are both 404, by design.
  - So the information is not widened against develop's stub, but it is now traceless and repeatable. It is wider than /lookup, as develop's stub already was (the KS-74 limitation the code names).
- **TESTED:** over a real socket, both arms (`proof_socket_g414.txt`):
  - ORG_ADMIN(none): NEW address develop `201` and the row written, head `403` with no row in Postgres; EXISTING same-tenant 200 on both; OTHER-tenant 404 on both.
  - `/lookup` for a nonexistent address: 404 on both arms.
- **HOW:** this is inside Wednesday's ruled order ("resolve first, refuse only the insert"), and the plan named /lookup as the comparison. I list it for the KS-74 / S10 follow-up and do not treat it as a defect.

### INFO
**G414-2290-3: the S10 spoof is live at the stub, as listed.**
- The re-signed token with role `SUPER_ADMıN` (U+0131) got 201 and minted a placeholder on BOTH arms, over a real socket.
- The same token got 403 at S2 and 404 at S7.
- This is the KS-1591 class the PR lists (S10 and S11 untouched). It is pre-existing and unchanged.

**G414-2290-4: the S7 gain is tenant-bounded, measured on my database.**
- The PR's "Not measured: whether getAppById reads are tenant-bounded" now has a local answer.
- `oauth_apps` has FORCE ROW LEVEL SECURITY with `tenant_isolation` for PUBLIC. Its permissive `oauth_apps_auth_lookup` (USING true) applies only to role `secuura_auth_lookup`, while the service connects as `secuura_app` with the GUC seeded from the token.
- Results over a socket for OWNER's app in T1:
  - `Super_Admin` with tenant T1: 404 on develop, 200 on the head;
  - `Super_Admin` and exact `SYSTEM_ADMIN` with tenant T2: 404 on both arms.
- So the gain is exactly what an exact SYSTEM_ADMIN holds: apps of its own tenant.
- This was measured on migrations applied to my container, not on Kintsugi's database.

**G414-2290-5: two of the originate line numbers in the PR body and facts comment are off by a few lines.**
- The message "Could not resolve recipient via users/stub" sits at:
  - 8c2c24d: `certifications.ts:410`, `documents.ts:2091` and `:2106`;
  - 7af256b: `certifications.ts:407`, `documents.ts:2093` and `:2108`.
- The body says 407 and 2089. The listed sibling exists; only the anchors drift.

**G414-2290-6:** "691/691 auth cells" was not reproduced as a figure. My cell set (the 8 PR files plus ks564, ks1653, ks1402, ks806, ks467, ks1873 and ks728) is 637/637 on the head. The 8 PR files hold 558, and the seat's frame was not stated. Every other figure I checked reproduces.

## The commission's questions
**Q1 COMPLETENESS. No auth site that the platform ruling covers is left unchanged and unlisted.**
- **Frame:** `services/auth/src`, non-test (`__tests__`, `.test.`, `.spec.`, node_modules, dist and migrations excluded), `.ts .tsx .js .mjs .cjs`.
- **P1** (case-insensitive `system_admin|super_admin`): 37 lines in 9 files at develop, and 30 lines in 8 files at the head.
  - Positive control: `routes/users.ts:644` is found at develop (1 of 1). This reproduces the BRIEF's 37/9.
- **P2** (quoted `ORG_ADMIN|ISSUER_ADMIN|admin|ADMIN`): 33 lines in 6 files at develop (= the seat's 33), and 34 at the head (the +1 is the stub's new `callerRole === 'ORG_ADMIN'`).
- **P3** (`.role`, callerRole, isPlatform, isAdmin, hasAdminRole, `toUpperCase()`, `/admin/i`): 108 lines.
- **Every role test at the head falls into one of these classes:**
  1. **Changed:** S1 to S6 (`users.ts` 531, 587, 643, 675, 809, 1658); S7 (`oauth.ts` 1257 via `isOauthPlatformAdmin`, with OAUTH_APP_ADMIN_ROLES at 1248 = the three tenant names); S8 (`authenticate.ts:229`) and S9 (`:251`).
  2. **LISTED, untouched:**
     - S10, `users.ts:182` ALLOWED_LOOKUP_ROLES, read at 348 (/lookup) and 440 (/stub), with a full `toUpperCase()`;
     - S11, `issuerCerts.ts:65/73` `hasAdminRole`.
  3. **Not admission checks:**
     - `users.ts:235` PLATFORM_ONLY_CANONICAL_ROLES (the role being assigned);
     - `users.ts` ROLE_ALIASES 223-228;
     - `userRepo` `mapDbRole` and seeds;
     - `auth.ts:465` (a role assigned);
     - `password.ts:277` (ks1536's named exception);
     - `requireRole` (`authenticate.ts:189`, no platform spelling, no product caller);
     - the openapi string `auth.openapi.ts:926`.
  4. **Already shared:** `isPlatformAdmin` uses at `users.ts` 539/542/595/598/650/654/697/870/1672 and oauth gate 1 (1304, 1424).
- **Outside the frame (named, not chased):** `getDefaultScopesForRole` in `packages/shared/security/scopes` (role → scopes), SQL/RLS (no role-keyed policy on users, oauth_apps or organizations: all are tenant policies), and the frontends (listed by the PR).

**Q2 NO LOSS AT S1 TO S9. Proven by measurement.**
- **The probe** (`probes/g414-noloss.probe.test.ts`, mine, run in d and h then moved to `_quarantine`): the REAL users and oauth routers over a loopback listener, with the token verifier mocked; S8 and S9 called as the real middleware.
- **The universe: 6,510 roles.** Every ASCII capitalisation of SYSTEM_ADMIN, SUPER_ADMIN, ORG_ADMIN, ISSUER_ADMIN, ADMIN, OWNER, CONNECTOR, USER and VERIFIER; 269 PLATFORM_ADMIN variants and platform_viewer; the U+0131 and U+017F spoofs; padded strings; ''; undefined (an absent property); null; arrays; a number; an object.
- **LOST = [] at all nine sites.** gainedNotPlatform = [] everywhere. Each site gains exactly 3,069 roles: the ASCII platform variants (all 3,072 are admitted on the head, of which 3 were exact before).
- **Non-platform admitted, develop = head:**
  - S1, S2, S3, S7: {ORG_ADMIN, ISSUER_ADMIN, admin}
  - S4, S6, S8: {ORG_ADMIN}
  - S5: {ORG_ADMIN, admin}
  - S9: {}
- **Stays refused at all nine:** `org_admin`, `issuer_admin`, `ADMIN`, `platform_admin`, both spoofs, arrays and undefined. The bounded predicates are not used anywhere in the change: mutant GM7 (`isPlatformOrOrgAdminRole` at S4) is killed.
- **S7 and getAppById's tenant scope:** see G414-2290-4. RLS bounds the gain to the caller's tenant.

**Q3 THE STUB.**
- **The repo write:** `createInvitedStub(email, tenant, placement)` passes `organizationId: placement.organizationId` into `createUser`. Its INSERT writes `organization_id` as parameter `user.organizationId || null` (`userRepo.ts` 691 and 724).
- **Over the socket on Postgres, rows read back** (develop → head):
  - **ORG_ADMIN(O1):** NEW 201 with organization_id NULL → 201 **O1**.
  - **A token CLAIMING a different organisation** (re-signed from the O1 admin's own login): head 201 **O1**. The row, not the token, decides.
  - **ORG_ADMIN with no organisation:**
    - NEW 201 → **403** "Only an admin who belongs to an organisation can create placeholder users", with no row;
    - EXISTING same-tenant 200 `alreadyExisted` on both;
    - OTHER-tenant 404 on both.
  - **`org_admin` (folded):** bound the same way (201 → 403).
  - **Unchanged on both arms:**
    - ISSUER_ADMIN(O1): 201 with NULL;
    - the connector token (`certifications:write`): 201 with NULL;
    - SYSTEM_ADMIN, SUPER_ADMIN, super_admin, Super_Admin and system_admin: 201 with NULL;
    - platform_admin and OWNER: 403;
    - no token: 401.
- **Cells:** ks564, ks1653 and ks1402 are green on the head (14/14).
- **The repo insert is not called** for the org-less admin: the "insert not called" cells pass, mutants SM12, SM15, GM2 and GM9 are killed, and the socket shows no row.
- **Existence oracle:** see G414-2290-2. It is not widened against develop's stub, it is wider than /lookup (as before), and it is now traceless.

**Q4 THE CAP. Holds.**
- **Over the socket, ORG_ADMIN(O1), rows read back:**
  - NONE, BASIC, SOCIAL, STANDARD (and `standard`): 201, written at that level in O1.
  - ENHANCED, HIGH, GOVERNMENT: 403 "Only a platform admin can set a verification level above STANDARD", with no row.
  - FOO: 400.
- **Platform admins:**
  - SYSTEM_ADMIN: all seven are 201 with organisation NULL, on both arms.
  - `Super_Admin`: 403 "Admin role required" on develop, and all seven 201 on the head (the S4 gain).
- **The words:** the refusal is the editor's exact template (`users.ts:737` = `:965`, the same `withinOrgAdminLevelCap` and `ORG_ADMIN_VERIFICATION_LEVEL_CAP`). The spec's three strings and the 5 yaml lines say the same.
- **No other create rule is weakened:**
  - the org-less admin is still 403 at every level up to STANDARD;
  - the new user still lands in the caller's row organisation;
  - the PR 2288 own-organisation cells are 82/82;
  - mutants GM5, GM6, GM12, SM17 are killed.
- **The order is unchanged from develop:** the level is checked before the organisation, so an org-less admin at ENHANCED reads the cap message.

**Q5 THE GUARDS ON THE MOVED DEVELOP. This PR CAN merge onto 7af256b71a3b as it stands. No rebase or fix round is required.**
- **merge-tree:**
  - (7af256b, head) rc 0 → tree 71b319a0f994;
  - (head, 7af256b) rc 0 → the same 71b319a0f994, which equals the seat's predicted tree.
- **Planted control** (`plant_merge.py`; a LOCAL commit on the head that edits the json line `"services/originate/src/routes/documents.ts": 1`, which PR 2289 removed; the anchor was asserted to occur once): rc 1 with 1 CONFLICT, in both orders.
- **The merged json:**
  - users.ts 3; authenticate.ts and oauth.ts absent; 20 files; total 36.
  - Against 7af256b: users.ts 9 → 3, with two entries removed and none raised or added.
  - Against 8c2c24d: the same 3 auth changes plus PR 2289's 7 removals.
- **packages/shared WHOLE on the merged tree m: 1746/1747.** The one failure is `wallet-signature … KS-278 accepts a valid wallet signature over the message`, the SAME name as 7af256b (1746/1747).
  - On it: ks1701 G1, G1c, G1r and G2 pass; ks2125 C0, C1, R1 and R2 pass; ks1536 G1 to G7 pass.
  - So the seat's claim (2289's ks1701 guard passes on these lower counts without the deferred lowering) now holds on the REAL merge, not only a prediction.
- **ks2125 can still FAIL:** GA (a list planted in oauth.ts) turns R1 red, and GB/GC turn R2 red.
- **What the deferred lowering would add:** see G414-2290-1. It is wanted for the ratchet and not needed for the merge.

**Q6 RED-FIRST and MUTANTS.**
- **Red-first,** tree r (develop's product with the PR's 8 auth test files):
  - 88 of 637 fail: ks1701 55, stub 10, create 11, ks2287 3, ks1536-users 3, ks1536-oauth 4, ks2316 1, ks1210 E2 1.
  - All 88 fail by assertion, with 0 load failures. 87 are RED-titled, plus E2.
  - On the head: 637/637.
- **Mutants** (`mutants.py`; tree x; the 15-file cell set; control green before and after; every file sha-restored; x clean at the end):
  - **25 run, 25 killed, 0 survivors, 0 load failures.**
  - **The seat's families, re-typed (13):**
    - S1 back to six names; S2 exact platform arm; S7 back to six; S8 back to four; ORG_ADMIN at S9; platform_admin at S5; the full-fold spoof at S6;
    - the stub organisation check removed; organisation not passed; repo ignores the organisation; repo ignores mayCreate; repo refuses before resolving;
    - the cap back to BASIC.
  - **The commission's own, all killed:**
    - GM1: the stub organisation from the TOKEN;
    - GM2: the refusal moved BEFORE the lookup;
    - GM3: a connector bound;
    - GM4: ISSUER_ADMIN bound;
    - GM5: the cap raised to ENHANCED;
    - GM6: NONE refused;
    - GM7: the bounded predicate admitting org_admin at S4.
  - **Mine:**
    - GM8: binding on the exact raw ORG_ADMIN, so org_admin escapes;
    - GM9: a missing caller row allowed to create;
    - GM10: ORG_ADMIN case-folded at S6;
    - GM11: ISSUER_ADMIN dropped from gate 2;
    - GM12: the shared cap constant raised.
  - **The json mutants** "users.ts back to 4" (GB) and "a list in oauth.ts" (GA) are red in `guards.py`.

**Q7 PROOF. The REAL auth service was booted twice, over real sockets.**
- **The stack:**
  - `src/index.ts` over tsx, from develop 8c2c24d (port 51358) and the head (port 51364);
  - both bound to 127.0.0.1 by a listen preload;
  - both on my own Postgres 15 (`run-migrations.sh` applied=60 failed=0; `runStartupMigrations` applied=48 failed=0) and my own Redis.
- **Accounts:** 7, registered through `POST /api/auth/register`. Roles and organisations were set by SQL in my container only.
- **Tokens:**
  - **Real logins** (real sessions, service-signed): SYSTEM_ADMIN, ORG_ADMIN(O1), ORG_ADMIN(none), ISSUER_ADMIN(O1) and OWNER.
  - **Re-signed spellings:** SUPER_ADMIN, super_admin, Super_Admin, system_admin, platform_admin, SUPER_ADMıN, org_admin, a T2 tenant and a stale organisation claim. Each is the SYSTEM_ADMIN (or ORG_ADMIN) login's own claims on its live session, with only the role, tenant or organisation changed, signed by the same throwaway key the services hold.
  - **The connector token:** minted in `generateConnectorToken`'s shape.
- **Driven on both arms:** S2 `GET /admin/list`; S7 `GET /oauth/apps/:id` on an app OWNER created through the API; `POST /api/users/stub` (new, existing, other-tenant); `POST /api/users/admin/create` at nine levels for four callers. Every write was read back from Postgres.
- **The full table is in `evidence/proof_socket_g414.txt`.** The flips:
  - Super_Admin and system_admin: S2 403 → 200 and S7 404 → 200;
  - Super_Admin: create 403 → 201;
  - the ORG_ADMIN stub rows NULL → O1;
  - org-less ORG_ADMIN and org_admin: new stub 201 → 403;
  - ORG_ADMIN create at NONE, SOCIAL, STANDARD and `standard`: 403 → 201.
  - Everything else is equal on both arms.
- **Not driven:**
  - S1, S3, S5, S6, S8 and S9 over the service (probe only);
  - a real `platform_admins` login (read from code: `auth.ts` 533 and 557 mint the stored role verbatim; that column's CHECK allows `super_admin`, `platform_admin` and `platform_viewer`, so no mixed case arrives from that path);
  - the gateway;
  - originate's 502 mapping;
  - a connector key exchanged at the real `/connector` mint;
  - Kintsugi's database.

**Q8 WHOLE and WORDS.**
- **Suites WHOLE** (failure-name sets compared):

| suite | develop | head / merge |
|---|---|---|
| services/auth | 2151/2151 (8c2c24d = 7af256b subtree) | 2462/2462 |
| packages/shared at 8c2c24d → head | 1742/1743 | 1742/1743 |
| packages/shared at 7af256b → merge | 1746/1747 | 1746/1747 |

  - In packages/shared, KS-278 `wallet-signature` is the one name on all four.
  - In auth, 12 names were dropped (exactly the 12 ruled flips, renamed) and 323 were added (310 new + 12 renamed + 1 twin).
- **Static:**
  - tsc `--noEmit`, auth and shared: rc 0 on d, h and m. The planted control gives rc 2.
  - eslint (the PR's auth files and ks2125): 0 errors on all three arms. The one warning is the same pre-existing `authenticate.ts:100`. The planted `debugger` control gives rc 1.
  - `generate-openapi --check`: PASS on d, h and m. A one-word plant in `auth.openapi.ts` gives CHECK FAIL, rc 1.
  - Test-file type ratchet (auth): 41 errors, all in the baseline, 0 new; files 216 → 219.
- **Overlap** (13:28:27Z, gh, 18 open PRs, 130 file rows, no truncated file list): only PR 2099 shares a path (the yaml).
  - merge-tree of 2099 with the merge m: rc 0, tree 97e83513, in both orders.
  - merge-tree of 2099 with the head: rc 0, tree 359fb4f08ac3 (= the seat's), in both orders.
  - merge-tree of 2099 with 7af256b: rc 0.
  - Planted control on 2099's `walletAddress: type: string` line (asserted once) on top of m: rc 1 with 1 CONFLICT, in both orders.
- **Words:** the PR body, facts comment db525eb5 (KS-2316, 3392 B, 13:04:46Z) and pointer 245fa311 (KS-1701, 278 B, 13:04:57Z) were read whole, read-only. The key was read inside python and never printed. Both tickets were selected by identifier, and the team key KS was confirmed.
  - Every sentence I checked holds, except the line anchors in G414-2290-5 and the unreproduced "691" (G414-2290-6).
  - The figures that reproduce: 310 new cells (254, 29, 27); 12 flips (1 + 4 + 3 + 3 + 1) plus 1 twin; 88 red; 2151 → 2462; 1742/1743 both; users.ts 9 → 3 with the three remaining lists at 182, 213 and 235 as named; 52 → 44; tree 71b319a0 and 359fb4f0; eslint and the ratchet.
  - "Not measured: getAppById tenant-bounded" now has a local measurement (G414-2290-4).
  - "the guard passes as it stands" is true on the real merge, though it leaves slack (G414-2290-1).

## Siblings found (listed, not acted on)
- **S10 /lookup and /stub, and S11 issuerCerts:** the U+0131 spoof mints a stub over a real socket (G414-2290-3). This is the same KS-1591 follow-up the PR lists.
- **The ks1701 guard lowering:** needed to close five auth slack shapes (G414-2290-1).
- **The stub's traceless three-way answer** for an org-less admin (G414-2290-2). This belongs with the KS-74 limitation.
- **The originate 502 label** (`certifications.ts:407`, `documents.ts:2093/2108` at 7af256b), as the PR lists.

## Faults, disclosed
- **A hook refusal that ran nothing:** an unquoted `=====` separator.
- **A second refused call, which ran nothing:** a `$M` word-split under zsh. It was re-run under `bash`.
- **A third refused call, which ran nothing and wrote no file:** it held a stray `cd /dev/null` at its tail. I wrote the script with the Write tool and ran it by absolute path.
- **My first `guards.py` opened files for writing before reading them,** which truncated them. The GA result from that run is void: oauth.ts held only the planted line.
  - The run stopped on GB with the baseline json empty in x.
  - I restored it from `git show refs/g414/merged:<path>`, confirmed x clean, fixed the script and re-ran everything. Only the re-run is reported.
- **`suites.log`'s "end … rc=" field reads `$?` after a `$(date)` substitution,** so it shows 0 for the shared runs. The authoritative rc is the `rc N` line `run_cwd.py` prints just above each one (rc 1 for shared, which is the KS-278 failure).
- **I discarded stderr once,** on a `sleep 3 2>/dev/null` after the kill. The kill's own rc and the lsof check are reported.
- **Throwaway data only:** the proof's organisation, tenant move and roles were set by SQL in my container only. The re-signed tokens use my throwaway key, never a project credential.
- **No** push, comment, mail, ticket write or `!CODING` write.

## Not run
- The four platform suites (Schemathesis, Akto, Playwright, k6), preflight and leg 14's shell suites.
- The api-gateway and originate, booted (so originate's 502 mapping of the new 403 was not driven).
- S1, S3, S5, S6, S8 and S9 over the booted service. They were covered by the probe and the cells.
- A real `platform_admins` login, and a connector key exchanged at the real mint.
- Node 24.
- Any deployed box or database (Kintsugi included).
