// Gate 145 probe (never committed; copied into src/__tests__ only for its run, then removed by literal path).
// Runs the REAL executeErasure (services/gdprService.ts), the REAL lifecyclePayloadCodec, the REAL SubjectDekProvider,
// the REAL AES-GCM field crypto (@secuura/shared, test keys generated here) and the REAL winston logger.
// Replaced: ../db (an in-memory recording stand-in that answers each SQL the erasure issues), ../events (records the publish),
// and decryptField is wrapped ONLY to throw a hostile value for one row's context in the hostile modes.
import * as fs from 'node:fs';
import * as crypto from 'node:crypto';

const H: any = { mode: 'none', hostileCtx: '', sql: [] as string[], users: {} as any, events: [] as any[], keys: new Map<string, any>(), dsrUpdated: 0, published: [] as any[] };
(globalThis as any).__G145 = H;

jest.mock('../db', () => {
  const G = () => (globalThis as any).__G145;
  const text = (s: any) => (Array.isArray(s) ? s.join('?') : String(s)).replace(/\s+/g, ' ').trim();
  return {
    withPlatformScopeTransaction: async (fn: any) => fn({}),
    prisma: {
      $queryRaw: async (s: any, ...v: any[]) => {
        const t = text(s); const g = G(); g.sql.push('Q ' + t.slice(0, 60));
        if (t.startsWith('SELECT email FROM users')) return [{ email: g.users.email }];
        if (t.startsWith('SELECT id, payload FROM document_lifecycle_events')) return g.events.map((e: any) => ({ id: e.id, payload: e.payload }));
        if (t.startsWith('INSERT INTO data_deletion_log')) return [{ id: 'log-' + g.sql.length, user_id: v[0], dsr_id: v[1], data_type: v[2], records_affected: v[3], deletion_method: v[4], reason: v[5], performed_by: v[6], created_at: new Date(0) }];
        return [];
      },
      $executeRaw: async (s: any, ...v: any[]) => {
        const t = text(s); const g = G(); g.sql.push('X ' + t.slice(0, 60));
        if (t.startsWith('UPDATE document_lifecycle_events SET payload')) { const e = g.events.find((x: any) => x.id === v[1]); if (e) { e.payload = JSON.parse(v[0]); e.updated = true; } return e ? 1 : 0; }
        if (t.startsWith('UPDATE data_subject_requests')) { g.dsrUpdated++; return 1; }
        if (t.startsWith('UPDATE users SET')) { g.users.email = 'deleted_' + g.users.id + '@anonymized.local'; g.users.anonymised = true; return 1; }
        return 0;
      },
      $queryRawUnsafe: async (t0: string, ...p: any[]) => {
        const t = text(t0); const g = G(); g.sql.push('U ' + t.slice(0, 60));
        const id = p[0];
        if (t.startsWith('SELECT wrapped_dek')) { const r = g.keys.get(id); return r ? [r] : []; }
        if (t.startsWith('INSERT INTO pii_subject_keys')) { if (g.keys.has(id)) return []; g.keys.set(id, { wrapped_dek: p[1] ?? null, wrap_iv: p[2] ?? null, wrap_auth_tag: p[3] ?? null, kek_version: p[4] ?? 1, destroyed_at: p[1] == null ? new Date() : null }); return [{ subject_id: id }]; }
        if (t.startsWith('UPDATE pii_subject_keys')) { const r = g.keys.get(id); if (!r || r.destroyed_at) return []; Object.assign(r, { wrapped_dek: null, wrap_iv: null, wrap_auth_tag: null, destroyed_at: new Date() }); return [{ subject_id: id }]; }
        return [];
      },
    },
  };
});
jest.mock('../events', () => ({ EventTypes: { USER_ERASED: 'user.erased' }, publishEvent: async (type: string, data: any) => { (globalThis as any).__G145.published.push({ type, userId: data?.userId }); } }));
jest.mock('@secuura/shared', () => {
  const a = jest.requireActual('@secuura/shared');
  const revoked = () => { const r = Proxy.revocable({}, {}); r.revoke(); return r.proxy; };
  return {
    ...a,
    decryptField: (stored: any, ctx: string) => {
      const g = (globalThis as any).__G145;
      if (ctx === g.hostileCtx) {
        if (g.mode === 'revokedProxy') throw revoked();
        if (g.mode === 'getterThrows') throw Object.defineProperty(new Error('x'), 'message', { get() { throw new Error('inner getter'); } });
        if (g.mode === 'nullProto') throw Object.create(null);
      }
      return a.decryptField(stored, ctx);
    },
  };
});

import { executeErasure } from '../services/gdprService';
import { subjectDeks } from '../services/subjectDeks';
import { logger } from '../utils/logger';

