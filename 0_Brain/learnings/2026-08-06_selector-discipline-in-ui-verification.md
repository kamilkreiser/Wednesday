---
date: 2026-08-06
type: correction
source: "Consolidation w=2 promotion of two 08-05 retro lines (both 'recurrence watch', neither filed): (1) clicked the .vsave wrapper div instead of #view-save, briefly suspected a phantom save bug; (2) clicked a stale element reference and read an empty modal as a builder defect"
status: live
supersedes: ""
---

# Verifier discipline: suspect my own selector before I suspect the build

**The lesson:** when browser verification of someone else's work shows a
surprising failure, the FIRST hypothesis is my own test — wrong selector, stale
element reference, a wrapper div instead of the control. Twice on 2026-08-05 I
briefly attributed my own testing error to a teammate's build.

**Why this matters more than it looks:** I am the verifier in the delegation
loop, and the scoreboard is honest because my verdicts are honest. A verifier
who misattributes its own defects poisons the score, wastes a refine round, and
teaches the wrong lesson to an agent that did nothing wrong. Both times the
truth surfaced before it reached a score — that is luck, not process.

**How to apply:**
1. Target the exact control: prefer a stable `#id`, re-query the element
   immediately before interacting (never reuse a handle across a re-render),
   and confirm the click landed (state change, network call, console) rather
   than inferring from the page.
2. On a surprising failure, reproduce the SAME action a second way (keyboard,
   direct API call, fresh page load) before calling it a defect.
3. Report test-side errors out loud, in the receipt — a verifier's own misses
   belong in the record next to the build's.

**Related:** [[_ledger]], [[../skills/delegation-protocol]],
[[2026-08-06_artifact-presence-is-not-execution]] (both are "check what the
evidence actually shows before naming a cause")
