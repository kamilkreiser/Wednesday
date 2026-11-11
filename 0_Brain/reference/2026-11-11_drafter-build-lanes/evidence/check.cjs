#!/usr/bin/env node
'use strict';
/**
 * KS-1000 — type-check a service's TEST files against a baseline that can only shrink.
 *
 * services/auth/tsconfig.json excludes src/__tests__, so `tsc -p tsconfig.json` ("npm run build") examines none of
 * the service's test files and a "0 errors" line over a test-only change is a green that could not fail. This runs
 * the same compiler over the service's tsconfig.test.json (which includes the tests) and compares the result to a
 * recorded baseline of the errors that already existed:
 *
 *   - an error the baseline does not admit FAILS the check (a new type error in a test cannot land silently);
 *   - a baseline entry that no longer reproduces FAILS the check (the baseline can only shrink: lower it with --update);
 *   - the check says which subset it examined, and exits 2 (not 0) when it examined no test file at all, or when tsc
 *     failed without producing a single diagnostic (KS-676's shape: a clean report over an empty file set).
 *
 * KS-1489 (the five gaps the #1480 gate found) closes these:
 *
 *   - SWAP. A baseline entry is keyed by file + code + a FINGERPRINT of the message (not by a count alone), so fixing one
 *     error and adding another of the same code in the same file is a new error and a stale entry, and fails. The old
 *     count-only line is refused with the command that converts it (--rekey), because accepting it keeps the gap open.
 *   - DROPPED DIAGNOSTICS. A tsc diagnostic with no file (`error TS5033: ...`) used to be thrown away whenever any file-level
 *     error existed. It now fails the check: no baseline entry can admit an error that names no file.
 *   - NARROWING. The baseline records `examined-test-files <N>`, a floor; fewer examined test files than that fails, so an
 *     `exclude`/`include` change in tsconfig.test.json cannot hide tests. And a `@ts-nocheck` in an examined test file
 *     fails, because it hides every error in the file from this check.
 *   - PATHS. tsc writes the checkout's ABSOLUTE path into SOME messages and not others. Measured, code by code (KS-1523 item (c);
 *     the list here used to name TS2307 and TS2305, which do not print it, and to omit two that do):
 *       prints it     TS1192 (`Module '"/abs/.../repo"' has no default export`), TS2306 (`File '/abs/.../empty.ts' is not a
 *                     module`), TS7016 (`'/abs/.../mod.js' implicitly has an 'any' type`), and the `import("/abs/...")` form an
 *                     assignability message uses to tell two same-named types apart (TS2741 here; the #1506 gate saw a TS2322).
 *       does NOT      TS2305 and TS2307 quote the specifier AS WRITTEN (`'"../repo"'`, `'../does-not-exist'`).
 *     A hash of that text only reproduces in the clone that made it, so the fingerprint is of the
 *     message with the service dir and this repo's Dev dir replaced by `<service>` and `<root>` (symlinked and resolved
 *     spellings both). What is shown to a human is still the raw message.
 *
 * usage: node scripts/typecheck-tests/check.cjs <service-dir> [--tsconfig <name>] [--baseline <file>] [--update | --init | --rekey]
 *   --update  rewrite the baseline from the current result; refuses (exit 1) if it would admit anything new. It sets the
 *             examined-test-files floor to the current count, up or down: a lower floor is a visible, reviewed change.
 *   --init    write a baseline that does not exist yet (refuses if the file exists). The one run that needs no baseline:
 *             every other run, --update and --rekey included, exits 2 when the file is missing (KS-1551).
 *   --rekey   convert a count-only baseline (`<file> <TSxxxx> <count>`) to the fingerprinted one. It can lower, and it
 *             REFUSES (exit 1) to admit a (file, code) group with more errors than the old line admitted.
 * exit: 0 pass | 1 new error, stale baseline, dropped diagnostic, @ts-nocheck or a fallen floor | 2 the check itself could
 *       not run or examined nothing, or the baseline cannot be trusted (missing, count-only, unparseable, no floor line, a second floor
 *       line, a duplicate entry) or cannot be written (a path the format cannot hold)
 *
 * Baseline lines (`#` starts a comment):
 *   examined-test-files <N>
 *   <path relative to the service dir> <TSxxxx> <fingerprint: 8 hex> <count>
 *
 * WHAT THIS DOES NOT CATCH (so nobody reads a green as more than it is):
 *   - `// @ts-ignore` and `// @ts-expect-error` are NOT policed. Either on a new error in a file the baseline does not list
 *     passes this check (on a baselined error they make the entry stale, which fails). Today the two services' tests use none.
 *   - The floor only protects down to the value recorded at the last --update: a tsconfig narrowing that keeps the count at or
 *     above it is not caught.
 *   - Two errors with IDENTICAL message text in one file are one entry with a count; swapping one for another is undetectable.
 *   - A test file outside a `__tests__` directory counts toward neither the floor nor the @ts-nocheck scan (none exist today).
 *   - The @ts-nocheck matcher is broader than tsc: it flags any line that starts with `//` or `/*` and then `@ts-nocheck`,
 *     including forms tsc does not honour. That fails safe (it can refuse something harmless; it cannot miss the real thing).
 *   - A path containing whitespace or `#` cannot be held by the baseline format (whitespace-split, `#` starts a comment); the
 *     writers refuse it (exit 2) instead of writing a file the reader would then reject.
 *   - A sibling path that BEGINS with a root's text and continues with `~`, `+` or a SPACE is partly replaced. The "longer
 *     name" guard after each root is `(?![\w.@-])`, a filename-character class, and those three are not in it. Left as written
 *     (KS-1523 item (b)): on POSIX every byte but `/` and NUL is legal in a name, so no such class can be complete, while the
 *     separator-only rule `(?![^/])` would stop replacing a root that a message follows with a quote -- reintroducing the
 *     cross-checkout instability this PATHS paragraph exists to remove. The effect is bounded: the replacement is still
 *     deterministic, so such a fingerprint remains stable across checkouts. It conflates; it cannot destabilise, and it cannot
 *     admit a new error (a wrong fingerprint reads as 1 new + 1 stale, which FAILS).
 *   - WINDOWS IS NOT SUPPORTED, and is not tested (KS-1523 item (f)): the path normalisation, the baseline's `/` separators and
 *     the `\r` handling were all written for POSIX checkouts.
 */
