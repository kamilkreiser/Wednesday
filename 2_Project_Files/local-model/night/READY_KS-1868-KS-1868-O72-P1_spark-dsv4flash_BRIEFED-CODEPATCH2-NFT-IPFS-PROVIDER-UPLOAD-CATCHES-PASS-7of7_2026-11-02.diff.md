# READY — KS-1868-KS-1868-O72-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p1_nft_ipfs_provider_upload_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 11:26 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p1_nft_ipfs_provider_upload_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p1_nft_ipfs_provider_upload_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p1_nft_ipfs_provider_upload_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p1_nft_ipfs_provider_upload_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 11:26 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p1_nft_ipfs_provider_upload_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `8aded39571d0d26dc5cd3632948803cd95c4680c`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts } + { Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-ipfs-upload-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts` (product) and `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-ipfs-upload-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
21	3	Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts
115	0	Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-ipfs-upload-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (21 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: ipfs.service.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts`; test(s): `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-ipfs-upload-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts 21 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-ipfs-upload-unreadable-throw.test.ts 115 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-ipfs-upload-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 `IPFSService.upload` reads the thrown value safely RED ks1868 R1 pinata: a revoked Proxy thrown value is reported with a constant reason', 'KS-1868 `IPFSService.upload` reads the thrown value safely RED ks1868 R2 pinata: an Error whose message getter throws is reported with a constant reason', 'KS-1868 `IPFSService.upload` reads the thrown value safely RED ks1868 R3 infura: a revoked Proxy thrown value is reported with a constant reason', 'KS-1868 `IPFSService.upload` reads the thrown value safely RED ks1868 R4 infura: an Error whose message getter throws is reported with a constant reason', 'KS-1868 `IPFSService.upload` reads the thrown value safely RED ks1868 R5 web3storage: a revoked Proxy thrown value is reported with a constant reason', 'KS-1868 `IPFSService.upload` reads the thrown value safely RED ks1868 R6 web3storage: an Error whose message getter throws is reported with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=162 failed=0 | after: total=171 failed=0` · `NEW reds: []` [baseline_suite.json total=162 failed=0; after_suite.json total=171 failed=0]
- A6 [verbatim]: `PASS A6 whole services/nft-certificate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/nft-certificate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts` (+21/-3 per numstat.out) and the test file `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-ipfs-upload-unreadable-throw.test.ts` (+115/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `8aded39571d0d26dc5cd3632948803cd95c4680c` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p1_nft_ipfs_provider_upload_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o72_p1_nft_ipfs_provider_upload_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o72_p1_nft_ipfs_provider_upload_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts b/Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts
--- a/Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts
+++ b/Blockchain/Dev/services/nft-certificate/src/services/ipfs.service.ts
@@ -106,9 +106,15 @@
         pinned: true,
       };
     } catch (error) {
+      let reason: string;
+      try {
+        reason = (error as Error).message;
+      } catch {
+        reason = 'unreadable thrown value';
+      }
       return {
         success: false,
-        error: `Pinata upload error: ${(error as Error).message}`,
+        error: `Pinata upload error: ${reason}`,
       };
     }
   }
@@ -201,6 +207,12 @@
         pinned: true,
       };
     } catch (error) {
-      return { success: false, error: `Infura upload error: ${(error as Error).message}` };
+      let reason: string;
+      try {
+        reason = (error as Error).message;
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      return { success: false, error: `Infura upload error: ${reason}` };
     }
   }
@@ -278,6 +290,12 @@
         pinned: true,
       };
     } catch (error) {
-      return { success: false, error: `Web3.Storage upload error: ${(error as Error).message}` };
+      let reason: string;
+      try {
+        reason = (error as Error).message;
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      return { success: false, error: `Web3.Storage upload error: ${reason}` };
     }
   }
diff --git a/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-ipfs-upload-unreadable-throw.test.ts b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-ipfs-upload-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1868-ipfs-upload-unreadable-throw.test.ts
@@ -0,0 +1,115 @@
+import { describe, it, expect, vi, beforeEach, afterEach } from 'vitest';
+
+// KS-1868: the three provider `upload` methods of `IPFSService` must still answer `{ success: false, error }`
+// (and not reject) when the thrown value itself cannot be read (a revoked Proxy throws on any property read;
+// an Error whose `message` getter throws, throws on `.message`). One catch block per provider: Pinata, Infura,
+// Web3.Storage. The `fetch` stand-in is a plain function, not vi.fn(): a spy inspects what it rejects with and
+// could itself fail on a revoked Proxy before the code under test saw it.
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
+}));
+
+import { IPFSService } from '../services/ipfs.service';
+
+const REQUEST = { data: Buffer.from('ks1868'), filename: 'ks1868.bin', mimeType: 'application/octet-stream' };
+
+const KEYS = { apiKey: 'k', secretKey: 's' };
+
+const pinata = () => new IPFSService('pinata', KEYS);
+const infura = () => new IPFSService('infura', KEYS);
+const web3 = () => new IPFSService('web3storage', { apiKey: 'token-ks1868' });
+
+const answer = async (make: () => IPFSService): Promise<unknown> => {
+  try {
+    return { resolved: await make().upload(REQUEST) };
+  } catch (e) {
+    return { rejected: true };
+  }
+};
+
+const requestRejects = () => vi.stubGlobal('fetch', () => Promise.reject(h.toThrow));
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
+const failed = (text: string) => ({ resolved: { success: false, error: text } });
+
+describe('KS-1868 `IPFSService.upload` reads the thrown value safely', () => {
+  beforeEach(() => {
+    h.toThrow = undefined;
+  });
+
+  afterEach(() => {
+    vi.unstubAllGlobals();
+  });
+
+  it('control ks1868 C1 pinata: an ordinary Error is reported with its own message', async () => {
+    h.toThrow = new Error('connect refused');
+    requestRejects();
+    expect(await answer(pinata)).toEqual(failed('Pinata upload error: connect refused'));
+  });
+
+  it('control ks1868 C2 infura: an ordinary Error is reported with its own message', async () => {
+    h.toThrow = new Error('connect refused');
+    requestRejects();
+    expect(await answer(infura)).toEqual(failed('Infura upload error: connect refused'));
+  });
+
+  it('control ks1868 C3 web3storage: an ordinary Error is reported with its own message', async () => {
+    h.toThrow = new Error('connect refused');
+    requestRejects();
+    expect(await answer(web3)).toEqual(failed('Web3.Storage upload error: connect refused'));
+  });
+
+  it('RED ks1868 R1 pinata: a revoked Proxy thrown value is reported with a constant reason', async () => {
+    h.toThrow = revoked();
+    requestRejects();
+    expect(await answer(pinata)).toEqual(failed('Pinata upload error: unreadable thrown value'));
+  });
+
+  it('RED ks1868 R2 pinata: an Error whose message getter throws is reported with a constant reason', async () => {
+    h.toThrow = badGetter();
+    requestRejects();
+    expect(await answer(pinata)).toEqual(failed('Pinata upload error: unreadable thrown value'));
+  });
+
+  it('RED ks1868 R3 infura: a revoked Proxy thrown value is reported with a constant reason', async () => {
+    h.toThrow = revoked();
+    requestRejects();
+    expect(await answer(infura)).toEqual(failed('Infura upload error: unreadable thrown value'));
+  });
+
+  it('RED ks1868 R4 infura: an Error whose message getter throws is reported with a constant reason', async () => {
+    h.toThrow = badGetter();
+    requestRejects();
+    expect(await answer(infura)).toEqual(failed('Infura upload error: unreadable thrown value'));
+  });
+
+  it('RED ks1868 R5 web3storage: a revoked Proxy thrown value is reported with a constant reason', async () => {
+    h.toThrow = revoked();
+    requestRejects();
+    expect(await answer(web3)).toEqual(failed('Web3.Storage upload error: unreadable thrown value'));
+  });
+
+  it('RED ks1868 R6 web3storage: an Error whose message getter throws is reported with a constant reason', async () => {
+    h.toThrow = badGetter();
+    requestRejects();
+    expect(await answer(web3)).toEqual(failed('Web3.Storage upload error: unreadable thrown value'));
+  });
+});
```
