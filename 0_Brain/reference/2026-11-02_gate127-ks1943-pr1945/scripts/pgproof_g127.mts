/**
 * Gate 127 (KS-1943 / PR 1945) real-PostgreSQL proof. Evidence only, never committed.
 * Runs the REAL enforceRetention from my clone (whatever product bytes are in place: base or head) in mode st
 * (single-tenant: Prisma 7 + adapter-pg behind db.ts) or mt (MULTI_TENANCY_ENABLED=true, the real TenantPoolManager),
 * connected as the non-superuser secuura_app (audit_logs has RLS ENABLED + FORCED), against MY container g127-pg.
 * Failures are real database errors raised by triggers created and dropped in that throwaway DB only; commit-time
 * failures are DEFERRABLE INITIALLY DEFERRED constraint triggers. Persisted state + a per-statement trace
 * (txid, backend pid, bypass GUC, session user) are read on an independent superuser connection.
 * usage: tsx pgproof_g127.mts <label> <st|mt> <out.json>   (env G127_PG_PW, G127_PG_APW, G127_PG_PORT)
 */
import { createRequire } from 'node:module';
import { writeFileSync } from 'node:fs';

const [LABEL, MODE, OUT] = process.argv.slice(2);
const PORT = process.env.G127_PG_PORT;
const SU = `postgresql://secuura:${process.env.G127_PG_PW}@127.0.0.1:${PORT}/secuura`;
const SU_PLATFORM = `postgresql://secuura:${process.env.G127_PG_PW}@127.0.0.1:${PORT}/secuura_platform`;
const APP = `postgresql://secuura_app:${process.env.G127_PG_APW}@127.0.0.1:${PORT}/secuura`;
const ORIG = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate127-ks1943-pr1945/repo/Blockchain/Dev/services/originate';
const req = createRequire(`${ORIG}/package.json`);
const { Client } = req('pg');
process.env.DATABASE_URL = APP;
process.env.NODE_ENV = 'test';
process.env.LOG_LEVEL = 'error';
if (MODE === 'mt') { process.env.MULTI_TENANCY_ENABLED = 'true'; process.env.PLATFORM_DATABASE_URL = SU_PLATFORM; }
else { delete process.env.MULTI_TENANCY_ENABLED; delete process.env.PLATFORM_DATABASE_URL; }

const db = await import(`${ORIG}/src/db.ts`);
await db.initDb();
const loggerMod: any = await import(`${ORIG}/src/utils/logger.ts`);
const logger = loggerMod.logger ?? loggerMod.default?.logger;
const errLines: unknown[][] = [];
const origError = logger.error.bind(logger);
logger.error = (...a: unknown[]) => { errLines.push(a); return origError(...a); };
const gdpr: any = await import(`${ORIG}/src/services/gdprService.ts`);
const su = new Client({ connectionString: SU });
await su.connect();

const DOC = 'a1270000-0000-4000-8000-000000000001';
const TA = '00000000-0000-0000-0000-0000000001a1';
const TB = '00000000-0000-0000-0000-0000000001b2';
const USER = '00000000-0000-0000-0000-0000000001c1';
const KINDS = ['user_sessions', 'audit_logs', 'verification_requests', 'system_errors', 'share_records'];
const TARGET_TABLES = KINDS;
const id = (p: string, g: string) => `md5('g127-${p}-' || ${g})::uuid`;
const ago = (d: number) => `now() - interval '${d} days'`;