const fs = require('fs');
const path = require('path');
const crypto = require('crypto');
const { spawnSync } = require('child_process');

function die(code, msg) { process.stderr.write(msg + '\n'); process.exit(code); }

const argv = process.argv.slice(2);
const flag = (name) => { const i = argv.indexOf(name); if (i < 0) return undefined; const v = argv[i + 1]; argv.splice(i, 2); return v; };
const bare = (name) => { const i = argv.indexOf(name); if (i < 0) return false; argv.splice(i, 1); return true; };
const tsconfigName = flag('--tsconfig') || 'tsconfig.test.json';
const baselineArg = flag('--baseline');
const update = bare('--update');
const init = bare('--init');
const rekey = bare('--rekey');
const USAGE = 'usage: check.cjs <service-dir> [--tsconfig <name>] [--baseline <file>] [--update | --init | --rekey]';
if (argv.length !== 1 || [update, init, rekey].filter(Boolean).length > 1) die(2, USAGE);

// realpath: tsc's --listFiles prints resolved paths, so a symlinked checkout (macOS /var -> /private/var, a /Volumes mount)
// would otherwise match none of the files below and read as "examined nothing".
if (!fs.existsSync(argv[0])) die(2, `no such directory: ${argv[0]}`);
const serviceDir = fs.realpathSync(path.resolve(argv[0]));
if (!fs.existsSync(path.join(serviceDir, tsconfigName))) die(2, `no ${tsconfigName} in ${serviceDir}`);
const baselinePath = path.resolve(baselineArg || path.join(__dirname, `baseline-${path.basename(serviceDir)}.txt`));

let tscBin;
try { tscBin = require.resolve('typescript/bin/tsc', { paths: [serviceDir, __dirname] }); }
catch { die(2, 'cannot resolve typescript/bin/tsc from the service dir or this script: run `npm ci` first'); }

