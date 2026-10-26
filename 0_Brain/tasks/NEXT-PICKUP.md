---
date: 2026-10-26
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE by the Mon 26 Oct 12:0x successor seat at its 65% checkpoint (13:4x AEDT). Previous: NEXT-PICKUP.md.pre-1026-1348 (and .pre-1026-1130). Replace wholesale; never stack.
---

# NEXT PICKUP (Mon 26 Oct ~13:48 AEDT; account gauge 7d ~1%; develop = c2505d5c6fe0)

## 0. READ FIRST
- Machine = the LAPTOP (Kamils-MBP, 32 GB). Ornith unavailable here. Docker Desktop was RESTARTED 12:1x (its VM had wedged at ~900% CPU, load 97). If load climbs with low CPU, it is disk wait (Spotlight/mds indexing new clones, git); the launch rule is load1 < 7, enforced by background waiters, never by guessing.
- Every Blockchain/Dev push uses the per-command ssh KEEPALIVE (GitHub drops idle ssh at ~364 s): fleet/STANDING_LINES.md. The Secuura launcher does NOT write the keepalive in its "[F-02] No SSH identity" branch (R's finding, recorded on KS-1149): OWED, a brief item for a Secuura seat.
- Floor (tmux `fleet`): %3 D, %4 R, %5 K, %1 fleet-monitor (J's %6 closed 14:3x). All on the shared inbox secuura-blockchain@; every mail names its seat.
- **Push rule, every seat:** one pre-push at a time on this laptop. The check is `pgrep -fl '^/bin/sh [.]githooks/pre-push'` (the unanchored form self-matches waiters; ledger 14:0x).
- **macOS idle work** (mediaanalysisd, Aerial wallpaper) saturated the box at 14:1x; `caffeinate -u -d -i -s -t 7200` (pid 45194) stopped it and LAPSES ~16:18. Re-arm it if seats are still live. If load is high with low disk I/O, sum CPU by command (`ps -Ao pcpu=,comm=`) before blaming anything.
- **The Spark is DOWN for DeepSeek during the A/B Ornith phase** (results_ornith.tsv exists in spark-ab/). Its local checker runs drive the laptop's load (~8 cores of node).

## 1. IN FLIGHT
- **D** `Secuura/Blockchain-D` (Opus): kintsugi DEPLOYED + verified at 1ae6f17d19a8 (00:52Z STATUS, 25/25 swaps, KS-535 OK, anchoring REAL). DEMO build d1 at batch 11/15 at 02:46Z (heartbeat: Secuura/Blockchain 5_Project_History/2026-10-26_seatD-31st/evidence/heartbeat.demo.d1.txt); then swap, live check, KS-535 after, STATUS. Ack an idle wake only on a MOVING heartbeat line. After demo: KS-741 -> Done (deployed); D's wrap.
- **R** `Secuura/Blockchain-R` (Sonnet; UPDATE 15:0x: 5 of 9 on origin, pushes at load1 < 10, one preflight at a time): the nine Spark patches. On origin with PRs: KS-1716 #1689 (pushed with NO preflight leg, by the hook's design; its gate must run the real pre-push hook), KS-1560 #1692, KS-1391 #1693; KS-1289 on origin (048b9d5fa48b), PR opening. Remaining, SERIALISED (one R preflight at a time, none while another seat's pre-push hook runs): KS-1513 (once refused by the printf|grep -q tell), KS-1527, KS-1548, KS-1524, KS-1649. READY FOR GATE comes as ONE batch mail when all nine are up. Then: ONE tier-2 batch gate (Sonnet + spark_gate.sh runner first; KS-1649 developer-portal text and KS-1716 hook script need a careful read). AFTER the nine: R's small PR under KS-1728 rewriting the 4 observed `printf|grep -q` lines to a pipe-free form.
- **K** `Secuura/Blockchain-K` (Opus): #1691 (KS-1683) MERGED as c2505d5c6fe0, scored 0.96. NOW KS-1722 (blank ?proposerId= lists all proposals): plan GO'd 13:2x, fix (a) = a route 400 from one schema for proposerId/category/status + the openapi declaration (0 open PRs touch secuura-api.yaml, K measured). Red run 30 red / 13 green. NEXT: commit red, fix, READY -> tier-1 Opus gate. K's rule-7 wrap notify (KS-485 Peter, KS-772 Stuart, one each) is authorised at K's wrap.
- **K, update 14:5x:** KS-1722 is PR #1696 at 9f567635fba5 (READY 03:05Z); tier-1 Opus gate RUNNING (launched 14:21), verdict -> 0_Brain/reference/2026-10-26_gate-pr1696-ks1722/verdict.md. On its verdict: completion check, then merge GO (re-pin head + develop) or a fix round. K filed KS-1729, KS-1731, KS-1732. K's own ctx was 69% at 14:4x.
- **J WRAPPED 03:37Z, pane %6 CLOSED, scored 0.95.** KS-1717 PR #1690 is FINAL at 83b9b5f52cac (both gate rounds GO WITH NOTES; N1 docs commit verified as 2 hunks). Earlier history: (round 2: bearer bound into the HMAC, 32-char floor cells, residual text exact; verdict_round2.md). **MERGE IS HELD: merge + the new EMITTER_SIGNING_SECRET go out TOGETHER in one deploy round (Kam's card secuura-ks1717-new-emitter-secret-1026). Kintsugi/demo set the secret in the box .env (compose passes it); the Azure path is KS-1730.** Post-deploy smoke: both services log `[emitter-guard] ACTIVE`; one create writes exactly one provenance row.
- **UPDATE 15:0x — background AGENTS in this seat (they DIE at a rotation; a successor re-commissions from the files named):**
  1. **DeepSeek QUANT test on the Spark** (Kam ~14:59, "maybe test a slightly smaller quant"): brief `2_Project_Files/local-model/spark-ab/BRIEF_QUANT.md` (claimed). **🔴 If the seat rotates mid-run, DeepSeek may be STOPPED: FIRST run `ssh ZGX-Nano-G1n 'docker ps'`; if `deepseek-v4-flash-spark-deepseek-v4-flash-1` is not Up, stop any other model container (never remove it), then `ssh ZGX-Nano-G1n 'docker start deepseek-v4-flash-spark-deepseek-v4-flash-1'`, wait for health, and prove it answers (`curl -s http://127.0.0.1:8888/v1/models` on the box = deepseek-v4-flash-0731).** Then re-commission from the brief. The report text comes back in the agent's final message: save it to `0_Brain/reference/2026-10-26_deepseek-quant-on-spark/report.md`.
  2. **Tier-1 gate for PR #1696 (KS-1722)**, verdict -> `0_Brain/reference/2026-10-26_gate-pr1696-ks1722/verdict.md`. If it is missing after a rotation, re-commission (round 1, head 9f567635fba5, re-pin first). K holds at READY.
  3. **Research: Apple Silicon inference speedups** (Kam 15:04:51), text -> `0_Brain/reference/2026-10-26_apple-silicon-inference-speedups/report.md`, then answer Kam on the panel. Re-commission if lost.
- **D 31st WRAPPED, pane %3 CLOSED, scored 0.96**: both boxes run 1ae6f17d19a8. K was asked (15:05) to move KS-741 to Done and post D's two deploy notices (KS-485 Peter, KS-772 Stuart) verbatim from D's wrap mail.
- **Ornith 1.5 122B vs DeepSeek V4 Flash: DONE** (report `0_Brain/reference/2026-10-26_ornith122b-vs-deepseek-spark/report.md`: DeepSeek 16/23, Ornith 12/23; DeepSeek restored and verified; Kam told). Original line, for history:
- **Ornith 1.5 122B vs DeepSeek V4 Flash on the Spark** (Kam 12:32:27): Opus teammate (Agent) on 2_Project_Files/local-model/spark-ab/BRIEF.md (claimed via wed_claim). Report -> 0_Brain/reference/2026-10-26_ornith122b-vs-deepseek-spark/report.md. **DeepSeek MUST be restored and proven before the job is called done.** If the seat rotates and no report has landed: read the Spark (`ssh ZGX-Nano-G1n 'docker ps'`), restore DeepSeek per the brief's step 6 if it is down, then re-commission from the brief. The 10-08 Qwen 122B leg-2 hard-task set was handed to it.

## 2. OWED
1. The chain above. Every READY: gate -> Wednesday's completion check -> merge GO under the TESTED grant (re-pin head + develop first).
2. Spark: queue empty for a measured reason (screen of 8 new tickets, 0 briefable: 0_Brain/reference/2026-10-26_spark-screen-new-tickets/report.md). The Spark is busy with Kam's A/B test until it reports.
3. Kam-facing, when it happens: the deploy round that carries KS-1717 + the secret (tell him; demo under the October grant after kintsugi verified); the A/B report as a table.
4. Ledger: rows 10-21..10-23 are past rule 3c (archive at the next wrap, conservation asserted). Today's rows: 7 [W].
5. Brief items for Secuura's own launcher (the project's file, via a brief to a Secuura seat): step 8 names coagent@; step 7 orders POST /api/seen; and R's finding (d), the keepalive missing in the F-02 branch.
6. Possible duplicate launchd jobs if the Studio still runs its own (a 05:30 mail came from elsewhere today): ask Kam once at a natural moment.
7. decision_queue's prior-ruling refusal prints other clients' card TITLES into this seat (seen 12:2x): a tooling fix to make the refusal filter by client. Shared tooling: claim first.

## 3. IN FORCE (read the files, not this list)
Usage is a GUIDE (2026-10-22). Routing v1.0. October deploy grant (until further notice). TESTED merge grant; merge-and-archive (2026-10-10). Done = tested + works + deployed. Max agents + Spark always running (09-13 lesson, 10-26 extension). Spark-gate conditional grant (2026-10-26). Advisory baseline zod/msal to Mon 2026-11-09.
