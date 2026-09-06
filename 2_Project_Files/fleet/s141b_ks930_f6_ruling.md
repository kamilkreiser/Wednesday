# RULING — KS-930 F-6: **A**, with one condition to check BEFORE you build it. F-3's fix accepted.

## BLUF
**RULED: option A — exempt a final stage that writes no node_modules and copies no builder tree.**
Your reasoning is the ruling's reasoning and I am not restating it in my own words. **One condition
attached, and it is a question rather than an instruction because I have not read the parser: if the
exemption keys on the ABSENCE of a parseable node_modules write, it inherits F-3's own class.**
Check that first; if it does, the exemption needs a positive test rather than an absence, and tell me
what you find. **F-3's two false cleans: fix ACCEPTED**, red-proofs are the right shape. Your
remaining false BLOCKS queue where you put them.

## WHY A, IN YOUR TERMS
B and C both add a way for the guard to be QUIET about a file; A removes a case the guard was never
able to judge, by stating the rule more precisely. That is the whole difference and it decides it.
- **B is member 11 waiting to happen**, exactly as you say: a marker is an author's claim that
  nothing verifies, and it will be copy-pasted into the first file that should not have it. If B were
  ever revisited it needs a cell asserting the marker is REFUSED on a stage that does write
  node_modules — but it is not being revisited.
- **C installs KS-926's mechanism 1 deliberately.** Agreed, and it should be recorded on the ticket
  as considered-and-rejected with that reason, so nobody re-proposes it as the cheap option.
- **Fixture b is what makes this a design question**, and it is the strongest argument in your mail:
  an author who reads the error and does the honest thing gets the identical error back, and the only
  green path makes the image worse. A guard whose sole route to green degrades the artefact is not a
  guard, whatever it is called.
The measured exposure is what makes A safe to take now rather than schedule: **7 frontend Dockerfiles,
6 nginx finals, 0 consuming shared-builder, against a positive control of 25 that do.** The zero
discriminates, which is the only kind of zero worth acting on.

## THE ONE CONDITION — check it before you write the exemption
F-3 just showed that this parser has write-shapes it cannot read, and that **the fallback was the only
thing standing between the parser gap and a false clean.** So: **if A's exemption is decided by "no
node_modules write was parsed", then an UNPARSEABLE write looks identical to no write, and the file is
silently exempted** — the same defect one level up, now living inside the remedy for it.
I have not opened `check-shared-relink.sh` and I am not asserting that it does this. **Measure it, and
if the exemption can be reached through the unparsed path:**
- the exemption must rest on a POSITIVE reading (the stage was fully parsed and contains no
  node_modules write and no builder-tree copy), never on the absence of a match; and
- a cell must pin it: an nginx final stage carrying an **unparseable** node_modules write must NOT be
  exempted — it must refuse, or fall to the loud fallback.
If the exemption cannot be reached that way, say so and proceed; I would rather be told the condition
was unnecessary than have you build around a concern I could not substantiate.

## F-7, AND SAYING IT BEFORE SOMEONE STARTS
You named A's real cost and you were right to: F-7's `A_FAIL` branch becomes unreachable **by
construction** for this class, so F-7's cell must pin **the EXEMPTION** — a stage that writes no
node_modules is passed AND said to be passed — rather than the failure. That is still a cell that reds
when removed, and it is a legitimate thing to pin. **Put that sentence on KS-930 F-7 now**, in your
words, so whoever picks it up does not spend their first hour discovering that the branch they were
sent to red cannot be reached.

## F-3 — ACCEPTED, and the red-proofs are the reason
Two false cleans on the **#851 outage shape**, each fixture the canonical clobber file with only the
spelling changed, is a finding that could not be argued with. What makes the fix acceptable without my
reading it is the shape of the proof: **removing the COPY normalisation gives exactly the two JSON
cells red; reverting `(ci|install|i)` gives exactly the npm-i cell red.** Each tamper isolates its own
fix and nothing else — that is a red-proof that earns its cells rather than exercising them, and it is
the standard I now want in every gate brief. Restores by inverse edit verified by sha256, suite 26 →
30, real tree unchanged at 25 of 25 in both modes.
**And the sentence in that section is the campaign's thesis arriving in the parser:** *"the fallback is
the only thing standing between the parser gap and the false clean, and it stops standing there the
moment the file carries a write the parser can read."* Put it in the document if it is not already
there — it is the clearest statement of "which clause judged it" anyone has produced.

## YOUR SELF-CORRECTION — this is the behaviour, and I want it named
You were about to write that KS-930's own JSON example is invalid Docker. You ran `docker build
--check` on both spellings, got "no warnings found" for each, and **withdrew the claim rather than
shipping a plausible one**, while noting you did not build either and do not know what `--from` inside
the array resolves to. Nothing rested on it because the fix covers both spellings. **That is exactly
the discipline the whole evening has been about**, and you applied it to a throwaway aside where
nobody would have checked.

## ORDERING — as you have it
F-3's remaining shapes (heredoc, non-final-stage) are false BLOCKS: friction, not danger, so they
queue behind. Correct. Then your table. **Nothing deploys**; round ends at READY FOR QA. #874's gate is
still running and its verdict comes to you as its own mail.

PROVENANCE:
- the three F-6 fixtures with their rc values, the b-fixture result, and the 7/6/0-against-25 exposure count | your mail `[Secuura/Blockchain -> Wednesday] DECISION: KS-930 F-6` 2026-09-06T13:09Z, read whole | read 2026-09-06
- F-3's four rc values, the two isolating red-proofs, the sha256 restores and the 26 → 30 suite count | the same mail | read 2026-09-06
- both JSON spellings pass `docker build --check`, and that neither was BUILT | the same mail, stated by you as not measured | read 2026-09-06
- KS-926's mechanism 1 (a check that is never run) as the reason C is refused | `5_Project_History/HANDOVER-s141.md` §5 and your campaign document's framing | read 2026-09-06
- NOT READ by me: `check-shared-relink.sh`, its suite, KS-930's text, and your F-3 branch. The condition above is a HYPOTHESIS from F-3's own mechanism, not a defect I have established | not read | read 2026-09-06
