/**
 * =============================================================================
 * QUALIFIED TSA PROVIDERS FOR eIDAS COMPLIANCE
 * =============================================================================
 * This module provides integration with eIDAS-qualified Time Stamp Authorities
 * for legally binding timestamps in the EU and other regulated jurisdictions.
 * 
 * Compliance:
 * - eIDAS Regulation (EU) 910/2014
 * - UK Electronic Communications Act 2000
 * - Various regional electronic signature laws
 * 
 * Reference: https://ec.europa.eu/digital-building-blocks/wikis/display/DIGITAL/eIDAS
 * =============================================================================
 */

import crypto from 'crypto';
import { requestTimestamp as rfc3161Request, RFC3161Response } from './rfc3161-client';
import { logger } from '../utils/logger';
import { readFileSync } from 'fs';
import { verifyRfc3161Token } from './rfc3161-verify';

// =============================================================================
// TYPES
// =============================================================================

export interface QualifiedTSAProvider {
  /** Provider name */
  name: string;
  /** TSA endpoint URL */
  url: string;
  /** Region/jurisdiction */
  region: 'eu' | 'uk' | 'us' | 'global';
  /** URL to certificate chain for verification */
  certificateChainUrl: string;
  /** Whether this provider is eIDAS qualified */
  eidasQualified: boolean;
  /** Supported hash algorithms */
  supportedAlgorithms: string[];
  /** Provider status */
  status: 'active' | 'deprecated' | 'testing';
  /** Authentication method if required */
  authMethod?: 'none' | 'basic' | 'certificate' | 'api_key';
}

export interface TimestampRequest {
  /** Hash of the data to timestamp (hex encoded) */
  hash: string;
  /** Hash algorithm used */
  hashAlgorithm: 'SHA-256' | 'SHA-384' | 'SHA-512';
  /** Optional nonce for request uniqueness */
  nonce?: string;
  /** Request policy OID */
  policyOid?: string;
}

export interface TimestampResponse {
  /** Whether the timestamp was successful */
  success: boolean;
  /** The timestamp token (base64 encoded) */
  token?: string;
  /** Timestamp in ISO format */
  timestamp?: string;
  /** Serial number of the timestamp */
  serialNumber?: string;
  /** TSA name that issued the timestamp */
  tsaName?: string;
  /** Error message if failed */
  error?: string;
  /** Provider used */
  provider: string;
  /** Whether this is eIDAS qualified */
  eidasQualified: boolean;
}

export interface TimestampVerification {
  /** Whether the timestamp is valid */
  valid: boolean;
  /** Original hash that was timestamped */
  originalHash?: string;
  /** Timestamp from the token */
  timestamp?: string;
  /** TSA certificate information */
  tsaCertificate?: {
    subject: string;
    issuer: string;
    validFrom: string;
    validTo: string;
  };
  /** Error message if verification failed */
  error?: string;
}

// =============================================================================
// QUALIFIED TSA PROVIDERS
// =============================================================================

