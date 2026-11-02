# READY — KS-1868-KS-1868-O91-P10 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p10_anchoring_cardano_init_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 07:46 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p10_anchoring_cardano_init_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p10_anchoring_cardano_init_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p10_anchoring_cardano_init_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p10_anchoring_cardano_init_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 07:46 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p10_anchoring_cardano_init_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/cardano/index.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-cardano-init-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/cardano/index.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-cardano-init-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
8	1	Blockchain/Dev/services/anchoring/src/cardano/index.ts
124	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-cardano-init-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (8 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: index.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/cardano/index.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-cardano-init-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/cardano/index.ts 8 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-cardano-init-catch-unreadable-throw.test.ts 124 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/cardano/index.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-cardano-init-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1868 the initCardano catch answers false and logs text for a hostile thrown value RED ks1868 R1: a provider init failure that is a revoked Proxy is logged as text and initCardano answers false, as for an ordinary Error', 'KS-1868 the initCardano catch answers false and logs text for a hostile thrown value RED ks1868 R2: a provider init failure that is an Error whose message getter throws is logged as text and initCardano answers false, as for an ordinary Error', 'KS-1868 the initCardano catch answers false and logs text for a hostile thrown value RED ks1868 R3: a provider init failure that is an Error whose message is a Symbol is logged as text and initCardano answers false, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=796 failed=2 | after: total=802 failed=2` · `NEW reds: []` [baseline_suite.json total=796 failed=2; after_suite.json total=802 failed=2]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/cardano/index.ts` (+8/-1 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-cardano-init-catch-unreadable-throw.test.ts` (+124/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/cardano/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p10_anchoring_cardano_init_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o91_p10_anchoring_cardano_init_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p10_anchoring_cardano_init_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/cardano/index.ts b/Blockchain/Dev/services/anchoring/src/cardano/index.ts
--- a/Blockchain/Dev/services/anchoring/src/cardano/index.ts
+++ b/Blockchain/Dev/services/anchoring/src/cardano/index.ts
@@ -112,7 +112,14 @@
     logger.info(`[Cardano] Integration ready — network: ${network}`);
     return true;
   } catch (err: any) {
-    logger.error(`[Cardano] Initialisation failed: ${err?.message}`);
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    logger.error(`[Cardano] Initialisation failed: ${reason}`);
     return false;
   }
 }
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-cardano-init-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-cardano-init-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1868-anchoring-cardano-init-catch-unreadable-throw.test.ts
@@ -0,0 +1,124 @@
+import { describe, it, expect, beforeEach, afterEach, vi } from 'vitest';
+
+// KS-1868 (operator 91 screen, anchoring cardano module): the initialisation catch of initCardano (line 115) of
+// services/anchoring/src/cardano/index.ts interpolates `err?.message` into the logger.error template, unguarded.
+// A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws) makes the catch itself throw:
+// initCardano REJECTS to its boot caller (index.ts, `await initCardano(...)`) instead of logging and answering false (real
+// minting unavailable, `cardanoConfigured` already recorded as true so /health can say "configured but not ready"); an Error
+// whose message is readable but not a string is interpolated by the template literal, which throws for a Symbol. The cells
+// make the Blockfrost provider initialisation throw such a value and assert initCardano resolves false and the logged line
+// carries text (the constant when the value cannot be turned into text). Harness: the real module with ./provider, ./wallet,
+// ./transaction, ./confirmation, the mock provider, the wallet view and spend modules and the attempt-family module replaced by
+// plain stand-ins and the logger by a plain recording object (no Blockfrost, no wallet).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  errors: [] as unknown[][],
+}));
+
+vi.mock('../cardano/provider', () => ({
+  initProvider: () => {
+    throw h.toThrow;
+  },
+  fetchProtocolParams: async () => ({}),
+  fetchUtxosAll: async () => [],
+  fetchLiveTip: async () => null,
+  getTransaction: async () => null,
+  submitTransaction: async () => 'hash',
+}));
+vi.mock('../cardano/wallet', () => ({ initWallet: () => ({ address: 'addr_test1stub' }) }));
+vi.mock('../cardano/transaction', () => ({ buildAnchorTransaction: async () => ({}) }));
+vi.mock('../cardano/confirmation', () => ({ waitForConfirmation: async () => ({}) }));
+vi.mock('../mocks/mockProvider', () => ({ MockAnchoringProvider: class MockAnchoringProviderStub {} }));
+vi.mock('../walletView', () => ({ platformWalletView: () => ({}) }));
+vi.mock('../walletSpend', () => ({ spendFromView: () => ({}), payloadDigest: () => 'digest' }));
+vi.mock('../attemptFamily', () => ({ platformBootArm: { observe: () => undefined } }));
+vi.mock('../utils/logger', () => {
+  const rec = (message: string) => {
+    h.errors.push([message]);
+  };
+  return { logger: { debug: () => undefined, info: () => undefined, warn: () => undefined, error: rec } };
+});
+
+import { initCardano } from '../cardano';
+
+const PREFIX = '[Cardano] Initialisation failed: ';
+const realKey = process.env.BLOCKFROST_API_KEY;
+const realMnemonic = process.env.PLATFORM_WALLET_MNEMONIC;
+const realDemo = process.env.DEMO_MODE;
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.errors.length = 0;
+  delete process.env.DEMO_MODE;
+  process.env.BLOCKFROST_API_KEY = 'preprodStubKey';
+  process.env.PLATFORM_WALLET_MNEMONIC = 'stub mnemonic words';
+});
+afterEach(() => {
+  if (realKey === undefined) delete process.env.BLOCKFROST_API_KEY;
+  else process.env.BLOCKFROST_API_KEY = realKey;
+  if (realMnemonic === undefined) delete process.env.PLATFORM_WALLET_MNEMONIC;
+  else process.env.PLATFORM_WALLET_MNEMONIC = realMnemonic;
+  if (realDemo === undefined) delete process.env.DEMO_MODE;
+  else process.env.DEMO_MODE = realDemo;
+});
+
+async function run(value: unknown): Promise<{ ok: boolean; value: boolean | undefined }> {
+  h.toThrow = value;
+  try {
+    return { ok: true, value: await initCardano('preprod') };
+  } catch {
+    return { ok: false, value: undefined };
+  }
+}
+const LINES = () => h.errors.filter((a) => typeof a[0] === 'string' && (a[0] as string).startsWith(PREFIX));
+/** The text after the prefix of the logged line. */
+const reasonOf = (a: unknown[] | undefined): string => (a ? (a[0] as string).slice(PREFIX.length) : '<none>');
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
+describe('KS-1868 the initCardano catch answers false and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the provider init is logged with its message and initCardano answers false', async () => {
+    expect(await run(new Error('provider boom'))).toEqual({ ok: true, value: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('provider boom');
+  });
+  it('control ks1868 C2: a thrown plain string is logged as undefined text and initCardano answers false', async () => {
+    expect(await run('plain boom')).toEqual({ ok: true, value: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('undefined');
+  });
+  it('control ks1868 C3: an Error with an empty message is logged with the empty text and initCardano answers false', async () => {
+    expect(await run(new Error(''))).toEqual({ ok: true, value: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('');
+  });
+  it('RED ks1868 R1: a provider init failure that is a revoked Proxy is logged as text and initCardano answers false, as for an ordinary Error', async () => {
+    expect(await run(revokedProxy())).toEqual({ ok: true, value: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: a provider init failure that is an Error whose message getter throws is logged as text and initCardano answers false, as for an ordinary Error', async () => {
+    expect(await run(getterThrows())).toEqual({ ok: true, value: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: a provider init failure that is an Error whose message is a Symbol is logged as text and initCardano answers false, as for an ordinary Error', async () => {
+    expect(await run(withMessage(Symbol('ks1868')))).toEqual({ ok: true, value: false });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('Symbol(ks1868)');
+  });
+});
```