await su.query(`CREATE TABLE IF NOT EXISTS g127_trace (n bigserial PRIMARY KEY, tbl text, op text, txid bigint, pid int, bypass text, who text)`);
await su.query(`CREATE OR REPLACE FUNCTION g127_trace_fn() RETURNS trigger LANGUAGE plpgsql SECURITY DEFINER AS $$
BEGIN INSERT INTO g127_trace (tbl, op, txid, pid, bypass, who) VALUES (TG_TABLE_NAME, TG_OP, txid_current(), pg_backend_pid(), current_setting('app.tenant_scope_bypass', true), session_user::text); RETURN NULL; END $$`);
await su.query(`CREATE OR REPLACE FUNCTION g127_fail() RETURNS trigger LANGUAGE plpgsql AS $$ BEGIN RAISE EXCEPTION 'g127 injected failure on % %', TG_TABLE_NAME, TG_OP; END $$`);
for (const t of TARGET_TABLES) {
  await su.query(`DROP TRIGGER IF EXISTS g127_tr ON ${t}`);
  await su.query(`CREATE TRIGGER g127_tr AFTER DELETE OR UPDATE ON ${t} FOR EACH STATEMENT EXECUTE FUNCTION g127_trace_fn()`);
}
await su.query(`DROP TRIGGER IF EXISTS g127_tr ON data_deletion_log`);
await su.query(`CREATE TRIGGER g127_tr AFTER INSERT ON data_deletion_log FOR EACH STATEMENT EXECUTE FUNCTION g127_trace_fn()`);
await su.query(`DROP TRIGGER IF EXISTS g127_tr ON data_retention_policies`);
await su.query(`CREATE TRIGGER g127_tr AFTER UPDATE ON data_retention_policies FOR EACH STATEMENT EXECUTE FUNCTION g127_trace_fn()`);

