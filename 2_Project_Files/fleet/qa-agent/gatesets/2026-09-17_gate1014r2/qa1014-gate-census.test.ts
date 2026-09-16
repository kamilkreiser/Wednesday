/**
 * QA gate #1014 (KS-1176) — principal x type census through the REAL index.ts app.
 * An INSTRUMENT, copied into a scratch tree, run alone, quarantined by rename. Never committed.
 * Same file on base / head / merged; tree-dependent expectations live in compare.py, not here.
 * Substrate: the real app (default export of ../index, require.main guard keeps it from booting),
 * the real services/redis.ts in its in-memory fallback (no client is connected: initRedis only runs
 * in startServer), catalogue seeded through the REAL admin seed route GET /api/admin/document-types,
 * synthetic types added through the REAL admin POST /api/admin/document-types. One loopback stub stands
 * in for security (/api/keys/validate), auth (/internal/connector-token, /.well-known/jwks.json 404),
 * originate (POST/GET /api/documents) and anchoring. RS256 keys: vitest.setup.ts's per-run throwaway pair.
 */
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import http from 'http';
import fs from 'fs';
import express from 'express';
import jwt from 'jsonwebtoken';
import type { AddressInfo } from 'net';

const OUT = process.env.QA_OUT || '';
const PRIV = process.env.__TEST_JWT_PRIVATE_PEM || '';

type Rec = { method: string; url: string; headers: Record<string, any>; body: string };
const stubSeen: Rec[] = [];
const minted: string[] = [];

// ---- throwaway sk_ keys (validate table) ----
const KEYS: Record<string, any> = {
  sk_qa_write_000001: { connectorId: 'c-write', scopes: ['documents:write'], organizationId: 'org-key', tenantId: 't-key', tenantSlug: 'key' },
  sk_qa_noscope_0001: { connectorId: 'c-noscope', scopes: [], organizationId: 'org-key', tenantId: 't-key' },
  sk_qa_restrict_001: { connectorId: 'c-restricted', scopes: ['documents:write'], organizationId: 'org-key', tenantId: 't-key' },
  sk_qa_bypass_00001: { connectorId: 'c-bypass', scopes: ['documents:write'], organizationId: 'org-key', tenantId: 't-key' },
  sk_qa_wildcard_001: { connectorId: 'c-wild', scopes: ['*'], organizationId: 'org-key', tenantId: 't-key' },
  sk_qa_notenant_001: { connectorId: 'c-notenant', scopes: ['documents:write'] },
  sk_qa_readonly_001: { connectorId: 'c-read', scopes: ['documents:read'], organizationId: 'org-key', tenantId: 't-key' },
  sk_qa_ratelimit_01: { connectorId: 'c-rl', scopes: ['documents:write'], tenantId: 't-key', rateLimit: 2, rateLimitWindow: 60 },
  sk_qa_ratelimit_02: { connectorId: 'c-rl-ctrl', scopes: ['documents:write'], tenantId: 't-key', rateLimit: 2, rateLimitWindow: 60 },
};

function readBody(req: http.IncomingMessage): Promise<string> {
  return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); });
}
function send(base: string, method: string, path: string, headers: Record<string, string>, body?: string): Promise<{ status: number; code: string | null; text: string; headers: Record<string, any>; json: any }> {
  return new Promise((resolve, reject) => {
    const u = new URL(base);
    const h: Record<string, string> = { ...headers };
    if (body !== undefined) { h['content-type'] = h['content-type'] || 'application/json'; h['content-length'] = String(Buffer.byteLength(body)); }
    const req = http.request({ hostname: u.hostname, port: u.port, path, method, headers: h, agent: false }, (res) => {
      const c: Buffer[] = []; res.on('data', (d) => c.push(d));
      res.on('end', () => {
        const text = Buffer.concat(c).toString(); let json: any = null; let code: string | null = null;
        try { json = JSON.parse(text); code = json?.error?.code ?? json?.code ?? null; } catch { /* non-JSON body recorded as text */ }
        resolve({ status: res.statusCode || 0, code, text, headers: res.headers as any, json });
      });
    });
    req.on('error', (e) => { if ((e as any).qaTimeout) return; reject(e); });
    req.setTimeout(3000, () => { const e: any = new Error('QA client timeout'); e.qaTimeout = true; req.destroy(e); resolve({ status: 0, code: 'QA_CLIENT_TIMEOUT_3S', text: '', headers: {}, json: null }); }); // QA-EDIT-CLIENT-TIMEOUT
    if (body !== undefined) req.end(body); else req.end();
  });
}
async function listen(s: http.Server): Promise<string> {
  await new Promise<void>((r) => s.listen(0, '127.0.0.1', () => r()));
  return `http://127.0.0.1:${(s.address() as AddressInfo).port}`;
}
const b64 = (o: any) => Buffer.from(JSON.stringify(o)).toString('base64');
const rs = (claims: any) => jwt.sign(claims, PRIV, { algorithm: 'RS256', expiresIn: 3600 });

