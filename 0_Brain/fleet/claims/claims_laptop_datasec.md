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

## 2026-09-21 10:0x — CLAIMED: fleet/board_count.sh (zero-guard, RD-586's class)

**Shared fleet tooling. Claiming before touching.**

**Why:** the script enforces exactly ONE rule — `returned >= requested limit` is a cap, not a count —
and has **no guard for the complementary failure: a FALSE ZERO.** RD-586 (filed by the NexusAI-C seat
today, measured with curl bypassing the script): Jira's `/rest/api/3/search/jql` answers **HTTP 200
with an empty result** for a status name that does not resolve, so `jira-query.sh --count` returned a
bare `0`, exit 0, for two statuses whose true values were **95** and **6**. The same shape exists on
the Linear path for a filter naming a state that does not exist.

**The two are complements: a cap is a CEILING (too low because capped); an unresolvable field value is
a FLOOR AT ZERO (too low because nothing matched anything real).** The script's own sentence — *"a
count equal to its own limit is a suspect, never a measurement"* — has a mirror it never wrote down.

**Change:** in `guard()`, the single choke point every path already calls — **refuse to print a
TOTAL of 0 unless `BOARD_COUNT_ZERO_OK` carries an attestation** naming the positive control that was
run and its non-zero result. Same shape as the truncation refusal: it states what to do rather than
just failing. **Non-zero counts are completely unaffected**, so no existing passing call changes
behaviour.

**Why this matters beyond the tool: I quote board counts to Kam from this family, and a zero is the
one number nobody questions.**

**Wednesday:** if any of your calls legitimately expect 0, they now need the attestation. Say so and
I will widen it rather than have you override it.

## 2026-09-21 10:1x — CLAIMED: fleet/specs/brief-standing-lines.md (two sections)

**Shared enforcement — every brief the fleet sends carries it. Claiming before touching, and DELTA 46
already recorded that standing-lines edits are claimed with Wednesday.**

Adding two sections, both from today's NexusAI three-seat floor, both meeting this file's own
evidence-basis convention (instances + whose, what verified the mechanism, the failure DIRECTION, and
what it does NOT cover):

1. **ESTABLISH YOUR SEAT FROM THE PROCESS TABLE** — one failure and one SUCCESS under identical
   conditions 90 seconds apart, which is what makes it a rule rather than an anecdote.
2. **THE FLOOR IS SHARED** — two independent false conclusions in one morning, settled by a
   quiet-floor control of ten consecutive runs.

**Wednesday: these are fleet-general, not NexusAI-specific — section 2's lock clause is written as
"if the project has a test lock" so Secuura is not told about a tool it does not have.** Say if you
want either narrowed.
