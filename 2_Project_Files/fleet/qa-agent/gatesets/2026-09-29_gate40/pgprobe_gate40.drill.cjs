/* pgprobe_gate40.drill.cjs — ONE side of the drafter's REAL-POSTGRES drill of KS-1370 (#1338), driven by pgprobe_gate40.py; never run by hand against
 * anything else. Run by node with the checkout's tsx CJS hook. The PRODUCT is services/security/src/index.ts EXTRACTED (git archive) at the side's
 * revision into the drafter's scratchpad; nothing in it is edited here (an ARM side is a COPY whose single edit pgprobe_gate40.py made and asserted).
 *
 * THE ROLE (requirement 2 of gate40's commission): every product module instance connects as ROLE (env; `secuura_app`, provisioned by the REAL
 * api-gateway runStartupMigrations() with APP_DB_PASSWORD set — NOSUPERUSER NOBYPASSRLS, read back from pg_roles), so the stored read and the usage
 * write run UNDER FORCE RLS. The same drill with ROLE=postgres is the builder's superuser drill, kept only as the CONTROL that shows what a superuser
 * cannot see. Only SETUP statements (seed / revoke-in-another-process / delete / a REVOKE or GRANT that plants a fault) run as the superuser; each is
 * named in the output.
 * env: DEV (the side's Blockchain/Dev), SOCK (unix socket dir), DB, ROLE, SUPER, SIDE. Prints ONE JSON line last.
 */
/* eslint-disable */
const path = require('path'), crypto = require('crypto'), http = require('http');
const { Client } = require('pg');
const { DEV, SOCK, DB, ROLE, SUPER, SIDE } = process.env;
const PRODUCT = path.join(DEV, 'services/security/src/index.ts');
const DBTS = path.join(DEV, 'services/security/src/db.ts');
const url = (u) => `postgresql://${u}@localhost/${DB}?host=${encodeURIComponent(SOCK)}&port=${process.env.PGPORT}`;
const TENANT = '40404040-4040-4040-8040-404040404040';
const OUT = { side: SIDE, role: ROLE, scen: {} };
const note = (k, v) => { OUT.scen[k] = v; };

async function sqlAs(u, q, p) { const c = new Client({ connectionString: url(u) }); await c.connect(); try { return await c.query(q, p); } finally { await c.end(); } }
async function one(u, q, p) { try { const r = await sqlAs(u, q, p); return r.rows[0] ? Object.values(r.rows[0])[0] : null; } catch (e) { return 'ERROR ' + (e.code || '') + ' ' + String(e.message).slice(0, 140); } }
const hash = (k) => crypto.createHash('sha256').update(k).digest('hex');
let seq = 0;
async function seed(tag, active = true) {
  seq += 1;
  const id = `40404040-0000-4000-8000-${String(seq).padStart(12, '0')}`;
  const key = `sk_gate40_${tag}_${crypto.randomBytes(6).toString('hex')}`;
  await sqlAs(SUPER, 'DELETE FROM svc_api_keys WHERE id=$1', [id]);
  await sqlAs(SUPER, `INSERT INTO svc_api_keys (id, tenant_id, name, key_hash, key_prefix, scopes, is_active, usage_count)
                      VALUES ($1,$2,$3,$4,'sk_gate40','{}',$5,0)`, [id, TENANT, 'gate40 ' + tag, hash(key), active]);
  return { id, key, h: hash(key) };
}
const row = async (id) => { const r = await sqlAs(SUPER, 'SELECT is_active, usage_count::int AS usage FROM svc_api_keys WHERE id=$1', [id]); return r.rows[0] || null; };

function fresh(dbUrl) {
  for (const k of Object.keys(require.cache)) if (k.includes('/services/security/src/')) delete require.cache[k];
  if (dbUrl) process.env.DATABASE_URL = dbUrl; else delete process.env.DATABASE_URL;
  const m = require(PRODUCT); const db = require(DBTS);
  return { app: m.default || m.app || m, mem: m.memApiKeys, load: m.loadFromDb, rowToApiKey: m.rowToApiKey, initDb: db.initDb, avail: db.isDbAvailable };
}
async function serve(app) { const s = http.createServer(app); await new Promise((r) => s.listen(0, '127.0.0.1', r)); return { port: s.address().port, close: () => new Promise((r) => s.close(r)) }; }
async function validate(port, key) {
  const r = await fetch(`http://127.0.0.1:${port}/api/keys/validate`, { method: 'POST', headers: { 'Content-Type': 'application/json' }, body: JSON.stringify({ key }), signal: AbortSignal.timeout(8000) });
  const b = await r.json().catch(() => null);
  return { status: r.status, valid: b && b.data ? b.data.valid : undefined, reason: b && b.data ? b.data.reason : undefined, code: b && b.error ? b.error.code : undefined, message: b && b.error ? b.error.message : undefined };
}
function capture() {
  const lines = []; const o = process.stdout.write.bind(process.stdout), e = process.stderr.write.bind(process.stderr);
  process.stdout.write = (c, ...a) => { lines.push(String(c)); return true; };
  process.stderr.write = (c, ...a) => { lines.push(String(c)); return true; };
  return { stop: () => { process.stdout.write = o; process.stderr.write = e; return lines.join('').split('\n').filter(Boolean); } };
}

