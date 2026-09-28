# READY — KS-888-VALIDATE-LOGONLY (spark-dsv4flash, briefed, first round) — PASS 7/7 — HELD for QA

> **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-888-VALIDATE-LOGONLY/out.md.checker/patch.diff`**. **BYTE-IDENTICAL to the brief-writer's golden** `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/KS-888-validate-logonly/KS-888.golden.diff` (`cmp` rc 0; a mutated-golden control DIFFERS, rc 1), measured by Wednesday.

**Held BY HAND at 00:07 2026-09-29 by Wednesday overnight seat 24014037.** hold_ready.py refused: `hold_ready: REFUSE — checker.out has no 'mode: code_patch' line — the input says code_patch but the checker did not run it as one` (the owed product-only / code_patch-mode assumption, the same class as KS-888-REVOKE on 2026-09-28). Source at develop 0d156d12cc0f (base porcelain 0 before and after).

- Contract: Kam ruled card secuura-ks888-validate-usage-write-failure = a (2026-09-28 20:22:15): a failed usage write is logged, never refused. MEASURED by the brief-writer at develop 0d156d12: validate ALREADY behaves so (no opt-in at index.ts:1369), so this is a TEST-ONLY pin, no product change; the tamper (the log line gains k.keyHash) reds only the log cell. The conflicting later tap (20:22:48, refuse 503) has a check-back posted; the old REFUSE brief night/briefs/KS-888-validate/ must never run. UNMEASURED, for the raise seat: validate's upsert also writes is_active from memory (index.ts:316-318), so a stale replica could undo another replica's revoke; measure and file if real.
- Checker verdict [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`
  - `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts } — the product file is untouched, as the ticket requires`
  - `PASS A3c every '+' line the brief adds is in the product hunk (34 line(s)), and no tip line is re-added as a '+' (A3d)`
  - `PASS A4 RED-FIRST: src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts fails at the untouched tip (1 failed / 19 run; controls green; assertion reds)`
  - `PASS A5 GREEN-AFTER: src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts passes with the product hunk (19 passed / 19 run)`
  - `PASS A6 whole services/security suite: no NEW red vs the untouched tip`
  - `PASS A7 tsc --noEmit for services/security: rc 0 after the patch (baseline rc=0)`
  - `SUMMARY files=1 +38/-1 test=src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts red_first=yes apply_mode=strict`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `SPARK RESULT: PASS (checker rc 0 + A2a anchor OK)`

```diff
--- a/Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts
+++ b/Blockchain/Dev/services/security/src/__tests__/ks888-failed-mint-save-issues-no-key.test.ts
@@ -162,3 +162,40 @@
   });
-
+
+  it.each(INFRA)('control KS-888 V1 %s: validate answers 200 valid from the key itself while its usage write fails', async (_label, fault) => {
+    const minted = await mint('ks888 validate usage write infra');
+    state.fault = fault;
+    const before = state.inserts;
+    const res = await fetch(base + '/api/keys/validate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ key: minted.body.data.key }), signal: AbortSignal.timeout(3000) });
+    const json = (await res.json()) as { data?: { valid?: boolean; tenantId?: string; scopes?: string[] } };
+    expect({ minted: minted.status, status: res.status, valid: json.data?.valid, tenantId: json.data?.tenantId, scopes: json.data?.scopes, writes: state.inserts - before }).toEqual({ minted: 201, status: 200, valid: true, tenantId: TENANT, scopes: ['documents:read'], writes: 1 });
+  });
+
+  it('pin KS-888 V2: a failed usage write logs ONE error line, and no log line carries the key or its hash', async () => {
+    const { logger } = await import('../utils/logger');
+    const minted = await mint('ks888 validate usage write log');
+    const key = String(minted.body.data.key);
+    const hash = crypto.createHash('sha256').update(key).digest('hex');
+    const errors = vi.spyOn(logger, 'error');
+    const warns = vi.spyOn(logger, 'warn');
+    const lines = vi.spyOn(console, 'log');
+    try {
+      state.fault = STRUCTURAL;
+      const res = await fetch(base + '/api/keys/validate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ key }), signal: AbortSignal.timeout(3000) });
+      const valid = ((await res.json()) as { data?: { valid?: boolean } }).data?.valid;
+      const logged = JSON.stringify([errors.mock.calls, warns.mock.calls, lines.mock.calls]);
+      expect({ status: res.status, valid, errorLines: errors.mock.calls.length, first: errors.mock.calls[0]?.[0], key: logged.includes(key), hash: logged.includes(hash) }).toEqual({ status: 200, valid: true, errorLines: 1, first: 'DB save API key failed', key: false, hash: false });
+    } finally {
+      errors.mockRestore();
+      warns.mockRestore();
+      lines.mockRestore();
+    }
+  });
+
+  it('control KS-888 V3: a validate whose usage write lands answers 200 valid, and the write was issued', async () => {
+    const minted = await mint('ks888 validate usage write lands');
+    const before = state.inserts;
+    const res = await fetch(base + '/api/keys/validate', { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ key: minted.body.data.key }), signal: AbortSignal.timeout(3000) });
+    expect({ minted: minted.status, status: res.status, valid: ((await res.json()) as { data?: { valid?: boolean } }).data?.valid, writes: state.inserts - before }).toEqual({ minted: 201, status: 200, valid: true, writes: 1 });
+  });
+
   it('control KS-888 C4: with no database at all the memory-only mint still answers 201 with the key', async () => {
```
