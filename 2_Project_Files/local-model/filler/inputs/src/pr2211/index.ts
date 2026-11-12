/**
 * =============================================================================
 * SECUURA KYC SERVICE
 * =============================================================================
 * Handles advanced identity verification:
 * - Multiple verification levels (Basic to Government)
 * - Third-party KYC provider integration (Onfido, Jumio, Sumsub)
 * - Document verification
 * - Liveness detection
 * - GDPR compliance
 * Port: 4011
 * =============================================================================
 */

// KS-1725: FIRST import, before any module that could parse: installs the zod 3 compatible issue map
// (zod 4 error map; see packages/shared/src/validation/zod3-compat.ts) for this whole process.
import '@secuura/shared/zod3-compat';
import express, { Request, Response, NextFunction, RequestHandler } from 'express';
import { boundedJson } from '@secuura/shared'; // KS-1724: express.json plus the structural caps (array length, node count, depth)
import cors from 'cors';
import helmet from 'helmet';
import { z } from 'zod';
import { v4 as uuidv4 } from 'uuid';
import crypto from 'crypto';
import dotenv from 'dotenv';
import { initDb, query, isDbAvailable } from './db';
import { logger, validateEnv } from './utils/logger';
import {
  enforceProductionConfig, decryptField, initFromEnv as initPiiCrypto,
  encryptFieldWithDek, decryptFieldWithDek, isSubjectDekCiphertext, isEncryptedPii,
  authenticate as jwtAuthenticate, errorHandler, AppError,
  rejectNulBytes,
  assertSupportedImage,
  // KS-1845: the shared platform-role predicate gates POST /api/kyc/:id/review below.
  isPlatformRole,
} from '@secuura/shared';
import type { VerifiedImageType } from '@secuura/shared';
import { subjectDeks } from './subjectDeks';

dotenv.config();

// Validate environment variables at startup
validateEnv();

// Production startup guard — refuse to start with mock KYC in production
enforceProductionConfig('kyc', {
  requiredEnvVars: ['ENTRA_VERIFIED_ID_TENANT_ID', 'ENTRA_VERIFIED_ID_CLIENT_ID'],
  forbiddenValues: {
    'KYC_PROVIDER': ['mock'],
  },
  requireRealProviders: true,
});

// Import Microsoft Entra routes
import { microsoftVerificationRoutes } from './routes/microsoft-verification';

const app = express();
const PORT = process.env.PORT || 4011;

// KYC Provider configuration
const KYC_PROVIDER = process.env.KYC_PROVIDER || 'mock'; // mock | microsoft (Entra Verified ID). Onfido / Jumio / Sumsub retired 2026-04-29.

// =============================================================================
// TYPE DEFINITIONS
// =============================================================================

type VerificationLevel = 'NONE' | 'BASIC' | 'SOCIAL' | 'STANDARD' | 'ENHANCED' | 'HIGH' | 'GOVERNMENT';
type VerificationStatus = 'pending' | 'in_progress' | 'under_review' | 'approved' | 'rejected' | 'expired';
type DocumentType = 'passport' | 'driving_license' | 'national_id' | 'residence_permit' | 'other';

interface KYCVerification {
  id: string;
  userId: string;
  requestedLevel: VerificationLevel;
  currentLevel: VerificationLevel;
  status: VerificationStatus;
  
  // Provider info
  provider: string;
  providerApplicationId?: string;
  providerCheckId?: string;
  
  // Submitted documents
  documents: VerificationDocument[];
  
  // Liveness check
  livenessCompleted: boolean;
  livenessScore?: number;
  
  // Results
  checks: VerificationCheck[];
  overallScore?: number;
  riskLevel?: 'low' | 'medium' | 'high';
  
  // Review
  reviewedBy?: string;
  reviewNotes?: string;
  
  // Compliance
  consentGiven: boolean;
  consentTimestamp?: Date;
  dataRetentionExpiry?: Date;
  
  // Timestamps
  createdAt: Date;
  updatedAt: Date;
  completedAt?: Date;
  expiresAt?: Date;
}

interface VerificationDocument {
  id: string;
  type: DocumentType;
  country: string;
  frontImageId?: string;
  backImageId?: string;
  extractedData?: {
    fullName?: string;
    dateOfBirth?: string;
    documentNumber?: string;
    expiryDate?: string;
    nationality?: string;
    address?: string;
  };
  validationStatus: 'pending' | 'valid' | 'invalid' | 'expired';
  validationErrors?: string[];
  uploadedAt: Date;
}

interface VerificationCheck {
  id: string;
  type: 'document' | 'facial' | 'liveness' | 'watchlist' | 'pep' | 'sanctions';
  status: 'pending' | 'passed' | 'failed' | 'review_required';
  result?: object;
  completedAt?: Date;
}

interface ConsentRecord {
  id: string;
  userId: string;
  verificationId: string;
  consentType: 'data_processing' | 'data_sharing' | 'biometric';
  consentGiven: boolean;
  ipAddress?: string;
  userAgent?: string;
  timestamp: Date;
  expiresAt?: Date;
  withdrawnAt?: Date;
}

// =============================================================================
// DATABASE HELPER FUNCTIONS (DB-only — no in-memory Maps)
// =============================================================================

