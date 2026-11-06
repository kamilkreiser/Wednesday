// Gate 210 Q3. Records, does not assert: same seam as the seat's harness (getNotificationSettings is the only double on
// storage; enforcement + workflow spies stand past the guard), real createHealthRoutes + real createVerificationRoutes.
import { describe, it, beforeAll, afterAll, vi } from 'vitest';
import express from 'express';
import http from 'node:http';
import fs from 'node:fs';
import type { Server } from 'node:http';
import type { AddressInfo } from 'node:net';
import type { Request, Response, Router, RequestHandler } from 'express';
import { apiKeyCache, connectorBearerCache } from '../middleware/auth';

const CONNECTOR_ID = 'g210-c1';
const API_KEY = 'sk_g210';
const META = { connectorId: CONNECTOR_ID, scopes: ['documents:write'], organizationId: 'org-1', tenantId: 'ten-1', rateLimit: 100, rateLimitWindow: 60 };
const HOLED: unknown[] = ['SSD_DOCUMENT']; HOLED.length = 2;
const ABSENT = Symbol('absent');
const ROWS: Array<[string, unknown, string]> = [
  ['undefined (key absent)', ABSENT, 'unrestricted'],
  ['undefined (explicit key)', undefined, 'unrestricted'],
  ['null', null, 'unrestricted'],
  ['[]', [], 'unrestricted'],
  ["['SSD_DOCUMENT']", ['SSD_DOCUMENT'], 'strings'],
  ["['SSD_DOCUMENT',1]", ['SSD_DOCUMENT', 1], 'nonstring'],
  ['[1,2]', [1, 2], 'nonstring'],
  ['[null]', [null], 'nonstring'],
  ["['SSD_DOCUMENT',null]", ['SSD_DOCUMENT', null], 'nonstring'],
  ["['SSD_DOCUMENT',{}]", ['SSD_DOCUMENT', {}], 'nonstring'],
  ["['SSD_DOCUMENT',['x']]", ['SSD_DOCUMENT', ['x']], 'nonstring'],
  ['hole after string', HOLED, 'nonstring'],
  ["['SSD_DOCUMENT',undefined]", ['SSD_DOCUMENT', undefined], 'nonstring'],
  ["'' (string)", '', 'nonarray'],
  ["'SSD_DOCUMENT' (string)", 'SSD_DOCUMENT', 'nonarray'],
  ['{} (object)', {}, 'nonarray'],
  ['0', 0, 'nonarray'],
  ['false', false, 'nonarray'],
  // gate's own extras, beyond the commission's 17
  ["EXTRA ['A','SSD_DOCUMENT',1] (third position)", ['A', 'SSD_DOCUMENT', 1], 'nonstring'],
  ["EXTRA [''] (empty-string element)", [''], 'empty-string'],
  ["EXTRA ['SSD_DOCUMENT','']", ['SSD_DOCUMENT', ''], 'empty-string'],
  ['EXTRA true', true, 'nonarray'],
  ["EXTRA [true,'SSD_DOCUMENT']", [true, 'SSD_DOCUMENT'], 'nonstring'],
];

