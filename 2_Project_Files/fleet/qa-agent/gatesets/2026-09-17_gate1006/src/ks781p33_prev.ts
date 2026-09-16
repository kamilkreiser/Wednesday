// =============================================================================
// KS-781 P3-3 CLASS GUARD — the control-byte guard must be mounted after EVERY
// body parser, in every service, or it inspects a body that is not there yet
// =============================================================================
//
// WHAT WENT WRONG, so the shape is on the record.
//
// `rejectControlBytes()` (KS-471 / KS-472) inspects `req.body`. Five services
// mounted it BETWEEN the two parsers:
//
//     app.use(express.json({ limit: '10mb' }));
//     app.use(rejectNulBytes());              <-- runs here
//     app.use(express.urlencoded({ extended: true }));
//
// On a form-encoded request `express.json()` sets `req.body = {}` and skips
// parsing, so the guard walked an empty object and passed. The form body was
// then parsed AFTER it. Measured on the real middleware at `de1206a63`: the
// identical NUL was `400 VALIDATION_ERROR` as JSON and `200` as a form, and on
// `/api/oauth/authorize` it reached the authorization-code minter. The guard
// was mounted, exported, imported by 22 call sites and green in its own tests —
// and could not work, because every one of those tests called the middleware
// directly with a fabricated `req`. A guard mounted where it cannot run looks
// exactly like a guard that runs, to a test that never mounts it.
//
// That is why LEG B below exists and is load-bearing.
//
// CORPUS — stated as exact sets, each asserted by a test that names its
// members, so a count here being wrong is a red rather than a stale comment.
//
//   LEG A — BEHAVIOURAL. A real Express app in the CORRECT order, driven over
//     a real socket, for `application/json` AND
//     `application/x-www-form-urlencoded`. Both must be refused identically.
//
//   LEG B — DISCRIMINATION CONTROL. The same probe against the PRE-FIX order.
//     The form request MUST get through. Without this leg, LEG A cannot tell
//     "the guard covers form bodies" from "this probe cannot see form bodies at
//     all" — the two are indistinguishable from a pair of green assertions.
//     If LEG B ever goes green-on-both, LEG A has stopped proving anything.
//
//   LEG C — STRUCTURAL, app-level parsers. Every entrypoint that mounts the
//     guard must mount it after every parser mounted THROUGH `app.use(...)` in
//     that file. Covers the 24 entrypoints today, including those that mount
//     only `express.json()` and would acquire the defect the day `urlencoded`
//     is added below the guard. The services mounting urlencoded are named as
//     an exact set (`SERVICES_WITH_URLENCODED`).
//
//   LEG D — STRUCTURAL, parsers reachable after the guard by another route. A
//     parser can also sit after the global guard by being passed as a route
//     handler (`app.post(path, parser, …)`) or handed to a router factory
//     (`app.use(createVerificationRoutes({ …, mockBodyParser, … }))`). Bodies
//     parsed that way are never seen by the global guard either. Declared as an
//     EXACT SET (`POST_GUARD_PARSER_SITES`) rather than left as prose, so it
//     cannot be forgotten and cannot grow silently.
//
//   ⚠ LEG C AND LEG D ARE POSITIONAL SINCE KS-800 item 3. Both used to ask
//     whether two regexes matched the same physical LINE, and two shapes went
//     straight through that with the suite green — an inline route parser
//     (F-01) and a multi-line `app.use(...)` (F-02), both confirmed by the gate
//     to put a NUL in front of a handler over a real socket. They now compare
//     the SOURCE POSITION of each parser's `CallExpression` against the
//     guard's, on the same AST LEG E/F use. See the block above `scan()`.
//
// ⚠ WHAT THIS FILE DOES NOT COVER — restated after KS-800 item 3, because two
//     of the three things this block used to claim are no longer true.
//     Router-module parsers ARE covered now, by LEG F, and two are declared
//     rather than unknown. What remains genuinely uncovered:
//       · Buffer bodies. `express.raw` sets `req.body` to a Buffer, which
//         `findNulBytePath` walks to null, so ORDERING a raw parser correctly
//         still inspects nothing (KS-802's own caveat, not closed here).
//         Detection is not protection.
//       · A parser reached through a value this file cannot follow — an import
//         from another module, a property on an object, a computed callee.
//         Symbol tracking here covers a parser bound to a local `const` in the
//         same file, and nothing wider.
//       · Directories outside the DECLARED roots. `services/` and
//         `connectors/` are walked (KS-800 F-15 closed `connectors/`, which
//         held an unguarded body-parsing express app). `frontend/`, `sdk/`,
//         `scripts/` and anything added later are NOT — measured today as
//         holding no express app, but that is a measurement with a date on it,
//         not a property. A new root is a new blind spot until it is added to
//         ENTRYPOINT_ROOTS.
// =============================================================================

import { describe, it, expect, beforeAll, afterAll } from 'vitest';
import ts from 'typescript';
import { readFileSync, existsSync, readdirSync } from 'node:fs';
import { join, resolve, relative } from 'node:path';
import { pathToFileURL } from 'node:url';
import type { Server } from 'node:http';
import type { AddressInfo } from 'node:net';
import { connect as netConnect } from 'node:net';
import express from 'express';
import { rejectNulBytes, mountBodyParsers } from '../middleware';
import {
  createsExpressApp,
  ENTRYPOINT_ROOTS,
  entrypoints as structuralEntrypoints,
} from './entrypoint-corpus';

/**
 * Locate the Dev root by walking up until `services/` and `packages/` are both
 * present. Same idiom as `ks727-errorhandler-class-guard.test.ts`, so the
 * structural guards root themselves identically however vitest is invoked.
 */
function findDevRoot(start: string): string {
  let dir = start;
  for (let i = 0; i < 10; i++) {
    if (existsSync(join(dir, 'services')) && existsSync(join(dir, 'packages'))) return dir;
    const parent = resolve(dir, '..');
    if (parent === dir) break;
    dir = parent;
  }
  throw new Error(`[ks781 p3-3 guard] could not locate the Dev root from ${start}`);
}

const DEV_ROOT = findDevRoot(process.cwd());

/** The exact set of service entrypoints that mount `express.urlencoded`. */
const SERVICES_WITH_URLENCODED = [
  'services/api-gateway/src/index.ts',
  'services/auth/src/index.ts',
  'services/nft-certificate/src/app.ts',
  'services/originate/src/index.ts',
  'services/referral/src/index.ts',
  'services/staking/src/index.ts',
  'services/vc-issuer/src/index.ts',
];

/**
 * LEG D's exact set: parsers reachable AFTER the global guard because they are
 * passed as a handler rather than mounted. All three are in the api-gateway,
 * at lines 816, 829 and 862.
 *
 * 816 and 829 sit behind `ENABLE_MOCK_ENDPOINTS`. 862 hands `mockBodyParser` to
 * `createVerificationRoutes`, which is explicitly NOT mock-gated by its own
 * comment, so it is live wherever the gateway runs.
 *
 * ⚠ KS-800 F-14 CALLED 862 A DEAD ARGUMENT AND IT IS NOT — re-derived at this
 * head before acting on it. F-14 reads: "`api-gateway/src/index.ts:862` hands
 * `mockBodyParser` to `createAdminRoutes({…})`, which does not destructure it …
 * it inflates a declared exclusion set by one entry that exposes nothing."
 * Measured here: 862 is inside `createVerificationRoutes`, not
 * `createAdminRoutes` (which never receives it — `admin.ts` declares its OWN
 * parser at :535); `verification.ts:305` destructures `mockBodyParser` and
 * hands it to **6 routes**, including `/api/documents/:id/verify` and
 * `/api/certifications/:id/verify`. So 862 is not dead and is the most exposed
 * of the three. Pruning it as F-14 suggests would have removed the LIVE entry.
 * Tracked on the KS-781 P3-3 class ticket.
 */
const POST_GUARD_PARSER_SITES: Record<string, number> = {
  'services/api-gateway/src/index.ts': 3,
};

/** U+0000 — the byte KS-471 exists to stop. Written as an escape, never literal. */
const NUL = '\u0000';
/** BEL (0x07) — a non-NUL member of the KS-472 disallowed class. */
const BEL = '\u0007';

// ---------------------------------------------------------------------------
// Harness — a real app, a real socket, real content types.
// ---------------------------------------------------------------------------

type Order = 'fixed' | 'pre-fix';

function buildApp(order: Order) {
  const app = express();
  if (order === 'fixed') {
    app.use(express.json({ limit: '1mb' }));
    app.use(express.urlencoded({ extended: true }));
    app.use(rejectNulBytes());
  } else {
    app.use(express.json({ limit: '1mb' }));
    app.use(rejectNulBytes());
    app.use(express.urlencoded({ extended: true }));
  }
  app.post('/probe', (req, res) => {
    res.status(200).json({ reached: true, body: req.body });
  });
  return app;
}

async function listen(app: express.Express): Promise<{ base: string; server: Server }> {
  const server = app.listen(0, '127.0.0.1');
  await new Promise<void>((r) => server.once('listening', () => r()));
  const { port } = server.address() as AddressInfo;
  return { base: `http://127.0.0.1:${port}`, server };
}

async function close(server: Server) {
  await new Promise<void>((r) => server.close(() => r()));
}

async function postJson(base: string, value: string) {
  const res = await fetch(`${base}/probe`, {
    method: 'POST',
    headers: { 'content-type': 'application/json' },
    body: JSON.stringify({ state: value }),
  });
  return { status: res.status, body: (await res.json().catch(() => null)) as any };
}

async function postForm(base: string, value: string) {
  const res = await fetch(`${base}/probe`, {
    method: 'POST',
    headers: { 'content-type': 'application/x-www-form-urlencoded' },
    body: new URLSearchParams({ state: value }).toString(),
  });
  return { status: res.status, body: (await res.json().catch(() => null)) as any };
}

// ---------------------------------------------------------------------------
// LEG A — behavioural, the fixed order
// ---------------------------------------------------------------------------

describe('KS-781 P3-3 LEG A — the guard covers BOTH content types in the fixed order', () => {
  let base: string;
  let server: Server;
  beforeAll(async () => {
    ({ base, server } = await listen(buildApp('fixed')));
  });
  afterAll(async () => {
    await close(server);
  });

  it('refuses a NUL in a JSON body', async () => {
    const r = await postJson(base, `ab${NUL}cd`);
    expect(r.status).toBe(400);
    expect(r.body?.error?.code).toBe('VALIDATION_ERROR');
  });

  it('refuses the SAME NUL in a form-encoded body — the case that was a 200', async () => {
    const r = await postForm(base, `ab${NUL}cd`);
    expect(r.status).toBe(400);
    expect(r.body?.error?.code).toBe('VALIDATION_ERROR');
  });

  it('refuses a non-NUL disallowed control byte (BEL) in a form body too', async () => {
    const r = await postForm(base, `ab${BEL}cd`);
    expect(r.status).toBe(400);
  });

  it('still lets a clean form body through — the guard is not refusing everything', async () => {
    const r = await postForm(base, 'abcd');
    expect(r.status).toBe(200);
    expect(r.body?.body?.state).toBe('abcd');
  });

  it('agrees across content types: identical value, identical status', async () => {
    const value = `x${NUL}y`;
    const j = await postJson(base, value);
    const f = await postForm(base, value);
    expect(f.status).toBe(j.status);
  });
});

// ---------------------------------------------------------------------------
// LEG B — the discrimination control. This is what makes LEG A mean something.
// ---------------------------------------------------------------------------

describe('KS-781 P3-3 LEG B — the pre-fix order MUST let the form NUL through', () => {
  let base: string;
  let server: Server;
  beforeAll(async () => {
    ({ base, server } = await listen(buildApp('pre-fix')));
  });
  afterAll(async () => {
    await close(server);
  });

  it('still refuses the JSON NUL — the pre-fix order was never broken for JSON', async () => {
    const r = await postJson(base, `ab${NUL}cd`);
    expect(r.status).toBe(400);
  });

  it('LETS THE FORM NUL THROUGH — if this ever goes 400, LEG A proves nothing', async () => {
    const r = await postForm(base, `ab${NUL}cd`);
    expect(r.status).toBe(200);
    expect(r.body?.body?.state).toContain(NUL);
  });
});

// ---------------------------------------------------------------------------
// LEG C + D — structural, across every service entrypoint
// ---------------------------------------------------------------------------

/**
 * Every service entrypoint that exists, across the three names a service may
 * use.
 *
 * ⚠ THIS LIST WAS `index.ts` ALONE AND THAT WAS WRONG. Two services mount the
 * guard somewhere else — `nft-certificate/src/app.ts` and
 * `wallet-connector/src/server.ts` — so an index-only walk reported 20 mounts
 * where KS-573 counts 23, and both of those services were invisible to every
 * assertion below. A corpus inherits the blind spot of whatever found its
 * members; this one found them with a grep over `index.ts`. Same three names
 * as `ks727-errorhandler-class-guard.test.ts`, for the same reason.
 */

/**
 * KS-800: an entrypoint is a file that CREATES THE EXPRESS APP, not a file with
 * a blessed name.
 *
 * A name list (`index.ts`, `app.ts`, `server.ts`) is NOT the corpus.
 *
 * KS-833 Q-1 corrects what this paragraph used to say. It claimed "the array
 * that held it was deleted in KS-818 G-08" — false of the file it pointed at.
 * G-08 deleted the DEAD copy (here) and left the LIVE one in
 * `ks727-errorhandler-class-guard.test.ts:339`, where it was that suite's
 * corpus. So the list this comment declared dead was still choosing which files
 * ks727 could see, and it could not see `mcp-server/src/http-server.ts` — the
 * very file named below as the miss that motivated the deletion.
 *
 * Both suites now derive the corpus from `./entrypoint-corpus`, so there is no
 * second copy left to drift. A name list is the very defect this ticket exists
 * to close: the list went `index.ts` -> `{index,app,server}.ts` after missing
 * two services, and it STILL missed `mcp-server/src/http-server.ts`. A third
 * literal would have been the third instance of the same mistake.
 *
 * Asking the AST "does this file call `express()`?" cannot miss a filename
 * nobody thought of. Measured: the name list finds 22 files, this finds 24 —
 * the two extra are `mcp-server/src/http-server.ts` and, once it gained a
 * guard, `demo-service/src/app.ts`.
 */

/**
 * KS-800 item 5 (F-15) — THE WALK IS NO LONGER `services/` ONLY.
 *
 * The corpus went `index.ts` -> `{index,app,server}.ts` -> "a file that calls
 * `express()`", and each widening fixed the instrument while leaving the
 * DIRECTORY assumed. `connectors/whatsapp-bot/src/index.ts` creates an express
 * app, mounts `express.json()`, and took `POST /webhook` from Meta's Cloud API
 * with no control-byte guard at all — outside the walk by construction, so it
 * was invisible rather than failing, the same shape as `demo-service` and
 * `mcp-server` before item 2.
 *
 * Applying the structural predicate to the whole repo finds **25** entrypoints:
 * the 24 under `services/` plus that one connector, and NOTHING spurious — no
 * script, no fixture, no test helper. So there is no declared exclusion set,
 * because nothing needed excluding. If a future root drags in something that is
 * genuinely not a deployable app, exclude it HERE by name with a reason line
 * each — never by narrowing the roots again, which is the mistake this walk has
 * now made twice.
 */

/**
 * KS-802 (re-gate (4) Q4-7): widened from `json|urlencoded`.
 *
 * `express.raw` and `express.text` set `req.body` just as the other two do, and
 * `body-parser` may be used directly. A service mounting one of those AFTER the
 * guard was invisible to LEG C — the guard would be "correctly ordered" with
 * respect to parsers this regex happened to know about.
 *
 * ⚠ DETECTION IS NOT PROTECTION, and the difference matters here. A raw parser
 * sets `req.body` to a **Buffer**. `findNulBytePath` walks it via
 * `Object.entries`, which yields numeric indices with NUMBER values — no
 * branch matches, so it returns null for every Buffer. Ordering a raw parser
 * before the guard therefore buys nothing; widening this regex tells you WHERE
 * raw bodies are, not that they are checked. Measured on this tree: the only
 * real `express.raw` is `billing/src/index.ts:50`, path-scoped to `/webhooks`
 * and mounted before the guard, so LEG C does not flag it — correctly, and
 * also uselessly. Buffer-body inspection is not in KS-802's scope; it needs
 * its own decision about whether a webhook payload should be scanned at all.
 */
/**
 * KS-800 F-03 + F-16 — THE NAMES, DECLARED ONCE.
 *
 * Two shared-exported ways to mount a body parser were invisible to every leg,
 * and one of them is the helper THIS branch introduces:
 *
 *   F-03  `mountBodyParsers(app)` mounts express.json, optionally
 *         express.urlencoded, and then the guard LAST. A service adopting it
 *         has no literal `express.json(` and no `app.use(rejectNulBytes()`, so
 *         `scan()` returned null and the service dropped out of LEG C, LEG E
 *         and LEG F at once. Measured by the gate: adopting it took LEG C from
 *         24 to 23, and the only signal was `expected 23 to be 24` — which
 *         invites the maintainer to edit the 24 down and erase the service
 *         from the corpus. With the count "fixed" the suite went 46/46 GREEN
 *         with a service invisible to all three predicates.
 *
 *   F-16  `packages/shared/src/middleware/request-limits.ts` exports six more
 *         parser factories. `app.use(...standardBodyParsers())` produces no
 *         `express.json(` either. Latent today (no service uses them), which is
 *         exactly when it is cheap to close.
 *
 * Declared here as name SETS because this file recognises the same facts twice
 * — once by regex for LEG C/D and once through the TypeScript AST for LEG E/F.
 * Two encodings of one list drift; one list feeding both cannot.
 */
const PARSER_FACTORY_NAMES = [
  'jsonParser',
  'urlencodedParser',
  'rawParser',
  'textParser',
  'standardBodyParsers',
  'largeBodyParsers',
  'webhookBodyParsers',
  'minimalBodyParsers',
] as const;

/**
 * Mounts parsers AND the guard, guard last, in one call. It is therefore both a
 * parser mount and a guard mount at the SAME line — which is why the ordering
 * assertion (`parserMountLines.filter(n => n > guardLine)`) passes for it
 * without a special case: a parser at the guard's own line is not after it.
 */
const COMBINED_MOUNT_NAME = 'mountBodyParsers';

/**
 * KS-800 item 3 (F-01 / F-02) — THE ORDERING LEG IS NOW POSITIONAL, NOT TEXTUAL.
 *
 * Everything below this comment used to be four regexes:
 *
 *     PARSER_CALL   /express\.(json|urlencoded|raw|text)…\(/
 *     GUARD_MOUNT   /app\.use\(\s*rejectNulBytes\(\)/
 *     APP_MOUNT     /app\.use\(/
 *     PARSER_ASSIGN /(?:const|let|var)\s+(\w+)\s*=\s*express\.json\s*\(/
 *
 * and `scan()` asked whether APP_MOUNT and PARSER_CALL matched THE SAME
 * PHYSICAL LINE. Two shapes walked straight through that, both measured green
 * on 66/66 before this change and both confirmed to put a NUL in front of a
 * handler by the gate's real-socket probe:
 *
 *   F-01  `app.post('/x', express.json(), h)` — an inline parser handed to a
 *         route INSIDE an entrypoint. `APP_MOUNT` is `app.use(`, which never
 *         matches `app.post(`; LEG D's symbol trace needed a
 *         `const p = express.json()` binding, which an inline call has not;
 *         and LEG F skips any file that creates the app. Unseen by every leg.
 *
 *   F-02  `app.use(\n  express.json({ limit: '10mb' }),\n);` — the SAME mount
 *         a formatter would produce. `APP_MOUNT` matches the first line,
 *         `PARSER_CALL` the second, never one line, so nothing was recorded.
 *         This one needs no new code at all: reflowing a currently-correct
 *         mount is enough to blind the leg, silently, with a green suite.
 *
 * The method note on the gate report is the real instruction, and it is why
 * this is not a fifth regex: across KS-781 → KS-800 each fix replaced one cheap
 * predicate with a slightly better cheap predicate while `scan()` stayed
 * line-oriented. The next literal would not have closed it either.
 *
 * So ordering is now decided by SOURCE POSITION — the character offset of the
 * parser's own `CallExpression` against the guard's — read off the same
 * TypeScript AST that LEG E and LEG F already use. A position is exact where a
 * line is an approximation: it orders two calls on one line correctly, it is
 * unmoved by reflowing one call across three lines, and a comment cannot
 * produce one.
 *
 * ⚠ KS-802's WIDENING IS SUPERSEDED, AND ITS INTENT IS CARRIED. #818 widened
 * `PARSER_CALL` from `json|urlencoded` to include `raw`, `text` and
 * `bodyParser.*` — a regex over a line, and this file no longer has one. The
 * fact it encoded (those ARE parsers, they DO set `req.body`) now lives in
 * `PARSER_MODULES` × `PARSER_METHODS` below, which every leg reads. Measured
 * on this tree: carrying the widening changes NOTHING today — 24 services with
 * a parser either way, the same two router-module sites — so it is latent
 * detection, which is exactly when it is cheap. KS-802's own caveat still
 * stands and is still not closed by this: `express.raw` sets `req.body` to a
 * Buffer, which `findNulBytePath` walks to `null`, so ordering a raw parser
 * before the guard buys nothing. Detection is not protection.
 *
 * ONE ENCODING, NOT TWO. This file used to recognise the same facts twice —
 * by regex for LEG C/D, by AST for LEG E/F — and carried a test that the two
 * agreed, because two encodings of one list drift. There is now one encoding.
 * The drift risk is not managed; it is gone.
 */

/** Methods on the parser modules that set `req.body`. KS-802 added `raw` and `text`. */
const PARSER_METHODS = ['json', 'urlencoded', 'raw', 'text'] as const;
/** The guard's real exported names. `mountBodyParsers` mounts it last, internally. */
const CANONICAL_GUARD_NAMES = [
  'rejectNulBytes',
  'rejectControlBytes',
  COMBINED_MOUNT_NAME,
] as const;

/**
 * KS-800 item 4 (F-04) — RESOLVE THE IMPORT BINDING, DO NOT MATCH THE SPELLING.
 *
 * Every predicate in this file used to compare `Identifier.text` against the
 * literal string `'express'`. The AST was chosen to escape a cheap textual
 * extractor, and this was a cheap textual extractor in AST clothing. The gate
 * proved it with a paired probe on a new service that parses JSON and form
 * bodies, mounts no guard and persists `req.body`:
 *
 *     import express    from 'express'   -> 1 failure, LEG E names it
 *     import expressLib from 'express'   -> 47/47, FULLY GREEN
 *
 * A whole unguarded service disappears on a rename of the import.
 *
 * So the local binding is resolved per file. Measured on this tree: all 61
 * express imports under `services/` are a plain default `import express from
 * 'express'`, none renamed, no `require`, and `body-parser` is not imported at
 * all — so this is latent today, exactly like F-16, and latent is when it is
 * cheap.
 *
 * FALLBACK, stated because it is load-bearing: a file with NO express import
 * falls back to the literal names. Synthetic sources in this file's own leg
 * tests are written without imports, and a service file always has the import,
 * so resolution governs wherever it matters.
 */
interface ModuleBindings {
  /** Local names bound to the express module itself. */
  express: Set<string>;
  /** Local names bound to the body-parser module. */
  bodyParser: Set<string>;
  /** Local name -> canonical parser, for `import { json } from 'express'`. */
  direct: Map<string, string>;
  /**
   * Local name -> canonical guard, for
   * `import { rejectNulBytes as nulGuard } from '@secuura/shared'`.
   *
   * KS-800 F-10: without this the guard is unrecognised under an alias and LEG E
   * reports the service *"mounts NO control-byte guard anywhere in src/"* while
   * the guard is mounted and working. Fail-safe direction, wrong diagnosis — and
   * a wrong diagnosis on a red is what gets a guard switched off by someone
   * who checks and sees it right there.
   */
  guards: Map<string, string>;
}

const PARSER_MODULES: Record<string, string> = { express: 'express', 'body-parser': 'bodyParser' };

function moduleBindings(sf: ts.SourceFile): ModuleBindings {
  const out: ModuleBindings = {
    express: new Set(),
    bodyParser: new Set(),
    direct: new Map(),
    guards: new Map(),
  };
  let sawSharedImport = false;
  const bindNamed = (mod: string, local: string, imported: string): void => {
    if ((PARSER_METHODS as readonly string[]).includes(imported)) {
      out.direct.set(local, `${mod}.${imported}`);
    }
  };
  const visit = (n: ts.Node): void => {
    // import { rejectNulBytes as nulGuard } from '@secuura/shared' (F-10)
    if (
      ts.isImportDeclaration(n) &&
      ts.isStringLiteral(n.moduleSpecifier) &&
      n.moduleSpecifier.text.startsWith('@secuura/shared') &&
      n.importClause?.namedBindings &&
      ts.isNamedImports(n.importClause.namedBindings)
    ) {
      sawSharedImport = true;
      for (const el of n.importClause.namedBindings.elements) {
        const imported = (el.propertyName ?? el.name).text;
        if ((CANONICAL_GUARD_NAMES as readonly string[]).includes(imported)) {
          out.guards.set(el.name.text, imported);
        }
      }
    }
    // import ... from 'express' | 'body-parser'
    if (ts.isImportDeclaration(n) && ts.isStringLiteral(n.moduleSpecifier)) {
      const mod = PARSER_MODULES[n.moduleSpecifier.text];
      if (mod) {
        const c = n.importClause;
        if (c?.name) (mod === 'express' ? out.express : out.bodyParser).add(c.name.text);
        if (c?.namedBindings) {
          if (ts.isNamespaceImport(c.namedBindings)) {
            (mod === 'express' ? out.express : out.bodyParser).add(c.namedBindings.name.text);
          } else {
            for (const el of c.namedBindings.elements) {
              bindNamed(mod, el.name.text, (el.propertyName ?? el.name).text);
            }
          }
        }
      }
    }
    // const x = require('express') | const { json } = require('express')
    if (
      ts.isVariableDeclaration(n) &&
      n.initializer &&
      ts.isCallExpression(n.initializer) &&
      ts.isIdentifier(n.initializer.expression) &&
      n.initializer.expression.text === 'require' &&
      n.initializer.arguments.length === 1 &&
      ts.isStringLiteral(n.initializer.arguments[0])
    ) {
      const mod = PARSER_MODULES[(n.initializer.arguments[0] as ts.StringLiteral).text];
      if (mod) {
        if (ts.isIdentifier(n.name)) {
          (mod === 'express' ? out.express : out.bodyParser).add(n.name.text);
        } else if (ts.isObjectBindingPattern(n.name)) {
          for (const el of n.name.elements) {
            if (ts.isIdentifier(el.name)) {
              const imported = el.propertyName && ts.isIdentifier(el.propertyName)
                ? el.propertyName.text
                : el.name.text;
              bindNamed(mod, el.name.text, imported);
            }
          }
        }
      }
    }
    ts.forEachChild(n, visit);
  };
  visit(sf);
  // A file that imports neither falls back to the conventional spellings, so
  // synthetic sources without imports still read correctly.
  if (out.express.size === 0 && out.direct.size === 0) out.express.add('express');
  if (out.bodyParser.size === 0 && out.direct.size === 0) out.bodyParser.add('bodyParser');
  // Same fallback rule for guards: a file that imports nothing from the shared
  // package is read by the conventional spellings.
  if (!sawSharedImport) for (const g of CANONICAL_GUARD_NAMES) out.guards.set(g, g);
  return out;
}

/** The parser this call is, or null. One predicate, read by every leg in this file. */
function parserCallName(n: ts.Node, b: ModuleBindings): string | null {
  if (!ts.isCallExpression(n)) return null;
  const e = n.expression;
  if (
    ts.isPropertyAccessExpression(e) &&
    ts.isIdentifier(e.expression) &&
    (PARSER_METHODS as readonly string[]).includes(e.name.text)
  ) {
    // Canonical name, not the local spelling: `expressLib.json()` reports as
    // `express.json` so declared sets and messages stay stable under a rename.
    if (b.express.has(e.expression.text)) return `express.${e.name.text}`;
    if (b.bodyParser.has(e.expression.text)) return `bodyParser.${e.name.text}`;
  }
  if (ts.isIdentifier(e)) {
    const direct = b.direct.get(e.text);
    if (direct) return direct;
    if ((PARSER_FACTORY_NAMES as readonly string[]).includes(e.text) || e.text === COMBINED_MOUNT_NAME) {
      return e.text;
    }
  }
  return null;
}

/**
 * KS-833 Q-3 — the MODULE-REACH half of {@link parserCallName}, with the
 * name-list branch removed.
 *
 * `parserCallName` returns non-null for any identifier in
 * `PARSER_FACTORY_NAMES`. That is right for the mount legs — a call to
 * `jsonParser()` really is a parser mount — but it is WRONG as the base case of
 * the G-05 derivation, which exists to check that list against the module. Used
 * there, the list validates itself: the predicate becomes structure UNION the
 * list, so two exported functions that only delegate to each other and never
 * reach `express.*` are still "detected", and a factory that quietly stopped
 * producing a parser stays green forever.
 *
 * It also means the presets qualify on PASS 1 by the name branch, not "on the
 * second pass" as the G-05 header used to claim — the fixed point was never
 * exercised by the real module.
 */
function moduleParserReach(n: ts.Node, b: ModuleBindings): string | null {
  if (!ts.isCallExpression(n)) return null;
  const e = n.expression;
  if (
    ts.isPropertyAccessExpression(e) &&
    ts.isIdentifier(e.expression) &&
    (PARSER_METHODS as readonly string[]).includes(e.name.text)
  ) {
    if (b.express.has(e.expression.text)) return `express.${e.name.text}`;
    if (b.bodyParser.has(e.expression.text)) return `bodyParser.${e.name.text}`;
  }
  if (ts.isIdentifier(e)) return b.direct.get(e.text) ?? null;
  return null;
}

/** The guard this call is (canonical name), or null. Alias-aware — KS-800 F-10. */
function guardCallName(n: ts.Node, b: ModuleBindings): string | null {
  if (!ts.isCallExpression(n) || !ts.isIdentifier(n.expression)) return null;
  return b.guards.get(n.expression.text) ?? null;
}

/**
 * A parser reachable in a file, with the position that decides its ordering.
 *
 * `app-level`  — handed to `app.use(...)`, so it runs for every request. LEG C
 *                owns these: one after the guard is a hard failure.
 * `reachable`  — everything else: passed to a route (`app.post(p, parser, h)`)
 *                or handed to a router factory (`createVerificationRoutes(…,
 *                mockBodyParser, …)`). The global guard never sees these
 *                bodies either. LEG D owns them as a declared, bounded set.
 */
interface ParserSite {
  pos: number;
  line: number;
  kind: 'app-level' | 'reachable';
  via: string;
}

interface Scan {
  rel: string;
  guardPos: number;
  guardLine: number;
  lateAppLevel: ParserSite[];
  postGuardParserSites: ParserSite[];
  urlencodedMounted: boolean;
}

/**
 * Read one entrypoint positionally.
 *
 * The app is found rather than assumed: whatever identifier `express()` is
 * bound to is the app, so a file naming it `server` is read correctly instead
 * of silently producing nothing. A parser bound to a symbol
 * (`const mockBodyParser = express.json()`) is counted at each REFERENCE, never
 * at its declaration — a declaration parses no bodies; its uses do. Getting
 * that wrong reads api-gateway as 5 sites where it has 3.
 */
