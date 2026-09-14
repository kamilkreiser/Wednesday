---
date: 2026-09-14
type: grant
source: Kam, panel 2026-09-14 18:15:36 +10:00 (view=wednesday), verbatim in the prompt log
status: live
tier: W
---

# Grant: Ornith (the local 35B coding model) works the Secuura backlog AT NIGHT, in the downtime, only when no other agent runs — memory cleared first; a standing rule with a prepared ticket list

**His words, verbatim (2026-09-14 18:15:36):**
> *"ok.  thanks.  lets use Ornith at night in the downtime (when no other agents run).  clear system
> memory before it runs so that's not a problem.  Set this up as a rule and get it working on the
> backlog.  Prepare a list of tickets for it to work on."*

**The grant (recorded per go-slow rule 5), read through the day's evidence:** the head-to-head
(16:4x) showed Ornith 35B writes a correct product hunk and the best test of the three models when
the ticket spells its fix out, cannot yet scope a whole ticket, and needs `--recount` on its diffs;
its KS-806 empty result was a runtime cut, not a model verdict. Kam's decision from that: use it —
at night, alone, on a list.

**Operative clauses:**
1. **WHEN:** night, in the downtime — and *"when no other agents run"* is the gate, not the clock:
   the runner REFUSES to start while any fleet pane other than `wednesday`/`fleet-monitor` is live,
   or a QA gate or drafter is running, or the 1-min load is above the harness rule. A clock window
   (23:00–06:00) is the outer bound; the pane census is the inner one.
2. **MEMORY CLEARED FIRST:** every other model unloaded from the Ollama server (`keep_alive: 0` /
   `ollama stop`) and free memory measured (`memory_pressure`, `vm_stat`) before each task; the
   headroom (≥ the model's 21 GB + the checker's clone) asserted, else skip. **Honest limit, told to
   Kam:** a full page-cache purge (`sudo purge`) needs an admin password this seat does not hold —
   stated as a one-line sudoers rule he can set, not done silently.
3. **THE BACKLOG, FROM A LIST:** one checked ticket at a time from a prepared queue file — KS
   Backlog/Todo tickets that fit the `code_patch` contract (ONE product file, a fix shape the ticket
   describes, a runnable in-process test to copy the mock shape from; NO auth/oauth/security
   surfaces; NO tickets a live lane owns; nothing on Peter or Stuart). The list is a board-seat
   artefact, re-derived at source each night (a ticket can be closed, archived by cascade, or taken
   by a lane during the day).
4. **CHECKED, NEVER PUSHED:** each run ends at the checker's verdict + an agent's source read in the
   morning sweep; a PASS becomes a PR only through a Secuura seat under the normal gate; a FAIL is
   evidence. The model holds no board identity.
5. **The two defects the head-to-head named are fixed BEFORE the first night run:** the `task.md`
   copying text (the KS-806 fix expression hard-wired into the prompt) removed; Ornith's runtime cut
   worked around (`think:false` trial, then the harness flag).
6. **Reported, not requested:** the morning brief leads with what the night produced (the
   overnight-is-working-time shape); Kam sees the verdict + the read, never a raw diff.

**Mechanism (a grant is not a mechanism — 08-07):** `2_Project_Files/local-model/night/`
(`night_run.sh` with the pane/load/memory gates, the queue file, per-ticket `input.json` builders),
a launchd job installed the scheduler's way (`install_scheduler.command` pattern), a `doctor.sh`
check that the job is armed and the model present, PORTABILITY item for the drive-local Ollama +
the night job. Exercised both branches before arming: refuse (a live seat) and fire (a scratch
"night" with the floor empty).

**Family:** [[2026-09-14_local-model-pilot-grant-qwen3-30b-simple-checked-tasks-only]] (the pilot
this supersedes in model and in hours) · [[2026-08-28_overnight-is-working-time]] ·
[[2026-08-07_a-promise-is-not-a-mechanism]] · [[2026-08-03_go-slow-earn-autonomy]] (rule 4: pilot,
measure, review) · [[2026-09-14_do-not-guess-a-comparison-a-citation-you-did-not-open-is-a-guess]]
(the comparison this decision rests on was measured, not recited).
