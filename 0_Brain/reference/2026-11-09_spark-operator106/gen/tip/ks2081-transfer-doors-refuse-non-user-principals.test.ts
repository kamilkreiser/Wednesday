// KS-2081 (gate 229 F1): a non-user principal is never a party at the transfer write doors. Kam ruled it: card
// secuura-ks2038-connector-principals-on-transfer-doors-1106 = a, "Keys are never a party on these doors (recommended)".
// Nothing about the caller is stubbed here: tokens come from auth's real generateConnectorToken and generateAccessToken, or are signed
// by hand with the same key where a cell needs one claim alone, and the real authenticate() verifies them. The database is stubbed only
// so a key-opened row can be warmed through loadFromDb, because under this rule no key can open one through POST.
// Labels: a name starting RED fails at the branch's base by assertion; a name starting control passes there too, so it proves only by
// the planted mutants named in the PR.
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import crypto from 'crypto';
import http from 'http';
import type { AddressInfo } from 'net';
import jwt from 'jsonwebtoken';

const store = vi.hoisted(() => ({ available: false, rows: [] as Record<string, unknown>[] }));

vi.mock('../db', async (importOriginal) => {
  const actual = await importOriginal<typeof import('../db')>();
  return {
    ...actual,
    initDb: async () => false,
    isDbAvailable: () => store.available,
    query: async (sql: string) => ({ rows: store.available && sql.includes('FROM svc_transfers') ? store.rows : [], rowCount: 0 }),
  };
});

const { publicKey, privateKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }) as string;
process.env.JWT_PRIVATE_KEY = Buffer.from(PRIVATE_PEM).toString('base64');
process.env.JWT_PUBLIC_KEY = Buffer.from(publicKey.export({ type: 'spki', format: 'pem' }) as string).toString('base64');
delete process.env.DATABASE_URL;
delete process.env.JWT_JWKS_URL;
delete process.env.AUTH_SERVICE_URL;
process.env.PORT = '0';

const OWNER = '00000000-0000-4000-8000-00000000a001';
const RECIPIENT = '00000000-0000-4000-8000-00000000a002';
const INITIATOR = '00000000-0000-4000-8000-00000000a003';
const EXECUTOR = '00000000-0000-4000-8000-00000000a004';
const STRANGER = '00000000-0000-4000-8000-00000000f001';
const UPPER_INITIATOR = '00000000-0000-4000-8000-00000000ABCD';
const UNKNOWN_ID = '00000000-0000-4000-8000-0000000000ff';
const TENANT_A = 'a0000000-0000-4000-8000-000000000001';
const TENANT_B = 'b0000000-0000-4000-8000-000000000002';

// The refusal, byte for byte. Written out here and not imported, so a change to the product's text reds these cells.
const REFUSAL = '{"success":false,"error":{"code":"FORBIDDEN","message":"An API key cannot open or act on a transfer."}}';

type Reply = { status: number; data: any; raw: string; headers: http.IncomingHttpHeaders };
type Mint = typeof import('../../../auth/src/services/jwt');

let baseUrl = '';
let server: http.Server;
let mint: Mint;
let app: { default: http.RequestListener; loadFromDb: () => Promise<void> };

