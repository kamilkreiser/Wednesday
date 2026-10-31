
// ============================ GATE 62 OWN CELLS ============================

/** Status, body and every response header except Date, which is the clock. */
async function sendFull(principal: Record<string, unknown> | undefined, req: { method: string; path: string; body?: unknown }) {
  PRINCIPAL = principal;
  const res = await fetch(`${baseUrl}/billing${req.path}`, {
    method: req.method,
    headers: { 'content-type': 'application/json' },
    body: req.body === undefined ? undefined : JSON.stringify(req.body),
  });
  const headers: Record<string, string> = {};
  res.headers.forEach((v, k) => { if (k !== 'date' && k !== 'keep-alive' && k !== 'connection') headers[k] = v; });
  return { status: res.status, headers, text: await res.text() };
}

const CONNECTOR = { userId: 'svc-connector', role: 'CONNECTOR', tenantId: 't-1' };
const SERVICE_NO_USER = { role: 'SERVICE', tenantId: 't-1' };
const ARRAY_ROLE = { userId: 'u-x', role: ['SYSTEM_ADMIN'], tenantId: 't-1' };
const ADMIN_PLAIN = { userId: 'u-adm', role: 'ADMIN', tenantId: 't-1' };
const ORG_OWNER_ROLE = { userId: 'u-own', role: 'OWNER', tenantId: 't-1' };
const DOTLESS = { userId: 'u-d', role: 'SYSTEM_ADMıN', tenantId: 't-1' };
const ALICE_NO_TENANT = { userId: 'u-alice', role: 'OWNER' };
const ALICE_UPPER = { userId: 'U-ALICE', role: 'OWNER', tenantId: 't-1' };

const REFUSED_PRINCIPALS: Array<[string, Record<string, unknown> | undefined]> = [
  ['BOB same tenant', BOB],
  ['ORG_ADMIN of owner tenant', CAROL_ORG_ADMIN],
  ['anonymous', undefined],
  ['connector token', CONNECTOR],
  ['service token without userId', SERVICE_NO_USER],
  ['array role [SYSTEM_ADMIN]', ARRAY_ROLE],
  ['role ADMIN', ADMIN_PLAIN],
  ['dotless-i SYSTEM_ADMIN', DOTLESS],
  ['owner userId but token has no tenant (customer records t-1)', ALICE_NO_TENANT],
  ['owner userId in other case', ALICE_UPPER],
];

describe.each(ROUTES)('G62 — $name: refused is byte-identical to unknown incl. headers', (route) => {
  const S = SUBJECTS[route.kind];
  it.each(REFUSED_PRINCIPALS)('G62-H %s', async (_l, principal) => {
    const before = fake.snapshot();
    const eff = effectCalls();
    const logsBefore = JSON.stringify(Object.values(log).flatMap((m) => m.mock.calls));
    const refused = await sendFull(principal, route.request(S.alice));
    expect(effectCalls() - eff).toBe(0);
    expect(fake.snapshot()).toBe(before);
    expect(JSON.stringify(Object.values(log).flatMap((m) => m.mock.calls))).toBe(logsBefore);
    const unknown = await sendFull(principal, route.request(S.unknown));
    expect(refused).toEqual(unknown);
    expect(refused.status).toBe(404);
  });
  it('G62-H control: the owner differs from unknown (instrument discriminates)', async () => {
    const own = await sendFull(ALICE, route.request(S.alice));
    const unknown = await sendFull(ALICE, route.request(S.unknown));
    expect(own).not.toEqual(unknown);
  });
});

describe('G62 — POST /customers cannot create for another user', () => {
  const post = (p: Record<string, unknown> | undefined, body: Record<string, unknown>) => sendFull(p, { method: 'POST', path: '/customers', body });
  it.each([
    ['ORG_ADMIN', CAROL_ORG_ADMIN],
    ['connector', CONNECTOR],
    ['service no userId', SERVICE_NO_USER],
    ['array role', ARRAY_ROLE],
    ['anonymous', undefined],
    ['OWNER', ORG_OWNER_ROLE],
  ])('G62-P1 %s posting userId u-alice is 403 with no Stripe call', async (_l, p) => {
    const res = await post(p, { email: 'x@a.test', userId: 'u-alice' });
    expect(res.status).toBe(403);
    expect(fake.mocks.createCustomer).not.toHaveBeenCalled();
    expect(fake.mocks.listCustomersByEmail).not.toHaveBeenCalled();
    expect(fake.mocks.findCustomerByEmail).not.toHaveBeenCalled();
  });
  it('G62-P2 anonymous posting an empty userId is 403', async () => {
    const res = await post(undefined, { email: 'x@a.test', userId: '' });
    expect(res.status).toBe(403);
    expect(fake.mocks.createCustomer).not.toHaveBeenCalled();
  });
  it('G62-P3 a body metadata.userId/tenantId on create is ignored: the owner is the caller', async () => {
    const res = await post(BOB, { email: 'y@a.test', userId: 'u-bob', metadata: { userId: 'u-alice', tenantId: 't-9' } });
    expect(res.status, res.text).toBe(201);
    const id = JSON.parse(res.text).customer.id;
    expect(fake.customers.get(id)?.metadata).toMatchObject({ userId: 'u-bob', tenantId: 't-1' });
  });
  it("G62-P4 ORG_ADMIN posting the owner's email gets a new customer of their own, not the owner's", async () => {
    const res = await post(CAROL_ORG_ADMIN, { email: 'alice@a.test', userId: 'u-carol' });
    expect(res.status, res.text).toBe(201);
    expect(res.text).not.toContain('cus_alice');
  });
});

describe('G62 — PUT /customers/:id reserved keys and owner change', () => {
  it.each([
    ['userId empty', { userId: '' }],
    ['tenantId empty', { tenantId: '' }],
  ])('G62-M %s is 400 and nothing written', async (_l, metadata) => {
    const before = fake.snapshot();
    const res = await sendFull(ALICE, { method: 'PUT', path: '/customers/cus_alice', body: { metadata } });
    expect(res.status).toBe(400);
    expect(fake.snapshot()).toBe(before);
  });
});
