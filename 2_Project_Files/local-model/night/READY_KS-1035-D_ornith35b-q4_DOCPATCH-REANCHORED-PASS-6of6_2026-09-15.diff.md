# READY — KS-1035 Part D ONLY (checklist item: write the withdrawn-approval rule into docs/DEV-PROCESS.md next to the at-head paragraph) — Ornith ornith:35b (Q4_K_M) PASS 6/6 FIRST SAMPLE (the run's own verdict was FAIL D4/D6: the doc checker's section() knew `## ` and `# ` only and the brief named a `### ` sub-heading — fixed where it lives, row 97, re-checked in the run's clone → PASS 6/6, verdict retracted in done.md), doc_patch D2 REANCHORED (the model over-indented its context lines; the six `+` lines are the brief's byte-for-byte), run `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-15_ks1035-ornith35b-night`, 2026-09-15 23:5x
# Source read by me (Wednesday): one insert-only paragraph after DEV-PROCESS.md:189 ('merge.'), before the blank that precedes '### 3. Parked work is ARCHIVED, never closed' — the rule 'an APPROVED is live only when no later review from the same reviewer exists at or after it'. Nothing removed; D4 tokens absent before / D5 present after, D6 inside section 2. The ticket's OTHER items are NOT here: dismissing the stale approvals on #813 and #785 (a maintainer's click — Kam's or Peter's), and the pre-merge sweep rule in code (a Claude seat).
# PR NOTES for the Sunday raising seat: one docs PR; the PR body cites KS-1035's measurement (#813 14:52→14:56 on 2026-09-08); leave the ticket open after merge — items 1–3 and 5 remain.
# ⚠ PLACEMENT, corrected by Wednesday after READING after.md: the model over-indented its context lines, D2 re-anchored the insert AFTER the existing blank at :190, and the applied file carried a DOUBLE blank after 'merge.' and NO blank before '### 3.' (the D-gates cannot see spacing). The diff below is the brief's hunk rebuilt with tip-exact context (@@ -187,6 +187,12 @@: 187–189 · `+` blank · the five `+` lines · 190–192); proved with `patch --dry-run` on a copy of the tip file — applies strictly, one blank each side. The six `+` lines are the model's, unchanged.

```diff
--- a/Blockchain/Dev/docs/DEV-PROCESS.md
+++ b/Blockchain/Dev/docs/DEV-PROCESS.md
@@ -187,6 +187,12 @@
 reviews endpoint (`commit_id == head.sha`) — the GitHub **search index cannot see approval staleness** and
 will list a PR as approved when its only approval is many commits back. A reviewer's own PRs are theirs to
 merge.
+
+The same endpoint is blind to a **withdrawn** approval (KS-1035): a reviewer who approves and then, at the
+same commit, comments that the approval is withdrawn still reads as `APPROVED` with `commit_id == head.sha`,
+because the head never moved. An `APPROVED` is live only when **no later review from the same reviewer exists
+at or after it** — a later `COMMENTED` from the approver is read as the withdrawal it says it is, until a
+maintainer dismisses the stale approval. Prose is the only instrument that sees it; read it.
 
 ### 3. Parked work is ARCHIVED, never closed
 
```
