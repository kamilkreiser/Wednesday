# READY — KS-1454-KS-1454-P1-SIGHASH (Spark (DeepSeek V4 Flash), briefed, code_patch, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p1/out.md.checker/patch.diff`** (from `ls` at 19:22 2026-10-29; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p1/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p1/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden not located — no identity claim is made.

**Held 19:22 2026-10-29 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p1/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `fd84001c738a1bf9071d2d8a5cac6e953ad95789`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 touched-file set == { Blockchain/Dev/services/anchoring/src/anchorSchema.ts , Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` (product) and `Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
12	0	Blockchain/Dev/services/anchoring/src/anchorSchema.ts
80	0	Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the product hunk (12 line(s)), and no tip line is re-added as a '+' (A3d)` — product section `+` lines 12 ordered-equal (whitespace-stripped) to the brief's `expected_plus` (ASCII); `-` lines 0.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: every '+' line the brief adds is in the applied Blockchain/Dev/services/anchoring/src/anchorSchema.ts byte-exact incl. leading whitespace (apply mode strict): OK 12 line(s) byte-exact incl. leading whitespace (of 12; 12 line(s) added by the apply)` [a3i_indent.out: `OK 12 line(s) byte-exact incl. leading whitespace (of 12; 12 line(s) added by the apply)`]
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts fails at the untouched tip (10 failed / 14 run; controls green; assertion reds)` [red_first.json: failed=10 of total=14; red cell(s): ['KS-1454: metadata.signatureHash on the sign verb RED KS-1454 R1: a sign anchor carrying a signatureHash is accepted and the hash is anchored verbatim', 'KS-1454: metadata.signatureHash on the sign verb RED KS-1454 R2: the same hash on an upload anchor is refused, not anchored', 'KS-1454: metadata.signatureHash on the sign verb RED KS-1454 R3: a signatureHash with no documentType is refused', 'KS-1454: metadata.signatureHash on the sign verb RED KS-1454 R4: a malformed signatureHash (uppercase hex) on a sign anchor is refused', 'KS-1454: metadata.signatureHash on the sign verb RED KS-1454 R4: a malformed signatureHash (63 characters) on a sign anchor is refused', 'KS-1454: metadata.signatureHash on the sign verb RED KS-1454 R4: a malformed signatureHash (65 characters) on a sign anchor is refused', 'KS-1454: metadata.signatureHash on the sign verb RED KS-1454 R4: a malformed signatureHash (non-hex) on a sign anchor is refused', 'KS-1454: metadata.signatureHash on the sign verb RED KS-1454 R4: a malformed signatureHash (a number) on a sign anchor is refused', 'KS-1454: metadata.signatureHash on the sign verb RED KS-1454 R4: a malformed signatureHash (an array) on a sign anchor is refused', 'KS-1454: metadata.signatureHash on the sign verb RED KS-1454 R5: the anchored signatureHash reaches the Cardano metadatum as ONE string, not an array']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts passes with the product hunk (14 passed / 14 run)` [green_after.json: failed=0 of total=14, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=405 failed=1 | after: total=419 failed=1` · `NEW reds: []` [baseline_suite.json total=405 failed=1; after_suite.json total=419 failed=1]
- A6 [verbatim]: `PASS A6 whole services/anchoring suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/anchoring: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 +92/-0 test=src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/anchoring/src/anchorSchema.ts` (+12/-0 per numstat.out) and the test file `Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts` (+80/-0); two files. Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `fd84001c738a1bf9071d2d8a5cac6e953ad95789` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p1/input.json`. Brief (located from the run dir's own name under night/briefs/): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1454_p1/KS-1454.md`. Verdict source: `2_Project_Files/local-model/runs/spark_secuura_2026-10-29_ks_1454_p1/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/anchoring/src/anchorSchema.ts b/Blockchain/Dev/services/anchoring/src/anchorSchema.ts
--- a/Blockchain/Dev/services/anchoring/src/anchorSchema.ts
+++ b/Blockchain/Dev/services/anchoring/src/anchorSchema.ts
@@ -212,6 +212,8 @@
       IDENTITY_COMMITMENT_PATTERN,
       'Invalid identityCommitment format — expect <label>.v<N>:<64 lowercase hex>',
     ).optional(),
+    // KS-1454 (Stuart 2026-10-09, amended 10 Oct): the plain SHA-256 of the detached .p7s, lowercase hex, sign verb only (the refinement below refuses it on any other verb).
+    signatureHash: z.string().regex(/^[a-f0-9]{64}$/, 'Invalid signatureHash format - expect 64 lowercase hex (the SHA-256 of the detached .p7s)').optional(),
   }).optional(),
   // KS-1175: the top-level identity block (see identitySchema above). On POST /api/anchors S sends the commitment
   // here AND as metadata.identityCommitment (KS-721's field) — the refinement below the object rules on the pair.