function analyseSource(source: string, fileName: string, rel: string): Scan | null {
  const sf = ts.createSourceFile(fileName, source, ts.ScriptTarget.Latest, true);
  const lineOf = (pos: number): number => sf.getLineAndCharacterOfPosition(pos).line + 1;
  // KS-800 F-04 — resolved once per file, read by every predicate below.
  const bindings = moduleBindings(sf);

  // Pass 1 — what is the app called, and which symbols hold a parser?
  const appNames = new Set<string>();
  const parserSymbols = new Map<string, string>();
  const declaredNamePos = new Set<number>();
  const initializerPos = new Set<number>();
  const visitDecls = (n: ts.Node): void => {
    if (ts.isVariableDeclaration(n) && ts.isIdentifier(n.name) && n.initializer) {
      const init = n.initializer;
      if (
        ts.isCallExpression(init) &&
        ts.isIdentifier(init.expression) &&
        bindings.express.has(init.expression.text) &&
        init.arguments.length === 0
      ) {
        appNames.add(n.name.text);
      }
      const parser = parserCallName(init, bindings);
      if (parser) {
        parserSymbols.set(n.name.text, parser);
        declaredNamePos.add(n.name.getStart(sf));
        initializerPos.add(init.getStart(sf));
      }
    }
    ts.forEachChild(n, visitDecls);
  };
  visitDecls(sf);
  if (appNames.size === 0) appNames.add('app');

  // Pass 2 — the SPANS of every `app.use(...)` argument, and where the guard is.
  //
  // Spans, not argument positions. api-gateway mounts its parsers inside a
  // wrapper closure — `app.use((req, res, next) => { if (…) express.json({…})
  // (req, res, next); else next(); })` — so the parser is nowhere near being a
  // direct argument. Reading direct arguments only classified it as merely
  // "reachable" and lost `express.urlencoded` from the declared set entirely,
  // which is how this was caught: SERVICES_WITH_URLENCODED went 7 -> 6 and the
  // leg failed. Anything mounted THROUGH `app.use` runs for every request, so
  // anything lexically inside one of its arguments is app-level.
  const guardPositions: number[] = [];
  const combinedCalls: ts.CallExpression[] = [];
  const visitMounts = (n: ts.Node): void => {
    if (
      ts.isCallExpression(n) &&
      ts.isPropertyAccessExpression(n.expression) &&
      ts.isIdentifier(n.expression.expression) &&
      appNames.has(n.expression.expression.text) &&
      n.expression.name.text === 'use'
    ) {
      // arguments are classified by `classify()` below, from the parser's side
    }
    // `mountBodyParsers(app)` is a bare call, not an `app.use` argument. It is
    // BOTH a parser mount and a guard mount, at one position — which is why the
    // ordering test needs no special case for it: a parser at the guard's own
    // position is not after it.
    if (ts.isCallExpression(n) && ts.isIdentifier(n.expression) && n.expression.text === COMBINED_MOUNT_NAME) {
      combinedCalls.push(n);
    }
    ts.forEachChild(n, visitMounts);
  };
  visitMounts(sf);

  /**
   * app-level, or merely reachable?
   *
   * Walk up from the site to whatever mounts it. Two shapes look alike in a
   * span test and are NOT alike, both live in api-gateway:
   *
   *   app.use((req, res, next) => { … express.urlencoded({…})(req, res, next) … })
   *       the parser IS the mounted middleware, invoked per request  -> app-level
   *
   *   app.use(createVerificationRoutes({ …, mockBodyParser, … }))
   *       the parser is DATA handed to a factory, which makes it a route
   *       handler inside the router it builds                        -> reachable
   *
   * So: crossing into another call's ARGUMENTS on the way up means the parser
   * was passed along rather than mounted. A span test cannot see the
   * difference — it read the second as app-level and moved the one live,
   * non-mock-gated site out of LEG D, which the CONTROL below caught.
   */
  const isAppUseCall = (c: ts.CallExpression): boolean =>
    ts.isPropertyAccessExpression(c.expression) &&
    ts.isIdentifier(c.expression.expression) &&
    appNames.has(c.expression.expression.text) &&
    c.expression.name.text === 'use';

  const encloses = (outer: ts.Node, inner: ts.Node): boolean =>
    inner.getStart(sf) >= outer.getStart(sf) && inner.getEnd() <= outer.getEnd();

  const classify = (node: ts.Node): 'app-level' | 'reachable' => {
    let prev: ts.Node = node;
    let cur: ts.Node | undefined = node.parent;
    while (cur) {
      if (ts.isCallExpression(cur) && cur.arguments.some((a) => encloses(a, prev))) {
        return isAppUseCall(cur) ? 'app-level' : 'reachable';
      }
      prev = cur;
      cur = cur.parent;
    }
    return 'reachable';
  };

  // A guard call counts as MOUNTED when it is mounted through `app.use(...)`
  // (F-09's distinction: mounted on the app, not merely mentioned in src/).
  //
  // KS-827 — the rest of the guard positions are derived AFTER the helper
  // machinery below, because a guard mounted or invoked by a local helper
  // belongs to the CALL and not to the declaration. Deriving `guardPos` here
  // would read a position the guard never runs at. Only the combined-helper
  // calls, which are already call sites, can be collected this early.
  for (const c of combinedCalls) guardPositions.push(c.getStart(sf));

  const combinedPos = new Set(combinedCalls.map((c) => c.getStart(sf)));
  // The helper mounts urlencoded unless it is switched off explicitly, so read
  // the option off the AST rather than assuming either way.
  const combinedMountsUrlencoded = combinedCalls.some((c) => {
    const opts = c.arguments[1];
    if (opts === undefined || !ts.isObjectLiteralExpression(opts)) return true;
    return !opts.properties.some(
      (pr) =>
        ts.isPropertyAssignment(pr) &&
        ts.isIdentifier(pr.name) &&
        pr.name.text === 'urlencoded' &&
        pr.initializer.kind === ts.SyntaxKind.FalseKeyword,
    );
  });

  // -------------------------------------------------------------------
  // KS-816 — A LOCAL FUNCTION THAT MOUNTS A PARSER IS A PARSER MOUNT, AND
  // THE POSITION THAT COUNTS IS WHERE IT IS CALLED.
  //
  // Item 3 put LEG C/D on source positions, which closed every shape where the
  // parser sits where it runs. It does not follow a call INTO a local
  // function. So `function mountMine(app) { app.use(express.json()); }`
  // declared above the guard and called below it read CLEAN on all eight legs
  // — predicted 0 failures, measured 107/107 green, with the NUL reaching the
  // handler over a real socket.
  //
  // A declaration mounts nothing; its CALLS do. That is the same reasoning
  // that already counts a parser bound to a symbol at its references rather
  // than at its declaration — this applies it one level up.
  //
  // Resolved to a FIXED POINT rather than one hop, so a helper calling a
  // helper does not simply move the blind spot to depth 2.
  //
  // ⚠ BOUNDED, and the bound is deliberate: this attributes PARSERS. The
  // mirror shape on the guard side — a GUARD mounted inside a helper, so
  // `guardPos` reads the declaration rather than the call — is NOT closed
  // here. It is recorded rather than widened into this round.
  // -------------------------------------------------------------------
  const paramNames = (fn: ts.SignatureDeclarationBase): Set<string> => {
    const out = new Set<string>();
    for (const prm of fn.parameters) if (ts.isIdentifier(prm.name)) out.add(prm.name.text);
    return out;
  };
  // F-QA-B needs the parameter POSITION, not just the name, to read what a call
  // site actually passes into the parameter a guard is mounted on.
  const paramList = (fn: ts.SignatureDeclarationBase): string[] =>
    fn.parameters.map((prm) => (ts.isIdentifier(prm.name) ? prm.name.text : '\u0000'));

  interface Helper { body: ts.Node; params: Set<string>; order: string[]; }
  const helpers = new Map<string, Helper>();
  const collectHelpers = (n: ts.Node): void => {
    if (ts.isFunctionDeclaration(n) && n.name && n.body) {
      helpers.set(n.name.text, { body: n.body, params: paramNames(n), order: paramList(n) });
    }
    if (
      ts.isVariableDeclaration(n) &&
      ts.isIdentifier(n.name) &&
      n.initializer &&
      (ts.isArrowFunction(n.initializer) || ts.isFunctionExpression(n.initializer))
    ) {
      helpers.set(n.name.text, {
        body: n.initializer.body,
        params: paramNames(n.initializer),
        order: paramList(n.initializer),
      });
    }
    ts.forEachChild(n, collectHelpers);
  };
  collectHelpers(sf);

  // `mountedOnApp` lived here and is GONE — superseded by `mountReceiver` +
  // `parserTarget`, which answer the same question without collapsing "the
  // file's app" and "any parameter" into one boolean (F-QA-05/F-QA-B). It is
  // removed rather than left dead because this ticket's own residue section
  // records that ADDING DEAD CODE to this file converts a loud red into a
  // silent clean — a dead predicate in a security instrument is not inert.
  // Recoverable in full at `f4ac95fe2`.

  /**
   * F-QA-03 — is this parser site in a MOUNTING position at all?
   *
   * `parserViaAt` answers "is there a parser here", not "is one mounted here".
   * A helper that merely DECLARES one (`const p = express.json()`) or MENTIONS
   * the symbol (`return { mock }`) mounted nothing, and was being credited with
   * a site — measured, `const p = express.json(); return p;` produced TWO,
   * one for the call and one for the reference.
   *
   * Everything that actually mounts a parser is an ARGUMENT to something:
   * `app.use(express.json())`, `app.post('/x', parser, h)`, a wrapper closure
   * handed to `app.use`. A declaration and a bare mention are arguments to
   * nothing. That is the same walk `classify` already does — this asks only
   * whether it terminates in a call, rather than which kind.
   *
   * Bounded to the HELPER machinery, which is where F-QA-03 was filed. The
   * file-level pass keeps counting a symbol at each reference, as documented.
   */
  const inMountingPosition = (node: ts.Node): boolean => {
    let prev: ts.Node = node;
    let cur: ts.Node | undefined = node.parent;
    while (cur) {
      if (ts.isCallExpression(cur) && cur.arguments.some((a) => encloses(a, prev))) return true;
      prev = cur;
      cur = cur.parent;
    }
    return false;
  };

  /** Sentinel target: the file's own app, reached by closure rather than an argument. */
  const APP_TARGET = '<app>';

  /** The identifier a `X.use(...)` mount hangs off, for a node inside its arguments. */
  const mountReceiver = (node: ts.Node): string | null => {
    let prev: ts.Node = node;
    let cur: ts.Node | undefined = node.parent;
    while (cur) {
      if (ts.isCallExpression(cur) && cur.arguments.some((a) => encloses(a, prev))) {
        return ts.isPropertyAccessExpression(cur.expression) &&
          ts.isIdentifier(cur.expression.expression) &&
          cur.expression.name.text === 'use'
          ? cur.expression.expression.text
          : null;
      }
      prev = cur;
      cur = cur.parent;
    }
    return null;
  };

  /**
   * F-QA-05 — WHAT a parser is mounted on: the file's app, one of this
   * helper's parameters, or nothing app-like at all.
   *
   * The guard side learned this in F-QA-B; the parser side had the same hole,
   * one list over. `mountedOnApp` accepted ANY parameter as the app, so a
   * ROUTER parser mounted through a helper was reported APP-LEVEL — measured,
   * `mountParser(r)` on a router read app-level=1 where the correct answer is
   * a route-scoped site. Wrong list, wrong leg, and it errs loud rather than
   * silent, which is why it is not the Major of this round.
   *
   * `null` means "not an `X.use(...)` mount" — a route handler, a wrapper —
   * and those keep being classified by `classify` exactly as before.
   */
  const parserTarget = (node: ts.Node, params: Set<string>): string | null => {
    const recv = mountReceiver(node);
    if (recv === null) return null;
    // A parameter SHADOWS the file's app, so parameters are tested first.
    if (params.has(recv)) return recv;
    if (appNames.has(recv)) return APP_TARGET;
    return null;
  };

  /** Does this call pass the file's app into `param` of helper `name`? */
  const argForParamIsApp = (call: ts.CallExpression, name: string, param: string): boolean => {
    const order = helpers.get(name)?.order ?? [];
    const idx = order.indexOf(param);
    const arg = idx >= 0 ? call.arguments[idx] : undefined;
    return !!arg && ts.isIdentifier(arg) && appNames.has(arg.text);
  };

  const parserViaAt = (n: ts.Node): string | null => {
    const direct = parserCallName(n, bindings);
    if (direct) return direct;
    if (ts.isIdentifier(n) && parserSymbols.has(n.text) && !declaredNamePos.has(n.getStart(sf))) {
      return parserSymbols.get(n.text)!;
    }
    return null;
  };

  // -------------------------------------------------------------------
  // F-QA-10 — AN ALIAS OR A PROPERTY IS STILL A CALL.
  //
  // `const m = mountParser; m(app)` and `const obj = { mount: mountParser };
  // obj.mount(app)` were not recognised as calls to the helper, so the site
  // fell through to the DECLARATION — measured, the via read a bare
  // `express.json` rather than `express.json (via mountParser)`, and the kind
  // came out `reachable` instead of app-level. Nothing was lost, but the
  // position was the declaration's, which is the same position-dependence
  // F-QA-07 exists to remove.
  //
  // Bounded on purpose: ONE level of indirection through a `const` binding, and
  // object-literal properties of a `const` object. A reassigned binding, a
  // computed key, or a value crossing a function boundary is NOT resolved — it
  // falls through to the declaration exactly as before, which is the behaviour
  // this replaces rather than a new blind spot.
  // -------------------------------------------------------------------
  const helperAliases = new Map<string, string>();
  const collectAliases = (n: ts.Node): void => {
    if (ts.isVariableDeclaration(n) && ts.isIdentifier(n.name) && n.initializer) {
      // const m = mountParser;
      if (ts.isIdentifier(n.initializer) && helpers.has(n.initializer.text)) {
        helperAliases.set(n.name.text, n.initializer.text);
      }
      // const obj = { mount: mountParser, other };
      if (ts.isObjectLiteralExpression(n.initializer)) {
        for (const pr of n.initializer.properties) {
          if (ts.isPropertyAssignment(pr) && ts.isIdentifier(pr.name) &&
              ts.isIdentifier(pr.initializer) && helpers.has(pr.initializer.text)) {
            helperAliases.set(`${n.name.text}.${pr.name.text}`, pr.initializer.text);
          } else if (ts.isShorthandPropertyAssignment(pr) && helpers.has(pr.name.text)) {
            helperAliases.set(`${n.name.text}.${pr.name.text}`, pr.name.text);
          }
        }
      }
    }
    ts.forEachChild(n, collectAliases);
  };
  collectAliases(sf);

  /** The helper a call expression resolves to — directly, or through one alias. */
  const calleeHelperName = (n: ts.Node): string | null => {
    if (!ts.isCallExpression(n)) return null;
    if (ts.isIdentifier(n.expression)) {
      const direct = n.expression.text;
      if (helpers.has(direct)) return direct;
      return helperAliases.get(direct) ?? null;
    }
    if (ts.isPropertyAccessExpression(n.expression) && ts.isIdentifier(n.expression.expression)) {
      return helperAliases.get(`${n.expression.expression.text}.${n.expression.name.text}`) ?? null;
    }
    return null;
  };

  // A helper "mounts a parser" if its body contains a parser site, or calls a
  // helper that does. Iterated to a fixed point; the loop can only add, and it
  // is bounded by the number of helpers.
  // F-QA-02: collect EVERY parser a helper mounts, not the first one. The first
  // cut short-circuited, so `json` + `urlencoded` in one helper read as `json`
  // alone and `urlencodedMounted` went false where the parent read true —
  // SERVICES_WITH_URLENCODED would have shrunk without a single leg moving.
  // F-QA-A — each entry carries `innerPos`, the position INSIDE the helper at
  // which that parser runs. Without it every parser a helper mounts collapses
  // to the call site, which is also where the helper's own guard lands, and
  // `pos > guardPos` is false at equality — so guard-then-parser reads CLEAN.
  const helperMounts = new Map<string, Array<{ via: string; appVia: string | null; innerPos: number }>>();
  for (let pass = 0; pass <= helpers.size; pass += 1) {
    let grew = false;
    for (const [name, h] of helpers) {
      // F-QA-07 (Major, latent) — DO NOT SKIP AN ALREADY-RECORDED HELPER.
      //
      // This loop used to `continue` on any helper already in `helperMounts`.
      // A helper with its OWN parser is recorded on pass 1; if it also calls a
      // mounting helper DECLARED AFTER IT, that callee is only recorded on a
      // later pass — and by then the caller is never revisited, so the callee's
      // parsers are attributed to a helper whose own sites are suppressed and
      // emitted at no call site. They are emitted NOWHERE.
      //
      // Measured against the unfixed scanner before this was written, on one
      // program written two ways (only the declaration order differs):
      //
      //   outer declared FIRST : urlencodedMounted=false, lateAppLevel=1
      //   inner declared FIRST : urlencodedMounted=true,  lateAppLevel=2
      //
      // So it is not merely a flipped boolean — the post-guard case UNDER-COUNTS
      // BY A WHOLE PARSER in one order. `express.urlencoded` appears in no site
      // list at all when `outer` comes first.
      //
      //   "A static instrument whose verdict depends on declaration order is
      //    wrong in one of the two orders by construction."
      //
      // So: recompute every helper on every pass, and treat a CHANGE — not a
      // first write — as growth. The set of (via, appLevel) pairs a helper can
      // hold is monotone (a pair is never removed, and the vias come from a
      // finite set of parser sites), so the loop still terminates; the pass
      // bound below is unchanged and remains a hard stop either way.
      const found: Array<{ via: string; appVia: string | null; innerPos: number }> = [];
      const walk = (n: ts.Node): void => {
        const via = parserViaAt(n);
        // F-QA-03: a parser only counts where it is MOUNTED. A declaration and
        // a bare mention are arguments to nothing.
        if (via && inMountingPosition(n)) {
          found.push({ via, appVia: parserTarget(n, h.params), innerPos: n.getStart(sf) });
          return;
        }
        const callee = calleeHelperName(n);
        if (callee && helperMounts.has(callee)) {
          const calleeBody = helpers.get(callee)?.body;
          // F-QA-11: a helper declared INSIDE this one was already walked as
          // part of this body, with THIS helper's parameters in scope — which
          // is the correct reading. Adding it again at its call re-attributes
          // the same parser with the CALLEE's parameters, which do not contain
          // the outer's, so the duplicate lands in the other list. Measured:
          // one parser, app-level=1 AND reachable=1.
          const nestedHere = !!calleeBody && encloses(h.body, calleeBody);
          if (!nestedHere) {
            for (const inner of helperMounts.get(callee)!) {
              // The callee's parsers run where the callee is CALLED, so the
              // position that orders them inside THIS helper is this call's,
              // and the callee's target is re-resolved through the ARGUMENT
              // this call passes — the same rule the guard side uses.
              let appVia: string | null = inner.appVia;
              if (appVia !== null && appVia !== APP_TARGET) {
                const order = helpers.get(callee)?.order ?? [];
                const idx = order.indexOf(appVia);
                const arg = idx >= 0 && ts.isCallExpression(n) ? n.arguments[idx] : undefined;
                appVia =
                  arg && ts.isIdentifier(arg)
                    ? h.params.has(arg.text)
                      ? arg.text
                      : appNames.has(arg.text)
                        ? APP_TARGET
                        : null
                    : null;
              }
              found.push({ via: inner.via, appVia, innerPos: n.getStart(sf) });
            }
          }
          return;
        }
        ts.forEachChild(n, walk);
      };
      walk(h.body);
      if (found.length) {
        // Compare on content, not on presence. `grew` must mean "this pass
        // learned something", or the loop either stops early (the old bug) or
        // never stops at all.
        const key = (xs: Array<{ via: string; appVia: string | null; innerPos: number }>): string =>
          xs.map((x) => `${x.via}\u0000${x.appVia}\u0000${x.innerPos}`).sort().join('\u0001');
        const prev = helperMounts.get(name);
        if (!prev || key(prev) !== key(found)) {
          helperMounts.set(name, found);
          grew = true;
        }
      }
    }
    if (!grew) break;
  }

  // -------------------------------------------------------------------
  // F-QA-01 — SUPPRESS ONLY WHAT IS ACTUALLY RE-ATTACHED.
  //
  // The first cut suppressed every site inside a mounting helper and restored
  // it only where that helper was called by a bare identifier IN THIS FILE. A
  // helper exported and called from another module got nothing back, so the
  // fix made a live service INVISIBLE where the unfixed scanner had seen it —
  // `services/demo-service/src/app.ts` builds its whole app inside
  // `export function createApp()` and `index.ts` calls it.
  //
  // A helper is ATTRIBUTED only if it has a call in this file that is itself
  // attributed: a call at top level, or a call inside an attributed helper.
  // Anything else falls through to the DECLARATION position, exactly as the
  // parent did — inside a factory the declaration IS the run position, which
  // makes falling through the fail-safe direction rather than the lossy one.
  // -------------------------------------------------------------------
  const enclosingHelperOf = (n: ts.Node): string | null => {
    let best: string | null = null;
    let bestStart = -1;
    for (const [name, h] of helpers) {
      if (encloses(h.body, n) && h.body.getStart(sf) > bestStart) {
        best = name;
        bestStart = h.body.getStart(sf);
      }
    }
    return best;
  };

  const callsOf = new Map<string, Array<string | null>>();
  const visitCalls = (n: ts.Node): void => {
    const callee = calleeHelperName(n);
    if (callee && helperMounts.has(callee)) {
      const list = callsOf.get(callee) ?? [];
      list.push(enclosingHelperOf(n));
      callsOf.set(callee, list);
    }
    ts.forEachChild(n, visitCalls);
  };
  visitCalls(sf);

  const attributed = new Set<string>();
  for (let pass = 0; pass <= helpers.size; pass += 1) {
    let grew = false;
    for (const [name] of helperMounts) {
      if (attributed.has(name)) continue;
      const sites = callsOf.get(name) ?? [];
      if (sites.some((encl) => encl === null || attributed.has(encl))) {
        attributed.add(name);
        grew = true;
      }
    }
    if (!grew) break;
  }

  /** Is this node lexically inside a helper whose mount is attributed to its calls? */
  const insideAttributedHelper = (n: ts.Node): boolean => {
    for (const [name, h] of helpers) {
      if (attributed.has(name) && encloses(h.body, n)) return true;
    }
    return false;
  };

  // -------------------------------------------------------------------
  // KS-827 — A GUARD MOUNTED OR INVOKED BY A SAME-FILE HELPER.
  //
  // The mirror of KS-816, and the same one rule: a declaration mounts nothing,
  // its CALLS do. `visitGuards` used to walk the whole file and push
  // `n.getStart(sf)` for every guard call it found, including the ones inside
  // helper bodies, then take the MINIMUM. So the verdict was decided by where a
  // helper is WRITTEN rather than where it RUNS.
  //
  // Measured against the unfixed scanner before this was written, because the
  // direction is not guessable — a code read of the old `visitGuards` predicted
  // the wrong one:
  //
  //   M1  helper declared ABOVE the parser, called BELOW it
  //       → the guard really runs last, so the file is CLEAN
  //       → old scanner: `lateAppLevel = 1`. A FALSE RED.
  //
  //   M2  helper called ABOVE the parser, declared BELOW it (hoisting, and
  //       helpers are commonly written at the bottom of a file)
  //       → the parser really is unguarded, so the file is RED
  //       → old scanner: `lateAppLevel = 0`. A FALSE CLEAN — the dangerous one.
  //
  //   M3  helper never called at all
  //       → no guard ever runs, so the file is RED
  //       → old scanner: whichever the declaration's position implied.
  //
  // M1 and M3 have NO fixed direction: flip the declaration above or below the
  // parser and the verdict flips with it. That is the defect stated properly —
  // not "M2 is a false clean" but THE VERDICT IS A FUNCTION OF DECLARATION
  // POSITION, and declaration position is arbitrary. Which is why the closure
  // cell below is an order-swap PAIR asserted to AGREE, and not a list of three
  // shapes each pinned separately.
  //
  // Resolved to a FIXED POINT, like the parser side, so a helper calling a
  // guard-mounting helper does not move the blind spot to depth 2. Hoisting
  // needs no special case once positions come from call sites: a call above its
  // own declaration is just a call site with a lower position.
  // -------------------------------------------------------------------
  // Which helpers are EXPORTED — needed for the asymmetry below.
  //
  // F-QA-C — SIX SHAPES THAT WERE MISSED, and every one errs LOUD. A missed
  // export makes a live factory look like dead code: `deadHere` becomes true,
  // its guard is suppressed with no call site to re-attach it to, the scan
  // returns null, the file drops out of `SCANS`, and the corpus leg reds
  // NAMING it. So this is a false-RED fix, not a false-clean one — which is
  // why it is the Minor of the three and still worth closing: a security
  // instrument that cries wolf on a legitimate spelling gets its corpus edited
  // rather than its finding read.
  //
  // Measured against the unfixed instrument before this was written, on one
  // factory (parser then guard, no in-file caller — `demo-service`'s shape)
  // written eleven ways:
  //
  //   export { createApp }                     NULL   <- missed
  //   export { createApp as makeApp }          NULL   <- missed
  //   export default createApp                 NULL   <- missed
  //   export = createApp                       NULL   <- missed
  //   module.exports = createApp               NULL   <- missed
  //   exports.createApp = createApp            NULL   <- missed
  //   export function createApp()              scan      already collected
  //   export default function createApp()      scan      already collected
  //   export const createApp = () => {}        scan      already collected
  //   NOT exported, never called               NULL      correct, and MUST stay
  //   exported AND called in this file         scan      correct
  //
  // The last two are the discriminating pair: widening what counts as exported
  // must not make genuinely dead code look live.
  const exportedHelpers = new Set<string>();
  const collectExports = (n: ts.Node): void => {
    const exported = (mods?: ts.NodeArray<ts.ModifierLike>): boolean =>
      !!mods && mods.some((m) => m.kind === ts.SyntaxKind.ExportKeyword);
    if (ts.isFunctionDeclaration(n) && n.name && exported(n.modifiers)) {
      exportedHelpers.add(n.name.text);
    }
    if (ts.isVariableStatement(n) && exported(n.modifiers)) {
      for (const d of n.declarationList.declarations) {
        if (ts.isIdentifier(d.name)) exportedHelpers.add(d.name.text);
      }
    }
    // `export { f }` and `export { f as g }` — the LOCAL name is what binds a
    // helper here, so an alias is read from `propertyName`, not `name`. A
    // re-export (`export { f } from './y'`) names no local binding and is
    // skipped: it would credit a helper this file does not contain.
    if (ts.isExportDeclaration(n) && !n.moduleSpecifier && n.exportClause && ts.isNamedExports(n.exportClause)) {
      for (const el of n.exportClause.elements) {
        exportedHelpers.add((el.propertyName ?? el.name).text);
      }
    }
    // `export default createApp;` and `export = createApp;` — both are
    // ExportAssignment; `isExportEquals` is the only thing that separates them,
    // and for this purpose neither distinction matters.
    if (ts.isExportAssignment(n) && ts.isIdentifier(n.expression)) {
      exportedHelpers.add(n.expression.text);
    }
    // CommonJS: `module.exports = createApp`, `module.exports = { createApp }`,
    // and `exports.createApp = createApp`. Only an identifier right-hand side
    // names a helper; an inline function expression is not one of `helpers`.
    if (ts.isExpressionStatement(n) && ts.isBinaryExpression(n.expression) &&
        n.expression.operatorToken.kind === ts.SyntaxKind.EqualsToken &&
        ts.isPropertyAccessExpression(n.expression.left) &&
        ts.isIdentifier(n.expression.left.expression)) {
      const target = n.expression.left.expression.text;
      const prop = n.expression.left.name.text;
      const isModuleExports = target === 'module' && prop === 'exports';
      const isExportsProp = target === 'exports';
      if (isModuleExports || isExportsProp) {
        const rhs = n.expression.right;
        if (ts.isIdentifier(rhs)) {
          exportedHelpers.add(rhs.text);
        } else if (isModuleExports && ts.isObjectLiteralExpression(rhs)) {
          for (const pr of rhs.properties) {
            if (ts.isShorthandPropertyAssignment(pr)) exportedHelpers.add(pr.name.text);
            else if (ts.isPropertyAssignment(pr) && ts.isIdentifier(pr.initializer)) {
              exportedHelpers.add(pr.initializer.text);
            }
          }
        }
      }
    }
    ts.forEachChild(n, collectExports);
  };
  collectExports(sf);

  // -------------------------------------------------------------------
  // F-QA-B — WHAT the guard was mounted ON, not merely THAT one was mounted.
  //
  // `mountedOnApp` accepts ANY of the helper's parameters as "the app". A file
  // cannot see that from inside the helper — `x.use(guard())` is the same AST
  // whether `x` is the application or an `express.Router()`. So a ROUTER guard
  // mounted through a helper credited a guard position on the APP, and the
  // app-level `express.json()` above it read CLEAN while genuinely unguarded.
  // The inline spelling of the same program reads NULL, which is loud. Same
  // program, two spellings, opposite loudness — and the wrong one silent.
  //
  // MEASURED against the unfixed instrument before this was written:
  //
  //   router guard VIA HELPER, app json above it    late=0   <- FALSE CLEAN
  //   the same program INLINE                       NULL        loud
  //   depth 2, outer called with a router           late=0   <- FALSE CLEAN
  //   param SHADOWS the file app, called w/ router  late=0   <- FALSE CLEAN
  //
  // So a helper no longer records a boolean. It records its guard TARGETS: the
  // file's own app (a closure mount, which needs no argument), or the names of
  // its own parameters. A call site credits a guard position only when it
  // actually passes the file's app into one of those parameters. An argument
  // that is neither the app nor a parameter of the calling helper is UNKNOWN
  // and earns NO credit — the fail-safe direction, because an uncredited guard
  // makes the file read NULL, which the corpus leg reds BY NAME.
  //
  // A parameter SHADOWS the file's app, so parameters are tested FIRST: a
  // helper written `function mountGuard(app) { app.use(guard()) }` mounts on
  // its parameter, whatever the outer app happens to be called.
  // -------------------------------------------------------------------
  // helper name -> the targets its guard is mounted on (APP_TARGET, or its own
  // parameter names). Fixed point, so a helper calling a guard-mounting helper
  // inherits the target the ARGUMENT it passes resolves to.
  const guardTargets = new Map<string, Set<string>>();
  // ...and the earliest position INSIDE the helper at which that guard runs,
  // which is what F-QA-A orders the helper's own parsers against.
  const helperGuardInnerPos = new Map<string, number>();
  const targetKey = (xs: Set<string>): string => [...xs].sort().join('|');

  for (let pass = 0; pass <= helpers.size; pass += 1) {
    let grew = false;
    for (const [name, h] of helpers) {
      const targets = new Set<string>(guardTargets.get(name) ?? []);
      let earliest = helperGuardInnerPos.get(name) ?? Number.POSITIVE_INFINITY;
      const note = (n: ts.Node): void => {
        earliest = Math.min(earliest, n.getStart(sf));
      };
      const walk = (n: ts.Node): void => {
        if (guardCallName(n, bindings)) {
          const recv = mountReceiver(n);
          if (recv !== null) {
            // Parameters shadow the file's app, so they are tested first.
            if (h.params.has(recv)) {
              targets.add(recv);
              note(n);
            } else if (appNames.has(recv)) {
              targets.add(APP_TARGET);
              note(n);
            }
          }
          return;
        }
        // ...or a call to a helper already known to mount one. The callee's
        // guard runs where it is CALLED, so this call's position is the one
        // that orders it inside this body.
        const calleeName = calleeHelperName(n);
        if (calleeName && guardTargets.has(calleeName)) {
          const callee = helpers.get(calleeName);
          if (callee && ts.isCallExpression(n)) {
            for (const t of guardTargets.get(calleeName)!) {
              if (t === APP_TARGET) {
                targets.add(APP_TARGET);
                note(n);
                continue;
              }
              const idx = callee.order.indexOf(t);
              const arg = idx >= 0 ? n.arguments[idx] : undefined;
              if (arg && ts.isIdentifier(arg)) {
                if (h.params.has(arg.text)) {
                  targets.add(arg.text);
                  note(n);
                } else if (appNames.has(arg.text)) {
                  targets.add(APP_TARGET);
                  note(n);
                }
                // anything else is UNKNOWN — no credit, which reads NULL, loud.
              }
            }
          }
          return;
        }
        ts.forEachChild(n, walk);
      };
      walk(h.body);
      const prevTargets = guardTargets.get(name);
      if (targets.size > 0 && (!prevTargets || targetKey(targets) !== targetKey(prevTargets))) {
        guardTargets.set(name, targets);
        grew = true;
      }
      if (Number.isFinite(earliest) && helperGuardInnerPos.get(name) !== earliest) {
        helperGuardInnerPos.set(name, earliest);
        grew = true;
      }
    }
    if (!grew) break;
  }

  /** The helpers that mount a guard at all — the set the rest of the pass reads. */
  const guardMounting = new Set<string>(guardTargets.keys());

  /**
   * Does THIS call site actually put the guard on the file's app?
   *
   * A closure mount needs no argument. A parameter mount needs the call to pass
   * the file's app into that parameter's position; a router, or anything this
   * file cannot resolve to the app, earns nothing.
   */
  const guardCreditedAt = (call: ts.CallExpression, name: string): boolean => {
    const targets = guardTargets.get(name);
    if (!targets) return false;
    if (targets.has(APP_TARGET)) return true;
    const order = helpers.get(name)?.order ?? [];
    for (const t of targets) {
      const idx = order.indexOf(t);
      const arg = idx >= 0 ? call.arguments[idx] : undefined;
      if (arg && ts.isIdentifier(arg) && appNames.has(arg.text)) return true;
    }
    return false;
  };

  // Pass 2 — which of those are ATTRIBUTED TO THEIR CALLS, which is NOT the
  // same question and is where the first cut of this fix was wrong.
  //
  // ⚠ THE MIRROR IS NOT SYMMETRIC, and this is the whole subtlety. On the
  // parser side, a factory with no in-file caller keeps its DECLARATION as the
  // run position, and #828 calls that "the fail-safe direction" — for a PARSER
  // it is, because it still reports the parser. For a GUARD the same choice is
  // the LOSSY one: crediting a guard at a declaration that may never run is a
  // false CLEAN, the exact thing this ticket exists to stop.
  //
  // My first cut attributed every guard-mounting helper unconditionally. That
  // reproduced #828 round 1's own regression in mirror: `createApp()` in
  // `services/demo-service` is exported and called from ANOTHER file, so it has
  // no in-file call site, its guard was suppressed with nothing to re-attach
  // it to, and the whole scan returned null — dropping the service out of the
  // corpus. Seven suites red, caught by the full run, not by the new cases.
  //
  // So the two shapes are separated by the only signal a single file carries:
  //   · EXPORTED, no in-file caller  → a factory; its caller is elsewhere, so
  //     the declaration stands as the run position (parser-side behaviour).
  //   · NOT exported, no in-file caller → dead code in this file; nothing
  //     calls it, so no guard runs, and it contributes no position.
  // A file cannot tell an exported-but-never-called factory from a live one.
  // That residue is named on the ticket rather than papered over here.
  const guardCallsOf = new Map<string, Array<string | null>>();
  const visitGuardCalls = (n: ts.Node): void => {
    const callee = calleeHelperName(n);
    if (callee && guardMounting.has(callee)) {
      const list = guardCallsOf.get(callee) ?? [];
      list.push(enclosingHelperOf(n));
      guardCallsOf.set(callee, list);
    }
    ts.forEachChild(n, visitGuardCalls);
  };
  visitGuardCalls(sf);

  const helperGuards = new Set<string>();
  for (let pass = 0; pass <= helpers.size; pass += 1) {
    let grew = false;
    for (const name of guardMounting) {
      if (helperGuards.has(name)) continue;
      const sites = guardCallsOf.get(name) ?? [];
      const calledInFile = sites.some((encl) => encl === null || helperGuards.has(encl));
      // Dead in this file AND not exported → nothing can call it, so its guard
      // never runs and it is attributed (suppressed) with no call to re-attach.
      const deadHere = sites.length === 0 && !exportedHelpers.has(name);
      if (calledInFile || deadHere) {
        helperGuards.add(name);
        grew = true;
      }
    }
    if (!grew) break;
  }

  /** Is this node lexically inside a helper whose guard belongs to its calls? */
  const insideGuardHelper = (n: ts.Node): boolean => {
    for (const [name, h] of helpers) {
      if (helperGuards.has(name) && encloses(h.body, n)) return true;
    }
    return false;
  };

  // KS-832 F-QA-D — A GUARD REACHABLE ONLY THROUGH A CONDITIONAL IS NOT A CLEAN
  // POSITION. Measured on the unfixed scanner, two files with the SAME runtime
  // reality (no guard is mounted) and opposite verdicts:
  //
  //   no call at all                     -> null           LOUD
  //   `if (process.env.NOPE) mountGuard(app)` -> late=0     CLEAN
  //
  // So ADDING DEAD CODE TURNED A LOUD FILE QUIET. Both spellings do it — the
  // via-helper call the finding named, and the inline `app.use(rejectNulBytes())`
  // it did not.
  //
  // Note the asymmetry that made KS-817's F-QA-09 deferral reason wrong: on the
  // PARSER side a never-taken branch OVER-attributes — a false RED, loud. On the
  // GUARD side it UNDER-attributes — a false CLEAN, silent. A silent false clean
  // in an instrument whose green is read as evidence is the worse half, which is
  // why this one is closed and that one was deferred on its census.
  //
  // The rule: a position contributes only if it is UNCONDITIONALLY reached
  // within its own statement list. If every guard position in a file is
  // conditional, the file resolves NULL — exactly as if there were no call —
  // so the corpus leg names it and a human decides. The scanner cannot know
  // whether a branch is taken, and guessing "taken" is the guess that certifies.
  //
  // Scope, stated: this is LEXICAL conditionality. A guard call inside an
  // ordinary function that nobody calls is the cross-file caller-graph problem,
  // recorded as out of scope on KS-832 and needing a different instrument.
  //
  // KS-842 Q-1 — the walk enumerated FOUR node kinds, and the set of TypeScript
  // nodes that make a statement conditionally reached is larger than four. The
  // #836 gate probed sixteen lexical shapes and found SIX silent false cleans;
  // all six are decided inside a single file by this same walk. Added below:
  // the catch clause, the zero-iteration loop bodies, and IIFE transparency.
  //
  // NOT added, deliberately: `DoStatement`. The gate's recommendation lists it
  // among the iteration statements, but a do-while body executes EXACTLY ONCE
  // before its condition is ever evaluated, so the guard genuinely is mounted.
  // Treating it as conditional would answer NULL for a file whose guard really
  // runs — a false LOUD, which sends a human to investigate a clean file.
  // `while` stays conditional even for `while (true)`: the walker cannot
  // evaluate a condition, and conservative-loud is the right direction there.
  // Both directions are pinned by cells in the KS-842 Q-1 battery.
  const isImmediatelyInvoked = (fn: ts.Node): boolean => {
    // `(() => { … })()` — the callee is the function itself, possibly wrapped in
    // parentheses. Its caller is one line up, so it is not a caller-graph
    // question and the walk must continue THROUGH it.
    let outer: ts.Node = fn;
    while (outer.parent && ts.isParenthesizedExpression(outer.parent)) outer = outer.parent;
    const p = outer.parent;
    if (!p) return false;
    if (ts.isCallExpression(p) && p.expression === outer) return true;
    // KS-859 F-842-01 — `(function () { … }).call(this)` and `.apply(…)`.
    //
    // Semantically identical to the form above — the function runs where it is
    // written, and there is no caller graph to ask about — but it is reached
    // through a PROPERTY ACCESS, which the plain form does not follow, so these
    // two spellings read `late=0` where `(() => {})()` reads NULL. KS-842
    // closed one spelling and did not declare the others still open, which is
    // the reason this is written down rather than the loop being closed
    // quietly.
    //
    // Censused at `50913d2c3`: ZERO instances under `services/` and
    // `connectors/` (against a control of 3 plain `.call`/`.apply` calls in the
    // same tree, so the census can match). Latent, not live.
    //
    // `.bind(x)()` is deliberately NOT followed: it is a different shape — the
    // call is on the RESULT of bind, not on the function — and it has no
    // instances either. If it ever appears it belongs in this same block.
    if (
      ts.isPropertyAccessExpression(p) &&
      p.expression === outer &&
      (p.name.text === 'call' || p.name.text === 'apply') &&
      p.parent &&
      ts.isCallExpression(p.parent) &&
      p.parent.expression === p
    ) {
      return true;
    }
    return false;
  };
  const isConditionallyReached = (n: ts.Node): boolean => {
    let child = n;
    let cur = n.parent;
    while (cur && !ts.isSourceFile(cur)) {
      if (ts.isIfStatement(cur) && (cur.thenStatement === child || cur.elseStatement === child)) return true;
      if (ts.isConditionalExpression(cur) && (cur.whenTrue === child || cur.whenFalse === child)) return true;
      if (ts.isCaseClause(cur) || ts.isDefaultClause(cur)) return true;
      // KS-842 Q-1: a catch block runs only on a throw. `try {}` and `finally {}`
      // are NOT conditional and are controlled for.
      if (ts.isCatchClause(cur)) return true;
      // KS-842 Q-1: a loop whose body may run zero times. `for (const r of
      // routers) { r.use(guard) }` over an empty array is the "adding code
      // turned a loud file quiet" mechanism KS-832 named.
      if (
        (ts.isForStatement(cur) ||
          ts.isForOfStatement(cur) ||
          ts.isForInStatement(cur) ||
          ts.isWhileStatement(cur)) &&
        cur.statement === child
      ) {
        return true;
      }
      if (
        ts.isBinaryExpression(cur) &&
        cur.right === child &&
        (cur.operatorToken.kind === ts.SyntaxKind.AmpersandAmpersandToken ||
          cur.operatorToken.kind === ts.SyntaxKind.BarBarToken ||
          cur.operatorToken.kind === ts.SyntaxKind.QuestionQuestionToken)
      ) {
        return true;
      }
      // A function boundary ends the walk: whether THAT function runs is the
      // caller-graph question, not this one. KS-842 Q-1: unless it is
      // IMMEDIATELY INVOKED, in which case the walk continues into the
      // surrounding statement — an IIFE has no caller graph.
      if (ts.isFunctionDeclaration(cur) || ts.isFunctionExpression(cur) || ts.isArrowFunction(cur) || ts.isMethodDeclaration(cur)) {
        if (!isImmediatelyInvoked(cur)) return false;
      }
      child = cur;
      cur = cur.parent;
    }
    return false;
  };
  /**
   * KS-842 Q-1, the bigger half — helpers whose OWN guard mount is conditional.
   *
   * `visitGuards` runs `insideGuardHelper(n)` FIRST, so a mount inside an
   * attributed helper never reaches `isConditionallyReached` at all; the credit
   * is taken at the call site, which may be perfectly unconditional. That makes
   * the mirror image of KS-832's own headline fixture a silent false clean:
   *
   *   function mountGuard(x) { if (cond) { x.use(rejectNulBytes()) } }
   *   mountGuard(app);                       // -> late=0, guard may never run
   *
   * So the conditionality has to travel WITH the helper. A helper counts as
   * conditional when it mounts a guard and EVERY such mount is conditional
   * within its own body — one unconditional mount is enough to make the helper
   * unconditional. `isConditionallyReached` stops at the helper's own function
   * boundary, so this is conditionality within the helper, which is what the
   * call site needs to know.
   */
  const conditionalHelperGuards = new Set<string>();
  for (const [name, h] of helpers) {
    if (!helperGuards.has(name)) continue;
    let sawGuard = false;
    let sawUnconditional = false;
    const walkHelper = (x: ts.Node): void => {
      if (guardCallName(x, bindings)) {
        sawGuard = true;
        if (!isConditionallyReached(x)) sawUnconditional = true;
      }
      ts.forEachChild(x, walkHelper);
    };
    walkHelper(h.body);
    if (sawGuard && !sawUnconditional) conditionalHelperGuards.add(name);
  }

  const conditionalGuardPositions: number[] = [];

  const visitGuards = (n: ts.Node): void => {
    // Suppression runs FIRST and covers both emissions: a guard call inside an
    // attributed helper is that helper's, and so is a call to another
    // guard-helper made from inside one. Both are reached at the OUTER helper's
    // own call sites instead.
    if (!insideGuardHelper(n)) {
      if (guardCallName(n, bindings) && classify(n) === 'app-level') {
        (isConditionallyReached(n) ? conditionalGuardPositions : guardPositions).push(n.getStart(sf));
      }
      const guardCallee = calleeHelperName(n);
      if (
        guardCallee &&
        ts.isCallExpression(n) &&
        helperGuards.has(guardCallee) &&
        // F-QA-B: a call that hands the helper a ROUTER mounts no guard on the
        // app, so it contributes no position and the file reads NULL — loud.
        guardCreditedAt(n, guardCallee)
      ) {
        // KS-842 Q-1: conditional at the CALL SITE, or conditional INSIDE the
        // helper — either way the guard may not run, so the position is not clean.
        (isConditionallyReached(n) || conditionalHelperGuards.has(guardCallee)
          ? conditionalGuardPositions
          : guardPositions
        ).push(n.getStart(sf));
      }
    }
    ts.forEachChild(n, visitGuards);
  };
  visitGuards(sf);

  // A helper that mounts a guard but is NEVER CALLED contributes no position,
  // so a file whose only guard sits in dead code returns null here — and the
  // corpus leg (`expect(guarded).toEqual(CORPUS)`) then reds NAMING the file,
  // rather than the file quietly vanishing from SCANS. That is the honest
  // answer: no call, no guard.
  // KS-832 F-QA-D: conditional positions do not establish a clean guard. A file
  // whose ONLY guard sits behind an `if` reads null here, the same as a file
  // with no call — so the two programs with the same runtime reality now give
  // the same verdict instead of opposite ones.
  if (guardPositions.length === 0) return null;
  const guardPos = Math.min(...guardPositions);

  // Pass 3 — every parser site in the file, positioned and classified.
  const sites: ParserSite[] = [];
  const visitSites = (n: ts.Node): void => {
    // KS-816: sites INSIDE an attributed helper belong to that helper's CALLS,
    // not to the declaration — a declaration mounts nothing. This check runs
    // FIRST: a helper that calls a helper would otherwise emit a site at the
    // inner call, which is still inside a declaration.
    const attributedHere = !insideAttributedHelper(n);
    // KS-816: a call to a helper that mounts a parser IS the mount, here.
    const siteCallee = calleeHelperName(n);
    if (attributedHere && ts.isCallExpression(n) && siteCallee && attributed.has(siteCallee)) {
      const pos = n.getStart(sf);
      // F-QA-A — if this helper also carries the guard, the guard is emitted at
      // exactly `pos` (below, in `visitGuards`) and every parser it mounts would
      // land on that same position, where `pos > guardPos` is false. So order
      // the parsers AROUND the guard using the order they have INSIDE the
      // helper. A half-unit is sound and deliberate: positions are integer
      // character offsets, so `pos ± 0.5` cannot cross any other site or guard
      // position — it settles this parser against the guard at its own call
      // site and against nothing else.
      //
      // Only when the helper's guard belongs to this call. A helper whose guard
      // stays at its declaration (exported, no in-file caller) keeps its parsers
      // there too, so both are already in their true order and need no offset.
      const helperName = siteCallee;
      const innerGuardPos = helperGuards.has(helperName)
        ? helperGuardInnerPos.get(helperName)
        : undefined;
      // F-QA-02: one site per parser the helper mounts, not one per helper.
      for (const h of helperMounts.get(helperName)!) {
        const effectivePos =
          innerGuardPos === undefined ? pos : h.innerPos > innerGuardPos ? pos + 0.5 : pos - 0.5;
        // F-QA-05: a parameter mount is app-level only if THIS call hands it
        // the file's app. A router earns `classify`, which reads route-scoped.
        const appLevel =
          h.appVia === APP_TARGET ||
          (h.appVia !== null && argForParamIsApp(n, helperName, h.appVia));
        sites.push({
          pos: effectivePos,
          // The LINE stays the call's own — a half-unit orders the site, it
          // does not move it to another line of source.
          line: lineOf(pos),
          kind: appLevel ? 'app-level' : classify(n),
          via: `${h.via} (via ${helperName})`,
        });
      }
    }
    if (!attributedHere) {
      ts.forEachChild(n, visitSites);
      return;
    }
    const parser = parserCallName(n, bindings);
    if (parser) {
      const pos = n.getStart(sf);
      // A parser bound to a symbol is counted at its uses, not here.
      if (!initializerPos.has(pos)) {
        sites.push({
          pos,
          line: lineOf(pos),
          kind: combinedPos.has(pos) ? 'app-level' : classify(n),
          via: parser,
        });
      }
    } else if (
      ts.isIdentifier(n) &&
      parserSymbols.has(n.text) &&
      !declaredNamePos.has(n.getStart(sf))
    ) {
      const pos = n.getStart(sf);
      sites.push({
        pos,
        line: lineOf(pos),
        kind: classify(n),
        via: `${parserSymbols.get(n.text)} (via ${n.text})`,
      });
    }
    ts.forEachChild(n, visitSites);
  };
  visitSites(sf);

  return {
    rel,
    guardPos,
    guardLine: lineOf(guardPos),
    lateAppLevel: sites.filter((s) => s.kind === 'app-level' && s.pos > guardPos),
    postGuardParserSites: sites.filter((s) => s.kind === 'reachable' && s.pos > guardPos),
    urlencodedMounted:
      sites.some((s) => s.kind === 'app-level' && s.via.startsWith('express.urlencoded')) ||
      (combinedCalls.length > 0 && combinedMountsUrlencoded),
  };
}

