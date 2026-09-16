// =============================================================================
// KS-727 CLASS GUARD — no error handler may put a thrown message into a 5xx
// response body, on any NODE_ENV
// =============================================================================
//
// CORPUS — what this guard covers, and what it does NOT. Read this before
// quoting it as evidence that the class is closed.
//
// The first version of this guard covered ONE corpus (exported `errorHandler`
// symbols) while its PR claimed the class. A through-code QA pass found the
// gap, and the site it missed was the internet-facing one: the api-gateway's
// global handler is written INLINE (`app.use((err, …) => …)`), so it was
// invisible to an export scan by construction. A guard's corpus is itself a
// claim about reach, and it inherits the blind spot of whatever found the
// instances. So the corpora are stated here with counts, including the count
// of what is not covered.
//
// Both corpora are stated below as EXACT SETS, and each set is asserted by a
// test that names its members. The counts here and the assertions in the file
// are the same object: if a count below is wrong, a test is red. That is the
// only form in which a corpus statement is worth reading — the previous
// version of this header carried corpus 2's PRE-EXTRACTION count while the
// tree held a different number, and nothing failed.
//
// CORPUS 1 — BEHAVIOURAL (the strong one).
//   What:  every `.ts` under `services/` and `packages/` that EXPORTS a symbol
//          matching /errorhandler/i with express error-middleware arity (4).
//   How:   each is imported and driven through a REAL express route, over a
//          real socket, across all six NODE_ENV values, asserting a per-run
//          canary never reaches the caller — on `message`, on `details`, and
//          on the payload-size path a filter answers itself.
//   Count today: 8 modules contributing 9 handlers. Both are exact sets
//          (`EXPECTED_CORPUS`, `EXPECTED_HANDLERS`): a member that vanishes
//          fails by name, and so does one that is added. The 9th handler is
//          api-gateway's `payloadTooLargeErrorHandler` — one module can
//          contribute more than one handler, which is why the handler set is
//          (file, export) pairs and not a count.
//   Of those 9, exactly 1 is a FILTER that forwards a typed 4xx rather than
//          answering it (`FORWARDING_HANDLERS`, also an exact set). A handler
//          that silently starts or stops forwarding is a red.
//
// CORPUS 2 — STRUCTURAL (the reach-extender).
//   What:  inline `app.use((err, …))` error middleware in service entrypoints
//          (`services/*/src/{index,app,server}.ts`) — the form corpus 1 cannot
//          see, because an inline arrow function is not an export and the
//          entrypoint cannot be imported without booting the service.
//   How:   every inline site is classified TERMINAL-ON-ANY-PATH (commits a
//          response on at least one path, whether or not it also forwards) or
//          PURE FORWARDER (commits none). A terminal-on-any-path inline
//          handler is a RED: it must be extracted to an exported module, which
//          lands it in corpus 1 and gets it driven for real.
//   Count today: 0 inline sites, across 0 files — an exact set
//          (`EXPECTED_INLINE_SITES`), so an added site is a red naming its own
//          file and line.
//   ⚠ The rule was WRONG until this commit and the count reflects the fix.
//          It classified on the PRESENCE of a `next(err)` anywhere in the
//          body, so a CONDITIONALLY terminal handler — one that answers some
//          errors itself and forwards the rest — was exempt. The live instance
//          was the api-gateway's 413 body-parser filter at
//          `services/api-gateway/src/index.ts:1071`: it owned the response
//          body on its 413 path while corpus 1 could not import it and corpus
//          2 excused it. It is now exported and driven. Before this change the
//          set held 1 member; the header said 3 across 2 files, which was the
//          count from before the two earlier extractions.
//
// NOT COVERED — stated, with today's counts, so nobody reads a green here as
// more than it is:
//   - Exported error middleware whose name does not match /errorhandler/i.
//     Direct arity-4 exports: 0. But the FACTORY form is not zero, and the
//     `.length === 4` discriminator cannot see it: `errorTrackingMiddleware`
//     (`packages/shared/src/errors/middleware.ts:21`, re-exported from
//     `errors/index.ts:16`) is an arity-1 function RETURNING an arity-4 error
//     middleware, and is mounted on the api-gateway between the payload filter
//     and the terminal handler. Count today: 1 published factory, plus 1
//     unpublished twin of it in `errors/tracking.ts:116`. Neither is a leak
//     surface — both call `next(err)` unconditionally and commit no response,
//     which is corpus 2's PURE FORWARDER disposition — but neither is covered,
//     and a future edit that gave one a response path would be invisible to
//     both corpora. (F-3, widened.)
//   - Inline error middleware outside the three entrypoint FILENAMES, or
//     mounted on a `Router` rather than `app`. Runtime count today: 0. There
//     is 1 such site in a test file, excluded deliberately — test fixtures are
//     not a leak surface.
//   - Error handling done INSIDE a route body (a `try/catch` that writes its
//     own response). Not covered at all, and unbounded — no count is claimed.
//     This is the largest uncovered surface and it is not addressed here.
//
// =============================================================================
// KS-727 fixed two handlers. The commit's own words were "the sweep found 12
// more services" — and a sweep is a measurement taken once. Nothing in the tree
// failed when a fourteenth handler kept the leak, which is exactly how
// `services/referral/src/middleware/errorHandler.ts` survived it: its gate is
// INVERTED relative to the one that was fixed
// (`=== 'development' ? leak : generic` rather than
// `=== 'production' ? generic : leak`), so a grep for the fixed pattern could
// not match it. A second copy in `packages/shared/src/errors/error-handler.ts`
// survived for the same reason, in the sibling file of the one that was fixed.
//
// This test replaces the sweep with a guard. It does not take a list of
// handlers; it DISCOVERS them by walking `services/` and `packages/`, then
// drives every one it finds through a real express route across every
// NODE_ENV value and asserts a per-run canary never reaches the caller. There
// is no glob to forget: a fifteenth handler is covered the moment it is
// written, and a handler that cannot be imported fails the run rather than
// being skipped.
//
// Walk-by-default is deliberate. The failure mode this guard exists to prevent
// is omission, and an allowlist of directories is an omission waiting to
// happen — so directories are pruned by an explicit SKIP list and everything
// else is in scope.
//
// Related: KS-658 (the demo VM runs every Node service as
// `NODE_ENV=development`, which is why "only leaks in development" is not a
// mitigation on this platform).
// =============================================================================

