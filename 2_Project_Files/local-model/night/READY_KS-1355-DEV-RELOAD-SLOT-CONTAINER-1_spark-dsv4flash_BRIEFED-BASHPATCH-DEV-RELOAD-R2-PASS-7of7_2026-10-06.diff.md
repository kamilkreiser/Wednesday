# READY — KS-1355-DEV-RELOAD-SLOT-CONTAINER-1 (Spark deepseek-v4-flash, briefed, bash_patch round 2, bash) — PASS 7/7 — HELD for QA (label corrected by Wednesday 18:0x: hold_ready.py tags bash_patch as Ornith)

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-dev-reload-slot-container-r2/out.md.checker/patch.diff`** (from `ls` at 18:04 2026-10-06; sha256[:16] c9e9d772affa3597, 5499 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-dev-reload-slot-container-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-dev-reload-slot-container-r2/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-dev-reload-slot-container-r2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-dev-reload-slot-container-control-r2/out.md.checker/patch.diff` rc 0, Wednesday (evening seat), source read 18:0x); APPLIED PRODUCT IDENTICAL: the two checkers' own `after.sh` (the script after its hunk) `cmp` rc 0.

**Held 18:04 2026-10-06 by Wednesday (evening seat), source read 18:0x after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-dev-reload-slot-container-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe, Blockchain/Dev/scripts/dev-reload.sh and Blockchain/Dev/scripts/__tests__/stack_guard.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh', 'Blockchain/Dev/scripts/dev-reload.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { Blockchain/Dev/scripts/dev-reload.sh , Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/scripts/dev-reload.sh` (script) and `Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `Blockchain/Dev/scripts/__tests__/stack_guard.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_2.diff` + input.json defect_line: every one of the 7 brief `+` line(s) present; script `+` lines 8 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 2; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh` (+99/-0 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/dev-reload.sh` (+8/-2 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh fails at the untouched tip (rc=1, 4 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=4 pass_lines=3 load_error=0 timeout=0` [red_first.out re-count: 4 FAIL line(s), 3 pass line(s); FAIL lines: ['FAIL slot 2: reload of demo exits 0 when secuura-s2-demo is running', 'FAIL slot 2: it restarts secuura-s2-demo', 'FAIL slot 2: it copies dist into secuura-s2-demo:/app/dist', "FAIL slot 2 with slot 1 also up: slot 1's secuura-demo is NOT restarted"]]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 7 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=7 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 7 pass line(s)]
- Siblings [checker.out B6, verbatim]: `INFO B6 no sibling suite in Blockchain/Dev/scripts/__tests__ names dev-reload.sh — nothing else drives this script (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/dev-reload.sh` (+8/-2 counted from `section_2.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh` (+99/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4eaf7741a6a4b2c82752d0d94f8bbacb5493aabe` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-dev-reload-slot-container-r2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-06_KS-1355-dev-reload-slot-container-r2/checker.out`.

```diff
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh
@@ -0,0 +1,99 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for scripts/dev-reload.sh - KS-1355 spot 2: the container it hot-swaps
+# into must be the CURRENT SLOT's, not slot 1's.
+# =============================================================================
+# dev-reload.sh named its container `secuura-<svc>` (slot 1's name) and never
+# sourced stack_env.sh, so with SECUURA_STACK_SLOT=2 it could not find
+# `secuura-s2-<svc>`, and when slot 1 was also up it rebuilt dist/ and restarted
+# SLOT 1's container - another stack's service - and reported success.
+#
+# Same method as stack_guard.test.sh: `docker` (and `npm`) are stubs on PATH, so
+# no daemon, no build and no network. A copy of dev-reload.sh and stack_env.sh
+# runs inside a temp tree with one fixture service, `demo`; the docker stub
+# lists the containers a case says are running and logs every cp / restart.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/ks1355_dev_reload_slot_container.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SCRIPTS="$(cd "$HERE/.." && pwd)"
+PASS=0; FAIL=0
+
+check() {
+  local desc="$1" want="$2" got="$3"
+  if [[ "$got" == "$want" ]]; then PASS=$((PASS + 1)); printf 'ok   %s\n' "$desc"
+  else FAIL=$((FAIL + 1)); printf 'FAIL %s\n       want "%s", got "%s"\n' "$desc" "$want" "$got"; fi
+}
+
+FIX="$(mktemp -d "${TMPDIR:-/tmp}/secuura-ks1355-reload.XXXXXX")"
+trap 'rm -rf "$FIX"' EXIT INT TERM
+
+DEV="$FIX/repo/Blockchain/Dev"
+mkdir -p "$DEV/scripts" "$DEV/services/demo" "$FIX/bin"
+cp "$SCRIPTS/dev-reload.sh" "$SCRIPTS/stack_env.sh" "$DEV/scripts/"
+printf '{ "name": "demo", "version": "0.0.0" }\n' > "$DEV/services/demo/package.json"
+
+# docker stub: `ps` prints the names in $KS1355_FIX/running; cp and restart are logged.
+cat > "$FIX/bin/docker" <<'STUB'
+#!/usr/bin/env bash
+case "$1" in
+  ps) cat "$KS1355_FIX/running" 2>/dev/null; exit 0 ;;
+  cp|restart) echo "$*" >> "$KS1355_FIX/docker.log"; exit 0 ;;
+esac
+exit 0
+STUB
+# npm stub: `npm run build` (run inside services/<svc>) just produces dist/.
+cat > "$FIX/bin/npm" <<'STUB'
+#!/usr/bin/env bash
+mkdir -p dist && echo built > dist/index.js
+STUB
+chmod +x "$FIX/bin/docker" "$FIX/bin/npm"
+
+# reload <slot or ""> <running container names...> - prints the exit code.
+# LC_ALL=C: under bash 3.2 in a UTF-8 locale, dev-reload.sh's own `$CONTAINER...`
+# progress line (an ellipsis right after the name) reads as an unbound variable and
+# aborts before the restart - a separate defect, not this ticket's; C keeps it out.
+reload() {
+  local slot="$1"; shift
+  printf '%s\n' "$@" > "$FIX/running"
+  : > "$FIX/docker.log"
+  if [[ -n "$slot" ]]; then
+    env -u STACK_SLOT -u STACK_PREFIX -u COMPOSE_PROJECT_NAME LC_ALL=C PATH="$FIX/bin:$PATH" KS1355_FIX="$FIX" \
+      SECUURA_STACK_SLOT="$slot" bash "$DEV/scripts/dev-reload.sh" demo > "$FIX/out" 2>&1
+  else
+    env -u STACK_SLOT -u STACK_PREFIX -u COMPOSE_PROJECT_NAME -u SECUURA_STACK_SLOT LC_ALL=C PATH="$FIX/bin:$PATH" \
+      KS1355_FIX="$FIX" bash "$DEV/scripts/dev-reload.sh" demo > "$FIX/out" 2>&1
+  fi
+  echo $?
+}
+restarted() { grep -c "^restart $1\$" "$FIX/docker.log"; }
+
+# --- RED at the tip: slot 2 reloads slot 2's container ------------------------
+rc="$(reload 2 secuura-s2-demo)"
+check "slot 2: reload of demo exits 0 when secuura-s2-demo is running" "0" "$rc"
+check "slot 2: it restarts secuura-s2-demo" "1" "$(restarted secuura-s2-demo)"
+check "slot 2: it copies dist into secuura-s2-demo:/app/dist" "1" \
+  "$(grep -c '^cp services/demo/dist/\. secuura-s2-demo:/app/dist$' "$FIX/docker.log")"
+
+# --- RED at the tip: slot 2 never touches slot 1's container ------------------
+# Slot 1 and slot 2 both up: the tip found `secuura-demo` and restarted it.
+rc="$(reload 2 secuura-demo secuura-s2-demo)"
+check "slot 2 with slot 1 also up: slot 1's secuura-demo is NOT restarted" "0" "$(restarted secuura-demo)"
+
+# --- CONTROL (tip AND after): slot 1 keeps the historic name -------------------
+rc="$(reload "" secuura-demo)"
+check "CONTROL no slot set: exits 0 and restarts secuura-demo" "0 1" "$rc $(restarted secuura-demo)"
+rc="$(reload 1 secuura-demo)"
+check "CONTROL slot 1: exits 0 and restarts secuura-demo" "0 1" "$rc $(restarted secuura-demo)"
+
+# --- CONTROL (tip AND after): a missing container still refuses, touching nothing
+rc="$(reload 1 secuura-other)"
+check "CONTROL slot 1, demo not running: exits 1 and restarts nothing" "1 0" \
+  "$rc $(grep -c . "$FIX/docker.log")"
+
+echo ""
+echo "ks1355_dev_reload_slot_container: ${PASS} passed, ${FAIL} failed"
+(( FAIL == 0 ))
--- a/Blockchain/Dev/scripts/dev-reload.sh
+++ b/Blockchain/Dev/scripts/dev-reload.sh
@@ -44,4 +44,10 @@ fi
 SVC_DIR="services/$SVC"
-CONTAINER="secuura-$SVC"
-
+# KS-1355: the container is per stack slot (`secuura-<svc>` on slot 1, `secuura-sN-<svc>` on slot N >= 2),
+# so the name comes from stack_env.sh, the derivation start-secuura.sh and stop-secuura.sh share. A malformed
+# or out-of-range slot exits 2 there instead of reloading slot 1's container.
+PROJECT_ROOT="$(cd "$ROOT/../.." && pwd)"
+# shellcheck source=stack_env.sh
+source "$ROOT/scripts/stack_env.sh"
+CONTAINER="${STACK_PREFIX}-$SVC"
+
 if [[ ! -d "$SVC_DIR" ]]; then
```
