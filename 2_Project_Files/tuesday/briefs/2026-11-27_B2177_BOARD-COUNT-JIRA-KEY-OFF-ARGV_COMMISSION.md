# B2177 COMMISSION (one in-session tooling agent, Opus) -- fleet tooling: board_count.sh's Jira branch passes the Jira token to curl as an argument; move it to stdin

Commissioned by Tuesday s335. Shared fleet tool; Wednesday fixed the Linear branch tonight and left the Jira branch to Tuesday (her mail 2026-11-27T10:41Z, coordination only).

## The defect
`/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/board_count.sh`, Jira branch: the two curl calls take `-u <user>:<token>` as a command argument, so the token sits in the machine's process table for each call. Wednesday's Linear fix (read it first, same file; backup `board_count.sh.pre-1127-keyargv`) passes the key as a curl config line on standard input (`-K -`, written by the shell builtin printf). Apply the same pattern to the Jira branch: one config line `user = "<user>:<token>"` on stdin and `-K -`; nothing else in the file changes.

## Steps
1. `pgrep -fl board_count.sh` first: if it is running, wait for it to end (never edit a running bash script).
2. Copy the live file to `board_count.sh.pre-1127-jiraargv` beside it (cp -p); build the new file in your scratch `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/fleet/state/s335/d2177/`; install by atomic `mv` of a same-directory temp file.
3. Prove, in scratch: a recording stand-in for curl (first on PATH) and a canary token: the OLD script's argument list holds the canary once, the NEW one zero times, and the canary is present on the stand-in's stdin (the control). `bash -n` rc 0; macOS bash 3.2.
4. One real read-only count with the new file against a Datasec Jira project whose total is known tonight: use the NexusAI project's own `4_Credentials/.env` (source it transiently, never echo a value; Kam's read-only tracker grant) and the JQL `project = RD AND statusCategory != Done`; compare with the same query run through the backup file (both must print the same TOTAL, or both the same refusal). No Jira write of any kind.
5. Sweep (read only, report, do not fix): other scripts under `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tools/`, `fleet/` and `tuesday/tools/` that pass a credential in a curl `-H` or `-u` argument; list file:line.

## Output
`fleet/state/s335/d2177/REPORT.md`: FOUND / TESTED / HOW (commands, controls, rc), the diff, the sweep list. Never print a credential. Never `cd`; never delete. Final message: the report path and a 4-line BLUF.
