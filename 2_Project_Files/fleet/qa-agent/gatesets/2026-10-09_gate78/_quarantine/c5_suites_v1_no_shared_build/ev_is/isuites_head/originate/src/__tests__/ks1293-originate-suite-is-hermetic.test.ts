/**
 * KS-1293 — HERMETIC-UNPINNED. KS-1266 (#1221) stopped the anchoring-touching unit files reaching
 * the network, and NOTHING in the suite would have noticed if that regressed: the property was
 * proved by an out-of-band probe, so once #1221 merged it was protected by nobody. The tier-2 gate
 * measured it — revert one file's env line and the suite stays green.
 *
 * RUNS UNDER: the DEFAULT jest config (`npm test` / `jest`). It therefore covers the files that run
 * in that config. `*.integration.test.ts` is in `testPathIgnorePatterns` and is NOT covered here —
 * see the NOT-COVERED note at the foot of this file.
 *
 * Two cells, because the ticket has two acceptance criteria and ONE instrument cannot serve both:
 *   1. CONFIGPINNED (static) — every anchoring-touching file in this config still sets the base to a
 *      loopback host on a port that is NOT a Fetch-spec bad port. Catches criterion 2 (a drift back
 *      to a bad port), which a DNS spy cannot see: `:1` and `:2` are both loopback and both produce
 *      zero lookups.
 *   2. NODNS (probe-backed) — with a `dns.lookup` spy installed, the configured base produces ZERO
 *      non-loopback lookups AND fails with a socket-level ECONNREFUSED. Catches criterion 1 (the
 *      hermeticity property itself), however a regression arrives.
 *
 * Measured on node 24 while writing these cells:
 *   http://127.0.0.1:2  -> cause.code ECONNREFUSED  (a socket WAS attempted and refused)
 *   http://127.0.0.1:1  -> cause.code undefined     (a Fetch BAD PORT: refused BEFORE any socket,
 *                                                    so the "closed port" never happened)
 *   a loopback literal  -> 0 dns.lookup calls
 *   the product default -> 1 dns.lookup call for its non-loopback host  <- the regression shape
 */
// This file is a SUBJECT of its own first cell as well as its author: it runs in the same config,
// so it sets the same loopback base the other files do. That is also what gives the second cell a
// configured base to exercise — without it `process.env` falls through to the product default, and
// the cell would measure the regression shape instead of the pinned one.
process.env.ANCHORING_SERVICE_URL = 'http://127.0.0.1:2';

import * as fs from 'fs';
import * as os from 'os';
import * as path from 'path';
import * as ts from 'typescript';

const TESTS_DIR = __dirname;
const ENV_KEY = 'ANCHORING_SERVICE_URL';

/**
 * THE SUBJECT MANIFEST — B-1261-1 REVERT-SKIPS.
 *
 * The first version of this cell derived its subjects from "which files MENTION the key". That is
 * circular, and the gate measured the consequence: deleting the env line of ks1228 (:26), ks1264
 * (:16) or ks1213 (:30) left this cell GREEN, because the deletion removed the file from its own
 * subject set. The shape the file exists to catch erased its own subject.
 *
 * Two of these nine files carry NO second mention of the key (ks1228 and ks1264 — measured, `grep -c`
 * = 1 each), so for them a single deleted line is the whole of it.
 *
 * The manifest is therefore EXPLICIT. A subject that stops pinning the base is an offender NAMED BY
 * FILE, whether the assignment was deleted, nested, or the file renamed. MANIFEST-DRIFT below keeps
 * the manifest honest in the other direction: a NEW anchoring-touching file that nobody added here
 * is also an offender, so the list cannot silently under-cover as the suite grows.
 */
const SUBJECTS: readonly string[] = [
  'ks1213-a-derived-writer-relabel-is-refused.test.ts',
  'ks1228-a-refused-request-writes-no-provenance-row.test.ts',
  'ks1264-revoke-records-its-action-provenance-row.test.ts',
  'ks1278-revoke-is-one-atomic-transition.test.ts',
  'ks1293-originate-suite-is-hermetic.test.ts',
  'ks444-certifications-issue-body-types.test.ts',
  'ks444-documents-create-title-guard.test.ts',
  'ks445-certifications-issue-unstorable-payload.test.ts',
  'ks520-anchor-fail-closed.test.ts',
  'ks543-certify-boundary-strip.test.ts',
  'ks593-share-refuses-non-object-recipient.test.ts',
];

