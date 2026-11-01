// QA gate 96 probe (NOT part of the PR): real express app + the real router + the real request schemas;
// only the service modules and the logger are replaced.
import { describe, it, expect, vi, beforeAll, afterAll } from 'vitest';
import express from 'express';
import { z } from 'zod';
import { writeFileSync } from 'node:fs';
import type { AddressInfo } from 'node:net';

const ks = vi.hoisted(() => ({ value: undefined as unknown, logs: [] as Array<[string, unknown]> }));
const rej = () => Promise.reject(ks.value);
vi.mock('../services/analyticsService', () => ({
  analyticsService: {
    getPlatformOverview: rej, getCertificationMetrics: rej, getVerificationMetrics: rej, getGovernanceMetrics: rej,
    getRevenueMetrics: rej, getUserMetrics: rej, getRealTimeMetrics: rej, getActivityFeed: rej,
  },
}));
vi.mock('../services/exportService', () => ({
  exportService: { createExport: rej, getExport: rej, listExports: rej, generateReport: rej },
}));
vi.mock('../utils/logger', () => ({
  logger: {
    info: () => undefined, warn: () => undefined, debug: () => undefined,
    error: (m: string, meta: unknown) => { ks.logs.push([m, JSON.parse(JSON.stringify(meta))]); },
  },
}));

type R = { name: string; method: 'GET' | 'POST'; url: string; body?: unknown; zodable: boolean };
const VALID_EXPORT = { type: 'x', period: 'month', format: 'json' };
const VALID_REPORT = { type: 'summary', period: 'month' };
const ROUTES: R[] = [
  { name: 'overview', method: 'GET', url: '/api/analytics/overview', zodable: true },
  { name: 'certifications', method: 'GET', url: '/api/analytics/certifications', zodable: true },
  { name: 'verifications', method: 'GET', url: '/api/analytics/verifications', zodable: true },
  { name: 'governance', method: 'GET', url: '/api/analytics/governance', zodable: true },
  { name: 'revenue', method: 'GET', url: '/api/analytics/revenue', zodable: true },
  { name: 'users', method: 'GET', url: '/api/analytics/users', zodable: true },
  { name: 'activity', method: 'GET', url: '/api/analytics/activity', zodable: true },
  { name: 'post_exports', method: 'POST', url: '/api/analytics/exports', body: VALID_EXPORT, zodable: true },
  { name: 'post_reports', method: 'POST', url: '/api/analytics/reports', body: VALID_REPORT, zodable: true },
  { name: 'realtime', method: 'GET', url: '/api/analytics/realtime', zodable: false },
  { name: 'export_by_id', method: 'GET', url: '/api/analytics/exports/abc', zodable: false },
  { name: 'export_list', method: 'GET', url: '/api/analytics/exports', zodable: false },
];
// requests that make the REAL schema throw a REAL ZodError (before any service call)
const BAD: Record<string, { url?: string; body?: unknown }> = {
  overview: { url: '/api/analytics/overview?period=nonsense' },
  certifications: { url: '/api/analytics/certifications?period=nonsense' },
  verifications: { url: '/api/analytics/verifications?period=nonsense' },
  governance: { url: '/api/analytics/governance?period=nonsense' },
  revenue: { url: '/api/analytics/revenue?period=nonsense' },
  users: { url: '/api/analytics/users?period=nonsense' },
  activity: { url: '/api/analytics/activity?limit=abc&zzz=1' },
  post_exports: { body: { type: 5 } },
  post_reports: { body: { type: 'nope' } },
};
const revoked = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const getterErr = () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } });
const nullProto = () => Object.create(null);
const VALUES: Array<[string, () => unknown]> = [
  ['ordinaryError', () => new Error('boom ordinary')],
  ['string', () => 'plain string'],
  ['plainObject', () => ({ a: 1 })],
  ['nullish', () => null],
  ['zodErrorFromService', () => new z.ZodError([{ code: 'custom', path: ['svc'], message: 'from service' }])],
  ['zodErrorMessageGetterThrows', () => { const e = new z.ZodError([{ code: 'custom', path: ['svc'], message: 'bigint' }]); Object.defineProperty(e, 'message', { get() { throw new Error('zod message boom'); } }); return e; }],
  ['revokedProxy', revoked],
  ['getterThrowsError', getterErr],
  ['nullProtoObject', nullProto],
];

let server: import('node:http').Server; let base = '';
const unhandled: string[] = [];
const onUnh = (e: unknown) => { unhandled.push('unhandled'); void e; };
beforeAll(async () => {
  process.on('unhandledRejection', onUnh);
  const { default: router } = await import('../routes/analytics.js');
  const app = express(); app.use(express.json()); app.use('/api/analytics', router);
  await new Promise<void>((r) => { server = app.listen(0, '127.0.0.1', () => r()); });
  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => { process.off('unhandledRejection', onUnh); server.close(); });

async function call(r: R, over?: { url?: string; body?: unknown }) {
  ks.logs.length = 0; unhandled.length = 0;
  const ctl = new AbortController(); const t = setTimeout(() => ctl.abort(), 2500);
  let out: Record<string, unknown>;
  try {
    const resp = await fetch(base + (over?.url ?? r.url), {
      method: r.method, signal: ctl.signal,
      headers: { 'content-type': 'application/json' },
      body: r.method === 'POST' ? JSON.stringify(over?.body ?? r.body) : undefined,
    });
    const text = await resp.text();
    out = { status: resp.status, text };
  } catch (e) { out = { status: 'NO_RESPONSE', text: String((e as Error).name) }; }
  clearTimeout(t);
  await new Promise((r2) => setTimeout(r2, 30));
  out.logs = JSON.parse(JSON.stringify(ks.logs)); out.unhandled = unhandled.length;
  return out;
}

describe('gate96 probe', () => {
  it('matrix', async () => {
    const rows: Record<string, unknown> = {};
    for (const r of ROUTES) {
      for (const [vn, mk] of VALUES) { ks.value = mk(); rows[`${r.name}/${vn}`] = await call(r); }
      if (BAD[r.name]) { ks.value = new Error('should not be reached'); rows[`${r.name}/realSchemaZodError`] = await call(r, BAD[r.name]); }
    }
    writeFileSync(process.env.PROBE_OUT as string, JSON.stringify(rows, null, 1));
    expect(Object.keys(rows).length).toBeGreaterThan(100);
  }, 120000);
});
