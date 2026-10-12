# QA gate, round 4: Secuura Platform K PR #1497 (KS-695 ask 3 part ii, the organisation erasure), head 4ca14654

- **Head:** `4ca146545f15010d5b2adf7e022ce3122498e065`. `ls-remote` at 02:36 AEDT gave the same sha for both `refs/pull/1497/head` and `feature/ks-695-ask3-erase-connector-the-erasure-j3`.
  - Parents: `1f0aa1ad4` (the one fix commit on `e6b52ee1`) and `f6f2a539f4a0` (develop, merged in, never rebased).
- **Develop:** `551dc9808aee1c89d217cd662628c17ef8ad3a0e` at 02:36 AEDT. That is one commit past the `92f68da9` in the brief (KS-1520, scripts/preflight).
  - `92f68da9` and `f6f2a539` are both ancestors of it.
  - The three develop commits after the merge-in are `629349da`, `92f68da9` and `551dc980`. They touch only api-gateway `platform.ts`, `services/security/*` and the preflight scripts.
- **How I got the tree:**
  - `git clone --shared` of the Blockchain `2_Project_Files` into my scratchpad.
  - I added a `gh` remote with push disabled, then fetched the PR head and develop over the project's deploy key, read with `config --get`.
  - Worktrees: `head` = 4ca14654, and `merged` = develop 551dc980 plus `git merge` of the head, giving commit `a3b96d0f`, tree `0b9ca314`. `merge-tree --write-tree` predicted the same tree.
  - `npm ci --ignore-scripts`, a shared build and `npm run generate` in both worktrees.
  - I wrote nothing under `!CODING`, and never fetched or checked out there.
- **Database:** my own throwaway PostgreSQL 15.14 on 127.0.0.1:55431, data directory in my scratchpad.
  - Init SQL 11/0 and migrations 49/0, plus platform tenancy.
  - `secuura_app` has rolsuper f and rolbypassrls f. FORCE RLS is t on documents, organizations, svc_api_keys and action_provenance.
  - The database is stopped (`pg_isready` rc 2).
  - I touched no live, Kintsugi, demo or remote system.
- **Gate:** independent Opus, delta gate, round 4, Tier 1 (destructive, GDPR-class), 2026-10-13.

## VERDICT: NO GO

**The author's whole fix list holds. m-A, m-B, N1, N2 and N3 each re-proved on real Postgres in both tenancy modes (the m-A route cells were also run through the real route), and the scale cell reproduces.** The NO GO comes from one new **Major**, found by this round's hostile reading, that no earlier gate tried. Following the brief's severity rule ("any path that erases data it should not ... is a Major"):

**M-1. An organisation-scoped admin of org A can erase org B.**
- **Path 1:** mint a key for org B through `/api/security/keys`, with any `connectorId`, then call erase-connector with it.
- **Path 2:** mint a key for A's OWN organisation carrying B's connector id. A's erasure then also blanks B's connector-made NULL-issuer documents.
- **Where the root cause sits:** in the key mint (security service and gateway), not in the PR's ten files. The PR is the irreversible sink.
- **To get to GO, either:**
  - (a) Wednesday rules M-1 a deploy blocker tracked like KS-1508, and gets a ticket for the mint's organisation arm plus connector-id binding, which must land before KS-695 deploys. The PR is otherwise **GO WITH NOTE** on this head. Or:
  - (b) The author adds an in-PR guard (proposed below) and comes back for a short delta.

## Majors

### M-1. Cross-organisation erasure through an admin-minted connector key (new; root cause outside the PR, sink inside it)

**Path 1: a key for another organisation.**
- `services/security/src/provisioningPolicy.ts:43-49,97-98`: `ORG_ADMIN` and `ISSUER_ADMIN` are `KEY_ADMIN_ROLES`, and `decideMint` returns `allow via admin` at once.
- `services/security/src/index.ts:477-491`: the body's `organizationId` and `connectorId` are free strings.
- `index.ts:1017` calls `decideTenantAccess(user, tenantId)` WITHOUT the `organisationScope` argument.
  - `packages/shared/src/security/keyRevokePolicy.ts:141-164` says that arm is engaged "ONLY when the caller supplies `organisationScope`, so the two existing callers (KS-742's list and mint) keep exactly today's behaviour".
  - So the mint is bounded by tenant only. KS-764 bounded org-scoped admins on REVOKE but not on MINT.
