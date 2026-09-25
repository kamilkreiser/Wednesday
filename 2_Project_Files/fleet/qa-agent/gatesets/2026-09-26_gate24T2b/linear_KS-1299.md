KS-1299 OpenAPI v2 verify description still says v1's legacy bodies keep their answer — it overstates, for bodies pairing hash with a document id or data
state In Progress

## BLUF

PR **#1233** (KS-1133 + KS-1229, merged `1f1da7f35040`) documented the v1/v2 hash-alias split in the served spec. **The v2 description still carries the older claim that v1's legacy bodies keep their answer** — and that is exactly the sentence #1223 had to narrow in the *code* comment on the same day, for the same reason.

**It overstates for one case:** a body pairing `hash` with a document id **or** document data now takes the hash strategy, as v2 already does. So the spec tells an integrator something the route no longer does.

## Why this one matters more than an internal comment

It is in `docs/openapi/secuura-api.yaml` — the served spec. An integrator reading it has no other source, and the S5 probe on #1233 confirmed the served yaml is byte-identical to the merged blob, so this text is what clients actually receive.

## The fix shape

Mirror the wording that #1223 landed in the code comment: v1 reads `hash` **last** and v2 **first**, by design; a body pairing `hash` with `documentId` or `documentData` takes the hash strategy on **both**. Both routes' descriptions should say the same thing, since the point of #1233 was to stop them disagreeing.

## NOT claimed

No behaviour defect and no drift: `check:openapi` passes rc 0 at the merged tree with the drift control CAUGHT, and leg 8 read 309 paths / 343 operations json==yaml rc 0. This is the spec's prose being wrong, not the spec being out of sync with the code.

## Board search before filing (team Secuura-PK, 1,286 issues incl. archived, 3,631 comments, literal match on titles, descriptions and comments)

* `v2 description` -> **0**. `hash-alias` -> **0**.
* `legacy bodies` -> 1 total / 1 open: **KS-1133**, which is the merged ticket this residue comes from, not a separate owner of it.
* Controls that fire: `KS-1229` -> 5; `consumeResetToken` -> 3; nonsense control -> 0.

`Refs KS-1133`; does not close it.

## Provenance

Tier-2c QA gate `2026-09-25-batch1218-t2c` (report sha256 `70dc4c987f04…`), raised as a **non-blocking** finding and recorded at the merge. Filed on the coordinator's instruction after the batch landed; it did not hold the merge.
