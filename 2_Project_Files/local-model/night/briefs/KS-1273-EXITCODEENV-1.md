# KS-1273 EXITCODEENV-1 JOB 04 PASSES --exit-code 0 TO TRIVY SO A TRIVY_EXIT_CODE IN THE CALLER'S ENVIRONMENT CAN NO LONGER TURN AN IMAGE WITH FINDINGS INTO scan-failed — Wednesday's task for Ornith, BASH_PATCH, **ONE script (one hunk: one line changed, one comment line added) + ONE NEW `*.test.sh`** (written 05:5x AEST on 2026-09-21 from the file at develop `362e51fe0db7e73d5557924902763fe3f10fd8c7` — `04-container-trivy.sh` read whole, 133 lines)

Written from origin develop `362e51fe0db7e73d5557924902763fe3f10fd8c7` (measured by `git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 05:38 AEST 2026-09-21 — the #1111 KS-1223 WALLET-1 merge; read verbs only on the source checkout).
`Blockchain/Testing/jobs/04-container-trivy.sh` at that tip: sha256 `0720a4bfa4a4e8d3…`, **133 lines** (`wc -l`). Lines 92-95 carry no blank line; line 93 occurs ONCE in the file (`grep -c -F -x`: 1); the three context lines `:92`, `:94`, `:95` each occur once (1 / 1 / 1).
The ticket KS-1273 (Backlog, Kam, 0 attachments; refs KS-1136) was read: its fix shape is exactly this — *"Pass `--exit-code 0` to trivy explicitly in `Blockchain/Testing/jobs/04-container-trivy.sh`, so its rc means 'the scan ran', never 'it found something'. Add a cell … with the env var set."*

## THE MODE — read this twice

**BASH_PATCH.** Your diff contains EXACTLY TWO files:
1. `Blockchain/Testing/jobs/04-container-trivy.sh` — ONE hunk: ONE `-` line, TWO `+` lines.
2. `Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh` — ONE NEW file (`--- /dev/null`).

**In THIS tier the paths are FULL repository paths** — the checker applies with `git apply -p1` from the repository root. Nothing else changes: not `container_trivy_failed_scan_is_loud.test.sh` (your READ-ONLY reference, the KS-1136 suite), not `container_trivy_image_filter.test.sh` (the KS-867 suite), not any other job.

## What is wrong (one paragraph)

Since KS-1136 (#1051) job 04 keeps trivy's own exit code in `trc` (`:93`) and treats a non-zero `trc` as a FAILED scan (`:115-:117`: `error: "scan-failed"`, `counts: {}`, `vulns: []`), then exits 1 with `could not scan` (`:126-:129`). That is right when trivy could not scan. But trivy ALSO exits non-zero when it FOUND vulnerabilities, if its exit code is set — by `TRIVY_EXIT_CODE` in the caller's environment or by `exit-code:` in a `trivy.yaml` — and the job passes no `--exit-code` of its own (`:87-:93`: `--quiet --format json --severity … --vuln-type … --skip-db-update "$img"`). So in such an environment an image WITH findings is recorded as `scan-failed` with its findings DROPPED, the job exits 1 and says `could not scan` about an image it did scan (the KS-1050-1060 batch gate measured exactly this on #1051's head with a stubbed trivy: `TRIVY_EXIT_CODE=1`, 1 CRITICAL + 1 HIGH → scan-failed, 2 findings dropped, rc 1). No repo file sets either knob today (`git grep -i TRIVY_EXIT_CODE` at the tip: 0 files; control `exit-code`: 10 files; `trivy.yaml` in the tree: 0) — the defect is latent, and one exported variable on a developer's or a runner's shell arms it. **MEASURED on the real trivy 0.71.0 installed here (a local secret scan, no network, no DB): `TRIVY_EXIT_CODE=1` + findings → rc 1; the SAME scan with `--exit-code 0` on the command line → rc 0 (the flag wins over the environment, as viper's precedence promises); `--exit-code 1` alone → rc 1; `TRIVY_EXIT_CODE=1` with no findings → rc 0.** **This task: pass `--exit-code 0` explicitly on the `"$img"` line (`:93`), so `trc` means "the scan ran" whatever the environment says; plus one NEW shell suite (three CONTROLs, two 🔴) in the shape of the KS-1136 suite.**

NOT in this task: KS-1274 (a bare `{}` reading as clean — a different guard, and its fix would change the `{}` stub both existing suites rely on); the `--quiet`/`--format`/`--severity`/`--vuln-type`/`--skip-db-update` flags (unchanged, `:88-:92`); the KS-1136 arm itself (`:114-:117`, `:125-:130`) — it stays exactly as it is and the new suite's third CONTROL proves it survives.

## WHY THE TEST STUBS trivy AND docker

The reference suite (KS-1136's) never runs docker or trivy: both are stubs on a private PATH, and the trivy stub reads a per-image mode from `$root/fail.txt`. This suite copies that shape and adds one mode, `findings`: the stub prints a report with 1 CRITICAL + 1 HIGH and then behaves as the real trivy was MEASURED to: `exit 0` when `--exit-code 0` is on its command line, else `exit "${TRIVY_EXIT_CODE:-0}"`. The environment variable reaches the job through `run_job`'s subshell (`export TRIVY_EXIT_CODE="$envcode"` when a second argument is given). So the 🔴 cells red at the tip for the ticket's reason — the job passed no `--exit-code`, the stub exited 1, the job called it scan-failed — and go green when the job passes `--exit-code 0`, with no daemon, no image and no network.

## Where

- `:92` — (correct) `    --skip-db-update \` — leading context. Stays. (It ends with a backslash: it is the line-continuation of the `trivy image` command. Copy it exactly.)
- `:93` — **CHANGES** `    "$img" 2>/dev/null)"; trc=$?` — this line is REMOVED (a `-` line) and replaced by the two `+` lines below. It is the ONLY line in the file with this text.
- `:94` — (correct) `  # KS-1136: trc is trivy's own exit code - a failed scan is no longer turned into an empty, clean-looking report.` — trailing context. Stays.
- `:95` — (correct) `  # extract just the high-signal subset` — trailing context. Stays.

