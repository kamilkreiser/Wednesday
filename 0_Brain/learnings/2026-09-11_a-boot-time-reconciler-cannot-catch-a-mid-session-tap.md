---
date: 2026-09-11
type: correction
source: "Kam's 20:27 and 20:28 card taps on 2026-09-10 reached their cards ~10 hours late; found by the 06:03 seat's boot reconcile, filed by the 13:26 seat"
status: live
supersedes: ""
tier: W
---

# A reconciler that only runs at boot cannot catch a tap Kam makes mid-session — run it at every checkpoint and before every wrap

**The operative case, so the headline matches it:** Wednesday is at a checkpoint, about to write a handover, or about to wrap — and Kam has been on the panel at any point since this seat booted. **Run `2_Project_Files/tools/reconcile_rulings.py` (report mode, then `--apply`) before writing anything that says what Kam has or has not ruled.** His taps are chat messages; nothing writes them onto the card except that tool, and nothing runs that tool except a seat choosing to.

**Context:** on 2026-09-10 Kam tapped `wed-nas-nightly-leg-has-never-completed` → `stop-partition-rerun` at 20:27 and `nas-shared-folders-owner` → `wednesday` at 20:28. The seat had booted before both taps and ran its reconcile at boot only. It then worked the night and wrapped without running it again, so both cards read `open` for ~10 hours. The first ruling's ACTION had been done by hand; the second had not been acted on at all, and Kam's next message, *"Please advise Tuesday about the fleet sink decision"*, went unexecuted until 06:1x. A tool that fires at one moment only catches events that happened before that moment.

**How to apply:**
1. **The checkpoint ritual gains one command:** `reconcile_rulings.py` next to `kam_rulings_today.sh`, at the 50% and 70% checkpoints and before the wrap or rotation handover. Report mode first. `--apply` only for this seat's scope.
2. **A handover line about a card's state is written after the reconcile, never before.** "Nothing ruled since X" rests on a read taken in the same action.
3. **When a tap is found late, check the ACTION as well as the record.** A card recorded late may also be an instruction nobody carried out; read Kam's next messages after the tap for what he expected to follow.
4. **Mechanism candidate (named, not built):** the watcher's checkpoint legs run the reconcile in report mode and put any `to rule: N>0` into the wake text. `wake_watch.sh` is shared with Tuesday, so it is claimed with her before it is touched ([[2026-09-10_claim-a-task-with-tuesday-before-starting-it]]).

**Related:** [[2026-08-10_a-ritual-nothing-triggers-is-not-a-ritual]] · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (its 2026-09-10 clause: a tool you must choose to call is not one) · [[2026-09-05_a-relayed-ruling-is-delivered-only-when-it-is-in-the-artefact]] · [[2026-09-10_kam-rules-by-tapping-cards]]
