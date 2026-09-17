// express_route_probe.js — PROBED (not originate itself): does express 4 (the farm's copy, the version originate's routes run on — READ its package.json
// separately) route the W-class raw targets to a router shaped like originate's gdprRouter (`app.use('/api/gdpr', r)`; r.get('/erasures/:externalRef'),
// r.post('/erasures'), r.get('/consent/check'))? Listener on 127.0.0.1:0, closed at the end. Prints the handler reached and req.params per target.
const express = require('express'); const http = require('http');
const app = express(); const r = express.Router();
r.get('/erasures/:externalRef', (req, res) => res.json({ h: 'GET /erasures/:externalRef', params: req.params }));
r.post('/erasures', (req, res) => res.json({ h: 'POST /erasures' }));
r.get('/consent/check', (req, res) => res.json({ h: 'GET /consent/check' }));
app.use('/api/gdpr', r);
app.use((req, res) => res.status(404).json({ h: null }));
const T = [['GET', '/api/gdpr/erasures/..'], ['GET', '/api/gdpr/erasures/%2e%2e'], ['GET', '/api/gdpr/erasures/..;x'], ['GET', '/api/gdpr/erasures/%2e%2e%2fabc'],
  ['GET', '/api/gdpr/erasures/.%2e'], ['POST', '/api/gdpr/erasures/..'], ['GET', '/api/gdpr/erasures/abc'], ['POST', '/api/gdpr/erasures'], ['POST', '/api/gdpr/%65rasures'],
  ['POST', '/api/gdpr/./erasures'], ['POST', '/api/gdpr/erasures;x=1'], ['POST', '/api/gdpr/ERASURES'], ['GET', '/api/gdpr/ERASURES/abc'], ['POST', '/api/gdpr/x/../erasures']];
const srv = http.createServer(app).listen(0, '127.0.0.1', async () => {
  const port = srv.address().port; console.log('express', require('express/package.json').version, 'listening 127.0.0.1:' + port, 'pid', process.pid);
  for (const [m, p] of T) {
    await new Promise((done) => { const q = http.request({ host: '127.0.0.1', port, method: m, path: p, agent: false }, (res) => { let b = ''; res.on('data', (d) => b += d); res.on('end', () => { console.log(m, p, '->', res.statusCode, b); done(); }); }); q.on('error', (e) => { console.log(m, p, 'ERR', String(e)); done(); }); q.end(); });
  }
  srv.close(() => console.log('closed'));
});
