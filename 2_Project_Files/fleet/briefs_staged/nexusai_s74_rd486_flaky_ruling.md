# BLUF — **N=5, YOUR CRITERION ADOPTED WITH ONE ADDITION. DO NOT HOLD rd486. AND MY ACCEPTANCE CRITERION WAS UNSOUND — THAT IS MY DEFECT, NOT YOURS.**

1. **N = 5 each side.** Your criterion is adopted: compare the SET of cells that ever fail; require it
   unchanged and explained. **Plus one addition in section 2 below, for the case your own numbers are
   walking into.**
2. **Do NOT hold rd486.** Land it. The instability is pre-existing on `main` and RD-574 did not cause
   it — **holding the fix for a defect it did not introduce would block the merge blocker for the
   resubmission, to wait on a race nobody has been asked to fix.**
3. **File the flakiness ticket once your extra runs land**, with a measured rate, as you planned.

# 🔴 MY CRITERION WAS UNSOUND AND YOU FOUND IT BY OBEYING IT

**"Per-suite inertness, a single before/after pair, empty per-cell diff" assumes the baseline is
DETERMINISTIC. I never checked that assumption for any of the five suites, and I wrote it into two
briefs as an acceptance condition.** Your sentence is the exact statement of the defect and I am
adopting it verbatim:

> *If either side can fail on its own, an empty diff is luck and a non-empty diff is not necessarily
> a finding.*

**You found it because the criterion made you STOP instead of re-running until green.** That is the
only reason this surfaced before the gate. Had you retried once, you would have got 45/45 and
reported inertness in good faith.

# 2. THE ADDITION — WHAT TO DO WHEN THE SET *SHRINKS*

Your numbers are heading somewhere your criterion does not yet cover. Counting what you have:
**BASELINE 2 pass / 2 fail of 4; MODIFIED 4 pass / 1 fail of 5.** If the next runs continue that way,
the failing-cell SET on the modified side will be **empty** while baseline's is `{a (SAVED)}`.

**Under your criterion as written, that is a CHANGED set — and therefore a finding.** It is also a
change in the *flattering* direction, which is exactly when a criterion gets quietly waived.

🔴 **RULING: a set that SHRINKS is neither a pass nor a failure. It is an UNEXPLAINED CHANGE, and it
lands only with the words "unexplained" attached.** Concretely, rd486 may land with a shrunk set if
and only if your READY carries:
- **the counts, both sides, every run** — not a summary;
- **the hypothesis NAMED AS A HYPOTHESIS** — `localhost` resolving to both `::1` and `127.0.0.1`
  with the stand-in on both, so undici can race them, while your stub resolver answers exactly one
  address and removes the race;
- **the sentence that you are NOT claiming your change stabilises it**;
- **the ticket number** for the flakiness.

**Why I am not letting a green-er result pass quietly:** *"my change made a flaky test stop
failing"* and *"my change made a test stop being able to fail"* produce identical numbers. **Only the
mechanism tells them apart, and you have a mechanism but not a proof.** This is the third time today
this floor has hit the same shape — **a suite that stays green while covering less** — and it is the
shape that survives every check we have.

# 3. YOUR REFUSAL TO CLAIM STABILISATION IS THE BEST THING IN THE MAIL

You had a plausible mechanism, a 9-run lean, and every incentive to write *"and my change fixes it."*
**You wrote "that is a hypothesis with 9 runs behind it" instead.** Keep exactly that standard. **Four
more runs each side is the right response to a lean, not a better-argued paragraph.**

# 4. THE TWO CORRECTIONS YOU VOLUNTEERED — BOTH ACCEPTED, AND ONE IS MINE TO CARRY

**(1) Your five-suite baseline's rd486 component is one draw from an unstable suite.** Accepted, and
**you were right to correct it yourself rather than let the gate find it.** I had accepted 105/105
and **I passed it upward as an independently confirmed measurement.** I am correcting that on my side
in the same terms you used: **the four-suite 105/105 stands as a measurement of one draw; its rd486
component is not a repeatable constant.**

**(2) The gate's §5(c) control carries the same caveat.** Agreed — *"with the policy neutralised:
105/105 PASS"* is one run of the same suite. **And your own judgement on its weight is correct and I
want it recorded: this does NOT overturn the verdict. The 27-red measurement is a far larger signal
than one intermittent cell**, and rd464's and rd486's test files being byte-identical between
`60c76d7` and `f4264e5` is untouched by any of this. **The caveat is on the phrase "105/105", not on
the finding.**

# 5. RD-590 — FILED CORRECTLY, AND IT IS THE SUBTLEST THING ANYONE HAS FOUND TODAY

**Four `d-nomatch` cells lose their discriminating power once the stored endpoint becomes a NAME:**
each isolates one variable today (path, scheme, port, host-alias); afterwards each also differs in
HOST, so they pass **for a weaker reason** and the `dAlias` label becomes false.

🔴 **"They stay GREEN, which is why inertness cannot see it"** — that is the sentence. **My acceptance
criterion is blind to this entire class by construction**, because it compares outcomes and this
changes the REASON behind an unchanged outcome. **A separate ticket is right; not fixing it inside
RD-574 is right** (outside §6, and hard stop 1 covers two of them); **not touching them is right.**

**Put a one-line pointer to RD-590 in your READY** even though it is out of scope — the next reader of
those four cells needs to find it, and a ticket nobody is pointed at is a ticket nobody reads.

# 6. STATE — ACKNOWLEDGED

`rd464` committed (`8f7264d`, 30/30 both sides, empty diff, **seam proven load-bearing in both
directions** — that last part is what makes it a real pair rather than a matching pair of nothings).
Preload committed (`5f3341e`, byte-identical). rd486 edited, uncommitted, correctly held pending this.
**rd545/rd523 next, all 31, per the (b) ruling.**

**rd464 showed no instability in any run — so this is an rd486 finding, not a five-suite finding.**
Apply N=5 to rd486. **The other suites keep the single pair unless you see the same shape**, and if
you do, the same rule applies without asking me.

PROVENANCE:
- rd486 fails intermittently at BASELINE on main 60c76d7 with the RD-574 change reverted — 2 pass 2 fail of 4 baseline, 4 pass 1 fail of 5 modified, alternating on one machine with git checkout between runs | S74's measurement, its FINDING mail 2026-09-20T23:40:07Z | read 2026-09-21 by Tuesday
- the failing cell is a SAVED, expecting zero stored connections and requests and receiving two of each, the shape of one boot warm-up probe cycle inside a 1500 ms window | the same measurement | read 2026-09-21 by Tuesday
- localhost resolves to both colon-colon-1 and 127.0.0.1 and the stand-in listens on both, which is a NAMED HYPOTHESIS for the race and not a proven mechanism | S74's own framing, explicitly labelled a hypothesis with 9 runs behind it | read 2026-09-21 by Tuesday
- rd464 showed 30 of 30 on both sides with no instability in any run | S74's measurement, same mail | read 2026-09-21 by Tuesday
- my per-suite single-pair inertness criterion assumed a deterministic baseline and I never checked that assumption | my own RD-574 brief and the RD-516 fix-round brief, re-read this action | read 2026-09-21 by Tuesday

RULED BY KAM, NOT YET IN AN ARTEFACT
- none for this item.

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-21 09:42
