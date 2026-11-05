GO WITH NOTES

# Gate 205: Secuura / Blockchain PR 2014 (KS-1968 B2, breached password refused at change-password), tier 1, round 1

**Subject:** head `fb1e054d53a8fb258f050034e5b26c637ab9c664`, base `5fc5569ed96ac61f64823cc9e1fa841899aa1f62`, develop `688c5cc177f85a11e050357856eb69ee4f4a9069`. This verdict applies to that head SHA only.

**Head readings** (from local refs only; no network, so no ls-remote): 20:11:44 clone, detached at fb1e054d5 (branch `feature/ks-1968-b2-breached-password-refused-at-change-password`). 20:29:05: the project's `refs/remotes/origin/feature/ks-1968-b2-…` still reads fb1e054d5, and my clone's HEAD reads fb1e054d5.

## BLUF
The change does what Kam ruled, and I measured it on the real route.

- **Refusals:** a breached password is refused only when the breach service actually answered. The answer is 422 `VALIDATION_ERROR` with Kam's sentence and one `details` entry on `newPassword`.
- **Outage and switch:** every outage cell (throw, 503, timeout) and every `HIBP_ENABLED=false` cell is identical to base. **24 of 24** decision-table cells are as ruled.
- **No side effects:** a refusal makes no hash call, no store check, no write and no session revocation. A wrong current password, a weak password or a too-short password makes no lookup.
- **Privacy:** only the 5-character prefix leaves the process. Planted marker passwords, their full SHA-1 and the suffix appear in no URL, fetch init, response body or log line. This holds even when the thrown error text carries them.
- **Mutants:** 6 of 6 killed (3 of the seat's, 3 of my own).
- **Suites:** they match the READY: 1,695 tests, and the only failure is a known ks949 timeout.
- **Merge:** clean onto develop, with 0 shared paths.

There are five Notes. None blocks, and four are pre-existing or environmental.

## Findings
- **N1 (Note, pre-existing, not changed by this PR): only the exact string `false` turns the check off.** At `services/auth/src/services/password.ts:160`, `HIBP_ENABLED=FALSE`, `0` and `off` all leave the check ON. With the service answering, a breached password then gets 422 at change-password (base: 200). This is B1's switch semantics, and the PR now reaches them from change-password as well. It is consistent with "behind the existing switch". An operator who writes `HIBP_ENABLED=0` expecting the check off will be surprised. MEASURED AT RUNTIME. Evidence: `ev_decision_table.txt` (rows `extra|sw=FALSE/0/off`).
- **N2 (Note, pre-existing, not changed): the range-body match ignores the count.** At `password.ts:175-178` the code splits each line on `:` and compares the suffix only. With `Add-Padding: true`, HIBP adds padding rows with count 0. If a padding row ever carried the user's suffix, the password would be refused as breached. The probability is negligible, and the fix (require count > 0) belongs to password.ts, which is outside this PR's scope. READ ONLY.
- **N3 (Note, disclosed by the seat): an outage costs latency.** With the real 2 s `AbortSignal.timeout` (`password.ts:168`), the timeout cells answered 200 after the abort, so they are allowed as ruled. A deployed container with no egress to the breach service will wait up to 2 s on every change-password. MEASURED AT RUNTIME with a hanging stub that honours the signal. A real egress probe is NOT RUN (no external host was called).
- **N4 (Note, environment): the run was on a non-LTS runtime under load.** Node v26.8.1 is not LTS, against the project's LTS rule; the seat ran on the same version. The ks949 cells time out at the 5000 ms default under load ~8-10, on base too. In isolation, base had 1 timeout and head 3; all are `Test timed out in 5000ms`, and none is an assertion. Evidence: `ev_suites.txt`.
- **N5 (Note, coverage): the open-PR heads are unverified.** The heads for PR 2008 (`587db03ce`, KS-1150) and PR 2013 (`ea1952fa0`, KS-1460) were read from the project's local remote-tracking refs, not by ls-remote, because no network was allowed. If either PR has moved since, its shared-path count must be re-read.

## Answers to the commission
1. **Scope:** exactly 4 paths, +236/-1, one commit on base. `password.ts` is unchanged. `users.ts` changes only line 16 (the import gains `isPasswordBreached` and `BREACHED_PASSWORD_MESSAGE`, plus a comment line) and the block at `users.ts:997-1005` inside the `/me/change-password` handler. Evidence: `git diff --numstat` (in `ev_mergetree.txt` context) and this report's diff read.
2. **Order:**
   - **Setup:** the real route, real `authenticate` (a real RS256 token), the real errorHandler, the real password module (spied with call-through: real hash and verify, real strength rules, real `isPasswordBreached`) and the real winston logger with a capture transport. Doubled: userRepo, the session store, db/events and the breach fetch.
   - **Breached, head:** the sequence is `repo.getUser>pw.verify>hibp.fetch`, with hash 0, store 0, write 0 and revoke 0.
   - **Clean, head:** the sequence is `getUser>verify>hibp.fetch>hash>isRedisAvailable>write>revokeAll>isRedisAvailable`.
   - **No lookup:** a wrong current password gives 400 with 0 lookups; a weak password gives 422 "too weak" with 0 lookups; a too-short password (zod) gives 400 with 0 lookups. Base and head match on all three.
   - Evidence: `ev_decision_table.txt` (`order|…`), test `_gate205-own-change-password.test.ts.txt`.
3. **Decision table:** {breached, clean} × {ok, throw, 503, timeout} × {unset, true, false}: **24 of 24** as ruled. The 422 appears in exactly 2 cells (breached, ok, switch unset or true). Every other cell has the same status and body as base (200 "Password changed successfully"), with the same hash, write and revoke counts. Extra rows: 429, 500 and an unparseable 200 body are all allowed (200). Evidence: `ev_decision_table.txt`.
4. **Privacy:**
   - **What leaves:** for 5 service modes × 2 marker passwords, each URL is `https://api.pwnedpasswords.com/range/<5 hex>`. The fetch init carries only `Add-Padding` and a signal.
   - **Grep results:** the markers, the full hash in upper and lower case, the suffix, and the current password with its SHA-1 appear in 0 sent strings, 0 bodies and 0 log lines.
   - **Planted error text:** the planted throw text, which contains every one of those values, was produced 6 times. The log carries only `thrownType: "Error"` or `"DOMException"`.
   - **Controls:** the capture transport recorded a control line, and an independent grep of the captured file finds 0 markers and 5 occurrences of the prefix.
   - Evidence: `ev_privacy_head.txt`.
5. **Direction:** in all 30 head/base pairs, no input that base refused is allowed at head. The only new refusal is breached-and-answered with the switch not exactly `false` (see N1 for the spellings).
6. **Mutants (all tsc rc 0, files restored and git-status clean):**

   | Mutant | Seat's test | My test |
   |---|---|---|
   | S1 check disabled | 3 failed | 3 failed |
   | S2 lookup after the write | 1 failed | 2 failed |
   | S3 current password checked | 2 failed | 2 failed |
   | G1 prefix+suffix sent, own | 2 failed | 2 failed |
   | G2 outage fails CLOSED, own | 1 failed | survived* |
   | G3 lookup after the store pre-check but before the write, own | 1 failed | 2 failed |

   *G2 survives my vitest file because its table cells assert only status ∈ {200, 422}. The table is judged by the base-vs-head comparison, not inside vitest. That is a weakness of my instrument, not the PR's; the seat's test kills G2. The first G1 form, `range/${sha1}`, was inadmissible (tsc TS6133), so it was redone with the admissible form. Evidence: `ev_mutants.txt`, `_mutants.py.txt`.
7. **Suites** (by-SHA clones, deps from gate 204's `npm ci` of the identical lock, `@secuura/shared` built in-clone, cwd = the auth service dir):
   - **Auth vitest, head:** 1,694 of 1,695 passed, 142 files. The 1 failure is a ks949 5000 ms timeout.
   - **Auth vitest, base:** 1,687 of 1,687 passed, 141 files. Head adds 8 tests.
   - **Seat's file:** 8 of 8.
   - **Classification:** the ks949 timeout is the same class on base (it also times out in isolation, N4). It is not new. The ks795 and ks819 cold-import hook timeouts did not recur this run.
   - **Static checks:** `tsc --noEmit` rc 0 (a planted TS2322 gives rc 2). `check:test-types` auth: 41 in the baseline, 0 new, 0 stale. That run examined 143 test files including my gate file; my gate file added no error. eslint on `users.ts` plus the new test: 0 problems (a planted unused var is reported at `users.ts:1007`). docs-fragments `check`: OK. A planted unbalanced `<table>` in the new flow fragment gives FAIL rc 1, and after the restore it is OK again.
   - Evidence: `ev_suites.txt`, `ev_plants.txt`.
8. **Merge** (`ev_mergetree.txt`):
   - **Onto develop:** `merge-tree` onto develop `688c5cc177f8` gives rc 0 and tree `d72035eb2e72`. Merged vs develop differs in exactly the PR's 4 paths.
   - **Since base:** develop moved 4 commits (`cb1cadfa2` KS-1262, `c9cb07738` KS-1504, `8c5da776e` KS-1185, `688c5cc17` KS-1645, which are PRs 2007/2010/2011/2012) and 24 paths. Shared with PR 2014: **0**. Planted control: 1.
   - **Open PRs:** OPEN PR 2008 (6 paths) shares 0 paths, and PR 2013 (6 paths) shares 0. Both are measured from base, and their heads are local refs only (N5).

## Not run / not covered
- A real breach-service call and a booted service.
- Container egress.
- The four platform suites: not commissioned, and no stack was allowed.
- Node 24 LTS.
- Register and reset (B1), and `POST /api/users/admin/create`.

## Method and boundaries
- **Clones:** `repo/` (head) and `repo_base/` are `git clone --shared` by SHA, inside this folder and gitignored (`.gitignore:324`).
- **Dependencies:** `node_modules` are symlinks to gate 204's install of the byte-identical lock. The project's own install is stale (zod 3.25.76 against lock 4.6.7); it was tried first and abandoned to `_quarantine_2026-11-05/`.
- **Cache:** the vitest cacheDir was redirected to `cache/`. 0 files newer than the start marker exist in the project's or gate 204's `.vite` or `dist` directories.
- **Gate-only additions (not product):** in `repo/`, `vitest.gate205.config.ts`, `src/__tests__/gate205-own-change-password.test.ts` and `src/routes/users.gatebase.ts` (base `users.ts`, sha1 `eb06e2a1…` equal to `git show`).
- **No outside effects:** no network call, no `cd`, no write into `!CODING`, nothing posted, no rm. No long-lived process was left running.