## The exact change — ONE hunk in `Blockchain/Testing/jobs/04-container-trivy.sh`

One context line above, the one `-` line, your 2 `+` lines, two context lines below. **Every context line is copied byte for byte and none of them is blank.** The `+` lines are ASCII only (a plain `-` hyphen in the comment, never a dash character). The first `+` line is indented FOUR spaces (it is inside the `$( … )` of the `raw=` command, like the `-` line it replaces); the second `+` line is indented TWO spaces (it is a comment at the loop body's level, like `:94` below it).

```
@@ -92,4 +92,5 @@
     --skip-db-update \
-    "$img" 2>/dev/null)"; trc=$?
+    --exit-code 0 "$img" 2>/dev/null)"; trc=$?
+  # KS-1273: --exit-code 0 keeps trc meaning "the scan ran" - a TRIVY_EXIT_CODE (or a trivy.yaml exit-code) in the caller's environment would otherwise make findings read as a failed scan and drop them.
   # KS-1136: trc is trivy's own exit code - a failed scan is no longer turned into an empty, clean-looking report.
   # extract just the high-signal subset
```

Why this is correct, so you do not "improve" it:
- The first `+` line is the OLD `:93` with `--exit-code 0 ` (two dashes, the word, a space, a zero, a space) put in front of `"$img"`. Everything after it — `"$img" 2>/dev/null)"; trc=$?` — is byte for byte the old line. Trivy accepts `--exit-code` on `trivy image` (its `--help` lists `--exit-code int   specify exit code when any security issues are found`), and a flag before the positional image argument is how the other flags on `:88-:92` are already passed.
- Do NOT add a new `    --exit-code 0 \` continuation line instead: the checker holds you to the `+` lines above, stripped of leading whitespace, and a line that is not there is a dropped addition.
- Do NOT touch `:88-:92`, `:94-:95`, the KS-1136 guard at `:115` or the summary block at `:125-:133`.

## The test — CREATE THE NEW FILE

File: `Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh`

**Reference suite (READ-ONLY, do not modify, do not add it to your diff):** `Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh` (93 lines, the KS-1136 suite). This file copies its `set -uo pipefail`, `HERE=`/`REPO_ROOT=`/`JOB=` lines and the two `FATAL` guards, its `ok()`/`bad()` helpers with the `pass`/`fail` counters, its `mktemp -d` + `trap` cleanup, its `build_fixture` (the docker stub, the `sed "s#@ROOT@#$root#g"` trivy stub written from a quoted heredoc, the `fail.txt` mode file), its `run_job` subshell and its `art()` jq reader, and its last three lines. Three things are this suite's own: the trivy stub's `findings` mode (a two-vulnerability report, then `exit 0` if `--exit-code 0` is on its argv, else `exit "${TRIVY_EXIT_CODE:-0}"`); `run_job`'s optional second argument, exported as `TRIVY_EXIT_CODE` inside the subshell; and `row()`, which reads the one image's `error`, `counts.CRITICAL` and `counts.HIGH` in one string.

Write EXACTLY this file (114 lines) — three CONTROL cells, then two 🔴. It is bash 3.2: no `mapfile`, no `declare -A`, no `timeout`. Write the 🔴 with the literal 🔴 character.

```
#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Testing/jobs/04-container-trivy.sh - a TRIVY_EXIT_CODE in
# the caller's environment must not turn an image WITH findings into a failed
# scan (KS-1273)
# =============================================================================
# The defect: after KS-1136 the job keeps trivy's own exit code as "the scan
# ran". But trivy also exits non-zero when it FOUND something, if the caller's
# environment carries TRIVY_EXIT_CODE (or a trivy.yaml sets exit-code). With no
# --exit-code on its command line the job then recorded such an image as
# error: scan-failed, counts {} and vulns [] - the findings DROPPED - exited 1
# and said "could not scan" about an image it did scan. Measured on trivy
# 0.71.0: TRIVY_EXIT_CODE=1 plus findings exits 1; the same scan with
# --exit-code 0 on the command line exits 0 (the flag wins over the env).
#
# docker and trivy are NEVER run here (no stack, no daemon): both are STUBS on
# a private PATH, in the shape of container_trivy_failed_scan_is_loud.test.sh.
# The trivy stub reads $root/fail.txt ("<image> findings|empty" per line): a
# findings image prints a report with 1 CRITICAL + 1 HIGH and, like the real
# trivy, exits TRIVY_EXIT_CODE when that is set UNLESS --exit-code 0 is on its
# command line; an empty image exits 1 with no output; every other image gets
# `{}` and exits 0.
#
# Usage: bash Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh
# =============================================================================
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
JOB="$REPO_ROOT/Blockchain/Testing/jobs/04-container-trivy.sh"
[ -f "$JOB" ] || { echo "FATAL: 04-container-trivy.sh not found at $JOB" >&2; exit 2; }
command -v jq >/dev/null 2>&1 || { echo "FATAL: jq is not on PATH - the subject cannot run, so nothing here can be graded" >&2; exit 2; }

WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1273.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

pass=0; fail=0
ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }

