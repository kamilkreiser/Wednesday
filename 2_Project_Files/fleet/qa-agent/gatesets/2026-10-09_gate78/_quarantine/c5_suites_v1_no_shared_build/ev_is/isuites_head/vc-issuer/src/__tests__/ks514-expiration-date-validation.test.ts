/**
 * KS-514 — POST /api/credentials returned 500 INTERNAL_ERROR "Invalid time
 * value" for an unparseable `expirationDate`.
 *
 * Mechanism: routes/credentials.ts did `new Date(request.expirationDate)` and
 * handed the result to the VC builder, whose setExpirationDate calls
 * `.toISOString()` (packages/shared/src/vc/builder.ts:97). On an Invalid Date
 * that throws a JS RangeError, which escaped to a 500.
 *
 * Two corrections to the ticket, both measured live against the running
 * service before this fix was written:
 *
 *  1. The ticket says the VC_SIGNING_KEY 503 gate short-circuits before the
 *     date parse, so the bug needs the key SET to reach. It does not — the
 *     parse is at credentials.ts:119 and the gate at :129, so the 500
 *     reproduces on a stock local stack with the key unset. Confirmed: 500.
 *
 *  2. The ticket names `certificationDate` alongside `expirationDate`. Only
 *     `expirationDate` can throw — `certificationDate` is passed through as a
 *     STRING (builder.ts:119) and never parsed. Confirmed: a bad
 *     certificationDate with a valid expirationDate returns the by-design 503,
 *     not a 500.
 *
 * The schema is exported so this suite does not have to import index.ts, which
 * calls app.listen() at module load — the same reason ks444.requestSchema.test
 * exists.
 */

import { describe, it, expect } from 'vitest';
import { IssueCredentialSchema } from '../routes/credentials';

const base = {
  documentId: 'doc-1',
  documentHash: 'abc',
  documentTitle: 'Title',
  documentType: 'PropertyDeed',
};

const parse = (over: Record<string, unknown>) =>
  IssueCredentialSchema.safeParse({ ...base, ...over });

describe('KS-514: expirationDate must be rejected as 400, never crash to 500', () => {
  describe('rejects values that produce an Invalid Date', () => {
    it.each([
      ['not-a-date'],
      ['also-bad'],
      ['2026-13-45'],
      ['NaN'],
      ['Invalid Date'],
    ])('rejects %o', (value) => {
      expect(parse({ expirationDate: value }).success).toBe(false);
    });

    it('rejects a numeric-looking string that Date cannot parse', () => {
      expect(parse({ expirationDate: 'ffff' }).success).toBe(false);
    });
  });

  describe('POSITIVE CONTROL — real date formats still pass', () => {
    // Without these the suite would pass against a schema that rejects
    // everything, which would turn a 500 into a 400 for legitimate callers.
    it.each([
      ['2027-01-01T00:00:00Z'],
      ['2027-01-01T00:00:00.000Z'],
      ['2027-01-01'],
      ['2027-12-31T23:59:59+10:00'],
    ])('accepts %o', (value) => {
      expect(parse({ expirationDate: value }).success).toBe(true);
    });

    it('still accepts a request with NO expirationDate — the field is optional', () => {
      expect(parse({}).success).toBe(true);
    });
  });

  describe('EMPTY means ABSENT, not "bad date" (#741 review)', () => {
    // These two were rejected by this branch's first draft, and that was a
    // contract narrowing the ticket never asked for. Before this PR they passed
    // the schema and were skipped by the truthiness check at credentials.ts:136,
    // so they never reached the Date constructor and were never part of the 500.
    //
    // The cost was MEASURED, not argued: Peter's post-fix sweep found exactly one
    // new failure attributable to this branch — Schemathesis
    // `positive_data_acceptance` on `"expirationDate": ""`, answered 400 by the
    // draft. Mapping empty to undefined restores the prior behaviour and closes it.
    it.each([[''], ['   '], ['\t\n ']])('accepts %o and drops the field', (value) => {
      const r = parse({ expirationDate: value });
      expect(r.success).toBe(true);
      if (r.success) expect(r.data.expirationDate).toBeUndefined();
    });
  });

  describe('the subject and the top level cannot disagree (KS-201, #741 review)', () => {
    // setExpirationDate normalises (builder.ts:97 `date.toISOString()`) but
    // setCredentialSubjectFromRequest passes the RAW string through
    // (builder.ts:120). Both read validationResult.data, so normalising at the
    // boundary makes them agree by construction. Without the transform a
    // credential could be anchored whose subject reads "2027-02-30" while its
    // top-level expirationDate reads 2027-03-02T00:00:00.000Z.
    it('normalises a rolled-over date to canonical UTC', () => {
      const r = parse({ expirationDate: '2027-02-30' });
      expect(r.success).toBe(true);
      // JS rolls 30 Feb to 2 Mar; the point is that ONE value now reaches both
      // sites, not which way the roll goes.
      if (r.success) expect(r.data.expirationDate).toBe('2027-03-02T00:00:00.000Z');
    });

    it('normalises a date-only value the shared isoDateTimeSchema would reject', () => {
      const r = parse({ expirationDate: '2027-01-01' });
      expect(r.success).toBe(true);
      if (r.success) expect(r.data.expirationDate).toBe('2027-01-01T00:00:00.000Z');
    });

    it('normalises an offset date-time to UTC', () => {
      const r = parse({ expirationDate: '2027-12-31T23:59:59+10:00' });
      expect(r.success).toBe(true);
      if (r.success) expect(r.data.expirationDate).toBe('2027-12-31T13:59:59.000Z');
    });

    it('CONTROL: the normalised value is a canonical round-trip', () => {
      // If the transform were dropped, this would read back the raw input and fail.
      const r = parse({ expirationDate: '2027-02-30' });
      if (r.success && r.data.expirationDate) {
        expect(new Date(r.data.expirationDate).toISOString()).toBe(r.data.expirationDate);
      }
    });
  });

  describe('certificationDate is deliberately NOT tightened', () => {
    // It never reaches a Date constructor — builder.ts:119 passes it through
    // as a string — so it cannot cause the 500 this ticket is about.
    // Rejecting it here would narrow inputs the published contract permits
    // (bare `type: string`) and would put the Schemathesis positive generator
    // at odds with the runtime, which is its own class of failure.
    it('accepts an unparseable certificationDate, as today', () => {
      expect(parse({ certificationDate: 'not-a-date' }).success).toBe(true);
    });
  });

  describe('the rejection carries a usable message', () => {
    it('names the field and says what was wrong', () => {
      const r = parse({ expirationDate: 'not-a-date' });
      expect(r.success).toBe(false);
      if (!r.success) {
        const issue = r.error.issues.find((i) => i.path.includes('expirationDate'));
        expect(issue).toBeDefined();
        expect(issue!.message).toMatch(/date/i);
      }
    });
  });
});
