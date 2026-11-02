# READY — KS-1868-KS-1868-O91-P7 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p7_tokenisation_vault_detokenise_decrypt_failed_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 07:33 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p7_tokenisation_vault_detokenise_decrypt_failed_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p7_tokenisation_vault_detokenise_decrypt_failed_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p7_tokenisation_vault_detokenise_decrypt_failed_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p7_tokenisation_vault_detokenise_decrypt_failed_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 07:33 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p7_tokenisation_vault_detokenise_decrypt_failed_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/tokenisation/src/vault.ts } + { Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-detokenise-decrypt-failed-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/tokenisation/src/vault.ts` (product) and `Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-detokenise-decrypt-failed-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/tokenisation/src/vault.ts
112	0	Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-detokenise-decrypt-failed-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: vault.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/tokenisation/src/vault.ts`; test(s): `Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-detokenise-decrypt-failed-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/tokenisation/src/vault.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-detokenise-decrypt-failed-catch-unreadable-throw.test.ts 112 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/tokenisation/src/vault.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-detokenise-decrypt-failed-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 6 run; controls green; assertion reds)` [red_first.json: failed=3 of total=6; red cell(s): ['KS-1868 the detokenise decrypt-failed catch answers a null entry and logs text for a hostile thrown value RED ks1868 R1: a decrypt failure that is a revoked Proxy is logged as text and the entry answers null, as for an ordinary Error', 'KS-1868 the detokenise decrypt-failed catch answers a null entry and logs text for a hostile thrown value RED ks1868 R2: a decrypt failure that is an Error whose message getter throws is logged as text and the entry answers null, as for an ordinary Error', 'KS-1868 the detokenise decrypt-failed catch answers a null entry and logs text for a hostile thrown value RED ks1868 R3: a decrypt failure with no message whose String() conversion throws is logged as text and the entry answers null, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (6 passed / 6 run)` [green_after.json: failed=0 of total=6, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=8 failed=0 | after: total=14 failed=0` · `NEW reds: []` [baseline_suite.json total=8 failed=0; after_suite.json total=14 failed=0]
- A6 [verbatim]: `PASS A6 whole services/tokenisation suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/tokenisation: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/tokenisation/src/vault.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-detokenise-decrypt-failed-catch-unreadable-throw.test.ts` (+112/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/tokenisation/src/vault.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `7ad0dcc14e5c565be7d7dbd0d24a357f3c3b06b6` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p7_tokenisation_vault_detokenise_decrypt_failed_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o91_p7_tokenisation_vault_detokenise_decrypt_failed_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o91_p7_tokenisation_vault_detokenise_decrypt_failed_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/tokenisation/src/vault.ts b/Blockchain/Dev/services/tokenisation/src/vault.ts
--- a/Blockchain/Dev/services/tokenisation/src/vault.ts
+++ b/Blockchain/Dev/services/tokenisation/src/vault.ts
@@ -76,9 +76,15 @@
       // the token is the lookup key and is auditable in the vault_entries
       // table directly).
       const tokenHash = require('node:crypto').createHash('sha256').update(tok).digest('hex').slice(0, 16);
+      let reason: string;
+      try {
+        reason = (err as Error)?.message ?? String(err);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
       // eslint-disable-next-line no-console
       console.error('[tokenisation/vault] decrypt failed', {
-        tenantId, tokenHash, error: (err as Error)?.message ?? String(err),
+        tenantId, tokenHash, error: reason,
       });
       return { token: tok, value: null };
     }
diff --git a/Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-detokenise-decrypt-failed-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-detokenise-decrypt-failed-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/tokenisation/src/__tests__/ks1868-tokenisation-detokenise-decrypt-failed-catch-unreadable-throw.test.ts
@@ -0,0 +1,112 @@
+import { describe, it, expect, beforeEach, afterAll, vi } from 'vitest';
+
+// KS-1868 (operator 91 screen, tokenisation vault): the decrypt-failed catch of detokenise (line 81) of
+// services/tokenisation/src/vault.ts reads `(err as Error)?.message ?? String(err)` inside console.error's arguments, unguarded.
+// A thrown value whose read throws (a revoked Proxy, an Error whose message getter throws, a value whose message is absent and
+// whose String() conversion throws) makes the catch itself throw: the line is never logged and detokenise REJECTS for the whole
+// batch instead of answering `value: null` for the entry that could not be decrypted, as an ordinary Error does. The cells make
+// the decrypt step throw such a value and assert detokenise resolves with the null entry and the logged value is text (the
+// constant when the value cannot be read). Harness: the real vault module with ./db and ./crypto replaced by plain stand-ins (the
+// query answers one vault row; decrypt throws the value) and console.error replaced by a plain recording function (no database).
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  errors: [] as unknown[][],
+}));
+
+vi.mock('../db.js', () => ({
+  query: async () => ({
+    rows: [{ token: 'tok_1', encrypted_value: Buffer.from('x'), iv: 'iv', auth_tag: Buffer.from('t') }],
+  }),
+}));
+
+vi.mock('../crypto.js', () => ({
+  encrypt: () => ({ ciphertext: Buffer.from('x'), iv: 'iv', authTag: Buffer.from('t') }),
+  generateToken: () => 'tok_generated',
+  decrypt: () => {
+    throw h.toThrow;
+  },
+}));
+
+import { detokenise } from '../vault.js';
+
+const FAILED = '[tokenisation/vault] decrypt failed';
+const realError = console.error;
+afterAll(() => {
+  console.error = realError;
+});
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.errors.length = 0;
+  console.error = (...args: unknown[]) => {
+    h.errors.push(args);
+  };
+});
+
+async function run(value: unknown): Promise<{ ok: boolean; answer: string }> {
+  h.toThrow = value;
+  try {
+    const out = await detokenise('tenant-1', ['tok_1'], 'a2V5');
+    return { ok: true, answer: out.map((o) => o.token + ':' + String(o.value)).join(',') };
+  } catch {
+    return { ok: false, answer: '' };
+  }
+}
+const LINES = () => h.errors.filter((a) => a[0] === FAILED);
+/** The logged `error` field as a string; the type name when it is not one (a hostile value never reaches an assertion). */
+const reasonOf = (a: unknown[] | undefined): string => {
+  const v = (a?.[1] as { error?: unknown } | undefined)?.error;
+  return typeof v === 'string' ? v : '<' + typeof v + '>';
+};
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+/** A value with no message whose String() conversion throws. */
+const stringThrows = (): unknown => ({
+  toString() {
+    throw new Error('toString boom');
+  },
+});
+
+describe('KS-1868 the detokenise decrypt-failed catch answers a null entry and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from decrypt is logged with its message and the entry answers null', async () => {
+    expect(await run(new Error('bad auth tag'))).toEqual({ ok: true, answer: 'tok_1:null' });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('bad auth tag');
+  });
+  it('control ks1868 C2: a thrown plain string from decrypt is logged as its text and the entry answers null', async () => {
+    expect(await run('plain boom')).toEqual({ ok: true, answer: 'tok_1:null' });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('plain boom');
+  });
+  it('control ks1868 C3: an Error with an empty message is logged with the empty text and the entry answers null', async () => {
+    expect(await run(new Error(''))).toEqual({ ok: true, answer: 'tok_1:null' });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('');
+  });
+  it('RED ks1868 R1: a decrypt failure that is a revoked Proxy is logged as text and the entry answers null, as for an ordinary Error', async () => {
+    expect(await run(revokedProxy())).toEqual({ ok: true, answer: 'tok_1:null' });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: a decrypt failure that is an Error whose message getter throws is logged as text and the entry answers null, as for an ordinary Error', async () => {
+    expect(await run(getterThrows())).toEqual({ ok: true, answer: 'tok_1:null' });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: a decrypt failure with no message whose String() conversion throws is logged as text and the entry answers null, as for an ordinary Error', async () => {
+    expect(await run(stringThrows())).toEqual({ ok: true, answer: 'tok_1:null' });
+    expect(LINES()).toHaveLength(1);
+    expect(reasonOf(LINES()[0])).toBe('unreadable thrown value');
+  });
+});
```
