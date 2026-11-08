COMBINATION OK WITH NOTES. No cell fails because of the combination: every enumerated suite is green on the union, every suite went red under a planted defect, and the two PRs' code does not disagree about any principal or role. The notes are all pre-existing and identical at develop.

# Gate 258, tier 1 COMPARE: PR 2066 (KS-2032) squashed onto develop abd044f63a9d (after PR 2060 KS-1536 3a and PR 2058 KS-1231)

Relaunch run (the 22:4x seat's RE-PIN). Findings only. Nothing posted, nothing written outside this folder and my clone. Severity is mine; priority is not.

## Pins, read at origin (ls-remote from my clone)

| Reading | develop | refs/pull/2066/head | other |
|---|---|---|---|
| start 2026-11-08T11:45:29Z | abd044f63a9dd5673f1b9ff7a2b1e42e1c26de82 | baf577c78e7f876551e132e407d0982232622de9 | 2060 head 796ea55fb8eb (merged as cfb6c1573ba9), 2058 head 527d67b1852e (merged as abd044f63a9d) |
| end 2026-11-08T12:01:53Z | abd044f63a9d (unchanged) | baf577c78e7f (unchanged) | |

Nothing moved during the run, so the verdict holds for these two SHAs.

## The tree I built

- Clone: /private/tmp/g258 (the dead run's clone, reused as the RE-PIN allowed). I fetched develop and the PR heads inside it. Its old branch `g258-union` (a239c780f, the union on cfb6c1573) is left as it was.
- merge-base(develop abd044, PR head baf577c7) = 35bcfa000b44. `git merge-tree --write-tree abd044f63a9d baf577c78e7f` is clean, with no conflicts.
- **Union tree: 77cd297aa857cda35a1a89b3130bceec07b1938b.** Committed as a squash commit fe9514e5ab55 (parent abd044f63a9d) on branch `g258-union-abd044`. Every run below used this tree.
- B 98th's figure checked: the same merge on cfb6c1573ba9 gives c2940eebfc6db7c11eb39aac6e32df9d0d2cc00d, and that equals the dead run's a239c780f tree. **B 98th's computation is correct for its pin.** The new union differs from it by exactly PR 2058's 7 files (766+/64-).
- **PR 2058's files do not intersect PR 2066's.** `diff --name-only abd044^1 abd044` lists 7 files, all frontend/admin Settings, the ks1231 script cells and two KS-1231 fragments. PR 2066 has 14 files. The intersection is 0.
- PR 2060 and PR 2066 share exactly two files: `Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts` and `Blockchain/Dev/docs/security/ROLES-AND-AUTHORIZATION-INVENTORY.md`. That matches what B 98th said.

## 1. Suites on the union, with controls

Environment: Node v26.8.1 (the host's), node_modules from the dead run's clone, `@secuura/shared` dist rebuilt from the union before every run (services resolve it through a symlink to packages/shared/dist). Integration suites ran against the dead run's private PostgreSQL 15 on 127.0.0.1:55258. The schema is docker/init plus the main-DB migrations, built on cfb6c1573. Neither PR 2058 nor PR 2066 adds a migration. The platform DB is used for originate integration. I stopped that PG by its recorded PID at the end. Workers: 1 to 3, with a load gate (load1 under 7) before each suite.

**Importers, enumerated rather than sampled.** I grepped every non-node_modules `.ts/.tsx/.mts/.js` under Blockchain/Dev for `keyRevokePolicy|isPlatformRole|isPlatformOrOrgBoundedRole|isPlatformOrOrgAdminRole|isScopedAdminRole|isOrgBoundedRole|decideTenantAccess|decideKeyRevoke|decideProvisionerRegistration`. That gives 64 files (list in /private/tmp/g258/_g258/importers.txt). Every test file among them was run. So were the KS-2032 cells PR 2066 added and the KS-1536 cells PR 2060 added, including those that reach the policy only through a route (security ks1585/ks2032, gateway ks1536/ks570/ks745/ks1645/platformRbac/ks480, originate ks1536, auth ks1536).

**Whole-suite run on the union (`runs2/union_full`):**

| Suite | Files | Passed | Failed | Not run |
|---|---|---|---|---|
| packages/shared (WHOLE suite) | 78 | 1613 | 1 (wallet-signature, see N1) | 0 |
| services/security unit (WHOLE suite) | 55 | 533 | 0 | 0 |
| services/api-gateway (WHOLE suite) | 166 | 1840 | 0 | 0 |
| security integration: ks1570, ks1584, ks1585-scope-rows, ks2032-tenant-level-keys (real PG) | 4 | 74 | 0 | 0 |
| auth ks1536-issuer-certs | 1 | 9 | 0 | 0 |
| originate unit: ks1536-adminconfig, ks695-ask3, ks764-admin-api-keys, ks1695 | 4 | 99 | 0 | 0 |
| originate integration ks1594 (real PG) | 1 | 26 | 0 | 0 |
| billing ks1850, ks1888 | 2 | 210 | 0 | 0 |
| governance ks1845, ks1942 | 2 | 55 | 0 | 0 |
| kyc ks1845, ks849 | 2 | 27 | 0 | 0 |
| nft-certificate ks1850 | 1 | 14 | 0 | 0 |
| referral ks1957 | 1 | 25 | 0 | 0 |
| staking ks1845, staking.test | 2 | 62 | 0 | 0 |
| transfer ks1410, ks1845, ks1881 | 3 | 34 | 0 | 0 |
| vc-issuer ks1906, ks692 | 2 | 320 | 0 | 0 |
| wallet-connector ks1845 | 1 | 12 | 0 | 0 |

The KS-1536 guard cells G1 to G7 in `packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts` (97 cells), and the gateway's `ks1536-gateway-role-checks-are-the-shared-predicates.test.ts` (103 cells), are green on the union, with PR 2066's new source inside the guard's sweep (see control E).

After all the plants I ran a final targeted rerun on the restored tree (`runs2/union_final`). It was green in every suite: shared 185, security 132, gateway 146, security integration 74, auth 9, originate 99+26, billing 210, governance 55, kyc 27, nft 14, referral 25, staking 62, transfer 34, vc 320, wallet 12. keyRevokePolicy.ts sha256 was 67e4f5a6...d0 before and after.

**Controls.** One defect at a time. I backed up the file, applied the defect, proved the sha changed, ran all 16 suite groups, restored from the backup and proved the sha256 equals the original. The script is `_g258/plant.sh` and the logs are in `_g258/plants_BF.out`.

| Plant | Defect | Suites that went RED (first failing cell) |
|---|---|---|
| A | keyRevokePolicy.ts:299 `adminIsLive === true` changed to `!== false` (an absent liveness answer allowed) | shared: ks2032 "RED ks2032 P1 mint: adminIsLive absent is refused 403", ks1570. Everything else green, see N3 |
| B | keyRevokePolicy.ts:299 changed to `return true` (PR 2066's rule reverted) | shared ks2032 (7 red), ks1570; **security** ks2032-tenant-level-liveness-read "RED ks2032 R1 mint: no live row answers 403"; **security integration** ks2032-tenant-level-keys "RED status 'deleted', the token still says ADMIN" (15 red) |
| C | keyRevokePolicy.ts:156 drops `\|\| ORG_BOUNDED_ROLES.has(folded)` (PR 2060's predicate broken) | shared ks1536 "RED ks1536 P3 isPlatformOrOrgBoundedRole admits ORG_ADMIN"; **gateway** ks1536-gateway "requireAdmin admits org_admin" (12 red) |
| D | keyRevokePolicy.ts:60 PLATFORM_ROLES without SUPER_ADMIN | shared (18), security (25), gateway (39), security integration (38), **originate** ks1695 and ks1536 O2, **originate integration** ks1594 c18, **billing** B7/A3, **governance** R11/C1, **kyc** R11, **nft** B7, **referral** C3, **staking** R11, **transfer** R11/E13, **vc-issuer** M1/D3, **wallet** R11 |
| E | appended `export const G258_PLANT_ROLES = ['platform_admin'];` to services/security/src/adminScope.ts (a file PR 2066 changed) | shared ks1536 "RED ks1536 G1 platform_admin is a role nowhere in non-test source". This proves PR 2060's guard sweeps PR 2066's files |
| F | services/auth/src/routes/issuerCerts.ts:65 ADMIN_ROLES without ORG_ADMIN | **auth** ks1536 "RED KS-1536 R2 hasAdminRole keeps the truth table" (2 red) |

Every suite group went red under at least one plant: shared (A to E), security (B, D), gateway (C, D), security integration (B, D), auth (F), and originate, originate integration, billing, governance, kyc, nft, referral, staking, transfer, vc-issuer and wallet (D). Every restore was verified by sha256 (keyRevokePolicy 67e4f5a6...d0, adminScope dffe2b6b...f38, issuerCerts 346c8fab...e7e). `git status` is clean apart from my untracked `_g258/` work folder.

## 2. Line-level reading of the union keyRevokePolicy.ts (Blockchain/Dev/packages/shared/src/security/keyRevokePolicy.ts, 423 lines)

- **The hunks are disjoint and independent.** PR 2060 adds lines 147 to 167: two exported predicates, `isPlatformOrOrgBoundedRole` and `isPlatformOrOrgAdminRole`, built only from `PLATFORM_ROLES` (line 60) and `ORG_BOUNDED_ROLES` (line 77). PR 2066 changes lines 194 to 199 (the `adminIsLive` option), 285 to 301 (the scoped-ADMIN arm: an unqualified target now needs `adminIsLive === true`, otherwise 403 'admin not live'), and 368, 374 and 375 (`decideKeyRevoke` passes `adminIsLive` through only when it is resolved). Neither PR edits a line, a set or a function the other reads. PR 2060 does not change `PLATFORM_ROLES`, `ORG_BOUNDED_ROLES`, `SCOPED_ADMIN_ROLES`, `isPlatformRole` or `decideTenantAccess`. PR 2066 does not change any role set or predicate.
- **Each intent survives the other.** PR 2060's intent is one shared list of platform and org-admin roles at the gateway, with no platform_admin; plants C and E prove it is still enforced. PR 2066's intent is that a tenant-level mint or revoke by ADMIN needs a live ADMIN row; plant B proves it is still enforced, at the policy, the security route and real PG.
- **No line where the two disagree about the same principal or role.** Checked role by role:
  - **`ADMIN` / `admin`.** PR 2060's predicates answer false: it is in neither set, so the gateway's admin.ts, proxy.ts and audit-export gates refuse it, as before (the removed local lists never named ADMIN either). PR 2066 treats it as a scoped admin (line 101 to 103, `isScopedAdminRole`, upper-cased) and now requires liveness. The two do not contradict each other: one is the gateway admin-portal door, the other the security service's `/api/keys` door, and neither PR makes ADMIN a platform role. The lowercase `admin` vocabulary split noted at lines 91 and 92 (auth's `PLATFORM_ADMIN_ROLES` at services/auth/src/routes/users.ts:194 still contains `'admin'`) is still true at the union, and it predates both PRs.
  - **`platform_admin`.** platform_admins.role can hold it (docker/init-platform/01-platform-schema.sql:80). PR 2060 removes it from every gate. In this file it was never a platform role, and it is not ADMIN, so PR 2066's arm never sees it. `KEY_ADMIN_ROLES` (services/security/src/index.ts:1152) refuses it before the policy is reached. Same answer from both PRs.
  - **SYSTEM_ADMIN / SUPER_ADMIN.** Both PRs rely on the same `isPlatformRole` early return (line 203). Plant D reds both PRs' cells, which shows they share one definition, and it is consistent.
  - **ORG_ADMIN / ISSUER_ADMIN.** These take PR 2060's predicates and the KS-764 org arm (line 229), which is reached before PR 2066's arm. PR 2066 does not touch them.
- **One pre-existing divergence, not created by the combination (INFO):** `isOrgBoundedRole` and `isScopedAdminRole` (lines 85 and 102) fold with Unicode `toUpperCase()`. PR 2060's two predicates (lines 155 and 165) fold ASCII only, deliberately, as the comment at line 151 says. A claim like `org_admın` (dotless i) is therefore org-bounded at the security service but refused at the gateway's portal gates. For PR 2066's arm, `admın` would read as a scoped ADMIN and be held to the liveness rule, which only narrows access. Role claims are signed and come from the database, so I see no exploit in the combination. It is recorded because the commission asked for any line where the two read a role differently.

## 3. tsc on the union (`tsc --noEmit -p`, `_g258/tsc2/`)

| Project | Result |
|---|---|
| packages/shared/tsconfig.json | 0 errors |
| services/security/tsconfig.json and tsconfig.test.json | 0 and 0 |
| services/api-gateway/tsconfig.json | 0 |
| services/api-gateway/tsconfig.test.json | **25 errors, byte-identical log at develop abd044** (N2) |
| services/originate/tsconfig.json | 0 |
| services/tokenisation/tsconfig.json | 0 |
| services/auth/tsconfig.json | 0 |
| frontend/admin/tsconfig.json (PR 2060 authStore and PR 2058 Settings) | 0 |
| frontend/shared | no tsconfig.json in that directory, not run |

The 25 gateway test-config errors are in csrf.test.ts (10), ks1165 (5), rateLimitEnforce (6), ks1464 (2), ks1374 (1) and ks695-ask3-erase-connector-door (1). None of these files is touched by PR 2058, 2060 or 2066.

## 4. Inventory doc (Blockchain/Dev/docs/security/ROLES-AND-AUTHORIZATION-INVENTORY.md at the union)

- **PR 2060's four edits are present:** line 49 (platform_admin removed from every role check by KS-1536, except password.ts), line 102 (`enforceAdminProxy` with `isPlatformOrOrgAdminRole`), line 193 (x-tenant-override honoured only for `isPlatformRole`: SYSTEM_ADMIN and SUPER_ADMIN in any ASCII case), and line 198 (`isPlatformRole` / `runWithPlatformScope` in admin.ts).
- **PR 2066's edit is present:** line 314 (the mint 403 text without "omit organizationId", and "KS-2032 dropped its 'omit organizationId' clause, because a tenant-level mint now needs a live ADMIN too"). It matches the mint message in services/security/src/index.ts at the union.
- **They do not contradict each other.** Line 314 says ADMIN is "in neither PLATFORM_ROLES nor ORG_BOUNDED_ROLES", which is still true after PR 2060 (it changed neither set). Line 49 says platform_admin is gone from every role check, and that stays true with PR 2066's new source: guard G1 is green on the union and plant E proves it sweeps adminScope.ts. The two rows describe different doors and neither restates the other's rule.
- Minor and pre-existing, not a contradiction: line 314 still describes the KS-1570 behaviour in prose and does not name KS-2032's tenant-level liveness rule as a rule of its own. It names it only in the parenthesis.

## Notes

- **N1, INFO, pre-existing.** `packages/shared/src/__tests__/wallet-signature.test.ts` "accepts a valid wallet signature over the message" fails deterministically. It fails alone on the union and alone at develop abd044 ("1 failed | 4 passed", `_g258/runs2/ws_develop.log`). Neither PR touches it or its source. It is most likely an Ed25519/CBOR behaviour of Node v26.8.1. It does not touch keyRevokePolicy.
- **N2, INFO, pre-existing.** The api-gateway tsconfig.test.json has 25 errors, identical at develop. See section 3.
- **N3, LOW, test-depth.** PR 2066's "an ABSENT liveness answer is refused" rule (keyRevokePolicy.ts:299, `=== true`) is pinned only by the pure-function cells (shared ks2032 P1, ks1570). Under plant A every route-level and real-PG suite stayed green, because both security call sites always resolve `adminIsLive` to a boolean for an ADMIN. That is correct today. But if a future call site forgets the read, only the shared cells would catch it. This is not a combination defect, and it is the same at PR 2066 alone.
- **N4, INFO.** The Unicode-versus-ASCII fold divergence between the KS-764/KS-1570 role tests and PR 2060's predicates is described in section 2. It predates both PRs and does not make the combination wrong.

## NOT TESTED

- No live stack, no box, no docker, no real gateway-to-security hop. The gateway-to-security `/api/keys` path was not driven end to end; each side was tested in its own suite.
- The whole-suite runs covered only packages/shared, services/security unit and services/api-gateway. The other services ran only the enumerated importer and KS cells, not their whole suites. Originate ran only its four importer and KS-1536 unit files and its ks1594 integration file.
- services/auth was not run as a whole suite, only ks1536-issuer-certs. Auth integration suites were not run.
- The security integration DB schema was built (by the dead run) from cfb6c1573's migrations. Neither PR 2058 nor PR 2066 adds a migration, so I judged it equivalent, but I did not rebuild it.
- Frontend tests (admin, shared) were not run. PR 2058's ks1231 script cells were not run: they are outside the question and share no file with PR 2066.
- PR 2066 was not re-gated (gate 245 stands). Nothing in the PR bodies or ticket comments was checked.
- Cards were not re-read through decision_queue.sh. This commission cites none beyond the cards named in code comments.

## Conduct

- I never used `cd`. Every git write verb (fetch, commit-tree, checkout) ran only in /private/tmp/g258. Nothing was written under /Volumes/DevMASTER/!CODING/, which was read for nothing but the remote URL and deploy-key path.
- No files were deleted. **The clone is left at /private/tmp/g258, 2.5 GiB** (it includes `_g258/` with the logs, plant backups and the stopped PG data dir), as the commission's no-rm correction requires. The common file's "remove it at the end" is overridden by the commission.
- The dead run's PostgreSQL (PID 29526) was found running and was stopped by its recorded PID ("pid 29526 gone"). Its data was not removed.
- Load: two moments over 8 (8.15 after the first whole-suite run at 3 workers, 8.69 after plant A at 2 workers; the host was already at about 7 to 8 from other work). After that I cut workers to 1 and gated each suite on load1 under 7. No later reading went over 8.4 on the 5-minute average, and none over 8 on the 1-minute reading at a suite start.
- DevMASTER free space: 23 GiB at start and 25 GiB at end, never under 12.
- A hook refused `git -C $G fetch` with an unexpanded variable path. The same verb with the literal /private/tmp/g258 path was accepted. merge-tree was not refused, so no scratchpad clone was needed.
