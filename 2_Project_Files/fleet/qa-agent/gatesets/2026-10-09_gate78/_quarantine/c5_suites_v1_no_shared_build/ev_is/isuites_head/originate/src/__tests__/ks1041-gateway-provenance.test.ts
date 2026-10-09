/**
 * =============================================================================
 * KS-1041 Step 2 — gateway provenance
 * =============================================================================
 * The vulnerability, measured on the demo box from `secuura-verifier-frontend`
 * (a container with no business reaching originate):
 *
 *   | request                                            | result  |
 *   | -------------------------------------------------- | ------- |
 *   | direct to originate:4000, no headers                | 401     |
 *   | direct, forged `x-user-role: connector` + tenant id | **200** |
 *   | the SAME forged request through api-gateway:8080    | 401     |
 *
 * `routes/metering.ts:42` promotes `x-user-role: connector` straight into
 * `req.user` without consulting a JWT. Through the gateway that is safe — the
 * gateway strips client-supplied trust headers and re-sets them from a verified
 * JWT. On the direct path nothing establishes who set them.
 *
 * BOTH ARMS ARE PINNED HERE, deliberately. A suite that only proves the
 * refusal has not shown the service still works — it is equally satisfied by a
 * middleware that rejects everything.
 *
 *   ARM A (refusal)  — a forged trust header on an unvouched request is DROPPED,
 *                      so the metering shim never fires and auth answers 401.
 *   ARM B (function) — the same headers on a gateway-vouched request SURVIVE,
 *                      so the shim fires and the request succeeds.
 *   ARM C (no leak)  — the vouch itself never travels past this service.
 *
 * The probe route below is a faithful copy of the metering shim's predicate
 * (`routes/metering.ts:42`), not an approximation: it is the actual thing being
 * protected. Using the real router would drag in `../db` and `config.ts`, which
 * demand DATABASE_URL at module load — the reason the other unit suites here
 * use a local harness.
 * =============================================================================
 */

import express, { Request, Response } from 'express';
import {
  createGatewayProvenanceMiddleware,
  vouchMatches,
  describeState,
  UNVOUCHED_STRIP_PATTERN,
  VOUCH_HEADER,
} from '../utils/gatewayProvenance';

const SECRET = 'a'.repeat(64);
const WRONG_SECRET = 'b'.repeat(64);

// Same harness as the other route tests in this service: a real listener driven
// over HTTP. This service has no supertest and adding a test-only dep would
// break the Docker build, which compiles __tests__.
function buildApp(secret: string) {
  const app = express();
  app.use(express.json());
  app.use(createGatewayProvenanceMiddleware(secret));

  // Faithful copy of routes/metering.ts:42 — the shim this change protects.
  app.get('/probe/metering', (req: Request, res: Response) => {
    if (req.headers['x-user-role'] === 'connector' && req.headers['x-tenant-id']) {
      return res.status(200).json({
        ok: true,
        user: { userId: String(req.headers['x-user-id'] || 'connector'), role: 'connector' },
        tenantId: req.headers['x-tenant-id'],
      });
    }
    // What the real route's own auth does once the shim has not fired.
    return res.status(401).json({ ok: false, error: 'UNAUTHENTICATED' });
  });

  // Reports what survived, so ARM C can assert on the vouch specifically.
  app.get('/probe/headers', (req: Request, res: Response) => {
    res.status(200).json({ headers: Object.keys(req.headers).sort() });
  });

  return app;
}

type Harness = { baseUrl: string; close: () => void };

async function listen(app: express.Express): Promise<Harness> {
  // 127.0.0.1, never 0.0.0.0 — KS-860: test listeners must not bind all interfaces.
  const server = await new Promise<ReturnType<typeof app.listen>>((resolve) => {
    const s = app.listen(0, '127.0.0.1', () => resolve(s));
  });
  const address = server.address();
  const port = typeof address === 'object' && address ? address.port : 0;
  return { baseUrl: `http://127.0.0.1:${port}`, close: () => server.close() };
}

const FORGED = {
  'x-user-role': 'connector',
  'x-tenant-id': '11111111-1111-4111-8111-111111111111',
  'x-user-id': 'attacker',
};