import { describe, it, expect, afterEach } from 'vitest';
import express from 'express';
import { readFileSync, readdirSync, existsSync } from 'node:fs';
import { join, resolve, relative } from 'node:path';
import { pathToFileURL } from 'node:url';
import { randomUUID } from 'node:crypto';
import type { AddressInfo } from 'node:net';
import { BadRequestError as SharedBadRequestError } from '../errors';
import { entrypoints as structuralEntrypoints, ENTRYPOINT_ROOTS } from './entrypoint-corpus';

/**
 * Locate the Blockchain/Dev root (the directory holding both `services/` and
 * `packages/`) by walking up from the working directory. Same idiom as
 * `crypto-agility.guard.test.ts`, so the two guards root themselves the same
 * way however vitest is invoked.
 *
 * @param start - directory to start the upward search from.
 * @returns absolute path to the Dev root.
 */
function findDevRoot(start: string): string {
  let dir = start;
  for (let i = 0; i < 10; i++) {
    if (existsSync(join(dir, 'services')) && existsSync(join(dir, 'packages'))) return dir;
    const parent = resolve(dir, '..');
    if (parent === dir) break;
    dir = parent;
  }
  throw new Error(`[ks727 class guard] could not locate the Dev root (services/ + packages/) from ${start}`);
}

const DEV_ROOT = findDevRoot(process.cwd());

/** Trees that hold first-party runtime source. Walked recursively, in full. */
const SCAN_ROOTS = ['services', 'packages'];

/**
 * Directories pruned during the walk. Everything NOT named here is in scope —
 * the inverse of an allowlist, so a new source directory is covered by default.
 */
const SKIP_DIRS = new Set(['node_modules', 'dist', 'build', 'coverage', '.git', '__tests__', 'tests']);

/**
 * Source of an `errorHandler` export, in any of the forms the tree actually
 * uses: a declaration (`export function errorHandler`, `export const
 * errorHandler`) or a re-export (`export { errorHandler }`, `export { x as
 * errorHandler }` — how `staking` and `vc-issuer` republish the shared one).
 */
const DECLARED = /^[ \t]*export[ \t]+(?:async[ \t]+)?(?:const|let|var|function)[ \t]+errorHandler\b/m;
const REEXPORTED = /^[ \t]*export[ \t]*\{[^}]*\berrorHandler\b[^}]*\}/m;

/** True if `source` exports a symbol named `errorHandler`. */
function exportsErrorHandler(source: string): boolean {
  return DECLARED.test(source) || REEXPORTED.test(source);
}

/**
 * Walk `dir` recursively and return every `.ts` file whose source exports an
 * `errorHandler`, pruning {@link SKIP_DIRS}. Declaration files are excluded:
 * a `.d.ts` has no runtime behaviour to drive.
 */
function findHandlerModules(dir: string, out: string[] = []): string[] {
  for (const entry of readdirSync(dir, { withFileTypes: true })) {
    const full = join(dir, entry.name);
    if (entry.isDirectory()) {
      if (SKIP_DIRS.has(entry.name)) continue;
      findHandlerModules(full, out);
    } else if (entry.name.endsWith('.ts') && !entry.name.endsWith('.d.ts')) {
      if (exportsErrorHandler(readFileSync(full, 'utf8'))) out.push(full);
    }
  }
  return out;
}

const HANDLER_FILES = SCAN_ROOTS.flatMap((root) => findHandlerModules(join(DEV_ROOT, root))).sort();

/** Every NODE_ENV the platform is ever set to, plus unset (a bare `node dist/`). */
const ENVS: (string | undefined)[] = ['production', 'development', 'demo', 'test', 'staging', undefined];

/** Per-run, so a stale assertion string cannot pass by coincidence. */
const CANARY = `CANARY-${randomUUID()}`;

/**
 * Handlers that legitimately FORWARD a typed 4xx rather than answering it —
 * filters, in corpus 2's vocabulary. Exact set, not a predicate: a handler
 * that starts forwarding, or stops, is a red here rather than a quiet change
 * of behaviour that the 4xx control would absorb.
 *
 * Keyed `<dev-root-relative path> → <export name>`.
 */
const FORWARDING_HANDLERS = new Set([
  'services/api-gateway/src/middleware/errorHandler.ts → payloadTooLargeErrorHandler',
]);

type Handler = (err: unknown, req: unknown, res: unknown, next: unknown) => void;

interface Discovered {
  /** Dev-root-relative path, used as the test name. */
  label: string;
  exportName: string;
  handler: Handler;
  /** The imported module, so a 4xx control can use its own error types. */
  module: Record<string, unknown>;
}

/**
 * Import every discovered module and collect its express error-handling
 * middleware: an exported function of arity 4 whose name mentions
 * `errorHandler`. Arity is the discriminator express itself uses.
 */
