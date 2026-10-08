---
date: 2026-10-08
type: grant
source: Kam, live board 2026-10-08 18:12:53 view=wednesday
status: live
tier: W
---

# Ornith 1.5 replaces Ornith 1.0 — push it to harder tasks, and run it AND the Spark as much as possible

**The operative case, so the headline matches it:** Wednesday is about to route a task to the local Studio model, or to brief one. **The Studio model is now Ornith‑1.5‑35B‑A3B (MLX 8‑bit, served by oMLX on 47780), not Ornith 1.0 on Ollama.** Give it harder tasks than 1.0 got, measured rung by rung, and keep both it and the Spark busy.

**His words, verbatim (18:12:53):**
> *"go with Ornith 1.5 and deploy it.  use this instead of the old model.  Keep pushing it and see how far it can go.  The old Ornith has been rather dormant with the spark doing a lot of work.  see if you can give it harder tasks and run both the Spark and Ornith 1.5 as much as possible"*

**Context he ruled on:** Wednesday's A/B (`0_Brain/reference/2026-10-08_omlx-flash-next/ORNITH15_AB.md`) measured a tie, 17/20 each, with 1.5 faster (13.4 vs 16.4 s per task) and using ~35 GB vs 21 GB. Wednesday recommended staying on 1.0. **Kam overruled the recommendation** — the decision is his, and the argument he gave (1.0 has been dormant; push the new one to find its ceiling) is about USE, which the A/B did not measure.

**How to apply:**
1. **Swap, don't delete.** 1.5 becomes the night runner's default model; 1.0 (Ollama `ornith:35b`) stays installed as a named fallback. Nothing is removed.
2. **The serving path is a mechanism, so it is armed AND checked:** a scripted oMLX start on 47780 with the `balanced` memory tier untouched, a memory guard while seats are live, a `doctor.sh` check, and a PORTABILITY item for the off-drive `~/.omlx/bin` symlink.
3. **Harder tasks = a ladder, measured** (the 2026-09-25 Spark calibration shape): multi-hunk, then multi-file, then looser briefs. Record each rung's PASS/FAIL and its cause (model / harness / brief). The counter stands: original brief + ONE rebrief, then a Claude seat.
4. **Known 1.5 defect, from the A/B:** it rewrites a bare identifier `+` line among quoted strings as a quoted string (`gap,` → `'gap',`). The checker's A3c catches it. Briefs carrying such a line name it explicitly.
5. **Both local tiers as much as possible:** Spark-first for medium work, 1.5 for what it can be briefed for, Claude seats only to raise, gate and merge. Client scope is unchanged (one client per task; Ornith is the Studio's and is not Datasec's).

**Family:** [[2026-09-16_local-model-is-long-term-and-claude-takes-what-it-cannot-do]] · [[2026-09-25_three-tier-routing-ornith-spark-cloud-always-on]] · [[2026-09-25_spark-calibrate-like-ornith-start-high-oversight]] · [[2026-09-18_ornith-works-constantly-standing-rule]] · [[2026-08-21_challenge-me-when-you-think-im-wrong]] (a recommendation overruled is recorded, and the ruling is executed fully) · [[2026-08-03_go-slow-earn-autonomy]] (rule 5: every grant recorded).
