/**
 * =============================================================================
 * KS-1822 — an anchor of another tenant's document reads exactly as an absent one
 * =============================================================================
 * THE DEFECT. `GET /api/anchors/:id` and `GET /api/anchors/document/:documentId` had no
 * tenant check: behind `jwtAuthenticate()` only, with unscoped row reads, so a caller in
 * tenant A read tenant B's anchor — content hash, transaction, identity block and the
 * KS-1454 signature hash — by id or by document id.
 *
 * THE RULE PINNED HERE (anchorReadGate.ts): the KS-1603 write gate's decision table,
 * applied to the reads. Refuse only a row whose document is held by a `documents` row in
 * another tenant, and answer that refusal with the 404 the SAME request gets when no row
 * exists — status, content type, length, ETag and body byte for byte — so the refusal is
 * not an existence oracle. Allow, by name: own tenant; no document holds the id (flat
 * anchors, residual i); no usable tenant claim (residual ii); probe fault (residual iii).
 *
 * WHY THIS FILE BOOTS THE REAL APP. The defect is in what the two HANDLERS answer, after
 * the whole middleware chain. A cell that called the gate function directly would pass
 * with the gate unwired. So every cell drives the real `index.ts` app (the KS-1603 /
 * KS-1717 recipe: `express.application.listen` is spied before the import, the app is
 * served on an ephemeral port) with a real RS256 bearer.
 *
 * THE DB BOUNDARY IS MOCKED, not the gate. `../db` keeps its real exports, with
 * `isDbAvailable` true, `query` answering the two `anchor_store` SELECTs from `h.anchors`,
 * and `transaction` handing the REAL `readIdOwners` a client that answers its `documents`
 * SELECT from `h.documents` (or throws, for the probe-fault cell). So the id resolution
 * the gate relies on (external_id first, then the primary key) is the real code.
 *
 * RED ON DEVELOP (no gate): R1, R2, R3 (foreign rows answered 200), R7 and R8 (no warn
 * line), R9 (no refusal line in the log), R11 (foreign answered 200).
 * CONTROLS, green on develop and after: R4, R5, R6, R10, R12 — they pin what the gate must
 * NOT change (own-tenant bodies, the residuals, the case-insensitive tenant compare, the
 * empty-read short-circuit).
 * =============================================================================
 */
import { describe, it, expect, beforeAll, afterAll, beforeEach, vi } from 'vitest';
import crypto from 'crypto';
import http from 'http';
import type { AddressInfo } from 'net';
import express from 'express';

const h = vi.hoisted(() => ({
  anchors: [] as Array<Record<string, unknown>>,
  documents: [] as Array<{ id: string; external_id: string | null; tenant_id: string }>,
  probeFault: false,
  probes: 0,
}));

vi.mock('../db', async (importOriginal) => {
  const real = await importOriginal<typeof import('../db')>();
  const probeClient = {
    async query(sql: string, params: unknown[] = []) {
      if (sql.includes('set_config')) return { rows: [] };
      if (sql.includes('FROM documents d')) {
        const [externalIds, primaryKeys] = params as [string[], string[]];
        const keys = primaryKeys.map((k) => k.toLowerCase());
        const rows = h.documents
          .filter((d) => (d.external_id !== null && externalIds.includes(d.external_id)) || keys.includes(d.id.toLowerCase()))
          .map((d) => ({ external_id: d.external_id, primary_key: d.id, tenant_id: d.tenant_id }));
        return { rows };
      }
      throw new Error(`KS-1822 test: unexpected probe SQL: ${sql}`);
    },
  };
  return {
    ...real,
    isDbAvailable: () => true,
    query: async (sql: string, params: unknown[] = []) => {
      if (sql.includes('to_regclass')) return { rows: [{ s: 'anchor_store', b: 'anchor_batches' }], rowCount: 1 };
      if (/FROM anchor_store WHERE id = \$1/.test(sql)) {
        const rows = h.anchors.filter((a) => a.id === params[0]);
        return { rows, rowCount: rows.length };
      }
      if (/FROM anchor_store WHERE document_id = \$1/.test(sql)) {
        const rows = h.anchors.filter((a) => a.document_id === params[0]);
        return { rows, rowCount: rows.length };
      }
      return { rows: [], rowCount: 0 };
    },
    transaction: async (fn: (client: unknown) => Promise<unknown>) => {
      h.probes += 1;
      if (h.probeFault) throw new Error('connect ECONNREFUSED 127.0.0.1:5432 (KS-1822 planted probe fault)');
      return fn(probeClient);
    },
  };
});

