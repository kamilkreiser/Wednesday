/**
 * KS-1213 — a derived-document writer refuses a caller type that differs from the type it stores.
 *
 * A document is served as `data.documentType || type`. `/:id/version`, `/:id/sign-cert` and
 * `/:id/sign-wallet` store the new row as `source.type` but spread the caller's `metadata` into `data`;
 * `POST /api/certifications/issue` with `parentDocumentId` stores the derived row as the certification
 * type and spreads the caller's `data`. So a caller could have the new row served, and verified, as a
 * type it was never stored as. Measured on develop 19f1e5475 for all four (201, stored DOCUMENT, served
 * PROPERTY_DEED). Each now refuses 400 BAD_REQUEST before any write, with the KS-1202 create guard's
 * comparison: exact, no case-folding, and a non-string never matches.
 *
 * Also here, the KS-1202 create guard's properties its gate left unpinned (#1024 N-B): a case variant, an
 * array carrier, the legacy `{type X, data.documentType X}` shape, and the untyped `data.documentType
 * DOCUMENT` shape.
 *
 * Harness: the real documentsRouter and certificationsRouter over one in-memory document store that keeps
 * exactly the rows the handlers saved (the KS-1202 suite's pattern). `sign-cert`'s issuer-certs upstream
 * is a loopback stub that answers a sign envelope; `sign-wallet`'s CIP-8 verification is stubbed true.
 * The served type is read back through GET /api/documents/:id as a SYSTEM_ADMIN, which can read every row written here.
 */
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@127.0.0.1:1/test';
process.env.SIMULATE_ANCHORING = 'true';

// KS-1266: keep this unit file off the network. Left at its default, ANCHORING_SERVICE_URL
// resolves the host `anchoring` by DNS and opens a TCP connection to :4005, so the result
// depends on the host's resolver. Port 2, NOT port 1: port 1 is on the Fetch-spec bad-port
// list and undici refuses it before any socket opens, so it never produces the
// ECONNREFUSED the cell is written for. 127.0.0.1:2 does.
const ANCHORING_REFUSED = 'http://127.0.0.1:2';
process.env.ANCHORING_SERVICE_URL = ANCHORING_REFUSED;

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
jest.mock('../db', () => ({ prisma: { $queryRaw: jest.fn(), $executeRaw: jest.fn(), $executeRawUnsafe: jest.fn() } }));
jest.mock('../services/chargeEvents', () => ({ createChargeEvent: jest.fn(async () => ({ id: 'charge-1' })), getChargeEventsByCertification: jest.fn() }));
jest.mock('../utils/notificationClient', () => ({ notifyDocumentCertified: jest.fn(async () => undefined), notifyDocumentRevoked: jest.fn(async () => undefined), notifyDocumentShared: jest.fn(async () => undefined) }));
jest.mock('../repositories/shareRepo', () => ({ createShare: jest.fn() }));
jest.mock('../repositories/lifecycleEventRepo', () => ({ createLifecycleEvent: jest.fn(), setLifecycleEventAnchor: jest.fn(), listLifecycleEvents: jest.fn() }));
jest.mock('../events', () => ({ publishEvent: jest.fn(async () => undefined), EventTypes: { DOCUMENT_CREATED: 'document.created', DOCUMENT_OWNERSHIP_TRANSFERRED: 'document.ownership_transferred', DOCUMENT_VERSIONED: 'document.versioned', CERTIFICATION_ISSUED: 'certification.issued' } }));
jest.mock('../services/threadTokenClient', () => ({ mintAndRegisterThreadToken: jest.fn(async () => ({})) }));
jest.mock('../routes/verification', () => ({ registerInPlatformRegistry: jest.fn(async () => undefined) }));
jest.mock('../services/anchorStateSync', () => ({ pollAnchorUntilConfirmed: jest.fn(async () => undefined), reconcileDocumentAnchorState: jest.fn(async (d: any) => d) }));
jest.mock('../services/provenance', () => {
  const actual = jest.requireActual('../services/provenance');
  return { ...actual, recordActionProvenance: jest.fn(async () => undefined), getCreationProvenance: jest.fn(async () => null), wasCreatedByConnector: jest.fn(async () => false) };
});
// KS-1061: through makeSharedMock. The routes' own shared imports stay real; only the CIP-8 check is stubbed.
jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
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
import { documentsRouter } from '../routes/documents';
import { certificationsRouter } from '../routes/certifications';

