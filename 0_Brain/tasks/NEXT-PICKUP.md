---
date: 2026-10-26
type: pickup
scope: SECUURA + all general/generic work. Datasec is TUESDAY's (Mac mini).
status: live
supersede: REPLACED WHOLESALE by the Mon 26 Oct laptop seat at its 53% checkpoint. Previous: NEXT-PICKUP.md.pre-1026-0855. Replace wholesale; never stack.
---

# NEXT PICKUP (Mon 26 Oct, written at the 53% checkpoint; gauge 7d ~5%)

## 0. MACHINE: Wednesday runs on the LAPTOP (Kamils-MBP, 32 GB) until Kam's new machine arrives
- Fixed today (see today's note, 07:54 block): dashboard-cloud venv (python@3.12 installed), live_chat_poll, 7 launchd jobs from this drive, rsync, usage publisher, Spark tunnel alias fallback (`ZGX-Nano-G1n`), python@3.14 -> 3.14.9.
- ⚠ `brew upgrade python@3.14` DROPPED `/opt/homebrew/bin/python3`; Wednesday re-created it by hand (`ln -s ../opt/python@3.14/libexec/bin/python3`, same for pip3). If `python3 --version` says 3.9, that link is gone again.
- Ornith is NOT available here (Studio-only, paused since 10-12). The Spark works: http://127.0.0.1:47788.
- Open question for Kam at a natural moment: does the Studio still run its launchd jobs? A 05:30 shift-change mail came from somewhere else today; with this laptop's jobs now installed, duplicates are possible from tomorrow.

## 1. LIVE FLOOR (refreshed at the 65% checkpoint, ~09:27 AEDT; panes in tmux `fleet`)
- DONE: KS-1719 (Peter's ask). PR #1687 merged as 7ce64f5d6739 (Wednesday read origin), two tier-2 gate rounds, Peter's comment 5f02798a posted, ticket left In Progress on him. G 20th scored 0.96, pane closed. Kam has a paste-ready reply for Peter on the panel.
- %3 `Secuura/Blockchain-D` = D 31st, Opus 5.5: kintsugi build k1 (heartbeat at Secuura/Blockchain 5_Project_History/2026-10-26_seatD-31st/evidence/heartbeat.kintsugi.k1.txt), then demo ONLY after kintsugi is verified (Kam 08:58, relayed). Ack an idle wake only after reading a MOVING heartbeat figure.
- %4 `Secuura/Blockchain-R` = R, Sonnet 5.5: five raise PRs from held Spark READYs (KS-1391, KS-1289, then KS-1548, KS-1524, KS-1649). KS-1649 changes the PUBLISHED developer portal: 3,000 is CONNECTOR_RATE_LIMIT_DEFAULT (range 1-10,000); the gate must weigh the wording.
- %5 `Secuura/Blockchain-K` = K, Opus 5.5: KS-1683 (vc-issuer list/by-hash bound to the creator), comment-only exception granted for 3 comments. Tier-1 Opus gate when READY.
- %6 `Secuura/Blockchain-J` = J, Opus 5.5 (switch at its plan prompt): KS-1717 anchoring x-emitter-internal guard. DESIGN FIRST: its plan proposes options; if a new secret/identity changes the trust model, card Kam.
- Drafters (Agent tool, Sonnet): (1) Spark rung-3/4 batch + round.sh/brief_lint eval-warning fix (it is editing spark/round.sh NOW: do not commit that file mid-edit; safe_pull refuses until it lands); (2) the SPARK GATE pilot (local-model/gate/, calibrated on PR #1687 r1/r2 vs the Sonnet verdicts). Kam's conditional grant: learnings/2026-10-26_spark-gate-pilot-if-it-works-put-it-into-practice.md.
- Spark today: 5 tasks, 5/5 round-1 PASS, all read and held. Rung 1/2 pool dry at the tip (~40 screened).

## 2. OWED, in order
1. Gate verdict -> Wednesday's completion check -> GO merge to G 20th (TESTED grant) or a fix round (round 2 of 2). Then clear Peter's comment text and have G post it. KS-1719 stays assigned to Peter.
2. D 31st STATUS mails: verify each box at source; KS-741 to Done after demo is live (Done = tested + works + deployed).
3. Spark: KS-1391 PASS held -> night/READY_KS-1391-...-PASS-7of7_2026-10-26.diff.md. KS-1289 round running/ran (check spark/state + runs/spark_secuura_2026-10-26_ks_1289_p1). A Sonnet RAISE seat (row C1) raises the held READYs as PRs; needs a pane name not in use (G and D are live).
4. Brief item for the next Secuura seat: the Secuura launcher's step 8 names coagent@, which the project key cannot read (NotFound parses as "0 messages").
5. Ledger rows past ~3 days (10-21..10-23) to archive at the wrap (rule 3c, conservation asserted).

## 3. IN FORCE (read the files, not this list)
Usage is a GUIDE (2026-10-22). Routing v1.0 (Opus/Sonnet/Spark per table). October deploy grant (extended until further notice). TESTED merge grant; merge-and-archive (2026-10-10). Done = tested + works + deployed (2026-10-12). Kam ruled wed-morning-plan-1026 = a (carry on).
