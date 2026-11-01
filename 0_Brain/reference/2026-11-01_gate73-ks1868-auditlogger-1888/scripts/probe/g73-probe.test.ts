// Gate 73 probe cells (NOT part of the PR). Lives outside the repo; run with scripts/vitest.probe.config.ts.
// Imports the product by absolute path so mutants applied to the working tree are measured.
import { describe, it, expect, vi, beforeEach } from 'vitest';
import crypto from 'crypto';

const h = vi.hoisted(() => ({ error: vi.fn() }));
vi.mock('/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate73-ks1868-auditlogger-1888/repo/Blockchain/Dev/packages/shared/src/logger', () => ({
  logger: { debug: vi.fn(), info: vi.fn(), warn: vi.fn(), error: h.error },
}));

import {
  AuditLogger,
  AuditEventCategory,
  AuditEvent,
} from '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-01_gate73-ks1868-auditlogger-1888/repo/Blockchain/Dev/packages/shared/src/security/audit-logger';

function revoked(): unknown {
  const { proxy, revoke } = Proxy.revocable({}, {});
  revoke();
  return proxy;
}
function hostileGetter(): unknown {
  return Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } });
}

// failPlan: per call index, a value to reject with, or undefined to accept.
function mk(hashIntegrity: boolean, failFor: (ev: AuditEvent, attempt: number) => unknown, maxBatchSize = 1000) {
  const delivered: AuditEvent[] = [];
  const attempts = new Map<string, number>();
  let calls = 0;
  const audit = new AuditLogger({
    serviceName: 'svc', version: '1', environment: 'test', hashIntegrity, maxBatchSize, flushIntervalMs: 3600000,
    onEvent: (ev) => {
      calls++;
      const n = (attempts.get(ev.id) ?? 0) + 1;
      attempts.set(ev.id, n);
      const v = failFor(ev, n);
      if (v !== undefined) return Promise.reject(v);
      delivered.push(ev);
      return Promise.resolve();
    },
  });
  return { audit, delivered, attempts, calls: () => calls, buf: () => (audit as any).eventBuffer as AuditEvent[] };
}

function verifyChain(events: AuditEvent[]): boolean {
  let prev = '';
  for (const e of events) {
    const { hash, ...rest } = e;
    const want = crypto.createHash('sha256').update(JSON.stringify({ ...rest, previousHash: prev })).digest('hex');
    if (want !== hash) return false;
    prev = hash!;
  }
  return true;
}

async function flushSafe(a: AuditLogger): Promise<boolean> {
  try { await a.flush(); return false; } catch { return true; }
}

const FLUSH_ERRORS = () => h.error.mock.calls.filter((c) => String(c[0]) === 'Failed to process audit event');

