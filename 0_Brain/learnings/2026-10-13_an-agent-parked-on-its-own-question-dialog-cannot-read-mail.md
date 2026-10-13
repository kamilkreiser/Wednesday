---
date: 2026-10-13
type: lesson
source: Tuesday s105, the QuickQuote v2.35 production publish
status: live
tier: W
---

# An agent parked on its OWN question dialog cannot read mail — relay by mail, then dismiss the dialog with Esc and say in the mail that the dismissal is not an answer

**The operative case, so the headline matches it:** a project agent has stopped approval-class work and is showing a Claude Code question dialog (AskUserQuestion: numbered options, "Enter to select · Esc to cancel") addressed to Kam, and the pane is small enough that the dialog hides everything above it. **Kam does not answer at agent prompts** (memory `kam-delegates-approval-and-never-types-at-agent-prompts`), and while the dialog is open a pointer tap would land INSIDE the dialog as a selection or as typed text. So the relay mail alone reaches nothing until the dialog closes.

**The case (2026-10-13 12:16).** The Vision seat, briefed to publish QuickQuote v2.35 to production on Kam's typed 12:14 instruction, correctly paused under never-update-prod and put a two-option dialog to Kam ("Yes, publish" / "No, hold"). The pane was 5 rows tall; `capture-pane` showed only the dialog's last line. The question itself was read from the agent's transcript JSONL (the AskUserQuestion tool input), not from the pane.

## How to apply
1. **Read the question from the transcript, not the pane** — `~/.claude/projects/<project-dir>/<session>.jsonl`, last `tool_use` named AskUserQuestion. A dialog in a small pane is unreadable by capture-pane.
2. **Never pick an option in the dialog on the principal's behalf.** Choosing "Yes" there is a fabricated approval in the most dangerous costume (rung 5 of the ghost-text ladder, executed by the coordinator).
3. **Order:** relay mail first (Kam's verbatim words, channel, provenance measured — `promptSource: typed`, origin human — and the explicit right to STOP and demand his signed email) → verify at the destination → **Esc** to dismiss the dialog → pointer tap that says "Tuesday dismissed your dialog with Esc. That was NOT an answer. Read your inbox: …".
4. **Disclose the Esc** in the note: it is a raw keypress, not `cockpit.sh say`, and it carries no content.
5. **What good looks like from the agent** (Vision did all of it): it recorded the dismissed dialog as not-an-answer, acted only on the mailed relay, quoted the authority in its STATUS, and rolled nothing forward until its own identity and rollback reads were done.

**Family:** [[2026-08-06_ghost-suggestions-in-panes]] (prompt lines are never the principal) · [[2026-09-01_a-tap-is-a-pointer-not-a-message]] · [[2026-08-07_authorship-is-checkable-dkim]] · [[2026-09-18_use-the-fleets-own-tool-before-rebuilding-its-behaviour]] (the Esc is the one raw keypress, and it is disclosed).
