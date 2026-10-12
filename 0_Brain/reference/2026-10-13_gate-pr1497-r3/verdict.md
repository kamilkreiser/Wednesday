# QA gate, round 3: Secuura Platform K PR #1497 (KS-695 ask 3 part ii, the organisation erasure), head e6b52ee1

- **Head:** `e6b52ee151fff5bb2687ee4c4d59c3a5974d61ba`. It is ONE commit on `6454dc9cb6a751b243d20e4c7a7c946791dd80a2`, the head the round-2 gate said NO GO to (`rev-list --parents`: parent `6454dc9c`; `rev-list --count 6454dc9c..e6b52ee1` = 1). Delta: 3 files, +288/-27 (the service, the unit file, the bounds integration file). Whole PR on `1158045e`: 10 files, +1547/-51.
- **Bundles:** full `4fcb561c87fa7b12` (needs `1158045e52b8`), delta `f270995752c8f94d` (needs `6454dc9cb6a7`). Both gave `git bundle verify` rc 0 in my clone. The delta bundle fails in an empty repo ("Repository lacks these prerequisite commits: 6454dc9c..."), which is expected.
- **Real develop:** `git ls-remote origin refs/heads/develop` at 00:54 AEDT returned **`c63cec1f6070e06009969526615011dc8734ac13`**. That is newer than the `36f0f56f` in the brief. I fetched it read-only into my scratch clone.
- **Merged tree:** a local merge of e6b52ee1 into c63cec1f gave commit `d527e622`, tree `64698cca2198`, with **no conflicts** (rc 0).
  - Develop is 12 commits past the PR base (47 files, +2111/-113), and **none of them touch any of the PR's 10 files** (`comm` of the two name lists is empty).
  - What the merge pulls into originate's source: `routes/verification.ts`, `services/anchorStateSync.ts`, `utils/blockHeight.ts`, plus a new suite, `ks1333`.
  - It also pulls in `scripts/preflight/*`, `scripts/__tests__/*.sh` and `scripts/typecheck-tests/*`. So the builder is right that the shell leg must run in full at merge time.
  - No migration or lockfile changes, and no changes to `db.ts`, `routes/documents.ts`, the security service or packages/shared revoke code.
- **How I got the tree:** I cloned with `--no-hardlinks` from my own earlier scratch clone and fetched the bundles and develop into it. Nothing was written under `!CODING`, and I never fetched or checked out inside it; its `git status` is not mine to change. I ran `npm ci --ignore-scripts` in BOTH scratch worktrees, so **no symlinked node_modules**, because the project install has no generated Prisma client. Then I built `packages/shared` and ran `npm run generate`.
- **Database:** my own throwaway PostgreSQL 15.14 on 127.0.0.1:55419, TCP only, with its data dir in my scratchpad. Init SQL: 11 applied, 0 failed. Migrations: 49 applied, 0 failed, plus platform tenancy. `secuura_app` has rolsuper=f and rolbypassrls=f. FORCE RLS is t on documents, organizations, svc_api_keys and action_provenance. The database is now stopped (`pg_isready` rc 2). No real database, Kintsugi, demo or remote box was touched.
- **Gate:** independent Opus, full delta, Tier 1 (destructive GDPR path), 2026-10-13.

## VERDICT: GO WITH NOTE

