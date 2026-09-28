# READY — KS-888-REVOKE (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 on RE-CHECK — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-888-REVOKE/out.md.checker/patch.diff`**. **BYTE-IDENTICAL to the brief-writer's golden** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-888-revoke/KS-888.golden.diff` (`cmp` rc 0).

**Held BY HAND at 18:24 2026-09-28 by Wednesday morning 4901153c.** hold_ready.py refused ("product hunk '+' lines (19) are not ordered-equal to the brief's expected_plus (43)"), the same product-only assumption the checker had. This brief edits an EXISTING test file in place, so 24 of the 43 expected lines are test-file lines. OWED: fix hold_ready the same way as the checker.

- **First checker pass FAILED at A3c** (`checker.firstpass.out`: "22 of 43 line(s) … ABSENT from the product hunk"). **Class: HARNESS**, not model: A3c measured the product section only. Fixed in `tasks/code_patch/checker.sh` (backup `.pre-0928-a3cinplacetest`): in code_patch mode, when the diff carries the test file's section, A3c measures product + test together. Proved: this output re-checks PASS 7/7 (`checker.out`); a one-line-dropped mutation FAILs A3c (1 of 43 absent); KS-747-R2 (new test file) still PASSes 7/7.
- RED-FIRST / GREEN-AFTER [checker.out, verbatim]:
  - `PASS A4 RED-FIRST: src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts fails at the untouched tip (4 failed / 14 run; controls green; assertion reds)`
  - `PASS A5 GREEN-AFTER: src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts passes with the product hunk (14 passed / 14 run)`
  - `PASS A6 whole services/security suite: no NEW red vs the untouched tip`
  - `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
- Contract (the card default, 18:00): revoke → 503 (infra) / 500 (other) when the save fails, and the in-memory revoke is KEPT (in-process only; other replicas and a restart still see the key active; nothing retries). Mint unchanged. Validate is NOT in this patch (re-carded to Kam).

```diff
--- a/Blockchain/Dev/services/security/src/index.ts
+++ b/Blockchain/Dev/services/security/src/index.ts
@@ -330,8 +330,9 @@
     ));
   } catch (err: any) {
     logger.error('DB save API key failed', { error: err?.message });
-    // KS-888: only the mint opts in. Revoke and validate keep this log-only swallow: their handlers
-    // take no next, so a throw from here would be an unhandled rejection that ends the process.
+    // KS-888: re-throws only for a caller that opts in, and each caller that opts in catches it in its own try.
+    // Any other caller keeps this log-only swallow: a throw into a handler that takes no next is an unhandled
+    // rejection, and that ends the process.
     if (opts.rethrow) throw err;
   }
 }
@@ -1285,4 +1286,18 @@
   apiKey.isActive = false;
-  await dbSaveApiKey(apiKey);
-  
+  // KS-888 (card secuura-ks888-revoke-validate-on-failed-save, option a, the default from 2026-09-28 18:00):
+  // a revoke whose save did not persist is not acknowledged. The in-memory revoke above is KEPT, so the key
+  // stops working in this process, and the caller is told the revoke was not stored: 503 for an infrastructure
+  // fault (the mint classifier: SQLSTATE 08, 53, 57, a lost socket, a pool timeout), 500 for anything else.
+  // The try is required: this handler takes no next, so an uncaught throw would end the process (KS-888 r2).
+  try {
+    await dbSaveApiKey(apiKey, { rethrow: true });
+  } catch (saveErr: any) {
+    const infra = /^(08|53|57)|^(ECONNREFUSED|ECONNRESET|ETIMEDOUT|EHOSTUNREACH|ENETUNREACH|EPIPE)$/.test(String(saveErr?.code)) || /connection terminated|timeout exceeded when trying to connect|connection timeout|pool is draining|client has encountered a connection error/i.test(String(saveErr?.message));
+    log('error', 'KS-888: API key revoke not stored, the key is revoked in this process only', { keyId: apiKey.id, code: saveErr?.code, infra });
+    return res.status(infra ? 503 : 500).json({
+      success: false,
+      error: { code: infra ? 'SERVICE_UNAVAILABLE' : 'INTERNAL_ERROR', message: 'The API key revoke could not be saved, so it may not survive a restart' },
+    });
+  }
+
   log('info', 'API key revoked', { keyId: apiKey.id });
