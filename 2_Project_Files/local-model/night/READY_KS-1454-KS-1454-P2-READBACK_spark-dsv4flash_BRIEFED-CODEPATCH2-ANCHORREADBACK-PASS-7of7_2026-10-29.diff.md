# READY — KS-1454-KS-1454-P2-READBACK (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p2_readback/out.md.checker/patch.diff`** (from `ls` at 21:33 2026-10-29; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p2_readback/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p2_readback/out.md.checker/section_2.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p2_readback/out.md.checker/section_3.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 21:33 2026-10-29 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p2_readback/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `6d41673e0f79c0f02c2ec7b893cc960b6fa3ec10`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/anchoring/src/anchorReadback.ts , Blockchain/Dev/services/anchoring/src/index.ts } + { Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/anchorReadback.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts` (test) — equal to numstat.out's set (3 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
12	0	Blockchain/Dev/services/anchoring/src/anchorReadback.ts
3	1	Blockchain/Dev/services/anchoring/src/index.ts
81	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: anchorReadback.ts index.ts`
- CODE_PATCH2 (rung 3, 2 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/anchoring/src/anchorReadback.ts`, `Blockchain/Dev/services/anchoring/src/index.ts`; test(s): `Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/anchoring/src/anchorReadback.ts 12 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/index.ts 3 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts 81 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=3 measured=3 ok=3 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=3 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/anchorReadback.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/index.ts` (hunks=2, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- section 3 `section_3.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts` (hunks=1, miscount=0; applied file per `section_3.opts`: `section_3.diff`, git-apply options: `(none — strict)`; `apply_check_strict_3.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=5 of total=9; red cell(s): ['KS-1454: the anchored signatureHash is read back RED KS-1454 B1: anchorSignatureHashView returns the anchored hash from a logical (DB-form) payload', 'KS-1454: the anchored signatureHash is read back RED KS-1454 B2: anchorSignatureHashView returns the same hash from a payload that went through the chain codec', 'KS-1454: the anchored signatureHash is read back RED KS-1454 B3: GET /api/anchors/verify/:hash (db source) carries the hash under metadata.signatureHash beside documentType', 'KS-1454: the anchored signatureHash is read back RED KS-1454 B4: GET /api/anchors/verify/:hash (chain source) carries the same hash', 'KS-1454: the anchored signatureHash is read back RED KS-1454 B5: the GET /api/anchors/:id handler imports anchorSignatureHashView and spreads it over the row metadata_payload secuura block']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 2 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=456 failed=1 | after: total=465 failed=1` · `NEW reds: []` [baseline_suite.json total=456 failed=1; after_suite.json total=465 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=3 products=2 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/anchorReadback.ts` (+12/-0 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts` (+81/-0); 3 files in all (code_patch2: products Blockchain/Dev/services/anchoring/src/anchorReadback.ts, Blockchain/Dev/services/anchoring/src/index.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict); section 3 `section_3.diff`: `git apply -p1` (strict) — at the tip `6d41673e0f79c0f02c2ec7b893cc960b6fa3ec10` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p2_readback/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p2_readback/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/anchorReadback.ts b/Blockchain/Dev/services/anchoring/src/anchorReadback.ts
--- a/Blockchain/Dev/services/anchoring/src/anchorReadback.ts
+++ b/Blockchain/Dev/services/anchoring/src/anchorReadback.ts
@@ -52,4 +52,14 @@
     identityCommitment: typeof sec.identityCommitment === 'string' ? sec.identityCommitment : null,
     identity: Object.keys(identity).length > 0 ? identity : null,
   };
+}
+
+/**
+ * KS-1454: the plain SHA-256 of Platform-S's detached .p7s, as anchored beside documentType on a `sign` anchor. A string under
+ * `secuura.signatureHash` is read back verbatim (a 64-char lowercase-hex value is never chunked on chain); anything else, or no key at all
+ * (every anchor that predates the field), reads `null`. Same source-agnostic read as anchorIdentityView: DB (logical) or chain payload.
+ */
+export function anchorSignatureHashView(secuura: unknown): { signatureHash: string | null } {
+  const sec = (secuura && typeof secuura === 'object' ? secuura : {}) as Record<string, unknown>;
+  return { signatureHash: typeof sec.signatureHash === 'string' ? sec.signatureHash : null };
 }
@@ -157,6 +167,8 @@
       // KS-1175: the seven non-PII identity fields that were anchored beside it
       // (object, or null for an anchor that predates the field), typed.
       identity: identityView.identity,
+      // KS-1454: the SHA-256 of the detached .p7s anchored with a `sign` event (null for every other anchor), so a verifier can compare it.
+      signatureHash: anchorSignatureHashView(sec).signatureHash,
     },
   };
 }
