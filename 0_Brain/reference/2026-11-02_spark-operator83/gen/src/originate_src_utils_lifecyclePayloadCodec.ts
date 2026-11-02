/**
 * =============================================================================
 * LIFECYCLE PAYLOAD CODEC — KS-537 at-rest encryption for
 * `document_lifecycle_events.payload`
 * =============================================================================
 * The payload column accepts caller-supplied free-form JSON, and the published
 * contract's own example taught callers to put an email in it — so the blob is
 * treated as PII-bearing and encrypted at rest with the platform keyring, AAD
 * bound to `document_lifecycle_events.payload.<eventId>` (the
 * `audit_logs.details` pattern from the security service).
 *
 * Storage shape: a NON-EMPTY payload is stored as a JSONB *string* containing
 * the `v<N>:iv:tag:ciphertext` token (no migration — the column stays jsonb).
 * An empty `{}` stays a plaintext `{}` (nothing to protect, and the common
 * case stays queryable). Legacy plaintext-object rows decode as-is until
 * touched (migration-window tolerance, same as audit_logs.details).
 *
 * Lives in its own module (no uuid import) so it stays loadable under jest —
 * the repository's own suite is dead to the uuid-v14 ESM issue (BACKLOG).
 */

import { encryptField, decryptField, isEncryptedPii } from '@secuura/shared';
import { logger } from './logger';

const context = (eventId: string): string => `document_lifecycle_events.payload.${eventId}`;

import { ERASED_MARKER } from './erasureMarker';

/**
 * Encode a payload for storage. Returns the string to bind as `::jsonb`.
 * `{}` passes through unencrypted; anything else becomes a JSONB string
 * holding the ciphertext token.
 */
export function encodeLifecyclePayload(payload: Record<string, unknown>, eventId: string): string {
  if (Object.keys(payload).length === 0) return '{}';
  const token = encryptField(JSON.stringify(payload), context(eventId));
  // encryptField only returns null for null/'' input, which can't happen here.
  return JSON.stringify(token);
}

/**
 * Decode a stored payload column value back to the plaintext object.
 * Tolerates: encrypted JSONB-string rows (current), legacy plaintext objects
 * (pre-KS-537), and plaintext JSON strings. A decrypt failure returns a
 * `payloadUnavailable` marker rather than throwing — one unreadable row must
 * not fail a listing — and logs the event id for the no-skip trail.
 */
export function decodeLifecyclePayload(raw: unknown, eventId: string): Record<string, unknown> {
  if (raw == null) return {};
  if (typeof raw === 'string') {
    if (isEncryptedPii(raw)) {
      try {
        const plain = decryptField(raw, context(eventId));
        return plain ? (JSON.parse(plain) as Record<string, unknown>) : {};
      } catch (err) {
        logger.error('lifecycle payload decrypt failed', {
          eventId,
          error: err instanceof Error ? err.message : String(err),
        });
        return { payloadUnavailable: true };
      }
    }
    try {
      return JSON.parse(raw) as Record<string, unknown>;
    } catch {
      return {};
    }
  }
  return raw as Record<string, unknown>;
}

/**
 * Deep-erase a subject's email from a decoded payload (KS-537 erasure step).
 * Every string value containing the email (case-insensitive) has each
 * occurrence replaced with `[erased]` — containment, not equality, because
 * observed shapes embed the address inside larger strings
 * (`"First Last (email@example.com)"`). Non-string leaves are untouched.
 * Returns the (new) value and whether anything changed.
 */
export function eraseEmailDeep(
  value: unknown,
  email: string | undefined,
): { value: unknown; changed: boolean } {
  if (!email) return { value, changed: false };
  if (typeof value === 'string') {
    const idx = value.toLowerCase().indexOf(email.toLowerCase());
    if (idx === -1) return { value, changed: false };
    const pattern = new RegExp(email.replace(/[.*+?^${}()|[\]\\]/g, '\\$&'), 'gi');
    return { value: value.replace(pattern, ERASED_MARKER), changed: true };
  }
  if (Array.isArray(value)) {
    let changed = false;
    const out = value.map((v) => {
      const r = eraseEmailDeep(v, email);
      changed = changed || r.changed;
      return r.value;
    });
    return { value: out, changed };
  }
  if (value !== null && typeof value === 'object') {
    let changed = false;
    const out: Record<string, unknown> = {};
    for (const [k, v] of Object.entries(value as Record<string, unknown>)) {
      const r = eraseEmailDeep(v, email);
      changed = changed || r.changed;
      out[k] = r.value;
    }
    return { value: out, changed };
  }
  return { value, changed: false };
}