--- a/Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts
+++ b/Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts
@@ -122,8 +122,33 @@
   });
-
+
+  it.each(INFRA)('RED KS-888 R1 %s: a revoke whose save hits an infrastructure fault answers a retryable 503', async (_label, fault) => {
+    const minted = await mint('ks888 revoke infra');
+    state.fault = fault;
+    const res = await fetch(base + '/api/keys/' + minted.body.data.id, { method: 'DELETE', headers: { Authorization: 'Bearer ' + PLATFORM() }, signal: AbortSignal.timeout(3000) });
+    const json = (await res.json()) as { success?: boolean; message?: string; error?: { code?: string } };
+    expect({ minted: minted.status, status: res.status, success: json.success, code: json.error?.code, message: json.message }).toEqual({ minted: 201, status: 503, success: false, code: 'SERVICE_UNAVAILABLE', message: undefined });
+  });
+
+  it('control KS-888 R2: the in-memory revoke is kept when its save fails, so validate answers Key revoked', async () => {
+    const minted = await mint('ks888 revoke kept in memory');
+    state.fault = STRUCTURAL;
+    await fetch(base + '/api/keys/' + minted.body.data.id, { method: 'DELETE', headers: { Authorization: 'Bearer ' + PLATFORM() }, signal: AbortSignal.timeout(3000) });
+    const res = await fetch(base + '/api/keys/validate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ key: minted.body.data.key }), signal: AbortSignal.timeout(3000) });
+    const json = (await res.json()) as { data?: { valid?: boolean; reason?: string } };
+    expect({ minted: minted.status, status: res.status, valid: json.data?.valid, reason: json.data?.reason }).toEqual({ minted: 201, status: 200, valid: false, reason: 'Key revoked' });
+  });
+
+  it('control KS-888 R3: a revoke whose save lands answers 200 API key revoked, and the save was issued', async () => {
+    const minted = await mint('ks888 revoke saved');
+    const before = state.inserts;
+    const res = await fetch(base + '/api/keys/' + minted.body.data.id, { method: 'DELETE', headers: { Authorization: 'Bearer ' + PLATFORM() }, signal: AbortSignal.timeout(3000) });
+    expect({ minted: minted.status, status: res.status, message: ((await res.json()) as { message?: string }).message, inserts: state.inserts - before }).toEqual({ minted: 201, status: 200, message: 'API key revoked', inserts: 1 });
+  });
+
-  it('control KS-888 C2: revoke still answers 200 while the same INSERT fails (the swallow is unchanged there)', async () => {
-    const minted = await mint('ks888 revoke control');
+  it('RED KS-888 R4: a revoke whose save fails structurally (42703) answers 500 INTERNAL_ERROR, not API key revoked', async () => {
+    const minted = await mint('ks888 revoke structural');
     state.fault = STRUCTURAL;
     const res = await fetch(base + '/api/keys/' + minted.body.data.id, { method: 'DELETE', headers: { Authorization: 'Bearer ' + PLATFORM() }, signal: AbortSignal.timeout(3000) });
-    expect({ minted: minted.status, status: res.status, message: ((await res.json()) as { message?: string }).message }).toEqual({ minted: 201, status: 200, message: 'API key revoked' });
+    const json = (await res.json()) as { success?: boolean; message?: string; error?: { code?: string } };
+    expect({ minted: minted.status, status: res.status, success: json.success, code: json.error?.code, message: json.message }).toEqual({ minted: 201, status: 500, success: false, code: 'INTERNAL_ERROR', message: undefined });
   });
```