- `services/api-gateway/src/routes/proxy.ts:1189-1192`: `/api/security` is mounted behind `authenticateToken(true)` only.
- The gateway's erase-connector door (`proxy.ts:857-862`, `ERASURE_SCOPE='subjects:erase'`, grace role `connector`) admits any sk_ key while grace is on, and a key carrying `subjects:erase` when it is enforced. An admin mint may carry any scope.
- On the originate side, the PR trusts the key row. `resolveOrganisationErasureTarget` (`connectorOrganisationErasure.ts:105-114`) and the in-transaction check (`:265-284`) compare the key's own `organization_id` and `connector_id` with the claims minted from that same key.
- **Measured (originate half, real Postgres, both modes), cell P8.** A key row for org B with connector_id `forged-by-org-a-admin-<run>`, i.e. what the mint above writes, gives `200 completed documentsBlanked:1`, `Bname=[erased]`, `Bdoc=[erased]`, the forged key `false`, and **B's own provisioned key still `true`**.
- **Not run by me:** the security-service and gateway half (the mint itself). It is read from code at the lines above, which I checked myself after an Explore pass.

**Path 2: a key for A's own org that shares B's connector id.**
- `svc_api_keys.connector_id` has no uniqueness constraint (indexes: pkey, org, prefix, tenant only, read from the live DB).
- Seed arm (b) (`:292-293`) and the lineage arm (`:300`) match `versionedById = 'connector:' + connectorId` by value.
- **Measured, cell P6, both modes:** two organisations whose keys share one connector_id. A erases and gets `200 documentsBlanked:4`:
  - **erased:** B's unissued connector root, B's connector derivative of B's OWN issued document, and B's connector derivative of A's document;
  - **kept:** B's issued document, B's name and B's key.
- This also falsifies the newly published N2 sentence, "another organisation's CONNECTOR derivative survives", whenever connector ids collide. The mint path above lets an org admin choose `platform-s:<B's GUID>` for A's own key. Org-arm-on-mint alone does NOT close this path.
- The constant `'platform-s'` connector id already exists on every tenant's (org-less) metering key (`tenant-provisioning/src/meteringKey.ts:56`). So shared ids are not hypothetical in this system, though an org-less key is refused `unresolvable` here.

**Why Major and not a note:**
- The data destroyed (titles, descriptions and the organisation name) is another organisation's.
- The caller is an org-scoped admin of a different organisation, which KS-764 says must not even revoke B's keys.
- The erasure is irreversible.
- Merging does not deploy (N5 of round 3 still applies), so the harm is after deploy.

