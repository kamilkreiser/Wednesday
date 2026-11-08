# READY — KS-1973-KS-1973-O107-P3 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1973_o107_p3_shared_vc_verifier_issuer_lookup_and_ed25519_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 04:17 2026-11-09; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1973_o107_p3_shared_vc_verifier_issuer_lookup_and_ed25519_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1973_o107_p3_shared_vc_verifier_issuer_lookup_and_ed25519_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1973_o107_p3_shared_vc_verifier_issuer_lookup_and_ed25519_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1973_o107_p3_shared_vc_verifier_issuer_lookup_and_ed25519_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 04:17 2026-11-09 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1973_o107_p3_shared_vc_verifier_issuer_lookup_and_ed25519_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `2935f723109756a60cadc5521977c7a036ec322d`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/packages/shared/src/vc/verifier.ts } + { Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/packages/shared/src/vc/verifier.ts` (product) and `Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
13	2	Blockchain/Dev/packages/shared/src/vc/verifier.ts
113	0	Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (13 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: verifier.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/packages/shared/src/vc/verifier.ts`; test(s): `Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/packages/shared/src/vc/verifier.ts 13 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts 113 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/packages/shared/src/vc/verifier.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=5 of total=8; red cell(s): ['KS-1973 the issuer lookup and the Ed25519 catch read a thrown value safely RED ks1973 R1 a revoked Proxy from the DID resolver gives the lookup entry with a constant reason', 'KS-1973 the issuer lookup and the Ed25519 catch read a thrown value safely RED ks1973 R2 an object whose toString throws from the DID resolver gives the lookup entry with a constant reason', 'KS-1973 the issuer lookup and the Ed25519 catch read a thrown value safely RED ks1973 R3 a thrown Symbol from the DID resolver gives the lookup entry with its text', 'KS-1973 the issuer lookup and the Ed25519 catch read a thrown value safely RED ks1973 R4 a revoked Proxy thrown by the key decode gives the Ed25519 entry with a constant reason', 'KS-1973 the issuer lookup and the Ed25519 catch read a thrown value safely RED ks1973 R5 an object whose toString throws, thrown by the key decode, gives the Ed25519 entry with a constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1597 failed=1 | after: total=1605 failed=1` · `NEW reds: []` [baseline_suite.json total=1597 failed=1; after_suite.json total=1605 failed=1]
- A6 [verbatim]: `PASS A6 whole packages/shared suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for packages/shared: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/packages/shared/src/vc/verifier.ts` (+13/-2 per numstat.out) and the test file `Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts` (+113/-0); 2 files in all (code_patch2: products Blockchain/Dev/packages/shared/src/vc/verifier.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `2935f723109756a60cadc5521977c7a036ec322d` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1973_o107_p3_shared_vc_verifier_issuer_lookup_and_ed25519_catches_unreadable_throw/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1973_o107_p3_shared_vc_verifier_issuer_lookup_and_ed25519_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/packages/shared/src/vc/verifier.ts b/Blockchain/Dev/packages/shared/src/vc/verifier.ts
--- a/Blockchain/Dev/packages/shared/src/vc/verifier.ts
+++ b/Blockchain/Dev/packages/shared/src/vc/verifier.ts
@@ -399,5 +399,10 @@
               }
             } catch (verifyErr: unknown) {
-              const msg = verifyErr instanceof Error ? verifyErr.message : String(verifyErr);
+              let msg: string;
+              try {
+                msg = verifyErr instanceof Error ? verifyErr.message : String(verifyErr);
+              } catch {
+                msg = 'unreadable thrown value';
+              }
               errors.push(`Ed25519 verification error: ${msg}`);
             }
@@ -457,5 +462,11 @@
         }
       } catch (error) {
-        errors.push(`Failed to resolve DID ${issuerDID}: ${error}`);
+        let reason: string;
+        try {
+          reason = String(error);
+        } catch {
+          reason = 'unreadable thrown value';
+        }
+        errors.push(`Failed to resolve DID ${issuerDID}: ${reason}`);
       }
     }