const S: any = jest.requireActual('@secuura/shared');
const USER = '11111111-1111-4111-8111-111111111111', DSR = '22222222-2222-4222-8222-222222222222';
const EMAIL = 'subject.g145@example.test';
const ctx = (id: string) => `document_lifecycle_events.payload.${id}`;
const E1 = '33333333-3333-4333-8333-333333333331', E2 = '33333333-3333-4333-8333-333333333332';

it('g145 erasure probe', async () => {
  const mode = process.env.G145_MODE as string;
  const k1 = crypto.randomBytes(32).toString('hex'), k2 = crypto.randomBytes(32).toString('hex'); // generated test keys, never persisted
  S.__resetKeyringForTesting(); S.registerKey(1, k1); S.registerKey(2, k2);
  // E2 = the row whose decrypt fails. ordinary: encrypted under key v2, which is then NOT loaded during the erasure (the real decryptField throws a real Error).
  S.setActiveVersion(mode === 'ordinary' ? 2 : 1);
  const e2tok = S.encryptField(JSON.stringify({ recipient: 'Subject (' + EMAIL + ')' }), ctx(E2));
  S.setActiveVersion(1);
  const e1tok = S.encryptField(JSON.stringify({ note: 'sent to ' + EMAIL }), ctx(E1));
  S.__resetKeyringForTesting(); S.registerKey(1, k1); S.setActiveVersion(1);
  subjectDeks.__clearCacheForTesting();
  const dek = await subjectDeks.getOrCreateDek(USER);
  H.users = { id: USER, email: S.encryptFieldWithDek(EMAIL, `users.email.${USER}`, dek) };
  subjectDeks.__clearCacheForTesting();
  H.events = [{ id: E1, payload: e1tok, orig: e1tok }, { id: E2, payload: e2tok, orig: e2tok }];
  H.mode = mode; H.hostileCtx = ['revokedProxy', 'getterThrows', 'nullProto'].includes(mode) ? ctx(E2) : '';
  H.sql.length = 0;
  const lines: string[] = [];
  const tr: any = (logger as any).transports[0];
  const on = (info: any) => lines.push(String(info[Symbol.for('message')]).replace(/\u001b\[[0-9;]*m/g, '').replace(/^\S+ \S+ /, ''));
  tr.on('logged', on);
  let outcome: string;
  try { const r = await executeErasure(USER, DSR, 'admin-g145'); outcome = `RESOLVED success=${r.success} deletionLog=[${r.deletionLog.map((l) => l.dataType + ':' + l.recordsAffected + ':' + l.deletionMethod).join(', ')}]`; }
  catch (e: any) { outcome = 'REJECTED ' + (e?.constructor?.name ?? typeof e); }
  await new Promise((r) => setImmediate(r));
  tr.off('logged', on);
  // After-state + recoverability. "Anyone holding the platform keys": register the WHOLE platform keyring (v1 and v2) and try the skipped row.
  S.registerKey(2, k2);
  const after: any = {};
  for (const e of H.events) {
    const cur = e.payload;
    let plain: string; try { plain = typeof cur === 'string' && S.isEncryptedPii(cur) ? String(S.decryptField(cur, ctx(e.id))) : JSON.stringify(cur); } catch (x: any) { plain = 'DECRYPT FAILED: ' + x?.message; }
    after[e.id === E1 ? 'E1_control_row' : 'E2_failing_row'] = { rewritten: !!e.updated, stillOriginalCiphertext: cur === e.orig, platformKeyringDecrypts: !plain.startsWith('DECRYPT FAILED'), containsSubjectEmail: plain.toLowerCase().includes(EMAIL), plaintextShape: plain.replace(EMAIL, '<SUBJECT_EMAIL>').slice(0, 90) };
  }
  subjectDeks.__clearCacheForTesting();
  const dekAfter = await subjectDeks.getDek(USER);
  const keyRow = H.keys.get(USER);
  const res = {
    mode, outcome,
    steps: { dsrMarkedCompleted: H.dsrUpdated > 0, userRowAnonymised: !!H.users.anonymised, subjectDekDestroyed: !!keyRow?.destroyed_at && keyRow?.wrapped_dek == null, userErasedPublished: H.published.length },
    after,
    subjectDekCiphertextAfter: H.users.anonymised ? 'users.email overwritten by step 10' : (dekAfter ? 'subject DEK still live: users.email d1 decrypts' : 'subject DEK gone'),
    subjectDekLiveAfter: !!dekAfter,
    sqlTail: H.sql.filter((s: string) => !s.includes('data_deletion_log')).map((s: string) => s.slice(0, 50)),
    logs: lines.filter((l) => /lifecycle|Erasure|erased|DSR/i.test(l)).map((l) => l.replace(EMAIL, '<SUBJECT_EMAIL>')),
  };
  fs.writeFileSync(process.env.G145_OUT as string, JSON.stringify(res, null, 1));
}, 60_000);
