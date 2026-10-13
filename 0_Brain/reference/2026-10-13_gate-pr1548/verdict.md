VERDICT: GO WITH NOTE (0 Major, 1 Minor, 6 Info). Head gated 9d974c4b516cc665a6c5d3b26b06eae22c09a9b3. Develop measured d53d80cbb2d50a5525c3d881a2da7a31eba67fb5.
REPORT_SHA256_16: 20fb01665917ef45
# Gate verdict: PR #1548 (KS-1598), the PR 1539 r2 follow-up set. Opus, through-code weight

Recipe for line 2: delete line 2, take the sha256 of the remaining bytes, keep the first 16 hex characters.

**Head under test:** `9d974c4b516cc665a6c5d3b26b06eae22c09a9b3`.
- My own `ls-remote` read the same SHA for `refs/pull/1548/head` at the start and again at the end (21:49 AEDT). See `results/lsremote_start.txt` and `lsremote_final.txt`.
- The commit's tree is `4627f0429b05491eb3acdf164297c5e329ba41bd`, which matches the author's claim. Its parent is `026c2d16`.
- Live develop is `d53d80cbb2d50a5525c3d881a2da7a31eba67fb5`, the same at start and end. It is ONE commit past the base: "KS-1032: an unconfigured box refuses forged trust headers…", 10 files, all in `services/originate`, the env templates and the docs.
  - Its subject is consistent with PR #1546 (KS-1032).
  - The commit message carries no PR number, so I cannot confirm the squash beyond the subject.

**Merge only on Wednesday's head-bound GO. Nothing deploys from this verdict.**

Gate: an independent Opus seat, 2026-10-13 AEDT. Findings only; I changed nothing in the project.
- **Code:** `git clone --shared` into my scratchpad (`g1548/repo`), with the push URL set to `DISABLED`. The project's `core.sshCommand` was used only for `ls-remote` and fetch.
  - Write verbs ran in that clone only: worktree, `hash-object`, `commit-tree` for one conflict-control commit, and `merge-tree`.
  - Nothing was written in `!CODING`. No GitHub or Linear reads or writes succeeded: `gh` had no credential, and I made no other attempt.
- **Database:** my own PostgreSQL 15.14 on 127.0.0.1:**55477**, TCP only, unix socket disabled, `en_US.UTF-8`.
  - `lsof` showed 55416, 55418, 55471 and 55521 in use when I started (other seats). I never touched them.
  - My server is **stopped**: `lsof` shows 0 listeners on 55477 and `pgrep vitest` finds 0 processes.
- **Schema:** built from the head's `docker/init/*` in order, then `scripts/run-migrations.sh`: rc 0, `applied=51 failed=0`, with an explicit `Applying 049_admin_organisation_scopes.sql` (`results/pgsetup_head.txt`).
- **Roles:** the service ran as `secuura_app` (rolsuper f, rolbypassrls f). FORCE RLS is on `users`, `organizations`, `audit_logs` and `admin_organisation_scopes` (`results/catalogue.txt`).
- **Where things are:** raw outputs in `evidence/results/`, my cells in `evidence/cells/`, tools in `evidence/tools/`, init and migration logs in `evidence/pg/`.

## Findings