let stub: http.Server; let stubUrl = '';
let gw: http.Server; let gwUrl = '';
let app: any; let redis: any; let auth: any; let rle: any; let enforcement: any;
const out: any = { rows: [], verify: [], pure: [], ratelimit: {}, tenant: [], seed: {}, reach: {}, admin_probe: {}, meta: {} };

beforeAll(async () => {
  expect(PRIV.length, 'vitest.setup.ts provisioned a throwaway RS256 private key').toBeGreaterThan(100);
  stub = http.createServer(async (req, res) => {
    const body = await readBody(req);
    stubSeen.push({ method: req.method || '', url: req.url || '', headers: { ...req.headers }, body });
    const j = (s: number, o: any) => { res.writeHead(s, { 'content-type': 'application/json' }); res.end(JSON.stringify(o)); };
    if (req.url === '/api/keys/validate') { const k = JSON.parse(body || '{}').key; const m = KEYS[k]; return j(200, m ? { data: { valid: true, ...m } } : { data: { valid: false } }); }
    if (req.url === '/internal/connector-token') {
      const k = JSON.parse(body || '{}').apiKey; const m = KEYS[k];
      if (!m) return j(401, { success: false });
      // mirrors auth services/jwt.ts generateConnectorToken claims (READ at head)
      const t = rs({ userId: `connector:${m.connectorId || 'api-key'}`, email: 'connector@secuura.io', role: 'connector', ...(m.organizationId ? { organizationId: m.organizationId } : {}), verificationLevel: 'api_key', type: 'connector', ...(m.tenantId ? { tenantId: m.tenantId } : {}), scopes: m.scopes || [] });
      minted.push(t); return j(200, { success: true, data: { token: t, expiresIn: 600 } });
    }
    if (req.url === '/.well-known/jwks.json') return j(404, {});
    if (req.method === 'POST' && req.url === '/api/documents') { let id = 'doc-x'; try { id = 'doc-' + JSON.parse(body).title; } catch { /* keep */ } return j(201, { success: true, data: { id } }); }
    const m = /^\/api\/documents\/vdoc-(.*)$/.exec(req.url || '');
    if (req.method === 'GET' && m) return j(200, { id: `vdoc-${m[1]}`, documentType: decodeURIComponent(m[1]), status: 'anchored' });
    return j(404, { success: false });
  });
  stubUrl = await listen(stub);
  vi.resetModules();
  vi.stubEnv('NODE_ENV', 'test');
  vi.stubEnv('ENABLE_TEST_TOKENS', 'true');
  vi.stubEnv('ORIGINATE_SERVICE_URL', stubUrl);
  vi.stubEnv('SECURITY_SERVICE_URL', stubUrl);
  vi.stubEnv('AUTH_SERVICE_URL', stubUrl);
  vi.stubEnv('ANCHORING_SERVICE_URL', stubUrl);
  vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
  delete process.env.JWT_JWKS_URL;
  app = (await import('../index')).default;
  redis = await import('../services/redis');
  auth = await import('../middleware/auth');
  rle = await import('../middleware/rateLimitEnforce');
  enforcement = await import('../services/enforcement');
  gw = http.createServer(app as http.RequestListener);
  gwUrl = await listen(gw);
  out.meta.redisAvailable = redis.isRedisAvailable();
  expect(redis.isRedisAvailable(), 'no real Redis: the in-memory fallback is the catalogue').toBe(false);
}, 60000);

afterAll(async () => {
  if (gw) { (gw as any).closeAllConnections?.(); await new Promise<void>((r) => gw.close(() => r())); }
  if (stub) { (stub as any).closeAllConnections?.(); await new Promise<void>((r) => stub.close(() => r())); }
  vi.unstubAllEnvs();
}, 30000);

