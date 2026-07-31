# Spec: feeding the projects index from other projects' sessions

**Goal (from Kam's brief):** every coding project's wrap-up updates an index entry,
so that when Wednesday starts she reviews her own brain *plus* the current state of
every other project, and Kam can delegate / control / advise coding projects
through her. Token cost at Wednesday's startup is explicitly accepted.

**Status:** SPEC ONLY. Implementing this touches other projects' launchers and the
vault `end-of-session` skill — that crosses project boundaries (workspace hard rule
1), so it needs Kam's explicit go-ahead and probably a dedicated session in the
workspace itself.

## Design (proposed)

1. **One index file per project**, written at wrap-up:
   `0_Brain/projects_index/entries/<client>__<project>.md` — frontmatter
   (`client`, `project`, `path`, `status`, `updated`) + the same four fields as
   INDEX.md's template (last session, open/next, blockers, notes for Wednesday).
2. **Writer:** extend the vault `end-of-session` skill (single point — all
   projects inherit it) with a final step: "if the Wednesday drive is mounted,
   write/refresh this project's index entry". Launchers need no per-project edits
   beyond pulling the updated skill — keeping change surface to ONE file.
3. **Mount-tolerant:** if `/Volumes/KK_T9_External_HDD/WEDNESDAY` isn't mounted,
   the step is skipped silently (never blocks another project's wrap-up).
4. **Wednesday's startup** reads `INDEX.md` + every file in `entries/` (accepted
   token cost), and rebuilds the INDEX.md summary table from the entries.
5. **Direction of trust:** other agents may ONLY write inside
   `projects_index/entries/` — nothing else in Wednesday's brain. Wednesday never
   writes into other projects without explicit delegation from Kam.

## Alternative considered

Wednesday sweeps all `5_Project_History/history.md` files herself at startup
(read-only, no cross-project changes needed). Simpler, zero touch to other
projects — but stale between wrap-up formats and misses in-flight sessions. Use
this as the interim mechanism until the skill change is approved.
