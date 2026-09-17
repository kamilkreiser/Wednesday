/**
 * qa1024-drafter-probe — #1024 (KS-1202) drafter rows, NOT a seat test. Harness = the seat's ks1202 test harness (real documentsRouter, in-memory
 * documentRepo keeping the JSON copy saveDocument received, real isAllowedByRoleOrScope, the KS-549 mocks) + rows the seat's 19 cells do not have:
 * carriers (case / null / '' / array / object / ZWSP / Cyrillic / __proto__ / duplicate key / escaped key / array type / text/plain), the list read,
 * a LEGACY stored row whose data.documentType already differs (readable? served as?), and the /:id/version writer (metadata.documentType).
 * Rows are written as JSON to QA1024_ROWS_OUT; every expectation is recorded, never asserted, except the instrument controls at the end.
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
    store.set(copy.id, copy); saved.push(copy);
    return { dbId: '99999999-9999-4999-8999-999999999999', inserted: true };
  }),
  updateDocument: jest.fn(async () => undefined),
  getSigningRequest: jest.fn(), saveSigningRequest: jest.fn(), deleteSigningRequest: jest.fn(),
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
  authenticate: () => (req: any, _res: unknown, next: () => void) => { req.user = JSON.parse(String(req.headers['x-probe-user'] || '{}')); next(); },
}));
jest.mock('../utils/logger', () => ({ logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() } }));

import express from 'express';
import * as fs from 'fs';
import { documentsRouter } from '../routes/documents';

const TENANT = 'a0000000-0000-4000-8000-000000000001';
const PRINCIPALS: Array<[string, Record<string, unknown>]> = [
  ['connector', { userId: 'connector:qa1024-conn', role: 'connector', scopes: ['documents:write'], organizationId: 'd0000000-0000-4000-8000-000000001024', tenantId: TENANT }],
  ['ISSUER_ADMIN', { userId: '11111111-2222-4333-8444-555555551024', role: 'ISSUER_ADMIN', verificationLevel: 'none', tenantId: TENANT }],
];
const app = express();
app.use((req: any, _res, next) => { req.tenantId = TENANT; next(); });
app.use('/api/documents', express.json(), documentsRouter);
let base = ''; let server: ReturnType<typeof app.listen>;
const rows: any[] = [];
beforeAll(async () => { await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); }); const a = server.address(); base = 'http://127.0.0.1:' + String(typeof a === 'object' && a ? a.port : 0); });
afterAll(() => { server?.close(); fs.writeFileSync(String(process.env.QA1024_ROWS_OUT || '/dev/null'), JSON.stringify(rows, null, 1)); });
beforeEach(() => { store.clear(); saved.length = 0; });

async function served(headers: Record<string, string>, id: string) {
  const g = await fetch(base + '/api/documents/' + encodeURIComponent(id), { headers });
  const gj: any = await g.json().catch(() => null);
  const l = await fetch(base + '/api/documents', { headers });
  const lj: any = await l.json().catch(() => null);
  const li = (lj?.documents || []).find((d: any) => d.id === id);
  return { getStatus: g.status, servedType: gj?.documentType ?? null, listStatus: l.status, listType: li ? li.documentType : 'NOT LISTED' };
}
async function create(principal: Record<string, unknown>, raw: string, ctype = 'application/json') {
  const headers = { 'x-probe-user': JSON.stringify(principal) };
  const post = await fetch(base + '/api/documents', { method: 'POST', headers: { ...headers, 'content-type': ctype }, body: raw });
  const pj: any = await post.json().catch(() => null);
  const rec = saved.length > 0 ? saved[saved.length - 1] : null;
  const s = rec ? await served(headers, rec.id) : null;
  return { status: post.status, code: pj?.error?.code ?? null, message: pj?.error?.message ?? null, saved: saved.length, storedType: rec ? rec.type : null, storedDataType: rec ? (rec.data?.documentType ?? 'ABSENT') : null, ...(s || {}) };
}
const J = (o: unknown) => JSON.stringify(o);
const CARRIERS: Array<[string, string, string, string]> = [
  // id, raw body, content-type, drafter prediction at head (dev column predicted in DRAFTER_REPORT)
  ['C01 case variant data degree vs documentType DEGREE', J({ title: 'qa', documentType: 'DEGREE', data: { title: 'qa', documentType: 'degree' } }), 'application/json', '400'],
  ['C02 type DEGREE + data DEGREE', J({ title: 'qa', type: 'DEGREE', data: { title: 'qa', documentType: 'DEGREE' } }), 'application/json', '201 DEGREE/DEGREE'],
  ['C03 documentType empty + type DEGREE + data DEGREE', J({ title: 'qa', documentType: '', type: 'DEGREE', data: { title: 'qa', documentType: 'DEGREE' } }), 'application/json', '201 DEGREE/DEGREE'],
  ['C04 untyped + data DOCUMENT', J({ data: { title: 'qa', documentType: 'DOCUMENT' } }), 'application/json', '201 DOCUMENT/DOCUMENT'],
  ['C05 data null', J({ title: 'qa', type: 'DOCUMENT', data: { title: 'qa', documentType: null } }), 'application/json', '400'],
  ['C06 data empty string', J({ title: 'qa', type: 'DOCUMENT', data: { title: 'qa', documentType: '' } }), 'application/json', '400'],
  ['C07 data array', J({ title: 'qa', type: 'DOCUMENT', data: { title: 'qa', documentType: ['DOCUMENT'] } }), 'application/json', '400'],
  ['C08 data object', J({ title: 'qa', type: 'DOCUMENT', data: { title: 'qa', documentType: { toString: 'DOCUMENT' } } }), 'application/json', '400'],
  ['C09 data ZWSP suffix', J({ title: 'qa', type: 'DOCUMENT', data: { title: 'qa', documentType: 'DOCUMENT​' } }), 'application/json', '400'],
  ['C10 data Cyrillic O', J({ title: 'qa', type: 'DOCUMENT', data: { title: 'qa', documentType: 'DОCUMENT' } }), 'application/json', '400'],
  ['C11 data __proto__ carrier', '{"title":"qa","type":"DOCUMENT","data":{"title":"qa","__proto__":{"documentType":"PROPERTY_DEED"}}}', 'application/json', '201 DOCUMENT/DOCUMENT'],
  ['C12 duplicate key last DOCUMENT', '{"title":"qa","type":"DOCUMENT","data":{"title":"qa","documentType":"PROPERTY_DEED","documentType":"DOCUMENT"}}', 'application/json', '201 DOCUMENT/DOCUMENT'],
  ['C13 duplicate key last PROPERTY_DEED', '{"title":"qa","type":"DOCUMENT","data":{"title":"qa","documentType":"DOCUMENT","documentType":"PROPERTY_DEED"}}', 'application/json', '400'],
  ['C14 escaped key documentTyp\\u0065', '{"title":"qa","type":"DOCUMENT","data":{"title":"qa","documentTyp\\u0065":"PROPERTY_DEED"}}', 'application/json', '400'],
  ['C15 type array + data DOCUMENT', J({ title: 'qa', type: ['DOCUMENT'], data: { title: 'qa', documentType: 'DOCUMENT' } }), 'application/json', '400'],
  ['C16 type array, no data', J({ title: 'qa', type: ['PROPERTY_DEED'] }), 'application/json', 'unpredicted (type is not string-checked)'],
  ['C17 documentType wins over type; data = type', J({ title: 'qa', documentType: 'PROPERTY_DEED', type: 'DOCUMENT', data: { title: 'qa', documentType: 'DOCUMENT' } }), 'application/json', '400'],
  ['C18 text/plain carrier', J({ title: 'qa', type: 'DOCUMENT', data: { title: 'qa', documentType: 'PROPERTY_DEED' } }), 'text/plain', 'not 201 (body unparsed)'],
  ['C19 portal shape + top-level documentType only', J({ title: 'qa', documentType: 'DEGREE', contentHash: 'b'.repeat(64) }), 'application/json', '201 DEGREE/DEGREE'],
  ['C20 add-in shape (MIME documentType, metadata, hash)', J({ title: 'qa', hash: 'c'.repeat(64), documentType: 'application/pdf', source: 'outlook-addin', metadata: { registeredVia: 'secuura-outlook-addin' } }), 'application/json', 'unchanged dev = head'],
  ['C21 data blob without documentType + documentType', J({ title: 'qa', documentType: 'DEGREE', data: { title: 'qa' } }), 'application/json', '201 DEGREE/DEGREE (filled)'],
  ['C22 data.documentType equal, differently cased top-level', J({ title: 'qa', documentType: 'degree', data: { title: 'qa', documentType: 'degree' } }), 'application/json', '201 degree/degree'],
  ['C23 gate typed carrier (seat row, reproduced)', J({ title: 'qa', type: 'DOCUMENT', data: { title: 'qa', documentType: 'PROPERTY_DEED' } }), 'application/json', '400'],
];
describe.each(PRINCIPALS)('qa1024 carriers as %s', (pname, principal) => {
  it.each(CARRIERS)('%s', async (id, raw, ctype, predicted) => {
    const r = await create(principal, raw, ctype);
    rows.push({ kind: 'carrier', principal: pname, id, predicted, ...r, storedEqualsServed: r.saved ? r.storedType === (r as any).servedType : null });
  });
});
describe.each(PRINCIPALS)('qa1024 writers + legacy as %s', (pname, principal) => {
  const headers = { 'x-probe-user': JSON.stringify(principal), 'content-type': 'application/json' };
  const version = async (id: string, metadata: Record<string, unknown> | undefined) => {
    const n0 = saved.length;
    const v = await fetch(base + '/api/documents/' + encodeURIComponent(id) + '/version', { method: 'POST', headers, body: J({ action: 'watermark', newContentHash: 'd'.repeat(64), ...(metadata ? { metadata } : {}) }) });
    const vj: any = await v.json().catch(() => null);
    const rec = saved.length > n0 ? saved[saved.length - 1] : null;
    const s = rec ? await served(headers, rec.id) : null;
    return { status: v.status, code: vj?.error?.code ?? null, message: vj?.error?.message ?? null, derivedSaved: saved.length - n0, storedType: rec ? rec.type : null, storedDataType: rec ? (rec.data?.documentType ?? 'ABSENT') : null, ...(s || {}) };
  };
  it('W01 version with metadata.documentType PROPERTY_DEED of a DOCUMENT', async () => {
    const c = await create(principal, J({ title: 'qa', documentType: 'DOCUMENT' }));
    const src = saved[saved.length - 1];
    rows.push({ kind: 'writer', principal: pname, id: 'W01 source create', predicted: '201 DOCUMENT/DOCUMENT', ...c });
    const r = src ? await version(src.id, { documentType: 'PROPERTY_DEED' }) : { status: 'NO SOURCE' };
    rows.push({ kind: 'writer', principal: pname, id: 'W01 /:id/version metadata.documentType PROPERTY_DEED', predicted: '201, derived stored DOCUMENT served PROPERTY_DEED on head AND dev (writer not covered)', ...r });
  });
  it('W02 version without metadata (control)', async () => {
    await create(principal, J({ title: 'qa', documentType: 'DOCUMENT' }));
    const src = saved[saved.length - 1];
    const r = src ? await version(src.id, undefined) : { status: 'NO SOURCE' };
    rows.push({ kind: 'writer', principal: pname, id: 'W02 /:id/version no metadata', predicted: '201 DOCUMENT/DOCUMENT', ...r });
  });
  it('L01 legacy stored row already mismatched: readable, served as, versionable', async () => {
    const legacy = { id: 'doc-legacy-qa1024', type: 'DOCUMENT', status: 'anchored', owner: { id: String(principal.userId) }, data: { title: 'legacy', documentType: 'PROPERTY_DEED' }, contentHash: 'sha256:' + 'e'.repeat(64), signatures: [], createdAt: '2026-01-01T00:00:00.000Z', updatedAt: '2026-01-01T00:00:00.000Z' };
    store.set(legacy.id, JSON.parse(J(legacy)));
    rows.push({ kind: 'legacy', principal: pname, id: 'L01 GET + list of a legacy mismatched row', predicted: 'readable 200, served PROPERTY_DEED on head AND dev (create-only guard)', ...(await served({ 'x-probe-user': JSON.stringify(principal) }, legacy.id)) });
    rows.push({ kind: 'legacy', principal: pname, id: 'L01 version of the legacy row, no metadata', predicted: '201, derived inherits data.documentType PROPERTY_DEED', ...(await version(legacy.id, undefined)) });
  });
});
it('instrument controls: rows recorded for every cell', () => {
  expect(rows.filter((r) => r.kind === 'carrier').length).toBe(CARRIERS.length * PRINCIPALS.length);
  expect(rows.filter((r) => r.kind !== 'carrier').length).toBe(5 * PRINCIPALS.length);
});
