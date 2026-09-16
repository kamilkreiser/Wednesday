// qa1014-drafter-principals.test.ts — DRAFTER PROBE for the #1014 (KS-1176) tier-1 gate set. NOT a product test; copied into the drafter's own
// clone only (base / head / merged), never into the Secuura checkout. Records rows; asserts nothing about the verdict (the Python comparer does).
//
// Real: authenticateToken (sk_ path, Bearer RS256 path, test-token path), createVerificationRoutes (POST /api/documents and
// POST /api/documents/:id/verify), enforceDocumentTypeRules, createWorkflowInstanceIfRequired, meetsVerificationLevel, SEED_DOCUMENT_TYPES.
// Stubbed: ../services/redis (catalogue + workflow store, in memory), one loopback service standing in for security (/api/keys/validate),
// auth (/internal/connector-token), originate (GET + POST /api/documents) and anchoring (404s). Throwaway RSA key generated per run.
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import express from 'express';
import http from 'node:http';
import crypto from 'node:crypto';
import fs from 'node:fs';
import type { AddressInfo } from 'node:net';
import jwt from 'jsonwebtoken';

const store = vi.hoisted(() => ({ types: [] as Array<Record<string, unknown>>, wfi: [] as unknown[], pending: [] as unknown[] }));
vi.mock('../services/redis', () => ({
  getAllDocumentTypes: vi.fn(async () => store.types),
  getWorkflow: vi.fn(async () => ({ id: 'wf-qa', name: 'QA wf', steps: [{ name: 's1' }] })),
  setWorkflowInstance: vi.fn(async (_id: string, i: unknown) => { store.wfi.push(i); }),
  setPendingDocument: vi.fn(async (_id: string, d: unknown) => { store.pending.push(d); }),
  getRedisClient: vi.fn(() => null),
}));

import { meetsVerificationLevel, enforceDocumentTypeRules, createWorkflowInstanceIfRequired } from '../services/enforcement';
import { configureAuth, authenticateToken } from '../middleware/auth';
import { SEED_DOCUMENT_TYPES } from '../routes/admin';
import { createVerificationRoutes } from '../routes/verification';

const OUT = process.env.QA1014_OUT || '/dev/null';
const rows: Array<Record<string, unknown>> = [];
const hits: Array<Record<string, unknown>> = [];
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIV = privateKey.export({ type: 'pkcs1', format: 'pem' }).toString();
const PUB = publicKey.export({ type: 'spki', format: 'pem' }).toString();
const sign = (claims: Record<string, unknown>) => jwt.sign(claims, PRIV, { algorithm: 'RS256', expiresIn: 600 });
const connectorJwt = (scopes: string[]) => sign({ userId: 'connector:qa-cjwt', email: 'connector@secuura.io', role: 'connector', organizationId: 'org-qa', verificationLevel: 'api_key', type: 'connector', tenantId: 't-qa', scopes });
const testToken = (p: Record<string, unknown>) => 'test_token_' + Buffer.from(JSON.stringify({ sub: 'qa-tt', role: 'ISSUER', ...p })).toString('base64');

const KEYS: Record<string, Record<string, unknown>> = {
  sk_qa_write_0000000: { valid: true, connectorId: 'qa-c-write', scopes: ['documents:write'], organizationId: 'org-qa', tenantId: 't-qa' },
  sk_qa_noscope_00000: { valid: true, connectorId: 'qa-c-noscope', scopes: [], organizationId: 'org-qa', tenantId: 't-qa' },
  sk_qa_restricted_00: { valid: true, connectorId: 'qa-c-restricted', scopes: ['documents:write'], organizationId: 'org-qa', tenantId: 't-qa' },
  sk_qa_bypass_000000: { valid: true, connectorId: 'qa-c-bypass', scopes: ['documents:write'], organizationId: 'org-qa', tenantId: 't-qa' },
};

