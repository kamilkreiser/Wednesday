// Gate 193: PG15 harness config. LINEAGE: Seat F 32nd's jest.pg.config.js, re-keyed to the gate's own clone.
const O = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2/repo/Blockchain/Dev';
const H = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2/pgcell';
module.exports = {
  rootDir: O + '/services/originate',
  roots: [H],
  testMatch: [H + '/**/*.harness.test.ts'],
  testEnvironment: 'node',
  cacheDirectory: '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-05_gate193-ks1986-pr2004-r2/tmp/jestcache',
  transform: { '^.+\\.ts$': [O + '/node_modules/ts-jest', { tsconfig: H + '/tsconfig.json', diagnostics: false }] },
  moduleDirectories: ['node_modules', O + '/services/originate/node_modules', O + '/node_modules'],
  moduleNameMapper: { '^uuid$': O + '/services/originate/src/testUtils/uuid-cjs.ts' },
};
