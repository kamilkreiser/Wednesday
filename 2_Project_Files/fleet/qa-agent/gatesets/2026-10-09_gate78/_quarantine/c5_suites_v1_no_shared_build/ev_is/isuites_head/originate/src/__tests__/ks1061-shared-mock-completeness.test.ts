/**
 * KS-1061 (QA finding F-926-2) — the guard that makes a partial
 * `@secuura/shared` mock factory impossible rather than remembered.
 *
 * Ten suites in this service each hand-wrote their own object-literal factory,
 * listing between 1 and 10 of the module's 248 exports. Every unlisted export
 * came back `undefined`, so the first cell to reach one died on a TypeError
 * about the mock rather than about the code. `ks444` shipped three keys and no
 * `safeOutboundRequest` while the sibling suite covering the same routes
 * shipped five, and nothing reconciled them.
 *
 * These cells fail if a new factory bypasses the helper, if the helper stops
 * reproducing the real export list, or if the unexported-override check stops
 * throwing.
 */
import * as fs from 'fs';
import * as path from 'path';

import { makeSharedMock } from './helpers/sharedModuleMock';

const TESTS_DIR = __dirname;

/**
 * Only the ROOT module. `@secuura/shared/crypto/jwks` is a different module.
 *
 * KS-1159 (L3b gate record F-931-G1) widened these three readers, because the guard was a text
 * scanner with three blind spots and a factory in any of them shipped a partial mock GREEN:
 *   * QUOTE STYLE. The pattern required a SINGLE-quoted module name. A double-quoted
 *     a double-quoted module name matched NEITHER pattern, so `declared` and `viaHelper` were
 *     both 0, `declared !== viaHelper` was false, and no offender was reported. Nothing pins quote
 *     style: there is no prettier config and no `quotes` rule in eslint.config.mjs.
 *   * `jest.doMock`. Only `jest.mock` was matched, and doMock registers a factory just the same.
 *   * NON-RECURSIVE WALK. `readdirSync` alone, while jest's own `testMatch`
 *     (`**\/__tests__/**\/*.test.ts`) is recursive — so a factory in `__tests__/<sub>/` was never
 *     read.
 * The VIA_HELPER require path also had to accept `../helpers/…`: once the walk is recursive, a
 * LEGITIMATE nested factory requires the helper one level up, and leaving that out would have
 * turned every nested compliant file into a false offender.
 */
const ROOT_MOCK = /jest\.(?:mock|doMock)\(\s*['"]@secuura\/shared['"]\s*,/g;
const VIA_HELPER =
  /jest\.(?:mock|doMock)\(\s*['"]@secuura\/shared['"]\s*,\s*\(\)\s*=>\s*\n?\s*require\(\s*['"](?:\.\.?\/)+helpers\/sharedModuleMock['"]\s*\)\.makeSharedMock\(/g;

/** Recursive, to match jest's own testMatch. `helpers/` holds no `.test.ts` but a subdir may. */
function testFiles(dir: string = TESTS_DIR): string[] {
  const out: string[] = [];
  for (const entry of fs.readdirSync(dir, { withFileTypes: true })) {
    const full = path.join(dir, entry.name);
    if (entry.isDirectory()) out.push(...testFiles(full));
    else if (entry.name.endsWith('.test.ts')) out.push(full);
  }
  return out;
}

describe('KS-1061 @secuura/shared mock factories are built from the real export list', () => {
  it('every root-module factory in this service goes through makeSharedMock', () => {
    const offenders: string[] = [];
    let totalFactories = 0;

    for (const file of testFiles()) {
      const src = fs.readFileSync(file, 'utf-8');
      const declared = (src.match(ROOT_MOCK) || []).length;
      const viaHelper = (src.match(VIA_HELPER) || []).length;
      totalFactories += declared;
      if (declared !== viaHelper) {
        offenders.push(`${path.basename(file)} (${declared} factories, ${viaHelper} via helper)`);
      }
    }

    // Non-zero control: if this ever reads 0 the scan found nothing and the
    // assertion below would pass vacuously.
    expect(totalFactories).toBeGreaterThanOrEqual(10);
    expect(offenders).toEqual([]);
  });

  it('the helper reproduces the real module surface, not a subset', () => {
    const actual = jest.requireActual('@secuura/shared') as Record<string, unknown>;
    const mocked = makeSharedMock();

    expect(Object.keys(actual).length).toBeGreaterThan(200);
    expect(Object.keys(mocked).sort()).toEqual(Object.keys(actual).sort());
    // The one the finding was named for.
    expect(mocked).toHaveProperty('safeOutboundRequest');
  });

  it('overrides replace the stub, and a non-export throws instead of rotting', () => {
    const marker = jest.fn();
    expect(makeSharedMock({ safeOutboundRequest: marker }).safeOutboundRequest).toBe(marker);

    expect(() => makeSharedMock({ definitelyNotAnExport: jest.fn() })).toThrow(
      /not exported by @secuura\/shared/,
    );
  });
});
