# Drafter notes, Seat S 84th board brief, 2026-11-16 04:3x AEDT

Output: /Volumes/DevMASTER/WEDNESDAY/2_Project_Files/fleet/briefs_staged/2026-11-16_seatS84_board.md (about 35 KB). Writes: that file and this one only. Linear read-only (key read in-process, never printed). GitHub read-only via gh api (Blockchain's GH_CONFIG_DIR).

## Measured
- Ordinal: history.md `Seat S 84th` 0, `Seat S 83rd` 1 (heading line 21).
- PRs 2242, 2243, 2244, 2245 all merged; develop 42e242166f89; PR 2170 open; develop 13 ahead of k28.
- Controls: idNamespaceCollision 6 issues; fresh token 0/0.
- Queue A: 2 new tickets (K1 Low kyc test gaps + GET read; P1 Medium-proposed upper-case DEK residue), 5 comments (KS-1882, KS-2056, KS-2200, KS-2189, KS-2188). Covered already: gate 369 case fold, ratchet, Akto (KS-1882 16:01Z comment); C 40th (iii) = KS-2200.
- Queue B: only KS-1233 still owed (close under done rule, live TTL -1 read at k28). Ten others already Done; KS-1197, 1934, 1912, 1699 open by S 82nd's reasons. KS-1699 already carries the G364-2239-1 fix (dropped).
- Correction recorded in the brief: GET /api/kyc/user/:userId returns an empty list (count 0), not a failure, on one undecodable row (by reading at 42e242166f89).

## Faults / caveats
- The shared scratchpad lin.py was overwritten by the beside-running K 32nd drafter after my last use; no effect on results (my outputs were saved before).
- Hook advisory: one lowercase-only grep for the ordinal was caught; re-run with /usr/bin/grep -i and a positive control.
- Format: no line in the brief contains the substring "card"; the wallet-connector test file is given by a `cip30` name match, not a full path (resolve at tip).

## UNMEASURED
No suite or tsc run; line numbers are one raw-blob read at 42e242166f89; whether upper-case kyc rows or key rows exist anywhere; which id spelling originate's erasure receives; KS-1233 cell-file pass at develop; the 3 failing check runs at PR 1038's squash; KS-265 title; live floor and mail.
