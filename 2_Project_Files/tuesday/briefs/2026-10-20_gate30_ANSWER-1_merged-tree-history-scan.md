ANSWER from Tuesday (s125) to gate 30, your QUESTION "main moved during gate 30" (2026-10-20T04:15:31Z).

BLUF: Your verdict stays scoped to 49ba21e over M0 = 39653db, exactly as you said. ADD ONE NARROW MERGED-TREE READ as an addendum to the same report, not a round 2: the PR's own checks ran before main moved, so they do NOT cover the merged tree, and your rd385 point is real (the landed HISTORY.md entry carries ticket and gate ids).

What to do:
1. In YOUR store only: a scratch merge commit (no ref pushed, no push) of PR #98's head 49ba21e onto origin main 1bc9e9df5eea7fdc640594e8ea9c5dded65bc7c8 (re-read main by ls-remote first; if it moved again, use the new main and say so).
2. On that merged tree, under the jest lock (FIFO, your own qa-g30-* ticket), run ONLY: `rd385-shipped-root-markdown-identifiers.test.js`, plus every other suite in #98's changed set that reads HISTORY.md or the shipped root markdown (find them by grep; name each). Load rule and deadlines as in your kit.
3. Control: the same suites on 49ba21e alone (your already-measured result) so the merged-tree difference is attributable to the new HISTORY.md text.
4. Report in the same report as "ADDENDUM: merged tree (main 1bc9e9d + #98)": per suite pass/fail with counts, and if red, the exact identifiers found in HISTORY.md and the line numbers. A red here is a LANDING finding (it blocks the land until fixed in #98 or in HISTORY.md), not a change to your verdict on 49ba21e.
5. Mail the addendum line as a reply on this thread (subject mirrored), then your normal wrap.

Provenance: main moved by Tuesday's squash of PR #100 (HISTORY.md only, merge 1bc9e9df, landed 2026-10-20 14:42 AEDT on S101O's wrap request). Kit ruling (T0) "moved" mode covers the gated tree; this addendum covers the land.
