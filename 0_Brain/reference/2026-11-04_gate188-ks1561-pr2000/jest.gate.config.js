// Gate 188 harness config. Wraps the clone's own originate jest.config.js unchanged, and adds ONE thing:
// @secuura/shared resolves to the (read-only) shared checkout's packages/shared build, because the monorepo
// workspace link that provides it is not part of originate's lock and a second install is forbidden (disk).
// packages/shared's source tree is byte-identical at base d92b849e, head d03b0304 and the checkout's HEAD
// (tree d94503e350c8 at all three). Every suite that uses it wraps it in makeSharedMock (functions -> jest.fn).
const W = '/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-04_gate188-ks1561-pr2000';
const O = process.env.GATE_O || (W + '/repo/Blockchain/Dev/services/originate');
const SHARED = '/Volumes/DevMASTER/!CODING/Secuura/Blockchain/2_Project_Files/Blockchain/Dev/packages/shared';
const base = require(O + '/jest.config.js');
module.exports = {
  ...base,
  rootDir: O,
  moduleNameMapper: {
    ...base.moduleNameMapper,
    '^@secuura/shared$': SHARED + '/dist/index.js',
    '^@secuura/shared/(.*)$': SHARED + '/dist/$1',
  },
  transform: { '^.+\\.tsx?$': ['ts-jest', { tsconfig: W + '/tsconfig.gate.json' }] },
};
