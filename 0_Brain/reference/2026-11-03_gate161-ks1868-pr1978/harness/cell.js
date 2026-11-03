// G161 recorder cell: one process per (version, path, kind). NODE_ENV from the parent (development|production).
// Real auth logger (winston, resolved from the clone's install), real base/head password.ts, email.ts, oauthState.ts,
// issuerCertSweep.ts (extracted by blob, transpiled verbatim). Replaced through Module._load ONLY: argon2, global fetch,
// nodemailer, @azure/communication-email, ./session (getRedisClient), ../events (publishEvent),
// ../repositories/issuerCertRepo, and @secuura/shared's runWithPlatformScope for the sweep (email uses the REAL shared).
// No process-level handlers: an unhandled rejection takes Node's default (exit 1), as auth registers none.
// argv: version(base|head) path kind
const path = require('path');
const Module = require('module');
const [, , version, cellPath, kind] = process.argv;
const W = path.resolve(__dirname, '..');
const AUTH = path.join(W, 'repo/Blockchain/Dev/services/auth');
const BUILD = process.env.G161_BUILD || path.join(__dirname, 'build_' + version);
const out = { version, path: cellPath, kind, env: process.env.NODE_ENV, calls: [] };
function safeDesc(e) { try { return String(e && e.message !== undefined ? e.message : e).slice(0, 80); } catch { return '<undescribable>'; } }

// ---- values ----
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const withMessage = (m) => Object.create(Error.prototype, { message: { get() { return m; } } });
const KINDS = {
  ordinaryError: () => new Error('g161 boom'),
  plainString: () => 'g161 boom',
  number42: () => 42,
  null: () => null,
  undefined: () => undefined,
  revokedProxy: revoked,
  messageGetterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  symbolMessage: () => withMessage(Symbol('g161')),
  bigintMessage: () => withMessage(10n),
  bigintValue: () => 10n,
  messageToJSONThrows: () => withMessage({ toJSON() { throw new Error('toJSON boom'); } }),
  errToJSONThrows: () => { const e = new Error('g161 boom'); e.toJSON = () => { throw new Error('toJSON boom'); }; return e; },
  objToStringThrows: () => ({ toString() { throw new Error('toString boom'); } }),
  messageToStringThrows: () => withMessage({ toString() { throw new Error('toString boom'); } }),
  messageIsRevokedProxy: () => withMessage(revoked()),
  cyclicMessage: () => { const o = { a: 1 }; o.self = o; return withMessage(o); },
  numberMessage: () => withMessage(42),
  nullMessage: () => withMessage(null),
  nullProtoMessage: () => withMessage(Object.create(null)),
};
const UP = /Up$/.test(cellPath); // positive-control paths: the dependency succeeds
const hostile = () => KINDS[kind]();

// ---- stubs ----
const sha1Suffix = require('crypto').createHash('sha1').update('g161 pw').digest('hex').toUpperCase().slice(5);
global.fetch = async () => {
  out.calls.push('fetch');
  if (cellPath === 'hibp') throw hostile();
  return { ok: true, status: 200, text: async () => `${sha1Suffix}:42\nAAAAA:1` };
};
const argon2Stub = {
  verify: async () => { out.calls.push('argon2.verify'); if (cellPath === 'verify') throw hostile(); return true; },
  hash: async () => '$argon2id$stub',
};
const nodemailerStub = {
  createTransport: () => ({
    sendMail: async () => { out.calls.push('smtp.sendMail'); if (cellPath === 'smtp') throw hostile(); return { messageId: 'm1' }; },
  }),
};
class EmailClient {
  async beginSend() { out.calls.push('acs.beginSend'); if (cellPath === 'acsNoSmtp' || cellPath === 'acsSmtpOk') throw hostile(); return { pollUntilDone: async () => ({ status: 'Succeeded', id: 'a1' }) }; }
}
const stored = new Map();
const redisStub = {
  getdel: async (k) => { out.calls.push('getdel'); if (cellPath === 'oauthGetdel') throw hostile(); const v = stored.has(k) ? stored.get(k) : null; stored.delete(k); return v; },
};
const redisMultiStub = {
  multi: () => ({ get() { return this; }, del() { return this; }, exec: async () => { out.calls.push('multi.exec'); if (cellPath === 'oauthMulti') throw hostile(); const v = stored.get('oauth_state:google:S1') ?? null; stored.delete('oauth_state:google:S1'); return [[null, v], [null, 1]]; } }),
};
const row = (id, days) => ({ id, tenantId: 't1', fingerprintSha256: 'fp' + id, name: 'c' + id, validUntil: new Date(Date.now() + days * 86400e3) });
const certRepo = {
  markExpiredCerts: async () => {
    out.calls.push('markExpired');
    if (cellPath === 'sweepMark') throw hostile();
    return cellPath === 'sweepPubExpired' || cellPath === 'sweepUp' ? [row('E1', -1), row('E2', -2)] : [];
  },
  findExpiringSoon: async (d) => {
    out.calls.push('find' + d);
    if (cellPath === 'sweepFind7' && d === 7) throw hostile();
    return [row('S' + d, d)];
  },
};
const events = {
  EventTypes: { ISSUER_CERT_EXPIRED: 'issuer_cert.expired', ISSUER_CERT_EXPIRING_SOON: 'issuer_cert.expiring_soon' },
  publishEvent: (t, p) => {
    out.calls.push('pub:' + t.split('.')[1] + ':' + p.certId);
    if (cellPath === 'sweepPubExpired' && t === 'issuer_cert.expired') return Promise.reject(hostile());
    if (cellPath === 'sweepPubSoon' && t === 'issuer_cert.expiring_soon') return Promise.reject(hostile());
    return Promise.resolve();
  },
};
const origLoad = Module._load;
Module._load = function (req, parent, isMain) {
  if (req === 'argon2') return argon2Stub;
  if (req === 'nodemailer') return nodemailerStub;
  if (req === '@azure/communication-email') return { EmailClient };
  if (req === './session') return { getRedisClient: () => (cellPath === 'oauthMulti' || cellPath === 'oauthMultiUp' ? redisMultiStub : redisStub) };
  if (req === '../events') return events;
  if (req === '../repositories/issuerCertRepo') return certRepo;
  if (req === '@secuura/shared' && /^sweep/.test(cellPath)) return { runWithPlatformScope: (fn) => fn() };
  if (!req.startsWith('.') && !req.startsWith('/') && !req.startsWith('node:') && !Module.isBuiltin(req))
    return origLoad.call(this, require.resolve(req, { paths: [AUTH] }), parent, isMain);
  return origLoad.apply(this, arguments);
};

