# READY — KS-766 (Secuura) base-image-watch.sh: the DB-age producer isolated + two self-test checks (QA F-5 producer half)

- Model: Spark (DeepSeek V4 Flash) via LM_BACKEND=spark, round 1 of the counter; run dir `runs/2026-09-26_ks766-spark/`
- Brief: `night/briefs/KS-766/KS-766.md` (anchors verified by Wednesday at d7cdecf1; golden applies with patch -F0 rc 0)
- Tip: d7cdecf1d2eef7dde26dd23120e80c9db3f0e4a9 via the G6 override against origin develop df5e9f5da6d2 (compare: 0 files under Blockchain/Dev/scripts/)
- Model call (from model.log): lm_call: ok backend=spark wall=61.97s prompt_tokens=23857 eval_count=1965 tok/s(end-to-end)=31.71 think=0 thinking_chars=0 done_reason=stop unfenced_wrapped=False content_chars=6457
- Checker: `tasks/bash_patch/checker.sh` self-testing mode (arms 10/10 re-run by Wednesday before this round)
- Checker lines, copied:
    SUMMARY files=1 mode=self_testing apply_mode=strict tip=rc0/20P/0F red=rc12/20P/2F green=rc0/22P/0F scratch=/var/folders/xl/p96z5mmd3lzcn3pt8t6djkl40000gn/T/bash_selftest.L9rNA8 (kept, never deleted)
    RESULT: PASS (self-testing, all S-assertions)
- Wednesday's source read: the patch is identical to the verified golden in every hunk header, '-', '+' and context line (diff rc 0).
- NOT covered: no docker/network run of the real trivy path (the self-test drives the producer on JSON only); shellcheck not installed; legs 3/4/8 n/a.

```diff
--- a/Blockchain/Dev/scripts/base-image-watch.sh
+++ b/Blockchain/Dev/scripts/base-image-watch.sh
@@ -429,7 +429,47 @@
 sys.exit(11)
 ' "$report" "$BASELINE_IMAGE" "$BASELINE_CVE" "$ref_image" "$db_age" "$max_db_age"
 }
-
+# --- the DB-age PRODUCER, isolated so the self-test can drive it (KS-766) ----
+# Reads `trivy version --format json` on stdin and prints the age in hours, the
+# sentinel "future" for a stamp ahead of the clock, or "" when unreadable. The
+# caller measures with this; decide() only judges what it is handed.
+db_age_from_version_json() {
+    python3 -c '
+import json,sys,datetime,re
+try:
+    d = json.load(sys.stdin)
+    ts = (d.get("VulnerabilityDB") or {}).get("UpdatedAt")
+    if not ts:
+        print(""); raise SystemExit
+    ts = ts.replace("Z", "+00:00")
+    # QA F-8. trivy stamps RFC3339 with NANOSECOND precision. On a host running
+    # python < 3.11 `fromisoformat` rejects that outright, so this whole block
+    # raised, printed "", and decide() read the age as unknown — which makes the
+    # gate PERMANENTLY indeterminate the moment a residual clears, silently
+    # disabling the one verdict it exists to produce. It fails safe, which is
+    # why nothing noticed. Truncate the fraction to microseconds first.
+    ts = re.sub(r"\.(\d{6})\d+", r".\1", ts)
+    upd = datetime.datetime.fromisoformat(ts)
+    now = datetime.datetime.now(datetime.timezone.utc)
+    age = (now - upd).total_seconds() / 3600
+    # QA F-5. A FUTURE stamp (clock skew, a bad cache) was CLAMPED to 0 and then
+    # printed inside a CLEARED verdict as "the vulnerability DB is 0.0h old" —
+    # i.e. the freshest possible reading, produced by the one input that means
+    # the clock cannot be trusted at all. That is the worst direction for this
+    # value to fail in: it is the sentence an operator reads before running the
+    # ACR leg against the live registry.
+    #
+    # A future stamp is now its OWN answer. It is not "fresh" and it is not
+    # "stale" — it is unreadable, and decide() must say INDETERMINATE with a
+    # remedy that fits a clock rather than one that says re-download the DB.
+    if age < 0:
+        print("future")
+    else:
+        print(f"{age:.2f}")
+except Exception:
+    print("")
+' 2>/dev/null || true
+}
 # --- self-test: the positive control -----------------------------------------
 # The whole point is that this gate must not be able to pass vacuously. Each
 # case asserts an EXIT CODE, and the first two are known-bad inputs that MUST
@@ -628,7 +668,24 @@
 "node:24-alpine|0||3|22
 postgres:15-alpine|1|CVE-2025-68121|5|61
 alpine:3.10|0||4|31" "alpine:3.10" "2.0"
-
+    # KS-766: the PRODUCER half of QA F-5. Every run_case row above hands decide()
+    #    its age as a string, so none of them runs db_age_from_version_json. These
+    #    two do. Restoring the old clamp there reds the first and not the second.
+    echo "=== self-test: the DB-age producer reads the stamp it is given (KS-766) ==="
+    got="$(printf '%s' '{"VulnerabilityDB":{"UpdatedAt":"2999-01-01T00:00:00.123456789Z"}}' | db_age_from_version_json || true)"
+    if [ "$got" = "future" ]; then
+        echo "  PASS  a FUTURE UpdatedAt yields the future sentinel"
+    else
+        echo "  FAIL  a FUTURE UpdatedAt yielded '$got', not the future sentinel"
+        fails=$((fails + 1))
+    fi
+    got="$(printf '%s' '{"VulnerabilityDB":{"UpdatedAt":"2020-01-01T00:00:00.123456789Z"}}' | db_age_from_version_json || true)"
+    if printf '%s' "$got" | grep -Eq '^[0-9]+[.][0-9]{2}$'; then
+        echo "  PASS  a past UpdatedAt yields a numeric age (${got}h)"
+    else
+        echo "  FAIL  a past UpdatedAt yielded '$got', not a numeric age"
+        fails=$((fails + 1))
+    fi
     # 6. The base list here must match refresh-base-images.sh, or a base added
     #    there would silently go unscanned by this gate.
     echo "=== self-test: base list is in step with refresh-base-images.sh ==="
@@ -792,42 +849,7 @@
 # version --format json` reports VulnerabilityDB.UpdatedAt for the cache this
 # very run used. Unreadable is NOT treated as fresh — decide() takes an empty
 # value as unknown and refuses to call a residual cleared on it.
