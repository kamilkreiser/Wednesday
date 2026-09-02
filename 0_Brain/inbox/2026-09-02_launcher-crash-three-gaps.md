# Launcher crash 21:30 — fix detail + three gaps to queue
From: Kam's side-session Claude (not Wednesday), 2026-09-02 22:2x. For ledger + Linear; no reply needed.

**Fix (commit 9ee732e, pushed):** four inner double-quotes inside the bash double-quoted `INITIAL_PROMPT` string in `Launch_Wednesday.command` (lines 168, 172, 269, 270) were escaped as `\"` (line 213 already used that pattern). Verified by sourcing lines 140-282 with dummy vars: the full 9,716-char prompt now assigns and ends at the session-end ritual line.

**What actually happened:** `"go` at line 168 closed the string, so bash parsed line 140-168 as `INITIAL_PROMPT=... with ...` (an assignment prefix on a command called `with`, so the variable was never set in the shell), then `line 336: INITIAL_PROMPT: unbound variable` under `set -u`, and the pane fell through to `exec bash` from 21:31 to 22:04.

## Gaps
1. **Silent truncation since 16:27 (commit a7834ad).** The `"statusline` quote at line 269 ended the assignment early. The 16:30, 17:52, 19:27 and 20:29 seats booted WITHOUT lines 270-282 of the prompt (the 70% rotate instruction and the session-end ritual). `bash -n` passes, so a syntax check does not catch this.
2. **Dead-seat leg is too narrow.** `wake_watch.sh` leg (d) and `wednesday_rotate.sh --dead` only recognise `Context limit reached`. A launcher crash shows `[cockpit] wednesday exited — pane stays for inspection` and a `bash-3.2$` prompt; nothing respawned it, and the watcher typed its WAKE lines into bare bash (syntax errors) for 33 minutes. Suggest: treat that exit marker (or `pane_current_command` = bash with `@cockpit_name` = wednesday) as DEAD too.
3. **doctor.sh has no launcher parse check.** Suggest a `--check` that sources the prompt block with dummy vars and asserts `INITIAL_PROMPT` ends with the session-end ritual line, and a grep for unescaped `"` between the opening line and the closing line.

**Lesson rule:** the boot prompt is one bash double-quoted string; every quote inside it must be `\"`.
