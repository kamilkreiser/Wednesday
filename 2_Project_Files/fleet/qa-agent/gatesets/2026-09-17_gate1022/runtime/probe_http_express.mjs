// probe_http_express.mjs — Probe B: the IMAGE's CMD entry (dist/http-server.js, express) started as a child on 127.0.0.1:0
// (MCP_HTTP_PORT=0 + loopback_pin preload), driven over real HTTP, ended by its own pid (SIGTERM), exit awaited.
import { spawn } from 'node:child_process';
import fs from 'node:fs';
const { CENSUS, PIN, CENSUS_OUT, CLOSED_PORT, OUT, ADDR_OUT } = process.env;
const child = spawn(process.execPath, ['--import', CENSUS, '--import', PIN, 'dist/http-server.js'], { cwd: process.cwd(),
  env: { ...process.env, CENSUS_OUT, ADDR_OUT, MCP_HTTP_PORT: '0', SECUURA_API_URL: `http://127.0.0.1:${CLOSED_PORT}` }, stdio: ['ignore', 'pipe', 'pipe'] });
let stderr = ''; child.stderr.on('data', (d) => { stderr += d; });
const t0 = Date.now(); while (!fs.existsSync(ADDR_OUT) && Date.now() - t0 < 15000) await new Promise((r) => setTimeout(r, 100));
const addr = JSON.parse(fs.readFileSync(ADDR_OUT, 'utf8'));
const rec = { probe: 'B express dist/http-server.js', childPid: child.pid, addr };
const base = `http://127.0.0.1:${addr.port}`;
async function hit(method, path, body, headers = { 'content-type': 'application/json' }) {
  const r = await fetch(base + path, { method, headers, body });
  const buf = Buffer.from(await r.arrayBuffer());
  const ct = r.headers.get('content-type') || '';
  let parsed; try { parsed = ct.includes('json') ? JSON.parse(buf.toString()) : { bytes: buf.length }; } catch { parsed = { unparsed: buf.toString().slice(0, 200) }; }
  return { status: r.status, contentType: ct, body: parsed };
}
rec.health = await hit('GET', '/health');
rec.hashContent = await hit('POST', '/hash', JSON.stringify({ content: Buffer.from('qa-1022').toString('base64'), fileName: 'x.txt' }));
rec.hashEmpty = await hit('POST', '/hash', JSON.stringify({}));
rec.hashNul = await hit('POST', '/hash', JSON.stringify({ content: 'a' + String.fromCharCode(0) + 'b' }));
rec.policyClosedApi = await hit('GET', '/policy');
rec.genBadType = await hit('POST', '/generate-package', JSON.stringify({ agentType: 'nope', apiKey: 'k' }));
rec.unknownRouteMcp = await hit('GET', '/mcp');
child.kill('SIGTERM');
const code = await new Promise((r) => child.on('exit', (c, s) => r({ code: c, signal: s })));
rec.exit = code; rec.stderr = stderr;
fs.writeFileSync(OUT, JSON.stringify(rec, null, 1));
