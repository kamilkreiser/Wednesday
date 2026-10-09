/**
 * =============================================================================
 * KS-695 ask 1 — ERASURE ADDRESSED BY external_ref (connector-driven)
 * =============================================================================
 * Platform S holds no K `users.id`, so it addresses erasure by
 * `Person.PersonGuid` (K's `action_provenance.external_ref`). S retries
 * WITHOUT BOUND, so the two properties that matter are:
 *
 *   1. TENANCY — resolution is scoped to the caller's own tenant. This is the
 *      only gate: `executeErasure` itself runs platform-scoped (cross-tenant by
 *      design, KS-458), so if resolution were unscoped a connector could name a
 *      subject in someone else's tenant.
 *   2. TERMINATION — every path answers `completed`. There is deliberately no
 *      404: an unresolvable ref is not a not-found, and anything non-terminal
 *      strands a legal obligation against an unbounded retry.
 * =============================================================================
 */

const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();

jest.mock('../db', () => ({ prisma: { $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw } }));
jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: jest.fn(), debug: jest.fn() },
}));
jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    publishEvent: jest.fn().mockResolvedValue(undefined),
    EventTypes: { USER_ERASED: 'user.erased' },
    encryptField: jest.fn((v: string) => v),
    decryptField: jest.fn((v: string) => v),
    encryptFieldWithDek: jest.fn((v: string) => v),
    decryptFieldWithDek: jest.fn((v: string) => v),
    isSubjectDekCiphertext: jest.fn(() => false),
    isEncryptedPii: jest.fn(() => false),
    runWithPlatformScope: jest.fn(<T,>(fn: () => T): T => fn()),
    // KS-780: the org-id normaliser now lives in @secuura/shared and originate's
    // orgId.ts re-exports it, so this hand-listed mock must pass the REAL one
    // through — a stub here would be a second implementation, the thing removed.
    normaliseOrgId: jest.requireActual('@secuura/shared').normaliseOrgId,
    SubjectDekProvider: class {
      getOrCreateDek = async () => Buffer.alloc(32);
      getDek = async () => null;
      destroyDek = async () => 'destroyed' as const;
      evict = () => undefined;
    },
  }),
);
jest.mock('../services/subjectDeks', () => ({
  subjectDeks: {
    getOrCreateDek: jest.fn(async () => Buffer.alloc(32)),
    getDek: jest.fn(async () => null),
    destroyDek: jest.fn().mockResolvedValue('destroyed'),
    evict: jest.fn(),
  },
}));
jest.mock('../events', () => ({
  publishEvent: jest.fn().mockResolvedValue(undefined),
  EventTypes: { USER_ERASED: 'user.erased' },
}));

import { executeErasureByExternalRef, getErasureStatusByExternalRef } from '../services/gdprService';

function sqlOf(call: unknown[]): string {
  return (call[0] as readonly string[]).join(' ? ').replace(/\s+/g, ' ').trim();
}
function valuesOf(call: unknown[]): unknown[] {
  return call.slice(1);
}

const EXTERNAL_REF = 'person-guid-from-platform-s';
const TENANT = 'aaaaaaaa-aaaa-aaaa-aaaa-aaaaaaaaaaaa';
const OTHER_TENANT = 'bbbbbbbb-bbbb-bbbb-bbbb-bbbbbbbbbbbb';
/** The caller key's Organisation, and a different one inside the SAME tenant. */
const ORG = 'cccccccc-cccc-cccc-cccc-cccccccccccc';
const OTHER_ORG = 'dddddddd-dddd-dddd-dddd-dddddddddddd';
const SECOND_USER = '22222222-2222-2222-2222-222222222222';
const USER = '11111111-1111-1111-1111-111111111111';
const CONNECTOR = 'platform-s:org-guid';
/** What `performedBy` becomes inside the service — the actor the DSR must name. */
const CONNECTOR_PRINCIPAL = `connector:${CONNECTOR}`;

