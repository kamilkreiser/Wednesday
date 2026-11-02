/**
 * =============================================================================
 * CARDANO BLOCKFROST PROVIDER
 * =============================================================================
 * Initialises and configures the Blockfrost provider for Cardano chain
 * interaction. Provides helper methods for UTxO queries, tx submission,
 * and protocol parameter retrieval.
 * =============================================================================
 */

import { BlockFrostAPI } from '@blockfrost/blockfrost-js';
import { logger } from '../utils/logger';

let blockfrost: BlockFrostAPI | null = null;

/**
 * ---------------------------------------------------------------------------
 * KS-671: passive chain-reachability record
 * ---------------------------------------------------------------------------
 * `/health` used to assert "connected (Blockfrost)" from isCardanoReady(),
 * which only tests that the key and mnemonic are SET. A key that is present,
 * valid and OVER QUOTA satisfies it — which is how demo reported `healthy`
 * for six days while every chain call returned 402 (KS-670).
 *
 * This records the outcome of the calls the service ALREADY makes. It never
 * issues a request of its own: a health check that polled Blockfrost every
 * 15s would add ~5,760 calls/day against the same 50,000 free-tier allowance
 * whose exhaustion caused KS-670 — a probe that consumes the budget it
 * monitors.
 *
 * ---------------------------------------------------------------------------
 * WHY THE CLIENT IS INSTRUMENTED AND NOT THE CALL SITES (#728 review)
 * ---------------------------------------------------------------------------
 * The first version of this recorded at four hand-picked call sites inside
 * this file, on the ticket's premise that "every anchoring chain call already
 * funnels through provider.ts". THAT PREMISE IS FALSE, and Peter's review
 * disproved it by replaying KS-670's own timeline: all 56,385 failures came
 * from the verify-by-hash scan, which takes the RAW client through
 * getProvider() and never touched the record. The service would still have
 * reported `connected (Blockfrost)` for six days.
 *
 * Enumerating call sites fails OPEN — a call site nobody listed records
 * nothing, and reads exactly like a healthy chain. So the recorder moved onto
 * the CLIENT ITSELF: initProvider wraps the BlockFrostAPI instance in a Proxy
 * that records every method call through it, whoever makes it. A new chain
 * call added anywhere is instrumented by construction, not by remembering.
 *
 * `this` is bound to the TARGET, not the proxy, so the client's own internal
 * property access does not re-enter the trap and one logical call records once.
 *
 * Route 3 — `cardano/threadTokenMint.ts:256` builds its OWN
 * `Lucid(new Blockfrost(...))` on the same BLOCKFROST_API_KEY and is NOT
 * covered by this proxy. That is stated rather than silently left: it runs
 * only on an explicit mint, and it throws on failure rather than degrading
 * quietly. Declared so the next reader does not re-derive the false premise.
 * ---------------------------------------------------------------------------
 */
export type ChainReachability = 'unknown' | 'ok' | 'failing';

export interface ChainHealth {
  reachability: ChainReachability;
  lastSuccessAt: string | null;
  lastFailureAt: string | null;
  lastFailureStatus: number | null;
  lastFailureMessage: string | null;
  consecutiveFailures: number;
  /** True when `reachability` was downgraded to 'unknown' by the staleness rule. */
  stale: boolean;
}

interface ChainHealthRecord {
  reachability: ChainReachability;
  lastSuccessAt: string | null;
  lastFailureAt: string | null;
  lastFailureStatus: number | null;
  lastFailureMessage: string | null;
  consecutiveFailures: number;
}

const chainHealth: ChainHealthRecord = {
  reachability: 'unknown',
  lastSuccessAt: null,
  lastFailureAt: null,
  lastFailureStatus: null,
  lastFailureMessage: null,
  consecutiveFailures: 0,
};

/**
 * How long a success stands before it stops being evidence about NOW.
 *
 * The bug being fixed is a six-day-old success still reading as `connected`.
 * The record only moves when a call happens, so `ok` is a statement about the
 * last call — whenever that was — while `/health` presents it as a statement
 * about the present. Ageing it costs zero chain calls.
 */
export const CHAIN_HEALTH_STALE_MS = Number.isFinite(Number(process.env.CHAIN_HEALTH_STALE_MS))
  ? Number(process.env.CHAIN_HEALTH_STALE_MS)
  : 15 * 60 * 1000;

