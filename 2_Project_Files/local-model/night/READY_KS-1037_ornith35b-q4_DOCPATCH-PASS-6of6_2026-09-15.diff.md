# READY — KS-1037 (document the NO-FORCE-PUSH rule in `CONTRIBUTING.md` beside the Merge method bullet: the rule + why, the `ALLOW_FORCE=1` escape, Kam's 2026-09-07 narrow-allow ruling's scope, the merge-develop-in route and its one cost) — Ornith ornith:35b (Q4_K_M) FIRST SAMPLE (`2026-09-15_ks1037-ornith35b-night`, doc_patch) — checker PASS 6/6 at develop M55 `48e65c435`
# Source read by Wednesday 23:12: the eight `+` lines are the brief's byte-for-byte, inserted after line 107 with lines 106–107 and 108–110 intact (read in after.md); D4/D5 prove the five tokens absent before / present after in `## Branching Model — Git Flow`. Docs only — the hook is untouched (the ticket's scope). The wording is Wednesday's from the ticket's four checklist items; the ruling's scope is quoted from `secuura-force-push-own-branch-standing` as the ticket carries it.
# PR NOTES for the raising seat: (1) docs PR, tier through-code; (2) re-derive the ruling's wording from `decision_queue.sh show secuura-force-push-own-branch-standing` before merging — the brief quoted it from the ticket; (3) KS-1035 (the stale-approval cost) is linked in the ticket — cite it in the PR body; (4) the KS-1097 docs PR touches the same file (bundle in the staged brief) — land KS-1097 first, then this on top (a fast-forward).

```diff
--- a/Blockchain/Dev/CONTRIBUTING.md
+++ b/Blockchain/Dev/CONTRIBUTING.md
@@ -105,6 +105,14 @@ hotfix review must eyeball the diff for this shape.
   fold-back/tombstone mechanics below depend on shared history. Feature PRs into `develop` stay squash.
+- **No force push (KS-1037):** `.githooks/pre-push` REFUSES any non-fast-forward push to a branch that
+  already exists at origin — a rebase becomes a NEW branch. Why: a force push rewrites history another
+  process may depend on — an open PR's head, or a gate running against the SHA being replaced.
+  - `ALLOW_FORCE=1 git push …` is the escape, for the deliberate case only, stated explicitly.
+  - Scope (Kam's standing ruling, 2026-09-07, narrow-allow): permitted on your OWN unshared branch with no PR
+    and no live gate; anything shared — `develop`, `main`, a branch with an open PR — stays as it is.
+  - Behind or `dirty`? Merge `develop` INTO the branch, do not rebase: it is a fast-forward, keeps the PR and
+    its review thread, and the merge commit collapses at squash time. One cost: any new commit makes an existing approval stale.
 - The bootstrap workflow lives **only on the main line**; the KS-383 fold-back removed it from
   `develop`, so the first `release/*` merge into `main` deletes it and installs the real
   `pr-security-gates.yml`. Don't re-add it to `develop`.
```
