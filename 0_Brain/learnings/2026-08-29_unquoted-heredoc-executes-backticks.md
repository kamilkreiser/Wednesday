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

## Extension 2026-09-02 (launcher costume): an unescaped `"` inside a double-quoted bash STRING truncates it silently, and `bash -n` passes
**The case.** `Launch_Wednesday.command` builds the boot prompt as ONE double-quoted bash string (`INITIAL_PROMPT="…"`). Commit a7834ad (16:27) added a line containing `a "statusline` — the quote CLOSED the string. `bash -n` passed. Four seats (16:30, 17:52, 19:27, 20:29) booted WITHOUT the prompt's tail (the 70% rotate line and the session-end ritual) and nobody saw it. At 20:5x a second unescaped quote (`"go` mid-line 168) made bash parse the block as a command called `with`; under `set -u` the 21:30 seat died at boot with `INITIAL_PROMPT: unbound variable`, the pane fell to bare bash, the watcher typed WAKE lines into it for 33 minutes, and Kam noticed before any mechanism did. Found and fixed by Kam's side-session Claude (9ee732e): every inner quote is `\"`.

**The rule, extended:** the heredoc rule (`<<'EOF'`) and this one are the same defect from two sides — prose carried through a shell that INTERPRETS it. (1) Any prose inside a double-quoted bash string carries `\"` for every quote — and the safer shape is no prose in a double-quoted string at all: a quoted heredoc into a variable (`INITIAL_PROMPT=$(cat <<'EOF' … EOF)`) never has this problem. (2) `bash -n` is a check that cannot see a string boundary moving; the check that CAN is to source the block with dummy vars and assert the variable ENDS where it should (WED-141 puts that into doctor.sh). (3) A seat that dies at boot leaves a bare shell, not the `Context limit reached` literal — the DEAD leg must recognise that shape too (WED-140).
