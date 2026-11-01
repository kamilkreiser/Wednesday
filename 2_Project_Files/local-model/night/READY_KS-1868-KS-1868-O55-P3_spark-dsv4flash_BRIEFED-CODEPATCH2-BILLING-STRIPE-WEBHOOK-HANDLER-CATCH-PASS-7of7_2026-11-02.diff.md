# READY — KS-1868-KS-1868-O55-P3 (spark-dsv4flash, briefed, code_patch2, vitest) — PASS 7/7 — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p3_billing_stripe_webhook_handler_unreadable_throw/out.md.checker/patch.diff`** (from `ls` at 07:21 2026-11-02; it is `cat` of the section files in order: `cmp` rc 0: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p3_billing_stripe_webhook_handler_unreadable_throw/out.md.checker/section_1.diff`, `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p3_billing_stripe_webhook_handler_unreadable_throw/out.md.checker/section_2.diff`). Checker A2 (verbatim from checker.out): `PASS A2 diff applies at the tip (strict git apply --check, every section, hunk headers consistent)`; the run's patch is BYTE-IDENTICAL to the drafter's golden (`cmp -s /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p3_billing_stripe_webhook_handler_unreadable_throw/out.md.checker/patch.diff /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p3_billing_stripe_webhook_handler_unreadable_throw-control/out.md.checker/patch.diff` rc 0, Wednesday).

