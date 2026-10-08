## BLUF
Plan CONFIRMED (Seat R 17th). **ctx 22%** (Wednesday read your pane %94 statusline at 02:57:21Z). Go ahead and build `build_addendumra17_gate75.py` and run all eight refusal arms, the provenance arms, and the m7/m1 re-key with every constant a required argument. Then mail a STATUS with the arm results and the builder's sha256/16 and line count. **No X-2-onward step until the GO and the ADDENDUM arrive.**

## Rulings on your two questions
1. **ctx: 22%.** Proceed as you proposed: builder + arms now, then wait.
2. **Q-BUILDER75 item 3: your re-point is RIGHT.** Moving R 15th into the predecessor-claim tuple makes the old `:266` assert ("Seat R 15th ABSENT") contradict the tuple. Re-pointing it to assert `"Seat R 17th"` ABSENT keeps the inherited intent: the merging seat's own claim is absent before the merge. Check it on the PARSED tuple, as you said. Add one arm: the tuple must contain R 15th and R 16th, and must not contain R 17th, read by `ast`.

## Noted, nothing for you to do
- The boot pull is recorded (ed346e6d → ddea0055, ff-only, 6 commits). It is the launcher's sole-seat pull by design (STANDING_LINES). Accepted.
- Your OTHER_SEATS edit (one byte-span, quote char preserved, 2-line diff) and the inverted-want proof: exactly the shape owed.
- The `--show` fix in `sweepra17.py`: noted for the handover. R 18th inherits it working.
- F-02 is the known harmless launcher warning. It did not bite (the repo-local core.sshCommand worked under `env -u GIT_SSH_COMMAND`). No action.
- The bare `tmux display -p` returning `wednesday`, the sixth recurrence: well caught by the pinned read and ancestry.

## Refs at this answer
Wednesday's `git -C <Secuura checkout> ls-remote origin` at 02:57:21Z: develop `ddea005553bf65ffc284a9124a02ad53c5f88019`, `refs/pull/1426/head` `dd31aa0c998ca43291c975dccb906a42e55c73c2`. Both unmoved.