/**
 * Bases assigned at IMPORT SCOPE — a top-level statement of the module, read from the AST rather
 * than from text.
 *
 * Why import scope and not "anywhere in the file": ks1213 assigns the key inside `finally` blocks at
 * :341 and :356 as well as at :30. Deleting :30 leaves those behind, so a text reader still found a
 * base and stayed green — RS3a. But a nested assignment runs during a test, not at module load, so it
 * does NOT pin the phase this cell is about. Only a top-level statement does.
 *
 * The AST is used rather than a column-0 regex because indentation is a formatting accident and
 * prettier is free to change it; `sf.statements` is the language's own answer to "is this top level".
 */
export function importScopeBases(src: string, fileName: string): string[] {
  const sf = ts.createSourceFile(fileName, src, ts.ScriptTarget.Latest, true);
  // two passes: a const may be declared after the assignment that uses it
  const consts = new Map<string, string>();
  for (const st of sf.statements) {
    if (!ts.isVariableStatement(st)) continue;
    for (const d of st.declarationList.declarations) {
      if (ts.isIdentifier(d.name) && d.initializer && ts.isStringLiteral(d.initializer)) {
        consts.set(d.name.text, d.initializer.text);
      }
    }
  }
  const out: string[] = [];
  for (const st of sf.statements) {
    if (!ts.isExpressionStatement(st)) continue;
    const e = st.expression;
    if (!ts.isBinaryExpression(e) || e.operatorToken.kind !== ts.SyntaxKind.EqualsToken) continue;
    const lhs = e.left;
    if (!ts.isPropertyAccessExpression(lhs) || lhs.name.text !== ENV_KEY) continue;
    const obj = lhs.expression;
    if (!ts.isPropertyAccessExpression(obj) || obj.name.text !== 'env') continue;
    if (!ts.isIdentifier(obj.expression) || obj.expression.text !== 'process') continue;
    const r = e.right;
    if (ts.isStringLiteral(r)) out.push(r.text);
    else if (ts.isIdentifier(r) && consts.has(r.text)) out.push(consts.get(r.text) as string);
  }
  return out;
}

/** The scan, taking its directory and manifest as arguments so a fixture can drive it. */
export function scanHermeticity(
  dir: string,
  subjects: readonly string[],
): { offenders: string[]; pinned: number } {
  const offenders: string[] = [];
  let pinned = 0;
  for (const name of subjects) {
    const file = path.join(dir, name);
    if (!fs.existsSync(file)) {
      offenders.push(`${name} is named in the subject manifest but does not exist — if it was renamed or removed, update SUBJECTS in the same change`);
      continue;
    }
    const bases = importScopeBases(fs.readFileSync(file, 'utf-8'), name);
    if (bases.length === 0) {
      offenders.push(`${name} sets no IMPORT-SCOPE ${ENV_KEY} base — a deleted or nested assignment does not pin the module-load phase`);
      continue;
    }
    for (const base of bases) {
      pinned += 1;
      let url: URL;
      try {
        url = new URL(base);
      } catch {
        offenders.push(`${name} base ${base} is not a URL`);
        continue;
      }
      if (url.hostname !== '127.0.0.1') {
        offenders.push(`${name} base ${base} is not loopback — a lookup would leave the host`);
      }
      if (BAD_PORTS.has(Number(url.port))) {
        offenders.push(
          `${name} base ${base} is a Fetch BAD PORT — refused before any socket, so the closed port never happens`,
        );
      }
    }
  }
  return { offenders, pinned };
}

/** The Fetch spec's bad ports. A base on one of these is never actually connected to. */
const BAD_PORTS = new Set([
  1, 7, 9, 11, 13, 15, 17, 19, 20, 21, 22, 23, 25, 37, 42, 43, 53, 69, 77, 79, 87, 95, 101, 102,
  103, 104, 109, 110, 111, 113, 115, 117, 119, 123, 135, 137, 139, 143, 161, 179, 389, 427, 465,
  512, 513, 514, 515, 526, 530, 531, 532, 540, 548, 554, 556, 563, 587, 601, 636, 989, 990, 993,
  995, 1719, 1720, 1723, 2049, 3659, 4045, 4190, 5060, 5061, 6000, 6566, 6665, 6666, 6667, 6668,
  6669, 6679, 6697, 10080,
]);

