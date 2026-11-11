# READY — KS-1868-KS-1868-O138-P2 (Spark (DeepSeek V4 Flash), briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p2_auth_issuer_cert_parse_cert_and_verify_key_matches_cert_catches_guard_the_thrown_value_read/out.md.checker/patch.diff`** (from `ls` at 15:57 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p2_auth_issuer_cert_parse_cert_and_verify_key_matches_cert_catches_guard_the_thrown_value_read/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p2_auth_issuer_cert_parse_cert_and_verify_key_matches_cert_catches_guard_the_thrown_value_read/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o138_p2_auth_issuer_cert_parse_cert_and_verify_key_matches_cert_catches_guard_the_thrown_value_read/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 15:57 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p2_auth_issuer_cert_parse_cert_and_verify_key_matches_cert_catches_guard_the_thrown_value_read/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/services/issuerCert.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-crypto-failures-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/services/issuerCert.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-crypto-failures-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
18	3	Blockchain/Dev/services/auth/src/services/issuerCert.ts
130	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-crypto-failures-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (18 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: issuerCert.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/services/issuerCert.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-crypto-failures-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/services/issuerCert.ts 18 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-crypto-failures-unreadable-throw.test.ts 130 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/services/issuerCert.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-crypto-failures-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (6 failed / 9 run; controls green; assertion reds)` [red_first.json: failed=6 of total=9; red cell(s): ['KS-1868 issuerCert reads a thrown crypto failure safely RED ks1868 R1 parseCert: a revoked Proxy thrown by the X.509 parser becomes INVALID_CERT_PEM with the constant reason', 'KS-1868 issuerCert reads a thrown crypto failure safely RED ks1868 R2 parseCert: an Error whose message getter throws becomes INVALID_CERT_PEM with the constant reason', 'KS-1868 issuerCert reads a thrown crypto failure safely RED ks1868 R3 verifyKeyMatchesCert key load: a revoked Proxy becomes KEY_PARSE_ERROR with the constant reason', 'KS-1868 issuerCert reads a thrown crypto failure safely RED ks1868 R4 verifyKeyMatchesCert key load: an Error whose message getter throws becomes KEY_PARSE_ERROR with the constant reason', 'KS-1868 issuerCert reads a thrown crypto failure safely RED ks1868 R5 verifyKeyMatchesCert sign: a revoked Proxy becomes KEY_MISMATCH with the constant reason', 'KS-1868 issuerCert reads a thrown crypto failure safely RED ks1868 R6 verifyKeyMatchesCert sign: an Error whose message getter throws becomes KEY_MISMATCH with the constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (9 passed / 9 run)` [green_after.json: failed=0 of total=9, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1839 failed=0 | after: total=1848 failed=0` · `NEW reds: []` [baseline_suite.json total=1839 failed=0; after_suite.json total=1848 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/services/issuerCert.ts` (+18/-3 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-crypto-failures-unreadable-throw.test.ts` (+130/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/services/issuerCert.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p2_auth_issuer_cert_parse_cert_and_verify_key_matches_cert_catches_guard_the_thrown_value_read/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o138_p2_auth_issuer_cert_parse_cert_and_verify_key_matches_cert_catches_guard_the_thrown_value_read/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o138_p2_auth_issuer_cert_parse_cert_and_verify_key_matches_cert_catches_guard_the_thrown_value_read/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/services/issuerCert.ts b/Blockchain/Dev/services/auth/src/services/issuerCert.ts
--- a/Blockchain/Dev/services/auth/src/services/issuerCert.ts
+++ b/Blockchain/Dev/services/auth/src/services/issuerCert.ts
@@ -112,5 +112,10 @@
     cert = new crypto.X509Certificate(trimmed);
   } catch (err) {
-    const msg = err instanceof Error ? err.message : String(err);
+    let msg: string;
+    try {
+      msg = err instanceof Error ? err.message : String(err);
+    } catch {
+      msg = 'unreadable thrown value';
+    }
     throw new IssuerCertError('INVALID_CERT_PEM', `Could not parse cert: ${msg}`);
   }
@@ -197,5 +202,10 @@
     });
   } catch (err) {
-    const msg = err instanceof Error ? err.message : String(err);
+    let msg: string;
+    try {
+      msg = err instanceof Error ? err.message : String(err);
+    } catch {
+      msg = 'unreadable thrown value';
+    }
     // Distinguish "wrong passphrase" from "malformed PEM" if we can.
     if (passphrase && /bad decrypt|invalid|incorrect/i.test(msg)) {
@@ -217,5 +227,10 @@
     signature = crypto.sign(algo, nonce, privateKey);
   } catch (err) {
-    const msg = err instanceof Error ? err.message : String(err);
+    let msg: string;
+    try {
+      msg = err instanceof Error ? err.message : String(err);
+    } catch {
+      msg = 'unreadable thrown value';
+    }
     throw new IssuerCertError('KEY_MISMATCH', `Could not sign with private key: ${msg}`);
   }
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-crypto-failures-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-crypto-failures-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-crypto-failures-unreadable-throw.test.ts
@@ -0,0 +1,130 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868: parseCert and verifyKeyMatchesCert (services/issuerCert.ts) wrap a failed crypto call in an IssuerCertError whose text carries the
+// caught value, read with `err instanceof Error ? err.message : String(err)`. That read can itself throw (a revoked Proxy throws on `instanceof`;
+// an Error whose `message` getter throws, throws on `.message`): the caller then got a bare TypeError instead of the IssuerCertError with its
+// stable code that the route layer maps to a 4xx answer. Each of the three catches now reads the value inside its own try and uses the constant
+// `unreadable thrown value` when it cannot be read; an ordinary Error still produces the same IssuerCertError text as before.
+// Node's `crypto` is replaced by a wrapper whose X509Certificate constructor, createPrivateKey and sign raise `h.toThrow` when armed and are
+// plain stubs otherwise, so no real key or certificate is needed.
+const h = vi.hoisted(() => ({
+  arm: '' as '' | 'x509' | 'key' | 'sign',
+  toThrow: undefined as unknown,
+}));
+
+vi.mock('crypto', async () => {
+  const actual = await vi.importActual<typeof import('crypto')>('crypto');
+  class StubCert {
+    publicKey = {};
+    constructor(_pem: string) {
+      if (h.arm === 'x509') throw h.toThrow;
+    }
+  }
+  const mocked = {
+    ...actual,
+    X509Certificate: StubCert,
+    createPrivateKey: (_o: unknown) => {
+      if (h.arm === 'key') throw h.toThrow;
+      return { asymmetricKeyType: 'rsa' };
+    },
+    sign: (..._a: unknown[]) => {
+      if (h.arm === 'sign') throw h.toThrow;
+      return Buffer.from('sig');
+    },
+  };
+  return { ...mocked, default: mocked };
+});
+
+import { parseCert, verifyKeyMatchesCert, IssuerCertError } from '../services/issuerCert';
+
+const CERT = '-----BEGIN CERTIFICATE-----\nAAAA\n-----END CERTIFICATE-----\n';
+
+type Seen = { code: string; message: string } | { notAnIssuerCertError: true } | undefined;
+
+function seen(fn: () => void): Seen {
+  try {
+    fn();
+    return undefined;
+  } catch (e) {
+    return e instanceof IssuerCertError ? { code: e.code, message: e.message } : { notAnIssuerCertError: true };
+  }
+}
+
+const revoked = () => {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+};
+const getterThrows = () =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+const parse = () => seen(() => parseCert(CERT));
+const keyParse = () => seen(() => verifyKeyMatchesCert(CERT, 'key-pem'));
+const signing = () => seen(() => verifyKeyMatchesCert(CERT, 'key-pem'));
+
+describe('KS-1868 issuerCert reads a thrown crypto failure safely', () => {
+  beforeEach(() => {
+    h.arm = '';
+    h.toThrow = undefined;
+  });
+
+  it('RED ks1868 R1 parseCert: a revoked Proxy thrown by the X.509 parser becomes INVALID_CERT_PEM with the constant reason', () => {
+    h.arm = 'x509';
+    h.toThrow = revoked();
+    expect(parse()).toEqual({ code: 'INVALID_CERT_PEM', message: 'Could not parse cert: unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 parseCert: an Error whose message getter throws becomes INVALID_CERT_PEM with the constant reason', () => {
+    h.arm = 'x509';
+    h.toThrow = getterThrows();
+    expect(parse()).toEqual({ code: 'INVALID_CERT_PEM', message: 'Could not parse cert: unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 verifyKeyMatchesCert key load: a revoked Proxy becomes KEY_PARSE_ERROR with the constant reason', () => {
+    h.arm = 'key';
+    h.toThrow = revoked();
+    expect(keyParse()).toEqual({ code: 'KEY_PARSE_ERROR', message: 'Could not parse private key: unreadable thrown value' });
+  });
+
+  it('RED ks1868 R4 verifyKeyMatchesCert key load: an Error whose message getter throws becomes KEY_PARSE_ERROR with the constant reason', () => {
+    h.arm = 'key';
+    h.toThrow = getterThrows();
+    expect(keyParse()).toEqual({ code: 'KEY_PARSE_ERROR', message: 'Could not parse private key: unreadable thrown value' });
+  });
+
+  it('RED ks1868 R5 verifyKeyMatchesCert sign: a revoked Proxy becomes KEY_MISMATCH with the constant reason', () => {
+    h.arm = 'sign';
+    h.toThrow = revoked();
+    expect(signing()).toEqual({ code: 'KEY_MISMATCH', message: 'Could not sign with private key: unreadable thrown value' });
+  });
+
+  it('RED ks1868 R6 verifyKeyMatchesCert sign: an Error whose message getter throws becomes KEY_MISMATCH with the constant reason', () => {
+    h.arm = 'sign';
+    h.toThrow = getterThrows();
+    expect(signing()).toEqual({ code: 'KEY_MISMATCH', message: 'Could not sign with private key: unreadable thrown value' });
+  });
+
+  it('control ks1868 C1 parseCert: an ordinary Error keeps its own text in the INVALID_CERT_PEM message', () => {
+    h.arm = 'x509';
+    h.toThrow = new Error('asn1 boom');
+    expect(parse()).toEqual({ code: 'INVALID_CERT_PEM', message: 'Could not parse cert: asn1 boom' });
+  });
+
+  it('control ks1868 C2 verifyKeyMatchesCert key load: an ordinary Error keeps its own text in the KEY_PARSE_ERROR message', () => {
+    h.arm = 'key';
+    h.toThrow = new Error('pem boom');
+    expect(keyParse()).toEqual({ code: 'KEY_PARSE_ERROR', message: 'Could not parse private key: pem boom' });
+  });
+
+  it('control ks1868 C3 verifyKeyMatchesCert sign: an ordinary Error keeps its own text in the KEY_MISMATCH message', () => {
+    h.arm = 'sign';
+    h.toThrow = new Error('sign boom');
+    expect(signing()).toEqual({ code: 'KEY_MISMATCH', message: 'Could not sign with private key: sign boom' });
+  });
+});
```
