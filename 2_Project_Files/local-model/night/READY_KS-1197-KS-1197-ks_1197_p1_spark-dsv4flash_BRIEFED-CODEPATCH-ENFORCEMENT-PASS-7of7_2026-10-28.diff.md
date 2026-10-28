# READY — KS-1197-KS-1197-ks_1197_p1 (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1197_p1/out.md.checker/patch.diff`** (from `ls` at 13:50 2026-10-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1197_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1197_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1197_p1/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1197_p1-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 13:50 2026-10-28 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1197_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `1d07ce26ae2fa6e03ea73cf73579a3c812f672f9`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/api-gateway/src/services/enforcement.ts , Blockchain/Dev/services/api-gateway/src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/api-gateway/src/services/enforcement.ts` (product) and `Blockchain/Dev/services/api-gateway/src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	2	Blockchain/Dev/services/api-gateway/src/services/enforcement.ts
102	0	Blockchain/Dev/services/api-gateway/src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (3 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 3 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/api-gateway/src/services/enforcement.ts byte-exact incl. leading whitespace (apply mode strict): OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)` [a3i_indent.out: `OK 3 line(s) byte-exact incl. leading whitespace (of 3; 3 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/api-gateway/src/services/enforcement.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/api-gateway/src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts fails at the untouched tip (9 failed / 13 run; controls green; assertion reds)` [red_first.json: failed=9 of total=13; red cell(s): ['KS-1197: a non-string verification level ranks as none RED KS-1197 K1 a number level meets nothing above none: a standard type refuses it with 403', 'KS-1197: a non-string verification level ranks as none RED KS-1197 K1 a array level meets nothing above none: a standard type refuses it with 403', 'KS-1197: a non-string verification level ranks as none RED KS-1197 K1 a object level meets nothing above none: a standard type refuses it with 403', 'KS-1197: a non-string verification level ranks as none RED KS-1197 K2 the 403 text names the level as NONE', 'KS-1197: a non-string verification level ranks as none RED KS-1197 K3 a number level still meets a none requirement: a none type admits it', 'KS-1197: a non-string verification level ranks as none RED KS-1197 K3 a array level still meets a none requirement: a none type admits it', 'KS-1197: a non-string verification level ranks as none RED KS-1197 K3 a object level still meets a none requirement: a none type admits it', 'KS-1197: a non-string verification level ranks as none RED KS-1197 K4 meetsVerificationLevel of a number is true against none and false against basic', 'KS-1197: a non-string verification level ranks as none RED KS-1197 K5 meetsVerificationLevel of an array or an object is true against none and false against basic']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts passes with the product hunk (13 passed / 13 run)` [green_after.json: failed=0 of total=13, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1255 failed=0 | after: total=1268 failed=0` · `NEW reds: []` [baseline_suite.json total=1255 failed=0; after_suite.json total=1268 failed=0]
- A6 [verbatim]: `PASS A6 whole services/api-gateway suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/api-gateway: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +105/-2 test=src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/api-gateway/src/services/enforcement.ts` (+3/-2 per numstat.out) and the test file `Blockchain/Dev/services/api-gateway/src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts` (+102/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `1d07ce26ae2fa6e03ea73cf73579a3c812f672f9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1197_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1197_p1/KS-1197.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-28_ks_1197_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/api-gateway/src/services/enforcement.ts b/Blockchain/Dev/services/api-gateway/src/services/enforcement.ts
--- a/Blockchain/Dev/services/api-gateway/src/services/enforcement.ts
+++ b/Blockchain/Dev/services/api-gateway/src/services/enforcement.ts
@@ -54,5 +54,6 @@
 export function meetsVerificationLevel(userLevel: string, requiredLevel: string): boolean {
-  const userIdx = VERIFICATION_LEVEL_ORDER.indexOf((userLevel || 'none').toLowerCase());
+  // KS-1197: a level that is not a string (a number, an array, an object off a token claim) made `.toLowerCase()` throw. It now ranks as 'none', the same as any unrecognised level (KS-1176).
+  const userIdx = VERIFICATION_LEVEL_ORDER.indexOf((typeof userLevel === 'string' && userLevel ? userLevel : 'none').toLowerCase());
   const reqIdx = VERIFICATION_LEVEL_ORDER.indexOf((requiredLevel || 'none').toLowerCase());
   // KS-1176: a user level outside the order ranks as 'none'. A connector key carries
   // 'api_key' (middleware/auth.ts), which indexOf read as -1, and `-1 >= 0` failed even a
@@ -151,5 +152,5 @@
   const requiredLevel = (docType.creatorVerificationLevel as string) || 'none';
-  const userLevel = user.verificationLevel || 'none';
+  const userLevel = typeof user.verificationLevel === 'string' && user.verificationLevel ? user.verificationLevel : 'none';
   if (!meetsVerificationLevel(userLevel, requiredLevel)) {
     return {
       ok: false, status: 403,
diff --git a/Blockchain/Dev/services/api-gateway/src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/api-gateway/src/__tests__/ks1197-a-non-string-verification-level-ranks-as-none.test.ts
@@ -0,0 +1,102 @@
+/**
+ * KS-1197 (api-gateway services/enforcement.ts): a verificationLevel that is not a string made POST /api/documents answer 500. `meetsVerificationLevel` read
+ * `(userLevel || 'none').toLowerCase()`, and `enforceDocumentTypeRules` read `user.verificationLevel || 'none'` and later `userLevel.toUpperCase()` in its 403 text; a
+ * truthy non-string (a number, an array, an object) passed the `||` and threw a TypeError. A level that is not a string now ranks as 'none', the lowest authenticated level,
+ * exactly as an unrecognised level already does (KS-1176): it meets a 'none' requirement and nothing above it. Every cell reads a thrown error as the string THREW, so a red is an
+ * assertion. K1-K5 are red at the tip; C1-C4 pin the known levels and the connector-key level, which must not change.
+ */
+
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+import { enforceDocumentTypeRules, meetsVerificationLevel } from '../services/enforcement';
+import type { UserPayload } from '../services/enforcement';
+
+vi.mock('../services/redis', () => ({
+  getAllDocumentTypes: vi.fn(),
+  getWorkflow: vi.fn(),
+  setWorkflowInstance: vi.fn(),
+  setPendingDocument: vi.fn(),
+}));
+
+import * as redisService from '../services/redis';
+
+type Outcome = string | [boolean, number | undefined, string | undefined];
+
+async function enforce(level: unknown, required: string): Promise<Outcome> {
+  vi.mocked(redisService.getAllDocumentTypes).mockResolvedValue([
+    { id: 'dt-1', code: 'DEGREE', isActive: true, creatorVerificationLevel: required },
+  ]);
+  const user = { userId: 'u-1', email: 'u@example.test', role: 'OWNER', verificationLevel: level } as unknown as UserPayload;
+  try {
+    const result = await enforceDocumentTypeRules({ documentType: 'DEGREE' }, user);
+    return [result.ok, (result as { status?: number }).status, (result as { code?: string }).code];
+  } catch (err) {
+    return 'THREW ' + (err instanceof Error ? err.message : String(err));
+  }
+}
+
+function meets(level: unknown, required: string): boolean | string {
+  try {
+    return meetsVerificationLevel(level as string, required);
+  } catch (err) {
+    return 'THREW ' + (err instanceof Error ? err.message : String(err));
+  }
+}
+
+const REFUSED: Outcome = [false, 403, 'INSUFFICIENT_VERIFICATION_LEVEL'];
+const ADMITTED: Outcome = [true, undefined, undefined];
+
+describe('KS-1197: a non-string verification level ranks as none', () => {
+  beforeEach(() => vi.clearAllMocks());
+
+  it.each([
+    ['number', 7],
+    ['array', ['high']],
+    ['object', {}],
+  ])('RED KS-1197 K1 a %s level meets nothing above none: a standard type refuses it with 403', async (_kind, level) => {
+    expect(await enforce(level, 'standard')).toEqual(REFUSED);
+  });
+
+  it('RED KS-1197 K2 the 403 text names the level as NONE', async () => {
+    vi.mocked(redisService.getAllDocumentTypes).mockResolvedValue([{ id: 'dt-1', code: 'DEGREE', isActive: true, creatorVerificationLevel: 'standard' }]);
+    const user = { userId: 'u-1', email: 'u@example.test', role: 'OWNER', verificationLevel: 7 } as unknown as UserPayload;
+    let message = 'THREW';
+    try {
+      message = (await enforceDocumentTypeRules({ documentType: 'DEGREE' }, user) as { error?: string }).error ?? 'no error text';
+    } catch {
+      message = 'THREW';
+    }
+    expect(message).toBe('This document type requires STANDARD verification. Your current level is NONE.');
+  });
+
+  it.each([
+    ['number', 7],
+    ['array', ['high']],
+    ['object', {}],
+  ])('RED KS-1197 K3 a %s level still meets a none requirement: a none type admits it', async (_kind, level) => {
+    expect(await enforce(level, 'none')).toEqual(ADMITTED);
+  });
+
+  it('RED KS-1197 K4 meetsVerificationLevel of a number is true against none and false against basic', () => {
+    expect([meets(7, 'none'), meets(7, 'basic')]).toEqual([true, false]);
+  });
+
+  it('RED KS-1197 K5 meetsVerificationLevel of an array or an object is true against none and false against basic', () => {
+    expect([meets(['high'], 'none'), meets(['high'], 'basic'), meets({}, 'none'), meets({}, 'basic')]).toEqual([true, false, true, false]);
+  });
+
+  it('control KS-1197 C1 a level that meets the requirement is admitted, case-insensitively', async () => {
+    expect([await enforce('standard', 'standard'), await enforce('HIGH', 'standard')]).toEqual([ADMITTED, ADMITTED]);
+  });
+
+  it('control KS-1197 C2 a known level below the requirement is still refused with 403', async () => {
+    expect(await enforce('basic', 'standard')).toEqual(REFUSED);
+  });
+
+  it('control KS-1197 C3 the connector-key level api_key still ranks as none: admitted on a none type, refused on a basic one', async () => {
+    expect([await enforce('api_key', 'none'), await enforce('api_key', 'basic')]).toEqual([ADMITTED, REFUSED]);
+  });
+
+  it('control KS-1197 C4 an absent or empty level still ranks as none', async () => {
+    expect([await enforce(undefined, 'none'), await enforce('', 'none'), await enforce('', 'basic')]).toEqual([ADMITTED, ADMITTED, REFUSED]);
+  });
+});
```

## DECISION NOTE (source-read, Spark operator for Wednesday, 2026-10-28 PM) - HOLD-WITH-DECISION: partial fix, consumer-side shape chosen by the drafter, security-adjacent
- KS-1197 = a non-string `verificationLevel` claim: `POST /api/documents` answers 500 AND a verifier-gated verify never answers (async throw). This patch fixes ONLY the POST /api/documents half. The verify-handler half was in open PR #1756's file set when drafted (#1756 has since merged; that half is now a candidate for a later brief). The ticket recommends a different place for the fix (validating the claim at the source); the drafter fixed the CONSUMER in `services/api-gateway/src/services/enforcement.ts` instead.
- What changes (2 hunks): `meetsVerificationLevel` folds a non-string/empty `userLevel` to `'none'` before `.toLowerCase()` (a number, array or object off a token claim used to throw); `enforceDocumentTypeRules` does the same for `user.verificationLevel`. A non-string level therefore RANKS AS NONE, the same as any unrecognised level (KS-1176's rule for `api_key`).
- Direction of the change: it fails toward LESS access (a non-string level ranks lowest). A valid string level is byte-for-byte as before (the 16 rows of the new test include case-insensitive admit, known-below refuse, `api_key` rank none, absent/empty rank none).
- Not covered (stated): `requiredLevel` (from the document type, `creatorVerificationLevel as string`) is still `(requiredLevel || 'none').toLowerCase()` and would still throw on a non-string; that value comes from the catalogue row, not a token claim, so the drafter left it. The 403 text now names the level as NONE for such callers (cell K2).
- Verdict: HOLD-WITH-DECISION: the owner confirms consumer-side vs source-side validation; keep as Refs KS-1197 (verify-handler half open), never a close-word.
