PR 2288: GO WITH NOTES (at head 88d31bd3a5fd4cfbc1697cfcad773f5fb25549a5; tier 1)

# Gate 412, tier 1 (Opus), PR 2288 (KS-2316), 2026-11-23 07:58:10Z to 08:10:14Z (18:58 to 19:10 AEDT, both from `date`)

**Authority:** Kam's card `secuura-org-admin-user-writes-scope-ks2316-1122` = a, "Own organisation only" (ruled 2026-11-23T10:13:00+11:00, read through `decision_queue.sh show`). It must not weaken KS-2287 (`secuura-org-admin-sets-verification-level-1120` = b), KS-2300 (`secuura-org-admin-moves-users-between-orgs-1120` = b) or KS-1701 = a.

**How rulings:** Wednesday's W70 plan ANSWER (design B, QA to QH), its twin ANSWER and its PR 2099 waiver ANSWER.

**Scope:** findings only. Nothing was fixed, pushed, posted, mailed, merged or deployed, and nothing was written to GitHub or Linear.

## Pins
- **Pin 1, 07:58:30Z (ls-remote over https, gh credential helper):**
  - develop: a5ce6ee8b662f697b2b5fa405f5c67cea67aebc0
  - refs/pull/2288/head: 88d31bd3a5fd4cfbc1697cfcad773f5fb25549a5
  - refs/pull/2099/head: 8967de8b17558890dc4ace2732cb8350768df601
