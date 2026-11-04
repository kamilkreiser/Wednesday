-- Gate 188 r2 Q6 part 2: the planner's choice for MIN(created_at) when the hash's rows are the NEWEST in the table
-- (a recently registered file; explain.sql's hot hash was the OLDEST, the planner's best case). Same DB as explain.sql.
\set n30 '''bbbb0000000000000000000000000000000000000000000000000000000new30'''
\set n5k '''cccc0000000000000000000000000000000000000000000000000000000new5k'''
DELETE FROM documents WHERE content_hash IN (:n30, :n5k);
INSERT INTO documents (external_id, title, document_type, content_hash, status, created_at, certified_at)
SELECT 'new30-' || g, 't', 'DOCUMENT', :n30, CASE WHEN g = 1 THEN 'anchored' ELSE 'certified' END,
       timestamptz '2026-11-03' + (g || ' minutes')::interval, CASE WHEN g = 1 THEN NULL ELSE timestamptz '2026-11-03 12:00' + (g || ' minutes')::interval END
FROM generate_series(1, 30) g;
INSERT INTO documents (external_id, title, document_type, content_hash, status, created_at, certified_at)
SELECT 'new5k-' || g, 't', 'DOCUMENT', :n5k, CASE WHEN g = 1 THEN 'anchored' ELSE 'certified' END,
       timestamptz '2026-11-03' + (g || ' seconds')::interval, CASE WHEN g = 1 THEN NULL ELSE timestamptz '2026-11-03 12:00' + (g || ' seconds')::interval END
FROM generate_series(1, 5000) g;
ANALYZE documents;
SELECT min(created_at) AS table_oldest, max(created_at) FILTER (WHERE content_hash NOT IN (:n30, :n5k)) AS bulk_newest,
       min(created_at) FILTER (WHERE content_hash = :n30) AS n30_first, count(*) AS total FROM documents;

\echo '=== D. ORIGINAL_ROWS_POOL_SQL, 30-row hash whose rows are the newest (literal values = custom plan)'
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF)
SELECT d.id, d.created_at, o.name FROM documents d LEFT JOIN organizations o ON d.issuer_organization_id = o.id
  WHERE (d.content_hash = :n30 OR d.content_hash = 'x' || :n30 OR d.content_hash = 'sha256:' || :n30)
    AND d.created_at = (SELECT MIN(e.created_at) FROM documents e WHERE e.content_hash = :n30 OR e.content_hash = 'x' || :n30 OR e.content_hash = 'sha256:' || :n30)
  ORDER BY d.id LIMIT 25;

\echo '=== E. ORIGINAL_ROWS_POOL_SQL, 5,000-row hash whose rows are the newest'
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF)
SELECT d.id, d.created_at, o.name FROM documents d LEFT JOIN organizations o ON d.issuer_organization_id = o.id
  WHERE (d.content_hash = :n5k OR d.content_hash = 'x' || :n5k OR d.content_hash = 'sha256:' || :n5k)
    AND d.created_at = (SELECT MIN(e.created_at) FROM documents e WHERE e.content_hash = :n5k OR e.content_hash = 'x' || :n5k OR e.content_hash = 'sha256:' || :n5k)
  ORDER BY d.id LIMIT 25;

\echo '=== F. via node-pg-style parameters ($1..$3, unnamed statement = custom plan), 5,000-row newest hash'
PREPARE origp(text, text, text) AS
SELECT d.id, d.created_at FROM documents d LEFT JOIN organizations o ON d.issuer_organization_id = o.id
  WHERE (d.content_hash = $1 OR d.content_hash = $2 OR d.content_hash = $3)
    AND d.created_at = (SELECT MIN(e.created_at) FROM documents e WHERE e.content_hash = $1 OR e.content_hash = $2 OR e.content_hash = $3)
  ORDER BY d.id LIMIT 25;
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF) EXECUTE origp(:n5k, 'x' || :n5k, 'sha256:' || :n5k);
DEALLOCATE origp;

\echo '=== G. CONTROL: the row-set read (unchanged since base) on the same 5,000-row newest hash'
EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF)
SELECT d.id FROM documents d LEFT JOIN organizations o ON d.issuer_organization_id = o.id
WHERE d.content_hash = :n5k OR d.content_hash = 'x' || :n5k OR d.content_hash = 'sha256:' || :n5k
ORDER BY d.certified_at DESC NULLS LAST LIMIT 24;
