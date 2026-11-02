// Gate 100 real-PostgreSQL proof of the four creditGrants.ts statements (read FROM the head source file, not retyped).
// usage: node pgproof.mjs <connString> <creditGrants.ts path> [planted]
import { createRequire } from 'module';
import fs from 'fs';
const require = createRequire('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-02_gate100-ks1933-pr1918/repo/Blockchain/Dev/package.json');
const { Client, Pool } = require('pg');
const [conn, srcPath, planted] = process.argv.slice(2);
const src = fs.readFileSync(srcPath, 'utf8');
const grab = (name) => { const m = src.match(new RegExp('export const ' + name + ' = `([\\s\\S]*?)`;')); if (!m) throw new Error('no ' + name); return m[1]; };
let CLAIM = grab('CLAIM_GRANT_SQL'); const GRANTED = grab('MARK_GRANTED_SQL'); const FAILED = grab('MARK_FAILED_SQL'); const READ = grab('READ_GRANT_SQL');
if (planted === 'nowhere') CLAIM = CLAIM.replace(/\n\s*WHERE billing_credit_grants\.status = 'failed'/, '');
if (planted === 'donothing') CLAIM = CLAIM.replace(/DO UPDATE[\s\S]*?WHERE billing_credit_grants\.status = 'failed'/, 'DO NOTHING');
const results = []; let fails = 0;
const check = (name, ok, detail) => { results.push({ name, ok, detail }); if (!ok) fails++; console.log(`${ok ? 'PASS' : 'FAIL'} ${name} ${detail ?? ''}`); };
const pool = new Pool({ connectionString: conn, max: 30 });
const claim = (c, key, ev) => c.query(CLAIM, [key, 'cus_g100', 5, ev, 'checkout.session.completed']);
const status = async (key) => (await pool.query('SELECT status, event_id FROM billing_credit_grants WHERE payment_key=$1', [key])).rows[0];
try {
  await pool.query('TRUNCATE billing_credit_grants');
  // 1 fresh claim
  let r = await claim(pool, 'pi:a', 'evt1'); check('fresh claim returns 1 row', r.rowCount === 1, `rowCount=${r.rowCount}`);
  check('fresh row is granting', (await status('pi:a')).status === 'granting');
  // 2 granting blocks
  r = await claim(pool, 'pi:a', 'evt2'); check('claim on granting returns 0', r.rowCount === 0, `rowCount=${r.rowCount}`);
  r = await pool.query(READ, ['pi:a']); check('READ gives status+age', r.rows[0]?.status === 'granting' && typeof r.rows[0]?.age_seconds === 'number', JSON.stringify(r.rows[0]));
  // 3 mark granted, then blocked
  r = await pool.query(GRANTED, ['pi:a']); check('mark granted 1 row', r.rowCount === 1);
  r = await claim(pool, 'pi:a', 'evt3'); check('claim on granted returns 0', r.rowCount === 0, `rowCount=${r.rowCount}`);
  r = await pool.query(FAILED, ['pi:a']); check('mark failed leaves granted alone', r.rowCount === 0 && (await status('pi:a')).status === 'granted');
  // 4 failed re-claimable
  await claim(pool, 'pi:b', 'evt1'); await pool.query(FAILED, ['pi:b']);
  check('mark failed from granting', (await status('pi:b')).status === 'failed');
  r = await claim(pool, 'pi:b', 'evt9'); const sb = await status('pi:b');
  check('failed re-claimable, names new event', r.rowCount === 1 && sb.status === 'granting' && sb.event_id === 'evt9', JSON.stringify(sb));
  // 5 constraints
  for (const [label, params] of [['credits 0', ['pi:c0', 'c', 0, 'e', 't']], ['credits -1', ['pi:c1', 'c', -1, 'e', 't']], ['null customer', ['pi:c2', null, 5, 'e', 't']]]) {
    let threw = false; try { await pool.query(CLAIM, params); } catch { threw = true; } check(`constraint refuses ${label}`, threw);
  }
  { let threw = false; try { await pool.query("INSERT INTO billing_credit_grants (payment_key,customer_id,credits,status,event_id,event_type) VALUES ('pi:x','c',1,'bogus','e','t')"); } catch { threw = true; } check('constraint refuses bad status', threw); }
  // 6 race across two connections on a fresh key: A holds its INSERT uncommitted
  for (const outcome of ['COMMIT', 'ROLLBACK']) {
    const key = 'pi:race_' + outcome;
    const A = new Client({ connectionString: conn }); const B = new Client({ connectionString: conn }); await A.connect(); await B.connect();
    await A.query('BEGIN'); const ra = await claim(A, key, 'evtA');
    let bDone = false; const pb = claim(B, key, 'evtB').then((x) => { bDone = true; return x; });
    await new Promise((res) => setTimeout(res, 400));
    check(`race(${outcome}): B waits on A's uncommitted claim`, ra.rowCount === 1 && bDone === false);
    await A.query(outcome); const rb = await pb;
    check(`race(${outcome}): B gets ${outcome === 'COMMIT' ? 0 : 1}`, rb.rowCount === (outcome === 'COMMIT' ? 0 : 1), `rowCount=${rb.rowCount}`);
    await A.end(); await B.end();
  }
  // 7 failed row contended by two transactions
  {
    const key = 'pi:failrace'; await claim(pool, key, 'e0'); await pool.query(FAILED, [key]);
    const A = new Client({ connectionString: conn }); const B = new Client({ connectionString: conn }); await A.connect(); await B.connect();
    await A.query('BEGIN'); const ra = await claim(A, key, 'evtA');
    const pb = claim(B, key, 'evtB'); await new Promise((res) => setTimeout(res, 300)); await A.query('COMMIT'); const rb = await pb;
    check('failed row, two contenders: exactly one wins', ra.rowCount + rb.rowCount === 1, `A=${ra.rowCount} B=${rb.rowCount}`);
    await A.end(); await B.end();
  }
  // 8 20 concurrent claims on a fresh key, and on a failed key
  for (const pre of ['fresh', 'failed']) {
    const key = 'pi:twenty_' + pre;
    if (pre === 'failed') { await claim(pool, key, 'e0'); await pool.query(FAILED, [key]); }
    const rs = await Promise.all(Array.from({ length: 20 }, (_, i) => claim(pool, key, 'evt' + i)));
    const winners = rs.filter((x) => x.rowCount === 1).length;
    check(`20 concurrent claims (${pre}): 1 winner`, winners === 1, `winners=${winners}`);
  }
  // 9 pi: and cs: are distinct keys (a cs: claim never blocks a pi: claim)
  await claim(pool, 'cs:cs_1', 'e1'); r = await claim(pool, 'pi:pi_1', 'e2'); check('cs: and pi: keys independent', r.rowCount === 1);
} catch (e) { fails++; console.log('ERROR', e && e.message); }
await pool.end();
console.log(`SUMMARY planted=${planted ?? 'none'} pass=${results.filter((x) => x.ok).length} fail=${fails}`);
process.exit(fails ? 1 : 0);
