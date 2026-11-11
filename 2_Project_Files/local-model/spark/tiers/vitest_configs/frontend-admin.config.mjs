// HARNESS-SUPPLIED vitest config for Blockchain/Dev/frontend/admin (Spark o136, 2026-11-11). NOT a product file: it lives in
// the harness (local-model/spark/tiers/vitest_configs/), is passed as an ABSOLUTE `--config` by the checker, and is never
// copied into, or diffed against, any repo tree. frontend/admin has no vitest config of its own at the tip (vite.config.ts has
// no `test:` block) and no test files. It mirrors frontend/issuer's: jsdom + globals, the package's `@` / `@shared` aliases
// from its vite.config.ts, the automatic JSX runtime its tsconfig names. Self-contained on purpose (no imports beyond node:):
// a config file outside the repo cannot resolve `vite`/`vitest/config` from where it sits. The run's cwd is the package dir.
//
// ONE React is NOT done here (measured 2026-11-11: an alias reaches only what the bundler sees, and lucide-react / react-dom are
// loaded natively): spark/dedupe_admin_react.sh makes frontend/admin/node_modules/{react,react-dom,scheduler} in the deps store
// symlinks to the workspace root's copies, so Node's realpath resolution finds one React everywhere.
import path from 'node:path';

const root = process.cwd();

export default {
  root,
  resolve: {
    alias: [
      { find: '@shared', replacement: path.resolve(root, process.env.SHARED_DIR || '../shared/src') },
      { find: /^@\//, replacement: path.resolve(root, 'src') + '/' },
    ],
  },
  esbuild: { jsx: 'automatic' },
  test: {
    environment: 'jsdom',
    globals: true,
    setupFiles: [],
    include: ['src/**/*.test.{ts,tsx}'],
  },
};
