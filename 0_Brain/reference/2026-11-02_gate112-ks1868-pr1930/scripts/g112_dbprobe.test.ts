// QA GATE 112 db probe (not part of the PR): REAL db.ts initDb/probeDb/runDbReadyHook, only `pg` replaced.
import { describe, it, vi } from 'vitest';
import { appendFileSync } from 'fs';
process.env.DATABASE_URL = 'postgres://gate112:stub@127.0.0.1:1/gate112';
const OUT = process.env.PROBE_OUT as string;
const h = vi.hoisted(() => ({ probeFail: false, toThrow: undefined as unknown }));
vi.mock('pg', () => {
  class Pool { constructor(_o?: unknown) {} on() { return this; } connect() { return Promise.reject(new Error('no client')); }
    query(text: string) { if (/SELECT 1 AS ok/.test(text) && h.probeFail) return Promise.reject(h.toThrow); return Promise.resolve({ rows: [{ ok: 1 }], rowCount: 1 }); }
    end() { return Promise.resolve(); } }
  return { Pool, default: { Pool } };
});
const SECRET = 'G112-SECRET-IN-MESSAGE';
function withMsg(get: () => unknown) { return Object.create(Error.prototype, { message: { get, configurable: true } }); }
const KINDS: Record<string, () => unknown> = {
  ordinary: () => new Error('db down ' + SECRET),
  revokedProxy: () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; },
  getterThrows: () => withMsg(() => { throw new Error('getter boom ' + SECRET); }),
  nullProto: () => Object.create(null),
  plainString: () => 'db down ' + SECRET,
  msgSymbol: () => withMsg(() => Symbol(SECRET)),
  msgRevokedProxy: () => withMsg(() => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }),
  msgBigInt: () => withMsg(() => 1868n),
  msgToStringThrows: () => withMsg(() => ({ toString() { throw new Error('toString boom'); } })),
};
async function cell(site: string, kind: string) {
  vi.resetModules();
  const lines: string[] = [];
  const spy = vi.spyOn(console, 'log').mockImplementation((...a: unknown[]) => { try { lines.push(a.map(String).join(' ')); } catch { lines.push('<unprintable>'); } });
  h.probeFail = site === 'probe'; h.toThrow = KINDS[kind]();
  const db = await import('../db');
  let outcome: Record<string, unknown>;
  try {
    const v = site === 'probe' ? await db.initDb() : await db.initDb(async () => { throw KINDS[kind](); });
    outcome = { resolved: true, value: v };
  } catch (e) { let n = '?'; try { n = (e as Error).constructor.name + ': ' + String((e as Error).message).slice(0, 80); } catch { /* */ } outcome = { resolved: false, threw: n }; }
  const avail = db.isDbAvailable();
  await db.closeDb();
  spy.mockRestore();
  appendFileSync(OUT, JSON.stringify({ cell: site, kind, ...outcome, isDbAvailable: avail, valueLeak: lines.filter((l) => l.includes(SECRET)).length,
    unreadableConst: lines.some((l) => l.includes('unreadable thrown value')), logs: lines.map((l) => l.slice(0, 200)) }) + '\n');
}
describe('gate 112 db probe', () => {
  for (const k of Object.keys(KINDS)) {
    it(`probeDb rejects ${k}`, async () => { await cell('probe', k); });
    it(`ready hook throws ${k}`, async () => { await cell('hook', k); });
  }
});
