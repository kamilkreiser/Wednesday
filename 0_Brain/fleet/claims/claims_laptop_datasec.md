# Claims — TUESDAY (Datasec seat, Mac mini)

## 2026-09-21 09:5x — CLAIMED: scheduler/jobs/nassync.plist.template + scheduler/install_all_jobs.sh

**Shared fleet tooling, both seats install from it. Claiming before touching, per Kam's 2026-09-08
rule.**

**Why:** `nassync.plist.template` hardcodes `Hour 3 / Minute 30` and `install_all_jobs.sh` substitutes
only `@PROJECT_DIR@`, `@SEAT@` and `@HOME@` — **not the hour**. So installing nassync on Tuesday's
machine schedules her leg at **03:30, the same minute as Wednesday's**, which (a) contradicts Kam's
instruction of 2026-09-08 14:57 — *"Get Tuesday to sync at 11pm, and I think you should sync at 3 or
4am"* — and (b) puts **two concurrent unison legs on the same NAS replicas with
`confirmbigdel = false`**.

**Change:** add an `@NASHOUR@`/`@NASMIN@` placeholder pair, rendered per seat —
**tuesday 23:00, wednesday 03:30**. Wednesday's rendered plist is UNCHANGED in value (still 03:30),
so this cannot disturb her installed job; it only stops Tuesday's from colliding with it.

**Status: DONE and verified this session.** Wednesday: no action needed, but re-run
`install_all_jobs.sh --check` at your next boot to confirm your own job still reads 03:30.
