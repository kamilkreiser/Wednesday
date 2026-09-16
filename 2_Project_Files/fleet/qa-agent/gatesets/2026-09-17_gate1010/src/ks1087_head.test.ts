// KS-1087 — workflow approve must keep the pending doc when originate fails
// KS-1183 — ...and the forward to originate must answer within a bound
//
// Every cell builds its own gateway on a STATEFUL Redis stub (the instance and the
// pending documents live in `store`), so a cell reads what the route actually left
// behind rather than a canned answer. One originate stub serves every cell; each cell
// sets how it behaves.
import { describe, it, expect, beforeAll, afterAll, afterEach, vi } from 'vitest';
import express from 'express';
import http from 'node:http';
import type { AddressInfo } from 'node:net';
import type { IncomingMessage, ServerResponse } from 'node:http';
import type { RequestHandler } from 'express';
// A namespace import, so an export missing from the module reads as undefined in a cell
// instead of failing the whole file at load.
import * as verification from '../routes/verification';

const DOC_ID = 'doc-ks1087';
const WFI_ID = 'wfi-ks1087';
/** The forward bound these cells run the route with (the production default is ORIGINATE_FORWARD_TIMEOUT_MS). */
const FORWARD_TIMEOUT_MS = 1_000;
/** How long a cell's client waits before it records NO RESPONSE. */
const CLIENT_WAIT_MS = 5_000;
const ORIGINATE_BODY_MARKER = 'ORIGINATE-BODY-MARKER-ks1183';

type Behaviour = (req: IncomingMessage, res: ServerResponse) => void;

interface Store {
  instance: Record<string, unknown>;
  pendingDocs: Map<string, Record<string, unknown>>;
  deletes: number;
}

function freshStore(): Store {
  return {
    instance: { status: 'pending_approval', documentId: DOC_ID, steps: [{ name: 'Approve' }], currentStepIndex: 0 },
    pendingDocs: new Map([[DOC_ID, { title: 't', contentHash: 'h', createdBy: 'u' }]]),
    deletes: 0,
  };
}

let originate: http.Server | undefined;
let originatePort = 0;
let originateHits = 0;
let behave: Behaviour = (_req, res) => res.end();

beforeAll(async () => {
  const server = http.createServer((req, res) => {
    originateHits++;
    req.resume();
    behave(req, res);
  });
  server.listen(0, '127.0.0.1');
  await new Promise<void>((r) => server.once('listening', () => r()));
  originatePort = (server.address() as AddressInfo).port;
  originate = server;
});

afterAll(async () => {
  const server = originate;
  if (!server) return;
  server.closeAllConnections();
  await new Promise<void>((r) => server.close(() => r()));
});

const openGateways: Array<ReturnType<ReturnType<typeof express>['listen']>> = [];

afterEach(async () => {
  for (const server of openGateways.splice(0)) {
    server.closeAllConnections();
    await new Promise<void>((r) => server.close(() => r()));
  }
});

type Log = (level: 'info' | 'warn' | 'error', message: string, meta?: object) => void;

async function startGateway(
  store: Store,
  originateUrl = `http://127.0.0.1:${originatePort}`,
  log: Log = () => undefined,
): Promise<number> {
  const mockBodyParser: RequestHandler = express.json({ limit: '1mb' });
  const app = express();
  app.use(
    verification.createVerificationRoutes({
      authenticateToken: () => (_req, _res, next) => next(),
      mockBodyParser,
      query: vi.fn(async () => ({ rows: [] })) as never,
      isDbAvailable: () => false,
      redisService: {
        getWorkflowInstance: vi.fn(async (id: string) => (id === WFI_ID ? structuredClone(store.instance) : null)),
        getAllWorkflowInstances: vi.fn(async () => [structuredClone(store.instance)]),
        setWorkflowInstance: vi.fn(async (id: string, value: Record<string, unknown>) => {
          if (id === WFI_ID) store.instance = structuredClone(value);
        }),
        getPendingDocument: vi.fn(async (id: string) => store.pendingDocs.get(id) ?? null),
        deletePendingDocument: vi.fn(async (id: string) => {
          store.deletes++;
          store.pendingDocs.delete(id);
        }),
      } as never,
      services: { originate: { url: originateUrl }, anchoring: { url: '' } } as never,
      log,
      memWorkflowToDocumentMap: new Map(),
      memRejectedDocuments: new Map(),
      dbSaveRejection: vi.fn(async () => undefined),
      ADMIN_ROLES: ['ADMIN'],
      enforceDocumentTypeRules: vi.fn(async () => ({ ok: true, docType: {} })) as never,
      createWorkflowInstanceIfRequired: vi.fn(async () => ({ gated: false })) as never,
      meetsVerificationLevel: () => true,
      originateForwardTimeoutMs: FORWARD_TIMEOUT_MS,
    }),
  );
  const server = app.listen(0, '127.0.0.1');
  openGateways.push(server);
  await new Promise<void>((r) => server.once('listening', () => r()));
  return (server.address() as AddressInfo).port;
}

