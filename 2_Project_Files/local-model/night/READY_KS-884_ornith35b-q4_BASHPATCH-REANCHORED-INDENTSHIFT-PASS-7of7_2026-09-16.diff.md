# READY — KS-884 (`.githooks/pre-push`: the base-selection refs are FULLY QUALIFIED — `refs/heads/develop` / `refs/remotes/origin/develop` replace the bare `develop` / `origin/develop` in `_refs`, the three `rev-parse` guards and the `merge-base` at :160–:168; the stale-local fallback keeps `refs/remotes/origin/develop`) — Ornith ornith:35b (Q4_K_M) PASS 7/7 on r2 RE-CHECK, BASH_PATCH, tip develop M55 48e65c435 (G6 override verified against origin 0b25f823f), run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks884-ornith35b-night2 (recheck/)
# Source read by me (Wednesday): the applied region :157–:172 read with visible whitespace — indents 4/4/7/7/7/8/8/8/8 IDENTICAL to the tip's (the model wrote every line at +4; the harness shifted the '+' lines back — an accommodation the verdict names); all six brief '+' lines present (stripped compare — the builder stores them stripped); `grep -ci KS-884` on the applied hook = 0 (the r1 floating comment is gone; control: 27 `develop` hits); no other line touched. The model's suite `scripts/__tests__/pre_push_qualified_develop.test.sh` (76 lines, header synthesised — the headerless new-file dialect): at the tip rc 1 / 2 FAIL for the predicted reason (bare refs still present), after rc 0 / 4 pass; B6 SIX sibling suites that drive pre-push — no new failure. Accommodations named: section_1 REANCHORED on the '-' LINES with INDENT SHIFT -4; section_2 header SYNTHESISED.
# PR NOTES for the Sunday raising seat: (1) TWO files: the hook (six lines at :160–:168) + the NEW suite; KS-884 → Done. (2) The r1 output (2026-09-16_ks884-ornith35b-night) is SUPERSEDED — it carried an over-indented block and a floating `# KS-884` comment; use ONLY this r2 diff. (3) The hook is copied into `.git/hooks/` per clone — the PR body should say the change lands on the next `install-hooks` / clone, not on merge (the 09-09 guard-exclusion lesson's rule 6).

