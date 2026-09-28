/**
 * pgprobe_gate39.runner.ts — ONE boot of the REAL `runStartupMigrations()` (the file extracted from the scratch clone at a pinned revision), run by
 * node with the checkout's tsx CJS hook against a throwaway PostgreSQL over a UNIX SOCKET (no TCP). Driven by pgprobe_gate39.py; never run by hand
 * against anything else. Shape copied from gate38's runner (gate37 lineage), extended for gate39: the tenant_isolation shape on the four tables, the
 * whole `_secuura_migrations` list, and an OPTIONAL CORE-stage throw (QA_CORE_THROW=1: a pg Pool that has run CORE's `CREATE TABLE IF NOT EXISTS
 * oauth_apps` throws from its end() — the same plant gate38's gate used, `pool.end rejects inside migrateDatabase`; nothing in the product is edited).
 * argv: <startup-migrations.ts path> <migrations dir> <database url (unix socket)>
 * Prints ONE JSON line last: the run's return value, the recorded summary, the captured log lines, and the database read AFTER the boot.
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
const FOUR = ['oauth_apps', 'svc_webhooks', 'certifications', 'charge_events'];
(async () => {
  let ret: unknown = null; let threw: string | null = null; let recorded: unknown = null; let planted = 0;
  const pgm = require('pg');
  if (process.env.QA_CORE_THROW === '1') {
    const q0 = pgm.Pool.prototype.query; const e0 = pgm.Pool.prototype.end;
    pgm.Pool.prototype.query = function (this: any, sql: any, ...rest: any[]) {
      if (typeof sql === 'string' && /CREATE TABLE IF NOT EXISTS oauth_apps/.test(sql)) this.__qaCore = true;
      return q0.call(this, sql, ...rest);
    };
    pgm.Pool.prototype.end = async function (this: any, ...rest: any[]) {
      await e0.apply(this, rest);
      if (this.__qaCore) { planted += 1; throw new Error('QA-PLANT gate39 core stage threw'); }
    };
  }
  try {
    const m = require(smPath);
    ret = await m.runStartupMigrations();
  } catch (e: any) { threw = String(e?.message || e); }
  try { recorded = require(path.join(path.dirname(smPath), 'services', 'startupMigrationStatus')).getStartupMigrations(); } catch { recorded = 'MODULE ABSENT'; }
  const c = new pgm.Client({ connectionString: dbUrl });
  await c.connect();
  const one = async (sql: string) => { try { const r = await c.query(sql); return r.rows[0] ? Object.values(r.rows[0])[0] : null; } catch (e: any) { return 'ERROR ' + (e?.code || '') + ' ' + String(e?.message).slice(0, 120); } };
  const rows = async (sql: string) => { try { return (await c.query(sql)).rows; } catch (e: any) { return 'ERROR ' + (e?.code || '') + ' ' + String(e?.message).slice(0, 120); } };
  const db = {
    fn_auth_find_oauth_app_by_client_id: await one(`SELECT to_regprocedure('auth_find_oauth_app_by_client_id(text)')::text`),
    fn_owner: await one(`SELECT pg_get_userbyid(proowner) FROM pg_proc WHERE proname = 'auth_find_oauth_app_by_client_id'`),
    oauth_apps_auth_lookup_policy: await one(`SELECT count(*)::int FROM pg_policies WHERE tablename = 'oauth_apps' AND policyname = 'oauth_apps_auth_lookup'`),
    tenant_isolation_policies: await one(`SELECT count(*)::int FROM pg_policies WHERE policyname = 'tenant_isolation'`),
    four_tables: await rows(`SELECT c.relname AS t, c.relrowsecurity AS rls, c.relforcerowsecurity AS force,
        (SELECT count(*)::int FROM pg_policies p WHERE p.tablename = c.relname AND p.policyname = 'tenant_isolation') AS ti,
        (SELECT string_agg(pg_get_expr(pol.polqual, pol.polrelid), ' | ') FROM pg_policy pol WHERE pol.polrelid = c.oid AND pol.polname = 'tenant_isolation') AS ti_qual
      FROM pg_class c JOIN pg_namespace n ON n.oid = c.relnamespace WHERE n.nspname = 'public' AND c.relkind = 'r' AND c.relname = ANY($$${'{' + FOUR.join(',') + '}'}$$::text[]) ORDER BY 1`),
    tracked_039: await one(`SELECT count(*)::int FROM _secuura_migrations WHERE filename = '039_rls_fail_closed.sql'`),
    tracked_total: await one(`SELECT count(*)::int FROM _secuura_migrations`),
    tracked: await rows(`SELECT filename FROM _secuura_migrations ORDER BY filename`),
    lookup_call: await one(`SELECT count(*)::int FROM auth_find_oauth_app_by_client_id('no-such-client')`),
  };
  await c.end();
  const warn = lines.filter((l) => l.startsWith('[WARN]'));
  const failedFiles = lines.filter((l) => /migration \S+\.sql failed/.test(l)).map((l) => (l.match(/migration (\S+\.sql) failed/) || [])[1]);
  console.log = orig.log;
  process.exitCode = 0;
  orig.log(JSON.stringify({ ret, threw, recorded, planted, db: { ...db, tracked: Array.isArray(db.tracked) ? db.tracked.map((r: any) => r.filename) : db.tracked },
    failed_files: failedFiles, warn: warn.map((l) => l.slice(0, 260)), n_lines: lines.length }));
})().catch((e) => { console.log = orig.log; orig.log(JSON.stringify({ fatal: String(e?.message || e) })); process.exitCode = 3; });
