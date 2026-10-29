# READY — KS-1836-KS-1836 (Spark (DeepSeek V4 Flash), briefed, test_only (code_patch checker, MODE=test_only), vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1836_p3_wallet_selector_exact-r2/out.md.checker/patch.diff`** (from `ls` at 10:38 2026-10-30; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1836_p3_wallet_selector_exact-r2/out.md.checker/section_1.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 10:38 2026-10-30 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1836_p3_wallet_selector_exact-r2/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `a786e06e6f6ec66245a0d0d6d36959e247f7c989`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (test-only) touched-file set == { Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-read-gate-wallet-selector-compares-exactly.test.ts } — the product file is untouched, as the ticket requires`
- Declared set [input.json suggested_test_file; product_file = the TAMPER TARGET, not modified]: `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-read-gate-wallet-selector-compares-exactly.test.ts` (test) — equal to numstat.out's set (1 file); `Blockchain/Dev/services/nft-certificate/src/services/nftReadGate.ts` (product) untouched, measured above.
- numstat [out.md.checker/numstat.out, verbatim]:
```
38	0	Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-read-gate-wallet-selector-compares-exactly.test.ts
```
- Test hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (30 line(s)), and no tip line is re-added as a '+' (A3d)` — test section `+` lines 38 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-read-gate-wallet-selector-compares-exactly.test.ts byte-exact incl. leading whitespace (apply mode strict): OK 30 line(s) byte-exact incl. leading whitespace (of 30; 39 line(s) added by the apply)` [a3i_indent.out: `OK 30 line(s) byte-exact incl. leading whitespace (of 30; 39 line(s) added by the apply)`]
- **TEST-ONLY (code_patch checker MODE=test_only)** — the product `Blockchain/Dev/services/nft-certificate/src/services/nftReadGate.ts` is the TAMPER TARGET and is BYTE-UNCHANGED: the run's `patch.diff` re-applied strictly (`git apply -p1`, scratch tempdir) to the tip content in input.json['files'] leaves it sha256 `68ebcfa1df851202` = the tip's; numstat.out does not list it; no section names it. [checker.out mode line, verbatim]: `mode: test_only (tamper at Blockchain/Dev/services/nft-certificate/src/services/nftReadGate.ts:91)` · [tamper.out, verbatim]: `tampered /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/spark/cache/work/spark_secuura_2026-10-30_ks_1836_p3_wallet_selector_exact-r2_102634/clone/Blockchain/Dev/services/nft-certificate/src/services/nftReadGate.ts:91: '    if (selectors.walletAddress !== undefined && cert.walletAddress !== selectors.walletAddress) return false;' -> '    if (selectors.walletAddress !== undefined && cert.walletAddress.trim() !== String(selectors.walletAddress).trim()) return false;'` · [checker.out, verbatim]: `A4 (test-only): tamper reverted (Blockchain/Dev/services/nft-certificate/src/services/nftReadGate.ts back to the tip)` (tamper_revert.out EMPTY) · the tamper's `from` equals the product's tip line 91. [apply_product.out, verbatim]: `A5 (test-only): no product hunk — the test must be GREEN at the untouched tip`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=1 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-read-gate-wallet-selector-compares-exactly.test.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1836-read-gate-wallet-selector-compares-exactly.test.ts fails at the untouched tip (2 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=2 of total=5; red cell(s): ['KS-1836 read gate: the walletAddress selector compares exactly RED KS-1836 W1 a selector padded with spaces does not match the unpadded row wallet', 'KS-1836 read gate: the walletAddress selector compares exactly RED KS-1836 W2 a row wallet padded with spaces is not matched by the unpadded selector']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1836-read-gate-wallet-selector-compares-exactly.test.ts passes with the product hunk (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=107 failed=0 | after: total=112 failed=0` · `NEW reds: []` [baseline_suite.json total=107 failed=0; after_suite.json total=112 failed=0]
- A6 [verbatim]: `PASS A6 whole services/nft-certificate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/nft-certificate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=1 +38/-0 test=src/__tests__/ks1836-read-gate-wallet-selector-compares-exactly.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** TEST-ONLY — ZERO PRODUCT BYTES: one file, the test `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-read-gate-wallet-selector-compares-exactly.test.ts` (+38/-0 per numstat.out); the product `Blockchain/Dev/services/nft-certificate/src/services/nftReadGate.ts` is the tamper target and is byte-unchanged (sha256 68ebcfa1df851202, measured). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict) — at the tip `a786e06e6f6ec66245a0d0d6d36959e247f7c989` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: the gate decides (test file only). Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1836_p3_wallet_selector_exact-r2/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-30_ks_1836_p3_wallet_selector_exact-r2/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-read-gate-wallet-selector-compares-exactly.test.ts b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-read-gate-wallet-selector-compares-exactly.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1836-read-gate-wallet-selector-compares-exactly.test.ts
@@ -0,0 +1,38 @@
+// KS-1836 (gate 23 mutant Mf): selectReadableCertificates (services/nftReadGate.ts) documents that the `walletAddress` selector "must
+// equal the row's wallet". The comparison is exact: a wallet address is an opaque string, so a selector or a row value that differs
+// only by surrounding whitespace is a DIFFERENT wallet and matches nothing. The PR's own cells use well-formed wallets only, so a
+// compare that trims both sides stayed green. Unit level: the pure function, no router, no database.
+import { describe, it, expect } from 'vitest';
+import { selectReadableCertificates } from '../services/nftReadGate';
+import type { NFTCertificate } from '../types';
+
+const OWNER = 'user-A';
+const WALLET = 'addr_test1_ks1836_exact_wallet';
+
+function cert(id: string, walletAddress: string): NFTCertificate {
+  return { id, userId: OWNER, walletAddress } as unknown as NFTCertificate;
+}
+
+const ids = (list: readonly NFTCertificate[]) => list.map(c => c.id);
+
+describe('KS-1836 read gate: the walletAddress selector compares exactly', () => {
+  it('RED KS-1836 W1 a selector padded with spaces does not match the unpadded row wallet', () => {
+    expect(ids(selectReadableCertificates([cert('c1', WALLET)], OWNER, { walletAddress: ` ${WALLET} ` }))).toEqual([]);
+  });
+
+  it('RED KS-1836 W2 a row wallet padded with spaces is not matched by the unpadded selector', () => {
+    expect(ids(selectReadableCertificates([cert('c1', ` ${WALLET}`)], OWNER, { walletAddress: WALLET }))).toEqual([]);
+  });
+
+  it('CONTROL KS-1836 W3 the exact selector returns the row', () => {
+    expect(ids(selectReadableCertificates([cert('c1', WALLET)], OWNER, { walletAddress: WALLET }))).toEqual(['c1']);
+  });
+
+  it('CONTROL KS-1836 W4 a different wallet returns nothing', () => {
+    expect(ids(selectReadableCertificates([cert('c1', WALLET)], OWNER, { walletAddress: `${WALLET}_other` }))).toEqual([]);
+  });
+
+  it('CONTROL KS-1836 W5 no walletAddress selector returns every row the owner holds', () => {
+    expect(ids(selectReadableCertificates([cert('c1', WALLET), cert('c2', 'addr_other')], OWNER, {}))).toEqual(['c1', 'c2']);
+  });
+});
```
