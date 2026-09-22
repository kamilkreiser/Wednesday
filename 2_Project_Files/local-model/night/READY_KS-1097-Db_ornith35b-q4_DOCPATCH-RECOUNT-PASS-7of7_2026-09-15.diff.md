# READY — KS-1097 PART D-b of five (repo-root `CLAUDE.md` lines 256–258 → ONE line: the QA-2 annotation now names the pending ruling — raise-to-1, Kam's card `secuura-required-approvals-zero-after-the-untick`, Kam applies it himself, not yet applied — and says "do not turn it on while fleet PRs carry 0 GitHub reviews")
# Source read by me (Wednesday): three `-` lines are 256–258 verbatim, ONE `+` line is the brief's; applied with --recount (miscounted header only); D7 3/3; after.md 482 lines (484 − 2), the old "Kam has ruled…" text gone, one NOT APPLIED. First sample on the split shape (the unsplit D needed three rounds: r2 a false green caught by D7 after the fact, r3 the wrong three lines caught by D7). Run: runs/2026-09-15_ks1097-ornith35b-night12.
# PR NOTES: KS-1097 is COMPLETE in Ornith's hands — ONE docs PR: A (DEV-PROCESS.md) + B + C (CONTRIBUTING.md) + D-a + D-b (repo-root CLAUDE.md). Tier-2 docs gate at head, Wednesday's GO. NOT in the PR: CONTRIBUTING:531-532, DEV-PROCESS:26 (Kam's red-pen lines), `.github/workflows/`. The project-root untracked `CLAUDE.md` mirror is done by hand after merge.

```diff
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -255,5 +255,3 @@
   so a missing box/ticket fails the check, then (2) add the check names to the develop AND
-  main `require-pr-gates` rulesets and turn on required reviews = 1 (any writer). *[NOT APPLIED (2026-09-11, KS-1095): Kam has
-  ruled on the required-approvals setting and that ruling is not yet applied; turning required reviews on
-  while fleet PRs carry 0 GitHub reviews would block every fleet merge.]* The former
+  main `require-pr-gates` rulesets and turn on required reviews = 1 (any writer). *[NOT APPLIED (2026-09-11, KS-1095): the pending ruling is raise-to-1 (Kam's card `secuura-required-approvals-zero-after-the-untick`; Kam applies it himself; not yet applied) — do not turn it on while fleet PRs carry 0 GitHub reviews: it would block every fleet merge.]* The former
    Environment-based sign-off jobs were removed in favour of this checkbox approach.
```

# SUPERSEDED-BY (feed11 drafter, 2026-09-22 12:57:28 AEST): re-briefed at develop 8c2f7b3fd as night/briefs/KS-1097-R16B-CLAUDEMD.md (golden PASS through the real checker in the feed11 precheck clone; Wednesday queues). This READY is STALE - do not raise it.
