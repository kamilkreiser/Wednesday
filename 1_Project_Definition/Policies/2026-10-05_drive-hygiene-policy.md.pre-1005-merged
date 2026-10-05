---
date: 2026-10-05
type: policy
source: Kam, live board 2026-10-05 12:13:55 view=wednesday — "Clear up the drives and put in a policy to do that regularly. Send a message to the other agents to do the same."
status: live
---

# Drive hygiene policy — every coordinator, every project, on a cadence

**Where stale files go:** `/Volumes/G-DRIVE/Scratch Files/<YYYY-MM-DD>_<seat-or-project>_<what>/` on the Studio's G-DRIVE
(shared on the LAN as `smb://Kamils-Mac-Studio.local/G-DRIVE`, guest off). Kam clears that folder periodically.
**A move is: copy → verify at the destination (size + checksum, or byte compare) → only then remove the source.**

## What is stale (move it)
1. Working copies whose work is MERGED and whose tree is clean (git worktrees, scratch clones, QA run clones), older than 7 days.
2. Regenerable leftovers older than 14 days: `node_modules`, `.venv`, `.next`, `.turbo`, `dist`, `build`, `coverage`, caches.
   Prefer letting the owning project's own agent REMOVE these (they reinstall with `npm ci`); copying millions of
   small files to the G-DRIVE costs hours (Kam 2026-09-29: regenerable leftovers are not kept).
3. Superseded disk images, duplicate model stores, large archives no tool references (prove non-use first: `lsof`, the
   tool's own config, a grep of the project's scripts for the path).

## What is NEVER moved
`.git` directories; credentials (`3_Access_Keys/`, `4_Credentials/`, any `.env`); records (`0_Brain/`,
`1_Project_Definition/`, `5_Project_History/`, `Notes (MASTER)/`); anything changed in the last 3 days; anything a live
seat or process uses (its cwd, an open file, a path in a running job's config); worktrees with uncommitted or unpushed work.

## Who moves what (hard rule 1: manage, don't do)
- Each **project's own agent** cleans its own project tree (its worktrees, then `git worktree prune` in its own repo).
- Each **coordinator** (Wednesday: Secuura + general + her own tree; Tuesday: Datasec; Friday: its laptop and its own
  projects) commissions that, and cleans its own tree directly.
- **Cross-client never:** a coordinator never moves, lists by name, or reads another client's files.

## Cadence (the "regularly")
- **Weekly**, at each coordinator's weekly consolidation: re-run the survey for its scope (Wednesday's 2026-10-05 survey
  is the template: `0_Brain/reference/2026-10-05_dev-drive-survey/SURVEY.md`), move class 1-3, report reclaimed GB and
  free space before/after to Kam in that day's receipt.
- **Immediately** when a drive passes 85% used.
- Every seat's wrap: worktrees and clones it created for a merged PR are removed or moved by that seat (its own only).

## Report shape (to Kam, one line per drive)
`<drive>: <used>/<size> (<pct>%) · moved <GB> to G-DRIVE Scratch Files · removed regenerable <GB> · kept <class> because <reason>`
