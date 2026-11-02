// Probe: DefaultAzureCredential (no options, exactly as key-vault.ts:190) on the Container Apps
// managed-identity shape (IDENTITY_ENDPOINT + IDENTITY_HEADER) against a 127.0.0.1 stand-in.
// argv[2] = node_modules dir holding @azure/identity; argv[3] = label
const http = require('http'); const path = require('path');
const nm = process.argv[2], label = process.argv[3];
for (const k of Object.keys(process.env)) if (/^(AZURE_|IDENTITY_|MSI_|IMDS_|ARM_)/.test(k)) delete process.env[k];
const seen = [];
const srv = http.createServer((req, res) => {
  seen.push({ method: req.method, url: req.url.replace(/[?&]client_id=[^&]*/, ''), hdr: req.headers['x-identity-header'] ? 'x-identity-header:set' : 'x-identity-header:absent' });
  res.setHeader('content-type', 'application/json');
  const exp = Math.floor(Date.now() / 1000) + 3600;
  res.end(JSON.stringify({ access_token: 'stand-in-token-' + label, expires_on: String(exp), resource: 'https://vault.azure.net', token_type: 'Bearer' }));
});
srv.listen(0, '127.0.0.1', async () => {
  const port = srv.address().port;
  process.env.IDENTITY_ENDPOINT = `http://127.0.0.1:${port}/msi/token`;
  process.env.IDENTITY_HEADER = 'stand-in-header';
  const idPkg = require(path.join(nm, '@azure/identity/package.json'));
  const msalPkg = require(require.resolve('@azure/msal-node/package.json', { paths: [path.dirname(require.resolve('@azure/identity', { paths: [nm] }))] }));
  const { DefaultAzureCredential } = require(require.resolve('@azure/identity', { paths: [nm] }));
  const out = { label, identity: idPkg.version, msalNode: msalPkg.version };
  try {
    const cred = new DefaultAzureCredential();
    const t = await cred.getToken('https://vault.azure.net/.default');
    out.result = 'token'; out.tokenMatches = t.token === 'stand-in-token-' + label; out.expiresInS = Math.round((t.expiresOnTimestamp - Date.now()) / 1000);
    const t2 = await cred.getToken('https://vault.azure.net/.default');
    out.secondCall = t2.token === t.token ? 'same token' : 'different';
  } catch (e) { out.result = 'error'; out.errorName = e && e.name; out.errorMessage = String(e && e.message).slice(0, 300); }
  out.requests = seen;
  console.log(JSON.stringify(out, null, 1));
  srv.close(); process.exit(0);
});