const TENANT = 'a0000000-0000-4000-8000-000000000001';
const ISSUER = { userId: '11111111-2222-4333-8444-555555551213', role: 'ISSUER_ADMIN', verificationLevel: 'none', tenantId: TENANT };
const SYSADMIN = { userId: '11111111-2222-4333-8444-555555551214', role: 'SYSTEM_ADMIN', tenantId: TENANT };
const CONNECTOR = { userId: 'connector:ks1213-conn', role: 'connector', scopes: ['documents:write', 'documents:read', 'certifications:write'], organizationId: 'd0000000-0000-4000-8000-000000001213', tenantId: TENANT };
const HASH = 'sha256:' + 'b'.repeat(64);

const app = express();
app.use((req: any, _res, next) => { req.tenantId = TENANT; next(); });
app.use('/api/documents', express.json(), documentsRouter);
app.use('/api/certifications', express.json(), certificationsRouter);
const certStub = express();
certStub.use(express.json());
certStub.post('/api/issuer-certs/sign', (req, res) => {
  res.json({ success: true, signature: 'ab', signatureAlgorithm: 'RSASSA-PSS-SHA256', signedContentHash: req.body.contentHash, signedAt: new Date().toISOString(),
    cert: { id: 'c1', fingerprintSha256: 'f'.repeat(64), subject: 'CN=probe', issuer: 'CN=probe', certPem: 'PEM', validFrom: '2026-01-01', validUntil: '2027-01-01', trustLevel: 'self-signed' } });
});
let base = '';
let server: ReturnType<typeof app.listen>;
let stub: ReturnType<typeof certStub.listen>;
beforeAll(async () => {
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  await new Promise<void>((r) => { stub = certStub.listen(0, '127.0.0.1', () => r()); });
  const a = server.address(); base = 'http://127.0.0.1:' + String(typeof a === 'object' && a ? a.port : 0);
  const s = stub.address(); process.env.AUTH_SERVICE_URL = 'http://127.0.0.1:' + String(typeof s === 'object' && s ? s.port : 0);
});
describe('KS-1229 X-SIGNCERT-AFTER-UPSTREAM - a refused sign-cert reaches no upstream', () => {
  const signCert = (metadata: Record<string, unknown>) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-cert', { metadata });
  it('RED KS-1229 SC1 - a refused sign-cert sends nothing to the issuer-certs upstream', async () => {
    // KS-1229 (X-SIGNCERT-AFTER-UPSTREAM): the sign request is a real upstream call, so the refusal must come first.
    seed('DOCUMENT');
    const upstreamUrls: string[] = [];
    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
    stub.on('request', onUpstream);
    try {
      const r = await signCert({ documentType: 'PROPERTY_DEED' });
      expect([r.status, r.code, upstreamUrls]).toEqual([400, 'BAD_REQUEST', []]);
    } finally {
      stub.off('request', onUpstream);
    }
  }); // KS-1229 SC1
  it('control - KS-1229 an accepted sign-cert does reach the issuer-certs upstream', async () => {
    seed('DOCUMENT');
    const upstreamUrls: string[] = [];
    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
    stub.on('request', onUpstream);
    try {
      const r = await signCert({ documentType: 'DOCUMENT' });
      expect([r.status, upstreamUrls]).toEqual([201, ['/api/issuer-certs/sign']]);
    } finally {
      stub.off('request', onUpstream);
    }
  }); // KS-1229 SC control
});
afterAll(() => {
  server?.close(); stub?.close();
});
describe('KS-1229 Q-SIGNWALLET-AFTER-VERIFY - the label refusal comes BEFORE the wallet signature check', () => {
  it('RED KS-1229 AV1 - a mislabelled request with a bad signature is refused BAD_REQUEST, not INVALID_WALLET_SIGNATURE', async () => {
    // KS-1229 (Q-SIGNWALLET-AFTER-VERIFY): the cheap, caller-fixable refusal must precede the CIP-8 check.
    const shared = jest.requireMock('@secuura/shared') as { verifyMessageSignature: jest.Mock };
    seed('DOCUMENT');
    shared.verifyMessageSignature.mockImplementation(() => false);
    try {
      const r = await write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-wallet', { walletAddress: 'addr_test1ks1229', signature: 'a1', key: 'a2', metadata: { documentType: 'PROPERTY_DEED' } });
      expect([r.status, r.code, r.saved]).toEqual([400, 'BAD_REQUEST', 0]);
    } finally {
      shared.verifyMessageSignature.mockImplementation(() => true);
    }
  }); // KS-1229 AV1
  it('control - KS-1229 the same mislabelled request with a good signature is refused BAD_REQUEST', async () => {
    seed('DOCUMENT');
    const r = await write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-wallet', { walletAddress: 'addr_test1ks1229', signature: 'a1', key: 'a2', metadata: { documentType: 'PROPERTY_DEED' } });
    expect([r.status, r.code, r.saved]).toEqual([400, 'BAD_REQUEST', 0]);
  }); // KS-1229 AV control
});
beforeEach(() => { store.clear(); saved.length = 0; mockSaveCertification.mockClear(); });


