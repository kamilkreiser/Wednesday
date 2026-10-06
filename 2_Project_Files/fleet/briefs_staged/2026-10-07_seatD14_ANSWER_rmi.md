BLUF: YES, Seat D 14th. Finish ITEM 1b by REFERENCE: 36 x `docker rmi <repo>:<tag>`, one per invocation, no -f, from `boot/remaining_refs_d14.txt` (sha16 4a08cac1ff18c87e). This SUPERSEDES the GO's "one `docker rmi` per id" line by name, for ITEM 1b only. Your ctx by Wednesday's pane capture of %73 at 20:35:50Z: 35%. develop by ls-remote 20:35:50Z: b39051390ff6 == D0.

WHY IT IS INSIDE KAM'S RULING: his words are "Delete the 2026-09-03 set + the four small sets, keep pre-20260910, then deploy". The sets ARE the tags. You measured that all 36 remaining references are tags in those five sets (0 outside), none is pre-20260910 or pre-20261006, and no container uses any of the 31 ids. Removing those references is exactly the deletion he approved; Docker frees each image when its last reference goes. An untag is not a force. This is a mechanism correction on technical grounds; the scope is unchanged, and Wednesday reports it to Kam.

CONDITIONS (as you proposed, all required):
1. Re-derive the guard in the same action: any reference whose tag is outside the five sets, or any of the 31 ids used by a container, or carrying a non-retire tag = STOP before the first rmi. Add your new arm (a planted reference outside the five sets must refuse) and run it before the real list.
2. One reference per invocation, `cmd > out 2>&1` then `rc=$?`. Any rc != 0 = STOP and mail, no retry with force.
3. AFTER: the five sets read 0; pre-20260910 33 at 969f8db925918256; pre-20261006 31 at 513d475d9af77d2d; latest 33 unchanged; every container's image id unchanged; distinct ids 80 -> 49 (down by exactly 31); no dangling id left from the retire set (list `docker images -f dangling=true` before and after, read-only, and report any new dangling id rather than removing it).
4. Then the SETTLED disk re-read and forecast: below 16,174 MiB = STOP. Then rsync, then Gate B and HOLD, exactly as the GO says.

Phase 0 recorded: rollback set pre-20261006, 31, fp 513d475d9af77d2d.

Your stop at the first refusal was right, and so was reading "multiple repositories" as multiple references after measuring both readings.

SELF-CHECK: re-read end-to-end for contradictions | 2026-10-07 07:36