let allowList: unknown = ABSENT;
const storedSettings = () => ({ integrations: [{ id: CONNECTOR_ID, config: allowList === ABSENT ? {} : { allowedDocumentTypes: allowList } }] });
let infoRouter: Router;
async function info() {
  const req = { headers: { 'x-api-key': API_KEY }, method: 'GET', url: '/api/connector/info', get(n: string) { return (this as any).headers[n?.toLowerCase()]; } } as unknown as Request;
  const res: any = { _status: 0, status(c: number) { res._status = c; return res; }, json(b: unknown) { return b; }, setHeader() { return res; } };
  let calls = 0;
  const body = await new Promise<any>((resolve) => {
    res.json = (b: unknown) => { calls += 1; resolve(b); return res; };
    infoRouter(req, res as Response, () => resolve({ fellThrough: true }));
  });
  return { status: (res._status || 200) as number, code: body?.error?.code ?? null, message: body?.error?.message ?? null, echoed: body?.allowedDocumentTypes === undefined ? '(none)' : JSON.stringify(body.allowedDocumentTypes), calls };
}
const enforceSpy = vi.fn(async () => ({ ok: true as const, docType: {} }));
const workflowSpy = vi.fn(async () => ({ gated: true as const, response: { success: true, data: { past: true } } }));
let gateway: Server; let originate: Server; let port: number;
const realFetch = globalThis.fetch;
async function create(field: 'documentType' | 'type' | null, type: string) {
  enforceSpy.mockClear(); workflowSpy.mockClear();
  const payload: Record<string, unknown> = { title: 'g210', contentHash: 'd'.repeat(64) };
  if (field) payload[field] = type;
  const r = await realFetch(`http://127.0.0.1:${port}/api/documents`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: 'Bearer t' }, body: JSON.stringify(payload) });
  const b: any = await r.json();
  return { status: r.status, code: b?.error?.code ?? null, message: b?.error?.message ?? null, enforced: enforceSpy.mock.calls.length, workflowed: workflowSpy.mock.calls.length };
}
beforeAll(async () => {
  apiKeyCache.set(API_KEY, { result: META, expiresAt: Date.now() + 600000 });
  connectorBearerCache.set(API_KEY, { token: 'connector.jwt.token', expiresAt: Date.now() + 600000 });
  const { createHealthRoutes } = await import('../services/health');
  infoRouter = createHealthRoutes({}, { getNotificationSettings: async () => storedSettings(), getRedisClient: () => null } as any);
  originate = http.createServer((_q, s) => { s.writeHead(404); s.end('{}'); });
  originate.listen(0, '127.0.0.1');
  await new Promise<void>((r) => originate.once('listening', () => r()));
  const op = (originate.address() as AddressInfo).port;
  const { createVerificationRoutes } = await import('../routes/verification');
  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });
  const app = express();
  app.use(createVerificationRoutes({
    authenticateToken: () => (req, _res, next) => {
      (req as any).user = { userId: `connector:${CONNECTOR_ID}`, email: 'c@secuura.io', role: 'connector', organizationId: 'org-1', verificationLevel: 'api_key', authMethod: 'api_key', connectorId: CONNECTOR_ID, rateLimit: 100, rateLimitWindow: 60, scopes: ['documents:write'], tenantId: 'ten-1' };
      (req as any).connectorMeta = { ...META };
      next();
    },
    mockBodyParser, query: vi.fn(async () => ({ rows: [] })) as never, isDbAvailable: () => false,
    redisService: {
      isRedisAvailable: () => true, getPendingDocument: vi.fn(async () => null), deletePendingDocument: vi.fn(async () => undefined),
      getAllDocumentTypes: vi.fn(async () => []), getAllWorkflowInstances: vi.fn(async () => []),
      getNotificationSettings: vi.fn(async () => storedSettings()), getRejectedDocument: vi.fn(async () => null), setRejectedDocument: vi.fn(async () => undefined),
      getWorkflowDocumentMapping: vi.fn(async () => null), getWorkflowInstance: vi.fn(async () => null), setWorkflowInstance: vi.fn(async () => undefined),
    } as never,
    services: { originate: { url: `http://127.0.0.1:${op}` }, anchoring: { url: `http://127.0.0.1:${op}` } } as never,
    log: () => undefined, memWorkflowToDocumentMap: new Map(), memRejectedDocuments: new Map(), dbSaveRejection: vi.fn(async () => undefined),
    ADMIN_ROLES: ['ADMIN', 'admin'], enforceDocumentTypeRules: enforceSpy as never, createWorkflowInstanceIfRequired: workflowSpy as never,
  }));
  gateway = app.listen(0, '127.0.0.1');
  await new Promise<void>((r) => gateway.once('listening', () => r()));
  port = (gateway.address() as AddressInfo).port;
});
afterAll(async () => { await new Promise<void>((r) => gateway.close(() => r())); await new Promise<void>((r) => originate.close(() => r())); });
describe('gate 210 table', () => {
  it('records', async () => {
    const out: unknown[] = [];
    for (const [label, value, klass] of ROWS) {
      allowList = value;
      out.push({ label, klass, info: await info(), postNamed: await create('documentType', 'SSD_DOCUMENT'), postOther: await create('documentType', 'INVOICE'), postUntyped: await create(null, ''), postTypeKey: await create('type', 'SSD_DOCUMENT') });
    }
    fs.writeFileSync(process.env.G210_OUT as string, JSON.stringify(out, null, 1));
  }, 60000);
});
