/**
 * =============================================================================
 * ANCHOR HONESTY (KS-587 — document-blob leg)
 * =============================================================================
 * Originate's single source of the KS-522/KS-587 honest-labelling rules:
 * a `tx_sim_` / `mock_tx_` / `tx_…` placeholder corresponds to NO Cardano
 * transaction and must never be presented as an on-chain claim.
 *
 * The anchoring service's READ + POST surfaces have applied these rules since
 * KS-587 (services/anchoring/src/honestAnchor.ts — this module mirrors it).
 * What they did NOT cover is the document's own `blockchain` blob: none of
 * its writers propagated the anchor's `simulated` flag outside the explicit
 * SIMULATE_ANCHORING branch, so `presentBlockchainHonestly`
 * (routes/verification.ts) had neither of its inputs (no `simulated` key,
 * txHash null since KS-522) and returned mock blobs untouched — a caller
 * reading only the document could not tell the anchor is not on chain
 * (KS-589 D1), and the verifier-side protection was disarmed for that same
 * document (KS-589 D4).
 *
 * Consumers: routes/documents.ts (create-path initial write, manual-anchor
 * write, GET /:id read composition), services/anchorStateSync.ts (poll +
 * reconcile writes), routes/anchors.ts (persist/read of originate's own
 * anchor rows — re-exports from here).
 * =============================================================================
 */

/** Placeholder tx prefixes. Mirrors services/anchoring/src/honestAnchor.ts. */
export const FABRICATED_TX_PREFIX = /^(tx_sim_|mock_tx_|tx_)/;

/**
 * A row/payload counts as simulated when its flag says so OR its hash carries
 * a placeholder prefix — both, because the KS-587 incident rows proved the
 * flag can lie (they were written `simulated = false`).
 */
export function isSimulatedAnchor(transactionId: string | null | undefined, simulatedFlag?: boolean): boolean {
  return simulatedFlag === true || (!!transactionId && FABRICATED_TX_PREFIX.test(transactionId));
}

/** The honesty fields a document blockchain blob carries for a simulated anchor. */
export interface SimulatedTxFields {
  simulated?: true;
  /** The raw placeholder, machine-readable, never presented as `txHash`. */
  simulatedTxRef?: string;
}

/** The subset of an anchoring-service payload the honesty derivation reads. */
export interface AnchorHonestyInput {
  simulated?: boolean;
  simulatedTxRef?: string | null;
  txHash?: string | null;
  transactionHash?: string | null;
  transactionId?: string | null;
}

/**
 * Derive the `simulated`/`simulatedTxRef` fields to merge into a document
 * blockchain blob from an anchoring-service payload. Post-KS-587 those
 * payloads are already honest (`txHash` null, `simulated: true`,
 * `simulatedTxRef` carrying the placeholder), so this normally just carries
 * the declaration through; belt-and-braces it also detects a raw placeholder
 * hash (an older anchoring image, or originate's own SIMULATE_ANCHORING
 * synthesis) so the flag derives from the hash shape even when absent.
 *
 * Returns an empty object for a real (or undeclared-and-realistic) anchor, so
 * call sites can spread it unconditionally.
 */
export function simulatedFieldsFromAnchor(anchor: AnchorHonestyInput | null | undefined): SimulatedTxFields {
  if (!anchor) return {};
  const raw = anchor.transactionHash ?? anchor.txHash ?? anchor.transactionId ?? null;
  const ref = anchor.simulatedTxRef || (typeof raw === 'string' && FABRICATED_TX_PREFIX.test(raw) ? raw : undefined);
  if (!isSimulatedAnchor(typeof raw === 'string' ? raw : null, anchor.simulated) && !anchor.simulatedTxRef) return {};
  return { simulated: true, ...(ref ? { simulatedTxRef: ref } : {}) };
}

/**
 * Read-time honest composition for a STORED document blockchain blob (the
 * KS-522 rules applied at the serve boundary, same as the anchor READ
 * endpoints since KS-587): a placeholder is never presented as `txHash` — it
 * moves to `simulatedTxRef` with `simulated: true`. Blobs written before the
 * writer fixes (or by any writer this leg missed) therefore still read
 * honestly.
 *
 * Returns the blob unchanged (same reference) when nothing is fabricated —
 * real anchors, fail-closed states and absent blobs are untouched.
 */
export type HonestBlockchainBlob = Record<string, unknown> & {
  txHash?: string | null;
  simulated?: boolean;
  simulatedTxRef?: string;
};

export function composeHonestBlockchainBlob(
  blob: Record<string, unknown> | null | undefined,
): HonestBlockchainBlob | null | undefined {
  if (!blob || typeof blob !== 'object') return blob;
  const raw = typeof blob.txHash === 'string' ? blob.txHash : null;
  const fabricatedHash = raw !== null && FABRICATED_TX_PREFIX.test(raw);
  if (blob.simulated !== true && !fabricatedHash) return blob;
  const ref = fabricatedHash ? raw : typeof blob.simulatedTxRef === 'string' ? blob.simulatedTxRef : undefined;
  return {
    ...blob,
    txHash: fabricatedHash ? null : ((blob.txHash as string | null | undefined) ?? null),
    simulated: true,
    ...(ref ? { simulatedTxRef: ref } : {}),
  };
}
