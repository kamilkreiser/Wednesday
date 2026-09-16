// qa-netredirect.config.ts — the package's own vitest config plus the redirect setupFile (scratch clone only).
import { defineConfig, mergeConfig } from 'vitest/config';
import base from './vitest.config';
export default mergeConfig(base, defineConfig({ test: { setupFiles: ['./qa-netredirect.setup.ts'] } }));