/** Route each mocked read by the SQL it carries. */
function wireReads(opts: {
  resolved?: string | null;
  provenanceRows?: number;
  priorDsr?: boolean;
  deniedDsr?: boolean;
  openDsr?: string | null;
  uneased?: number;
  /** provenance rows carry an email_hash (Peter F1's fallback input) */
  hashRows?: boolean;
  /** the user that hash resolves to, and its tenant (F1's assertion) */
  hashUser?: { id: string; tenantId?: string | null; orgId?: string | null } | null;
  /** what `SELECT email FROM users` returns — ciphertext by default in F3's cases */
  subjectEmailStored?: string;
  /** the SET-valued hash match; overrides `hashUser` when present */
  hashUsers?: Array<{ id: string; tenantId?: string | null; orgId?: string | null }> | null;
}) {
  const {
    resolved = null, provenanceRows = 0, priorDsr = false, deniedDsr = false,
    openDsr = null, uneased = 0, hashRows = false, hashUser = null,
    hashUsers = null,
    subjectEmailStored = 'subject@example.com',
  } = opts;
  mockQueryRaw.mockImplementation((...call: unknown[]) => {
    const sql = sqlOf(call);
    if (/SELECT resolved_user_id, email_hash FROM action_provenance/i.test(sql)) {
      return Promise.resolve(Array.from({ length: provenanceRows }, (_, i) => ({
        resolved_user_id: i === 0 ? resolved : null,
        email_hash: hashRows ? `hash-${i}` : null,
      })));
    }
    // Peter F1's fallback: hash -> users, then the ORGANISATION is ASSERTED,
    // not filtered (QA Blocker 2 moved this from the tenant to the org).
    // `hashUsers` models the SET-valued match: LIMIT 2 makes "more than one"
    // observable, so the fixture must be able to return two rows.
    if (/SELECT id, tenant_id, organization_id FROM users/i.test(sql)) {
      const list = hashUsers ?? (hashUser ? [hashUser] : []);
      return Promise.resolve(list.map((u) => ({
        id: u.id,
        tenant_id: u.tenantId === undefined ? TENANT : u.tenantId,
        organization_id: u.orgId === undefined ? ORG : u.orgId,
      })));
    }
    if (/COUNT\(\*\)::bigint AS n FROM action_provenance/i.test(sql)) {
      return Promise.resolve([{ n: BigInt(uneased) }]);
    }
    // Two DIFFERENT reads hit data_subject_requests on this path and they must
    // not be conflated: the terminal read looks for a CONCLUDED erasure
    // (completed OR denied — QA F-1), the re-drive read looks for a
    // NON-TERMINAL one. Discriminate on the status clause, not on the table.
    if (/FROM data_subject_requests .*status NOT IN \('completed', 'denied'\)/i.test(sql)) {
      return Promise.resolve(openDsr ? [{ id: openDsr }] : []);
    }
    if (/FROM data_subject_requests .*status IN \('completed', 'denied'\)/i.test(sql)) {
      if (deniedDsr) return Promise.resolve([{ id: 'dsr-denied', status: 'denied' }]);
      return Promise.resolve(priorDsr ? [{ id: 'dsr-existing', status: 'completed' }] : []);
    }
    if (/SELECT email FROM users/i.test(sql)) return Promise.resolve([{ email: subjectEmailStored }]);
    // createDSR's INSERT ... RETURNING *, and logDeletion's INSERT
    return Promise.resolve([{ id: 'dsr-new', type: 'erasure', user_id: USER, records_affected: 1 }]);
  });
  mockExecuteRaw.mockResolvedValue(1);
}

/** The write that marks the DSR done — the one F-1 was issuing unconditionally. */
function completionWrites() {
  return mockExecuteRaw.mock.calls.filter((c) =>
    /UPDATE data_subject_requests SET status = 'completed'/i.test(sqlOf(c)),
  );
}

/**
 * A fixture that MODELS the DSR row instead of answering every read from a
 * fixed literal.
 *
 * QA F-5 (Major, test integrity): the previous 'leaves the subject re-drivable'
 * test wired `priorDsr: false` and then asserted that the status read returned
 * `alreadyErased: false`. That wiring makes the read return `[]` unconditionally,
 * so the assertion held for ANY implementation — including one that completes a
 * failed erasure, and including one that does nothing at all. It asserted its
 * own fixture.
 *
 * Here the erasure path's completion WRITE mutates `state.status`, and the
 * status READ is answered from that same state. The two halves are connected,
 * so the assertion can actually fail: an implementation that marks a failed
 * erasure 'completed' flips the state and the read-back reds.
 */
function wireStatefulDsr(opts: { initialStatus?: string; failErasureStep?: boolean } = {}) {
  const TERMINAL = ['completed', 'denied'];
  const state = { status: opts.initialStatus ?? 'pending', erasureStepsRun: 0 };

  mockQueryRaw.mockImplementation((...call: unknown[]) => {
    const sql = sqlOf(call);
    if (/SELECT resolved_user_id, email_hash FROM action_provenance/i.test(sql)) {
      return Promise.resolve([{ resolved_user_id: USER, email_hash: null }]);
    }
    if (/SELECT id, tenant_id FROM users/i.test(sql)) return Promise.resolve([]);
    if (/COUNT\(\*\)::bigint AS n FROM action_provenance/i.test(sql)) {
      return Promise.resolve([{ n: BigInt(0) }]);
    }
    if (/FROM data_subject_requests .*status NOT IN \('completed', 'denied'\)/i.test(sql)) {
      return Promise.resolve(TERMINAL.includes(state.status) ? [] : [{ id: 'dsr-stateful' }]);
    }
    if (/FROM data_subject_requests .*status IN \('completed', 'denied'\)/i.test(sql)) {
      return Promise.resolve(
        TERMINAL.includes(state.status) ? [{ id: 'dsr-stateful', status: state.status }] : [],
      );
    }
    if (/SELECT email FROM users/i.test(sql)) return Promise.resolve([{ email: 'subject@example.com' }]);
    return Promise.resolve([{ id: 'dsr-stateful', type: 'erasure', user_id: USER, records_affected: 1 }]);
  });

  mockExecuteRaw.mockImplementation((...call: unknown[]) => {
    const sql = sqlOf(call);
    if (/UPDATE data_subject_requests SET status = 'completed'/i.test(sql)) {
      state.status = 'completed';
      return Promise.resolve(1);
    }
    if (/UPDATE users SET/i.test(sql)) {
      if (opts.failErasureStep) return Promise.reject(new Error('simulated erasure step failure'));
      state.erasureStepsRun += 1;
    }
    return Promise.resolve(1);
  });

  return state;
}