/**
 * Consecutive failures before the AGGREGATE `/health.status` reports degraded.
 *
 * `reachability` in the body flips on the FIRST failure and stays honest;
 * only the aggregate waits, because alerting is wired to `status` and one
 * transient blip should not page anyone (#728 review).
 */
export const CHAIN_DEGRADED_AFTER_FAILURES = Number.isFinite(
  Number(process.env.CHAIN_DEGRADED_AFTER_FAILURES),
)
  ? Number(process.env.CHAIN_DEGRADED_AFTER_FAILURES)
  : 3;

/**
 * Did the chain ANSWER, or was it unreachable?
 *
 * The original 404-is-a-success rule was right and this applies it
 * symmetrically (#728 review). A 400 `All inputs are spent` (the KS-535
 * signature), a script failure or `ValueNotConservedUTxO` are the chain
 * telling us our transaction is invalid — that is a reachable chain giving a
 * real answer, and it must not read as an outage that sticks until the next
 * success.
 *
 * Unreachable: 402 (quota — the KS-670 signature), 408, 429, any 5xx, and any
 * error carrying NO status code at all (DNS, TCP, TLS, timeout).
 * Answered:    every other 4xx.
 */
export function isChainReachableError(err: any): boolean {
  const status = typeof err?.status_code === 'number' ? err.status_code : null;
  if (status === null) return false;
  if (status === 402 || status === 408 || status === 429) return false;
  if (status >= 500) return false;
  return status >= 400 && status < 500;
}

function recordChainSuccess(): void {
  chainHealth.reachability = 'ok';
  chainHealth.lastSuccessAt = new Date().toISOString();
  chainHealth.consecutiveFailures = 0;
}

function recordChainFailure(err: any): void {
  chainHealth.reachability = 'failing';
  chainHealth.lastFailureAt = new Date().toISOString();
  chainHealth.lastFailureStatus = typeof err?.status_code === 'number' ? err.status_code : null;
  chainHealth.lastFailureMessage = String(err?.message ?? 'unknown error').slice(0, 200);
  chainHealth.consecutiveFailures += 1;
}

/** Record one chain outcome, classifying the error first. Exported for the proxy and for tests. */
export function recordChainOutcome(err: any | null): void {
  if (err === null) {
    recordChainSuccess();
    return;
  }
  if (isChainReachableError(err)) {
    // The chain answered. Reachability holds; the caller deals with the error.
    recordChainSuccess();
    return;
  }
  recordChainFailure(err);
}

/**
 * Snapshot of chain reachability, derived only from calls already made.
 *
 * ASYMMETRY, DELIBERATE: a stale `ok` ages to `unknown`; a stale `failing`
 * does NOT. Ageing `ok` prevents false reassurance, which is the whole bug.
 * Ageing `failing` would do the opposite — quietly retire an outage nobody
 * fixed and switch the alert off. `failing` clears when a call succeeds, and
 * only then.
 */
export function getChainHealth(now: number = Date.now()): ChainHealth {
  const snapshot: ChainHealth = { ...chainHealth, stale: false };

  if (snapshot.reachability === 'ok' && snapshot.lastSuccessAt) {
    const age = now - Date.parse(snapshot.lastSuccessAt);
    if (Number.isFinite(age) && age > CHAIN_HEALTH_STALE_MS) {
      snapshot.reachability = 'unknown';
      snapshot.stale = true;
    }
  }

  return snapshot;
}

/** Test seam — resets the record. Not used at runtime. */
export function __resetChainHealth(): void {
  chainHealth.reachability = 'unknown';
  chainHealth.lastSuccessAt = null;
  chainHealth.lastFailureAt = null;
  chainHealth.lastFailureStatus = null;
  chainHealth.lastFailureMessage = null;
  chainHealth.consecutiveFailures = 0;
}

/**
 * Wrap a BlockFrostAPI instance so every method call through it records its
 * outcome. See the block comment above for why this is on the client and not
 * on the call sites.
 */
export function instrumentProvider<T extends object>(client: T): T {
  return new Proxy(client, {
    get(target, prop, receiver) {
      const value = Reflect.get(target, prop, receiver);
      if (typeof value !== 'function') return value;

      return function instrumented(this: unknown, ...args: unknown[]) {
        // `this` is the TARGET, never the proxy: the client's own internal
        // property access must not re-enter this trap, or one logical call
        // would record several times.
        let result: unknown;
        try {
          result = (value as (...a: unknown[]) => unknown).apply(target, args);
        } catch (err) {
          recordChainOutcome(err);
          throw err;
        }

        if (result && typeof (result as Promise<unknown>).then === 'function') {
          return (result as Promise<unknown>).then(
            (ok) => {
              recordChainOutcome(null);
              return ok;
            },
            (err) => {
              recordChainOutcome(err);
              throw err;
            },
          );
        }

        // Synchronous, non-promise return — not a chain round trip. Record
        // nothing rather than inventing a success.
        return result;
      };
    },
  });
}