interface Outcome {
  status: number | 'NO RESPONSE';
  text: string;
  ms: number;
}

async function approve(gatewayPort: number): Promise<Outcome> {
  const started = Date.now();
  try {
    const res = await fetch(`http://127.0.0.1:${gatewayPort}/api/workflow-instances/${WFI_ID}/approve`, {
      method: 'POST',
      signal: AbortSignal.timeout(CLIENT_WAIT_MS),
    });
    return { status: res.status, text: await res.text(), ms: Date.now() - started };
  } catch {
    return { status: 'NO RESPONSE', text: '', ms: Date.now() - started };
  }
}

const answer = (status: number, body: string = JSON.stringify({ id: DOC_ID })): Behaviour => (_req, res) => {
  res.writeHead(status, { 'Content-Type': 'application/json' });
  res.end(body);
};

const sleep = (ms: number) => new Promise<void>((r) => setTimeout(r, ms));

function forwardError(text: string): unknown {
  return (JSON.parse(text) as { error?: unknown }).error;
}

describe('KS-1087 — workflow approve keeps pending doc on originate failure', () => {
  it('🔴 KS-1087 — originate 401: no 200 approved, and the pending document survives', async () => {
    behave = answer(401);
    const store = freshStore();
    const out = await approve(await startGateway(store));
    expect(out.status).not.toBe(200);
    expect(out.status).toBe(502);
    expect(forwardError(out.text)).toMatchObject({ code: 'ORIGINATE_FORWARD_FAILED', status: 401 });
    expect(store.deletes, 'the pending document survives a refused forward').toBe(0);
    expect(store.pendingDocs.has(DOC_ID), 'the pending document is still in the store').toBe(true);
  });

  it('🔴 KS-1087 — originate unreachable: the pending document survives', async () => {
    // A closed port, so http.request errors out immediately.
    const store = freshStore();
    const out = await approve(await startGateway(store, 'http://127.0.0.1:1'));
    expect(out.status).not.toBe(200);
    expect(out.status).toBe(502);
    expect(forwardError(out.text)).toMatchObject({ code: 'ORIGINATE_FORWARD_FAILED', status: 0 });
    expect(store.deletes).toBe(0);
    expect(store.pendingDocs.has(DOC_ID)).toBe(true);
  });

  it('KS-1087 control — originate 201: approved and the pending document is deleted', async () => {
    behave = answer(201);
    const store = freshStore();
    const out = await approve(await startGateway(store));
    expect(out.status).toBe(200);
    expect(store.deletes, 'the pending document is deleted once originate accepts').toBe(1);
    const body = JSON.parse(out.text) as { success?: unknown; message?: unknown };
    expect(body.success).toBe(true);
    expect(String(body.message)).toContain('created');
  });
});