describe('KS-695 ask 1 — executeErasureByExternalRef', () => {
  beforeEach(() => jest.clearAllMocks());

  it('resolves external_ref SCOPED TO THE CALLER TENANT — the only tenancy gate on this path', async () => {
    wireReads({ resolved: USER, provenanceRows: 1 });
    await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
    const lookup = mockQueryRaw.mock.calls.find((c) =>
      /SELECT resolved_user_id, email_hash FROM action_provenance/i.test(sqlOf(c)),
    );
    expect(lookup).toBeDefined();
    expect(sqlOf(lookup as unknown[])).toMatch(/WHERE external_ref = \? AND tenant_id = \? ::uuid/i);
    // The caller's OWN tenant is interpolated — not a header, not a wildcard.
    expect(valuesOf(lookup as unknown[])).toEqual([EXTERNAL_REF, TENANT]);
    expect(valuesOf(lookup as unknown[])).not.toContain(OTHER_TENANT);
  });

  it('a repeat does NOT re-execute the erasure — it returns alreadyErased', async () => {
    wireReads({ resolved: USER, provenanceRows: 1, priorDsr: true });
    const r = await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
    expect(r).toEqual({ status: 'completed', alreadyErased: true });
    // The control that makes this meaningful: nothing was written at all.
    // S retries unbounded, so a second execution is the real hazard.
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });

  it('a first call for a resolvable subject DOES execute the erasure', async () => {
    wireReads({ resolved: USER, provenanceRows: 1, priorDsr: false });
    const r = await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
    expect(r).toEqual({ status: 'completed', alreadyErased: false });
    const anonymisedUser = mockExecuteRaw.mock.calls.find((c) => /UPDATE users SET/i.test(sqlOf(c)));
    expect(anonymisedUser).toBeDefined();
  });

  it('an UNRESOLVABLE ref still erases what IS addressable — the provenance identity columns', async () => {
    wireReads({ resolved: null, provenanceRows: 3, uneased: 3 });
    const r = await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
    expect(r).toEqual({ status: 'completed', alreadyErased: false });
    const blank = mockExecuteRaw.mock.calls.find((c) => /UPDATE action_provenance SET/i.test(sqlOf(c)));
    expect(blank).toBeDefined();
    expect(sqlOf(blank as unknown[])).toMatch(/email_enc = NULL, display_name_enc = NULL, email_hash = NULL/i);
    // Tenant-scoped here too — this write is reached without any users row.
    expect(sqlOf(blank as unknown[])).toMatch(/tenant_id = \? ::uuid/i);
    expect(valuesOf(blank as unknown[])).toEqual([EXTERNAL_REF, TENANT]);
  });

  it('an unresolvable ref already blanked writes NOTHING and reports alreadyErased', async () => {
    wireReads({ resolved: null, provenanceRows: 3, uneased: 0 });
    const r = await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
    expect(r).toEqual({ status: 'completed', alreadyErased: true });
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });

  // ── QA F-1 (Major) ────────────────────────────────────────────────────────
  // `executeErasureImpl` never throws: its catch returns `{ success: false }`.
  // The original caller discarded that and marked the DSR 'completed' anyway,
  // so a FAILED Art. 17 erasure answered `alreadyErased: true` forever — S
  // stopped retrying and the stranded obligation had no trace on the wire.
  describe('a FAILED erasure is never reported completed (QA F-1)', () => {
    /** Fail one step inside executeErasureImpl, exactly as a real fault would. */
    function failOneErasureStep() {
      mockExecuteRaw.mockImplementation((...call: unknown[]) =>
        /UPDATE users SET/i.test(sqlOf(call))
          ? Promise.reject(new Error('simulated erasure step failure'))
          : Promise.resolve(1),
      );
    }

    it('does NOT mark the DSR completed, and does not resolve as completed', async () => {
      wireReads({ resolved: USER, provenanceRows: 1, priorDsr: false });
      failOneErasureStep();
      await expect(executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT)).rejects.toThrow(
        /did not complete/i,
      );
      // The heart of F-1: the completion write must not be issued at all.
      expect(completionWrites()).toHaveLength(0);
    });

    it('leaves the subject re-drivable — the status read reflects the FAILED run, not a fixture', async () => {
      // QA F-5. This used to wire `priorDsr: false` and assert the read said
      // `alreadyErased: false` — which that wiring guarantees for every possible
      // implementation. Now the fixture is stateful: the erasure runs, FAILS,
      // and the status read is answered from the state the run actually left.
      const state = wireStatefulDsr({ failErasureStep: true });

      await expect(executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT))
        .rejects.toThrow(/did not complete/i);

      // The DSR was never concluded, so the read-back reports outstanding work.
      expect(state.status).toBe('pending');
      await expect(getErasureStatusByExternalRef(EXTERNAL_REF, TENANT))
        .resolves.toEqual({ status: 'completed', alreadyErased: false });
    });

    it('POSITIVE CONTROL for the stateful fixture — a SUCCESSFUL run flips the read-back', async () => {
      // Without this the test above passes on a fixture that can never report
      // `alreadyErased: true`, which is precisely the F-5 defect it replaces.
      // Same fixture, same reads, only the outcome differs.
      const state = wireStatefulDsr({ failErasureStep: false });

      await expect(executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT))
        .resolves.toEqual({ status: 'completed', alreadyErased: false });

      expect(state.status).toBe('completed');
      await expect(getErasureStatusByExternalRef(EXTERNAL_REF, TENANT))
        .resolves.toEqual({ status: 'completed', alreadyErased: true });
    });

    it('POSITIVE CONTROL — a successful erasure still issues the completion write', async () => {
      // Without this, the two assertions above are satisfied by any change that
      // simply never completes anything.
      wireReads({ resolved: USER, provenanceRows: 1, priorDsr: false });
      const r = await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
      expect(r).toEqual({ status: 'completed', alreadyErased: false });
      expect(completionWrites()).toHaveLength(1);
    });
  });

  // ── Peter F3 (Major) — the DSR recorded ciphertext-of-ciphertext ───────────
  // `users.email` is encrypted at rest, and `createDSR` runs `writePii` over
  // whatever it is handed. Passing the STORED value straight through stored
  // ciphertext-of-ciphertext, and `mapDsrRow` then decrypted once to an
  // unusable blob. Step 5c forty lines above already wraps the identical query
  // in `readPii`.
  //
  // This test exists because the suite stubs PII crypto to the IDENTITY
  // function — which is exactly why nothing caught it. Here the stubs are
  // re-armed for one test so ciphertext and plaintext are distinguishable.
  describe('Peter F3 — the subject email is decrypted before the DSR records it', () => {
    const CIPHERTEXT = 'enc:v1:Zm9vYmFy';
    const PLAINTEXT = 'subject@example.com';

    function armRealisticPiiCrypto() {
      const shared = jest.requireMock('@secuura/shared') as Record<string, jest.Mock>;
      shared.isEncryptedPii.mockImplementation((v: unknown) => typeof v === 'string' && v.startsWith('enc:'));
      shared.isSubjectDekCiphertext.mockImplementation(() => false);
      shared.decryptField.mockImplementation((v: unknown) =>
        typeof v === 'string' && v.startsWith('enc:') ? PLAINTEXT : v);
    }

    function dsrInsertValues(): unknown[] {
      const insert = mockQueryRaw.mock.calls.find((c) => /INSERT INTO data_subject_requests/i.test(sqlOf(c)));
      return insert ? valuesOf(insert) : [];
    }

    it('the DSR insert carries the DECRYPTED address, never the stored ciphertext', async () => {
      armRealisticPiiCrypto();
      wireReads({ resolved: USER, provenanceRows: 1, subjectEmailStored: CIPHERTEXT });
      await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
      const values = dsrInsertValues();
      expect(values).toContain(PLAINTEXT);
      expect(values).not.toContain(CIPHERTEXT);
    });

    it('CONTROL — a PLAINTEXT stored email passes through untouched', async () => {
      // readPii returns non-encrypted input as-is, so the fix must not mangle
      // legacy rows. Without this, "always decrypt" would pass the test above.
      armRealisticPiiCrypto();
      wireReads({ resolved: USER, provenanceRows: 1, subjectEmailStored: 'legacy@example.com' });
      await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
      expect(dsrInsertValues()).toContain('legacy@example.com');
    });
  });

  // ── Peter F1 (Major) — the resolver was weaker than the two already in tree ─
  // `resolveOnBehalfOf` opens with `if (!connectorOrgId) return null`
  // (provenance.ts:108), so a key minted WITHOUT an organizationId never sets
  // `resolved_user_id` on any row — whether or not a matching K user exists.
  // Resolving on that column alone sent a real user's erasure down the
  // unresolvable branch: three provenance columns blanked, no users row, no
  // documents, no crypto-shred, and `completed` on the wire.
  describe('Peter F1 / QA Blocker 2 — the hash fallback is ORGANISATION-scoped', () => {
    it('resolves through email_hash when NO row carries resolved_user_id, and runs the FULL erasure', async () => {
      wireReads({ resolved: null, provenanceRows: 3, hashRows: true, hashUser: { id: USER, tenantId: TENANT, orgId: ORG } });
      const r = await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT, ORG);
      expect(r).toEqual({ status: 'completed', alreadyErased: false });
      // The discriminator between the branches: only the full erasure touches users.
      expect(mockExecuteRaw.mock.calls.find((c) => /UPDATE users SET/i.test(sqlOf(c)))).toBeDefined();
    });

    it('CONTROL — with NO hash on any row it is still genuinely unresolvable', async () => {
      // Without this, the fix could be "always resolve to something", which
      // would erase the wrong subject.
      wireReads({ resolved: null, provenanceRows: 3, hashRows: false, uneased: 3 });
      await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT, ORG);
      expect(mockExecuteRaw.mock.calls.find((c) => /UPDATE users SET/i.test(sqlOf(c)))).toBeUndefined();
      expect(mockExecuteRaw.mock.calls.find((c) => /UPDATE action_provenance SET/i.test(sqlOf(c)))).toBeDefined();
    });

    // ── QA Blocker 2 (a): the crossing that used to be allowed ───────────────
    it('REFUSES when the hash resolves to another ORGANISATION in the SAME tenant', async () => {
      // THE BLOCKER. The assertion was `candidate.tenant_id !== tenantId`, and a
      // tenant contains many organisations — so this exact fixture (same tenant,
      // different org) RESOLVED and crypto-shredded another org's subject. The
      // write-side sibling `resolveOnBehalfOf` 403s this crossing by design.
      wireReads({ resolved: null, provenanceRows: 2, hashRows: true, hashUser: { id: USER, tenantId: TENANT, orgId: OTHER_ORG } });
      await expect(executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT, ORG))
        .rejects.toThrow(/outside this connector's Organisation/i);
      expect(mockExecuteRaw).not.toHaveBeenCalled();
    });

    it('CONTROL — the same hash INSIDE the caller Organisation resolves rather than refusing', async () => {
      // Proves the refusal keys on the ORGANISATION, not merely on taking the
      // hash path. This pair is the whole finding: same tenant in BOTH cases,
      // opposite outcomes, and the only thing that differs is the org.
      wireReads({ resolved: null, provenanceRows: 2, hashRows: true, hashUser: { id: USER, tenantId: TENANT, orgId: ORG } });
      await expect(executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT, ORG))
        .resolves.toEqual({ status: 'completed', alreadyErased: false });
    });

    // ── QA Blocker 2 (b): the org-less key ───────────────────────────────────
    it('an ORG-LESS KEY refuses terminally and erases NOTHING — never `completed`', async () => {
      // The sibling returns null for an org-less key, which is harmless on a
      // write (verbatim provenance). On an erasure, null means the branch that
      // blanks provenance and answers `completed` — a partial erasure reported
      // as a discharged Art. 17 obligation.
      wireReads({ resolved: null, provenanceRows: 2, hashRows: true, hashUser: { id: USER, tenantId: TENANT, orgId: ORG } });
      await expect(executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT, undefined))
        .rejects.toThrow(/org_less_key/i);
      expect(mockExecuteRaw).not.toHaveBeenCalled();
    });

    // ── QA finding 4: the set-valued match ───────────────────────────────────
    it('REFUSES as ambiguous when the ref hash-matches MORE THAN ONE user', async () => {
      // `= ANY(hashes) … LIMIT 1` has no ORDER BY, and the single-row uniqueness
      // argument does not hold for a SET of hashes (the address-change
      // population). Picking one arbitrarily is a guess with an irreversible
      // consequence.
      wireReads({
        resolved: null, provenanceRows: 2, hashRows: true,
        hashUsers: [{ id: USER, tenantId: TENANT, orgId: ORG }, { id: SECOND_USER, tenantId: TENANT, orgId: ORG }],
      });
      await expect(executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT, ORG))
        .rejects.toThrow(/ambiguous_subject/i);
      expect(mockExecuteRaw).not.toHaveBeenCalled();
    });

    it('CONTROL — exactly ONE match on the same fixture shape proceeds', async () => {
      // Without this the "ambiguous" guard could be a blanket refusal of the
      // hash path, which would re-create the under-erasure it is meant to stop.
      wireReads({
        resolved: null, provenanceRows: 2, hashRows: true,
        hashUsers: [{ id: USER, tenantId: TENANT, orgId: ORG }],
      });
      await expect(executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT, ORG))
        .resolves.toEqual({ status: 'completed', alreadyErased: false });
    });

    // ── QA finding 5: the NULL-tenant user, decided rather than implied ──────
    it('a NULL-TENANT user whose ORGANISATION matches RESOLVES — the org is the gate', async () => {
      // `users.tenant_id` is NULLABLE (01-schema.sql:42). The old assertion
      // `null !== tenantId` refused such a user terminally, with no branch and
      // no case covering it. The rule is now stated and exercised.
      wireReads({ resolved: null, provenanceRows: 2, hashRows: true, hashUser: { id: USER, tenantId: null, orgId: ORG } });
      await expect(executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT, ORG))
        .resolves.toEqual({ status: 'completed', alreadyErased: false });
    });

    it('a user with NO organisation is refused — membership cannot be shown', async () => {
      wireReads({ resolved: null, provenanceRows: 2, hashRows: true, hashUser: { id: USER, tenantId: TENANT, orgId: null } });
      await expect(executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT, ORG))
        .rejects.toThrow(/subject_outside_connector_organisation/i);
      expect(mockExecuteRaw).not.toHaveBeenCalled();
    });

    // ── QA finding 11: the uuid compare ──────────────────────────────────────
    it('an UPPERCASE organizationId claim is the SAME Organisation, not a different one', async () => {
      // The SQL one statement earlier casts to ::uuid and compares canonically;
      // this comparison was a raw JS string compare against an un-normalised JWT
      // claim, so a differently-cased claim read as a different org and 403'd a
      // legitimate erasure.
      wireReads({ resolved: null, provenanceRows: 2, hashRows: true, hashUser: { id: USER, tenantId: TENANT, orgId: ORG } });
      await expect(executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT, ORG.toUpperCase()))
        .resolves.toEqual({ status: 'completed', alreadyErased: false });
    });
  });

  // ── Peter F2 (Major) — sibling rows under one ref ──────────────────────────
  describe('Peter F2 — sibling provenance rows under the same ref are blanked', () => {
    it('the RESOLVABLE path also runs the ref-scoped blank', async () => {
      // The mock generates this shape whenever provenanceRows > 1: row 0 carries
      // resolved_user_id, the rest null — a PersonGuid whose address changed on
      // S. Step 5b matches neither those rows' user id nor the subject's hash,
      // and the ref-scoped blank previously ran ONLY on the unresolvable branch.
      wireReads({ resolved: USER, provenanceRows: 3 });
      await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
      const refBlank = mockExecuteRaw.mock.calls.find((c) =>
        /UPDATE action_provenance SET/i.test(sqlOf(c)) && /external_ref = \?/i.test(sqlOf(c)),
      );
      expect(refBlank).toBeDefined();
      expect(sqlOf(refBlank as unknown[])).toMatch(/tenant_id = \? ::uuid/i);
      expect(valuesOf(refBlank as unknown[])).toEqual([EXTERNAL_REF, TENANT]);
    });

    it('the GET does not report alreadyErased while ref-scoped rows remain', async () => {
      wireReads({ resolved: USER, provenanceRows: 3, priorDsr: true, uneased: 2 });
      await expect(getErasureStatusByExternalRef(EXTERNAL_REF, TENANT))
        .resolves.toEqual({ status: 'completed', alreadyErased: false });
    });

    it('POSITIVE CONTROL — with zero remaining it DOES report alreadyErased', async () => {
      // Without this, the assertion above is satisfied by an implementation
      // that can never report true.
      wireReads({ resolved: USER, provenanceRows: 3, priorDsr: true, uneased: 0 });
      await expect(getErasureStatusByExternalRef(EXTERNAL_REF, TENANT))
        .resolves.toEqual({ status: 'completed', alreadyErased: true });
    });
  });

  // ── QA F-1 (Major) — a DENIED erasure is TERMINAL ─────────────────────────
  // `data_subject_requests.status` admits five values (schema CHECK,
  // `docker/init/01-schema.sql:490`): pending, processing, completed, denied,
  // extended. The re-drive predicate was `status <> 'completed'`, so a DENIED
  // DSR read as non-terminal: an erasure a human REFUSED under Art. 17(3) was
  // re-driven, executed irreversibly, and the denial overwritten with
  // 'completed' — the record of the refusal destroyed by the act it forbade.
  describe('a DENIED erasure DSR is terminal and is never re-driven (QA F-1)', () => {
    it('POST answers the refusal and runs NO erasure step at all', async () => {
      wireReads({ resolved: USER, provenanceRows: 1, deniedDsr: true });
      const r = await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
      expect(r).toEqual({ status: 'denied', alreadyErased: false });
      // The whole point: nothing was written. Not the anonymisation, not the
      // completion, not a new DSR. A denial that gets overwritten is worse than
      // a denial that is merely ignored.
      expect(mockExecuteRaw).not.toHaveBeenCalled();
      expect(completionWrites()).toHaveLength(0);
    });

    it('POST never reports a denial as alreadyErased — nothing WAS erased', async () => {
      wireReads({ resolved: USER, provenanceRows: 1, deniedDsr: true });
      const r = await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
      // The distinction that matters to S: `completed/alreadyErased:true` means
      // the obligation is discharged; `denied` means it was refused. Collapsing
      // the second into the first tells S an erasure happened that did not.
      expect(r.status).toBe('denied');
      expect(r.alreadyErased).toBe(false);
    });

    it('GET reports the denial too, so the convergence sweep stops', async () => {
      // The read side is half the defect: reading only 'completed' made a denied
      // subject report outstanding work forever, which is what kept S POSTing.
      wireReads({ resolved: USER, provenanceRows: 1, deniedDsr: true });
      await expect(getErasureStatusByExternalRef(EXTERNAL_REF, TENANT))
        .resolves.toEqual({ status: 'denied', alreadyErased: false });
    });

    it('the terminal read asks for BOTH terminal statuses, not just completed', async () => {
      wireReads({ resolved: USER, provenanceRows: 1, deniedDsr: true });
      await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
      const terminalRead = mockQueryRaw.mock.calls.find((c) =>
        /FROM data_subject_requests/i.test(sqlOf(c)) && /status IN/i.test(sqlOf(c)),
      );
      expect(terminalRead).toBeDefined();
      expect(sqlOf(terminalRead as unknown[])).toMatch(/status IN \('completed', 'denied'\)/i);
    });

    it("CONTROL — 'extended' is NOT terminal and is still re-driven", async () => {
      // The control that stops the fix from being 'treat everything as
      // terminal'. `extended` is an Art. 12(3) extension of the RESPONSE
      // DEADLINE, not a conclusion: the request is still live and must still be
      // driven. If this test passed alongside the denied ones under a fix that
      // widened the terminal set, the widening would be silently wrong.
      wireReads({ resolved: USER, provenanceRows: 1, deniedDsr: false, openDsr: 'dsr-extended' });
      const r = await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
      expect(r).toEqual({ status: 'completed', alreadyErased: false });
      // It re-drove the EXISTING row rather than filing a new one...
      const filed = mockQueryRaw.mock.calls.filter((c) => /INSERT INTO data_subject_requests/i.test(sqlOf(c)));
      expect(filed).toHaveLength(0);
      // ...and it actually ran the erasure.
      expect(mockExecuteRaw.mock.calls.find((c) => /UPDATE users SET/i.test(sqlOf(c)))).toBeDefined();
    });

    it('CONTROL — the re-drive predicate excludes both terminal statuses', async () => {
      wireReads({ resolved: USER, provenanceRows: 1, openDsr: 'dsr-open' });
      await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
      const redrive = mockQueryRaw.mock.calls.find((c) =>
        /FROM data_subject_requests/i.test(sqlOf(c)) && /status NOT IN/i.test(sqlOf(c)),
      );
      expect(redrive).toBeDefined();
      expect(sqlOf(redrive as unknown[])).toMatch(/status NOT IN \('completed', 'denied'\)/i);
      // The literal the defect was written with must be gone, not merely joined.
      expect(sqlOf(redrive as unknown[])).not.toMatch(/status <> 'completed'/i);
    });
  });

  // ── QA F-5 (Minor) ────────────────────────────────────────────────────────
  // S retries without bound. Filing a fresh DSR per attempt accumulates one
  // orphan row per retry, and from the second attempt the recorded `email` is
  // the post-anonymisation sentinel rather than the subject's address.
  it('re-drives an EXISTING non-terminal DSR instead of filing another (QA F-5)', async () => {
    wireReads({ resolved: USER, provenanceRows: 1, priorDsr: false, openDsr: 'dsr-open-from-a-failed-attempt' });
    await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);

    const inserts = mockQueryRaw.mock.calls.filter((c) =>
      /INSERT INTO data_subject_requests/i.test(sqlOf(c)),
    );
    expect(inserts).toHaveLength(0);

    // And the completion write names THAT row, not a new one.
    const [completion] = completionWrites();
    expect(valuesOf(completion as unknown[])).toContain('dsr-open-from-a-failed-attempt');
    // Peter F8: the write also carries an audit-trail entry naming the actor,
    // because `updateDSRStatus` cannot run on this path (KS-754) and its
    // substitute previously recorded strictly less than the call it replaced.
    const audit = (valuesOf(completion as unknown[]) as string[])
      .find((v) => typeof v === 'string' && v.includes('"action":"completed"'));
    expect(audit).toBeDefined();
    expect(JSON.parse(audit as string).actor).toBe(CONNECTOR_PRINCIPAL);
  });

  it('POSITIVE CONTROL — with no open DSR it still files one', async () => {
    wireReads({ resolved: USER, provenanceRows: 1, priorDsr: false, openDsr: null });
    await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT);
    const inserts = mockQueryRaw.mock.calls.filter((c) =>
      /INSERT INTO data_subject_requests/i.test(sqlOf(c)),
    );
    expect(inserts).toHaveLength(1);
  });

  it('an external_ref K has NEVER SEEN terminates as completed — it must never 404', async () => {
    // The failure this guards: S retries without bound, so any non-terminal
    // answer here strands the erasure permanently. "No provenance" is not a
    // not-found — it is K holding nothing erasable for that subject.
    wireReads({ resolved: null, provenanceRows: 0, uneased: 0 });
    const r = await executeErasureByExternalRef('never-seen-by-k', CONNECTOR, TENANT);
    expect(r).toEqual({ status: 'completed', alreadyErased: true });
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });
});

