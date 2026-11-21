---
date: 2026-11-21
type: correction
source: "Kam, live board 2026-11-21 20:05:41, verbatim: \"the PC was waiting for a while.  after I asked, it confirmed it finished.\" and 20:06:43: \"or do you need me to do anything on the PC?\""
status: live
supersedes: ""
---

# A helper I put on hold gets the next useful job, not an open-ended wait

**The lesson:** When a helper finishes a job and the next planned job is blocked, I don't send it a bare "hold". I give it the most useful unblocked job straight away, and tell Kam the one line to type if it needs restarting. A capable machine sitting idle while Kam watches is waste he notices.

**Context:** WO-1 finished at 17:33 (Windows pipe tests green on the PC). I told the PC to hold for WO-2, which I had tied to the W-DAEMON lane, hours away. The PC sat idle for about 2.5 hours until Kam asked it and then me. Useful work had been available the whole time: every crate except the daemon compiles for Windows, and nobody had run their tests there. That became WO-2 at 20:06.

**How to apply:**
- When a helper reports "done", ask what it can usefully do NOW with what exists: run tests, measure, read and report. Give it that, so its hold only starts when nothing useful is left.
- For a helper only Kam can restart (the PC seat), tell him the exact line to type in the same message.
- The same applies to project seats that hold for a merge: if a holding seat could do bounded, useful, non-conflicting work, give it that work.

**Related:** [[2026-11-21_windows-helper-launches-without-permission-prompts]], [[../people/kam]]