| id | severity | where (head 9d974c4b) | what | minimal fix |
|---|---|---|---|---|
| **m1** | **Minor** (new in this delta) | `services/security/src/index.ts:1637` | **The fold is wider than ASCII case.** `lower(status) = 'active'` uses the database's libc collation, which folds U+0130 (capital I with dot above) to `i`. So stored values `ACTİVE` and `actİve` pass the CHECK (`lower(status) IN (…)`) and pass this guard. Auth's `mapDbStatus` folds with JS `toLowerCase()`, which gives `acti̇ve` (i plus U+0307), not in the vocabulary, so auth treats the user as **DEACTIVATED**: the user cannot log in.<br>**Measured at the real route** (cell H):<br>• head: `ACTİVE` → **200, scope row written**; `actİve` → **200, row written**;<br>• base 026c2d16 (control): **404** for both;<br>• controls `ACTIVE` → 200 on head and 404 on base; `DELETED` → 404 on both.<br>So this delta **widens liveness** for one spelling. That is what the PR's control cell and the comment at `:1634` say cannot happen. | `lower(status COLLATE "C") = 'active'`. Measured as my mutant X5:<br>• it **survives all 71 asserting cells**, so it is neutral for ASCII;<br>• it turns cell H's U+0130 rows to **404** while `ACTIVE` stays 200 (`results/H_ledger_X5fix.json`).<br>Add one U+0130 → 404 cell. |
| i1 | Info | `index.ts:1630-1631`, the test at `ks1570b-admin-scope-route…:254-255`, the commit message, PR body | **The comment misquotes migration 046.** It says 046 "constrains it with `lower(status) NOT IN (...)` (:34, :41)". Lines 34 and 41 are the NORMALISATION `UPDATE`'s `NOT IN`. The constraint is `CHECK (lower(status) IN (...))` at `046:60` (catalogue: `users_status_vocabulary`). The conclusion (case is folded) is right. | Cite `:60` and `IN`. |
| i2 | Info (pre-existing test gap, made visible) | The m1 CONTROL cell at `ks1570b-admin-scope-route…:282`, and the m2 cell at `:231` | **The liveness control pins one non-live status.** My mutant X4, `lower(status) <> 'deleted'`, makes `pending`, `suspended`, `deactivated`, `invited` and `inactive` grantable. It **survives all 18 author route cells and the 3 concurrency cells**, and only my G spectrum kills it (15 red). The same gap existed on base (its m2 cell also tests only `deleted`). | Parametrise the control over the vocabulary in 2–3 spellings. My `cells/gate1548-g-status.integration.test.ts` has that shape (22 cells). |
| i3 | Info | PR body "Mutants" table; commit message ("R4 (the lock keyed on raw ids) is KILLED, but ONLY by E2…") | **The author's "R4" is mislabelled.** In the author's tool (`5_Project_History/2026-10-13_seatV-8th/tools/mutants_job2.py`), R4 is `hashtext($1), hashtext($2)` with the PARSED `[tenantId, userId]`: bd11c34e reverted, not raw ids. That is my X3, and I reproduce its result: killed only by E2's source-text pin, with E3 green. The real raw-ids mutant (`lower()` kept, raw `req.body.tenantId` and `req.params.userId`; my R4) **survives every cell**, equivalent by construction, exactly as the new code comment says. The r2 gate's R4 semantics (raw ids AND no `lower()`; my X2) is **killed behaviourally by E3** and by my R1 and R2. The conclusions stand; the label does not. | Relabel the author's R4 as "bd11c34e reverted". |
| i4 | Info | PR body "The sweep" table | **The sweep table is not the route's site list, though its conclusion holds.**<br>• Its last two rows (`k.keyHash === keyHash`, `apiKey.isActive === false`) are in `POST /api/keys/validate`, not in this route.<br>• It omits three sites that are in the route: the caller-role gate (`isPlatformRole`, which folds with `toUpperCase`); the `wanted` Set de-duplication (on lower-cased ids); and the **RLS `tenant_isolation` policy**. That policy compares `tenant_id::text = current_setting('app.current_tenant_id')` as **case-sensitive text**. It folds only because UUID_TEXT lower-cases `tenantId` before `runWithTenantId`. My cells R1 and R2 send an UPPER-case `tenantId` and get 200 with the rows written, so this site was measured end to end.<br>No site is unfolded where the data can differ in case (item 3). | Correct the table. |
| i5 | Info | `ks1570b-concurrent-replace…:66-69` and `:175-185` (E3) | **E3's instrument is cluster-wide, and E3 assumes X reaches the lock first.** It counts every `NOT granted` advisory lock in the cluster, not the (tenant, user) key. It also assumes X gets there within the 300 ms head start. Neither weakens it today: green 3/3 on head, and my key-bound instrument (filtered to `classid`/`objid` = `hashtext(lower(T))`/`hashtext(lower(U))`) read the same 1 waiter. But a parallelised suite could feed it a foreign waiter. | Optional: filter on the key, as in `cells/gate1548-r-race…`. |
| i6 | Info (pre-existing, not in this delta) | `index.ts:1637` `upper(role) = $3` | **The same libc-fold class applies to the role check.** In SQL, `upper('admın')` (U+0131 dotless ı) = `'ADMIN'` is **t** in this collation, and **f** under `COLLATE "C"` (`results/role_fold_and_rls.txt`). The role column has no CHECK. Not measured at the route and not introduced here. Recorded so the m1 fix is applied to both folds or neither. | Same `COLLATE "C"` treatment, on its own ticket if wanted. |

