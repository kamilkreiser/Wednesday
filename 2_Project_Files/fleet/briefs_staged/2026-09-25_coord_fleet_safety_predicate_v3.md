BLUF: (Seat B 25th, Seat L1, Seat L4) The pre-push suite STOP predicate is SHARPENED. **This SUPERSEDES rule 2 of Wednesday's 05:44Z safety correction.** L4 found that the bare substring `FIXTURE BUILD FAILED` matches a PASSING cell's label in its own round-2 guard suite, so every seat would have false-stopped once #1218 merges. The rule now:

2'. Inside the pre-push hook, a **STOP** means EITHER `pre_push_hook_base.test.sh` reads anything other than **28 passed / 0 failed** (its count changes when #1218 lands; then the rule is "0 failed" plus the suite's own pass count, stated in #1218's squash body), OR a line that **STARTS WITH** `FIXTURE BUILD FAILED` (`^FIXTURE BUILD FAILED`, where `build_fixture` writes it). The words appearing mid-line in a label or prose are NOT a STOP.

Rules 1 (no standalone runs until #1218 merges; L4's own round-2 runs only from a cwd outside any git repo) and 3 are unchanged.

L4: your attribution before acting (line 335, inside a PASSING cell, the suite's own 6/0 verdict) is exactly how rule 2 should be applied. Fixing the label at source was right. Your disclosed standalone run started before the correction arrived, at the fixed head, and the checkout is measured untouched: accepted, no action. Push round 2 (`d971aa4f2`, per your mail) and send READY; it joins the next tier-2 batch.
