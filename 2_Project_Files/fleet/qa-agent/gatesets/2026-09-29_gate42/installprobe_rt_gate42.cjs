// installprobe_rt_gate42.cjs <install dir> — the drafter's LOAD SMOKE for the runtime-moved packages of KS-1379 inside ONE standalone
// `npm ci --ignore-scripts` (services/queue, services/m365-integration, packages/shared). Prints ONE JSON line. Nothing connects: msgpackr packs and
// unpacks in memory; bullmq is required (no Queue is constructed — that would dial Redis); msal-node's ConfidentialClientApplication and
// @azure/identity's ClientSecretCredential are CONSTRUCTED only (no token is requested).
const path = require('path');
const dir = process.argv[2]; const has = (m) => { try { require.resolve(m, { paths: [dir] }); return true; } catch (e) { return false; } };
const req = (m) => require(require.resolve(m, { paths: [dir] }));
const fs = require('fs');
// the version from the package's OWN package.json found by walking up from its resolved entry (an `exports` map may refuse `<m>/package.json`)
const pkgver = (entry, m) => { let d = path.dirname(entry); while (d !== path.dirname(d)) { const f = path.join(d, 'package.json'); if (fs.existsSync(f)) { try { const j = JSON.parse(fs.readFileSync(f, 'utf8')); if (j.name === m) return j.version; } catch (e) {} } d = path.dirname(d); } return null; };
const ver = (m) => { try { return pkgver(require.resolve(m, { paths: [dir] }), m); } catch (e) { return null; } };
const verFrom = (m, fromPkg) => { try { return pkgver(require.resolve(m, { paths: [path.dirname(require.resolve(fromPkg, { paths: [dir] }))] }), m); } catch (e) { return null; } };
const out = { dir: path.basename(dir), node: process.version, checks: {} };
try {
  if (has('msgpackr')) {
    const { pack, unpack } = req('msgpackr'); const v = { a: 1, s: 'secuura', arr: [1, 2, 3], nested: { d: new Date(0).toISOString() } };
    out.checks.msgpackr = { version: ver('msgpackr'), roundtrip: JSON.stringify(unpack(pack(v))) === JSON.stringify(v) };
  }
  if (has('bullmq')) { const b = req('bullmq'); out.checks.bullmq = { version: ver('bullmq'), Queue: typeof b.Queue, Worker: typeof b.Worker,
    msgpackr_seen_by_bullmq: verFrom('msgpackr', 'bullmq') }; }
  if (has('@azure/identity')) {
    const id = req('@azure/identity'); const c = new id.ClientSecretCredential('00000000-0000-0000-0000-000000000000', 'client-id', 'secret');
    out.checks.identity = { version: ver('@azure/identity'), ClientSecretCredential: typeof c.getToken,
      msal_node_seen_by_identity: verFrom('@azure/msal-node', '@azure/identity') };
  }
  if (has('@azure/msal-node')) {
    const m = req('@azure/msal-node');
    const app = new m.ConfidentialClientApplication({ auth: { clientId: 'client-id', authority: 'https://login.microsoftonline.com/common', clientSecret: 'secret' } });
    out.checks.msal_node_top = { version: ver('@azure/msal-node'), acquireTokenByClientCredential: typeof app.acquireTokenByClientCredential };
  }
  const c = out.checks;
  out.ok = Object.keys(c).length > 0 && (!c.msgpackr || c.msgpackr.roundtrip === true) && (!c.bullmq || (c.bullmq.Queue === 'function' && c.bullmq.Worker === 'function'))
    && (!c.identity || c.identity.ClientSecretCredential === 'function') && (!c.msal_node_top || c.msal_node_top.acquireTokenByClientCredential === 'function');
} catch (e) { out.ok = false; out.fatal = String(e && e.stack || e).slice(0, 300); }
console.log(JSON.stringify(out));
process.exit(out.ok ? 0 : 1);