async function dbSaveVerification(v: KYCVerification): Promise<void> {
  if (!isDbAvailable()) return;
  try {
    // Audit 1.3 phase 4b: encrypt documents (JSONB → ciphertext stored as
    // TEXT) and review_notes (TEXT → ciphertext) at rest. AAD bound to the
    // verification id so a ciphertext can't be ported between rows. Other
    // fields stay plaintext (status flags, scores, timestamps, references).
    // KS-291: encryption is under the USER's subject DEK (d1: format) so the
    // ciphertext becomes unrecoverable everywhere — including backups — when
    // the key is destroyed on erasure.
    const docsPlain = JSON.stringify(v.documents || []);
    const dek = (docsPlain && docsPlain !== '[]') || v.reviewNotes
      ? await subjectDeks.getOrCreateDek(v.userId)
      : null;
    const docsEncrypted = docsPlain && docsPlain !== '[]' && dek
      ? encryptFieldWithDek(docsPlain, `svc_kyc_verifications.documents.${v.id}`, dek)
      : null;
    const notesEncrypted = v.reviewNotes && dek
      ? encryptFieldWithDek(v.reviewNotes, `svc_kyc_verifications.review_notes.${v.id}`, dek)
      : null;

    await query(
      `INSERT INTO svc_kyc_verifications (id, user_id, requested_level, current_level, status, provider,
         provider_application_id, provider_check_id, documents, liveness_completed, liveness_score,
         checks, overall_score, risk_level, reviewed_by, review_notes, consent_given, consent_timestamp,
         data_retention_expiry, created_at, updated_at, completed_at, expires_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10,$11,$12,$13,$14,$15,$16,$17,$18,$19,$20,$21,$22,$23)
       ON CONFLICT (id) DO UPDATE SET
         status = EXCLUDED.status, current_level = EXCLUDED.current_level, documents = EXCLUDED.documents,
         liveness_completed = EXCLUDED.liveness_completed, liveness_score = EXCLUDED.liveness_score,
         checks = EXCLUDED.checks, overall_score = EXCLUDED.overall_score, risk_level = EXCLUDED.risk_level,
         reviewed_by = EXCLUDED.reviewed_by, review_notes = EXCLUDED.review_notes,
         updated_at = NOW(), completed_at = EXCLUDED.completed_at`,
      [v.id, v.userId, v.requestedLevel, v.currentLevel, v.status, v.provider,
       v.providerApplicationId || null, v.providerCheckId || null, docsEncrypted,
       v.livenessCompleted, v.livenessScore || null, JSON.stringify(v.checks || []),
       v.overallScore || null, v.riskLevel || null, v.reviewedBy || null, notesEncrypted,
       v.consentGiven, v.consentTimestamp || null, v.dataRetentionExpiry || null,
       v.createdAt, v.updatedAt, v.completedAt || null, v.expiresAt || null]
    );
  } catch (err: any) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.error('DB save verification failed', { error: reason });
  }
}

async function dbGetVerification(id: string): Promise<KYCVerification | undefined> {
  if (!isDbAvailable()) return undefined;
  try {
    const result = await query('SELECT * FROM svc_kyc_verifications WHERE id = $1', [id]);
    if (result.rows.length > 0) return rowToVerification(result.rows[0]);
  } catch (err: any) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.error('DB get verification failed', { id, error: reason });
  }
  return undefined;
}

async function dbGetVerificationsByUser(userId: string, throwOnError = false): Promise<KYCVerification[]> {
  if (!isDbAvailable()) return [];
  try {
    const result = await query(
      'SELECT * FROM svc_kyc_verifications WHERE user_id = $1 ORDER BY created_at DESC',
      [userId],
    );
    // KS-291: rowToVerification is async (per-row subject-DEK resolve, cached)
    return await Promise.all(result.rows.map((row) => rowToVerification(row)));
  } catch (err: any) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.error('DB get verifications by user failed', { userId, error: reason });
    // KS-1931: the erasure cascade passes throwOnError so a failed read stops it (its own comment: failures THROW); every other caller keeps the empty list.
    if (throwOnError) throw err;
    return [];
  }
}

async function dbGetVerificationStats(): Promise<{ total: number; pending: number; approved: number }> {
  if (!isDbAvailable()) return { total: 0, pending: 0, approved: 0 };
  try {
    const result = await query(
      `SELECT
         COUNT(*) AS total,
         COUNT(*) FILTER (WHERE status = 'pending') AS pending,
         COUNT(*) FILTER (WHERE status = 'approved') AS approved
       FROM svc_kyc_verifications`
    );
    const r = result.rows[0];
    return { total: Number(r.total), pending: Number(r.pending), approved: Number(r.approved) };
  } catch (err: any) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.error('DB get verification stats failed', { error: reason });
    return { total: 0, pending: 0, approved: 0 };
  }
}

async function dbSaveConsent(c: ConsentRecord): Promise<void> {
  if (!isDbAvailable()) return;
  try {
    await query(
      `INSERT INTO svc_kyc_consents (id, user_id, verification_id, consent_type, consent_given, ip_address, user_agent, timestamp, expires_at, withdrawn_at)
       VALUES ($1,$2,$3,$4,$5,$6,$7,$8,$9,$10)
       ON CONFLICT (id) DO UPDATE SET consent_given = EXCLUDED.consent_given, withdrawn_at = EXCLUDED.withdrawn_at`,
      [c.id, c.userId, c.verificationId, c.consentType, c.consentGiven,
       c.ipAddress || null, c.userAgent || null, c.timestamp, c.expiresAt || null, c.withdrawnAt || null]
    );
  } catch (err: any) {
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.error('DB save consent failed', { error: reason });
  }
}

/**
 * KS-487 B-4: `mimeType` is a VerifiedImageType — a BRANDED type that only
 * `assertSupportedImage` can produce. The literal `'image/jpeg'` this function
 * used to be called with no longer compiles.
 *
 * The brand is load-bearing and was added after a plain union failed its own
 * check: with `mimeType: SupportedImageType`, passing `'image/jpeg'` still
 * type-checked cleanly, because that literal is a member of the union. The
 * comment claiming the type carried the rule was true of the intent and false
 * of the code. The type system now actually carries it: you cannot call this
 * without having sniffed the bytes.
 */
/**
 * Record the ATTESTATION for a submitted image. The payload is NOT persisted.
 *
 * KS-386, on Kam's ruling of 2026-08-14: *"Platform K should not hold the
 * images at all, only the attestation (what check, which partner, what level,
 * when)."* Migration 045 made `svc_kyc_images.data` nullable so this write
 * could stop while the row survives as that attestation.
 *
 * The bytes are still READ — `assertSupportedImage()` sniffs them at each call
 * site to produce the `mimeType` recorded here (KS-487 B-4), so `mime_type`
 * remains a verified claim about content we looked at and did not keep. That
 * is the distinction migration 045's column comment exists to preserve: NULL
 * means "no payload retained", not "nothing was submitted".
 *
 * The `data` PARAMETER is deliberately gone rather than passed and ignored: a
 * parameter that is accepted and dropped is one edit away from being written
 * again, and this function is the only INSERT into that table.
 *
 * ON FAILURE (KS-386 F-1(b)): THROWS `AppError` 500 `KYC_ATTESTATION_WRITE_FAILED`.
 * All three call sites are inside route handlers whose `catch` forwards to
 * `next(error)` and thence to the shared `errorHandler`, so `/document` and
 * `/selfie` answer 500 with that stable code and an authored message — never
 * `200 success:true` with no row. The thrown message is written here, so the
 * KS-727 redaction has nothing of the driver's to suppress.
 *
 * ONE HONEST LIMIT: when `isDbAvailable()` is false this returns early and
 * writes nothing, and the route still answers 200. That is the in-memory mode,
 * where no row is expected by anyone and there is no database to have failed.
 * It is not the F-1 case, which is a live database refusing the INSERT.
 */
