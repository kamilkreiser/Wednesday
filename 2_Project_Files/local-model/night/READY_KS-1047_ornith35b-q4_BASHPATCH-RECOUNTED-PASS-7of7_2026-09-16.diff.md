# READY — KS-1047 (`.githooks/pre-push` :268 — the KS-691 rationale comment enumerated the stack-dependent legs as "(3, 4, 7)" while the measured set is 3, 4, 8; the ticket's better fix taken: the comment now POINTS at the preflight verdict's SKIPPED line (KS-1046) instead of enumerating, so it cannot drift again) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE (r1), BASH_PATCH, tip develop M55 48e65c435 (G6 override verified against origin), run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1047-ornith35b-night
# Source read by me (Wednesday): the product hunk's `-` and `+` lines are the brief's BYTE-FOR-BYTE (grep of the brief's `+` sentence in out.md = 1; the applied `after.sh` :268 carries it, `(3, 4, 7)` = 0 after / 1 at the tip, `KS-1046` = 1 after / 0 at the tip, the `KS-691` anchor = 1 on both — read from the checker's after.sh and red_first/green_after outputs, not from the verdict line). Two harness accommodations, both NAMED in checker.out: section_1 needed `--recount --ignore-whitespace`; the NEW-FILE test's hunk header declared 55 lines for a 74-line body (RECOUNTED 55 -> 74 — the model's stable new-file undercount) and one `# ===` banner line had its `+` marker dropped (restored). The model's suite: 4 cells (two 🔴 + two CONTROL) exactly as briefed; at the tip rc 1 / 2 FAIL for the predicted reasons (count=1 expected 0; count=0 expected 1), after 4/4; B6 six sibling suites clean.
# PR NOTES for the Sunday raising seat: (1) TWO files: `.githooks/pre-push` (ONE comment line, :268) + the NEW suite `Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh` (reads the subject at `$REPO_ROOT/.githooks/pre-push`, `PRE_PUSH_HOOK` override); KS-1047 → Done. (2) No behaviour change — a comment only; `bash -n` is a cell. (3) The ticket named `:230`; at M55 the comment sits at `:268` (grep: exactly one hit) — say so in the PR body. (4) Apply the RECOUNTED section_2 as held in this READY (the as-written header would drop the tail silently).

```diff
--- a/.githooks/pre-push
+++ b/.githooks/pre-push
@@ -265,7 +265,7 @@ echo "[pre-push] Blockchain/Dev changes detected → running preflight gate (bypass
 # Safe on macOS bash 3.2: the script uses no bash-4 constructs (no mapfile/readarray,
 # no associative arrays, no ${x^^}).
-# KS-691: source slot-target.sh first so the stack-dependent legs (3, 4, 7) probe
+# KS-691: source slot-target.sh first so the stack-dependent legs (the ones the preflight verdict lists as SKIPPED when the stack is down — KS-1046; not enumerated here, an enumeration drifts) probe
 # THIS slot's gateway. preflight.sh defaults GATEWAY to localhost:6882 (slot 1),
 # so from any other slot those legs either silently SKIP (slot 1 down) — the push
 # passes having probed nothing — or probe SLOT 1 and report success for a stack
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh
@@ -0,0 +1,74 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for .githooks/pre-push line :268 comment — stale leg enumeration gone, pointer present (KS-1047)
+# =============================================================================
+# The defect at tip `48e65c435`: line 268 enumerates legs "(3, 4, 7)" which is
+# wrong (measured 2026-09-09 they are 3, 4, 8). The fix drops the enumeration
+# and points at the verdict line instead. These four cells prove that.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/pre_push_stack_legs_comment.test.sh
+# =============================================================================
+set -uo pipefail
+TOTAL_CELLS=4
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+SUBJ="${PRE_PUSH_HOOK-$REPO_ROOT/.githooks/pre-push}"
+[ -f "$SUBJ" ] || { echo "FATAL: pre-push hook not found at $SUBJ" >&2; exit 2; }
+[ -r "$SUBJ" ] || { echo "FATAL: PRE_PUSH_HOOK is not readable at $SUBJ" >&2; exit 2; }
+printf 'SUBJECT %s\n        sha256 %s\n\n' "$SUBJ" "$(shasum -a 256 "$SUBJ" | cut -d" " -f1)"
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+
+# ---------------------------------------------------------------------------
+# CELL 1 — KS-1047 RED. THE STALE ENUMERATION IS GONE.
+# ---------------------------------------------------------------------------
+stale_hits="$(grep -c '(3, 4, 7)' "$SUBJ" || true)"
+if [ "$stale_hits" = 0 ]; then
+  ok "the stale leg enumeration (3, 4, 7) is gone from pre-push"
+else
+  bad "the stale leg enumeration (3, 4, 7) is gone from pre-push" \
+      "count=$stale_hits (expected 0)"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 2 — KS-1047 RED. THE COMMENT POINTS AT THE VERDICT LINE (KS-1046), NOT LEGS.
+# ---------------------------------------------------------------------------
+ptr_hits="$(grep -c 'KS-1046' "$SUBJ" || true)"
+if [ "$ptr_hits" = 1 ]; then
+  ok "the comment points at the verdict line (KS-1046) instead of enumerating legs"
+else
+  bad "the comment points at the verdict line (KS-1046) instead of enumerating legs" \
+      "count=$ptr_hits (expected 1)"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 3 — CONTROL. THE KS-691 RATIONALE COMMENT IS STILL THERE.
+# ---------------------------------------------------------------------------
+anchor_hits="$(grep -c 'KS-691: source slot-target.sh first so the stack-dependent legs' "$SUBJ" || true)"
+if [ "$anchor_hits" = 1 ]; then
+  ok "the KS-691 rationale comment anchor is still present in pre-push"
+else
+  bad "the KS-691 rationale comment anchor is still present in pre-push" \
+      "count=$anchor_hits (expected 1)"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 4 — CONTROL. PRE-PUSH PARSes (bash -n).
+# ---------------------------------------------------------------------------
+if bash -n "$SUBJ" >/dev/null 2>&1; then
+  ok "pre-push parses (bash -n)"
+else
+  bad "pre-push parses (bash -n)" "$(bash -n "$SUBJ" 2>&1 | head -5 | tr '\n' ' ')"
+fi
+
+printf '\n  %d passed, %d failed (of %d cells)\n' "$pass" "$fail" "$TOTAL_CELLS"
+# A cell that never ran is not a pass: the ratio must add up.
+if [ "$((pass + fail))" -ne "$TOTAL_CELLS" ]; then
+  printf '  INCOMPLETE — %d of %d cells ran\n' "$((pass + fail))" "$TOTAL_CELLS"
+  exit 1
+fi
+[ "$fail" -eq 0 ] || exit 1
+exit 0
```