-DB_AGE_HOURS="$(docker run --rm -v secuura-trivy-cache:/root/.cache "$TRIVY_IMAGE" \
-    version --format json 2>/dev/null \
-  | python3 -c '
-import json,sys,datetime,re
-try:
-    d = json.load(sys.stdin)
-    ts = (d.get("VulnerabilityDB") or {}).get("UpdatedAt")
-    if not ts:
-        print(""); raise SystemExit
-    ts = ts.replace("Z", "+00:00")
-    # QA F-8. trivy stamps RFC3339 with NANOSECOND precision. On a host running
-    # python < 3.11 `fromisoformat` rejects that outright, so this whole block
-    # raised, printed "", and decide() read the age as unknown — which makes the
-    # gate PERMANENTLY indeterminate the moment a residual clears, silently
-    # disabling the one verdict it exists to produce. It fails safe, which is
-    # why nothing noticed. Truncate the fraction to microseconds first.
-    ts = re.sub(r"\.(\d{6})\d+", r".\1", ts)
-    upd = datetime.datetime.fromisoformat(ts)
-    now = datetime.datetime.now(datetime.timezone.utc)
-    age = (now - upd).total_seconds() / 3600
-    # QA F-5. A FUTURE stamp (clock skew, a bad cache) was CLAMPED to 0 and then
-    # printed inside a CLEARED verdict as "the vulnerability DB is 0.0h old" —
-    # i.e. the freshest possible reading, produced by the one input that means
-    # the clock cannot be trusted at all. That is the worst direction for this
-    # value to fail in: it is the sentence an operator reads before running the
-    # ACR leg against the live registry.
-    #
-    # A future stamp is now its OWN answer. It is not "fresh" and it is not
-    # "stale" — it is unreadable, and decide() must say INDETERMINATE with a
-    # remedy that fits a clock rather than one that says re-download the DB.
-    if age < 0:
-        print("future")
-    else:
-        print(f"{age:.2f}")
-except Exception:
-    print("")
-' 2>/dev/null || true)"
+DB_AGE_HOURS="$(docker run --rm -v secuura-trivy-cache:/root/.cache "$TRIVY_IMAGE" \
+    version --format json 2>/dev/null | db_age_from_version_json || true)"
 [ -n "$DB_AGE_HOURS" ] && echo "  (currency control) vulnerability DB age: ${DB_AGE_HOURS}h (limit ${MAX_DB_AGE_HOURS}h)" \
                       || echo "  (currency control) vulnerability DB age: UNREADABLE"
```
