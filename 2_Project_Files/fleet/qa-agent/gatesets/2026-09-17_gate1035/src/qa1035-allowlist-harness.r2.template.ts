/**
 * qa1035-allowlist-harness (TEMPLATE, r2: per-step Content-Type + client timeout) — QA RE-DRAFTER instrument (derived from the dead drafter's template by asserted substitutions) for #1035 (KS-1204), run OUT OF vitest as a real node process (tsx), so the REAL index.ts
 * app with its REAL mount order (versioning -> csrf -> content-type -> ... -> createHealthRoutes -> createAdminRoutes -> createVerificationRoutes), its REAL
 * services/redis.ts in-memory fallback, the REAL PUT /api/admin/settings writer and the REAL POST /api/documents create route all act for real.
 * Written by drafter_probe_1035.py to <tree>/Blockchain/Dev/qa_probe_1035/ (OUTSIDE services/api-gateway). __GW_SRC__ = the tree's api-gateway src.
 * One loopback recorder (127.0.0.1:0) answers security /api/keys/validate (sk_qa1035_<connectorId> -> valid), auth /internal/connector-token (an RS256
 * connector JWT signed by a keypair generated here, JWT_PUBLIC_KEY set before the app loads, as vitest.setup.ts does) and COUNTS every other request
 * (originate POST /api/documents = a FORWARD). The app is served on 127.0.0.1:0. The plan comes from QA_PLAN, rows go to QA_ROWS. Never a secret:
 * the keypair and every token exist only inside this process.
 */
