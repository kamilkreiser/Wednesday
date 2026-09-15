# READY — KS-972 (start-secuura.sh Credentials banner :712: the retired admin@secuura.com / admin123 line → a pointer to systemTest/fixtures/provision-actors.ts, KS-966) — Ornith ornith:35b (Q4_K_M) PASS 7/7 FIRST SAMPLE, BASH_PATCH, tip develop M55 48e65c435 (G6 override verified against origin 0b25f823f), run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks972-ornith35b-night
# Source read by me (Wednesday): the product diff is the brief's one -/+ pair at :712 byte-for-byte (REANCHORED from the model's -709,7 header); `grep -n admin123` on the APPLIED script = ONE hit, :614 — the admin login CHECK, which is OUT OF SCOPE here (KS-966 item 3's sweep of scripts that READ the fallback). The model's suite: four cells (banner no longer prints admin123 · banner names provision-actors.ts · CONTROL the issuer line untouched · CONTROL bash -n), the closing seven lines present; at the tip 2 red for the predicted reason, after 4/4 green. Accommodations named: REANCHORED product section; one `+` restored in the new file.
# PR NOTES for the Sunday raising seat: (1) TWO files: the banner line + the NEW suite scripts/__tests__/start_secuura_banner.test.sh (reached by run-shell-suites.sh's glob — verify with --list); KS-972 → Done (its 'Suggested fix' is exactly this: print the mechanism, not a value). (2) The login CHECK at :610–:620 still posts admin@secuura.com / admin123 and will report a failed admin login on every start — that is KS-966 item 3 (scripts that read the fallback), not this ticket; say so in the PR body so a reviewer does not read the banner fix as the whole story. (3) The ticket's 'Project: <compose default>' aside is untouched (not the subject).

```diff
--- a/Start_Up/start-secuura.sh
+++ b/Start_Up/start-secuura.sh
@@ -709,7 +709,7 @@
 echo ""
 echo -e "  ${BOLD}Credentials:${NC}"
 echo -e "    Issuer:  demo@secuura.io / demo123"
-echo -e "    Admin:   admin@secuura.com / admin123"
+echo -e "    Admin:   provisioned per run — see systemTest/fixtures/provision-actors.ts (KS-966: no shared admin credential is published)"
 echo ""
 # KS-666: state, on screen, who now holds this stack — so the next person does
 # not have to run a destructive command to discover it is occupied.
--- /dev/null
+++ b/Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh
@@ -0,0 +1,78 @@
+#!/usr/bin/env bash
+# =============================================================================
+# TESTS for Start_Up/start-secuura.sh Credentials banner (KS-972)
+# =============================================================================
+# The defect: line 712 still prints `Admin: admin@secuura.com / admin123` — a
+# login retired by PR #888. Every operator reads it as valid; every attempt to
+# use it returns 401. This task replaces the value with a pointer to where the
+# admin is actually provisioned per run and adds one shell suite proving the
+# change took effect without touching any other line.
+#
+# Usage: bash Blockchain/Dev/scripts/__tests__/start_secuura_banner.test.sh
+# =============================================================================
+set -uo pipefail
+TOTAL_CELLS=4
+
+HERE="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
+REPO_ROOT="$(cd "$HERE/../../../.." && pwd)"
+SUBJ="${START_SECUURA_SH-$REPO_ROOT/Start_Up/start-secuura.sh}"
+[ -f "$SUBJ" ] || { echo "FATAL: start-secuura.sh not found at $SUBJ" >&2; exit 2; }
+[ -r "$SUBJ" ] || { echo "FATAL: START_SECUURA_SH is not readable at $SUBJ" >&2; exit 2; }
+printf 'SUBJECT %s\n        sha256 %s\n\n' "$SUBJ" "$(shasum -a 256 "$SUBJ" | cut -d" " -f1)"
+
+pass=0; fail=0
+ok()  { printf '  ok   %s\n' "$1"; pass=$((pass + 1)); }
+bad() { printf '  FAIL %s\n     %s\n' "$1" "$2"; fail=$((fail + 1)); }
+
+# ---------------------------------------------------------------------------
+# CELL 1 — RED. Untouched script has exactly one hit of the retired credential
+# in its own source. After the fix there must be zero hits.
+# ---------------------------------------------------------------------------
+banner_hits="$(grep -c 'Admin:.*admin123' "$SUBJ" || true)"
+if [ "$banner_hits" = 0 ]; then
+  ok "the Credentials banner no longer prints the retired admin credential ($banner_hits hits)"
+else
+  bad "the Credentials banner no longer prints the retired admin credential" \
+      "found $banner_hits hit(s) of 'Admin:.*admin123' in $SUBJ"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 2 — RED. The new mechanism-pointer text must appear exactly once.
+# ---------------------------------------------------------------------------
+mech_hits="$(grep -c 'Admin:.*provision-actors.ts' "$SUBJ" || true)"
+if [ "$mech_hits" = 1 ]; then
+  ok "the banner names the provisioning mechanism instead of a value ($mech_hits hit)"
+else
+  bad "the banner names the provisioning mechanism instead of a value" \
+      "expected 1 hit, got $mech_hits"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 3 — CONTROL (green on both trees). Issuer line untouched.
+# ---------------------------------------------------------------------------
+issuer_hits="$(grep -c 'Issuer:  demo@secuura.io / demo123' "$SUBJ" || true)"
+if [ "$issuer_hits" = 1 ]; then
+  ok "CONTROL — issuer line untouched (demo@secuura.io still authenticates)"
+else
+  bad "CONTROL — issuer line untouched" \
+      "expected 1 hit, got $issuer_hits"
+fi
+
+# ---------------------------------------------------------------------------
+# CELL 4 — CONTROL (green on both trees). Script parses under bash -n.
+# ---------------------------------------------------------------------------
+if bash -n "$SUBJ" >/dev/null 2>&1; then
+  ok "start-secuura.sh parses (bash -n)"
+else
+  bad "start-secuura.sh parses (bash -n)" \
+      "$(bash -n "$SUBJ" 2>&1 | head -5 | tr '\n' ' ')"
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
