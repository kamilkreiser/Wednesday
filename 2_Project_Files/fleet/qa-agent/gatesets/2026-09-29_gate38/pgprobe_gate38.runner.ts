/**
 * pgprobe_gate38.runner.ts — ONE boot of the REAL `runStartupMigrations()` (the file extracted from the scratch clone at a pinned revision), run by the
 * checkout's tsx against a throwaway PostgreSQL over a UNIX SOCKET (no TCP). Driven by pgprobe_gate38.py; never run by hand against anything else.
 * argv: <startup-migrations.ts path> <migrations dir> <database url (unix socket)>
 * Prints ONE JSON line last: the run's return value, the recorded summary (head only), the captured log lines, and the database read AFTER the boot.
 */
/* eslint-disable */
const path = require('path');
const [, , smPath, migDir, dbUrl] = process.argv;
for (const k of ['PLATFORM_DATABASE_URL', 'MIGRATION_DATABASE_URL', 'MIGRATION_PLATFORM_DATABASE_URL', 'APP_DB_PASSWORD', 'MULTI_TENANCY_ENABLED']) delete process.env[k];
process.env.DATABASE_URL = dbUrl;
process.env.MIGRATIONS_DIR = migDir;
const lines: string[] = [];
const cap = (...a: unknown[]) => { lines.push(a.map((x) => (typeof x === 'string' ? x : JSON.stringify(x))).join(' ')); };
const orig = { log: console.log, warn: console.warn, error: console.error };
console.log = cap; console.warn = cap; console.error = cap;
(async () => {
  let ret: unknown = null; let threw: string | null = null; let recorded: unknown = null;
  try {
    const m = require(smPath);
    ret = await m.runStartupMigrations();
  } catch (e: any) { threw = String(e?.message || e); }
  try { recorded = require(path.join(path.dirname(smPath), 'services', 'startupMigrationStatus')).getStartupMigrations(); } catch { recorded = 'MODULE ABSENT'; }
  const pg = require('pg');
  const c = new pg.Client({ connectionString: dbUrl });
  await c.connect();
  const one = async (sql: string) => { try { const r = await c.query(sql); return r.rows[0] ? Object.values(r.rows[0])[0] : null; } catch (e: any) { return 'ERROR ' + (e?.code || '') + ' ' + String(e?.message).slice(0, 120); } };
  const db = {
    fn_auth_find_oauth_app_by_client_id: await one(`SELECT to_regprocedure('auth_find_oauth_app_by_client_id(text)')::text`),
    fn_security_find_api_key_by_hash: await one(`SELECT to_regprocedure('security_find_api_key_by_hash(text)')::text`),
    fn_owner: await one(`SELECT pg_get_userbyid(proowner) FROM pg_proc WHERE proname = 'auth_find_oauth_app_by_client_id'`),
    oauth_apps: await one(`SELECT to_regclass('public.oauth_apps')::text`),
    oauth_apps_auth_lookup_policy: await one(`SELECT count(*)::int FROM pg_policies WHERE tablename = 'oauth_apps' AND policyname = 'oauth_apps_auth_lookup'`),
    tracked_039: await one(`SELECT count(*)::int FROM _secuura_migrations WHERE filename = '039_rls_fail_closed.sql'`),
    tracked_total: await one(`SELECT count(*)::int FROM _secuura_migrations`),
    lookup_call: await one(`SELECT count(*)::int FROM auth_find_oauth_app_by_client_id('no-such-client')`),
  };
  await c.end();
  const warn = lines.filter((l) => l.startsWith('[WARN]'));
  const notice039 = lines.filter((l) => /039/.test(l));
  console.log = orig.log;
  process.exitCode = 0;
  orig.log(JSON.stringify({ ret, threw, recorded, db, warn: warn.map((l) => l.slice(0, 260)), lines_039: notice039.map((l) => l.slice(0, 260)), n_lines: lines.length }));
})().catch((e) => { console.log = orig.log; orig.log(JSON.stringify({ fatal: String(e?.message || e) })); process.exitCode = 3; });
