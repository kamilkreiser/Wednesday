/**
 * =============================================================================
 * IPFS SERVICE
 * =============================================================================
 * IPFS storage integration for encrypted document storage (Premium tier)
 * Supports Pinata, Infura, and Web3.Storage
 */

import { IPFSUploadRequest, IPFSUploadResponse } from '../types';
import { logger } from '../utils/logger';
import { NotFoundError, ServiceUnavailableError } from '@secuura/shared';

// =============================================================================
// OUTBOUND TIMEOUTS (KS-1240)
// =============================================================================
// Every outbound fetch carries AbortSignal.timeout. Without one, a provider or gateway that accepts the connection
// and then goes quiet holds the caller for as long as the socket lives. The signal covers the whole exchange, body
// included, so a stalled body is cut off too. On expiry the fetch (or the body read) rejects and the existing
// handling answers: upload { success: false }, pin and unpin false, gateway read ServiceUnavailableError (503).
// Trade-off: an object the gateway needs more than the read bound to deliver now answers 503 instead of waiting.
const IPFS_UPLOAD_TIMEOUT_MS = 60_000;
const IPFS_PIN_TIMEOUT_MS = 15_000;
const IPFS_GATEWAY_READ_TIMEOUT_MS = 30_000;

// =============================================================================
// IPFS PROVIDER INTERFACE
// =============================================================================

interface IPFSProvider {
  name: string;
  upload(data: Buffer, filename: string, mimeType: string): Promise<IPFSUploadResponse>;
  pin(cid: string): Promise<boolean>;
  unpin(cid: string): Promise<boolean>;
  getGatewayUrl(cid: string): string;
  /**
   * Optional native read path. Providers that can serve content directly
   * (e.g. the in-memory mock) implement this; HTTP-gateway providers
   * (Pinata/Infura/Web3.Storage) leave it undefined and are read via the
   * gateway URL in IPFSService.fetch(). Implementations MUST throw a
   * NotFoundError for an unknown cid and a ServiceUnavailableError if the
   * backing store is unreachable — never a bare Error (KS-118).
   */
  read?(cid: string): Promise<Buffer>;
}

// =============================================================================
// PINATA PROVIDER
// =============================================================================

class PinataProvider implements IPFSProvider {
  name = 'pinata';
  private apiKey: string;
  private secretKey: string;
  private gateway: string;

  constructor(apiKey: string, secretKey: string, gateway?: string) {
    this.apiKey = apiKey;
    this.secretKey = secretKey;
    this.gateway = gateway || 'https://gateway.pinata.cloud/ipfs';
  }

  async upload(data: Buffer, filename: string, mimeType: string): Promise<IPFSUploadResponse> {
    try {
      const formData = new FormData();
      const blob = new Blob([data], { type: mimeType });
      formData.append('file', blob, filename);

      const metadata = JSON.stringify({
        name: filename,
        keyvalues: {
          app: 'secuura',
          type: 'nft-certificate',
        },
      });
      formData.append('pinataMetadata', metadata);

      const options = JSON.stringify({
        cidVersion: 1,
      });
      formData.append('pinataOptions', options);

      const response = await fetch('https://api.pinata.cloud/pinning/pinFileToIPFS', {
        method: 'POST',
        headers: {
          pinata_api_key: this.apiKey,
          pinata_secret_api_key: this.secretKey,
        },
        body: formData,
        signal: AbortSignal.timeout(IPFS_UPLOAD_TIMEOUT_MS),
      });

      if (!response.ok) {
        const error = await response.text();
        return {
          success: false,
          error: `Pinata upload failed: ${error}`,
        };
      }

      const result = await response.json() as { IpfsHash: string; PinSize: number };

      return {
        success: true,
        cid: result.IpfsHash,
        size: result.PinSize,
        pinned: true,
      };
    } catch (error) {
      return {
        success: false,
        error: `Pinata upload error: ${(error as Error).message}`,
      };
    }
  }