function call(token: string, method: string, path: string, body?: unknown): Promise<Reply> {
  return new Promise((resolve, reject) => {
    const url = new URL(path, baseUrl);
    const r = http.request(
      { hostname: url.hostname, port: url.port, path: url.pathname, method, agent: false, headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${token}` } },
      (res) => {
        let raw = '';
        res.on('data', (c) => (raw += c));
        res.on('end', () => {
          let data: any;
          try {
            data = raw ? JSON.parse(raw) : undefined;
          } catch {
            data = raw;
          }
          resolve({ status: res.statusCode || 0, data, raw, headers: res.headers });
        });
      },
    );
    r.on('error', reject);
    if (body !== undefined) r.write(typeof body === 'string' ? body : JSON.stringify(body));
    r.end();
  });
}

const person = (id: string, oauth?: { clientId: string; scopes: string[] }): string =>
  mint.generateAccessToken(
    { id, email: 'person@example.test', role: 'OWNER', verificationLevel: 'BASIC', tenantId: TENANT_A, tenantSlug: 'tenant-a' } as Parameters<Mint['generateAccessToken']>[0],
    'session-ks2081',
    oauth,
  );
const refreshTokenOf = (id: string): string =>
  mint.generateRefreshToken(
    { id, email: 'person@example.test', role: 'OWNER', verificationLevel: 'BASIC', tenantId: TENANT_A } as Parameters<Mint['generateRefreshToken']>[0],
    'session-ks2081',
  );
const key = (connectorId: string | null, tenantId: string): string => mint.generateConnectorToken({ connectorId, tenantId, scopes: [] }).token;
// A token only a test can make, for a shape no minter writes today: one signal alone on an otherwise ordinary person.
const handMade = (claims: object, options: jwt.SignOptions = {}): string => jwt.sign(claims, PRIVATE_PEM, { algorithm: 'RS256', expiresIn: 600, ...options });
const personClaims = (over: object = {}): object => ({ userId: INITIATOR, email: 'person@example.test', role: 'OWNER', verificationLevel: 'BASIC', type: 'access', tenantId: TENANT_A, ...over });

const docId = (): string => `doc-1700000000000-${crypto.randomBytes(4).toString('hex')}`;
const openBody = (over: object = {}): object => ({
  documentId: docId(),
  transferType: 'simple',
  currentOwnerId: OWNER,
  newOwnerId: RECIPIENT,
  documentHash: 'a'.repeat(64),
  documentTitle: 'ks2081',
  documentType: 'certificate',
  ...over,
});
const TYPE_FIELDS: Record<string, object> = {
  simple: {},
  sale: { saleAmount: 100, saleCurrency: 'USD' },
  inheritance: { executorId: EXECUTOR, deceasedId: OWNER, probateReference: 'P' },
  corporate: { corporateResolutionRef: 'R', boardApprovalRef: 'B' },
};
const open = async (type = 'simple', over: object = {}, token = person(INITIATOR)): Promise<string> => {
  const res = await call(token, 'POST', '/api/transfers', openBody({ transferType: type, ...TYPE_FIELDS[type], ...over }));
  if (res.status !== 201) throw new Error(`open ${type}: ${res.status} ${res.raw}`);
  return res.data.data.id as string;
};
const approveBody = (id: string): object => ({ approverId: id, approverRole: 'body-role' });
const rejectBody = (id: string): object => ({ rejectorId: id, rejectorRole: 'body-role', reason: 'ks2081' });

// A row as a key opened it before this rule: the stored form loadFromDb reads back at boot. Doors read the Map, so the row is warmed and the db goes away again.
const seedRow = async (initiatedBy: string, over: Record<string, unknown> = {}): Promise<string> => {
  const id = crypto.randomUUID();
  store.rows = [
    {
      id,
      document_id: docId(),
      document_hash: 'a'.repeat(64),
      document_title: 'ks2081',
      document_type: 'certificate',
      transfer_type: 'simple',
      current_owner_id: OWNER,
      new_owner_id: RECIPIENT,
      initiated_by: initiatedBy,
      required_approvals: 1,
      payment_verified: false,
      status: 'pending_approval',
      status_history: [],
      approvals: [],
      rejections: [],
      created_at: new Date().toISOString(),
      updated_at: new Date().toISOString(),
      ...over,
    },
  ];
  store.available = true;
  await app.loadFromDb();
  store.available = false;
  store.rows = [];
  return id;
};
const statusOf = async (id: string): Promise<string> => (await call(person(STRANGER), 'GET', `/api/transfers/${id}`)).data.data.status as string;

type Door = { name: string; path: (id: string) => string; body: () => object; bad: unknown };
const OPEN_DOORS: Door[] = [
  { name: 'open', path: () => '/api/transfers', body: openBody, bad: {} },
  { name: 'open alias', path: () => '/api/transfers/initiate', body: openBody, bad: {} },
];
const ID_DOORS: Door[] = [
  { name: 'approve', path: (id) => `/api/transfers/${id}/approve`, body: () => approveBody(RECIPIENT), bad: {} },
  { name: 'reject', path: (id) => `/api/transfers/${id}/reject`, body: () => rejectBody(RECIPIENT), bad: {} },
  { name: 'execute', path: (id) => `/api/transfers/${id}/execute`, body: () => ({}), bad: { reason: 7 } },
  { name: 'cancel', path: (id) => `/api/transfers/${id}/cancel`, body: () => ({ reason: 'ks2081' }), bad: { reason: 7 } },
];
const DOORS = [...OPEN_DOORS, ...ID_DOORS];

const KEYS: { name: string; token: () => string }[] = [
  { name: 'a key with no connector id', token: () => key(null, TENANT_A) },
  { name: 'a connector key', token: () => key('c-one', TENANT_A) },
  { name: 'a connector key of another tenant differing only in case', token: () => key('C-ONE', TENANT_B) },
];

// Everything a reply carries except the clock.
const fingerprint = (r: Reply): string => {
  const { date: _date, ...headers } = r.headers;
  return JSON.stringify({ status: r.status, raw: r.raw, headers: Object.entries(headers).sort() });
};

beforeAll(async () => {
  mint = await import('../../../auth/src/services/jwt');
  await mint.initJwtKeys();
  app = (await import('../index')) as unknown as typeof app;
  await new Promise<void>((resolve) => {
    server = (app.default as unknown as { listen: (p: number, h: string, cb: () => void) => http.Server }).listen(0, '127.0.0.1', () => resolve());
  });
  baseUrl = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
}, 60_000);

afterAll(() => new Promise<void>((resolve) => server.close(() => resolve())));

describe('KS-2081: the tokens this rule reads', () => {
  it('control D1 auth\'s real mint stamps every claim the rule reads, and two tenants\' no-id keys share one id', () => {
    const a = jwt.decode(key(null, TENANT_A)) as Record<string, unknown>;
    const b = jwt.decode(key(null, TENANT_B)) as Record<string, unknown>;
    const named = jwt.decode(key('c-one', TENANT_A)) as Record<string, unknown>;
    expect([a.type, a.role, a.verificationLevel, a.userId]).toEqual(['connector', 'connector', 'api_key', 'connector:api-key']);
    expect([named.type, named.role, named.verificationLevel, named.userId]).toEqual(['connector', 'connector', 'api_key', 'connector:c-one']);
    expect(b.userId).toBe(a.userId);
    expect(b.tenantId).not.toBe(a.tenantId);
  });

  it('control D2 auth\'s real mint gives a person a GUID id and none of the claims the rule refuses', () => {
    const p = jwt.decode(person(RECIPIENT)) as Record<string, unknown>;
    expect([p.type, p.role, p.verificationLevel, p.userId]).toEqual(['access', 'OWNER', 'BASIC', RECIPIENT]);
  });
});

describe('KS-2081: a key gets the one refusal at every write path', () => {
  const R1 = KEYS.flatMap((k) => DOORS.map((d) => ({ name: `RED R1 ${k.name} at ${d.name} reads the refusal`, k, d })));
  it.each(R1.map((r) => [r.name, r] as const))('%s', async (_n, { k, d }) => {
    const id = await open();
    const res = await call(k.token(), 'POST', d.path(id), d.body());
    expect(res.status).toBe(403);
    expect(res.raw).toBe(REFUSAL);
  });

  const R2 = DOORS.map((d) => ({ name: `RED R2 a key sending a body the door would refuse at ${d.name} still reads the refusal`, d }));
  it.each(R2.map((r) => [r.name, r] as const))('%s', async (_n, { d }) => {
    const id = await open();
    const res = await call(key(null, TENANT_A), 'POST', d.path(id), d.bad);
    expect(res.status).toBe(403);
    expect(res.raw).toBe(REFUSAL);
  });

  const R3 = ID_DOORS.map((d) => ({ name: `RED R3 ${d.name}: a key reads the same bytes for its own row, an unknown id and a malformed id`, d }));
  it.each(R3.map((r) => [r.name, r] as const))('%s', async (_n, { d }) => {
    const own = await seedRow('connector:api-key');
    const token = key(null, TENANT_A);
    const onOwn = await call(token, 'POST', d.path(own), d.body());
    const onUnknown = await call(token, 'POST', d.path(UNKNOWN_ID), d.body());
    const onMalformed = await call(token, 'POST', d.path('not-an-id'), d.body());
    expect(onOwn.status).toBe(403);
    expect(fingerprint(onUnknown)).toBe(fingerprint(onOwn));
    expect(fingerprint(onMalformed)).toBe(fingerprint(onOwn));
  });
});

describe('KS-2081: gate 229 F1, a row a key opened', () => {
  it('RED R4 a no-id key of another tenant cannot cancel a row a no-id key opened', async () => {
    const id = await seedRow('connector:api-key');
    const res = await call(key(null, TENANT_B), 'POST', `/api/transfers/${id}/cancel`, { reason: 'ks2081' });
    expect(res.status).toBe(403);
    expect(res.raw).toBe(REFUSAL);
    expect(await statusOf(id)).toBe('pending_approval');
  });

  it('RED R4 a connector id of another tenant differing only in case cannot cancel it', async () => {
    const id = await seedRow('connector:c-one');
    const res = await call(key('C-ONE', TENANT_B), 'POST', `/api/transfers/${id}/cancel`, { reason: 'ks2081' });
    expect(res.status).toBe(403);
    expect(res.raw).toBe(REFUSAL);
    expect(await statusOf(id)).toBe('pending_approval');
  });

  it('RED R4 the key that opened a row cannot cancel it either', async () => {
    const id = await seedRow('connector:c-one');
    const res = await call(key('c-one', TENANT_A), 'POST', `/api/transfers/${id}/cancel`, { reason: 'ks2081' });
    expect(res.status).toBe(403);
    expect(res.raw).toBe(REFUSAL);
    expect(await statusOf(id)).toBe('pending_approval');
  });

  it('control N5 a named party can still reject a row a key opened', async () => {
    const id = await seedRow('connector:api-key');
    const res = await call(person(OWNER), 'POST', `/api/transfers/${id}/reject`, rejectBody(OWNER));
    expect(res.status).toBe(200);
    expect(await statusOf(id)).toBe('rejected');
  });
});

describe('KS-2081: a refused open writes nothing', () => {
  const R5 = OPEN_DOORS.map((d) => ({ name: `RED R5 a key at ${d.name} leaves no transfer and no notification`, d }));
  it.each(R5.map((r) => [r.name, r] as const))('%s', async (_n, { d }) => {
    const before = (await call(person(STRANGER), 'GET', '/api/transfers?limit=1')).data.data.total as number;
    const named = crypto.randomUUID();
    const documentId = docId();
    const res = await call(key(null, TENANT_A), 'POST', d.path(''), openBody({ documentId, newOwnerId: named }));
    expect(res.status).toBe(403);
    expect((await call(person(STRANGER), 'GET', '/api/transfers?limit=1')).data.data.total).toBe(before);
    expect((await call(person(STRANGER), 'GET', `/api/transfers/document/${documentId}`)).data.data.count).toBe(0);
    expect((await call(person(named), 'GET', '/api/notifications')).data.data.notifications).toHaveLength(0);
  });

  // The instrument above must be able to see a write, or its zeros say nothing.
  it('control R5 a person opening the same way leaves a transfer and a notification those reads can see', async () => {
    const before = (await call(person(STRANGER), 'GET', '/api/transfers?limit=1')).data.data.total as number;
    const named = crypto.randomUUID();
    const documentId = docId();
    const res = await call(person(INITIATOR), 'POST', '/api/transfers', openBody({ documentId, newOwnerId: named }));
    expect(res.status).toBe(201);
    expect((await call(person(STRANGER), 'GET', '/api/transfers?limit=1')).data.data.total).toBe(before + 1);
    expect((await call(person(STRANGER), 'GET', `/api/transfers/document/${documentId}`)).data.data.count).toBe(1);
    expect((await call(person(named), 'GET', '/api/notifications')).data.data.notifications).toHaveLength(1);
  });
});

describe('KS-2081: the test reads each signal on its own', () => {
  const R6 = DOORS.map((d) => ({ name: `RED R6 a connector type with no user id at ${d.name} reads the refusal, not 401`, d }));
  it.each(R6.map((r) => [r.name, r] as const))('%s', async (_n, { d }) => {
    const { userId: _userId, ...claims } = personClaims({ type: 'connector' }) as Record<string, unknown>;
    const id = await open();
    const res = await call(handMade(claims), 'POST', d.path(id), d.body());
    expect(res.status).toBe(403);
    expect(res.raw).toBe(REFUSAL);
  });

  const GUID_SIGNALS: { name: string; over: object }[] = [
    { name: 'type connector alone', over: { type: 'connector' } },
    { name: 'role connector alone', over: { role: 'connector' } },
    { name: 'verificationLevel api_key alone', over: { verificationLevel: 'api_key' } },
  ];
  const C1 = GUID_SIGNALS.map((s) => ({ name: `RED C1 ${s.name} on a named initiator's own transfer: cancel reads the refusal`, s }));
  it.each(C1.map((r) => [r.name, r] as const))('%s', async (_n, { s }) => {
    const id = await open();
    const res = await call(handMade(personClaims(s.over)), 'POST', `/api/transfers/${id}/cancel`, { reason: 'ks2081' });
    expect(res.status).toBe(403);
    expect(res.raw).toBe(REFUSAL);
    expect(await statusOf(id)).toBe('pending_approval');
  });

  const C2 = GUID_SIGNALS.map((s) => ({ name: `RED C2 ${s.name}: open reads the refusal`, s }));
  it.each(C2.map((r) => [r.name, r] as const))('%s', async (_n, { s }) => {
    const res = await call(handMade(personClaims(s.over)), 'POST', '/api/transfers', openBody());
    expect(res.status).toBe(403);
    expect(res.raw).toBe(REFUSAL);
  });

  const NON_GUID = ['connector:someone', 'svc:billing', 'not-a-guid'];
  const C3 = NON_GUID.map((userId) => ({ name: `RED C3 an id of ${userId} and every other claim a person's: cancel of its own row reads the refusal`, userId }));
  it.each(C3.map((r) => [r.name, r] as const))('%s', async (_n, { userId }) => {
    const id = await seedRow(userId);
    const res = await call(handMade(personClaims({ userId })), 'POST', `/api/transfers/${id}/cancel`, { reason: 'ks2081' });
    expect(res.status).toBe(403);
    expect(res.raw).toBe(REFUSAL);
    expect(await statusOf(id)).toBe('pending_approval');
  });

  const C4 = NON_GUID.map((userId) => ({ name: `RED C4 an id of ${userId} and every other claim a person's: open reads the refusal`, userId }));
  it.each(C4.map((r) => [r.name, r] as const))('%s', async (_n, { userId }) => {
    const res = await call(handMade(personClaims({ userId })), 'POST', '/api/transfers', openBody());
    expect(res.status).toBe(403);
    expect(res.raw).toBe(REFUSAL);
  });
});

// Kam's rule for people, written out by hand and NOT imported from the product, and read through the real authenticator with auth's real
// mint. Gate 229 measured these 40 rows on PR 2048; this PR changes none of them.
// Each row is [approve, reject, execute, cancel]. "+executor" names an executor on a type that does not need one, which POST allows.
// 400 on execute means the caller passed and the transfer's own state refused it.
type People = Record<'owner' | 'recipient' | 'initiator' | 'executor' | 'stranger', [number, number, number, number]>;
const PEOPLE_IDS: Record<keyof People, string> = { owner: OWNER, recipient: RECIPIENT, initiator: INITIATOR, executor: EXECUTOR, stranger: STRANGER };
const NOBODY: [number, number, number, number] = [404, 404, 404, 404];
const INITIATOR_ROW: [number, number, number, number] = [403, 403, 403, 200];
const PEOPLE: { label: string; type: string; over: object; rows: People }[] = [
  { label: 'simple', type: 'simple', over: {}, rows: { owner: [403, 200, 200, 403], recipient: [200, 200, 403, 403], initiator: INITIATOR_ROW, executor: NOBODY, stranger: NOBODY } },
  { label: 'sale', type: 'sale', over: {}, rows: { owner: [200, 200, 400, 403], recipient: [200, 200, 403, 403], initiator: INITIATOR_ROW, executor: NOBODY, stranger: NOBODY } },
  { label: 'inheritance', type: 'inheritance', over: {}, rows: { owner: [403, 200, 403, 403], recipient: [200, 200, 403, 403], initiator: INITIATOR_ROW, executor: [200, 200, 200, 403], stranger: NOBODY } },
  { label: 'corporate', type: 'corporate', over: {}, rows: { owner: [403, 200, 400, 403], recipient: [403, 200, 403, 403], initiator: INITIATOR_ROW, executor: NOBODY, stranger: NOBODY } },
  { label: 'simple+executor', type: 'simple', over: { executorId: EXECUTOR }, rows: { owner: [403, 200, 200, 403], recipient: [200, 200, 403, 403], initiator: INITIATOR_ROW, executor: [403, 200, 403, 403], stranger: NOBODY } },
  { label: 'sale+executor', type: 'sale', over: { executorId: EXECUTOR }, rows: { owner: [200, 200, 400, 403], recipient: [200, 200, 403, 403], initiator: INITIATOR_ROW, executor: [403, 200, 403, 403], stranger: NOBODY } },
  { label: 'corporate+executor', type: 'corporate', over: { executorId: EXECUTOR }, rows: { owner: [403, 200, 400, 403], recipient: [403, 200, 403, 403], initiator: INITIATOR_ROW, executor: [403, 200, 403, 403], stranger: NOBODY } },
  { label: 'inheritance with no executor', type: 'inheritance', over: { executorId: undefined }, rows: { owner: [403, 200, 403, 403], recipient: [200, 200, 403, 403], initiator: INITIATOR_ROW, executor: NOBODY, stranger: NOBODY } },
];

describe('KS-2081: the rule for people does not move', () => {
  const approveAs = (who: string, id: string) => call(person(who), 'POST', `/api/transfers/${id}/approve`, approveBody(who));
  // Bring a transfer to the state execute is asked about, by the parties the rule lets approve it.
  const ready = async (type: string, over: object): Promise<string> => {
    const id = await open(type, over);
    if (type === 'simple') await approveAs(RECIPIENT, id);
    if (type === 'sale') {
      await approveAs(OWNER, id);
      await approveAs(RECIPIENT, id);
    }
    if (type === 'inheritance') {
      if (!('executorId' in over)) await approveAs(EXECUTOR, id);
      await approveAs(RECIPIENT, id);
    }
    return id;
  };
  const P1 = PEOPLE.flatMap((t) => (Object.keys(t.rows) as (keyof People)[]).map((who) => ({ name: `control P1 ${t.label} by ${who}`, t, who })));
  it.each(P1.map((r) => [r.name, r] as const))('%s', async (_n, { t, who }) => {
    const uid = PEOPLE_IDS[who];
    const token = person(uid);
    let id = await open(t.type, t.over);
    const approve = (await call(token, 'POST', `/api/transfers/${id}/approve`, approveBody(uid))).status;
    id = await open(t.type, t.over);
    const reject = (await call(token, 'POST', `/api/transfers/${id}/reject`, rejectBody(uid))).status;
    id = await ready(t.type, t.over);
    const execute = (await call(token, 'POST', `/api/transfers/${id}/execute`)).status;
    id = await open(t.type, t.over);
    const cancel = (await call(token, 'POST', `/api/transfers/${id}/cancel`, { reason: 'ks2081' })).status;
    expect([approve, reject, execute, cancel]).toEqual(t.rows[who]);
  });

  it('control P2 a person\'s OAuth-minted token opens and approves as that person', async () => {
    const oauth = { clientId: 'app-ks2081', scopes: ['documents:read'] };
    const id = await open('simple', {}, person(INITIATOR, oauth));
    const res = await call(person(RECIPIENT, oauth), 'POST', `/api/transfers/${id}/approve`, approveBody(RECIPIENT));
    expect(res.status).toBe(200);
  });

  it('control P3 a person\'s refresh-typed token is unchanged: gate 229 F8 as it stands, not a rule', async () => {
    const id = await open();
    const res = await call(refreshTokenOf(RECIPIENT), 'POST', `/api/transfers/${id}/approve`, approveBody(RECIPIENT));
    expect(res.status).toBe(200);
  });

  it('control P4 a person whose id is an upper-case GUID opens and cancels their own', async () => {
    const token = person(UPPER_INITIATOR);
    const id = await open('simple', {}, token);
    const res = await call(token, 'POST', `/api/transfers/${id}/cancel`, { reason: 'ks2081' });
    expect(res.status).toBe(200);
  });

  const NO_ID: { name: string; over: object | null }[] = [
    { name: 'a token with no user id', over: null },
    { name: 'an empty user id', over: { userId: '' } },
    { name: 'a null user id', over: { userId: null } },
    { name: 'a number as user id', over: { userId: 7 } },
    { name: 'an array as user id', over: { userId: [INITIATOR] } },
  ];
  const P5 = NO_ID.map((s) => ({ name: `control P5 ${s.name} keeps today's answers: 401 at the id doors, the open door's 201`, s }));
  it.each(P5.map((r) => [r.name, r] as const))('%s', async (_n, { s }) => {
    const { userId: _userId, ...claims } = personClaims() as Record<string, unknown>;
    const token = handMade(s.over ? { ...claims, ...s.over } : claims);
    const id = await open();
    for (const d of ID_DOORS) {
      expect((await call(token, 'POST', d.path(id), d.body())).status).toBe(401);
    }
    expect((await call(token, 'POST', '/api/transfers', openBody())).status).toBe(201);
    expect(await statusOf(id)).toBe('pending_approval');
  });
});

describe('KS-2081: what stays as it is', () => {
  const claims = { userId: 'connector:api-key', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector' };
  it('control P6 a connector-shaped token with a bad signature reads 401, not the refusal', async () => {
    const other = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 }).privateKey.export({ type: 'pkcs8', format: 'pem' }) as string;
    const token = jwt.sign(claims, other, { algorithm: 'RS256', expiresIn: 600 });
    expect((await call(token, 'POST', '/api/transfers', openBody())).status).toBe(401);
    expect((await call(token, 'POST', `/api/transfers/${UNKNOWN_ID}/cancel`, {})).status).toBe(401);
  });

  it('control P6 an expired connector-shaped token reads 401, not the refusal', async () => {
    const token = handMade(claims, { expiresIn: -60 });
    expect((await call(token, 'POST', '/api/transfers', openBody())).status).toBe(401);
    expect((await call(token, 'POST', `/api/transfers/${UNKNOWN_ID}/cancel`, {})).status).toBe(401);
  });

  // Today's state and NOT a rule: any signed-in caller can read these, and the reads are KS-1703's. When that lands this cell changes, knowingly.
  it('control P7 a key can still read all four GET doors', async () => {
    const documentId = docId();
    const id = await open('simple', { documentId });
    const token = key(null, TENANT_A);
    expect((await call(token, 'GET', '/api/transfers')).status).toBe(200);
    expect((await call(token, 'GET', `/api/transfers/${id}`)).status).toBe(200);
    expect((await call(token, 'GET', `/api/transfers/${id}/history`)).status).toBe(200);
    expect((await call(token, 'GET', `/api/transfers/document/${documentId}`)).status).toBe(200);
  });

  // The body parser runs before the authenticator, so this answer is the same for any caller and any id: it says nothing about a transfer.
  it('control P8 unparseable JSON from a key reads the parser\'s answer for its own row and an unknown id alike', async () => {
    const own = await seedRow('connector:api-key');
    const token = key(null, TENANT_A);
    const onOwn = await call(token, 'POST', `/api/transfers/${own}/cancel`, '{not json');
    const onUnknown = await call(token, 'POST', `/api/transfers/${UNKNOWN_ID}/cancel`, '{not json');
    expect(onOwn.status).toBe(400);
    expect(fingerprint(onUnknown)).toBe(fingerprint(onOwn));
    expect(await statusOf(own)).toBe('pending_approval');
  });
});