async function dbSaveImage(
  id: string,
  mimeType: VerifiedImageType,
  userId: string,
): Promise<void> {
  if (!isDbAvailable()) return;
  try {
    // KS-291: user_id gives erasure a direct SQL path to the image rows —
    // previously the only linkage was inside the ENCRYPTED documents blob.
    // KS-386: `data` is not named here and must not be re-added.
    await query(
      `INSERT INTO svc_kyc_images (id, mime_type, user_id) VALUES ($1,$2,$3)
       ON CONFLICT (id) DO NOTHING`,
      [id, mimeType, userId]
    );
  } catch (err: any) {
    // KS-386 F-1(b): this used to log and return void, so a failed INSERT
    // produced `200 success:true` with ZERO rows — the caller was told the
    // attestation was recorded when it was not. On a schema whose
    // `svc_kyc_images` predates migrations 035/045 that was every single
    // upload. The attestation is the whole point of the ticket: if it cannot
    // be written, the request must fail rather than lie about it.
    //
    // Deliberately NOT widened (Wednesday's ruling, 2026-09-06): no retry, no
    // queue, no schema check at boot. Failing loud IS the fix; anything more
    // is a separate ticket.
    let reason: string;
    try {
      reason = err instanceof Error ? err.message : String(err);
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.error('DB save image failed', { error: reason });
    throw new AppError(
      'The verification attestation could not be recorded. No document was accepted.',
      500,
      'KYC_ATTESTATION_WRITE_FAILED',
    );
  }
}

async function dbDeleteUserData(userId: string): Promise<number> {
  if (!isDbAvailable()) return 0;
  // KS-291 rewrite. The old version extracted image ids in SQL with
  // jsonb_array_elements(documents) — but documents has been an encrypted
  // TEXT column since audit 1.3 phase 4b, so that statement threw 42883 on
  // every erasure and the single catch swallowed it: images, consents AND
  // verifications all silently survived. Now:
  //   1. image ids are collected app-side from the decrypted verifications
  //      (legacy rows without svc_kyc_images.user_id), plus deleted directly
  //      by the user_id column (rows written after migration 035);
  //   2. failures THROW so the event bus retries and dead-letters instead of
  //      reporting a successful cascade that deleted nothing.

  // Collect legacy image ids while the rows still exist. rowToVerification
  // degrades to documents: [] when ciphertext is unreadable (e.g. DEK already
  // destroyed) — in that case the user_id-column path below still applies to
  // post-035 images, and unreadable-blob legacy images are handled by the
  // 035 backfill having stamped user_id on them.
  const verifications = await dbGetVerificationsByUser(userId, true);
  const imageIds = new Set<string>();
  for (const v of verifications) {
    for (const d of v.documents || []) {
      if (d?.frontImageId) imageIds.add(String(d.frontImageId));
      if (d?.backImageId) imageIds.add(String(d.backImageId));
    }
  }

  if (imageIds.size > 0) {
    await query('DELETE FROM svc_kyc_images WHERE id = ANY($1)', [Array.from(imageIds)]);
  }
  await query('DELETE FROM svc_kyc_images WHERE user_id = $1', [userId]);
  await query('DELETE FROM svc_kyc_consents WHERE user_id = $1', [userId]);
  const result = await query('DELETE FROM svc_kyc_verifications WHERE user_id = $1', [userId]);

  // Drop this instance's cached DEK; originate destroys the key itself.
  subjectDeks.evict(userId);
  return result.rowCount ?? 0;
}

// =============================================================================
// ROW CONVERTER FUNCTIONS
// =============================================================================

async function rowToVerification(r: any): Promise<KYCVerification> {
  const parseJsonb = (val: any, defaultValue: any = []): any => {
    if (val === null || val === undefined) return defaultValue;
    if (typeof val === 'string') return JSON.parse(val);
    return val;
  };

  // KS-291: d1: rows decrypt under the row's user's subject DEK, resolved once
  // per row (cached in-process). Legacy v<N>: rows use the master keyring.
  const needsDek = isSubjectDekCiphertext(r.documents) || isSubjectDekCiphertext(r.review_notes);
  const dek: Buffer | null = needsDek ? await subjectDeks.getDek(r.user_id) : null;

  // Audit 1.3 phase 4b: documents was originally JSONB. Now we serialise +
  // encrypt + base64 the whole array for at-rest protection (it carries
  // government IDs, passport scans references). The column was changed to
  // TEXT in the migration. Plaintext-tail handling: if the value isn't
  // encrypted-field ciphertext we treat it as legacy JSON.
  const decryptDocuments = (val: any): any[] => {
    if (val === null || val === undefined) return [];
    if (typeof val !== 'string') return val;
    if (!isEncryptedPii(val)) return parseJsonb(val, []);
    try {
      if (isSubjectDekCiphertext(val)) {
        if (!dek) {
          log('warn', '[piiCrypto] kyc documents are subject-DEK ciphertext but no DEK is available (destroyed or missing)', { id: r.id });
          return [];
        }
        const plainDek = decryptFieldWithDek(val, `svc_kyc_verifications.documents.${r.id}`, dek);
        return plainDek ? JSON.parse(plainDek) : [];
      }
      const plain = decryptField(val, `svc_kyc_verifications.documents.${r.id}`);
      return plain ? JSON.parse(plain) : [];
    } catch (err: any) {
      log('error', '[piiCrypto] kyc documents decrypt failed', { id: r.id, error: err?.message });
      return [];
    }
  };

  const decryptText = (val: any, col: string): string | undefined => {
    if (val === null || val === undefined || val === '') return undefined;
    if (typeof val !== 'string') return val;
    if (!isEncryptedPii(val)) return val; // legacy plaintext
    try {
      if (isSubjectDekCiphertext(val)) {
        if (!dek) {
          log('warn', `[piiCrypto] kyc ${col} is subject-DEK ciphertext but no DEK is available (destroyed or missing)`, { id: r.id });
          return undefined;
        }
        return decryptFieldWithDek(val, `svc_kyc_verifications.${col}.${r.id}`, dek) ?? undefined;
      }
      return decryptField(val, `svc_kyc_verifications.${col}.${r.id}`) ?? undefined;
    } catch (err: any) {
      log('error', `[piiCrypto] kyc ${col} decrypt failed`, { id: r.id, error: err?.message });
      return undefined;
    }
  };

  return {
    id: r.id,
    userId: r.user_id,
    requestedLevel: r.requested_level,
    currentLevel: r.current_level,
    status: r.status,
    provider: r.provider,
    providerApplicationId: r.provider_application_id,
    providerCheckId: r.provider_check_id,
    documents: decryptDocuments(r.documents),
    livenessCompleted: r.liveness_completed,
    livenessScore: r.liveness_score ? Number(r.liveness_score) : undefined,
    checks: parseJsonb(r.checks, []),
    overallScore: r.overall_score ? Number(r.overall_score) : undefined,
    riskLevel: r.risk_level,
    reviewedBy: r.reviewed_by,
    reviewNotes: decryptText(r.review_notes, 'review_notes'),
    consentGiven: r.consent_given,
    consentTimestamp: r.consent_timestamp ? new Date(r.consent_timestamp) : undefined,
    dataRetentionExpiry: r.data_retention_expiry ? new Date(r.data_retention_expiry) : undefined,
    createdAt: new Date(r.created_at),
    updatedAt: new Date(r.updated_at),
    completedAt: r.completed_at ? new Date(r.completed_at) : undefined,
    expiresAt: r.expires_at ? new Date(r.expires_at) : undefined,
  };
}

/**
 * Verify that required DB tables are reachable.
 * Replaces the old loadFromDb() — data is now read directly from the DB
 * on each request instead of being cached in Maps.
 */
async function verifyDbReady(): Promise<void> {
  if (!isDbAvailable()) {
    logger.warn('KYC DB not available — service running in degraded mode');
    return;
  }
  try {
    const result = await query(
      `SELECT COUNT(*) AS cnt FROM svc_kyc_verifications`
    );
    logger.info('KYC DB verified', { verifications: Number(result.rows[0]?.cnt ?? 0) });
  } catch (err: any) {
    let reason: string;
    try {
      reason = err?.message;
    } catch {
      reason = 'unreadable thrown value';
    }
    logger.warn('KYC DB verification query failed', { error: reason });
  }
}

// =============================================================================
// LOGGING
// =============================================================================

function log(level: 'info' | 'warn' | 'error', message: string, meta?: object) {
  const timestamp = new Date().toISOString();
  console.log(JSON.stringify({ timestamp, level, service: 'kyc', message, ...meta }));
}

// =============================================================================
// MIDDLEWARE
// =============================================================================

app.use(helmet());
app.use(cors({
  origin: process.env.CORS_ORIGINS?.split(',') || ['http://localhost:6100', 'http://localhost:6101'],
  credentials: true,
}));
// KS-1724: was `app.use(express.json({ limit: '10mb' }));`; the same options, plus the structural caps.
app.use(boundedJson({ service: 'kyc', limit: '10mb' })); // Allow larger payloads for images
app.use(rejectNulBytes()); // KS-471: no U+0000 may pass the boundary (raw-500 / persist class)

const requestLogger: RequestHandler = (req, res, next) => {
  const start = Date.now();
  res.on('finish', () => {
    log('info', 'Request completed', {
      method: req.method,
      path: req.path,
      statusCode: res.statusCode,
      duration: `${Date.now() - start}ms`,
    });
  });
  next();
};
app.use(requestLogger);

// =============================================================================
// VALIDATION SCHEMAS
// =============================================================================

const initiateVerificationSchema = z.object({
  userId: z.string().guid(),
  requestedLevel: z.enum(['NONE', 'BASIC', 'SOCIAL', 'STANDARD', 'ENHANCED', 'HIGH', 'GOVERNMENT']),
  consentGiven: z.boolean(),
  redirectUrl: z.string().url().optional(),
});

const submitDocumentSchema = z.object({
  verificationId: z.string().guid(),
  documentType: z.enum(['passport', 'driving_license', 'national_id', 'residence_permit', 'other']),
  country: z.string().length(2), // ISO 3166-1 alpha-2
  frontImage: z.string(), // Base64 encoded
  backImage: z.string().optional(),
});

const submitSelfieSchema = z.object({
  verificationId: z.string().guid(),
  selfieImage: z.string(), // Base64 encoded
});

const reviewVerificationSchema = z.object({
  status: z.enum(['approved', 'rejected']),
  reviewNotes: z.string().optional(),
  newLevel: z.enum(['NONE', 'BASIC', 'SOCIAL', 'STANDARD', 'ENHANCED', 'HIGH', 'GOVERNMENT']).optional(),
});

// =============================================================================
// ROUTES
// =============================================================================

// Pen-test H2 — every /api/* route below this point JWT-verifies the
// bearer token via @secuura/shared's `authenticate()`. Without this,
// downstream services trusted the gateway-injected x-user-* headers,
// which an attacker reaching a service directly (intra-cluster, leaked
// internal endpoint, etc.) could forge.
app.use('/api', jwtAuthenticate());

// Health check
app.get('/health', async (_req: Request, res: Response) => {
  const stats = await dbGetVerificationStats();
  res.json({
    status: 'healthy',
    service: 'kyc',
    version: '0.1.0',
    timestamp: new Date().toISOString(),
    provider: KYC_PROVIDER,
    stats: {
      totalVerifications: stats.total,
      pending: stats.pending,
      approved: stats.approved,
    },
  });
});

// Mount Microsoft Entra Verified ID routes
app.use('/api/kyc/microsoft', microsoftVerificationRoutes);

// API info
app.get('/api', (_req: Request, res: Response) => {
  res.json({
    service: 'Secuura KYC Service',
    version: '0.2.0',
    provider: KYC_PROVIDER,
    endpoints: {
      traditional: {
        'POST /api/kyc/initiate': 'Start KYC verification',
        'GET /api/kyc/:id': 'Get verification status',
        'GET /api/kyc/user/:userId': 'Get user verifications',
        'POST /api/kyc/:id/document': 'Submit identity document',
        'POST /api/kyc/:id/selfie': 'Submit selfie for liveness',
        'POST /api/kyc/:id/complete': 'Complete verification submission',
        'POST /api/kyc/:id/review': 'Admin: Review verification',
        'GET /api/kyc/:id/result': 'Get verification result',
      },
      microsoft: {
        'POST /api/kyc/microsoft/start': 'Start Microsoft Entra verification',
        'GET /api/kyc/microsoft/session/:sessionId': 'Get session status',
        'GET /api/kyc/microsoft/user/:userId/sessions': 'Get user sessions',
        'POST /api/kyc/microsoft/issue': 'Issue Secuura KYC credential',
        'GET /api/kyc/microsoft/result/:sessionId': 'Get verification result',
        'POST /api/kyc/microsoft/callback': 'Microsoft callback (internal)',
        'POST /api/kyc/microsoft/simulate/:sessionId': 'DEV: Simulate completion',
      },
      gdpr: {
        'POST /api/consent': 'Record user consent',
        'DELETE /api/consent/:id': 'Withdraw consent',
        'DELETE /api/kyc/user/:userId/data': 'Delete user data',
      },
    },
    verificationLevels: {
      BASIC: 'Email verification only',
      STANDARD: 'MFA enabled / Microsoft credential',
      ENHANCED: 'Federated identity (Microsoft Entra ID)',
      HIGH: 'Document + selfie + Face Check',
      GOVERNMENT: 'Government ID verification (eIDAS)',
    },
    microsoftFeatures: {
      verifiableCredentials: 'Accept and issue W3C Verifiable Credentials',
      faceCheck: 'Biometric face matching with liveness detection',
      linkedDomainVerification: 'Verify credential issuer domains',
      revocationCheck: 'Check credential revocation status',
    },
    supportedDocuments: ['passport', 'driving_license', 'national_id', 'residence_permit'],
  });
});

// AUDIT B-13: in-memory rate-limit on KYC verification endpoints. Identity-
// provider calls are downstream and burn third-party quota; without a cap an
// authenticated user can blow through the budget in seconds. 10 verifications
// per user per hour is the default per the audit recommendation. Keyed by
// JWT userId when present, falling back to IP. For multi-instance deploys,
// migrate to a Redis token bucket — flagged as an upgrade in BACKLOG.
const KYC_RATE_LIMIT_PER_HOUR = parseInt(process.env.KYC_RATE_LIMIT_PER_HOUR || '10', 10);
const kycHits = new Map<string, { count: number; resetAt: number }>();
const kycRateLimit: RequestHandler = (req: Request, res: Response, next: NextFunction): void => {
  const u = (req as Request & { user?: { userId?: string } }).user;
  const key = u?.userId || req.ip || 'unknown';
  const now = Date.now();
  const entry = kycHits.get(key);
  if (!entry || entry.resetAt < now) {
    kycHits.set(key, { count: 1, resetAt: now + 60 * 60 * 1000 });
    return next();
  }
  if (entry.count >= KYC_RATE_LIMIT_PER_HOUR) {
    const retryAfterSec = Math.ceil((entry.resetAt - now) / 1000);
    res.setHeader('Retry-After', String(retryAfterSec));
    res.status(429).json({
      success: false,
      error: { code: 'RATE_LIMIT_EXCEEDED', message: `Limit of ${KYC_RATE_LIMIT_PER_HOUR} per hour exceeded. Retry in ${retryAfterSec}s.`, retryAfterSec },
    });
    return;
  }
  entry.count += 1;
  next();
};

/**
 * POST /api/kyc/initiate
 * Start a new KYC verification
 */
app.post('/api/kyc/initiate', kycRateLimit, async (req: Request, res: Response, next: NextFunction) => {
  try {
    const data = initiateVerificationSchema.parse(req.body);
    
    if (!data.consentGiven) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Consent must be given to proceed with KYC' } });
    }
    
    const verificationId = uuidv4();
    
    // Get user's current verification level (mock)
    const currentLevel: VerificationLevel = 'BASIC';
    
    const verification: KYCVerification = {
      id: verificationId,
      userId: data.userId,
      requestedLevel: data.requestedLevel,
      currentLevel,
      status: 'pending',
      provider: KYC_PROVIDER,
      documents: [],
      livenessCompleted: false,
      checks: [],
      consentGiven: true,
      consentTimestamp: new Date(),
      dataRetentionExpiry: new Date(Date.now() + 365 * 24 * 60 * 60 * 1000), // 1 year
      createdAt: new Date(),
      updatedAt: new Date(),
      expiresAt: new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days to complete
    };
    
    // Initialize checks based on requested level
    if (data.requestedLevel === 'HIGH' || data.requestedLevel === 'GOVERNMENT') {
      verification.checks = [
        { id: uuidv4(), type: 'document', status: 'pending' },
        { id: uuidv4(), type: 'facial', status: 'pending' },
        { id: uuidv4(), type: 'liveness', status: 'pending' },
        { id: uuidv4(), type: 'watchlist', status: 'pending' },
      ];
      
      if (data.requestedLevel === 'GOVERNMENT') {
        verification.checks.push(
          { id: uuidv4(), type: 'pep', status: 'pending' },
          { id: uuidv4(), type: 'sanctions', status: 'pending' }
        );
      }
    }
    
    // For mock provider, create a mock provider application ID
    if (KYC_PROVIDER === 'mock') {
      verification.providerApplicationId = `mock_app_${crypto.randomBytes(8).toString('hex')}`;
    }
    
    // Store verification
    await dbSaveVerification(verification);
    
    // Record consent
    const consent: ConsentRecord = {
      id: uuidv4(),
      userId: data.userId,
      verificationId,
      consentType: 'data_processing',
      consentGiven: true,
      ipAddress: req.ip,
      userAgent: req.headers['user-agent'],
      timestamp: new Date(),
    };
    await dbSaveConsent(consent);
    
    log('info', 'KYC verification initiated', { 
      verificationId, 
      userId: data.userId,
      requestedLevel: data.requestedLevel,
    });
    
    res.status(201).json({
      success: true,
      data: {
        verificationId,
        status: verification.status,
        requestedLevel: verification.requestedLevel,
        requiredSteps: getRequiredSteps(verification.requestedLevel),
        expiresAt: verification.expiresAt,
        providerApplicationId: verification.providerApplicationId,
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: zod3Issues(error.issues) } });
    }
    next(error);
  }
});