# Build a fixture around the job under test.
#   $1 = dir   $2 = corpus text (what `docker images` prints)   $3 = mode list ("<image> findings|empty" lines)
build_fixture() {
  local root="$1" corpus="$2" modes="${3:-}"
  rm -rf "$root"; mkdir -p "$root/Testing/jobs" "$root/bin" "$root/run"
  cp "$JOB" "$root/Testing/jobs/04-container-trivy.sh"
  printf '%s\n' "$corpus" > "$root/images.txt"
  printf '%s\n' "$modes" > "$root/fail.txt"
  { printf '#!/bin/bash\n'
    printf 'case "${1:-}" in\n'
    printf '  info) exit 0 ;;\n'
    printf '  images) cat "%s/images.txt" ;;\n' "$root"
    printf 'esac\nexit 0\n'
  } > "$root/bin/docker"
  sed "s#@ROOT@#$root#g" > "$root/bin/trivy" <<'STUB'
#!/bin/bash
for last; do :; done
echo "$*" >> "@ROOT@/trivy_calls.txt"
mode="$(awk -v i="$last" '$1 == i { print $2 }' "@ROOT@/fail.txt")"
if [ "$mode" = empty ]; then exit 1; fi
if [ "$mode" = findings ]; then
  echo '{"Results":[{"Vulnerabilities":[{"VulnerabilityID":"CVE-2026-1273","PkgName":"openssl","InstalledVersion":"3.0.0","Severity":"CRITICAL"},{"VulnerabilityID":"CVE-2026-1274","PkgName":"zlib","InstalledVersion":"1.2.0","Severity":"HIGH"}]}]}'
  case " $* " in *" --exit-code 0 "*) exit 0 ;; esac
  exit "${TRIVY_EXIT_CODE:-0}"
