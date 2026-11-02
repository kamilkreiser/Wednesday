// gate 101 probe B + D (NOT part of the PR): real notificationClient, real verifyDbReady x2.
import * as fs from 'fs';
const OUT = process.env.PROBE_OUT as string;
const emit = (o: unknown) => fs.appendFileSync(OUT, JSON.stringify(o) + '\n');
const logs: any[] = [];
const sent: any[] = [];
const mockFetch = jest.fn();
jest.mock('../utils/logger', () => ({ logger: {
  info: (...a: any[]) => logs.push(['info', ...a]), warn: (...a: any[]) => logs.push(['warn', ...a]),
  error: (...a: any[]) => logs.push(['error', ...a]), debug: () => {} } }));
jest.mock('../services/email', () => ({
  sendEmail: jest.fn(async (o: any) => { sent.push({ fn: 'sendEmail', to: o.to }); }),
  sendCertificationNotification: jest.fn(async (to: string, t: string, c: string) => { sent.push({ fn: 'cert', to, t, c }); }),
  sendRevocationNotification: jest.fn(async (to: string) => { sent.push({ fn: 'rev', to }); }),
  sendShareNotification: jest.fn(async (to: string) => { sent.push({ fn: 'share', to }); }),
  isEmailConfigured: () => true,
}));
jest.mock('../db', () => ({ prisma: { $queryRaw: jest.fn() } }));
import { notifyDocumentCertified } from '../utils/notificationClient';
import * as certRepo from '../repositories/certificationRepo';
import * as docRepo from '../repositories/documentRepo';

function revokedProxy(): object { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }
function throwingGetter(): Error { const e = new Error('hidden'); Object.defineProperty(e, 'message', { get() { throw new Error('getter'); } }); return e; }
const KINDS: Record<string, () => unknown> = { ordinaryError: () => new Error('svc down'), string: () => 'plain', revokedProxy, throwingGetter };
const TO = 'recipient-secret@example.test', TITLE = 'CONFIDENTIAL-TITLE-77';

describe('probe B notification', () => {
  for (const k of Object.keys(KINDS)) {
    it(`B service-down ${k}`, async () => {
      logs.length = 0; sent.length = 0; (globalThis as any).fetch = mockFetch;
      mockFetch.mockReset(); mockFetch.mockRejectedValueOnce(KINDS[k]());
      const out = await notifyDocumentCertified({ toEmail: TO, documentTitle: TITLE, certifierName: 'cn', certificationId: 'c1', certifiedAt: 'now' } as any).then(() => 'resolved', () => 'REJECTED');
      const warnLines = logs.filter((l) => l[0] === 'warn' || l[0] === 'error');
      const txtWarn = JSON.stringify(warnLines);
      emit({ probe: 'B', kind: k, out, sent, logs, warnHasRecipient: txtWarn.includes(TO), warnHasTitle: txtWarn.includes(TITLE), allHasTitle: JSON.stringify(logs).includes(TITLE), allHasRecipient: JSON.stringify(logs).includes(TO) });
    });
  }
});

describe('probe D verifyDbReady', () => {
  for (const [name, mod] of [['cert', certRepo], ['doc', docRepo]] as const) {
    for (const k of Object.keys(KINDS)) {
      it(`D ${name} ${k}`, async () => {
        logs.length = 0;
        const db: any = { $queryRaw: async () => { throw KINDS[k](); } };
        let thrown: any = null; let msg = 'NA';
        try { await (mod as any).verifyDbReady(db); } catch (e) { thrown = e; }
        try { msg = thrown?.message; } catch { msg = 'UNREADABLE'; }
        // index.ts:514 catch reads err?.message
        emit({ probe: 'D', repo: name, kind: k, thrownIsError: thrown instanceof Error, thrownCtor: thrown?.constructor?.name, indexCatchMessage: msg, logs });
      });
    }
  }
});
