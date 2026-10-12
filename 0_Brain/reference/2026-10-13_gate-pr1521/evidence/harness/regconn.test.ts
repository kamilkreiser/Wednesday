import { it, expect } from 'vitest';
import crypto from 'crypto';
import fs from 'fs';
process.env.SECURITY_DISABLE_BOOT = '1'; delete process.env.DATABASE_URL;
const TA = 'a0000000-0000-4000-8000-0000000000aa';
const { privateKey, publicKey } = crypto.generateKeyPairSync('rsa', { modulusLength: 2048 });
const PRIV = privateKey.export({ type: 'pkcs8', format: 'pem' }).toString();
const b64u = (b: Buffer) => b.toString('base64').replace(/\+/g, '-').replace(/\//g, '_').replace(/=+$/, '');
const tok = (c: object) => { const h = b64u(Buffer.from('{"alg":"RS256","typ":"JWT"}')); const n = Math.floor(Date.now()/1000);
  const p = b64u(Buffer.from(JSON.stringify({ sub: 'g', iat: n, exp: n + 600, ...c }))); return `${h}.${p}.${b64u(crypto.sign('RSA-SHA256', Buffer.from(`${h}.${p}`), PRIV))}`; };
// S_CONNECTOR_SCOPES and body shape copied from api-gateway/src/routes/platform.ts:487-711
const SC = ['documents:write','documents:read','documents:share','documents:revoke','documents:transfer-custody','certifications:write','anchors:read','anchors:write','subjects:erase'];
it('register-connector mint body, per bearer kind requireOrgProvisioner admits', async () => {
  process.env.JWT_PUBLIC_KEY = Buffer.from(publicKey.export({ type: 'spki', format: 'pem' }).toString()).toString('base64');
  delete process.env.JWT_JWKS_URL; delete process.env.AUTH_SERVICE_URL;
  const mod: any = await import('../index');
  const srv: any = await new Promise((r) => { const s = mod.default.listen(0, '127.0.0.1', () => r(s)); });
  const base = `http://127.0.0.1:${srv.address().port}`;
  const bearers: Record<string, object> = {
    super_admin: { role: 'super_admin' }, SUPER_ADMIN: { role: 'SUPER_ADMIN' }, SYSTEM_ADMIN: { role: 'SYSTEM_ADMIN' }, platform_admin: { role: 'platform_admin', tenantId: TA },
    provisioner: { role: 'connector', type: 'connector', tenantId: TA, organizationId: '99999999-9999-4999-8999-999999999999', scopes: ['organizations:register'] },
  };
  const res: any[] = [];
  for (const [n, c] of Object.entries(bearers)) for (const rotate of [false, true]) {
    if (n === 'provisioner' && rotate) continue; // gateway Guardrail 1 refuses before the mint
    const org = crypto.randomUUID(); const ref = `ref-${n}-${rotate}`;
    if (rotate) await fetch(`${base}/api/keys`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${tok(bearers.super_admin)}` },
      body: JSON.stringify({ name: 'prior', organizationId: org, tenantId: TA, scopes: SC, connectorId: `platform-s:${ref}` }) });
    const r = await fetch(`${base}/api/keys`, { method: 'POST', headers: { 'Content-Type': 'application/json', Authorization: `Bearer ${tok(c)}` },
      body: JSON.stringify({ name: `Platform S connector — ${ref}`, organizationId: org, tenantId: TA, scopes: SC, connectorId: `platform-s:${ref}`, rotate }) });
    const j: any = await r.json();
    res.push({ bearer: n, rotate, status: r.status, priorKeysRevoked: j?.data?.priorKeysRevoked, msg: j?.error?.message });
  }
  fs.writeFileSync(process.env.GATE_OUT!, JSON.stringify(res, null, 1));
  srv.close(); expect(res.length).toBe(9);
});
