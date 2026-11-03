"use strict";
/**
 * =============================================================================
 * API-KEY REVOKE — this service's half (KS-643 / KS-764 / KS-578)
 * =============================================================================
 * The DECISION moved to `@secuura/shared` (KS-764, QA F-764-01) so that
 * `originate`'s sibling revoke route can be bound to the same rule instead of
 * carrying a second copy of it. It is re-exported here unchanged, so every
 * existing import of this module — including this service's own routes and the
 * KS-764 test suite — keeps working and there is exactly one implementation.
 *
 * What stays: `lookupKeyForRevoke`, which needs this service's pool and the
 * platform-scope wrapper. That is the half that cannot be shared.
 * =============================================================================
 */
Object.defineProperty(exports, "__esModule", { value: true });
exports.decideKeyRevoke = exports.decideTenantAccess = exports.isPlatformRole = exports.isScopedAdminRole = exports.isOrgBoundedRole = void 0;
exports.lookupKeyForRevoke = lookupKeyForRevoke;
const shared_1 = require("@secuura/shared");
const db_1 = require("./db");
var shared_2 = require("@secuura/shared");
Object.defineProperty(exports, "isOrgBoundedRole", { enumerable: true, get: function () { return shared_2.isOrgBoundedRole; } });
Object.defineProperty(exports, "isScopedAdminRole", { enumerable: true, get: function () { return shared_2.isScopedAdminRole; } });
Object.defineProperty(exports, "isPlatformRole", { enumerable: true, get: function () { return shared_2.isPlatformRole; } });
Object.defineProperty(exports, "decideTenantAccess", { enumerable: true, get: function () { return shared_2.decideTenantAccess; } });
Object.defineProperty(exports, "decideKeyRevoke", { enumerable: true, get: function () { return shared_2.decideKeyRevoke; } });
/**
 * KS-578: resolve the key for a revoke regardless of the caller's tenant GUC.
 *
 * Under migration 039 (FORCE RLS) the `tenant_isolation` policy needs either a
 * matching `app.current_tenant_id` or `app.tenant_scope_bypass='platform_admin'`,
 * and services connect as `secuura_app`, which holds neither BYPASSRLS nor
 * superuser. So a foreign-tenant row read under the caller's GUC returns zero
 * rows and the handler 404s on a key that exists.
 *
 * The wrap is on this ONE lookup and nothing else — same shape as the
 * admin-authorised organisation lookup already in this service (index.ts:826),
 * not a widening of the bypass surface. It is safe only because every caller
 * routes the result through `decideKeyRevoke` above.
 *
 * NOTE on the ticket's stated repro: it says the miss happens "straight after a
 * restart". It does not — `loadFromDb` warms the in-memory cache with an
 * unbounded cross-tenant `SELECT * FROM svc_api_keys` (boot log: `apiKeys: 821`,
 * the whole table), so the cache is at its FULLEST after a restart. The real
 * window is a key written by ANOTHER service after this one booted, which the
 * cache has never seen.
 */
async function lookupKeyForRevoke(id) {
    const result = await (0, shared_1.runWithPlatformScope)(() => (0, db_1.query)('SELECT * FROM svc_api_keys WHERE id = $1', [id]));
    return result.rows.length > 0 ? result.rows[0] : undefined;
}
