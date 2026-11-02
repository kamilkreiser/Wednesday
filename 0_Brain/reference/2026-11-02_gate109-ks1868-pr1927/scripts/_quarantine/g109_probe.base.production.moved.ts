// GATE 109 probe: real BlockchainVerifierService + real nft.routes router on a real http server + real
// NFTMintingService.recordClientMint + REAL winston logger (wrapped call-through). Replaced: the Blockfrost
// client (counting stand-in) and the db module's query/isDbAvailable (stateful upsert recorder).
import { describe, it, vi } from 'vitest';
import http from 'http';
import express from 'express';
import fs from 'fs';

const S = vi.hoisted(() => ({
  rows: new Map<string, any>(),
  ops: [] as string[],
  mode: 'none' as string, // none | init | lookup
  toThrow: undefined as unknown,
  chain: { init: 0, txs: 0, txsResolved: 0 },
}));

vi.mock('../db', async (orig) => {
  const real: any = await orig();
  return {
    ...real,
    isDbAvailable: () => true,
    query: async (text: string, p: unknown[] = []) => {
      if (/INSERT INTO svc_nft_certificates/i.test(text)) {
        const id = p[0] as string;
        const prev = S.rows.get(id);
        S.rows.set(id, { ...(prev || {}), id, certification_id: p[1], transaction_hash: p[8], status: p[12], error_message: p[18], minted_at: p[21] ?? null });
        S.ops.push((prev ? 'update ' : 'insert ') + id);
      } else {
        S.ops.push('other ' + String(text).trim().slice(0, 30));
      }
      return { rows: [], rowCount: 0 };
    },
  };
});

vi.mock('@blockfrost/blockfrost-js', () => ({
  BlockFrostAPI: class {
    constructor() {
      S.chain.init++;
      if (S.mode === 'init') throw S.toThrow;
    }
    txs() {
      S.chain.txs++;
      if (S.mode === 'lookup') return Promise.reject(S.toThrow);
      S.chain.txsResolved++;
      return Promise.resolve({ block: 'blk', slot: 7, fees: '170000' });
    }
  },
}));

const rev = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const withMsg = (get: () => unknown) => Object.create(Error.prototype, { message: { get } });
const VALUES: Record<string, () => unknown> = {
  ord: () => new Error('upstream 500'),
  str: () => 'plain string',
  revoked: rev,
  getterThrows: () => withMsg(() => { throw new Error('getter boom'); }),
  msgRevoked: () => withMsg(() => rev()),
  msgToStrThrows: () => withMsg(() => ({ toString() { throw new Error('ts boom'); } })),
  msgSymbol: () => withMsg(() => Symbol('sym')),
  msgNullProto: () => withMsg(() => Object.create(null)),
  nullProto: () => Object.create(null),
  plainMsgGetter: () => ({ get message() { throw new Error('plain getter boom'); } }),
  s404: () => Object.assign(new Error('not found'), { status_code: 404 }),
};
const SCEN: [string, string, string][] = [['none', 'none', 'none'], ['unconfigured', 'unconfigured', 'none']];
for (const site of ['init', 'lookup']) for (const v of Object.keys(VALUES)) {
  if (v === 's404' && site === 'init') continue;
  SCEN.push([site + ':' + v, site, v]);
}

const safe = (x: unknown): string => {
  try {
    if (typeof x === 'string') return x;
    if (typeof x === 'symbol') return 'symbol';
    return x === null ? 'null' : typeof x + ':' + Object.prototype.toString.call(x);
  } catch { return 'unreadable'; }
};
const errName = (e: unknown) => { try { return (e as Error).constructor.name + ':' + String((e as Error).message).slice(0, 60); } catch { return 'unreadable'; } };

