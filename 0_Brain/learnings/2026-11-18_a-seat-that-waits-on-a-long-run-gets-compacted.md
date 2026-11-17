---
date: 2026-11-18
type: lesson
source: Friday's overnight build coordination, CoAgent, 2026-11-17 to 18: three idle compactions across two build seats, each seen on the pane
status: live
tier: M
---

# A seat that waits past the prompt cache on a long run gets compacted: its brief says what to re-read, and the coordinator sends a re-read line the moment the pane shows it

**The operative case.** A build seat has started a run that takes longer than about an hour (a full check, a five-run test, a hundred red-control rows) and ends its turn to wait for it. **Expect the host to compact that seat's context while it is idle.** The pane then shows a line saying it was compacted while idle and names the setting that turns this off. From that moment the seat's closing report, the part a check and an owner read, would be written from a summary.

**What happened.** On the night of 17 to 18 November the daemon seat was compacted twice and the permission-gate seat once, always while holding for a long run of their own. Nothing else showed it: the idle alert looked like every other "waiting on its own run" alert, except that once the usual note about a live background shell was missing. Friday saw it only because she read the pane on every alert and did not acknowledge by habit. Each time she sent one line, naming the seat's addendum, telling it to re-read the addendum and its own status section whole before writing anything more, and not to start a second run. The seats' reports afterwards were coherent; whether they would have been without the line is not measured.

**How to apply:**
1. **Every build brief carries the sentence** "after any context compaction, re-read this brief and your own STATUS file WHOLE before you write anything more". The two briefs of 18 November have it. It costs one line and does not depend on the coordinator being awake.
2. **Read the pane on every idle alert.** An acknowledgement without a look would have hidden all three. The pane line is the only signal.
3. **The remedy line names the seat's brief or addendum** (a seat is told to act on nothing else at its prompt), says what to re-read, and says whether a run of the seat's own is still alive, measured by `ps`, so it does not start a second copy.
4. **A seat reports its long runs' results into its STATUS file as each ends**, not only in its head: then a compaction loses nothing that matters. Ask for "update STATUS at least every 20 minutes" and check the file's time, not the pane.
5. **Whether to turn idle compaction off for build seats is a settings change and the owner's choice.** Friday has not changed any seat's settings. It is on the list for Kam.

**Family:** [[2026-08-03_context-discipline-close-before-full]] (never work on summaries of summaries; here the summary was imposed while the seat slept) · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (the brief sentence is the in-path form; the coordinator's line is the backstop) · [[2026-08-06_artifact-presence-is-not-execution]] (an idle alert says a turn ended, not what state the seat is in).
