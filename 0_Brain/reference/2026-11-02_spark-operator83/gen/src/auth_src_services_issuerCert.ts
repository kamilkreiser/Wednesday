/**
 * =============================================================================
 * ISSUER CERT SERVICE — KS-83 PR 1
 * =============================================================================
 * X.509 cert parsing, key-matching verification, and at-rest encryption of
 * the private key. Pure domain logic — no DB, no Express, easy to unit test.
 *
 * What this module owns:
 *   1. Parse a PEM-encoded cert via node:crypto X509Certificate.
 *   2. Parse an (optionally passphrase-protected) PEM private key.
 *   3. Verify the key matches the cert (sign + verify roundtrip on a nonce).
 *   4. Compute the SHA-256 fingerprint of the DER cert (uniqueness key).
 *   5. Detect trust level: self-signed vs ca-anchored vs aatl.
 *   6. Encrypt + decrypt the private-key PEM via packages/shared encryptField.
 *
 * What it does NOT own (lives in repo + route layers):
 *   - DB persistence — repository
 *   - HTTP validation / status codes — route
 *   - RBAC — route (via packages/shared scopes + role allow-list)
 *   - Tenant scoping — repository (RLS in Postgres) + route (req.tenantId)
 *
 * Trust-level policy (KS-83 sub-decision 2):
 *   * `subject == issuer` → 'self-signed' (allowed in v1, surfaced in
 *     metadata + verify response so consumers can decide).
 *   * Otherwise → 'ca-anchored'. We do NOT validate the chain in v1 —
 *     we take the caller's assertion. PR 2 / v2 introduces real chain
 *     validation against bundled CA roots.
 *   * `aatl` is reserved for PR 2 / v2 (Adobe Approved Trust List
 *     membership requires fetching the AATL CSV and matching against it).
 * =============================================================================
 */

import * as crypto from 'crypto';
import { encryptField, decryptField } from '@secuura/shared';

// =============================================================================
// TYPES
// =============================================================================

export type TrustLevel = 'self-signed' | 'ca-anchored' | 'aatl';

export interface ParsedCert {
  /** Public cert in PEM form, normalised (trailing newline stripped). */
  certPem: string;
  /** SHA-256 of the DER-encoded cert, hex-encoded — uniqueness key. */
  fingerprintSha256: string;
  /** Subject DN, e.g. "CN=Acme Corp, O=Acme, C=US". */
  subject: string;
  /** Issuer DN; equals subject for self-signed. */
  issuer: string;
  serialNumber: string;
  /** Cert validity start (UTC). */
  validFrom: Date;
  /** Cert validity end (UTC). */
  validUntil: Date;
  /** 'RSA' | 'EC' | 'Ed25519' | 'unknown'. */
  keyAlgorithm: string;
  /** Bits for RSA keys; null for EC / Ed25519 (where bits is not the right unit). */
  keySizeBits: number | null;
  /** v1: 'self-signed' if subject == issuer, else 'ca-anchored'. */
  trustLevel: TrustLevel;
}

export class IssuerCertError extends Error {
  constructor(public code: string, message: string) {
    super(message);
    this.name = 'IssuerCertError';
  }
}

// =============================================================================
// PARSING
// =============================================================================

/**
 * Parse a PEM-encoded X.509 cert. Returns the metadata plus a normalised
 * cert PEM (trailing whitespace trimmed; multi-cert PEM bundles rejected
 * because v1 only accepts a single end-entity cert — chain handling is
 * v2 work).
 *
 * Throws `IssuerCertError` with stable codes the route layer maps to
 * 4xx responses:
 *   - INVALID_CERT_PEM        — couldn't parse as X.509
 *   - MULTI_CERT_PEM          — caller sent a chain; v1 accepts single cert only
 *   - CERT_EXPIRED            — validUntil < now (refused at upload — KS-83 sub-decision 3)
 *   - CERT_NOT_YET_VALID      — validFrom > now (probably a clock or paste error)
 */
