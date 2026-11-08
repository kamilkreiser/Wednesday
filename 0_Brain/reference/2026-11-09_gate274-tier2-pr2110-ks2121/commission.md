# Gate 274, tier 2: PR 2110 (KS-2121, test-only, Seat T 18th's D3). Commissioned 2026-11-09 07:5x by the 06:3x Wednesday seat.

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at TIER 2 depth (through code: diff read, words true, cells re-run with a planted defect of your own). Stop line: any product byte = NEEDS TIER 1.

Pins (Wednesday's ls-remote 07:49:45; RE-READ at start and end, and say whether each moved):
- develop 93028c8151ecdd173c341fb7c23a4b89e381cc04
- PR 2110 head 2cfbd109db5d6ccf5303e6362c5177b96e916254 (branch feature/ks-2121-transfer-no-cell-compares-the-403-refusals)

READY (untested by Wednesday; read whole): /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-18th/mail/ready_ks2121_body.txt . It originates from a held Spark pass (READY_KS-2121-* in /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/local-model/night/); the seat says the Spark checker's plant (req.path) is id-dependent and reddens four existing R3 cells too, and that a per-door id-free mutant reddens exactly the new cell.

Questions:
1. Test-only: the diff touches only the transfer test file (+15 -0 by the seat); no product, config or docs byte.
2. Does the new cell compare the 403 refusals as KS-2121 asks (read the ticket's words in the READY and the ticket body if you can)? Quote the cell. An overstated test name is a finding.
3. Red-first: on develop the new cell must pass (a pin of correct code) and must go red, by assertion, under a mutant of YOUR OWN that changes exactly the behaviour it pins; show the seat's id-free mutant too; restore by sha. Whole transfer suite: 460 -> 461 cells, 0 failed both sides (re-run).
4. Merge tree of the head on develop 93028c8151ec: rc 0; list open PRs sharing its path (planted control).
5. PR body and the KS-2121 comment named in the READY: true at the head.

Constraints: clone on the boot volume /private/tmp/g274 (QA no-rm; name its size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; load1 under 8; STOP if DevMASTER free space falls under 8 GiB (df at start and end; 9.70 GiB at 07:4x).

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate274-tier2-pr2110-ks2121/verdict.md (or the whole verdict in your final message if the Write is refused). Line 1 exactly: 'PR 2110: <V>' with V one of GO | GO WITH NOTES | NO GO | NEEDS TIER 1. Then FOUND / TESTED / HOW (instrument, controls), NOT TESTED, findings with ids G274-<n> and severity. Findings only; post nothing; mail nothing.
