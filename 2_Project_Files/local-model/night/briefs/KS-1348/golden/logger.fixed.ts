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

// File transports for production
// KS-1348: each File transport carries its own json() format, as the Console transport does. The
// logger-level format renders nothing, so without it every line written was the literal undefined.
if (nodeEnv === 'production') {
  transports.push(
    new winston.transports.File({ filename: 'logs/error.log', level: 'error', format: combine(json()), maxsize: 10_000_000, maxFiles: 5 }),
    new winston.transports.File({ filename: 'logs/combined.log', format: combine(json()), maxsize: 10_000_000, maxFiles: 5 }),
  );
}

export const logger = winston.createLogger({
  level: process.env.LOG_LEVEL || (nodeEnv === 'production' ? 'info' : 'debug'),
  defaultMeta: { service: 'originate' },
  format: combine(
    errors({ stack: true }),
    timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' }),
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
