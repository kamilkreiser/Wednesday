# READY — KS-1081-NEITHERTEMPLATE-1 (Ornith, briefed, test_only, modify · bash) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1081-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 06:06 2026-09-23). Checker T3 (verbatim from checker.out): `PASS T3 diff applies at the tip (strict git apply --check)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1081-ornith35b-night2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_feed17-drafter-precheck/NEITHERTEMPLATE/out.md.checker/patch.diff` rc 0, Wednesday 06:0x seat 2026-09-23).

**Held 06:06 2026-09-23 by Wednesday 06:0x seat 2026-09-23 after a source read (hold_ready.py — every clause below is built from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1081-ornith35b-night2/out.md.checker`, not typed).** Tip `2bc5ccf63b8c40911afb568b03cace066238ffcf`. Touches ONE file: `Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh` (modify). `+` lines 14 ordered-equal to the brief's `expected_plus` (ASCII); `-` lines 0 == `must_remove`. Green at the tip: 7/7 cells. Tampers (1), each red exactly its declared set with controls green and the product file restored by bytes (T6/T7/T8):
- `GUARDGONE` → red exactly ['a tree carrying NEITHER template']

**PR NOTES for the raise seat:** TEST-ONLY — zero product bytes; one file, apply `patch.diff` strictly at the tip (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` and state it). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1081-ornith35b-night2/input.json`. Brief: `night/briefs/KS-1081-NEITHERTEMPLATE-1.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-22_ks1081-ornith35b-night2/checker.out`.

```diff
--- a/Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/bootstrap_env_canonical_template.test.sh
@@ -88,2 +88,16 @@
 echo ""
+# KS-1081 (gate 19C CANONENV-NEITHER, #1191): a tree carrying NEITHER template must be
+# refused by the pre-flight guard (bootstrap-env.sh:68-71) with its named message and
+# rc 1 - not die later on a failed cp. Built and run here so the block stays contiguous.
+NEITHER="$SCRATCH_ROOT/neither/Blockchain/Dev"
+mkdir -p "$NEITHER/scripts"
+cp "$BOOTSTRAP" "$NEITHER/scripts/bootstrap-env.sh"
+cp "$ENV_SH" "$NEITHER/scripts/stack_env.sh"
+env -u SECUURA_STACK_SLOT -u STACK_SLOT -u POSTGRES_EXTERNAL_PORT -u REDIS_EXTERNAL_PORT HOME="$HOME" PATH="$PATH" bash "$NEITHER/scripts/bootstrap-env.sh" >"$NEITHER/bootstrap.log" 2>&1
+NEITHER_RC=$?
+if [[ "$NEITHER_RC" -eq 1 ]] && grep -qF 'No env template found' "$NEITHER/bootstrap.log"; then
+  echo "PASS: a tree carrying NEITHER template is refused by name (rc 1, No env template found)"; PASS=$((PASS+1))
+else
+  echo "FAIL: a tree carrying NEITHER template: rc=$NEITHER_RC, named refusal present=$(grep -qF 'No env template found' "$NEITHER/bootstrap.log" && echo yes || echo NO) (want rc 1 and the message)"; FAIL=$((FAIL+1))
+fi
 echo "bootstrap_env_canonical_template: $PASS passed, $FAIL failed"
```
