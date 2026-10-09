/**
 * =============================================================================
 * KS-1041 Step 2 — gateway provenance: establish WHERE a request came from
 * before any trust header is honoured.
 * =============================================================================
 *
 * WHY THIS EXISTS
 * ---------------
 * Downstream of this middleware, several places treat identity/tenant/role
 * headers as authoritative:
 *   - `extractTenantContext` resolves `x-tenant-id` (multi-tenant mode);
 *   - the KS-458 block falls back to `x-tenant-id` for the RLS GUC;
 *   - `routes/metering.ts:42` promotes `x-user-role: connector` straight into
 *     `req.user` without consulting a JWT.
 *
 * api-gateway sets those headers from a VERIFIED JWT and strips any that a
 * client supplied, so *via the edge* they are trustworthy.
 *
 * They are not trustworthy on the direct path. `originate:4000` is not
 * published to the host, but it sits on one flat compose network alongside
 * every other service, and any peer can address it directly. Measured on the
 * demo box, from a container with no business reaching originate:
 *
 *   | request                                             | result |
 *   | --------------------------------------------------- | ------ |
 *   | direct to originate:4000, no headers                 | 401    |
 *   | direct, forged `x-user-role: connector` + tenant id  | **200**|
 *   | the SAME forged request through api-gateway:8080     | 401    |
 *
 * The gateway's strip works exactly as written — the difference is the path,
 * not the header handling. So: honour trust headers only on a request the
 * gateway vouched for, and drop them otherwise.
 *
 * WHY STRIP AND NOT REFUSE — measured, not stylistic
 * --------------------------------------------------
 * Two services call originate directly by design:
 *   - `services/m365-integration/src/index.ts` — the Outlook add-in's
 *     verify-hash forward; sends `Content-Type` and nothing else.
 *   - `services/nft-certificate/src/services/minting.service.ts` — the
 *     certification fetch; a bare `fetch(url)` with no headers at all.
 *
 * NEITHER sends a trust header. The attack works by *supplying* these headers;
 * the legitimate direct callers supply none. So stripping closes the hole and
 * leaves both untouched, while refusing every unvouched request would break
 * them on a box prospects use and buy nothing extra.
 *
 * The refusal still happens — in the right place. With the headers gone the
 * metering shim never fires, `req.user` stays unset, and the route's own auth
 * answers 401. We redden the real arm, not one built to be reddened.
 *
 * FAIL-OPEN WHEN UNCONFIGURED, AND LOUDLY
 * ---------------------------------------
 * An unset secret leaves this inert. That is deliberate: fail-closed would mean
 * an unconfigured deploy silently loses every gateway-set identity at once —
 * an outage, not a safeguard. `describeState()` gives the caller a boot line
 * that names the CONSEQUENCE rather than the flag state, so an unprotected
 * deploy is loud instead of quiet.
 */

import type { Request, Response, NextFunction, RequestHandler } from 'express';
import * as crypto from 'crypto';

/**
 * The header the gateway mints — for originate only (`VOUCH_RECIPIENTS` in
 * services/api-gateway/src/routes/proxy.ts). It is also in api-gateway's
 * `TRUST_HEADER_PATTERN` (services/api-gateway/src/utils/trustHeaders.ts,
 * applied by index.ts before any auth or proxy logic), which is what makes it
 * unforgeable: a client that sends it has it removed at the edge, so the only
 * value originate can ever see is one the gateway itself set. That strip and
 * this check must change together.
 */
export const VOUCH_HEADER = 'x-gateway-vouch';

/**
 * The trust set dropped from an unvouched request. Mirrors the gateway's
 * inbound strip, plus `x-tenant-override`.
 *
 * `x-tenant-override` is deliberately ALLOWED through the gateway's edge strip
 * so its auth middleware can decide whether to honour it against the verified
 * JWT's role. An unvouched caller here has no verified JWT, so there is nothing
 * to decide — it drops with the rest.
 *
 * `x-emitter-internal` is deliberately NOT here. It marks K's own
 * originate -> anchoring hops and is consumed by anchoring, not by originate;
 * stripping it on the way IN would not protect anything and could interfere
 * with a legitimate internal hop that arrives here first.
 */
export const UNVOUCHED_STRIP_PATTERN =
  /^x-(user|tenant|organization|org|role|roles?|auth-user|policy|gateway-vouch)(-|$)/i;

/**
 * Constant-time comparison of a presented vouch against the configured secret.
 *
 * Lengths are compared first and return the same `false`: `timingSafeEqual`
 * throws on a length mismatch, and letting that throw would leak the secret's
 * length through the error path.
 */
export function vouchMatches(presented: unknown, secret: string): boolean {
  if (!secret) return false;
  if (typeof presented !== 'string' || presented.length === 0) return false;
  const a = Buffer.from(presented, 'utf8');
  const b = Buffer.from(secret, 'utf8');
  if (a.length !== b.length) return false;
  return crypto.timingSafeEqual(a, b);
}

/**
 * The boot line. Returns the CONSEQUENCE of the current configuration, not the
 * flag's value — a reader needs to know what is true, not which switch is off.
 */
export function describeState(secret: string): { level: 'info' | 'warn'; message: string } {
  if (secret) {
    return {
      level: 'info',
      message:
        '[gateway-provenance] ACTIVE — identity/tenant/role headers are honoured only on gateway-vouched requests',
    };
  }
  return {
    level: 'warn',
    message:
      '[gateway-provenance] DISABLED — GATEWAY_VOUCH_SECRET is unset, so identity/tenant/role headers are honoured from ANY caller that can reach this service directly, not only from api-gateway',
  };
}

/**
 * Mount as early as possible — ahead of `extractTenantContext` and the KS-458
 * tenant block, both of which read `x-tenant-id`.
 */
export function createGatewayProvenanceMiddleware(secret: string): RequestHandler {
  return (req: Request, _res: Response, next: NextFunction): void => {
    // Unconfigured: inert. describeState() has already said so at boot.
    if (!secret) return next();

    if (vouchMatches(req.headers[VOUCH_HEADER], secret)) {
      // Vouched. Drop the vouch itself so it never travels further: originate
      // makes its own server-to-server hops (originate -> anchoring) and the
      // secret has no business riding along on them.
      delete req.headers[VOUCH_HEADER];
      return next();
    }

    for (const header of Object.keys(req.headers)) {
      if (UNVOUCHED_STRIP_PATTERN.test(header)) {
        delete req.headers[header];
      }
    }
    next();
  };
}
