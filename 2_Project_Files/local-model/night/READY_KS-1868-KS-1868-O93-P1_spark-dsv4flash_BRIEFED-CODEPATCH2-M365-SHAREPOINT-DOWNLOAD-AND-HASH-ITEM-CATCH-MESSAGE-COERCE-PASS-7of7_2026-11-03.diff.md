# READY — KS-1868-KS-1868-O93-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p1_m365_sharepoint_download_and_hash_item_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 09:28 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p1_m365_sharepoint_download_and_hash_item_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p1_m365_sharepoint_download_and_hash_item_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p1_m365_sharepoint_download_and_hash_item_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p1_m365_sharepoint_download_and_hash_item_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:28 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p1_m365_sharepoint_download_and_hash_item_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `f7b4a7173010a407864ecb7ab92814824f9cb4b6`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/m365-integration/src/sharepoint/client.ts } + { Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-sharepoint-download-and-hash-item-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/m365-integration/src/sharepoint/client.ts` (product) and `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-sharepoint-download-and-hash-item-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
15	1	Blockchain/Dev/services/m365-integration/src/sharepoint/client.ts
126	0	Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-sharepoint-download-and-hash-item-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (15 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: client.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/m365-integration/src/sharepoint/client.ts`; test(s): `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-sharepoint-download-and-hash-item-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/m365-integration/src/sharepoint/client.ts 15 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-sharepoint-download-and-hash-item-catch-unreadable-throw.test.ts 126 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/m365-integration/src/sharepoint/client.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-sharepoint-download-and-hash-item-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=4 of total=6; red cell(s): ['KS-1868 the sharepoint downloadAndHashItem catch resolves null and logs text for a hostile thrown value RED ks1868 R1: a revoked Proxy from the fetch is logged as text and the call resolves null, as for an ordinary Error', 'KS-1868 the sharepoint downloadAndHashItem catch resolves null and logs text for a hostile thrown value RED ks1868 R2: an Error whose message is a Symbol from the fetch is logged as text and the call resolves null, as for an ordinary Error', 'KS-1868 the sharepoint downloadAndHashItem catch resolves null and logs text for a hostile thrown value RED ks1868 R3: an Error whose message getter throws from the fetch is logged as text and the call resolves null, as for an ordinary Error', 'KS-1868 the sharepoint downloadAndHashItem catch resolves null and logs text for a hostile thrown value RED ks1868 R4: an Error whose cause is a revoked Proxy is logged as text and the call resolves null, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=289 failed=0 | after: total=295 failed=0` · `NEW reds: []` [baseline_suite.json total=289 failed=0; after_suite.json total=295 failed=0]
- A6 [verbatim]: `PASS A6 whole services/m365-integration suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/m365-integration: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/m365-integration/src/sharepoint/client.ts` (+15/-1 per numstat.out) and the test file `Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-sharepoint-download-and-hash-item-catch-unreadable-throw.test.ts` (+126/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/m365-integration/src/sharepoint/client.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `f7b4a7173010a407864ecb7ab92814824f9cb4b6` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p1_m365_sharepoint_download_and_hash_item_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o93_p1_m365_sharepoint_download_and_hash_item_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o93_p1_m365_sharepoint_download_and_hash_item_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/m365-integration/src/sharepoint/client.ts b/Blockchain/Dev/services/m365-integration/src/sharepoint/client.ts
--- a/Blockchain/Dev/services/m365-integration/src/sharepoint/client.ts
+++ b/Blockchain/Dev/services/m365-integration/src/sharepoint/client.ts
@@ -234,7 +234,21 @@
       lastModified: item.lastModifiedDateTime,
     };
   } catch (err: any) {
-    logger.warn('[Graph] downloadAndHashItem failed', { error: err?.message, cause: err?.cause?.message, code: err?.cause?.code, itemId });
+    let reason: string | null | undefined;
+    let cause: string | null | undefined;
+    let code: unknown;
+    try {
+      const m = err?.message;
+      const cm = err?.cause?.message;
+      reason = m === undefined || m === null ? m : String(m);
+      cause = cm === undefined || cm === null ? cm : String(cm);
+      code = err?.cause?.code;
+    } catch {
+      reason = 'unreadable thrown value';
+      cause = undefined;
+      code = undefined;
+    }
+    logger.warn('[Graph] downloadAndHashItem failed', { error: reason, cause, code, itemId });
     return null;
   }
 }