describe('KS-1183 — the forward to originate answers within a bound', () => {
  it('🔴 KS-1183 — originate accepts and never answers: 502 at the bound, the pending document kept', { timeout: 15_000 }, async () => {
    behave = () => undefined; // hold the request open, never write a byte
    const store = freshStore();
    const hitsBefore = originateHits;
    const out = await approve(await startGateway(store));
    expect(out.status, `answered after ${out.ms} ms`).toBe(502);
    expect(forwardError(out.text)).toMatchObject({ code: 'ORIGINATE_FORWARD_FAILED', status: 0 });
    expect(out.ms, 'the route answers at the forward bound, not after the client gives up').toBeLessThan(FORWARD_TIMEOUT_MS + 1_500);
    expect(originateHits - hitsBefore).toBe(1);
    expect(store.deletes).toBe(0);
    expect(store.pendingDocs.has(DOC_ID)).toBe(true);
  });

  it('🔴 KS-1183 — originate answers 201 after the bound: the caller got 502, and the late 201 deletes nothing', { timeout: 15_000 }, async () => {
    const lateMs = FORWARD_TIMEOUT_MS + 1_500;
    behave = (_req, res) => {
      setTimeout(() => {
        if (res.destroyed || res.socket?.destroyed) return;
        res.writeHead(201, { 'Content-Type': 'application/json' });
        res.end(JSON.stringify({ id: DOC_ID }));
      }, lateMs);
    };
    const store = freshStore();
    const out = await approve(await startGateway(store));
    expect(out.status, `answered after ${out.ms} ms`).toBe(502);
    expect(forwardError(out.text)).toMatchObject({ code: 'ORIGINATE_FORWARD_FAILED', status: 0 });
    // Let originate's late answer come and go before reading the store.
    await sleep(Math.max(0, lateMs + 500 - out.ms));
    expect(store.deletes, 'nothing is deleted after the caller was told the forward failed').toBe(0);
    expect(store.pendingDocs.has(DOC_ID)).toBe(true);
  });

  it('KS-1183 — a forward that completed is not failed later by the bound (no forward error logged)', { timeout: 15_000 }, async () => {
    behave = answer(201);
    const store = freshStore();
    const log = vi.fn<Log>();
    const out = await approve(await startGateway(store, undefined, log));
    expect(out.status).toBe(200);
    expect(store.deletes).toBe(1);
    await sleep(FORWARD_TIMEOUT_MS + 500);
    const errors = log.mock.calls.filter(([level]) => level === 'error');
    expect(errors, 'no forward error after a completed 201').toEqual([]);
    expect(log.mock.calls.map(([, message]) => message)).toContain('Workflow approved — document forwarded to originate');
  });

  it('KS-1183 — originate 302: a redirect is not a created document (502, kept)', async () => {
    behave = answer(302);
    const store = freshStore();
    const out = await approve(await startGateway(store));
    expect(out.status).toBe(502);
    expect(forwardError(out.text)).toMatchObject({ code: 'ORIGINATE_FORWARD_FAILED', status: 302 });
    expect(store.deletes).toBe(0);
  });

  it('KS-1183 — 201 headers, body never ends: approved on the status line, before the bound', { timeout: 15_000 }, async () => {
    // originate persists before it writes a 2xx (services/originate/src/routes/documents.ts
    // saveDocument, then the single res.status(201).json), so the status line is enough.
    behave = (_req, res) => {
      res.writeHead(201, { 'Content-Type': 'application/json' });
      res.write('{"id":');
    };
    const store = freshStore();
    const out = await approve(await startGateway(store));
    expect(out.status, `answered after ${out.ms} ms`).toBe(200);
    expect(out.ms).toBeLessThan(FORWARD_TIMEOUT_MS);
    expect(store.deletes).toBe(1);
  });

  it('KS-1183 — 201 headers, connection reset mid-body: approved on the status line', { timeout: 15_000 }, async () => {
    behave = (_req, res) => {
      res.writeHead(201, { 'Content-Type': 'application/json' });
      res.write('{"id":');
      setTimeout(() => res.socket?.destroy(), 50);
    };
    const store = freshStore();
    const out = await approve(await startGateway(store));
    expect(out.status, `answered after ${out.ms} ms`).toBe(200);
    expect(out.ms).toBeLessThan(FORWARD_TIMEOUT_MS);
    expect(store.deletes).toBe(1);
  });

  it('KS-1183 — the 502 body is the fixed shape and never carries originate\'s body', async () => {
    behave = answer(401, JSON.stringify({ error: ORIGINATE_BODY_MARKER, path: '/api/documents' }));
    const store = freshStore();
    const out = await approve(await startGateway(store));
    expect(out.status).toBe(502);
    expect(out.text).not.toContain(ORIGINATE_BODY_MARKER);
    const body = JSON.parse(out.text) as { success?: unknown; error?: Record<string, unknown> };
    expect(Object.keys(body).sort()).toEqual(['error', 'success']);
    expect(body.success).toBe(false);
    expect(Object.keys(body.error ?? {}).sort()).toEqual(['code', 'message', 'status']);
  });

  it('🔴 KS-1183 — the default bound answers before the tightest proxy in front of the gateway gives up', () => {
    // nginx-production.conf sets proxy_read_timeout 30s (nginx-demo.conf 60s, nginx.conf 120s).
    const bound = (verification as Record<string, unknown>).ORIGINATE_FORWARD_TIMEOUT_MS;
    expect(typeof bound).toBe('number');
    expect(bound as number).toBeGreaterThan(0);
    expect(bound as number).toBeLessThan(30_000);
  });
});
