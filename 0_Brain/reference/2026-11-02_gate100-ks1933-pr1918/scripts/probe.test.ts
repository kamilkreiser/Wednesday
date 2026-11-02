// QA gate 100 probe (NOT part of the PR). The REAL webhooks router, mounted as billing src/index.ts mounts it
// (express.raw on /webhooks), the real logger (wrapped, pass-through), the real @secuura/shared errorHandler.
// Replaced: ../db (an in-memory model of webhook_events + billing_credit_grants, written by the gate from the SQL text,
// independent of the author's stand-in) and ../services/stripeService (constructWebhookEvent + addCertificationCredits).
// One JSON line per cell to $PROBE_OUT. Cells only RECORD; the verdict reads the figures.
import { describe, it, beforeAll, afterAll, beforeEach } from 'vitest';
import express from 'express';
import crypto from 'crypto';
import fs from 'fs';
import jwt from 'jsonwebtoken';

const { privateKey: rsaPriv, publicKey: rsaPub } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIV = rsaPriv.export({ type: 'pkcs8', format: 'pem' }).toString();
process.env.NODE_ENV = 'development';
process.env.JWT_PUBLIC_KEY = Buffer.from(rsaPub.export({ type: 'spki', format: 'pem' }).toString()).toString('base64');
process.env.DATABASE_URL = 'postgres://test:test@localhost:5432/test';

const h = vi.hoisted(() => ({
  events: new Map<string, any>(),
  ev: new Map<string, { status: string; payload: any; type: string }>(),
  gr: new Map<string, { status: string; credits: number; eventId: string }>(),
  grants: 0, creditCalls: 0, calls: [] as string[], unknown: [] as string[],
  fail: {} as Record<string, unknown>,   // statement tag -> value to throw once
  claimEmpty: false, readEmpty: false,
  hold: undefined as undefined | Promise<void>,
  creditThrow: undefined as unknown, creditThrowAfterApply: undefined as unknown,
}));
import { vi } from 'vitest';
function once(tag: string) { if (tag in h.fail) { const v = h.fail[tag]; delete h.fail[tag]; throw v; } }

vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: async (sql: string, p: unknown[] = []) => {
    const s = sql.replace(/\s+/g, ' ').trim(); const id = String(p[0]);
    let m: RegExpMatchArray | null;
    if (/^INSERT INTO webhook_events .* ON CONFLICT \(event_id\) DO UPDATE SET status = 'processing', processed_at = NOW\(\) WHERE webhook_events\.status = 'failed' RETURNING event_id$/.test(s)) {
      h.calls.push('evClaim'); once('evClaim');
      const r = h.ev.get(id);
      if (!r || r.status === 'failed') { h.ev.set(id, { status: 'processing', payload: JSON.parse(String(p[2])), type: String(p[1]) }); return { rows: [{ event_id: id }], rowCount: 1 }; }
      return { rows: [], rowCount: 0 };
    }
    if (s === "UPDATE webhook_events SET status = 'failed' WHERE event_id = $1 AND status = 'processing'") {
      h.calls.push('evRelease'); once('evRelease');
      const r = h.ev.get(id); if (r?.status === 'processing') { r.status = 'failed'; return { rows: [], rowCount: 1 }; } return { rows: [], rowCount: 0 };
    }
    if (/^UPDATE webhook_events SET status = 'processed'/.test(s)) {
      h.calls.push('evFinalise'); once('evFinalise');
      const r = h.ev.get(id); if (r) r.status = 'processed'; return { rows: [], rowCount: r ? 1 : 0 };
    }
    if (s === 'SELECT payload, event_type, status FROM webhook_events WHERE event_id = $1') {
      h.calls.push('evRead'); const r = h.ev.get(id);
      return r ? { rows: [{ payload: r.payload, event_type: r.type, status: r.status }], rowCount: 1 } : { rows: [], rowCount: 0 };
    }
    if (/^UPDATE webhook_events SET status = 'replayed'/.test(s)) { h.calls.push('evReplayed'); const r = h.ev.get(id); if (r) r.status = 'replayed'; return { rows: [], rowCount: 1 }; }
    if (s === "INSERT INTO billing_credit_grants (payment_key, customer_id, credits, status, event_id, event_type) VALUES ($1, $2, $3, 'granting', $4, $5) ON CONFLICT (payment_key) DO UPDATE SET status = 'granting', event_id = EXCLUDED.event_id, event_type = EXCLUDED.event_type, updated_at = NOW() WHERE billing_credit_grants.status = 'failed' RETURNING payment_key") {
      h.calls.push('grClaim:' + id); once('grClaim');
      if (h.claimEmpty) return { rows: [], rowCount: 0 };
      const r = h.gr.get(id);
      if (!r) { h.gr.set(id, { status: 'granting', credits: Number(p[2]), eventId: String(p[3]) }); return { rows: [{ payment_key: id }], rowCount: 1 }; }
      if (r.status === 'failed') { r.status = 'granting'; r.eventId = String(p[3]); return { rows: [{ payment_key: id }], rowCount: 1 }; }
      return { rows: [], rowCount: 0 };
    }
    if ((m = s.match(/^UPDATE billing_credit_grants SET status = '(granted|failed)', updated_at = NOW\(\) WHERE payment_key = \$1 AND status = 'granting'$/))) {
      const tag = m[1] === 'granted' ? 'grMarkGranted' : 'grMarkFailed'; h.calls.push(tag); once(tag);
      const r = h.gr.get(id); if (r?.status === 'granting') { r.status = m[1]; return { rows: [], rowCount: 1 }; } return { rows: [], rowCount: 0 };
    }
    if (/^SELECT status, EXTRACT\(EPOCH FROM \(NOW\(\) - updated_at\)\)::int AS age_seconds FROM billing_credit_grants WHERE payment_key = \$1$/.test(s)) {
      h.calls.push('grRead'); once('grRead');
      const r = h.gr.get(id); if (!r || h.readEmpty) return { rows: [], rowCount: 0 };
      return { rows: [{ status: r.status, age_seconds: 42 }], rowCount: 1 };
    }
    h.unknown.push(s.slice(0, 90)); return { rows: [], rowCount: 0 };
  },
}));

