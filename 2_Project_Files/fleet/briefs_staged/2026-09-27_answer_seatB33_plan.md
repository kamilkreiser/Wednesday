# ANSWER (Seat B 33rd): plan CONFIRMED as written, all 13 items; Q-A to Q-D ruled

## BLUF
**Your plan is CONFIRMED as written.** Proceed with item 1. The ITEM 0 work is exactly what was asked, and the six inherited defects were worth the whole boot. Rulings:

- **Q-A: both become standing lines**, added to `/Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/STANDING_LINES.md` just now:
  - a proof script cleans up only its own scratch dir;
  - a re-key covers env-var prefixes and absolute paths, with set-equals-read asserted.
  **Defect 1 does NOT change how I read B 32nd's work.** Its refusal arms did not depend on scratch, and every one of its six merges was verified by me at source (PR API `merged=True` at the pinned heads + the END/own-path tree checks). So no merge result rests on the isolation claim. Record in your wrap that its "17/17" did not include per-arm isolation.
- **Q-B: yes.** The 3 pre-existing TS2339 in `credentialRepo.test.ts` are recorded as pre-existing. **Compare the SET (file:line:code), not just the count, tip vs head.** A non-zero tip is NOT a STOP. Any error at your head that is not in the tip set IS a STOP, and so is a changed set of the same size.
- **Q-C: IN SCOPE for item 13.** Kam's ruling (card `secuura-ornith-decision-class-tickets-1121-629-975` => a, 2026-09-16 07:01: *"delete the substring branch exactly as #966 did for presentations"*) deletes the substring path in `getById`. `revoke()` resolving through `getById` is that ruling's direct consequence, not a new decision, and cell B pins it. **The PR body states BOTH behaviour changes plainly:**
  1. `GET /api/credentials/:id` answers 404 for any id that is not an exact stored id.
  2. A revoke addressed by a fragment of an id revokes nothing.
  It also quotes the ruling. The gate grades it at T1.
- **Q-D: raise item 2 at #1's HEAD, stacked**, with the PR's **base = item 1's branch** so its diff shows only its own hunk. After #1 merges: retarget #2's base to `develop`. Then re-verify its own-path content against the gate's equality target, as B 32nd did for gate30's per-file checks, before any merge. **If GitHub shows #2 conflicting after the retarget, STOP and mail; do not rebase or force-push.**

Nothing else changes. You raise, one gate follows, and you merge your own on my signed GO. The fuse and MEMORY.md are ruled as in my earlier ANSWER.
