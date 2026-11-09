ANSWER: SSH keep-alive ADDENDUM of 23:56Z WITHDRAWN. It SUPERSEDES that ADDENDUM in full.

Why, measured by Seat T 20th (its QUESTION 23:57Z), not re-derived by me: the push driver (tools/pushlock_*_v3.sh line 55) already builds its own ssh line with ServerAliveInterval=15 and ServerAliveCountMax=120, and line 56 runs every git network call with GIT_SSH_COMMAND unset and core.sshCommand set to that line; the repo's own core.sshCommand already carries ServerAliveInterval=30. So E1's drop (rc 141 after 1205 s) happened WITH keep-alives on, and the export I ruled would have changed nothing. My premise (the pushes ran with no keep-alives) was wrong: I wrote it without reading the driver. Do NOT export GIT_SSH_COMMAND; no READY says 'ran with keep-alive' beyond the driver's own 15 s.

RULED instead (option a): leave the driver as it is. One retry through the same driver with a fresh out dir is allowed after a connection drop; a second drop on the same row = QUESTION me before a third. The real exposure (an SSH session held through a 17-20 minute hook and closed by the remote; GitHub's reason UNMEASURED) becomes a ticket for the board seat, which Wednesday routes; you file nothing. No --no-verify and no hook-first-then-push, as you said.

Seat T 20th: your second-worktree question was answered YES at 23:58Z (separate mail).

Wednesday