diff --git a/Blockchain/Dev/services/anchoring/src/index.ts b/Blockchain/Dev/services/anchoring/src/index.ts
--- a/Blockchain/Dev/services/anchoring/src/index.ts
+++ b/Blockchain/Dev/services/anchoring/src/index.ts
@@ -42,7 +42,7 @@
 // booting this service (this module calls app.listen on import).
 import { anchorDocumentSchema, buildFlatAnchorMetadataPayload } from './anchorSchema';
 // KS-1175: the read-back surfaces as pure modules (verify-by-hash body; the GET /:id identity view).
-import { anchorIdentityView, buildVerifyResponse } from './anchorReadback';
+import { anchorIdentityView, anchorSignatureHashView, buildVerifyResponse } from './anchorReadback';
 // KS-1284: the chain read must undo the tx-build codec (long strings arrive as arrays, booleans as strings).
 import { fromCardanoMetadatum } from './cardano/cardanoMetadatum';
 // KS-445: thread-mint request contract + mint-failure classifier — extracted
@@ -956,6 +956,8 @@
     // identityCommitment (KS-721) and the seven non-PII identity fields, from the row's metadata_payload (logical
     // form). null / null for an anchor that predates the fields. This route returned neither before KS-1175.
     ...anchorIdentityView((anchor.metadataPayload as any)?.secuura),
