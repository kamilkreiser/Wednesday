"use strict";
/**
 * =============================================================================
 * ISSUER CERT SWEEP — KS-83 PR 2
 * =============================================================================
 * Periodic background job that:
 *   1. Flips active certs whose validUntil has passed → status='expired'
 *      and emits ISSUER_CERT_EXPIRED for each.
 *   2. Finds active certs expiring in T-30 / T-7 / T-1 days and emits
 *      ISSUER_CERT_EXPIRING_SOON for each.
 *
 * Subscribers (downstream services / future): notification service for
 * email/Slack pings to issuer admins; admin portal for the cert health
 * widget; audit-log retention for the immutable expiry record.
 *
 * Schedule: every 6h. The sweep is cheap (single UPDATE + 3 windowed
 * SELECTs), runs cross-tenant (RLS permissive when GUC unset), and is
 * idempotent — flipping an already-expired cert does nothing, the
 * expiring-soon window is small enough that we won't double-fire on
 * a daily cycle.
 *
 * Run-at-startup: yes — covers the case where the service was down
 * for a few hours and missed a tick. Subsequent ticks then run on
 * the interval.
 *
 * Dev/test mode: callers can pass an interval of 0 to disable the
 * timer (the sweep methods are still callable directly for tests).
 * =============================================================================
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.runIssuerCertSweep = runIssuerCertSweep;
exports.startIssuerCertSweep = startIssuerCertSweep;
exports.stopIssuerCertSweep = stopIssuerCertSweep;
const logger_1 = require("../utils/logger");
const events_1 = require("../events");
const issuerCertRepo_1 = require("../repositories/issuerCertRepo");
const shared_1 = require("@secuura/shared");
const DEFAULT_INTERVAL_MS = 6 * 60 * 60 * 1000; // 6h
const EXPIRING_SOON_WINDOWS_DAYS = [30, 7, 1];
let sweepTimer = null;
/**
 * One full sweep — exposed for direct test invocation. Returns counts
 * for log assertions.
 */
async function runIssuerCertSweep() {
    // KS-458: scheduled maintenance sweep across every tenant's issuer_certs —
    // a deliberate cross-tenant background path, so it runs under the
    // platform scope (fail-closed RLS would otherwise silently sweep nothing).
    return (0, shared_1.runWithPlatformScope)(() => runIssuerCertSweepInner());
}
async function runIssuerCertSweepInner() {
    const counts = { expired: 0, expiringSoon: {} };
    // 1. Flip any cert past validUntil → expired + emit events
    let expiredRows = [];
    try {
        expiredRows = await (0, issuerCertRepo_1.markExpiredCerts)();
    }
    catch (err) {
        logger_1.logger.error('Issuer cert sweep: markExpiredCerts failed', {
            error: err instanceof Error ? err.message : String(err),
        });
        // Continue to the expiring-soon checks even if the flip failed —
        // they're independent and we don't want one DB blip to mask both.
    }
    counts.expired = expiredRows.length;
    for (const row of expiredRows) {
        (0, events_1.publishEvent)(events_1.EventTypes.ISSUER_CERT_EXPIRED, {
            certId: row.id,
            tenantId: row.tenantId,
            fingerprintSha256: row.fingerprintSha256,
            name: row.name,
            validUntil: row.validUntil.toISOString(),
        }).catch((err) => logger_1.logger.warn('publishEvent ISSUER_CERT_EXPIRED failed', {
            certId: row.id,
            error: err instanceof Error ? err.message : String(err),
        }));
    }
    // 2. Expiring-soon windows (T-30, T-7, T-1)
    for (const days of EXPIRING_SOON_WINDOWS_DAYS) {
        let rows = [];
        try {
            rows = await (0, issuerCertRepo_1.findExpiringSoon)(days);
        }
        catch (err) {
            logger_1.logger.error(`Issuer cert sweep: findExpiringSoon(${days}d) failed`, {
                error: err instanceof Error ? err.message : String(err),
            });
            continue;
        }
        counts.expiringSoon[days] = rows.length;
        for (const row of rows) {
            (0, events_1.publishEvent)(events_1.EventTypes.ISSUER_CERT_EXPIRING_SOON, {
                certId: row.id,
                tenantId: row.tenantId,
                fingerprintSha256: row.fingerprintSha256,
                name: row.name,
                validUntil: row.validUntil.toISOString(),
                daysRemaining: days,
            }).catch((err) => logger_1.logger.warn('publishEvent ISSUER_CERT_EXPIRING_SOON failed', {
                certId: row.id,
                daysRemaining: days,
                error: err instanceof Error ? err.message : String(err),
            }));
        }
    }
    if (counts.expired > 0 || Object.values(counts.expiringSoon).some((n) => n > 0)) {
        logger_1.logger.info('Issuer cert sweep complete', counts);
    }
    else {
        logger_1.logger.debug('Issuer cert sweep complete (nothing to do)', counts);
    }
    return counts;
}
/**
 * Start the periodic sweep. Idempotent — calling start twice doesn't
 * stack timers. Call `stopIssuerCertSweep()` for clean shutdown / tests.
 *
 * Set ISSUER_CERT_SWEEP_INTERVAL_MS=0 to disable the timer entirely
 * (useful for tests + ephemeral envs that don't want the background
 * load). The first sweep still runs at startup unless the env var is
 * the literal string 'disabled'.
 */
function startIssuerCertSweep(intervalMs = DEFAULT_INTERVAL_MS) {
    if (sweepTimer) {
        logger_1.logger.debug('Issuer cert sweep already running; not restarting');
        return;
    }
    const envInterval = process.env.ISSUER_CERT_SWEEP_INTERVAL_MS;
    if (envInterval === 'disabled') {
        logger_1.logger.info('Issuer cert sweep disabled via ISSUER_CERT_SWEEP_INTERVAL_MS=disabled');
        return;
    }
    const effectiveInterval = envInterval ? parseInt(envInterval, 10) : intervalMs;
    // Run once at startup so any cert that expired while the service was
    // down gets caught immediately. Errors are logged inside runIssuerCertSweep.
    runIssuerCertSweep().catch((err) => logger_1.logger.error('Initial issuer cert sweep failed', {
        error: err instanceof Error ? err.message : String(err),
    }));
    if (effectiveInterval > 0) {
        sweepTimer = setInterval(() => {
            runIssuerCertSweep().catch((err) => logger_1.logger.error('Scheduled issuer cert sweep failed', {
                error: err instanceof Error ? err.message : String(err),
            }));
        }, effectiveInterval);
        logger_1.logger.info('Issuer cert sweep scheduled', { intervalMs: effectiveInterval });
    }
    else {
        logger_1.logger.info('Issuer cert sweep ran once at startup; periodic timer disabled');
    }
}
function stopIssuerCertSweep() {
    if (sweepTimer) {
        clearInterval(sweepTimer);
        sweepTimer = null;
    }
}
