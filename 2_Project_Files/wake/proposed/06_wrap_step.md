# Proposal 6: the wrap step that writes the handover through the tool

TARGET: `CLAUDE.md`

## Reason

The session-end ritual names no handover step at all; the pickup file was written by habit, with a text editor, which is how 106 blocks were stacked under a header that says never stack. The new step puts the tool in the path: one command for wrap, checkpoint and rotation, and the command refuses a stack. Seat-neutral wording, so it binds only a seat that has moved to the pack.

Round 3 (the checker's N8): the step no longer carries Kam's name and date. His words on 2026-11-27 were the go for steps 1 to 3 of the design; the wording of this wrap rule is the coordinator's, and the text now says only which ticket it belongs to.

```old
1. Distil the session: new learnings → `0_Brain/learnings/`, decisions →
   `1_Project_Definition/`, open threads → `0_Brain/tasks/TASKS.md`.
```

```new
1. Distil the session: new learnings → `0_Brain/learnings/`, decisions →
   `1_Project_Definition/`, open threads → `0_Brain/tasks/TASKS.md`.
1a. **Handover through the tool (WED-170 step 1).** A seat that
   boots on a wake pack writes its handover ONLY with
   `2_Project_Files/wake/handover.sh write --stdin` (a quoted heredoc; five headed
   parts: FLOOR, FIRST WORK, OWED, OPEN CARDS, GRANTS IN PLAY). The tool keeps ONE
   block in `0_Brain/tasks/STATE-<seat>.md`, moves the previous block to
   `STATE-<seat>-archive.md` in the same action, and refuses a block over its size
   cap, a clock with an x digit, or a second block. The same command serves every
   checkpoint and rotation. Such a seat adds nothing to `NEXT-PICKUP*.md`. Then
   `handover.sh check` must print OK, and both STATE files go in the wrap commit.
   One writer at a time: the tool takes a lock for the whole write; a second write
   waits, then refuses (rc 5) and is simply run again.
```

ROLLBACK: `git revert` of the commit; the seat then hands over as before. Blocks already written stay in the STATE files and lose nothing.
