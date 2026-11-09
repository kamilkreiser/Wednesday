# READY - KS-2148-KS-2148-O115-P1 (Spark (DeepSeek V4 Flash), briefed, test_only_input) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2148_o115_p1_vc_verifier_public_verify_resolves_not_verified_on_unreadable_resolver_throw/out.md.checker/patch.diff` (from `ls` at 16:45 2026-11-09; sha256[:16] bb375e8664af3d37, 3041 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 16:45 2026-11-09 by Spark operator o115 after a source read (hold_ready.py, test_only_input path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2148_o115_p1_vc_verifier_public_verify_resolves_not_verified_on_unreadable_resolver_throw/out.md.checker`; product bytes were RE-MEASURED here.** Tip `6beac8734a2f607200e3e71371b84268e1599029`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json test_files, no product or plant file named]: ['Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts']; `+` lines 44 (ASCII), `-` lines 0.
- Product bytes UNCHANGED [re-measured: tip index blobs before and after a strict `git apply --cached -p1` of patch.diff]: `Blockchain/Dev/packages/shared/src/vc/verifier.ts` blob 04f24453c911; plant file(s) also unchanged.
- Red cells [input.json]:
  - `ks2148 N2 verify() with a revoked Proxy`
  - `ks2148 N3 verify() with an object whose toString throws`
  - `ks2148 N4 verify() with a Symbol`
- Red-first evidence [checker.out, verbatim]: A4 green without plant, A5 red under the plant by assertion.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts)`
  - `PASS A3p the plant applies at the tip (golden_red.diff)`
  - `PASS A4 GREEN WITHOUT PLANT: 3 red cell(s) exist and pass on the unmodified product; declared files 12 cells, 0 red`
  - `PASS A6 WHOLE SUITE no worse: cells 1618 -> 1622, red 1 -> 1`
  - `PASS A5 RED WITH PLANT: 3 red cell(s) fail by assertion under the plant (Blockchain/Dev/packages/shared/src/vc/verifier.ts), pass without it`
  - `PASS A7 RESTORE: 2 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier test_only_input)`

**PR NOTES for the raise seat:** TEST_ONLY_INPUT - test bytes only, zero product bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The red proof is the brief's plant (checker clone only), not a change in the PR. No `tsc` leg covers a vitest file; DOES NOT PROVE the plant is the regression that matters or that a cell catches a different one. Wednesday read the cells against the brief before this hold.

```diff
--- a/Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts
+++ b/Blockchain/Dev/packages/shared/src/__tests__/ks1973-vc-verifier-issuer-lookup-and-ed25519-catches-unreadable-throw.test.ts
@@ -110,4 +110,48 @@
   it('RED ks1973 R5 an object whose toString throws, thrown by the key decode, gives the Ed25519 entry with a constant reason', async () => {
     expect(await signatureWithKey(throwingKey(toStringThrows()))).toEqual({ valid: false, errors: [`${ED}unreadable thrown value`] });
   });
+
+  // KS-2148 (gate 273 G273-2108-3): the public verify() is reached by no cell above; the eight cells call a private method through the cast.
+  type Verified = { verified: boolean; checks: { issuerDID: boolean }; errors?: string[] };
+  async function verifyWith(value: unknown): Promise<Verified | 'rejected'> {
+    const verifier = new VerifiableCredentialVerifier({ didResolver: () => Promise.reject(value) });
+    try {
+      return (await verifier.verify(credential('zAAAA') as never)) as unknown as Verified;
+    } catch {
+      return 'rejected';
+    }
+  }
+  const entry = (text: string): string => `Failed to resolve DID did:example:issuer: ${text}`;
+
+  it('control ks2148 N1 verify() with an ordinary Error from the DID resolver resolves not verified, with the lookup entry and its text', async () => {
+    const out = await verifyWith(new Error('resolver down'));
+    expect(out).not.toBe('rejected');
+    expect((out as Verified).verified).toBe(false);
+    expect((out as Verified).checks.issuerDID).toBe(false);
+    expect((out as Verified).errors).toContain(entry('Error: resolver down'));
+  });
+
+  it('control ks2148 N2 verify() with a revoked Proxy from the DID resolver resolves not verified, with the lookup entry and a constant reason', async () => {
+    const out = await verifyWith(revokedProxy());
+    expect(out).not.toBe('rejected');
+    expect((out as Verified).verified).toBe(false);
+    expect((out as Verified).checks.issuerDID).toBe(false);
+    expect((out as Verified).errors).toContain(entry('unreadable thrown value'));
+  });
+
+  it('control ks2148 N3 verify() with an object whose toString throws from the DID resolver resolves not verified, with a constant reason', async () => {
+    const out = await verifyWith(toStringThrows());
+    expect(out).not.toBe('rejected');
+    expect((out as Verified).verified).toBe(false);
+    expect((out as Verified).checks.issuerDID).toBe(false);
+    expect((out as Verified).errors).toContain(entry('unreadable thrown value'));
+  });
+
+  it('control ks2148 N4 verify() with a Symbol from the DID resolver resolves not verified, with the lookup entry and its text', async () => {
+    const out = await verifyWith(Symbol('ks2148'));
+    expect(out).not.toBe('rejected');
+    expect((out as Verified).verified).toBe(false);
+    expect((out as Verified).checks.issuerDID).toBe(false);
+    expect((out as Verified).errors).toContain(entry('Symbol(ks2148)'));
+  });
 });
```
