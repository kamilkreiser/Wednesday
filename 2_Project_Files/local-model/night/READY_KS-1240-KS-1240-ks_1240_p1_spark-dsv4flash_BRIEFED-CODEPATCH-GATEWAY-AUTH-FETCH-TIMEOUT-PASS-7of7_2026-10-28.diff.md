# READY — KS-1240-KS-1240-ks_1240_p1 (spark-dsv4flash, briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p1/out.md.checker/patch.diff`** (from `ls` at 14:15 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p1-control/out.md.checker/patch.diff` rc 0, Spark operator for Wednesday).

**Held 14:15 2026-10-28 by Spark operator for Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `65bc28234507ffcf242381f8020d80b3efe83e85`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/middleware/auth.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	0	Blockchain/Dev/services/api-gateway/src/middleware/auth.ts
97	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (5 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 6 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/middleware/auth.ts byte-exact incl. leading whitespace (apply mode strict): OK 5 line(s) byte-exact incl. leading whitespace (of 5; 6 line(s) added by the apply)` [a3i_indent.out: `OK 5 line(s) byte-exact incl. leading whitespace (of 5; 6 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts fails at the untouched tip (4 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=4 of total=7; red cell(s): ['KS-1240: the gateway key-exchange and key-validate fetches are bounded RED KS-1240 T1 the connector-token exchange fetch is given a timeout signal', 'KS-1240: the gateway key-exchange and key-validate fetches are bounded RED KS-1240 T2 the key-validate fetch is given a timeout signal', 'KS-1240: the gateway key-exchange and key-validate fetches are bounded RED KS-1240 T3 an exchange that never answers settles with null once the signal fires', 'KS-1240: the gateway key-exchange and key-validate fetches are bounded RED KS-1240 T4 a validate that never answers settles with null once the signal fires and caches nothing']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts passes with the product hunk (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1255 failed=0 | after: total=1262 failed=0` · `NEW reds: []` [baseline_suite.json total=1255 failed=0; after_suite.json total=1262 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +103/-0 test=src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` (+6/-0 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts` (+97/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `65bc28234507ffcf242381f8020d80b3efe83e85` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p1/input.json`. Brief (given by --brief; its `# ` heading names KS-1240): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1240_p1/KS-1240.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1240_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts b/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts
--- a/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts
+++ b/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts
@@ -187,3 +187,7 @@
+// KS-1240: the longest the gateway waits for auth's connector-token exchange or security's key-validate answer. Neither fetch carried a timeout, so an upstream that never answered held the
+// caller's request for as long as the socket lived. On expiry the fetch rejects and the existing catch in each function answers exactly as it already did for an unreachable upstream (null).
+const UPSTREAM_AUTH_FETCH_TIMEOUT_MS = 5_000;
+
 /**
  * Exchange a validated sk_ key for a short-lived connector JWT via auth.
  * Returns null (and logs) on failure — downstream Bearer-only services will
@@ -198,6 +202,7 @@
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ apiKey: key }),
+      signal: AbortSignal.timeout(UPSTREAM_AUTH_FETCH_TIMEOUT_MS),
     });
     if (!resp.ok) {
       console.error(`[gateway] connector-token exchange failed (${resp.status}) — downstream Bearer-only services will 401 this connector request`);
@@ -228,6 +233,7 @@
       method: 'POST',
       headers: { 'Content-Type': 'application/json' },
       body: JSON.stringify({ key }),
+      signal: AbortSignal.timeout(UPSTREAM_AUTH_FETCH_TIMEOUT_MS),
     });
     if (!resp.ok) {
       apiKeyCache.set(key, { result: null, expiresAt: Date.now() + 30_000 });
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240-gateway-key-exchange-and-validate-fetches-are-bounded.test.ts
@@ -0,0 +1,97 @@
+// KS-1240 (api-gateway middleware/auth.ts getConnectorBearer and validateApiKey): both fetches carried no timeout, so an upstream (auth's connector-token exchange, security's key-validate) that never
+// answered held the caller's request open with no bound. T1/T2 pin that each fetch is given an abort signal built from AbortSignal.timeout with a bounded value; T3/T4 drive an upstream that never
+// answers and fire that signal: the call must settle with null (the existing unreachable-upstream answer) instead of hanging. A call still pending after 300 ms is reported as the string HUNG, so a
+// hang is a red assertion, not a stuck run. C1 to C3 keep the answers for a healthy upstream exactly as they were.
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+import { getConnectorBearer, validateApiKey, apiKeyCache, connectorBearerCache } from '../middleware/auth';
+
+const fetchMock = vi.fn();
+vi.stubGlobal('fetch', fetchMock);
+
+let timeoutSpy: ReturnType<typeof vi.spyOn>;
+let controller: AbortController;
+
+beforeEach(() => {
+  fetchMock.mockReset();
+  apiKeyCache.clear();
+  connectorBearerCache.clear();
+  controller = new AbortController();
+  timeoutSpy = vi.spyOn(AbortSignal, 'timeout').mockImplementation(() => controller.signal);
+});
+
+afterEach(() => {
+  timeoutSpy.mockRestore();
+});
+
+function neverAnswering(): void {
+  fetchMock.mockImplementation(
+    (_url: string, init?: { signal?: AbortSignal }) =>
+      new Promise((_resolve, reject) => {
+        init?.signal?.addEventListener('abort', () => reject(new Error('aborted by signal')));
+      }),
+  );
+}
+
+async function settled<T>(pending: Promise<T>): Promise<T | 'HUNG'> {
+  return Promise.race([pending, new Promise<'HUNG'>((resolve) => setTimeout(() => resolve('HUNG'), 300))]);
+}
+
+describe('KS-1240: the gateway key-exchange and key-validate fetches are bounded', () => {
+  it('RED KS-1240 T1 the connector-token exchange fetch is given a timeout signal', async () => {
+    fetchMock.mockResolvedValue({ ok: true, json: async () => ({ data: { token: 't1', expiresIn: 600 } }) });
+    await getConnectorBearer('sk_ks1240_t1');
+    const init = fetchMock.mock.calls[0][1] as { signal?: unknown };
+    expect(init.signal).toBeInstanceOf(AbortSignal);
+    expect(timeoutSpy).toHaveBeenCalledTimes(1);
+    const ms = timeoutSpy.mock.calls[0][0] as number;
+    expect(ms).toBeGreaterThan(0);
+    expect(ms).toBeLessThanOrEqual(30000);
+  });
+
+  it('RED KS-1240 T2 the key-validate fetch is given a timeout signal', async () => {
+    fetchMock.mockResolvedValue({ ok: true, json: async () => ({ data: { valid: false } }) });
+    await validateApiKey('sk_ks1240_t2');
+    const init = fetchMock.mock.calls[0][1] as { signal?: unknown };
+    expect(init.signal).toBeInstanceOf(AbortSignal);
+    expect(timeoutSpy).toHaveBeenCalledTimes(1);
+    const ms = timeoutSpy.mock.calls[0][0] as number;
+    expect(ms).toBeGreaterThan(0);
+    expect(ms).toBeLessThanOrEqual(30000);
+  });
+
+  it('RED KS-1240 T3 an exchange that never answers settles with null once the signal fires', async () => {
+    neverAnswering();
+    const pending = getConnectorBearer('sk_ks1240_t3');
+    controller.abort();
+    expect(await settled(pending)).toBeNull();
+  });
+
+  it('RED KS-1240 T4 a validate that never answers settles with null once the signal fires and caches nothing', async () => {
+    neverAnswering();
+    const pending = validateApiKey('sk_ks1240_t4');
+    controller.abort();
+    expect(await settled(pending)).toBeNull();
+    expect(apiKeyCache.has('sk_ks1240_t4')).toBe(false);
+  });
+
+  it('control KS-1240 C1 a healthy exchange still returns the connector token and caches it', async () => {
+    fetchMock.mockResolvedValue({ ok: true, json: async () => ({ data: { token: 'jwt-c1', expiresIn: 600 } }) });
+    expect(await getConnectorBearer('sk_ks1240_c1')).toBe('jwt-c1');
+    expect(connectorBearerCache.get('sk_ks1240_c1')?.token).toBe('jwt-c1');
+  });
+
+  it('control KS-1240 C2 a healthy validate still returns the key metadata', async () => {
+    fetchMock.mockResolvedValue({
+      ok: true,
+      json: async () => ({ data: { valid: true, connectorId: 'platform-s:c2', scopes: ['documents:write'], organizationId: 'org-c2', tenantId: 'ten-c2' } }),
+    });
+    const meta = await validateApiKey('sk_ks1240_c2');
+    expect(meta?.connectorId).toBe('platform-s:c2');
+    expect(meta?.tenantId).toBe('ten-c2');
+  });
+
+  it('control KS-1240 C3 a refused exchange (HTTP 502) still returns null', async () => {
+    fetchMock.mockResolvedValue({ ok: false, status: 502, json: async () => ({}) });
+    expect(await getConnectorBearer('sk_ks1240_c3')).toBeNull();
+  });
+});
```

## DECISION NOTE (source-read, Spark operator for Wednesday, 2026-10-28 PM) - HOLD-WITH-DECISION
- Source-read: one module constant `UPSTREAM_AUTH_FETCH_TIMEOUT_MS = 5_000` and `signal: AbortSignal.timeout(...)` in the two fetches of `middleware/auth.ts` (getConnectorBearer, validateApiKey). On timeout each fetch rejects into the EXISTING `catch { return null }`, which does not cache, so a hung security service answers 401 for that request exactly as an unreachable one already does.
- DECISIONS for the owner: (1) the 5000 ms value is the drafter's; (2) the ticket suggests a 503 on timeout and this patch does NOT build it (a valid key reads as invalid for the request that timed out, which is the present unreachable-upstream behaviour); (3) AbortSignal.timeout also bounds reading the body of a slow answer.
- SEQUENCE: KS-1240 has THREE READYs (`ks_1240_p1` auth.ts; `ks_1240_p2_proxy_admin` proxy.ts + admin.ts; `ks_1240_p3_batch_audit` batch.ts + audit-export.ts). They share NO file with each other, so no order is forced; they can be one PR or three. Each adds its own constant, and the three new test files have different names. Refs KS-1240 on each; close-word only after the last merges and the owner accepts the 401-vs-503 question.
- Verdict: HOLD-WITH-DECISION.
