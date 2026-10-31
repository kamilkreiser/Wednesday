// GATE 62 PROBE: harness lines 1-216 copied verbatim from the PR's ks1888 route test at aa64f183, then gate 62's own cells.
/**
 * KS-1888 — twelve billing routes took a Stripe customer, invoice or payment-method id from the caller and acted on
 * it with no check of who was asking: read and change any customer, spend its certification credits, list or detach
 * its payment methods, read its invoices. POST /customers also handed any existing customer to whoever posted its
 * email, and PUT /customers/:id let a caller write `metadata.certificationCredits`, which is where the balance lives.
 *
 * The rule pinned here is Wednesday's ANSWER of 2026-10-31 10:33:28Z, under Kam's "fix it properly" (2026-10-30
 * 12:55:54), quoted:
 *   "APPROVED as you recommend: D1 (owner or platform administrator; tenantId must match where the customer records
 *   one; a refusal is byte-identical to an unknown id, with no write and no reason logged), D2 (POST /customers joins
 *   as the 13th route; userId and tenantId come from the token; a differing body userId gets 403 unless platform
 *   admin; the existing-by-email branch returns that customer only to its owner or a platform admin, otherwise a new
 *   customer), D3 (PUT refuses certificationCredits/userId/tenantId with 400 for everyone) and D4 (move GET
 *   /customers/by-email above /:id, under D1)."
 *
 * - Owner: the customer's `metadata.userId` equals `req.user.userId`, both non-empty strings, exact compare; and where
 *   the customer records `metadata.tenantId`, it equals `req.user.tenantId`. Platform administrator: the shared
 *   `isPlatformRole` (KS 1591, as KS-1850). Tenant roles get nothing beyond their own customer.
 * - An invoice or payment method belongs to the owner of its `customer`; with no customer, or on a customer with no
 *   recorded owner, it is platform administrators only.
 * - The owner lookup must not turn a provider outage into a 404: it still answers 503 (the KS-445 class).
 *
 * Harness: the KS-1850 one (the billing router on a real express app on 127.0.0.1, the Stripe service a mock, so no
 * real or test Stripe account is ever called, plus a stand-in for `jwtAuthenticate()` that sets the cell's principal).
 * The mock keeps an in-memory store with Stripe's semantics for the calls these routes make ("No such ..." on an
 * unknown id), so a refusal can be compared byte for byte with an unknown id and the store checked unchanged.
 */
import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
import express from 'express';

type Meta = Record<string, string>;
interface FakeCustomer { id: string; email: string; name?: string; metadata: Meta; defaultPaymentMethod?: string }
interface FakeAttached { id: string; customer: string | null }

