// Gate 177 mutant oracle (api-gateway): for every value class V01-V17, the /dashboard handler lists the bad service as
// 'down' with a string error, and the overall status equals the ordinary-Error one (layout: 1 bad + 5 up => degraded).
import { it, expect, vi } from 'vitest';
import { VALUES } from './values';
const h = vi.hoisted(() => ({ services: {} as Record<string, { url: string; healthPath: string }> }));
vi.mock('../config/services', () => ({ get services() { return h.services; } }));
import router from '../routes/health-dashboard';
const V17 = VALUES.filter(([n]) => !n.startsWith('V18') && !n.startsWith('V19'));
h.services = Object.fromEntries([['bad', 'https://bad.t'], ...[1, 2, 3, 4, 5].map((i) => [`ok${i}`, `https://ok${i}.t`])].map(([k, u]) => [k, { url: u, healthPath: '/health' }]));
async function dash(mk: () => unknown) {
  vi.stubGlobal('fetch', async (url: string) => { if (String(url).startsWith('https://bad.t')) throw mk(); return { ok: true, status: 200, json: async () => ({ status: 'ok' }) }; });
  const layer = (router as any).stack.find((l: any) => l.route?.path === '/dashboard');
  const out: any = {};
  const res: any = { status(c: number) { out.code = c; return res; }, json(b: unknown) { out.body = b; return res; } };
  await layer.route.stack[0].handle({}, res);
  vi.unstubAllGlobals();
  return out;
}
for (const [name, mk] of V17) {
  it(`oracle dashboard ${name}`, async () => {
    const o = await dash(mk);
    expect(o.code).toBe(200);
    expect(o.body.status).toBe('degraded');
    expect(o.body.services.bad?.status).toBe('down');
    expect(typeof o.body.services.bad?.error).toBe('string');
    expect(o.body.summary.healthy).toBe(5);
  });
}
