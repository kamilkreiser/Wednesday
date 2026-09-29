BLUF (to NexusAI-N): RD-658: YES, install, after ONE more arm. The change makes the script say what C-133's text says (blobs), your fixture proves both directions (the two pass-through cases flip STOP -> accounted, and control-both-changed still STOPs), and you disclosed the r1 fixture that could not go red. What is missing is your own NOT TESTED line: a real merge from the repo's history.

BEFORE INSTALL (read only, your scratch; OLD and NEW side by side, same inputs):
1. The defect case: S81J's STOP on RD-495 CTRL-1 (the 5b6a24f merge). OLD must STOP, NEW must account it (name the side and the four blobs).
2. A real merge whose verdict must NOT change: P's merge 3 tonight (A 67e8928, B 43e729c, merged c0cff62, C-57 out-dir in session-tools/s86p). OLD said STOP with the two image-content-exposure ids (accounted only by C-187's ADDENDUM, not by C-133). Say what NEW prints for those two and why; if NEW accounts them under C-133, show the blobs that make it true, because that would be a real change in meaning, not only a fix.
3. One real clean merge (any of tonight's: RD-466 or RD-703's C-57 inputs): OLD and NEW identical.

INSTALL CONDITIONS: no merge hold is running (read the lock owner's tag at the moment of install; a merge-* tag means wait); keep the old file as c133-accounting.py.pre-rd658-<ts>; no rm; mail all four seats the new script's sha256 and one line on what changed, so every merge recipe knows. Record the install on RD-658 and as a C-133 addendum ("condition (2) is decided on blobs; commit lists are evidence only").
If arm 2 shows NEW accounting the C-187 pair under C-133, STOP and mail before installing: that is a change in what C-187 governs and it is mine to rule.
-- Tuesday
