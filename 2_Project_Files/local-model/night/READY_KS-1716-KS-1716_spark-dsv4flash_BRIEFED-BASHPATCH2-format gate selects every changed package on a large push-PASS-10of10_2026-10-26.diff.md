# READY — KS-1716-KS-1716 (Spark (DeepSeek V4 Flash), briefed, bash_patch2, bash) — PASS 10/10 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1716_p1/out.md.checker/patch.diff`** (from `ls` at 09:51 2026-10-26; sha256[:16] 47035c2470c21e80, 5026 B; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1716_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1716_p1/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1716_p1/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made. Run's own golden_cmp.out [verbatim]: `golden tree 4e85a4d97a49bb068b34734ae223ac9cef9fb6dc · patch tree 4e85a4d97a49bb068b34734ae223ac9cef9fb6dc -> TREE-IDENTICAL (logs /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-26_ks_1716_p1_093120/*_cmp.index.out)`.

**Held 09:51 2026-10-26 by Wednesday after a source read (hold_ready.py, bash_patch2 path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1716_p1/out.md.checker` or MEASURED here, not typed; the artefact each came from is named in brackets).** Tip `7ce64f5d6739c4e38a1ddcb3d4a84a4f6de41480`.
- Kind [three signals, all agree]: input.json task_type `bash_patch2`; checker.out's first line, verbatim: `mode: bash_patch2 (declared: 1 product(s), 1 test(s): 1 red, 0 support)`; round.json tier `bash_patch2`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 7ce64f5d6739c4e38a1ddcb3d4a84a4f6de41480, systemTest/scripts/check-package-format.sh and systemTest/__tests__/ks998_format_gate_stdin_isolated.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['systemTest/scripts/check-package-format.sh', 'systemTest/__tests__/ks1716_format_gate_selects_every_changed_package_on_a_large_push.test.sh']`
- Touched-file set [checker.out B3, verbatim]: `PASS B3 (bash_patch2) touched-file set == the declared set: { systemTest/scripts/check-package-format.sh } + { systemTest/__tests__/ks1716_format_gate_selects_every_changed_package_on_a_large_push.test.sh }` — MEASURED here: sections.json paths == each section's own `git apply --numstat` paths == the declared set (2 files: 1 product(s) + 1 test(s)); reference test `systemTest/__tests__/ks998_format_gate_stdin_isolated.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b 1 must_change site(s) of check-package-format.sh are '-' lines, no stays-site removed; all 1 brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)` — re-measured: all 1 brief `+` line(s) among the product sections' `+` lines (multiset; ASCII); must_change sites 1/1 of `systemTest/scripts/check-package-format.sh` each a `-` line; no stays-site removed.
- Byte identity [checker.out B3x, verbatim]: `PASS B3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)` · [brief_bytes.out, verbatim]: `OK systemTest/scripts/check-package-format.sh 1 '+' line(s) byte-identical to the brief, in order; OK systemTest/__tests__/ks1716_format_gate_selects_every_changed_package_on_a_large_push.test.sh 91 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Brief header [`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1716_p1/KS-1716.md`]: `File:` lines == product_files ['systemTest/scripts/check-package-format.sh']; `Test …:` lines == test_files ['systemTest/__tests__/ks1716_format_gate_selects_every_changed_package_on_a_large_push.test.sh'].
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `systemTest/scripts/check-package-format.sh` (+1/-1 counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `systemTest/__tests__/ks1716_format_gate_selects_every_changed_package_on_a_large_push.test.sh` (+91/-0 counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: with every test section and no product section — ks1716_format_gate_selects_every_changed_package_on_a_large_push.test.sh=RED(rc 1, 3 FAIL)`
- Parse [checker.out B5a, verbatim]: `PASS B5a every .sh product parses after the patch (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: every declared test passes with all 1 product section(s): ks1716_format_gate_selects_every_changed_package_on_a_large_push.test.sh(7 pass)`
- RED test `systemTest/__tests__/ks1716_format_gate_selects_every_changed_package_on_a_large_push.test.sh` (new) — B4 [verbatim]: `B4 ks1716_format_gate_selects_every_changed_package_on_a_large_push.test.sh (RED) with the test edits alone: rc=1 fail_lines=3 pass_lines=4 load_error=0 timeout=0` [red FAIL lines: ['FAIL large list, aaa first -> both packages checked', 'FAIL large list, red package first -> the gate fails (exit 1)', 'FAIL large list, zzz only -> one package checked']] · B5 [verbatim]: `B5 ks1716_format_gate_selects_every_changed_package_on_a_large_push.test.sh after every product section: rc=0 fail_lines=0 pass_lines=7 load_error=0 timeout=0`
- Siblings [checker.out B6, verbatim]: `PASS B6 undeclared sibling suite(s) naming a product: no NEW failure after (3 suite(s): ks998_format_gate_push_label_is_literal.test.sh 8p/0f->8p/0f; ks998_format_gate_stdin_isolated.test.sh 9p/0f->9p/0f; package_format_gate.test.sh 435p/0f->435p/0f;)` [3 sib<i>_after.out file(s) present]
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- Anchor [checker.out A2a, verbatim]: `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=1)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red=1 support=0 red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (10/10)`

**PR NOTES for the raise seat:** BASH_PATCH2 — PRODUCT BYTES CHANGE: `systemTest/scripts/check-package-format.sh` (+1/-1) (counted from the section files — the bash_patch2 checker writes no numstat.out) and the test(s) `systemTest/__tests__/ks1716_format_gate_selects_every_changed_package_on_a_large_push.test.sh` (NEW, RED, +91/-0); 2 files in all. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `7ce64f5d6739c4e38a1ddcb3d4a84a4f6de41480` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1716_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1716_p1/KS-1716.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-26_ks_1716_p1/checker.out`.

```diff
--- a/systemTest/scripts/check-package-format.sh
+++ b/systemTest/scripts/check-package-format.sh
@@ -728,5 +728,5 @@ else
     changed_paths="$(cat)"
     for p in "${packages[@]+"${packages[@]}"}"; do
-        if printf '%s\n' "$changed_paths" | grep -q "^systemTest/${p}/"; then
+        if printf '%s\n' "$changed_paths" | grep "^systemTest/${p}/" > /dev/null; then
             selected="${selected}${p}
 "
--- /dev/null
+++ b/systemTest/__tests__/ks1716_format_gate_selects_every_changed_package_on_a_large_push.test.sh
@@ -0,0 +1,91 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for systemTest/scripts/check-package-format.sh - KS-1716: the package
+# selection must not drop a changed package when the pushed path list is large.
+# =============================================================================
+# The gate picks each package with `printf '%s\n' "$changed_paths" | grep -q ...`
+# under `set -uo pipefail`. grep -q exits at its FIRST match; when the list is
+# bigger than the pipe buffer (64 KiB) printf is still writing, gets EPIPE, and
+# pipefail turns the pipeline into "no match". The package is then neither
+# checked nor skipped, and the gate still prints "0 skipped". The fix reads the
+# list to EOF (grep without -q, output to /dev/null).
+#
+# Same fixture method as ks998_format_gate_stdin_isolated.test.sh: a copy of the
+# gate inside a temp tree, fixture packages whose format:check is plain shell.
+#
+# Usage: bash systemTest/__tests__/ks1716_format_gate_selects_every_changed_package_on_a_large_push.test.sh
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
+FIX="$(mktemp -d "${TMPDIR:-/tmp}/secuura-ks1716.XXXXXX")"
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
+# `aaa` sorts first, so it matches on the first line of the list; `zzz` carries
+# the bulk of the list (2500 paths, well over 64 KiB). `red` fails its check.
+mk_pkg aaa "exit 0"
+mk_pkg zzz "exit 0"
+mk_pkg abc "echo '[warn] src/a.ts'; exit 1"
+
+# big_list <first line>: that line, then 2500 paths under systemTest/zzz/
+big_list() {
+    printf '%s\n' "$1"
+    awk 'BEGIN { for (i = 1; i <= 2500; i++) printf "systemTest/zzz/src/generated/file_%05d_padding_padding_padding.ts\n", i }'
+}
+
+# --- CELL 0 (CONTROL): the fixture list really is over the pipe buffer ----------
+check "CONTROL the large list is over 64 KiB" "1" \
+    "$([ "$(big_list 'systemTest/aaa/src/a.ts' | wc -c | tr -d ' ')" -gt 65536 ] && echo 1 || echo 0)"
+
+# --- CELL 1 (RED at the tip): aaa matches first, yet both packages are checked --
+out="$(big_list 'systemTest/aaa/src/a.ts' | bash "$GATE" 2>&1)"; rc=$?
+check "CONTROL large list, aaa first -> exit 0" "0" "$rc"
+check "large list, aaa first -> both packages checked" "1" \
+    "$(printf '%s\n' "$out" | grep -cF '2 package(s) checked, 0 skipped, 0 failed')"
+
+# --- CELL 2 (RED at the tip): a red package matched first still fails the gate --
+out="$(big_list 'systemTest/abc/src/a.ts' | bash "$GATE" 2>&1)"; rc=$?
+check "large list, red package first -> the gate fails (exit 1)" "1" "$rc"
+
+# --- CELL 3 (CONTROL, tip AND after): a small list selects the same packages ----
+out="$(printf '%s\n' 'systemTest/aaa/src/a.ts' 'systemTest/zzz/src/b.ts' | bash "$GATE" 2>&1)"; rc=$?
+check "CONTROL small list -> exit 0" "0" "$rc"
+check "CONTROL small list -> both packages checked" "1" \
+    "$(printf '%s\n' "$out" | grep -cF '2 package(s) checked, 0 skipped, 0 failed')"
+
+# --- CELL 4 (RED at the tip): a large list naming only zzz still checks zzz ------
+out="$(big_list 'systemTest/zzz/src/first.ts' | bash "$GATE" 2>&1)"; rc=$?
+check "large list, zzz only -> one package checked" "1" \
+    "$(printf '%s\n' "$out" | grep -cF '1 package(s) checked, 0 skipped, 0 failed')"
+
+echo ""
+echo "ks1716_format_gate_selects_every_changed_package_on_a_large_push: ${PASS} passed, ${FAIL} failed"
+(( FAIL == 0 ))
```
