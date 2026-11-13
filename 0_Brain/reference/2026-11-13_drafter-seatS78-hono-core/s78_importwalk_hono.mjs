// S78 drafter: import walk recording every resolved specifier; counts hits for `hono` (the package itself) and @hono/node-server separately.
import { register } from 'node:module';
import { pathToFileURL } from 'node:url';
const [, , base, ...entries] = process.argv;
const { port1, port2 } = new MessageChannel();
const seen = [];
port1.on('message', (m) => seen.push(m));
port1.unref();
register('data:text/javascript,' + encodeURIComponent(`
let port; export async function initialize(d){ port = d.port; }
export async function resolve(s, c, next){ const r = await next(s, c); port.postMessage(r.url); return r; }
`), { data: { port: port2 }, transferList: [port2] });
process.env.MCP_HTTP_PORT = '47911';
for (const e of entries) {
  const before = seen.length;
  const url = e.startsWith('/') ? pathToFileURL(e).href : pathToFileURL(base + '/' + e).href;
  try { await import(url); } catch (err) { console.log(e, 'IMPORT ERR', err.message.slice(0,100)); }
  await new Promise((r) => setTimeout(r, 300));
  const urls = seen.slice(before);
  const h = urls.filter((u) => /\/node_modules\/hono\//.test(u));
  const n = urls.filter((u) => u.includes('@hono/node-server'));
  console.log(`${e}: ${urls.length} modules, hono(pkg) hits=${h.length}, @hono/node-server hits=${n.length}`);
}
process.exit(0);
