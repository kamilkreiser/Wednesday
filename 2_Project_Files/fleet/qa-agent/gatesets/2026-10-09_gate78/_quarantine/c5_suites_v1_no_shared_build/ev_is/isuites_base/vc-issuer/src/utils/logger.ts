import winston from 'winston';

const { combine, timestamp, printf, colorize, json, errors } = winston.format;

const devFormat = printf(({ level, message, timestamp, service, ...meta }) => {
  const metaStr = Object.keys(meta).length ? ` ${JSON.stringify(meta)}` : '';
  return `${timestamp} [${service || 'app'}] ${level}: ${message}${metaStr}`;
});

export function createLogger(serviceName: string): winston.Logger {
  const isProduction = process.env.NODE_ENV === 'production';
  const logLevel = process.env.LOG_LEVEL || (isProduction ? 'info' : 'debug');
  return winston.createLogger({
    level: logLevel,
    defaultMeta: { service: serviceName },
    format: combine(errors({ stack: true }), timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' })),
    transports: [
      new winston.transports.Console({
        format: isProduction ? combine(json()) : combine(colorize(), devFormat),
      }),
    ],
  });
}

export const logger = createLogger('vc-issuer');
