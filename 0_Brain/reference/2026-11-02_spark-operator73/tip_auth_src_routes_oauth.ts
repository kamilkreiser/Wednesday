/**
 * =============================================================================
 * OAUTH 2.0 ROUTES
 * =============================================================================
 * Standard OAuth 2.0 Authorization Code Flow with PKCE.
 * Compatible with any OAuth client library.
 *
 * Endpoints:
 *   GET  /api/oauth/authorize  — Start authorization (shows consent page)
 *   GET  /api/oauth/consent.js — The consent page's submit script (KS-799 round 2)
 *   POST /api/oauth/token      — Exchange code for tokens
 *   POST /api/oauth/revoke     — Revoke a token
 *   POST /api/oauth/apps       — Register an app
 *   GET  /api/oauth/apps       — List my apps
 *   GET  /api/oauth/apps/:id   — App details
 *   PATCH /api/oauth/apps/:id  — Update app
 *   DELETE /api/oauth/apps/:id — Deactivate app
 *   POST /api/oauth/apps/:id/rotate-secret — Rotate client secret
 * =============================================================================
 */

import { Router, Request, Response, NextFunction } from 'express';
import { z } from 'zod';
// KS-1210: pgSafeStringSchema is no longer imported here. Both scope arrays it
// guarded are now closed z.enum(AVAILABLE_SCOPES) arrays, which cannot admit a NUL
// byte either, so the guard is subsumed rather than removed. tsc TS6133 caught the
// now-unused import; the enum is what replaced it.
import { runWithTenantId } from '@secuura/shared';
import {
  createApp, getAppByClientId, getAppById, listApps, updateApp, rotateSecret,
  createAuthorizationCode, exchangeCode, verifyClientSecret,
  validateScopes, parseScopeString, AVAILABLE_SCOPES,
} from '../services/oauth';
import { generateTokenPair, verifyRefreshToken } from '../services/jwt';
import { createSession } from '../services/session';
import { isRefreshJtiDenylisted } from '../services/refreshDenylist';
import * as userRepo from '../repositories/userRepo';
import { authenticate } from '../middleware/authenticate';
import { logger } from '../utils/logger';
import { enforcePasswordLoginGates, mfaCodeRuntimeSchema } from '../services/passwordLoginGate';

export const oauthRouter = Router();

/**
 * KS-781 F-1/F-6 — the credential fields of POST /api/oauth/authorize, typed and
 * normalised the same way `/api/auth/login` types and normalises them.
 *
 * Authorize previously read `email`, `password` and `mfaCode` straight off
 * `req.body` with no schema at all. Two consequences, both measured:
 *
 *   F-1 (BLOCKER) — an untrimmed email produced a lockout key nothing had ever
 *   incremented while still resolving the victim's row, so the account lockout
 *   was defeated by a single leading space.
 *
 *   F-6 — a NON-STRING `mfaCode` reached `verifyBackupCode`, which calls
 *   `.toUpperCase()` on it, and 500'd on an MFA account holding backup codes.
 *
 * `email` mirrors loginSchema's `z.string().trim().email()`. The gate normalises
 * again (lowercase + trim) because it is the shared layer doors 2 and 3 will
 * call — belt and braces here is deliberate, not redundant.
 *
 * Deliberately covers ONLY the credential fields. The OAuth parameters keep
 * their existing hand-rolled validation and their existing 400 shapes (KS-144),
 * so this closes the finding without re-contracting the endpoint.
 */
// KS-796 F-6: exported for the identity assertion — see routes/auth.ts.
export const authorizeCredentialsSchema = z.object({
  email: z.string().trim().email(),
  password: z.string().min(1),
  // KS-781 N-1 — AN EMPTY STRING IS AN ABSENT SECOND FACTOR, NOT A MALFORMED ONE.
  //
  // The consent page this route ships renders `mfaCode` unconditionally and
  // NOT `required`, because an account without MFA has nothing to type. An HTML
  // form submits every named input; an untouched one arrives as `""`. To zod,
  // `""` is PRESENT — `.optional()` does not apply, the regex runs, and it
  // fails. So the first version of this schema returned `400 invalid_request`
  // to every non-MFA user, on a page whose own comment said they were
  // unaffected. Measured on the re-gate, and a regression introduced with the
  // field itself.
  //
  // Normalised here rather than at the page: the same shape reaches us from any
  // form-backed SPA that posts its whole state, and a fix living in a `<script>`
  // would not cover them. `.min(1)` on the union arm keeps a genuinely
  // malformed code (`"abc"`, `"12345"`) a 400 — the relaxation is exactly the
  // empty string and nothing else.
  mfaCode: mfaCodeRuntimeSchema,
});

// KS-466: the platform default tenant (KS-192) — the tenant createApp pins for
// a tenantless caller and the value the migration backfills rows into.
const DEFAULT_TENANT_ID = 'a0000000-0000-4000-8000-000000000001';

// KS-466: seed the fail-closed RLS tenant GUC for the authenticated /apps
// management routes. The gateway's `/api/oauth` proxy also carries the pre-auth
// token/authorize endpoints, so it deliberately sets no `x-tenant-id` header —
// which means the auth service's global tenantGucContext has nothing to seed,
// and fail-closed RLS (migration 039) returns ZERO rows on every oauth_apps
// read. Seed the GUC from the VERIFIED JWT here, after authenticate(); the same
// default createApp pins keeps writes and reads on the same tenant. Runs the
// downstream handler inside the tenant scope via AsyncLocalStorage.
function seedTenantGuc(req: Request, _res: Response, next: NextFunction): void {
  const tenantId = ((req as { user?: { tenantId?: string } }).user?.tenantId) || DEFAULT_TENANT_ID;
  runWithTenantId(tenantId, () => next());
}

// =============================================================================
// KS-797 — ONE definition of "which client is this, and may it be redirected
// there", used by every branch of the authorization endpoint.
// =============================================================================
// The GET handler validated the client and the redirect URI. The POST handler
// did neither: measured on the same file, `getAppByClientId` 0 / redirectUris 0
// / invalid_client 0 in the POST block against 2 / 3 / 3 in the GET block.
//
// Two consequences, both measured live through the gateway:
//   - with valid credentials, a code was minted for an unregistered client and
//     302'd to an attacker-chosen URL (the QA pass's finding);
//   - with NO credentials at all, `action=deny` 302'd to an attacker-chosen URL
//     carrying `error=access_denied` — an open redirect off the platform's own
//     authorization endpoint, reachable by anyone. The GET handler refused the
//     same client_id with 400 invalid_client on the same input, which is what
//     made it a defect rather than a configuration accident.
//
// Extracted rather than copied into POST, because two definitions of
// "registered redirect" is the drift class this endpoint has already produced
// twice (KS-737, KS-781). Callers get the rule or they get a refusal; there is
// nowhere for a second opinion to live.
//
// ⚠ THE WILDCARD IS INHERITED, NOT INTRODUCED. `redirectUris.includes('*')`
// accepts any redirect URI for that app. It is the GET path's existing rule and
// is preserved deliberately so the two handlers cannot disagree; it is NOT
// endorsed. Measured on this deployment: 0 of 21 registered apps carry one, so
// it is latent. Recorded on KS-797 as its own concern.
// =============================================================================

/**
 * =============================================================================
 * KS-804 — THE RESOLVER CARRIES ALL FOUR APP-DERIVED RULES, NOT ONE
 * =============================================================================
 * KS-797 moved the client/redirect rule in here and left three behind in the
 * GET handler. POST enforced none of them. Measured by the tester: a POST for a
 * PUBLIC app with no `code_challenge` returned 302 with a code minted and
 * `codeChallenge` undefined — and `exchangeCode` verifies PKCE only inside
 * `if (row.code_challenge)`, so that code was redeemable with **no verifier at
 * all**. PKCE was not merely skipped at authorize time; it was unenforceable at
 * exchange time for every code minted that way.
 *
 * This is the THIRD instance of GET/POST drift on this one endpoint — KS-737,
 * KS-781, KS-797, now this. Fixing the rules one at a time is what invited a
 * fourth, so all four live here and each handler renders the same resolution:
 *
 *   1. response_type            2. client_id + registered redirect_uri
 *   3. PKCE for public clients  4. scope against app.allowedScopes
 *
 * ⚠ THE WILDCARD IS INHERITED, NOT INTRODUCED. `redirectUris.includes('*')`
 * accepts any redirect URI for that app. It is the GET path's existing rule and
 * is preserved deliberately so the two handlers cannot disagree; it is NOT
 * endorsed. Measured: 0 of 21 registered apps carry one, so it is latent.
 * Recorded on KS-797 as its own concern.
 * =============================================================================
 */

/**
 * KS-804 Q4 — schemes a redirect target may use.
 *
 * The registration schema admits `javascript:` and `data:`, so a registered URI
 * can be a script payload the browser executes on redirect. Census 2026-09-05:
 * 0 such rows on local (of 21) or demo (of 3) — hardening, not a live exposure.
 *
 * Stated honestly: this is a REFUSAL SET, not a true allow-list, and the reason
 * is that a true one is not constructible here. Native clients register their
 * own custom schemes (`com.example.app:`), which are per-app and unbounded, so
 * enumerating what is permitted would break every mobile client. What CAN be
 * enumerated is the set that makes a redirect dangerous: schemes the browser
 * executes or treats as an inline document. Everything else is allowed, and
 * `https:` is the only web scheme among them.
 *
 * `http:` is refused too. It is not executable, but an authorization code
 * delivered over cleartext is a code on the wire, and RFC 8252 §7.3 already
 * excludes it for native apps.
 */
