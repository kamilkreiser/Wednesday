# For the records (MPSCALC-429), gate B1902

## The ticket now
MPSCALC-429 reads Backlog, 0 comments, 0 links, label `records-pass-1120d`, updated 2026-11-20 20:18 (unchanged since the kit) at this gate's own Jira GET (2026-11-22 evening; control MPSCALC-361 reads Done). No pull request names it. A merge does not move a ticket; the records pass moves it and comments after the pull request lands.

## Sentence for the comment (Tuesday's choice as coordinator, not the product owner's; the ticket says "no product byte changes and no word of the product owner is needed")
Two cells, G15 (an explicit save 5 seconds into a gap makes the next autosave wait until the gap after that save) and G16 (a second save request restarts the running gap timer), added at the end of the gap describe in `web/src/screens/QuoteScreen.autosave.test.tsx`; cells 30 -> 32, whole web run 1734 -> 1736, 0 failed; each red under the one-line change that removes its behaviour and green on current code; one file, no product byte.

## Two readings the comment should carry (findings of this gate, both Minor)
1. The ticket's sentence "a change that does not clear the running gap timer on re-arm is caught only by a cell that counts timers" does not hold at main: the existing cell G5 (it counts timers after leaving the screen) is already red under that change at base (measured: 1 failed, G5; 30 cells). So that change was never "every owned test green"; only the first change (an explicit save that arms no gap) leaves all 30 cells green. The new cells are red under both.
2. Both new cells are red under the first change, and G15, G16 and G5 are red under the second. This is named, not a defect: G15 reads the request count (a no-clear build lets the old timer end at T+GAP and send the trailing save early); G16 reads the timer count.

## Ticket candidate (not blocking, not this change)
The source comment at `web/src/screens/QuoteScreen.tsx:268` says the gap is armed synchronously BEFORE the request, so a refused or slow request starts the gap too. No cell pins that: moving `armGap()` to after the awaited request leaves all 32 cells of the file green (measured in this gate; the mocked request settles at once). A cell with a request that stays pending (or is refused) while the clock advances would pin it. Out of the lane of MPSCALC-429.

## Measured in the gate
Head tarball of 5b3a5ee0 and base tarball of ec281cfb: the head file equals the base file plus the frozen block, by program; the only differing path of the two trees is the test file; file alone 32 passed; whole run 149 files, 1736 passed (base 149 files, 1734 passed); `eslint .` rc 0; `tsc -b` rc 0; `red429.py` 6 labels DIFF 0. Nothing deployed.