describe('KS-695 ask 1 — getErasureStatusByExternalRef', () => {
  beforeEach(() => jest.clearAllMocks());

  it('never writes', async () => {
    wireReads({ resolved: USER, provenanceRows: 1, priorDsr: true });
    await getErasureStatusByExternalRef(EXTERNAL_REF, TENANT);
    expect(mockExecuteRaw).not.toHaveBeenCalled();
  });

  it('reports alreadyErased true once the subject is erased, false while outstanding', async () => {
    wireReads({ resolved: USER, provenanceRows: 1, priorDsr: true });
    await expect(getErasureStatusByExternalRef(EXTERNAL_REF, TENANT))
      .resolves.toEqual({ status: 'completed', alreadyErased: true });
    jest.clearAllMocks();
    wireReads({ resolved: USER, provenanceRows: 1, priorDsr: false });
    await expect(getErasureStatusByExternalRef(EXTERNAL_REF, TENANT))
      .resolves.toEqual({ status: 'completed', alreadyErased: false });
  });

  it('is tenant-scoped', async () => {
    wireReads({ resolved: USER, provenanceRows: 1, priorDsr: true });
    await getErasureStatusByExternalRef(EXTERNAL_REF, TENANT);
    const lookup = mockQueryRaw.mock.calls.find((c) =>
      /SELECT resolved_user_id, email_hash FROM action_provenance/i.test(sqlOf(c)),
    );
    expect(valuesOf(lookup as unknown[])).toEqual([EXTERNAL_REF, TENANT]);
  });
});