fi
echo '{}'
STUB
  chmod +x "$root/bin/docker" "$root/bin/trivy"
}

# Run the job the way the orchestrator / audit runner do; when $2 is given the
# caller's environment carries it as TRIVY_EXIT_CODE. Prints rc.
run_job() {
  local root="$1" envcode="${2:-}"
  ( export PATH="$root/bin:/usr/bin:/bin" SELF="$root/Testing" RUN_DIR="$root/run"
    if [ -n "$envcode" ]; then export TRIVY_EXIT_CODE="$envcode"; fi
    cd "$SELF" && bash jobs/04-container-trivy.sh ) >"$root/out.txt" 2>&1
  echo $?
}
art() { jq -r "$2" "$1/run/04-container-trivy.json" 2>/dev/null || echo unparseable; }
# The ONE image's row: "<error or none> <CRITICAL count> <HIGH count>"
row() { echo "$(art "$1" '.images[0].error // "none"') $(art "$1" '.images[0].counts.CRITICAL // 0') $(art "$1" '.images[0].counts.HIGH // 0')"; }

# CONTROL - no TRIVY_EXIT_CODE: an image WITH findings is counted, no error, rc 0 (both trees).
build_fixture "$WORK/plain" 'dev-auth:latest' 'dev-auth:latest findings'
rc="$(run_job "$WORK/plain")"
got="$rc $(row "$WORK/plain")"
if [ "$got" = "0 none 1 1" ]; then ok "CONTROL - without TRIVY_EXIT_CODE an image with findings is counted: rc 0, no error, CRITICAL=1 HIGH=1"; else bad "CONTROL - without TRIVY_EXIT_CODE an image with findings is counted: rc 0, no error, CRITICAL=1 HIGH=1" "want 0 none 1 1, got $got"; fi

# CONTROL - TRIVY_EXIT_CODE=1 and an image with NO findings: clean, rc 0 (the gate's second row; both trees).
build_fixture "$WORK/cleanenv" 'dev-auth:latest'
rc="$(run_job "$WORK/cleanenv" 1)"
got="$rc $(row "$WORK/cleanenv")"
if [ "$got" = "0 none 0 0" ]; then ok "CONTROL - TRIVY_EXIT_CODE=1 with an image that has no findings stays clean: rc 0, no error"; else bad "CONTROL - TRIVY_EXIT_CODE=1 with an image that has no findings stays clean: rc 0, no error" "want 0 none 0 0, got $got"; fi

# CONTROL - KS-1136 survives: a trivy that exits 1 with NO output is still scan-failed, rc 1 (both trees).
build_fixture "$WORK/empty" 'dev-auth:latest' 'dev-auth:latest empty'
rc="$(run_job "$WORK/empty" 1)"
got="$rc $(row "$WORK/empty")"
if [ "$got" = "1 scan-failed 0 0" ]; then ok "CONTROL - a trivy that exits 1 with no output is still recorded as scan-failed and the job still exits 1"; else bad "CONTROL - a trivy that exits 1 with no output is still recorded as scan-failed and the job still exits 1" "want 1 scan-failed 0 0, got $got"; fi

