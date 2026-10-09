import { describe, it, expect, vi } from 'vitest';

// The route module pulls in referralService (DB-backed). Stub it so importing
// the schemas under test never touches a real datastore.
vi.mock('../services/referralService', () => ({ referralService: {} }));

import { generateCodeSchema, applyCodeSchema } from '../routes/referrals';

/**
 * KS-202 — referral codes must be trimmed both when created and when looked up,
 * otherwise a code stored with a trailing space (referral-lookup risk #3) never
 * matches a clean-typed input and silently voids the referral.
 */
describe('KS-202 — referral code trimming', () => {
  it('trims a trailing space on a generated custom code', () => {
    const parsed = generateCodeSchema.parse({ customCode: 'REF2026 ' });
    expect(parsed.customCode).toBe('REF2026');
  });

  it('trims the code at lookup so a padded paste still matches', () => {
    const parsed = applyCodeSchema.parse({
      code: ' REF2026',
      userId: '00000000-0000-0000-0000-000000000001',
    });
    expect(parsed.code).toBe('REF2026');
  });

  it('trims customLabel', () => {
    const parsed = generateCodeSchema.parse({ customLabel: '  Spring promo  ' });
    expect(parsed.customLabel).toBe('Spring promo');
  });
});
