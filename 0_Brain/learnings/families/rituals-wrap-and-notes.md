---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# Rituals, wraps and notes: the daily rhythm and the steps that must not be skipped

**The one idea.** The day has a shape (a morning start, checkpoints, a wrap, a close), and the steps that keep memory intact hang off that shape. A step that depends on someone remembering it is a habit, and habits skip; a step that must not be skipped is bolted to an event that fires anyway. A session that simply goes quiet looks exactly like a session that is working.

## The rules

1. **When planning the day or about to speak aloud:** the day runs from 06:00 (spoken morning briefing, and the natural slot for contemplation and consolidation work, so the briefing is ready when Kam surfaces) to a 23:00 close. Kam framed the times as a starting point, so they are tuneable. No spoken messages before 06:00 or after 23:00 unless something is genuinely on fire. Any machine-local scheduler piece goes on the portability checklist. Note: the quiet hours govern speech only; later lessons in other families make overnight working time. `2026-08-03_daily-rhythm-6-to-23.md`

2. **When the 05:30 shift change fires:** it taps every live fleet pane so that Kam's 06:00 start finds a clean floor (work committed, history written, wrap mail sent, panes free to relaunch fresh), and the 06:00 session verifies the wraps arrived and reports any session that did not wrap. The tap fires once a day and only inside the 05:00 to 05:59 window, so a late fire can never wrap sessions Kam is using. Corrected 2026-08-28: the tap is no longer a wrap order for an agent with a live queue, because overnight is working time; for those agents it is a checkpoint, and the 06:00 verification stays. `2026-08-06_morning-shift-change.md`

3. **When a step must not be skipped (wrap, retro, commit, arming a watcher):** anchor it to an event that happens whether or not anyone remembers: the scheduled shift change or the close bell. Never anchor it to a phrase or to memory. It is not enough for a safeguard to sit in the path of the work; it must sit in the path of something that reliably happens. Sessions ending is not such a thing. `2026-08-10_a-ritual-nothing-triggers-is-not-a-ritual.md`

4. **When creating the daily note:** `git add` it in the same action as creating it. Untracked is worse than uncommitted: a never-added note is invisible to every status habit. `2026-08-10_a-ritual-nothing-triggers-is-not-a-ritual.md`

5. **When a session names its own remaining gap:** give the gap an owner and a date. A named gap with neither is a prediction, not a plan. And when a last-line net (the shift change, the close bell) recovers skipped work, report that as a finding about the system, not as relief. `2026-08-10_a-ritual-nothing-triggers-is-not-a-ritual.md`

6. **When at a checkpoint, about to write a handover, or about to wrap, and Kam may have been on the panel since this seat booted:** run `2_Project_Files/tools/reconcile_rulings.py` in report mode, then `--apply` for this seat's scope only, before writing anything that says what Kam has or has not ruled. His card taps are chat messages; nothing writes them onto the card except that tool, and a run at boot cannot see a tap made later. A handover line about a card's state is written after the reconcile, from a read in the same action. `2026-09-11_a-boot-time-reconciler-cannot-catch-a-mid-session-tap.md`

7. **When a tap is found recorded late:** check the action as well as the record. A late-recorded card may also be an instruction nobody carried out; read Kam's next messages after the tap for what he expected to follow. `2026-09-11_a-boot-time-reconciler-cannot-catch-a-mid-session-tap.md`

8. **During any work:** when a task shows a repeatable pattern (a sequence worth running again, a check always wanted, a delegation shape that worked), note it the same session in the daily note as a one-line workflow candidate. At task end or day end the retro asks "what from today should be systemised?" (a ritual, a launcher or CLAUDE.md line, a script, a workflow definition). Weekly, promote what recurred and retire what did not. A systemised workflow is validated by later evidence, not by having been written. `2026-08-03_workflow-systemisation-duty.md`

9. **When considering adopting a new approach from outside:** adopt it only if it beats what is already run. Novelty is not a reason; regression is a veto. Compare every candidate against current practice first. `2026-08-03_workflow-systemisation-duty.md`

10. **Tuesday seat only. At boot, after the mail check:** sweep every in-scope Datasec feedback store (inventory under `0_Brain/reference/2026-10-12_datasec-feedback-stores/`), report new items by project in the morning receipt, and route each actionable item to its project's agent as a brief item through the normal path (QA gate, merge on the coordinator's GO, deploy only under that project's own grant). Do not stop at telling Kam the feedback exists. Excluded "at the moment", until Kam says otherwise: HPSM-POC, the Security Configuration tool, the MPS Calculator. Feedback from a client human is answered only by Kam. `2026-10-12_boot-sweeps-all-feedback-repositories.md`

## What a tool already enforces

- `2_Project_Files/scheduler/close_wednesday.sh` (the close bell) is the index's enforcing tool for the anchored-ritual rule. The lesson's own text describes the bell as only stamping a line and says it should detect an unwrapped session (blank retro, uncommitted tree, untracked daily note); read the script before relying on what it covers. Adding the daily note to git at creation, and giving a gap an owner and date, are not covered by it.
- Not enforced: the mid-session reconcile (rule 6) is a tool a seat must choose to run; putting it into the watcher's checkpoint legs was named and not built. The Tuesday feedback sweep (rule 10) is carried by the lesson and the pickup line, not yet by the launcher.

## The mistakes this family keeps catching

- A session that did real work and then went quiet, with no wrap, a blank retro and an untracked daily note.
- A watcher or safeguard armed by hand in the morning and off again the next day.
- A handover stating "nothing ruled since X" from a reconcile run hours earlier, while a tap sat unrecorded and unacted.
- A repeatable pattern noticed during work and never written down as a candidate.
- A feedback item or gap reported to Kam as existing, with no route to anyone who will act on it.

## Members

- `2026-08-03_daily-rhythm-6-to-23.md` — The day runs 06:00 (spoken morning briefing; the contemplation/consolidation slot) to 23:00 close. Times are a tuneable starting point. No spoken messages outside those hours unless something is genuinely on fire.
- `2026-08-03_workflow-systemisation-duty.md` — During work note repeatable patterns as workflow candidates in the daily note; at task or day end ask what to systemise; weekly promote what recurred. Adopt a new approach only if it beats current practice; regression is a veto.
- `2026-08-06_morning-shift-change.md` — The 05:30 shift change taps panes to wrap so Kam starts on a clean floor, and the 06:00 session verifies wraps arrived. Since 2026-08-28 the tap is not a wrap ORDER for agents with a live queue (overnight is working time); checkpoint and verification stay.
- `2026-08-10_a-ritual-nothing-triggers-is-not-a-ritual.md` — Anchor any must-not-skip ritual to an event that fires whether or not I remember (shift change, close bell), not to a phrase. git-add the daily note at creation. A named remaining gap gets an owner and a date. 'The net caught it' is a finding, not relief.
- `2026-09-11_a-boot-time-reconciler-cannot-catch-a-mid-session-tap.md` — At each checkpoint and before any handover or wrap: run tools/reconcile_rulings.py (report, then --apply for this seat's scope) before writing what Kam has or has not ruled. Check the ACTION behind a late-recorded tap, not just the card.
- `2026-10-12_boot-sweeps-all-feedback-repositories.md` — Tuesday boot: after the mail check, sweep every in-scope Datasec feedback store and route actionable items to the project's agent. Excluded for now: HPSM-POC, Security Configuration tool, MPS Calculator. Only Kam answers client humans.