@@ -243,6 +245,14 @@
       code: z.ZodIssueCode.custom,
       path: ['identity', 'identityCommitment'],
       message: 'identity.identityCommitment and metadata.identityCommitment differ — send one value, or the same value in both',
+    });
+  }
+  // KS-1454: a signature hash on any verb but `sign` (or with no verb) is a caller error (400); a stray hash must not be anchored as if it named a signature.
+  if (data.metadata?.signatureHash !== undefined && data.metadata.documentType !== 'sign') {
+    ctx.addIssue({
+      code: z.ZodIssueCode.custom,
+      path: ['metadata', 'signatureHash'],
+      message: 'metadata.signatureHash is only accepted with metadata.documentType "sign"',
     });
   }
 });
@@ -302,6 +312,8 @@
       ...(resolveIdentityCommitment(data)
         ? { identityCommitment: resolveIdentityCommitment(data) }
         : {}),
+      // KS-1454: the plain SHA-256 of S's detached .p7s, anchored VERBATIM (64 lowercase hex = exactly 64 bytes, the Cardano string cap, so the KS-1284 codec leaves it a single string).
+      ...(data.metadata?.signatureHash ? { signatureHash: data.metadata.signatureHash } : {}),
       // KS-1175: the seven non-PII identity fields, FLAT under secuura and whitelisted BY NAME — seven explicit
       // spreads, never `...data.identity` (the whitelist rule in this function's doc-comment). Flat rather than a nested `secuura.identity` map
       // (DECIDE 3) so every anchored value stays a scalar: the KS-1284 chain codec treats them uniformly and the
