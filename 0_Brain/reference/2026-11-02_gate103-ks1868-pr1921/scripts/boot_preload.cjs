// QA gate 103: replaces ONLY the `pg` driver for a real `node` boot of the kyc service. BOOT_KIND picks what the
// verifyDbReady COUNT(*) probe rejects with.
const Module = require('module');
const kinds = {
  none: null,
  ordinary: () => new Error('db down'),
  string: () => 'db down (string)',
  plainObject: () => ({ code: 'X' }),
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  throwingGetter: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
};
const kind = process.env.BOOT_KIND || 'none';
let probes = 0;
function exec(text) {
  const n = String(text).replace(/\s+/g, ' ').trim();
  if (/^SELECT 1 AS ok/i.test(n)) return Promise.resolve({ rows: [{ ok: 1 }], rowCount: 1 });
  if (/^SELECT COUNT\(\*\) AS cnt FROM svc_kyc_verifications/i.test(n)) {
    probes += 1; process.stderr.write(`GATE103 probe-query #${probes}\n`);
    if (kinds[kind]) return Promise.reject(kinds[kind]());
    return Promise.resolve({ rows: [{ cnt: 0 }], rowCount: 1 });
  }
  return Promise.resolve({ rows: [], rowCount: 0 });
}
class Pool { constructor() {} on() { return this; } query(t) { return exec(t); } connect() { return Promise.resolve({ query: exec, release() {} }); } end() { return Promise.resolve(); } }
const stub = { Pool, default: { Pool } };
const orig = Module._load;
Module._load = function (request, parent, isMain) { if (request === 'pg') return stub; return orig.apply(this, arguments); };
