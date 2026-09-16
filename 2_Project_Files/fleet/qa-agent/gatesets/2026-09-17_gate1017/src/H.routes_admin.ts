/**
 * Admin route handlers — extracted from the API gateway monolith.
 *
 * Usage in index.ts:
 *   import { createAdminRoutes } from './routes/admin';
 *   app.use(createAdminRoutes({ authenticateToken, query, redisService, log }));
 */

import { Router, Request, Response, NextFunction, RequestHandler } from 'express';
import { rejectControlBytes } from '@secuura/shared';
import crypto from 'crypto';
import express from 'express';
import { runWithPlatformScope } from '@secuura/shared';

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

interface UserPayload {
  userId: string;
  email: string;
  role: string;
  organizationId?: string;
  verificationLevel: string;
  authMethod?: string;
  mfaEnabled?: boolean;
  tenantId?: string;
  tenantSlug?: string;
}

declare module 'express-serve-static-core' {
  interface Request {
    user?: UserPayload;
    requestId?: string;
  }
}

type QueryFn = (text: string, params?: unknown[]) => Promise<{ rows: any[]; rowCount: number }>;

interface RedisService {
  getAllDocumentTypes(): Promise<object[]>;
  getDocumentType(id: string): Promise<object | null>;
  setDocumentType(id: string, data: object): Promise<void>;
  deleteDocumentType(id: string): Promise<boolean>;

  getAllWorkflows(): Promise<object[]>;
  getWorkflow(id: string): Promise<object | null>;
  setWorkflow(id: string, data: object): Promise<void>;
  deleteWorkflow(id: string): Promise<boolean>;

  getAllIntegrations(): Promise<object[]>;
  getIntegration(id: string): Promise<object | null>;
  setIntegration(id: string, data: object): Promise<void>;
  deleteIntegration(id: string): Promise<boolean>;

  getNotificationSettings(key: string): Promise<object | null>;
  setNotificationSettings(key: string, data: object): Promise<void>;

  getPrivacySettings(key: string): Promise<object | null>;
  setPrivacySettings(key: string, data: object): Promise<void>;

  getAllVerificationPolicies(): Promise<object[]>;
  getVerificationPolicy(id: string): Promise<object | null>;
  setVerificationPolicy(id: string, data: object): Promise<void>;
  deleteVerificationPolicy(id: string): Promise<boolean>;
}

export interface AdminRouteDeps {
  authenticateToken: (required?: boolean) => RequestHandler;
  query: QueryFn;
  redisService: RedisService;
  log: (level: 'info' | 'warn' | 'error', message: string, meta?: object) => void;
  /** RS256 token verifier (the gateway's verifyRs256) — verifies admin tokens with the JWKS/public key; async (KS-347) since it may fetch a rotated key from auth's JWKS */
  verifyToken?: (token: string) => unknown | Promise<unknown>;
  /** parseTestToken from the main module — enables dev/test token flow */
  parseTestToken?: (token: string) => UserPayload | null;
  /** Whether DB (PostgreSQL) is currently reachable */
  isDbAvailable?: () => boolean;
  /** Service URL map (used to proxy PATCH /api/users/admin/:id to auth service) */
  services?: Record<string, { url: string; [k: string]: unknown }>;
}

// ---------------------------------------------------------------------------
// Seed data constants
// ---------------------------------------------------------------------------

