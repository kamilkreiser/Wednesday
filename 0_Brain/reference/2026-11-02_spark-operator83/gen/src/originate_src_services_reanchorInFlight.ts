/**
 * =============================================================================
 * KS-1384 R1 step 4 — before the retry route POSTs, is an attempt still in flight? (design rev 4 §6 D; the fourth
 * review's M-4)
 * =============================================================================
 * The retry route (`POST /api/documents/:id/anchor`) used to POST a new anchor whenever the document's blob read
 * `anchor_failed` or was absent. But the blob and anchoring's own row can disagree: a holder that crashed after its
 * POST leaves a blob with no outcome while anchoring's row is still `pending`, `submitting` or `submitted`, and a
 * second POST then resets that row and pays a second fee. So the route asks anchoring first, with the caller's bearer:
 * `GET /api/anchors/document/:documentId`.
 *
 *   - any row `pending`, `submitting` or `submitted`, at any age -> IN FLIGHT: answer 409 naming it, POST nothing;
 *   - a `confirmed` row that is this document's anchor for this content on this network -> ANCHORED: answer 409 naming
 *     it, POST nothing (KS-1384 R2a, below);
 *   - rows, none of them in flight or anchored -> ABSENT: go on and POST;
 *   - a 404 -> ABSENT, UNLESS it is ambiguous (below);
 *   - a fetch error, a non-2xx other than 404, or a 2xx without an `anchors` array -> UNAVAILABLE: 503, POST nothing.
 *
 * WHY A 404 CAN BE AMBIGUOUS (M-4). Since KS-1822 the anchor read gate (anchoring `anchorReadGate.ts`,
 * `mayReadAnchorRows`) answers a foreign tenant's rows with a body byte-identical to "no rows". It refuses exactly one
 * case: the caller's token carries a usable (uuid-shaped) tenant claim, and a row's document belongs to another tenant.
 * This route found the document under `documentTenantId`, so when the token's tenant claim is uuid-shaped and is NOT
 * that tenant, a 404 may be the gate refusing, not absence; and a blob that already names an `anchorId` has had a row
 * at some point. Both are read as UNAVAILABLE, never as absent, so a refusal can never become a second paid POST.
 * Residual, stated in the PR: the gate's per-id collision (KS-1822 gap (i)) can refuse while tenants match. Today the
 * write gate on the same table refuses that POST too, so no fee is paid, but this rests on the two gates moving in
 * lockstep. The structural answer is a service-identity read, which is not in R1's file set.
 *
 * originate's tenant-scoped `getDocument(id, tenantId)` stays the real authorisation boundary for this route; this
 * module only decides whether a POST could duplicate one already in flight.
 * =============================================================================
 */

/** Anchoring's statuses for an attempt that may still land (anchorSubmission.ts; `submitting` is the write-ahead). */
export const IN_FLIGHT_STATUSES: readonly string[] = ['pending', 'submitting', 'submitted'];

/**
 * KS-1384 R1 round 2 (gate 58 G58-F1): the retry route's two anchoring calls are bounded. Before round 2 neither passed a
 * signal, so a stalled call (Node's defaults allow minutes) could outlast the claim's 10-minute lease
 * (documentRepo REANCHOR_CLAIM_TTL_MS) and a newer retry could take the document over while the old holder still meant to
 * POST: two fees. The route already gives the users/stub call 5 s.
 *
 * KS-1384 R1 round 3 (gate 61 G61-F1, item 2): the POST has TWO deadlines, one to its answer's headers and one, after a 2xx
 * header, to its body. In round 2 one 10 s signal covered both, so a 202 whose headers had ARRIVED was thrown away when its
 * body was slow (gate 61's P3c). The whole budget is read 5 s + headers 10 s + body 10 s = 25 s, 1/24 of the lease.
 */
export const REANCHOR_READ_TIMEOUT_MS = 5_000;
export const REANCHOR_POST_TIMEOUT_MS = 10_000;
export const REANCHOR_POST_BODY_TIMEOUT_MS = 10_000;

