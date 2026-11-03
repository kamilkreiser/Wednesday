// Gate 176 recorder, Q3 + Q4: the REAL security/secrets-manager.ts (real VaultClient, real package logger; the global
// fetch is a stand-in rejecting with the value) and the REAL blockchain/event-indexer.ts (Blockfrost API a stand-in
// object; '@blockfrost/blockfrost-js' aliased to harness/blockfrost_stub.ts for the start() path).
import { describe, it, vi } from 'vitest';
import fs from 'node:fs';
import { VALUES, capture, kind, hits, SENT } from './values';

const OUT = process.env.GATE176_OUT as string;
const TAG = process.env.GATE176_TAG as string;
const rec = (o: Record<string, unknown>) => fs.appendFileSync(OUT, JSON.stringify({ tag: TAG, ...o }) + '\n');

describe('gate176 Q3 secrets-manager', () => {
  it('Q3 getSecret / getSecretOrThrow per class, useEnvironment on and off', async () => {
    const { SecretsManager } = await import('../security/secrets-manager');
    for (const [name, make] of VALUES) {
      for (const useEnv of [true, false]) {
        for (const verb of ['getSecret', 'getSecretOrThrow'] as const) {
          process.env.GATE176_VAULT_SECRET = 'gate176-env-value';
          const v = make();
          vi.stubGlobal('fetch', () => Promise.reject(v));
          const sm = new SecretsManager({
            vault: { address: 'http://vault.gate176.invalid', token: 't', engine: 'secret', basePath: 'p' },
            useEnvironment: useEnv,
          });
          const { result, lines } = await capture(async () => {
            try {
              const r = await (sm as any)[verb]('gate176.vault.secret');
              return { out: r === 'gate176-env-value' ? 'returned ENV value' : r === null ? 'returned null' : 'returned other' };
            } catch (e) {
              return { out: 'REJECTED ' + kind(e, v) };
            }
          });
          vi.unstubAllGlobals();
          const cached = (sm as any).cache.has('gate176.vault.secret');
          rec({ q: 'Q3', site: `${verb} useEnvironment=${useEnv}`, value: name, ...result, cached, sentinelLines: hits(lines) });
        }
      }
    }
    delete process.env.GATE176_VAULT_SECRET;
  });
});

const P1 = 'a'.repeat(56);
const P2 = 'b'.repeat(56);

type Api = Record<string, (...a: any[]) => Promise<any>>;
function mkApi(site: string, v: () => unknown, counts: Record<string, number>): Api {
  const c = (k: string) => (counts[k] = (counts[k] ?? 0) + 1);
  return {
    blocksLatest: async () => {
      c('blocksLatest');
      if (site === 'S133 start blocksLatest' || site === 'S210 poll blocksLatest') throw v();
      return { height: 11 };
    },
    blocksByNumber: async (hgt: number) => {
      c('blocksByNumber');
      if (site === 'S232 processBlock blocksByNumber') throw v();
      return { tx_count: 2, height: hgt };
    },
    blocksByNumberTxs: async () => (c('blocksByNumberTxs'), ['tx1', 'tx2']),
    txsUtxos: async (tx: string) => {
      c('txsUtxos:' + tx);
      if (site === 'S329 processTransaction txsUtxos' && tx === 'tx1') throw v();
      return { inputs: [], outputs: [{ address: 'addr', amount: [{ unit: 'lovelace', quantity: '1' }, { unit: P1 + '00', quantity: '1' }, { unit: P2 + '00', quantity: '1' }] }] };
    },
    txs: async () => ({ block: 'b', block_height: 11, slot: 1, block_time: 1 }),
    txsMetadata: async () => [],
  };
}

describe('gate176 Q4 event-indexer', () => {
  it('Q4 five catch sites x onError set/unset x 3 polls', async () => {
    const { ContractEventIndexer } = await import('../blockchain/event-indexer');
    const SITES = ['S133 start blocksLatest', 'S210 poll blocksLatest', 'S232 processBlock blocksByNumber', 'S321 onTransaction callback', 'S329 processTransaction txsUtxos'];
    for (const site of SITES) {
      for (const withOnError of [true, false]) {
        for (const [name, make] of VALUES) {
          const counts: Record<string, number> = {};
          const onErr: string[] = [];
          const delivered: string[] = [];
          const unhandled: unknown[] = [];
          const onUnhandled = (r: unknown) => unhandled.push(r);
          process.on('unhandledRejection', onUnhandled);
          const opts: any = {
            blockfrostApiKey: 'gate176-not-a-key',
            policyIds: [P1, P2],
            pollingIntervalMs: 3_600_000,
            onTransaction: async (tx: any) => {
              delivered.push(`${tx.txHash}/${tx.policyId.slice(0, 1)}`);
              if (site === 'S321 onTransaction callback') throw make();
            },
          };
          if (withOnError)
            opts.onError = (e: Error) => {
              let m = '';
              try {
                m = String(e.message);
              } catch {
                m = '<onError could not read message>';
              }
              onErr.push(m.includes(SENT) ? 'SENTINEL' : m.includes('unreadable thrown value') ? 'constant' : 'other:' + m.slice(0, 40));
            };
          const idx = new ContractEventIndexer(opts);
          const g = globalThis as any;
          g.__gate176Api = mkApi(site, make, counts);
          const polls: string[] = [];
          const { lines } = await capture(async () => {
            if (site === 'S133 start blocksLatest') {
              try {
                await idx.start();
                polls.push('start resolved');
              } catch (e) {
                polls.push('start REJECTED ' + kind(e, undefined));
              }
            } else {
              (idx as any).api = g.__gate176Api;
              (idx as any).running = true;
              (idx as any).lastProcessedBlock = 10;
              for (let i = 0; i < 3; i++) {
                const before = (idx as any).lastProcessedBlock;
                try {
                  await (idx as any).poll();
                  polls.push(`poll${i} resolved lastBlock ${before}->${(idx as any).lastProcessedBlock}`);
                } catch (e) {
                  polls.push(`poll${i} REJECTED ${kind(e, undefined)} lastBlock ${before}->${(idx as any).lastProcessedBlock}`);
                }
                if ((idx as any).lastProcessedBlock >= 11) break; // advanced past 11: the block is considered done (skipped if it failed)
              }
            }
            await new Promise((r) => setTimeout(r, 5));
          });
          idx.stop();
          process.off('unhandledRejection', onUnhandled);
          const st = idx.getStatus();
          rec({
            q: 'Q4', site: `${site} onError=${withOnError}`, value: name,
            polls: polls.join(' | ').replace(/SNTL176/g, 'S'),
            pollsRun: polls.length,
            lastBlock: st.lastBlock,
            block11Advanced: st.lastBlock >= 11,
            running: st.running,
            onErrorCalls: onErr.length, onErrorKinds: onErr.join(','),
            delivered: delivered.join(','),
            blocksByNumberCalls: counts.blocksByNumber ?? 0,
            tx2Read: counts['txsUtxos:tx2'] ?? 0,
            unhandled: unhandled.length,
            sentinelLines: hits(lines),
          });
        }
      }
    }
  });
});
