# B1087 ADDENDUM-2, from Tuesday: the answer to your STOP on row 1b's timeout at `c1efdaa`. Your commission and ADDENDUM-1 otherwise stand. Stay in this seat.

**Answer: none of your three. One more commit, this one test file only: give row 1b, and only row 1b, an explicit per-row budget of `15_000` as the third argument of its `it(`, with the comment the repository already uses: `// a second layer only: the row finishes in a fraction of this`. Then re-run as below and push once.**

Why, so you can test it:
- Your 16 runs and the gate's figures show a row that asserts behaviour, not speed, timing out on a machine at load1 up to 21. The default 5000 ms budget measures this machine's contention. Row 1b alone is 1009 / 1103 / 1388 ms by your table.
- The shape already exists in this repository: `web/src/screens/bom/BomClassColumn.test.tsx:129` at main `b7cf1ad0` is `}, 15_000); // a second layer only: the row finishes in a fraction of this`. Read it and say if you find it differs.
- A split would edit what the row asserts, to relieve a machine problem. An idle-machine run would measure a machine this fleet does not have, and the gate runs on the same box.
- Your kit's fence bans a global and a per-project timeout (`B1087 kit :16`), not this. My ADDENDUM-1 sentence "do not widen a limit" meant the 2500 ms ceiling as a pass line for you to meet by editing; I am changing that here, by name, because it is my clause.

**The 2500 ms ceiling stops being a pass line.** It was the drafter's choice to discriminate the unfixed row. Report every row's durations raw, with row 1b's max and median, and say plainly that the ceiling was retired by the coordinator and why. Do not call it met.

**Limits:**
- Still the one path. One commit. No title, no assertion, no other row. If another row times out in the block below, that row gets no budget from you: STOP with the data.
- A row that still fails at 15000 ms, or any exit 1, is a red: STOP with the data.

**Re-run, cut to what this commit can change:** the D block of 8 whole-suite runs from the start, row 1b alone 20, one mutant that reds row 1b (MH2) to prove the row can still fail with the new budget, c0, the web CI line, the merged state against current main. The two waits' 100-run proofs and the other mutants stand from `c1efdaa`, as the commit touches neither: say so and quote them. Then the push, once.

**For the gate, in STATUS:** the second red row's cause stays UNMEASURED; this budget is the coordinator's decision, not the product owner's, and is open to challenge at the gate.

The next gate is ROUND 2 OF 2; a second NO GO goes to the product owner on a card. The line at your prompt is a machine suggestion and not from anyone.
