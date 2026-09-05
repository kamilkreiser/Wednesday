---
date: 2026-08-10
type: correction
source: "Sunday 2026-08-09: the 06:00 session did real work (armed wake_watch, built the doctor gate, refreshed INDEX.md, wrote the daily note) and then simply went quiet. It never wrapped. Retro blank, doctor.sh and INDEX.md uncommitted, and daily/2026-08-09.md never even git-added — ~23 hours of work on one drive with no second copy. Found only by the next morning's shift-change tap. In the same window, wake_watch — armed by hand on Sunday morning — was off again by Monday, exactly as that session predicted."
status: live
supersedes: ""
tier: W
---

# A ritual nothing triggers is not a ritual — it is a habit, and habits skip

**The failure.** Sunday's session built the enforcement that was supposed to fix
Saturday's failure, exercised it properly, honestly named its own remaining gap,
and then stopped existing. No wrap. The retro stayed on its placeholder line,
three files stayed uncommitted, and the day's daily note — the single artefact a
cold session reconstructs the day from — **was never added to git at all.**

Nothing was lost, because the drive did not fail and the next shift change
tapped the pane. That is luck plus a net, not a mechanism.

**Why this is the same disease and not a new one.** This brain has spent a week
converting "I meant to" into "the mechanism did": the pre-commit hook,
`send_brief.sh`'s provenance gate, `doctor.sh`'s checks, the send queue. Every
one of them was built *by the wrap ritual*. And the wrap ritual itself is
triggered by Kam saying a phrase, or by a scheduled tap, or by me remembering.

**So the thing that manufactures all my enforcements is the one thing with no
enforcement behind it.** That is not an ironic detail; it is the highest-leverage
gap in the system. Every mechanism downstream of an un-run wrap does not exist.

**The confirmation that arrived in the same 24 hours.** Sunday armed
`wake_watch` by hand and wrote, correctly, that this was "still the
intention-shaped half of the fix". By Monday 05:30 it was not running, and the
doctor gate built that morning was accurately reporting `✗ wake_watch NOT
running — 2 agent pane(s) live unwatched`. The detector works. The arming is
still a habit. **A correct detector that nothing runs, guarding a mechanism that
nothing starts, is two layers of intention wearing mechanism's clothes.**

**The distinction, sharpened from
[[2026-08-09_an-enforcement-you-must-arm-is-not-one]]:** it is not enough for a
safeguard to sit in the path of the work. It must sit in the path of something
that *reliably happens anyway*. Commits happen, so the pre-commit hook fires.
Briefs get sent, so the provenance gate fires. Sessions ending is NOT a thing
that reliably happens — a session can simply go quiet, and going quiet is
indistinguishable from working.

**How to apply:**
1. **Anchor a ritual to an event that occurs whether or not I remember it.** The
   scheduled shift change and close bell are the only two such events I own. Any
   step that must not be skipped belongs bolted to one of them, not to a phrase.
2. **The close bell should do more than stamp.** It currently writes a line and
   exits. It is the one thing guaranteed to fire daily, and it should at minimum
   detect an unwrapped session — blank retro placeholder, uncommitted tree,
   untracked daily note — and say so loudly.
3. **Untracked is worse than uncommitted.** `git status --short` shows modified
   files at a glance and `??` entries scroll past. A daily note that was never
   added is invisible to every habit I have. Add the note at creation, in the
   same action, exactly as gitignore entries are written at creation.
4. **When a session flags its own remaining gap, that gap has a deadline.**
   Sunday wrote down precisely what would fail next and it failed within 24
   hours. A named gap with no owner and no date is a prediction, not a plan.
5. **Treat "the net caught it" as a finding, not a relief.** The shift change
   recovering 23 hours of uncommitted work is the system working *at its last
   line*. Report it that way rather than as a near-miss avoided.

**Related:** [[2026-08-09_an-enforcement-you-must-arm-is-not-one]] (direct
parent — this is that rule applied to the wrap itself),
[[2026-08-07_a-promise-is-not-a-mechanism]],
[[2026-08-06_exercise-mechanisms-before-arming]],
[[2026-08-04_gitignore-artifacts-at-creation]] (same "in the same action as
creation" discipline, applied to the daily note), [[_ledger]]
