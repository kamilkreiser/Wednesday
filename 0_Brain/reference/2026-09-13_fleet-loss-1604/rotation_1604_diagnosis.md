# 16:04:29 rotation — why the agents died (read-only diagnosis, 2026-09-13)

All times AEST unless marked Z (transcripts are UTC: 06:04:29Z = 16:04:29 AEST).

## BLUF

**Mechanism: PARTLY established.**

- **ESTABLISHED:** at **16:04:29.03 the whole `fleet` tmux session was destroyed as one unit.** That took every pane with it: s194 (%38), s195 (%39), the QA gate (%40), the monitor (%1), and the launcher that had started in %0 about 35 ms earlier. It happened **~36 ms after `respawn-pane -k` ran on %0**. These processes share only one parent, the tmux server / `fleet` session, and every one of them died in the same ~10 ms. This was not a string of separate agent exits.
- **NOT ESTABLISHED:** what made a one-pane respawn end the session or server. None of these ran at that moment: a kill-session, kill-server or kill-pane from any script; a tmux upgrade; a Claude Code update; a crash report; a memory-pressure (jetsam) kill.
- **Best-supported HYPOTHESIS (labelled as such):** the tmux 3.7b server itself exited, either through a fatal exit or a delivered signal, while handling the `-k` respawn of %0. It is rare: **1 loss in 63 rotations that had agents live** (2026-09-02 16:30 to 2026-09-12 16:04).

**Would it recur today?** It cannot be ruled out, and nothing has changed since 16:04: same script, same tmux binary, and agents still share the coordinator's tmux server. **Guard that prevents the effect whatever the trigger:** put the coordinator's pane on its OWN tmux server/socket, separate from the agents. `respawn-pane -k` then never touches a server that holds agents. **Companion post-condition:** `wednesday_rotate.sh` checks the fleet session and the agent-pane set after the respawn, and rebuilds and alerts on a loss. Details are in the last section.

The rotation was also dark for 16 hours because **nothing recovers a missing fleet session.** The watcher only logs, and `--dead` refuses when there is no session. Kam then restarted the Mac at 16:27 and 17:07 (`last`), and no seat booted until 2026-09-13 08:39.

## FOUND