async function discover(): Promise<Discovered[]> {
  const found: Discovered[] = [];
  for (const file of HANDLER_FILES) {
    const label = relative(DEV_ROOT, file);
    // No try/catch: a module that cannot be imported must FAIL this run, not
    // vanish from the corpus. A silent skip here would recreate the very hole
    // this guard exists to close.
    const mod = (await import(pathToFileURL(file).href)) as Record<string, unknown>;
    for (const [exportName, value] of Object.entries(mod)) {
      if (typeof value === 'function' && value.length === 4 && /errorhandler/i.test(exportName)) {
        found.push({ label, exportName, handler: value as Handler, module: mod });
      }
    }
  }
  return found;
}

const HANDLERS = await discover();

/**
 * Drive `handler` through a REAL express app: a real route that fails, a real
 * `next(err)`, the handler mounted as real error middleware, and a real HTTP
 * request over a real socket. The response is read as raw text so a leak in
 * any field — `message`, `details`, anywhere — is visible, not just the one
 * field an assertion happened to name.
 *
 * @returns the response status and the whole body as text.
 */
async function driveThroughRoute(
  handler: Handler,
  err: unknown
): Promise<{ status: number; body: string; forwarded: boolean }> {
  const app = express();
  app.get('/boom', (_req, _res, next) => next(err));
  app.use(handler as express.ErrorRequestHandler);
  // A terminal backstop, mounted AFTER the handler under test.
  //
  // Corpus 1 now contains handlers that legitimately forward (a filter answers
  // some errors and passes the rest on — see corpus 2's classification). With
  // no backstop, a forwarded error reaches express's own final handler, which
  // serialises `err.stack` into the response body outside production. That
  // would read as a leak by the handler under test and it is not one: it is
  // the harness's own default. The backstop writes a CONSTANT body, so any
  // canary in a response is attributable to the handler.
  //
  // The header is how a caller tells "the handler forwarded" from "the handler
  // answered" — the two have different correct behaviours on the 4xx control.
  app.use(((_e, _req, res, _next) => {
    res.setHeader('x-ks727-backstop', '1');
    res.status(500).json({ error: { code: 'BACKSTOP', message: 'backstop answered' } });
  }) as express.ErrorRequestHandler);

  // KS-818 G-07: bind loopback. `app.listen(0)` binds `::`, so on a shared host
  // this probe server is briefly reachable off-box — the same shape already
  // fixed in `contentType.test.ts` and elsewhere in the KS-800 round.
  const server = app.listen(0, '127.0.0.1');
  try {
    await new Promise<void>((ok, fail) => {
      server.once('listening', () => ok());
      server.once('error', fail);
    });
    const { port } = server.address() as AddressInfo;
    const res = await fetch(`http://127.0.0.1:${port}/boom`);
    return {
      status: res.status,
      body: await res.text(),
      forwarded: res.headers.get('x-ks727-backstop') === '1',
    };
  } finally {
    await new Promise<void>((done) => server.close(() => done()));
  }
}

/**
 * A 4xx error each discovered handler can recognise: the module's own
 * `BadRequestError` when it exports one (auth defines a private hierarchy and
 * matches on `instanceof` against it), otherwise the shared one. The duck-typed
 * handler in `errors/error-handler.ts` reads plain `statusCode` / `code`
 * properties, which both constructors already set.
 */
function clientErrorFor(mod: Record<string, unknown>, message: string): Error {
  const Ctor = (typeof mod.BadRequestError === 'function' ? mod.BadRequestError : SharedBadRequestError) as new (
    m: string
  ) => Error;
  return new Ctor(message);
}

/** A 5xx whose internals live in `details` rather than `message`. */
function serverErrorWithDetails(message: string, details: string): Error {
  const err = new Error(message) as Error & { statusCode: number; code: string; details: string };
  err.statusCode = 500;
  err.code = 'INTERNAL_ERROR';
  err.details = details;
  return err;
}

// =============================================================================
// CORPUS 2 — inline `app.use((err, …))` error middleware in service entrypoints
// =============================================================================
// Corpus 1 can only see exports. The api-gateway's global handler is an inline
// arrow function inside `index.ts`, which is not an export and cannot be
// imported without booting the service — so it was outside corpus 1 by
// construction while carrying the exact defect KS-727 is about.
//
// The invariant here is structural rather than behavioural, and deliberately
// so: rather than trying to decide from source whether an inline handler leaks
// (which needs dataflow and would go red on the legitimate 4xx path, where
// authored text MUST survive), it requires that a TERMINAL error handler be an
// EXPORTED symbol. Exported means corpus 1 drives it for real. The rule needs
// no allowlist: the gateway's 413 body-parser filter passes on its merits,
// because it calls `next(err)` for everything it does not itself answer.
// =============================================================================


/**
 * Start of an inline express error middleware: `app.use((err …`, capturing the
 * parameter list so the response parameter can be named. The list is needed
 * because "does this body write a response?" is only answerable against the
 * identifier the handler actually bound the response to.
 */
const INLINE_SITE = /\.use\(\s*(?:async\s*)?\(\s*(err\b[^)]*)\)/g;

/** Response methods that COMMIT a response — the handler owns the body. */
const RESPONSE_WRITERS = 'status|json|send|sendStatus|end|redirect|render|jsonp';

