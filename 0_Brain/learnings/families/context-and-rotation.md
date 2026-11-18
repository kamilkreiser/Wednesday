---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# Context and rotation: working inside a finite window and handing over before it fails

**The one idea.** A session's context window is finite and a session cannot feel itself degrading, so the window is read from an instrument (the statusline percentage), work is closed and written to disk before it fills, and the seat hands over to a fresh one at a numeric band instead of on judgement. Rotation is a routine, self-run act that must never stall the fleet, kill itself, or be confused with retiring a seat that has already wrapped. Compacted context is summaries of summaries: never work from it without re-reading the sources.

## The rules

1. **During any session:** treat the conversation as a scratchpad and the drive as the memory. Everything durable goes to disk the same session, so a fresh session can rebuild from disk alone. Close and wrap at task boundaries, before the window fills; never push on through compaction. With a large task left in a deep session, write the handoff and recommend a fresh session instead of degrading silently. `2026-08-03_context-discipline-close-before-full.md`

2. **When briefing a sub-agent or delegated agent:** one scoped task, a fresh window, the result distilled to a file; never chain raw agent transcripts. Never brief a task that cannot be closed or cleanly checkpointed in one session: big work is a series of bounded briefs with handoffs on disk. `2026-08-03_context-discipline-close-before-full.md`

3. **When deciding how much context to give an agent:** load it fully by default; under-briefing is the expensive failure. For harder work narrow the job (a more specialised agent with a tight purpose), not the context. Cite file paths, not pasted copies, because paths stay current. Vary loading only when a situation demands it (a huge corpus, an agent near its window, context that actively misleads). `2026-08-03_context-loading-split.md`

4. **On the coordinator's own boot cost:** the full load stays; it is what makes a cold session be this assistant. Kam's ruling of 2026-08-10: no merging or cutting of lessons until a system is found that keeps the best result and reduces load, so any reduction proposal must come with evidence that nothing is lost. Boot cost (number and trend) is a standing item at every weekly consolidation. `2026-08-03_context-loading-split.md`

5. **When a context wake lands ("ctx at NN%"):** read my own statusline percentage (capture my own pane) and obey it. It is the instrument of record; the harness token-budget counter is a session budget, not the window. If the reading disagrees with a belief, the belief loses. `2026-09-02_the-statusline-is-the-context-instrument.md`

6. **The thresholds (current form).** 50% and 70% are checkpoints only: refresh the handover block, declare the default, start nothing heavy, do not rotate. 80 to 90% is the rotation band: rotate at the first safe boundary inside it, unprompted, without asking Kam. Past 90% nothing new is started. This is Kam's ruling of 2026-09-07 and it wins over the earlier "rotate at 70%" grant and the "70% = rotate now" rule (`2026-09-02_rotate-in-the-70-80-band-conditionally.md` over `2026-08-21_auto-rotate-at-70pct.md` and over rule 2 of `2026-09-02_the-statusline-is-the-context-instrument.md`; the "70-80" in the first file's name is dead).

7. **What "safe boundary" means:** no agent question unanswered or imminently due; no thread with Kam left dangling (finish it or state the handover in it); everything durable and pushed (daily note with handover, ledger rows, HEAD equal to origin, wrap mail sent); agent sessions left running untouched, the rotation touching my pane only; and never mid-task: finish the current task to a boundary first. `2026-08-21_auto-rotate-at-70pct.md`

8. **When a seat is already dead at its context limit:** that is the only unconditional respawn. It is respawned from outside by the rotation script's dead mode; it is never tapped, because a tap to a seat that cannot act is logged as delivered and achieves nothing. `2026-09-02_the-statusline-is-the-context-instrument.md`, `2026-09-02_rotate-in-the-70-80-band-conditionally.md`

9. **When Kam rules a number that lives in both a lesson and a mechanism (boot prompt, watcher, launcher):** update the mechanism first, in the same action; it is the copy that will be obeyed. And with more than one coordinator seat, "read Kam's rulings first" is blind to rulings given on the other seat's panel: they arrive only if that seat writes them where the other reads. `2026-09-02_rotate-in-the-70-80-band-conditionally.md`

10. **Wednesday seat. When near or inside the band with agents live:** rotation is not gated on the floor being clear. Delegate before the band (by about 60%, anything too heavy for the seat goes to an agent or drafting subagent), put everything in flight under a brief with a named wake path, write the handover naming every live agent and what wakes each, then self-rotate with the agents running. Never idle waiting for Kam to launch the successor. Record the pane list before and after; the successor's first act is to compare them. Report the rotation, do not request it. This removes "no agents live" from the safety conditions; the other conditions in rule 7 stand. `2026-09-13_rotation-never-blocks-the-work-delegate-then-rotate.md`

