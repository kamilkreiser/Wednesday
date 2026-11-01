// QA gate 95 probe (NOT part of the PR). Real webhooks router, mounted exactly as billing src/index.ts:50 mounts it
// (express.raw on /webhooks), the real logger (spied, pass-through), the real @secuura/shared errorHandler.
// Replaced: ../db (an in-memory webhook_events claim table that runs the same three statements' semantics) and
// ../services/stripeService (constructWebhookEvent stub + the credit call addCertificationCredits).
// Writes one JSON line per cell to $PROBE_OUT.
import { describe, it, beforeAll, afterAll, beforeEach, vi } from 'vitest';
import express from 'express';
import crypto from 'crypto';
import fs from 'fs';

const { publicKey: rsaPub } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
process.env.NODE_ENV = 'development';
process.env.JWT_PUBLIC_KEY = Buffer.from(rsaPub.export({ type: 'spki', format: 'pem' }).toString()).toString('base64');
process.env.DATABASE_URL = 'postgres://test:test@localhost:5432/test';

const h = vi.hoisted(() => ({
  dbAvailable: true,
  sigThrow: undefined as unknown,
  creditThrow: undefined as unknown,
  grants: 0,
  creditCalls: 0,
  dbCalls: [] as string[],
  rows: new Map<string, string>(),
  unhandled: 0,
  eventKind: 'checkout' as 'checkout' | 'pi',
  finaliseThrow: undefined as unknown,
  releaseThrow: undefined as unknown,
}));

vi.mock('../db', () => ({
  isDbAvailable: () => h.dbAvailable,
  query: async (sql: string, params: unknown[] = []) => {
    const id = String(params[0]);
    if (/insert\s+into\s+webhook_events/i.test(sql)) {
      h.dbCalls.push('claim');
      const state = h.rows.get(id);
      if (state === undefined || state === 'failed') {
        h.rows.set(id, 'processing');
        return { rows: [{ event_id: id }], rowCount: 1 };
      }
      return { rows: [], rowCount: 0 };
    }
    if (/set\s+status\s*=\s*'failed'/i.test(sql)) {
      h.dbCalls.push('release');
      if (h.releaseThrow !== undefined) { const t = h.releaseThrow; h.releaseThrow = undefined; throw t; }
      if (h.rows.get(id) === 'processing') h.rows.set(id, 'failed');
      return { rows: [], rowCount: 1 };
    }
    if (/set\s+status\s*=\s*'processed'/i.test(sql)) {
      h.dbCalls.push('finalise');
      if (h.finaliseThrow !== undefined) { const t = h.finaliseThrow; h.finaliseThrow = undefined; throw t; }
      h.rows.set(id, 'processed');
      return { rows: [], rowCount: 1 };
    }
    h.dbCalls.push('other');
    return { rows: [], rowCount: 0 };
  },
}));

vi.mock('../services/stripeService', () => ({
  getStripeService: () => ({
    // plain functions, not vi.fn(): a spy could itself trip on a revoked Proxy
    addCertificationCredits: async () => {
      h.creditCalls += 1;
      if (h.creditThrow !== undefined) throw h.creditThrow;
      h.grants += 1;
      return 120;
    },
    constructWebhookEvent: () => {
      if (h.sigThrow !== undefined) throw h.sigThrow;
      if (h.eventKind === 'pi') {
        return {
          id: 'evt_gate95_pi',
          type: 'payment_intent.succeeded',
          data: { object: { id: 'pi_gate95', customer: 'cus_gate95', amount: 9900, currency: 'aud',
            metadata: { certifications: '5', bundleId: 'bundle_pro' } } },
        };
      }
      return {
        id: 'evt_gate95',
        type: 'checkout.session.completed',
        data: {
          object: {
            id: 'cs_gate95',
            customer: 'cus_gate95',
            amount_total: 9900,
            currency: 'aud',
            payment_status: 'paid',
            metadata: { certifications: '5', bundleId: 'bundle_pro' },
          },
        },
      };
    },
  }),
}));

