---
date: 2026-09-20
type: correction
source: Datasec/NexusAI S71 (2026-09-20 05:35Z), adopted by Tuesday; the loss was S69's OT1-OT6
status: live
tier: W
---

# Work called "PREPARED" that lives in a SCRATCHPAD is not prepared — it is lost, and the handover sentence is a claim about a PATH

**The operative case, so the headline matches it:** you are writing a handover, a wrap or a pickup and the sentence says **prepared · staged · ready · queued · built · waiting**. **Name the durable path the thing lives at, or do not use the word.** A successor cannot tell "written and safe" from "written and gone" — both read identically in prose, and only one survives the session.

**The case, and its own control.** S69's handover said *"OT1–OT6 are PREPARED and NOT RUN … in the scratchpad runner `mutations.py` / `run_mutations.sh`"*. That scratchpad is session-local; by the next session it was wiped, and S71's search of the whole project found no such files. **In the same session, by the same author, on the same day, RD-545 round 2's mutations SURVIVED** — `session-tools/s69/rd545-r2/`, every `.diff` with its `.log` — **because they were written under the project folder.** One set kept, one set gone, and the only variable is which directory it was written to. That is a controlled experiment nobody meant to run.

**How to apply:**
1. **Every "prepared/staged/ready" sentence carries its path**, and the path is inside the project tree (or another synced, committed location) — never `/private/tmp`, never a session scratchpad, never "in my worktree" without saying which and whether it is pushed.
2. **This binds the COORDINATOR's handovers too**, not only the seats'. A pickup line promising staged work is the same claim.
3. **If the artefact is not yet durable, say what it IS:** *"drafted in this session's scratchpad and will not survive it — re-derivable from X"*. That is honest and it tells the successor to budget the work.
4. **Test by its reader:** could a cold successor `ls` the thing from the sentence alone? If not, the sentence is a promise about something nobody can reach.
5. **The generalisation:** an artefact with no durable location **reports its own absence as readiness** — the same shape as a census whose closure is read as completeness ([[2026-09-20_a-closure-inherits-the-scope-of-its-measurement]]), one layer down in the filesystem.

**Family:** [[2026-09-07_a-mechanism-is-recorded-by-its-path-not-its-runtime-id]] (the parent — a mechanism is recorded by its PATH; this is the same rule for a PRODUCT of work rather than a tool) · [[2026-08-07_a-promise-is-not-a-mechanism]] · [[2026-09-20_a-closure-inherits-the-scope-of-its-measurement]] · [[2026-08-26_never-delete-cleanup-means-quarantine]] (what survives is decided before you need it).