const SOURCE_ID = 'doc-src-1213';
describe('KS-1229 X-VERSION-TRIM - the /version guard compares EXACTLY, so a padded carrier is refused', () => {
  const version = (documentType: string) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/version', { action: 'watermark', newContentHash: HASH, metadata: { documentType } });
  it('RED KS-1229 VT1 - a trailing-space carrier is refused, never trimmed into a match', async () => {
    // KS-1229 (X-VERSION-TRIM): trimming would store DOCUMENT and serve the padded label - a relabel by invisible whitespace.
    seed('DOCUMENT');
    expect(await version('DOCUMENT ')).toEqual(REFUSED);
  }); // KS-1229 VT1
  it('control - KS-1229 the exact carrier is accepted and served as that type', async () => {
    seed('DOCUMENT');
    expect(await version('DOCUMENT')).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
  }); // KS-1229 VT control
});
describe('KS-1229 Q-VERSION-TRUTHY - the /version guard keys on PRESENCE, not truthiness', () => {
  // KS-1229 (Q-VERSION-TRUTHY): the guard reads `metadata.documentType !== undefined`. Written as
  // `metadata.documentType && ...` instead, null / '' / false slip past it. Nothing is RELABELLED by that
  // - the served type is `data.documentType || type`, so the stored type still wins - which is exactly why
  // the whole suite stayed green under the gate's tamper. What is lost is the rule the route states: a
  // documentType that is PRESENT and not equal to the stored type is refused, whatever its truthiness.
  // Measured at this base: null, '' and false each give 400 BAD_REQUEST with nothing saved, and it is the
  // guard that refuses them - an absent key is the only shape waved through.
  const present = (documentType: unknown) =>
    write(ISSUER, '/api/documents/' + SOURCE_ID + '/version', { action: 'watermark', newContentHash: HASH, metadata: { documentType } });
  it('RED KS-1229 QVT1 - a PRESENT null documentType is refused, not read as absent', async () => {
    seed('DOCUMENT');
    expect(await present(null)).toEqual(REFUSED);
  }); // KS-1229 QVT1
  it('RED KS-1229 QVT2 - a PRESENT empty-string documentType is refused', async () => {
    seed('DOCUMENT');
    expect(await present('')).toEqual(REFUSED);
  }); // KS-1229 QVT2
  it('RED KS-1229 QVT3 - a PRESENT false documentType is refused', async () => {
    seed('DOCUMENT');
    expect(await present(false)).toEqual(REFUSED);
  }); // KS-1229 QVT3
  it('control - KS-1229 an ABSENT documentType is accepted: undefined is the only waved-through shape', async () => {
    seed('DOCUMENT');
    expect(await write(ISSUER, '/api/documents/' + SOURCE_ID + '/version', { action: 'watermark', newContentHash: HASH, metadata: {} }))
      .toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
  }); // KS-1229 QVT control
});
function seed(type: string, data: Record<string, unknown> = {}) {
  store.set(SOURCE_ID, { id: SOURCE_ID, type, status: 'draft', owner: { id: ISSUER.userId }, data: { title: 'src', ...data }, contentHash: 'sha256:' + 'a'.repeat(64), signatures: [], createdAt: '2026-09-17T00:00:00Z', updatedAt: '2026-09-17T00:00:00Z' });
}