const { default: webhookRoutes } = await import('../routes/webhooks');
const { logger } = await import('../utils/logger');
const { errorHandler } = await import('@secuura/shared');

const app = express();
app.use('/webhooks', express.raw({ type: 'application/json' }), webhookRoutes);
app.use(errorHandler);

const OUT = process.env.PROBE_OUT || '/dev/null';
const LABEL = process.env.PROBE_LABEL || 'unlabelled';
const TIMEOUT_MS = 2500;
const EVENT_ID = 'evt_gate95';
const SAVED = process.listeners('unhandledRejection');
const onUnhandled = () => { h.unhandled += 1; };
let baseUrl = '';
let server: ReturnType<typeof app.listen>;
let logLines: { level: string; msg: string; meta: string }[] = [];

function safeJson(v: unknown) {
  try { return JSON.stringify(v); } catch { return '<unserialisable>'; }
}

beforeAll(async () => {
  process.removeAllListeners('unhandledRejection');
  process.on('unhandledRejection', onUnhandled);
  for (const lvl of ['debug', 'info', 'warn', 'error'] as const) {
    const orig = (logger as any)[lvl].bind(logger);
    (logger as any)[lvl] = (...args: unknown[]) => {
      logLines.push({ level: lvl, msg: String(args[0]), meta: safeJson(args[1]) });
      const hook = hooks[lvl];
      if (hook) hook(String(args[0]));
      return orig(...args);
    };
  }
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => {
      const a = server.address();
      baseUrl = `http://127.0.0.1:${typeof a === 'object' && a ? a.port : 0}`;
      resolve();
    });
  });
});
afterAll(() => {
  server?.close();
  process.removeListener('unhandledRejection', onUnhandled);
  for (const l of SAVED) process.on('unhandledRejection', l as (...a: any[]) => void);
});

const hooks: Partial<Record<'debug' | 'info' | 'warn' | 'error', (msg: string) => void>> = {};

beforeEach(() => {
  h.eventKind = 'checkout'; h.finaliseThrow = undefined; h.releaseThrow = undefined; h.dbAvailable = true; h.sigThrow = undefined; h.creditThrow = undefined;
  h.grants = 0; h.creditCalls = 0; h.dbCalls = []; h.rows.clear(); h.unhandled = 0;
  logLines = [];
  for (const k of Object.keys(hooks)) delete (hooks as any)[k];
});

async function deliver() {
  const res = await fetch(`${baseUrl}/webhooks/stripe`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json', 'stripe-signature': 't=1,v1=stub' },
    body: JSON.stringify({ id: EVENT_ID }),
    signal: AbortSignal.timeout(TIMEOUT_MS),
  }).catch(() => undefined);
  if (!res) return 'NO ANSWER (timeout 2.5 s)';
  const body = await res.text();
  return `${res.status} ${body}`;
}
const settle = () => new Promise((r) => setTimeout(r, 50));

function revoked() { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }
function badGetter() {
  return Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } });
}
const KINDS: Record<string, () => unknown> = {
  ordinaryError: () => new Error('credit service down'),
  revokedProxy: revoked,
  throwingGetter: badGetter,
};

function record(cell: string, extra: Record<string, unknown>) {
  const line = {
    label: LABEL, cell, ...extra,
    rowAfter: h.rows.get(EVENT_ID) ?? '(no row)', grants: h.grants, creditCalls: h.creditCalls,
    dbCalls: h.dbCalls.join(','), unhandled: h.unhandled,
    logs: logLines.filter((l) => l.level === 'error' || l.level === 'warn').map((l) => `${l.level}:${l.msg} ${l.meta}`),
  };
  fs.appendFileSync(OUT, JSON.stringify(line) + '\n');
}

