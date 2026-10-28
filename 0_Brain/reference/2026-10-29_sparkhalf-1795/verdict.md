# Spark half, PR #1795 (KS-1780 parts 1 and 3), Seat R 6th

- Operator: claude-sonnet-5-5, Spark gate-half operator, gauge 84%. Spark model: deepseek-v4-flash-0731 via the tunnel (UP, pid 52462).
- Pins (git ls-remote, at start and again at end): refs/pull/1795/head = `3b1741524383971b85037a6f048d9bc49e58c06c` (asked sha, equal). develop = `8fbda28e6e7988d7c1f218f3662cd6b2c0a4e204`. PR merge-base = `bd6697e079fce41db6b21e094a9eddb3d0e1d08e`.
- Wrote nothing to GitHub, Linear or mail. No process started that outlived its run. Load at start 4.7 (under 12; no wait).
- Clone: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/sg-1795/repo` (did not exist; git init; `rev-parse --show-toplevel` asserted equal before the first fetch and at the end). Deploy key of the Secuura Blockchain project via GIT_SSH_COMMAND, IdentitiesOnly. Work and evidence: `/private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/fccaae68-37b3-43d1-9466-4e52087c3d4f/scratchpad/sg1795/` (`out/` = facts.json, diff.patch, targeted_{base,head}.log, spark/review.json; worktrees under `w/` not removed).

## 1. Deterministic harness (spark_gate.sh, base = develop, jest auto-detected from the package's jest.config.js, as for #1787; read-only Dev node_modules)

Result is REAL (not 0/0, not blind). 87 s.

| Test file | HEAD product code | BASE product code (merge-base bd6697e) |
|---|---|---|
| ks1780-extract-pg-code-cannot-hang-a-webhook-patch.test.ts (8 cells) | 8 pass / 0 fail | 4 pass / 4 fail (B1 to B4 red; C1 to C4 green) |
| ks1780-system-errors-list-catch-cannot-hang-on-a-hostile-throw.test.ts (4 cells) | 4 pass / 0 fail | 2 pass / 2 fail (R1, R2 red; controls green) |
| Total | 12 pass / 0 fail, 2 of 2 files ok | 6 pass / 6 fail, 0 of 2 files ok |

On base, the four HTTP cells (B1, B2, R1, R2) receive `{status: "NO ANSWER", body: null}`: the hang is measured by the test, not inferred.

## 2. Spark review (spark_review.py, ticket KS-1780, facts minus the two Projects Documents html files, plus a note that the jest result is valid)

**Spark verdict: NO GO.** 2 Major, 2 Minor, 2 Note. One attempt, valid, 55.6 s, 19,762 prompt tokens. All six `evidence_quote_found_in_input: false`.

### Each Major, checked at source in the head worktree

- **Major 1 ("only 2 of the 17 sites; 15 adminConfig.ts catches remain"): TRUE AS A FACT, HARMLESS AS A DEFECT.** The PR is parts 1 and 3 by title; part 2 (adminConfig.ts) is not in the diff (name-status: systemErrors.ts, pgErrors.ts and two tests only). The PR's own docs say it twice ("The third part of KS-1780, the catches in routes/adminConfig.ts, is a separate change and is not here"; "Not measured: the other catches ... adminConfig.ts"). A scope statement, not a regression; the open work is KS-1780 part 2 (also a canonical Spark run, `ks_1780_p2_admin`).
- **Major 2 ("the tests do not measure a hang, only the constant 500"): FALSE.** The test's `patchWithThrow` aborts after 1500 ms and returns the string `NO ANSWER`; on base the received value in B1, B2, R1, R2 is exactly `status: "NO ANSWER"` (targeted_base.log lines 46, 92, 183, 229). The hang is a red assertion. One true nuance inside it: on base, jest also attributes the escaping TypeError ("Cannot perform 'get' on a proxy that has been revoked", at extractPgCode, webhooks.ts:320) as the first failure message; the PR's doc states that openly. Not a defect.

### The Minors and Notes (not asked, one line each)

- Minor 3 (isZodError, "a real ZodError with a throwing prototype is not pinned"): incoherent; a genuine ZodError has a normal prototype, so `instanceof` is true and C2 pins the ZodError arm. Harmless.
- Minor 4 (B4 covers only a meta getter): TRUE, LOW. B2 covers the `code` getter through the route and B3 a revoked Proxy; a throwing `message` getter alone is not a cell. The single try covers all three reads, so it is a pin gap only.
- Note (byte-identical claim "unverifiable"): it is verifiable and is TRUE, see section 3. Note (synthetic values): TRUE and disclosed by the PR ("The hostile values are synthetic").

Net: **0 defects confirmed.** Spark's NO GO is driven by two Majors that are a stated scope boundary and a misread of the test. Same pattern as the gate 6 and gate 8 NO GOs (see those verdicts).

## 3. Byte-identity with the canonical Spark patches

Canonical: `2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1780_p1/out.md.checker/` and `.../spark_secuura_2026-10-28_ks_1780_p3_webhooks/out.md.checker/` (`section_1.diff` product, `section_2.diff` test; both checkers PASS 7/7, apply_mode=strict).

| Part | Product hunks | New test file |
|---|---|---|
| ks_1780_p1 (routes/systemErrors.ts, +13/-1) | all added and removed lines `cmp` identical; canonical section_1 applied with strict `git apply --check` (rc 0) to the base blob gives the PR head file byte for byte | content `cmp` identical (sha256 efbf89ed01b0bf5e...) |
| ks_1780_p3_webhooks (utils/pgErrors.ts, +10/-0) | same; strict apply to base gives the head file byte for byte | content `cmp` identical (sha256 8476fb7798452d0e...) |

**Byte-identical: YES** in effect (resulting product files and both test files). Only the hunk header framing and context lines in the diff text differ (the PR's diff shows git's function-name context; canonical headers are bare); every +/- line is the same.

## Not run
Whole originate suite, tsc, lint on the PR (the harness's own lint/unit logs were not read), the adminConfig sites, a deployed stack. Spark review is a shadow opinion, not the gate verdict.