/** The disk-facing wrapper. All the logic is in `analyseSource`, so the legs
 *  below can drive the exact same predicate on a synthetic source. */
function scan(file: string): Scan | null {
  return analyseSource(readFileSync(file, 'utf8'), file, relative(DEV_ROOT, file));
}

/**
 * THE CORPUS, DECLARED — every file in the repo that creates an express app and
 * therefore owns a guard-ordering question.
 *
 * Declared rather than counted (KS-800 F-03's lesson): when the old
 * `expect(SCANS.length).toBe(24)` moved, the only signal was
 * `expected 23 to be 24`, naming neither the file nor the cause — which invites
 * editing the number and erasing a service from the corpus. A set names what
 * moved. Adding an entry should cost a deliberate edit here: a new express app
 * that parses bodies is a new attack surface.
 *
 * `connectors/whatsapp-bot/src/index.ts` is KS-800 F-15's addition — an
 * unguarded `POST /webhook` fed by Meta's Cloud API, outside the old walk by
 * construction and therefore invisible rather than failing.
 */
const CORPUS = [
  'connectors/whatsapp-bot/src/index.ts',
  'services/analytics/src/index.ts',
  'services/anchoring/src/index.ts',
  'services/api-gateway/src/index.ts',
  'services/auth/src/index.ts',
  'services/billing/src/index.ts',
  'services/demo-service/src/app.ts',
  'services/governance/src/index.ts',
  'services/guardian/src/index.ts',
  'services/kyc/src/index.ts',
  'services/m365-integration/src/index.ts',
  'services/mcp-server/src/http-server.ts',
  'services/nft-certificate/src/app.ts',
  'services/originate/src/index.ts',
  'services/prism/src/index.ts',
  'services/queue/src/index.ts',
  'services/referral/src/index.ts',
  'services/security/src/index.ts',
  'services/staking/src/index.ts',
  'services/tenant-provisioning/src/index.ts',
  'services/timestamping/src/index.ts',
  'services/tokenisation/src/index.ts',
  'services/transfer/src/index.ts',
  'services/vc-issuer/src/index.ts',
  'services/wallet-connector/src/server.ts',
];

function entrypoints(): string[] {
  return structuralEntrypoints(DEV_ROOT);
}

const SCANS = entrypoints()
  .map(scan)
  .filter((s): s is Scan => s !== null);

describe('KS-781 P3-3 LEG C — the guard is mounted after every app-level parser', () => {
  it('every entrypoint in the corpus mounts the guard — BY NAME, not by count', () => {
    // KS-800 F-03's lesson, applied to this leg. The old assertion was
    // `expect(SCANS.length).toBe(24)`, and when a service dropped out the only
    // signal was `expected 23 to be 24` — a message naming neither the file nor
    // the cause, which invites a maintainer to edit the 24 down and erase the
    // service from the corpus. A set names what moved.
    //
    // History the number alone did not record: 22 under the `{index,app,server}
    // .ts` name list, which could not see `mcp-server/src/http-server.ts`;
    // 24 once `demo-service` gained a guard (it creates an app and mounted none,
    // so `scan()` dropped it as null and no leg could see it); 25 once the walk
    // stopped assuming `services/` and found `connectors/whatsapp-bot`.
    const found = entrypoints().map((f) => relative(DEV_ROOT, f)).sort();
    const guarded = SCANS.map((s) => s.rel).sort();
    expect(
      found.filter((f) => !guarded.includes(f)),
      'These files create an express app but mount NO control-byte guard, so ' +
        '`scan()` returns null and every assertion below is blind to them. That ' +
        'is how demo-service, mcp-server and connectors/whatsapp-bot each stayed ' +
        'unguarded while this file was green.',
    ).toEqual([]);
    expect(guarded).toEqual(CORPUS);
  });

  it('🔴 KS-833 F-7 — the number of GENERATED cells equals the corpus size', () => {
    // LEG C below generates ONE CELL PER ENTRYPOINT. That means a narrowed
    // corpus does not FAIL a cell — it REMOVES one, and the suite reports a
    // smaller total instead of a red.
    //
    // Measured by the #838 gate (T-2): under a narrowed walk this file reported
    // `2 failed | 196 passed (198)` — a total of 198, not 199. The cell that
    // vanished was `connectors/whatsapp-bot/src/index.ts mounts rejectNulBytes()
    // …`. The narrowing was still caught there, by other cells — but "199
    // passed" cannot BY ITSELF be read as "the corpus is intact", and that is
    // the property this cell adds.
    //
    // Pinned to a LITERAL, deliberately. `SCANS.length === CORPUS.length` would
    // be satisfied by a narrowing that moved both sides together — the exact
    // shape that made the first version of the ROOTS cell in ks727 unable to
    // fail. Widening the corpus is welcome and updates this number by hand.
    expect(CORPUS.length, 'the declared corpus size — update deliberately').toBe(25);
    expect(
      SCANS.length,
      `LEG C generated ${SCANS.length} cells for a corpus of ${CORPUS.length}. A missing ` +
        'cell is an entrypoint that silently left the corpus: the suite would report a ' +
        'smaller PASSED total rather than a failure. Compare the set cell above for which.',
    ).toBe(CORPUS.length);
  });

  it.each(SCANS.map((s) => [s.rel, s] as const))(
    '%s mounts rejectNulBytes() after every app-level body parser',
    (_rel, s) => {
      expect(
        s.lateAppLevel.map((x) => `${x.via}@${x.line}`),
        `${s.rel}: rejectNulBytes() is mounted at line ${s.guardLine}, but app-level body ` +
          `parsers are mounted AFTER it at line(s) ` +
          `${s.lateAppLevel.map((x) => `${x.line} (${x.via})`).join(', ')}. The guard inspects ` +
          `req.body, so it cannot see a body parsed after it. Move the guard below every parser. ` +
          `Ordering here is by SOURCE POSITION, so a multi-line app.use(...) is caught too ` +
          `(KS-800 F-02) — reflowing the mount does not hide it.`,
      ).toEqual([]);
    },
  );

  it('the set of services mounting express.urlencoded is exactly as declared', () => {
    const actual = SCANS.filter((s) => s.urlencodedMounted)
      .map((s) => s.rel)
      .sort();
    expect(actual).toEqual([...SERVICES_WITH_URLENCODED].sort());
  });
});

describe('KS-781 P3-3 LEG D — route-scoped parsers after the guard are a declared, bounded set', () => {
  it('no service has grown an undeclared post-guard parser site', () => {
    const actual: Record<string, number> = {};
    for (const s of SCANS) {
      if (s.postGuardParserSites.length) actual[s.rel] = s.postGuardParserSites.length;
    }
    expect(
      actual,
      'A body parser is reachable after the global control-byte guard. Bodies it parses are ' +
        'never inspected. Either mount it before the guard, or add it to POST_GUARD_PARSER_SITES ' +
        'with a ticket — do not widen this set silently. This now includes an INLINE parser ' +
        'handed to a route inside an entrypoint (KS-800 F-01), which the previous line-oriented ' +
        'scan could not see at all.',
    ).toEqual(POST_GUARD_PARSER_SITES);
  });

  it('names WHERE each declared site is, so the count is not the only signal', () => {
    // F-03's lesson: `expected 23 to be 24` invites a maintainer to edit the
    // number. A count that changes should arrive with the site that changed it.
    const sites = SCANS.flatMap((s) =>
      s.postGuardParserSites.map((x) => `${s.rel}:${x.line} ${x.via}`),
    ).sort();
    // KS-818 F-06 moved all three by exactly +14 — that change added 14 net
    // lines of COMMENT above them (17 added, 3 removed) and touched no code.
    // Checked as a uniform shift of the same three sites with the same `via`,
    // not re-baselined from whatever the run happened to print: 816 -> 830,
    // 829 -> 843, 862 -> 876.
    //
    // KS-833 Q-5 moved all three again by exactly +10, and by the same cause:
    // that item rewrote the F-06 paragraph above these routes (10 net lines of
    // COMMENT, no code). Checked the same way — a uniform +10 on the same three
    // sites with the same `via`, each new line read back and confirmed to be the
    // statement it claims: 830 -> 840, 843 -> 853, 876 -> 886.
    //
    // KS-858 moved all three again by exactly +14 — the edge path-normalisation
    // mount and its comment, added ABOVE these routes at index.ts:220-234
    // (14 net lines: 1 import, 12 comment, 1 `app.use`, and the blank line;
    // index.ts 1249 -> 1263). Checked the same way: a uniform +14 on the same
    // three sites with the same `via`, each new line read back out of the file
    // and confirmed to be the statement it claims — 840 -> 854
    // (`app.post('/api/auth/wallet/challenge', mockBodyParser, …`), 853 -> 867
    // (`…/wallet/authenticate…`), 886 -> 900 (the createVerificationRoutes
    // factory argument) — not re-baselined from whatever the run printed.
    //
    // KS-1126 (KS-953 instance 4): #951 (KS-1041 Step 2, b75cff4d6) moved all
    // three by exactly -8 — its edit sat ABOVE these routes (index.ts 1288 ->
    // 1280, +6 -14). Checked the same way: a uniform -8 on the same three sites
    // with the same `via`, each new line read back out of the file and confirmed
    // to be the statement it claims — 854 -> 846 (`…/wallet/challenge…`),
    // 867 -> 859 (`…/wallet/authenticate…`), 900 -> 892 (the
    // createVerificationRoutes factory argument) — not re-baselined from the
    // run. packages/shared was red on develop for two days before anyone ran
    // it: the FOURTH instance of the KS-953 class, and the class fix is still
    // open there.
    //
    // THIS ONE WAS NOT CAUGHT BY THE AUTHOR OR BY THE PR'S TIER-1 GATE. Both
    // ran the api-gateway package suite (green, 277) and three of the four
    // platform suites; neither ran packages/shared, which is the only place
    // this list lives. The cross-package edge is the gap, not the numbers:
    // touching api-gateway's index.ts turns THIS package red, and nothing in
    // the touched package can say so. Tracked as KS-953.
    //
    // Four times now an edit above these routes has moved this list, which is
    // worth naming: these are hand-maintained line numbers, and the author who
    // moves them is the author least likely to notice. The single-file run is
    // what caught it every time — so run THIS file after touching
    // api-gateway's index.ts.
    expect(sites).toEqual([
      'services/api-gateway/src/index.ts:846 express.json (via mockBodyParser)',
      'services/api-gateway/src/index.ts:859 express.json (via mockBodyParser)',
      'services/api-gateway/src/index.ts:892 express.json (via mockBodyParser)',
    ]);
  });

  it('CONTROL — the three declared sites include the one that is NOT mock-gated', () => {
    // 846 and 859 sit behind ENABLE_MOCK_ENDPOINTS; 892 is the
    // createVerificationRoutes factory argument, live wherever the gateway
    // runs. (Before KS-858's +14 shift these read 840, 853 and 886; after it
    // 854, 867 and 900; KS-1126 re-measured them at 846, 859 and 892 after
    // #951's -8.) An earlier
    // draft of the positional rule counted only `app.<method>(...)` arguments
    // and silently dropped the factory one — narrowing the leg to 2 while
    // looking like a clean 3 -> 2 improvement. A parser handed to a router
    // FACTORY is reachable exactly as one handed to a route.
    const live = SCANS.find((s) => s.rel === 'services/api-gateway/src/index.ts')
      ?.postGuardParserSites.map((x) => x.line);
    // KS-1126: 900 -> 892 (the same factory-argument statement, read back).
    expect(live).toContain(892);
  });
});


// ===========================================================================
// KS-800 — LEG E and LEG F.
//
// LEG C/D above walk `services/*/src/{index,app,server}.ts` and, crucially,
// `scan()` returns null for any file with no guard mount. That is TWO blind
// spots, and the KS-781 re-gate walked through both:
//
//   1. A service that mounts a body parser and NO guard at all is not a
//      failure of LEG C — it is INVISIBLE to it. `demo-service` and
//      `mcp-server` were in exactly that state while every assertion above
//      was green. LEG E makes absence a failure.
//
//   2. A parser reached by being passed as a route HANDLER inside a router
//      module is not in the entrypoint corpus at all. `routes/admin.ts:535`
//      hands one to 19 routes. A router module is not an entrypoint, so
//      widening the corpus to `{index,app,server}.ts` — which is what the
//      previous fix did — still could not see it. LEG F widens to every
//      TypeScript file under a service's `src/`.
//
// ⚠ THE INSTRUMENT MATTERS, AND A REGEX IS THE WRONG ONE. Grepping raw lines
// for `express.json(` across all service files returns SEVEN files; only THREE
// are real. The other four are prose — `contentType.ts`, `auth.openapi.ts`,
// `routes/mfa.ts` and `referral/middleware/errorHandler.ts` each DISCUSS
// `express.json()` in a doc comment. A guard that fires on four healthy files
// is a guard someone switches off. So these legs parse the TypeScript and walk
// the AST for real CallExpressions; comments cannot produce one by
// construction. `discriminates between a comment and a call` below is the
// control that proves the walk actually has that property rather than being
// asserted to.
// ===========================================================================


const SERVICES_DIR = join(DEV_ROOT, 'services');
const SKIP_DIRS = new Set(['node_modules', 'dist', '__tests__', 'coverage']);

function tsFilesUnder(dir: string, out: string[] = []): string[] {
  if (!existsSync(dir)) return out;
  for (const e of readdirSync(dir, { withFileTypes: true })) {
    const full = join(dir, e.name);
    if (e.isDirectory()) {
      if (!SKIP_DIRS.has(e.name)) tsFilesUnder(full, out);
    } else if (e.name.endsWith('.ts') && !e.name.endsWith('.d.ts')) {
      out.push(full);
    }
  }
  return out;
}

/**
 * Real parser calls in a file, by 1-based line.
 *
 * KS-800 item 3: this reads `parserCallName` — the SAME predicate LEG C/D now
 * use — so LEG E and LEG F cannot drift from the ordering legs. It also
 * inherits KS-802's widening for free (`raw`, `text`, `bodyParser.*`), which
 * was measured inert on this tree: 24 services with a parser before and after,
 * the same two router-module sites.
 */
