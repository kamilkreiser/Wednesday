# READY — KS-1868-KS-1868-O92-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p3_referral_service_save_code_and_get_code_by_string_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 08:40 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p3_referral_service_save_code_and_get_code_by_string_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p3_referral_service_save_code_and_get_code_by_string_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p3_referral_service_save_code_and_get_code_by_string_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p3_referral_service_save_code_and_get_code_by_string_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 08:40 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p3_referral_service_save_code_and_get_code_by_string_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `b85b7b6786fa6329b6f781cebf2475147738004e`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/referral/src/services/referralService.ts } + { Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-service-save-code-and-code-by-string-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/referral/src/services/referralService.ts` (product) and `Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-service-save-code-and-code-by-string-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
18	2	Blockchain/Dev/services/referral/src/services/referralService.ts
111	0	Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-service-save-code-and-code-by-string-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (18 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: referralService.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/referral/src/services/referralService.ts`; test(s): `Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-service-save-code-and-code-by-string-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/referral/src/services/referralService.ts 18 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-service-save-code-and-code-by-string-catches-unreadable-throw.test.ts 111 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/referral/src/services/referralService.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-service-save-code-and-code-by-string-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 referral service: the code read and the code save catches survive a thrown value they cannot read RED ks1868 R1: a revoked Proxy from getCodeByString is logged as text and the fallback is answered', 'KS-1868 referral service: the code read and the code save catches survive a thrown value they cannot read RED ks1868 R2: an Error whose message getter throws from getCodeByString is logged as text and the fallback is answered', 'KS-1868 referral service: the code read and the code save catches survive a thrown value they cannot read RED ks1868 R3: a revoked Proxy from the code save of generateCode is logged as text and the code is still returned', 'KS-1868 referral service: the code read and the code save catches survive a thrown value they cannot read RED ks1868 R4: an Error whose message getter throws from the code save of generateCode is logged as text and the code is still returned']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=36 failed=0 | after: total=42 failed=0` · `NEW reds: []` [baseline_suite.json total=36 failed=0; after_suite.json total=42 failed=0]
- A6 [verbatim]: `PASS A6 whole services/referral suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/referral: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/referral/src/services/referralService.ts` (+18/-2 per numstat.out) and the test file `Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-service-save-code-and-code-by-string-catches-unreadable-throw.test.ts` (+111/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/referral/src/services/referralService.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `b85b7b6786fa6329b6f781cebf2475147738004e` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p3_referral_service_save_code_and_get_code_by_string_catches_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o92_p3_referral_service_save_code_and_get_code_by_string_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o92_p3_referral_service_save_code_and_get_code_by_string_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/referral/src/services/referralService.ts b/Blockchain/Dev/services/referral/src/services/referralService.ts
--- a/Blockchain/Dev/services/referral/src/services/referralService.ts
+++ b/Blockchain/Dev/services/referral/src/services/referralService.ts
@@ -65,5 +65,14 @@
         [c.id, c.code, c.ownerId, c.ownerWalletAddress || null, c.isActive, c.maxUses || null,
          c.currentUses, c.customLabel || null, JSON.stringify(c.metadata || {}), c.createdAt, c.expiresAt || null]
       );
-    } catch (err: any) { logger.error('DB save code failed', { error: err?.message }); }
+    } catch (err: any) {
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('DB save code failed', { error: reason });
+    }
   }
@@ -226,7 +235,14 @@
       if (result.rows.length === 0) return null;
       return this.rowToReferralCode(result.rows[0]);
     } catch (err: any) {
-      logger.error('DB read code by string failed', { error: err?.message, code });
+      let reason: string | null | undefined;
+      try {
+        const m = err?.message;
+        reason = m === undefined || m === null ? m : String(m);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('DB read code by string failed', { error: reason, code });
       return null;
     }
   }