// ---------------------------------------------------------------------------
// KS-1517: a stale workspace build must say "could not run", not blame the test files.
//
// The #1504 gate saw two TS2307s reported as NEW test-file type errors because @secuura/shared
// resolved to an older build. Nothing in that PR was wrong; the environment was. And the remedy a
// developer reaches for, --update, refuses to admit new entries, so the red cannot be silenced.
//
// WHICH MAP. tsc resolves these subpaths under Node10 through `typesVersions`, not through `exports`
// (measured with --traceResolution on services/api-gateway). `exports` governs runtime resolution.
// So the TYPE target is the one typesVersions names, and a missing one is what breaks the check:
// the declaration alone missing reads as TS7016, the whole directory gone as TS2307. An exports-only
// gap type-checks cleanly, so it is DELIBERATELY not a failure — a refusal over a build tsc is happy
// with would be a false alarm. It is reported and nothing more.
//
// Only subpaths this service actually imports are judged: a package may declare an entry point that
// nothing here uses, and whether that is built is not this service's business.
// This scan feeds ONLY the runtime note below; it decides nothing. Its resolver is not TypeScript's:
// it takes the FIRST matching key in object order (TypeScript takes the longest prefix) and reads only
// the `*` version range. That is why it may not decide anything.
const SCAN_MAX_BYTES = 4 * 1024 * 1024;
const SPEC = /(?:from|require\(|import\()\s*['"](@secuura\/[a-z0-9._-]+)((?:\/[^'"]+)?)['"]/g;
function sourceSpecifiers(root) {
  const out = new Map(); // pkg -> Set(subpath without leading slash; '' for the root import)
  const walk = (d) => {
    let ents;
    try { ents = fs.readdirSync(d, { withFileTypes: true }); } catch { return; }
    for (const e of ents) {
      if (e.name === 'node_modules' || e.name === 'dist' || e.name.startsWith('.')) continue;
      const f = path.join(d, e.name);
      if (e.isDirectory()) { walk(f); continue; }
      // MJ1 (#1515 round 2 gate): only REGULAR files. A FIFO named `x.ts` made readFileSync block
      // forever, hanging the checker on a build tsc was happy with.
      if (!e.isFile()) continue;
      if (!/\.(ts|tsx|mts|cts)$/.test(e.name)) continue;
      // ...and under a size cap. Not for correctness — the try/catch around the note covers a throw —
      // but because running out of memory is not a catchable exception. The largest real source file
      // under services/ and packages/ is 280,069 bytes (measured 2026-10-13): the cap is far above it.
      try { if (fs.statSync(f).size > SCAN_MAX_BYTES) continue; } catch { continue; }
      let text;
      try { text = fs.readFileSync(f, 'utf8'); } catch { continue; }
      const { stringStarts, comments } = lexSpans(text);
      for (const m of text.matchAll(SPEC)) {
        // The quote the regex matched must OPEN a real string, and must not be inside a comment.
        const quoteAt = m.index + m[0].indexOf(m[1]) - 1;
        if (!stringStarts.has(quoteAt) || inAny(comments, m.index)) continue;
        if (!out.has(m[1])) out.set(m[1], new Set());
        out.get(m[1]).add(m[2].replace(/^\//, ''));
      }
    }
  };
  walk(fs.existsSync(path.join(root, 'src')) ? path.join(root, 'src') : root);
  return out;
}
/**
 * Where the real string literals and the comments are (L2 of the #1515 gate).
 *
 * The specifier scan used to run over raw text, so a specifier written in a COMMENT, or quoted inside
 * another string, was judged as an import and could make the check exit 2 over a subpath tsc never
 * resolves. Blanking string bodies instead is worse than useless: an import specifier IS a string, so
 * blanking it stops the scan matching anything at all — a check that cannot fail. So this records
 * POSITIONS and the scan filters on them: a specifier counts only when its opening quote begins a
 * top-level string literal, and only when it sits outside every comment.
 */
function lexSpans(src) {
  const stringStarts = new Set();
  const comments = [];
  let i = 0;
  const N = src.length;
  while (i < N) {
    const c = src[i];
    const d = src[i + 1];
    if (c === '/' && d === '/') { const s0 = i; while (i < N && src[i] !== '\n') i += 1; comments.push([s0, i]); continue; }
    if (c === '/' && d === '*') {
      const s0 = i; i += 2;
      while (i < N && !(src[i] === '*' && src[i + 1] === '/')) i += 1;
      i = Math.min(i + 2, N); comments.push([s0, i]); continue;
    }
    if (c === '"' || c === "'" || c === '`') {
      stringStarts.add(i);
      const q = c; i += 1;
      while (i < N) {
        if (src[i] === '\\') { i += 2; continue; }
        if (src[i] === q) { i += 1; break; }
        if (src[i] === '\n' && q !== '`') { i += 1; break; }
        i += 1;
      }
      continue;
    }
    i += 1;
  }
  return { stringStarts, comments };
}
const inAny = (ranges, pos) => ranges.some(([a, b]) => pos >= a && pos < b);

/** The nearest node_modules/<name> walking up from the service, as node itself would resolve it. */
function packageRoot(from, name) {
  let d = from;
  for (;;) {
    const c = path.join(d, 'node_modules', name);
    if (fs.existsSync(path.join(c, 'package.json'))) return c;
    const up = path.dirname(d);
    if (up === d) return null;
    d = up;
  }
}
/** Every string target a map value can offer, in order: a bare string, an array, or a conditions object. */
function candidates(v) {
  if (typeof v === 'string') return [v];
  if (Array.isArray(v)) return v.flatMap(candidates);
  if (v && typeof v === 'object') {
    for (const k of ['types', 'import', 'require', 'default', 'node']) {
      if (k in v) { const r = candidates(v[k]); if (r.length) return r; }
    }
  }
  return [];
}
/**
 * Every target a subpath maps to. A literal key wins; otherwise a single trailing `*` key whose head matches,
 * with the tail substituted into each target. Returns a LIST, because typesVersions targets are arrays and
 * TypeScript takes the first that exists — judging only the first made this exit 2 on a complete build
 * (L1.4 of the #1515 gate).
 */
function mapTargets(map, subpath) {
  if (!map || typeof map !== 'object') return [];
  if (subpath in map) return candidates(map[subpath]);
  for (const [k, v] of Object.entries(map)) {
    if (!k.endsWith('*')) continue;
    const head = k.slice(0, -1);
    if (!subpath.startsWith(head)) continue;
    const tail = subpath.slice(head.length);
    return candidates(v).map((t) => t.replace(/\*/g, tail));
  }
  return [];
}
// A target is JUDGEABLE only when it names a declaration/runtime file outright. `typesVersions` and `exports`
// may legitimately point at an extensionless path or a wildcard, which TypeScript completes itself
// ("dist/sub/a" -> dist/sub/a.d.ts, "dist/d" -> dist/d/index.d.ts). The PR said anything more exotic is
// SKIPPED, not guessed at; before this fix the code guessed, and exited 2 on four shapes that resolve
// cleanly (L1 of the #1515 gate). Now: if no candidate resolves AND none of them is judgeable, say nothing.
const SUFFIX = { declaration: ['.d.ts'], runtime: ['.js', '.cjs', '.mjs'] };
const isJudgeable = (t, kind) => !t.includes('*') && SUFFIX[kind].some((e) => t.endsWith(e));
const stripDot = (t) => t.replace(/^\.\//, '');
/** The paths TypeScript/node would try for one declared target. */
function variantsOf(t, kind) {
  const rel = stripDot(t);
  const out = [rel];
  for (const e of SUFFIX[kind]) { out.push(rel + e); out.push(path.posix.join(rel, 'index' + e)); }
  return out;
}
const run = spawnSync(process.execPath, [tscBin, '--noEmit', '--pretty', 'false', '--listFiles', '-p', tsconfigName],
  { cwd: serviceDir, encoding: 'utf8', maxBuffer: 256 * 1024 * 1024 });
if (run.error) die(2, `could not run tsc: ${run.error.message}`);

const ERR = /^(.+?)\((\d+),(\d+)\): error (TS\d+): (.*)$/;
const FILELESS = /^error (TS\d+): (.*)$/;
const norm = (p) => path.relative(serviceDir, path.resolve(serviceDir, p)).split(path.sep).join('/');
// The fingerprint is of the CODE and the MESSAGE, never the position: an unrelated edit above an error moves its line
// and must not move its identity, while a different error of the same code in the same file must get a different key.
// ...and never the CHECKOUT: tsc prints absolute paths in some messages (see PATHS above), so the roots below are replaced
// before hashing. Longest first, and not when the path is only the start of a longer name (`/x/auth` inside `/x/auth-api`).
const DEV_ROOT = path.resolve(__dirname, '..', '..');
const realOrSame = (p) => { try { return fs.realpathSync(p); } catch { return p; } };
const ROOTS = [...new Map([
  [serviceDir, '<service>'], [path.resolve(argv[0]), '<service>'],
  [DEV_ROOT, '<root>'], [realOrSame(DEV_ROOT), '<root>'],
]).entries()].sort(([a], [b]) => b.length - a.length)
  .map(([p, token]) => [new RegExp(p.replace(/[.*+?^${}()|[\]\\]/g, '\\$&') + '(?![\\w.@-])', 'g'), token]);
const withoutRoots = (text) => ROOTS.reduce((t, [re, token]) => t.replace(re, token), String(text));
const fingerprint = (code, text) =>
  crypto.createHash('sha1').update(`${code}\n${withoutRoots(text).replace(/\s+/g, ' ').trim()}`).digest('hex').slice(0, 8);
const errors = [];
const unattributed = [];
const listed = [];
for (const line of (run.stdout || '').split('\n')) {
  const m = ERR.exec(line);
  if (m) errors.push({ file: norm(m[1]), line: m[2], col: m[3], code: m[4], text: m[5], fp: fingerprint(m[4], m[5]) });
  else if (FILELESS.test(line)) { const f = FILELESS.exec(line); unattributed.push({ code: f[1], text: f[2] }); }
  else if (path.isAbsolute(line.trim())) listed.push(line.trim());
}
if (run.status !== 0 && errors.length === 0) {
  die(2, `tsc exited ${run.status} without a single parseable diagnostic: the check cannot tell clean from broken.\n${(run.stderr || run.stdout || '').slice(0, 600)}`);
}

// ---------------------------------------------------------------------------
// KS-1517 round 2 — a stale workspace build is reported from TSC'S OWN DIAGNOSTICS.
//
// Round 1 tried to decide this BEFORE tsc ran, by resolving the package's `typesVersions` the way
// TypeScript does. Two gates found six shapes where that resolution differs from TypeScript's and
// exited 2 on a build tsc is perfectly happy with — longest-prefix versus first-match key order, a
// version range other than `*`, a redirected `types` field, extensionless and wildcard targets, a
// mixed array. Every one of them would have blocked every seat's push with a message telling them to
// rebuild, and rebuilding would not have helped. Emulating a resolver is the wrong shape of answer.
//
// So the question is asked the other way round, and a false exit 2 is impossible by construction
// wherever tsc is happy: this exits 2 ONLY for a module tsc ITSELF could not resolve (TS2307) or
// could not find a declaration for (TS7016), that is an `@secuura/*` package which IS installed, and
// whose mapped declaration target is genuinely absent from disk. If tsc resolved it, nothing here can
// fail — at most a note. If tsc's complaint is real but the target IS on disk, the diagnostic is left
// alone and flows to the baseline as the author's own error, which is the pre-KS-1517 behaviour.
//
// What this guarantees, and what it does not. Where tsc is HAPPY, nothing here can exit 2: measured
// over 50 tsc-rc-0 shapes by the round 2 gate. Where tsc is NOT happy, the resolver below still matters:
// it decides whether a TS2307/TS7016 is reported as a stale build, and it is not TypeScript's resolver.
// So in contrived shapes it can name the wrong file, or call a permanently-absent target "stale" — and
// if such a TS2307/TS7016 had been BASELINED, that turns a push develop accepts into a refusal. Both
// committed baselines hold zero TS2307/TS7016 entries (measured 2026-10-13). One judged stale cannot
// get in: the exit 2 below runs before --init or --update writes, and --update admits nothing new.
// --init can still admit one whose target is on disk at the time. Ticketed.
const SECUURA_IN_DIAGNOSTIC =
  /^(?:Cannot find module|Could not find a declaration file for module) '(@secuura\/[^']+)'/;
const SPLIT_SPEC = /^(@secuura\/[a-z0-9._-]+)(?:\/(.*))?$/;
const staleFatal = [];
const staleNotes = [];
/** The package.json of an installed @secuura package, or undefined. */
function packageJsonOf(pkgName) {
  const pkgRoot = packageRoot(serviceDir, pkgName);
  if (!pkgRoot) return undefined; // not installed: leg 1 owns the install and tsc's message is the right one
  try { return { pkgRoot, pkg: JSON.parse(fs.readFileSync(path.join(pkgRoot, 'package.json'), 'utf8')) }; }
  catch { return undefined; }
}
const declTargetsFor = (pkg, sub) =>
  sub === '' ? candidates(pkg.types) : mapTargets((pkg.typesVersions && pkg.typesVersions['*']) || undefined, sub);
const anyResolves = (pkgRoot, targets, kind) =>
  targets.some((t) => variantsOf(t, kind).some((v) => fs.existsSync(path.join(pkgRoot, v))));

for (const e of errors) {
  // BOTH the code and an ANCHORED message. Round 2 removed this code check, claiming "no other
  // diagnostic carries either phrase" so no fixture could make it the deciding guard. That was false,
  // and the round 2 gate built the fixture: a TS2322 quoting the phrase inside a string-literal type
  // ("Type '"Cannot find module '@secuura/...'"' is not assignable ...") made this exit 2 — and, with that
  // TS2322 baselined, turned a push develop accepts into a refusal. The anchor and the code each reject
  // it; the E1 cell pins it.
  if (e.code !== 'TS2307' && e.code !== 'TS7016') continue;
  const m = SECUURA_IN_DIAGNOSTIC.exec(e.text);
  if (!m) continue;                                  // not an @secuura module: never ours to reinterpret
  const parts = SPLIT_SPEC.exec(m[1]);
  if (!parts) continue;
  const [, pkgName, subRaw] = parts;
  const sub = subRaw || '';
  const found = packageJsonOf(pkgName);
  if (!found) continue;  // FATAL-SIDE: not installed, so leg 1 owns it
  const targets = declTargetsFor(found.pkg, sub);
  // The package declaring NOTHING for this subpath is not a stale build — it is an import of
  // something the package does not offer, which is the author's own error and tsc's message is the
  // right one. Caught by the sibling-prefix cell below, which went red when this exited 2.
  if (targets.length === 0) continue;
  if (anyResolves(found.pkgRoot, targets, 'declaration')) continue; // a real error, not a stale build
  staleFatal.push({
    pkgName,
    rel: targets.map(stripDot).join(' or '),
    asImported: `'${m[1]}'`,
    corroboration: `${e.code} at ${e.file}(${e.line},${e.col})`,
  });
}

// The runtime-only note. It must never fail the check. Round 2 claimed it could not, and the round 2
// gate showed the scan feeding it could crash (a RangeError in lexSpans on a 16.8 MB file, the G5
// cell) or hang (a FIFO). The walk now reads only regular files under a cap; this try/catch makes
// any remaining throw in this block — the scan, a malformed package.json, anything — cost the note
// and nothing else.
try {
for (const [pkgName, subpaths] of sourceSpecifiers(serviceDir)) {
  const found = packageJsonOf(pkgName);
  if (!found) continue;  // NOTE-SIDE: not installed, nothing to say
  const exp = found.pkg.exports || undefined;
  for (const sub of [...subpaths].sort()) {
    const runTargets = sub === ''
      ? candidates(exp && exp['.']).concat(candidates(found.pkg.main))
      : mapTargets(exp, './' + sub).concat(mapTargets(exp, sub));
    if (runTargets.length === 0) continue;
    if (anyResolves(found.pkgRoot, runTargets, 'runtime')) continue;
    const judgeable = runTargets.filter((t) => isJudgeable(t, 'runtime'));
    if (judgeable.length === 0) continue;
    staleNotes.push({ pkgName, rel: judgeable.map(stripDot).join(' or '), asImported: `'${pkgName}${sub ? '/' + sub : ''}'` });
  }
}
} catch {
  // Advisory only: a note we cannot compute is a note we do not print. Never a failure.
}

if (staleFatal.length > 0) {
  const pkgs = [...new Set(staleFatal.map((x) => x.pkgName))];
  const lines = [
    `${path.basename(serviceDir)}: the ${pkgs.join(', ')} build is stale or incomplete, so this check CANNOT RUN.`,
    '  tsc itself could not resolve the module below AND its declaration target is not on disk, so this is',
    '  not a type error in your test files, and --update will not admit it.',
    ...staleFatal.map((x) => `  missing declaration target: ${x.rel}   (imported as ${x.asImported}; tsc said ${x.corroboration})`),
    ...staleNotes.map((x) => `  also missing (runtime only, does not affect the type check): ${x.rel}`),
    ...pkgs.map((p) => `  rebuild it:  npm run build -w ${p}`),
    '  (npm ci does not build it here: Blockchain/Dev/.npmrc sets ignore-scripts=true.)',
  ];
  die(2, lines.join('\n'));
}
for (const x of staleNotes) {
  process.stdout.write(`note: ${x.pkgName} declares ${x.rel} for ${x.asImported} and it is not built. `
    + `The type check is unaffected (tsc resolved it), so this is not a failure. `
    + `Rebuild with: npm run build -w ${x.pkgName}\n`);
}
const inService = (f) => f.startsWith(serviceDir + path.sep) && !f.includes(`${path.sep}node_modules${path.sep}`);
const examined = listed.filter(inService);
const testFiles = examined.filter((f) => f.includes(`${path.sep}__tests__${path.sep}`));
if (testFiles.length === 0) {
  die(2, `${path.basename(serviceDir)}: ${tsconfigName} examined ${examined.length} files and NONE under __tests__: a clean result here would say nothing about the tests.`);
}
// A `@ts-nocheck` in an examined test file makes tsc report nothing for it, so it would pass this check while hiding everything.
const NOCHECK = /^\s*(?:\/\/|\/\*+)\s*@ts-nocheck\b/m;
const nocheck = testFiles.filter((f) => { try { return NOCHECK.test(fs.readFileSync(f, 'utf8')); } catch { return false; } }).map(norm);

const key = (e) => `${e.file} ${e.code} ${e.fp}`;
const current = new Map();
for (const e of errors) current.set(key(e), (current.get(key(e)) || 0) + 1);

const V2 = /^(\S+) (TS\d+) ([0-9a-f]{8}) (\d+)$/;
const LEGACY = /^(\S+) (TS\d+) (\d+)$/;
const FLOOR = /^examined-test-files (\d+)$/;
function readBaseline() {
  const out = { exists: false, entries: new Map(), floor: null, legacy: [] };
  if (!fs.existsSync(baselinePath)) return out;
  out.exists = true;
  // \r first: a CRLF checkout (autocrlf) leaves it at the end of a comment line, where `.` would not match it.
  fs.readFileSync(baselinePath, 'utf8').split('\n').forEach((raw, i) => {
    const line = raw.replace(/\r$/, '').replace(/#.*$/, '').trim();
    if (!line) return;
    let m;
    if ((m = V2.exec(line))) {
      const k = `${m[1]} ${m[2]} ${m[3]}`;
      if (out.entries.has(k)) die(2, `${baselinePath}:${i + 1}: duplicate entry ${JSON.stringify(k)} (the last one used to win silently; a repeated line is a mistake or an edit that raised a count)`);
      out.entries.set(k, Number(m[4]));
    } else if ((m = FLOOR.exec(line))) {
      if (out.floor !== null) die(2, `${baselinePath}:${i + 1}: a second examined-test-files line (the last one used to win silently, so a floor could be lowered by adding a line)`);
      out.floor = Number(m[1]);
    } else if ((m = LEGACY.exec(line))) out.legacy.push({ file: m[1], code: m[2], count: Number(m[3]) });
    else die(2, `${baselinePath}:${i + 1}: not "<file> <TSxxxx> <fingerprint> <count>" or "examined-test-files <N>": ${JSON.stringify(raw)}`);
  });
  return out;
}
const header = [
  '# KS-1000 ratchet: type errors already present in this service\'s test files, keyed by file + code + a fingerprint of the message.',
  '# It can only SHRINK. A new error fails `node scripts/typecheck-tests/check.cjs <service>`; an entry that no longer',
  '# reproduces fails it too; so does a swap (one error fixed, another of the same code added). Lower it with `--update` (which',
  '# refuses to admit anything new). Never edit a count up. `examined-test-files` is a floor: fewer examined test files fails.',
];
function writeBaseline(map, floor) {
  // The reader splits on whitespace and treats `#` as a comment: a path holding either would be written and then rejected.
  const unwritable = [...new Set(errors.map((e) => e.file))].filter((f) => /[\s#]/.test(f));
  if (unwritable.length) die(2, `typecheck-tests: cannot write ${baselinePath}: the baseline format cannot hold ${unwritable.map((f) => JSON.stringify(f)).join(', ')} (it is whitespace-split and '#' starts a comment). Rename the file.`);
  const lines = [...map.entries()].sort(([a], [b]) => (a < b ? -1 : 1)).map(([k, n]) => `${k} ${n}`);
  fs.writeFileSync(baselinePath, header.join('\n') + '\n' + `examined-test-files ${floor}\n` + lines.join('\n') + (lines.length ? '\n' : ''));
}
function listFresh(fresh) {
  for (const [k] of fresh) for (const e of errors.filter((x) => key(x) === k)) console.error(`  ${e.file}(${e.line},${e.col}): ${e.code}: ${e.text}`);
}
// What can never be baselined: a diagnostic that names no file, and a file that opts out of checking.
function reportUnbaselinable() {
  if (unattributed.length) {
    console.error('UNATTRIBUTED tsc diagnostics (they name no file, so no baseline entry can admit them):');
    for (const u of unattributed) console.error(`  ${u.code}: ${u.text}`);
  }
  if (nocheck.length) {
    console.error('@ts-nocheck in an examined test file (it hides every error in the file from this check):');
    for (const f of nocheck) console.error(`  ${f}`);
  }
}
const unbaselinable = () => unattributed.length > 0 || nocheck.length > 0;

const base = readBaseline();

// KS-1551: a baseline that is not there cannot be trusted. A missing file used to read as an EMPTY baseline with no
// examined-test-files floor, so deleting it passed: for a service whose baseline is empty nothing reappears as NEW, and the
// floor, the only guard against a deleted test file, went with the file. --init exists to create one, so it alone is exempt.
if (!base.exists && !init) {
  die(2, `${baselinePath}: no baseline, so the check cannot be trusted (a missing baseline used to read as an empty one with no examined-test-files floor). ` +
    (update ? '--update does not create one: write it with --init.' : 'Write it with --init.'));
}

if (init) {
  if (fs.existsSync(baselinePath)) die(2, `${baselinePath} exists: use --update`);
  if (unbaselinable()) { reportUnbaselinable(); die(1, 'typecheck-tests: --init refuses: the items above cannot be baselined.'); }
  writeBaseline(current, testFiles.length);
  console.log(`typecheck-tests: wrote ${baselinePath} (${errors.length} errors in ${current.size} entries; examined-test-files ${testFiles.length})`);
  process.exit(0);
}

if (rekey) {
  if (base.legacy.length === 0) die(2, `${baselinePath}: no count-only lines to convert`);
  if (unbaselinable()) { reportUnbaselinable(); die(1, 'typecheck-tests: --rekey refuses: the items above cannot be baselined.'); }
  // The old line admitted a COUNT per (file, code). It can be converted only if no group now has more errors than it admitted.
  const admitted = new Map();
  for (const l of base.legacy) admitted.set(`${l.file} ${l.code}`, (admitted.get(`${l.file} ${l.code}`) || 0) + l.count);
  const groups = new Map();
  for (const e of errors) groups.set(`${e.file} ${e.code}`, (groups.get(`${e.file} ${e.code}`) || 0) + 1);
  const over = [...groups].filter(([g, n]) => n > (admitted.get(g) || 0));
  if (over.length) {
    console.error(`typecheck-tests: --rekey refuses to admit ${over.length} group${over.length === 1 ? '' : 's'} with more errors than the count-only baseline did; fix the errors instead:`);
    for (const [g] of over) for (const e of errors.filter((x) => `${x.file} ${x.code}` === g)) console.error(`  ${e.file}(${e.line},${e.col}): ${e.code}: ${e.text}`);
    process.exit(1);
  }
  writeBaseline(current, testFiles.length);
  console.log(`typecheck-tests: rekeyed ${baselinePath}: ${base.legacy.length} count-only lines -> ${current.size} fingerprinted entries (${errors.length} errors; examined-test-files ${testFiles.length})`);
  process.exit(0);
}

if (base.legacy.length) {
  die(2, `${baselinePath}: ${base.legacy.length} count-only line(s) with no fingerprint (e.g. "${base.legacy[0].file} ${base.legacy[0].code} ${base.legacy[0].count}"). ` +
    'A count lets one error be swapped for another of the same code, so it is no longer accepted. Convert it (this can lower the baseline but never admit anything new) with:\n' +
    `  node scripts/typecheck-tests/check.cjs ${argv[0]} --rekey`);
}

if (base.exists && base.floor === null) {
  die(2, `${baselinePath}: no "examined-test-files <N>" line, so nothing stops test files dropping out of the check (every baseline this tool writes has one). ` +
    `Restore the line (this run examined ${testFiles.length}) or recreate the file with --init.`);
}

const fresh = [];
const stale = [];
for (const [k, n] of current) { const b = base.entries.get(k) || 0; if (n > b) fresh.push([k, n, b]); }
for (const [k, b] of base.entries) { const n = current.get(k) || 0; if (b > n) stale.push([k, n, b]); }
const admitted = errors.length - fresh.reduce((s, [, n, b]) => s + (n - b), 0);

if (update) {
  if (fresh.length) {
    console.error(`typecheck-tests: --update refuses to admit ${fresh.length} new entr${fresh.length === 1 ? 'y' : 'ies'}; fix the errors instead:`);
    listFresh(fresh);
    process.exit(1);
  }
  if (unbaselinable()) { reportUnbaselinable(); die(1, 'typecheck-tests: --update refuses: the items above cannot be baselined.'); }
  writeBaseline(current, testFiles.length);
  console.log(`typecheck-tests: baseline lowered to ${errors.length} errors in ${current.size} entries (${stale.length} stale entr${stale.length === 1 ? 'y' : 'ies'} dropped or reduced); examined-test-files ${base.floor === null ? 'none' : base.floor} -> ${testFiles.length}`);
  process.exit(0);
}

const svc = path.basename(serviceDir);
const floorFell = base.floor !== null && testFiles.length < base.floor;
console.log(`typecheck-tests: ${svc} (${tsconfigName}): tsc examined ${examined.length} files, ${testFiles.length} of them under __tests__; ` +
  `${errors.length} errors: ${admitted} in the baseline, ${errors.length - admitted} new; ${stale.length} stale baseline entr${stale.length === 1 ? 'y' : 'ies'}.`);
if (fresh.length) {
  console.error('NEW type errors (not in the baseline):');
  listFresh(fresh);
}
if (stale.length) {
  console.error('STALE baseline entries (the error no longer reproduces; the baseline can only shrink, lower it with --update):');
  for (const [k, n, b] of stale) console.error(`  ${k}: baseline ${b}, now ${n}`);
}
reportUnbaselinable();
if (floorFell) {
  console.error(`EXAMINED test files fell below the baseline's floor: ${testFiles.length} examined, examined-test-files ${base.floor}. ` +
    'A tsconfig narrowing, or a deleted test file? If it is deliberate, lower the floor with --update and have the diff reviewed.');
}
process.exit(fresh.length || stale.length || unbaselinable() || floorFell ? 1 : 0);
