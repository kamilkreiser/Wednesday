# READY — KS-1868-KS-1868-O139-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o139_p1_auth_issuer_cert_sign_content_hash_with_cert_catches_guard_the_thrown_value_read/out.md.checker/patch.diff`** (from `ls` at 16:26 2026-11-11; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o139_p1_auth_issuer_cert_sign_content_hash_with_cert_catches_guard_the_thrown_value_read/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o139_p1_auth_issuer_cert_sign_content_hash_with_cert_catches_guard_the_thrown_value_read/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; golden path `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o139_p1_auth_issuer_cert_sign_content_hash_with_cert_catches_guard_the_thrown_value_read/golden.diff/out.md.checker/patch.diff` does not exist — no identity claim is made.

**Held 16:26 2026-11-11 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o139_p1_auth_issuer_cert_sign_content_hash_with_cert_catches_guard_the_thrown_value_read/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/services/issuerCert.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-sign-content-hash-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/services/issuerCert.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-sign-content-hash-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	2	Blockchain/Dev/services/auth/src/services/issuerCert.ts
110	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-sign-content-hash-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: issuerCert.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/services/issuerCert.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-sign-content-hash-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/services/issuerCert.ts 14 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-sign-content-hash-unreadable-throw.test.ts 110 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/services/issuerCert.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-sign-content-hash-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 7 run; controls green; assertion reds)` [red_first.json: failed=4 of total=7; red cell(s): ['KS-1868 signContentHashWithCert reads a thrown crypto failure safely RED ks1868 R1 key load: a revoked Proxy becomes SIGN_FAILED with the constant reason', 'KS-1868 signContentHashWithCert reads a thrown crypto failure safely RED ks1868 R2 key load: an Error whose message getter throws becomes SIGN_FAILED with the constant reason', 'KS-1868 signContentHashWithCert reads a thrown crypto failure safely RED ks1868 R3 sign: a revoked Proxy becomes SIGN_FAILED with the constant reason', 'KS-1868 signContentHashWithCert reads a thrown crypto failure safely RED ks1868 R4 sign: an Error whose message getter throws becomes SIGN_FAILED with the constant reason']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (7 passed / 7 run)` [green_after.json: failed=0 of total=7, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1839 failed=0 | after: total=1846 failed=0` · `NEW reds: []` [baseline_suite.json total=1839 failed=0; after_suite.json total=1846 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/services/issuerCert.ts` (+14/-2 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-sign-content-hash-unreadable-throw.test.ts` (+110/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/services/issuerCert.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `249be7c8cd147b53301fccf389cfdeab9e6b1c56` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o139_p1_auth_issuer_cert_sign_content_hash_with_cert_catches_guard_the_thrown_value_read/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o139_p1_auth_issuer_cert_sign_content_hash_with_cert_catches_guard_the_thrown_value_read/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-11_ks_1868_o139_p1_auth_issuer_cert_sign_content_hash_with_cert_catches_guard_the_thrown_value_read/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/services/issuerCert.ts b/Blockchain/Dev/services/auth/src/services/issuerCert.ts
--- a/Blockchain/Dev/services/auth/src/services/issuerCert.ts
+++ b/Blockchain/Dev/services/auth/src/services/issuerCert.ts
@@ -344,8 +344,14 @@
   try {
     privateKey = crypto.createPrivateKey({ key: privateKeyPem, format: 'pem' });
   } catch (err) {
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     throw new IssuerCertError(
       'SIGN_FAILED',
-      `Could not load decrypted private key: ${err instanceof Error ? err.message : String(err)}`,
+      `Could not load decrypted private key: ${reason}`,
     );
   }
@@ -358,8 +364,14 @@
   try {
     signature = crypto.sign(digest, hashBytes, privateKey);
   } catch (err) {
+    let reason: string;
+    try {
+      reason = err instanceof Error ? err.message : String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     throw new IssuerCertError(
       'SIGN_FAILED',
-      `crypto.sign failed: ${err instanceof Error ? err.message : String(err)}`,
+      `crypto.sign failed: ${reason}`,
     );
   }
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-sign-content-hash-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-sign-content-hash-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-issuer-cert-sign-content-hash-unreadable-throw.test.ts
@@ -0,0 +1,110 @@
+import { describe, it, expect, vi, beforeEach } from 'vitest';
+
+// KS-1868: signContentHashWithCert (services/issuerCert.ts) wraps a failed key load or a failed signature in an IssuerCertError('SIGN_FAILED') whose
+// text carries the caught value, read INLINE in the message with `err instanceof Error ? err.message : String(err)`. That read can itself throw (a
+// revoked Proxy throws on `instanceof`; an Error whose `message` getter throws, throws on `.message`): the caller then got a bare TypeError instead of
+// the IssuerCertError with its stable code. Each of the two catches now reads the value into a local inside its own try and uses the constant
+// `unreadable thrown value` when it cannot be read; an ordinary Error still produces the same IssuerCertError text as before.
+// Node's `crypto` is replaced by a wrapper whose createPrivateKey and sign raise `h.toThrow` when armed and are plain stubs otherwise, and the shared
+// field decryption is replaced by a stand-in that returns a fixed PEM string, so no real key is needed and nothing touches a database or the network.
+const h = vi.hoisted(() => ({
+  arm: '' as '' | 'key' | 'sign',
+  toThrow: undefined as unknown,
+}));
+
+vi.mock('@secuura/shared', () => ({
+  encryptField: (v: string) => v,
+  decryptField: () => 'pem-text',
+}));
+
+vi.mock('crypto', async () => {
+  const actual = await vi.importActual<typeof import('crypto')>('crypto');
+  const mocked = {
+    ...actual,
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
+import { signContentHashWithCert, IssuerCertError } from '../services/issuerCert';
+
+const HASH = 'a'.repeat(64);
+
+type Seen = { code: string; message: string } | { notAnIssuerCertError: true } | { signed: true };
+
+function sign(): Seen {
+  try {
+    signContentHashWithCert({ encryptedPrivateKey: 'v1:blob', certId: 'cert-1868', keyAlgorithm: 'RSA', contentHash: HASH });
+    return { signed: true };
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
+describe('KS-1868 signContentHashWithCert reads a thrown crypto failure safely', () => {
+  beforeEach(() => {
+    h.arm = '';
+    h.toThrow = undefined;
+  });
+
+  it('RED ks1868 R1 key load: a revoked Proxy becomes SIGN_FAILED with the constant reason', () => {
+    h.arm = 'key';
+    h.toThrow = revoked();
+    expect(sign()).toEqual({ code: 'SIGN_FAILED', message: 'Could not load decrypted private key: unreadable thrown value' });
+  });
+
+  it('RED ks1868 R2 key load: an Error whose message getter throws becomes SIGN_FAILED with the constant reason', () => {
+    h.arm = 'key';
+    h.toThrow = getterThrows();
+    expect(sign()).toEqual({ code: 'SIGN_FAILED', message: 'Could not load decrypted private key: unreadable thrown value' });
+  });
+
+  it('RED ks1868 R3 sign: a revoked Proxy becomes SIGN_FAILED with the constant reason', () => {
+    h.arm = 'sign';
+    h.toThrow = revoked();
+    expect(sign()).toEqual({ code: 'SIGN_FAILED', message: 'crypto.sign failed: unreadable thrown value' });
+  });
+
+  it('RED ks1868 R4 sign: an Error whose message getter throws becomes SIGN_FAILED with the constant reason', () => {
+    h.arm = 'sign';
+    h.toThrow = getterThrows();
+    expect(sign()).toEqual({ code: 'SIGN_FAILED', message: 'crypto.sign failed: unreadable thrown value' });
+  });
+
+  it('control ks1868 C1 key load: an ordinary Error keeps its own text in the SIGN_FAILED message', () => {
+    h.arm = 'key';
+    h.toThrow = new Error('pem boom');
+    expect(sign()).toEqual({ code: 'SIGN_FAILED', message: 'Could not load decrypted private key: pem boom' });
+  });
+
+  it('control ks1868 C2 sign: an ordinary Error keeps its own text in the SIGN_FAILED message', () => {
+    h.arm = 'sign';
+    h.toThrow = new Error('sign boom');
+    expect(sign()).toEqual({ code: 'SIGN_FAILED', message: 'crypto.sign failed: sign boom' });
+  });
+
+  it('control ks1868 C3 no failure: a normal sign returns the envelope', () => {
+    expect(sign()).toEqual({ signed: true });
+  });
+});
```

> STACKING NOTE (operator o139, 2026-11-11): this is piece 2 of 2 for issuerCert.ts. It STACKS on the held o138 piece READY_KS-1868-KS-1868-O138-P2 (parseCert 114, verifyKeyMatchesCert 199/219) for the same file: hunks do not overlap (this one is lines 344-365 at the tip; apply them in ONE PR or in order, o138 P2 first, the line numbers here are tip numbers and shift by +5 per o138 hunk above). Both diffs were each checked against the tip alone, not against each other. Wednesday: read the + lines at source before accepting.
