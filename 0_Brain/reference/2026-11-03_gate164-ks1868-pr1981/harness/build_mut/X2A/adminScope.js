"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getAdminOrganisationScope = getAdminOrganisationScope;
/**
 * KS-1570 (Kam's ruling, shape b): the ADMIN ORGANISATION SCOPE of a tenant-level ADMIN.
 *
 * `admin_organisation_scopes` (migration 049) lists, per tenant and user, the organisations an ADMIN may
 * mint API keys for and revoke them from. It is read here PER DECISION (no token claim: an access token
 * lives up to a day, so a removed scope would keep working), under the caller's tenant GUC, because the
 * table is FORCE row-level security: read without the GUC it returns no rows and raises nothing.
 *
 * Returns the organisation ids granted (possibly none). It never guesses:
 *   - no tenant or no user id on the token, or a user id that cannot be a users row: nothing granted;
 *   - the database unavailable (in-memory degraded mode): nothing granted, so naming an organisation is
 *     refused, never allowed;
 *   - a read that FAILS throws. The caller answers 5xx; a broken read must not look like a refusal or an
 *     allow.
 */
const shared_1 = require("@secuura/shared");
const db_1 = require("./db");
const UUID_RE = /^[0-9a-f]{8}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{4}-[0-9a-f]{12}$/i;
async function getAdminOrganisationScope(tenantId, userId) {
    if (!(0, db_1.isDbAvailable)() || !tenantId || !userId || !UUID_RE.test(tenantId) || !UUID_RE.test(userId))
        return [];
    const result = await (0, shared_1.runWithTenantId)(tenantId, () => (0, db_1.query)(`SELECT organization_id::text AS organization_id
       FROM admin_organisation_scopes
      WHERE tenant_id = $1::uuid AND user_id = $2::uuid`, [tenantId, userId]));
    return result.rows.map((r) => r.organization_id);
}
