# READY - KS-2107-KS-2107-O106-P1 (Spark (DeepSeek V4 Flash), briefed, doc_only, markdown) - PASS 9/9 - HELD for QA

> CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2107_o106_p1_originate_anchor_emit_comments_doc_block_custody_shared_emitter/out.md.checker/patch.diff` (from `ls` at 02:23 2026-11-09; sha256[:16] 4896b423d89ef0d4, 2624 B; byte-equal to the out.md fence). Checker A2 (verbatim): `PASS A2 the diff applies at the tip (strict)`; golden comparison [round.json, verbatim]: TREE-IDENTICAL.

**Held 02:23 2026-11-09 by Wednesday after a source read (hold_ready.py, doc_only path; STRICT-APPLY leg passed first). Every clause below is copied from the run's artefacts in `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/spark_secuura_2026-11-09_ks_2107_o106_p1_originate_anchor_emit_comments_doc_block_custody_shared_emitter/out.md.checker`; the expectations were RE-MEASURED here.** Tip `c0e6e744b7b21f3e1aa28105766764775b50ce6d`. Brief: not given (--brief)
- Touched set [patch.diff `+++` headers == input.json doc_files]: ['Blockchain/Dev/services/originate/src/routes/documents.ts']; `+` lines 9 (2 NON-ASCII chars), `-` lines 5.
- Checker legs [checker.out, verbatim]:
  - `PASS A1 output is exactly one fenced ```diff block, nothing outside it`
  - `PASS A2 the diff applies at the tip (strict)`
  - `PASS A2a ANCHOR: every hunk's old side sits at its header's start line at the tip (SUMMARY hunks=3 ok=3 bad=0 skipped_newfile=0)`
  - `PASS A3 touched set == the brief's declared set (Blockchain/Dev/services/originate/src/routes/documents.ts)`
  - `PASS A4 RED AT BASE: all 7 expectation(s) fail at the untouched tip (the defect is there to be removed)`
  - `PASS A3d DOC-ONLY: 0 changed non-comment lines (14 comment line(s) changed in 1 code file(s); 0 doc file(s) are *.md / fragments)`
  - `PASS A5 GREEN AFTER: all 7 expectation(s) hold after the patch`
  - `PASS A7 REVERSION: with the patch reverse-applied, 7/7 expectation(s) fail again (the check discriminates)`
  - `PASS A8 RESTORE: 1 watched file(s) back at their tip sha256; tracked tree clean`
- RESULT [checker.out]: `RESULT: PASS (tier doc_only)`
- Expectations:
- expect_absent `KS-319. Anchoring is idempotent per` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_absent `return a resolvable anchor id (idempotent — reuses the document's` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_absent `KS-319 shared emitter: idempotent per (document, network)` - re-measured on a scratch copy of the tip file(s): before present, after absent
- expect_present `KS-319. The anchor id is idempotent per` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `Idempotent for the anchor id only: a repeat admitted event may still build and` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `a repeat admitted event may submit its own` - re-measured on a scratch copy of the tip file(s): before absent, after present
- expect_present `KS-319 shared emitter: the anchor id is idempotent per (document, network)` - re-measured on a scratch copy of the tip file(s): before absent, after present

**PR NOTES for the raise seat:** DOC_ONLY - documentation prose only, zero code bytes. Apply `patch.diff` strictly (`git apply -p1`; proven by the hold's STRICT-APPLY leg). The model wrote the prose given in the brief; Wednesday read it against the brief before this hold. No markdown link check was run.

```diff
--- a/Blockchain/Dev/services/originate/src/routes/documents.ts
+++ b/Blockchain/Dev/services/originate/src/routes/documents.ts
@@ -1387,12 +1387,14 @@
 
 /**
  * Emit (or resolve) the on-chain anchor for a non-mutating lifecycle event
- * (share / transfer-custody / revoke) — KS-319. Anchoring is idempotent per
+ * (share / transfer-custody / revoke) — KS-319. The anchor id is idempotent per
  * (document_id, network): re-anchoring an already-anchored document returns its
  * EXISTING anchor id, so the event is recorded against the existing document
  * (no new version / parent_document_id fork). Returns a resolvable anchor id
  * (GET /api/anchors/{id}) for the caller to surface, so Platform-S can persist
  * it as ExternalRef and its CardanoAnchorRefresher can upgrade it to a tx hash.
+ * Idempotent for the anchor id only: a repeat admitted event may still build and
+ * send its own transaction, and the row then names that one (KS-1384).
  * Shared so PS-123's generic lifecycle endpoint can reuse it (KS-274).
  *
  * Best-effort: the domain action (share/custody/revoke) has already committed by
@@ -2498,8 +2500,9 @@
       }).catch(() => {});
 
       // KS-319: emit the on-chain anchor for the custody-transfer event and
-      // return a resolvable anchor id (idempotent — reuses the document's
-      // existing anchor). Replaces the previously-deferred anchoredTxHash:null.
+      // return a resolvable anchor id (idempotent for the id only: it reuses the
+      // document's existing anchor, but a repeat admitted event may submit its own
+      // transaction, KS-1384). Replaces the previously-deferred anchoredTxHash:null.
       const custodyAnchor = await emitLifecycleAnchor({
         documentId: id,
         contentHash: doc.contentHash,
@@ -3146,9 +3149,10 @@
       // did not do: it recorded before validation, with an `unknown` fallback.
       recordConnectorProvenance(req, id, `lifecycle:${action}`);
 
-      // KS-319 shared emitter: idempotent per (document, network) — the event
+      // KS-319 shared emitter: the anchor id is idempotent per (document, network) — the event
       // anchors against the document's existing anchor, returning a resolvable
-      // anchor id (GET /api/anchors/{id}); null when anchoring is down (S falls
+      // anchor id (GET /api/anchors/{id}); a repeat admitted event may still submit
+      // its own transaction (KS-1384). The id is null when anchoring is down (S falls
       // back to POST /api/anchors, its existing HTTP-failure path).
       const eventAnchor = await emitLifecycleAnchor({
         documentId: id,
```
