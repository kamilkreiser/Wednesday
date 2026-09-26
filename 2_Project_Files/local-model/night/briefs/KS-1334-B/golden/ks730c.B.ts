// KS-730 part C (originate routes/adminConfig.ts): forty-six inline handlers returned `err.message`
// verbatim unless NODE_ENV === 'production', so development, demo, test and an UNSET NODE_ENV all
// answered an admin-configuration route with raw internal text. This is the largest of the three files
// KS-730 enumerates, and the reason the ticket asked for a helper rather than 67 edited ternaries.
//
// TWO KINDS OF CELL, and the difference is stated rather than blurred:
//   * BEHAVIOURAL cells drive four routes end to end over a loopback listener and read the real 500
//     body and the real log call. Strong evidence, four of forty-six.
//   * A SOURCE cell pins all forty-six by construction: zero live ternaries, forty-six helper calls,
//     forty-six DISTINCT contexts. Weaker — it reads the file, not the behaviour — and it is what
//     covers the other forty-two. Driving forty-six routes would need forty-six service shapes for no
//     additional discrimination.
process.env.NODE_ENV = 'development';
process.env.DATABASE_URL = process.env.DATABASE_URL || 'postgresql://test:test@localhost:5432/test';

const mockQueryRaw = jest.fn();
const mockExecuteRaw = jest.fn();
const mockLoggerError = jest.fn();

jest.mock('../db', () => ({
  prisma: { $queryRaw: mockQueryRaw, $executeRaw: mockExecuteRaw },
  refreshTenantConfigs: jest.fn(),
  withTenant: (_t: unknown, fn: () => unknown) => fn(),
  getTenantManager: () => null,
}));

jest.mock('../middleware/auth', () => {
  const actual = jest.requireActual('../middleware/auth');
  return {
    ...actual,
    authenticate: () => (req: any, _res: unknown, next: () => void) => {
      const principal = { id: 'u-ks730c', role: 'SYSTEM_ADMIN', tenantId: 't-ks730c' };
      req._secuuraUser = principal; req.user = principal; req.tenantId = principal.tenantId;
      next();
    },
    requireRole: () => (_req: unknown, _res: unknown, next: () => void) => next(),
  };
});

jest.mock('@secuura/shared', () =>
  require('./helpers/sharedModuleMock').makeSharedMock({
    ...(jest.requireActual('@secuura/shared') as Record<string, unknown>),
    runWithPlatformScope: (fn: () => unknown) => fn(),
    queryWithTenantGuc: jest.fn(),
  }),
);

jest.mock('../utils/logger', () => ({
  logger: { info: jest.fn(), warn: jest.fn(), error: mockLoggerError, debug: jest.fn() },
}));

import express from 'express';
import type { AddressInfo } from 'net';
import { adminConfigRouter } from '../routes/adminConfig';
import { readFileSync } from 'fs';
import path from 'path';

// THE FIXTURE IS LOAD-BEARING, and choosing it carelessly makes every cell below vacuous.
// All four routes' catch blocks open with a PRE-EXISTING benign branch:
//     if (err?.message?.includes('does not exist') || err?.code === '42P01') return res.json({ ... });
// The first draft of this cell threw `'relation admin_settings does not exist ...'`, which matches
// that substring, so all four routes answered 200 with an empty list and NEVER REACHED fail500 —
// 9 of these 12 cells failed, and the three that passed did so without exercising the fix at all.
// This message must therefore be a realistic internal error that does NOT contain 'does not exist'
// and carries no `code`. `control KS-730 C0` below pins the benign branch so the trap cannot return
// silently, and C1/C2 assert fail500 was REACHED rather than only that the body looks clean.
const LEAK = 'duplicate key value violates unique constraint "admin_settings_pkey" ks730c-private-detail';
const NODE_ENVS = ['development', 'demo', 'test', undefined];
const CONSTANT_BODY = { success: false, error: { code: 'INTERNAL_ERROR', message: 'Internal server error' } };
const ORIGINAL_NODE_ENV = process.env.NODE_ENV;

const app = express();
app.use('/api/admin', express.json(), adminConfigRouter);
let server: ReturnType<typeof app.listen>;
let baseUrl = '';

