// Gate 177 Q3 + Q4a recorder: the REAL IdentusClient.resolveDID and the REAL ServiceClient.healthCheck, with the global
// fetch replaced per cell (no socket opens). Q3 callers: the REAL DIDManager / DIDResolver with their `client` /
// `prismClient` field REPLACED by a real IdentusClient (the repo wires a MockPRISMClient there; see the verdict), so the
// caller lines 89/128/181 (did-manager) and 140 (resolver) are driven against IdentusClient's answers.
import { it, vi } from 'vitest';
import { appendFileSync } from 'node:fs';
import { IdentusClient } from '../prism/identus-client';
import { DIDManager } from '../prism/did-manager';
import { DIDResolver } from '../prism/resolver';
import { ServiceClient } from '../resilience/service-client';
import { VALUES, SENT, capture, kind, hits } from './values';
import { logger as pkgLogger } from '../logger';
import { createLogger } from '../utils/logger';

const OUT = process.env.GATE177_OUT!;
const TAG = process.env.GATE177_TAG!;
const rec = (o: Record<string, unknown>) => appendFileSync(OUT, JSON.stringify({ tag: TAG, ...o }) + '\n');
const norm = (s: unknown) => (typeof s === 'string' ? s.replace(/SNTL177[-\w]*/g, 'S') : `<${typeof s}>`);
const sentIn = (x: unknown) => { try { return JSON.stringify(x ?? null, (_k, v) => (typeof v === 'bigint' || typeof v === 'symbol' ? String(v) : v)).includes(SENT) ? 1 : 0; } catch { return -1; } };

const DOC = { '@context': ['https://www.w3.org/ns/did/v1'], id: 'did:prism:gate177', verificationMethod: [] };
const okRes = (body: unknown) => ({ ok: true, status: 200, json: async () => body, text: async () => '' });
// fetch behaviours per trigger. `mk` yields a fresh hostile value.
const FETCH: Record<string, (mk: () => unknown) => (url: string, init?: any) => Promise<any>> = {
  'T1 fetch rejects': (mk) => async () => { throw mk(); },
  'T2 response.json rejects': (mk) => async () => ({ ok: true, status: 200, json: async () => { throw mk(); }, text: async () => '' }),
  'T3 response.ok getter throws': (mk) => async () => ({ get ok(): boolean { throw mk(); }, status: 200, json: async () => ({ didDocument: DOC }), text: async () => '' }),
};

async function cell<T>(fn: () => Promise<T>) {
  return capture(async () => {
    try { return { outcome: 'resolved', r: await fn() } as const; } catch (e) { return { outcome: 'REJECTED', e } as const; }
  });
}

it('gate177 Q5 log-capture positive control', async () => {
  const a = await capture(async () => { pkgLogger.error('gate177 control', { e: SENT + '-ctl' }); });
  const c = await capture(async () => { createLogger('service-client').error('gate177 control ' + SENT); });
  const d = await capture(async () => { console.error(SENT); });
  rec({ q: 'Q5C', site: 'log capture', value: 'package logger (../logger) error', lines: a.lines.length, logSentinel: hits(a.lines) });
  rec({ q: 'Q5C', site: 'log capture', value: 'utils/logger createLogger(service-client) error', lines: c.lines.length, logSentinel: hits(c.lines) });
  rec({ q: 'Q5C', site: 'log capture', value: 'console.error', lines: d.lines.length, logSentinel: hits(d.lines) });
});