diff --git a/Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-sharepoint-download-and-hash-item-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-sharepoint-download-and-hash-item-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/m365-integration/src/__tests__/ks1868-m365-sharepoint-download-and-hash-item-catch-unreadable-throw.test.ts
@@ -0,0 +1,126 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+
+// KS-1868 (operator 93 screen, m365-integration sharepoint client): the catch of downloadAndHashItem (line 237) of
+// services/m365-integration/src/sharepoint/client.ts passes `err?.message`, `err?.cause?.message` and `err?.cause?.code` straight into the warn line's
+// meta object, unguarded. `?.` guards null and undefined only: a thrown value whose read throws (a revoked Proxy, an Error whose message getter throws)
+// makes the catch throw, so downloadAndHashItem REJECTS where an ordinary Error is logged and it resolves null (the sync route then answers 502 instead
+// of passing the TypeError of the failed read to the error handler); an Error whose message is readable but not a string (a Symbol) is handed to
+// JSON.stringify uncoerced and silently dropped from the line. The cells make the metadata fetch reject with such a value and assert downloadAndHashItem
+// resolves null and the line carries text (the constant when the value cannot be turned into text). Harness: the real module with the service logger replaced
+// by a plain recording object and the global fetch replaced by a plain function that rejects with the cell's value (no network, no Graph).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  warned: [] as unknown[][],
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    info: () => undefined,
+    debug: () => undefined,
+    error: () => undefined,
+    warn: (...args: unknown[]) => {
+      h.warned.push(args);
+    },
+  },
+}));
+
+type Client = typeof import('../sharepoint/client');
+let client: Client;
+const realFetch = globalThis.fetch;
+const realEnv = {
+  id: process.env.ENTRA_CLIENT_ID,
+  secret: process.env.ENTRA_CLIENT_SECRET,
+  tenant: process.env.ENTRA_TENANT_ID,
+};
+
+beforeAll(async () => {
+  process.env.ENTRA_CLIENT_ID = 'client-id';
+  process.env.ENTRA_CLIENT_SECRET = 'client-secret';
+  process.env.ENTRA_TENANT_ID = 'tenant-id';
+  client = await import('../sharepoint/client');
+  client.initGraphClient();
+});
+afterAll(() => {
+  globalThis.fetch = realFetch;
+  for (const [k, v] of [
+    ['ENTRA_CLIENT_ID', realEnv.id],
+    ['ENTRA_CLIENT_SECRET', realEnv.secret],
+    ['ENTRA_TENANT_ID', realEnv.tenant],
+  ] as const) {
+    if (v === undefined) delete process.env[k];
+    else process.env[k] = v;
+  }
+});
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.warned.length = 0;
+  globalThis.fetch = (() => Promise.reject(h.toThrow)) as unknown as typeof fetch;
+});
+
+const FAILED = '[Graph] downloadAndHashItem failed';
+const LINE = (): Record<string, unknown>[] =>
+  h.warned.filter((a) => a[0] === FAILED).map((a) => a[1] as Record<string, unknown>);
+/** A logged field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const fieldOf = (o: Record<string, unknown> | undefined, k: string): string => (typeof o?.[k] === 'string' ? (o[k] as string) : '<' + typeof o?.[k] + '>');
+
+async function download(value: unknown): Promise<{ threw: boolean; result: unknown }> {
+  h.toThrow = value;
+  try {
+    return { threw: false, result: await client.downloadAndHashItem('token', 'site-1', 'drive-1', 'item-1') };
+  } catch {
+    return { threw: true, result: undefined };
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
+describe('KS-1868 the sharepoint downloadAndHashItem catch resolves null and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error with a cause is logged with its message, cause message and cause code and the call resolves null', async () => {
+    const err = new Error('graph boom', { cause: { message: 'inner boom', code: 'ECONNRESET' } });
+    expect(await download(err)).toEqual({ threw: false, result: null });
+    expect(LINE()).toHaveLength(1);
+    expect(fieldOf(LINE()[0], 'error')).toBe('graph boom');
+    expect(fieldOf(LINE()[0], 'cause')).toBe('inner boom');
+    expect(fieldOf(LINE()[0], 'code')).toBe('ECONNRESET');
+    expect(LINE()[0].itemId).toBe('item-1');
+  });
+  it('control ks1868 C2: a thrown plain string is logged without a message and the call resolves null', async () => {
+    expect(await download('plain boom')).toEqual({ threw: false, result: null });
+    expect(LINE()).toHaveLength(1);
+    expect(fieldOf(LINE()[0], 'error')).toBe('<undefined>');
+  });
+  it('RED ks1868 R1: a revoked Proxy from the fetch is logged as text and the call resolves null, as for an ordinary Error', async () => {
+    expect(await download(revokedProxy())).toEqual({ threw: false, result: null });
+    expect(LINE()).toHaveLength(1);
+    expect(fieldOf(LINE()[0], 'error')).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an Error whose message is a Symbol from the fetch is logged as text and the call resolves null, as for an ordinary Error', async () => {
+    expect(await download(withMessage(Symbol('ks1868')))).toEqual({ threw: false, result: null });
+    expect(LINE()).toHaveLength(1);
+    expect(fieldOf(LINE()[0], 'error')).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R3: an Error whose message getter throws from the fetch is logged as text and the call resolves null, as for an ordinary Error', async () => {
+    expect(await download(getterThrows())).toEqual({ threw: false, result: null });
+    expect(LINE()).toHaveLength(1);
+    expect(fieldOf(LINE()[0], 'error')).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R4: an Error whose cause is a revoked Proxy is logged as text and the call resolves null, as for an ordinary Error', async () => {
+    expect(await download(new Error('outer boom', { cause: revokedProxy() }))).toEqual({ threw: false, result: null });
+    expect(LINE()).toHaveLength(1);
+    expect(fieldOf(LINE()[0], 'error')).toBe('unreadable thrown value');
+  });
+});
```
