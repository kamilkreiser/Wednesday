# Gate 280, tier 2: PR 2120 (KS-2129, Seat T 20th's E5). Commissioned 2026-11-09 13:0x by the 11:4x Wednesday seat. A single PR, because no other tier-2 READY is due: T 20th wraps after this, and R 90th's next two are tier 1.

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at TIER 2 depth (through code: read the diff, check the words are true, re-run the cells with a planted defect of your own). STOP LINE: any product byte, or any change to a tool the push hook RUNS (as opposed to a suite that tests it), means NEEDS TIER 1.

Pins (Wednesday's ls-remote at 13:09:38 AEDT; RE-READ at start and end, and say whether each moved):
- develop e028786a092195fe4b10507b995ff145872e0c91
- PR 2120 head f5aec11944e8ad6b8e238044c7ca36343bf4cb24 (KS-2129, bash suite only, +19/-2; branch feature/ks-2129-suite-the-grep-q-scanner-misses-five)

READY claims (untested by Wednesday; read whole): /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-20th/evidence/e5/mail/ready_ks2129_body.txt . Ticket comment d1750fe1.

Questions:
1. Is it suite-only, with no product byte and no change to a script the hook runs? Name every changed path.
2. The seat says: suite 29 -> 31 with 0 failed; five sibling suites byte-identical (151 cells); the checker's five-file plant gives 6 FAIL lines on the patched suite, and each script alone reddens its own named cell; four of the five single plants leave the unpatched suite 29 of 29 green. Re-run the suite on develop and at the head. Plant your OWN defect of the kind the new cells exist to catch (a grep -q scan that misses a file) and show the named cell goes red; restore by sha. Which of the five single plants does the UNPATCHED suite already catch, and is that stated honestly?
3. Are the cell names true?
4. Merge tree of the head on develop e028786a0921 (rc and tree). Open PRs sharing its paths, with a planted control. Note that PR 2114 (KS-2141) also edits a bash suite in the same scripts/__tests__ family: say whether they share a file.
5. Words: the PR body and ticket comment d1750fe1 are true at the head (if you cannot read them, say NOT TESTED).

Constraints: clone on the boot volume /private/tmp/g280 (no rm; state its size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; keep load1 under 8 (do NOT stress the machine on purpose this time); df DevMASTER at start and end.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate280-tier2-pr2120-ks2129/verdict.md (if your Write is refused, put the whole verdict in your final message). Line 1 exactly: 'PR 2120: <V>' with V one of GO | GO WITH NOTES | NO GO | NEEDS TIER 1. Then FOUND / TESTED / HOW (instrument, controls), NOT TESTED, and findings with ids G280-<n> and a severity. Findings only; post nothing; mail nothing.