const fake = vi.hoisted(() => {
  const customers = new Map<string, FakeCustomer>();
  const invoices = new Map<string, FakeAttached>();
  const paymentMethods = new Map<string, FakeAttached>();
  const clone = <T>(v: T): T => JSON.parse(JSON.stringify(v));
  const noSuch = (kind: string, id: string) =>
    Object.assign(new Error(`No such ${kind}: '${id}'`), { type: 'StripeInvalidRequestError', statusCode: 404, code: 'resource_missing' });
  let created = 0;
  const mustHave = (id: string): FakeCustomer => {
    const c = customers.get(id);
    if (!c) throw noSuch('customer', id);
    return c;
  };
  const mocks = {
    getCustomer: vi.fn(async (id: string) => (customers.has(id) ? clone(customers.get(id)) : null)),
    findCustomer: vi.fn(async (id: string) => (customers.has(id) ? clone(customers.get(id)) : null)),
    findCustomerByEmail: vi.fn(async (email: string) => {
      const hit = [...customers.values()].find((c) => c.email === email);
      return hit ? clone(hit) : null;
    }),
    listCustomersByEmail: vi.fn(async (email: string) => clone([...customers.values()].filter((c) => c.email === email))),
    createCustomer: vi.fn(async (p: { email: string; name?: string; userId: string; metadata?: Meta }) => {
      created += 1;
      const c: FakeCustomer = { id: `cus_new_${created}`, email: p.email, name: p.name, metadata: { userId: p.userId, certificationCredits: '0', ...(p.metadata ?? {}) } };
      customers.set(c.id, c);
      return clone(c);
    }),
    updateCustomer: vi.fn(async (id: string, p: { email?: string; name?: string; metadata?: Meta }) => {
      const c = mustHave(id);
      if (p.email !== undefined) c.email = p.email;
      if (p.name !== undefined) c.name = p.name;
      if (p.metadata) c.metadata = { ...c.metadata, ...p.metadata };
      return clone(c);
    }),
    getCertificationBalance: vi.fn(async (id: string) => {
      const c = customers.get(id);
      return c ? parseInt(c.metadata.certificationCredits || '0', 10) : 0;
    }),
    useCertificationCredits: vi.fn(async (id: string, credits: number) => {
      const c = mustHave(id);
      const balance = parseInt(c.metadata.certificationCredits || '0', 10);
      if (balance < credits) return { success: false, newBalance: balance };
      c.metadata.certificationCredits = String(balance - credits);
      return { success: true, newBalance: balance - credits };
    }),
    listPurchases: vi.fn(async (id: string) => [{ id: `pi_of_${id}` }]),
    listInvoices: vi.fn(async (id: string) => [...invoices.values()].filter((i) => i.customer === id).map(clone)),
    createSetupIntent: vi.fn(async (id: string) => {
      mustHave(id);
      return { client_secret: `seti_secret_of_${id}` };
    }),
    listPaymentMethods: vi.fn(async (id: string) => {
      mustHave(id);
      return [...paymentMethods.values()].filter((p) => p.customer === id).map(clone);
    }),
    setDefaultPaymentMethod: vi.fn(async (id: string, pm: string) => {
      const c = mustHave(id);
      c.defaultPaymentMethod = pm;
      return clone(c);
    }),
    detachPaymentMethod: vi.fn(async (id: string) => {
      const p = paymentMethods.get(id);
      if (!p) throw noSuch('payment_method', id);
      p.customer = null;
      return clone(p);
    }),
    getInvoice: vi.fn(async (id: string) => (invoices.has(id) ? clone(invoices.get(id)) : null)),
    getPaymentMethod: vi.fn(async (id: string) => (paymentMethods.has(id) ? clone(paymentMethods.get(id)) : null)),
  };
  const reset = () => {
    customers.clear(); invoices.clear(); paymentMethods.clear(); created = 0;
    const put = (id: string, email: string, metadata: Meta) => customers.set(id, { id, email, metadata });
    put('cus_alice', 'alice@a.test', { userId: 'u-alice', tenantId: 't-1', certificationCredits: '10' });
    put('cus_legacy', 'legacy@a.test', { userId: 'u-alice', certificationCredits: '5' });
    put('cus_unowned', 'unowned@a.test', { certificationCredits: '3' });
    put('cus_num', 'num@a.test', { userId: '42', tenantId: 't-1', certificationCredits: '7' });
    for (const [suffix, customer] of [['alice', 'cus_alice'], ['legacy', 'cus_legacy'], ['unowned', 'cus_unowned'], ['num', 'cus_num'], ['unattached', null]] as const) {
      invoices.set(`in_${suffix}`, { id: `in_${suffix}`, customer });
      paymentMethods.set(`pm_${suffix}`, { id: `pm_${suffix}`, customer });
    }
  };
  const snapshot = () => JSON.stringify({ c: [...customers.entries()], i: [...invoices.entries()], p: [...paymentMethods.entries()] });
  return { customers, mocks, reset, snapshot };
});

vi.mock('../services/stripeService', () => ({ getStripeService: () => fake.mocks }));

const log = vi.hoisted(() => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() }));
vi.mock('../utils/logger', () => ({ logger: log }));

// A static import (KS-1850): a top-level await is TS1378 under the service's module commonjs.
import billingRoutes from '../routes/billing';

/** The principal the stand-in puts on the request; `undefined` leaves req.user unset. */
let PRINCIPAL: Record<string, unknown> | undefined;

const app = express();
app.use((req: any, _res, next) => {
  if (PRINCIPAL !== undefined) req.user = { ...PRINCIPAL };
  next();
});
app.use('/billing', express.json(), billingRoutes);

let baseUrl = '';
let server: ReturnType<typeof app.listen>;

beforeAll(async () => {
  await new Promise<void>((resolve) => {
    server = app.listen(0, '127.0.0.1', () => resolve());
  });
  const address = server.address();
  baseUrl = `http://127.0.0.1:${typeof address === 'object' && address ? address.port : 0}`;
});

afterAll(() => {
  server?.close();
});

beforeEach(() => {
  fake.reset();
  for (const m of Object.values(fake.mocks)) m.mockClear();
  for (const m of Object.values(log)) m.mockClear();
  PRINCIPAL = undefined;
});

const ALICE = { userId: 'u-alice', email: 'alice@a.test', role: 'OWNER', tenantId: 't-1' };
const ALICE_OTHER_TENANT = { ...ALICE, tenantId: 't-2' };
const BOB = { userId: 'u-bob', email: 'bob@a.test', role: 'OWNER', tenantId: 't-1' };
const CAROL_ORG_ADMIN = { userId: 'u-carol', email: 'carol@a.test', role: 'ORG_ADMIN', tenantId: 't-1' };
const SYSTEM_ADMIN = { userId: 'u-sys', role: 'SYSTEM_ADMIN', tenantId: 't-9' };
const SUPER_ADMIN = { userId: 'u-super', role: 'SUPER_ADMIN' };
const SYSTEM_ADMIN_LOWER = { userId: 'u-sys2', role: 'system_admin', tenantId: 't-9' };
const NO_USERID = { role: 'OWNER', tenantId: 't-1' };
const NUMERIC_USERID = { userId: 42, role: 'OWNER', tenantId: 't-1' };

