# READY — KS-1137-F2-ESTATEIMAGE-1 (Ornith, briefed, test_only, BASH suite) — PASS 8/8 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-21_ks1137-ornith35b-night2/out.md.checker/patch.diff`** (from `ls` at 03:31 2026-09-21). Checker T3: strict `git apply --check` at the tip PASS; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp`, Wednesday).

**Held 03:31 2026-09-21 by the 01:3x Wednesday seat after a source read.** Tip `cbae988dbe90ebe556459ada2cb437eaf80e2402`. Adds ONE cell (3b) to the bash suite `scripts/__tests__/container_trivy_image_filter.test.sh` (hunk `@@ -140,1 +140,20 @@`): the estate's real digit-bearing image `dev-m365-integration:latest` (compose's 33rd `build:` service) passes the trivy image filter through the stubs — KS-1137 item 1 (F-2). Refs KS-1137; NEVER Closes. **Round accounting stated:** the 03:27 attempt was a LOAD refusal by the harness (rc 3, wall 0 s, the model never ran) — this is round 1 proper; no rebrief spent.

**Source read (Wednesday, same action):** 19 `+` lines, all byte-equal (ordered) to `night/briefs/KS-1137-F2-ESTATEIMAGE-1.md`; 0 `-`; one suite file; the run's patch BYTE-IDENTICAL to the golden. First sample.

**Tampers (T6 red exactly the declared set; T7 controls green; T8 restored):** TRAILINGDIGITONLY (`[a-z-]+[0-9]?`) on `Blockchain/Testing/jobs/04-container-trivy.sh:62` reds only the new cell (dev-auth2 stays green — the ticket's point); KS867REVERTED (`[a-z-]+`) reds the new cell + the KS-867 cell (declared). From byte-matches the tip (count 1 by `grep -c -F -x`, control `latest` 3, checked by Wednesday); T8 restored by bytes. Suite 4/4 → 5/5; applied suite `bash -n` ok; sibling trivy suites rc 0 (drafter). Instrument note carried: the stub's bare `{}` reads clean only until KS-1274 lands.

**Checker:** `RESULT: PASS (8/8)`; T5 green at the tip. Drafter precheck golden 8/8 twice.

**Collision:** KS-1136's READY on this job is spent (#1051 in the tip); KS-1273/1274 unbriefed; no held READY touches this suite (drafter's grep, frame `night/READY_*`).

**For the raise seat:** strict apply; TEST-ONLY; `/bin/bash` 3.2 harness, run from the repo root as `run-shell-suites.sh` does; tier 2; `Refs KS-1137`. **FIFTEEN banked for the next raise seat.**

---
--- a/Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh
+++ b/Blockchain/Dev/scripts/__tests__/container_trivy_image_filter.test.sh
@@ -140,1 +140,20 @@
+# ---------------------------------------------------------------------------
+# CELL 3b - KS-1137 F-2. The ESTATE's real digit-bearing image. dev-auth2 is a
+# synthetic name; the producible instance on this estate is
+# dev-m365-integration:latest (docker-compose.yml's m365-integration build:
+# service, the one of 33 that base scanned 0 times). Its digits sit MID-name,
+# so a class that admits only a trailing digit keeps CELL 1 green and still
+# skips it. Same stubs, same record: the image must be scanned exactly once
+# and the artefact must name it.
+# ---------------------------------------------------------------------------
+CORPUS_ESTATE='dev-m365-integration:latest
+dev-auth:latest
+postgres:15'
+build_fixture "$WORK/estate" "$CORPUS_ESTATE"
+rc_estate="$(run_job "$WORK/estate")"
+if [ "$rc_estate" = 0 ] && [ "$(scanned_times "$WORK/estate" dev-m365-integration:latest)" -eq 1 ] && [ "$(jq -r '.images[].image' "$WORK/estate/run/04-container-trivy.json" 2>/dev/null | grep -cx dev-m365-integration:latest)" = 1 ]; then
+  ok "KS-1137 F-2 - the estate's real digit-bearing image (dev-m365-integration:latest) IS scanned, once, and the artefact names it (rc=$rc_estate)"
+else
+  bad "KS-1137 F-2 - the estate's real digit-bearing image (dev-m365-integration:latest) is scanned" "rc=$rc_estate, scanned $(scanned_times "$WORK/estate" dev-m365-integration:latest) times of $(scanned_total "$WORK/estate") total, output: $(paste -sd ' ' "$WORK/estate/out.txt")"
+fi
 # ---------------------------------------------------------------------------