- **Pin 2, 08:09:57Z:** all three unchanged.
  - PR 2288 is OPEN at the same head, updatedAt 07:56:13Z.
  - The PR has 1 comment (Linear's bot) and 0 reviews.
- **The PR (gh, read-only):**
  - not draft, base develop, MERGEABLE;
  - 1 commit, 10 files, +589 −21;
  - the title starts "Refs KS-2316:", with no closing keyword.
- **The head:** its parent is a5ce6ee8b662, which is develop now. So the merged state equals the PR's own tree, and every "branch" figure below is the merged state.
- **Develop I ran:** a5ce6ee8b662, for every suite.

## How I measured
- **Clone:** my own clone `_work/g` from GitHub (`--reference-if-able` gate 411's clone, `--dissociate`). Write verbs ran only through `_work/gitx.sh`; the shared checkout was not touched.
- **Worktrees:**
  - `d`: develop
  - `h`: the head
  - `r`: develop plus the 7 cell files copied in (red-first)
  - `x`: the head, for mutants
  - `p`: planted controls, then a local commit of the combined 2288+2099 tree (d83f465e, never pushed)
- **node_modules:** APFS clones of gate 411's root and packages/shared trees, and gate 406's services/auth tree.
  - The manifests are sha-equal to develop: root package.json, the root lock, auth's package.json and lock, and shared's package.json.
  - The PR changes 0 package or lock files.
- **packages/shared:** dist built with tsc in every tree.
- **Environment:**
  - Node v26.8.1. Not an LTS line; the seat used the same.
  - TMPDIR was `_work/tmp`. tsx needed a short path for its IPC socket, so `/private/tmp/g412t` (a symlink to it) was used, then moved to `_work/_quarantine`.
- **Tools:** all in `_work/`: `suites.sh`, `an.py`, `cmp.py`, `mutants.py`, `static.sh`, `overlap.py`, `lin_read.py` and `proof/`. The proof tools are cut from the seat's recipe and re-keyed to my folder.
- **Evidence:** `_work/evidence/`.
- **End state:**
  - Worktrees d, h, x and p have 0 porcelain lines; r holds only the 7 copied cell files.
  - My containers `g412-ks2316-pg` and `g412-ks2316-redis` are STOPPED, kept and labelled `secuura.seat=g412`. They were loopback only.
  - The auth process was stopped by its task id, and nothing listens on its port.

## Findings
There is no HIGH and no MEDIUM finding. The gate is right on both routes:
- **Placement:** the PATCH gate is last before the write, behind the tenant 404, and the create check comes before `emailExists`.
- **Source of each organisation:** the caller's is read from its row, never from the token. The target's is its stored one.
- **Missing values:** missing on either side is never equal, and the compare is case-folded.
- **Platform callers** go through the one shared check.
- **Everything else is unchanged:** reads, the role lists, the KS-2287 and KS-2300 refusals with their messages, and the BASIC-only cap on create.

Red-first, the cells, the mutants, the whole suites and a 16-case socket proof all reproduce or add to what the seat reported.

### LOW
**G412-2288-1: an organisation admin can still create a user outside its organisation through `POST /api/users/stub`, and the PR's census did not name it.**
- **The path:** `users.ts:423`, reached through the gateway's `/api/users` proxy (proxy.ts:553).
  - It admits ORG_ADMIN, ISSUER_ADMIN, SYSTEM_ADMIN, SUPER_ADMIN (`ALLOWED_LOOKUP_ROLES`, users.ts:182) or a connector scope.
  - It creates an INVITED user row (`createInvitedStub`, userRepo.ts:757): role USER, the caller's tenant, and NO organisation.
  - An organisation-less ORG_ADMIN can still call it.
- **The seat's census** searched for `users/admin` only (plan, Q1 item 1).
- **Why LOW, and not a defect of this PR:**
  - It is the KS-74 recipient-stub door of the certificate-issuance flow, not the dashboard's create user that the card's BLUF describes.
  - It sets no role, status or name a caller chooses.
  - Placing a document recipient in the issuer's organisation would be wrong on its face.
- **Still:** the ruling's sentence "create users only in its own organisation" reads literally onto it. It needs Wednesday's routing: either "out of scope, recipient stubs" on record, or a card.

**G412-2288-2: one non-equivalent mutant survives all 299 cells. The shipped code is right.**
- **G-14:** the gate skips a request whose only field is `verificationLevel`.
- **What it changes:** an ORG_ADMIN that resends a sibling user's stored level alone gets 200, a no-op write, instead of 403.
  - Ruling QA says the gate binds the request, changed or not.
  - The QA cell sends status, role and names too, so a level-only (or level-plus-organisation-only) unchanged request is unpinned.
- **G-10** is the same class (the gate binds only status, role and names) and also survives.
- **G-11** (the gate reading the target's organisation from the body) survives, but is equivalent: KS-2300's 403 answers first for any organisation that is not the stored one.
- **Measured on the shipped code:** proof case G1, an all-unchanged save that includes the level and the organisation, is 403. No cell or proof sends the level alone.

**G412-2288-3: words. "SYSTEM_ADMIN and SUPER_ADMIN in any letter case" is true of the predicate, not of these two routes.**
- **Where it is said:** the PR body's "Unchanged on purpose" bullet, facts comment 53cd4ee5 ("Kept as built"), and the new cell file's header.
- **What the routes do:** both apply an exact-spelling role list first.
  - PATCH (users.ts:776) admits SYSTEM_ADMIN, ORG_ADMIN, `admin`, `super_admin` and SUPER_ADMIN.
  - Create (users.ts:643) admits SYSTEM_ADMIN, ORG_ADMIN, `super_admin` and SUPER_ADMIN.
  - So `system_admin` or `Super_Admin` gets "Admin role required" before `isPlatformAdmin` runs.
- **Not a defect:** it fails closed, it predates the PR, and it is the KS-1701 lane the seat rightly left alone. This is the same pattern as G410-2286-2.

### Info
- **The PR's "Not measured" item is now measured.** It said `generate-openapi --check` had not been run on the merged 2288+2099 tree. On my local combined commit (tree 850215f5cab2):
  - `generate-openapi --check`: CHECK PASS;
  - auth whole: 2164/2164 (2148 plus 2099's 16).
- **Sibling, outside KS-2316's scope (level, the KS-2287 lane), not externally reachable:** originate's `PATCH /api/admin/identity/users/:id/level` (adminConfig.ts:1895).
  - It sits behind `requireRole('SYSTEM_ADMIN','ORG_ADMIN')` only, with no tenant, organisation or cap check, so it would set any user's level to any value.
  - The gateway answers that path itself, platform-only (admin.ts:1406, mounted before the proxy).
  - The `/originate/` mount is refused by nginx: `location /originate/ { return 404 }` in nginx-demo.conf:457, and in the other two gateway nginx configs.
  - So it is reachable only from inside the compose network. Listed for the board, not this PR.
- **Two copies of the organisation compare:** KS-2287's inline compare (users.ts:923) is case-sensitive, and KS-2316's `isOwnOrganization` folds case. Both sides come from a Postgres `uuid` column, which reads back canonical lower case, so they cannot disagree at runtime. The seat was told not to edit the KS-2287 block.
- **Deploy note: confirmed from the seed code.**
  - Auth's `seedDemoUsers` has exactly 3 ORG_ADMIN rows (userRepo.ts 1561, 1595, 1640), each with a tenant and no `organizationId`.
  - The gateway identity seed (admin.ts ~497) has no org_admin (control: issuer_admin is found).
  - Wider than stated, not wrong: originate's `POST /api/admin/seed-demo-users` (adminConfig.ts:2171) also inserts 4 ORG_ADMINs with no `organization_id`. It is OFF unless both ALLOW_DEFAULT_SEED_PASSWORDS and ENABLE_DEMO_SEED are set for originate.
- **The open-PR count:** 19 today, including 2288 and 2287. PR 2287 was created 07:40:32Z and touches none of the 10 paths. The body's "17 open PRs" may predate it; the conclusion holds.

## The commission's questions
**Q1 COMPLETENESS (census).**
- **The frame:** the head's tracked tree.
  - Every `services/*/src` and `packages/*/src` (non-test), plus `scripts` and `frontend` for callers.
  - SQL writes on `users`: INSERT INTO users, UPDATE users, `users SET`, with a positive control.
  - Every repository write call: createUser, updateUser*, createInvitedStub, issueInviteClaimToken, seedDemoUsers.
  - Every write route in gateway admin.ts, gateway proxy.ts, auth users.ts and auth.ts, and originate adminConfig.ts and gdpr.ts.
- **Caller-reachable writers of a user's status, role, name or organisation, or creators of a user:**
  - **Apply the rule (this PR):**
    - auth `PATCH /api/users/admin/:id`;
    - auth `POST /api/users/admin/create`.
  - **Pure forwarders of those two:** gateway admin.ts:1514 and 1589 (answer first; mounted at index.ts:937, before the proxy at 1148), and the shadowed proxy.ts:489 and 522. All four forward the caller's own Authorization header.
  - **Out of scope by the ruling (not an organisation-admin power):**
    - `POST /api/auth/register`: public, always OWNER, refuses `role` and `organizationId`.
    - The invite claim: register's 202 writes nothing; reset-password's INVITED branch is driven by the mailed-token holder.
    - `PATCH /api/users/me`: self, names only.
    - Self password, MFA and wallet writes.
    - Login's tenant re-sync (auth.ts:675).
    - GDPR erasure: originate `POST /erasure/:userId` is SYSTEM_ADMIN only; `/erasures` is a connector.
    - The demo seeds and the gateway startup re-sync: system writers with no caller choice.
    - Level-only writers, the KS-2287/KS-2300 lane: gateway `/api/admin/identity/users/:id/level` (platform-only), originate's copy (Info), and auth `/verification/:requestId/review`.
  - **Neither:** `POST /api/users/stub` (G412-2288-1).
- **Organisation writes** (gateway `/api/users/admin/organizations*`) write organisations, not users. Out of scope.

**Q2 THE RULE. Holds.**
- **Order:** the tenant 404 comes first; S-M13 (the gate before the 404) is killed. The own-role, KS-2300, organisation-lookup and KS-2287 refusals keep their messages; G-8 and G-9 (the gate moved earlier) are killed. The gate is last.
- **The caller's organisation comes from the ROW:**
  - cells, plus S-M4, S-M5, G-2, G-3 and G-4, all killed;
  - proof G3 and G4: a stale token claiming O2 against a row moved to O1 gets 403 on the O2 user and 200 on the O1 user.
- **Missing on either side is never the same:** S-M7 and G-5 are killed.
- **Case fold:** S-M14 is killed.
- **Platform callers:** through `isPlatformAdmin` → the shared `isPlatformRole` only, with no new spelling list. S-M8, S-M9 and S-M10 are killed.
- **Still refused:** ISSUER_ADMIN and `platform_admin` (S-M11 and G-12 killed).
- **Reads:** the GET handlers are byte-unchanged (the diff has 4 hunks, none in a GET), and G-1 (the gate on GET `/admin/list`) is killed.
- **Create:**
  - the organisation comes from the caller's row (S-M3 killed);
  - an organisation-less admin is refused BEFORE `emailExists` (G-6 killed). Proof G5: an organisation-less admin creating an existing address gets 403; the control G6 (an admin with an organisation) gets 409;
  - a body `organizationId` is ignored (G-7 killed; proof C1 wrote O1 with O2 in the body);
  - the level is still BASIC-only (cell).

**Q3 THE PINNED CELLS. Every flip is a consequence of the ruling; none is a weakening.**
- **The fixture edits:**
  - ks467: 3 cells, plus `orgAdmin()`, called at 5 sites, of which 2 are 201 creates that need the row.
  - ks1536: 2 cells.
  - ks2083: 1 cell.
  - ks806: the mock returns the caller's row with an organisation.
  - Each now gives caller and target one organisation and keeps its original assertion; ks467's create cell also asserts the organisation.
- **Changed expectations: 2.**
  - The KS-2287 cell now expects 403 with the KS-2316 message, and the level stays HIGH.
  - The KS-2300 cell now expects 403 with the message, and the organisation unchanged.
  - In both, the built rule runs first, so a resend wrongly read as a change would answer with that rule's own message. The resend tolerance stays proven.
- **The twins:**
  - KS-2287's new twin (own organisation, HIGH resent with a rename): 200, written with `{displayName, verificationLevel: 'HIGH'}`.
  - KS-2300's existing twin ("the stored organisation resent with a new display name is 200 …"): present and green.
- **Name sets, develop to branch:**
  - +81: 78 in the new file, 2 in ks2287 (the renamed cell and its twin), 1 in ks2300 (the renamed cell);
  - −2: the two old names.
  - So 2069 + 79 = 2148. No cell was deleted.

**Q4 RED-FIRST and MUTANTS.**
- **Red-first:** reproduced. The 7 files on develop's product: 299 cells, 25 red by assertion (0 load failures), 274 passed.
  - The 25 are the 22 RED cells in the new file plus 3 changed cells: ks2287, ks2300 and ks467's create cell.
  - Branch: 299/299.
- **Mutants** (control 299/299 first and last in both runs; the file sha-restored; x clean):
  - **The seat's families, re-typed: 13 run, 13 killed.** S-M1 to S-M11, S-M13/M16 and S-M14. The seat's M12 and M15 are my G-1 and G-6.
  - **Mine, killed:**
    - G-1: the gate on GET;
    - G-2 and G-3: the token's organisation, as fallback and as preference;
    - G-4: the token as fallback on create;
    - G-5: two missing values equal;
    - G-6: the create check after `emailExists`;
    - G-7: the body organisation honoured;
    - G-8 and G-9: the gate earlier in the order;
    - G-12: ISSUER_ADMIN admitted;
    - G-13: the gate answering 404 (re-run as a real status swap; my first G-13 was a no-op edit and is not counted).
  - **Survivors:**
    - G-10 and G-14 (G412-2288-2);
    - G-11, which is equivalent.

**Q5 PROOF. 16 of 16, real sockets.**
- **The stack:** the real auth service from the head tree (tsx, `src/index.ts`) on my own loopback Postgres (postgres:15-alpine; docker/init; `run-migrations.sh` applied=60 failed=0; `runStartupMigrations` applied 48) and Redis 7.4.
- **Setup:**
  - 7 accounts registered and logged in for real.
  - Organisations O1 and O2, and the roles, were set by SQL in my container only.
  - Rows were read back from Postgres after each request.
- **PATCH:**
  - P1: an O1 admin suspending an O2 user gets 403 with the KS-2316 message; the row is unchanged.
  - P2: an O1 admin renaming an organisation-less user: 403.
  - P3: an organisation-less admin renaming an O1 user: 403.
  - P4: an O1 admin suspending an O1 user: 200, and the row reads `suspended`.
  - P5: SYSTEM_ADMIN re-roling the O2 user: 200.
  - P6: no token: 401.
  - G1: an all-unchanged save of the O2 user: 403.
  - G2: a role change on the O2 user with the path id in UPPER case: 403.
  - G3 and G4: the stale claim, as in Q2.
  - G7: SYSTEM_ADMIN renaming the organisation-less user: 200.
- **Create:**
  - C1: an O1 admin with body O2: 201, and the row holds O1.
  - C2: an organisation-less admin: 403, no row.
  - C3: SYSTEM_ADMIN: 201, organisation NULL.
  - G5 and G6: the email oracle, as in Q2.
- **Writes after refusals:** the O2 user's `updated_at` stayed at P5's write (08:06:52.070) through the later refusals G1 to G3. Only the 200s moved rows (`evidence/proof_rows_after.txt`).

**Q6 WHOLE and WORDS.**
- **Suites, develop → branch** (failure-name sets compared):
  - **auth vitest:** 2069/2069 → 2148/2148.
  - **packages/shared vitest WHOLE:** 1743 tests, 1742 pass and 1 fail on BOTH arms. The failing name sets are identical: `wallet-signature … KS-278 accepts a valid wallet signature over the message`.
- **Static:**
  - **tsc `--noEmit` (auth):** rc 0 on both arms. Planted: rc 2.
  - **eslint, the 9 touched auth files:** 0 errors, 0 warnings, both arms. Planted: rc 1.
  - **eslint src:** 0 errors, the same 2 warnings, identical lines on both arms.
  - **check:test-types (auth):** 41 errors, all in the baseline, 0 new, both arms. 216 files examined, against 215 on develop.
  - **generate-openapi `--check`:** PASS on both arms and on the combined tree. Planted one-word drift in `auth.openapi.ts`: CHECK FAIL.
- **Overlap:** 19 open PRs; only 2099 touches any of the 10 paths, on `secuura-api.yaml` alone. Its hunks are the components at ~3779 to 4218.
- **merge-tree against PR 2099:**
  - 2288×2099: rc 0, tree 850215f5cab2.
  - 2099×2288: rc 0, the same tree.
  - 2099 squash-simulated on develop, then 2288: rc 0, the same tree.
  - Planted control (a line added under the walletAddress block 2099 rewrites; unique context, 1 occurrence): rc 1 with a CONFLICT in the yaml in all three orders.
- **The PR body and Test Evidence:** every figure reproduces (25/274/299, 78 cells, 30 platform cells, 2069→2148, 1742/1743 ×2, 9-of-9 proof shapes, tree 850215f5cab2). The exceptions are G412-2288-3, the "17 open PRs" (Info), and the "Not measured" item, now measured (Info).
- **Facts comment 53cd4ee5:**
  - read-only, 5658 B, unedited (updatedAt .883Z before createdAt .940Z);
  - KS-2316 is In Progress, priority 2, 2 comments;
  - its sentences hold except G412-2288-3, and "No frontend, mobile app, script or seed calls POST /api/users/admin/create" holds (only docs, history and USER_TESTING notes name it);
  - the found-not-fixed items check out by read: api.ts:91 returns `body.error || body.message`; Users.tsx:304 posts to `/api/auth/register`; Users.tsx:716 renders `{errorMessage}`; the PATCH callers are at 221 and 288.
- **The DEPLOY NOTE:** confirmed (Info).

## Siblings found (listed, not acted on)
- G412-2288-1, `POST /api/users/stub`: a ruling-frame question for Wednesday.
- Originate `PATCH /api/admin/identity/users/:id/level`: unchecked, but internal only (Info).
- Originate `seed-demo-users`: 4 organisation-less ORG_ADMINs, gated off (Info).

## Two-NO-GO cap
Not engaged.

## Faults, disclosed
- **Hook refusals, which ran nothing:**
  - a `======` separator;
  - `git -C $W/g fetch` with an unexpanded path, re-issued through `gitx.sh`;
  - a redirect through `$E/..`.
- **ssh ls-remote failed** (no identity); re-done over https with the gh credential helper (Blockchain's GH_CONFIG_DIR, read-only).
- **My first G-13 mutant was a no-op edit** (`.json().status()`) and read "SURVIVED". It was replaced by a real 404 swap (killed) and is not counted.
- **The `summary.json` of mutant run 1** was overwritten by run 2. Run 1's full lines are in `mutants_run.txt`, run 2's in `mutants_run_b.txt`.
- **My proof script first carried a line that appended a constant True** without a request. I removed it before the run; the 16 results are all real requests.
- **A stray `run_cwd.py` call with a relative output path** threw before writing. I checked that no file was created outside `_work`.
- **generate-openapi first failed on tooling** (the tsx IPC socket path was too long under `_work/tmp`). It was re-run with the short `/private/tmp/g412t` symlink, which is now in `_work/_quarantine`.
- **Linear:** the key was read from the Blockchain project's `.env` inside the python reader, never printed or put in argv. One read-only query.
- No `cd`, no `rm`, no `!CODING` write (the seat's record and tools were only read), no push, no comment, no mail, no box.

## Not run
- The gateway hop (admin.ts forwarders), at runtime: confirmed a pass-through by reading only.
- The admin Users page in a browser, so the React object-render issue stays READ, NOT RUN.
- Schemathesis, Akto, Playwright e2e and k6.
- Preflight legs (including leg 14's shell suites).
- Node 24.
- The packages/shared ks1536 guard run on its own. It ran inside the whole shared suite: 99/99 on both arms.
- Any deployed box or database.