**Severity reasoning for m1.**
- **Why Minor:** it is new in this delta, and it fails toward a grant. It is the same class as round 1's m2 (a non-live target gets a scope row, which revives silently if the account is later reactivated). It also falsifies the invariant this PR's control cell was written to pin.
- **Why not Major:**
  - **No application writer can store such a value.** Code read: the admin PATCH checks status against an exact allow-list (`ADMIN_WRITABLE_STATUSES`). Every other writer I found writes a literal (`'active'`, `'ACTIVE'`, `'suspended'`, `'INVITED'`), so it takes a direct database write.
  - The target cannot log in.
  - Only a platform role can call the route: `requireAdminScopeWriter` → `platformRoleGate` → `isPlatformRole` (SYSTEM_ADMIN or SUPER_ADMIN). The author's 403 cells for ADMIN, ISSUER_ADMIN and connector are green on the head.
- **Not measured:** the production collation. I measured macOS libc `en_US.UTF-8`. glibc `en_US.utf8` is expected to fold U+0130 the same way.

## FOUND / TESTED / HOW

**1. Scope** (`scope.txt`, `delta.diff`, read whole)
- `git diff --stat 026c2d16 9d974c4b`: **4 files, +176/−7**, exactly the four named.
- Hunks by file:

| file | hunk | class |
|---|---|---|
| `index.ts` | `@@1395` and `@@1565` | n1, `;;` → `;`. Code, no behaviour change. |
| `index.ts` | `@@1624` | Comment (+8) and the guard SQL `status = 'active'` → `lower(status) = 'active'`. **Behaviour.** |
| `index.ts` | `@@1685` | Comment (+14) and the lock SQL `hashtext($1)` → `hashtext(lower($1))` for both keys. Code; behaviour-neutral as measured (item 5). |
| `ks1570b-admin-scope-route…` | `@@246`, +49 | Test: the ACTIVE, Active and DELETED cells. |
| `ks1570b-concurrent-replace…` | `import path` | Test. |
| `ks1570b-concurrent-replace…` | `put()` `{upper}` option, `chain()`, `waiters()` helpers, n4 message | Test. |
| `ks1570b-concurrent-replace…` | E1 chain assertions | Test. |
| `ks1570b-concurrent-replace…` | E2, E3 | Test. |
| `ks888-failed-mint-save…` | +11, two fixture rows (6 cells) | Test. |

- n1: `;;`-ending lines in `index.ts` are **0 on head and 2 on base** (the control) (`n1_semicolons.txt`).
- n4: `gate1539 E needs` is 0 on head and 1 in `git show 026c2d16:…`, the control.
- The env-unset run gives rc 1 with **3 skipped, not passed**, and the renamed message is printed (`author_head_noenv.txt`).

