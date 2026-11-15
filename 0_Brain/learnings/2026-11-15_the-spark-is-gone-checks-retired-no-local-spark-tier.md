---
date: 2026-11-15
type: principle
source: "Kam, Wednesday's terminal, 2026-11-15: 'please start with wiping any of our data from the HP spark. It has to go back to HP and I do not want it to have any of our data on it when it goes back' -> 'doing the factory restore now' -> 'yes, send Tuesday the note that the Spark is gone' -> 'the Spark has gone, retire the checks'"
status: live
tier: W
supersedes: "2026-10-28_never-keep-the-spark-idle-quota-and-capability-data (retired, not superseded in content: its subject no longer exists)"
---

# The Spark is gone: there is no local Spark tier — never route to it, never check it, never nag about it idling

**The lesson:** As of 2026-11-15 the HP loan Spark (hp-loan-spark / ZGX-Nano-G1n / zgx-15d5) has been wiped and returned to HP. Every rule that routes work to the Spark, asks for it to be kept busy, or checks its tunnel is **inactive**. Model choice is now Ornith (local, where it still runs), Sonnet or Opus, by `fleet/specs/model-routing.md` with the Spark column read as "not available".

**What was retired, 2026-11-15 (each file has a `.pre-1115-spark-retired` copy beside it):**
1. `2_Project_Files/fleet/send_brief.sh` — the spark_status.py line on every send (disabled with `false &&`).
2. `2_Project_Files/doctor.sh` — the Wednesday tunnel + allocation WARNs (now one ✓ "Spark retired" line) and Friday's ZGX endpoint check. The CAPACITY check beside them stays live. Verified: doctor rc 0, prints the retired line.
3. `Launch_Wednesday.command` boot step 10c — now reads RETIRED.
4. `Launch_New_Machine.command` — the NVIDIA Sync / `ssh Spark` MANUAL step.
5. The rule `2026-10-28_never-keep-the-spark-idle-quota-and-capability-data.md` — status retired.

**How to apply:**
1. A Spark-first / Spark-max / Spark-target line in any older lesson (14 other files carry "spark" in the name, 2026-09-23 to 2026-11-12) is **historical**: do not act on it; route the work to the next tier the routing spec names.
2. Never run `local-model/spark/tunnel.sh`, `round.sh` or `queue.sh`, and never brief "Spark" in a launch receipt.
3. Our records from the box are in `0_Brain/reference/2026-11-15_spark-return-archive/` (105 files, 8.3 MB, no weights) — read there, not on the box.
4. If Kam gets a new local box, the checks come back by removing the `false &&` guards — a new ruling, not an assumption.

**Family:** [[2026-10-28_never-keep-the-spark-idle-quota-and-capability-data]] (retired) · [[2026-09-25_three-tier-routing-ornith-spark-cloud-always-on]] (its Spark tier is gone) · [[2026-11-12_spark-for-harness-and-token-heavy-simple-tasks]] (historical)
