# READY — KS-1868-KS-1868-O55-P1 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p1_billing_stripe_webhook_signature_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 07:16 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p1_billing_stripe_webhook_signature_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p1_billing_stripe_webhook_signature_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p1_billing_stripe_webhook_signature_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p1_billing_stripe_webhook_signature_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 07:16 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p1_billing_stripe_webhook_signature_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `03977e89a343ad7362760e4fb0270602fb6da5ce`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/billing/src/routes/webhooks.ts } + { Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-signature-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/billing/src/routes/webhooks.ts` (product) and `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-signature-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
7	1	Blockchain/Dev/services/billing/src/routes/webhooks.ts
148	0	Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-signature-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (7 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: webhooks.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/billing/src/routes/webhooks.ts`; test(s): `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-signature-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/billing/src/routes/webhooks.ts 7 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-signature-unreadable-throw.test.ts 148 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/billing/src/routes/webhooks.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-signature-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (2 failed / 3 run; controls green; assertion reds)` [red_first.json: failed=2 of total=3; red cell(s): ['KS-1868 the Stripe webhook signature catch reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and the route answers the constant 400', 'KS-1868 the Stripe webhook signature catch reads the thrown value safely RED ks1868 R2 an Error whose message getter throws logs a constant reason and the route answers the constant 400']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (3 passed / 3 run)` [green_after.json: failed=0 of total=3, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=331 failed=0 | after: total=334 failed=0` · `NEW reds: []` [baseline_suite.json total=331 failed=0; after_suite.json total=334 failed=0]
- A6 [verbatim]: `PASS A6 whole services/billing suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/billing: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/billing/src/routes/webhooks.ts` (+7/-1 per numstat.out) and the test file `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-signature-unreadable-throw.test.ts` (+148/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/billing/src/routes/webhooks.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `03977e89a343ad7362760e4fb0270602fb6da5ce` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p1_billing_stripe_webhook_signature_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o55_p1_billing_stripe_webhook_signature_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p1_billing_stripe_webhook_signature_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/billing/src/routes/webhooks.ts b/Blockchain/Dev/services/billing/src/routes/webhooks.ts
--- a/Blockchain/Dev/services/billing/src/routes/webhooks.ts
+++ b/Blockchain/Dev/services/billing/src/routes/webhooks.ts
@@ -163,7 +163,13 @@
       const stripeService = getStripeService();
       event = stripeService.constructWebhookEvent(req.body, signature);
     } catch (error) {
-      logger.error('Webhook signature verification failed', { error: String(error) });
+      let reason: string;
+      try {
+        reason = String(error);
+      } catch {
+        reason = 'unreadable thrown value';
+      }
+      logger.error('Webhook signature verification failed', { error: reason });
       res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid signature' } });
       return;
     }
diff --git a/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-signature-unreadable-throw.test.ts b/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-signature-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-signature-unreadable-throw.test.ts
@@ -0,0 +1,148 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import express from 'express';
+import crypto from 'crypto';
+
+// KS-1868: the Stripe webhook route must still log its line and answer the constant 400 `Invalid signature` when the
+// value thrown by signature verification cannot be read (a revoked Proxy throws on `String(...)`; an Error whose
+// `message` getter throws, throws inside `String(...)`). Harness: webhooks-replay-auth.test.ts / ks1868 replay test
+// (real router on a loopback listener). `constructWebhookEvent` throws a plain function's value, not a vi.fn(): a spy
+// inspects what it throws and could itself fail on a revoked Proxy before the code under test saw it. At the tip the
+// request is never answered (Express 4 does not see an async handler's rejection), so the cell gives the request a
+// short deadline and counts the unhandled rejection itself instead of letting the runner report it.
+const { publicKey: rsaPub } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+
+process.env.NODE_ENV = 'development';
+process.env.JWT_PUBLIC_KEY = Buffer.from(rsaPub.export({ type: 'spki', format: 'pem' }).toString()).toString('base64');
+process.env.DATABASE_URL = 'postgres://test:test@localhost:5432/test';
+
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  logged: [] as unknown[][],
+  queries: 0,
+  unhandled: 0,
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: () => {
+    h.queries += 1;
+    return Promise.resolve({ rows: [], rowCount: 0 });
+  },
+}));
+
+vi.mock('../services/stripeService', () => ({
+  getStripeService: () => ({
+    addCertificationCredits: async () => 0,
+    constructWebhookEvent: () => {
+      throw h.toThrow;
+    },
+  }),
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    debug: () => undefined,
+    info: () => undefined,
+    warn: () => undefined,
+    error: (...args: unknown[]) => {
+      h.logged.push(args);
+    },
+  },
+}));
+
+const { default: webhookRoutes } = await import('../routes/webhooks');
+const { errorHandler } = await import('@secuura/shared');
+
+const app = express();
+app.use('/webhooks', express.json(), webhookRoutes);
+app.use(errorHandler);
+
+const TIMEOUT_MS = 2500;
+const SAVED_LISTENERS = process.listeners('unhandledRejection');
+const onUnhandled = () => {
+  h.unhandled += 1;
+};
+
+let baseUrl = '';
+let server: ReturnType<typeof app.listen>;
+
+beforeAll(async () => {
+  process.removeAllListeners('unhandledRejection');
+  process.on('unhandledRejection', onUnhandled);
+  await new Promise<void>((resolve) => {
+    server = app.listen(0, '127.0.0.1', () => {
+      const addr = server.address();
+      const port = typeof addr === 'object' && addr ? addr.port : 0;
+      baseUrl = `http://127.0.0.1:${port}`;
+      resolve();
+    });
+  });
+});
+
+afterAll(() => {
+  server?.close();
+  process.removeListener('unhandledRejection', onUnhandled);
+  for (const l of SAVED_LISTENERS) process.on('unhandledRejection', l as (...a: any[]) => void);
+});
+
+beforeEach(() => {
+  h.toThrow = undefined;
+  h.logged.length = 0;
+  h.queries = 0;
+  h.unhandled = 0;
+});
+
+/** undefined when the request got no answer inside the deadline. */
+async function deliver() {
+  const res = await fetch(`${baseUrl}/webhooks/stripe`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', 'stripe-signature': 't=1,v1=stub' },
+    body: JSON.stringify({ id: 'evt_ks1868_sig', type: 'customer.created' }),
+    signal: AbortSignal.timeout(TIMEOUT_MS),
+  }).catch(() => undefined);
+  if (!res) return undefined;
+  const body: any = await res.json().catch(() => undefined);
+  return { status: res.status, body };
+}
+const LINES = () => h.logged.filter((c) => c[0] === 'Webhook signature verification failed');
+const INVALID = { success: false, error: { code: 'BAD_REQUEST', message: 'Invalid signature' } };
+
+describe('KS-1868 the Stripe webhook signature catch reads the thrown value safely', () => {
+  it('control ks1868 C1 an ordinary Error still logs its text and the route answers the constant 400, touching no database', async () => {
+    h.toThrow = new Error('bad signature');
+    const res = await deliver();
+    expect(res?.status).toBe(400);
+    expect(res?.body).toEqual(INVALID);
+    expect(LINES()).toHaveLength(1);
+    expect(LINES()[0][1]).toEqual({ error: 'Error: bad signature' });
+    expect(h.queries).toBe(0);
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason and the route answers the constant 400', async () => {
+    const { proxy, revoke } = Proxy.revocable({}, {});
+    revoke();
+    h.toThrow = proxy;
+    const res = await deliver();
+    expect(res?.status).toBe(400);
+    expect(res?.body).toEqual(INVALID);
+    expect(LINES()).toHaveLength(1);
+    expect(LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+    expect(h.queries).toBe(0);
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason and the route answers the constant 400', async () => {
+    h.toThrow = Object.create(Error.prototype, {
+      message: {
+        get() {
+          throw new Error('getter boom');
+        },
+      },
+    });
+    const res = await deliver();
+    expect(res?.status).toBe(400);
+    expect(res?.body).toEqual(INVALID);
+    expect(LINES()).toHaveLength(1);
+    expect(LINES()[0][1]).toEqual({ error: 'unreadable thrown value' });
+    expect(h.queries).toBe(0);
+  });
+});
```
