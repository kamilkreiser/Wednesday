/**
 * KS-1202 — a create whose data.documentType differs from the resolved type is refused.
 *
 * Originate stored the checked type (`documentType || type || 'DOCUMENT'`) but served
 * `data.documentType || type`, so a document created as an allowed type with a different
 * `data.documentType` (PROPERTY_DEED, SSD_DOCUMENT, DEGREE) was served, and verified, as that
 * other type. Measured on this router before the change (KS-1202 comment 00260d56). A present
 * `data.documentType` must now equal the resolved type; it is refused 400, never overwritten.
 *
 * Harness: the real documentsRouter (POST /, GET /:id) over an in-memory documentRepo that keeps
 * exactly the record the create handler saved; the real isAllowedByRoleOrScope; the other mocks
 * as the KS-549 suite's. Three write-capable principals: a connector with documents:write, an
 * ISSUER_ADMIN and a SYSTEM_ADMIN.
 */
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@127.0.0.1:1/test';
process.env.SIMULATE_ANCHORING = 'true';

const store = new Map<string, any>();
const saved: any[] = [];


jest.mock('../repositories/documentRepo', () => ({
  getDocument: jest.fn(async (id: string) => store.get(id) ?? null),
  listDocuments: jest.fn(async () => ({ items: [...store.values()], total: store.size })),
  saveDocument: jest.fn(async (record: any) => {
    const copy = JSON.parse(JSON.stringify(record));
    if (!Array.isArray(copy.signatures)) copy.signatures = [];
    store.set(copy.id, copy);
    saved.push(copy);
    return { dbId: '99999999-9999-4999-8999-999999999999', inserted: true };
  }),
  updateDocument: jest.fn(async () => undefined),
  getSigningRequest: jest.fn(),
  saveSigningRequest: jest.fn(),
  deleteSigningRequest: jest.fn(),
  generateContentHash: jest.fn(() => 'a'.repeat(64)),
  seedDemoDocuments: jest.fn(async () => undefined),
  assertNoCycle: jest.fn(async () => undefined),
  getOrganizationExternalRef: jest.fn(async () => null),
}));
jest.mock('../repositories/shareRepo', () => ({ createShare: jest.fn() }));
jest.mock('../repositories/lifecycleEventRepo', () => ({ createLifecycleEvent: jest.fn(), setLifecycleEventAnchor: jest.fn(), listLifecycleEvents: jest.fn() }));
jest.mock('../events', () => ({ publishEvent: jest.fn(async () => undefined), EventTypes: { DOCUMENT_CREATED: 'document.created', DOCUMENT_OWNERSHIP_TRANSFERRED: 'document.ownership_transferred', DOCUMENT_VERSIONED: 'document.versioned' } }));
jest.mock('../services/threadTokenClient', () => ({ mintAndRegisterThreadToken: jest.fn(async () => ({})) }));
jest.mock('../routes/verification', () => ({ registerInPlatformRegistry: jest.fn(async () => undefined) }));
jest.mock('../services/anchorStateSync', () => ({ pollAnchorUntilConfirmed: jest.fn(async () => undefined), reconcileDocumentAnchorState: jest.fn(async (d: any) => d) }));
jest.mock('../services/provenance', () => {
  const actual = jest.requireActual('../services/provenance');
  return { ...actual, recordActionProvenance: jest.fn(async () => undefined), getCreationProvenance: jest.fn(async () => null), wasCreatedByConnector: jest.fn(async () => false) };
});
jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = JSON.parse(String(req.headers['x-probe-user'] || '{}'));
    next();
  },
}));
jest.mock('../utils/logger', () => ({ logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() } }));

import express from 'express';
import { documentsRouter } from '../routes/documents';


const TENANT = 'a0000000-0000-4000-8000-000000000001';
const PRINCIPALS: Array<[string, Record<string, unknown>]> = [
  ['connector with documents:write', { userId: 'connector:ks1202-conn', role: 'connector', scopes: ['documents:write'], organizationId: 'd0000000-0000-4000-8000-000000001202', tenantId: TENANT }],
  ['ISSUER_ADMIN', { userId: '11111111-2222-4333-8444-555555551202', role: 'ISSUER_ADMIN', verificationLevel: 'none', tenantId: TENANT }],
  ['SYSTEM_ADMIN', { userId: '11111111-2222-4333-8444-555555551203', role: 'SYSTEM_ADMIN', tenantId: TENANT }],
];

