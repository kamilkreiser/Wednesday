---
date: 2026-09-14
type: analysis
source: "Kam, panel 11:12 — 'analyze the system performance while we go through multiple agents and multiple tasks, and identify whether we have enough room to run a local model … which model … whether that model would be good enough to handle certain tasks in linear'"
status: measured 11:1x under the live fleet (3 seats + 1 QA gate + 1 drafter + the coordinator); a deeper profile is owed by a subagent at the next quiet hour
---

# Local-model headroom on the Studio — measured under fleet load

## FOUND (measured 11:1x AEST, `sysctl` / `top -l 1` / `vm_stat` / `df`)
- **Machine:** Mac Studio M3 Ultra — 28 CPU cores, 60 GPU cores, **96 GiB unified memory**, 1.5 TiB free on DevMASTER, 145 GiB free on the boot disk. `ollama` is already installed (`/opt/homebrew/bin/ollama`); no local model is running.
- **Now (fleet: s220 merge seat, s221 builder, one tier-1 QA gate `%19`, one gate drafter, the coordinator, Chrome, Postgres):** 71 GiB "used" of which ~45 GiB is INACTIVE file cache (reclaimable), 6 GiB wired, 24 GiB unused; **CPU 80 % idle, load 7.8** (1-min).
- **Peaks today:** load **28** at 07:39–08:04 when five builders booted while Spotlight's `mds` + 10 `mdworker` ran at ~80 % CPU each; load 17–22 through the morning with 3–4 tier-1 gates running node suites in parallel. Suites time out past ~load 20 (the fleet rule). Spotlight indexing has been the largest single consumer all day — unmeasured which volume it indexes; excluding DevMASTER from Spotlight (`sudo mdutil -i off /Volumes/DevMASTER`, Kam's hands) is the cheapest headroom on the box.

## HEADROOM VERDICT
- **A ~30B-class model fits at ALL times:** Q4 weights ≈ 17–20 GiB, inside the 24 GiB unused even at the morning peak; inference on the 60-core GPU with 800 GB/s unified bandwidth.
- **A 70B-class model (≈ 40 GiB Q4) fits only when the gates are not running suites** — it would take the inactive cache and push the fleet into compression at peaks; not for daytime.
- **The real contention is not memory, it is the shared CPU/GPU/bandwidth with the gates' test suites:** a local model generating at full tilt while three tier-1 gates run `vitest`/`jest` will slow both; the load rule (< ~16 before a tier-1 gate) has to count the model as a seat.

## WHICH MODEL (Wednesday's read — models newer than the 2026-05 knowledge line are unmeasured; test before choosing)
1. **Qwen3-30B-A3B (MoE, ~18 GiB Q4)** — the workhorse candidate: 3B active parameters → fast (tens of tok/s), tool/function calling, long context; fits at every hour.
2. **Qwen3-32B dense (~20 GiB Q4)** — better reasoning per token, ~3× slower; the "quality" alternative for the same memory.
3. **Gemma 3 27B (~17 GiB Q4)** — strong instruction following, weaker tool calling in Wednesday's experience of the family.
4. **Llama 3.3 70B (~40 GiB Q4)** — only for off-peak batch work.
Kimi-K2 (the CLAUDE.md "parked" mention) is a ~1T-parameter MoE — not a local candidate on this box.

## GOOD ENOUGH FOR LINEAR TASKS? — by task shape, the same rule as the Sonnet tiering
- **Yes, behind a harness that checks:** state-line reads and census diffs; facts-only comments from a template (the s218/s222 shape) with read-back by id; classifying tickets against a written predicate with verify-at-source; board reports and counts through `board_count.sh`; drafting the dedupe/residue tables for a human to rule on. Every one of these is checked by a mechanism after the model (census diff, read-back, `board_count`), so a weaker model's slips are caught before they land.
- **No:** rulings on security tickets, brief writing that re-derives facts from code, QA gates, anything where the model's own judgement is the claim. Today's catches (the H-launder Major, three of Wednesday's classification errors) came from Opus-grade source reads.

## RECOMMENDATION
- **Push through at the current pace this week (Kam's stated preference) — the headroom is there for a 30B-class model at any time, so the switch can start toward the end of the week without buying hardware.** First step when he says go: `ollama pull qwen3:30b-a3b` (and `qwen3:32b`), a 30-minute measured bake-off on THREE real board tasks from today's records (a state-line census of 20 tickets; a facts-only closing comment from s222's template; a class-h residue classification against the sweep's predicate), scored against what the Opus seats produced — numbers, not impressions; then a launcher entry so a local-model board seat runs under the same gates (`send_brief.sh`, census, read-back) as everything else.
- Owed before any of it: the Spotlight exclusion (Kam's hands), and a 24-hour load profile written by a subagent (`top` samples every 5 min) so the "off-peak" window is measured, not assumed.