**Every item on the round-2 list is fixed on this head, in both tenancy modes, through the real routes. I found no cross-organisation attack that blanks another organisation's issued document or revokes another organisation's key, and every partial-failure path I tried rolled back as a whole.**
**Two Minors remain, both on the 25 s budget, and both are unsafe only after deploy (merging does not deploy): the budget clock starts inside the callback, not at the request (a commit at 27.0 s was measured), and it is a wall clock that a backward step defeats (measured: committed at 26 s in production's pool branch). Fix both before KS-695 deploys. Neither blocks the merge.**

## By my runs

All runs were on the merged tree `64698cca` unless I say "head". Every Postgres-backed cell ran as `secuura_app` (the role probe printed `{"who":"secuura_app","su":false,"bp":false}`) in `MULTI_TENANCY_ENABLED=false` (F) and `=true` (T). Raw lines are in `evidence_runs.txt`, `evidence_mutations.txt` and `evidence_redfirst_scale.txt`.

### 1. The author's files

| File | F | T |
|---|---|---|
| bounds | 16/16 | 16/16 |
| older integration | 15/15 | 15/15 |
| unit file | 28/28 | (no DB) |

### 2. The gate's own eight files

- The files are the round-1 and round-2 copies from `0_Brain/reference`. `cmp` shows each is byte-identical to the builder's copies.
- Result: **24 passed, 1 skipped** in F and in T. The skip is R5, which needs `GATE_SLOW=1`.
- M-A, human cell: `GATE human A erase 200 ... documentsBlanked:3 after {"src":"[erased]","human":"[erased]","connector":"[erased]"}`. On 6454dc9c it was `human:"A contract with Jane Citizen.pdf (watermarked)"`, and I re-ran that red (below).
- N-B: `R2 TAB 200 completed | retry 200 alreadyErased:true | keyActive=false`, and the same for NBSP. It was 500 then 500 on 6454dc9c.
- R5, a 27 s statement against the 25 s budget, `GATE_SLOW=1`:
  - F: **500 at 25,120 ms**.
  - T: **500 at 25,033 ms**.
  - In both modes `S1=S doc.pdf`, the organisation name is unchanged and `keyActive=true`. Nothing was erased.
  - The caller sees `{"code":"INTERNAL_ERROR","message":"Organisation erasure failed. Nothing was erased."}`.
  - Round 2 measured T committing at 27 s.

### 3. My attack file, `gate1497r3-attack`, in both modes

**Fast cells: 9/9 green in F and in T.**

- **E1, the real routes** (`/api/documents`, `/version`, `/sign-cert` with the auth-service fetch stubbed, `/sign-wallet` with `verifyMessageSignature` mocked, then erase-connector). All 7 creates answered 201.
  - A's erasure gives `200 completed documentsBlanked:6`.
  - Blanked: src, the human /version, the human /sign-cert, the human /sign-wallet and the human grandchild.
  - **B connector's /version of A's document survives** (`A contract with Jane Citizen.pdf (watermarked)`, the m3 ruling).
  - **B's HUMAN /version of A's document, with B's own `title: "B human own title.pdf"`, is blanked** (Note N2).
  - B's name and key are unchanged.
  - This is also the first both-mode run of the human-derivative path (see N3).
- **X1, lookalikes. L erases, and nothing that is B's is touched.**
  - L's erasure answers 200 with 5 documents blanked.
  - **kept:** NULL-issuer roots with versionedById `connector<id>` (no colon), `Connector:<id>`, ` connector:<id>` (leading space), `connector:<id> ` (trailing space) and an upper-case GUID. Also kept: a B-issued doc claiming L, a B-issued child of an L doc, and B connector's child of an L doc.
  - **ERASED:** the exact `connector:<L>` NULL-issuer root (the positive control; this is m-1 / KS-1508, already known). Also erased: children of L's doc whose versionedById is `Connector:<B>`, ` connector:<B>` or the number `42`. These are followed because they do not match `LIKE 'connector:%'` (N2).
- **X2:** a named key with `organization_id` NULL gets **403**, and the title, name and key are unchanged.
- **X3:** a named key with NULL `is_active` gets `200 completed alreadyErased:false`, and the named key is now false. A sibling NULL key of the same organisation stays **null**, and **another organisation's NULL key stays null**. The repeat answers `200 alreadyErased:true`.
- **X4:** the key was moved to org B after the target was resolved (a stale target, calling `eraseConnectorOrganisation` directly). The result is `OrganisationErasureForbiddenError`, K's title and name are intact, and the moved key is still active.
- **X4b:** a key move tried DURING the erasure (a 3 s trigger) **waited 1,805-1,807 ms** on the `FOR UPDATE` lock and landed after the erasure committed. The erasure answered 200, and the key was revoked first.
- **X5:** two concurrent erasures of the same organisation both answered **200**. One gave `documentsBlanked:2, alreadyErased:false` and the other `0, alreadyErased:true`. No 500s and no double count.
- **X6:** two concurrent erasures of different organisations whose lineages touch. C1 blanked 2: its own document and its human derivative. It did **not** reach the C2-issued child, or C2 connector's derivative, of C1's document. C2 blanked 3, its own.

**Slow cells (`GATE_SLOW=1`):**

| Cell | F | T |
|---|---|---|
| **B1:** a 24 s statement | **200 at 24,034 ms**, committed, key false | **200 at 24,042 ms**, committed, key false |
| **B2:** two 13 s statements (each inside statement_timeout, 26 s in total) | **500 at 26,117 ms**, nothing erased, key true | **500 at 26,011 ms**, nothing erased, key true |
| **B3:** the default pool (max 10) held for 4 s, then a 23 s statement | skipped (T only) | **200 at requestMs=27,021**, committed (**m-A**) |
| **B4:** the wall clock steps back 60 s, then 26 s of statements | rolled back by Prisma's own timer: "timeout ... 25000 ms" | **completed, committed at 26,009 ms** (**m-B**) |

- B2 in F was stopped by Prisma's timer ("expired transaction ... 26009 ms passed").
- B2 in T was stopped by the new commit-time check, which logged `"erase-connector: the transaction outlived its 25000 ms budget; rolled back, not committed"`.

### 4. Red first on the old service

I swapped in 6454dc9c's service file and changed nothing else.

- **bounds: 6 failed, 10 passed in F and in T.** The six are M-A, N-B TAB, N-B NBSP, N-B NULL-flag, m-2 lock-wait and m-2 outlives-budget. This matches the builder's "6 of 16".
- My file: E1, X3, X4, X5 and X6 are red in both modes, and B2 is red in T only (`200 completed at 26,047 ms`, committed).
- The gate's human file is red.
- The unit file does not load against the old service ("Tests: 0 total"). That is a load failure, not a red.
- The service was restored to sha256/16 `909c2cbe3630e713`, the same as before.

### 5. Suites and static checks

- **Merged tree:**
  - originate `npx jest`, run twice: **102 suites / 1197 tests**, rc 0. The extra suite is develop's ks1333, with 10 tests.
  - `packages/shared` vitest, run twice: **49 files / 954 tests**, rc 0.
  - `tsc --noEmit`: rc 0 in originate (0 lines) and in shared (1 line, an npm warning).
  - eslint on the PR's 9 TS files: rc 0, empty output.
  - `check:openapi`: rc 0, `CHECK PASS`, 414 example blocks.
- **Head:** originate gives **101 / 1187**, rc 0, which is the builder's figure.
- **Typecheck ratchet:** `node scripts/typecheck-tests/check.cjs services/originate` gives rc 2, "no tsconfig.test.json". **originate is not under the ratchet.** The positive control, api-gateway, gives rc 0: "35 errors: 35 in the baseline, 0 new".
- **KS-764 guard line:**
  - The `if (!decision.allow) throw new OrganisationErasureForbiddenError('keyId');` text is identical at 6454dc9c (line 228) and e6b52ee1 (line 256). Only the line number moved.
  - The delta touches nothing under `packages/` (empty `diff --stat`).
  - The guard lists the file at `ks764-key-revoke-call-site-guard.test.ts:97`.
  - The shared suite is green, as above.
- **api-gateway:** the PR changes nothing under `services/api-gateway`, from base to head (empty `diff --stat`). Its only erase-connector references are the KS-695 (i) door test and the proxy and platform route mounts. Unchanged, so not re-run.

### 6. Scale

`GATE_N=149000 GATE_BYST=20000 GATE_DEEP=40`, using the builder's parameters:

| Mode | Blanked | Time | Bystanders erased | Key active |
|---|---|---|---|---|
| F | **149,041** | **6,308 ms** | 0 | false |
| T | **149,041** | **8,073 ms** | 0 | false |

### 7. Mutants

19 mutants, each applied alone to the merged tree. Each one compiled (`tsc` rc 0), and **each was restored byte-identical by sha256**. `git status` was clean afterwards. The runner is `mut.py.txt`.

**The builder's twelve (CTL + MU1-MU11), all run, all reproduce the PR table:**

| Mutant | Unit | bounds F | bounds T | Other |
|---|---|---|---|---|
| CTL | 1 | 7 | 7 | |
| MU1 | 1 | M-A | M-A | |
| MU2 | 1 | 0 | 0 | |
| MU3 | 1 | 4 | 4 | |
| MU4 | 2 | lock-wait | lock-wait | |
| MU5 | 1 | no-leak | no-leak | |
| MU6 | 1 | budget | budget | also my B2-T |
| MU7 | 1 | TAB+NBSP | TAB+NBSP | |
| MU8 | 1 | NULL-flag | NULL-flag | |
| MU9 | 1 | 0 | 0 | also my X4 in F |
| MU10 | 0 | X3 | X3 | |
| MU11 | 0 | m2 6 s | 0 | |

- MU2 is unit-only, and MU10 is Postgres-only.
- MU9 is unit-only in the PR's own tests, and my X4 also kills it.

**My seven:**

| Mutant | What it does | Unit | bounds F/T | Killed by |
|---|---|---|---|---|
| **G1** | lineage ISSUER guard dropped (cross-org) | 0 | 0 / 0 | **my X1 (F, T) and X6 (F)** only (N1) |
| G2 | revoke `organization_id` predicate dropped | 2 (text pins) | 0 / 0 | not my file either. An equivalent mutant: the FOR UPDATE lock plus the JS ownership check already bound the row (N6) |
| G3 | key-lock `FOR UPDATE` dropped | 20 (statement classifier) | 0 / 0 | my X4b (F, T) |
| G4 | db.ts pool `catch` COMMITs instead of ROLLBACK (rollback) | 0 | 0 / **3** | my B2-T |
| G5 | seed arm (b) case-insensitive (cross-org) | 1 | 0 / 0 | my X1 (F, T) |
| G6 | statement_timeout +10 s (rollback) | 1 | lock-wait / lock-wait | |
| G7 | budget check +2 s (rollback) | 1 | budget / budget | |

G4's three bounds-T reds are m1, N-D/X3 and the budget cell.

**No should-catch mutant survived the full set.** G1 and G5 survive everything the PR ships except a text pin (G5) or nothing at all (G1).

## Rulings on the builder's decisions

**(1) A NULL `is_active` key is revoked to false: KEEP.**
- It is reachable: the column is nullable, with default true (`information_schema`: `is_active|YES|true`). So it takes an explicit NULL write or upsert.
- The security service maps it with `isActive: Boolean(r.is_active)` (`services/security/src/index.ts:474`, `converters.ts:134`). So a NULL key already cannot authenticate, and writing false changes no authentication result. It only ends the permanent-500 loop.
- It changes no other caller's result. Only this UPDATE's predicate changed; the security service's own rotate-revoke still uses `is_active = true`.
- X3 proves the scope: a sibling NULL key of the same organisation and another organisation's NULL key both stay NULL, and the repeat answers `alreadyErased:true`.
- Safe for the owning organisation.

**(2) The commit-time budget check: KEEP, and CHANGE how it measures.**
- It is the check that actually fires in production's pool branch: B2-T logged its exact message, and MU6 and G4 are killed by it.
- But it uses `Date.now()` with `startedAt` taken inside the callback.
- Change it to a monotonic clock (`performance.now()` / `process.hrtime.bigint()`). Take the deadline at handler entry, or pass it into `eraseConnectorOrganisation`, so the connection wait and the pre-transaction reads count against it. These are m-A and m-B.

**(3) Rollback at the end, and statement_timeout bounding every statement including lock waits: KEEP.**
- R5 gives 500 at 25.1 s (F) and 25.0 s (T) with nothing erased.
- B1 shows 24 s commits in both modes.
- B2 shows 26 s split over two statements is rolled back in both modes.
- The setting is transaction-local (MU5 is killed by the no-leak cell).
- A second concurrent erasure that waits more than 25 s gets a 5xx that S retries. X5 at normal speed answers 200 / `alreadyErased:true`.
- Every write is in one `withTenant` transaction: `withTenant`'s pool branch ROLLBACKs on any throw (`db.ts:340-343`), and the route performs no writes. I found no path where a partial erasure commits.

**(4) The lineage arm follows any non-connector `versionedById` (FIX2): KEEP, and disclose the consequence.**
- E1 and the gate's human file pass in both modes, for /version, /sign-cert, /sign-wallet and a grandchild.
- The consequence: a derivative that ANOTHER organisation's HUMAN made of this organisation's document is blanked, including a title that human wrote (N2).
- **m-1 placement check:** the PR body states Wednesday's KS-1508 ruling in the first block, "Gate status", line 12: "KS-1508 ... must land BEFORE KS-695 deploys". The "NOT run" and live-check lines repeat it. I read this from the builder's local `pr1497_body_v3.md`, which its handover says was read back byte-exact. I could not fetch the live body (see Not measured).

## Findings

### Major

None.

### Minor

**m-A. The 25 s budget is measured from inside the transaction callback, not from the request, so the "never commit after the 30 s proxy cut" guarantee holds only when getting a connection is instant.**
- Where: `connectorOrganisationErasure.ts:226` sets `startedAt = Date.now()` inside `withTenant`'s callback. The check is at `:361`.
- Before the callback runs:
  - the pool branch waits on `pool.connect()` (`db.ts:328`; `connectionTimeoutMillis: 5_000`, `tenant-pool-manager.ts:252`);
  - the Prisma branch has a 5 s `maxWait`;
  - the route's two pre-transaction reads can each wait for a connection too.
- Measured in B3, mode T: the pool was held for 4 s, then a 23 s statement ran. The result was **200 committed at requestMs=27,021**, past the 25 s budget. The worst case, about 5 s of wait plus 24.9 s, commits at roughly 30 s or later.
- Consequence: S has already been told 5xx, and it retries with the revoked key. That is the open Platform S retry question, which already blocks deploy, so the harm is bounded.
- Fix: take the deadline at handler entry and pass it in. Before deploy.

**m-B. The commit-time check uses the wall clock. A backward clock step makes it pass a transaction that outlived the budget.**
- Where: `:226` and `:361`, `Date.now()`.
- Measured in B4: the clock stepped back 60 s, then 26 s of statements ran.
  - **T (production's branch): completed and committed at 26,009 ms.**
  - F: rolled back anyway, by Prisma's own timer.
- The builder's note says "fails safe". That is true only for a forward step.
- Fix: one word, `performance.now()`. Before deploy.

### Notes

**N1. The lineage ISSUER guard, the cross-organisation boundary on arm (c), is not pinned by any test the PR ships.**
- G1 replaced `c.issuer_organization_id IS NULL OR c.issuer_organization_id = org` with `true` in both copies. It stayed **green on unit 28/28 and on bounds 16/16 in both modes**. Only gate-side files kill it: my X1 and X6, and round-2's R1 (AX2).
- G5 (seed arm (b) made case-insensitive) is seen only by a unit text pin.
- Recommend porting one real-Postgres cell (an X-issued child of this organisation's document survives) into the bounds file before merge. This is the same family as round-2's N-D; the integration suites are still run by no CI gate (KS-1474).

**N2. FIX2 follows ANY value that does not start with `connector:`.**
- E1: B-org HUMAN's /version of A's document, carrying B's own title, is **blanked by A's erasure**, while B's CONNECTOR derivative of the same document (which carries A's title) survives under the m3 ruling.
- X1: children whose `versionedById` is `Connector:<B>`, ` connector:<B>` or a number are followed. Seeds are matched exactly, so a lookalike never makes a root another organisation's.
- A writer can still hide its own derivative from its own organisation's erasure by writing `metadata.versionedById: "connector:x"`. The bounds m3 CONTROL proves such a value is not followed. This is KS-1508 residue.
- None of this reaches an issued document of another organisation (X1, X6, G1). But the published spec ("never one issued by another organisation or versioned by another connector") does not tell Kam that another organisation's human derivatives, and their caller-set titles, are blanked. Add it to the "not reached / reached" disclosure.

**N3. Evidence correction.** Three gate files (`gate1497-e2e`, `gate1497r2-e2e`, `gate1497r2-human`) run `delete process.env.MULTI_TENANCY_ENABLED`. So the "human cell passes in each mode" claim, in the builder's mail and in round 2's verdict, was single-tenant twice. My E1 covers the real-route human path in BOTH modes, and it is green.

**N4.** originate is outside the typecheck ratchet: it has no `tsconfig.test.json`, while the ratchet works for api-gateway. And the new unit file does not compile against the old service, so the red-first evidence is the integration layer only, which I reproduced as 6/16.

**N5. Deploy ordering. Merging does not deploy. But after merge, the deploy hold is a process rule, not anything in code.**
- Nothing in this PR deploys itself: no workflow, compose, migration or infra files. `deploy-demo.yml` and `build-images.yml` are `workflow_dispatch`-only and guarded, and the live demo is a manual rsync.
- But the code has no flag. Once merged, the next deploy of develop by anyone turns part (i)'s 501 into a live, irreversible erasure that Platform S's client already calls.
- Before KS-695 deploys:
  - KS-1508 must have landed (Wednesday's m-1);
  - Platform S must have answered the revoked-key retry question;
  - m-A and m-B must be fixed.
- **Recommend a board-level deploy hold on develop, or merging only once KS-1508 is in.** That ruling is Wednesday's.

**N6.** G2 is an equivalent mutant: the revoke's `organization_id` predicate is redundant once the row is locked and checked in JS. Only unit text pins see it. It is fine as defence in depth.

**N7.** PR body figures, sampled:

| Figure | Status |
|---|---|
| bounds 16/16, old 15/15 | reproduced |
| unit 28/28 | reproduced |
| originate 101/1187 (head) | reproduced |
| shared 49/954 | reproduced |
| gate files 24 passed in each mode | reproduced, but see N3 |
| R5 at 25.1 / 25.0 s | reproduced: 25,120 / 25,033 ms |
| red-first 6 of 16 | reproduced |
| 149,041 documents blanked in 7.3 s / 7.2 s | count reproduced exactly; time on my laptop 6.3 s (F) / 8.1 s (T) |
| "about 3.4x headroom" | arithmetic on the builder's own numbers; mine give 3.1x in the slower mode. Either way it is a laptop figure, not production |
| hook output, `mergeable=True` | recorded only |

## Not measured

- The live PR body on GitHub. `gh` in the Blockchain `.gh-config` is not authenticated (rc 4, "gh auth login"), so I read the builder's local copy.
- Any live, Kintsugi, demo or production stack, the real gateway (including its 60 s key cache), and Azure Postgres or pgbouncer timing.
- Pool-wait saturation in mode F (Prisma `maxWait`): argued from code, not run.
- A real NTP or clock step. B4 mocks `Date.now`.
- Schemathesis, Akto, Playwright, k6, and the pre-push preflight on the merged tree, including the shell leg that develop's `scripts/` delta requires.
- api-gateway and the four platform suites (unchanged by this PR).
- `/sign-cert` against a real auth-service signer (stubbed), and `/sign-wallet` with a real CIP-8 signature (`verifyMessageSignature` mocked).
