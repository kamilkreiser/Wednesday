# Gate verdict: PR #1539 ROUND 2 OF 2 (KS-1570 PR B), Opus DELTA gate on the M1 fix and the same-delta Minors
Report sha256/16: c283b8ff9ca68c4c (recipe: delete this one line from the file, then sha256 of the remaining bytes, first 16 hex chars)

**Head under test:** `fdf314e0e8ebb0526cd7a9675d8beb32291d2e2d`. My own `ls-remote` gives the same SHA for `refs/pull/1539/head`. It also gives develop `a7cffc8d9831e67d91f6dd24d0047ffe3e26c97e` (unmoved) and PR #1541 `7d9cad92afa7e9d1be2e2a03515afd5754538d0d` (`results/lsremote.txt`).

**VERDICT: GO WITH NOTE.** Findings: **0 Major, 2 Minor, 6 Nit.**

- **M1 is closed.** On 61c30de5 I reproduced the race 3/3 with the author's cell, and 3/3 more with round 1's cell E verbatim. The head is green on every concurrency cell I ran:
  - cell E: 9 runs at pool sizes 1, 2 and 10;
  - my own case-spelling, platform-token, collision and deadlock cells;
  - a 20-writer audit-chain test, 3 rounds × 3 runs.

  The lock:
  - is released on COMMIT, on ROLLBACK, on a 503 and on a killed backend;
  - is keyed on the already lower-cased ids;
  - is taken before the previous-set SELECT and before the DELETE;
  - does not serialise different users.

  No deadlock appeared in any head run.
- **m1, m2, n1 and n3 are fixed as described.** The extracted classifier is the old predicate byte for byte, and behaves identically over 101,615 inputs. Mint and revoke error cells give the same results before and after.
- **No regression.** Round 1's whole cell set re-runs green on the head: A 64/64 ×3, B 8/8 at pools 1, 2 and 10, plus C, D and E. The only status changes are the intended ones:
  - B6's killed backend now answers 503 instead of 500 (B asserts ≥500);
  - A's deleted-status observe cell now records 404.
- **The two Minors are both new in this delta. Neither can widen a grant.**
  - The status filter is case-sensitive, so it refuses a live ADMIN whose status is stored as `ACTIVE`, a spelling the repo explicitly allows.
  - The author's own regression cells do not pin the audit half of M1. A mutant that takes the lock after the `before` SELECT survives all 16 author cells, and only my cells kill it.

**This PR ships only in the one round with PR A, KS-1564 and KS-1584. I do not recommend deploying anything.** Merge only on Wednesday's head-bound GO.

Gate: an independent Opus seat, 2026-10-13 AEDT. Read-only on the project:
- Code: `git clone --shared` into my scratchpad (`g2/repo`), push URL `DISABLED`. The project's `core.sshCommand` was used for fetches only. Write verbs (fetch, worktree, one control commit) ran in that clone only.
- Nothing was written inside `!CODING`. No GitHub or Linear writes, no remote environment.
- Database: my own PostgreSQL 15.14 on 127.0.0.1:**55421**, TCP only, with no unix socket.
  - Ports 55413, 55414, 55416, 55418 and 55436 were listening when I started (other seats). I never touched any of them.
  - My server is **stopped**: `lsof` shows nothing listening on 55421, and no vitest or mutant processes remain.

Raw outputs are in `evidence/results/`, my cells in `evidence/cells/`, the tools in `evidence/tools/`, and the migration log and the server log's deadlock excerpts in `evidence/pg/`.

## Findings