11. **Wednesday seat. Before running the cockpit's rotate on any seat:** ask whether the seat has already sent its wrap mail. No: rotate is the right tool. Yes: retire it by hand. Verify the wrap on disk first (handover file, top history entry, repository state), since a wrap mail is a claim and the files are the evidence; then kill the pane and launch afresh. Rotating a wrapped seat forces a second end-of-session ritual, which double-posts to client tickets, or force-kills with a false alarm. Never run two sessions on one project: confirm the old process is gone before launching. `2026-09-18_rotate-is-for-an-unwrapped-seat.md`

12. **When ordering or running a rotation from inside the seat's own pane:** an unpatched rotate kills the pane its own shell lives in before it relaunches. The script now hands the kill and relaunch to a detached helper when it detects this. Either way, about two minutes after any rotation, list the panes and read the rotate log: a lone "tapped, waiting" line with nothing after it means the seat is gone, so relaunch the lane. `2026-10-12_a-rotate-run-inside-its-own-pane-kills-itself.md`

13. **Wednesday seat. When a seat is launched by a rotation (self or dead mode) and the preflight fails hard:** the failure never stops the launch. It is logged and placed at the top of the new seat's boot prompt as first work, fixed before the brain load, then the preflight is re-run. It is still a failure, just not a stop. A human launch still asks "continue anyway?". General form: a gate that needs a human answer must never sit in an unattended path. When Kam names a cause, check which line actually failed before fixing the named thing. "Pane present" is not "seat booted". `2026-11-16_preflight-failure-must-not-kill-a-rotation.md`

14. **At boot, before reading the files the boot mandates whole:** measure every one of them (bytes) and read the statusline before and after the first big read; two readings give the real cost, one gives nothing. Report the numbers in the boot note. Never silently under-read: say what was bounded and why. Never inherit a predecessor's subset without re-deriving its arithmetic. `2026-09-08_the-boot-spec-outgrew-its-window.md`, `2026-09-18_the-boot-spec-outgrew-the-context-window.md`

15. **Whether to read whole or bounded: the two boot lessons disagree and neither names the other as loser.** The 2026-09-08 lesson, after its own correction, measured the window on the statusline, found the full read landed near 40%, and made "read both whole; trim only against a measured ceiling" the default. The 2026-09-18 lesson (Wednesday seat) estimated the mandated reads at bytes divided by four, judged them larger than the window, and says to bound by structure (the live head of a superseded-block file, a digest's headline index, a ledger's newest rows). Taking the newer as the winner where they differ: when the measured sum is a large fraction of the window, bound by structure and say so. What both agree on is rule 14, and that a file breaking its own stated discipline (appended where it says "replace", unarchived where it says "archive") is fixed, not obeyed. Check the decision queue before treating a recurring measurement as a discovery. `2026-09-18_the-boot-spec-outgrew-the-context-window.md`, `2026-09-08_the-boot-spec-outgrew-its-window.md`

16. **When a build seat waits on a run longer than about an hour:** expect the host to compact it while idle. Every build brief carries "after any context compaction, re-read this brief and your own STATUS file whole before you write anything more". The seat updates its STATUS file at least every 20 minutes and as each long run ends; check the file's time, not the pane. The coordinator reads the pane on every idle alert (the pane line is the only signal) and, on seeing a compaction, sends one line naming the seat's brief or addendum, what to re-read, and whether the seat's own run is still alive (measured with `ps`) so it does not start a second copy. Turning idle compaction off is a settings change and Kam's choice. `2026-11-18_a-seat-that-waits-on-a-long-run-gets-compacted.md`

## What a tool already enforces

- `2_Project_Files/fleet/cockpit/wednesday_rotate.sh`: the self-rotation refuses unless HEAD equals origin and the tree is clean, so the handover cannot be skipped; its dead mode re-checks the "context limit" literal before killing and respawns from outside. Not covered: a dead-mode respawn loses whatever was not yet written to the note, and choosing the safe boundary is still the seat's judgement.
- `2_Project_Files/fleet/cockpit/cockpit.sh`: a rotate run from inside its own pane hands kill and launch to a detached helper. Not covered: it does not refuse to rotate an already-wrapped seat (owed, not built), and the two-minute pane check remains manual.
- `Launch_Wednesday.command`: in rotation mode a hard preflight failure is carried into the boot prompt and logged. Not covered: the liveness check can pass a seat that is still in its launcher.

