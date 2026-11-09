From Tuesday (Datasec coordinator seat), Datasec / HPSM-POC. **Your STATUS file is the channel and the wrap** (no mail). A question is a last line `STOPPED: NEEDS TUESDAY <one question>`. Marks: **MEASURED** = printed by a named instrument; **DERIVED** = source reading, not run; **RELAYED** = read in another file; **UNMEASURED** = nobody has.

# BRIEF B1383 | SEAT-H139: HPSM-POC, BUILDER (OPUS), SUCCESSOR OF B1381. SAME BRANCH `b1381/hpsmpoc-demo-walkthrough`, SAME CLONE, SAME STATUS FILE. Written 2026-11-09 21:13 AEDT.

## WHY YOU EXIST
The B1381 seat was working this lane when the project drive `/Volumes/Datasec_DEV` dropped off the Mac (about 20:39 to 20:58 AEDT, MEASURED by the macOS disk log and by that seat's own STATUS). Its pane was gone by 21:02 (MEASURED: `tmux list-panes`, no HPSM pane; no claude process with an HPSM-POC cwd). **You continue its work. You are not starting over.**

## YOUR COMMISSION = THE ORIGINAL BRIEF, UNCHANGED
Read WHOLE first: `/Volumes/Datasec_DEV/TUESDAY/2_Project_Files/tuesday/briefs/2026-11-09_B1381_SEAT-H137_hpsmpoc-demo-walkthrough.md`. Every hold, decision, partition, check and housekeeping line in it binds you exactly as written; its STATUS path is yours (append to it, never rewrite what the previous seat wrote). Then read that STATUS file whole.

## STATE YOU INHERIT (MEASURED by Tuesday at 21:12 with `git -C <clone> status --short` and `log -1`)
- Clone `/Volumes/Datasec_DEV/!CODING/Datasec/HPSM-POC/.tools/b1381/repo`, branch head = main `2075486b`, no commits yet.
- Working tree: no modified or untracked files; the branch head is still main.
- **Uncommitted work from a seat that died mid-edit is a CLAIM, not a result.** Read every changed or new file whole before building on it; a file may be half-written. Keep what is right, finish what is partial, and record in STATUS which parts you kept and which you redid.
- The previous seat's baseline numbers in STATUS may be void if they were taken during the drop (the B1381 seat said so for its own run). Re-run any baseline you rely on.

## DRIVE DROPS (new since the original brief)
The drive may drop again (cause under test tonight). If a command fails with `Device not configured` or the volume is missing: stop, wait with a bounded loop until `/Volumes/Datasec_DEV` is back (check every 30 s, up to 30 min), re-check the clone (`git status`, `git fsck --no-dangling`), mark any check that ran across the drop as VOID, and re-run it. Write one STATUS line per drop with the times. **Commit and push green work early and often**, so a drop costs minutes, not the lane.

## DEADLINE
Unchanged: HARD STOP 06:00 AEDT 2026-11-10. Push what is green and write down what is not. Finish with `READY B1381: <head sha40>` exactly as the original brief says (keep the original B-number in the READY line so Tuesday's watcher matches it), plus a line `SUCCESSOR B1383`.

READ-WHOLE-BY-TUESDAY: DONE (written by Tuesday s260, read back whole 21:14)
