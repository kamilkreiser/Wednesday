# READY — KS-1868-KS-1868-O95-P5 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p5_auth_email_get_acs_client_init_catch_guard_message/out.md.checker/patch.diff`** (from `ls` at 15:08 2026-11-03; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p5_auth_email_get_acs_client_init_catch_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p5_auth_email_get_acs_client_init_catch_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p5_auth_email_get_acs_client_init_catch_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p5_auth_email_get_acs_client_init_catch_guard_message-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 15:08 2026-11-03 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p5_auth_email_get_acs_client_init_catch_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `67309f28ab2132ca7b6a45b28c731aa480642a9a`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/auth/src/services/email.ts } + { Blockchain/Dev/services/auth/src/__tests__/ks1868-email-acs-client-init-catch-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/auth/src/services/email.ts` (product) and `Blockchain/Dev/services/auth/src/__tests__/ks1868-email-acs-client-init-catch-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/auth/src/services/email.ts
111	0	Blockchain/Dev/services/auth/src/__tests__/ks1868-email-acs-client-init-catch-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: email.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/auth/src/services/email.ts`; test(s): `Blockchain/Dev/services/auth/src/__tests__/ks1868-email-acs-client-init-catch-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/auth/src/services/email.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/auth/src/__tests__/ks1868-email-acs-client-init-catch-unreadable-throw.test.ts 111 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/auth/src/services/email.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/auth/src/__tests__/ks1868-email-acs-client-init-catch-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 4 run; controls green; assertion reds)` [red_first.json: failed=2 of total=4; red cell(s): ['KS-1868 the ACS client init catch answers as for an ordinary Error and logs text for a hostile thrown value RED ks1868 R1: a constructor failure that is a revoked Proxy falls through to SMTP (true) and is logged as text, as for an ordinary Error', 'KS-1868 the ACS client init catch answers as for an ordinary Error and logs text for a hostile thrown value RED ks1868 R2: a constructor failure that is an Error whose message getter throws falls through to SMTP (true) and is logged as text, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (4 passed / 4 run)` [green_after.json: failed=0 of total=4, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1623 failed=0 | after: total=1627 failed=0` · `NEW reds: []` [baseline_suite.json total=1623 failed=0; after_suite.json total=1627 failed=0]
- A6 [verbatim]: `PASS A6 whole services/auth suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/auth: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/auth/src/services/email.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/auth/src/__tests__/ks1868-email-acs-client-init-catch-unreadable-throw.test.ts` (+111/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/auth/src/services/email.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `67309f28ab2132ca7b6a45b28c731aa480642a9a` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p5_auth_email_get_acs_client_init_catch_guard_message/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o95_p5_auth_email_get_acs_client_init_catch_guard_message/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-03_ks_1868_o95_p5_auth_email_get_acs_client_init_catch_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/auth/src/services/email.ts b/Blockchain/Dev/services/auth/src/services/email.ts
--- a/Blockchain/Dev/services/auth/src/services/email.ts
+++ b/Blockchain/Dev/services/auth/src/services/email.ts
@@ -137,7 +137,13 @@
     console.log(`[Email] ACS client initialised (sender=${ACS_SENDER_ADDRESS})`);
     return acsClient;
   } catch (err: any) {
-    console.error(`[Email] Failed to init ACS client (will fall back to SMTP): ${err?.message}`);
+    let reason: string;
+    try {
+      reason = String(err?.message);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    console.error(`[Email] Failed to init ACS client (will fall back to SMTP): ${reason}`);
     return null;
   }
 }
diff --git a/Blockchain/Dev/services/auth/src/__tests__/ks1868-email-acs-client-init-catch-unreadable-throw.test.ts b/Blockchain/Dev/services/auth/src/__tests__/ks1868-email-acs-client-init-catch-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/auth/src/__tests__/ks1868-email-acs-client-init-catch-unreadable-throw.test.ts
@@ -0,0 +1,111 @@
+import { describe, it, expect, beforeAll, beforeEach, afterAll, vi } from 'vitest';
+
+// KS-1868: getAcsClient (src/services/email.ts) builds the lazy ACS client; when the SDK import or the client constructor throws it logs
+// `[Email] Failed to init ACS client (will fall back to SMTP): ${err?.message}` and answers null, so sendEmail falls through to SMTP.
+// The message is read INSIDE the template literal, unguarded. A thrown value whose read throws (a revoked Proxy, an Error whose
+// `message` getter throws) makes the template throw INSIDE the catch, so getAcsClient and with it sendEmail REJECT instead of
+// answering what an ordinary Error gets (true, through SMTP). The cells make the ACS client constructor throw such a value and assert
+// the answer and the logged text. Harness: the real module, with the ACS SDK and nodemailer replaced by plain stand-ins (no network),
+// the provider variables set before the module is loaded, and console.error replaced by a plain function that records its arguments.
+const h = vi.hoisted(() => {
+  process.env.ACS_CONNECTION_STRING = 'endpoint=https://acs.invalid/;accesskey=k';
+  process.env.ACS_SENDER_ADDRESS = 'noreply@secuura.invalid';
+  process.env.SMTP_ENABLED = 'true';
+  process.env.SMTP_HOST = 'smtp.invalid';
+  process.env.SMTP_FROM = 'noreply@secuura.invalid';
+  delete process.env.EMAIL_RECIPIENT_ALLOWLIST;
+  return {
+    toThrow: undefined as unknown,
+    logged: [] as unknown[][],
+  };
+});
+
+vi.mock('@azure/communication-email', () => ({
+  EmailClient: class {
+    constructor() {
+      throw h.toThrow;
+    }
+  },
+}));
+vi.mock('nodemailer', () => ({
+  default: {
+    createTransport: () => ({
+      sendMail: () => Promise.resolve({ messageId: 'm1' }),
+    }),
+  },
+}));
+
+type Email = typeof import('../services/email');
+let mod: Email;
+const realError = console.error;
+const realLog = console.log;
+const realWarn = console.warn;
+beforeAll(async () => {
+  mod = await import('../services/email');
+}, 60_000);
+afterAll(() => {
+  console.error = realError;
+  console.log = realLog;
+  console.warn = realWarn;
+});
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.logged.length = 0;
+  console.log = () => undefined;
+  console.warn = () => undefined;
+  console.error = (...args: unknown[]) => {
+    h.logged.push(args);
+  };
+});
+
+async function send(): Promise<{ ok: boolean; value: boolean | undefined }> {
+  try {
+    return { ok: true, value: await mod.sendEmail({ to: 'user@example.test', subject: 's', text: 't' }) };
+  } catch {
+    return { ok: false, value: undefined };
+  }
+}
+const INIT_LINES = () => h.logged.filter((c) => typeof c[0] === 'string' && (c[0] as string).startsWith('[Email] Failed to init ACS client'));
+const INIT_PREFIX = '[Email] Failed to init ACS client (will fall back to SMTP): ';
+const textOf = (c: unknown[] | undefined): string => (typeof c?.[0] === 'string' ? (c[0] as string) : '<' + typeof c?.[0] + '>');
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
+
+describe('KS-1868 the ACS client init catch answers as for an ordinary Error and logs text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the ACS client constructor falls through to SMTP (true) and is logged with its message', async () => {
+    h.toThrow = new Error('acs init down');
+    expect(await send()).toEqual({ ok: true, value: true });
+    expect(INIT_LINES()).toHaveLength(1);
+    expect(textOf(INIT_LINES()[0])).toBe(INIT_PREFIX + 'acs init down');
+  });
+  it('control ks1868 C2: a thrown plain string falls through to SMTP (true) and is logged as undefined', async () => {
+    h.toThrow = 'plain boom';
+    expect(await send()).toEqual({ ok: true, value: true });
+    expect(INIT_LINES()).toHaveLength(1);
+    expect(textOf(INIT_LINES()[0])).toBe(INIT_PREFIX + 'undefined');
+  });
+  it('RED ks1868 R1: a constructor failure that is a revoked Proxy falls through to SMTP (true) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = revokedProxy();
+    expect(await send()).toEqual({ ok: true, value: true });
+    expect(INIT_LINES()).toHaveLength(1);
+    expect(textOf(INIT_LINES()[0])).toBe(INIT_PREFIX + 'unreadable thrown value');
+  });
+  it('RED ks1868 R2: a constructor failure that is an Error whose message getter throws falls through to SMTP (true) and is logged as text, as for an ordinary Error', async () => {
+    h.toThrow = getterThrows();
+    expect(await send()).toEqual({ ok: true, value: true });
+    expect(INIT_LINES()).toHaveLength(1);
+    expect(textOf(INIT_LINES()[0])).toBe(INIT_PREFIX + 'unreadable thrown value');
+  });
+});
```
