import { describe, it, expect, vi } from 'vitest';
import http from 'http';
import express from 'express';

process.env.IPFS_PROVIDER = process.env.G108_PROVIDER || 'pinata';
process.env.PINATA_API_KEY = 'k'; process.env.PINATA_SECRET_KEY = 's';
process.env.INFURA_PROJECT_ID = 'k'; process.env.INFURA_PROJECT_SECRET = 's';
process.env.WEB3_STORAGE_TOKEN = 't';
process.env.NODE_ENV = 'test';

const logs: unknown[][] = [];
vi.mock('../utils/logger', () => ({
  logger: { info: vi.fn(), warn: vi.fn(), error: (...a: unknown[]) => { logs.push(a); }, debug: vi.fn() },
}));

const realFetch = globalThis.fetch;
let toThrow: unknown; let providerCalls = 0;
const rev = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const getterThrows = () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } });
const getterRetRevoked = () => Object.create(Error.prototype, { message: { get() { return rev(); } } });
const getterRetToStrThrows = () => Object.create(Error.prototype, { message: { get() { return { toString() { throw new Error('ts boom'); } }; } } });
const getterRetSymbol = () => Object.create(Error.prototype, { message: { get() { return Symbol('sym'); } } });
const getterRetNullProto = () => Object.create(Error.prototype, { message: { get() { return Object.create(null); } } });
const VALUES: Record<string, () => unknown> = {
  ord: () => new Error('connect refused'),
  str: () => 'plain string',
  revoked: rev,
  getterThrows,
  msgRevoked: getterRetRevoked,
  msgToStrThrows: getterRetToStrThrows,
  msgSymbol: getterRetSymbol,
  msgNullProto: getterRetNullProto,
};
const out: Record<string, unknown> = {};

describe('g108 probe', () => {
  for (const [name, mk] of Object.entries(VALUES)) {
    it('value ' + name, async () => {
      globalThis.fetch = ((url: any, init: any) => {
        if (typeof url === 'string' && url.startsWith('http://127.0.0.1')) return realFetch(url, init);
        providerCalls++; return Promise.reject(toThrow);
      }) as typeof fetch;
      toThrow = mk(); providerCalls = 0; logs.length = 0;
      const { IPFSService } = await import('../services/ipfs.service');
      const prov = process.env.IPFS_PROVIDER as any;
      const svc = new IPFSService(prov, { apiKey: 'k', secretKey: 's' });
      const rec: any = { value: name };
      // (a) direct upload()
      try { rec.upload = await svc.upload({ data: Buffer.from('x'), filename: 'f', mimeType: 'a/b', encrypted: false }); }
      catch (e) { let m = '?'; try { m = (e as Error).constructor.name + ':' + (e as Error).message; } catch { m = 'unreadable'; } rec.upload = { rejected: m }; }
      rec.upCalls = providerCalls; providerCalls = 0;
      // (b) real /ipfs/upload route
      const { default: router } = await import('../routes/nft.routes');
      const app = express(); app.use(express.json()); app.use('/api/nft', router);
      const srv = http.createServer(app); await new Promise<void>(r => srv.listen(0, '127.0.0.1', r));
      const port = (srv.address() as any).port;
      const resp = await realFetch(`http://127.0.0.1:${port}/api/nft/ipfs/upload`, { method: 'POST', headers: { 'content-type': 'application/json' }, body: JSON.stringify({ data: Buffer.from('x').toString('base64'), filename: 'f', originalMimeType: 'a/b' }) });
      rec.route = { status: resp.status, body: await resp.json() };
      rec.routeCalls = providerCalls; providerCalls = 0;
      // (c) real mintNFT, PREMIUM
      const { nftMintingService } = await import('../services/minting.service');
      const { StorageTier, PrivacyLevel } = await import('../types');
      const mint: any = await nftMintingService.mintNFT({ certificationId: '11111111-1111-4111-8111-111111111111', walletAddress: 'addr_test1xxxxxxxxxxxx', chain: 'cardano', storageTier: StorageTier.PREMIUM, privacyLevel: PrivacyLevel.PARTIAL, documentData: Buffer.from('doc'), documentMimeType: 'application/pdf', walletSignature: 'sig' } as any);
      const { mintFailureHttpStatus } = await import('../utils/mintError');
      rec.mint = { success: mint.success, error: mint.error, errorCode: mint.errorCode, status: mintFailureHttpStatus(mint.errorCode) };
      rec.mintCalls = providerCalls;
      const recs = (await nftMintingService.getUserNFTCertificates('user-id')) as any[];
      const last = recs[recs.length - 1];
      rec.persisted = last ? { status: last.status, errorMessage: last.errorMessage } : null;
      rec.routeLogs = JSON.stringify(logs.map(l => l.map(x => typeof x === 'string' ? x : JSON.stringify(x)))).slice(0, 200);
      srv.close();
      out[name] = rec;
      require('fs').appendFileSync(process.env.G108_OUT as string, JSON.stringify(rec) + '\n');
    }, 30000);
  }
});
