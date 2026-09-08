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
