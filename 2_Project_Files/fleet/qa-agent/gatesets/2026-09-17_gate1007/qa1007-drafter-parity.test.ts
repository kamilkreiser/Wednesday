// QA drafter parity probe for #1007 (KS-864) — NOT committed; copied into a clone tree, run, moved out by rename.
// For each cell (NODE_ENV x env-var config x fetch mode): fresh module import of the REAL routes/system-status router,
// mounted as index.ts mounts it (/system and /api/system), on 127.0.0.1:0; fetch stubbed with a RECORDER (hit witness);
// GET /system/status, /api/system/status and /system/status/simple; volatile fields normalised; one JSON line per cell to QA_OUT.
import { describe, it, expect, vi } from 'vitest';
import http from 'node:http';
import express from 'express';
import { appendFileSync } from 'node:fs';
import { createHash } from 'node:crypto';

vi.mock('../services/redis', () => ({ getRedisHealth: vi.fn(async () => ({ status: 'healthy' })) }));

const SERVICE_VARS = ['API_GATEWAY_URL', 'AUTH_SERVICE_URL', 'ORIGINATE_SERVICE_URL', 'SECURITY_SERVICE_URL', 'ANCHORING_SERVICE_URL',
  'PRISM_SERVICE_URL', 'TIMESTAMPING_SERVICE_URL', 'WALLET_SERVICE_URL', 'VC_ISSUER_SERVICE_URL', 'BILLING_SERVICE_URL',
  'ANALYTICS_SERVICE_URL', 'STAKING_SERVICE_URL', 'REFERRAL_SERVICE_URL', 'GOVERNANCE_SERVICE_URL', 'KYC_SERVICE_URL',
  'NFT_SERVICE_URL', 'M365_SERVICE_URL', 'TRANSFER_SERVICE_URL'];
const PORTAL_VARS = ['ISSUER_PORTAL_URL', 'VERIFIER_PORTAL_URL', 'ADMIN_PORTAL_URL'];
const DEP_VARS = ['DATABASE_URL', 'REDIS_URL', 'BLOCKFROST_API_KEY', 'STRIPE_SECRET_KEY', 'WALLETCONNECT_PROJECT_ID'];
const NODE_ENVS: Array<string | undefined> = ['development', 'test', 'production', undefined, 'staging'];
const CONFIGS: Record<string, (v: string, i: number) => string | undefined> = {
  none: () => undefined,
  services: (v) => (SERVICE_VARS.includes(v) ? `http://qa-${v.toLowerCase()}.example:1` : undefined),
  portals: (v) => (PORTAL_VARS.includes(v) ? `http://qa-${v.toLowerCase()}.example:1` : undefined),
  all: (v) => `http://qa-${v.toLowerCase()}.example:1`,
  alternate: (v, i) => (i % 2 === 0 ? `http://qa-${v.toLowerCase()}.example:1` : undefined),
  empty: () => '',
};
const MODES = ['offline', 'healthy'] as const;
const DEAD = /ashypond|westeurope|secuura-staging-/g;

function norm(body: any): any {
  const b = JSON.parse(JSON.stringify(body));
  delete b.timestamp; delete b.responseTime;
  if (b.environment) { for (const k of ['nodeVersion', 'npmVersion', 'platform', 'arch', 'uptime', 'memoryUsage']) delete b.environment[k]; }
  if (b.services && !Array.isArray(b.services)) for (const arr of Object.values(b.services) as any[]) for (const s of arr) delete s.latency;
  return b;
}
function get(port: number, path: string): Promise<{ code: number; body: any }> {
  return new Promise((resolve, reject) => {
    http.get({ hostname: '127.0.0.1', port, path }, (res) => {
      let d = ''; res.on('data', (c) => (d += c));
      res.on('end', () => { try { resolve({ code: res.statusCode ?? 0, body: JSON.parse(d) }); } catch (e) { reject(e); } });
    }).on('error', reject);
  });
}
const h = (x: unknown) => createHash('sha256').update(JSON.stringify(x)).digest('hex');

describe('qa1007 drafter parity probe', () => {
  for (const nodeEnv of NODE_ENVS) for (const [cfgName, cfg] of Object.entries(CONFIGS)) for (const mode of MODES) {
    const id = `${nodeEnv ?? 'UNSET'}|${cfgName}|${mode}`;
    it(id, async () => {
      const saved = { ...process.env };
      const all = [...SERVICE_VARS, ...PORTAL_VARS];
      for (const v of [...all, ...DEP_VARS]) delete process.env[v];
      all.forEach((v, i) => { const val = cfg(v, i); if (val !== undefined) process.env[v] = val; });
      if (nodeEnv === undefined) delete process.env.NODE_ENV; else process.env.NODE_ENV = nodeEnv;
      const fetched: string[] = [];
      vi.stubGlobal('fetch', vi.fn(async (u: string) => {
        fetched.push(String(u));
        if (mode === 'offline') throw new Error('offline in qa probe');
        return { ok: true, json: async () => ({ version: 'qa' }) } as any;
      }));
      vi.resetModules();
      const router = (await import('../routes/system-status')).default;
      const app = express(); app.use('/system', router); app.use('/api/system', router);
      const server: http.Server = await new Promise((r) => { const s = app.listen(0, '127.0.0.1', () => r(s)); });
      const port = (server.address() as any).port;
      try {
        const st = await get(port, '/system/status');
        const hitsAfterStatus = fetched.length;
        const st2 = await get(port, '/api/system/status');
        const simple = await get(port, '/system/status/simple');
        const n = norm(st.body); const n2 = norm(st2.body);
        const urls = Object.fromEntries((Object.values(st.body.services) as any[]).flat().map((s: any) => [s.name, s.url]));
        const raw = JSON.stringify(st.body);
        const deadHits = raw.match(DEAD) ?? [];
        const deadWhere = (st.body.troubleshooting as any[]).flatMap((t) => (t.commands ?? []).filter((c: string) => /secuura-staging-/.test(c)).map((c: string) => `${t.component}: ${c}`));
        appendFileSync(process.env.QA_OUT as string, JSON.stringify({
          id, nodeEnvSeenInBody: st.body.environment?.env, statusCode: st.code, apiStatusCode: st2.code, simpleCode: simple.code,
          statusHash: h(n), apiStatusHash: h(n2), simpleHash: h(simple.body), mountsAgree: h(n) === h(n2),
          fetchHitsStatus: hitsAfterStatus, fetchHitsTotal: fetched.length, fetchedStatus: fetched.slice(0, hitsAfterStatus).sort(),
          urls, overall: st.body.status, healthy: st.body.summary?.services?.healthy, deadCount: deadHits.length,
          deadInUrls: Object.values(urls).filter((u: any) => /ashypond|westeurope|secuura-staging-/.test(String(u))).length,
          deadInTroubleshooting: deadWhere.length, deadSample: deadWhere.slice(0, 2), body: n,
        }) + '\n');
        expect(fetched.length).toBeGreaterThan(0);
      } finally {
        await new Promise<void>((r) => server.close(() => r()));
        vi.unstubAllGlobals();
        for (const k of Object.keys(process.env)) if (!(k in saved)) delete process.env[k];
        Object.assign(process.env, saved);
      }
    }, 60_000);
  }
});
