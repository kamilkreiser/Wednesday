# READY — KS-1868-KS-1868-O98-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o98_p3_nft_list_certificates_catch_guard/out.md.checker/patch.diff`** (from `ls` at 18:12 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o98_p3_nft_list_certificates_catch_guard/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o98_p3_nft_list_certificates_catch_guard/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o98_p3_nft_list_certificates_catch_guard/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o98_p3_nft_list_certificates_catch_guard-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 18:12 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o98_p3_nft_list_certificates_catch_guard/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `de8d208a8426747b3a752309e08167fa0de4b2ff`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts } + { Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-list-certificates-catch-guard-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts` (product) and `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-list-certificates-catch-guard-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts
106	0	Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-list-certificates-catch-guard-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: nft.routes.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts`; test(s): `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-list-certificates-catch-guard-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-list-certificates-catch-guard-catch-unreadable-throw.test.ts 106 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-list-certificates-catch-guard-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 nft router GET /certificates reads a thrown value safely RED ks1868 R1 a revoked Proxy is logged with a constant reason and answered 500', 'KS-1868 nft router GET /certificates reads a thrown value safely RED ks1868 R2 an Error whose message getter throws is logged with a constant reason and answered 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=209 failed=0 | after: total=213 failed=0` · `NEW reds: []` [baseline_suite.json total=209 failed=0; after_suite.json total=213 failed=0]
- A6 [verbatim]: `PASS A6 whole services/nft-certificate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/nft-certificate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-list-certificates-catch-guard-catch-unreadable-throw.test.ts` (+106/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `de8d208a8426747b3a752309e08167fa0de4b2ff` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o98_p3_nft_list_certificates_catch_guard/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o98_p3_nft_list_certificates_catch_guard/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o98_p3_nft_list_certificates_catch_guard/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts b/Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts
--- a/Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts
+++ b/Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts
@@ -259,7 +259,13 @@
       },
     });
   } catch (error) {
-    logger.error('Error fetching certificates', { error: error instanceof Error ? error.message : String(error) });
+    let reason: string;
+    try {
+      reason = error instanceof Error ? error.message : String(error);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('Error fetching certificates', { error: reason });
     res.status(500).json({
       success: false,
       error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch NFT certificates' },
diff --git a/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-list-certificates-catch-guard-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-list-certificates-catch-guard-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-list-certificates-catch-guard-catch-unreadable-throw.test.ts
@@ -0,0 +1,106 @@
+import { describe, it, expect, vi } from 'vitest';
+
+// KS-1868: the nft-certificate router (src/routes/nft.routes.ts), handler `GET /certificates`, logs a failure as
+// `logger.error('Error fetching certificates', { error: error instanceof Error ? error.message : String(error) })` and answers 500. The read is
+// unguarded. When the thrown value cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws)
+// the catch itself throws, so the async handler REJECTS and no reply is sent. The services and the logger are plain stand-ins
+// (the service call throws the cell's value); the handler is read off the router stack; no server, no network.
+const h = vi.hoisted(() => ({ toThrow: undefined as unknown, errors: [] as Array<[string, unknown]> }));
+
+vi.mock('../services/minting.service', () => ({ nftMintingService: { getUserNFTCertificates: () => Promise.reject(h.toThrow) } }));
+vi.mock('../services/blockchain-verifier.service', () => ({ blockchainVerifier: {} }));
+vi.mock('../services/ipfs.service', () => ({ ipfsService: {} }));
+vi.mock('../services/cost-estimator.service', () => ({ costEstimatorService: {} }));
+vi.mock('../services/metadata-builder.service', () => ({ metadataBuilderService: {} }));
+vi.mock('../utils/logger', () => ({
+  logger: {
+    error: (m: string, meta: unknown) => {
+      h.errors.push([m, meta]);
+    },
+    info: () => undefined,
+    warn: () => undefined,
+    debug: () => undefined,
+  },
+}));
+
+import router from '../routes/nft.routes';
+
+type Out = { rejected: boolean; code: number | undefined; body: unknown; logged: Array<[string, unknown]> };
+
+async function call(value: unknown): Promise<Out> {
+  h.toThrow = value;
+  h.errors = [];
+  const layer = (router as unknown as { stack: Array<{ route?: { path: string; methods: Record<string, boolean>; stack: Array<{ handle: (...a: unknown[]) => unknown }> } }> }).stack.find(
+    (l) => l.route?.path === '/certificates' && l.route.methods['get'],
+  );
+  const handle = layer!.route!.stack[0].handle;
+  const out: Out = { rejected: false, code: undefined, body: undefined, logged: [] };
+  const res = {
+    status(c: number) {
+      out.code = c;
+      return res;
+    },
+    json(b: unknown) {
+      out.body = b;
+      return res;
+    },
+  };
+  try {
+    await handle({ user: { userId: 'owner-ks1868' }, params: {}, query: {}, body: {} }, res);
+  } catch {
+    out.rejected = true;
+  }
+  out.logged = h.errors;
+  return out;
+}
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+const reply = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch NFT certificates' } };
+
+describe('KS-1868 nft router GET /certificates reads a thrown value safely', () => {
+  it('control ks1868 C1 an ordinary Error is logged with its message and answered 500', async () => {
+    const out = await call(new Error('service boom'));
+    expect(out.rejected).toBe(false);
+    expect(out.code).toBe(500);
+    expect(out.body).toEqual(reply);
+    expect(out.logged).toEqual([['Error fetching certificates', { error: 'service boom' }]]);
+  });
+
+  it('control ks1868 C2 a thrown plain string is logged as text and answered 500', async () => {
+    const out = await call('plain text failure');
+    expect(out.rejected).toBe(false);
+    expect(out.code).toBe(500);
+    expect(out.body).toEqual(reply);
+    expect(out.logged).toEqual([['Error fetching certificates', { error: 'plain text failure' }]]);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy is logged with a constant reason and answered 500', async () => {
+    const out = await call(revokedProxy());
+    expect(out.rejected).toBe(false);
+    expect(out.code).toBe(500);
+    expect(out.body).toEqual(reply);
+    expect(out.logged).toEqual([['Error fetching certificates', { error: 'unreadable thrown value' }]]);
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws is logged with a constant reason and answered 500', async () => {
+    const out = await call(getterThrows());
+    expect(out.rejected).toBe(false);
+    expect(out.code).toBe(500);
+    expect(out.body).toEqual(reply);
+    expect(out.logged).toEqual([['Error fetching certificates', { error: 'unreadable thrown value' }]]);
+  });
+});
```
