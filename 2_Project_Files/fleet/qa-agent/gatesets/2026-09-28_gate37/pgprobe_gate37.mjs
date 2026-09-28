// pgprobe_gate37.mjs — the drafter's REAL-POSTGRES probe for #1328 (KS-1335), driven by pgprobe_gate37.py (which extracts every SQL text from the
// scratch clone at the merge-base and at the head and passes it here as JSON on stdin). The engine is PGlite (@electric-sql/pglite, READ from the
// Secuura checkout's node_modules, never installed): the real Postgres engine compiled to WASM, IN-PROCESS — no socket, no port, no container, and
// NEVER the native Postgres on :5432. Each measurement opens a FRESH in-memory database. Prints one JSON object on stdout.
import { createRequire } from 'module';
const NM = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/node_modules/';
const require = createRequire(NM);
const { PGlite } = require(NM + '@electric-sql/pglite/dist/index.cjs');
const { uuid_ossp } = require(NM + '@electric-sql/pglite/dist/contrib/uuid_ossp.cjs');
const X = JSON.parse(await new Promise((r) => { let s = ''; process.stdin.on('data', (d) => (s += d)); process.stdin.on('end', () => r(s)); }));
const out = { engine: null, runs: {} };
async function fresh() { const db = new PGlite({ extensions: { uuid_ossp } }); await db.exec('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'); return db; }
async function cols(db) { return (await db.query("SELECT column_name, data_type, is_nullable FROM information_schema.columns WHERE table_name='svc_teams_webhooks' ORDER BY ordinal_position")).rows; }
async function tryExec(db, sql) { try { await db.exec(sql); return 'ok'; } catch (e) { return 'ERROR ' + (e.code || '?') + ' ' + String(e.message).slice(0, 120); } }
async function seed(db, n) {   // n rows, created_at strictly increasing (1 s apart), every row subscribed to 'certified', never sent, never attempted
  for (let i = 0; i < n; i += 1) {
    await db.query("INSERT INTO svc_teams_webhooks (organization_id, channel_name, webhook_url, events, is_active, created_at) VALUES ('org', $1, $2, '[\"certified\"]'::jsonb, true, TIMESTAMPTZ '2026-01-01' + ($3 || ' seconds')::interval)", ['wh-' + i, 'https://hooks.example.com/' + i, String(i)]);
  }
}
async function window(db, selectSql, max) {   // the route's own SELECT text, its params as the route passes them: [event, MAX + 1]; the +1 probe row sliced off
  const r = await db.query(selectSql, ['certified', max + 1]);
  return r.rows.slice(0, max).map((x) => x.channel_name);
}
async function stamp(db, updateSql, names) { for (const n of names) { const id = (await db.query('SELECT id FROM svc_teams_webhooks WHERE channel_name = $1', [n])).rows[0].id; await db.query(updateSql, [id]); } }
out.engine = (await (await fresh()).query('SELECT version()')).rows[0].version;

// A. MIGRATION IDEMPOTENCE, fresh database, head: the init CREATE, then the CORE CREATE, then the guarded DO block TWICE
{ const db = await fresh(); const steps = [];
  steps.push(['init 06 CREATE (head)', await tryExec(db, X.head.init_create)]);
  steps.push(['CORE CREATE (head)', await tryExec(db, X.head.core_create)]);
  steps.push(['CORE DO block (head) run 1', await tryExec(db, X.head.do_block)]);
  steps.push(['CORE DO block (head) run 2', await tryExec(db, X.head.do_block)]);
  steps.push(['CORE CREATE (head) run 2', await tryExec(db, X.head.core_create)]);
  out.runs.A_fresh_head_twice = { steps, columns: await cols(db) }; }
// A2. the CORE path alone (no init SQL), head, twice
{ const db = await fresh(); const steps = [];
  for (const k of [1, 2]) { steps.push(['CORE CREATE (head) run ' + k, await tryExec(db, X.head.core_create)]); steps.push(['CORE DO block (head) run ' + k, await tryExec(db, X.head.do_block)]); }
  out.runs.A2_core_only_head_twice = { steps, columns: (await cols(db)).map((c) => c.column_name) }; }
// B. UPGRADE: an EXISTING deployment at the merge-base schema with rows, then the head's DO block twice: every row kept, the new column NULL
{ const db = await fresh(); const steps = [];
  steps.push(['CORE CREATE (merge-base)', await tryExec(db, X.base.core_create)]);
  steps.push(['CORE DO block (merge-base)', await tryExec(db, X.base.do_block)]);
  await seed(db, 5); await db.query("UPDATE svc_teams_webhooks SET last_sent_at = TIMESTAMPTZ '2026-02-01' WHERE channel_name IN ('wh-1','wh-3')");
  const sig = async () => (await db.query("SELECT md5(string_agg(id::text || channel_name || coalesce(last_sent_at::text,'-') || created_at::text, ',' ORDER BY created_at)) AS h, count(*)::int AS n FROM svc_teams_webhooks")).rows[0];
  const before = await sig(); const hasBefore = (await cols(db)).some((c) => c.column_name === 'last_attempted_at');
  steps.push(['CORE DO block (head) run 1', await tryExec(db, X.head.do_block)]);
  steps.push(['CORE DO block (head) run 2', await tryExec(db, X.head.do_block)]);
  const after = await sig();
  const nulls = (await db.query('SELECT count(*)::int AS n FROM svc_teams_webhooks WHERE last_attempted_at IS NULL')).rows[0].n;
  out.runs.B_upgrade_existing_rows = { steps, column_before: hasBefore, column_after: (await cols(db)).find((c) => c.column_name === 'last_attempted_at') || null, rows_signature_before: before, rows_signature_after: after, rows_kept_byte_equal: before.h === after.h && before.n === after.n, last_attempted_at_null_rows: nulls }; }
