// gate133: a message getter that is readable on the first N reads and a revoked Proxy afterwards (non-idempotent).
// Real winston logger; Blockfrost stubbed. Not part of PR 1951.
import { it, vi, expect } from 'vitest';
import fs from 'fs';
const st = vi.hoisted(() => ({ toThrow: undefined as unknown }));
vi.mock('@blockfrost/blockfrost-js', () => ({ BlockFrostAPI: class { txs() { return Promise.reject(st.toThrow); } } }));
const revoked = () => { const { proxy, revoke } = Proxy.revocable({}, {}); revoke(); return proxy; };
for (const n of [0, 1, 2, 3]) {
  it(`flip after ${n} reads`, async () => {
    process.env.BLOCKFROST_API_KEY = 'gate133-k'; process.env.NODE_ENV = 'production';
    vi.resetModules();
    const { BlockchainVerifierService } = await import('../services/blockchain-verifier.service');
    let reads = 0;
    st.toThrow = Object.create(Error.prototype, { message: { get() { reads++; return reads <= n ? 'readable text' : revoked(); } } });
    let out: string;
    try { const r = await new BlockchainVerifierService().verifyTransaction('h'); out = `resolved status=${r.status} errorType=${typeof r.error}`; }
    catch (e) { out = `REJECTED ${(e as Error).message}`; }
    fs.appendFileSync(process.env.PROBE_OUT as string, JSON.stringify({ v: process.env.PROBE_VERSION, n, reads, out }) + '\n');
    expect(true).toBe(true);
  });
}
