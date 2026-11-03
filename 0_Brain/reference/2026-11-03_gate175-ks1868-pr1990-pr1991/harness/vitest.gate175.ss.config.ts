import { defineConfig } from 'vitest/config';
export default defineConfig({ test: { include: ['src/__gate175__/**/*.test.ts'], testTimeout: 120000, fileParallelism: false } });
