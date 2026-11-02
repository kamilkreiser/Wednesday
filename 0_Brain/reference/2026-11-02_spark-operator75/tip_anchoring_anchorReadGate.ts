/**
 * =============================================================================
 * KS-1822 — who may READ a stored anchor
 * =============================================================================
 * THE DEFECT. `GET /api/anchors/:id` and `GET /api/anchors/document/:documentId`
 * sit behind `jwtAuthenticate()` alone (index.ts, `app.use('/api', ...)`), and the
 * rows they read are not scoped to anyone: `dbGetAnchorById` selects by id and
 * `dbGetAnchorsByDocument` by document id. So any authenticated caller, in any
 * tenant, could read another tenant's anchor — its content hash, transaction,
 * anchored identity block and signature hash.
 *
 * THE FIX applies the WRITE side's ruled decision table (KS-1603,
 * `mayWriteAnchorRows` in anchorOverwriteGuard.ts) to the two reads, and nothing
 * more. It refuses exactly one thing: a row whose document id is held by a
 * `documents` row in a tenant that is not the caller's. It allows, naming the
 * reason, when:
 *   - no document holds the id (Platform S's flat anchors);
 *   - every id resolves, and to the caller's own tenant;
 *   - the caller carries no usable tenant claim (absent, blank, not uuid-shaped);
 *   - the ownership probe faulted — fail-open, logged at warn, as KS-1603 ruled.
 * `readIdOwners` and `isUuidShaped` are IMPORTED, not copied, so the two gates
 * resolve an id the same way (`external_id` first, then the primary key, read
 * across tenants in one statement). `sameUuid` is not exported there, so the
 * private copy below keeps its semantics exactly; a case-only cell pins it.
 *
 * A REFUSAL READS AS ABSENT. The handler answers the 404 that the SAME request
 * gets when no row exists, status and body byte for byte — never a 403, which
 * would tell the caller the anchor exists (an existence oracle; the H2 note on the
 * `/document` handler already rules out id reflection for that reason). The bodies
 * below restate the route's own absent-row literals, so the cells compare each
 * refusal with the route's real absent answer for the same request: if either
 * side is edited alone, they go red. The server log line names the document id
 * and both tenants; the response names neither.
 *
 * KNOWN GAPS — deliberate, named on KS-1822 and in its pull request:
 *   (i)   a flat anchor (no document holds its id) stays readable by any
 *         authenticated caller: the row records no owner, which needs KS-1384's
 *         tenant column;
 *   (ii)  a caller with no usable tenant claim stays allowed (the KS-1652 hole).
 *         Platform admins are minted with no tenant (auth routes/auth.ts), and so
 *         is a connector key whose metadata has none;
 *   (iii) a probe fault stays allowed (inherited fail-open);
 *   (iv)  two organisations inside one tenant are not separated (KS-1384's
 *         per-organisation rule; KS-1695, KS-1663);
 *   (v)   `GET /api/anchors/thread-state/:documentId`, `/tx/:txHash` and `/queue`
 *         are not gated by this change;
 *   (vi)  an admin reading another tenant's document through originate
 *         (`GET /api/documents/:id` with X-Tenant-Override) forwards a token whose
 *         tenant is the admin's own, so this gate answers 404 and that view no
 *         longer self-heals a stale anchor (KS-535). The document itself is still
 *         served. The registry-fallback branch is the same shape; whether its heal
 *         persists today is UNMEASURED.
 * =============================================================================
 */

import { readIdOwners, isUuidShaped, type AnchorCaller, type IdOwner } from './anchorOverwriteGuard';

/** The one refusal this gate adds — the write gate's, applied to a read. */
export type AnchorReadRefusal = 'document-belongs-to-another-tenant';

export type AnchorReadAllowReason =
  /** No `documents` row in any tenant holds these ids — Platform S's flat anchors. */
  | 'no-document-holds-these-ids'
  /** Every id resolved, and to the caller's own tenant. */
  | 'documents-are-in-callers-tenant'
  /** No usable tenant claim on the caller, so there is nothing to compare. */
  | 'caller-has-no-usable-tenant'
  /** The probe faulted. Fail-open, as KS-1603 ruled for the write side. */
  | 'ownership-probe-unavailable';