describe('KS-1041 Step 2 — gateway provenance', () => {
  describe('ARM A — a forged trust header on an UNVOUCHED request is refused', () => {
    let h: Harness;
    beforeAll(async () => { h = await listen(buildApp(SECRET)); });
    afterAll(() => h.close());

    it('drops the forged headers, so the metering shim never fires (401)', async () => {
      const res = await fetch(`${h.baseUrl}/probe/metering`, { headers: FORGED });
      expect(res.status).toBe(401);
      await expect(res.json()).resolves.toMatchObject({ error: 'UNAUTHENTICATED' });
    });

    it('refuses a WRONG vouch exactly as it refuses no vouch — a present header is not a valid one', async () => {
      const res = await fetch(`${h.baseUrl}/probe/metering`, {
        headers: { ...FORGED, [VOUCH_HEADER]: WRONG_SECRET },
      });
      expect(res.status).toBe(401);
    });

    it('refuses a vouch that is a PREFIX of the secret — a truncated guess must not pass', async () => {
      const res = await fetch(`${h.baseUrl}/probe/metering`, {
        headers: { ...FORGED, [VOUCH_HEADER]: SECRET.slice(0, 32) },
      });
      expect(res.status).toBe(401);
    });

    it('strips the whole trust family, not just the two the shim reads', async () => {
      const res = await fetch(`${h.baseUrl}/probe/headers`, {
        headers: {
          ...FORGED,
          'x-organization-id': 'org-1',
          'x-tenant-override': 'other-tenant',
          'x-policy-result': 'allow',
          'x-roles': 'admin',
        },
      });
      const { headers } = (await res.json()) as { headers: string[] };
      expect(headers.filter((k) => UNVOUCHED_STRIP_PATTERN.test(k))).toEqual([]);
    });

    it('CONTROL — leaves non-trust headers alone, so the strip is targeted and not a blanket wipe', async () => {
      // Without this, a middleware that deleted every header would pass every
      // assertion above while breaking the service.
      const res = await fetch(`${h.baseUrl}/probe/headers`, {
        headers: { ...FORGED, 'x-request-id': 'req-123', authorization: 'Bearer t' },
      });
      const { headers } = (await res.json()) as { headers: string[] };
      expect(headers).toContain('x-request-id');
      expect(headers).toContain('authorization');
    });
  });

  describe('ARM B — a genuine gateway-vouched request still WORKS', () => {
    let h: Harness;
    beforeAll(async () => { h = await listen(buildApp(SECRET)); });
    afterAll(() => h.close());

    it('honours the trust headers and the metering shim fires (200)', async () => {
      const res = await fetch(`${h.baseUrl}/probe/metering`, {
        headers: { ...FORGED, [VOUCH_HEADER]: SECRET },
      });
      expect(res.status).toBe(200);
      await expect(res.json()).resolves.toMatchObject({
        ok: true,
        user: { role: 'connector' },
        tenantId: FORGED['x-tenant-id'],
      });
    });

    it('leaves a request that sends NO trust headers working — the direct callers that legitimately exist', async () => {
      // m365-integration sends only Content-Type; nft-certificate sends none.
      // Stripping must be a no-op for them, which is why this strips instead
      // of refusing.
      const res = await fetch(`${h.baseUrl}/probe/headers`, {
        headers: { 'content-type': 'application/json' },
      });
      expect(res.status).toBe(200);
    });
  });

  describe('ARM C — the vouch never travels past this service', () => {
    let h: Harness;
    beforeAll(async () => { h = await listen(buildApp(SECRET)); });
    afterAll(() => h.close());

    it('deletes the vouch header after a successful match', async () => {
      // originate makes its own hops (originate -> anchoring). The secret must
      // not ride along on them.
      const res = await fetch(`${h.baseUrl}/probe/headers`, {
        headers: { [VOUCH_HEADER]: SECRET },
      });
      const { headers } = (await res.json()) as { headers: string[] };
      expect(headers).not.toContain(VOUCH_HEADER);
    });

    it('also removes an INVALID vouch, so a probe cannot confirm the header name downstream', async () => {
      const res = await fetch(`${h.baseUrl}/probe/headers`, {
        headers: { [VOUCH_HEADER]: WRONG_SECRET },
      });
      const { headers } = (await res.json()) as { headers: string[] };
      expect(headers).not.toContain(VOUCH_HEADER);
    });
  });

  describe('unconfigured — fail-open, but LOUD', () => {
    let h: Harness;
    beforeAll(async () => { h = await listen(buildApp('')); });
    afterAll(() => h.close());

    it('is inert when the secret is unset — pinned deliberately, not by accident', async () => {
      // Fail-closed here would mean an unconfigured deploy loses every
      // gateway-set identity at once. This test exists so that a future change
      // to fail-closed is a decision someone makes, not a silent regression.
      const res = await fetch(`${h.baseUrl}/probe/metering`, { headers: FORGED });
      expect(res.status).toBe(200);
    });

    it('the boot line names the CONSEQUENCE, not the flag state', async () => {
      const off = describeState('');
      expect(off.level).toBe('warn');
      expect(off.message).toContain('honoured from ANY caller');
      const on = describeState(SECRET);
      expect(on.level).toBe('info');
    });
  });

  describe('vouchMatches — the comparison itself', () => {
    it.each([
      ['exact match', SECRET, true],
      ['wrong value of equal length', WRONG_SECRET, false],
      ['prefix of the secret', SECRET.slice(0, 32), false],
      ['secret plus a suffix', `${SECRET}x`, false],
      ['empty string', '', false],
    ])('%s -> %s', (_label, presented, expected) => {
      expect(vouchMatches(presented, SECRET)).toBe(expected);
    });

    it.each([
      ['undefined (header absent)', undefined],
      ['an array (duplicated header)', [SECRET, SECRET]],
      ['a number', 42],
      ['null', null],
    ])('rejects a non-string presented value: %s', (_label, presented) => {
      expect(vouchMatches(presented, SECRET)).toBe(false);
    });

    it('never matches when the configured secret is empty, even against an empty presented value', () => {
      // Otherwise an unconfigured service would treat a header-less request as
      // vouched, which is the opposite of the inert behaviour intended.
      expect(vouchMatches('', '')).toBe(false);
      expect(vouchMatches('anything', '')).toBe(false);
    });
  });
});
