# READY — KS-1497-STAGINGDIR-1 (Spark (DeepSeek V4 Flash), briefed, bash_patch2, bash) — PASS 9/9 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1497_p1/out.md.checker/patch.diff`** (from `ls` at 23:18 2026-10-18; sha256[:16] eeaac686abb7b2da, 5467 B; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1497_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1497_p1/out.md.checker/section_2.diff`). Checker B2 (verbatim from checker.out): `PASS B2 every section applies at the tip (strict)`; CONTEXT-ONLY difference from the drafter's golden `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1497_p1-control/out.md.checker/patch.diff` (bytes DIFFER: `cmp` rc 1): change lines (`+`/`-`, ordered) IDENTICAL in every section; APPLIED PRODUCT(S): the two checkers' own `after_prisma-generate.cjs` IDENTICAL (`cmp` rc 0). Run's own golden_cmp.out [verbatim]: `golden tree f91cb64d00234fc8b5999d7e489b1869a2c28dac · patch tree f91cb64d00234fc8b5999d7e489b1869a2c28dac -> TREE-IDENTICAL (logs /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-18_ks_1497_p1_231410/*_cmp.index.out)`.

**Held 23:18 2026-10-18 by Wednesday after a source read (hold_ready.py, bash_patch2 path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1497_p1/out.md.checker` or MEASURED here, not typed; the artefact each came from is named in brackets).** Tip `1f73d7ac8cc17add318601c6c572bcace3d5a596`.
- Kind [three signals, all agree]: input.json task_type `bash_patch2`; checker.out's first line, verbatim: `mode: bash_patch2 (declared: 1 product(s), 1 test(s): 1 red, 0 support)`; round.json tier `bash_patch2`.
- Subject [checker.out B0, verbatim]: `PASS B0 subject: clone at 1f73d7ac8cc17add318601c6c572bcace3d5a596, Blockchain/Dev/scripts/prisma-generate.cjs and Blockchain/Dev/scripts/__tests__/ks998_pre_push_stale_base_hint.test.sh present`
- Output shape [checker.out B1, verbatim]: `PASS B1 output is exactly one fenced ```diff block` · sections [verbatim]: `sections: ['Blockchain/Dev/scripts/prisma-generate.cjs', 'Blockchain/Dev/scripts/__tests__/ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh']`
- Touched-file set [checker.out B3, verbatim]: `PASS B3 (bash_patch2) touched-file set == the declared set: { Blockchain/Dev/scripts/prisma-generate.cjs } + { Blockchain/Dev/scripts/__tests__/ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh }` — MEASURED here: sections.json paths == each section's own `git apply --numstat` paths == the declared set (2 files: 1 product(s) + 1 test(s)); reference test `Blockchain/Dev/scripts/__tests__/ks998_pre_push_stale_base_hint.test.sh` untouched.
- Brief lines [checker.out B3b, verbatim]: `PASS B3b 0 must_change site(s) of prisma-generate.cjs are '-' lines, no stays-site removed; all 13 brief '+' line(s) are in the product sections (multiset); no tip line re-added in any product (A3d)` — re-measured: all 13 brief `+` line(s) among the product sections' `+` lines (multiset; ASCII); must_change sites 0/0 of `Blockchain/Dev/scripts/prisma-generate.cjs` each a `-` line; no stays-site removed.
- Byte identity [checker.out B3x, verbatim]: `PASS B3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)` · [brief_bytes.out, verbatim]: `OK Blockchain/Dev/scripts/prisma-generate.cjs 13 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/scripts/__tests__/ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh 65 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Brief header [`/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1497_p1/KS-1497.md`]: `File:` lines == product_files ['Blockchain/Dev/scripts/prisma-generate.cjs']; `Test …:` lines == test_files ['Blockchain/Dev/scripts/__tests__/ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh'].
- Sections [out.md.checker/sections.json + section_<k>.diff.opts + .header_measure.out + .check.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/scripts/prisma-generate.cjs` (+13/-0 counted from the applied section file; git-apply options per `section_1.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- section 2 `section_2.diff` → `Blockchain/Dev/scripts/__tests__/ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh` (+65/-0 counted from the applied section file; git-apply options per `section_2.diff.opts`: `(none — strict)`; `.header_measure.out`: EMPTY; `.check.out` (strict --check): EMPTY (clean))
- RED-FIRST [checker.out B4, verbatim]: `PASS B4 RED-FIRST: with every test section and no product section — ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh=RED(rc 1, 5 FAIL)`
- Parse [checker.out B5a, verbatim]: `PASS B5a every .sh product parses after the patch (bash -n)`
- GREEN-AFTER [checker.out B5, verbatim]: `PASS B5 GREEN-AFTER: every declared test passes with all 1 product section(s): ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh(7 pass)`
- RED test `Blockchain/Dev/scripts/__tests__/ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh` (new) — B4 [verbatim]: `B4 ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh (RED) with the test edits alone: rc=1 fail_lines=5 pass_lines=2 load_error=0 timeout=0` [red FAIL lines: ["FAIL: RED KS-1497 a symlinked .generate is refused with exit 2 (want '2', got '0')", "FAIL: RED KS-1497 the refusal for a symlinked .generate says so (want 'yes/yes', got 'no/no')", "FAIL: RED KS-1497 nothing is written into the symlink's target (want '0', got '1')", "FAIL: RED KS-1497 a .generate that is a file is refused with exit 2 (want '2', got '1')", "FAIL: RED KS-1497 the refusal for a .generate that is a file says so (want 'yes/yes', got 'no/no')"]] · B5 [verbatim]: `B5 ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh after every product section: rc=0 fail_lines=0 pass_lines=7 load_error=0 timeout=0`
- Siblings [checker.out B6, verbatim]: `INFO B6 no undeclared suite in Blockchain/Dev/scripts/__tests__ names a product's stem — nothing else drives them (stated, not counted)`
- Shellcheck [checker.out B7, verbatim]: `INFO B7 shellcheck not installed (informational)`
- Anchor [checker.out A2a, verbatim]: `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=1)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red=1 support=0 red_first=yes apply_mode=strict`
- RESULT [checker.out, verbatim]: `RESULT: PASS (9/9)`

**PR NOTES for the raise seat:** BASH_PATCH2 — PRODUCT BYTES CHANGE: `Blockchain/Dev/scripts/prisma-generate.cjs` (+13/-0) (counted from the section files — the bash_patch2 checker writes no numstat.out) and the test(s) `Blockchain/Dev/scripts/__tests__/ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh` (NEW, RED, +65/-0); 2 files in all. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `1f73d7ac8cc17add318601c6c572bcace3d5a596` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product bytes change) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1497_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1497_p1/KS-1497.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-18_ks_1497_p1/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/prisma-generate.cjs
+++ b/Blockchain/Dev/scripts/prisma-generate.cjs
@@ -66,4 +66,17 @@ if (check) {
 
 const staging = path.join(svc, 'node_modules', '.generate');
+// KS-1497: never stage the schema through a symlink (the copy would land in its target) or onto a file (mkdir throws a stack trace).
+let stagingStat = null;
+try {
+  stagingStat = fs.lstatSync(staging);
+} catch (err) {
+  if (err.code !== 'ENOENT') throw err;
+}
+if (stagingStat && stagingStat.isSymbolicLink()) {
+  fail(`${staging} is a symbolic link; refusing to stage the schema through it. Remove it and run again.`);
+}
+if (stagingStat && !stagingStat.isDirectory()) {
+  fail(`${staging} exists and is not a directory. Remove it and run again.`);
+}
 fs.mkdirSync(staging, { recursive: true });
 const staged = path.join(staging, 'schema.prisma');
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh
@@ -0,0 +1,65 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/prisma-generate.cjs - KS-1497 items 2 and 4:
+# the staging directory node_modules/.generate must be a plain directory.
+# =============================================================================
+# The script copies the schema into node_modules/.generate, runs prisma generate, and removes
+# the directory. A .generate that is a SYMLINK made it write the schema into the link's target
+# (and delete only the link); a .generate that is a FILE made mkdirSync throw an uncaught
+# stack trace (rc 1). Both now stop with a "generate:" message and exit 2 before anything is
+# written. This suite runs the REAL script against a fixture service whose prisma CLI is a stub.
+# Usage: bash Blockchain/Dev/scripts/__tests__/ks1497_prisma_generate_refuses_a_bad_staging_dir.test.sh
+# =============================================================================
+
+set -uo pipefail
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+SCRIPT="${PRISMA_GENERATE_CJS:-$HERE/../prisma-generate.cjs}"
+[[ -r "$SCRIPT" ]] || { echo "FATAL: prisma-generate.cjs not readable at $SCRIPT" >&2; exit 2; }
+command -v node >/dev/null 2>&1 || { echo "FATAL: node is required" >&2; exit 2; }
+
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1497.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+PASS=0
+FAIL=0
+cell() { if [[ "$3" == "$2" ]]; then echo "PASS: $1"; PASS=$((PASS+1)); else echo "FAIL: $1 (want '$2', got '$3')"; FAIL=$((FAIL+1)); fi; }
+
+# fixture <name>: a service dir with a stub prisma CLI (generate writes node_modules/.prisma/client/default.js) and a schema.
+fixture() {
+  local svc="$WORK/$1/svc"
+  mkdir -p "$svc/node_modules/prisma/build" "$svc/node_modules/@prisma/client"
+  printf '{ "name": "prisma", "version": "0.0.0", "bin": "build/index.js" }\n' > "$svc/node_modules/prisma/package.json"
+  printf '%s\n' "const fs = require('fs');" "fs.mkdirSync('node_modules/.prisma/client', { recursive: true });" "fs.writeFileSync('node_modules/.prisma/client/default.js', '');" > "$svc/node_modules/prisma/build/index.js"
+  printf '{ "name": "@prisma/client", "version": "0.0.0" }\n' > "$svc/node_modules/@prisma/client/package.json"
+  printf 'model Thing {\n  id Int @id\n}\n' > "$WORK/$1/schema.prisma"
+}
+# run_generate <name>: the real script against that fixture; sets RC and ERR (stderr).
+run_generate() {
+  ERR="$(PRISMA_GENERATE_SVC_DIR="$WORK/$1/svc" PRISMA_SCHEMA_SRC="$WORK/$1/schema.prisma" node "$SCRIPT" 2>&1 >/dev/null)"; RC=$?
+}
+has() { if grep -qF -- "$2" <<<"$1"; then echo yes; else echo no; fi; }
+
+# CONTROL - no staging directory at all: generates, and leaves no .generate behind.
+fixture plain; run_generate plain
+cell "CONTROL KS-1497 with no .generate the script generates and removes its staging directory" "0/gone" "$RC/$([[ -e "$WORK/plain/svc/node_modules/.generate" || -L "$WORK/plain/svc/node_modules/.generate" ]] && echo left || echo gone)"
+
+# CONTROL - a stale REAL directory from an earlier interrupted run is reused and removed.
+fixture stale; mkdir -p "$WORK/stale/svc/node_modules/.generate"; echo old > "$WORK/stale/svc/node_modules/.generate/schema.prisma"
+run_generate stale
+cell "CONTROL KS-1497 a stale real .generate directory is reused and removed" "0/gone" "$RC/$([[ -e "$WORK/stale/svc/node_modules/.generate" ]] && echo left || echo gone)"
+
+# A symlinked .generate: refused before anything is written through it.
+fixture link; mkdir -p "$WORK/link/elsewhere"; ln -s "$WORK/link/elsewhere" "$WORK/link/svc/node_modules/.generate"
+run_generate link
+cell "RED KS-1497 a symlinked .generate is refused with exit 2" "2" "$RC"
+cell "RED KS-1497 the refusal for a symlinked .generate says so" "yes/yes" "$(has "$ERR" 'generate: ')/$(has "$ERR" 'symbolic link')"
+cell "RED KS-1497 nothing is written into the symlink's target" "0" "$(ls -A "$WORK/link/elsewhere" | wc -l | tr -d ' ')"
+
+# A .generate that is a FILE: a message, not a stack trace.
+fixture file; echo not-a-dir > "$WORK/file/svc/node_modules/.generate"
+run_generate file
+cell "RED KS-1497 a .generate that is a file is refused with exit 2" "2" "$RC"
+cell "RED KS-1497 the refusal for a .generate that is a file says so" "yes/yes" "$(has "$ERR" 'generate: ')/$(has "$ERR" 'is not a directory')"
+
+echo "ks1497_prisma_generate_refuses_a_bad_staging_dir: $PASS passed, $FAIL failed"
+[[ "$FAIL" -eq 0 && "$PASS" -eq 7 ]]
```