beforeAll(async () => {
  await new Promise<void>((resolve) => { server = app.listen(0, '127.0.0.1', () => resolve()); });
  baseUrl = 'http://127.0.0.1:' + (server.address() as AddressInfo).port;
});
afterAll(() => {
  if (ORIGINAL_NODE_ENV === undefined) delete process.env.NODE_ENV;
  else process.env.NODE_ENV = ORIGINAL_NODE_ENV;
  server?.close();
});
beforeEach(() => jest.clearAllMocks());

function setNodeEnv(v: string | undefined): void {
  if (v === undefined) delete process.env.NODE_ENV;
  else process.env.NODE_ENV = v;
}

// Four GET routes whose handler reaches prisma.$queryRaw with no body or param to satisfy first —
// verified at source, so the throw is what the cell measures rather than my own fixture.
const ROUTES = [
  { label: 'GET /settings', path: '/settings', context: 'Admin config request failed (GET /api/admin/settings)' },
  { label: 'GET /document-types', path: '/document-types', context: 'Admin config request failed (GET /api/admin/document-types)' },
  { label: 'GET /workflows', path: '/workflows', context: 'Admin config request failed (GET /api/admin/workflows)' },
  { label: 'GET /organizations', path: '/organizations', context: 'Admin config request failed (GET /api/admin/organizations)' },
] as const;

async function call(route: (typeof ROUTES)[number], nodeEnv: string | undefined, throwInDb: boolean): Promise<{ status: number; text: string }> {
  setNodeEnv(nodeEnv);
  if (throwInDb) mockQueryRaw.mockRejectedValue(new Error(LEAK));
  else mockQueryRaw.mockResolvedValue([]);
  const res = await fetch(baseUrl + '/api/admin' + route.path);
  return { status: res.status, text: await res.text() };
}

