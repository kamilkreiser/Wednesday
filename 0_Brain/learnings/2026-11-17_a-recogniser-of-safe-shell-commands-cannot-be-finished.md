---
date: 2026-11-17
type: lesson
source: Friday's own delegation, CoAgent overnight build (two independent gate verdicts on one crate)
status: live
tier: M
---

# A list of "safe" shell commands cannot be finished: the shell itself, not only the tool, decides what a line does

**What happened.** A build seat wrote a recogniser that classed some shell commands as harmless reads. Gate 1 broke it through OPTIONS the deny-list did not know (a shortened long option that writes a file; a recursion flag). I had it rebuilt as an exact-spelling allow-list. Gate 2 broke the rebuild through the SHELL: the path the shell walks through a directory symlink differs from the real one; a quoted expansion is an assignment in zsh; an operand after an option is a file to one implementation and not another; a compatibility character in a file name is the plain name to the file system. Six new dimensions, none an option. The second gate judged that the list would not close, and I removed the recogniser: every shell command is treated as execute.

**The lesson.** When a control works by enumerating what is safe inside a general-purpose interpreter, each fix is easy and the set of ways to be wrong is open. Two gate rounds failing on DIFFERENT dimensions of one class is the signal to remove the mechanism, not to patch a third time.

## How to apply

1. **In a brief:** never commission "recognise the safe cases" of shell, SQL, a template language or any interpreter as a security boundary. Commission the conservative rule (everything is the dangerous class) and let the structured, non-interpreted path carry the convenience.
2. **At a gate return:** if round 2 fails on a different dimension from round 1, ask the gate the direct question "can this approach be made sound at all?" in the round-2 commission, so the answer arrives with the verdict. (Done here; it saved a third round.)
3. **The two-NO-GO cap is the trigger, and removal is not a third round.** Dropping the unsound mechanism for the conservative default is the coordinator's call; the usability cost goes to Kam on a card with the default already applied.
4. **Quarantine, never delete, the removed attempt**, with both verdicts cited, so a later attempt starts from the evidence.
