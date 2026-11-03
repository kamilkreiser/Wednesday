// Gate 169 shared harness helpers (identical file in base and head trees).
import { writeFileSync, appendFileSync } from 'node:fs';
import Transport from 'winston-transport';
export const NET = 'preprod' as never;
export const PID = 'a'.repeat(56);
export const GENUINE = { amount: [{ unit: 'lovelace', quantity: '2000000' }, { unit: PID, quantity: '1' }] };
export const FOREIGN = { amount: [{ unit: 'lovelace', quantity: '2000000' }, { unit: 'f'.repeat(56), quantity: '1' }] };
export const lines: string[] = [];
export class Cap extends Transport {
  log(info: any, cb: () => void) {
    try { lines.push(JSON.stringify(info, (_k, v) => (typeof v === 'symbol' ? String(v) : v))); } catch { lines.push('<unserialisable info>'); }
    cb();
  }
}
export const typeName = (v: unknown): string => {
  try { if (v === null) return 'null'; if (typeof v !== 'object' && typeof v !== 'function') return typeof v; return Object.getPrototypeOf(v)?.constructor?.name ?? 'object'; } catch { return 'unreadable'; }
};
export function race<T>(p: Promise<T>, ms: number): Promise<{ s: 'resolved' | 'rejected' | 'pending'; v?: unknown; ms: number }> {
  const t0 = Date.now();
  return Promise.race([
    p.then((v) => ({ s: 'resolved' as const, v, ms: Date.now() - t0 }), (e) => ({ s: 'rejected' as const, v: e, ms: Date.now() - t0 })),
    new Promise<{ s: 'pending'; ms: number }>((r) => setTimeout(() => r({ s: 'pending', ms: Date.now() - t0 }), ms)),
  ]);
}
export function record(out: string, row: Record<string, unknown>) {
  appendFileSync(out, JSON.stringify(row) + '\n');
}
export function reset(out: string) { writeFileSync(out, ''); }