describe('KS-730 part C: the 46 converted admin-config sites never answer a 500 with err.message', () => {
  it.each(ROUTES)('RED KS-730 C1 $label: the thrown message is not in the 500 body under development, demo, test or unset', async (route) => {
    for (const nodeEnv of NODE_ENVS) {
      const reply = await call(route, nodeEnv, true);
      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      // REACHED, not merely clean: a body without the leak is also what the benign branch and any
      // mock-shaped crash produce. Only fail500 logs this route's context with the thrown text, so
      // this is the assertion that says the code under test actually ran for THIS nodeEnv.
      expect(mockLoggerError.mock.calls.at(-1)).toEqual([route.context, { error: LEAK }]);
    }
  });

  it.each(ROUTES)('RED KS-730 C2 $label: the thrown message is logged once, server-side, with this route named', async (route) => {
    const reply = await call(route, 'development', true);
    expect(reply.status).toBe(500);
    expect(mockLoggerError.mock.calls).toEqual([[route.context, { error: LEAK }]]);
  });

  it('KS-730 C3 SOURCE: all forty-six sites are routed through the helper, each with a DISTINCT context', () => {
    // Weaker than the behavioural cells and deliberately so: it reads the file rather than the
    // behaviour, and it is what covers the forty-two routes not driven here.
    const src = readFileSync(path.join(__dirname, '..', 'routes', 'adminConfig.ts'), 'utf8');
    const lines = src.split('\n');
    const liveTernaries = lines.filter(
      (l) => l.includes("NODE_ENV === 'production'") && !l.trim().startsWith('*') && !l.trim().startsWith('//') && !l.includes('logger.'),
    );
    const helperCalls = lines.filter((l) => l.includes('fail500(res,'));
    const contexts = helperCalls.map((l) => (l.match(/fail500\(res, '([^']+)'/) ?? [])[1]);
    // DISTINCTNESS is asserted, not just the count: a mislabelled context is worse than none, because
    // it sends a reader to the wrong handler. 46 generated strings could silently collide.
    expect({ liveTernaries: liveTernaries.length, helperCalls: helperCalls.length, distinctContexts: new Set(contexts).size })
      .toEqual({ liveTernaries: 0, helperCalls: 50, distinctContexts: 50 });
    expect(contexts.filter((c) => !c)).toEqual([]);
  });

  it('control KS-730 C0: a "does not exist" error still answers 200 and never reaches fail500', async () => {
    // PRE-EXISTING behaviour this change must NOT alter, and the discriminator for the fixture
    // trap described at LEAK. It also proves the 500s above are caused by the THROWN TEXT rather
    // than by throwing at all: same routes, same mechanism, different message, different answer.
    for (const route of ROUTES) {
      setNodeEnv('development');
      mockQueryRaw.mockRejectedValue(new Error('relation whatever does not exist'));
      const res = await fetch(baseUrl + '/api/admin' + route.path);
      expect({ label: route.label, status: res.status }).toEqual({ label: route.label, status: 200 });
      expect(mockLoggerError).not.toHaveBeenCalled();
      jest.clearAllMocks();
    }
  });

  it('KS-730 C4 SOURCE: the four UNCONDITIONAL err.message sites are named, not silently left', () => {
    // WHAT THIS FILE DOES NOT COVER, pinned in code rather than only in the PR body. KS-730 is about
    // the off-production ternary shape; these four sites return err.message in EVERY environment,
    // production included, which is a worse class and a different one. They are PRE-EXISTING —
    // measured 4 at the base d7cdecf1d2ee and 4 here — so this change neither introduced nor fixed
    // them. Pinned by their enclosing route so that a FIFTH reds, and so that fixing one reds
    // loudly enough to be a deliberate update of this list rather than a silent drift.
    // They are tracked on KS-1334, whose Done-when requires this KNOWN list to be emptied in the
    // same change that fixes them.
    const src = readFileSync(path.join(__dirname, '..', 'routes', 'adminConfig.ts'), 'utf8');
    const lines = src.split('\n');
    const KNOWN: string[] = [];
    let route = '';
    const found: string[] = [];
    for (const line of lines) {
      const m = line.match(/adminConfigRouter\.(get|post|put|patch|delete)\('([^']+)'/);
      if (m) route = m[1].toUpperCase() + ' ' + m[2];
      if (/message: *err\??\.?message/.test(line)) found.push(route);
    }
    expect(found).toEqual(KNOWN);
  });

  it('control KS-730 C: under production these routes already answered the constant text', async () => {
    for (const route of ROUTES) {
      const reply = await call(route, 'production', true);
      expect({ label: route.label, status: reply.status, body: JSON.parse(reply.text) })
        .toEqual({ label: route.label, status: 500, body: CONSTANT_BODY });
    }
  });

  it('control KS-730 C: a route that does NOT throw answers 200 and logs nothing', async () => {
    // Without this, every "not leaked" pass above is consistent with the router answering 500 always.
    const reply = await call(ROUTES[0], 'development', false);
    expect(reply.status).toBe(200);
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-730 C: the LEAK string really is the thrown text, so "not leaked" is not vacuous', () => {
    expect(new Error(LEAK).message).toBe(LEAK);
    expect(LEAK.length).toBeGreaterThan(20);
  });
});

// KS-1334 part A: two of the four UNCONDITIONAL sites named by C4 above now go through fail500. They
// answered err.message in EVERY environment, production included, so unlike the KS-730 cells the
// production row is the one that separates this class, and it is driven first. Part B covers the
// other two (seed-demo-users, migrate-tenant-data). Its own LEAK carries no double quote: the shared
// LEAK above does, JSON-escapes to a backslash-quote in the body, and so can never be found by includes.
const KS1334_LEAK = 'could not serialize access due to concurrent update ks1334-private-detail';
const KS1334_NODE_ENVS = ['production', 'development', 'demo', 'test', undefined];
const KS1334_ROUTES = [
  { label: 'POST /refresh-tenants', path: '/refresh-tenants', body: {}, context: 'Admin config request failed (POST /api/admin/refresh-tenants)' },
  { label: 'POST /backfill-certification-metadata', path: '/backfill-certification-metadata', body: { issuerName: 'ks1334-issuer' }, context: 'Admin config request failed (POST /api/admin/backfill-certification-metadata)' },
] as const;
const mockRefreshTenantConfigs = (jest.requireMock('../db') as { refreshTenantConfigs: jest.Mock }).refreshTenantConfigs;

async function post1334(route: (typeof KS1334_ROUTES)[number], nodeEnv: string | undefined, throwIt: boolean): Promise<{ status: number; text: string }> {
  setNodeEnv(nodeEnv);
  if (throwIt) {
    mockRefreshTenantConfigs.mockRejectedValue(new Error(KS1334_LEAK));
    mockExecuteRaw.mockRejectedValue(new Error(KS1334_LEAK));
  } else {
    mockRefreshTenantConfigs.mockResolvedValue(undefined);
    mockExecuteRaw.mockResolvedValue(3);
  }
  const res = await fetch(baseUrl + '/api/admin' + route.path, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify(route.body),
  });
  return { status: res.status, text: await res.text() };
}

describe('KS-1334 part A: refresh-tenants and backfill-certification-metadata never answer a 500 with err.message', () => {
  it.each(KS1334_ROUTES)('RED KS-1334 A1 $label: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it', async (route) => {
    for (const nodeEnv of KS1334_NODE_ENVS) {
      mockLoggerError.mockClear();
      const reply = await post1334(route, nodeEnv, true);
      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(KS1334_LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: KS1334_LEAK }]] });
    }
  });

  it.each(KS1334_ROUTES)('control KS-1334 A0 $label: a call that does not throw answers 200 and logs nothing', async (route) => {
    const reply = await post1334(route, 'production', false);
    expect({ status: reply.status, success: JSON.parse(reply.text).success }).toEqual({ status: 200, success: true });
    expect(mockLoggerError).not.toHaveBeenCalled();
  });

  it('control KS-1334 A2: KS1334_LEAK survives JSON encoding, so leaked: false above is not vacuous', () => {
    expect(JSON.stringify({ success: false, error: { message: KS1334_LEAK } }).includes(KS1334_LEAK)).toBe(true);
    expect(new Error(KS1334_LEAK).message).toBe(KS1334_LEAK);
  });
});

