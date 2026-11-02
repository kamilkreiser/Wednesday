// QA gate 133 probe (NOT part of PR 1951). Real nft.routes router, real minting service, real ipfs.service
// providers, real blockchain-verifier, REAL winston logger (utils/logger). Stubbed only: '../db' (a recording table),
// '@blockfrost/blockfrost-js' (a plain class), global fetch (IPFS provider + originate), '../cardano' (never reached).
import { describe, it, vi, afterAll } from 'vitest';
import express from 'express';
import type { Server } from 'http';
import type { AddressInfo } from 'net';
import fs from 'fs';

const realFetch = globalThis.fetch;
const OUT = process.env.PROBE_OUT as string;
const VERSION = process.env.PROBE_VERSION as string;

const st = vi.hoisted(() => ({
  initThrows: false, lookupThrows: false, toThrow: undefined as unknown,
  ipfsThrows: false, rows: [] as Record<string, unknown>[], pinataCalls: 0,
}));

vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: async (text: string, params: unknown[] = []) => {
    const sql = text.replace(/\s+/g, ' ').trim();
    if (sql.startsWith('INSERT INTO svc_nft_certificates')) {
      const [id, , , , , , , , tx, , , , status, ipfs, , , , , errm, , , minted] = params;
      const i = st.rows.findIndex(r => r.id === id);
      const row = { id, status, transaction_hash: tx, ipfs_cid: ipfs, error_message: errm, minted_at: minted ? 'set' : null };
      if (i >= 0) st.rows[i] = row; else st.rows.push(row);
      return { rows: [] };
    }
    return { rows: [] };
  },
}));
vi.mock('../cardano', () => ({
  isCardanoNFTReady: () => false, mintNFTOnChain: vi.fn(), getPolicyId: () => null, waitForNFTConfirmation: vi.fn(),
}));
vi.mock('@blockfrost/blockfrost-js', () => ({
  BlockFrostAPI: class {
    constructor() { if (st.initThrows) throw st.toThrow; }
    txs() { if (st.lookupThrows) return Promise.reject(st.toThrow); return Promise.resolve({ block: 'b', slot: 1, fees: '1' }); }
    assetsById() { return Promise.resolve({ quantity: '1' }); }
  },
}));

const revoked = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const withMessage = (fn: () => unknown) => Object.create(Error.prototype, { message: { get: fn } });
const KINDS: Record<string, () => unknown> = {
  ordinaryError: () => new Error('upstream boom'),
  thrownString: () => 'plain string thrown',
  revokedProxy: () => revoked(),
  throwingGetter: () => withMessage(() => { throw new Error('getter boom'); }),
  getterRevokedProxy: () => withMessage(() => revoked()),
  getterToStringThrows: () => withMessage(() => ({ toString() { throw new Error('ts boom'); } })),
  getterNullProto: () => withMessage(() => Object.create(null)),
  getterSymbol: () => withMessage(() => Symbol('sym-desc')),
};

const safe = (v: unknown): string => { try { return typeof v === 'string' ? v : `<${typeof v}>`; } catch { return '<unreadable>'; } };
const TX = 'a'.repeat(64);

type Cell = { site: string; env: string; kind: string; provider?: string };