export function parserCallLines(source: string, fileName = 'x.ts'): number[] {
  const sf = ts.createSourceFile(fileName, source, ts.ScriptTarget.Latest, true);
  const bindings = moduleBindings(sf);
  const lines: number[] = [];
  const visit = (n: ts.Node): void => {
    if (parserCallName(n, bindings)) {
      lines.push(sf.getLineAndCharacterOfPosition(n.getStart(sf)).line + 1);
    }
    ts.forEachChild(n, visit);
  };
  visit(sf);
  return lines;
}

/** Real `rejectNulBytes()` / `rejectControlBytes()` / `mountBodyParsers()` calls, by 1-based line. */
export function guardCallLines(source: string, fileName = 'x.ts'): number[] {
  const sf = ts.createSourceFile(fileName, source, ts.ScriptTarget.Latest, true);
  const bindings = moduleBindings(sf);
  const lines: number[] = [];
  const visit = (n: ts.Node): void => {
    if (guardCallName(n, bindings)) {
      lines.push(sf.getLineAndCharacterOfPosition(n.getStart(sf)).line + 1);
    }
    ts.forEachChild(n, visit);
  };
  visit(sf);
  return lines;
}

interface SvcScan {
  service: string;
  /** Absolute path to the unit's `src/`, carried rather than rebuilt from a
   *  root — rebuilding it as `join(SERVICES_DIR, service, 'src')` produces
   *  `services/connectors/whatsapp-bot` the moment a unit is not a service. */
  src: string;
  parserFiles: string[];
  guardFiles: string[];
}

/** Every deployable unit under the declared roots — `<root>/<name>`. */
const DEPLOYABLE_UNITS: Array<{ unit: string; src: string }> = ENTRYPOINT_ROOTS.flatMap((root) => {
  const dir = join(DEV_ROOT, root);
  if (!existsSync(dir)) return [];
  return readdirSync(dir, { withFileTypes: true })
    .filter((e) => e.isDirectory())
    .map((e) => ({
      // `services/x` keeps its bare name so declared sets and messages read as
      // before; anything else is prefixed by its root, so `connectors/x` cannot
      // be mistaken for a service.
      unit: root === 'services' ? e.name : `${root}/${e.name}`,
      src: join(dir, e.name, 'src'),
    }));
}).sort((a, b) => a.unit.localeCompare(b.unit));

const SERVICE_SCANS: SvcScan[] = DEPLOYABLE_UNITS
  .map(({ unit: service, src }) => {
    const parserFiles: string[] = [];
    const guardFiles: string[] = [];
    for (const f of tsFilesUnder(src)) {
      const text = readFileSync(f, 'utf8');
      if (parserCallLines(text, f).length) parserFiles.push(relative(src, f));
      if (guardCallLines(text, f).length) guardFiles.push(relative(src, f));
    }
    return { service, src, parserFiles: parserFiles.sort(), guardFiles: guardFiles.sort() };
  })
  .filter((s) => s.parserFiles.length || s.guardFiles.length);

/**
 * LEG F's exact set: real parser calls that live OUTSIDE
 * `{index,app,server}.ts`. Each is reachable as a route handler, so the global
 * guard — which runs at `app.use` time — never sees the body it parses.
 *
 * Both entries are the api-gateway and both are tracked on KS-800. Do not widen
 * this silently: a new entry means a new unguarded body.
 */
/**
 * KS-800 F-07 — this set now bounds EXPOSURE, not declarations.
 *
 * It used to count the parser CALL: `admin.ts: 1`. The gate added a 20th admin
 * route onto that already-declared parser and the suite stayed 47/47 green —
 * the declaration had not changed, so nothing moved. One call, nineteen
 * unguarded routes, and the number that bounded it could not tell the
 * difference. LEG D, guarding the same class one file away, counts REFERENCES
 * and would have moved: two legs, one class, inconsistent granularity, and the
 * looser one was guarding the larger surface.
 *
 * So the number is the count of ROUTES that carry the parser. Adding a route to
 * an existing parser is exactly the change that widens exposure, and it now
 * costs an edit here.
 *
 * Measured at this head: admin.ts hands one `express.json({ limit: '1mb' })` to
 * **19** routes; proxy.ts's parser reaches **1**.
 */
/**
 * KS-828 — the declaration carries TWO facts per file, not one.
 *
 * `routes` is F-07's count. `guarded` is new: whether every WRAPPER that feeds
 * those routes reaches a control-byte guard call inside its own body. After
 * KS-815 the admin wrapper carries the parser AND the guard, and LEG F counted
 * only the routes the parser reaches — so the guard could leave the wrapper
 * with the suite green (the #826 re-gate's F-05; re-measured at the tip
 * 2026-09-13: `controlByteGuard(req, res, next);` -> `next();` left ks781
 * unchanged). Now that edit reds here.
 *
 * `'none'` is the third state, for a parser handed to a route with no wrapper
 * at all (proxy.ts: `express.json()` inline on `router.post('/api/workflows')`,
 * 0 guard calls in the file). Nothing in that file guards the route and
 * nothing in it can — there is no wrapper body to inspect — so `false` would
 * red it for the wrong reason. Whether that route is guarded is decided at the
 * app level (`/api/workflows` is not on `proxyPaths`, so the global pair runs
 * first): LEG C/D's claim, not LEG F's. Derived the same way as declared, so a
 * wrapper appearing in proxy.ts later flips it to `true`/`false` and costs an
 * edit here.
 */
interface RouterParserSite {
  routes: number;
  guarded: boolean | 'none';
}

const ROUTER_MODULE_PARSER_SITES: Record<string, RouterParserSite> = {
  'api-gateway/routes/admin.ts': { routes: 19, guarded: true },
  'api-gateway/routes/proxy.ts': { routes: 1, guarded: 'none' },
};

/** Route methods a parser can be handed to as a handler. */
const ROUTE_METHODS = [
  'get', 'post', 'put', 'patch', 'delete', 'all', 'options', 'head',
] as const;

/**
 * How many ROUTES in this file carry a body parser as a handler — the parser
 * itself, or a local symbol bound to one — and whether the WRAPPERS feeding
 * them reach a guard (KS-828). One walk, one encoding: `parserRouteCount` and
 * `routerParserSites` are two readings of this analysis, so they cannot drift.
 */
function routerParserAnalysis(source: string, fileName: string): RouterParserSite {
  const sf = ts.createSourceFile(fileName, source, ts.ScriptTarget.Latest, true);
  const b = moduleBindings(sf);
  const syms = new Set<string>();
  // KS-828 — locals bound to a guard factory call (`const g = rejectControlBytes()`),
  // collected the way parser-bound locals are: the wrapper invokes the LOCAL,
  // and `guardCallLines` sees only the factory call that binds it.
  const guardSyms = new Set<string>();
  // KS-828 — the body of every symbol the wrapper pass admits, so the guard
  // walk below inspects exactly the wrappers that feed routes.
  const wrapperBodies = new Map<string, ts.Node>();
  const collect = (n: ts.Node): void => {
    if (ts.isVariableDeclaration(n) && ts.isIdentifier(n.name) && n.initializer && parserCallName(n.initializer, b)) {
      syms.add(n.name.text);
    }
    if (ts.isVariableDeclaration(n) && ts.isIdentifier(n.name) && n.initializer && guardCallName(n.initializer, b)) {
      guardSyms.add(n.name.text);
    }
    ts.forEachChild(n, collect);
  };
  collect(sf);

  // KS-816 — A WRAPPER AROUND A PARSER IS A PARSER.
  //
  // The set above knows only symbols bound DIRECTLY to a parser call. Wrap the
  // parser to run a guard after it — `const wrapped = (req, res, next) =>
  // rawBodyParser(req, res, () => guard(req, res, next))` — hand `wrapped` to
  // the routes, and every route carrying it counted as ZERO. That is not a
  // hypothetical: it is what nineteen parsing admin routes read as.
  //
  // A symbol bound to a function that invokes a parser (or another such
  // wrapper) is therefore a parser handler too. Fixed point, so wrapping the
  // wrapper does not move the blind spot one level out.
  for (let pass = 0; pass <= 32; pass += 1) {
    let grew = false;
    const addWrappers = (n: ts.Node): void => {
      // F-QA-04: ONE rule, ONE encoding. `analyseSource` already accepted a
      // FunctionDeclaration wrapper while this accepted only a const-bound
      // arrow/function expression — so the same wrapper written as
      // `function wrapped(req, res, next) { ... }` and handed to routes counted
      // ZERO. #826's wrapper is an arrow, so LEG F read 19 by luck; rewriting it
      // as a declaration would have returned it to zero in silence.
      let name: string | undefined;
      let body: ts.Node | undefined;
      if (
        ts.isVariableDeclaration(n) &&
        ts.isIdentifier(n.name) &&
        n.initializer &&
        (ts.isArrowFunction(n.initializer) || ts.isFunctionExpression(n.initializer))
      ) {
        name = n.name.text;
        body = n.initializer.body;
      } else if (ts.isFunctionDeclaration(n) && n.name && n.body) {
        name = n.name.text;
        body = n.body;
      }
      if (name !== undefined && body !== undefined && !syms.has(name)) {
        let hit = false;
        const walk = (m: ts.Node): void => {
          if (hit) return;
          if (parserCallName(m, b)) { hit = true; return; }
          if (ts.isIdentifier(m) && syms.has(m.text)) { hit = true; return; }
          ts.forEachChild(m, walk);
        };
        walk(body);
        if (hit) { syms.add(name); wrapperBodies.set(name, body); grew = true; }
      }
      ts.forEachChild(n, addWrappers);
    };
    addWrappers(sf);
    if (!grew) break;
  }
  // KS-828 — which wrappers reach a guard INSIDE their own body: a guard-bound
  // local invoked there, an inline factory call, or another wrapper that is
  // itself guarded. Fixed point, same shape as the parser reach above. The
  // binding `const g = rejectControlBytes()` sits OUTSIDE the wrapper and does
  // not qualify it on its own — F-09: a guard MENTIONED is not a guard MOUNTED.
  const guardedWrappers = new Set<string>();
  for (let pass = 0; pass <= 32; pass += 1) {
    let grew = false;
    for (const [name, body] of wrapperBodies) {
      if (guardedWrappers.has(name)) continue;
      let hit = false;
      const walk = (m: ts.Node): void => {
        if (hit) return;
        if (guardCallName(m, b)) { hit = true; return; }
        if (ts.isIdentifier(m) && (guardSyms.has(m.text) || guardedWrappers.has(m.text))) { hit = true; return; }
        ts.forEachChild(m, walk);
      };
      walk(body);
      if (hit) { guardedWrappers.add(name); grew = true; }
    }
    if (!grew) break;
  }
  let routes = 0;
  // KS-828 — the wrappers that actually feed a route; `guarded` is about
  // these, not about every wrapper declared in the file.
  const feeding = new Set<string>();
  const visit = (n: ts.Node): void => {
    if (
      ts.isCallExpression(n) &&
      ts.isPropertyAccessExpression(n.expression) &&
      (ROUTE_METHODS as readonly string[]).includes(n.expression.name.text)
    ) {
      let carries = false;
      for (const raw of n.arguments) {
        const a = ts.isSpreadElement(raw) ? raw.expression : raw;
        if (parserCallName(a, b) !== null || (ts.isIdentifier(a) && syms.has(a.text))) {
          carries = true;
          if (ts.isIdentifier(a) && wrapperBodies.has(a.text)) feeding.add(a.text);
        }
      }
      if (carries) routes += 1;
    }
    ts.forEachChild(n, visit);
  };
  visit(sf);
  const guarded: boolean | 'none' =
    feeding.size === 0 ? 'none' : [...feeding].every((w) => guardedWrappers.has(w));
  return { routes, guarded };
}

/** F-07's reading of the analysis: the number of routes a parser reaches. */
function parserRouteCount(source: string, fileName: string): number {
  return routerParserAnalysis(source, fileName).routes;
}

/** KS-828's reading: routes AND whether the feeding wrappers reach a guard. */
function routerParserSites(source: string, fileName: string): RouterParserSite {
  return routerParserAnalysis(source, fileName);
}

/**
 * KS-800 F-08 — the EXACT set of units that parse request bodies.
 *
 * The non-vacuity companion used to be `toBeGreaterThanOrEqual(20)` against a
 * measured 24 — four services of slack. A partial extractor break affecting up
 * to four units passes that floor while LEG E's main assertion goes vacuous for
 * exactly those units: they drop out of the corpus, so "no unguarded units"
 * becomes true by their absence. Every other leg in this file uses an exact set
 * or an exact count; this one alone used an inequality, and it was the one
 * guarding against the instrument breaking.
 */
const UNITS_WITH_A_BODY_PARSER = [
  'analytics',
  'anchoring',
  'api-gateway',
  'auth',
  'billing',
  'connectors/whatsapp-bot',
  'demo-service',
  'governance',
  'guardian',
  'kyc',
  'm365-integration',
  'mcp-server',
  'nft-certificate',
  'originate',
  'prism',
  'queue',
  'referral',
  'security',
  'staking',
  'tenant-provisioning',
  'timestamping',
  'tokenisation',
  'transfer',
  'vc-issuer',
  'wallet-connector',
];

describe('KS-800 LEG E — a service that parses bodies must mount the guard (absence is a failure, not a silence)', () => {
  it('every unit with a real body parser MOUNTS the guard on its app', () => {
    // KS-800 F-09. This used to ask whether a guard call appeared ANYWHERE under
    // `src/`, which is a different question from whether one is mounted. The
    // gate moved queue's guard onto a sub-router the parsed body never
    // traverses — `const r = express.Router(); r.use(rejectNulBytes());
    // app.use(r);` — and LEG E stayed green. A guard in dead code, in a test
    // helper, or on an unrelated router satisfied it identically. The only thing
    // that caught that tamper was LEG C's corpus COUNT, i.e. a size assertion
    // standing in for a placement one.
    //
    // `SCANS` is now the authority, and it is built from `analyseSource`, which
    // records a guard position only when the call is mounted through
    // `app.use(...)` (see `classify`). So this asks the placement question
    // directly.
    const mounted = new Set(SCANS.map((s) => s.rel.split('/src/')[0]));
    const unguarded = SERVICE_SCANS.filter((s) => s.parserFiles.length)
      .map((s) => s.service)
      .filter((unit) => {
        const prefix = unit.includes('/') ? unit : `services/${unit}`;
        return !mounted.has(prefix);
      });
    expect(
      unguarded,
      'These units parse request bodies and mount NO control-byte guard ON THE APP. A guard ' +
        'merely PRESENT somewhere under src/ — on a sub-router the body never traverses, in dead ' +
        'code, in a helper — does not count and never did; it only looked like it did (KS-800 ' +
        'F-09). That is how demo-service, mcp-server and connectors/whatsapp-bot stayed ' +
        'unguarded while every other leg here was green.',
    ).toEqual([]);
  });

  it('the scan is not vacuous — the set of parsing units is EXACT, not a floor', () => {
    // F-08: if the extractor partially breaks, the missing units show up here by
    // name instead of hiding inside four units of slack under a >= 20 floor.
    const actual = SERVICE_SCANS.filter((s) => s.parserFiles.length)
      .map((s) => s.service)
      .sort();
    expect(actual).toEqual([...UNITS_WITH_A_BODY_PARSER].sort());
  });
});

describe('KS-800 LEG F — parsers in router modules are a declared, bounded set', () => {
  it('no service has grown an undeclared parser outside its entrypoint', () => {
    const actual: Record<string, RouterParserSite> = {};
    for (const s of SERVICE_SCANS) {
      for (const rel of s.parserFiles) {
        const full = join(s.src, rel);
        const text = readFileSync(full, 'utf8');
        // Structural, not by filename: a file that creates the app is an
        // entrypoint and LEG C owns its ordering. Excluding by name here is what
        // let `mcp-server/src/http-server.ts` look like a router module.
        if (createsExpressApp(text, full)) continue;
        // F-07: routes carrying the parser, not parser declarations.
        // KS-828: AND whether the wrappers feeding them reach a guard call.
        actual[`${s.service}/${rel}`] = routerParserSites(text, full);
      }
    }
    expect(
      actual,
      'A body parser outside the service entrypoint reaches a different NUMBER OF ROUTES than ' +
        'declared — typically passed as a route handler, which the global guard never sees — ' +
        'OR the wrapper feeding those routes no longer reaches a control-byte guard call ' +
        '(KS-828: `guarded` is derived from the wrapper BODY; `false` means the parser runs ' +
        'and nothing after it inspects the body). The count is ROUTES, not parser ' +
        'declarations (KS-800 F-07): adding a route to an existing parser widens the ' +
        'unguarded surface and must cost an edit here. Mount it before the guard, put the ' +
        'guard back inside the wrapper, or update ROUTER_MODULE_PARSER_SITES with a ticket.',
    ).toEqual(ROUTER_MODULE_PARSER_SITES);
  });
});

describe('KS-828 — LEG F sees the guard LEAVE a wrapped router (the wrapper body must reach a guard call)', () => {
  // KS-828. After KS-815 the two api-gateway wrappers carry the parser AND the
  // guard. LEG F counted the routes the PARSER reaches, so dropping the guard
  // call out of a wrapper — parser kept — left packages/shared 118/118 green
  // (measured by the #826 re-gate as F-05; re-measured 2026-09-13 at the tip:
  // `controlByteGuard(req, res, next);` -> `next();` in admin.ts, ks781
  // unchanged). The thing LEG F measured was exactly the thing the tamper did
  // not disturb. `guarded` is derived from the wrapper BODY: a local bound to a
  // guard factory call and INVOKED inside the wrapper, an inline factory call,
  // or another wrapper that is itself guarded (fixed point) — the way
  // `parserRouteCount` follows parser-bound locals through `syms`. The factory
  // call that BINDS the local (`const g = rejectControlBytes()`) is outside the
  // wrapper and does not count on its own: F-09's distinction, a guard
  // MENTIONED is not a guard MOUNTED.
  const IMPORTS =
    "import express from 'express';\n" +
    "import { Router } from 'express';\n" +
    "import { rejectControlBytes } from '@secuura/shared';\n";
  const wrapperModule = (inside: string, before = ''): string =>
    IMPORTS +
    'export function make() {\n' +
    '  const router = Router();\n' +
    before +
    "  const raw = express.json({ limit: '1mb' });\n" +
    '  const wrapped = (req: any, res: any, next: any) => {\n' +
    '    raw(req, res, (err?: unknown) => {\n' +
    '      if (err) { next(err); return; }\n' +
    inside +
    '    });\n' +
    '  };\n' +
    "  router.post('/a', wrapped, (_q: any, s: any) => s.end());\n" +
    "  router.put('/b', wrapped, (_q: any, s: any) => s.end());\n" +
    '  return router;\n' +
    '}\n';

  it('W1 🔴 a wrapper that carries the parser but NOT the guard reads guarded: false — the ticket\'s regression', () => {
    const src = wrapperModule('      next();\n');
    expect(routerParserSites(src, 'x.ts')).toEqual({ routes: 2, guarded: false });
  });

  it('W2 CONTROL — the same wrapper invoking a guard-bound local reads guarded: true', () => {
    const src = wrapperModule('      g(req, res, next);\n', '  const g = rejectControlBytes();\n');
    expect(routerParserSites(src, 'x.ts')).toEqual({ routes: 2, guarded: true });
  });

  it('W3 CONTROL — an inline factory call inside the wrapper is a guard too', () => {
    const src = wrapperModule('      rejectControlBytes()(req, res, next);\n');
    expect(routerParserSites(src, 'x.ts')).toEqual({ routes: 2, guarded: true });
  });

  it('W4 — a guard bound at module level but never invoked inside the wrapper does NOT count (F-09)', () => {
    // The binding alone is a MENTION. Only its invocation inside the wrapper
    // that feeds the routes mounts it on those routes.
    const src = wrapperModule('      next();\n', '  const g = rejectControlBytes();\n');
    expect(routerParserSites(src, 'x.ts')).toEqual({ routes: 2, guarded: false });
  });

  it('W5 — a parser handed to routes with NO wrapper reads guarded: \'none\' (proxy.ts\'s shape)', () => {
    // Nothing in the file guards it and nothing in the file can — there is no
    // wrapper body to inspect. Whether that route is guarded is decided at the
    // app level, which is LEG C/D's claim, not LEG F's.
    const src =
      IMPORTS +
      'const router = Router();\n' +
      "router.post('/w', express.json(), (_q: any, s: any) => s.end());\n";
    expect(routerParserSites(src, 'x.ts')).toEqual({ routes: 1, guarded: 'none' });
  });
});

