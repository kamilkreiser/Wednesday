/**
 * =============================================================================
 * KS-537 — lifecycle payload codec unit tests (REAL crypto, no mocks)
 * =============================================================================
 * `document_lifecycle_events.payload` is caller-supplied free-form JSON that
 * the published contract used to seed with an email — so it is encrypted at
 * rest (platform keyring, AAD = `document_lifecycle_events.payload.<id>`) and
 * pseudonymised on GDPR erasure. These tests run the real AES-GCM path: the
 * codec lives in its own uuid-free module precisely so this suite stays
 * loadable while the repository's own suite is dead to the uuid-v14 ESM issue.
 * =============================================================================
 */

import { registerKey, setActiveVersion, __resetKeyringForTesting, isEncryptedPii } from '@secuura/shared';
import {
  encodeLifecyclePayload,
  decodeLifecyclePayload,
  eraseEmailDeep,
} from '../utils/lifecyclePayloadCodec';
import { ERASED_MARKER } from '../utils/erasureMarker';

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

const EVENT_ID = '9f0d76a2-0000-4000-8000-000000000001';

beforeAll(() => {
  __resetKeyringForTesting();
  registerKey(1, 'a'.repeat(64));
  setActiveVersion(1);
});

afterAll(() => __resetKeyringForTesting());

describe('encodeLifecyclePayload', () => {
  it('stores a non-empty payload as an encrypted JSONB string (no plaintext leakage)', () => {
    const stored = encodeLifecyclePayload({ subjectEmail: 'holder@example.com' }, EVENT_ID);
    // The stored value is a JSON string wrapping the ciphertext token…
    const token = JSON.parse(stored);
    expect(typeof token).toBe('string');
    expect(isEncryptedPii(token)).toBe(true);
    // …and carries no plaintext.
    expect(stored).not.toContain('holder@example.com');
    expect(stored).not.toContain('subjectEmail');
  });

  it('keeps the empty payload as plaintext {} (common case stays queryable)', () => {
    expect(encodeLifecyclePayload({}, EVENT_ID)).toBe('{}');
  });
});

describe('decodeLifecyclePayload', () => {
  it('round-trips an encrypted payload', () => {
    const payload = { note: 'released to A. Holder (holder@example.com)', count: 3 };
    const stored = encodeLifecyclePayload(payload, EVENT_ID);
    expect(decodeLifecyclePayload(JSON.parse(stored), EVENT_ID)).toEqual(payload);
  });

  it('is AAD-bound: the same ciphertext under another event id refuses to decrypt', () => {
    const stored = encodeLifecyclePayload({ secret: 'x' }, EVENT_ID);
    const decoded = decodeLifecyclePayload(JSON.parse(stored), 'other-event-id');
    expect(decoded).toEqual({ payloadUnavailable: true });
  });

  it('passes legacy plaintext-object rows through unchanged (migration tail)', () => {
    const legacy = { subjectEmail: 'holder@example.com' };
    expect(decodeLifecyclePayload(legacy, EVENT_ID)).toEqual(legacy);
  });

  it('handles null and empty-object rows', () => {
    expect(decodeLifecyclePayload(null, EVENT_ID)).toEqual({});
    expect(decodeLifecyclePayload({}, EVENT_ID)).toEqual({});
  });
});

describe('eraseEmailDeep', () => {
  const EMAIL = 'subject@example.com';

  it('replaces the bare address and embedded occurrences, case-insensitively', () => {
    const { value, changed } = eraseEmailDeep(
      {
        subjectEmail: 'Subject@Example.com',
        note: 'released to Subject Person (subject@example.com) on request',
        nested: { list: ['subject@example.com', 'other@example.com'] },
      },
      EMAIL,
    );
    expect(changed).toBe(true);
    expect(JSON.stringify(value)).not.toMatch(/subject@example\.com/i);
    // QA F-9: these are ASSERTIONS about the sentinel eraseEmailDeep writes, so
    // they follow the constant. If the marker's value ever changes, this test
    // must move with it rather than red on a stale literal.
    expect(value).toEqual({
      subjectEmail: ERASED_MARKER,
      note: `released to Subject Person (${ERASED_MARKER}) on request`,
      nested: { list: [ERASED_MARKER, 'other@example.com'] },
    });
  });

  it('reports unchanged when the subject email is absent', () => {
    const input = { reference: 'case-8891', other: 'unrelated@example.com' };
    const { value, changed } = eraseEmailDeep(input, EMAIL);
    expect(changed).toBe(false);
    expect(value).toEqual(input);
  });

  it('no-ops without an email to match (unresolvable subject)', () => {
    const input = { subjectEmail: EMAIL };
    const { changed } = eraseEmailDeep(input, undefined);
    expect(changed).toBe(false);
  });

  it('leaves non-string leaves intact', () => {
    const input = { count: 3, flag: true, when: null };
    const { value, changed } = eraseEmailDeep(input, EMAIL);
    expect(changed).toBe(false);
    expect(value).toEqual(input);
  });
});
