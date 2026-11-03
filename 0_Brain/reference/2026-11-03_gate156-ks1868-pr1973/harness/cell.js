// G156 recorder: ONE cell per process. Loads the REAL governance db.ts (base or head, transpiled
// verbatim with the clone's typescript), with only 'pg' and '@secuura/shared' replaced by stubs.
// Node's default uncaughtException / unhandledRejection behaviour is LEFT INTACT (governance installs no
// handler: read in index.ts + shared), so a crash shows up as a non-zero exit with no "alive" record.
// argv: <version: base|head> <site: pool|hookBoot|hookRecovery> <kind>
'use strict';
const fs = require('fs');
const path = require('path');
const Module = require('module');
const [version, site, kind] = process.argv.slice(2);
const H = __dirname;
const REPO_NM = path.resolve(H, '../repo/Blockchain/Dev/node_modules');
const ts = require(path.join(REPO_NM, 'typescript'));

// ---- stubs (pg + shared only) ------------------------------------------------------------
const { EventEmitter } = require('events');
let probeCount = 0;
const walletReads = [];
class Pool extends EventEmitter {
  constructor() { super(); global.__pool = this; }
  async query(sql) {
    probeCount++;
    if (process.env.G156_PROBE === 'failfirst' && probeCount === 1) throw new Error('ECONNREFUSED (stub)');
    return { rows: [{ ok: 1 }] };
  }
  async connect() {
    return {
      query: async (sql) => {
        if (/SELECT wallet_address/.test(String(sql))) { walletReads.push(sql); return { rows: [{ wallet_address: 'addr_test1' }] }; }
        return { rows: [] };
      },
      release() {},
    };
  }
  async end() {}
}
const STUBS = {
  pg: { Pool },
  '@secuura/shared': { applyTenantGuc: async () => undefined, runWithTenantId: async (_t, fn) => fn() },
};
const origLoad = Module._load;
Module._load = function (req, parent, isMain) {
  if (Object.prototype.hasOwnProperty.call(STUBS, req)) return STUBS[req];
  return origLoad.apply(this, arguments);
};

// ---- load the real db.ts ------------------------------------------------------------------
const src = fs.readFileSync(path.join(H, `db_${version}.ts`), 'utf8');
const js = ts.transpileModule(src, { compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2020, esModuleInterop: true } }).outputText;
const m = new Module(path.join(H, `db_${version}.js`), module);
m.filename = path.join(H, `db_${version}.js`);
m.paths = Module._nodeModulePaths(H);

// ---- record dbLog output (dbLog is console.log(JSON)) -------------------------------------
const lines = [];
console.log = (...a) => { lines.push(a); };
m._compile(js, m.filename);
const db = m.exports;

// ---- value kinds --------------------------------------------------------------------------
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const KINDS = {
  ordinaryError: () => new Error('ordinary boom'),
  plainString: () => 'plain boom',
  number42: () => 42,
  null: () => null,
  undefined: () => undefined,
  revokedProxy: revoked,
  messageGetterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  symbolMessage: () => Object.create(Error.prototype, { message: { value: Symbol('g156') } }),
  objToStringThrows: () => ({ toString() { throw new Error('toString boom'); } }),
  messageToStringThrows: () => ({ message: { toString() { throw new Error('msg toString boom'); } } }),
  bigintMessage: () => ({ message: 10n }),
  messageToJSONThrows: () => ({ message: { toJSON() { throw new Error('toJSON boom'); } } }),
  messageIsRevokedProxy: () => ({ get message() { return revoked(); } }),
};
const mk = KINDS[kind];
if (!mk) { process.stderr.write('unknown kind ' + kind + '\n'); process.exit(9); }

const rec = { version, site, kind, events: [] };
process.on('exit', (code) => {
  rec.exitCode = code;
  rec.logs = lines.map((a) => {
    try { const o = JSON.parse(a[0]); return { message: o.message, level: o.level, errorType: typeof o.error, hasErrorKey: 'error' in o, error: typeof o.error === 'string' ? o.error : String(o.error) }; }
    catch { return { raw: String(a[0]).slice(0, 120) }; }
  });
  fs.writeSync(1, 'G156REC ' + JSON.stringify(rec) + '\n');
});

const UUID = '11111111-2222-4333-8444-555555555555';
async function after() {
  rec.alive = true;
  rec.flagAfter = db.isDbAvailable();
  try { rec.walletRead = { ok: true, value: await db.getLinkedWalletAddress(UUID, 'tenant-1') }; }
  catch (e) { rec.walletRead = { ok: false, error: e && e.message }; }
  rec.walletSqlReads = walletReads.length;
  process.exitCode = 0;
}

process.env.DATABASE_URL = 'postgresql://stub:stub@localhost:5432/stub';
(async () => {
  if (site === 'pool') {
    const c = await db.initDb(); // no hook; flag true
    rec.events.push({ initDb: c });
    db.getPool();
    // pg-pool emits 'error' from a client socket event, i.e. outside any caller's try: model with setImmediate.
    setImmediate(() => {
      rec.events.push('emitting');
      global.__pool.emit('error', mk());
      rec.events.push('emit returned');
    });
    setTimeout(after, 200);
  } else if (site === 'hookBoot') {
    // index.ts:180 verbatim shape: .then with NO catch.
    db.initDb(async () => { throw mk(); }).then((connected) => { rec.events.push({ then: connected }); });
    setTimeout(after, 200);
  } else if (site === 'hookRecovery') {
    process.env.G156_PROBE = 'failfirst';
    db.initDb(async () => { throw mk(); }).then((connected) => { rec.events.push({ then: connected }); });
    setTimeout(after, 1600); // DB_RETRY_INITIAL_MS = 1000; timer is unref'd so keep the process alive
  }
})();
