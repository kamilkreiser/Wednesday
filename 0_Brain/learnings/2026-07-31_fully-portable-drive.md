---
date: 2026-07-31
type: principle
source: "Kam, discovery session (prompt #2), point 1"
status: superseded — the "T9 is the master" half by [[2026-08-25_one-drive-devmaster-is-master]] (2026-08-25); the portability principle itself still lives
supersedes: ""
---

# The T9 SSD is the master — Wednesday must be fully portable

**The lesson:** Absolutely everything for this project lives on the T9 drive
(`/Volumes/KK_T9_External_HDD/WEDNESDAY`). Kam travels: he wants to rip the SSD
out of the Mac Studio, plug it into his laptop, and have everything there.
Repetition and drive-local copies of applications/tools are explicitly fine.

**Context:** Interim arrangement while the project is developed; changes once the
Mac Studio is dedicated to Wednesday. Until then, portability beats elegance.

**How to apply:**
1. Never store project state outside the drive (no ~/Library, no /usr/local, no
   machine-local caches that matter). If a tool needs installing, install it under
   the project folder (e.g. `2_Project_Files/tools/`) even if the machine already
   has a copy.
2. Anything machine-dependent (paths, keychain items, voice downloads, global
   configs) must degrade gracefully on another Mac and be listed in a
   `PORTABILITY.md` checklist so a new machine can be brought up quickly.
3. Launcher and scripts stay self-locating (no absolute references to this
   machine beyond the optional DevMASTER read-only mount).
4. Known unavoidable machine-local items so far: macOS enhanced voice download,
   Claude Code itself + its auto-memory, ssh-agent/keychain state. Track them.

**Related:** [[../people/kam.md]]
