`check-startup-migrations.sh` treated a python3 that is PRESENT BUT BROKEN as "the /health body is not
JSON", so a deploy whose migration status could not be read exited 2 (PASS-WITH-SKIP) instead of
failing closed. python3 being ABSENT already failed closed (rc 1); a python3 that runs and exits
non-zero did not.

Two files: the predicate (+4/−2) and a new shell suite (+27).

## Kam's ruling, quoted verbatim

Card `secuura-ks1054-f9282-migration-failure-visibility`, `choice='a'`,
`ruled_ts=2026-09-28T20:24:31.316795+10:00`:

> [a] Keep serving, flag it on /health — The migration run returns its failed count. /health reports
> it, so the deploy scripts' existing /health checks (deploy-all.sh:281, deploy.sh:823) see it and the
> deploy reads as failed. The running service is not stopped.

Wednesday's standing ruling on the exit codes, as a stated decision: python3 ABSENT fails closed
(rc 1); python3 PRESENT BUT BROKEN fails closed (rc 1); a genuinely non-JSON body keeps rc 2.

## Test Evidence

**Touched:** `Blockchain/Dev/deployment/azure/check-startup-migrations.sh` (100755) and
`Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh` (100644).
No service code, no migration, no config, no lock, no gate file.

**Ran — red-first on TWO runners, rc captured on its own line:**
- macOS: with the change **40 passed / 0 failed**; with the predicate reverted to develop and the new
  suite kept, **38 passed / 2 failed**, and the reds are **exactly P10 and P10b** (set comparison rc 0,
  zero reds at head). Restored by byte copy (`cmp` rc 0, mode 755) and green again 40/0.
- `python:3.12-slim` (**bash 5.2.37, coreutils 9.7, Python 3.12.14**, `--network none`, source mounted
  read-only and copied to a writable layer): **40/0**, base **38/2**, reds **exactly P10 and P10b**,
  restored **40/0**.
- **Neither red is vacuous:** `P9-FIXTURE` ("python3 is absent under the stub PATH") and
  `P10-FIXTURE` ("python3 is on the stub PATH and exits non-zero") are green in every arm, so the
  cells below them are driven rather than skipped.
- The two reverted-product arms ARE the tamper arms: the guard alone reddens exactly those two cells.

**Rebase provenance (this branch carries an earlier seat's commit, rebased twice):**
the stored diff at the original base and the diff at this base are **`cmp`-equal, rc 0** (4175 bytes
both), with identical patch-ids (`ac8aa72adcea1dfe15e59d03ce3fe53550db9ca6`) across both rebases; both
product files are byte-identical to the original commit (`cmp` rc 0 each). Committed modes read from
the tree: **100755** predicate, **100644** suite — the 100644 file is the control in the same commit.

**Preflight, quoted as the hook prints it, NOT as a pass:**
`PREFLIGHT INCOMPLETE — 12/15 legs ran, 3 SKIPPED. Nothing failed.` ·
`legs 3 4 8 — local stack not up` · `This is NOT a pass. Do not quote it as one — say which legs ran.`
Inside it: **shell suites 61 passed, 0 failed, 0 skipped (of 61)**, **13 code guards passed**.

**NOT run / NOT covered:**
- **The whole shell runner does not discriminate this change** — it reads 61/0/0 both with the change
  and at the base. Stated because a green runner here is not evidence for this diff.
- The macOS python3 shim: **not reproducible on this Mac; unmeasured on a Mac without developer tools.**
- `deploy.sh` / `deploy-all.sh` were **not driven end to end** with a broken-python3 stub.
- The scripts were **not run against any real environment**. No deploy. **Merged is not deployed**, and
  the §5f live sweep remains owed, blocked on KS 1380.
- Round 1 of 2 on this class.

**Migrations + config:** none.

Refs KS-1054