/**
 * GET /api/kyc/:id
 * Get verification status
 */
app.get('/api/kyc/:id', async (req: Request, res: Response) => {
  const verification = await dbGetVerification(req.params.id);
  
  if (!verification) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Verification not found' } });
  }
  
  res.json({
    success: true,
    data: formatVerificationResponse(verification),
  });
});

/**
 * GET /api/kyc/user/:userId
 * Get all verifications for a user
 */
app.get('/api/kyc/user/:userId', async (req: Request, res: Response) => {
  const userVerifications = await dbGetVerificationsByUser(req.params.userId);
  const filteredVerifications = userVerifications
    .map(v => formatVerificationResponse(v));
  
  // Find the highest approved level
  const approvedLevels = filteredVerifications
    .filter(v => v.status === 'approved')
    .map(v => v.currentLevel);
  
  const levelOrder: VerificationLevel[] = ['NONE', 'BASIC', 'SOCIAL', 'STANDARD', 'ENHANCED', 'HIGH', 'GOVERNMENT'];
  const highestLevel = approvedLevels.reduce((highest, level) => {
    return levelOrder.indexOf(level) > levelOrder.indexOf(highest) ? level : highest;
  }, 'BASIC' as VerificationLevel);
  
  res.json({
    success: true,
    data: {
      userId: req.params.userId,
      currentLevel: highestLevel,
      verifications: filteredVerifications,
      count: filteredVerifications.length,
    },
  });
});