(async () => {
  // ---- P: the premise, read as ROLE and as the superuser (the builder could not see this: it ran as postgres) ----
  const pk = await seed('premise');
  note('P role attributes', await one(SUPER, `SELECT json_build_object('rolsuper', rolsuper, 'rolbypassrls', rolbypassrls, 'rolinherit', rolinherit) FROM pg_roles WHERE rolname=$1`, [ROLE]));
  note('P svc_api_keys rls/force/policies', await one(SUPER, `SELECT json_build_object('rls', c.relrowsecurity, 'force', c.relforcerowsecurity, 'policies', (SELECT json_agg(json_build_object('name', p.policyname, 'roles', p.roles, 'cmd', p.cmd) ORDER BY p.policyname) FROM pg_policies p WHERE p.tablename='svc_api_keys')) FROM pg_class c WHERE c.relname='svc_api_keys'`));
  note('P fn owner / EXECUTE for ROLE', await one(SUPER, `SELECT json_build_object('owner', pg_get_userbyid(p.proowner), 'secdef', p.prosecdef, 'execute', has_function_privilege($1, 'security_find_api_key_by_hash(text)', 'EXECUTE')) FROM pg_proc p WHERE p.proname='security_find_api_key_by_hash'`, [ROLE]));
  note('P direct SELECT by hash as ROLE, no GUC (premise: 0 under FORCE RLS for a non-bypass role)', await one(ROLE, 'SELECT count(*)::int FROM svc_api_keys WHERE key_hash=$1', [pk.h]));
  note('P carve-out security_find_api_key_by_hash as ROLE, no GUC (must be 1)', await one(ROLE, 'SELECT count(*)::int FROM security_find_api_key_by_hash($1)', [pk.h]));
  note('P CONTROL direct SELECT by hash as the SUPERUSER (1: a superuser bypasses RLS, so a superuser drill cannot see the premise)', await one(SUPER, 'SELECT count(*)::int FROM svc_api_keys WHERE key_hash=$1', [pk.h]));
  note('P CONTROL carve-out for an unknown hash as ROLE (0)', await one(ROLE, 'SELECT count(*)::int FROM security_find_api_key_by_hash($1)', ['0'.repeat(64)]));

  // ---- R: KS-1370 itself — a revoke performed in ANOTHER process ----
  const k1 = await seed('revoke');
  const B = fresh(url(ROLE)); await B.initDb(); await B.load();
  const sB = await serve(B.app);
  note('R0 B booted as ROLE: isDbAvailable / key warmed into memApiKeys by loadFromDb (platform scope) / cached isActive', [B.avail(), !!B.mem.get(k1.id), B.mem.get(k1.id) && B.mem.get(k1.id).isActive]);
  const c1 = await validate(sB.port, k1.key);
  note('R1 CONTROL never-revoked key validates, and the usage write lands as ROLE under RLS (usage 0 -> 1)', { answer: c1, row: await row(k1.id) });
  const before = await row(k1.id);
  await sqlAs(SUPER, 'UPDATE svc_api_keys SET is_active=false WHERE id=$1', [k1.id]);   // SETUP: the revoke another process persisted
  const q1 = await validate(sB.port, k1.key);
  note('R2 THE MEASUREMENT: B (stale cache says active) validates AFTER the stored revoke — base RED: valid true + is_active back to TRUE; head GREEN: Key revoked, row stays false', { answer: q1, row_before: before, row_after: await row(k1.id), cache_after: B.mem.get(k1.id) ? B.mem.get(k1.id).isActive : 'ABSENT' });
  await sqlAs(SUPER, 'UPDATE svc_api_keys SET is_active=false WHERE id=$1', [k1.id]);   // re-assert before C boots
  const C = fresh(url(ROLE)); await C.initDb(); await C.load();
  const sC = await serve(C.app);
  note('R3 CONTROL a THIRD instance booted after the revoke refuses (the store DOES hold the revoke)', { cached: C.mem.get(k1.id) ? C.mem.get(k1.id).isActive : 'ABSENT', answer: await validate(sC.port, k1.key), row: await row(k1.id) });
  await sC.close();

  // ---- A: design call (a), sticky revoke both ways ----
  const k2 = await seed('sticky');
  await B.load();   // a boot-equivalent re-warm of B so k2 is cached
  B.mem.get(k2.id).isActive = false;   // the KS-888 R2 state: revoked in memory, the save failed, the store still reads active
  note('A1 cached-REVOKED / stored-ACTIVE (KS-888 R2 shape) — must refuse, and must NOT flip the store', { answer: await validate(sB.port, k2.key), row: await row(k2.id), cache_after: B.mem.get(k2.id) ? B.mem.get(k2.id).isActive : 'ABSENT' });

  // ---- D: design call (b), a vanished row ----
  const k3 = await seed('vanish');
  await B.load();
  await sqlAs(SUPER, 'DELETE FROM svc_api_keys WHERE id=$1', [k3.id]);   // SETUP: the row deleted by another process
  note('D1 a VANISHED row with a stale cache entry — head: Key not found + entry evicted; base: answers from cache (and its upsert may RE-CREATE the row)', { answer: await validate(sB.port, k3.key), evicted: !B.mem.get(k3.id), row_after: await row(k3.id) });

  // ---- F: Kam's split, limb 1 — a configured database whose stored read FAILS ----
  const k4 = await seed('readfail');
  await B.load();
  const fk = await seed('readfail_cachemiss');   // seeded AFTER the warm: a cache MISS
  let planted = false;
  if (ROLE !== SUPER) { await sqlAs(SUPER, `REVOKE EXECUTE ON FUNCTION security_find_api_key_by_hash(text) FROM ${ROLE}`); planted = true; }   // SETUP: the plant
  const fcap = capture();
  const f1 = await validate(sB.port, k4.key); const f2 = await validate(sB.port, fk.key);
  const flog = fcap.stop();
  if (planted) await sqlAs(SUPER, `GRANT EXECUTE ON FUNCTION security_find_api_key_by_hash(text) TO ${ROLE}`);
  note('F1 stored read FAILS (EXECUTE revoked from ROLE) on a cache HIT — head: 503 Unable to verify key; base: never reads, answers valid', planted ? { answer: f1, row: await row(k4.id), log_lines: flog.filter((l) => /KS-1370|could not be read|DB fallback/.test(l)).map((l) => l.slice(0, 200)) } : 'N/A (a superuser cannot be refused EXECUTE)');
  note('F2 the same fault on a cache MISS — the pre-existing cache-miss branch (warn + Key not found)', planted ? { answer: f2 } : 'N/A');
  note('F3 CONTROL the grant restored: the same cache-hit key validates again', planted ? { answer: await validate(sB.port, k4.key), execute: await one(SUPER, `SELECT has_function_privilege($1, 'security_find_api_key_by_hash(text)', 'EXECUTE')`, [ROLE]) } : 'N/A');

  // ---- U: Kam's KS-888 ruling kept — a FAILED usage write is logged once, never refused, no key / hash in any log ----
  const k5 = await seed('usagefail');
  await B.load();
  if (ROLE !== SUPER) await sqlAs(SUPER, `REVOKE UPDATE ON svc_api_keys FROM ${ROLE}`);   // SETUP: the plant (base's upsert needs UPDATE too)
  const ucap = capture();
  const u1 = await validate(sB.port, k5.key);
  const ulog = ucap.stop();
  if (ROLE !== SUPER) await sqlAs(SUPER, `GRANT UPDATE ON svc_api_keys TO ${ROLE}`);
  note('U1 usage write FAILS (UPDATE revoked from ROLE) — still 200 valid, ONE error line, no key and no hash in any captured line', ROLE !== SUPER ? {
    answer: u1, row: await row(k5.id), error_lines: ulog.filter((l) => /DB save API key failed/.test(l)).length,
    lines_with_key: ulog.filter((l) => l.includes(k5.key)).length, lines_with_hash: ulog.filter((l) => l.includes(k5.h)).length, lines_captured: ulog.length,
    sample: ulog.filter((l) => /error/i.test(l)).map((l) => l.slice(0, 220)).slice(0, 3) } : 'N/A');
  const k6 = await seed('usagelands');
  await B.load();
  note('U2 CONTROL usage write lands as ROLE (usage 0 -> 1, is_active untouched)', { answer: await validate(sB.port, k6.key), row: await row(k6.id) });
  await sB.close();

  // ---- M: Kam's split, limb 2 — memory-only mode (no database configured) ----
  const M = fresh(null);
  const mk = 'sk_gate40_memonly_' + crypto.randomBytes(6).toString('hex');
  const mrow = { id: '40404040-0000-4000-8000-999999999999', tenant_id: TENANT, organization_id: null, name: 'mem', key_hash: hash(mk), key_prefix: 'sk_gate40', scopes: [], rate_limit: 1000, rate_limit_window: 3600, usage_count: 0, is_active: true, created_at: new Date(), connector_id: null };
  M.mem.set(mrow.id, M.rowToApiKey(mrow));
  const sM = await serve(M.app);
  const m1 = await validate(sM.port, mk);
  M.mem.get(mrow.id).isActive = false;
  const m2 = await validate(sM.port, mk);
  note('M1 memory-only (DATABASE_URL unset): isDbAvailable / an ACTIVE memory key answers 200 valid (never 503) / a key revoked IN memory is refused', { avail: M.avail(), active: m1, revoked: m2 });
  await sM.close();

  console.log('\n' + JSON.stringify(OUT));
  process.exit(0);
})().catch((e) => { console.log('\n' + JSON.stringify({ side: SIDE, role: ROLE, fatal: String(e && e.stack || e).slice(0, 800), partial: OUT })); process.exit(3); });