export const QUALIFIED_TSA_PROVIDERS: QualifiedTSAProvider[] = [
  // EU Qualified Providers
  {
    name: 'D-Trust GmbH',
    url: 'https://timestamp.d-trust.net/tsa',
    region: 'eu',
    certificateChainUrl: 'https://www.d-trust.net/cgi-bin/D-TRUST_Root_CA_1_2017.crt',
    eidasQualified: true,
    supportedAlgorithms: ['SHA-256', 'SHA-384', 'SHA-512'],
    status: 'active',
    authMethod: 'none',
  },
  {
    name: 'Swisscom Trust Services',
    url: 'https://tsa.swisscom.com/ais-server',
    region: 'eu',
    certificateChainUrl: 'https://www.swisscom.ch/en/business/enterprise/offer/security/digital-certificate/swisscom-root-ca-2.html',
    eidasQualified: true,
    supportedAlgorithms: ['SHA-256', 'SHA-512'],
    status: 'active',
    authMethod: 'certificate',
  },
  {
    name: 'QuoVadis (DigiCert)',
    url: 'https://timestamp.quovadisglobal.com/tsa',
    region: 'eu',
    certificateChainUrl: 'https://www.quovadisglobal.com/QVRepository/DownloadRootsAndCRLs.aspx',
    eidasQualified: true,
    supportedAlgorithms: ['SHA-256', 'SHA-384', 'SHA-512'],
    status: 'active',
    authMethod: 'none',
  },
  {
    name: 'Certum (Asseco)',
    url: 'http://time.certum.pl',
    region: 'eu',
    certificateChainUrl: 'https://www.certum.eu/en/cert_expertise_root_certificates/',
    eidasQualified: true,
    supportedAlgorithms: ['SHA-256', 'SHA-512'],
    status: 'active',
    authMethod: 'none',
  },
  
  // UK Providers
  {
    name: 'GlobalSign UK',
    url: 'http://timestamp.globalsign.com/tsa/r6advanced1',
    region: 'uk',
    certificateChainUrl: 'https://www.globalsign.com/en/repository',
    eidasQualified: false, // UK post-Brexit
    supportedAlgorithms: ['SHA-256', 'SHA-384', 'SHA-512'],
    status: 'active',
    authMethod: 'none',
  },
  
  // US/Global Providers
  {
    name: 'DigiCert',
    url: 'http://timestamp.digicert.com',
    region: 'us',
    certificateChainUrl: 'https://www.digicert.com/kb/digicert-root-certificates.htm',
    eidasQualified: false,
    supportedAlgorithms: ['SHA-256', 'SHA-384', 'SHA-512'],
    status: 'active',
    authMethod: 'none',
  },
  {
    name: 'Sectigo',
    url: 'http://timestamp.sectigo.com',
    region: 'global',
    certificateChainUrl: 'https://support.sectigo.com/articles/Knowledge/Sectigo-Intermediate-Certificates',
    eidasQualified: false,
    supportedAlgorithms: ['SHA-256', 'SHA-384', 'SHA-512'],
    status: 'active',
    authMethod: 'none',
  },
  {
    name: 'Entrust',
    url: 'http://timestamp.entrust.net/TSS/RFC3161sha2TS',
    region: 'global',
    certificateChainUrl: 'https://www.entrust.com/resources/certificate-solutions/certificate-download',
    eidasQualified: false,
    supportedAlgorithms: ['SHA-256'],
    status: 'active',
    authMethod: 'none',
  },
];

// =============================================================================
// PROVIDER SELECTION
// =============================================================================

/**
 * Select appropriate TSA provider based on requirements
 */
export function selectTSAProvider(options: {
  region?: 'eu' | 'uk' | 'us' | 'global';
  requireEidas?: boolean;
  preferredProvider?: string;
}): QualifiedTSAProvider {
  const { region, requireEidas = false, preferredProvider } = options;
  
  // Filter active providers
  let candidates = QUALIFIED_TSA_PROVIDERS.filter(p => p.status === 'active');
  
  // Filter by preferred provider if specified
  if (preferredProvider) {
    const preferred = candidates.find(p => 
      p.name.toLowerCase().includes(preferredProvider.toLowerCase())
    );
    if (preferred) return preferred;
  }
  
  // Filter by eIDAS requirement
  if (requireEidas) {
    candidates = candidates.filter(p => p.eidasQualified);
    if (candidates.length === 0) {
      throw new Error('No eIDAS-qualified TSA providers available');
    }
  }
  
  // Filter by region
  if (region) {
    const regionalCandidates = candidates.filter(p => p.region === region);
    if (regionalCandidates.length > 0) {
      candidates = regionalCandidates;
    }
    // Fall back to global providers if no regional match
  }
  
  // Return first matching provider (could implement load balancing here)
  return candidates[0];
}