export const SEED_DOCUMENT_TYPES = [
  {
    id: 'dt-seed-1',
    name: 'University Degree',
    code: 'DEGREE',
    description: 'Academic degrees from accredited universities',
    category: 'Education',
    isActive: true,
    status: 'active',
    creatorVerificationLevel: 'enhanced',
    ownerVerificationLevel: 'basic',
    viewerVerificationLevel: 'none',
    verifierVerificationLevel: 'standard',
    requireMFA: true,
    requireWalletSignature: true,
    requireKYC: false,
    allowedAuthProviders: ['entra', 'auth0'],
    requiresApproval: true,
    approvalWorkflowId: 'wf-1',
    autoAnchor: true,
    anchorNetwork: 'preprod',
    metadataSchema: [
      { name: 'studentId', type: 'string', required: true },
      { name: 'graduationDate', type: 'date', required: true },
      { name: 'classification', type: 'select', required: true, options: ['First Class', 'Upper Second', 'Lower Second', 'Third'] },
    ],
    allowedSources: ['sharepoint', 'manual'],
    webhookEvents: ['certified', 'verified', 'transferred'],
    documentCount: 1247,
    createdAt: '2024-01-15T00:00:00.000Z',
    updatedAt: '2024-01-20T00:00:00.000Z',
  },
  {
    id: 'dt-seed-2',
    name: 'Professional License',
    code: 'LICENSE',
    description: 'Professional licenses from regulatory bodies',
    category: 'Professional',
    isActive: true,
    status: 'active',
    creatorVerificationLevel: 'high',
    ownerVerificationLevel: 'standard',
    viewerVerificationLevel: 'basic',
    verifierVerificationLevel: 'enhanced',
    requireMFA: true,
    requireWalletSignature: true,
    requireKYC: true,
    allowedAuthProviders: ['entra', 'auth0', 'okta'],
    requiresApproval: true,
    approvalWorkflowId: 'wf-2',
    autoAnchor: true,
    anchorNetwork: 'mainnet',
    metadataSchema: [
      { name: 'licenseNumber', type: 'string', required: true },
      { name: 'issueDate', type: 'date', required: true },
      { name: 'expiryDate', type: 'date', required: true },
      { name: 'jurisdiction', type: 'string', required: true },
    ],
    allowedSources: ['api', 'manual'],
    webhookEvents: ['certified', 'verified', 'expired', 'revoked'],
    documentCount: 892,
    createdAt: '2024-02-10T00:00:00.000Z',
    updatedAt: '2024-03-15T00:00:00.000Z',
  },
  {
    id: 'dt-seed-3',
    name: 'Employment Reference',
    code: 'REFERENCE',
    description: 'Employment references and testimonials',
    category: 'Employment',
    isActive: true,
    status: 'active',
    creatorVerificationLevel: 'standard',
    ownerVerificationLevel: 'basic',
    viewerVerificationLevel: 'none',
    verifierVerificationLevel: 'basic',
    requireMFA: false,
    requireWalletSignature: false,
    requireKYC: false,
    allowedAuthProviders: ['entra', 'auth0'],
    requiresApproval: false,
    approvalWorkflowId: null,
    autoAnchor: false,
    anchorNetwork: 'preprod',
    metadataSchema: [
      { name: 'employeeId', type: 'string', required: false },
      { name: 'employmentStart', type: 'date', required: true },
      { name: 'employmentEnd', type: 'date', required: false },
      { name: 'position', type: 'string', required: true },
    ],
    allowedSources: ['sharepoint', 'manual', 'email'],
    webhookEvents: ['certified', 'verified'],
    documentCount: 2156,
    createdAt: '2024-01-05T00:00:00.000Z',
    updatedAt: '2024-01-28T00:00:00.000Z',
  },
  {
    id: 'dt-seed-4',
    name: 'Academic Transcript',
    code: 'TRANSCRIPT',
    description: 'Academic transcripts and records of achievement from educational institutions',
    category: 'Education',
    isActive: true,
    status: 'active',
    creatorVerificationLevel: 'enhanced',
    ownerVerificationLevel: 'basic',
    viewerVerificationLevel: 'none',
    verifierVerificationLevel: 'standard',
    requireMFA: true,
    requireWalletSignature: true,
    requireKYC: false,
    allowedAuthProviders: ['entra', 'auth0'],
    requiresApproval: true,
    approvalWorkflowId: 'wf-4',
    autoAnchor: true,
    anchorNetwork: 'preprod',
    metadataSchema: [
      { name: 'studentId', type: 'string', required: true },
      { name: 'institution', type: 'string', required: true },
      { name: 'programme', type: 'string', required: true },
      { name: 'graduationDate', type: 'date', required: true },
      { name: 'classification', type: 'select', required: true, options: ['First Class', 'Upper Second', 'Lower Second', 'Third', 'Pass', 'Distinction', 'Merit'] },
      { name: 'gpa', type: 'string', required: false },
    ],
    allowedSources: ['api', 'sharepoint', 'manual'],
    webhookEvents: ['certified', 'verified', 'shared', 'recertified', 'transferred'],
    documentCount: 834,
    createdAt: '2024-03-01T00:00:00.000Z',
    updatedAt: '2024-03-20T00:00:00.000Z',
  },
  {
    id: 'dt-seed-5',
    name: 'Verification Certificate',
    code: 'VCERT',
    description: 'Secondary credential issued by a Verifier attesting they have verified an original certification. Enables the Verifier to Certifier role transition.',
    category: 'Verification',
    isActive: true,
    status: 'active',
    creatorVerificationLevel: 'standard',
    ownerVerificationLevel: 'basic',
    viewerVerificationLevel: 'none',
    verifierVerificationLevel: 'basic',
    requireMFA: true,
    requireWalletSignature: true,
    requireKYC: false,
    allowedAuthProviders: ['entra', 'auth0', 'okta'],
    requiresApproval: false,
    approvalWorkflowId: null,
    autoAnchor: true,
    anchorNetwork: 'preprod',
    metadataSchema: [
      { name: 'originalCertificationId', type: 'string', required: true },
      { name: 'originalIssuer', type: 'string', required: true },
      { name: 'verificationDate', type: 'date', required: true },
      { name: 'verificationMethod', type: 'select', required: true, options: ['Automated', 'Manual Review', 'Hybrid'] },
      { name: 'verifierNote', type: 'string', required: false },
    ],
    allowedSources: ['api'],
    webhookEvents: ['certified', 'shared', 'distributed'],
    documentCount: 421,
    createdAt: '2024-03-15T00:00:00.000Z',
    updatedAt: '2024-04-01T00:00:00.000Z',
  },
  {
    id: 'dt-seed-6',
    name: 'Recommendation Letter',
    code: 'RECOMMENDATION',
    description: 'Professional or academic recommendation letters for recruitment purposes',
    category: 'Recruitment',
    isActive: true,
    status: 'active',
    creatorVerificationLevel: 'standard',
    ownerVerificationLevel: 'basic',
    viewerVerificationLevel: 'none',
    verifierVerificationLevel: 'basic',
    requireMFA: false,
    requireWalletSignature: false,
    requireKYC: false,
    allowedAuthProviders: ['entra', 'auth0'],
    requiresApproval: false,
    approvalWorkflowId: null,
    autoAnchor: false,
    anchorNetwork: 'preprod',
    metadataSchema: [
      { name: 'candidateName', type: 'string', required: true },
      { name: 'recommenderName', type: 'string', required: true },
      { name: 'recommenderTitle', type: 'string', required: true },
      { name: 'relationship', type: 'select', required: true, options: ['Academic Supervisor', 'Line Manager', 'Colleague', 'Client'] },
      { name: 'dateWritten', type: 'date', required: true },
    ],
    allowedSources: ['manual', 'email'],
    webhookEvents: ['certified', 'verified', 'shared'],
    documentCount: 567,
    createdAt: '2024-02-20T00:00:00.000Z',
    updatedAt: '2024-03-10T00:00:00.000Z',
  },
  // KS-388: with the catalogue registered, enforceDocumentTypeRules now 400s an
  // unknown documentType — so the two contract-critical types must be IN the seed.
  // Both are deliberately friction-free (no verification levels / MFA / approval):
  // SSD_DOCUMENT arrives from Platform-S connector calls, DOCUMENT is originate's
  // fallback for typeless creations; gating either would break those paths.
  {
    id: 'dt-seed-7',
    name: 'SSD Document',
    code: 'SSD_DOCUMENT',
    description: 'Document originated by Platform-S (Secuura Secure Distribution) — the fixed documentType S sends on POST /api/documents',
    category: 'Integration',
    isActive: true,
    status: 'active',
    creatorVerificationLevel: 'none',
    ownerVerificationLevel: 'none',
    viewerVerificationLevel: 'none',
    verifierVerificationLevel: 'none',
    requireMFA: false,
    requireWalletSignature: false,
    requireKYC: false,
    allowedAuthProviders: [],
    requiresApproval: false,
    approvalWorkflowId: null,
    autoAnchor: true,
    anchorNetwork: 'preprod',
    metadataSchema: [],
    allowedSources: ['api'],
    webhookEvents: ['certified', 'verified'],
    documentCount: 0,
    createdAt: '2026-07-08T00:00:00.000Z',
    updatedAt: '2026-07-08T00:00:00.000Z',
  },
  {
    id: 'dt-seed-8',
    name: 'Generic Document',
    code: 'DOCUMENT',
    description: 'General document with no specialised type — the default when a creation request names no documentType',
    category: 'General',
    isActive: true,
    status: 'active',
    creatorVerificationLevel: 'none',
    ownerVerificationLevel: 'none',
    viewerVerificationLevel: 'none',
    verifierVerificationLevel: 'none',
    requireMFA: false,
    requireWalletSignature: false,
    requireKYC: false,
    allowedAuthProviders: [],
    requiresApproval: false,
    approvalWorkflowId: null,
    autoAnchor: false,
    anchorNetwork: 'preprod',
    metadataSchema: [],
    allowedSources: ['manual', 'api'],
    webhookEvents: ['certified', 'verified'],
    documentCount: 0,
    createdAt: '2026-07-08T00:00:00.000Z',
    updatedAt: '2026-07-08T00:00:00.000Z',
  },
  {
    // KS-466 §7: the published spec's own DocumentCreateRequest example uses
    // documentType PROPERTY_DEED (the property-deed narrative also runs
    // through the Document + anchoring examples), but the type was never in
    // this catalogue — so copy-pasting the example from the spec earned a
    // 400 UNKNOWN_DOCUMENT_TYPE on any seeded env. Registered permissive
    // (DOCUMENT-shaped): the example must work unauthenticated-simple, and
    // admins can tighten it per env via the catalogue CRUD.
    id: 'dt-seed-9',
    name: 'Property Deed',
    code: 'PROPERTY_DEED',
    description: 'Property title deeds and land-registry documents',
    category: 'Property',
    isActive: true,
    status: 'active',
    creatorVerificationLevel: 'none',
    ownerVerificationLevel: 'none',
    viewerVerificationLevel: 'none',
    verifierVerificationLevel: 'none',
    requireMFA: false,
    requireWalletSignature: false,
    requireKYC: false,
    allowedAuthProviders: [],
    requiresApproval: false,
    approvalWorkflowId: null,
    autoAnchor: false,
    anchorNetwork: 'preprod',
    metadataSchema: [],
    allowedSources: ['manual', 'api'],
    webhookEvents: ['certified', 'verified'],
    documentCount: 0,
    createdAt: '2026-07-19T00:00:00.000Z',
    updatedAt: '2026-07-19T00:00:00.000Z',
  },
];

export const SEED_INTEGRATIONS = [
  {
    id: 'integ-seed-1',
    name: 'SharePoint \u2014 Document Source',
    integrationType: 'source',
    provider: 'microsoft',
    status: 'disconnected',
    isActive: false,
    lastSyncAt: null,
    config: { tenantId: '', clientId: '', clientSecret: '', siteUrl: '' },
    documentTypes: ['DEGREE', 'TRANSCRIPT'],
    errorMessage: null,
    createdAt: '2024-01-15T00:00:00.000Z',
    updatedAt: '2024-01-15T00:00:00.000Z',
  },
  {
    id: 'integ-seed-2',
    name: 'Microsoft Entra ID',
    integrationType: 'identity',
    provider: 'entra',
    status: 'disconnected',
    isActive: false,
    lastSyncAt: null,
    config: { tenantId: '', clientId: '', clientSecret: '', redirectUri: '' },
    documentTypes: [],
    errorMessage: null,
    createdAt: '2024-01-20T00:00:00.000Z',
    updatedAt: '2024-01-20T00:00:00.000Z',
  },
  // integ-seed-3 (Onfido KYC) retired 2026-04-29 — see CONNECTORS.md.
  // The platform's KYC path is Microsoft Entra Verified ID; the alt
  // providers (Onfido / Jumio / Sumsub) were never wired up.
  {
    id: 'integ-seed-4',
    name: 'Cardano Preprod (Blockfrost)',
    integrationType: 'blockchain',
    provider: 'blockfrost',
    status: 'connected',
    isActive: true,
    lastSyncAt: new Date().toISOString(),
    config: { network: 'preprod', projectId: 'preprodXXXXXXXXXXXXXXXXXXXXXXXXXXXX' },
    documentTypes: [],
    errorMessage: null,
    createdAt: '2024-01-10T00:00:00.000Z',
    updatedAt: new Date().toISOString(),
  },
  {
    id: 'integ-seed-5',
    name: 'AWS S3 \u2014 Document Archive',
    integrationType: 'source',
    provider: 'aws',
    status: 'disconnected',
    isActive: false,
    lastSyncAt: null,
    config: { bucket: '', region: 'eu-west-1', accessKeyId: '', secretAccessKey: '' },
    documentTypes: ['CERTIFICATE', 'LICENSE'],
    errorMessage: null,
    createdAt: '2024-02-10T00:00:00.000Z',
    updatedAt: '2024-02-10T00:00:00.000Z',
  },
  {
    id: 'integ-seed-6',
    name: 'Microsoft Outlook \u2014 Verify from Email',
    integrationType: 'addin',
    provider: 'outlook',
    status: 'disconnected',
    isActive: false,
    lastSyncAt: null,
    config: { tenantId: '', clientId: '', redirectUri: 'https://localhost:6104/auth/callback', manifestUrl: '/outlook-addin/manifest.xml', ssoEnabled: false },
    documentTypes: [],
    errorMessage: null,
    createdAt: '2024-03-01T00:00:00.000Z',
    updatedAt: '2024-03-01T00:00:00.000Z',
  },
];

