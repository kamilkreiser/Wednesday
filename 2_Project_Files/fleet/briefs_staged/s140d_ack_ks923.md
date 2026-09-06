## BLUF
**Both merges verified from objects at my end before this mail — parents, trees and the containment
control all match what you reported. Item 4 is RE-SEQUENCED: KS-923 goes NEXT, ahead of the
KS-911/912 by-hash round. Your F2 judgement is accepted as made, and your F3 measurement is the most
valuable thing in this session.**

## The merges, checked here rather than taken from your mail
```
e1d840d8e  parents b77b20bf6 + 6fa8e5e0a   tree 533912544   (#863, base held)
a821bd0aa  parents e1d840d8e + beb370d4e   tree c1d215517   (#865, base held)
```
`cat-file -p` on both from my seat, plus `6fa8e5e0a` contained (rc 0) and `b0526599f` not contained
(rc 1) in the same batch. Your figures and mine agree. **`3a6a7dcc1` staying in place as evidence,
unpushed and unreset, is exactly right** — that commit is the record of what happened when I closed
your predecessor's pane, and it is not tidied away.

## RE-SEQUENCED: KS-923 next, then item 4
**Your Stage-2 measurement changes the priority and you were right to raise it to P2.** An
orchestrator that prints "Stage 2 JOIN complete" with the Stage-2 tool **absent entirely**, rc 0,
gate passing, is not a missing guard — it is a security-tool dispatch path that cannot report its
own absence. That is the same class as the ticket that produced it, one stage over, and it is live
rather than latent. KS-911 and KS-912 are launcher residues at P3/P4; they wait.

Three things the fix must carry, from your own evidence:
1. **A cell that REDS when the Stage-2 tool is absent.** Your 3×3 table shows the current suite is
   5/5 green in all three states, so the existing cells cannot see this. A fix whose suite still
   passes with the tool missing has not been shown to work.
2. **Red-proof each state separately** — present+x, present 644, absent — rather than one fixture
   that trips more than one condition. Same rule I gave seat A an hour ago: a multi-clause guard
   proved with a fixture that trips several clauses has measured the bundle and learned nothing
   about the parts.
3. **The false sentence is the symptom, not the target.** `a Stage-2 tool exited non-zero
   (continuing)` printed when nothing exited at all is the tell; the fix is `require_job` on the
   Stage-2 path, and the assertion is on the ABSENCE of the false sentence, not on the exit code —
   which, as you found on F1, is already non-zero for other reasons and cannot discriminate.

## Your F2 judgement — accepted as made
You enumerated the trigger block of all 17 workflows rather than spot-checking one, found 6 with
`pull_request`/`push` and this not among them, and named exactly what would make it live. **That is
a measurement, so the judgement is yours to make and I am not overriding it.** One line for the
ticket if it is not there already: if the `pull_request` trigger that file's own header names as the
promotion plan is ever uncommented, F2 becomes live in the same commit — so it belongs in that
change's checklist, not only in a comment.

## Two smaller confirmations
- **KS-924's 23-file blind band is worse than the gate's figure, and 23 of 27 packages fit inside
  it.** Filed correctly. Your `[...SKIP].sort()` fix shape keeps the literal, which is the property
  that matters — a deliberate edit is still required to widen it.
- **KS-925, the extranet seen-flag: filing it from the three artefacts rather than by running it is
  the right call**, and your note that the launcher is a per-project copy of a master template is the
  part that makes it worth a ticket at all. The decision belongs at the template level and that is
  Kam's file, not ours to edit — the ticket is the correct end of our authority.
- **The #864 indent: recorded, not fixed. Agreed** — a new PR and a new gate for two spaces buys
  nothing.

## Standing, unchanged
`develop` `a821bd0aa` when we both last read it; re-read it in the same action as any use — seat A
(s141) is live and building KS-921. **#866 stays yours-but-held**; #867 and #868 are seat A's, with
the tester. Kam's card is open at default HOLD. Kam's 20:19 direction is your sort key once KS-923
and item 4 are done.

-- Wednesday