/** True for the rejection a fetch gives when its AbortSignal.timeout fires (a DOMException named TimeoutError, or AbortError). */
export function isTimeoutError(err: unknown): boolean {
  const name = (err as { name?: unknown } | null)?.name;
  return name === 'TimeoutError' || name === 'AbortError';
}

/** The same shape the anchoring gate tests a tenant claim with (anchorOverwriteGuard.ts `UUID_SHAPE`), kept identical. */
const UUID_SHAPE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;

export type InFlightDecision =
  | { kind: 'absent'; reason: string }
  | { kind: 'in-flight'; anchorId: string; status: string }
  | { kind: 'anchored'; anchorId: string; reason: string }
  /** KS-1384 R1 round 3: the blob records a POST whose outcome is unknown, and anchoring holds a row for the document. */
  | { kind: 'maybe-landed'; anchorId: string; status: string }
  | { kind: 'unavailable'; reason: string };

export interface InFlightAnswer {
  /** The HTTP status anchoring answered, or null when the fetch itself failed. */
  httpStatus: number | null;
  /** The parsed JSON body, or undefined. */
  body?: unknown;
  /** The fetch error's message, when `httpStatus` is null. */
  fetchError?: string;
}

export interface InFlightContext {
  /** The `tenantId` claim of the bearer the route forwards (what the anchoring gate compares). */
  tokenTenantId: unknown;
  /** The tenant this route found the document under. */
  documentTenantId: string;
  /** `blockchain.anchorId` from the document's blob, if any. */
  blobAnchorId: unknown;
  /** KS-1384 R2a: the document's content hash, as the route would POST it (normalised here: `sha256:` stripped, lower case). */
  documentContentHash: unknown;
  /** KS-1384 R2a: the network the route would POST to (its CARDANO_NETWORK). */
  network: unknown;
  /**
   * KS-1384 R1 round 3 (gate 61 G61-F1): the blob carries `retryPostUnknownAt`, a re-anchor POST whose outcome is unknown.
   * Anchoring writes its row before it spends the fee, so with this set ANY row for the document, `confirmed` and `failed`
   * included, may be that POST's: it is refused as landed, never read as absent.
   */
  postOutcomeUnknown?: boolean;
}

/**
 * KS-1384 R2a (QA gate 58, G58-F2): a LANDED anchor is "already anchored, do not pay". Before R2a a `confirmed` row read as
 * "nothing in flight", so the retry POSTed again; anchoring's upsert resets a confirmed (document_id, network) row and
 * submits it again, which pays a second fee for a document already on chain (gate 58's Q3a: a holder that crashed after
 * its POST, once its claim is stale; Q3b: an `anchor_failed` blob whose row later confirmed).
 * Wednesday's rule (2026-10-31): a `confirmed` row is this document's anchor when its network is the route's AND its
 * content hash equals the document's (both normalised). A row whose network or hash is missing or unreadable counts as
 * anchored too: fail toward not paying. A row with a readable DIFFERENT hash, or on another network, is not this content's
 * anchor and the retry proceeds as before (anchoring's KS-1385 overwrite guard decides what an upsert may replace).
 *
 * KS-1384 R2b (QA gate 68, G68-F1; Wednesday's ruling 2026-10-31 20:51:12Z): the NETWORK leg is dropped. Anchoring writes
 * ITS OWN CARDANO_NETWORK into every row (it ignores the request's) and keeps one row per (document_id, that network), so a
 * confirmed row it returns for this document is on the very network a POST would pay on. Comparing it with ORIGINATE's
 * CARDANO_NETWORK only ever differed where the two services were configured differently, and there every landed anchor
 * read as "another network" and was paid for again (gate 68's N-R3, N-Q3b, N-R4). The hash leg is unchanged. The deploy hold
 * also requires the two services' CARDANO_NETWORK to be equal on each box.
 */
