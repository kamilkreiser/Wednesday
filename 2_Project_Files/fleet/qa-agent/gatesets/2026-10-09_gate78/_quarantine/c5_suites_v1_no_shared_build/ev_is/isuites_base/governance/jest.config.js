/** @type {import('ts-jest').JestConfigWithTsJest} */
module.exports = {
  preset: 'ts-jest',
  testEnvironment: 'node',
  roots: ['<rootDir>/src'],
  testMatch: ['**/__tests__/**/*.test.ts'],
  moduleFileExtensions: ['ts', 'js', 'json'],
  testTimeout: 10000,
  // KS-594: `uuid` is ESM-only from v14, and jest's default CJS runtime does not
  // transform anything under node_modules — so `import { v4 } from 'uuid'` threw
  // `SyntaxError: Unexpected token 'export'` at module load and took the WHOLE
  // suite down before a single test ran. Transform that one package instead of
  // stubbing it, so the tests keep exercising the real uuid.
  transform: {
    '^.+\\.tsx?$': ['ts-jest', {}],
    '^.+\\.jsx?$': ['ts-jest', { tsconfig: { allowJs: true, module: 'commonjs' } }],
  },
  transformIgnorePatterns: ['/node_modules/(?!(uuid)/)'],
};
