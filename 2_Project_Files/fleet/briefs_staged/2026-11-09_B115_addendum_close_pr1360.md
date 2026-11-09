Seat B 115th

ADDENDUM: ONE extra row, a CLOSE (not a merge). Do it at your next safe point between rows: after a MERGED, or before your first GO arrives. Never between a GO and its MERGED.

What: close PR 1360 UNMERGED. It is Peter's revert of PR 1358 (KS-1380). PR 1358, the build fix, stays merged.

Authority, in order:
1. Kam's card secuura-ks1380-revert-pr1360-still-open-1106 was ruled 'a' on 2026-11-06 21:04:35 ("Let a seat ask Peter on the ticket, facts only").
2. Peter answered on KS-1380 in comment 81cd4067 (2026-11-07): "No, I was reverting on of your tickets I accidentally merged. Than realising my mistake, I backed it out and recreated it.  You can deal with it as you see fit".
3. Seat S 43rd posted the facts-only reply 7e377a37 (02:17:00Z, bytes approved by Wednesday), saying PR 1360 will be closed unmerged.
Closing an unmerged PR is reversible: it can be reopened. It is not a signature class.

How, under the kksecura identity:
1. Read PR 1360 at the API first. It must be OPEN and unmerged at head d0e99f181a4e (S 43rd's read at 02:17Z). If anything differs, STOP and QUESTION.
2. Post ONE PR comment, facts only: "Closed unmerged: the revert is no longer wanted (Peter, KS-1380 comment 81cd4067). PR 1358 stays merged. See KS-1380 comment 7e377a37."
3. Close the PR (state=closed). Do NOT delete its branch.
4. Read the PR back (state closed, merged false, head unchanged) and put both reads in your next mail.
Write nothing on KS-1380 itself.

If your kit has no close command, build the smallest one (one REST PATCH, method and URL printed, dry-run first), declare it, and red-proof it on a made-up PR number that must 404.

Wednesday
