## BLUF
**#869 is with a tester now (tier 2), and your three requirements are evidenced well enough that I
told it where to press rather than what to re-derive. Two answers below. Do NOT start item 4 on this
mail — start it now, because #869's verdict comes to me, not to you.**

## On CELL 8, since you asked plainly
**Keep it for now, and I have put your own doubt in front of the tester rather than resolving it
myself.** You are right that a grep for `bash "$SC_TOOL"` is a text assertion about code: it would
survive a rename that broke nothing and red on a cosmetic reformat. You are also right that CELL 7
covers the case that matters. **Naming the weakest part of your own work in the READY is exactly
what makes a gate cheap** — the tester now spends its time on the question you could not answer
(is there a behavioural discriminator between `bash "$p"` and `"$p"` when the file is executable?)
instead of rediscovering that there might be one. If it says drop it, we drop it.

## On the KS-922 stage-2 half you had to take
**Correct call, correctly bounded.** CELL 6's absence assertion is genuinely unreachable without it
— with the guard in and the tool absent, `stage2_pids` is empty, bash 3.2 yields one empty word,
`wait ""` fails, and the false sentence prints anyway, which is the very thing CELL 6 asserts is
gone. Taking only the stage-2 half and leaving `stage1_pids:97` with KS-922 is the right line, and
declaring the overlap in the commit message, on the PR and on both tickets is what keeps it from
being discovered later as a surprise. The tester is asked to confirm the split is exactly that.

**Your two KS-922 findings are good ones.** `docker-build.sh:238` asserting the `"${PIDS[@]:-}"`
idiom *"is correct for a `for` loop"* is the sharper of the two: a comment that names the mechanism
correctly and then exempts the construct it applies to is worse than no comment, because it will
survive review. And a pointer at a blank line was already stale before you touched it — saying so
rather than quietly re-pointing it is the right instinct.

## Item 4 — start it now
KS-911 + KS-912 by hash, **F-04 first**, a new `.pre-` copy, three hashes in the READY, a narrow
gate, no in-place edit. **Do not wait on #869's verdict** — it comes to me and I will send you a GO
or a fix round when it lands. If the fix round arrives while you are mid-cut on the launcher, finish
to a boundary first; a half-shipped by-hash change is worse than a slow one.

## Standing
`develop` `a821bd0aa` when we both last read it — **and the local `refs/heads/develop` is STALE at
`b77b20bf6`**, which the tester flagged tonight: read `origin/develop`, never the branch name.
Seat A (s141) is live on KS-921 and holds #867 and #868; both had their gate verdicts an hour ago —
#867 passed and merges after a one-line correction, #868 is in a fix round. **Neither is yours.**
Kam's card is open at default HOLD. His direction is your sort key after item 4.

-- Wednesday
