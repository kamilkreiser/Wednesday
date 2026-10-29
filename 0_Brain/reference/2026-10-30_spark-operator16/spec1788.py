# KS-1788 item 3 (tier-1 gate on #1785, finding 1785-4): the non-OK 4xx branch of checkApiKey has no cell (gate mutants F7, F8, F18 survived 40 green cells). Spark operator 16. test_only, gen/mk_testonly.py.
PROD = 'Blockchain/Dev/services/api-gateway/src/middleware/auth.ts'
TEST = 'Blockchain/Dev/services/api-gateway/src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts'
E1 = ("type Validate = 'valid' | 'rejected' | 'hang' | 'stall' | 'security503';\n",
      "type Validate = 'valid' | 'rejected' | 'hang' | 'stall' | 'security503' | 'status403' | 'status429';\n")
E2 = ("  SEC503: 'sk_ks1240b_security_503_001',\n",
      "  SEC503: 'sk_ks1240b_security_503_001',\n  S403: 'sk_ks1788_security_403_0001',\n  S429: 'sk_ks1788_security_429_0001',\n")
E3 = ("  [KEYS.EXCH_HANG]: 'valid', [KEYS.EXCH_STALL]: 'valid',\n};\n",
      "  [KEYS.EXCH_HANG]: 'valid', [KEYS.EXCH_STALL]: 'valid',\n  [KEYS.S403]: 'status403', [KEYS.S429]: 'status429',\n};\n")
E4 = ("        case 'stall': res.writeHead(200, { 'content-type': 'application/json' }); res.write('{\"success\":true,\"data\":{\"valid\":tr'); return;\n",
      "        // KS-1788 item 3: a non-OK answer that is a plain 4xx rejection (403) and one that is a rate-limit (429).\n"
      "        case 'status403': return json(403, { success: false, error: { code: 'FORBIDDEN', message: 'Key refused' } });\n"
      "        case 'status429': return json(429, { success: false, error: { code: 'RATE_LIMITED', message: 'Too many requests' } });\n"
      "        case 'stall': res.writeHead(200, { 'content-type': 'application/json' }); res.write('{\"success\":true,\"data\":{\"valid\":tr'); return;\n")
CELLS = '''
  // KS-1788 item 3 (gate on #1785, finding 1785-4): the `!resp.ok` branch of checkApiKey for a status that is not 5xx, 408 or 429 (cache 30 s, answer 401), and the 429 classification, had no cell.
  it('🔴 KS-1788 a plain 4xx from the security service (403) is a REJECTION: 401 Invalid API key, nothing forwarded, a 30 s negative cache entry, and the next request is answered from it', async () => {
    const r1 = await send(gatewayUrl, REQUIRED, { 'x-api-key': KEYS.S403 });
    expect([r1.status, r1.code, r1.message, r1.forwarded]).toEqual([401, 'UNAUTHORIZED', 'Invalid API key', []]);
    const cached = auth.apiKeyCache.get(KEYS.S403);
    expect(cached?.result, 'a negative entry').toBeNull();
    expect((cached?.expiresAt ?? 0) - Date.now(), 'about 30 s left').toBeGreaterThan(25_000);
    const r2 = await send(gatewayUrl, REQUIRED, { 'x-api-key': KEYS.S403 });
    expect([r2.status, r2.code], 'answered from the negative cache').toEqual([401, 'UNAUTHORIZED']);
    expect(validateHits[KEYS.S403], 'the security service was asked once').toBe(1);
  }, 15000);

  it('🔴 KS-1788 a 429 from the security service is NOT a rejection: 503 SERVICE_UNAVAILABLE, nothing forwarded, nothing cached', async () => {
    const r = await send(gatewayUrl, REQUIRED, { 'x-api-key': KEYS.S429 });
    expect([r.status, r.code, r.message, r.forwarded]).toEqual([503, ...UNAVAILABLE, []]);
    expect(auth.apiKeyCache.has(KEYS.S429), 'a check that could not complete leaves no cache entry').toBe(false);
  }, 15000);
'''
E5 = ("    expect(r.forwarded.map((h) => [h.userId, String(h.authorization).startsWith('Bearer ')])).toEqual([['connector:ks1240b-conn', true]]);\n  }, 15000);\n});\n",
      "    expect(r.forwarded.map((h) => [h.userId, String(h.authorization).startsWith('Bearer ')])).toEqual([['connector:ks1240b-conn', true]]);\n  }, 15000);\n" + CELLS + "});\n")
