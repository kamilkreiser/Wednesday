/**
 * =============================================================================
 * GDPR ERASURE — executeErasure UNIT TESTS (KS-293 / KS-292)
 * =============================================================================
 * Guards two erasure correctness fixes, with `prisma.$executeRaw` /
 * `$queryRaw` mocked at the unit boundary (SQL correctness against Postgres is
 * integration-test territory — see the end-to-end check on the ticket):
 *
 *   - KS-293: refresh_tokens MUST be hard-deleted on erasure. The FK to users
 *     is ON DELETE CASCADE, but erasure anonymises the user row (UPDATE) rather
 *     than deleting it, so the cascade never fires. An orphaned refresh token
 *     would otherwise still mint fresh access tokens for the anonymised account.
 *   - KS-292: erasure must NOT issue DELETEs against `encryption_keys` /
 *     `key_material` — neither table exists, so the old code was a swallowed
 *     no-op that presented as a "keys destroyed" step (false comfort).
 * =============================================================================
 */

// ---------------------------------------------------------------------------
// Mocks (must precede the import of the module under test)
// ---------------------------------------------------------------------------

const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();

jest.mock('../db', () => ({
  prisma: {
    $queryRaw: mockQueryRaw,
    $executeRaw: mockExecuteRaw,
  },
}));

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));

jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    publishEvent: jest.fn().mockResolvedValue(undefined),
    EventTypes: { USER_ERASED: 'user.erased' },
    encryptField: jest.fn((v: string) => v),
    decryptField: jest.fn((v: string) => v),
    // KS-291: subject-DEK surface used by gdprService's dual-format PII helpers
    encryptFieldWithDek: jest.fn((v: string) => v),
    decryptFieldWithDek: jest.fn((v: string) => v),
    isSubjectDekCiphertext: jest.fn(() => false),
    isEncryptedPii: jest.fn(() => false),
    // KS-458: gdprService's cross-tenant entry points run under the platform
    // scope; in the unit suite the scope is a pass-through (no DB, no RLS).
    runWithPlatformScope: jest.fn(<T,>(fn: () => T): T => fn()),
    SubjectDekProvider: class {
      getOrCreateDek = async () => Buffer.alloc(32);
      getDek = async () => null;
      destroyDek = async () => 'destroyed' as const;
      evict = () => undefined;
    },
  }),
);

// KS-291: the provider singleton is mocked directly so the crypto-shred step
// is observable without a DB.
const mockDestroyDek = jest.fn().mockResolvedValue('destroyed');
jest.mock('../services/subjectDeks', () => ({
  subjectDeks: {
    getOrCreateDek: jest.fn(async () => Buffer.alloc(32)),
    getDek: jest.fn(async () => null),
    destroyDek: mockDestroyDek,
    evict: jest.fn(),
  },
}));

// KS-291 regression guard: the USER_ERASED fan-out must go through
// originate's OWN initialised publisher (../events). The previous import
// from @secuura/shared silently no-op'd (that singleton is never
// initEventBus()'d in originate), so the auth/kyc/wallet cascades never
// fired despite the success log.
const mockLocalPublish = jest.fn().mockResolvedValue(undefined);
jest.mock('../events', () => ({
  publishEvent: mockLocalPublish,
  EventTypes: { USER_ERASED: 'user.erased' },
}));

import { executeErasure } from '../services/gdprService';
import { ERASED_MARKER } from '../utils/erasureMarker';

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/**
 * Reconstruct the SQL skeleton from a tagged-template `$executeRaw`/`$queryRaw`
 * mock invocation. Prisma passes the static string parts as the first argument
 * (a TemplateStringsArray) and the interpolated values as the rest.
 */
function sqlOf(call: unknown[]): string {
  const parts = call[0] as readonly string[];
  return parts.join(' ? ').replace(/\s+/g, ' ').trim();
}

/** Interpolated values of a tagged-template mock invocation (everything after the strings array). */
function valuesOf(call: unknown[]): unknown[] {
  return call.slice(1);
}

