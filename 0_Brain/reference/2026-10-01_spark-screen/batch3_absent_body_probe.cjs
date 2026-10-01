// Replica probe (scratch only): express 4 + express.json() + each handler's FIRST body gate, byte-copied from develop 0736d8b7.
const express = require('express'); const { z } = require('zod'); const http = require('http');
console.log('express', require('express/package.json').version, 'body-parser', require('body-parser/package.json').version, 'zod', require('zod/package.json').version);
// referral routes/referrals.ts:16-21
const generateCodeSchema = z.object({
  customCode: z.string().trim().min(4).max(16).optional(),
  maxUses: z.number().int().min(1).max(10000).optional(),
  expiresInDays: z.number().int().min(1).max(365).optional(),
  customLabel: z.string().trim().max(100).optional(),
});
// tenant-provisioning index.ts:431-438
const updateTenantSchema = z.object({
  name: z.string().trim().min(1).max(255).optional(),
  domain: z.string().trim().optional(),
  industry: z.string().trim().optional(),
  country: z.string().trim().optional(),
  test_url: z.string().url().optional().or(z.literal('')).or(z.null()),
  live_url: z.string().url().optional().or(z.literal('')).or(z.null()),
});
// POSITIVE CONTROL: a schema with a required field (billing PurchaseCustomSchema-like) must refuse {}
const controlSchema = z.object({ quantity: z.number() });
const app = express(); app.use(express.json({ limit: '1mb' }));
app.post('/generate', (req, res) => { try { generateCodeSchema.parse(req.body); return res.status(201).json({ gate: 'passed -> referralService.generateCode', body: req.body }); } catch (e) { return res.status(400).json({ zod: true }); } });
app.patch('/tenant', (req, res) => { try { const body = updateTenantSchema.parse(req.body); const sets = Object.entries(body).filter(([, v]) => v !== undefined); if (sets.length === 0) return res.status(400).json({ message: 'No fields to update' }); return res.status(200).json({ gate: 'passed' }); } catch (e) { return res.status(400).json({ zod: true }); } });
app.post('/v2verify', (req, res) => { const { documentId, hash, providedHash, contentHash, documentHash, documentData } = req.body || {}; const h = hash || providedHash || contentHash || documentHash; if (!documentId && !h && !documentData) return res.status(400).json({ message: 'Provide a content hash' }); return res.status(200).json({ gate: 'passed' }); });
app.post('/control', (req, res) => { try { controlSchema.parse(req.body); return res.status(201).json({}); } catch (e) { return res.status(400).json({ zod: true }); } });
app.use((err, req, res, next) => res.status(err.status || 500).json({ parserError: err.type }));
const srv = app.listen(0, async () => {
  const port = srv.address().port;
  const send = (method, path, body, ctype) => new Promise((r) => { const h = {}; if (ctype) h['content-type'] = ctype; if (body !== undefined) h['content-length'] = Buffer.byteLength(body); const q = http.request({ port, method, path, headers: h }, (s) => { let d = ''; s.on('data', (c) => d += c); s.on('end', () => r(s.statusCode + ' ' + d)); }); if (body !== undefined) q.write(body); q.end(); });
  for (const [m, p] of [['POST', '/control'], ['POST', '/generate'], ['PATCH', '/tenant'], ['POST', '/v2verify']]) {
    console.log(m, p, '| ABSENT (no body, no content-type):', await send(m, p));
    console.log(m, p, '| ABSENT (content-type json, length 0):', await send(m, p, '', 'application/json'));
    console.log(m, p, '| body null (json):', await send(m, p, 'null', 'application/json'));
    console.log(m, p, '| body {} (json):', await send(m, p, '{}', 'application/json'));
  }
  srv.close();
});