export function parseCert(certPem: string): ParsedCert {
  if (typeof certPem !== 'string' || certPem.trim() === '') {
    throw new IssuerCertError('INVALID_CERT_PEM', 'certPem is required');
  }

  const trimmed = certPem.trim();

  // Reject multi-cert PEM bundles (chain). v1 = single end-entity cert.
  const beginMatches = trimmed.match(/-----BEGIN CERTIFICATE-----/g);
  if (!beginMatches || beginMatches.length === 0) {
    throw new IssuerCertError(
      'INVALID_CERT_PEM',
      'certPem is not a PEM-encoded X.509 cert (missing BEGIN CERTIFICATE)',
    );
  }
  if (beginMatches.length > 1) {
    throw new IssuerCertError(
      'MULTI_CERT_PEM',
      'certPem contains multiple certs; v1 accepts a single end-entity cert. Strip intermediates.',
    );
  }

  let cert: crypto.X509Certificate;
  try {
    cert = new crypto.X509Certificate(trimmed);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    throw new IssuerCertError('INVALID_CERT_PEM', `Could not parse cert: ${msg}`);
  }

  const validFrom = new Date(cert.validFrom);
  const validUntil = new Date(cert.validTo);
  const now = new Date();

  // Refuse expired certs at upload time (KS-83 sub-decision 3 — refuse new
  // signings on expired cert; uploads are signings-of-tomorrow).
  if (validUntil.getTime() < now.getTime()) {
    throw new IssuerCertError(
      'CERT_EXPIRED',
      `Cert expired at ${validUntil.toISOString()}; refusing upload. Existing signatures made when the cert was valid stay valid forever.`,
    );
  }

  // Reject not-yet-valid certs (probably a paste error — fail loud rather
  // than silently store a cert nobody can use until N days from now).
  if (validFrom.getTime() > now.getTime() + 24 * 60 * 60 * 1000) {
    throw new IssuerCertError(
      'CERT_NOT_YET_VALID',
      `Cert validFrom is ${validFrom.toISOString()} (more than 24h in the future). Check system clock or cert.`,
    );
  }

  // SHA-256 fingerprint of the DER bytes.
  const der = cert.raw;
  const fingerprintSha256 = crypto.createHash('sha256').update(der).digest('hex');

  // Algorithm + size from the public key.
  const pubKey = cert.publicKey;
  const keyDetails = pubKey.asymmetricKeyDetails || {};
  let keyAlgorithm = pubKey.asymmetricKeyType || 'unknown';
  // Node reports 'rsa', 'ec', 'ed25519' lowercase — uppercase the canonical names
  if (keyAlgorithm === 'rsa') keyAlgorithm = 'RSA';
  else if (keyAlgorithm === 'ec') keyAlgorithm = 'EC';
  else if (keyAlgorithm === 'ed25519') keyAlgorithm = 'Ed25519';
  const keySizeBits = typeof keyDetails.modulusLength === 'number' ? keyDetails.modulusLength : null;

  // Trust level: self-signed iff subject DN == issuer DN. We don't
  // validate the chain in v1 — caller's assertion. KS-83 sub-decision 2.
  const trustLevel: TrustLevel = cert.subject === cert.issuer ? 'self-signed' : 'ca-anchored';

  return {
    certPem: trimmed + '\n',
    fingerprintSha256,
    subject: cert.subject,
    issuer: cert.issuer,
    serialNumber: cert.serialNumber,
    validFrom,
    validUntil,
    keyAlgorithm,
    keySizeBits,
    trustLevel,
  };
}

// =============================================================================
// KEY MATCHING
// =============================================================================

/**
 * Verify a private key matches a cert's public key by signing a random
 * nonce and verifying with the cert's public key. Throws IssuerCertError
 * with code KEY_MISMATCH on failure (and KEY_PARSE_ERROR if the key PEM
 * is malformed or the passphrase is wrong).
 *
 * Why a sign-and-verify roundtrip rather than comparing key params: it
 * works uniformly across RSA / EC / Ed25519, it tests the actual signing
 * flow we'll use later, and it doesn't rely on internal key serialisation.
 */
