// GATE PROBE (scratch only) - what the REAL winston logger writes for a hostile Error message, prod JSON + File transports, and dev format.
import { describe, it, vi } from 'vitest';
import * as fs from 'fs';
import * as path from 'path';
import http from 'http';
import express, { type RequestHandler } from 'express';
import { createRequire } from 'module';
import type { AddressInfo } from 'net';

const OUT = process.env.PROBE_OUT as string;
const LOGCWD = process.env.LOGCWD as string;
const emit = (s: string) => { fs.appendFileSync(OUT, s + '\n'); };
const nodeRequire = createRequire(__filename);

async function viaRoute(env: string) {
  process.chdir(LOGCWD);
  vi.stubEnv('NODE_ENV', env);
  vi.stubEnv('LOG_LEVEL', 'debug');
  vi.resetModules();
  const writes: string[] = [];
  const orig = process.stdout.write.bind(process.stdout);
  (process.stdout as any).write = (c: any, ...r: any[]) => { writes.push(String(c)); return true; };
  const origErr = process.stderr.write.bind(process.stderr);
  (process.stderr as any).write = (c: any, ...r: any[]) => { writes.push(String(c)); return true; };
  const { createPlatformRoutes } = await import('../routes/platform');
  const { logger } = await import('../utils/logger');
  const MSG = Symbol.for('message');
  const tr: any = (logger as any).transports[0];
  const origLog = tr.log.bind(tr);
  tr.log = (info: any, cb: any) => { writes.push(String(info[MSG]) + '\n'); return origLog(info, cb); };
  logger.info('CONTROL constant info line');
  const pg = nodeRequire('pg');
  const payload = 'x"\r\n2026-10-13 09:00:00.000 [api-gateway] info: admin login ok user=root\r\n{"level":"info","message":"forged"}\u001b[31m\u0000';
  vi.stubEnv('PLATFORM_DATABASE_URL', 'postgres://u:p@127.0.0.1:1/platform');
  const spy = vi.spyOn(pg.Pool.prototype, 'query').mockImplementation(((_sql: string, params: string[]) => Promise.reject(new Error('invalid input syntax for type uuid: "' + params[0] + '"'))) as never);
  const app = express();
  app.use(createPlatformRoutes({ authenticateToken: (() => ((_q, _s, n) => n()) as RequestHandler) as any, tenantProvisioningUrl: 'http://127.0.0.1:1', setTenantKey: () => {}, getTenantKey: () => undefined, removeTenantKey: () => {}, query: async () => ({ rows: [] }) }));
  const server = http.createServer(app);
  await new Promise<void>((r) => server.listen(0, '127.0.0.1', () => r()));
  const port = (server.address() as AddressInfo).port;
  const get = (p: string) => new Promise<string>((res) => { const rq = http.get({ host: '127.0.0.1', port, path: p }, (rs) => { let b = ''; rs.on('data', (c) => (b += c)); rs.on('end', () => res(rs.statusCode + ' ' + b.slice(0, 100))); }); rq.on('error', (e) => res('ERR ' + e.message)); });
  const s1 = await get('/api/platform/document-lookup?documentId=' + encodeURIComponent(payload.replace('\u0000', '')));
  // length probes: request-target of N chars
  const lens: string[] = [];
  for (const n of [8000, 15000, 16500, 20000]) lens.push(n + ':' + (await get('/api/platform/document-lookup?hash=' + 'a'.repeat(n))).slice(0, 3));
  await new Promise((r) => setTimeout(r, 400));
  process.stdout.write = orig as any; process.stderr.write = origErr as any;
  spy.mockRestore(); server.closeAllConnections(); server.close();
  return { s1, lens, writes };
}

describe('probe_e', () => {
  for (const env of ['production', 'development']) {
    it('real logger, NODE_ENV=' + env, async () => {
      const r = await viaRoute(env);
      const lines = r.writes.join('').split('\n').filter((l) => l.length);
      const ours = lines.filter((l) => l.includes('Document lookup failed'));
      emit(`E[${env}] route status for 1st request: ${r.s1} ; request-target length probes (n:status) ${r.lens.join(' ')}`);
      emit(`E[${env}] stdout physical lines total=${lines.length}; lines containing the context=${ours.length}`);
      emit(`E[${env}] raw count of lines starting with the forged timestamp or forged json: ${lines.filter((l) => l.startsWith('2026-10-13 09:00:00.000 [api-gateway] info: admin') || l.startsWith('{"level":"info","message":"forged"')).length}`);
      emit(`E[${env}] stdout logged line #1 (JSON.stringify of it, first 420 chars): ${JSON.stringify(ours[0] ?? '').slice(0, 420)}`);
      const lens = ours.map((l) => l.length);
      emit(`E[${env}] logged line lengths: ${JSON.stringify(lens)}`);
      if (env === 'production') {
        for (const f of ['logs/error.log', 'logs/combined.log']) {
          const p = path.join(LOGCWD, f);
          const txt = fs.existsSync(p) ? fs.readFileSync(p, 'utf8') : '(missing)';
          const ls = txt.split('\n').filter((l) => l.length);
          emit(`E[file ${f}] bytes=${txt.length} physical lines=${ls.length} forged-start lines=${ls.filter((l) => l.startsWith('2026-10-13 09:00:00.000 [api-gateway] info: admin') || l.startsWith('{"level":"info","message":"forged"')).length} first200=${JSON.stringify(txt.slice(0, 200))}`);
        }
      }
    }, 120000);
  }
});