vi.mock('../services/stripeService', () => ({
  getStripeService: () => ({
    addCertificationCredits: async () => {
      h.creditCalls += 1;
      if (h.hold) await h.hold;
      if (h.creditThrow !== undefined) { const t = h.creditThrow; h.creditThrow = undefined; throw t; }
      h.grants += 1;
      if (h.creditThrowAfterApply !== undefined) { const t = h.creditThrowAfterApply; h.creditThrowAfterApply = undefined; throw t; }
      return 100 + h.grants;
    },
    constructWebhookEvent: (payload: Buffer) => {
      const { id } = JSON.parse(String(payload)); const e = h.events.get(id);
      if (!e) throw new Error('unknown probe event'); return JSON.parse(JSON.stringify(e));
    },
  }),
}));

const OUT = process.env.PROBE_OUT || '/dev/null';
const LABEL = process.env.PROBE_LABEL || 'unlabelled';
let baseUrl = ''; let server: any; let unhandled = 0;
const onUnh = () => { unhandled += 1; };
const SAVED = process.listeners('unhandledRejection');
let lines: { level: string; msg: string; meta: string }[] = [];
const hooks: Record<string, (msg: string) => void> = {};
const sj = (v: unknown) => { try { return JSON.stringify(v) ?? ''; } catch { return '<unserialisable>'; } };

beforeAll(async () => {
  const { default: routes } = await import('../routes/webhooks');
  const { errorHandler } = await import('@secuura/shared');
  const { logger } = await import('../utils/logger');
  for (const lvl of ['debug', 'info', 'warn', 'error'] as const) {
    const orig = (logger as any)[lvl].bind(logger);
    (logger as any)[lvl] = (...a: unknown[]) => { lines.push({ level: lvl, msg: String(a[0]), meta: sj(a[1]) }); const k = hooks[lvl]; if (k) k(String(a[0])); return orig(...a); };
  }
  const app = express();
  app.use('/webhooks', express.raw({ type: 'application/json' }), routes);
  app.use(errorHandler);
  process.removeAllListeners('unhandledRejection'); process.on('unhandledRejection', onUnh);
  await new Promise<void>((res) => { server = app.listen(0, '127.0.0.1', () => { baseUrl = `http://127.0.0.1:${server.address().port}`; res(); }); });
});
afterAll(() => { server?.close(); process.removeListener('unhandledRejection', onUnh); for (const l of SAVED) process.on('unhandledRejection', l as any); });
beforeEach(() => {
  h.events.clear(); h.ev.clear(); h.gr.clear(); h.grants = 0; h.creditCalls = 0; h.calls = []; h.unknown = []; h.fail = {};
  h.claimEmpty = false; h.readEmpty = false; h.hold = undefined; h.creditThrow = undefined; h.creditThrowAfterApply = undefined;
  lines = []; unhandled = 0; for (const k of Object.keys(hooks)) delete hooks[k];
});