/**
 * KS-822 F-6 — the ONLY two methods `exchangeCode` can verify. Kept as a Set
 * beside the check so the pair cannot drift: the verifier's `=== 'S256'` else
 * branch IS the plain implementation, so this set is exhaustive by definition
 * and adding a member here without teaching the verifier would be the same
 * silent downgrade one level up.
 */
const PKCE_METHODS = new Set(['S256', 'plain']);

const REFUSED_REDIRECT_SCHEMES = new Set([
  'javascript:', 'data:', 'vbscript:', 'file:', 'blob:', 'about:', 'http:',
]);

type AuthorizeClientResolution =
  | {
      ok: true;
      app: Awaited<ReturnType<typeof getAppByClientId>> & object;
      redirectUri: string;
      /** Scopes actually granted — validated against `app.allowedScopes`. */
      grantedScopes: string[];
      codeChallenge?: string;
      codeChallengeMethod: string;
    }
  | {
      ok: false;
      message:
        | 'invalid_request'
        | 'invalid_client'
        | 'invalid_redirect_uri'
        | 'invalid_scope'
        | 'unsupported_response_type';
      description: string;
    };

interface AuthorizeParams {
  clientId?: string;
  redirectUri?: string;
  /**
   * The consent FORM carries no `response_type` — it is a submission for a flow
   * the GET already validated. POST therefore passes `body.response_type || 'code'`,
   * so a client that puts a bogus value in the body is refused rather than
   * ignored, and the rule still has exactly one definition.
   *
   * KS-822 F-3 — the operator is `||`, NOT `??`, and the difference is
   * user-visible. `??` substitutes only for null/undefined, and an HTML form
   * submits an empty field as `""`, which is PRESENT. RULE 1 then saw
   * `"" !== 'code'` and refused, so a person clicking "Deny" on the consent
   * form got a 400 JSON body where the parent had redirected them back to the
   * client with `error=access_denied`. An empty field is an absent one here; a
   * BOGUS one is still refused, which is what the third cell asserts.
   */
  responseType?: string;
  scope?: string;
  codeChallenge?: string;
  codeChallengeMethod?: string;
}

async function resolveAuthorizeClient(params: AuthorizeParams): Promise<AuthorizeClientResolution> {
  const { clientId, redirectUri, responseType, scope, codeChallenge, codeChallengeMethod } = params;

  // RULE 1 — response_type. Ahead of the client lookup: an unsupported flow is
  // wrong regardless of who is asking, and refusing first costs no DB read.
  if (responseType !== 'code') {
    return {
      ok: false,
      message: 'unsupported_response_type',
      description: 'Only response_type=code is supported',
    };
  }

  if (!clientId) {
    return { ok: false, message: 'invalid_request', description: 'client_id is required' };
  }

  // KS-283: reject a malformed client_id BEFORE the DB lookup. Non-UTF-8 / NUL
  // garbage makes Postgres throw 22021, which surfaced as a 500. A real
  // client_id is an opaque `sec_<hex>` we mint, so anything outside a
  // conservative URL-safe charset is simply not a known client.
  if (!/^[A-Za-z0-9._~-]+$/.test(clientId)) {
    return { ok: false, message: 'invalid_client', description: 'Unknown client_id' };
  }

  const app = await getAppByClientId(clientId);
  if (!app) {
    return { ok: false, message: 'invalid_client', description: 'Unknown client_id' };
  }

  if (redirectUri && !app.redirectUris.includes(redirectUri) && !app.redirectUris.includes('*')) {
    return { ok: false, message: 'invalid_redirect_uri', description: 'redirect_uri not registered for this app' };
  }

  // RULE 2c — KS-822 F-7: WHEN `redirect_uri` MAY BE OMITTED, decided here so all
  // three entry points agree.
  //
  // The disagreement F-7 names was three-way, not two-way: GET passed an absent
  // `redirect_uri` to this resolver and got the fallback; the POST DENY branch
  // did the same; and only the POST APPROVE path refused it, at a pre-resolver
  // required-field guard that never reached this line. So the fallback was dead
  // on exactly one of the three, which is the KS-804 shape again — a rule
  // enforced by a handler instead of by the resolver every handler shares.
  //
  // RFC 6749 3.1.2.3 makes the omission legal only when the ambiguity does not
  // exist: with more than one registered URI the client MUST send one. The old
  // fallback took `redirectUris[0]` no matter how many were registered, so with
  // two registered it silently picked the first — a choice nobody made, and the
  // same shape as F-5's empty filter. Now the omission is allowed only when the
  // app registers EXACTLY one, and refused otherwise.
  //
  // `invalid_request` is an existing message and so is invisible to F-8's
  // message-set guard — the RULES row for this rule is hand-added in the same
  // commit, as with F-6.
  if (!redirectUri && app.redirectUris.length !== 1) {
    return {
      ok: false,
      message: 'invalid_request',
      description: 'redirect_uri is required unless the app registers exactly one',
    };
  }

  const effectiveRedirect = redirectUri || app.redirectUris[0];

  // RULE 2b (KS-804 Q4) — the scheme. Applied to the EFFECTIVE target, so a
  // dangerous URI is refused whether the client supplied it or it came from the
  // app's own registration.
  let parsed: URL;
  try {
    parsed = new URL(effectiveRedirect);
  } catch {
    return {
      ok: false,
      message: 'invalid_redirect_uri',
      description: 'redirect_uri must be a valid absolute URL',
    };
  }
  if (REFUSED_REDIRECT_SCHEMES.has(parsed.protocol)) {
    return {
      ok: false,
      message: 'invalid_redirect_uri',
      description: 'redirect_uri scheme is not permitted',
    };
  }

  // RULE 3 — PKCE for public clients. This is the one whose absence on POST was
  // not merely a skipped check: a code minted with no challenge is redeemable
  // with no verifier, because exchangeCode only verifies inside
  // `if (row.code_challenge)`.
  if (app.appType === 'public' && !codeChallenge) {
    return {
      ok: false,
      message: 'invalid_request',
      description: 'code_challenge is required for public clients (PKCE)',
    };
  }

  // RULE 3b — KS-822 F-6: `code_challenge_method` must be one the verifier
  // understands, checked HERE rather than trusted downstream.
  //
  // `exchangeCode` selects the method with `row.code_challenge_method === 'S256'
  // ? sha256(verifier) : verifier` — an exact string match with the PLAIN
  // comparison as its else branch. So every value that is not exactly `S256`
  // verifies as plain, and the two that matter are:
  //   · `s256` — a client that believes it asked for S256 and got it. The
  //     challenge it computed is a sha256 digest; the server compares the raw
  //     verifier to it, so the code is simply unredeemable — but nothing tells
  //     the client its protection was never applied, and a client that instead
  //     sends the verifier as the challenge redeems with NO protection at all.
  //   · anything else — silently plain.
  // RFC 7636 4.3: the method must be a registered value. An unregistered one is
  // an error, not a default.
  //
  // Refused with `invalid_request`, an EXISTING message, deliberately: it is the
  // same class as RULE 3's refusal, and inventing a message for it would be a
  // published-contract change this ticket has no grant for. Note the consequence,
  // named because F-8's guard depends on it — a new rule reusing an existing
  // message is invisible to that guard, so the RULES row for this rule is added
  // by hand in the same commit and that is the only thing making it driven.
  //
  // NOT covered, and stated rather than implied: rows ALREADY stored carrying a
  // bad method still verify as plain. That population drains with the 5-minute
  // code TTL and no migration is attempted here.
  if (codeChallengeMethod !== undefined && !PKCE_METHODS.has(codeChallengeMethod)) {
    return {
      ok: false,
      message: 'invalid_request',
      description: 'code_challenge_method must be S256 or plain',
    };
  }

  // RULE 4 — scopes, against the app's own allow-list. POST used to store the
  // raw `scope` string from the body straight onto the code.
  //
  // KS-822 F-4 — OMITTING `scope` IS A DEFAULT, AND THE DEFAULT IS THE WHOLE
  // ALLOW-LIST. Named here deliberately rather than left to be re-derived.
  // RFC 6749 3.3 gives a server exactly two options when the client omits the
  // parameter: use a pre-defined default, or fail the request. This is the
  // first. Before KS-804 put GET and POST on this one resolver, POST stored the
  // raw body string, so omitting `scope` minted NULL — which is NEITHER of the
  // RFC's options. So the consolidation did not widen a correct behaviour; it
  // replaced a non-conforming one with a conforming and wider one.
  //
  // The asymmetry that makes this worth writing down: omitting the parameter
  // grants EVERYTHING the app may hold, while explicitly asking for only things
  // it may not hold grants NOTHING (`validateScopes` filters rather than
  // refuses — that is F-5, and it is a separate item). Asking for less than
  // nothing is therefore stricter than asking for nothing at all.
  //
  // Bound by `ks804-authorize-get-post-agree-per-rule.test.ts`, describe
  // "KS-822 F-4", four cases: the two no-scope cases plus a narrow-request
  // control (an explicit `openid` must NOT be widened to the allow-list) and
  // the all-unpermitted contrast. Removing the `?:` below reds exactly the two
  // no-scope cases. Narrowing this default is a decision to be made in those
  // cases first, not here.
  // KS-1219: a repeated query parameter (?scope=a&scope=b) or a JSON array body reaches this resolver as an ARRAY whatever the compile-time cast at the handler says, and
  // parseScopeString below would throw on it (an array has no split) and the handler would answer 500 server_error. A malformed request is a 400 invalid_request, the same
  // existing message RULE 3 uses, so no published message changes.
  if (scope !== undefined && typeof scope !== 'string') {
    return {
      ok: false,
      message: 'invalid_request',
      description: 'scope must be a single space- or comma-separated string',
    };
  }
  const requestedScopes = parseScopeString(scope);
  const grantedScopes = validateScopes(
    requestedScopes.length > 0 ? requestedScopes : app.allowedScopes,
    app.allowedScopes,
  );

  // RULE 5 — KS-822 F-5: rule 4 FILTERS, and a filter that removes everything is
  // not a decision anybody made. A request naming only scopes the app may not
  // hold used to reach `ok: true` with an EMPTY grant: on GET that renders a
  // consent page asking the user to approve a list of nothing, and on POST it
  // mints a code carrying scope ''.
  //
  // RFC 6749 4.1.2.1 registers `invalid_scope` for exactly this. Partial overlap
  // is left as a filter — that IS permitted, and §3.3's obligation to tell the
  // client what it actually got is already met by the token response's `scope`
  // field. Only the all-or-nothing case refuses.
  //
  // Deliberately conditioned on `requestedScopes.length > 0`, so this is about a
  // request that ASKED and got nothing. An app registered with an EMPTY
  // `allowedScopes` still takes RULE 4's default path unchanged and is not
  // refused here — whether such an app should be able to mint at all is a
  // different question and not this one.
  //
  // `invalid_scope` is a NEW message, and that is load-bearing twice over: it is
  // the RFC's own code for this condition (answering with `invalid_request`
  // would misreport a scope problem as a malformed request, the same species of
  // error F-1b corrected in the published contract), and unlike F-6's reused
  // message it IS visible to F-8's message-set guard — which reds until the
  // RULES row exists. That red was observed before the row was written.
  if (requestedScopes.length > 0 && grantedScopes.length === 0) {
    return {
      ok: false,
      message: 'invalid_scope',
      description: 'none of the requested scopes are permitted for this client',
    };
  }

  return {
    ok: true,
    app,
    redirectUri: effectiveRedirect,
    grantedScopes,
    codeChallenge,
    codeChallengeMethod: codeChallengeMethod || 'S256',
  };
}

