# READY — KS-1868-KS-1868-O85-P6 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p6_originate_lifecycle_payload_codec_decrypt_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 23:59 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p6_originate_lifecycle_payload_codec_decrypt_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p6_originate_lifecycle_payload_codec_decrypt_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p6_originate_lifecycle_payload_codec_decrypt_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p6_originate_lifecycle_payload_codec_decrypt_catch_guard_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 23:59 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p6_originate_lifecycle_payload_codec_decrypt_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `1584c0f0ff808fddf35245bee41b6b5f9231054c`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/utils/lifecyclePayloadCodec.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-payload-codec-decrypt-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/utils/lifecyclePayloadCodec.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-payload-codec-decrypt-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/originate/src/utils/lifecyclePayloadCodec.ts
129	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-payload-codec-decrypt-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: lifecyclePayloadCodec.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/utils/lifecyclePayloadCodec.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-payload-codec-decrypt-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/utils/lifecyclePayloadCodec.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-payload-codec-decrypt-catch-unreadable-throw.test.ts 129 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/utils/lifecyclePayloadCodec.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-payload-codec-decrypt-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=4 of total=8; red cell(s): ['KS-1868 the lifecycle payload decrypt catch returns its marker and logs text for a hostile thrown value RED ks1868 R1: a decrypt failure that is a revoked Proxy returns the payloadUnavailable marker and is logged as text, as for an ordinary Error', 'KS-1868 the lifecycle payload decrypt catch returns its marker and logs text for a hostile thrown value RED ks1868 R2: a decrypt failure that is an Error whose message getter throws returns the payloadUnavailable marker and is logged as text, as for an ordinary Error', 'KS-1868 the lifecycle payload decrypt catch returns its marker and logs text for a hostile thrown value RED ks1868 R3: a decrypt failure that is an Error whose message is a null-prototype object returns the payloadUnavailable marker and is logged as text, as for an ordinary Error', 'KS-1868 the lifecycle payload decrypt catch returns its marker and logs text for a hostile thrown value RED ks1868 R4: a decrypt failure that is an Error whose message is a Symbol returns the payloadUnavailable marker and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2283 failed=0 | after: total=2291 failed=0` · `NEW reds: []` [baseline_suite.json total=2283 failed=0; after_suite.json total=2291 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/utils/lifecyclePayloadCodec.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-payload-codec-decrypt-catch-unreadable-throw.test.ts` (+129/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/utils/lifecyclePayloadCodec.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `1584c0f0ff808fddf35245bee41b6b5f9231054c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p6_originate_lifecycle_payload_codec_decrypt_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o85_p6_originate_lifecycle_payload_codec_decrypt_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o85_p6_originate_lifecycle_payload_codec_decrypt_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/utils/lifecyclePayloadCodec.ts b/Blockchain/Dev/services/originate/src/utils/lifecyclePayloadCodec.ts
--- a/Blockchain/Dev/services/originate/src/utils/lifecyclePayloadCodec.ts
+++ b/Blockchain/Dev/services/originate/src/utils/lifecyclePayloadCodec.ts
@@ -53,9 +53,15 @@
         const plain = decryptField(raw, context(eventId));
         return plain ? (JSON.parse(plain) as Record<string, unknown>) : {};
       } catch (err) {
+        let reason: string;
+        try {
+          reason = String(err instanceof Error ? err.message : err);
+        } catch {
+          reason = 'unreadable thrown value';
+        }
         logger.error('lifecycle payload decrypt failed', {
           eventId,
-          error: err instanceof Error ? err.message : String(err),
+          error: reason,
         });
         return { payloadUnavailable: true };
       }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-payload-codec-decrypt-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-payload-codec-decrypt-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-lifecycle-payload-codec-decrypt-catch-unreadable-throw.test.ts
