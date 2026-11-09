# Gate 277, tier 2 BATCH: PR 2114 (KS-2141, Seat R 90th) + PR 2115 (KS-2132, Seat T 20th's E1). Commissioned 2026-11-09 11:3x by the 10:01 Wednesday seat.

Common rules: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-07_gate_tier1_common.md, read whole, applied at TIER 2 depth (through code: diff read, words true, cells re-run with a planted defect of your own). STOP LINE per PR: any product byte = NEEDS TIER 1 for that PR.

Pins (Wednesday's ls-remote 11:3x; RE-READ at start and end, and say whether each moved):
- develop 2a031f51403f107e7a062f9cf4ce3a68650e2c82 (PR 2109 squash)
- PR 2114 head 39be43e5cc63d9d486652fd4cbe2d1fb598e1b05 (KS-2141: the ks1560 jq-link census suite + two fragments, +70/-4; READY in Wednesday's inbox, R 90th record /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatR-90th/)
- PR 2115 head e9a127267f97dc7bea7cbd0a7ce849d0389ecdf8 (KS-2132: api-gateway ks1534 allow-list test, +3/-0; READY /Volumes/DevMASTER/!CODING/Secuura/Blockchain/5_Project_History/2026-11-09_seatT-20th/evidence/e1/mail/ready_ks2132_body.txt)

Questions:
1. Test-only / docs-only for each PR: no product byte (PR 2114 may touch only the suite and its two KS-2141 fragments).
2. PR 2114: the new links_jq predicate judges a link when, and only when, an `ln` command with a symlink flag names bin/jq as its destination. Re-run the suite (cells F-2078-1 x2, F-2078-2, and the census CELL 2 offenders must be empty); plant your OWN mutant of the predicate (e.g. drop the comment strip) and show the named cell goes red; restore by sha. The seat's hand change rewrote the paragraph above links_jq (quoted in its READY): is it TRUE of the code under it? Its UNMEASURED destination-directory spelling ("$root/bin/") stated as not covered.
3. PR 2115: the seat reports api-gateway 1880 -> 1880 cells with +3 lines and two mutants (skip-last-of-3+, skip-last-of-5+) turning R1-R5 red. Establish exactly WHAT the +3 lines strengthen (new assertions inside existing cells? new inputs?) and whether the cell names are true; plant your own mutant of the allow-list read that the new lines exist to catch; restore by sha.
4. Merge tree of each head on develop 2a031f51403f: rc 0 each; the two PRs share no path (list); open PRs sharing either PR's paths (planted control).
5. Words: PR bodies and the ticket comments named in the READYs are true at the heads (if you cannot read them, say NOT TESTED).

Constraints: clone on the boot volume /private/tmp/g277 (QA no-rm; name its size at the end); never cd; no git write verb in any /Volumes/DevMASTER/!CODING checkout; load1 under 8; df DevMASTER at start and end.

Output: /Volumes/DevMASTER/WEDNESDAY/0_Brain/reference/2026-11-09_gate277-tier2-pr2114-pr2115/verdict.md (or the whole verdict in your final message if the Write is refused). Line 1 exactly: 'PR 2114: <V>; PR 2115: <V>' with V one of GO | GO WITH NOTES | NO GO | NEEDS TIER 1. Then FOUND / TESTED / HOW (instrument, controls), NOT TESTED, findings with ids G277-<PR>-<n> and severity. Findings only; post nothing; mail nothing.
