# READY — KS-1788-KS-1788 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1788_p1_checkapikey_4xx/out.md.checker/patch.diff`** (from `ls` at 08:58 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1788_p1_checkapikey_4xx/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 08:58 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1788_p1_checkapikey_4xx/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `593cd90c3131f200f4adaf242c1a406a5b66fbb0`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/api-gateway/src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
25	1	Blockchain/Dev/services/api-gateway/src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (23 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 25 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (2 NON-ASCII chars); `-` lines 1.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 23 line(s) byte-exact incl. leading whitespace (of 23; 25 line(s) added by the apply)` [a3i_indent.out: `OK 23 line(s) byte-exact incl. leading whitespace (of 23; 25 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `33b19c8b01ce3d3e` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/api-gateway/src/middleware/auth.ts:205)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-30_ks_1788_p1_checkapikey_4xx_080533/clone/Blockchain/Dev/services/api-gateway/src/middleware/auth.ts:205: '  return status >= 500 || status === 408 || status === 429;' -> '  return status >= 500 || status === 408 || status === 403;'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/api-gateway/src/middleware/auth.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 205. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts` (hunks=5, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts fails at the untouched tip (2 failed / 14 run; controls green; assertion reds)` [red_first.json: failed=2 of total=14; red cell(s): ['KS-1240 controls: a REJECTED key keeps every answer it had 🔴 KS-1788 a plain 4xx from the security service (403) is a REJECTION: 401 Invalid API key, nothing forwarded, a 30 s negative cache entry, and the next request is answered from it', 'KS-1240 controls: a REJECTED key keeps every answer it had 🔴 KS-1788 a 429 from the security service is NOT a rejection: 503 SERVICE_UNAVAILABLE, nothing forwarded, nothing cached']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts passes with the product hunk (14 passed / 14 run)` [green_after.json: failed=0 of total=14, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1313 failed=2 | after: total=1315 failed=0` · `NEW reds: []` [baseline_suite.json total=1313 failed=2; after_suite.json total=1315 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +25/-1 test=src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/api-gateway/src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts` (+25/-1 per numstat.out); the product `Blockchain/Dev/services/api-gateway/src/middleware/auth.ts` is the tamper target and is byte-unchanged (sha256 33b19c8b01ce3d3e, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `593cd90c3131f200f4adaf242c1a406a5b66fbb0` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1788_p1_checkapikey_4xx/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1788_p1_checkapikey_4xx/checker.out`.

```diff
--- a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts
@@ -57,4 +57,4 @@
-type Validate = 'valid' | 'rejected' | 'hang' | 'stall' | 'security503';
+type Validate = 'valid' | 'rejected' | 'hang' | 'stall' | 'security503' | 'status403' | 'status429';
 type Exchange = 'ok' | 'hang' | 'stall';
 const KEYS = {
   VALID: 'sk_ks1240b_valid_key_00001',
@@ -65,6 +65,8 @@
   HANG_OPT: 'sk_ks1240b_validate_hangs_2',
   STALL: 'sk_ks1240b_validate_stall_1',
   SEC503: 'sk_ks1240b_security_503_001',
+  S403: 'sk_ks1788_security_403_0001',
+  S429: 'sk_ks1788_security_429_0001',
   EXCH_HANG: 'sk_ks1240b_exchange_hangs_1',
   EXCH_STALL: 'sk_ks1240b_exchange_stall_1',
 } as const;
@@ -72,6 +74,7 @@
   [KEYS.VALID]: 'valid', [KEYS.VALID_FRESH]: 'valid', [KEYS.REJECTED]: 'rejected', [KEYS.REJECTED_OPT]: 'rejected',
   [KEYS.HANG]: 'hang', [KEYS.HANG_OPT]: 'hang', [KEYS.STALL]: 'stall', [KEYS.SEC503]: 'security503',
   [KEYS.EXCH_HANG]: 'valid', [KEYS.EXCH_STALL]: 'valid',
+  [KEYS.S403]: 'status403', [KEYS.S429]: 'status429',
 };
 const exchangeAs: Record<string, Exchange> = { [KEYS.EXCH_HANG]: 'hang', [KEYS.EXCH_STALL]: 'stall' };
 const validateHits: Record<string, number> = {};
@@ -147,6 +150,9 @@
         case 'rejected': return json(200, { success: true, data: { valid: false, reason: 'Key not found' } });
         // The security service's own answer when it cannot read the key's stored state (security/src/index.ts, KS-1370).
         case 'security503': return json(503, { success: false, error: { code: 'SERVICE_UNAVAILABLE', message: 'Unable to verify key' } });
+        // KS-1788 item 3: a non-OK answer that is a plain 4xx rejection (403) and one that is a rate-limit (429).
+        case 'status403': return json(403, { success: false, error: { code: 'FORBIDDEN', message: 'Key refused' } });
+        case 'status429': return json(429, { success: false, error: { code: 'RATE_LIMITED', message: 'Too many requests' } });
         case 'stall': res.writeHead(200, { 'content-type': 'application/json' }); res.write('{"success":true,"data":{"valid":tr'); return;
         case 'hang': return;
       }
@@ -263,4 +269,22 @@
     expect(r.status).toBe(200);
     expect(r.forwarded.map((h) => [h.userId, String(h.authorization).startsWith('Bearer ')])).toEqual([['connector:ks1240b-conn', true]]);
   }, 15000);
+
+  // KS-1788 item 3 (gate on #1785, finding 1785-4): the `!resp.ok` branch of checkApiKey for a status that is not 5xx, 408 or 429 (cache 30 s, answer 401), and the 429 classification, had no cell.
+  it('🔴 KS-1788 a plain 4xx from the security service (403) is a REJECTION: 401 Invalid API key, nothing forwarded, a 30 s negative cache entry, and the next request is answered from it', async () => {
+    const r1 = await send(gatewayUrl, REQUIRED, { 'x-api-key': KEYS.S403 });
+    expect([r1.status, r1.code, r1.message, r1.forwarded]).toEqual([401, 'UNAUTHORIZED', 'Invalid API key', []]);
+    const cached = auth.apiKeyCache.get(KEYS.S403);
+    expect(cached?.result, 'a negative entry').toBeNull();
+    expect((cached?.expiresAt ?? 0) - Date.now(), 'about 30 s left').toBeGreaterThan(25_000);
+    const r2 = await send(gatewayUrl, REQUIRED, { 'x-api-key': KEYS.S403 });
+    expect([r2.status, r2.code], 'answered from the negative cache').toEqual([401, 'UNAUTHORIZED']);
+    expect(validateHits[KEYS.S403], 'the security service was asked once').toBe(1);
+  }, 15000);
+
+  it('🔴 KS-1788 a 429 from the security service is NOT a rejection: 503 SERVICE_UNAVAILABLE, nothing forwarded, nothing cached', async () => {
+    const r = await send(gatewayUrl, REQUIRED, { 'x-api-key': KEYS.S429 });
+    expect([r.status, r.code, r.message, r.forwarded]).toEqual([503, ...UNAVAILABLE, []]);
+    expect(auth.apiKeyCache.has(KEYS.S429), 'a check that could not complete leaves no cache entry').toBe(false);
+  }, 15000);
 });
```
