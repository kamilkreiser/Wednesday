"use strict";
/**
 * =============================================================================
 * LOGGER — Auth Service
 * =============================================================================
 * Standalone logger (identical to @secuura/shared createLogger).
 * Kept as standalone for Docker build compatibility — workspace packages
 * are not available in standalone Docker builds.
 * =============================================================================
 */
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.logger = void 0;
exports.createLogger = createLogger;
exports.validateEnv = validateEnv;
const winston_1 = __importDefault(require("winston"));
const { combine, timestamp, printf, colorize, json, errors } = winston_1.default.format;
const devFormat = printf(({ level, message, timestamp, service, ...meta }) => {
    const metaStr = Object.keys(meta).length ? ` ${JSON.stringify(meta)}` : '';
    return `${timestamp} [${service || 'auth'}] ${level}: ${message}${metaStr}`;
});
function createLogger(serviceName) {
    const isProduction = process.env.NODE_ENV === 'production';
    const logLevel = process.env.LOG_LEVEL || (isProduction ? 'info' : 'debug');
    return winston_1.default.createLogger({
        level: logLevel,
        defaultMeta: { service: serviceName },
        format: combine(errors({ stack: true }), timestamp({ format: 'YYYY-MM-DD HH:mm:ss.SSS' })),
        transports: [
            new winston_1.default.transports.Console({
                format: isProduction
                    ? combine(json())
                    : combine(colorize(), devFormat),
            }),
        ],
    });
}
exports.logger = createLogger('auth');
/**
 * Validate critical environment variables at startup.
 */
function validateEnv() {
    const dbUrl = process.env.DATABASE_URL || '';
    if (process.env.NODE_ENV === 'production') {
        if (dbUrl.includes('secuura_dev_password')) {
            exports.logger.error('FATAL: DATABASE_URL uses dev password — refusing to start in production');
            process.exit(1);
        }
    }
    else {
        if (dbUrl.includes('secuura_dev_password')) {
            exports.logger.warn('DATABASE_URL uses development default — change before deploying to production');
        }
    }
}
