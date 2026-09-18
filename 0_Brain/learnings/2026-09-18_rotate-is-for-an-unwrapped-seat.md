---
date: 2026-09-18
type: principle
source: "12:3x, retiring seat A 9th after it had wrapped by itself. `cockpit.sh rotate` would have tapped it to run its end-of-session ritual AGAIN, and that ritual posts the rule-7 ticket comments to Peter and Stuart."
status: live
supersedes: ""
tier: W
---

# `cockpit.sh rotate` is for a seat that has NOT wrapped; retire a wrapped seat by hand

**The lesson:** `rotate` does tap → **wait for a wrap mail NEWER than the tap** → kill → relaunch. On a
seat that has **already** wrapped, it forces a **second** end-of-session ritual. A Secuura seat's ritual
posts the rule-7 comments, so that means **double-posting to Peter and Stuart**. If no fresh wrap mail
comes within the timeout, it also force-kills with a false `!!!! ROTATE FORCED WITHOUT WRAP !!!!` alarm.

**Context:** seat A 9th wrapped by itself at 02:30Z (history entry, handover, rule-7 comments on KS-485 and
KS-772, wrap mail). Its Claude process then stayed alive at an empty prompt. "Rotate the seat" was the
obvious move, and reading `rotate`'s body showed it would have made the seat wrap again.

**How to apply:**
1. **Ask first: has this seat already sent its wrap mail?**
   - **No** → `cockpit.sh rotate <Client/Project>` (the tool's intended case).
   - **Yes** → retire it **by hand**. Verify the wrap landed ON DISK (handover file, the top history entry,
     repo porcelain against that project's known baseline), then `tmux kill-pane` and `cockpit.sh launch <Client/Project>`.
2. **A wrap MAIL is a claim; the handover and history entry are the evidence.** Check them before killing
   the pane, because killing loses everything that wasn't written.
3. **Never run two sessions on one project**: confirm the old Claude process is gone (its cwd) before launching.
4. **Owed (a mechanism, not just this lesson):** `rotate` should REFUSE when the pane's project already has
   a wrap mail since the pane's own boot, and say "already wrapped, retire by hand". It needs arms: a wrapped
   seat that must refuse, and an unwrapped one that must rotate normally.

**Related:** [[2026-09-18_use-the-fleets-own-tool-before-rebuilding-its-behaviour]], [[2026-09-01_a-tap-is-a-pointer-not-a-message]]
