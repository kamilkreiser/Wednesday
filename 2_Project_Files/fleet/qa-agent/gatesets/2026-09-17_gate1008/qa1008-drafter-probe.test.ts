// qa1008-drafter-probe.test.ts — DRAFTER RECORDING HARNESS for the #1008 (KS-1087) gate set. Not a pass/fail test: every cell
// records a row and asserts only that the row was recorded. Copied INTO the drafter's --shared clone (base and head trees), never
// into the Secuura checkout. Loopback 127.0.0.1:0 only. Mounts the REAL createVerificationRoutes with:
//   - a STATEFUL redis stub (Map-backed: setWorkflowInstance persists, getWorkflowInstance returns a copy of what was persisted)
//   - an originate stub on loopback that counts hits (the hit witness) and answers per MODE
// and, for the retry question, the seat's STATELESS stub shape as a comparison.
import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import express from 'express';
import http from 'node:http';
import fs from 'node:fs';
import type { Server } from 'node:http';
import type { AddressInfo } from 'node:net';

const OUT = process.env.PROBE_OUT || '/dev/null';
const rows: Record<string, unknown>[] = [];
const DOC = 'doc-qa1008';
const WFI = 'wfi-qa1008';

let mode: string = '201';
let hits = 0;
let origin: Server;
let originPort = 0;
const originSockets = new Set<import('node:net').Socket>();

beforeAll(async () => {
  origin = http.createServer((req, res) => {
    hits++;
    req.resume();
    const body = JSON.stringify({ id: 'x', internal: 'ORIGINATE-SECRET-BODY-MARKER', path: '/srv/originate/src/routes/documents.ts' });
    if (/^\d{3}$/.test(mode)) {
      req.on('end', () => { res.writeHead(Number(mode), { 'Content-Type': 'application/json' }); res.end(mode === '204' ? undefined : body); });
      return;
    }
    if (mode === 'destroy-before-headers') { req.socket.destroy(); return; }
    if (mode === 'no-response') { return; }
    if (mode === '201-then-destroy-mid-body') { res.writeHead(201, { 'Content-Type': 'application/json', 'Content-Length': '500' }); res.write('{"id":"par'); setTimeout(() => req.socket.destroy(), 50); return; }
    if (mode === '201-body-never-ends') { res.writeHead(201, { 'Content-Type': 'application/json', 'Content-Length': '500' }); res.write('{"id":"par'); return; }
    if (mode === '401-body-never-ends') { res.writeHead(401, { 'Content-Type': 'application/json', 'Content-Length': '500' }); res.write('{"err":"par'); return; }
    res.writeHead(599); res.end();
  });
  origin.on('connection', (s) => { originSockets.add(s); s.on('close', () => originSockets.delete(s)); });
  origin.listen(0, '127.0.0.1');
  await new Promise<void>((r) => origin.once('listening', () => r()));
  originPort = (origin.address() as AddressInfo).port;
});

afterAll(async () => {
  for (const s of originSockets) s.destroy();
  await new Promise<void>((r) => origin.close(() => r()));
  fs.writeFileSync(OUT, JSON.stringify(rows, null, 1));
});

type Harness = { server: Server; port: number; deletes: () => number; instanceStatus: () => unknown; close: () => Promise<void> };

async function harness(opts: { stateful: boolean; originateUrl?: string; steps?: Record<string, unknown>[]; user?: Record<string, unknown>; realAuth?: boolean }): Promise<Harness> {
  const { createVerificationRoutes } = await import('../routes/verification');
  let deletes = 0;
  const pending = new Map<string, Record<string, unknown>>([[DOC, { title: 't', contentHash: 'h', createdBy: 'u' }]]);
  const initial = { status: 'pending_approval', documentId: DOC, steps: opts.steps || [{ name: 'Approve' }], currentStepIndex: 0 };
  const store = new Map<string, string>([[WFI, JSON.stringify(initial)]]);
  let authenticateToken: unknown = () => (req: any, _res: any, next: any) => { if (opts.user) req.user = opts.user; next(); };
  if (opts.realAuth) authenticateToken = (await import('../middleware/auth')).authenticateToken;
  const app = express();
  app.use(
    createVerificationRoutes({
      authenticateToken,
      mockBodyParser: express.json({ limit: '1mb' }),
      query: (async () => ({ rows: [] })) as never,
      isDbAvailable: () => false,
      redisService: {
        getWorkflowInstance: async (id: string) => (opts.stateful ? (store.has(id) ? JSON.parse(store.get(id)!) : null) : id === WFI ? JSON.parse(JSON.stringify(initial)) : null),
        getAllWorkflowInstances: async () => [],
        setWorkflowInstance: async (id: string, v: unknown) => { if (opts.stateful) store.set(id, JSON.stringify(v)); },
        getPendingDocument: async (id: string) => pending.get(id) || null,
        deletePendingDocument: async (id: string) => { deletes++; if (opts.stateful) pending.delete(id); },
      } as never,
      services: { originate: { url: opts.originateUrl || `http://127.0.0.1:${originPort}` }, anchoring: { url: '' } } as never,
      log: () => undefined,
      memWorkflowToDocumentMap: new Map(),
      memRejectedDocuments: new Map(),
      dbSaveRejection: (async () => undefined) as never,
      ADMIN_ROLES: ['ADMIN'],
      enforceDocumentTypeRules: (async () => ({ ok: true, docType: {} })) as never,
      createWorkflowInstanceIfRequired: (async () => ({ gated: false })) as never,
      meetsVerificationLevel: () => true,
    } as never),
  );
  const server = app.listen(0, '127.0.0.1');
  await new Promise<void>((r) => server.once('listening', () => r()));
  return {
    server, port: (server.address() as AddressInfo).port, deletes: () => deletes,
    instanceStatus: () => (store.has(WFI) ? JSON.parse(store.get(WFI)!).status : null),
    close: async () => { server.closeAllConnections(); await new Promise<void>((r) => server.close(() => r())); },
  };
}

