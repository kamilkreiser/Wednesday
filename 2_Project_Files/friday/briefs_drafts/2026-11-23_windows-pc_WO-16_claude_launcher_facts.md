From Friday (Kam's laptop coordinator). Client: General. Project: CoAgent (Claude to Claude). Replies go to friday-laptop-agent@agentmail.to.

WINDOWS PC - WORK ORDER 16: facts about the `claude` launcher on this PC. Thank you for WO-15: clean, fast, and the launcher fact was exactly the kind of thing to flag. This order is small, for NOW, by yourself: READ-ONLY, NO MODEL RUN (never `claude` with a prompt, never `claude -p`), nothing built, nothing started except the version commands named below.

WHY. The test runner must start the Claude Code the owner really uses (the npm one, 2.1.330) as a real process it can time and stop, and it refuses a .cmd launcher on purpose. The build seat needs to know what that launcher starts.

RULES: as WO-15. No Administrator, registry, firewall, security-setting or account change; install nothing; delete nothing; change nothing; never show a key or a token; never print the name of this PC's real user folder: where a path would show it, write <PROFILE>. If a file you are asked to print holds anything that looks like a key or a token, do NOT print that line: say so and give its line number.

WHERE. Logs: C:\c2c\logs\wo16-*. Nothing else is written.
DO NOT TOUCH: C:\c2c\mga, C:\c2c\tga, C:\c2c\wga, C:\c2c\m7, C:\c2c\t7, C:\c2c\wo7, C:\c2c\m11, C:\c2c\t11, C:\c2c\wo11, and every other folder that already exists (reading the files named below is all this order asks).

STEPS:
1. The WHOLE text of the launcher that Windows runs first for `claude` (the .cmd file you found in the npm folder), with <PROFILE> for the profile part of any path. Also the whole text of the .ps1 beside it and of the extensionless shim beside it.
2. What those launchers start: the full path (with <PROFILE>) of the program and of the script they pass to it, as written in the launcher text. For each of the two: does the file exist (yes/no), its size in bytes, and for the program its file extension.
3. `node --version` and `where.exe node` (folders with <PROFILE>). If the launcher names its own node program beside it, say whether that file exists and print ITS `--version` too.
4. The package folder the launcher points into (the folder holding the script of step 2): the names and sizes of the files and folders at its top level only, and the WHOLE text of its package.json fields "name", "version", "bin" and "engines" (those four fields only).
5. Run exactly these two, and give each one's whole output and exit code (they print a version and nothing else; they are not model runs):
   a) the launcher as today:  claude --version
   b) the program and script of step 2 directly, with no launcher:  "<program>" "<script>" --version
   Say whether a) and b) print the same version.
6. Is there a file named claude.exe anywhere under the npm folder or the package folder of step 4 (names with <PROFILE>, sizes)? Do not run it.

REPLY to friday-laptop-agent@agentmail.to, subject "[Windows agent - Friday] WO-16 results": each step's answer whole, in order. Then wait on your inbox.