const http = require('http');
const fs = require('fs');
const crypto = require('crypto');
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
process.env.JWT_PUBLIC_KEY = Buffer.from(publicKey.export({ type: 'spki', format: 'pem' }).toString()).toString('base64');
const PRIV = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
process.on('exit', (code: number) => { process.stdout.write(`EXIT ${code} at ${new Date().toISOString()}\n`); });
const jwt = require('jsonwebtoken');
function readBody(req: any): Promise<string> { return new Promise((r) => { const c: Buffer[] = []; req.on('data', (d: Buffer) => c.push(d)); req.on('end', () => r(Buffer.concat(c).toString())); }); }
const seen: Array<{ method: string; url: string; body: string }> = [];
const recorder = http.createServer(async (req: any, res: any) => {
  const body = await readBody(req); const url = req.url || '';
  const json = (st: number, p: unknown) => { res.writeHead(st, { 'content-type': 'application/json' }); res.end(JSON.stringify(p)); };
  if (url === '/api/keys/validate') {
    const key = String(JSON.parse(body || '{}').key || '');
    if (!key.startsWith('sk_qa1035_')) return json(200, { data: { valid: false } });
    return json(200, { data: { valid: true, connectorId: key.slice('sk_qa1035_'.length), scopes: ['documents:write'], organizationId: 'org-qa1035', tenantId: 'a0000000-0000-4000-8000-000000000001', rateLimit: 1000000, rateLimitWindow: 60 } });
  }
  if (url === '/internal/connector-token') {
    const k = String(JSON.parse(body || '{}').apiKey || ''); const id = k.slice('sk_qa1035_'.length);
    return json(200, { success: true, data: { token: jwt.sign({ userId: `connector:${id}`, email: 'connector@secuura.io', role: 'connector', verificationLevel: 'api_key', type: 'connector', tenantId: 'a0000000-0000-4000-8000-000000000001', scopes: ['documents:write'] }, PRIV, { algorithm: 'RS256', expiresIn: 3600 }), expiresIn: 3600 } });
  }
  if (url.startsWith('/.well-known/')) return json(404, {});
  seen.push({ method: req.method || '', url, body });
  if (req.method === 'POST' && url === '/api/documents') return json(201, { success: true, data: { id: 'doc-qa1035', recorder: 'originate' } });
  return json(404, { success: false });
});
function send(port: number, method: string, path: string, headers: Record<string, string>, body?: string, ctype = 'application/json', tmo = 4000): Promise<{ status: number; code: string | null; msg: string | null; text: string; json: any }> {
  return new Promise((resolve) => {
    const h: Record<string, string> = { ...headers };
    if (body !== undefined) { h['content-type'] = ctype; h['content-length'] = String(Buffer.byteLength(body)); }
    const r = http.request({ hostname: '127.0.0.1', port, path, method, headers: h, agent: false }, (res: any) => {
      const c: Buffer[] = []; res.on('data', (d: Buffer) => c.push(d));
      res.on('end', () => { const text = Buffer.concat(c).toString(); let j: any = null; try { j = JSON.parse(text); } catch { /* text kept */ }
        resolve({ status: res.statusCode || 0, code: j?.error?.code ?? j?.code ?? null, msg: j?.error?.message ?? j?.message ?? null, text: text.slice(0, 400), json: j }); });
    });
    r.on('error', (e: Error) => resolve({ status: 0, code: 'QA_CLIENT_ERROR ' + e.message.slice(0, 60), msg: null, text: '', json: null }));
    r.setTimeout(tmo, () => { r.destroy(); resolve({ status: 0, code: 'QA_CLIENT_TIMEOUT_' + tmo + 'MS', msg: null, text: '', json: null }); });
    if (body !== undefined) r.end(body); else r.end();
  });
}
/** frontend/admin/src/pages/Settings.tsx :30-43 (load) + :58-73 (handleSave grouping), transcribed verbatim as data transforms — a PROBED emulation, not the React page. */
function portalSettingsSave(loaded: Record<string, any>, edits: Record<string, unknown>): Record<string, Record<string, unknown>> {
  const initialValues: Record<string, unknown> = {};
  Object.keys(loaded).forEach((category) => { Object.keys(loaded[category] || {}).forEach((key) => { initialValues[`${category}.${key}`] = loaded[category][key]; }); });
  const formValues: Record<string, unknown> = { ...initialValues, ...edits };
  const updates: Record<string, Record<string, unknown>> = {};
  Object.keys(formValues).forEach((key) => { const [category, field] = key.split('.'); if (!updates[category]) { updates[category] = {}; } updates[category][field] = formValues[key]; });
  return updates;
}
recorder.listen(0, '127.0.0.1', async () => {
  const rurl = `http://127.0.0.1:${recorder.address().port}`;
  for (const s of ['ANALYTICS', 'ANCHORING', 'AUTH', 'BILLING', 'GOVERNANCE', 'KYC', 'NFT', 'NOTIFICATION', 'ORIGINATE', 'PRISM', 'REFERRAL', 'SECURITY', 'STAKING', 'TIMESTAMPING', 'TRANSFER', 'VC_ISSUER', 'WALLET']) process.env[`${s}_SERVICE_URL`] = rurl;
  process.env.GATEWAY_VOUCH_SECRET = '';
  const app = require('__GW_SRC__/index.ts').default;
  const redis = require('__GW_SRC__/services/redis.ts');
  const server = http.createServer(app);
  server.listen(0, '127.0.0.1', async () => {
    const port = server.address().port;
    process.stdout.write('READY ' + JSON.stringify({ port, recorderPort: recorder.address().port, pid: process.pid, nodeEnv: process.env.NODE_ENV, mode: process.env.UNHANDLED_REJECTION_MODE ?? '(unset)', redisAvailable: redis.isRedisAvailable() }) + '\n');
    const plan = JSON.parse(fs.readFileSync(process.env.QA_PLAN as string, 'utf8'));
    const pre = process.env.NODE_ENV === 'production' ? '/api/v1' : '/api';
    const tok = (role: string, extra: Record<string, unknown> = {}) => jwt.sign({ userId: `qa-${role}`, email: `${role}@qa.invalid`, role, verificationLevel: 'government', tenantId: 'a0000000-0000-4000-8000-000000000001', ...extra }, PRIV, { algorithm: 'RS256', expiresIn: 3600 });
    const out: any = { meta: { pre, nodeEnv: process.env.NODE_ENV, redisAvailable: redis.isRedisAvailable() }, admin: [], rows: [] };
    const admin = { authorization: `Bearer ${tok('SYSTEM_ADMIN')}` };
    const seed = await send(port, 'GET', pre + '/admin/document-types', admin);
    const cat = (await redis.getAllDocumentTypes()) as any[];
    out.meta.seed = { status: seed.status, catalogue: cat.map((t) => t.code) };
    const T = (o: any) => JSON.stringify({ title: 'qa1035', contentHash: 'b'.repeat(64), ...o });
    async function create(connectorId: string, raw: string, path?: string, ctype?: string, tmo?: number) {
      const s0 = seen.length;
      const r = await send(port, 'POST', path || (pre + '/documents'), { 'x-api-key': 'sk_qa1035_' + connectorId }, raw, ctype || 'application/json', tmo || 4000);
      const fwd = seen.slice(s0).filter((x) => x.method === 'POST' && x.url === '/api/documents');
      const m = r.msg || '';
      const layer = /^Connector is not permitted to register document type "/.test(m) ? 'ALLOWLIST-MEMBER-403'
        : m === 'Connector document-type allow-list is not a list; refusing until it is corrected' ? 'ALLOWLIST-NONARRAY-403'
        : fwd.length ? 'FORWARDED' : r.status === 0 ? 'NO-RESPONSE' : 'OTHER';
      return { status: r.status, code: r.code, msg: m.slice(0, 160), layer, location: r.status === 307 ? 'see text' : undefined, forwarded: fwd.length, forwarded_body_identical: fwd.length ? fwd[0].body === raw : null, text: r.status >= 500 || r.status === 0 ? r.text.slice(0, 200) : undefined };
    }
    for (const step of plan.steps) {
      if (step.kind === 'put') {
        const h = step.as === 'none' ? {} : { authorization: `Bearer ${tok(step.as)}` };
        const r = await send(port, 'PUT', pre + '/admin/settings', h, JSON.stringify(step.body));
        const stored = (await redis.getNotificationSettings('platform-settings')) as any;
        const ints = stored?.integrations;
        out.admin.push({ label: step.label, as: step.as, status: r.status, code: r.code, stored_integrations_type: ints === undefined ? 'undefined' : ints === null ? 'null' : Array.isArray(ints) ? 'array' : typeof ints,
          stored_allow_shapes: Array.isArray(ints) ? ints.map((i: any) => i && i.config && typeof i.config === 'object' ? (Array.isArray(i.config.allowedDocumentTypes) ? 'array' : i.config.allowedDocumentTypes === null ? 'null' : typeof i.config.allowedDocumentTypes) : 'no-config-object') : null,
          echoed_success: r.json?.success ?? null });
      } else if (step.kind === 'portal-roundtrip') {
        const g = await send(port, 'GET', pre + '/admin/settings', admin);
        const updates = portalSettingsSave(g.json?.settings || {}, step.edits || {});
        const p = await send(port, 'PUT', pre + '/admin/settings', admin, JSON.stringify(updates));
        const stored = (await redis.getNotificationSettings('platform-settings')) as any;
        const ints = stored?.integrations;
        out.admin.push({ label: step.label, as: 'SYSTEM_ADMIN via Settings.tsx transform', get_status: g.status, put_status: p.status, sent_integrations_type: Array.isArray(updates.integrations) ? 'array' : typeof updates.integrations,
          sent_integrations_keys: updates.integrations ? Object.keys(updates.integrations) : null, stored_integrations_type: ints === undefined ? 'undefined' : Array.isArray(ints) ? 'array' : typeof ints });
      } else if (step.kind === 'create') {
        const r = await create(step.connector, step.raw ?? T(step.body), step.path, step.ctype, step.tmo);
        out.rows.push({ group: step.group, config_label: step.config_label, connector: step.connector, shape: step.shape, path: step.path || (pre + '/documents'), ctype: step.ctype || 'application/json', ...r });
      } else if (step.kind === 'info') {
        const r = await send(port, 'GET', pre + '/connector/info', { 'x-api-key': 'sk_qa1035_' + step.connector });
        out.rows.push({ group: 'info', config_label: step.config_label, connector: step.connector, shape: 'GET /api/connector/info', status: r.status, info_allowedDocumentTypes: r.json?.allowedDocumentTypes === undefined ? '(absent)' : r.json.allowedDocumentTypes });
      }
    }
    out.meta.unmatched_recorder = seen.filter((x) => !(x.method === 'POST' && x.url === '/api/documents')).map((x) => x.method + ' ' + x.url).slice(0, 20);
    fs.writeFileSync(process.env.QA_ROWS as string, JSON.stringify(out, null, 1));
    process.stdout.write('DONE rows ' + out.rows.length + ' admin ' + out.admin.length + '\n');
  });
});
