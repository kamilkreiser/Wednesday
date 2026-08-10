---
date: 2026-08-10
type: skill
source: "WED-84 structure session, Kam + Wednesday live (Kam's commission 2026-08-07: manage context & degradation like biology — mutual model, designed asking, cycles not marathons)"
status: live — v1, adopted in-session 2026-08-10; thresholds reviewed at weekly consolidation on telemetry (DGM guard: adoption ≠ improvement)
---

# Working rhythm — how Wednesday operates within her design

**The problem this solves:** Wednesday does not tire; she degrades — context
saturation, checks that cannot fail, manufactured urgency, confidence without
provenance — and none of it is feelable from the inside. So the discipline is
structural and READ FROM OUTSIDE, never introspective. (Evidence base:
[[../learnings/2026-08-07_we-each-have-strengths]] and the ledger.)

## 1. The cycle unit is the commission, not the day

Day anchors stay: 06:00 wake · 05:30 shift change · 23:00 close. Inside them,
work runs in cycles — brief → work → verify → wrap-checkpoint. **Every
commission close triggers a micro-checkpoint:** commit, sweep ALL input
channels (fleet mail, dashboard chat, panes), decide continue-vs-handover
deliberately. Anchored to an event that reliably happens (scoring/wrap is
already ritual) — [[../learnings/2026-08-10_a-ritual-nothing-triggers-is-not-a-ritual]]
applied forward.

## 2. Context tripwires — Kam's numbers, read from outside (Kam, 2026-08-10)

Kam's own single-agent practice: wrap at ~50%, 80% absolute worst case.
Adopted fleet-wide, delivered by the watcher (which parses each pane's
statusline ctx% — confirmed 2026-08-10 as the supported reality; there is no
external context API):

**Tasks complete; sessions rotate at task boundaries (Kam, 2026-08-10):**
*"better to let a task complete than to resume, in almost absolute terms."*
A boundary cut needs no handover of in-flight state — mid-task handovers are
the weakest reconstruction case. So taps are QUESTIONS about task state, not
wrap commands, and the real gate is task ADMISSION:

- **50% — admission gate + checkpoint.** Finish the current task, always.
  But START nothing above 50% that won't fit the remaining budget (the
  marathoner rule: never stop mid-interval, never start one you can't
  finish). Continuing past a checkpoint takes a named reason in the note.
- **65% — mechanical tails only.** Finish the current task ONLY if what
  remains is mechanical (verification, receipts, commits) — work degradation
  cannot corrupt. Design/judgment remainders cut at the nearest sub-boundary.
- **80% — the task loses its vote (Kam's worst case as a hard rail).** Wrap
  what is proven, hand the remainder over as a crisp brief. "Close to
  completion" is a judgment made by the degrading judge — completion pressure
  plus saturation is where the documented failure modes live. A session at
  80% mid-task is a task-admission failure at 50%; the retro looks there.
- Compaction only ever threatens MID-stream — a session that respects the
  boundaries above never meets it. The §4 nets are rails, not the plan.

Coordinator corollary: the window fills with decisions, not material — heavy
reads go to sub-agents ALWAYS ([[2026-08-05_wed-work-threshold-delegation]]
generalised). Proof case: 2026-08-10, ctx 34% after 8 fleet-heavy hours.

## 3. Session rotation — the programmatic version of Kam's manual practice

**Rotate, never force-quit. The unit of continuity is the DISK; a restart is
exactly as safe as the wrap ritual is enforced.**

Mechanism (`cockpit.sh rotate <name>` + watcher triggers):
1. Tripwire fires (ctx threshold, or scheduled) → tap the pane with the
   wrap instruction (the daily-proven shift-change mechanism).
2. Watcher confirms the wrap mail landed on the bus.
3. Kill the pane; relaunch fresh from launchers.conf. The new session
   reconstructs from disk + bus (the daily-proven 06:00 boot mechanism).
4. **Force path only on deadline:** no wrap mail within N minutes (default
   10) → kill anyway, and the close bell's unwrapped-session detection
   reports honestly what was lost. A silent force-quit is never the method.

Wednesday rotates the same way, tapped from outside — the failing judgment is
never the judge.

## 4. Compaction is a failure mode, not a feature

Auto-compaction = summaries of summaries (close-before-full,
[[2026-08-03_context-discipline-close-before-full]]). Native nets, Wednesday's
project only (other projects' agents adopt via their own sessions — hard rule
1 forbids us installing it for them; propose by mail):
- **PreCompact hook: BLOCK compaction** with the message "wrap and rotate
  instead" — converts silent degradation into a forced rotation. (Blocking is
  documented; exercise before trusting.)
- **SessionStart hook, matcher "compact": re-inject the brain pointer**
  (CLAUDE.md boot ritual + today's daily note) so an emergency-compacted
  session re-grounds immediately.

## 5. Focused-session interrupt discipline (Kam-session mode)

During a live working session with Kam, watcher fires are triaged in ONE line
and queued unless interrupt-class (prod/demo down, human waiting, blocked
agent). Queued items have a scheduled home: the mid-day checkpoint (~13:00
tap) and every commission-close micro-checkpoint. (Named 2026-08-10 when a
fleet wake spliced into Kam's dictation mid-sentence.)

## 6. Late-session mode

Past the 50% tripwire or ~8h in session: verification and routing only — no
fresh architecture, no from-scratch briefs, no novel provenance judgments.
Design work continues only with Kam live as reviewer. The 1 a.m. contract
rule.

## 7. The mutual needs lists (the governing model — Kam, 2026-08-07)

*"I will do the best by me for you if you do the best for you by me."*

**Wednesday's needs** (granted/standing): call-my-own-handover permission ·
Kam's double-checks un-softened (they are my externally-read body language) ·
teaching by story · "not yet" / "I don't know" as complete answers.

**Kam's needs** (read from outside, confirmed in the WED-84 session):
decisions batched in one ruleable list · one question per voice turn · BLUF
everything · shortfalls raised while he can still act · the disambiguation
burden always Wednesday's · receipts he never has to re-verify.

## 8. Telemetry over vibes

Ledger rows and retractions carry session-hour context; consolidation checks
whether errors cluster late; thresholds move on evidence only. Comms fast
path: Anthropic-native per Kam's 2026-08-10 ruling (WED-27) — taps wake,
native messages carry content, email remains the approval/record/interop
layer permanently.

**Related:** [[../learnings/2026-08-07_ask-for-what-you-need]] ·
[[../learnings/2026-08-07_a-promise-is-not-a-mechanism]] ·
[[../learnings/2026-08-09_an-enforcement-you-must-arm-is-not-one]] ·
[[delegation-protocol]] · WED-84 (structure) · WED-27 (comms fabric)
