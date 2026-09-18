# KS-936 (golden, bash test_only arm): pin that the GATE DOES NOT PASS on the post-API path — orchestrate_jobs.test.sh CELL 13

File: `Blockchain/Dev/scripts/__tests__/orchestrate_jobs.test.sh`
Tip: `921d201e358f572d6d19e84a5403a176b35e1f77`

The real merged change is Secuura #875 (`c342a62e9`, parent `921d201e3`): test-only, it adds a `post-api-unreadable` fixture
mode and CELL 13. This brief is that change with its five em-dashes written as ASCII `-` and its two blank '+' lines
dropped (the builder refuses non-ASCII and blank '+' lines in a modify-in-place fence). Product: `Blockchain/Testing/ci/orchestrate.sh`,
never edited.

## The exact change

```diff
@@ -59,3 +59,3 @@
 build_fixture() {
-  # $2 = all | one-missing | one-unreadable   (Stage-1 job condition)
+  # $2 = all | one-missing | one-unreadable | post-api-unreadable   (job condition)
   # $3 = exec | noexec | absent | failing | badshebang | unreadable  (Stage-2 tool)
@@ -111,2 +111,8 @@
       chmod 000 "$root/Testing/jobs/$j.sh"
+    # KS-936: `post-api-unreadable` makes 06-tenant-isolation mode-000. That job
+    # is reachable ONLY from the post-API loop (orchestrate.sh:125); Stage 1's
+    # list at :104 does not contain it. So this fixture drives the post-API path
+    # and nothing else - the path CELL 11 left inferred.
+    elif [ "$mode" = post-api-unreadable ] && [ "$j" = 06-tenant-isolation ]; then
+      chmod 000 "$root/Testing/jobs/$j.sh"
     else
@@ -351,1 +357,42 @@
+# ---------------------------------------------------------------------------
+# CELL 13 - KS-936. THE GATE MUST NOT PASS on the post-API path.
+#
+# Why this is not a restatement of CELLS 10 and 11. `require_job` delegates to
+# the same `require_script`, so the CODE is shared and CELL 11 already drives it
+# on Stage 1. What differs is the OBSERVABLE, and it is the one that matters:
+#
+#   Stage 1 pre-fix      -> rc NON-ZERO. CELL 11 pins that refusal.
+#   post-API loop pre-fix -> rc 0. A GATE PASS, with "06-tenant-isolation exited
+#                            non-zero (continuing)" said about a job that never
+#                            ran. Nothing pinned that.
+#
+# A future change that stopped the post-API loop refusing would leave CELLS 10
+# and 11 green while a run that could not start a security job reported success.
+# That is KS-868, the parent defect, exactly. So this cell asserts THE GATE DOES
+# NOT PASS - not merely that a refusal appears somewhere in the output.
+#
+# It sits after CELL 12 rather than beside CELLS 10/11 so the existing cell
+# numbers keep their meaning; KS-941 cites CELL 12 by number.
+# ---------------------------------------------------------------------------
+build_fixture "$WORK/postapiunread" post-api-unreadable
+PA_UNREAD_JOB="$WORK/postapiunread/Testing/jobs/06-tenant-isolation.sh"
+if [ -r "$PA_UNREAD_JOB" ]; then
+  # Same precondition guard CELLS 10 and 11 carry: root defeats mode-000, and a
+  # cell that cannot discriminate must not report a pass.
+  bad "an UNREADABLE post-API job makes the GATE NOT PASS" \
+      "the mode-000 fixture is STILL READABLE (running as root?) - this cell cannot discriminate and is not reporting a pass"
+else
+  rc_pa="$(run_orchestrator "$WORK/postapiunread")"
+  out_pa="$(cat "$WORK/postapiunread/out.txt")"
+  if [ "$rc_pa" != 0 ] \
+     && printf '%s' "$out_pa" | grep -q 'NOT READABLE' \
+     && printf '%s' "$out_pa" | grep -q '06-tenant-isolation' \
+     && ! printf '%s' "$out_pa" | grep -q '06-tenant-isolation exited non-zero'; then
+    ok "an UNREADABLE post-API job makes the GATE NOT PASS (rc=$rc_pa), REFUSES by name, and does NOT claim the job ran - the path CELL 11 left inferred is now DRIVEN"
+  else
+    bad "an UNREADABLE post-API job makes the GATE NOT PASS, REFUSES by name, and claims nothing about having run" \
+        "rc=$rc_pa (rc=0 here is the pre-fix GATE PASS this cell exists to catch), output: $(tail -5 "$WORK/postapiunread/out.txt" | tr '\n' ' ')"
+  fi
+fi
+chmod 644 "$PA_UNREAD_JOB" 2>/dev/null
 printf '\n  %d passed, %d failed\n' "$pass" "$fail"
```

## Cells

- `cell4` = `a missing job makes the run REFUSE loudly, BY NAME, and exit non-zero`
- `cell11` = `an UNREADABLE Stage-1 job REFUSES by name and exits non-zero`
- `cell13` = `an UNREADABLE post-API job makes the GATE NOT PASS`

## Tampers

### P1 post-API loop stops refusing an unreadable job (the #875 commit's "tamper 1cd260b7, post-API only")
File: `Blockchain/Testing/ci/orchestrate.sh`
Line: 129
From:
```
  if require_job "$job"; then
```
To:
```
  if true; then
```
Reds: `cell13`

### S1 Stage-1 loop stops refusing (the commit's "tamper f6cfeff1, Stage-1 only")
File: `Blockchain/Testing/ci/orchestrate.sh`
Line: 105
From:
```
  if require_job "$job"; then
```
To:
```
  if true; then
```
Reds: `cell4`, `cell11`

## Controls

- `CONTROL — every job present: the run exits 0 and all 7 fixture jobs RAN`
- `an UNREADABLE Stage-2 tool REFUSES by name`
- `SELF and RUN_DIR are BOUND in a child process`
