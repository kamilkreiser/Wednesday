# READY — KS-1120-F3 (comment_patch, comment lines only: vc-issuer ks1020 test :29-31 + :190-193 — the pgModel comments stop claiming PostgreSQL semantics (_, interior %, escapes not modelled))
# Source read by Wednesday 21:10: the model's 16 fence body lines IDENTICAL to the brief's (python compare; a mutated copy unequal); checker RESULT PASS (9/9) apply_mode=strict (C4 code tokens identical; C5 inside the named lines; C6/C7 byte-exact). Tip = develop 75ad0e55c.
# PR NOTES: `Refs KS-1120 (F-3)`, never Closes — Wednesday routed the REWORD option; the pgModel rewrite stays open on the ticket. TIER: comment-only → through-code. Run: runs/2026-09-17_ks1120-ornith35b-night/out.md.

```diff
--- a/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts
+++ b/Blockchain/Dev/services/vc-issuer/src/__tests__/ks1020-presentation-lookup-exact-or-404.test.ts
@@ -27,6 +27,7 @@
  *    uuid) are red at base by construction. The exact id, URL-encoded because
  *    it carries `/` and `:`, is the 200 control.
- *  - DB path (isDbAvailable() true, `query` mocked with a model of PostgreSQL
- *    `=` / `LIKE` semantics over one fixed row): an unknown id must cost
+ *  - DB path (isDbAvailable() true, `query` mocked with a model of `=` and of
+ *    a `%`-wrapped substring LIKE over one fixed row; `_`, interior `%` and
+ *    escapes are not modelled): an unknown id must cost
  *    exactly ONE query whose SQL is the exact `WHERE id = $1` and never a LIKE,
  *    and answer 404. Those two cells (C1, S1) cannot be satisfied by a lucky
@@ -188,5 +189,6 @@
 
   /**
-   * A model of PostgreSQL `=` and `LIKE` over the one stored row: `%` at either
+   * A model of `=` and of a `%`-wrapped substring LIKE over the one stored row;
+   * `_`, interior `%` and escapes are not modelled. Here `%` at either
    * end of the pattern is a wildcard, no `%` means an exact comparison — so a
    * `LIKE '%0%'` matches the row and a `LIKE '0'` does not.
```