// C. ORDERING with real rows: 30 rows, MAX 25 (the test env's), EVERY attempted row FAILS (stamped by the head's UPDATE, last_sent_at never written)
for (const [label, sel] of [['head ORDER BY last_attempted_at', X.head.select], ['CONTROL merge-base ORDER BY last_sent_at', X.base.select]]) {
  const db = await fresh(); await tryExec(db, X.head.core_create); await tryExec(db, X.head.do_block); await seed(db, 30);
  const c1 = await window(db, sel, 25); await stamp(db, X.head.update, c1);
  const c2 = await window(db, sel, 25);
  out.runs['C_rotation: ' + label] = { call1_first5: c1.slice(0, 5), call1_last: c1[c1.length - 1], call2_first5: c2.slice(0, 5), call2_equals_call1: JSON.stringify(c1) === JSON.stringify(c2), starved_reached_in_call2: ['wh-25', 'wh-26', 'wh-27', 'wh-28', 'wh-29'].filter((x) => c2.includes(x)) };
}
// D. THE DEADLINE-SKIPPED ROW: call 1 attempts (stamps) only the first 10 of its 25, the other 15 are SKIPPED (not stamped) — they must stay NULL and lead call 2
{ const db = await fresh(); await tryExec(db, X.head.core_create); await tryExec(db, X.head.do_block); await seed(db, 30);
  const c1 = await window(db, X.head.select, 25); const tried = c1.slice(0, 10), skipped = c1.slice(10);
  await stamp(db, X.head.update, tried);
  const nullSkipped = (await db.query('SELECT count(*)::int AS n FROM svc_teams_webhooks WHERE channel_name = ANY($1) AND last_attempted_at IS NULL', [skipped])).rows[0].n;
  const c2 = await window(db, X.head.select, 25);
  out.runs.D_skipped_stays_null = { tried: tried.length, skipped: skipped.length, skipped_still_null: nullSkipped, call2_first15_are_the_skipped: JSON.stringify(c2.slice(0, 15)) === JSON.stringify(skipped), call2_head: c2.slice(0, 3), tried_rows_in_call2: tried.filter((x) => c2.includes(x)).length }; }
// E. DEPLOY ORDER: the head's route SQL against a database the migration has NOT reached (the merge-base schema)
{ const db = await fresh(); await tryExec(db, X.base.core_create); await tryExec(db, X.base.do_block); await seed(db, 3);
  let sel = 'ok', upd = 'ok';
  try { await db.query(X.head.select, ['certified', 26]); } catch (e) { sel = 'ERROR ' + (e.code || '?') + ' ' + String(e.message).slice(0, 100); }
  try { await db.query(X.head.update, ['00000000-0000-0000-0000-000000000000']); } catch (e) { upd = 'ERROR ' + (e.code || '?') + ' ' + String(e.message).slice(0, 100); }
  out.runs.E_head_route_sql_on_unmigrated_schema = { select: sel, update: upd }; }
// F. THE EXTRA WRITE'S COST, in-process only: N stamp UPDATEs by primary key, timed one by one (NO network: a lower bound, never the deployed cost)
{ const db = await fresh(); await tryExec(db, X.head.core_create); await tryExec(db, X.head.do_block); await seed(db, 50);
  const ids = (await db.query('SELECT id FROM svc_teams_webhooks')).rows.map((r) => r.id); const t = [];
  for (let k = 0; k < 3; k += 1) for (const id of ids) { const s = process.hrtime.bigint(); await db.query(X.head.update, [id]); t.push(Number(process.hrtime.bigint() - s) / 1e6); }
  t.sort((a, b) => a - b);
  out.runs.F_update_cost_inprocess = { updates: t.length, median_ms: +t[Math.floor(t.length / 2)].toFixed(3), p95_ms: +t[Math.floor(t.length * 0.95)].toFixed(3), max_ms: +t[t.length - 1].toFixed(3), total_for_50_rows_at_median_ms: +(t[Math.floor(t.length / 2)] * 50).toFixed(2) }; }
// CONTROLS: the instrument can see a failure and an ordering difference
{ const db = await fresh();
  out.controls = { 'CT1 a bad statement reads as ERROR, not ok': (await tryExec(db, 'ALTER TABLE no_such_table ADD COLUMN x int')).startsWith('ERROR'),
                   'CT2 the merge-base DO block leaves NO last_attempted_at (so A/B can tell the head apart)': await (async () => { const d2 = await fresh(); await tryExec(d2, X.base.core_create); await tryExec(d2, X.base.do_block); return !(await cols(d2)).some((c) => c.column_name === 'last_attempted_at'); })(),
                   'CT3 the control ORDER BY starves (call 2 == call 1) where the head rotates': out.runs['C_rotation: CONTROL merge-base ORDER BY last_sent_at'].call2_equals_call1 === true && out.runs['C_rotation: head ORDER BY last_attempted_at'].call2_equals_call1 === false }; }
console.log(JSON.stringify(out));
