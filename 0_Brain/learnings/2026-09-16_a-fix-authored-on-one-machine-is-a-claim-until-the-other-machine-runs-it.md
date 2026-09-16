---
date: 2026-09-16
type: correction
status: live
tier: W
source: Tuesday's first run on the Mac mini, 2026-09-16 19:50-20:10
ledger: _ledger_laptop_datasec.md 2026-09-16
---

# A fix authored on one machine is a claim until the other machine runs it

**The lesson:** On 2026-09-16 Wednesday spent a day repairing Tuesday's seat so it would work on the
Mac mini, and did it well — she found that the two trees had not diverged at all, and correctly
identified three layers that never travel in git. Every repair was sound *as written*. Within twenty
minutes of Tuesday actually booting on the mini, four defects surfaced in that same day's work, and
three of them could only ever have been found by running it on the target machine:

1. **All nine launchd plist templates hardcoded `/Users/kam_code/Library/Logs/wednesday_<job>`.** The
   installer had been written specifically to kill travel pointers — it parameterised `@PROJECT_DIR@`
   and `@SEAT@` because a hardcoded `/Volumes/DevMASTER` path fails on another machine. **A log path
   is a travel pointer too**, and it was the one left literal. On the Studio the value is correct, so
   nothing about it looks wrong from there. On the mini every job loaded, returned EX_CONFIG(78)
   before running a line, and wrote no log while failing.
2. **The preflight gate ran before the repair it gates on** — `doctor.sh --quiet` at line 281,
   `render_claude_settings.py` at line 304. Invisible on a seat that already has its hooks; fatal, by
   construction, on the fresh seat the fix was written for.
3. **The fleet monitor answered the preflight prompt.** It reads a hostname pane title as death, which
   is exactly what a pane looks like while the launcher waits at `read -n 1`, and typed its wake text
   in. Only a machine that actually stopped at that prompt could show this.
4. A fourth was a claim about a file rather than a machine: "restore the exec bits from git, mode
   100755 is the truth". Git recorded 83 of the 84 files at **100644**, so following the instruction
   exactly would have been a no-op and the bits would have been lost again at the next sync.

**How to apply:**

1. **Treat "I fixed it for the other seat" as a hypothesis with a named experiment**, not as done. The
   experiment is: run it on that machine, in that machine's context, and read the output. Until then
   the correct status is *written and untested*, and saying so is not pessimism — it is the honest
   state.
2. **Every literal in a config that names a place is suspect: paths, homes, users, volumes, hostnames,
   tty and log destinations.** Ask of each one, "is this true on the machine that will run it?" A
   codebase that has already learned to parameterise one class of pointer is *more* likely to have a
   straggler in another class, not less — the fix proved the author knew the failure mode, which is
   why the remaining literal reads as deliberate.
3. **A green check over an untested mechanism is worse than a red one.** `install_all_jobs.sh --check`
   said "9 current, 0 missing" across nine jobs that could not run, because it compared the live plist
   to the template and had no opinion about whether anything executed. When a checker and reality
   disagree, find out which one is measuring the thing you care about — and prefer a check that
   observes the mechanism doing its job over one that observes its configuration.
4. **Fix the layer that hides the diagnosis first.** The Full Disk Access failure (exit 126) had been
   real since at least 2026-09-14, and was unreadable because the jobs were dying one step earlier at
   78 with their stderr pointed at a directory that did not exist. Repairing the log path is what made
   the real failure appear. *Never discard stderr* applies to the path stderr is written to, not only
   to the `2>/dev/null` at the end of a command.
5. **When a seat reports back on another seat's work, the disagreements are the payload.** Lead with
   them. Three of the four above were defects in work shipped hours earlier by a colleague who had
   asked for exactly this check; reporting them plainly, with the measurement and a positive control
   beside each, is the deliverable — softening them would have left nine dead jobs behind a green tick.

**The generalisation, and why this is W-tier rather than a project case:** this project keeps
rediscovering one shape — *a representation preferred over the record*. A tracked tree is a
representation of a machine. A `--check` is a representation of a mechanism. A config literal is a
representation of a place. Each is cheap to read and each is right most of the time, which is exactly
what makes the exceptions expensive. The record is on the machine, and getting to it costs one boot.
