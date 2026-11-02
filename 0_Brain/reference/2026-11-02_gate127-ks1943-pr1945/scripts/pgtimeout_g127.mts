/**
 * Gate 127 (KS-1943 / PR 1945): the 5000 ms question on a real PostgreSQL (my container g127-pg).
 * A superuser session holds row locks (SELECT ... FOR UPDATE) on the expired user_sessions rows, so the sweep's DELETE blocks.
 * Measures: when enforceRetention settles, what persisted for user_sessions, what the other policies did, and
 * pg_stat_activity / pg_locks for secuura_app backends WHILE the lock is held and AFTER it is released.
 * usage: tsx pgtimeout_g127.mts <label> <st|mt> <out.json> [holdMs]
 */
import { createRequire } from 'node:module';
import { writeFileSync } from 'node:fs';
const [LABEL, MODE, OUT, HOLD] = process.argv.slice(2);
const HOLD_MS = Number(HOLD || 9000);
const PORT = process.env.G127_PG_PORT;
const SU = `postgresql://secuura:${process.env.G127_PG_PW}@127.0.0.1:${PORT}/secuura`;
const SU_PLATFORM = `postgresql://secuura:${process.env.G127_PG_PW}@127.0.0.1:${PORT}/secuura_platform`;
const APP = `postgresql://secuura_app:${process.env.G127_PG_APW}@127.0.0.1:${PORT}/secuura`;
const ORIG = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945/repo/Blockchain/Dev/services/originate';
const req = createRequire(`${ORIG}/package.json`);
const { Client } = req('pg');
process.env.DATABASE_URL = APP; process.env.NODE_ENV = 'test'; process.env.LOG_LEVEL = 'error';
if (MODE === 'mt') { process.env.MULTI_TENANCY_ENABLED = 'true'; process.env.PLATFORM_DATABASE_URL = SU_PLATFORM; }
else { delete process.env.MULTI_TENANCY_ENABLED; delete process.env.PLATFORM_DATABASE_URL; }
const db = await import(`${ORIG}/src/db.ts`);
await db.initDb();
const loggerMod: any = await import(`${ORIG}/src/utils/logger.ts`);
const logger = loggerMod.logger ?? loggerMod.default?.logger;
const errLines: unknown[][] = [];
const oe = logger.error.bind(logger);
logger.error = (...a: unknown[]) => { errLines.push(a); return oe(...a); };
const gdpr: any = await import(`${ORIG}/src/services/gdprService.ts`);
const su = new Client({ connectionString: SU }); await su.connect();
const locker = new Client({ connectionString: SU }); await locker.connect();
const USER = '00000000-0000-0000-0000-0000000001c1';
await su.query(`DELETE FROM data_deletion_log; UPDATE data_retention_policies SET last_enforcement_at = NULL; DELETE FROM user_sessions WHERE token_hash LIKE 'g127t-%'`);
await su.query(`INSERT INTO user_sessions (user_id, token_hash, expires_at, created_at) SELECT '${USER}', 'g127t-' || g, now(), now() - interval '4000 days' FROM generate_series(1, 3) g`);
const activity = async () => (await su.query(`SELECT pid, state, wait_event_type, wait_event, round(extract(epoch FROM now() - xact_start)::numeric, 1)::text AS xact_age_s, left(regexp_replace(query, '\\s+', ' ', 'g'), 70) AS query FROM pg_stat_activity WHERE usename = 'secuura_app' AND datname = 'secuura' ORDER BY pid`)).rows;
const locks = async () => (await su.query(`SELECT l.pid, l.locktype, coalesce(c.relname, '') AS rel, l.mode, l.granted FROM pg_locks l LEFT JOIN pg_class c ON c.oid = l.relation WHERE l.pid IN (SELECT pid FROM pg_stat_activity WHERE usename = 'secuura_app') AND l.locktype NOT IN ('virtualxid') AND coalesce(c.relname, '') NOT LIKE 'pg_%' ORDER BY l.pid, rel`)).rows;
const state = async () => ({
  remaining: Number((await su.query(`SELECT count(*) n FROM user_sessions WHERE token_hash LIKE 'g127t-%'`)).rows[0].n),
  logRows: (await su.query(`SELECT data_type, records_affected FROM data_deletion_log`)).rows,
  stamped: (await su.query(`SELECT data_type FROM data_retention_policies WHERE last_enforcement_at IS NOT NULL ORDER BY 1`)).rows.map((r: any) => r.data_type),
});
await locker.query('BEGIN');
await locker.query(`SELECT id FROM user_sessions WHERE token_hash LIKE 'g127t-%' FOR UPDATE`);
const t0 = Date.now();
let settledAt: number | null = null; let returned: string[] | null = null; let rejected = '';
const run = gdpr.enforceRetention().then((r: any[]) => { settledAt = Date.now() - t0; returned = r.map((x) => x.dataType); }, (e: any) => { settledAt = Date.now() - t0; rejected = String(e?.constructor?.name); });
const sleep = (ms: number) => new Promise((r) => setTimeout(r, ms));
await sleep(HOLD_MS - 1500);
const duringActivity = await activity(); const duringLocks = await locks(); const duringState = await state();
const settledBeforeRelease = settledAt;
await sleep(1500);
await locker.query('COMMIT');
const releasedAt = Date.now() - t0;
for (let i = 0; i < 40 && settledAt === null; i += 1) await sleep(250);
await sleep(3000);
const afterActivity = await activity(); const afterLocks = await locks(); const afterState = await state();
const res = { label: LABEL, mode: MODE, holdMs: HOLD_MS, settledAt, settledBeforeRelease, releasedAt, returned, rejected, errLines: errLines.map((a) => JSON.stringify(a)), duringActivity, duringLocks, duringState, afterActivity, afterLocks, afterState,
  idleInTxAfter: afterActivity.filter((a: any) => String(a.state).startsWith('idle in transaction')).length,
  appLocksAfter: afterLocks.filter((l: any) => l.locktype !== 'transactionid' || true).length };
writeFileSync(OUT, JSON.stringify(res, null, 1));
console.log(`${LABEL} ${MODE}: settled at ${settledAt} ms (before release: ${settledBeforeRelease !== null}), lock released at ${releasedAt} ms; returned=${JSON.stringify(returned)} rejected='${rejected}'`);
console.log(`  during hold: user_sessions remaining=${duringState.remaining}, app backends=${JSON.stringify(duringActivity)}`);
console.log(`  during hold locks: ${JSON.stringify(duringLocks)}`);
console.log(`  after release+3s: remaining=${afterState.remaining} log=${JSON.stringify(afterState.logRows)} stamped=${JSON.stringify(afterState.stamped)}`);
console.log(`  after: app backends=${JSON.stringify(afterActivity)} idle-in-transaction=${res.idleInTxAfter} app locks=${JSON.stringify(afterLocks)}`);
console.log(`  error lines: ${res.errLines.join(' || ')}`);
await su.query(`DELETE FROM user_sessions WHERE token_hash LIKE 'g127t-%'; DELETE FROM data_deletion_log`);
await su.end(); await locker.end(); await db.disconnectDb(); process.exit(0);
