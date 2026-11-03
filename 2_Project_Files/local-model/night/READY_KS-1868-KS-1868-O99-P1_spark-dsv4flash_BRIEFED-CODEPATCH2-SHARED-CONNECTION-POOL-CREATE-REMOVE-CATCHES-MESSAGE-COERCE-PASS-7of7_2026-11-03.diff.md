# READY — KS-1868-KS-1868-O99-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o99_p1_shared_connection_pool_create_and_remove_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 21:12 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o99_p1_shared_connection_pool_create_and_remove_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o99_p1_shared_connection_pool_create_and_remove_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o99_p1_shared_connection_pool_create_and_remove_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o99_p1_shared_connection_pool_create_and_remove_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 21:12 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o99_p1_shared_connection_pool_create_and_remove_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `1cbf260548e7fd534603725f9fc6b05c5cdd9907`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/shared/src/cache/connection-pool.ts } + { Blockchain/Dev/services/shared/src/__tests__/ks1868-connection-pool-create-remove-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/shared/src/cache/connection-pool.ts` (product) and `Blockchain/Dev/services/shared/src/__tests__/ks1868-connection-pool-create-remove-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
15	3	Blockchain/Dev/services/shared/src/cache/connection-pool.ts
129	0	Blockchain/Dev/services/shared/src/__tests__/ks1868-connection-pool-create-remove-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (15 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: connection-pool.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/shared/src/cache/connection-pool.ts`; test(s): `Blockchain/Dev/services/shared/src/__tests__/ks1868-connection-pool-create-remove-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/shared/src/cache/connection-pool.ts 15 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/shared/src/__tests__/ks1868-connection-pool-create-remove-catches-unreadable-throw.test.ts 129 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/shared/src/cache/connection-pool.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/shared/src/__tests__/ks1868-connection-pool-create-remove-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 ConnectionPool reads a connection failure safely RED ks1868 R1 createConnection: a revoked Proxy is rethrown as is and a constant reason logged', 'KS-1868 ConnectionPool reads a connection failure safely RED ks1868 R2 createConnection: an Error whose message getter throws is rethrown as is and a constant reason logged', 'KS-1868 ConnectionPool reads a connection failure safely RED ks1868 R3 removeConnection: a revoked Proxy still emits connectionRemoved and logs a constant reason', 'KS-1868 ConnectionPool reads a connection failure safely RED ks1868 R4 removeConnection: an Error whose message getter throws still emits connectionRemoved and logs a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=13 failed=0 | after: total=19 failed=0` · `NEW reds: []` [baseline_suite.json total=13 failed=0; after_suite.json total=19 failed=0]
- A6 [verbatim]: `PASS A6 whole services/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/shared/src/cache/connection-pool.ts` (+15/-3 per numstat.out) and the test file `Blockchain/Dev/services/shared/src/__tests__/ks1868-connection-pool-create-remove-catches-unreadable-throw.test.ts` (+129/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/shared/src/cache/connection-pool.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `1cbf260548e7fd534603725f9fc6b05c5cdd9907` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o99_p1_shared_connection_pool_create_and_remove_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o99_p1_shared_connection_pool_create_and_remove_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o99_p1_shared_connection_pool_create_and_remove_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/shared/src/cache/connection-pool.ts b/Blockchain/Dev/services/shared/src/cache/connection-pool.ts
--- a/Blockchain/Dev/services/shared/src/cache/connection-pool.ts
+++ b/Blockchain/Dev/services/shared/src/cache/connection-pool.ts
@@ -112,5 +112,11 @@
         this.emit('connectionCreated', conn);
         return conn;
-      } catch (error) {
-        lastError = error as Error;
+      } catch (caught) {
+        lastError = caught as Error;
+        let error: string;
+        try {
+          error = String(caught);
+        } catch {
+          error = 'unreadable thrown value';
+        }
         logger.error('Pool create attempt failed', { attempt: attempt + 1, error: String(error) });
@@ -219,5 +225,11 @@
     try {
       await conn.close();
     } catch (error) {
-      logger.error('Pool error closing connection', { error: String(error) });
+      let reason: string;
+      try {
+        reason = String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Pool error closing connection', { error: reason });
     }
diff --git a/Blockchain/Dev/services/shared/src/__tests__/ks1868-connection-pool-create-remove-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/shared/src/__tests__/ks1868-connection-pool-create-remove-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/shared/src/__tests__/ks1868-connection-pool-create-remove-catches-unreadable-throw.test.ts
@@ -0,0 +1,129 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868: ConnectionPool (src/cache/connection-pool.ts) has two catches that log `{ error: String(error) }`:
+// createConnection (a factory failure; after the attempts it rethrows the last ORIGINAL value) and removeConnection
+// (a failed close(); the pool goes on and emits 'connectionRemoved'). The `String(error)` read is unguarded. When the value
+// cannot be read (a revoked Proxy throws on String(); an Error whose `message` getter throws, throws in
+// Error.prototype.toString) the catch itself throws a TypeError, so createConnection rejects with that TypeError instead of
+// the original value and removeConnection rejects without emitting. The factory and close() are plain functions rejecting
+// with the cell's value; the logger is a plain recorder; no network.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  errors: [] as unknown[][],
+  warns: [] as unknown[][],
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    debug: () => undefined,
+    info: () => undefined,
+    warn: (...args: unknown[]) => {
+      h.warns.push(args);
+    },
+    error: (...args: unknown[]) => {
+      h.errors.push(args);
+    },
+  },
+}));
+
+import { ConnectionPool } from '../cache/connection-pool';
+
+const mkPool = () =>
+  new ConnectionPool<never>(() => Promise.reject(h.toThrow), undefined, {
+    min: 0,
+    max: 1,
+    maxRetries: 1,
+    createRetryMs: 1,
+  });
+
+/** What createConnection rejected with, or 'resolved'. */
+// Boxed on purpose: a promise that resolves with a revoked Proxy throws when it reads `.then` on it.
+async function createOutcome(): Promise<{ caught: unknown }> {
+  try {
+    await (mkPool() as unknown as { createConnection(): Promise<unknown> }).createConnection();
+    return { caught: 'resolved' };
+  } catch (e) {
+    return { caught: e };
+  }
+}
+
+/** Whether removeConnection settled, and how many 'connectionRemoved' events it emitted. */
+async function removeOutcome(): Promise<{ threw: boolean; removed: number }> {
+  const pool = mkPool();
+  let removed = 0;
+  pool.on('connectionRemoved', () => {
+    removed++;
+  });
+  const conn = { id: 'c', close: () => Promise.reject(h.toThrow) };
+  let threw = false;
+  try {
+    await (pool as unknown as { removeConnection(c: unknown): Promise<void> }).removeConnection(conn);
+  } catch {
+    threw = true;
+  }
+  return { threw, removed };
+}
+
+const logged = (needle: string): unknown[][] => h.errors.filter((a) => String(a[0]).includes(needle));
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
+describe('KS-1868 ConnectionPool reads a connection failure safely', () => {
+  beforeEach(() => {
+    h.toThrow = undefined;
+    h.errors = [];
+    h.warns = [];
+  });
+
+  it('control ks1868 C1 createConnection: an ordinary Error is rethrown as is and its text logged', async () => {
+    const value = new Error('factory down');
+    h.toThrow = value;
+    expect((await createOutcome()).caught === value).toBe(true);
+    expect(logged('Pool create attempt failed')[0][1]).toEqual({ attempt: 1, error: 'Error: factory down' });
+  });
+
+  it('control ks1868 C2 removeConnection: a thrown plain string still emits connectionRemoved and logs that text', async () => {
+    h.toThrow = 'plain text failure';
+    expect(await removeOutcome()).toEqual({ threw: false, removed: 1 });
+    expect(logged('Pool error closing connection')[0][1]).toEqual({ error: 'plain text failure' });
+  });
+
+  it('RED ks1868 R1 createConnection: a revoked Proxy is rethrown as is and a constant reason logged', async () => {
+    const value = revokedProxy();
+    h.toThrow = value;
+    expect((await createOutcome()).caught === value).toBe(true);
+    expect(logged('Pool create attempt failed')[0][1]).toEqual({ attempt: 1, error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 createConnection: an Error whose message getter throws is rethrown as is and a constant reason logged', async () => {
+    const value = getterThrows();
+    h.toThrow = value;
+    expect((await createOutcome()).caught === value).toBe(true);
+    expect(logged('Pool create attempt failed')[0][1]).toEqual({ attempt: 1, error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 removeConnection: a revoked Proxy still emits connectionRemoved and logs a constant reason', async () => {
+    h.toThrow = revokedProxy();
+    expect(await removeOutcome()).toEqual({ threw: false, removed: 1 });
+    expect(logged('Pool error closing connection')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R4 removeConnection: an Error whose message getter throws still emits connectionRemoved and logs a constant reason', async () => {
+    h.toThrow = getterThrows();
+    expect(await removeOutcome()).toEqual({ threw: false, removed: 1 });
+    expect(logged('Pool error closing connection')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+});
```
