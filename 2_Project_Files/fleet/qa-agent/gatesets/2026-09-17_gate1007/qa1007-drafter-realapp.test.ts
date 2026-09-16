// QA drafter real-app probe for #1007 Q9 (KS-1102 record) — NOT committed; copied into a clone tree, run, moved out by rename.
// Imports the REAL gateway app (index.ts's require.main guard keeps it from booting) under NODE_ENV=test and =development, serves it on
// 127.0.0.1:0, and sends GETs with NO credential to /system/status, /api/system/status, /system/status/simple; a positive control sends
// a no-credential GET to an authenticated route. fetch is a recorder (hit witness: the status handler probes every service).
import { describe, it, expect, vi, afterAll } from 'vitest';
import http from 'node:http';
import { appendFileSync } from 'node:fs';

const fetched: string[] = [];
function get(port: number, path: string): Promise<{ code: number; text: string }> {
  return new Promise((resolve, reject) => {
    http.get({ hostname: '127.0.0.1', port, path, agent: false }, (res) => {
      let d = ''; res.on('data', (c) => (d += c)); res.on('end', () => resolve({ code: res.statusCode ?? 0, text: d }));
    }).on('error', reject);
  });
}
afterAll(() => { vi.unstubAllEnvs(); vi.unstubAllGlobals(); });

for (const nodeEnv of ['test', 'development']) {
  it(`real app, NODE_ENV=${nodeEnv}: public status routes answer with no credential`, async () => {
    vi.resetModules();
    vi.stubEnv('NODE_ENV', nodeEnv);
    vi.stubEnv('GATEWAY_VOUCH_SECRET', '');
    const realFetch = globalThis.fetch;
    vi.stubGlobal('fetch', vi.fn(async (u: any, ...rest: any[]) => {
      const s = String(u);
      if (s.startsWith('http://127.0.0.1:')) return (realFetch as any)(u, ...rest);
      fetched.push(s); throw new Error('offline in qa probe');
    }));
    const app = (await import('../index')).default;
    const server = http.createServer(app as http.RequestListener);
    await new Promise<void>((r) => server.listen(0, '127.0.0.1', () => r()));
    const port = (server.address() as any).port;
    try {
      const rows: any = { nodeEnv };
      for (const p of ['/system/status', '/api/system/status', '/system/status/simple', '/api/documents']) {
        const before = fetched.length; const r = await get(port, p);
        let keys: string[] = []; let svc0: any = null; let dep0: any = null; let envField: any = null;
        try { const j = JSON.parse(r.text); keys = Object.keys(j); svc0 = j.services?.core?.[0] ? Object.keys(j.services.core[0]) : (Array.isArray(j.services) ? Object.keys(j.services[0] ?? {}) : null); dep0 = j.dependencies?.[0] ? Object.keys(j.dependencies[0]) : null; envField = j.environment?.env ?? null; } catch { /* not JSON */ }
        rows[p] = { code: r.code, fetchHits: fetched.length - before, topKeys: keys, serviceEntryKeys: svc0, dependencyEntryKeys: dep0, environmentEnv: envField, bodyHead: r.text.slice(0, 120) };
      }
      appendFileSync(process.env.QA_OUT as string, JSON.stringify(rows) + '\n');
      expect(rows['/system/status'].fetchHits).toBeGreaterThan(0);
    } finally {
      await new Promise<void>((r) => server.close(() => r()));
    }
  }, 120_000);
}
