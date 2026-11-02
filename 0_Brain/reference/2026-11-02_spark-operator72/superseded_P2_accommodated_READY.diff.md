# READY — KS-1868-KS-1868-O72-P2 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p2_nft_blockchain_verifier_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 11:29 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p2_nft_blockchain_verifier_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p2_nft_blockchain_verifier_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip — with an accommodation: [section 1: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts b/Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts' vs '+++ --- a/Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts' — the model paired the product file's --- with another file's +++ (task.md 2d)] [Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts: FUZZY — applies only with -C1 (one context line): ; strict rc=1 lenient rc=1] [section 2: MISMATCHED HEADER '--- diff --git a/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-unreadable-throw.test.ts b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-unreadable-throw.test.ts' vs '+++ new file mode 100644' — the model paired the product file's --- with another file's +++ (task.md 2d)]` — STRICT APPLY NOT CLAIMED: section 1 (Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts): `error: patch failed: Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts:101` (apply with the options recorded in section_<k>.opts; the raise seat states which); the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p2_nft_blockchain_verifier_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p2_nft_blockchain_verifier_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 11:29 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p2_nft_blockchain_verifier_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8aded39571d0d26dc5cd3632948803cd95c4680c`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts } + { Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts` (product) and `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
27	4	Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts
126	0	Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (27 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: blockchain-verifier.service.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts`; test(s): `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts 27 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-unreadable-throw.test.ts 126 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `--recount --ignore-whitespace -C1`; `apply_check_strict_1.out`: NON-EMPTY: `error: patch failed: Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts:101`)
- section 2 `section_2.diff` → `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=4 of total=7; red cell(s): ['KS-1868 `BlockchainVerifierService` reads the thrown value safely RED ks1868 R1 init: a revoked Proxy thrown value logs a constant reason and verification stays pending', 'KS-1868 `BlockchainVerifierService` reads the thrown value safely RED ks1868 R2 init: an Error whose message getter throws logs a constant reason and verification stays pending', 'KS-1868 `BlockchainVerifierService` reads the thrown value safely RED ks1868 R3 lookup: a revoked Proxy thrown value logs a constant reason and answers an unverified error status', 'KS-1868 `BlockchainVerifierService` reads the thrown value safely RED ks1868 R4 lookup: an Error whose message getter throws logs a constant reason and answers an unverified error status']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=162 failed=0 | after: total=169 failed=0` · `NEW reds: []` [baseline_suite.json total=162 failed=0; after_suite.json total=169 failed=0]
- A6 [verbatim]: `PASS A6 whole services/nft-certificate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/nft-certificate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=accommodated (see the A2 line)`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts` (+27/-4 per numstat.out) and the test file `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-unreadable-throw.test.ts` (+126/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1 --recount --ignore-whitespace -C1`; section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8aded39571d0d26dc5cd3632948803cd95c4680c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p2_nft_blockchain_verifier_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o72_p2_nft_blockchain_verifier_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p2_nft_blockchain_verifier_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts b/Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts
--- a/Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts
+++ b/Blockchain/Dev/services/nft-certificate/src/services/blockchain-verifier.service.ts
@@ -66,6 +66,12 @@
       // A malformed key or unsupported network must degrade to
       // "verification disabled", never escape as a 500.