# RED - KS-1273: TRIVY_EXIT_CODE=1 in the caller's environment and the ONLY image HAS findings.
build_fixture "$WORK/envcode" 'dev-auth:latest' 'dev-auth:latest findings'
rc="$(run_job "$WORK/envcode" 1)"
got="$rc $(row "$WORK/envcode")"
if [ "$got" = "0 none 1 1" ]; then ok "🔴 KS-1273 with TRIVY_EXIT_CODE=1 an image WITH findings keeps them: rc 0, no error, CRITICAL=1 HIGH=1"; else bad "🔴 KS-1273 with TRIVY_EXIT_CODE=1 an image WITH findings keeps them: rc 0, no error, CRITICAL=1 HIGH=1" "want 0 none 1 1, got $got (trivy argv: $(tr '\n' ';' < "$WORK/envcode/trivy_calls.txt" 2>/dev/null))"; fi

# RED - KS-1273: the same run prints the clean-run summary with the counts and never says "could not scan".
got="$(grep -c -F 'CRITICAL=1 HIGH=1 across 1 image(s)' "$WORK/envcode/out.txt") $(grep -c -F 'could not scan' "$WORK/envcode/out.txt")"
if [ "$got" = "1 0" ]; then ok "🔴 KS-1273 the same run prints CRITICAL=1 HIGH=1 across 1 image(s) and never says could not scan"; else bad "🔴 KS-1273 the same run prints CRITICAL=1 HIGH=1 across 1 image(s) and never says could not scan" "want 1 0, got $got, output: $(tr '\n' ' ' < "$WORK/envcode/out.txt")"; fi

