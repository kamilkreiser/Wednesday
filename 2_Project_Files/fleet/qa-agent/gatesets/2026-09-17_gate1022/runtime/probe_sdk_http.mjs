// probe_sdk_http.mjs — Probe C: NOT a shipped entry. The SDK's StreamableHTTPServerTransport (the only SDK server module that imports
// @hono/node-server) serving an McpServer with the service's REAL compiled tools (dist/tools/*.js), on node:http 127.0.0.1:0, driven by the
// SDK's StreamableHTTPClientTransport. One process; the census covers server AND client modules. Then a positive control: import('hono').
import http from 'node:http';
import fs from 'node:fs';
import { McpServer } from '@modelcontextprotocol/sdk/server/mcp.js';
import { StreamableHTTPServerTransport } from '@modelcontextprotocol/sdk/server/streamableHttp.js';
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StreamableHTTPClientTransport } from '@modelcontextprotocol/sdk/client/streamableHttp.js';
const { OUT, SAMPLE, CENSUS_OUT } = process.env;
const dist = process.cwd() + '/dist/tools/';
const { registerHashTools } = await import(dist + 'hash.js');
const { registerRegisterTools } = await import(dist + 'register.js');
const { registerVerifyTools } = await import(dist + 'verify.js');
const { registerInfoTools } = await import(dist + 'info.js');
const srv = http.createServer(async (req, res) => {
  const server = new McpServer({ name: 'secuura', version: '1.0.0' });
  registerHashTools(server); registerRegisterTools(server); registerVerifyTools(server); registerInfoTools(server);
  const transport = new StreamableHTTPServerTransport({ sessionIdGenerator: undefined });
  res.on('close', () => { transport.close(); server.close(); });
  await server.connect(transport);
  let body = ''; for await (const ch of req) body += ch;
  await transport.handleRequest(req, res, body ? JSON.parse(body) : undefined);
});
await new Promise((r) => srv.listen(0, '127.0.0.1', r));
const step = (m) => process.stderr.write(`[C] ${m}\n`); step('listening');
const port = srv.address().port;
const rec = { probe: 'C SDK StreamableHTTP (not shipped)', pid: process.pid, addr: srv.address() };
const c = new Client({ name: 'qa-1022-drafter', version: '0' });
await c.connect(new StreamableHTTPClientTransport(new URL(`http://127.0.0.1:${port}/mcp`))); step('connected');
rec.serverVersion = c.getServerVersion();
rec.tools = (await c.listTools()).tools.map((x) => x.name); step('listed');
rec.callHash = await c.callTool({ name: 'secuura_hash_document', arguments: { filePath: SAMPLE } });
step('called'); await c.close(); step('client closed');
// a stateless GET opens a standalone SSE stream that never ends (drafter r1 hung here 120 s): read status + content-type, then abort.
const ac = new AbortController();
const raw = await fetch(`http://127.0.0.1:${port}/mcp?x=1`, { method: 'GET', headers: { accept: 'text/event-stream' }, signal: ac.signal });
rec.rawGetStateless = { status: raw.status, contentType: raw.headers.get('content-type') }; ac.abort(); step('raw status ' + raw.status + ', aborted');
srv.closeAllConnections?.();
await new Promise((r) => srv.close(r)); step('server closed');
fs.appendFileSync(CENSUS_OUT, '# ---- positive control: import(hono) ----\n');
const hono = await import('hono');
const app = new hono.Hono(); app.get('/q', (ctx) => ctx.text(String(ctx.req.query('a'))));
rec.honoControl = { exportsHono: typeof hono.Hono, query: await (await app.request('http://x/q?a=1')).text() };
fs.writeFileSync(OUT, JSON.stringify(rec, null, 1));
