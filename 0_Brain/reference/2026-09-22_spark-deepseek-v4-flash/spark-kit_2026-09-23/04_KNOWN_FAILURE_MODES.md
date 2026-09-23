# Known failure modes

Each one is measured, not theorised, from running a 35B local model against a live backlog since
2026-09-14. **They are a starting hypothesis for DeepSeek Flash, not a finished map** — that model
reportedly scores better, so some of these may not appear. Re-measure in the first week and delete
what does not.

---

## 1. Miscounted hunk headers — the most common, and it fails everything

**What it looks like:** the content is perfect and the patch refuses to apply.

**Measured 2026-09-23:** a task passed 8 of 8 checks, with the added lines byte-identical to the
brief's specification — and its header declared 8 new lines where there were 9. Strict apply
refused; it only applied with a recount. **This happened with the whole file in the prompt**, so it
is not a context problem, it is arithmetic.

**The catch:** have the checker try a STRICT apply and record which mode succeeded. Never let a
report say "applies cleanly" when it applied only with a recount — the person raising it needs to
know which. **Never claim strict unless strict was what ran.**

**If you make the input carry an excerpt instead of a whole file, this is the failure mode you are
pushing on.** The excerpt must carry its start line explicitly and the prompt must say so.

## 2. A green test that was green before the fix too

**What it looks like:** a PASS that proves nothing. The model wrote a test that passes whether or
not the change is there.

**The catch:** the "must be RED first" assertion — break the thing deliberately, confirm the new
test fails, restore, confirm it passes. **This is the single most valuable check in the harness.**
A FAIL on it is a BRIEF defect until proven otherwise: the brief did not make clear what the test
is supposed to detect.

## 3. Copying the brief's prose instead of the file's text

**What it looks like:** context lines that nearly match, so the patch will not anchor.

**The catch:** give the model the file content and say explicitly that context lines are copied
from the file, never retyped. Where the brief quotes a line, quote it byte-exact.

## 4. Editing beyond what was asked

**What it looks like:** the change is right AND something else moved — a tidy-up, a rename, an
import the model thought was missing.

**The catch:** name the off-limits regions in the brief, and have the checker assert the touched-file
set and the changed-line count against what was specified. A diff that changes something unnamed
fails even when the tests are green.

## 5. Large files simply do not fit

**Measured:** a 5,426-line / 264 KB test file produced a 295 KB input ≈ 74,000 tokens against a
65,536 window. The ticket passed every other selection clause and was unbriefable purely on size.

**The catch:** carry the region, not the whole file. Until then, the size check must REFUSE loudly —
a silently truncated file produces a confident wrong diff, which is the worst outcome available.

## 6. Decision-shaped tickets look like work

**What it looks like:** the model produces something plausible for a ticket that was really asking
a human to choose between three designs.

**The catch:** the selection predicate (§2 of the coordinator manual). If the ticket says "one of:",
"decide whether", or "or decide not to", it is a card for a human, not a task for a model.

## 7. The ticket's own fix shape can be stale

**Measured 2026-09-23:** a ticket asked for "a 7th step" in a script that already had 12. The
ticket was written months earlier and the file had moved on.

**The catch:** read the file at the tip before you believe the ticket. The ticket tells you where
someone previously looked; it is silent about everything that changed since.

---

## The meta-rule

**Every one of these is cheaper to catch in the brief than in the output.** When you find a new
one, do not just fix the instance — decide whether it is a model limit, a harness gap or a brief
defect, and put the fix where that answer points. Then write it down here, with the evidence.

---

## Measured on the Spark (DeepSeek V4 Flash) by Friday, 2026-09-23 — smoke test

**8. Fences omitted, content correct (MODEL, format).** Smoke run 1 returned a perfect unified diff with **no code fences**;
run 2 (same brief, temperature 0) fenced it. So the format rule is obeyed inconsistently. **Fix (harness):** `spark_run.py`
accepts an unfenced answer ONLY when there are zero fences, it starts with `--- `, and EVERY non-empty line is unified-diff
grammar; it logs `CONTRACT BREACH (format)`. Any prose keeps the refusal. Arms: `2_Project_Files/friday/spark/tests/unfenced_arms.py`
(pure diff → accepted; diff + one prose line → refused; prose only → refused), 3/3.

**9. A wrong line number still "applies strict" (HARNESS — the checker could not fail).** `git apply` relocates a hunk by
searching for its context, so a header pointing at line 902 of a 17-line file applied cleanly and C1 PASSED. This is
the kit's own deliberate break 2, and it exposed the hole. **Fix (checker):** C1 now includes an ANCHOR CHECK: every hunk's
old side (context + `-`) must sit at exactly the header's start line in the file at the pinned commit, otherwise C1 FAILS
(`applies only by git's context search`) and names where the content actually is. Evidence: `C1_anchor_check.txt`.
Re-proved: smoke PASS (anchor OK at line 2) · break 1 C2 FAIL · break 2 C1 FAIL · the original 22-case self-test ALL OK.