diff --git a/Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts b/Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts
@@ -0,0 +1,113 @@
+import { describe, it, expect } from 'vitest';
+
+// KS-1973: two catches of the credential verifier (src/vc/verifier.ts) still read a thrown value unguarded. (A) the catch of
+// verifyIssuerDID builds `Failed to resolve DID <did>: ${error}` with a bare template literal, so a DID resolver that rejects
+// with a revoked Proxy, a Symbol or an object whose toString throws makes verifyIssuerDID REJECT (and so verify()). (B) the inner
+// Ed25519 catch of verifySignature reads `verifyErr instanceof Error ? verifyErr.message : String(verifyErr)`, so a hostile value
+// thrown by the key decode makes that catch throw into the outer catch and the entry reads `Signature verification error: ...`
+// instead of `Ed25519 verification error: ...`. The DID resolver stand-in is a plain function; for (B) the resolver answers a
+// document whose publicKey is a Proxy that throws the cell's value when Buffer.from reads it; no network, no key material.
+import { VerifiableCredentialVerifier } from '../vc/verifier';
+
+type Result = { valid: boolean; errors: string[] };
+type Priv = {
+  verifyIssuerDID(c: unknown): Promise<Result>;
+  verifySignature(c: unknown): Promise<Result>;
+};
+
+const credential = (proofValue: string) => ({
+  '@context': ['https://www.w3.org/2018/credentials/v1'],
+  type: ['VerifiableCredential'],
+  issuer: 'did:example:issuer',
+  issuanceDate: '2026-01-01T00:00:00Z',
+  credentialSubject: { id: 'did:example:subject' },
+  proof: {
+    type: 'SecuuraSignature2024',
+    created: '2026-01-01T00:00:00Z',
+    verificationMethod: 'did:example:issuer#key-1',
+    proofPurpose: 'assertionMethod',
+    proofValue,
+  },
+});
+
+/** The result, or the string 'rejected' when the call rejects (an assertion can then fail on it). */
+async function issuerLookup(value: unknown): Promise<Result | 'rejected'> {
+  const verifier = new VerifiableCredentialVerifier({ didResolver: () => Promise.reject(value) });
+  try {
+    return await (verifier as unknown as Priv).verifyIssuerDID(credential('zAAAA'));
+  } catch {
+    return 'rejected';
+  }
+}
+
+async function signatureWithKey(publicKey: unknown): Promise<Result | 'rejected'> {
+  const verifier = new VerifiableCredentialVerifier({ didResolver: () => Promise.resolve({ publicKey }) } as never);
+  try {
+    return await (verifier as unknown as Priv).verifySignature(credential('zAAAA'));
+  } catch {
+    return 'rejected';
+  }
+}
+
+const throwingKey = (value: unknown): unknown =>
+  new Proxy(
+    {},
+    {
+      get() {
+        throw value;
+      },
+    },
+  );
+
+const revokedProxy = (): unknown => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+
+const toStringThrows = (): unknown => ({
+  toString() {
+    throw new Error('toString boom');
+  },
+});
+
+const lookupEntry = (text: string): Result => ({ valid: false, errors: [`Failed to resolve DID did:example:issuer: ${text}`] });
+const ED = 'Ed25519 verification error: ';
+
+describe('KS-1973 the issuer lookup and the Ed25519 catch read a thrown value safely', () => {
+  it('control ks1973 C1 an ordinary Error from the DID resolver gives the lookup entry with its text', async () => {
+    expect(await issuerLookup(new Error('resolver down'))).toEqual(lookupEntry('Error: resolver down'));
+  });
+
+  it('control ks1973 C2 a thrown plain string from the DID resolver gives the lookup entry with that text', async () => {
+    expect(await issuerLookup('plain text failure')).toEqual(lookupEntry('plain text failure'));
+  });
+
+  it('control ks1973 C3 an ordinary key decode failure gives the Ed25519 entry', async () => {
+    const out = await signatureWithKey('00');
+    expect(out).not.toBe('rejected');
+    const errors = (out as Result).errors;
+    expect(errors.length).toBe(1);
+    expect(errors[0].startsWith(ED)).toBe(true);
+  });
+
+  it('RED ks1973 R1 a revoked Proxy from the DID resolver gives the lookup entry with a constant reason', async () => {
+    expect(await issuerLookup(revokedProxy())).toEqual(lookupEntry('unreadable thrown value'));
+  });
+
+  it('RED ks1973 R2 an object whose toString throws from the DID resolver gives the lookup entry with a constant reason', async () => {
+    expect(await issuerLookup(toStringThrows())).toEqual(lookupEntry('unreadable thrown value'));
+  });
+
+  it('RED ks1973 R3 a thrown Symbol from the DID resolver gives the lookup entry with its text', async () => {
+    expect(await issuerLookup(Symbol('ks1973'))).toEqual(lookupEntry('Symbol(ks1973)'));
+  });
+
+  it('RED ks1973 R4 a revoked Proxy thrown by the key decode gives the Ed25519 entry with a constant reason', async () => {
+    expect(await signatureWithKey(throwingKey(revokedProxy()))).toEqual({ valid: false, errors: [`${ED}unreadable thrown value`] });
+  });
+
+  it('RED ks1973 R5 an object whose toString throws, thrown by the key decode, gives the Ed25519 entry with a constant reason', async () => {
+    expect(await signatureWithKey(throwingKey(toStringThrows()))).toEqual({ valid: false, errors: [`${ED}unreadable thrown value`] });
+  });
+});
```