```diff
--- a/.githooks/pre-push
+++ b/.githooks/pre-push
@@ -157,15 +157,15 @@
     # DEPS MISSING — an environment condition presented as a gate result, and
     # indistinguishable from a real red without reading 13 legs of output.
     # -----------------------------------------------------------------------
-    _refs='develop origin/develop refs/remotes/origin/develop'
-    if git rev-parse --verify --quiet develop >/dev/null 2>&1 &&
-       git rev-parse --verify --quiet origin/develop >/dev/null 2>&1 &&
-       [ "$(git rev-parse develop)" != "$(git rev-parse origin/develop)" ] &&
-       git merge-base --is-ancestor develop origin/develop 2>/dev/null; then
+    _refs='refs/heads/develop refs/remotes/origin/develop'
+    if git rev-parse --verify --quiet refs/heads/develop >/dev/null 2>&1 &&
+       git rev-parse --verify --quiet refs/remotes/origin/develop >/dev/null 2>&1 &&
+       [ "$(git rev-parse refs/heads/develop)" != "$(git rev-parse refs/remotes/origin/develop)" ] &&
+       git merge-base --is-ancestor refs/heads/develop refs/remotes/origin/develop 2>/dev/null; then
         echo "[pre-push] KS-991: local 'develop' is BEHIND origin/develop — ignoring the" >&2
         echo "[pre-push]   stale ref for base selection. (git fetch origin develop:develop" >&2
         echo "[pre-push]   to refresh it.) origin/develop is still consulted below." >&2
-        _refs='origin/develop refs/remotes/origin/develop'
+        _refs='refs/remotes/origin/develop'
     fi
     for _ref in $_refs; do
         git rev-parse --verify --quiet "$_ref" >/dev/null 2>&1 || continue
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/pre_push_qualified_develop.test.sh
@@ -0,0 +1,75 @@
+#!/usr/bin/env bash
+# =============================================================================
+# STATIC PIN for KS-884 — bare-name resolution of `develop` in `.githooks/pre-push`.
+# The ticket's fixture measurement against a tag-vs-branch conflict is the runtime proof;
+# this suite pins the ABSENCE of the bare-name candidate statically so the fix cannot drift back.
+# =============================================================================
+set -uo pipefail
+TOTAL_CELLS=4
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+SUBJ="${PRE_PUSH_HOOK-$REPO_ROOT/.githooks/pre-push}"
+[ -f "$SUBJ" ] || { echo "FATAL: pre-push hook not found at $SUBJ" >&2; exit 2; }
+[ -r "$SUBJ" ] || { echo "FATAL: pre-push hook is not readable at $SUBJ" >&2; exit 2; }
+printf 'SUBJECT %s\n        sha256 %s\n\n' "$SUBJ" "$(shasum -a 256 "$SUBJ" | cut -d" " -f1)"
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+
+# ---------------------------------------------------------------------------
+# 🔴 CELL 1 — no `_refs=` line begins with a bare `develop` or `origin/develop`.
+# Untouched tip reports 2 hits; after the fix reports 0.
+# ---------------------------------------------------------------------------
+bare_hits="$(grep -cE "^[[:space:]]*_refs='(develop|origin/develop)" "$SUBJ" || true)"
+if [ "$bare_hits" = 0 ]; then
+    ok "no base-candidate list begins with a bare develop name (hits=$bare_hits)"
+else
+    bad "no base-candidate list begins with a bare develop name" \
+        "expected 0, got $bare_hits — $(grep -nE "^[[:space:]]*_refs='(develop|origin/develop)" "$SUBJ")"
+fi
+
+# ---------------------------------------------------------------------------
+# 🔴 CELL 2 — the candidate list names the branch by its full ref exactly once.
+# Untouched tip reports 0 hits; after the fix reports 1.
+# ---------------------------------------------------------------------------
+qual_hits="$(grep -cE "^[[:space:]]*_refs='refs/heads/develop refs/remotes/origin/develop'" "$SUBJ" || true)"
+if [ "$qual_hits" = 1 ]; then
+    ok "the candidate list names the branch by its full ref (hits=$qual_hits)"
+else
+    bad "the candidate list names the branch by its full ref" \
+        "expected 1, got $qual_hits — $(grep -nE "^[[:space:]]*_refs='refs/heads/develop refs/remotes/origin/develop'" "$SUBJ")"
+fi
+
+# ---------------------------------------------------------------------------
+# CONTROL CELL 3 — the KS-991 stale-ref guard is still present in the hook.
+# Green on both trees.
+# ---------------------------------------------------------------------------
+guard_hits="$(grep -c 'KS-991' "$SUBJ" || true)"
+if [ "$guard_hits" -ge 1 ]; then
+    ok "the KS-991 stale-ref guard is still present (hits=$guard_hits)"
+else
+    bad "the KS-991 stale-ref guard is still present" \
+        "expected >=1, got $guard_hits"
+fi
+
+# ---------------------------------------------------------------------------
+# CONTROL CELL 4 — the subject parses under bash without errors.
+# Green on both trees.
+# ---------------------------------------------------------------------------
+if bash -n "$SUBJ"; then
+    ok "pre-push parses (bash -n)"
+else
+    bad "pre-push parses (bash -n)" \
+        "$(bash -n "$SUBJ" 2>&1 | head -5 | tr '\n' ' ')"
+fi
+
+printf '\n  %d passed, %d failed (of %d cells)\n' "$pass" "$fail" "$TOTAL_CELLS"
+# A cell that never ran is not a pass — the ratio must add up.
+if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
+    printf '  INCOMPLETE — %d of %d cells ran\n' "$((pass + fail))" "$TOTAL_CELLS"
+    exit 1
+fi
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