describe('gate95 probe', () => {
  // Q1: P3 site. A thrown value from the credit call (pre-grant), then a clean redelivery.
  for (const k of Object.keys(KINDS)) {
    it(`P3 pre-grant ${k} then clean redelivery`, async () => {
      h.creditThrow = KINDS[k]();
      const first = await deliver(); await settle();
      const rowAfterFirst = h.rows.get(EVENT_ID) ?? '(no row)';
      const unhandledAfterFirst = h.unhandled;
      h.creditThrow = undefined;
      const second = await deliver(); await settle();
      record(`P3-pre-${k}`, { first, rowAfterFirst, unhandledAfterFirst, redelivery: second });
    });
  }
  // Q3 reading (i): a thrown value AFTER the grant (logger.info('Payment status') throws), then a clean redelivery.
  for (const k of Object.keys(KINDS)) {
    it(`P3 post-grant ${k} then clean redelivery`, async () => {
      let armed = true;
      hooks.info = (msg) => { if (armed && msg === 'Payment status') { armed = false; throw KINDS[k](); } };
      const first = await deliver(); await settle();
      const rowAfterFirst = h.rows.get(EVENT_ID) ?? '(no row)';
      const unhandledAfterFirst = h.unhandled;
      const grantsAfterFirst = h.grants;
      const second = await deliver(); await settle();
      record(`P3-post-${k}`, { first, rowAfterFirst, unhandledAfterFirst, grantsAfterFirst, redelivery: second });
    });
  }
  // Q2: P1 signature check.
  for (const k of Object.keys(KINDS)) {
    it(`P1 signature ${k}`, async () => {
      h.sigThrow = KINDS[k]();
      const first = await deliver(); await settle();
      record(`P1-${k}`, { first });
    });
  }
  // Q2: P2 claim. Ordinary = the designed path (DB unavailable -> ClaimUnavailableError). Hostile = logger.warn in the
  // !isDbAvailable branch throws the value (the only way it reaches this catch, per operator 55).
  it('P2 claim ordinary (DB unavailable)', async () => {
    h.dbAvailable = false;
    const first = await deliver(); await settle();
    record('P2-ordinaryClaimUnavailable', { first });
  });
  for (const k of Object.keys(KINDS)) {
    it(`P2 claim logger.warn throws ${k}`, async () => {
      h.dbAvailable = false;
      let armed = true;
      hooks.warn = (msg) => { if (armed && msg.startsWith('DB unavailable')) { armed = false; throw KINDS[k](); } };
      const first = await deliver(); await settle();
      record(`P2-warnThrows-${k}`, { first });
    });
  }
  // Q3 reading (ii): one purchase, two events (checkout.session.completed then payment_intent.succeeded with the
  // same metadata and no creditsAdded flag), both delivered clean. Untouched code; measured for base == head.
  it('reading-ii two events one purchase', async () => {
    const first = await deliver(); await settle();
    h.eventKind = 'pi';
    const second = await deliver(); await settle();
    record('reading-ii-checkout-then-pi', { first, second, rowPi: h.rows.get('evt_gate95_pi') ?? '(no row)' });
  });
  // Neighbouring unguarded reads (pre-existing, NOT in this PR): finaliseEvent's catch and releaseClaim's catch read
  // err?.message. finalise runs AFTER the grant.
  for (const k of ['ordinaryError', 'revokedProxy']) {
    it(`neighbour finalise rejects ${k} then clean redelivery`, async () => {
      h.finaliseThrow = KINDS[k]();
      const first = await deliver(); await settle();
      const rowAfterFirst = h.rows.get(EVENT_ID) ?? '(no row)';
      const second = await deliver(); await settle();
      record(`N-finalise-${k}`, { first, rowAfterFirst, redelivery: second });
    });
    it(`neighbour release rejects ${k} after an ordinary credit Error, then clean redelivery`, async () => {
      h.creditThrow = new Error('credit service down');
      h.releaseThrow = KINDS[k]();
      const first = await deliver(); await settle();
      const rowAfterFirst = h.rows.get(EVENT_ID) ?? '(no row)';
      const unhandledAfterFirst = h.unhandled;
      h.creditThrow = undefined;
      const second = await deliver(); await settle();
      record(`N-release-${k}`, { first, rowAfterFirst, unhandledAfterFirst, redelivery: second });
    });
  }
  it('control clean delivery then redelivery', async () => {
    const first = await deliver(); await settle();
    const second = await deliver(); await settle();
    record('control-clean', { first, redelivery: second });
  });
});
