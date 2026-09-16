// qa1010-drafter-probe — RECORDING ONLY (not pass/fail). Real createVerificationRoutes, stateful store, hit-counting
// originate stub on 127.0.0.1:0, log capture, unhandled-rejection capture, active-resource census after each row.
import { it } from 'vitest';
import express from 'express';
import http from 'node:http';
import fs from 'node:fs';
import type { AddressInfo } from 'node:net';
import * as verification from '../routes/verification';

const DOC = 'doc-p'; const WFI = 'wfi-p';
const OUT = process.env.PROBE_OUT as string; const TREE = process.env.PROBE_TREE || '?';
const rows: any[] = [];
const unhandled: string[] = [];
process.on('unhandledRejection', (e: any) => { unhandled.push(String(e && (e.code || e.message) || e)); });
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
function census() { const c: Record<string, number> = {}; for (const k of (process as any).getActiveResourcesInfo()) c[k] = (c[k] || 0) + 1; return c; }

async function row(id: string, behave: (req: any, res: any, st: any) => void, opts: { url?: string; bound?: any; setBound?: boolean; wait?: number; settle?: number; retry?: boolean } = {}) {
  const st: any = { instance: { status: 'pending_approval', documentId: DOC, steps: [{ name: 'A' }], currentStepIndex: 0 }, docs: new Map([[DOC, { title: 't', contentHash: 'h', createdBy: 'u' }]]), deletes: 0, hits: 0, created: 0 };
  const logs: any[] = [];
  const orig = http.createServer((req, res) => { st.hits++; req.resume(); behave(req, res, st); });
  orig.listen(0, '127.0.0.1'); await new Promise((r) => orig.once('listening', r));
  const url = opts.url || `http://127.0.0.1:${(orig.address() as AddressInfo).port}`;
  const deps: any = {
    authenticateToken: () => (_q: any, _s: any, n: any) => n(), mockBodyParser: express.json(), query: async () => ({ rows: [] }), isDbAvailable: () => false,
    redisService: { getWorkflowInstance: async (id: string) => id === WFI ? structuredClone(st.instance) : null, getAllWorkflowInstances: async () => [], setWorkflowInstance: async (_i: string, v: any) => { st.instance = structuredClone(v); },
      getPendingDocument: async (id: string) => st.docs.get(id) ?? null, deletePendingDocument: async (id: string) => { st.deletes++; st.docs.delete(id); } },
    services: { originate: { url }, anchoring: { url: '' } }, log: (level: string, message: string, meta: any) => logs.push({ t: Date.now(), level, message, meta }),
    memWorkflowToDocumentMap: new Map(), memRejectedDocuments: new Map(), dbSaveRejection: async () => undefined, ADMIN_ROLES: ['ADMIN'],
    enforceDocumentTypeRules: async () => ({ ok: true, docType: {} }), createWorkflowInstanceIfRequired: async () => ({ gated: false }), meetsVerificationLevel: () => true,
  };
  if (opts.setBound !== false) deps.originateForwardTimeoutMs = opts.bound === undefined ? 800 : opts.bound;
  const unhBefore = unhandled.length;
  const app = express(); app.use(verification.createVerificationRoutes(deps));
  const gw = app.listen(0, '127.0.0.1'); await new Promise((r) => gw.once('listening', r));
  const port = (gw.address() as AddressInfo).port;
  const call = async () => { const t0 = Date.now(); try { const r = await fetch(`http://127.0.0.1:${port}/api/workflow-instances/${WFI}/approve`, { method: 'POST', signal: AbortSignal.timeout(opts.wait || 3000) }); return { status: r.status, body: (await r.text()).slice(0, 300), ms: Date.now() - t0 }; } catch (e: any) { return { status: 'NO RESPONSE', body: '', ms: Date.now() - t0 }; } };
  const t0 = Date.now();
  const first = await call();
  const hitsAtAnswer = st.hits, deletesAtAnswer = st.deletes;
  await sleep(opts.settle ?? 1500);
  const second = opts.retry ? await call() : undefined;
  if (opts.retry) await sleep(300);
  gw.closeAllConnections(); orig.closeAllConnections();
  await new Promise((r) => gw.close(r)); await new Promise((r) => orig.close(r));
  await sleep(200);
  rows.push({ tree: TREE, id, bound: opts.setBound === false ? 'deps-absent(default)' : String(opts.bound === undefined ? 800 : opts.bound), first, hitsAtAnswer, deletesAtAnswer,
    hitsFinal: st.hits, deletesFinal: st.deletes, created: st.created, pendingKept: st.docs.has(DOC), instance: st.instance.status, second,
    errorLogs: logs.filter((l) => l.level === 'error').map((l) => ({ dtFromCall: l.t - t0, msg: l.message, err: l.meta && l.meta.error })),
    infoLogs: logs.filter((l) => l.level === 'info').length, unhandled: unhandled.slice(unhBefore), censusAfter: census() });
}
const answer = (code: number, body = '{"id":"doc-p"}') => (_q: any, res: any) => { res.writeHead(code, { 'Content-Type': 'application/json' }); res.end(body); };

