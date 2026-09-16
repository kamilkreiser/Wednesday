---
date: 2026-09-16
type: correction
source: Kam's 14:00 commission — "I don't understand why you work really well, and Tuesday seems to be working very poorly" — and the measurement that answered it
status: live
tier: W
---

# What keeps a seat CORRECT is not all in git — and every mechanism that checks a tree checks only the part that is

**The operative case, so the headline matches it:** a seat is behaving badly and another seat, on the
same framework, is not. **Do not start by diffing the trees.** Ask instead: *which of the things that
make this seat work are NOT files in the repository?* On 2026-09-16 the answer was all of them. Every
hook, tool, scheduler script and skill was **byte-identical** in both trees and the launcher differed
by twelve lines. Three layers differed, and not one of them is in git:

1. **A gitignored config file.** `.claude/settings.local.json` carries the Claude Code hooks and the
   permission guards. It is gitignored by design — it holds a per-machine statusline path. Wednesday's
   was 1775 bytes with six hooks; Tuesday's was **169 bytes**: a statusline and nothing else. She had
   been running with no PreCompact block and none of the four Bash guards. It was **not mentioned once
   in `PORTABILITY.md` and not checked once by `doctor.sh`** — the two mechanisms whose whole job is to
   notice this class.
2. **A habit standing in for a boot step.** No boot step named a pickup file for EITHER seat. Wednesday
   read hers because she always had. Tuesday did not. **That is the entire reason an ongoing task
   survives a rotation on one seat and dies on the other** — and it looked like a behavioural
   difference between two agents rather than a missing line in a launcher.
3. **Machine-local jobs.** Six of the nine launchd jobs that keep Wednesday alive exist only as
   installed jobs on her Mac, with no plist on the drive at all, and none exist for Tuesday. The job
   that puts her replies on Kam's page **had never run on her machine, not once.**

**And a fourth found the same afternoon, which is the sharpest:** the launcher's boot `git pull` runs
only when the tree is CLEAN, and skips with *"If this seat is behind, commit or stash first"* — a
condition nobody evaluates. **A coordinator's tree is never clean**, because its dashboard writes data
files every minute. So the pull was structurally unreachable at every boot and said nothing when it
skipped. Tuesday sat **382 commits behind origin** — and this one would have quietly undone the other
three fixes, because her seat would have kept booting on last week's copy of them.

## How to apply

1. **When two seats of one system behave differently, enumerate what is NOT in the repo before you
   diff what is.** The list is short and it is always the same shape: gitignored config, machine-local
   daemons, credential stores, anything installed rather than checked out, and **habits**. A diff of
   tracked files answers a question you should not have asked first.
2. **Anything that changes how a seat BEHAVES belongs in a tracked artefact, even when the file it
   lands in cannot be.** The fix here was not "copy the file" — it is per-machine and carries each
   seat's own statusline. It was a **tracked template plus a renderer the launcher runs at every
   boot**, merging only the keys that are policy and preserving the keys that are local.
3. **If `doctor.sh` does not check it, it does not exist.** Every layer above was invisible to the one
   mechanism designed to find exactly this, and that is the reusable failure. A new machine-local
   dependency gets a doctor check in the same session it appears — and for a guard, that check
   **FAILS, it does not warn**. A warning about a missing guard is a guard that is missing.
4. **A SKIPPED step must say what it skipped and what that costs.** This is
   [[2026-09-10_a-refusal-nobody-reads-is-indistinguishable-from-working]] in the costume nobody
   watches: not a refusal, a **skip**, with a generic hint in place of a measurement. The fix is always
   the same — measure the thing the hint gestures at, and print the number.
5. **A habit is not a mechanism, and it is the hardest one to see, because it works.** Wednesday's
   pickup-reading looked like diligence and was actually an undocumented dependency on one seat's
   memory. **Test: if this seat were replaced tonight by a cold one, which of the things I do would
   still happen?** Whatever fails that test is a habit, and belongs in the launcher.

**The uncomfortable half, kept.** Kam framed this as Tuesday performing poorly, and it was tempting to
answer in those terms — she was less careful, she needed better instructions. **Not one of the four
causes was about her judgement.** She was running the same framework with its guards removed, its
handover unread, its jobs unarmed and its code a week stale, and doing so invisibly. Any seat would
have looked broken. **When a system blames the agent, measure the environment first.**

**Family:** [[2026-09-10_a-refusal-nobody-reads-is-indistinguishable-from-working]] (rule 4 above) ·
[[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (the parent — here the arming is a *file* that
never travels) · [[2026-08-25_travel-drive-stale-pointers]] (a sync copies files, not pointers; this
is: git carries tracked files, not configuration) · [[2026-08-07_a-promise-is-not-a-mechanism]] (a
habit is a promise a seat makes to itself) · [[2026-09-09_the-seat-resolver-is-the-layer-above-every-agent-aware-fix]]
(the layer above the thing you fixed) · [[2026-09-14_the-coordinator-adds-value-or-it-is-waste-three-duties-not-watching]].