+      let reason: string;
+      try {
+        reason = err instanceof Error ? err.message : String(err);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
       logger.warn('Blockfrost client init failed – on-chain verification disabled', {
-        error: err instanceof Error ? err.message : String(err),
+        error: reason,
       });
       return null;
@@ -101,3 +107,8 @@
     } catch (err: unknown) {
       // Blockfrost returns 404 for transactions not yet on-chain
-      const statusCode = (err as { status_code?: number }).status_code;
+      let statusCode: number | undefined;
+      try {
+        statusCode = (err as { status_code?: number }).status_code;
+      } catch {
+        statusCode = undefined;
+      }
@@ -109,7 +120,19 @@
-      logger.error('Error verifying transaction', { error: err instanceof Error ? err.message : String(err) });
+      let reason: string;
+      try {
+        reason = err instanceof Error ? err.message : String(err);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Error verifying transaction', { error: reason });
+      let errorText: string;
+      try {
+        errorText = (err as Error).message ?? 'Unknown error';
+      } catch {
+        errorText = 'unreadable thrown value';
+      }
       return {
         verified: false,
         status: 'error',
-        error: (err as Error).message ?? 'Unknown error',
+        error: errorText,
       };
     }
diff --git a/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-unreadable-throw.test.ts b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-blockchain-verifier-unreadable-throw.test.ts
@@ -0,0 +1,126 @@
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+
+// KS-1868: `BlockchainVerifierService` must still answer when the thrown value itself cannot be read (a revoked
+// Proxy throws on any property read; an Error whose `message` getter throws, throws on `.message`).
+// Two catch blocks: the Blockfrost client construction in `getClient` (answers "verification disabled", i.e. a
+// pending verification) and the transaction lookup in `verifyTransaction` (answers an unverified 'error' status).
+// The Blockfrost stand-in is a plain class, not vi.fn(): a spy inspects what it rejects with and could itself
+// fail on a revoked Proxy before the code under test saw it.
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
+const badGetter = () =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+const answer = async (): Promise<unknown> => {
+  try {
+    return { resolved: await new BlockchainVerifierService().verifyTransaction(HASH) };
+  } catch (e) {
+    return { rejected: true };
+  }
+};
+
+const LINES = (fn: { mock: { calls: unknown[][] } }, text: string) => fn.mock.calls.filter((c) => String(c[0]).includes(text));
+
+describe('KS-1868 `BlockchainVerifierService` reads the thrown value safely', () => {
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
+    expect(LINES(h.warn, 'Blockfrost client init failed')).toHaveLength(1);
+    expect(LINES(h.warn, 'Blockfrost client init failed')[0][1]).toEqual({ error: 'bad project id' });
+  });
+
+  it('control ks1868 C2 lookup: an ordinary Error logs its message and answers an unverified error status', async () => {
+    h.toThrow = new Error('upstream 500');
+    expect(await answer()).toEqual({ resolved: { verified: false, status: 'error', error: 'upstream 500' } });
+    expect(LINES(h.error, 'Error verifying transaction')).toHaveLength(1);
+    expect(LINES(h.error, 'Error verifying transaction')[0][1]).toEqual({ error: 'upstream 500' });
+  });
+
+  it('control ks1868 C3 lookup: a 404 from Blockfrost still answers not_found', async () => {
+    h.toThrow = Object.assign(new Error('not found'), { status_code: 404 });
+    expect(await answer()).toEqual({ resolved: { verified: false, status: 'not_found' } });
+    expect(LINES(h.error, 'Error verifying transaction')).toHaveLength(0);
+  });
+
+  it('RED ks1868 R1 init: a revoked Proxy thrown value logs a constant reason and verification stays pending', async () => {
+    h.initThrows = true;
+    h.toThrow = revoked();
+    expect(await answer()).toEqual({ resolved: { verified: false, status: 'pending' } });
+    expect(LINES(h.warn, 'Blockfrost client init failed')).toHaveLength(1);
+    expect(LINES(h.warn, 'Blockfrost client init failed')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 init: an Error whose message getter throws logs a constant reason and verification stays pending', async () => {
+    h.initThrows = true;
+    h.toThrow = badGetter();
+    expect(await answer()).toEqual({ resolved: { verified: false, status: 'pending' } });
+    expect(LINES(h.warn, 'Blockfrost client init failed')).toHaveLength(1);
+    expect(LINES(h.warn, 'Blockfrost client init failed')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 lookup: a revoked Proxy thrown value logs a constant reason and answers an unverified error status', async () => {
+    h.toThrow = revoked();
+    expect(await answer()).toEqual({ resolved: { verified: false, status: 'error', error: 'unreadable thrown value' } });
+    expect(LINES(h.error, 'Error verifying transaction')).toHaveLength(1);
+    expect(LINES(h.error, 'Error verifying transaction')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+
+  it('RED ks1868 R4 lookup: an Error whose message getter throws logs a constant reason and answers an unverified error status', async () => {
+    h.toThrow = badGetter();
+    expect(await answer()).toEqual({ resolved: { verified: false, status: 'error', error: 'unreadable thrown value' } });
+    expect(LINES(h.error, 'Error verifying transaction')).toHaveLength(1);
+    expect(LINES(h.error, 'Error verifying transaction')[0][1]).toEqual({ error: 'unreadable thrown value' });
+  });
+});
```
