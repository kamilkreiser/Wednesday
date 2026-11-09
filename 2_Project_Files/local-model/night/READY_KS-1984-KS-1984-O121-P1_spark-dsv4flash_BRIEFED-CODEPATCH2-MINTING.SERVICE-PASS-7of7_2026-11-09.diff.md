# READY — KS-1984-KS-1984-O121-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1984_o121_p1_nft_certificate_reads_back_a_jsonb_public_fields_array/out.md.checker/patch.diff`** (from `ls` at 22:41 2026-11-09; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1984_o121_p1_nft_certificate_reads_back_a_jsonb_public_fields_array/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1984_o121_p1_nft_certificate_reads_back_a_jsonb_public_fields_array/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1984_o121_p1_nft_certificate_reads_back_a_jsonb_public_fields_array/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1984_o121_p1_nft_certificate_reads_back_a_jsonb_public_fields_array-control-r2/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 22:41 2026-11-09 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1984_o121_p1_nft_certificate_reads_back_a_jsonb_public_fields_array/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d0b4825cc24493213f82b609670a4a0fa521a4b9`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts } + { Blockchain/Dev/services/nft-certificate/src/__tests__/ks1984-nft-certificate-reads-back-a-jsonb-public-fields-array.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts` (product) and `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1984-nft-certificate-reads-back-a-jsonb-public-fields-array.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
4	4	Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts
114	0	Blockchain/Dev/services/nft-certificate/src/__tests__/ks1984-nft-certificate-reads-back-a-jsonb-public-fields-array.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (4 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: minting.service.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts`; test(s): `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1984-nft-certificate-reads-back-a-jsonb-public-fields-array.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts 4 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/nft-certificate/src/__tests__/ks1984-nft-certificate-reads-back-a-jsonb-public-fields-array.test.ts 114 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts` (hunks=4, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1984-nft-certificate-reads-back-a-jsonb-public-fields-array.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=5 of total=7; red cell(s): ['KS-1984 a stored certificate is read back when public_fields arrives as a parsed JSONB array RED ks1984 R1 getNFTCertificate reads back a row whose public_fields is an array', 'KS-1984 a stored certificate is read back when public_fields arrives as a parsed JSONB array RED ks1984 R2 getNFTCertificate reads back a row whose public_fields is an empty array (the column default)', 'KS-1984 a stored certificate is read back when public_fields arrives as a parsed JSONB array RED ks1984 R3 getUserNFTCertificates lists a row whose public_fields is an array', 'KS-1984 a stored certificate is read back when public_fields arrives as a parsed JSONB array RED ks1984 R4 getWalletNFTCertificates lists a row whose public_fields is an array', 'KS-1984 a stored certificate is read back when public_fields arrives as a parsed JSONB array RED ks1984 R5 loadFromDb loads a row whose public_fields is an array into memory']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=241 failed=1 | after: total=248 failed=0` · `NEW reds: []` [baseline_suite.json total=241 failed=1; after_suite.json total=248 failed=0]
- A6 [verbatim]: `PASS A6 whole services/nft-certificate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/nft-certificate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts` (+4/-4 per numstat.out) and the test file `Blockchain/Dev/services/nft-certificate/src/__tests__/ks1984-nft-certificate-reads-back-a-jsonb-public-fields-array.test.ts` (+114/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d0b4825cc24493213f82b609670a4a0fa521a4b9` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1984_o121_p1_nft_certificate_reads_back_a_jsonb_public_fields_array/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1984_o121_p1_nft_certificate_reads_back_a_jsonb_public_fields_array/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts b/Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts
--- a/Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts
+++ b/Blockchain/Dev/services/nft-certificate/src/services/minting.service.ts
@@ -120,7 +120,7 @@
         policyId: row.policy_id || undefined, assetName: row.asset_name || undefined,
         assetId: row.asset_id || undefined, transactionHash: row.transaction_hash || undefined,
         storageTier: row.storage_tier as StorageTier, privacyLevel: row.privacy_level as PrivacyLevel,
-        publicFields: JSON.parse(row.public_fields || '[]'), status: row.status as NFTStatus,
+        publicFields: Array.isArray(row.public_fields) ? row.public_fields : JSON.parse(row.public_fields || '[]'), status: row.status as NFTStatus,
         ipfsCid: row.ipfs_cid || undefined, encryptedKey: row.encrypted_key || undefined,
         mintingCost: row.minting_cost != null ? String(row.minting_cost) : undefined,
         platformFee: row.platform_fee != null ? String(row.platform_fee) : undefined,
@@ -502,7 +502,7 @@
             transactionHash: row.transaction_hash || undefined,
             storageTier: row.storage_tier as StorageTier,
             privacyLevel: row.privacy_level as PrivacyLevel,
-            publicFields: JSON.parse(row.public_fields || '[]'),
+            publicFields: Array.isArray(row.public_fields) ? row.public_fields : JSON.parse(row.public_fields || '[]'), // KS-1984: a JSONB column arrives already parsed
             status: row.status as NFTStatus,
             ipfsCid: row.ipfs_cid || undefined,
             encryptedKey: row.encrypted_key || undefined,
@@ -589,7 +589,7 @@
             transactionHash: row.transaction_hash || undefined,
             storageTier: row.storage_tier as StorageTier,
             privacyLevel: row.privacy_level as PrivacyLevel,
-            publicFields: JSON.parse(row.public_fields || '[]'),
+            publicFields: Array.isArray(row.public_fields) ? row.public_fields : JSON.parse(row.public_fields || '[]'), // KS-1984: a JSONB column arrives already parsed
             status: row.status as NFTStatus,
             ipfsCid: row.ipfs_cid || undefined,
             encryptedKey: row.encrypted_key || undefined,
@@ -675,7 +675,7 @@
             transactionHash: row.transaction_hash || undefined,
             storageTier: row.storage_tier as StorageTier,
             privacyLevel: row.privacy_level as PrivacyLevel,
-            publicFields: JSON.parse(row.public_fields || '[]'),
+            publicFields: Array.isArray(row.public_fields) ? row.public_fields : JSON.parse(row.public_fields || '[]'), // KS-1984: a JSONB column arrives already parsed
             status: row.status as NFTStatus,
             ipfsCid: row.ipfs_cid || undefined,
             encryptedKey: row.encrypted_key || undefined,
diff --git a/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1984-nft-certificate-reads-back-a-jsonb-public-fields-array.test.ts b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1984-nft-certificate-reads-back-a-jsonb-public-fields-array.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/nft-certificate/src/__tests__/ks1984-nft-certificate-reads-back-a-jsonb-public-fields-array.test.ts
@@ -0,0 +1,114 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1984: svc_nft_certificates.public_fields is a JSONB column, so the Postgres driver hands the service an
+// already-parsed array. Every read site ran JSON.parse on it, which throws on an array, so a stored certificate
+// could not be read back (the catch logged 'DB get ... failed' and the service answered null or an empty list,
+// and loadFromDb stopped at the first row). These cells feed the real service rows shaped the way the driver
+// returns them. The db stand-in is a plain function over a hoisted row list.
+const h = vi.hoisted(() => ({
+  rows: [] as Array<Record<string, unknown>>,
+  fail: false,
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: () => (h.fail ? Promise.reject(new Error('db down')) : Promise.resolve({ rows: h.rows })),
+}));
+
+vi.mock('../cardano', () => ({
+  isCardanoNFTReady: () => false,
+  mintNFTOnChain: vi.fn(),
+  getPolicyId: () => null,
+  waitForNFTConfirmation: vi.fn(),
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: { info: vi.fn(), warn: vi.fn(), error: vi.fn(), debug: vi.fn() },
+}));
+
+import { loadFromDb, nftMintingService } from '../services/minting.service';
+
+const row = (id: string, userId: string, wallet: string, publicFields: unknown): Record<string, unknown> => ({
+  id,
+  certification_id: `cert-${id}`,
+  user_id: userId,
+  chain: 'cardano',
+  wallet_address: wallet,
+  policy_id: null,
+  asset_name: null,
+  asset_id: null,
+  transaction_hash: null,
+  storage_tier: 'ipfs',
+  privacy_level: 'public',
+  public_fields: publicFields,
+  status: 'minted',
+  ipfs_cid: null,
+  encrypted_key: null,
+  minting_cost: null,
+  platform_fee: null,
+  total_cost: null,
+  error_message: null,
+  created_at: new Date('2026-11-01T00:00:00Z'),
+  updated_at: new Date('2026-11-01T00:00:00Z'),
+  minted_at: null,
+});
+
+const FIELDS = ['certificateId', 'documentHash'];
+
+describe('KS-1984 a stored certificate is read back when public_fields arrives as a parsed JSONB array', () => {
+  beforeEach(() => {
+    h.rows = [];
+    h.fail = false;
+  });
+
+  it('control ks1984 C1 a row whose public_fields is NULL reads back with an empty list', async () => {
+    h.rows = [row('ks1984-c1', 'ks1984-u-c1', 'addr-c1', null)];
+    const cert = await nftMintingService.getNFTCertificate('ks1984-c1');
+    expect(cert).not.toBeNull();
+    expect(cert!.publicFields).toEqual([]);
+  });
+
+  it('control ks1984 C2 a row whose public_fields is JSON text still reads back as the list it holds', async () => {
+    h.rows = [row('ks1984-c2', 'ks1984-u-c2', 'addr-c2', JSON.stringify(FIELDS))];
+    const cert = await nftMintingService.getNFTCertificate('ks1984-c2');
+    expect(cert).not.toBeNull();
+    expect(cert!.publicFields).toEqual(FIELDS);
+  });
+
+  it('RED ks1984 R1 getNFTCertificate reads back a row whose public_fields is an array', async () => {
+    h.rows = [row('ks1984-r1', 'ks1984-u-r1', 'addr-r1', FIELDS)];
+    const cert = await nftMintingService.getNFTCertificate('ks1984-r1');
+    expect(cert).not.toBeNull();
+    expect(cert!.publicFields).toEqual(FIELDS);
+  });
+
+  it('RED ks1984 R2 getNFTCertificate reads back a row whose public_fields is an empty array (the column default)', async () => {
+    h.rows = [row('ks1984-r2', 'ks1984-u-r2', 'addr-r2', [])];
+    const cert = await nftMintingService.getNFTCertificate('ks1984-r2');
+    expect(cert).not.toBeNull();
+    expect(cert!.publicFields).toEqual([]);
+  });
+
+  it('RED ks1984 R3 getUserNFTCertificates lists a row whose public_fields is an array', async () => {
+    h.rows = [row('ks1984-r3', 'ks1984-u-r3', 'addr-r3', FIELDS)];
+    const list = await nftMintingService.getUserNFTCertificates('ks1984-u-r3');
+    expect(list).toHaveLength(1);
+    expect(list[0].publicFields).toEqual(FIELDS);
+  });
+
+  it('RED ks1984 R4 getWalletNFTCertificates lists a row whose public_fields is an array', async () => {
+    h.rows = [row('ks1984-r4', 'ks1984-u-r4', 'addr-r4', FIELDS)];
+    const list = await nftMintingService.getWalletNFTCertificates('addr-r4');
+    expect(list).toHaveLength(1);
+    expect(list[0].publicFields).toEqual(FIELDS);
+  });
+
+  it('RED ks1984 R5 loadFromDb loads a row whose public_fields is an array into memory', async () => {
+    h.rows = [row('ks1984-r5', 'ks1984-u-r5', 'addr-r5', FIELDS)];
+    await loadFromDb();
+    h.fail = true;
+    const cert = await nftMintingService.getNFTCertificate('ks1984-r5');
+    expect(cert).not.toBeNull();
+    expect(cert!.publicFields).toEqual(FIELDS);
+  });
+});
```