async function write(principal: Record<string, unknown>, path: string, body: unknown) {
  const post = await fetch(base + path, { method: 'POST', headers: { 'content-type': 'application/json', 'x-probe-user': JSON.stringify(principal) }, body: JSON.stringify(body) });
  const pj: any = await post.json().catch(() => null);
  const derived = saved.filter((r) => r.id !== SOURCE_ID);
  const rec = derived.length > 0 ? derived[derived.length - 1] : null;
  let served: unknown = null;
  if (rec) {
    const g = await fetch(base + '/api/documents/' + encodeURIComponent(rec.id), { headers: { 'x-probe-user': JSON.stringify(SYSADMIN) } });
    served = ((await g.json().catch(() => null)) as any)?.documentType ?? null;
  }
  return { status: post.status, code: pj?.error?.code ?? null, saved: derived.length, stored: rec?.type ?? null, served };
}

const REFUSED = { status: 400, code: 'BAD_REQUEST', saved: 0, stored: null, served: null };
describe('KS-1229 X-SIGNWALLET-SERVED - sign-wallet compares with the STORED type, not the served label', () => {
  const signWallet = (metadata: Record<string, unknown>) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-wallet', { walletAddress: 'addr_test1ks1229', signature: 'a1', key: 'a2', metadata });
  it('RED KS-1229 SW1 - a legacy source served as DEGREE still refuses metadata.documentType DEGREE', async () => {
    // KS-1229 (X-SIGNWALLET-SERVED): the new row would be STORED CERTIFICATE and SERVED DEGREE - the relabel KS-1213 closed.
    seed('CERTIFICATE', { documentType: 'DEGREE' });
    expect(await signWallet({ documentType: 'DEGREE' })).toEqual(REFUSED);
  }); // KS-1229 SW1
  it('control - KS-1229 an ordinary source accepts a metadata.documentType equal to its stored type', async () => {
    seed('DOCUMENT');
    expect(await signWallet({ documentType: 'DOCUMENT' })).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
  }); // KS-1229 SW control
});
const PRINCIPALS: Array<[string, Record<string, unknown>]> = [['ISSUER_ADMIN', ISSUER], ['SYSTEM_ADMIN', SYSADMIN], ['connector with documents:write', CONNECTOR]];
const WRITERS: Array<[string, string, (metadata?: Record<string, unknown>) => Record<string, unknown>]> = [
  ['/version', `/api/documents/${SOURCE_ID}/version`, (metadata) => ({ action: 'watermark', newContentHash: HASH, ...(metadata ? { metadata } : {}) })],
  ['/sign-cert', `/api/documents/${SOURCE_ID}/sign-cert`, (metadata) => ({ ...(metadata ? { metadata } : {}) })],
  ['/sign-wallet', `/api/documents/${SOURCE_ID}/sign-wallet`, (metadata) => ({ walletAddress: 'addr_test1ks1213', signature: 'a1', key: 'a2', ...(metadata ? { metadata } : {}) })],
];

describe.each(WRITERS)('KS-1213 %s', (_writer, path, body) => {
  describe.each(PRINCIPALS)('as %s', (_who, principal) => {
    it.each([
      ['PROPERTY_DEED on a DOCUMENT source', 'DOCUMENT', 'PROPERTY_DEED'],
      ['DEGREE on a CERTIFICATE source', 'CERTIFICATE', 'DEGREE'],
      ['a case variant (document on DOCUMENT)', 'DOCUMENT', 'document'],
      ['an array carrier ([DOCUMENT] on DOCUMENT)', 'DOCUMENT', ['DOCUMENT']],
    ])('RED metadata.documentType %s: refused 400, nothing saved', async (_label, sourceType, documentType) => {
      seed(sourceType as string);
      expect(await write(principal, path, body({ documentType }))).toEqual(REFUSED);
    });

    it('control - metadata.documentType equal to the source type is written and served as that type', async () => {
      seed('DOCUMENT');
      expect(await write(principal, path, body({ documentType: 'DOCUMENT' }))).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
    });

    it('control - no metadata is written and served as the source type', async () => {
      seed('CERTIFICATE');
      expect(await write(principal, path, body())).toEqual({ status: 201, code: null, saved: 1, stored: 'CERTIFICATE', served: 'CERTIFICATE' });
    });

    it('control - a legacy source already served as another type keeps its own label when the caller names none', async () => {
      seed('CERTIFICATE', { documentType: 'DEGREE' });
      expect(await write(principal, path, body())).toEqual({ status: 201, code: null, saved: 1, stored: 'CERTIFICATE', served: 'DEGREE' });
    });
  });
});

