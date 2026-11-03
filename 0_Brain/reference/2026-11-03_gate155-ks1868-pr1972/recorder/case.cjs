// usage: node case.cjs <TREE originate dir> <arm: ctor|listener|initdb> <kind>
const path = require('path');
const Module = require('module');
const EE = require('events');
const [TREE, ARM, KIND] = process.argv.slice(2);
require(path.join(TREE, 'node_modules/tsx/dist/cjs/index.cjs'));
const out = { arm: ARM, kind: KIND, result: null, loggedType: null, loggedText: null, uncaught: [], unhandled: [], loggerErrors: [], processAlive: true };
process.on('uncaughtException', (e) => { out.uncaught.push(safe(() => String(e && e.message))); });
process.on('unhandledRejection', (r) => { out.unhandled.push(safe(() => String(r && r.message))); });
function safe(f) { try { return f(); } catch (e) { return '<unreadable:' + e.constructor.name + '>'; } }

function makeValue(kind) {
  switch (kind) {
    case 'ordinary': return new Error('boom ordinary');
    case 'revoked_proxy': { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; }
    case 'getter_throws': return Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } });
    case 'symbol_message': return Object.create(Error.prototype, { message: { get() { return Symbol('sym'); } } });
    case 'frozen_throwing_toString': return Object.freeze({ toString() { throw new Error('ts boom'); } });
    case 'message_frozen_throwing_toString': return Object.create(Error.prototype, { message: { get() { return Object.freeze({ toString() { throw new Error('ts boom'); } }); } } });
    case 'message_nullproto': return Object.create(Error.prototype, { message: { get() { return Object.create(null); } } });
    case 'message_toPrimitive_object': return Object.create(Error.prototype, { message: { get() { return { [Symbol.toPrimitive]() { return {}; } }; } } });
    case 'proxy_get_throws': return new Proxy({}, { get() { throw new Error('trap boom'); } });
    case 'null': return null;
    case 'undefined': return undefined;
    case 'number': return 42;
    case 'string': return 'plain string';
    default: throw new Error('unknown kind ' + kind);
  }
}
const VALUE = makeValue(KIND);

const src = path.join(TREE, 'src');
const orig = Module._load;
let listener = null;
Module._load = function (req, parent, isMain) {
  if (req === 'ioredis') {
    function RedisMock() {
      if (ARM === 'ctor') throw VALUE;
      const ee = new EE();
      ee.status = 'wait'; ee.connect = async () => {}; ee.disconnect = () => {}; ee.xadd = async () => '1-0';
      listener = ee; return ee;
    }
    return { __esModule: true, default: RedisMock };
  }
  if (req === '@prisma/client') return { PrismaClient: function () { return { $queryRaw: async () => { throw VALUE; }, $executeRaw: async () => 0, $disconnect: async () => {} }; } };
  if (req === '@prisma/adapter-pg') return { PrismaPg: function () { return {}; } };
  if (/config$/.test(req) && parent && parent.filename && parent.filename.startsWith(src)) return { config: { databaseUrl: 'postgresql://t:t@localhost:5432/t', nodeEnv: 'test' } };
  return orig.apply(this, arguments);
};

const wait = () => new Promise((r) => setTimeout(r, 60));
(async () => {
  const errLines = [];
  if (ARM === 'ctor' || ARM === 'listener') {
    const { logger } = require(path.join(src, 'utils/logger.ts'));
    logger.level = 'debug';
    logger.on('error', (e) => out.loggerErrors.push(safe(() => String(e && e.message))));
    const Transport = require(path.join(TREE, 'node_modules/winston-transport'));
    class Cap extends Transport { log(info, cb) { cap.push(info); cb(); } }
    var cap = [];
    logger.add(new Cap());
    const ev = require(path.join(src, 'events.ts'));
    let r, threw = false;
    try { r = ev.initEventBus('redis://localhost:6379'); } catch (e) { threw = true; }
    out.result = threw ? 'THROWS' : 'returns ' + r;
    if (ARM === 'listener' && !threw) {
      setImmediate(() => { listener.emit('error', VALUE); });
    }
    await wait();
    const want = ARM === 'ctor' ? 'Failed to initialise EventBus' : 'EventBus Redis error (non-fatal)';
    const line = cap.filter((i) => i.message === want);
    out.loggedCount = line.length;
    if (line[0]) { out.loggedType = typeof line[0].error; out.loggedText = out.loggedType === 'string' ? line[0].error : null; }
    if (ARM === 'listener') out.result = (threw ? 'THROWS' : 'init ok') + '; listener ' + (out.uncaught.length ? 'UNCAUGHT' : 'ok');
  } else {
    const origErr = console.error; console.error = (...a) => errLines.push(a);
    const db = require(path.join(src, 'db.ts'));
    let res;
    try { await db.initDb(); res = 'resolves'; } catch (e) { res = 'REJECTS'; }
    console.error = origErr;
    out.result = res;
    const line = errLines.filter((a) => a[0] === '[DB] Prisma connection failed:');
    out.loggedCount = line.length;
    if (line[0]) { out.loggedType = typeof line[0][1]; out.loggedText = typeof line[0][1] === 'string' ? line[0][1] : null; }
    await wait();
  }
  process.stdout.write('\n@@REC@@' + JSON.stringify(out) + '\n');
})().catch((e) => { out.result = 'HARNESS-ERROR ' + safe(() => e.stack); process.stdout.write('\n@@REC@@' + JSON.stringify(out) + '\n'); });
