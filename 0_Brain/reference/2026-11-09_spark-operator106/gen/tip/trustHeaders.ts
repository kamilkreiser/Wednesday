/**
 * =============================================================================
 * Edge strip — identity/authorization-trust headers the gateway SETS, never
 * RECEIVES.
 * =============================================================================
 * Extracted from index.ts so it can be tested against the real pattern rather
 * than a copy. A test that re-declares the regex proves only that the copy
 * behaves; the thing that must hold is that THIS pattern, the one mounted on
 * every inbound request, removes what it claims to.
 *
 * These headers are set from a verified JWT (middleware/auth.ts) and are
 * meaningless — worse, dangerous — when a client supplies them: without the
 * strip, any caller can spoof identity, tenant, organization or role by
 * sending the header (audit finding A-01, the keystone that unblocks A-06,
 * A-08 and A-09 trivially).
 *
 * KS-566: `x-emitter-internal` marks K's OWN originate -> anchoring hops so
 * anchoring can tell them from Platform-S's genuine flat-anchor fallback.
 * This edge strip covers `/api/*` and is NOT what makes the marker
 * non-spoofable on its own: the nginx `/originate/` bypass route answers 404
 * (#938), but the flat compose network still reaches `originate:4000`
 * directly, so originate strips the marker at its own inbound as well
 * (`services/originate/src/utils/gatewayProvenance.ts`,
 * `createEmitterMarkerStrip`, KS-741). The marker is protected by BOTH strips.
 *
 * KS-1041 Step 2: `x-gateway-vouch` is the gateway's proof to originate that a
 * request came through the edge. It MUST be in this pattern. If a client could
 * supply it, the vouch would be forgeable by exactly the callers it exists to
 * exclude — the same hole with a new name. The strip and the check in
 * `services/originate/src/utils/gatewayProvenance.ts` must change together.
 */

/**
 * EXCEPTION: `x-tenant-override` is intentional super-admin functionality (the
 * admin portal's tenant selector). It is a *request* — auth middleware decides
 * whether to honour it based on the verified JWT's role, gating on
 * SUPER_ADMIN_ROLES before doing so. The blanket strip added 2026-04-25
 * (c796138f0) was matching it too, which broke the override path silently for
 * two weeks and made KS-4 untestable.
 */
export const TRUST_HEADER_ALLOW_LIST = new Set(['x-tenant-override']);

export const TRUST_HEADER_PATTERN =
  /^x-(user|tenant|organization|org|role|roles?|auth-user|policy|emitter|gateway-vouch)(-|$)/i;

/** True when the header must be removed from an inbound client request. */
export function isStrippedTrustHeader(header: string): boolean {
  return (
    TRUST_HEADER_PATTERN.test(header) && !TRUST_HEADER_ALLOW_LIST.has(header.toLowerCase())
  );
}

/** Mutates `headers` in place, removing every client-supplied trust header. */
export function stripTrustHeaders(headers: Record<string, unknown>): void {
  for (const header of Object.keys(headers)) {
    if (isStrippedTrustHeader(header)) {
      delete headers[header];
    }
  }
}
