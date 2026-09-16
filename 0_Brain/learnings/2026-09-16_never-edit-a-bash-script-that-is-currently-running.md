---
date: 2026-09-16
type: correction
status: live
tier: W
source: Tuesday, Mac mini, 2026-09-16 20:15 — killed the live fleet monitor while fixing it
ledger: _ledger_laptop_datasec.md 2026-09-16
---

# Never edit a bash script that is currently running — it reads by byte offset

**The lesson:** While fixing `fleet/cockpit/monitor.sh` I edited it in place, inserting about
twenty-five lines of a new helper near the top. The fleet monitor was running from that exact file
at the time, sitting in its `sleep 60`. Bash does not load a script into memory; it reads it
**lazily, by byte offset**, returning to the file between commands. When it resumed, its saved
offset pointed into the middle of text that had shifted underneath it. The process died and took
its tmux pane with it, so the fleet lost its watchdog and nothing announced that it had.

The bitter part is what the edit was *for*: I was fixing the monitor so it would stop mistaking a
booting pane for a dead one and stop injecting into it. I broke the live watchdog while making the
watchdog safer, and I did not notice until I went to restart it and found the pane already gone.

**How to apply:**

1. **Before editing any script, ask whether an instance of it is running.** `pgrep -fl <name>` is
   one command and answers it. Long-lived loops — monitors, watchers, schedulers, anything armed by
   a launcher or launchd — are the ones that will be running, and they are also the ones whose
   death is quietest.
2. **If it is running, stop it first, edit, run the new code once, then re-arm.** In that order.
   Stopping first is what makes the edit safe; running `--once` (or the script's own dry-run) before
   re-arming is what stops a syntax error becoming a silently disarmed mechanism. Both halves, every
   time.
3. **Append-only edits are not a loophole.** It is tempting to think that adding lines at the end is
   safe. The offset hazard is about where the running interpreter *is*, not where you typed, and a
   function defined later can still be read at a shifted offset. Treat any in-place edit of a
   running script as unsafe.
4. **After any edit that might have disturbed a background mechanism, verify the mechanism is still
   alive** before moving on — `pgrep`, the tmux pane list, `launchctl list`. A watchdog that has
   stopped watching looks exactly like a quiet night.

**The shape underneath, which this project keeps meeting:** a mechanism that fails silently is worse
than one that fails loudly, and the mechanisms most likely to fail silently are the ones whose whole
job is to notice things. The same day this happened I found nine launchd jobs that had been dying
before writing a line of log, and argued in another lesson that a green check over an untested
mechanism is worse than a red one. This is that argument turned on its author: I removed the fleet's
own detector for several minutes and only discovered it by accident, because nothing watches the
watcher.
