# READY — KS-1868-KS-1868-O83-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p1_security_revoke_on_rotate_catches_coerce_message/out.md.checker/patch.diff`** (from `ls` at 21:49 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p1_security_revoke_on_rotate_catches_coerce_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p1_security_revoke_on_rotate_catches_coerce_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p1_security_revoke_on_rotate_catches_coerce_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p1_security_revoke_on_rotate_catches_coerce_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 21:49 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p1_security_revoke_on_rotate_catches_coerce_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `58b5042ccdb5a06a213ba53f5d4f7644f5f52549`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/security/src/index.ts } + { Blockchain/Dev/services/security/src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/security/src/index.ts` (product) and `Blockchain/Dev/services/security/src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
2	2	Blockchain/Dev/services/security/src/index.ts
168	0	Blockchain/Dev/services/security/src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (2 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/security/src/index.ts`; test(s): `Blockchain/Dev/services/security/src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/security/src/index.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/security/src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts 168 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/security/src/index.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/security/src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=6 of total=10; red cell(s): ['KS-1868 the revoke-on-rotate catches turn a hostile message into text RED ks1868 R1 revokePriorConnectorKeys: an Error whose message is a revoked Proxy logs the constant and the function answers null', 'KS-1868 the revoke-on-rotate catches turn a hostile message into text RED ks1868 R2 revokePriorConnectorKeys: an Error whose message is a null-prototype object logs the constant and the function answers null', 'KS-1868 the revoke-on-rotate catches turn a hostile message into text RED ks1868 R3 revokePriorConnectorKeys: an Error whose message is a Symbol logs the Symbol text and the function answers null', 'KS-1868 the revoke-on-rotate catches turn a hostile message into text RED ks1868 R4 saveKeyAndRetirePriors: an Error whose message is a revoked Proxy logs the constant, the retire is rolled back alone and the mint stands', 'KS-1868 the revoke-on-rotate catches turn a hostile message into text RED ks1868 R5 saveKeyAndRetirePriors: an Error whose message is a null-prototype object logs the constant, the retire is rolled back alone and the mint stands', 'KS-1868 the revoke-on-rotate catches turn a hostile message into text RED ks1868 R6 saveKeyAndRetirePriors: an Error whose message is a Symbol logs the Symbol text, the retire is rolled back alone and the mint stands']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=424 failed=0 | after: total=434 failed=0` · `NEW reds: []` [baseline_suite.json total=424 failed=0; after_suite.json total=434 failed=0]
- A6 [verbatim]: `PASS A6 whole services/security suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/security/src/index.ts` (+2/-2 per numstat.out) and the test file `Blockchain/Dev/services/security/src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts` (+168/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/security/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `58b5042ccdb5a06a213ba53f5d4f7644f5f52549` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p1_security_revoke_on_rotate_catches_coerce_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o83_p1_security_revoke_on_rotate_catches_coerce_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o83_p1_security_revoke_on_rotate_catches_coerce_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/security/src/index.ts b/Blockchain/Dev/services/security/src/index.ts
--- a/Blockchain/Dev/services/security/src/index.ts
+++ b/Blockchain/Dev/services/security/src/index.ts
@@ -303,7 +303,7 @@
     // old credential is STILL LIVE.
     let reason: string;
     try {
-      reason = err instanceof Error ? err.message : String(err);
+      reason = String(err instanceof Error ? err.message : err);
     } catch {
       reason = 'unreadable thrown value';
     }
@@ -416,7 +416,7 @@
         await client.query('ROLLBACK TO SAVEPOINT ks1549_retire');
         let reason: string;
         try {
-          reason = err instanceof Error ? err.message : String(err);
+          reason = String(err instanceof Error ? err.message : err);
         } catch {
           reason = 'unreadable thrown value';
         }
diff --git a/Blockchain/Dev/services/security/src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts b/Blockchain/Dev/services/security/src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/security/src/__tests__/ks1868-security-rotate-message-coercion-unreadable-throw.test.ts
@@ -0,0 +1,168 @@
+import { describe, it, expect, vi, beforeAll, beforeEach, afterEach } from 'vitest';
+
+process.env.SECURITY_DISABLE_BOOT = '1';
+
+// KS-1868: the two revoke-on-rotate catches (`revokePriorConnectorKeys` and the savepoint catch of `saveKeyAndRetirePriors`) read the thrown value
+// inside their own guard, but an Error whose `message` getter SUCCEEDS and returns a hostile NON-string (a revoked Proxy, a null-prototype object,
+// a Symbol) hands that value to the service's own `log()` (JSON.stringify), which can throw INSIDE the catch. The line must be logged as text and the
+// KS-577/KS-1549 contract must hold: the function answers null, and for the rotate transaction the mint stands.
+// The db stand-in rejects with a plain function, not a vi.fn(): a spy inspects what it rejects with and could
+// itself fail on a hostile value before the code under test saw it. The outcome is captured with
+// `.then(onOk, onReject)` so a hostile value is never handed to an assertion message.
+// The service logs through console.log (JSON lines), so the log is read from a console.log spy.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  sql: [] as string[],
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  initDb: async () => true,
+  query: () => Promise.reject(h.toThrow),
+  transaction: async (fn: (client: unknown) => Promise<unknown>) =>
+    fn({
+      query: (sql: string) => {
+        h.sql.push(String(sql));
+        if (/^\s*UPDATE\s+svc_api_keys/i.test(String(sql))) return Promise.reject(h.toThrow);
+        return Promise.resolve({ rows: [], rowCount: 0 });
+      },
+    }),
+}));
+
+const TENANT = 'c0000000-0000-4000-8000-000000001868';
+const CONNECTOR = 'ks1868-connector';
+const LOGGED: string[] = [];
+const LINES = () =>
+  LOGGED.filter((s) => s.includes('KS-577: revoke-on-rotate FAILED')).map((s) => JSON.parse(s) as { error?: unknown });
+
+let revokePriorConnectorKeys: (connectorId: string, tenantId: string, keepKeyId: string) => Promise<number | null>;
+let saveKeyAndRetirePriors: (k: unknown, connectorId: string) => Promise<number | null>;
+let memApiKeys: Map<string, unknown>;
+const KEY = {
+  id: 'key_ks1868',
+  tenantId: TENANT,
+  connectorId: CONNECTOR,
+  name: 'ks1868',
+  keyHash: 'ks1868-hash',
+  keyPrefix: 'ks1868',
+  scopes: [] as string[],
+  usageCount: 0,
+  isActive: true,
+  createdAt: new Date(),
+};
+
+beforeAll(async () => {
+  const mod = await import('../index');
+  revokePriorConnectorKeys = mod.revokePriorConnectorKeys;
+  saveKeyAndRetirePriors = mod.saveKeyAndRetirePriors as unknown as typeof saveKeyAndRetirePriors;
+  memApiKeys = mod.memApiKeys as unknown as Map<string, unknown>;
+});
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.sql.length = 0;
+  LOGGED.length = 0;
+  memApiKeys.clear();
+  delete process.env.API_KEY_ROTATION_GRACE_SECONDS;
+  vi.spyOn(console, 'log').mockImplementation((...args: unknown[]) => {
+    LOGGED.push(String(args[0]));
+  });
+});
+
+afterEach(() => {
+  vi.restoreAllMocks();
+});
+
+const settle = (p: Promise<number | null>) =>
+  p.then(
+    (value) => ({ rejected: false, value }),
+    () => ({ rejected: true, value: undefined }),
+  );
+const revoked = () => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+const errorWithMessage = (message: unknown) =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        return message;
+      },
+    },
+  });
+const CONSTANT = 'unreadable thrown value';
+
+describe('KS-1868 the revoke-on-rotate catches turn a hostile message into text', () => {
+  it('control ks1868 C1 revokePriorConnectorKeys: an ordinary Error logs its message and the function answers null', async () => {
+    h.toThrow = new Error('db down');
+    expect(await settle(revokePriorConnectorKeys(CONNECTOR, TENANT, 'new-key'))).toEqual({ rejected: false, value: null });
+    expect(LINES().map((l) => l.error)).toEqual(['db down']);
+  });
+
+  it('control ks1868 C2 revokePriorConnectorKeys: a thrown plain string is logged as that text and the function answers null', async () => {
+    h.toThrow = 'plain boom';
+    expect(await settle(revokePriorConnectorKeys(CONNECTOR, TENANT, 'new-key'))).toEqual({ rejected: false, value: null });
+    expect(LINES().map((l) => l.error)).toEqual(['plain boom']);
+  });
+
+  it('control ks1868 C3 saveKeyAndRetirePriors: an ordinary Error logs its message, the retire is rolled back alone and the mint stands', async () => {
+    h.toThrow = new Error('db down');
+    expect(await settle(saveKeyAndRetirePriors(KEY, CONNECTOR))).toEqual({ rejected: false, value: null });
+    expect(h.sql).toContain('ROLLBACK TO SAVEPOINT ks1549_retire');
+    expect(h.sql).not.toContain('RELEASE SAVEPOINT ks1549_retire');
+    expect(memApiKeys.has(KEY.id)).toBe(true);
+    expect(LINES().map((l) => l.error)).toEqual(['db down']);
+  });
+
+  it('control ks1868 C4 saveKeyAndRetirePriors: a thrown plain string is logged as that text and the mint stands', async () => {
+    h.toThrow = 'plain boom';
+    expect(await settle(saveKeyAndRetirePriors(KEY, CONNECTOR))).toEqual({ rejected: false, value: null });
+    expect(h.sql).toContain('ROLLBACK TO SAVEPOINT ks1549_retire');
+    expect(memApiKeys.has(KEY.id)).toBe(true);
+    expect(LINES().map((l) => l.error)).toEqual(['plain boom']);
+  });
+
+  it('RED ks1868 R1 revokePriorConnectorKeys: an Error whose message is a revoked Proxy logs the constant and the function answers null', async () => {
+    h.toThrow = errorWithMessage(revoked());
+    expect(await settle(revokePriorConnectorKeys(CONNECTOR, TENANT, 'new-key'))).toEqual({ rejected: false, value: null });
+    expect(LINES().map((l) => l.error)).toEqual([CONSTANT]);
+  });
+
+  it('RED ks1868 R2 revokePriorConnectorKeys: an Error whose message is a null-prototype object logs the constant and the function answers null', async () => {
+    h.toThrow = errorWithMessage(Object.create(null));
+    expect(await settle(revokePriorConnectorKeys(CONNECTOR, TENANT, 'new-key'))).toEqual({ rejected: false, value: null });
+    expect(LINES().map((l) => l.error)).toEqual([CONSTANT]);
+  });
+
+  it('RED ks1868 R3 revokePriorConnectorKeys: an Error whose message is a Symbol logs the Symbol text and the function answers null', async () => {
+    h.toThrow = errorWithMessage(Symbol('ks1868'));
+    expect(await settle(revokePriorConnectorKeys(CONNECTOR, TENANT, 'new-key'))).toEqual({ rejected: false, value: null });
+    expect(LINES().map((l) => l.error)).toEqual(['Symbol(ks1868)']);
+  });
+
+  it('RED ks1868 R4 saveKeyAndRetirePriors: an Error whose message is a revoked Proxy logs the constant, the retire is rolled back alone and the mint stands', async () => {
+    h.toThrow = errorWithMessage(revoked());
+    expect(await settle(saveKeyAndRetirePriors(KEY, CONNECTOR))).toEqual({ rejected: false, value: null });
+    expect(h.sql).toContain('ROLLBACK TO SAVEPOINT ks1549_retire');
+    expect(h.sql).not.toContain('RELEASE SAVEPOINT ks1549_retire');
+    expect(memApiKeys.has(KEY.id)).toBe(true);
+    expect(LINES().map((l) => l.error)).toEqual([CONSTANT]);
+  });
+
+  it('RED ks1868 R5 saveKeyAndRetirePriors: an Error whose message is a null-prototype object logs the constant, the retire is rolled back alone and the mint stands', async () => {
+    h.toThrow = errorWithMessage(Object.create(null));
+    expect(await settle(saveKeyAndRetirePriors(KEY, CONNECTOR))).toEqual({ rejected: false, value: null });
+    expect(h.sql).toContain('ROLLBACK TO SAVEPOINT ks1549_retire');
+    expect(memApiKeys.has(KEY.id)).toBe(true);
+    expect(LINES().map((l) => l.error)).toEqual([CONSTANT]);
+  });
+
+  it('RED ks1868 R6 saveKeyAndRetirePriors: an Error whose message is a Symbol logs the Symbol text, the retire is rolled back alone and the mint stands', async () => {
+    h.toThrow = errorWithMessage(Symbol('ks1868'));
+    expect(await settle(saveKeyAndRetirePriors(KEY, CONNECTOR))).toEqual({ rejected: false, value: null });
+    expect(h.sql).toContain('ROLLBACK TO SAVEPOINT ks1549_retire');
+    expect(memApiKeys.has(KEY.id)).toBe(true);
+    expect(LINES().map((l) => l.error)).toEqual(['Symbol(ks1868)']);
+  });
+});
```
