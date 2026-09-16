// dotseg_probe.js — PROBED, not the real originate app: does express (the farm's version) resolve dot segments when the
// v2 router mount and a /api/documents mount sit side by side, as in originate/src/index.ts :273/:277? Raw http.request paths.
const path = process.argv[2];
const express = require(path + '/express');
const http = require('http');
const app = express();
const v2 = express.Router();
v2.post('/verify', (req, res) => res.json({ hit: 'v2-verify', url: req.originalUrl }));
v2.post('/verify-file', (req, res) => res.json({ hit: 'v2-verify-file', url: req.originalUrl }));
app.use('/api/v2/verification', v2);
app.use('/api/documents', (req, res) => res.json({ hit: 'documents', url: req.originalUrl }));
app.use((req, res) => res.status(404).json({ hit: 'fallthrough-404', url: req.originalUrl }));
const srv = app.listen(0, '127.0.0.1', async () => {
  const port = srv.address().port;
  const rows = ['/api/v2/verification/verify', '/api/v2/verification/VERIFY', '/api/v2/verification/verify/', '/api/v2/verification/verify/x', '/api/v2/verification/verifyX',
    '/api/v2/verification/verify/../../../documents', '/api/v2/verification/verify/../../../api/documents', '/api/v2/verification/verify/%2e%2e/%2e%2e/%2e%2e/documents', '/api/documents'];
  console.log('express version', require(path + '/express/package.json').version, 'node', process.version);
  for (const p of rows) {
    const r = await new Promise((resolve) => { const q = http.request({ host: '127.0.0.1', port, path: p, method: 'POST', agent: false }, (res) => { let b = ''; res.on('data', (c) => b += c); res.on('end', () => resolve(res.statusCode + ' ' + b)); }); q.end(); });
    console.log(p.padEnd(62), r);
  }
  srv.close();
});
