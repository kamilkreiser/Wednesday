/**
 * Thread-mint request validation + mint-failure classification (KS-445).
 * Extracted from index.ts so both are unit-testable without booting the
 * service (index.ts calls app.listen on import) — same pattern as
 * anchorSchema.ts.
 *
 * Why this exists: POST /api/anchors/thread-mint only checked that the five
 * required fields were non-empty strings, then handed the body straight to
 * mintAndLock (cardano/threadTokenMint.ts). A fuzz-shaped body — non-hex
 * hash fields, a float/string createdAtMs (BigInt() throws), a non-hex
 * deploymentIdHex (lucid Data.to throws) — or a missing/unreachable Cardano
 * dependency (no BLOCKFROST_API_KEY / PLATFORM_WALLET_MNEMONIC on the
 * SIMULATE_ANCHORING demo stack, devnet down) all surfaced as a raw
 * 500 INTERNAL_ERROR. Invalid input is a 400; a missing/unreachable
 * dependency is a 503; only a genuinely unexpected failure keeps the 500.
 */

import { z } from 'zod';

/**
 * Mirrors the published contract exactly — ThreadMintRequestSchema in
 * anchoring.openapi.ts (64-hex hashes, 56-hex PKH, integer createdAtMs,
 * boolean dryRun). Nothing here is stricter than the spec; the schema exists
 * so spec-illegal fuzz shapes earn a 400 instead of crashing the Cardano
 * encoding layer into a 500. (documentId/documentType keep the handler's
 * long-standing non-empty requirement — the previous inline check already
 * rejected empty strings with a 400; the spec publishes it as min(1) since
 * KS-444, so the mirror is exact.)
 */
export const threadMintRequestSchema = z.object({
  documentId: z.string().min(1),
  documentHashHex: z.string().regex(/^[a-f0-9]{64}$/),
  originatorPkhHex: z.string().regex(/^[a-f0-9]{56}$/),
  documentType: z.string().min(1),
  metadataHashHex: z.string().regex(/^[a-f0-9]{64}$/),
  deploymentIdHex: z.string().optional(),
  createdAtMs: z.number().int().optional(),
  dryRun: z.boolean().optional(),
});

export type ThreadMintRequest = z.infer<typeof threadMintRequestSchema>;

/**
 * The spec declares deploymentIdHex as a plain optional string, so the schema
 * above deliberately does NOT tighten it — but a non-hex value can never
 * encode (lucid's Data.to needs an even-length hex bytestring and throws,
 * which used to be a raw 500). Guard-and-map per KS-445: a value that can
 * never succeed earns an honest 400 with a message naming the field, instead
 * of a validator rejection baked into the published schema.
 */
export function isEncodableDeploymentIdHex(value: string): boolean {
  // Even-length lowercase hex (or empty — the handler defaults '' anyway).
  return /^([a-f0-9]{2})*$/.test(value);
}

/** A classified, honestly-mapped mint failure. */
export interface ClassifiedMintError {
  status: 400 | 503;
  code: 'BAD_REQUEST' | 'SERVICE_UNAVAILABLE';
  message: string;
}

// Node/undici network failure markers — a bare syscall errno either as the
// error `code` or embedded in the message (lucid/blockfrost wrap fetch).
const NETWORK_ERRNOS = /\b(ECONNREFUSED|ECONNRESET|ENOTFOUND|ETIMEDOUT|EAI_AGAIN|EPIPE)\b/;

/**
 * Classify an error thrown by mintAndLock into an honest HTTP mapping
 * (mirrors the KS-431 billing classifier pattern). Returns null when the
 * error is unclassified — the route keeps its 500 for those.
 *
 * @param error - the caught error from the mint path.
 * @returns a {status, code, message} mapping, or null → caller answers 500.
 */
export function classifyThreadMintError(error: unknown): ClassifiedMintError | null {
  const err = error as { message?: unknown; code?: unknown };
  const msg = typeof err?.message === 'string' ? err.message : String(error);
  const errCode = typeof err?.code === 'string' ? err.code : '';

  // mintAndLock's own config guards ("mintAndLock: BLOCKFROST_API_KEY is
  // required" / "PLATFORM_WALLET_MNEMONIC is required") — the demo stack runs
  // SIMULATE_ANCHORING=true, where originate never calls thread-mint and the
  // Cardano credentials are deliberately absent, so a direct (fuzzer) call is
  // an unconfigured dependency: 503, never a server fault.
  if (/BLOCKFROST_API_KEY|PLATFORM_WALLET_MNEMONIC/.test(msg)) {
    return {
      status: 503,
      code: 'SERVICE_UNAVAILABLE',
      message: 'Cardano anchoring dependency not configured',
    };
  }

  // Contract blueprint (plutus.json) missing from the deployment — an
  // operator/deployment problem, not the caller's request.
  if (/blueprint|plutus\.json/i.test(msg) || errCode === 'ENOENT') {
    return {
      status: 503,
      code: 'SERVICE_UNAVAILABLE',
      message: 'Cardano contract blueprint unavailable',
    };
  }

  // Platform wallet has no spendable seed UTxO — an ops/funding state the
  // caller cannot influence; the mint will succeed again once funded.
  if (/no UTxO with >= 5 ADA/i.test(msg)) {
    return {
      status: 503,
      code: 'SERVICE_UNAVAILABLE',
      message: 'Cardano platform wallet not ready',
    };
  }

  // Blockfrost / devnet provider unreachable or erroring (network errno,
  // undici "fetch failed", provider-named failures) — dependency outage.
  if (
    NETWORK_ERRNOS.test(errCode) ||
    NETWORK_ERRNOS.test(msg) ||
    /fetch failed|socket hang up|network|blockfrost/i.test(msg)
  ) {
    return {
      status: 503,
      code: 'SERVICE_UNAVAILABLE',
      message: 'Cardano network provider unreachable',
    };
  }

  // lucid Data/CBOR encoding rejected a value the schema cannot pre-check
  // (defence-in-depth behind isEncodableDeploymentIdHex) — the input can
  // never encode, so it is the request's fault: 400.
  if (/invalid hex|hex string|cbor/i.test(msg)) {
    return {
      status: 400,
      code: 'BAD_REQUEST',
      message: 'Request contains a value that cannot be encoded on-chain',
    };
  }

  return null;
}
