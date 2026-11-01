# READY — KS-1868-KS-1868-O68-P1 (spark-dsv4flash, briefed, code_patch2, jest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p1_originate_notification_client_two_catches_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 09:30 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p1_originate_notification_client_two_catches_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p1_originate_notification_client_two_catches_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p1_originate_notification_client_two_catches_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p1_originate_notification_client_two_catches_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 09:30 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p1_originate_notification_client_two_catches_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `cde2dee4dffba6a61228c40d641ff567660c32b2`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/originate/src/utils/notificationClient.ts } + { Blockchain/Dev/services/originate/src/__tests__/ks1868-notification-client-catches-p1-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/originate/src/utils/notificationClient.ts` (product) and `Blockchain/Dev/services/originate/src/__tests__/ks1868-notification-client-catches-p1-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
14	2	Blockchain/Dev/services/originate/src/utils/notificationClient.ts
138	0	Blockchain/Dev/services/originate/src/__tests__/ks1868-notification-client-catches-p1-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (14 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: notificationClient.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/originate/src/utils/notificationClient.ts`; test(s): `Blockchain/Dev/services/originate/src/__tests__/ks1868-notification-client-catches-p1-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/originate/src/utils/notificationClient.ts 14 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/originate/src/__tests__/ks1868-notification-client-catches-p1-unreadable-throw.test.ts 138 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/originate/src/utils/notificationClient.ts` (hunks=2, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/originate/src/__tests__/ks1868-notification-client-catches-p1-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (4 failed / 8 run; controls green; assertion reds)` [red_first.json: failed=4 of total=8; red cell(s): ['KS-1868 notificationClient reads the thrown value safely RED ks1868 R1 service call: a revoked Proxy is logged as a constant reason, the SMTP fallback still runs and the call resolves', 'KS-1868 notificationClient reads the thrown value safely RED ks1868 R2 service call: an Error whose message getter throws is logged as a constant reason, the SMTP fallback still runs and the call resolves', 'KS-1868 notificationClient reads the thrown value safely RED ks1868 R3 SMTP fallback: a revoked Proxy thrown by the send is logged as a constant reason and the call resolves', 'KS-1868 notificationClient reads the thrown value safely RED ks1868 R4 SMTP fallback: an Error whose message getter throws is logged as a constant reason and the call resolves']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (8 passed / 8 run)` [green_after.json: failed=0 of total=8, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=1999 failed=0 | after: total=2007 failed=0` · `NEW reds: []` [baseline_suite.json total=1999 failed=0; after_suite.json total=2007 failed=0]
- A6 [verbatim]: `PASS A6 whole services/originate suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/originate: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/originate/src/utils/notificationClient.ts` (+14/-2 per numstat.out) and the test file `Blockchain/Dev/services/originate/src/__tests__/ks1868-notification-client-catches-p1-unreadable-throw.test.ts` (+138/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/originate/src/utils/notificationClient.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `cde2dee4dffba6a61228c40d641ff567660c32b2` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p1_originate_notification_client_two_catches_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o68_p1_originate_notification_client_two_catches_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o68_p1_originate_notification_client_two_catches_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/originate/src/utils/notificationClient.ts b/Blockchain/Dev/services/originate/src/utils/notificationClient.ts
--- a/Blockchain/Dev/services/originate/src/utils/notificationClient.ts
+++ b/Blockchain/Dev/services/originate/src/utils/notificationClient.ts
@@ -51,9 +51,15 @@
       logger.info('Notification sent via service', { template: payload.template, to: payload.to });
     }
   } catch (err) {
+    let reason: string;
+    try {
+      reason = String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     logger.warn('Notification service unreachable, falling back to SMTP', {
       template: payload.template,
-      error: String(err),
+      error: reason,
     });
     await sendSmtpFallback(payload);
   }
@@ -105,9 +111,15 @@
     }
     logger.info('Notification sent via SMTP fallback', { template, to });
   } catch (err) {
+    let reason: string;
+    try {
+      reason = String(err);
+    } catch {
+      reason = 'unreadable thrown value';
+    }
     logger.warn('SMTP fallback also failed (non-blocking)', {
       template: payload.template,
-      error: String(err),
+      error: reason,
     });
   }
 }
