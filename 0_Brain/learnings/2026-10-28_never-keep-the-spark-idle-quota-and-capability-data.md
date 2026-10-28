---
date: 2026-10-28
type: grant
source: "Kam, Wednesday's terminal (laptop), 2026-10-28 ~12:0x AEDT, verbatim: 'That is very good to hear.  thank you for the feedback and this helps with making decisions going forward.  There is another reason to use the spark - I am hopin that it makes the weekly quota last the full week.  I see that allocating to Sonnet is probably going to help a large amount but just to make sure, please create a new rule for now - never keep the spark idle.  Use it for one thing or another.  The speed will matter if they are related tasks but with a board of 400 I am sure we can find enough tasks that do not relate to other work.  Giving it tasks it fails on is an overhead for you (sorry) but it also gives us more real world information about its capability which is good.  Please capture this as well'"
status: live
tier: W
expires: none stated ("for now" — until Kam changes it)
extends: 2026-09-18_ornith-works-constantly-standing-rule (Ornith) and 2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry — now explicitly the SPARK
---

# NEVER keep the Spark idle — use it for one thing or another; a failed task is data, not waste; pick work that does not relate to other in-flight work

**The operative case, so the headline matches it:** I am at a boot, a checkpoint, or between waves, and the Spark has no round running. **That is the rule being broken, not a gap to notice later.** Before anything else at that boundary: is the tunnel up (`local-model/spark/tunnel.sh check`), is a round queued, and if not, what can I give it from the 400+ open tickets that does NOT touch code another seat is changing?

**Kam's two reasons, both his:**
1. **The weekly quota should last the whole week.** Every task the Spark does is a task a Claude seat does not spend allowance on. Sonnet routing helps a lot; the Spark is the extra margin "just to make sure".
2. **Real-world capability data.** Giving it tasks it may fail is an overhead for me, and Kam accepts that overhead explicitly ("sorry") because each attempt measures what it can do. A failure is a calibration row, not a wasted round.

**How to apply:**
1. **Idle is the failure, not the failed round.** The bar for briefing the Spark is LOWER than the old one-file / spelled-out / no-security screen: that screen is how the Spark sat idle on 2026-10-27/28 with "0 briefable". Widen it: multi-file test-only work, comment and doc fixes, test hardening, filing-list items, second-opinion reviews, mechanical gate halves. A task it fails on is still allowed; it is recorded in `done.md` with what it got wrong.
2. **Independence over speed.** The Spark is slower; give it work that no other seat is waiting on and that does not touch files an in-flight PR changes (check the open PRs' file sets before queuing). Related or blocking work stays with Claude seats.
3. **The 2026-10-26 gate pilot is part of "never idle"** ([[2026-10-26_spark-gate-pilot-if-it-works-put-it-into-practice]]): every gate runs `local-model/gate/spark_gate.sh` first, and every tier-2 Claude gate gets a Spark shadow review. Those count as Spark work.
4. **Check at every boot and checkpoint**, the same way the inbox is checked: tunnel up, queue non-empty or a round running. If neither, brief the next task before starting new Claude work. The tunnel dropping silently is a known cause (it was DOWN on 2026-10-28 until 12:0x, nothing re-opened it).
5. **Unchanged:** the Spark never merges; its passes are raised, gated and GO'd as before; one client's content per task (Secuura only); signature classes stand.
6. **Report it:** the morning card says how many Spark rounds ran, passed and failed since the last report — counts from `done.md`, not memory.

**Why this was needed (the honest part):** the "never idle" rule already existed for Ornith (2026-09-18) and the gate pilot was ruled on 2026-10-26, and on 2026-10-28 I used neither: the Spark's tunnel was down, I did not check it, I ran two gates without the Spark half, and then described the Spark's capability to Kam from the 10-27 SSD experiment instead of its own `done.md` (9/9 PASS on 10-26, 2-5 min a round). Ledger rows 2026-10-28.

**Family:** [[2026-09-18_ornith-works-constantly-standing-rule]] · [[2026-09-15_never-idle-the-gatekeeper-widens-the-harness-when-the-pool-runs-dry]] · [[2026-10-26_spark-gate-pilot-if-it-works-put-it-into-practice]] · [[2026-09-25_three-tier-routing-ornith-spark-cloud-always-on]] · [[2026-09-18_ornith-is-cheap-the-brief-is-the-cost]] · [[2026-09-14_do-not-guess-a-comparison-a-citation-you-did-not-open-is-a-guess]] · [[2026-08-09_an-enforcement-you-must-arm-is-not-one]]

## MECHANISM (Kam, terminal ~12:1x the same day: "keep the rule and maybe introduce an allocation check for local LLM into your wakeup procedure")
- `2_Project_Files/fleet/spark_status.py` prints `SPARK: tunnel · queue · drainer · round · last` and, when no round is running and the queue is empty or undrained or the tunnel is down, `SPARK: ⚠ IDLE … allocate a task NOW`. Always exits 0. Arms run 2026-10-28 12:1x: empty/no drainer → IDLE; queued + live drainer → not idle; round running → not idle; dead drainer pid + queued → IDLE naming queue.sh; corrupt last_round.json → "status unreadable", rc 0.
- **Rides three wake points:** `doctor.sh` (every boot: WARN "Spark IDLE" with the fix; proven firing live at 12:1x, "IDLE since last round 9841 min ago" — the Spark had not run a round since 2026-10-21), `fleet/send_brief.sh` (every send, beside the Ornith line; proven printing "round LIVE pid 60423" while the drafter's control round ran), and `Launch_Wednesday.command` boot step **10c** (quote/backtick counts unchanged 674/90; swapped in by mv so the running launcher was not edited in place; backups `.pre-1028-sparkalloc` on all three files).
