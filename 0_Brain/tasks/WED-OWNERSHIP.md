# WED ownership — who is doing which Wednesday-project item

**Kam's rule (panel, 2026-09-08, verbatim):** *"from now on, any work on wednesday, take
ownership so both agents dont work on the same things"*

Client work is already split (Secuura = Studio seat, Datasec = laptop seat). **This file is
for WED work — Wednesday's own project — which is the half with no owner.**

**Claim BEFORE starting, release when done.** Written by `2_Project_Files/tools/wed_claim.sh`,
which pulls before every read and pushes immediately after every write, so the other seat
sees the claim rather than discovering it in a conflict.

| Claimed (local) | Seat | Item | State | Released / note |
|---|---|---|---|---|
| 2026-09-08 10:08 | Kamils-MBP | wed_claim.sh itself — the ownership mechanism Kam asked for 2026-09-08 | OPEN | |
| 2026-09-08 10:09 | Kamils-MBP | wed_claim.sh docs pass (distinct work) | CLOSED |  2026-09-08 10:09 exercised, not real work |
| 2026-09-08 10:09 | Kamils-MBP | throwaway control item 1788826188 | CLOSED |  2026-09-08 10:09 control, exercised only |
| 2026-09-08 10:16 | Kamils-MBP | Launch_Wednesday.command line 198 — per-seat ledger scope (Kam ruled 'scope' 09:57) | CLOSED |  2026-09-08 10:18 done: per-seat ledger live, 3 hosts exercised, tail asserted |
| 2026-09-08 10:40 | Kamils-Mac-Studio | Fleet activity items never clear — attn is derived from the subject each run; wire it to ack_state (Kam 10:19) | CLOSED |  2026-09-08 10:43 DONE — generate.py honours mail:<ts> acks, fleet_ack.sh built, red-proofed on the rendered page both ways; also fixed wed_claim.sh's dead T9 path found while claiming this |
| 2026-09-08 11:07 | Kamils-Mac-Studio | decision_queue.sh + sync_kam_rulings.sh write Kam's rulings file without checking it is current — staleness guard | CLOSED |  2026-09-08 11:10 DONE — shared _store_guard.sh, rc 7 stale / rc 8 markers, write paths only, 8 cells exercised |
| 2026-09-08 11:26 | Kamils-Mac-Studio | INDEX.md head block is 4 weeks stale and misleads every cold seat at boot — rewrite the head, not a full sweep | CLOSED |  2026-09-08 11:26 DONE — head corrected + scope reason stated, additive only, WED-7 still unbuilt |
| 2026-09-08 11:27 | Kamils-Mac-Studio | KS-996 measurement (read-only): are the 95 archived non-terminal Secuura tickets cascade collateral? parent archivedAt to the millisecond | OPEN | |
| 2026-09-08 12:23 | Kamils-Mac-Studio | Phase 0 + Phase 1 — chat streams (one writer per file, chat_log.json becomes DERIVED) and the WEDNESDAY|TUESDAY toggle. Kam's 12:1x commission. | OPEN | |
| 2026-09-08 13:14 | Kamils-Mac-Studio | Secuura s153 launched on the standing queue (KS-989 first) — supervision, gate, scoring | OPEN | |
| 2026-09-08 14:58 | Kamils-Mac-Studio | Drive sync topology: DevMASTER->T9 full sync now, plus nightly NAS sync schedules for both agents (Tuesday 23:00, Wednesday 03:00-04:00) — Kam 14:57 | OPEN | |
| 2026-09-08 17:57 | Kamils-Mac-Studio | Correct learnings/2026-09-08_the-boot-spec-outgrew-its-window.md — its premise (the digest + ledger do not fit the window) is falsified by measurement; it is causing seats to under-read their own ledger | CLOSED |  2026-09-08 18:02 DONE 18:0x — headline rewritten, false clause struck in place, rules 1/3/4/5 kept, rule 2 withdrawn as a default only; both digests regenerated and the corrected headline verified present in the committed by-tier digest |
| 2026-09-09 06:12 | Kamils-Mac-Studio | fleet/specs/BRIEF_SKELETON.md — the four gate literals unprefixed at line start, as the starting point of every brief (ledger w=4, the ##-prefix regression) | CLOSED |  2026-09-09 06:14 --note |
| 2026-09-09 07:46 | Kamils-Mac-mini | Mac mini (Kamils-Mac-mini) bring-up — Tuesday's machine, fresh macOS 27 install: GUI apps, Homebrew formulae, credentials, scheduler. Kam's 2026-09-09 07:5x commission. | CLOSED |  2026-09-09 10:28 DONE at s1 wrap 7a55c299: 19->3 doctor warnings, 6 GUI apps + 11 brew formulae, scheduler agent-aware and armed, ~/.zprofile created. Record in PORTABILITY.md 'Kamils-Mac-mini' section. Open for Kam: dead tenant in ~/.azure (inert), 23:00 close/nassync collision. |
| 2026-09-09 08:26 | Kamils-Mac-mini | Parameterise install_scheduler.command + doctor.sh by WED_AGENT (Kam ruled 'parameterise' 08:21). SHARED files both seats run — testing both agent directions before arming. | CLOSED |  2026-09-09 08:36 Done fa587be8/47a879ec: all four jobs agent-aware, both directions sandbox-tested, Tuesday's four armed. Extended to wake+close (launcher and inbox) because a correct label with a wrong launcher/inbox is worse. Also fixed the pre-commit JSON blindness found en route. |