it('gate177 Q3 IdentusClient.resolveDID + callers', async () => {
  // controls: a found DID, and an ordinary agent 404, no hostile value
  for (const [name, f] of [
    ['C1 agent returns a DID document', async () => okRes({ didDocument: DOC })],
    ['C2 agent answers 404 (agentFetch throws its own Error)', async () => ({ ok: false, status: 404, json: async () => ({}), text: async () => 'nope' })],
  ] as const) {
    vi.stubGlobal('fetch', f);
    const { result } = await cell(() => new IdentusClient({ cloudAgentUrl: 'http://agent.invalid' }).resolveDID('did:prism:gate177'));
    const r: any = (result as any).r;
    rec({ q: 'Q3C', site: 'controls', value: name, outcome: result.outcome, docNull: r ? r.didDocument === null : undefined, error: r?.didResolutionMetadata?.error, errorMessage: norm(r?.didResolutionMetadata?.errorMessage) });
    vi.unstubAllGlobals();
  }
  for (const [t, F] of Object.entries(FETCH)) {
    for (const [vname, mk] of VALUES) {
      let orig: unknown; const mk2 = () => (orig = mk());
      vi.stubGlobal('fetch', F(mk2));
      const { result, lines } = await cell(() => new IdentusClient({ cloudAgentUrl: 'http://agent.invalid' }).resolveDID('did:prism:gate177'));
      vi.unstubAllGlobals();
      const r: any = (result as any).r;
      const em = r?.didResolutionMetadata?.errorMessage;
      rec({ q: 'Q3', site: 'resolveDID ' + t, value: vname, outcome: result.outcome, docNull: r ? r.didDocument === null : undefined,
        docNonNull: r ? r.didDocument !== null && r.didDocument !== undefined : undefined,
        error: r?.didResolutionMetadata?.error, errorMessageType: r ? typeof em : undefined, errorMessage: r ? norm(em) : undefined,
        rejectKind: result.outcome === 'REJECTED' ? kind((result as any).e, orig) : undefined, answerSentinel: sentIn(r), logSentinel: hits(lines) });
    }
  }
  // callers (T1 fetch rejects only, plus the C1 control)
  const callers: Array<[string, (c: IdentusClient) => Promise<unknown>]> = [
    ['did-manager:89 createIssuerDID', async (c) => { const m: any = new DIDManager({ autoRegisterIssuerProfile: false }); m.client = c; return m.createIssuerDID('gate177'); }],
    ['did-manager:128 connectExistingDID', async (c) => { const m: any = new DIDManager(); m.client = c; return m.connectExistingDID('did:prism:gate177', 'gate177'); }],
    ['did-manager:181 getDIDDocument', async (c) => { const m: any = new DIDManager(); m.client = c; return m.getDIDDocument('did:prism:gate177'); }],
    ['resolver:140 resolve(did:prism)', async (c) => { const r: any = new DIDResolver({ cacheEnabled: true }); r.prismClient = c; const out = await r.resolve('did:prism:gate177'); return { out, cached: r.cache.size }; }],
  ];
  for (const [site, call] of callers) {
    for (const [vname, mk] of [['C1 control: agent returns a document', null] as const, ...VALUES]) {
      let orig: unknown;
      let n = 0;
      vi.stubGlobal('fetch', async (url: string) => {
        n++;
        if (String(url).includes('did-registrar')) return okRes({ longFormDid: 'did:prism:gate177', scheduledOperation: { id: 'op1', didRef: 'x', status: 'PENDING' } });
        if (mk === null) return okRes({ didDocument: DOC });
        throw (orig = (mk as () => unknown)());
      });
      const { result, lines } = await cell(() => call(new IdentusClient({ cloudAgentUrl: 'http://agent.invalid' })));
      vi.unstubAllGlobals();
      const r: any = (result as any).r;
      let shape: string;
      try { shape = result.outcome === 'resolved' ? norm(JSON.stringify(r, (_k, v) => (typeof v === 'symbol' || typeof v === 'bigint' ? `<${typeof v}>` : v))).replace(/"(created|updated|expiresAt|challenge|id)":"[^"]*"/g, '"$1":"…"') : ''; } catch { shape = '<unserialisable>'; }
      let rk: string | undefined;
      if (result.outcome === 'REJECTED') { const e: any = (result as any).e; rk = kind(e, orig); }
      rec({ q: 'Q3callers', site, value: vname, outcome: result.outcome, shape: shape.slice(0, 300), rejectKind: rk, fetchCalls: n, answerSentinel: sentIn(r), logSentinel: hits(lines) });
    }
  }
});

it('gate177 Q4a ServiceClient.healthCheck', async () => {
  for (const [name, f] of [
    ['C1 service answers 200', async () => ({ ok: true, status: 200 })],
    ['C2 service answers 503', async () => ({ ok: false, status: 503 })],
  ] as const) {
    vi.stubGlobal('fetch', f);
    const { result } = await cell(() => new ServiceClient({ baseUrl: 'http://svc.invalid', serviceName: 'g177', retries: 0 }).healthCheck());
    vi.unstubAllGlobals();
    const r: any = (result as any).r;
    rec({ q: 'Q4C', site: 'healthCheck controls', value: name, outcome: result.outcome, healthy: r?.healthy, error: norm(r?.error) });
  }
  const F2: Record<string, (mk: () => unknown) => () => Promise<any>> = {
    'T1 fetch rejects': (mk) => async () => { throw mk(); },
    'T2 response.ok getter throws': (mk) => async () => ({ get ok(): boolean { throw mk(); }, status: 200 }),
  };
  for (const [t, F] of Object.entries(F2)) {
    for (const [vname, mk] of VALUES) {
      let orig: unknown; const mk2 = () => (orig = mk());
      vi.stubGlobal('fetch', F(mk2));
      const { result, lines } = await cell(() => new ServiceClient({ baseUrl: 'http://svc.invalid', serviceName: 'g177', retries: 0 }).healthCheck());
      vi.unstubAllGlobals();
      const r: any = (result as any).r;
      rec({ q: 'Q4a', site: 'healthCheck ' + t, value: vname, outcome: result.outcome, healthy: r?.healthy, errorType: r ? typeof r.error : undefined,
        error: r ? norm(r.error) : undefined, rejectKind: result.outcome === 'REJECTED' ? kind((result as any).e, orig) : undefined,
        answerSentinel: sentIn(r), logSentinel: hits(lines) });
    }
  }
});
