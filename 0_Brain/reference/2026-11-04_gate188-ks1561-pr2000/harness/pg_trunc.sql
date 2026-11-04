-- Gate 188: real-engine read of the head's row-set SELECT (verify-file / /verify / v2 local share this shape).
-- Schema: docker/init/01-schema.sql at the head; parent_document_id is added by a later migration, so it is added here.
\set ON_ERROR_STOP 1
ALTER TABLE documents ADD COLUMN IF NOT EXISTS parent_document_id uuid;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS tenant_id uuid;
BEGIN;
-- B registers H first (uncertified), then A registers the same bytes N times and certifies each copy.
INSERT INTO documents (id, external_id, title, document_type, content_hash, status, created_at, certified_at, owner_user_id)
VALUES ('0b000000-0000-4000-8000-000000000000', 'B-original', 'B', 'DOCUMENT', :'h', 'anchored', '2026-07-15 10:00:00+00', NULL, '0b0b0b0b-1111-4111-8111-000000000001');
INSERT INTO documents (id, external_id, title, document_type, content_hash, status, created_at, certified_at, owner_user_id)
SELECT ('0a000000-0000-4000-8000-0000000000' || lpad(i::text, 2, '0'))::uuid, 'A-copy-' || i, 'A', 'DOCUMENT', :'h', 'certified',
       '2026-07-15 10:30:00+00'::timestamptz + (i || ' minutes')::interval,
       '2026-07-15 11:40:00+00'::timestamptz + (i || ' minutes')::interval,
       '0a0a0a0a-2222-4222-8222-000000000001'
FROM generate_series(1, :n) AS i;
-- The head's statement (verification.ts verify-file row-set, d03b0304), parameters bound to the same hash, LIMIT = VERIFY_ROWSET_LIMIT (24).
SELECT count(*) AS fetched,
       bool_or(external_id = 'B-original') AS original_in_fetched_set,
       min(created_at) AS earliest_in_fetched_set
FROM (
  SELECT d.id, d.external_id, d.title, d.document_type, d.content_hash, d.status,
         d.certification_metadata, d.metadata, d.created_at, d.certified_at,
         d.tenant_id, d.parent_document_id, d.owner_user_id, d.issuer_organization_id, o.name AS organization_name
  FROM documents d
  LEFT JOIN organizations o ON d.issuer_organization_id = o.id
  WHERE d.content_hash = :'h' OR d.content_hash = :'h' OR d.content_hash = 'sha256:' || :'h'
  ORDER BY d.certified_at DESC NULLS LAST
  LIMIT 24
) s;
ROLLBACK;
