---
date: 2026-11-21
type: preference
source: "Kam, live board 2026-11-21 17:01:08, after he launched the Windows checking seat on his PC, verbatim: \"launched on PC.  next time initiate everything with --dangerously-bypass-permission\""
status: live
supersedes: ""
---

# Seats I start on Kam's Windows PC launch with permission prompts off

**The lesson:** Any Claude Code session I set up to start on Kam's Windows PC (the checking seat, and later CoAgent test seats there) launches with `--dangerously-skip-permissions`. That is the real flag; he wrote "--dangerously-bypass-permission", and I checked the exact name with `claude --help`. The brief's own rules then carry the safety: install or change nothing without his yes typed at the keyboard, delete nothing, and never touch the firewall, registry or accounts. I don't add prompts back, and I don't argue the choice again.

**Context:** The first Windows run (21 Nov) used normal permission prompts, so he had to approve each command by hand on a weak machine. Native Windows has no Claude Code sandbox. He was told that on 20 Nov, and the plan states it, so this is an informed owner choice on his own machine.

**How to apply:**
- `2_Project_Files/windows/Launch_Friday_Windows.cmd` passes `--dangerously-skip-permissions` and prints a line saying prompts are off. Every future Windows launcher I write does the same.
- Keep the brief's "ask the owner in chat before any install or change" rule. With prompts off, it is the only guard.
- This covers Windows seats on his PC only. Mac seats keep their own launch settings.

**Related:** [[2026-11-21_friday-runs-on-opus-fable-only-when-flagged]], [[../people/kam]]