/**
 * Get all available providers for a region
 */
export function getProvidersForRegion(region: 'eu' | 'uk' | 'us' | 'global'): QualifiedTSAProvider[] {
  return QUALIFIED_TSA_PROVIDERS.filter(p => 
    p.status === 'active' && (p.region === region || p.region === 'global')
  );
}

/**
 * Get all eIDAS-qualified providers
 */
export function getEidasQualifiedProviders(): QualifiedTSAProvider[] {
  return QUALIFIED_TSA_PROVIDERS.filter(p => p.status === 'active' && p.eidasQualified);
}

// =============================================================================
// TIMESTAMP OPERATIONS
// =============================================================================

/**
 * Create a timestamp using a real RFC-3161 TSA.
 *
 * Builds a proper ASN.1 DER-encoded TimeStampReq, submits it to the TSA,
 * and parses the TimeStampResp. Falls back to a mock token if no TSA is
 * reachable (development/offline mode).
 */
export async function createTimestamp(
  request: TimestampRequest,
  provider?: QualifiedTSAProvider
): Promise<TimestampResponse> {
  const selectedProvider = provider || selectTSAProvider({ region: 'eu' });

  // If a custom TSA URL is configured, use it; otherwise use the provider's URL
  const tsaUrl = process.env.TSA_URL || selectedProvider.url;
  const authKey = process.env.TSA_AUTH_KEY;
  const authHeader = authKey ? `Bearer ${authKey}` : undefined;

  logger.info('[TSA] Requesting RFC-3161 timestamp', { provider: selectedProvider.name, tsaUrl });
  logger.info('[TSA] Hash', { hash: request.hash.substring(0, 20) + '...' });

  try {
    // Attempt real RFC-3161 request
    const rfc3161Result: RFC3161Response = await rfc3161Request(
      request.hash,
      request.hashAlgorithm,
      tsaUrl,
      authHeader,
    );

    if (rfc3161Result.success && rfc3161Result.token) {
      logger.info('[TSA] Timestamp received', { provider: selectedProvider.name });
      if (rfc3161Result.timestamp) {
        logger.info('[TSA] GenTime', { genTime: rfc3161Result.timestamp });
      }
      return {
        success: true,
        token: rfc3161Result.token,
        timestamp: rfc3161Result.timestamp || new Date().toISOString(),
        serialNumber: rfc3161Result.serialNumber,
        tsaName: rfc3161Result.tsaName || selectedProvider.name,
        provider: selectedProvider.name,
        eidasQualified: selectedProvider.eidasQualified,
      };
    }

    // TSA returned an error — log and fall through to mock
    logger.warn('[TSA] RFC-3161 request failed', { error: rfc3161Result.error });

  } catch (err: any) {
    logger.warn('[TSA] RFC-3161 request exception', { error: err?.message });
  }

  // ── Mock fallback (development / offline) ───────────────────────────────
  logger.info('[TSA] Falling back to mock timestamp token');
  const nonce = request.nonce || crypto.randomBytes(8).toString('hex');
  const timestamp = new Date().toISOString();
  const serialNumber = crypto.randomBytes(16).toString('hex');

  return {
    success: true,
    token: Buffer.from(JSON.stringify({
      hash: request.hash,
      hashAlgorithm: request.hashAlgorithm,
      nonce,
      timestamp,
      serialNumber,
      provider: selectedProvider.name,
      type: 'rfc3161',
      mock: true,
    })).toString('base64'),
    timestamp,
    serialNumber,
    tsaName: `${selectedProvider.name} (mock)`,
    provider: selectedProvider.name,
    eidasQualified: false,
  };
}

/**
 * Verify a timestamp token.
 *
 * Handles two token formats:
 * 1. Real ASN.1 DER tokens (base64-encoded ContentInfo from an RFC-3161 TSA)
 * 2. Mock JSON tokens (base64-encoded JSON produced by our development fallback)
 */
