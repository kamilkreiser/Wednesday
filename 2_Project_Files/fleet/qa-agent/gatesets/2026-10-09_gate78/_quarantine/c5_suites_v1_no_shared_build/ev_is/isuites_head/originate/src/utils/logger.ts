/**
 * =============================================================================
 * STRUCTURED WINSTON LOGGER — Originate Service
 * =============================================================================
 * Replaces console.log with structured, level-based logging.
 * - Development: colorized, human-readable format
 * - Production: JSON format with file transports
 * - Errors >= 500 are automatically persisted to system_errors table
 * =============================================================================
 */

import winston from 'winston';

// KS-727: this module deliberately does NOT import `../config`. It used it for
// exactly one value — `config.nodeEnv`, defined as
// `process.env.NODE_ENV || 'development'` — while `config` ALSO throws at
// module load when `DATABASE_URL` is unset. That made a LOGGER un-importable
// without a database URL, and with it every module that logs, including
// `../middleware/errorHandler`. The KS-727 class guard imports that handler
// directly and treats an unimportable module as a FAILED run (by design: a
// handler must never drop out of the corpus silently), so the coupling had to
// go. The read below is byte-for-byte what `config.nodeEnv` evaluated to.
const nodeEnv = process.env.NODE_ENV || 'development';

const { combine, timestamp, printf, colorize, json, errors } = winston.format;

const devFormat = printf(({ level, message, timestamp: ts, service, ...meta }) => {
  const metaStr = Object.keys(meta).length > 0
    ? ` ${JSON.stringify(meta, null, 0)}`
    : '';
  return `${ts} [${service || 'originate'}] ${level}: ${message}${metaStr}`;
});

const transports: winston.transport[] = [
  new winston.transports.Console({
    format: nodeEnv === 'production'
      ? combine(json())
      : combine(colorize(), devFormat),
  }),
];

// KS-1348: the Console first passes through this logger-level redaction. The VALUE of any key
// naming a secret or PII field is replaced by [REDACTED], at any depth: the packages/shared logger
// list, matched case-insensitively on the key ending, so recipientEmail and accessToken match too.
const SENSITIVE_LOG_KEY = /(password|passwd|secret|token|apikey|api_key|api-key|authorization|cookie|ssn|email|creditcard|phonenumber)$/i;

function redactLogValue(key: string, value: unknown, depth: number): unknown {
  if (SENSITIVE_LOG_KEY.test(key)) return '[REDACTED]';
  if (value === null || typeof value !== 'object' || value instanceof Error || value instanceof Date || ArrayBuffer.isView(value)) return value;
  if (depth >= 10) return '[TRUNCATED]';
  if (Array.isArray(value)) return value.map((item) => redactLogValue('', item, depth + 1));
  const copy: Record<string, unknown> = {};
  for (const [k, v] of Object.entries(value)) copy[k] = redactLogValue(k, v, depth + 1);
  return copy;
}

const redactSecrets = winston.format((info) => {
  const copy = { ...info };
  for (const key of Object.keys(copy)) {
    if (key !== 'level' && key !== 'message') copy[key] = redactLogValue(key, copy[key], 0);
  }
  return copy;
});

// KS-1348 r3 (Kam ruled 2026-09-28: allow-list the file format): the production log FILES are a
// closed world. They record ONLY these named fields, when each is a string or a number, plus the
// error text when it is a string. Every other key a caller logs, under any name and at any depth,
// nested Errors included, stays out of the files. The Console keeps the redacted line above.
const FILE_LOG_FIELDS = ['timestamp', 'level', 'service', 'message', 'requestId', 'method', 'path', 'statusCode'];

const keepFileFields = winston.format((info) => {
  const kept: Record<string, unknown> = {};
  for (const key of FILE_LOG_FIELDS) {
    if (typeof info[key] === 'string' || typeof info[key] === 'number') kept[key] = info[key];
  }
  if (typeof info.error === 'string') kept.error = info.error;
  return kept as winston.Logform.TransformableInfo;
});

// File transports for production
if (nodeEnv === 'production') {
  transports.push(
    new winston.transports.File({ filename: 'logs/error.log', level: 'error', format: combine(keepFileFields(), json()), maxsize: 10_000_000, maxFiles: 5 }),
    new winston.transports.File({ filename: 'logs/combined.log', format: combine(keepFileFields(), json()), maxsize: 10_000_000, maxFiles: 5 }),
  );
}

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || (nodeEnv === 'production' ? 'info' : 'debug'),
  defaultMeta: { service: 'originate' },
  format: combine(
    errors({ stack: true }),
    timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }),
    redactSecrets(),
  ),
  transports,
});

/**
 * Validate critical environment variables at startup.
 * Warns in development, blocks startup in production if insecure defaults detected.
 */
export function validateEnv(): void {
  const dbUrl = process.env.DATABASE_URL || '';

  if (process.env.NODE_ENV === 'production') {
    if (dbUrl.includes('secuura_dev_password')) {
      logger.error('FATAL: DATABASE_URL uses dev password — refusing to start in production');
      process.exit(1);
    }
  } else {
    if (dbUrl.includes('secuura_dev_password')) {
      logger.warn('DATABASE_URL uses development default — change before deploying to production');
    }
  }
}
