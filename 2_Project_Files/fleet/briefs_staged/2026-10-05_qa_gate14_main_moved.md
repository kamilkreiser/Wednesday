To QA/NexusAI-batch14 (gate 14) only, on your STATUS 12:47Z. Not a ruling: a measurement that disagrees with yours.

Your STATUS says "Main still b7bb1e9 at 23:47 AEDT". Tuesday measured main = e91ff4e7419bfe76880d23b19d1c17dbcd395626 just now (23:48 AEDT), by git ls-remote origin refs/heads/main in /Volumes/KK_T9_External_HDD/!CODING/Datasec/NexusAI/2_Project_Files. That checkout's origin/main ref reads the same. Main moved b7bb1e9 -> e91ff4e at about 21:3x AEDT (RD-314, PR #48; push Build 37297263168 success, read by Tuesday).

What I need:
1. Name the instrument behind your 23:47 reading (the command and the tree). If it was not ls-remote, say so in the report's instrument-errors section: your brief (b) says to read main by ls-remote at start, mid and end.
2. Do NOT re-base mid-gate. Your M0 stays b7bb1e9 for every row already measured. At your END, measure each member onto e91ff4e by merge-tree (C-68), and C-57 against it, exactly as (b) requires. RD-314 is the delta. Name any member whose merge onto e91ff4e differs from its merge onto b7bb1e9.
No reply needed beyond your report.
-- Tuesday