**Held 07:21 2026-11-02 by Wednesday after a source read (hold_ready.py, code_patch path — every clause below is COPIED from the checker's own artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p3_billing_stripe_webhook_handler_unreadable_throw/out.md.checker`, not typed; the artefact each came from is named in brackets).** Tip `03977e89a343ad7362760e4fb0270602fb6da5ce`.
- Touched-file set [checker.out A3, verbatim]: `PASS A3 (code_patch2) touched-file set == the declared set: { Blockchain/Dev/services/billing/src/routes/webhooks.ts } + { Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts }`
- Declared set [input.json product_file + suggested_test_file]: `Blockchain/Dev/services/billing/src/routes/webhooks.ts` (product) and `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts` (test) — equal to numstat.out's set (2 files).
- numstat [out.md.checker/numstat.out, verbatim]:
```
6	1	Blockchain/Dev/services/billing/src/routes/webhooks.ts
227	0	Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts
```
- Product hunk `+` count [checker.out A3c, verbatim]: `PASS A3c every '+' line the brief adds is in the declared sections (6 line(s), multiset), and no tip line is re-added as a '+' in any product (A3d)` — no expected_plus in the input; not re-measured here.
- Byte-exactness [checker.out A3i, verbatim]: `A3i: brief '+' lines byte-exact incl. leading whitespace in: webhooks.ts`
- CODE_PATCH2 (rung 3, 1 product files + 1 test file(s)) — identity was PER-FILE A3x, not a single-file A3i. Product files (brief `File:` lines == input.json product_files): `Blockchain/Dev/services/billing/src/routes/webhooks.ts`; test(s): `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts`. [checker.out PASS A3x, verbatim]: `PASS A3x every declared file's '+' lines are byte-identical to the brief's, in order (SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0)`. [brief_bytes.out, verbatim]: `OK Blockchain/Dev/services/billing/src/routes/webhooks.ts 6 '+' line(s) byte-identical to the brief, in order; OK Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts 227 '+' line(s) byte-identical to the brief, in order; SUMMARY declared=2 measured=2 ok=2 diff=0 unmeasured=0`
- Hunk audit [out.md.checker/hunk_audit.out, first line verbatim]: `sections=2 miscounted_sections=0`
- Sections [out.md.checker/sections.json + section_<k>.opts + apply_check_strict_<k>.out]:
- section 1 `section_1.diff` → `Blockchain/Dev/services/billing/src/routes/webhooks.ts` (hunks=1, miscount=0; applied file per `section_1.opts`: `section_1.diff`, git-apply options: `(none — strict)`; `apply_check_strict_1.out`: EMPTY (strict apply --check clean))
- section 2 `section_2.diff` → `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts` (hunks=1, miscount=0; applied file per `section_2.opts`: `section_2.diff`, git-apply options: `(none — strict)`; `apply_check_strict_2.out`: EMPTY (strict apply --check clean))
- RED-FIRST [checker.out A4, verbatim]: `PASS A4 RED-FIRST: the declared test(s) fail with every test section and no product section (3 failed / 5 run; controls green; assertion reds)` [red_first.json: failed=3 of total=5; red cell(s): ['KS-1868 the Stripe webhook handler catch reads the thrown value safely RED ks1868 R1 a revoked Proxy thrown value logs a constant reason, releases the claim and answers the constant 500', 'KS-1868 the Stripe webhook handler catch reads the thrown value safely RED ks1868 R2 an Error whose message getter throws logs a constant reason, releases the claim and answers the constant 500', 'KS-1868 the Stripe webhook handler catch reads the thrown value safely RED ks1868 R3 after an unreadable thrown value the redelivery is processed, not acknowledged as a duplicate']]
- GREEN-AFTER [checker.out A5, verbatim]: `PASS A5 GREEN-AFTER: every declared test passes with all 1 product section(s) (5 passed / 5 run)` [green_after.json: failed=0 of total=5, success=True]
- Whole suite [out.md.checker/suite_delta.out, verbatim]: `baseline: total=331 failed=0 | after: total=336 failed=0` · `NEW reds: []` [baseline_suite.json total=331 failed=0; after_suite.json total=336 failed=0]
- A6 [verbatim]: `PASS A6 whole services/billing suite: no NEW red vs the untouched tip` · A7 [verbatim]: `PASS A7 tsc --noEmit for services/billing: rc 0 after the patch (baseline rc=0)`
- SUMMARY [checker.out, verbatim]: `SUMMARY files=2 products=1 tests=1 red_first=yes apply_mode=strict`

**PR NOTES for the raise seat:** CODE_PATCH — PRODUCT BYTES CHANGE: `Blockchain/Dev/services/billing/src/routes/webhooks.ts` (+6/-1 per numstat.out) and the test file `Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts` (+227/-0); 2 files in all (code_patch2: products Blockchain/Dev/services/billing/src/routes/webhooks.ts). Apply PER SECTION with the checker's apply mode — section 1 `section_1.diff`: `git apply -p1` (strict); section 2 `section_2.diff`: `git apply -p1` (strict) — at the tip `03977e89a343ad7362760e4fb0270602fb6da5ce` (re-check `git ls-remote origin develop` first; if develop moved, re-run `git apply --check` per section and state it). Tier: AT LEAST tier 2 (product code changes) — the gate decides. Input: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p3_billing_stripe_webhook_handler_unreadable_throw/input.json`. Brief (given by --brief; its `# ` heading names KS-1868): `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/briefs/ks_1868_o55_p3_billing_stripe_webhook_handler_unreadable_throw/KS-1868.md`. Verdict source: `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-02_ks_1868_o55_p3_billing_stripe_webhook_handler_unreadable_throw/checker.out`.

```diff
diff --git a/Blockchain/Dev/services/billing/src/routes/webhooks.ts b/Blockchain/Dev/services/billing/src/routes/webhooks.ts
--- a/Blockchain/Dev/services/billing/src/routes/webhooks.ts
+++ b/Blockchain/Dev/services/billing/src/routes/webhooks.ts
@@ -213,6 +213,11 @@
       res.json({ received: true });
     } catch (error) {
-      const message = error instanceof Error ? error.message : String(error);
+      let message: string;
+      try {
+        message = error instanceof Error ? error.message : String(error);
+      } catch {
+        message = 'unreadable thrown value';
+      }
       logger.error(`[Webhook] Error handling ${event.type}:`, { error: message });
       // Hand the claim back so the redelivery is processed rather than
       // acknowledged as a duplicate.
diff --git a/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts b/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts
new file mode 100644
--- /dev/null
+++ b/Blockchain/Dev/services/billing/src/__tests__/ks1868-billing-webhook-stripe-handler-unreadable-throw.test.ts
@@ -0,0 +1,227 @@
+import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
+import express from 'express';
+import crypto from 'crypto';
+
+// KS-1868: when the Stripe webhook handler fails with a thrown value that cannot be read (a revoked Proxy throws on
+// `instanceof`; an Error whose `message` getter throws, throws on `.message`), the route must still log, hand the
+// idempotency claim back (status 'failed') and answer the constant 500, exactly as it does for an ordinary Error, so
+// Stripe's redelivery is processed instead of being acknowledged as a duplicate. Harness: the ks1868 replay test (real
+// router on a loopback listener) with a small in-memory stand-in for the webhook_events claim table. The credit stand-in
+// rejects with a plain function's value, not a vi.fn(): a spy inspects what it rejects with and could itself fail on a
+// revoked Proxy before the code under test saw it. At the tip the request is never answered (Express 4 does not see an
+// async handler's rejection) and the claim stays 'processing', so the cell gives the request a short deadline and counts
+// the unhandled rejection itself instead of letting the runner report it.
+
+const { publicKey: rsaPub } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
+
+process.env.NODE_ENV = 'development';
+process.env.JWT_PUBLIC_KEY = Buffer.from(rsaPub.export({ type: 'spki', format: 'pem' }).toString()).toString('base64');
+process.env.DATABASE_URL = 'postgres://test:test@localhost:5432/test';
+
+const h = vi.hoisted(() => ({
+  toThrow: undefined as unknown,
+  granted: 0,
+  logged: [] as unknown[][],
+  warned: [] as unknown[][],
+  rows: new Map<string, string>(),
+  unhandled: 0,
+}));
+
+vi.mock('../db', () => ({
+  isDbAvailable: () => true,
+  query: async (sql: string, params: unknown[] = []) => {
+    const id = String(params[0]);
+    if (/insert\s+into\s+webhook_events/i.test(sql)) {
+      const state = h.rows.get(id);
+      if (state === undefined || state === 'failed') {
+        h.rows.set(id, 'processing');
+        return { rows: [{ event_id: id }], rowCount: 1 };
+      }
+      return { rows: [], rowCount: 0 };
+    }
+    if (/set\s+status\s*=\s*'failed'/i.test(sql)) {
+      if (h.rows.get(id) === 'processing') h.rows.set(id, 'failed');
+      return { rows: [], rowCount: 1 };
+    }
+    if (/set\s+status\s*=\s*'processed'/i.test(sql)) {
+      h.rows.set(id, 'processed');
+      return { rows: [], rowCount: 1 };
+    }
+    return { rows: [], rowCount: 0 };
+  },
+}));
+
+vi.mock('../services/stripeService', () => ({
+  getStripeService: () => ({
+    addCertificationCredits: async () => {
+      if (h.toThrow !== undefined) throw h.toThrow;
+      h.granted += 1;
+      return 120;
+    },
+    constructWebhookEvent: () => ({
+      id: 'evt_ks1868_handler',
+      type: 'checkout.session.completed',
+      data: {
+        object: {
+          id: 'cs_ks1868',
+          customer: 'cus_ks1868',
+          amount_total: 9900,
+          currency: 'aud',
+          payment_status: 'paid',
+          metadata: { certifications: '5', bundleId: 'bundle_pro' },
+        },
+      },
+    }),
+  }),
+}));
+
+vi.mock('../utils/logger', () => ({
+  logger: {
+    debug: () => undefined,
+    info: () => undefined,
+    warn: (...args: unknown[]) => {
+      h.warned.push(args);
+    },
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
+const EVENT_ID = 'evt_ks1868_handler';
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
+  h.granted = 0;
+  h.logged.length = 0;
+  h.warned.length = 0;
+  h.rows.clear();
+  h.unhandled = 0;
+});
+
+/** undefined when the request got no answer inside the deadline. */
+async function deliver() {
+  const res = await fetch(`${baseUrl}/webhooks/stripe`, {
+    method: 'POST',
+    headers: { 'Content-Type': 'application/json', 'stripe-signature': 't=1,v1=stub' },
+    body: JSON.stringify({ id: EVENT_ID, type: 'checkout.session.completed' }),
+    signal: AbortSignal.timeout(TIMEOUT_MS),
+  }).catch(() => undefined);
+  if (!res) return undefined;
+  const body: any = await res.json().catch(() => undefined);
+  return { status: res.status, body };
+}
+const ERRORS = () => h.logged.filter((c) => c[0] === '[Webhook] Error handling checkout.session.completed:');
+const RELEASES = () => h.warned.filter((c) => c[0] === 'Webhook claim released for retry');
+const FAILED = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Webhook handler failed' } };
+
+function revoked() {
+  const { proxy, revoke } = Proxy.revocable({}, {});
+  revoke();
+  return proxy;
+}
+function badGetter() {
+  return Object.create(Error.prototype, {
+    message: {
+      get() {
+        throw new Error('getter boom');
+      },
+    },
+  });
+}
+
+describe('KS-1868 the Stripe webhook handler catch reads the thrown value safely', () => {
+  it('control ks1868 C1 an ordinary Error logs its message, releases the claim and answers the constant 500', async () => {
+    h.toThrow = new Error('credit service down');
+    const res = await deliver();
+    expect(res?.status).toBe(500);
+    expect(res?.body).toEqual(FAILED);
+    expect(ERRORS()).toHaveLength(1);
+    expect(ERRORS()[0][1]).toEqual({ error: 'credit service down' });
+    expect(RELEASES()).toHaveLength(1);
+    expect(RELEASES()[0][1]).toEqual({ eventId: EVENT_ID, reason: 'credit service down' });
+    expect(h.rows.get(EVENT_ID)).toBe('failed');
+  });
+
+  it('control ks1868 C2 after an ordinary Error the redelivery is processed, not acknowledged as a duplicate', async () => {
+    h.toThrow = new Error('credit service down');
+    const first = await deliver();
+    expect(first?.status).toBe(500);
+    h.toThrow = undefined;
+    const second = await deliver();
+    expect(second?.status).toBe(200);
+    expect(second?.body).toEqual({ received: true });
+    expect(h.granted).toBe(1);
+    expect(h.rows.get(EVENT_ID)).toBe('processed');
+  });
+
+  it('RED ks1868 R1 a revoked Proxy thrown value logs a constant reason, releases the claim and answers the constant 500', async () => {
+    h.toThrow = revoked();
+    const res = await deliver();
+    expect(res?.status).toBe(500);
+    expect(res?.body).toEqual(FAILED);
+    expect(ERRORS()).toHaveLength(1);
+    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+    expect(RELEASES()).toHaveLength(1);
+    expect(RELEASES()[0][1]).toEqual({ eventId: EVENT_ID, reason: 'unreadable thrown value' });
+    expect(h.rows.get(EVENT_ID)).toBe('failed');
+  });
+
+  it('RED ks1868 R2 an Error whose message getter throws logs a constant reason, releases the claim and answers the constant 500', async () => {
+    h.toThrow = badGetter();
+    const res = await deliver();
+    expect(res?.status).toBe(500);
+    expect(res?.body).toEqual(FAILED);
+    expect(ERRORS()).toHaveLength(1);
+    expect(ERRORS()[0][1]).toEqual({ error: 'unreadable thrown value' });
+    expect(RELEASES()).toHaveLength(1);
+    expect(RELEASES()[0][1]).toEqual({ eventId: EVENT_ID, reason: 'unreadable thrown value' });
+    expect(h.rows.get(EVENT_ID)).toBe('failed');
+  });
+
+  it('RED ks1868 R3 after an unreadable thrown value the redelivery is processed, not acknowledged as a duplicate', async () => {
+    h.toThrow = revoked();
+    const first = await deliver();
+    expect(first?.status).toBe(500);
+    h.toThrow = undefined;
+    const second = await deliver();
+    expect(second?.status).toBe(200);
+    expect(second?.body).toEqual({ received: true });
+    expect(h.granted).toBe(1);
+    expect(h.rows.get(EVENT_ID)).toBe('processed');
+  });
+});
```
