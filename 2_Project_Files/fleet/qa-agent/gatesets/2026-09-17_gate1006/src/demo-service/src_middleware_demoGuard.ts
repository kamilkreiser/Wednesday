/**
 * =============================================================================
 * DEMO GUARD — DEMO SERVICE (KS-641)
 * =============================================================================
 * demo-service mints REAL platform tokens without asking the caller for a
 * credential: POST /demo-api/persona/switch authenticates server-side as one
 * of four seeded personas — including `admin@secuura.io`, role Platform Admin
 * — and proxies the httpOnly refresh cookie back. POST /demo-api/reset runs a
 * pg_restore plus a Redis FLUSHALL behind nothing but an `X-Demo-Reset`
 * header, which is an accidental-trigger guard rather than an access control.
 *
 * Until now the service was held shut only by three incidental barriers (the
 * gateway location block deleted under F-09, the host port unpublished under
 * pen-test F-04, and the personas unseeded). None of the three is an access
 * control, each was introduced for an unrelated reason, and ANY ONE of them
 * being reverted re-opens an unauthenticated admin-token endpoint.
 *
 * This module supplies the two controls the service never had:
 *
 *   1. `assertDemoServiceEnabled()` — a boot-time, fail-closed gate. The
 *      service refuses to start in production at all, refuses to start
 *      without an explicit opt-in, and refuses to start without a usable
 *      shared key. Mirrors the PII_ENCRYPTION_KEY pattern already used by
 *      auth / kyc / security / m365-integration.
 *
 *   2. `requireDemoKey` — inbound auth on every route except /health.
 *
 * WHY A SHARED KEY AND NOT A JWT. The only caller is the demo overlay, a
 * browser bundle with no credential of its own, and persona/switch is the
 * route that mints the FIRST token — so requiring a platform JWT to obtain a
 * platform JWT is circular. A secret baked into a public demo bundle is not a
 * secret either. The achievable control is a key held by the gateway and
 * injected server-side, so the service refuses anything that did not arrive
 * through the demo gateway. Nothing routes /demo-api/ today (both confs), so
 * this breaks no live caller; whoever restores the location block must also
 * inject the header, which is the correct coupling — re-routing it forces you
 * to confront the credential.
 * =============================================================================
 */

import { Request, Response, NextFunction } from 'express';
import { createHash, timingSafeEqual } from 'node:crypto';

// A key short enough to guess is not a key. 16 chars is the floor, not advice.
export const MIN_DEMO_KEY_LENGTH = 16;

// Distinctness floor, not an entropy estimate — see the check in
// assertDemoServiceEnabled(). `openssl rand -hex 32` yields 16 by construction.
export const MIN_DEMO_KEY_DISTINCT_CHARS = 8;

/**
 * Boot-time gate. Throws with an operator-readable reason; the caller is
 * expected to log FATAL and exit non-zero. Fails CLOSED in every branch —
 * a missing key refuses to start rather than running without a guard.
 */
export function assertDemoServiceEnabled(): void {
  // KS-641 (#737 review): an UNSET NODE_ENV used to default to 'development' and
  // sail past this branch, so the one gate named "never production" was not
  // strictly fail-closed. An environment that has not said what it is does not
  // get the benefit of the doubt from a service that mints Platform Admin tokens.
  const nodeEnv = process.env.NODE_ENV;

  if (nodeEnv === undefined || nodeEnv === '') {
    throw new Error(
      'NODE_ENV is not set. demo-service mints Platform Admin tokens without a ' +
        'caller credential and will not start in an environment that has not ' +
        'declared itself non-production. Set NODE_ENV explicitly.',
    );
  }

  if (nodeEnv === 'production') {
    throw new Error(
      'demo-service must never run in production — it mints Platform Admin tokens ' +
        'without a caller credential. Refusing to start (NODE_ENV=production).',
    );
  }

  if (process.env.DEMO_SERVICE_ENABLED !== 'true') {
    throw new Error(
      'DEMO_SERVICE_ENABLED must be exactly "true" to run demo-service. ' +
        'This is a deliberate opt-in, not a default — refusing to start.',
    );
  }

  const key = process.env.DEMO_SERVICE_KEY ?? '';

  if (key.length < MIN_DEMO_KEY_LENGTH) {
    throw new Error(
      `DEMO_SERVICE_KEY must be set and at least ${MIN_DEMO_KEY_LENGTH} characters ` +
        `(got ${key.length}). Without it every /demo-api route is unauthenticated — ` +
        'refusing to start rather than running open.',
    );
  }

  // KS-641 (#737 review): length is not entropy — `aaaaaaaaaaaaaaaa` cleared the
  // floor above. This is a cheap distinctness check, NOT an entropy estimate: it
  // rejects the degenerate keys a human types when asked for "16 characters",
  // and nothing more. bootstrap-env.sh generates `openssl rand -hex 32`, which
  // has 16 distinct characters by construction.
  const distinct = new Set(key).size;
  if (distinct < MIN_DEMO_KEY_DISTINCT_CHARS) {
    throw new Error(
      `DEMO_SERVICE_KEY has only ${distinct} distinct characters (minimum ` +
        `${MIN_DEMO_KEY_DISTINCT_CHARS}). A repeated-character string is long, not ` +
        'secret — refusing to start. Generate one with `openssl rand -hex 32`.',
    );
  }
}

/** Length-independent comparison — hashing first avoids leaking key length. */
function safeEqual(provided: string, expected: string): boolean {
  if (!expected) return false; // fail closed if the key vanished after boot
  const a = createHash('sha256').update(provided).digest();
  const b = createHash('sha256').update(expected).digest();
  return timingSafeEqual(a, b);
}

/**
 * Inbound auth for /demo-api. 401 when no key is presented, 403 when a wrong
 * one is. Short-circuits BEFORE the handler, so an anonymous caller never
 * drives credentialed traffic at the auth service.
 */
export function requireDemoKey(req: Request, res: Response, next: NextFunction): void {
  const expected = process.env.DEMO_SERVICE_KEY ?? '';
  const provided = req.header('x-demo-key');

  if (!provided) {
    res.status(401).json({
      success: false,
      error: {
        code: 'UNAUTHORIZED',
        message: 'Missing X-Demo-Key header. /demo-api is not a public surface.',
      },
    });
    return;
  }

  if (!safeEqual(provided, expected)) {
    res.status(403).json({
      success: false,
      error: { code: 'FORBIDDEN', message: 'Invalid X-Demo-Key.' },
    });
    return;
  }

  next();
}