**2. m1 (the guard)**
- **The author's cells, head:**
  - the 2 author files: **21/21, three runs out of three** (`author_head_{1,2,3}.txt`);
  - **base with the head's test files copied in: 3 red / 18 green, three runs out of three** (`author_base_{1,2,3}.txt`). Each red is for the right reason:
    - ACTIVE and Active: `expected 404 to be 200`;
    - E2: the source-text regex does not match.
  - E1's new chain assertion and E3 are green on base too. They are regression pins, not red-first proofs, which is correct, because base already had the lock.
  - The DELETED control is green on both.
- **My spectrum, cell G** (22 cells, real route, app role):
  - `active`, `ACTIVE`, `Active` and `aCtIvE` → 200, with 1 row and 1 audit row each;
  - each of `pending`, `suspended`, `deactivated`, `invited`, `inactive` and `deleted`, in lower, UPPER and Title case → **404 `NOT_FOUND`, 0 rows, 0 audit rows**;
  - head: **22/22, three runs out of three**; base: **3 red** (the three non-lower live spellings), with all 18 dead cells green (`GR_head_{1,2,3}.txt`, `GR_base_1.txt`).
- **The negative controls the brief asked for** (`status_probe_sql.txt`, 19 strings, with what the CHECK admits beside the guard):
  - **Whitespace:** leading space, trailing space, tab and newline are **rejected by the CHECK**, and the guard is false on all four.
  - **NULL:** the column is NOT NULL (catalogue), and `lower(NULL)` is NULL, so it fails closed.
  - **Mixed-case spellings of other statuses** are admitted by the CHECK, and the guard is false on all of them.
  - Combining-dot `i`+U+0307, full-width letters and the empty string are rejected by the CHECK.
  - **U+0130 is the one exception:** the CHECK admits it, and the guard is **true** under the database's default collation and **false** under `"C"` and under ICU `und-x-icu`. This is finding m1, measured at the route by cell H (`H_ledger_head.json` vs `H_ledger_base.json`).

**3. The sweep: every comparison in `PUT /api/keys/admin-scopes/:userId` (`index.ts:1597-1753`, read whole) and the GET (`1755-1771`)**
- **The caller's role:** `isPlatformRole`, `String(role).toUpperCase()` (`packages/shared/src/security/keyRevokePolicy.ts:140`). Folds.
- **The id inputs:** UUID_TEXT on `userId`, `tenantId` and every `organizationIds` entry (`:1601-1607`). They are lower-cased at parse.
- **`wanted`:** a Set over the lower-cased ids, so case variants collapse. The author's "duplicates and case variants" cell is green.
- **The target query (`:1637`):**
  - `id` and `tenant_id` are compared as `::uuid`, which folds by type;
  - `upper(role)` folds (i6 is pre-existing);
  - `lower(status)` folds after this delta (m1 is the U+0130 edge).
- **The organisation check:** `tenant_id = $1::uuid` and `id = ANY($2::uuid[])` are typed. The `known` Set compares `id::text` with the lower-cased `wanted`: PostgreSQL prints a uuid in lower case, and the "duplicates and case variants" cell exercises this path.
- **The advisory lock:** lower-cased twice over (item 5).
- **The previous-set SELECT, the DELETE and the INSERT:** all `::uuid`.
- **RLS `tenant_isolation`:** a case-sensitive text comparison, folded because the GUC carries the lower-cased `tenantId`. Measured with UPPER-case `tenantId` in my R1 and R2 (200, rows correct).
- **`callerUuid` (`/…/i`) and `grantedBy`:** not comparisons that gate anything. The caller id is stored as sent, an audit spelling only.
- **The GET:** typed uuid comparisons only.
- **Answer:** given UUID_TEXT, no comparison in the route fails to fold ASCII case where the data can differ in case. The two Unicode-fold edges are m1 and i6.

**4. m2 / E3, and mutants** (`tools/mutants_1548.py`; `results/mutants_1548_run.txt`, `mutants_1548.json`, `mutants_1548_run_x5.txt`)

