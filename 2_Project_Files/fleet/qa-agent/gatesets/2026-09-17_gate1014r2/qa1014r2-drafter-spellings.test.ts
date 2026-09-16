/**
 * QA DRAFTER #1014 ROUND 2 (KS-1176 F-1) — every spelling a caller could use to name a document type, through the REAL index.ts app.
 * An INSTRUMENT, copied into a scratch tree, run alone, quarantined by rename. Never committed. Same file on base / r1 / head / merged.
 * Substrate (as the round-1 GATE's census harness): the real app (default export of ../index), the real services/redis.ts in its in-memory
 * fallback, the catalogue seeded through the REAL admin seed route, one synthetic approval type through the REAL admin POST, one loopback stub
 * for security validate / auth connector-token mint / originate / anchoring. HIT COUNTERS: ../services/enforcement is wrapped (importOriginal:
 * the REAL enforceDocumentTypeRules and createWorkflowInstanceIfRequired run; the wrapper only counts and records the RESOLVED docType code).
 * originate's persistence is NOT run: the forwarded raw body is recorded and originate's resolution is applied by READ
 * (services/originate/src/routes/documents.ts:381-415 destructure + string check, :565 docType, :567-574 data blob, :1051-1053 read surface).
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import fs from 'fs';
import jwt from 'jsonwebtoken';
import type { AddressInfo } from 'net';

const hits = vi.hoisted(() => ({ enforce: 0, workflow: 0, resolved: [] as Array<{ ok: boolean; code: string | null; keyCode: string | null; status: number | null; err: string | null }> }));
vi.mock('../services/enforcement', async (importOriginal) => {
  const m: any = await importOriginal();
  return {
    ...m,
    enforceDocumentTypeRules: async (body: any, user: any) => {
      hits.enforce++;
      const r = await m.enforceDocumentTypeRules(body, user);
      // KEY PROBE (QA-EDIT-KEYPROBE): which catalogue type did ENFORCEMENT's own key resolution land on, even when this principal was refused?
      // Re-ask the REAL function with a principal that passes every level / MFA check and a metadata object that answers every field.
      let keyCode: string | null = r.ok ? ((r.docType && (r.docType as any).code) || null) : null;
      if (!r.ok) {
        const god = { userId: 'qa-keyprobe', verificationLevel: 'government', mfaEnabled: true, authMethod: 'email' };
        const anyMeta = new Proxy({}, { get: () => 'qa' });
        const r2 = await m.enforceDocumentTypeRules({ ...body, metadata: anyMeta }, god);
        keyCode = r2.ok ? ((r2.docType && (r2.docType as any).code) || null) : null;
      }
      hits.resolved.push({ ok: !!r.ok, code: r.ok ? ((r.docType && (r.docType as any).code) || null) : null, keyCode, status: r.ok ? null : r.status, err: r.ok ? null : r.code });
      return r;
    },
    createWorkflowInstanceIfRequired: async (...a: any[]) => { hits.workflow++; return m.createWorkflowInstanceIfRequired(...a); },
  };
});

const OUT = process.env.QA_OUT || '';
const PRIV = process.env.__TEST_JWT_PRIVATE_PEM || '';
type Rec = { method: string; url: string; headers: Record<string, any>; body: string };
const stubSeen: Rec[] = [];
const KEYS: Record<string, any> = {
  sk_qa_write_000001: { connectorId: 'c-write', scopes: ['documents:write'], tenantId: 't-key' },
  sk_qa_restrict_001: { connectorId: 'c-restricted', scopes: ['documents:write'], tenantId: 't-key' },
  sk_qa_restrict_ssd: { connectorId: 'c-restricted-ssd', scopes: ['documents:write'], tenantId: 't-key' },
  sk_qa_restrict_low: { connectorId: 'c-restricted-lower', scopes: ['documents:write'], tenantId: 't-key' },
  sk_qa_restrict_str: { connectorId: 'c-restricted-string', scopes: ['documents:write'], tenantId: 't-key' },
};
const ALLOW: Record<string, any> = { 'c-restricted': ['DOCUMENT'], 'c-restricted-ssd': ['SSD_DOCUMENT'], 'c-restricted-lower': ['document'], 'c-restricted-string': 'SSD_DOCUMENT' };

function readBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); });
}
function send(base: string, method: string, path: string, headers: Record<string, string>, body?: string): Promise<{ status: number; code: string | null; msg: string | null; text: string; json: any }> {
  return new Promise((resolve, reject) => {
    const u = new URL(base); const h: Record<string, string> = { ...headers };
    if (body !== undefined) { h['content-type'] = 'application/json'; h['content-length'] = String(Buffer.byteLength(body)); }
    const req = http.request({ hostname: u.hostname, port: u.port, path, method, headers: h, agent: false }, (res) => {
      const c: Buffer[] = []; res.on('data', (d) => c.push(d));
      res.on('end', () => {
        const text = Buffer.concat(c).toString(); let json: any = null;
        try { json = JSON.parse(text); } catch { /* recorded as text */ }
        resolve({ status: res.statusCode || 0, code: json?.error?.code ?? json?.code ?? null, msg: json?.error?.message ?? null, text, json });
      });
    });
    req.on('error', (e) => { if ((e as any).qaTimeout) return; reject(e); });
    req.setTimeout(3000, () => { const e: any = new Error('QA client timeout'); e.qaTimeout = true; req.destroy(e); resolve({ status: 0, code: 'QA_CLIENT_TIMEOUT_3S', msg: null, text: '', json: null }); });
    if (body !== undefined) req.end(body); else req.end();
  });
}
async function listen(s: http.Server): Promise<string> {
  await new Promise<void>((r) => s.listen(0, '127.0.0.1', () => r()));
  return `http://127.0.0.1:${(s.address() as AddressInfo).port}`;
}
const rs = (claims: any) => jwt.sign(claims, PRIV, { algorithm: 'RS256', expiresIn: 3600 });

