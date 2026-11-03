# READY — KS-1868-KS-1868-O93-P5 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p5_auth_user_repo_mfa_reencrypt_catches_guard_message-r2/out.md.checker/patch.diff`** (from `ls` at 11:50 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p5_auth_user_repo_mfa_reencrypt_catches_guard_message-r2/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p5_auth_user_repo_mfa_reencrypt_catches_guard_message-r2/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p5_auth_user_repo_mfa_reencrypt_catches_guard_message-r2/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p5_auth_user_repo_mfa_reencrypt_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 11:50 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p5_auth_user_repo_mfa_reencrypt_catches_guard_message-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `19fc68309c254227e751b3186970360f921fdc74`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/repositories/userRepo.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-repo-mfa-reencrypt-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/repositories/userRepo.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-repo-mfa-reencrypt-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
16	2	Blockchain/Dev/services/auth/src/repositories/userRepo.ts
157	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-repo-mfa-reencrypt-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (16 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: userRepo.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/repositories/userRepo.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-repo-mfa-reencrypt-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/repositories/userRepo.ts 16 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-repo-mfa-reencrypt-catches-unreadable-throw.test.ts 157 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/repositories/userRepo.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-repo-mfa-reencrypt-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 the userRepo re-encrypt catches resolve and log text for a hostile thrown value RED ks1868 R1: a revoked Proxy from the mfa re-encrypt query is logged as text and the call resolves, as for an ordinary Error', 'KS-1868 the userRepo re-encrypt catches resolve and log text for a hostile thrown value RED ks1868 R2: an Error whose message is a Symbol from the mfa re-encrypt query is logged as text and the call resolves, as for an ordinary Error', 'KS-1868 the userRepo re-encrypt catches resolve and log text for a hostile thrown value RED ks1868 R3: an Error whose message getter throws from the mfa re-encrypt query is logged as text and the call resolves, as for an ordinary Error', 'KS-1868 the userRepo re-encrypt catches resolve and log text for a hostile thrown value RED ks1868 R4: a revoked Proxy from the platform-admin re-encrypt query is logged as text and the call resolves, as for an ordinary Error', 'KS-1868 the userRepo re-encrypt catches resolve and log text for a hostile thrown value RED ks1868 R5: an Error whose message is a Symbol from the platform-admin re-encrypt query is logged as text and the call resolves, as for an ordinary Error', 'KS-1868 the userRepo re-encrypt catches resolve and log text for a hostile thrown value RED ks1868 R6: an Error whose message getter throws from the platform-admin re-encrypt query is logged as text and the call resolves, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1561 failed=3 | after: total=1570 failed=1` · `NEW reds: []` [baseline_suite.json total=1561 failed=3; after_suite.json total=1570 failed=1]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/repositories/userRepo.ts` (+16/-2 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-repo-mfa-reencrypt-catches-unreadable-throw.test.ts` (+157/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/repositories/userRepo.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `19fc68309c254227e751b3186970360f921fdc74` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p5_auth_user_repo_mfa_reencrypt_catches_guard_message-r2/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o93_p5_auth_user_repo_mfa_reencrypt_catches_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p5_auth_user_repo_mfa_reencrypt_catches_guard_message-r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/repositories/userRepo.ts b/Blockchain/Dev/services/auth/src/repositories/userRepo.ts
--- a/Blockchain/Dev/services/auth/src/repositories/userRepo.ts
+++ b/Blockchain/Dev/services/auth/src/repositories/userRepo.ts
@@ -1911,6 +1911,13 @@
     }
   } catch (err: any) {
     // Never fail the verify on a migration hiccup — just log.
-    logger.error('[KS-158] mfa_secret re-encrypt failed', { userId, error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('[KS-158] mfa_secret re-encrypt failed', { userId, error: reason });
   }
 }
@@ -1979,6 +1986,13 @@
     }
   } catch (err: any) {
     // Never fail the login on a migration hiccup — just log.
-    logger.error('[KS-171] platform_admins.mfa_secret re-encrypt failed', { adminId, error: err?.message });
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('[KS-171] platform_admins.mfa_secret re-encrypt failed', { adminId, error: reason });
   }
 }
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-repo-mfa-reencrypt-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-repo-mfa-reencrypt-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-auth-user-repo-mfa-reencrypt-catches-unreadable-throw.test.ts
@@ -0,0 +1,157 @@
+import { describe, it, expect, beforeEach, afterAll, vi } from 'vitest';
+
+// KS-1868 (operator 93 screen, auth userRepo): the catches of reencryptMfaSecretIfLegacy (line 1914) and reencryptPlatformAdminMfaSecretIfLegacy
+// (line 1982) of services/auth/src/repositories/userRepo.ts pass `err?.message` straight into the error line's meta object, unguarded. `?.` guards
+// null and undefined only: a thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the catch throw, so the
+// function REJECTS although both are documented as never failing the verify / the login ("never throws - a migration hiccup must not fail the login"),
+// where an ordinary Error is logged and the function resolves; an Error whose message is readable but not a string (a Symbol) is handed to the logger
+// uncoerced and silently dropped from the JSON line. The cells make the first query of each function reject with such a value and assert the function
+// resolves and the line carries text (the constant when the value cannot be turned into text). Harness: the ks1186 userRepo suite's mocks (the shared
+// module spread from the real one, the subject-DEK store and the logger as stand-ins) with `../db` and `pg` replaced by plain stand-ins that reject the
+// query with the cell's value (no database, no network).
+const h = vi.hoisted(() => {
+  process.env.NODE_ENV = 'development';
+  return { toThrow: undefined as unknown, errors: [] as unknown[][] };
+});
+
+vi.mock('@secuura/shared', async (importOriginal) => {
+  const actual = await importOriginal<Record<string, unknown>>();
+  return {
+    ...actual,
+    encryptField: async (v: string) => v,
+    decryptField: async (v: string) => v,
+    encryptFieldWithDek: async (v: string) => v,
+    decryptFieldWithDek: async (v: string) => v,
+    isSubjectDekCiphertext: () => false,
+    isEncryptedPii: () => false,
+    lookupHash: (v: string) => `hash:${v}`,
+  };
+});
+
+vi.mock('../services/subjectDeks', () => ({
+  subjectDeks: {
+    getDek: async () => 'test-dek',
+    getOrCreateDek: async () => 'test-dek',
+  },
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    info: () => undefined,
+    debug: () => undefined,
+    warn: () => undefined,
+    error: (...args: unknown[]) => {
+      h.errors.push(args);
+    },
+  },
+}));
+
+vi.mock('../db', () => ({
+  query: (..._args: unknown[]) => Promise.reject(h.toThrow),
+}));
+
+vi.mock('pg', () => ({
+  Pool: function PoolMock() {
+    return {
+      query: (..._args: unknown[]) => Promise.reject(h.toThrow),
+      end: async () => undefined,
+    };
+  },
+}));
+
+import { reencryptMfaSecretIfLegacy, reencryptPlatformAdminMfaSecretIfLegacy } from '../repositories/userRepo';
+
+const MFA = '[KS-158] mfa_secret re-encrypt failed';
+const ADMIN = '[KS-171] platform_admins.mfa_secret re-encrypt failed';
+const realPlatformUrl = process.env.PLATFORM_DATABASE_URL;
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.errors.length = 0;
+  process.env.PLATFORM_DATABASE_URL = 'postgresql://test:test@localhost:5432/platform';
+});
+afterAll(() => {
+  if (realPlatformUrl === undefined) delete process.env.PLATFORM_DATABASE_URL;
+  else process.env.PLATFORM_DATABASE_URL = realPlatformUrl;
+});
+
+const LINE = (message: string): Record<string, unknown>[] =>
+  h.errors.filter((a) => a[0] === message).map((a) => a[1] as Record<string, unknown>);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (o: Record<string, unknown> | undefined): string => (typeof o?.error === 'string' ? (o.error as string) : '<' + typeof o?.error + '>');
+
+async function run(which: 'mfa' | 'admin', value: unknown): Promise<{ threw: boolean }> {
+  h.toThrow = value;
+  try {
+    if (which === 'mfa') await reencryptMfaSecretIfLegacy('user-1');
+    else await reencryptPlatformAdminMfaSecretIfLegacy('admin-1');
+    return { threw: false };
+  } catch {
+    return { threw: true };
+  }
+}
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+/** An Error whose `message` getter succeeds and returns the value m. */
+const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 the userRepo re-encrypt catches resolve and log text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the mfa re-encrypt query is logged with its message and the call resolves', async () => {
+    expect(await run('mfa', new Error('db boom'))).toEqual({ threw: false });
+    expect(LINE(MFA)).toHaveLength(1);
+    expect(reasonOf(LINE(MFA)[0])).toBe('db boom');
+    expect(LINE(MFA)[0].userId).toBe('user-1');
+  });
+  it('control ks1868 C2: a thrown plain string from the mfa re-encrypt query is logged without a message and the call resolves', async () => {
+    expect(await run('mfa', 'plain boom')).toEqual({ threw: false });
+    expect(LINE(MFA)).toHaveLength(1);
+    expect(reasonOf(LINE(MFA)[0])).toBe('<undefined>');
+  });
+  it('control ks1868 C3: an ordinary Error from the platform-admin re-encrypt query is logged with its message and the call resolves', async () => {
+    expect(await run('admin', new Error('platform boom'))).toEqual({ threw: false });
+    expect(LINE(ADMIN)).toHaveLength(1);
+    expect(reasonOf(LINE(ADMIN)[0])).toBe('platform boom');
+    expect(LINE(ADMIN)[0].adminId).toBe('admin-1');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the mfa re-encrypt query is logged as text and the call resolves, as for an ordinary Error', async () => {
+    expect(await run('mfa', revokedProxy())).toEqual({ threw: false });
+    expect(LINE(MFA)).toHaveLength(1);
+    expect(reasonOf(LINE(MFA)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message is a Symbol from the mfa re-encrypt query is logged as text and the call resolves, as for an ordinary Error', async () => {
+    expect(await run('mfa', withMessage(Symbol('ks1868')))).toEqual({ threw: false });
+    expect(LINE(MFA)).toHaveLength(1);
+    expect(reasonOf(LINE(MFA)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R3: an Error whose message getter throws from the mfa re-encrypt query is logged as text and the call resolves, as for an ordinary Error', async () => {
+    expect(await run('mfa', getterThrows())).toEqual({ threw: false });
+    expect(LINE(MFA)).toHaveLength(1);
+    expect(reasonOf(LINE(MFA)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R4: a revoked Proxy from the platform-admin re-encrypt query is logged as text and the call resolves, as for an ordinary Error', async () => {
+    expect(await run('admin', revokedProxy())).toEqual({ threw: false });
+    expect(LINE(ADMIN)).toHaveLength(1);
+    expect(reasonOf(LINE(ADMIN)[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R5: an Error whose message is a Symbol from the platform-admin re-encrypt query is logged as text and the call resolves, as for an ordinary Error', async () => {
+    expect(await run('admin', withMessage(Symbol('ks1868')))).toEqual({ threw: false });
+    expect(LINE(ADMIN)).toHaveLength(1);
+    expect(reasonOf(LINE(ADMIN)[0])).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R6: an Error whose message getter throws from the platform-admin re-encrypt query is logged as text and the call resolves, as for an ordinary Error', async () => {
+    expect(await run('admin', getterThrows())).toEqual({ threw: false });
+    expect(LINE(ADMIN)).toHaveLength(1);
+    expect(reasonOf(LINE(ADMIN)[0])).toBe('unreadable thrown value');
+  });
+});
```
