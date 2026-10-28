# READY — KS-1467-KS-1467-ks_1467_p2_shared (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p2_shared/out.md.checker/patch.diff`** (from `ls` at 13:50 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p2_shared/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p2_shared/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p2_shared/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p2_shared-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:50 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p2_shared/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8894c7486f82f6eb682fecb879791f53312537b1`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/packages/shared/src/errors/index.ts , Blockchain/Dev/packages/shared/src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/errors/index.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
1	1	Blockchain/Dev/packages/shared/src/errors/index.ts
73	0	Blockchain/Dev/packages/shared/src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (1 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 1 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/packages/shared/src/errors/index.ts byte-exact incl. leading whitespace (apply mode strict): OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)` [a3i_indent.out: `OK 1 line(s) byte-exact incl. leading whitespace (of 1; 1 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/errors/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts fails at the untouched tip (19 failed / 29 run; controls green; assertion reds)` [red_first.json: failed=19 of total=29; red cell(s): ["KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P1 'BadRequestError': an instance is an instance of its own class", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P1 'UnauthorizedError': an instance is an instance of its own class", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P1 'ForbiddenError': an instance is an instance of its own class", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P1 'NotFoundError': an instance is an instance of its own class", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P1 'ConflictError': an instance is an instance of its own class", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P1 'ValidationError': an instance is an instance of its own class", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P1 'RateLimitError': an instance is an instance of its own class", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P1 'InternalError': an instance is an instance of its own class", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P1 'ServiceUnavailableError': an instance is an instance of its own class", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P2 'BadRequestError': the prototype of an instance is the class prototype", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P2 'UnauthorizedError': the prototype of an instance is the class prototype", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P2 'ForbiddenError': the prototype of an instance is the class prototype", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P2 'NotFoundError': the prototype of an instance is the class prototype", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P2 'ConflictError': the prototype of an instance is the class prototype", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P2 'ValidationError': the prototype of an instance is the class prototype", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P2 'RateLimitError': the prototype of an instance is the class prototype", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P2 'InternalError': the prototype of an instance is the class prototype", "KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P2 'ServiceUnavailableError': the prototype of an instance is the class prototype", 'KS-1467: shared AppError subclasses keep their own prototype RED KS-1467 P3 a two-level subclass is an instance of every class in its chain']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts passes with the product hunk (29 passed / 29 run)` [green_after.json: failed=0 of total=29, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1039 failed=2 | after: total=1068 failed=1` · `NEW reds: []` [baseline_suite.json total=1039 failed=2; after_suite.json total=1068 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +74/-1 test=src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/errors/index.ts` (+1/-1 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts` (+73/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8894c7486f82f6eb682fecb879791f53312537b1` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p2_shared/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1467_p2_shared/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/errors/index.ts b/Blockchain/Dev/packages/shared/src/errors/index.ts
--- a/Blockchain/Dev/packages/shared/src/errors/index.ts
+++ b/Blockchain/Dev/packages/shared/src/errors/index.ts
@@ -44,4 +44,4 @@
-    Object.setPrototypeOf(this, AppError.prototype);
+    Object.setPrototypeOf(this, new.target.prototype);
     Error.captureStackTrace(this, this.constructor);
   }
 }
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1467-shared-app-error-subclasses-keep-their-own-prototype.test.ts
@@ -0,0 +1,73 @@
+// KS-1467 (packages/shared src/errors/index.ts, mounted by twelve services): AppError's constructor ended with `Object.setPrototypeOf(this, AppError.prototype)`, which resets EVERY subclass
+// instance to the base prototype, so `err instanceof <subclass>` was always false. The constructor now uses `new.target.prototype`. P1/P2/P3 pin the prototypes (three levels deep for
+// DocumentNotFoundError); C1/C2 pin what must not change: the status, the code, the details, and the handler's answer.
+import { describe, it, expect } from 'vitest';
+import type { Response } from 'express';
+import {
+  errorHandler,
+  AppError,
+  BadRequestError,
+  UnauthorizedError,
+  ForbiddenError,
+  NotFoundError,
+  ConflictError,
+  ValidationError,
+  RateLimitError,
+  InternalError,
+  ServiceUnavailableError,
+  DocumentNotFoundError,
+} from '../errors';
+
+const FACTORIES = [
+  { name: 'BadRequestError', make: () => new BadRequestError('x'), cls: BadRequestError, status: 400 },
+  { name: 'UnauthorizedError', make: () => new UnauthorizedError('x'), cls: UnauthorizedError, status: 401 },
+  { name: 'ForbiddenError', make: () => new ForbiddenError('x'), cls: ForbiddenError, status: 403 },
+  { name: 'NotFoundError', make: () => new NotFoundError('Thing'), cls: NotFoundError, status: 404 },
+  { name: 'ConflictError', make: () => new ConflictError('x'), cls: ConflictError, status: 409 },
+  { name: 'ValidationError', make: () => new ValidationError('x', { a: 1 }), cls: ValidationError, status: 422 },
+  { name: 'RateLimitError', make: () => new RateLimitError(5), cls: RateLimitError, status: 429 },
+  { name: 'InternalError', make: () => new InternalError('x'), cls: InternalError, status: 500 },
+  { name: 'ServiceUnavailableError', make: () => new ServiceUnavailableError('Billing'), cls: ServiceUnavailableError, status: 503 },
+] as const;
+
+function run(err: Error): { statusCode: number; body: { error: { code: string; message: string; details?: unknown } } } {
+  const captured = { statusCode: 0, body: undefined } as unknown as { statusCode: number; body: { error: { code: string; message: string; details?: unknown } } };
+  const res = {
+    status(code: number) {
+      captured.statusCode = code;
+      return this;
+    },
+    json(payload: unknown) {
+      captured.body = payload as typeof captured.body;
+      return this;
+    },
+  } as unknown as Response;
+  errorHandler(err, undefined, res, undefined);
+  return captured;
+}
+
+describe('KS-1467: shared AppError subclasses keep their own prototype', () => {
+  it.each(FACTORIES)('RED KS-1467 P1 $name: an instance is an instance of its own class', ({ make, cls }) => {
+    expect(make() instanceof cls).toBe(true);
+  });
+
+  it.each(FACTORIES)('RED KS-1467 P2 $name: the prototype of an instance is the class prototype', ({ make, cls }) => {
+    expect(Object.getPrototypeOf(make())).toBe(cls.prototype);
+  });
+
+  it('RED KS-1467 P3 a two-level subclass is an instance of every class in its chain', () => {
+    const e = new DocumentNotFoundError('d-1');
+    expect([e instanceof DocumentNotFoundError, e instanceof NotFoundError, e instanceof AppError]).toEqual([true, true, true]);
+  });
+
+  it.each(FACTORIES)('control KS-1467 C1 $name: an instance is still an AppError and an Error with its status', ({ make, status }) => {
+    const e = make();
+    expect([e instanceof AppError, e instanceof Error, e.statusCode]).toEqual([true, true, status]);
+  });
+
+  it('control KS-1467 C2 the handler still answers a ValidationError with its details and a 422', () => {
+    const r = run(new ValidationError('bad', { field: 'name' }));
+    expect(r.statusCode).toBe(422);
+    expect(r.body.error).toEqual({ code: 'VALIDATION_ERROR', message: 'bad', details: { field: 'name' } });
+  });
+});
```