async function call(h: Harness, verb: 'approve' | 'reject', waitMs: number) {
  const t0 = Date.now();
  try {
    const r = await fetch(`http://127.0.0.1:${h.port}/api/workflow-instances/${WFI}/${verb}`, { method: 'POST', signal: AbortSignal.timeout(waitMs) });
    const text = await r.text();
    return { status: r.status, body: text.slice(0, 400), ms: Date.now() - t0 };
  } catch (e) {
    return { status: 'NO RESPONSE', body: `${(e as Error).name} after ${Date.now() - t0}ms (client wait ${waitMs}ms)`, ms: Date.now() - t0 };
  }
}

const OUTCOMES = ['200', '201', '204', '302', '400', '401', '403', '404', '409', '422', '500', '503',
  'destroy-before-headers', 'no-response', '201-then-destroy-mid-body', '201-body-never-ends', '401-body-never-ends'];

describe('QA1008 drafter probe — every forward outcome on the real route (stateful stub)', () => {
  for (const m of OUTCOMES) {
    it(`outcome ${m}`, async () => {
      mode = m; const hitsBefore = hits;
      const h = await harness({ stateful: true });
      const r = await call(h, 'approve', 2500);
      await new Promise((x) => setTimeout(x, 300));
      const row = { id: 'O-' + m, originate_mode: m, gateway_status: r.status, ms: r.ms, originate_hits: hits - hitsBefore, deletes: h.deletes(), instance_status_after: h.instanceStatus(), body: r.body,
        body_echoes_originate_body: r.body.includes('ORIGINATE-SECRET-BODY-MARKER'), body_echoes_path: r.body.includes('/srv/originate'), body_names_port: r.body.includes(String(originPort)) };
      rows.push(row);
      for (const s of originSockets) s.destroy();
      await h.close();
      expect(rows.includes(row)).toBe(true);
    }, 15000);
  }
  it('transport error: closed port 127.0.0.1:1', async () => {
    const h = await harness({ stateful: true, originateUrl: 'http://127.0.0.1:1' });
    const r = await call(h, 'approve', 2500);
    const row = { id: 'O-closed-port', gateway_status: r.status, ms: r.ms, deletes: h.deletes(), instance_status_after: h.instanceStatus(), body: r.body };
    rows.push(row); await h.close(); expect(rows.includes(row)).toBe(true);
  }, 15000);
});

describe('QA1008 drafter probe — retry after a refused forward', () => {
  for (const stateful of [true, false]) {
    it(`retry stateful=${stateful}: 401 then originate 201, then reject`, async () => {
      const h = await harness({ stateful });
      mode = '401'; const h0 = hits; const r1 = await call(h, 'approve', 2500); const hits1 = hits - h0; const d1 = h.deletes(); const s1 = h.instanceStatus();
      mode = '201'; const h1 = hits; const r2 = await call(h, 'approve', 2500); const hits2 = hits - h1; const d2 = h.deletes(); const s2 = h.instanceStatus();
      const r3 = await call(h, 'reject', 2500);
      const row = { id: 'R-stateful-' + stateful, first: { status: r1.status, body: r1.body, originate_hits: hits1, deletes: d1, instance_status: s1 },
        second_after_originate_fixed: { status: r2.status, body: r2.body, originate_hits: hits2, deletes_total: d2, instance_status: s2 },
        reject_after: { status: r3.status, body: r3.body }, deletes_final: h.deletes() };
      rows.push(row); await h.close(); expect(rows.includes(row)).toBe(true);
    }, 15000);
  }
});

describe('QA1008 drafter probe — authz before the forward', () => {
  it('403: role step, wrong role', async () => {
    mode = '201'; const h0 = hits;
    const h = await harness({ stateful: true, steps: [{ name: 'Approve', approverType: 'role', approverValue: 'issuer' }], user: { userId: 'u2', role: 'viewer' } });
    const r = await call(h, 'approve', 2500);
    const row = { id: 'A-403-role', gateway_status: r.status, body: r.body, originate_hits: hits - h0, deletes: h.deletes(), instance_status_after: h.instanceStatus() };
    rows.push(row); await h.close(); expect(rows.includes(row)).toBe(true);
  }, 15000);
  it('403: user step, wrong user', async () => {
    mode = '201'; const h0 = hits;
    const h = await harness({ stateful: true, steps: [{ name: 'Approve', approverType: 'user', approverValue: 'u9' }], user: { userId: 'u2', role: 'viewer' } });
    const r = await call(h, 'approve', 2500);
    const row = { id: 'A-403-user', gateway_status: r.status, body: r.body, originate_hits: hits - h0, deletes: h.deletes(), instance_status_after: h.instanceStatus() };
    rows.push(row); await h.close(); expect(rows.includes(row)).toBe(true);
  }, 15000);
  it('401: the REAL authenticateToken, no token', async () => {
    mode = '201'; const h0 = hits;
    let row: Record<string, unknown>;
    try {
      const h = await harness({ stateful: true, realAuth: true });
      const r = await call(h, 'approve', 2500);
      row = { id: 'A-401-real-auth', gateway_status: r.status, body: r.body, originate_hits: hits - h0, deletes: h.deletes(), instance_status_after: h.instanceStatus() };
      await h.close();
    } catch (e) {
      row = { id: 'A-401-real-auth', harness_error: String(e).slice(0, 300) };
    }
    rows.push(row); expect(rows.includes(row)).toBe(true);
  }, 15000);
});