| id | severity | where (head fdf314e0) | what | minimal fix |
|---|---|---|---|---|
| **m1** | **Minor** (new in this delta) | `services/security/src/index.ts:1571` (`… AND status = 'active' LIMIT 1`) | **The status filter is case-sensitive, but the repo stores and accepts status case-insensitively.** See "m1 details" below the table. | `AND lower(status) = 'active'`. Mutant R9 is exactly this change: it survives every cell I have, and all 16 author cells stay green. Add one cell: status `'ACTIVE'` → 200. |
| **m2** | **Minor** (new in this delta, test gap) | `src/__tests__/ks1570b-concurrent-replace-is-not-a-union.integration.test.ts:100-102`, and the 15 cells of `ks1570b-admin-scope-route` | **The author's regression cells pin only half of M1.** See "m2 details" below the table. | Add one assertion to the adopted cell: `aud.map(a => [a.before, a.after])` equals `[[[],[A1]],[[A1],[A2]],[[A2],[A3]]]`. My F1 shows the shape. Optionally add one upper-case-vs-lower-case concurrent cell, as in my F1. |
| n1 | Nit | `index.ts:1340`, `index.ts:1510` | `const infra = isInfrastructureDbError(saveErr);;` has a doubled semicolon at both refactored sites. It is harmless. eslint stays rc 0 because `no-extra-semi` is not active: a planted `;;` in my control file was not flagged either. | Delete the extra `;`. |
| n2 | Nit (pre-existing coverage, made visible) | `index.ts:1136` and `ks888-failed-mint-save-issues-no-key.test.ts` | **No cell anywhere pins SQLSTATE classes 53 or 57.** Mutants R10 (57 dropped) and R11 (53 dropped) survive every suite, including KS-888's unit cells, whose INFRA list is 08006, ECONNREFUSED and a code-less pool timeout. This is not a regression: develop had the same gap twice. Class 57 includes `57014 query_canceled` (statement_timeout), which now answers 503 at all three sites. That is retryable, and consistent with the old predicate. | Add a 53300 case and a 57P01 case to KS-888's INFRA table. |
| n3 | Nit | `index.ts:1570-1573` vs the transaction at 1615 | **The status is read once, before the lock and outside the transaction.** My cell F10 holds a PUT inside its transaction and marks the target `deleted` meanwhile: the held PUT still commits **200 with its row written**. The next PUT answers 404. The window is one transaction long, and only a platform operator can act inside it. Purging rows on deletion is KS-1592's question either way. | Accept, or repeat the status check inside the transaction after the lock (`SELECT … FOR SHARE` on the user row). |
| n4 | Nit | the adopted cell, line 56 | Its config-refusal message still says `gate1539 E needs …`. It does refuse correctly: rc 1, 16 skipped, both files naming the variables (`results/author_head_noenv.txt`). | Rename the message. |
| n5 | Nit | PR body (author's logged copy, see item 8) | "**This is true for CONCURRENT calls only since the gate's M1 delta**" reads as "only for concurrent calls". "The change" still says "13 cells" (the file now has 15) and "details `{tenantId, before, after}`" (the code also writes `targetUserId` and `grantedBy`, a superset). | Rephrase as "true for concurrent calls too, since the M1 delta"; update the count. |
| n6 | Nit (equivalent mutant, recorded) | `index.ts:1630` | Mutant R5 (lock keyed on the user id only) **survives every cell, and is behaviourally equivalent for correctness.** It would only also serialise the same user id across two tenants. | None needed. Recorded so nobody reads the survivor as a hole. |

**m1 details.**
- The `users_status_vocabulary` CHECK is `lower(status) IN ('active','pending','suspended','deactivated','invited','inactive','deleted')` (`results/catalogue.txt`). Migration `046_users_status_vocabulary.sql` says in so many words: "Case is folded rather than forbidden: mapDbStatus already accepts either case, and rejecting 'ACTIVE' here would break a write the application considers legal."
- At least one live writer stores the upper-case spelling raw: the demo-seed id-collision path, `services/auth/src/repositories/userRepo.ts:1716` (`status = 'ACTIVE'`). Auth's `mapDbStatus` folds case, so that user logs in as ACTIVE.
- **Measured at the real route** (cell F9 and F9b, 3 runs out of 3):
  - status `ACTIVE` gives **404**, and `Active` gives **404**, with nothing written. On 61c30de5 both gave 200.
  - `active` gives 200. `pending`, `suspended`, `deactivated`, `invited`, `inactive` and `deleted` give 404, 0 rows, 0 audit rows.
- **Severity: Minor.** It fails closed (a refusal, never a grant), and an unscoped ADMIN loses nothing that PR A did not already default-deny. But a live, log-in-capable ADMIN cannot be given a scope.
- The author's "checked against the schema" covered NOT NULL and DEFAULT, and missed the CHECK's `lower()`.

**m2 details.** The adopted cell's title says "and its audit row tells the truth", but it asserts only the statuses and `final == last writer's response`.
- **Measured with the mutant runner:**
  - **R2 (lock moved AFTER the previous-set SELECT)** survives all 15 route cells and the adopted cell, and round 1's cells A, B and E. That mutant restores the exact audit lie M1 named (`before [A1]` after X committed `[A2]`) while the final set stays right.
  - **R4 (lock keyed on the RAW un-lower-cased request ids)** also survives every author cell.
- **Only my cells kill them:** F1 ×2, F5 and F7, which assert the audit chain and use upper/lower spellings.
- The code at the head is correct (see item 3). The gap is that a later refactor could reopen half of the Major with the author's suite green.

## What I measured (instrument and control for every number)

**8. Scope, ancestry, merge** (`results/scope.txt`, `results/delta.diff`, `results/mergetree.txt`).
- **Ancestry:**
  - `merge-base --is-ancestor 61c30de5 fdf314e0`: rc 0. The reverse is rc 1, which is the control.
  - develop is an ancestor of the head: rc 0.
- **Commits:** `61c30de5..fdf314e0` is ONE commit, `fdf314e0` (parent `61c30de5`), "KS-1570 (PR B): serialise concurrent scope replaces, and the 1539 gate's four minors".
- **`git diff --stat 61c30de5..fdf314e0`: 5 files, +215/−13.** I read the diff whole:
  - `docs/openapi/secuura-api.yaml` (+3/−6): the GET 200 description is extended and the GET 404 removed;
  - `ks1570b-admin-scope-route.integration.test.ts` (+41): 2 cells, m2 and m1;
  - `ks1570b-concurrent-replace-is-not-a-union.integration.test.ts` (+104, new). Its code is **byte-identical** to round 1's cell E, and only the header comment differs (`results/cellE_vs_adopted.diff`: 27 diff lines, all in the `/** */` block);
  - `services/security/src/index.ts` (+66/−3):
    - the new `isInfrastructureDbError` at 1118-1138;
    - the mint site 1340 and the revoke site 1510 (one line each);
    - the n1 comment at 1536;
    - the m2 filter at 1565-1572;
    - the lock at 1617-1630;
    - the 503 branch at 1654-1670;
  - `security.openapi.ts` (+5/−3): n3.
- **Nothing outside the author's list changed.** The only code outside PR B's routes is the two one-line classifier calls (judged in item 4).
- **Against develop:** 5 files, +888/−2 (the two −2 are the mint and revoke lines).
- **Merge-tree** (my own clone):
  - head vs develop: rc 0, tree `89b24b1c…`, which equals the head's own tree;
  - head vs PR #1541 `7d9cad92`: rc 0, tree `87e61f61…`;
  - **control:** a develop-based commit editing the mint classifier line gives rc 1, with `CONFLICT (content)` in `index.ts`. **Both clean readings discriminate.**
- **Linear:** not read and not written.

**1. Regression, 3 runs each.** Real PG15 built from `docker/init/*` in order, then `scripts/run-migrations.sh`: rc 0, an explicit `[main] Applying 049_admin_organisation_scopes.sql...`, `applied=51 failed=0` (`results/pgsetup_head.txt`). The service ran as `secuura_app`: rolsuper f, rolbypassrls f, and FORCE RLS on `admin_organisation_scopes`, `audit_logs`, `users` and `organizations` (`results/catalogue.txt`).
- **The author's 13 original + 2 new + the adopted cell:**
  - **Head: 16/16**, three runs out of three (`author_head_{1,2,3}.txt`).
  - **61c30de5 with the head's two test files copied in: 13 green / 3 red**, three runs out of three (`author_old_{1,2,3}.txt`). Each red is for the right reason:
    - m2: `expected 200 to be 404`;
    - m1: `expected 500 to be 503`;
    - E: `expected [ …(2) ] to deeply equal [ Array(1) ]`.
  - **Config refusal:** env unset gives rc 1, with 16 skipped, not passed (`author_head_noenv.txt`).
- **Round 1's cells on the head:**
  - **A: 64/64**, three runs out of three (`r1A_head_{1,2,3}.txt`). Its observe-only deleted-status cell now records `{status: 404, rows: []}` (it was 200).
  - **B: 8/8 at pools 10, 1 and 2** (`r1B_head_pool*.txt`, ledgers alongside):
    - B1–B5b: still 500 `INTERNAL_ERROR`. These are application faults (permission, a missing table, a CHECK, a deferred trigger, REVOKE), correctly not classified as infrastructure.
    - **B6 (pg_terminate_backend): now 503** `SERVICE_UNAVAILABLE`.
    - Every fault: rows unchanged, audit delta 0, follow-ups 200.
    - B7: GUC `''` six times out of six; pool 1 answers T2 at 1510 ms, pools 2 and 10 at 216 ms and 214 ms. **The pool patch was live.**
  - **C** (develop's mint, killed backend): 503, the same as round 1's develop control.
  - **D**: 1/1.
  - **E verbatim**:
    - head: green 3/3 at pool 10, 3/3 at pool 1 and 3/3 at pool 2 (run with the adopted copy each time);
    - **61c30de5: red 3/3**, final `{f2,f3}`, audits `[]→[f1]`, `[f1]→[f2]`, `[f1]→[f3]` (`results/E_summary.txt`).
  - **Anything green before and red now: none.** The pool size came from a scratch-only `GATE_POOL_MAX` patch to `db.ts`. It was restored, and the sha256 is identical before and after (`2a2908bf…`, `db_ts_sha_{before,after}.txt`).
  - Harness note: B, C and F exit rc 1 with all tests passed. That is vitest reporting the uncaught `Connection terminated unexpectedly` from the deliberate kill: round 1's m3, now on KS-1587. The class is pre-existing (develop's mint path raises it too, cell C).
- **The rest of the security integration suite** (excluding gate files): **6 files / 76**, rc 0 (`sec_integ_head.txt`). This includes PR A's `ks1570-admin-organisation-scope` (16), and ks1549, ks1553 and ks1556.

**2. M1 and the lock** (`cells/gate1539r2-f-delta.integration.test.ts`; ledgers `results/F_ledger_head_{1,2,3}.json`, `F_ledger_old_1.json`).

How the cells work:
- A request is held inside its transaction by a SECURITY DEFINER BEFORE INSERT trigger on `audit_logs`. It fires only for the (target, after) pair named in a superuser-only table, so the window is deterministic, not timer luck.
- **Instrument:** `pg_stat_activity` rows with `usename='secuura_app' AND wait_event_type='Lock' AND wait_event='advisory'`, polled every 40 ms by the superuser during the hold. Plus `pg_locks WHERE locktype='advisory'`.
- **Control:** on 61c30de5 the same instrument reads **0 advisory waiters** in every cell, so it can tell the two apart.

Results on the head, 3 runs out of 3:

| cell | head (each of 3 runs) | 61c30de5 (control) |
|---|---|---|
| F1 X=upper-case tenantId and path userId, Y=lower-case (and the reverse) | Y waited on the advisory lock (**1 waiter seen**). Y answered after ~1205 ms. Final `[A3]`. Audits `[]→[A1]`, `[A1]→[A2]`, `[A2]→[A3]` | 0 waiters, final `{A2,A3}`, audits `[A1]→[A2]`, `[A1]→[A3]`: RED |
| F2 different users, same tenant | 0 waiters. Y answered in **4–5 ms** while X was held 1505 ms | same (control: no lock involved) |
| F3 a failing audit insert after the lock (ROLLBACK) | 500, then advisory locks held **0**, then next PUT 200 in 2–3 ms. Final `[A3]` | n/a |
| F3b SQLSTATE 08006 after the lock | **503**. Body exactly `{success:false, error:{code:'SERVICE_UNAVAILABLE', message:'The admin organisation scope could not be written, so nothing changed'}}`. 0 of the leak tokens (`terminated`, `08006`, the planted hostname `db-host-7`, `5432`, `postgres`, `sqlstate`, `stack`) appear, although the injected error message carried all of them. Audit delta 0, locks 0, next PUT 200 | 500 `INTERNAL_ERROR`: RED |
| F4 the backend killed mid-transaction while holding the lock | locks held during **1** and after **0**. 503 with the same fixed body. The next PUT for the same key: 200 in 3–4 ms (no hang). Audits show no trace of the killed write | 500: RED |
| F5 a platform token with no tenantId and no userId | 1 waiter. Final `[A3]`, audit chain exact | union: RED |
| F6 PR A's mint while a replace is held (observe) | mid-replace mint A1 **201**, A2 403, A3 403. After commit: A1 403, A2 **201**, A3 403 | identical |
| F7 an attempted deadlock: 2 users, 2 held PUTs, then opposite-order PUTs | 6×200, both audit chains hold, **0 `deadlock detected`** in the head windows | chains broken: RED |
| F8 20 concurrent writers, 5 organisations, random subsets, 0–80 ms jitter inside the transaction, ×3 rounds | all 200, 20 audit rows, **one chain from `[]` ending at the stored set**, every round of every run (9/9) | 500s and broken chains in 3/3 rounds: RED |
| F11 a real hashtext collision (see below) | Y **waited** (1 waiter, ~1203 ms). Both ends correct (`u1=[A2]`, `u2=[A3]`) | no wait |

- **Mint during a replace (F6): READ COMMITTED.** A mint sees the last committed scope for the whole duration of a replace (the old set until COMMIT, the new set after). It never sees a union and never sees an intermediate state, so it **never sees a grant wider than some committed request**. Nothing to fix.
- **Deadlocks** (`evidence/pg/server_log_deadlocks.txt`). The server log has 24 `deadlock detected` lines, and I mapped every one by timestamp:
  - 14:59:54–57: the 61c30de5 control run (old code, F8);
  - 15:14:42–44: mutant R1 (lock removed);
  - 15:15:40–42: mutant R3 (lock after the DELETE), which produces genuine **advisory-lock** deadlocks;
  - **zero in any head run.**

  So the fix also removes a deadlock and 23505 class the old code had under load, and the lock's position before the DELETE matters.
- **hashtext collision cost:**
  - **Instrument:** a superuser query over 400,000 random uuids finds pairs with equal `hashtext`. I found a fresh pair each run, e.g. `9018a1ce-…` / `c09bc7f6-…`, both `-1861540003`.
  - **Measured:** the collision **serialises** two unrelated ADMINs of one tenant, and the second waits for the first's whole transaction. Both results are exact.
  - **Cost:** throughput only, never correctness, because a collision only adds waiting. Expected colliding pairs for n ADMINs in one tenant ≈ n²/2³³, about 1.2×10⁻⁴ for 1,000 ADMINs. Across tenants a pair must collide on both 32-bit halves.
  - The same `(hashtext(tenant), hashtext(x))` namespace is shared with KS-1549's rotate lock at `index.ts:387`. A connectorId colliding with an ADMIN id in the same tenant would serialise a rotate with a scope PUT. That cannot deadlock, because each transaction takes exactly one advisory lock before any row lock (code read; not measured).
- **The lock key uses the normalised ids:** `UUID_TEXT = z.string().uuid().transform(toLowerCase)` (`index.ts:1543`) is applied to both `userId` and `tenantId` before line 1630. The rows are written with the same variables. F1 measured it concurrently, and mutant R4 (raw ids) is killed by F1.
- **Lock order in the code:** `applyTenantGuc` (1616), then the lock (1630), then `prev` SELECT (1631), DELETE (1635), INSERT (1637) and the audit insert (1646). Mutants R2 and R3 (moved below the SELECT or the DELETE) are killed.

**3. The audit row equals the stored state.**
- In every head interleaving I built, the second writer's `before` equals the first writer's `after`: F1 ×2, F5, F7, E ×9 and F8 ×9 rounds.
- In F8 (20 writers × 3 rounds × 3 runs) the audit rows always chain from `[]` to exactly the stored set, checked by an exhaustive search over row orderings, because `created_at` is stamped before the lock and is not commit order.
- **Control:** the same check fails on 61c30de5 in 3/3 rounds.

**4. m1** (`results/classifier_text.txt`, `classifier_equiv.txt`, `ks888_{head,old}.*`).
- **Byte-for-byte:** both regex literals in `isInfrastructureDbError` are byte-identical to the two inline copies at 61c30de5. The two old copies are identical to each other once the variable name is normalised.
- **Behaviour:** both predicates were copied verbatim into node and evaluated over **101,615 inputs**:
  - every 2-character SQLSTATE class with `000` and `001` suffixes;
  - the errno set, plus near-misses (`ECONNRESET `, lower case, `ENOTFOUND`);
  - numeric codes, objects with a custom `toString`, arrays, null and undefined values;
  - each infrastructure message and non-message.

  Result: **0 differences**, 54,928 infra-true. **Control:** a predicate with class 57 dropped is reported as different on 48 inputs.
- **The mint and revoke error cells**, KS-888 (19) and KS-1370 (9), on the head and on 61c30de5: **28/28 both, with identical cell names and outcomes** (`diff` empty). That covers mint 503 for 08006, ECONNREFUSED and the code-less pool timeout; revoke 503 for the same three; and the 500 `INTERNAL_ERROR` for the structural 42703.
- **Security unit:** 31 files / 336 on the head and on 61c30de5.
- **Mutants R13 and R14** (the mint or the revoke site reverted to never-infra) are each killed by 3 KS-888 cells, so the shared function is really what those sites call.
- **No leak in the 503:** the PUT's 503 body is a fixed string (F3b, B6, F4). The log line carries the SQLSTATE `code` and the raw `req.body.tenantId`, in logs only.
- **The 503 path writes nothing:** round 1's six injected faults plus the kill, at three pool sizes (item 1, B ledgers), and F3b/F4: rows unchanged, audit delta 0, locks released.

**5. m2** (F9, F9b, F10; schema in `results/catalogue.txt`).
- **The author's schema claim holds:** `users.status` is `character varying NOT NULL DEFAULT 'active'`.
- **The status values that exist** are the seven in the CHECK. Every one except `active` gives 404 with nothing written and nothing audited.
- **Should any be grantable?** I found nothing that should be:
  - auth refuses login for anything but ACTIVE (`routes/auth.ts:709`, `oauth.ts:961/1071`);
  - an `invited` stub becomes `active` on registration (`routes/auth.ts:195-258`), so an operator can scope it after that.
- **The hole is case** (finding m1).
- **Where the filter applies:** only to the target check. The previous-set read is on the scope table and has no status (correctly).
- **A status change mid-transaction:** n3.

**6. n3 and the spec** (`results/check_openapi_*.txt`, `openapi.txt`, `yaml_parse.txt`).
- **`npm run check:openapi`: rc 0** (`CHECK PASS`, 414 example blocks).
- **Control:** restoring the GET's `404: commonErrorResponses[404]` in `security.openapi.ts` makes it **rc 1** (`CHECK FAIL: generated YAML differs`). Restored with `git checkout` in my scratch tree, which is clean afterwards.
- **I regenerated the spec myself:** the YAML sha256 is `379ec0ad…` before and after, and `git status` is clean, so it is byte-identical.
- **Parsed with the `yaml` package** (61c30de5 vs head):
  - **GET** goes from `[200,400,401,403,404,429,500,502,503]` to `[200,400,401,403,429,500,502,503]`, with the new 200 description.
  - **PUT** is unchanged at `[200,400,401,403,404,415,429,500,502,503]`. That is the control: its real 404 stays.
  - `paths` 313 on both.
- **Against develop:** +202/−0 on the YAML, so no develop line is lost.
- **Spec readers:**
  - api-gateway full unit suite: **118 files / 1146**, rc 0 (includes the 4 spec-reading files);
  - auth's 6 spec-reading files: **77/77**;
  - security's 2 (ks1434, ks952) are inside the 336.
- **Platform suites NOT RUN** (by me or the author). The ones that would exercise the changed operations:
  - **Schemathesis**, with a **platform-role** token, would fuzz the GET against its now-404-less response set, and the PUT including its 503.
  - **Akto BFLA/BOLA** (a tenant ADMIN calling either route).
  - Preflight **legs 3/4/8** (spec-auth, path resolvability through the gateway, served spec).
  - Playwright and k6 do not apply.

**7. Mutants** (`tools/mutants_r2.py`; `results/mutants_r2_run.txt`, `mutants_r2.json`, per-suite JSON in `results/mut/`).

Method:
- The baseline was green first: author 15, adopted E 1, gate A 64, B 8, E 1, F 16, KS-888 unit 19.
- Each mutant was applied alone to the head's `index.ts`, and each anchor had to occur exactly once.
- After every mutant `index.ts` was restored from a byte snapshot, and its sha256 was asserted identical each time (`0af03466…` = `git show fdf314e0:…`).

Results:
- **The author's nine** (P1–P8, P10; anchors re-derived for the head where the text moved, e.g. P2's target SQL now carries the status filter): **9/9 KILLED**. For example:
  - P4 is killed by the author's m1 and atomicity cells, the adopted E, B1–B4 and F;
  - P5 by 6 author cells, the adopted E, A, B, E and F.
- **The author's delta-specific mutants:** I found **none**. The seat's tools folder holds only `mutants_ks1570b_v7.py` (the round-1 nine), and the ready mail lists no new ones. Nothing to re-derive.
- **Round 1's fourteen:** 13 KILLED, and **G7 SURVIVED**. As in round 1, G7 is equivalent: FORCE RLS on `users` bounds it.
- **C0, the comment-only control: SURVIVED** (nothing red).
- **Mine, aimed at the delta:**
  - **R1 lock removed: KILLED** by the author's adopted E, gate E and F (8 cells). E's kill is deterministic (the trigger holds X for 1.5 s), not timing luck: 9/9 on head, 6/6 red on 61c30de5.
  - **R2 lock after the previous-set SELECT: KILLED, but only by F** (F1 ×2, F5, F7, F8). **No author cell kills it**: finding m2.
  - **R3 lock after the DELETE: KILLED** (adopted E, gate E, F).
  - **R4 lock keyed on the raw request ids: KILLED, but only by F1 ×2**: finding m2.
  - **R5 user-id-only key: SURVIVED**, equivalent for correctness (n6).
  - **R6 tenant-only key: KILLED, only by F2** (it serialises different users).
  - **R7 lock inside a SAVEPOINT that is rolled back: KILLED** (adopted E, gate E, F). PostgreSQL releases the subtransaction's advisory lock.
  - **R8 m2 filter dropped: KILLED** (author m2, F9).
  - **R9 `lower(status)` (my proposed fix): SURVIVED**, as expected. No cell pins case: finding m1.
  - **R10 class 57 dropped: SURVIVED. R11 class 53 dropped: SURVIVED.** This is n2.
  - **R12 message arm dropped: KILLED** (F4, KS-888 ×2).
  - **R13 mint site never-infra: KILLED** (KS-888 ×3). **R14 revoke site never-infra: KILLED** (KS-888 ×3).
  - **R15 the PUT's 503 branch removed: KILLED** (author m1, F3b, F4).
  - **R16 the 503 body echoes the db message: KILLED** (F3b).
- **Totals:**
  - author 9/9;
  - round-1 gate 13/14 (1 equivalent);
  - round-2 gate 12/16. The survivors are R5 (equivalent), R9 (the fix itself) and R10/R11 (n2).
  - 0 LOADFAIL.

**Other author numbers, re-measured on the head:**
- security unit **31 / 336** (and the same on 61c30de5);
- security integration **6 / 76**;
- api-gateway **1146**;
- `tsc --noEmit` (security) **rc 0**;
- eslint `--max-warnings=0` on the 4 changed `.ts` files **rc 0**;
- `check:openapi` **rc 0**.

Controls:
- a planted file gives **1 `error TS`** (tsc rc 2);
- eslint gives **rc 1** (`no-var`);
- the planted file was removed, and the tree is clean.

**Shared unit (980): NOT re-run.** The delta touches nothing in `packages/` (`git diff --quiet 61c30de5 fdf314e0 -- '*package*.json' Blockchain/Dev/packages` rc 0).

## PR body vs code (item 8)
- **The live PR body could not be read.** My read-only `gh` attempt had no usable credential in a copied config (the token is not in that directory), and I made no further attempt.
- I checked the author's logged copy instead, `5_Project_History/2026-10-13_seatV-7th/logs/pr1539_body_final.md`: **16,602 bytes**, as claimed (sha256 `65f3ed9d…`). **I cannot vouch that it is byte-equal to what is on GitHub.**
- Against the code:
  - the head and round: present and correct;
  - the "replaces" claim: qualified (wording, n5);
  - **the grant table matches the statements in the code:** SELECT, INSERT and DELETE on `admin_organisation_scopes`, INSERT on `audit_logs`, SELECT on `users` and `organizations`, no UPDATE. the PUT handler (`index.ts:1555-1673`, read whole) contains no UPDATE statement;
  - "Hash recomputed": not my matter.
  - The m2 paragraph's "checked against the schema" is true but incomplete (m1).
- **The four ticket actions** (KS-1587, KS-1586, KS-1591, KS-1592): not verified. Linear is read-only for me, and I did not read it.

## NOT tested (plainly)
- **The live PR body, Linear, and the author's ticket actions.**
- **Preflight** legs 3/4/8 and the leg-14 arm.
- **The platform suites:** Schemathesis, Akto, Playwright, k6.
- **The gateway and the network:** no gateway process, no served spec, no CSRF or content-type path.
- **Environments:** any live or remote one.
- **Not re-run:**
  - **multi-tenancy mode** (`MULTI_TENANCY_ENABLED=true`). Round 1 found the flag inert for this service, and the delta does not touch tenancy;
  - shared unit and `packages/shared` tsc;
  - the tsc-with-tests config.
- **Not measured, code read only:**
  - the `FOR UPDATE` alternative (not chosen);
  - lock contention against KS-1549's rotate on a colliding connectorId.
- **The mint under real overlap at pool size 1:** not measured. At pool 1, cell E's serialisation comes from the single connection, not from the lock.
- **Could any of it hide a Major?**
  - The untested gateway path cannot change who may call (round 1: the guard reads only the verified JWT).
  - Tenancy mode is inert for this service.
  - The platform suites would find spec or status mismatches, not a grant widening.
  - **I see no untested surface that could hide a grant wider than requested, or an audit row that misstates the stored state.**

## Scratch state when stopped
- **Database:** the gate triggers, the hold table and its function were dropped by the cells. The scope table held 1 row (round 1's cell A leaves one; throwaway).
- **Server:** stopped with `pg_ctl -m fast`.
- **The head worktree** still holds the six gate test files. They are untracked, and live in my scratchpad only.
