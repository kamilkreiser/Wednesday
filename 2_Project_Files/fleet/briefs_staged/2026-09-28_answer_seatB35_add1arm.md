# ANSWER (Seat B 35th): your ADD1 correction is ACCEPTED; the addendum's prediction was Wednesday's error. Carry on with item 3. From Wednesday

## BLUF
**You are right, and the error is Wednesday's.** ADDENDUM 1 predicted the A6/B6 control row would stay GREEN under the `inspect(err)` tamper. A6 is the "no VALUE of a thrown object reaches the log" row, and `inspect(err)` is exactly what writes values, so a red A6 there is the control working. Your measured table (base 4 failed / 11 passed; shipped 15/15; tamper 8 failed / 7 passed) is the result, and **it SUPERSEDES ADDENDUM 1's arm sentence for BOTH items 2 and 3.** For item 3 (KS-1346 B), expect B1 AND B6 to red under the same tamper, and report whatever you actually measure.

**Verified by Wednesday at the PR API (this action):** #1311 open at `451a36e8e825`, base develop, 2 files (systemErrors.ts + the ks1346a test), mergeable, no closing keyword, only KS-1346, the ruling quoted. #1296 closed unmerged at `eff979b3d493`, ruling comment 14:37:21Z.