/**
 * POST /api/kyc/:id/document
 * Submit an identity document
 */
app.post('/api/kyc/:id/document', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const data = submitDocumentSchema.parse(req.body);
    const verification = await dbGetVerification(req.params.id);
    
    if (!verification) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Verification not found' } });
    }
    
    if (verification.status !== 'pending' && verification.status !== 'in_progress') {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `Cannot submit documents in ${verification.status} status` } });
    }
    
    // KS-487 B-4: verify the bytes BEFORE storing anything. Both images are
    // checked up front rather than as each is written, so a rejected back image
    // cannot leave an orphaned front image behind.
    const front = assertSupportedImage(data.frontImage);
    if (!front.ok) {
      return res.status(400).json({
        success: false,
        error: { code: 'INVALID_IMAGE', message: `frontImage: ${front.error}` },
      });
    }

    const back = data.backImage ? assertSupportedImage(data.backImage) : null;
    if (back && !back.ok) {
      return res.status(400).json({
        success: false,
        error: { code: 'INVALID_IMAGE', message: `backImage: ${back.error}` },
      });
    }

    // KS-386: the images are NOT stored. Each id records an attestation —
    // a verified image type submitted for this subject at this time.
    const frontImageId = uuidv4();
    await dbSaveImage(frontImageId, front.mimeType, verification.userId);

    let backImageId: string | undefined;
    if (back && back.ok) {
      backImageId = uuidv4();
      await dbSaveImage(backImageId, back.mimeType, verification.userId);
    }
    
    const document: VerificationDocument = {
      id: uuidv4(),
      type: data.documentType,
      country: data.country,
      frontImageId,
      backImageId,
      validationStatus: 'pending',
      uploadedAt: new Date(),
    };
    
    verification.documents.push(document);
    verification.status = 'in_progress';
    verification.updatedAt = new Date();
    await dbSaveVerification(verification);
    
    // In mock mode, simulate document extraction
    if (KYC_PROVIDER === 'mock') {
      // KS-849: this timer used to close over `verification` — the object as it was
      // at UPLOAD time — and write the WHOLE of it back when it fired. The store is
      // DB-only (see the helpers above: no in-memory Map), so every request rebuilds
      // its own object, and `dbSaveVerification` is a full upsert whose DO UPDATE SET
      // names liveness_completed, liveness_score and checks. A selfie arriving inside
      // this 1500 ms window therefore had its liveness result silently overwritten by
      // the stale copy. Re-read instead, so the write is made against whatever is in
      // the database NOW. The document is located by id because the re-read rebuilds
      // the documents array — the captured `document` reference is not in it.
      const verificationId = verification.id;
      const documentId = document.id;
      setTimeout(() => {
        void (async () => {
          const fresh = await dbGetVerification(verificationId);
          if (!fresh) return;
          const doc = fresh.documents.find(d => d.id === documentId);
          if (!doc) return;
          doc.extractedData = {
            fullName: 'John Doe',
            dateOfBirth: '1990-01-15',
            documentNumber: `DOC${require('crypto').randomInt(10_000_000, 99_999_999)}`,
            expiryDate: '2028-01-15',
            nationality: data.country,
          };
          doc.validationStatus = 'valid';

          // Update document check
          const docCheck = fresh.checks.find(c => c.type === 'document');
          if (docCheck) {
            docCheck.status = 'passed';
            docCheck.completedAt = new Date();
          }
          fresh.updatedAt = new Date();
          await dbSaveVerification(fresh);
        })().catch(() => {});
      }, 1500);
    }
    
    log('info', 'Document submitted', { 
      verificationId: verification.id, 
      documentType: data.documentType,
    });
    
    res.json({
      success: true,
      data: {
        documentId: document.id,
        status: document.validationStatus,
        message: 'Document submitted successfully. Processing...',
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: zod3Issues(error.issues) } });
    }
    next(error);
  }
});