/** The refusal envelope both handlers already use, so the shape does not drift either. */
function authorizeRefusal(res: Response, r: Extract<AuthorizeClientResolution, { ok: false }>) {
  return res.status(400).json({
    success: false,
    error: { code: 'BAD_REQUEST', message: r.message, description: r.description },
  });
}

/**
 * KS-799 — deliver the post-consent redirect target in a way the consent page
 * can actually act on.
 *
 * The gateway CSRF guard is double-submit-cookie: it requires the `X-XSRF-TOKEN`
 * *header* (csrf.ts), which a top-level `<form>` POST cannot set — so the consent
 * page must submit via `fetch` with the header (the XSRF-TOKEN cookie is
 * httpOnly:false for exactly this). But a browser `fetch` cannot follow this 302
 * to NAVIGATE the page, so an XHR caller is handed the target as JSON and
 * navigates itself; every other caller keeps the native 302.
 *
 * This is the whole of Option 2 (KS-799 ruling, 2026-09-07): no CSRF exemption
 * and no change to the CSRF middleware. It is additive and backward-compatible —
 * a request without `X-Requested-With: XMLHttpRequest` behaves exactly as before,
 * which is why every existing authorize test still sees a 302. Error responses on
 * this path were already JSON, so the fetch client reads those unchanged.
 */
function respondAuthorizeRedirect(req: Request, res: Response, url: string): void {
  if ((req.get('x-requested-with') || '').toLowerCase() === 'xmlhttprequest') {
    res.status(200).json({ success: true, redirect: url });
    return;
  }
  res.redirect(url);
}

// =============================================================================
// GET /api/oauth/authorize — Authorization endpoint
// =============================================================================

oauthRouter.get('/authorize', async (req: Request, res: Response) => {
  try {
    const {
      client_id, redirect_uri, response_type, scope, state,
      code_challenge, code_challenge_method,
    } = req.query as Record<string, string>;
    // KS-1797: a repeated query parameter (?state=a&state=b) reaches this handler as an ARRAY whatever the cast above says. generateConsentPage then calls escapeHtml on it, an array has no
    // `replace`, and the catch below answered 500 server_error. A malformed request is a 400 invalid_request, the existing message the resolver's rules use, so no published message changes.
    if ((state !== undefined && typeof state !== 'string') || (code_challenge !== undefined && typeof code_challenge !== 'string')) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_request', description: 'state and code_challenge must each be a single string' } });
    }
    // KS-804: every app-derived rule lives in the resolver now — response_type,
    // client/redirect, the scheme, PKCE for public clients and scopes. This
    // handler renders the resolution; it does not re-decide any of it.
    const resolved = await resolveAuthorizeClient({
      clientId: client_id,
      redirectUri: redirect_uri,
      responseType: response_type,
      scope,
      codeChallenge: code_challenge,
      codeChallengeMethod: code_challenge_method,
    });
    if (!resolved.ok) return authorizeRefusal(res, resolved);
    const { app, grantedScopes } = resolved;
    const effectiveRedirect = resolved.redirectUri;

    // Serve the consent page
    const consentHtml = generateConsentPage({
      app,
      // KS-798: the canonical client_id from the resolved app record, not the
      // caller-supplied query param — the resolver already confirmed the two match
      // (getAppByClientId(client_id) returned this app), and the record is the
      // source that cannot be spoofed by a crafted request.
      clientId: app.clientId,
      scopes: grantedScopes,
      state: state || '',
      redirectUri: effectiveRedirect,
      codeChallenge: resolved.codeChallenge,
      codeChallengeMethod: resolved.codeChallengeMethod,
    });

    res.setHeader('Content-Type', 'text/html');
    res.send(consentHtml);

  } catch (error: any) {
    // KS-283: a malformed query param (NUL byte / non-UTF-8 sequence) can still
    // reach the DB layer and surface as Postgres 22021 / 22P05 — that is a
    // client error, answer 400 not 500 (mirrors the KS-144 22P02 mapping on the
    // /apps/:id routes below).
    if (error?.code === '22021' || error?.code === '22P05' || /invalid byte sequence|untranslatable character/i.test(error?.message || '')) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_request', description: 'Malformed request parameters' } });
    }
    logger.error('OAuth authorize error', { error: error.message });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'server_error', description: 'Internal server error' } });
  }
});

// =============================================================================
// POST /api/oauth/authorize — Process consent (login + approve)
// =============================================================================

// =============================================================================
// KS-799 (round 2) — the consent page's submit script, served as an EXTERNAL
// same-origin resource.
//
// Round 1 rendered these bytes as an inline <script> inside generateConsentPage.
// Peter's review of PR #881 measured what a browser actually receives on this
// route: /api/oauth/* is proxied by the api-gateway; this service sets its own
// Content-Security-Policy on every response (index.ts `app.use(helmet())` —
// helmet's defaults are script-src 'self' and script-src-attr 'none'); and
// http-proxy writes upstream headers with res.setHeader, which REPLACES the
// gateway's deliberate 'unsafe-inline' (KS-245). So script-src as the browser
// sees it is 'self' — the inline script was refused, no submit listener
// attached, the native <form> POST went out without X-XSRF-TOKEN, and the page
// landed back on the 403 CSRF_TOKEN_MISSING this ticket was filed to remove.
//
// Of the three vehicles Peter offered (per-request nonce · external same-origin
// script · per-route CSP), only this one is admitted at EVERY layer without a
// change outside this file: the production nginx gateway
// (docker/nginx-gateway/nginx-production.conf) sends script-src 'self' too, and
// browsers enforce the intersection of the policies they receive, so a nonce
// minted here would still be refused there. 'self' admits a same-origin
// <script src> everywhere; no CSP header is authored in a second place.
//
// The bytes below are the round-1 script, moved verbatim. They run inside the
// consent page (see generateConsentPage), so the constraints that applied
// inside the template literal still apply: no backticks, no dollar-brace.
// Executed under test by ks799-consent-script-csp-and-execution.test.ts (jsdom
// drives a real click through this script); admission by the response's own
// CSP is asserted there too.
// =============================================================================
const CONSENT_SUBMIT_SCRIPT = `
    (function () {
      var form = document.getElementById('form');
      var errorEl = document.getElementById('error');
      if (!form) return;
      var chosen = 'approve';
      var btns = form.querySelectorAll('button[type="submit"]');
      for (var i = 0; i < btns.length; i++) {
        btns[i].addEventListener('click', function (e) { chosen = e.currentTarget.value || 'approve'; });
      }
      function readCookie(name) {
        var parts = document.cookie ? document.cookie.split('; ') : [];
        for (var j = 0; j < parts.length; j++) {
          var eq = parts[j].indexOf('=');
          if (eq > -1 && parts[j].slice(0, eq) === name) return decodeURIComponent(parts[j].slice(eq + 1));
        }
        return '';
      }
      function showError(msg) { errorEl.textContent = msg; errorEl.style.display = 'block'; }
      form.addEventListener('submit', function (ev) {
        ev.preventDefault();
        var token = readCookie('XSRF-TOKEN');
        if (!token) { showError('Your session could not be verified. Please reload this page and try again.'); return; }
        var body = {};
        new FormData(form).forEach(function (v, k) { body[k] = v; });
        body.action = chosen;
        fetch(form.getAttribute('action'), {
          method: 'POST',
          credentials: 'same-origin',
          redirect: 'manual',
          headers: {
            'Content-Type': 'application/json',
            'Accept': 'application/json',
            'X-XSRF-TOKEN': token,
            'X-Requested-With': 'XMLHttpRequest'
          },
          body: JSON.stringify(body)
        }).then(function (res) {
          return res.json().then(
            function (d) { return { status: res.status, data: d }; },
            function () { return { status: res.status, data: {} }; }
          );
        }).then(function (r) {
          if (r.data && r.data.redirect) { window.location.assign(r.data.redirect); return; }
          var err = r.data && r.data.error;
          showError((err && (err.description || err.message)) || ('Request failed (' + r.status + ').'));
        }).catch(function () { showError('Network error. Please try again.'); });
      });
    })();
`;