interface InlineSite {
  /** Dev-root-relative path. */
  label: string;
  /** 1-based line number of the `app.use((err` token. */
  line: number;
  /** The handler's body source, brace-matched from the arrow. */
  body: string;
  /** True when the body hands unhandled errors onward via `next(err)`. */
  forwards: boolean;
  /** True when the body commits an HTTP response on at least one path. */
  writesResponse: boolean;
  /**
   * TERMINAL-ON-ANY-PATH — the site owns the response body on at least one
   * path, whether or not it forwards on the others.
   *
   * This is the corrected rule, and the correction is the point of it. The
   * first version classified a site as an exempt FILTER on the mere PRESENCE
   * of a `next(err)` anywhere in its body. That reads one token and draws a
   * conclusion about every path. The api-gateway's 413 body-parser filter
   * answers `entity.too.large` ITSELF and forwards the rest, so it owned a
   * response body on a live path while sitting outside both corpora by
   * construction: corpus 1 could not import it (inline), and corpus 2 excused
   * it (it forwards). A leak added to its 413 branch would have been invisible
   * to a guard whose whole subject is exactly that leak.
   *
   * A site is exempt only if it commits NO response at all — a pure forwarder,
   * which by construction cannot leak because it never writes a body.
   */
  isTerminal: boolean;
}

/**
 * Extract the balanced `{ … }` block that follows `from`, respecting string
 * literals, template literals AND comments, so neither a brace inside a
 * message nor an apostrophe inside a comment can unbalance the scan.
 *
 * Comments are not a nicety here. The first version of this function tracked
 * quotes but not comments, so the apostrophe in originate's own
 * `// … the endpoint's own error shape …` opened a string that never closed,
 * brace counting stopped, and the extracted "body" ran to the end of the file.
 * It was caught by diffing the edit it drove, not by this scan complaining —
 * the scan reported success. Hence the control below.
 *
 * @returns the block source including its braces, or '' if none is found.
 */
function balancedBlockAfter(source: string, from: number): string {
  const open = source.indexOf('{', from);
  if (open === -1) return '';
  let depth = 0;
  let quote: string | null = null;
  let comment: 'line' | 'block' | null = null;
  for (let i = open; i < source.length; i++) {
    const ch = source[i];
    const next = source[i + 1];
    const prev = source[i - 1];
    if (comment === 'line') {
      if (ch === '\n') comment = null;
      continue;
    }
    if (comment === 'block') {
      if (ch === '*' && next === '/') { comment = null; i++; }
      continue;
    }
    if (quote) {
      if (ch === quote && prev !== '\\') quote = null;
      continue;
    }
    if (ch === '/' && next === '/') { comment = 'line'; i++; continue; }
    if (ch === '/' && next === '*') { comment = 'block'; i++; continue; }
    if (ch === '"' || ch === "'" || ch === '`') { quote = ch; continue; }
    if (ch === '{') depth++;
    else if (ch === '}') {
      depth--;
      if (depth === 0) return source.slice(open, i + 1);
    }
  }
  return '';
}

/**
 * Every entrypoint, across every root — a file that CREATES THE EXPRESS APP.
 *
 * KS-833 Q-1: this was a `{index,app,server}.ts` name list, and it was the
 * surviving half of a pair. KS-818 G-08 deleted the copy in ks781 and left this
 * one live, then wrote a comment in ks781 saying the array "was deleted" —
 * false of the file it pointed at. Measured at `904ca6ef2`: the list collected
 * 23 of the 24 app-creating files under `services/*\/src`, missing
 * `services/mcp-server/src/http-server.ts`, and could not see
 * `connectors/whatsapp-bot/src/index.ts` at all because it never left
 * `services/`.
 *
 * The derivation now lives in ONE place, imported by this suite and by ks781,
 * because a corpus two suites derive separately is how this defect happened.
 */
function entrypointFiles(): string[] {
  return structuralEntrypoints(DEV_ROOT);
}

/**
 * The name the handler bound its response parameter to, or `null` when the
 * signature is too short to have one (`(err, req)` cannot write a response).
 *
 * Reading the identifier rather than assuming `res` matters: the site this
 * whole corpus exists for was written `(err: any, _req: Request, res:
 * Response, next: any)`, and the tree also contains `_res` spellings. A
 * hard-coded `res` would silently report "writes no response" for a handler
 * that writes one, which is the direction of error this guard cannot afford.
 */
function responseParamName(paramList: string): string | null {
  const params = paramList.split(',').map((x) => x.trim());
  if (params.length < 3) return null;
  const ident = params[2].split(':')[0].trim();
  return /^[A-Za-z_$][\w$]*$/.test(ident) ? ident : null;
}

/**
 * Classify every inline error-middleware site in `source`.
 *
 * Source-callable rather than file-callable on purpose. The controls below
 * have to prove this classifier still works WITHOUT depending on the tree
 * containing an inline site — and the tree containing none is the guard's own
 * goal. A classifier that can only be exercised against the repository is one
 * whose controls go red exactly when the codebase gets healthy.
 *
 * @param source - file contents to scan.
 * @param label - name to report the sites under (a path, or a fixture name).
 */