  async pin(cid: string): Promise<boolean> {
    try {
      const response = await fetch(`https://api.pinata.cloud/pinning/pinByHash`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          pinata_api_key: this.apiKey,
          pinata_secret_api_key: this.secretKey,
        },
        body: JSON.stringify({ hashToPin: cid }),
        signal: AbortSignal.timeout(IPFS_PIN_TIMEOUT_MS),
      });

      return response.ok;
    } catch {
      return false;
    }
  }

  async unpin(cid: string): Promise<boolean> {
    try {
      const response = await fetch(`https://api.pinata.cloud/pinning/unpin/${cid}`, {
        method: 'DELETE',
        headers: {
          pinata_api_key: this.apiKey,
          pinata_secret_api_key: this.secretKey,
        },
        signal: AbortSignal.timeout(IPFS_PIN_TIMEOUT_MS),
      });

      return response.ok;
    } catch {
      return false;
    }
  }

  getGatewayUrl(cid: string): string {
    return `${this.gateway}/${cid}`;
  }
}

// =============================================================================
// INFURA PROVIDER
// =============================================================================

class InfuraIPFSProvider implements IPFSProvider {
  name = 'infura';
  private projectId: string;
  private projectSecret: string;
  private gateway: string;

  constructor(projectId: string, projectSecret: string, gateway?: string) {
    this.projectId = projectId;
    this.projectSecret = projectSecret;
    this.gateway = gateway || 'https://ipfs.infura.io/ipfs';
  }

  async upload(data: Buffer, filename: string, mimeType: string): Promise<IPFSUploadResponse> {
    try {
      const formData = new FormData();
      const blob = new Blob([data], { type: mimeType });
      formData.append('file', blob, filename);

      const auth = Buffer.from(`${this.projectId}:${this.projectSecret}`).toString('base64');

      const response = await fetch('https://ipfs.infura.io:5001/api/v0/add', {
        method: 'POST',
        headers: {
          Authorization: `Basic ${auth}`,
        },
        body: formData,
        signal: AbortSignal.timeout(IPFS_UPLOAD_TIMEOUT_MS),
      });

      if (!response.ok) {
        const error = await response.text();
        return { success: false, error: `Infura upload failed: ${error}` };
      }

      const result = await response.json() as { Hash: string; Size: string };

      return {
        success: true,
        cid: result.Hash,
        size: parseInt(result.Size, 10),
        pinned: true,
      };
    } catch (error) {
      return { success: false, error: `Infura upload error: ${(error as Error).message}` };
    }
  }

  async pin(cid: string): Promise<boolean> {
    try {
      const auth = Buffer.from(`${this.projectId}:${this.projectSecret}`).toString('base64');
      const response = await fetch(`https://ipfs.infura.io:5001/api/v0/pin/add?arg=${cid}`, {
        method: 'POST',
        headers: { Authorization: `Basic ${auth}` },
        signal: AbortSignal.timeout(IPFS_PIN_TIMEOUT_MS),
      });
      return response.ok;
    } catch {
      return false;
    }
  }

  async unpin(cid: string): Promise<boolean> {
    try {
      const auth = Buffer.from(`${this.projectId}:${this.projectSecret}`).toString('base64');
      const response = await fetch(`https://ipfs.infura.io:5001/api/v0/pin/rm?arg=${cid}`, {
        method: 'POST',
        headers: { Authorization: `Basic ${auth}` },
        signal: AbortSignal.timeout(IPFS_PIN_TIMEOUT_MS),
      });
      return response.ok;
    } catch {
      return false;
    }
  }

  getGatewayUrl(cid: string): string {
    return `${this.gateway}/${cid}`;
  }
}

// =============================================================================
// WEB3.STORAGE PROVIDER
// =============================================================================

class Web3StorageProvider implements IPFSProvider {
  name = 'web3storage';
  private apiToken: string;

  constructor(apiToken: string) {
    this.apiToken = apiToken;
  }