it('probe rows', { timeout: 120_000 }, async () => {
  const head = typeof (verification as any).ORIGINATE_FORWARD_TIMEOUT_MS === 'number';
  rows.push({ tree: TREE, id: 'EXPORT', ORIGINATE_FORWARD_TIMEOUT_MS: (verification as any).ORIGINATE_FORWARD_TIMEOUT_MS, censusBaseline: census() });
  await row('O-201', answer(201));
  await row('O-200', answer(200));
  await row('O-204', (_q, res) => { res.writeHead(204); res.end(); });
  await row('O-302', answer(302));
  await row('O-401', answer(401, '{"error":"ORIGINATE-BODY-MARKER"}'));
  await row('O-500', answer(500));
  await row('O-closed-port', () => undefined, { url: 'http://127.0.0.1:1' });
  await row('O-destroy-before-headers', (req) => req.socket.destroy());
  await row('O-never-answers', () => undefined);
  await row('O-late-201-bound+700', (_q, res, st) => setTimeout(() => { if (res.destroyed || res.socket?.destroyed) { st.lateSkipped = true; return; } st.created++; res.writeHead(201); res.end('{}'); }, 1500), { settle: 1500 });
  await row('O-late-201-persist-then-lost+retry', (_q, res, st) => setTimeout(() => { st.created++; if (res.socket?.destroyed) return; res.writeHead(201); res.end('{}'); }, 1500), { settle: 1200, retry: true });
  await row('O-201-mid-body-reset', (_q, res) => { res.writeHead(201); res.write('{"id":'); setTimeout(() => res.socket?.destroy(), 50); });
  await row('O-201-body-never-ends', (_q, res) => { res.writeHead(201); res.write('{"id":'); }, { settle: 1800 });
  await row('O-drip-102-then-201-at-2500', (_q, res) => { const iv = setInterval(() => { try { res.writeProcessing(); } catch { /* */ } }, 300); setTimeout(() => { clearInterval(iv); if (!res.socket?.destroyed) { res.writeHead(201); res.end('{}'); } }, 2500); }, { wait: 4000, settle: 500 });
  if (head) {
    await row('BOUND-0', () => undefined, { bound: 0, wait: 3000, settle: 300 });
    await row('BOUND-neg1', () => undefined, { bound: -1, wait: 2000, settle: 300 });
    await row('BOUND-NaN', () => undefined, { bound: NaN, wait: 2000, settle: 300 });
    await row('BOUND-string', () => undefined, { bound: '800', wait: 2000, settle: 300 });
    await row('BOUND-null', () => undefined, { bound: null, wait: 2000, settle: 300 });
    await row('BOUND-neg1-closed-port', () => undefined, { bound: -1, url: 'http://127.0.0.1:1', wait: 2000, settle: 500 });
    if (process.env.PROBE_DEFAULT === '1') await row('BOUND-deps-absent-default', () => undefined, { setBound: false, wait: 17_000, settle: 300 });
  }
  fs.writeFileSync(OUT, JSON.stringify(rows, null, 1));
});