**Fix options:**
- (i) Security service: pass `organisationScope` on mint for org-bounded roles, as revoke does, and refuse a caller-chosen `connectorId` from non-provisioners.
- (ii) In this PR, cheap and local: inside the transaction, refuse (403, nothing written) when ANY other organisation's key in the tenant carries the same `connector_id`. Optionally also require `connector_id = 'platform-s:' + <the organisation's stored externalRef>`, the register-connector convention (`api-gateway/src/routes/platform.ts:702`). (ii) closes Path 2 and narrows Path 1. Only (i) closes Path 1.

## Minors

**m-C. The commit-time check runs BEFORE `COMMIT`. Commit-time work is neither in the check nor stopped by `statement_timeout`, so "past it nothing is committed" (published description, yaml line ~31209, `originate.openapi.ts:3727`) is stronger than the code.**
- Where: `connectorOrganisationErasure.ts:383`, then `withTenant` issues `COMMIT` (`db.ts:338` pool branch, Prisma `$transaction` in the other).
- Measured with a deferred constraint trigger on `organizations`, both modes, budget 2 s:
  - P5d: a 2.5 s sleep at commit was **committed at 2,505 ms (T) and 2,506 ms (F)**;
  - P5e: 1.0 s of statements plus a 1.5 s commit was **committed at 2,507 ms (T) and 2,509 ms (F)**.
  - Postgres did not cancel the COMMIT-time trigger at the transaction-local `statement_timeout`.
- Reachability today:
  - The schema has NO deferrable constraints and NO user triggers on documents, organizations or svc_api_keys (read from `pg_constraint` and `pg_trigger`).
  - So the residual is COMMIT latency itself, for example a synchronous-replication or fsync stall on Azure HA, which a statement cancel cannot interrupt.
  - Harm needs COMMIT to exceed the margin between the 25 s budget and the real proxy cut.
- Fix: soften the published sentence ("no statement runs and no commit is attempted after the budget"), or accept and document it. Never a half state: in every cell the row set was all-or-nothing.

## Notes

- **N-a. Test gap, killed only by the gate:** G8 (the commit check moved to BEFORE the revoke and read-back) survives unit 33/33 and bounds 21/21 in both modes. Only my P5f kills it (docs 1.2 s + revoke 1.2 s, 2 s budget, rolled back with `outlived`). Recommend porting P5f into the bounds file.
- **N-b. Coverage, improved by the gate:**
  - The author's unit-only mutants R2 (route stops passing the clock) and R3 (route clock after its reads) are now killed through the REAL route on Postgres by my Q1 (T).
  - R8 (no 1 ms floor) is now killed by my P1b in both modes.
  - MU9 stays unit-only, as the author says.
- **N-c. The response can still arrive after the budget, but it never commits there.**
  - `statement_timeout` is set ONCE, to the remaining budget at transaction start (`:251`). Each later statement may run up to that long.
  - Q4 (same organisation, the first holding the row for 14 s): the second request answered **500 at 27,015 ms (T) and 27,106 ms (F)**, rolled back, no double effect.
  - The worst case is several times 25 s before the rollback. This is data-safe. It is a latency and lock-hold fact for the Platform S retry question.
- **N-d. Single-tenant pre-transaction reads.** In mode F the request-scoped Prisma runs the route's pre-reads inside a 5 s interactive transaction. A slow read therefore ends as `500 "Organisation erasure check failed"` (Q1/Q2/Q3 F: 26.0, 24.0, 24.95 and 24.99 s), never reaching the budget code. Nothing was written. This is pre-existing and not the production branch.
- **N-e. The budget's premise.**
  - The api-gateway proxy for this route has `proxyTimeout`/`timeout` **60,000 ms** (`api-gateway/src/routes/proxy.ts:183-184`). Nothing in the gateway is a 30 s cut.
  - The "30 s proxy" the budget is sized against must be another hop, such as ACA ingress or a front door, which I did not find in the repo.
  - The clock starts at handler entry (`platformOrganizations.ts:84`), after the JWKS verify (bounded 3 s, `packages/shared/src/crypto/jwks.ts:83`) and body parsing.
- **N-f.** The PR body (`pr1497_body_v4.md`) states N2 in "Behaviour changes" and the service header (`:160-168`) and yaml state it too. I read the builder's local copy. The live body was not fetched (`gh` was not used).

## What I ran (all on the merged tree `0b9ca314` unless noted; Postgres cells as `secuura_app`)

**Tenancy mode and the fallback warning.**
- F = `MULTI_TENANCY_ENABLED=false`. T = `true` with `PLATFORM_DATABASE_URL` exported.
- Every log was grepped for `falling back to single-tenant` (`/usr/bin/grep -c -i`): **0 in every F and T log**.
- Positive control: `NOPLAT=1` (URL unset) gave **2** on bounds-T and **2** on the N3 human copy.
- My file's setup line prints `poolBranch=true` in T.

### 1. Topology
- Delta from `e6b52ee1`: `1f0aa1ad4` (6 files, +251/-30: service, route, openapi.ts, yaml, unit, bounds), then the merge.
- My `merge-tree` of `1f0aa1ad4` + `f6f2a539` gives tree `f4ed1f42565e`, **identical to the head's tree**. There is no evil merge.
- All 10 PR files are **byte-identical by blob** across the merge (`1f0aa1ad4` vs `4ca14654`: SAME x10). `git diff 1f0aa1ad4 4ca14654 -- <10 files>` is empty.
- `git log 1158045e..<develop> -- <10 files>` is empty for both the merged-in develop and current develop. Positive control: the same log over `services/security/src/index.ts` lists `92f68da9`.
- Merge onto current develop `551dc980`: rc 0, tree `0b9ca314`. Onto `92f68da9`: rc 0, tree `e04e21b8`.

### 2. Suites and static checks (merged tree)

| Check | Result | Notes |
|---|---|---|
| originate `npx jest`, run twice | **102 suites / 1202 tests**, rc 0 both | |
| `packages/shared` vitest, run twice | **49 files / 954 tests**, rc 0 both | |
| unit file | **33/33** | |
| `tsc --noEmit` | originate rc 0 (0 lines); shared rc 0 | |
| eslint on the PR's 9 TS files | rc 0, empty output | A first run over 49 files included develop's api-gateway files: 8 warnings, 0 errors, none in PR files |
| `check:openapi` | rc 0, `CHECK PASS`, 414 example blocks | |

### 3. The author's integration files, both modes

| File | F | T |
|---|---|---|
| bounds | 21/21 | 21/21 |
| older integration | 15/15 | 15/15 |

### 4. Re-proof of the fix list

**m-A**
- Bounds cells T/U/V are green in both modes, and R1, R5 and R6 each red them (mutants below).
- Through the REAL route, T (production's branch):
  - **Q1:** svc_api_keys was ACCESS EXCLUSIVE locked for 26 s, so the budget was spent inside the route's own key read. Result: **500 at 26,012 ms**, logged `the request had already spent its 25000 ms budget before the transaction began; nothing written`, nothing changed, key true.
  - **Q2:** 24.0 s spent in the read. Result: **200 at 24,032 ms**, committed.
  - **Q3:** 24.95 s and 24.99 s spent. Result: **200 at 24,958 and 24,998 ms**, committed. Both committed inside 25 s, consistent.
  - **B3 (round 3's pool-wait cell):** pool max 10 held 4 s, then a 23 s statement. It **is now 500 at 25,004 ms**, title and key untouched (round 3: 200 at 27,021). Its assertion of the OLD defect therefore reports failed, which is the fix.
- **P1** (direct, production 25 s budget, remaining -5 to 400 ms):
  - F: `already spent` for -5, 0 and 0.3; `57014 statement timeout` for 1 and 2; completed for 5 ms and up.
  - T: `already spent` for -5 and 0; `statement timeout` for 0.3; `outlived` for 1; completed for 2 ms and up.
  - **Every row was all-or-nothing.** The latest completed return was 24,999.9 ms after the start.
- **P1b** (remaining forced to 0.5 ms, organisation row held by another session): cancelled at **10-11 ms** with `statement timeout`, nothing written, in both modes. The 1 ms floor works on real Postgres. R8 (floor removed) reds it.
- **P7:** spent budget gives the `already spent` refusal, nothing written.

**m-B**
- Bounds cell W is green in both modes. R7 reds it, and R4 is the author's (not re-run).
- Round 3's B4 (wall clock stepped back 60 s, then 26 s of statements) is now `the request outlived its 25000 ms budget; rolled back, not committed` at **26,009 ms (T)**, title intact and key true. Round 3 committed it.
- No `Date.now` remains on the budget path: the route uses `:84 performance.now()`, the service `:240, :247, :383`.
- G10 (route clock switched to `Date.now`) is red in unit, in bounds (10 cells, F and T) and in Q1.

**N1**
- Bounds cell N1 is green in both modes. **G1 (issuer guard to `(true)`, both copies) is red in bounds F and T, and unit stays 33/33**, as claimed.
- My P4 also kills G1, in both modes.

**N2**
- Text is present in the service header `:160-168`, `originate.openapi.ts:3723-3727`, the yaml (`check:openapi` pass) and the body draft.
- Behaviour measured, P4 and E1, both modes:
  - B's HUMAN derivative of A's document, titled by B, is **ERASED**.
  - B's connector derivative is **kept**, and so is a human child under it.
  - A B-issued derivative and its human child are **kept**.
  - B's human derivative's human child is **ERASED**. B's human derivative's connector child and its B-issued child are **kept**.
  - A's connector derivative of a B document is **ERASED** (A's own work).
  - B's name and key are untouched.
- r3 X1 still shows `Connector:<B>`, ` connector:<B>` and numeric-`versionedById` children of L's document ERASED, and the exact `connector:<L>` NULL-issuer root ERASED (KS-1508, known).
- **The N2 sentence is false under shared connector ids** (M-1 Path 2).

**N3**
- Scratch copies of `gate1497-e2e`, `gate1497r2-e2e` and `gate1497r2-human` with only the `delete process.env.MULTI_TENANCY_ENABLED;` line removed give **3/3 in F and in T**, with 0 fallback warnings (control: 2 with the URL unset).
- Human cell: `documentsBlanked:3`, src, human and connector all `[erased]`, in both modes.

### 5. Gate files of earlier rounds on this tree

| File | F | T |
|---|---|---|
| r3 attack, fast | 9 passed / 4 skipped | 9 passed / 4 skipped |
| r1 + r2 attack and m1 | 19 passed / 1 skipped | 19 passed / 1 skipped |

- In the r3 file, E1 gave `documentsBlanked:6` in both modes. X1 to X6 are as in round 3.
- r3 slow cells (B3 is T only):

| Cell | F | T |
|---|---|---|
| B1 | 200 at 24,045 ms | 200 at 24,040 ms |
| B2 | 500 at 26,089 ms, nothing erased | 500 at 26,010 ms, nothing erased |
| B3 | not run | 500 at 25,004 ms |
| B4 | rolled back at 26,012 ms | rolled back at 26,009 ms (`outlived`) |

- R5: **500 at 25,099 ms (F) and 25,030 ms (T)**, nothing erased, key true.

### 6. My attack file `gate1497r4-attack` (fast 13 pass in F and in T; slow cells below)

**Partial-failure and commit cells:**

| Cell | What it does | Result |
|---|---|---|
| P5a | the LAST write (revoke) cancelled by `statement_timeout` (2.5 s trigger, 2 s budget) | at 2.0 s name, title, child and key all rolled back. **Retry: 200, alreadyErased false, documentsBlanked 2. Third call: 200, alreadyErased true, 0** (idempotent re-run after a rollback). |
| P5b | AFTER-UPDATE trigger on the key raises | 500, nothing written, key true |
| P5c | deferred trigger raises at COMMIT | 500, nothing written, key true (both branches) |
| P5d, P5e | commit-time work | see m-C |
| P5f | | rolled back (`outlived`), key true |

**Lineage and forged-key cells:** P4 (see N2), P6 and P8 (see M-1).

**Slow cells:** Q1 to Q3 (see m-A) and Q4 (see N-c). In F, Q1 to Q3 end at the pre-read (N-d), consistent, with nothing written.

### 7. Scale

`GATE_N=149000 GATE_BYST=20000 GATE_DEEP=40`:

| Mode | Blanked | Time | Bystanders erased | Key active |
|---|---|---|---|---|
| F | **149,041** | **6,570 ms** | 0 | false |
| T | **149,041** | **6,532 ms** | 0 | false |

### 8. Mutants

- 15 mutants, each applied alone to the merged tree. Each compiled (`tsc` rc 0). **Each was restored byte-identical by sha256**: service `599d4f2e4ef9`, route `abcda71e0632`, `git status --porcelain` clean.
- Layers: unit, bounds F/T, my fast file F/T (a), my Q1 through the real route in T (q).
- The author's 12:

| Mutant | Unit | Bounds F/T | Mine |
|---|---|---|---|
| CTL | 1 | 9/9 | 5/5 |
| MU1 | 1 | 1/1 | 2/2 |
| **G1** | **0** | **1/1** | P4 |
| R1 | 2 | 3/3 | P1b, P7 |
| **R2** | 1 | **0/0** | **Q1-T** |
| **R3** | 1 | **0/0** | **Q1-T** |
| R5 | 2 | 1/1 | P1b |
| R6 | 1 | 1/1 | P7 |
| R7 | 2 | 3/3 | P5f |
| **R8** | 1 | **0/0** | **P1b** |
| MU9 | 1 | 0/0 | 0 (unit-only) |
| MU10 | 0 | 1/1 | 0 |

- This reproduces the author's table where they overlap.
- **My three:**
  - **G8**, check moved before the revoke: unit 0, bounds 0/0, **only my P5f** (N-a).
  - **G10**, route clock on `Date.now`: unit 2, bounds 10/10, Q1-T.
  - **G11**, seed-arm issuer bound dropped (M1 regression): unit 1, bounds 2/2.
- No should-catch mutant survived the full set.

### 9. Merge cleanliness
`git -C merged status --porcelain` is clean after every run. All my scratch test copies were removed from the worktree.

## NOT tested
- The security-service and api-gateway half of M-1: the mint through `/api/security/keys`, JWT forwarding and the erase door's scope check. Read from code only. The originate half is measured (P8, P6).
- api-gateway, auth and security services at runtime; Platform S; any live, Kintsugi, demo or production stack; Azure Postgres, HA or synchronous replication commit latency (m-C is shown with a deferred trigger, not a real stall); pgbouncer.
- A real NTP step. Monotonicity is shown by code reading and the B4 and bounds-W cells, which mock `Date.now`.
- The author's mutants R4, R9, R10, MU2, MU3, MU7, MU8 and MU11 (not re-run).
- The `head` worktree on its own: the PR files are blob-identical, and every run was on the merged tree.
- Schemathesis, Akto, Playwright, k6, and the pre-push preflight or shell leg on the merged tree (develop's `551dc980` touches `scripts/preflight`).
- The live PR body on GitHub.
- `/sign-cert` against a real signer and `/sign-wallet` with a real CIP-8 signature (round 3's E1 stubs them).

## Evidence in this folder
`evidence_topology.txt`, `evidence_suites.txt`, `evidence_runs.txt`, `evidence_mutations.txt`, `gate1497r4-attack.integration.test.ts.txt`, `mut.py.txt`.
