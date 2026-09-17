// probe_stdio.mjs — Probe A: the SHIPPED stdio entry (dist/index.js, `npm start`) driven by the SDK's own Client over StdioClientTransport.
// Runs with cwd = img-<tree>/prod so bare specifiers resolve to that tree's runtime node_modules. The server child gets the census preload.
import { Client } from '@modelcontextprotocol/sdk/client/index.js';
import { StdioClientTransport } from '@modelcontextprotocol/sdk/client/stdio.js';
import fs from 'node:fs';
const { CENSUS, CENSUS_OUT, CLOSED_PORT, SAMPLE, OUT } = process.env;
const rec = { probe: 'A stdio dist/index.js' };
const t = new StdioClientTransport({ command: process.execPath, args: ['--import', CENSUS, 'dist/index.js'], cwd: process.cwd(),
  env: { ...process.env, CENSUS_OUT, SECUURA_API_URL: `http://127.0.0.1:${CLOSED_PORT}` }, stderr: 'pipe' });
let stderr = ''; t.stderr?.on('data', (d) => { stderr += d; });
const c = new Client({ name: 'qa-1022-drafter', version: '0' });
await c.connect(t);
rec.serverPid = t.pid;
rec.serverVersion = c.getServerVersion(); rec.capabilities = c.getServerCapabilities();
const tools = await c.listTools();
rec.tools = tools.tools.map((x) => ({ name: x.name, inputSchema: x.inputSchema }));
rec.callHash = await c.callTool({ name: 'secuura_hash_document', arguments: { filePath: SAMPLE } });
rec.callConnectorInfoClosedApi = await c.callTool({ name: 'secuura_get_connector_info', arguments: {} });
try { rec.callUnknown = await c.callTool({ name: 'no_such_tool', arguments: {} }); } catch (e) { rec.callUnknown = { thrown: String(e.message) }; }
try { rec.callBadArgs = await c.callTool({ name: 'secuura_hash_document', arguments: { filePath: 42 } }); } catch (e) { rec.callBadArgs = { thrown: String(e.message) }; }
await c.close();
await new Promise((r) => setTimeout(r, 300));
let alive = true; try { process.kill(rec.serverPid, 0); } catch { alive = false; }
rec.serverAliveAfterClose = alive; rec.serverStderr = stderr;
fs.writeFileSync(OUT, JSON.stringify(rec, null, 1));
