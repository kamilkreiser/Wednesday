// GATE 201 own probe: base vs head response equivalence on the real route + log-arg marker search.
import { describe, it, expect, beforeAll, afterAll, vi } from 'vitest';
import express from 'express';
import http from 'node:http';
import net from 'node:net';
import fs from 'node:fs';
import type { AddressInfo } from 'node:net';
import * as verification from '../routes/verification';

const DOC = 'doc-g201', WFI = 'wfi-g201', BOUND = 700;
const OUT = process.env.G201_OUT as string;
type Beh = (req: http.IncomingMessage, res: http.ServerResponse) => void;
let beh: Beh = (_q, r) => r.end();
let rawMode: ((s: net.Socket) => void) | null = null;
let srv: http.Server, raw: net.Server, port = 0, rawPort = 0;
beforeAll(async () => {
  srv = http.createServer((q, r) => { q.resume(); beh(q, r); });
  srv.listen(0, '127.0.0.1'); await new Promise<void>((r) => srv.once('listening', () => r()));
  port = (srv.address() as AddressInfo).port;
  raw = net.createServer((s) => { s.on('error', () => {}); s.once('data', () => rawMode?.(s)); });
  raw.listen(0, '127.0.0.1'); await new Promise<void>((r) => raw.once('listening', () => r()));
  rawPort = (raw.address() as AddressInfo).port;
});
afterAll(() => { srv.closeAllConnections(); srv.close(); raw.close(); });

async function run(name: string, url: string) {
  let inst: any = { status: 'pending_approval', documentId: DOC, steps: [{ name: 'A' }], currentStepIndex: 0 };
  const pend = new Map<string, any>([[DOC, { title: 't', contentHash: 'h', createdBy: 'u' }]]);
  let deletes = 0; const logs: any[] = [];
  const app = express();
  app.use(verification.createVerificationRoutes({
    authenticateToken: () => (_q: any, _r: any, n: any) => n(), mockBodyParser: express.json(),
    query: vi.fn(async () => ({ rows: [] })) as never, isDbAvailable: () => false,
    redisService: {
      getWorkflowInstance: async (id: string) => (id === WFI ? structuredClone(inst) : null),
      getAllWorkflowInstances: async () => [structuredClone(inst)],
      setWorkflowInstance: async (_i: string, v: any) => { inst = structuredClone(v); },
      getPendingDocument: async (id: string) => pend.get(id) ?? null,
      deletePendingDocument: async (id: string) => { deletes++; pend.delete(id); },
    } as never,
    services: { originate: { url }, anchoring: { url: '' } } as never,
    log: (l: string, m: string, meta?: object) => { logs.push({ l, m, meta }); },
    memWorkflowToDocumentMap: new Map(), memRejectedDocuments: new Map(), dbSaveRejection: async () => undefined,
    ADMIN_ROLES: ['ADMIN'], enforceDocumentTypeRules: async () => ({ ok: true, docType: {} }) as never,
    createWorkflowInstanceIfRequired: async () => ({ gated: false }) as never, originateForwardTimeoutMs: BOUND,
  } as any));
  const s = app.listen(0, '127.0.0.1'); await new Promise<void>((r) => s.once('listening', () => r()));
  const gp = (s.address() as AddressInfo).port;
  const res = await fetch(`http://127.0.0.1:${gp}/api/workflow-instances/${WFI}/approve`, { method: 'POST', signal: AbortSignal.timeout(5000) });
  const body = await res.text();
  const h: Record<string, string> = {}; res.headers.forEach((v, k) => { if (!['date', 'etag'].includes(k)) h[k] = v; });
  await new Promise((r) => setTimeout(r, BOUND + 600));
  s.closeAllConnections(); s.close();
  const rec = { name, status: res.status, body, headers: h, deletes, logs };
  fs.appendFileSync(OUT, JSON.stringify(rec) + '\n');
  return rec;
}
const u = () => `http://127.0.0.1:${port}`;
const ru = () => `http://127.0.0.1:${rawPort}`;
describe('matrix', () => {
  it('s1 normal 201 ends', async () => { beh = (_q, r) => { r.writeHead(201, { 'content-type': 'application/json' }); r.end('{"id":1}'); }; await run('s1_201_end', u()); });
  it('s2 non-2xx 401 ends', async () => { beh = (_q, r) => { r.writeHead(401); r.end('no'); }; await run('s2_401_end', u()); });
  it('s2b non-2xx 500 ends', async () => { beh = (_q, r) => { r.writeHead(500); r.end('no'); }; await run('s2b_500_end', u()); });
  it('s3a error after status decided: 201 then silence', async () => { beh = (_q, r) => { r.writeHead(201); r.write('{"id":'); }; await run('s3a_201_silence', u()); });
  it('s3b error after status decided: 401 then silence', async () => { beh = (_q, r) => { r.writeHead(401); r.write('x'); }; await run('s3b_401_silence', u()); });
  it('s4a error before status: silent', async () => { beh = () => undefined; await run('s4a_silent', u()); });
  it('s4b error before status: closed port', async () => { await run('s4b_closed', 'http://127.0.0.1:1'); });
  it('s4c error before status: socket destroyed', async () => { rawMode = (s) => s.destroy(); await run('s4c_reset', ru()); });
  it('s5 MARKER: status ok then malformed chunk framing carrying marker', async () => {
    rawMode = (s) => { s.write('HTTP/1.1 201 Created\r\nTransfer-Encoding: chunked\r\n\r\nZZMARKER_CHUNK_9f3\r\nmore'); };
    await run('s5_marker_chunk', ru());
  });
  it('s6 MARKER: status ok then invalid header', async () => {
    rawMode = (s) => { s.write('HTTP/1.1 201 Created\r\nX-Bad: v\x01MARKER_HDR_9f3\r\n\r\n'); };
    await run('s6_marker_hdr', ru());
  });
  it('s7 MARKER: garbage instead of status line', async () => {
    rawMode = (s) => { s.write('GARBAGE_MARKER_STATUS_9f3\r\n\r\n'); };
    await run('s7_marker_status', ru());
  });
  it('s8 mid-body socket destroy after 201', async () => {
    rawMode = (s) => { s.write('HTTP/1.1 201 Created\r\nContent-Length: 100\r\n\r\npartial'); setTimeout(() => s.destroy(), 100); };
    await run('s8_midbody_destroy', ru());
  });
});
