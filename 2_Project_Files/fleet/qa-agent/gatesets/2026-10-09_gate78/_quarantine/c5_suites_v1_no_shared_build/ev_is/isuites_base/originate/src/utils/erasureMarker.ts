/**
 * The sentinel written into a NOT NULL text column whose contents have been
 * erased under GDPR Art. 17.
 *
 * It exists because some erased columns cannot simply be nulled:
 * `documents.title` is `character varying NOT NULL` on the live schema, so an
 * erasure has to put *something* there. Where the column IS nullable —
 * `documents.description`, `share_records.to_name`, `documents.owner_did` — the
 * erasure writes `NULL` instead, because storing nothing is a stronger erasure
 * than storing a marker.
 *
 * Kept as one exported constant rather than a repeated literal so that the
 * value a relying party sees is a contract and not a coincidence: it is quoted
 * in the OpenAPI description of `Document.title`, and a renderer or Platform S
 * matching on it is matching on something declared.
 *
 * Do not change the value without changing the spec text that quotes it.
 */
export const ERASED_MARKER = '[erased]';