describe('QA #1014 census (instrument)', () => {
  it('runs the census and writes rows', async () => {
    const admin = rs({ userId: 'qa-admin', email: 'a@qa.invalid', role: 'SYSTEM_ADMIN', verificationLevel: 'government', tenantId: 't-admin' }); // QA-EDIT-ROLE
    // --- seed through the REAL admin route (empty catalogue -> SEED_DOCUMENT_TYPES) ---
    expect((await redis.getAllDocumentTypes()).length, 'catalogue empty before seed').toBe(0);
    const seedRes = await send(gwUrl, 'GET', '/api/admin/document-types', { authorization: `Bearer ${admin}` });
    expect(Array.isArray(seedRes.json), `seed route answered ${seedRes.status} ${seedRes.text.slice(0, 300)}`).toBe(true);
    const seeded = (seedRes.json || []) as any[];
    out.seed = { status: seedRes.status, count: seeded.length, types: seeded.map((t) => ({ code: t.code, creator: t.creatorVerificationLevel, verifier: t.verifierVerificationLevel, mfa: t.requireMFA, providers: t.allowedAuthProviders, approval: t.requiresApproval, wf: t.approvalWorkflowId, schema: (t.metadataSchema || []).filter((f: any) => f.required).map((f: any) => f.name) })) };
    expect(seedRes.status).toBe(200);
    expect(seeded.length, 'seed route registered the seed catalogue').toBeGreaterThanOrEqual(9);
    // --- synthetic types through the REAL admin POST (stores the body verbatim) ---
    const base = { isActive: true, status: 'active', requireMFA: false, allowedAuthProviders: [], requiresApproval: false, approvalWorkflowId: null, metadataSchema: [], verifierVerificationLevel: 'none' };
    const synth: Record<string, any> = {
      QA_NONE_UPPER: { creatorVerificationLevel: 'NONE' },
      QA_EMPTY: { creatorVerificationLevel: '' },
      QA_ABSENT: {},
      QA_NONE_SPACE: { creatorVerificationLevel: ' none' },
      QA_TYPO: { creatorVerificationLevel: 'standrd' },
      QA_BASIC: { creatorVerificationLevel: 'basic' },
      QA_SOCIAL: { creatorVerificationLevel: 'SOCIAL' },
      QA_GOV: { creatorVerificationLevel: 'government' },
      QA_NONE_MFA: { creatorVerificationLevel: 'none', requireMFA: true },
      QA_NONE_PROVIDER: { creatorVerificationLevel: 'none', allowedAuthProviders: ['google'] },
      QA_NONE_APIKEY_PROVIDER: { creatorVerificationLevel: 'none', allowedAuthProviders: ['api_key'] },
      QA_NONE_APPROVAL: { creatorVerificationLevel: 'none', requiresApproval: true, approvalWorkflowId: 'wf-qa' },
      QA_NONE_INACTIVE: { creatorVerificationLevel: 'none', isActive: false },
      QA_NONE_SCHEMA: { creatorVerificationLevel: 'none', metadataSchema: [{ name: 'ref', required: true }] },
      QA_V_NONE_UPPER: { creatorVerificationLevel: 'none', verifierVerificationLevel: 'NONE' },
      QA_V_EMPTY: { creatorVerificationLevel: 'none', verifierVerificationLevel: '' },
      QA_V_ABSENT: { creatorVerificationLevel: 'none', verifierVerificationLevel: undefined },
      QA_V_NONE_SPACE: { creatorVerificationLevel: 'none', verifierVerificationLevel: ' none' },
      QA_V_TYPO: { creatorVerificationLevel: 'none', verifierVerificationLevel: 'standrd' },
      QA_V_BASIC: { creatorVerificationLevel: 'none', verifierVerificationLevel: 'basic' },
      QA_V_STANDARD: { creatorVerificationLevel: 'none', verifierVerificationLevel: 'standard' },
      QA_V_GOV: { creatorVerificationLevel: 'none', verifierVerificationLevel: 'GOVERNMENT' },
    };
    for (const [code, extra] of Object.entries(synth)) {
      const doc: any = { name: code, code, ...base, ...extra };
      if (!('creatorVerificationLevel' in extra)) delete doc.creatorVerificationLevel;
      if ('verifierVerificationLevel' in extra && extra.verifierVerificationLevel === undefined) delete doc.verifierVerificationLevel;
      const r = await send(gwUrl, 'POST', '/api/admin/document-types', { authorization: `Bearer ${admin}` }, JSON.stringify(doc));
      expect(r.status, `admin POST ${code}`).toBe(201);
      await new Promise((res) => setTimeout(res, 5)); // QA-EDIT-SPACING: ids are dt-${Date.now()}; same-ms creates collide
    }
    const catalogue = (await redis.getAllDocumentTypes()) as any[];
    expect(catalogue.length, 'every seeded and synthetic type is in the catalogue').toBe(seeded.length + Object.keys(synth).length);
    out.meta.catalogue = catalogue.map((t) => ({ code: t.code, creator: t.creatorVerificationLevel ?? '<absent>', verifier: t.verifierVerificationLevel ?? '<absent>', mfa: t.requireMFA, providers: t.allowedAuthProviders, approval: t.requiresApproval, wf: t.approvalWorkflowId, active: t.isActive, schema: (t.metadataSchema || []).filter((f: any) => f.required).map((f: any) => f.name) }));
    await redis.setNotificationSettings('platform-settings', { integrations: [
      { id: 'c-restricted', config: { allowedDocumentTypes: ['DOCUMENT'] } },
      { id: 'c-bypass', config: { workflowPolicy: 'bypass' } },
    ] });

    // --- principals ---
    const tt = (o: any) => `Bearer test_token_${b64({ sub: 'tt-user', role: 'issuer', ...o })}`;
    const P: Array<{ id: string; claim: string; h: Record<string, string> }> = [
      { id: 'anonymous', claim: '<anon>', h: {} },
      { id: 'sk_write', claim: 'api_key', h: { 'x-api-key': 'sk_qa_write_000001' } },
      { id: 'sk_noscope', claim: 'api_key', h: { 'x-api-key': 'sk_qa_noscope_0001' } },
      { id: 'sk_readonly', claim: 'api_key', h: { 'x-api-key': 'sk_qa_readonly_001' } },
      { id: 'sk_restricted_DOCUMENT', claim: 'api_key', h: { 'x-api-key': 'sk_qa_restrict_001' } },
      { id: 'sk_bypass_workflow', claim: 'api_key', h: { 'x-api-key': 'sk_qa_bypass_00001' } },
      { id: 'sk_wildcard', claim: 'api_key', h: { 'x-api-key': 'sk_qa_wildcard_001' } },
      { id: 'sk_invalid', claim: '<invalid>', h: { 'x-api-key': 'sk_qa_not_a_key_01' } },
      { id: 'xapikey_not_sk_prefix', claim: '<anon>', h: { 'x-api-key': 'SK_qa_write_000001' } },
      { id: 'jwt_connector_scoped', claim: 'api_key', h: { authorization: `Bearer ${rs({ userId: 'connector:c-jwt', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector', tenantId: 't-key', scopes: ['documents:write'] })}` } },
      { id: 'jwt_connector_noscope', claim: 'api_key', h: { authorization: `Bearer ${rs({ userId: 'connector:c-jwt0', email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector', tenantId: 't-key', scopes: [] })}` } },
      { id: 'jwt_NONE', claim: 'NONE', h: { authorization: `Bearer ${rs({ userId: 'u-none', email: 'n@qa.invalid', role: 'issuer', verificationLevel: 'NONE', tenantId: 't-h' })}` } },
      { id: 'jwt_BASIC', claim: 'BASIC', h: { authorization: `Bearer ${rs({ userId: 'u-basic', email: 'b@qa.invalid', role: 'issuer', verificationLevel: 'BASIC', tenantId: 't-h' })}` } },
      { id: 'jwt_SOCIAL', claim: 'SOCIAL', h: { authorization: `Bearer ${rs({ userId: 'u-soc', email: 's@qa.invalid', role: 'issuer', verificationLevel: 'SOCIAL', tenantId: 't-h' })}` } },
      { id: 'jwt_STANDARD_mfa', claim: 'STANDARD', h: { authorization: `Bearer ${rs({ userId: 'u-std', email: 'st@qa.invalid', role: 'issuer', verificationLevel: 'STANDARD', mfaEnabled: true, authMethod: 'entra', tenantId: 't-h' })}` } },
      { id: 'jwt_ENHANCED_mfa', claim: 'ENHANCED', h: { authorization: `Bearer ${rs({ userId: 'u-enh', email: 'e@qa.invalid', role: 'issuer', verificationLevel: 'ENHANCED', mfaEnabled: true, authMethod: 'entra', tenantId: 't-h' })}` } },
      { id: 'jwt_GOVERNMENT_mfa', claim: 'GOVERNMENT', h: { authorization: `Bearer ${rs({ userId: 'u-gov', email: 'g@qa.invalid', role: 'issuer', verificationLevel: 'GOVERNMENT', mfaEnabled: true, authMethod: 'entra', tenantId: 't-h' })}` } },
      { id: 'jwt_no_level_claim', claim: '<absent>', h: { authorization: `Bearer ${rs({ userId: 'u-nolvl', email: 'x@qa.invalid', role: 'issuer', tenantId: 't-h' })}` } },
      { id: 'jwt_level_number7', claim: '<number>', h: { authorization: `Bearer ${rs({ userId: 'u-num', email: 'x@qa.invalid', role: 'issuer', verificationLevel: 7, tenantId: 't-h' })}` } },
      { id: 'jwt_level_array', claim: '<array>', h: { authorization: `Bearer ${rs({ userId: 'u-arr', email: 'x@qa.invalid', role: 'issuer', verificationLevel: ['standard'], tenantId: 't-h' })}` } },
      { id: 'jwt_level_api_key_human', claim: 'api_key', h: { authorization: `Bearer ${rs({ userId: 'u-apikeylvl', email: 'x@qa.invalid', role: 'issuer', verificationLevel: 'api_key', tenantId: 't-h' })}` } },
      { id: 'tt_api_key', claim: 'api_key', h: { authorization: tt({ verificationLevel: 'api_key', authMethod: 'api_key' }) } },
      { id: 'tt_API_KEY', claim: 'API_KEY', h: { authorization: tt({ verificationLevel: 'API_KEY' }) } },
      { id: 'tt_oauth_app', claim: 'oauth_app', h: { authorization: tt({ verificationLevel: 'oauth_app', authMethod: 'oauth_app' }) } },
      { id: 'tt_FULL', claim: 'FULL', h: { authorization: tt({ verificationLevel: 'FULL' }) } },
      { id: 'tt_kyc_pending', claim: 'kyc-pending', h: { authorization: tt({ verificationLevel: 'kyc-pending' }) } },
      { id: 'tt_space_standard', claim: ' standard', h: { authorization: tt({ verificationLevel: ' standard' }) } },
      { id: 'tt_standard_space', claim: 'standard ', h: { authorization: tt({ verificationLevel: 'standard ' }) } },
      { id: 'tt_fullwidth_STANDARD', claim: 'ＳＴＡＮＤＡＲＤ', h: { authorization: tt({ verificationLevel: 'ＳＴＡＮＤＡＲＤ' }) } },
      { id: 'tt_turkish_SOCIAL', claim: 'SOCİAL', h: { authorization: tt({ verificationLevel: 'SOCİAL' }) } },
      { id: 'tt_zwsp_government', claim: 'government​', h: { authorization: tt({ verificationLevel: 'government​' }) } },
      { id: 'tt_none', claim: 'none', h: { authorization: tt({ verificationLevel: 'none' }) } },
      { id: 'tt_empty_defaults_BASIC', claim: 'BASIC', h: { authorization: tt({ verificationLevel: '' }) } },
      { id: 'tt_Government', claim: 'Government', h: { authorization: tt({ verificationLevel: 'Government', mfaEnabled: true }) } },
      { id: 'tt_BASIC_spoof_hdr_GOV', claim: 'BASIC', h: { authorization: tt({ verificationLevel: 'BASIC' }), 'x-verification-level': 'GOVERNMENT', 'x-user-role': 'admin' } },
    ];
    const ONLY = (process.env.QA_PRINCIPALS || '').split(',').filter(Boolean); // QA-EDIT-FILTER
    if (ONLY.length) P.splice(0, P.length, ...P.filter((x) => ONLY.includes(x.id)));
    out.meta.principals = P.map((p) => ({ id: p.id, claim: p.claim }));
    const codes = catalogue.map((t) => t.code as string).sort();
    const createCodes: Array<string | null> = [null, 'QA_UNREGISTERED', ...codes, 'ssd_document'];
    const bodyKeys = ['documentType', 'type'];
    let n = 0;
    for (const p of P) {
      for (const key of bodyKeys) {
        for (const code of createCodes) {
          if (code === null && key === 'type') continue;
          const rowId = `r${++n}`;
          const b: any = { title: rowId, contentHash: 'a'.repeat(64) };
          if (code !== null) b[key] = code;
          const wfBefore = (await redis.getAllWorkflowInstances()).length;
          const seenBefore = stubSeen.length;
          const t0 = Date.now(); // QA-EDIT-TIMING
          const r = await send(gwUrl, 'POST', '/api/documents', p.h, JSON.stringify(b));
          const ms = Date.now() - t0;
          const fwd = stubSeen.slice(seenBefore).find((s) => s.method === 'POST' && s.url === '/api/documents');
          const wfAfter = (await redis.getAllWorkflowInstances()).length;
          out.rows.push({ principal: p.id, claim: p.claim, key, type: code, status: r.status, code: r.code, forwarded: !!fwd, workflow: wfAfter - wfBefore, pending: r.json?.status === 'pending_approval', ms,
            fwd: fwd ? { xuser: fwd.headers['x-user-id'] ?? null, xtenant: fwd.headers['x-tenant-id'] ?? null, xslug: fwd.headers['x-tenant-slug'] ?? null, xorg: fwd.headers['x-organization-id'] ?? null, xlevel: fwd.headers['x-verification-level'] ?? null, authz: fwd.headers['authorization'] ? (minted.some((t) => fwd.headers['authorization'] === `Bearer ${t}`) ? 'minted-connector-jwt' : 'caller-bearer') : null } : null,
            resp_contains_minted: minted.some((t) => r.text.includes(t) || JSON.stringify(r.headers).includes(t)) });
        }
      }
      // --- verify route rows ---
      for (const code of codes) {
        const t1 = Date.now();
        const r = await send(gwUrl, 'POST', `/api/documents/vdoc-${encodeURIComponent(code)}/verify`, p.h, JSON.stringify({}));
        const vms = Date.now() - t1;
        out.verify.push({ principal: p.id, claim: p.claim, type: code, status: r.status, code: r.code, requiredLevel: r.json?.requiredLevel ?? null, currentLevel: r.json?.currentLevel ?? null, ms: vms, resp_contains_minted: minted.some((t) => r.text.includes(t)) });
      }
    }
    // drift guard: the first principal rows re-run at the end must answer the same
    const again = await send(gwUrl, 'POST', '/api/documents', { authorization: P.find((x) => x.id === 'jwt_BASIC')!.h.authorization }, JSON.stringify({ title: 'drift', documentType: 'SSD_DOCUMENT' }));
    out.meta.drift_jwt_BASIC_SSD = again.status;
    expect(again.status, 'drift guard: a BASIC human still creates SSD_DOCUMENT at the end of the census').toBe(201);

    // --- tenant scoping: spoofed inbound x-tenant-id / x-tenant-slug ---
    const spoof = { 'x-tenant-id': 't-EVIL', 'x-tenant-slug': 'evil' };
    for (const p of [...P.filter((x) => ['sk_write', 'jwt_connector_scoped', 'jwt_connector_noscope', 'jwt_NONE', 'tt_api_key'].includes(x.id)), { id: 'sk_notenant', claim: 'api_key', h: { 'x-api-key': 'sk_qa_notenant_001' } }]) {
      for (const code of [null, 'SSD_DOCUMENT']) {
        const seenBefore = stubSeen.length;
        const b: any = { title: `ten-${p.id}-${code}` }; if (code) b.documentType = code;
        const r = await send(gwUrl, 'POST', '/api/documents', { ...p.h, ...spoof }, JSON.stringify(b));
        const fwd = stubSeen.slice(seenBefore).find((s) => s.method === 'POST' && s.url === '/api/documents');
        out.tenant.push({ principal: p.id, type: code, status: r.status, code: r.code, forwarded: !!fwd, xtenant: fwd?.headers['x-tenant-id'] ?? null, xslug: fwd?.headers['x-tenant-slug'] ?? null, xuser: fwd?.headers['x-user-id'] ?? null });
      }
    }

    // --- rate limit on the REAL app: rateLimit 2/60s key, 5 creates of SSD_DOCUMENT ---
    const rl: any[] = [];
    for (let i = 0; i < 5; i++) {
      const r = await send(gwUrl, 'POST', '/api/documents', { 'x-api-key': 'sk_qa_ratelimit_01' }, JSON.stringify({ title: `rl${i}`, documentType: 'SSD_DOCUMENT' }));
      rl.push({ i, status: r.status, code: r.code, xrl_limit: r.headers['x-ratelimit-limit'] ?? null, xrl_remaining: r.headers['x-ratelimit-remaining'] ?? null, ratelimit_std: r.headers['ratelimit-limit'] ?? null });
    }
    out.ratelimit.real_app = rl;
    // positive control: the SAME limiter mounted AFTER the SAME authenticateToken on a bare express app
    const ctl = express();
    ctl.post('/c', auth.authenticateToken(true), rle.enforceClientRateLimit(), (_q: any, s: any) => s.status(200).json({ ok: true }));
    const cs = http.createServer(ctl); const cu = await listen(cs);
    const rc: any[] = [];
    for (let i = 0; i < 5; i++) { const r = await send(cu, 'POST', '/c', { 'x-api-key': 'sk_qa_ratelimit_02' }, '{}'); rc.push({ i, status: r.status, code: r.code, xrl_limit: r.headers['x-ratelimit-limit'] ?? null }); }
    await new Promise<void>((r) => cs.close(() => r()));
    out.ratelimit.control_after_auth = rc;

    // --- reachability of minted connector JWTs in any client-visible response ---
    out.reach = { minted: minted.length, create_rows_resp_contains_minted: out.rows.filter((x: any) => x.resp_contains_minted).length, verify_rows_resp_contains_minted: out.verify.filter((x: any) => x.resp_contains_minted).length };

    // --- pure function universe (item 2) ---
    const U: any[] = [];
    for (const l of ['none', 'basic', 'social', 'standard', 'enhanced', 'high', 'government']) U.push(l, l.toUpperCase(), l[0].toUpperCase() + l.slice(1));
    U.push('', ' ', 'none ', ' standard', 'standard​', 'standard ', 'ＳＴＡＮＤＡＲＤ', 'SOCİAL', 'api_key', 'API_KEY', 'oauth_app', 'FULL', 'kyc-pending', 'standrd', 'constructor', '__proto__', null, undefined);
    const UserExtra: any[] = [0, false, 7, ['standard'], {}];
    for (const u of [...U, ...UserExtra]) for (const q of U) {
      let res: any;
      try { res = enforcement.meetsVerificationLevel(u, q); } catch (e: any) { res = `throw:${e?.constructor?.name}`; }
      out.pure.push({ u: u === undefined ? '<undefined>' : u, q: q === undefined ? '<undefined>' : q, res });
    }
    out.meta.order = enforcement.VERIFICATION_LEVEL_ORDER;
    // --- admin create id collision probe (after the census; QA-EDIT-COLLIDE) ---
    const nBefore = (await redis.getAllDocumentTypes()).length;
    const ca = await send(gwUrl, 'POST', '/api/admin/document-types', { authorization: `Bearer ${admin}` }, JSON.stringify({ name: 'QA_COLLIDE_A', code: 'QA_COLLIDE_A', creatorVerificationLevel: 'none' }));
    const cb = await send(gwUrl, 'POST', '/api/admin/document-types', { authorization: `Bearer ${admin}` }, JSON.stringify({ name: 'QA_COLLIDE_B', code: 'QA_COLLIDE_B', creatorVerificationLevel: 'none' }));
    const after = (await redis.getAllDocumentTypes()) as any[];
    out.admin_probe = { a_status: ca.status, b_status: cb.status, a_id: ca.json?.id, b_id: cb.json?.id, same_id: ca.json?.id === cb.json?.id, added: after.length - nBefore, codes_present: after.filter((t) => String(t.code).startsWith('QA_COLLIDE')).map((t) => t.code) };
    if (OUT) fs.writeFileSync(OUT, JSON.stringify(out, null, 1));
    expect(out.rows.length, 'rows produced').toBeGreaterThan(1000);
  }, 1500000);
});
