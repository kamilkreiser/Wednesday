# READY — KS-1036 item 3 ONLY (DEV-PROCESS.md: the review-stream counts are a 2026-09-03 snapshot and have decayed) — Ornith ornith:35b (Q4_K_M) PASS 8/8 on the ONE REBRIEF (r2, doc_1036r2.json; run /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/runs/2026-09-16_ks1036-ornith35b-night2). Held by Wednesday at 22:17 AEST.
# Source read by me (Wednesday), the model's diff and not the verdict: ONE insert-only hunk, six '+' lines byte-identical to the brief's fence, appended straight after DEV-PROCESS.md:227 'their stream.' (the paragraph's last line), before the blank :228 and '## Review capacity'. No line removed, no blank added. In rendered markdown the bold sentence CONTINUES that paragraph (the brief's intent — r1 landed a paragraph too low).
# PR NOTES for the raising seat: ⚠ the counts (71 active · 40 under the four parents · 2 elsewhere · 29 none) were measured by a subagent ~21:3x; board_count.sh read KS active = 74 at 21:4x the same evening — RE-COUNT at raise time and update the four numbers + the date in the + lines before the PR (the sentence tells readers to count at the time; the PR must obey it). One docs PR; leave KS-1036 open after merge unless every item is done.

```diff
--- a/Blockchain/Dev/docs/DEV-PROCESS.md
+++ b/Blockchain/Dev/docs/DEV-PROCESS.md
@@ -224,4 +224,10 @@ their stream. A wrap that files tickets names
 
 **Every new K-side ticket that reaches Todo is parented into one of the four** (or into a new stream, proposed first). A wrap that files tickets names
 their stream.
+**Measured 2026-09-16 (KS-1036): the counts above are the 2026-09-03 snapshot and have decayed.**
+Of the 71 KS tickets in a started or unstarted state, 40 sit directly under one of the four
+parents (KS-485 9, KS-770 10, KS-771 9, KS-772 12), 2 under another parent and 29 under none.
+Do not quote 97 or "nothing left over" as current. When the number matters, count it at the time:
+the direct children of KS-485, KS-770, KS-771 and KS-772 that are started or unstarted, against
+every started or unstarted ticket on team KS.
 
 ## Review capacity — the constraint this flow creates
```