const DROP_FAIL = ['data_deletion_log', 'data_retention_policies', ...TARGET_TABLES].map((t) => `DROP TRIGGER IF EXISTS g127_f ON ${t}`).join('; ');
async function seed() {
  await su.query(DROP_FAIL);
  await su.query(`DELETE FROM data_deletion_log; UPDATE data_retention_policies SET last_enforcement_at = NULL`);
  await su.query(`DELETE FROM user_sessions WHERE token_hash LIKE 'g127-%'; DELETE FROM audit_logs WHERE action = 'g127-probe'; DELETE FROM system_errors WHERE service = 'g127-probe'; DELETE FROM share_records WHERE document_id = '${DOC}'; DELETE FROM verification_requests WHERE document_id = '${DOC}'; DELETE FROM documents WHERE id = '${DOC}'`);
  await su.query(`INSERT INTO documents (id, title, document_type, content_hash, tenant_id) VALUES ('${DOC}', 'g127', 'pdf', 'g127hash', '${TA}')`);
  // user_sessions (90 d): 4 old, 1 at 91 d (expired), 1 at 89 d (kept), 2 fresh
  await su.query(`INSERT INTO user_sessions (id, user_id, token_hash, expires_at, created_at) SELECT ${id('us', 'g')}, '${USER}', 'g127-' || g, now(), CASE WHEN g <= 4 THEN ${ago(4000)} WHEN g = 5 THEN ${ago(91)} WHEN g = 6 THEN ${ago(89)} ELSE ${ago(1)} END FROM generate_series(1, 8) g`);
  // audit_logs (2555 d, anonymise, FORCED RLS): tenant A 3 old with user, 1 old with NULL user (not matched), 1 at 2556 d, 1 at 2554 d, 2 fresh; tenant B 2 old with user, 1 fresh
  await su.query(`INSERT INTO audit_logs (id, action, resource_type, tenant_id, user_id, ip_address, user_agent, details, created_at) SELECT ${id('al', 'g')}, 'g127-probe', 'probe', CASE WHEN g <= 8 THEN '${TA}'::uuid ELSE '${TB}'::uuid END, CASE WHEN g = 4 THEN NULL ELSE '${USER}'::uuid END, '10.0.0.' || g, 'ua-' || g, jsonb_build_object('k', g), CASE WHEN g <= 4 THEN ${ago(4000)} WHEN g = 5 THEN ${ago(2556)} WHEN g = 6 THEN ${ago(2554)} WHEN g IN (7, 8) THEN ${ago(1)} WHEN g IN (9, 10) THEN ${ago(4000)} ELSE ${ago(1)} END FROM generate_series(1, 11) g`);
  // verification_requests (365 d): 3 old, 1 at 366, 1 at 364, 1 fresh
  await su.query(`INSERT INTO verification_requests (id, document_id, created_at) SELECT ${id('vr', 'g')}, '${DOC}', CASE WHEN g <= 3 THEN ${ago(4000)} WHEN g = 4 THEN ${ago(366)} WHEN g = 5 THEN ${ago(364)} ELSE ${ago(1)} END FROM generate_series(1, 6) g`);
  // system_errors (90 d, anonymise): 2 old with user, 1 old NULL user, 1 at 91 d, 1 at 89 d, 1 fresh
  await su.query(`INSERT INTO system_errors (id, service, error_type, message, severity, user_id, ip_address, stack, metadata, created_at) SELECT ${id('se', 'g')}, 'g127-probe', 'x', 'm' || g, 'error', CASE WHEN g = 3 THEN NULL ELSE '${USER}'::uuid END, ('10.0.1.' || g)::inet, 'st' || g, jsonb_build_object('k', g), CASE WHEN g <= 3 THEN ${ago(4000)} WHEN g = 4 THEN ${ago(91)} WHEN g = 5 THEN ${ago(89)} ELSE ${ago(1)} END FROM generate_series(1, 6) g`);
  // share_records (365 d): 3 old, 1 at 366, 1 at 364, 1 fresh
  await su.query(`INSERT INTO share_records (id, document_id, to_email, shared_by_id, created_at) SELECT ${id('sr', 'g')}, '${DOC}', 'g' || g || '@example.test', 'u', CASE WHEN g <= 3 THEN ${ago(4000)} WHEN g = 4 THEN ${ago(366)} WHEN g = 5 THEN ${ago(364)} ELSE ${ago(1)} END FROM generate_series(1, 6) g`);
  await su.query(`TRUNCATE g127_trace`);
}
const EXPECT_N: Record<string, number> = { user_sessions: 5, audit_logs: 6, verification_requests: 4, system_errors: 3, share_records: 4 };
async function snapshot() {
  const q = async (sql: string) => (await su.query(sql)).rows;
  return {
    user_sessions: await q(`SELECT id::text, token_hash FROM user_sessions WHERE token_hash LIKE 'g127-%' ORDER BY id`),
    audit_logs: await q(`SELECT id::text, tenant_id::text, user_id::text, ip_address, user_agent, details::text FROM audit_logs WHERE action = 'g127-probe' ORDER BY id`),
    verification_requests: await q(`SELECT id::text FROM verification_requests WHERE document_id = '${DOC}' ORDER BY id`),
    system_errors: await q(`SELECT id::text, user_id::text, host(ip_address) AS ip, stack, metadata::text FROM system_errors WHERE service = 'g127-probe' ORDER BY id`),
    share_records: await q(`SELECT id::text FROM share_records WHERE document_id = '${DOC}' ORDER BY id`),
  };
}
type Snap = Awaited<ReturnType<typeof snapshot>>;
async function state(seedSnap: Snap) {
  const after = await snapshot();
  const log = (await su.query(`SELECT data_type, records_affected FROM data_deletion_log`)).rows;
  const stamped = (await su.query(`SELECT data_type FROM data_retention_policies WHERE last_enforcement_at IS NOT NULL`)).rows.map((r: any) => r.data_type);
  const out: Record<string, { changed: string[]; logRows: number; affected: number | null; stamped: boolean }> = {};
  for (const k of KINDS) {
    const before = new Map((seedSnap as any)[k].map((r: any) => [r.id, JSON.stringify(r)]));
    const now = new Map((after as any)[k].map((r: any) => [r.id, JSON.stringify(r)]));
    const changed: string[] = [];
    for (const [rid, v] of before) { if (!now.has(rid)) changed.push('del:' + rid.slice(0, 8)); else if (now.get(rid) !== v) changed.push('anon:' + rid.slice(0, 8)); }
    const rows = log.filter((r: any) => r.data_type === k);
    out[k] = { changed: changed.sort(), logRows: rows.length, affected: rows[0] ? Number(rows[0].records_affected) : null, stamped: stamped.includes(k) };
  }
  return { per: out, after };
}
const complete = (s: any, k: string) => s[k].changed.length === EXPECT_N[k] && s[k].logRows === 1 && s[k].affected === EXPECT_N[k] && s[k].stamped;
const untouched = (s: any, k: string) => s[k].changed.length === 0 && s[k].logRows === 0 && !s[k].stamped;
const shape = (s: any, k: string) => `${s[k].changed.length ? 'DATA' : '-'}/${s[k].logRows ? 'LOG' : '-'}/${s[k].stamped ? 'STAMP' : '-'}`;

