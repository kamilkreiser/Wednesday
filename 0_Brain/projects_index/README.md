# Spec: feeding the projects index from other projects' sessions

**Goal (from Kam's brief):** every coding project's wrap-up updates an index entry,
so that when Wednesday starts she reviews her own brain *plus* the current state of
every other project, and Kam can delegate / control / advise coding projects
through her. Token cost at Wednesday's startup is explicitly accepted.

**Status:** IMPLEMENTED 2026-07-31 with Kam's explicit approval (same-day session,
prompt log #4). Step 2c added to the vault `end-of-session.md` skill — auto-loaded
by all 15 launchers, so no per-launcher edits were needed. Mount-tolerant (skips
with a one-line note when the T9 isn't plugged in). Smoke-tested by writing
`entries/Secuura__Blockchain.md` from the project's real history head. Survey
confirmed no launcher and no vault file previously maintained any index.

## Design (proposed)

1. **One index file per project**, written at wrap-up:
   `0_Brain/projects_index/entries/<client>__<project>.md` — frontmatter
   (`client`, `project`, `path`, `status`, `updated`) + the same four fields as
   INDEX.md's template (last session, open/next, blockers, notes for Wednesday).
2. **Writer:** extend the vault `end-of-session` skill (single point — all
   projects inherit it) with a final step: "if the Wednesday drive is mounted,
   write/refresh this project's index entry". Launchers need no per-project edits
   beyond pulling the updated skill — keeping change surface to ONE file.
3. **Mount-tolerant:** if `/Volumes/DevMASTER/WEDNESDAY` isn't mounted,
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
