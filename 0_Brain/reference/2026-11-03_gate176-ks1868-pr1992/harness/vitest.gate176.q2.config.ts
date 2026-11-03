import { defineConfig } from 'vitest/config';
import { resolve } from 'node:path';
const SRC = resolve(__dirname, 'src');
const NM = resolve(__dirname, 'node_modules');
// originate has no install in this sparse clone: its bare imports resolve to packages/shared's own install.
export default defineConfig({
  resolve: {
    alias: [
      { find: '@secuura/shared/zod3-compat', replacement: resolve(SRC, 'validation/zod3-compat.ts') },
      { find: /^@secuura\/shared$/, replacement: resolve(SRC, 'index.ts') },
      { find: /^express$/, replacement: resolve(NM, 'express') },
      { find: /^uuid$/, replacement: resolve(NM, 'uuid') },
      { find: /^winston$/, replacement: resolve(NM, 'winston') },
      { find: /^zod$/, replacement: resolve(NM, 'zod') },
    ],
  },
  test: { include: ['src/__gate176__/dispatch.test.ts'], testTimeout: 300000 },
});
