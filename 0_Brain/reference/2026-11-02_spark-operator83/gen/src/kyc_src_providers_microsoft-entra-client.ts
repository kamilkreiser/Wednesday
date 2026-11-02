/**
 * =============================================================================
 * MICROSOFT ENTRA VERIFIED ID CLIENT
 * =============================================================================
 * Client for Microsoft Entra Verified ID (formerly Azure AD Verifiable Credentials)
 * Handles issuance and verification of credentials with Face Check support
 */

import axios, { AxiosInstance } from 'axios';
import { v4 as uuidv4 } from 'uuid';
import {
  MicrosoftEntraConfig,
  IssuanceRequest,
  IssuanceResponse,
  PresentationRequest,
  PresentationRequestConfig,
  PresentationResponse,
  VerificationSession,
  CallbackPayload,
  VerifiedCredentialData,
  FaceCheckConfig,
  MicrosoftIdvError,
} from '../types/microsoft-idv.types';
import { logger } from '../utils/logger';
import { resolveCallbackApiKey } from '../utils/callbackAuth';

// =============================================================================
// MICROSOFT AUTHENTICATION
// =============================================================================

interface TokenResponse {
  access_token: string;
  token_type: string;
  expires_in: number;
}

// =============================================================================
// MICROSOFT ENTRA VERIFIED ID CLIENT
// =============================================================================

export class MicrosoftEntraClient {
  private config: MicrosoftEntraConfig;
  private httpClient: AxiosInstance;
  private accessToken: string | null = null;
  private tokenExpiresAt: number = 0;

  // Session storage (in production, use Redis or database)
  private sessions = new Map<string, VerificationSession>();
  private sessionsByCallback = new Map<string, string>(); // callbackState -> sessionId

  constructor(config: MicrosoftEntraConfig) {
    this.config = config;
    this.httpClient = axios.create({
      baseURL: 'https://verifiedid.did.msidentity.com/v1.0/verifiableCredentials',
      timeout: 15000,
      headers: {
        'Content-Type': 'application/json',
      },
    });

    logger.info('MicrosoftEntraClient initialized', {
      tenantId: config.tenantId,
      verifierDid: config.verifierDid,
    });
  }

  // ==========================================================================
  // AUTHENTICATION
  // ==========================================================================

