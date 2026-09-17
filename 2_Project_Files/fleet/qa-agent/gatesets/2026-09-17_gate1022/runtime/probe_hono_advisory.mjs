// probe_hono_advisory.mjs — Probe D: the hono bytes that ship in the mcp-server runtime tree, exercised DIRECTLY on two of the three
// advisory behaviours (the service never loads hono; this is the only way 4.13.x runs at all). Run with cwd = img-<tree>/prod.
// crvj (query read after a fragment): hono's own getQueryParam on a raw URL string containing '#', and a Hono app behind @hono/node-server's
//   getRequestListener fed a raw request-target with '#'. g6gw (unbounded dot nesting in parseBody): a urlencoded body with a deep dotted key.
import fs from 'node:fs';
import http from 'node:http';
import { createRequire } from 'node:module';
const require = createRequire(process.cwd() + '/');
const rec = { hono: JSON.parse(fs.readFileSync(process.cwd() + '/node_modules/hono/package.json', 'utf8')).version };
const { Hono } = await import('hono');
const url = await import('hono/utils/url').catch((e) => ({ err: String(e) }));
rec.crvj_getQueryParam = url.getQueryParam
  ? { afterFragment: url.getQueryParam('http://x/p#frag?a=1', 'a') ?? null, control_beforeFragment: url.getQueryParam('http://x/p?a=1#frag', 'a') ?? null }
  : { importError: url.err };
const app = new Hono();
app.get('/p', (c) => c.json({ a: c.req.query('a') ?? null }));
app.post('/b', async (c) => { const t0 = Date.now(); try { const b = await c.req.parseBody({ dot: true }); let d = 0, o = b; while (o && typeof o === 'object') { const k = Object.keys(o)[0]; o = o[k]; d++; } return c.json({ depth: d, ms: Date.now() - t0 }); } catch (e) { return c.json({ error: String(e).slice(0, 120) }, 500); } });
const { getRequestListener } = await import('@hono/node-server');
const srv = http.createServer(getRequestListener(app.fetch));
await new Promise((r) => srv.listen(0, '127.0.0.1', r));
const port = srv.address().port;
function raw(method, target, body, ctype) {
  return new Promise((resolve) => {
    const req = http.request({ host: '127.0.0.1', port, method, path: target, headers: body ? { 'content-type': ctype, 'content-length': Buffer.byteLength(body) } : {} }, (res) => {
      let d = ''; res.on('data', (x) => (d += x)); res.on('end', () => resolve({ status: res.statusCode, body: d.slice(0, 200) }));
    });
    req.on('error', (e) => resolve({ error: String(e) })); if (body) req.write(body); req.end();
  });
}
rec.crvj_nodeServer = { afterFragment: await raw('GET', '/p#frag?a=1'), control_plainQuery: await raw('GET', '/p?a=1') };
const deep = Array.from({ length: 5000 }, (_, i) => 'k' + i).join('.') + '=1';
rec.g6gw_parseBody = { depth5000: await raw('POST', '/b', deep, 'application/x-www-form-urlencoded'), control_depth3: await raw('POST', '/b', 'a.b.c=1', 'application/x-www-form-urlencoded') };
srv.closeAllConnections?.();
await new Promise((r) => srv.close(r));
rec.listenerClosed = true;
fs.writeFileSync(process.env.OUT, JSON.stringify(rec, null, 1));
