// GATE PROBE (scratch only) - can the new logger.error line throw / change the response? Real createPlatformRoutes over HTTP.
import { describe, it, beforeAll, afterAll, afterEach, vi } from 'vitest';
import express, { type RequestHandler } from 'express';
import http from 'http';
import { createRequire } from 'module';
import type { AddressInfo } from 'net';
import * as fs from 'fs';
import { createPlatformRoutes } from '../routes/platform';
import { logger } from '../utils/logger';

const OUT = process.env.PROBE_OUT as string;
const emit = (s: string) => { fs.appendFileSync(OUT, s + '\n'); };
const nodeRequire = createRequire(__filename);
const pg = nodeRequire('pg') as { Pool: { prototype: { query: (...a: unknown[]) => Promise<unknown> } } };
let base = ''; let server: http.Server;
const errorSpy = vi.spyOn(logger, 'error').mockImplementation((() => logger) as never);
let querySpy: { mockRestore: () => void } | undefined;
const unhandled: string[] = [];
const onUR = (e: unknown) => { unhandled.push(String((e as Error)?.message ?? e)); };

beforeAll(async () => {
  process.on('unhandledRejection', onUR);
  const app = express();
  app.use(createPlatformRoutes({
    authenticateToken: (() => ((_req, _res, next) => next()) as RequestHandler) as (required?: boolean) => RequestHandler,
    tenantProvisioningUrl: 'http://127.0.0.1:1', setTenantKey: () => {}, getTenantKey: () => undefined, removeTenantKey: () => {}, query: async () => ({ rows: [] }),
  }));
  server = http.createServer(app);
  await new Promise<void>((r) => server.listen(0, '127.0.0.1', () => r()));
  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterEach(() => { errorSpy.mockClear(); errorSpy.mockImplementation((() => logger) as never); querySpy?.mockRestore(); querySpy = undefined; vi.unstubAllEnvs(); });
afterAll(async () => { process.off('unhandledRejection', onUR); server.closeAllConnections(); await new Promise<void>((r) => server.close(() => r())); errorSpy.mockRestore(); });

function get(): Promise<string> {
  return new Promise((resolve) => {
    const t = setTimeout(() => { r.destroy(); resolve('HUNG (no response in 2.5 s)'); }, 2500);
    const r = http.get(base + '/api/platform/document-lookup?hash=abc', (res) => {
      let b = ''; res.on('data', (c) => (b += c)); res.on('end', () => { clearTimeout(t); resolve(`${res.statusCode} ${b}`); });
    });
    r.on('error', (e) => { clearTimeout(t); resolve('ERR ' + e.message); });
  });
}
async function cell(name: string, value: () => unknown, loggerThrows = false) {
  vi.stubEnv('PLATFORM_DATABASE_URL', 'postgres://u:p@127.0.0.1:1/platform');
  querySpy = vi.spyOn(pg.Pool.prototype, 'query').mockImplementation((() => Promise.reject(value())) as never);
  errorSpy.mockClear(); errorSpy.mockImplementation((() => logger) as never);
  if (loggerThrows) errorSpy.mockImplementation((() => { throw new Error('logger exploded'); }) as never);
  const before = unhandled.length;
  const out = await get();
  await new Promise((r) => setTimeout(r, 50));
  emit(`${name.padEnd(46)} -> ${out}  | logger.error calls=${errorSpy.mock.calls.length} meta=${JSON.stringify(errorSpy.mock.calls[0]?.[1])?.slice(0, 120)} | unhandledRejections+=${unhandled.length - before}${unhandled.length > before ? ' [' + unhandled.slice(before).join('; ').slice(0, 100) + ']' : ''}`);
}

describe('probe_d', () => {
  it('shapes', async () => {
    const circ: any = { a: 1 }; circ.self = circ;
    await cell('Error', () => new Error('boom'));
    await cell('null', () => null);
    await cell('undefined', () => undefined);
    await cell('Symbol', () => Symbol('s'));
    await cell('BigInt', () => 10n);
    await cell('circular object', () => circ);
    await cell('Object.create(null) {x}', () => Object.assign(Object.create(null), { x: 1 }));
    await cell('Error with throwing message getter', () => { const e = new Error('x'); Object.defineProperty(e, 'message', { get() { throw new Error('getter'); } }); return e; });
    await cell('object with throwing constructor getter', () => ({ get constructor(): never { throw new Error('ctor getter'); } }));
    await cell('Proxy, throwing getPrototypeOf trap', () => new Proxy({}, { getPrototypeOf() { throw new Error('gpo trap'); } }));
    await cell('Proxy, throwing ownKeys trap', () => new Proxy({}, { ownKeys() { throw new Error('ownKeys trap'); } }));
    await cell('Proxy, throwing get trap (constructor)', () => new Proxy({}, { get() { throw new Error('get trap'); } }));
    await cell('revoked Proxy', () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; });
    await cell('object with 100k field names', () => { const o: any = {}; for (let i = 0; i < 100000; i++) o['k' + i] = 1; return o; });
    await cell('logger.error itself throws (Error thrown)', () => new Error('boom'), true);
  }, 120000);
});
