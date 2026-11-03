/**
 * =============================================================================
 * LOGGER — Auth Service
 * =============================================================================
 * Standalone logger (identical to @secuura/shared createLogger).
 * Kept as standalone for Docker build compatibility — workspace packages
 * are not available in standalone Docker builds.
 * =============================================================================
 */

import winston from 'winston';

const { combine, timestamp, printf, colorize, json, errors } = winston.format;

const devFormat = printf(({ level, message, timestamp, service, ...meta }) => {
  const metaStr = Object.keys(meta).length ? ` ${JSON.stringify(meta)}` : '';
  return `${timestamp} [${service || 'auth'}] ${level}: ${message}${metaStr}`;
});

export function createLogger(serviceName: string): winston.Logger {
  const isProduction = process.env.NODE_ENV === 'production';
  const logLevel = process.env.LOG_LEVEL || (isProduction ? 'info' : 'debug');

  return winston.createLogger({
    level: logLevel,
    defaultMeta: { service: serviceName },
    format: combine(
      errors({ stack: true }),
      timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' })
    ),
    transports: [
      new winston.transports.Console({
        format: isProduction
          ? combine(json())
          : combine(colorize(), devFormat),
      }),
    ],
  });
}

export const logger = createLogger('auth');

/**
 * Validate critical environment variables at startup.
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
