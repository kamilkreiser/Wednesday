// node crash.cjs <base|head> <cls: ord|revoked> : real compiled app, NO unhandledRejection listener (server.ts installs none),
// one public POST /api/nft/verify/asset with no token; the parent reports whether this process died.
const path = require('node:path');
const SVC = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate178-ks1868-pr1994/repo/Blockchain/Dev/services/nft-certificate';
const D = path.join(SVC, 'dist_gate_' + process.argv[2]);
const app = require(path.join(D, 'app.js')).default;
const { blockchainVerifier } = require(path.join(D, 'services/blockchain-verifier.service.js'));
const mk = process.argv[3] === 'ord' ? () => new Error('x') : () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
blockchainVerifier.verifyAsset = () => Promise.reject(mk());
const s = app.listen(0, '127.0.0.1', async () => {
  const u = `http://127.0.0.1:${s.address().port}/api/nft/verify/asset`;
  try {
    const r = await fetch(u, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ policyId: 'p', assetNameHex: '61' }), signal: AbortSignal.timeout(5000) });
    console.log('REPLY', r.status);
  } catch (e) { console.log('NOREPLY', e.name); }
  setTimeout(() => { console.log('ALIVE after 1s'); process.exit(0); }, 1000);
});
