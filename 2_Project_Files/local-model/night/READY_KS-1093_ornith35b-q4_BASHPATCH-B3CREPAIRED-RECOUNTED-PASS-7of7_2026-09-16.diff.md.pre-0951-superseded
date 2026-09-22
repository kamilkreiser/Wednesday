# READY — KS-1093 (P0 — `check-stack-safety.sh` §6f false red once a real Playwright run exists: `git check-ignore` refuses any path BEYOND the `results/latest-slot<N>` SYMLINK (rc 128, read as "not ignored"); the probe now names the symlink ITSELF, plus a two-line comment above `PW_STAMP=` naming the rule) — Ornith ornith:35b (Q4_K_M) PASS 7/7 on r3 (r1: the brief declared `RES=` in prose → LOAD error; r2: the model's insert-after dialect deleted the anchor line :321, caught by the NEW B3c; r3: same dialect, REPAIRED by B3c), BASH_PATCH, tip develop M55 48e65c435 (G6 override verified against origin), run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1093-ornith35b-night3
# Source read by me (Wednesday): the applied `after.sh` is BYTE-IDENTICAL (`cmp`) to the copy Wednesday fixed by hand and measured in a scratch clone BEFORE the brief (the defect reproduced at this tip: `::error::latest-slot4/index.html is NOT gitignored on slot 4`, rc 1; the fix → rc 0 `100 shared-stack safety invariants hold` with the symlink present AND on a clean tree). After: `latest-slot${slot}/index.html` 0, `latest-slot${slot}"` 1, the :321 sentence present 1, `KS-1093` 1. THE SECTION HELD HERE IS THE B3c-REPAIRED ONE (the model marked :321 `-`; B3c restored it as context and named the accommodation; `section_1.diff.pre-b3c` beside it is the model's as-written). Two more accommodations named by the checker: section_1 `--recount --ignore-whitespace`; the new-file header RECOUNTED 65 -> 67. The model's suite: 6 cells as briefed (two text reds; one BEHAVIOURAL red that creates a `results/latest-slot4` symlink under the repo's ignored `results/`, runs the gate, and removes exactly what it created; three controls incl. the git mechanism in a mktemp repo): at the tip `3 passed, 3 failed` for the predicted reasons, after 6/6; B6 one sibling suite clean.
# PR NOTES for the Sunday raising seat: (1) TWO files: `Blockchain/Dev/scripts/check-stack-safety.sh` (:321 gains two comment lines; :328 the probe) + the NEW suite `Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh`; KS-1093 → Done. (2) Behaviour: §6f's fourth Playwright shape is now probed as the symlink path itself — the blanket `results/` rule at `systemTest/playwright/.gitignore:17` covers it on both a clean tree and a run tree; nothing else in the gate changes (100 invariants before and after). (3) NIT, not verdict-changing: the model's suite omits the reference's set-but-empty refusal block for `CHECK_STACK_SAFETY_SH` (the `[ -f ]`/`[ -r ]` FATAL lines are present) — add the four lines if the raising seat wants shape parity. (4) CELL 4 writes under `systemTest/playwright/results/` ONLY when no `latest-slot4` exists, and removes only what it created (`rm` on the symlink + the one index.html it made, `rmdir` on the dir); on a machine with a real run present it uses the real symlink and removes nothing. (5) Apply the RECOUNTED section_2 and the B3c-REPAIRED section_1 as held in this READY.

