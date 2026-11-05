GO WITH NOTES

# Gate 204: Secuura / Blockchain PR 2013 (KS-1460 rows 4 and 6 + the row-1 log), tier 1, round 1 of 2

**Subject:** head `ea1952fa00d7f942edb298af98728d20497e53a4`, one commit whose parent is base `5fc5569ed96a`. This verdict covers that SHA only.
**Head readings (refs/pull/2013/head, ls-remote):** 19:26:22 `ea1952fa00d7` (Wednesday), ~19:27 `ea1952fa00d7` (gate start), 19:47:02 `ea1952fa00d7` (end). **develop moved during the gate**, from `8c5da776eccf` (the commission's reading) to `688c5cc177f8` (PR 2012 / KS-1645 squash), read at 19:44:27. Q7 checks both. The shared checkout stayed on branch develop at `5fc5569ed96a` for the whole gate, and I used only read verbs on it.
**Environment:** by-SHA clones in this folder. `repo/` is head with a clean `npm ci --ignore-scripts` (1798 packages) and `packages/shared` built. `repo_base/` is base, with node_modules symlinked from `repo/` (same lock) and its own shared build. `own/` is head plus my gate-only test files and `routes/auth.gatebase.ts` (base's auth.ts, byte-copied by `git show`). Node v26.8.1 (not LTS), vitest 4.1.12.

## BLUF
The change does what the ruling asks, and I measured it rather than taking the READY's word. With the real `userRepo.updateUser` / `updateUserOrThrow`, I drove 50 base-vs-head cells: two routes × five stored levels × five write outcomes. Every SOCIAL raise that did not land (UPDATE matched 0 rows) gets **503 SERVICE_UNAVAILABLE at head in 4 of 4 cells**, where base answered 200 with tokens or `linked:true`. In those cells head creates no session, mints no token, sends no Set-Cookie and gives no success body. Every landed write, and every account already at SOCIAL or higher, is **identical to base** (status, normalised body, cookies, session/mint counts, write count) in 30 of 30 cells. A write that throws behaves the same on base and head. Head never issues a session or token that base did not, in 50 of 50 cells. For row 1, the login answer, headers, writes and sessions are byte-identical base vs head in 4 of 4 modes. Only the log line differs, and the new warn carries none of the planted password, hash or token markers. Scope is exactly the 6 paths, and the ks795 edit is mock-only (proved below). Mutants: 3 of the seat's 7 plus 1 of mine, all killed. The suites match the READY to the count. The merge onto both develop heads is clean, with 0 shared paths. Two Minor findings and two Notes, none blocking.

## Findings

**F1 (Minor): head answers 503 for a SOCIAL raise that DID land when the read-back comes back empty. That is a refusal outside the ruled "write did not land" case.** Location: `routes/auth.ts:1402` and `:1492` → `repositories/userRepo.ts:968-977` (`updateUserOrThrow` throws on any `null`). `updateUser` also answers `null` when the UPDATE matched a row but the trailing `getUserById` read-back finds nothing (`userRepo.ts:917-929`). The repo's own comment at `userRepo.ts:932-958` says `null` cannot tell those two causes apart.

MEASURED AT RUNTIME (cell `blind`: UPDATE rowCount 1, read-back SELECT empty) on the callback and the link route, levels basic and none. Base gives `200` with tokens / `linked:true`. Head gives `503`, no session, no token, and the database already holds SOCIAL. 4 of 4 such cells.

Mitigation: the 503 text says "Please retry — if you already succeeded, you may not need to". A retry reads level SOCIAL, skips the write, and succeeds; my `social` cells show that path as 200. Reachability is READ ONLY: the UPDATE and the read-back use the same tenant scope (`userRepo.ts:884-929`, QA F-1), so a blind read-back needs a row that is deleted or re-scoped between the two statements, or a tenant that cannot be resolved. This is the accepted KS-1052 design, not new code, but Q3 asked for any such input to be named. Oracle: Purpose (the ruling refuses *non-landed* writes). Fix shape, if wanted: none needed in this PR. A future `updateUser` that returns rowCount separately from the read-back would separate the two causes. Evidence: `ev_own_social_table.tsv` (rows `blind`), `_gate204-own-social.test.ts.txt`.

**F2 (Minor): the row-1 warn text claims the stronger cause that the repo's own contract forbids.** Location: `routes/auth.ts:569` logs *"the rehash write did not take effect (non-fatal); the old hash stays"* on any `null` from `updateUser`. For the reason in F1, `null` can also mean "landed, read-back blind", and in that case the new argon2id hash *was* stored and "the old hash stays" is false. `updateUserOrThrow`'s doc comment (`userRepo.ts:944-952`) records exactly this wording being removed as defect F-929-2 ("could not be confirmed", never "was not applied"). The two fragments repeat the claim. READ ONLY for the login path; the social analogue is MEASURED (F1). Severity Minor: the line is log-only, the case is rare, and the ruling asked only for "a warn otherwise". But the ticket exists to make this line truthful. Fix shape: "the rehash write could not be confirmed (non-fatal); the next login retries". Evidence: `ev_pr.diff`, `ev_own_login_table.txt`.

**F3 (Note, pre-existing, unchanged): the rehash catch logs the thrown message verbatim.** `routes/auth.ts:579` (`error: reason`). Planted: an `updateUser` throw whose message carries `Bearer PLANT_TOKEN_G204 <new hash>` is logged with both markers, **on base and head equally**. The PR does not touch this branch. The new warn and info lines carry only `{ userId }`, and none of the 5 plant markers appear in them. Evidence: `ev_own_login_table.txt` (mode `throwToken`).

**F4 (Note, pre-existing, unchanged): an infrastructure DB error on the SOCIAL UPDATE answers 500 INTERNAL_ERROR, not 503.** `updateUser` does not classify infra errors, unlike `getUserById`. MEASURED: an `ECONNREFUSED`-coded throw gives 500 on base and head, with no session or token on either. That fails closed and is outside the ruling. Evidence: `ev_own_social_table.tsv` (rows `infra`).

## Questions, measured
1. **Scope:** exactly 6 paths (`ev_pr2013_paths.txt`). `auth.ts` has 3 hunks, and each maps to row 1 (`:558-571`), row 4 (`:1394-1403`) or row 6 (`:1485-1493`). Nothing else changed. **ks795, line by line** (`ev_ks795_proof.txt`): numstat `6 0`, one `-U0` hunk `@@ -123,0 +124,6 @@` inside `vi.mock('../repositories/userRepo', ...)`, 2 comment lines plus a 4-line `updateUserOrThrow` mock. 0 deleted lines. 0 added lines containing expect / it( / describe / toBe / toEqual. Necessity control: base's ks795 file run against head fails 5 of 41 (the controls that mint or link: `updateUserOrThrow` is not a function). With the edit, 41 of 41 pass (`ev_ks795_basefile_at_head.log`).
2. **Rows 4 and 6, base vs head** (`ev_own_social_table.tsv`, own test `_gate204-own-social.test.ts.txt`). Real router, real errorHandler, real `userRepo` (`updateUser`, `updateUserOrThrow`, `fromRow`). Doubled: the `db.query` below the repo, the social provider, session/Redis, jwt, lockout, logger and the authenticate middleware. That is a little wider than "only repos/providers", and the extra doubles are infrastructure the routes need to run.
   - **Not landed (0 rows), level basic or none:** head is 503 SERVICE_UNAVAILABLE in **4 of 4**, with no session, no token, no Set-Cookie and no `"success":true`. Base was 200 with tokens / `linked:true` in 4 of 4.
   - **Landed:** head equals base in **4 of 4**.
   - **Level SOCIAL / STANDARD / HIGH:** no level write on either side, and head equals base in **30 of 30**, including all failure modes.
   - **Write throws (plain or infra):** 500 on both sides, no session or token, in 8 of 8.
   - **Blind read-back:** see F1.
   - The callback sets no cookie on base or head in any cell.
   - Aside: an unknown stored level (`verified`) maps to a raise on both sides, which is base behaviour.
3. **Direction:** head sessions ≤ base and mints ≤ base in **50 of 50** cells. The refusals head adds are the ruled 0-row case (8 cells across both routes and both levels) and F1 (4 cells).
4. **Row 1** (`ev_own_login_table.txt`, own test `_gate204-own-login.test.ts.txt` on the seat's ks1868-style harness, base and head routers side by side). Modes: lands / 0 rows / throws / throws with secret. Status, normalised body, response headers, write list and session count are **equal in 4 of 4**. Logs:
   - lands: info "rehashed" on both;
   - 0 rows: base logs info "rehashed", head logs the warn (F2 on its wording);
   - throws: the same "rehash failed" warn on both.
   - Plants (password, old hash, new hash, Bearer token, minted token) are absent from every head log in the lands and 0-row modes (F3 for the throw mode).
5. **Mutants** (`ev_mutants.log`, script `_mutants.py.txt`). Every mutant compiles (tsc rc 0), the file was restored, and its sha256 `77a5c620…` was asserted after the run.
   - Seat's 1 (row 4 back to `updateUser`): killed by the seat's row-4 RED cell and my 2 zero cells.
   - Seat's 4 (row 6 `.catch(() => null)`): killed by the seat's row-6 RED cell and my 2 zero cells.
   - Seat's 6 (row-1 branches swapped): killed by both seat row-1 cells.
   - **Mine, M8** (the raise moved after `createSession` + `generateTokenPair`, so the 503 is sent after the mint): killed by the seat's row-4 RED cell (sessions 0) and my cells. Caveat: M8 also writes for already-SOCIAL accounts, so it is a coarser mutant than intended.
6. **Suites.** I ran vitest with cwd = services/auth. My first pass used `--root` from another cwd, and ks1009 and ks1467 then failed on both sides for that reason alone (they resolve paths from cwd), so I discarded it.
   - Auth full suite: **base 1,685 of 1,687; head 1,693 of 1,695.** The only failures are the same 2 `ks949-platform-admin-seed-identity` cells on both sides, as 5000 ms timeouts. Isolated with a longer timeout at head: 31 of 31 (`ev_ks949_isolated_head.log`). auth.integration ran green here.
   - `tsc --noEmit` (auth): rc 0. Planted TS2322: rc 2.
   - `check:test-types` auth: 41 errors, 41 in the baseline, 0 new, 0 stale, 143 test files.
   - eslint on the 4 changed .ts files: 0 problems. A planted unused var is reported at `auth.ts:1403`.
   - docs-fragments `check`: OK. A planted unbalanced `<table>` in the new flow fragment gives FAIL rc 1, and after the restore it is OK again (`ev_plants.log`).
7. **Merge** (`ev_mergetree.txt`). The PRs were mapped to develop squashes by message: PR 2007 = `cb1cadfa2` (per gate 202's commission), PR 2010 = `c9cb07738`, PR 2011 = `8c5da776e` (KS-1185, inferred; PR 2011's head `40d3f247` is not in the local object store), plus PR 2012 = `688c5cc17`. Shared paths with each: **0, 0, 0, 0**. Planted control (`cb1cadfa2` list plus `auth.ts`): 1. `merge-tree` onto `8c5da776eccf`: rc 0, tree `389157a7ef9b`. Onto the current develop `688c5cc177f8`: rc 0, tree `10ddf27848e1`. In both, the changed paths equal the PR's 6.

## NOT tested
- A real Postgres 0-row UPDATE (fail-closed RLS), a booted auth service, a real social provider, real Redis/session/jwt. Every runtime result above comes from in-process doubles below the repository.
- The four platform suites (Schemathesis, Akto, Playwright, k6). Node 24 LTS: everything ran on v26.8.1.
- The seat's other 4 mutants (row-4 catch, row-6 back to `updateUser`, info always, warn dropped). By design, the commission asked for 3 of 7.
- Rows 2, 3 and 5, and KS-1672's social-id persistence: out of scope by ruling.
- PR 2007/2010/2011 heads as PR refs (objects not local). The check used the develop squash commits.
- The full suite on the merged tree.

## Gate conduct
I made no change to the project or the shared checkout, and posted nothing anywhere. Planted edits and mutants touched only `own/`. Each one was restored, with an asserted sha256 or an equality check. `own/` still holds my two gate tests and `auth.gatebase.ts`; copies of the tests are kept here as `_*.txt`. The clone directories are gitignored (`.gitignore:323`). I used no `cd`: cwd-dependent runs went through a python `subprocess(cwd=...)` wrapper.