// ---- capture output of the real logger (stdout) and console.error (stderr) ----
const logLines = [];
const origOut = process.stdout.write.bind(process.stdout);
process.stdout.write = (c) => { logLines.push(String(c)); return true; };
process.stderr.write = (c) => { logLines.push(String(c)); return true; };
let emitted = false;
function emitResult() {
  if (emitted) return; emitted = true;
  out.logs = logLines.join('').split('\n').map((l) => l.replace(/\u001b\[[0-9;]*m/g, '').trim()).filter(Boolean).map((l) => l.slice(0, 300));
  origOut('G161RESULT ' + JSON.stringify(out) + '\n');
}
// Node's default for an unhandled rejection is to throw it as an uncaught exception -> exit 1. We only OBSERVE
// the exit (no handler is registered); 'exit' still fires, so record the state reached before death.
process.on('exit', (code) => { out.exitCode = code; if (!out.done) out.died = true; emitResult(); });
const sleep = (ms) => new Promise((r) => setTimeout(r, ms));
async function settle(fn) { try { return 'resolved:' + JSON.stringify(await fn()); } catch (e) { return 'REJECTED'; } }

async function main() {
  if (cellPath === 'verify' || cellPath === 'verifyUp') {
    const pw = require(path.join(BUILD, 'services/password.js'));
    out.outcome = await settle(() => pw.verifyPassword('g161 pw', '$argon2id$v=19$stub'));
  } else if (cellPath === 'hibp' || cellPath === 'hibpUp') {
    delete process.env.HIBP_ENABLED;
    const pw = require(path.join(BUILD, 'services/password.js'));
    out.outcome = await settle(() => pw.isPasswordBreached('g161 pw'));
  } else if (/^(acs|smtp|email)/.test(cellPath)) {
    delete process.env.EMAIL_RECIPIENT_ALLOWLIST;
    if (cellPath.startsWith('acs')) { process.env.ACS_CONNECTION_STRING = 'endpoint=https://stub.invalid/;accesskey=stub'; process.env.ACS_SENDER_ADDRESS = 'no-reply@stub.invalid'; }
    if (cellPath !== 'acsNoSmtp') { process.env.SMTP_ENABLED = 'true'; process.env.SMTP_HOST = 'smtp.stub.invalid'; process.env.SMTP_FROM = 'no-reply@stub.invalid'; }
    const em = require(path.join(BUILD, 'services/email.js'));
    out.outcome = await settle(() => em.sendVerificationEmail('victim@stub.invalid', 'https://x.invalid/verify?token=T'));
  } else if (/^oauth/.test(cellPath)) {
    const os = require(path.join(BUILD, 'services/oauthState.js'));
    stored.set('oauth_state:google:S1', 'google');
    out.outcome = await settle(() => os.consumeOAuthState('S1', 'google'));
    out.stateStillStored = stored.has('oauth_state:google:S1');
    // replay: a second consume of the same state must refuse in every cell
    out.replay = await settle(() => os.consumeOAuthState('S1', 'google'));
  } else if (/^sweep/.test(cellPath)) {
    process.env.ISSUER_CERT_SWEEP_INTERVAL_MS = '0';
    const sw = require(path.join(BUILD, 'services/issuerCertSweep.js'));
    sw.startIssuerCertSweep(0); // the production entry: runs once, outer .catch attached (index.ts:276)
    await sleep(60);
    sw.stopIssuerCertSweep();
  }
  await sleep(30);
  out.alive = true;
  out.done = true;
  emitResult();
}
main().catch((e) => { out.harnessError = safeDesc(e); out.done = true; emitResult(); process.exit(3); });