oauthRouter.get('/consent.js', (_req: Request, res: Response) => {
  // helmet sets X-Content-Type-Options: nosniff, so the media type is
  // load-bearing: a browser refuses to execute a script served as anything else.
  res.setHeader('Content-Type', 'application/javascript; charset=utf-8');
  res.setHeader('Cache-Control', 'no-store');
  res.send(CONSENT_SUBMIT_SCRIPT);
});

oauthRouter.post('/authorize', async (req: Request, res: Response) => {
  try {
    const {
      email, password, client_id, redirect_uri, scope, state,
      code_challenge, code_challenge_method, action,
      // KS-804: the consent FORM does not send this, so it is normally
      // undefined and defaults to 'code'. Destructured so a client that DOES
      // put a value in the body is validated rather than ignored.
      response_type,
      // KS-781: the second factor. Same field name and same accepted shapes as
      // `/api/auth/login` (6 digits = TOTP, 8 alphanumeric = backup code), so a
      // client that can log in can authorize without learning a second dialect.
      mfaCode,
    } = req.body;

    // KS-797 — VALIDATE BEFORE REDIRECTING, INCLUDING ON DENY.
    //
    // This branch redirected to whatever `redirect_uri` arrived, before anything
    // was checked and with no credentials required at all. Measured live: an
    // unauthenticated POST with an unregistered client_id and
    // `redirect_uri=https://evil.example.net/steal` returned
    // `302 -> https://evil.example.net/steal?error=access_denied&state=xyz`,
    // while the GET handler refused the same client_id with 400 invalid_client.
    // An open redirect off the platform's own authorization endpoint, reachable
    // by anyone. It carries no code, so it is a phishing primitive rather than a
    // credential leak — and it needs no account, which the code-carrying half
    // does.
    if (action === 'deny') {
      const denied = await resolveAuthorizeClient({
        clientId: client_id,
        redirectUri: redirect_uri,
        responseType: response_type || 'code',
        scope,
        // A deny mints nothing, so PKCE cannot apply — the user is refusing,
        // and demanding a challenge to decline would strand public clients on
        // the consent page with no way out.
        codeChallenge: 'n/a-deny',
        codeChallengeMethod: code_challenge_method,
      });
      if (!denied.ok) return authorizeRefusal(res, denied);

      // KS-804 D1/D3 — BUILD THE URL, DO NOT CONCATENATE IT.
      //
      // This was `${redir}?error=...`. A registered URI that already carries a
      // query (`https://app.test/cb?tenant=acme`) produced a second `?`, so the
      // client never received `error=access_denied` at all — the deny outcome
      // was silently undeliverable for exactly those apps. A fragment did the
      // same, with the whole query landing inside it.
      let denyUrl: URL;
      try {
        denyUrl = new URL(denied.redirectUri);
      } catch {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_redirect_uri', description: 'redirect_uri must be a valid absolute URL' } });
      }
      denyUrl.searchParams.set('error', 'access_denied');
      if (state) denyUrl.searchParams.set('state', state);
      return respondAuthorizeRedirect(req, res, denyUrl.toString()); // KS-799
    }

    // Validate required fields up-front — a missing/malformed body is an
    // invalid_request (400), not a server error. Without this, undefined
    // fields fell through to getUserByEmail() / new URL() and threw → 500
    // (KS-144).
    // KS-822 F-7: `redirect_uri` is NO LONGER required here. It was the only
    // thing standing between this path and RULE 2c, and requiring it at the
    // handler is what made the fallback dead on approve while GET and deny both
    // had it. The resolver decides optionality now; `client_id` stays because
    // without it there is no app to fall back TO, and email/password stay
    // because this path authenticates.
    if (!email || !password || !client_id) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_request', description: 'email, password and client_id are required' } });
    }

    // KS-797 — RESOLVE THE CLIENT BEFORE ANY CREDENTIAL LOGIC.
    //
    // This handler consulted neither `client_id` nor `redirect_uri` anywhere:
    // measured against the GET block in the same file as the control,
    // getAppByClientId 0 vs 2, redirectUris 0 vs 3, invalid_client 0 vs 3. With
    // valid credentials it minted a code for an unregistered client and 302'd it
    // to an attacker-chosen URL (RFC 6749 §3.1.2.3 and §4.1.1).
    //
    // Before the gate rather than after: an unregistered client should cost no
    // password verify, and it discloses nothing the GET handler does not already
    // disclose on the same input.
    // KS-804: the SAME resolver, so POST now carries response_type, the scheme,
    // PKCE-for-public-clients and scope validation — the three rules it had
    // never enforced.
    const client = await resolveAuthorizeClient({
      clientId: client_id,
      redirectUri: redirect_uri,
      responseType: response_type || 'code',
      scope,
      codeChallenge: code_challenge,
      codeChallengeMethod: code_challenge_method,
    });
    if (!client.ok) return authorizeRefusal(res, client);

    // KS-797 — and parse the target BEFORE minting, not after. The code used to
    // be created and persisted at what is now the line below, and only then was
    // `new URL(redirect_uri)` attempted; a malformed target therefore left an
    // orphaned code behind every 400.
    let redirectUrl: URL;
    try {
      redirectUrl = new URL(client.redirectUri);
    } catch {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_redirect_uri', description: 'redirect_uri must be a valid absolute URL' } });
    }

    // KS-781 — authenticate the user through the SAME gates as /api/auth/login.
    //
    // What used to be here was `getUserByEmail` + `verifyPassword` and nothing
    // else: no second factor, no account lockout, no account-status check. That
    // made this endpoint a second, password-only login — a password alone
    // yielded an authorization code for an account whose front door refuses
    // password-only login, which was confirmed at runtime, not inferred.
    //
    // The refusal is uniform (pen-test F-11): unknown email, wrong password,
    // suspended, deactivated, SSO-only and locked-out all return the same 401.
    // Only "this account has a second factor and you did not supply a usable
    // code" is distinguishable, and it mirrors login's 403 MFA_REQUIRED.
    // KS-781 F-1/F-6: type and normalise the credential fields before they reach
    // any consumer. A malformed body is an invalid_request (400), in the same
    // shape the hand-rolled checks above already return.
    const creds = authorizeCredentialsSchema.safeParse({ email, password, mfaCode });
    if (!creds.success) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_request', description: 'email must be a valid address, password must be a non-empty string, and mfaCode (if supplied) must be 6 digits or an 8-character backup code' } });
    }

    const sourceIp = (req.ip as string) || (req.socket?.remoteAddress as string) || '';
    const gate = await enforcePasswordLoginGates({
      email: creds.data.email,
      password: creds.data.password,
      mfaCode: creds.data.mfaCode,
      sourceIp,
      route: 'oauth/authorize',
    });

    if (!gate.ok) {
      if (gate.reason === 'mfa_required') {
        return res.status(403).json({ success: false, error: { code: 'MFA_REQUIRED', message: 'MFA verification required', description: 'This account requires a second factor. Supply mfaCode.' } });
      }
      return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'invalid_credentials', description: 'Invalid email or password' } });
    }
    const user = gate.user;

    // Generate authorization code
    const code = await createAuthorizationCode({
      clientId: client_id,
      userId: user.id,
      // KS-797: the VALIDATED target, not the raw body field. On this path they
      // are the same string (redirect_uri is required above), but the token
      // exchange compares what was stored against what the client sends, so the
      // stored value should be the one that passed the registration check.
      redirectUri: client.redirectUri,
      // KS-804: the VALIDATED scopes, not the raw body string. The body's
      // `scope` was stored verbatim, so a code could carry scopes the app is
      // not permitted to hold.
      scope: client.grantedScopes.join(' '),
      codeChallenge: client.codeChallenge,
      codeChallengeMethod: client.codeChallengeMethod,
    });

    // The target was resolved and parsed above, before the code was minted.
    redirectUrl.searchParams.set('code', code);
    if (state) redirectUrl.searchParams.set('state', state);

    respondAuthorizeRedirect(req, res, redirectUrl.toString()); // KS-799

  } catch (error: any) {
    logger.error('OAuth authorize POST error', { error: error.message });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'server_error' } });
  }
});

