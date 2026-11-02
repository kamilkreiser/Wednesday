# READY — KS-1868-KS-1868-O90-P13 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p13_transfer_delegation_service_verify_and_expire_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 06:16 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p13_transfer_delegation_service_verify_and_expire_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p13_transfer_delegation_service_verify_and_expire_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p13_transfer_delegation_service_verify_and_expire_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p13_transfer_delegation_service_verify_and_expire_catches_guard_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 06:16 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p13_transfer_delegation_service_verify_and_expire_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `4d1ab2cb6574e2b221353ac3a1de56d515711aaf`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/transfer/src/services/delegationService.ts } + { Blockchain/Dev/services/transfer/src/__tests__/ks1868-delegation-service-db-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/transfer/src/services/delegationService.ts` (product) and `Blockchain/Dev/services/transfer/src/__tests__/ks1868-delegation-service-db-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
16	2	Blockchain/Dev/services/transfer/src/services/delegationService.ts
109	0	Blockchain/Dev/services/transfer/src/__tests__/ks1868-delegation-service-db-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (16 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: delegationService.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/transfer/src/services/delegationService.ts`; test(s): `Blockchain/Dev/services/transfer/src/__tests__/ks1868-delegation-service-db-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/transfer/src/services/delegationService.ts 16 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/transfer/src/__tests__/ks1868-delegation-service-db-catches-unreadable-throw.test.ts 109 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/transfer/src/services/delegationService.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/transfer/src/__tests__/ks1868-delegation-service-db-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 delegation service: the verifyDbReady and processExpiredDelegations catches survive a thrown value they cannot read RED ks1868 R1: a revoked Proxy from verifyDbReady is written as text and the call resolves', 'KS-1868 delegation service: the verifyDbReady and processExpiredDelegations catches survive a thrown value they cannot read RED ks1868 R2: an Error whose message getter throws from verifyDbReady is written as text and the call resolves', 'KS-1868 delegation service: the verifyDbReady and processExpiredDelegations catches survive a thrown value they cannot read RED ks1868 R3: a revoked Proxy from processExpiredDelegations is written as text and 0 is answered', 'KS-1868 delegation service: the verifyDbReady and processExpiredDelegations catches survive a thrown value they cannot read RED ks1868 R4: an Error whose message getter throws from processExpiredDelegations is written as text and 0 is answered']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=129 failed=1 | after: total=135 failed=0` · `NEW reds: []` [baseline_suite.json total=129 failed=1; after_suite.json total=135 failed=0]
- A6 [verbatim]: `PASS A6 whole services/transfer suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/transfer: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/transfer/src/services/delegationService.ts` (+16/-2 per numstat.out) and the test file `Blockchain/Dev/services/transfer/src/__tests__/ks1868-delegation-service-db-catches-unreadable-throw.test.ts` (+109/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/transfer/src/services/delegationService.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `4d1ab2cb6574e2b221353ac3a1de56d515711aaf` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p13_transfer_delegation_service_verify_and_expire_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o90_p13_transfer_delegation_service_verify_and_expire_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o90_p13_transfer_delegation_service_verify_and_expire_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/transfer/src/services/delegationService.ts b/Blockchain/Dev/services/transfer/src/services/delegationService.ts
--- a/Blockchain/Dev/services/transfer/src/services/delegationService.ts
+++ b/Blockchain/Dev/services/transfer/src/services/delegationService.ts
@@ -167,6 +167,13 @@
   try {
     await query('SELECT 1 FROM svc_transfer_delegations LIMIT 1');
   } catch (err: any) {
-    console.warn('[delegationService] DB tables not ready:', err?.message);
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    console.warn('[delegationService] DB tables not ready:', reason);
   }
 }
@@ -491,7 +498,14 @@
       );
       return result.rowCount ?? 0;
     } catch (err: any) {
-      console.error('[delegationService] processExpiredDelegations error:', err?.message);
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      console.error('[delegationService] processExpiredDelegations error:', reason);
       return 0;
     }
   }