/**
 * POST /api/kyc/:id/selfie
 * Submit selfie for liveness check
 */
app.post('/api/kyc/:id/selfie', async (req: Request, res: Response, next: NextFunction) => {
  try {
    const data = submitSelfieSchema.parse(req.body);
    const verification = await dbGetVerification(req.params.id);
    
    if (!verification) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Verification not found' } });
    }
    
    // KS-487 B-4: verify before storing, and before the mock liveness result
    // below asserts a pass. Previously a non-image string earned
    // `livenessCompleted: true, livenessScore: 0.95`.
    const selfie = assertSupportedImage(data.selfieImage);
    if (!selfie.ok) {
      return res.status(400).json({
        success: false,
        error: { code: 'INVALID_IMAGE', message: `selfieImage: ${selfie.error}` },
      });
    }

    // KS-386: attestation only — the selfie bytes are sniffed and not stored.
    const selfieImageId = uuidv4();
    await dbSaveImage(selfieImageId, selfie.mimeType, verification.userId);
    
    // In mock mode, simulate liveness check
    if (KYC_PROVIDER === 'mock') {
      verification.livenessCompleted = true;
      verification.livenessScore = 0.95;
      
      // Update facial and liveness checks
      const facialCheck = verification.checks.find(c => c.type === 'facial');
      if (facialCheck) {
        facialCheck.status = 'passed';
        facialCheck.completedAt = new Date();
      }
      
      const livenessCheck = verification.checks.find(c => c.type === 'liveness');
      if (livenessCheck) {
        livenessCheck.status = 'passed';
        livenessCheck.completedAt = new Date();
      }
    }
    
    verification.updatedAt = new Date();
    await dbSaveVerification(verification);
    
    log('info', 'Selfie submitted', { verificationId: verification.id });
    
    res.json({
      success: true,
      data: {
        livenessCompleted: verification.livenessCompleted,
        livenessScore: verification.livenessScore,
        message: 'Selfie submitted successfully.',
      },
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: zod3Issues(error.issues) } });
    }
    next(error);
  }
});

