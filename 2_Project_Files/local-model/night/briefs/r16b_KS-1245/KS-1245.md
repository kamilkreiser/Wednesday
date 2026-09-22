# KS-1245 R16B-DEGRADEDWARN - bash_patch at develop 3bad652d1: `scripts/smoke-test.sh` passes a `degraded` /health/deep service WITH a warning that names it; `down`/`error` still fail (Kam's ruling 2026-09-22 18:11, card `secuura-ks1245-smoke-test-degraded-semantics` option a; written 2026-09-22 18:57:07 AEST by Wednesday's feed16 drafter; every context line below is read from the tip file, never typed)

File: `Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh`
Tip: 3bad652d17cf111c1e2e1bed1ae7686894637487
Runner: bash (the shell suite runner - `bash <file>` under /bin/bash 3.2; the checker runs the suite alone at the tip, then again after the script hunk)

## What is wrong (one paragraph)
Since #1037 (KS-1101) the gateway's `/health/deep` reports a soft-down dependency as `degraded` instead of `up`. `scripts/smoke-test.sh` reads that aggregator in section 1 and its branch at `:107` treats ANYTHING that is not `up` as a failure, so a degraded service reds the whole smoke test (the gate measured 5 pass / 0 fail becoming 4 pass / 1 fail). Kam ruled (2026-09-22 18:11, option a): **`degraded` is a PASS WITH A WARNING that names the service; `down` / `error` (anything else) still fail.** The change is ONE `elif` arm between the `up` branch and the `else` branch: it calls the script's existing `pass` helper (so the service counts in `PASS`) and its existing `warn` helper (so `WARN` counts it and the `!` line names the service and its status). Nothing else in the script changes: the `up` arm, the `else`/`fail` arm, the python parser, the counters and the RESULTS block are untouched. NOT in this task: `/health/deep` itself, the api-gateway, any other section of the smoke test.

## The exact change - 1 hunk(s) in `Blockchain/Dev/scripts/smoke-test.sh` (0 '-' line(s), 6 '+' line(s), one '+' group per hunk)
Copy the block below BYTE FOR BYTE as the first file of your diff: the two file-header lines, the `@@` header, every context line (a leading space, copied from `files[product_file]`), and every `+` line, in this order. Do not add, drop, re-indent or reword a line; do not add a trailing comment; do not mark a context line as `+`. Every `+` line is ASCII - a double quote or a dollar sign on a `+` line is copied as written, never escaped; there is no backslash on any `+` line.
```
--- a/Blockchain/Dev/scripts/smoke-test.sh
+++ b/Blockchain/Dev/scripts/smoke-test.sh
@@ -106,4 +106,10 @@
     [ -z "$svc" ] && continue
     if [ "$status" = "up" ]; then
       pass "$svc (latency ${latency}ms)"
+    elif [ "$status" = "degraded" ]; then
+      # KS-1245 (Kam 2026-09-22, option a): since #1037 /health/deep reports a
+      # soft-down dependency as 'degraded'. That is a PASS WITH A WARNING that
+      # names the service; only 'down' / 'error' (anything else) still fail.
+      pass "$svc (latency ${latency}ms) - DEGRADED"
+      warn "$svc - status=degraded (KS-1245: passes with this warning; down/error still fail)"
     else
```

## Where (parsed into the checklist - every **must change** line must appear as a `-` line in your diff; there is none here, the change is an insertion)

