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

## 1. LIVE FLOOR (panes in tmux `fleet`)
- %2 `Secuura/Blockchain-G` = Seat G 20th, SONNET 5.5. KS-1719 (Peter's ask; Kam: "prioritise this from Peter"). PR #1687 head 02399bd018aa READY FOR GATE. Filed KS-1720 (mypy aborts on develop) + KS-1721 (symlinked-venv test fails on Linux). Waiting for the gate verdict. Peter's ticket comment is DRAFTED at Secuura/Blockchain 5_Project_History/2026-10-26_seatG-20th/ks1719_peter_comment_DRAFT.md — post ONLY after the gate has read every sentence and Wednesday clears it.
- %3 `Secuura/Blockchain-D` = Seat D 31st, OPUS 5.5. Deploying develop 1ae6f17d19a8 to kintsugi then demo (card secuura-kintsugi-deploy-held-at-99pct-1023's default fired; card withdrawn). GO sent 21:40Z: disk floor 12,000 MB; demo-service held + ticket; host keys TOFU UNVERIFIED (recorded in its handover). Expect STATUS mails per box.
- QA GATE (Agent-tool subagent, Sonnet, tier 2 round 1) on PR #1687 -> verdict at 0_Brain/reference/2026-10-26_gate-pr1687-ks1719/verdict.md. Its main question: does the helper's new cancel of QUEUED proposals stay bounded to test residue?

## 2. OWED, in order
1. Gate verdict -> Wednesday's completion check -> GO merge to G 20th (TESTED grant) or a fix round (round 2 of 2). Then clear Peter's comment text and have G post it. KS-1719 stays assigned to Peter.
2. D 31st STATUS mails: verify each box at source; KS-741 to Done after demo is live (Done = tested + works + deployed).
3. Spark: KS-1391 PASS held -> night/READY_KS-1391-...-PASS-7of7_2026-10-26.diff.md. KS-1289 round running/ran (check spark/state + runs/spark_secuura_2026-10-26_ks_1289_p1). A Sonnet RAISE seat (row C1) raises the held READYs as PRs; needs a pane name not in use (G and D are live).
4. Brief item for the next Secuura seat: the Secuura launcher's step 8 names coagent@, which the project key cannot read (NotFound parses as "0 messages").
5. Ledger rows past ~3 days (10-21..10-23) to archive at the wrap (rule 3c, conservation asserted).

## 3. IN FORCE (read the files, not this list)
Usage is a GUIDE (2026-10-22). Routing v1.0 (Opus/Sonnet/Spark per table). October deploy grant (extended until further notice). TESTED merge grant; merge-and-archive (2026-10-10). Done = tested + works + deployed (2026-10-12). Kam ruled wed-morning-plan-1026 = a (carry on).
