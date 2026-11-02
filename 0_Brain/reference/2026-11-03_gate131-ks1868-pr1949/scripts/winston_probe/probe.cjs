// Real winston (the auth logger's exact config, rebuilt in CJS) given each hostile `error` meta value.
// Measures: does logger.warn throw synchronously? does a LATER ordinary log still print (hang/poison)?
const path = require('path');
const winston = require(path.join(process.argv[2], 'node_modules/winston'));
const prod = process.argv[3] === 'production';
const { combine, timestamp, printf, colorize, json, errors } = winston.format;
const devFormat = printf(({ level, message, timestamp, service, ...meta }) => {
  const metaStr = Object.keys(meta).length ? ` ${JSON.stringify(meta)}` : '';
  return `${timestamp} [${service || 'auth'}] ${level}: ${message}${metaStr}`;
});
const kinds = {
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  toStringThrows: () => ({ toString() { throw new Error('ts boom'); } }),
  nullProto: () => Object.create(null),
  nullProtoWithField: () => Object.assign(Object.create(null), { f: 'VALUE_SHOULD_NOT_PRINT' }),
  symbol: () => Symbol('ks1868'),
  undef: () => undefined,
  str: () => 'db down',
};
const out = [];
for (const [k, mk] of Object.entries(kinds)) {
  const lines = [];
  const logger = winston.createLogger({
    level: 'debug', defaultMeta: { service: 'auth' },
    format: combine(errors({ stack: true }), timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' })),
    transports: [new winston.transports.Console({ format: prod ? combine(json()) : combine(colorize(), devFormat) })],
  });
  // capture console transport output
  const t = logger.transports[0];
  t.log = (info, cb) => { lines.push(info[Symbol.for('message')]); cb && cb(); };
  let threw = null;
  try { logger.warn('UPGRADE-ON-VERIFY rehash failed (non-fatal)', { userId: 'u1', error: mk() }); } catch (e) { threw = e && e.constructor && e.constructor.name + ': ' + e.message; }
  let threw2 = null;
  try { logger.info('after', { x: 1 }); } catch (e) { threw2 = String(e); }
  out.push({ kind: k, syncThrow: threw, firstLine: lines[0] ?? null, laterLogPrinted: lines.some((l) => String(l).includes('after')), laterThrow: threw2 });
}
console.log(JSON.stringify({ mode: prod ? 'production(json)' : 'dev(printf)', results: out }, null, 1));