// KS-1301: #1237 pinned the presence-not-truthiness rule on /version ONLY (its QVT cells). The SAME
// guard is written identically at three call sites in routes/documents.ts — /version, /sign-cert and
// /sign-wallet — and only /version was ever held to it. A truthiness bug here is invisible to ordinary
// testing, because null, '' and false all LOOK absent to an `if (!documentType)` check while being
// present in the request. Ported below for the two unpinned routes, ONE DESCRIBE PER ROUTE so a
// truthiness tamper of one guard reds only that route's cells and the other route stays green.
const PRESENCE_WRITERS = WRITERS.filter(([writer]) => writer !== '/version');
describe.each(PRESENCE_WRITERS)('KS-1301 %s keys on PRESENCE, not truthiness', (_writer, path, body) => {
  it.each([
    ['null', null],
    ['an empty string', ''],
    ['false', false],
  ])('RED KS-1301 a PRESENT %s documentType is refused, not read as absent', async (_label, documentType) => {
    seed('DOCUMENT');
    expect(await write(ISSUER, path, body({ documentType }))).toEqual(REFUSED);
  });

  it('control - KS-1301 an ABSENT documentType is accepted: undefined is the only waved-through shape', async () => {
    seed('DOCUMENT');
    expect(await write(ISSUER, path, body({}))).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
  });
});

describe.each(PRINCIPALS)('KS-1213 POST /api/certifications/issue with parentDocumentId as %s', (_who, principal) => {
  const issue = (b: Record<string, unknown>) => write(principal, '/api/certifications/issue', b);

  it.each([
    ['a non-string number carrier (type DOCUMENT, data.documentType 7)', { type: 'DOCUMENT', data: { title: 'c', documentType: 7 } }], // KS-1229 X-ISSUE-LOOSE
    ['an object carrier (type DOCUMENT, data.documentType an object)', { type: 'DOCUMENT', data: { title: 'c', documentType: { name: 'DOCUMENT' } } }], // KS-1229 X-ISSUE-LOOSE
    ['type DOCUMENT, data.documentType PROPERTY_DEED', { type: 'DOCUMENT', data: { title: 'c', documentType: 'PROPERTY_DEED' } }],
    ["type certificate, data.documentType DOCUMENT (the parent's type)", { type: 'certificate', data: { title: 'c', documentType: 'DOCUMENT' } }],
    ['a case variant (type DOCUMENT, data.documentType document)', { type: 'DOCUMENT', data: { title: 'c', documentType: 'document' } }],
  ])('RED %s: refused 400, no certification and no derived document written', async (_label, b) => {
    seed('DOCUMENT');
    expect(await issue({ ...b, parentDocumentId: SOURCE_ID })).toEqual(REFUSED);
    expect(mockSaveCertification).not.toHaveBeenCalled();
  });

  it('control - data.documentType equal to the certification type is written and served as that type', async () => {
    seed('DOCUMENT');
    expect(await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'DOCUMENT' }, parentDocumentId: SOURCE_ID })).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
  });

  it('control - no data.documentType is written and served as the certification type', async () => {
    seed('DOCUMENT');
    expect(await issue({ type: 'certificate', data: { title: 'c' }, parentDocumentId: SOURCE_ID })).toEqual({ status: 201, code: null, saved: 1, stored: 'certificate', served: 'certificate' });
  });

  it('control - without parentDocumentId no derived document is written, and the request is not refused', async () => {
    seed('DOCUMENT');
    const r = await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'PROPERTY_DEED' } });
    expect([r.status, r.saved]).toEqual([201, 0]);
    expect(mockSaveCertification).toHaveBeenCalledTimes(1);
  });
  it('RED KS-1229 R1 - a refused issue with holderEmail sends nothing to the users/stub upstream', async () => {
    // KS-1229 (X-ISSUE-AFTER-HOLDER): users/stub mints or resolves an INVITED user in auth, so the refusal must come first.
    seed('DOCUMENT');
    const upstreamUrls: string[] = [];
    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
    stub.on('request', onUpstream);
    try {
      const r = await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'PROPERTY_DEED' }, holderEmail: 'holder-ks1229@example.test', parentDocumentId: SOURCE_ID });
      expect([r.status, r.code, upstreamUrls]).toEqual([400, 'BAD_REQUEST', []]);
    } finally {
      stub.off('request', onUpstream);
    }
  }); // KS-1229 R1
  it('RED KS-1229 R2 - a refused issue submits no anchoring job', async () => {
    // KS-1229 (X-ISSUE-AFTER-ANCHOR): the anchoring base points at the loopback stub for this cell only.
    seed('DOCUMENT');
    const upstreamUrls: string[] = [];
    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
    stub.on('request', onUpstream);
    process.env.ANCHORING_SERVICE_URL = process.env.AUTH_SERVICE_URL;
    try {
      const r = await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'PROPERTY_DEED' }, parentDocumentId: SOURCE_ID });
      expect([r.status, r.code, upstreamUrls]).toEqual([400, 'BAD_REQUEST', []]);
    } finally {
      stub.off('request', onUpstream);
      process.env.ANCHORING_SERVICE_URL = ANCHORING_REFUSED;
    }
  }); // KS-1229 R2
  it('control - KS-1229 an accepted issue reaches /api/anchors and a holderEmail issue reaches /api/users/stub on the loopback stub', async () => {
    seed('DOCUMENT');
    const upstreamUrls: string[] = [];
    const onUpstream = (req: { url?: string }): void => { upstreamUrls.push(String(req.url)); };
    stub.on('request', onUpstream);
    process.env.ANCHORING_SERVICE_URL = process.env.AUTH_SERVICE_URL;
    try {
      const accepted = await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'DOCUMENT' }, parentDocumentId: SOURCE_ID });
      const invited = await issue({ type: 'DOCUMENT', data: { title: 'c', documentType: 'DOCUMENT' }, holderEmail: 'holder-ks1229@example.test', parentDocumentId: SOURCE_ID });
      expect([accepted.status, invited.status, upstreamUrls]).toEqual([201, 404, ['/api/anchors', '/api/users/stub']]);
    } finally {
      stub.off('request', onUpstream);
      process.env.ANCHORING_SERVICE_URL = ANCHORING_REFUSED;
    }
  }); // KS-1229 control
});