export const SEED_IDENTITY_ORGS = [
  { id: 'b0000000-0000-4000-8000-000000000001', name: 'Secuura Ltd', slug: 'secuura', type: 'ENTERPRISE', status: 'active', verified: true, metadata: { domain: 'secuura.io', domain_verified: true, trust_level: 'KYC_VERIFIED', verification_mode: 'HYBRID', region: 'EU' } },
  { id: 'b0000000-0000-4000-8000-000000000002', name: 'Acme University', slug: 'acme-uni', type: 'UNIVERSITY', status: 'active', verified: true, metadata: { domain: 'acme-university.edu', domain_verified: true, trust_level: 'DOCUMENT_VERIFIED', verification_mode: 'MANUAL_REVIEW', region: 'UK' } },
  { id: 'b0000000-0000-4000-8000-000000000003', name: 'Global Verify Inc', slug: 'global-verify', type: 'PROFESSIONAL_BODY', status: 'active', verified: false, metadata: { domain: 'globalverify.com', domain_verified: false, trust_level: 'UNVERIFIED', verification_mode: 'DOMAIN_ONLY', region: 'US' } },
];

export const SEED_IDENTITY_USERS = [
  { email: 'alice@secuura.io', display_name: 'Alice Johnson', role: 'issuer_admin', verification_level: 'STANDARD', auth_method: 'email', mfa_enabled: true, wallet_address: 'addr1q9example1', external_provider: 'google', organization_id: 'b0000000-0000-4000-8000-000000000001', metadata: { region: 'EU', social_providers: ['google', 'linkedin'] } },
  { email: 'bob@acme-university.edu', display_name: 'Prof. Bob Williams', role: 'issuer_approver', verification_level: 'SOCIAL', auth_method: 'google', mfa_enabled: false, wallet_address: null, external_provider: 'google', organization_id: 'b0000000-0000-4000-8000-000000000002', metadata: { region: 'UK', social_providers: ['google'] } },
  { email: 'carol@globalverify.com', display_name: 'Carol Davis', role: 'verifier', verification_level: 'BASIC', auth_method: 'email', mfa_enabled: false, wallet_address: null, external_provider: null, organization_id: 'b0000000-0000-4000-8000-000000000003', metadata: { region: 'US', social_providers: [] } },
  { email: 'dave@example.com', display_name: 'Dave Miller', role: 'owner', verification_level: 'SOCIAL', auth_method: 'github', mfa_enabled: false, wallet_address: 'addr1q9example2', external_provider: 'github', organization_id: null, metadata: { region: 'EU', social_providers: ['github'] } },
  { email: 'eve@secuura.io', display_name: 'Eve Chen', role: 'system_admin', verification_level: 'STANDARD', auth_method: 'email', mfa_enabled: true, wallet_address: 'addr1q9example3', external_provider: null, organization_id: 'b0000000-0000-4000-8000-000000000001', metadata: { region: 'EU', social_providers: ['google', 'github', 'linkedin'] } },
];

export const SEED_POLICIES = [
  { id: 'vpol-001', name: 'Document Creation \u2013 Standard', description: 'Require BASIC identity for all document creation actions', scope: 'action', scopeId: 'document.create', minUserLevel: 'BASIC', minOrgLevel: 'UNVERIFIED', enforcementMode: 'block', requiredMfa: false, requiredWallet: false, isActive: true, createdAt: new Date().toISOString() },
  { id: 'vpol-002', name: 'High-Value Transfers', description: 'Require HIGH identity and MFA for document transfers', scope: 'action', scopeId: 'document.transfer', minUserLevel: 'HIGH', minOrgLevel: 'KYC_VERIFIED', enforcementMode: 'block', requiredMfa: true, requiredWallet: true, isActive: true, createdAt: new Date().toISOString() },
  { id: 'vpol-003', name: 'Government Documents', description: 'Government-level verification for government document types', scope: 'document_type', scopeId: 'GOV', minUserLevel: 'GOVERNMENT', minOrgLevel: 'GOVERNMENT_VERIFIED', enforcementMode: 'block', requiredMfa: true, requiredWallet: false, isActive: true, createdAt: new Date().toISOString() },
];

// ---------------------------------------------------------------------------
// Required config fields — used by integration test-connection endpoint
// ---------------------------------------------------------------------------

const REQUIRED_CONFIG_FIELDS: Record<string, Record<string, string[]>> = {
  source: {
    microsoft: ['tenantId', 'clientId', 'clientSecret', 'siteUrl'],
    aws: ['bucket', 'region', 'accessKeyId', 'secretAccessKey'],
    azure: ['storageAccount', 'containerName'],
    onedrive: ['tenantId', 'clientId', 'clientSecret'],
    gcs: ['projectId', 'bucketName', 'serviceAccountKey'],
    dropbox: ['accessToken'],
  },
  identity: {
    entra: ['tenantId', 'clientId', 'clientSecret', 'redirectUri'],
    auth0: ['domain', 'clientId', 'clientSecret', 'redirectUri'],
    okta: ['orgUrl', 'clientId', 'clientSecret', 'redirectUri'],
    google: ['clientId', 'clientSecret', 'redirectUri'],
    saml: ['metadataUrl', 'entityId'],
    oidc: ['issuerUrl', 'clientId', 'clientSecret'],
  },
  verification: {
    // Onfido / Jumio / Sumsub retired 2026-04-29 — see CONNECTORS.md.
    veriff: ['apiKey', 'sessionUrl'],
    govuk: ['apiKey', 'serviceId'],
    mygovid: ['apiKey', 'agencyId'],
  },
  blockchain: {
    blockfrost: ['projectId'],
    ogmios: ['host'],
    koios: [],
  },
  social: {
    google: ['clientId', 'clientSecret'],
    linkedin: ['clientId', 'clientSecret'],
    facebook: ['appId', 'appSecret'],
    apple: ['serviceId', 'teamId', 'keyId', 'privateKey'],
    github: ['clientId', 'clientSecret'],
    microsoft_personal: ['clientId', 'clientSecret'],
  },
  addin: {
    outlook: ['tenantId', 'clientId'],
  },
};

// ---------------------------------------------------------------------------
// Factory
// ---------------------------------------------------------------------------