export type AnchorReadDecision =
  | { allow: true; reason: AnchorReadAllowReason }
  | { allow: false; reason: AnchorReadRefusal; documentId: string; ownerTenantId: string };

type ReadLog = (level: 'warn', message: string, meta?: Record<string, unknown>) => void;

/** uuids are case-insensitive and Postgres renders them lower-case — anchorOverwriteGuard.ts's `sameUuid`, kept identical. */
function sameUuid(a: string | null | undefined, b: string | null | undefined): boolean {
  if (typeof a !== 'string' || typeof b !== 'string') return false;
  const left = a.trim().toLowerCase();
  const right = b.trim().toLowerCase();
  if (left.length === 0 || right.length === 0) return false;
  return left === right;
}

/**
 * THE GATE. Refuses exactly one thing: a row whose document is in a tenant that is
 * not the caller's. Never throws outward — a probe fault answers "allow", which is
 * develop's behaviour, so the read can never become a 5xx because of this check.
 *
 * `documentIds` are the document ids OF THE ROWS the handler already fetched. When
 * it fetched none there is nothing to disclose and the route's own 404 follows, so
 * the gate answers at once: no probe, and no log line on every miss.
 */
export async function mayReadAnchorRows(
  documentIds: readonly string[],
  caller: AnchorCaller | undefined,
  log?: ReadLog,
): Promise<AnchorReadDecision> {
  if (documentIds.length === 0) return { allow: true, reason: 'no-document-holds-these-ids' };
  const callerTenantId = typeof caller?.tenantId === 'string' ? caller.tenantId.trim() : '';
  if (!isUuidShaped(callerTenantId)) {
    log?.('warn', 'KS-1822: the anchor reader carries no usable tenant claim — allowing the read, as develop does', {
      documentIds: documentIds.slice(0, 8),
      callerTenantIdPresent: callerTenantId.length > 0,
    });
    return { allow: true, reason: 'caller-has-no-usable-tenant' };
  }
  let owners: IdOwner[];
  try {
    owners = await readIdOwners(documentIds);
  } catch (err: unknown) {
    log?.('warn', 'KS-1822: the anchor ownership probe could not read the owning document — allowing the read (fail-open), as develop does', {
      documentIds: documentIds.slice(0, 8),
      error: (err as { message?: string })?.message,
    });
    return { allow: true, reason: 'ownership-probe-unavailable' };
  }
  const foreign = owners.find((o) => !sameUuid(o.ownerTenantId, callerTenantId));
  if (foreign) {
    log?.('warn', 'KS-1822: refused an anchor read — its document is in another tenant; answering as an absent row', {
      documentId: foreign.documentId,
      ownerTenantId: foreign.ownerTenantId,
      callerTenantId,
      callerOrganizationId: caller?.organizationId,
    });
    return { allow: false, reason: 'document-belongs-to-another-tenant', documentId: foreign.documentId, ownerTenantId: foreign.ownerTenantId };
  }
  return { allow: true, reason: owners.length === 0 ? 'no-document-holds-these-ids' : 'documents-are-in-callers-tenant' };
}

/**
 * What `GET /api/anchors/:id` answers when no row exists for `id` — index.ts has two
 * absent-row literals: an `anchor_`-prefixed id gets 'Anchor not found'; any other id
 * goes through the document-id fallback and gets 'No anchor found for this document'
 * with its own input echoed. Every anchor id the service issues is `anchor_`-prefixed
 * (`anchor_<uuid>` single, `anchor_<uuid>_<i>` batch), so a row found by a
 * non-prefixed id was found through the fallback.
 */
export function absentAnchorBody(id: string) {
  return id.startsWith('anchor_')
    ? { success: false, error: { code: 'NOT_FOUND', message: 'Anchor not found' } }
    : { success: false, error: { code: 'NOT_FOUND', message: 'No anchor found for this document', documentId: id } };
}

/** What `GET /api/anchors/document/:documentId` answers when no row exists (the H2 body: no echoed id). */
export const ABSENT_DOCUMENT_ANCHORS_BODY = { success: false, error: { code: 'NOT_FOUND', message: 'No anchors found' } };
