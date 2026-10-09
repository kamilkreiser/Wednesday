/**
 * KS-444 — POST /api/referrals/qualify request validation.
 *
 * The published spec (ReferralQualifyRequest) declares exactly one required
 * plain string: `userId`. The old handler used a manual `if (!userId)` truthy
 * check, which drifted from that contract in both directions:
 *   - the spec-legal empty string was rejected with 400 "userId is required";
 *   - spec-violating non-string bodies (e.g. `{ userId: {} }` — truthy) fell
 *     through to the service and answered 200-with-no-effect.
 * The route now parses `qualifyReferralSchema` (userId: z.string()) and
 * answers the canonical 400 BAD_REQUEST envelope on a Zod failure.
 */

import { describe, it, expect, vi } from 'vitest';
import express from 'express';

// The route module pulls in referralService (DB-backed). Stub it so importing
// the schemas/routes never touches a real datastore. qualifyReferral resolves
// null = "no pending referral for this user" (the business no-effect path).
vi.mock('../services/referralService', () => ({
  referralService: { qualifyReferral: vi.fn(async () => null) },
}));

import { qualifyReferralSchema } from '../routes/referrals';

describe('KS-444 — qualifyReferralSchema matches the published contract', () => {
  it('accepts a plain string userId', () => {
    expect(qualifyReferralSchema.parse({ userId: 'user-1' }).userId).toBe('user-1');
  });

  it('accepts the spec-legal empty string (no minLength is published)', () => {
    expect(qualifyReferralSchema.parse({ userId: '' }).userId).toBe('');
  });

  it('rejects a missing userId', () => {
    expect(() => qualifyReferralSchema.parse({})).toThrow();
  });

  it('rejects a non-string userId (object)', () => {
    expect(() => qualifyReferralSchema.parse({ userId: {} })).toThrow();
  });
});

describe('KS-444 — POST /api/referrals/qualify route behaviour', () => {
  interface Envelope {
    success: boolean;
    data?: { qualified: boolean; message?: string };
    error?: { code: string; message: string };
  }

  /** Drive the real route stack (express.json → referralRoutes) as index.ts wires it, minus auth. */
  async function postQualify(body: string): Promise<{ status: number; body: Envelope }> {
    const { referralRoutes } = await import('../routes/referrals');
    const app = express();
    app.use(express.json());
    app.use('/api/referrals', referralRoutes);

    const server = app.listen(0, '127.0.0.1');
    try {
      // KS-845: listen(0, host) defers the bind, so address() is null until 'listening' fires.
      await new Promise<void>((r) => server.once('listening', () => r()));
      const port = (server.address() as { port: number }).port;
      const res = await fetch(`http://127.0.0.1:${port}/api/referrals/qualify`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body,
      });
      return { status: res.status, body: (await res.json()) as Envelope };
    } finally {
      server.close();
    }
  }

  it('answers 400 BAD_REQUEST for a spec-violating non-string userId (was 200-with-no-effect)', async () => {
    const r = await postQualify(JSON.stringify({ userId: {} }));
    expect(r.status).toBe(400);
    expect(r.body.success).toBe(false);
    expect(r.body.error?.code).toBe('BAD_REQUEST');
    expect(r.body.error?.message).toBe('Validation error');
  });

  it('answers 400 BAD_REQUEST when userId is missing', async () => {
    const r = await postQualify(JSON.stringify({}));
    expect(r.status).toBe(400);
    expect(r.body.error?.code).toBe('BAD_REQUEST');
  });

  it('accepts the spec-legal empty string and reports the business no-pending result (was 400)', async () => {
    const r = await postQualify(JSON.stringify({ userId: '' }));
    expect(r.status).toBe(200);
    expect(r.body.success).toBe(true);
    expect(r.body.data?.qualified).toBe(false);
  });

  it('accepts a normal string userId with no pending referral → 200 qualified:false', async () => {
    const r = await postQualify(JSON.stringify({ userId: 'user-with-no-referral' }));
    expect(r.status).toBe(200);
    expect(r.body.data?.qualified).toBe(false);
  });
});
