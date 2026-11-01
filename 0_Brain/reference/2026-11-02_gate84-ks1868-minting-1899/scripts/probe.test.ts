// QA GATE 84 probe (not part of the PR). Copied into the gate clone's src/__tests__ for the run only, then moved out.
// Measures what the CALLERS see when the DB rejects with an unreadable thrown value, versus an ordinary Error.
import { describe, it, vi } from 'vitest';
import { appendFileSync } from 'fs';

const OUT = process.env.PROBE_OUT as string;
const h = vi.hoisted(() => ({
  mode: 'none' as string,
  toThrow: undefined as unknown,
  saved: [] as string[],
  failedSaves: 0,
  errLogs: [] as any[],
}));

vi.mock('../db', () => ({
  isDbAvailable: () => true,
  query: (sql: string, params: any[]) => {
    const isInsert = /INSERT INTO svc_nft_certificates/.test(sql);
    if (isInsert) {
      const status = params[12];
      if (h.mode === 'insertMinted' && status === 'minted') { h.failedSaves++; return Promise.reject(h.toThrow); }
      if (h.mode === 'insertAll') { h.failedSaves++; return Promise.reject(h.toThrow); }
      h.saved.push(status);
      return Promise.resolve({ rows: [] });
    }
    if (h.mode === 'select') return Promise.reject(h.toThrow);
    return Promise.resolve({ rows: [] });
  },
}));
vi.mock('../cardano', () => ({ isCardanoNFTReady: () => false, mintNFTOnChain: vi.fn(), getPolicyId: () => null, waitForNFTConfirmation: vi.fn() }));
vi.mock('../utils/logger', () => ({ logger: { info: vi.fn(), warn: (...a: any[]) => h.errLogs.push(['warn', ...a]), error: (...a: any[]) => h.errLogs.push(['error', ...a]), debug: vi.fn() } }));

import { nftMintingService, loadFromDb } from '../services/minting.service';

const revoked = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
const KINDS: Record<string, () => unknown> = {
  ordinary: () => new Error('db down'),
  revokedProxy: revoked,
  throwingGetter: () => Object.create(Error.prototype, { message: { get() { throw new Error('getter boom'); } } }),
};
const rec = (o: any) => appendFileSync(OUT, JSON.stringify(o) + '\n');
const safe = (v: unknown) => { try { return v instanceof Error ? 'Error:' + v.message : typeof v; } catch { return 'unreadable'; } };
const reset = (mode: string, kind: string) => { h.mode = mode; h.toThrow = KINDS[kind](); h.saved = []; h.failedSaves = 0; h.errLogs = []; };
const logs = () => h.errLogs.map((l) => { try { return l[0] + ':' + l[1] + ':' + JSON.stringify(l[2]); } catch { return 'unserialisable'; } });

describe('probe', () => {
  for (const kind of Object.keys(KINDS)) {
    it(`mintNFT post-mint save fails [${kind}]`, async () => {
      reset('insertMinted', kind);
      let outcome: any; let thrown: any = null;
      try { outcome = await nftMintingService.mintNFT({ certificationId: 'c1', chain: 'cardano', walletAddress: 'addr_test1xyz', storageTier: 'standard', privacyLevel: 'partial' } as any); }
      catch (e) { thrown = safe(e); }
      const id = outcome?.nftCertificateId;
      let memStatus: any = 'n/a';
      if (id) { try { memStatus = (await nftMintingService.getNFTCertificate(id))?.status; } catch (e) { memStatus = 'getter threw ' + safe(e); } }
      rec({ probe: 'mintNFT_post_mint_save_fails', kind, outcome: outcome ? { success: outcome.success, errorCode: outcome.errorCode, error: outcome.error, txHash: !!outcome.transactionHash } : null, thrown, memStatus, dbSavedStatuses: h.saved, failedSaves: h.failedSaves, logs: logs() });
    }, 20000);
    it(`recordClientMint save fails [${kind}]`, async () => {
      reset('insertAll', kind);
      let outcome: any; let thrown: any = null;
      try { outcome = await nftMintingService.recordClientMint({ certificationId: 'c2', txHash: 't', policyId: 'p', assetName: 'a', assetId: 'p.a', walletAddress: 'w', onChainVerified: true, onChainStatus: 'ok' }); }
      catch (e) { thrown = safe(e); }
      rec({ probe: 'recordClientMint', kind, resolved: !!outcome, status: outcome?.status, thrown, logs: logs() });
    });
    it(`getNFTCertificate select fails [${kind}]`, async () => {
      reset('select', kind);
      let outcome: any = 'unset'; let thrown: any = null;
      try { outcome = await nftMintingService.getNFTCertificate('missing-id-' + kind); } catch (e) { thrown = safe(e); }
      rec({ probe: 'getNFTCertificate', kind, outcome: outcome === null ? 'null' : outcome, thrown, logs: logs() });
    });
    it(`getUserNFTCertificates select fails [${kind}]`, async () => {
      reset('select', kind);
      let outcome: any = 'unset'; let thrown: any = null;
      try { outcome = await nftMintingService.getUserNFTCertificates('user-id'); } catch (e) { thrown = safe(e); }
      rec({ probe: 'getUserNFTCertificates', kind, outcomeLen: Array.isArray(outcome) ? outcome.length : outcome, thrown, logs: logs() });
    });
    it(`loadFromDb select fails [${kind}]`, async () => {
      reset('select', kind);
      let thrown: any = null; let resolved = false;
      try { await loadFromDb(); resolved = true; } catch (e) { thrown = safe(e); }
      rec({ probe: 'loadFromDb', kind, resolved, thrown, logs: logs() });
    });
  }
});
