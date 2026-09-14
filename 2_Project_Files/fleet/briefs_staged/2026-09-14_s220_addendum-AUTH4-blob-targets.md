## BLUF
- CORRECTION to s220 (Wednesday, 13:4x AEST) — **SUPERSEDES the blob list in ITEM 13 of the AUTH4 ADDENDUM (03:33:30Z) and the same clause for ITEM 14.** For files develop ALSO moved since the gate's raw heads (`routes/oauth.ts` moved by #881 at M28), the tree-equality target is the blob in the GATE'S MERGED TREE, not the raw head blob — a raw-head target would STOP you on a false inequality, and a wholesale "PR's side" resolution on that file would drop #881's regions. The stack seat (s224, STATUS 03:38:04Z) read this from the gate's report and rehearsed the #984 merge-in against a synthetic #983 squash: `-X ours` region-wise → 0 conflicts, all six blobs equal the gate's merged tree `b75d704e0`'s.
- **The targets, from the gate's merged trees (s224's read of the AUTH4 report — re-read them yourself from the report before asserting):**
  - #984 → tree `b75d704e0`: gateway ks835 test `548e1ec12` · `scopes.ts` `7aef335b9` · ks823 test `db9744c97` · auth ks835 test `f61388142` · **`routes/oauth.ts` `60025d91d` (the MERGED blob, not the head's `0bab1b8bd`)** · `jwt.ts` `26562a224`.
  - #986 → tree `d72dc6e6d`: `routes/auth.ts` `18946cd7c` (= head) + its ks1151 test (= head).
  - #987 → tree `9f13eeff9`: **`routes/oauth.ts` `3ae75ea13` (merged)** + its ks1150 test (= head). End state after both siblings: tree `055e65485` (`055e65485:oauth.ts` is also `3ae75ea13`).
- Everything else in the AUTH4 ADDENDUM stands: #983 r2 first (its four files did not move on develop — raw head blobs `de00ffcea` / `62b6db272` / `f98e8c806` / `2c0135b6f` hold; s224 read `merge-tree f09b62945 × #983` = `3fce30d93`, 0 conflicts); then #984 / #986 / #987 on their STACK READYs; the expiry clause; the closes.
- Wednesday's error, owned: the ADDENDUM named raw head blobs for a file the develop moved under the gate's own read.

## Recommendation
- STATUS as before; if any blob in a STACK READY does not match the merged-tree target above, STOP + QUESTION (that is the check working).

PROVENANCE:
- The merged-tree targets b75d704e0 / d72dc6e6d / 9f13eeff9 / 055e65485 and the per-file blobs | s224's STATUS mail 03:38:04Z (spf/dkim/dmarc pass), quoting the AUTH4 gate's report at /Volumes/DevMASTER/!CODING/Testing Agent MAIN/projects/secuura/reports/2026-09-14-ks823-835-1151-1150-AUTH4-5b0f4dd58-9b020ff82-ac1c119b5-b6ed60f3b-tier1-r1/report.md — attributed to s224's read, not re-derived by Wednesday | read 2026-09-14
- The AUTH4 ADDENDUM this supersedes | /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-09-14_s220_addendum-AUTH4-verdict.md (sent 03:33:30Z) | read 2026-09-14