const base = { isActive: true, requireMFA: false, allowedAuthProviders: [], metadataSchema: [], requiresApproval: false, approvalWorkflowId: null };
const SYNTH = [
  { id: 'qa-1', code: 'QA_NONE_UPPER', name: 'QA none upper', creatorVerificationLevel: 'NONE', verifierVerificationLevel: 'NONE' },
  { id: 'qa-2', code: 'QA_NONE_EMPTY', name: 'QA none empty', creatorVerificationLevel: '', verifierVerificationLevel: '' },
  { id: 'qa-3', code: 'QA_NONE_ABSENT', name: 'QA none absent' },
  { id: 'qa-4', code: 'QA_NONE_SPACE', name: 'QA none space', creatorVerificationLevel: ' none', verifierVerificationLevel: ' none' },
  { id: 'qa-5', code: 'QA_TYPO', name: 'QA typo', creatorVerificationLevel: 'standrd', verifierVerificationLevel: 'standrd' },
  { id: 'qa-6', code: 'QA_BASIC', name: 'QA basic', creatorVerificationLevel: 'basic', verifierVerificationLevel: 'basic' },
  { id: 'qa-7', code: 'QA_GOV', name: 'QA gov', creatorVerificationLevel: 'government', verifierVerificationLevel: 'government' },
  { id: 'qa-8', code: 'QA_NONE_MFA', name: 'QA none mfa', creatorVerificationLevel: 'none', verifierVerificationLevel: 'none', requireMFA: true },
  { id: 'qa-9', code: 'QA_NONE_PROVIDER', name: 'QA none provider', creatorVerificationLevel: 'none', verifierVerificationLevel: 'none', allowedAuthProviders: ['google'] },
  { id: 'qa-10', code: 'QA_NONE_APPROVAL', name: 'QA none approval', creatorVerificationLevel: 'none', verifierVerificationLevel: 'none', requiresApproval: true, approvalWorkflowId: 'wf-qa' },
].map((t) => ({ ...base, ...t }));

const PRINCIPALS: Record<string, Record<string, string>> = {
  anon: {},
  sk_write: { 'x-api-key': 'sk_qa_write_0000000' },
  sk_noscope: { 'x-api-key': 'sk_qa_noscope_00000' },
  sk_restricted_to_DOCUMENT: { 'x-api-key': 'sk_qa_restricted_00' },
  sk_bypass_workflow: { 'x-api-key': 'sk_qa_bypass_000000' },
  sk_invalid: { 'x-api-key': 'sk_qa_unknown_00000' },
  cjwt_bearer_write: { authorization: 'Bearer ' + connectorJwt(['documents:write']) },
  cjwt_bearer_noscope: { authorization: 'Bearer ' + connectorJwt([]) },
  jwt_NONE: { authorization: 'Bearer ' + sign({ userId: 'u-none', email: 'n@qa', role: 'ISSUER', verificationLevel: 'NONE', tenantId: 't-qa' }) },
  jwt_BASIC: { authorization: 'Bearer ' + sign({ userId: 'u-basic', email: 'b@qa', role: 'ISSUER', verificationLevel: 'BASIC', tenantId: 't-qa' }) },
  jwt_STANDARD_mfa: { authorization: 'Bearer ' + sign({ userId: 'u-std', email: 's@qa', role: 'ISSUER', verificationLevel: 'STANDARD', mfaEnabled: true, tenantId: 't-qa' }) },
  jwt_GOVERNMENT_mfa: { authorization: 'Bearer ' + sign({ userId: 'u-gov', email: 'g@qa', role: 'ISSUER', verificationLevel: 'GOVERNMENT', mfaEnabled: true, tenantId: 't-qa' }) },
  jwt_no_level_claim: { authorization: 'Bearer ' + sign({ userId: 'u-nolevel', email: 'x@qa', role: 'ISSUER', tenantId: 't-qa' }) },
  tt_api_key: { authorization: 'Bearer ' + testToken({ verificationLevel: 'api_key', authMethod: 'api_key' }) },
  tt_API_KEY: { authorization: 'Bearer ' + testToken({ verificationLevel: 'API_KEY' }) },
  tt_oauth_app: { authorization: 'Bearer ' + testToken({ verificationLevel: 'oauth_app', authMethod: 'oauth_app' }) },
  tt_FULL: { authorization: 'Bearer ' + testToken({ verificationLevel: 'FULL' }) },
  tt_kyc_pending: { authorization: 'Bearer ' + testToken({ verificationLevel: 'kyc-pending' }) },
  tt_space_standard: { authorization: 'Bearer ' + testToken({ verificationLevel: ' standard' }) },
  tt_standard_space: { authorization: 'Bearer ' + testToken({ verificationLevel: 'standard ' }) },
  tt_fullwidth_STANDARD: { authorization: 'Bearer ' + testToken({ verificationLevel: 'ＳＴＡＮＤＡＲＤ' }) },
  tt_turkish_SOCIAL: { authorization: 'Bearer ' + testToken({ verificationLevel: 'SOCİAL' }) },
  tt_none: { authorization: 'Bearer ' + testToken({ verificationLevel: 'none' }) },
  tt_empty_defaults_BASIC: { authorization: 'Bearer ' + testToken({ verificationLevel: '' }) },
  tt_Government_mixed: { authorization: 'Bearer ' + testToken({ verificationLevel: 'Government', mfaEnabled: true }) },
  tt_BASIC_spoof_header_GOVERNMENT: { authorization: 'Bearer ' + testToken({ verificationLevel: 'BASIC' }), 'x-verification-level': 'GOVERNMENT' },
};