describe('gate73 probe', () => {
  beforeEach(() => h.error.mockReset());

  for (const hi of [false, true]) {
    for (const [label, mkv] of [['readable Error', () => new Error('sink down')], ['revoked Proxy', revoked], ['throwing getter', hostileGetter]] as const) {
      it(`P1 hashIntegrity=${hi} ${label}: single event re-buffered once, same object/id/hash, delivered once, chain verifies`, async () => {
        const t = mk(hi, (_e, n) => (n === 1 ? (mkv as () => unknown)() : undefined));
        const ev = await t.audit.log(AuditEventCategory.SECURITY, 'P1');
        const threw = await flushSafe(t.audit);
        expect(threw).toBe(false);
        expect(t.buf()).toHaveLength(1);
        expect(t.buf()[0]).toBe(ev);
        await t.audit.flush();
        t.audit.stopFlushTimer();
        expect(t.delivered).toHaveLength(1);
        expect(t.delivered[0].id).toBe(ev.id);
        expect(t.delivered[0].hash).toBe(ev.hash);
        expect(t.buf()).toHaveLength(0);
        if (hi) { expect(typeof ev.hash).toBe('string'); expect(verifyChain(t.delivered)).toBe(true); }
        else expect(ev.hash).toBeUndefined();
        expect(FLUSH_ERRORS()).toHaveLength(1);
        expect(Object.keys(FLUSH_ERRORS()[0][1])).toEqual(['error']);
      });
    }

    it(`P2 hashIntegrity=${hi}: 3 events, middle one rejects with a revoked Proxy once: flush resolves, A and C delivered in pass 1, B in pass 2, each exactly once`, async () => {
      const t = mk(hi, (e, n) => (e.action === 'B' && n === 1 ? revoked() : undefined));
      const a = await t.audit.log(AuditEventCategory.SECURITY, 'A');
      const b = await t.audit.log(AuditEventCategory.SECURITY, 'B');
      const c = await t.audit.log(AuditEventCategory.SECURITY, 'C');
      expect(await flushSafe(t.audit)).toBe(false);
      expect(t.delivered.map((e) => e.action)).toEqual(['A', 'C']);
      expect(t.buf().map((e) => e.action)).toEqual(['B']);
      await t.audit.flush();
      t.audit.stopFlushTimer();
      expect(t.delivered.map((e) => e.id)).toEqual([a.id, c.id, b.id]);
      expect(new Set(t.delivered.map((e) => e.id)).size).toBe(3);
      if (hi) {
        // the chain verifies in LOG order (it is computed at log()), not in delivery order
        expect(verifyChain([a, b, c])).toBe(true);
        expect(verifyChain(t.delivered)).toBe(false);
      }
    });

    it(`P3 hashIntegrity=${hi}: 3 events all reject once (mixed readable/hostile): buffer order after the failed pass, delivery order after retry`, async () => {
      const vals: Record<string, () => unknown> = { A: () => new Error('x'), B: revoked, C: hostileGetter };
      const t = mk(hi, (e, n) => (n === 1 ? vals[e.action]() : undefined));
      for (const k of ['A', 'B', 'C']) await t.audit.log(AuditEventCategory.SECURITY, k);
      expect(await flushSafe(t.audit)).toBe(false);
      const bufOrder = t.buf().map((e) => e.action).join('');
      await t.audit.flush();
      t.audit.stopFlushTimer();
      const delOrder = t.delivered.map((e) => e.action).join('');
      console.log(`G73_ORDER hashIntegrity=${hi} buffer_after_fail=${bufOrder} delivered_after_retry=${delOrder}`);
      expect(t.delivered).toHaveLength(3);
      expect(new Set(t.delivered.map((e) => e.id)).size).toBe(3);
      expect(FLUSH_ERRORS()).toHaveLength(3);
      expect(FLUSH_ERRORS().map((c) => c[1].error)).toEqual(['x', 'unreadable thrown value', 'unreadable thrown value']);
      // pin the observed (pre-existing) order so a mutant that changes it is visible
      expect(bufOrder).toBe('CBA');
    });
  }

  it('P4 a log() racing an in-flight failing flush: the late event is not lost or duplicated', async () => {
    let release!: (v: unknown) => void;
    let first = true;
    const delivered: string[] = [];
    const audit = new AuditLogger({
      serviceName: 'svc', version: '1', environment: 'test', hashIntegrity: true, maxBatchSize: 1000, flushIntervalMs: 3600000,
      onEvent: (ev) => {
        if (first) { first = false; return new Promise((_r, rej) => { release = rej; }); }
        delivered.push(ev.action);
        return Promise.resolve();
      },
    });
    await audit.log(AuditEventCategory.SECURITY, 'A');
    const p = audit.flush();
    await audit.log(AuditEventCategory.SECURITY, 'LATE');
    release(revoked());
    await p;
    const bufOrder = (audit as any).eventBuffer.map((e: AuditEvent) => e.action).join(',');
    await audit.flush();
    audit.stopFlushTimer();
    console.log(`G73_RACE buffer_after_fail=${bufOrder} delivered=${delivered.join(',')}`);
    expect(delivered.sort()).toEqual(['A', 'LATE']);
  });

  for (const [label, mkv] of [['readable Error', () => new Error('down')], ['revoked Proxy', revoked]] as const) {
    it(`P5 repeated rejection (${label}), maxBatchSize=3, 10 log() calls: buffer growth and onEvent call count`, async () => {
      const t = mk(true, () => (mkv as () => unknown)(), 3);
      let logRejects = 0;
      for (let i = 0; i < 10; i++) {
        try { await t.audit.log(AuditEventCategory.SECURITY, `E${i}`); } catch { logRejects++; }
      }
      t.audit.stopFlushTimer();
      console.log(`G73_STORM ${label}: buffer=${t.buf().length} onEvent_calls=${t.calls()} log_rejects=${logRejects} flush_error_logs=${FLUSH_ERRORS().length}`);
      expect(t.buf().length).toBe(10);
    });
  }
});
