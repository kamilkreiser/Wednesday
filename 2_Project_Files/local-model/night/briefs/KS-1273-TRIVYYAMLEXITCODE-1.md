# KS-1273 TRIVYYAMLEXITCODE-1 PIN THE TICKET'S SECOND ARM — A `trivy.yaml` WITH `exit-code: 1` IN THE JOB'S CWD, NO ENV VAR, AND AN IMAGE WITH FINDINGS IS STILL COUNTED (rc 0, no error, CRITICAL=1 HIGH=1) — the suite's trivy STUB learns to read `$PWD/trivy.yaml` the way it reads `TRIVY_EXIT_CODE`, `--exit-code 0` on argv still winning — Wednesday's task for Ornith, TEST_ONLY, **ONE existing bash suite, TWO hunks (one stub line replaced by two; one cell added), no product file** (written 2026-09-21 15:4x after the #1119-#1128 batch gate; its NOT-PINNED row TRIVYYAMLEXITCODE, #1122 / KS-1273, "a FIXTURE gap, kept")

File: `Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh`
Tip: `9f0265eb06ecf24d4de18149ce862ad2330a61ee`

Written from develop `9f0265eb06ecf24d4de18149ce862ad2330a61ee` (`git -C "/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files" ls-remote origin refs/heads/develop` at 15:30 on 2026-09-21, read verbs only; the tree `23d60cace7c3` that carries the ten #1119-#1128 squashes, #1122 = KS-1273 EXITCODEENV-1 included). The suite at that tip is **114 lines** (blob `d119e64ba755`), read whole; its full content is in `files[...]` of your input. The product the cells pin is `Blockchain/Testing/jobs/04-container-trivy.sh` (blob `6dfc5731e56e`, **134 lines**): `cd "$SELF"` at `:16` (the job runs from the Testing directory), the `trivy image` command `:87-:93` ending on **`:93`** `    --exit-code 0 "$img" 2>/dev/null)"; trc=$?` and the KS-1273 comment on **`:94`** (the #1122 hunk — the two lines the tamper below reverts), the KS-1136 guard `:115-:118` (`trc -ne 0` → `error: "scan-failed"`, counts `{}`, findings dropped). Runner: **bash** (a `*.test.sh` suite, run by the checker as `/bin/bash <file>` from the clone root, bash 3.2.57; no node, no farm).

## THE MODE — read this twice

**TEST_ONLY.** Your diff touches EXACTLY ONE file: the suite above, MODIFIED IN PLACE (`--- a/<path>` / `+++ b/<path>`, the path exactly as written above), in TWO hunks. You never touch `04-container-trivy.sh` or any other file: the job already passes `--exit-code 0` at the tip, and the new cell PINS that the flag also covers the `trivy.yaml` arm the ticket named.

## What the cell pins (one paragraph)

KS-1273 named TWO ways a caller's environment arms trivy's exit code — `TRIVY_EXIT_CODE` exported, or `exit-code:` in a `trivy.yaml` in the working directory — and #1122 fixed both with one flag (`--exit-code 0` on `:93`), because on the real trivy the flag wins over both. But the suite #1122 added exercises ONLY the env arm: its trivy stub (`:55-:67`, a quoted heredoc) exits `${TRIVY_EXIT_CODE:-0}` and reads no file, so no cell feeds a `trivy.yaml`, and a future job that dropped the flag while (say) clearing `TRIVY_EXIT_CODE` itself would keep this suite green and still fail on a runner whose cwd carries a `trivy.yaml`. The gate (#1119-#1128, row TRIVYYAMLEXITCODE) measured the real trivy 0.71.0 offline: `./trivy.yaml` `exit-code: 1` → rc 1 bare, rc 0 with `--exit-code 0`. This change (1) teaches the stub to read `$PWD/trivy.yaml`'s `exit-code:` value — `cfg` via one `awk` line — and to exit `${TRIVY_EXIT_CODE:-${cfg:-0}}` (env over config, then the default; `--exit-code 0` on argv still wins through the `case` on `:63`, untouched), and (2) adds ONE cell that builds a findings fixture, writes `exit-code: 1` into `$WORK/yamlcode/Testing/trivy.yaml` (the job's cwd — `run_job` does `cd "$SELF"` and the job itself `cd "$SELF"` again), runs the job with NO env var, and asserts `0 none 1 1` — rc 0, no error, CRITICAL=1, HIGH=1. **It pins TODAY's flag for the arm the ticket named second**: with `:93`'s `--exit-code 0` gone (develop's job as it was at `7be81d5c9`, before #1122), the stub exits 1 on the config, the job records `scan-failed` and drops both findings, and the cell reds beside the two existing red cells.

**Precedence, said plainly (a deviation from the gate row's letter):** the gate's row wrote the stub's exit as `exit "${cfg:-${TRIVY_EXIT_CODE:-0}}"` (config over env). Measured by the writing seat on the real trivy 0.71.0 (offline secret scan, `runs/2026-09-21_gate1119rows-drafter-precheck/TRIVYYAMLEXITCODE/trivy_precedence.log`): `trivy.yaml` `exit-code: 1` + `TRIVY_EXIT_CODE=0` → **rc 0** (env wins), `exit-code: 0` + `TRIVY_EXIT_CODE=1` → **rc 1** (env wins again), `exit-code: 1` + `--exit-code 0` → rc 0 (flag wins), `exit-code: 1` alone → rc 1, nothing set → rc 0. So the stub exits `${TRIVY_EXIT_CODE:-${cfg:-0}}` — the real precedence, flag > env > config. The new cell sets no env, so either order reds and greens the same; the order is chosen to keep the stub honest for any later cell that sets both.

## The exact change — TWO hunks in the suite

**Hunk 1 (the stub, inside the quoted heredoc `:55-:67`):** ONE `-` line, TWO `+` lines, with ONE leading context line (`:63`, the `case` that makes `--exit-code 0` win — unique in the file) and TWO trailing (`:65` `fi`, `:66` `echo '{}'`). Both `+` lines are indented TWO spaces like the `-` line they replace (they sit inside the `if [ "$mode" = findings ]` block). The heredoc is QUOTED (`<<'STUB'`), so `$1`, `$2`, `$PWD`, `${TRIVY_EXIT_CODE…}` and `${cfg…}` are written LITERALLY and expand when the stub runs — exactly as the `-` line's `${TRIVY_EXIT_CODE:-0}` already does. `awk '$1 == "exit-code:" { print $2 }' "$PWD/trivy.yaml" 2>/dev/null` prints the value after `exit-code:` when the file exists in the job's cwd and nothing (stderr discarded) when it does not, so `cfg` is empty in every fixture that writes no `trivy.yaml` — the five existing cells see the stub behave exactly as before.

**Hunk 2 (the new cell):** SIX `+` lines inserted directly ABOVE the tally line `:112` (`printf '\n  %d passed, %d failed\n' "$pass" "$fail"`), with the three closing lines `:112-:114` as trailing context and NO leading context (the line above, `:111`, is blank and a blank line is never in a fence). The cell copies the shape of the first red cell `:102-:106` (comment, `build_fixture`, `rc=`, `got=`, one `if … ok … else bad … fi` line), adds the ONE `echo` that writes the config file, and passes NO second argument to `run_job` (no `TRIVY_EXIT_CODE`). The `bad` detail prints the stub's recorded argv with `cat` (one image, one call, one line).

Copy every line byte for byte. Every `+` line is ASCII only (the title says `RED`, never the red glyph; a plain `-` in the comment), carries NO backslash (the diagnostic uses `cat`, not `tr`), and no backtick. There is no blank line anywhere in either fence. Keep both headers exactly as shown. **Your diff MUST begin with the two file-header lines, above the first `@@` line: `--- a/Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh` then `+++ b/Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh`.**

```
@@ -63,4 +63,5 @@
   case " $* " in *" --exit-code 0 "*) exit 0 ;; esac
-  exit "${TRIVY_EXIT_CODE:-0}"
+  cfg="$(awk '$1 == "exit-code:" { print $2 }' "$PWD/trivy.yaml" 2>/dev/null)"
+  exit "${TRIVY_EXIT_CODE:-${cfg:-0}}"
 fi
 echo '{}'
```

```
@@ -112,3 +112,9 @@
+# RED - KS-1273, the ticket's second arm: a trivy.yaml with exit-code: 1 in the job's cwd (the job runs from $SELF) and NO env var; the ONLY image HAS findings.
+build_fixture "$WORK/yamlcode" 'dev-auth:latest' 'dev-auth:latest findings'
+echo 'exit-code: 1' > "$WORK/yamlcode/Testing/trivy.yaml"
+rc="$(run_job "$WORK/yamlcode")"
+got="$rc $(row "$WORK/yamlcode")"
+if [ "$got" = "0 none 1 1" ]; then ok "RED KS-1273 a trivy.yaml exit-code: 1 in the job's cwd keeps findings: rc 0, no error, CRITICAL=1 HIGH=1"; else bad "RED KS-1273 a trivy.yaml exit-code: 1 in the job's cwd keeps findings: rc 0, no error, CRITICAL=1 HIGH=1" "want 0 none 1 1, got $got (trivy argv: $(cat "$WORK/yamlcode/trivy_calls.txt" 2>/dev/null))"; fi
 printf '\n  %d passed, %d failed\n' "$pass" "$fail"
 [ "$fail" -eq 0 ] || exit 1
 exit 0
```

`build_fixture` (`:43-:69`) makes `$root/Testing/jobs` before anything else (`:45`), so `$WORK/yamlcode/Testing/trivy.yaml` has a directory to land in; `run_job` (`:73-:79`) exports the private PATH, `SELF="$root/Testing"`, `RUN_DIR`, then `cd "$SELF" && bash jobs/04-container-trivy.sh` — the job's cwd, and so the stub's `$PWD`, is `$WORK/yamlcode/Testing`, where the file is. `row()` (`:82`) reads the one image's `error`, `counts.CRITICAL`, `counts.HIGH`. You add NO helper, NO variable at file scope, NO change to `build_fixture`'s docker stub, to `run_job` or to any existing cell. Nothing listens, nothing is fetched, no docker, no real trivy: both are the suite's stubs on a private PATH.

## Cells

- `yamlcode` = `RED KS-1273 a trivy.yaml exit-code: 1 in the job's cwd keeps findings: rc 0, no error, CRITICAL=1 HIGH=1`
- `envcode` = `🔴 KS-1273 with TRIVY_EXIT_CODE=1 an image WITH findings keeps them: rc 0, no error, CRITICAL=1 HIGH=1`
- `summary` = `🔴 KS-1273 the same run prints CRITICAL=1 HIGH=1 across 1 image(s) and never says could not scan`

## Red cells

The new cell below is a GENUINE assertion-red: it fails under the tamper declared for it and passes at the tip. It is declared here rather than with a red glyph in its title because every `+` line in this diff must be ASCII only (the suite's two existing red cells carry the glyph and are declared under the same tamper).

- RED KS-1273 a trivy.yaml exit-code: 1 in the job's cwd keeps findings: rc 0, no error, CRITICAL=1 HIGH=1

## Tampers

One BLOCK tamper on the job, `04-container-trivy.sh:93-:94`: the #1122 hunk reverted — `From` is the tip's `:93` (the `"$img"` line WITH `--exit-code 0`) followed by `:94` (the KS-1273 comment), `To` is the single pre-#1122 `"$img"` line. The two-line From block occurs EXACTLY ONCE in the file (python whole-line scan over the tip file: 1 hit at 93; the first line alone also 1). The tampered file is byte-for-byte develop's job at `7be81d5c9` (blob `88444463f9d4`, measured by `git hash-object` after planting — the gate's "red fixture"). It parses (`bash -n` rc 0 — it ran as develop's job for three days). The checker plants it as whole lines and restores the file by bytes.

### EXITCODEFLAGGONE — the job's `--exit-code 0` (and its KS-1273 comment) removed: develop's job as it was before #1122
File: `Blockchain/Testing/jobs/04-container-trivy.sh`
Line: 93
From:
```
    --exit-code 0 "$img" 2>/dev/null)"; trc=$?
  # KS-1273: --exit-code 0 keeps trc meaning "the scan ran" - a TRIVY_EXIT_CODE (or a trivy.yaml exit-code) in the caller's environment would otherwise make findings read as a failed scan and drop them.
```
To:
```
    "$img" 2>/dev/null)"; trc=$?
```
Reds: `yamlcode`, `envcode`, `summary`

## Controls

- `CONTROL - without TRIVY_EXIT_CODE an image with findings is counted: rc 0, no error, CRITICAL=1 HIGH=1`
- `CONTROL - TRIVY_EXIT_CODE=1 with an image that has no findings stays clean: rc 0, no error`
- `CONTROL - a trivy that exits 1 with no output is still recorded as scan-failed and the job still exits 1`

*(All three are the FULL descriptions the suite prints on its `ok` lines, copied from `:88`, `:94`, `:100` at the tip — unchanged by this diff. For a BASH suite the checker matches a declared cell by a literal PREFIX of the printed description; no declared name is a prefix of another. Under EXITCODEFLAGGONE the three stay green (measured): the first sets no exit code anywhere, so the stub exits 0 flag or no flag; the second has no findings, so the stub prints `{}` and exits 0 before any exit-code logic; the third's `empty` mode exits 1 with no output on both trees — KS-1136's arm, which the flag never touched.)*

## THE CELL — state it to yourself before you write a line

At the untouched tip the new cell passes: `run_job` starts the job from `$WORK/yamlcode/Testing`; the job's `trivy image … --skip-db-update --exit-code 0 dev-auth:latest` reaches the stub, whose `awk` reads `exit-code: 1` from `$PWD/trivy.yaml` into `cfg` — but the `case " $* "` on `:63` sees `--exit-code 0` on argv and exits 0 first; `trc` is 0, the job's `jq` counts `CRITICAL: 1, HIGH: 1`, no error, rc 0 → `0 none 1 1` (measured: `6 passed, 0 failed`, rc 0). Under **EXITCODEFLAGGONE** the job's command line carries no `--exit-code`, the `case` does not match, `TRIVY_EXIT_CODE` is unset, so the stub exits `cfg` = 1; the job's `:115` guard fires, the row becomes `error: "scan-failed"`, counts `{}`, and the job exits 1 → `1 scan-failed 0 0` against `0 none 1 1` — an assertion red on `yamlcode`, printed with the recorded argv (`image --quiet --format json --severity CRITICAL,HIGH,MEDIUM --vuln-type os,library --skip-db-update dev-auth:latest` — no `--exit-code`). The same tamper reds the suite's two existing red cells `envcode` and `summary` for the reason #1122 fixed (the env arm), so the declared red set is exactly those three (measured: `3 passed, 3 failed`, rc 1). The three controls stay green.

## Premises (measured — by reading the tip, NOT by running anything, except where the MEASURED section below says so)

- **Premise: the From block.** `04-container-trivy.sh` at `9f0265eb0`, `:93` is `    --exit-code 0 "$img" 2>/dev/null)"; trc=$?` (4-space indent, inside the `raw="$(trivy image …)"` command) and `:94` is the KS-1273 comment (2-space indent); as a two-line block they occur **once**. `To` is `7be81d5c9`'s `:93` byte for byte (that job is 133 lines; the tip's is 134).
- **Premise: the gate's claim, re-derived.** `grep -c -F 'trivy.yaml'` over the suite at the tip = **1** hit, in the header comment (`:9`; positive control `TRIVY_EXIT_CODE`: 13 lines); no cell writes one; the stub (`:55-:67`) reads only `fail.txt` and `TRIVY_EXIT_CODE`. Agreed: the config arm is unexercised.
- **Premise: the anchors.** `:63`, `:64`, `:65`, `:66` are each `grep -c -F -x` **1** in the suite; `:112`, `:113`, `:114` likewise **1** each. `:111` is blank and is NOT in any fence — hunk 2 has no leading context on purpose (74 earlier briefs use this shape; the merged KS-1198-SKMETA-1 is one).
- **Premise: `+` lines that also occur at the tip.** None: no `+` line of either hunk is byte-identical to any tip line (python: 0 of 8), and no `+` line equals the `-` line.
- **No backslash** in any `+` line (0, counted). **No non-ASCII** in any `+` line (0, counted). **No backtick** (0). Longest `+` line 359 bytes (the `if … ok … else bad … fi` line; the suite's own `:106` is 400 bytes and was produced by this model in #1122's run).
- **Premise: the runner.** A `*.test.sh` File selects runner bash; the builder refuses a `Runner:` line for it, so none is written. The suite after the fence parses (`bash -n` rc 0, measured) and uses no bash-4 idiom.
- **Premise: the surface.** Stubs on a private PATH under `mktemp -d`; no docker, no trivy, no network, no port. A CI job's test suite, not an HTTP surface.

## Collision

`/usr/bin/grep -il 'container_trivy_exit_code_env_keeps_findings' night/READY_*.md` = **1** of 259 (KS-1273-EXITCODEENV-1 — MERGED as #1122; its lines ARE the tip). `04-container-trivy.sh` is named in **3** READYs, `+++ b/` in 2 (KS-1136 item 1, merged #1051; KS-1273-EXITCODEENV-1, merged #1122). The held KS-1137-F2-ESTATEIMAGE-1 (image_filter suite) is ALSO merged at this tip (the sibling now reads `5 passed`). No brief of this round touches these two files (row 1 is the security service; row 3 is `systemTest/`). Sequencing needed: none.

## MEASURED by the writing seat (2026-09-21 15:3x-15:4x, `--shared` scratch clone `m_main` at `9f0265eb0`, bash runner — no node farm; source tracked-modified count 0 before and after; artefacts under `2_Project_Files/local-model/runs/2026-09-21_gate1119rows-drafter-precheck/TRIVYYAMLEXITCODE/`)

- `bare_bash.sh` → `tip_suite.out`: the suite at the bare tip **5 passed, 0 failed**, rc 0.
- `measure_trivy.sh` → `measure.log`: `git apply --check` rc 0, `git apply` rc 0, numstat `8 1`; `bash -n` rc 0; 114 → 121 lines. With the hunks, no tamper: **6 passed, 0 failed**, rc 0 (`applied_suite.out`). EXITCODEFLAGGONE planted by the two-line block (1 occurrence): the job's blob = `88444463f9d42a3ee4ad8f8b5ca24123ae678fb6` = `7be81d5c9:Blockchain/Testing/jobs/04-container-trivy.sh` (equal); the suite **3 passed, 3 failed**, rc 1 — the reds `envcode`, `summary`, `yamlcode` (`want 0 none 1 1, got 1 scan-failed 0 0 (trivy argv: image --quiet … --skip-db-update dev-auth:latest)`), the three controls green (`under_EXITCODEFLAGGONE.out`). Restored by checkout: job blob `6dfc5731e56e` == tip. Sibling suites with the hunks applied: `container_trivy_failed_scan_is_loud` **3 passed, 0 failed**, `container_trivy_image_filter` **5 passed, 0 failed** (rc 0 both). Clone porcelain 0 after.
- `trivy_precedence.sh` → `trivy_precedence.log` (real trivy 0.71.0, offline `fs --scanners secret` on a scratch dir holding a private-key block and two tokens, 3 secrets found every time): A nothing → rc 0; B config 1 → rc 1; C config 1 + env 0 → rc 0; D config 1 + `--exit-code 0` → rc 0; E config 0 + env 1 → rc 1; F env 1 → rc 1.
- **Golden and variants:** see the drafter report (`runs/2026-09-21_gate1119rows-drafter-precheck/REPORT.md`, Row 2) — `golden_runs.log`.

## Output

Exactly ONE ```diff block, nothing outside it: `--- a/Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh` / `+++ b/Blockchain/Dev/scripts/__tests__/container_trivy_exit_code_env_keeps_findings.test.sh`, then the two hunks above exactly as shown, in this order (`@@ -63,4 +63,5 @@` then `@@ -112,3 +112,9 @@`).

## Notes for the raise (not for the model)

- Test-only, zero product bytes. **Raise tier: TIER 2 (a CI job's shell suite, no service, no runtime image). Refs KS-1273.** **NEVER Closes** — whether the ticket is complete is Wednesday's ruling (the gate's TICKETCOMPLETEBYDESIGN row); this cell pins the second arm the ticket named.
- **From the #1119-#1128 batch gate's NOT-PINNED table** (`Testing Agent MAIN/projects/secuura/reports/2026-09-21-batch1119-1128-tier1-r1/report.md`, row TRIVYYAMLEXITCODE, "a FIXTURE gap, kept … Polish"). The gate's proposed cell title is used with a `RED` prefix (ASCII); the stub's precedence is env-over-config (measured), not the row's config-over-env.
- **Not touched, said plainly:** the suite's header comment (`:18-:22`) still describes the stub as reading `TRIVY_EXIT_CODE` only — a one-line prose update the raiser may add by hand (kept out of the model's diff to hold it at two hunks).

## Build line (not for the model)

```
bash tasks/test_only/build_test_only_input.sh KS-1273 night/inputs/test_only_1273TRIVYYAMLEXITCODE-1.json night/briefs/KS-1273-TRIVYYAMLEXITCODE-1.md tip=9f0265eb06ecf24d4de18149ce862ad2330a61ee ctx=65536
```
