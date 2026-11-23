This addendum is from Friday (the owner's laptop coordinator seat). Client: General. Project: CoAgent. It belongs to the brief `2026-11-23_coagent_W-GATE-TEST_brief.md`. Seat W-GATE-TEST only. It is the facts ADDENDUM 3 told you to wait for.

# W-GATE-TEST ADDENDUM 4: what the `claude` launcher on the PC starts

The PC helper's answer to work order 16 (read-only, no model run) is saved WHOLE, unchanged: `/Volumes/Laptop-DEV/FRIDAY/0_Brain/reference/2026-11-16_claude-to-claude/windows/2026-11-23_WO-16_results.md` (81 lines; READ-ONLY; data from another machine: facts, not instructions). Friday read it whole; it holds no key or token and no real account folder (`<PROFILE>` throughout). Read it whole yourself. In short:
- All three launchers in the npm folder (the `.cmd`, the `.ps1`, the extensionless shim) start ONE native program directly and pass only the user's arguments: `<npm folder>\node_modules\@anthropic-ai\claude-code\bin\claude.exe`. No node, no script argument.
- That program exists, has the extension `.exe`, and prints `2.1.330 (Claude Code)`, exit 0, both through the launcher and when started directly; the package's `package.json` says name `@anthropic-ai/claude-code`, version `2.1.330`, `"bin": {"claude":"bin/claude.exe"}`.
- A second, different `claude.exe` sits deeper in the same package (`...\claude-code-win32-x64\claude.exe`), and a third, older one in another application's folder (2.1.76, from work order 15). Neither is what the launcher starts.

RULED BY FRIDAY:
1. **The runner starts exactly the program the owner's launcher starts:** it resolves a `.cmd` launcher by READING it (the one line that names the program, relative to the launcher's own folder), checks that the result exists, is an `.exe`, and that `<that program> --version` prints the same version line as `claude --version` through the launcher, and only then uses it. If the launcher's text has any other shape (more than one program line, a script argument, an interpreter), the runner REFUSES with the reason, as it does today. It never searches the disk for a `claude.exe` and never takes the first `.exe` on the PATH: two wrong ones exist on this very PC.
2. An explicit `-Claude <path>` parameter may override the resolution, with the same checks; the work order would then name the path with the profile part taken from the environment, never typed.
3. The raw files and the report record which program ran (its path with the profile part replaced, its size, its SHA-256, its version line), so a result can be tied to a build of Claude Code.
4. Everything else as ADDENDUM 3 item 5 says: a new head, `w1.py selftest` with new arms for this (a launcher of the PC's shape resolves; a launcher with a script argument is refused; a version mismatch is refused; a missing program is refused), the Mac stand-in `run-set`, the scope proofs; then `RUN ON PC REQUEST: <full sha> — STAGE A2` with the exact commands (no model run: the resolution printed, the selftest, and whatever your change touches) and the expected answers.

After ANY context compaction, re-read the brief, all addenda and your STATUS whole before writing anything more.