FROM = "  return status >= 500 || status === 408 || status === 429;"
TO = "  return status >= 500 || status === 408 || status === 403;"
T = dict(dir='ks_1788_p1_checkapikey_4xx',
 ticket='KS-1788',
 title="api-gateway ks1240b front-door test: the non-OK 4xx branch of checkApiKey has no cell (gate 1785-4, mutants F7 and F8 survive all 40 cells): add a 403 stub (a rejection, cached 30 s) and a 429 stub (unavailable, 503, uncached) (KS-1788 item 3; RUNG 3, TEST-ONLY: one in-place test file, five hunks, with a planted tamper; the product does not change)",
 intro="DRAFT by Spark operator 16 for Wednesday, 2026-10-30 AEDT. Secuura (Platform K / api-gateway) only. A local PASS is a candidate, never a merge; the normal QA gate before merge. **The tamper target `middleware/auth.ts` is an authentication file; the Spark edits only the test, but a PR touching the auth test family gets a tier-1 gate (routing row 4).** Origin: KS-1788 item 3 (tier-1 gate on #1785, finding 1785-4). ONLY item 3 is in this brief; items 1 and 2 (the timeout answer, two unbounded `http.request` forwards) change behaviour and stay with Claude seats. The product is right today for both branches; the gap is a missing pin. Link the PR as Refs KS-1788 and KS-1240, never a close-word.",
 product=PROD, test=TEST, ref='Blockchain/Dev/services/api-gateway/src/__tests__/ks1207-a-failed-optional-api-key-falls-through-to-the-bearer-check.test.ts',
 tamper_line=205, tamper_from=FROM, tamper_to=TO,
 statement_ok="line 205 is the one `return` of `couldNotAnswer`; the tamper swaps `429` for `403`, so a 429 is read as a plain rejection (gate mutant F7) and a 403 is read as 'could not answer' (gate mutant F8); the file compiles and 5xx and 408 are untouched, so every existing cell stays green",
 edit=[E1, E2, E3, E4, E5],
 nh_txt='5 edits (they appear as 5 hunks): the Validate type, two keys and two table rows near the top; two stub cases in the validate switch; two cells at the end of the controls describe',
 nh_word='the hunks listed below',
 nh_head='EDITS in the TEST file (the hunks below)',
 red=['KS-1788 a plain 4xx from the security service (403) is a REJECTION', 'KS-1788 a 429 from the security service is NOT a rejection'],
 runner='vitest` (`npx vitest run src/__tests__/ks1240b-front-door-key-exchange-timeout-answers-503-not-401.test.ts` from `Blockchain/Dev/services/api-gateway',
 rung='3 (test-only mode: a planted tamper must redden the new cells; the hunks are given byte-exact)',
 what_wrong="`checkApiKey` (`middleware/auth.ts`) has a `!resp.ok` branch: a status that `couldNotAnswer` accepts (5xx, 408, 429) returns `unavailable` and is never cached, any other non-OK status is cached as a rejection for 30 s and answered 401. The KS-1240 front-door test file stubs only a 200 `valid:false` rejection and a 503, so the tier-1 gate on #1785 found three mutants that survive all 40 cells: F7 (a 429 treated as a rejection), F8 (every non-OK status treated as unavailable, so a 4xx rejection becomes 503) and F18 (a non-OK 4xx rejection not cached). Add two validate-stub modes to the file's own upstream stub (a 403 answer and a 429 answer), two keys, and two cells that use them through the real app on the required mount `/api/documents`.",
 where="- `src/middleware/auth.ts:205` - (correct, STAYS) the one return of `couldNotAnswer`; the line the tamper replaces in the checker's clone.\n- Test file: the `Validate` type is :57; `KEYS` runs :58-70 (`SEC503` is :67); the `validateAs` table is :71-75 (its last row is :74 and `};` is :75); the stub switch has `case 'stall':` at :150; the controls describe is :243-266: its last cell (`control: a valid key is forwarded ...`) is :261-265 and `});` at :266 closes the describe. **The two new cells go between :265 and :266.** `send`, `gatewayUrl`, `REQUIRED`, `UNAVAILABLE`, `auth`, `validateHits` and `KEYS` are in scope at module level.",
 cells="- RED under the tamper: both `🔴 KS-1788 ...` cells fail by assertion (the 403 answers 503 and is not cached; the 429 answers 401 and is cached).\n- GREEN at the untouched tip: both new cells and every existing cell.\n- F18 (a non-OK 4xx rejection not cached) is NOT the planted tamper; the 403 cell's negative-cache assertions are written to catch it (the operator ran that mutant separately, see the report).\n- The tamper keeps every existing cell green (5xx and 408 are unchanged and no existing key gets a 403 or a 429).",
 unmeasured="- The drafter did NOT run vitest through the round machinery for the brief; the RED-under-tamper / GREEN-at-tip result is the `round.sh --control` run on this golden.\n- Items 1 and 2 of KS-1788 are not covered.\n- The 429 body and the 403 body shape in the stub are inventions (the product reads only the status).\n- Open PRs touching either file: see the overlap count in the operator report.",
 scope="**KS-1788 item 3 only.** Link the PR as Refs KS-1788 and KS-1240, never a close-word. No product file changes.",
)
