/**
 * JWKS endpoint (KS-182)
 *
 * Publishes the auth service's RS256 public signing key as a JSON Web Key Set at
 * `GET /.well-known/jwks.json`, so verifier services (KS-183) can fetch + cache
 * the public key and verify RS256 tokens without holding any secret. Rotation is
 * a key swap: a new `kid` appears here, old verifiers refetch on an unknown kid.
 *
 * While auth is still HS256-only (no asymmetric key provisioned), `keys` is an
 * empty array — there is no public key to publish yet.
 */
import { Router, Request, Response } from 'express';
import crypto from 'crypto';
import { getActiveJwk } from '../services/jwt';

/**
 * Build the JWKS document from the active signing key. Returns `{ keys: [] }`
 * when signing is still HS256-only.
 */
export function buildJwks(): { keys: Array<Record<string, unknown>> } {
  const active = getActiveJwk();
  if (!active) {
    return { keys: [] };
  }
  // Export the RSA public key as a JWK (kty/n/e), then annotate it for verifiers.
  const jwk = crypto.createPublicKey(active.publicKeyPem).export({ format: 'jwk' }) as Record<string, unknown>;
  return {
    keys: [
      {
        ...jwk,
        use: 'sig',
        alg: active.alg,
        ...(active.kid ? { kid: active.kid } : {}),
      },
    ],
  };
}

export const jwksRoutes = Router();

jwksRoutes.get('/jwks.json', (_req: Request, res: Response) => {
  // Public + cacheable. Verifiers fetch and cache; a key rotation publishes a
  // new kid and they refetch on first sight of an unknown one.
  res.set('Cache-Control', 'public, max-age=300');
  res.json(buildJwks());
});