export function verifyKeyMatchesCert(
  certPem: string,
  privateKeyPem: string,
  passphrase?: string,
): void {
  let privateKey: crypto.KeyObject;
  try {
    privateKey = crypto.createPrivateKey({
      key: privateKeyPem,
      format: 'pem',
      ...(passphrase ? { passphrase } : {}),
    });
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    // Distinguish "wrong passphrase" from "malformed PEM" if we can.
    if (passphrase && /bad decrypt|invalid|incorrect/i.test(msg)) {
      throw new IssuerCertError('KEY_PARSE_ERROR', 'Private key passphrase is incorrect or key is malformed');
    }
    throw new IssuerCertError('KEY_PARSE_ERROR', `Could not parse private key: ${msg}`);
  }

  const cert = new crypto.X509Certificate(certPem);
  const publicKey = cert.publicKey;

  // Pick a sign algorithm based on key type. Ed25519 has no separate
  // hash — pass null. RSA/EC default to SHA-256.
  const algo: string | null = privateKey.asymmetricKeyType === 'ed25519' ? null : 'sha256';
  const nonce = crypto.randomBytes(32);

  let signature: Buffer;
  try {
    signature = crypto.sign(algo, nonce, privateKey);
  } catch (err) {
    const msg = err instanceof Error ? err.message : String(err);
    throw new IssuerCertError('KEY_MISMATCH', `Could not sign with private key: ${msg}`);
  }

  let verified = false;
  try {
    verified = crypto.verify(algo, nonce, publicKey, signature);
  } catch (err) {
    // verify() can throw on key-type mismatch (e.g. RSA cert + EC key)
    throw new IssuerCertError('KEY_MISMATCH', 'Private key does not match cert public key (algorithm mismatch)');
  }

  if (!verified) {
    throw new IssuerCertError('KEY_MISMATCH', 'Private key does not match cert public key');
  }
}

// =============================================================================
// ENCRYPTION (envelope around packages/shared encryptField)
// =============================================================================

/**
 * AAD context for the encrypted private key. Binds the ciphertext to the
 * cert row's id — swapping ciphertexts between rows fails AES-GCM
 * verification rather than silently decrypting to the wrong key.
 */
export function privateKeyAadContext(certId: string): string {
  if (!certId || typeof certId !== 'string') {
    throw new IssuerCertError('INVALID_CERT_ID', 'certId is required for AAD context');
  }
  return `issuer_certs.private_key.${certId}`;
}

/**
 * Encrypt a private-key PEM for at-rest storage. Returns the
 * `v<N>:iv:tag:ciphertext` blob to write into `encrypted_private_key`.
 *
 * The keyring (PII_ENCRYPTION_KEY) MUST be initialised at service
 * startup — the auth service already does this for PII columns, so
 * issuer-certs piggy-backs on the same keyring.
 */
export function encryptPrivateKeyPem(privateKeyPem: string, certId: string): string {
  const ctx = privateKeyAadContext(certId);
  const result = encryptField(privateKeyPem, ctx);
  if (result === null) {
    throw new IssuerCertError('ENCRYPTION_FAILED', 'Refused to encrypt empty private key');
  }
  return result;
}

/**
 * Decrypt a stored private-key blob. Used by the sign-cert endpoint (PR 3).
 */
export function decryptPrivateKeyPem(encrypted: string, certId: string): string {
  const ctx = privateKeyAadContext(certId);
  const result = decryptField(encrypted, ctx);
  if (result === null) {
    throw new IssuerCertError('DECRYPTION_FAILED', 'Stored private key is empty');
  }
  return result;
}

// =============================================================================
// SIGNING (KS-83 PR 3)
// =============================================================================

