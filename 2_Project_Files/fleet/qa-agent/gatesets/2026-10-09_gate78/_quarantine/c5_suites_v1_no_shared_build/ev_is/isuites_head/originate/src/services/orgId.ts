/**
 * =============================================================================
 * Organisation-id normalisation — ONE implementation, re-exported (QA F-4 / KS-780)
 * =============================================================================
 * `resolveOnBehalfOf` (provenance.ts), the GDPR subject resolver
 * (gdprService.ts) and the documents route's caller-scoped externalRef check
 * all compare a PG-canonical `organization_id` against a connector-supplied
 * claim that nothing normalises. Each was fixed by a local `norm`, and the
 * copies were byte-identical.
 *
 * Peter Obeden's review of #795 made the point that two identical private copies
 * is precisely the arrangement that produced the drift in the first place: fix a
 * normalisation bug in one — NFKC, a `::uuid` canonicalisation, a locale-aware
 * lowercase — and the other sits there looking correct. This module was that
 * consolidation for originate.
 *
 * WHY IT IS NOW A RE-EXPORT (KS-780). This module used to justify staying
 * service-local because "nothing outside it compares organisation ids this
 * way". That stopped being true when the API-key revoke policy in
 * `@secuura/shared` (`security/keyRevokePolicy.ts`) grew an organisation arm
 * and — unable to import from a service — carried its own byte-identical copy,
 * on a DESTRUCTIVE surface. Two layers, two implementations, neither able to
 * witness the other drifting. The implementation now lives once, in
 * `@secuura/shared` (`security/orgId.ts`), beside the policy that needs it; this
 * module re-exports it so every existing originate import line is unchanged.
 * `git grep` finds one definition.
 *
 * The two PROPERTIES the callers rely on are unchanged: a whitespace-only or
 * empty value is `null` rather than a distinct id (blank is absent), and case is
 * not identity — a PG-canonical lowercase uuid and a caller's upper-cased
 * rendering of the same uuid are the SAME organisation.
 *
 * The stale-`dist/` trap this file's old docblock warned about is real and is
 * now this module's too: a service test that fails with "normaliseOrgId is not
 * a function" is reading a stale `packages/shared/dist`, not a defect here —
 * `npm run build --workspace=packages/shared` first (BACKLOG.md).
 * =============================================================================
 */

export { normaliseOrgId } from '@secuura/shared';
