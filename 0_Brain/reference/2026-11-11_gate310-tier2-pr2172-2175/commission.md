# Gate 310, TIER 2 (Sonnet, routing v1.0 tier-2 row), ONE batched session: R 98th round 1 = PR 2172 (KS-2158), PR 2173 (KS-2085), PR 2174 (KS-2156), PR 2175 (KS-1928). Four PRs, one verdict file with one section per PR. Commissioned 2026-11-11 ~22:4x AEDT by the Mac mini Wednesday seat (21:5x seat). Batched under the 2026-09-18 minimise-duplication rule: the four write disjoint paths (the seat's census, 11:43:31Z; re-measure it).

Common rules: the tier-2 shape of /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-10_gate306-tier2-pr2166-2169/commission.md (read whole; its common-rules pointer and Constraints apply unchanged). Calibration: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_gate307-tier2-pr2170/verdict.md and /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_gate309-tier2-pr2171/verdict.md.

Pins (Wednesday's ls-remote 22:4x AEDT, equal to the READY's 11:43:31Z reads; RE-READ at start and end, say whether each moved):
- develop 2e998b8d9aeaeaa6e87a35d933c6f0445bb981d4
- PR 2172 head b392346f7ab494a3526e862b3a44542f9ccee674
- PR 2173 head 263277643672d02954f155bcdba830f0daed24fb
- PR 2174 head 8879a67709e3754c9dec10ee134ce3f0b8a2fa76
- PR 2175 head c8e3a2f7ddd4d0e7f55f7fb09865ae97a2b3cbea
Every branch is cut on fcd178ff34fa (one commit behind develop). The merge seat squash-merges onto 2e998b8d9aea, so your merge-tree questions are asked onto 2e998b8d9aea.

READY (read whole; reproduce, do not trust): /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-11_gate310-tier2-pr2172-2175/ready_r98_round1.txt. The seat's brief: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-11_seatR98_raise.md (rows 13, 14, 15, 10). Most suite figures in the PR bodies are R 96th's, carried and not re-run by R 98th: treat every one as a claim.

Questions, per PR:
1. File set at the head: exactly the files the READY names (PR files API + a diff read; planted difference control). Zero product bytes for 2172, 2173, 2174; ONE product file for 2175 (mcp-server src/tools/info.ts) plus its new test.
2. Does the change do what its ticket asks and no more? Read each ticket whole on Linear (read-only). Row 14 pins the rule of card secuura-ks2038-who-may-approve-transfers-1106 = a: quote it with `bash /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/tools/decision_queue.sh show secuura-ks2038-who-may-approve-transfers-1106` (read-only verb) and check the pin matches it.
3. RED-FIRST: in YOUR scratch copy, each new or changed cell fails for the right reason without the change (the product line restored for 2175; the scanner line for 2174; the old assertion for 2172 and 2173), and passes at the head. Run the declared file at the head AND the whole service suite (api-gateway, transfer, the bash suite, mcp-server) at the head, against develop's counts. Whole-suite legs only at load1 < 8; if the load does not fall, run the declared files and say which suites were not run.
4. PR 2172 and open PR 2125: 2125 changes api-gateway src/index.ts, which 2172's cells mount and read. Run 2172's file on 2125's head merged with 2172 in your copy and report whether it still passes (UNMEASURED by the seat).
5. PR 2175: the constant reason the tools now return, the real error going to the log only, and nothing secret logged; register.ts and verify.ts out of the diff (the seat's flag): say whether they hold the same defect, a FINDING for the board seat, not this PR's fix.
6. Bodies: title 'Refs KS-NNNN:'; no closing word in closing form in title, body, commit or comments; what was carried vs run named honestly.
7. Merge tree of each PR onto 2e998b8d9aea: clean, with a planted conflict control; no other open PR touches any of the write paths.
Constraints: read-only on the Secuura checkout (ls-remote, show, log, diff, ls-tree, cat-file, grep only, with GIT_OPTIONAL_LOCKS=0; fetch or clone into YOUR scratchpad only); no push, no merge, no board/Linear/GitHub writes, no mail; never print secrets; no cd; quoted heredocs; never rm.
OUTPUT: verdict.md in this folder: per PR, GO / GO WITH NOTES / NO GO at its head sha, findings numbered G310-<PR>-N with severity, what you ran (commands + rc + load1), what you did NOT run. Return it in full.
