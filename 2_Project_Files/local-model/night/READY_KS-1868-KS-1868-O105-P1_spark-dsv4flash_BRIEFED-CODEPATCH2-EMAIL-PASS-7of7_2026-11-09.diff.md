# READY — KS-1868-KS-1868-O105-P1 (Spark (DeepSeek V4 Flash), briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1868_o105_p1_originate_email_acs_init_acs_send_and_smtp_send_catches_guard_message/out.md.checker/patch.diff`** (from `ls` at 00:45 2026-11-09; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1868_o105_p1_originate_email_acs_init_acs_send_and_smtp_send_catches_guard_message/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1868_o105_p1_originate_email_acs_init_acs_send_and_smtp_send_catches_guard_message/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1868_o105_p1_originate_email_acs_init_acs_send_and_smtp_send_catches_guard_message/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1868_o105_p1_originate_email_acs_init_acs_send_and_smtp_send_catches_guard_message-control/out.md.checker/patch.diff` rc 0, Spark operator 105).

**Held 00:45 2026-11-09 by Spark operator 105 after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1868_o105_p1_originate_email_acs_init_acs_send_and_smtp_send_catches_guard_message/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `092d30706b9561bb7d28aeffedf1e37ba62b4cd5`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/services/email.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-email-acs-and-smtp-catches-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/services/email.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-email-acs-and-smtp-catches-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
24	3	Blockchain/Dev/services/originate/src/services/email.ts
160	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-email-acs-and-smtp-catches-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (24 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: email.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/services/email.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-email-acs-and-smtp-catches-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/services/email.ts 24 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-email-acs-and-smtp-catches-unreadable-throw.test.ts 160 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/services/email.ts` (hunks=3, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-email-acs-and-smtp-catches-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (5 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=5 of total=8; red cell(s): ['KS-1868 the email init and send catches answer false and log text for a hostile thrown value RED ks1868 R1: an ACS client constructor failure that is a revoked Proxy is logged as text and sendEmail answers false, as for an ordinary Error', 'KS-1868 the email init and send catches answer false and log text for a hostile thrown value RED ks1868 R2: an ACS send failure that is a revoked Proxy is logged as text and sendEmail answers false, as for an ordinary Error', 'KS-1868 the email init and send catches answer false and log text for a hostile thrown value RED ks1868 R3: an ACS send failure that is an Error whose message is a Symbol is logged as text and sendEmail answers false, as for an ordinary Error', 'KS-1868 the email init and send catches answer false and log text for a hostile thrown value RED ks1868 R4: an SMTP send failure that is a revoked Proxy is logged as text and sendEmail answers false, as for an ordinary Error', 'KS-1868 the email init and send catches answer false and log text for a hostile thrown value RED ks1868 R5: an SMTP send failure that is an Error whose message getter throws is logged as text and sendEmail answers false, as for an ordinary Error']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=2592 failed=11 | after: total=2600 failed=11` · `NEW reds: []` [baseline_suite.json total=2592 failed=11; after_suite.json total=2600 failed=11]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/services/email.ts` (+24/-3 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-email-acs-and-smtp-catches-unreadable-throw.test.ts` (+160/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/services/email.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `092d30706b9561bb7d28aeffedf1e37ba62b4cd5` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1868_o105_p1_originate_email_acs_init_acs_send_and_smtp_send_catches_guard_message/input.json`. brief NOT LOCATED under night/briefs/ (no claim made). Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_1868_o105_p1_originate_email_acs_init_acs_send_and_smtp_send_catches_guard_message/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/services/email.ts b/Blockchain/Dev/services/originate/src/services/email.ts
--- a/Blockchain/Dev/services/originate/src/services/email.ts
+++ b/Blockchain/Dev/services/originate/src/services/email.ts
@@ -136,7 +136,14 @@
     console.log(`[Email] ACS client initialised (sender=${ACS_SENDER_ADDRESS})`);
     return acsClient;
   } catch (err: any) {
-    console.error(`[Email] Failed to init ACS client (will fall back to SMTP): ${err?.message}`);
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    console.error(`[Email] Failed to init ACS client (will fall back to SMTP): ${reason}`);
     return null;
   }
 }
@@ -164,7 +171,14 @@
     console.error(`[Email/ACS] Send failed: status=${result.status}`, result.error);
     return false;
   } catch (err: any) {
-    console.error(`[Email/ACS] Send threw: ${err?.message}`);
+    let reason: string | null | undefined;
+    try {
+      const m = err?.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    console.error(`[Email/ACS] Send threw: ${reason}`);
     return false;
   }
 }
@@ -207,7 +221,14 @@
     console.log(`[Email/SMTP] Sent: ${options.subject} (messageId: ${info.messageId})`);
     return true;
   } catch (error: any) {
-    console.error(`[Email/SMTP] Failed to send: ${error.message}`);
+    let reason: string | null | undefined;
+    try {
+      const m = error.message;
+      reason = m === undefined || m === null ? m : String(m);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
+    console.error(`[Email/SMTP] Failed to send: ${reason}`);
     return false;
   }
 }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-email-acs-and-smtp-catches-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-email-acs-and-smtp-catches-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-originate-email-acs-and-smtp-catches-unreadable-throw.test.ts
@@ -0,0 +1,160 @@
+// KS-1868 (operator 91 screen, originate email service): the ACS-client init catch of getAcsClient (line 139), the ACS send catch
+// of sendViaAcs (line 167) and the SMTP send catch of sendEmail (line 210) of services/originate/src/services/email.ts interpolate
+// `err?.message` / `error.message` into a console.error template, unguarded. A thrown value whose read throws (a revoked Proxy, an
+// Error whose message getter throws) makes the catch itself throw: sendEmail REJECTS instead of logging and answering false (its
+// contract: "Returns true if delivered to a provider successfully"; every caller treats false as not sent); an Error whose
+// message is not a string (a Symbol) makes the template literal throw. The cells make the ACS client constructor, the ACS send or
+// the SMTP send throw such a value and assert sendEmail resolves false and the logged line carries text (the constant when the value
+// cannot be turned into text). Harness: the real module with nodemailer, @azure/communication-email and the shared package
+// replaced by plain stand-ins and console.error by a plain recording function (no network, no mail).
+const mockH: { mode: 'acsinit' | 'acssend' | 'smtp'; toThrow: unknown; errors: unknown[][] } = { mode: 'smtp', toThrow: undefined, errors: [] };
+
+jest.mock('@secuura/shared', () =>
+  require('./helpers/sharedModuleMock').makeSharedMock({
+    parseRecipientAllowlist: () => undefined,
+    isRecipientAllowed: () => true,
+    sanitizeHeaderText: (s: string) => s,
+    escapeHtmlText: (s: string) => s,
+  }),
+);
+jest.mock('nodemailer', () => ({
+  __esModule: true,
+  default: {
+    createTransport: () => ({
+      sendMail: async () => {
+        throw mockH.toThrow;
+      },
+    }),
+  },
+}));
+jest.mock(
+  '@azure/communication-email',
+  () => ({
+    EmailClient: function EmailClientMock() {
+      if (mockH.mode === 'acsinit') throw mockH.toThrow;
+      return {
+        beginSend: async () => {
+          throw mockH.toThrow;
+        },
+      };
+    },
+  }),
+  { virtual: true },
+);
+
+const TO = 'rcpt@example.test';
+const P_INIT = '[Email] Failed to init ACS client (will fall back to SMTP): ';
+const P_ACS = '[Email/ACS] Send threw: ';
+const P_SMTP = '[Email/SMTP] Failed to send: ';
+const ENV_KEYS = ['ACS_CONNECTION_STRING', 'ACS_SENDER_ADDRESS', 'SMTP_ENABLED', 'SMTP_HOST', 'SMTP_FROM', 'EMAIL_FROM', 'EMAIL_RECIPIENT_ALLOWLIST'];
+const savedEnv: Record<string, string | undefined> = {};
+const realError = console.error;
+const realLog = console.log;
+const realWarn = console.warn;
+
+beforeEach(() => {
+  mockH.toThrow = undefined;
+  mockH.errors.length = 0;
+  for (const k of ENV_KEYS) {
+    savedEnv[k] = process.env[k];
+    delete process.env[k];
+  }
+  console.error = (...args: unknown[]) => {
+    mockH.errors.push(args);
+  };
+  console.log = () => undefined;
+  console.warn = () => undefined;
+});
+afterEach(() => {
+  console.error = realError;
+  console.log = realLog;
+  console.warn = realWarn;
+  for (const k of ENV_KEYS) {
+    if (savedEnv[k] === undefined) delete process.env[k];
+    else process.env[k] = savedEnv[k];
+  }
+});
+
+type Mail = typeof import('../services/email');
+async function send(mode: 'acsinit' | 'acssend' | 'smtp', value: unknown): Promise<{ ok: boolean; sent: boolean }> {
+  mockH.mode = mode;
+  mockH.toThrow = value;
+  if (mode === 'smtp') {
+    process.env.SMTP_ENABLED = 'true';
+    process.env.SMTP_HOST = 'smtp.invalid';
+    process.env.SMTP_FROM = 'noreply@example.test';
+  } else {
+    process.env.ACS_CONNECTION_STRING = 'endpoint=https://acs.invalid/;accesskey=stub';
+    process.env.ACS_SENDER_ADDRESS = 'donotreply@example.test';
+  }
+  jest.resetModules();
+  // eslint-disable-next-line @typescript-eslint/no-require-imports
+  const mail = require('../services/email') as Mail;
+  try {
+    return { ok: true, sent: await mail.sendEmail({ to: TO, subject: 'subject', text: 'text' }) };
+  } catch {
+    return { ok: false, sent: false };
+  }
+}
+const LINES = (prefix: string) => mockH.errors.filter((a) => typeof a[0] === 'string' && (a[0] as string).startsWith(prefix));
+/** The text after the prefix of the logged line. */
+const reasonOf = (a: unknown[] | undefined, prefix: string): string => (a ? (a[0] as string).slice(prefix.length) : '<none>');
+
+const revokedProxy = (): unknown => {
+  const rp = Proxy.revocable({}, {});
+  rp.revoke();
+  return rp.proxy;
+};
+/** An Error whose `message` getter succeeds and returns the value m. */
+const withMessage = (m: unknown): unknown => Object.create(Error.prototype, { message: { get() { return m; } } });
+const getterThrows = (): unknown =>
+  Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+
+describe('KS-1868 the email init and send catches answer false and log text for a hostile thrown value', () => {
+  it('control ks1868 C1: an ordinary Error from the ACS client constructor is logged with its message and sendEmail answers false', async () => {
+    expect(await send('acsinit', new Error('acs ctor boom'))).toEqual({ ok: true, sent: false });
+    expect(LINES(P_INIT)).toHaveLength(1);
+    expect(reasonOf(LINES(P_INIT)[0], P_INIT)).toBe('acs ctor boom');
+  });
+  it('control ks1868 C2: an ordinary Error from the ACS send is logged with its message and sendEmail answers false', async () => {
+    expect(await send('acssend', new Error('acs send boom'))).toEqual({ ok: true, sent: false });
+    expect(LINES(P_ACS)).toHaveLength(1);
+    expect(reasonOf(LINES(P_ACS)[0], P_ACS)).toBe('acs send boom');
+  });
+  it('control ks1868 C3: an ordinary Error from the SMTP send is logged with its message and sendEmail answers false', async () => {
+    expect(await send('smtp', new Error('smtp boom'))).toEqual({ ok: true, sent: false });
+    expect(LINES(P_SMTP)).toHaveLength(1);
+    expect(reasonOf(LINES(P_SMTP)[0], P_SMTP)).toBe('smtp boom');
+  });
+  it('RED ks1868 R1: an ACS client constructor failure that is a revoked Proxy is logged as text and sendEmail answers false, as for an ordinary Error', async () => {
+    expect(await send('acsinit', revokedProxy())).toEqual({ ok: true, sent: false });
+    expect(LINES(P_INIT)).toHaveLength(1);
+    expect(reasonOf(LINES(P_INIT)[0], P_INIT)).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R2: an ACS send failure that is a revoked Proxy is logged as text and sendEmail answers false, as for an ordinary Error', async () => {
+    expect(await send('acssend', revokedProxy())).toEqual({ ok: true, sent: false });
+    expect(LINES(P_ACS)).toHaveLength(1);
+    expect(reasonOf(LINES(P_ACS)[0], P_ACS)).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R3: an ACS send failure that is an Error whose message is a Symbol is logged as text and sendEmail answers false, as for an ordinary Error', async () => {
+    expect(await send('acssend', withMessage(Symbol('ks1868')))).toEqual({ ok: true, sent: false });
+    expect(LINES(P_ACS)).toHaveLength(1);
+    expect(reasonOf(LINES(P_ACS)[0], P_ACS)).toBe('Symbol(ks1868)');
+  });
+  it('RED ks1868 R4: an SMTP send failure that is a revoked Proxy is logged as text and sendEmail answers false, as for an ordinary Error', async () => {
+    expect(await send('smtp', revokedProxy())).toEqual({ ok: true, sent: false });
+    expect(LINES(P_SMTP)).toHaveLength(1);
+    expect(reasonOf(LINES(P_SMTP)[0], P_SMTP)).toBe('unreadable thrown value');
+  });
+  it('RED ks1868 R5: an SMTP send failure that is an Error whose message getter throws is logged as text and sendEmail answers false, as for an ordinary Error', async () => {
+    expect(await send('smtp', getterThrows())).toEqual({ ok: true, sent: false });
+    expect(LINES(P_SMTP)).toHaveLength(1);
+    expect(reasonOf(LINES(P_SMTP)[0], P_SMTP)).toBe('unreadable thrown value');
+  });
+});
```
