/**
 * qa1034-hang-harness (TEMPLATE) — QA DRAFTER harness for #1034's cache-get-throws LEAD, run OUT OF vitest as a real node process (tsx), so the gateway's
 * own unhandledRejection handler and gracefulShutdown (index.ts:1151-1189) act for real instead of vitest intercepting process.exit.
 * Written by drafter_hang_1034.py to <tree>/Blockchain/Dev/qa_hang_1034/ (OUTSIDE services/api-gateway). __GW_SRC__ = the tree's api-gateway src.
 * It: provisions an RS256 keypair (as vitest.setup.ts), starts ONE loopback recorder (key validate: valid for sk_qa1034h_*; exchange: OK), points every
 * *_SERVICE_URL at it, requires the REAL index.ts app (require.main !== module, so it does not listen itself), serves it on 127.0.0.1:0, and patches
 * connectorBearerCache.get to THROW for keys containing `_cachethrow_` (the fault injection the seat used — an INSTRUMENT, not a request-reachable
 * state). Every patched-get call prints a line (same-instance control). Prints READY <json> with the port; prints EXIT <code> on process exit.
 */
const http = require('http');
const crypto = require('crypto');
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
process.env.JWT_PUBLIC_KEY = Buffer.from(publicKey.export({ type: 'spki', format: 'pem' }).toString()).toString('base64');
const PRIV = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
process.on('exit', (code: number) => { process.stdout.write(`EXIT ${code} at ${new Date().toISOString()}\n`); });
function readBody(req: any): Promise<string> { return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d: Buffer) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); }); }
let upstreamHits = 0;
const recorder = http.createServer(async (req: any, res: any) => {
  const body = await readBody(req); const url = req.url || '';
  const json = (st: number, p: unknown) => { res.writeHead(st, { 'content-type': 'application/json' }); res.end(JSON.stringify(p)); };
  if (url === '/api/keys/validate') {
    const key = String(JSON.parse(body || '{}').key || '');
    return json(200, key.startsWith('sk_qa1034h_') ? { data: { valid: true, connectorId: 'qa1034h', scopes: ['*'], organizationId: 'org-qa1034h', tenantId: 'a0000000-0000-4000-8000-000000000001', rateLimit: 100000, rateLimitWindow: 60 } } : { data: { valid: false } });
  }
  if (url === '/internal/connector-token') {
    const jwt = require('jsonwebtoken');
    return json(200, { success: true, data: { token: jwt.sign({ userId: 'connector:qa1034h', role: 'connector', type: 'connector' }, PRIV, { algorithm: 'RS256', expiresIn: 600 }), expiresIn: 600 } });
  }
  if (url.startsWith('/.well-known/')) return json(404, {});
  upstreamHits++; process.stdout.write(`UPSTREAM-HIT ${upstreamHits} ${req.method} ${url}\n`);
  return json(200, { success: true, data: { recorder: true } });
});
recorder.listen(0, '127.0.0.1', () => {
  const rurl = `http://127.0.0.1:${recorder.address().port}`;
  for (const s of ['ANALYTICS', 'ANCHORING', 'AUTH', 'BILLING', 'GOVERNANCE', 'KYC', 'NFT', 'NOTIFICATION', 'ORIGINATE', 'PRISM', 'REFERRAL', 'SECURITY', 'STAKING', 'TIMESTAMPING', 'TRANSFER', 'VC_ISSUER', 'WALLET']) process.env[`${s}_SERVICE_URL`] = rurl;
  process.env.GATEWAY_VOUCH_SECRET = '';
  const app = require('__GW_SRC__/index.ts').default;
  const auth = require('__GW_SRC__/middleware/auth.ts');
  const cache = auth.connectorBearerCache; const realGet = cache.get;
  Object.defineProperty(cache, 'get', { configurable: true, writable: true, value: function (this: any, k: string) {
    process.stdout.write(`PATCHED-GET ${k.includes('_cachethrow_') ? 'cachethrow' : 'ok'}\n`);
    if (k.includes('_cachethrow_')) throw new Error('qa1034 instrument: connectorBearerCache.get threw');
    return realGet.call(this, k);
  } });
  const server = http.createServer(app);
  server.listen(0, '127.0.0.1', () => {
    process.stdout.write('READY ' + JSON.stringify({ port: server.address().port, recorderPort: recorder.address().port, pid: process.pid, nodeEnv: process.env.NODE_ENV, mode: process.env.UNHANDLED_REJECTION_MODE ?? '(unset)' }) + '\n');
  });
});