/**
 * The value BOUND immediately after a given SQL fragment.
 *
 * QA F-1: `sqlOf` renders every interpolated value as `?`, so an assertion
 * written against its output cannot tell `document_type = ${ERASED_MARKER}`
 * from `document_type = ${null}` — BOTH render `document_type = ?`. That makes
 * the control below vacuous on precisely the wrong fix it exists to reject: a
 * NULL-writing "fix" satisfies `toMatch(/document_type\s*=/)` and
 * `not.toMatch(/document_type\s*=\s*NULL/)` at the same time.
 *
 * A tagged template's Nth interpolation sits between `strings[N]` and
 * `strings[N+1]`, so the value bound after a fragment is `values[N]` where
 * `strings[N]` ENDS with that fragment. Reading the bound value instead of the
 * rendered text is the only way to assert WHAT is written.
 */
function boundValueAfter(call: unknown[], endsWith: RegExp): unknown {
  const parts = call[0] as readonly string[];
  const idx = parts.findIndex((p) => endsWith.test(p));
  return idx === -1 ? undefined : valuesOf(call)[idx];
}

const USER_ID = '11111111-1111-1111-1111-111111111111';
const DSR_ID = '22222222-2222-2222-2222-222222222222';
const ADMIN_ID = '33333333-3333-3333-3333-333333333333';

