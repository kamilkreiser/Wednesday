-- Gate 188 r2 Q6 part 3: where the MIN subquery's plan flips, and the worst case (the hash's rows newer than every other row).
-- For each group size, a fresh hash whose rows are all created AFTER every row in the table; the MIN subquery alone is EXPLAINed.
CREATE OR REPLACE FUNCTION g188_probe(k int) RETURNS TABLE(group_rows int, plan_node text, rows_removed text, buffers text, exec_ms text) LANGUAGE plpgsql AS $f$
DECLARE h text := 'dddd' || lpad(k::text, 60, '0'); line text; node text := ''; rem text := ''; buf text := ''; ms text := '';
BEGIN
  DELETE FROM documents WHERE content_hash LIKE 'dddd%';
  INSERT INTO documents (external_id, title, document_type, content_hash, status, created_at)
  SELECT 'probe-' || g, 't', 'DOCUMENT', h, 'certified', timestamptz '2026-12-01' + (g || ' seconds')::interval FROM generate_series(1, k) g;
  ANALYZE documents;
  FOR line IN EXECUTE format('EXPLAIN (ANALYZE, BUFFERS, COSTS OFF, TIMING OFF) SELECT MIN(e.created_at) FROM documents e WHERE e.content_hash = %L OR e.content_hash = %L OR e.content_hash = %L', h, 'x' || h, 'sha256:' || h) LOOP
    IF node = '' AND (line LIKE '%Scan%') THEN node := trim(line); END IF;
    IF line LIKE '%Rows Removed by Filter%' THEN rem := trim(line); END IF;
    IF buf = '' AND line LIKE '%Buffers:%' THEN buf := trim(line); END IF;
    IF line LIKE '%Execution Time%' THEN ms := trim(line); END IF;
  END LOOP;
  RETURN QUERY SELECT k, node, rem, buf, ms;
END $f$;
SELECT count(*) AS table_rows FROM documents;
SELECT * FROM g188_probe(24);
SELECT * FROM g188_probe(100);
SELECT * FROM g188_probe(300);
SELECT * FROM g188_probe(576);
SELECT * FROM g188_probe(1000);
SELECT * FROM g188_probe(2000);
SELECT * FROM g188_probe(5000);
DELETE FROM documents WHERE content_hash LIKE 'dddd%';
DROP FUNCTION g188_probe(int);
