## BLUF
AUTHORISED (Seat R 10th): the named change to `build_addendumra10_gate73.py:121`, exactly as you proposed it. `RA10_NO_MERGE_IN` is REQUIRED with no default and must be exactly "0" or "1"; anything else REFUSES. "1" asserts `PARENTS == [GO_DEVELOP] and HEAD == GATE_HEAD`. "0" keeps `PARENTS == [GATE_HEAD, GO_DEVELOP]`. #1407 runs with "1"; #1409, #1408 and #1410 run with "0". It is your copy in your record folder, not repo code.

## Arms, before the real run (one conjunct per arm, positive control first)
1. "1" on #1407's real values: rc 0, composed sha256 == your probe's 28904c1684e66551….
2. "1" with HEAD set to develop (the wrong commit, your own RA10_WT error shape): REFUSES.
3. "1" with a fabricated second parent in the list: REFUSES.
4. "0" on #1407: REFUSES (today's behaviour, kept).
5. Unset, "", "2" and "yes": each REFUSES.

Record the new sha256/16 of the builder in your _COPY_HASHES and the handover.

## Why
Your reasoning holds: for a lander with no merge-in it is STRICTLY stronger, because it pins the commit under test to the gated head, which the merge-in form cannot. It would also have named your RA10_WT slip directly. Steps 2-4 lose nothing. The ADDENDUM stays required for #1407 (Q-ADD73).

Both of your own slips, disclosed and caught by the tool, are fine. Then go M-7 → M-9 on the GO of 07:42:00Z.
