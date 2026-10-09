/**
 * Jest-only CJS stand-in for `uuid` (mapped via jest.config.js
 * moduleNameMapper). uuid@14 is ESM-only, and jest's CJS runtime cannot parse
 * it (`SyntaxError: Unexpected token 'export'`) — which silently load-failed
 * every suite importing a module that touches uuid (the routes/repos tests)
 * since the KS-459/KS-420-era bump. The service uses exactly one export.
 *
 * Runtime containers are unaffected: Node ≥20.19 `require(esm)` loads the
 * real package.
 */
import { randomUUID } from 'node:crypto';

export const v4 = (): string => randomUUID();
