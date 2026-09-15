# READY — KS-1049 Part A ONLY (the evidence convention: a preflight line in CONTRIBUTING.md's Test Evidence block; the optional hook notice is a SHELL change, not here) — Ornith ornith:35b (Q4_K_M), THREE rounds: r1 a FALSE GREEN under the old doc checker (backticks dropped + bullet placed below the paragraph — found by reading after.md; D8/D9 built from it, row 99), r2 refused by D8 (a stray space inside a backtick), r3 D8 PASS (the two lines byte-for-byte) but D9 FAIL — the model places a new bullet BELOW the prose paragraph that follows the list, three rounds running (a stable dialect on this shape), run `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1049-ornith35b-night2`, 2026-09-16 00:08
# Source read by me (Wednesday): the two `+` lines below are the model's r3 output, byte-identical to the brief. The PLACEMENT is Wednesday's: the hunk is rebuilt with tip-exact context (@@ -577,6 +577,8 @@: 577–579 · the two `+` lines · 580–582) so the bullet sits after '- **Unit suites (touched services):** …' as the ticket and the brief require — proved with `patch --dry-run` strict on a copy of the tip file. Nothing removed; the hook is untouched. D4/D5 tokens (Preflight · .githooks/pre-push · SILENTLY · KS-1049) absent before / present after.
# PR NOTES for the Sunday raising seat: docs-only PR; the ticket's optional hook line (a skip notice printed by .githooks/pre-push) is a separate, shell change — cite KS-1049 and leave the ticket open for it; .github/pull_request_template.md carries no evidence block (53 lines, ack checkboxes) so nothing to mirror there.

```diff
--- a/Blockchain/Dev/CONTRIBUTING.md
+++ b/Blockchain/Dev/CONTRIBUTING.md
@@ -577,6 +577,8 @@
 - **Playwright:** run/result | not run + why
 - **Performance / k6:** run/result | not run + why
 - **Unit suites (touched services):** run/result | not run + why
+- **Preflight (the pre-push hook, .githooks/pre-push):** N/13 legs ran | NOT RUN + why — the hook skips vault-only,
+  docs-only and systemTest-only pushes SILENTLY (KS-1049), so a pushed PR is not evidence the gate ran
 
 A "NOT run" line is the point of this block, not an embarrassment in it —
 because the QA gate reads it and needs to know where to look.
```