// =============================================================================
// POST /api/oauth/token — Token exchange
// =============================================================================

/**
 * KS-820 — read the client secret from either place RFC 6749 2.3.1 allows.
 *
 * HTTP Basic first, because the RFC says a server MUST support it and SHOULD
 * prefer it. The body form is accepted too: it is what most SDKs send.
 *
 * The Basic credentials are only honoured when the userid half MATCHES the
 * `client_id` the request is exchanging under. Without that check a caller
 * could authenticate as one client and redeem another's code.
 *
 * Per the RFC the two halves are form-urlencoded before the base64, so they are
 * decoded here; a secret containing `:` is not mangled because only the FIRST
 * colon separates the pair.
 */
/**
 * KS-823 — the client a token request is made under: `client_id` in the body
 * (what public clients send, RFC 6749 §6) or the userid half of an HTTP Basic
 * header (a confidential client authenticating per §2.3.1 need not repeat it in
 * the body). Body wins when both are present; readClientSecret() then refuses a
 * Basic userid that does not match it.
 */
function readClientId(req: Request): string | undefined {
  const fromBody = (req.body as Record<string, unknown> | undefined)?.client_id;
  if (typeof fromBody === 'string' && fromBody.length > 0) return fromBody;
  const header = req.get('authorization');
  if (header && /^Basic /i.test(header)) {
    try {
      const decoded = Buffer.from(header.slice(6).trim(), 'base64').toString('utf8');
      const sep = decoded.indexOf(':');
      if (sep > 0) return decodeURIComponent(decoded.slice(0, sep));
    } catch {
      // malformed — not an identification
    }
  }
  return undefined;
}

function readClientSecret(req: Request, clientId: string): string | undefined {
  const header = req.get('authorization');
  if (header && /^Basic /i.test(header)) {
    try {
      const decoded = Buffer.from(header.slice(6).trim(), 'base64').toString('utf8');
      const sep = decoded.indexOf(':');
      if (sep > 0) {
        const user = decodeURIComponent(decoded.slice(0, sep));
        const pass = decodeURIComponent(decoded.slice(sep + 1));
        if (user === clientId && pass) return pass;
      }
    } catch {
      // A malformed Authorization header is not a credential. Fall through to
      // the body rather than 500 on it.
    }
  }
  const fromBody = (req.body as Record<string, unknown> | undefined)?.client_secret;
  return typeof fromBody === 'string' && fromBody.length > 0 ? fromBody : undefined;
}

oauthRouter.post('/token', async (req: Request, res: Response) => {
  try {
    const { grant_type, code, redirect_uri, client_id, code_verifier, refresh_token } = req.body;

    if (grant_type === 'authorization_code') {
      // Exchange authorization code for tokens
      if (!code || !client_id || !redirect_uri) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_request', description: 'code, client_id, and redirect_uri are required' } });
      }

      // -----------------------------------------------------------------
      // KS-820 — AUTHENTICATE THE CLIENT. This endpoint did not, at all.
      //
      // The destructure above named six fields and `client_secret` was not one
      // of them, so a confidential app's code redeemed with no credential
      // whatsoever. `getAppByClientId`'s own comment already asserted the
      // opposite -- "the OAuth token/authorize endpoints resolve the app
      // pre-auth (the client secret is the credential being checked)" -- which
      // is how this survived: the claim was written down, so it read as done.
      //
      // RFC 6749 4.1.3: a confidential client MUST authenticate here. 2.3.1:
      // the server MUST support HTTP Basic and MAY support the body, so both
      // are accepted below.
      //
      // A PUBLIC app has no secret to keep, so ON THIS GRANT it authenticates
      // no client: `clientAuthenticated` stays false and PKCE is the only
      // thing that can carry the code.
      //
      // F-2a — what `exchangeCode` enforces is the FLOOR, not this rule, and
      // this sentence used to call it "the invariant". See
      // `services/oauth.ts` (the KS-820 block above the credential check),
      // which states the floor and says in the same breath that calling it
      // "the invariant" is exactly how the weaker half comes to be read as
      // the whole one. THE rule is the one above: a code is redeemable only
      // on the credential its client type demands — a verified secret for a
      // confidential app, a verified PKCE challenge for a public one — and
      // never on neither. That is enforced HERE, in the route.
      //
      // Worth naming: this is the FOURTH place one wrong sentence reached
      // (comment → contract → test header → here), and the first three were
      // corrected in #827 and #831 while this one survived inside the very
      // commit that corrected them.
      //
      // SCOPE — this block is grant_type=authorization_code. The refresh_token
      // branch below authenticates the client on the SAME terms (KS-823): it
      // resolves the app (is_active pinned), requires a confidential app's
      // secret, and additionally checks the refresh token's `client_id` claim
      // against the presenting client. Until 2026-09-13 that branch
      // authenticated no client at all; this sentence used to record that as
      // an open defect so no reader would take the rule above as a universal
      // and close the ticket as working-as-intended (the KS-820 failure mode:
      // a claim written down reads as done).
      //
      // ALSO CLOSED, and named rather than left as a side effect: resolving the
      // app pins `is_active = true`, so a DEACTIVATED app can no longer redeem
      // a code that was minted while it was live. The old path never looked the
      // app up at all.
      // -----------------------------------------------------------------
      const app = await getAppByClientId(client_id);
      if (!app) {
        // One refusal for unknown and for deactivated. `client_id` is public by
        // design (it travels in the authorize URL), so this is not an oracle
        // over a secret.
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'invalid_client', description: 'Unknown or inactive client' } });
      }

      let clientAuthenticated = false;
      if (app.appType === 'confidential') {
        const presented = readClientSecret(req, client_id);
        if (!presented || !(await verifyClientSecret(client_id, presented))) {
          logger.warn('OAuth token exchange refused: confidential client did not authenticate', { clientId: client_id });
          return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'invalid_client', description: 'Client authentication failed' } });
        }
        clientAuthenticated = true;
      }

      const result = await exchangeCode({
        code,
        clientId: client_id,
        redirectUri: redirect_uri,
        codeVerifier: code_verifier,
        clientAuthenticated,
      });

      if (!result) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_grant', description: 'Invalid or expired authorization code' } });
      }

      // Get user and generate tokens.
      //
      // KS-790: this is a PRE-auth path — the caller holds an authorization
      // code, not a bearer, and no tenant GUC is seeded — so the lookup goes
      // through the SECURITY DEFINER carve-out (migration 039), exactly as the
      // other pre-auth token flows do since KS-458. The plain, RLS-scoped
      // `getUserById` answers nothing here under fail-closed RLS and the grant
      // failed `invalid_grant: User not found` for EVERY code, MFA or not. The
      // null guard below is unchanged: a user the carve-out cannot see is still
      // refused.
      const user = await userRepo.getUserByIdPreAuth(result.userId);
      // KS-1150 (R-1): pin user.status === 'ACTIVE' here as the refresh grant below
      // and POST /api/auth/refresh already do — a SUSPENDED user's code minted a
      // pair (the window is a code minted before a suspension); ONE refusal and
      // ONE description for missing and inactive, the refresh grant's.
      if (!user || user.status !== 'ACTIVE') {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_grant', description: 'User inactive or not found' } });
      }

      // KS-43: OAuth authorization_code grants are user-redirect-driven flows.
      // The SPA / mobile app receives the code via browser redirect and
      // exchanges it here. Default to 'browser' — confidential server-side
      // clients can re-issue under 'api' if they want single-session.
      const session = await createSession(user, req.ip, req.get('user-agent'), undefined, 'browser', 'oauth');
      // KS-823: the pair is bound to the client that redeemed the code — the
      // refresh grant checks the claim against the presenting client.
      // KS-835: and it carries what the user GRANTED (result.scope, validated
      // against the app's allow-list at /authorize), not the role default. The
      // response's informational `scope` below now describes the token it
      // accompanies.
      const tokens = generateTokenPair(user, session.id, { clientId: client_id, scopes: parseScopeString(result.scope || '') });

      logger.info('OAuth token issued', { clientId: client_id, userId: user.id, scope: result.scope });

      return res.json({
        access_token: tokens.accessToken,
        refresh_token: tokens.refreshToken,
        token_type: 'Bearer',
        expires_in: tokens.expiresIn,
        scope: result.scope || '',
      });

    } else if (grant_type === 'refresh_token') {
      // Refresh token grant
      if (!refresh_token) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_request', description: 'refresh_token is required' } });
      }

      // -----------------------------------------------------------------
      // KS-823 — AUTHENTICATE THE CLIENT on this grant too. Until 2026-09-13
      // the whole client-authentication block sat inside the
      // authorization_code branch: this one read no client_id, resolved no
      // app and never reached verifyClientSecret, so a CONFIDENTIAL app's
      // refresh token needed no credential, a DEACTIVATED app's refresh token
      // kept working while its codes stopped, and nothing checked that the
      // redeemer was the client the token was issued to.
      //
      // RFC 6749 §6: a confidential client MUST authenticate on the refresh
      // grant (secret by Basic or body, §2.3.1); a public client MUST send its
      // client_id. The client is resolved through the same definer lookup as
      // the code grant, which pins is_active — one refusal for unknown and for
      // deactivated, so the distinction is not an oracle. The client is
      // authenticated BEFORE the token is verified: a caller who cannot
      // identify itself learns nothing about the token it holds.
      // -----------------------------------------------------------------
      const refreshClientId = readClientId(req);
      if (!refreshClientId) {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_request', description: 'client_id is required' } });
      }
      const refreshApp = await getAppByClientId(refreshClientId);
      if (!refreshApp) {
        return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'invalid_client', description: 'Unknown or inactive client' } });
      }
      if (refreshApp.appType === 'confidential') {
        const presented = readClientSecret(req, refreshClientId);
        if (!presented || !(await verifyClientSecret(refreshClientId, presented))) {
          logger.warn('OAuth refresh refused: confidential client did not authenticate', { clientId: refreshClientId });
          return res.status(401).json({ success: false, error: { code: 'UNAUTHORIZED', message: 'invalid_client', description: 'Client authentication failed' } });
        }
      }

      // Verify and rotate refresh token. verifyRefreshToken THROWS
      // InvalidTokenError on a bad/expired/wrong-type token — without this
      // catch the throw lands in the route's outer handler and answers 500
      // for what is a client error (KS-255; regressed when the guard was
      // removed in #248, re-verified live 2026-06-12).
      //
      // KS-790: verifyRefreshToken comes from the file's static import now. It
      // used to be a `require('../services/jwt')` on this line — redundant with
      // the import at the top of the file, and the reason NO test had ever
      // reached this branch: under vitest a runtime require of a TypeScript
      // module answers "Cannot find module", the throw lands in the outer catch,
      // and every refresh-grant case reads 500 whatever it asserts (measured
      // 2026-09-13 while writing ks790-token-pre-auth-user-lookup.test.ts).
      let decoded;
      try {
        decoded = verifyRefreshToken(refresh_token);
      } catch {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_grant', description: 'Invalid refresh token' } });
      }

      // Audit A-05: refuse refresh tokens that have been denylisted elsewhere
      // (rotated via /api/auth/refresh, or revoked at logout). Without this
      // check, the OAuth grant_type=refresh_token path is a backdoor around
      // the rotation-replay defence.
      if (decoded.jti && (await isRefreshJtiDenylisted(decoded.jti))) {
        logger.warn('OAuth refresh token replay refused', { jti: decoded.jti, userId: decoded.userId });
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_grant', description: 'Refresh token revoked' } });
      }

      // KS-823 — TOKEN BINDING. OAuth-minted refresh tokens carry the client
      // they were issued to (jwt.ts, `client_id`); a token that names another
      // client, or names none, is not this client's to redeem. "None" covers a
      // token minted before binding existed and a token minted by the
      // interactive login flow (which never passes through this grant) — both
      // refused, fail-closed: the cost is one re-authorization, the alternative
      // is a token redeemable by any party that holds it.
      if (decoded.client_id !== refreshClientId) {
        logger.warn('OAuth refresh refused: token not bound to the presenting client', { clientId: refreshClientId, bound: decoded.client_id ?? null, userId: decoded.userId });
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_grant', description: 'Refresh token was not issued to this client' } });
      }

      // KS-790: the same pre-auth carve-out as the authorization_code grant
      // above — a refresh token is not a bearer and seeds no tenant context.
      const user = await userRepo.getUserByIdPreAuth(decoded.userId);
      if (!user || user.status !== 'ACTIVE') {
        return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'invalid_grant', description: 'User inactive or not found' } });
      }

      // KS-43: refresh_token grants typically come from the same client that
      // did the original authorization_code exchange (browser SPA / mobile).
      // Default to 'browser' to match the original session's policy.
      const session = await createSession(user, req.ip, req.get('user-agent'), undefined, 'browser', 'oauth');
      // KS-823: the re-issued pair stays bound to the same client.
      // KS-835: and keeps the token's OWN granted scopes — a refresh never widens
      // a grant back to the role default.
      const tokens = generateTokenPair(user, session.id, { clientId: refreshClientId, scopes: decoded.scopes ?? [] });

      return res.json({
        access_token: tokens.accessToken,
        refresh_token: tokens.refreshToken,
        token_type: 'Bearer',
        expires_in: tokens.expiresIn,
      });

    } else {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'unsupported_grant_type', description: 'Only authorization_code and refresh_token are supported' } });
    }

  } catch (error: any) {
    logger.error('OAuth token error', { error: error.message });
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: 'server_error' } });
  }
});

