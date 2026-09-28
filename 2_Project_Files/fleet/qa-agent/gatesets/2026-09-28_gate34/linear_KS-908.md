KS-908 connectorId persists but is invisible through the API — POST and GET both return null while the row holds the value
state In Progress

## `connectorId` persists correctly but is invisible through the API — a Platform S caller cannot read back the connector it just set

Found during probe 5(ii) on the demo box, 2026-09-06, against `security` rebuilt from `db1848abf` (KS-869's code live: `connector_id` 7 occurrences in `/app/dist`, 0 in the pre-rebuild image).

### What happens

`POST /api/security/keys` with `connectorId: "probe-connector-20260906T084007Z"`:

* **HTTP 201.** Response body carries `connectorId: null`.
* `GET /api/security/keys?organizationId=…` for the same key: `connectorId: null`.
* **The database has the value**: `SELECT connector_id FROM svc_api_keys WHERE name = 'wednesday-probe-20260906T084007Z'` → `probe-connector-20260906T084007Z`.

So KS-869's write half works — the totals moved **39 rows / 0 connectors → 40 / 1**, exactly one new row with exactly one connector. What does not work is the read-back: **neither the write response nor the list response exposes the field**, so the only way to confirm a connector was recorded is direct database access, which an integrator does not have.

### Why it matters

The S↔K ownership contract has Platform S minting connector-scoped keys through this endpoint. Under KS-843's cutover the connector is load-bearing. An integrator that sets `connectorId` and reads the response back sees `null` and cannot distinguish "not persisted" from "persisted but not returned" — the two have opposite remedies.

`rowToApiKey` (`services/security/src/index.ts:345`) does map `connectorId`, which suggests the write and list responses are served from the in-memory representation rather than a row read — that is a hypothesis, stated as one; the measurement above is not.

### Controls

* Impossible token in the same image → 0.
* Validate on the revoked probe key → `valid:false, reason:"Key revoked"`; on a key that never existed → `valid:false, reason:"Key not found"`. Different reasons, so the API's own instruments do discriminate — this is not a blanket read failure.

### Housekeeping

The probe key `wednesday-probe-20260906T084007Z` was revoked in-leg through the API (`DELETE`, HTTP 200) and the revocation confirmed two ways: `is_active = f` in the row, and `validate` → `"Key revoked"`. No probe key is live.

Related: KS-869 (the write), KS-889 (the empty backfill window), KS-887 (the write-half pin that cannot discriminate).