/**
 * POST /api/kyc/:id/complete
 * Complete the verification submission
 */
app.post('/api/kyc/:id/complete', async (req: Request, res: Response) => {
  const verification = await dbGetVerification(req.params.id);
  
  if (!verification) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Verification not found' } });
  }
  
  // Check if all required steps are completed
  const hasDocument = verification.documents.length > 0;
  const hasLiveness = verification.livenessCompleted;
  
  if (verification.requestedLevel === 'HIGH' || verification.requestedLevel === 'GOVERNMENT') {
    if (!hasDocument) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Document submission required' } });
    }
    if (!hasLiveness) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Selfie/liveness check required' } });
    }
  }
  
  verification.status = 'under_review';
  verification.updatedAt = new Date();
  await dbSaveVerification(verification);
  
  // In mock mode, auto-approve after delay
  if (KYC_PROVIDER === 'mock') {
    // KS-849: the same stale-write class as the document timer above, with a window
    // twice as long and a heavier payload. This one writes status='approved' plus
    // currentLevel, overallScore, riskLevel and completedAt, so ANY write landing in
    // these 3000 ms — including an admin decision through POST /api/kyc/:id/review —
    // was overwritten by an approval. Re-read before mutating.
    const verificationId = verification.id;
    setTimeout(() => {
      void (async () => {
        const fresh = await dbGetVerification(verificationId);
        if (!fresh) return;
        // Complete remaining checks
        fresh.checks.forEach(check => {
          if (check.status === 'pending') {
            check.status = 'passed';
            check.completedAt = new Date();
          }
        });

        fresh.status = 'approved';
        fresh.currentLevel = fresh.requestedLevel;
        fresh.overallScore = 0.92;
        fresh.riskLevel = 'low';
        fresh.completedAt = new Date();
        fresh.updatedAt = new Date();

        await dbSaveVerification(fresh);
        log('info', 'KYC verification approved (mock)', { verificationId: fresh.id });
      })().catch(() => {});
    }, 3000);
  }
  
  log('info', 'KYC verification submitted for review', { verificationId: verification.id });
  
  res.json({
    success: true,
    data: {
      verificationId: verification.id,
      status: verification.status,
      message: 'Verification submitted for review. You will be notified of the result.',
    },
  });
});

/** KS-1845 (gate 42 F1): a user id in the form used to compare two ids; '' when it is missing, empty or not a string. */
const foldedUserId = (id: unknown): string => (typeof id === 'string' ? id.toLowerCase() : '');

/**
 * POST /api/kyc/:id/review
 * Admin: Review and approve/reject verification
 */
app.post('/api/kyc/:id/review', async (req: Request, res: Response, next: NextFunction) => {
  try {
    // KS-1845: reviewing decides a verification and sets its level (up to GOVERNMENT), so only a platform
    // reviewer may do it: the shared isPlatformRole (SYSTEM_ADMIN / SUPER_ADMIN, ASCII case fold only). Before,
    // no role was checked and any signed-in caller could approve, though the spec declares 403 'Reviewer role
    // required'. It runs before the body or the id is read, so a refused caller learns neither.
    if (!isPlatformRole((req as any).user?.role)) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Reviewer role required' } });
    }
    const data = reviewVerificationSchema.parse(req.body);
    const verification = await dbGetVerification(req.params.id);
    // Pen-test F-04: read from authenticated req.user (set by authenticate()
    // middleware), NOT from raw headers. Direct header reads are spoofable.
    const reviewerId = ((req as any).user?.userId as string) || 'admin';
    
    if (!verification) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Verification not found' } });
    }
    
    // KS-1845: a reviewer may not decide their own verification, even as a platform administrator. Before,
    // nothing compared the reviewer with the verification's subject. This check refuses on EQUALITY, so a
    // strict compare fails open on any spelling difference: z.string().uuid() admits upper case and user_id
    // is TEXT, so a row can hold the reviewer's own id in another case (gate 42 F1). Both ids are folded, and
    // an id that is missing or not a string cannot be shown to be someone else's, so it is refused too.
    const reviewerKey = foldedUserId((req as any).user?.userId);
    const subjectKey = foldedUserId(verification.userId);
    if (!reviewerKey || !subjectKey || reviewerKey === subjectKey) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: 'Reviewer role required' } });
    }

    if (verification.status !== 'under_review') {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: `Cannot review verification in ${verification.status} status` } });
    }
    
    verification.status = data.status;
    verification.reviewedBy = reviewerId;
    verification.reviewNotes = data.reviewNotes;
    verification.completedAt = new Date();
    verification.updatedAt = new Date();
    
    if (data.status === 'approved') {
      verification.currentLevel = data.newLevel || verification.requestedLevel;
    }
    
    await dbSaveVerification(verification);
    
    log('info', 'KYC verification reviewed', { 
      verificationId: verification.id, 
      status: data.status,
      reviewedBy: reviewerId,
    });
    
    res.json({
      success: true,
      data: formatVerificationResponse(verification),
    });
  } catch (error) {
    if (error instanceof z.ZodError) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Validation failed', details: zod3Issues(error.issues) } });
    }
    next(error);
  }
});