  async upload(data: Buffer, filename: string, mimeType: string): Promise<IPFSUploadResponse> {
    try {
      const blob = new Blob([data], { type: mimeType });

      const response = await fetch('https://api.web3.storage/upload', {
        method: 'POST',
        headers: {
          Authorization: `Bearer ${this.apiToken}`,
          'X-Name': filename,
        },
        body: blob,
        signal: AbortSignal.timeout(IPFS_UPLOAD_TIMEOUT_MS),
      });

      if (!response.ok) {
        const error = await response.text();
        return { success: false, error: `Web3.Storage upload failed: ${error}` };
      }

      const result = await response.json() as { cid: string };

      return {
        success: true,
        cid: result.cid,
        size: data.length,
        pinned: true,
      };
    } catch (error) {
      return { success: false, error: `Web3.Storage upload error: ${(error as Error).message}` };
    }
  }

  async pin(_cid: string): Promise<boolean> {
    // Web3.Storage pins automatically on upload
    return true;
  }

  async unpin(_cid: string): Promise<boolean> {
    // Web3.Storage does not support unpinning via simple API
    return false;
  }

  getGatewayUrl(cid: string): string {
    return `https://${cid}.ipfs.w3s.link`;
  }
}

// =============================================================================
// MOCK PROVIDER (Development)
// =============================================================================

class MockIPFSProvider implements IPFSProvider {
  name = 'mock';
  private storage = new Map<string, Buffer>();

  async upload(data: Buffer, _filename: string, _mimeType: string): Promise<IPFSUploadResponse> {
    // Generate mock CID
    const crypto = await import('crypto');
    const hash = crypto.createHash('sha256').update(data).digest('hex');
    const cid = `Qm${hash.slice(0, 44)}`;

    this.storage.set(cid, data);

    return {
      success: true,
      cid,
      size: data.length,
      pinned: true,
    };
  }

  async pin(_cid: string): Promise<boolean> {
    return true;
  }

  async unpin(cid: string): Promise<boolean> {
    this.storage.delete(cid);
    return true;
  }

  // KS-118: the mock has no reachable HTTP gateway, so it serves reads from
  // its in-memory store. An unknown cid is a genuine 404 — not a 500.
  async read(cid: string): Promise<Buffer> {
    const data = this.storage.get(cid);
    if (!data) {
      throw new NotFoundError(`IPFS content ${cid}`);
    }
    return data;
  }

  getGatewayUrl(cid: string): string {
    return `https://mock-ipfs.local/${cid}`;
  }

  // For testing
  getData(cid: string): Buffer | undefined {
    return this.storage.get(cid);
  }
}

// =============================================================================
// IPFS SERVICE
// =============================================================================

export class IPFSService {
  private provider: IPFSProvider;

  constructor(
    providerName: 'pinata' | 'infura' | 'web3storage' | 'mock' = 'mock',
    config?: {
      apiKey?: string;
      secretKey?: string;
      gateway?: string;
    }
  ) {
    switch (providerName) {
      case 'pinata':
        if (!config?.apiKey || !config?.secretKey) {
          throw new Error('Pinata requires apiKey and secretKey');
        }
        this.provider = new PinataProvider(config.apiKey, config.secretKey, config.gateway);
        break;

      case 'infura':
        if (!config?.apiKey || !config?.secretKey) {
          logger.warn('Infura requires INFURA_PROJECT_ID and INFURA_PROJECT_SECRET — falling back to mock');
          this.provider = new MockIPFSProvider();
        } else {
          this.provider = new InfuraIPFSProvider(config.apiKey, config.secretKey, config.gateway);
        }
        break;

      case 'web3storage':
        if (!config?.apiKey) {
          logger.warn('Web3.Storage requires WEB3_STORAGE_TOKEN — falling back to mock');
          this.provider = new MockIPFSProvider();
        } else {
          this.provider = new Web3StorageProvider(config.apiKey);
        }
        break;

      case 'mock':
      default:
        this.provider = new MockIPFSProvider();
        break;
    }
  }

  /**
   * Get the current provider name
   */
  getProviderName(): string {
    return this.provider.name;
  }