describe('executeErasure', () => {
  beforeEach(() => {
    jest.clearAllMocks();
    // Every DELETE/UPDATE reports one affected row so the `if (count > 0)`
    // logging branches (and thus logDeletion's $queryRaw) actually fire.
    mockExecuteRaw.mockResolvedValue(1);
    // $queryRaw backs both logDeletion (INSERT ... RETURNING *) and the
    // pre-anonymise wallet lookup; a single generic row satisfies both.
    mockQueryRaw.mockResolvedValue([{ id: 'log-row', records_affected: 1 }]);
  });

  it('hard-deletes refresh_tokens for the erased user (KS-293)', async () => {
    const result = await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    expect(result.success).toBe(true);

    // A DELETE against refresh_tokens, scoped to the user, must be issued.
    const refreshDelete = mockExecuteRaw.mock.calls.find(
      (call) => /DELETE\s+FROM\s+refresh_tokens/i.test(sqlOf(call)),
    );
    expect(refreshDelete).toBeDefined();
    expect(valuesOf(refreshDelete as unknown[])).toContain(USER_ID);
  });

  it('logs the refresh_tokens deletion in the data deletion log (KS-293)', async () => {
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);

    // logDeletion writes one data_deletion_log row per processed data type;
    // refresh_tokens must be among them.
    const loggedRefresh = mockQueryRaw.mock.calls.find(
      (call) =>
        /INSERT\s+INTO\s+data_deletion_log/i.test(sqlOf(call)) &&
        valuesOf(call).includes('refresh_tokens'),
    );
    expect(loggedRefresh).toBeDefined();
  });

  it('still deletes user_sessions (regression guard for the adjacent step)', async () => {
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    const sessionDelete = mockExecuteRaw.mock.calls.find(
      (call) => /DELETE\s+FROM\s+user_sessions/i.test(sqlOf(call)),
    );
    expect(sessionDelete).toBeDefined();
  });

  it('does NOT touch the non-existent encryption_keys / key_material tables (KS-292)', async () => {
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    const touchedDeadTables = mockExecuteRaw.mock.calls.some(
      (call) => /encryption_keys|key_material/i.test(sqlOf(call)),
    );
    expect(touchedDeadTables).toBe(false);
  });

  it('publishes user.erased via the LOCAL initialised publisher (KS-291)', async () => {
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    expect(mockLocalPublish).toHaveBeenCalledWith(
      'user.erased',
      expect.objectContaining({ userId: USER_ID, dsrId: DSR_ID }),
    );
  });

  it('crypto-shreds the subject DEK and logs it (KS-291)', async () => {
    const result = await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    expect(result.success).toBe(true);

    // The subject's key material must be destroyed via the provider...
    expect(mockDestroyDek).toHaveBeenCalledWith(USER_ID);

    // ...and recorded in the deletion log as a crypto-shred step.
    const loggedShred = mockQueryRaw.mock.calls.find(
      (call) =>
        /INSERT\s+INTO\s+data_deletion_log/i.test(sqlOf(call)) &&
        valuesOf(call).includes('pii_subject_keys') &&
        valuesOf(call).includes('crypto-shred'),
    );
    expect(loggedShred).toBeDefined();
  });

  it('KS-537: pseudonymises the subject email inside lifecycle payloads and re-stores them', async () => {
    mockQueryRaw.mockImplementation((...args: unknown[]) => {
      const sql = sqlOf(args);
      if (/SELECT\s+email\s+FROM\s+users/i.test(sql)) {
        return Promise.resolve([{ email: 'subject@example.com' }]);
      }
      if (/FROM\s+document_lifecycle_events/i.test(sql)) {
        return Promise.resolve([
          // Observed shapes: the address bare under a key, and embedded in a
          // larger display string.
          { id: 'ev-1', payload: { note: 'released to Subject Person (subject@example.com)' } },
          { id: 'ev-2', payload: { reference: 'case-8891' } },
        ]);
      }
      return Promise.resolve([{ id: 'log-row', records_affected: 1 }]);
    });

    const result = await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    expect(result.success).toBe(true);

    // Only the matching row is rewritten…
    const evUpdates = mockExecuteRaw.mock.calls.filter((call) =>
      /UPDATE\s+document_lifecycle_events\s+SET\s+payload/i.test(sqlOf(call)),
    );
    expect(evUpdates).toHaveLength(1);
    // …with the address gone and the erasure marker present.
    const bound = valuesOf(evUpdates[0] as unknown[]).map(String).join(' ');
    expect(bound).toContain(ERASED_MARKER);
    expect(bound).toContain('piiErased');
    expect(bound).not.toContain('subject@example.com');

    // And the step lands in the deletion log as an anonymize action.
    const logged = mockQueryRaw.mock.calls.find(
      (call) =>
        /INSERT\s+INTO\s+data_deletion_log/i.test(sqlOf(call)) &&
        valuesOf(call).includes('document_lifecycle_events'),
    );
    expect(logged).toBeDefined();
  });

  it('KS-537: shares — sharer rows hard-deleted, recipient email blanked (record retained)', async () => {
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);

    const del = mockExecuteRaw.mock.calls.find((call) =>
      /DELETE\s+FROM\s+shares\s+WHERE\s+shared_by_id/i.test(sqlOf(call)),
    );
    expect(del).toBeDefined();
    expect(valuesOf(del as unknown[])).toContain(USER_ID);

    const upd = mockExecuteRaw.mock.calls.find((call) =>
      /UPDATE\s+shares\s+SET\s+recipient_email\s*=\s*NULL/i.test(sqlOf(call)),
    );
    expect(upd).toBeDefined();
    expect(valuesOf(upd as unknown[])).toContain(USER_ID);
  });

  it('KS-537: the lifecycle payload scan is skipped when the subject email cannot be resolved', async () => {
    // Default $queryRaw mock returns no email column → subjectEmail stays
    // undefined → no lifecycle SELECT sweep and no payload rewrites; the
    // uuid-matched steps (incl. shares) still run — asserted above.
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    const evSelect = mockQueryRaw.mock.calls.find((call) =>
      /FROM\s+document_lifecycle_events/i.test(sqlOf(call)),
    );
    expect(evSelect).toBeUndefined();
  });

  it('erasure still succeeds and shreds when earlier counts are zero', async () => {
    // Zero affected rows on every step (idempotent re-run of an erasure):
    // the shred must still fire — it is not gated on prior deletions.
    mockExecuteRaw.mockResolvedValue(0);
    const result = await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    expect(result.success).toBe(true);
    expect(mockDestroyDek).toHaveBeenCalledWith(USER_ID);
  });

  // -------------------------------------------------------------------------
  // KS-543 — certification erasure must actually strip, not stamp
  // -------------------------------------------------------------------------

  it('KS-543: certification_events actor rows are rebuilt from the allow-list, not stamped', async () => {
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);

    const certUpdate = mockExecuteRaw.mock.calls.find(
      (call) =>
        /UPDATE\s+certification_events\s+SET/i.test(sqlOf(call)) &&
        /actor_user_id\s*=\s*NULL/i.test(sqlOf(call)),
    );
    expect(certUpdate).toBeDefined();
    const sql = sqlOf(certUpdate as unknown[]);
    // The details are REBUILT from the non-identifying allow-list…
    expect(sql).toMatch(/jsonb_object_agg/i);
    expect(sql).toContain("'status', 'blockchain', 'shareType'");
    // …not merely stamped anonymized:true over intact values (the old shape).
    expect(sql).not.toMatch(/jsonb_set/i);
    expect(valuesOf(certUpdate as unknown[])).toContain(USER_ID);
  });

  it('KS-543: SHARE events + legacy share_records where the subject was the RECIPIENT lose toEmail/toName', async () => {
    mockQueryRaw.mockImplementation((...args: unknown[]) => {
      const sql = sqlOf(args);
      if (/SELECT\s+email\s+FROM\s+users/i.test(sql)) {
        return Promise.resolve([{ email: 'subject@example.com' }]);
      }
      if (/FROM\s+document_lifecycle_events/i.test(sql) || /FROM\s+documents\s+WHERE\s+certification_metadata/i.test(sql)) {
        return Promise.resolve([]);
      }
      return Promise.resolve([{ id: 'log-row', records_affected: 1 }]);
    });

    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);

    const evRecipient = mockExecuteRaw.mock.calls.find((call) =>
      /UPDATE\s+certification_events\s+SET\s+details\s*=\s*\(details\s*-\s*'toEmail'\s*-\s*'toName'\)/i.test(sqlOf(call)),
    );
    expect(evRecipient).toBeDefined();
    expect(valuesOf(evRecipient as unknown[])).toContain('subject@example.com');

    // The marker is a bound value since QA F-13, so the statement reads
    // `to_email = ?` and the sentinel is asserted among the bound values.
    const legacyRecipient = mockExecuteRaw.mock.calls.find((call) =>
      /UPDATE\s+share_records\s+SET\s+to_email\s*=\s*\?\s*,\s*to_name\s*=\s*NULL/i.test(sqlOf(call)),
    );
    expect(legacyRecipient).toBeDefined();
    expect(valuesOf(legacyRecipient as unknown[])).toContain(ERASED_MARKER);
    expect(valuesOf(legacyRecipient as unknown[])).toContain('subject@example.com');
  });

  it('KS-543: recipient-matched steps are skipped when the subject email cannot be resolved', async () => {
    // Default mock resolves no email → nothing to match recipient rows by.
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    const touched = mockExecuteRaw.mock.calls.some(
      (call) => /toEmail|share_records\s+SET\s+to_email/i.test(sqlOf(call)),
    );
    expect(touched).toBe(false);
  });

  it('KS-543: non-owned certification_metadata is surgically scrubbed — issuer identity out, holder chain linkage kept', async () => {
    mockQueryRaw.mockImplementation((...args: unknown[]) => {
      const sql = sqlOf(args);
      if (/SELECT\s+email\s+FROM\s+users/i.test(sql)) {
        return Promise.resolve([{ email: 'subject@example.com' }]);
      }
      if (/FROM\s+documents\s+WHERE\s+certification_metadata/i.test(sql)) {
        return Promise.resolve([{
          id: '44444444-4444-4444-4444-444444444444',
          certification_metadata: {
            issuerId: USER_ID,
            issuerName: 'Subject Person',
            certificationType: 'certificate',
            certificationData: { grade: 'A', actorName: 'Subject Person (subject@example.com)' },
            blockchain: { txHash: 'abc123', anchorId: 'anchor_9' },
          },
        }]);
      }
      if (/FROM\s+document_lifecycle_events/i.test(sql)) return Promise.resolve([]);
      return Promise.resolve([{ id: 'log-row', records_affected: 1 }]);
    });

    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);

    const metaUpdate = mockExecuteRaw.mock.calls.find((call) =>
      /UPDATE\s+documents\s+SET\s+certification_metadata\s*=/i.test(sqlOf(call)) &&
      valuesOf(call).some((v) => typeof v === 'string' && v.includes('piiErased')),
    );
    expect(metaUpdate).toBeDefined();
    const stored = valuesOf(metaUpdate as unknown[]).find(
      (v): v is string => typeof v === 'string' && v.includes('piiErased'),
    )!;
    const parsed = JSON.parse(stored);
    // Issuer identity blanked (issuerId uuid survives as attribution)…
    expect(parsed.issuerName).toBe(ERASED_MARKER);
    expect(parsed.issuerId).toBe(USER_ID);
    // …subject email deep-erased wherever it sat…
    expect(stored).not.toContain('subject@example.com');
    expect(parsed.certificationData.actorName).toContain(ERASED_MARKER);
    // …and the holder's chain linkage untouched.
    expect(parsed.blockchain).toEqual({ txHash: 'abc123', anchorId: 'anchor_9' });
    expect(parsed.certificationData.grade).toBe('A');
  });

  // -------------------------------------------------------------------------
  // KS-695 ask 2 — documents.title in erasure coverage
  //
  // S sends the real filename as `Title` on originate
  // (platform-s `CardanoAnchorService.cs:407`), so before this change a real
  // filename survived erasure on the subject's own documents: step 6 blanked
  // metadata, certification_metadata and owner_did, and left `title` alone.
  // '[erased]' rather than NULL to match the existing convention on
  // share_records.to_email, and because title renders in list views.
  // -------------------------------------------------------------------------

  it('KS-695: step 6 blanks documents.title for the subject\'s own documents', async () => {
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    const step6 = mockExecuteRaw.mock.calls.find((call) =>
      /UPDATE\s+documents\s+SET/i.test(sqlOf(call)) && /owner_did\s*=\s*NULL/i.test(sqlOf(call)),
    );
    expect(step6).toBeDefined();
    // The marker is a BOUND value now, not an inlined literal (QA F-13), so the
    // assertion pins the bound value rather than the SQL text.
    expect(sqlOf(step6 as unknown[])).toMatch(/title\s*=\s*\?/i);
    expect(valuesOf(step6 as unknown[])).toContain(ERASED_MARKER);
    // Scope unchanged — still the subject's OWN documents, by owner_user_id.
    expect(sqlOf(step6 as unknown[])).toMatch(/WHERE\s+owner_user_id\s*=\s*\?/i);
    expect(valuesOf(step6 as unknown[])).toContain(USER_ID);
  });

  // QA F-2 (Major) — `description` is the same class as `title`: caller-supplied
  // free text on create (`routes/documents.ts:471`), touched by no erasure step.
  // It is nulled rather than marked, because unlike `title` the column IS
  // nullable and storing nothing erases more than storing a marker.
  it('KS-695/F-2: step 6 also nulls documents.description', async () => {
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    const step6 = mockExecuteRaw.mock.calls.find((call) =>
      /UPDATE\s+documents\s+SET/i.test(sqlOf(call)) && /owner_did\s*=\s*NULL/i.test(sqlOf(call)),
    );
    expect(sqlOf(step6 as unknown[])).toMatch(/description\s*=\s*NULL/i);
  });

  // QA F-2 (Major) — `document_type` is the THIRD column of this class on this
  // one table, which is why the PR now enumerates all 24 columns rather than
  // arguing them one at a time.
  //
  // It is caller-supplied free text: `routes/documents.ts:412-413` checks only
  // that it is a *string*, and unlike `title`/`description` it never passes
  // through `sanitizeString` (`:485`). Measured on the live table — no CHECK
  // constraint, 33 distinct values, fuzzer bytes among them — so it accepts
  // arbitrary caller input and can carry a subject's identity.
  //
  // It takes the MARKER rather than NULL because the column is NOT NULL
  // (`character varying(100)`), the same asymmetry as title-vs-description.
  it('KS-695/F-2: step 6 marks documents.document_type — it is caller-supplied free text', async () => {
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    const step6 = mockExecuteRaw.mock.calls.find((call) =>
      /UPDATE\s+documents\s+SET/i.test(sqlOf(call)) && /owner_did\s*=\s*NULL/i.test(sqlOf(call)),
    );
    expect(step6).toBeDefined();
    expect(sqlOf(step6 as unknown[])).toMatch(/document_type\s*=\s*\?/i);
    // The marker is BOUND, not inlined (QA F-13's convention).
    expect(valuesOf(step6 as unknown[])).toContain(ERASED_MARKER);
  });

  it('CONTROL/F-2: document_type is marked, NOT nulled — the column is NOT NULL', async () => {
    // Without this, a "fix" that wrote `document_type = NULL` would satisfy the
    // test above's intent and then fail at runtime against the live schema. The
    // distinction between the marker and NULL is the whole per-column judgement
    // this PR is being asked to enumerate, so it gets its own assertion.
    //
    // The presence assertion is load-bearing and is NOT redundant with the test
    // above. `not.toMatch(/document_type = NULL/)` is satisfied VACUOUSLY by a
    // statement that never mentions the column at all — which is precisely the
    // state this PR shipped in at 292634718, where this control passed while
    // the fix was absent. A control that cannot fail on the absent-fix case is
    // not a control, so it asserts the column is SET first, then that what it
    // is set to is not NULL.
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    const step6 = mockExecuteRaw.mock.calls.find((call) =>
      /UPDATE\s+documents\s+SET/i.test(sqlOf(call)) && /owner_did\s*=\s*NULL/i.test(sqlOf(call)),
    );
    expect(sqlOf(step6 as unknown[])).toMatch(/document_type\s*=/i);
    expect(sqlOf(step6 as unknown[])).not.toMatch(/document_type\s*=\s*NULL/i);

    // QA F-1: the two assertions above are STILL vacuous for the wrong-fix case.
    // `sqlOf` renders every bound value as `?`, so `document_type = ${null}`
    // renders `document_type = ?` — which matches the first and does not match
    // the second. Both pass on exactly the fix this control exists to reject.
    // Reading the BOUND VALUE is the only assertion that discriminates.
    const bound = boundValueAfter(step6 as unknown[], /document_type\s*=\s*$/i);
    expect(bound).toBe(ERASED_MARKER);
    expect(bound).not.toBeNull();
  });

  /**
   * CONTROL for the control. Proves `boundValueAfter` can actually FAIL — a
   * helper that returned the marker regardless, or that never located the
   * fragment and returned `undefined` compared loosely, would look identical to
   * a real pass. Both arms are asserted on a synthetic call whose shape matches
   * the real one.
   */
  it('CONTROL/F-1: boundValueAfter discriminates the marker from a NULL write', () => {
    const marked = [['UPDATE documents SET owner_did = NULL, document_type = ', ' WHERE id = ', ''], ERASED_MARKER, 'doc-1'];
    const nulled = [['UPDATE documents SET owner_did = NULL, document_type = ', ' WHERE id = ', ''], null, 'doc-1'];

    // The rendered text is IDENTICAL for both — this is the vacuity itself.
    expect(sqlOf(marked)).toEqual(sqlOf(nulled));
    expect(sqlOf(nulled)).toMatch(/document_type\s*=/i);
    expect(sqlOf(nulled)).not.toMatch(/document_type\s*=\s*NULL/i);

    // The bound value is not.
    expect(boundValueAfter(marked, /document_type\s*=\s*$/i)).toBe(ERASED_MARKER);
    expect(boundValueAfter(nulled, /document_type\s*=\s*$/i)).toBeNull();
  });

  it('KS-695: the 6b surgical pass does NOT blank title — a non-subject\'s filename survives', async () => {
    // 6b reaches documents the subject does NOT own (it excludes owner-scoped
    // rows). Those titles belong to someone else, so widening the title blank
    // into 6b would erase a third party's data.
    //
    // QA F-12 corrected what this control actually catches. A fix applied to the
    // WRONG update fails the test above on its own, because that test pins the
    // statement carrying `owner_did = NULL` and `WHERE owner_user_id = ?`. What
    // this control catches is a fix applied to BOTH updates — a blank widened
    // past the subject's own rows.
    mockQueryRaw.mockImplementation((...call: unknown[]) => {
      if (/FROM\s+documents\s+WHERE\s+certification_metadata/i.test(sqlOf(call))) {
        return Promise.resolve([
          { id: 'doc-not-owned', certification_metadata: { issuerId: USER_ID, issuerName: 'Subject Name' } },
        ]);
      }
      return Promise.resolve([{ id: 'log-row', records_affected: 1 }]);
    });

    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);

    const sixB = mockExecuteRaw.mock.calls.filter((call) =>
      /UPDATE\s+documents\s+SET\s+certification_metadata\s*=/i.test(sqlOf(call)),
    );
    expect(sixB.length).toBeGreaterThan(0);
    for (const call of sixB) {
      expect(sqlOf(call)).not.toMatch(/title\s*=/i);
      // Same containment for F-2's column.
      expect(sqlOf(call)).not.toMatch(/description\s*=/i);
    }
  });

  it('KS-543: owner-scoped docs stay on the wholesale step-6 blank (6b excludes them)', async () => {
    await executeErasure(USER_ID, DSR_ID, ADMIN_ID);
    const selectLinked = mockQueryRaw.mock.calls.find((call) =>
      /FROM\s+documents\s+WHERE\s+certification_metadata/i.test(sqlOf(call)),
    );
    expect(selectLinked).toBeDefined();
    expect(sqlOf(selectLinked as unknown[])).toMatch(/owner_user_id\s*<>\s*\?/i);
  });
});
