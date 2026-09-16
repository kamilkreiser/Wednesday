// qa1006-drafter-probe.test.ts — #1006 DRAFTER RECORDING harness (not a gate cell: it RECORDS, the gate's cells ASSERT).
// Boots demo-service's REAL createApp() on 127.0.0.1:0 per NODE_ENV (set BEFORE createApp: express reads app.get('env') at init, and
// finalhandler's stack-in-body decision reads it), sends one request per upstream error class, and records status, content-type,
// selected headers, a body digest and leak markers. Row set E* = the error classes that can reach the handler in this app; K* =
// controls answered by something else. Then H* = the exported handler (head only) vs express's own finalhandler (the base behaviour,
// demo-service had no handler) on SYNTHETIC errors: out-of-range / non-numeric status, message-less 4xx, headersSent.
// Writes JSON to process.env.QA_OUT.
vi.mock('../utils/logger', () => ({
  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() },
  createLogger: () => ({ debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: vi.fn() }),
}));
vi.mock('../services/authClient', () => ({ authenticatePersona: vi.fn() }));

import { describe, it, expect, vi } from 'vitest';
import express from 'express';
import { writeFileSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { gzipSync } from 'node:zlib';
import { request as httpRequest } from 'node:http';
import type { AddressInfo } from 'node:net';
import { createApp } from '../app';

const ENVS: (string | undefined)[] = ['production', 'development', 'demo', 'test', 'staging', undefined];
const rows: Record<string, unknown>[] = [];

function send(port: number, method: string, path: string, headers: Record<string, string>, body?: Buffer): Promise<{ status: number; headers: Record<string, unknown>; body: string }> {
  return new Promise((ok, fail) => {
    const req = httpRequest({ host: '127.0.0.1', port, method, path, headers: { ...headers, ...(body ? { 'content-length': String(body.length) } : {}) } }, (res) => {
      const chunks: Buffer[] = [];
      res.on('data', (d) => chunks.push(d as Buffer));
      res.on('end', () => ok({ status: res.statusCode ?? 0, headers: res.headers as Record<string, unknown>, body: Buffer.concat(chunks).toString('utf8') }));
      res.on('error', fail);
    });
    req.on('error', fail);
    req.setTimeout(2500, () => { req.destroy(); ok({ status: -2, headers: {}, body: 'CLIENT TIMEOUT 2500ms (no complete response)' }); });
    if (body) req.write(body);
    req.end();
  });
}
function listen(app: express.Express): Promise<{ port: number; close: () => Promise<void> }> {
  return new Promise((ok) => {
    const s = app.listen(0, '127.0.0.1', () => ok({ port: (s.address() as AddressInfo).port, close: () => new Promise((d) => s.close(() => d())) }));
  });
}
function record(id: string, env: string | undefined, r: { status: number; headers: Record<string, unknown>; body: string }) {
  const b = r.body;
  rows.push({
    id, env: env ?? 'unset', status: r.status, ctype: r.headers['content-type'] ?? null,
    csp: r.headers['content-security-policy'] ?? null, nosniff: r.headers['x-content-type-options'] ?? null,
    header_names: Object.keys(r.headers).sort(), body_len: b.length, body_head: b.slice(0, 220),
    html: /<html|<!DOCTYPE/i.test(b), stack: /\n\s+at |    at /.test(b), abs_path: /\/(Volumes|private|Users|app|home)\//.test(b), node_modules: b.includes('node_modules'),
  });
}
const OVERSIZE = Buffer.from(JSON.stringify({ x: 'a'.repeat(150 * 1024) }));
const LONG_SYNTAX = Buffer.from('{"k": "' + 'SECRETISH'.repeat(20) + '" oops}');
const CLASSES: [string, string, string, Record<string, string>, Buffer | undefined][] = [
  ['E1 JSON syntax {not json', 'POST', '/demo-api/health', { 'content-type': 'application/json' }, Buffer.from('{not json')],
  ['E2 raw 0x00 inside a string', 'POST', '/nope', { 'content-type': 'application/json' }, Buffer.concat([Buffer.from('{"x":"a'), Buffer.from([0]), Buffer.from('b"}')])],
  ['E3 strict first-char (body "nope")', 'POST', '/demo-api/health', { 'content-type': 'application/json' }, Buffer.from('nope')],
  ['E4 oversize 150KB > express.json 100kb default', 'POST', '/demo-api/health', { 'content-type': 'application/json' }, OVERSIZE],
  ['E5 unsupported charset koi8-r (body-parser refuses a non-utf- charset; utf-7 PASSES its utf- prefix check: first run)', 'POST', '/demo-api/health', { 'content-type': 'application/json; charset=koi8-r' }, Buffer.from('{"a":1}')],
  ['E6 unsupported content-encoding br', 'POST', '/demo-api/health', { 'content-type': 'application/json', 'content-encoding': 'br' }, Buffer.from('{"a":1}')],
  ['E7 gzip header, non-gzip bytes', 'POST', '/demo-api/health', { 'content-type': 'application/json', 'content-encoding': 'gzip' }, Buffer.from('{"a":1}')],
  ['E8 long syntax error (how much body is echoed)', 'POST', '/demo-api/health', { 'content-type': 'application/json' }, LONG_SYNTAX],
  ['K1 valid gzip body -> routing (control: encoding path works)', 'POST', '/nope', { 'content-type': 'application/json', 'content-encoding': 'gzip' }, gzipSync(Buffer.from('{"a":1}'))],
  ['K2 escaped NUL -> the control-byte guard answers (not the handler)', 'POST', '/nope', { 'content-type': 'application/json' }, Buffer.from('{"x":"a\\u0000b"}')],
  ['K3 clean body, unrouted -> 404 handler (not the handler)', 'POST', '/nope', { 'content-type': 'application/json' }, Buffer.from('{"x":"ab"}')],
  ['K4 GET /demo-api/health -> 200', 'GET', '/demo-api/health', {}, undefined],
  ['K5 guarded route without key -> 401 (not the handler)', 'POST', '/demo-api/presenter-mode', { 'content-type': 'application/json' }, Buffer.from('{"enabled":true}')],
];

describe('qa1006 drafter probe (RECORDING)', () => {
  it('records every error class x every NODE_ENV on the real createApp()', async () => {
    const saved = process.env.NODE_ENV;
    for (const env of ENVS) {
      if (env === undefined) delete process.env.NODE_ENV; else process.env.NODE_ENV = env;
      process.env.DEMO_SERVICE_KEY = 'qa-probe-key-0123456789abcdef';
      const app = createApp();
      const { port, close } = await listen(app);
      try {
        for (const [id, m, p, h, b] of CLASSES) record(id, env, await send(port, m, p, h, b));
      } finally { await close(); }
    }
    if (saved === undefined) delete process.env.NODE_ENV; else process.env.NODE_ENV = saved;
    expect(rows.length).toBe(ENVS.length * CLASSES.length);
  }, 120000);

  it('records the exported handler vs express finalhandler on synthetic errors (head only)', async () => {
    const handlerPath = join(__dirname, '..', 'middleware', 'errorHandler.ts');
    const has = existsSync(handlerPath);
    const mod = has ? await import('../middleware/errorHandler') : null;
    const SYN: [string, () => unknown][] = [
      ['H1 status 200', () => Object.assign(new Error('msg-200'), { status: 200 })],
      ['H2 status 302', () => Object.assign(new Error('msg-302'), { status: 302 })],
      ['H3 status 600', () => Object.assign(new Error('msg-600'), { status: 600 })],
      ['H4 status "400" (string)', () => Object.assign(new Error('msg-str'), { status: '400' })],
      ['H5 status NaN', () => Object.assign(new Error('msg-nan'), { status: Number.NaN })],
      ['H6 statusCode 404, empty message', () => Object.assign(new Error(''), { statusCode: 404 })],
      ['H7 a thrown string (non-Error)', () => 'a-thrown-string'],
      ['H8 5xx carrying a message', () => Object.assign(new Error('internal /Volumes/x detail'), { status: 503 })],
      ['H9 http-errors-style 405 with err.headers {Allow}', () => Object.assign(new Error('Method Not Allowed'), { status: 405, headers: { Allow: 'GET' } })],
    ];
    for (const withHandler of has ? [false, true] : [false]) {
      for (const env of ['development', 'production']) {
        process.env.NODE_ENV = env;
        for (const [id, mk] of SYN) {
          const app = express();
          app.get('/boom', (_q, _s, next) => next(mk()));
          app.get('/sent', (_q, res, next) => { res.status(200); res.write('partial'); next(Object.assign(new Error('after-headers'), { status: 400 })); });
          if (withHandler && mod) app.use(mod.errorHandler as express.ErrorRequestHandler);
          const { port, close } = await listen(app);
          try {
            record(`${id} [${withHandler ? 'errorHandler' : 'finalhandler'}]`, env, await send(port, 'GET', '/boom', {}).catch((e: Error) => ({ status: -1, headers: {}, body: 'CLIENT ERROR ' + e.message })));
            if (id.startsWith('H1')) {
              const r = await send(port, 'GET', '/sent', {}).catch((e: Error) => ({ status: -1, headers: {}, body: 'CLIENT ERROR ' + e.message }));
              record(`H10 error after headers sent [${withHandler ? 'errorHandler' : 'finalhandler'}]`, env, r);
            }
          } finally { await close(); }
        }
      }
    }
    writeFileSync(process.env.QA_OUT as string, JSON.stringify(rows, null, 1));
    expect(rows.length).toBeGreaterThan(0);
  }, 120000);
});
