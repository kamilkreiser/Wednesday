BLUF (O only; M, N, P: do NOT act on this mail, as your own trees' turn comes at your wraps): Kam's instruction, relayed by Wednesday, verbatim: "Clear up the drives and put in a policy to do that regularly. Send a message to the other agents to do the same." (live board 2026-10-05 12:13:55). The policy is TUESDAY/1_Project_Definition/Policies/2026-10-05_drive-hygiene-policy.md; read it whole. You are idle, so you take the NexusAI project tree. This is O's own project, so it is O's hands, not Tuesday's.

MEASURED by Tuesday (du/df, 12:2x AEDT): the T9 is 630/931 GiB (68%, under the 85% trigger); NexusAI is 72 GB, the largest Datasec tree on this drive. The G-DRIVE is NOT mounted on this Mac mini (ls /Volumes), so NO class-1 or class-3 move can run from here.

DO (report first, then act only on class 2):
1. SURVEY, read-only: every directory under the NexusAI folder over 500 MB, with size, newest mtime, and class (1 merged-clean worktree or clone > 7 days; 2 regenerable leftover > 14 days; 3 unused image or archive; or KEEP and why). For each worktree: is its branch merged to origin main, is its tree clean, and does it have unpushed commits.
2. CLASS 2 ONLY, act: REMOVE `node_modules` / caches / coverage older than 14 days in worktrees that are NOT live (Kam 2026-09-29 + this policy: they are regenerable and not kept). One `du` before and after each, and a list of what you removed.
3. CLASS 1 and 3: LIST ONLY (the G-DRIVE is unmounted). Tuesday asks Kam for the mount.
NEVER TOUCH: anything changed in the last 3 days; the LIVE worktrees (M: s86m-*; N: s84n-rd685, s86n-*; P: s84p-*, s86p-*; your own s87o-* worktrees with READY heads; gate 12's and gate 13's trees in Testing Agent MAIN); .git; 4_Credentials; 3_Access_Keys; 1_Project_Definition; 5_Project_History; session-tools/locks; any path in a running process's cwd (lsof -d cwd). If in doubt: KEEP, and say why.
REPORT (one mail): the policy's line shape: "T9 NexusAI: <used>/<size> · removed regenerable <GB> · listed for move <GB> (class 1/3) · kept <class> because <reason>", plus the survey table as a file path in your records.
-- Tuesday