const TENANT_A = 'a1822000-0000-4000-8000-00000000000a';
const TENANT_B = 'b1822000-0000-4000-8000-00000000000b';
const ORG_A = 'c1822000-0000-4000-8000-0000000000ca';
const ORG_B = 'c1822000-0000-4000-8000-0000000000cb';
/** Tenant B's document, held by its EXTERNAL id (originate's document anchors send that). */
const FOREIGN_DOC = 'doc-1761700000000-ks1822f';
/** Tenant A's document, held by its PRIMARY key (certification anchors send that). */
const OWN_DOC = 'd1822000-0000-4000-8000-0000000000d1';
/** No `documents` row holds this id — a Platform S flat anchor. */
const FLAT_DOC = 's-flat-ks1822-0001';
const FOREIGN_ANCHOR = 'anchor_e1822000-0000-4000-8000-0000000000e1';
const OWN_ANCHOR = 'anchor_e1822000-0000-4000-8000-0000000000e2';
const FLAT_ANCHOR = 'anchor_e1822000-0000-4000-8000-0000000000e3';
const TX = 'ab'.repeat(32);
const HASH = 'cd'.repeat(32);
const SIG = 'ef'.repeat(32);
const COMMITMENT = '12'.repeat(32);
const CREATED_AT = '2026-10-29T12:00:00.000Z';
const CONFIRMED_AT = '2026-10-29T12:01:00.000Z';

function row(id: string, documentId: string): Record<string, unknown> {
  return {
    id, document_id: documentId, anchor_type: 'single', content_hash: HASH, network: 'preview', metadata_label: 674,
    // KS-1175 identity fields and the KS-1454 signature hash, so the own-tenant cells compare the whole view.
    metadata_payload: { secuura: { documentType: 'sign', identityCommitment: COMMITMENT, actorDid: 'did:key:z6MkKs1822', actorLevel: 'L2', orgVerified: 'true', signatureHash: SIG } },
    status: 'confirmed', transaction_hash: TX, block_hash: null, block_number: '4242', confirmed_at: CONFIRMED_AT,
    error_message: null, retry_count: 0, simulated: false, created_at: CREATED_AT, updated_at: CONFIRMED_AT,
  };
}
const FOREIGN_ROW = row(FOREIGN_ANCHOR, FOREIGN_DOC);
const OWN_ROW = row(OWN_ANCHOR, OWN_DOC);
const FLAT_ROW = row(FLAT_ANCHOR, FLAT_DOC);
const DOCUMENTS = [
  { id: 'f1822000-0000-4000-8000-0000000000f1', external_id: FOREIGN_DOC, tenant_id: TENANT_B },
  { id: OWN_DOC, external_id: null, tenant_id: TENANT_A },
];