+    // KS-1454: the SHA-256 of the detached .p7s anchored with a `sign` event (S's "signature anchored" check); null for any other anchor.
+    ...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),
     // KS-535: surfaced so originate's poller/reconciler can record WHY a
     // terminal failure happened on the document (KS-520 `error` field), and
     // for operator diagnostics. `failed` is terminal (see processAnchor —
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-read-back-on-the-verify-and-by-id-reads.test.ts
@@ -0,0 +1,81 @@
+// KS-1454 (anchoring read-back): S shows "signature anchored" from GET /api/anchors/:id and a verifier compares the hash from GET /api/anchors/verify/:hash. Before this change neither read returned the
+// anchored `secuura.signatureHash`, so a hash that is on the ledger could not be read back. After it: anchorSignatureHashView reads the string (DB form or chain form), buildVerifyResponse carries it under
+// metadata.signatureHash, and the by-id handler spreads the view into its res.json (index.ts is bootless, so that last point is a source-text guard, as in ks1175-getid-view-wired).
+import { describe, it, expect } from 'vitest';
+import { readFileSync } from 'fs';
+import { resolve } from 'path';
+
+import * as RB from '../anchorReadback';
+import { toCardanoMetadatum, fromCardanoMetadatum } from '../cardano/cardanoMetadatum';
+
+const HASH = 'a1b2c3d4e5f60718293a4b5c6d7e8f901a2b3c4d5e6f70819203a4b5c6d7e8f9';
+const SIG = 'd'.repeat(32) + '0123456789abcdef0123456789abcdef';
+const COMMITMENT = 'identity-commitment-l2.v1:' + 'b'.repeat(64);
+const SIGNED = {
+  secuura: {
+    version: '2.0', type: 'document', hash: HASH, algorithm: 'sha256',
+    documentId: 'doc-1777346021120-1e528170', certId: 'doc-1777346021120-1e528170',
+    timestamp: '2026-10-29T12:00:00.000Z', network: 'preview', documentType: 'sign', signatureHash: SIG,
+    identityCommitment: COMMITMENT,
+  },
+};
+const PLAIN = { secuura: { ...SIGNED.secuura, documentType: 'upload', signatureHash: undefined } };
+const CTX = { hash: HASH, network: 'preview' };
+const ROW = {
+  transaction_hash: 'f'.repeat(64), block_number: 4242, confirmed_at: '2026-10-29T12:01:00.000Z',
+  created_at: '2026-10-29T12:00:00.000Z', document_id: 'doc-1777346021120-1e528170', status: 'confirmed',
+};
+const SRC = readFileSync(resolve(__dirname, '..', 'index.ts'), 'utf8');
+const FROM = SRC.indexOf("app.get('/api/anchors/:id',");
+const END_LINE = 'retryCount: anchor.retryCount ?? 0,';
+const GET_BY_ID = FROM < 0 ? '' : SRC.slice(FROM, SRC.indexOf(END_LINE, FROM) + END_LINE.length);
+
+describe('KS-1454: the anchored signatureHash is read back', () => {
+  it('RED KS-1454 B1: anchorSignatureHashView returns the anchored hash from a logical (DB-form) payload', () => {
+    expect(RB.anchorSignatureHashView?.(SIGNED.secuura)).toEqual({ signatureHash: SIG });
+  });
+
+  it('RED KS-1454 B2: anchorSignatureHashView returns the same hash from a payload that went through the chain codec', () => {
+    const chainForm = fromCardanoMetadatum(toCardanoMetadatum(SIGNED)) as typeof SIGNED;
+    expect(typeof chainForm.secuura.signatureHash).toBe('string');
+    expect(RB.anchorSignatureHashView?.(chainForm.secuura)).toEqual({ signatureHash: SIG });
+  });
+
+  it('RED KS-1454 B3: GET /api/anchors/verify/:hash (db source) carries the hash under metadata.signatureHash beside documentType', () => {
+    const body = RB.buildVerifyResponse('db', SIGNED, ROW, CTX) as any;
+    expect(body.metadata.signatureHash).toBe(SIG);
+    expect(body.metadata.documentType).toBe('sign');
+  });
+
+  it('RED KS-1454 B4: GET /api/anchors/verify/:hash (chain source) carries the same hash', () => {
+    const onChain = { secuura: (fromCardanoMetadatum(toCardanoMetadatum(SIGNED)) as typeof SIGNED).secuura, txHash: 'e'.repeat(64) };
+    const body = RB.buildVerifyResponse('chain', onChain, undefined, CTX) as any;
+    expect(body.metadata.signatureHash).toBe(SIG);
+  });
+
+  it('RED KS-1454 B5: the GET /api/anchors/:id handler imports anchorSignatureHashView and spreads it over the row metadata_payload secuura block', () => {
+    expect(SRC.includes("import { anchorIdentityView, anchorSignatureHashView, buildVerifyResponse } from './anchorReadback';")).toBe(true);
+    expect(GET_BY_ID.includes('...anchorSignatureHashView((anchor.metadataPayload as any)?.secuura),')).toBe(true);
+  });
+
+  it('control KS-1454 C1: an anchor with no signatureHash reads null (the key is never invented), on both reads', () => {
+    expect(RB.anchorSignatureHashView?.(PLAIN.secuura) ?? { signatureHash: null }).toEqual({ signatureHash: null });
+    expect((RB.buildVerifyResponse('db', PLAIN, ROW, CTX) as any).metadata.signatureHash ?? null).toBeNull();
+  });
+
+  it('control KS-1454 C2: a value that is not a string (a number, an array, an object) is not surfaced as a hash', () => {
+    for (const bad of [12345, [SIG], { h: SIG }, null]) {
+      expect(RB.anchorSignatureHashView?.({ ...SIGNED.secuura, signatureHash: bad }) ?? { signatureHash: null }).toEqual({ signatureHash: null });
+    }
+    expect(RB.anchorSignatureHashView?.(undefined) ?? { signatureHash: null }).toEqual({ signatureHash: null });
+  });
+
+  it('control KS-1454 C3: the identity read-back is unchanged by a signatureHash beside it', () => {
+    expect(RB.anchorIdentityView(SIGNED.secuura)).toEqual({ identityCommitment: COMMITMENT, identity: null });
+    expect((RB.buildVerifyResponse('db', SIGNED, ROW, CTX) as any).metadata.identityCommitment).toBe(COMMITMENT);
+  });
+
+  it('control KS-1454 C4: the block located in index.ts is ONE handler, the anchor-by-id route (contentHash and the KS-535 errorMessage are in it)', () => {
+    expect([GET_BY_ID.split('app.get(').length, GET_BY_ID.includes('contentHash: anchor.contentHash,'), GET_BY_ID.includes('errorMessage: anchor.errorMessage || null,')]).toEqual([2, true, true]);
+  });
+});
```