Method:
- The baseline was green first: author route 18, author E 3, KS-888 unit 25, gate G 22, gate R 3.
- Each mutant was applied alone, and each anchor had to occur exactly once.
- `index.ts` was restored from a byte snapshot, and its sha256 `95d06080d86f3245…` was asserted identical after every mutant.
- **Every red cell is recorded with its failure message. A kill whose red cells all carry an empty message is not counted.**

Results:

| mutant | result | killed by (red cells) |
|---|---|---|
| **C0** comment-only control | **SURVIVED** | 0 red |
| **m1r** fold reverted | **KILLED** | author ACTIVE and Active; G ×3 (`expected 404 to be 200`) |
| **R2** lock after the previous-set SELECT | **KILLED** | **E1 and E3** (chain message), my R1 and R2 |
| **R3** lock after the DELETE | **KILLED** | **E1** (`final … to deeply equal`), **E3** (`a waiter was seen … expected 0 to be ≥ 1`), my R1 and R2 |
| **R10** class 57 dropped | **KILLED** | 2 KS-888 57P01 cells (`status 500` vs `503`) |
| **R11** class 53 dropped | **KILLED** | 2 KS-888 53300 cells |
| **R4** raw request ids, `lower()` kept (the real raw-ids mutant) | **SURVIVED** | equivalent by construction (i3) |
| **X1** (mine) lock removed | **KILLED** | E1, E2, E3, my R1 and R2 |
| **X2** (mine) raw ids AND no `lower()`, the r2 gate's R4 | **KILLED behaviourally** | **E3** (`waiter … expected 0`), E2, my R1 and R2 |
| **X3** (mine; = the author's "R4") bd11c34e reverted, parsed ids | **KILLED only by E2's source-text pin** | none of E1, E3, R0, R1, R2 or G goes red, so it is behaviour-neutral (item 5) |
| **X4** (mine) guard `lower(status) <> 'deleted'` | **KILLED only by my G** | 15 red; all 21 author cells green (i2) |
| **X5** (mine) the proposed fix `COLLATE "C"` | **SURVIVED** | 0 red. The first X5 attempt reported **EMPTY-MSG**: 71 "red" cells, every one with an empty message, because my anchor broke the TS string quoting and the module failed to load. That run is **rejected and not counted**; it is the empty-message rule doing its job. The corrected re-run: 0 red. |

**Does E3 prove serialisation?**
- E3 **does observe a waiter.** On the head, my key-bound instrument read 1 waiter on the exact (T, U) key in R1 and R2, 3 runs out of 3.
- **The instrument's control:** R0, sequential writers with the same poller, read **0**, 3 runs out of 3 (`R_ledger_head_{1,2,3}.json`).
- E3 goes **red under R2** (chain) and **red under R3** (no advisory waiter, because Y blocks on the row lock instead). Both kills carry a message.

**5. bd11c34e**
- The carried SQL is **byte-identical** to the patch's line (`5_Project_History/2026-10-13_seatV-8th/evidence/bd11c34e-defence-in-depth.patch`). Only the comment differs. The commit object is not in the repository: `cat-file` fails, as expected for an unpushed commit.
- **Behaviour-neutral given UUID_TEXT:**
  - In SQL, over 200,000 random lower-case uuid strings: `lower(t) <> t` **0**, and `hashtext(lower(t)) <> hashtext(t)` **0**. **Control:** the same check on `upper(t)` differs **200,000/200,000** (`results/lock_key_identity.txt`). So the lock key values are unchanged, and so is the namespace shared with KS-1549's rotate lock at `:387`.
  - Behaviourally, the revert (X3) leaves every concurrency cell green, mixed-case ones included.
- **The rewritten comment (`:1696-1709`) is now true, claim by claim:**
  - hashtext is case-sensitive: E2's control is green.
  - UUID_TEXT lower-cases both ids: code at `:1601-1604` and `:1615-1617`.
  - The r2 gate's F1 and R4 record: matches its verdict.
  - With `lower()` in the key, the raw-ids R4 is equivalent: **my R4 survived every cell.**
- The PR body's mutant table mislabels which mutant is "R4" (i3).

**6. Merge prediction against LIVE develop `d53d80cb`** (`results/mergetree.txt`, `mt_clean.txt`, `mt_control.txt`)
- **Ancestry:**
  - merge-base(head, develop) = `026c2d16`;
  - `026c2d16` is an ancestor of develop: rc 0;
  - develop is an ancestor of the head: rc 1, so a merge is needed.
- **Overlap scan:**
  - PR files 4, develop-moved files 10, **overlap 0**;
  - **planted control:** one PR path added to the develop list gives overlap **1**;
  - develop's move touches `services/security/` or `packages/` **0** times (positive control: `services/originate/` matches 7).
- **`merge-tree --write-tree` head × develop: rc 0**, tree `d00499fd…`.
  - In that tree, `security/src/index.ts` equals the head's and `originate/src/index.ts` equals develop's.
  - `diff --stat develop..merged` is exactly the PR's 4 files, +176/−7.
- **Negative control:** a scratch commit on develop (`194de33b`, the guard line rewritten) gives **rc 1** with `CONFLICT (content) … index.ts`. **The clean reading discriminates.**

**Author's other numbers, re-measured on the head:**
- security **unit 31 files / 343**, rc 0 (`sec_unit_head.txt`);
- security **integration 7 files / 95**, rc 0 (`sec_integ_head.txt`);
- KS-888: **25/25 on head and 25/25 on base with the head's file**, so the 6 new cells are green on arrival, as claimed (coverage, not red-first);
- `tsc --noEmit` **rc 0, 0 `error TS`**; **control:** a planted file gives rc 2 with 1 `error TS`;
- eslint `--max-warnings=0` on the 4 changed files: **rc 0**; **control:** the planted file gives rc 1 (`no-var`).

The planted file was moved out to `g1548/quarantine/` (not deleted), and the head worktree is clean apart from my untracked gate cells.

## NOT tested (plainly)
- **The live PR body on GitHub.** `gh` had no credential. I read the author's logged copy `5_Project_History/2026-10-13_seatV-8th/logs/pr_ks1598_body.md` (9,442 bytes) and cannot vouch that it is byte-equal to GitHub's.
- Linear and the KS-1598 per-site record.
- **The production collation's fold of U+0130.** I measured macOS libc only; glibc is inferred.
- The full set of `users.status` writers across ops scripts and other repos. I code-read the services' `INSERT` and `UPDATE` sites only.
- **Multi-tenancy mode.** I ran with `MULTI_TENANCY_ENABLED=false`; the author's mutants ran with `true`.
- **Suites:** the shared unit suite and the platform suites (Schemathesis, Akto, Playwright, k6). Preflight legs 3, 4 and 8. The gateway path.
- **The merged tree's suites.** I ran no suite on the merged tree: develop's move touches no security or shared file, and the merged security files are byte-equal to the head's.
- The KS-1549 rotate lock: out of scope, by the author's ruling.

**Could any of this hide a Major?**
- **The route:** only a platform role can call it, the grant set is validated against the tenant's organisations, and the lock and audit chain are measured correct.
- **The one widening (m1):** it needs a non-application write and targets a user who cannot log in.
- **The untested surfaces** (gateway, platform suites, the GitHub body) cannot widen who may call this route.
- **I see no untested surface that could hide a grant wider than requested, or an audit row that misstates the stored state.**

## Scratch state when stopped
- **PostgreSQL:** stopped (`pg_ctl -m fast`), with nothing listening on 55477.
- **Worktrees** `g1548/wt_head` and `g1548/wt_base`: they hold my untracked gate cells, and `wt_base` also holds the head's three test files copied in. Scratchpad only.
- **The scratch clone** holds refs `refs/gate/head` and `refs/gate/develop` and the conflict-control commit `194de33b`. Its push URL is `DISABLED`.