export function createAdminRoutes(deps: AdminRouteDeps): Router {
  const {
    authenticateToken,
    query,
    redisService,
    log,
    verifyToken,
    parseTestToken,
    isDbAvailable = () => false,
    services = {},
  } = deps;

  const router = Router();
  // KS-815 (same class as the verification router) — GUARD THE BODY THIS
  // ROUTER PARSES ITSELF.
  //
  // This router is mounted at `index.ts:856`, after the global control-byte
  // guard at :422, and it parses with its own `express.json()`. For any route
  // whose prefix is on `proxyPaths` the global parser was skipped, so the
  // global guard saw an unset body and no-oped — and then this parser ran.
  //
  // SEVENTEEN of the NINETEEN routes below are on such a prefix: thirteen
  // `/api/admin/*` routes (`/api/admin` is on the list) and four
  // `/api/users/admin/*` routes (`/api/users` is on it). The two that are not
  // are `/api/settings/notifications` and `/api/privacy/settings`, which the
  // global pair already covers; they are now covered twice, which is a no-op
  // and deliberate — their outer coverage is an accident of prefix membership
  // and a future addition to `proxyPaths` would silently remove it.
  //
  // Measured, not inferred from the skip list: a NUL in
  // POST /api/admin/document-types reached the handler over a real socket
  // against this router before this change.
  const controlByteGuard = rejectControlBytes();
  const rawBodyParser = express.json({ limit: '1mb' });
  const mockBodyParser: RequestHandler = (req, res, next) => {
    rawBodyParser(req, res, (err?: unknown) => {
      if (err) { next(err as Error); return; }
      controlByteGuard(req, res, next);
    });
  };

  const NODE_ENV = process.env.NODE_ENV || 'development';
  const enableDemoSeed = process.env.ENABLE_DEMO_SEED === 'true' || !['production', 'staging'].includes(NODE_ENV);

  // =========================================================================
  // requireAdmin middleware
  // =========================================================================

  const ADMIN_ROLES = ['SYSTEM_ADMIN', 'system_admin', 'super_admin', 'SUPER_ADMIN', 'platform_admin', 'ORG_ADMIN', 'ISSUER_ADMIN', 'issuer_admin'];

  // KS-458: fail-closed RLS. Platform-level admins legitimately read across
  // tenants (dashboards/seeds), so their queries run under the reviewed
  // platform scope; ORG_ADMIN / ISSUER_ADMIN keep the tenant-scoped view the
  // policy now enforces (their request ALS context applies).
  const PLATFORM_SCOPE_ROLES = ['SYSTEM_ADMIN', 'system_admin', 'super_admin', 'SUPER_ADMIN', 'platform_admin'];
  const adminScope = <T,>(req: Request, fn: () => Promise<T>): Promise<T> =>
    PLATFORM_SCOPE_ROLES.includes(((req as any).user?.role as string) || '')
      ? runWithPlatformScope(fn)
      : fn();

  const requireAdmin = async (req: Request, res: Response, next: NextFunction) => {
    const authHeader = req.headers.authorization;
    if (!authHeader || !authHeader.startsWith('Bearer ')) {
      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Authentication required' } });
      return;
    }

    const token = authHeader.split(' ')[1];

    if (parseTestToken) {
      const testPayload = parseTestToken(token);
      if (testPayload) {
        if (!ADMIN_ROLES.includes(testPayload.role)) {
          res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Admin access required' } });
          return;
        }
        req.user = testPayload;
        next();
        return;
      }
    }

    try {
      // KS-302/KS-184: admin tokens are verified RS256-only (previously HS256 with the
      // now-removed symmetric secret). Uses the gateway's injected RS256 verifier (public key);
      // fails closed (caught below → 401) if no verifier was wired.
      if (!verifyToken) throw new Error('No RS256 token verifier configured');
      // KS-347: verifyToken (the gateway's verifyRs256) is async — it may fetch
      // the verification key from auth's JWKS to pick up a rotated signing key.
      const decoded = (await verifyToken(token)) as UserPayload;
      if (!ADMIN_ROLES.includes(decoded.role)) {
        res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Admin access required' } });
        return;
      }
      req.user = decoded;
      next();
    } catch {
      res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'Invalid token' } });
    }
  };

  // =========================================================================
  // Document Types CRUD (Redis-backed)
  // =========================================================================

  async function seedDocumentTypesIfEmpty(): Promise<object[]> {
    const existing = await redisService.getAllDocumentTypes();
    if (existing.length > 0) return existing;
    if (!enableDemoSeed) return [];
    for (const dt of SEED_DOCUMENT_TYPES) {
      await redisService.setDocumentType(dt.id, dt);
    }
    return SEED_DOCUMENT_TYPES;
  }

  router.get('/api/admin/document-types', requireAdmin, async (_req: Request, res: Response) => {
    try {
      const types = await seedDocumentTypesIfEmpty();
      res.json(types);
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch document types' } });
    }
  });

  router.get('/api/admin/document-types/:id', requireAdmin, async (req: Request, res: Response) => {
    try {
      const dt = await redisService.getDocumentType(req.params.id);
      if (!dt) {
        res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document type not found' } });
        return;
      }
      res.json(dt);
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch document type' } });
    }
  });

  router.get('/api/admin/document-types/:id/documents', requireAdmin, async (req: Request, res: Response) => {
    const dt = await redisService.getDocumentType(req.params.id);
    if (!dt) {
      res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document type not found' } });
      return;
    }
    const dtObj = dt as any;
    const mockDocs = Array.from({ length: Math.min(dtObj.documentCount || 5, 10) }, (_, i) => ({
      id: `doc-${req.params.id}-${i + 1}`,
      title: `${dtObj.name} #${i + 1}`,
      status: ['certified', 'pending', 'verified', 'draft'][i % 4],
      owner: `user-${1000 + i}`,
      ownerName: ['Alice Johnson', 'Bob Smith', 'Charlie Brown', 'Diana Ross', 'Eve Williams'][i % 5],
      createdAt: new Date(Date.now() - i * 86400000 * 7).toISOString(),
      updatedAt: new Date(Date.now() - i * 86400000 * 2).toISOString(),
    }));
    res.json({ success: true, documents: mockDocs, total: dtObj.documentCount || mockDocs.length });
  });

  router.post('/api/admin/document-types', mockBodyParser, requireAdmin, async (req: Request, res: Response) => {
    try {
      const body = req.body || {};
      const id = `dt-${Date.now()}`;
      const now = new Date().toISOString();
      const docType = {
        id,
        ...body,
        documentCount: body.documentCount || 0,
        createdAt: now,
        updatedAt: now,
      };
      await redisService.setDocumentType(id, docType);
      res.status(201).json(docType);
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create document type' } });
    }
  });

  router.put('/api/admin/document-types/:id', mockBodyParser, requireAdmin, async (req: Request, res: Response) => {
    try {
      const existing = await redisService.getDocumentType(req.params.id);
      if (!existing) {
        res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document type not found' } });
        return;
      }
      const updated = { ...(existing as any), ...req.body, id: req.params.id, updatedAt: new Date().toISOString() };
      await redisService.setDocumentType(req.params.id, updated);
      res.json(updated);
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update document type' } });
    }
  });

  router.patch('/api/admin/document-types/:id/status', mockBodyParser, requireAdmin, async (req: Request, res: Response) => {
    try {
      const existing = await redisService.getDocumentType(req.params.id);
      if (!existing) {
        res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document type not found' } });
        return;
      }
      const { status } = req.body || {};
      const validStatuses = ['active', 'inactive', 'archived'];
      if (!validStatuses.includes(status)) {
        res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `Invalid status. Must be one of: ${validStatuses.join(', ')}` } });
        return;
      }
      const updated = {
        ...(existing as any),
        isActive: status === 'active',
        status,
        updatedAt: new Date().toISOString(),
      };
      await redisService.setDocumentType(req.params.id, updated);
      res.json(updated);
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update document type status' } });
    }
  });

  router.delete('/api/admin/document-types/:id', requireAdmin, async (req: Request, res: Response) => {
    try {
      const deleted = await redisService.deleteDocumentType(req.params.id);
      if (!deleted) {
        res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Document type not found' } });
        return;
      }
      res.json({ success: true });
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to delete document type' } });
    }
  });

  // =========================================================================
  // Workflow CRUD
  // =========================================================================

  router.get('/api/admin/workflows', requireAdmin, async (_req: Request, res: Response) => {
    try {
      const workflows = await redisService.getAllWorkflows();
      res.json(workflows);
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch workflows' } });
    }
  });

  router.post('/api/admin/workflows', mockBodyParser, requireAdmin, async (req: Request, res: Response) => {
    try {
      const body = req.body || {};
      const id = `wf-${Date.now()}`;
      const now = new Date().toISOString();

      const workflow = {
        id,
        name: body.name || 'Unnamed Workflow',
        description: body.description || '',
        type: body.type || 'sequential',
        isActive: body.isActive !== false,
        slaHours: body.slaHours || 24,
        steps: Array.isArray(body.steps) ? body.steps : [],
        documentTypes: Array.isArray(body.documentTypes) ? body.documentTypes : [],
        usageCount: 0,
        createdAt: now,
        updatedAt: now,
      };
      await redisService.setWorkflow(id, workflow);
      res.status(201).json(workflow);
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create workflow' } });
    }
  });

  router.put('/api/admin/workflows/:id', mockBodyParser, requireAdmin, async (req: Request, res: Response) => {
    try {
      const existing = await redisService.getWorkflow(req.params.id);
      if (!existing) {
        res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Workflow not found' } });
        return;
      }
      const updated = { ...(existing as any), ...req.body, id: req.params.id, updatedAt: new Date().toISOString() };
      await redisService.setWorkflow(req.params.id, updated);
      res.json(updated);
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update workflow' } });
    }
  });

  router.delete('/api/admin/workflows/:id', requireAdmin, async (req: Request, res: Response) => {
    try {
      const deleted = await redisService.deleteWorkflow(req.params.id);
      if (!deleted) {
        res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Workflow not found' } });
        return;
      }
      res.json({ success: true });
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to delete workflow' } });
    }
  });

  // =========================================================================
  // Integration CRUD (Redis-backed with seeding)
  // =========================================================================

  async function seedIntegrationsIfEmpty(): Promise<object[]> {
    const existing = await redisService.getAllIntegrations() as Array<Record<string, unknown>>;
    // KS-15: reconcile against the current seed set rather than just
    // seeding-if-empty. The old behaviour ("if existing.length > 0 return
    // existing") meant Redis kept whatever was seeded the FIRST time —
    // including the retired Onfido row (`int_onfido` / `provider: 'onfido'`)
    // that's no longer in SEED_INTEGRATIONS. Drop any row whose id isn't in
    // the current seed AND whose provider was a retired one. (We don't blow
    // away user-added integrations — only the known-retired seeded ones.)
    const RETIRED_PROVIDERS = new Set(['onfido']);
    const seedIds = new Set(SEED_INTEGRATIONS.map((s) => s.id));
    for (const row of existing) {
      const id = row.id as string | undefined;
      const provider = (row.provider as string | undefined)?.toLowerCase();
      if (id && !seedIds.has(id) && provider && RETIRED_PROVIDERS.has(provider)) {
        await redisService.deleteIntegration(id);
      }
    }

    const afterPrune = await redisService.getAllIntegrations() as Array<Record<string, unknown>>;
    if (afterPrune.length > 0) return afterPrune;
    if (!enableDemoSeed) return [];
    for (const integ of SEED_INTEGRATIONS) {
      await redisService.setIntegration(integ.id, integ);
    }
    return SEED_INTEGRATIONS;
  }

  router.get('/api/admin/integrations', requireAdmin, async (_req: Request, res: Response) => {
    try {
      const integrations = await seedIntegrationsIfEmpty();
      res.json(integrations);
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch integrations' } });
    }
  });

  router.get('/api/admin/integrations/:id', requireAdmin, async (req: Request, res: Response) => {
    try {
      const integ = await redisService.getIntegration(req.params.id);
      if (!integ) {
        res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Integration not found' } });
        return;
      }
      res.json(integ);
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch integration' } });
    }
  });

  router.post('/api/admin/integrations', mockBodyParser, requireAdmin, async (req: Request, res: Response) => {
    try {
      const body = req.body || {};
      const id = `integ-${Date.now()}`;
      const now = new Date().toISOString();

      const integration = {
        id,
        name: body.name || 'Unnamed Integration',
        integrationType: body.integrationType || 'source',
        provider: body.provider || '',
        status: body.status || 'disconnected',
        isActive: body.isActive !== false,
        lastSyncAt: null,
        config: body.config || {},
        documentTypes: Array.isArray(body.documentTypes) ? body.documentTypes : [],
        errorMessage: null,
        createdAt: now,
        updatedAt: now,
      };
      await redisService.setIntegration(id, integration);
      res.status(201).json(integration);
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create integration' } });
    }
  });

  router.put('/api/admin/integrations/:id', mockBodyParser, requireAdmin, async (req: Request, res: Response) => {
    try {
      const existing = await redisService.getIntegration(req.params.id);
      if (!existing) {
        res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Integration not found' } });
        return;
      }
      const updated = { ...(existing as any), ...req.body, id: req.params.id, updatedAt: new Date().toISOString() };
      await redisService.setIntegration(req.params.id, updated);
      res.json(updated);
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update integration' } });
    }
  });

  router.delete('/api/admin/integrations/:id', requireAdmin, async (req: Request, res: Response) => {
    try {
      const deleted = await redisService.deleteIntegration(req.params.id);
      if (!deleted) {
        res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Integration not found' } });
        return;
      }
      res.json({ success: true });
    } catch (err) {
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to delete integration' } });
    }
  });

  // -------------------------------------------------------------------------
  // Integration Test Connection
  // -------------------------------------------------------------------------

  router.post('/api/admin/integrations/:id/test', mockBodyParser, requireAdmin, async (req: Request, res: Response) => {
    const start = Date.now();
    try {
      const integ = await redisService.getIntegration(req.params.id) as any;
      if (!integ) {
        res.json({ success: false, message: 'Integration not found', troubleshooting: ['Ensure the integration has been saved before testing.'] });
        return;
      }

      const cfg = integ.config || {};
      const requiredFields = REQUIRED_CONFIG_FIELDS[integ.integrationType]?.[integ.provider] || [];
      const missingFields = requiredFields.filter((f: string) => {
        const val = cfg[f];
        return val === undefined || val === null || val === '';
      });

      if (missingFields.length > 0) {
        const troubleshooting = missingFields.map((f: string) =>
          `Missing required field: ${f}. Check the setup guide for where to find this value.`
        );
        res.json({
          success: false,
          message: `Configuration incomplete \u2014 ${missingFields.length} required field(s) missing`,
          latencyMs: Date.now() - start,
          details: { missingFields, provider: integ.provider, integrationType: integ.integrationType },
          troubleshooting,
        });
        return;
      }

      // Blockfrost: real API test
      if (integ.integrationType === 'blockchain' && integ.provider === 'blockfrost' && cfg.projectId) {
        try {
          const network = cfg.network || 'preprod';
          const bfUrl = `https://cardano-${network}.blockfrost.io/api/v0/`;
          const bfResp = await fetch(bfUrl, { headers: { project_id: cfg.projectId }, signal: AbortSignal.timeout(8000) });
          const latencyMs = Date.now() - start;
          if (bfResp.ok) {
            const body = await bfResp.json() as Record<string, unknown>;
            const updated = { ...integ, status: 'connected', lastSyncAt: new Date().toISOString(), errorMessage: null, updatedAt: new Date().toISOString() };
            await redisService.setIntegration(integ.id, updated);
            res.json({ success: true, message: `Connected to Cardano ${network} via Blockfrost`, latencyMs, details: { network, url: body.url, version: body.version } });
          } else {
            const errBody = await bfResp.json().catch(() => ({})) as Record<string, unknown>;
            const troubleshooting: string[] = [];
            if (bfResp.status === 403) {
              troubleshooting.push('The project ID is invalid or does not have access to this network.');
              troubleshooting.push('Go to blockfrost.io/dashboard, check the project exists and the network matches.');
            } else if (bfResp.status === 402) {
              troubleshooting.push('Blockfrost API usage limit exceeded. Check your plan on blockfrost.io.');
            }
            const updated = { ...integ, status: 'error', errorMessage: (errBody.message as string) || `HTTP ${bfResp.status}`, updatedAt: new Date().toISOString() };
            await redisService.setIntegration(integ.id, updated);
            res.json({ success: false, message: (errBody.message as string) || `Blockfrost returned HTTP ${bfResp.status}`, latencyMs, troubleshooting });
          }
          return;
        } catch (err: any) {
          res.json({ success: false, message: `Network error: ${err.message}`, latencyMs: Date.now() - start, troubleshooting: ['Check that the API gateway has outbound internet access.', 'Verify the network name (mainnet, preprod, preview) is correct.'] });
          return;
        }
      }

      // All other providers: config-validation-based test
      const latencyMs = Date.now() - start;
      const updated = { ...integ, status: 'connected', lastSyncAt: new Date().toISOString(), errorMessage: null, updatedAt: new Date().toISOString() };
      await redisService.setIntegration(integ.id, updated);
      res.json({
        success: true,
        message: `Configuration validated for ${integ.provider}. All required fields present.`,
        latencyMs,
        details: { provider: integ.provider, integrationType: integ.integrationType, fieldsValidated: requiredFields.length },
      });
    } catch (err) {
      res.json({ success: false, message: 'Test failed unexpectedly', latencyMs: Date.now() - start, troubleshooting: ['An internal error occurred. Check API gateway logs.'] });
    }
  });

  // =========================================================================
  // Verification Queue (in-memory, development only)
  // =========================================================================

  const mockVerificationQueue: Array<Record<string, unknown>> = [];

  router.get('/api/admin/verification-queue', requireAdmin, (req: Request, res: Response) => {
    const { documentType, status } = req.query;
    let items = [...mockVerificationQueue];

    if (documentType) {
      items = items.filter(item => item.documentType === documentType);
    }
    if (status) {
      items = items.filter(item => (item.status as string) === status);
    }

    res.json({
      items,
      queue: items, // Alias for backwards compatibility
      total: items.length,
      pending: items.filter(i => i.status === 'pending').length,
    });
  });

  router.post('/api/admin/verification-queue/:id/action', requireAdmin, mockBodyParser, (req: Request, res: Response) => {
    const { id } = req.params;
    const { action, notes, assignedTo } = req.body || {};
    const validActions = ['approve', 'reject', 'escalate', 'assign'];
    if (!action || !validActions.includes(action)) {
      res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `Invalid action. Must be one of: ${validActions.join(', ')}` } });
      return;
    }
    const idx = mockVerificationQueue.findIndex(item => item.id === id);
    if (idx !== -1) {
      if (action === 'approve') mockVerificationQueue[idx].status = 'approved';
      else if (action === 'reject') mockVerificationQueue[idx].status = 'rejected';
      else if (action === 'escalate') mockVerificationQueue[idx].status = 'escalated';
      else if (action === 'assign') mockVerificationQueue[idx].assignedTo = assignedTo;
      if (notes) mockVerificationQueue[idx].notes = notes;
      mockVerificationQueue[idx].updatedAt = new Date().toISOString();
      mockVerificationQueue[idx].updatedBy = req.user?.email || 'admin';
    }
    res.json({
      success: true,
      id,
      action,
      notes: notes || null,
      assignedTo: assignedTo || null,
      updatedAt: new Date().toISOString(),
    });
  });

  // =========================================================================
  // Audit Logs
  // =========================================================================

  router.get('/api/admin/audit-logs', requireAdmin, (req: Request, res: Response) => {
    const { action, resourceType, limit = 50, offset = 0 } = req.query;
    let logs = [
      { id: 'evt-1', action: 'admin.login', type: 'admin.login', resourceType: 'auth', actor: 'admin@test.local', userId: 'admin-001', createdAt: new Date().toISOString(), success: true, ipAddress: '127.0.0.1', details: {} },
      { id: 'evt-2', action: 'document_type_created', type: 'workflow.created', resourceType: 'document_type', actor: 'admin@test.local', userId: 'admin-001', createdAt: new Date().toISOString(), success: true, ipAddress: '127.0.0.1', details: {} },
      { id: 'evt-3', action: 'document_type_created', type: 'document.created', resourceType: 'document_type', actor: 'admin@test.local', userId: 'admin-001', createdAt: new Date().toISOString(), success: true, ipAddress: '127.0.0.1', details: {} },
      { id: 'evt-4', action: 'verification_policy_created', type: 'policy.created', resourceType: 'verification_policy', actor: 'admin@test.local', userId: 'admin-001', createdAt: new Date().toISOString(), success: true, ipAddress: '127.0.0.1', details: {} },
    ];

    if (action) logs = logs.filter(log => log.action === action);
    if (resourceType) logs = logs.filter(log => log.resourceType === resourceType);

    const total = logs.length;
    logs = logs.slice(Number(offset), Number(offset) + Number(limit));

    res.json({
      success: true,
      logs,
      events: logs,
      total,
    });
  });

  // Alias: the frontend calls /api/security/audit, map it to the same handler
  router.get('/api/security/audit', requireAdmin, (req: Request, res: Response) => {
    const { action, resourceType, limit = 50, offset = 0 } = req.query;
    let logs = [
      { id: 'evt-1', action: 'admin.login', type: 'admin.login', resourceType: 'auth', actor: 'admin@test.local', userId: 'admin-001', createdAt: new Date().toISOString(), success: true, ipAddress: '127.0.0.1', details: {} },
      { id: 'evt-2', action: 'document_type_created', type: 'workflow.created', resourceType: 'document_type', actor: 'admin@test.local', userId: 'admin-001', createdAt: new Date().toISOString(), success: true, ipAddress: '127.0.0.1', details: {} },
      { id: 'evt-3', action: 'verification_policy_created', type: 'policy.created', resourceType: 'verification_policy', actor: 'admin@test.local', userId: 'admin-001', createdAt: new Date().toISOString(), success: true, ipAddress: '127.0.0.1', details: {} },
    ];
    if (action) logs = logs.filter(l => l.action === action);
    if (resourceType) logs = logs.filter(l => l.resourceType === resourceType);
    const total = logs.length;
    logs = logs.slice(Number(offset), Number(offset) + Number(limit));
    res.json({ success: true, logs, total });
  });

  // =========================================================================
  // Platform Settings (Redis-backed)
  // =========================================================================

  router.get('/api/admin/settings', requireAdmin, async (req: Request, res: Response) => {
    const { category } = req.query;
    const allSettings = (await redisService.getNotificationSettings('platform-settings') || {
      general: { platformName: 'Secuura', defaultLanguage: 'en', maintenanceMode: false },
      security: { mfaRequired: false, sessionTimeout: 3600, passwordPolicy: 'strong' },
      notifications: { emailEnabled: true, slackEnabled: false, webhookUrl: '' },
      blockchain: { network: 'preprod', confirmationBlocks: 6, autoAnchor: false },
    }) as Record<string, unknown>;
    if (category && typeof category === 'string' && allSettings[category]) {
      res.json({ settings: { [category]: allSettings[category] } });
    } else {
      res.json({ settings: allSettings });
    }
  });

  router.put('/api/admin/settings', requireAdmin, mockBodyParser, async (req: Request, res: Response) => {
    const body = req.body || {};
    const existing = (await redisService.getNotificationSettings('platform-settings') || {}) as Record<string, unknown>;
    const merged = { ...existing, ...body };
    await redisService.setNotificationSettings('platform-settings', merged);
    res.json({ success: true, settings: merged, updatedAt: new Date().toISOString() });
  });

  // Public read-only endpoint — verifier portal uses this to know which matching
  // strategy is active (no auth required because the verifier portal is public).
  router.get('/api/verification/policy', async (_req: Request, res: Response) => {
    try {
      const allSettings = (await redisService.getNotificationSettings('platform-settings') || {}) as Record<string, any>;
      const verification = allSettings.verification || {};
      res.json({
        matchingStrategy: verification.matchingStrategy || 'title_and_hash',
        requireBlockchainAnchor: verification.requireBlockchainAnchor ?? true,
        showTamperWarning: verification.showTamperWarning ?? true,
      });
    } catch {
      res.json({ matchingStrategy: 'title_and_hash', requireBlockchainAnchor: true, showTamperWarning: true });
    }
  });

  // =========================================================================
  // Identity Management (PostgreSQL-backed)
  // =========================================================================

  async function ensureIdentityColumns(): Promise<void> {
    if (!isDbAvailable()) return;
    try {
      await query(`ALTER TABLE users ADD COLUMN IF NOT EXISTS display_name VARCHAR(200)`);
      await query(`ALTER TABLE users ADD COLUMN IF NOT EXISTS wallet_address VARCHAR(255)`);
      await query(`ALTER TABLE users ADD COLUMN IF NOT EXISTS auth_method VARCHAR(20) DEFAULT 'email'`);
      await query(`ALTER TABLE users ADD COLUMN IF NOT EXISTS organization_id UUID REFERENCES organizations(id)`);
    } catch { /* columns may already exist */ }
  }

  let identityColumnsEnsured = false;
  async function seedIdentityOrgsIfEmpty(): Promise<void> {
    if (!isDbAvailable()) return;
    if (!enableDemoSeed) return;
    if (!identityColumnsEnsured) {
      await ensureIdentityColumns();
      identityColumnsEnsured = true;
    }
    try {
      const orgResult = await runWithPlatformScope(() => query('SELECT COUNT(*) as cnt FROM organizations'));
      const needOrgs = parseInt(orgResult.rows[0].cnt, 10) === 0;
      const userResult = await runWithPlatformScope(() => query('SELECT COUNT(*) as cnt FROM users'));
      const needUsers = parseInt(userResult.rows[0].cnt, 10) === 0;
      if (!needOrgs && !needUsers) return;
      for (const org of SEED_IDENTITY_ORGS) {
        await runWithPlatformScope(() => query(
          `INSERT INTO organizations (id, name, slug, type, status, verified, metadata) VALUES ($1, $2, $3, $4, $5, $6, $7) ON CONFLICT (id) DO NOTHING`,
          [org.id, org.name, org.slug, org.type, org.status, org.verified, JSON.stringify(org.metadata)]
        ));
      }
      for (const u of SEED_IDENTITY_USERS) {
        await runWithPlatformScope(() => query(
          `INSERT INTO users (email, display_name, role, verification_level, auth_method, mfa_enabled, wallet_address, external_provider, organization_id, metadata, password_hash)
           VALUES ($1, $2, $3, $4, $5, $6, $7, $8, $9, $10, $11) ON CONFLICT (email) DO NOTHING`,
          [u.email, u.display_name, u.role, u.verification_level, u.auth_method, u.mfa_enabled, u.wallet_address, u.external_provider, u.organization_id, JSON.stringify(u.metadata), null]
        ));
      }
      log('info', '[Identity] Seeded demo organizations and identity users');
    } catch (err) {
      log('warn', '[Identity] Seed skipped: ' + (err as Error).message);
    }
  }

  router.get('/api/admin/identity/users', requireAdmin, async (req: Request, res: Response) => {
    try {
      await seedIdentityOrgsIfEmpty();
      const result = await adminScope(req, () => query(`
        SELECT
          u.id AS "userId",
          u.email,
          COALESCE(u.display_name, u.first_name || ' ' || u.last_name, u.email) AS "name",
          UPPER(COALESCE(u.verification_level, 'BASIC')) AS "verificationLevel",
          COALESCE(u.auth_method, 'email') AS "authMethod",
          COALESCE((u.metadata->>'social_providers')::text, '[]') AS "socialProvidersRaw",
          COALESCE(u.mfa_enabled, false) AS "mfaEnabled",
          CASE WHEN u.wallet_address IS NOT NULL AND u.wallet_address <> '' THEN true ELSE false END AS "walletConnected",
          COALESCE(u.organization_id::text, '') AS "orgId",
          COALESCE(o.name, '') AS "orgName",
          COALESCE(u.metadata->>'region', 'Unknown') AS "region"
        FROM users u
        LEFT JOIN organizations o ON o.id = u.organization_id
        ORDER BY u.display_name ASC
      `));

      const users = result.rows.map((r: Record<string, unknown>) => {
        let socialProviders: string[] = [];
        try { socialProviders = JSON.parse(r.socialProvidersRaw as string); } catch { /* empty */ }
        if (r.authMethod && r.authMethod !== 'email' && !socialProviders.includes(r.authMethod as string)) {
          socialProviders.push(r.authMethod as string);
        }
        return { ...r, socialProviders, socialProvidersRaw: undefined };
      });

      res.json({ success: true, users });
    } catch (err) {
      log('error', '[Identity] Failed to fetch users', { error: err instanceof Error ? err.message : String(err) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch identity users' } });
    }
  });

  router.get('/api/admin/identity/organizations', requireAdmin, async (req: Request, res: Response) => {
    try {
      await seedIdentityOrgsIfEmpty();
      const result = await adminScope(req, () => query(`
        SELECT
          id AS "orgId",
          name AS "orgName",
          COALESCE(metadata->>'trust_level', 'UNVERIFIED') AS "trustLevel",
          COALESCE(metadata->>'verification_mode', 'DOMAIN_ONLY') AS "verificationMode",
          COALESCE(metadata->>'domain', '') AS "domain",
          COALESCE((metadata->>'domain_verified')::boolean, false) AS "domainVerified",
          CASE WHEN verified THEN 'verified' ELSE 'pending' END AS "status"
        FROM organizations
        ORDER BY name ASC
      `));
      res.json({ success: true, organizations: result.rows });
    } catch (err) {
      log('error', '[Identity] Failed to fetch organizations', { error: err instanceof Error ? err.message : String(err) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to fetch identity organizations' } });
    }
  });

  router.patch('/api/admin/identity/users/:id/level', requireAdmin, mockBodyParser, async (req: Request, res: Response) => {
    try {
      const { id } = req.params;
      const { verificationLevel } = req.body || {};
      const validLevels = ['NONE', 'BASIC', 'SOCIAL', 'STANDARD', 'ENHANCED', 'HIGH', 'GOVERNMENT'];
      if (!verificationLevel || !validLevels.includes(verificationLevel)) {
        res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `Invalid verification level. Must be one of: ${validLevels.join(', ')}` } });
        return;
      }
      const result = await adminScope(req, () => query(
        'UPDATE users SET verification_level = $1, updated_at = NOW() WHERE id = $2::uuid RETURNING id, verification_level',
        [verificationLevel, id]
      ));
      if (result.rowCount === 0) {
        res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'User not found' } });
        return;
      }
      res.json({ success: true, userId: id, verificationLevel });
    } catch (err) {
      log('error', '[Identity] Failed to update level', { error: err instanceof Error ? err.message : String(err) });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update verification level' } });
    }
  });

  router.get('/api/admin/identity/providers', requireAdmin, async (_req: Request, res: Response) => {
    const providers = [
      { name: 'google', label: 'Google', tier: 'SOCIAL', configured: !!(process.env.SOCIAL_GOOGLE_CLIENT_ID), status: process.env.SOCIAL_GOOGLE_CLIENT_ID ? 'active' : 'not_configured' },
      { name: 'github', label: 'GitHub', tier: 'SOCIAL', configured: !!(process.env.SOCIAL_GITHUB_CLIENT_ID), status: process.env.SOCIAL_GITHUB_CLIENT_ID ? 'active' : 'not_configured' },
      { name: 'linkedin', label: 'LinkedIn', tier: 'SOCIAL', configured: !!(process.env.SOCIAL_LINKEDIN_CLIENT_ID), status: process.env.SOCIAL_LINKEDIN_CLIENT_ID ? 'active' : 'not_configured' },
      { name: 'facebook', label: 'Facebook', tier: 'SOCIAL', configured: false, status: 'not_configured' },
      { name: 'apple', label: 'Apple', tier: 'SOCIAL', configured: false, status: 'not_configured' },
      { name: 'microsoft_personal', label: 'Microsoft Personal', tier: 'SOCIAL', configured: false, status: 'not_configured' },
      { name: 'entra_id', label: 'Microsoft Entra ID', tier: 'ENHANCED', configured: !!(process.env.AZURE_AD_CLIENT_ID), status: process.env.AZURE_AD_CLIENT_ID ? 'active' : 'not_configured' },
      { name: 'auth0', label: 'Auth0', tier: 'ENHANCED', configured: !!(process.env.AUTH0_DOMAIN), status: process.env.AUTH0_DOMAIN ? 'active' : 'not_configured' },
      { name: 'okta', label: 'Okta', tier: 'ENHANCED', configured: false, status: 'not_configured' },
      { name: 'entra_verified_id', label: 'Entra Verified ID', tier: 'HIGH', configured: !!(process.env.ENTRA_CLIENT_ID), status: process.env.ENTRA_CLIENT_ID ? 'active' : 'not_configured' },
      // Onfido retired 2026-04-29 — see CONNECTORS.md. The platform's HIGH-
      // tier identity path is Microsoft Entra Verified ID (entry above).
    ];
    res.json({ success: true, providers });
  });

  // =========================================================================
  // Verification Policies CRUD (Redis-backed)
  // =========================================================================

  // Seed policies on first load
  (async () => {
    const existing = await redisService.getAllVerificationPolicies();
    if (existing.length === 0 && enableDemoSeed) {
      for (const p of SEED_POLICIES) {
        await redisService.setVerificationPolicy(p.id, p);
      }
      log('info', `[VerifPolicies] Seeded ${SEED_POLICIES.length} default policies`);
    }
  })().catch(() => {});

  router.get('/api/admin/verification-policies', requireAdmin, async (_req: Request, res: Response) => {
    const policies = await redisService.getAllVerificationPolicies();
    res.json({ success: true, policies, total: policies.length });
  });

  router.post('/api/admin/verification-policies', requireAdmin, mockBodyParser, async (req: Request, res: Response) => {
    const body = req.body || {};
    if (!body.name) { res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Policy name is required' } }); return; }
    const id = `vpol-${require('crypto').randomUUID()}`;
    const policy = { id, ...body, isActive: body.isActive !== false, createdAt: new Date().toISOString() };
    await redisService.setVerificationPolicy(id, policy);
    res.status(201).json(policy);
  });

  router.put('/api/admin/verification-policies/:id', requireAdmin, mockBodyParser, async (req: Request, res: Response) => {
    const { id } = req.params;
    const existing = await redisService.getVerificationPolicy(id);
    if (!existing) { res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Policy not found' } }); return; }
    const updated = { ...(existing as Record<string, unknown>), ...req.body, id, updatedAt: new Date().toISOString() };
    await redisService.setVerificationPolicy(id, updated);
    res.json(updated);
  });

  router.delete('/api/admin/verification-policies/:id', requireAdmin, async (req: Request, res: Response) => {
    const { id } = req.params;
    const deleted = await redisService.deleteVerificationPolicy(id);
    if (!deleted) { res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Policy not found' } }); return; }
    res.json({ success: true });
  });

  router.get('/api/admin/verification-policies/audit', requireAdmin, (_req: Request, res: Response) => {
    res.json({ success: true, entries: [] });
  });

  router.get('/api/admin/verification-policies/regional', requireAdmin, (_req: Request, res: Response) => {
    res.json({ success: true, regions: [] });
  });

  // =========================================================================
  // =========================================================================
  // POST /api/users/admin/create — Proxy to auth service for user creation
  // =========================================================================
  router.post('/api/users/admin/create', requireAdmin, mockBodyParser, async (req: Request, res: Response) => {
    try {
      const authUrl = services.auth?.url || 'http://auth:4003';
      const token = req.headers.authorization;
      const upstream = await fetch(`${authUrl}/api/users/admin/create`, {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: token } : {}),
        },
        body: JSON.stringify(req.body),
      });
      const data = await upstream.json().catch(() => ({}));
      res.status(upstream.status).json(data);
    } catch (err: any) {
      console.error('Failed to create user via auth:', err?.message);
      res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'Auth service unavailable' } });
    }
  });

  // Organizations CRUD (PostgreSQL-backed)
  // =========================================================================

  router.post('/api/users/admin/organizations', requireAdmin, mockBodyParser, async (req: Request, res: Response) => {
    try {
      const { name, type, status } = req.body || {};
      if (!name) { res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Organization name is required' } }); return; }
      const id = `org-${require('crypto').randomUUID()}`;
      if (isDbAvailable()) {
        await adminScope(req, () => query(
          `INSERT INTO organizations (id, name, type, status, slug, verified, metadata) VALUES ($1::uuid, $2, $3, $4, $5, false, '{}')`,
          [crypto.randomUUID(), name, type || 'Organization', status || 'pending', name.toLowerCase().replace(/\s+/g, '-')]
        ));
      }
      res.status(201).json({ id, name, type: type || 'Organization', status: status || 'pending', userCount: 0, documentCount: 0, createdAt: new Date().toISOString() });
    } catch (err) {
      log('error', '[Orgs] Create failed', { error: (err as Error).message });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to create organization' } });
    }
  });

  router.put('/api/users/admin/organizations/:id', requireAdmin, mockBodyParser, async (req: Request, res: Response) => {
    try {
      const { id } = req.params;
      const { name, type, status } = req.body || {};
      if (isDbAvailable()) {
        const result = await adminScope(req, () => query(
          `UPDATE organizations SET name = COALESCE($1, name), type = COALESCE($2, type), status = COALESCE($3, status), updated_at = NOW() WHERE id = $4::uuid RETURNING *`,
          [name, type, status, id]
        ));
        if (result.rowCount === 0) { res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Organization not found' } }); return; }
        res.json({ success: true, ...result.rows[0] });
      } else {
        res.json({ success: true });
      }
    } catch (err) {
      log('error', '[Orgs] Update failed', { error: (err as Error).message });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to update organization' } });
    }
  });

  // PATCH /api/users/admin/:id — Admin: update a user (role, status, etc.)
  router.patch('/api/users/admin/:id', requireAdmin, mockBodyParser, async (req: Request, res: Response) => {
    try {
      const { id } = req.params;
      const updates = req.body || {};
      const authUrl = services.auth?.url || 'http://auth:4003';
      const token = req.headers.authorization;

      const upstream = await fetch(`${authUrl}/api/users/admin/${encodeURIComponent(id)}`, {
        method: 'PATCH',
        headers: {
          'Content-Type': 'application/json',
          ...(token ? { Authorization: token } : {}),
        },
        body: JSON.stringify(updates),
      });

      const body = await upstream.json().catch(() => ({}));
      res.status(upstream.status).json(body);
    } catch (err: any) {
      res.status(502).json({ success: false, error: { code: 'BAD_GATEWAY', message: 'Auth service unavailable', details: { details: err.message } } });
    }
  });

  router.delete('/api/users/admin/organizations/:id', requireAdmin, async (req: Request, res: Response) => {
    try {
      const { id } = req.params;
      if (isDbAvailable()) {
        const result = await adminScope(req, () => query('DELETE FROM organizations WHERE id = $1::uuid', [id]));
        if (result.rowCount === 0) { res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Organization not found' } }); return; }
      }
      res.json({ success: true });
    } catch (err) {
      log('error', '[Orgs] Delete failed', { error: (err as Error).message });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to delete organization' } });
    }
  });

  // =========================================================================
  // Notification Settings (Redis-backed)
  // =========================================================================

  router.get('/api/settings/notifications', authenticateToken(false), async (req: Request, res: Response) => {
    // Pen-test F-04: read from authenticated req.user only — fallback to raw
    // x-user-id header was spoofable on optional-auth routes.
    const userId = req.user?.userId || 'default';
    const settings = await redisService.getNotificationSettings(userId);
    const data = settings || { certificationNotifications: true, verificationNotifications: true };
    res.json({ success: true, ...data });
  });

  router.put('/api/settings/notifications', authenticateToken(true), mockBodyParser, async (req: Request, res: Response) => {
    // Pen-test F-04: read from authenticated req.user only — fallback to raw
    // x-user-id header was spoofable on optional-auth routes.
    // KS-719: this is a WRITE, so it requires authentication (Kam, 2026-08-29).
    // The GET above keeps optional auth so anonymous readers still get the
    // documented defaults, but there is no 'default' write bucket: an
    // unauthenticated PUT used to land in one that every other anonymous
    // caller then read back. authenticateToken(true) guarantees req.user
    // here, so the fallback is not merely unused — it must not exist.
    const userId = req.user!.userId;
    const body = req.body || {};
    await redisService.setNotificationSettings(userId, body);
    res.json({ success: true, ...body, updatedAt: new Date().toISOString() });
  });

  // =========================================================================
  // Privacy Settings (per-user toggle settings, Redis-backed)
  // =========================================================================

  router.get('/api/privacy/settings', authenticateToken(false), async (req: Request, res: Response) => {
    // Pen-test F-04: read from authenticated req.user only — fallback to raw
    // x-user-id header was spoofable on optional-auth routes.
    const userId = req.user?.userId || 'default';
    const settings = await redisService.getPrivacySettings(`priv-settings-${userId}`);
    res.json({
      success: true,
      settings: settings || {
        autoRejectUnknown: false,
        preferRangeProofs: true,
        preferCommitments: true,
        logAllDisclosures: true,
        notifyOnDisclosure: true,
      },
    });
  });

  router.put('/api/privacy/settings', authenticateToken(true), mockBodyParser, async (req: Request, res: Response) => {
    // Pen-test F-04: read from authenticated req.user only — fallback to raw
    // x-user-id header was spoofable on optional-auth routes.
    // KS-719: this is a WRITE, so it requires authentication (Kam, 2026-08-29).
    // The GET above keeps optional auth so anonymous readers still get the
    // documented defaults, but there is no 'default' write bucket: an
    // unauthenticated PUT used to land in one that every other anonymous
    // caller then read back. authenticateToken(true) guarantees req.user
    // here, so the fallback is not merely unused — it must not exist.
    const userId = req.user!.userId;
    const body = req.body || {};
    await redisService.setPrivacySettings(`priv-settings-${userId}`, body);
    res.json({ success: true, settings: body, updatedAt: new Date().toISOString() });
  });

  // =========================================================================
  // Audit Export
  // =========================================================================

  router.get('/api/security/audit/export', requireAdmin, async (req: Request, res: Response) => {
    try {
      let logs: Array<Record<string, unknown>> = [];
      if (isDbAvailable()) {
        const result = await adminScope(req, () => query('SELECT * FROM audit_logs ORDER BY created_at DESC LIMIT 1000'));
        logs = result.rows;
      }
      const header = 'Timestamp,Action,UserID,ResourceType,ResourceID,Success,IP Address,Details';
      const rows = logs.map((l: Record<string, unknown>) =>
        `"${l.created_at || ''}","${l.action || ''}","${l.user_id || ''}","${l.resource_type || ''}","${l.resource_id || ''}","${l.success ?? ''}","${l.ip_address || ''}","${String(l.details || '').replace(/"/g, '""')}"`
      );
      const csv = [header, ...rows].join('\n');
      res.setHeader('Content-Type', 'text/csv');
      res.setHeader('Content-Disposition', `attachment; filename=secuura-audit-${new Date().toISOString().slice(0, 10)}.csv`);
      res.send(csv);
    } catch (err) {
      log('error', '[AuditExport] Failed', { error: (err as Error).message });
      res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'Failed to export audit logs' } });
    }
  });

  return router;
}