export interface ProtocolParams {
  minFeeA: string;
  minFeeB: string;
  poolDeposit: string;
  keyDeposit: string;
  maxValSize: number;
  maxTxSize: number;
  coinsPerUtxoByte: string;
  priceMem: number;
  priceStep: number;
  collateralPercent: number;
  maxCollateralInputs: number;
  slot: number;
}

/**
 * Initialise the Blockfrost provider.
 * Returns null if no API key is configured.
 */
export function initProvider(apiKey: string, network: string): BlockFrostAPI | null {
  if (!apiKey) return null;

  const networkMap: Record<string, string> = {
    mainnet: 'https://cardano-mainnet.blockfrost.io/api',
    preprod: 'https://cardano-preprod.blockfrost.io/api',
    preview: 'https://cardano-preview.blockfrost.io/api',
  };

  const baseUrl = networkMap[network];
  if (!baseUrl) {
    logger.warn('[Cardano] Unknown network — cannot initialise Blockfrost', { network });
    return null;
  }

  // KS-671 (#728 review): every call through this handle records its own
  // outcome. Instrumenting the CLIENT rather than the call sites is what
  // makes the verify-by-hash scan — which takes this handle raw via
  // getProvider() — impossible to miss.
  blockfrost = instrumentProvider(
    new BlockFrostAPI({
      projectId: apiKey,
      network: network as 'mainnet' | 'preprod' | 'preview',
    }),
  );

  return blockfrost;
}

/**
 * Get the current Blockfrost instance.
 */
export function getProvider(): BlockFrostAPI | null {
  return blockfrost;
}

/**
 * Fetch current protocol parameters from the chain.
 */
export async function fetchProtocolParams(): Promise<ProtocolParams | null> {
  if (!blockfrost) return null;

  try {
    const params = await blockfrost.epochsLatestParameters();
    const tip = await blockfrost.blocksLatest();

    return {
      minFeeA: params.min_fee_a.toString(),
      minFeeB: params.min_fee_b.toString(),
      poolDeposit: params.pool_deposit,
      keyDeposit: params.key_deposit,
      maxValSize: parseInt(params.max_val_size || '5000', 10),
      maxTxSize: params.max_tx_size,
      coinsPerUtxoByte: params.coins_per_utxo_size || '4310',
      priceMem: params.price_mem || 0.0577,
      priceStep: params.price_step || 0.0000721,
      collateralPercent: params.collateral_percent || 150,
      maxCollateralInputs: params.max_collateral_inputs || 3,
      slot: tip.slot || 0,
    };
  } catch (err: any) {
    logger.error('[Cardano] Failed to fetch protocol parameters', { error: err?.message });
    return null;
  }
}

/**
 * Fetch UTxOs for a given address via Blockfrost.
 */
export async function fetchUtxos(address: string) {
  if (!blockfrost) return [];
  try {
    return await blockfrost.addressesUtxos(address);
  } catch (err: any) {
    // 404 = the chain answered: this address has no on-chain history (an
    // unfunded wallet). Reachability is recorded by the client proxy via
    // isChainReachableError; this only decides what the CALLER gets back.
    if (err?.status_code === 404) return [];
    throw err;
  }
}

/**
 * KS-1384 F-b (the shared scan core, walletLabelScan.ts): one page (1-based) of the address's transactions,
 * NEWEST FIRST. Returns [] when the chain answered that the address has no history (404), and null when the
 * read failed: a caller must read null as "unknown", never as "no transactions".
 */
export async function fetchAddressTxPage(
  address: string,
  page: number,
  count: number,
): Promise<Array<{ txHash: string; blockHeight: number; blockTime: number; txIndex: number }> | null> {
  if (!blockfrost) return null;
  try {
    const rows = await blockfrost.addressesTransactions(address, { page, count, order: 'desc' });
    return (rows ?? []).map((r) => ({ txHash: r.tx_hash, blockHeight: r.block_height, blockTime: r.block_time, txIndex: r.tx_index }));
  } catch (err: any) {
    if (err?.status_code === 404) return [];
    logger.warn('[Cardano] Address transactions page read failed', { page, count, error: err?.message });
    return null;
  }
}

