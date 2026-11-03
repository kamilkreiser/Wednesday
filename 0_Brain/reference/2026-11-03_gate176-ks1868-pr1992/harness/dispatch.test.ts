// Gate 176 recorder, Q2: drives the REAL services/originate/src/routes/webhooks.ts dispatchEvent -> deliverWebhook ->
// the REAL @secuura/shared safeOutboundRequest (whichever ssrf-guard blob swap.sh wrote). Stand-ins: the db client
// ($queryRaw / $executeRaw), ../db and ../middleware/auth (module mocks), dns/promises lookup, and http(s).request
// (a fake req object; nothing opens a socket). The originate logger is the REAL winston logger.
// Three subscriptions: wh1 gets the hostile value (DNS or request construction), wh2 and wh3 are healthy.
import { describe, it, vi } from 'vitest';
import fs from 'node:fs';
import { EventEmitter } from 'node:events';
import { VALUES, capture, kind, hits } from './values';

const OUT = process.env.GATE176_OUT as string;
const TAG = process.env.GATE176_TAG as string;
const rec = (o: Record<string, unknown>) => fs.appendFileSync(OUT, JSON.stringify({ tag: TAG, ...o }) + '\n');

const h = vi.hoisted(() => ({ mode: 'dns' as 'dns' | 'req', v: undefined as unknown, constructed: [] as string[], sent: [] as string[] }));

vi.mock('dns/promises', () => {
  const lookup = (host: string) =>
    host.startsWith('wh1') && h.mode === 'dns' ? Promise.reject(h.v) : Promise.resolve([{ address: '203.0.113.7', family: 4 }]);
  return { lookup, default: { lookup } };
});
const fakeRequest = (opts: any, cb: (res: any) => void) => {
  const host = String(opts.hostname);
  h.constructed.push(host);
  if (host.startsWith('wh1') && h.mode === 'req') throw h.v;
  const req: any = new EventEmitter();
  req.write = () => true;
  req.destroy = () => undefined;
  req.end = () => {
    h.sent.push(host);
    setImmediate(() => {
      const res: any = new EventEmitter();
      res.statusCode = 200;
      res.resume = () => setImmediate(() => res.emit('end'));
      cb(res);
    });
  };
  return req;
};
vi.mock('https', async (importOriginal) => {
  const a = await importOriginal<typeof import('https')>();
  return { ...a, default: { ...a, request: fakeRequest }, request: fakeRequest };
});
vi.mock('http', async (importOriginal) => {
  const a = await importOriginal<typeof import('http')>();
  return { ...a, default: { ...a, request: fakeRequest }, request: fakeRequest };
});
vi.mock('../../../../services/originate/src/db', () => ({ prisma: {} }));
vi.mock('../../../../services/originate/src/middleware/auth', () => ({ authenticate: () => (_q: any, _s: any, n: any) => n() }));

describe('gate176 Q2 originate dispatchEvent', () => {
  it('Q2 dispatch loop per class', async () => {
    const { dispatchEvent } = await import('../../../../services/originate/src/routes/webhooks');
    for (const mode of ['dns', 'req'] as const) {
      for (const [name, make] of VALUES) {
        h.mode = mode;
        h.v = make();
        h.constructed = [];
        h.sent = [];
        const rows: Array<{ wh: unknown; success: unknown; errType: string }> = [];
        const client = {
          $queryRaw: (_s: TemplateStringsArray, ..._a: unknown[]) =>
            Promise.resolve([
              { id: '00000000-0000-4000-8000-000000000001', url: 'https://wh1.example.test/hook', secret_v2: 'plain-1' },
              { id: '00000000-0000-4000-8000-000000000002', url: 'https://wh2.example.test/hook', secret_v2: 'plain-2' },
              { id: '00000000-0000-4000-8000-000000000003', url: 'https://wh3.example.test/hook', secret_v2: 'plain-3' },
            ]),
          $executeRaw: (_s: TemplateStringsArray, ...a: unknown[]) => {
            rows.push({ wh: String(a[0]).slice(-1), success: a[4], errType: typeof a[5] });
            return Promise.resolve(1);
          },
        };
        const { result, lines } = await capture(async () => {
          try {
            return { out: 'returned ' + (await dispatchEvent('gate176.event', { k: 1 }, client)) };
          } catch (e) {
            return { out: 'REJECTED ' + kind(e, h.v) };
          }
        });
        rec({
          q: 'Q2', site: `dispatchEvent wh1-${mode}-throws`, value: name, ...result,
          rowsLogged: rows.map((r) => `${r.wh}:${r.success}:${r.errType}`).join(','),
          constructed: h.constructed.map((x) => x.slice(0, 3)).join(','),
          sentToStandIn: h.sent.map((x) => x.slice(0, 3)).join(','),
          sentinelLines: hits(lines),
        });
      }
    }
  });
});
