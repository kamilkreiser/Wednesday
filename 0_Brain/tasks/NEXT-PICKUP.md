---
date: 2026-10-26
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE by the Mon 26 Oct laptop seat at ~79% before its rotation (~11:3x AEDT). Previous: NEXT-PICKUP.md.pre-1026-1130 (and .pre-1026-0855). Replace wholesale; never stack.
---

# NEXT PICKUP (Mon 26 Oct ~11:30 AEDT; new account since ~11:2x, gauge 7d ~0-1%)

## 0. READ FIRST
- Machine = the LAPTOP (Kamils-MBP, 32 GB) until Kam's new Studio arrives. Fixed today: dashboard venv (python@3.12), live poller, 7 launchd jobs, rsync, usage publisher, Spark tunnel alias (ZGX-Nano-G1n), python@3.14.9 (+ a hand-made /opt/homebrew/bin/python3 link: if `python3 --version` says 3.9 it is gone again). Ornith unavailable here. Docker Desktop running.
- Kam switched accounts (/login) and said "please continue": the 10-18 grant is re-read as reaffirmed (EXPIRING-GRANTS).
- Load rule: launch at load1 < 7 (watch it; R/K/J/D plus gates pushed it to 11-12).
- Every push of Blockchain/Dev code needs the per-command ssh KEEPALIVE (GitHub drops idle ssh at ~364 s; preflight is 11-15 min): fleet/STANDING_LINES.md.

## 1. IN FLIGHT (panes in tmux `fleet`)
- %4 `Secuura/Blockchain-R` (Sonnet 5.5): PR #1688 MERGED 00:29:58Z as develop 28dac5c12ba5 (verified at origin); K and J told to resume. NOW: R pushes its NINE branches (KS-1391, 1289, 1548, 1524, 1649, 1716, 1560 [--recount only, approved], 1513, 1527 sequenced) and mails READY FOR GATE -> gates: tier 2 Sonnet with local-model/gate/spark_gate.sh first (+ Spark review as shadow); KS-1649 (published developer portal) and KS-1716 (a pre-push gate script) need a careful read.
- %5 `Secuura/Blockchain-K` (Opus 5.5): KS-1683 built red-first (13/13 mutants, 840 Postgres comparisons), holding; handover + bundle written. After #1688 merges: merge develop in, push with keepalive, PR, READY -> TIER-1 Opus gate (authorization surface).
- %6 `Secuura/Blockchain-J` (Opus 5.5): KS-1717 HMAC (Kam ruled b) committed at 708be64ccafd, holding. After #1688: push with keepalive, PR, READY -> TIER-1 Opus gate. Stated residual (tell Kam when the PR lands): same-body replay inside 60 s accepted (no nonce cache). MERGE + the new EMITTER_SIGNING_SECRET go out TOGETHER in a deploy round (Kam's card text); never merge it alone.
- %3 `Secuura/Blockchain-D` (Opus 5.5): kintsugi build k1 at 13/15 (~00:23Z), 0 failures, floor 12,000 MB never approached; then swap one-by-one, live check, KS-535 after, STATUS -> DEMO only after kintsugi is verified (Kam 08:58 verbatim, relayed). KS-741 -> Done after the deploy. Heartbeat: Secuura/Blockchain 5_Project_History/2026-10-26_seatD-31st/evidence/heartbeat.kintsugi.k1.txt (ack an idle wake only on a MOVING figure).

## 2. OWED
1. The above chain. Every READY: gate, then Wednesday's completion check, then merge GO under the TESTED grant.
2. Spark: pool dry at rung 4 (why in spark/queue.md). Next lift: extend the builder to loose TS briefs or a Postgres-backed checker, or new tickets. Spark gate pilot: CALIBRATION 1 recorded (runner in practice; Spark review shadow on tier 2); build the 5 named improvements before calibration 2.
3. Kam-facing: tell him the KS-1717 replay residual when J's PR lands; KS-1724/1725 priorities are unset (his to rank); baseline expires Mon 2026-11-09.
4. Ledger: rows 10-21..10-23 are past rule 3c (archive at the next wrap, conservation asserted). Today's rows: 6 (all [W]).
5. Brief items for Secuura's own launcher (the project's file, via a brief): step 8 names coagent@ (NotFound reads as empty); step 7 orders POST /api/seen on the extranet; the arms script local-model/gate/tests/test_spark_gate_arms.sh does not refuse missing args (Wednesday's own file: fix).
6. Possible duplicate launchd jobs if the Studio still runs its own (a 05:30 shift-change mail came from elsewhere today): ask Kam once at a natural moment.

## 3. IN FORCE (read the files, not this list)
Usage is a GUIDE (2026-10-22). Routing v1.0. October deploy grant (until further notice). TESTED merge grant; merge-and-archive (2026-10-10). Done = tested + works + deployed. Max agents + Spark always running (09-13 lesson, 10-26 extension). Spark-gate conditional grant (2026-10-26).
