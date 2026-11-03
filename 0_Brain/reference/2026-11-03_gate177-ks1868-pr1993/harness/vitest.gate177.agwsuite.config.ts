// Gate 177: api-gateway's own vitest settings (vitest.config.ts) PLUS aliases that resolve @secuura/shared (and each
// subpath in packages/shared/package.json "exports") to the SAME tree's packages/shared/src, because the sparse clone has
// no workspace link or built dist. Identical file at base and head.
import { defineConfig } from 'vitest/config';
import { resolve } from 'node:path';
const SHARED = resolve(__dirname, '../../packages/shared');
export default defineConfig({
  resolve: {
    alias: [
      { find: /^@secuura\/shared\/security\/secrets-manager$/, replacement: resolve(SHARED, 'src/security/secrets-manager.ts') },
      { find: /^@secuura\/shared\/security\/gdpr-compliance$/, replacement: resolve(SHARED, 'src/security/gdpr-compliance.ts') },
      { find: /^@secuura\/shared\/security\/token-rotation$/, replacement: resolve(SHARED, 'src/security/token-rotation.ts') },
      { find: /^@secuura\/shared\/documents\/default-type$/, replacement: resolve(SHARED, 'src/documents/defaultDocumentType.ts') },
      { find: /^@secuura\/shared\/security\/audit-logger$/, replacement: resolve(SHARED, 'src/security/audit-logger.ts') },
      { find: /^@secuura\/shared\/crypto\/hybrid-kem$/, replacement: resolve(SHARED, 'src/crypto/hybrid-kem.ts') },
      { find: /^@secuura\/shared\/crypto\/registry$/, replacement: resolve(SHARED, 'src/crypto/registry.ts') },
      { find: /^@secuura\/shared\/vault\/key-vault$/, replacement: resolve(SHARED, 'src/vault/key-vault.ts') },
      { find: /^@secuura\/shared\/security\/scopes$/, replacement: resolve(SHARED, 'src/security/scopes.ts') },
      { find: /^@secuura\/shared\/db\/optimization$/, replacement: resolve(SHARED, 'src/db/optimization.ts') },
      { find: /^@secuura\/shared\/crypto\/jwks$/, replacement: resolve(SHARED, 'src/crypto/jwks.ts') },
      { find: /^@secuura\/shared\/cache\/redis$/, replacement: resolve(SHARED, 'src/cache/redis.ts') },
      { find: /^@secuura\/shared\/zod3-compat$/, replacement: resolve(SHARED, 'src/validation/zod3-compat.ts') },
      { find: /^@secuura\/shared\/validation$/, replacement: resolve(SHARED, 'src/validation/index.ts') },
      { find: /^@secuura\/shared\/middleware$/, replacement: resolve(SHARED, 'src/middleware/index.ts') },
      { find: /^@secuura\/shared\/pagination$/, replacement: resolve(SHARED, 'src/pagination/index.ts') },
      { find: /^@secuura\/shared\/security$/, replacement: resolve(SHARED, 'src/security/index.ts') },
      { find: /^@secuura\/shared\/logger$/, replacement: resolve(SHARED, 'src/logger/index.ts') },
      { find: /^@secuura\/shared\/crypto$/, replacement: resolve(SHARED, 'src/crypto/index.ts') },
      { find: /^@secuura\/shared\/errors$/, replacement: resolve(SHARED, 'src/errors/index.ts') },
      { find: /^@secuura\/shared\/config$/, replacement: resolve(SHARED, 'src/config/index.ts') },
      { find: /^@secuura\/shared\/events$/, replacement: resolve(SHARED, 'src/events/index.ts') },
      { find: /^@secuura\/shared\/vc$/, replacement: resolve(SHARED, 'src/vc/index.ts') },
      { find: /^@secuura\/shared\/db$/, replacement: resolve(SHARED, 'src/db/index.ts') },
      { find: /^@secuura\/shared$/, replacement: resolve(SHARED, 'src/index.ts') },
    ],
  },
  test: { globals: true, environment: 'node', setupFiles: ['./vitest.setup.ts'] },
});