// =============================================================================
// POST /api/oauth/revoke — Token revocation
// =============================================================================

oauthRouter.post('/revoke', async (_req: Request, res: Response) => {
  // OAuth 2.0 token revocation always returns 200 (even if token is invalid)
  // This prevents information leakage about token validity
  res.json({ success: true });
});

// =============================================================================
// APP MANAGEMENT (authenticated)
// =============================================================================

// KS-444: the create handler only truthy-checked name/redirectUris, so a body
// violating the published OAuthAppCreateRequest contract (the sweep sent
// `description: {}` — spec says string) was accepted and stored → 201. Validate
// against the published request schema (same shape as UpdateOAuthAppSchema below,
// with the spec's required fields required; trim user-facing strings per KS-202).
// The spec object is non-strict, so undeclared extras (logoUrl, …) stay
// permitted and are read from req.body as before.
//
// KS-821 — `appType` USED TO BE ONE OF THOSE EXTRAS, and that was the defect.
// It was read from `req.body` on the line after this schema parsed, so the
// closed set never applied to it and `POST /apps {"appType":"native"}` returned
// 201 for an app that is neither public nor confidential. It is declared here
// now, which is what makes KS-804's central rule non-negotiable at
// registration rather than the caller's choice.
//
// Case is FOLDED, not rejected: an exact-match rule elsewhere reads "Public"
// and "public" as different strings, and the one that reaches the database is
// what every later comparison sees. Normalising at the boundary means there is
// only ever one spelling to compare.
export const OAUTH_APP_TYPES = ['public', 'confidential'] as const;

// =============================================================================
// KS-1210: TWO GATES, TWO LISTS.
// Neither list in routes/users.ts is importable: PLATFORM_ADMIN_ROLES is a
// module-level const that is NOT exported (routes/users.ts:192, blob
// ea9f8da97a049f4de93d815ba7de0ed655ba65dd) and ADMIN_ROLES is local to that
// file's GET '/' handler (routes/users.ts:439, same blob). They are copied here
// BY NAME rather than exported from there, because routes/users.ts is another
// row's file this round. A drift cell in
// __tests__/ks1210-oauth-app-scopes-and-ownership.test.ts reads users.ts SOURCE
// and fails if either copy stops matching it, so the duplication cannot rot
// silently.
//
// Gate 1 (privileged scope): only a caller in the FOUR-role PLATFORM list may
// register or keep a privileged scope. certifications:write and webhooks:manage
// are deliberately NOT privileged in this change — a product choice, stated in
// the PR body so it can be tightened later.
// Gate 2 (ownership): the by-id routes answer 404 to a caller who is neither the
// app's creator nor in the SIX-role admin list. 404, not 403, so the existence of
// another user's app is not disclosed.
const OAUTH_PRIVILEGED_SCOPES: readonly string[] = ['admin:read', 'admin:write'];
const OAUTH_PLATFORM_ADMIN_ROLES: readonly string[] = ['SYSTEM_ADMIN', 'SUPER_ADMIN', 'admin', 'super_admin'];
const OAUTH_APP_ADMIN_ROLES: readonly string[] = ['SYSTEM_ADMIN', 'ORG_ADMIN', 'ISSUER_ADMIN', 'admin', 'super_admin', 'SUPER_ADMIN'];

function privilegedScopesIn(scopes?: readonly string[]): string[] {
  return (scopes || []).filter((s) => OAUTH_PRIVILEGED_SCOPES.includes(s));
}
function isOauthPlatformAdmin(role?: string): boolean {
  return !!role && OAUTH_PLATFORM_ADMIN_ROLES.includes(role);
}
function isOauthAppAdmin(role?: string): boolean {
  return !!role && OAUTH_APP_ADMIN_ROLES.includes(role);
}
// Returns the app when the caller may act on it, or null when it does not exist
// or is not theirs. Both cases are a 404 to the caller.
async function appVisibleTo(req: any, id: string) {
  const app = await getAppById(id);
  if (!app) return null;
  if (app.createdBy && app.createdBy === req.user?.userId) return app;
  if (isOauthAppAdmin(req.user?.role as string)) return app;
  return null;
}
const PRIVILEGE_REFUSED = 'that scope may only be registered by a platform administrator';

