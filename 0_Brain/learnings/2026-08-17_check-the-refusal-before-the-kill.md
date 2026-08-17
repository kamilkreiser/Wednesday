---
date: 2026-08-17
type: correction
source: "w=2: 2026-08-14 (path-gate refusal + chained kill-pane/launch left a fresh agent briefless) and 2026-08-17 (freshness-gate refusal, same chain, same result — s41 booted toward an inbox holding only a SCORE). Both self-caught within a minute; both cost only the send-fix race against the boot."
status: live
---

# Check the refusal before the kill — never chain a destructive step after a step that can refuse

**The operative case:** I am about to run, in ONE action, a step that can REFUSE (a gated
send, a validated write, anything with a non-zero exit path) followed by a step that is
DESTRUCTIVE or irreversible-in-the-moment (kill-pane, launch, deploy, delete). **Split them.
The destructive step runs only after the refusable step's success is verified.**

**Why the rule keeps losing to convenience:** the batch is faster to write, and the gates
pass most of the time — so the chain feels safe precisely because the gate is good. But the
gate's whole purpose is the rare refusal, and the chain converts every refusal into a
second incident: the send fails AND the fresh agent boots briefless, turning one fix into a
race against the boot ritual.

**How to apply:**
1. Gated send → verify at the destination → THEN kill/launch. Three actions, not one.
2. The same split applies to any refuse-capable step: preflight → check rc → destructive.
3. If the chain has already fired and the refusable step failed: fix and re-send FIRST
   (the booting agent reads mail at boot end — the brief usually wins the race), and say so.

**Related:** [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (a gate people route
around or race is not protecting), [[2026-08-06_never-discard-stderr]] (the refusal is
output; consuming it is the point), [[_ledger]]
