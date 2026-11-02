// plain-node probe: real retentionScheduler.ts (transpiled), real utils/logger.ts (transports silenced), only enforceRetention stubbed. argv: <originate dir> <retentionScheduler.ts path> <kind>
const path = require('path'), fs = require('fs'), Module = require('module');
const [O, SCHED, kind] = process.argv.slice(2);
const ts = require(path.join(O, 'node_modules/typescript'));
const load = (file, requireFn) => { const src = ts.transpileModule(fs.readFileSync(file, 'utf8'), { compilerOptions: { module: 'commonjs', target: 'es2022', esModuleInterop: true } }).outputText; const m = { exports: {} }; new Function('exports', 'require', 'module', '__filename', '__dirname', src)(m.exports, requireFn, m, file, path.dirname(file)); return m.exports; };
const oreq = Module.createRequire(path.join(O, 'package.json'));
const logger = load(path.join(O, 'src/utils/logger.ts'), oreq).logger;
logger.transports.forEach((t) => { t.log = (_i, n) => n(); });
const rp = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const ge = (fn) => { const e = new Error('hidden'); Object.defineProperty(e, 'message', { get: fn }); return e; };
const K = { ordinary: () => new Error('ordinary msg'), string: () => 'thrown string', revokedProxy: rp,
  throwingGetter: () => ge(() => { throw new Error('getter threw'); }), getterRevokedProxy: () => ge(() => rp()), getterThrowingToJSON: () => ge(() => ({ toJSON() { throw new Error('tojson'); } })) };
let calls = 0; const errLines = [];
const origErr = logger.error.bind(logger);
const wrapped = { info() {}, warn() {}, debug() {}, error: (...a) => { errLines.push([a[0], typeof (a[1] || {}).error]); return origErr(...a); } };
const stub = { enforceRetention: async () => { calls++; if (calls <= 2) throw K[kind](); return []; } };
process.env.RETENTION_STARTUP_DELAY_MS = '10'; process.env.RETENTION_INTERVAL_MS = '60';
const req = (id) => id === './gdprService' ? stub : id === '../utils/logger' ? { logger: wrapped } : oreq(id);
const sched = load(SCHED, req);
if (!process.env.NOHANDLER) process.on('unhandledRejection', (r) => { console.log('UNHANDLED_REJECTION'); });
sched.startRetentionScheduler();
setTimeout(() => { sched.stopRetentionScheduler(); console.log(JSON.stringify({ kind, calls, errLines })); process.exit(0); }, 400);
