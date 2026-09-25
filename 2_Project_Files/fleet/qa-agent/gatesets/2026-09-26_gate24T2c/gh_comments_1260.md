--- comment 5835115552 by linear[bot] at 2026-09-25T15:38:39Z
<!-- linear-linkback -->
<details>
<summary><a href="https://linear.app/secuura/issue/KS-1139/bare-arithmetic-command-x-under-set-e-exits-1-at-0-and-bash-41-errexit">KS-1139 Bare arithmetic-command `((X++))` under `set -e` — exits 1 at 0 and bash ≥ 4.1 errexit kills the script: 10 errexit-live sites remain in `sync-secrets.sh` (×8) and `validate-lint.sh` (×2) after #977's docker-build.sh fix</a></summary>
<p>

## BLUF

The class fixed in `docker-build.sh` by PR #977 round 2 (KS-877) and in `validate-env.sh` by KS-680 is still present at **10 errexit-live sites in two host scripts**. An arithmetic command exits 1 when its expression evaluates to 0, and a post-increment yields the OLD value — so `((COUNT++))` at COUNT=0 "fails", and bash ≥ 4.1 `set -e` exits the script on it (bash COMPAT item 45), silently. bash 3.2 (macOS) does not apply errexit to arithmetic commands, so these scripts pass on the Mac and die on Linux / CI / containers at their first count.

## Census (develop `3fc158c39`, 2026-09-13)

Instrument: the CELL 4 regex from `Blockchain/Dev/scripts/__tests__/docker_build_empty_table.test.sh` — `^[[:space:]]*\(\([A-Za-z_][A-Za-z_0-9]*(\+\+|--)\)\)[[:space:]]*$` — over tracked `*.sh` (`git grep -nE`, `[[:space:]]` not `\s`: BSD grep). Positive control: 2 hits on `docker-build.sh` at `a70585823`, 0 at `aede93117`.

| file | sites | errexit | context |
| -- | -- | -- | -- |
| `Blockchain/Dev/deployment/azure/sync-secrets.sh` | **8** — `:186 :192 :198 :204 :216 :221 :227 :232` (`SKIPPED`, `GENERATED`, `UPDATED`) | `set -euo pipefail` at `:20` | each inside an `if … then` BODY (not a condition) — errexit-live; the first `((SKIPPED++))` / `((GENERATED++))` / `((UPDATED++))` at 0 exits the script on bash ≥ 4.1 |
| `systemTest/schemathesis/validate-lint.sh` | **2** — `:33 :38` (`PASS_COUNT`, `FAIL_COUNT`) | `set -e` at `:6` | to be confirmed at the site (a tested context suppresses errexit) |
| `Blockchain/Dev/scripts/validate-env.sh` | 3 — `:62 :81 :99` | `set -e` at `:9` | **NOT defects** — inside `if check_required_var …` bodies, where errexit is suppressed for the whole function (KS-680 measured both ways); listed so the census is complete |
| `Blockchain/Dev/scripts/docker-build.sh` | 0 at `aede93117` (2 at `a70585823`) | `set -euo pipefail` | fixed in #977 round 2 |

## Fix shape (measured on 3.2.57; the shape Peter named on the archived bash-3.2 portability ticket, and KS-680's at `validate-env.sh:179-219`)

`COUNT=$((COUNT + 1))` — an assignment's exit status is 0 at every value and the effect is identical. Not `((++X))` (a pre-decrement evaluates to 0 at the last step and fails there); not `((X++)) || true` (masks the status instead of removing the failing construct).

## Durable home

`Blockchain/Dev/scripts/check-script-portability.sh` has 7 rules and none for this construct (a "rule 8" was proposed on the portability ticket and reverted on KS-666). The census regex above is the candidate rule; the suite's CELL 4 shows the shape with its positive control.

## Searched before filing

`RUNNING++`, `((RUNNING`, `arithmetic command`, `post-increment`, `errexit`, `set -e`, `bash 4.1`, `sync-secrets`, `validate-lint` — 0 literal title hits among open issues; the archived homes (KS-680 and the docker-build portability ticket's defect (c)) surface only with `includeArchived: true`. Not fixed this round — filed on Wednesday's ruling (s208, 2026-09-13).
</p>
</details>
<!-- linear-review-link -->
<p><a href="https://linear.app/secuura/review/ks-1139-arithstatus-the-8-sync-secrets-counters-stop-returning-1-at-ea6076b087e5">Review in Linear</a></p>

