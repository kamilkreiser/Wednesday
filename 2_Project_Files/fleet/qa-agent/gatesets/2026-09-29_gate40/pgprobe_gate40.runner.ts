/**
 * pgprobe_gate40.runner.ts — ONE boot of the REAL api-gateway `runStartupMigrations()` (extracted from the scratch clone at the side's revision), run by
 * node with the checkout's tsx CJS hook against the drafter's throwaway PostgreSQL over a UNIX SOCKET (no TCP), WITH APP_DB_PASSWORD set so the REAL
 * provisionAppRole() creates `secuura_app` (NOSUPERUSER NOINHERIT NOBYPASSRLS) and applies its grants — the role every data service's DATABASE_URL
 * names (docker-compose.yml, deployment/azure/deploy.sh). Shape copied from gate39's runner (re-key), cut down to what KS-1370's drill needs: the
 * migration summary, the role's attributes, and svc_api_keys' RLS shape. Driven by pgprobe_gate40.py; never run by hand against anything else.
 * argv: <startup-migrations.ts path> <migrations dir> <database url (unix socket, the superuser)>
 */
/* eslint-disable */
const [, , smPath, migDir, dbUrl] = process.argv;
for (const k of ['PLATFORM_DATABASE_URL', 'MIGRATION_DATABASE_URL', 'MIGRATION_PLATFORM_DATABASE_URL', 'MULTI_TENANCY_ENABLED']) delete process.env[k];
process.env.DATABASE_URL = dbUrl;
process.env.MIGRATIONS_DIR = migDir;
process.env.APP_DB_PASSWORD = 'gate40-drill-only';   // a throwaway cluster's role password; the socket uses trust auth, disclosed
const lines: string[] = [];
const cap = (...a: unknown[]) => { lines.push(a.map((x) => (typeof x === 'string' ? x : JSON.stringify(x))).join(' ')); };
const orig = { log: console.log, warn: console.warn, error: console.error };
console.log = cap; console.warn = cap; console.error = cap;
(async () => {
  let ret: unknown = null; let threw: string | null = null;
  const pgm = require('pg');
  try { ret = await require(smPath).runStartupMigrations(); } catch (e: any) { threw = String(e?.message || e); }
  const c = new pgm.Client({ connectionString: dbUrl });
  await c.connect();
  const one = async (sql: string) => { try { const r = await c.query(sql); return r.rows[0] ? Object.values(r.rows[0])[0] : null; } catch (e: any) { return 'ERROR ' + (e?.code || '') + ' ' + String(e?.message).slice(0, 120); } };
  const db = {
    tracked_039: await one(`SELECT count(*)::int FROM _secuura_migrations WHERE filename = '039_rls_fail_closed.sql'`),
    tracked_total: await one(`SELECT count(*)::int FROM _secuura_migrations`),
    secuura_app: await one(`SELECT json_build_object('exists', true, 'rolsuper', rolsuper, 'rolbypassrls', rolbypassrls, 'rolinherit', rolinherit, 'rolcanlogin', rolcanlogin) FROM pg_roles WHERE rolname = 'secuura_app'`),
    svc_api_keys: await one(`SELECT json_build_object('rls', relrowsecurity, 'force', relforcerowsecurity) FROM pg_class WHERE relname = 'svc_api_keys'`),
    fn: await one(`SELECT to_regprocedure('security_find_api_key_by_hash(text)')::text`),
  };
  await c.end();
  const failedFiles = lines.filter((l) => /migration \S+\.sql failed/.test(l)).map((l) => (l.match(/migration (\S+\.sql) failed/) || [])[1]);
  console.log = orig.log;
  orig.log(JSON.stringify({ ret, threw, db, failed_files: failedFiles, provision: lines.filter((l) => /secuura_app/.test(l)).map((l) => l.slice(0, 200)), n_lines: lines.length }));
})().catch((e) => { console.log = orig.log; orig.log(JSON.stringify({ fatal: String(e?.message || e) })); process.exitCode = 3; });