/** The body `GET /api/anchors/:id` answered for OWN_ROW on develop — the gate must not change one key of it. */
function byIdBody(documentId: string): Record<string, unknown> {
  return {
    documentId, transactionId: TX, transactionHash: TX, status: 'confirmed', blockNumber: 4242, network: 'preview',
    anchoredAt: CONFIRMED_AT, createdAt: CREATED_AT, contentHash: HASH, verified: true,
    identityCommitment: COMMITMENT, identity: { actorDid: 'did:key:z6MkKs1822', actorLevel: 'L2', orgVerified: true },
    signatureHash: SIG,
    // KS-1384 F-a added payloadTimestamp to this route (the stored payload's secuura.timestamp). null here because
    // this fixture's payload carries no timestamp; the gate still must not change any other key.
    payloadTimestamp: null,
    errorMessage: null, retryCount: 0,
  };
}
/** The body `GET /api/anchors/document/:documentId` answered for one row on develop. */
function byDocumentBody(anchorId: string, documentId: string): Record<string, unknown> {
  return {
    success: true,
    data: {
      documentId,
      anchors: [{
        id: anchorId, documentId, anchorType: 'single', contentHash: HASH, transactionHash: TX, blockHash: null, blockNumber: 4242,
        network: 'preview', metadataLabel: 674, status: 'confirmed', confirmations: 0, confirmedAt: CONFIRMED_AT, createdAt: CREATED_AT,
      }],
      count: 1,
    },
  };
}

const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIVATE_PEM = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const PUBLIC_PEM = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const b64url = (b: Buffer): string => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
function token(claims: Record<string, unknown>): string {
  const header = b64url(Buffer.from(JSON.stringify({ alg: 'RS256', typ: 'JWT' })));
  const now = Math.floor(Date.now() / 1000);
  const payload = b64url(Buffer.from(JSON.stringify({ iat: now, exp: now + 600, ...claims })));
  return `${header}.${payload}.${b64url(crypto.sign('RSA-SHA256', Buffer.from(`${header}.${payload}`), PRIVATE_PEM))}`;
}
const caller = (tenantId: string | undefined, organizationId: string = ORG_A): string =>
  token({ userId: '2a182200-0000-4000-8000-0000000018a2', role: 'user', organizationId, ...(tenantId === undefined ? {} : { tenantId }) });
const IN_A = (): string => caller(TENANT_A);
const IN_B = (): string => caller(TENANT_B, ORG_B);

/** Everything a client can observe about a response except the clock (Date). */
type Wire = { status: number; type: string | null; length: string | null; etag: string | null; body: string };

let server: http.Server;
let base = '';
const logLines: string[] = [];

async function get(path: string, tok: string): Promise<Wire> {
  const res = await fetch(`${base}${path}`, { headers: { Authorization: `Bearer ${tok}` } });
  const body = await res.text();
  return { status: res.status, type: res.headers.get('content-type'), length: res.headers.get('content-length'), etag: res.headers.get('etag'), body };
}
/** The same request against the same app with NO rows stored — what "absent" answers. */
async function absent(path: string, tok: string): Promise<Wire> {
  const saved = h.anchors;
  h.anchors = [];
  try { return await get(path, tok); } finally { h.anchors = saved; }
}
/** index.ts `log()` writes one JSON object per console.log line; the KS-1822 ones. */
function ks1822Lines(): Array<Record<string, unknown>> {
  return logLines
    .filter((l) => l.startsWith('{') && l.includes('KS-1822'))
    .map((l) => JSON.parse(l) as Record<string, unknown>);
}

beforeAll(async () => {
  process.env.JWT_PUBLIC_KEY = Buffer.from(PUBLIC_PEM, 'utf8').toString('base64');
  delete process.env.JWT_JWKS_URL;
  delete process.env.AUTH_SERVICE_URL;
  delete process.env.PLATFORM_WALLET_MNEMONIC;
  delete process.env.BLOCKFROST_API_KEY;
  delete process.env.DATABASE_URL;
  process.env.CARDANO_NETWORK = 'preview';
  vi.spyOn(console, 'log').mockImplementation((...args: unknown[]) => { logLines.push(args.map(String).join(' ')); });
  vi.spyOn(express.application, 'listen').mockReturnValue(
    { keepAliveTimeout: 0, headersTimeout: 0, close: () => undefined } as unknown as http.Server,
  );
  const app = (await import('../index')).default;
  server = http.createServer(app);
  await new Promise<void>((resolve) => { server.listen(0, '127.0.0.1', resolve); });
  base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
}, 60000);

