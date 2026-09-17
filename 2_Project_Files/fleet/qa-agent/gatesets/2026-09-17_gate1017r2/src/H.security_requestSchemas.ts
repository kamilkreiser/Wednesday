/**
 * =============================================================================
 * REQUEST-BODY SCHEMAS (KS-444)
 * =============================================================================
 * Boundary validators for the security service's write endpoints, mirroring
 * the published request contracts in security.openapi.ts. They live in their
 * own module (rather than index.ts) so unit tests can exercise them without
 * booting the service — index.ts calls app.listen() at module load.
 *
 * Why they exist (KS-444, verified live 2026-07-13):
 *   - POST /api/keys/validate reads `key` (the field the api-gateway's
 *     validateApiKey sends and the spec now publishes); the old truthy check
 *     let a wrong-typed `key` (object/number) through to
 *     crypto.createHash().update(), which throws.
 *   - POST /api/rate-limit/reset answered 200 "Rate limit reset" to a
 *     wrong-typed `key`.
 * =============================================================================
 */

import { z } from 'zod';
import { RATE_LIMIT_KEY_MAX, hasLoneSurrogate } from './rateLimitScope';

/**
 * KS-970 item 4. `z.string().max(n)` counts UTF-16 CODE UNITS; JSON Schema
 * `maxLength` - which is what the published contract carries - counts CODE
 * POINTS. So 256 astral characters are 256 code points and 512 code units:
 * published as valid, refused at runtime. The spec cannot express code units,
 * so the RUNTIME is aligned to the spec rather than the other way round. Still
 * bounded: 256 code points is at most 512 code units, nowhere near the
 * 100,000-character key F10 was filed for.
 */
const boundedByCodePoints = (schema: z.ZodString) =>
  schema.refine((value) => [...value].length <= RATE_LIMIT_KEY_MAX, {
    message: `must not exceed ${RATE_LIMIT_KEY_MAX} characters`,
  });

/**
 * The full scope-field contract for `tenantId` and `userId`, the two body fields
 * that reach the scope encoder.
 *
 * KS-952 F2 - an unpaired surrogate is not representable in UTF-8, so every one
 * encodes to the same replacement bytes and they collide, in the one property
 * this route's scoping exists to establish. Refused at the boundary so no
 * malformed value reaches the encoder.
 *
 * KS-970 item 1 - `min(1)` does not catch a BLANK value: `"   "` has length 3.
 * A blank `tenantId` makes `explicitScope` treat the field as unnamed, so the
 * operator who asked to clear tenant X's bucket cleared THEIR OWN and the route
 * answered `200 "Rate limit reset"`. A wrong action reported as success is the
 * worst shape available, so a present-but-blank scope field is a 400.
 *
 * `key` gets the bound but NOT these two: it is appended RAW and last, never
 * encoded, so nothing malformed can reach the encoder through it.
 *
 * Chained directly rather than composed from named helpers, because
 * each `.refine()` returns a `ZodEffects` and composing them through the
 * `ZodString` helpers needs casts — and a cast that hides a type is how the
 * next person stops trusting the signature.
 */
const scopeField = () =>
  z
    .string()
    .min(1)
    .refine((value) => !hasLoneSurrogate(value), {
      message: 'must not contain an unpaired surrogate',
    })
    .refine((value) => value.trim().length > 0, { message: 'must not be blank' })
    .refine((value) => [...value].length <= RATE_LIMIT_KEY_MAX, {
      message: `must not exceed ${RATE_LIMIT_KEY_MAX} characters`,
    });

/** Body for POST /api/keys/validate — mirrors ApiKeyValidateRequest. */
export const validateKeySchema = z.object({
  key: z.string().min(1),
});

/** Body for POST /api/rate-limit/reset — mirrors RateLimitResetRequest. */
export const resetRateLimitSchema = z.object({
  // KS-952 F10: bounded, matching checkRateLimitSchema.
  // KS-970 item 4: bounded by CODE POINTS, matching the published maxLength.
  key: boundedByCodePoints(z.string().min(1)),
  // KS-952: the SCOPE the key lives under. Only a platform role reaches this
  // route, and naming another tenant's bucket is plausibly what a
  // platform-operator reset is for — so these are how that capability survives
  // /check being bound to its caller. Omitted => the caller's own scope.
  // KS-970 item 1: present-but-BLANK is refused, not treated as omitted.
  tenantId: scopeField().optional(),
  userId: scopeField().optional(),
});
