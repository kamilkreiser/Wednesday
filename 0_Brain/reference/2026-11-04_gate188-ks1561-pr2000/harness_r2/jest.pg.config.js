// Gate 188 round 2: PostgreSQL 15 harness config (adapted from Seat F 30th's pgcell/jest.pg.config.js, copied, not run in place).
// Route blobs come from MY clone's originate; @secuura/shared mapped read-only to the shared checkout's build as in round 1.
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000';
const O = W + '/repo/Blockchain/Dev/services/originate';
const SHARED = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/packages/shared';
module.exports = {
  rootDir: O,
  roots: [W + '/harness_r2'],
  testMatch: [W + '/harness_r2/**/*.harness.test.ts'],
  testEnvironment: 'node',
  transform: { '^.+\\.ts$': [O + '/node_modules/ts-jest', { tsconfig: W + '/harness_r2/tsconfig.json', diagnostics: false }] },
  moduleDirectories: ['node_modules', O + '/node_modules'],
  moduleNameMapper: {
    '^uuid$': O + '/src/testUtils/uuid-cjs.ts',
    '^@secuura/shared$': SHARED + '/dist/index.js',
    '^@secuura/shared/(.*)$': SHARED + '/dist/$1',
  },
};