@@ -0,0 +1,129 @@
+// KS-1868 (operator 85 screen, lifecycle payload codec): the decrypt-failed catch of decodeLifecyclePayload in
+// services/originate/src/utils/lifecyclePayloadCodec.ts logs `{ eventId, error: err instanceof Error ? err.message : String(err) }`
+// with the read INSIDE the logger call's arguments, unguarded. A thrown value whose read throws (a revoked Proxy: `instanceof`
+// throws; an Error whose message getter throws) makes the catch itself throw, so the function THROWS instead of returning its
+// `payloadUnavailable` marker (one unreadable row would fail a whole listing); an Error whose message is readable but not a
+// string is handed to the logger as is. The cells make decryptField throw such a value and assert the marker is returned and the
+// line is logged as text (the constant when the value cannot be turned into text). Harness: the real codec with the logger
+// replaced by a plain stand-in and @secuura/shared built through the service's makeSharedMock helper (KS-1061) with decryptField / isEncryptedPii overridden by plain functions (no keyring).
+import { decodeLifecyclePayload } from '../utils/lifecyclePayloadCodec';
+
+const mockH: { toThrow: unknown; logged: unknown[][] } = { toThrow: undefined, logged: [] };
+
+jest.mock('@secuura/shared', () => require('./helpers/sharedModuleMock').makeSharedMock({
+  isEncryptedPii: () => true,
+  decryptField: () => {
+    throw mockH.toThrow;
+  },
+}));
+jest.mock('../utils/logger', () => ({
+  logger: {
+    info: () => undefined,
+    warn: () => undefined,
+    debug: () => undefined,
+    error: (...args: unknown[]) => {
+      mockH.logged.push(args);
+    },
+  },
+}));
+
+const EVENT_ID = '9f0d76a2-0000-4000-8000-000000000001';
+const FAILED = 'lifecycle payload decrypt failed';
+
+beforeEach(() => {
+  mockH.toThrow = undefined;
+  mockH.logged.length = 0;
+});
+
+function decode(): { ok: boolean; value: Record<string, unknown> | undefined } {
+  try {
+    return { ok: true, value: decodeLifecyclePayload('v1:iv:tag:ciphertext', EVENT_ID) };
+  } catch {
+    return { ok: false, value: undefined };
+  }
+}
+const LINES = () => mockH.logged.filter((c) => c[0] === FAILED);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (c: unknown[] | undefined): string => {
+  const v = (c?.[1] as { error?: unknown } | undefined)?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+const eventOf = (c: unknown[] | undefined): unknown => (c?.[1] as { eventId?: unknown } | undefined)?.eventId;
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
+const SHAPES: Array<[string, () => unknown, string]> = [
+  ['a revoked Proxy', revokedProxy, 'unreadable thrown value'],
+  ['an Error whose message getter throws', getterThrows, 'unreadable thrown value'],
+  ['an Error whose message is a null-prototype object', () => withMessage(Object.create(null)), 'unreadable thrown value'],
+  ['an Error whose message is a Symbol', () => withMessage(Symbol('ks1868')), 'Symbol(ks1868)'],
+];
+
+describe('KS-1868 the lifecycle payload decrypt catch returns its marker and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error returns the payloadUnavailable marker and is logged with its message', () => {
+    mockH.toThrow = new Error('bad auth tag');
+    expect(decode()).toEqual({ ok: true, value: { payloadUnavailable: true } });
+    expect(LINES()).toHaveLength(1);
+    expect(eventOf(LINES()[0])).toBe(EVENT_ID);
+    expect(reasonOf(LINES()[0])).toBe('bad auth tag');
+  });
+  it('control ks1868 C2: a thrown plain string returns the marker and is logged as its own text', () => {
+    mockH.toThrow = 'plain boom';
+    expect(decode()).toEqual({ ok: true, value: { payloadUnavailable: true } });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('plain boom');
+  });
+  it('control ks1868 C3: a thrown number returns the marker and is logged as its text', () => {
+    mockH.toThrow = 42;
+    expect(decode()).toEqual({ ok: true, value: { payloadUnavailable: true } });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('42');
+  });
+  it('control ks1868 C4: an Error with an empty message returns the marker and is logged with the empty text', () => {
+    mockH.toThrow = new Error('');
+    expect(decode()).toEqual({ ok: true, value: { payloadUnavailable: true } });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('');
+  });
+  it('RED ks1868 R1: a decrypt failure that is a revoked Proxy returns the payloadUnavailable marker and is logged as text, as for an ordinary Error', () => {
+    mockH.toThrow = SHAPES[0][1]();
+    expect(decode()).toEqual({ ok: true, value: { payloadUnavailable: true } });
+    expect(LINES()).toHaveLength(1);
+    expect(eventOf(LINES()[0])).toBe(EVENT_ID);
+    expect(reasonOf(LINES()[0])).toBe(SHAPES[0][2]);
+  });
+  it('RED ks1868 R2: a decrypt failure that is an Error whose message getter throws returns the payloadUnavailable marker and is logged as text, as for an ordinary Error', () => {
+    mockH.toThrow = SHAPES[1][1]();
+    expect(decode()).toEqual({ ok: true, value: { payloadUnavailable: true } });
+    expect(LINES()).toHaveLength(1);
+    expect(eventOf(LINES()[0])).toBe(EVENT_ID);
+    expect(reasonOf(LINES()[0])).toBe(SHAPES[1][2]);
+  });
+  it('RED ks1868 R3: a decrypt failure that is an Error whose message is a null-prototype object returns the payloadUnavailable marker and is logged as text, as for an ordinary Error', () => {
+    mockH.toThrow = SHAPES[2][1]();
+    expect(decode()).toEqual({ ok: true, value: { payloadUnavailable: true } });
+    expect(LINES()).toHaveLength(1);
+    expect(eventOf(LINES()[0])).toBe(EVENT_ID);
+    expect(reasonOf(LINES()[0])).toBe(SHAPES[2][2]);
+  });
+  it('RED ks1868 R4: a decrypt failure that is an Error whose message is a Symbol returns the payloadUnavailable marker and is logged as text, as for an ordinary Error', () => {
+    mockH.toThrow = SHAPES[3][1]();
+    expect(decode()).toEqual({ ok: true, value: { payloadUnavailable: true } });
+    expect(LINES()).toHaveLength(1);
+    expect(eventOf(LINES()[0])).toBe(EVENT_ID);
+    expect(reasonOf(LINES()[0])).toBe(SHAPES[3][2]);
+  });
+});
```
