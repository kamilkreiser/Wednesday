/**
 * Edge path canonicalisation — collapse repeated `/` before any predicate runs.
 *
 * KS-858 is the CLASS: a predicate mounted as an exact or prefix route above a
 * catch-all proxy is walked around by a path that carries the same route in a
 * different spelling, because the proxy normalises it again on the way out. The
 * predicate misses, the handler is still reached, and the guard is silently not
 * applied. Two instances were confirmed before this fix existed:
 *
 *   - KS-843: `POST /api/gdpr//erasures` missed the `subjects:erase` scope gate.
 *     Closed at the time by a normalisation scoped to `/api/gdpr` (routes/proxy.ts),
 *     which its own comment recorded as DELIBERATELY not the class fix, deferring
 *     the class to this ticket by name.
 *   - KS-946 / pen-test F5: the same spelling walked around ALL EIGHT path-scoped
 *     rate limiters (`/api/auth/{login,register,forgot-password,refresh,
 *     password-reset,verify-email,mfa}` and `/api/users/me/mfa`), six of them
 *     unauthenticated under the public `/api/auth` proxy. `POST /api/auth//verify-email`
 *     × 12 returned 12× 200 and never 429 — the counter never incremented, so the
 *     surface was unlimited rather than merely post-exhaustion.
 *
 * This middleware is the class fix: one collapse, once, above every predicate.
 *
 * MOUNTED APP-WIDE, AND THAT IS LOAD-BEARING, NOT STYLE. A path-scoped mount
 * cannot do this job, because it carries the very defect it exists to fix:
 * measured on express 4.22.1 — the version this service's own package-lock pins
 * and the version the built image runs; the workspace tree the unit suite runs
 * against is 4.22.2 and behaves identically, checked on both — `app.use('/api',
 * fn)` does NOT
 * run for `//api/auth/login`, while it does run for `/api/auth/login` and for
 * `/api/auth//login`. A `/api`-scoped normaliser would therefore be walked around
 * by a leading `//` exactly as the limiters are walked around by an interior one.
 * Only an unscoped `app.use(fn)` sees every spelling.
 *
 * SCOPE, deliberately narrow — this closes the reachable exploit and nothing else:
 *   - Repeated separators ONLY. No `%2F` / `%XX` decoding, no case folding.
 *     Case is KS-801 and is not folded in here. The other three F5 spellings
 *     (`%XX`, `;x=1` matrix, `%2F`) skip the limiter but are 404'd by the auth
 *     service's own express 4.22.2, which decodes neither for routing nor strips
 *     matrix params — they never reach a guarded operation, so widening this
 *     change to cover them would add blast radius with no exploit behind it.
 *   - PATH ONLY, and that is now true of every request-target form. A query
 *     string (or a fragment) can legitimately carry `//` — a URL in a
 *     parameter — and rewriting it would corrupt the request, so everything
 *     from the first `?` or `#` onwards is copied through byte-for-byte.
 *   - THE PATH IS FOUND, NOT ASSUMED. RFC 9112 §3.2 gives a request-target four
 *     forms and only one of them is all path. `collapseRepeatedSlashes` locates
 *     the path within the target and rewrites only that:
 *       origin-form     `/api/auth//login`            → path is the whole target
 *       absolute-form   `http://host/api/auth//login` → path starts after the authority
 *       authority-form  `host:443`   (CONNECT only)   → no path; returned unchanged
 *       asterisk-form   `*`          (OPTIONS only)   → no path; returned unchanged
 *     KS-858 round 2 (gate finding F-QA-1): the first cut split on the first `?`
 *     and treated everything before it as path, so an absolute-form target had
 *     its SCHEME collapsed — `http://host/api/auth/login` became
 *     `http:/host/api/auth/login`, whose pathname is `/host/api/auth/login`, and
 *     the gateway answered 404 to EVERY absolute-form request. RFC 9112 §3.2.2
 *     says a server MUST accept absolute-form, and index.ts's own KS-245 comment
 *     names where nothing normalises it first: "Dev/Demo Container Apps expose
 *     api-gateway directly with NO nginx in front."
 *     Handling absolute-form is not merely repairing that regression. Measured
 *     over a raw socket on real express, WITHOUT this middleware:
 *       POST http://host/api/auth/login   → the `/api/auth/login` mount RUNS
 *       POST http://host/api/auth//login  → the mount is MISSED
 *       POST http://host//api/auth/login  → the mount is MISSED
 *     so the KS-858 class is reachable through absolute-form as well, and a fix
 *     that merely skipped every non-origin-form target would have left it open.
 *   - `req.originalUrl` is untouched by design: express assigns it before the
 *     first middleware runs, so the audit and grace logs keep recording the
 *     spelling the caller actually sent, not the one we routed.
 *
 * `req.url` is deliberately NOT restored afterwards, which is the one way this
 * differs from the `/api/gdpr` block it generalises. That block restores because
 * it wraps a self-contained sub-router and wants the proxy to forward what the
 * caller typed. Here the collapsed path IS the routing decision for the whole
 * chain: restoring it would hand `//` back to every predicate downstream and
 * reinstate the bypass. The upstream service is unaffected either way — the
 * proxy already collapsed repeated slashes on the way out, so the backend
 * receives the same canonical path it received before this change.
 */

