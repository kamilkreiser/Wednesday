// gate 136 (from gate 134): the PostgreSQL mechanism behind Q3d, with no app code. Two REAL gate_app connections each run the SAME
// first-registration insert for the same (id, wallet) at the same moment, N rounds per SQL form.
//  head form : INSERT ... ON CONFLICT (id) DO NOTHING RETURNING *   (the PR's dbInsertParticipantIfAbsent)
//  untargeted: INSERT ... ON CONFLICT DO NOTHING RETURNING *        (candidate fix B)
const pg = require('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-03_gate136-ks1950-pr1952-delta/repo/Blockchain/Dev/node_modules/pg');
const URL = 'postgres://gate_app:gate136local@127.0.0.1:55136/postgres';
const N = Number(process.argv[2] || 1000);
const cols = '(id, wallet_address, staked_amount, tier, vote_power)';
const FORMS = {
  head: `INSERT INTO svc_governance_participants ${cols} VALUES ($1,$2,0,'basic',0) ON CONFLICT (id) DO NOTHING RETURNING *`,
  untargeted: `INSERT INTO svc_governance_participants ${cols} VALUES ($1,$2,0,'basic',0) ON CONFLICT DO NOTHING RETURNING *`,
};
(async () => {
  const a = new pg.Client(URL), b = new pg.Client(URL), c = new pg.Client(URL);
  await a.connect(); await b.connect(); await c.connect();
  for (const [name, sql] of Object.entries(FORMS)) {
    const out = { inserted1_nothing1: 0, err23505: {}, otherErr: 0, rowsAfterNot1: 0 };
    for (let i = 0; i < N; i += 1) {
      const id = `sqlrace-${name}-${i}`, w = `addr_sqlrace_${name}_${i}`;
      const r = await Promise.allSettled([a.query(sql, [id, w]), b.query(sql, [id, w])]);
      const ok = r.filter((x) => x.status === 'fulfilled').map((x) => x.value.rowCount).sort().join('');
      if (ok === '01') out.inserted1_nothing1 += 1;
      for (const x of r.filter((y) => y.status === 'rejected')) {
        if (x.reason.code === '23505') out.err23505[x.reason.constraint] = (out.err23505[x.reason.constraint] || 0) + 1; else out.otherErr += 1;
      }
      const n = (await c.query('SELECT count(*)::int n FROM svc_governance_participants WHERE id = $1 OR wallet_address = $2', [id, w])).rows[0].n;
      if (n !== 1) out.rowsAfterNot1 += 1;
    }
    await c.query("DELETE FROM svc_governance_participants WHERE id LIKE 'sqlrace-%'");
    console.log(JSON.stringify({ form: name, rounds: N, ...out }));
  }
  await a.end(); await b.end(); await c.end();
})().catch((e) => { console.error('FAIL', e.message); process.exit(1); });