diff --git a/Blockchain/Dev/services/originate/src/__tests__/ks1868-notification-client-catches-p1-unreadable-throw.test.ts b/Blockchain/Dev/services/originate/src/__tests__/ks1868-notification-client-catches-p1-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/originate/src/__tests__/ks1868-notification-client-catches-p1-unreadable-throw.test.ts
@@ -0,0 +1,138 @@
+// KS-1868 (originate utils/notificationClient.ts): two catch blocks log the thrown value as `error: String(err)`. String() on a revoked Proxy throws a TypeError, and on an Error whose `message` getter
+// throws it throws too, so the read threw INSIDE the catch. (A) In sendNotification the catch is the "notification service unreachable" path: the throw happened BEFORE the SMTP fallback line, so the
+// notification was DROPPED (no email) and the returned promise rejected although the file promises "failures are logged but never thrown". (B) In sendSmtpFallback the catch is the "SMTP fallback also
+// failed (non-blocking)" path: the throw made the fallback reject. Each catch now reads the same String(err) into a local inside its own try and logs the constant `unreadable thrown value` when it cannot
+// be read; an ordinary Error and a string log exactly what they logged before. The service stand-ins are plain functions; the outcome is read through `.then(() => 'resolved', () => 'REJECTED')` so a
+// rejection carrying a revoked Proxy is a red assertion and never a formatted-matcher crash.
+const mockLoggerWarn = jest.fn();
+const mockLoggerInfo = jest.fn();
+const mockFetch = jest.fn();
+const mockIsEmailConfigured = jest.fn();
+const mockSendCertification = jest.fn();
+
+jest.mock('../utils/logger', () => ({
+  logger: { info: mockLoggerInfo, warn: mockLoggerWarn, error: jest.fn(), debug: jest.fn() },
+}));
+
+jest.mock('../services/email', () => ({
+  sendEmail: jest.fn(),
+  sendCertificationNotification: mockSendCertification,
+  sendRevocationNotification: jest.fn(),
+  sendShareNotification: jest.fn(),
+  isEmailConfigured: mockIsEmailConfigured,
+}));
+
+import { notifyDocumentCertified } from '../utils/notificationClient';
+
+const PARAMS = {
+  toEmail: 'holder@example.test',
+  documentTitle: 'ks1868 title',
+  certifierName: 'ks1868 certifier',
+  certificationId: 'cert-ks1868',
+  certifiedAt: '2026-11-02T00:00:00Z',
+};
+
+beforeEach(() => {
+  jest.clearAllMocks();
+  (globalThis as any).fetch = mockFetch;
+  mockIsEmailConfigured.mockReturnValue(true);
+  mockSendCertification.mockResolvedValue(undefined);
+});
+
+async function outcome(): Promise<'resolved' | 'REJECTED'> {
+  return notifyDocumentCertified(PARAMS).then(
+    () => 'resolved' as const,
+    () => 'REJECTED' as const,
+  );
+}
+
+// Site A: the notification service call itself rejects with the thrown value.
+async function serviceDownWith(thrown: unknown): Promise<'resolved' | 'REJECTED'> {
+  mockFetch.mockRejectedValueOnce(thrown);
+  return outcome();
+}
+
+// Site B: the service is down with an ordinary Error, so the SMTP fallback runs, and the SMTP send rejects with the thrown value.
+async function smtpDownWith(thrown: unknown): Promise<'resolved' | 'REJECTED'> {
+  mockFetch.mockRejectedValueOnce(new Error('ks1868 service down'));
+  mockSendCertification.mockRejectedValueOnce(thrown);
+  return outcome();
+}
+
+function revokedProxy(): object {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+}
+
+function throwingMessageError(): Error {
+  const e = new Error('ks1868 hidden');
+  Object.defineProperty(e, 'message', {
+    get() {
+      throw new Error('ks1868 message getter');
+    },
+  });
+  return e;
+}
+
+const UNREACHABLE = 'Notification service unreachable, falling back to SMTP';
+const SMTP_FAILED = 'SMTP fallback also failed (non-blocking)';
+const TEMPLATE = { template: 'document_certified' };
+
+describe('KS-1868 notificationClient reads the thrown value safely', () => {
+  it('RED ks1868 R1 service call: a revoked Proxy is logged as a constant reason, the SMTP fallback still runs and the call resolves', async () => {
+    expect(await serviceDownWith(revokedProxy())).toBe('resolved');
+    expect(mockLoggerWarn.mock.calls).toEqual([[UNREACHABLE, { ...TEMPLATE, error: 'unreadable thrown value' }]]);
+    expect(mockSendCertification).toHaveBeenCalledTimes(1);
+  });
+
+  it('RED ks1868 R2 service call: an Error whose message getter throws is logged as a constant reason, the SMTP fallback still runs and the call resolves', async () => {
+    expect(await serviceDownWith(throwingMessageError())).toBe('resolved');
+    expect(mockLoggerWarn.mock.calls).toEqual([[UNREACHABLE, { ...TEMPLATE, error: 'unreadable thrown value' }]]);
+    expect(mockSendCertification).toHaveBeenCalledTimes(1);
+  });
+
+  it('control ks1868 C1 service call: an ordinary Error is logged as String(err), the SMTP fallback runs and the call resolves', async () => {
+    expect(await serviceDownWith(new Error('ks1868 ordinary'))).toBe('resolved');
+    expect(mockLoggerWarn.mock.calls).toEqual([[UNREACHABLE, { ...TEMPLATE, error: 'Error: ks1868 ordinary' }]]);
+    expect(mockSendCertification).toHaveBeenCalledTimes(1);
+  });
+
+  it('control ks1868 C2 service call: a thrown string is logged as itself, as before', async () => {
+    expect(await serviceDownWith('ks1868 plain string')).toBe('resolved');
+    expect(mockLoggerWarn.mock.calls).toEqual([[UNREACHABLE, { ...TEMPLATE, error: 'ks1868 plain string' }]]);
+    expect(mockSendCertification).toHaveBeenCalledTimes(1);
+  });
+
+  it('RED ks1868 R3 SMTP fallback: a revoked Proxy thrown by the send is logged as a constant reason and the call resolves', async () => {
+    expect(await smtpDownWith(revokedProxy())).toBe('resolved');
+    expect(mockLoggerWarn.mock.calls).toEqual([
+      [UNREACHABLE, { ...TEMPLATE, error: 'Error: ks1868 service down' }],
+      [SMTP_FAILED, { ...TEMPLATE, error: 'unreadable thrown value' }],
+    ]);
+  });
+
+  it('RED ks1868 R4 SMTP fallback: an Error whose message getter throws is logged as a constant reason and the call resolves', async () => {
+    expect(await smtpDownWith(throwingMessageError())).toBe('resolved');
+    expect(mockLoggerWarn.mock.calls).toEqual([
+      [UNREACHABLE, { ...TEMPLATE, error: 'Error: ks1868 service down' }],
+      [SMTP_FAILED, { ...TEMPLATE, error: 'unreadable thrown value' }],
+    ]);
+  });
+
+  it('control ks1868 C3 SMTP fallback: an ordinary Error is logged as String(err) and the call resolves', async () => {
+    expect(await smtpDownWith(new Error('ks1868 smtp ordinary'))).toBe('resolved');
+    expect(mockLoggerWarn.mock.calls).toEqual([
+      [UNREACHABLE, { ...TEMPLATE, error: 'Error: ks1868 service down' }],
+      [SMTP_FAILED, { ...TEMPLATE, error: 'Error: ks1868 smtp ordinary' }],
+    ]);
+  });
+
+  it('control ks1868 C4 SMTP fallback: a thrown string is logged as itself, as before', async () => {
+    expect(await smtpDownWith('ks1868 smtp string')).toBe('resolved');
+    expect(mockLoggerWarn.mock.calls).toEqual([
+      [UNREACHABLE, { ...TEMPLATE, error: 'Error: ks1868 service down' }],
+      [SMTP_FAILED, { ...TEMPLATE, error: 'ks1868 smtp string' }],
+    ]);
+  });
+});
```
