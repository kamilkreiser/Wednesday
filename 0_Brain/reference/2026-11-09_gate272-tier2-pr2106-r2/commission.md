# Gate 272, tier 2 COMPARE, round 2 of 2: PR 2106 (KS-2117, words only). Commissioned 2026-11-09 07:1x by the 06:3x Wednesday seat. Round 1 was gate 271 (GO WITH NOTES with a MEDIUM false-docs finding, G271-2106-1).

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at TIER 2 depth (through code: diff read, words true against the source). Round 1's verdict: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate271-tier2-batch/verdict.md (read its PR 2106 section whole). Stop line: any byte that changes behaviour (a code byte, an option, a default) = NEEDS TIER 1.

Pins (Wednesday's ls-remote: develop at 07:10:36; RE-READ at start and end, and say whether each moved):
- develop 93028c8151ecdd173c341fb7c23a4b89e381cc04 (PR 2078)
- PR 2106 head 1881831e7d0411d00eb425d29daeb2b13b7d71d6 (Seat T 18th; one commit on round 1's head a8d19bf3918ebe7571bf756fbdeb8cc43e2631de; base develop 15dca468b86f)

READY claims (untested by Wednesday; read whole): /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-18th/mail/ready_ks2117_round2_body.txt

Questions:
1. The words delta a8d19bf3918e..1881831e7d04 (4 files, +18 -20 by the seat): does it close G271-2106-1 (Medium), G271-2106-2 (Low) and G271-2106-3 (Info) as the READY says? Quote the before and after lines.
2. Are the new README note and the approve/initiate/cancel docstrings TRUE against the source at the head? In particular: what client.transfers.approve posts (read the SDK method), and what the transfer service's approve route requires and reads (read approveTransferSchema and the approverId check in services/transfer at develop); is "answered with a 400" what that code does? Is "Reject is a separate route with no SDK method" true? Quote the lines. An overstatement is a finding.
3. No code byte: re-derive the seat's strip-and-compare of the emitted JS for transfers.ts yourself (TypeScript emit with comments removed), with a control that differs on a planted code line and not on a planted comment line.
4. The fragments (cheat + flow, KS-2117) say the same as the README and docstrings; docs-fragments check passes and fails on a planted defect.
5. PR body and the KS-2117 comment d90aa502 (both edited in place by the seat) are true at the head.
6. Merge tree of the head on develop 93028c8151ec: rc 0, and list any open PR sharing one of its 4 paths (the seat says none; verify with a planted control).

Constraints: clone on the boot volume /private/tmp/g272 (QA no-rm; name its size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; load1 under 8; STOP if DevMASTER free space falls under 8 GiB (df at start and end; it read 9.99 GiB at 07:1x).

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate272-tier2-pr2106-r2/verdict.md (if your Write is refused, put the whole verdict in your final message). Line 1 exactly: 'PR 2106: <V>' with V one of GO | GO WITH NOTES | NO GO | NEEDS TIER 1. This is round 2 of 2 under the cap: a NO GO ships the closed instances and tickets the residue, so say per finding whether it is closed, residue, or new. Then FOUND / TESTED / HOW (instrument, controls), NOT TESTED, findings with ids G272-<n>. Findings only; post nothing; mail nothing.
