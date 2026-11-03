import { defineConfig } from 'vitest/config';
import { resolve } from 'node:path';
const SRC = resolve(__dirname, 'src');
export default defineConfig({
  resolve: {
    alias: [
      { find: '@secuura/shared/zod3-compat', replacement: resolve(SRC, 'validation/zod3-compat.ts') },
      { find: /^@secuura\/shared$/, replacement: resolve(SRC, 'index.ts') },
    ],
  },
  test: { include: ['src/__gate177__/**/*.test.ts'], testTimeout: 300000, fileParallelism: false },
});
