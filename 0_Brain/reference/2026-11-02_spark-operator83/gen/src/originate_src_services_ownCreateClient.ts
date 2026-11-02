/**
 * =============================================================================
 * KS-1384 R2b — originate's client for anchoring's POST /api/anchors/own-create (D4)
 * =============================================================================
 * One POST with the caller's bearer, never retried, bounded by OWN_CREATE_CALL_TIMEOUT_MS (5 s: anchoring's own scan deadline
 * is 4 s, plus 1 s for the hop). Its answer feeds the resolver (anchorResolution.ts) and the retry route's step 3.
 *
 * FAIL-SAFE BY CONSTRUCTION: every way this call can fail is `not-answered`, which the resolver turns into "write nothing"
 * and the retry route into 503 with no POST. Only a well-formed 200 can say `found` or `none`:
 *   - the deadline passes                            -> not-answered, kind `deadline`;
 *   - a fetch error, a non-200 (404 included), a body that is not the declared shape
 *                                                    -> not-answered, kind `unanswered`;
 *   - anchoring's own not-answered                   -> not-answered, with ITS kind (`truncated` | `unanswered`).
 * A `found` without a 64-hex tx is malformed, so not-answered: a bound transaction is the one answer that can confirm a
 * document, so it is the one answer that must not be guessed.
 * =============================================================================
 */
import { isTimeoutError } from './reanchorInFlight';
import type { OwnCreateAnswer, OwnCreateNotAnsweredKind } from './anchorResolution';

export const OWN_CREATE_CALL_TIMEOUT_MS = 5_000;

export interface OwnCreateQuestion {
  documentId: string;
  contentHash: string;
  /** The blob's create attempts (ISO strings), 1 to 10; the newest ten when there are more. */
  timestamps: string[];
}

const TX64 = /^[0-9a-f]{64}$/i;

function strings(v: unknown): string[] {
  return Array.isArray(v) ? v.filter((x): x is string => typeof x === 'string') : [];
}

function notAnswered(kind: OwnCreateNotAnsweredKind, reason: string, loose: string[] = []): OwnCreateAnswer {
  return { outcome: 'not-answered', kind, reason, loose };
}

/** Maps anchoring's 200 body to the resolver's answer; anything not of the declared shape is `unanswered`. */
export function readOwnCreateBody(body: unknown): OwnCreateAnswer {
  const data = (body as { data?: Record<string, unknown> } | null | undefined)?.data;
  if (!data || typeof data !== 'object') return notAnswered('unanswered', 'own-create answered without a data object');
  const loose = strings(data.loose);
  if (data.outcome === 'found') {
    const bound = data.bound as { tx?: unknown; blockNumber?: unknown } | undefined;
    const tx = typeof bound?.tx === 'string' ? bound.tx : '';
    if (!TX64.test(tx)) return notAnswered('unanswered', 'own-create answered found without a 64-hex transaction', loose);
    const blockNumber = typeof bound?.blockNumber === 'number' ? bound.blockNumber : null;
    return { outcome: 'found', tx: tx.toLowerCase(), blockNumber, loose };
  }
  if (data.outcome === 'none') return { outcome: 'none', loose };
  if (data.outcome === 'not-answered') {
    const kind: OwnCreateNotAnsweredKind = data.kind === 'truncated' ? 'truncated' : 'unanswered';
    const reason = typeof data.reason === 'string' && data.reason.length > 0 ? data.reason : 'own-create did not answer';
    return notAnswered(kind, reason, loose);
  }
  return notAnswered('unanswered', 'own-create answered an outcome it does not declare');
}

/** The call itself. Never throws. */
export async function askOwnCreate(
  fetchImpl: typeof fetch,
  anchoringBase: string,
  authHeader: string,
  q: OwnCreateQuestion,
): Promise<OwnCreateAnswer> {
  if (q.timestamps.length === 0) return notAnswered('unanswered', 'the document records no create attempt to bind to');
  try {
    const resp = await fetchImpl(`${anchoringBase}/api/anchors/own-create`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', ...(authHeader ? { Authorization: authHeader } : {}) },
      body: JSON.stringify({ documentId: q.documentId, contentHash: q.contentHash, timestamps: q.timestamps.slice(-10) }),
      signal: AbortSignal.timeout(OWN_CREATE_CALL_TIMEOUT_MS),
    });
    if (resp.status !== 200) return notAnswered('unanswered', `own-create answered HTTP ${resp.status}`);
    let body: unknown;
    try {
      body = await resp.json();
    } catch (err: unknown) {
      // The timeout signal also bounds the body read, so a deadline can land here too.
      if (isTimeoutError(err)) return notAnswered('deadline', `own-create did not answer within ${OWN_CREATE_CALL_TIMEOUT_MS} ms`);
      return notAnswered('unanswered', 'own-create answered a body that is not JSON');
    }
    return readOwnCreateBody(body);
  } catch (err: unknown) {
    if (isTimeoutError(err)) return notAnswered('deadline', `own-create did not answer within ${OWN_CREATE_CALL_TIMEOUT_MS} ms`);
    return notAnswered('unanswered', `own-create could not be reached: ${err instanceof Error ? err.message : String(err)}`);
  }
}