export const CreateOAuthAppSchema = z.object({
  name: z.string().trim().min(1).max(100),
  redirectUris: z.array(z.string().url()).min(1),
  // KS-1210: CLOSED to the published vocabulary. AVAILABLE_SCOPES is the nine
  // scopes in services/oauth.ts:57-67 (blob
  // 8995edec6a43b7623def6c9d1b002ed0a1b0dc86); anything else — '*',
  // 'subjects:erase', 'made:up' — is a 400 for EVERY caller, which alone closes
  // the sev-5 this ticket was raised for.
  // KS-451 is SUBSUMED, not dropped: a closed enum cannot admit a NUL byte
  // either, so the pgSafeStringSchema guard this replaces is strictly weaker.
  scopes: z.array(z.enum(AVAILABLE_SCOPES as unknown as [string, ...string[]])).optional(),
  description: z.string().trim().optional(),
  appType: z
    .string()
    .trim()
    .toLowerCase()
    .pipe(z.enum(OAUTH_APP_TYPES))
    .optional(),
});

oauthRouter.post('/apps', authenticate(), seedTenantGuc, async (req: any, res: Response) => {
  try {
    const parsed = CreateOAuthAppSchema.safeParse(req.body);
    if (!parsed.success) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'name and redirectUris (array) are required', details: parsed.error.errors } });
    }
    // KS-821: `appType` comes from parsed.data now — the schema's closed,
    // case-folded set — NOT from the raw body.
    const { name, description, redirectUris, scopes, appType } = parsed.data;

    // KS-1210 gate 1: a privileged scope may only be registered by a caller in the
    // FOUR-role PLATFORM list. Creation itself stays open to any authenticated user,
    // which is the ticket's question 2 answered deliberately rather than by omission.
    const privileged = privilegedScopesIn(scopes);
    if (privileged.length > 0 && !isOauthPlatformAdmin(req.user?.role as string)) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: PRIVILEGE_REFUSED, details: { scopes: privileged } } });
    }
    const { logoUrl, websiteUrl, privacyPolicyUrl } = req.body;

    const result = await createApp({
      name,
      description,
      redirectUris,
      scopes,
      appType: appType || 'public',
      organizationId: req.user?.organizationId,
      tenantId: req.user?.tenantId,
      logoUrl,
      websiteUrl,
      privacyPolicyUrl,
      createdBy: req.user?.userId,
    });

    res.status(201).json({
      success: true,
      app: {
        id: result.app.id,
        name: result.app.name,
        clientId: result.app.clientId,
        redirectUris: result.app.redirectUris,
        allowedScopes: result.app.allowedScopes,
        appType: result.app.appType,
      },
      clientSecret: result.clientSecret, // Only returned at creation time
      warning: result.clientSecret ? 'Store the client_secret securely — it cannot be retrieved later.' : undefined,
    });
  } catch (error: any) {
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: error.message } });
  }
});

oauthRouter.get('/apps', authenticate(), seedTenantGuc, async (req: any, res: Response) => {
  try {
    const apps = await listApps(req.user?.userId);
    res.json({
      success: true,
      apps: apps.map(a => ({
        id: a.id,
        name: a.name,
        description: a.description,
        clientId: a.clientId,
        redirectUris: a.redirectUris,
        allowedScopes: a.allowedScopes,
        appType: a.appType,
        logoUrl: a.logoUrl,
        websiteUrl: a.websiteUrl,
        isActive: a.isActive,
        createdAt: a.createdAt,
      })),
    });
  } catch (error: any) {
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: error.message } });
  }
});

oauthRouter.get('/apps/:id', authenticate(), seedTenantGuc, async (req: any, res: Response) => {
  try {
    // KS-1210 gate 2: owner-or-admin. A caller who is neither the creator nor in the
    // SIX-role admin list gets the same 404 as a missing app, so the existence of
    // someone else's app is not disclosed.
    const app = await appVisibleTo(req, req.params.id);
    if (!app) return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'App not found' } });
    res.json({ success: true, app });
  } catch (error: any) {
    // KS-144: a malformed id (non-UUID) makes the lookup throw (Postgres 22P02) —
    // that's a not-found, not a server error. KS-445: an id carrying a NUL byte /
    // invalid UTF-8 raises 22021/22P05 instead — the only input here is the id,
    // and an unstorable id is equally not a known app.
    if (error?.code === '22P02' || error?.code === '22021' || error?.code === '22P05' || /invalid input syntax|invalid byte sequence|untranslatable character/i.test(error?.message || '')) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'App not found' } });
    }
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: error.message } });
  }
});

// KS-431: the update body was passed straight to updateApp, which builds a dynamic
// UPDATE from whatever keys/values it receives. A wrong-type value (the sweep sent
// `description: {}`) and the spec's `scopes` key (whose column is `allowed_scopes`, not
// `scopes`) both made Postgres throw → a raw 500. Validate against the published request
// schema (trim user-facing strings per KS-202) and remap `scopes` → the domain field.
export const UpdateOAuthAppSchema = z.object({
  name: z.string().trim().min(1).max(100).optional(),
  redirectUris: z.array(z.string().url()).min(1).optional(),
  // KS-1210: same closed vocabulary as the create path; KS-451's NUL guard is
  // subsumed by the enum.
  scopes: z.array(z.enum(AVAILABLE_SCOPES as unknown as [string, ...string[]])).optional(),
  description: z.string().trim().optional(),
});

oauthRouter.patch('/apps/:id', authenticate(), seedTenantGuc, async (req: any, res: Response) => {
  const parsed = UpdateOAuthAppSchema.safeParse(req.body);
  if (!parsed.success) {
    return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Invalid request', details: parsed.error.errors } });
  }
  // KS-445: a malformed {id} can't match any app — answer 404 up-front instead
  // of letting Postgres throw. The 22P02 mapping below already covered plain
  // non-UUID ids, but an id carrying a NUL byte / invalid UTF-8 raises 22021
  // instead, which fell through to the raw 500. Every real app id is a UUID we
  // mint, so anything else is simply not a known app.
  if (!z.string().uuid().safeParse(req.params.id).success) {
    return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'App not found' } });
  }
  // The spec field `scopes` is the domain's `allowedScopes` (DB column allowed_scopes);
  // updateApp camel→snake-maps its keys, so pass the domain name, never the raw `scopes`.
  const { scopes, ...rest } = parsed.data;
  const updates = scopes !== undefined ? { ...rest, allowedScopes: scopes } : rest;
  try {
    // KS-1210 gate 2 BEFORE gate 1, deliberately: a non-owner must not be able to
    // tell a 403 (the app exists, my scope was refused) from a 404 (no such app).
    if (!(await appVisibleTo(req, req.params.id))) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'App not found' } });
    }
    // KS-1210 gate 1: the same privileged-scope rule as the create path.
    const privilegedUpdate = privilegedScopesIn(scopes);
    if (privilegedUpdate.length > 0 && !isOauthPlatformAdmin(req.user?.role as string)) {
      return res.status(403).json({ success: false, error: { code: 'FORBIDDEN', message: PRIVILEGE_REFUSED, details: { scopes: privilegedUpdate } } });
    }
    const app = await updateApp(req.params.id, updates);
    if (!app) return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'App not found' } });
    res.json({ success: true, app });
  } catch (error: any) {
    // KS-144: a malformed id (non-UUID) makes the lookup throw (Postgres 22P02) —
    // that's a not-found, not a server error.
    if (error?.code === '22P02' || /invalid input syntax/i.test(error?.message || '')) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'App not found' } });
    }
    // KS-445: with the id pre-validated as a UUID above, a 22021/22P05 here can
    // only come from a body value — the spec permits any string, but a NUL byte
    // / invalid UTF-8 sequence is unstorable in Postgres text. That's the
    // client's malformed input, not a server fault (mirrors the KS-283 mapping
    // on GET /authorize).
    if (error?.code === '22021' || error?.code === '22P05' || /invalid byte sequence|untranslatable character/i.test(error?.message || '')) {
      return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Malformed request parameters' } });
    }
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: error.message } });
  }
});

oauthRouter.delete('/apps/:id', authenticate(), seedTenantGuc, async (req: any, res: Response) => {
  try {
    // KS-1210 gate 2. CONSEQUENCE BEYOND THE TICKET, stated in the PR body: this
    // route previously answered 200 for an id that does not exist at all, because
    // updateApp's null return was never inspected. With the ownership lookup in
    // front of it, a non-existent app is now a 404 as well as a foreign one.
    if (!(await appVisibleTo(req, req.params.id))) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'App not found' } });
    }
    await updateApp(req.params.id, { isActive: false });
    res.json({ success: true });
  } catch (error: any) {
    // KS-144: a malformed id (non-UUID) makes the lookup throw (Postgres 22P02) —
    // that's a not-found, not a server error. KS-445: NUL-byte / invalid-UTF-8
    // ids raise 22021/22P05 — same not-found semantics (id is the only input).
    if (error?.code === '22P02' || error?.code === '22021' || error?.code === '22P05' || /invalid input syntax|invalid byte sequence|untranslatable character/i.test(error?.message || '')) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'App not found' } });
    }
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: error.message } });
  }
});

