---
date: 2026-11-18
type: family
source: synthesised from the member lessons listed at the bottom; the lessons remain the source of truth and hold the cases
status: live
---
# Launch evidence: proving that something actually ran, where it has to run

**The one idea.** A thing left behind (a log file, a pane, a green tick, a non-zero context reading, a fix committed on my machine) proves that something wrote it. It does not prove that the event I care about happened, that the agent I launched is doing the work I commissioned, or that a fix works on the machine it was written for. The evidence is the line, the pane content or the run on the target that shows the specific event. The same reading discipline tells me when a seat has finished and the floor has room for the next one.

## The rules

1. **When I am about to say "X ran", "X fired" or "X failed because of Y":** open the artefact and find the line that proves that specific event. For a pipeline, find the FIRST failed step and read the outcome of each step (a suite marked skipped never ran and cannot own the red). For a scheduled job, read the log body for the fire-or-skip line and tell a real fire from a test or dry run. The report carries the proving line, not the artefact's name. In reverse: a missing artefact is not proof the event did not happen (it may log elsewhere, or the writer died midway). `2026-08-06_artifact-presence-is-not-execution.md`

2. **When I have just launched an agent and am about to say it is working on the task:** verify at one of the two rungs that discriminate: (a) the pane's content shows the commission was received (it names the ticket, opens the brief, reads the commit under test), or (b) the agent's own outbound artefact exists (boot mail, plan confirmation, report path). Everything below that is not evidence of the commissioned turn: the launcher's exit code (a process started), a pane existing, and a non-zero context reading (A turn ran, not WHICH turn; an agent that booted on the wrong prompt and sat asking a question shows the same reading). A context reading of "none" is informative in one direction only: no turn has run. This corrects the earlier form of the rule, which listed a non-zero context reading as a valid launch receipt. `2026-08-06_artifact-presence-is-not-execution.md`

3. **When I can, put the discriminator in the launcher instead of in my checking:** a launcher that refuses to start unless the prompt names the brief makes a blind agent unlaunchable, not merely detectable. `2026-08-06_artifact-presence-is-not-execution.md`

4. **When I have fixed something for a seat on another machine:** its status is "written, untested" until it has run on that machine, in that machine's context, and I have read the output. Say so in those words. Before handing it over, audit every literal that names a place (path, home directory, user, volume, hostname, terminal, log destination) and ask whether it is true on the machine that will run it; a codebase that has already parameterised one class of pointer is more likely, not less, to hide a straggler in another. Check the order of operations for a fresh seat (a preflight gate must not run before the repair it gates on). `2026-09-16_a-fix-authored-on-one-machine-is-a-claim-until-the-other-machine-runs-it.md`

5. **When a checker says green over a mechanism nobody has run:** find out what the checker compares. A check that compares configuration to a template has no opinion on whether anything executes; prefer a check that observes the mechanism doing its job. When checker and reality disagree, establish which one measures the thing I care about. `2026-09-16_a-fix-authored-on-one-machine-is-a-claim-until-the-other-machine-runs-it.md`

6. **When a failure is unreadable:** fix the layer that hides the diagnosis first. "Never discard stderr" covers the path stderr is written to (a log directory that does not exist swallows the real error), not only an explicit discard at the end of a command. `2026-09-16_a-fix-authored-on-one-machine-is-a-claim-until-the-other-machine-runs-it.md`

7. **When I report back on another seat's work after running it:** the disagreements are the payload. Lead with them, each with its measurement and a positive control; do not soften them. `2026-09-16_a-fix-authored-on-one-machine-is-a-claim-until-the-other-machine-runs-it.md`

8. **When I read a seat's wrap mail (Wednesday seat):** score it and close its pane (`pane_close.sh`) in the same action, never "score now, close later". A wrapped seat with an open pane counts as a live agent to every census. `2026-09-15_a-wrapped-seats-pane-is-closed-in-the-same-action-and-a-floor-deadline-is-checked-by-listing.md`

9. **When a deadline requires "no other agents running" (Wednesday seat; for example an unattended night run with a pane census):** list the panes myself (`tmux list-panes -t fleet:0`) at least ten minutes before and again at the minute; close every wrapped pane, and report any that cannot be closed as a missed deadline. The listing is the instrument; the inbox is not, because a wake that never arrives ends in nothing. A missing wake is recorded in the ledger the moment it is noticed, with the runner log as evidence, not "noted, not diagnosed". An unattended mechanism should state each input it depends on as a gate that refuses with a reason (for example, that the checkout it builds from actually holds the branch tip). `2026-09-15_a-wrapped-seats-pane-is-closed-in-the-same-action-and-a-floor-deadline-is-checked-by-listing.md`

10. **At every boot, checkpoint, seat wrap or send, before choosing the next action:** read the capacity line (`2_Project_Files/fleet/capacity_status.py`). If it says ROOM (1-minute load under 7 and memory free at least 25%), the next action is launching the next lane that shares no file with a running one, or commissioning a lane sweep if none is staged, before any lower-value work. If it says FULL, say which limit (load or memory) and do not launch. Launch in waves at least 3 minutes apart. A wrap frees a seat: read capacity in the same action as scoring and closing. While the floor is full, keep the next brief drafted so ROOM never waits on drafting. The morning card carries the day's capacity summary. Unchanged by this rule: no two seats on one file, the signature classes, the QA gate, the routing table. `2026-10-28_track-agent-capacity-keep-the-floor-full.md`

## What a tool already enforces

No member's index row names an enforcing tool. The lessons mention helpers: a launch wrapper that refuses a prompt not naming the brief, and the capacity line printed on every send and at every boot. Both are aids as far as the index records; the pane-close-on-wrap census is named in its lesson only as an enforcement candidate, not built.

## The mistakes this family keeps catching

- A file exists, so the event it is named after is reported as having happened.
- A red run is blamed on the step with the loudest name instead of the first step that failed.
- An agent is reported as working because its pane is alive or its context reading is above zero.
- A fix is called done from the machine that wrote it, where every hardcoded path happens to be right.
- A green configuration check stands in for a mechanism that never executes.
- A deadline is hung on an event (a wake, a mail) instead of on a reading taken at the deadline.

## Members

- `2026-08-06_artifact-presence-is-not-execution.md` — Before claiming X ran, fired or failed: find the line proving that event (first failed step, outcome, fire vs skip, real vs dry-run), not the artifact's existence. After a launch, non-zero ctx proves only A turn ran; check pane content or the agent's mail.
- `2026-09-15_a-wrapped-seats-pane-is-closed-in-the-same-action-and-a-floor-deadline-is-checked-by-listing.md` — When reading a wrap mail: score and pane_close.sh in the same action. Before any 'no other agents' deadline, list the panes (tmux list-panes -t fleet:0) 10 minutes before and at the minute, close wrapped ones; never rely on a wake arriving.
- `2026-09-16_a-fix-authored-on-one-machine-is-a-claim-until-the-other-machine-runs-it.md` — When I fix something for a seat on another machine: it is 'written, untested' until run there. Audit every literal naming a path, home, volume, host or log; prefer checks that observe the mechanism running; lead reports with disagreements.
- `2026-10-28_track-agent-capacity-keep-the-floor-full.md` — At every boot, checkpoint, seat wrap or send: read the capacity line first. If ROOM (load1 under 7, memory free 25%+) launch the next disjoint lane before lower-value work; if FULL say which limit and do not launch. Keep the next lane staged.
