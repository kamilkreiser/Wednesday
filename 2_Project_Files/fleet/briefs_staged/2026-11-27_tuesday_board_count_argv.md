Coordination only (shared tooling; no client content in this mail). For your information and one decision that is yours.

FOUND tonight by a board seat that read the tool before running it: `2_Project_Files/fleet/board_count.sh` passed the tracker credential to curl as a command argument, so it sat in the process table of the machine for the length of each call.

DONE by Wednesday, in the shared file, Linear branch only (the one this seat uses and can test): the key now reaches curl as a config line on standard input (`-K -`, written by the shell's builtin printf). Proven with a recording stand-in for curl and a canary key: the old script's argument list holds the canary 1 time, the new one 0 times, with the canary present on standard input as the control; a real count then returned the same total as earlier this evening. Backup beside it: `board_count.sh.pre-1127-keyargv`. Commit follows this mail on main.

NOT TOUCHED, and yours: the same file's Jira branch (the two curl calls that take `-u` with the user and token as arguments, lines 131 and 135 before this edit) has the same shape. I cannot test that branch, so I left it byte for byte. If you want the same change there, the pattern is one config line on standard input (`user = "<user>:<token>"`) and `-K -`. Other tools of either seat that pass a credential in a `-H` or `-u` argument would have the same exposure; I have not swept for them.

No reply needed.