```diff
--- a/Blockchain/Dev/scripts/check-stack-safety.sh
+++ b/Blockchain/Dev/scripts/check-stack-safety.sh
@@ -318,15 +318,17 @@ PW_STAMP="2026-01-01T00-00-00-000Z"
 # Honest limit, measured on #803 review: `systemTest/playwright/.gitignore` carries a blanket
 # `results/`, so every `results/...` probe passes by that line alone — they prove the blanket
 # holds, not the suffix. The `.auth-*/` probe is the one that tests a suffix pattern, and it is the
 # one holding a bearer token, which is why it is here for every slot and not just slot 3.
+# KS-1093: `latest-slot<N>` is a SYMLINK once a run exists, and `git check-ignore` refuses any path
+# beyond a symlink (fatal, rc 128 — read as "not ignored"). Probe the symlink ITSELF, never through it.
 PW_STAMP="2026-01-01T00-00-00-000Z"
 for slot in 1 2 3 4; do
   for artifact in \
     "$REPO/systemTest/playwright/results/playwright-report-ks-682-${PW_STAMP}-slot${slot}/index.html" \
     "$REPO/systemTest/playwright/results/test-results-ks-682-${PW_STAMP}-slot${slot}/.last-run.json" \
     "$REPO/systemTest/playwright/results/har-ks-682-${PW_STAMP}-slot${slot}/1.har" \
-    "$REPO/systemTest/playwright/results/latest-slot${slot}/index.html" \
+    "$REPO/systemTest/playwright/results/latest-slot${slot}" \
     "$REPO/systemTest/playwright/.auth-ks-682-slot${slot}/token.json" \
     "$REPO/systemTest/playwright/.auth-ks-682-slot${slot}/state.json"; do
     if git -C "$REPO" check-ignore -q "$artifact" 2>/dev/null; then ok; else
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh
@@ -0,0 +1,67 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Blockchain/Dev/scripts/check-stack-safety.sh — latest-slot symlinks (KS-1093)
+# =============================================================================
+# The defect: with `systemTest/playwright/results/latest-slot4` a symlink,
+# the gate prints `::error::latest-slot4/index.html is NOT gitignored on slot 4 (KS-682).`
+# and exits 1 because `git check-ignore` refuses paths beyond a symbolic link.
+# This suite proves E1+E2 fix that without weakening what is proven.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/check_stack_safety_latest_slot_symlink.test.sh
+# =============================================================================
+set -uo pipefail
+TOTAL_CELLS=6
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+SUBJ="${CHECK_STACK_SAFETY_SH-$REPO_ROOT/Blockchain/Dev/scripts/check-stack-safety.sh}"
+[ -f "$SUBJ" ] || { echo "FATAL: check-stack-safety.sh not found at $SUBJ" >&2; exit 2; }
+[ -r "$SUBJ" ] || { echo "FATAL: CHECK_STACK_SAFETY_SH is not readable at $SUBJ" >&2; exit 2; }
+printf 'SUBJECT %s\n        sha256 %s\n\n' "$SUBJ" "$(shasum -a 256 "$SUBJ" | cut -d" " -f1)"
+
+WORK="$(mktemp -d "${TMPDIR:-/tmp}/ks1093.XXXXXX")"
+trap 'rm -rf "$WORK"' EXIT
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+RES="$REPO_ROOT/systemTest/playwright/results"
+
+# CELL 1 — RED at the tip: the through-symlink probe is gone.
+through_hits="$(grep -c 'results/latest-slot${slot}/index.html' "$SUBJ" || true)"
+if [ "$through_hits" -eq 0 ]; then ok "the probe no longer reads THROUGH the latest-slot symlink (index.html)"; else bad "the probe no longer reads THROUGH the latest-slot symlink (index.html)" "count=$through_hits (expected 0)"; fi
+# CELL 2 — RED at the tip: the probe of the symlink itself is present.
+self_hits="$(grep -c 'results/latest-slot${slot}"' "$SUBJ" || true)"
+if [ "$self_hits" -eq 1 ]; then ok "the probe names the latest-slot symlink ITSELF"; else bad "the probe names the latest-slot symlink ITSELF" "count=$self_hits (expected 1)"; fi
+# CELL 3 — CONTROL on a clean checkout: the gate exits 0 on this tree as found (nothing created yet).
+bash "$SUBJ" > "$WORK/clean.out" 2>&1; rc_clean=$?
+if [ "$rc_clean" -eq 0 ]; then ok "the gate exits 0 on this tree as found"; else bad "the gate exits 0 on this tree as found" "rc=$rc_clean: $(grep '::error::' "$WORK/clean.out" | head -2 | tr '\n' ' ')"; fi
+# CELL 4 — RED at the tip: with a latest-slot4 SYMLINK present the gate still exits 0 and names no latest-slot error.
+made_results=0; made_link=0
+[ -d "$RES" ] || { mkdir -p "$RES"; made_results=1; }
+if [ ! -e "$RES/latest-slot4" ] && [ ! -L "$RES/latest-slot4" ]; then
+  mkdir -p "$RES/playwright-report-ks-1093-slot4"; : > "$RES/playwright-report-ks-1093-slot4/index.html"
+  ln -s playwright-report-ks-1093-slot4 "$RES/latest-slot4"; made_link=1
+fi
+bash "$SUBJ" > "$WORK/symlink.out" 2>&1; rc_link=$?
+link_errors="$(grep -c '::error::latest-slot' "$WORK/symlink.out" || true)"
+if [ "$made_link" -eq 1 ]; then rm "$RES/latest-slot4"; rm "$RES/playwright-report-ks-1093-slot4/index.html"; rmdir "$RES/playwright-report-ks-1093-slot4"; fi
+if [ "$made_results" -eq 1 ]; then rmdir "$RES" 2>/dev/null || true; fi
+if [ "$rc_link" -eq 0 ] && [ "$link_errors" -eq 0 ]; then ok "with a latest-slot4 symlink present the gate exits 0 and names no latest-slot error"; else bad "with a latest-slot4 symlink present the gate exits 0 and names no latest-slot error" "rc=$rc_link latest-slot errors=$link_errors"; fi
+# CELL 5 — CONTROL: the git mechanism the fix rests on, in a throwaway repo (through the symlink: rc 128; the symlink itself: rc 0).
+git -C "$WORK" init -q; printf 'results/\n' > "$WORK/.gitignore"
+mkdir -p "$WORK/results/playwright-report-x-slot4"; ln -s playwright-report-x-slot4 "$WORK/results/latest-slot4"
+git -C "$WORK" check-ignore -q results/latest-slot4/index.html 2>/dev/null; rc_through=$?
+git -C "$WORK" check-ignore -q results/latest-slot4 2>/dev/null; rc_self=$?
+if [ "$rc_through" -eq 128 ] && [ "$rc_self" -eq 0 ]; then ok "git check-ignore refuses a path beyond a symlink (rc 128) and accepts the symlink itself (rc 0)"; else bad "git check-ignore refuses a path beyond a symlink (rc 128) and accepts the symlink itself (rc 0)" "through=$rc_through self=$rc_self"; fi
+# CELL 6 — CONTROL: the subject parses.
+if bash -n "$SUBJ" >/dev/null 2>&1; then ok "check-stack-safety.sh parses (bash -n)"; else bad "check-stack-safety.sh parses (bash -n)" "$(bash -n "$SUBJ" 2>&1 | head -5 | tr '\n' ' ')"; fi
+
+printf '\n  %d passed, %d failed (of %d cells)\n' "$pass" "$fail" "$TOTAL_CELLS"
+# A cell that never ran is not a pass (KS-1093 round 2): the ratio must add up.
+if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
+  printf '  INCOMPLETE — %d of %d cells ran\n' "$((pass + fail))" "$TOTAL_CELLS"
+  exit 1
+fi
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
