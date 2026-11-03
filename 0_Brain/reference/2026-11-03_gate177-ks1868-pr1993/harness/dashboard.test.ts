// Gate 177 Q4b recorder: the REAL api-gateway health-dashboard router (whichever blob swap.sh wrote), mounted on a REAL
// express app listening on 127.0.0.1 (ephemeral port) and requested over a REAL socket with node:http. Only the probe
// fetch (the global fetch the route uses to reach each service) is replaced; the service list is a stand-in.
// Layout A: 1 deployed service (the bad one) + 1 localhost (not_deployed).
// Layout B: 6 deployed (1 bad + 5 answering 200 {status:'ok'}) + 1 localhost, so 5/6 > 0.8.
import { it, vi } from 'vitest';
import { appendFileSync } from 'node:fs';
import http from 'node:http';
import type { AddressInfo } from 'node:net';
import { VALUES, SENT, capture, kind, hits } from './values';

const h = vi.hoisted(() => ({ services: {} as Record<string, { url: string; healthPath: string }> }));
vi.mock('../config/services', () => ({
  get services() {
    return h.services;
  },
}));
import express from 'express';
import router from '../routes/health-dashboard';

const OUT = process.env.GATE177_OUT!;
const TAG = process.env.GATE177_TAG!;
const rec = (o: Record<string, unknown>) => appendFileSync(OUT, JSON.stringify({ tag: TAG, ...o }) + '\n');
const norm = (s: string) => s.replace(/SNTL177[-\w]*/g, 'S');

const BAD = 'https://bad.gate177.test';
const LAYOUTS: Record<string, Record<string, { url: string; healthPath: string }>> = {
  A: { bad: { url: BAD, healthPath: '/health' }, local: { url: 'http://localhost:9999', healthPath: '/health' } },
  B: {
    bad: { url: BAD, healthPath: '/health' },
    ...Object.fromEntries([1, 2, 3, 4, 5].map((i) => [`ok${i}`, { url: `https://ok${i}.gate177.test`, healthPath: '/health' }])),
    local: { url: 'http://localhost:9999', healthPath: '/health' },
  },
};
const TRIG: Record<string, (mk: () => unknown) => () => Promise<any>> = {
  'T1 fetch rejects': (mk) => async () => { throw mk(); },
  'T2 response.ok getter throws': (mk) => async () => ({ get ok(): boolean { throw mk(); }, status: 200, json: async () => ({}) }),
};

function get(port: number): Promise<{ code: number; body: string }> {
  return new Promise((res, rej) => {
    http.get({ host: '127.0.0.1', port, path: '/api/system/health/dashboard' }, (r) => {
      let b = '';
      r.setEncoding('utf8');
      r.on('data', (c) => (b += c));
      r.on('end', () => res({ code: r.statusCode!, body: b }));
    }).on('error', rej);
  });
}

it('gate177 Q4b /dashboard over HTTP', async () => {
  const app = express();
  app.use('/api/system/health', router);
  const server = app.listen(0, '127.0.0.1');
  await new Promise((r) => server.once('listening', r));
  const port = (server.address() as AddressInfo).port;
  const realFetch = globalThis.fetch;
  try {
    const cells: Array<[string, (() => unknown) | null | 'http500']> = [
      ['C1 control: bad service answers 200', null],
      ['C2 control: bad service answers 500', 'http500'],
      ...VALUES,
    ];
    { const c = await capture(async () => { console.error(SENT); }); rec({ q: 'Q5C', site: 'log capture (api-gateway)', value: 'console.error', lines: c.lines.length, logSentinel: hits(c.lines) }); }
    for (const layout of ['A', 'B']) {
      for (const t of Object.keys(TRIG)) {
        for (const [vname, mk] of cells) {
          if (mk === null || mk === 'http500') { if (t !== 'T1 fetch rejects') continue; }
          h.services = LAYOUTS[layout];
          let orig: unknown;
          const badFetch = mk === null ? async () => ({ ok: true, status: 200, json: async () => ({ status: 'ok' }) })
            : mk === 'http500' ? async () => ({ ok: false, status: 500, json: async () => ({}) })
            : TRIG[t](() => (orig = (mk as () => unknown)()));
          let probes = 0;
          globalThis.fetch = (async (url: any, init?: any) => {
            probes++;
            if (String(url).startsWith(BAD)) return badFetch();
            return { ok: true, status: 200, json: async () => ({ status: 'ok' }) };
          }) as any;
          const { result, lines } = await capture(() => get(port));
          globalThis.fetch = realFetch;
          const body = JSON.parse(result.body);
          const badEntry = body.services?.bad;
          rec({ q: 'Q4b', site: `dashboard layout ${layout} ${t}`, value: vname, http: result.code, status: body.status,
            summary: JSON.stringify(body.summary), badPresent: badEntry !== undefined, badStatus: badEntry?.status,
            badError: badEntry?.error === undefined ? undefined : norm(String(badEntry.error)), badErrorType: typeof badEntry?.error,
            keys: Object.keys(body.services ?? {}).sort().join(','), probes, answerSentinel: result.body.includes(SENT) ? 1 : 0, logSentinel: hits(lines),
            origKind: orig === undefined ? undefined : typeof orig });
        }
      }
    }
  } finally {
    globalThis.fetch = realFetch;
    await new Promise((r) => server.close(r));
  }
});