  /**
   * Get access token for Microsoft Entra API
   */
  private async getAccessToken(): Promise<string> {
    if (this.accessToken && Date.now() < this.tokenExpiresAt - 60000) {
      return this.accessToken;
    }

    const tokenEndpoint = `https://login.microsoftonline.com/${this.config.tenantId}/oauth2/v2.0/token`;

    const params = new URLSearchParams({
      client_id: this.config.clientId,
      client_secret: this.config.clientSecret,
      scope: '3db474b9-6a0c-4840-96ac-1fceb342124f/.default', // Verified ID scope
      grant_type: 'client_credentials',
    });

    try {
      const response = await axios.post<TokenResponse>(tokenEndpoint, params, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      this.accessToken = response.data.access_token;
      this.tokenExpiresAt = Date.now() + (response.data.expires_in * 1000);

      logger.info('Token acquired');
      return this.accessToken;
    } catch (error: any) {
      logger.error('Token acquisition failed', { 
        error: error.response?.data || (error instanceof Error ? error.message : String(error)) 
      });
      throw new MicrosoftIdvError(
        'TOKEN_ACQUISITION_FAILED',
        'Failed to acquire access token',
        error.response?.data
      );
    }
  }

  /**
   * Make authenticated API request
   */
  private async apiRequest<T>(method: string, endpoint: string, data?: any): Promise<T> {
    const token = await this.getAccessToken();

    try {
      const response = await this.httpClient.request<T>({
        method,
        url: endpoint,
        data,
        headers: {
          Authorization: `Bearer ${token}`,
        },
      });
      return response.data;
    } catch (error: any) {
      logger.error('API request failed', {
        endpoint,
        error: error.response?.data || (error instanceof Error ? error.message : String(error)),
      });
      throw new MicrosoftIdvError(
        error.response?.data?.error?.code || 'API_ERROR',
        error.response?.data?.error?.message || 'API request failed',
        error.response?.data
      );
    }
  }

  // ==========================================================================
  // PRESENTATION (VERIFICATION) REQUESTS
  // ==========================================================================

  /**
   * Create a presentation request for credential verification
   */
  async createPresentationRequest(
    userId: string,
    config: PresentationRequestConfig
  ): Promise<VerificationSession> {
    const sessionId = uuidv4();
    const callbackState = uuidv4();

    const request: PresentationRequest = {
      includeQRCode: true,
      includeReceipt: config.includeReceipt ?? true,
      callback: {
        url: `${this.config.callbackHost}/api/kyc/callback`,
        state: callbackState,
        headers: {
          // KS-488 C-1: one shared resolution with the VERIFIER route, which used to
          // carry a different fallback literal ('secuura-kyc-callback') and no production
          // guard. Same throw-in-production behaviour as before, expressed once.
          'api-key': resolveCallbackApiKey(),
        },
      },
      authority: this.config.verifierDid,
      registration: {
        clientName: this.config.verifierName,
        purpose: config.purpose,
      },
      requestedCredentials: [
        {
          type: config.credentialType,
          purpose: config.purpose,
          acceptedIssuers: config.acceptedIssuers,
          configuration: config.faceCheck ? {
            validation: {
              allowRevoked: false,
              validateLinkedDomain: true,
            },
            constraints: {
              faceCheck: config.faceCheck,
            },
          } : undefined,
        },
      ],
    };

    const response = await this.apiRequest<PresentationResponse>(
      'POST',
      '/createPresentationRequest',
      request
    );

    // Create session
    const session: VerificationSession = {
      id: sessionId,
      userId,
      type: 'presentation',
      status: 'pending',
      requestId: response.requestId,
      requestUrl: response.url,
      qrCode: response.qrCode,
      credentialType: config.credentialType,
      purpose: config.purpose,
      faceCheckRequired: !!config.faceCheck,
      createdAt: new Date(),
      expiresAt: new Date(response.expiry * 1000),
      callbackState,
    };

    // Store session
    this.sessions.set(sessionId, session);
    this.sessionsByCallback.set(callbackState, sessionId);

    logger.info('Presentation request created', {
      sessionId,
      requestId: response.requestId,
      credentialType: config.credentialType,
    });

    return session;
  }

  /**
   * Create a KYC verification request with Face Check
   */
  async createKYCVerificationRequest(
    userId: string,
    level: 'STANDARD' | 'HIGH' | 'GOVERNMENT',
    options?: {
      purpose?: string;
      photoClaimName?: string;
      confidenceThreshold?: number;
    }
  ): Promise<VerificationSession> {
    const faceCheckConfig: FaceCheckConfig | undefined = 
      level === 'HIGH' || level === 'GOVERNMENT'
        ? {
            sourcePhotoClaimName: options?.photoClaimName || 'photo',
            matchConfidenceThreshold: options?.confidenceThreshold || 70,
          }
        : undefined;

    return this.createPresentationRequest(userId, {
      credentialType: 'VerifiedCredentialExpert', // Or custom credential type
      purpose: options?.purpose || `Secuura KYC Verification (Level: ${level})`,
      includeReceipt: true,
      faceCheck: faceCheckConfig,
      callback: {
        url: `${this.config.callbackHost}/api/kyc/callback`,
        state: uuidv4(),
      },
    });
  }

  // ==========================================================================
  // CALLBACK HANDLING
  // ==========================================================================

  /**
   * Process callback from Microsoft Entra Verified ID
   */
  async processCallback(payload: CallbackPayload): Promise<VerificationSession | null> {
    const sessionId = this.sessionsByCallback.get(payload.state);
    if (!sessionId) {
      logger.warn('Unknown callback state', { state: payload.state });
      return null;
    }

    const session = this.sessions.get(sessionId);
    if (!session) {
      logger.warn('Session not found', { sessionId });
      return null;
    }

    logger.info('Processing callback', {
      sessionId,
      requestStatus: payload.requestStatus,
    });

    switch (payload.requestStatus) {
      case 'request_retrieved':
        session.status = 'retrieved';
        break;

      case 'presentation_verified':
        session.status = 'completed';
        session.verifiedCredentials = payload.verifiedCredentialsData;
        session.completedAt = new Date();

        // Extract Face Check result if present
        if (payload.verifiedCredentialsData?.[0]?.faceCheck) {
          session.faceCheckResult = payload.verifiedCredentialsData[0].faceCheck;
        }
        break;

      case 'presentation_error':
      case 'issuance_error':
        session.status = 'failed';
        logger.error('Verification failed', { error: payload.error });
        break;

      case 'issuance_successful':
        session.status = 'completed';
        session.completedAt = new Date();
        break;
    }

    return session;
  }

  // ==========================================================================
  // SESSION MANAGEMENT
  // ==========================================================================

  /**
   * Get session by ID
   */
  getSession(sessionId: string): VerificationSession | undefined {
    return this.sessions.get(sessionId);
  }

  /**
   * Get sessions for user
   */
  getUserSessions(userId: string): VerificationSession[] {
    return Array.from(this.sessions.values()).filter(s => s.userId === userId);
  }

  /**
   * Check session status
   */
  async checkSessionStatus(sessionId: string): Promise<VerificationSession | null> {
    const session = this.sessions.get(sessionId);
    if (!session) return null;

    // Check if expired
    if (new Date() > session.expiresAt && session.status === 'pending') {
      session.status = 'expired';
    }

    return session;
  }

  /**
   * Clean up expired sessions
   */
  cleanupExpiredSessions(): number {
    let cleaned = 0;
    const now = new Date();

    for (const [id, session] of this.sessions.entries()) {
      if (now > session.expiresAt && session.status === 'pending') {
        this.sessions.delete(id);
        this.sessionsByCallback.delete(session.callbackState);
        cleaned++;
      }
    }

    return cleaned;
  }

  // ==========================================================================
  // CREDENTIAL ISSUANCE (for issuing Secuura credentials)
  // ==========================================================================

  /**
   * Create an issuance request for Secuura KYC credential
   */
  async createKYCCredentialIssuance(
    userId: string,
    claims: Record<string, string>,
    options?: {
      pinRequired?: boolean;
      pinLength?: number;
    }
  ): Promise<{ session: VerificationSession; pin?: string }> {
    const sessionId = uuidv4();
    const callbackState = uuidv4();
    // Pen-test F-07 fix: PIN must come from a cryptographically-secure RNG.
    // V8's Math.random() is xorshift128+ — predictable from a few outputs,
    // and an attacker who can race the issuance can shortcut the PIN.
    // crypto.randomInt is the correct source for short numeric secrets.
    const pin = options?.pinRequired
      ? (() => {
          const cryptoMod = require('crypto') as typeof import('crypto');
          const len = options.pinLength || 4;
          return cryptoMod.randomInt(0, 10 ** len).toString().padStart(len, '0');
        })()
      : undefined;

    const request: IssuanceRequest = {
      includeQRCode: true,
      callback: {
        url: `${this.config.callbackHost}/api/kyc/callback`,
        state: callbackState,
        headers: {
          // KS-488 C-1: one shared resolution with the VERIFIER route, which used to
          // carry a different fallback literal ('secuura-kyc-callback') and no production
          // guard. Same throw-in-production behaviour as before, expressed once.
          'api-key': resolveCallbackApiKey(),
        },
      },
      authority: this.config.verifierDid,
      registration: {
        clientName: this.config.verifierName,
      },
      issuance: {
        type: 'SecuuraKYCCredential',
        manifest: this.config.credentialManifestUrl,
        pin: pin ? { value: pin, length: pin.length } : undefined,
        claims,
      },
    };

    const response = await this.apiRequest<IssuanceResponse>(
      'POST',
      '/createIssuanceRequest',
      request
    );

    const session: VerificationSession = {
      id: sessionId,
      userId,
      type: 'issuance',
      status: 'pending',
      requestId: response.requestId,
      requestUrl: response.url,
      qrCode: response.qrCode,
      credentialType: 'SecuuraKYCCredential',
      faceCheckRequired: false,
      createdAt: new Date(),
      expiresAt: new Date(response.expiry * 1000),
      callbackState,
    };

    this.sessions.set(sessionId, session);
    this.sessionsByCallback.set(callbackState, sessionId);

    logger.info('Issuance request created', {
      sessionId,
      requestId: response.requestId,
    });

    return { session, pin };
  }

  // ==========================================================================
  // UTILITIES
  // ==========================================================================

  /**
   * Verify that Face Check passed with sufficient confidence
   */
  validateFaceCheck(
    result: VerifiedCredentialData | undefined,
    requiredThreshold: number = 70
  ): { passed: boolean; confidence?: number; reason?: string } {
    if (!result?.faceCheck) {
      return { passed: false, reason: 'No face check result' };
    }

    if (result.faceCheck.matchConfidence >= requiredThreshold) {
      return { 
        passed: true, 
        confidence: result.faceCheck.matchConfidence,
      };
    }

    return {
      passed: false,
      confidence: result.faceCheck.matchConfidence,
      reason: `Confidence ${result.faceCheck.matchConfidence}% below threshold ${requiredThreshold}%`,
    };
  }

  /**
   * Extract claims from verified credential
   */
  extractClaims(credential: VerifiedCredentialData): Record<string, any> {
    return {
      ...credential.claims,
      ...credential.credentialSubject,
      issuer: credential.issuer,
      issuanceDate: credential.issuanceDate,
      expirationDate: credential.expirationDate,
      credentialTypes: credential.type,
    };
  }
}

// =============================================================================
// FACTORY
// =============================================================================

let clientInstance: MicrosoftEntraClient | null = null;

export function getMicrosoftEntraClient(): MicrosoftEntraClient {
  if (!clientInstance) {
    const config: MicrosoftEntraConfig = {
      tenantId: process.env.ENTRA_TENANT_ID || process.env.AZURE_AD_TENANT_ID || '',
      clientId: process.env.ENTRA_CLIENT_ID || process.env.AZURE_AD_CLIENT_ID || '',
      clientSecret: process.env.ENTRA_CLIENT_SECRET || process.env.AZURE_AD_CLIENT_SECRET || '',
      authority: process.env.ENTRA_VERIFIED_ID_AUTHORITY || '',
      credentialManifestUrl: process.env.ENTRA_CREDENTIAL_MANIFEST_URL || '',
      verifierDid: process.env.ENTRA_VERIFIER_DID || '',
      verifierName: process.env.ENTRA_VERIFIER_NAME || 'Secuura',
      callbackHost: process.env.KYC_CALLBACK_HOST || 'http://localhost:6011',
    };

    if (!config.tenantId || !config.clientId || !config.clientSecret) {
      logger.warn('Entra Verified ID config incomplete — production verification will fail');
    }

    clientInstance = new MicrosoftEntraClient(config);
  }

  return clientInstance;
}

/**
 * Determine whether production Entra Verified ID is properly configured.
 */
export function isEntraConfigured(): boolean {
  return Boolean(
    (process.env.ENTRA_TENANT_ID || process.env.AZURE_AD_TENANT_ID) &&
    (process.env.ENTRA_CLIENT_ID || process.env.AZURE_AD_CLIENT_ID) &&
    (process.env.ENTRA_CLIENT_SECRET || process.env.AZURE_AD_CLIENT_SECRET),
  );
}