afterAll(async () => {
  (server as any)?.closeAllConnections?.();
  await new Promise<void>((resolve) => (server ? server.close(() => resolve()) : resolve()));
  vi.restoreAllMocks();
});

beforeEach(() => {
  h.anchors = [FOREIGN_ROW, OWN_ROW, FLAT_ROW];
  h.documents = DOCUMENTS;
  h.probeFault = false;
  h.probes = 0;
  logLines.length = 0;
});

describe('KS-1822 — a foreign tenant\'s anchor is refused, and the refusal is indistinguishable from absent', () => {
  it('RED R1 GET /api/anchors/:id — another tenant\'s anchor answers 404, byte-identical to the same id with no row', async () => {
    const tok = IN_A();
    const path = `/api/anchors/${FOREIGN_ANCHOR}`;
    const refused = await get(path, tok);
    const none = await absent(path, tok);
    expect(refused.status, `received body: ${refused.body}`).toBe(404);
    expect(refused).toEqual(none);
  });

  it('RED R2 GET /api/anchors/:id through the DOCUMENT-ID fallback — refused, byte-identical to that document id with no rows', async () => {
    const tok = IN_A();
    const path = `/api/anchors/${FOREIGN_DOC}`;
    const refused = await get(path, tok);
    const none = await absent(path, tok);
    expect(refused.status, `received body: ${refused.body}`).toBe(404);
    expect(refused).toEqual(none);
  });

  it('RED R3 GET /api/anchors/document/:documentId — another tenant\'s document answers 404, byte-identical to no rows', async () => {
    const tok = IN_A();
    const path = `/api/anchors/document/${FOREIGN_DOC}`;
    const refused = await get(path, tok);
    const none = await absent(path, tok);
    expect(refused.status, `received body: ${refused.body}`).toBe(404);
    expect(refused).toEqual(none);
  });

  it('CONTROL R4 the owner\'s tenant reads its anchor with the body unchanged — own row for tenant A, the R1 row for tenant B', async () => {
    const own = await get(`/api/anchors/${OWN_ANCHOR}`, IN_A());
    expect(own.status, `received body: ${own.body}`).toBe(200);
    expect(JSON.parse(own.body)).toEqual(byIdBody(OWN_DOC));
    const theirs = await get(`/api/anchors/${FOREIGN_ANCHOR}`, IN_B());
    expect(theirs.status, `received body: ${theirs.body}`).toBe(200);
    expect(JSON.parse(theirs.body)).toEqual(byIdBody(FOREIGN_DOC));
  });

  it('CONTROL R5 own tenant through the document-id fallback and through /document — 200, bodies unchanged', async () => {
    const fallback = await get(`/api/anchors/${OWN_DOC}`, IN_A());
    expect(fallback.status, `received body: ${fallback.body}`).toBe(200);
    expect(JSON.parse(fallback.body)).toEqual(byIdBody(OWN_DOC));
    const listing = await get(`/api/anchors/document/${OWN_DOC}`, IN_A());
    expect(listing.status, `received body: ${listing.body}`).toBe(200);
    expect(JSON.parse(listing.body)).toEqual(byDocumentBody(OWN_ANCHOR, OWN_DOC));
  });

  it('CONTROL R6 residual (i): a flat anchor (no document holds its id) stays readable by a caller in any tenant, on both routes', async () => {
    for (const tok of [IN_A(), IN_B()]) {
      const byId = await get(`/api/anchors/${FLAT_ANCHOR}`, tok);
      expect(byId.status, `received body: ${byId.body}`).toBe(200);
      expect(JSON.parse(byId.body)).toEqual(byIdBody(FLAT_DOC));
      const listing = await get(`/api/anchors/document/${FLAT_DOC}`, tok);
      expect(listing.status, `received body: ${listing.body}`).toBe(200);
      expect(JSON.parse(listing.body)).toEqual(byDocumentBody(FLAT_ANCHOR, FLAT_DOC));
    }
  });

  it('RED R7 residual (ii): a caller with no usable tenant claim still reads the foreign anchor — without reaching the probe, and says so in one warn line', async () => {
    for (const tenantId of [undefined, '', '   ', 'not-a-uuid']) {
      logLines.length = 0;
      h.probes = 0;
      const res = await get(`/api/anchors/${FOREIGN_ANCHOR}`, caller(tenantId));
      expect(res.status, `tenantId=${JSON.stringify(tenantId)} received body: ${res.body}`).toBe(200);
      expect(JSON.parse(res.body)).toEqual(byIdBody(FOREIGN_DOC));
      expect(h.probes).toBe(0);
      const lines = ks1822Lines();
      expect(lines, `tenantId=${JSON.stringify(tenantId)}`).toHaveLength(1);
      expect(lines[0].level).toBe('warn');
      expect(String(lines[0].message)).toContain('no usable tenant claim');
    }
  });

  it('RED R8 residual (iii): a probe fault ALLOWS the read (fail-open) and logs exactly one warn naming it', async () => {
    h.probeFault = true;
    const res = await get(`/api/anchors/${FOREIGN_ANCHOR}`, IN_A());
    expect(res.status, `received body: ${res.body}`).toBe(200);
    expect(JSON.parse(res.body)).toEqual(byIdBody(FOREIGN_DOC));
    expect(h.probes).toBeGreaterThan(0);
    const lines = ks1822Lines();
    expect(lines).toHaveLength(1);
    expect(lines[0].level).toBe('warn');
    expect(String(lines[0].message)).toContain('fail-open');
    expect(lines[0].documentIds).toEqual([FOREIGN_DOC]);
  });

  it('RED R9 the refusal response names no tenant and no organisation; the server log line names the document and BOTH tenants', async () => {
    const paths = [`/api/anchors/${FOREIGN_ANCHOR}`, `/api/anchors/${FOREIGN_DOC}`, `/api/anchors/document/${FOREIGN_DOC}`];
    for (const path of paths) {
      logLines.length = 0;
      const refused = await get(path, IN_A());
      expect(refused.status, `${path} received body: ${refused.body}`).toBe(404);
      for (const secret of [TENANT_B, TENANT_A, ORG_A, ORG_B]) expect(refused.body).not.toContain(secret);
      const lines = ks1822Lines();
      expect(lines, path).toHaveLength(1);
      expect(String(lines[0].message)).toContain('refused an anchor read');
      expect([lines[0].documentId, lines[0].ownerTenantId, lines[0].callerTenantId]).toEqual([FOREIGN_DOC, TENANT_B, TENANT_A]);
    }
  });

  it('CONTROL R10 a tenant claim that differs from the owner\'s only in letter case is the SAME tenant (200, and no KS-1822 line: not treated as unusable)', async () => {
    const res = await get(`/api/anchors/${OWN_ANCHOR}`, caller(TENANT_A.toUpperCase()));
    expect(res.status, `received body: ${res.body}`).toBe(200);
    expect(JSON.parse(res.body)).toEqual(byIdBody(OWN_DOC));
    expect(ks1822Lines()).toHaveLength(0);
  });

  it('RED R11 the comparison is tenant to tenant: a caller whose ORGANISATION id equals the owner tenant id is still refused', async () => {
    const res = await get(`/api/anchors/${FOREIGN_ANCHOR}`, caller(TENANT_A, TENANT_B));
    expect(res.status, `received body: ${res.body}`).toBe(404);
  });

  it('CONTROL R12 a read that found NO rows answers the route\'s own 404 with no probe and no KS-1822 line, even for a tenantless caller', async () => {
    h.anchors = [];
    const res = await get('/api/anchors/document/doc-ks1822-nothing-stored', caller(undefined));
    expect(res.status, `received body: ${res.body}`).toBe(404);
    expect(JSON.parse(res.body)).toEqual({ success: false, error: { code: 'NOT_FOUND', message: 'No anchors found' } });
    expect(h.probes).toBe(0);
    expect(ks1822Lines()).toHaveLength(0);
  });
});
