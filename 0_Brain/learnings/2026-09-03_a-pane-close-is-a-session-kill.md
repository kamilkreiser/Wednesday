---
date: 2026-09-03
type: correction
source: own act at 06:5x (pane %23 closed; the :3052 QA surface died with it) — second instance of the 2026-09-02 04:29 row (ledger w=2)
status: live
---

# A pane close is a SESSION kill — a listener with parent 1 still dies if it shares the pane's tty; check `ps -o sess,tty`, never `ppid`

**The operative case, so the headline matches it:** I am about to close (kill) a builder's or tester's pane, and a surface the handover names as "left up" is served by a process whose parent is `launchd` (ppid 1). **That is not daemonisation.** A process reparented to 1 after its parent exited can still be a member of the pane's SESSION with the pane's controlling tty; when the pane dies, the tty hangs up and every process still attached to it gets SIGHUP. The check is `ps -o pid,ppid,sess,tty -p <pid>`: tty `??` (and session 0) = detached and survives; `ttysNNN` = it dies with the pane, whatever its ppid says.

## The two cases

1. **2026-09-02 04:29 (w=1):** the QA surface at `:3017` (PID 68452) was a CHILD of the pane's shell; closing s15's wrapped pane killed the process tree. The rule written then: "before closing any builder pane, `lsof` the listeners its tree owns". Correct for that shape, blind to the next.
2. **2026-09-03 06:5x (w=2):** NexusAI S21's two surfaces: `:3052` PID 82968 under `bash ./scripts/qa-surface-up.sh` (82966, **ppid 1**) — started INLINE from the pane; `:3053` PID 95059 under a bash launched from a SCRIPT FILE (95058, ppid 1, **sess 0, tty `??`**). I ran the w=1 check (the pane's process tree by `pgrep -P`: only the session's MCP servers and a `tail`), read both ppids as 1, called both daemonised, closed the pane. `:3052` → 000 within the second; `:3053` survived. The builder had written the exact trap into its own handover an hour earlier: "an inline `nohup … &` in a tool call is reaped when the call returns — launch from a script file" — and I had read it and still read `ppid 1` as the proof.

## Why the w=1 rule did not fire (the diagnosis w=2 requires)

The w=1 rule named the wrong discriminator. "Listeners its tree owns" is a PARENTAGE test; the kill is a TTY/SESSION event. A process can leave the tree (reparent to 1) and keep the tty. Every reading I took was true and none of them measured the property that decides survival — the 08-07 a-check-that-cannot-fail shape: the check I ran could only ever say "safe". The tester in pass 12 had already used the right instrument in its own isolation table ("sess 0, tty `??` (daemonised)") and I read it as prose, not as the method.

## How to apply

1. **Before closing ANY pane, for EVERY listener the handover names as up:** `ps -o pid,ppid,sess,tty,command -p <pid> <parent>` — tty must read `??` on the listener AND on its immediate parent. A `ttys…` anywhere in that pair = it dies with the pane: do not close until the surface is re-stood detached, or its owner has said it may die.
2. **`ppid 1` proves nothing about survival.** Say "detached" only after reading the tty.
3. **After ANY pane close, curl every surface the handover names as up, in the same minutes** (the w=1 rule, kept) — a 000 there is my act, disclosed first on every surface that reads it (the QA brief, the note, the panel if Kam is reading).
4. **Briefs to builders carry the launch rule:** a surface that must outlive the session is launched from a script FILE with `setsid`/`nohup`, stdin/stdout/stderr redirected, and its handover row states `sess`/`tty` as measured — "left up" without those two fields is a claim.
5. **Enforcement candidate (w=3 would promote it):** a `pane_close.sh` that takes the pane id + the listener pids from the handover, refuses (rc 5) if any listener or its parent has a tty, and only then `kill-pane`s and re-curls — the check in the path, not in memory.

**Family:** [[2026-08-26_never-delete-cleanup-means-quarantine]] (a close that destroys; the blast radius of a tidy act) · [[2026-08-07_a-check-that-cannot-fail]] (a parentage test asked a survival question) · [[2026-08-14_i-read-representations-they-read-sources]] ("ppid 1" read as "daemonised" — a representation of detachment) · [[2026-08-15_a-gui-open-is-a-write]] (my own action's side effect read as the world's state).

## SHARPENED 2026-09-05 (w=2): the check has TWO halves, and a hand-run check drops one — so it is now a script

**The case.** Closing S33's NexusAI pane: Wednesday ran `ps -o pid,ppid,sess,tty -p <listener>` on the 3111 surface, read tty `??`, and closed the pane. The listener's PARENT (a shell on the pane's tty) was never checked; the pane close hung up the tty; 3111 died with it (listeners 24→23, curl 000). The rule above says "on the listener AND on its immediate parent" — the second half was dropped under load, exactly the failure a two-part manual check invites.

**The mechanism (rule 5, now built rather than a candidate):** `2_Project_Files/fleet/cockpit/pane_close.sh <pane> [port …]` — resolves every listener on the named ports (or every TCP listener whose tty matches the pane's), checks the listener AND its parent for a tty, **refuses (rc 5) if either has one**, otherwise `kill-pane` and re-curls every port. A pane is closed through it or not at all.

