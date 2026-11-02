# READY — KS-1868-KS-1868-O80-G2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g2_nftcertificate_blockchain_verifier_catches_coerce_message/out.md.checker/patch.diff`** (from `ls` at 18:13 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g2_nftcertificate_blockchain_verifier_catches_coerce_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g2_nftcertificate_blockchain_verifier_catches_coerce_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g2_nftcertificate_blockchain_verifier_catches_coerce_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g2_nftcertificate_blockchain_verifier_catches_coerce_message-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 18:13 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g2_nftcertificate_blockchain_verifier_catches_coerce_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `c234c2388a162385eae32b9d5dc31de781f13908`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts } + { Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-message-coercion-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts` (product) and `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-message-coercion-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
3	3	Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts
159	0	Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-message-coercion-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (3 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: blockchain-verifier.service.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts`; test(s): `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-message-coercion-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-message-coercion-unreadable-throw.test.ts 159 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-message-coercion-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (7 failed / 10 run; controls green; assertion reds)` [red_first.json: failed=7 of total=10; red cell(s): ['KS-1868 `BlockchainVerifierService` coerces a non-string message safely RED ks1868 R1 init: a message that is a revoked Proxy logs a constant reason and verification stays pending', 'KS-1868 `BlockchainVerifierService` coerces a non-string message safely RED ks1868 R2 init: a message whose toString throws logs a constant reason and verification stays pending', 'KS-1868 `BlockchainVerifierService` coerces a non-string message safely RED ks1868 R3 init: a null-prototype message logs a constant reason and verification stays pending', 'KS-1868 `BlockchainVerifierService` coerces a non-string message safely RED ks1868 R4 lookup: an Error whose message is a revoked Proxy answers an unverified error status with a constant reason', 'KS-1868 `BlockchainVerifierService` coerces a non-string message safely RED ks1868 R5 lookup: an Error whose message toString throws answers an unverified error status with a constant reason', 'KS-1868 `BlockchainVerifierService` coerces a non-string message safely RED ks1868 R6 lookup: an Error with a null-prototype message answers an unverified error status with a constant reason', 'KS-1868 `BlockchainVerifierService` coerces a non-string message safely RED ks1868 R7 lookup: a non-Error object whose message is a revoked Proxy answers an unverified error status with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (10 passed / 10 run)` [green_after.json: failed=0 of total=10, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=178 failed=0 | after: total=188 failed=0` · `NEW reds: []` [baseline_suite.json total=178 failed=0; after_suite.json total=188 failed=0]
- A6 [verbatim]: `PASS A6 whole services/nft-certificate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/nft-certificate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts` (+3/-3 per numstat.out) and the test file `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-message-coercion-unreadable-throw.test.ts` (+159/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `c234c2388a162385eae32b9d5dc31de781f13908` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g2_nftcertificate_blockchain_verifier_catches_coerce_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o80_g2_nftcertificate_blockchain_verifier_catches_coerce_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o80_g2_nftcertificate_blockchain_verifier_catches_coerce_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts b/Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts
--- a/Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts
+++ b/Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts
@@ -67,7 +67,7 @@
       // "verification disabled", never escape as a 500.
       let reason: string;
       try {
-        reason = err instanceof Error ? err.message : String(err);
+        reason = String(err instanceof Error ? err.message : err);
       } catch {
         reason = 'unreadable thrown value';
       }
@@ -108,8 +108,8 @@
       // Blockfrost returns 404 for transactions not yet on-chain
       try {
         void (err as { status_code?: number }).status_code;
-        void (err instanceof Error ? err.message : String(err));
-        void (err as Error).message;
+        void String(err instanceof Error ? err.message : err);
+        void String((err as Error).message);
       } catch {
         logger.error('Error verifying transaction', { error: 'unreadable thrown value' });
         return { verified: false, status: 'error', error: 'unreadable thrown value' };
diff --git a/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-message-coercion-unreadable-throw.test.ts b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-message-coercion-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-message-coercion-unreadable-throw.test.ts
@@ -0,0 +1,159 @@
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+
+// KS-1868 (QA gate 109, G109-F1/F2): `BlockchainVerifierService` guards the READ of the thrown value's `message`
+// in its two catch blocks, but does not coerce it. When the `message` getter SUCCEEDS and returns a hostile
+// NON-string (a revoked Proxy, an object whose `toString` throws, a null-prototype object), the hostile value is
+// logged and returned as is: the real winston logger throws while formatting it, so the route answers 500 and
+// stores nothing. Two catch blocks: the Blockfrost client construction in `getClient` (answers "verification
+// disabled", i.e. a pending verification) and the transaction lookup in `verifyTransaction` (answers an
+// unverified 'error' status). The Blockfrost stand-in is a plain class, not vi.fn(): a spy inspects what it
+// rejects with and could itself fail on a revoked Proxy before the code under test saw it.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  initThrows: false,
+  warn: vi.fn(),
+  error: vi.fn(),
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: h.warn, error: h.error, debug: vi.fn() },
+}));
+
+vi.mock('@blockfrost/blockfrost-js', () => ({
+  BlockFrostAPI: class {
+    constructor() {
+      if (h.initThrows) throw h.toThrow;
+    }
+    txs() {
+      return Promise.reject(h.toThrow);
+    }
+  },
+}));
+
+import { BlockchainVerifierService } from '../services/blockchain-verifier.service';
+
+const HASH = 'ks1868txhash';
+
+const revoked = () => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+
+const toStringThrows = () => ({
+  toString() {
+    throw new Error('toString boom');
+  },
+});
+
+// An Error whose `message` getter succeeds but returns the given value.
+const withMessage = (value: () => unknown) =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        return value();
+      },
+    },
+  });
+
+// Compare strings, never a hostile value: `toEqual` on a revoked Proxy would throw inside the assertion itself.
+const plain = (v: unknown): unknown => (typeof v === 'string' ? v : '<non-string>');
+
+const answer = async (): Promise<unknown> => {
+  try {
+    const r = (await new BlockchainVerifierService().verifyTransaction(HASH)) as unknown as Record<string, unknown>;
+    const out: Record<string, unknown> = { verified: r.verified, status: r.status };
+    if ('error' in r) out.error = plain(r.error);
+    return { resolved: out };
+  } catch (e) {
+    return { rejected: true };
+  }
+};
+
+const logged = (fn: { mock: { calls: unknown[][] } }, text: string): unknown[] =>
+  fn.mock.calls.filter((c) => String(c[0]).includes(text)).map((c) => plain((c[1] as { error?: unknown }).error));
+
+const UNREADABLE = ['unreadable thrown value'];
+const LOOKUP_UNREADABLE = { resolved: { verified: false, status: 'error', error: 'unreadable thrown value' } };
+
+describe('KS-1868 `BlockchainVerifierService` coerces a non-string message safely', () => {
+  const saved = process.env.BLOCKFROST_API_KEY;
+
+  beforeEach(() => {
+    h.toThrow = undefined;
+    h.initThrows = false;
+    h.warn.mockReset();
+    h.error.mockReset();
+    process.env.BLOCKFROST_API_KEY = 'ks1868-real-looking-key';
+  });
+
+  afterEach(() => {
+    if (saved === undefined) delete process.env.BLOCKFROST_API_KEY;
+    else process.env.BLOCKFROST_API_KEY = saved;
+  });
+
+  it('control ks1868 C1 init: an ordinary Error from the client constructor logs its message and verification stays pending', async () => {
+    h.initThrows = true;
+    h.toThrow = new Error('bad project id');
+    expect(await answer()).toEqual({ resolved: { verified: false, status: 'pending' } });
+    expect(logged(h.warn, 'Blockfrost client init failed')).toEqual(['bad project id']);
+  });
+
+  it('control ks1868 C2 init: a thrown plain string is logged as itself and verification stays pending', async () => {
+    h.initThrows = true;
+    h.toThrow = 'plain string';
+    expect(await answer()).toEqual({ resolved: { verified: false, status: 'pending' } });
+    expect(logged(h.warn, 'Blockfrost client init failed')).toEqual(['plain string']);
+  });
+
+  it('control ks1868 C3 lookup: an ordinary Error logs its message and answers an unverified error status', async () => {
+    h.toThrow = new Error('upstream 500');
+    expect(await answer()).toEqual({ resolved: { verified: false, status: 'error', error: 'upstream 500' } });
+    expect(logged(h.error, 'Error verifying transaction')).toEqual(['upstream 500']);
+  });
+
+  it('RED ks1868 R1 init: a message that is a revoked Proxy logs a constant reason and verification stays pending', async () => {
+    h.initThrows = true;
+    h.toThrow = withMessage(revoked);
+    expect(await answer()).toEqual({ resolved: { verified: false, status: 'pending' } });
+    expect(logged(h.warn, 'Blockfrost client init failed')).toEqual(UNREADABLE);
+  });
+
+  it('RED ks1868 R2 init: a message whose toString throws logs a constant reason and verification stays pending', async () => {
+    h.initThrows = true;
+    h.toThrow = withMessage(toStringThrows);
+    expect(await answer()).toEqual({ resolved: { verified: false, status: 'pending' } });
+    expect(logged(h.warn, 'Blockfrost client init failed')).toEqual(UNREADABLE);
+  });
+
+  it('RED ks1868 R3 init: a null-prototype message logs a constant reason and verification stays pending', async () => {
+    h.initThrows = true;
+    h.toThrow = withMessage(() => Object.create(null));
+    expect(await answer()).toEqual({ resolved: { verified: false, status: 'pending' } });
+    expect(logged(h.warn, 'Blockfrost client init failed')).toEqual(UNREADABLE);
+  });
+
+  it('RED ks1868 R4 lookup: an Error whose message is a revoked Proxy answers an unverified error status with a constant reason', async () => {
+    h.toThrow = withMessage(revoked);
+    expect(await answer()).toEqual(LOOKUP_UNREADABLE);
+    expect(logged(h.error, 'Error verifying transaction')).toEqual(UNREADABLE);
+  });
+
+  it('RED ks1868 R5 lookup: an Error whose message toString throws answers an unverified error status with a constant reason', async () => {
+    h.toThrow = withMessage(toStringThrows);
+    expect(await answer()).toEqual(LOOKUP_UNREADABLE);
+    expect(logged(h.error, 'Error verifying transaction')).toEqual(UNREADABLE);
+  });
+
+  it('RED ks1868 R6 lookup: an Error with a null-prototype message answers an unverified error status with a constant reason', async () => {
+    h.toThrow = withMessage(() => Object.create(null));
+    expect(await answer()).toEqual(LOOKUP_UNREADABLE);
+    expect(logged(h.error, 'Error verifying transaction')).toEqual(UNREADABLE);
+  });
+
+  it('RED ks1868 R7 lookup: a non-Error object whose message is a revoked Proxy answers an unverified error status with a constant reason', async () => {
+    h.toThrow = { message: revoked() };
+    expect(await answer()).toEqual(LOOKUP_UNREADABLE);
+    expect(logged(h.error, 'Error verifying transaction')).toEqual(UNREADABLE);
+  });
+});
```
