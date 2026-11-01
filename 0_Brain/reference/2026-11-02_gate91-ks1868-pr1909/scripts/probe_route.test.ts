// gate 91 probe: the REAL router (routes/nft.routes.ts) + REAL minting.service + REAL mintError, on a loopback listener.
// Only replaced: ../db (recording), ../cardano (recording), logger (recording), global fetch for the originate URL only.
import { describe, it, expect, vi, beforeEach, afterAll, beforeAll } from 'vitest';
import * as fs from 'fs';
const h = vi.hoisted(() => ({
  toThrow: undefined as unknown, mode: 'ok' as string,
  sql: [] as string[], chain: [] as string[], logs: [] as any[],
}));
vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: (sql: string) => {
    h.sql.push(String(sql).trim().split(/\s+/).slice(0, 4).join(' '));
    if (/FROM svc_nft_certificates WHERE wallet_address/.test(sql) && h.mode === 'walletThrow') return Promise.reject(h.toThrow);
    return Promise.resolve({ rows: [] });
  },
}));
vi.mock('../cardano', () => ({
  isCardanoNFTReady: () => { h.chain.push('isReady'); return false; },
  mintNFTOnChain: () => { h.chain.push('mintNFTOnChain'); return Promise.resolve({}); },
  getPolicyId: () => { h.chain.push('getPolicyId'); return null; },
  waitForNFTConfirmation: () => { h.chain.push('wait'); return Promise.resolve({}); },
}));
vi.mock('../utils/logger', () => {
  const rec = (lvl: string) => (m: string, meta?: any) => { h.logs.push({ lvl, m, meta }); };
  return { logger: { info: rec('info'), warn: rec('warn'), error: rec('error'), debug: rec('debug') } };
});
import express from 'express';
import type { AddressInfo } from 'net';
import { createServer, Server } from 'http';
import router from '../routes/nft.routes';
import { nftMintingService } from '../services/minting.service';

const realFetch = globalThis.fetch;
let server: Server; let base = '';
const CERT = '11111111-1111-4111-8111-111111111111';
const out: any[] = [];

function mk(kind: string): unknown {
  if (kind === 'ordinary') return new Error('originate down');
  if (kind === 'proxy') { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; }
  return Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } });
}

beforeAll(async () => {
  const app = express(); app.use(express.json());
  app.use((req, _res, next) => { (req as any).user = { userId: 'caller1' }; next(); });
  app.use('/api/nft', router);
  server = createServer(app); await new Promise<void>((r) => server.listen(0, '127.0.0.1', () => r()));
  base = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => { server.close(); fs.writeFileSync(process.env.PROBE_OUT as string, JSON.stringify(out, null, 1)); });
beforeEach(() => { h.sql = []; h.chain = []; h.logs = []; h.mode = 'ok'; });

describe('POST /api/nft/mint, production fetch rejection', () => {
  for (const kind of ['ordinary', 'proxy', 'getter', 'nonok']) {
    it('mint ' + kind, async () => {
      const saved = process.env.NODE_ENV; process.env.NODE_ENV = 'production';
      const thrown = kind === 'nonok' ? null : mk(kind);
      vi.stubGlobal('fetch', (u: any, i: any) => String(u).includes('/api/certifications/')
        ? (kind === 'nonok' ? Promise.resolve({ ok: false, status: 404 }) : Promise.reject(thrown)) : realFetch(u, i));
      const unhandled: any[] = []; const uh = (e: any) => unhandled.push(String(e)); process.on('unhandledRejection', uh);
      try {
        const certId = CERT.slice(0, -2) + String(out.length).padStart(2, '0');
        const r = await realFetch(base + '/api/nft/mint', { method: 'POST', headers: { 'content-type': 'application/json' },
          body: JSON.stringify({ certificationId: certId, walletAddress: 'addr_test1gate91wallet', chain: 'cardano', storageTier: 'basic', privacyLevel: 'full_privacy' }) });
        const txt = await r.text();
        await new Promise((x) => setTimeout(x, 20));
        out.push({ cell: 'mint/' + kind, status: r.status, body: txt, sql: h.sql, chain: h.chain,
          logs: h.logs.filter((l) => l.lvl === 'error' || l.lvl === 'warn').map((l) => ({ lvl: l.lvl, m: l.m, meta: l.meta })), unhandled });
      } finally { process.off('unhandledRejection', uh); process.env.NODE_ENV = saved; vi.unstubAllGlobals(); }
    });
  }
});

describe('GET /api/nft/certificates?walletAddress=', () => {
  for (const kind of ['ordinary', 'proxy', 'getter']) {
    it('wallet ' + kind, async () => {
      const rec = await nftMintingService.recordClientMint({ certificationId: 'seed-' + kind, txHash: 'a'.repeat(64), policyId: 'p', assetName: 'n', assetId: 'p.n',
        walletAddress: 'addr_test1w_' + kind, onChainVerified: true, onChainStatus: 'ok' });
      rec.userId = 'caller1'; // the KS-1836 gate only shows the caller's own rows
      h.sql = []; h.logs = []; h.mode = 'walletThrow'; h.toThrow = mk(kind);
      const unhandled: any[] = []; const uh = (e: any) => unhandled.push(String(e)); process.on('unhandledRejection', uh);
      try {
        const r = await realFetch(base + '/api/nft/certificates?walletAddress=addr_test1w_' + kind);
        const txt = await r.text();
        out.push({ cell: 'wallet/' + kind, status: r.status, body: txt.length > 400 ? JSON.parse(txt).data?.count + ' certs; ' + txt.slice(0, 120) : txt, sql: h.sql,
          logs: h.logs.filter((l) => l.lvl === 'error' || l.lvl === 'warn').map((l) => ({ lvl: l.lvl, m: l.m, meta: l.meta })), unhandled });
      } finally { process.off('unhandledRejection', uh); }
    });
  }
});
