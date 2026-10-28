# READY — KS-1467-KS-1467-ks_1467_p1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p1/out.md.checker/patch.diff`** (from `ls` at 13:50 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p1/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p1/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p1-control-r4/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:50 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/middleware/errorHandler.ts , Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/middleware/errorHandler.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/services/auth/src/middleware/errorHandler.ts
2	2	Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts
104	0	Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (3 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: errorHandler.ts passwordLoginGate.ts`
- CODE_PATCH2 (rung 3, 2 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/middleware/errorHandler.ts`, `Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/middleware/errorHandler.ts 1 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts 2 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts 104 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/middleware/errorHandler.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (21 failed / 34 run; controls green; assertion reds)` [red_first.json: failed=21 of total=34; red cell(s): ["KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P1 'BadRequestError': an instance is an instance of its own class", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P1 'UnauthorizedError': an instance is an instance of its own class", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P1 'ForbiddenError': an instance is an instance of its own class", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P1 'NotFoundError': an instance is an instance of its own class", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P1 'ConflictError': an instance is an instance of its own class", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P1 'ValidationError': an instance is an instance of its own class", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P1 'TooManyRequestsError': an instance is an instance of its own class", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P1 'ServiceUnavailableError': an instance is an instance of its own class", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P1 'MfaRequiredError': an instance is an instance of its own class", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P2 'BadRequestError': the prototype of an instance is the class prototype", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P2 'UnauthorizedError': the prototype of an instance is the class prototype", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P2 'ForbiddenError': the prototype of an instance is the class prototype", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P2 'NotFoundError': the prototype of an instance is the class prototype", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P2 'ConflictError': the prototype of an instance is the class prototype", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P2 'ValidationError': the prototype of an instance is the class prototype", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P2 'TooManyRequestsError': the prototype of an instance is the class prototype", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P2 'ServiceUnavailableError': the prototype of an instance is the class prototype", "KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P2 'MfaRequiredError': the prototype of an instance is the class prototype", 'KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 P3 a two-level subclass is an instance of both of its classes', 'KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 H1 the handler answers a ValidationError with its details', 'KS-1467: auth AppError subclasses keep their own prototype RED KS-1467 S1 the comment above the 503 statusCode check no longer claims instanceof is always false']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (34 passed / 34 run)` [green_after.json: failed=0 of total=34, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1200 failed=0 | after: total=1234 failed=0` · `NEW reds: []` [baseline_suite.json total=1200 failed=0; after_suite.json total=1234 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=2 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/middleware/errorHandler.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts` (+104/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/auth/src/middleware/errorHandler.ts, Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1467_p1/KS-1467.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/middleware/errorHandler.ts b/Blockchain/Dev/services/auth/src/middleware/errorHandler.ts
--- a/Blockchain/Dev/services/auth/src/middleware/errorHandler.ts
+++ b/Blockchain/Dev/services/auth/src/middleware/errorHandler.ts
@@ -22,6 +22,6 @@
     this.statusCode = statusCode;
     this.code = code;
     this.isOperational = isOperational;
-    Object.setPrototypeOf(this, AppError.prototype);
+    Object.setPrototypeOf(this, new.target.prototype);
   }
 }
diff --git a/Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts b/Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts
--- a/Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts
+++ b/Blockchain/Dev/services/auth/src/services/passwordLoginGate.ts
@@ -284,8 +284,8 @@
             'Backup-code sign-in',
           );
         } catch (err) {
-          // `statusCode`, not `instanceof`: AppError's constructor ends with Object.setPrototypeOf(this, AppError.prototype), which
-          // resets every subclass instance to the base prototype, so `err instanceof ServiceUnavailableError` is always false here.
+          // `statusCode`, not `instanceof`: this reads the same for an AppError from any package. (KS-1467: AppError's constructor used to end with
+          // Object.setPrototypeOf(this, AppError.prototype), which reset every subclass instance, so `instanceof ServiceUnavailableError` was always false here.)
           if ((err as { statusCode?: unknown } | null)?.statusCode === 503) throw new ServiceUnavailableError(BACKUP_CODE_UNCONFIRMED_MESSAGE);
           throw err;
         }
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1467-auth-app-error-subclasses-keep-their-own-prototype.test.ts
@@ -0,0 +1,104 @@
+// KS-1467 (services/auth middleware/errorHandler.ts): AppError's constructor ended with `Object.setPrototypeOf(this, AppError.prototype)`, which resets EVERY subclass instance to the base
+// prototype. So `err instanceof ValidationError` (or any other subclass) was always false, and the errorHandler's own `err instanceof ValidationError && err.details` branch could never run:
+// the password-strength `feedback` that registration, password reset and password change build never reached the client. The constructor now uses `new.target.prototype`.
+// P1/P2 pin the prototype of each subclass (and the two-level chain), H1 pins the handler's `details` branch, S1 pins that the stale comment in passwordLoginGate.ts is reworded, C1 to C4 and S2 pin what must not change.
+import { describe, it, expect, vi } from 'vitest';
+import { readFileSync } from 'node:fs';
+import { join } from 'node:path';
+import type { Request, Response, NextFunction } from 'express';
+import * as mod from '../middleware/errorHandler';
+
+vi.mock('../utils/logger', () => ({
+  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() },
+  createLogger: vi.fn(),
+  validateEnv: vi.fn(),
+}));
+
+const { errorHandler, AppError } = mod;
+
+const FACTORIES = [
+  { name: 'BadRequestError', make: () => new mod.BadRequestError('x'), cls: mod.BadRequestError, status: 400 },
+  { name: 'UnauthorizedError', make: () => new mod.UnauthorizedError('x'), cls: mod.UnauthorizedError, status: 401 },
+  { name: 'ForbiddenError', make: () => new mod.ForbiddenError('x'), cls: mod.ForbiddenError, status: 403 },
+  { name: 'NotFoundError', make: () => new mod.NotFoundError('Thing'), cls: mod.NotFoundError, status: 404 },
+  { name: 'ConflictError', make: () => new mod.ConflictError('x'), cls: mod.ConflictError, status: 409 },
+  { name: 'ValidationError', make: () => new mod.ValidationError('x', { a: 1 }), cls: mod.ValidationError, status: 422 },
+  { name: 'TooManyRequestsError', make: () => new mod.TooManyRequestsError(), cls: mod.TooManyRequestsError, status: 429 },
+  { name: 'ServiceUnavailableError', make: () => new mod.ServiceUnavailableError('x'), cls: mod.ServiceUnavailableError, status: 503 },
+  { name: 'MfaRequiredError', make: () => new mod.MfaRequiredError(), cls: mod.MfaRequiredError, status: 403 },
+] as const;
+
+interface Captured {
+  statusCode: number;
+  body: { success: boolean; error: { code: string; message: string; details?: unknown } };
+}
+
+function run(err: Error): Captured {
+  const captured = { statusCode: 0, body: undefined } as unknown as Captured;
+  const res = {
+    status(code: number) {
+      captured.statusCode = code;
+      return this;
+    },
+    json(payload: unknown) {
+      captured.body = payload as Captured['body'];
+      return this;
+    },
+  } as unknown as Response;
+  const req = { path: '/api/auth/register', method: 'POST' } as unknown as Request;
+  errorHandler(err, req, res, (() => undefined) as unknown as NextFunction);
+  return captured;
+}
+
+describe('KS-1467: auth AppError subclasses keep their own prototype', () => {
+  it.each(FACTORIES)('RED KS-1467 P1 $name: an instance is an instance of its own class', ({ make, cls }) => {
+    expect(make() instanceof cls).toBe(true);
+  });
+
+  it.each(FACTORIES)('RED KS-1467 P2 $name: the prototype of an instance is the class prototype', ({ make, cls }) => {
+    expect(Object.getPrototypeOf(make())).toBe(cls.prototype);
+  });
+
+  it('RED KS-1467 P3 a two-level subclass is an instance of both of its classes', () => {
+    const e = new mod.InvalidCredentialsError();
+    expect([e instanceof mod.InvalidCredentialsError, e instanceof mod.UnauthorizedError, e instanceof AppError]).toEqual([true, true, true]);
+  });
+
+  it('RED KS-1467 H1 the handler answers a ValidationError with its details', () => {
+    const r = run(new mod.ValidationError('New password is too weak', { feedback: ['add a number'] }));
+    expect(r.statusCode).toBe(422);
+    expect(r.body.error).toEqual({ code: 'VALIDATION_ERROR', message: 'New password is too weak', details: { feedback: ['add a number'] } });
+  });
+
+  it('RED KS-1467 S1 the comment above the 503 statusCode check no longer claims instanceof is always false', () => {
+    const source = readFileSync(join(process.cwd(), 'src', 'services', 'passwordLoginGate.ts'), 'utf8');
+    expect(source).not.toContain('is always false here');
+  });
+
+  it('control KS-1467 S2 passwordLoginGate.ts still reaches the 503 by statusCode and still throws the unconfirmed message', () => {
+    const source = readFileSync(join(process.cwd(), 'src', 'services', 'passwordLoginGate.ts'), 'utf8');
+    expect(source).toContain('?.statusCode === 503) throw new ServiceUnavailableError(BACKUP_CODE_UNCONFIRMED_MESSAGE);');
+  });
+
+  it.each(FACTORIES)('control KS-1467 C1 $name: an instance is still an AppError and an Error with its status', ({ make, status }) => {
+    const e = make();
+    expect([e instanceof AppError, e instanceof Error, e.statusCode]).toEqual([true, true, status]);
+  });
+
+  it('control KS-1467 C2 a plain AppError is still an AppError with its own prototype', () => {
+    const e = new AppError('teapot', 418, 'TEAPOT');
+    expect([e instanceof AppError, Object.getPrototypeOf(e) === AppError.prototype, e.code]).toEqual([true, true, 'TEAPOT']);
+  });
+
+  it('control KS-1467 C3 a ValidationError without details is answered without a details key', () => {
+    const r = run(new mod.ValidationError('bad'));
+    expect(r.statusCode).toBe(422);
+    expect(r.body.error).toEqual({ code: 'VALIDATION_ERROR', message: 'bad' });
+  });
+
+  it('control KS-1467 C4 a BadRequestError is answered with code and message only', () => {
+    const r = run(new mod.BadRequestError('nope'));
+    expect(r.statusCode).toBe(400);
+    expect(r.body.error).toEqual({ code: 'BAD_REQUEST', message: 'nope' });
+  });
+});
```

## DECISION NOTE (source-read, Spark operator for Wednesday, 2026-10-28 PM) - HOLD-WITH-DECISION: put the 422 `details` change to the owner BEFORE raising
- What the fix does: `Object.setPrototypeOf(this, new.target.prototype)` in services/auth `AppError` makes `instanceof <subclass>` true for every subclass. The visible consequence is in `errorHandler.ts:296`: `if (err instanceof ValidationError && err.details) errorPayload.details = err.details;` has NEVER run (instanceof was always false), so it starts to run. The ticket itself says "decide deliberately that 422 responses now carry details".
- Measured at the tip (65bc28234507, cache clone): `throw new ValidationError(` appears 4 times in services/auth non-test code. THREE carry details and will start sending them in the 422 body: `routes/auth.ts:204` and `:822` (`{ feedback: strength.feedback }`, password-strength feedback on register and reset) and `routes/users.ts:993` (`{ feedback: strength.feedback }`, change-password). `routes/auth.ts:173` (role not permitted on /register) has NO details, so its body is unchanged. So the response change is exactly: a weak-password 422 now also carries `error.details = { feedback: ... }` (the zxcvbn warning/suggestions). The owner decides whether that is wanted (it is what the frontend was written to show) and whether the feedback can ever echo the candidate password.
- No other `instanceof` flip in services/auth: the only `instanceof <X>Error` sites are `instanceof AppError` (base, unchanged) and `instanceof IssuerCertError` (5 sites in routes/issuerCerts.ts; `IssuerCertError extends Error`, NOT AppError, so it is unaffected).
- passwordLoginGate.ts comment reword is accurate (statusCode check still reads the same); the 503 path is unchanged.
- Gate notes 1 and 2 of KS-1467 are deliberately NOT in this patch (note 1 was dropped because the builder refuses a pure move). The `packages/shared` half is the separate held READY `..._ks_1467_p2_shared_...` (shared `errorHandler` formats details from any AppError already; no `instanceof <subclass>` of a shared subclass exists in services/ at the tip, so that half changes no handler).
- Verdict: HOLD-WITH-DECISION (do not close KS-1467 on this; Refs only).