async function run(c: Cell): Promise<Record<string, unknown>> {
  vi.resetModules();
  st.rows = []; st.pinataCalls = 0;
  st.initThrows = c.site.endsWith('/init'); st.lookupThrows = c.site.endsWith('/lookup');
  st.ipfsThrows = c.site.startsWith('ipfs') || c.site.startsWith('mint');
  st.toThrow = KINDS[c.kind]();
  process.env.NODE_ENV = c.env;
  process.env.LOG_LEVEL = 'debug';
  process.env.BLOCKFROST_API_KEY = 'gate133-not-a-real-key';
  process.env.IPFS_PROVIDER = c.provider ?? 'pinata';
  process.env.PINATA_API_KEY = 'gate133-k'; process.env.PINATA_SECRET_KEY = 'gate133-s';
  process.env.INFURA_PROJECT_ID = 'gate133-i'; process.env.INFURA_PROJECT_SECRET = 'gate133-is';
  process.env.WEB3_STORAGE_TOKEN = 'gate133-w';
  vi.stubGlobal('fetch', async (url: unknown) => {
    const u = String(url);
    if (u.includes('/api/certifications/')) {
      return new Response(JSON.stringify({ data: { id: 'cert-1', documentHash: 'sha256:00', documentType: 'Certificate', documentTitle: 'T', issuer: { name: 'I', did: 'did:x' }, recipient: { name: 'R' }, issuedDate: '2026-01-01', verificationUrl: 'https://v' } }), { status: 200, headers: { 'content-type': 'application/json' } });
    }
    st.pinataCalls++;
    if (st.ipfsThrows) throw st.toThrow;
    return new Response('{}', { status: 500 });
  });

  const routes = (await import('../routes/nft.routes')).default;
  const { logger } = await import('../utils/logger');
  const { errorHandler } = await import('@secuura/shared');
  const logs: Array<Record<string, unknown>> = [];
  for (const level of ['error', 'warn', 'info'] as const) {
    const orig = (logger as any)[level].bind(logger);
    (logger as any)[level] = (msg: unknown, meta?: Record<string, unknown>) => {
      const rec: Record<string, unknown> = { level, msg: safe(msg) };
      if (meta && typeof meta === 'object') { rec.keys = Object.keys(meta); rec.errorField = safe((meta as any).error); }
      try { const r = orig(msg, meta); rec.threw = false; logs.push(rec); return r; }
      catch (e) { rec.threw = true; rec.thrownName = safe((e as Error)?.name); rec.thrownMsg = safe((e as Error)?.message); logs.push(rec); throw e; }
    };
  }
  const uncaught: string[] = [];
  const onU = (e: unknown) => { uncaught.push(safe((e as Error)?.message)); };
  process.on('uncaughtException', onU); process.on('unhandledRejection', onU);
  const out: Record<string, unknown> = { version: VERSION, ...c };
  try {
    if (c.site.startsWith('mintNFT-direct')) {
      const { nftMintingService } = await import('../services/minting.service');
      try {
        const r = await nftMintingService.mintNFT({
          certificationId: '11111111-1111-4111-8111-111111111111', walletAddress: 'addr_test1_gate133_wallet', chain: 'cardano',
          storageTier: 'premium' as any, privacyLevel: 'full_privacy' as any, documentData: Buffer.from('doc'),
          documentMimeType: 'application/pdf', walletSignature: 'gate133-sig',
        } as any);
        const { mintFailureHttpStatus } = await import('../utils/mintError');
        out.result = { success: r.success, error: safe(r.error), errorCode: r.errorCode, routeWouldAnswer: r.success ? 201 : mintFailureHttpStatus(r.errorCode) };
      } catch (e) { out.result = { rejected: true, name: safe((e as Error)?.name) }; }
    } else {
      const app = express();
      app.use(express.json({ limit: '50mb' }));
      app.use((req: any, _res, next) => { req.user = { userId: 'user-A', role: 'ISSUER', tenantId: 't1', email: 'a@x.test', verificationLevel: 'basic' }; next(); });
      app.use('/api/nft', routes);
      app.use(errorHandler as any);
      const server: Server = await new Promise(r => { const s = app.listen(0, '127.0.0.1', () => r(s)); });
      const base = `http://127.0.0.1:${(server.address() as AddressInfo).port}`;
      let path = ''; let body: unknown = {};
      if (c.site.startsWith('record')) { path = '/api/nft/record'; body = { certificationId: 'cert-1', txHash: TX, policyId: 'p', assetName: 'n', assetId: 'pn', walletAddress: 'addr_test1_gate133_wallet' }; }
      if (c.site.startsWith('verifyTx')) { path = '/api/nft/verify/transaction'; body = { txHash: TX }; }
      if (c.site.startsWith('verifyAsset')) { path = '/api/nft/verify/asset'; body = { policyId: 'p', assetNameHex: '00' }; }
      if (c.site.startsWith('ipfsUpload')) { path = '/api/nft/ipfs/upload'; body = { data: Buffer.from('x').toString('base64'), filename: 'f', originalMimeType: 'application/pdf' }; }
      if (c.site.startsWith('mintRoute')) { path = '/api/nft/mint'; body = { certificationId: '11111111-1111-4111-8111-111111111111', walletAddress: 'addr_test1_gate133_wallet', chain: 'cardano', storageTier: 'premium', privacyLevel: 'full_privacy' }; }
      const resp = await realFetch(base + path, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify(body) });
      out.status = resp.status;
      out.body = await resp.text();
      await new Promise(r => setTimeout(r, 30));
      await new Promise<void>(r => server.close(() => r()));
    }
  } finally {
    process.off('uncaughtException', onU); process.off('unhandledRejection', onU);
    vi.unstubAllGlobals();
  }
  out.rows = st.rows; out.ipfsFetchCalls = st.pinataCalls; out.logs = logs.filter(l => l.msg !== 'Using Pinata provider' && !String(l.msg).startsWith('Using ')); out.uncaught = uncaught;
  return out;
}

const SITES = ['record/init', 'record/lookup', 'verifyTx/init', 'verifyTx/lookup', 'verifyAsset/init', 'ipfsUpload', 'mintNFT-direct', 'mintRoute'];
const CELLS: Cell[] = [];
for (const env of ['production', 'development'])
  for (const site of SITES)
    for (const kind of Object.keys(KINDS)) {
      if (site === 'ipfsUpload') for (const provider of ['pinata', 'infura', 'web3storage']) CELLS.push({ site, env, kind, provider });
      else CELLS.push({ site, env, kind });
    }

describe(`gate133 probe ${VERSION}`, () => {
  for (const c of CELLS) {
    it(`${c.env} ${c.site}${c.provider ? '/' + c.provider : ''} ${c.kind}`, async () => {
      const r = await run(c);
      fs.appendFileSync(OUT, JSON.stringify(r) + '\n');
    }, 20000);
  }
  afterAll(() => { fs.appendFileSync(OUT, JSON.stringify({ done: true, cells: CELLS.length }) + '\n'); });
});