printf '\n  %d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
exit 0
```

### READ THIS BEFORE YOU WRITE THE FILE

- The trivy stub is a QUOTED heredoc (`<<'STUB'`) piped through `sed "s#@ROOT@#$root#g"`, exactly as in the reference: `$last`, `$*`, `$1`, `$2` and `${TRIVY_EXIT_CODE:-0}` inside it are written into the stub LITERALLY and expand when the stub runs. Keep the quotes on `'STUB'`. Only `@ROOT@` is substituted.
- In the stub, `case " $* " in *" --exit-code 0 "*) exit 0 ;; esac` is what makes the flag win over the environment, as the real trivy does. Keep the spaces inside the quotes: they make `--exit-code 0` match as whole words.
- `run_job`'s second argument is OPTIONAL (`"${2:-}"`); the `if [ -n "$envcode" ]` export happens INSIDE the subshell, so a cell that passes `1` arms the environment for that job run only. Three cells pass `1`; the first passes nothing.
- The `echo` of the findings report is ONE line. Its JSON carries exactly two vulnerabilities, `CRITICAL` and `HIGH`, which is what the `CRITICAL=1 HIGH=1` expectations count.
- `row()`'s three `art` calls read `.images[0]` — every fixture in this suite has ONE image, so `[0]` is the image.
- `grep -c -F` prints its count even when it exits 1 on zero matches; the suite has no `set -e`, so a zero count is a value, not an abort.
- The suite's output goes to `$root/out.txt` and `$root/run/04-container-trivy.json` under `$WORK`, never to the suite's own stdout.

## THE RED-FIRST CELLS — state it to yourself before you write a line

**At the untouched tip, BOTH 🔴 cells FAIL, by assertion.** With `TRIVY_EXIT_CODE=1` exported and the one image in `findings` mode, the stub prints the two-vulnerability report and — seeing no `--exit-code 0` on the job's command line (`:87-:93` at the tip) — exits 1. The job's `:115` guard fires on `trc -ne 0`, the row becomes `error: "scan-failed"`, `counts: {}`, `vulns: []`, `:126` counts 1 failed, `:128` prints `-> FAILED: trivy could not scan 1 of 1 image(s) - a failed scan is not a clean image` and `:129` exits 1:
- `🔴 KS-1273 with TRIVY_EXIT_CODE=1 an image WITH findings keeps them …` reads `1 scan-failed 0 0` against `0 none 1 1`. After your hunk the stub sees `--exit-code 0` and exits 0; `trc` is 0, the jq at `:96` counts `CRITICAL: 1, HIGH: 1`, no error, the job exits 0 — GREEN.
- `🔴 KS-1273 the same run prints CRITICAL=1 HIGH=1 across 1 image(s) and never says could not scan` reads `0 1` against `1 0` (the `could not scan` line IS there at the tip, the summary is not). After your hunk `:133` prints `CRITICAL=1 HIGH=1 across 1 image(s)` and nothing says `could not scan` — GREEN. This cell blocks a "fix" that keeps the counts but still exits through the failed-scan branch.

The three CONTROLS are green on BOTH trees, and each blocks a way to pass by deleting behaviour:
- `CONTROL - without TRIVY_EXIT_CODE an image with findings is counted …` — the stub's report IS parsed to `CRITICAL=1 HIGH=1` when nothing sets an exit code, so the 🔴 red is the exit code alone, not the report's shape.
- `CONTROL - TRIVY_EXIT_CODE=1 with an image that has no findings stays clean …` — the batch gate's second row (`TRIVY_EXIT_CODE=1`, no findings → clean, rc 0 on both sides). Blocks a "fix" that reads every non-zero environment as a failure.
- `CONTROL - a trivy that exits 1 with no output is still recorded as scan-failed …` — KS-1136's arm must SURVIVE: `--exit-code 0` changes what trivy's rc MEANS, not the job's handling of a real failure. Blocks a "fix" that drops the `trc -ne 0` guard.

**MEASURED, not predicted** (drafter 05:50 AEST 2026-09-21, macOS `/bin/bash` 3.2.57, `jq` 1.6, a `git clone --shared` scratch clone detached at `362e51fe0`): this exact test at the tip → `3 passed, 2 failed`, rc 1, the two failures being the 🔴 cells (`want 0 none 1 1, got 1 scan-failed 0 0 (trivy argv: image --quiet --format json --severity CRITICAL,HIGH,MEDIUM --vuln-type os,library --skip-db-update dev-auth:latest;)` and `want 1 0, got 0 1, output: -> FAILED: trivy could not scan 1 of 1 image(s) - a failed scan is not a clean image`). This exact hunk applied with `git apply --check -p1` (strict, rc 0), `git apply --numstat` = `2 1 Blockchain/Testing/jobs/04-container-trivy.sh`, `bash -n` passed, the file went 133 → 134 lines, and the test → `5 passed, 0 failed`, rc 0. The two sibling suites that drive this job — `container_trivy_failed_scan_is_loud.test.sh` (3 passed, 0 failed) and `container_trivy_image_filter.test.sh` (4 passed, 0 failed) — read the same before and after: their stubs ignore trivy's argv and print `{}`, so `--exit-code 0` changes nothing they see.

## Red cells

- 🔴 KS-1273 with TRIVY_EXIT_CODE=1 an image WITH findings keeps them: rc 0, no error, CRITICAL=1 HIGH=1
- 🔴 KS-1273 the same run prints CRITICAL=1 HIGH=1 across 1 image(s) and never says could not scan

## Output

Exactly ONE ```diff block, nothing outside it, with TWO sections in this order:
1. `--- a/Blockchain/Testing/jobs/04-container-trivy.sh` / `+++ b/Blockchain/Testing/jobs/04-container-trivy.sh`, ONE hunk with the header exactly as shown: `@@ -92,4 +92,5 @@`.
2. `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh`, ONE hunk `@@ -0,0 +1,N @@` where N is the number of lines you emit (114 if you copy the file exactly; count them), every line a `+`.

## Premises (measured)

All times AEST 2026-09-21. Scratch clone `m_clone_1273` = `git clone --shared` of the Secuura checkout, `checkout --detach 362e51fe0`; every write verb ran in the scratch clone, restored by `git checkout --` and the new test PARKED (never deleted) — clone porcelain 0 after; source checkout tracked-modified 0 before and after (`runs/2026-09-21_round24-drafter-precheck/KS-1273/measure.log`).

