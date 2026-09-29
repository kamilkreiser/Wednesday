`Refs KS-1054`

## What this does
ONE predicate that both deploy scripts call. The migration runner already returns its failed count
and `/health` already reports it, so the deploy's existing `/health` checks can see a half-migrated
database instead of passing over it.

**Kam's ruling, option (a), verbatim** (`secuura-ks1054-f9282-migration-failure-visibility`,
`ruled_ts=2026-09-28T20:24:31.316795+10:00`):

> **[a] Keep serving, flag it on /health** — The migration run returns its failed count. /health
> reports it, so the deploy scripts' existing /health checks (deploy-all.sh:281, deploy.sh:823) see
> it and the deploy reads as failed. The running service is not stopped.

## The shape, as claims with reasons
- **ONE predicate, called by both scripts.** `deployment/azure/check-startup-migrations.sh` is the
  single reader; `deploy-all.sh` and `deploy.sh` each invoke it. Cells C1 and C2 pin each call site,
  C3 pins that `deploy-all.sh` fetches the `/health` **body** and not only the status code.
- **Keyed on `failed`, never on `error`.** Cell P3 pins it. A core statement failure is served as
  `failed: N` with **no** `error` field, so an `error`-keyed check reads that as clean. Measured
  under gate39's finding N G39 2.
- **`/health` itself is untouched.** There is no service code in this diff — the four files are the
  helper, the two deploy scripts and the test suite.
- **An ABSENT field PASSES, and says so loudly** (cell P4). Failing closed on absence would block a
  **rollback** to an older image that has no such field, which is the one deploy you most need to
  work when migrations are broken.
- **A non-JSON body and an empty body are SKIPPED and named, never a silent pass** (P5, P7). P7 pins
  an actual defect the author hit: an EMPTY argument fell through to `cat` and hung on stdin.
- **Wrong-type values are refused, not coerced** (P6): `failed: "two"` is rejected rather than read
  as zero.

## Test Evidence
**Touched:** `Blockchain/Dev/deployment/azure/check-startup-migrations.sh` (new),
`Blockchain/Dev/deployment/azure/deploy-all.sh`, `Blockchain/Dev/deployment/azure/deploy.sh`,
`Blockchain/Dev/scripts/__tests__/ks1054_deploy_scripts_read_startup_migrations.test.sh` (new).
4 files, +201/−0.

**Ran, at base `0aa9b52c691b`, head `2075c3ec7078`:**
- Shell suite, **whole branch: 11 passed / 0 failed** (rc 0) — cells P1-P7, C1-C4.
- Shell suite, **test half alone** (the two deploy scripts reverted to `0aa9b52c691b`, the new helper
  removed, the test file byte-identical): **0 passed / 11 failed** (rc 1). Restored by byte copy and
  proved equal by sha256 on all three; the tree read 0 tracked modifications afterwards and the
  suite returned to 11/0.
- `bash -n` clean on all three shell scripts (3 checked, 3 clean).
- **The helper's RECORDED mode is `100755`**, asserted with `git ls-tree 2075c3ec7078 --
  Blockchain/Dev/deployment/azure/check-startup-migrations.sh` (blob `8ef35013e2c2`). This matters
  because both deploy scripts invoke the helper directly, so a recorded `100644` would die
  `Permission denied` in a fresh clone. **The on-disk `-x` bit is NOT the evidence**: this repo has
  `core.filemode=false`, so git ignores it. **Control that prints the other way:** the same command
  on the test file in the SAME commit prints `100644`, so the instrument discriminates rather than
  returning `100755` for everything.
- **Rebase integrity.** This branch was rebased twice (onto `2cb858335472`, then onto
  `0aa9b52c691b`). `git diff <base> <head>` is **byte-identical to the diff stored before the first
  rebase** — `cmp` rc 0, 12,296 B, sha256 `c661dfaf9283beb8` both sides. Controls: a one-byte
  mutation of a copy `cmp`-differs, and a **whitespace-only** mutation also `cmp`-differs while
  `git patch-id` reports the **same** id (`76f97e2c57aa6967`) for both — which is why `cmp` is the
  proof here and patch-id is only corroboration. Commit message byte-identical before and after
  (`cmp` rc 0), author unchanged.
- Push preflight: **12/15 legs ran, 3 SKIPPED — legs 3, 4 and 8, "local stack not up". Nothing
  failed.** That is the hook's own wording and **it is not a pass**; the ratio is stated as a ratio.

**NOT run:**
- **The deploy scripts were not executed against any real environment.** No Azure, demo or kintsugi
  deploy, and no migration run against a real database. The cells drive the predicate with fabricated
  `/health` bodies, so what is proved is the predicate's reading of a body, not an end-to-end deploy.
- Preflight legs 3, 4 and 8 (they need a running local stack on `http://localhost:6882`).
- The four platform suites (Schemathesis, Akto, Playwright, k6) — this change adds no HTTP surface
  and no service code, so none of them exercises it.

**Migrations + config:** no migration file, no schema change, no config or environment default
changed. Nothing to apply and nothing to roll back beyond the three shell files.

## Not covered / owed
- **RUNTIME change → a §5f live sweep is owed.** The predicate ships in the deploy path; it is not
  proved against a live deploy by this PR.
- The helper's behaviour when `/health` is unreachable altogether (as opposed to returning a
  non-JSON or empty body) is not pinned by a cell.

Foreign ticket keys are de-hyphenated on purpose so this PR attaches only its own: KS 1332 (the
N 1332 5 predicate this continues), KS 5, KS 733.
