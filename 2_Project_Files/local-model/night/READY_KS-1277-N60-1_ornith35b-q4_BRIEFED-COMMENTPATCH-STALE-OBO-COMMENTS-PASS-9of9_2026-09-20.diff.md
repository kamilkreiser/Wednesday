# READY — KS-1277-N60-1 (Ornith, briefed, comment_patch) — PASS 9/9 first sample — HELD for QA

> ⚠ **CANONICAL PATCH = `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-20_ks1277-ornith35b-night/out.md.checker/patch.diff`** (from `ls` of that dir, 16:02).

**Held 16:02 2026-09-20 by the 03:3x Wednesday seat after a source read.** Tip `e47019878`. Corrects TWO STALE COMMENTS in `Blockchain/Dev/services/originate/src/routes/documents.ts` (the /revoke PLACEMENT note and the KS-480 §6 docblock) — the gate finding N60-1. **comment_patch tier: documentation only, NO behaviour change.** The checker PASSED 9/9 strict, including **C4 token equivalence (15537 code tokens identical before and after)** and C4b (directive comments unchanged); the brief also carries an INDEPENDENT line-level proof (1939 code lines, sha256 identical, with a control showing the instrument can see a difference). Source read: 6/6 `+` lines and 4/4 `-` lines are the brief;s, one file, run input sha256 `9b24be7edf29` = the queued input.

⚠ **WEDNESDAY'S RULING FOR THE RAISE:** the brief's raise note says *Closes KS-1277*. **Raise as `Refs KS-1277`, never a closing word** (the standing rule, 2026-09-19). If the ticket is then finished, the close is a Linear state op AFTER the merge, under a ruling — never a magic word. Also `Refs KS-1264` / `Refs KS-1228` are NOT to be written: both are merged work named only as the reason the prose went stale.

**HELD. Not raised.**

---
## Checker verdict (verbatim tail)
PASS C4 token equivalence: 15537 code tokens (kind + text, literals included) identical before and after (typescript 5.9.3 parser leaves; gaps proven trivia-only)
PASS C4b directive comments unchanged (0 before, 0 after)
PASS C5 every changed line lies inside the named lines (:62-66, :2327-2334)
PASS C6 every brief '-' line (4) is the tip's line at its number and absent after
PASS C7 every brief '+' line (6) is in the file after, byte-exact
RESULT: PASS (9/9) apply_mode=strict

## Diff
```diff
--- a/Blockchain/Dev/services/originate/src/routes/documents.ts
+++ b/Blockchain/Dev/services/originate/src/routes/documents.ts
@@ -62,6 +62,7 @@
- * (version / share / transfer-custody / lifecycle-events; create has its own
+ * (version / share / transfer-custody / revoke; create has its own
  * inline flow because it also overrides owner_user_id). Validates the field
  * (connector-only, 400 on shape), resolves it against the key's org (403
- * cross-org), and appends the provenance row fire-and-forget.
+ * cross-org). It appends no row: since KS-1228 the provenance row is
+ * recordOnBehalfOf's job, after the action (see below).
  *
  * KS-564: also RETURNS the resolved user id. `/share` and `/lifecycle-events`
@@ -2325,5 +2325,5 @@
       // PLACEMENT (#742 review): deliberately AFTER the 404, the ownership 403 and the
       // already-revoked 400, and NOT at the top of the handler where /share and
-      // /transfer-custody put it. handleOnBehalfOf writes an action_provenance row
+      // /transfer-custody put it. recordOnBehalfOf writes an action_provenance row
       // carrying email_enc, display_name_enc and email_hash. At the top of the handler a
       // connector could POST /api/documents/<any-string>/revoke and persist that PII
@@ -2331,5 +2331,6 @@
       // migrations/041_action_provenance.sql:33-36 makes document_id deliberately NOT a
       // foreign key and no later migration adds one, so nothing downstream rejects it.
-      // Writing it here means a row exists only for a call that was going to succeed.
+      // Since KS-1264 the row is not written here at all: recordOnBehalfOf runs after
+      // updateDocument below, so a row exists only for a revoke that actually happened.
       // /share and /transfer-custody kept the top-of-handler shape until KS-1228, which
       // moved their row (and /version's) after the action; see checkOnBehalfOf.
```
