# READY — KS-998-FORMATGATESTDIN-1 (spark-dsv4flash, briefed, bash_patch, bash) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-09_KS-998-format-gate-npm-stdin/out.md.checker/patch.diff`** (from `ls` at 14:19 2026-10-09; sha256[:16] 8c2bd29b5ae4010a, 5136 B — a BYTE count; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-09_KS-998-format-gate-npm-stdin/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-09_KS-998-format-gate-npm-stdin/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; golden not located — no identity claim is made.

**Held 14:19 2026-10-09 by Wednesday 14:0x seat after a source read (hold_ready.py, bash_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-09_KS-998-format-gate-npm-stdin/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6, systemTest/scripts/check-package-format.sh and systemTest/__tests__/package_format_gate.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['systemTest/__tests__/ks998_format_gate_stdin_isolated.test.sh', 'systemTest/scripts/check-package-format.sh']`
- No new-file normalisation line in checker.out (none applied)
- Touched-file set [checker.out B3, verbatim]: `PASS B3 touched-file set == { systemTest/scripts/check-package-format.sh , systemTest/__tests__/ks998_format_gate_stdin_isolated.test.sh (new) }`
- Declared set [input.json product_file + suggested_test_file]: `systemTest/scripts/check-package-format.sh` (script) and `systemTest/__tests__/ks998_format_gate_stdin_isolated.test.sh` (NEW file — `--- /dev/null` section) — equal to sections.json's paths (2 files); reference test `systemTest/__tests__/package_format_gate.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b every must_change site is a '-' line; every brief '+' line is in the script hunk; no tip line re-added as '+'` — re-measured from `section_2.diff` + input.json defect_line: every one of the 4 brief `+` line(s) present; script `+` lines 4 ordered-equal (whitespace-stripped) to expected_plus (ASCII); `-` lines 1; must_change sites 1/1 each a `-` line; must_remove 1 (all among the `-` lines).
- No B3c line in checker.out (no stays-site repair)
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `systemTest/__tests__/ks998_format_gate_stdin_isolated.test.sh` (+93/-0 lines counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `section_1.diff.header_measure.out`: EMPTY (headers consistent); `section_1.diff.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `systemTest/scripts/check-package-format.sh` (+4/-1 lines counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `section_2.diff.header_measure.out`: EMPTY (headers consistent); `section_2.diff.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: systemTest/__tests__/ks998_format_gate_stdin_isolated.test.sh fails at the untouched tip (rc=1, 3 FAIL line(s))` · run line [verbatim]: `B4 run at the tip: rc=1 fail_lines=3 pass_lines=6 load_error=0 timeout=0` [red_first.out re-count: 3 FAIL line(s), 6 pass line(s); FAIL lines: ['FAIL drain then green -> both packages checked', 'FAIL drain then green -> green reports format:check OK', 'FAIL drain then red -> the gate fails (exit 1)']]
- Parse [checker.out B5a, verbatim]: `PASS B5a the script parses after the hunk (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: systemTest/__tests__/ks998_format_gate_stdin_isolated.test.sh passes with the script hunk (rc=0, 0 FAIL lines, 9 pass line(s))` · run line [verbatim]: `B5 run after the script hunk: rc=0 fail_lines=0 pass_lines=9 load_error=0 timeout=0` [green_after.out re-count: 0 FAIL line(s), 9 pass line(s)]
- Siblings [checker.out B6, verbatim]: `PASS B6 sibling suite(s) that drive check-package-format.sh: no NEW failure after (2 suite(s))` [2 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 test=systemTest/__tests__/ks998_format_gate_stdin_isolated.test.sh red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (7/7)`

**PR NOTES for the raise seat:** BASH_PATCH — PRODUCT BYTES CHANGE: `systemTest/scripts/check-package-format.sh` (+4/-1 counted from `section_2.diff` by hold_ready — the bash checker writes no numstat.out) and the NEW test `systemTest/__tests__/ks998_format_gate_stdin_isolated.test.sh` (+93/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `81d2e5f4c4151f5291a7a9c186d93a02dc5d38d6` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (script bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-09_KS-998-format-gate-npm-stdin/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-09_KS-998-format-gate-npm-stdin/checker.out`.

```diff
--- /dev/null
+++ b/systemTest/__tests__/ks998_format_gate_stdin_isolated.test.sh
@@ -0,0 +1,93 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for systemTest/scripts/check-package-format.sh - KS-998 robustness
+# note: a package's format:check must NOT inherit the gate's own stdin.
+# =============================================================================
+# The gate reads its selected packages one per line from a here-string on
+# stdin (`done <<< "$selected"`), and runs each package's
+# `npm run --silent format:check` INSIDE that loop with no redirect. npm passes
+# its stdin to the script, so a format:check that reads stdin swallows the
+# names of every package after it in the list. Those packages are never
+# checked, and a red one among them passes the gate. `< /dev/null` on the npm
+# call closes that.
+#
+# Same fixture method as package_format_gate.test.sh: a copy of the gate inside
+# a temp tree, fixture packages whose `format:check` is plain shell, so no npm
+# install and no real prettier is needed (npm itself must be on PATH, as it is
+# for that suite).
+#
+# Usage: bash systemTest/__tests__/ks998_format_gate_stdin_isolated.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+GATE_SRC="${PACKAGE_FORMAT_GATE_SH:-$HERE/../scripts/check-package-format.sh}"
+PASS=0; FAIL=0
+
+[[ -f "$GATE_SRC" ]] || { echo "FATAL: gate script not found at $GATE_SRC" >&2; exit 2; }
+
+FIX="$(mktemp -d "${TMPDIR:-/tmp}/secuura-ks998-stdin.XXXXXX")"
+trap 'rm -rf "$FIX"' EXIT INT TERM
+
+check() {
+    local desc="$1" want="$2" got="$3"
+    if [[ "$got" == "$want" ]]; then PASS=$((PASS+1)); printf 'ok   %s\n' "$desc"
+    else FAIL=$((FAIL+1)); printf 'FAIL %s\n       want "%s", got "%s"\n' "$desc" "$want" "$got"; fi
+}
+
+GATE="$FIX/systemTest/scripts/check-package-format.sh"
+mkdir -p "$FIX/systemTest/scripts"
+cp "$GATE_SRC" "$GATE"
+
+# mk_pkg <name> <format:check shell command> - deps always present
+mk_pkg() {
+    local name="$1" cmd="$2"
+    local dir="$FIX/systemTest/$name"
+    mkdir -p "$dir/node_modules/.bin"
+    cat > "$dir/package.json" <<JSON
+{ "name": "fixture-$name", "version": "0.0.0", "scripts": { "format:check": "$cmd" } }
+JSON
+    printf '#!/bin/sh\nexit 0\n' > "$dir/node_modules/.bin/prettier"
+    chmod +x "$dir/node_modules/.bin/prettier"
+}
+
+# `drain` sorts first, so the gate runs it before `green` and `red`. Its
+# format:check is clean but reads whatever is on its stdin.
+mk_pkg drain "cat >/dev/null; exit 0"
+mk_pkg green "exit 0"
+mk_pkg red   "echo '[warn] src/a.ts'; exit 1"
+
+# --- CELL 1 (RED at the tip): the package after a stdin reader is still checked --
+out="$(printf '%s\n' 'systemTest/drain/src/a.ts
+systemTest/green/src/b.ts' | bash "$GATE" 2>&1)"
+check "drain then green -> both packages checked" "1" \
+    "$(printf '%s\n' "$out" | grep -cF '2 package(s) checked, 0 skipped, 0 failed')"
+check "drain then green -> green reports format:check OK" "1" \
+    "$(printf '%s\n' "$out" | grep -cF 'systemTest/green ')"
+
+# --- CELL 2 (RED at the tip): a red package after a stdin reader still fails ----
+out="$(printf '%s\n' 'systemTest/drain/src/a.ts
+systemTest/red/src/a.ts' | bash "$GATE" 2>&1)"; rc=$?
+check "drain then red -> the gate fails (exit 1)" "1" "$rc"
+
+# --- CELL 3 (CONTROL, tip AND after): each package alone behaves as before -------
+out="$(printf '%s\n' 'systemTest/drain/src/a.ts' | bash "$GATE" 2>&1)"; rc=$?
+check "CONTROL drain alone -> exit 0" "0" "$rc"
+check "CONTROL drain alone -> one package checked" "1" \
+    "$(printf '%s\n' "$out" | grep -cF '1 package(s) checked, 0 skipped, 0 failed')"
+out="$(printf '%s\n' 'systemTest/red/src/a.ts' | bash "$GATE" 2>&1)"; rc=$?
+check "CONTROL red alone -> exit 1" "1" "$rc"
+check "CONTROL red alone -> names the file" "1" \
+    "$(printf '%s\n' "$out" | grep -cF 'systemTest/red/src/a.ts   (in this push)')"
+
+# --- CELL 4 (CONTROL, tip AND after): no stdin reader, both packages checked -----
+out="$(printf '%s\n' 'systemTest/green/src/b.ts
+systemTest/red/src/a.ts' | bash "$GATE" 2>&1)"; rc=$?
+check "CONTROL green then red -> exit 1" "1" "$rc"
+check "CONTROL green then red -> both packages checked" "1" \
+    "$(printf '%s\n' "$out" | grep -cF '2 package(s) checked, 0 skipped, 1 failed')"
+
+echo ""
+echo "ks998_format_gate_stdin_isolated: ${PASS} passed, ${FAIL} failed"
+(( FAIL == 0 ))
--- a/systemTest/scripts/check-package-format.sh
+++ b/systemTest/scripts/check-package-format.sh
@@ -152,4 +152,7 @@ while IFS= read -r p; do
-    out="$(cd "$dir" && npm run --silent format:check 2>&1)"
+    # KS-998: `< /dev/null`. This loop reads its package list from the
+    # here-string at its `done` on stdin, and npm hands its stdin to the script:
+    # a format:check that reads stdin would swallow every package after it.
+    out="$(cd "$dir" && npm run --silent format:check < /dev/null 2>&1)"
     rc=$?
     checked=$((checked + 1))
     if [ "$rc" -eq 0 ]; then
```
