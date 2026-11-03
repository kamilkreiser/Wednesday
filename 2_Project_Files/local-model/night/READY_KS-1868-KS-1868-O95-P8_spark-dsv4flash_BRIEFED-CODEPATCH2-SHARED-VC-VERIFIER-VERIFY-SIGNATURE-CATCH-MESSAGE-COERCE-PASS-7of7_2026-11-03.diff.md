# READY — KS-1868-KS-1868-O95-P8 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p8_shared_vc_verifier_verify_signature_outer_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 15:13 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p8_shared_vc_verifier_verify_signature_outer_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p8_shared_vc_verifier_verify_signature_outer_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p8_shared_vc_verifier_verify_signature_outer_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p8_shared_vc_verifier_verify_signature_outer_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 15:13 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p8_shared_vc_verifier_verify_signature_outer_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `67309f28ab2132ca7b6a45b28c731aa480642a9a`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/packages/shared/src/vc/verifier.ts } + { Blockchain/Dev/packages/shared/src/__tests__/ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/vc/verifier.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	1	Blockchain/Dev/packages/shared/src/vc/verifier.ts
71	0	Blockchain/Dev/packages/shared/src/__tests__/ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (6 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: verifier.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/packages/shared/src/vc/verifier.ts`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/packages/shared/src/vc/verifier.ts 6 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts 71 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/vc/verifier.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 the credential signature check reads the thrown value safely RED ks1868 R1 a revoked Proxy from the DID resolver gives the error entry with a constant reason', 'KS-1868 the credential signature check reads the thrown value safely RED ks1868 R2 an Error whose message getter throws from the DID resolver gives the error entry with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1447 failed=1 | after: total=1451 failed=1` · `NEW reds: []` [baseline_suite.json total=1447 failed=1; after_suite.json total=1451 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/vc/verifier.ts` (+6/-1 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts` (+71/-0); 2 files in all (code_patch2: products Blockchain/Dev/packages/shared/src/vc/verifier.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `67309f28ab2132ca7b6a45b28c731aa480642a9a` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p8_shared_vc_verifier_verify_signature_outer_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o95_p8_shared_vc_verifier_verify_signature_outer_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p8_shared_vc_verifier_verify_signature_outer_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/vc/verifier.ts b/Blockchain/Dev/packages/shared/src/vc/verifier.ts
--- a/Blockchain/Dev/packages/shared/src/vc/verifier.ts
+++ b/Blockchain/Dev/packages/shared/src/vc/verifier.ts
@@ -415,6 +415,11 @@
         errors.push(`Unknown proof value format: ${proofValue.substring(0, 10)}...`);
       }
     } catch (err: unknown) {
-      const msg = err instanceof Error ? err.message : String(err);
+      let msg: string;
+      try {
+        msg = err instanceof Error ? err.message : String(err);
+      } catch {
+        msg = 'unreadable thrown value';
+      }
       errors.push(`Signature verification error: ${msg}`);
     }
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1868-vc-verifier-verify-signature-catch-unreadable-throw.test.ts
@@ -0,0 +1,71 @@
+import { describe, it, expect } from 'vitest';
+
+// KS-1868: the signature check of the credential verifier (VerifiableCredentialVerifier.verifySignature in src/vc/verifier.ts) answers
+// `{ valid, errors }`; a failure while checking a proof is the error entry `Signature verification error: <message>`, never a throw.
+// The outer catch reads the failure as `err instanceof Error ? err.message : String(err)`, unguarded. When the value the DID resolver
+// rejected with cannot be read (a revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on `.message`)
+// the catch throws, so verifySignature REJECTS where an ordinary Error gives the error entry. The DID resolver stand-in is a plain
+// function rejecting with the cell's value; the proof is an HMAC-form proof so the resolver is the only thing that can throw; no
+// network, no key material.
+import { VerifiableCredentialVerifier } from '../vc/verifier';
+
+type SignatureResult = { valid: boolean; errors: string[] };
+
+/** The signature result, or the string 'rejected' when verifySignature rejects (an assertion can then fail on it). */
+async function check(value: unknown): Promise<SignatureResult | 'rejected'> {
+  const verifier = new VerifiableCredentialVerifier({ didResolver: () => Promise.reject(value) });
+  const credential = {
+    '@context': ['https://www.w3.org/2018/credentials/v1'],
+    type: ['VerifiableCredential'],
+    issuer: 'did:example:issuer',
+    issuanceDate: '2026-01-01T00:00:00Z',
+    credentialSubject: { id: 'did:example:subject' },
+    proof: {
+      type: 'SecuuraSignature2024',
+      created: '2026-01-01T00:00:00Z',
+      verificationMethod: 'did:example:issuer#key-1',
+      proofPurpose: 'assertionMethod',
+      proofValue: 'zHMAC_ks1868',
+    },
+  };
+  try {
+    return await (verifier as unknown as { verifySignature(c: unknown): Promise<SignatureResult> }).verifySignature(credential);
+  } catch {
+    return 'rejected';
+  }
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
+const entry = (message: string): SignatureResult => ({ valid: false, errors: [`Signature verification error: ${message}`] });
+
+describe('KS-1868 the credential signature check reads the thrown value safely', () => {
+  it('control ks1868 C1 an ordinary Error from the DID resolver gives the error entry with its message', async () => {
+    expect(await check(new Error('resolver down'))).toEqual(entry('resolver down'));
+  });
+
+  it('control ks1868 C2 a thrown plain string from the DID resolver gives the error entry with that text', async () => {
+    expect(await check('plain text failure')).toEqual(entry('plain text failure'));
+  });
+
+  it('RED ks1868 R1 a revoked Proxy from the DID resolver gives the error entry with a constant reason', async () => {
+    expect(await check(revokedProxy())).toEqual(entry('unreadable thrown value'));
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws from the DID resolver gives the error entry with a constant reason', async () => {
+    expect(await check(getterThrows())).toEqual(entry('unreadable thrown value'));
+  });
+});
```