function normalisedHash(v: unknown): string | null {
  if (typeof v !== 'string') return null;
  const h = v.trim().replace(/^sha256:/i, '').toLowerCase();
  return h.length > 0 ? h : null;
}
/** True when a `confirmed` row counts as this document's anchor for this content (rule above; the network is not compared). */
export function isLandedForThisContent(row: { contentHash?: unknown }, ctx: Pick<InFlightContext, 'documentContentHash'>): boolean {
  const rowHash = normalisedHash(row.contentHash);
  const docHash = normalisedHash(ctx.documentContentHash);
  if (rowHash !== null && docHash !== null && rowHash !== docHash) return false;
  return true;
}

function sameUuid(a: string, b: string): boolean {
  return a.trim().toLowerCase() === b.trim().toLowerCase();
}

/** Pure: what the answer means for the retry. */
export function decideInFlight(answer: InFlightAnswer, ctx: InFlightContext): InFlightDecision {
  if (answer.httpStatus === null) {
    return { kind: 'unavailable', reason: `the anchoring service could not be read: ${answer.fetchError ?? 'unknown error'}` };
  }
  if (answer.httpStatus === 404) {
    const token = typeof ctx.tokenTenantId === 'string' ? ctx.tokenTenantId.trim() : '';
    if (UUID_SHAPE.test(token) && !sameUuid(token, ctx.documentTenantId)) {
      return { kind: 'unavailable', reason: 'a 404 under a token whose tenant is not the document\'s may be the read gate refusing (M-4)' };
    }
    if (typeof ctx.blobAnchorId === 'string' && ctx.blobAnchorId.length > 0) {
      return { kind: 'unavailable', reason: `a 404 for a document whose blob names ${ctx.blobAnchorId} is not absence (M-4)` };
    }
    return { kind: 'absent', reason: 'no anchor row for this document' };
  }
  if (answer.httpStatus < 200 || answer.httpStatus > 299) {
    return { kind: 'unavailable', reason: `the anchoring service answered ${answer.httpStatus}` };
  }
  const anchors = (answer.body as { data?: { anchors?: unknown } } | undefined)?.data?.anchors;
  if (!Array.isArray(anchors)) {
    return { kind: 'unavailable', reason: 'the anchoring service answered without an anchors list' };
  }
  for (const a of anchors as Array<{ id?: unknown; status?: unknown }>) {
    if (typeof a?.status === 'string' && IN_FLIGHT_STATUSES.includes(a.status)) {
      return { kind: 'in-flight', anchorId: String(a.id ?? ''), status: a.status };
    }
  }
  // KS-1384 R2a (G58-F2): after the in-flight rows, a landed one. Before R2a a confirmed row fell through to ABSENT.
  for (const a of anchors as Array<{ id?: unknown; status?: unknown; contentHash?: unknown; network?: unknown }>) {
    if (a?.status === 'confirmed' && isLandedForThisContent(a, ctx)) {
      return { kind: 'anchored', anchorId: String(a.id ?? ''), reason: 'a confirmed anchor for this content on this network' };
    }
  }
  // KS-1384 R1 round 3 (G61-F1), merged after R2a's landed check: before round 3 a row that had CONFIRMED read as absent here, so the retry after a
  // POST whose outcome was unknown paid a second fee for an anchor that had landed (gate 61's P3b, P3c). With the marker set,
  // any row is that POST's as far as this route can tell.
  if (ctx.postOutcomeUnknown && anchors.length > 0) {
    const a = anchors[0] as { id?: unknown; status?: unknown };
    return { kind: 'maybe-landed', anchorId: String(a?.id ?? ''), status: typeof a?.status === 'string' ? a.status : '' };
  }
  return { kind: 'absent', reason: `${anchors.length} anchor row(s), none in flight or anchored for this content` };
}

