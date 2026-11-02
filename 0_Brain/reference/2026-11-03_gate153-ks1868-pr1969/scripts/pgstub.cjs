// Gate 153: replaces ONLY the 'pg' module for a real referral-service process (tsx, real index.ts, real db.ts,
// real referral/milestone/fraud services, real winston logger). One in-memory store models svc_referral_codes,
// svc_referrals, svc_referral_rewards, svc_referral_milestones (PK user_id, ON CONFLICT upsert),
// svc_referral_milestones_rewards (PK id, ON CONFLICT DO NOTHING; G153_MR=absent makes it a missing relation, as in
// the repo's DDL which never creates it) and svc_referral_fraud_log. Autocommit per statement, as pool.query is.
const Module = require('module');
const fs = require('fs');
const OUT = process.env.G153_OUT, SNAP = OUT + '.snap.json';
const SCEN = process.env.G153_SCEN || 'none', KIND = process.env.G153_KIND || 'none', MR = process.env.G153_MR || 'present';
const ev = (o) => fs.appendFileSync(OUT, JSON.stringify({ t: Date.now(), ...o }) + '\n');
function hostile() {
  switch (KIND) {
    case 'ordinary': return new Error('db down');
    case 'string': return 'plain boom';
    case 'revokedProxy': { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; }
    case 'throwingGetter': return Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } });
    default: return null;
  }
}
const REF = '11111111-1111-4111-8111-111111111111', BAD = '22222222-2222-4222-8222-222222222222', NEWU = '33333333-3333-4333-8333-333333333333';
const REF2 = '44444444-4444-4444-8444-444444444444', GEN = '55555555-5555-4555-8555-555555555555';
const past = new Date(Date.now() - 86400e3).toISOString();
const codes = new Map(), referrals = new Map(), rewards = new Map(), ms = new Map(), mr = new Map(), fraud = [];
codes.set('c-ref', { id: 'c-ref', code: 'GATE1530', owner_id: REF, owner_wallet_address: null, is_active: true, max_uses: 100000, current_uses: 0, custom_label: null, metadata: '{}', created_at: past, expires_at: null });
for (let i = 0; i < 5; i++) codes.set('c-gen' + i, { id: 'c-gen' + i, code: 'GENC000' + i, owner_id: GEN, owner_wallet_address: null, is_active: true, max_uses: 100, current_uses: 0, custom_label: null, metadata: '{}', created_at: past, expires_at: null });
for (let i = 0; i < 1000; i++) referrals.set('r' + i, { id: 'r' + i, referral_code_id: 'c-ref', referrer_id: REF, referred_user_id: 'u' + i, referred_wallet_address: null, status: 'QUALIFIED', referrer_reward: '50000000', referred_reward: '25000000', fraud_check_passed: true, fraud_flags: '[]', metadata: '{}', created_at: past, qualified_at: past, reward_distributed_at: null });
referrals.set('r2', { id: 'r2', referral_code_id: 'c-x', referrer_id: REF2, referred_user_id: 'v1', status: 'QUALIFIED', referrer_reward: '50000000', referred_reward: '25000000', fraud_check_passed: true, fraud_flags: '[]', metadata: '{}', created_at: past, qualified_at: past });
const TIERS = [['milestone-first', 'FIRST_REFERRAL', '100000000'], ['milestone-bronze', 'BRONZE', '500000000'], ['milestone-silver', 'SILVER', '2500000000'], ['milestone-gold', 'GOLD', '10000000000'], ['milestone-platinum', 'PLATINUM', '50000000000'], ['milestone-ambassador', 'AMBASSADOR', '100000000000']];
ms.set(REF, { user_id: REF, milestones_completed: JSON.stringify(TIERS.map(([id, tier, amt]) => ({ milestoneId: id, tier, achievedAt: past, rewardAmount: amt }))), total_referrals: 1000, total_rewards_earned: '163100000000', current_tier: 'AMBASSADOR' });
if (MR === 'present') for (const [id, tier, amt] of TIERS) mr.set('prior-' + id, { id: 'prior-' + id, user_id: REF, type: 'MILESTONE_REWARD', amount: amt, status: 'CLAIMED', source_id: id, source_type: 'MILESTONE', created_at: past, metadata: '{}' });
fraud.push({ ip_address: '10.9.9.9', device_fingerprint: 'dev-x', referrer_id: BAD, flag_type: 'KNOWN_FRAUD' });
for (let i = 0; i < 3; i++) fraud.push({ ip_address: '10.9.9.9', device_fingerprint: 'dev-x', referrer_id: 'someone' + i, flag_type: 'SYBIL_PATTERN' });
const snap = () => fs.writeFileSync(SNAP, JSON.stringify({
  codesByGEN: [...codes.values()].filter((c) => c.owner_id === GEN).length,
  referralsForBAD: [...referrals.values()].filter((r) => r.referred_user_id === BAD).map((r) => ({ status: r.status, fraud_check_passed: r.fraud_check_passed, fraud_flags: r.fraud_flags })),
  rewards: [...rewards.values()].map((r) => ({ user: r.user_id === BAD ? 'BAD' : r.user_id === REF ? 'REF' : r.user_id, type: r.type, amount: r.amount, status: r.status })),
  msRow: ms.get(REF) ? { tiers: JSON.parse(ms.get(REF).milestones_completed).map((m) => m.tier + '@' + String(m.achievedAt).slice(0, 10)), total_rewards_earned: ms.get(REF).total_rewards_earned, current_tier: ms.get(REF).current_tier } : null,
  msRowREF2: ms.get(REF2) ? JSON.parse(ms.get(REF2).milestones_completed).length : null,
  milestoneRewardsREF: [...mr.values()].filter((r) => r.user_id === REF).map((r) => r.source_id.replace('milestone-', '') + ':' + r.status),
  milestoneRewardsREF2: [...mr.values()].filter((r) => r.user_id === REF2).length,
  fraudLogRows: fraud.length }, null, 1));
