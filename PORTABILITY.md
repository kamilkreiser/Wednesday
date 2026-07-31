# Portability checklist — bringing Wednesday up on another Mac

The T9 SSD is the master copy (Kam's rule, 2026-07-31): plug it into any Mac and
everything should be here. These are the ONLY machine-local dependencies; run
through this list on a new machine.

| # | Dependency | On a new Mac | Degrades to |
|---|---|---|---|
| 1 | Claude Code CLI + Kam's login | Install Claude Code, log in to the Max account | Nothing works without it |
| 2 | "Moira (Enhanced)" voice | System Settings → Accessibility → Spoken Content → System Voice → Manage Voices… → English (Ireland) → download Moira (Enhanced/Premium) | Compact Moira (robotic) — speak.sh auto-detects |
| 3 | Volume name/mount path | Drive must mount as `/Volumes/KK_T9_External_HDD` (default). If renamed, launcher still works (self-locating) but memory notes referencing the path go stale | — |
| 4 | DevMASTER workspace | Optional read-only context; launcher reports "NOT mounted" and continues | Reduced cross-project awareness |
| 5 | git + ssh | Xcode CLT (`xcode-select --install`). Deploy key lives ON the drive (`3_Access_Keys/github_deploy_rw`, gitignored) — no keychain dependency, portable by design | — |
| 6 | Claude Code auto-memory | Lives in `~/.claude` per machine — NOT portable. Wednesday's real memory is `0_Brain/` (on-drive) by design; treat auto-memory as a cache | — |

Keep this file updated whenever a new machine-local dependency appears.