let svc: http.Server; let gw: http.Server; let svcUrl = ''; let gwPort = 0;
const realFetch = globalThis.fetch;

beforeAll(async () => {
  process.env.JWT_PUBLIC_KEY = Buffer.from(PUB).toString('base64');
  delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL; delete process.env.JWT_ACCEPTED_ALGS;
  store.types = [...(SEED_DOCUMENT_TYPES as Array<Record<string, unknown>>), ...SYNTH];
  svc = http.createServer((req, res) => {
    let b = ''; req.on('data', (c) => { b += c; });
    req.on('end', () => {
      const j = (s: number, o: unknown) => { res.writeHead(s, { 'Content-Type': 'application/json' }); res.end(JSON.stringify(o)); };
      const url = req.url || '';
      if (req.method === 'POST' && url === '/api/keys/validate') { const k = JSON.parse(b || '{}').key; return j(200, { data: KEYS[k] || { valid: false } }); }
      if (req.method === 'POST' && url === '/internal/connector-token') { const k = JSON.parse(b || '{}').apiKey; const m = KEYS[k]; if (!m) return j(401, {}); return j(200, { data: { token: sign({ userId: 'connector:' + m.connectorId, email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector', scopes: m.scopes }), expiresIn: 600 } }); }
      if (req.method === 'POST' && url === '/api/documents') { let parsed: unknown = null; try { parsed = JSON.parse(b); } catch { parsed = b; } hits.push({ method: 'POST', url, xUserId: req.headers['x-user-id'], xVerificationLevel: req.headers['x-verification-level'] ?? null, xTenantId: req.headers['x-tenant-id'] ?? null, authorization: req.headers.authorization ? 'present' : 'absent', bodyKeys: parsed && typeof parsed === 'object' ? Object.keys(parsed as object).sort() : [] }); return j(201, { success: true, data: { id: 'qa-created' } }); }
      const m = url.match(/^\/api\/documents\/doc-([A-Z_]+)$/);
      if (req.method === 'GET' && m) return j(200, { id: 'doc-' + m[1], status: 'anchored', contentHash: 'c'.repeat(64), documentType: m[1], owner: { id: 'org-qa' } });
      return j(404, {});
    });
  });
  svc.listen(0, '127.0.0.1'); await new Promise<void>((r) => svc.once('listening', () => r()));
  svcUrl = 'http://127.0.0.1:' + (svc.address() as AddressInfo).port;
  process.env.ANCHORING_SERVICE_URL = svcUrl;
  configureAuth({ enableTestTokens: true, securityServiceUrl: svcUrl, authServiceUrl: svcUrl });
  const app = express();
  app.use(createVerificationRoutes({
    authenticateToken, mockBodyParser: express.json({ limit: '1mb' }), query: (async () => ({ rows: [] })) as never, isDbAvailable: () => false,
    redisService: {
      getPendingDocument: async () => null, deletePendingDocument: async () => undefined, getAllDocumentTypes: async () => store.types,
      getAllWorkflowInstances: async () => [], getRejectedDocument: async () => null, setRejectedDocument: async () => undefined,
      getWorkflowDocumentMapping: async () => null, getWorkflowInstance: async () => null, setWorkflowInstance: async () => undefined,
      getNotificationSettings: async () => ({ integrations: [{ id: 'qa-c-restricted', config: { allowedDocumentTypes: ['DOCUMENT'] } }, { id: 'qa-c-bypass', config: { workflowPolicy: 'bypass' } }] }),
    } as never,
    services: { originate: { url: svcUrl }, anchoring: { url: svcUrl } } as never,
    log: () => undefined, memWorkflowToDocumentMap: new Map(), memRejectedDocuments: new Map(), dbSaveRejection: async () => undefined,
    ADMIN_ROLES: ['ADMIN', 'admin'], enforceDocumentTypeRules, createWorkflowInstanceIfRequired, meetsVerificationLevel,
  }));
  gw = app.listen(0, '127.0.0.1'); await new Promise<void>((r) => gw.once('listening', () => r()));
  gwPort = (gw.address() as AddressInfo).port;
});

afterAll(async () => {
  await new Promise<void>((r) => gw.close(() => r())); await new Promise<void>((r) => svc.close(() => r()));
  fs.writeFileSync(OUT, JSON.stringify({ node: process.version, nodeEnv: process.env.NODE_ENV, rows, hits }, null, 1));
});

describe('qa1014 drafter probe', () => {
  it('pure function: meetsVerificationLevel over a level universe x itself', () => {
    const K = ['none', 'basic', 'social', 'standard', 'enhanced', 'high', 'government'];
    const U = ['', ...K, ...K.map((k) => k.toUpperCase()), 'Standard', ' none', 'none ', ' standard', 'standard ', 'standrd', 'kyc', 'api_key', 'API_KEY', 'oauth_app', 'FULL', 'kyc-pending', 'null', 'undefined', 'ＳＴＡＮＤＡＲＤ', 'SOCİAL', 'gov​ernment', 'NONE '];
    for (const u of U) for (const r of U) rows.push({ kind: 'fn', user: u, required: r, result: meetsVerificationLevel(u, r) });
    for (const [label, v] of [['undefined', undefined], ['null', null], ['number0', 0], ['number3', 3], ['array', ['standard']], ['object', {}]] as Array<[string, unknown]>) {
      for (const r of ['none', 'standard', 'standrd']) {
        let result: unknown; try { result = meetsVerificationLevel(v as string, r); } catch (e) { result = 'THROW ' + (e as Error).name; }
        rows.push({ kind: 'fn-nonstring', user: label, required: r, result });
      }
    }
    expect(rows.length).toBeGreaterThan(900);
  });

  it('HTTP: POST /api/documents and POST /api/documents/:id/verify per principal x document type', async () => {
    const codes = [null, 'QA_UNREGISTERED', ...store.types.map((t) => t.code as string)];
    for (const [pname, headers] of Object.entries(PRINCIPALS)) {
      for (const code of codes) {
        const before = hits.length; const wfBefore = store.wfi.length;
        const body: Record<string, unknown> = { title: 'qa1014', contentHash: 'c'.repeat(64), metadata: {} };
        if (code) body.documentType = code;
        const r = await realFetch(`http://127.0.0.1:${gwPort}/api/documents`, { method: 'POST', headers: { 'content-type': 'application/json', ...headers }, body: JSON.stringify(body) });
        const t = await r.text(); let j: any = null; try { j = JSON.parse(t); } catch { j = null; }
        rows.push({ kind: 'create', principal: pname, type: code, status: r.status, code: j?.error?.code ?? j?.code ?? null, forwarded: hits.length - before, forwardedHit: hits.length > before ? hits[hits.length - 1] : null, workflowInstances: store.wfi.length - wfBefore });
      }
      for (const t of store.types) {
        const r = await realFetch(`http://127.0.0.1:${gwPort}/api/documents/doc-${t.code}/verify`, { method: 'POST', headers: { 'content-type': 'application/json', ...headers }, body: JSON.stringify({ purpose: 'qa' }) });
        const txt = await r.text(); let j: any = null; try { j = JSON.parse(txt); } catch { j = null; }
        rows.push({ kind: 'verify', principal: pname, type: t.code, verifierLevel: (t as any).verifierVerificationLevel ?? '(absent)', status: r.status, code: j?.code ?? j?.error?.code ?? null, requiredLevel: j?.requiredLevel ?? null, currentLevel: j?.currentLevel ?? null });
      }
    }
    expect(rows.filter((x) => x.kind === 'create').length).toBe(Object.keys(PRINCIPALS).length * codes.length);
  }, 120_000);
});
