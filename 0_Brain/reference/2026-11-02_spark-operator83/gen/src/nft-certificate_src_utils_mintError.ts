/**
 * =============================================================================
 * MINT FAILURE CLASSIFICATION (KS-444)
 * =============================================================================
 * The mint pipeline can fail for three distinct reasons that deserve three
 * distinct HTTP statuses (KS-445 precedent — never answer a non-client fault
 * with a 400):
 *
 *   - the referenced certification does not exist            → 404
 *   - an upstream dependency (chain backend / IPFS) is down  → 503
 *   - a genuine client fault (e.g. an unparseable bech32
 *     wallet address rejected by the Cardano SDK)            → 400
 *
 * Pure functions, no imports — safe to unit-test in isolation.
 * =============================================================================
 */

/** Failure classes surfaced to the route layer via MintNFTResponse.errorCode. */
export type MintFailureCode =
  | 'CERTIFICATION_NOT_FOUND'
  | 'MINT_DEPENDENCY_UNAVAILABLE'
  | 'MINT_FAILED';

/**
 * Normalise a thrown value and classify the failure.
 *
 * The Cardano serialization lib throws plain STRINGS for bech32 address
 * parse errors (e.g. 'invalid checksum', 'missing human-readable
 * separator, "1"'). `(error as Error).message` on a string is undefined,
 * which JSON.stringify silently drops — the observed KS-444 defect where
 * the 400 body carried no message at all. Always fall back to String(error).
 */
export function classifyMintError(error: unknown): {
  message: string;
  errorCode: MintFailureCode;
} {
  const message = error instanceof Error ? error.message : String(error);

  // The certification referenced in the request body does not exist —
  // a business not-found, never a client-syntax fault.
  if (message === 'Certification not found') {
    return { message, errorCode: 'CERTIFICATION_NOT_FOUND' };
  }

  // Known dependency-unavailable markers thrown by the mint pipeline:
  // cardano/index.ts guards (readiness, protocol params, chain submission)
  // and the IPFS upload wrapper in minting.service.
  if (
    message === 'Cardano NFT integration not ready' ||
    message === 'Protocol parameters unavailable' ||
    message === 'Blockfrost provider not initialised' ||
    message.startsWith('Transaction submission failed') ||
    message.startsWith('IPFS upload failed')
  ) {
    return { message, errorCode: 'MINT_DEPENDENCY_UNAVAILABLE' };
  }

  // Everything else stays a client-fault default (400) — e.g. wallet
  // addresses that pass the schema's min-length but are not valid bech32.
  return { message, errorCode: 'MINT_FAILED' };
}

/**
 * Map a mint failure class to its honest HTTP status.
 */
export function mintFailureHttpStatus(
  errorCode: string | undefined,
): 400 | 404 | 503 {
  if (errorCode === 'CERTIFICATION_NOT_FOUND') return 404;
  if (errorCode === 'MINT_DEPENDENCY_UNAVAILABLE') return 503;
  return 400;
}

/**
 * Map an HTTP status chosen by mintFailureHttpStatus to the platform's
 * canonical error envelope code.
 */
export function mintFailureEnvelopeCode(
  status: 400 | 404 | 503,
): 'BAD_REQUEST' | 'NOT_FOUND' | 'SERVICE_UNAVAILABLE' {
  if (status === 404) return 'NOT_FOUND';
  if (status === 503) return 'SERVICE_UNAVAILABLE';
  return 'BAD_REQUEST';
}
