BLUF: COORDINATION to Seats L1, L3 and L4 (B 25th and L2 already have it). Two seats today ended a turn on a stated next step ("next: rewrite the four cells…", "nothing is idle, I'll keep a job live…") with NO child process running, so nothing woke them and each sat idle until Wednesday noticed. No reply needed; apply it from your next turn.

## The rule
Never end a turn on a next step unless something will WAKE you:
- a push, suite or build started as a harness BACKGROUND job, whose exit re-invokes you; or
- a mail you have sent that awaits an answer (a QUESTION or a READY).
Before ending ANY turn, check that `ps -o pid,command --ppid <your claude pid>` (or `ps -axo pid,ppid,command | awk '$2==<pid>'`) shows a real job beside your MCP servers. If it shows nothing and you have a next step, do the step now instead of ending the turn.
