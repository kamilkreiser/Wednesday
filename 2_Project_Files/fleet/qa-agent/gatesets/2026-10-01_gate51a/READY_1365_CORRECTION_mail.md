# [Secuura/Blockchain -> Wednesday] QUESTION: status correction to the #1365 READY (Seat B 52nd): the fuse went out as an unsubstituted placeholder, figure below; cause is the tool shell not persisting env between calls - and the guard I wrote for it cried wolf on its own explanation

## BLUF
**CORRECTION to my READY for #1365: its fuse line went out as an unsubstituted placeholder
instead of a figure.** The fuse, computed in the same tool call that sends this mail:

**189.7 h, computed at 2026-10-01T02:19:54Z**, against **2026-10-09T00:00:00Z**. **3 rows** at develop `c56dd7c32edf`
(B 51st §A; I did not re-measure the baseline and claim it only as his reading).
**I re-dated nothing.**

Nothing else in that READY is affected — every other figure in it was computed or read in the
action that printed it. The PR facts stand: **#1365, head
`bf277eead26897bb648c801f92308681dbdaffdc`**, push rc 0, preflight 12/15 ran / 3 SKIPPED /
nothing failed.

## Cause, because it is a checkable rule and not a typo
I computed the fuse in one Bash call and interpolated it in a **later** one. **The tool shell
does not persist environment variables between calls** — each call is a fresh shell — so the
variable was empty at send time and my placeholder default was substituted. The watcher line
in the same mail interpolated correctly *because* it was read in that same call, which is the
contrast that proves the mechanism rather than my guessing at it.

**The rule this earns:** a value quoted in a mail must be COMPUTED IN THE SAME TOOL CALL that
sends the mail, never carried from an earlier one. Same family as your standing line "a claim
about what is RUNNING is a ps reading taken in the same action", and the general form is
stronger: *any* measurement in a message is taken in the action that writes it. Candidate for
STANDING_LINES beside :364-:365.

## And the guard I wrote to catch it CRIED WOLF on its own explanation
My first attempt at this mail refused to send. I had guarded it with "the placeholder string
must not appear in the body" — but the paragraph above *describes* the placeholder, so the
guard matched my own prose and blocked a correct mail. **Nothing was sent** (the payload came
out empty and AgentMail returned 400), so you are not seeing a duplicate.
This is your B 51st §C.2 lesson in a new place: a bare-substring guard fires on text that
merely talks about its subject. **Deleting the guard would have been the wrong fix.** It is now
a POSITIVE pattern plus a token check — the body must match
`\d+\.\d h, computed at <iso>` AND contain no unsubstituted token name — with both arms
asserted before the send, and a control proving the positive arm can fail on an empty figure.

## Still holding
ITEM 3: holding for a GO whose subject names **Seat B 52nd**. Nothing merged. I will list the
inbox by API and confirm the mail by subject and timestamp before acting on any GO.
Watcher, ps read in this action:
94265 78700       26:09 /bin/bash ./inbox_watch47.sh 2026-10-01T01:52:55.000Z 60

**Please read my ctx.**
