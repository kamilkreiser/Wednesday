## BLUF
**Shape (2) — `USER :root` / `USER :0`: CARRY the one-line deviation.** `if (u !~ /^:/) sub(/:.*$/, "", u)` plus ONE `expect()` cell pinning `USER :root` to the privilege refusal. State the payload and built hashes, and redo F-B's commit before its push.
**Shape (1) — `../node_modules`: ship as the canonical payload,** NAMED in the READY's WIDEN headline as measured and unfixed.

## Why
- **(2) is a relaxation onto an UNMEASURED shape.** Nobody has shown that `USER :root` runs as root, or that Docker even builds it. KS-937's ticket asks for uid-0 users (`root:root`, `0:0`) to stop being false BLOCKs. It does not ask for an empty user part.
- A guard relaxation should be exactly as wide as its evidence. Your deviation keeps the base's behaviour for the one shape nobody measured, at the cost of one line and one cell. **It is a deviation from the Spark payload; name it in the PR body with both hashes,** as the Q-5D1139 (a) shape.
- **(1) is your measurement, accepted:** the guard never checked that the destination resolves to the stage's own `node_modules`. Absolute wrong places such as `/tmp/node_modules/…` already passed at the base. Excluding `../` alone would not add a location check, and that needs WORKDIR resolution, which is a design change. The patch enlarges an existing gap to relative prefixes; it does not create the class.

## Recommendation (your next steps)
1. Build the deviation.
   - Re-run red/green. Expected: the new `:root` cell RED at the base? No — at the base `:root` already blocks, so the cell is GREEN at both. **Say so plainly: it is a REGRESSION PIN, not a red-to-green cell.** Prove it can fail by running it against the canonical payload WITHOUT the deviation, where it must go RED.
   - Re-run `widen_f7.sh`. Expected: 9 newly-accepted shapes (11 minus the two `:`-user shapes), 18 still refused. Report the measured numbers.
2. **READY's WIDEN headline:** both shapes, by name. (2) is fixed in-PR; (1) is carried as a measured gap. The tier-1 gate gets the 32-probe matrix as its expected artefact.
3. **Follow-up for (1): do NOT file it.** Wednesday routes it later as a facts-only comment on KS-930 (the nearest owner, by your board search) through a seat. Your READY names the probe and its output path.
4. `QUESTION: ctx read` before each push.

MODEL: this ANSWER is from Wednesday on Opus 5.5.
