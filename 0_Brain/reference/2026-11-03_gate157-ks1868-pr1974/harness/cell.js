// G157 recorder: ONE cell per process. Loads the REAL billing db.ts (base or head blob, transpiled verbatim with the
// clone's typescript) and the REAL billing utils/logger.ts (incl. its NODE_ENV=production redaction pass), and for the
// hookReal* sites the REAL chargeable-events.ts loadChargeEventsFromDb (the production onReady hook, index.ts:219).
// Only 'pg' and '@secuura/shared' are replaced. Node's default uncaughtException / unhandledRejection behaviour is
// LEFT INTACT (billing installs no handler: read in index.ts; shared's setupGracefulShutdown has no consumer), so a crash
// shows as a non-zero exit with no "alive" record.
// argv: <version: base|head> <site> <kind> <nodeEnv: test|production>
'use strict';
const fs = require('fs');
const path = require('path');
const Module = require('module');
const [version, site, kind, nodeEnv] = process.argv.slice(2);
process.env.NODE_ENV = nodeEnv;
delete process.env.LOG_LEVEL;
const H = __dirname;
const DEV = path.resolve(H, '../repo/Blockchain/Dev');
const BILL = path.join(DEV, 'services/billing/src');
const ts = require(path.join(DEV, 'node_modules/typescript'));

require.extensions['.ts'] = function (mod, filename) {
  const src = fs.readFileSync(filename, 'utf8');
  const js = ts.transpileModule(src, { fileName: filename, compilerOptions: { module: ts.ModuleKind.CommonJS, target: ts.ScriptTarget.ES2022, esModuleInterop: true } }).outputText;
  mod._compile(js, filename);
};

// ---- stubs (pg + shared only) ------------------------------------------------------------
const { EventEmitter } = require('events');
const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
const KINDS = {
  ordinaryError: () => new Error('ordinary boom'),
  plainString: () => 'plain boom',
  number42: () => 42,
  emailMessage: () => new Error('lookup failed for alice@example.com'),
  null: () => null,
  undefined: () => undefined,
  revokedProxy: revoked,
  messageGetterThrows: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
  symbolMessage: () => Object.create(Error.prototype, { message: { value: Symbol('g157') } }),
  objToStringThrows: () => ({ toString() { throw new Error('toString boom'); } }),
  messageToStringThrows: () => ({ message: { toString() { throw new Error('msg toString boom'); } } }),
  bigintMessage: () => ({ message: 10n }),
  messageToJSONThrows: () => ({ message: { toJSON() { throw new Error('toJSON boom'); } } }),
  messageIsRevokedProxy: () => ({ get message() { return revoked(); } }),
  toJSONThrowsError: () => Object.assign(new Error('tj'), { toJSON() { throw new Error('toJSON on error'); } }),
};
const mk = KINDS[kind];
if (!mk) { process.stderr.write('unknown kind ' + kind + '\n'); process.exit(9); }

let probeCount = 0;
const sqlSeen = [];
class Pool extends EventEmitter {
  constructor() { super(); global.__pool = this; }
  async query(sql) {
    sqlSeen.push(String(sql).trim().slice(0, 40));
    if (/SELECT 1 AS ok/.test(sql)) {
      probeCount++;
      if (process.env.G157_PROBE === 'failfirst' && probeCount === 1) throw new Error('ECONNREFUSED (stub)');
      return { rows: [{ ok: 1 }] };
    }
    // hookReal sites: every warm query (CREATE TABLE / COUNT) throws the value under test
    throw mk();
  }
  async connect() { return { query: async () => ({ rows: [] }), release() {} }; }
  async end() {}
}
const STUBS = {
  pg: { Pool },
  '@secuura/shared': {
    queryWithTenantGuc: (pool, text, params) => pool.query(text, params),
    runWithPlatformScope: (fn) => fn(),
    runWithTenantId: (_t, fn) => fn(),
  },
};
const DBFILE = path.join(H, `db_${version}.ts`);
const origLoad = Module._load;
Module._load = function (req, parent, isMain) {
  if (Object.prototype.hasOwnProperty.call(STUBS, req)) return STUBS[req];
  if (req === './utils/logger' && parent && (parent.filename === DBFILE || parent.filename.startsWith(BILL))) return origLoad.call(this, path.join(BILL, 'utils/logger.ts'), parent, isMain);
  if (req === './db' && parent && parent.filename.startsWith(BILL)) return origLoad.call(this, DBFILE, parent, isMain);
  return origLoad.apply(this, arguments);
};

// ---- record the real logger's output (error->console.error, warn->console.warn, info->console.log) ----
const lines = [];
for (const k of ['log', 'warn', 'error', 'debug']) console[k] = (...a) => { lines.push({ via: k, a }); };

const db = require(DBFILE);
const { logger } = require(path.join(BILL, 'utils/logger.ts'));

const rec = { version, site, kind, nodeEnv, events: [] };
process.on('exit', (code) => {
  rec.exitCode = code;
  rec.logs = lines.map(({ via, a }) => {
    try {
      const o = JSON.parse(a[0]);
      const d = o.data || {};
      return { via, message: o.message, level: o.level, hasData: 'data' in o, hasErrorKey: 'error' in d, errorType: typeof d.error, error: typeof d.error === 'string' ? d.error : String(d.error) };
    } catch { return { via, raw: String(a[0]).slice(0, 120) }; }
  });
  rec.sql = sqlSeen;
  fs.writeSync(1, 'G157REC ' + JSON.stringify(rec) + '\n');
});

function after() {
  rec.alive = true;
  rec.flagAfter = db.isDbAvailable();
  process.exitCode = 0;
}
// index.ts:217-226 verbatim shape: startup() awaits initDb(hook); .catch logs with the REAL logger reading err?.message.
function bootLikeIndex(hook) {
  async function startup() { const c = await db.initDb(hook); rec.events.push({ initDbResolved: c }); }
  startup().catch((err) => {
    rec.events.push({ startupCatch: true, errType: (() => { try { return Object.prototype.toString.call(err); } catch { return 'unreadable'; } })() });
    logger.warn('Database init failed during startup — running in degraded mode', { error: err?.message });
  });
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
    bootLikeIndex(async () => { throw mk(); });
    setTimeout(after, 200);
  } else if (site === 'hookRecovery') {
    process.env.G157_PROBE = 'failfirst';
    bootLikeIndex(async () => { throw mk(); });
    setTimeout(after, 1600); // DB_RETRY_INITIAL_MS = 1000; timer is unref'd so keep the process alive
  } else if (site === 'hookRealBoot' || site === 'hookRealRecovery') {
    if (site === 'hookRealRecovery') process.env.G157_PROBE = 'failfirst';
    const { loadChargeEventsFromDb } = require(path.join(BILL, 'chargeable-events.ts'));
    bootLikeIndex(loadChargeEventsFromDb);
    setTimeout(after, site === 'hookRealRecovery' ? 1600 : 200);
  }
})();
