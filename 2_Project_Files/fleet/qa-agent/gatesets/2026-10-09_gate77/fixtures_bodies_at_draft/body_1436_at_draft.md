Refs KS-808 — https://linear.app/secuura/issue/KS-808

Raised from a Wednesday-held Spark pass (`spark_secuura_2026-10-05_KS-808-applied-counts-skips`, REVIEW HOLD and READY held 2026-10-08), re-proved by Seat F 6th on develop `1e7f90e26137`; develop `81d2e5f4c415` (#1435, KS 1452, the handlebars lock refresh) was then merged in, and it touches none of this PR's files.

## What changes
Defect (2) of KS-808 only: the summary of the deploy-path migration runner counted skipped migrations as applied.

- **Before:** `apply_one` returned 0 for an *already applied* skip as well as for a real apply (`Blockchain/Dev/scripts/run-migrations.sh:119-122` at the base), and the loop counted every 0 into `applied_count`. A re-run over an up-to-date database printed `Summary: applied=N failed=0` with N = every file.
- **After:** `apply_one` counts its skips (`:122`), the counter is initialised before the loop (`:148`), skips are subtracted before the summary (`:175`), and the summary line gains ` skipped=N` (`:176`): `Summary: applied=A failed=F skipped=S`. `Migration runner finished (applied=…, failed=…)` (`:200`) keeps its format and now reports the true apply count. Line numbers are the built file's.
- **Unchanged:** the return codes of `apply_one`, the loop's branches, all SQL, and the exit code. Since KS 1031 (#1183) the runner exits 3 on any failed migration (built `:197`, documented in the header at `:26`); that is defect (1) and it is not touched here. Defect (3), the tracker citation, was #1229 (merged 2026-09-25).
- Two comment lines go beyond the held payload (Q-5D808, comment-only): a WHY line above `:122` and above `:148`, each naming defect (2) and the prior behaviour, so every changed line carries its reason.

KS-808 stays open; whether it closes after the owed live run is Wednesday's call.

## Test Evidence
**Touched (4 files):** `Blockchain/Dev/scripts/run-migrations.sh` (+8/-1) · NEW `Blockchain/Dev/scripts/__tests__/ks808_run_migrations_counts_skips_apart.test.sh` (+104) · the two platform docs (flow block `41.`, cheat section KS-808).

**Ran** (in the pushing worktree; `/bin/bash` 3.2.57, node v24.7.0, npm 11.5.1, vitest 4.1.11 as read from `Blockchain/Dev`):
- **Product red / green.** The new suite points its own `RUN_MIGRATIONS_SH` knob (suite `:18`) at a copy of the BASE runner blob `7318c392c1f2`, with no edit to the tree: **3 passed, 2 failed, rc 1**. The two failing cells are the defect itself: one applied + one skipped, and an all-skip run, both printed `Summary: applied=2 failed=0`. Against the built runner: **5 passed, 0 failed, rc 0**. `psql` and `pg_isready` are stubs in a private `mktemp` tree; no database is dialled.
- **Siblings:** `run_migrations_failure_exit_code.test.sh` 7/0 at the base and 7/0 after; `ks1054_deploy_scripts_read_startup_migrations.test.sh` 40/0 (its subject `check-startup-migrations.sh` is not touched); `ks949_main_seed_idempotence.test.sh` **27 passed, 0 failed** in leg 14 of the push, against a real PostgreSQL 15.14 (`27 passed, 0 failed (of 27 cells); wall-clock 8s`).
- `sh -n` on the runner and `bash -n` on the suite: rc 0.
- **Two true +/- readings of the runner**, both correct: the held patch is +8/-3 (`git apply --numstat`), the payload tree is +6/-1 (its third hunk removes and re-adds two blank lines), and the built file is +8/-1 (the payload tree plus the two WHY lines).
- **Mode:** the new suite lands **100644**. `run-shell-suites.sh:360` runs every suite as `bash "$REPO_ROOT/$rel"` with no `-x` test; `__tests__/` holds 39×100644 and 15×100755 suites with this one; its nearest sibling `run_migrations_failure_exit_code.test.sh` is 100644; and leg 10 checks only `.sh` paths invoked bare from a `package.json`, which this suite is not. The runner stays 100755 in the tree.
- **Both docs, appended byte-for-byte** (`docblockra3.py` at the base; the merge-in changed neither doc, so the blobs are identical at the head): the flow doc goes from 31 to 32 numbered blocks with its tail moving from `39.` to `41.`, and all 31 pre-existing blocks are byte-identical. The cheat sheet goes from 20 to 21 `<h2>` sections with its tail moving from `KS 593` to this ticket's section, all 20 pre-existing headings are byte-identical, and it still ends `</html>`. In each doc the ONLY difference from the base blob is the fragment, byte for byte, and a 1-byte-altered fragment fails the same comparison (the control). The tool's verdict: `0 failed`. `html_docs_matrix.test.sh` 12/0 in leg 14 is not offered as evidence that the blocks are well-formed.
- **Re-proved at the merge commit `90d98754db7b`** (develop `81d2e5f4c415` merged in, tree `43a9d3089e19`): `npm ci --ignore-scripts` re-run in the worktree, so `handlebars` on disk is 4.7.10 (it was 4.7.9); the suite again **5/0** green and **3/2** red against blob `7318c392c1f2`; legs 6 and 7 standalone (`npm run audit:gate`, `npm run audit:locks`) **rc 0 / rc 0**, and the three handlebars advisory ids (GHSA-8r5x-fm3f-whwj, GHSA-p8wg-vrv2-v86f, GHSA-xw65-4hp5-5hc7) are named 0 times. The same count reads 3 each in the refused push's log.
- **The push's own gate lines, verbatim:**
  - leg 2: `All 35 standalone lock(s) pass clean-room npm ci.`
  - leg 5: `OK — 59 audit-contract cases pass (expected 59)`
  - leg 6: `audit-gate: 9 distinct advisories reported, 24 baselined.` then `OK — no advisories outside the triaged baseline.`
  - leg 7: `audit-locks: 43 standalone lockfiles` … `OK — no standalone-lock advisories outside the triaged baseline.`
  - leg 10: `OK — 4 bare-path .sh invocation(s) are tracked at mode 100755 (21 invoked via an interpreter, mode not applicable)`
  - leg 12: `OK — all 72 tracked shell suite(s) are reached by the runner.`
  - leg 14: `ks808_run_migrations_counts_skips_apart: 5 passed, 0 failed` and `shell suites: 72 passed, 0 failed, 0 skipped (of 72)`
  - leg 15: `OK — 13 code guards passed.`
  - verdict: `PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` / `legs 3 4 8 — local stack not up; you can clear this by starting it.`
- The held READY's last line ("Raise is blocked until develop is green on pre-push leg 14", 2026-10-08 03:25) is superseded: leg 14 is green above.

**NOT run:** the four platform suites (Schemathesis, Akto, Playwright, Performance/k6) are **UNMEASURED**, because there is no local stack; the push printed SKIP lines for them, not passes. The runner was never run by its own container `/bin/sh` against a real PostgreSQL with a skip present: **a live run is owed** (SKILL §5f). The runner ships inside the `migrations` image (built from `services/originate/Dockerfile`), so that run needs a rebuilt `migrations` service.

**Migrations + config:** no migration file and no config changed; the migration RUNNER's summary line changed (it gains `skipped=N`).

## Deploy-path note
- The summary line's only code consumer is `run_migrations_failure_exit_code.test.sh:82`, which matches `Summary: applied=2 failed=0` as a prefix and stays green.
- Prose that still describes the pre-change `applied=N` line is named here and **not edited** (no MD edits in this PR): `Blockchain/Dev/deployment/DEPLOYMENT-ARCHITECTURE.md:82`, `Blockchain/Dev/deployment/KINTSUGI-REBUILD-RUNBOOK.md:216`, `:241`, `CLAUDE.md:21`, `.claude/skills/secuura-test-discipline/SKILL.md:351`, `systemTest/CLAUDE.md:232`, `:779`.

## Project rules walked
- **Language boundary (SKILL §5e):** both files are shell, POSIX `sh` (the runner) and `bash` (the suite), in `Blockchain/Dev/scripts/`, which holds 54 tracked `.test.sh` beside the runner they test. Named here rather than claimed by silence.
- **SKILL §5c** is systemTest-only; no file under `systemTest/` is touched.
- **Slot literals:** the suite's `DB_URL="postgresql://secuura:pw@localhost:5432/secuura"` (`:24`) is a stub URL that is never dialled, and it is the same literal develop already carries at `run_migrations_failure_exit_code.test.sh:22`.
- **Both platform docs** are updated in the same commit (SKILL §4). The change alters no timing either document carries.

🤖 Generated with [Claude Code](https://claude.com/claude-code)
