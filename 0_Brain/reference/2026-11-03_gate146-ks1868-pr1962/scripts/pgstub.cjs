// Gate 146: replaces ONLY the 'pg' module for a real transfer-service process (tsx, real index.ts, real db.ts,
// real approvalWorkflowService). A one-process in-memory store models svc_approval_workflows (unique id, ON CONFLICT
// upsert) and svc_approval_step_instances (unique id, upsert). Autocommit per statement, as pool.query is.
const Module = require('module');
const fs = require('fs');
const OUT = process.env.G146_OUT, SNAP = OUT + '.snap.json';
const SCEN = process.env.G146_SCEN || 'none', KIND = process.env.G146_KIND || 'none', FAILAT = Number(process.env.G146_FAILAT || 3);
const ev = (o) => fs.appendFileSync(OUT, JSON.stringify({ t: Date.now(), ...o }) + '\n');
function hostile() {
  switch (KIND) {
    case 'ordinary': return new Error('db down');
    case 'string': return 'plain boom';
    case 'revokedProxy': { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; }
    case 'throwingGetter': return Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } });
    case 'bigintMsg': return Object.create(Error.prototype, { message: { value: 10n } });
    default: return null;
  }
}
const past = new Date(Date.now() - 3 * 3600e3);
const wf = new Map(), si = new Map();
if (SCEN.startsWith('sweep')) {
  wf.set('g146-escalating', { id: 'g146-escalating', name: 'g146', workflow_type: 'sequential', is_active: true, created_by: 'g146',
    steps: [{ id: 'esc-step', order: 1, name: 'Esc', approverType: 'user', autoEscalate: true, escalateTo: 'boss-user', timeoutHours: 1 }],
    created_at: past, updated_at: past });
  const mk = (id, step) => ({ id, step_id: step, transfer_id: 'T-' + id, status: 'pending', assigned_to: 'owner-' + id, assigned_at: past,
    due_at: new Date(Date.now() - 3600e3), escalated_at: null, escalated_to: null });
  for (const [id, s] of [['I1', 'esc-step'], ['I2', 'step-1'], ['I3', 'esc-step'], ['I4', 'step-1']]) si.set(id, mk(id, s));
}
const snap = () => fs.writeFileSync(SNAP, JSON.stringify({ workflows: [...wf.keys()], instances: [...si.values()].map((r) => ({
  id: r.id, step_id: r.step_id, status: r.status, assigned_to: r.assigned_to, escalated_at: r.escalated_at ? 'set' : null,
  escalated_to: r.escalated_to, due_future: r.due_at ? new Date(r.due_at) > new Date() : null })) }, null, 1));
snap();
let sweepNo = 0, siInsertsInSweep = 0, wfInsertNo = 0;
async function answer(text, params) {
  const q = String(text).replace(/\s+/g, ' ').trim();
  ev({ sql: q.slice(0, 70), sweepNo });
  if (q === 'SELECT 1 AS ok') return { rows: [{ ok: 1 }], rowCount: 1 };
  if (q.startsWith('SELECT 1 FROM svc_approval_workflows')) {
    if (SCEN === 'boot_probe' && KIND !== 'none') throw hostile();
    return { rows: [], rowCount: 0 };
  }
  if (q.startsWith('INSERT INTO svc_approval_workflows')) {
    wfInsertNo += 1;
    if ((SCEN === 'boot_seedall' || (SCEN === 'boot_seed1' && wfInsertNo === 1)) && KIND !== 'none') throw hostile();
    const p = params; const prev = wf.get(p[0]);
    wf.set(p[0], { ...(prev || {}), id: p[0], name: p[1], workflow_type: p[3], steps: JSON.parse(p[6]), is_active: p[11],
      required_approvals: p[4], created_by: prev ? prev.created_by : p[10], created_at: prev ? prev.created_at : p[15], updated_at: p[16] });
    snap(); return { rows: [], rowCount: 1 };
  }
  if (q.startsWith('SELECT * FROM svc_approval_workflows')) {
    if (SCEN === 'sweep_wfread' && sweepNo === 1 && KIND !== 'none') throw hostile();
    let rows = [...wf.values()];
    if (q.includes('WHERE id = $1')) rows = rows.filter((r) => r.id === params[0]);
    if (q.includes('is_active = TRUE')) rows = rows.filter((r) => r.is_active);
    return { rows, rowCount: rows.length };
  }
  if (q.startsWith("SELECT * FROM svc_approval_step_instances WHERE status = 'pending' AND due_at")) {
    sweepNo += 1; siInsertsInSweep = 0;
    if (SCEN === 'sweep_select' && sweepNo === 1 && KIND !== 'none') throw hostile();
    const now = params[0];
    const rows = [...si.values()].filter((r) => r.status === 'pending' && r.due_at && new Date(r.due_at) < now).map((r) => ({ ...r }));
    return { rows, rowCount: rows.length };
  }
  if (q.startsWith('INSERT INTO svc_approval_step_instances')) {
    siInsertsInSweep += 1;
    if (SCEN === 'sweep_k' && sweepNo === 1 && siInsertsInSweep === FAILAT && KIND !== 'none') { ev({ failedWriteOf: params[0] }); throw hostile(); }
    const p = params; const prev = si.get(p[0]) || { id: p[0], step_id: p[1], transfer_id: p[2], assigned_at: p[11] };
    si.set(p[0], { ...prev, status: p[3], assigned_to: p[4], due_at: p[12], escalated_at: p[14], escalated_to: p[15] });
    snap(); return { rows: [], rowCount: 1 };
  }
  if (q.startsWith('SELECT * FROM svc_approval_step_instances')) return { rows: [], rowCount: 0 };
  return { rows: [], rowCount: 0 };
}
class Pool { constructor() { ev({ pool: 'new' }); } on() { return this; } async query(t, p) { return answer(t, p); } async connect() { return { query: (t, p) => answer(t, p), release() {} }; } async end() {} }
const stub = { Pool, Client: Pool, types: { setTypeParser() {} } }; stub.default = stub;
const orig = Module._load;
Module._load = function (req, parent, isMain) { if (req === 'pg') return stub; return orig.apply(this, arguments); };
process.on('exit', (c) => ev({ exit: c }));