import type { Request, Response, NextFunction, RequestHandler } from 'express';

/** Two or more consecutive `/`. Used as a test AND as the replace pattern. */
const REPEATED_SLASH = /\/{2,}/;
const REPEATED_SLASH_GLOBAL = /\/{2,}/g;

/**
 * The `scheme "://"` opening of an absolute-form request-target: RFC 9112
 * §3.2.2 for the form, RFC 3986 §3.1 for the scheme grammar. Anchored, so it
 * can only ever match at the start of the target.
 */
const ABSOLUTE_FORM_PREFIX = /^[A-Za-z][A-Za-z0-9+\-.]*:\/\//;

/**
 * Where the PATH begins inside a request-target, or -1 when the target has no
 * path to canonicalise. See the four forms in the module docblock.
 */
function pathOffset(target: string): number {
  if (target.startsWith('/')) return 0;
  const scheme = ABSOLUTE_FORM_PREFIX.exec(target);
  if (scheme === null) return -1;
  // The first `/` AFTER the authority. -1 when the target is scheme + authority
  // and nothing else, which again leaves nothing to canonicalise.
  return target.indexOf('/', scheme[0].length);
}

/**
 * Collapse runs of `/` in the PATH portion of a raw request URL.
 *
 * Returns the input STRING UNCHANGED when there is nothing to collapse. The
 * middleware below compares before assigning, so an already-canonical request
 * is never re-assigned at all — that is the observable promise, and the cell
 * that pins it watches the `req.url` setter. (An earlier version of this
 * comment claimed the test asserted "reference identity, not equality". It
 * cannot: a JavaScript string is a primitive and `toBe` is `Object.is`, i.e.
 * value equality, so a rebuilt-but-equal string passes it. Gate finding F-QA-4.)
 */
export function collapseRepeatedSlashes(rawUrl: string): string {
  const queryStart = rawUrl.indexOf('?');
  const fragmentStart = rawUrl.indexOf('#');
  const tailStart =
    queryStart === -1 ? fragmentStart
    : fragmentStart === -1 ? queryStart
    : Math.min(queryStart, fragmentStart);

  const target = tailStart === -1 ? rawUrl : rawUrl.slice(0, tailStart);
  const tail = tailStart === -1 ? '' : rawUrl.slice(tailStart);

  const pathStart = pathOffset(target);
  if (pathStart === -1) return rawUrl;

  const path = target.slice(pathStart);
  if (!REPEATED_SLASH.test(path)) return rawUrl;
  return target.slice(0, pathStart) + path.replace(REPEATED_SLASH_GLOBAL, '/') + tail;
}

/**
 * Tag stamped on the middleware instance so a test can find THIS layer inside
 * the real app's middleware stack.
 *
 * Why a property and not the function's name: a build step may rename a
 * function. Measured on this repo — vitest's transform emits the inner handler
 * as `normaliseRepeatedSlashes2`, because a named function expression that
 * shadows its own factory gets a suffix, while `tsc` emits it unrenamed. A cell
 * matching on the name would therefore pass under one toolchain and fail under
 * the other. An own property survives both.
 */
export const NORMALISE_PATH_LAYER_TAG = 'ks858:normalise-repeated-slashes';

/** A request handler carrying the layer tag above. */
export type TaggedHandler = RequestHandler & { layerTag?: string };

/**
 * The middleware form. Mount FIRST in the chain, unscoped.
 *
 * The tag is load-bearing: `ks858-edge-path-normalisation.test.ts` uses it to
 * locate this layer in the real app's stack and assert that nothing
 * application-level sits above it (gate finding F-QA-2 — before that cell
 * existed, deleting the mount from index.ts left all 277 tests green).
 */
export function normaliseRepeatedSlashes(): TaggedHandler {
  const handler: TaggedHandler = function ks858NormaliseRepeatedSlashes(
    req: Request,
    _res: Response,
    next: NextFunction,
  ): void {
    const canonical = collapseRepeatedSlashes(req.url);
    // Compare before assigning: an already-canonical request is never
    // re-assigned at all, which is the observable form of the no-op promise.
    if (canonical !== req.url) req.url = canonical;
    next();
  };
  handler.layerTag = NORMALISE_PATH_LAYER_TAG;
  return handler;
}
