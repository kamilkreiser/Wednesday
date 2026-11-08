# Gate 275, TIER 1 BATCH (Opus): PR 2111 (KS-2109, D5) and PR 2112 (KS-2120, D6). Both by Seat T 19th; both are comment/doc changes on security-surface files (trustHeaders.ts, transferAccess.ts) plus fragments. Commissioned 2026-11-09 09:3x by the 08:0x Wednesday seat.

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at FULL tier-1 depth (the files are on auth/role and transfer-access surfaces even though the change is comments and docs).

Pins (Wednesday's ls-remote 09:37:37; RE-READ at start and end, and say in the verdict whether each moved):
- develop a1bfe7a7df25005eaec4a5d42028889fb3b5e224 (PR 2105)
- PR 2111 head 4fff98cb12f2ae5e11619ef5d38176d7c16a45a5 (KS-2109: trustHeaders.ts one comment line, AGENT-DOCUMENT-OPERATION-RULES.md one line, cheat + flow fragments; cut on 425ea1d3df0f)
- PR 2112 head ba5cb57dcecaeeff6e0bbc226597c40d19141afc (KS-2120: one transferAccess.ts comment + fragments; cut on 64671e97ce62)
- PR 2109 head 5350041b426d3e3ee42d5bd812a17b07a2718c3d (OPEN, not in this gate: it adds two cells to packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts, which D5's checks read)
- PR 2110 head 2cfbd109db5d6ccf5303e6362c5177b96e916254 (OPEN, not in this gate: it adds one cell to the ks2081 doors test, which D6's checks read)

READY claims (untested by Wednesday; read each whole), in /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-19th/mail/ : ready_ks2109_body.txt and ready_ks2120_body.txt. Their source briefs: the Spark-free D-rows of T 18th's HANDOVER (/Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-18th/HANDOVER.md); api-gateway/src/index.ts 327-329 was RULED OUT of D5 and the PR body says so.

Questions, per PR:
1. Does the diff do ONLY what the READY says? Read every changed line. A comment change on a security file: is the new comment TRUE at the head (quote the code it describes)? An overstatement or a wrong claim about the code is a finding.
2. Comment-only proof: confirm the TypeScript emit with comments stripped is identical to develop's for the changed .ts file (an independent method, plus a control that DOES differ).
3. D5 / PR 2111: run the ks1536 guard test at the head AND on the UNION of PR 2111 with PR 2109's version of packages/shared/src/__tests__/ks1536-one-role-vocabulary.test.ts (T 19th did not run the union; it is this gate's question). Same red set as develop.
4. D6 / PR 2112: run the transfer suite and the ks2081 doors test at the head AND on the union with PR 2110's version of that test file.
5. The fragments and the AGENT-DOCUMENT-OPERATION-RULES.md line: true, and do they pass `node Blockchain/Dev/scripts/docs-fragments.mjs check`? D5's fragments carry the key 'KS-1536' hyphenated once each: say whether that has any effect (T 19th says file content only; Wednesday's default is to leave it).
6. Merge tree of each PR on develop a1bfe7a7df25; the two are file-disjoint by T's census: verify with a planted overlap control; list open PRs sharing any path.
7. Ticket comments e4a94ed6 (KS-2109) and 16d3f464 (KS-2120) named in the READYs: true at the head.

Constraints: clone on the boot volume /private/tmp/g275 (QA no-rm; name its size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; load1 under 8; DevMASTER read 107 GiB free at 09:3x.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate275-tier1-t19-d5d6/verdict.md (if your Write is refused, put the whole verdict in your final message). Line 1 exactly: 'PR 2111: <V>; PR 2112: <V>' with V one of GO | GO WITH NOTES | NO GO. Then per PR: FOUND / TESTED / HOW (instrument, controls), NOT TESTED, findings with ids G275-<PR>-<n> and a severity. Findings only; post nothing; mail nothing.
