/**
 * QA F-4 — `resolveOnBehalfOf` compared Organisation ids RAW.
 *
 * `provenance.ts` matched a PG-canonical `users.organization_id` against a
 * connector-supplied `connectorOrgId` with `!==` / `===` and no normalisation,
 * while its SIBLING resolver — `gdprService.ts:1249`, same relationship, same
 * pair of values — normalises both sides (trim + lowercase). The two resolvers
 * had drifted apart on the one comparison that decides Organisation identity.
 *
 * Two consequences, both silent:
 *   - a same-org caller whose claim differs only in CASE is 403'd, and
 *   - a same-org user is treated as org-less, so the write loses true per-user
 *     attribution and records verbatim provenance instead.
 *
 * THE CONTROL PAIR: every case below holds the Organisation IDENTITY constant
 * and varies ONLY its rendering. That is what makes these tests measure
 * normalisation rather than re-measuring the org compare that already existed —
 * a differently-named org would fail with or without the fix.
 */

process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const mockQueryRaw = jest.fn();
jest.mock('../db', () => ({
  prisma: {
    get $queryRaw() {
      return (...args: unknown[]) => mockQueryRaw(...args);
    },
  },
}));
jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    ...(jest.requireActual('@secuura/shared') as Record<string, unknown>),
    lookupHash: (v: string) => `hash-of-${v}`,
  }),
);

// eslint-disable-next-line @typescript-eslint/no-var-requires
const { resolveOnBehalfOf, OnBehalfOfError } = require('../services/provenance');

const USER_ID = '11111111-1111-1111-1111-111111111111';
const OBO = { email: 'Jane@Org.Example', displayName: 'Jane Doe', externalRef: 'guid-1' };

/** The org id as PostgreSQL hands it back. */
const ORG_CANONICAL = 'cccccccc-cccc-cccc-cccc-cccccccccccc';
/** The SAME organisation, as a connector might send it. */
const ORG_UPPER = ORG_CANONICAL.toUpperCase();
const ORG_PADDED = `  ${ORG_CANONICAL}  `;
/** A genuinely DIFFERENT organisation — the negative pole. */
const ORG_OTHER = 'dddddddd-dddd-dddd-dddd-dddddddddddd';

function userInOrg(organization_id: string | null) {
  mockQueryRaw.mockReset();
  mockQueryRaw.mockResolvedValue([{ id: USER_ID, organization_id }]);
}

describe('QA F-4 — Organisation ids are normalised before comparison', () => {
  describe('same organisation, different rendering — must RESOLVE', () => {
    it('exact match resolves (baseline — passes with or without the fix)', async () => {
      userInOrg(ORG_CANONICAL);
      await expect(resolveOnBehalfOf(OBO, ORG_CANONICAL)).resolves.toBe(USER_ID);
    });

    it('caller claim differs only in CASE — same org, so it resolves', async () => {
      userInOrg(ORG_CANONICAL);
      await expect(resolveOnBehalfOf(OBO, ORG_UPPER)).resolves.toBe(USER_ID);
    });

    it('caller claim differs only in surrounding WHITESPACE — same org, so it resolves', async () => {
      userInOrg(ORG_CANONICAL);
      await expect(resolveOnBehalfOf(OBO, ORG_PADDED)).resolves.toBe(USER_ID);
    });

    it('the STORED value differs only in case — same org, so it resolves', async () => {
      userInOrg(ORG_UPPER);
      await expect(resolveOnBehalfOf(OBO, ORG_CANONICAL)).resolves.toBe(USER_ID);
    });
  });

  describe('the refusal still keys on IDENTITY, not on rendering', () => {
    it('a genuinely different organisation is still 403 — the fix did not widen the gate', async () => {
      userInOrg(ORG_OTHER);
      await expect(resolveOnBehalfOf(OBO, ORG_CANONICAL)).rejects.toBeInstanceOf(OnBehalfOfError);
    });

    it('a different org in a different CASE is still 403 — normalisation is not a bypass', async () => {
      userInOrg(ORG_OTHER.toUpperCase());
      await expect(resolveOnBehalfOf(OBO, ORG_CANONICAL)).rejects.toBeInstanceOf(OnBehalfOfError);
    });

    it('an org-LESS user resolves to null — not attributed, and NOT 403', async () => {
      userInOrg(null);
      await expect(resolveOnBehalfOf(OBO, ORG_CANONICAL)).resolves.toBeNull();
    });

    it('an org-less user against an EMPTY caller org is still null, never a match', async () => {
      userInOrg(null);
      await expect(resolveOnBehalfOf(OBO, '   ')).resolves.toBeNull();
    });
  });
});
