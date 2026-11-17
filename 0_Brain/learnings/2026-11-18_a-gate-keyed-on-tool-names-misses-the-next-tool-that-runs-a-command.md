---
date: 2026-11-18
type: lesson
source: Friday's own delegation, CoAgent permission gate; third independent check, verdict of 2026-11-17 evening (`reference/2026-11-16_claude-to-claude/m1_review/gate_M2_POLICY_r5_verdict.md`, finding M1)
status: live
tier: M
---

# A gate keyed on tool NAMES misses the next tool that runs a command: brief the gate on what the input DOES, never on what the tool is called

**The operative case.** Friday is about to brief, or review, any control that decides how dangerous an agent's action is: a permission gate, a hook, an allow-list, an audit filter. The brief names the tools it covers ("Bash", "PowerShell"). **Stop: name the capability, and make the unknown case the strict one.**

**What happened.** The permission gate was rebuilt over five rounds around one rule from Kam: every terminal command asks, each time, on a red card. The third check tried 135,408 decisions over 651 generated commands and found no shell text that got less than that. It still failed, on a door nobody had looked at: Claude Code has a second tool, Monitor, whose input also carries a `command` that is run as shell. The gate classed it as an unknown tool, and unknown tools got the ordinary card: batchable, allowed for the session, with none of the hard refusals. So the strictest rule in the product held for the tool named in the brief and did not exist for its sibling.

**Friday's part.** Every brief and addendum for that piece said "Bash" or "the terminal tool". None said "any tool whose input is executed as a command", and none asked what an unknown tool gets by default. Five rounds of checks attacked the text of commands and none listed the tools.

**How to apply:**
1. **Write the rule by capability:** "any tool input that is executed as a command, by whatever tool" (likewise: any input that is written to a file, any input that is fetched). The named tools are examples under it, never the definition.
2. **The unknown case is the strict case.** A tool the control does not recognise gets the highest tier, not the middle one. A brief says so in one sentence and asks for the test: a made-up tool name carrying a command must get the red card.
3. **Enumerate the surface before the logic.** The first step of such a build, and the first item of its check, is the list of every tool the host offers and every field in each that can carry a command, a path or a URL, read from the host's own tool list at that moment, not from memory. The list is a dated measurement: a new host version adds tools.
4. **In a gate commission, ask for the sibling:** "which other inputs reach the same effect by another route?" is a standing line in the check's attack list.

**Family:** [[2026-11-17_a-recogniser-of-safe-shell-commands-cannot-be-finished]] (the same piece: an allow-list of safe commands cannot be finished; here an allow-list of dangerous tools cannot either) · [[2026-08-07_enumerate-every-surface-before-done]] (list the render paths; here, list the tools) · "A guard's refusal set is built from MISSING and MALFORMED" and "Read a guard's EXCLUSION list before trusting the guard" (the class a guard skips is where the failure is).
