# READY — KS-1350 fail500 docblock (originate webhooks.ts, COMMENTS ONLY) — Spark, comment_patch — PASS 9/9 — HELD for QA

**Held 02:16 2026-09-27 by Wednesday BY HAND** (hold_ready.py does not handle comment_patch runs). Source read: `patch.diff` == `night/briefs/KS-1350/golden/KS-1350.golden.diff` (`cmp` rc 0, sha1 d3fa0a25e1c8). C4: 2756 code tokens identical before/after — no code change. tsc + eslint rc 0 on the resulting file (runner).

## Checker verdict (verbatim)
```
PASS C0 subject: clone at 94c9c7aa9be7f0c05f4a89cdc532ec6f2fef3812, Blockchain/Dev/services/originate/src/routes/webhooks.ts present and clean, typescript 5.9.3 loads from the clone
PASS C1 output is exactly one fenced ```diff block, nothing outside it
PASS C2 diff applies at the tip (strict)
PASS C3 touched-file set == { Blockchain/Dev/services/originate/src/routes/webhooks.ts }
PASS C4 token equivalence: 2756 code tokens (kind + text, literals included) identical before and after (typescript 5.9.3 parser leaves; gaps proven trivia-only)
PASS C4b directive comments unchanged (0 before, 0 after)
PASS C5 every changed line lies inside the named lines (:549-561)
PASS C6 every brief '-' line (8) is the tip's line at its number and absent after
PASS C7 every brief '+' line (11) is in the file after, byte-exact
RESULT: PASS (9/9) apply_mode=strict
A2a rc=0: OK   Blockchain/Dev/services/originate/src/routes/webhooks.ts hunk 1 @@ -549,13: old side (13 lines) is at line 549 SUMMARY hunks=1 ok=1 bad=0 skipped_newfile=0 
```

## PR NOTES
- COMMENT-ONLY change to `Blockchain/Dev/services/originate/src/routes/webhooks.ts:549-561`. Refs KS-1350 (closes it). Tier 3 (docs/comments). Raise with (or after) the KS-1334-B / KS-1349 / KS-1348 batch; no overlap with those files.

## Canonical patch (== model == golden)
```diff
--- a/Blockchain/Dev/services/originate/src/routes/webhooks.ts
+++ b/Blockchain/Dev/services/originate/src/routes/webhooks.ts
@@ -549,13 +549,16 @@
 /**
  * KS-1341: the only place in this router that turns a caught error into a 500.
+ * All seven route catch blocks above now call it (KS-1341 parts A, B, C: #1288, #1290, #1292).
  *
- * Seven catch blocks above put the thrown error's own text in the 500 body with NO NODE_ENV
- * guard, so it reached the client in every environment, production included (measured by the
- * 2026-09-26 gate: DELETE /:id returned the thrown text, rotate-secret returned internal
- * encryption-configuration text). Same helper as routes/gdpr.ts and routes/systemErrors.ts
- * (KS-730): log the thrown text server-side with the route named, answer the constant body.
+ * Until KS-1341 those catch blocks put the thrown error's own text in the 500 body with NO
+ * NODE_ENV guard, so it reached the client in every environment, production included
+ * (measured by the 2026-09-26 gate: DELETE /:id returned the thrown text, rotate-secret
+ * returned internal encryption-configuration text). Same helper as routes/gdpr.ts and
+ * routes/systemErrors.ts (KS-730): log the thrown text server-side with the route named,
+ * answer the constant body.
  *
- * Declared at the END of the file on purpose: a function declaration is hoisted, and the
- * handlers above only call it at request time (deliverWebhook is called above its own
- * declaration the same way). Placing it here leaves every line above it where it was.
+ * Declared after every route, immediately above the default export, on purpose: a function
+ * declaration is hoisted, and the handlers above only call it at request time (deliverWebhook
+ * is called above its own declaration the same way). Placing it here left every line above it
+ * where it was.
  */
```
