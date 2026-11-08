# READY - KS-2107-KS-2107-O106-P2 (Spark (DeepSeek V4 Flash), briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2107_o106_p2_originate_anchor_emit_comments_share_and_revoke/out.md.checker/patch.diff` (from `ls` at 02:23 2026-11-09; sha256[:16] ec90ffe985b80086, 1448 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 02:23 2026-11-09 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2107_o106_p2_originate_anchor_emit_comments_share_and_revoke/out.md.checker`; the expectations were RE-MEASURED here.** Tip `c0e6e744b7b21f3e1aa28105766764775b50ce6d`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/services/originate/src/routes/documents.ts']; `+` lines 4 (ASCII), `-` lines 2.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=2 ok=2 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/originate/src/routes/documents.ts)`
  - `PASS A4 RED AT BASE: all 3 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (6 comment line(s) changed in 1 code file(s); 0 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 3 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 3/3 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `resolvable anchor id (idempotent — reuses the document's existing anchor).` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `resolvable anchor id (idempotent for the id only: it reuses the document's` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `existing anchor, but a repeat admitted event may submit its own transaction, KS-1384).` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/documents.ts
+++ b/Blockchain/Dev/services/originate/src/routes/documents.ts
@@ -2918,7 +2918,8 @@
       recordOnBehalfOf(req, id, 'share', shareObo);
 
       // KS-319: emit the on-chain anchor for the share event + return a
-      // resolvable anchor id (idempotent — reuses the document's existing anchor).
+      // resolvable anchor id (idempotent for the id only: it reuses the document's
+      // existing anchor, but a repeat admitted event may submit its own transaction, KS-1384).
       const shareAnchor = await emitLifecycleAnchor({
         documentId: id,
         contentHash: doc.contentHash,
@@ -3020,7 +3021,8 @@
       // KS-1264: the row is recorded only now, after updateDocument, so a revoke that throws writes none.
       recordOnBehalfOf(req, id, 'revoke', revokeObo);
       // KS-319: emit the on-chain anchor for the revoke event + return a
-      // resolvable anchor id (idempotent — reuses the document's existing anchor).
+      // resolvable anchor id (idempotent for the id only: it reuses the document's
+      // existing anchor, but a repeat admitted event may submit its own transaction, KS-1384).
       // K `revoke` = global invalidation of the document (status:'revoked'); S's
       // owner-local soft-delete routes here per PS-124 (semantics noted) — the
       // anchor records the revoke against the existing document, not a derived one.
```