diff --git a/Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts b/Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/anchoring/src/__tests__/ks1454-signature-hash-is-accepted-and-anchored-on-the-sign-verb.test.ts
@@ -0,0 +1,80 @@
+// KS-1454 (anchoring anchorSchema.ts): Platform-S signs a file detached and wants the SHA-256 of the .p7s in the chain with the sign anchor. Today zod strips the unknown metadata key, so S's hash is silently dropped and
+// the anchor looks like a plain sign event. After the change: metadata.signatureHash (64 lowercase hex) is accepted, anchored verbatim as `signatureHash` beside documentType, and refused (400 at the route, a failed
+// parse here) on any verb but `sign` and when malformed. Pure cells: zod, the payload builder and the Cardano metadatum codec; no port, no database, no chain.
+import { describe, it, expect } from 'vitest';
+
+import { anchorDocumentSchema, buildFlatAnchorMetadataPayload } from '../anchorSchema';
+import { toCardanoMetadatum } from '../cardano/cardanoMetadatum';
+
+const BASE_BODY = {
+  documentId: 'doc-1777346021120-1e528170',
+  contentHash: 'a1b2c3d4e5f60718293a4b5c6d7e8f901a2b3c4d5e6f70819203a4b5c6d7e8f9',
+};
+const SIG = 'd'.repeat(32) + '0123456789abcdef0123456789abcdef';
+
+function signBody(signatureHash: unknown) {
+  return { ...BASE_BODY, metadata: { documentType: 'sign', signatureHash } };
+}
+
+describe('KS-1454: metadata.signatureHash on the sign verb', () => {
+  it('RED KS-1454 R1: a sign anchor carrying a signatureHash is accepted and the hash is anchored verbatim', () => {
+    const parsed = anchorDocumentSchema.parse(signBody(SIG));
+    const sec = buildFlatAnchorMetadataPayload(parsed, 'preview').secuura;
+    expect(sec.signatureHash).toBe(SIG);
+    expect(sec.documentType).toBe('sign');
+    expect(sec.hash).toBe(BASE_BODY.contentHash);
+  });
+
+  it('RED KS-1454 R2: the same hash on an upload anchor is refused, not anchored', () => {
+    const result = anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: 'upload', signatureHash: SIG } });
+    expect(result.success).toBe(false);
+  });
+
+  it('RED KS-1454 R3: a signatureHash with no documentType is refused', () => {
+    const result = anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { signatureHash: SIG } });
+    expect(result.success).toBe(false);
+  });
+
+  it.each([
+    ['uppercase hex', SIG.toUpperCase()],
+    ['63 characters', SIG.slice(1)],
+    ['65 characters', SIG + '0'],
+    ['non-hex', 'g'.repeat(64)],
+    ['a number', 12345],
+    ['an array', [SIG]],
+  ])('RED KS-1454 R4: a malformed signatureHash (%s) on a sign anchor is refused', (_label, value) => {
+    const result = anchorDocumentSchema.safeParse(signBody(value));
+    expect(result.success).toBe(false);
+  });
+
+  it('RED KS-1454 R5: the anchored signatureHash reaches the Cardano metadatum as ONE string, not an array', () => {
+    const parsed = anchorDocumentSchema.parse(signBody(SIG));
+    const sec = buildFlatAnchorMetadataPayload(parsed, 'preview').secuura;
+    const onChain = toCardanoMetadatum(sec) as Record<string, unknown>;
+    expect(onChain.signatureHash).toBe(SIG);
+  });
+
+  it('control KS-1454 C1: a sign anchor with no signatureHash is still accepted and anchors no signatureHash key', () => {
+    const parsed = anchorDocumentSchema.parse({ ...BASE_BODY, metadata: { documentType: 'sign' } });
+    const sec = buildFlatAnchorMetadataPayload(parsed, 'preview').secuura;
+    expect('signatureHash' in sec).toBe(false);
+    expect(sec.documentType).toBe('sign');
+  });
+
+  it('control KS-1454 C2: an upload anchor with no signatureHash is still accepted', () => {
+    expect(anchorDocumentSchema.safeParse({ ...BASE_BODY, metadata: { documentType: 'upload' } }).success).toBe(true);
+  });
+
+  it('control KS-1454 C3: a body with no metadata at all is still accepted and anchors exactly the base keys', () => {
+    const payload = buildFlatAnchorMetadataPayload(anchorDocumentSchema.parse(BASE_BODY), 'preview');
+    expect(Object.keys(payload.secuura).sort()).toEqual(['algorithm', 'certId', 'documentId', 'hash', 'network', 'timestamp', 'type', 'version']);
+  });
+
+  it('control KS-1454 C4: a sign anchor with a signatureHash and an identityCommitment keeps both distinct', () => {
+    const commitment = 'identity-commitment-l2.v1:' + 'b'.repeat(64);
+    const parsed = anchorDocumentSchema.parse({ ...BASE_BODY, metadata: { documentType: 'sign', signatureHash: SIG, identityCommitment: commitment } });
+    const sec = buildFlatAnchorMetadataPayload(parsed, 'preview').secuura;
+    expect(sec.identityCommitment).toBe(commitment);
+    expect(sec.hash).toBe(BASE_BODY.contentHash);
+  });
+});
```
