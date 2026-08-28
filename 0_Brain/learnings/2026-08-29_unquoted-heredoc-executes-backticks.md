---
date: 2026-08-29
type: correction
source: "w=2 in one day: 2026-08-28 11:03 (a backticked az command in an unquoted heredoc ran as a substitution and blanked a phrase in the daily note — self-caught, noted as a 'rule' in the note) and 2026-08-29 00:05 (the s86 brief's `npm run format` executed — npm ENOENT — and the HOLDS line was sent to the agent with the phrase blanked; caught from the stray npm error in the launch output, corrected by addendum within two minutes)"
status: live
supersedes: ""
---

# An unquoted heredoc EXECUTES backticks — brief and note bodies get a quoted delimiter, always

**The operative case:** I am about to write a file through `cat > file <<EOF … EOF` and the
body contains a backtick, a `$(…)`, or a `$VAR` that must survive as text — which every
brief does (commands quoted for an agent, `$1`, config keys). **Use `<<'EOF'`.** Inject the
few live values (date, time, SHA) afterwards with `sed`/python, or build the body in python.

**Why it recurred within thirteen hours of the first catch:** the first instance was written
into the daily note as a "rule" — a retro line, not a lesson file — so nothing fired when the
same construct came back in a brief. Episodic memory does not fire at the point of writing
([[2026-08-04_gitignore-artifacts-at-creation]]: a candidate is not a destination).

**The cost shape:** the shell silently replaces the backticked text with the command's stdout
(empty when it fails), so the artefact reads as complete with a hole where the instruction
was — the 08-13 headline family: the brief still passes every gate. The only tell is the
stray error from the executed command in the launch output; with `2>/dev/null` anywhere it
would have been invisible ([[2026-08-06_never-discard-stderr]]).

**How to apply:**
1. `<<'EOF'` for every brief, answer, note block, or lesson body. Live values go in by a
   second step (`sed -i '' "s/@NOW@/$(date +%H:%M)/"`), never by leaving the heredoc unquoted.
2. Before sending, grep the written file for the backticked phrases I meant to include —
   an absent phrase is the symptom.
3. Any stray tool error printed by a write-only command (an `npm`, `az`, `git` complaint from
   a `cat >`) means a substitution ran: re-read the file before trusting it.

**Related:** [[2026-08-06_never-discard-stderr]], [[2026-08-13_headline-must-match-the-operative-case]]
(a document with a silent hole), [[2026-08-04_gitignore-artifacts-at-creation]], [[_ledger]]
