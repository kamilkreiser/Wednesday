## QA GATE - TIER 1, round 1: GO WITH NOTES

**Surface check (top line):** test-only PR on the auth surface. Zero product bytes (proved below). The new cells do pin what KS-1804 note 2 asked for: the burn runs exactly once, on a healthy sign-in and when the read-back fails. The faulted-case cell is the only cell in the backup-code test set that kills one realistic double-burn mutant (e2 below). Two weaknesses are older than this PR and outside its scope, and both should be filed: the burn is not safe under concurrency (F1), and no cell checks WHAT the burn writes (F2). TIER 1 is right.

**PR:** Secuura/Distributed_Secuura #1826, "Refs KS-1804: pin the backup-code burn to exactly one UPDATE users (note 2)" (Seat T 7th)
**Head:** `020803325b05e819e2d235f1e873907fa9a7b7af`. `git ls-remote` of refs/pull/1826/head showed this SHA at the start (2026-10-30T01:11:03Z) and at the end (01:26:08Z). It matches the claim.
**Develop:** `530f091120d5da749edf972e8e0089e44cfc5589` at both reads. The merge-base equals develop (1 commit on top, no merge-in), so the merge is a fast-forward.
**Gate:** QA gate 30. Findings only. I fixed, commented, pushed, merged and deployed nothing, and wrote nothing under `!CODING/`.

### Counts
1. **spark_gate (run first; `facts.json` is beside this file):** diff 3 files / +41 / -0, head asserted as tip. Targeted on HEAD: **8 passed / 0 failed**. On BASE product code: 8 / 0. That BASE column is expected for a test-only PR (the product is the same), so it is NOT a red-first. Red-first comes from the tampers in point 4. The counts are real, not the 0/0 runner defect.
2. **Scope** (`git diff --stat` and `--name-status`, three-dot develop...pr1826): exactly the 3 declared files. The test file has +14 (two cells, one helper, one comment), the flow doc +11, the cheat sheet +16. **Zero product bytes:** the blob of `passwordLoginGate.ts` is `c4d562c54b8e` at both develop and head (`git rev-parse <ref>:<path>`). Its sha256 in my clone is `b11d690dc858e92b…`, the author's value, and it was the same at the end of the gate.
3. **Is "exactly one UPDATE users" the right invariant?** I read `passwordLoginGate.ts` lines 255-307 and `userRepo.ts` `updateUser` / `updateUserOrThrow` (lines 799-980) at develop.
   - The burn does `user.mfaBackupCodes.splice(index, 1)` and then calls `updateUserOrThrow(user.id, { mfaBackupCodes })`. That issues `UPDATE users SET mfa_backup_codes = $1, updated_at = NOW() WHERE id = $2`: it overwrites the **whole array**, matched **only by id**. There is no condition on the code being present, no row lock and no compare-and-swap.
   - Within one request, exactly one burn UPDATE is the right invariant. Zero would leave the code valid; two is a double write. For this fixture it is also exactly one `UPDATE users` overall. Caveat F4: an account with a legacy-plaintext secret legitimately issues a second `UPDATE users` through `reencryptMfaSecretIfLegacy` (userRepo.ts ~1834).
   - **Concurrency:** the product does not guard it, and the cells say nothing about it. See F1.