/**
 * KS-1384 F0 (design rev 4 INFO 2): every UTxO at the address, all pages. `addressesUtxos` returns one page of
 * 100, so a wallet holding more coins was read short. The batch size is explicit: without it the SDK falls back
 * to its own page-count default (blockfrost-js `lib/utils/index.js`).
 */
export const UTXO_PAGE_BATCH = 10;
export async function fetchUtxosAll(address: string) {
  if (!blockfrost) return [];
  try {
    return await blockfrost.addressesUtxosAll(address, { batchSize: UTXO_PAGE_BATCH });
  } catch (err: any) {
    if (err?.status_code === 404) return [];
    throw err;
  }
}

/**
 * KS-1384 F0 (the fourth review's m-2a): the live tip from an ANSWERED read, or null. Never 0: a slot of 0 or a
 * missing slot is not an answer, and the boot arm must not read it as one (`fetchProtocolParams` writes
 * `tip.slot || 0`, which is fine for its own use and wrong for the arm's).
 */
export async function fetchLiveTip(): Promise<{ slot: number; height: number | null } | null> {
  if (!blockfrost) return null;
  try {
    const tip = await blockfrost.blocksLatest();
    const slot = tip?.slot;
    if (typeof slot !== 'number' || !Number.isInteger(slot) || slot <= 0) return null;
    const height = typeof tip.height === 'number' ? tip.height : null;
    return { slot, height };
  } catch (err: any) {
    logger.warn('[Cardano] Live tip read failed', { error: err?.message });
    return null;
  }
}

/**
 * KS-1384 F0 (design §3.4 rule 4, the fourth review's m-6 and m-8): the transaction that consumed an output.
 * Returns the spender's hash, or null when it is UNKNOWN: the provider says `consumed_by_tx` is null or absent
 * (it is optional in the SDK's types), the output is not listed, the transaction is not found, or the read
 * failed. A caller reads null as "rest the row", never as "unspent" and never as "a foreign spender".
 */
export async function fetchOutputSpender(txHash: string, index: number): Promise<string | null> {
  if (!blockfrost) return null;
  try {
    const utxos = await blockfrost.txsUtxos(txHash);
    const out = utxos?.outputs?.find((o: { output_index: number }) => o.output_index === index) as
      | { consumed_by_tx?: string | null }
      | undefined;
    const spender = out?.consumed_by_tx;
    return typeof spender === 'string' && /^[0-9a-f]{64}$/i.test(spender) ? spender : null;
  } catch (err: any) {
    logger.warn('[Cardano] Output spender read failed', { txHash, index, error: err?.message });
    return null;
  }
}

/**
 * KS-1384 F0 (A1): a transaction's metadata under one label. `undefined` = the transaction carries no such label
 * (the chain answered); null = the read failed or the transaction is not found (unknown).
 */
export async function fetchTxLabelMetadata(txHash: string, label: number): Promise<unknown | null | undefined> {
  if (!blockfrost) return null;
  try {
    const rows = await blockfrost.txsMetadata(txHash);
    const row = (rows ?? []).find((r: { label: string }) => r.label === String(label)) as
      | { json_metadata?: unknown }
      | undefined;
    return row ? row.json_metadata : undefined;
  } catch (err: any) {
    logger.warn('[Cardano] Transaction metadata read failed', { txHash, label, error: err?.message });
    return null;
  }
}

/**
 * Submit a signed transaction (CBOR bytes) via Blockfrost.
 */
export async function submitTransaction(txCborHex: string): Promise<string> {
  if (!blockfrost) throw new Error('Blockfrost provider not initialised');

  const txBytes = Buffer.from(txCborHex, 'hex');
  return await blockfrost.txSubmit(txBytes);
}

/**
 * Check if a transaction has been confirmed on chain.
 * Returns the transaction details or null if not yet confirmed.
 */
export async function getTransaction(txHash: string) {
  if (!blockfrost) return null;
  try {
    return await blockfrost.txs(txHash);
  } catch (err: any) {
    // 404 = the chain answered: tx not on chain yet. Reachability is recorded
    // by the client proxy; this only decides what the CALLER gets back.
    if (err?.status_code === 404) return null;
    throw err;
  }
}