export async function verifyTimestamp(
  token: string,
  originalHash: string
): Promise<TimestampVerification> {
  // KS 1404. The old implementation routed by FIRST BYTE: a DER token (0x30) went to a walk that
  // accepted any token merely CONTAINING the expected digest, and ANY OTHER token went to
  // verifyMockToken, which returned valid:true whenever a JSON `hash` field matched. Both accepted
  // unsigned input. Both are gone.
  //
  // Q4, ruled by Wednesday 2026-10-04T12:55Z: DB-ROW-ONLY. The parser refuses every non-DER token
  // outright; a mock token verifies only through the DB-row branch in index.ts (same hash AND
  // byte-identical proof), never through here. "Refuse unless mock:true" was rejected because a
  // forger can simply add mock:true, so it does not close the path — and Kam's ruling says both
  // forgeable paths close.
  //
  // BEHAVIOUR CHANGE, named in the PR body: a mock token that is NOT stored in the DB no longer
  // verifies.
  const tokenBuf = Buffer.from(token, 'base64');
  if (tokenBuf.length === 0 || tokenBuf[0] !== 0x30) {
    return {
      valid: false,
      error:
        'Timestamp proof is not a DER-encoded RFC 3161 token; a stored mock token verifies only through its database record',
    };
  }

  const result = await verifyRfc3161Token({
    tokenBase64: token,
    expectedHashHex: originalHash,
    trustAnchorsPem: readTrustAnchorsPem(),
  });

  return {
    valid: result.valid,
    originalHash: result.valid ? originalHash : undefined,
    timestamp: result.timestamp,
    tsaCertificate: result.tsaCertificate
      ? {
          subject: result.tsaCertificate.subject ?? 'Unknown',
          issuer: result.tsaCertificate.issuer ?? result.tsaCertificate.subject ?? 'Unknown',
          validFrom: result.tsaCertificate.validFrom,
          validTo: result.tsaCertificate.validTo,
        }
      : undefined,
    error: result.reason,
  };
}

/**
 * The configured trust anchors, as a PEM bundle.
 *
 * `TSA_TRUST_ANCHORS_PEM` holds either the PEM text itself or a path to a file containing it.
 * Kam ruled (card secuura-ks1404-tsa-trust-and-library-1004, option a) that we trust the authority
 * each environment's `TSA_URL` already points at. Those providers' PUBLISHED roots are committed at
 * `config/tsa-trust-anchors.crt` (`.crt`, not `.pem`: preflight leg 9 refuses a tracked `*.pem` as a
 * credential — KS-646 — and these are public CA roots), with their source URLs, SHA-256
 * fingerprints, read time and
 * second-source status recorded in `config/README.md`. This variable is how an operator SELECTS
 * them: it holds the PEM text or a path, and there is deliberately no default. Unset or empty means
 * NO anchor, and the verifier then fails CLOSED.
 *
 * NOT COVERED, and in the PR body: nothing is wired into any environment by this change, so no box
 * has an anchor in effect yet; box-only `TSA_URL` values are unmeasured; and pinning a root does not
 * prove it anchors that authority's signing chain.
 */
function readTrustAnchorsPem(): string | undefined {
  const raw = process.env.TSA_TRUST_ANCHORS_PEM;
  if (!raw || !raw.trim()) return undefined;
  if (raw.includes('-----BEGIN CERTIFICATE-----')) return raw;
  try {
    return readFileSync(raw, 'utf-8');
  } catch (err: any) {
    logger.error('[TSA] TSA_TRUST_ANCHORS_PEM points at a file that could not be read', {
      error: err?.message,
    });
    return undefined;
  }
}

// =============================================================================
// EXPORTS
// =============================================================================

export default {
  providers: QUALIFIED_TSA_PROVIDERS,
  selectTSAProvider,
  getProvidersForRegion,
  getEidasQualifiedProviders,
  createTimestamp,
  verifyTimestamp,
};
