/**
 * Strict request media-type enforcement (KS-439).
 *
 * The published OpenAPI contract declares `application/json` for every request
 * body on the `/api/*` surface (sole exception: the OAuth 2.0 token endpoint,
 * which RFC 6749 §4.1.3 defines as `application/x-www-form-urlencoded`). The
 * platform previously parsed JSON leniently — a `text/plain` request with a
 * JSON-parseable body was accepted — which made the runtime broader than the
 * contract (found by the post-KS-428 sweep, decided on KS-439: enforce).
 *
 * Rule: an `/api/*` request that CARRIES A BODY must declare a JSON media
 * type, or it is rejected 415 before any parsing or proxying. Requests
 * without a body (no Content-Length / zero / no Transfer-Encoding) pass
 * untouched — several spec'd POSTs legitimately have no requestBody
 * (e.g. rotate-secret, webhook test), and clients often omit Content-Type
 * on empty requests.
 */

import type { NextFunction, Request, Response } from 'express';

/** Paths outside the enforced surface: everything not under /api/ (health, metrics, bare /webhooks receivers). */
const ENFORCED_PREFIX = '/api/';

/**
 * The OAuth 2.0 token endpoint is the one operation whose spec'd request body
 * is form-encoded (RFC 6749); JSON is also accepted for SPA convenience.
 *
 * ⚠ KS-781: `/api/oauth/authorize` WAS added here and has been REVERTED on
 * Kam's ruling (2026-09-05). Do not re-add it without reading why:
 *
 *  1. It bought no working functionality. The consent page still could not
 *     submit — the gateway mounts `csrfMiddleware.protect` BEFORE this
 *     middleware and `/api/oauth/authorize` is not in CSRF's `excludedPaths`,
 *     so a browser form POST is answered `403 CSRF_TOKEN_MISSING` and never
 *     reaches the 415 this entry would have relaxed. The page's brokenness is
 *     PRE-EXISTING, predates KS-781, and is tracked on its own ticket.
 *  2. It cost a new attack surface. Allowing a form body opens a cross-origin,
 *     PREFLIGHT-FREE path to a credential-verifying, lockout-accruing endpoint
 *     — removing the exact defence csrf.ts's own H21 comment cites for
 *     pre-session endpoints ("CSRF attacks via image/form tags can't set
 *     Content-Type"). `/api/oauth/token` already sits in that class; authorize
 *     would have been the first member taking a PASSWORD.
 *
 * If it is ever taken deliberately, it is taken with Origin/Sec-Fetch-Site
 * enforced BEFORE csrf.ts's no-cookie bail-out, and it is its own ticket and
 * its own review — not a line added here.
 */
// ⚠ KS-801: this membership test is CASE-SENSITIVE while Express routing is not.
// `req.path` arrives as the client sent it, so `/API/oauth/token` matches no
// entry here and skips the form allowance — and three sibling predicates in this
// gateway have the same shape, which is why KS-801 tracks them together rather
// than patching this one line. Do not "fix" it here in isolation: the class is
// the ticket.
const FORM_ALLOWED_PATHS = new Set(['/api/oauth/token']);

/**
 * KS-791: the two verify-file operations are the only ones on the `/api/*`
 * surface whose spec'd request body is RAW BYTES — the SERVER computes the
 * hash from the uploaded file (`verification.ts:511`, `verificationV2.ts:501`)
 * rather than receiving a hex digest in JSON. The JSON-only rule therefore made
 * them unreachable through the gateway: measured live, `octet-stream`, `pdf`,
 * `text/plain`, `multipart` and no content-type ALL returned 415, and only
 * `application/json` reached the handler — where it is the wrong body.
 *
 * The relaxation is deliberately as small as it can be:
 *   - two EXACT paths, matched by equality, never a prefix or a pattern;
 *   - ONE additional media type, `application/octet-stream`, and no other;
 *   - every other `/api/*` path keeps the strict rule unchanged.
 *
 * The JSON-only rule is a content-type-confusion defence (KS-439), so widening
 * it anywhere it is not required would trade a real defence for convenience.
 * `contentType.test.ts` pins both halves: these two paths accept octet-stream,
 * and a sibling verification route still 415s the identical binary body.
 */
const OCTET_STREAM_ALLOWED_PATHS = new Set([
  '/api/verification/verify-file',
  '/api/v2/verification/verify-file',
]);

/**
 * Media types accepted as "JSON" — the exact type plus any registered
 * `application/*+json` structured-syntax suffix (merge-patch, json-patch, …).
 *
 * @param mediaType - lowercased media type with parameters already stripped
 * @returns true when the type is a JSON media type per the contract
 */
function isJsonMediaType(mediaType: string): boolean {
  return mediaType === 'application/json' || (mediaType.startsWith('application/') && mediaType.endsWith('+json'));
}

/**
 * Whether the request actually carries a body. Deliberately NOT type-is's
 * `hasbody` — that treats `Content-Length: 0` as "has body", which would 415
 * every body-less POST a curl/SDK sends with an explicit zero length.
 *
 * @param req - incoming request
 * @returns true when a non-empty body is being transmitted
 */
function hasBody(req: Request): boolean {
  if (req.headers['transfer-encoding'] !== undefined) return true;
  const contentLength = Number(req.headers['content-length']);
  return Number.isFinite(contentLength) && contentLength > 0;
}

/**
 * Reject `/api/*` requests whose body is not declared as JSON with 415 and
 * the standard error envelope (KS-367 shape). Mounted ahead of the body
 * parsers AND the service proxies so the whole API surface is covered by
 * one choke point.
 *
 * @param req - incoming request
 * @param res - response used to emit the 415 envelope on mismatch
 * @param next - continuation for conforming (or out-of-scope) requests
 * @example
 * app.use(enforceJsonContentType); // before express.json() and the proxies
 */
export function enforceJsonContentType(req: Request, res: Response, next: NextFunction): void {
  // Out-of-scope surfaces (health, metrics, external webhook receivers) keep their own rules.
  if (!req.path.startsWith(ENFORCED_PREFIX)) return next();

  // No body → nothing to type-check; empty POSTs are legitimate for ops with no requestBody.
  if (!hasBody(req)) return next();

  // Strip parameters (charset etc.) — only the media type itself is contractual.
  const raw = req.headers['content-type'] ?? '';
  const mediaType = raw.split(';')[0].trim().toLowerCase();

  if (isJsonMediaType(mediaType)) return next();

  // RFC 6749 exception: the token endpoint's spec'd body is form-encoded.
  if (FORM_ALLOWED_PATHS.has(req.path) && mediaType === 'application/x-www-form-urlencoded') return next();

  // KS-791 exception: the two verify-file operations take raw bytes, because
  // the server — not the client — computes the hash.
  if (OCTET_STREAM_ALLOWED_PATHS.has(req.path) && mediaType === 'application/octet-stream') return next();

  res.status(415).json({
    success: false,
    error: {
      code: 'UNSUPPORTED_MEDIA_TYPE',
      message: 'This API accepts application/json request bodies. Please send Content-Type: application/json.',
      details: { received: mediaType === '' ? '(none)' : mediaType.slice(0, 100) },
    },
  });
}
