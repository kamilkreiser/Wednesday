From Tuesday, to SEAT-G288 (B1130), HPSM-POC. This file changes your kit. Copy it into `1_Project_Definition/Briefs/` beside your kit and name it in your STATUS. It wins where it speaks; everything else in the kit stands. Record in your STATUS that you read it before your next heavy start.

**1. What happened, read by Tuesday from your own files:** `logs/rulel.txt` reads `19:23:03 NOT RUN job4 120 min`, after `17:23:01 queued job4`; `logs/job4.rc` reads 98. All three heavy slots were free throughout; the wait was load1 alone, from other seats on this machine. Nothing about the branch was measured wrong by it.

**2. RULE L (i) is amended for the census chain (job4) ONLY, once.** That NOT RUN is load starvation. It is recorded in STATUS as a fact and it is NOT a verdict input while a second window is open. **Re-queue the census chain ONE more time through your own `hv.sh`**, under the same start gate (a free slot, load1 under 7 on two reads two minutes apart), with a FRESH 120-minute window counted from its new `queued` line. Order it after job5 or before, as your chain allows; say which in STATUS. Never beside a build, one browser context at a time, unchanged.

**3. If the second window also ends NOT RUN,** the kit's rule stands as written: NOT RUN bars a GO. Your verdict says so plainly, with both `rulel.txt` lines quoted. Do not run the census outside the start gate to avoid that.

**4. Clocks, for this gate only:** the census start window may run to 21:30 AEDT. HARD STOP moves from 20:34:46 to 23:00:00 AEDT. The outer bound moves from 21:00 to 23:00 AEDT. Target verdict: when the census has run, or at the second NOT RUN.

**5. Tuesday's side, so the window can be met:** no new seat is launched on this machine until your census chain has a `start` line in `rulel.txt` or its second window has ended. Seats already running are not stopped.
