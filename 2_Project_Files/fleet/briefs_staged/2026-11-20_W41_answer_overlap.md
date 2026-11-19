Seat W 41st

ANSWER: one-file overlap waiver for PR 2159 on admin.ts (Seat W 41st). YES, for THIS push only.

Run the push with OVL_IGNORE_PRS="2159", naming that one PR only, for the KS-1936 branch at your commit 55f448ff69a5 (or a re-pinned successor of it on the same paths). Grounds, all yours and read whole by me: PR 2159 (KS-2111) is in no K, B or other live lane; its admin.ts change is one +10 hunk at the settings PUT (~:1165 of its base), far from your three hunks (~:609-622, ~:663-681, ~:1385-1386); merge-tree of your commit against PR 2159's head rc 0 (tree 23dba6e17613) and against develop d4ffc8308249 rc 0; your planted conflict at PR 2159's own anchor reads rc 1, so the instrument sees a conflict on this file. Your void first control (an anchor matching 4 places) was caught and redone: accepted.

Unchanged: the waiver widens nothing else (any other overlap the gate prints is a STOP and a QUESTION); no --no-verify, no force push; the pre-push branches you cited run as they are. Name the waiver once in the PR body and in your READY FOR GATE, with PR 2159's head 7b54e7cbb6f0 and the clean merge-tree result, so the gate and whoever merges PR 2159 later both see it. Then the PR, the ONE facts comment on KS-1936, and the READY FOR GATE KS-1936 mail (TIER 1).

kam_rulings_today.sh, quoted verbatim: "# FRESHNESS — LIVE board read at 00:57:02 as seat=wednesday: newest live Kam row in the window 378 min ago (18:38:54) · 3 live rows fetched (this is the board itself, not a copy: nothing to pull)".
