# READY — KS-1868-KS-1868-O94-P17 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p17_originate_provenance_resolve_on_behalf_of_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 13:38 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p17_originate_provenance_resolve_on_behalf_of_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p17_originate_provenance_resolve_on_behalf_of_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p17_originate_provenance_resolve_on_behalf_of_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p17_originate_provenance_resolve_on_behalf_of_catch_guard_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:38 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p17_originate_provenance_resolve_on_behalf_of_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `09884b0e63825db223497e1af7c3f6bc445721e2`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/services/provenance.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-provenance-resolve-on-behalf-of-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/provenance.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-provenance-resolve-on-behalf-of-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
12	2	Blockchain/Dev/services/originate/src/services/provenance.ts
86	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-provenance-resolve-on-behalf-of-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (12 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: provenance.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/services/provenance.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-provenance-resolve-on-behalf-of-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/services/provenance.ts 12 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-provenance-resolve-on-behalf-of-catch-unreadable-throw.test.ts 86 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/services/provenance.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-provenance-resolve-on-behalf-of-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 resolveOnBehalfOf reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value stores verbatim provenance (null) and logs a constant reason', 'KS-1868 resolveOnBehalfOf reads the thrown value safely RED ks1868 R2 an Error whose message getter throws stores verbatim provenance (null) and logs a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2390 failed=11 | after: total=2394 failed=11` · `NEW reds: []` [baseline_suite.json total=2390 failed=11; after_suite.json total=2394 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/provenance.ts` (+12/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-provenance-resolve-on-behalf-of-catch-unreadable-throw.test.ts` (+86/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/services/provenance.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `09884b0e63825db223497e1af7c3f6bc445721e2` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p17_originate_provenance_resolve_on_behalf_of_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o94_p17_originate_provenance_resolve_on_behalf_of_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o94_p17_originate_provenance_resolve_on_behalf_of_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/services/provenance.ts b/Blockchain/Dev/services/originate/src/services/provenance.ts
--- a/Blockchain/Dev/services/originate/src/services/provenance.ts
+++ b/Blockchain/Dev/services/originate/src/services/provenance.ts
@@ -154,10 +154,20 @@
     // (and no 403: they are not in a *different* org).
     return subjectOrg !== null && subjectOrg === callerOrg ? user.id : null;
   } catch (err) {
-    if (err instanceof OnBehalfOfError) throw err;
+    let isOnBehalfOfError: boolean;
+    let reason: string | null | undefined;
+    try {
+      isOnBehalfOfError = err instanceof OnBehalfOfError;
+      const m = (err as Error).message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      isOnBehalfOfError = false;
+      reason = 'unreadable thrown value';
+    }
+    if (isOnBehalfOfError) throw err;
     // Lookup infrastructure failure → attribute verbatim rather than fail the
     // write; the provenance row still records who acted.
-    logger.warn('onBehalfOf resolution failed — storing verbatim provenance', { error: (err as Error).message });
+    logger.warn('onBehalfOf resolution failed — storing verbatim provenance', { error: reason });
     return null;
   }
 }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-provenance-resolve-on-behalf-of-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-provenance-resolve-on-behalf-of-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-provenance-resolve-on-behalf-of-catch-unreadable-throw.test.ts
@@ -0,0 +1,86 @@
+// KS-1868: resolveOnBehalfOf (src/services/provenance.ts) resolves a connector's onBehalfOf email to a same-org user id, and in its catch
+// stores verbatim provenance (resolves null) when the lookup fails ("attribute verbatim rather than fail the write"). The catch tests the thrown
+// value with `err instanceof OnBehalfOfError` and reads `(err as Error).message` into the warn line, both unguarded. A revoked Proxy makes `instanceof`
+// throw, and an Error whose `message` getter throws makes the read throw: the catch throws, so resolveOnBehalfOf REJECTS and the whole write fails,
+// where an ordinary Error is logged and null is returned. An OnBehalfOfError is still rethrown.
+// The database and logger stand-ins are plain functions, not jest.fn(): a spy inspects what it rejects with and could itself fail on a revoked Proxy first.
+const mockState: { toThrow: unknown; warned: unknown[][] } = { toThrow: undefined, warned: [] };
+
+jest.mock('../db', () => ({
+  prisma: {
+    $queryRaw: (..._args: unknown[]) => Promise.reject(mockState.toThrow),
+  },
+}));
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    encryptField: async (v: string) => v,
+    decryptField: async (v: string) => v,
+    lookupHash: (v: string) => `hash:${v}`,
+  }),
+);
+
+jest.mock('../utils/logger', () => ({
+  logger: {
+    debug: () => undefined,
+    info: () => undefined,
+    error: () => undefined,
+    warn: (...args: unknown[]) => {
+      mockState.warned.push(args);
+    },
+  },
+}));
+
+import { resolveOnBehalfOf, OnBehalfOfError } from '../services/provenance';
+
+const ORG = '11111111-2222-4333-8444-555555555555';
+
+/** The resolved id, or the string 'rejected' when it rejects (an assertion can then fail on it). */
+async function resolve(value: unknown): Promise<unknown> {
+  mockState.toThrow = value;
+  try {
+    return await resolveOnBehalfOf({ email: 'someone@example.com' }, ORG);
+  } catch {
+    return 'rejected';
+  }
+}
+
+function loggedError(): unknown {
+  const hit = mockState.warned.find((a) => typeof a[0] === 'string' && (a[0] as string).startsWith('onBehalfOf resolution failed'));
+  return (hit?.[1] as { error?: unknown } | undefined)?.error;
+}
+
+describe('KS-1868 resolveOnBehalfOf reads the thrown value safely', () => {
+  beforeEach(() => {
+    mockState.toThrow = undefined;
+    mockState.warned = [];
+  });
+
+  it('control ks1868 C1 an ordinary Error stores verbatim provenance (null) and logs its message', async () => {
+    expect(await resolve(new Error('db down'))).toBeNull();
+    expect(loggedError()).toBe('db down');
+  });
+
+  it('control ks1868 C2 an OnBehalfOfError is still rethrown', async () => {
+    expect(await resolve(new OnBehalfOfError(403, 'FORBIDDEN', 'different organisation'))).toBe('rejected');
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value stores verbatim provenance (null) and logs a constant reason', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    expect(await resolve(proxy)).toBeNull();
+    expect(loggedError()).toBe('unreadable thrown value');
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws stores verbatim provenance (null) and logs a constant reason', async () => {
+    const hostile = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    expect(await resolve(hostile)).toBeNull();
+    expect(loggedError()).toBe('unreadable thrown value');
+  });
+});
```