diff --git a/Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-service-save-code-and-code-by-string-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-service-save-code-and-code-by-string-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/referral/src/__tests__/ks1868-referral-service-save-code-and-code-by-string-catches-unreadable-throw.test.ts
@@ -0,0 +1,111 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868 (operator 92 screen, referral service): the save catch of dbSaveReferralCode (line 68) and the read catch of dbGetCodeByString (line 229) of
+// services/referral/src/services/referralService.ts pass `err?.message` straight into the logger's meta object, unguarded. `?.` guards null and undefined
+// only: a thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the catch throw, so generateCode / getCodeByString
+// REJECT where an ordinary Error gets a logged failure and the fallback (the generated code is still returned; `undefined`). The cells make the database
+// stand-in reject the one statement with such a value and assert the public method still resolves with the fallback and the failure is logged as text.
+// The stand-in rejects with a plain function, not vi.fn(): a spy could inspect a revoked Proxy and fail before the code under test saw it. Harness: the
+// real module with ../db and ../utils/logger replaced by plain stand-ins; every other statement answers an empty result; no database, no network.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  failOn: '' as string,
+  logs: [] as { level: string; message: string; meta: Record<string, unknown> | undefined }[],
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: (sql: string, ..._args: unknown[]) =>
+    h.failOn !== '' && String(sql).includes(h.failOn) ? Promise.reject(h.toThrow) : Promise.resolve({ rows: [] }),
+}));
+
+vi.mock('../utils/logger', () => {
+  const rec = (level: string) => (message: string, meta?: Record<string, unknown>) => {
+    h.logs.push({ level, message, meta });
+  };
+  return { createLogger: () => ({ debug: rec('debug'), info: rec('info'), warn: rec('warn'), error: rec('error') }) };
+});
+
+import { referralService } from '../services/referralService';
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.failOn = '';
+  h.logs.length = 0;
+});
+
+const LOG = (message: string) => h.logs.filter((l) => l.message === message);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (l: { meta?: Record<string, unknown> } | undefined): string => {
+  const e = l?.meta?.error;
+  return typeof e === 'string' ? e : '<' + typeof e + '>';
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
+type Out = { threw: boolean; value?: unknown };
+async function run(fn: () => Promise<unknown>, failOn: string, value: unknown): Promise<Out> {
+  h.failOn = failOn;
+  h.toThrow = value;
+  try {
+    return { threw: false, value: await fn() };
+  } catch {
+    return { threw: true };
+  }
+}
+
+const SITES = [
+  { name: 'getCodeByString (dbGetCodeByString)', log: 'DB read code by string failed', failOn: 'WHERE code = $1', call: () => referralService.getCodeByString('KS1868CODE'), fallback: undefined },
+  { name: 'generateCode (dbSaveReferralCode)', log: 'DB save code failed', failOn: 'INSERT INTO svc_referral_codes', call: async () => (await referralService.generateCode('user-ks1868')).ownerId, fallback: 'user-ks1868' },
+];
+
+describe('KS-1868 referral service: the code read and the code save catches survive a thrown value they cannot read', () => {
+  it('control ks1868 C1: an ordinary Error from getCodeByString is logged with its message and the fallback is answered', async () => {
+    const s = SITES[0];
+    expect(await run(s.call, s.failOn, new Error('db boom'))).toEqual({ threw: false, value: s.fallback });
+    expect(LOG(s.log)).toHaveLength(1);
+    expect(reasonOf(LOG(s.log)[0])).toBe('db boom');
+  });
+  it('control ks1868 C2: an ordinary Error from the code save of generateCode is logged with its message and the code is still returned', async () => {
+    const s = SITES[1];
+    expect(await run(s.call, s.failOn, new Error('db boom'))).toEqual({ threw: false, value: s.fallback });
+    expect(LOG(s.log)).toHaveLength(1);
+    expect(reasonOf(LOG(s.log)[0])).toBe('db boom');
+  });
+  it('RED ks1868 R1: a revoked Proxy from getCodeByString is logged as text and the fallback is answered', async () => {
+    const s = SITES[0];
+    expect(await run(s.call, s.failOn, revokedProxy())).toEqual({ threw: false, value: s.fallback });
+    expect(LOG(s.log)).toHaveLength(1);
+    expect(reasonOf(LOG(s.log)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message getter throws from getCodeByString is logged as text and the fallback is answered', async () => {
+    const s = SITES[0];
+    expect(await run(s.call, s.failOn, getterThrows())).toEqual({ threw: false, value: s.fallback });
+    expect(LOG(s.log)).toHaveLength(1);
+    expect(reasonOf(LOG(s.log)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: a revoked Proxy from the code save of generateCode is logged as text and the code is still returned', async () => {
+    const s = SITES[1];
+    expect(await run(s.call, s.failOn, revokedProxy())).toEqual({ threw: false, value: s.fallback });
+    expect(LOG(s.log)).toHaveLength(1);
+    expect(reasonOf(LOG(s.log)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R4: an Error whose message getter throws from the code save of generateCode is logged as text and the code is still returned', async () => {
+    const s = SITES[1];
+    expect(await run(s.call, s.failOn, getterThrows())).toEqual({ threw: false, value: s.fallback });
+    expect(LOG(s.log)).toHaveLength(1);
+    expect(reasonOf(LOG(s.log)[0])).toBe('unreadable thrown value');
+  });
+});
```
