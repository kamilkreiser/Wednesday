# Gate 279, tier 2 BATCH: PR 2116 (KS-2133, E2), PR 2117 (KS-2134, E3) and PR 2119 (KS-2138 item 1, E4). All three are Seat T 20th's. Commissioned 2026-11-09 12:4x by the 11:4x Wednesday seat.

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at TIER 2 depth (through code: read the diff, check the words are true, re-run the cells with a planted defect of your own). STOP LINE per PR: any product byte means NEEDS TIER 1 for that PR.

Pins (Wednesday's ls-remote at 12:48:22 AEDT; RE-READ at start and end, and say whether each moved):
- develop e028786a092195fe4b10507b995ff145872e0c91 (moved after the READYs were written, most likely the PR 2108 squash; the READYs name b9fd80eee85b)
- PR 2116 head 84401f920af8caa04576a2b3bc9627b640e68a0c (KS-2133, test-only +13/-0, api-gateway spec-reload test; READY /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-20th/evidence/e2/mail/ready_ks2133_body.txt)
- PR 2117 head 0efffbb15fe6d4bde70043ed3b11e7869e56ed34 (KS-2134, test-only +29/-0, auth token pins for lower-cased Google/GitHub tokens; READY .../evidence/e3/mail/ready_ks2134_body.txt)
- PR 2119 head 6facf676e10b93bdc343baef80a5ec1ade1bd087 (KS-2138 item 1 only, doc-only +1/-1, the gate 260 notes docs row, with Wednesday's one-clause G6 rewording applied; READY .../evidence/e4/mail/ready_ks2138_body.txt)

Questions:
1. For each PR, is it test-only or docs-only, with no product byte?
2. PR 2116: the seat says the checker's || mutant reddens both new cells, its length-only and trim-only mutants each redden exactly one, and the unpatched file stays 5 of 5 green; api-gateway goes 1880 -> 1882. Re-run the cells, plant your OWN mutant of the code under test, show which cell goes red, and restore by sha. Are the cell names true?
3. PR 2117: the same claims shape (auth 1837 -> 1839; google-only and github-only mutants). Same checks. The seat also explains an earlier 'red 1 -> 0' as a 5 s timeout flake in two tree-walk cells of ks949, reproduced on untouched develop: is that explanation true (run ks949 on develop yourself)?
4. PR 2119: is the reworded docs row TRUE of the code it describes? Quote that code. The seat reports an issuer opt-out count of 0 at the old base and 1 at the merge and at the cut, portals suite 25 of 25, and the docs-fragments check rc 0 (planted failure rc 1). Items 2 to 4 of KS-2138 are deliberately NOT in this PR: say whether the PR body states that narrowing.
5. Merge tree of each head on develop e028786a0921: rc 0 for each. List any paths the three PRs share with each other, and any open PRs sharing their paths (with a planted control).
6. Words: the PR bodies and the ticket comments the READYs name are true at the heads (if you cannot read them, say NOT TESTED).

Constraints: clone on the boot volume /private/tmp/g279 (no rm; state its size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; load1 under 8; df DevMASTER at start and end.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate279-tier2-pr2116-2117-2119/verdict.md (if your Write is refused, put the whole verdict in your final message). Line 1 exactly: 'PR 2116: <V>; PR 2117: <V>; PR 2119: <V>' with V one of GO | GO WITH NOTES | NO GO | NEEDS TIER 1. Then FOUND / TESTED / HOW (instrument, controls), NOT TESTED, and findings with ids G279-<PR>-<n> and a severity. Findings only; post nothing; mail nothing.
