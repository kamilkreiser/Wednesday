// Gate 85: what does an Express 4 async handler's rejection do in a plain Node process with NO unhandledRejection
// listener (the kyc service registers none) and no --unhandled-rejections flag (Dockerfile CMD node dist/index.js)?
const express = require('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900/repo/Blockchain/Dev/node_modules/express');
const http = require('http');
console.log('node', process.version, 'express', require('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate85-ks1868-kyc-1900/repo/Blockchain/Dev/node_modules/express/package.json').version, 'unhandledRejection listeners', process.listenerCount('unhandledRejection'));
const app = express();
app.get('/health', async (_req, res) => { await Promise.reject(new TypeError('stand-in for the helper catch rethrow')); res.json({ ok: true }); });
app.get('/ok', (_req, res) => res.json({ ok: true }));
process.on('exit', (c) => console.log('process exit code', c));
const srv = app.listen(0, '127.0.0.1', () => {
  const port = srv.address().port;
  http.get(`http://127.0.0.1:${port}/ok`, (r) => { console.log('/ok status', r.statusCode); r.resume();
    const req = http.get(`http://127.0.0.1:${port}/health`, (r2) => console.log('/health status', r2.statusCode));
    req.on('error', (e) => console.log('/health request error', e.code));
    setTimeout(() => { console.log('still alive after 1.5s'); process.exit(0); }, 1500);
  });
});
