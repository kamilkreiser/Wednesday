Seat S 8th

## BLUF
MERGE GO #1823 at head 0d134803b6f28da2028f6b5211aaf9f1c2153360 onto develop 530f091120d5. Squash, pinned to that head (--match-head-commit). Then mail MERGED with the squash SHA, and start #1824's docs-only merge-in.

## Verified by Wednesday at source (own scratch clone, fetch rc 0, in this action)
- pull/1823/head = 0d134803b6f2; parents 3952a5852539 (the gated head) + 530f091120d5 (develop); develop is an ancestor (merge-base rc 0).
- Three-dot file set against develop = exactly your five paths (gdpr.ts, ks445 + ks1780 tests, the two html docs).
- Gated head vs new head differ ONLY in the two html docs plus certifications.ts and the ks1666 test, which are develop's (#1822) arriving through the merge: gdpr.ts and both tests are byte-equal to the gated head.
- Gate 27 TIER 1 GO WITH NOTES, fix-before-merge (none); completion check passed earlier (KS-1798 + KS-1799).

## Authority
Kam 2026-09-11 17:50, verbatim: "you also have my approval to merge anything that has been finished and tested". Tested = gate 27 at the gated head + this check of the merge-in.

## Steps
1. Re-read develop by ls-remote immediately before the merge. If it is no longer 530f091120d5, STOP and mail (do not merge).
2. Squash-merge with --match-head-commit 0d134803b6f28da2028f6b5211aaf9f1c2153360.
3. Read back: develop's new SHA, one parent 530f091120d5, its tree equal to the head's tree. Mail MERGED.
4. Then #1824: docs-only merge-in of the new develop, READY TO MERGE (same blob-table shape). Then #1825 with its comment fix round in the same push.

Wednesday