* `:107` - (correct) `    if [ "$status" = "up" ]; then` - stays (the `up` arm)
* `:108` - (correct) `      pass "$svc (latency ${latency}ms)"` - stays (the `up` arm's pass line; the new `elif` arm goes directly below it)
* `:109` - (correct) `    else` - stays (the `else` arm; its `fail` line at `:110` is the down/error path and is untouched)

## The test - CREATE THE NEW FILE `Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh`

File: `Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh`

bash 3.2. It lives under `Blockchain/Dev/scripts/__tests__/` beside the reference `Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh` (full content in `files[...]`) and copies its shape: a private PATH with a STUB in front of the real command (the reference stubs `docker` and `trivy`; this suite stubs `curl`, so the smoke test never reaches a network), `mktemp -d` + `trap`, `ok`/`bad` counters, the totals line and `exit 1` on any failure. It locates the subject from `${BASH_SOURCE[0]}` exactly as the block below does. It creates nothing outside `mktemp -d` and never edits the repo's real files. The stub `curl` answers `/health/deep` with the fixture's JSON body and answers every `-w "%{http_code}"` probe (sections 2 and 3 of the smoke test) with `200`, so under `--quick` the ONLY thing that can fail is section 1.

**Reproduce the file below EXACTLY as written - every line, in order (81 lines).** Do not invent a helper, do not rename a variable, do not reword a message, do not add or drop a cell. **Your diff for this file is a NEW-FILE diff: `--- /dev/null`, `+++ b/Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh`, ONE hunk header `@@ -0,0 +1,81 @@`, then EVERY line with a leading `+` (a blank line is a lone `+`) - no context lines, no `-` lines: you are not diffing the reference.**

```
#!/usr/bin/env bash
# =============================================================================
# TESTS for Blockchain/Dev/scripts/smoke-test.sh - a 'degraded' /health/deep
# service passes WITH a warning that names it; 'down'/'error' still fail
# (KS-1245, Kam's ruling 2026-09-22 option a)
# =============================================================================
# curl is NEVER run here (no stack, no network): it is a STUB on a private
# PATH, in the shape of container_trivy_failed_scan_is_loud.test.sh. The stub
# answers /health/deep with the fixture's JSON and every http_code probe with
# 200, so under --quick only section 1 of the smoke test can fail.
#
# Usage: bash Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh
# =============================================================================
set -uo pipefail

HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
SMOKE="$REPO_ROOT/Blockchain/Dev/scripts/smoke-test.sh"
[ -f "$SMOKE" ] || { echo "FATAL: smoke-test.sh not found at $SMOKE" >&2; exit 2; }

WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1245.XXXXXX")"
trap 'rm -rf "$WORK"' EXIT

pass=0; fail=0
ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }

# A /health/deep body with the five services at the given statuses.
deep_body() {
  printf '{"ready":true,"status":"x","checks":{"redis":{"status":"%s","latencyMs":1},"postgres":{"status":"%s","latencyMs":2},"auth":{"status":"%s","latencyMs":3},"originate":{"status":"%s","latencyMs":4},"anchoring":{"status":"%s","latencyMs":5}}}' "$1" "$2" "$3" "$4" "$5"
}

# Build a fixture: $1 = dir, $2 = the /health/deep body the stub curl returns.
build_fixture() {
  local root="$1" deep="$2"
  rm -rf "$root"; mkdir -p "$root/bin"
  printf '%s' "$deep" > "$root/deep.json"
  sed "s#@ROOT@#$root#g" > "$root/bin/curl" <<'STUB'
#!/bin/bash
for a in "$@"; do
  case "$a" in */health/deep) cat "@ROOT@/deep.json"; exit 0 ;; esac
done
for a in "$@"; do [ "$a" = "-w" ] && { printf '200'; exit 0; }; done
exit 0
STUB
  chmod +x "$root/bin/curl"
}

# Run the smoke test in --quick mode with the stub curl first on PATH. Prints rc.
run_smoke() {
  local root="$1"
  ( export PATH="$root/bin:$PATH"; bash "$SMOKE" --quick ) > "$root/out.txt" 2>&1
  echo $?
}
count() { grep -c -F "$2" "$1/out.txt"; }

# CONTROL - every service 'up': rc 0, no failure, no warning.
build_fixture "$WORK/allup" "$(deep_body up up up up up)"
got="$(run_smoke "$WORK/allup") $(count "$WORK/allup" 'Failed: 0') $(count "$WORK/allup" 'Warnings: 0')"
if [ "$got" = "0 1 1" ]; then ok "CONTROL - five services up: rc 0, Failed: 0, Warnings: 0"; else bad "CONTROL - five services up: rc 0, Failed: 0, Warnings: 0" "want 0 1 1, got $got"; fi

# RED - auth 'degraded', the rest up: the run passes (rc 0) with ONE warning that names auth and its status.
build_fixture "$WORK/degraded" "$(deep_body up up degraded up up)"
got="$(run_smoke "$WORK/degraded") $(count "$WORK/degraded" 'Warnings: 1') $(count "$WORK/degraded" 'auth - status=degraded')"
if [ "$got" = "0 1 1" ]; then ok "RED a degraded service passes the smoke test with one warning naming the service and its status"; else bad "RED a degraded service passes the smoke test with one warning naming the service and its status" "want 0 1 1, got $got"; fi
got="$(count "$WORK/degraded" 'Passed: 13') $(count "$WORK/degraded" 'Failed: 0')"
if [ "$got" = "1 1" ]; then ok "RED the degraded service is COUNTED as passed (Passed: 13, Failed: 0), not as a failure"; else bad "RED the degraded service is COUNTED as passed (Passed: 13, Failed: 0), not as a failure" "want 1 1, got $got"; fi

# CONTROL - postgres 'down': still a failure (rc 1) naming the service and status, on both trees.
build_fixture "$WORK/down" "$(deep_body up down up up up)"
got="$(run_smoke "$WORK/down") $(count "$WORK/down" 'Failed: 1') $(count "$WORK/down" 'status=down')"
if [ "$got" = "1 1 2" ]; then ok "CONTROL - a down service still fails the smoke test (rc 1, Failed: 1, postgres named twice: the line and the FAILURES list)"; else bad "CONTROL - a down service still fails the smoke test (rc 1, Failed: 1, postgres named twice: the line and the FAILURES list)" "want 1 1 2, got $got"; fi

# CONTROL - anchoring 'error': still a failure, on both trees.
build_fixture "$WORK/error" "$(deep_body up up up up error)"
got="$(run_smoke "$WORK/error") $(count "$WORK/error" 'Failed: 1') $(count "$WORK/error" 'status=error')"
if [ "$got" = "1 1 2" ]; then ok "CONTROL - an error service still fails the smoke test (rc 1, Failed: 1)"; else bad "CONTROL - an error service still fails the smoke test (rc 1, Failed: 1)" "want 1 1 2, got $got"; fi

printf '\n  %d passed, %d failed\n' "$pass" "$fail"
[ "$fail" -eq 0 ] || exit 1
exit 0
```

Cells, in file order (a RED cell FAILS at the untouched tip by assertion and PASSES after the script hunk; a CONTROL cell passes on both trees):
- `ok "CONTROL - five services up: rc 0, Failed: 0, Warnings: 0"`
- `ok "RED a degraded service passes the smoke test with one warning naming the service and its status"` - at the tip: rc 1, `Warnings: 0`, no such line (`want 0 1 1, got 1 0 0`)
- `ok "RED the degraded service is COUNTED as passed (Passed: 13, Failed: 0), not as a failure"` - at the tip: `Passed: 12` / `Failed: 1` (`want 1 1, got 0 0`)
- `ok "CONTROL - a down service still fails the smoke test (rc 1, Failed: 1, postgres named twice: the line and the FAILURES list)"`
- `ok "CONTROL - an error service still fails the smoke test (rc 1, Failed: 1)"`

## Output
Exactly ONE ```diff block with TWO files: `--- a/Blockchain/Dev/scripts/smoke-test.sh` / `+++ b/Blockchain/Dev/scripts/smoke-test.sh` (1 hunk, copied from `## The exact change`), then `--- /dev/null` / `+++ b/Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh` (one hunk, `@@ -0,0 +1,81 @@`, every line a `+`). No prose before or after the block.

## Premises (measured at develop 3bad652d17cf111c1e2e1bed1ae7686894637487 by the feed16 drafter in a `git clone --shared` scratchpad clone, 2026-09-22 18:57:07 AEST)
- `Blockchain/Dev/scripts/smoke-test.sh` at the tip carries every context line of the hunk above BYTE FOR BYTE at `:106-:109` (generated from `git show 3bad652d1:Blockchain/Dev/scripts/smoke-test.sh` by the writer script, never typed); the product section applies STRICT (`git apply --check -p1` rc 0 in the clone). The file is 395 lines; `--quick` runs sections 1-3 only (`:88-:139`) and every network call in them is a `curl` the stub answers.
- The defect REPRODUCED in-process at the untouched tip with the same stub curl: a body whose `auth` is `degraded` prints `auth — status=degraded` under `✗`, `Passed: 12  Failed: 1`, rc 1 (`runs/2026-09-22_feed16-drafter-precheck/probe_tip_degraded.out`).
- The new suite `Blockchain/Dev/scripts/__tests__/smoke_test_degraded_warns.test.sh` is ABSENT at the tip (`git cat-file -e` rc 1). The reference suite `Blockchain/Dev/scripts/__tests__/container_trivy_failed_scan_is_loud.test.sh` is present (93 lines) and is the PATH-stub exemplar this suite copies.
- Every `+` line of the product hunk and every line of the suite is ASCII (non-ASCII 0, asserted by the writer; the cell glyph is the word RED); no backslash and no backtick on any `+` line (0 / 0, asserted). The FEED 8 ruling WAIVES the `"` 0 rule for bash_patch - the guard is the checker's B3b (every brief `+` line present in the script hunk) and B4/B5 (RED at the tip, GREEN after).
- No sibling suite in `scripts/__tests__` names `smoke-test.sh` (`grep -il smoke-test *.test.sh` = 0; control `start-secuura` = 4), so B6 has nothing to drive.
- Golden precheck through the real `tasks/bash_patch/checker.sh` in the clone: `runs/2026-09-22_feed16-drafter-precheck/DEGRADEDWARN/checker.log` (the verdict is quoted on the queue line, never here by hand).
- Ticket KS-1245 on the Secuura board at 2026-09-22 18:57:07 AEST: Backlog, P3, unassigned, no PR, not archived (`fetch_tickets.log`). Round-19 collision: `Blockchain/Dev/scripts/smoke-test.sh` is in NONE of the 21 round-19 PR heads' file sets (`union.log`: 0 of 38 paths; control `Blockchain/Dev/CONTRIBUTING.md` = 1); the `scripts/` DIRECTORY is Seat C's lane (10 sibling `scripts/__tests__` suites and 5 `scripts/` files are in the union) - Wednesday rules the lane at queue time, as for KS-1145.
