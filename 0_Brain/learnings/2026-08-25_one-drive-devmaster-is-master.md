---
date: 2026-08-25
type: preference
source: "Kam, 2026-08-25 ~10:2x (terminal, verbatim in Discovery/00_prompt-log.md): 'once done, i will unplug t9 as well and launch you from dev master so we use 1 drive for you and dev code'"
status: live
supersedes: "2026-07-31_fully-portable-drive (the T9-is-master half; portability itself still stands)"
tier: W
---

# One drive: DevMASTER is Wednesday's master, the T9 is a sync copy

**The decision:** Wednesday's home moves from `/Volumes/KK_T9_External_HDD/WEDNESDAY`
to `/Volumes/DevMASTER/WEDNESDAY` — the same drive as the dev code. Kam launches
me from DevMASTER from 2026-08-25; the T9 travels with him and stays current only
through his unison engine (`!SYNC FILES/Sync All Drives.command`, bidirectional,
prefer-newer, `.git` excluded by design).

**Drive roles (Kam, same day, 10:3x): DevMASTER = master (Studio); KK_DEV_Local = the
TRAVEL drive and must carry EVERYTHING, no exclusions ("I will travel with this drive");
T9 = a separate backup.** So a sync to KK_DEV_Local is unison (bidirectional, his engine)
PLUS a one-way additive rsync from DevMASTER that carries what unison skips — the `.git`
directories (as snapshots; `git pull` reconciles on the laptop), the ignored paths, and
the file MODES (unison `perms=0` drops exec bits and leaves the deploy key 0644).

**What does NOT change:** the portability principle (everything on-drive,
machine-local pieces on PORTABILITY.md + doctor.sh), the read-only rule on the
DevMASTER vault and other projects' folders, hard rule 1 (writes stay under
`WEDNESDAY/`), the fleet mechanics. Only the mount path of "home" moved.

**How to apply:**
1. Every path in scripts/notes derives from the script's own location or names
   `/Volumes/DevMASTER/WEDNESDAY`; no `KK_T9_External_HDD` in tracked files (swept
   2026-08-25: adopt_scoped_identity.sh, media/receiver.py + stitch.py, BRIEF_TEMPLATE,
   send_brief.sh help text, projects_index/README, CLAUDE.md, PORTABILITY.md, kam.md).
2. `.git` does not sync: the repo travels by `git` (clone/pull/push to
   `kamilkreiser/Wednesday`), never by drive sync. On 2026-08-25 the T9's `.git` was
   copied once to seed DevMASTER; after that the T9 copy's `.git` is stale by design —
   if Wednesday must ever run from the T9 again, `git pull` first.
3. Machine-local pointers re-seated on the day: launchd plists (install_scheduler.command
   re-run from DevMASTER), `/opt/homebrew/bin/wednesday`, the watcher runner and
   dashboard server (armed by the DevMASTER launcher on its first boot).
4. Sync-then-launch order when both copies exist: run the sync engine, verify content
   at the destination, THEN launch — a session launched from a stale copy writes a fork.

**Related:** [[2026-07-31_fully-portable-drive]] (superseded half),
[[2026-08-05_verify-the-chain-not-the-legs]], [[../skills/churn-aware-sync]]