/**
 * QA F-3 — the ambiguity guard was pinned by NOTHING.
 *
 * `resolveSubjectByExternalRef`'s hash fallback selects with `ORDER BY id ASC`
 * and `LIMIT 2` (`gdprService.ts:1232-1235`). Both are load-bearing: LIMIT 2 is
 * what makes "more than one match" OBSERVABLE at all, and without it the code
 * cannot refuse an ambiguous match — it erases whichever row the planner
 * happened to return first. `ORDER BY id ASC` makes that observation
 * deterministic rather than planner-dependent.
 *
 * Neither was asserted anywhere. Every fixture in this file matches that read
 * with `/SELECT id, tenant_id, organization_id FROM users/i`, which is blind to
 * the tail of the statement — so reverting production to `LIMIT 1`, or dropping
 * the ORDER BY, left the whole suite GREEN while re-opening the exact defect the
 * ambiguity branch exists to close.
 *
 * These assert the statement TEXT, because the behaviour cannot be exhibited
 * through the mock: the FIXTURE decides how many rows come back, so a `LIMIT 1`
 * in production still yields two rows here. The SQL is the only witness.
 */
describe('QA F-3 — the ambiguity guard is pinned to the statement, not to the fixture', () => {
  beforeEach(() => jest.clearAllMocks());

  /** The hash-fallback SELECT, as it was actually issued. */
  async function hashFallbackStatement(): Promise<string> {
    wireReads({
      resolved: null, provenanceRows: 2, hashRows: true,
      hashUsers: [{ id: USER, tenantId: TENANT, orgId: ORG }],
    });
    await executeErasureByExternalRef(EXTERNAL_REF, CONNECTOR, TENANT, ORG);
    const call = mockQueryRaw.mock.calls.find((c) =>
      /SELECT id, tenant_id, organization_id FROM users/i.test(sqlOf(c)),
    );
    // If this ever fails, the fixture no longer reaches the hash fallback and
    // every assertion below would pass vacuously on an empty string.
    expect(call).toBeDefined();
    return sqlOf(call as unknown[]);
  }

  it('selects LIMIT 2 — a revert to LIMIT 1 makes an ambiguous match unobservable', async () => {
    expect(await hashFallbackStatement()).toMatch(/LIMIT\s+2\b/i);
  });

  it('does NOT select LIMIT 1 — stated separately so a failure names the regression', async () => {
    expect(await hashFallbackStatement()).not.toMatch(/LIMIT\s+1\b/i);
  });

  it('orders by id ASC — so "the first row" is deterministic, not planner-dependent', async () => {
    expect(await hashFallbackStatement()).toMatch(/ORDER\s+BY\s+id\s+ASC/i);
  });

  /**
   * CONTROL. The three assertions above only mean something if these matchers
   * COULD fail on this statement — a pattern that matches anything, or a
   * statement the fixture never reaches, looks identical to a real pass. This
   * takes the statement actually issued, applies the regression by hand, and
   * proves each matcher flips.
   */
  it('CONTROL — the same matchers reject a LIMIT 1 / unordered version of the same statement', async () => {
    const real = await hashFallbackStatement();
    const reverted = real.replace(/ORDER\s+BY\s+id\s+ASC/i, '').replace(/LIMIT\s+2\b/i, 'LIMIT 1');
    expect(real).not.toEqual(reverted);
    expect(reverted).not.toMatch(/LIMIT\s+2\b/i);
    expect(reverted).not.toMatch(/ORDER\s+BY\s+id\s+ASC/i);
    expect(reverted).toMatch(/LIMIT\s+1\b/i);
  });
});