type Kind = 'customer' | 'email' | 'invoice' | 'paymentMethod';
const SUBJECTS: Record<Kind, Record<'alice' | 'legacy' | 'unowned' | 'num' | 'unknown' | 'unattached', string>> = {
  customer: { alice: 'cus_alice', legacy: 'cus_legacy', unowned: 'cus_unowned', num: 'cus_num', unknown: 'cus_unknown', unattached: '' },
  email: { alice: 'alice@a.test', legacy: 'legacy@a.test', unowned: 'unowned@a.test', num: 'num@a.test', unknown: 'nobody@a.test', unattached: '' },
  invoice: { alice: 'in_alice', legacy: 'in_legacy', unowned: 'in_unowned', num: 'in_num', unknown: 'in_unknown', unattached: 'in_unattached' },
  paymentMethod: { alice: 'pm_alice', legacy: 'pm_legacy', unowned: 'pm_unowned', num: 'pm_num', unknown: 'pm_unknown', unattached: 'pm_unattached' },
};

/** Calls that change Stripe state or list a customer's data: none may run for a refused caller. */
const EFFECTS = ['createCustomer', 'updateCustomer', 'useCertificationCredits', 'createSetupIntent', 'setDefaultPaymentMethod', 'detachPaymentMethod', 'listPurchases', 'listInvoices', 'listPaymentMethods'] as const;

interface Route {
  name: string;
  kind: Kind;
  ok: number;
  request: (subject: string) => { method: string; path: string; body?: unknown };
  /** The call the admitted cell must see, with the subject as its first argument (absent on pure reads). */
  effect?: (typeof EFFECTS)[number];
}

const ROUTES: Route[] = [
  { name: 'POST /credits/use', kind: 'customer', ok: 200, effect: 'useCertificationCredits', request: (s) => ({ method: 'POST', path: '/credits/use', body: { customerId: s, credits: 1 } }) },
  { name: 'GET /customers/:id', kind: 'customer', ok: 200, request: (s) => ({ method: 'GET', path: `/customers/${s}` }) },
  { name: 'GET /customers/:id/credits', kind: 'customer', ok: 200, request: (s) => ({ method: 'GET', path: `/customers/${s}/credits` }) },
  { name: 'PUT /customers/:id', kind: 'customer', ok: 200, effect: 'updateCustomer', request: (s) => ({ method: 'PUT', path: `/customers/${s}`, body: { name: 'Renamed' } }) },
  { name: 'GET /customers/by-email', kind: 'email', ok: 200, request: (s) => ({ method: 'GET', path: `/customers/by-email?email=${encodeURIComponent(s)}` }) },
  { name: 'GET /customers/:customerId/purchases', kind: 'customer', ok: 200, effect: 'listPurchases', request: (s) => ({ method: 'GET', path: `/customers/${s}/purchases` }) },
  { name: 'GET /customers/:customerId/invoices', kind: 'customer', ok: 200, effect: 'listInvoices', request: (s) => ({ method: 'GET', path: `/customers/${s}/invoices` }) },
  { name: 'GET /invoices/:id', kind: 'invoice', ok: 200, request: (s) => ({ method: 'GET', path: `/invoices/${s}` }) },
  { name: 'POST /customers/:customerId/setup-intent', kind: 'customer', ok: 200, effect: 'createSetupIntent', request: (s) => ({ method: 'POST', path: `/customers/${s}/setup-intent` }) },
  { name: 'GET /customers/:customerId/payment-methods', kind: 'customer', ok: 200, effect: 'listPaymentMethods', request: (s) => ({ method: 'GET', path: `/customers/${s}/payment-methods` }) },
  { name: 'POST /customers/:customerId/default-payment-method', kind: 'customer', ok: 200, effect: 'setDefaultPaymentMethod', request: (s) => ({ method: 'POST', path: `/customers/${s}/default-payment-method`, body: { paymentMethodId: 'pm_alice' } }) },
  { name: 'DELETE /payment-methods/:id', kind: 'paymentMethod', ok: 200, effect: 'detachPaymentMethod', request: (s) => ({ method: 'DELETE', path: `/payment-methods/${s}` }) },
];

async function send(principal: Record<string, unknown> | undefined, req: { method: string; path: string; body?: unknown }) {
  PRINCIPAL = principal;
  const res = await fetch(`${baseUrl}/billing${req.path}`, {
    method: req.method,
    headers: { 'content-type': 'application/json' },
    body: req.body === undefined ? undefined : JSON.stringify(req.body),
  });
  return { status: res.status, text: await res.text() };
}

const effectCalls = () => EFFECTS.reduce((n, k) => n + fake.mocks[k].mock.calls.length, 0);
const logged = () => JSON.stringify(Object.values(log).flatMap((m) => m.mock.calls));
