From Tuesday (Kam's Datasec coordinator seat), Datasec / HPSM-POC, to SEAT-H1R (pane Datasec/HPSM-POC-H1R). ANSWER-1 to your B542 last line "STOPPED: NEEDS TUESDAY Real preview texts hold an ISO timestamp whose milliseconds are 777 ...". Written 19:02 AEDT.

## RULING: YES. Remove ISO timestamps from the scanned text as well as the ids. The boundary stays DIGIT-ONLY.
Why (from your STATUS, read whole by Tuesday): the ruling forbade widening the BOUNDARY, and you did not. The cause you measured is a second text that holds a digit run BY CONSTRUCTION (`firstAssessmentAt` milliseconds), exactly the reason the ids are removed. Removing it is the same fix-shape as the ids, not a widening. HPSMPOC-325's Done-when ("the scanned text cannot contain a random digit run ... and a 1000 repeat is green") needs it. This extends C2 from "ids" to "ids and ISO timestamps" by this ruling; the round count is unchanged (round 2 of 2).

## Exact shape (binding)
1. `ISO_TIMESTAMP = /\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}\.\d{3}Z/g`, used ONLY in `replace` (as you did for `ENGAGEMENT_ID`), each match replaced by a SPACE, applied together with the id removal inside `leaksExactNumber` (order: ids, then timestamps; say if the order matters and prove it).
2. Nothing else is removed. No other date or time shape is stripped. If any other shape turns up, STOP again with the shape and its count; do not add a third removal on your own.

## Rows to add (each its own title, red-first where it can be)
- (t1) a text whose only number is a timestamp holding `.777Z` is NOT flagged;
- (t2) a 777 directly after a timestamp (`...42.123Z777`) IS flagged (the space replacement must not hide it);
- (t3) a 4321 directly before a timestamp IS flagged;
- (t4) two timestamps in one text, both `.777Z`, NOT flagged (the non-global mutant dies here);
- (t5) the glue row: `77<timestamp>7` NOT read as 777 (the empty-string mutant dies here);
- (t6) a time WITHOUT the ISO frame (`07:59:42.777` with no date, T or Z) IS still flagged: this pins the frame of the removal and says, by a row, what is NOT stripped.

## Mutants to add (your own, as before: anchor 1, sha256 before/after, restore byte-equal)
timestamp removal dropped; non-global; replaced by the empty string; the `Z` made optional; the milliseconds part made optional. Each must be killed by a named row; an equivalent one is proved, not asserted.

## Re-measure (binding, the same instruments as your STATUS)
- Real-text census at N = 20000 per pool (forks and threads): after ids AND timestamps removed, flagged must be 0 of 40000; report OLD and HEAD beside it.
- The 1000-run repeat (`--repeats=999`) of the changed file under BOTH forks and threads: both green. A red in either is a STOP with the failing text's shape.
- Then the rest of your contract as briefed: whole suite as a multiset (names lost 0, added = your rows), lint, typecheck, gitleaks, non-ASCII, name scan, commit, push to the PR branch, CodeQL poll, READY FOR QA line.

## Main moved (FACT, no action)
main moved from `2c94b9b0` to `9fc0a450` after your launch (#200 landed). Do NOT rebase or merge main; push to the PR branch as briefed. The batched gate predicts the merge.

## Records
Add `## TUESDAY RULING (ANSWER-1)` to your STATUS quoting the ruling line and this file's path, and a "For the records seat" row: "HPSMPOC-325: preview texts carry ISO timestamps with digit runs by construction; the exact-number check strips ids AND ISO timestamps before scanning (B542 ANSWER-1)."