describe('KS-1293 the originate unit suite stays off the network, and it is PINNED here', () => {
  it('CONFIGPINNED: every SUBJECT sets an import-scope base on a loopback host and a non-bad port', () => {
    const { offenders, pinned } = scanHermeticity(TESTS_DIR, SUBJECTS);
    expect(offenders).toEqual([]);
    // Non-vacuity: the manifest is 9 files and each must yield at least one base.
    expect(pinned).toBeGreaterThanOrEqual(SUBJECTS.length);
  });

  it('MANIFEST-DRIFT: no file this config runs touches the key without being a SUBJECT', () => {
    // The manifest fixes the REVERT-SKIPS hole in one direction; this closes the other. Without it a
    // new anchoring-touching file could be added and never pinned, and CONFIGPINNED would stay green
    // while covering less of the suite than its name implies.
    const configured = fs
      .readdirSync(TESTS_DIR)
      .filter((f) => f.endsWith('.test.ts') && !f.endsWith('.integration.test.ts'));
    const mentions = configured.filter((f) =>
      fs.readFileSync(path.join(TESTS_DIR, f), 'utf-8').includes(ENV_KEY),
    );
    const missing = mentions.filter((f) => !SUBJECTS.includes(f));
    expect({ missing, scanned: mentions.length > 0 }).toEqual({ missing: [], scanned: true });
  });

    // RS1 / RS2 / RS3a — the three REAL shapes the gate measured going green. Each drives the scan
  // against a COPY of the real subject with its import-scope assignment removed, in a temp directory.
  // The real files are never touched, so these cells cannot disturb another seat's tree or each
  // other, and they still reproduce the tamper exactly.
  function fixtureOf(name: string, drop: (src: string) => string): string {
    const dir = fs.mkdtempSync(path.join(os.tmpdir(), 'ks1293-b30-'));
    fs.writeFileSync(path.join(dir, name), drop(fs.readFileSync(path.join(TESTS_DIR, name), 'utf-8')));
    return dir;
  }
  /** Remove the import-scope assignment only — exactly what the gate's revert did. */
  function dropImportScopeAssignment(src: string): string {
    const lines = src.split('\n');
    const idx = lines.findIndex((l) => /^process\.env\.ANCHORING_SERVICE_URL\s*=/.test(l));
    expect(idx).toBeGreaterThanOrEqual(0); // the fixture must actually have one to remove
    lines.splice(idx, 1);
    return lines.join('\n');
  }

  const REVERT_SKIPS: ReadonlyArray<readonly [string, string]> = [
    ['RS1', 'ks1228-a-refused-request-writes-no-provenance-row.test.ts'],
    ['RS2', 'ks1264-revoke-records-its-action-provenance-row.test.ts'],
    ['RS3a', 'ks1213-a-derived-writer-relabel-is-refused.test.ts'],
  ];

  it.each(REVERT_SKIPS)(
    '%s 🔴 B-1261-1: deleting %s\'s import-scope assignment is an offender NAMED BY FILE',
    (_label, name) => {
      const dir = fixtureOf(name, dropImportScopeAssignment);
      const { offenders } = scanHermeticity(dir, [name]);
      expect(offenders).toHaveLength(1);
      expect(offenders[0]).toContain(name);
      expect(offenders[0]).toContain('IMPORT-SCOPE');
      fs.rmSync(dir, { recursive: true, force: true });
    },
  );

  it.each(REVERT_SKIPS)('%s CONTROL: the SAME file untouched is clean, so the red is the deletion', (_label, name) => {
    // Without this pair, each RS cell above also passes for a scan that calls everything an offender.
    const dir = fixtureOf(name, (src) => src);
    const { offenders, pinned } = scanHermeticity(dir, [name]);
    expect({ offenders, cleanScanFoundABase: pinned > 0 }).toEqual({ offenders: [], cleanScanFoundABase: true });
    fs.rmSync(dir, { recursive: true, force: true });
  });

  it('RS3a MECHANISM: ks1213 keeps NESTED assignments, which is why a text reader stayed green', () => {
    // States why RS3a needed the import-scope rule and not just the manifest: the manifest alone
    // keeps the file as a subject, but a reader that accepted ANY assignment would still find the
    // `finally`-block ones and report no offender.
    const src = dropImportScopeAssignment(
      fs.readFileSync(path.join(TESTS_DIR, 'ks1213-a-derived-writer-relabel-is-refused.test.ts'), 'utf-8'),
    );
    expect(src).toContain(`${ENV_KEY} = ANCHORING_REFUSED`); // nested ones survive the deletion
    expect(importScopeBases(src, 'ks1213.test.ts')).toEqual([]); // but none is at import scope
  });

  it('NODNS: the configured base resolves no non-loopback host and is refused at the SOCKET, and the spy is proven able to fire', async () => {
    const seen: string[] = [];
    // `import * as dns` gives a namespace object whose `lookup` is getter-only, so assigning it
    // throws. The mutable module exports come from require(), which is what a spy needs.
    const dnsMod = require('dns') as { lookup: (...a: unknown[]) => unknown };
    const real = dnsMod.lookup;
    dnsMod.lookup = (...args: unknown[]) => {
      const host = String(args[0]);
      seen.push(host);
      // N-1261-a NODNS-EGRESS. This used to delegate every name to the real resolver, so the pin
      // ITSELF sent a live getaddrinfo for `anchoring` off-host on every originate run. Worse, inside
      // the compose network — where `anchoring` IS a real service — the name resolves, the arm makes a
      // real GET to a live service, `rejects.toThrow()` fails, and the red is both false and noisy.
      // The spy now answers non-loopback names itself, so the arm proves the spy fires without any
      // packet leaving the host. Loopback still goes to the real resolver, because the second arm's
      // ECONNREFUSED must be a genuine socket-level refusal and not something this spy invented.
      if (host !== '127.0.0.1' && host !== 'localhost') {
        const cb = args[args.length - 1];
        if (typeof cb === 'function') {
          const err = Object.assign(new Error(`getaddrinfo ENOTFOUND ${host}`), {
            code: 'ENOTFOUND', errno: -3008, syscall: 'getaddrinfo', hostname: host,
          });
          process.nextTick(() => (cb as (e: unknown) => void)(err));
          return undefined;
        }
      }
      return real(...args);
    };
    try {
      const configured = process.env[ENV_KEY] || 'http://anchoring:4005';

      // (a) the product default IS a non-loopback host — so the spy demonstrably fires. Without
      // this arm a spy that was never installed would record nothing and the cell would pass
      // vacuously.
      seen.length = 0;
      await expect(fetch(new URL('/healthz', 'http://anchoring:4005'))).rejects.toThrow();
      const defaultLookups = [...seen];

      // (b) the configured base: zero lookups, and a SOCKET-level refusal rather than a
      // pre-socket bad-port rejection.
      seen.length = 0;
      let code: string | undefined;
      try {
        await fetch(new URL('/healthz', configured));
      } catch (err) {
        code = (err as { cause?: { code?: string } }).cause?.code;
      }
      expect([
        defaultLookups.length > 0,
        seen.filter((h) => h !== '127.0.0.1' && h !== 'localhost'),
        code,
      ]).toEqual([true, [], 'ECONNREFUSED']);
    } finally {
      dnsMod.lookup = real;
    }
  });
});

/*
 * NOT COVERED by these cells, stated rather than left implicit:
 *   * `*.integration.test.ts` runs only under `jest.integration.config.js`, so CONFIGPINNED does not
 *     read it. `ks1263-multi-write-rolls-back.integration.test.ts` currently sets the base to
 *     127.0.0.1:1 — a Fetch bad port, exactly the shape criterion 2 names — and correcting it was
 *     ruled into the KS-1310/KS-1311 PR, where that file is already open. Widening this scan to the
 *     integration config belongs with that change, not ahead of it.
 *   * These cells pin the suite's CONFIGURATION and the configured base's behaviour. They do not
 *     prove that every anchoring call site in the product routes through that base.
 */
