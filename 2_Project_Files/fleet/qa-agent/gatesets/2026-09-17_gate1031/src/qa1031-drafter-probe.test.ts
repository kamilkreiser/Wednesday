/**
 * qa1031-drafter-probe — DRAFTER measurement for the #1031 (KS-1213) tier-1 gate. Runs from src/qa_probe/ (outside the default
 * __tests__ testMatch and outside tsc's program) in the drafter clone only. No asserts: every row is recorded and the runner
 * compares head and develop. Harness = the seat's (real documentsRouter + certificationsRouter over an in-memory store), plus:
 * one loopback upstream counting /api/issuer-certs/sign, /api/users/stub and /api/anchors hits; recordActionProvenance and
 * resolveOnBehalfOf counted (extractOnBehalfOf real); raw JSON bodies for the duplicate / escaped / __proto__ keys.
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
const mockSaveCertification = jest.fn(async () => undefined);
jest.mock('../repositories/certificationRepo', () => ({
  initRepo: jest.fn(async () => undefined),
  getCertification: jest.fn(),
  saveCertification: (...a: unknown[]) => mockSaveCertification(...(a as [])),
  listCertifications: jest.fn(),
  saveShare: jest.fn(),
  getSharesByCertification: jest.fn(),
  getLineageEvents: jest.fn(),
}));
jest.mock('../db', () => ({ prisma: { $queryRaw: jest.fn(async () => []), $executeRaw: jest.fn(async () => 0), $executeRawUnsafe: jest.fn(async () => 0) } }));
jest.mock('../services/chargeEvents', () => ({ createChargeEvent: jest.fn(async () => ({ id: 'charge-1' })), getChargeEventsByCertification: jest.fn() }));
jest.mock('../utils/notificationClient', () => ({ notifyDocumentCertified: jest.fn(async () => undefined), notifyDocumentRevoked: jest.fn(async () => undefined), notifyDocumentShared: jest.fn(async () => undefined) }));
jest.mock('../repositories/shareRepo', () => ({ createShare: jest.fn() }));
jest.mock('../repositories/lifecycleEventRepo', () => ({ createLifecycleEvent: jest.fn(), setLifecycleEventAnchor: jest.fn(), listLifecycleEvents: jest.fn() }));
const mockPublish = jest.fn(async () => undefined);
jest.mock('../events', () => ({ publishEvent: (...a: unknown[]) => mockPublish(...(a as [])), EventTypes: { DOCUMENT_CREATED: 'document.created', DOCUMENT_OWNERSHIP_TRANSFERRED: 'document.ownership_transferred', DOCUMENT_VERSIONED: 'document.versioned', CERTIFICATION_ISSUED: 'certification.issued' } }));
jest.mock('../services/threadTokenClient', () => ({ mintAndRegisterThreadToken: jest.fn(async () => ({})) }));
jest.mock('../routes/verification', () => ({ registerInPlatformRegistry: jest.fn(async () => undefined) }));
jest.mock('../services/anchorStateSync', () => ({ pollAnchorUntilConfirmed: jest.fn(async () => undefined), reconcileDocumentAnchorState: jest.fn(async (d: any) => d) }));
const mockProvenance = jest.fn(async () => undefined);
jest.mock('../services/provenance', () => {
  const actual = jest.requireActual('../services/provenance');
  return { ...actual, recordActionProvenance: (...a: unknown[]) => mockProvenance(...(a as [])), resolveOnBehalfOf: jest.fn(async () => null), getCreationProvenance: jest.fn(async () => null), wasCreatedByConnector: jest.fn(async () => false) };
});
jest.mock('@secuura/shared', () =>
  require('../__tests__/helpers/sharedModuleMock').makeSharedMock({
    hasNulByte: jest.requireActual('@secuura/shared').hasNulByte,
    runWithTenantId: jest.requireActual('@secuura/shared').runWithTenantId,
    encryptField: jest.requireActual('@secuura/shared').encryptField,
    decryptField: jest.requireActual('@secuura/shared').decryptField,
    lookupHash: jest.requireActual('@secuura/shared').lookupHash,
    verifyMessageSignature: jest.fn(() => true),
  }),
);
jest.mock('../middleware/auth', () => ({
  authenticate: () => (req: any, _res: unknown, next: () => void) => {
    req.user = JSON.parse(String(req.headers['x-probe-user'] || '{}'));
    next();
  },
}));
jest.mock('../utils/logger', () => ({ logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() } }));

import express from 'express';
import * as fs from 'fs';
import { documentsRouter } from '../routes/documents';
import { certificationsRouter } from '../routes/certifications';

const TENANT = 'a0000000-0000-4000-8000-000000000001';
const ISSUER = { userId: '11111111-2222-4333-8444-555555551031', role: 'ISSUER_ADMIN', verificationLevel: 'none', tenantId: TENANT };
const SYSADMIN = { userId: '11111111-2222-4333-8444-555555551032', role: 'SYSTEM_ADMIN', tenantId: TENANT };
const CONN_DOCS = { userId: 'connector:qa1031-docs', role: 'connector', scopes: ['documents:write', 'documents:read'], organizationId: 'd0000000-0000-4000-8000-000000001031', tenantId: TENANT };
const CONN_CERTS = { userId: 'connector:qa1031-certs', role: 'connector', scopes: ['certifications:write'], organizationId: 'd0000000-0000-4000-8000-000000001031', tenantId: TENANT };
const PRINC: Record<string, any> = { ISSUER, CONN_DOCS, CONN_CERTS };
const HASH = 'sha256:' + 'b'.repeat(64);
const SRC = 'doc-src-qa1031';

const app = express();
app.use((req: any, _res, next) => { req.tenantId = TENANT; next(); });
app.use('/api/documents', express.json(), documentsRouter);
app.use('/api/certifications', express.json(), certificationsRouter);
const hits: Record<string, number> = {};
const up = express();
up.use(express.json());
up.use((req, _res, next) => { hits[req.path] = (hits[req.path] || 0) + 1; next(); });
up.post('/api/issuer-certs/sign', (req, res) => {
  res.json({ success: true, signature: 'ab', signatureAlgorithm: 'RSASSA-PSS-SHA256', signedContentHash: req.body.contentHash, signedAt: new Date().toISOString(),
    cert: { id: 'c1', fingerprintSha256: 'f'.repeat(64), subject: 'CN=qa', issuer: 'CN=qa', certPem: 'PEM', validFrom: '2026-01-01', validUntil: '2027-01-01', trustLevel: 'self-signed' } });
});
up.post('/api/users/stub', (_req, res) => { res.json({ data: { userId: '22222222-3333-4444-8555-666666661031', status: 'INVITED', email: 'h@qa1031.invalid' } }); });
up.post('/api/anchors', (_req, res) => { res.json({ data: { id: 'anchor-qa1031' } }); });

let base = '';
let server: ReturnType<typeof app.listen>;
let upstream: ReturnType<typeof up.listen>;
const rows: any[] = [];
beforeAll(async () => {
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  await new Promise<void>((r) => { upstream = up.listen(0, '127.0.0.1', () => r()); });
  const a = server.address(); base = 'http://127.0.0.1:' + String(typeof a === 'object' && a ? a.port : 0);
  const s = upstream.address(); const u = 'http://127.0.0.1:' + String(typeof s === 'object' && s ? s.port : 0);
  process.env.AUTH_SERVICE_URL = u; process.env.ANCHORING_SERVICE_URL = u;
});
afterAll(async () => {
  if (process.env.QA1031_ROWS_OUT) fs.writeFileSync(process.env.QA1031_ROWS_OUT, JSON.stringify(rows, null, 1));
  await new Promise<void>((r) => server.close(() => r()));
  await new Promise<void>((r) => upstream.close(() => r()));
});

function seed(type: unknown, data: Record<string, unknown> = {}) {
  store.set(SRC, { id: SRC, type, status: 'draft', owner: { id: ISSUER.userId }, data: { title: 'src', ...data }, contentHash: 'sha256:' + 'a'.repeat(64), signatures: [], createdAt: '2026-09-17T00:00:00Z', updatedAt: '2026-09-17T00:00:00Z' });
}
async function run(id: string, who: string, path: string, body: unknown, predicted: string, seedFn: () => void) {
  store.clear(); saved.length = 0; mockSaveCertification.mockClear(); mockProvenance.mockClear(); mockPublish.mockClear();
  for (const k of Object.keys(hits)) delete hits[k];
  seedFn();
  const raw = typeof body === 'string' ? body : JSON.stringify(body);
  const post = await fetch(base + path, { method: 'POST', headers: { 'content-type': 'application/json', 'x-probe-user': JSON.stringify(PRINC[who]) }, body: raw });
  const pj: any = await post.json().catch(() => null);
  const derived = saved.filter((r) => r.id !== SRC);
  const rec = derived.length ? derived[derived.length - 1] : null;
  let served: unknown = null; let listed: unknown = null;
  if (rec) {
    const g = await fetch(base + '/api/documents/' + encodeURIComponent(rec.id), { headers: { 'x-probe-user': JSON.stringify(SYSADMIN) } });
    served = ((await g.json().catch(() => null)) as any)?.documentType ?? null;
    const l = await fetch(base + '/api/documents', { headers: { 'x-probe-user': JSON.stringify(SYSADMIN) } });
    const lj: any = await l.json().catch(() => null);
    listed = (lj?.documents || []).find((d: any) => d.id === rec.id)?.documentType ?? null;
  }
  const row = { id, who, path: path.replace(SRC, ':id'), status: post.status, code: pj?.error?.code ?? null, derivedSaved: derived.length, storedType: rec?.type ?? null,
    storedDataType: rec ? (Object.prototype.hasOwnProperty.call(rec.data || {}, 'documentType') ? rec.data.documentType : '<absent>') : null,
    servedGET: served, servedList: listed, saveCertification: mockSaveCertification.mock.calls.length, signUpstream: hits['/api/issuer-certs/sign'] || 0,
    holderStub: hits['/api/users/stub'] || 0, anchorsUpstream: hits['/api/anchors'] || 0, provenance: mockProvenance.mock.calls.length, events: mockPublish.mock.calls.length,
    storedEqServed: rec ? JSON.stringify(rec.type) === JSON.stringify(served) : null, predicted };
  rows.push(row);
}

const DOC_WRITERS: Array<[string, string, (m?: unknown) => Record<string, unknown>]> = [
  ['V', `/api/documents/${SRC}/version`, (m) => ({ action: 'watermark', newContentHash: HASH, ...(m === undefined ? {} : { metadata: m }) })],
  ['C', `/api/documents/${SRC}/sign-cert`, (m) => ({ ...(m === undefined ? {} : { metadata: m }) })],
  ['W', `/api/documents/${SRC}/sign-wallet`, (m) => ({ walletAddress: 'addr_test1qa1031', signature: 'a1', key: 'a2', ...(m === undefined ? {} : { metadata: m }) })],
];
const R400 = 'head 400 BAD_REQUEST saved 0 upstream 0 | dev 201 relabel';
const SAME = 'head = dev 201 stored = served source type';
const CARRIERS: Array<[string, unknown, string]> = [
  ['M01 PROPERTY_DEED', 'PROPERTY_DEED', R400], ['M02 null', null, 'head 400 | dev 201 served DOCUMENT (null || type)'], ['M03 empty string', '', 'head 400 | dev 201 served DOCUMENT'],
  ['M04 number 7', 7, R400], ['M05 object', { v: 'PROPERTY_DEED' }, R400], ['M06 trailing space', 'DOCUMENT ', R400], ['M07 leading space', ' DOCUMENT', R400],
  ['M08 ZWSP', 'DOCUMENT​', R400], ['M09 Cyrillic TE', 'DOCUMENТ', R400], ['M10 fullwidth', 'ＤＯＣＵＭＥＮＴ', R400],
  ['M11 lower-case', 'document', R400], ['M12 array [DOCUMENT]', ['DOCUMENT'], R400], ['M13 equal DOCUMENT', 'DOCUMENT', SAME],
];
describe.each(DOC_WRITERS)('writer %s', (w, path, body) => {
  describe.each(['ISSUER', 'CONN_DOCS'])('as %s', (who) => {
    it.each(CARRIERS)('%s', async (label, carrier, pred) => { await run(w + '-' + label, who, path, body({ documentType: carrier }), pred, () => seed('DOCUMENT')); });
    it('M14 no metadata', async () => { await run(w + '-M14 no metadata', who, path, body(), SAME, () => seed('DOCUMENT')); });
    it('M15 metadata {}', async () => { await run(w + '-M15 metadata {}', who, path, body({}), SAME, () => seed('DOCUMENT')); });
    it('M16 nested data.documentType', async () => { await run(w + '-M16 nested', who, path, body({ data: { documentType: 'PROPERTY_DEED' }, extra: { documentType: 'PROPERTY_DEED' } }), SAME, () => seed('DOCUMENT')); });
    it('M17 key case DocumentType', async () => { await run(w + '-M17 DocumentType key', who, path, body({ DocumentType: 'PROPERTY_DEED', document_type: 'PROPERTY_DEED' }), SAME, () => seed('DOCUMENT')); });
    it('M18 __proto__ key raw JSON', async () => {
      const b = JSON.stringify(body({ title: 'p' })).replace('"metadata":{"title":"p"}', '"metadata":{"__proto__":{"documentType":"PROPERTY_DEED"}}');
      await run(w + '-M18 __proto__ raw', who, path, b.includes('__proto__') ? b : 'ANCHOR-MISS', SAME + ' (own __proto__ key, spread keeps it own)', () => seed('DOCUMENT'));
    });
    it('M19 duplicate key last-wins raw JSON', async () => {
      const b = JSON.stringify(body({ documentType: 'DOCUMENT' })).replace('"documentType":"DOCUMENT"', '"documentType":"DOCUMENT","documentType":"PROPERTY_DEED"');
      await run(w + '-M19 duplicate last PROPERTY_DEED', who, path, b, R400, () => seed('DOCUMENT'));
    });
    it('M20 escaped key raw JSON', async () => {
      const b = JSON.stringify(body({ documentType: 'PROPERTY_DEED' })).replace('"documentType"', '"documentTyp\\u0065"');
      await run(w + '-M20 escaped key', who, path, b, R400, () => seed('DOCUMENT'));
    });
    it('M21 top-level documentType + data, no metadata', async () => { await run(w + '-M21 top-level carriers', who, path, { ...body(), documentType: 'PROPERTY_DEED', type: 'PROPERTY_DEED', data: { documentType: 'PROPERTY_DEED' } }, SAME, () => seed('DOCUMENT')); });
    it('M22 metadata as string', async () => { await run(w + '-M22 metadata string', who, path, body('PROPERTY_DEED'), 'head = dev 400 VALIDATION_ERROR', () => seed('DOCUMENT')); });
    it('L01 legacy source + its SERVED label', async () => { await run(w + '-L01 legacy CERTIFICATE/DEGREE + DEGREE', who, path, body({ documentType: 'DEGREE' }), 'head 400 (behaviour change) | dev 201 served DEGREE', () => seed('CERTIFICATE', { documentType: 'DEGREE' })); });
    it('L02 legacy source + its STORED type', async () => { await run(w + '-L02 legacy CERTIFICATE/DEGREE + CERTIFICATE', who, path, body({ documentType: 'CERTIFICATE' }), 'head = dev 201 served CERTIFICATE (stored = served again)', () => seed('CERTIFICATE', { documentType: 'DEGREE' })); });
    it('L03 legacy source, no metadata', async () => { await run(w + '-L03 legacy no metadata', who, path, body(), 'head = dev 201 stored CERTIFICATE served DEGREE (ruled: not refused)', () => seed('CERTIFICATE', { documentType: 'DEGREE' })); });
    it('S01 lower-case source type equal', async () => { await run(w + '-S01 source degree + degree', who, path, body({ documentType: 'degree' }), SAME, () => seed('degree')); });
    it('S02 source with a padded stored type, equal', async () => { await run(w + '-S02 source "DOCUMENT " + "DOCUMENT "', who, path, body({ documentType: 'DOCUMENT ' }), SAME, () => seed('DOCUMENT ')); });
  });
  it('P01 connector with only certifications:write', async () => { await run(w + '-P01 certs-only connector', 'CONN_CERTS', path, body({ documentType: 'PROPERTY_DEED' }), 'head = dev 403', () => seed('DOCUMENT')); });
});
it('V-OBO mismatch with onBehalfOf (connector)', async () => {
  await run('V-OBO mismatch + onBehalfOf', 'CONN_DOCS', `/api/documents/${SRC}/version`, { action: 'watermark', newContentHash: HASH, onBehalfOf: { email: 'obo@qa1031.invalid' }, metadata: { documentType: 'PROPERTY_DEED' } },
    'head 400 BUT provenance 1 (handleOnBehalfOf precedes the guard) | dev 201', () => seed('DOCUMENT'));
});
it('C-OBO sign-cert mismatch with onBehalfOf (connector)', async () => {
  await run('C-OBO mismatch + onBehalfOf', 'CONN_DOCS', `/api/documents/${SRC}/sign-cert`, { onBehalfOf: { email: 'obo@qa1031.invalid' }, metadata: { documentType: 'PROPERTY_DEED' } }, 'head 400 provenance 0', () => seed('DOCUMENT'));
});

const ISSUE = '/api/certifications/issue';
const I400 = 'head 400 saveCertification 0 holderStub 0 anchors 0 | dev 201 derived relabel';
const ICARRIERS: Array<[string, unknown, string]> = [
  ['I01 PROPERTY_DEED', 'PROPERTY_DEED', I400], ['I02 null', null, 'head 400 | dev 201 served certificate'], ['I03 number 7', 7, I400], ['I04 array [certificate]', ['certificate'], I400],
  ['I05 object', { v: 1 }, I400], ['I06 padded', 'certificate ', I400], ['I07 upper-case', 'CERTIFICATE', I400], ['I08 ZWSP', 'certificate​', I400], ['I09 empty string', '', 'head 400 | dev 201 served certificate'],
  ['I10 equal', 'certificate', 'head = dev 201 stored = served certificate'],
];
describe.each(['ISSUER', 'CONN_CERTS'])('issue as %s', (who) => {
  it.each(ICARRIERS)('%s', async (label, carrier, pred) => { await run('I-' + label, who, ISSUE, { type: 'certificate', data: { title: 'c', documentType: carrier }, parentDocumentId: SRC }, pred, () => seed('DOCUMENT')); });
  it('I11 absent', async () => { await run('I-I11 absent', who, ISSUE, { type: 'certificate', data: { title: 'c' }, parentDocumentId: SRC }, 'head = dev 201 served certificate', () => seed('DOCUMENT')); });
  it('I12 no parent + mismatch', async () => { await run('I-I12 no parent', who, ISSUE, { type: 'certificate', data: { title: 'c', documentType: 'PROPERTY_DEED' } }, 'head = dev 201 derived 0 saveCertification 1', () => seed('DOCUMENT')); });
  it('I13 parentDocumentId empty string + mismatch', async () => { await run('I-I13 parent ""', who, ISSUE, { type: 'certificate', data: { title: 'c', documentType: 'PROPERTY_DEED' }, parentDocumentId: '' }, 'head = dev 201 derived 0 (falsy parent: neither guard nor derive)', () => seed('DOCUMENT')); });
  it('I14 holderEmail + parent + mismatch', async () => { await run('I-I14 holderEmail', who, ISSUE, { type: 'certificate', holderEmail: 'h@qa1031.invalid', data: { title: 'c', documentType: 'PROPERTY_DEED' }, parentDocumentId: SRC }, 'head 400 holderStub 0 | dev 201 holderStub 1', () => seed('DOCUMENT')); });
  it('I15 duplicate key last-wins raw JSON', async () => {
    const b = JSON.stringify({ type: 'certificate', data: { title: 'c', documentType: 'certificate' }, parentDocumentId: SRC }).replace('"documentType":"certificate"', '"documentType":"certificate","documentType":"PROPERTY_DEED"');
    await run('I-I15 duplicate last PROPERTY_DEED', who, ISSUE, b, I400, () => seed('DOCUMENT'));
  });
  it('I16 parent missing + mismatch', async () => { await run('I-I16 parent missing', who, ISSUE, { type: 'certificate', data: { title: 'c', documentType: 'PROPERTY_DEED' }, parentDocumentId: 'doc-qa1031-missing' }, 'head 400 | dev 201 derived relabel', () => seed('DOCUMENT')); });
  it('I17 nested data.metadata.documentType', async () => { await run('I-I17 nested', who, ISSUE, { type: 'certificate', data: { title: 'c', metadata: { documentType: 'PROPERTY_DEED' } }, parentDocumentId: SRC }, 'head = dev 201 served certificate', () => seed('DOCUMENT')); });
  it('I18 parent type differs from cert type, no data.documentType', async () => { await run('I-I18 parent PROPERTY_DEED, cert certificate', who, ISSUE, { type: 'certificate', data: { title: 'c' }, parentDocumentId: SRC }, 'head = dev 201 served certificate (parent type not inherited)', () => seed('PROPERTY_DEED', { documentType: 'PROPERTY_DEED' })); });
});
it('I-P01 connector with only documents:write', async () => { await run('I-P01 docs-only connector', 'CONN_DOCS', ISSUE, { type: 'certificate', data: { title: 'c', documentType: 'PROPERTY_DEED' }, parentDocumentId: SRC }, 'head = dev 403', () => seed('DOCUMENT')); });