describe('g109 probe', () => {
  for (const [name, site, v] of SCEN) {
    it('scenario ' + name, async () => {
      const { blockchainVerifier } = await import('../services/blockchain-verifier.service');
      const { logger } = await import('../utils/logger');
      const { default: router } = await import('../routes/nft.routes');
      const logs: string[] = [];
      const logThrows: string[] = [];
      for (const lvl of ['warn', 'error', 'info'] as const) {
        const orig = (logger as any)['__g109_' + lvl] || (logger as any)[lvl].bind(logger);
        (logger as any)['__g109_' + lvl] = orig;
        (logger as any)[lvl] = (msg: unknown, meta?: Record<string, unknown>) => {
          let keys = '';
          try { keys = meta ? Object.keys(meta).map(k => k + '=' + safe((meta as any)[k])).join(',') : ''; } catch { keys = 'unreadable-meta'; }
          logs.push(lvl + ':' + String(msg).slice(0, 50) + '{' + keys + '}');
          try { return orig(msg, meta); } catch (e) { logThrows.push(lvl + ':' + errName(e)); throw e; }
        };
      }
      const rec: any = { scenario: name, label: process.env.G109_LABEL, nodeEnv: process.env.NODE_ENV };
      const app = express(); app.use(express.json()); app.use('/api/nft', router);
      const srv = http.createServer(app); await new Promise<void>(r => srv.listen(0, '127.0.0.1', r));
      const port = (srv.address() as any).port;
      const txHash = 'ab'.repeat(32);
      const reset = () => {
        (blockchainVerifier as any).api = null;
        S.mode = site === 'unconfigured' ? 'none' : site;
        S.toThrow = v === 'none' ? undefined : VALUES[v]();
        S.chain.init = 0; S.chain.txs = 0; S.chain.txsResolved = 0;
        if (site === 'unconfigured') delete process.env.BLOCKFROST_API_KEY; else process.env.BLOCKFROST_API_KEY = 'g109-real-looking-key';
      };
      // (a) direct call
      reset(); logs.length = 0; logThrows.length = 0;
      try {
        const r: any = await blockchainVerifier.verifyTransaction(txHash);
        rec.direct = { resolved: 'error' in r ? { ...r, error: safe(r.error) } : r };
      } catch (e) { rec.direct = { rejected: errName(e) }; }
      rec.directChain = { ...S.chain }; rec.directLogs = [...logs]; rec.directLogThrows = [...logThrows];
      // (b) POST /api/nft/record
      reset(); logs.length = 0; logThrows.length = 0;
      const before = new Set(S.rows.keys()); S.ops.length = 0;
      const r1 = await fetch(`http://127.0.0.1:${port}/api/nft/record`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ certificationId: 'cert-' + name, txHash, policyId: 'pol', assetName: 'asset', assetId: 'polasset', walletAddress: 'addr_test1xxxxxxxxxxxx' }) });
      const b1: any = await r1.json();
      if (b1?.data?.nftCertificateId) b1.data.nftCertificateId = '<uuid>';
      rec.record = { status: r1.status, body: b1 };
      rec.recordRows = [...S.rows.values()].filter(x => !before.has(x.id)).map(x => ({ status: x.status, minted: x.minted_at !== null, txHashIsCallers: x.transaction_hash === txHash, error_message: x.error_message ?? null }));
      rec.recordOps = S.ops.map(o => o.split(' ')[0]);
      rec.recordChain = { ...S.chain };
      rec.recordLogs = [...logs]; rec.recordLogThrows = [...logThrows];
      // (c) POST /api/nft/verify/transaction
      reset(); logs.length = 0; logThrows.length = 0; S.ops.length = 0;
      const r2 = await fetch(`http://127.0.0.1:${port}/api/nft/verify/transaction`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ txHash }) });
      rec.verify = { status: r2.status, body: await r2.json() };
      rec.verifyChain = { ...S.chain }; rec.verifyOps = S.ops.length;
      rec.verifyLogs = [...logs]; rec.verifyLogThrows = [...logThrows];
      srv.close();
      fs.appendFileSync(process.env.G109_OUT as string, JSON.stringify(rec) + '\n');
    }, 30000);
  }
});