snap();
const fail = (cond) => { if (cond && KIND !== 'none') { ev({ injected: SCEN }); throw hostile(); } };
const missing = () => { const e = new Error('relation "svc_referral_milestones_rewards" does not exist'); e.code = '42P01'; throw e; };
async function answer(text, params) {
  const q = String(text).replace(/\s+/g, ' ').trim();
  ev({ sql: q.slice(0, 80) });
  if (q === 'SELECT 1 AS ok') return { rows: [{ ok: 1 }], rowCount: 1 };
  if (q.startsWith('SELECT COUNT(*) as count FROM svc_referral_codes')) { fail(SCEN === 'boot_refverify'); return { rows: [{ count: codes.size }] }; }
  if (q.startsWith('SELECT COUNT(*) as count FROM')) return { rows: [{ count: 0 }] };
  if (q.startsWith('SELECT COUNT(*) AS cnt FROM svc_referral_milestones')) { fail(SCEN === 'boot_msverify'); return { rows: [{ cnt: ms.size }] }; }
  if (q.startsWith('SELECT ip_address, device_fingerprint')) { fail(SCEN === 'boot_fraudload'); return { rows: fraud.map((r) => ({ ...r })) }; }
  if (q.startsWith('INSERT INTO svc_referral_fraud_log')) { fraud.push({ ip_address: params[0], device_fingerprint: params[1], referrer_id: params[2], flag_type: params[3] }); snap(); return { rows: [] }; }
  if (q.startsWith('SELECT * FROM svc_referral_milestones WHERE user_id')) { fail(SCEN.startsWith('award_read')); const r = ms.get(params[0]); return { rows: r ? [{ ...r }] : [] }; }
  if (q.startsWith('INSERT INTO svc_referral_milestones (')) { fail(SCEN === 'award_read_wfail'); ms.set(params[0], { user_id: params[0], milestones_completed: params[1], total_referrals: params[2], total_rewards_earned: params[3], current_tier: params[4] }); snap(); return { rows: [] }; }
  if (q.startsWith('SELECT * FROM svc_referral_milestones_rewards')) { if (MR !== 'present') missing(); fail(SCEN === 'rewards_read'); const rows = [...mr.values()].filter((r) => r.user_id === params[0] && (r.status === params[1] || r.status === params[2])); return { rows }; }
  if (q.startsWith('INSERT INTO svc_referral_milestones_rewards')) { if (MR !== 'present') missing(); fail(SCEN === 'award_read_wfail'); if (!mr.has(params[0])) mr.set(params[0], { id: params[0], user_id: params[1], type: params[2], amount: params[3], status: params[4], source_id: params[5], source_type: params[6], created_at: params[7], metadata: params[8] }); snap(); return { rows: [] }; }
  if (q.startsWith('SELECT * FROM svc_referral_codes WHERE owner_id')) { fail(SCEN === 'gen_owner' || SCEN === 'gen_all'); const rows = [...codes.values()].filter((c) => c.owner_id === params[0]); return { rows }; }
  if (q.startsWith('SELECT * FROM svc_referral_codes WHERE code')) { fail(SCEN === 'gen_all'); const rows = [...codes.values()].filter((c) => c.code === params[0]); return { rows }; }
  if (q.startsWith('SELECT * FROM svc_referral_codes WHERE id')) { const r = codes.get(params[0]); return { rows: r ? [r] : [] }; }
  if (q.startsWith('INSERT INTO svc_referral_codes')) { fail(SCEN === 'gen_all'); const p = params; const prev = codes.get(p[0]); codes.set(p[0], prev ? { ...prev, is_active: p[4], current_uses: p[6] } : { id: p[0], code: p[1], owner_id: p[2], owner_wallet_address: p[3], is_active: p[4], max_uses: p[5], current_uses: p[6], custom_label: p[7], metadata: p[8], created_at: p[9], expires_at: p[10] }); snap(); return { rows: [] }; }
  if (q.startsWith('SELECT * FROM svc_referrals WHERE referrer_id')) { const rows = [...referrals.values()].filter((r) => r.referrer_id === params[0]); return { rows }; }
  if (q.startsWith('SELECT * FROM svc_referrals WHERE referred_user_id = $1 AND status')) { const rows = [...referrals.values()].filter((r) => r.referred_user_id === params[0] && r.status === params[1]); return { rows: rows.slice(0, 1) }; }
  if (q.startsWith('SELECT * FROM svc_referrals WHERE referred_user_id')) { const rows = [...referrals.values()].filter((r) => r.referred_user_id === params[0]); return { rows: rows.slice(0, 1) }; }
  if (q.startsWith('INSERT INTO svc_referrals')) { const p = params; const prev = referrals.get(p[0]); referrals.set(p[0], { ...(prev || {}), id: p[0], referral_code_id: p[1], referrer_id: p[2], referred_user_id: p[3], status: p[5], referrer_reward: p[6], referred_reward: p[7], fraud_check_passed: p[8], fraud_flags: p[9], metadata: p[10], created_at: p[11], qualified_at: p[12] }); snap(); return { rows: [] }; }
  if (q.startsWith('SELECT * FROM svc_referral_rewards WHERE user_id')) { return { rows: [...rewards.values()].filter((r) => r.user_id === params[0]) }; }
  if (q.startsWith('SELECT * FROM svc_referral_rewards WHERE id')) { const r = rewards.get(params[0]); return { rows: r && r.user_id === params[1] ? [r] : [] }; }
  if (q.startsWith('INSERT INTO svc_referral_rewards')) { const p = params; const prev = rewards.get(p[0]); rewards.set(p[0], { ...(prev || {}), id: p[0], user_id: p[1], type: p[2], amount: p[3], status: p[4], source_id: p[5], source_type: p[6], metadata: p[8], created_at: p[9], claimed_at: p[10] }); snap(); return { rows: [] }; }
  ev({ unmodelled: q.slice(0, 80) });
  return { rows: [], rowCount: 0 };
}
class Pool { constructor() { ev({ pool: 'new' }); } on() { return this; } async query(t, p) { return answer(t, p); } async connect() { return { query: (t, p) => answer(t, p), release() {} }; } async end() {} }
const stub = { Pool, Client: Pool, types: { setTypeParser() {} } }; stub.default = stub;
const orig = Module._load;
Module._load = function (req, parent, isMain) { if (req === 'pg') return stub; return orig.apply(this, arguments); };
process.on('exit', (c) => ev({ exit: c }));
