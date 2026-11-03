# READY — KS-1868-KS-1868-O97-P5 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p5_shared_auto_migrate_run_migrations_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 17:29 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p5_shared_auto_migrate_run_migrations_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p5_shared_auto_migrate_run_migrations_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p5_shared_auto_migrate_run_migrations_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p5_shared_auto_migrate_run_migrations_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 17:29 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p5_shared_auto_migrate_run_migrations_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `de8d208a8426747b3a752309e08167fa0de4b2ff`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/packages/shared/src/db/auto-migrate.ts } + { Blockchain/Dev/packages/shared/src/__tests__/ks1868-auto-migrate-run-migrations-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/db/auto-migrate.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1868-auto-migrate-run-migrations-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/packages/shared/src/db/auto-migrate.ts
101	0	Blockchain/Dev/packages/shared/src/__tests__/ks1868-auto-migrate-run-migrations-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: auto-migrate.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/packages/shared/src/db/auto-migrate.ts`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1868-auto-migrate-run-migrations-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/packages/shared/src/db/auto-migrate.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1868-auto-migrate-run-migrations-catch-unreadable-throw.test.ts 101 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/db/auto-migrate.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1868-auto-migrate-run-migrations-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 runMigrations reads a migration failure safely RED ks1868 R1 a revoked Proxy is recorded with a constant reason', 'KS-1868 runMigrations reads a migration failure safely RED ks1868 R2 an Error whose message getter throws is recorded with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1447 failed=1 | after: total=1451 failed=1` · `NEW reds: []` [baseline_suite.json total=1447 failed=1; after_suite.json total=1451 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/db/auto-migrate.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1868-auto-migrate-run-migrations-catch-unreadable-throw.test.ts` (+101/-0); 2 files in all (code_patch2: products Blockchain/Dev/packages/shared/src/db/auto-migrate.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `de8d208a8426747b3a752309e08167fa0de4b2ff` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p5_shared_auto_migrate_run_migrations_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o97_p5_shared_auto_migrate_run_migrations_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o97_p5_shared_auto_migrate_run_migrations_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/db/auto-migrate.ts b/Blockchain/Dev/packages/shared/src/db/auto-migrate.ts
--- a/Blockchain/Dev/packages/shared/src/db/auto-migrate.ts
+++ b/Blockchain/Dev/packages/shared/src/db/auto-migrate.ts
@@ -161,7 +161,13 @@
         result.applied.push(filename);
       } catch (err: any) {
         await client.query('ROLLBACK').catch(() => {});
-        const message = `Failed to apply ${filename}: ${err.message || err}`;
+        let detail: string;
+        try {
+          detail = `${err.message || err}`;
+        } catch {
+          detail = 'unreadable thrown value';
+        }
+        const message = `Failed to apply ${filename}: ${detail}`;
         console.error(`[auto-migrate] ${message}`);
         result.errors.push(message);
         // Stop on first error — later migrations may depend on this one
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1868-auto-migrate-run-migrations-catch-unreadable-throw.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-auto-migrate-run-migrations-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-auto-migrate-run-migrations-catch-unreadable-throw.test.ts
@@ -0,0 +1,101 @@
+import { describe, it, expect, vi, afterEach } from 'vitest';
+import fs from 'fs';
+import os from 'os';
+import path from 'path';
+
+// KS-1868: runMigrations (src/db/auto-migrate.ts) rolls a failed migration back and records `Failed to apply <file>: ${err.message || err}`
+// in its result. The `err.message || err` read is unguarded. When the value cannot be read (a revoked Proxy throws on any
+// property read; an Error whose `message` getter throws) the catch itself throws, so runMigrations REJECTS and the caller
+// gets no result where an ordinary failure is returned in `errors`. `pg` is replaced by a plain Pool stand-in whose client
+// rejects the migration statement with the cell's value; the migration is a real one-line file in a temporary directory;
+// console is silenced; no network.
+const h = vi.hoisted(() => ({ toThrow: undefined as unknown }));
+
+vi.mock('pg', () => {
+  class Pool {
+    async query(): Promise<{ rows: unknown[]; rowCount: number }> {
+      return { rows: [], rowCount: 0 };
+    }
+    async connect() {
+      return {
+        query: (text: string): Promise<unknown> => (text === 'SELECT 1;' ? Promise.reject(h.toThrow) : Promise.resolve({ rows: [] })),
+        release: () => undefined,
+      };
+    }
+    async end(): Promise<void> {
+      return undefined;
+    }
+  }
+  return { default: { Pool }, Pool };
+});
+
+import { runMigrations } from '../db/auto-migrate';
+
+type Outcome = { rejected: boolean; errors: string[] | undefined; applied: string[] | undefined };
+
+async function run(value: unknown): Promise<Outcome> {
+  h.toThrow = value;
+  vi.spyOn(console, 'log').mockImplementation(() => undefined);
+  vi.spyOn(console, 'error').mockImplementation(() => undefined);
+  const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'ks1868-migrate-'));
+  fs.writeFileSync(path.join(dir, '001_ks1868.sql'), 'SELECT 1;');
+  let rejected = false;
+  let errors: string[] | undefined;
+  let applied: string[] | undefined;
+  try {
+    const r = await runMigrations({ migrationsDir: dir, databaseUrl: 'postgres://app:pw@127.0.0.1:5432/secuura' });
+    errors = r.errors;
+    applied = r.applied;
+  } catch {
+    rejected = true;
+  } finally {
+    fs.rmSync(dir, { recursive: true, force: true });
+  }
+  return { rejected, errors, applied };
+}
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 runMigrations reads a migration failure safely', () => {
+  afterEach(() => {
+    vi.restoreAllMocks();
+  });
+
+  it('control ks1868 C1 an ordinary Error is recorded with its message', async () => {
+    const out = await run(new Error('syntax boom'));
+    expect(out.rejected).toBe(false);
+    expect(out.errors).toEqual(['Failed to apply 001_ks1868.sql: syntax boom']);
+    expect(out.applied).toEqual([]);
+  });
+
+  it('control ks1868 C2 a thrown plain string is recorded with that text', async () => {
+    const out = await run('plain text failure');
+    expect(out.rejected).toBe(false);
+    expect(out.errors).toEqual(['Failed to apply 001_ks1868.sql: plain text failure']);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy is recorded with a constant reason', async () => {
+    const out = await run(revokedProxy());
+    expect(out.rejected).toBe(false);
+    expect(out.errors).toEqual(['Failed to apply 001_ks1868.sql: unreadable thrown value']);
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws is recorded with a constant reason', async () => {
+    const out = await run(getterThrows());
+    expect(out.rejected).toBe(false);
+    expect(out.errors).toEqual(['Failed to apply 001_ks1868.sql: unreadable thrown value']);
+  });
+});
```