// KS-1334 part B: the last two UNCONDITIONAL sites (seed-demo-users, migrate-tenant-data) now go through
// fail500, so the KNOWN list in C4 is empty and C3 counts 50. Neither handler reaches its outer catch
// through the prisma mock the cells above use, so each is driven through the first call its try block
// makes outside any inner catch: seed-demo-users through the refusal warning of its demo-seed gate
// (the gate is closed here), migrate-tenant-data through the platform pool of its tenant manager.
const mockLoggerWarn = (jest.requireMock('../utils/logger') as { logger: { warn: jest.Mock } }).logger.warn;
const mockDb = jest.requireMock('../db') as { getTenantManager: () => unknown };
const KS1334B_ROUTES = [
  { label: 'POST /seed-demo-users', path: '/seed-demo-users', calmStatus: 403, context: 'Admin config request failed (POST /api/admin/seed-demo-users)' },
  { label: 'POST /migrate-tenant-data', path: '/migrate-tenant-data', calmStatus: 400, context: 'Admin config request failed (POST /api/admin/migrate-tenant-data)' },
] as const;

async function post1334b(route: (typeof KS1334B_ROUTES)[number], nodeEnv: string | undefined, throwIt: boolean): Promise<{ status: number; text: string }> {
  setNodeEnv(nodeEnv);
  delete process.env.ENABLE_DEMO_SEED;
  mockLoggerWarn.mockReset();
  mockDb.getTenantManager = () => null;
  if (throwIt && route.path === '/seed-demo-users') {
    mockLoggerWarn.mockImplementationOnce(() => { throw new Error(KS1334_LEAK); });
  }
  if (throwIt && route.path === '/migrate-tenant-data') {
    mockDb.getTenantManager = () => ({ getPlatformPool: () => { throw new Error(KS1334_LEAK); } });
  }
  const res = await fetch(baseUrl + '/api/admin' + route.path, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({}),
  });
  return { status: res.status, text: await res.text() };
}

describe('KS-1334 part B: seed-demo-users and migrate-tenant-data never answer a 500 with err.message', () => {
  it.each(KS1334B_ROUTES)('RED KS-1334 B1 $label: the thrown message is not in the 500 body under production or any other NODE_ENV, and fail500 logged it', async (route) => {
    for (const nodeEnv of KS1334_NODE_ENVS) {
      mockLoggerError.mockClear();
      const reply = await post1334b(route, nodeEnv, true);
      expect({ nodeEnv, status: reply.status, leaked: reply.text.includes(KS1334_LEAK) }).toEqual({ nodeEnv, status: 500, leaked: false });
      expect(JSON.parse(reply.text)).toEqual(CONSTANT_BODY);
      expect({ nodeEnv, calls: mockLoggerError.mock.calls }).toEqual({ nodeEnv, calls: [[route.context, { error: KS1334_LEAK }]] });
    }
  });

  it.each(KS1334B_ROUTES)('control KS-1334 B0 $label: with nothing thrown the route answers its own refusal and logs no error', async (route) => {
    const reply = await post1334b(route, 'production', false);
    expect({ status: reply.status, success: JSON.parse(reply.text).success }).toEqual({ status: route.calmStatus, success: false });
    expect(mockLoggerError).not.toHaveBeenCalled();
  });
});