diff --git a/Blockchain/Dev/services/transfer/src/__tests__/ks1868-delegation-service-db-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/transfer/src/__tests__/ks1868-delegation-service-db-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/transfer/src/__tests__/ks1868-delegation-service-db-catches-unreadable-throw.test.ts
@@ -0,0 +1,109 @@
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+
+// KS-1868 (operator 90 screen, transfer delegation service): two catches of services/transfer/src/services/delegationService.ts pass
+// `err?.message` straight into a console call, unguarded: verifyDbReady (line 170, console.warn) and processExpiredDelegations (line 494,
+// console.error). `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy, an Error whose message
+// getter throws) makes the catch throw while the call's arguments are built, so the call REJECTS where an ordinary Error gets a
+// console line and the documented outcome (verifyDbReady resolves; processExpiredDelegations answers 0). The cells make the database
+// stand-in reject with such a value, replace console.warn and console.error with plain recorders, and assert the call still resolves
+// with that outcome and the recorded argument is text. The stand-in rejects with a plain function, not vi.fn(): a spy could inspect a
+// revoked Proxy and fail before the code under test saw it. Harness: the real module with ../db replaced by a plain stand-in; no
+// database, no network.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  warns: [] as unknown[][],
+  errors: [] as unknown[][],
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: (..._args: unknown[]) => Promise.reject(h.toThrow),
+}));
+
+import { verifyDbReady, delegationService } from '../services/delegationService';
+
+const realWarn = console.warn;
+const realError = console.error;
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.warns.length = 0;
+  h.errors.length = 0;
+  console.warn = (...args: unknown[]) => {
+    h.warns.push(args);
+  };
+  console.error = (...args: unknown[]) => {
+    h.errors.push(args);
+  };
+});
+afterEach(() => {
+  console.warn = realWarn;
+  console.error = realError;
+});
+
+const WARN = '[delegationService] DB tables not ready:';
+const ERROR = '[delegationService] processExpiredDelegations error:';
+/** The second console argument as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const argOf = (calls: unknown[][], first: string): string => {
+  const c = calls.filter((a) => a[0] === first);
+  if (c.length !== 1) return '<' + c.length + ' calls>';
+  return typeof c[0][1] === 'string' ? (c[0][1] as string) : '<' + typeof c[0][1] + '>';
+};
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+async function verifyWith(value: unknown): Promise<{ threw: boolean }> {
+  h.toThrow = value;
+  try {
+    await verifyDbReady();
+    return { threw: false };
+  } catch {
+    return { threw: true };
+  }
+}
+async function expireWith(value: unknown): Promise<{ threw: boolean; count?: number }> {
+  h.toThrow = value;
+  try {
+    return { threw: false, count: await delegationService.processExpiredDelegations() };
+  } catch {
+    return { threw: true };
+  }
+}
+
+describe('KS-1868 delegation service: the verifyDbReady and processExpiredDelegations catches survive a thrown value they cannot read', () => {
+  it('control ks1868 C1: an ordinary Error from verifyDbReady is written with its message and the call resolves', async () => {
+    expect(await verifyWith(new Error('db boom'))).toEqual({ threw: false });
+    expect(argOf(h.warns, WARN)).toBe('db boom');
+  });
+  it('control ks1868 C2: an ordinary Error from processExpiredDelegations is written with its message and 0 is answered', async () => {
+    expect(await expireWith(new Error('db boom'))).toEqual({ threw: false, count: 0 });
+    expect(argOf(h.errors, ERROR)).toBe('db boom');
+  });
+  it('RED ks1868 R1: a revoked Proxy from verifyDbReady is written as text and the call resolves', async () => {
+    expect(await verifyWith(revokedProxy())).toEqual({ threw: false });
+    expect(argOf(h.warns, WARN)).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message getter throws from verifyDbReady is written as text and the call resolves', async () => {
+    expect(await verifyWith(getterThrows())).toEqual({ threw: false });
+    expect(argOf(h.warns, WARN)).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: a revoked Proxy from processExpiredDelegations is written as text and 0 is answered', async () => {
+    expect(await expireWith(revokedProxy())).toEqual({ threw: false, count: 0 });
+    expect(argOf(h.errors, ERROR)).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R4: an Error whose message getter throws from processExpiredDelegations is written as text and 0 is answered', async () => {
+    expect(await expireWith(getterThrows())).toEqual({ threw: false, count: 0 });
+    expect(argOf(h.errors, ERROR)).toBe('unreadable thrown value');
+  });
+});
```