function findInlineSitesIn(source: string, label: string): InlineSite[] {
  const sites: InlineSite[] = [];
  INLINE_SITE.lastIndex = 0;
  let m: RegExpExecArray | null;
  while ((m = INLINE_SITE.exec(source)) !== null) {
    const body = balancedBlockAfter(source, m.index);
    const resName = responseParamName(m[1]);
    const writesResponse =
      resName !== null && new RegExp(`\\b${resName}\\s*\\.\\s*(?:${RESPONSE_WRITERS})\\s*\\(`).test(body);
    sites.push({
      label,
      line: source.slice(0, m.index).split('\n').length,
      body,
      forwards: /\bnext\s*\(\s*err\b/.test(body),
      writesResponse,
      isTerminal: writesResponse,
    });
  }
  return sites;
}

/** Every inline site across every service entrypoint, classified. */
function findInlineSites(): InlineSite[] {
  return entrypointFiles().flatMap((file) =>
    findInlineSitesIn(readFileSync(file, 'utf8'), relative(DEV_ROOT, file))
  );
}

const INLINE_SITES = findInlineSites();

/**
 * Independent count of inline sites in `source`, by a plain line scan rather
 * than the brace-matching parser above. If the two disagree the parser is
 * broken, and "zero terminal handlers" would be an artefact rather than a
 * measurement. Also source-callable, so the agreement can be demonstrated on a
 * fixture with a known non-zero answer — on a clean tree both instruments
 * return 0, and 0 === 0 proves nothing about either.
 */
function independentInlineCountIn(source: string): number {
  return source.split('\n').filter((line) => /\.use\(\s*(?:async\s*)?\(\s*err\b/.test(line)).length;
}

/** The same independent count, across every service entrypoint. */
function independentInlineCount(): number {
  return entrypointFiles().reduce((n, file) => n + independentInlineCountIn(readFileSync(file, 'utf8')), 0);
}

/**
 * A fixture carrying one of each disposition, with a known answer. This is
 * what the corpus-2 controls assert against, so they test the INSTRUMENT and
 * fail only when the instrument breaks — never because the repository reached
 * the state this guard is trying to bring about.
 *
 * Site 1 is the shape the old rule got wrong: it answers one error class
 * itself and forwards the rest. Under `isFilter = has next(err)` it was exempt.
 */
const CLASSIFIER_FIXTURE = [
  "app.use((err: any, _req: Request, res: Response, next: any) => {",
  "  if (err.type === 'entity.too.large') {",
  "    res.status(413).json({ success: false, error: { message: 'Payload too large' } });",
  '    return;',
  '  }',
  '  next(err);',
  '});',
  'app.use((err, req, res, next) => {',
  "  // pass it on, keeping the endpoint's own error shape",
  '  next(err);',
  '});',
  'app.use((err, req, res) => {',
  '  res.status(500).json({ error: err.message });',
  '});',
].join('\n');

describe('KS-727 class guard — no exported errorHandler leaks a thrown message on a 5xx', () => {
  const originalNodeEnv = process.env.NODE_ENV;
  afterEach(() => {
    if (originalNodeEnv === undefined) delete process.env.NODE_ENV;
    else process.env.NODE_ENV = originalNodeEnv;
  });

  // ---------------------------------------------------------------------------
  // Controls first. Each can fail independently of the assertions it guards —
  // a null result from the tests below only means something if these pass.
  // ---------------------------------------------------------------------------

  it('CONTROL — the discovery finds EXACTLY the known corpus, so half of it cannot vanish silently', () => {
    // A broken walk, a bad regex or a moved Dev root would return [] and every
    // parameterised test below would silently not exist.
    //
    // This was a floor (`> 3`) against a real corpus of six, which meant half
    // the corpus could disappear and the control would still pass — the same
    // shape of defect as the guard's original corpus gap. It is now the exact
    // set: a member that vanishes fails here by name, and a member that is
    // ADDED fails here too, which is deliberate. A new error handler must be
    // added to this list consciously, and that is the moment someone reads the
    // rest of this file.
    const EXPECTED_CORPUS = [
      'packages/shared/src/errors/error-handler.ts',
      'packages/shared/src/errors/index.ts',
      'services/api-gateway/src/middleware/errorHandler.ts',
      'services/auth/src/middleware/errorHandler.ts',
      'services/demo-service/src/middleware/errorHandler.ts',
      'services/originate/src/middleware/errorHandler.ts',
      'services/referral/src/middleware/errorHandler.ts',
      'services/staking/src/middleware/errorHandler.ts',
      'services/vc-issuer/src/middleware/errorHandler.ts',
    ];
    expect(HANDLER_FILES.map((f) => relative(DEV_ROOT, f)).sort()).toEqual(EXPECTED_CORPUS);

    // The DRIVEN set, also exact. `>= EXPECTED_CORPUS.length` was a floor, and
    // a floor over a corpus of eight is the same shape of defect the file
    // corpus above was just fixed for: a module could stop exporting a handler
    // and another could start exporting two, and the count would still pass.
    // One file may contribute more than one handler — api-gateway contributes
    // both the terminal handler and the payload-size filter — so this is a set
    // of (file, export) pairs rather than a count.
    const EXPECTED_HANDLERS = [
      'packages/shared/src/errors/error-handler.ts → errorHandler',
      'packages/shared/src/errors/index.ts → errorHandler',
      'services/api-gateway/src/middleware/errorHandler.ts → errorHandler',
      'services/api-gateway/src/middleware/errorHandler.ts → payloadTooLargeErrorHandler',
      'services/auth/src/middleware/errorHandler.ts → errorHandler',
      'services/demo-service/src/middleware/errorHandler.ts → errorHandler',
      'services/originate/src/middleware/errorHandler.ts → errorHandler',
      'services/referral/src/middleware/errorHandler.ts → errorHandler',
      'services/staking/src/middleware/errorHandler.ts → errorHandler',
      'services/vc-issuer/src/middleware/errorHandler.ts → errorHandler',
    ];
    expect(HANDLERS.map((h) => `${h.label} → ${h.exportName}`).sort()).toEqual(EXPECTED_HANDLERS);

    // Every file the scan matched must yield a drivable handler. A file that
    // exports the name but not an arity-4 function means the matcher and the
    // corpus have drifted apart.
    expect(new Set(HANDLERS.map((h) => h.label)).size).toBe(HANDLER_FILES.length);

    // And every declared forwarder must actually be in the corpus — otherwise
    // the 4xx control's expectation below is written against a handler that no
    // longer exists and would silently stop being checked.
    for (const key of FORWARDING_HANDLERS) expect(EXPECTED_HANDLERS).toContain(key);
  });

  it('CONTROL — the export matcher accepts every form in the tree and rejects near-misses', () => {
    expect(exportsErrorHandler('export function errorHandler(err, req, res, next) {}')).toBe(true);
    expect(exportsErrorHandler('export const errorHandler = (e, q, s, n) => {};')).toBe(true);
    expect(exportsErrorHandler('export { errorHandler };')).toBe(true);
    expect(exportsErrorHandler('export { shared as errorHandler };')).toBe(true);
    // Near-misses that must NOT enter the corpus, or the matcher is matching
    // on the substring rather than on an export.
    expect(exportsErrorHandler("import { errorHandler } from '@secuura/shared';")).toBe(false);
    expect(exportsErrorHandler("const logger = createLogger('referral-error-handler');")).toBe(false);
    expect(exportsErrorHandler('export function errorHandlerFactory() {}')).toBe(false);
  });

  it('CONTROL — a deliberately leaky handler DOES leak through this harness', async () => {
    // The independent control. Without it, every assertion below would also
    // pass if the route never ran, the request never reached the handler, or
    // the body were read empty — a green that means nothing. This proves the
    // harness can observe the exact leak it claims the real handlers do not
    // have.
    // FOUR declared parameters, and the count is load-bearing. Express decides
    // whether a function is error middleware by `fn.length`, so the arity-3
    // version this fixture used to have was mounted as ORDINARY middleware and
    // never ran: the CANARY this control observed was produced by express's own
    // default error handler, not by the fixture. The control passed, and it was
    // not testing what it said. The terminal backstop is what exposed it — with
    // a constant-writing handler mounted last, there is no longer a leaky
    // default to borrow a green from.
    const leaky: Handler = (err, _req, res, _next) => {
      (res as express.Response).status(500).json({ error: { message: (err as Error).message } });
    };
    const { status, body } = await driveThroughRoute(leaky, new Error(CANARY));
    expect(status).toBe(500);
    expect(body).toContain(CANARY);
  });

  // ---------------------------------------------------------------------------
  // The guard.
  // ---------------------------------------------------------------------------

  for (const { label, exportName, handler, module } of HANDLERS) {
    describe(`${label} → ${exportName}`, () => {
      for (const env of ENVS) {
        it(`does not return the thrown message when NODE_ENV is ${env ?? 'unset'}`, async () => {
          if (env === undefined) delete process.env.NODE_ENV;
          else process.env.NODE_ENV = env;

          const { status, body } = await driveThroughRoute(handler, new Error(CANARY));

          expect(status).toBeGreaterThanOrEqual(500);
          expect(body).not.toContain(CANARY);
        });
      }

      it('does not return the thrown message on a payload-size error either', async () => {
        // The class widened when the gateway's 413 filter was extracted into
        // this corpus (ask 2): a handler that ANSWERS a typed error owns that
        // response body, so the leak question has to be asked on the answering
        // path too, not only on the generic 5xx path above. Handlers that do
        // not recognise the type forward it to the backstop, which is also a
        // pass — the assertion is about the canary, not about the status.
        //
        // No `statusCode` is set deliberately. A `statusCode: 413` would make
        // this a typed 4xx, whose authored text MUST survive by this guard's
        // own doctrine, and the assertion would then be testing the opposite
        // of the platform's intended behaviour.
        process.env.NODE_ENV = 'development';
        const oversize = new Error(CANARY) as Error & { type: string };
        oversize.type = 'entity.too.large';

        const { status, body } = await driveThroughRoute(handler, oversize);

        expect(status).toBeGreaterThanOrEqual(400);
        expect(body).not.toContain(CANARY);
      });

      it('does not return internals through a `details` channel on a 5xx', async () => {
        // `errors/error-handler.ts` carries a second, independent path —
        // `if (!isProduction && err.details)` — that the message assertion
        // above cannot see, because a plain Error has no `details`. Asserting
        // the message alone would have claimed a coverage this test did not
        // have.
        process.env.NODE_ENV = 'development';
        const { body } = await driveThroughRoute(handler, serverErrorWithDetails('boom', CANARY));
        expect(body).not.toContain(CANARY);
      });

      it('CONTROL — an authored client error still reaches the caller', async () => {
        // Without this, a handler rewritten to answer a constant for
        // everything would pass every assertion above. Typed 4xx text is
        // authored by us and must survive; only thrown internals are redacted.
        //
        // A FILTER has a different correct behaviour: it does not answer a 4xx
        // at all, it passes it to the next handler. Both are asserted, and
        // which one applies is read from the exact `FORWARDING_HANDLERS` set
        // rather than from what the handler happens to do — so a handler that
        // silently starts (or stops) forwarding is a red here, not an
        // absorbed change. `expect(forwarded).toBe(shouldForward)` is the
        // assertion doing that work; the branch below only says what each
        // disposition must then look like.
        const authored = 'provider and code are required';
        const shouldForward = FORWARDING_HANDLERS.has(`${label} → ${exportName}`);
        for (const env of ['development', 'production', undefined]) {
          if (env === undefined) delete process.env.NODE_ENV;
          else process.env.NODE_ENV = env;
          const { status, body, forwarded } = await driveThroughRoute(handler, clientErrorFor(module, authored));

          expect(forwarded).toBe(shouldForward);
          if (shouldForward) {
            // The backstop answered, which proves the error traversed this
            // handler intact rather than being swallowed by it.
            expect(status).toBe(500);
            expect(body).toContain('backstop answered');
          } else {
            expect(status).toBe(400);
            expect(body).toContain(authored);
          }
        }
      });
    });
  }
});

// =============================================================================
// CORPUS 2 — the reach-extender
// =============================================================================

describe('KS-727 class guard (corpus 2) — no service entrypoint answers errors from an inline handler', () => {
  // ---------------------------------------------------------------------------
  // Controls. Each runs against a FIXTURE with a known answer, not against the
  // repository.
  //
  // The previous version asserted `INLINE_SITES.length > 0` and
  // `filters.length > 0` to prove the scan was not vacuous. Both were read off
  // the tree — and the tree reaching zero inline sites is precisely what this
  // guard exists to bring about. They were controls built to go red on
  // success, and they did: extracting the gateway's 413 filter, which is the
  // fix this rule demands, takes the entrypoint corpus to zero. A control must
  // fail when the instrument breaks and at no other time; a claim about the
  // tree belongs in the exact set below, where a change reads as a diff rather
  // than as a broken control.
  // ---------------------------------------------------------------------------

  it('CONTROL — the classifier returns the known answer on a fixture of all three dispositions', () => {
    const sites = findInlineSitesIn(CLASSIFIER_FIXTURE, 'fixture');
    expect(sites).toHaveLength(3);

    // 1. CONDITIONALLY TERMINAL — answers `entity.too.large` itself, forwards
    //    the rest. This is the regression this ask fixed: under the old rule
    //    (`isFilter = body contains next(err)`) the site was exempt, and it is
    //    the exact shape that was live at `services/api-gateway/src/index.ts`.
    //    If this assertion is ever softened back to `false`, the gateway's 413
    //    branch leaves the corpus again.
    expect(sites[0].writesResponse).toBe(true);
    expect(sites[0].forwards).toBe(true);
    expect(sites[0].isTerminal).toBe(true);

    // 2. PURE FORWARDER — commits no response, so it cannot leak one. The only
    //    disposition this rule exempts.
    expect(sites[1].writesResponse).toBe(false);
    expect(sites[1].forwards).toBe(true);
    expect(sites[1].isTerminal).toBe(false);

    // 3. FULLY TERMINAL — answers everything, forwards nothing.
    expect(sites[2].writesResponse).toBe(true);
    expect(sites[2].forwards).toBe(false);
    expect(sites[2].isTerminal).toBe(true);
  });

  it('CONTROL — both enumerations agree on a fixture with a known non-zero count', () => {
    // On a clean tree both instruments return 0, and `0 === 0` says nothing
    // about either. The agreement has to be demonstrated where a disagreement
    // is possible, which is a fixture that actually contains sites.
    expect(findInlineSitesIn(CLASSIFIER_FIXTURE, 'fixture')).toHaveLength(3);
    expect(independentInlineCountIn(CLASSIFIER_FIXTURE)).toBe(3);
  });

  it('CONTROL — the response parameter is read from the signature, not assumed', () => {
    // A hard-coded `res` would report "writes no response" for a handler that
    // writes one — the direction of error this guard cannot afford. The live
    // site was `(err: any, _req: Request, res: Response, next: any)`, and the
    // tree also spells it `_res`.
    expect(responseParamName('err: any, _req: Request, res: Response, next: any')).toBe('res');
    expect(responseParamName('err, req, _res, next')).toBe('_res');
    expect(responseParamName('err, req')).toBeNull();

    // And the writer detection must key on THAT identifier, not on any `.json(`
    // in the body — otherwise a logger call would read as a response.
    const loggerOnly = ['app.use((err, req, response, next) => {', '  logger.json(err);', '  next(err);', '});'].join(
      '\n'
    );
    expect(findInlineSitesIn(loggerOnly, 'fixture')[0].writesResponse).toBe(false);

    const realWrite = ['app.use((err, req, response, next) => {', '  response.status(500).end();', '});'].join('\n');
    expect(findInlineSitesIn(realWrite, 'fixture')[0].writesResponse).toBe(true);
  });

  it('CONTROL — the block extractor is not fooled by an apostrophe in a comment, or a brace in a string', () => {
    // This control exists because the omission it tests for actually happened,
    // in the throwaway script that performed the original extraction. Tracking
    // quotes but not comments makes `endpoint's` open a string that never
    // closes; brace counting then stops and the "body" runs to EOF. The failure
    // is silent — the extractor returns a long string and reports success — so
    // it can only be caught by asserting on a known answer.
    const withApostropheInComment = [
      'app.use((err, req, res, next) => {',
      "  // translate them into the endpoint's own error shape",
      '  next(err);',
      '});',
      'const AFTER_THE_BLOCK = 1;',
    ].join('\n');
    const body = balancedBlockAfter(withApostropheInComment, 0);
    expect(body.endsWith('}')).toBe(true);
    expect(body).not.toContain('AFTER_THE_BLOCK');
    expect(/\bnext\s*\(\s*err\b/.test(body)).toBe(true);

    // A brace inside a string literal must not close the block either.
    const withBraceInString = 'app.use((err, req, res) => {\n  res.json({ m: "a } b" });\n});\nconst TAIL = 1;';
    const body2 = balancedBlockAfter(withBraceInString, 0);
    expect(body2).not.toContain('TAIL');
    expect(body2.endsWith('}')).toBe(true);
  });

  it('CONTROL — the two enumerations agree on the tree as well', () => {
    // Weak on a clean tree by construction (0 === 0) and kept anyway: it is
    // the one control that would catch the parser and the line scan drifting
    // apart on a tree that DOES contain a site. The fixture control above is
    // what carries the non-vacuity.
    expect(INLINE_SITES.length).toBe(independentInlineCount());
  });

  // ---------------------------------------------------------------------------
  // The tree. Stated as an exact set, so a new inline site is a red that names
  // itself rather than an absence nobody notices.
  // ---------------------------------------------------------------------------

  it('the entrypoint inline-site corpus is exactly the declared set', () => {
    // Empty today. It held ONE member before this change —
    // `services/api-gateway/src/index.ts:1071`, the 413 body-parser filter —
    // which the corrected classification made a red, and which is now exported
    // as `payloadTooLargeErrorHandler` and driven by corpus 1.
    //
    // An added inline site fails here by name and line. That is deliberate: the
    // rule below says what is forbidden, and this says what is present, and the
    // second is what makes a silent addition impossible.
    const EXPECTED_INLINE_SITES: string[] = [];
    expect(INLINE_SITES.map((s) => `${s.label}:${s.line}`)).toEqual(EXPECTED_INLINE_SITES);
  });

  it('every inline error handler in a service entrypoint is a pure forwarder — terminal-on-any-path ones must be exported', () => {
    // The invariant. A site that commits a response on ANY path owns that
    // response body, and being inline, corpus 1 cannot import it, cannot drive
    // it through a route, and cannot see whether it leaks. That is exactly how
    // the api-gateway's global handler kept the KS-727 construct through a PR
    // that claimed to close the class — and, on the corrected rule, how its 413
    // filter kept a second, smaller version of the same blind spot.
    //
    // The fix for a red here is not to soften this test: extract the handler
    // into `services/<svc>/src/middleware/errorHandler.ts` and export it under
    // a name matching /errorhandler/i. It then enters corpus 1 and gets driven
    // for real across every NODE_ENV value, which is the coverage the class
    // claim actually needs.
    const terminal = INLINE_SITES.filter((s) => s.isTerminal).map((s) => `${s.label}:${s.line}`);
    expect(terminal).toEqual([]);
  });
});

describe('KS-833 Q-1 — the corpus is every file that CREATES an express app, not every blessed filename', () => {
  // RED-PROOF, predicted in writing before the run: against the UNFIXED
  // `entrypointFiles()` (the `{index,app,server}.ts` name list) this cell fails
  // with SET = { services/mcp-server/src/http-server.ts,
  // connectors/whatsapp-bot/src/index.ts } and COUNT = 2.
  //
  // The ticket said "the 24th file", singular. That was written from a
  // services-only walk. Rooting the corpus the KS-800 way finds a second: the
  // whatsapp-bot creator ks781 already knows about, which mounts express.json()
  // and took POST /webhook from Meta's Cloud API. Widening stated as a widening.
  //
  // KS-833 F-4 — RETITLED. This cell used to be called "every file that creates
  // an express app is IN the corpus", which describes a COMPLETENESS property.
  // It cannot test that. At the head `entrypointFiles()` is
  // `return structuralEntrypoints(DEV_ROOT)`, so both sides of the comparison
  // are the SAME CALL: the only thing it can fail on is the WIRING — a local
  // copy of the corpus creeping back in, which T-1 proves it catches loudly.
  //
  // The gate measured the gap: T-3 narrowed the READER (it disabled the
  // `require('express')` branch) and all three cells in this describe stayed
  // GREEN at 94/94. Completeness of the reader is now pinned where it belongs,
  // in the module's own suite — `entrypoint-corpus.test.ts`, added by the same
  // PR — which reds on exactly that tamper.
  it('🔴 this suite\'s corpus IS the shared derivation — no local copy has crept back', () => {
    const structural = structuralEntrypoints(DEV_ROOT).map((f) => relative(DEV_ROOT, f)).sort();
    const collected = entrypointFiles().map((f) => relative(DEV_ROOT, f)).sort();
    expect(
      structural.filter((f) => !collected.includes(f)),
      'This suite is reading a corpus that is NOT the shared derivation, so every ' +
        'assertion in this file is blind to whatever the two disagree about. That is ' +
        'how mcp-server/src/http-server.ts stayed outside a name-list corpus while ' +
        'KS-818 G-08 deleted the OTHER copy of that list and left a comment saying it ' +
        'had deleted this one. NOTE: this cell does NOT test that the shared reader ' +
        'is CORRECT — see entrypoint-corpus.test.ts for that (KS-833 F-4).',
    ).toEqual([]);
  });

  it('CONTROL — the structural walk is not empty, so the case above is not "empty is empty"', () => {
    expect(structuralEntrypoints(DEV_ROOT).length).toBeGreaterThan(20);
  });

  it('🔴 the ROOTS are pinned — narrowing the walk is the mistake this has already made twice', () => {
    // Written as a pinned literal, not as a loop over ENTRYPOINT_ROOTS.
    //
    // The first version of this cell DID loop over the constant, asserting that
    // every root in the list contributes an entrypoint. Measured under the
    // red-proof (`connectors` deleted from the helper): it stayed GREEN at
    // 94/94, because a narrowed list simply means the loop checks fewer roots.
    // A control that reads the value it is guarding cannot fail. The tamper
    // caught it; ks781 reddened on the same tamper and this file did not.
    //
    // Widening the roots is welcome and should update this line deliberately.
    // Narrowing them silently is the defect.
    expect([...ENTRYPOINT_ROOTS]).toEqual(['services', 'connectors']);
    const all = structuralEntrypoints(DEV_ROOT).map((f) => relative(DEV_ROOT, f));
    for (const root of ['services', 'connectors']) {
      expect(
        all.filter((f) => f.startsWith(`${root}/`)).length,
        `root ${root} contributed no entrypoint — the walk has been narrowed`,
      ).toBeGreaterThan(0);
    }
  });
});
