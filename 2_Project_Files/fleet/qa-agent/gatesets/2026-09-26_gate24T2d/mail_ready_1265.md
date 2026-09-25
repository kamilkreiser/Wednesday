## #1265 KS-1315 (Seat L7, round 25, tier 2) — NO READY MESSAGE ID WAS HANDED TO THE DRAFTER (Wednesday named it as "the newest READY FOR QA (Seat L7): #1265 mail"; locating it would need a listing, which marks mail seen): the PR BODY instead (REST GET, gh_body_1265.md)
SOURCE gh_body_1265.md
TEXT_SHA256 e4182d19a76866b053f1b1b51849adb9bacb68c20f306a3c09fb36a62ccb327a
#1265 KS-1315 head 87ef6a1b088754ab773f541ddb273acce8dfab4f

#1265 KS-1315: row the four sibling argv spellings the QA-961-1 fallthrough covers
head 87ef6a1b088754ab773f541ddb273acce8dfab4f

## BLUF

**Test-only.** Four argv spellings that the KS-1111 (QA-961-1) fallthrough masks had **no row that discriminated them**, so the suite could not tell the real fix from one handling only the three rowed shapes. Four rows added. **Each is measured RED under T-1**, not argued to be.

`Refs KS-1315`

## The rows

| row | spelling | name |
|---|---|---|
| L05 | `--label -one -qe=NAME=VALUE` | `API_KEY` |
| L07 | `-a -e --env=NAME=VALUE` | `ADMIN_TOKEN` |
| L04 | `-e -e -eKEY=VALUE` | **`KEY` exactly** |
| L01 | `--label -e --env=NAME=VALUE` | `DB_PASSWORD` |

## Measured, not reasoned

**T-1** reverts the QA-961-1 fallthrough (`return masked === arg ? maskOneArgumentForms(arg) : masked;` → `return masked;`).

- **Before these rows:** T-1 reddens **3** — L02, L03, L08.
- **After:** T-1 reddens **7** — those three plus **all four** rows above.
- At head, unmodified: **0 red**, 1108/1108.

Reds were read from vitest's `--json` `fullName`, never the bare title — a truncated `$label` carries no `describe` prefix and cannot be attributed to a row.

## The name is part of the row, and that is measured too

`SECRET_ENV_NAME` is `/PASSWORD|PASSWD|SECRET|TOKEN|MNEMONIC|(?:^|_)KEY$/i` — **unanchored** for the first five, **anchored** only for `KEY`.

- In the **`=` forms** (`-qe=`, `--env=`) the broken path splits at the first `=`, so the name it reads is the literal `-qe` or `--env`, which matches no clause. Those rows leak whatever they are named, so L05/L07/L01 carry ordinary secret names.
- In the **attached form** (`-eKEY=V`) the broken path reads the whole glued token `-eKEY` as the name. An unanchored word still substring-matches there, so such a row is masked **by accident** and is green before the fix.

**Proof, run in this tree rather than quoted from the ticket:** renaming L04's `-eKEY` to `-eADMIN_PASSWORD` takes the file from **7 RED to 6 RED** under T-1 — **L04 alone turns green**, i.e. that row would pin nothing. That is why L04 is named `KEY` exactly, for the same reason L03 is. The reverted rename is not in this PR; only the measurement is, in the file's comment.

## Test Evidence

**Touched**
- `systemTest/performance/tests/unit/runner/k6DockerRedaction.test.ts` — four `it.each` rows plus the naming note. **Test-only: no product file is in this PR.**

**Ran**
- `npm run test:unit` (`vitest run --config vitest.unit.config.ts`) in `s-l7-ks1315/systemTest/performance`, at develop `4db87c3e4b98`: **1104/1104 bare → 1108/1108 patched**, 63 files, **+4 = exactly these rows**. Load average **5.98** bare / **8.84** patched. Baseline taken before the edit on a clean tree (0 uncommitted files).
- `npm run lint` → **rc 0**. That is `tsc -p tsconfig.json --noEmit` **and** `tsc -p tsconfig.node.json --noEmit` **and** `eslint`. Both tsconfigs matter here: `tsconfig.json` **excludes `tests`**, so `tsconfig.node.json` is the only one that type-checks this file at all.
- T-1 arm and the naming arm, above. The product file was byte-copied outside the repo before the tamper and restored — **sha256 `36377af024eb…` identical, `git diff -- runner/k6_docker.ts` 0 lines.**

**NOT run**
- **No preflight. This is a `systemTest/` path and the pre-push hook gates on `^Blockchain/Dev/`, so the 15-leg preflight was skipped entirely** — the push took 13 s. Only `[format-gate] 1 package(s) checked, 0 skipped, 0 failed` ran. **The fleet STOP count was therefore never executed, and this PR quotes none.**
- No k6 run against any environment, and no docker run of the k6 image. The echo is exercised through the unit harness only.
- **Labels only, not behaviour:** this PR adds no product change. The masking is already correct at develop; what was missing was evidence that it is correct for a reason rather than by coincidence.
- The `-l`/`--label` boundary cell and the KS-1098 name-set question are untouched — the latter stays with Peter.

**Migrations + config**
- **None.** No migration, schema, runtime config, `package.json`, lockfile, Dockerfile, route or OpenAPI surface.

## Note for the reviewer

Labels are 29–32 characters, under vitest's ~37-character truncation of an interpolated `$label`, so each row remains identifiable in a failure line.
