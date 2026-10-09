// Integration tests (DB-backed). Kept separate from the default unit run
// (jest.config.js), which mocks the DB. Run with `npm run test:integration`
// and a Postgres reachable via TEST_DATABASE_URL (+ TEST_PLATFORM_DATABASE_URL),
// falling back to the service's DATABASE_URL / PLATFORM_DATABASE_URL.
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.integration.test.ts'],
  moduleFileExtensions: ['ts', 'js', 'json'],
  // KS-466, applied here too: uuid@14 is ESM-only and jest's CJS runtime cannot
  // parse it, so every suite importing a repository load-fails. jest.config.js
  // has carried this mapper since the bump; this config did not, which only
  // became visible when an integration suite first imported documentRepo.
  // Runtime uses the real package.
  moduleNameMapper: {
    '^uuid$': '<rootDir>/src/testUtils/uuid-cjs.ts',
  },
  testTimeout: 30000,
};
