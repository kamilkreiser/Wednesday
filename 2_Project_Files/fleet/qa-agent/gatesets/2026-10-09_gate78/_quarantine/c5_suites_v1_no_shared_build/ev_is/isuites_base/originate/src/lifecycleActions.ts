/**
 * =============================================================================
 * LIFECYCLE EVENT ACTIONS — KS-387 vocabulary subset for /lifecycle-events
 * =============================================================================
 * The KS-134 master S↔K verbs that have NO dedicated K endpoint and therefore
 * route through the generic POST /api/documents/{id}/lifecycle-events. Verbs
 * WITH dedicated endpoints (share, transfer-custody, revoke, certify, sign,
 * upload/version) are deliberately NOT accepted here — S routes those to their
 * own endpoints, and accepting them twice would double-record lifecycle rows.
 *
 * - rights-unassign / share-revoke / share-permission-change: the original
 *   KS-387 gap (previously flat-anchored with no lineage).
 * - rename: accepted now; S sends it once PS-64 (filename stability) and its
 *   net-new TransactionAction.Rename land — nothing K-side blocks it.
 * - delete / restore: the KS-389 decision (2026-07-08) — S's owner-local,
 *   recoverable soft-delete records here as a lifecycle event, NEVER as K
 *   /revoke (which is a terminal global withdrawal); restore is its reserved
 *   inverse.
 * - share-recipient-change / share-expiry-change / share-token-rotate /
 *   share-resend: the four PS-235 share-edit verbs (KS-415) — exactly the
 *   KS-387 shape (non-mutating, attach to the current doc, no dedicated K
 *   endpoint). Payload shapes documented on PS-235.
 * - share-attach-consent: the PS-458 verb (KS-534) — the sender's consent to
 *   email an UNCONTROLLED copy as an attachment (a release Secuura cannot
 *   revoke, expire or access-log). Same KS-387 shape, with one semantic
 *   difference worth knowing: it is NOT governed by live share-link state, so
 *   revoking/expiring the link never invalidates the consent. NOTE (PII): the
 *   S-side payload carries `recipientEmails[]` in S's OWN store only — S sends
 *   no payload on this endpoint (verified KS-537). Since KS-537 the payload
 *   column is encrypted at rest and covered by GDPR erasure, but the contract
 *   stands: send counts/opaque references (`recipientCount`), never addresses.
 *
 * Kept as its own module so the route, the OpenAPI registration, and the unit
 * tests share one source of truth. The full vocabulary + contract live in
 * Blockchain/Dev/docs/VOCABULARY.md — keep the two in lockstep.
 */

export const LIFECYCLE_EVENT_ACTIONS = [
  'rights-unassign',
  'share-revoke',
  'share-permission-change',
  'rename',
  'delete',
  'restore',
  'share-recipient-change',
  'share-expiry-change',
  'share-token-rotate',
  'share-resend',
  'share-attach-consent',
  // KS-556: S's document-protection toggle (edit/delete guard) — real S
  // lifecycle events with no dedicated K endpoint, exactly the KS-387 shape
  // (non-mutating, attach to the current doc). Pairs with the existing
  // delete/restore entries above; per PS-499 S stops omitting documentType
  // for these once this lands.
  'protect',
  'unprotect',
  // KS-1172 (Stuart 2026-09-15): `note` (a user's short note on a document; payload = noteSha256/noteLength only)
  // `certified` (the Certify FLOW completed) and `verified` (the Verify FLOW completed) — KS-1173. All non-mutating,
  // KS-387 shape; paired in anchorSchema.ts.
  'note',
  'certified',
  'verified',
] as const;

export type LifecycleEventAction = (typeof LIFECYCLE_EVENT_ACTIONS)[number];