4. **Tampers.** Instrument: `tamper.py`, beside this file. Each tamper replaces one anchor (count asserted to be 1), the mutant must transpile with no diagnostics first, and the mutant copy is kept in the scratchpad (outside `src/` and `__tests__`). Each run is vitest json. Every tamper was restored by byte copy with the sha256 equal (`b11d690dc858e92b` for the gate, `6ea5c4715825adc9` for userRepo), and `git status` was clean after each. Results on the PR's file (8 cells) and on all **32 auth test files that touch backup codes** (347 cells):

   | Mutant | PR file (8) | All 32 files (347) | Killed by |
   |---|---|---|---|
   | (a) burn UPDATE removed (code reusable) | **6 red** incl. both N2 | 9 red | N2 x2, F3 x4, ks1052 A1/A2, ks781 LEG 4 |
   | (b1) splice the wrong index (used code kept) | **8/8 green** | **347/347 green** | **nothing** |
   | (b2) splice removed (array written unchanged) | **8/8 green** | **347/347 green** | **nothing** |
   | (b3) `splice(0)` (every code destroyed) | **8/8 green** | **347/347 green** | **nothing** |
   | (b4) the UPDATE loses `WHERE id` (all users' rows) | **8/8 green** | 6 red | other files only (ks1050, ks1194); no backup-code cell |
   | (c) author's shape: extra `updateUserOrThrow` before the burn | 1 red (healthy N2) | 2 red | N2 healthy, ks1052 A2 |
   | (c2) author's shape, non-throwing extra `updateUser` | **2 red (both N2)**, the author's 2 of 8 reproduced | 5 red | N2 x2, ks1052 A1/A2, ks781 LEG 4 |
   | (d) a second burn after the real one | 1 red (healthy N2) | 2 red | N2 healthy, ks1052 A2 |
   | (e) burn retried inside the catch | 1 red (faulted N2) | 2 red | N2 faulted, ks1052 A1 |
   | (e2) retry in the catch only on a read-back fault | 1 red (faulted N2) | **1 red** | **N2 faulted only** |

   Baseline and final were both 8/8 and 347/347. The author's tamper reproduces as 2 of 8 only when the extra UPDATE does not throw (c2). Through `updateUserOrThrow` it gives 1 of 8 (c), because in the faulted case the extra call throws first and the real burn never runs. Both are red, so the claim holds.
5. **Whole auth suite.** vitest 4.1.12, `--maxWorkers=3`, cwd `services/auth`, each run started only when the 1-minute load was below 8 (`runsuite.py`). Two runs each side, alternating:
   - **HEAD:** 110 files, **1328/1328** in both runs.
   - **develop 530f0911:** 110 files, **1326/1326** in both runs.
   - The delta is +2, exactly the two N2 cells (ks1188-f3: 8 cells at head, 6 at develop). The author's 1328 and 1326 match.
   - **The ks949 flake (KS-1053) did not fire:** ks949 was 31/31 in all 4 runs. The flake is therefore UNMEASURED by this gate on both sides, neither confirmed nor refuted.
6. **Concurrency probe** (`g30-probe-race.test.ts`, beside this file). It runs the real gate over a STATEFUL db stub that applies the burn UPDATE last-write-wins. It was copied into `__tests__` for the run only and then removed.
   - **P0 control:** the same code used twice in sequence gives ok, then refused, so the stub models single-use.
   - **P1:** two concurrent sign-ins with the SAME code, each holding its own snapshot of the row: **both `{ok:true}`**.
   - **P2:** two concurrent sign-ins with DIFFERENT codes A and B from `[A,B]`: both succeed, and **one spent code is left in storage and is accepted again** (`{ok:true}`).
   - **Firing control:** expecting 1 success in P1 fails with `expected 2 to be 1`.
7. **Predicted merge** (`merge-tree --write-tree origin/develop origin/pr1826`, in my clone): rc 0, tree `bade5aa4d481…`, identical to the head's tree (a fast-forward). Nothing conflicts today, not even the html docs. They will conflict once any of #1823/#1824/#1825 lands first (see Merge-prep).

### Findings (none blocks this PR)
- **F1 (Major, PRE-EXISTING product, out of this PR's scope; recommend filing).** The single-use burn is not atomic.
  - **Where:** `passwordLoginGate.ts:273-285` + `userRepo.ts:891-894`. The code reads, then splices in memory, then writes the whole array by `WHERE id` only.
  - **Effect:** two concurrent logins with one backup code both get a credential, and two concurrent logins with different codes can leave a spent code valid (a lost update). Measured against a stateful stub (probe P1 and P2), NOT against Postgres.
  - **Board search (Linear `searchIssues`, includeArchived):** no ticket matched literally on "backup code concurrent", "backup code race", "mfa_backup_codes race" or "backup code twice"; the fuzzy hits were KS-809, KS-1052 and KS-1081, none about concurrency. Control: a nonsense term gave 0. KS-1052 and KS-533 contain no race or concurrency text (grep).
  - **Possible remedies (not built):** `UPDATE … SET mfa_backup_codes = array_remove(mfa_backup_codes, $hash) WHERE id = $id AND $hash = ANY(mfa_backup_codes)`, requiring rowCount 1; or `SELECT … FOR UPDATE` in a transaction.
- **F2 (Minor, test strength, pre-existing).** No backup-code cell pins WHAT the burn writes.
  - Burning the wrong index, writing the array unchanged, or deleting every code (b1/b2/b3) all pass every one of the 347 cells.
  - The new healthy cell is titled "burns the code with exactly one UPDATE users" but asserts only the count. `ks781` LEG 4 ("authorizes AND is burned") asserts only that `updateUserOrThrow` was called.
  - **Suggested pin:** record the `values` in the db stub and assert that the written `mfa_backup_codes` equals the stored array minus the used hash.
- **F3 (Note).** The count was already pinned for the healthy case on develop: `ks1052-backup-code-burn-cause-a` A2 asserts `updates()).toHaveLength(1)` (line 137), and it kills c and d.
  - So the healthy N2 cell is a co-located duplicate. The faulted N2 cell is the new pin: it alone kills e2.
  - This settles KS-1804's "probably not done" honestly: half done before, done now.
- **F4 (Note).** The helper counts every `/^\s*UPDATE\s+users/`, not the burn's own UPDATE.
  - It is correct for this fixture (the stub row has `mfa_secret: null`, so the legacy re-encrypt is a no-op). A fixture with a legacy-plaintext secret would legitimately show 2.
  - Filtering on `mfa_backup_codes =` would make the invariant exact.
- **F5 (Note, docs).** The docs say the measurement was taken at develop `a786e06e6f6e`. This is disclosed in 122.2, and the auth tree is unchanged to `530f0911` (the blob is equal).

### Merge-prep (doc only, required at merge; not code)
- **M1.** "the file walks the whole checkout" (flow doc 122.1; the cheat sheet carries the same figure) should be corrected as the author promised. ks949's walks at lines 300-314 (`SKIP_DIR`) and 523-536 (`SKIP = node_modules|dist|build|coverage|.git`) skip those directories. I read both at head.
- **M2.** **The section number `122.` collides with #1823**, which also adds `<h2>122.` (`git show` of each PR head's flow doc). #1824 uses 123, #1825 uses 124, and develop's highest is 121. Renumber at merge to whatever develop holds then.

### FIX-BEFORE-MERGE
(none)

Recommended follow-ups (Wednesday's call): file F1 as a tier-1 product ticket (the backup-code burn is not atomic); file F2 as a test pin (assert the written array); M1 and M2 at merge-prep.

### TESTED / NOT TESTED / HOW
**TESTED**
- Head pin at both ends.
- spark_gate.
- Diff scope and product-byte equality (blob + sha256).
- A read of the burn path and `updateUser`/`updateUserOrThrow`.
- 10 tampers (6 of my own semantic mutants, plus the author's shape in two forms), on the PR file and on all 32 backup-code files, each sha256-restored.
- A concurrency probe with a control and a firing control.
- The whole auth suite twice at head and twice at develop.
- html_docs_check rc 0 on both docs at head and at develop, and rc 1 on planted copies (`<p>` prose outside a table, one per doc).
- Section numbers across #1823-#1826.
- merge-tree.
- Linear KS-1804, KS-1188, KS-1052 and KS-533, read-only, plus a board search.

**NOT TESTED**
- A real Postgres: F1 is shown only on a stateful stub.
- The integration config (`vitest.integration.config.ts`).
- tsc and eslint (the author reports 42 baselined errors and 0 new).
- The four platform suites, a running stack, Node 24, the pre-push hook legs.
- A render of the docs.
- KS-1804 note 1 (not in this PR, disclosed).
- The ks949 flake itself: 0 of 4 runs.

**HOW**
- **The clone:** `git clone --shared` of the checkout into the then-non-existent path `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/3595961a-a258-453d-996e-1aad78887d58/scratchpad/gate30/clone`.
  - `rev-parse --show-toplevel` was asserted equal to that path before any fetch.
  - origin was set to the GitHub URL, and the checkout's `core.sshCommand` was copied in (read with `git config --get`).
  - I fetched pr1826 and develop (and later 1823/1824/1825 for the section numbers only).
  - The clone was checked out at head, and develop was in a worktree `wt_dev`.
- **Dependencies:** each tree got its own `npm ci --ignore-scripts` (1806 packages), then `fix-libsodium-symlink.js`, then a `packages/shared` build with rc 0 and `dist/index.js` present. Nothing was symlinked from another tree. spark_gate's own worktree used `--node-modules` set to my clone's hoisted root.
- **Cleanup:** the final `git status` is clean in both trees. Every process I started (npm ci, vitest via runsuite.py, the tamper runs) exited on its own, so nothing was killed. The evidence files are beside this file.

### Instrument errors
- **I1.** My first head suite run used `vitest --root` from the WEDNESDAY cwd, so ks1009 (could not locate the Dev root) and ks1467 S1/S2 (ENOENT on a relative path) failed: 1315 cells, 2 red, 1 file failed. I discarded it and re-ran with cwd = `services/auth`. The counts in point 5 come from the re-runs.
- **I2.** My first probe run used `npm --prefix … exec`, which kept the WEDNESDAY cwd ("No test files found", rc 1). I re-ran it with `--root`. The probe has no cwd-relative reads.
- **I3.** The shared-box hooks refused: `$VAR` paths in git write verbs (re-issued with literal paths), `rm` via `$VAR`, a compound `cd`, and an unquoted `=====`. Separately, zsh's `$r:P` modifier mangled one ref loop (re-issued as `${r}`). Nothing ran under a refused call.
- **I4.** spark_gate's BASE 8/8 is not a red-first for a test-only PR (see point 1).
