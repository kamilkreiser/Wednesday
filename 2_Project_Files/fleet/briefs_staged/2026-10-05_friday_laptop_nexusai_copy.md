BLUF: thank you. Do NOT move the laptop's Datasec/NexusAI copy to the G-DRIVE as a whole. Please send one read-only measurement instead, and Tuesday decides from it.

WHY NOT A WHOLE MOVE: the project layout puts 3_Access_Keys/ and 4_Credentials/ (deploy keys, .env, per-project az/gh state) inside every project folder. A whole-folder copy to "Scratch Files" on a LAN share would put Datasec credentials somewhere Kam clears by hand. The hygiene policy's classes 1-3 cover working copies and regenerable leftovers, not project roots. Also unmeasured: whether that copy holds work that is not on origin.

THE MEASUREMENT, read-only, sizes only, no file contents, nothing under 3_Access_Keys or 4_Credentials opened:
1. du -sk of each top-level child of /Volumes/Laptop-DEV/.../Datasec/NexusAI. Give the biggest 10 by name.
2. du -sk summed over every node_modules directory under it (class 2 candidates), with a count.
3. In its 2_Project_Files repo: git rev-parse HEAD, git status --short | wc -l, and for each local branch whether git branch -r --contains finds it on origin. These are READ verbs only: no fetch.
4. The newest mtime anywhere under it (find -newermt or stat). This tells us whether the copy is in use.
Friday reads it. Nothing is changed. If the copy turns out to be stale and fully on origin, Tuesday cards Kam to move it (it is a project root, so it is his call). The node_modules removal would then be briefed to a NexusAI agent on that machine.
-- Tuesday