1. **The OS log shows the respawn, then a second kill 36 ms later that the 14:40 control does not have.**
   - 16:04:28.991: caffeinate 91930 exits (the coordinator's). 28.992: `zsh` exec (tmux default-shell running the respawn command). 29.000 and 29.006: `bash` (the respawned launcher). 29.001: node 56968 exits.
   - **29.027: caffeinate 92072, 91448 and 91373 exit in the SAME millisecond. 29.033, 29.034, 29.038: node 86123, 17021 and 82237 exit.** That is one caffeinate plus one node per agent session.
   - **Control, the harmless 14:40:08 rotation:** tmux client 56566, caffeinate 54752 exits, zsh, node 52752 exits, tmux 56568 (set-option), launcher bash, git 56586 (launcher). **Only one caffeinate and one node.**
2. **The agents recorded their tools being SIGKILLed at that instant, then never wrote again:**
   - **s194** `229061dc…`: Bash tool_use at 06:04:00.221Z ("File QA-961 ticket, post verdicts, census, squash-merge #961"). tool_result at **06:04:29.123Z, is_error=true, "Exit code 137"** (137 = SIGKILL). The partial output shows **KS-1111 filed** and a **KS-1098 verdict comment posted**. No row after that, so it stopped mid-turn, mid-command. It was part-way through external writes, and whether the #961 squash-merge happened is **UNKNOWN; check it.**
   - **s195** `5c4a861a…`: already wrapped (06:02:56Z per NEXT-PICKUP.md:10) and idle. Its background task `b9gmo61l2` (`wait_for_mail.py`) logged **status killed at 06:04:29.121Z**. No row after that; a live seat would have taken a turn on that notification.
   - **QA gate** `-Volumes-DevMASTER--CODING-Testing-Agent-MAIN/598afd13…`: last timestamped row is a tool_result at 06:03:30.168Z (lockfile parity check), then untimestamped last-prompt/cost-state rows. File mtime 16:04:29. It was mid-turn waiting on the model; there is no verdict row.
   - **Coordinator** `ee2841ed…`: the final call (06:04:16.027Z) nohup'd the rotate script. Its result at 06:04:24.373Z reads "rotation started detached, pid 93197, at 16:04:24". Then at 06:04:29.108/.109Z two background tasks show **killed** (`bzsqjytog` #962 verdict wait, `bddd3j1kk` #963 push wait). This is the normal shape for a rotated seat: the 14:40 seat has the same killed row at 04:40:08.070Z, and the 09:18 seat at 23:18:04.004Z.
   - **None of the four transcripts has an end_turn row or "interrupted" text.**
3. **The new seat never got past the first ~50 ms of its launcher.**
   - There is no launcher `git` call after 29.006; the control shows one 45 ms in.
   - **Zero Tailscale log lines from 16:04:29 to 16:05:30.** The controls show **30 lines at 12:08:36-12:09:00 and 30 at 14:40:08-14:40:30**, which is doctor.sh's `tailscale status`, about 9 s after a respawn.
   - This explains why no coordinator transcript exists between 16:04 and 08:39.
4. **The panes were destroyed; their claude processes did not merely exit.**
   - Panes are created with an `exec bash` tail (cockpit.sh:109; the 16:04 seat added %40 via `cockpit.sh add "QA/Secuura-ks1029-962"`, per the ee2841ed transcript). A pane whose claude exits therefore stays, keeps its @cockpit_name, and trips a monitor DEATH alert (monitor.sh:56).
   - The monitor's state files `.hash_/.time_{Secuura_Blockchain, Secuura_Blockchain_B, QA_Secuura_ks1029_962}` were **last written 16:04:02**, with no 16:05 cycle, and **alerts.log was last written 15:56:01** (no DEATH line).
   - The watcher counts names, not liveness (arm_wake_watch.sh:107), and logged **16:05:04 agents=0** (wake_watch_runner.log:9940; the previous row, :9937 at 16:03:03, had agents=3).
5. **iTerm2 reacted after the kill, not before.** At 16:04:29.275 it made 18 pasteboard reads, and at 16:04:33.339 it posted a user notification. The 14:40 control has no iTerm2 lines. iTerm2 is attached with `tmux -CC` (Launch_Cockpit.command:142).
6. **The invocation was not what differed.**
   - The 12:08:36 rotation had the same shape: nohup from a foreground call that returned 3 s before the respawn (ca383558 result 02:08:33.669Z), and the chat mirror ran (rotate_wednesday.log:299-301). Its agent survived: %31 was closed later, at 12:27:58 (pane_close.log).
   - At 09:18:03 and 14:40:08 there is no chat line (log:295-296, 302-303). At 14:40 the rotate script ran as the seat's background task and was killed with the seat (killed row b064a3ahd at 04:40:08Z).
   - 16:04 has no REFUSED line and no error line, and uses the same pane %0.
7. **Across the full rotation history, this is the only real loss.** 65 rotations had agents>0 before and a watcher line within 15 min after. 3 show a drop to 0:
   - 2026-09-02 16:20:13 and 16:20:17 were **`fleet-rt` test rotations** (rotate_wednesday.log:2-5). The drop came first: agents=2 at 16:04:33 then 0 at 16:21:02 (runner log:3805, :3808), matching "until Kam killed the fleet at 16:06" (wednesday_rotate.sh:8).
   - **2026-09-12 16:04:29 is the one genuine loss: 1 of 63.**

## TESTED (what I examined)

- Read whole: `wednesday_rotate.sh` (89 lines), `Launch_Wednesday.command` (623), `cockpit.sh` (441), `arm_wake_watch.sh`, `rotate_wednesday.log` (308).
- Also read: monitor.sh, Launch_Cockpit.command:85-148, server.py:520-570.
- Four transcripts: tails, the killed tasks' tool_use inputs, and final commands. Earlier coordinator transcripts 67e2e56d, ca383558 and d009e255 as controls.
- Logs: wake_watch_runner.log (09-12 15:40-16:05, 09-02 15:50-16:29), pane_close.log, tap_wednesday.log, panel_sync.log, monitor state-file mtimes.
- git: reflog 15:58-16:06, commits 15:50-17:30, change history of the rotate/launcher/cockpit/doctor/monitor files, panel_sync commit stats.
- System: Claude Code `versions/` mtimes, the tmux Cellar, tmux global options, `last`, DiagnosticReports (user, system, Retired), current `ps`.
- Unified log, bounded windows only: 16:04:25-35, 16:04:28-32, 16:04:29-16:05:30; controls at 14:40:07-50 and 12:08:36-12:09:00.

## HOW (commands → evidence, file:line)

- **Rotation record:** `rotate_wednesday.log:304-308`. 16:04:29 "respawning wednesday pane %0 … (--self)", "respawned OK", chat mirror (339), then "[browser speaks…]". So the rotate script survived and ran to the end.
- **Respawn code:** `wednesday_rotate.sh:76`, `respawn-pane -k -t %0 "bash Launch_Wednesday.command; …; exec bash"`. LAUNCH_CMD is at :45. "respawned OK" depends only on respawn-pane's rc (:76-78). **:80 tells Kam "agents are untouched" without checking.**
- **Launcher:** `Launch_Wednesday.command` has no tmux, kill or respawn call and never runs cockpit.sh.
  - Grep for `tmux|kill|cockpit.sh|read -r|exec claude`: tmux/cockpit.sh match only prompt text (:467, :525); control hit :623 `exec claude`.
  - There is **no Resume/Fresh prompt in this launcher.** Its only prompt is doctor's hard-fail `[y/N]` (:209-216): no timeout, default N → exit 1.
  - The Resume/Fresh prompt lives in `Launch_Cockpit.command:100-133`: default Resume; Fresh runs `kill-session` (:126) and needs a typed YES when agents are live (:119-124). Nothing shows it ran: no new session or seat appeared afterwards.
- **Other kill sites (grep over fleet/, tools/, dashboard/, scheduler/, doctor.sh):**
  - `cockpit.sh:421` kill-pane (rotate subcommand) and `:436` kill-session (`down`).
  - `pane_close.sh:93` kill-pane. Its log ends at :463-464, 15:57:05 (%37). No 16:04 entry; the control is that the same log recorded 15:57.
  - `arm_wake_watch.sh:96` `pkill -f wake_watch\.sh`, which runs only when the runner is dead. The runner was alive and logged at 16:05:04.
  - `server.py:535/562` `pkill -g` on the speak group. It needs the chat message, which was written after 29.027, and no `pkill` exec appears in the log.
  - `chat_reply.sh` + `speak.sh`: 0 tmux/kill hits (control: 5 hits for known strings).
- **Transcript tails:** a python parser over the last ~400 KB (scratchpad `tailrows.py`, `lastcmd.py`).
  - **Control:** grep for `status>killed|Exit code 137` in Secuura + QA transcripts at the earlier rotation instants gives **0 at 04:40:0[89]Z, 0 at 02:08:3[67]Z, 0 at 23:18:0[45]Z; 2 at 06:04:29Z.**
- **Unified log (`log show --style compact`, predicates: termination reported | keys-off | triggered unnest | exited due to | iTerm2 | tailscale):**
  - **Control that the log covers the moment:** 2,908 lines in 16:04:29-16:04:30.
  - Tailscale counts: 0 (16:04:29-16:05:30) vs 30 and 30 in the two controls.
  - ReportCrash at 16:04:38.805: **pid 6847 = com.apple.SafariPlatformSupport, non-fatal 15 MB watermark.** Unrelated.
  - Before the kill, the only `SIGKILL` lines are mdworker processes killed by mds at 16:04:25. No `memorystatus` kill lines.
- **No tmux crash report:** no .ips from 09-12 in `~/Library/Logs/DiagnosticReports` or `/Library/Logs/DiagnosticReports` (Retired is empty). **Control:** the user folder holds `node-2026-09-07-*.ips`, so user-process crashes do land there.
- **No update or upgrade near 16:04:**
  - `~/.local/share/claude/versions`: 2.1.269 installed 12 Sep 05:21:04; **2.1.270 at 13 Sep 08:40:22.** The "Update installed · Restart to update" banner is today's.
  - tmux `Cellar/tmux/3.7b` was installed 4 Aug and there is no other version.
  - Scripts: no commits 09-11 12:00 to 09-12 16:10 on wednesday_rotate/Launch_Wednesday/cockpit.conf/arm_wake_watch/cockpit/doctor/monitor. Control: the last commit on wednesday_rotate.sh is found, d62ce2dd on 09-07.
- **tmux server lifetime:** pane ids ran monotonically from %23 (09-11 22:36) to %37 (09-12 15:57) with wednesday fixed at %0 (pane_close.log), so one server outlived every earlier rotation. The current server started 13 Sep 08:39:47 (`tmux display -p`). `exit-empty on`, `destroy-unattached off`; there is no tmux.conf.
- **Afterwards:**
  - panel_sync runs outside tmux and ends at `panel_sync.log:4858` (16:26:14), right before the 16:27 shutdown (`last`: shutdown 16:27, reboot 16:27, console 16:37-17:07, shutdown 17:07, reboot 17:09, reboot 13 Sep 05:28).
  - The tap log's last line is :870 at 15:24:29; nothing near 16:00-16:10.
  - Watcher: next line after 16:05:04 is 09-13 08:40:07.

## NOT ESTABLISHED

- **What ended the tmux server or session at 16:04:29.03:** a tmux fatal exit, a signal, or an iTerm2 `-CC` command. tmux keeps no server log, the unified log does not record tmux, and a fatal/exit(1) leaves no crash report.
- **Why this rotation and not the other 62.** Things that differed but are not shown to be causal: 3 agents live, one mid-command (s194 node/Linear writes) and one mid-model-turn (QA); two coordinator background tasks; chat mirror plus browser autoplay after the respawn. Also observed but **not controlled:** Avast's network extension logged claude-code flows to api.anthropic.com at 16:04:29.000-.039 as "provider rejected new flow".
- **Whether the tmux server outlived the session**, i.e. killed session versus dead server. Both give the same observables here.
  - The 16:27:09 and 17:07:41 `shutdown_stall` reports would show whether any tmux/claude process was still alive at shutdown. They are spindump binary, and my grep was blind to them (control: WindowServer = 0). `spindump -i <file>` would settle it; not run.
- **How %38 and %39 were created** was not verified; only %40 was. Both `cockpit.sh launch` and `add` go through add_pane (cockpit.sh:213, :170).
- **Login/auth state** at 16:04 was not examined; nothing points to it.

## WOULD IT RECUR TODAY + THE GUARD

**Recurrence:** possible, and with no warning.
- The trigger is unknown. The observed rate is 1 in 63 rotations with agents live.
- Nothing has changed: script, tmux binary, topology (wednesday, fleet-monitor and agents all in `fleet:0`; cockpit.conf and cockpit.sh:109).
- A QA agent claude process is running now (`ps`: started 08:54:15), so today's `--self` carries the same exposure.
- If it happens again, nothing respawns the fleet: the watcher only logs "no wednesday pane" (arm_wake_watch.sh:173), and `--dead` refuses when there is no session (wednesday_rotate.sh:47).

**Guard that prevents it (named, not implemented):**
1. **Separate the coordinator's tmux server from the agents'.** Run the wednesday pane on its own socket (e.g. `tmux -L wednesday`) and the agents on `fleet`. `wednesday_rotate.sh` then respawns inside a server that holds no agents, so even a server-level failure during `respawn-pane -k` cannot kill agents. This is the only guard that works without knowing the trigger.
   - Cost: every `-t fleet` caller that addresses wednesday (rotate, watcher tap, monitor, cockpit layout) needs the socket, and the iTerm2 view becomes two attaches.
2. **Post-condition in `wednesday_rotate.sh`** (damage control, required alongside 1):
   - Before the respawn, snapshot `has-session` plus the set of agent panes (@cockpit_name and pane_pid).
   - About 3-5 s after, re-check that the session, those panes and the new %0 process are all alive.
   - On any loss, log `FLEET LOST`, mirror it to Kam, and rebuild with `cockpit.sh up` plus a relaunch list.
   - Never send "agents are untouched" (:80) unless that check passed.
   - Also make the watcher treat "no fleet session" as a wake that rebuilds, not a log line.
3. **Rejected as a guard:** "don't rotate while agents are mid-command". s195 (idle, wrapped) and the QA gate (waiting on the model) died too, so it would not have prevented 16:04.

**Follow-ups from the damage:**
- s194 was killed part-way through external writes. KS-1111 was filed and the KS-1098 comment posted; check whether the #961 squash-merge happened.
- The #962 QA gate produced no verdict.
- s195 had wrapped; confirm its wrap on disk.
