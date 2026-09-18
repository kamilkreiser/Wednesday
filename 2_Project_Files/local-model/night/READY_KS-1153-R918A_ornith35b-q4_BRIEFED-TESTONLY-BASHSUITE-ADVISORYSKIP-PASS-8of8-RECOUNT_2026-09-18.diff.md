# READY — KS-1153 R-918-A (Ornith, briefed, TEST_ONLY bash suite — the first) — PASS 8/8 (harness re-run) — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-18_ks1153-ornith35b-night2/out.md.checker/patch.diff` applied with `git apply --recount`.** The model's header reads `@@ -156,0 +156,9 @@` over 9 '+' + 1 trailing context line. **A STRICT apply ACCEPTS it and misplaces CASE 9 AFTER the suite's tally** (proven 18:3x) — the raising seat must use --recount and confirm CASE 9 sits BEFORE `echo "run_code_guards.test.sh — …"`.

**Held 2026-09-18 18:49 by the 14:4x Wednesday seat after a source read.** Tip `52df64f84`. r1 FAILED on a harness fault (strict apply of a miscounted header); the checker was fixed header-first and the SAME input re-run (not a rebrief).

## Source read
- CASE 9 + 2 cells in `Blockchain/Dev/scripts/__tests__/run_code_guards.test.sh`: a tree that is not a git checkout → `run-code-guards.sh --check-unreached` prints `SKIP (advisory)` and exits 0 (:145-148, read at 52df64f84; no existing cell reached it).
- 9 '+' lines IDENTICAL to the brief. T6: RC/MSG/ARM each red exactly their declared cells (assertions); controls green; product restored.
- **No product change.** Refs KS-1153. Test-only (bash), tier 2.
**HELD. Not raised.**

---
## The model's output, verbatim

```diff
--- a/Blockchain/Dev/scripts/__tests__/run_code_guards.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/run_code_guards.test.sh
@@ -156,0 +156,9 @@
+echo "=== CASE 9 - ADVISORY SKIP: a tree that is NOT a git checkout skips the census with rc 0 (KS-1153 R-918-A) ==="
+# Preflight leg 15 runs --check-unreached. From an export with no .git the census cannot enumerate tracked guards; it
+# must say so and step aside with rc 0 (run-code-guards.sh:145-148). Every fixture above is a git tree, so nothing
+# reached that arm. GIT_CEILING_DIRECTORIES stops git's upward search at $TMP, so the fixture is never inside a repo.
+F="$TMP/c9"; mkdir -p "$F/Blockchain/Dev/scripts"
+cp "$RUNNER" "$F/Blockchain/Dev/scripts/run-code-guards.sh"
+out9=$( cd "$F/Blockchain/Dev" && GIT_CEILING_DIRECTORIES="$TMP" bash scripts/run-code-guards.sh --check-unreached 2>&1; echo "rc=$?" )
+check "a non-git tree: the census exits 0" "rc=0" "$(printf '%s\n' "$out9" | tail -1)"
+check "a non-git tree: the census prints the advisory SKIP line" "yes" "$(printf '%s\n' "$out9" | grep -q '^SKIP (advisory)' && echo yes || echo no)"
 echo
```
