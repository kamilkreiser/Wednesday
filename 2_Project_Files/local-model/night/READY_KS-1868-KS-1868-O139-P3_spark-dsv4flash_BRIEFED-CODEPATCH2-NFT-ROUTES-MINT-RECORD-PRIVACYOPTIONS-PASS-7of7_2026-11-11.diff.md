# READY — KS-1868-KS-1868-O139-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o139_p3_nft_certificate_nft_routes_mint_record_privacy_options_catches_guard_the_thrown_value_read/out.md.checker/patch.diff`** (from `ls` at 16:32 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o139_p3_nft_certificate_nft_routes_mint_record_privacy_options_catches_guard_the_thrown_value_read/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o139_p3_nft_certificate_nft_routes_mint_record_privacy_options_catches_guard_the_thrown_value_read/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o139_p3_nft_certificate_nft_routes_mint_record_privacy_options_catches_guard_the_thrown_value_read/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 16:32 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o139_p3_nft_certificate_nft_routes_mint_record_privacy_options_catches_guard_the_thrown_value_read/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts } + { Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-mint-record-privacy-options-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts` (product) and `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-mint-record-privacy-options-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts
138	0	Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-mint-record-privacy-options-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: nft.routes.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts`; test(s): `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-mint-record-privacy-options-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-mint-record-privacy-options-catches-unreadable-throw.test.ts 138 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-mint-record-privacy-options-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 nft router catches read a thrown value safely RED ks1868 R1 POST /mint: a revoked Proxy is logged with a constant reason and answered 500', 'KS-1868 nft router catches read a thrown value safely RED ks1868 R2 POST /mint: an Error whose message getter throws is logged with a constant reason and answered 500', 'KS-1868 nft router catches read a thrown value safely RED ks1868 R3 POST /record: a revoked Proxy is logged with a constant reason and answered 500', 'KS-1868 nft router catches read a thrown value safely RED ks1868 R4 POST /record: an Error whose message getter throws is logged with a constant reason and answered 500', 'KS-1868 nft router catches read a thrown value safely RED ks1868 R5 GET /privacy-options: a revoked Proxy is logged with a constant reason and answered 500', 'KS-1868 nft router catches read a thrown value safely RED ks1868 R6 GET /privacy-options: an Error whose message getter throws is logged with a constant reason and answered 500']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=241 failed=0 | after: total=250 failed=0` · `NEW reds: []` [baseline_suite.json total=241 failed=0; after_suite.json total=250 failed=0]
- A6 [verbatim]: `PASS A6 whole services/nft-certificate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/nft-certificate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-mint-record-privacy-options-catches-unreadable-throw.test.ts` (+138/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o139_p3_nft_certificate_nft_routes_mint_record_privacy_options_catches_guard_the_thrown_value_read/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o139_p3_nft_certificate_nft_routes_mint_record_privacy_options_catches_guard_the_thrown_value_read/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o139_p3_nft_certificate_nft_routes_mint_record_privacy_options_catches_guard_the_thrown_value_read/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts b/Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts
--- a/Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts
+++ b/Blockchain/Dev/services/nft-certificate/src/routes/nft.routes.ts
@@ -116,5 +116,11 @@
     }
   } catch (error) {
-    logger.error('Error minting NFT', { error: error instanceof Error ? error.message : String(error) });
+    let reason: string;
+    try {
+      reason = error instanceof Error ? error.message : String(error);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('Error minting NFT', { error: reason });
     res.status(500).json({
       success: false,
@@ -175,5 +181,11 @@
     });
   } catch (error) {
-    logger.error('Error recording NFT mint', { error: error instanceof Error ? error.message : String(error) });
+    let reason: string;
+    try {
+      reason = error instanceof Error ? error.message : String(error);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('Error recording NFT mint', { error: reason });
     res.status(500).json({
       success: false,
@@ -364,5 +376,11 @@
     });
   } catch (error) {
-    logger.error('Error fetching privacy options', { error: error instanceof Error ? error.message : String(error) });
+    let reason: string;
+    try {
+      reason = error instanceof Error ? error.message : String(error);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error('Error fetching privacy options', { error: reason });
     res.status(500).json({
       success: false,
diff --git a/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-mint-record-privacy-options-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-mint-record-privacy-options-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-nft-mint-record-privacy-options-catches-unreadable-throw.test.ts
@@ -0,0 +1,138 @@
+import { describe, it, expect, vi } from 'vitest';
+
+// KS-1868: the nft-certificate router (src/routes/nft.routes.ts), handlers POST /mint, POST /record and GET /privacy-options, log a failure as
+// `logger.error('<message>', { error: error instanceof Error ? error.message : String(error) })` and answer 500. The read is
+// unguarded. When the thrown value cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws)
+// the catch itself throws, so the async handler REJECTS and no reply is sent. The services and the logger are plain stand-ins; the
+// handlers are read off the router stack; no server, no network. The value under test is raised from INSIDE each handler's try:
+// by a getter on the fake request (`body` or `user`, the first thing the handler reads) or, for the two handlers that read nothing
+// from the request, by the response's first `json` call (the success answer), after which the 500 answer is sent normally.
+const h = vi.hoisted(() => ({ toThrow: undefined as unknown, errors: [] as Array<[string, unknown]> }));
+
+vi.mock('../services/minting.service', () => ({ nftMintingService: {} }));
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
+type Raise = 'body' | 'user' | 'json';
+
+async function call(method: string, path: string, raise: Raise, value: unknown): Promise<Out> {
+  h.toThrow = value;
+  h.errors = [];
+  const layer = (router as unknown as { stack: Array<{ route?: { path: string; methods: Record<string, boolean>; stack: Array<{ handle: (...a: unknown[]) => unknown }> } }> }).stack.find(
+    (l) => l.route?.path === path && l.route.methods[method],
+  );
+  const handle = layer!.route!.stack[0].handle;
+  const out: Out = { rejected: false, code: undefined, body: undefined, logged: [] };
+  let jsonThrown = false;
+  const res = {
+    status(c: number) {
+      out.code = c;
+      return res;
+    },
+    json(b: unknown) {
+      if (raise === 'json' && !jsonThrown) {
+        jsonThrown = true;
+        throw h.toThrow;
+      }
+      out.body = b;
+      return res;
+    },
+  };
+  const req: Record<string, unknown> = { params: {}, query: {}, body: {}, user: { role: 'SYSTEM_ADMIN' } };
+  if (raise !== 'json') {
+    Object.defineProperty(req, raise, {
+      get() {
+        throw h.toThrow;
+      },
+    });
+  }
+  try {
+    await handle(req, res);
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
+const reply = (message: string) => ({ success: false, error: { code: 'INTERNAL_ERROR', message } });
+
+const SITES = [
+  { method: 'post', path: '/mint', raise: 'body' as Raise, logged: 'Error minting NFT', reply: 'Failed to mint NFT certificate' },
+  { method: 'post', path: '/record', raise: 'body' as Raise, logged: 'Error recording NFT mint', reply: 'Failed to record NFT mint' },
+  { method: 'get', path: '/privacy-options', raise: 'json' as Raise, logged: 'Error fetching privacy options', reply: 'Failed to fetch privacy options' },
+];
+
+describe('KS-1868 nft router catches read a thrown value safely', () => {
+  SITES.forEach((s, i) => {
+    it(`RED ks1868 R${2 * i + 1} ${s.method.toUpperCase()} ${s.path}: a revoked Proxy is logged with a constant reason and answered 500`, async () => {
+      const out = await call(s.method, s.path, s.raise, revokedProxy());
+      expect(out.rejected).toBe(false);
+      expect(out.code).toBe(500);
+      expect(out.body).toEqual(reply(s.reply));
+      expect(out.logged).toEqual([[s.logged, { error: 'unreadable thrown value' }]]);
+    });
+
+    it(`RED ks1868 R${2 * i + 2} ${s.method.toUpperCase()} ${s.path}: an Error whose message getter throws is logged with a constant reason and answered 500`, async () => {
+      const out = await call(s.method, s.path, s.raise, getterThrows());
+      expect(out.rejected).toBe(false);
+      expect(out.code).toBe(500);
+      expect(out.body).toEqual(reply(s.reply));
+      expect(out.logged).toEqual([[s.logged, { error: 'unreadable thrown value' }]]);
+    });
+  });
+
+  it(`control ks1868 C1 ${SITES[0].method.toUpperCase()} ${SITES[0].path}: an ordinary Error is logged with its message and answered 500`, async () => {
+    const out = await call(SITES[0].method, SITES[0].path, SITES[0].raise, new Error('service boom'));
+    expect(out.rejected).toBe(false);
+    expect(out.code).toBe(500);
+    expect(out.body).toEqual(reply(SITES[0].reply));
+    expect(out.logged).toEqual([[SITES[0].logged, { error: 'service boom' }]]);
+  });
+
+  it(`control ks1868 C2 ${SITES[1].method.toUpperCase()} ${SITES[1].path}: a thrown plain string is logged as text and answered 500`, async () => {
+    const out = await call(SITES[1].method, SITES[1].path, SITES[1].raise, 'plain text failure');
+    expect(out.rejected).toBe(false);
+    expect(out.code).toBe(500);
+    expect(out.body).toEqual(reply(SITES[1].reply));
+    expect(out.logged).toEqual([[SITES[1].logged, { error: 'plain text failure' }]]);
+  });
+
+  it(`control ks1868 C3 ${SITES[2].method.toUpperCase()} ${SITES[2].path}: an ordinary Error is logged with its message and answered 500`, async () => {
+    const out = await call(SITES[2].method, SITES[2].path, SITES[2].raise, new Error('service boom'));
+    expect(out.rejected).toBe(false);
+    expect(out.code).toBe(500);
+    expect(out.body).toEqual(reply(SITES[2].reply));
+    expect(out.logged).toEqual([[SITES[2].logged, { error: 'service boom' }]]);
+  });
+});
```

> STACKING NOTE (operator o139, 2026-11-11): piece 1 of 3 for nft-certificate nft.routes.ts (sites 118, 177, 366). Pieces O139-P4 (412, 558, 741) and O139-P5 (787) are the other two: hunks do not overlap, put the three in ONE PR or in order. The file is in no open PR and no other held READY (re-measured 16:1x). Wednesday: read the + lines at source before accepting.
