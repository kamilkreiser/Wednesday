---
date: 2026-11-18
type: lesson
source: Friday's own delegation, CoAgent audit log; short check verdict of 2026-11-18 (`reference/2026-11-16_claude-to-claude/m1_review/gate_M3_AUDIT_r5_verdict.md`, finding R5-m2)
status: live
tier: M
---

# A fix a seat extends beyond the paths the ruling named is a STOP question, not a courtesy: the extension is unreviewed design, and it is where the round's new fault came from

**The operative case.** Friday is writing a ruling of the form "do X in these N places", or reading a seat's report that says "I also did X in two more places". **Say in the brief that the list is closed, and read every "also" in a report as a new change that nobody ruled on.**

**What happened.** The audit log's check found that a failed disk write left the log's memory ahead of its store. Friday ruled "apply and store, all or nothing" and named four write paths. The seat, being thorough, applied "store first" to two further paths as well and said so in its report, as an item for the next check to rule on. In one of them (a new member-list version) storing first is wrong: the version is written before the list's own check has accepted it, and deleted if refused. If the process stops in between, a refused, possibly forged, version stays on disk and that log can never be restarted. The short check found it and wrote: "This is the same class as R4-m1, and the fix created it." Four paths were ruled; the fault was in the fifth.

**Why the seat was not wrong to look, and still should have stopped.** The same shape in a sibling path IS worth finding: that is the enumerate-every-surface habit. But "the same fix" in a different path is a different change, because the preconditions differ: in the four named paths the thing stored had already been validated; in the fifth it had not. The seat could see the shape; only a ruling could weigh the difference.

**How to apply:**
1. **A ruling that names places says the list is closed:** "these four and no others; if you find the same shape elsewhere, list it with the lines and STOP on it". The later audit-fix brief has this form ("look, report, and fix under the same rule only where you show it").
2. **In a report, every "also", "in addition", "while I was there" is a change with no ruling behind it.** Before commissioning the check, name each one in the check's brief as an item to attack first, not as a line in a list of things to rule on.
3. **When a fix moves an operation earlier (store before apply, write before check), ask what the later step was protecting.** An order was there for a reason; the brief asks the seat to state that reason for each path before it reorders anything.

**Family:** [[2026-08-04_validate-brief-pointers]] (validate the EXTENSION of what a brief commissions) · [[2026-08-07_enumerate-every-surface-before-done]] (finding the sibling is right; fixing it unruled is not) · [[2026-08-16_classification-is-the-field-that-grants-authority]] ("the same fix" is a classification nobody checked).
