import { defineConfig } from 'vitest/config';

/**
 * Pen-test H13 scaffold. Coverage thresholds are present but only enforced
 * by the explicit `npm run test:coverage` script — the default `npm test`
 * runs the suite without coverage so adding a service with zero tests
 * doesn't immediately break CI. Ratchet thresholds quarterly.
 */
export default defineConfig({
  test: {
    globals: true,
    environment: 'node',
    coverage: {
      provider: 'v8',
      reporter: ['text', 'json-summary'],
      include: ['src/**/*.ts'],
      exclude: ['src/__tests__/**', 'src/**/*.d.ts'],
      thresholds: {
        statements: 60,
        branches: 50,
        functions: 60,
        lines: 60,
      },
    },
  },
});
