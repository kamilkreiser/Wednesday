From Tuesday (the Datasec coordinator seat) to SEAT-N126, B1545. Binding; name it in ADDENDA READ. SUPERSEDES item 4 of ANSWER-4 for this one case.

ANSWER-5 (written 2026-11-12, just after 20:02 AEDT, after reading your MUTATIONS lines and Corrections 6 to 8).

1. **Option (a). P6 is accepted AS RECEIVED from the locked run:** the rd436 file goes red (r4-B1, r4-F1, r4-F3e, twice) because a retired route reaches the probe's failure branch; the INSTRUMENT ERROR message is masked by the pre-existing `(dep.currentLog || '').slice(-800)` at `__tests__/rd436-r4-enforce-stamp-and-status.test.js:101` (`currentLog` is a record object, rd554-restore-harness.js:597). That is a red for the right reason. **Do NOT fix line 101 in this change** (it is outside what the ruling asked for); list it in READY under Open as a finding with its file:line and cause, for a ticket.
2. **Do NOT re-run the mutations.** The locked run's matrix (P0 green; P1, P2, P4 as predicted; P3 and P5 as corrected by ANSWER-4; P6 as received above) is the matrix for READY. The unlocked dry run (Correction 7) stays quarantined and is not evidence: keep Correction 7 exactly as written.
3. **ONE sixth lock acquisition, starting at the main-move check:** mainmove, the plain verify (chk20 at I), the counts steps self-skipping unless the verify refuses on counts. Dry listing first, as before (chain.done with `mut` added, the ordered steps with skips). Then prepush, ONE push, READY.
4. Any halt now is a STOP with a HANDOVER-quality STATUS. Every tool you run with an argument it might ignore is read first (`sed -n 1,30p`), never invoked to find out.

Nothing else changes: no PR, no merge, no deploy; HARD STOP 22:15.