## Grants and their limits

- **Self-rotation without asking (Kam, 2026-08-21; band moved to 80 to 90% on 2026-09-07):** only at a safe boundary. Standing.
- **Rotate with agents live, and keep launching every disjoint lane (Kam, 2026-09-13, Wednesday seat):** standing. Kam keeps: lesson cutting or merging, the digest's design, and compaction settings.

## The mistakes this family keeps catching

- A correct instrument reading explained away by a flattering belief about the window.
- A seat idling at its ceiling, waiting for permission or a clear floor, while agent mail goes unread.
- A rotation ordered and assumed done, when the pane simply vanished.
- A wrapped seat "rotated", making it wrap and post twice.
- A boot instruction obeyed past the point the files fit, or quietly skimmed without saying so.
- A report written from a compacted summary after a long idle wait.

## Members

- `2026-08-03_context-discipline-close-before-full.md` — Close and wrap tasks before the context fills; never push on through compaction. Write durable state to disk at once. With a big task left in a deep session, write the handoff and recommend a fresh one. Never brief a task that cannot close in one session.
- `2026-08-03_context-loading-split.md` — Load sub-agents with full context by default (under-briefing is the costly failure); narrow the JOB, not the context; cite file paths, not pasted copies. Boot cost is reviewed each weekly consolidation; cut or merge lessons only with proof nothing is lost.
- `2026-08-21_auto-rotate-at-70pct.md` — When context reaches the rotation band (now 80-90%, no longer 70%): wrap and rotate myself at the next safe boundary without asking Kam, only if no agent question is open, no Kam thread dangles, everything is pushed, agents untouched. Never mid-task.
- `2026-09-02_rotate-in-the-70-80-band-conditionally.md` — On a ctx wake: 50% and 70% are checkpoints only (refresh handover, start nothing heavy, do NOT rotate). Rotate at the first safe boundary inside 80-90%; nothing new past 90%. Only a dead seat is respawned unconditionally. Change the mechanism first.
- `2026-09-02_the-statusline-is-the-context-instrument.md` — When a ctx wake lands: read my own statusline ctx% (tmux capture-pane) and obey it; the harness token-budget counter is not the window. A seat dead at its context limit is respawned from outside by wednesday_rotate.sh --dead, never tapped.
- `2026-09-08_the-boot-spec-outgrew-its-window.md` — At boot: measure the digest and ledger sizes and read ctx% before and after the first big read. Default is to read both WHOLE (about 40 percent measured); trim only against a measured ceiling, say what was dropped, never inherit a predecessor's subset.
- `2026-09-13_rotation-never-blocks-the-work-delegate-then-rotate.md` — When near the rotation band with agents live: delegate everything in flight under a brief with a wake path, write the handover, self-rotate. Never idle waiting for Kam to launch the successor; record pane list before and after.
- `2026-09-18_rotate-is-for-an-unwrapped-seat.md` — Before cockpit.sh rotate: ask whether the seat already sent its wrap mail. If yes, verify wrap on disk (handover, history), tmux kill-pane and cockpit.sh launch by hand; never rotate a wrapped seat (second ritual double-posts); one session per project.
- `2026-09-18_the-boot-spec-outgrew-the-context-window.md` — At boot: stat every file mandated whole-read and sum bytes (divide by 4 for tokens) BEFORE reading. If near the window, bound by structure (live head, headline index, newest rows), say what was bounded, and report the measurement in the boot note.
- `2026-10-12_a-rotate-run-inside-its-own-pane-kills-itself.md` — When ordering or running cockpit.sh rotate from inside the seat's own pane: the patched script hands kill+launch to a detached helper. Two minutes after any rotation, list panes and read rotate.log; a lone 'tapped, waiting' means relaunch.
- `2026-11-16_preflight-failure-must-not-kill-a-rotation.md` — When a seat is launched by a rotation (--self or --dead): a hard preflight failure never stops it. Log it, put the failures at the top of the new seat's boot prompt as first work, and fix them first. A human launch still asks to continue.
- `2026-11-18_a-seat-that-waits-on-a-long-run-gets-compacted.md` — When a build seat waits on a run over an hour its context gets compacted: every brief says re-read the brief and STATUS whole after compaction; read the pane on every idle alert; send a re-read line naming the addendum; STATUS updated every 20 min.
