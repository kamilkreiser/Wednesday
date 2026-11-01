# READY — KS-1841-KS-1841-O49-P4 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1841_o49_p4_gateway_dockerfile_find_keeps_only_spec/out.md.checker/patch.diff`** (from `ls` at 00:29 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1841_o49_p4_gateway_dockerfile_find_keeps_only_spec/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1841_o49_p4_gateway_dockerfile_find_keeps_only_spec/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1841_o49_p4_gateway_dockerfile_find_keeps_only_spec/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1841_o49_p4_gateway_dockerfile_find_keeps_only_spec/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1841_o49_p4_gateway_dockerfile_find_keeps_only_spec-control-r3/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 00:29 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1841_o49_p4_gateway_dockerfile_find_keeps_only_spec/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `ca36945e974081be6abbc15e548f4f8d02767e14`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/api-gateway/Dockerfile } + { Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1841-dockerfile-keeps-only-the-spec.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/Dockerfile` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/api-gateway/Dockerfile
7	7	Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts
82	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1841-dockerfile-keeps-only-the-spec.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (9 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: Dockerfile ks1823-dockerfile-drops-spec-backups.test.ts`
- CODE_PATCH2 (rung 3, 1 product files + 2 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/api-gateway/Dockerfile`; test(s): `Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts`, `Blockchain/Dev/services/api-gateway/src/__tests__/ks1841-dockerfile-keeps-only-the-spec.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/api-gateway/Dockerfile 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/api-gateway/src/__tests__/ks1841-dockerfile-keeps-only-the-spec.test.ts 82 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/Dockerfile` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts` (hunks=3, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1841-dockerfile-keeps-only-the-spec.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 13 run; controls green; assertion reds)` [red_first.json: failed=6 of total=13; red cell(s): ['KS-1823: the api-gateway image does not carry the spec rollback copies RED KS-1823 R1 the builder stage removes every file but the spec with a find that spares secuura-api.yaml by name (KS-1841)', 'KS-1823: the api-gateway image does not carry the spec rollback copies RED KS-1823 R2 the two name globs of the first fix are gone (KS-1841)', 'KS-1823: the api-gateway image does not carry the spec rollback copies RED KS-1823 R3 the removal is the single line given, after the spec COPY, before the build, and before the runtime stage', 'KS-1841: the api-gateway builder stage keeps only secuura-api.yaml in docs/openapi RED KS-1841 R1 the Dockerfile has a find over docs/openapi that spares secuura-api.yaml by name', 'KS-1841: the api-gateway builder stage keeps only secuura-api.yaml in docs/openapi RED KS-1841 R2 running that command leaves exactly secuura-api.yaml, with every missed name shape and the folder gone', 'KS-1841: the api-gateway builder stage keeps only secuura-api.yaml in docs/openapi RED KS-1841 R3 running it twice, or on a directory that already holds only the spec, succeeds and changes nothing']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (13 passed / 13 run)` [green_after.json: failed=0 of total=13, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1368 failed=0 | after: total=1373 failed=0` · `NEW reds: []` [baseline_suite.json total=1368 failed=0; after_suite.json total=1373 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=1 tests=2 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/Dockerfile` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts` (+7/-7); 3 files in all (code_patch2: products Blockchain/Dev/services/api-gateway/Dockerfile). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `ca36945e974081be6abbc15e548f4f8d02767e14` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1841_o49_p4_gateway_dockerfile_find_keeps_only_spec/input.json`. Brief (given by --brief; its `# ` heading names KS-1841): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1841_o49_p4_gateway_dockerfile_find_keeps_only_spec/KS-1841.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1841_o49_p4_gateway_dockerfile_find_keeps_only_spec/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/Dockerfile b/Blockchain/Dev/services/api-gateway/Dockerfile
--- a/Blockchain/Dev/services/api-gateway/Dockerfile
+++ b/Blockchain/Dev/services/api-gateway/Dockerfile
@@ -34,3 +34,3 @@
-# KS-1823: the host directory can also hold rollback copies of the spec; the gateway reads secuura-api.yaml only.
-RUN rm -f ./docs/openapi/*.pre-* ./docs/openapi/*.rollback-*
+# KS-1841 (it replaces KS-1823's two name globs): the host directory can hold backups of the spec under any name; the gateway reads secuura-api.yaml only, so keep that file and nothing else.
+RUN find ./docs/openapi -mindepth 1 -maxdepth 1 ! -name secuura-api.yaml -exec rm -rf {} +
 # Relax strict unused-variable checks for production build
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1823-dockerfile-drops-spec-backups.test.ts
@@ -12,3 +12,3 @@
 const COPY_AT = DOCKERFILE.indexOf(COPY_SPEC);
-const RM_LINE = 'RUN rm -f ./docs/openapi/*.pre-* ./docs/openapi/*.rollback-*';
+const RM_LINE = 'RUN find ./docs/openapi -mindepth 1 -maxdepth 1 ! -name secuura-api.yaml -exec rm -rf {} +';
 const RM_AT = DOCKERFILE.indexOf(RM_LINE);
@@ -17,8 +17,8 @@
 describe('KS-1823: the api-gateway image does not carry the spec rollback copies', () => {
-  it('RED KS-1823 R1 the builder stage removes the pre-ks508 style rollback copies', () => {
-    expect(DOCKERFILE.some((l) => l.startsWith('RUN rm -f') && l.includes('./docs/openapi/*.pre-*'))).toBe(true);
+  it('RED KS-1823 R1 the builder stage removes every file but the spec with a find that spares secuura-api.yaml by name (KS-1841)', () => {
+    expect(DOCKERFILE.some((l) => l.startsWith('RUN find ./docs/openapi') && l.includes('! -name secuura-api.yaml'))).toBe(true);
   });
-
-  it('RED KS-1823 R2 the builder stage removes the rollback-dated copies', () => {
-    expect(DOCKERFILE.some((l) => l.startsWith('RUN rm -f') && l.includes('./docs/openapi/*.rollback-*'))).toBe(true);
+  // KS-1841: R2 is the other half of R1, the two name globs of the first fix are gone.
+  it('RED KS-1823 R2 the two name globs of the first fix are gone (KS-1841)', () => {
+    expect(DOCKERFILE.some((l) => l.includes('*.pre-*') || l.includes('*.rollback-*'))).toBe(false);
   });
@@ -40,3 +40,3 @@
   it('control KS-1823 C3 no line removes the spec itself or the whole directory', () => {
-    const rmLines = DOCKERFILE.filter((l) => /\brm\b/.test(l) && l.includes('docs/openapi'));
+    const rmLines = DOCKERFILE.filter((l) => l.startsWith('RUN rm') && l.includes('docs/openapi'));
     for (const l of rmLines) {
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1841-dockerfile-keeps-only-the-spec.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1841-dockerfile-keeps-only-the-spec.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1841-dockerfile-keeps-only-the-spec.test.ts
@@ -0,0 +1,82 @@
+// KS-1841 (api-gateway image): the builder stage copies the whole docs/openapi directory and then removes everything in it
+// except secuura-api.yaml. KS-1823 removed two name shapes only (*.pre-*, *.rollback-*), so a backup under any other name
+// (.bak, ~, .orig, a prefix, an editor swap file, a stray note or folder) was still baked into the image.
+// This test runs the Dockerfile's own RUN command (the text after `RUN `) with `sh -c` against a throwaway directory tree
+// that holds the spec and the missed name shapes. No docker daemon is involved; the command is read from the Dockerfile, not copied.
+import { describe, it, expect, afterEach } from 'vitest';
+import { execFileSync } from 'child_process';
+import { mkdirSync, mkdtempSync, readdirSync, readFileSync, rmSync, writeFileSync } from 'fs';
+import { tmpdir } from 'os';
+import { join, resolve } from 'path';
+
+const FIXTURE_LINES = readFileSync(resolve(__dirname, '..', '..', 'Dockerfile'), 'utf8').split('\n');
+const FIND_RUN = FIXTURE_LINES.find((l) => l.startsWith('RUN find ./docs/openapi'));
+const SPEC_BODY = 'openapi: 3.0.3\ninfo:\n  title: ks1841 fixture\n';
+const MISSED_NAMES = [
+  'secuura-api.yaml.pre-ks508',
+  'secuura-api.yaml.rollback-2026-08-27-ks661',
+  'secuura-api.yaml.bak',
+  'secuura-api.yaml~',
+  'secuura-api.yaml.orig',
+  '.secuura-api.yaml.swp',
+  'backup-secuura-api.yaml',
+  'WORKFLOWS.md',
+];
+
+const made: string[] = [];
+function fixture(): string {
+  const root = mkdtempSync(join(tmpdir(), 'ks1841-'));
+  made.push(root);
+  const dir = join(root, 'docs', 'openapi');
+  mkdirSync(join(dir, 'old-copies'), { recursive: true });
+  writeFileSync(join(dir, 'secuura-api.yaml'), SPEC_BODY);
+  for (const name of MISSED_NAMES) writeFileSync(join(dir, name), 'stale ' + name + '\n');
+  writeFileSync(join(dir, 'old-copies', 'secuura-api.yaml'), 'stale nested spec\n');
+  return root;
+}
+const run = (command: string, root: string) => execFileSync('sh', ['-c', command], { cwd: root, stdio: 'pipe' });
+const left = (root: string) => readdirSync(join(root, 'docs', 'openapi')).sort();
+
+afterEach(() => {
+  for (const root of made.splice(0)) rmSync(root, { recursive: true, force: true });
+});
+
+describe('KS-1841: the api-gateway builder stage keeps only secuura-api.yaml in docs/openapi', () => {
+  it('RED KS-1841 R1 the Dockerfile has a find over docs/openapi that spares secuura-api.yaml by name', () => {
+    expect(FIND_RUN).toBeDefined();
+    expect(FIND_RUN).toContain('! -name secuura-api.yaml');
+  });
+
+  it('RED KS-1841 R2 running that command leaves exactly secuura-api.yaml, with every missed name shape and the folder gone', () => {
+    expect(FIND_RUN).toBeDefined();
+    const root = fixture();
+    run(String(FIND_RUN).slice('RUN '.length), root);
+    expect(left(root)).toEqual(['secuura-api.yaml']);
+    expect(readFileSync(join(root, 'docs', 'openapi', 'secuura-api.yaml'), 'utf8')).toBe(SPEC_BODY);
+  });
+
+  it('RED KS-1841 R3 running it twice, or on a directory that already holds only the spec, succeeds and changes nothing', () => {
+    expect(FIND_RUN).toBeDefined();
+    const root = fixture();
+    const command = String(FIND_RUN).slice('RUN '.length);
+    run(command, root);
+    run(command, root);
+    expect(left(root)).toEqual(['secuura-api.yaml']);
+    expect(readFileSync(join(root, 'docs', 'openapi', 'secuura-api.yaml'), 'utf8')).toBe(SPEC_BODY);
+  });
+
+  it('control KS-1841 C1 the fixture sees the gap: the two-glob command of KS-1823 leaves the missed name shapes behind', () => {
+    const root = fixture();
+    run('rm -f ./docs/openapi/*.pre-* ./docs/openapi/*.rollback-*', root);
+    const remaining = left(root);
+    expect(remaining).toContain('secuura-api.yaml');
+    expect(remaining).toContain('secuura-api.yaml.bak');
+    expect(remaining).toContain('WORKFLOWS.md');
+    expect(remaining).not.toContain('secuura-api.yaml.pre-ks508');
+  });
+
+  it('control KS-1841 C2 the fixture starts with the spec, all eight missed names and the folder', () => {
+    const root = fixture();
+    expect(left(root)).toEqual(['secuura-api.yaml', 'old-copies', ...MISSED_NAMES].sort());
+  });
+});
```