- **P1 tip.** `ls-remote origin refs/heads/develop` = `362e51fe0db7e73d5557924902763fe3f10fd8c7` (05:38:29); `cat-file -t` = commit (local, no override). KS-1136's #1051 is merged — the tip's `:93-:94` and `:114-:130` ARE its result (`git log -1 -- Blockchain/Testing/jobs/04-container-trivy.sh`).
- **P2 the file at the tip.** `04-container-trivy.sh` sha256 `0720a4bfa4a4e8d3…`, 133 lines. `:93` occurs ONCE (`grep -c -F -x`: 1). `:92` / `:94` / `:95` each occur once (1 / 1 / 1), so the B3c stays-check matches each site exactly. The `-` line and both `+` lines are ASCII (the job's own `→` glyphs sit on other lines, none in the hunk).
- **P3 the real trivy's precedence, MEASURED** (`trivy` 0.71.0 at `/opt/homebrew/bin/trivy`; `trivy fs --scanners secret --quiet --format json --skip-version-check --offline-scan --cache-dir <scratch>` on a scratch directory holding three fake secrets — no image, no DB, no network; `scratchpad/trivyprec/measure.log`): A no env, no flag → rc 0, 3 secrets; **B `TRIVY_EXIT_CODE=1`, no flag → rc 1**, 3 secrets; **C `TRIVY_EXIT_CODE=1` + `--exit-code 0` → rc 0**, 3 secrets; D no env, `--exit-code 1` → rc 1 (the flag alone fires); E `TRIVY_EXIT_CODE=1` on a directory with no secret → rc 0. So the stub's `case " $* " in *" --exit-code 0 "*) exit 0` / `exit "${TRIVY_EXIT_CODE:-0}"` is the measured behaviour, not a guess. `trivy image --help` lists `--exit-code` (1 line).
- **P4 the knob is set nowhere in the repo.** `git grep -i -c TRIVY_EXIT_CODE <tip>`: 0 files (control `exit-code`: 10 files, including `.github/workflows/security-scan.yml`'s gitleaks `--exit-code 0`); `git ls-tree -r --name-only <tip> | grep -i -c trivy.yaml`: 0.
- **P5 the sibling suites (B6)** — every `*.test.sh` under `scripts/__tests__/` that names `04-container-trivy.sh`: `container_trivy_failed_scan_is_loud` and `container_trivy_image_filter`, run on BOTH trees in the scratch clone under `/bin/bash` 3.2: rc 0 both, `3 passed, 0 failed` and `4 passed, 0 failed`, identical before and after. Both stubs print `{}` regardless of argv (`failed_scan_is_loud.test.sh:57`, `image_filter.test.sh:76`).
- **P6 red and green, MEASURED** — see the red-first section (`KS-1273/tip_test.out`, `KS-1273/fix_test.out`).
- **P7 this brief through the real checker** — appended below after the golden run.

## Notes for the raise (not for the model)

- **Behaviour change:** in an environment with no `TRIVY_EXIT_CODE` and no `trivy.yaml` exit-code (every environment the repo defines today), trivy's rc for a scan with findings is already 0, so nothing moves: same artefact, same summary, same exit code in every case the two existing suites drive. With such a knob set, an image WITH findings is now counted instead of being recorded as `scan-failed` with its findings dropped. A real failed scan (non-zero rc with no/partial output) is handled exactly as KS-1136 left it.
- **Deviation from the ticket's letter, said plainly:** the ticket says "add a cell to `container_trivy_failed_scan_is_loud.test.sh`". This brief adds a NEW sibling suite instead, because the bash_patch tier's proven shape is `ONE script + ONE NEW *.test.sh` (20+ PASSes) while its modify-in-place shape has never passed (KS-1163: four FAILs at B3/B4/B5, 2026-09-16). The new suite copies the KS-1136 harness line for line and adds the `findings` mode; it pins the ticket's row exactly.
- **KS-1274 is NOT this diff and is not briefable in this tier at this tip:** any guard that turns a bare `{}` into `scan-failed` reds the clean stub in BOTH existing suites (`{}` is what they print for a clean image — `failed_scan_is_loud`'s CONTROL asserts `0 2 0` and `image_filter`'s CELL 1 asserts `rc=0`), so its fix needs the image_filter suite's stub changed too — a third file the checker refuses, and a file the held KS-1137-F2 READY already modifies.
- **Raise tier: TIER 2.** File-collision check owed at raise time (job 04 and the new test file — see the drafter report's collision section: no READY names `04-container-trivy.sh` as a `+++ b/` path except the merged KS-1136 item 1; the new test file name occurs in no READY). **Refs KS-1273; Closes** is the raiser's call — the ticket's fix shape is implemented in full (the flag) and its cell is pinned (as a new suite).

## Build line (not for the model)

```
bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/bash_patch/build_bash_input.sh KS-1273 /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/inputs/bash_1273EXITCODEENV-1.json /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-1273-EXITCODEENV-1.md product=Blockchain/Testing/jobs/04-container-trivy.sh ref=Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh
```
Queue with `task=/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/tasks/bash_patch/task.md` (NOT code_patch) and `ctx=49152`, as KS-1279 ran.

## MEASURED — appended after the golden run (artefacts `runs/2026-09-21_round24-drafter-precheck/KS-1273/`, `golden_runs.log`)

- Input built 05:53 AEST: `bash tasks/bash_patch/build_bash_input.sh … product=… ref=…` rc 0 — `sites 4 (1 must_change); expected '+' 2; must_remove 1; new test …container_trivy_exit_code_env_keeps_findings.test.sh` at `362e51fe0`; top-level AND `defect_line` key sets identical to `bash_1279.json` (the newest PASSING bash input) in both directions.
- Golden = the two fences above assembled verbatim by `KS-1273/assemble.py` (`out.md`, 118 `+` lines), through `tasks/bash_patch/checker.sh` on a FRESH `--shared` clone at `362e51fe0` (`gb_clone_1273_1`, 05:54:34-05:55:00): **RESULT: PASS (7/7)** — B2 strict both sections; B3 {script, the new test}; B3b 1/1 must_change + 2/2 `+` lines, no tip line re-added; B4 `rc=1 fail_lines=2 pass_lines=3 load_error=0`; B5a `bash -n` ok; B5 `rc=0 fail_lines=0 pass_lines=5`; B6 2 sibling suites, no NEW failure; B7 shellcheck not installed (informational). **Second fresh clone (`gb_clone_1273_2`): RESULT: PASS (7/7).** Source tracked-modified 0 before and after every run.
- Wrong variants REFUSED (fresh clone each): `test_only` (no script section) → **FAIL B3** (`n=1 product=0 test=1`); `wrong_flag` (`--exit-code 1` on the product line) → **FAIL B3b INCOMPLETE (A3c): brief '+' line ABSENT** (`--exit-code 0 "$img" …`); `dropped_comment` (the code `+` line without the KS-1273 comment, header `+92,4`) → **FAIL B3b INCOMPLETE (a dropped addition)**; `green_test` (the two 🔴 expectations swapped to the tip's answers) → **FAIL B4 RED-FIRST: the test is NOT red at the untouched tip (rc=0, 0 FAIL line(s))**.
- Collision, MEASURED: the only READY naming `04-container-trivy.sh` as a `+++ b/` path is the merged KS-1136 item 1 (its lines ARE the tip); the new test's basename occurs in 0 READY files; the held `KS-1137-F2-ESTATEIMAGE-1` READY (image_filter suite, `@@ -140,1 +140,20 @@`) shares no file with this diff — both apply orders on fresh clones (`collision_orders.log`) give ONE sha256 `ba7a4a360dce8949` over job + three suites, rc 0, and all three suites green after each (`3 passed` / `5 passed` / `5 passed`).
