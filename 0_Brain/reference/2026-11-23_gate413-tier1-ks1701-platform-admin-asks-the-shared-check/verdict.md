PR 2289: GO WITH NOTES (at head ffefc60696307d7e403df83bfc82ebf93d4502c1; tier 1)

# Gate 413, tier 1 (Opus), PR 2289 (KS-1701), 2026-11-23 10:30:03Z to 10:50:24Z (21:30 to 21:50 AEDT, both from `date`)

**Authority:** Kam's card `secuura-platform-role-spellings-ks1701-1123` = a, "Everything asks the shared check" (ruled 2026-11-23T10:11:59+11:00, read through `decision_queue.sh show`), and `secuura-ks-1536-platform-admin-role-one-list-1106` = a (one vocabulary, ruled 2026-11-06).
**How rulings:** Wednesday's W71 plan ANSWER (QA to QH; QE puts vc-issuer `ownership.ts` in scope), the docs ANSWER (closed list v3) and the coupled ANSWER (closed list v4, 35 paths).
**Scope:** findings only. Nothing was fixed, pushed, posted, mailed, merged or deployed. Nothing was written to GitHub, Linear or any `!CODING` path.

## Pins
- **Pin 1, 10:30:42Z** (ls-remote over https, gh credential helper, Blockchain's GH_CONFIG_DIR):
  - develop: d59c623e061756a3419a54a648db62b164ef04ed (PR 2287's squash, KS-2331, 4 `frontend/issuer` files);
  - refs/pull/2289/head and the branch: ffefc60696307d7e403df83bfc82ebf93d4502c1;
  - refs/pull/2288/head: 8f9e98115ad65564185dd6bc60cc61465d4649a3. It has MOVED from the commission's 88d31bd3 (a "gate 412 fix round 1" commit) and is still OPEN.
- **Pin 2, 10:49:48Z:** all three unchanged. PR 2289 is OPEN at the same head, updatedAt 10:28:26Z, with 1 comment and 0 reviews.
- **The PR (gh, read-only):** not draft, base develop, MERGEABLE. 1 commit, parent a5ce6ee8b662. 35 files, +915 −74. The title starts "Refs KS-1701:".
- **Paths:** the commit's paths are exactly the closed list v4: 11 product files, the baseline, 5 new cell files, 16 changed test files and 2 docs fragments.
- **The merged state:** develop's only new commit touches 4 `frontend/issuer` files, none of the 35. merge-tree in both orders gives tree caf79cec, which equals the seat's figure. So the head tree is the merged state for every suite below.

## How I measured
- **Clone:** my own clone `_work/g` (`--reference-if-able` gate 412's clone, `--dissociate`). Git write verbs ran only through `_work/gitx.sh`.
- **Worktrees:**
  - `d`: develop d59c623e
  - `h`: the head
  - `r`: develop plus the PR's 21 test files (not the baseline)
  - `x`: the head, used for mutants, guard plants and static plants
- **node_modules:** APFS clones from gates 412 (root and shared), 410 (originate and gateway) and 405 (billing and vc-issuer).
  - Every package.json and package-lock.json used is sha-equal to develop's.
  - The PR changes no manifest.
  - Shared `dist` was built with tsc in every tree.
- **Environment:** Node v26.8.1. TMPDIR was the short `/private/tmp/g413`, which is now moved to `_work/_quarantine/private_tmp_g413`.
- **Tools** (all in `_work/`): `cells.sh`, `suites.sh`, `an.py`, `guards.py`, `mutants.py`, `static.sh`, `lin_read.py`, `probes/noloss.ts` and `proof/`. Evidence is in `_work/evidence/`.
- **End state:**
  - Worktrees d, h and x have 0 porcelain lines. r holds only the 21 copied test files.
  - Container `g413-ks1701-pg` (postgres:15-alpine, `127.0.0.1:56573`, labels `secuura.seat=g413` and `secuura.purpose=g413-socket-proof`) is STOPPED and kept.
  - All six service processes were stopped by PID (rc 0), and each port was confirmed free afterwards.

## Findings
There is no HIGH and no MEDIUM finding.
- Every changed site now asks the shared `isPlatformRole`, and `isPlatformRole` itself is unchanged.
- No caller loses access. Every gain is a platform role.
- `platform_admin`, the U+0131 and U+017F spoofs, non-string roles and missing roles stay refused.
- ORG_ADMIN, ISSUER_ADMIN, connector and bare `admin`/`ADMIN` keep their outcomes.
- I reproduced red-first, every whole-suite figure, the static legs and the merge check.
- 27 of 27 mutants were killed, 16 of them my own.
- A real-socket proof on the real services matches the ruling on both arms.

### LOW
**G413-2289-1: the guards hold what they claim, but a raised baseline entry for a file outside the seven goes through both of them, and so do four other shapes of hand-written check.**
- **FOUND:** ks1701 G2 ratchets only the seven entries KS-1701 lowered to zero. ks1536 G2 fails only when a file's count is ABOVE its baseline. So these pass both guards:
  - raising any of the other 22 entries;
  - adding a new entry, which gives headroom for a list to come back.
  G1's expression sees only `===`/`!==` against a quoted spelling, and it counts lines, not comparisons.
- **TESTED** (`guards.py`; each plant was applied alone in tree x and both guard files were run, 103 cells; the file was then restored and its sha checked; x was clean at the end):
  - RED as claimed:
    - GP1 (a chain in a non-allow-listed `anchors.ts`): G1 red;
    - GP2 (billing `webhooks.ts: 1` put back in the baseline): ks1701 G2 red;
    - GP8 (a new bracket list): ks1536 G2 red;
    - GP10 (a new comparison line in allow-listed auth `users.ts`): G1 red.
  - GREEN, so the guards cannot see them:
    - GP3: `gdpr.ts` raised from 6 to 7;
    - GP4: a new `anchors.ts: 1` entry;
    - GP5: `switch (r) { case 'SUPER_ADMIN': ... }`;
    - GP6: a loose `==`;
    - GP7: a compare through a named constant;
    - GP9: a second comparison on auth `authenticate.ts`'s already-allowed line 249.
- **HOW:** the code that ships is right. These are limits of the guard's scope, and the PR body states G2's scope correctly ("the seven lowered entries"). The commission's test, "a raised baseline entry ... must go red", holds for the seven lowered entries and not for any other entry. Whether to ratchet the whole baseline (equality instead of `<=`) is for Wednesday to route.

**G413-2289-2: the facts comment's list of frontends misses two admin-portal files.**
- **FOUND:**
  - `frontend/admin/src/store/authStore.ts:23-25` (`authUserToLocal`) is an equality chain: ADMIN, admin, super_admin, SYSTEM_ADMIN or OWNER map to the local `super_admin`.
    - SUPER_ADMIN, system_admin and the mixed-case spellings become local `admin`.
    - `Layout.tsx` (109, 126, 304, 320) then hides the platform section from them.
  - `frontend/admin/src/pages/Profile.tsx:105` and `:111` render the label from `=== 'super_admin'`.
  - The facts comment and PR body list only Layout.tsx (4), Users.tsx (1) and `frontend/shared/src/auth/index.ts` (1).
- **TESTED:** a read only, by git grep over `Blockchain/Dev/frontend/*/src` (non-test) at the head. I did not drive it in a browser.
- **HOW:** these are UI mappings, not gates; the server gates decide what a caller may do. Frontends are OUT by QF. This is a gap in the listing that Wednesday's later frontend or auth follow-up should carry. It is not a defect of this PR.

### INFO
**G413-2289-3: the red-first count of flipped cells is 34, not 31.**
- The PR body and READY say "31 flipped cells fail (originate 29, vc-issuer 2)".
- I measured vc-issuer at 5: ks1116 A2b and A5b, ks1906 P2b, ks692 S1 and ks692 A1. All 5 are red by assertion on develop's product (`cells_red_vc-issuer.json`).
- The "66 new cells red" figure reproduces exactly (originate 43, billing 5, vc-issuer 10, gateway 6, shared 2), so the total red is 100.
- The body itself lists all five vc-issuer cells as changed. Only the count is short.

**G413-2289-4: at the gateway override, an array role is not "refused" but never answered.**
- The PR body says every site keeps refusing "an array role".
- On a ROLE step, an array role throws `userRole.toLowerCase is not a function` at verification.ts:457, before any check. The request is never answered, and nothing is approved.
- This happens identically on develop: the first operand is unchanged (probe `gw_array_r.out` and `gw_array_x.out`).
- On a USER step, an array, undefined, empty or numeric role gets 403 with no approval, on both arms (`gw_array_*.json`).
- The gateway cells do not send an array or undefined (`NOT_PLATFORM` has 5 strings).
- In practice it cannot be reached: the role claim comes from an RS256 token that the gateway verified.

**G413-2289-5: Wednesday's QE reading holds.**
- Card `secuura-ks1116-null-owner-who-reads-1020` (read at source) chose option a, verbatim: "Tenant administrators (ORG_ADMIN / SYSTEM_ADMIN with a tenant on the token)". It names a class of WHO and two role names. It says nothing about letter case.
- The words "Exact, case-sensitive strings" were in the builder's code comment (develop `ownership.ts:79`), not on Kam's card.
- Kam's 11-23 card says SYSTEM_ADMIN and SUPER_ADMIN in any capitalisation count as platform admin. KS-1906 had already admitted SUPER_ADMIN as a platform administrator for owner-less credentials (`ownerlessCredentialReadable`).
- So the build matches both cards:
  - the SYSTEM_ADMIN arm uses `isPlatformRole`;
  - the ORG_ADMIN arm stays exact;
  - the tenant-on-the-token condition is unchanged.
- That condition is proven by my no-loss run: with no tenant claim, 0 roles are admitted on both arms. Mutant G-5 is also killed.

**G413-2289-6: PR 2288 composes with this PR.**
- 2288's head moved to 8f9e9811. Its 10 files share none of the 35 paths.
- merge-tree of 2289 and 2288 in both orders gives the same tree, 2ecb130d.
- At that tree, the things this PR's guards read are unchanged:
  - auth `users.ts` holds 1 G1 comparison line and 9 ks1536 lists;
  - `authenticate.ts` holds 1 G1 comparison line.
  - So G1's allowance and the ks1536 baseline still hold after both merge.

**Other INFO:**
- **The duplicate facts comment** a0f9e65f now reads 98 bytes, updatedAt 10:30:45Z, so it has been edited since READY. Wednesday is handling it, and I did not act on it.
- **The original facts comment** f4292579 is unchanged: 5468 B, sha256 prefix 433670127b19 (equal to READY's), updatedAt .057Z, earlier than its createdAt .085Z. KS-1701 is In Progress, priority 3, with 4 comments.

## The commission's questions
**Q1 COMPLETENESS CENSUS. No platform-admin test that the ruling covers is left unchanged and unlisted in services, packages or the gateway.**
- **Frame:** git grep at the head of `services/*/src` and `packages/*/src`, non-test, case-insensitive `system_admin|super_admin`.
  - 152 lines at the head and 158 at develop (`census_p1_head.txt`, `census_p1_dev.txt`).
  - On the seat's exact frame at a5ce6ee8, I get 155 lines; its "155 in 50 files" reproduces. The one line my first frame dropped is `startup-migrations.ts:436`, because the word "migrations" matched my exclusion.
  - Positive control: `documents.ts` 354, 1181 and 1545 are found (3 of 3).
- **Second patterns:**
  - an `isAdmin`/`isSystemAdmin`-style assignment: 5 hits, being the 3 changed sites plus auth `authenticate.ts` 228 and 249;
  - substring and regex role tests: only auth `password.ts`'s `/admin/i` password rule;
  - `platform_admin`: no admission.
- **Every hit outside the 11 changed files** falls into one of these classes:
  1. **Deferred, auth, behind PR 2288 (listed with develop lines):** `users.ts` 485, 541, 597, 629, 750 and 1589; `oauth.ts` 1246; `authenticate.ts` 228 and 249.
  2. **Already admit every ASCII spelling (listed):**
     - auth `issuerCerts.ts` `hasAdminRole` (as it is, or upper-cased) and `users.ts` 182 (lookup);
     - originate `DOCUMENT_WRITE_ROLES` through rbac;
     - gateway `GATEWAY_DOCUMENT_WRITE_ROLES`;
     - security `KEY_ADMIN_ROLES` and `provisioningPolicy`.
  3. **Already ask `isPlatformRole`:**
     - gateway `middleware/auth.ts:766` (tenant override) and `platform.ts`;
     - security `/api/audit`;
     - governance, kyc, referral, transfer, staking, wallet-connector, analytics, nft-certificate;
     - billing `billing.ts`.
  4. **Seeds and canonicalisers, which are not admission checks:**
     - auth `userRepo` `mapDbRole` and its seeds; `users.ts` 221-229; `auth.ts` 465;
     - gateway `admin.ts:501`;
     - demo-service `access.ts:61`, `documents.ts:115` and `config.ts`.
  5. **Comments and openapi strings.**
  6. **Named exception:** `password.ts:277`.
- **The middleware's callers** (adminConfig 51; gdpr 425, 471, 674, 707, 725, 365, 460, 511, 522, 196 and 201; systemErrors 185, 207, 229 and 239; the connector lists at gdpr 618 and 653 and platformOrganizations 93 and 151) are exactly the PR body's blast radius. No other file imports `requireRole`, `hasAnyRole` or `requireSelfOrRole`.
- **Outside the frame:**
  - **Frontends:** admin `Layout.tsx` 109, 126, 304 and 320; `Users.tsx` 90 (a menu roles list) and 343 (a colour switch); `frontend/shared/src/auth/index.ts` 46-47; plus the unlisted `authStore.ts` 23-25 and `Profile.tsx` 105 and 111 (G413-2289-2).
  - **SQL:** no RLS policy keys on a role. All 22 `CREATE POLICY` statements are tenant policies. Platform DB `platform_admins.role CHECK (role IN ('super_admin','platform_admin','platform_viewer'))` (`docker/init-platform/01-platform-schema.sql:79-80`) is a data constraint on the separate platform-portal table, not an admission check.

**Q2 NO LOSS. Proven by measurement.**
- `probes/noloss.ts` imports the REAL `hasAnyRole` and `requireRole` (originate) and `ownerlessRowReadable` (vc-issuer) from BOTH trees. It compares them over 16,460 roles:
  - every ASCII capitalisation of SYSTEM_ADMIN, SUPER_ADMIN, ORG_ADMIN, ISSUER_ADMIN, PLATFORM_ADMIN, ADMIN, OWNER, CONNECTOR, TENANT_ADMIN and VERIFIER;
  - the U+0131 and U+017F spoofs, arrays, undefined, null, '', a number and an object.
- **Lost = [] at every site and for every list:**
  - `hasAnyRole` with ['SYSTEM_ADMIN','ORG_ADMIN'], ['SYSTEM_ADMIN'], ['ORG_ADMIN'], ['connector'], ['SUPER_ADMIN'] and ['SYSTEM_ADMIN','ORG_ADMIN','ISSUER_ADMIN'];
  - `requireRole` with ['SYSTEM_ADMIN','ORG_ADMIN'], ['SYSTEM_ADMIN'] and ['connector'];
  - `ownerlessRowReadable`, with a tenant on the token and without one;
  - the develop chains (3 spellings), billing (2), vc-issuer status (3) and the gateway's six-spelling list, each compared with the head.
- **Every gain is a platform role.** `gainedNotPlatform` is [] everywhere.
- **ORG_ADMIN-only and connector lists:** 1 role admitted, before and after.
- **Without a tenant on the token:** 0 roles are admitted, before and after.
- **The gateway** keeps `admin` and `ADMIN` exactly (mutants G-4 and G-4b are killed by the W3 twins). Missing, empty, numeric and array roles on a user step: 403 on both arms. For an array role on a role step, see G413-2289-4.
- **What gains:** gdpr's `isBoundOrgAdmin` (196) and `mayActForSubject` (201) now treat the case variants as platform. That is the ruled gain, and P1b covers it.

**Q3 THE GUARDS.**
- **The baseline only goes down:**
  - 7 entries are removed and none is raised: 52 to 44, files 29 to 22.
  - The removed entries are gateway `index.ts` 1, billing `webhooks.ts` 1, originate `middleware/auth.ts` 2, `certifications.ts` 1, `documents.ts` 1, vc-issuer `ownership.ts` 1 and `status.ts` 1, which sum to 8.
- **G1 and G2 can fail:**
  - Red-first: both are red on develop (`cells_red_shared.json`, 2 of 4 failed by assertion).
  - Planted: GP1 turns G1 red, GP2 turns ks1701 G2 red and GP8 turns ks1536 G2 red.
  - The limits are in G413-2289-1.

**Q4 RED-FIRST and MUTANTS.**
- **Red-first,** in tree r (develop's product with the PR's tests):
  - originate 72 of 686 red (43 new + 29 flips);
  - billing 5 of 18; vc-issuer 15 of 525 (10 new + 5 flips); gateway 6 of 25; shared 2 of 4;
  - every failure is by assertion, with 0 load failures.
  - At the head: 686/686, 18/18, 525/525, 25/25 and 4/4.
- **Mutants** (`mutants.py`; the control was green before and after on all four services; every file was sha-restored; x was clean):
  - **27 run, 27 killed, 0 survivors, 0 load failures.**
  - **The seat's families, re-typed:** S-M1 (documents list chain), S-M4 (certify chain), S-M6 (alias fold), S-M7 (exact), S-M8 (toUpperCase), S-M9 (any role), S-M10 (`platform_admin`), S-M12 (billing exact), S-M13 (vc-issuer exact), S-M14 (gateway six-list) and S-M17 (ownership exact).
  - **Mine:**
    - G-1: `hasAnyRole` exact while `requireRole` moved (26 cells red);
    - G-2: ORG_ADMIN admitted at a SYSTEM_ADMIN-only list;
    - G-3, G-3b, G-3c and G-3d: a toUpperCase fold admitting the dotless-i spoof at documents, ownership and billing;
    - G-4 and G-4b: the gateway dropping bare `admin` or `ADMIN`;
    - G-5: ownership admitting a platform caller with no tenant on the token;
    - G-6: originate's ORG_ADMIN arm case-folded;
    - G-7: the gateway user-step branch left without `isPlatformRole`;
    - G-8: billing on a 4-spelling list without mixed case;
    - G-9: ownership's ORG_ADMIN arm case-folded;
    - G-10, G-11 and G-12: the by-id fallback, the certifications list and the anchor check each reverted on their own.

**Q5 PROOF. The REAL services were booted over real sockets.** These were not cells and not stubbed persistence.
- **The stack:**
  - originate, billing and vc-issuer, each `src/index.ts` over tsx, from develop (d) and the head (h);
  - each bound to 127.0.0.1 by a listen preload;
  - all on my own Postgres (`run-migrations.sh` applied=60 failed=0; `runStartupMigrations` applied=48 failed=0).
- **Tokens:** signed with my own throwaway RS256 key and verified by each service's REAL `authenticate` (`JWT_PUBLIC_KEY`), with tenant a0000000-…-0001.
- **Seed data:** one document of that tenant owned by a non-caller, and one stored webhook event.

| request | SYSTEM_ADMIN | SUPER_ADMIN | Super_Admin | system_admin | ORG_ADMIN | platform_admin | SUPER_ADMıN | no token |
|---|---|---|---|---|---|---|---|---|
| originate adminConfig gate GET /api/admin/document-types, develop | 200 | 200 | 403 | 403 | 200 | 403 | 403 | 401 |
| the same, head | 200 | 200 | **200** | **200** | 200 | 403 | 403 | 401 |
| originate GET /api/documents (seed doc listed?), develop | 5, yes | **0, no** | 0, no | 5, yes | 0, no | 0, no | 0, no | 401 |
| the same, head | 5, yes | **5, yes** | **5, yes** | 5, yes | 0, no | 0, no | 0, no | 401 |
| originate systemErrors GET /api/system-errors/stats, develop | 200 | 200 | 403 | 403 | 403 | 403 | 403 | 401 |
| the same, head | 200 | 200 | **200** | **200** | 403 | 403 | 403 | 401 |
| billing POST /webhooks/replay, develop | 200 | 200 | 403 | 403 | 403 | 403 | 403 | 401 |
| the same, head (`replayed:true`) | 200 | 200 | **200** | **200** | 403 | 403 | 403 | 401 |
| vc-issuer POST /api/status (create), develop | 201 | 201 | 403 | 403 | 403 | 403 | 403 | 401 |
| the same, head | 201 | 201 | **201** | **201** | 403 | 403 | 403 | 401 |

- **The vc-issuer writes were read back:**
  - develop's `GET /api/status` lists default plus 2 created lists;
  - the head's lists default plus 4.
- **Develop's documents row shows the disagreement KS-1701 removes:** SUPER_ADMIN passed the adminConfig gate but was scoped out of the documents list.
- **Not driven:** the gateway approval override over a booted gateway (it was driven only by the cells and my probe, through the real router with an injected user) and the vc-issuer owner-less presentation read (cells and the no-loss run only). Evidence: `evidence/proof/`.

**Q6 WHOLE and WORDS.**
- **Suites WHOLE, develop d59c623e → head** (failure-name sets compared):

| suite | develop | head |
|---|---|---|
| originate | 3442/3442 | 3610/3610 |
| billing | 507/507 | 525/525 |
| vc-issuer | 893/893 | 939/939 |
| api-gateway | 2376/2376 | 2401/2401 |
| packages/shared | 1742/1743 | 1746/1747 |

  - In packages/shared, the one failure is IDENTICAL on both arms: `wallet-signature … KS-278 accepts a valid wallet signature over the message`.
  - The 33 names dropped (originate 29, vc-issuer 4) are exactly the flipped pins and ks586's renamed rows. No cell was deleted without a replacement.
- **Static:**
  - tsc `--noEmit`: rc 0 on all five packages on both arms. The planted control gives rc 2.
  - eslint on the touched .ts files: 0 errors and the same 2 gateway warnings on both arms. The planted control gives 2 errors.
  - `docs-fragments.mjs check`: OK on both arms, with the same 2 ADVISORY lines.
- **Overlap:** 19 open PRs, 159 file rows. None of the 35 paths is in any other PR. The positive control is 2289 itself, which matched 35/35.
  - **PR 2288 is OPEN and disjoint.** merge-tree with it in both orders gives tree 2ecb130d (G413-2289-6).
- **merge-tree at develop d59c623e:** caf79cec in both orders. The planted control (a develop-side edit to the billing `requireRole` line, local commit c06c1177 that was never pushed) gives rc 1 with 1 CONFLICT in both orders.
- **The STATUS_WRITE_ROLES removal:**
  - At the head, no source file imports the name. Every remaining hit is prose: comments in status.ts and the vc-issuer tests, `docs/security/ROLES-AND-AUTHORIZATION-INVENTORY.md:108`, and docstrings in 4 schemathesis files. None of the schemathesis files reads status.ts.
  - At develop there were 3 test importers, plus status.ts's definition as the positive control.
- **Words:** the PR body, Test Evidence and facts comment f4292579 were read whole, read-only. The key was read inside python from the project's `.env` and never printed.
  - Every sentence holds except G413-2289-3 (31 vs 34), G413-2289-2 (the frontends list is incomplete) and G413-2289-4 ("refusing an array role" at the gateway role step).
  - The figures that reproduce: 66 new red; 257 new cells (168, 18, 42, 25, 4); 16 changed cell files; 52 to 44 and 29 to 22; the five suite pairs; tree caf79cec; "no open PR touches the 35 paths"; "its only importers were three tests"; the census's 155 lines.

## Siblings found (listed, not acted on)
- `frontend/admin/src/store/authStore.ts:23-25` and `Profile.tsx:105` and `:111` (G413-2289-2).
- The ratchet covers only the 7 lowered entries, and G1 does not see four other shapes of check (G413-2289-1).
- The gateway approval override throws, unanswered, on an array role at a role step. This is pre-existing (G413-2289-4).
- The auth sites deferred behind PR 2288 are as listed on KS-1701.

## Two-NO-GO cap
Not engaged.

## Faults, disclosed
- **A hook refusal that ran nothing:** a `=====` separator.
- **My first planted merge commit failed** for lack of a committer identity, so `merge-tree` received an empty argument and printed usage (rc 129). It proved nothing and is not counted. I re-ran it with a local identity on a temporary index; the result is above.
- **My first gateway probe sent an array role on a role step.** The request hung and timed out (that run is G413-2289-4's evidence). The re-run excluded that one case.
- **Overlapping runs:** the guard plants (2 shared test files, about 30 s) ran while the background whole-suite run was on its head arm; load was 20.6 at their start. The whole-suite figures equal the seat's on both arms, and the guard runs had a green control.
- **My first originate proof read `total=None`** for admin callers, because the body was cut at 400 characters. I re-ran originate on both arms with full bodies; that run is in the table.
- **The proof data:** the document row and the webhook event were inserted by SQL into my container only. The vc-issuer status lists were created in-process.
- **No** `cd`, `rm`, push, comment, mail, ticket write or `!CODING` write. The seat's record was not read beyond the commission's two files.

## Not run
- A booted api-gateway (the override was driven through the real router only).
- The admin portal in a browser.
- The four platform suites (Schemathesis, Akto, Playwright, k6), preflight and leg 14's shell suites, and the test-type ratchet (`check:test-types`).
- Node 24.
- Any deployed box or database.
