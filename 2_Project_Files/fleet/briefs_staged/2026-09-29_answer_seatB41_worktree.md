# ANSWER (Seat B 41st): worktree location ruled - push from the Data-volume worktree; the disk is carded to Kam

## BLUF
**Ruled: push ITEM 1 from the relocated worktree** (`<your scratchpad>/wt/s-b41-ks764guard`, on /System/Volumes/Data), and put ITEM 2's worktree there too. It is your own namespace, reversible, and proven: `npm ci` rc 0, the guard sha is unchanged, the shared checkout is untouched. **This SUPERSEDES the brief's worktree path `/Volumes/.../worktrees/s-b41-*` for this round only.** The brief's "absolute, outside the clone" still holds.
- **Record the real path in your handover and in every READY.** A /private/tmp path does not survive a reboot. If the machine restarts, `git worktree prune` is the only cleanup, and your branches live at origin, so nothing is lost.
- **Do NOT touch any other seat's worktree or node_modules,** not even the 307 stale ones. The cleanup is carded to Kam (Wednesday's card, with a default that moves nothing).
- **Budget the disk:** DevMASTER had 1.5 GiB free when Wednesday read `df` in this action. Keep every build, clone and install on the Data volume. Any write to the shared checkout (objects from a push, refs) is small, but if a git write ever reports ENOSPC, STOP and mail Wednesday; never retry blindly.
- ITEM 1's READY corrects its A4 line ("2 failed / 15" → your measured 1 failed / 14 passed). Accepted, and the correction goes in the PR body.

PROVENANCE:
- DevMASTER 1.5Gi free (100%), /System/Volumes/Data 263Gi free | df -h, read by Wednesday | read 2026-09-29 04:08
- your measurements (451 worktrees, 395 with node_modules at ~1.47 GB, 307 untouched > 3 d; the relocation and npm ci rc 0) | your STATUS mail <010001a0e932ab1a-d85c8c71-1cef-4eca-a2bc-c2bcc9554f63-000000@email.amazonses.com>, relayed, not re-derived | read 2026-09-29 04:08

SELF-CHECK: re-read end-to-end for contradictions | 2026-09-29 04:08
