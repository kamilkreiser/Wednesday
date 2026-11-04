-- Gate 188 r2 Q6: cost of the originals read on a migrated DB (migration 001 at f702d4da4b69), realistic size.
-- Seed once: 300,000 rows over 100,000 other hashes + one hot hash with 5,000 rows (the later 4,999 certified), then ANALYZE.
\set hot '''aaaa000000000000000000000000000000000000000000000000000000000hot'''
ALTER TABLE documents ADD COLUMN IF NOT EXISTS parent_document_id uuid;
ALTER TABLE documents ADD COLUMN IF NOT EXISTS tenant_id uuid;
TRUNCATE documents CASCADE;
INSERT INTO documents (external_id, title, document_type, content_hash, status, created_at, certified_at)
SELECT 'bulk-' || g, 't', 'DOCUMENT', md5((g % 100000)::text) || md5((g % 100000)::text),
       CASE WHEN g % 3 = 0 THEN 'certified' ELSE 'anchored' END,
       now() - (g || ' seconds')::interval, CASE WHEN g % 3 = 0 THEN now() - ((g/2) || ' seconds')::interval END
FROM generate_series(1, 300000) g;
INSERT INTO documents (external_id, title, document_type, content_hash, status, created_at, certified_at)
SELECT 'hot-' || g, 't', 'DOCUMENT', :hot,
       CASE WHEN g = 1 THEN 'anchored' ELSE 'certified' END,
       timestamptz '2026-01-01' + (g || ' minutes')::interval,
       CASE WHEN g = 1 THEN NULL ELSE timestamptz '2026-06-01' + (g || ' minutes')::interval END
FROM generate_series(1, 5000) g;
ANALYZE documents;
SELECT count(*) AS total_rows, count(*) FILTER (WHERE content_hash = :hot) AS hot_rows, count(DISTINCT content_hash) AS hashes FROM documents;

\echo '=== A. row-set read (unchanged since base), hot hash'
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF)
SELECT d.id, d.created_at, d.certified_at, o.name FROM documents d LEFT JOIN organizations o ON d.issuer_organization_id = o.id
WHERE d.content_hash = :hot OR d.content_hash = 'x' || :hot OR d.content_hash = 'sha256:' || :hot
ORDER BY d.certified_at DESC NULLS LAST LIMIT 24;

\echo '=== B. ORIGINAL_ROWS_POOL_SQL (round 2, verbatim shape), hot hash'
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF)
SELECT d.id, d.external_id, d.title, d.document_type, d.content_hash, d.status,
         d.certification_metadata, d.metadata, d.created_at, d.certified_at,
         d.tenant_id, d.parent_document_id, d.owner_user_id, d.issuer_organization_id, o.name AS organization_name
  FROM documents d
  LEFT JOIN organizations o ON d.issuer_organization_id = o.id
  WHERE (d.content_hash = :hot OR d.content_hash = 'x' || :hot OR d.content_hash = 'sha256:' || :hot)
    AND d.created_at = (SELECT MIN(e.created_at) FROM documents e WHERE e.content_hash = :hot OR e.content_hash = 'x' || :hot OR e.content_hash = 'sha256:' || :hot)
  ORDER BY d.id
  LIMIT 25;

\echo '=== B2. the same with $n parameters, generic plan forced (what a prepared/pg-driver statement can run)'
SET plan_cache_mode = force_generic_plan;
PREPARE orig(text, text, text) AS
SELECT d.id, d.created_at FROM documents d LEFT JOIN organizations o ON d.issuer_organization_id = o.id
  WHERE (d.content_hash = $1 OR d.content_hash = $2 OR d.content_hash = $3)
    AND d.created_at = (SELECT MIN(e.created_at) FROM documents e WHERE e.content_hash = $1 OR e.content_hash = $2 OR e.content_hash = $3)
  ORDER BY d.id LIMIT 25;
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF) EXECUTE orig(:hot, 'x' || :hot, 'sha256:' || :hot);
DEALLOCATE orig;
RESET plan_cache_mode;

\echo '=== C. CONTROL: the same read with idx_documents_content_hash dropped (in a rolled-back transaction): the instrument shows a Seq Scan'
BEGIN;
DROP INDEX idx_documents_content_hash;
EXPLAIN (COSTS OFF)
SELECT d.id FROM documents d
  WHERE (d.content_hash = :hot OR d.content_hash = 'x' || :hot OR d.content_hash = 'sha256:' || :hot)
    AND d.created_at = (SELECT MIN(e.created_at) FROM documents e WHERE e.content_hash = :hot OR e.content_hash = 'x' || :hot OR e.content_hash = 'sha256:' || :hot)
  ORDER BY d.id LIMIT 25;
ROLLBACK;
