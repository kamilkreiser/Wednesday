module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.test.ts'],
  // Integration tests are DB-backed and run via jest.integration.config.js
  // (`npm run test:integration`); the default run stays unit-only + mock-DB.
  testPathIgnorePatterns: ['/node_modules/', '\\.integration\\.test\\.ts$'],
  moduleFileExtensions: ['ts', 'js', 'json'],
  // uuid@14 is ESM-only and jest's CJS runtime can't parse it — every suite
  // importing routes/repos load-failed since the bump (KS-466 fix). The stub
  // exports the one API the service uses (v4). Runtime uses the real package.
  moduleNameMapper: {
    '^uuid$': '<rootDir>/src/testUtils/uuid-cjs.ts',
  },
};