oauthRouter.post('/apps/:id/rotate-secret', authenticate(), seedTenantGuc, async (req: any, res: Response) => {
  try {
    // KS-1210 gate 2: rotating another user's client secret is the sharpest of the
    // four by-id routes — it would hand the caller working credentials.
    if (!(await appVisibleTo(req, req.params.id))) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'App not found' } });
    }
    const newSecret = await rotateSecret(req.params.id);
    if (!newSecret) return res.status(400).json({ success: false, error: { code: 'BAD_REQUEST', message: 'Cannot rotate secret for public apps' } });
    res.json({
      success: true,
      clientSecret: newSecret,
      warning: 'Store the new client_secret securely — it cannot be retrieved later.',
    });
  } catch (error: any) {
    // KS-144: a malformed id (non-UUID) makes the lookup throw (Postgres 22P02) —
    // that's a not-found, not a server error. KS-445: NUL-byte / invalid-UTF-8
    // ids raise 22021/22P05 — same not-found semantics (id is the only input).
    if (error?.code === '22P02' || error?.code === '22021' || error?.code === '22P05' || /invalid input syntax|invalid byte sequence|untranslatable character/i.test(error?.message || '')) {
      return res.status(404).json({ success: false, error: { code: 'NOT_FOUND', message: 'App not found' } });
    }
    res.status(500).json({ success: false, error: { code: 'INTERNAL_ERROR', message: error.message } });
  }
});

// =============================================================================
// SCOPES INFO
// =============================================================================

oauthRouter.get('/scopes', (_req: Request, res: Response) => {
  res.json({
    scopes: AVAILABLE_SCOPES.map(s => {
      const [resource, action] = s.split(':');
      return { scope: s, resource, action, description: getScopeDescription(s) };
    }),
  });
});

function getScopeDescription(scope: string): string {
  const descriptions: Record<string, string> = {
    'verify:read': 'Verify documents against the blockchain registry',
    'documents:read': 'List and read your documents',
    'documents:write': 'Create, modify, and upload documents',
    'certifications:read': 'List and view certifications',
    'certifications:write': 'Issue and revoke certifications',
    'users:read': 'Read your user profile',
    'webhooks:manage': 'Create and manage webhook subscriptions',
    'admin:read': 'Read organisation settings and configuration',
    'admin:write': 'Modify organisation settings',
  };
  return descriptions[scope] || scope;
}

// =============================================================================
// CONSENT PAGE HTML
// =============================================================================

function generateConsentPage(params: {
  app: { name: string; logoUrl?: string; websiteUrl?: string };
  // KS-798: the consent form's hidden client_id field used to be derived from
  // params.redirectUri (a URL, rejected by the resolver's RULE 2a charset check
  // — `:` and `/` are not in `[A-Za-z0-9._~-]`), so a POST of the rendered form
  // answered 400 invalid_client and the flow could not complete. generateConsentPage
  // is now passed the real client_id explicitly; the GET handler sources it from
  // the resolved app record (canonical `sec_<hex>`), never from caller-echoed input.
  clientId: string;
  scopes: string[];
  state: string;
  redirectUri: string;
  codeChallenge?: string;
  codeChallengeMethod: string;
}): string {
  const scopeList = params.scopes.map(s =>
    `<li>${getScopeDescription(s)}</li>`
  ).join('');

  return `<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Authorize ${params.app.name} — Secuura</title>
  <style>
    * { margin: 0; padding: 0; box-sizing: border-box; }
    body { font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif;
           background: #0F1B33; color: white; display: flex; justify-content: center;
           align-items: center; min-height: 100vh; }
    .card { background: #1a2740; border-radius: 16px; padding: 40px; width: 420px;
            box-shadow: 0 8px 32px rgba(0,0,0,0.3); }
    .app-info { text-align: center; margin-bottom: 24px; }
    .app-info .name { font-size: 1.3rem; font-weight: 700; }
    .app-info .desc { font-size: 0.85rem; color: #888; margin-top: 4px; }
    .divider { border-top: 1px solid #334; margin: 20px 0; }
    .scopes h3 { font-size: 0.85rem; color: #aaa; margin-bottom: 8px; }
    .scopes ul { list-style: none; }
    .scopes li { padding: 8px 0; border-bottom: 1px solid #1f2f45; font-size: 0.9rem; }
    .scopes li::before { content: "\\2713"; color: #0CF7C4; margin-right: 8px; }
    .field { margin-bottom: 14px; }
    .field label { display: block; font-size: 0.85rem; color: #aaa; margin-bottom: 4px; }
    .field input { width: 100%; padding: 10px 14px; border-radius: 8px; border: 1px solid #334;
                   background: #0F1B33; color: white; font-size: 0.95rem; }
    .field input:focus { border-color: #0CF7C4; outline: none; }
    .buttons { display: flex; gap: 10px; margin-top: 20px; }
    .buttons button { flex: 1; padding: 12px; border: none; border-radius: 8px; font-size: 1rem;
                      font-weight: 600; cursor: pointer; }
    .btn-approve { background: #0CF7C4; color: #0F1B33; }
    .btn-approve:hover { background: #0ad9a8; }
    .btn-deny { background: transparent; color: #888; border: 1px solid #334; }
    .btn-deny:hover { color: white; border-color: #666; }
    .error { color: #ff6b6b; font-size: 0.85rem; margin-bottom: 10px; display: none; }
    .powered { text-align: center; margin-top: 20px; font-size: 0.7rem; color: #444; }
  </style>
</head>
<body>
  <div class="card">
    <div class="app-info">
      <div class="name">${escapeHtml(params.app.name)}</div>
      <div class="desc">wants to access your Secuura account</div>
    </div>

    <div class="scopes">
      <h3>This app will be able to:</h3>
      <ul>${scopeList}</ul>
    </div>

    <div class="divider"></div>

    <div class="error" id="error"></div>

    <form method="POST" action="/api/oauth/authorize" id="form">
      <input type="hidden" name="client_id" value="${escapeHtml(params.clientId)}"/>
      <input type="hidden" name="redirect_uri" value="${escapeHtml(params.redirectUri)}"/>
      <input type="hidden" name="scope" value="${escapeHtml(params.scopes.join(' '))}"/>
      <input type="hidden" name="state" value="${escapeHtml(params.state)}"/>
      <input type="hidden" name="code_challenge" value="${escapeHtml(params.codeChallenge || '')}"/>
      <input type="hidden" name="code_challenge_method" value="${escapeHtml(params.codeChallengeMethod)}"/>

      <div class="field">
        <label>Email</label>
        <input type="email" name="email" required autofocus placeholder="you@company.com"/>
      </div>
      <div class="field">
        <label>Password</label>
        <input type="password" name="password" required placeholder="Your Secuura password"/>
      </div>
      <!--
        KS-781: the second factor. OPTIONAL, exactly as mfaCode is optional on
        /api/auth/login — accounts without MFA leave it blank and are unaffected.
        (No backticks in this comment: it lives inside a template literal, where
        a backtick ends the string. It did, and cost a build.)
        Without this field the form could not supply what the route now
        requires, so an MFA-enabled user would receive 403 MFA_REQUIRED with no
        way to answer it. Reuses the existing .field / input styling; no new
        rule and no new colour.
      -->
      <div class="field">
        <label>Authentication code (if your account has MFA enabled)</label>
        <input type="text" name="mfaCode" autocomplete="one-time-code"
               placeholder="6-digit code, or a backup code"/>
      </div>

      <div class="buttons">
        <button type="submit" name="action" value="approve" class="btn-approve">Authorize</button>
        <button type="submit" name="action" value="deny" class="btn-deny">Deny</button>
      </div>
    </form>

    <div class="powered">Powered by Secuura Platform K</div>
  </div>

  <!--
    KS-799: the gateway CSRF guard is double-submit-cookie and requires the
    X-XSRF-TOKEN *header*, which a top-level <form> POST cannot set — so a native
    submit is refused 403 CSRF_TOKEN_MISSING. The submit script below posts via
    fetch with the header read from the httpOnly:false XSRF-TOKEN cookie, keeping
    the CSRF choke point intact (no exemption, no CSRF-middleware change).

    Round 2 (Peter's review of PR #881): the script is EXTERNAL, not inline. This
    service sets its own CSP on every response (index.ts: helmet defaults,
    script-src 'self'), the api-gateway proxies /api/oauth/* and http-proxy's
    setHeader replaces the gateway's 'unsafe-inline' with ours, and the production
    nginx gateway sends script-src 'self' as well — browsers enforce the
    intersection. An inline script element is therefore refused at every layer
    and the page silently falls back to the native, headerless POST. A
    same-origin external script (src attribute) is admitted by 'self' everywhere.
    The bytes are served by GET /api/oauth/consent.js on this router
    (CONSENT_SUBMIT_SCRIPT).
  -->
  <script src="/api/oauth/consent.js"></script>
</body>
</html>`;
}

function escapeHtml(s: string): string {
  return s.replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;').replace(/"/g, '&quot;');
}
