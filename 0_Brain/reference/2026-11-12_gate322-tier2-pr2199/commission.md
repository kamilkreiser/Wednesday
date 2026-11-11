# Gate 322, TIER 2 (Sonnet; routing v1.0 tier-2 row: a test pin + one doc sentence, no service source). Seat A 23rd's row KS-2170 = PR 2199. Commissioned 2026-11-12 ~10:0x AEDT by the 07:51 Wednesday seat.

Method: copy-and-change of `/Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-12_gate320-tier2-pr2196/commission.md`. Read it whole: its Constraints, output shape and controls all apply. Calibration: gate 320's verdict.md.

Pins (Wednesday's ls-remote ~10:0x; RE-READ at start and end): develop d35f75875275158ce3b20b636b4198a4c8834968; refs/pull/2199/head 4a0a166b95a1c1c14c7813604ecff1b14db0bfb1. The branch was cut on c78c80bd5370. develop has since moved by PR 2186 (one test file), so merge-tree onto d35f75875275.

READY (read whole; reproduce, do not trust): ready_a23_ks2170_mail.txt in THIS folder.

What the row claims:
- `Blockchain/Dev/packages/shared/src/__tests__/ks1725-zod3-compat.test.ts`: the zod3Issues call-site pin moves 113 -> 114. PR 2182 (KS-2055) added the 114th site.
- A second commit changes the flow fragment `KS-1725-zod-4-with-a-zod-3-issue-layer.html` line 3 from "113" to "114".

Questions:
1. Count the wrapped `zod3Issues(` call sites at develop d35f75875275 with the TEST'S OWN walk (never a hand grep; rule: never re-implement a tool's method). Is it 114? A planted 115th must turn the cell red.
2. Is the fragment sentence now true, and does docs-fragments check pass (a planted defect must exit 1)?
3. PR 2079 (KS-657) edits the F2 file-count floor of the same test file in a disjoint hunk; Wednesday WAIVED it. Reproduce: `git merge-file` of the file in both orders, 0 conflicts. Also measure what Wednesday left unmeasured: the count and the F2 floor on a merged result of 2199 + 2079's head.
4. The two held KS-2055 READYs (O141, O142) each add one zod3Issues site in services/transfer/src/index.ts. Say whether they are already in develop through PR 2182 (diff them against develop's transfer index.ts). If not, raising either would make the count 115. That is a finding for Wednesday, not a defect of this PR.
5. Census on the two paths (GraphQL, with a control).

Spark shadow after your verdict: run spark_gate.sh / spark_review.py with --pr-body-file, in the session scratchpad.

OUTPUT: verdict.md in THIS folder. First line: 'PR 2199: GO / GO WITH NOTES / NO GO (at head ...; tier 2)'. Findings G322-2199-N, graded. NOT TESTED. The Spark shadow result. If your Write is refused, return the text in full.

Constraints: exactly gate 320's. DevMASTER has dropped four times today (enclosure power). If it drops, wait, re-read what you wrote, then resume.