describe('KS-1202 create guard - the properties its gate left unpinned (#1024 N-B)', () => {
  const create = async (b: Record<string, unknown>) => {
    const r = await write(ISSUER, '/api/documents', b);
    return r;
  };
  it('RED a case variant: documentType DOCUMENT with data.documentType document is refused 400', async () => {
    expect(await create({ title: 'nb', documentType: 'DOCUMENT', data: { title: 'nb', documentType: 'document' } })).toEqual(REFUSED);
  });
  it('RED an array carrier: documentType DOCUMENT with data.documentType [DOCUMENT] is refused 400', async () => {
    expect(await create({ title: 'nb', documentType: 'DOCUMENT', data: { title: 'nb', documentType: ['DOCUMENT'] } })).toEqual(REFUSED);
  });
  it('control - the legacy shape {type X, data.documentType X} is created and served as X', async () => {
    expect(await create({ title: 'nb', type: 'CERTIFICATE', data: { title: 'nb', documentType: 'CERTIFICATE' } })).toEqual({ status: 201, code: null, saved: 1, stored: 'CERTIFICATE', served: 'CERTIFICATE' });
  });
  it('control - an untyped body with data.documentType DOCUMENT is created and served as DOCUMENT', async () => {
    expect(await create({ data: { title: 'nb', documentType: 'DOCUMENT' } })).toEqual({ status: 201, code: null, saved: 1, stored: 'DOCUMENT', served: 'DOCUMENT' });
  });
}); // KS-1202 create guard
describe('KS-1229 Q-SIGNCERT-UNTYPED-SOURCE-SKIP - the sign-cert guard still refuses when the source has no type', () => {
  const signCert = (metadata: Record<string, unknown>) => write(ISSUER, '/api/documents/' + SOURCE_ID + '/sign-cert', { metadata });
  it('RED KS-1229 U1 - an untyped source is refused a relabel, nothing saved', async () => {
    // KS-1229 (Q-SIGNCERT-UNTYPED-SOURCE-SKIP): an untyped in-memory source must not skip the guard.
    seed(undefined as unknown as string);
    expect(await signCert({ documentType: 'DEGREE' })).toEqual(REFUSED);
  }); // KS-1229 U1
  it('control - KS-1229 a typed source is still refused a differing relabel', async () => {
    seed('DOCUMENT');
    expect(await signCert({ documentType: 'PROPERTY_DEED' })).toEqual(REFUSED);
  }); // KS-1229 U control
}); // KS-1229 Q-SIGNCERT-UNTYPED-SOURCE-SKIP
