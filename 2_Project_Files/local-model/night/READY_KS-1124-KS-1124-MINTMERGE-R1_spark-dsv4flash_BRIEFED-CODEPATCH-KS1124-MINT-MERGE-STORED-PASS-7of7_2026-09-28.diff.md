# READY — KS-1124-KS-1124-MINTMERGE-R1 (spark-dsv4flash, briefed, code_patch, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1124-MINTMERGE-R1/out.md.checker/patch.diff`** (from `ls` at 16:27 2026-09-28; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1124-MINTMERGE-R1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1124-MINTMERGE-R1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1124-MINTMERGE-R1/out.md.checker/patch.diff /private/tmp/claude-501/-Volumes-DevMASTER-WEDNESDAY/4901153c-5db0-4cfc-bf83-c25726202b34/scratchpad/golden_KS-1124-MINTMERGE-R1/out.md.checker/patch.diff` rc 0, Wednesday morning 4901153c).

**Held 16:27 2026-09-28 by Wednesday morning 4901153c after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1124-MINTMERGE-R1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/originate/src/routes/documents.ts , Blockchain/Dev/services/originate/src/__tests__/ks520-anchor-fail-closed.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/routes/documents.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks520-anchor-fail-closed.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
5	2	Blockchain/Dev/services/originate/src/routes/documents.ts
63	0	Blockchain/Dev/services/originate/src/__tests__/ks520-anchor-fail-closed.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (5 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 5 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 2.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/originate/src/routes/documents.ts byte-exact incl. leading whitespace (apply mode strict): OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)` [a3i_indent.out: `OK 5 line(s) byte-exact incl. leading whitespace (of 5; 5 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/routes/documents.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks520-anchor-fail-closed.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks520-anchor-fail-closed.test.ts fails at the untouched tip (1 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=1 of total=6; red cell(s): ['KS-1124 O1: the thread-token cache write merges into the persisted blob RED KS-1124 M1: an anchor accept already persisted keeps its txHash, status and anchorId']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks520-anchor-fail-closed.test.ts passes with the product hunk (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1052 failed=0 | after: total=1055 failed=0` · `NEW reds: []` [baseline_suite.json total=1052 failed=0; after_suite.json total=1055 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +68/-2 test=src/__tests__/ks520-anchor-fail-closed.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/routes/documents.ts` (+5/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks520-anchor-fail-closed.test.ts` (+63/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `d9ce1403d1581ff1584ab799fbbf7fc6f9f8d817` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1124-MINTMERGE-R1/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-09-28_KS-1124-MINTMERGE-R1/checker.out`.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/documents.ts
+++ b/Blockchain/Dev/services/originate/src/routes/documents.ts
@@ -785,7 +785,7 @@
           createdAtMs: Date.now(),
           bearerToken,
         })
-          .then((entry) => {
+          .then(async (entry) => {
             logger.info('thread-token minted at document create', {
               documentId: id,
               policyId: entry.policyId,
@@ -794,9 +794,12 @@
             // Surface the thread-token info on the document record so
             // dashboards can show it without a separate lookup. The
             // canonical truth is state_thread_registry; this is a cache.
+            // KS-1124 O1: merge into the blob as persisted NOW, not the create-time local, so an anchor
+            // write that landed first (txHash, status, anchorId) is not erased by this cache write.
+            const current = await getDocument(id, tenantId).catch(() => null);
             updateDocument(id, tenantId, {
               blockchain: {
-                ...(document.blockchain || {}),
+                ...(current?.blockchain || document.blockchain || {}),
                 threadToken: {
                   policyId: entry.policyId,
                   scriptAddress: entry.scriptAddress,
--- a/Blockchain/Dev/services/originate/src/__tests__/ks520-anchor-fail-closed.test.ts
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks520-anchor-fail-closed.test.ts
@@ -191,2 +191,65 @@
   });
+});
+
+// KS-1124 O1: the thread-token mint callback at document create wrote the create-time local (which has
+// no blockchain key) plus the token, and updateDocument replaces the blockchain column wholesale. So an
+// anchor accept persisted FIRST lost its txHash, status and anchorId. The callback now merges into the
+// blob as persisted at write time. Same harness as above: documentRepo and the thread-token client are
+// this file's own mocks, reached through jest.requireMock.
+const KS1124_TX = 'a'.repeat(64);
+const KS1124_MINTED = { policyId: 'policy-ks1124', scriptAddress: 'addr_test1ks1124', mintTxHash: 'b'.repeat(64), network: 'preprod' };
+const ks1124GetDocument = (jest.requireMock('../repositories/documentRepo') as { getDocument: jest.Mock }).getDocument;
+const ks1124Mint = (jest.requireMock('../services/threadTokenClient') as { mintAndRegisterThreadToken: jest.Mock }).mintAndRegisterThreadToken;
+
+/** Create a document, then wait (bounded) for the fire-and-forget thread-token write and return its blob. */
+async function ks1124ThreadTokenWrite(): Promise<Record<string, any> | undefined> {
+  const res = await fetch(baseUrl + '/api/documents', {
+    method: 'POST',
+    headers: { 'content-type': 'application/json', authorization: 'Bearer t' },
+    body: JSON.stringify({ title: 'ks1124 thread token', type: 'general', data: { note: 'x' } }),
+  });
+  expect(res.status).toBe(201);
+  const deadline = Date.now() + 3000;
+  while (Date.now() < deadline) {
+    const hit = (mockUpdateDocument.mock.calls as unknown[][]).find(
+      (c) => (c[2] as { blockchain?: { threadToken?: { mintTxHash?: string } } }).blockchain?.threadToken?.mintTxHash === KS1124_MINTED.mintTxHash,
+    );
+    if (hit) return (hit[2] as { blockchain: Record<string, any> }).blockchain;
+    await new Promise((r) => setTimeout(r, 25));
+  }
+  return undefined;
+}
+
+describe('KS-1124 O1: the thread-token cache write merges into the persisted blob', () => {
+  beforeEach(() => {
+    process.env.STATE_THREAD_NFT_ENABLED = 'true';
+    ks1124Mint.mockResolvedValue(KS1124_MINTED);
+  });
+  afterEach(() => {
+    delete process.env.STATE_THREAD_NFT_ENABLED;
+  });
+
+  it('RED KS-1124 M1: an anchor accept already persisted keeps its txHash, status and anchorId', async () => {
+    ks1124GetDocument.mockResolvedValue({
+      id: 'doc-ks1124',
+      blockchain: { txHash: KS1124_TX, status: 'submitted', anchorId: 'anchor-ks1124', network: 'preprod' },
+    });
+    const blob = await ks1124ThreadTokenWrite();
+    expect(blob).toBeDefined();
+    expect({ txHash: blob?.txHash, status: blob?.status, anchorId: blob?.anchorId })
+      .toEqual({ txHash: KS1124_TX, status: 'submitted', anchorId: 'anchor-ks1124' });
+  });
+
+  it('control KS-1124 C1: the write carries the minted thread token, field for field', async () => {
+    ks1124GetDocument.mockResolvedValue({ id: 'doc-ks1124', blockchain: { txHash: KS1124_TX, status: 'submitted' } });
+    const blob = await ks1124ThreadTokenWrite();
+    expect(ks1124Mint).toHaveBeenCalledTimes(1);
+    expect(blob?.threadToken).toEqual(KS1124_MINTED);
+  });
+
+  it('control KS-1124 C2: with no persisted row the write carries the thread token and invents no anchor field', async () => {
+    ks1124GetDocument.mockResolvedValue(null);
+    const blob = await ks1124ThreadTokenWrite();
+    expect(Object.keys(blob ?? {})).toEqual(['threadToken']);
+  });
 });
```