const FAILS: Record<string, (k: string) => string> = {
  'F1 at the DELETE/anonymise': (k) => `CREATE TRIGGER g127_f BEFORE ${k === 'audit_logs' || k === 'system_errors' ? 'UPDATE' : 'DELETE'} ON ${k} FOR EACH ROW EXECUTE FUNCTION g127_fail()`,
  'F2 at the log INSERT': (k) => `CREATE TRIGGER g127_f BEFORE INSERT ON data_deletion_log FOR EACH ROW WHEN (NEW.data_type = '${k}') EXECUTE FUNCTION g127_fail()`,
  'F3 at the stamp': (k) => `CREATE TRIGGER g127_f BEFORE UPDATE ON data_retention_policies FOR EACH ROW WHEN (NEW.data_type = '${k}') EXECUTE FUNCTION g127_fail()`,
  'F4 at COMMIT (deferred, on the stamp row)': (k) => `CREATE CONSTRAINT TRIGGER g127_f AFTER UPDATE ON data_retention_policies DEFERRABLE INITIALLY DEFERRED FOR EACH ROW WHEN (NEW.data_type = '${k}') EXECUTE FUNCTION g127_fail()`,
  'F5 at COMMIT (deferred, on the log row)': (k) => `CREATE CONSTRAINT TRIGGER g127_f AFTER INSERT ON data_deletion_log DEFERRABLE INITIALLY DEFERRED FOR EACH ROW WHEN (NEW.data_type = '${k}') EXECUTE FUNCTION g127_fail()`,
};
const cells: Array<{ name: string; kind: string | null; point: string | null }> = [{ name: 'healthy', kind: null, point: null }];
for (const kind of ['user_sessions', 'audit_logs']) for (const point of Object.keys(FAILS)) cells.push({ name: `${point} / ${kind}`, kind, point });

const results: any[] = [];
let healthySnap: any = null;
for (const c of cells) {
  await seed();
  const seedSnap = await snapshot();
  const seedOk = KINDS.every((k) => (seedSnap as any)[k].length > 0);
  if (c.kind && c.point) await su.query(FAILS[c.point](c.kind));
  errLines.length = 0;
  let returned: string[] = [];
  let rejected = '';
  try { returned = ((await gdpr.enforceRetention()) as Array<{ dataType: string }>).map((l) => l.dataType); }
  catch (e) { rejected = String((e as Error)?.constructor?.name); }
  await su.query(DROP_FAIL);
  const { per, after } = await state(seedSnap);
  const trace = (await su.query(`SELECT tbl, op, txid::text, pid, bypass, who FROM g127_trace ORDER BY n`)).rows;
  const logLines = errLines.map((a) => JSON.stringify(a));
  const othersComplete = KINDS.filter((k) => k !== c.kind).every((k) => complete(per, k));
  const failedShape = c.kind ? shape(per, c.kind) : null;
  const allOrNothing = c.kind ? (untouched(per, c.kind) || complete(per, c.kind)) : KINDS.every((k) => complete(per, k));
  const ks1943 = !rejected && seedOk && othersComplete && (c.kind ? untouched(per, c.kind) && !returned.includes(c.kind) : returned.length === 5);
  if (c.name === 'healthy') healthySnap = after;
  results.push({ name: c.name, kind: c.kind, point: c.point, ks1943, allOrNothing, failedShape, othersComplete, returned, rejected, logLines, per, trace });
  console.log(`${ks1943 ? 'PASS' : 'FAIL'} ${LABEL} ${MODE} | ${c.name} | failed-policy after-state ${failedShape ?? 'n/a'} | allOrNothing=${allOrNothing} othersComplete=${othersComplete} returned=${returned.join(',')} errLogs=${errLines.length}`);
}
await seed();
await su.query(`DELETE FROM user_sessions WHERE token_hash LIKE 'g127-%'; DELETE FROM audit_logs WHERE action = 'g127-probe'; DELETE FROM system_errors WHERE service = 'g127-probe'; DELETE FROM share_records WHERE document_id = '${DOC}'; DELETE FROM verification_requests WHERE document_id = '${DOC}'; DELETE FROM documents WHERE id = '${DOC}'; DELETE FROM data_deletion_log; TRUNCATE g127_trace`);
writeFileSync(OUT, JSON.stringify({ label: LABEL, mode: MODE, results, healthySnap }, null, 1));
console.log(`RESULT ${LABEL} ${MODE}: ${results.filter((r) => r.ks1943).length}/${results.length} cells hold the KS-1943 outcome; allOrNothing ${results.filter((r) => r.allOrNothing).length}/${results.length}`);
await su.end();
await db.disconnectDb();
process.exit(0);