describe('KS-800 — the instrument itself: the AST walk discriminates a call from a comment', () => {
  // Without this control, LEG E and LEG F passing would be consistent with an
  // extractor that silently returns [] for everything.
  const REAL = `import express from 'express';\nconst app = express();\napp.use(express.json());\n`;
  const COMMENTED = `// app.use(express.json()); - discussed, not mounted\n/* express.urlencoded({ extended: true }) */\nconst x = 1;\n`;

  it('finds a real express.json() call', () => {
    expect(parserCallLines(REAL)).toEqual([3]);
  });

  it('finds NOTHING in a file that only mentions parsers in comments', () => {
    expect(parserCallLines(COMMENTED)).toEqual([]);
  });

  it('the four files that only DISCUSS express.json() are really clean', () => {
    // These are the false positives a raw-text grep produces. Named explicitly:
    // if one of them ever mounts a parser for real, this flips and LEG F catches it.
    const proseOnly = [
      'api-gateway/src/middleware/contentType.ts',
      'auth/src/auth.openapi.ts',
      'auth/src/routes/mfa.ts',
      'referral/src/middleware/errorHandler.ts',
    ];
    for (const rel of proseOnly) {
      const full = join(SERVICES_DIR, rel);
      expect(existsSync(full), `${rel} moved — update this list`).toBe(true);
      const text = readFileSync(full, 'utf8');
      expect(parserCallLines(text, full), `${rel} now mounts a real parser`).toEqual([]);
      // control: the text really does mention it, so the [] above is the AST
      // discriminating rather than the file having become unrelated.
      expect(/express\.(json|urlencoded)\s*\(/.test(text), `${rel} no longer mentions it`).toBe(true);
    }
  });

  it('finds the guard call in a service that mounts it', () => {
    expect(guardCallLines(`app.use(rejectNulBytes());`).length).toBe(1);
    expect(guardCallLines(`// app.use(rejectNulBytes());`).length).toBe(0);
  });
});


// ---------------------------------------------------------------------------
// KS-800 LEG G — the structural fix behaves, and the helper is not decorative.
//
// LEG C/E/F make a wrong order impossible to land unnoticed. mountBodyParsers()
// makes it harder to write in the first place: the order lives in one place
// instead of in 24 services' memories. This leg proves the helper produces the
// FIXED behaviour, using the same real-socket harness as LEG A — an export whose
// ordering is only asserted by reading it is the convention it replaces.
// ---------------------------------------------------------------------------

describe('KS-800 LEG G — mountBodyParsers() produces the fixed order', () => {
  let base: string;
  let server: Server;
  beforeAll(async () => {
    const app = express();
    mountBodyParsers(app);
    app.post('/probe', (req, res) => {
      res.status(200).json({ reached: true, body: req.body });
    });
    ({ base, server } = await listen(app));
  });
  afterAll(async () => {
    await close(server);
  });

  it('refuses a NUL in a JSON body', async () => {
    expect((await postJson(base, `ab${NUL}cd`)).status).toBe(400);
  });

  it('refuses the SAME NUL in a form body — the case a hand-mounted guard got wrong', async () => {
    const r = await postForm(base, `ab${NUL}cd`);
    expect(r.status).toBe(400);
    expect(r.body?.error?.code).toBe('VALIDATION_ERROR');
  });

  it('refuses BEL in a form body', async () => {
    expect((await postForm(base, `ab${BEL}cd`)).status).toBe(400);
  });

  it('lets a clean form body through — not a blanket refusal', async () => {
    const r = await postForm(base, 'abcd');
    expect(r.status).toBe(200);
    expect(r.body?.body?.state).toBe('abcd');
  });

  it('lets a clean JSON body through', async () => {
    const r = await postJson(base, 'abcd');
    expect(r.status).toBe(200);
    expect(r.body?.body?.state).toBe('abcd');
  });

  it('honours urlencoded:false without breaking the guard on JSON', async () => {
    const app = express();
    mountBodyParsers(app, { urlencoded: false });
    app.post('/probe', (req, res) => res.status(200).json({ body: req.body }));
    const { base: b2, server: s2 } = await listen(app);
    try {
      expect((await postJson(b2, `x${NUL}y`)).status).toBe(400);
      expect((await postJson(b2, 'xy')).status).toBe(200);
    } finally {
      await close(s2);
    }
  });
});


// ---------------------------------------------------------------------------
// KS-800 LEG H — the mount points are reachable from the package ROOT, which is
// the only specifier consumers use.
//
// LEG G proved mountBodyParsers() behaves. It proved it over `../middleware`, an
// intra-package relative path, and every leg in this file could have stayed green
// while the helper was unreachable by every consumer in the repo — which is
// exactly what shipped: `mountBodyParsers` was added to `src/middleware/index.ts`
// and never added to `src/index.ts`'s named re-export list. Measured at the head
// that shipped it: **143 import lines across 130 files under `services/` use
// `from '@secuura/shared'`; 0 use `'@secuura/shared/middleware'`** (`git ls-files`
// over tracked sources, so build output cannot inflate it; 13 other subpaths ARE
// used, which is the control proving the predicate can return non-zero).
//
// The barrel is a DECLARED named list, not `export * from './middleware'`, so a
// new mount point is reachable only if someone remembers to add it. That is the
// class this leg closes: a helper is not shipped until a consumer can import it.
// ---------------------------------------------------------------------------

/**
 * Every middleware export a SERVICE is meant to call. Declared, not inferred —
 * adding a member is the deliberate act of making it part of the platform's
 * public surface, and each carries the reason it is on the list.
 */
const SERVICE_FACING_MOUNTS = [
  ['rejectNulBytes', 'KS-471 compatibility alias — the name 22 services already mount'],
  ['rejectControlBytes', 'KS-472 — the guard itself, the wider class'],
  ['findNulBytePath', 'used directly by services validating their own payloads'],
  ['findControlBytePath', 'ditto, wider class'],
  ['mountBodyParsers', 'KS-800 — parsers + guard in the only correct order'],
] as const;

describe('KS-800 LEG H — every service-facing mount point is exported from the package root', () => {
  let root: Record<string, unknown>;
  let middleware: Record<string, unknown>;

  beforeAll(async () => {
    // The root barrel, imported the way a service imports `@secuura/shared`.
    // Dynamic so a barrel-load failure surfaces as THIS leg failing rather than
    // taking the whole file down with it.
    root = (await import('../index')) as unknown as Record<string, unknown>;
    middleware = (await import('../middleware')) as unknown as Record<string, unknown>;
  });

  it.each(SERVICE_FACING_MOUNTS)(
    '`%s` is reachable from the package root (%s)',
    async (name) => {
      expect(
        typeof root[name],
        `@secuura/shared does not export ${name}. It is defined in src/middleware/index.ts ` +
          `but missing from src/index.ts's named re-export list, so no consumer can reach it ` +
          `— 143 service import lines use the package root and 0 use the ./middleware subpath.`,
      ).toBe('function');

      // Same binding, not a lookalike re-exported under the same name.
      expect(root[name]).toBe(middleware[name]);
    },
  );
});

// ===========================================================================
// KS-800 F-03 + F-16 — THE TWO SHARED MOUNT APIS THE GUARD COULD NOT SEE
//
// F-03 is the sharp one because the invisible helper is the one THIS branch
// introduces and the follow-up ticket migrates 24 services onto. Measured by
// the gate before this fix: a service adopting `mountBodyParsers(app)` left
// LEG C at 23 of 24, and the ONLY signal was `expected 23 to be 24` — a message
// naming neither the service nor the cause, which invites the maintainer to
// edit the 24 down. With the count so "fixed" the suite went 46/46 GREEN with
// that service invisible to LEG C, LEG E and LEG F simultaneously.
//
// These cases assert the recognition itself, on synthetic sources, so they hold
// whether or not any service has adopted either API yet. Measured today: ZERO
// services call either (control: 28 call the guard), so both are latent — and
// latent is exactly when this is cheap to close.
//
// Both ENCODINGS are asserted, not just one. This file recognises the same fact
// twice — by regex for LEG C/D, through the TypeScript AST for LEG E/F — and a
// fix applied to one encoding while the other still reads the old list is the
// exact shape of the defect being closed here.
// ===========================================================================
const AT = (src: string) => analyseSource(src, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts');

describe('KS-800 F-03 — mountBodyParsers is both a guard mount and a parser mount', () => {
  // These used to assert that the regex encoding and the AST encoding agreed.
  // There is now ONE encoding (KS-800 item 3), so they assert the predicate
  // itself and — more usefully — the ORDERING property, positionally.
  it('is seen as a guard mount', () => {
    expect(guardCallLines('import x from "y";\nmountBodyParsers(app);\n')).toEqual([2]);
  });

  it('is seen as a parser mount', () => {
    expect(parserCallLines('mountBodyParsers(app);\n')).toEqual([1]);
  });

  it('mounting via the helper leaves NO parser after the guard — it mounts the guard last', () => {
    const a = AT('const app = express();\nmountBodyParsers(app);\n');
    expect(a).not.toBeNull();
    expect(a!.lateAppLevel).toEqual([]);
    expect(a!.postGuardParserSites).toEqual([]);
    // and it really was recognised as both, at one position — not skipped
    expect(a!.guardLine).toBe(2);
  });

  it('honours urlencoded:false — read from the AST, not a regex over the line', () => {
    expect(AT('const app = express();\nmountBodyParsers(app);\n')!.urlencodedMounted).toBe(true);
    expect(
      AT('const app = express();\nmountBodyParsers(app, { urlencoded: false });\n')!
        .urlencodedMounted,
    ).toBe(false);
    // The option survives a reflow, which a line-oriented read would not.
    expect(
      AT('const app = express();\nmountBodyParsers(app, {\n  urlencoded: false,\n});\n')!
        .urlencodedMounted,
    ).toBe(false);
  });

  it('CONTROL — a mount that is neither is seen as neither', () => {
    expect(parserCallLines('app.use(helmet());\n')).toEqual([]);
    expect(guardCallLines('app.use(helmet());\n')).toEqual([]);
    expect(AT('const app = express();\napp.use(helmet());\n')).toBeNull();
  });
});

describe('KS-800 F-16 — the request-limits parser factories are parser mounts', () => {
  it.each([...PARSER_FACTORY_NAMES])('%s is a parser mount', (name) => {
    const spread = name.endsWith('Parsers') ? '...' : '';
    expect(parserCallLines(`app.use(${spread}${name}());\n`), `must see ${name}`).toEqual([1]);
  });

  it('a factory parser mounted AFTER the guard is visible as late — the whole point', () => {
    const a = AT(
      'const app = express();\n' +
        'app.use(rejectControlBytes());\n' +
        'app.use(...standardBodyParsers());\n',
    );
    expect(a!.lateAppLevel.map((x) => x.line)).toEqual([3]);
  });
});

// ===========================================================================
// KS-800 item 3 (F-01 / F-02) — THE TWO SHAPES THAT WERE GREEN.
//
// Both were reproduced against the UNFIXED file before this change was
// written: each was inserted after the guard in `services/queue/src/index.ts`
// and the suite stayed at 66/66 green, exactly as predicted, exactly as the
// gate measured at 47/47. The gate also drove both over a real socket and got
// `200` with the NUL reaching the handler. These cases hold the fix in place.
// ===========================================================================
describe('KS-800 F-01 — an INLINE parser handed to a route after the guard is caught', () => {
  const src =
    'const app = express();\n' +
    'app.use(express.json());\n' +
    'app.use(rejectNulBytes());\n' +
    "app.post('/qa-probe', express.json(), handler);\n";

  it('is recorded as a post-guard parser site', () => {
    const a = AT(src)!;
    expect(a.postGuardParserSites.map((x) => x.line)).toEqual([4]);
  });

  it('is NOT miscounted as an app-level mount — LEG C and LEG D stay distinct', () => {
    expect(AT(src)!.lateAppLevel).toEqual([]);
  });

  it('CONTROL — the same route with NO parser argument is clean', () => {
    const clean = src.replace("express.json(), handler", "handler");
    const a = AT(clean)!;
    expect(a.postGuardParserSites).toEqual([]);
    expect(a.lateAppLevel).toEqual([]);
  });

  it('the same parser BEFORE the guard is not a finding — order is what matters', () => {
    const early =
      'const app = express();\n' +
      "app.post('/qa-probe', express.json(), handler);\n" +
      'app.use(rejectNulBytes());\n';
    expect(AT(early)!.postGuardParserSites).toEqual([]);
  });
});

describe('KS-800 F-02 — a MULTI-LINE app.use(...) parser after the guard is caught', () => {
  it('a reflowed mount is caught: the position moves, the line text no longer matters', () => {
    const a = AT(
      'const app = express();\n' +
        'app.use(rejectNulBytes());\n' +
        'app.use(\n' +
        "  express.json({ limit: '10mb' }),\n" +
        ');\n',
    )!;
    expect(a.lateAppLevel.map((x) => x.line)).toEqual([4]);
  });

  it('the SAME mount on one line is caught identically — reflow changes nothing', () => {
    const a = AT(
      'const app = express();\n' +
        'app.use(rejectNulBytes());\n' +
        "app.use(express.json({ limit: '10mb' }));\n",
    )!;
    expect(a.lateAppLevel.length).toBe(1);
  });

  it('CONTROL — the same multi-line mount BEFORE the guard is clean', () => {
    const a = AT(
      'const app = express();\n' +
        'app.use(\n' +
        "  express.json({ limit: '10mb' }),\n" +
        ');\n' +
        'app.use(rejectNulBytes());\n',
    )!;
    expect(a.lateAppLevel).toEqual([]);
  });
});

describe('KS-800 item 3 — the positional instrument itself', () => {
  it('orders two calls on ONE line correctly, which a line number cannot', () => {
    // Same line, guard first: the parser is genuinely after it.
    const a = AT('const app = express();\napp.use(rejectNulBytes()); app.use(express.json());\n')!;
    expect(a.lateAppLevel.map((x) => x.via)).toEqual(['express.json']);
    // Same line, parser first: correct order, nothing to report.
    const b = AT('const app = express();\napp.use(express.json()); app.use(rejectNulBytes());\n')!;
    expect(b.lateAppLevel).toEqual([]);
  });

  it('finds the app whatever it is named — an assumed `app` reads nothing', () => {
    const a = AT(
      'const server = express();\n' +
        'server.use(rejectNulBytes());\n' +
        'server.use(express.json());\n',
    )!;
    expect(a.lateAppLevel.map((x) => x.line)).toEqual([3]);
  });

  it('a parser BOUND to a symbol is counted at its USES, not its declaration', () => {
    const a = AT(
      'const app = express();\n' +
        'app.use(rejectNulBytes());\n' +
        'const p = express.json();\n' +
        "app.post('/a', p, h);\n",
    )!;
    // one site, at line 4 (the use) — not line 3 (the declaration)
    expect(a.postGuardParserSites.map((x) => x.line)).toEqual([4]);
  });

  it('carries KS-802 intent: bodyParser.* and express.raw/text are parsers', () => {
    for (const call of ['express.raw()', 'express.text()', 'bodyParser.json()', 'bodyParser.urlencoded()']) {
      const a = AT(`const app = express();\napp.use(rejectNulBytes());\napp.use(${call});\n`)!;
      expect(a.lateAppLevel.map((x) => x.line), `${call} must be seen as a parser`).toEqual([3]);
    }
  });

  it('CONTROL — a comment cannot produce a position', () => {
    const a = AT(
      'const app = express();\n' +
        'app.use(rejectNulBytes());\n' +
        '// app.use(express.json());\n' +
        '/* app.use(express.urlencoded({ extended: true })); */\n',
    )!;
    expect(a.lateAppLevel).toEqual([]);
    expect(a.postGuardParserSites).toEqual([]);
  });
});

// ===========================================================================
// KS-800 item 4 (F-04) — THE PREDICATE RESOLVES THE IMPORT, NOT THE SPELLING.
//
// The gate's paired probe on a new unguarded body-parsing service:
//   `import express    from 'express'`  -> 1 failure, LEG E named it
//   `import expressLib from 'express'`  -> 47/47 FULLY GREEN, service invisible
// A rename of the import erased a whole unguarded service from every leg.
// ===========================================================================
describe('KS-800 F-04 — an express import is followed by its binding, whatever it is named', () => {
  const app = (bind: string) =>
    `import ${bind} from 'express';\n` +
    `const app = ${bind}();\n` +
    `app.use(${bind}.json());\n`;

  it.each([['express'], ['expressLib'], ['e']])(
    'a default import named `%s` is still the express module',
    (bind) => {
      expect(createsExpressApp(app(bind), 'x.ts'), 'creates the app').toBe(true);
      expect(parserCallLines(app(bind), 'x.ts'), 'mounts a parser').toEqual([3]);
    },
  );

  it('a namespace import is followed too', () => {
    const src = "import * as ex from 'express';\nconst app = ex();\napp.use(ex.json());\n";
    expect(createsExpressApp(src, 'x.ts')).toBe(true);
    expect(parserCallLines(src, 'x.ts')).toEqual([3]);
  });

  it('a require binding is followed too', () => {
    const src = "const ex = require('express');\nconst app = ex();\napp.use(ex.urlencoded());\n";
    expect(createsExpressApp(src, 'x.ts')).toBe(true);
    expect(parserCallLines(src, 'x.ts')).toEqual([3]);
  });

  it('a NAMED parser import is a parser — `import { json } from \'express\'`', () => {
    const src = "import express, { json } from 'express';\nconst app = express();\napp.use(json());\n";
    expect(parserCallLines(src, 'x.ts')).toEqual([3]);
  });

  it('reports the CANONICAL name, so declared sets survive a rename', () => {
    const a = analyseSource(
      "import expressLib from 'express';\n" +
        'const app = expressLib();\n' +
        'app.use(rejectNulBytes());\n' +
        'app.use(expressLib.urlencoded());\n',
      '/x/services/qa/src/index.ts',
      'services/qa/src/index.ts',
    )!;
    expect(a.lateAppLevel.map((x) => x.via)).toEqual(['express.urlencoded']);
    expect(a.urlencodedMounted).toBe(true);
  });

  it('CONTROL — a name is not enough: `express` NOT bound to the module is not a parser', () => {
    // This is the half that proves resolution rather than a wider name match.
    // If the predicate had simply been loosened to accept any `<x>.json()`,
    // this would pass too — and the leg would fire on healthy files.
    const src =
      "import expressLib from 'express';\n" +
      'const express = { json: () => undefined };\n' +
      'const app = expressLib();\n' +
      'app.use(express.json());\n';
    expect(createsExpressApp(src, 'x.ts'), 'expressLib() still creates the app').toBe(true);
    expect(parserCallLines(src, 'x.ts'), '`express.json()` here is NOT the module').toEqual([]);
  });

  it('CONTROL — a module that is not express/body-parser is not a parser source', () => {
    const src = "import bp from 'not-body-parser';\nconst app = bp();\napp.use(bp.json());\n";
    expect(createsExpressApp(src, 'x.ts')).toBe(false);
    expect(parserCallLines(src, 'x.ts')).toEqual([]);
  });
});

// ===========================================================================
// KS-800 item 6 — F-09 (mounted vs mentioned) and F-10 (aliased guard import).
// ===========================================================================
describe('KS-800 F-09 — a guard MENTIONED under src/ is not a guard MOUNTED on the app', () => {
  it('a guard mounted only on a sub-router does not count as mounted', () => {
    // The gate's exact tamper. The parsed body never traverses that router, and
    // the old LEG E — "is there a guard call anywhere in src/?" — was satisfied.
    const a = analyseSource(
      "import express from 'express';\n" +
        "import { rejectNulBytes } from '@secuura/shared';\n" +
        'const app = express();\n' +
        'app.use(express.json());\n' +
        'const bodyRouter = express.Router();\n' +
        'bodyRouter.use(rejectNulBytes());\n' +
        'app.use(bodyRouter);\n',
      '/x/services/qa/src/index.ts',
      'services/qa/src/index.ts',
    );
    expect(a, 'no app-level guard mount, so this file is UNGUARDED, not scannable').toBeNull();
  });

  it('CONTROL — the same guard mounted on the app DOES count', () => {
    const a = analyseSource(
      "import express from 'express';\n" +
        "import { rejectNulBytes } from '@secuura/shared';\n" +
        'const app = express();\n' +
        'app.use(express.json());\n' +
        'app.use(rejectNulBytes());\n',
      '/x/services/qa/src/index.ts',
      'services/qa/src/index.ts',
    );
    expect(a).not.toBeNull();
    expect(a!.guardLine).toBe(5);
    expect(a!.lateAppLevel).toEqual([]);
  });

  it('a guard sitting in dead code is not mounted either', () => {
    const a = analyseSource(
      "import express from 'express';\n" +
        "import { rejectNulBytes } from '@secuura/shared';\n" +
        'const app = express();\n' +
        'app.use(express.json());\n' +
        'const unused = () => rejectNulBytes();\n',
      '/x/services/qa/src/index.ts',
      'services/qa/src/index.ts',
    );
    expect(a).toBeNull();
  });
});

describe('KS-800 F-10 — an ALIASED guard import is still the guard', () => {
  const aliased =
    "import express from 'express';\n" +
    "import { rejectNulBytes as nulGuard } from '@secuura/shared';\n" +
    'const app = express();\n' +
    'app.use(express.json());\n' +
    'app.use(nulGuard());\n';

  it('is recognised as a guard mount, so no service is falsely reported unguarded', () => {
    // Before this, LEG E reported the service "mounts NO control-byte guard
    // anywhere in src/" while the guard was mounted and effective. Fail-safe
    // direction, wrong diagnosis — and a wrong diagnosis on a red is what gets
    // a guard switched off by whoever goes and looks.
    expect(guardCallLines(aliased, 'x.ts')).toEqual([5]);
    const a = analyseSource(aliased, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts');
    expect(a).not.toBeNull();
    expect(a!.guardLine).toBe(5);
  });

  it('ordering still applies under the alias — a parser after it is late', () => {
    const a = analyseSource(
      aliased + 'app.use(express.urlencoded());\n',
      '/x/services/qa/src/index.ts',
      'services/qa/src/index.ts',
    )!;
    expect(a.lateAppLevel.map((x) => x.line)).toEqual([6]);
  });

  it('CONTROL — a name is not enough: an alias of something ELSE is not the guard', () => {
    // Proves resolution rather than a widened name list. `nulGuard` here is a
    // local function, not the shared export.
    const notTheGuard =
      "import express from 'express';\n" +
      "import { somethingElse } from '@secuura/shared';\n" +
      'const nulGuard = () => (_req: unknown, _res: unknown, next: () => void) => next();\n' +
      'const app = express();\n' +
      'app.use(express.json());\n' +
      'app.use(nulGuard());\n';
    expect(guardCallLines(notTheGuard, 'x.ts')).toEqual([]);
    expect(
      analyseSource(notTheGuard, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts'),
    ).toBeNull();
  });
});

describe('KS-800 F-07 — LEG F counts routes, so widening exposure costs an edit', () => {
  const base =
    "import express from 'express';\n" +
    'const router = express.Router();\n' +
    "const bodyParser = express.json({ limit: '1mb' });\n" +
    "router.post('/a', bodyParser, h);\n" +
    "router.post('/b', bodyParser, h);\n";

  it('counts the ROUTES a parser feeds, not the parser declarations', () => {
    expect(parserRouteCount(base, 'x.ts')).toBe(2);
    // one declaration, two routes — the whole point
    expect(parserCallLines(base, 'x.ts').length).toBe(1);
  });

  it('adding a route on the SAME parser moves the number', () => {
    expect(parserRouteCount(base + "router.post('/c', bodyParser, h);\n", 'x.ts')).toBe(3);
  });

  it('CONTROL — routes without a parser are not counted', () => {
    expect(parserRouteCount("const router = express.Router();\nrouter.get('/a', h);\n", 'x.ts')).toBe(0);
  });
});

// ===========================================================================
// KS-800 item 8 — the three test-coverage findings from #818's gate.
//
// F-03 is this file's. #818 widened `PARSER_CALL` to raw/text/bodyParser.* and
// left `PARSER_ASSIGN` on `json|urlencoded`: the two constants encoded ONE
// concept and drifted apart, so `const p = express.raw(…)` mounted after the
// guard was invisible to BOTH LEG C and LEG D while the identical shape with
// `express.json` was caught. Measured then: 32/32 green with a body parser
// mounted after the guard.
//
// Item 3 removed both constants, so the drift is not narrowed — it is
// structurally impossible; there is one predicate. The gate's suggested
// regression ("assert PARSER_ASSIGN and PARSER_CALL recognise the same set")
// cannot be written any more, and the property it was protecting is asserted
// directly instead.
//
// ⚠ The severity is not uniform across the widening, and the sharp half is the
// one the assign-shape hid. For `express.raw` the guard cannot help anyway —
// a Buffer body walks to null (detection, not protection). For `express.text`
// ordering IS protection: measured end-to-end by the gate, a NUL in a
// `text/plain` body is 400 with the parser before the guard and reaches the
// handler with it after.
// ===========================================================================
describe('KS-800 item 8 / #818 F-03 — a parser BOUND to a symbol is caught for every parser kind', () => {
  const mountedAfter = (call: string) =>
    analyseSource(
      "import express from 'express';\n" +
        "import { rejectNulBytes } from '@secuura/shared';\n" +
        'const app = express();\n' +
        `const p = ${call};\n` +
        'app.use(express.json());\n' +
        'app.use(rejectNulBytes());\n' +
        'app.use(p);\n',
      '/x/services/qa/src/index.ts',
      'services/qa/src/index.ts',
    )!;

  it.each([
    ["express.raw({ type: '*/*' })", 'express.raw'],
    ['express.text()', 'express.text'],
    ['express.json()', 'express.json'],
    ['express.urlencoded({ extended: true })', 'express.urlencoded'],
    ['bodyParser.raw()', 'bodyParser.raw'],
    ['bodyParser.text()', 'bodyParser.text'],
  ])('`const p = %s` mounted after the guard is late', (call, canonical) => {
    const a = mountedAfter(call);
    expect(a.lateAppLevel.map((x) => x.via)).toEqual([`${canonical} (via p)`]);
    expect(a.lateAppLevel.map((x) => x.line)).toEqual([7]);
  });

  it('CONTROL — the same binding mounted BEFORE the guard is clean, for every kind', () => {
    for (const call of ['express.raw()', 'express.text()', 'bodyParser.json()']) {
      const a = analyseSource(
        "import express from 'express';\n" +
          "import { rejectNulBytes } from '@secuura/shared';\n" +
          'const app = express();\n' +
          `const p = ${call};\n` +
          'app.use(p);\n' +
          'app.use(rejectNulBytes());\n',
        '/x/services/qa/src/index.ts',
        'services/qa/src/index.ts',
      )!;
      expect(a.lateAppLevel, `${call} before the guard must be clean`).toEqual([]);
    }
  });

  it('the drift the gate found cannot recur — one predicate feeds every leg', () => {
    // Not a restatement of the above: this asserts the LEG C/D path and the
    // LEG E/F path agree on the same source, which is what the two constants
    // failed to do. `parserCallLines` is LEG E/F's entry point; `analyseSource`
    // is LEG C/D's. Both read `parserCallName`.
    const src =
      "import express from 'express';\n" +
      "import { rejectNulBytes } from '@secuura/shared';\n" +
      'const app = express();\n' +
      "const p = express.text();\n" +
      'app.use(rejectNulBytes());\n' +
      'app.use(p);\n';
    expect(parserCallLines(src, 'x.ts'), 'LEG E/F sees the declaration').toEqual([4]);
    const a = analyseSource(src, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts')!;
    expect(a.lateAppLevel.map((x) => x.via), 'LEG C sees the mount').toEqual(['express.text (via p)']);
  });
});


// ===========================================================================
// KS-816 — A PARSER MOUNTED BY A SAME-FILE HELPER.
//
// KS-800 item 3 moved LEG C/D onto source POSITIONS, which closed every shape
// where the parser is lexically where it runs. It does not follow a call INTO
// a local function. So a file can declare the mount above the guard, call it
// below, and every leg reads clean — predicted 0 failures and measured 107/107
// green on the re-gate, with the NUL reaching the handler over a real socket.
//
// The same one hop hides the ROUTE shape from LEG F: a parser bound to a
// symbol, that symbol invoked inside a wrapper handler, and the WRAPPER handed
// to the routes. `parserRouteCount` knew only symbols bound DIRECTLY to a
// parser call, so nineteen parsing routes counted as zero.
//
// Both are one rule: a local function that mounts or invokes a parser IS a
// parser, and the position that matters is where it is CALLED, not where it is
// declared.
//
// The controls below are the load-bearing half, and they guard TWO distinct
// failure modes rather than one — worth stating so nobody deletes one as
// redundant. Measured: (ii) and (iii) redden under OVER-FIRING while (i) stays
// green; (i) reddens only under POSITION-BLINDNESS while (ii) and (iii) stay
// green. An attribution that fired on any helper would satisfy (i) and fail
// (ii)/(iii); one that ignored position would satisfy (ii)/(iii) and fail (i).
// ===========================================================================
describe('KS-816 — a parser mounted by a same-file helper is attributed to the CALL, not the declaration', () => {
  const at = (src: string) =>
    analyseSource(src, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts');

  const HEAD =
    "import express from 'express';\n" +
    "import { rejectNulBytes } from '@secuura/shared';\n" +
    'const app = express();\n';

  it('G-02 — a helper DECLARED above the guard and CALLED below it is late', () => {
    // The declaration is on line 4, the guard on line 5, the call on line 6.
    // Positionally the parser text sits BEFORE the guard; the mount happens
    // after it. Attributing to the declaration is what read this clean.
    const a = at(
      HEAD +
        'function mountMine(app) { app.use(express.json()); }\n' +
        'app.use(rejectNulBytes());\n' +
        'mountMine(app);\n',
    )!;
    expect(a.lateAppLevel.map((x) => x.line)).toEqual([6]);
    expect(a.lateAppLevel.map((x) => x.via)).toEqual(['express.json (via mountMine)']);
  });

  it('the same shape as an arrow bound to a const is the same finding', () => {
    const a = at(
      HEAD +
        'const mountMine = (app) => { app.use(express.urlencoded({ extended: true })); };\n' +
        'app.use(rejectNulBytes());\n' +
        'mountMine(app);\n',
    )!;
    expect(a.lateAppLevel.map((x) => x.line)).toEqual([6]);
    expect(a.lateAppLevel.map((x) => x.via)).toEqual(['express.urlencoded (via mountMine)']);
  });

  it('CONTROL — the same helper CALLED BEFORE the guard is clean', () => {
    // Must pass before and after the fix. If this ever reddens, the fix has
    // stopped being positional and is just flagging every helper.
    const a = at(
      HEAD +
        'function mountMine(app) { app.use(express.json()); }\n' +
        'mountMine(app);\n' +
        'app.use(rejectNulBytes());\n',
    )!;
    expect(a.lateAppLevel).toEqual([]);
  });

  it('CONTROL — a helper that mounts NO parser is not a parser, wherever it is called', () => {
    const a = at(
      HEAD +
        'function mountMine(app) { app.use(helmet()); }\n' +
        'app.use(rejectNulBytes());\n' +
        'mountMine(app);\n',
    )!;
    expect(a.lateAppLevel).toEqual([]);
    expect(a.postGuardParserSites).toEqual([]);
  });

  it('LEG F — a parser reaching routes through a same-file WRAPPER counts those routes', () => {
    const src =
      "import express from 'express';\n" +
      'const router = express.Router();\n' +
      "const rawBodyParser = express.json({ limit: '1mb' });\n" +
      'const wrapped = (req, res, next) => { rawBodyParser(req, res, next); };\n' +
      "router.post('/a', wrapped, h);\n" +
      "router.post('/b', wrapped, h);\n";
    expect(parserRouteCount(src, 'x.ts')).toBe(2);
  });

  it('CONTROL — a wrapper that invokes something else is not a parser', () => {
    const src =
      "import express from 'express';\n" +
      'const router = express.Router();\n' +
      "const rawBodyParser = express.json({ limit: '1mb' });\n" +
      'const wrapped = (req, res, next) => { somethingElse(req, res, next); };\n' +
      "router.post('/a', wrapped, h);\n";
    expect(parserRouteCount(src, 'x.ts')).toBe(0);
  });
});

// ===========================================================================
// KS-816 F-QA-01 — SUPPRESS-WITHOUT-REPLACE. The regression this round exists
// for, and it was introduced by the round before it.
//
// The first cut suppressed every parser site lexically inside a helper that
// mounts a parser, and re-attached it only where that helper is called by a
// bare identifier IN THE SAME FILE. A helper EXPORTED and called from another
// module got nothing back — the parent at least reported the declaration
// position, so the fix made a live service INVISIBLE where the unfixed scanner
// had seen it.
//
// It was not hypothetical: `services/demo-service/src/app.ts` builds its whole
// app inside `export function createApp()` and `index.ts` calls it. Moving
// `express.json()` below `rejectNulBytes()` inside that factory reddened the
// parent and was SILENT at the first cut — 113 passed, no leg moved.
//
// THE RULE NOW: suppress inside helper H only if H actually has an attributing
// call site in this file. Otherwise fall through and emit at the DECLARATION,
// exactly as the parent did — inside a factory the declaration position IS the
// run position, so that is the fail-safe reading.
//
// Reachability of a helper is itself a fixed point: a call at top level
// attributes, and so does a call inside a helper that is itself attributed. A
// call sitting only inside a never-called helper attributes nothing, so that
// case falls through to the declaration too.
// ===========================================================================
describe('KS-816 F-QA-01 — a factory whose caller is in ANOTHER file still reports its parser', () => {
  const at = (src: string) =>
    analyseSource(src, '/x/services/qa/src/app.ts', 'services/qa/src/app.ts');

  const HEAD =
    "import express from 'express';\n" +
    "import { rejectNulBytes } from '@secuura/shared';\n";

  it('(a) a BROKEN factory — parser AFTER the guard, no in-file caller — names the parser line', () => {
    const a = at(
      HEAD +
        'export function createApp() {\n' +
        '  const app = express();\n' +
        '  app.use(rejectNulBytes());\n' +
        '  app.use(express.json());\n' +
        '  return app;\n' +
        '}\n',
    )!;
    expect(a.lateAppLevel.map((x) => x.line)).toEqual([6]);
    expect(a.lateAppLevel.map((x) => x.via)).toEqual(['express.json']);
  });

  it('(b) CONTROL — the correctly-ordered twin of that factory stays clean', () => {
    // Without this, "flag every factory" would satisfy (a).
    const a = at(
      HEAD +
        'export function createApp() {\n' +
        '  const app = express();\n' +
        '  app.use(express.json());\n' +
        '  app.use(rejectNulBytes());\n' +
        '  return app;\n' +
        '}\n',
    )!;
    expect(a.lateAppLevel).toEqual([]);
  });

  it('(c) CONTROL — an in-file-called helper still attributes to the CALL (KS-816 intact)', () => {
    const a = at(
      HEAD +
        'const app = express();\n' +
        'function mountMine(app) { app.use(express.json()); }\n' +
        'app.use(rejectNulBytes());\n' +
        'mountMine(app);\n',
    )!;
    expect(a.lateAppLevel.map((x) => x.line)).toEqual([6]);
    expect(a.lateAppLevel.map((x) => x.via)).toEqual(['express.json (via mountMine)']);
  });
});

// ===========================================================================
// KS-816 F-QA-02 — a helper that mounts TWO parsers must report BOTH.
// The first cut short-circuited on the first site found, so json+urlencoded in
// one helper read as json alone and `urlencodedMounted` went false where the
// parent read true — SERVICES_WITH_URLENCODED would have shrunk silently.
//
// F-QA-04 — one rule, one encoding. `analyseSource` accepted a FunctionDeclaration
// wrapper; `parserRouteCount` accepted only a const-bound arrow/function
// expression. The same wrapper written as `function wrapped(...) {}` and handed
// to routes counted ZERO. #826's wrapper is an arrow, so LEG F read 19 by luck;
// rewriting it as a declaration would have returned it to zero in silence.
// ===========================================================================
describe('KS-816 F-QA-02 / F-QA-04 — every parser in a helper, and every wrapper shape', () => {
  it('F-QA-02 — a helper mounting json AND urlencoded reports both, so urlencoded is still seen', () => {
    const a = analyseSource(
      "import express from 'express';\n" +
        "import { rejectNulBytes } from '@secuura/shared';\n" +
        'const app = express();\n' +
        'function mountBoth(app) {\n' +
        '  app.use(express.json());\n' +
        '  app.use(express.urlencoded({ extended: true }));\n' +
        '}\n' +
        'mountBoth(app);\n' +
        'app.use(rejectNulBytes());\n',
      '/x/services/qa/src/index.ts',
      'services/qa/src/index.ts',
    )!;
    expect(a.urlencodedMounted).toBe(true);
  });

  it('F-QA-04 — a FUNCTION-DECLARATION wrapper handed to routes counts its routes', () => {
    const src =
      "import express from 'express';\n" +
      'const router = express.Router();\n' +
      "const rawBodyParser = express.json({ limit: '1mb' });\n" +
      'function wrapped(req, res, next) { rawBodyParser(req, res, next); }\n' +
      "router.post('/a', wrapped, h);\n" +
      "router.post('/b', wrapped, h);\n";
    expect(parserRouteCount(src, 'x.ts')).toBe(2);
  });
});

// ===========================================================================
// KS-827 — A GUARD MOUNTED OR INVOKED BY A SAME-FILE HELPER.
//
// The mirror of KS-816. `visitGuards` walked the whole file, pushed every
// guard call's own position — including calls inside helper bodies — and took
// the minimum. So the verdict was decided by where a helper is WRITTEN.
//
// The shapes were MEASURED against the unfixed scanner before the fix was
// written, because the direction is not guessable from a code read (one was
// attempted and predicted the wrong direction for M1):
//
//   fixture                                  unfixed        correct
//   M1 declared above, called below          lateAppLevel=1  clean      FALSE RED
//   M2 called above, declared below          lateAppLevel=0  red        FALSE CLEAN
//   M3 never called                          per declaration no guard
//
// M1 and M3 have no fixed direction — move the declaration and the verdict
// moves. So the closure cell is not three shapes pinned separately, it is the
// ORDER-SWAP PAIR: the same program with the helper's declaration moved must
// give the SAME answer. A fix that pins M2 alone would pass a three-shape
// checklist and still leave the verdict position-dependent.
// ===========================================================================
describe('KS-827 — a guard mounted by a same-file helper belongs to the CALL', () => {
  const IMP =
    "import express from 'express';\n" +
    "import { rejectNulBytes } from '@secuura/shared';\n";
  const G = (src: string) =>
    analyseSource(src, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts');

  // The guard reads req.body, so it must be mounted AFTER every parser; a
  // parser mounted after it is what `lateAppLevel` reports.
  it('CONTROL — the inline shapes are unchanged, in both directions', () => {
    const clean = G(IMP + 'const app = express();\napp.use(express.json());\napp.use(rejectNulBytes());\n')!;
    expect(clean.lateAppLevel, 'guard mounted last is clean').toEqual([]);
    const dirty = G(IMP + 'const app = express();\napp.use(rejectNulBytes());\napp.use(express.json());\n')!;
    expect(dirty.lateAppLevel.length, 'a parser after the guard is the defect').toBe(1);
  });

  it('M1 — helper declared ABOVE the parser but called BELOW it is CLEAN (was a false red)', () => {
    const viaParam = G(
      IMP +
        'function mountGuard(app: any) { app.use(rejectNulBytes()); }\n' +
        'const app = express();\napp.use(express.json());\nmountGuard(app);\n',
    )!;
    expect(viaParam.lateAppLevel).toEqual([]);
    const viaClosure = G(
      IMP +
        'const app = express();\nfunction mountGuard() { app.use(rejectNulBytes()); }\n' +
        'app.use(express.json());\nmountGuard();\n',
    )!;
    expect(viaClosure.lateAppLevel).toEqual([]);
  });

  it('M2 — helper called ABOVE the parser but declared BELOW it is RED (was a false clean)', () => {
    const a = G(
      IMP +
        'const app = express();\nmountGuard();\napp.use(express.json());\n' +
        'function mountGuard() { app.use(rejectNulBytes()); }\n',
    )!;
    expect(a.lateAppLevel.length, 'the parser runs after the guard and is unguarded').toBe(1);
  });

  it('M3 — a guard only inside a helper that is NEVER CALLED is no guard at all', () => {
    // Both orders, because the old reading depended on which one you wrote.
    for (const src of [
      IMP + 'const app = express();\nfunction mountGuard() { app.use(rejectNulBytes()); }\napp.use(express.json());\n',
      IMP + 'const app = express();\napp.use(express.json());\nfunction mountGuard() { app.use(rejectNulBytes()); }\n',
    ]) {
      expect(G(src), 'no call, no guard — and the corpus leg reds by name').toBeNull();
    }
  });

  it('🔴 CLOSURE — the order-swap PAIR must AGREE: same program, declaration moved', () => {
    const declaredFirst =
      IMP +
      'function mountGuard(app: any) { app.use(rejectNulBytes()); }\n' +
      'const app = express();\napp.use(express.json());\nmountGuard(app);\n';
    const declaredLast =
      IMP +
      'const app = express();\napp.use(express.json());\nmountGuard(app);\n' +
      'function mountGuard(app: any) { app.use(rejectNulBytes()); }\n';
    const a = G(declaredFirst)!;
    const b = G(declaredLast)!;
    expect(a.lateAppLevel.length, 'declared first').toBe(0);
    expect(b.lateAppLevel.length, 'declared last — the SAME program').toBe(0);
    expect(a.lateAppLevel.length).toBe(b.lateAppLevel.length);
    // Non-vacuity: the pair is only meaningful if this predicate CAN be 1.
    const canFail = G(
      IMP + 'const app = express();\napp.use(rejectNulBytes());\napp.use(express.json());\n',
    )!;
    expect(canFail.lateAppLevel.length, 'the predicate can report 1').toBe(1);
  });

  it('CONTROL — a helper that mounts NO guard is not a guard, wherever it is called', () => {
    const a = G(
      IMP +
        'const app = express();\nfunction addRoutes(app: any) { app.use(helmet()); }\n' +
        'addRoutes(app);\napp.use(express.json());\napp.use(rejectNulBytes());\n',
    )!;
    // The real guard is still the last mount, so the file stays clean; the
    // helper must not have contributed a guard position of its own.
    expect(a.lateAppLevel).toEqual([]);
    const b = G(
      IMP + 'const app = express();\nfunction addRoutes(app: any) { app.use(helmet()); }\naddRoutes(app);\napp.use(express.json());\n',
    );
    expect(b, 'a helper mounting no guard cannot make a guardless file look guarded').toBeNull();
  });

  it('CONTROL — a helper calling a guard-helper is attributed at the OUTER call (depth 2)', () => {
    const a = G(
      IMP +
        'const app = express();\napp.use(express.json());\n' +
        'function inner() { app.use(rejectNulBytes()); }\nfunction outer() { inner(); }\nouter();\n',
    )!;
    expect(a.lateAppLevel, 'the fixed point follows the second hop').toEqual([]);
  });
});

// ===========================================================================
// KS-831 F-QA-A — THE ORDER *INSIDE* A HELPER, WHICH BOTH PREVIOUS FIXES ERASED.
//
// KS-816 moved a helper's parsers to its CALL. KS-827 moved a helper's guard to
// the same call. Individually each was right; together they put the guard and
// the parsers it is supposed to precede on ONE position, and `lateAppLevel` is
// `pos > guardPos` — equal is not greater. So a helper mounting
// guard-then-parser, which is KS-781 LEG B's original defect and the whole
// reason this instrument exists, read CLEAN.
//
// The parent reddened BOTH orders (M1's false red). The head cleaned BOTH.
// Loud became silent, and the silence sat on the broken order.
//
// MEASURED against the unfixed instrument before the fix was written — one
// program in two spellings, which is the sharpest statement of the defect:
//
//   fixture                              unfixed   correct
//   helper  guard-then-parser  (param)    late=0    late=1   FALSE CLEAN
//   helper  parser-then-guard  (param)    late=0    late=0
//   helper  guard-then-parser  (closure)  late=0    late=1   FALSE CLEAN
//   helper  parser-then-guard  (closure)  late=0    late=0
//   inline  guard-then-parser             late=1    late=1   <- same program, LOUD
//   inline  parser-then-guard             late=0    late=0
//
// So the closure cell is the WITHIN-HELPER ORDER PAIR, asserted to DISAGREE —
// the exact mirror of KS-827's order-swap pair, which must AGREE. Both pairs
// live in this file on purpose: a fix that satisfies one by collapsing
// positions breaks the other, and only the two together pin the model.
// ===========================================================================
describe('KS-831 F-QA-A — the order INSIDE a helper decides the verdict, not the call position', () => {
  const IMP =
    "import express from 'express';\n" +
    "import { rejectNulBytes } from '@secuura/shared';\n";
  const G = (src: string) =>
    analyseSource(src, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts');

  const helperParam = (body: string) =>
    IMP + 'const app = express();\n' + `function mountBoth(app: any) { ${body} }\n` + 'mountBoth(app);\n';
  const helperClosure = (body: string) =>
    IMP + 'const app = express();\n' + `function mountBoth() { ${body} }\n` + 'mountBoth();\n';

  const GUARD_FIRST = 'app.use(rejectNulBytes()); app.use(express.json());';
  const PARSER_FIRST = 'app.use(express.json()); app.use(rejectNulBytes());';

  it('a helper mounting GUARD-then-PARSER is RED — the parser it mounts is unguarded', () => {
    const a = G(helperParam(GUARD_FIRST))!;
    expect(a.lateAppLevel.length, 'the parser runs after the guard').toBe(1);
    expect(a.lateAppLevel[0].via).toContain('express.json');
    // The site is still reported at the CALL's line — the ordering is carried
    // by a half-unit, it does not relocate the finding to another line.
    expect(a.lateAppLevel[0].line, 'reported where the helper is called').toBe(a.guardLine);
  });

  it('a helper mounting PARSER-then-GUARD is CLEAN — the guard covers it', () => {
    expect(G(helperParam(PARSER_FIRST))!.lateAppLevel).toEqual([]);
  });

  it('the same two orders through a CLOSURE, not a parameter, read identically', () => {
    expect(G(helperClosure(GUARD_FIRST))!.lateAppLevel.length, 'guard first').toBe(1);
    expect(G(helperClosure(PARSER_FIRST))!.lateAppLevel, 'parser first').toEqual([]);
  });

  it('🔴 CLOSURE — the within-helper order PAIR must DISAGREE (mirror of KS-827, which must AGREE)', () => {
    const guardFirst = G(helperParam(GUARD_FIRST))!;
    const parserFirst = G(helperParam(PARSER_FIRST))!;
    expect(guardFirst.lateAppLevel.length, 'guard-then-parser').toBe(1);
    expect(parserFirst.lateAppLevel.length, 'parser-then-guard').toBe(0);
    expect(
      guardFirst.lateAppLevel.length === parserFirst.lateAppLevel.length,
      'the two within-helper orders are DIFFERENT programs and must not agree',
    ).toBe(false);
  });

  it('🔴 ONE PROGRAM, TWO SPELLINGS — inline and via-helper must give the SAME answer', () => {
    const inlineGuardFirst = G(
      IMP + 'const app = express();\napp.use(rejectNulBytes());\napp.use(express.json());\n',
    )!;
    const inlineParserFirst = G(
      IMP + 'const app = express();\napp.use(express.json());\napp.use(rejectNulBytes());\n',
    )!;
    expect(
      G(helperParam(GUARD_FIRST))!.lateAppLevel.length,
      'guard-then-parser: helper spelling must match the inline one',
    ).toBe(inlineGuardFirst.lateAppLevel.length);
    expect(
      G(helperParam(PARSER_FIRST))!.lateAppLevel.length,
      'parser-then-guard: helper spelling must match the inline one',
    ).toBe(inlineParserFirst.lateAppLevel.length);
    // Non-vacuity: the two inline readings must themselves differ, or the
    // assertions above are satisfied by everything being zero.
    expect(inlineGuardFirst.lateAppLevel.length).toBe(1);
    expect(inlineParserFirst.lateAppLevel.length).toBe(0);
  });

  it('DEPTH 2 — the order holds when the parser arrives through a second helper', () => {
    const outerGuardFirst = G(
      IMP +
        'const app = express();\n' +
        'function inner(app: any) { app.use(express.json()); }\n' +
        'function outer(app: any) { app.use(rejectNulBytes()); inner(app); }\n' +
        'outer(app);\n',
    )!;
    expect(outerGuardFirst.lateAppLevel.length, 'guard, then the parser-helper').toBe(1);
    const outerParserFirst = G(
      IMP +
        'const app = express();\n' +
        'function inner(app: any) { app.use(express.json()); }\n' +
        'function outer(app: any) { inner(app); app.use(rejectNulBytes()); }\n' +
        'outer(app);\n',
    )!;
    expect(outerParserFirst.lateAppLevel, 'the parser-helper, then the guard').toEqual([]);
  });

  it('CONTROL — KS-827’s order-swap pair still AGREES: moving a DECLARATION changes nothing', () => {
    const declaredFirst =
      IMP +
      'function mountGuard(app: any) { app.use(rejectNulBytes()); }\n' +
      'const app = express();\napp.use(express.json());\nmountGuard(app);\n';
    const declaredLast =
      IMP +
      'const app = express();\napp.use(express.json());\nmountGuard(app);\n' +
      'function mountGuard(app: any) { app.use(rejectNulBytes()); }\n';
    expect(G(declaredFirst)!.lateAppLevel.length).toBe(0);
    expect(G(declaredLast)!.lateAppLevel.length).toBe(0);
  });

  it('CONTROL — a helper that mounts a parser and NO guard is untouched by the offset', () => {
    // Its parsers still land on the call position, ordered against whatever
    // guard the file mounts elsewhere — the KS-816 behaviour, unchanged.
    const before = G(
      IMP +
        'const app = express();\n' +
        'function mountParser(app: any) { app.use(express.json()); }\n' +
        'mountParser(app);\napp.use(rejectNulBytes());\n',
    )!;
    expect(before.lateAppLevel, 'parser helper called before the guard is clean').toEqual([]);
    const after = G(
      IMP +
        'const app = express();\n' +
        'function mountParser(app: any) { app.use(express.json()); }\n' +
        'app.use(rejectNulBytes());\nmountParser(app);\n',
    )!;
    expect(after.lateAppLevel.length, 'parser helper called after the guard is red').toBe(1);
  });

  it('CONTROL — mountBodyParsers() is NOT a local helper, so it keeps its single position', () => {
    // The combined mount is a guard mount and a parser mount at ONE position,
    // and "a parser at the guard's own position is not after it" must stay true.
    const a = G(IMP + 'const app = express();\nmountBodyParsers(app);\n')!;
    expect(a.lateAppLevel, 'the combined helper mounts the guard last, by construction').toEqual([]);
    expect(a.postGuardParserSites).toEqual([]);
  });
});

// ===========================================================================
// KS-831 F-QA-B — A ROUTER GUARD VIA A HELPER WAS PROMOTED TO APP-LEVEL.
//
// `mountedOnApp` accepts ANY of a helper's parameters as "the app", because
// from inside the helper `x.use(guard())` is the same AST whether `x` is the
// application or an `express.Router()`. So a router guard mounted through a
// helper credited a guard position on the APP, and an app-level
// `express.json()` above it read CLEAN while genuinely unguarded.
//
// The INLINE spelling of the same program reads NULL — loud, because `classify`
// only calls a guard app-level when it hangs off the file's app. One program,
// two spellings, opposite loudness, and the silent one is the dangerous one.
//
// MEASURED against the unfixed instrument before the fix was written:
//
//   fixture                                       unfixed   correct
//   router guard VIA HELPER, app json above it     late=0    NULL    FALSE CLEAN
//   the same program INLINE                        NULL      NULL
//   depth 2, the outer helper called with a router late=0    NULL    FALSE CLEAN
//   param SHADOWS the file app, called w/ a router late=0    NULL    FALSE CLEAN
//   CONTROL — the same helper called with the app  late=0    late=0
//   CONTROL — app guard via helper, parser after   late=1    late=1
//
// The fix records what a helper mounts its guard ON — the file's app (a closure
// mount) or its own parameter names — and credits a position at a call site
// only when that call passes the file's app into such a parameter. An argument
// this file cannot resolve to the app earns NOTHING, which makes the file read
// NULL and the corpus leg red it BY NAME: the loud direction.
// ===========================================================================
describe('KS-831 F-QA-B — a guard mounted on a ROUTER through a helper is not an app guard', () => {
  const IMP =
    "import express from 'express';\n" +
    "import { rejectNulBytes } from '@secuura/shared';\n";
  const G = (src: string) =>
    analyseSource(src, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts');

  it('a ROUTER guard via a helper leaves the app-level json unguarded — NULL, not clean', () => {
    const a = G(
      IMP +
        'const app = express();\napp.use(express.json());\nconst r = express.Router();\n' +
        'function mountGuard(x: any) { x.use(rejectNulBytes()); }\nmountGuard(r);\napp.use(r);\n',
    );
    expect(a, 'no guard reaches the app, so there is no guard').toBeNull();
  });

  it('🔴 ONE PROGRAM, TWO SPELLINGS — the inline and via-helper router forms must AGREE', () => {
    const viaHelper = G(
      IMP +
        'const app = express();\napp.use(express.json());\nconst r = express.Router();\n' +
        'function mountGuard(x: any) { x.use(rejectNulBytes()); }\nmountGuard(r);\napp.use(r);\n',
    );
    const inline = G(
      IMP +
        'const app = express();\napp.use(express.json());\nconst r = express.Router();\n' +
        'r.use(rejectNulBytes());\napp.use(r);\n',
    );
    expect(inline, 'the inline form was always loud').toBeNull();
    expect(viaHelper, 'the helper form must be exactly as loud').toBeNull();
    // Non-vacuity: this shape is only meaningful because the SAME helper
    // handed the app does produce a scan.
    const handedTheApp = G(
      IMP +
        'const app = express();\napp.use(express.json());\n' +
        'function mountGuard(x: any) { x.use(rejectNulBytes()); }\nmountGuard(app);\n',
    );
    expect(handedTheApp, 'the predicate can return a scan').not.toBeNull();
  });

  it('a PARAMETER shadows the file app — the same name is not the same object', () => {
    // `function mountGuard(app)` mounts on its PARAMETER, whoever calls it.
    const withRouter = G(
      IMP +
        'const app = express();\napp.use(express.json());\nconst r = express.Router();\n' +
        'function mountGuard(app: any) { app.use(rejectNulBytes()); }\nmountGuard(r);\napp.use(r);\n',
    );
    expect(withRouter, 'called with a router: no app guard').toBeNull();
    const withApp = G(
      IMP +
        'const app = express();\napp.use(express.json());\n' +
        'function mountGuard(app: any) { app.use(rejectNulBytes()); }\nmountGuard(app);\n',
    )!;
    expect(withApp.lateAppLevel, 'called with the app: guarded, and clean').toEqual([]);
  });

  it('DEPTH 2 — the target follows the argument through the second hop', () => {
    const viaApp = G(
      IMP +
        'const app = express();\napp.use(express.json());\n' +
        'function inner(x: any) { x.use(rejectNulBytes()); }\n' +
        'function outer(x: any) { inner(x); }\nouter(app);\n',
    )!;
    expect(viaApp.lateAppLevel, 'the app was passed the whole way down').toEqual([]);
    const viaRouter = G(
      IMP +
        'const app = express();\napp.use(express.json());\nconst r = express.Router();\n' +
        'function inner(x: any) { x.use(rejectNulBytes()); }\n' +
        'function outer(x: any) { inner(x); }\nouter(r);\napp.use(r);\n',
    );
    expect(viaRouter, 'a router was passed the whole way down').toBeNull();
  });

  it('CONTROL — a CLOSURE mount needs no argument and is unaffected', () => {
    const a = G(
      IMP +
        'const app = express();\napp.use(express.json());\n' +
        'function mountGuard() { app.use(rejectNulBytes()); }\nmountGuard();\n',
    )!;
    expect(a.lateAppLevel).toEqual([]);
  });

  it('CONTROL — the app-guard-via-helper orderings still read as before', () => {
    const parserFirst = G(
      IMP +
        'const app = express();\napp.use(express.json());\n' +
        'function mountGuard(x: any) { x.use(rejectNulBytes()); }\nmountGuard(app);\n',
    )!;
    expect(parserFirst.lateAppLevel, 'guard last is clean').toEqual([]);
    const parserAfter = G(
      IMP +
        'const app = express();\n' +
        'function mountGuard(x: any) { x.use(rejectNulBytes()); }\nmountGuard(app);\napp.use(express.json());\n',
    )!;
    expect(parserAfter.lateAppLevel.length, 'a parser after the guard is still the defect').toBe(1);
  });

  it('CONTROL — F-QA-A still holds: within-helper guard-then-parser is still RED', () => {
    const a = G(
      IMP +
        'const app = express();\n' +
        'function mountBoth(app: any) { app.use(rejectNulBytes()); app.use(express.json()); }\n' +
        'mountBoth(app);\n',
    )!;
    expect(a.lateAppLevel.length).toBe(1);
  });
});

// ===========================================================================
// KS-831 F-QA-C — THE EXPORT SHAPES `collectExports` COULD NOT SEE.
//
// A helper with no in-file caller is `deadHere` unless it is EXPORTED. Get the
// export wrong and a live factory reads as dead code: its guard is suppressed
// with no call site to re-attach it to, the scan returns null, the file drops
// out of `SCANS`, and the corpus leg reds NAMING it.
//
// So every shape here errs LOUD. This is a false-RED fix, the Minor of the
// three — and still worth closing, because an instrument that cries wolf on a
// legitimate spelling gets its corpus edited rather than its finding read.
//
// MEASURED against the unfixed instrument first, on ONE factory (parser, then
// guard, no in-file caller — `services/demo-service/src/app.ts`'s shape)
// written eleven ways. Six read NULL; three already scanned; and the two
// controls at the end are the discriminating pair.
//
//   export { createApp }                  NULL -> scan
//   export { createApp as makeApp }       NULL -> scan
//   export default createApp              NULL -> scan
//   export = createApp                    NULL -> scan
//   module.exports = createApp            NULL -> scan
//   exports.createApp = createApp         NULL -> scan
//   export function createApp()           scan    unchanged
//   export default function createApp()   scan    unchanged  (NOT a miss — measured)
//   export const createApp = () => {}     scan    unchanged
//   not exported, never called            NULL    unchanged  <- MUST stay NULL
//   exported AND called in this file      scan    unchanged
// ===========================================================================
describe('KS-831 F-QA-C — every export shape that keeps a factory alive is collected', () => {
  const IMP =
    "import express from 'express';\n" +
    "import { rejectNulBytes } from '@secuura/shared';\n";
  // Parser first, guard last: a CLEAN factory, so "did it scan at all" is the
  // only thing these cells are asking.
  const FACTORY =
    'function createApp() {\n' +
    '  const app = express();\n' +
    '  app.use(express.json());\n' +
    '  app.use(rejectNulBytes());\n' +
    '  return app;\n' +
    '}\n';
  const G = (src: string) => analyseSource(src, '/x/services/qa/src/app.ts', 'services/qa/src/app.ts');

  it.each([
    ['export { createApp };', IMP + FACTORY + 'export { createApp };\n'],
    ['export { createApp as makeApp };', IMP + FACTORY + 'export { createApp as makeApp };\n'],
    ['export default createApp;', IMP + FACTORY + 'export default createApp;\n'],
    ['export = createApp;', FACTORY + 'export = createApp;\n'],
    ['module.exports = createApp;', IMP + FACTORY + 'module.exports = createApp;\n'],
    ['exports.createApp = createApp;', IMP + FACTORY + 'exports.createApp = createApp;\n'],
    ['module.exports = { createApp };', IMP + FACTORY + 'module.exports = { createApp };\n'],
  ])('%s keeps the factory alive — the file still scans', (_shape, src) => {
    const a = G(src);
    expect(a, 'an exported factory is not dead code').not.toBeNull();
    expect(a!.lateAppLevel, 'and it is clean — guard mounted last').toEqual([]);
  });

  it('CONTROL — the three shapes that already worked are unchanged', () => {
    expect(G(IMP + 'export ' + FACTORY), 'export function').not.toBeNull();
    expect(G(IMP + 'export default ' + FACTORY), 'export default function').not.toBeNull();
    expect(
      G(
        IMP +
          'export const createApp = () => {\n  const app = express();\n' +
          '  app.use(express.json());\n  app.use(rejectNulBytes());\n  return app;\n};\n',
      ),
      'export const arrow',
    ).not.toBeNull();
  });

  it('🔴 CONTROL — a factory that is NOT exported and never called is still DEAD', () => {
    // The whole point of widening: it must not make dead code look live.
    expect(G(IMP + FACTORY), 'no export, no call — no guard runs').toBeNull();
  });

  it('CONTROL — a RE-EXPORT names another module’s binding, not this file’s', () => {
    // `export { createApp } from './elsewhere'` exports elsewhere's createApp.
    // The local one is still uncalled and unexported, so the file stays NULL.
    const a = G(IMP + FACTORY + "export { createApp } from './elsewhere';\n");
    expect(a, 'a re-export must not resurrect a local dead helper').toBeNull();
  });

  it('CONTROL — the export shapes do not change a file that is genuinely RED', () => {
    // Guard first, parser after, inside an exported factory: still a finding.
    const dirty =
      'function createApp() {\n' +
      '  const app = express();\n' +
      '  app.use(rejectNulBytes());\n' +
      '  app.use(express.json());\n' +
      '  return app;\n' +
      '}\n';
    const a = G(IMP + dirty + 'export { createApp };\n')!;
    expect(a, 'it scans').not.toBeNull();
    expect(a.lateAppLevel.length, 'and the parser after the guard is still caught').toBe(1);
  });
});

// ===========================================================================
// KS-817 F-QA-03 / F-QA-05 / F-QA-10 / F-QA-11 — the rest of the helper model.
//
// All four measured against the instrument BEFORE each fix, one battery, SET
// and COUNT predicted. Two of the predictions were WRONG and are recorded here
// rather than quietly corrected — see F-QA-03 and F-QA-11 below.
//
//   item     before                              after
//   F-QA-03  decl-only helper -> reachable=2     the helper is credited with NOTHING
//   F-QA-05  router parser via helper -> app-lvl app-level=0, reachable=1
//   F-QA-10  alias/property call -> `express.json` at the DECLARATION
//                                                 app-level=1 `(via mountParser)`
//   F-QA-11  lexically nested -> app-level=1 AND reachable=1   the duplicate is gone
//
// F-QA-09 IS DEFERRED, NOT FIXED — ruled 2026-09-06. A call inside `if (false)`
// still attributes (measured app-level=1, with the taken branch as its control
// reading the same). Closing it means constant-folding machinery for a defect
// that errs LOUD and has zero measured instances. The reason is recorded on
// KS-817. Deliberately NOT pinned by an assertion here: a test asserting the
// present wrong answer would have to be deleted before anyone could fix it.
// ===========================================================================
describe('KS-817 F-QA-03 — a parser DECLARED or MENTIONED in a helper is not one it mounts', () => {
  const IMP =
    "import express from 'express';\n" +
    "import { rejectNulBytes } from '@secuura/shared';\n";
  // Guard FIRST, so anything the scanner attributes lands after it and shows up.
  const HEAD = IMP + 'const app = express();\napp.use(rejectNulBytes());\n';
  const G = (src: string) =>
    analyseSource(src, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts');

  it('a helper that only DECLARES a parser is credited with no site of its own', () => {
    const a = G(HEAD + 'function helper() { const p = express.json(); return p; }\nhelper();\n')!;
    // Nothing is attributed to the helper: no site names `(via helper)`.
    expect(
      [...a.lateAppLevel, ...a.postGuardParserSites].filter((x) => x.via.includes('via helper')),
      'the helper mounted nothing, so nothing is attributed to its call',
    ).toEqual([]);
  });

  it('🔴 the residue is the FILE-LEVEL reference rule, not the helper — the two spellings AGREE', () => {
    // This is the correction: the prediction was 0 sites, and it is 1. The one
    // that remains is the documented "a parser bound to a symbol is counted at
    // each REFERENCE" rule, which fires identically with NO helper in the file.
    const viaHelper = G(HEAD + 'function helper() { const p = express.json(); return p; }\nhelper();\n')!;
    const noHelper = G(HEAD + 'const p = express.json();\nconst z = p;\n')!;
    expect(viaHelper.postGuardParserSites.length, 'helper spelling').toBe(1);
    expect(noHelper.postGuardParserSites.length, 'no-helper spelling').toBe(
      viaHelper.postGuardParserSites.length,
    );
    expect(viaHelper.postGuardParserSites[0].via).toBe(noHelper.postGuardParserSites[0].via);
  });

  it('a helper that only MENTIONS a parser symbol is credited with nothing either', () => {
    const a = G(
      IMP + 'const app = express();\nconst mock = express.json();\napp.use(rejectNulBytes());\n' +
        'function helper() { return { mock }; }\nhelper();\n',
    )!;
    expect(a.lateAppLevel, 'a mention mounts nothing app-level').toEqual([]);
    expect(
      a.postGuardParserSites.filter((x) => x.via.includes('via helper')),
      'and nothing is attributed to the helper call',
    ).toEqual([]);
  });

  it('CONTROL — a helper that really MOUNTS one is still app-level, and a parser-free helper is silent', () => {
    const mounts = G(HEAD + 'function helper() { app.use(express.json()); }\nhelper();\n')!;
    expect(mounts.lateAppLevel.length, 'a real mount is still caught').toBe(1);
    expect(mounts.lateAppLevel[0].via).toContain('via helper');
    const none = G(HEAD + 'function helper() { return 1; }\nhelper();\n')!;
    expect(none.lateAppLevel, 'no parser, no site').toEqual([]);
    expect(none.postGuardParserSites).toEqual([]);
    // And a declaration with NO reference is not a site at all.
    expect(G(HEAD + 'const p = express.json();\n')!.postGuardParserSites).toEqual([]);
  });
});

describe('KS-817 F-QA-05 — a parser on a ROUTER via a helper is route-scoped, not app-level', () => {
  const IMP =
    "import express from 'express';\n" +
    "import { rejectNulBytes } from '@secuura/shared';\n";
  const HEAD = IMP + 'const app = express();\napp.use(rejectNulBytes());\n';
  const G = (src: string) =>
    analyseSource(src, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts');
  const HELPER = 'function mountParser(x: any) { x.use(express.json()); }\n';

  it('🔴 the ROUTER and APP call sites of ONE helper must DISAGREE about the list', () => {
    const onRouter = G(HEAD + 'const r = express.Router();\n' + HELPER + 'mountParser(r);\napp.use(r);\n')!;
    const onApp = G(HEAD + HELPER + 'mountParser(app);\n')!;
    expect(onRouter.lateAppLevel, 'a router parser is not app-level').toEqual([]);
    expect(onRouter.postGuardParserSites.length, 'it is a route-scoped site').toBe(1);
    expect(onApp.lateAppLevel.length, 'the app parser IS app-level').toBe(1);
    expect(onApp.postGuardParserSites, 'and is not double-counted as route-scoped').toEqual([]);
  });

  it('CONTROL — the guard side reads the same program the same way (F-QA-B)', () => {
    const routerGuard = G(
      IMP + 'const app = express();\napp.use(express.json());\nconst r = express.Router();\n' +
        'function mountGuard(x: any) { x.use(rejectNulBytes()); }\nmountGuard(r);\napp.use(r);\n',
    );
    expect(routerGuard, 'a router guard is no app guard').toBeNull();
  });
});

describe('KS-817 F-QA-10 — an alias or a property is still a call to the helper', () => {
  const IMP =
    "import express from 'express';\n" +
    "import { rejectNulBytes } from '@secuura/shared';\n";
  const HEAD = IMP + 'const app = express();\napp.use(rejectNulBytes());\n';
  const G = (src: string) =>
    analyseSource(src, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts');
  const HELPER = 'function mountParser(x: any) { x.use(express.json()); }\n';

  it.each([
    ['bare call', 'mountParser(app);\n'],
    ['alias call', 'const m = mountParser;\nm(app);\n'],
    ['property call', 'const obj = { mount: mountParser };\nobj.mount(app);\n'],
    ['shorthand property call', 'const obj = { mountParser };\nobj.mountParser(app);\n'],
  ])('%s attributes at the CALL, naming the helper', (_shape, tail) => {
    const a = G(HEAD + HELPER + tail)!;
    expect(a.lateAppLevel.length, 'one app-level site').toBe(1);
    expect(a.lateAppLevel[0].via, 'named by the helper it came through').toContain('via mountParser');
  });

  it('🔴 all three spellings of ONE program must AGREE', () => {
    const read = (tail: string) => {
      const a = G(HEAD + HELPER + tail)!;
      return `${a.lateAppLevel.length}/${a.postGuardParserSites.length}/${a.lateAppLevel[0]?.via}`;
    };
    const bare = read('mountParser(app);\n');
    expect(read('const m = mountParser;\nm(app);\n'), 'alias').toBe(bare);
    expect(read('const obj = { mount: mountParser };\nobj.mount(app);\n'), 'property').toBe(bare);
    // Non-vacuity: the reading is not a constant — a router call differs.
    const onRouter = G(HEAD + 'const r = express.Router();\n' + HELPER + 'mountParser(r);\napp.use(r);\n')!;
    expect(`${onRouter.lateAppLevel.length}/${onRouter.postGuardParserSites.length}`).not.toBe(
      bare.split('/').slice(0, 2).join('/'),
    );
  });

  it('CONTROL — an unresolvable indirection is NOT invented into a call site', () => {
    // A binding this file cannot resolve to a helper falls through exactly as
    // before; the fix is one level of `const` aliasing, not a dataflow engine.
    const a = G(HEAD + HELPER + 'const m = pickAtRuntime();\nm(app);\n')!;
    expect(
      a.lateAppLevel.filter((x) => x.via.includes('via mountParser')),
      'nothing is attributed through an unknown binding',
    ).toEqual([]);
  });
});

describe('KS-817 F-QA-11 — a lexically NESTED helper is counted once, not twice', () => {
  const IMP =
    "import express from 'express';\n" +
    "import { rejectNulBytes } from '@secuura/shared';\n";
  const HEAD = IMP + 'const app = express();\napp.use(rejectNulBytes());\n';
  const G = (src: string) =>
    analyseSource(src, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts');

  // The correction worth keeping: the ticket described this as "classifies
  // `reachable`, so LEG D reds with the wrong diagnosis". Measured, NONE of the
  // four sibling-helper shapes reproduced it — F-QA-07's fix already covers
  // those. It reproduces only when the inner helper is nested LEXICALLY and
  // mounts on the OUTER's parameter, and then the symptom is a DOUBLE COUNT:
  // app-level=1 AND reachable=1 for one parser. `outer`'s walk reads the inner
  // body with outer's params in scope (correct, app-level) and then reads it
  // AGAIN at `inner()` with inner's own empty params (wrong, reachable).

  it('🔴 one parser, one site — the duplicate in the other list is gone', () => {
    const a = G(
      HEAD + 'function outer(y: any) { function inner() { y.use(express.json()); } inner(); }\nouter(app);\n',
    )!;
    expect(a.lateAppLevel.length, 'app-level').toBe(1);
    expect(a.postGuardParserSites, 'and NOT also route-scoped').toEqual([]);
  });

  it('the arrow spelling of the nested helper reads identically', () => {
    const a = G(
      HEAD + 'function outer(y: any) { const inner = () => { y.use(express.json()); }; inner(); }\nouter(app);\n',
    )!;
    expect(a.lateAppLevel.length).toBe(1);
    expect(a.postGuardParserSites).toEqual([]);
  });

  it('🔴 nesting must not change the count — the nested and direct spellings AGREE', () => {
    const nested = G(
      HEAD + 'function outer(y: any) { function inner() { y.use(express.json()); } inner(); }\nouter(app);\n',
    )!;
    const direct = G(HEAD + 'function outer(y: any) { y.use(express.json()); }\nouter(app);\n')!;
    expect(nested.lateAppLevel.length).toBe(direct.lateAppLevel.length);
    expect(nested.postGuardParserSites.length).toBe(direct.postGuardParserSites.length);
  });

  it('a second, genuine parser is still counted alongside it', () => {
    // Non-vacuity: the fix removes a DUPLICATE, not every extra site.
    const a = G(
      HEAD + 'function outer(y: any) { function inner() { y.use(express.json()); } inner(); }\n' +
        'outer(app);\napp.use(express.text());\n',
    )!;
    expect(a.lateAppLevel.length, 'the nested one plus the real second one').toBe(2);
    expect(a.postGuardParserSites).toEqual([]);
  });

  it('CONTROL — sibling helpers (not nested) are unchanged in all four shapes', () => {
    const inner = 'function inner(x: any) { x.use(express.json()); }\n';
    expect(G(HEAD + inner + 'function outer(y: any) { inner(y); }\nouter(app);\n')!.lateAppLevel.length)
      .toBe(1);
    expect(
      G(HEAD + 'function outer(y: any) { inner(y); }\n' + inner + 'outer(app);\n')!.lateAppLevel.length,
      'inner declared AFTER outer — F-QA-07 territory',
    ).toBe(1);
    expect(
      G(HEAD + "function inner(x: any) { x.post('/p', express.json(), h); }\n" +
        'function outer(y: any) { inner(y); }\nouter(app);\n')!.postGuardParserSites.length,
      'a route-scoped nested parser stays route-scoped',
    ).toBe(1);
    expect(
      G(HEAD + 'function inner() { app.use(express.json()); }\nfunction outer() { inner(); }\nouter();\n')!
        .lateAppLevel.length,
      'closure over the file app',
    ).toBe(1);
  });
});

// ===========================================================================
// KS-817 — THE SOCKET-LEVEL ACCEPTANCE CELL. THE ROUND ENDS HERE.
//
// Carried verbatim from the KS-816 re-gate's NOT-TESTED #1, and repeated on
// every scanner gate since: *nothing in the KS-816 or KS-827 rounds has touched
// a running Express app.* Every cell above this one reads the INSTRUMENT. None
// of them shows that what the instrument reports is true of a program that
// runs.
//
// So this cell closes the loop for the helper shape the whole round is about:
//
//   source text  ->  analyseSource verdict  ->  booted express app
//                ->  a real TCP socket      ->  a NUL byte in req.body
//
// ONE source string per program is the single source of truth. The scanner
// reads it; the runtime executes it. The only transform is dropping the two
// `import` lines and appending `return app;`, and that transform is ASSERTED
// rather than assumed — otherwise the thing analysed and the thing run are two
// artefacts and the cell proves nothing about either.
//
// The client is a raw `net` socket, not `fetch`: fetch will not put a raw NUL
// on the wire (URLSearchParams percent-encodes it), so a NUL that survives
// `fetch` is a NUL the client chose to send in some other form. The assertion
// `body.includes(0)` proves the byte is really there before anything is read
// into the result.
//
// MEASURED:
//   RED    parser AFTER  the guard via a helper   scanner late=1
//                                                 socket NUL -> 200, reached=true,
//                                                 req.body echoed back, JSON-escaped
//   CLEAN  parser BEFORE the guard via a helper   scanner late=0
//                                                 socket NUL -> 400, refused
//   both                                          clean body -> 200
// ===========================================================================
describe('KS-817 ACCEPTANCE — the scanner’s verdict predicts what a booted app does with a NUL', () => {
  // Two programs, differing ONLY in whether the helper is called before or
  // after the guard. Written without type annotations so the exact text the
  // scanner parses is also valid JavaScript to execute.
  const HELPER = 'function mountParser(a) { a.use(express.urlencoded({ extended: true })); }\n';
  const HANDLER =
    "app.post('/probe', function (req, res) { res.status(200).json({ reached: true, state: req.body && req.body.state }); });\n";
  const IMPORTS =
    "import express from 'express';\n" + "import { rejectNulBytes } from '@secuura/shared';\n";
  const RED_SRC =
    IMPORTS + 'const app = express();\n' + HELPER + 'app.use(rejectNulBytes());\nmountParser(app);\n' + HANDLER;
  const CLEAN_SRC =
    IMPORTS + 'const app = express();\n' + HELPER + 'mountParser(app);\napp.use(rejectNulBytes());\n' + HANDLER;

  // KS-832 F-QA-I — the program this bar did NOT cover. RED_SRC and CLEAN_SRC
  // both put the guard and the parser at the FILE level and differ only in
  // order. Neither is a HELPER that mounts guard-then-parser inside itself,
  // which is F-QA-A, the Major the KS-817/831 round actually closed. The gate
  // measured that both collapse tampers left all six acceptance cells green:
  // the bar passed on the defect the round was about.
  const HELPER_BOTH =
    'function mountBoth(a) { a.use(rejectNulBytes()); a.use(express.urlencoded({ extended: true })); }\n';
  const WITHIN_HELPER_SRC =
    IMPORTS + 'const app = express();\n' + HELPER_BOTH + 'mountBoth(app);\n' + HANDLER;

  /** The ONLY transform between what is analysed and what is run. */
  const toRuntime = (src: string): string =>
    src
      .split('\n')
      .filter((l) => !l.startsWith('import '))
      .join('\n') + '\nreturn app;\n';

  const build = (src: string): express.Express =>
    new Function('express', 'rejectNulBytes', toRuntime(src))(express, rejectNulBytes) as express.Express;

  /** POST over a real socket. No client library touches the bytes. */
  function rawPost(port: number, body: Buffer): Promise<{ status: number; text: string }> {
    return new Promise((res, rej) => {
      const sock = netConnect(port, '127.0.0.1');
      const chunks: Buffer[] = [];
      sock.on('error', rej);
      sock.on('connect', () => {
        const head = Buffer.from(
          'POST /probe HTTP/1.1\r\nHost: 127.0.0.1\r\n' +
            'Content-Type: application/x-www-form-urlencoded\r\n' +
            `Content-Length: ${body.length}\r\nConnection: close\r\n\r\n`,
          'latin1',
        );
        sock.write(Buffer.concat([head, body]));
      });
      sock.on('data', (d) => chunks.push(d as Buffer));
      sock.on('close', () => {
        const text = Buffer.concat(chunks).toString('latin1');
        const m = /^HTTP\/1\.1 (\d{3})/.exec(text);
        res({ status: m ? Number(m[1]) : 0, text });
      });
    });
  }

  const NUL_BODY = Buffer.from('state=ab' + String.fromCharCode(0) + 'cd', 'latin1');
  const CLEAN_BODY = Buffer.from('state=abcd', 'latin1');

  const drive = async (src: string) => {
    const scan = analyseSource(src, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts');
    const { base, server } = await listen(build(src));
    const port = Number(base.split(':').pop());
    try {
      return {
        late: scan === null ? -1 : scan.lateAppLevel.length,
        nul: await rawPost(port, NUL_BODY),
        clean: await rawPost(port, CLEAN_BODY),
      };
    } finally {
      await close(server);
    }
  };

  // KS-832 F-QA-G — this cell used to compare `toRuntime` to a character-for-
  // character COPY of its own body:
  //
  //     expect(toRuntime(src)).toBe(
  //       src.split('\n').filter(l => !l.startsWith('import ')).join('\n') + '\nreturn app;\n')
  //
  // which guarantees that `toRuntime` equals itself. Its stated claim — that the
  // text ANALYSED and the text EXECUTED differ only by the import lines — was
  // not what it checked, and the gate's T7 showed it cannot fail on a divergence
  // introduced anywhere else. Worse, the realistic failure is invisible to it:
  // someone edits the transform and updates the mirrored expectation in the same
  // commit, and the mirror certifies the edit.
  //
  // Replaced by four properties, each computed WITHOUT calling `toRuntime`, each
  // failing on a different kind of divergence: nothing dropped, imports gone,
  // nothing added but the return, order preserved.
  //
  // Residual limit, stated rather than left to be discovered: this asserts a
  // property of the TRANSFORM. It does not intercept `new Function`, so a `build`
  // that stopped calling `toRuntime` altogether would still pass. Closing that
  // needs the executed string captured at the call site, which is a different
  // change from this one.
  it('the text analysed and the text executed differ ONLY by the import lines', () => {
    for (const [name, src] of [['RED', RED_SRC], ['CLEAN', CLEAN_SRC]] as const) {
      const analysedLines = src.split('\n').filter((l) => l !== '');
      const importLines = analysedLines.filter((l) => l.startsWith('import '));
      const bodyLines = analysedLines.filter((l) => !l.startsWith('import '));
      const executedLines = toRuntime(src).split('\n').filter((l) => l !== '');

      expect(importLines.length, `${name}: exactly two imports exist to be dropped`).toBe(2);
      expect(bodyLines.length, `${name}: and there is a body to preserve`).toBeGreaterThan(2);

      // (1) nothing the SCANNER sees, other than an import, is missing from what RUNS
      for (const line of bodyLines) {
        expect(executedLines, `${name}: a non-import line was dropped — ${line.slice(0, 48)}`).toContain(line);
      }
      // (2) no import survives into the executed text
      for (const line of importLines) {
        expect(executedLines, `${name}: an import survived — ${line.slice(0, 48)}`).not.toContain(line);
      }
      // (3) nothing was ADDED except the appended return
      const added = executedLines.filter((l) => !bodyLines.includes(l));
      expect(added, `${name}: the only addition is the return`).toEqual(['return app;']);
      // (4) order is preserved — the body lines appear in the executed text in
      //     the same relative order they appear in the source
      const positions = bodyLines.map((l) => executedLines.indexOf(l));
      expect(positions, `${name}: the transform reordered the program`).toEqual(
        [...positions].sort((a, b) => a - b),
      );
      // (5) KS-842 Q-2 — MULTIPLICITY. Properties (1)-(4) are all SET-shaped:
      //     `includes`, `filter(… !includes)` and `indexOf` every one of them
      //     collapses duplicates, and `indexOf` returns the FIRST occurrence so
      //     a repeated line maps every copy to the same index and (4) still
      //     reads sorted. Measured by the #836 gate: a transform that emits a
      //     body line TWICE, and one that DROPS the second of two identical
      //     lines, both pass all four while changing what runs.
      //
      //     That matters here specifically: a duplicated GUARD mount is
      //     harmless, but a duplicated or dropped PARSER mount is the exact
      //     shape of the KS-800 defect this file exists to detect — the
      //     scanner would see two mounts and the socket exercise one.
      //
      //     Computed from the two values actually used, `src` and
      //     `toRuntime(src)`, so an edit to `toRuntime` cannot satisfy it
      //     unless the edit really preserves the property. Not a mirror.
      const countIn = (xs: readonly string[], line: string): number =>
        xs.reduce((acc, x) => (x === line ? acc + 1 : acc), 0);
      for (const line of new Set(bodyLines)) {
        expect(
          countIn(executedLines, line),
          `${name}: multiplicity changed for — ${line.slice(0, 48)}`,
        ).toBe(countIn(bodyLines, line));
      }
      expect(
        countIn(executedLines, 'return app;') - countIn(bodyLines, 'return app;'),
        `${name}: 'return app;' is the single permitted +1`,
      ).toBe(1);
    }
  });

  it('\u{1f534} F-QA-I — a HELPER mounting guard-then-parser: the scanner says late=1 and the NUL REACHES THE HANDLER', async () => {
    // The implication this bar exists to test, over the shape the round closed.
    // Both file-level programs above keep the guard and the parser as separate
    // statements; this one puts BOTH inside one helper, where the within-helper
    // ORDER is the only thing that decides the answer.
    const r = await drive(WITHIN_HELPER_SRC);
    expect(r.late, 'a parser mounted after the guard, both inside one helper').toBe(1);
    expect(r.nul.status, 'the guard ran before the body existed, so it never saw it').toBe(200);
    expect(r.nul.text, 'and the NUL is in req.body, echoed back').toContain('\\u0000');
    expect(r.clean.status, 'CONTROL — the same app answers a clean body identically').toBe(200);
  });

  it('a real NUL byte is on the wire — not a percent-encoding', () => {
    expect(NUL_BODY.includes(0), 'the request body carries byte 0x00').toBe(true);
    expect(CLEAN_BODY.includes(0), 'and the control body does not').toBe(false);
  });

  it('RED — the scanner says late=1, and over a socket the NUL REACHES THE HANDLER', async () => {
    const r = await drive(RED_SRC);
    expect(r.late, 'a parser mounted after the guard').toBe(1);
    expect(r.nul.status, 'the guard never saw this body').toBe(200);
    expect(/"reached":true/.test(r.nul.text), 'the handler ran').toBe(true);
    expect(r.nul.text.includes('\\u0000'), 'and the NUL is in req.body, echoed back').toBe(true);
  });

  it('CLEAN — the scanner says late=0, and over a socket the SAME NUL is refused', async () => {
    const r = await drive(CLEAN_SRC);
    expect(r.late, 'the guard is mounted last').toBe(0);
    expect(r.nul.status, 'refused').toBe(400);
    expect(/"reached":true/.test(r.nul.text), 'the handler never ran').toBe(false);
  });

  it('CONTROL — neither program is blanket-refusing: a clean body is 200 in both', async () => {
    for (const [label, src] of [['red', RED_SRC], ['clean', CLEAN_SRC]] as const) {
      const r = await drive(src);
      expect(r.clean.status, `${label}: a clean body is accepted`).toBe(200);
      expect(/"reached":true/.test(r.clean.text), `${label}: and reaches the handler`).toBe(true);
    }
  });

  it('🔴 THE ACCEPTANCE — the verdict PREDICTS the socket, in both directions', async () => {
    const red = await drive(RED_SRC);
    const clean = await drive(CLEAN_SRC);
    // "the scanner reports a late parser" must mean exactly "a NUL gets through".
    expect(red.late > 0, 'red: reported').toBe(red.nul.status === 200);
    expect(clean.late > 0, 'clean: not reported').toBe(clean.nul.status === 200);
    // Non-vacuity: the two runtime outcomes must actually differ, or the
    // implication above is satisfied by everything behaving the same way.
    expect(red.nul.status).not.toBe(clean.nul.status);
  });
});

// KS-818 G-05 — `PARSER_FACTORY_NAMES` WAS A HAND-MAINTAINED LIST WITH NO LEG.
//
// Eight names here, eight parser factories exported by
// `packages/shared/src/middleware/request-limits.ts` — and NOTHING asserted the
// two agree. A ninth factory added there was invisible to every leg until
// somebody remembered to edit this array. That is the same defect KS-800
// closed for the corpus (`ENTRYPOINT_NAMES`, deleted in G-08 of this ticket):
// a literal list standing in for a property.
//
// The property is asserted STRUCTURALLY rather than by naming convention,
// because "ends in Parser" is another literal list wearing a different hat.
// A module function is a parser factory iff its body reaches an
// `express.json|urlencoded|raw|text` call, or calls another function in this
// module that does — a fixed point, so a preset that only calls one of the four
// base factories can qualify through a LATER pass.
//
// KS-833 Q-3 corrects that last clause and the predicate under it. The base
// case used to be `parserCallName`, which returns non-null for any name in
// PARSER_FACTORY_NAMES — so the presets qualified on PASS 1 by the name branch
// and the fixed point was never exercised by the real module. Worse, the leg
// was then structure UNION the list it was checking: two exported functions
// that only delegate to each other, reaching no `express.*` at all, were still
// "detected". The base case is now `moduleParserReach`, which does not consult
// the list.
//
// KS-833 F-2 corrects the sentence that stood here ("the presets now really do
// qualify on the second pass"). Measured: with this module's declaration order
// all eight enter on pass 0 — the loop walks declarations in order, so a target
// declared before its delegator is already marked when the delegator is
// visited, within the SAME pass. Which pass a name enters on is a property of
// DECLARATION ORDER, not of the presets. The fixed point is still load-bearing:
// declare the delegator first and it takes pass 1. Both directions are pinned
// by the F-2 cell below, so this paragraph is now testable rather than
// asserted.
//
// MEASURED before this was written:
//   declared              jsonParser, largeBodyParsers, minimalBodyParsers, rawParser,
//                         standardBodyParsers, textParser, urlencodedParser, webhookBodyParsers
//   structurally detected  ...identical
//   ALL exported functions  ...the same eight PLUS requestTimeout, payloadSizeChecker
//   excluded               requestTimeout, payloadSizeChecker   <- the control
//   a synthetic NINTH      detected, and reds the leg           <- the point
// ===========================================================================
describe('KS-818 G-05 — the parser-factory list is asserted against the module, not maintained by hand', () => {
  const REQUEST_LIMITS_REL = 'packages/shared/src/middleware/request-limits.ts';

  /** Every exported function declaration in a module, by name. */
  const exportedFunctionNames = (sf: ts.SourceFile): string[] => {
    const out: string[] = [];
    const walk = (n: ts.Node): void => {
      if (
        ts.isFunctionDeclaration(n) &&
        n.name &&
        n.modifiers?.some((m) => m.kind === ts.SyntaxKind.ExportKeyword)
      ) {
        out.push(n.name.text);
      }
      ts.forEachChild(n, walk);
    };
    walk(sf);
    return out.sort();
  };

  /**
   * Which exported functions actually PRODUCE a body parser.
   *
   * Structural: reaches an `express.<parser>()` call directly, or calls another
   * function in this module that does. Fixed point, bounded by the function
   * count — the same shape as the helper resolution in `analyseSource`.
   */
  const parserFactoryReachOf = (
    source: string,
    fileName: string,
  ): { exports: string[]; passOf: ReadonlyMap<string, number> } => {
    const sf = ts.createSourceFile(fileName, source, ts.ScriptTarget.Latest, true);
    const bindings = moduleBindings(sf);
    // KS-833 Q-4. This used to collect EXPORTED FunctionDeclarations only, which
    // made two shapes invisible:
    //
    //   1. `export const ndjsonParser = (): RequestHandler => express.json(...)`
    //      - an arrow-const factory is not a FunctionDeclaration.
    //   2. `export function ndjsonParser() { return build(); }` where the
    //      NON-EXPORTED `build()` is the thing that reaches express - the reach
    //      analysis could not follow into a function it never collected.
    //
    // Latent while `request-limits.ts` uses exported declarations only; it stops
    // being latent the moment somebody writes either shape. The walk now
    // collects EVERY module function by either spelling, and the EXPORT filter
    // moves to the RESULT - reachability is a property of the call graph, being
    // exported is a property of the answer.
    const fns = new Map<string, ts.Node>();
    // KS-833 F-3. LOCAL name -> the name the module EXPORTS it under. A map, not
    // a set, because `export { ndjsonImpl as ndjsonParser }` makes those differ
    // and the callable name is the one `PARSER_FACTORY_NAMES` has to carry.
    // For a modifier export the two are identical, so the existing eight are
    // unchanged.
    // KS-857 N-3 — a local name may be exported under SEVERAL names, so this is
    // a Map to a SET. It was `Map<string, string>`, i.e. last-write-wins, and
    // `collect` walks in source order: an `export { jsonParser as alias }` at
    // the bottom of a file OVERWROTE the entry `export function jsonParser` set
    // earlier, and `jsonParser` vanished from the answer though the module
    // still exports it. The equality leg is loud when that happens — but it
    // says "jsonParser is not an exported factory" about a function that IS
    // one, which sends the reader after the wrong thing. The defect was in the
    // message, not the detection.
    const exported = new Map<string, Set<string>>();
    const addExport = (local: string, exportedAs: string): void => {
      // `export { x as default }` yields the literal name "default", which no
      // consumer can call and which PARSER_FACTORY_NAMES could never carry.
      // KS-857 N-3 SKIPPED it — and KS-900 measured what that opened: a factory
      // exported ONLY as default contributed no name at all, so if it was also
      // absent from the array the equality leg was satisfied and nothing
      // fired. It is now recorded under its LOCAL name instead, so the
      // equality leg reports it as missing from the array — loud in one
      // direction rather than silent. The literal "default" is still never an
      // answer (the CONTROL below pins both halves).
      const names = exported.get(local) ?? new Set<string>();
      names.add(exportedAs === 'default' ? local : exportedAs);
      exported.set(local, names);
    };
    const hasExport = (n: ts.Node): boolean =>
      ts.canHaveModifiers(n) &&
      (ts.getModifiers(n)?.some((m) => m.kind === ts.SyntaxKind.ExportKeyword) ?? false);
    const collect = (n: ts.Node): void => {
      if (ts.isFunctionDeclaration(n) && n.name && n.body) {
        fns.set(n.name.text, n.body);
        if (hasExport(n)) addExport(n.name.text, n.name.text);
      }
      // KS-833 F-3 — `export { ndjsonParser }`. `hasExport` reads MODIFIERS, and
      // an ExportDeclaration sets none, so a factory exported this way was
      // collected, marked a factory, then dropped from the answer. n fell back
      // to 8, which EQUALS the array, so the equality leg stayed GREEN and the
      // leg's whole purpose failed with no signal. A re-export carrying a module
      // specifier (`export { x } from './y'`) is skipped: its local name is not
      // a declaration in this file.
      if (
        ts.isExportDeclaration(n) &&
        !n.moduleSpecifier &&
        n.exportClause &&
        ts.isNamedExports(n.exportClause)
      ) {
        for (const el of n.exportClause.elements) {
          addExport((el.propertyName ?? el.name).text, el.name.text);
        }
      }
      if (ts.isVariableStatement(n)) {
        for (const d of n.declarationList.declarations) {
          if (
            ts.isIdentifier(d.name) &&
            d.initializer &&
            (ts.isArrowFunction(d.initializer) || ts.isFunctionExpression(d.initializer))
          ) {
            fns.set(d.name.text, d.initializer.body);
            if (hasExport(n)) addExport(d.name.text, d.name.text);
          }
        }
      }
      ts.forEachChild(n, collect);
    };
    collect(sf);
    const isFactory = new Set<string>();
    // KS-833 F-2 — the pass each name entered on. The header claimed the presets
    // "really do qualify on the second pass"; nothing measured that, and it is
    // false for this module's declaration order. Recording the index makes the
    // claim testable instead of decorative.
    const passOf = new Map<string, number>();
    for (let pass = 0; pass <= fns.size; pass += 1) {
      let grew = false;
      for (const [name, body] of fns) {
        if (isFactory.has(name)) continue;
        let found = false;
        const walk = (n: ts.Node): void => {
          if (found) return;
          // KS-833 Q-3: the module-reach predicate, NOT parserCallName — the
          // latter consults PARSER_FACTORY_NAMES, which is the list this leg
          // exists to check.
          if (moduleParserReach(n, bindings)) {
            found = true;
            return;
          }
          if (
            ts.isCallExpression(n) &&
            ts.isIdentifier(n.expression) &&
            isFactory.has(n.expression.text)
          ) {
            found = true;
            return;
          }
          ts.forEachChild(n, walk);
        };
        walk(body);
        if (found) {
          isFactory.add(name);
          passOf.set(name, pass);
          grew = true;
        }
      }
      if (!grew) break;
    }
    // The export filter is applied HERE, not during collection: a non-exported
    // helper may CARRY the reach without itself being an answer.
    // Answered under the EXPORTED name (KS-833 F-3): identical to the local name
    // for every modifier export, and the callable name for an aliased one.
    // KS-857 N-3: EVERY name the module exports a factory under, not just the
    // last one `collect` happened to see.
    const exportsSorted = [...isFactory]
      .flatMap((n) => [...(exported.get(n) ?? [])])
      .sort();
    return { exports: exportsSorted, passOf };
  };

  /**
   * The exported parser factories of a module. The answer every leg reads —
   * {@link parserFactoryReachOf} is the same derivation with the pass indices
   * kept, so there is ONE fixed point here, not two that can drift. (Two copies
   * of one rule is the defect KS-833 Q-1 closed for the corpus; it is not
   * reintroduced here for the sake of one assertion.)
   */
  const parserFactoryExportsOf = (source: string, fileName: string): string[] =>
    parserFactoryReachOf(source, fileName).exports;

  const requestLimitsSource = (): string => {
    const p = join(DEV_ROOT, REQUEST_LIMITS_REL);
    expect(existsSync(p), `${REQUEST_LIMITS_REL} must exist — a missing file reads as zero factories`).toBe(true);
    return readFileSync(p, 'utf8');
  };

  it('🔴 PARSER_FACTORY_NAMES is EXACTLY the module’s parser factories', () => {
    const found = parserFactoryExportsOf(requestLimitsSource(), 'request-limits.ts');
    expect(
      found,
      'A parser factory exported by request-limits.ts and absent from PARSER_FACTORY_NAMES is ' +
        'invisible to every leg in this file. Add it to the array with a ticket — or, if it is ' +
        'not a body parser, say why here.',
    ).toEqual([...PARSER_FACTORY_NAMES].sort());
  });

  it('\u{1f534} KS-857 N-3 — a factory exported under TWO names yields BOTH, not the last one collected', () => {
    // `collect` walks in source order, and the local -> exported map was
    // last-write-wins. An `export { jsonParser as alias }` at the bottom of the
    // file OVERWROTE the entry `export function jsonParser` set earlier, so
    // `jsonParser` vanished from the answer while the module still exported it.
    //
    // The equality leg above IS loud when that happens — but it says
    // "jsonParser is not an exported factory" about a function that is one, and
    // sends the reader after the wrong thing. The defect was in the message,
    // not the detection, which is why this cell asserts the CONTENT of the
    // answer rather than that the leg reds.
    const src = `${requestLimitsSource()}\nexport { jsonParser as jsonParserAlias };\n`;
    const found = parserFactoryExportsOf(src, 'request-limits.ts');
    expect(found, 'the modifier export survives the later export list').toContain('jsonParser');
    expect(found, 'and the alias is reported alongside it').toContain('jsonParserAlias');
  });

  it('CONTROL — `export { x as default }` records the LOCAL name, never the literal "default"', () => {
    // "default" is the literal name an ExportSpecifier yields here. No consumer
    // can call it and PARSER_FACTORY_NAMES could never carry it. This cell used
    // to pin that the specifier was SKIPPED ("contributes NO callable name");
    // KS-900 reshaped it: the specifier now records the local name, so a
    // factory exported only that way is reported by the equality leg instead
    // of vanishing (J1 below is the red-first for that half). Both halves
    // pinned: no "default" in the answer, and the local name exactly ONCE even
    // when the modifier export and the default specifier both name it.
    const src = `${requestLimitsSource()}\nexport { jsonParser as default };\n`;
    const found = parserFactoryExportsOf(src, 'request-limits.ts');
    expect(found, 'a name no consumer can call is not an export the array can carry').not.toContain(
      'default',
    );
    expect(found, 'and the modifier export is untouched by it').toContain('jsonParser');
    expect(found.filter((n) => n === 'jsonParser'), 'recorded once, not once per export site').toHaveLength(1);
  });

  it('J1 🔴 KS-900 — a factory exported ONLY as default is recorded under its LOCAL name, not dropped', () => {
    // KS-900. The `default` skip (KS-857 N-3) made a default-only factory
    // vanish from the answer entirely: if it was also absent from
    // PARSER_FACTORY_NAMES the equality leg was satisfied and nothing fired.
    // Recording the local under its own name makes the equality leg report it
    // as missing from the array — loud in one direction. Fixture: the real
    // module with jsonParser's modifier export removed and re-exported only as
    // default. No live instance (measured 2026-09-13: request-limits.ts has no
    // default FUNCTION export — J2 pins that).
    const base = requestLimitsSource();
    expect(base, 'fixture precondition: jsonParser is a modifier export in the real module').toContain(
      'export function jsonParser(',
    );
    const src = `${base.replace('export function jsonParser(', 'function jsonParser(')}\nexport { jsonParser as default };\n`;
    const found = parserFactoryExportsOf(src, 'request-limits.ts');
    expect(found, 'a default-only factory must still be loud under its local name').toContain('jsonParser');
    expect(found, 'and the literal name "default" is never an answer').not.toContain('default');
  });

  it('J2 KS-900 — the real request-limits.ts has NO default FUNCTION export (structural pin)', () => {
    // KS-900's other half: the cheap structural cell. Three function-shaped
    // defaults are pinned ABSENT — `export default function`, `export default
    // <expression that is not an object literal>`, `export { x as default }`.
    // KNOWN, DIFFERENT shape, deliberately outside this pin: request-limits.ts
    // ends with `export default { REQUEST_LIMITS, jsonParser, … }` — an
    // OBJECT-LITERAL default listing every export as a shorthand property.
    // That is a property access (`limits.jsonParser`), not a bare callable
    // name PARSER_FACTORY_NAMES could carry, and the G-05 walk ignores an
    // ExportAssignment entirely. A pin that every shorthand property of that
    // object is also a modifier export would close `default.x`-only smuggling;
    // it is not built here (a KS-900 widening) and is recorded on the ticket.
    const sf = ts.createSourceFile('request-limits.ts', requestLimitsSource(), ts.ScriptTarget.Latest, true);
    const shapes: string[] = [];
    const walk = (n: ts.Node): void => {
      if (ts.isFunctionDeclaration(n) && n.modifiers?.some((m) => m.kind === ts.SyntaxKind.DefaultKeyword)) {
        shapes.push('export default function');
      }
      if (ts.isExportAssignment(n) && !ts.isObjectLiteralExpression(n.expression)) {
        shapes.push(`export default <${ts.SyntaxKind[n.expression.kind]}>`);
      }
      if (
        ts.isExportDeclaration(n) &&
        n.exportClause &&
        ts.isNamedExports(n.exportClause) &&
        n.exportClause.elements.some((e) => e.name.text === 'default')
      ) {
        shapes.push('export { x as default }');
      }
      ts.forEachChild(n, walk);
    };
    walk(sf);
    expect(shapes, 'a default FUNCTION export would be a factory no bare name reaches').toEqual([]);
  });

  it('CONTROL — the module’s NON-parser exports are excluded, so this is not "every export"', () => {
    const src = requestLimitsSource();
    const all = exportedFunctionNames(ts.createSourceFile('x.ts', src, ts.ScriptTarget.Latest, true));
    const found = parserFactoryExportsOf(src, 'request-limits.ts');
    // `requestTimeout` and `payloadSizeChecker` return an inline handler and
    // reach no parser. If the predicate collected every export, the assertion
    // above would be satisfied by a predicate that discriminates nothing.
    expect(all.length, 'the module exports more functions than it does parser factories').toBeGreaterThan(
      found.length,
    );
    expect(found).not.toContain('requestTimeout');
    expect(found).not.toContain('payloadSizeChecker');
    expect(all, 'and those two really are exported — or the exclusion is vacuous').toEqual(
      expect.arrayContaining(['requestTimeout', 'payloadSizeChecker']),
    );
  });

  it('🔴 a NINTH factory added to that module WOULD be caught — the whole point of the leg', () => {
    // Synthesised, not written to disk: the leg above must be shown to fire on
    // the case it exists for, without tampering the real module.
    const withNinth =
      requestLimitsSource() +
      '\nexport function ndjsonParser(): RequestHandler {\n' +
      "  return express.json({ type: 'application/x-ndjson' });\n}\n";
    const found = parserFactoryExportsOf(withNinth, 'request-limits.ts');
    expect(found, 'the new factory is detected').toContain('ndjsonParser');
    expect(
      found,
      'and it makes the leg above RED rather than passing silently — which is what ' +
        'the hand-maintained array could not do',
    ).not.toEqual([...PARSER_FACTORY_NAMES].sort());
  });

  it('🔴 KS-833 Q-3 — mutual delegation that reaches NO parser is NOT a factory', () => {
    // The case the old base case could not see. `parserCallName` returns
    // non-null for any name in PARSER_FACTORY_NAMES, so when it was the base
    // case of this derivation the list validated itself: these two qualify by
    // being NAMED, never by producing a parser.
    //
    // Both names are real entries in PARSER_FACTORY_NAMES, which is the point —
    // a synthetic pair with invented names would prove nothing about the branch
    // that fires on the declared list.
    //
    // Red-proof, predicted before the tamper: restore `parserCallName` as the
    // base case and this cell fails with SET = ['jsonParser', 'urlencodedParser']
    // and COUNT = 2.
    const delegatingOnly = [
      "import express from 'express';",
      'export function jsonParser(): RequestHandler {',
      '  return urlencodedParser();',
      '}',
      'export function urlencodedParser(): RequestHandler {',
      '  return jsonParser();',
      '}',
    ].join('\n');
    expect(
      parserFactoryExportsOf(delegatingOnly, 'request-limits.ts'),
      'Neither function reaches an express parser — they only call each other. A ' +
        'derivation that consults PARSER_FACTORY_NAMES calls both factories anyway, ' +
        'which means a factory that quietly stopped producing a parser would stay ' +
        'green forever.',
    ).toEqual([]);
  });

  it('CONTROL — the same pair DOES qualify once one of them actually reaches express', () => {
    // So the cell above is not passing because the derivation stopped working.
    //
    // KS-833 F-2 — the DELEGATOR IS DECLARED FIRST here, deliberately. With the
    // other order this cell still passes, but urlencodedParser qualifies within
    // pass 0 (the target is already marked when the loop reaches the delegator),
    // so the comment below would be false and the fixed point would never be
    // exercised by this cell at all. The pass index itself is pinned by the F-2
    // cell above; this ordering is what makes that pinning meaningful here.
    const oneReaches = [
      "import express from 'express';",
      'export function urlencodedParser(): RequestHandler {',
      '  return jsonParser();',
      '}',
      'export function jsonParser(): RequestHandler {',
      '  return express.json();',
      '}',
    ].join('\n');
    // urlencodedParser qualifies only on the SECOND pass, via the fixed point —
    // the behaviour the G-05 header claimed all along and did not have.
    expect(parserFactoryExportsOf(oneReaches, 'request-limits.ts')).toEqual([
      'jsonParser',
      'urlencodedParser',
    ]);
    expect(
      parserFactoryReachOf(oneReaches, 'request-limits.ts').passOf.get('urlencodedParser'),
      'and it really did take the second pass — otherwise the comment above is decoration',
    ).toBe(1);
  });

  it('🔴 KS-833 F-2 — which pass a delegator enters on is DECLARATION ORDER, not a law', () => {
    // The G-05 header used to say the presets "really do qualify on the second
    // pass". Measured against the real module, all eight enter on pass 0. The
    // mechanism: the inner loop walks `fns` in DECLARATION order, so when the
    // target is declared first it is already in `isFactory` by the time the
    // delegator is visited IN THE SAME PASS.
    //
    // Red-proof, run before the prose was corrected: a cell asserting the header
    // sentence as written (`passOf.get('urlencodedParser') > 0` on the
    // target-first source) failed with `expected 0 to be greater than 0`.
    //
    // This cell asserts BOTH orderings, so it cannot be satisfied by a fixed
    // point that never runs a second pass, nor by one that always does.
    const body = [
      'export function jsonParser(): RequestHandler {',
      '  return express.json();',
      '}',
    ];
    const delegator = [
      'export function urlencodedParser(): RequestHandler {',
      '  return jsonParser();',
      '}',
    ];
    const IMPORT = "import express from 'express';";

    const targetFirst = [IMPORT, ...body, ...delegator].join('\n');
    expect(
      parserFactoryReachOf(targetFirst, 'request-limits.ts').passOf.get('urlencodedParser'),
      'target declared first: the delegator qualifies within the SAME pass, because the ' +
        'target is already in isFactory when the loop reaches it',
    ).toBe(0);

    const delegatorFirst = [IMPORT, ...delegator, ...body].join('\n');
    expect(
      parserFactoryReachOf(delegatorFirst, 'request-limits.ts').passOf.get('urlencodedParser'),
      'delegator declared first: nothing is in isFactory when it is first visited, so it ' +
        'takes a SECOND pass — this is the case that actually exercises the fixed point',
    ).toBe(1);

    // And the answer is the same either way: order changes the pass, not the result.
    expect(parserFactoryReachOf(targetFirst, 'request-limits.ts').exports).toEqual(
      parserFactoryReachOf(delegatorFirst, 'request-limits.ts').exports,
    );
  });

  it('🔴 KS-833 Q-4a — an ARROW-CONST factory is detected, not just a declaration', () => {
    // `export const x = () => express.json()` is not a FunctionDeclaration, so
    // the declaration-only reader could not see it at all. A ninth factory
    // written in the spelling half this repo already uses elsewhere would have
    // been invisible to every leg.
    //
    // Red-proof, predicted before the tamper: with the reader restricted to
    // exported FunctionDeclarations this cell fails, `found` missing
    // 'ndjsonParser'.
    const withArrow =
      requestLimitsSource() +
      '\nexport const ndjsonParser = (): RequestHandler =>\n' +
      "  express.json({ type: 'application/x-ndjson' });\n";
    expect(parserFactoryExportsOf(withArrow, 'request-limits.ts')).toContain('ndjsonParser');
  });

  it('🔴 KS-833 Q-4b — a factory whose reach is inside a NON-EXPORTED helper is detected', () => {
    // The export filter used to be applied during COLLECTION, so a helper that
    // is not exported was never in the call graph and the exported factory that
    // delegates to it reached nothing. Reachability is a property of the graph;
    // being exported is a property of the answer.
    //
    // Red-proof, predicted before the tamper: same restriction, this cell fails,
    // `found` missing 'ndjsonParser'.
    const viaHelper =
      requestLimitsSource() +
      '\nfunction buildNdjson(): RequestHandler {\n' +
      "  return express.json({ type: 'application/x-ndjson' });\n}\n" +
      '\nexport function ndjsonParser(): RequestHandler {\n' +
      '  return buildNdjson();\n}\n';
    const found = parserFactoryExportsOf(viaHelper, 'request-limits.ts');
    expect(found).toContain('ndjsonParser');
    expect(
      found,
      'and the non-exported helper is NOT itself an answer — it carries the reach, ' +
        'it is not a factory the module offers',
    ).not.toContain('buildNdjson');
  });

  it('🔴 KS-833 Q-4c — a ninth factory exported by an EXPORT LIST is detected', () => {
    // THE SILENT ONE. Q-4a and Q-4b were misses the ninth-factory cell would
    // eventually surface. This one is different: `hasExport` reads MODIFIERS on
    // the declaration, and an `ExportDeclaration` sets none — so the factory is
    // collected, is marked a factory, and is then dropped from the ANSWER. The
    // answer is n = 8, which EQUALS `PARSER_FACTORY_NAMES`, so the equality cell
    // above stays GREEN. The leg's whole purpose — "a new factory missing from
    // the array is caught" — fails with no signal at all.
    //
    // Red-proof, predicted before the cell was written: against the modifier-only
    // `hasExport` this fails with `found` = the eight declared names and
    // 'ndjsonParser' absent, while the equality cell stays green — the silence
    // is the finding.
    const withExportList =
      requestLimitsSource() +
      '\nfunction ndjsonParser(): RequestHandler {\n' +
      "  return express.json({ type: 'application/x-ndjson' });\n}\n" +
      'export { ndjsonParser };\n';
    const found = parserFactoryExportsOf(withExportList, 'request-limits.ts');
    expect(found, 'an export-list factory is still an exported factory').toContain('ndjsonParser');
    expect(
      found,
      'and it makes the equality leg RED rather than passing silently — without this, ' +
        'n = 8 equals the array and the miss is invisible',
    ).not.toEqual([...PARSER_FACTORY_NAMES].sort());
  });

  it('🔴 KS-833 Q-4d — an ALIASED export-list ninth is detected under its EXPORTED name', () => {
    // `export { ndjsonImpl as ndjsonParser }`. The name a CONSUMER calls is
    // `ndjsonParser`, and that is the name `PARSER_FACTORY_NAMES` would have to
    // carry, so that is the name this derivation must answer with.
    //
    // NOTE — deliberate deviation from the gate report's fix-shape. The report
    // prescribes `(el.propertyName ?? el.name).text`, i.e. the LOCAL name; that
    // would answer 'ndjsonImpl' here, and the report's own stated regression
    // (`toContain('ndjsonParser')`) would not hold for this shape. The export
    // map below records local -> EXPORTED, which is identical for all eight
    // existing factories (a modifier export has local === exported) and answers
    // with the name that is actually callable.
    const withAlias =
      requestLimitsSource() +
      '\nfunction ndjsonImpl(): RequestHandler {\n' +
      "  return express.json({ type: 'application/x-ndjson' });\n}\n" +
      'export { ndjsonImpl as ndjsonParser };\n';
    const found = parserFactoryExportsOf(withAlias, 'request-limits.ts');
    expect(found, 'the exported alias is the callable name').toContain('ndjsonParser');
    expect(
      found,
      'and the private local name is NOT an answer — nobody outside the module can call it',
    ).not.toContain('ndjsonImpl');
  });

  it('CONTROL — a non-parser export added to that module is NOT swept up', () => {
    // The mirror of the cell above: the predicate must not fire on anything new.
    const withHelper =
      requestLimitsSource() +
      '\nexport function correlationId(): RequestHandler {\n' +
      '  return (_req, _res, next) => next();\n}\n';
    const found = parserFactoryExportsOf(withHelper, 'request-limits.ts');
    expect(found).not.toContain('correlationId');
    expect(found, 'and the leg stays green').toEqual([...PARSER_FACTORY_NAMES].sort());
  });
});

// KS-842 Q-6 — THE `tsc` FIGURE FOR THIS FILE IS MEANINGLESS WITHOUT ITS FLAGS.
//
// The three `readFileSync(new URL(import.meta.url))` reads below are `import.meta`
// under a package whose declared `module` is **commonjs**, so a DIRECT `tsc` on
// this file answers differently depending on how it is invoked. Measured, same
// file, same commit:
//
// KS-859 F-842-03. This block used to carry four counts (0 / 2 / 5 / 20). NONE
// of the last three reproduce, and the fourth never added up on its face —
// "2 x TS1259 and 15 x TS7006 on top" of 5 does not make 20. Re-measured at
// `50913d2c3` with EXACTLY the flags each line names:
//
//   tsc --noEmit -p tsconfig.json                          -> 0, and BLIND
//   tsc --noEmit --module es2022 <this file>               -> 78
//   tsc --noEmit --module commonjs --esModuleInterop \
//       --moduleResolution node <this file>                -> 35
//   ...the same without --esModuleInterop                  -> 48
//
// The counts moved because the file grew, and because a flag the original
// figures omitted (`--moduleResolution node` on the es2022 line) decides
// whether every import resolves at all. That is the block's own thesis landing
// on the block: A COUNT IS NOT A FACT ABOUT THIS FILE, IT IS A FACT ABOUT AN
// INVOCATION AT A COMMIT. Treat the numbers above as indicative at the SHA
// named, re-measure before citing, and never carry a count without the exact
// command beside it.
//
// The one durable claim here is structural, and it still holds: the package
// tsconfig's `exclude` lists `src/__tests__`, so `-p tsconfig.json` NEVER READS
// THIS FILE. Its 0 is a statement about coverage, not about correctness — which
// is the whole reason this block exists.
//
// NOT a behavioural defect: vitest runs this file as ESM and the cells below are
// correct there. Nothing in the gates catches the CommonJS delta — `-p` excludes
// the file, eslint is clean, vitest transpiles ESM happily — so this file is the
// only thing in `packages/shared/src` that would not compile under the package's
// own declared module system. Whether to align the read with that is the owner's
// call and is deliberately NOT changed here.
describe('KS-832 F-QA-H — this file can detect a control byte in its OWN source', () => {
  // The round that wrote this suite reported that "an assertion before commit
  // caught" literal NUL bytes arriving in a fixture. That assertion lived in
  // scratch tooling, not here. The tester planted a real 0x00 in this file and
  // 175/175 stayed green — in the file whose entire subject is control bytes.
  // The property was held by discipline. This holds it with a cell.
  //
  // Bytes, not a string: reading as utf8 and scanning the result would go
  // through a decoder that can normalise or replace, and the claim is about
  // what is ON DISK. `readFileSync` with no encoding returns the Buffer.
  //
  // Every NUL this suite needs is written as the two-character escape
  // `<backslash>u0000` or via String.fromCharCode(0), so a raw C0 byte here is
  // always an accident.
  const ALLOWED_C0 = new Set([0x09, 0x0a, 0x0d]); // tab, LF, CR

  function rawC0Bytes(buf: Buffer): { offset: number; byte: number }[] {
    const out: { offset: number; byte: number }[] = [];
    for (let i = 0; i < buf.length; i++) {
      const b = buf[i];
      // KS-842 Q-3 — the product's own class is C0-minus-whitespace PLUS DEL:
      // `[\u0000-\u0008\u000B\u000C\u000E-\u001F\u007F]` at
      // packages/shared/src/middleware/index.ts. This scan tested `b < 0x20`
      // only, so a raw 0x7F left the suite 195/195 GREEN while a raw 0x00
      // reddened it — in the file whose whole subject is control bytes. A raw
      // DEL landing in a fixture string changes what these fixtures test just
      // as silently as a NUL would.
      if ((b < 0x20 && !ALLOWED_C0.has(b)) || b === 0x7f) out.push({ offset: i, byte: b });
    }
    return out;
  }

  it('\u{1f534} no raw C0 byte appears in this file on disk', () => {
    const buf = readFileSync(new URL(import.meta.url)) as Buffer;
    const found = rawC0Bytes(buf);
    expect(
      found.map((f) => `0x${f.byte.toString(16).padStart(2, '0')} at byte ${f.offset}`),
      'a raw control byte reached this file — every NUL here must be an escape, never a byte',
    ).toEqual([]);
  });

  it('CONTROL — the reader actually read this file, so the case above is not "empty is empty"', () => {
    const buf = readFileSync(new URL(import.meta.url)) as Buffer;
    expect(buf.length, 'a truncated or missing read would make the scan vacuously clean').toBeGreaterThan(100_000);
    expect(buf.includes(Buffer.from('F-QA-H')), 'and it read THIS file, not another').toBe(true);
  });

  it('CONTROL — the predicate DOES fire on a raw C0 byte, so a clean result means something', () => {
    const planted = Buffer.concat([Buffer.from('abc'), Buffer.from([0x00]), Buffer.from('def')]);
    expect(rawC0Bytes(planted)).toEqual([{ offset: 3, byte: 0x00 }]);
    // KS-842 Q-3: the DEL row, beside the NUL row. Before the widening this
    // returned [] — the byte the product refuses was invisible to the scan.
    const plantedDel = Buffer.concat([Buffer.from('abc'), Buffer.from([0x7f]), Buffer.from('def')]);
    expect(rawC0Bytes(plantedDel), 'a raw DEL is a control byte here too').toEqual([
      { offset: 3, byte: 0x7f },
    ]);
    // and it is not "any low byte": the three legal whitespace bytes pass
    expect(rawC0Bytes(Buffer.from('a\tb\nc\rd'))).toEqual([]);
  });

  it('CONTROL — the escapes this suite deliberately writes are NOT raw bytes', () => {
    const buf = readFileSync(new URL(import.meta.url)) as Buffer;
    // NOTE the doubled backslash: `'\\u0000'` is the six-character escape TEXT
    // that appears in this file's source. Written singly it is a NUL at runtime
    // and this control silently searches for the very byte the case above
    // proves absent — which is exactly how it failed on first run.
    expect(buf.includes(Buffer.from('\\u0000')), 'the escape sequence is present as text').toBe(true);
    expect(rawC0Bytes(buf), 'and it contributes no raw C0 byte').toEqual([]);
  });
});

describe('KS-842 Q-1 — the conditional-reachability walk, across every lexical shape the gate probed', () => {
  // The #836 gate probed SIXTEEN lexical shapes against this walker and found
  // SIX SILENT FALSE CLEANS: a guard that may not run, read as a clean late=0
  // instead of the loud NULL. All six are decided LEXICALLY, inside one file,
  // by the same walk that already answers `if` / `?:` / `&&` / `case` — none is
  // the cross-file caller-graph question the scope note excludes.
  //
  // The whole table is asserted here as ONE battery, loud rows and clean rows
  // together, deliberately. A widening that simply answered NULL more often
  // would satisfy the six rows while destroying the instrument; the six CLEAN
  // controls are what makes that impossible.
  //
  // Blast radius when this was written: ZERO, censused not assumed — 25 guard
  // mounts in the corpus, 24 top-level, the 25th inside `createApp()` (a
  // function boundary, correctly unconditional). Latent instrument gap, not a
  // live exposure.
  const IMP =
    "import express from 'express';\n" +
    "import { rejectNulBytes } from '@secuura/shared';\n";
  const APP = 'const app = express();\napp.use(express.json());\n';
  const D = (body: string) =>
    analyseSource(IMP + APP + body, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts');

  // ---- THE SIX FALSE CLEANS. Each read late=0 before this ticket. ----

  it('🔴 a guard mounted in a CATCH clause reads NULL — it runs only on a throw', () => {
    // The likeliest real-world spelling of the class: "mount the guard only if
    // the optional thing failed". There was no isCatchClause check at all.
    expect(D('try { JSON.parse("{}"); } catch { app.use(rejectNulBytes()); }\n')).toBeNull();
  });

  it('🔴 a guard mounted in a FOR-OF body reads NULL — the iterable may be empty', () => {
    // `for (const r of routers) { r.use(guard) }` over an empty array is exactly
    // the "adding code turned a loud file quiet" mechanism KS-832 names.
    expect(D('for (const q of []) { app.use(rejectNulBytes()); }\n')).toBeNull();
  });

  it('🔴 a guard mounted in a WHILE body reads NULL — the loop may run zero times', () => {
    expect(D('while (process.env.NOPE) { app.use(rejectNulBytes()); }\n')).toBeNull();
  });

  it('🔴 a guard mounted in a classic FOR body reads NULL', () => {
    expect(D('for (let i = 0; i < 0; i += 1) { app.use(rejectNulBytes()); }\n')).toBeNull();
  });

  it('🔴 a guard inside an IIFE inside an if reads NULL — its caller is one line up', () => {
    // The function-boundary stop is right as a rule, but an immediately-invoked
    // arrow is not a caller-graph question.
    expect(D('if (process.env.NOPE) { (() => { app.use(rejectNulBytes()); })(); }\n')).toBeNull();
  });

  it('🔴 KS-859 — an IIFE spelled `.call(this)` reads NULL too, the spelling the walk did not follow', () => {
    // KS-842 closed `(() => { … })()`. `.call` and `.apply` are the same shape
    // reached through a property access. Censused at 50913d2c3: zero instances
    // under services/ + connectors/, so this was latent — but the walk claimed
    // IIFE transparency and only had one spelling of it.
    expect(
      D('if (process.env.NOPE) { (function () { app.use(rejectNulBytes()); }).call(this); }\n'),
    ).toBeNull();
  });

  it('🔴 KS-859 — and the `.apply(…)` spelling', () => {
    expect(
      D('if (process.env.NOPE) { (function () { app.use(rejectNulBytes()); }).apply(this, []); }\n'),
    ).toBeNull();
  });

  it('CONTROL — an UNCONDITIONAL `.call` IIFE is still CLEAN, so the fix is not "every .call is conditional"', () => {
    // Without this the two rows above are satisfied by a walk that treats any
    // `.call` as conditional, which would answer NULL for guards that really run.
    const a = D('(function () { app.use(rejectNulBytes()); }).call(this);\n');
    expect(a, 'the guard really does run, so the file must stay clean').not.toBeNull();
  });

  it('🔴 a helper whose BODY is conditional, called unconditionally, reads NULL', () => {
    // The mirror image of KS-832's own headline fixture, and the half the
    // suppression ORDER left open: `insideGuardHelper` runs first, so the inner
    // mount never reaches the conditionality test, and the credit is then taken
    // at an unconditional call site. The conditionality has to travel WITH the
    // helper to its call sites.
    expect(
      D(
        'function mountGuard(x: any) { if (process.env.NOPE) { x.use(rejectNulBytes()); } }\n' +
          'mountGuard(app);\n',
      ),
    ).toBeNull();
  });

  // ---- CONTROLS: guards that REALLY DO run must stay CLEAN. ----
  // Without these, "answer NULL more often" would pass every row above.

  it('CONTROL — a guard in a TRY block is clean: the block is entered unconditionally', () => {
    const a = D('try { app.use(rejectNulBytes()); } catch { /* nothing */ }\n');
    expect(a).not.toBeNull();
    expect(a!.lateAppLevel).toEqual([]);
  });

  it('CONTROL — a guard in a FINALLY block is clean: finally always runs', () => {
    const a = D('try { JSON.parse("{}"); } finally { app.use(rejectNulBytes()); }\n');
    expect(a).not.toBeNull();
    expect(a!.lateAppLevel).toEqual([]);
  });

  it('CONTROL — a DO-WHILE body is clean: it executes ONCE before the condition is read', () => {
    // DELIBERATE DEVIATION from the gate report's fix-shape, and the reason is
    // semantics rather than preference. §2 of that report groups
    // `do { … } while(false)` with the zero-iteration loops and its
    // recommendation lists `DoStatement` among the iteration statements to add.
    //
    // A do-while body runs EXACTLY ONCE before the condition is ever evaluated,
    // so the guard genuinely IS mounted. Treating it as conditional would make
    // this file read NULL while its guard really runs — a FALSE LOUD, which
    // sends a human to investigate a clean file. `while` stays conditional even
    // for `while (true)`, because the walker cannot evaluate a condition and
    // conservative-loud is right there. The asymmetry is real semantics.
    const a = D('do { app.use(rejectNulBytes()); } while (false);\n');
    expect(a, 'the guard runs — a NULL here would be a false loud').not.toBeNull();
    expect(a!.lateAppLevel).toEqual([]);
  });

  it('CONTROL — a bare block and a labelled block are clean', () => {
    const bare = D('{ app.use(rejectNulBytes()); }\n');
    expect(bare).not.toBeNull();
    expect(bare!.lateAppLevel).toEqual([]);
    const labelled = D('mount: { app.use(rejectNulBytes()); }\n');
    expect(labelled).not.toBeNull();
    expect(labelled!.lateAppLevel).toEqual([]);
  });

  it('CONTROL — a guard in the CONDITION itself is clean: the condition always evaluates', () => {
    const a = D('if (app.use(rejectNulBytes())) { /* nothing */ }\n');
    expect(a).not.toBeNull();
    expect(a!.lateAppLevel).toEqual([]);
  });

  it('CONTROL — a switch statement followed by an unconditional guard is clean', () => {
    const a = D('switch (1) { case 1: break; }\napp.use(rejectNulBytes());\n');
    expect(a).not.toBeNull();
    expect(a!.lateAppLevel).toEqual([]);
  });

  it('CONTROL — a helper with an UNCONDITIONAL body, called unconditionally, is clean', () => {
    // The mirror of the sixth red row: the conditionality must travel with the
    // helper only when it is actually there.
    const a = D('function mountGuard(x: any) { x.use(rejectNulBytes()); }\nmountGuard(app);\n');
    expect(a).not.toBeNull();
    expect(a!.lateAppLevel).toEqual([]);
  });

  // ---- The rows that were already loud, kept so a regression is visible. ----

  it('CONTROL — a CASE clause was already loud, and stays loud', () => {
    expect(D('switch (1) { case 1: app.use(rejectNulBytes()); break; }\n')).toBeNull();
  });

  it('CONTROL — an ELSE branch was already loud, and stays loud', () => {
    expect(D('if (process.env.NOPE) { /* nothing */ } else { app.use(rejectNulBytes()); }\n')).toBeNull();
  });

  it('CONTROL — a file with NO guard call at all is loud, the reference verdict', () => {
    expect(D('app.get("/x", (_q, s) => s.json({}));\n')).toBeNull();
  });
});

describe('KS-832 F-QA-D — a guard reachable ONLY through a conditional is not a clean position', () => {
  // Measured on the UNFIXED scanner before any of this was written. Two files
  // with the SAME runtime reality — no guard is mounted — and opposite verdicts:
  //   no call at all                          -> null    LOUD
  //   `if (process.env.NOPE) { mountGuard(app) }` -> late=0  CLEAN
  // Adding dead code turned a loud file quiet. Both spellings did it.
  const IMP =
    "import express from 'express';\n" +
    "import { rejectNulBytes } from '@secuura/shared';\n";
  const HELPER = 'function mountGuard(x: any) { x.use(rejectNulBytes()); }\n';
  const D = (src: string) =>
    analyseSource(src, '/x/services/qa/src/index.ts', 'services/qa/src/index.ts');

  it('\u{1f534} a guard-HELPER called only inside an if reads NULL, not clean', () => {
    const a = D(IMP + 'const app = express();\napp.use(express.json());\n' + HELPER + 'if (process.env.NOPE) { mountGuard(app); }\n');
    expect(a, 'measured late=0 guardLine=6 before the fix — a silent false clean').toBeNull();
  });

  it('\u{1f534} the INLINE spelling does it too — the half the finding did not name', () => {
    const a = D(IMP + 'const app = express();\napp.use(express.json());\nif (process.env.NOPE) { app.use(rejectNulBytes()); }\n');
    expect(a, 'measured late=0 guardLine=5 before the fix').toBeNull();
  });

  it('\u{1f534} THE ASYMMETRY IS CLOSED — the dead-conditional file and the no-call file now AGREE', () => {
    const deadConditional = D(IMP + 'const app = express();\napp.use(express.json());\n' + HELPER + 'if (process.env.NOPE) { mountGuard(app); }\n');
    const noCallAtAll = D(IMP + 'const app = express();\napp.use(express.json());\n' + HELPER);
    expect(noCallAtAll, 'the no-call file was always loud').toBeNull();
    expect(deadConditional, 'and the dead-conditional file must be exactly as loud').toBeNull();
  });

  it('CONTROL — an UNCONDITIONAL guard is unaffected, so the fix is not "everything is null now"', () => {
    const a = D(IMP + 'const app = express();\napp.use(express.json());\napp.use(rejectNulBytes());\n');
    expect(a, 'a real guard still resolves').not.toBeNull();
    expect(a!.guardLine).toBe(5);
    expect(a!.lateAppLevel, 'parser before guard is the SAFE order').toEqual([]);
  });

  it('CONTROL — the real defect is still LOUD: an unconditional guard BEFORE the parser', () => {
    const a = D(IMP + 'const app = express();\napp.use(rejectNulBytes());\napp.use(express.json());\n');
    expect(a).not.toBeNull();
    expect(a!.lateAppLevel.length, 'a parser mounted after the guard is the KS-800 defect').toBe(1);
  });

  it('CONTROL — one UNCONDITIONAL guard plus a conditional one still resolves on the unconditional', () => {
    const a = D(
      IMP + 'const app = express();\napp.use(rejectNulBytes());\napp.use(express.json());\n' +
      'if (process.env.NOPE) { app.use(rejectNulBytes()); }\n',
    );
    expect(a, 'the conditional one is ignored, not poisonous').not.toBeNull();
    expect(a!.guardLine, 'and the position is the unconditional one').toBe(4);
    expect(a!.lateAppLevel.length).toBe(1);
  });

  it('CONTROL — a ternary and a short-circuit are conditionals too, not just `if`', () => {
    const ternary = D(IMP + 'const app = express();\napp.use(express.json());\nprocess.env.NOPE ? app.use(rejectNulBytes()) : null;\n');
    const shortCircuit = D(IMP + 'const app = express();\napp.use(express.json());\nprocess.env.NOPE && app.use(rejectNulBytes());\n');
    expect(ternary, 'a ternary arm is conditional').toBeNull();
    expect(shortCircuit, 'and so is the right of &&').toBeNull();
  });
});

describe('KS-832 ACCEPTANCE BAR — a REAL corpus service, booted, driven over a raw socket', () => {
  // The #833 socket cell drives programs this file writes as strings. That is
  // synthetic by construction, and it carried a NOT-TESTED line saying so. This
  // one boots an actual corpus service - demo-service's exported `createApp()` -
  // and asserts the scanner's verdict against what that service really does with
  // a NUL on the wire.
  //
  // HOME, and why it is here rather than in demo-service: the scanner's verdict
  // and the runtime evidence for it belong in one file. Split across suites the
  // claim and its proof drift apart, which is how this round's residues happened.
  // The precedent for reaching outside the package is already in this suite -
  // `ks727-errorhandler-class-guard.test.ts` loads service modules with
  // `await import(pathToFileURL(file).href)`. Dynamic import by absolute path, so
  // there is NO static cross-package import and no new dependency edge.
  //
  // `createApp()` needs no DB and no redis; demo-service boots it in four of its
  // own tests. If it ever needs anything external this cell moves to
  // `systemTest/` - a package unit suite that depends on a running stack is the
  // KS-830 class, and that line is not crossed to keep the cell close to the
  // scanner.
  const APP_TS = join(DEV_ROOT, 'services', 'demo-service', 'src', 'app.ts');

  let server: Server | null = null;
  let port = 0;

  beforeAll(async () => {
    const mod = await import(pathToFileURL(APP_TS).href);
    const app = (mod as { createApp: () => express.Express }).createApp();
    // KS-859 F-842-02 — SURFACE THE PARSER'S OWN MARKER, not V8's prose.
    //
    // The RAW-0x00 cell below used to assert on the text of express's default
    // error page: `SyntaxError: Bad control character in string literal in JSON
    // at position 7`. That is doubly environment-bound, and both halves were
    // measured: the wording is V8's and is not a stable contract, and under
    // `NODE_ENV=production` express omits the message ENTIRELY, so the cell
    // goes red on the ambient environment rather than on the behaviour. A cell
    // that reds because of how the runner was invoked is a flake waiting for
    // whoever sets that variable.
    //
    // `err.type` is body-parser's own documented, machine-readable marker:
    // `entity.parse.failed` for a body it could not parse. It does not move
    // with V8's phrasing or with NODE_ENV. It must run FIRST among error
    // handlers. Since KS-844, demo-service mounts its own terminal JSON
    // `errorHandler` last in `createApp()`, so a marker appended after it would
    // never run: the marker's layer is spliced into the router stack
    // immediately BEFORE demo-service's error handler. It sets a header and
    // delegates with `next(err)`, so the status and body the other cells
    // assert on are demo-service's own.
    const markErrType: express.ErrorRequestHandler = (err, _req, res, next) => {
      const e = err as { type?: unknown; statusCode?: unknown };
      if (typeof e?.type === 'string') res.setHeader('x-test-err-type', e.type);
      if (typeof e?.statusCode === 'number') {
        res.setHeader('x-test-err-status', String(e.statusCode));
      }
      next(err);
    };
    app.use(markErrType);
    // KS-844: move the marker ahead of demo-service's own terminal errorHandler.
    const routerStack = (app as unknown as { _router: { stack: Array<{ name: string }> } })._router.stack;
    const markerLayer = routerStack.pop();
    expect(markerLayer?.name, 'the layer just mounted is the marker').toBe('markErrType');
    const handlerAt = routerStack.findIndex((layer) => layer.name === 'errorHandler');
    expect(handlerAt, "demo-service's errorHandler layer is mounted").toBeGreaterThan(-1);
    routerStack.splice(handlerAt, 0, markerLayer!);
    const listening = await listen(app);
    server = listening.server;
    port = Number(listening.base.split(':').pop());
  });

  afterAll(async () => {
    if (server) await close(server);
  });

  /** POST a JSON body to a path no router serves, over a real socket. */
  function post(body: Buffer): Promise<{ status: number; text: string }> {
    return new Promise((res, rej) => {
      const sock = netConnect(port, '127.0.0.1');
      const chunks: Buffer[] = [];
      sock.on('error', rej);
      sock.on('connect', () => {
        const head = Buffer.from(
          'POST /nope HTTP/1.1\r\nHost: 127.0.0.1\r\nContent-Type: application/json\r\n' +
            `Content-Length: ${body.length}\r\nConnection: close\r\n\r\n`,
          'latin1',
        );
        sock.write(Buffer.concat([head, body]));
      });
      sock.on('data', (d) => chunks.push(d as Buffer));
      sock.on('close', () => {
        const text = Buffer.concat(chunks).toString('latin1');
        const m = /^HTTP\/1\.1 (\d{3})/.exec(text);
        res({ status: m ? Number(m[1]) : 0, text });
      });
    });
  }

  it('the scanner reads this REAL service as late=0 - parser first, guard after', () => {
    const s = scan(APP_TS);
    expect(s, 'demo-service mounts a guard, so it is not null').not.toBeNull();
    expect(s!.lateAppLevel, 'no app-level parser sits after the guard').toEqual([]);
    expect(s!.postGuardParserSites, 'and no reachable one either').toEqual([]);
  });

  it('\u{1f534} an ESCAPED NUL in the body is refused BY NAME - the guard ran on a parsed body', async () => {
    const v = await post(Buffer.from('{"x":"a\\u0000b"}', 'latin1'));
    expect(v.status, 'the guard refuses it').toBe(400);
    expect(v.text, 'and it is the control-byte guard, named, not some other 400').toContain('VALIDATION_ERROR');
    expect(v.text.toUpperCase()).toContain('NUL');
  });

  it('CONTROL - a CLEAN body reaches routing and 404s, so the 400 above is the NUL and not the request shape', async () => {
    const v = await post(Buffer.from('{"x":"ab"}', 'latin1'));
    expect(v.status, 'same method, same path, same content type - only the NUL differs').toBe(404);
  });

  it('CONTROL - a RAW 0x00 byte is refused by the JSON PARSER, a different mechanism, and is labelled as such', async () => {
    const v = await post(Buffer.concat([Buffer.from('{"x":"a', 'latin1'), Buffer.from([0x00]), Buffer.from('b"}', 'latin1')]));
    expect(v.status, 'still refused').toBe(400);
    expect(v.text, 'but NOT by the control-byte guard - express.json rejects the bytes first').not.toContain('VALIDATION_ERROR');
    // KS-842 Q-4 - ASSERT THE POSITIVE. The negative above is satisfied by ANY
    // 400 that is not the guard's: a proxy's, a timeout's, an empty body, or a
    // future error handler returning a different code. It never names what the
    // mechanism IS, so it cannot notice if the mechanism changes - and this
    // cell's whole prose claims the refusal came from the JSON PARSER.
    // KS-859 F-842-02: assert body-parser's own marker, surfaced by the
    // test-local handler in beforeAll. `entity.parse.failed` is the parser
    // saying it could not parse the entity — stable across V8 versions and
    // across NODE_ENV, where the previous assertion on express's error prose
    // was measured red under `NODE_ENV=production`.
    expect(
      v.text,
      'the refusal must come from the JSON parser BY NAME - "not the guard" is not the same claim as "the parser"',
    ).toContain('x-test-err-type: entity.parse.failed');
  });
});
