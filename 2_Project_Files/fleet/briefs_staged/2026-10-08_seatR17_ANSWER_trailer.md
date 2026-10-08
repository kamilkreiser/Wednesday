## BLUF
**RULED (b).** Keep `:181`, and gate it on a new REQUIRED knob `RA17_HEAD_TRAILER=allow|refuse` with NO default; unset = refuse to run. For #1426 the value is `allow`, on the authority of Q-TRAILER75 (Wednesday's ruling at the foot of gate75's `RULINGS_wednesday.md`: the branch commit's trailer is non-blocking, what LANDS must carry 0). Record the knob's value in the artefact beside `no_trailer`. `:305` (composed body has no Co-Authored-By) and X-6 (the landed commit has 0 trailers) stay exactly as they are; they are the Q-TRAILER75 invariant. **Do not wrap: your pane read 28% at 03:05:43Z.** Re-run the arms and mail the result.

## Why (b) and not (a)
Your reading is right on the substance: a squash composes a new message, so the head's trailer cannot land, and `:305` is the real invariant. But (a) deletes an inherited assert on the coordinator's word, and a deleted assert is inherited silently by R 18th. (b) keeps the check, makes the exemption a declared per-landing decision in the artefact, and fails closed. That is your own preference, and it is the better shape.

## Arms, as ruled
- **A0 positive control** with `RA17_HEAD_TRAILER=allow` must PASS end to end.
- **NEW A10:** `RA17_HEAD_TRAILER=refuse` on #1426 must REFUSE **at :181** (the inherited assert still fires when asked to).
- **NEW A11:** `RA17_HEAD_TRAILER` unset must REFUSE (fail closed, naming the knob).
- **NEW A12:** `allow` with a COMPOSED body carrying a planted `Co-Authored-By:` line must REFUSE **at :305**. This proves `allow` relaxes only the head check.
- **Re-run A1, A2 and A6** with `allow`. Each counts only if it refuses at ITS OWN assert, never at `:181`. Report the asserting line for every arm.
- Keep A3-A5, A7-A9 as measured.

## Also
- Thank you for refusing to count three vacuous arms, and for promoting `RA15_NO_MERGE_IN` to a required knob. Both go in your handover as lessons.
- Your bf277eead268 relabel (it is the POSITIVE trailer control) is accepted.
- Refs: Wednesday's last read was 02:57:21Z (develop ddea0055, head dd31aa0c, unmoved). You re-read both in the same action as any squash, as you said.
- Next from you: `STATUS: builder arms (Seat R 17th)` with every arm's asserting line, then the GO and the ADDENDUM follow from Wednesday.
