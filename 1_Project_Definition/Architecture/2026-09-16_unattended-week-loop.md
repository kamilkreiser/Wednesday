---
date: 2026-09-16
type: architecture
source: Kam 2026-09-15 18:19 ("Next week I will be away and would love to give you an instruction at the start of the week and know progress continues through the week and does not stop") + 18:23 ("it will be from Monday night so we will have a full day to work through things")
status: design — owed a BUILD + PILOT by Monday 2026-09-21 morning (Monday is refinement with Kam; he leaves Monday NIGHT)
author: Wednesday, the 07:00 seat, written at ~62% ctx from what exists on disk this morning (every "exists" below was checked: launchctl list, the plists, the scripts named)
---

# The unattended week — one instruction Monday night, progress every day until Kam is back

## BLUF
The loop that runs Ornith is already unattended (`com.wednesday.ornith-loop`, launchd, every 900 s, consumes `night/queue.md`; the 06:45 `ornith-receipt` posts Kam's morning line). **What is NOT unattended is the only human-shaped step: writing the brief.** Kam's rule (09-15): the ticket is never the prompt — Wednesday reads the file at the tip and writes `night/briefs/<id>.md`. Today that is a Claude seat's act, and a Claude seat costs weekly allowance (the gauge reads 99% at 07:3x; renews Saturday ~11:00 AEST) and needs a live coordinator. So the week's loop is: **a Wednesday seat that stays alive all week on a fresh allowance, whose FIRST act at every boot is "brief the next K candidates from the derived queue", with Ornith consuming them and the receipt job reporting.** The five pieces, what exists, what is owed:

| piece | exists today | owed before Monday |
|---|---|---|
| (a) coordinator alive all week | `wednesday_rotate.sh --self` (refuse-tap + push, built 06:2x), the watcher's DEAD leg + `dead_banner_check.sh`, the 05:30 shift change and 23:00 close bell | a **WEEK INSTRUCTION file** the boot prompt reads (`0_Brain/tasks/WEEK-INSTRUCTION.md`: Kam's words verbatim + scope + stop conditions), so a cold seat needs no Kam; the launcher line that reads it; a `doctor.sh` check that it is dated this week |
| (b) candidate derivation | `night/derive_candidates.py` (T1 vitest · T2b bash · T3 jest · T4 docs · T5 later; HELD / SET_ASIDE / EXCLUDED with reasons; re-run at each sweep) | run it at every boot AND every 6 h from the loop job (a ticket closed/archived/taken during the day must drop out); its output is the queue's SOURCE, never the queue |
| (c) briefs batched ahead | this seat's shapes: bash (KS-1047/1093), vitest one-hunk (KS-1121), test-only + tamper (KS-975), source-pin (KS-629); the pre-measure template `scratchpad/ks1093/` | a **brief budget per seat** (K = 4 at boot, +1 per hold) and the rule that a seat ends its turn with the model RUNNING or a batch QUEUED — already standing; the missing piece is the pool: by 07:3x the easy pool for THIS tip is decision/design/Kam-class only (see §Pool) |
| (d) the loop job pulls `queue.md` 24/7 | `com.wednesday.ornith-loop` (900 s) + `night_run.sh` gates G1–G6 | a G7: refuse when `usage_gate.sh` says a CLAUDE seat is over the cut — no, the loop is Ornith (free); G7 is instead a **liveness line to the panel when the queue has been EMPTY for > 2 h during 06–23** (the never-idle rule needs a wake, not a hope) |
| (e) a daily receipt Kam reads anywhere | `com.wednesday.ornith-receipt` 06:45 → the panel (fired today: "4 passes / 10 fails / 9 new pins / 67 pins") | the receipt counts VERDICT LINES — today's "10 fails" were harness/brief rounds later retracted; it must count **READY pins (distinct ticket+pin)** and name the day's holds, and say when the queue is dry or the coordinator is dead |

## The instruction Monday night, as Wednesday will read it
Kam types one panel line (any words). The seat receipts it, writes it VERBATIM into `WEEK-INSTRUCTION.md` with the derived scope (which boards, which tiers, what pauses — signature classes unchanged; auth/MFA/OAuth last; nothing merges without the TESTED grant's conditions), and from then on every boot's first read is that file. Rotations self-heal (06:2x mechanism); a dead seat is respawned by the watcher; the 05:30 and 23:00 bells tap. **If the file is older than 7 days or names a week that has passed, the seat STOPS briefing and cards Kam** — a time-scoped instruction carries its own expiry (09-06 lesson).

## Pool — the honest state at 07:3x on 2026-09-16 (the risk the design must name)
The T2b bash tier (14 rows at 06:5x) was read this morning: KS-1093 held; KS-998 → a decision card (item 1) + a Sunday Claude seat (items 2–4); KS-1011 and KS-1081 → decisions (recreate path / which template is canonical); KS-1148 and KS-1162 → `.github/workflows` = Kam-class; KS-1031/1033 → design; KS-813/1163 → 200+ line reads. The T1 vitest pool: KS-1168 (ILIKE on ciphertext — needs a design: HMAC lookup or decrypt-side filter), KS-839 (OAuth — last), KS-1125 (a fake-`pg` module-resolution harness — a QA-gate cell, not first-sample), KS-960/746/683 → decisions, KS-1173 → Sunday (Kam 19:44). **So the unattended week runs dry within a day unless (1) Kam rules the decision cards Monday (KS-998, KS-1011, KS-1081, KS-1168 — card them Monday morning as ONE batch with defaults), or (2) the harness widens to a new shape: MULTI-FILE (T5, 23 rows) as split runs, and DB-backed bash suites (ks949) with a scratch Postgres.** Both are the next seat's; (2) is the one that does not need Kam.

## Build order (the next seats, in this order; each with arms before install)
1. `WEEK-INSTRUCTION.md` + the launcher read + the doctor expiry check (small; the 09-06 scoped-override shape).
2. The receipt job counts distinct pins from `READY_*` filenames and names the day's holds + "queue dry since HH:MM" / "coordinator dead since HH:MM" (the 06:45 line today misled by counting verdict lines — a representations failure in a job).
3. The loop job's empty-queue liveness line (G7) to the panel via `chat_reply.sh`, rate-limited to one per 2 h.
4. A Monday-morning card batch to Kam: the four decision tickets above with defaults, so the week has a ruled pool.
5. The T5 multi-file split tier in `derive_candidates.py` (a ticket naming N files → N split rows with `NIGHT_BRIEFS_DIR=briefs/split_<id><X>/`) — the shape this seat used by hand for KS-629 A/B and KS-975 item 2.
6. PILOT: Saturday (allowance renewed) — one seat boots on the instruction file alone, briefs K=4 from the derived queue, and the receipt reports it; Kam reads the receipt Sunday; Monday is refinement.

## What Kam decides before he leaves (a card, Monday morning)
- Merge authority while away: the TESTED grant is open-ended ("for the time being"); the Sunday QA sitting is his — if he wants merges to continue unattended, he says so; default: READYs accumulate, nothing merges.
- Allowance: a coordinator seat every ~3 h × 7 days ≈ the whole week's Claude allowance on rotations alone unless the by-tier boot holds ~30% — measured this seat: boot 32%, +30% for seven holds and one harness gate. State the number on the card.
- The four decision tickets (KS-998 item 1, KS-1011, KS-1081, KS-1168) with recommended defaults.