/** originate's create-side resolution, applied by READ to the forwarded raw body (documents.ts:381-415, :565-574, :1051-1053). */
function originateRead(raw: string): { precheck: string | null; storedType: string | null; readSurfaceType: string | null } {
  let b: any; try { b = JSON.parse(raw); } catch { return { precheck: 'unparseable', storedType: null, readSurfaceType: null }; }
  const { type: rawType, data: rawData, documentType } = b;
  if (documentType !== undefined && typeof documentType !== 'string') return { precheck: '400 documentType must be a string', storedType: null, readSurfaceType: null };
  if (rawData !== undefined && (rawData === null || typeof rawData !== 'object' || Array.isArray(rawData))) return { precheck: '400 data must be a JSON object', storedType: null, readSurfaceType: null };
  const docType = documentType || rawType || 'DOCUMENT';
  const data: any = rawData && typeof rawData === 'object' ? { ...rawData } : { documentType: docType };
  if (documentType && !data.documentType) data.documentType = documentType;
  return { precheck: null, storedType: typeof docType === 'string' ? docType : JSON.stringify(docType), readSurfaceType: String(data.documentType || docType) };
}

let stub: http.Server; let stubUrl = ''; let gw: http.Server; let gwUrl = ''; let app: any; let redis: any;
const out: any = { rows: [], meta: {} };

