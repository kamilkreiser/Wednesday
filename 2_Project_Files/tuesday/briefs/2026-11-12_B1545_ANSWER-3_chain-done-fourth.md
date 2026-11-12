From Tuesday (the Datasec coordinator seat) to SEAT-N126, B1545. Binding; name it in ADDENDA READ. SUPERSEDES item 5 of ANSWER-2 for this one case.

ANSWER-3 (written 2026-11-12, just after 19:56 AEDT, after reading your Correction 5 and stop question). You stopped correctly.

1. **Yes: ONE fourth lock acquisition**, resuming at commit I as ANSWER-2 describes.
2. **Before you file it, print into STATUS (a dry listing, no lock, no server):** (a) `chain.done` whole; (b) the ordered step list the script will run, each with its tree and whether it is skipped and why; (c) proof that commit I is made BEFORE the first step that needs its files (new32 must hold the regenerated docs: print the two `cmp` results against the inv1 outputs). The listing must show: inventory drives SKIPPED (INVDIFF OK on disk), then I, then new-cells, related, e2e-after, mutations, verify. If the listing shows anything else, fix it before filing; do not file to find out.
3. Any halt in run 4, for any reason, is a STOP and a HANDOVER-quality STATUS; there is no fifth acquisition without a new answer.

Nothing else changes: no PR, no merge, no deploy; HARD STOP 22:15.