  /**
   * Upload data to IPFS
   */
  async upload(request: IPFSUploadRequest): Promise<IPFSUploadResponse> {
    return this.provider.upload(request.data, request.filename, request.mimeType);
  }

  /**
   * Upload encrypted document
   */
  async uploadEncrypted(
    encryptedData: Buffer,
    metadata: {
      filename: string;
      originalMimeType: string;
      encryptionMethod: string;
    }
  ): Promise<IPFSUploadResponse> {
    // Create a package with metadata
    const packageData = {
      encrypted: true,
      encryptionMethod: metadata.encryptionMethod,
      originalMimeType: metadata.originalMimeType,
      data: encryptedData.toString('base64'),
    };

    const packageBuffer = Buffer.from(JSON.stringify(packageData));

    return this.provider.upload(
      packageBuffer,
      `${metadata.filename}.encrypted.json`,
      'application/json'
    );
  }

  /**
   * Pin a CID (ensure it stays available)
   */
  async pin(cid: string): Promise<boolean> {
    return this.provider.pin(cid);
  }

  /**
   * Unpin a CID (allow garbage collection)
   */
  async unpin(cid: string): Promise<boolean> {
    return this.provider.unpin(cid);
  }

  /**
   * Get gateway URL for a CID
   */
  getGatewayUrl(cid: string): string {
    return this.provider.getGatewayUrl(cid);
  }