beforeAll(async () => {
  expect(PRIV.length, 'vitest.setup.ts provisioned a throwaway RS256 private key').toBeGreaterThan(100);
  stub = http.createServer(async (req, res) => {
    const body = await readBody(req);
    stubSeen.push({ method: req.method || '', url: req.url || '', headers: { ...req.headers }, body });
    const j = (s: number, o: any) => { res.writeHead(s, { 'content-type': 'application/json' }); res.end(JSON.stringify(o)); };
    if (req.url === '/api/keys/validate') { const k = JSON.parse(body || '{}').key; const m = KEYS[k]; return j(200, m ? { data: { valid: true, ...m } } : { data: { valid: false } }); }
    if (req.url === '/internal/connector-token') {
      const m = KEYS[JSON.parse(body || '{}').apiKey]; if (!m) return j(401, { success: false });
      return j(200, { success: true, data: { token: rs({ userId: `connector:${m.connectorId}`, email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector', tenantId: m.tenantId, scopes: m.scopes }), expiresIn: 600 } });
    }
    if (req.url === '/.well-known/jwks.json') return j(404, {});
    if (req.method === 'POST' && req.url === '/api/documents') return j(201, { success: true, data: { id: 'doc-qa' } });
    return j(404, { success: false });
  });
  stubUrl = await listen(stub);
  vi.resetModules();
  vi.stubEnv('NODE_ENV', 'test'); vi.stubEnv('ENABLE_TEST_TOKENS', 'true');
  for (const k of ['ORIGINATE_SERVICE_URL', 'SECURITY_SERVICE_URL', 'AUTH_SERVICE_URL', 'ANCHORING_SERVICE_URL']) vi.stubEnv(k, stubUrl);
  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
  delete process.env.JWT_JWKS_URL;
  app = (await import('../index')).default;
  redis = await import('../services/redis');
  gw = http.createServer(app as http.RequestListener); gwUrl = await listen(gw);
  expect(redis.isRedisAvailable(), 'no real Redis: the in-memory fallback is the catalogue').toBe(false);
}, 60000);

afterAll(async () => {
  if (gw) { (gw as any).closeAllConnections?.(); await new Promise<void>((r) => gw.close(() => r())); }
  if (stub) { (stub as any).closeAllConnections?.(); await new Promise<void>((r) => stub.close(() => r())); }
  vi.unstubAllEnvs();
}, 30000);

describe('QA #1014 round 2 spellings (instrument)', () => {
  it('runs every type spelling for restricted and unrestricted principals and writes rows', async () => {
    const admin = rs({ userId: 'qa-admin', email: 'a@qa.invalid', role: 'SYSTEM_ADMIN', verificationLevel: 'government', tenantId: 't-admin' });
    const seedRes = await send(gwUrl, 'GET', '/api/admin/document-types', { authorization: `Bearer ${admin}` });
    expect(seedRes.status).toBe(200);
    const ap = await send(gwUrl, 'POST', '/api/admin/document-types', { authorization: `Bearer ${admin}` }, JSON.stringify({ name: 'QA_NONE_APPROVAL', code: 'QA_NONE_APPROVAL', creatorVerificationLevel: 'none', verifierVerificationLevel: 'none', isActive: true, status: 'active', requireMFA: false, allowedAuthProviders: [], requiresApproval: true, approvalWorkflowId: 'wf-qa', metadataSchema: [] }));
    expect(ap.status).toBe(201);
    const catalogue = (await redis.getAllDocumentTypes()) as any[];
    expect(catalogue.length, 'seed (9) + QA_NONE_APPROVAL').toBe(10);
    out.meta.catalogue = catalogue.map((t) => ({ id: t.id, code: t.code, creator: t.creatorVerificationLevel }));
    const idOf = (code: string) => catalogue.find((t) => t.code === code)?.id as string;
    expect(idOf('SSD_DOCUMENT') && idOf('DOCUMENT'), 'seed ids resolved').toBeTruthy();
    await redis.setNotificationSettings('platform-settings', { integrations: Object.entries(ALLOW).map(([id, allowedDocumentTypes]) => ({ id, config: { allowedDocumentTypes } })) });

    const P: Array<{ id: string; allow: any; h: Record<string, string> }> = [
      { id: 'sk_restricted_DOCUMENT', allow: ['DOCUMENT'], h: { 'x-api-key': 'sk_qa_restrict_001' } },
      { id: 'sk_restricted_SSD', allow: ['SSD_DOCUMENT'], h: { 'x-api-key': 'sk_qa_restrict_ssd' } },
      { id: 'sk_restricted_lowercase_document', allow: ['document'], h: { 'x-api-key': 'sk_qa_restrict_low' } },
      { id: 'sk_restricted_STRING_misconfig', allow: 'SSD_DOCUMENT', h: { 'x-api-key': 'sk_qa_restrict_str' } },
      { id: 'sk_write_unrestricted', allow: null, h: { 'x-api-key': 'sk_qa_write_000001' } },
      { id: 'jwt_connector_scoped_bearer', allow: null, h: { authorization: `Bearer ${rs({ userId: 'connector:c-restricted', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector', tenantId: 't-key', scopes: ['documents:write'] })}` } },
      { id: 'jwt_NONE_human', allow: null, h: { authorization: `Bearer ${rs({ userId: 'u-none', email: 'n@qa.invalid', role: 'issuer', verificationLevel: 'NONE', tenantId: 't-h' })}` } },
    ];
    const T = (o: any) => JSON.stringify({ title: 'qa', contentHash: 'a'.repeat(64), ...o });
    const S = 'SSD_DOCUMENT', D = 'DOCUMENT';
    const SHAPES: Array<[string, string]> = [
      ['untyped', T({})],
      ['dt:SSD', T({ documentType: S })], ['ty:SSD', T({ type: S })],
      ['dt:DOC', T({ documentType: D })], ['ty:DOC', T({ type: D })],
      ['dt:PROPERTY_DEED', T({ documentType: 'PROPERTY_DEED' })], ['ty:PROPERTY_DEED', T({ type: 'PROPERTY_DEED' })],
      ['ty:REFERENCE(standard)', T({ type: 'REFERENCE' })], ['ty:QA_NONE_APPROVAL', T({ type: 'QA_NONE_APPROVAL' })], ['ty:QA_UNREGISTERED', T({ type: 'QA_UNREGISTERED' })],
      ['both dt:DOC ty:SSD', T({ documentType: D, type: S })], ['both ty:SSD dt:DOC (key order)', T({ type: S, documentType: D })],
      ['both dt:SSD ty:DOC', T({ documentType: S, type: D })], ['both ty:DOC dt:SSD (key order)', T({ type: D, documentType: S })],
      ['both dt:DOC ty:DOC', T({ documentType: D, type: D })],
      ["dt:'' ty:SSD", T({ documentType: '', type: S })], ["dt:'' ty:DOC", T({ documentType: '', type: D })], ["dt:''", T({ documentType: '' })], ["ty:''", T({ type: '' })],
      ['dt:null ty:SSD', T({ documentType: null, type: S })], ['dt:false ty:SSD', T({ documentType: false, type: S })], ['dt:0 ty:SSD', T({ documentType: 0, type: S })],
      ['dt:true ty:SSD', T({ documentType: true, type: S })], ['dt:123 ty:DOC', T({ documentType: 123, type: D })], ['ty:123', T({ type: 123 })],
      ["dt:['DOCUMENT']", T({ documentType: [D] })], ["ty:['DOCUMENT']", T({ type: [D] })], ["ty:['SSD_DOCUMENT']", T({ type: [S] })], ['dt:{} ty:DOC', T({ documentType: {}, type: D })],
      ['ty:ssd_document', T({ type: 'ssd_document' })], ['ty:document', T({ type: 'document' })], ['dt:document', T({ documentType: 'document' })], ['ty:Ssd_Document', T({ type: 'Ssd_Document' })],
      ["ty:' SSD_DOCUMENT'", T({ type: ' ' + S })], ["ty:'SSD_DOCUMENT '", T({ type: S + ' ' })], ["ty:'DOCUMENT '", T({ type: D + ' ' })], ["ty:' '", T({ type: ' ' })],
      ['ty:TAB+SSD', T({ type: '\t' + S })], ['ty:SSD+ZWSP', T({ type: S + '​' })],
      ['ty:<SSD id>', T({ type: idOf(S) })], ['dt:<SSD id>', T({ documentType: idOf(S) })], ['ty:<DOCUMENT id>', T({ type: idOf(D) })],
      ['key DocumentType:SSD', T({ DocumentType: S })], ['key document_type:SSD', T({ document_type: S })], ['key Type:SSD', T({ Type: S })],
      ['dup dt SSD then DOC (raw)', `{"title":"qa","documentType":"${S}","documentType":"${D}"}`], ['dup dt DOC then SSD (raw)', `{"title":"qa","documentType":"${D}","documentType":"${S}"}`],
      ['dup ty DOC then SSD (raw)', `{"title":"qa","type":"${D}","type":"${S}"}`],
      ['escaped key document\\u0054ype:SSD (raw)', `{"title":"qa","document\\u0054ype":"${S}"}`], ['escaped key typ\\u0065:SSD (raw)', `{"title":"qa","typ\\u0065":"${S}"}`],
      ['__proto__.type:SSD (raw)', `{"title":"qa","__proto__":{"type":"${S}"}}`],
      ['legacy ty:DOC data.documentType:PROPERTY_DEED', T({ type: D, data: { title: 'qa', documentType: 'PROPERTY_DEED' } })],
      ['legacy untyped data.documentType:DEGREE', T({ data: { title: 'qa', documentType: 'DEGREE' } })],
      ['dt:DOC data.documentType:SSD', T({ documentType: D, data: { title: 'qa', documentType: S } })],
      ['ty:DOC metadata.documentType:SSD', T({ type: D, metadata: { documentType: S } })],
    ];
    out.meta.shapes = SHAPES.map((s) => s[0]); out.meta.principals = P.map((p) => ({ id: p.id, allow: p.allow }));
    for (const p of P) {
      for (const [sid, raw] of SHAPES) {
        const e0 = hits.enforce, w0 = hits.workflow, r0 = hits.resolved.length, s0 = stubSeen.length;
        const wfBefore = (await redis.getAllWorkflowInstances()).length;
        const r = await send(gwUrl, 'POST', '/api/documents', p.h, raw);
        const fwd = stubSeen.slice(s0).find((s) => s.method === 'POST' && s.url === '/api/documents');
        const wfAfter = (await redis.getAllWorkflowInstances()).length;
        const allowMsg = r.status === 403 && r.code === 'FORBIDDEN' && /^Connector is not permitted to register document type "/.test(r.msg || '');
        out.rows.push({
          principal: p.id, allow: p.allow, shape: sid, status: r.status, code: r.code,
          allowlist_refused: allowMsg, allowlist_named: allowMsg ? (r.msg as string).replace(/^Connector is not permitted to register document type "/, '').replace(/"$/, '') : null,
          enforce_hits: hits.enforce - e0, workflow_hits: hits.workflow - w0, workflow_instances: wfAfter - wfBefore,
          enforcement: hits.resolved.length > r0 ? hits.resolved[hits.resolved.length - 1] : null,
          forwarded: !!fwd, originate_read: fwd ? originateRead(fwd.body) : null, forwarded_body_identical: fwd ? fwd.body === raw : null,
        });
      }
    }
    if (OUT) fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
    expect(out.rows.length).toBe(P.length * SHAPES.length);
  }, 600000);
});