const CUS = 'cus_g100';
function cs(n: number, pi: unknown = `pi_g100_${n}`, credits = '5') {
  const e = { id: `evt_cs_${n}`, type: 'checkout.session.completed', data: { object: { id: `cs_g100_${n}`, object: 'checkout.session', mode: 'payment', customer: CUS, payment_intent: pi, payment_status: 'paid', amount_total: 9900, currency: 'aud', metadata: { certifications: credits, bundleId: 'bundle_pro' } } } };
  h.events.set(e.id, e); return e.id;
}
function pi(n: number, credits = '5') {
  const e = { id: `evt_pi_${n}`, type: 'payment_intent.succeeded', data: { object: { id: `pi_g100_${n}`, object: 'payment_intent', customer: CUS, amount: 9900, currency: 'aud', metadata: { certifications: credits, bundleId: 'bundle_pro' } } } };
  h.events.set(e.id, e); return e.id;
}
const revoked = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const KINDS: Record<string, () => unknown> = { ordinary: () => Object.assign(new Error('SECRET-msg cus_leak a@b.c'), { code: 'X1', amount: 9900 }), unreadable: revoked };

async function deliver(id: string) {
  const r = await fetch(`${baseUrl}/webhooks/stripe`, { method: 'POST', headers: { 'Content-Type': 'application/json', 'stripe-signature': 't=1,v1=stub' }, body: JSON.stringify({ id }), signal: AbortSignal.timeout(2500) }).catch(() => undefined);
  if (!r) return 'NO ANSWER'; const b = await r.text(); return `${r.status} ${b}`.slice(0, 120);
}
async function replay(id: string) {
  const tok = jwt.sign({ userId: 'u-g100', email: 'admin@secuura.io', role: 'SYSTEM_ADMIN' }, PRIV, { algorithm: 'RS256', expiresIn: '5m' });
  const r = await fetch(`${baseUrl}/webhooks/replay`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${tok}` }, body: JSON.stringify({ eventId: id, reason: 'gate 100 probe' }), signal: AbortSignal.timeout(2500) }).catch(() => undefined);
  if (!r) return 'NO ANSWER'; return `${r.status} ${(await r.text()).slice(0, 120)}`;
}
const settle = () => new Promise((r) => setTimeout(r, 30));
function rec(cell: string, x: Record<string, unknown>) {
  fs.appendFileSync(OUT, JSON.stringify({ label: LABEL, cell, ...x, GRANTS: h.grants, creditCalls: h.creditCalls, unhandled,
    evRows: Object.fromEntries([...h.ev].map(([k, v]) => [k, v.status])), grRows: Object.fromEntries([...h.gr].map(([k, v]) => [k, v.status])),
    calls: h.calls.join(','), unknownSql: h.unknown,
    logs: lines.filter((l) => l.level === 'warn' || l.level === 'error').map((l) => `${l.level}:${l.msg} ${l.meta}`) }) + '\n');
}

describe('gate100 probe', () => {
  it('A1 cs then pi, clean', async () => { const a = await deliver(cs(1)); const b = await deliver(pi(1)); rec('A1-cs-then-pi', { a, b }); });
  it('A2 pi then cs, clean', async () => { const a = await deliver(pi(1)); const b = await deliver(cs(1)); rec('A2-pi-then-cs', { a, b }); });
  it('A3 concurrent cs + pi, credit held', async () => {
    let rel!: () => void; h.hold = new Promise<void>((r) => { rel = r; });
    const pa = deliver(cs(1)); const pb = deliver(pi(1));
    const t0 = Date.now(); while (Date.now() - t0 < 1500 && h.calls.filter((c) => c.startsWith('grClaim') || c === 'x').length < 2 && h.creditCalls < 2) await new Promise((r) => setTimeout(r, 5));
    rel(); const [a, b] = await Promise.all([pa, pb]); rec('A3-concurrent', { a, b });
  });
  it('A3b concurrent, the held credit FAILS, then its redelivery', async () => {
    let rel!: () => void; h.hold = new Promise<void>((r) => { rel = r; });
    const pa = deliver(cs(1)); const t0 = Date.now(); while (Date.now() - t0 < 1500 && h.creditCalls < 1) await new Promise((r) => setTimeout(r, 5));
    const b = await deliver(pi(1)); // arrives while cs's credit is in flight
    h.creditThrow = new Error('stripe down'); h.hold = undefined; rel(); const a = await pa; await settle();
    const a2 = await deliver('evt_cs_1'); rec('A3b-concurrent-first-fails-then-redelivered', { a, b, a2 });
  });
  it('A3c concurrent same event twice (Stripe double send)', async () => {
    let rel!: () => void; h.hold = new Promise<void>((r) => { rel = r; }); const id = cs(1);
    const pa = deliver(id); const pb = deliver(id); await new Promise((r) => setTimeout(r, 200)); rel();
    const [a, b] = await Promise.all([pa, pb]); rec('A3c-same-event-concurrent', { a, b });
  });
  for (const k of Object.keys(KINDS)) {
    it(`A4 post-grant ${k} (checkout), redelivered`, async () => {
      let armed = true; hooks.info = (m) => { if (armed && m === 'Payment status') { armed = false; throw KINDS[k](); } };
      const id = cs(1); const a = await deliver(id); await settle(); const rowAfter = h.ev.get(id)?.status; const b = await deliver(id);
      rec(`A4-post-grant-checkout-${k}`, { a, rowAfter, b });
    });
    it(`A4b post-grant ${k} (payment_intent), redelivered`, async () => {
      let armed = true; hooks.info = (m) => { if (armed && m === 'Credits added via payment_intent backup') { armed = false; throw KINDS[k](); } };
      const id = pi(1); const a = await deliver(id); await settle(); const b = await deliver(id); rec(`A4b-post-grant-pi-${k}`, { a, b });
    });
    it(`A5 finalise rejects ${k}, redelivered, then the other event`, async () => {
      h.fail.evFinalise = KINDS[k](); const id = cs(1); const a = await deliver(id); await settle(); const b = await deliver(id); const c = await deliver(pi(1));
      rec(`A5-finalise-${k}`, { a, b, c });
    });
    it(`A6 release rejects ${k} after a credit-call failure, redelivered, then admin replay`, async () => {
      h.creditThrow = new Error('stripe down'); h.fail.evRelease = KINDS[k](); const id = cs(1);
      const a = await deliver(id); await settle(); const unhAfterA = unhandled; const b = await deliver(id); const r = await replay(id);
      rec(`A6-release-${k}`, { a, unhAfterA, b, replay: r });
    });
    it(`A6b release rejects ${k} after a POST-grant throw, redelivered, then the other event`, async () => {
      let armed = true; hooks.info = (m) => { if (armed && m === 'Payment status') { armed = false; throw new Error('post'); } };
      h.fail.evRelease = KINDS[k](); const id = cs(1); const a = await deliver(id); await settle(); const b = await deliver(id); const c = await deliver(pi(1));
      rec(`A6b-release-after-postgrant-${k}`, { a, b, c });
    });
  }
  it('A7 single clean event + redelivery', async () => { const id = cs(1); const a = await deliver(id); const b = await deliver(id); rec('A7-single-clean', { a, b }); });
  it('A8 two purchases one customer, both events each, interleaved', async () => {
    const r = [await deliver(cs(1)), await deliver(pi(2)), await deliver(cs(2)), await deliver(pi(1))]; rec('A8-two-purchases', { r });
  });
  it('A9 replay of a credited event', async () => { const id = cs(1); const a = await deliver(id); const r = await replay(id); const r2 = await replay(pi(1) && id); rec('A9-replay-credited', { a, replay: r, replay2: r2 }); });
  it('A9b replay of a credited purchase via its OTHER event stored', async () => { const a = await deliver(cs(1)); const id = pi(1); const b = await deliver(id); const r = await replay(id); rec('A9b-replay-other-event', { a, b, replay: r }); });
  it('A10 replay of a never-credited event (credit failed, release ok, no redelivery yet)', async () => {
    h.creditThrow = new Error('stripe down'); const id = cs(1); const a = await deliver(id); const r = await replay(id); const b = await deliver(id);
    rec('A10-replay-never-credited', { a, replay: r, redeliveryAfterReplay: b });
  });
  it('A11 session with NO PaymentIntent (cs: key), replay, redelivery', async () => { const id = cs(1, null); const a = await deliver(id); const r = await replay(id); const b = await deliver(id); rec('A11-cs-key', { a, replay: r, b }); });
  it('A12 session with an EXPANDED payment_intent object, then the pi event', async () => { const a = await deliver(cs(1, { id: 'pi_g100_1', object: 'payment_intent' })); const b = await deliver(pi(1)); rec('A12-expanded-pi', { a, b }); });
  it('A13 session payment_intent null on cs event but a pi event for the same purchase (hypothetical)', async () => { const a = await deliver(cs(1, null)); const b = await deliver(pi(1)); rec('A13-hypothetical-null-pi-then-pi', { a, b }); });
  // B: fail-closed
  for (const k of Object.keys(KINDS)) {
    it(`B1 grant claim INSERT rejects ${k}, redelivered`, async () => {
      h.fail.grClaim = KINDS[k](); const id = cs(1); const a = await deliver(id); await settle(); const rowAfter = h.ev.get(id)?.status; const unhA = unhandled; const b = await deliver(id);
      rec(`B1-claim-rejects-${k}`, { a, rowAfter, unhA, b });
    });
  }
  it('B2 grant claim returns no row and READ finds none (impossible on PG)', async () => { h.claimEmpty = true; h.readEmpty = true; const id = cs(1); const a = await deliver(id); h.claimEmpty = false; h.readEmpty = false; const b = await deliver(id); rec('B2-claim-empty-read-empty', { a, b }); });
  it('B3 READ after a lost claim rejects', async () => { await deliver(cs(1)); h.fail.grRead = new Error('read down'); const id = pi(1); const a = await deliver(id); const b = await deliver(id); rec('B3-read-rejects', { a, b }); });
  for (const k of Object.keys(KINDS)) {
    it(`B4 mark-granted rejects ${k}; redelivery, other event, replay`, async () => {
      h.fail.grMarkGranted = KINDS[k](); const id = cs(1); const a = await deliver(id); const b = await deliver(id); const c = await deliver(pi(1)); const r = await replay(id);
      rec(`B4-mark-granted-rejects-${k}`, { a, b, c, replay: r });
    });
  }
  it('B5 process died between claim and credit (state seeded: grant granting, event processing)', async () => {
    const id = cs(1); h.gr.set('pi:pi_g100_1', { status: 'granting', credits: 5, eventId: id });
    const ev = h.events.get(id); h.ev.set(id, { status: 'processing', payload: ev, type: ev.type });
    const a = await deliver(id); const b = await deliver(pi(1)); const r = await replay(id);
    rec('B5-died-mid-credit', { a, b, replay: r });
  });
  it('B6 credit throws AND mark-failed rejects; redelivery; other event', async () => {
    h.creditThrow = new Error('stripe down'); h.fail.grMarkFailed = new Error('db blip'); const id = cs(1);
    const a = await deliver(id); const b = await deliver(id); const c = await deliver(pi(1)); rec('B6-credit-and-markfailed-fail', { a, b, c });
  });
  it('B7 residual: credit applied in Stripe then the call throws; redelivered', async () => {
    h.creditThrowAfterApply = new Error('network after write'); const id = cs(1); const a = await deliver(id); const b = await deliver(id); rec('B7-residual-throw-after-apply', { a, b });
  });
  it('B8 different credits on the two events (pi first with 3, cs with 5)', async () => { const a = await deliver(pi(1, '3')); const b = await deliver(cs(1, 'pi_g100_1', '5')); rec('B8-mismatched-credits', { a, b }); });
});
