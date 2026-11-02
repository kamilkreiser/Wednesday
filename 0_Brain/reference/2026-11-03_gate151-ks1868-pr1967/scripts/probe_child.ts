// usage: tsx -r stub_ioredis.js probe_child.ts <base|head> <kind> <N> <mode>
// mode "listener": N cycles of (GET /state ; GET /state ; POST presenter-mode true ; emit kind to the live client's error listener)
// mode "catch":    POST /presenter-mode with set() rejecting kind (client healthy), N times
import express from 'express';
import http from 'node:http';
const [, , which, kind, nStr, mode] = process.argv;
const N = Number(nStr);
const reg = (globalThis as any).__redisReg;
const uncaught: string[] = []; const unhandled: string[] = [];
process.on('uncaughtException', (e: any) => { uncaught.push('uncaught'); });
process.on('unhandledRejection', (e: any) => { unhandled.push('unhandled'); });
const mk = (k: string): (() => unknown) => {
  switch (k) {
    case 'error': return () => new Error('boom');
    case 'revoked': return () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
    case 'getter': return () => Object.create(Error.prototype, { message: { get() { throw new Error('g'); } } });
    case 'null': return () => null;
    case 'undefined': return () => undefined;
    case 'string': return () => 'plain string';
    case 'number': return () => 42;
    case 'plainobj': return () => ({ message: 'x' });
    case 'symbolmsg': return () => { const e = new Error('x'); Object.defineProperty(e, 'message', { value: Symbol('s') }); return e; };
    default: throw new Error('kind');
  }
};
async function main() {
  process.env.REDIS_URL = 'redis://127.0.0.1:1';
  const mod = await import(which === 'base' ? '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate151-ks1868-pr1967/repo/Blockchain/Dev/services/demo-service/src/routes/state_base.ts' : '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate151-ks1868-pr1967/repo/Blockchain/Dev/services/demo-service/src/routes/state.ts');
  const app = express(); app.use(express.json()); app.use('/demo-api', mod.stateRouter);
  const srv = http.createServer(app); await new Promise<void>((r) => srv.listen(0, '127.0.0.1', r));
  const port = (srv.address() as any).port;
  const call = async (method: string, path: string, body?: any) => {
    const ac = new AbortController(); const t = setTimeout(() => ac.abort(), 1200);
    try {
      const r = await fetch(`http://127.0.0.1:${port}/demo-api${path}`, { method, headers: { 'content-type': 'application/json' }, body: body ? JSON.stringify(body) : undefined, signal: ac.signal });
      const txt = await r.text(); return `${r.status} ${txt}`;
    } catch { return 'NO-RESPONSE(timeout)'; } finally { clearTimeout(t); }
  };
  const rows: string[] = []; let listenerThrows = 0;
  if (mode === 'listener') {
    for (let i = 0; i < N; i++) {
      rows.push('GET ' + await call('GET', '/state'));
      rows.push('POST ' + await call('POST', '/presenter-mode', { enabled: true }));
      const live = reg.clients[reg.clients.length - 1];
      try { live.emitError(mk(kind)()); } catch { listenerThrows++; }
      await new Promise((r) => setTimeout(r, 5));
    }
    rows.push('final GET ' + await call('GET', '/state'));
  } else {
    reg.setFail = mk(kind);
    for (let i = 0; i < N; i++) rows.push('POST ' + await call('POST', '/presenter-mode', { enabled: true }));
    rows.push('final GET ' + await call('GET', '/state'));
  }
  const out = { which, kind, N, mode, clients: reg.clients.length, deadClients: reg.clients.filter((c: any) => c.dead).length, listenerThrows, uncaught: uncaught.length, unhandled: unhandled.length, rowsDistinct: [...new Set(rows)], rows: rows.length };
  process.stderr.write('RESULT ' + JSON.stringify(out) + '\n');
  srv.close(); process.exit(0);
}
main();
