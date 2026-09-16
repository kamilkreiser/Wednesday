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

---

## ⚡ UPDATE 2026-09-16 14:5x — the BLUF's premise changed today, and it is the best news in this document

The BLUF says *"what is NOT unattended is the only human-shaped step: writing the brief."* **That is no
longer true, and it was proven twice this afternoon rather than argued.**

**What happened.** Two briefs were written by SUBAGENTS given the day's brief rules verbatim, not by a
coordinator seat reading files into its own window:

- **KS-1081** — the agent read the ticket, read the product file at the tip, chose the reference suite,
  wrote literal test cells, pre-measured in its own scratch clone (2 passed / 4 failed at the tip → 6/6
  after), and **Ornith passed it 7/7 on its FIRST sample.** KS-1011, written by the coordinator itself
  before those rules were written down, took four rounds.
- **KS-1031** — the same shape. It also **refused the half of the ticket that was documentation rather
  than code**, and found that the ticket's own justification had expired (the `exit 0` workaround
  outlived the schema-drift problem it apologised for, per `BACKLOG.md:131`) — which is what turned a
  judgement call into a mechanical change. Its first run then failed at B4 on a suite that asserted
  nothing, and the repair went back to the same agent with the checker's evidence.

**Why this matters more than any other piece here.** The week's binding constraint was assumed to be a
coordinator's window: one seat, reading tickets and files, rotating every few hours, each rotation
paying the boot cost again. It is not. **The coordinator's job in the loop is to CHOOSE the candidate,
COMMISSION the brief, QUEUE the result and READ the verdict** — all of which are cheap — while the
expensive reading happens in a window that is thrown away.

### What this changes in the table above

| piece | revised |
|---|---|
| **(c) briefs batched ahead** | **Not a batching problem any more — a commissioning problem.** The seat does not need K briefs written before it rotates; it needs to be able to commission one in a single tool call and have the result queued without it. Both halves now exist: the commission is a subagent with the rules prompt (the KS-1081 prompt is the template — keep it verbatim, its rules are each a round someone paid for), and `night/autostart_on_brief.sh` builds, queues and launches the moment a brief file appears, with a give-up that reports rather than sits silent. |
| **the RULES are the asset** | The brief rules are now written in `0_Brain/tasks/NEXT-PICKUP.md` under BRIEF RULES and must be carried into every commissioning prompt verbatim. Each line is a model round that was paid for: no context lines in the fence · no backslash continuations · literal shell cells · every 🔴 red by assertion at the tip · one 🟢 control · every `-` line copied byte-for-byte from `git show`. **A commissioning prompt without them regresses to four rounds per ticket.** |

### What is still owed, and it is now a shorter list

1. **The commissioning step is not yet a mechanism** — it is a coordinator choosing to make the call.
   For a week without Kam the seat needs it in its boot rule: *"if the queue is empty and the model is
   idle, commission the next candidate from `night/candidates.md` before doing anything else."* That is
   INSTRUCTION, not code, and it belongs in the boot prompt beside the pickup read.
2. **`autostart_on_brief.sh` has run once and failed once** (a `case` inside `$( )`, which `bash -n`
   passes — fixed and armed by running it). Under 2026-09-08's rule it is a mechanism with one worked
   example and no exception met: **it must complete one unattended cycle end to end before Monday**,
   or the week's loop rests on a script that has never finished its job.
3. **Nothing yet writes the verdict back to the board.** A week of held pins with no ticket comments
   means Peter and Stuart see silence. Decide before Monday whether that is acceptable (Kam's 09-15
   ruling says QA and merge happen Sunday, so silence may be correct) or whether the receipt should
   also post per-ticket.

**The honest risk, unchanged:** the POOL. Every candidate left for this tip is decision-shaped,
design-shaped or under `systemTest/` (blocked on a stale object store). A loop that runs perfectly
through an empty pool produces nothing. **Kam's 09-16 09:53 ruling is the answer — skip the blocked
one, card it with a default, take the next, down the whole list — and that ruling has to be IN the
week instruction, not only in a lesson.**