  /**
   * Fetch data from IPFS by CID.
   *
   * Error mapping (KS-118 — so routes return an honest status instead of a
   * blanket 500):
   *   - unknown / not-found cid    → NotFoundError (404)
   *   - gateway unreachable, 5xx, or stalled past the read bound (headers or body) → ServiceUnavailableError (503)
   * Providers with a native read path (the mock) handle this themselves;
   * HTTP-gateway providers are read here via the gateway URL.
   */
  async fetch(cid: string): Promise<Buffer> {
    if (this.provider.read) {
      return this.provider.read(cid);
    }

    const url = this.getGatewayUrl(cid);
    let response: Awaited<ReturnType<typeof fetch>>;
    try {
      response = await fetch(url, { signal: AbortSignal.timeout(IPFS_GATEWAY_READ_TIMEOUT_MS) });
    } catch (error) {
      // DNS / connection failure — the IPFS gateway is unreachable.
      let reason: string;
      try {
        reason = error instanceof Error ? error.message : String(error);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.warn('IPFS gateway unreachable', {
        cid,
        error: reason,
      });
      throw new ServiceUnavailableError('IPFS gateway');
    }

    if (response.status === 404 || response.status === 410) {
      throw new NotFoundError(`IPFS content ${cid}`);
    }

    if (!response.ok) {
      // Any other non-2xx from the gateway (5xx, 502, gateway timeout) is an
      // upstream availability problem — surface it as 503, don't mask it as
      // our own 500.
      logger.warn('IPFS gateway returned non-OK', { cid, status: response.status });
      throw new ServiceUnavailableError('IPFS gateway');
    }

    // The bound covers the body too: a gateway that sends its headers and then stalls (or drops the connection
    // mid-body) rejects here, and that is the same "gateway unavailable" as a failed connect.
    let arrayBuffer: ArrayBuffer;
    try {
      arrayBuffer = await response.arrayBuffer();
    } catch (error) {
      let reason: string;
      try {
        reason = error instanceof Error ? error.message : String(error);
      } catch {
        reason = 'unreadable thrown value';
      }
      logger.warn('IPFS gateway body read failed', {
        cid,
        error: reason,
      });
      throw new ServiceUnavailableError('IPFS gateway');
    }
    return Buffer.from(arrayBuffer);
  }

  /**
   * Fetch and decrypt encrypted document
   */
  async fetchEncrypted(cid: string): Promise<{
    encryptedData: Buffer;
    metadata: {
      encryptionMethod: string;
      originalMimeType: string;
    };
  }> {
    const data = await this.fetch(cid);
    const packageData = JSON.parse(data.toString()) as {
      encrypted: boolean;
      encryptionMethod: string;
      originalMimeType: string;
      data: string;
    };

    if (!packageData.encrypted) {
      throw new Error('Data is not encrypted');
    }

    return {
      encryptedData: Buffer.from(packageData.data, 'base64'),
      metadata: {
        encryptionMethod: packageData.encryptionMethod,
        originalMimeType: packageData.originalMimeType,
      },
    };
  }
}

// =============================================================================
// SINGLETON EXPORT
// =============================================================================

export function createIPFSService(
  provider?: 'pinata' | 'infura' | 'web3storage' | 'mock',
  config?: {
    apiKey?: string;
    secretKey?: string;
    gateway?: string;
  }
): IPFSService {
  return new IPFSService(provider, config);
}

/**
 * Initialise the IPFS service singleton from environment variables.
 * Falls back to mock if no provider credentials are configured.
 *
 * Supported env vars:
 *   IPFS_PROVIDER       — 'pinata' | 'infura' | 'web3storage'
 *   PINATA_API_KEY       — Pinata API key
 *   PINATA_SECRET_KEY    — Pinata secret key
 *   INFURA_PROJECT_ID    — Infura IPFS project ID
 *   INFURA_PROJECT_SECRET — Infura IPFS project secret
 *   WEB3_STORAGE_TOKEN   — Web3.Storage API token
 *   IPFS_GATEWAY         — Custom IPFS gateway URL
 */
function initIPFSFromEnv(): IPFSService {
  const provider = (process.env.IPFS_PROVIDER || 'mock') as 'pinata' | 'infura' | 'web3storage' | 'mock';
  const isProd = process.env.NODE_ENV === 'production';

  // In production, refuse to use mock IPFS provider
  if (isProd && provider === 'mock') {
    throw new Error('Mock IPFS provider cannot be used in production. Set IPFS_PROVIDER to pinata, infura, or web3storage with valid credentials.');
  }

  switch (provider) {
    case 'pinata': {
      const apiKey = process.env.PINATA_API_KEY;
      const secretKey = process.env.PINATA_SECRET_KEY;
      if (apiKey && secretKey) {
        logger.info('Using Pinata provider');
        return new IPFSService('pinata', {
          apiKey,
          secretKey,
          gateway: process.env.IPFS_GATEWAY,
        });
      }
      if (isProd) {
        throw new Error('Pinata credentials (PINATA_API_KEY, PINATA_SECRET_KEY) required in production');
      }
      logger.warn('Pinata credentials missing — falling back to mock');
      return new IPFSService('mock');
    }

    case 'infura': {
      const projectId = process.env.INFURA_PROJECT_ID;
      const projectSecret = process.env.INFURA_PROJECT_SECRET;
      if (projectId && projectSecret) {
        logger.info('Using Infura provider');
        return new IPFSService('infura', {
          apiKey: projectId,
          secretKey: projectSecret,
          gateway: process.env.IPFS_GATEWAY,
        });
      }
      if (isProd) {
        throw new Error('Infura credentials (INFURA_PROJECT_ID, INFURA_PROJECT_SECRET) required in production');
      }
      logger.warn('Infura credentials missing — falling back to mock');
      return new IPFSService('mock');
    }

    case 'web3storage': {
      const token = process.env.WEB3_STORAGE_TOKEN;
      if (token) {
        logger.info('Using Web3.Storage provider');
        return new IPFSService('web3storage', { apiKey: token });
      }
      if (isProd) {
        throw new Error('Web3.Storage token (WEB3_STORAGE_TOKEN) required in production');
      }
      logger.warn('Web3.Storage token missing — falling back to mock');
      return new IPFSService('mock');
    }

    default:
      if (isProd) {
        throw new Error('Mock IPFS provider cannot be used in production. Set IPFS_PROVIDER to pinata, infura, or web3storage with valid credentials.');
      }
      logger.info('Using mock provider');
      return new IPFSService('mock');
  }
}

// Initialise singleton from environment
export const ipfsService = initIPFSFromEnv();