export interface SignatureEnvelope {
  /** Base64-encoded signature bytes. */
  signature: string;
  /** JOSE-style algorithm tag — RS256 / ES256 / EdDSA. */
  signatureAlgorithm: 'RS256' | 'ES256' | 'EdDSA';
  /** Hex sha256 digest that was signed (the input to crypto.sign). */
  signedContentHash: string;
  signedAt: string;
}

/**
 * Map a node:crypto key type to a JOSE-style algorithm tag, and pick the
 * digest algorithm crypto.sign() expects. Ed25519 wants `null` as the
 * digest argument (the signature spec hashes internally); RSA/EC want 'sha256'.
 */
export function pickSignAlgorithm(
  keyAlgorithm: string,
): { joseAlg: SignatureEnvelope['signatureAlgorithm']; digest: string | null } {
  const algo = keyAlgorithm.toUpperCase();
  if (algo === 'RSA') return { joseAlg: 'RS256', digest: 'sha256' };
  if (algo === 'EC') return { joseAlg: 'ES256', digest: 'sha256' };
  if (algo === 'ED25519') return { joseAlg: 'EdDSA', digest: null };
  throw new IssuerCertError('UNSUPPORTED_KEY_ALGORITHM', `Cannot sign with key algorithm '${keyAlgorithm}' (supported: RSA, EC, Ed25519)`);
}

/**
 * Sign a content hash with a cert's private key. The caller supplies:
 *   - the encrypted private key blob + the cert id (for AAD context)
 *   - the cert's key algorithm (so we pick the right sign algorithm)
 *   - the contentHash to sign — accepted as 64 lowercase hex chars (with
 *     optional `sha256:` prefix), the same format the documents service
 *     uses everywhere.
 *
 * Returns the signature + algorithm + canonical hash + timestamp.
 * Throws IssuerCertError on:
 *   - INVALID_CONTENT_HASH (not sha256 hex)
 *   - UNSUPPORTED_KEY_ALGORITHM (cert key isn't RSA/EC/Ed25519)
 *   - SIGN_FAILED (crypto.sign threw — key/algorithm mismatch in practice)
 */
export function signContentHashWithCert(input: {
  encryptedPrivateKey: string;
  certId: string;
  keyAlgorithm: string;
  contentHash: string;
}): SignatureEnvelope {
  const normalisedHash = input.contentHash.replace(/^sha256:/i, '').toLowerCase();
  if (!/^[a-f0-9]{64}$/.test(normalisedHash)) {
    throw new IssuerCertError(
      'INVALID_CONTENT_HASH',
      'contentHash must be a sha256 hex digest (64 lowercase hex chars, optional sha256: prefix)',
    );
  }

  const { joseAlg, digest } = pickSignAlgorithm(input.keyAlgorithm);

  // Decrypt the private key (AAD-bound to certId).
  const privateKeyPem = decryptPrivateKeyPem(input.encryptedPrivateKey, input.certId);

  let privateKey: crypto.KeyObject;
  try {
    privateKey = crypto.createPrivateKey({ key: privateKeyPem, format: 'pem' });
  } catch (err) {
    throw new IssuerCertError(
      'SIGN_FAILED',
      `Could not load decrypted private key: ${err instanceof Error ? err.message : String(err)}`,
    );
  }

  // We sign the RAW hash bytes (32 bytes for sha256). Don't re-hash —
  // the document hash is already the canonical input.
  const hashBytes = Buffer.from(normalisedHash, 'hex');

  let signature: Buffer;
  try {
    signature = crypto.sign(digest, hashBytes, privateKey);
  } catch (err) {
    throw new IssuerCertError(
      'SIGN_FAILED',
      `crypto.sign failed: ${err instanceof Error ? err.message : String(err)}`,
    );
  }

  return {
    signature: signature.toString('base64'),
    signatureAlgorithm: joseAlg,
    signedContentHash: `sha256:${normalisedHash}`,
    signedAt: new Date().toISOString(),
  };
}
