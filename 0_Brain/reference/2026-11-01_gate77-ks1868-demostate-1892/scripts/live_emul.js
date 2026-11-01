// usage: node live_emul.js <base|head> <proxy|getter|plainstr|error>
const express = require('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate77-ks1868-demostate-1892/repo/Blockchain/Dev/node_modules/express');
const http = require('http');
const [,, variant, kind] = process.argv;
console.log('express', require('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate77-ks1868-demostate-1892/repo/Blockchain/Dev/node_modules/express/package.json').version, 'node', process.version);
const inMemoryState = { currentPersona: null, presenterMode: false, scenarioStep: 0 };
function thrown() {
  if (kind === 'proxy') { const {proxy, revoke} = Proxy.revocable({}, {}); revoke(); return proxy; }
  if (kind === 'getter') return Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } });
  if (kind === 'plainstr') return 'a string';
  return new Error('redis boom');
}
const logs = [];
const logger = { error: (...a) => logs.push(a) };
const app = express();
app.get('/state', async (_req, res) => {
  try { throw thrown(); }
  catch (err) {
    let message;
    if (variant === 'base') { message = err instanceof Error ? err.message : 'Unknown error'; }
    else { try { message = err instanceof Error ? err.message : 'Unknown error'; } catch { message = 'unreadable thrown value'; } }
    logger.error('Failed to read demo state', { error: message });
    return res.json(inMemoryState);
  }
});
app.use((err, _req, res, _next) => { console.log('ERROR MIDDLEWARE REACHED'); res.status(500).json({e:1}); });
process.on('exit', (c) => console.log('process exit code', c, 'logs', JSON.stringify(logs)));
const srv = app.listen(0, () => {
  const port = srv.address().port;
  const t = setTimeout(() => { console.log('RESULT: NO RESPONSE after 3000ms (hang)'); process.exit(0); }, 3000);
  http.get({ port, path: '/state' }, (r) => { let b=''; r.on('data', d=>b+=d); r.on('end', () => { clearTimeout(t); console.log('RESULT: HTTP', r.statusCode, b); process.exit(0); }); }).on('error', (e) => { console.log('RESULT: socket error', e.code); });
});