const app = express();
app.use((req: any, _res, next) => { req.tenantId = TENANT; next(); });
app.use('/api/documents', express.json(), documentsRouter);
let base = '';
let server: ReturnType<typeof app.listen>;
beforeAll(async () => {
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  const a = server.address();
  base = 'http://127.0.0.1:' + String(typeof a === 'object' && a ? a.port : 0);
});
afterAll(() => server?.close());
beforeEach(() => { store.clear(); saved.length = 0; });

async function create(principal: Record<string, unknown>, body: unknown): Promise<{ status: number; code: unknown; saved: number; storedType: unknown; servedType: unknown }> {
  const headers = { 'content-type': 'application/json', 'x-probe-user': JSON.stringify(principal) };
  const post = await fetch(base + '/api/documents', { method: 'POST', headers, body: JSON.stringify(body) });
  const pj: any = await post.json().catch(() => null);
  const rec = saved.length > 0 ? saved[saved.length - 1] : null;
  let servedType: unknown = null;
  if (rec) {
    const g = await fetch(base + '/api/documents/' + encodeURIComponent(rec.id), { headers });
    servedType = ((await g.json().catch(() => null)) as any)?.documentType ?? null;
  }
  return { status: post.status, code: pj?.error?.code ?? null, saved: saved.length, storedType: rec?.type ?? null, servedType };
}

describe.each(PRINCIPALS)('KS-1202 as %s', (_name, principal) => {
  it.each([
    ['the gate typed carrier: type DOCUMENT, data.documentType PROPERTY_DEED', { title: 'qa', type: 'DOCUMENT', data: { title: 'qa', documentType: 'PROPERTY_DEED' } }],
    ['documentType DOCUMENT, data.documentType SSD_DOCUMENT', { documentType: 'DOCUMENT', title: 'qa', data: { title: 'qa', documentType: 'SSD_DOCUMENT' } }],
    ['no top-level type (resolves DOCUMENT), data.documentType DEGREE', { data: { title: 'qa', documentType: 'DEGREE' } }],
  ])('RED KS-1202 - %s: refused 400, nothing saved', async (_label, body) => {
    expect(await create(principal, body)).toEqual({ status: 400, code: 'BAD_REQUEST', saved: 0, storedType: null, servedType: null });
  });

  it('GREEN control - a data.documentType equal to the resolved type is still created and served as that type', async () => {
    expect(await create(principal, { title: 'qa', documentType: 'DEGREE', data: { title: 'qa', documentType: 'DEGREE' } })).toEqual({ status: 201, code: null, saved: 1, storedType: 'DEGREE', servedType: 'DEGREE' });
  });

  it('control - the portal shape (no data blob) is created and served as its documentType', async () => {
    expect(await create(principal, { title: 'qa', documentType: 'DOCUMENT' })).toEqual({ status: 201, code: null, saved: 1, storedType: 'DOCUMENT', servedType: 'DOCUMENT' });
  });

  it('control - the legacy shape without data.documentType is created and served as its type', async () => {
    expect(await create(principal, { title: 'qa', type: 'CERTIFICATE', data: { title: 'qa' } })).toEqual({ status: 201, code: null, saved: 1, storedType: 'CERTIFICATE', servedType: 'CERTIFICATE' });
  });
  it('KS-1202 N-B - the legacy shape with a MATCHING data.documentType (type DEGREE, data DEGREE) is created and served as DEGREE', async () => {
    expect(await create(principal, { title: 'qa', type: 'DEGREE', data: { title: 'qa', documentType: 'DEGREE' } })).toEqual({ status: 201, code: null, saved: 1, storedType: 'DEGREE', servedType: 'DEGREE' });
  });
  it('KS-1202 N-B - a data.documentType that differs only in CASE (type DEGREE, data degree) is refused 400, nothing saved', async () => {
    expect(await create(principal, { title: 'qa', type: 'DEGREE', data: { title: 'qa', documentType: 'degree' } })).toEqual({ status: 400, code: 'BAD_REQUEST', saved: 0, storedType: null, servedType: null });
  });
});

it('RED KS-1202 - a non-string data.documentType is refused 400, nothing saved', async () => {
  expect(await create(PRINCIPALS[0][1], { title: 'qa', documentType: 'DOCUMENT', data: { title: 'qa', documentType: 7 } })).toEqual({ status: 400, code: 'BAD_REQUEST', saved: 0, storedType: null, servedType: null });
});