/** The read itself: one GET with the caller's bearer, never retried, bounded by REANCHOR_READ_TIMEOUT_MS. */
export async function readInFlightAnchor(
  fetchImpl: typeof fetch,
  anchoringBase: string,
  authHeader: string,
  documentId: string,
  ctx: InFlightContext,
): Promise<InFlightDecision> {
  let answer: InFlightAnswer;
  try {
    const resp = await fetchImpl(`${anchoringBase}/api/anchors/document/${encodeURIComponent(documentId)}`, {
      method: 'GET',
      headers: authHeader ? { Authorization: authHeader } : {},
      // KS-1384 R1 round 2: a read that does not answer in time is a fetch error below, so UNAVAILABLE: 503, no POST.
      signal: AbortSignal.timeout(REANCHOR_READ_TIMEOUT_MS),
    });
    let body: unknown;
    try { body = await resp.json(); } catch { body = undefined; }
    answer = { httpStatus: resp.status, body };
  } catch (err: unknown) {
    answer = { httpStatus: null, fetchError: err instanceof Error ? err.message : String(err) };
  }
  return decideInFlight(answer, ctx);
}

/**
 * KS-1384 R1 round 3 (gate 61 G61-F1, item 2): what the re-anchor POST came to.
 *   - answered            anchoring answered and, for a 2xx, its body was read (`body` undefined when it is not JSON);
 *   - unknown             no answer's headers within REANCHOR_POST_TIMEOUT_MS: the POST may have landed;
 *   - accepted-body-lost  a 2xx's headers ARRIVED but its body did not, within REANCHOR_POST_BODY_TIMEOUT_MS, or the body
 *                         read failed: anchoring accepted the POST, so it is treated as landed with its anchorId unknown;
 *   - failed              the request failed another way before any answer (for example, connection refused).
 */
export type ReanchorPostOutcome =
  | { kind: 'answered'; status: number; body: unknown }
  | { kind: 'unknown'; reason: string }
  | { kind: 'accepted-body-lost'; status: number; reason: string }
  | { kind: 'failed'; error: string };

/**
 * The POST itself, never retried, with its two deadlines. One AbortController carries both: the header timer is cleared when
 * the headers arrive, and the body timer starts only after a 2xx header. Every timer is cleared before this returns.
 */
export async function postReanchor(
  fetchImpl: typeof fetch,
  url: string,
  init: Omit<RequestInit, 'signal'>,
  deadlines: { headerMs: number; bodyMs: number } = { headerMs: REANCHOR_POST_TIMEOUT_MS, bodyMs: REANCHOR_POST_BODY_TIMEOUT_MS },
): Promise<ReanchorPostOutcome> {
  const abort = new AbortController();
  // An object, not a `let`: TypeScript would narrow a `let` assigned only inside the timer callback to `null`.
  const timers: { fired: 'headers' | 'body' | null } = { fired: null };
  const arm = (ms: number, phase: 'headers' | 'body') => setTimeout(() => {
    timers.fired = phase;
    abort.abort(new DOMException(`no ${phase} within ${ms} ms`, 'TimeoutError'));
  }, ms);
  const message = (err: unknown) => (err instanceof Error ? err.message : String(err));

  let resp: Response;
  const headerTimer = arm(deadlines.headerMs, 'headers');
  try {
    resp = await fetchImpl(url, { ...init, signal: abort.signal });
  } catch (err: unknown) {
    if (timers.fired === 'headers' || isTimeoutError(err)) {
      return { kind: 'unknown', reason: `no answer within ${deadlines.headerMs} ms` };
    }
    return { kind: 'failed', error: message(err) };
  } finally {
    clearTimeout(headerTimer);
  }
  if (!resp.ok) return { kind: 'answered', status: resp.status, body: undefined };

  const bodyTimer = arm(deadlines.bodyMs, 'body');
  let text: string;
  try {
    text = await resp.text();
  } catch (err: unknown) {
    const why = timers.fired === 'body' || isTimeoutError(err) ? `the body did not arrive within ${deadlines.bodyMs} ms` : `the body read failed: ${message(err)}`;
    return { kind: 'accepted-body-lost', status: resp.status, reason: why };
  } finally {
    clearTimeout(bodyTimer);
  }
  let body: unknown;
  try { body = JSON.parse(text); } catch { body = undefined; }
  return { kind: 'answered', status: resp.status, body };
}