/**
 * GET /api/kyc/:id/result
 * Get verification result
 */
app.get('/api/kyc/:id/result', async (req: Request, res: Response) => {
  const verification = await dbGetVerification(req.params.id);
  
  if (!verification) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Verification not found' } });
  }
  
  if (verification.status !== 'approved' && verification.status !== 'rejected') {
    return res.json({
      success: true,
      data: {
        status: verification.status,
        message: 'Verification is still in progress.',
      },
    });
  }
  
  res.json({
    success: true,
    data: {
      verified: verification.status === 'approved',
      level: verification.currentLevel,
      overallScore: verification.overallScore,
      riskLevel: verification.riskLevel,
      checks: verification.checks.map(c => ({
        type: c.type,
        status: c.status,
        completedAt: c.completedAt,
      })),
      completedAt: verification.completedAt,
    },
  });
});

/**
 * DELETE /api/kyc/user/:userId/data
 * GDPR: Delete user KYC data
 */
app.delete('/api/kyc/user/:userId/data', async (req: Request, res: Response) => {
  const deletedCount = await dbDeleteUserData(req.params.userId);

  log('info', 'User KYC data deleted (GDPR)', { userId: req.params.userId });

  res.json({
    success: true,
    message: 'All KYC data for user has been deleted.',
    deletedVerifications: deletedCount,
  });
});

// =============================================================================
// HELPER FUNCTIONS
// =============================================================================

function formatVerificationResponse(verification: KYCVerification) {
  return {
    id: verification.id,
    userId: verification.userId,
    requestedLevel: verification.requestedLevel,
    currentLevel: verification.currentLevel,
    status: verification.status,
    provider: verification.provider,
    documentsSubmitted: verification.documents.length,
    livenessCompleted: verification.livenessCompleted,
    checks: verification.checks.map(c => ({
      type: c.type,
      status: c.status,
    })),
    overallScore: verification.overallScore,
    riskLevel: verification.riskLevel,
    createdAt: verification.createdAt,
    updatedAt: verification.updatedAt,
    completedAt: verification.completedAt,
    expiresAt: verification.expiresAt,
  };
}

function getRequiredSteps(level: VerificationLevel): string[] {
  switch (level) {
    case 'BASIC':
      return ['email_verification'];
    case 'STANDARD':
      return ['email_verification', 'mfa_setup'];
    case 'ENHANCED':
      return ['federated_login'];
    case 'HIGH':
      return ['document_upload', 'selfie_liveness'];
    case 'GOVERNMENT':
      return ['document_upload', 'selfie_liveness', 'address_verification', 'pep_screening'];
    default:
      return [];
  }
}

// =============================================================================
// ERROR HANDLING
// =============================================================================

app.use((_req: Request, res: Response) => {
  res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'Not Found' } });
});

// KS-111: route errors through the shared AppError-aware handler (maps
// AppError.statusCode + Zod -> 4xx; emits the canonical {success,error} shape).
app.use(errorHandler);

// =============================================================================
// START SERVER
// =============================================================================

initDb().then(async (connected) => {
  console.log('[KYC] DB init:', connected);
  if (connected) {
    await verifyDbReady();
  }
});

// Audit 1.3 phase 4b: PII encryption for documents + review_notes. Init the
// keyring before the cascade subscriber starts so any handler-time decrypt
// is ready.
if (process.env.PII_ENCRYPTION_KEY) {
  try {
    initPiiCrypto();
    log('info', 'PII encryption keyring initialised');
  } catch (err: any) {
    log('warn', 'PII encryption init failed (KYC will store plaintext until fixed)', { error: err?.message });
  }
} else if (process.env.NODE_ENV === 'production') {
  log('error', 'FATAL: PII_ENCRYPTION_KEY missing in production — refusing to start');
  process.exit(1);
} else {
  log('warn', 'PII_ENCRYPTION_KEY not set — KYC writes will store plaintext');
}

// Audit 2.2: cascade subscriber for GDPR user.erased events from originate
import { startUserErasedSubscriber } from './userErasedSubscriber';
// KS-1725: zod 4 issues rendered in zod 3.25.76's shape for every response (the client contract unchanged).
import { zod3Issues } from '@secuura/shared/zod3-compat';
startUserErasedSubscriber(log, dbDeleteUserData).catch((err) => {
  log('warn', '[cascade] failed to start user.erased subscriber', { error: err?.message });
});

const server = app.listen(PORT, () => {
  log('info', 'KYC Service started', { port: PORT, provider: KYC_PROVIDER });
  console.log(`
╔═══════════════════════════════════════════════════════════════╗
║                  SECUURA KYC SERVICE                          ║
╠═══════════════════════════════════════════════════════════════╣
║  Port:      ${PORT}                                              ║
║  Provider:  ${KYC_PROVIDER.padEnd(44)}║
║  API Info:  http://localhost:${PORT}/api                          ║
╠═══════════════════════════════════════════════════════════════╣
║  Verification Levels:                                         ║
║    • BASIC:      Email verification                          ║
║    • STANDARD:   MFA / Microsoft credential                  ║
║    • ENHANCED:   Federated identity (Entra ID)              ║
║    • HIGH:       Document + selfie + Face Check             ║
║    • GOVERNMENT: eIDAS / Gov ID verification                 ║
╠═══════════════════════════════════════════════════════════════╣
║  Microsoft Entra Verified ID:                                 ║
║    • Verifiable Credentials (W3C standard)                   ║
║    • Face Check (biometric matching)                         ║
║    • Linked Domain Verification                              ║
║    • Credential Issuance & Presentation                      ║
╚═══════════════════════════════════════════════════════════════╝
`);
});

// KS-252: hold keep-alive sockets longer than any upstream proxy's idle
// window (gateway http-proxy-middleware / nginx / ACA envoy reuse pooled
// sockets; Node's 5 s default close races their reuse -> ECONNRESET and
// 19-29 s stalls under load). headersTimeout must exceed keepAliveTimeout.
server.keepAliveTimeout = 65_000;
server.headersTimeout = 66_000;

export default app;
