import { defineConfig } from 'vitest/config';
export default defineConfig({
  test: { globals: true, environment: 'node', setupFiles: ['./vitest.setup.ts'], include: ['src/__gate177__/**/*.test.ts'], testTimeout: 300000, fileParallelism: false },
});
