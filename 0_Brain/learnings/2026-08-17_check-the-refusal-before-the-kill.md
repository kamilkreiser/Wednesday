---
date: 2026-08-17
type: correction
source: "w=2: 2026-08-14 (path-gate refusal + chained kill-pane/launch left a fresh agent briefless) and 2026-08-17 (freshness-gate refusal, same chain, same result — s41 booted toward an inbox holding only a SCORE). Both self-caught within a minute; both cost only the send-fix race against the boot."
status: live
tier: M
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


## EXTENSION 2026-09-08 — a VERIFIER is a step that must be gated too, and it fails as a FALSE ALARM

**The operative case, added because a verifier feels safe by definition and so nobody sequences it:**
you have just run an action that can fail, and a verification block runs next **unconditionally**.
**If the action did not happen, the verifier reports on the PREVIOUS state — and its output looks like
a finding.**

**The case (Secuura s151).** `python3 -c "..." H="$X"` passes `H=` as a **script argument, not an env
var**, so the payload file was never written and curl failed. The verification block then read the
**unmoved `origin/develop`** as though it were the merge commit and printed **`⚠ TREE MISMATCH`** —
output identical to a corrupted merge, from a merge that never happened. Acting on it would have meant
investigating a corruption that did not exist.

**The seat's formulation, adopted: *a verifier that runs unconditionally after a failed action reports
on the wrong object.***

**Why it belongs in THIS file:** the original rule is *never chain a destructive step after a step that
can refuse*. This is the same sequencing failure with the second step being a CHECK rather than a KILL
— and it is easier to miss precisely because a check has no blast radius, so nobody asks whether it
should run.

**And the direction matters:** the other two instances of this family on 2026-09-08 (a comment API
returning `success: true` on an empty body; a push read as dead while in flight) produced **false
greens**. This one produced a **false RED**. *A false green ships a defect; a false red spends an hour
on a phantom.* Both come from the same root — **an output produced by a step that never addressed its
subject.**

**How to apply:**
1. **Gate the verifier on the action's own success**, by rc or by a completion marker — `[ $rc -eq 0 ]
   && verify`. An unconditional verifier is a check with no subject.
2. **A verifier's first assertion is that its SUBJECT EXISTS** — the ref moved, the file was written,
   the id came back. Assert the subject before asserting anything about it.
3. **On a surprising verifier result, check whether the ACTION happened before investigating the
   RESULT.** The seat did this correctly: `state: open, merged: false` on the PR — the destination,
   not the alarm.
4. **Shell/interpreter argument shapes are a live source of this** — `python3 -c "…" VAR=x` passes
   `VAR=x` as `sys.argv[1]`, not as an environment variable. The command succeeds, does nothing you
   intended, and the next step proceeds.
