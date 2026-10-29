# READY — KS-1823-KS-1823-SPECBACKUPS (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1823_p1_dockerfile/out.md.checker/patch.diff`** (from `ls` at 04:34 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1823_p1_dockerfile/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1823_p1_dockerfile/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1823_p1_dockerfile/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 04:34 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1823_p1_dockerfile/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `203734468019feaf44428975b10cf5f799483187`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/Dockerfile } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/Dockerfile` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	0	Blockchain/Dev/services/api-gateway/Dockerfile
57	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (2 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: Dockerfile`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/Dockerfile`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/Dockerfile 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts 57 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/Dockerfile` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=3 of total=8; red cell(s): ['KS-1823: the api-gateway image does not carry the spec rollback copies RED KS-1823 R1 the builder stage removes the pre-ks508 style rollback copies', 'KS-1823: the api-gateway image does not carry the spec rollback copies RED KS-1823 R2 the builder stage removes the rollback-dated copies', 'KS-1823: the api-gateway image does not carry the spec rollback copies RED KS-1823 R3 the removal is the single line given, after the spec COPY, before the build, and before the runtime stage']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1313 failed=0 | after: total=1321 failed=0` · `NEW reds: []` [baseline_suite.json total=1313 failed=0; after_suite.json total=1321 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/Dockerfile` (+2/-0 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts` (+57/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/Dockerfile). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `203734468019feaf44428975b10cf5f799483187` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1823_p1_dockerfile/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1823_p1_dockerfile/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/Dockerfile b/Blockchain/Dev/services/api-gateway/Dockerfile
--- a/Blockchain/Dev/services/api-gateway/Dockerfile
+++ b/Blockchain/Dev/services/api-gateway/Dockerfile
@@ -34,3 +34,5 @@
+# KS-1823: the host directory can also hold rollback copies of the spec; the gateway reads secuura-api.yaml only.
+RUN rm -f ./docs/openapi/*.pre-* ./docs/openapi/*.rollback-*
 # Relax strict unused-variable checks for production build
 # Build TypeScript
 RUN npm run build
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts
@@ -0,0 +1,57 @@
+// KS-1823 (api-gateway image): the builder stage copies the whole docs/openapi directory (`COPY docs/openapi/ ./docs/openapi/`), so the two rollback copies of the spec that sit on the demo host
+// (secuura-api.yaml.pre-ks508, secuura-api.yaml.rollback-2026-08-27-ks661) were baked into demo's image. These cells read the Dockerfile and the gateway source as text.
+// R1 to R3 are red until the builder stage removes the rollback copies right after that COPY; C1 to C5 pin what must not move, in particular that the spec the gateway reads is still copied.
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'fs';
+import { resolve } from 'path';
+
+const DOCKERFILE = readFileSync(resolve(__dirname, '..', '..', 'Dockerfile'), 'utf8').split('\n');
+const GATEWAY_INDEX = readFileSync(resolve(__dirname, '..', 'index.ts'), 'utf8');
+
+const COPY_SPEC = 'COPY docs/openapi/ ./docs/openapi/';
+const COPY_AT = DOCKERFILE.indexOf(COPY_SPEC);
+const RM_LINE = 'RUN rm -f ./docs/openapi/*.pre-* ./docs/openapi/*.rollback-*';
+const RM_AT = DOCKERFILE.indexOf(RM_LINE);
+const RUNTIME_STAGE_AT = DOCKERFILE.findIndex((l, i) => i > COPY_AT && l.startsWith('FROM '));
+
+describe('KS-1823: the api-gateway image does not carry the spec rollback copies', () => {
+  it('RED KS-1823 R1 the builder stage removes the pre-ks508 style rollback copies', () => {
+    expect(DOCKERFILE.some((l) => l.startsWith('RUN rm -f') && l.includes('./docs/openapi/*.pre-*'))).toBe(true);
+  });
+
+  it('RED KS-1823 R2 the builder stage removes the rollback-dated copies', () => {
+    expect(DOCKERFILE.some((l) => l.startsWith('RUN rm -f') && l.includes('./docs/openapi/*.rollback-*'))).toBe(true);
+  });
+
+  it('RED KS-1823 R3 the removal is the single line given, after the spec COPY, before the build, and before the runtime stage', () => {
+    expect(RM_AT).toBeGreaterThan(COPY_AT);
+    expect(RM_AT).toBeLessThan(RUNTIME_STAGE_AT);
+    expect(RM_AT - COPY_AT).toBeLessThanOrEqual(4);
+  });
+
+  it('control KS-1823 C1 the whole-directory spec COPY is still there (the spec is still copied)', () => {
+    expect(COPY_AT).toBeGreaterThan(-1);
+  });
+
+  it('control KS-1823 C2 the runtime stage still copies the directory from the builder', () => {
+    expect(DOCKERFILE).toContain('COPY --from=builder /app/docs/openapi ./docs/openapi');
+  });
+
+  it('control KS-1823 C3 no line removes the spec itself or the whole directory', () => {
+    const rmLines = DOCKERFILE.filter((l) => /\brm\b/.test(l) && l.includes('docs/openapi'));
+    for (const l of rmLines) {
+      expect(l).not.toContain('secuura-api.yaml');
+      expect(l).not.toMatch(/docs\/openapi\/?\s*$/);
+      expect(l).not.toMatch(/docs\/openapi\/\*(\s|$)/);
+    }
+  });
+
+  it('control KS-1823 C4 the gateway still reads docs/openapi/secuura-api.yaml', () => {
+    expect(GATEWAY_INDEX).toContain('docs/openapi/secuura-api.yaml');
+  });
+
+  it('control KS-1823 C5 the instrument reads real files (the Dockerfile has several stages and the gateway source is not empty)', () => {
+    expect(DOCKERFILE.filter((l) => l.startsWith('FROM ')).length).toBeGreaterThanOrEqual(3);
+    expect(GATEWAY_INDEX.length).toBeGreaterThan(5000);
+  });
+});
```
